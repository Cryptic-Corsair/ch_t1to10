#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams for the IAL Chemistry site — Topic 5 (Alkenes).

Outputs light + dark variants for each diagram into public/diagrams/.
Style follows the site token contract: neutral canvas, coral accent #F5654A,
hairline strokes, DejaVu labels, transparent background.

Figures:
  sp2-hybridization      orbital boxes: 2s2 2p2 -> promote -> hybridize -> 3 sp2 + 1 p
  ethene-bonding         sigma framework + pi cloud of ethene
  isomerism-tree         structural vs stereoisomerism family tree
  structural-isomers     chain (pent-1-ene / 3-methylbut-1-ene) + positional (pent-1-ene / pent-2-ene)
  no-rotation            but-2-ene, rotation arrow crossed out
  cis-trans              cis-but-2-ene vs trans-but-2-ene
  ez-priority            Z-isomer and E-isomer with priority annotations
  ez-worked-example      E-1-chloro-2-methylbut-1-ene priority walkthrough
  reaction-map           five reactions of alkenes (radial map)
  mechanism-hbr-ethene   electrophilic addition of HBr to ethene (2 steps, curly arrows)
  mechanism-br2-ethene   electrophilic addition of Br2 to ethene (induced dipole)
  mechanism-hbr-propene  HBr + propene: major (2°) vs minor (1°) routes
  carbocation-stability  primary -> secondary -> tertiary
  polymerisation         n ethene -> poly(ethene) repeat unit
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

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


def axis_frame(ax):
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])


def panel_title(ax, x, y, text, C, fs=10.5, color=None, weight="medium"):
    ax.text(x, y, text, fontsize=fs, color=color or C["ink"], ha="center", va="center",
            fontweight=weight)


def sub_label(ax, x, y, text, C, fs=8.6, color=None):
    ax.text(x, y, text, fontsize=fs, color=color or C["muted"], ha="center", va="center")


def acc_label(ax, x, y, text, C, fs=9.0, ha="center", va="center", weight="medium"):
    ax.text(x, y, text, fontsize=fs, color=C["acc"], ha=ha, va=va, fontweight=weight)


def curly(ax, x1, y1, x2, y2, C, rad=0.28, lw=1.7, color=None, full=True):
    """Full-headed curly arrow (movement of an electron pair)."""
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>" if full else "-[|>",
                                 mutation_scale=12, lw=lw, color=color or C["acc"],
                                 connectionstyle=f"arc3,rad={rad}", zorder=9,
                                 shrinkA=2, shrinkB=2))


def straight_arrow(ax, x1, y1, x2, y2, C, color=None, lw=1.6, style="-|>", ms=13):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 lw=lw, color=color or C["ink"], zorder=8, shrinkA=0, shrinkB=0))


# ---- organic structure primitives ------------------------------------------
ATOM_FS = 10.6

def at(ax, x, y, text, C, fs=ATOM_FS, color=None, weight="normal", ha="center", va="center"):
    """Bare atom/group label (displayed-formula style)."""
    ax.text(x, y, text, fontsize=fs, color=color or C["ink"], ha=ha, va=va,
            fontweight=weight, zorder=7)


def bnd(ax, x1, y1, x2, y2, C, lw=1.5, color=None):
    ax.plot([x1, x2], [y1, y2], lw=lw, color=color or C["ink"], zorder=3,
            solid_capstyle="round")


def dbl(ax, x1, y1, x2, y2, C, lw=1.5, gap=0.075, color=None):
    """Double bond: two parallel lines offset perpendicular to the bond axis."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = -dy / L, dx / L
    for s in (-gap, gap):
        ax.plot([x1 + ux * s, x2 + ux * s], [y1 + uy * s, y2 + uy * s], lw=lw,
                color=color or C["ink"], zorder=3, solid_capstyle="round")


def chg(ax, x, y, symbol, C, fs=10, color=None):
    ax.text(x, y, symbol, fontsize=fs, color=color or C["acc"], ha="center", va="center",
            fontweight="bold", zorder=9)


def lone_pairs(ax, x, y, C, n=4, r=0.20, color=None, start=200):
    """Lone-pair dots around an ion."""
    for i in range(n):
        a = math.radians(start + i * (360 / max(n, 1)))
        px, py = x + r * math.cos(a), y + r * math.sin(a)
        ax.add_patch(Circle((px, py), 0.030, facecolor=color or C["ink"], edgecolor="none",
                            zorder=9))


def box_node(ax, x, y, w, h, text, C, fs=10, accent=False, radius=0.09):
    ec = C["acc"] if accent else C["grey_edge"]
    lw = 1.4 if accent else 1.1
    fc = C["acc_tint"] if accent else C["grey_tint"]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={radius}",
                                facecolor=fc, edgecolor=ec, lw=lw, zorder=4))
    ax.text(x, y, text, fontsize=fs, color=C["ink"], ha="center", va="center", zorder=6)


def conn(ax, x1, y1, x2, y2, C, color=None):
    ax.plot([x1, x2], [y1, y2], lw=1.1, color=color or C["hair"], zorder=1)


# ────────────────────────────────────────────────────────────────────
# 1) sp2 hybridization — orbital boxes
# ────────────────────────────────────────────────────────────────────
def orb_box(ax, x, y, C, label="", occ=1, w=0.46, h=0.62, accent=False, up=True):
    ec = C["acc"] if accent else C["ink"]
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, facecolor="none", edgecolor=ec,
                           lw=1.3, zorder=4))
    # occupancy arrows
    if occ >= 1:
        ay = y + 0.17 if up else y - 0.17
        ax.add_patch(FancyArrowPatch((x - 0.09, y - (0.17 if up else -0.17)) if False else (x, y - 0.17),
                                     (x, y + 0.17), arrowstyle="-|>", mutation_scale=8,
                                     lw=1.2, color=C["ink"], zorder=6, shrinkA=0, shrinkB=0))
    if occ >= 2:
        ax.add_patch(FancyArrowPatch((x + 0.09, y + 0.17), (x + 0.09, y - 0.17),
                                     arrowstyle="-|>", mutation_scale=8, lw=1.2,
                                     color=C["ink"], zorder=6, shrinkA=0, shrinkB=0))
    if label:
        ax.text(x, y - h / 2 - 0.24, label, fontsize=9, color=C["muted"], ha="center",
                va="top", zorder=6)


def sp2_hybridization(C):
    fig = new_fig(12.6, 3.3)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.6); ax.set_ylim(0, 3.3); ax.axis("off")
    cy = 1.85

    # group 1: ground state  2s(↑↓) 2p(↑)(↑)( )
    g1 = 2.1
    orb_box(ax, g1 - 0.95, cy, C, "2s", occ=2)
    orb_box(ax, g1 + 0.10, cy, C, "2p", occ=1)
    orb_box(ax, g1 + 0.75, cy, C, "2p", occ=1)
    orb_box(ax, g1 + 1.40, cy, C, "2p", occ=0)
    panel_title(ax, g1 + 0.25, cy + 0.95, "ground state:  2s²  2p²", C, fs=9.6)

    straight_arrow(ax, g1 + 2.15, cy, g1 + 2.75, cy, C, color=C["acc"], lw=1.6)
    acc_label(ax, g1 + 2.45, cy + 0.30, "promote", C, fs=8.6)

    # group 2: excited state  2s(↑) 2p(↑)(↑)(↑)
    g2 = 6.4
    orb_box(ax, g2 - 1.10, cy, C, "2s", occ=1)
    orb_box(ax, g2 - 0.05, cy, C, "2p", occ=1)
    orb_box(ax, g2 + 0.60, cy, C, "2p", occ=1)
    orb_box(ax, g2 + 1.25, cy, C, "2p", occ=1)
    panel_title(ax, g2 + 0.1, cy + 0.95, "excited state:  2s¹  2p³", C, fs=9.6)
    sub_label(ax, g2 + 0.1, cy - 1.05, "S          P    P    P", C, fs=8.8)

    straight_arrow(ax, g2 + 2.0, cy, g2 + 2.6, cy, C, color=C["acc"], lw=1.6)
    acc_label(ax, g2 + 2.3, cy + 0.30, "hybridize", C, fs=8.6)

    # group 3: three sp2 + one p
    g3 = 11.2
    for i in range(3):
        orb_box(ax, g3 - 1.25 + i * 0.62, cy, C, "", occ=1, accent=True)
    orb_box(ax, g3 + 0.95, cy, C, "", occ=1)
    panel_title(ax, g3 - 0.65, cy + 0.95, "hybridized carbon", C, fs=9.6)
    ax.plot([g3 - 1.55, g3 + 0.15], [cy - 0.55, cy - 0.55], lw=1.0, color=C["ink"], zorder=5)
    ax.plot([g3 - 1.55, g3 - 1.55], [cy - 0.55, cy - 0.42], lw=1.0, color=C["ink"], zorder=5)
    ax.plot([g3 + 0.15, g3 + 0.15], [cy - 0.55, cy - 0.42], lw=1.0, color=C["ink"], zorder=5)
    acc_label(ax, g3 - 0.70, cy - 0.86, "three sp² hybrid orbitals", C, fs=8.8)
    ax.plot([g3 + 0.62, g3 + 1.28], [cy - 0.55, cy - 0.55], lw=1.0, color=C["ink"], zorder=5)
    ax.plot([g3 + 0.62, g3 + 0.62], [cy - 0.55, cy - 0.42], lw=1.0, color=C["ink"], zorder=5)
    ax.plot([g3 + 1.28, g3 + 1.28], [cy - 0.55, cy - 0.42], lw=1.0, color=C["ink"], zorder=5)
    sub_label(ax, g3 + 0.95, cy - 0.86, "one p orbital", C, fs=8.8)

    save(fig, "sp2-hybridization", C)


# ────────────────────────────────────────────────────────────────────
# 2) Ethene bonding — sigma framework + pi cloud
# ────────────────────────────────────────────────────────────────────
def ethene_bonding(C):
    fig = new_fig(10.6, 4.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.6); ax.set_ylim(0, 4.5); ax.axis("off")
    cy = 2.15
    cx1, cx2 = 4.25, 6.35  # the two carbons

    # pi cloud above and below the C=C axis
    ax.add_patch(Ellipse(((cx1 + cx2) / 2 - 0.1, cy + 0.72), 2.5, 0.62, facecolor=C["acc_tint"],
                         edgecolor="none", zorder=2))
    ax.add_patch(Ellipse(((cx1 + cx2) / 2 - 0.1, cy - 0.72), 2.5, 0.62, facecolor=C["acc_tint"],
                         edgecolor="none", zorder=2))
    acc_label(ax, (cx1 + cx2) / 2 - 0.1, cy + 1.52, "π cloud", C, fs=9.2)
    acc_label(ax, (cx1 + cx2) / 2 - 0.1, cy - 1.55, "π cloud", C, fs=9.2)

    # unhybridized p orbitals (vertical lobes on each carbon)
    for cx in (cx1, cx2):
        ax.add_patch(Ellipse((cx, cy + 0.62), 0.42, 0.95, facecolor=C["grey_tint"],
                             edgecolor=C["grey_edge"], lw=1.0, zorder=3))
        ax.add_patch(Ellipse((cx, cy - 0.62), 0.42, 0.95, facecolor=C["grey_tint"],
                             edgecolor=C["grey_edge"], lw=1.0, zorder=3))
        ax.add_patch(Circle((cx, cy), 0.045, facecolor=C["ink"], zorder=7))
    sub_label(ax, cx2 + 0.02, cy + 1.75, "unhybridized 2p orbitals", C, fs=8.8)
    ax.plot([cx2 + 0.02, cx2 + 0.25], [cy + 1.55, cy + 1.12], lw=0.9, color=C["muted"], zorder=5)

    # C=C sigma overlap (head-on sp2–sp2)
    ax.add_patch(Ellipse(((cx1 + cx2) / 2, cy), 0.75, 0.34, facecolor=C["acc_tint2"],
                         edgecolor=C["acc"], lw=1.2, zorder=4))
    acc_label(ax, (cx1 + cx2) / 2, cy - 1.55, "σ bond (sp²–sp² head-on)", C, fs=9.2)

    # C–H sigma bonds and hydrogens
    hyd = [
        (cx1 - 1.15, cy + 0.80, "H"), (cx1 - 1.15, cy - 0.80, "H"),
        (cx2 + 1.15, cy + 0.80, "H"), (cx2 + 1.15, cy - 0.80, "H"),
    ]
    for hx, hy, lab in hyd:
        # head-on overlap ellipse along the bond
        mx, my = (cx1 + hx) / 2 if hx < cx1 else (cx2 + hx) / 2, (cy + hy) / 2
        ang = math.degrees(math.atan2(hy - cy, hx - (cx1 if hx < cx1 else cx2)))
        ax.add_patch(Ellipse((mx, my), 0.52, 0.24, angle=ang, facecolor=C["acc_tint"],
                             edgecolor="none", zorder=2))
        bnd(ax, cx1 if hx < cx1 else cx2, cy, hx, hy, C)
        at(ax, hx, hy, lab, C)
    at(ax, cx1, cy, "C", C, weight="bold")
    at(ax, cx2, cy, "C", C, weight="bold")
    bnd(ax, cx1 + 0.12, cy, cx2 - 0.12, cy, C)

    # 120° angle arc
    a_right = math.degrees(math.atan2(0.80, 1.15))
    ax.add_patch(Arc((cx2, cy), 1.5, 1.5, angle=0, theta1=-a_right, theta2=a_right,
                     color=C["acc"], lw=1.4, zorder=8))
    ax.text(cx2 + 1.02, cy + 0.02, "≈120°", fontsize=9, color=C["acc"], ha="left", va="center")

    panel_title(ax, 5.3, 4.15, "The C=C double bond: one σ bond + one π bond", C, fs=10.5)
    save(fig, "ethene-bonding", C)


# ────────────────────────────────────────────────────────────────────
# 3) Isomerism family tree
# ────────────────────────────────────────────────────────────────────
def isomerism_tree(C):
    fig = new_fig(11.6, 4.7)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.6); ax.set_ylim(0, 4.7); ax.axis("off")

    box_node(ax, 5.8, 4.05, 2.3, 0.62, "Isomerism", C, fs=10.5)
    box_node(ax, 2.95, 2.85, 2.6, 0.62, "Structural\nisomerism", C, fs=9.6)
    box_node(ax, 8.45, 2.85, 2.6, 0.62, "Stereoisomerism", C, fs=9.6)
    conn(ax, 5.8, 3.74, 5.8, 3.45, C); conn(ax, 2.95, 3.45, 8.45, 3.45, C)
    conn(ax, 2.95, 3.45, 2.95, 3.16, C); conn(ax, 8.45, 3.45, 8.45, 3.16, C)

    kids = [
        (1.40, "Functional group\nisomerism", False),
        (3.90, "Chain\nisomerism", False),
        (6.10, "Position\nisomerism", False),
        (8.45, "Geometric\nisomerism", True),
        (10.45, "Optical\nisomerism", False),
    ]
    for kx, label, hot in kids:
        box_node(ax, kx, 1.45, 1.9, 0.78, label, C, fs=8.8, accent=hot)
        parent_x = 2.95 if kx < 7 else 8.45
        conn(ax, parent_x, 2.54, parent_x, 2.25, C)
        conn(ax, kx, 2.25, parent_x if abs(kx - parent_x) > 0.1 else kx, 2.25, C)
        conn(ax, kx, 2.25, kx, 1.84, C)
    sub_label(ax, 8.45, 0.62, "alkenes exhibit this — spec 5.2 / 5.3", C, fs=8.6)
    acc_label(ax, 8.45, 0.92, "▲", C, fs=9)
    save(fig, "isomerism-tree", C)


# ────────────────────────────────────────────────────────────────────
# 4) Structural isomers of C5H10 — chain + positional
# ────────────────────────────────────────────────────────────────────
def zigzag(ax, x0, y0, n, step=0.78, updown=(1, -1), C=None):
    """Return vertices of a zigzag carbon chain and draw bonds between them."""
    pts = []
    for i in range(n):
        pts.append((x0 + i * step * 0.86, y0 + (updown[i % 2] * step * 0.42 if 0 < i < n - 1 or n > 1 else 0)))
    return pts


def structural_isomers(C):
    fig = new_fig(11.6, 4.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.6); ax.set_ylim(0, 4.6); ax.axis("off")

    dy_chain, dy_pos = 3.15, 1.30
    acc_label(ax, 1.30, dy_chain, "CHAIN\nISOMERISM", C, fs=8.8)
    acc_label(ax, 1.30, dy_pos, "POSITIONAL\nISOMERISM", C, fs=8.8)

    def draw_pent1(cx, cy):
        pts = [(cx, cy), (cx + 0.52, cy + 0.34), (cx + 1.04, cy), (cx + 1.56, cy + 0.34), (cx + 2.08, cy)]
        dbl(ax, *pts[0], *pts[1], C)
        for i in range(1, 4):
            bnd(ax, *pts[i], *pts[i + 1], C)
        at(ax, pts[0][0] - 0.02, pts[0][1] - 0.24, "H₂C", C, fs=9.2)
        at(ax, pts[1][0] + 0.02, pts[1][1] + 0.26, "CH", C, fs=9.2)
        for i in (2, 3):
            at(ax, pts[i][0], pts[i][1] - 0.26, "CH₂", C, fs=9.2)
        at(ax, pts[4][0] + 0.10, pts[4][1] + 0.26, "CH₃", C, fs=9.2)
        return pts

    def draw_3methyl(cx, cy):
        pts = [(cx, cy), (cx + 0.52, cy + 0.34), (cx + 1.04, cy), (cx + 1.56, cy + 0.34)]
        dbl(ax, *pts[0], *pts[1], C)
        for i in range(1, 3):
            bnd(ax, *pts[i], *pts[i + 1], C)
        at(ax, pts[0][0] - 0.02, pts[0][1] - 0.24, "H₂C", C, fs=9.2)
        at(ax, pts[1][0] + 0.02, pts[1][1] + 0.26, "CH", C, fs=9.2)
        at(ax, pts[2][0], pts[2][1] - 0.28, "CH", C, fs=9.2)
        at(ax, pts[3][0] + 0.10, pts[3][1] + 0.26, "CH₃", C, fs=9.2)
        bnd(ax, pts[2][0], pts[2][1], pts[2][0] + 0.30, pts[2][1] - 0.42, C)
        at(ax, pts[2][0] + 0.38, pts[2][1] - 0.58, "CH₃", C, fs=9.2)
        return pts

    def draw_pent2(cx, cy):
        pts = [(cx, cy), (cx + 0.52, cy + 0.34), (cx + 1.04, cy), (cx + 1.56, cy + 0.34), (cx + 2.08, cy)]
        for i in range(0, 4):
            if i == 1:
                dbl(ax, *pts[i], *pts[i + 1], C)
            else:
                bnd(ax, *pts[i], *pts[i + 1], C)
        at(ax, pts[0][0] - 0.04, pts[0][1] - 0.26, "H₃C", C, fs=9.2)
        at(ax, pts[1][0] + 0.02, pts[1][1] + 0.26, "CH", C, fs=9.2)
        at(ax, pts[2][0], pts[2][1] - 0.26, "CH", C, fs=9.2)
        at(ax, pts[3][0], pts[3][1] + 0.26, "CH₂", C, fs=9.2)
        at(ax, pts[4][0] + 0.12, pts[4][1] - 0.26, "CH₃", C, fs=9.2)
        return pts

    # chain panel: pent-1-ene vs 3-methylbut-1-ene
    draw_pent1(2.45, dy_chain)
    box_label = "Pent-1-ene"
    sub_label(ax, 3.55, dy_chain - 0.78, box_label, C, fs=9.0)
    at(ax, 5.15, dy_chain, "≠", C, fs=13, color=C["muted"])
    draw_3methyl(5.75, dy_chain)
    sub_label(ax, 7.35, dy_chain - 0.78, "3-methylbut-1-ene", C, fs=9.0)

    # positional panel: pent-1-ene vs pent-2-ene
    draw_pent1(2.45, dy_pos)
    sub_label(ax, 3.55, dy_pos - 0.78, "Pent-1-ene", C, fs=9.0)
    at(ax, 5.15, dy_pos, "≠", C, fs=13, color=C["muted"])
    draw_pent2(5.75, dy_pos)
    sub_label(ax, 7.35, dy_pos - 0.78, "Pent-2-ene", C, fs=9.0)

    # side notes
    sub_label(ax, 9.65, dy_chain + 0.15, "branching of the\ncarbon chain\n(C₅H₁₀)", C, fs=8.6)
    sub_label(ax, 9.65, dy_pos + 0.15, "the C=C moved\nto a different\nposition", C, fs=8.6)
    panel_title(ax, 5.8, 4.30, "Structural isomerism in alkenes", C, fs=10.5)
    save(fig, "structural-isomers", C)


# ────────────────────────────────────────────────────────────────────
# 5) Restricted rotation — but-2-ene, crossed rotation arrow
# ────────────────────────────────────────────────────────────────────
def draw_but2ene(ax, cx, cy, C, cis=False, fs=10.2):
    """But-2-ene around C=C centred at (cx, cy). cis=True puts CH3 groups on the same side."""
    lx, rx = cx - 0.62, cx + 0.62
    bnd(ax, lx, cy, rx, cy, C)
    dbl(ax, lx, cy, rx, cy, C)
    at(ax, cx, cy, "", C)
    if cis:
        l_top, l_bot, r_top, r_bot = "CH₃", "H", "CH₃", "H"
    else:
        l_top, l_bot, r_top, r_bot = "CH₃", "H", "H", "CH₃"
    at(ax, lx - 0.42, cy + 0.52, l_top, C, fs=fs)
    at(ax, lx - 0.42, cy - 0.52, l_bot, C, fs=fs)
    at(ax, rx + 0.42, cy + 0.52, r_top, C, fs=fs)
    at(ax, rx + 0.42, cy - 0.52, r_bot, C, fs=fs)
    bnd(ax, lx, cy, lx - 0.22, cy + 0.36, C)
    bnd(ax, lx, cy, lx - 0.22, cy - 0.36, C)
    bnd(ax, rx, cy, rx + 0.22, cy + 0.36, C)
    bnd(ax, rx, cy, rx + 0.22, cy - 0.36, C)
    return lx, rx


def no_rotation(C):
    fig = new_fig(7.0, 3.9)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 7.0); ax.set_ylim(0, 3.9); ax.axis("off")
    cx, cy = 3.5, 2.45
    lx, rx = draw_but2ene(ax, cx, cy, C, cis=False)

    # small circular rotation arrow looping around the C=C bond, crossed out
    ax.add_patch(Arc((cx, cy), 1.8, 1.0, angle=0, theta1=195, theta2=330,
                     color=C["acc"], lw=1.9, zorder=9))
    # arrowhead at the end of the arc (330 deg)
    ae = math.radians(330)
    ax.add_patch(FancyArrowPatch((cx + 0.90 * math.cos(ae) - 0.02, cy + 0.50 * math.sin(ae)),
                                 (cx + 0.90 * math.cos(ae), cy + 0.50 * math.sin(ae)),
                                 arrowstyle="-|>", mutation_scale=13, lw=1.9,
                                 color=C["acc"], zorder=9))
    # cross over the arc's lower part
    ax.plot([cx - 0.17, cx + 0.17], [cy - 0.62, cy - 0.30], lw=1.9, color=C["acc"], zorder=10)
    ax.plot([cx - 0.17, cx + 0.17], [cy - 0.30, cy - 0.62], lw=1.9, color=C["acc"], zorder=10)
    acc_label(ax, cx, cy - 1.30, "CANNOT ROTATE AROUND C=C", C, fs=9.6)
    sub_label(ax, cx, 0.55, "rotation would break the π bond", C, fs=9.0)
    save(fig, "no-rotation", C)


# ────────────────────────────────────────────────────────────────────
# 6) cis/trans but-2-ene
# ────────────────────────────────────────────────────────────────────
def cis_trans(C):
    fig = new_fig(10.4, 3.9)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.4); ax.set_ylim(0, 3.9); ax.axis("off")

    draw_but2ene(ax, 2.75, 2.30, C, cis=True)
    panel_title(ax, 2.75, 0.85, "cis-but-2-ene", C, fs=10.2)
    sub_label(ax, 2.75, 0.45, "methyl groups on the same side", C, fs=8.8)

    draw_but2ene(ax, 7.65, 2.30, C, cis=False)
    panel_title(ax, 7.65, 0.85, "trans-but-2-ene", C, fs=10.2)
    sub_label(ax, 7.65, 0.45, "methyl groups across the double bond", C, fs=8.8)

    panel_title(ax, 5.2, 3.55, "The cis–trans system for but-2-ene", C, fs=10.5)
    save(fig, "cis-trans", C)


# ────────────────────────────────────────────────────────────────────
# 7) E/Z priority diagram — C(Br)(F)=C(Cl)(H)
# ────────────────────────────────────────────────────────────────────
def draw_ef_cclh(ax, cx, cy, C, z=True, fs=10.4):
    """Left C: Br (35) and F (9); right C: Cl (17) and H (1). z=True: high priorities same side."""
    lx, rx = cx - 0.58, cx + 0.58
    bnd(ax, lx, cy, rx, cy, C)
    dbl(ax, lx, cy, rx, cy, C)
    at(ax, lx, cy, "", C); at(ax, rx, cy, "", C)
    if z:
        l_top, l_bot, r_top, r_bot = "Br", "F", "Cl", "H"
    else:
        l_top, l_bot, r_top, r_bot = "Br", "F", "H", "Cl"
    at(ax, lx - 0.40, cy + 0.50, l_top, C, fs=fs, weight="bold" if l_top in ("Br", "Cl") else "normal")
    at(ax, lx - 0.40, cy - 0.50, l_bot, C, fs=fs, weight="bold" if l_bot in ("Br", "Cl") else "normal")
    at(ax, rx + 0.40, cy + 0.50, r_top, C, fs=fs, weight="bold" if r_top in ("Br", "Cl") else "normal")
    at(ax, rx + 0.40, cy - 0.50, r_bot, C, fs=fs, weight="bold" if r_bot in ("Br", "Cl") else "normal")
    bnd(ax, lx, cy, lx - 0.20, cy + 0.34, C)
    bnd(ax, lx, cy, lx - 0.20, cy - 0.34, C)
    bnd(ax, rx, cy, rx + 0.20, cy + 0.34, C)
    bnd(ax, rx, cy, rx + 0.20, cy - 0.34, C)
    return lx, rx


def ez_priority(C):
    fig = new_fig(11.4, 4.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.4); ax.set_ylim(0, 4.5); ax.axis("off")

    # Z isomer
    lx, rx = draw_ef_cclh(ax, 3.1, 2.35, C, z=True)
    ax.plot([3.1, 3.1], [1.35, 3.45], lw=1.0, color=C["faint"], ls=(0, (4, 3)), zorder=1)
    acc_label(ax, 2.05, 3.62, "higher priority\non first C", C, fs=8.6)
    curly(ax, 2.42, 3.42, 2.62, 3.02, C, rad=-0.25, lw=1.4)
    acc_label(ax, 4.45, 3.62, "higher priority\non second C", C, fs=8.6)
    curly(ax, 3.98, 3.42, 3.72, 3.02, C, rad=0.25, lw=1.4)
    box_node(ax, 1.30, 2.35, 1.35, 0.52, "Z-isomer", C, fs=9.4, accent=True)
    sub_label(ax, 3.1, 0.72, "zusammen — both high-priority groups above", C, fs=8.8)

    # E isomer
    lx, rx = draw_ef_cclh(ax, 8.3, 2.35, C, z=False)
    ax.plot([8.3, 8.3], [1.35, 3.45], lw=1.0, color=C["faint"], ls=(0, (4, 3)), zorder=1)
    acc_label(ax, 7.25, 3.62, "higher priority\non first C", C, fs=8.6)
    curly(ax, 7.62, 3.42, 7.82, 3.02, C, rad=-0.25, lw=1.4)
    acc_label(ax, 9.72, 1.02, "higher priority\non second C", C, fs=8.6)
    curly(ax, 9.42, 1.30, 8.86, 1.92, C, rad=-0.25, lw=1.4)
    box_node(ax, 6.50, 2.35, 1.35, 0.52, "E-isomer", C, fs=9.4, accent=True)
    sub_label(ax, 8.3, 0.72, "entgegen — high-priority groups on opposite sides", C, fs=8.8)

    panel_title(ax, 5.7, 4.22, "The E–Z system ranks substituents by atomic number", C, fs=10.5)
    save(fig, "ez-priority", C)


# ────────────────────────────────────────────────────────────────────
# 8) E/Z worked example — E-1-chloro-2-methylbut-1-ene
# ────────────────────────────────────────────────────────────────────
def ez_worked_example(C):
    fig = new_fig(11.0, 4.4)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.0); ax.set_ylim(0, 4.4); ax.axis("off")

    cx, cy = 3.4, 2.55
    lx, rx = cx - 0.58, cx + 0.58
    bnd(ax, lx, cy, rx, cy, C)
    dbl(ax, lx, cy, rx, cy, C)
    # left C: CH3 above, C2H5 below
    bnd(ax, lx, cy, lx - 0.24, cy + 0.40, C)
    at(ax, lx - 0.78, cy + 0.56, "CH₃", C, fs=10.6)
    bnd(ax, lx, cy, lx - 0.24, cy - 0.40, C)
    at(ax, lx - 0.80, cy - 0.58, "C₂H₅", C, fs=10.6)
    # right C: Cl above, H below
    bnd(ax, rx, cy, rx + 0.24, cy + 0.40, C)
    at(ax, rx + 0.62, cy + 0.56, "Cl", C, fs=10.6, weight="bold")
    bnd(ax, rx, cy, rx + 0.24, cy - 0.40, C)
    at(ax, rx + 0.58, cy - 0.58, "H", C, fs=10.6)

    # red ellipse highlighting the right-hand carbon's substituents
    ax.add_patch(Ellipse((rx + 0.42, cy), 1.5, 2.3, facecolor="none",
                         edgecolor=C["acc"], lw=1.5, zorder=8))

    # priority tags
    box_node(ax, rx + 1.55, cy + 0.94, 0.72, 0.44, "17", C, fs=9.6, accent=True)
    curly(ax, rx + 1.20, cy + 0.86, rx + 0.92, cy + 0.68, C, rad=0.2, lw=1.3)
    box_node(ax, rx + 1.55, cy - 0.94, 0.72, 0.44, "1", C, fs=9.6)
    curly(ax, rx + 1.20, cy - 0.86, rx + 0.88, cy - 0.68, C, rad=-0.2, lw=1.3)

    # annotations
    sub_label(ax, 8.05, cy + 0.94, "right-hand C:\nCl has the higher priority", C, fs=8.8)
    sub_label(ax, 8.05, cy - 0.55, "left-hand C: two carbons attached —\nsame priority, so look one shell out", C, fs=8.8)
    sub_label(ax, 8.05, cy - 1.42, "CH₃ → H, H, H\nC₂H₅ → C, H, H\nso C₂H₅ wins (it carries a C)", C, fs=8.8)

    # verdict
    box_node(ax, 3.4, 0.72, 5.9, 0.62, "high-priority groups on opposite sides  →  E-1-chloro-2-methylbut-1-ene", C,
             fs=9.6, accent=True)
    save(fig, "ez-worked-example", C)


# ────────────────────────────────────────────────────────────────────
# 9) Reactions of alkenes — radial map
# ────────────────────────────────────────────────────────────────────
def reaction_map(C):
    fig = new_fig(10.6, 5.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.6); ax.set_ylim(0, 5.0); ax.axis("off")
    cx, cy = 5.3, 2.5

    ax.add_patch(Ellipse((cx, cy), 2.5, 1.15, facecolor=C["acc_tint"], edgecolor=C["acc"],
                         lw=1.5, zorder=4))
    ax.text(cx, cy, "Reactions\nof Alkenes", fontsize=10.4, color=C["ink"], ha="center",
            va="center", fontweight="medium", zorder=6)

    sats = [
        (5.3, 4.25, "1. Hydrogenation"),
        (8.35, 3.35, "2. Halogenation"),
        (7.45, 1.10, "3. Hydration"),
        (3.15, 1.10, "4. Addition of\nHydrogen Halides"),
        (2.25, 3.35, "5. Oxidation by\npotassium\nmanganate(VII)"),
    ]
    for sx, sy, label in sats:
        ax.add_patch(Ellipse((sx, sy), 2.35, 1.05, facecolor=C["grey_tint"],
                             edgecolor=C["grey_edge"], lw=1.1, zorder=4))
        ax.text(sx, sy, label, fontsize=8.8, color=C["ink"], ha="center", va="center", zorder=6)
        # arrow from centre towards satellite
        dx, dy = sx - cx, sy - cy
        L = math.hypot(dx, dy)
        sx1, sy1 = cx + dx / L * 1.35, cy + dy / L * 0.62
        ax.add_patch(FancyArrowPatch((sx1, sy1), (sx - dx / L * 1.28, sy - dy / L * 0.57),
                                     arrowstyle="-|>", mutation_scale=13, lw=1.7,
                                     color=C["ink"], zorder=5))
    save(fig, "reaction-map", C)


# ────────────────────────────────────────────────────────────────────
# 10) Mechanism — electrophilic addition of HBr to ethene
# ────────────────────────────────────────────────────────────────────
def h_bonds(ax, cx, cy, offs, C, lab="H", fs=9.8, stub=0.5):
    for dx, dy in offs:
        bnd(ax, cx, cy, cx + dx * stub, cy + dy * stub, C)
        at(ax, cx + dx, cy + dy, lab, C, fs=fs)


def mechanism_hbr_ethene(C):
    fig = new_fig(12.2, 4.7)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.2); ax.set_ylim(0, 4.7); ax.axis("off")

    # ---- stage 1: approach
    c1, c2, cy = 1.55, 2.55, 1.95
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    dbl(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    h_bonds(ax, c1, cy, [(-0.62, 0.55), (-0.62, -0.55)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    # HBr approaching
    hx, bx, hy = 4.05, 4.95, 3.55
    bnd(ax, hx + 0.10, hy, bx - 0.22, hy, C)
    at(ax, hx, hy, "H", C); at(ax, bx, hy, "Br", C)
    at(ax, hx - 0.14, hy + 0.34, "δ+", C, fs=9.4, color=C["acc"])
    at(ax, bx + 0.30, hy + 0.34, "δ−", C, fs=9.4, color=C["acc"])
    # curly arrows: pi pair -> H ; H-Br pair -> Br
    curly(ax, 2.05, 2.16, 3.72, 3.32, C, rad=-0.30)
    curly(ax, 4.45, 3.42, 4.82, 3.62, C, rad=0.45)
    sub_label(ax, 2.2, 0.62, "the π pair bonds to the δ+ H\n(ethene acts as a nucleophile)", C, fs=8.6)

    straight_arrow(ax, 5.55, 2.2, 6.15, 2.2, C, lw=1.7, ms=15)

    # ---- stage 2: carbocation + bromide
    c1, c2, cy = 6.85, 7.85, 1.95
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    h_bonds(ax, c1, cy, [(-0.62, 0.55), (-0.62, -0.55), (0.0, -0.85)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    chg(ax, c2 + 0.22, cy + 0.38, "+", C, fs=12)
    # bromide ion with lone pairs
    brx, bry = 7.85, 0.78
    at(ax, brx, bry, "Br", C, weight="bold")
    lone_pairs(ax, brx - 0.02, bry, C, n=4, r=0.26)
    at(ax, brx + 0.34, bry + 0.28, "−", C, fs=10)
    curly(ax, 7.62, 1.02, 7.80, 1.68, C, rad=0.25)
    sub_label(ax, 7.35, 3.55, "carbocation intermediate\n+ Br⁻ (heterolytic fission)", C, fs=8.6)

    straight_arrow(ax, 9.0, 2.2, 9.6, 2.2, C, lw=1.7, ms=15)

    # ---- stage 3: product
    c1, c2, cy = 10.3, 11.3, 1.95
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    h_bonds(ax, c1, cy, [(-0.62, 0.55), (-0.62, -0.55), (0.0, -0.85)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.0, -0.85)], C)
    bnd(ax, c2 + 0.12, cy, c2 + 0.52, cy, C)
    at(ax, c2 + 0.80, cy, "Br", C)
    sub_label(ax, 10.75, 3.55, "bromoethane —\nHBr added across\nthe double bond", C, fs=8.6)

    panel_title(ax, 2.05, 4.35, "Step 1 — electrophilic attack", C, fs=9.6)
    panel_title(ax, 7.35, 4.35, "Step 2 — nucleophilic attack", C, fs=9.6)
    save(fig, "mechanism-hbr-ethene", C)


# ────────────────────────────────────────────────────────────────────
# 11) Mechanism — electrophilic addition of Br2 to ethene
# ────────────────────────────────────────────────────────────────────
def mechanism_br2_ethene(C):
    fig = new_fig(12.2, 4.7)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.2); ax.set_ylim(0, 4.7); ax.axis("off")

    # ---- stage 1: induced dipole
    c1, c2, cy = 1.55, 2.55, 1.80
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    dbl(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    h_bonds(ax, c1, cy, [(-0.62, 0.55), (-0.62, -0.55)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    # Br-Br
    b1x, b2x, by = 4.15, 5.05, 3.60
    bnd(ax, b1x + 0.28, by, b2x - 0.28, by, C)
    at(ax, b1x, by, "Br", C); at(ax, b2x, by, "Br", C)
    at(ax, b1x - 0.10, by + 0.34, "δ+", C, fs=9.4, color=C["acc"])
    at(ax, b2x + 0.34, by + 0.34, "δ−", C, fs=9.4, color=C["acc"])
    sub_label(ax, 4.6, 4.30, "induced dipole", C, fs=8.6)
    # curly arrows: pi pair -> nearer Br ; Br-Br pair -> far Br
    curly(ax, 2.05, 2.01, 3.72, 3.38, C, rad=-0.30)
    curly(ax, 4.55, 3.74, 4.92, 3.78, C, rad=0.45)
    sub_label(ax, 2.2, 0.55, "the π electrons repel the Br–Br pair,\ninducing a dipole — Brδ+ is attacked", C, fs=8.6)

    straight_arrow(ax, 5.55, 1.05, 6.15, 1.05, C, lw=1.7, ms=15)

    # ---- stage 2: carbocation with Br already attached
    c1, c2, cy = 6.85, 7.85, 2.30
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    bnd(ax, c1 - 0.12, cy, c1 - 0.62, cy, C)
    at(ax, c1 - 0.90, cy, "Br", C)
    h_bonds(ax, c1, cy, [(-0.45, 0.62), (-0.45, -0.62)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    chg(ax, c2 + 0.22, cy + 0.38, "+", C, fs=12)
    # bromide ion attacks C+
    brx, bry = 7.85, 0.85
    at(ax, brx, bry, "Br", C, weight="bold")
    lone_pairs(ax, brx - 0.02, bry, C, n=4, r=0.26)
    at(ax, brx + 0.34, bry + 0.28, "−", C, fs=10)
    curly(ax, 7.62, 1.10, 7.80, 2.02, C, rad=0.25)
    sub_label(ax, 7.35, 4.05, "carbocation intermediate + Br⁻", C, fs=8.6)

    straight_arrow(ax, 9.0, 1.05, 9.6, 1.05, C, lw=1.7, ms=15)

    # ---- stage 3: product
    c1, c2, cy = 10.3, 11.3, 2.30
    bnd(ax, c1 + 0.12, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
    bnd(ax, c1 - 0.12, cy, c1 - 0.62, cy, C)
    at(ax, c1 - 0.90, cy, "Br", C)
    h_bonds(ax, c1, cy, [(-0.45, 0.62), (-0.45, -0.62)], C)
    h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    bnd(ax, c2 + 0.12, cy, c2 + 0.52, cy, C)
    at(ax, c2 + 0.80, cy, "Br", C)
    sub_label(ax, 10.8, 4.05, "1,2-dibromoethane —\ntwo Br atoms added\nacross the double bond", C, fs=8.6)

    save(fig, "mechanism-br2-ethene", C)


# ────────────────────────────────────────────────────────────────────
# 12) Mechanism — HBr + propene: major (2°) vs minor (1°)
# ────────────────────────────────────────────────────────────────────
def mechanism_hbr_propene(C):
    fig = new_fig(12.8, 5.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.8); ax.set_ylim(0, 5.6); ax.axis("off")

    # ---- reactants (left centre)
    c1, c2, c3, cy = 1.30, 2.15, 3.00, 2.85
    bnd(ax, c1 + 0.30, cy, c2 - 0.12, cy, C)
    at(ax, c1, cy, "CH₃", C, fs=10.2)
    at(ax, c2, cy, "C", C)
    bnd(ax, c2 + 0.12, cy, c3 - 0.12, cy, C)
    dbl(ax, c2 + 0.12, cy, c3 - 0.12, cy, C)
    at(ax, c3, cy, "C", C)
    bnd(ax, c2, cy, c2 - 0.02, cy + 0.55, C)
    at(ax, c2 - 0.02, cy + 0.78, "H", C, fs=9.8)
    h_bonds(ax, c3, cy, [(0.62, 0.55), (0.62, -0.55)], C)
    # HBr above
    hx, bx, hy = 2.75, 3.65, 4.65
    bnd(ax, hx + 0.10, hy, bx - 0.22, hy, C)
    at(ax, hx, hy, "H", C); at(ax, bx, hy, "Br", C)
    at(ax, hx - 0.14, hy + 0.32, "δ+", C, fs=9.2, color=C["acc"])
    at(ax, bx + 0.30, hy + 0.32, "δ−", C, fs=9.2, color=C["acc"])
    curly(ax, 2.55, 3.06, 2.62, 4.42, C, rad=-0.25)
    curly(ax, 3.15, 4.52, 3.52, 4.72, C, rad=0.45)

    # branch arrows A / B
    straight_arrow(ax, 3.85, 2.95, 5.05, 3.75, C, lw=1.6)
    straight_arrow(ax, 3.85, 2.70, 5.05, 1.95, C, lw=1.6)
    box_node(ax, 4.45, 3.58, 0.44, 0.40, "A", C, fs=9.4, accent=True)
    box_node(ax, 4.45, 2.10, 0.44, 0.40, "B", C, fs=9.4)

    # ---- route A: secondary carbocation -> 2-bromopropane (major)
    ay = 3.95
    a1, a2, a3 = 5.85, 6.75, 7.65
    bnd(ax, a1 + 0.32, ay, a2 - 0.12, ay, C)
    at(ax, a1, ay, "CH₃", C, fs=10.2)
    at(ax, a2, ay, "C", C)
    bnd(ax, a2 + 0.12, ay, a3 - 0.34, ay, C)
    at(ax, a3 - 0.02, ay, "CH₃", C, fs=10.2)
    bnd(ax, a2, ay, a2, ay + 0.50, C)
    at(ax, a2, ay + 0.72, "H", C, fs=9.8)
    chg(ax, a2 + 0.20, ay + 0.26, "+", C, fs=11)
    sub_label(ax, 6.75, ay - 0.72, "secondary carbocation (2°)", C, fs=8.6)
    brx, bry = 6.75, 2.85
    at(ax, brx, bry, "Br", C, weight="bold")
    lone_pairs(ax, brx - 0.02, bry, C, n=4, r=0.24)
    at(ax, brx + 0.32, bry + 0.26, "−", C, fs=9.6)
    curly(ax, 6.60, 3.08, 6.72, 3.66, C, rad=0.22)
    straight_arrow(ax, 8.35, ay, 8.95, ay, C, lw=1.6)
    # product A
    p1, p2, p3 = 9.65, 10.55, 11.45
    bnd(ax, p1 + 0.32, ay, p2 - 0.12, ay, C)
    at(ax, p1, ay, "CH₃", C, fs=10.2)
    at(ax, p2, ay, "C", C)
    bnd(ax, p2 + 0.12, ay, p3 - 0.34, ay, C)
    at(ax, p3 - 0.02, ay, "CH₃", C, fs=10.2)
    bnd(ax, p2, ay - 0.06, p2, ay - 0.55, C)
    at(ax, p2, ay - 0.80, "Br", C)
    h_bonds(ax, p2, ay, [(0.0, 0.62)], C)
    box_node(ax, 10.55, 2.55, 1.9, 0.5, "Major product", C, fs=9.4, accent=True)

    # ---- route B: primary carbocation -> 1-bromopropane (minor)
    by_ = 1.60
    b1, b2, b3 = 5.85, 6.75, 7.65
    bnd(ax, b1 + 0.32, by_, b2 - 0.34, by_, C)
    at(ax, b1, by_, "CH₃", C, fs=10.2)
    at(ax, b2 - 0.02, by_, "CH₂", C, fs=10.2)
    bnd(ax, b2 + 0.34, by_, b3 - 0.34, by_, C)
    at(ax, b3 - 0.02, by_, "CH₂", C, fs=10.2)
    chg(ax, b3 + 0.34, by_ + 0.26, "+", C, fs=11)
    sub_label(ax, 6.75, by_ - 0.55, "primary carbocation (1°)", C, fs=8.6)
    brx2, bry2 = 7.65, 0.70
    at(ax, brx2, bry2, "Br", C, weight="bold")
    lone_pairs(ax, brx2 - 0.02, bry2, C, n=4, r=0.24)
    at(ax, brx2 + 0.32, bry2 + 0.26, "−", C, fs=9.6)
    curly(ax, 7.55, 0.94, 7.66, 1.30, C, rad=0.2)
    straight_arrow(ax, 8.35, by_, 8.95, by_, C, lw=1.6)
    # product B
    q1, q2, q3 = 9.65, 10.55, 11.45
    bnd(ax, q1 + 0.32, by_, q2 - 0.34, by_, C)
    at(ax, q1, by_, "CH₃", C, fs=10.2)
    at(ax, q2 - 0.02, by_, "CH₂", C, fs=10.2)
    bnd(ax, q2 + 0.34, by_, q3 - 0.34, by_, C)
    at(ax, q3 - 0.02, by_, "CH₂", C, fs=10.2)
    bnd(ax, q3 + 0.30, by_, q3 + 0.62, by_, C)
    at(ax, q3 + 0.94, by_, "Br", C, fs=10.2)
    box_node(ax, 10.55, 0.55, 1.9, 0.5, "Minor product", C, fs=9.4)

    panel_title(ax, 6.4, 5.30, "HBr + propene — two routes, two products", C, fs=10.5)
    save(fig, "mechanism-hbr-propene", C)


# ────────────────────────────────────────────────────────────────────
# 13) Carbocation stability
# ────────────────────────────────────────────────────────────────────
def carbocation_stability(C):
    fig = new_fig(10.6, 3.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.6); ax.set_ylim(0, 3.6); ax.axis("off")

    straight_arrow(ax, 1.5, 3.05, 9.1, 3.05, C, lw=1.7, ms=15)
    panel_title(ax, 5.3, 3.30, "Stability increases", C, fs=10.2)

    def carbocation(cx, cy, top, bottom, left):
        bnd(ax, cx - 0.12, cy, cx - 0.55, cy, C)
        at(ax, cx - 0.80, cy, left, C, fs=10.4)
        if top:
            bnd(ax, cx, cy + 0.06, cx, cy + 0.48, C)
            at(ax, cx, cy + 0.72, top, C, fs=10.4)
        if bottom:
            bnd(ax, cx, cy - 0.06, cx, cy - 0.48, C)
            at(ax, cx, cy - 0.72, bottom, C, fs=10.4)
        chg(ax, cx + 0.24, cy + 0.30, "+", C, fs=12)

    carbocation(2.2, 1.85, "H", "H", "R")
    sub_label(ax, 2.2, 0.62, "primary (1°)", C, fs=9.6)
    carbocation(5.3, 1.85, "H", "R", "R")
    sub_label(ax, 5.3, 0.62, "secondary (2°)", C, fs=9.6)
    carbocation(8.4, 1.85, "R", "R", "R")
    sub_label(ax, 8.4, 0.62, "tertiary (3°)", C, fs=9.6)
    save(fig, "carbocation-stability", C)


# ────────────────────────────────────────────────────────────────────
# 14) Addition polymerisation — ethene -> poly(ethene)
# ────────────────────────────────────────────────────────────────────
def polymerisation(C):
    fig = new_fig(10.8, 4.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.8); ax.set_ylim(0, 4.0); ax.axis("off")

    def ethene_unit(ax, c1, c2, cy, C, bond="double", stub=0.12):
        if bond == "double":
            dbl(ax, c1 + stub, cy, c2 - stub, cy, C)
        else:
            bnd(ax, c1 + stub, cy, c2 - stub, cy, C)
        at(ax, c1, cy, "C", C); at(ax, c2, cy, "C", C)
        h_bonds(ax, c1, cy, [(-0.62, 0.55), (-0.62, -0.55)], C)
        h_bonds(ax, c2, cy, [(0.62, 0.55), (0.62, -0.55)], C)

    cy = 2.45
    acc_label(ax, 1.30, cy, "n", C, fs=13)
    ethene_unit(ax, 3.0, 3.9, cy, C, bond="double")

    straight_arrow(ax, 4.95, cy, 5.85, cy, C, lw=1.8, ms=16)
    sub_label(ax, 5.4, cy + 0.42, "addition\npolymerisation", C, fs=8.4)

    # repeat unit in brackets
    ax.text(6.55, cy, "(", fontsize=52, color=C["ink"], ha="center", va="center", zorder=5)
    ax.text(9.45, cy, ")", fontsize=52, color=C["ink"], ha="center", va="center", zorder=5)
    acc_label(ax, 9.72, cy - 0.52, "n", C, fs=11)
    ethene_unit(ax, 7.55, 8.45, cy, C, bond="single")
    # bonds continuing through the brackets
    ax.plot([6.85, 7.43], [cy, cy], lw=1.5, color=C["ink"], zorder=3, solid_capstyle="round")
    ax.plot([8.57, 9.15], [cy, cy], lw=1.5, color=C["ink"], zorder=3, solid_capstyle="round")

    panel_title(ax, 3.45, 1.02, "ethene — MONOMER", C, fs=9.8)
    panel_title(ax, 8.0, 1.02, "poly(ethene) — POLYMER", C, fs=9.8)
    save(fig, "polymerisation", C)


if __name__ == "__main__":
    for theme in (LIGHT, DARK):
        sp2_hybridization(theme)
        ethene_bonding(theme)
        isomerism_tree(theme)
        structural_isomers(theme)
        no_rotation(theme)
        cis_trans(theme)
        ez_priority(theme)
        ez_worked_example(theme)
        reaction_map(theme)
        mechanism_hbr_ethene(theme)
        mechanism_br2_ethene(theme)
        mechanism_hbr_propene(theme)
        carbocation_stability(theme)
        polymerisation(theme)
    print("done (all 14)")
