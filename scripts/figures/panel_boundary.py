"""Fig. 3a: the convergence rates R_vis = log(1/p) and R_agg = (1/2) log(1/4pq)
against p, crossing at p = 4/5."""
from mta.theory import Rate_agg, Rate_vis
from mta.viz import C_AGG, C_LINE, C_VIS, render
import numpy as np


def draw(ax):
    ps = np.linspace(0.5001, 0.9999, 800)
    rvis = np.array([Rate_vis(0.0, p) for p in ps])
    ragg = np.array([Rate_agg(p) for p in ps])

    ax.plot(ps, rvis, color=C_VIS, lw=2.0,
            label=r"$\mathrm{R}_{\mathrm{vis}}$ ($\geq 2$) $=\log(1/p)$")
    ax.plot(ps, ragg, color=C_AGG, lw=2.0,
            label=r"$\mathrm{R}_{\mathrm{agg}}=\frac{1}{2}\log\frac{1}{4pq}$")
    ax.axvline(0.8, color=C_LINE, lw=0.9, ls=(0, (4, 3)))
    ax.plot([0.8], [Rate_agg(0.8)], marker="o", ms=6, color=C_LINE, zorder=6)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(0.0, 1.5)
    ax.set_xlabel(r"Adviser accuracy  $p$")
    ax.set_ylabel("Convergence rate")
    ax.legend(loc="upper left", frameon=True, framealpha=0.95)


if __name__ == "__main__":
    render(draw, "panel_boundary", (5.8, 4.8))
