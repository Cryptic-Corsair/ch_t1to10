#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams — Topic 3 Part I (Ionic + Metallic bonding).

Outputs light + dark variants for each diagram into public/diagrams/.
Style follows the site token contract: neutral canvas, coral accent #F5654A,
hairline strokes, DejaVu labels, transparent background.

Figures:
  evidence-ions      U-tube migration of CuCrO4 ions (blue Cu2+ -> cathode, yellow CrO4^2- -> anode)
  dot-cross-ions     electron transfer diagrams for NaCl and MgO (before -> after, brackets + charges)
  ionic-lattice      giant ionic lattice slice with 6:6 coordination highlighted
  mp-comparison      melting points NaCl / NaF / MgO as bond-strength evidence
  isoelectronic-radii  N3- -> Al3+ radii with proton counts (all 10 electrons)
  ion-polarisation   ideal vs polarised anion next to a small cation
  polarising-power   cation polarising power / anion polarisability ladders
  metallic-lattice   cation layers + sea of delocalised electrons
  metallic-slide     layers slide, the non-directional sea adjusts
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Arc

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


def panel_title(ax, x, y, text, C, fs=10.5, color=None, weight="medium"):
    ax.text(x, y, text, fontsize=fs, color=color or C["ink"], ha="center",
            va="center", fontweight=weight)


def sub_label(ax, x, y, text, C, fs=8.6, color=None, ha="center"):
    ax.text(x, y, text, fontsize=fs, color=color or C["muted"], ha=ha, va="center")


# ---------------------------------------------------------------- figure 1
def fig_evidence_ions(C):
    fig = new_fig(7.6, 3.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 4.6))

    bx0, bx1, by = 3.4, 6.6, 4.25
    ax.plot([bx0, bx0 + 0.32], [by, by], color=C["ink"], lw=2.6)
    ax.plot([bx0 + 0.48, bx1 - 0.48], [by, by], color=C["ink"], lw=1.2)
    ax.plot([bx1 - 0.32, bx1], [by, by], color=C["ink"], lw=2.6)
    ax.text(bx0 - 0.22, by, "+", ha="center", va="center", fontsize=11, color=C["ink"])
    ax.text(bx1 + 0.24, by, "\u2212", ha="center", va="center", fontsize=11, color=C["ink"])
    sub_label(ax, 5.0, 3.98, "d.c. supply", C, fs=8.4)

    blue = "#3b6fd4"
    yellow = "#d9a514"
    green = "#4d8f4a"
    if C is DARK:
        blue = "#7fa8ee"; yellow = "#e8c04a"; green = "#6fb56c"

    ax.add_patch(FancyBboxPatch((1.6, 0.55), 6.8, 3.15,
                                boxstyle="round,pad=0,rounding_size=0.3",
                                fill=True, facecolor=C["grey_tint"],
                                edgecolor=C["hair"], lw=1.2))
    ax.text(5.0, 3.15, "green CuCrO\u2084(aq)", ha="center", fontsize=9.5, color=green,
            fontweight="medium")

    for ex, lab, sign in ((2.35, "cathode", "\u2212"), (7.65, "anode", "+")):
        ax.plot([ex, ex], [1.0, 3.3], color=C["ink"], lw=3.2, solid_capstyle="round")
        ax.plot([ex, ex], [3.3, 4.25], color=C["ink"], lw=1.2)
        sub_label(ax, ex, 0.72, lab, C, fs=9.0)
        ax.text(ex, 0.36, sign, ha="center", va="center", fontsize=13, color=C["ink"],
                fontweight="bold")
    ax.text(2.62, 3.62, "negative\nelectrode", ha="left", va="center", fontsize=7.6,
            color=C["muted"])
    ax.text(7.38, 3.62, "positive\nelectrode", ha="right", va="center", fontsize=7.6,
            color=C["muted"])

    ax.add_patch(FancyBboxPatch((1.95, 1.35), 1.35, 1.5,
                                boxstyle="round,pad=0,rounding_size=0.25",
                                fill=True, facecolor=blue, edgecolor="none", alpha=0.75))
    ax.add_patch(FancyBboxPatch((6.7, 1.35), 1.35, 1.5,
                                boxstyle="round,pad=0,rounding_size=0.25",
                                fill=True, facecolor=yellow, edgecolor="none", alpha=0.75))
    arrow(ax, (3.45, 2.1), (2.75, 2.1), C, color=blue, lw=2.0, mut=14)
    arrow(ax, (6.55, 2.1), (7.25, 2.1), C, color=yellow, lw=2.0, mut=14)

    ax.text(4.05, 2.62, "blue Cu\u00b2\u207a", ha="center", fontsize=9.5, color=blue,
            fontweight="medium")
    ax.text(5.95, 2.62, "yellow CrO\u2084\u00b2\u207b", ha="center", fontsize=9.5,
            color=yellow, fontweight="medium")
    ax.text(4.05, 1.12, "cations \u2192 cathode", ha="center", fontsize=8.2, color=C["muted"])
    ax.text(5.95, 1.12, "anions \u2192 anode", ha="center", fontsize=8.2, color=C["muted"])

    save(fig, "evidence-ions", C)


def _atom(ax, x, y, shells, nucleus, C, syms_last=None, r0=0.55, dr=0.42):
    """Shell-model atom/ion: nucleus label + concentric shells of electron marks.

    shells: electron count per shell; syms_last: list of 'dot'/'cross' applied to the
    outer shell (crosses mark transferred electrons)."""
    for i, n in enumerate(shells):
        r = r0 + i * dr
        ax.add_patch(Circle((x, y), r, fill=False, lw=0.9, edgecolor=C["hair"]))
        for k in range(n):
            ang = np.pi/2 + k * (2*np.pi / n)
            ex, ey = x + r*np.cos(ang), y + r*np.sin(ang)
            if syms_last and i == len(shells) - 1 and syms_last[k % len(syms_last)] == 'cross':
                s = 0.07
                ax.plot([ex-s, ex+s], [ey-s, ey+s], color=C["acc"], lw=1.3,
                        solid_capstyle="round", zorder=6)
                ax.plot([ex-s, ex+s], [ey+s, ey-s], color=C["acc"], lw=1.3,
                        solid_capstyle="round", zorder=6)
            else:
                ax.plot(ex, ey, 'o', ms=2.3, color=C["ink"], zorder=6)
    ax.text(x, y, nucleus, ha="center", va="center", fontsize=10, color=C["ink"],
            fontweight="medium")


def _bracket_pair(ax, x0, x1, y0, y1, C):
    w = 0.16
    for bx, sign in ((x0, 1), (x1, -1)):
        ax.plot([bx + sign*w, bx, bx], [y1, y1, y0], color=C["ink"], lw=1.3)
        ax.plot([bx, bx + sign*w], [y0, y0], color=C["ink"], lw=1.3)


def fig_dot_cross_ions(C):
    fig = plt.figure(figsize=(8.2, 5.0), dpi=160)
    fig.patch.set_alpha(0)
    axL = fig.add_subplot(121)
    axR = fig.add_subplot(122)
    for ax, title, metal, nonmet, ne_m, ne_nm, n_tr in (
        (axL, "Sodium chloride, NaCl", "Na", "Cl", [2, 8, 1], [2, 8, 7], 1),
        (axR, "Magnesium oxide, MgO", "Mg", "O", [2, 8, 2], [2, 8, 6], 2),
    ):
        axis_frame(ax, (0, 10), (-0.2, 10))
        panel_title(ax, 5.0, 9.5, title, C, fs=10.5)

        # BEFORE — atoms with outer electrons
        yB = 6.6
        _atom(ax, 2.3, yB, ne_m, metal, C, syms_last=['cross'] * n_tr)
        _atom(ax, 7.7, yB, ne_nm, nonmet, C)
        arrow(ax, (3.85, yB), (6.15, yB), C, color=C["acc"], lw=1.5)
        ax.text(5.0, yB + 0.62, f"{n_tr} e\u207b transferred" if n_tr == 1
                else f"{n_tr} e\u207b transferred", ha="center", fontsize=8.2, color=C["acc"])
        sub_label(ax, 5.0, 4.45, "atoms before transfer", C, fs=8.4, color=C["faint"])

        # AFTER — ions in square brackets
        yA = 2.3
        _atom(ax, 2.9, yA, [8], metal, C, r0=0.72)
        _bracket_pair(ax, 1.55, 4.25, yA - 1.15, yA + 1.15, C)
        ax.text(4.55, yA + 0.78, "+", ha="center", va="center", fontsize=12,
                color=C["ink"], fontweight="bold")
        _atom(ax, 7.3, yA, [2, 8], nonmet, C, r0=0.42, dr=0.46,
              syms_last=['dot'] * (ne_nm[2] - n_tr) + ['cross'] * n_tr)
        _bracket_pair(ax, 5.75, 8.85, yA - 1.35, yA + 1.35, C)
        ax.text(9.15, yA + 0.95, "\u2212" if n_tr == 1 else "2\u2212", ha="center",
                va="center", fontsize=12, color=C["ink"], fontweight="bold")
        sub_label(ax, 5.0, 0.15, "ions after transfer \u2014 crosses = transferred electrons",
                  C, fs=8.4, color=C["faint"])
    fig.subplots_adjust(wspace=0.06)
    save(fig, "dot-cross-ions", C)


# ---------------------------------------------------------------- figure 3
def fig_ionic_lattice(C):
    fig = new_fig(7.2, 4.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (-0.65, 6.2))

    def ion(x, y, cation, highlight=False, dashed=False):
        r = 0.45
        edge = C["acc"] if highlight else C["grey_edge"]
        face = C["acc_tint2"] if highlight else (C["grey_tint"] if cation else C["fill"])
        ax.add_patch(Circle((x, y), r, facecolor=face, edgecolor=edge, lw=1.3,
                            ls=(0, (3, 2)) if dashed else "-", zorder=3))
        lab = "Na\u207a" if cation else "Cl\u207b"
        col = C["acc"] if highlight else C["ink"]
        ax.text(x, y, lab, ha="center", va="center", fontsize=8.4, color=col,
                fontweight="medium", zorder=4)

    # 3x3 mid-plane grid; alternating ions, central Na+ highlighted
    cx, cy = 4.6, 3.15
    for j, gy in enumerate((1.9, 3.15, 4.4)):
        for i, gx in enumerate((2.6, 4.6, 6.6)):
            if gx == cx and gy == cy:
                continue
            ion(gx, gy, (i + j) % 2 == 0)
    ion(cx, cy, True)

    # above + below Cl- (the two out-of-plane neighbours)
    ion(cx, 5.55, False, dashed=True)
    ion(cx, 0.75, False, dashed=True)
    for yy in (5.55, 0.75):
        ax.plot([cx, cx], [3.6 if yy > cy else 2.7, yy - 0.45 if yy > cy else yy + 0.45],
                color=C["acc"], lw=1.0, ls=(0, (3, 3)), zorder=1)

    # dashed coordination ring
    ax.add_patch(Circle((cx, cy), 1.02, fill=False, lw=1.1, edgecolor=C["acc"],
                        ls=(0, (4, 3)), zorder=2))

    # legend (well separated)
    ion(8.35, 5.0, True)
    sub_label(ax, 9.05, 5.0, "Na\u207a", C, fs=9.0, ha="left")
    ion(8.35, 3.9, False)
    sub_label(ax, 9.05, 3.9, "Cl\u207b", C, fs=9.0, ha="left")

    sub_label(ax, 5.0, 0.02, "alternating Na\u207a and Cl\u207b in all three dimensions", C, fs=9.2)
    ax.text(5.0, -0.45, "the highlighted Na\u207a touches 6 Cl\u207b \u2014 6:6 coordination",
            ha="center", fontsize=9.6, color=C["acc"], fontweight="medium")

    save(fig, "ionic-lattice", C)


# ---------------------------------------------------------------- figure 4
def fig_mp_comparison(C):
    fig = new_fig(6.4, 3.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 6.4), (0, 3.6))
    names = ["NaCl", "NaF", "MgO"]
    vals = [801, 993, 2852]
    notes = ["same charge,\nCl\u207b larger", "same charge,\nF\u207b smaller",
             "doubly charged,\nsmaller ions"]
    xs = [1.15, 2.85, 4.55]
    top = 2.95
    for x, v, n, name in zip(xs, vals, notes, names):
        h = v / 2852 * top
        acc = name == "MgO"
        ax.add_patch(FancyBboxPatch((x - 0.5, 0.45), 1.0, h,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=C["acc_tint2"] if acc else C["grey_tint"],
                                    edgecolor=C["acc"] if acc else C["grey_edge"],
                                    lw=1.3))
        ax.text(x, 0.45 + h + 0.16, f"{v} \u00b0C", ha="center", fontsize=10,
                color=C["acc"] if acc else C["ink"], fontweight="bold")
        ax.text(x, 0.22, name, ha="center", fontsize=11, color=C["ink"], fontweight="medium")
        ax.text(x + 0.78, 0.45 + h * 0.55, n, ha="left", fontsize=7.6, color=C["muted"])
    sub_label(ax, 0.35, 2.2, "melting point\nrises as bonding\nstrengthens", C, fs=8.0, ha="left")
    save(fig, "mp-comparison", C)


# ---------------------------------------------------------------- figure 5
def fig_isoelectronic_radii(C):
    fig = new_fig(7.2, 3.7)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 3.7))
    ions = [("N\u00b3\u207b", 7, 171), ("O\u00b2\u207b", 8, 140), ("F\u207b", 9, 133),
            ("Na\u207a", 11, 102), ("Mg\u00b2\u207a", 12, 72), ("Al\u00b3\u207a", 13, 54)]
    xs = np.linspace(1.15, 8.85, 6)
    top = 2.5
    for k, ((lab, Z, r), x) in enumerate(zip(ions, xs)):
        h = r / 171 * top
        acc = k == 5
        ax.add_patch(FancyBboxPatch((x - 0.44, 0.85), 0.88, h,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=C["acc_tint2"] if acc else C["grey_tint"],
                                    edgecolor=C["acc"] if acc else C["grey_edge"], lw=1.3))
        ax.text(x, 0.85 + h + 0.17, f"{r} pm", ha="center", fontsize=9,
                color=C["acc"] if acc else C["ink"], fontweight="bold")
        ax.text(x, 0.58, lab, ha="center", fontsize=10.5, color=C["ink"], fontweight="medium")
        ax.text(x, 0.28, f"{Z} p\u207a", ha="center", fontsize=8.2, color=C["muted"])
    # proton arrow
    arrow(ax, (1.0, 3.28), (9.0, 3.28), C, color=C["acc"], lw=1.5)
    ax.text(5.0, 3.48, "proton number rises 7 \u2192 13  \u00b7  same 10 electrons  \u00b7  radius falls",
            ha="center", fontsize=9.2, color=C["acc"], fontweight="medium")
    sub_label(ax, 0.55, 1.9, "all ions\n1s\u00b2 2s\u00b2 2p\u2076", C, fs=8.0, ha="left")
    save(fig, "isoelectronic-radii", C)


# ---------------------------------------------------------------- figure 6
def fig_ion_polarisation(C):
    fig = new_fig(7.6, 3.1)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (-0.15, 3.3))
    # panel A: ideal ions
    panel_title(ax, 2.35, 3.05, "pure ionic \u2014 no distortion", C, fs=10)
    ax.add_patch(Circle((1.1, 1.75), 0.52, facecolor=C["acc_tint2"], edgecolor=C["acc"], lw=1.4))
    ax.text(1.1, 1.75, "3+", ha="center", va="center", fontsize=10, color=C["acc"], fontweight="bold")
    ax.add_patch(Circle((3.45, 1.75), 1.05, facecolor=C["grey_tint"], edgecolor=C["grey_edge"], lw=1.4))
    ax.text(3.45, 1.75, "\u2212", ha="center", va="center", fontsize=13, color=C["ink"])
    sub_label(ax, 2.3, 0.35, "anion \u2014 a perfect sphere of charge", C, fs=8.2)
    # panel B: polarised
    panel_title(ax, 7.4, 3.05, "polarised \u2014 covalent character", C, fs=10)
    cxb, cyb = 5.65, 1.75
    ax.add_patch(Circle((cxb, cyb), 0.52, facecolor=C["acc_tint2"], edgecolor=C["acc"], lw=1.4))
    ax.text(cxb, cyb, "3+", ha="center", va="center", fontsize=10, color=C["acc"], fontweight="bold")
    # anion drawn as an oval stretched towards the cation
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((8.45, 1.75), 2.15, 1.75, facecolor=C["grey_tint"],
                         edgecolor=C["grey_edge"], lw=1.4))
    ax.text(8.45, 1.75, "\u2212", ha="center", va="center", fontsize=13, color=C["ink"])
    # shared-density region between the nuclei
    ax.add_patch(Circle((7.05, 1.75), 0.30, facecolor=C["acc_tint"], edgecolor=C["acc"], lw=1.0))
    ax.text(7.1, 0.32, "electron density pulled between the nuclei", ha="center",
            fontsize=8.4, color=C["acc"])
    save(fig, "ion-polarisation", C)


# ---------------------------------------------------------------- figure 7
def fig_polarising_power(C):
    fig = new_fig(7.6, 3.4)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 3.6))
    # cations row
    panel_title(ax, 5.0, 3.35, "Cations \u2014 polarising power", C, fs=10.5)
    cat = [("Na\u207a", "+1", 0.52), ("Li\u207a", "+1", 0.40), ("Al\u00b3\u207a", "+3", 0.34)]
    xs = [1.6, 3.5, 5.4]
    for (lab, ch, r), x in zip(cat, xs):
        ax.add_patch(Circle((x, 2.35), r, facecolor=C["acc_tint2"], edgecolor=C["acc"], lw=1.4))
        ax.text(x, 2.35, ch, ha="center", va="center", fontsize=8.4, color=C["acc"], fontweight="bold")
        ax.text(x, 1.62, lab, ha="center", fontsize=10, color=C["ink"], fontweight="medium")
    arrow(ax, (6.2, 2.35), (9.3, 2.35), C, color=C["acc"], lw=1.6)
    ax.text(7.75, 2.72, "charge \u2191", ha="center", fontsize=8.4, color=C["acc"])
    ax.text(7.75, 1.98, "radius \u2193", ha="center", fontsize=8.4, color=C["acc"])
    ax.text(7.75, 2.35, "polarising\npower \u2191", ha="center", va="center", fontsize=8.8,
            color=C["acc"], fontweight="medium")
    # anions row
    panel_title(ax, 5.0, 1.28, "Anions \u2014 polarisability", C, fs=10.5)
    an = [("F\u207b", 0.44), ("Cl\u207b", 0.56), ("I\u207b", 0.70)]
    for (lab, r), x in zip(an, xs):
        ax.add_patch(Circle((x, 0.52), r, facecolor=C["grey_tint"], edgecolor=C["grey_edge"], lw=1.4))
        ax.text(x, 0.52, lab, ha="center", va="center", fontsize=8.6, color=C["ink"])
    arrow(ax, (6.2, 0.52), (9.3, 0.52), C, color=C["acc"], lw=1.6)
    ax.text(7.75, 0.52, "polarisability \u2191\n(radius \u2191, charge \u2191)", ha="center",
            va="center", fontsize=8.4, color=C["acc"], fontweight="medium")
    sub_label(ax, 1.6, 0.05, "large + highly charged = easily distorted", C, fs=8.0, color=C["faint"])
    save(fig, "polarising-power", C)


# ---------------------------------------------------------------- figure 8
def fig_metallic_lattice(C):
    fig = new_fig(7.2, 3.9)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 4.2))
    rng = np.random.default_rng(7)
    # electron sea first (behind)
    ex = rng.uniform(0.8, 9.2, 46)
    ey = rng.uniform(0.55, 3.55, 46)
    ax.plot(ex, ey, 'o', ms=2.6, color=C["acc"], alpha=0.75, zorder=1)
    # cation layers (rows shifted like a lattice)
    for row, y in enumerate((1.05, 2.1, 3.15)):
        off = 0.0 if row % 2 == 0 else 0.62
        for k in range(5):
            x = 1.35 + k * 1.55 + off
            ax.add_patch(Circle((x, y), 0.40, facecolor=C["grey_tint"],
                                edgecolor=C["grey_edge"], lw=1.3, zorder=3))
            ax.text(x, y, "M\u207a", ha="center", va="center", fontsize=8.0,
                    color=C["ink"], zorder=4)
    # layer guides
    for y in (1.05, 2.1, 3.15):
        ax.plot([0.7, 9.3], [y, y], color=C["hair"], lw=0.8, ls=(0, (2, 4)), zorder=0)
    sub_label(ax, 9.55, 3.15, "cation layer", C, fs=8.2, ha="right")
    ax.text(5.0, 3.85, "fixed positive ions in regular layers \u2014 surrounded by a sea of mobile, delocalised electrons",
            ha="center", fontsize=9.4, color=C["ink"])
    ax.text(5.0, 0.22, "\u2022 delocalised electrons \u2014 mobile, not attached to any single ion",
            ha="center", fontsize=8.8, color=C["acc"], fontweight="medium")
    save(fig, "metallic-lattice", C)


# ---------------------------------------------------------------- figure 9
def fig_metallic_slide(C):
    fig = new_fig(7.6, 3.6)
    ax = fig.add_subplot(111)
    axis_frame(ax, (0, 10), (0, 3.8))

    def grid(xoff, y0, nrows=3, ncols=4):
        for row in range(nrows):
            y = y0 + row * 0.85
            for k in range(ncols):
                x = 1.3 + k * 1.15 + xoff
                ax.add_patch(Circle((x, y), 0.30, facecolor=C["grey_tint"],
                                    edgecolor=C["grey_edge"], lw=1.2, zorder=3))
                ax.text(x, y, "+", ha="center", va="center", fontsize=9,
                        color=C["ink"], zorder=4)

    panel_title(ax, 2.9, 3.5, "before \u2014 layers aligned", C, fs=9.8)
    grid(0, 0.9)
    panel_title(ax, 7.55, 3.5, "after \u2014 top layer slides", C, fs=9.8)
    grid(0.55, 0.9, nrows=3, ncols=4)
    # electrons adjust (drawn between ions on both panels)
    rng = np.random.default_rng(11)
    ax.plot(rng.uniform(1.0, 5.4, 14), rng.uniform(0.85, 3.0, 14), 'o', ms=2.4,
            color=C["acc"], alpha=0.8, zorder=1)
    ax.plot(rng.uniform(6.0, 9.9, 14), rng.uniform(0.85, 3.0, 14), 'o', ms=2.4,
            color=C["acc"], alpha=0.8, zorder=1)
    # slide arrow between panels
    arrow(ax, (5.0, 3.05), (6.3, 3.05), C, color=C["acc"], lw=1.8, mut=14)
    sub_label(ax, 5.65, 3.3, "force", C, fs=8.2, color=C["acc"])
    ax.text(5.0, 0.45, "the non-directional sea of electrons adjusts \u2014 the metallic bond never breaks",
            ha="center", fontsize=9.4, color=C["acc"], fontweight="medium")
    save(fig, "metallic-slide", C)


ALL = {
    "evidence-ions": fig_evidence_ions,
    "dot-cross-ions": fig_dot_cross_ions,
    "ionic-lattice": fig_ionic_lattice,
    "mp-comparison": fig_mp_comparison,
    "isoelectronic-radii": fig_isoelectronic_radii,
    "ion-polarisation": fig_ion_polarisation,
    "polarising-power": fig_polarising_power,
    "metallic-lattice": fig_metallic_lattice,
    "metallic-slide": fig_metallic_slide,
}

if __name__ == "__main__":
    for name, fn in ALL.items():
        for theme in (LIGHT, DARK):
            fn(theme)
    print("done: topic 3 part 1 diagrams")

