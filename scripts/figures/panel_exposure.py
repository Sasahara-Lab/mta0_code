"""Fig. 2d: heatmap of P_vis over (K, p)."""
from mta.theory import P_vis
from mta.viz import CMAP_VIS, KS, render
import numpy as np


def draw(ax):
    pgrid = np.linspace(0.55, 0.97, 80)
    Z = np.array([[P_vis(K, p) for K in KS] for p in pgrid])

    Kedges = np.arange(1.5, 31.5, 1.0)
    pedges = np.linspace(pgrid[0] - (pgrid[1] - pgrid[0]) / 2,
                         pgrid[-1] + (pgrid[1] - pgrid[0]) / 2, len(pgrid) + 1)
    pm = ax.pcolormesh(Kedges, pedges, Z, cmap=CMAP_VIS, vmin=0, vmax=1,
                       shading="auto", rasterized=True)
    cs = ax.contour(KS, pgrid, Z, levels=[0.5, 0.7, 0.9], colors="white",
                    linewidths=0.8, alpha=0.85)
    ax.clabel(cs, fmt=lambda v: f"{int(v*100)}%", inline=True)

    cb = ax.figure.colorbar(pm, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label(r"$P_{\mathrm{vis}}\ (\geq 2)$")
    ax.set_xlim(2, 30)
    ax.set_ylim(0.55, 0.97)
    ax.set_xlabel(r"Number of advisers  $K$")
    ax.set_ylabel(r"Adviser accuracy  $p$")


if __name__ == "__main__":
    render(draw, "panel_exposure", (6.6, 4.7))
