"""Fig. 4c: probability of an all-wrong panel, q^K (log scale)."""
from mta.viz import P_VALUES, P_COLORS, KS, lineplot, mark_kstar, render


def draw(ax):
    for p in P_VALUES:
        q = 1.0 - p
        lineplot(ax, KS, [q**K for K in KS], lw=2.0,
                 color=P_COLORS[p], label=fr"$p={p}$")
    mark_kstar(ax)
    ax.set_yscale("log")
    ax.set_xlim(2, 30)
    ax.set_ylim(1e-14, 0.5)
    ax.set_xlabel(r"Number of advisers  $K$")
    ax.set_ylabel(r"All-wrong unanimity  $q^{K}$")


if __name__ == "__main__":
    render(draw, "panel_unanimity", (4.8, 4.4))
