"""Fig. S2, step 2: (a) simulated dissent rate and (b) all-wrong rate of the
correlated panels against the independence baselines, from data/raw/figS2_nullmodel.csv."""
import csv
import os

import matplotlib.pyplot as plt

from mta import ROOT
from mta.theory import P_vis
from mta.viz import CB, lineplot, setup_theme, save

DATA = os.path.join(ROOT, "data", "raw", "figS2_nullmodel.csv")
RHOS = (0.2, 0.5)
RHO_COLORS = {0.2: CB[1], 0.5: CB[3]}


def load():
    """Returns (Ks, p, dissent, allwrong); the last two map rho -> list over Ks."""
    if not os.path.exists(DATA):
        raise FileNotFoundError(f"{DATA}: run scripts/run_figS2_nullmodel.py first")
    with open(DATA) as f:
        rows = list(csv.DictReader(f))
    Ks, p = [int(r["K"]) for r in rows], float(rows[0]["p"])
    dissent, allwrong = {r: [] for r in RHOS}, {r: [] for r in RHOS}
    for row in rows:
        for r in RHOS:
            dissent[r].append(float(row[f"rho_{r}"]))
            allwrong[r].append(float(row[f"allwrong_{r}"]))
    return Ks, p, dissent, allwrong


def _mark_kstar14(ax):
    ax.axvline(14, color="0.4", lw=0.9, ls=(0, (2, 3)), zorder=1)
    ax.text(14, 1.02, r"$K^{*}(0.7)=14$", color="black",
            ha="center", va="bottom", fontsize=9,
            transform=ax.get_xaxis_transform(), clip_on=False)


def draw_dissent(ax, Ks, p, dissent):
    lineplot(ax, Ks, [P_vis(K, p) for K in Ks], color=CB[0], lw=2.4, zorder=5,
             label="independence baseline")
    for r in RHOS:
        lineplot(ax, Ks, dissent[r], color=RHO_COLORS[r],
                 lw=2.0, linestyle="--", marker="o", markersize=4,
                 label=fr"$\rho={r}$")
    _mark_kstar14(ax)
    ax.set_xlabel("Number of advisers $K$")
    ax.set_ylabel(r"$P_{\rm vis}$")
    ax.set_ylim(0, 1.03)
    ax.set_xlim(2, 30)
    ax.grid(alpha=.25)
    ax.legend(loc="lower right", framealpha=.95)


def draw_allwrong(ax, Ks, p, allwrong):
    q = 1.0 - p
    lineplot(ax, Ks, [q**K for K in Ks], color=CB[0], lw=2.4, zorder=5,
             label=r"independence baseline $q^{K}$")
    for r in RHOS:
        lineplot(ax, Ks, allwrong[r], color=RHO_COLORS[r],
                 lw=2.0, linestyle="--", marker="o", markersize=4,
                 label=fr"$\rho={r}$")
    ax.set_yscale("log")
    _mark_kstar14(ax)
    ax.set_xlabel("Number of advisers $K$")
    ax.set_ylabel(r"All-wrong unanimity  $P(Y=0)$")
    ax.set_ylim(1e-12, 0.3)
    ax.set_xlim(2, 30)
    ax.grid(alpha=.25)
    ax.legend(loc="lower left", framealpha=.95)


def main():
    Ks, p, dissent, allwrong = load()
    setup_theme()
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.3))
    draw_dissent(axes[0], Ks, p, dissent)
    draw_allwrong(axes[1], Ks, p, allwrong)
    for ax, lab in zip(axes, "ab"):
        ax.set_title(lab, loc="left", weight="bold")
    fig.tight_layout(w_pad=2.4)
    save(fig, "figS2_nullmodel_illustration")


if __name__ == "__main__":
    main()
