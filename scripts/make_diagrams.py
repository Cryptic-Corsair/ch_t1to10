#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams for the IAL Chemistry site — Topic 1.

Outputs light + dark variants for each diagram into public/diagrams/.
Style follows the site token contract: neutral canvas, coral accent #F5654A,
hairline strokes, mono-ish labels (DejaVu Sans), transparent background.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon

OUT = "/home/z/my-project/public/diagrams"
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "none"

ACCENT = "#F5654A"

LIGHT = {
    "ink": "#1d1d1b",
    "muted": "#5f6268",
    "faint": "#9a9da3",
    "hair": "#c9c7c2",       # hairline stroke
    "hair_soft": "#dedcd7",
    "fill": "#ffffff",
    "acc": ACCENT,
    "acc_tint": (245/255, 101/255, 74/255, 0.10),
    "neutron": "#8d9096",
}
DARK = {
    "ink": "#f0efee",
    "muted": "#a3a6ad",
    "faint": "#71747a",
    "hair": "#4c4c50",       # hairline stroke on dark
    "hair_soft": "#3a3a3e",
    "fill": "#161616",
    "acc": ACCENT,
    "acc_tint": (245/255, 101/255, 74/255, 0.16),
    "neutron": "#7c7f85",
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


def ring(ax, x, y, r, C, lw=1.0):
    ax.add_patch(Circle((x, y), r, fill=False, edgecolor=C["hair"], lw=lw, linestyle=(0, (4, 3))))


def e_dot(ax, x, y, r, C):
    ax.add_patch(Circle((x, y), r, facecolor=C["ink"], edgecolor="none", zorder=6))


def shell_electrons(ax, cx, cy, r, n, C, dot_r=0.030, phase=0.0):
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        e_dot(ax, cx + r * math.cos(a), cy + r * math.sin(a), dot_r, C)


def nucleus(ax, cx, cy, C, protons=4, neutrons=3, r0=0.11, spread=0.075):
    """Small cluster of proton/neutron circles at the centre."""
    pts = []
    n = protons + neutrons
    for i in range(n):
        a = 2 * math.pi * i / n + 0.35
        rr = 0 if i == 0 else spread * (1.25 if i % 2 == 0 else 0.75)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a), i % 2 == 0))
    for (x, y, is_p) in pts:
        col = C["acc"] if is_p else C["neutron"]
        ax.add_patch(Circle((x, y), r0, facecolor=col, edgecolor=C["fill"], lw=0.8, zorder=5))


# ────────────────────────────────────────────────────────────────────
# 1) Atom structure
# ────────────────────────────────────────────────────────────────────
def atom_structure(C):
    fig = new_fig(9.4, 5.4)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")

    cx, cy = 3.6, 2.85
    ring(ax, cx, cy, 0.95, C); ring(ax, cx, cy, 1.65, C)
    nucleus(ax, cx, cy, C)
    # electrons: 2 inner, 4 outer
    shell_electrons(ax, cx, cy, 0.95, 2, C, dot_r=0.045, phase=math.pi / 2)
    shell_electrons(ax, cx, cy, 1.65, 4, C, dot_r=0.045, phase=math.pi / 4)

    # nucleus label — top left, leader drops down to the centre
    ax.text(0.55, 5.18, "Nucleus — protons and neutrons\n(together known as nucleons)",
            fontsize=10.5, color=C["ink"], ha="left", va="center", linespacing=1.45)
    ax.annotate("", xy=(cx - 0.06, cy + 0.14), xytext=(2.35, 4.92),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=1.0,
                                connectionstyle="arc3,rad=-0.12"))

    # electron label — top right
    ax.text(5.75, 4.45, "Electron", fontsize=10.5, color=C["ink"], ha="left", va="center")
    ax.annotate("", xy=(cx + 1.65 * math.cos(math.pi / 4) + 0.05,
                         cy + 1.65 * math.sin(math.pi / 4) + 0.05),
                xytext=(5.65, 4.38),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=1.0))

    # shell label — bottom right
    ax.text(5.75, 1.05, "Shell — a definite energy level\nin which electrons orbit",
            fontsize=10.5, color=C["ink"], ha="left", va="center", linespacing=1.45)
    ax.annotate("", xy=(cx, cy - 1.65), xytext=(5.65, 1.05),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=1.0))

    # legend chips — horizontal row, bottom left
    lx, ly = 0.75, 0.42
    items = [(C["acc"], "proton"), (C["neutron"], "neutron"), (C["ink"], "electron")]
    for i, (col, lab) in enumerate(items):
        x = lx + i * 1.85
        ax.add_patch(Circle((x, ly), 0.085, facecolor=col, edgecolor="none"))
        ax.text(x + 0.24, ly, lab, fontsize=10, color=C["muted"], va="center")
    save(fig, "atom-structure", C)


# ────────────────────────────────────────────────────────────────────
# 2) Nuclide notation
# ────────────────────────────────────────────────────────────────────
def nuclide_notation(C):
    fig = new_fig(9.4, 3.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 3.6); ax.axis("off")

    ax.text(2.15, 1.8, r"$^{A}_{Z}\ \mathrm{X}$", fontsize=64, color=C["ink"],
            ha="center", va="center")

    ax.annotate("Mass number A\nsum of protons and neutrons\nin the nucleus of an atom",
                xy=(1.72, 2.42), xytext=(4.6, 2.82),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=1.0),
                fontsize=10.5, color=C["ink"], ha="left", va="center", linespacing=1.5)
    ax.annotate("Atomic number Z\nprotons in the nucleus\nof an atom",
                xy=(1.72, 1.18), xytext=(4.6, 0.86),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=1.0),
                fontsize=10.5, color=C["ink"], ha="left", va="center", linespacing=1.5)

    ax.text(8.15, 1.8, "the symbol of\nthe element", fontsize=10, color=C["muted"],
            ha="center", va="center", linespacing=1.5)
    ax.annotate("", xy=(3.15, 1.8), xytext=(7.05, 1.8),
                arrowprops=dict(arrowstyle="<->", color=C["hair"], lw=1.0))
    save(fig, "nuclide-notation", C)


# ────────────────────────────────────────────────────────────────────
# 3) Ion formation
# ────────────────────────────────────────────────────────────────────
def draw_ion(ax, cx, cy, shells, C, scale=1.0):
    """shells = list of electron counts, inner first."""
    r_step = 0.34 * scale
    for si, count in enumerate(shells):
        r = (0.34 + si * r_step) * scale
        ring(ax, cx, cy, r, C, lw=0.9)
        shell_electrons(ax, cx, cy, r, count, C, dot_r=0.028 * scale,
                        phase=(math.pi / 2) * si)
    ax.add_patch(Circle((cx, cy), 0.10 * scale, facecolor=C["acc"], edgecolor="none", zorder=7))


def ion_formation(C):
    fig = new_fig(9.6, 6.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.4); ax.set_ylim(0, 6.6); ax.axis("off")

    # ── row 1: sodium atom → sodium ion (loses one electron)
    y1 = 5.15
    draw_ion(ax, 1.55, y1, [2, 8, 1], C, scale=0.92)
    ax.text(1.55, 3.95, "sodium atom\nNa  [2,8,1]", fontsize=10, color=C["ink"],
            ha="center", va="top", linespacing=1.5)
    ax.annotate("", xy=(4.55, y1), xytext=(3.05, y1),
                arrowprops=dict(arrowstyle="-|>", color=C["acc"], lw=1.6))
    ax.text(3.8, y1 + 0.42, "loses 1 e⁻", fontsize=10, color=C["acc"], ha="center")
    draw_ion(ax, 6.05, y1, [2, 8], C, scale=0.92)
    ax.text(6.05, 3.95, "sodium ion\nNa⁺  [2,8]⁺", fontsize=10, color=C["ink"],
            ha="center", va="top", linespacing=1.5)
    ax.text(8.15, y1, "11 protons, 10 electrons\n→ overall charge +1", fontsize=10,
            color=C["muted"], ha="left", va="center", linespacing=1.55)

    # divider
    ax.plot([0.7, 9.9], [3.1, 3.1], color=C["hair_soft"], lw=1.0)

    # ── row 2: chlorine atom → chloride ion (gains one electron)
    y2 = 2.3
    draw_ion(ax, 1.55, y2, [2, 8, 7], C, scale=0.92)
    ax.text(1.55, 1.1, "chlorine atom\nCl  [2,8,7]", fontsize=10, color=C["ink"],
            ha="center", va="top", linespacing=1.5)
    ax.annotate("", xy=(4.55, y2), xytext=(3.05, y2),
                arrowprops=dict(arrowstyle="-|>", color=C["acc"], lw=1.6))
    ax.text(3.8, y2 + 0.42, "gains 1 e⁻", fontsize=10, color=C["acc"], ha="center")
    draw_ion(ax, 6.05, y2, [2, 8, 8], C, scale=0.92)
    ax.text(6.05, 1.1, "chloride ion\nCl⁻  [2,8,8]⁻", fontsize=10, color=C["ink"],
            ha="center", va="top", linespacing=1.5)
    ax.text(8.15, y2, "17 protons, 18 electrons\n→ overall charge −1", fontsize=10,
            color=C["muted"], ha="left", va="center", linespacing=1.55)
    save(fig, "ion-formation", C)


# ────────────────────────────────────────────────────────────────────
# 4) Element symbol tiles
# ────────────────────────────────────────────────────────────────────
ELEMENTS = [
    ("6", "C", "Carbon", "12.0107"),
    ("2", "He", "Helium", "4.002602"),
    ("25", "Mn", "Manganese", "54.938049"),
    ("53", "I", "Iodine", "126.90447"),
    ("16", "S", "Sulfur", "32.065"),
    ("69", "Tm", "Thulium", "168.93421"),
    ("86", "Rn", "Radon", "[222]"),
    ("39", "Y", "Yttrium", "88.90585"),
    ("4", "Be", "Beryllium", "9.02182"),
    ("49", "In", "Indium", "114.818"),
    ("16", "S", "Sulfur", "32.065"),
    ("15", "P", "Phosphorus", "30.973762"),
    ("77", "Ir", "Iridium", "192.217"),
    ("63", "Eu", "Europium", "151.964"),
    ("105", "Db", "Dubnium", "[268]"),
]


def element_symbols(C):
    fig = new_fig(9.4, 4.3)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 4.3); ax.axis("off")

    cols, rows = 5, 3
    tw, th = 1.72, 1.14
    gx, gy = 0.32, 0.28
    x0 = (10 - cols * tw - (cols - 1) * gx) / 2
    y_top = 4.16
    for i, (num, sym, name, mass) in enumerate(ELEMENTS):
        r, c = divmod(i, cols)
        x = x0 + c * (tw + gx)
        y = y_top - (r + 1) * th - r * gy
        ax.add_patch(FancyBboxPatch((x, y), tw, th,
                                    boxstyle="round,pad=0.02,rounding_size=0.07",
                                    facecolor="none", edgecolor=C["hair"], lw=1.0))
        ax.text(x + 0.12, y + th - 0.17, num, fontsize=8.5, color=C["acc"],
                ha="left", va="center", fontweight="bold")
        ax.text(x + tw / 2, y + th * 0.52, sym, fontsize=17, color=C["ink"],
                ha="center", va="center", fontweight="bold")
        ax.text(x + tw / 2, y + 0.30, name, fontsize=6.8, color=C["muted"],
                ha="center", va="center")
        ax.text(x + tw / 2, y + 0.13, mass, fontsize=6.2, color=C["faint"],
                ha="center", va="center")
    save(fig, "element-symbols", C)


# ────────────────────────────────────────────────────────────────────
# 5) The mole map
# ────────────────────────────────────────────────────────────────────
def mole_map(C):
    fig = new_fig(9.6, 5.2)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")

    def box(x, y, w, h, tint=False, lw=1.0):
        if tint:
            ax.add_patch(FancyBboxPatch((x, y), w, h,
                                        boxstyle="round,pad=0.02,rounding_size=0.12",
                                        facecolor=C["acc"], alpha=0.10,
                                        edgecolor="none"))
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor="none",
                                    edgecolor=(C["acc"] if tint else C["hair"]), lw=lw))

    # centre hub
    bx, by, bw, bh = 3.62, 1.95, 2.76, 1.3
    box(bx, by, bw, bh, tint=True, lw=1.4)
    ax.text(bx + bw / 2, by + bh * 0.66, "AMOUNT OF SUBSTANCE", fontsize=9.2,
            color=C["acc"], ha="center", va="center", fontweight="bold")
    ax.text(bx + bw / 2, by + bh * 0.27, "n  (mol)", fontsize=15, color=C["ink"],
            ha="center", va="center", fontweight="bold")

    sat = [
        # (x, y, w, h, title, lines)
        (0.55, 3.62, 3.1, 1.28, "MASS  m (g)", ["n = m ÷ M", "M = molar mass (g mol⁻¹)"]),
        (6.35, 3.62, 3.1, 1.28, "NUMBER OF PARTICLES", ["N = n × L", "L = 6.02 × 10²³ mol⁻¹"]),
        (0.55, 0.32, 3.1, 1.28, "GAS VOLUME  V (dm³)", ["n = V ÷ 24", "at r.t.p."]),
        (6.35, 0.32, 3.1, 1.28, "SOLUTIONS", ["n = c × V", "c in mol dm⁻³, V in dm³"]),
    ]
    for (x, y, w, h, title, lines) in sat:
        box(x, y, w, h)
        ax.text(x + w / 2, y + h * 0.70, title, fontsize=9.0, color=C["ink"],
                ha="center", va="center", fontweight="bold")
        for j, ln in enumerate(lines):
            ax.text(x + w / 2, y + h * (0.40 - j * 0.24), ln, fontsize=9.4,
                    color=C["muted"], ha="center", va="center")

    # double-headed connectors hub ↔ satellites
    hubs = [(2.1, 3.62), (7.9, 3.62), (2.1, 1.60), (7.9, 1.60)]
    targets = [(bx + 0.7, by + bh), (bx + bw - 0.7, by + bh),
               (bx + 0.7, by), (bx + bw - 0.7, by)]
    for (tx, ty), (hx, hy) in zip(hubs, targets):
        ax.add_patch(FancyArrowPatch((hx, hy), (tx, ty), arrowstyle="<|-|>",
                                     mutation_scale=11, color=C["hair"], lw=1.1))
    save(fig, "mole-map", C)


# ────────────────────────────────────────────────────────────────────
# 6) One mole, three substances
# ────────────────────────────────────────────────────────────────────
def flask(ax, cx, base, w, h, C):
    """Simple flat Erlenmeyer flask outline."""
    neck_w = w * 0.16
    top = base + h
    shoulder = base + h * 0.62
    pts = [
        (cx - neck_w / 2, top),
        (cx - neck_w / 2, shoulder),
        (cx - w / 2, base),
        (cx + w / 2, base),
        (cx + neck_w / 2, shoulder),
        (cx + neck_w / 2, top),
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor="none",
                         edgecolor=C["hair"], lw=1.2, joinstyle="round"))
    # lip
    ax.plot([cx - neck_w * 0.95, cx + neck_w * 0.95], [top, top],
            color=C["hair"], lw=1.2, solid_capstyle="round")


def mole_comparison(C):
    fig = new_fig(9.6, 4.3)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")

    ax.text(5.0, 3.94, "One mole of each — the same number of particles, different masses",
            fontsize=10.5, color=C["muted"], ha="center", va="center")

    panels = [
        (1.75, "He", "helium", "4 g", "6.02 × 10²³ atoms"),
        (5.0, "CO₂", "carbon dioxide", "44 g", "6.02 × 10²³ molecules"),
        (8.25, "NO₃⁻", "nitrate ions", "62 g", "6.02 × 10²³ ions"),
    ]
    for cx, formula, name, mass, count in panels:
        base = 1.72
        flask(ax, cx, base, 1.7, 1.55, C)
        # particle dots inside the body
        dot_r = 0.052
        pts = [(-0.36, 0.22), (-0.16, 0.32), (0.08, 0.22), (0.30, 0.30),
               (-0.26, 0.06), (0.02, 0.10), (0.26, 0.06), (-0.06, -0.10),
               (0.18, -0.12), (-0.28, -0.14), (0.06, -0.24), (-0.12, 0.46),
               (0.14, 0.48), (-0.02, 0.62)]
        for (dx, dy) in pts:
            ax.add_patch(Circle((cx + dx, base + 0.36 + dy), dot_r,
                                facecolor=C["acc"], edgecolor="none", alpha=0.85, zorder=5))
        ax.text(cx, 1.06, f"{name} — {formula}", fontsize=10.5, color=C["ink"],
                ha="center", va="center", fontweight="bold")
        ax.text(cx, 0.72, mass + " per mole", fontsize=10, color=C["muted"],
                ha="center", va="center")
        ax.text(cx, 0.36, count, fontsize=10, color=C["acc"], ha="center", va="center")
    save(fig, "mole-comparison", C)


if __name__ == "__main__":
    for theme in (LIGHT, DARK):
        atom_structure(theme)
        nuclide_notation(theme)
        ion_formation(theme)
        element_symbols(theme)
        mole_map(theme)
        mole_comparison(theme)
    print("done")
