"""Fig. 4: (a) any disagreement, (b) dissenting fraction, (c) all-wrong unanimity."""
from mta.viz import setup_theme, save
import matplotlib.pyplot as plt

from panel_disagreement import draw as draw_disagreement
from panel_fraction import draw as draw_fraction
from panel_unanimity import draw as draw_unanimity


def main():
    setup_theme()
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3))
    for ax, draw, lab in zip(axes, (draw_disagreement, draw_fraction, draw_unanimity), "abc"):
        draw(ax)
        ax.set_title(lab, loc="left", weight="bold")
    fig.tight_layout(w_pad=2.4)
    save(fig, "fig4_all")


if __name__ == "__main__":
    main()
