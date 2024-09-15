import numpy as np
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="dark")
plt.style.use('dark_background')
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": "Computer Modern",
    "font.sans-serif": "Helvetica",
    "axes.axisbelow" : True
})

ms_year = 1000 * 86400 * 365.25

df = pl.scan_parquet("all_décès.parquet")

# remove all the uncanny dates

sex = pl.col("Sexe")
dd = pl.col("Date_décès")
dn = pl.col("Date_naissance")
Age = (dd - dn).alias("Age").cast(pl.Int64)/ms_year


yn = dn.dt.year()
yd = dd.dt.year()

uncanny = (yd <= 2023) & (yd >= 1970) & (dd >= dn) & (yn <= 2023) & (yn >= 1870)
df = df.filter(uncanny)

data = df.select([
    sex,
    dn,
    dd,
    Age,
    
]).collect()

yd = data["Date_décès"].dt.year()
yn = data["Date_naissance"].dt.year()
Yd, Nd = np.unique(yd, return_counts=True)
Yn, Nn = np.unique(yn, return_counts=True)


fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
fig.set_size_inches(12, 4)

ax1.bar(Yn, Nn, 1, color="#559")
ax1.legend(["Birth years of the desceased"])
ax1.grid(linestyle="--")
ax1.set_ylabel("Number")
ax1.set_xlabel("Year")

ax2.bar(Yd, Nd, 1, color="#644")
ax2.legend(["Years of the deaths"])
ax2.grid(linestyle="--")
ax2.set_xlabel("Year")
fig.savefig("figures/year_dist.svg")
plt.show()

md = yd.min()
mn = yn.min()
D = (yd - md).to_numpy()
N = (yn - mn).to_numpy()
rd, rn = D.max() + 1, N.max() + 1
count = np.bincount(D + N*rd,  minlength=rn*rd)
count = count.reshape(rn, rd).T

kwargs = {
        "frameon" : False,
        "xmargin" : 0,
        "ymargin" : 0,
        }

fig = plt.figure()
fig.set_size_inches(8, 8)
ax1 = fig.add_axes((0.1,0.1,0.7,0.7))
ax1.set_xlabel("Birth year")
ax1.set_ylabel("Death year")
ax2 = fig.add_axes((0.1,0.8,0.7,0.18), sharex=ax1, **kwargs)
ax3 = fig.add_axes((0.8,0.1,0.1,0.7), sharey=ax1, **kwargs)
ax4 = fig.add_axes((0.91,0.1,0.02,0.7))

plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)
ax2.bar(Yn, Nn, 1, color="#559")
ax3.barh(Yd, Nd, 1, color="#644")

cm = ax1.pcolor(np.arange(mn, mn+rn+1) - 0.5, np.arange(md, md+rd+1) - 0.5, count, cmap="nipy_spectral")
ax1.set_xlim(1891, 2023)
ax1.set_ylim(1972, 2023)

fig.colorbar(cm, cax=ax4)
fig.savefig("figures/year_dist_2D.svg")
plt.show()