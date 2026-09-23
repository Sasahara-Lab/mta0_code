"""Fig. 4b: expected dissenting fraction E[m(K)] = E[min(Y, K-Y)]/K -> q."""
from mta.theory import M
from mta.viz import P_VALUES, P_COLORS, KS, lineplot, mark_kstar, render


def draw(ax):
    for p in P_VALUES:
        lineplot(ax, KS, [M(K, p) / K for K in KS], lw=2.0,
                 color=P_COLORS[p], label=fr"$p={p}$")
        ax.axhline(1 - p, ls="-.", lw=0.9, color="black", alpha=0.6)
    mark_kstar(ax)
    ax.set_xlim(2, 30)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel(r"Number of advisers  $K$")
    ax.set_ylabel(r"Expected dissenting fraction  $\mathbb{E}[m(K)]$")
    ax.annotate(r"dash-dot: $q=1{-}p$", xy=(0.96, 0.92), xycoords="axes fraction",
                color="0.4", ha="right")


if __name__ == "__main__":
    render(draw, "panel_fraction", (4.8, 4.4))
