#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams — Topic 4 (Introductory Organic Chemistry and Alkanes).

Outputs light + dark variants for each diagram into public/diagrams/.
Style follows the site token contract: neutral canvas, coral accent #F5654A,
hairline strokes, DejaVu labels, transparent background.

Figures:
  hazard-symbols       six GHS-style pictograms (flammable, toxic, corrosive, irritant,
                       oxidising, environmental hazard)
  formula-types        butane as molecular / structural / displayed / skeletal
  skeletal-heteroatom  butan-2-ol skeletal with the O-H drawn out
  alkane-isomers       chain isomers of C4H10 (2), C5H12 (3), C6H14 (5)
  cycloalkane-isomers  cyclopropane, cyclobutane, methylcyclopropane, cyclopentane,
                       methylcyclobutane
  fractionating-column temperature-gradient column with fractions
  pollutants-map       pollutant -> origin -> problem flow
  mechanism-radical-substitution  initiation / propagation / termination
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon

OUT = "/home/z/my-project/public/diagrams"
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"

ACCENT = "#F5654A"

LIGHT = {
    "ink": "#1d1d1b",
    "muted": "#5f6268",
    "faint": "#9a9da3",
    "hair": "#c9c7c2",
    "hair_soft": "#dedcd7",
    "fill": "#ffffff",
    "acc": ACCENT,
    "acc_tint": (245/255, 101/255, 74/255, 0.10),
    "acc_tint2": (245/255, 101/255, 74/255, 0.20),
    "grey_tint": (141/255, 144/255, 150/255, 0.16),
    "grey_edge": "#8d9096",
}
DARK = {
    "ink": "#f0efee",
    "muted": "#a3a6ad",
    "faint": "#71747a",
    "hair": "#4c4c50",
    "hair_soft": "#3a3a3e",
    "fill": "#161616",
    "acc": ACCENT,
    "acc_tint": (245/255, 101/255, 74/255, 0.16),
    "acc_tint2": (245/255, 101/255, 74/255, 0.30),
    "grey_tint": (163/255, 166/255, 173/255, 0.18),
    "grey_edge": "#7c7f85",
}


def new_fig(w, h):
    fig = plt.figure(figsize=(w, h), dpi=160)
    fig.patch.set_alpha(0)
    return fig


def save(fig, name, theme):
    suffix = "" if theme is LIGHT else "-dark"
    path = os.path.join(OUT, f"{name}{suffix}.png")
    fig.savefig(path, transparent=True)
    plt.close(fig)
    print("wrote", path)


def axis_frame(ax, xlim, ylim):
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def arrow(ax, xy0, xy1, C, color=None, lw=1.5, style="-|>", ls="-", mut=12):
    ax.add_patch(FancyArrowPatch(xy0, xy1, arrowstyle=style, mutation_scale=mut,
                                 lw=lw, color=color or C["muted"], linestyle=ls,
                                 shrinkA=0, shrinkB=0))


def panel_title(ax, x, y, text, C, fs=10.5, color=None, weight="medium", ha="center"):
    ax.text(x, y, text, fontsize=fs, color=color or C["ink"], ha=ha,
            va="center", fontweight=weight)


def sub_label(ax, x, y, text, C, fs=8.6, color=None, ha="center"):
    ax.text(x, y, text, fontsize=fs, color=color or C["muted"], ha=ha, va="center")


def box(ax, x, y, w, h, C, face=None, edge=None, lw=1.2, round_=0.10):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle=f"round,pad=0,rounding_size={round_}",
                                facecolor=face if face is not None else C["grey_tint"],
                                edgecolor=edge or C["grey_edge"], lw=lw))


# ---------------------------------------------------------------- skeletal helper
def zigzag(ax, pts, C, lw=1.6, color=None):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color or C["ink"], lw=lw, solid_capstyle="round",
            solid_joinstyle="round", zorder=4)


def chain_pts(x0, y0, n, step=0.62, ang=30):
    """n vertices of a zig-zag chain starting at (x0, y0)."""
    pts = [(x0, y0)]
    dx, dy = step * np.cos(np.radians(ang)), step * np.sin(np.radians(ang))
    x, y = x0, y0
    for k in range(n - 1):
        x += dx if k % 2 == 0 else dx
        y += dy if k % 2 == 0 else -dy
        pts.append((x, y))
    return pts


def bond_down(ax, x, y, C, ln=0.34, color=None):
    ax.plot([x, x], [y, y - ln], color=color or C["ink"], lw=1.6,
            solid_capstyle="round", zorder=4)


# ---------------------------------------------------------------- figure 1
def _flame(ax, x, y, s, C):
    """classic flame silhouette (filled) with an inner cut-out"""
    body = [(-0.17, -0.16), (-0.10, -0.30), (0.0, -0.34), (0.11, -0.28),
            (0.17, -0.16), (0.14, -0.02), (0.02, 0.16), (0.10, 0.32),
            (-0.02, 0.22), (-0.08, 0.30), (-0.10, 0.10), (-0.17, -0.04)]
    ax.add_patch(Polygon([(x + px * s, y + py * s) for px, py in body],
                         closed=True, facecolor=C["ink"], edgecolor="none"))
    ax.add_patch(Circle((x - 0.015 * s, y - 0.10 * s), 0.085 * s,
                        facecolor=C["fill"], edgecolor="none"))


def _pictogram_flame(ax, x, y, C, s=1.0):
    _flame(ax, x, y + 0.05, 1.0 * s, C)


def _pictogram_skull(ax, x, y, C, s=1.0):
    ax.add_patch(Circle((x, y + 0.10*s), 0.22*s, facecolor=C["ink"], edgecolor="none"))
    for dx in (-0.08, 0.08):
        ax.add_patch(Circle((x + dx*s, y + 0.13*s), 0.05*s, facecolor=C["fill"], edgecolor="none"))
    ax.plot([x - 0.26*s, x + 0.26*s], [y - 0.20*s, y - 0.02*s], color=C["ink"], lw=2.4*s)
    ax.plot([x - 0.26*s, x + 0.26*s], [y - 0.02*s, y - 0.20*s], color=C["ink"], lw=2.4*s)


def _pictogram_corrosive(ax, x, y, C, s=1.0):
    # two tilted tubes dripping onto a surface
    ax.plot([x - 0.30*s, x - 0.10*s], [y + 0.32*s, y - 0.04*s], color=C["ink"], lw=2.2*s)
    ax.plot([x + 0.30*s, x + 0.10*s], [y + 0.32*s, y - 0.12*s], color=C["ink"], lw=2.2*s)
    ax.plot([x - 0.36*s, x + 0.36*s], [y - 0.20*s, y - 0.20*s], color=C["ink"], lw=2.0*s)
    for dx, dy in ((-0.14, -0.10), (0.16, -0.15)):
        ax.plot(x + dx*s, y + dy*s, 'o', ms=2.4*s, color=C["ink"])
    ax.plot([x - 0.24*s, x - 0.24*s], [y - 0.26*s, y - 0.34*s], color=C["ink"], lw=1.8*s)
    ax.plot([x + 0.24*s, x + 0.24*s], [y - 0.26*s, y - 0.34*s], color=C["ink"], lw=1.8*s)


def _pictogram_exclamation(ax, x, y, C, s=1.0):
    ax.plot([x, x], [y + 0.30*s, y - 0.06*s], color=C["ink"], lw=3.4*s, solid_capstyle="round")
    ax.plot(x, y - 0.24*s, 'o', ms=3.4*s, color=C["ink"])


def _pictogram_oxidising(ax, x, y, C, s=1.0):
    ax.add_patch(Circle((x, y - 0.14*s), 0.15*s, fill=False, edgecolor=C["ink"], lw=2.2*s))
    _flame(ax, x, y + 0.20, 0.62 * s, C)


def _pictogram_environment(ax, x, y, C, s=1.0):
    # dead tree
    ax.plot([x - 0.22*s, x - 0.22*s], [y - 0.22*s, y + 0.16*s], color=C["ink"], lw=2.0*s)
    ax.plot([x - 0.22*s, x - 0.34*s], [y + 0.08*s, y + 0.18*s], color=C["ink"], lw=1.6*s)
    ax.plot([x - 0.22*s, x - 0.10*s], [y + 0.14*s, y + 0.24*s], color=C["ink"], lw=1.6*s)
    # dead fish
    ax.add_patch(Ellipse((x + 0.16*s, y - 0.10*s), 0.34*s, 0.16*s, angle=-14,
                         fill=False, edgecolor=C["ink"], lw=1.6*s))
    ax.plot([x + 0.32*s, x + 0.42*s, x + 0.32*s], [y - 0.02*s, y - 0.12*s, y - 0.20*s],
            color=C["ink"], lw=1.4*s)


def fig_hazard_symbols(C):
    fig = new_fig(7.8, 3.0)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 12), (0, 4.6))
    glyphs = [(_pictogram_flame, "Flammable"), (_pictogram_skull, "Toxic"),
              (_pictogram_corrosive, "Corrosive"), (_pictogram_exclamation, "Irritant"),
              (_pictogram_oxidising, "Oxidising"), (_pictogram_environment, "Environmental")]
    red = "#c0392b" if C is LIGHT else "#e06050"
    for k, (fn, lab) in enumerate(glyphs):
        x = 1.1 + k * 1.96
        # rotated square (diamond)
        d = 0.82
        ax.add_patch(Polygon([(x, 2.6 + d), (x + d, 2.6), (x, 2.6 - d), (x - d, 2.6)],
                             closed=True, facecolor=C["fill"], edgecolor=red, lw=2.2))
        fn(ax, x, 2.66, C, s=1.05)
        sub_label(ax, x, 1.15, lab, C, fs=8.8)
    sub_label(ax, 6.0, 0.35, "the six standard hazard pictograms", C, fs=9.0, color=C["faint"])
    save(fig, "hazard-symbols", C)


# ---------------------------------------------------------------- figure 2
def fig_formula_types(C):
    fig = new_fig(8.0, 4.4)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 12), (0, 6.6))
    cols = [2.0, 5.0, 8.0, 10.9]
    heads = ["Molecular", "Structural", "Displayed", "Skeletal"]
    for x, h in zip(cols, heads):
        panel_title(ax, x, 6.05, h, C, fs=10.5)
    # molecular
    ax.text(2.0, 3.6, "C\u2084H\u2081\u2080", ha="center", va="center", fontsize=17,
            color=C["ink"], fontweight="medium")
    sub_label(ax, 2.0, 2.55, "actual atom count", C, fs=7.8)
    # structural
    ax.text(5.0, 3.6, "CH\u2083\u2014CH\u2082\u2014CH\u2082\u2014CH\u2083", ha="center",
            va="center", fontsize=11.5, color=C["ink"])
    sub_label(ax, 5.0, 2.55, "carbon by carbon", C, fs=7.8)
    # displayed
    yd = 3.6
    xs = [7.0, 7.9, 8.8, 9.7]  # wait — displayed panel centre 8.0
    xs = [6.55, 7.4, 8.25, 9.1]
    for i, x in enumerate(xs):
        ax.text(x, yd, "C", ha="center", va="center", fontsize=11, color=C["ink"])
        if i < 3:
            ax.plot([x + 0.13, xs[i+1] - 0.13], [yd, yd], color=C["ink"], lw=1.5)
        # H stubs
        if i in (0, 2):
            ax.plot([x, x], [yd + 0.13, yd + 0.42], color=C["ink"], lw=1.5)
            ax.text(x, yd + 0.58, "H", ha="center", va="center", fontsize=9, color=C["ink"])
        if i in (1, 3) or True:
            ax.plot([x, x], [yd - 0.13, yd - 0.42], color=C["ink"], lw=1.5)
            ax.text(x, yd - 0.58, "H", ha="center", va="center", fontsize=9, color=C["ink"])
        if i in (1, 2):
            ax.plot([x, x], [yd + 0.13, yd + 0.42], color=C["ink"], lw=1.5)
            ax.text(x, yd + 0.58, "H", ha="center", va="center", fontsize=9, color=C["ink"])
    sub_label(ax, 8.0, 2.55, "every bond drawn", C, fs=7.8)
    # skeletal
    pts = chain_pts(10.15, 3.25, 4, step=0.62, ang=32)
    zigzag(ax, pts, C, lw=1.8)
    sub_label(ax, 11.0, 2.55, "zig-zag: vertices = C", C, fs=7.8)
    # captions
    ax.text(6.0, 5.1, "butane, drawn four ways", ha="center", fontsize=9.0,
            color=C["acc"], fontweight="medium")
    sub_label(ax, 6.0, 1.35, "molecular and structural formulae can be written as text;",
              C, fs=8.2, color=C["faint"])
    sub_label(ax, 6.0, 0.95, "displayed and skeletal are drawings with different rules",
              C, fs=8.2, color=C["faint"])
    save(fig, "formula-types", C)


# ---------------------------------------------------------------- figure 3
def fig_skeletal_heteroatom(C):
    fig = new_fig(6.8, 3.2)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 5.0))
    panel_title(ax, 5.0, 4.55, "Butan-2-ol, CH\u2083CH(OH)CH\u2082CH\u2083", C, fs=10.5)
    # backbone: C1-C2-C3-C4
    pts = chain_pts(2.2, 2.55, 4, step=1.05, ang=30)
    zigzag(ax, pts, C, lw=1.9)
    # OH on C2 (second vertex), drawn up-right
    x2, y2 = pts[1]
    ax.plot([x2, x2 + 0.72], [y2, y2 + 0.62], color=C["ink"], lw=1.9, zorder=4)
    ax.text(x2 + 0.92, y2 + 0.74, "OH", ha="center", va="center", fontsize=11.5,
            color=C["acc"], fontweight="bold")
    # annotations
    sub_label(ax, pts[0][0], pts[0][1] - 0.42, "C (invisible)", C, fs=7.8, color=C["faint"])
    sub_label(ax, x2 + 1.35, y2 + 1.28, "heteroatom + its H \u2014 always drawn", C, fs=8.2,
              color=C["acc"])
    sub_label(ax, 5.0, 0.55, "carbon-bonded hydrogens are omitted; vertices and ends are carbon atoms",
              C, fs=8.4, color=C["faint"])
    save(fig, "skeletal-heteroatom", C)


# ---------------------------------------------------------------- figure 4
def fig_alkane_isomers(C):
    fig = new_fig(7.8, 6.0)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 12), (0, 11.6))
    B = C["ink"]

    def draw(name, pts, branches, label_y=None):
        """branches: list of (vertex_index, 'up'/'down', offset)"""
        zigzag(ax, pts, C, lw=1.7)
        for bi, side, off in branches:
            x0, y0 = pts[bi]
            if side == 'up':
                ax.plot([x0 + off, x0 + off], [y0 + 0.05, y0 + 0.62], color=B, lw=1.7, zorder=4)
            else:
                ax.plot([x0 + off, x0 + off], [y0 - 0.05, y0 - 0.62], color=B, lw=1.7, zorder=4)
        sub_label(ax, (pts[0][0] + pts[-1][0]) / 2 + 0.2,
                  label_y if label_y is not None else pts[-1][1] - 0.95, name, C, fs=8.0)

    # --- C4 row
    panel_title(ax, 0.55, 9.75, "C\u2084H\u2081\u2080 \u2014 2 isomers", C, fs=9.8, color=C["acc"], ha="left")
    draw("butane", chain_pts(1.0, 8.1, 4), [])
    draw("2-methylpropane", chain_pts(4.6, 8.1, 3), [(1, 'up', 0.0)])

    # --- C5 row
    panel_title(ax, 0.55, 6.95, "C\u2085H\u2081\u2082 \u2014 3 isomers", C, fs=9.8, color=C["acc"], ha="left")
    draw("pentane", chain_pts(0.7, 5.3, 5), [], label_y=4.62)
    draw("2-methylbutane", chain_pts(4.3, 5.3, 4), [(1, 'up', 0.0)])
    # 2,2-dimethylpropane: central quaternary C as a plus
    cx, cy = 9.4, 5.3
    ax.plot([cx - 0.62, cx - 0.18], [cy, cy], color=B, lw=1.7, zorder=4)
    ax.plot([cx + 0.18, cx + 0.62], [cy, cy], color=B, lw=1.7, zorder=4)
    ax.plot([cx, cx], [cy - 0.62, cy - 0.18], color=B, lw=1.7, zorder=4)
    ax.plot([cx, cx], [cy + 0.18, cy + 0.62], color=B, lw=1.7, zorder=4)
    sub_label(ax, cx, cy - 0.95, "2,2-dimethylpropane", C, fs=8.0)

    # --- C6 row a
    panel_title(ax, 0.55, 4.15, "C\u2086H\u2081\u2084 \u2014 5 isomers", C, fs=9.8, color=C["acc"], ha="left")
    draw("hexane", chain_pts(0.7, 2.55, 6), [])
    draw("2-methylpentane", chain_pts(4.6, 2.55, 5), [(1, 'up', 0.0)])
    draw("3-methylpentane", chain_pts(8.5, 2.55, 5), [(2, 'down', 0.0)])
    # --- C6 row b
    draw("2,2-dimethylbutane", chain_pts(2.2, 0.6, 4), [(1, 'up', -0.10), (1, 'up', 0.16)], label_y=-0.15)
    draw("2,3-dimethylbutane", chain_pts(7.2, 0.6, 4), [(1, 'up', 0.0), (2, 'down', 0.0)], label_y=-0.15)
    save(fig, "alkane-isomers", C)


# ---------------------------------------------------------------- figure 5
def _ring(ax, x, y, n, r, C, lw=1.7, color=None):
    th = np.linspace(0, 2*np.pi, 200) + np.pi / 2
    ax.plot(x + r*np.cos(th), y + r*np.sin(th), color=color or C["ink"], lw=lw,
            zorder=4, solid_capstyle="round")


def fig_cycloalkane_isomers(C):
    fig = new_fig(7.8, 3.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 12), (0, 5.6))
    items = [
        ("cyclopropane", 1.5, 3.0, 3, 0.62, None),
        ("cyclobutane", 3.9, 3.0, 4, 0.70, None),
        ("methylcyclopropane", 6.3, 3.0, 3, 0.62, 1),
        ("cyclopentane", 8.9, 3.0, 5, 0.80, None),
        ("methylcyclobutane", 11.2, 3.0, 4, 0.70, 1),
    ]
    for name, x, y, n, r, branch in items:
        _ring(ax, x, y, n, r, C)
        if branch is not None:
            ax.plot([x, x], [y + r, y + r + 0.5], color=C["ink"], lw=1.7, zorder=4)
        sub_label(ax, x, y - r - 0.55, name, C, fs=8.2)
    sub_label(ax, 6.0, 0.55, "ring isomers \u2014 same molecular formula, different ring size or substituents",
              C, fs=8.4, color=C["faint"])
    panel_title(ax, 6.0, 5.05, "Cycloalkane isomers (examples)", C, fs=10.5)
    save(fig, "cycloalkane-isomers", C)


# ---------------------------------------------------------------- figure 6
def fig_fractionating_column(C):
    fig = new_fig(7.2, 4.8)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 7.4))
    # column (wider at bottom)
    top_w, bot_w = 1.7, 2.6
    y0, y1 = 0.7, 6.7
    ax.add_patch(Polygon([(5 - top_w/2, y1), (5 + top_w/2, y1),
                          (5 + bot_w/2, y0), (5 - bot_w/2, y0)],
                         closed=True, facecolor=C["grey_tint"], edgecolor=C["grey_edge"], lw=1.4))
    # trays
    for ty in np.linspace(y0 + 0.55, y1 - 0.45, 8):
        w = np.interp(ty, [y0, y1], [bot_w, top_w]) - 0.22
        ax.plot([5 - w/2, 5 + w/2], [ty, ty], color=C["hair"], lw=1.0)
    # feed + heat
    arrow(ax, (1.6, 1.6), (5 - np.interp(1.6, [y0, y1], [bot_w, top_w])/2 - 0.05, 1.6), C, lw=1.6)
    ax.text(1.45, 1.6, "crude oil\n(vaporised)", ha="right", va="center", fontsize=8.4, color=C["ink"])
    # temperature gradient
    ax.plot([8.45, 8.45], [y0 + 0.25, y1 - 0.25], color=C["acc"], lw=3.0,
            solid_capstyle="round", alpha=0.35)
    arrow(ax, (8.45, 3.4), (8.45, 5.9), C, color=C["acc"], lw=1.6)
    ax.text(8.45, 2.6, "cooler\nat the top", ha="center", va="top", fontsize=7.8, color=C["muted"])
    ax.text(8.45, 0.55, "hotter\nat the bottom", ha="center", va="top", fontsize=7.8, color=C["muted"])
    # fractions
    fr = [("refinery gas", 6.15), ("petrol / gasoline", 5.35), ("naphtha", 4.62),
          ("kerosene", 3.85), ("diesel oil", 3.05), ("fuel oil", 2.15), ("residue", 1.15)]
    for i, (name, fy) in enumerate(fr):
        side = 1 if i % 2 == 0 else 0
        if side:
            ax.plot([5 + np.interp(fy, [y0, y1], [bot_w, top_w])/2,
                     7.15], [fy, fy], color=C["hair"], lw=1.1)
            ax.text(7.28, fy, name, ha="left", va="center", fontsize=8.4, color=C["ink"])
        else:
            ax.plot([5 - np.interp(fy, [y0, y1], [bot_w, top_w])/2,
                     2.85], [fy, fy], color=C["hair"], lw=1.1)
            ax.text(2.72, fy, name, ha="right", va="center", fontsize=8.4, color=C["ink"])
    ax.text(5.0, 7.05, "short chains condense high \u00b7 long chains condense low",
            ha="center", fontsize=9.2, color=C["acc"], fontweight="medium")
    save(fig, "fractionating-column", C)


# ---------------------------------------------------------------- figure 7
def fig_pollutants_map(C):
    fig = new_fig(7.8, 4.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 12), (0, 8.6))
    panel_title(ax, 1.7, 8.05, "Origin", C, fs=10)
    panel_title(ax, 6.0, 8.05, "Pollutant", C, fs=10)
    panel_title(ax, 10.3, 8.05, "Problem", C, fs=10)
    rows = [
        ("plenty of O\u2082", "CO\u2082", "climate change"),
        ("limited O\u2082", "CO", "binds haemoglobin \u2014 toxic"),
        ("severe O\u2082 shortage", "C particulates", "asthma \u00b7 global dimming"),
        ("fuel escapes burning", "unburned HC", "ground-level ozone, smog"),
        ("N\u2082 + O\u2082 in hot engines", "NO\u2093", "nitric acid \u2014 acid rain"),
        ("sulfur impurities burn", "SO\u2082", "sulfuric acid \u2014 acid rain"),
    ]
    ys = np.linspace(6.9, 1.1, 6)
    for y, (o, p, pr) in zip(ys, rows):
        box(ax, 1.7, y, 2.9, 0.92, C)
        ax.text(1.7, y, o, ha="center", va="center", fontsize=7.8, color=C["ink"])
        box(ax, 6.0, y, 2.2, 0.92, C, face=C["acc_tint"], edge=C["acc"])
        ax.text(6.0, y, p, ha="center", va="center", fontsize=8.6, color=C["acc"],
                fontweight="medium")
        box(ax, 10.3, y, 3.3, 0.92, C)
        ax.text(10.3, y, pr, ha="center", va="center", fontsize=7.6, color=C["ink"])
        arrow(ax, (3.2, y), (4.85, y), C, lw=1.3)
        arrow(ax, (7.15, y), (8.6, y), C, lw=1.3)
    save(fig, "pollutants-map", C)


# ---------------------------------------------------------------- figure 8
def fig_mechanism_radical_substitution(C):
    fig = new_fig(7.6, 5.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 9.4))

    # INITIATION
    box(ax, 5.0, 7.9, 9.0, 2.35, C, face=C["acc_tint"] if False else C["fill"], edge=C["hair"])
    panel_title(ax, 0.65, 9.0, "1  INITIATION", C, fs=9.6, color=C["acc"], ha="left")
    ax.text(3.6, 8.15, "Cl\u2014Cl", ha="center", va="center", fontsize=11, color=C["ink"])
    # UV wavy arrow
    th = np.linspace(0, 3.2*np.pi, 120)
    ax.plot(0.55 + np.linspace(0, 2.5, 120),
            8.38 + 0.085*np.sin(th), color=C["acc"], lw=1.3)
    arrow(ax, (2.95, 8.38), (3.28, 8.32), C, color=C["acc"], lw=1.3, mut=9)
    ax.text(1.8, 8.66, "UV light", ha="center", fontsize=8.0, color=C["acc"])
    # fish-hook half arrows from bond to each Cl
    for dx, sgn in ((-0.18, -1), (0.18, 1)):
        ax.add_patch(FancyArrowPatch((3.6 + dx, 8.42), (3.6 + dx + sgn*0.55, 8.78),
                                     arrowstyle="-|>", mutation_scale=8, lw=1.2,
                                     color=C["acc"], connectionstyle="arc3,rad=0.35",
                                     shrinkA=0, shrinkB=0))
    ax.text(6.4, 8.15, "Cl\u2022  +  Cl\u2022", ha="center", va="center", fontsize=11,
            color=C["ink"])
    ax.text(8.55, 8.15, "homolytic fission:\none electron each", ha="center", va="center",
            fontsize=7.4, color=C["muted"])
    ax.text(5.0, 7.05, "half-headed (fish-hook) arrows \u2014 a single electron moves",
            ha="center", fontsize=7.8, color=C["faint"])

    # PROPAGATION
    box(ax, 5.0, 4.6, 9.0, 2.9, C, face=C["fill"], edge=C["hair"])
    panel_title(ax, 0.65, 5.95, "2  PROPAGATION", C, fs=9.6, color=C["acc"], ha="left")
    ax.text(4.3, 5.45, "Cl\u2022 + CH\u2084 \u2192 \u2022CH\u2083 + HCl", ha="center",
            va="center", fontsize=9.6, color=C["ink"])
    ax.text(4.3, 4.35, "\u2022CH\u2083 + Cl\u2082 \u2192 CH\u2083Cl + Cl\u2022", ha="center",
            va="center", fontsize=9.6, color=C["ink"])
    # chain loop
    ax.add_patch(FancyArrowPatch((7.3, 5.45), (7.3, 4.35), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.3, color=C["acc"],
                                 connectionstyle="arc3,rad=-0.55", shrinkA=0, shrinkB=0))
    ax.text(8.45, 4.9, "radical used\nand regenerated\n\u2014 the chain continues",
            ha="center", va="center", fontsize=7.4, color=C["acc"])

    # TERMINATION
    box(ax, 5.0, 1.6, 9.0, 2.5, C, face=C["fill"], edge=C["hair"])
    panel_title(ax, 0.65, 2.72, "3  TERMINATION", C, fs=9.6, color=C["acc"], ha="left")
    ax.text(4.6, 2.35, "Cl\u2022 + Cl\u2022 \u2192 Cl\u2082", ha="center", va="center",
            fontsize=9.2, color=C["ink"])
    ax.text(4.6, 1.7, "\u2022CH\u2083 + Cl\u2022 \u2192 CH\u2083Cl", ha="center", va="center",
            fontsize=9.2, color=C["ink"])
    ax.text(7.6, 2.0, "\u2022CH\u2083 + \u2022CH\u2083 \u2192 C\u2082H\u2086", ha="center",
            va="center", fontsize=9.2, color=C["ink"])
    ax.text(7.6, 1.25, "ethane = evidence for \u2022CH\u2083", ha="center", fontsize=7.6,
            color=C["acc"])
    ax.text(5.0, 0.45, "two radicals combine \u2014 the chain ends", ha="center",
            fontsize=7.8, color=C["faint"])
    save(fig, "mechanism-radical-substitution", C)


ALL = {
    "hazard-symbols": fig_hazard_symbols,
    "formula-types": fig_formula_types,
    "skeletal-heteroatom": fig_skeletal_heteroatom,
    "alkane-isomers": fig_alkane_isomers,
    "cycloalkane-isomers": fig_cycloalkane_isomers,
    "fractionating-column": fig_fractionating_column,
    "pollutants-map": fig_pollutants_map,
    "mechanism-radical-substitution": fig_mechanism_radical_substitution,
}

if __name__ == "__main__":
    for name, fn in ALL.items():
        for theme in (LIGHT, DARK):
            fn(theme)
    print("done: topic 4 diagrams")

