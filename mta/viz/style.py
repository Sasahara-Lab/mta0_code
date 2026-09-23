"""Shared theme, colours and output helpers for the figure scripts.

Importing this module selects matplotlib's "Agg" backend.
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from mta import ROOT
from mta.theory.condorcet import K_star


def setup_theme():
    """Apply the shared seaborn theme; call once per script."""
    sns.set_theme(context="paper", style="ticks", palette="colorblind")
    plt.rcParams.update({"mathtext.fontset": "dejavusans"})


def lineplot(ax, x, y, **kwargs):
    return sns.lineplot(x=x, y=y, ax=ax, **kwargs)


# Colours (seaborn "colorblind" palette). Blue = aggregate side (P_agg, R_agg),
# red = visible-dissent side (P_vis, R_vis), grey = reference lines and markers.
CB = sns.color_palette("colorblind")
C_AGG = CB[0]
C_VIS = CB[3]
C_LINE = "0.2"

CMAP_VIS = sns.color_palette("rocket_r", as_cmap=True)

# Fig. 4: one blue per accuracy, light to dark.
P_VALUES = [0.6, 0.7, 0.8]
P_COLORS = dict(zip(P_VALUES, sns.color_palette("Blues", len(P_VALUES) + 1)[1:]))

# K axis shared by the line panels.
KS = np.arange(2, 31)


def mark_kstar(ax):
    """Vertical dotted lines at K*(p) for each p in P_VALUES with a finite K* <= 30."""
    for p in P_VALUES:
        ks = K_star(p)
        if ks is not None and ks <= 30:
            ax.axvline(ks, color=P_COLORS[p], lw=1.0, ls=(0, (2, 2)), alpha=0.75)


def save(fig, stem, dpi=300):
    """Save <stem>.png (and <stem>.pdf when MTA_PDF is set) into figures/ or MTA_OUTDIR."""
    d = os.environ.get("MTA_OUTDIR", os.path.join(ROOT, "figures"))
    os.makedirs(d, exist_ok=True)
    outs = [os.path.join(d, stem + ".png")]
    if os.environ.get("MTA_PDF"):
        outs.append(os.path.join(d, stem + ".pdf"))
    for path in outs:
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print("saved: " + "\n       ".join(outs))


def render(draw, stem, figsize):
    """Render one panel as a standalone figure and save it."""
    setup_theme()
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.tight_layout()
    save(fig, stem)
