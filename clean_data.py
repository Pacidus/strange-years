import sys
import polars as pl

match sys.argv:
    case ["clean_data.py", folder]:
        pass
    case ["clean_data.py"]:
        folder = "./"

print(f"Les fichier à modifier sont stoquées dans '{folder}'.")

df = pl.scan_csv(
    f"{folder}/*.txt",
    has_header=False,
    new_columns=["full_str"],
    separator="\n",
)

print("Lazy loading done.")

widths = [80, 1, 8, 5, 30, 30, 8, 5, 30]
column_names = [
    "noms",
    "sexe",
    "date naissance",
    "code location naissance",
    "commune naissance",
    "pays naissance",
    "date décès",
    "code location décès",
    "numéro acte décès",
]


# Calculate slice values from widths.

print("Recover fields")
slice_tuples = []
idx = 0
for i in widths:
    slice_tuples.append([idx, i])
    idx += i

df = df.with_columns(
    [
        pl.col("full_str").str.slice(i, w).str.strip_chars().alias(col)
        for (i, w), col in zip(slice_tuples, column_names)
    ]
).drop("full_str")

print("Converting fields")

df = df.with_columns(
    [pl.col("noms").str.strip_chars("/").str.split("*").alias("nn")]
).drop("noms")

df = df.with_columns(
    [
        pl.col("nn").list.get(-2, null_on_oob=True).alias("Noms"),
        pl.col("nn").list.get(-1).str.split(" ").alias("Prenoms"),
    ]
).drop("nn")


df = df.select(
    [
        "Noms",
        "Prenoms",
        pl.col("sexe").cast(pl.UInt8).alias("Sexe"),
        pl.col("date naissance")
        .str.pad_end(8, "0")
        .str.to_date("%Y%m%d", strict=False)
        .alias("Date_naissance"),
        pl.col("code location naissance").alias("Code_location_naissance"),
        pl.col("commune naissance").alias("Commune_naissance"),
        pl.col("pays naissance").alias("Pays_naissance"),
        pl.col("date décès")
        .str.pad_end(8, "0")
        .str.to_date("%Y%m%d", strict=False)
        .alias("Date_décès"),
        pl.col("code location décès").alias("Code_location_décès"),
        pl.col("numéro acte décès").alias("Numéro_acte_décès"),
        pl.col("date décès").str.pad_end(8, "0"),
        pl.col("date naissance").str.pad_end(8, "0"),
    ]
)


def repair(name):
    col = pl.col(name)
    Y = col.str.slice(0, 4)
    m = col.str.slice(4, 2).cast(pl.UInt8)
    d = col.str.slice(6, 2).cast(pl.UInt8)
    m = pl.when(m == 0).then(pl.lit(1)).otherwise(m)
    m = pl.when(m >= 13).then(pl.lit(12)).otherwise(m)
    d = pl.when(m == 2, d >= 29).then(pl.lit(28)).otherwise(d)
    d = pl.when(m != 2, d >= 31).then(pl.lit(30)).otherwise(d)
    d = pl.when(d == 0).then(pl.lit(1)).otherwise(d)
    m = m.cast(pl.String).str.zfill(2)
    d = d.cast(pl.String).str.zfill(2)
    return (Y + m + d).str.to_date("%Y%m%d")


Dn = pl.col("Date_naissance").is_null()
Dd = pl.col("Date_décès").is_null()

df = df.with_columns(
    [
        pl.when(Dn)
        .then(repair("date naissance"))
        .otherwise("Date_naissance")
        .alias("Date_naissance"),
        pl.when(Dd)
        .then(repair("date décès"))
        .otherwise("Date_décès")
        .alias("Date_décès"),
    ]
).drop(["date décès", "date naissance"])

print("Resolving schema")

df.collect_schema()

print("Reading and writting file")

df.sink_parquet("all_décès.parquet", maintain_order=False)
