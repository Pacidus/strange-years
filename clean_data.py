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
        (pl.col("nn").list.get(-1).str.split(" ").alias("Prenoms")),
    ]
).drop("nn")


def repair(name):
    col = pl.col(name)
    col = pl.when(col.str.len_chars() == 0).then(pl.lit("19700101"))
    Y = col.str.slice(0, 4)
    m = col.str.slice(4, 2).cast(pl.UInt8)
    d = col.str.slice(6, 2).cast(pl.UInt8)
    m = pl.when(m == 0).then(pl.lit(1))
    m = pl.when(m >= 13).then(pl.lit(12))
    d = pl.when(m == 2, d >= 29).then(pl.lit(28))
    d = pl.when(m >= 1, d >= 31).then(pl.lit(30))
    d = pl.when(d == 0).then(pl.lit(1))
    m = m.cast(pl.String).str.zfill(2)
    d = d.cast(pl.String).str.zfill(2)
    return (Y + m + d).str.to_date("%Y%m%d")


df = df.select(
    [
        "Noms",
        "Prenoms",
        pl.col("sexe").cast(pl.UInt8).alias("Sexe"),
        pl.col("date naissance")
        .str.to_date("%Y%m%d", strict=False)
        .fill_null(repair("date naissance"))
        .alias("Date_naissance"),
        pl.col("code location naissance").alias("Code_location_naissance"),
        pl.col("commune naissance").alias("Commune_naissance"),
        pl.col("pays naissance").alias("Pays_naissance"),
        pl.col("date décès")
        .str.to_date("%Y%m%d", strict=False)
        .fill_null(repair("date décès"))
        .alias("Date_décès"),
        pl.col("code location décès").alias("Code_location_décès"),
        pl.col("numéro acte décès").alias("Numéro_acte_décès"),
    ]
)

print("Resolving schema")

df.collect_schema()

print("Reading and writting file")

df.sink_parquet("all_décès.parquet", maintain_order=False)
