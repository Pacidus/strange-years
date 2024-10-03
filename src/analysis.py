import numpy as np
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt


###############
## Functions ##
###############

def recover_year(dta):
    yd = dta["Date_décès"].dt.year()
    yn = dta["Date_naissance"].dt.year()

    year = {
        "Death" : np.unique(yd, return_counts=True),
        "Born" : np.unique(yn, return_counts=True),
        "data_d" : yd.to_numpy(),
        "data_n" : yn.to_numpy(),
    }
    return year

def plot_2D(fig): 
    kwargs = {
        "frameon": False,
        "xmargin": 0,
        "ymargin": 0,
    }

    ax1 = fig.add_axes((0.1, 0.1, 0.7, 0.7))
    ax1.set_xlabel("Birth year")
    ax1.set_ylabel("Death year")
    ax2 = fig.add_axes((0.1, 0.8, 0.7, 0.18), sharex=ax1, **kwargs)
    ax3 = fig.add_axes((0.8, 0.1, 0.1, 0.7), sharey=ax1, **kwargs)
    ax4 = fig.add_axes((0.91, 0.1, 0.02, 0.7))

    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)
    
    return ax1, ax2, ax3, ax4

def fig_histogram(dta):
    year = recover_year(dta)

    Yn, Nn = year["Born"]
    Yd, Nd = year["Death"]

    fig = plt.figure()
    fig.set_size_inches(12, 4)
    ax1 = fig.add_axes((0.07, 0.12, 0.42, 0.86))
    ax2 = fig.add_axes((0.51, 0.12, 0.42, 0.86), sharey=ax1)
    plt.setp(ax2.get_yticklabels(), visible=False)

    ax1.bar(Yn, Nn, 1, color="#559")
    ax1.legend(["Birth year of the desceased"])
    ax1.grid(linestyle="--")
    ax1.set_ylabel("Number")
    ax1.set_xlabel("Year")

    ax2.bar(Yd, Nd, 1, color="#644")
    ax2.legend(["Year of death"])
    ax2.grid(linestyle="--")
    ax2.set_xlabel("Year")
    return fig


def fig_2Dhist(dta, kw=dict()):
    if "cmap" not in kw:
        kw["cmap"] = "nipy_spectral"
    if "rasterized" not in kw:
        kw["crasterized"] = True

    year = recover_year(dta)
    Yn, Nn = year["Born"]
    Yd, Nd = year["Death"]
    
    md = Yd[0]
    mn = Yn[0] 

    D = year["data_d"] - md
    N = year["data_n"] - mn
    rd, rn = Yd[-1] - md + 1, Yn[-1] - mn + 1
    count = np.bincount(D + N * rd, minlength=rn * rd)
    count = count.reshape(rn, rd).T


    fig = plt.figure() 
    fig.set_size_inches(8,8)
    ax1, ax2, ax3, ax4 = plot_2D(fig)

    ax2.bar(Yn, Nn, 1, color="#559")
    ax3.barh(Yd, Nd, 1, color="#644")

    X, Y = np.arange(mn, mn + rn + 1) - 0.5, np.arange(md, md + rd + 1) -0.5
    cm = ax1.pcolormesh(X, Y, count, , **kw)

    ax1.set_xlim(1891, 2023)
    ax1.set_ylim(1972, 2023)

    fig.colorbar(cm, cax=ax4)
    return fig


############################
## Setup plots parameters ##
############################

sns.set_theme(style="dark")
plt.style.use("dark_background")
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": "Computer Modern",
        "font.sans-serif": "Helvetica",
        "axes.axisbelow": True,
    }
)

###############################
## Data recovery and parsing ##
###############################

# Constents

# Number of ms in one tropical year
ms_year = 1000 * 86400 * 365.24219

# Data
df = pl.scan_parquet("all_décès.parquet")

# Remove all the uncanny dates
sex = pl.col("Sexe")
dd = pl.col("Date_décès")
dn = pl.col("Date_naissance")
Age = (dd - dn).alias("Age").cast(pl.Int64) / ms_year


yn = dn.dt.year()
yd = dd.dt.year()

uncanny = (yd <= 2023) & (yd >= 1970) & (dd >= dn) & (yn <= 2023) & (yn >= 1870)
df = df.filter(uncanny)

# Recover data
data = df.select(
    [
        sex,
        dn,
        dd,
        Age,
    ]
).collect()


##################
## Plot figures ##
##################


# Death Birth comparaison without gender
fig = fig_histogram(data)
fig.savefig("figures/year_dist.svg")
plt.show()

# 2D distributions
fig = fig_2Dhist(data)
fig.savefig("figures/year_dist_2D.svg")
plt.show()

# Gender based figures
kw = {
    "vmin": 0,
    "vmax": 16400,
}
# Death Birth comparaison for male
dta = data.filter(pl.col("Sexe") == 1)

fig = fig_histogram(dta)
fig.savefig("figures/M_year_dist.svg")
plt.show()

# 2D distributions
fig = fig_2Dhist(dta, kw)
fig.savefig("figures/M_year_dist_2D.svg")
plt.show()

# Death Birth comparaison for female
dta = data.filter(pl.col("Sexe") == 2)

fig = fig_histogram(dta)
fig.savefig("figures/F_year_dist.svg")
plt.show()

# 2D distributions
fig = fig_2Dhist(dta, kw)
fig.savefig("figures/F_year_dist_2D.svg")
plt.show()
