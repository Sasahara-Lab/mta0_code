"""Fig. 3b: the disclosure reference scale K*(p), drawn through its inverse p_K
(the accuracy at which K* equals exactly K)."""
import numpy as np
from scipy.optimize import brentq

from mta.theory import log1m_P_vis, log1m_P_agg
from mta.viz import C_LINE, C_VIS, render


def _p_of_K(K):
    """Root of P_vis(K, p) = P_agg(K, p), found on the log residuals."""
    return brentq(lambda p: log1m_P_vis(K, p) - log1m_P_agg(K, p),
                  0.5, 0.79999, xtol=1e-14)


def draw(ax):
    Ks = sorted(set(int(round(k)) for k in np.concatenate(
        [np.arange(5, 40), np.geomspace(40, 2000, 26)])))
    xs, ys = [], []
    for K in Ks:
        p = _p_of_K(K)
        if xs and p <= xs[-1]:          # absorb tiny even/odd reversals
            p = xs[-1] + 1e-6
        xs.append(p); ys.append(K)
    xs = [0.5] + xs                     # K* = 5 from p = 1/2 to the first root
    ys = [ys[0]] + ys
    ax.plot(xs, ys, color=C_VIS, lw=2.0)

    ax.text(0.512, 2300, "finite $K^{*}$", color=C_VIS, ha="left",
            va="top", fontsize=8)
    ax.text(0.988, 2300, "no finite $K^{*}$", color="0.35", ha="right",
            va="top", fontsize=8)
    ax.axvline(0.8, color=C_LINE, lw=0.9, ls=(0, (4, 3)))

    ax.set_yscale("log")
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(4, 3000)
    ax.set_xlabel(r"Adviser accuracy  $p$")
    ax.set_ylabel(r"Disclosure reference scale  $K^{*}(p)$")
    ax.grid(False)


if __name__ == "__main__":
    render(draw, "panel_kstar", (5.8, 4.8))
