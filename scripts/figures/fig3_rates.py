"""Fig. 3: (a) rate-crossover boundary p = 4/5; (b) disclosure reference scale K*(p)."""
from mta.viz import setup_theme, save
import matplotlib.pyplot as plt

from panel_boundary import draw as draw_boundary
from panel_kstar import draw as draw_kstar


def main():
    setup_theme()
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.3))
    for ax, draw, lab in zip(axes, (draw_boundary, draw_kstar), "ab"):
        draw(ax)
        ax.set_title(lab, loc="left", weight="bold")
    fig.tight_layout(w_pad=2.4)
    save(fig, "fig3_rates")


if __name__ == "__main__":
    main()
