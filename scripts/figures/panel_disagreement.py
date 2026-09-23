"""Fig. 4a: probability of any disagreement, 1 - p^K - q^K."""
from mta.theory import P_any
from mta.viz import P_VALUES, P_COLORS, KS, lineplot, mark_kstar, render


def draw(ax):
    for p in P_VALUES:
        lineplot(ax, KS, [P_any(K, p) for K in KS], lw=2.0,
                 color=P_COLORS[p], label=fr"$p={p}$")
    ax.axhline(1.0, color="0.8", lw=0.8, ls=":")
    mark_kstar(ax)
    for ks in (6, 14):
        ax.text(ks, 1.02, fr"$K^{{*}}={ks}$", color="black",
                ha="center", va="bottom", fontsize=9,
                transform=ax.get_xaxis_transform(), clip_on=False)
    ax.set_xlim(2, 30)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Number of advisers  $K$")
    ax.set_ylabel(r"Any disagreement  $1-p^{K}-q^{K}$")
    ax.legend(loc="lower right", frameon=True, framealpha=0.95,
              title="accuracy")


if __name__ == "__main__":
    render(draw, "panel_disagreement", (4.8, 4.4))
