#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams for the IAL Chemistry site — Topic 3.

Outputs light + dark variants for each diagram into public/diagrams/.
Style follows the site token contract: neutral canvas, coral accent #F5654A,
hairline strokes, DejaVu labels, transparent background.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon

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


def axis_frame(ax, C):
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])


def atom(ax, x, y, C, r=0.34, label="", fs=11, fc=None, ec=None, lw=1.1, tc=None, zorder=6):
    ax.add_patch(Circle((x, y), r, facecolor=fc or C["fill"], edgecolor=ec or C["ink"],
                        lw=lw, zorder=zorder))
    if label:
        ax.text(x, y, label, fontsize=fs, color=tc or C["ink"], ha="center", va="center",
                zorder=zorder + 1)


def bond_line(ax, x1, y1, x2, y2, C, lw=1.6, color=None, ls="-", zorder=3):
    ax.plot([x1, x2], [y1, y2], ls=ls, lw=lw, color=color or C["ink"], zorder=zorder,
            solid_capstyle="round")


def wedge(ax, x1, y1, x2, y2, C, w=0.30, color=None, zorder=3):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = -dy / L, dx / L
    ax.add_patch(Polygon([(x1, y1), (x2 + ux * w, y2 + uy * w), (x2 - ux * w, y2 - uy * w)],
                         closed=True, facecolor=color or C["ink"], edgecolor="none",
                         zorder=zorder))


def dash_bond(ax, x1, y1, x2, y2, C, lw=1.8, color=None, zorder=2):
    ax.plot([x1, x2], [y1, y2], ls=(0, (2.2, 2.2)), lw=lw, color=color or C["ink"],
            zorder=zorder, solid_capstyle="round")


def angle_arc(ax, cx, cy, r, a1, a2, C, label="", lab_xy=None, color=None, fs=10):
    col = color or C["acc"]
    ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, angle=0, theta1=min(a1, a2),
                     theta2=max(a1, a2), color=col, lw=1.5, zorder=7))
    if label:
        if lab_xy is None:
            mid = math.radians((a1 + a2) / 2)
            lab_xy = (cx + 1.45 * r * math.cos(mid), cy + 1.45 * r * math.sin(mid))
        ax.text(lab_xy[0], lab_xy[1], label, fontsize=fs, color=col, ha="center",
                va="center", zorder=8)


def lone_lobe(ax, x, y, C, w=0.34, h=0.5, angle=0, color=None, ec=None, zorder=4):
    ax.add_patch(Ellipse((x, y), w, h, angle=angle,
                         facecolor=color or C["grey_tint"], edgecolor=ec or C["grey_edge"],
                         lw=0.9, zorder=zorder))


def dipole_arrow(ax, x1, y1, x2, y2, C, color=None, lw=1.7, zorder=8):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, lw=lw, color=color or C["acc"],
                                 zorder=zorder, shrinkA=0, shrinkB=0))


def panel_title(ax, x, y, text, C, fs=10.5):
    ax.text(x, y, text, fontsize=fs, color=C["ink"], ha="center", va="center",
            fontweight="medium")


def sub_label(ax, x, y, text, C, fs=8.6):
    ax.text(x, y, text, fontsize=fs, color=C["muted"], ha="center", va="center")


# ---- dot-and-cross primitives ---------------------------------------------
def _dot(ax, x, y, C):
    ax.add_patch(Circle((x, y), 0.048, facecolor=C["ink"], edgecolor="none", zorder=9))


def _cross(ax, x, y, C):
    s = 0.046
    col = "#b03a1e" if C is LIGHT else "#ffa090"
    ax.plot([x - s, x + s], [y - s, y + s], color=col, lw=1.3, zorder=9)
    ax.plot([x - s, x + s], [y + s, y - s], color=col, lw=1.3, zorder=9)


def pair_h(ax, x, y, C, s1="dot", s2="cross"):
    """Shared pair drawn horizontally: symbol 1 left of symbol 2."""
    for dx, sym in ((-0.078, s1), (0.078, s2)):
        (_dot if sym == "dot" else _cross)(ax, x + dx, y, C)


def lone_on_shell(ax, cx, cy, r, ang_deg, C, sym="dot"):
    """Lone pair sitting ON a shell of radius r at angle ang, tangent to it."""
    a = math.radians(ang_deg)
    px, py = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    for s in (-0.078, 0.078):
        (_dot if sym == "dot" else _cross)(ax, px + tx * s, py + ty * s, C)


def shell(ax, x, y, r, C):
    ax.add_patch(Circle((x, y), r, fill=False, edgecolor=C["hair"], lw=1.0,
                        linestyle=(0, (3, 2.6)), zorder=1))


# ────────────────────────────────────────────────────────────────────
# 1) Sigma bonds — head-on overlap (s–s, s–p, p–p)
# ────────────────────────────────────────────────────────────────────
def sigma_bonds(C):
    fig = new_fig(11.4, 3.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 3.6); ax.axis("off")
    cy = 2.05

    # panel A: s–s (two circles overlapping)
    cxA = 2.0
    ax.add_patch(Circle((cxA - 0.55, cy), 0.75, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Circle((cxA + 0.55, cy), 0.75, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxA, cy), 0.42, 1.0, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.add_patch(Circle((cxA - 0.55, cy), 0.055, facecolor=C["ink"], zorder=7))
    ax.add_patch(Circle((cxA + 0.55, cy), 0.055, facecolor=C["ink"], zorder=7))
    _dot(ax, cxA - 0.075, cy, C)
    _cross(ax, cxA + 0.075, cy, C)
    panel_title(ax, cxA, 0.72, "s–s overlap — H₂", C)

    # panel B: s–p
    cxB = 5.7
    ax.add_patch(Circle((cxB - 0.85, cy), 0.72, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxB + 0.09, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxB + 0.75, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxB - 0.185, cy), 0.22, 0.5, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.add_patch(Circle((cxB - 0.85, cy), 0.055, facecolor=C["ink"], zorder=7))
    ax.add_patch(Circle((cxB + 0.42, cy), 0.055, facecolor=C["ink"], zorder=7))
    _dot(ax, cxB - 0.26, cy, C)
    _cross(ax, cxB - 0.11, cy, C)
    panel_title(ax, cxB, 0.72, "s–p overlap — HBr", C)

    # panel C: p–p
    cxC = 9.4
    for off in (-0.45, 0.45):
        ax.add_patch(Ellipse((cxC + off - 0.32, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
        ax.add_patch(Ellipse((cxC + off + 0.32, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxC, cy), 0.32, 0.4, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.add_patch(Circle((cxC - 0.45, cy), 0.055, facecolor=C["ink"], zorder=7))
    ax.add_patch(Circle((cxC + 0.45, cy), 0.055, facecolor=C["ink"], zorder=7))
    _dot(ax, cxC - 0.075, cy, C)
    _cross(ax, cxC + 0.075, cy, C)
    panel_title(ax, cxC, 0.72, "p–p overlap — F₂", C)

    sub_label(ax, 5.7, 0.3, "linear (head-on) overlap — the shared pair sits between the two nuclei, in the overlap zone", C)
    save(fig, "sigma-bonds", C)


# ────────────────────────────────────────────────────────────────────
# 2) Pi bond — lateral overlap of p orbitals
# ────────────────────────────────────────────────────────────────────
def pi_bond(C):
    fig = new_fig(11.4, 3.8)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 3.8); ax.axis("off")
    cy = 2.35

    # left: sigma (head-on) for contrast
    cxA = 3.0
    for off in (-0.45, 0.45):
        ax.add_patch(Ellipse((cxA + off - 0.32, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
        ax.add_patch(Ellipse((cxA + off + 0.32, cy), 0.66, 0.46, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
    ax.add_patch(Ellipse((cxA, cy), 0.3, 0.4, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.add_patch(Circle((cxA - 0.45, cy), 0.055, facecolor=C["ink"], zorder=7))
    ax.add_patch(Circle((cxA + 0.45, cy), 0.055, facecolor=C["ink"], zorder=7))
    panel_title(ax, cxA, 0.72, "σ — head-on overlap", C)
    sub_label(ax, cxA, 0.34, "density directly between the two nuclei", C)

    # right: pi (lateral) — two vertical p orbitals side by side
    cxB = 8.4
    for X in (cxB - 0.3, cxB + 0.3):
        ax.add_patch(Ellipse((X, cy + 0.52), 0.44, 0.92, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
        ax.add_patch(Ellipse((X, cy - 0.52), 0.44, 0.92, facecolor=C["acc_tint"], edgecolor=C["grey_edge"], lw=1.2, zorder=2))
        ax.add_patch(Circle((X, cy), 0.055, facecolor=C["ink"], zorder=7))
    bond_line(ax, cxB - 0.3, cy, cxB + 0.3, cy, C, lw=1.8, zorder=3)
    ax.add_patch(Ellipse((cxB, cy + 0.52), 0.24, 0.66, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cxB, cy - 0.52), 0.24, 0.66, facecolor=C["acc_tint2"], edgecolor="none", zorder=3))
    ax.text(cxB, cy + 1.32, "π overlap above the axis", fontsize=8.4, color=C["muted"], ha="center")
    ax.text(cxB, cy - 1.32, "π overlap below the axis", fontsize=8.4, color=C["muted"], ha="center")
    panel_title(ax, cxB, 0.72, "π — lateral (sideways) overlap", C)
    sub_label(ax, cxB, 0.34, "e.g. the second bond of the C=C in ethene — weaker than σ", C)
    save(fig, "pi-bond", C)


# ────────────────────────────────────────────────────────────────────
# 3) Dot-and-cross diagrams — six molecules
# ────────────────────────────────────────────────────────────────────
def dot_cross_molecules(C):
    fig = new_fig(11.4, 7.9)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 7.9); ax.axis("off")

    pos = [(2.0, 5.75), (5.7, 5.75), (9.4, 5.75), (2.0, 2.45), (5.7, 2.45), (9.4, 2.45)]
    titles = ["HCl — single bond", "H₂O — two single bonds", "CH₄ — four single bonds",
              "CO₂ — two double bonds", "O₂ — double bond", "N₂ — triple bond"]

    # HCl: H(0,0) r0.30 · Cl(0.92,0) r0.72 · pair at (0.30,0) · Cl lone pairs at 0,±90 …
    x, y = pos[0]
    shell(ax, x, y, 0.30, C); shell(ax, x + 0.92, y, 0.72, C)
    ax.text(x, y, "H", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    ax.text(x + 0.92, y, "Cl", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    pair_h(ax, x + 0.30, y, C)
    lone_on_shell(ax, x + 0.92, y, 0.72, 0, C, "dot")
    lone_on_shell(ax, x + 0.92, y, 0.72, 90, C, "dot")
    lone_on_shell(ax, x + 0.92, y, 0.72, 270, C, "dot")

    # H2O: O(0,0) r0.66 · H(±0.72,-0.62) r0.27 · LP at 60,120
    x, y = pos[1]
    shell(ax, x, y, 0.66, C)
    ax.text(x, y, "O", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    for sx in (-1, 1):
        hx, hy = x + 0.72 * sx, y - 0.62
        shell(ax, hx, hy, 0.27, C)
        ax.text(hx, hy, "H", fontsize=10, color=C["ink"], ha="center", va="center", zorder=8)
        dx, dy = hx - x, hy - y
        n = math.hypot(dx, dy)
        pair_h(ax, x + 0.56 * dx / n, y + 0.56 * dy / n, C)
    lone_on_shell(ax, x, y, 0.66, 60, C, "dot")
    lone_on_shell(ax, x, y, 0.66, 120, C, "dot")

    # CH4: C(0,0) r0.60 · H at 45,135,225,315 dist 1.02 r0.27
    x, y = pos[2]
    shell(ax, x, y, 0.60, C)
    ax.text(x, y, "C", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hx, hy = x + 1.02 * math.cos(a), y + 1.02 * math.sin(a)
        shell(ax, hx, hy, 0.27, C)
        ax.text(hx, hy, "H", fontsize=10, color=C["ink"], ha="center", va="center", zorder=8)
        pair_h(ax, x + 0.58 * math.cos(a), y + 0.58 * math.sin(a), C)

    # CO2: C(0,0) r0.55 · O(±1.1,0) r0.68 · 2 pairs per bond at ∓0.48, y ±0.11 · LP at 90,270
    x, y = pos[3]
    shell(ax, x, y, 0.55, C)
    ax.text(x, y, "C", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    for sx in (-1, 1):
        ox = x + 1.1 * sx
        shell(ax, ox, y, 0.68, C)
        ax.text(ox, y, "O", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
        pair_h(ax, x + 0.48 * sx, y + 0.11, C)
        pair_h(ax, x + 0.48 * sx, y - 0.11, C)
        lone_on_shell(ax, ox, y, 0.68, 90, C, "cross")
        lone_on_shell(ax, ox, y, 0.68, 270, C, "cross")

    # O2: O(±0.62,0) r0.72 · 2 stacked pairs at (0,±0.11) · LP 135/225 left, 45/315 right
    x, y = pos[4]
    for sx in (-1, 1):
        shell(ax, x + 0.62 * sx, y, 0.72, C)
        ax.text(x + 0.62 * sx, y, "O", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    pair_h(ax, x, y + 0.11, C)
    pair_h(ax, x, y - 0.11, C)
    lone_on_shell(ax, x - 0.62, y, 0.72, 135, C, "dot")
    lone_on_shell(ax, x - 0.62, y, 0.72, 225, C, "dot")
    lone_on_shell(ax, x + 0.62, y, 0.72, 45, C, "cross")
    lone_on_shell(ax, x + 0.62, y, 0.72, 315, C, "cross")

    # N2: N(±0.6,0) r0.75 · 3 pairs at y -0.2,0,0.2 · LP 135/225 left, 45/315 right
    x, y = pos[5]
    for sx in (-1, 1):
        shell(ax, x + 0.6 * sx, y, 0.75, C)
        ax.text(x + 0.6 * sx, y, "N", fontsize=10.5, color=C["ink"], ha="center", va="center", zorder=8)
    for off in (-0.2, 0.0, 0.2):
        pair_h(ax, x, y + off, C)
    lone_on_shell(ax, x - 0.6, y, 0.75, 135, C, "dot")
    lone_on_shell(ax, x - 0.6, y, 0.75, 225, C, "dot")
    lone_on_shell(ax, x + 0.6, y, 0.75, 45, C, "cross")
    lone_on_shell(ax, x + 0.6, y, 0.75, 315, C, "cross")

    for (px, py), t in zip(pos, titles):
        panel_title(ax, px, py - 1.5, t, C)
    sub_label(ax, 5.7, 0.38, "dots = electrons from one atom · crosses = electrons from the other · every shared pair is one covalent bond", C)
    save(fig, "dot-cross-molecules", C)


# ────────────────────────────────────────────────────────────────────
# 4) Dative covalent bonds — NH₄⁺, H₃O⁺, Al₂Cl₆
# ────────────────────────────────────────────────────────────────────
def dative_bonds(C):
    fig = new_fig(11.4, 3.9)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 3.9); ax.axis("off")

    def dative_bond(ax, x1, y1, x2, y2, C, rad=0.0):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                                     lw=1.5, color=C["acc"], zorder=6,
                                     connectionstyle=f"arc3,rad={rad}"))

    # panel 1: NH4+
    cx, cy = 1.9, 2.3
    atom(ax, cx, cy, C, r=0.36, label="N", fs=11.5)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        hx, hy = cx + 0.88 * math.cos(a), cy + 0.88 * math.sin(a)
        atom(ax, hx, hy, C, r=0.24, label="H", fs=9)
        if ang == 45:
            dative_bond(ax, cx + 0.36 * math.cos(a), cy + 0.36 * math.sin(a),
                        hx - 0.26 * math.cos(a), hy - 0.26 * math.sin(a), C)
            ax.text(cx + 1.28, cy + 0.62, "dative", fontsize=8.2, color=C["acc"], ha="center")
        else:
            bond_line(ax, cx + 0.36 * math.cos(a), cy + 0.36 * math.sin(a),
                      hx - 0.24 * math.cos(a), hy - 0.24 * math.sin(a), C)
    ax.text(cx, cy + 1.32, "NH₄⁺", fontsize=11.5, color=C["ink"], ha="center", fontweight="medium")
    sub_label(ax, cx, 0.86, "the lone pair of NH₃ is donated", C)
    sub_label(ax, cx, 0.6, "into the empty 1s orbital of H⁺", C)

    # panel 2: H3O+
    cx, cy = 5.7, 2.3
    atom(ax, cx, cy, C, r=0.36, label="O", fs=11.5)
    for ang in (30, 150, 270):
        a = math.radians(ang)
        hx, hy = cx + 0.88 * math.cos(a), cy + 0.88 * math.sin(a)
        atom(ax, hx, hy, C, r=0.24, label="H", fs=9)
        if ang == 30:
            dative_bond(ax, cx + 0.36 * math.cos(a), cy + 0.36 * math.sin(a),
                        hx - 0.26 * math.cos(a), hy - 0.26 * math.sin(a), C)
            ax.text(cx + 1.26, cy + 0.5, "dative", fontsize=8.2, color=C["acc"], ha="center")
        else:
            bond_line(ax, cx + 0.36 * math.cos(a), cy + 0.36 * math.sin(a),
                      hx - 0.24 * math.cos(a), hy - 0.24 * math.sin(a), C)
    lone_lobe(ax, cx - 0.3, cy + 0.52, C, w=0.3, h=0.44, angle=64)
    ax.text(cx, cy + 1.32, "H₃O⁺ (hydroxonium ion)", fontsize=11, color=C["ink"], ha="center", fontweight="medium")
    sub_label(ax, cx, 0.86, "the lone pair of H₂O is donated to H⁺", C)

    # panel 3: Al2Cl6
    alL, alR = (8.75, 2.35), (10.25, 2.35)
    bT, bB = (9.5, 3.02), (9.5, 1.68)
    tLT, tLB = (8.0, 3.02), (8.0, 1.68)
    tRT, tRB = (11.0, 3.02), (11.0, 1.68)
    atom(ax, *alL, C, r=0.34, label="Al", fs=10.5)
    atom(ax, *alR, C, r=0.34, label="Al", fs=10.5)
    for p in (bT, bB, tLT, tLB, tRT, tRB):
        atom(ax, *p, C, r=0.3, label="Cl", fs=9)
    bond_line(ax, alL[0] + 0.24, alL[1] + 0.2, bT[0] - 0.22, bT[1] - 0.1, C)
    bond_line(ax, alR[0] - 0.24, alR[1] - 0.2, bB[0] + 0.22, bB[1] + 0.1, C)
    bond_line(ax, alL[0] - 0.24, alL[1] + 0.2, tLT[0] + 0.22, tLT[1] - 0.1, C)
    bond_line(ax, alL[0] - 0.24, alL[1] - 0.2, tLB[0] + 0.22, tLB[1] + 0.1, C)
    bond_line(ax, alR[0] + 0.24, alR[1] + 0.2, tRT[0] - 0.22, tRT[1] - 0.1, C)
    bond_line(ax, alR[0] + 0.24, alR[1] - 0.2, tRB[0] - 0.22, tRB[1] + 0.1, C)
    dative_bond(ax, bT[0] + 0.26, bT[1] - 0.08, alR[0] - 0.26, alR[1] + 0.16, C, rad=-0.3)
    dative_bond(ax, bB[0] - 0.26, bB[1] + 0.08, alL[0] + 0.26, alL[1] - 0.16, C, rad=-0.3)
    ax.text(9.5, 3.68, "Al₂Cl₆ (the dimer)", fontsize=11, color=C["ink"], ha="center", fontweight="medium")
    sub_label(ax, 9.5, 1.14, "each bridging chlorine donates a lone pair", C)
    sub_label(ax, 9.5, 0.88, "into the empty orbital of the opposite aluminium", C)
    save(fig, "dative-bonds", C)


# ────────────────────────────────────────────────────────────────────
# 5) Octet exceptions — BeCl₂, BCl₃, PCl₅, SF₆
# ────────────────────────────────────────────────────────────────────
def octet_exceptions(C):
    fig = new_fig(11.5, 3.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.5); ax.set_ylim(0, 3.5); ax.axis("off")

    panels = [(1.5, "BeCl₂", "Be", 2, 90, 180, "4 electrons"),
              (4.3, "BCl₃", "B", 3, 90, 120, "6 electrons"),
              (7.1, "PCl₅ (gaseous)", "P", 5, 90, 72, "10 electrons"),
              (9.9, "SF₆", "S", 6, 90, 60, "12 electrons")]
    for cx, name, sym, n, a0, step, count in panels:
        outer = "Cl" if sym != "S" else "F"
        atom(ax, cx, 2.05, C, r=0.4, label=sym, fs=12)
        for k in range(n):
            a = math.radians(a0 + step * k)
            ex, ey = cx + 1.0 * math.cos(a), 2.05 + 1.0 * math.sin(a)
            bond_line(ax, cx + 0.4 * math.cos(a), 2.05 + 0.4 * math.sin(a),
                      ex - 0.28 * math.cos(a), ey - 0.28 * math.sin(a), C)
            atom(ax, ex, ey, C, r=0.28, label=outer, fs=8.5)
            pair_h(ax, cx + 0.7 * math.cos(a), 2.05 + 0.7 * math.sin(a), C)
        panel_title(ax, cx, 0.52, name, C)
        sub_label(ax, cx, 0.24, count + " around the central atom", C)
    save(fig, "octet-exceptions", C)


# ────────────────────────────────────────────────────────────────────
# 6) Carbon lattices — diamond, graphite, graphene
# ────────────────────────────────────────────────────────────────────
def _honeycomb(ax, cx, cy, cols, rows, s, C, alpha=1.0, lw=1.1, zorder=3):
    """Pointy-top hexagons sharing edges."""
    w = math.sqrt(3) * s
    for r in range(rows):
        for c in range(cols):
            ox = cx + c * w + (w / 2 if r % 2 else 0)
            oy = cy + r * 1.5 * s
            pts = [(ox + s * math.cos(math.radians(30 + 60 * k)),
                    oy + s * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
            pts.append(pts[0])
    # draw hexagon edges
    for r in range(rows):
        for c in range(cols):
            ox = cx + c * w + (w / 2 if r % 2 else 0)
            oy = cy + r * 1.5 * s
            pts = [(ox + s * math.cos(math.radians(30 + 60 * k)),
                    oy + s * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
            for k in range(6):
                x1, y1 = pts[k]; x2, y2 = pts[(k + 1) % 6]
                ax.plot([x1, x2], [y1, y2], color=C["ink"], lw=lw, alpha=alpha, zorder=zorder)
                ax.add_patch(Circle(pts[k], 0.038, facecolor=C["ink"], alpha=alpha, zorder=zorder + 2))


def carbon_lattices(C):
    fig = new_fig(11.4, 4.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 4.0); ax.axis("off")

    # ── diamond: isometric projection of the diamond lattice, centred
    pts = set()
    fcc = [(0, 0, 0), (0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                for f in fcc:
                    for b in ((0, 0, 0), (.25, .25, .25)):
                        p = (round(i + f[0] + b[0], 3), round(j + f[1] + b[1], 3), round(k + f[2] + b[2], 3))
                        pts.add(p)

    def proj(p):
        x, y, z = p
        return ((x - y) / math.sqrt(2), (x + y - 2 * z) / math.sqrt(6), x + y + z)

    scr = {p: proj(p) for p in pts}
    xs = [v[0] for v in scr.values()]; ys = [v[1] for v in scr.values()]
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    k = 3.0 / span
    cxp, cyp = 1.95, 2.25

    bonds = set()
    pl = sorted(pts)
    for i, p in enumerate(pl):
        for q in pl[i + 1:]:
            if math.dist(p, q) < 0.45:
                bonds.add((p, q))
    for p, q in bonds:
        X1, Y1, d1 = scr[p]; X2, Y2, d2 = scr[q]
        depth = (d1 + d2) / 2
        alpha = 0.85 if depth > 3.4 else (0.4 if depth > 2.9 else 0.16)
        ax.plot([cxp + (X1 - mx) * k, cxp + (X2 - mx) * k],
                [cyp + (Y1 - my) * k, cyp + (Y2 - my) * k],
                color=C["ink"], lw=1.25 if depth > 3.4 else 0.8, alpha=alpha, zorder=2)
    for p, (X, Y, d) in scr.items():
        front = d > 3.4
        ax.add_patch(Circle((cxp + (X - mx) * k, cyp + (Y - my) * k), 0.06 if front else 0.045,
                            facecolor=C["acc"] if front else C["ink"],
                            alpha=0.95 if front else 0.35, edgecolor="none", zorder=4))
    panel_title(ax, 1.95, 0.5, "Diamond — tetrahedral 3D network", C)

    # ── graphite: three stacked layers
    cxg = 6.3
    _honeycomb(ax, cxg + 0.3, 2.75, 4, 2, 0.34, C, alpha=0.22, lw=0.9)
    _honeycomb(ax, cxg + 0.15, 2.3, 4, 2, 0.34, C, alpha=0.45, lw=1.0)
    _honeycomb(ax, cxg, 1.85, 4, 2, 0.34, C, alpha=1.0, lw=1.15)
    ax.annotate("", xy=(cxg + 1.62, 2.95), xytext=(cxg + 1.62, 1.7),
                arrowprops=dict(arrowstyle="<|-|>", color=C["faint"], lw=1.1))
    ax.text(cxg + 1.78, 2.32, "weak London forces\nbetween the layers", fontsize=7.8,
            color=C["muted"], va="center")
    panel_title(ax, cxg, 0.5, "Graphite — layers of hexagons", C)

    # ── graphene: a single sheet
    _honeycomb(ax, 9.7, 1.95, 4, 3, 0.3, C, alpha=1.0, lw=1.15)
    panel_title(ax, 9.85, 0.5, "Graphene — one atom thick", C)
    save(fig, "carbon-lattices", C)


# ────────────────────────────────────────────────────────────────────
# 7) Electron density maps — Cl₂ vs HCl (theme-aware palette)
# ────────────────────────────────────────────────────────────────────
def _density_cmap(C):
    if C is LIGHT:
        return matplotlib.colors.LinearSegmentedColormap.from_list(
            "dens", [(1, 1, 1, 0), "#fbd9cf", "#f2a893", "#e2664a", "#b0321f"])
    return matplotlib.colors.LinearSegmentedColormap.from_list(
        "dens", [(0, 0, 0, 0), "#3d1d16", "#8c3a26", "#e2664a", "#ffb096"])


def electron_density(C):
    fig = new_fig(10.0, 3.4)
    axA = fig.add_axes([0.03, 0.05, 0.44, 0.8]); axB = fig.add_axes([0.52, 0.05, 0.44, 0.8])
    cmap = _density_cmap(C)
    for ax in (axA, axB):
        axis_frame(ax, C)

    n = 220
    xs = np.linspace(-2.2, 2.2, n); ys = np.linspace(-1.2, 1.2, n)
    X, Y = np.meshgrid(xs, ys)

    def blob(x0, y0, sx, sy, amp):
        return amp * np.exp(-(((X - x0) ** 2) / (2 * sx ** 2) + ((Y - y0) ** 2) / (2 * sy ** 2)))

    Z = blob(-0.85, 0, 0.55, 0.42, 1.0) + blob(0.85, 0, 0.55, 0.42, 1.0) + blob(0, 0, 0.62, 0.4, 0.9)
    axA.contourf(X, Y, Z, levels=np.linspace(0.1, 1.95, 12), cmap=cmap)
    axA.add_patch(Circle((-0.85, 0), 0.09, facecolor=C["ink"], zorder=6))
    axA.add_patch(Circle((0.85, 0), 0.09, facecolor=C["ink"], zorder=6))
    axA.text(-0.85, -0.88, "Cl", fontsize=11, color=C["ink"], ha="center")
    axA.text(0.85, -0.88, "Cl", fontsize=11, color=C["ink"], ha="center")
    axA.text(0, 1.04, "equal, symmetrical sharing", fontsize=8.4, color=C["muted"], ha="center")
    axA.set_title("Cl₂", fontsize=11, color=C["ink"], pad=2)

    Z = blob(-1.0, 0, 0.5, 0.4, 0.65) + blob(1.0, 0, 0.62, 0.46, 1.25) + blob(0.42, 0, 0.42, 0.34, 0.75)
    axB.contourf(X, Y, Z, levels=np.linspace(0.1, 1.95, 12), cmap=cmap)
    axB.add_patch(Circle((-1.0, 0), 0.07, facecolor=C["ink"], zorder=6))
    axB.add_patch(Circle((1.0, 0), 0.09, facecolor=C["ink"], zorder=6))
    axB.text(-1.0, -0.88, "H", fontsize=11, color=C["ink"], ha="center")
    axB.text(1.0, -0.88, "Cl", fontsize=11, color=C["ink"], ha="center")
    axB.text(0.35, 1.04, "density pulled towards the more electronegative atom", fontsize=8.4, color=C["muted"], ha="center")
    axB.set_title("HCl", fontsize=11, color=C["ink"], pad=2)
    save(fig, "electron-density", C)


# ────────────────────────────────────────────────────────────────────
# 8) Bond polarity — non-polar vs polar (theme-aware palette)
# ────────────────────────────────────────────────────────────────────
def bond_polarity(C):
    fig = new_fig(10.0, 3.3)
    axA = fig.add_axes([0.03, 0.05, 0.44, 0.82]); axB = fig.add_axes([0.52, 0.05, 0.44, 0.82])
    cmap = _density_cmap(C)
    for ax in (axA, axB):
        axis_frame(ax, C)

    n = 220
    xs = np.linspace(-2.2, 2.2, n); ys = np.linspace(-1.1, 1.1, n)
    X, Y = np.meshgrid(xs, ys)

    def blob(x0, y0, sx, sy, amp):
        return amp * np.exp(-(((X - x0) ** 2) / (2 * sx ** 2) + ((Y - y0) ** 2) / (2 * sy ** 2)))

    Z = blob(-0.95, 0, 0.5, 0.4, 1.0) + blob(0.95, 0, 0.5, 0.4, 1.0) + blob(0, 0, 0.55, 0.38, 1.0)
    axA.contourf(X, Y, Z, levels=np.linspace(0.1, 1.95, 12), cmap=cmap)
    axA.add_patch(Circle((-0.95, 0), 0.08, facecolor=C["ink"], zorder=6))
    axA.add_patch(Circle((0.95, 0), 0.08, facecolor=C["ink"], zorder=6))
    axA.text(-0.95, -0.84, "A", fontsize=11, color=C["ink"], ha="center")
    axA.text(0.95, -0.84, "A", fontsize=11, color=C["ink"], ha="center")
    axA.text(0, 0.97, "same electronegativity — equal share, no charges", fontsize=8.4, color=C["muted"], ha="center")
    axA.set_title("Non-polar bond  (ΔX = 0)", fontsize=10.5, color=C["ink"], pad=2)

    Z = blob(-0.95, 0, 0.44, 0.36, 0.55) + blob(0.95, 0, 0.62, 0.46, 1.3) + blob(0.35, 0, 0.4, 0.32, 0.7)
    axB.contourf(X, Y, Z, levels=np.linspace(0.1, 1.95, 12), cmap=cmap)
    axB.add_patch(Circle((-0.95, 0), 0.08, facecolor=C["ink"], zorder=6))
    axB.add_patch(Circle((0.95, 0), 0.08, facecolor=C["ink"], zorder=6))
    axB.text(-0.95, -0.84, "Aδ⁺", fontsize=10.5, color=C["ink"], ha="center")
    axB.text(0.95, -0.84, "Zδ⁻", fontsize=10.5, color=C["ink"], ha="center")
    dipole_arrow(axB, -0.75, 0.55, 0.75, 0.55, C)
    axB.text(0, 0.97, "electron drift towards Z — a dipole is induced", fontsize=8.4, color=C["muted"], ha="center")
    axB.set_title("Polar covalent bond  (0 < ΔX < 1.7)", fontsize=10.5, color=C["ink"], pad=2)
    save(fig, "bond-polarity", C)


# ────────────────────────────────────────────────────────────────────
# 9) The bonding continuum
# ────────────────────────────────────────────────────────────────────
def bonding_continuum(C):
    fig = new_fig(10.6, 3.2)
    ax = fig.add_axes([0.06, 0.16, 0.88, 0.5])
    axis_frame(ax, C)
    grad = np.linspace(0, 1, 512).reshape(1, -1)
    ax.imshow(grad, extent=[0, 10, 0, 1], aspect="auto",
              cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
                  "cont", ["#f0b2a4", ACCENT, "#8d5a50"]), alpha=0.85, zorder=1)
    ax.set_xlim(0, 10); ax.set_ylim(0, 1)
    for val, lab in ((0, "0"), (2.25, "0.9"), (4.25, "1.7"), (10, "3.0")):
        ax.plot([val, val], [-0.1, -0.02], color=C["muted"], lw=1.0, clip_on=False)
        ax.text(min(max(val, 0.18), 9.82), -0.32, lab, fontsize=8.6, color=C["muted"], ha="center")
    ax.text(5, -0.75, "electronegativity difference ΔX  →", fontsize=9.2, color=C["muted"], ha="center")
    ax.plot([4.25, 4.25], [0, 1], color=C["ink"], lw=1.2, ls=(0, (4, 3)), zorder=3)
    ax.text(4.25, 1.22, "ΔX = 1.7", fontsize=8.6, color=C["ink"], ha="center")
    ax.text(1.6, 1.32, "pure covalent", fontsize=9.6, color=C["ink"], ha="center", fontweight="medium")
    ax.text(6.6, 1.32, "polar covalent", fontsize=9.6, color=C["ink"], ha="center", fontweight="medium")
    ax.text(8.9, 1.32, "ionic", fontsize=9.6, color=C["ink"], ha="center", fontweight="medium")
    species = [(0.12, "Cl₂ · H₂"), (2.25, "H₂O · HCl"), (4.5, "SrBr₂"), (5.25, "NaCl"), (9.82, "LiF")]
    for val, name in species:
        ax.plot([val], [0.5], marker="o", ms=5.5, color=C["ink"], zorder=5)
        ax.annotate(name, xy=(val, 0.5), xytext=(val, 0.06), fontsize=8.4, color=C["ink"],
                    ha="center", zorder=6,
                    arrowprops=dict(arrowstyle="-", color=C["faint"], lw=0.9))
    ax.text(5, -1.15, "ionic and covalent bonding are the extremes of a continuum of bonding type",
            fontsize=9, color=C["muted"], ha="center", style="italic")
    save(fig, "bonding-continuum", C)


# ────────────────────────────────────────────────────────────────────
# 10) Electronegativity trends (Pauling values)
# ────────────────────────────────────────────────────────────────────
def electronegativity_trends(C):
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.2, 3.4), dpi=160)
    fig.patch.set_alpha(0)
    for ax in (axA, axB):
        ax.set_facecolor("none")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(C["hair"])
        ax.tick_params(colors=C["muted"], labelsize=8.5)

    per3 = ["Na", "Mg", "Al", "Si", "P", "S", "Cl"]
    vals3 = [0.9, 1.2, 1.5, 1.8, 2.1, 2.5, 3.0]
    axA.bar(per3, vals3, color=ACCENT, alpha=0.85, width=0.62)
    for i, v in enumerate(vals3):
        axA.text(i, v + 0.07, f"{v}", fontsize=8, color=C["muted"], ha="center")
    axA.set_ylim(0, 4.4)
    axA.set_title("Across Period 3 — increases", fontsize=10.5, color=C["ink"], pad=8)
    axA.set_ylabel("Pauling electronegativity", fontsize=9, color=C["muted"])

    g17 = ["F", "Cl", "Br", "I"]
    vals17 = [4.0, 3.0, 2.8, 2.5]
    axB.bar(g17, vals17, color=ACCENT, alpha=0.85, width=0.5)
    for i, v in enumerate(vals17):
        axB.text(i, v + 0.07, f"{v}", fontsize=8, color=C["muted"], ha="center")
    axB.set_ylim(0, 4.4)
    axB.set_title("Down Group 17 — decreases", fontsize=10.5, color=C["ink"], pad=8)
    fig.subplots_adjust(wspace=0.3, left=0.08, right=0.98, top=0.86, bottom=0.1)
    save(fig, "electronegativity-trends", C)


# ────────────────────────────────────────────────────────────────────
# 11) Molecular polarity — CCl₄ vs CHCl₃ vs H₂O
# ────────────────────────────────────────────────────────────────────
def molecular_polarity(C):
    fig = new_fig(11.6, 4.1)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.6); ax.set_ylim(0, 4.1); ax.axis("off")
    cy = 2.15

    # CCl4
    cx = 2.0
    atom(ax, cx, cy, C, r=0.4, label="C", fs=12)
    for dx, dy in ((0, 1.0), (0, -1.0), (-1.0, 0), (1.0, 0)):
        atom(ax, cx + dx, cy + dy, C, r=0.32, label="Cl", fs=9)
        bond_line(ax, cx + 0.4 * dx, cy + 0.4 * dy, cx + 0.68 * dx, cy + 0.68 * dy, C)
        dipole_arrow(ax, cx + 0.46 * dx, cy + 0.46 * dy, cx + 0.66 * dx, cy + 0.66 * dy, C, lw=1.3)
    panel_title(ax, cx, 0.62, "CCl₄ — dipoles cancel", C)
    sub_label(ax, cx, 0.3, "symmetrical → non-polar", C)

    # CHCl3
    cx = 5.8
    atom(ax, cx, cy, C, r=0.4, label="C", fs=12)
    for dx, dy, lab in ((0, 1.0, "H"), (0, -1.0, "Cl"), (-1.0, 0, "Cl"), (1.0, 0, "Cl")):
        atom(ax, cx + dx, cy + dy, C, r=0.32, label=lab, fs=9)
        bond_line(ax, cx + 0.4 * dx, cy + 0.4 * dy, cx + 0.68 * dx, cy + 0.68 * dy, C)
        if lab == "Cl":
            dipole_arrow(ax, cx + 0.46 * dx, cy + 0.46 * dy, cx + 0.66 * dx, cy + 0.66 * dy, C, lw=1.3)
    dipole_arrow(ax, cx, cy - 1.08, cx, cy - 1.44, C)
    ax.text(cx + 0.14, cy - 1.28, "net dipole", fontsize=8.2, color=C["acc"], ha="left")
    ax.text(cx, cy + 1.62, "H is less electronegative than C —", fontsize=8, color=C["muted"], ha="center")
    ax.text(cx, cy + 1.44, "the three C–Cl dipoles cannot cancel", fontsize=8, color=C["muted"], ha="center")
    panel_title(ax, cx, 0.62, "CHCl₃ — dipoles do not cancel", C)
    sub_label(ax, cx, 0.3, "overall polar", C)

    # H2O — O centre, H below, lone lobes above
    cx = 9.6
    atom(ax, cx, cy, C, r=0.4, label="O", fs=12)
    h1 = (cx - 0.85, cy - 0.72); h2 = (cx + 0.85, cy - 0.72)
    atom(ax, *h1, C, r=0.28, label="H", fs=9.5)
    atom(ax, *h2, C, r=0.28, label="H", fs=9.5)
    bond_line(ax, cx - 0.3, cy - 0.28, h1[0] + 0.2, h1[1] + 0.16, C)
    bond_line(ax, cx + 0.3, cy - 0.28, h2[0] - 0.2, h2[1] + 0.16, C)
    lone_lobe(ax, cx - 0.38, cy + 0.62, C, w=0.32, h=0.46, angle=-20)
    lone_lobe(ax, cx + 0.38, cy + 0.62, C, w=0.32, h=0.46, angle=20)
    angle_arc(ax, cx, cy, 0.52, 237, 303, C, "104.5°", lab_xy=(cx, cy - 1.18), fs=9.5)
    dipole_arrow(ax, cx + 1.45, cy - 0.85, cx + 1.45, cy + 0.45, C)
    ax.text(cx + 1.45, cy + 0.68, "net dipole", fontsize=8.2, color=C["acc"], ha="center")
    panel_title(ax, cx, 0.62, "H₂O — angular", C)
    sub_label(ax, cx, 0.3, "not symmetrical → polar", C)
    save(fig, "molecular-polarity", C)


# ────────────────────────────────────────────────────────────────────
# 12) Liquid jets experiment
# ────────────────────────────────────────────────────────────────────
def liquid_jets(C):
    fig = new_fig(9.6, 4.1)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 9.6); ax.set_ylim(0, 4.1); ax.axis("off")

    def burette(cx, deflected):
        ax.add_patch(FancyBboxPatch((cx - 0.16, 2.0), 0.32, 1.7, boxstyle="square,pad=0",
                                    facecolor=C["grey_tint"], edgecolor=C["grey_edge"], lw=1.0, zorder=2))
        ax.add_patch(Polygon([(cx - 0.16, 2.0), (cx + 0.16, 2.0), (cx, 1.78)], closed=True,
                             facecolor=C["grey_tint"], edgecolor=C["grey_edge"], lw=1.0, zorder=2))
        ax.text(cx, 3.85, "burette", fontsize=8.4, color=C["muted"], ha="center")
        ax.add_patch(FancyBboxPatch((cx + 0.55, 1.25), 0.3, 1.15, boxstyle="square,pad=0.02",
                                    facecolor=C["acc_tint"], edgecolor=C["acc"], lw=1.2, zorder=3))
        ax.text(cx + 0.7, 2.62, "charged\nrod", fontsize=7.6, color=C["acc"], ha="center")
        if deflected:
            t = np.linspace(0, 1, 60)
            xj = cx + 0.58 * t ** 2
            yj = 1.78 - 1.52 * t
            ax.plot(xj, yj, color=ACCENT, lw=2.0, zorder=4, solid_capstyle="round")
            ax.text(cx + 1.25, 0.5, "jet deflects", fontsize=8.6, color=C["ink"], ha="center")
        else:
            ax.plot([cx, cx], [1.78, 0.26], color=C["ink"], lw=2.0, zorder=4,
                    solid_capstyle="round")
            ax.text(cx + 0.9, 0.5, "jet falls straight", fontsize=8.6, color=C["ink"], ha="center")

    burette(2.6, True)
    burette(6.6, False)
    panel_title(ax, 2.6, 3.5, "Polar liquid (water, ethanol)", C)
    panel_title(ax, 6.6, 3.5, "Non-polar liquid (cyclohexane)", C)
    sub_label(ax, 4.8, 0.12, "the charged rod attracts the polar molecules — the jet is deflected towards it", C)
    save(fig, "liquid-jets", C)


# ────────────────────────────────────────────────────────────────────
# 13) VSEPR — the five regular arrangements
# ────────────────────────────────────────────────────────────────────
def vsepr_shapes(C):
    fig = new_fig(12.6, 4.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.6); ax.set_ylim(0, 4.0); ax.axis("off")

    L = 0.8
    rA, rB = 0.3, 0.26
    cy = 2.35

    # linear
    cx = 1.45
    atom(ax, cx, cy, C, r=rA, label="A", fs=10)
    atom(ax, cx - L, cy, C, r=rB, label="B", fs=9.5)
    atom(ax, cx + L, cy, C, r=rB, label="B", fs=9.5)
    bond_line(ax, cx - rA, cy, cx - L + rB, cy, C); bond_line(ax, cx + rA, cy, cx + L - rB, cy, C)
    panel_title(ax, cx, 0.92, "Linear", C); sub_label(ax, cx, 0.6, "2 pairs · 180°", C)

    # trigonal planar
    cx = 3.95
    atom(ax, cx, cy, C, r=rA, label="A", fs=10)
    for ang in (90, 210, 330):
        a = math.radians(ang)
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a)
        atom(ax, ex, ey, C, r=rB, label="B", fs=9.5)
        bond_line(ax, cx + rA * math.cos(a), cy + rA * math.sin(a),
                  ex - rB * math.cos(a), ey - rB * math.sin(a), C)
    panel_title(ax, cx, 0.92, "Trigonal planar", C); sub_label(ax, cx, 0.6, "3 pairs · 120°", C)

    # tetrahedral (wedge drawing)
    cx = 6.45
    atom(ax, cx, cy, C, r=rA, label="A", fs=10, zorder=7)
    b1 = (cx - 0.78, cy - 0.32); b2 = (cx + 0.78, cy - 0.32)
    b3 = (cx - 0.4, cy + 0.78); b4 = (cx + 0.62, cy + 0.66)
    atom(ax, *b1, C, r=rB, label="B", fs=9.5)
    atom(ax, *b2, C, r=rB, label="B", fs=9.5)
    atom(ax, *b3, C, r=rB, label="B", fs=9.5)
    bond_line(ax, cx - 0.26, cy - 0.08, b1[0] + 0.24, b1[1] + 0.1, C)
    bond_line(ax, cx + 0.26, cy - 0.08, b2[0] - 0.24, b2[1] + 0.1, C)
    dash_bond(ax, cx - 0.09, cy + 0.28, b3[0] + 0.18, b3[1] - 0.2, C)
    wedge(ax, cx + 0.1, cy + 0.05, b4[0] - 0.18, b4[1] - 0.16, C, w=0.22)
    atom(ax, *b4, C, r=rB, label="B", fs=9.5)
    panel_title(ax, cx, 0.92, "Tetrahedral", C); sub_label(ax, cx, 0.6, "4 pairs · 109.5°", C)

    # trigonal bipyramidal
    cx = 8.95
    atom(ax, cx, cy, C, r=rA, label="A", fs=10, zorder=7)
    bN = (cx, cy + 0.95); bS = (cx, cy - 0.95)
    bE = (cx + 0.8, cy); bW1 = (cx - 0.52, cy + 0.48); bW2 = (cx - 0.52, cy - 0.48)
    for b in (bN, bS, bE, bW1, bW2):
        atom(ax, *b, C, r=rB, label="B", fs=9.5)
    bond_line(ax, cx, cy + rA, bN[0], bN[1] - rB, C)
    bond_line(ax, cx, cy - rA, bS[0], bS[1] + rB, C)
    bond_line(ax, cx + rA, cy, bE[0] - rB, cy, C)
    bond_line(ax, cx - 0.26, cy + 0.14, bW1[0] + 0.2, bW1[1] - 0.18, C)
    bond_line(ax, cx - 0.26, cy - 0.14, bW2[0] + 0.2, bW2[1] + 0.18, C)
    panel_title(ax, cx, 0.92, "Trigonal bipyramidal", C); sub_label(ax, cx, 0.6, "5 pairs · 90° and 120°", C)

    # octahedral — 4 equatorial in a flattened X + 2 axial (wedge towards, dash away)
    cx = 11.45
    atom(ax, cx, cy, C, r=rA, label="A", fs=10, zorder=7)
    eq = [(cx + 0.68, cy + 0.26), (cx - 0.68, cy + 0.26), (cx - 0.68, cy - 0.26), (cx + 0.68, cy - 0.26)]
    bN = (cx, cy + 0.95); bS = (cx, cy - 0.95)
    for b in eq:
        atom(ax, *b, C, r=rB, label="B", fs=9.5)
    for b in eq:
        dxs = 1 if b[0] > cx else -1
        dys = 1 if b[1] > cy else -1
        bond_line(ax, cx + 0.26 * dxs, cy + 0.1 * dys, b[0] - 0.24 * dxs, b[1] - 0.1 * dys, C)
    wedge(ax, cx + 0.08, cy + 0.12, bN[0] + 0.12, bN[1] - rB, C, w=0.2)
    atom(ax, *bN, C, r=rB, label="B", fs=9.5)
    dash_bond(ax, cx - 0.06, cy - 0.26, bS[0], bS[1] + rB, C)
    atom(ax, *bS, C, r=rB, label="B", fs=9.5)
    panel_title(ax, cx, 0.92, "Octahedral", C); sub_label(ax, cx, 0.6, "6 pairs · 90°", C)

    sub_label(ax, 6.3, 0.16, "only bond pairs present — the shapes are regular · dashed bond points away, wedge points towards you", C)
    save(fig, "vsepr-shapes", C)


# ────────────────────────────────────────────────────────────────────
# 14) VSEPR — lone-pair compression CH₄ → NH₃ → H₂O
# ────────────────────────────────────────────────────────────────────
def vsepr_lone_pairs(C):
    fig = new_fig(11.4, 4.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 4.0); ax.axis("off")
    cy = 2.35

    # CH4
    cx = 1.9
    atom(ax, cx, cy, C, r=0.3, label="C", fs=11, zorder=7)
    b1 = (cx - 0.78, cy - 0.34); b2 = (cx + 0.78, cy - 0.34)
    b3 = (cx - 0.4, cy + 0.8); b4 = (cx + 0.64, cy + 0.68)
    atom(ax, *b1, C, r=0.24, label="H", fs=9)
    atom(ax, *b2, C, r=0.24, label="H", fs=9)
    atom(ax, *b3, C, r=0.24, label="H", fs=9)
    bond_line(ax, cx - 0.26, cy - 0.08, b1[0] + 0.2, b1[1] + 0.1, C)
    bond_line(ax, cx + 0.26, cy - 0.08, b2[0] - 0.2, b2[1] + 0.1, C)
    dash_bond(ax, cx - 0.09, cy + 0.28, b3[0] + 0.16, b3[1] - 0.2, C)
    wedge(ax, cx + 0.1, cy + 0.04, b4[0] - 0.16, b4[1] - 0.14, C, w=0.2)
    atom(ax, *b4, C, r=0.24, label="H", fs=9)
    angle_arc(ax, cx, cy, 0.48, 52, 128, C, "109.5°", lab_xy=(cx, cy + 1.28), fs=10)
    panel_title(ax, cx, 0.92, "CH₄ — 4 bond pairs, 0 lone pairs", C)
    sub_label(ax, cx, 0.6, "tetrahedral", C)

    # NH3
    cx = 5.7
    atom(ax, cx, cy, C, r=0.3, label="N", fs=11, zorder=7)
    b1 = (cx - 0.85, cy - 0.42); b2 = (cx + 0.85, cy - 0.42); b3 = (cx, cy - 1.0)
    atom(ax, *b1, C, r=0.24, label="H", fs=9)
    atom(ax, *b2, C, r=0.24, label="H", fs=9)
    atom(ax, *b3, C, r=0.24, label="H", fs=9)
    bond_line(ax, cx - 0.26, cy - 0.12, b1[0] + 0.2, b1[1] + 0.12, C)
    bond_line(ax, cx + 0.26, cy - 0.12, b2[0] - 0.2, b2[1] + 0.12, C)
    bond_line(ax, cx, cy - 0.3, b3[0], b3[1] + 0.24, C)
    lone_lobe(ax, cx, cy + 0.88, C, w=0.4, h=0.56, angle=0)
    angle_arc(ax, cx, cy, 0.46, 206, 334, C, "107°", lab_xy=(cx + 1.02, cy - 0.98), fs=10)
    panel_title(ax, cx, 0.92, "NH₃ — 3 bond pairs, 1 lone pair", C)
    sub_label(ax, cx, 0.6, "trigonal pyramidal — the lone pair squeezes 109.5° → 107°", C)

    # H2O
    cx = 9.5
    atom(ax, cx, cy, C, r=0.3, label="O", fs=11, zorder=7)
    b1 = (cx - 0.82, cy - 0.62); b2 = (cx + 0.82, cy - 0.62)
    atom(ax, *b1, C, r=0.24, label="H", fs=9)
    atom(ax, *b2, C, r=0.24, label="H", fs=9)
    bond_line(ax, cx - 0.26, cy - 0.14, b1[0] + 0.2, b1[1] + 0.14, C)
    bond_line(ax, cx + 0.26, cy - 0.14, b2[0] - 0.2, b2[1] + 0.14, C)
    lone_lobe(ax, cx - 0.42, cy + 0.72, C, w=0.36, h=0.52, angle=-16)
    lone_lobe(ax, cx + 0.42, cy + 0.72, C, w=0.36, h=0.52, angle=16)
    angle_arc(ax, cx, cy, 0.46, 213, 327, C, "104.5°", lab_xy=(cx, cy - 1.14), fs=10)
    panel_title(ax, cx, 0.92, "H₂O — 2 bond pairs, 2 lone pairs", C)
    sub_label(ax, cx, 0.6, "angular — two lone pairs squeeze the angle to 104.5°", C)

    sub_label(ax, 5.7, 0.16, "repulsion: lone pair–lone pair  >  lone pair–bond pair  >  bond pair–bond pair", C)
    save(fig, "vsepr-lone-pairs", C)


# ────────────────────────────────────────────────────────────────────
# 15) Bond length and bond angle defined on one molecule
# ────────────────────────────────────────────────────────────────────
def bond_angle_def(C):
    fig = new_fig(8.8, 3.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 8.8); ax.set_ylim(0, 3.5); ax.axis("off")

    cx, cy = 3.3, 1.95
    h1 = (cx + 1.15, cy + 0.62); h2 = (cx + 1.15, cy - 0.62)
    atom(ax, cx, cy, C, r=0.4, label="O", fs=12)
    atom(ax, *h1, C, r=0.3, label="H", fs=10)
    atom(ax, *h2, C, r=0.3, label="H", fs=10)
    bond_line(ax, cx + 0.32, cy + 0.2, h1[0] - 0.24, h1[1] - 0.13, C)
    bond_line(ax, cx + 0.32, cy - 0.2, h2[0] - 0.24, h2[1] + 0.13, C)
    angle_arc(ax, cx, cy, 0.58, -28.3, 28.3, C, "θ = 104.5°", lab_xy=(cx - 0.62, cy), fs=10.5)

    # bond length marker along the lower O–H bond, offset below it
    dx_, dy_ = h2[0] - cx, h2[1] - cy
    n = math.hypot(dx_, dy_)
    ux, uy = dx_ / n, dy_ / n
    px, py = -uy, ux  # perpendicular pointing up-left; we want below-right → negative
    ox, oy = 0.24 * (-px), 0.24 * (-py)
    ax.annotate("", xy=(cx + 0.4 * ux + ox, cy + 0.4 * uy + oy),
                xytext=(cx + 1.0 * ux + ox, cy + 1.0 * uy + oy),
                arrowprops=dict(arrowstyle="<|-|>", color=C["acc"], lw=1.4))
    ax.text(2.9, 0.72, "bond length, d", fontsize=9.5, color=C["acc"], ha="center")
    ax.text(6.9, 2.5, "bond length — the average distance between", fontsize=8.8, color=C["muted"], ha="center")
    ax.text(6.9, 2.26, "the centres of the nuclei of two bonded atoms", fontsize=8.8, color=C["muted"], ha="center")
    ax.text(6.9, 1.62, "bond angle — the average angle between two", fontsize=8.8, color=C["muted"], ha="center")
    ax.text(6.9, 1.38, "covalent bonds meeting at the central atom", fontsize=8.8, color=C["muted"], ha="center")
    save(fig, "bond-angle-def", C)


ALL = [
    sigma_bonds, pi_bond, dot_cross_molecules, dative_bonds, octet_exceptions,
    carbon_lattices, electron_density, bond_polarity, bonding_continuum,
    electronegativity_trends, molecular_polarity, liquid_jets, vsepr_shapes,
    vsepr_lone_pairs, bond_angle_def,
]

if __name__ == "__main__":
    for fn in ALL:
        fn(LIGHT)
        fn(DARK)
    print("done —", len(ALL), "figures x 2 themes")
