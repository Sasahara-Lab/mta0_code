"""Fig. 2a-c: P_agg and P_vis against K at adviser accuracy p0."""
from mta.theory import P_agg, P_vis
from mta.viz import C_AGG, C_VIS, KS, lineplot, render
import numpy as np


def draw(ax, p0=0.7):
    pa = np.array([P_agg(K, p0) for K in KS])
    pv = np.array([P_vis(K, p0) for K in KS])

    lineplot(ax, KS, pa, color=C_AGG, marker="o", markersize=4, lw=1.8,
             label=r"$P_{\mathrm{agg}}$")
    lineplot(ax, KS, pv, color=C_VIS, marker="o", markersize=4, lw=1.8,
             label=r"$P_{\mathrm{vis}}$ ($\geq 2$)")
    ax.axhline(1.0, color="0.7", ls=":")
    ax.text(0.97, 0.04, fr"$p={p0:g}$", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=11, color="0.25")
    ax.set_xlim(2, 30)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Number of advisers  $K$")
    ax.set_ylabel("Probability")
    ax.legend(loc="center right")


if __name__ == "__main__":
    render(draw, "panel_decoupling", (5.8, 4.6))
