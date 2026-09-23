"""Fig. 2: (a-c) P_agg and P_vis at p = 0.8, 0.7, 0.6; (d) P_vis heatmap."""
from mta.viz import setup_theme, save
import matplotlib.pyplot as plt

from panel_decoupling import draw as draw_decoupling
from panel_exposure import draw as draw_exposure


def main():
    setup_theme()
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 9.0))
    ax = axes.flat
    for a, p0 in zip(ax[:3], (0.8, 0.7, 0.6)):
        draw_decoupling(a, p0=p0)
    draw_exposure(ax[3])
    for a, lab in zip(ax, "abcd"):
        a.set_title(lab, loc="left", weight="bold")
    fig.tight_layout(w_pad=2.2, h_pad=2.6)
    save(fig, "fig2_abcd")


if __name__ == "__main__":
    main()
