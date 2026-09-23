"""Fig. S1: phase diagram in (p, r) with the boundaries r = q and r = r*(p)."""
from mta.theory import r_star
from mta.viz import CB, C_LINE, C_VIS, render
import numpy as np


def draw(ax):
    ps = np.linspace(0.5001, 0.9999, 600)
    q_curve = 1.0 - ps
    rstar_curve = np.array([r_star(p) for p in ps])

    ax.fill_between(ps, 0, rstar_curve, color=CB[0], alpha=0.22, lw=0)
    ax.fill_between(ps, rstar_curve, q_curve, color=CB[1], alpha=0.28, lw=0)
    ax.fill_between(ps, q_curve, 0.5, color="0.9", alpha=0.9, lw=0)
    ax.plot(ps, q_curve, color=C_LINE, lw=1.6, label=r"$r=q=1-p$")
    ax.plot(ps, rstar_curve, color=C_VIS, lw=2.0, label=r"$r=r^{*}(p)$")
    ax.axvline(0.8, color=C_LINE, lw=0.9, ls=(0, (4, 3)))
    ax.plot([0.8], [0.0], marker="o", ms=5, color=C_VIS, zorder=5)
    ax.text(0.6, 0.1, "Faster than\npanel", ha="center", va="center", color="0.2")
    ax.text(0.72, 0.20, "Inevitable,\nbut slower", ha="center", va="center", color="0.2")
    ax.text(0.9, 0.3, "Not\ninevitable", ha="center", va="center", color="0.4")
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(0.0, 0.5)
    ax.set_xlabel(r"Adviser accuracy  $p$")
    ax.set_ylabel(r"Dissent threshold  $r$")
    ax.legend(loc="upper right", frameon=True, framealpha=0.95)


if __name__ == "__main__":
    render(draw, "figS1_phase", (5.8, 4.8))
