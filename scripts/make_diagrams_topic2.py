#!/usr/bin/env python3
"""Generate raster (PNG) chemistry diagrams for the IAL Chemistry site — Topic 2.

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
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, FancyBboxPatch

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
    "neutron": "#8d9096",
    "grey_tint": (141/255, 144/255, 150/255, 0.16),
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
    "neutron": "#7c7f85",
    "grey_tint": (163/255, 166/255, 173/255, 0.18),
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


def style_axes(ax, C, xlabel="", ylabel=""):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(C["hair"])
        ax.spines[side].set_linewidth(1.0)
    ax.tick_params(colors=C["muted"], labelsize=9, width=1.0, length=3.5)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=C["muted"])
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=C["muted"])


def nucleus(ax, cx, cy, C, protons=6, neutrons=6, r0=0.075, spread=0.055):
    pts = []
    n = protons + neutrons
    for i in range(n):
        a = 2 * math.pi * i / n + 0.35
        rr = 0 if i == 0 else spread * (1.25 if i % 2 == 0 else 0.75)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a), i % 2 == 0))
    for (x, y, is_p) in pts:
        col = C["acc"] if is_p else C["neutron"]
        ax.add_patch(Circle((x, y), r0, facecolor=col, edgecolor=C["fill"], lw=0.6, zorder=6))


def shell_electrons(ax, cx, cy, r, n, C, dot_r=0.035, phase=0.0):
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        ax.add_patch(Circle((cx + r * math.cos(a), cy + r * math.sin(a)), dot_r,
                            facecolor=C["ink"], edgecolor="none", zorder=6))


# ────────────────────────────────────────────────────────────────────
# 1) The three isotopes of carbon
# ────────────────────────────────────────────────────────────────────
def carbon_isotopes(C):
    fig = new_fig(9.8, 4.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.5); ax.axis("off")

    panels = [
        (1.9, 12, 6, 6),
        (5.2, 13, 6, 7),
        (8.5, 14, 6, 8),
    ]
    for cx, mass, np_, nn in panels:
        ax.add_patch(Circle((cx, 2.55), 0.78, fill=False, edgecolor=C["hair"], lw=1.0,
                            linestyle=(0, (4, 3))))
        ax.add_patch(Circle((cx, 2.55), 1.32, fill=False, edgecolor=C["hair"], lw=1.0,
                            linestyle=(0, (4, 3))))
        nucleus(ax, cx, 2.55, C, protons=np_, neutrons=nn, r0=0.062, spread=0.05)
        shell_electrons(ax, cx, 2.55, 0.78, 2, C, dot_r=0.045, phase=math.pi / 2)
        shell_electrons(ax, cx, 2.55, 1.32, 4, C, dot_r=0.045, phase=math.pi / 4)
        ax.text(cx, 4.18, rf"$^{{{mass}}}_{{6}}\,$C", fontsize=17, color=C["ink"],
                ha="center", va="center")
        ax.text(cx, 0.66, f"{np_} protons · {nn} neutrons", fontsize=9.5, color=C["muted"],
                ha="center", va="center")
        ax.text(cx, 0.30, f"mass number {mass}", fontsize=9.5, color=C["acc"],
                ha="center", va="center")
    # shared electron note
    ax.text(5.2, 0.02, "", fontsize=1)  # spacing guard
    ax.text(1.9, 3.62, "", fontsize=1)
    ax.text(10.15, 2.55, "same number\nof electrons →\nsame chemical\nproperties", fontsize=9.0,
            color=C["muted"], ha="right", va="center", linespacing=1.5)
    save(fig, "carbon-isotopes", C)


# ────────────────────────────────────────────────────────────────────
# 2) Mass spectrometer schematic
# ────────────────────────────────────────────────────────────────────
def station_label(ax, cx, cy, text, C, w=1.62, h=0.52):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor=C["fill"], edgecolor=C["hair"], lw=1.0, zorder=8))
    ax.text(cx, cy, text, fontsize=8.0, color=C["ink"], ha="center", va="center",
            zorder=9, linespacing=1.3)


def small_box(ax, cx, cy, text, C, w=1.05, h=0.44, fs=7.6):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="none", edgecolor=C["hair"], lw=0.9, zorder=8))
    ax.text(cx, cy, text, fontsize=fs, color=C["muted"], ha="center", va="center", zorder=9)


def mass_spectrometer(C):
    fig = new_fig(10.6, 5.5)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.6); ax.set_ylim(0, 5.5); ax.axis("off")

    y_tube = 3.30
    yt, yb = y_tube + 0.11, y_tube - 0.11

    # straight flight tube (hairline walls, faint accent fill)
    ax.fill([0.95, 5.60, 5.60, 0.95], [yb, yb, yt, yt], color=C["acc_tint"],
            edgecolor="none", zorder=1)
    ax.plot([0.95, 5.60], [yt, yt], color=C["hair"], lw=1.1, zorder=2)
    ax.plot([0.95, 5.60], [yb, yb], color=C["hair"], lw=1.1, zorder=2)

    # sample inlet
    small_box(ax, 1.05, 4.55, "vapourised\nsample", C, w=1.30, h=0.60, fs=8.0)
    ax.add_patch(FancyArrowPatch((1.05, 4.25), (1.05, 3.44),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))

    # ionisation: electron gun from above
    ax.plot([2.40, 2.40], [yt, yt + 0.58], color=C["hair"], lw=1.0, zorder=2)
    ax.plot([2.52, 2.52], [yt, yt + 0.58], color=C["hair"], lw=1.0, zorder=2)
    ax.text(2.62, yt + 0.44, "e⁻ gun", fontsize=7.8, color=C["faint"], ha="left", va="center")
    station_label(ax, 2.45, 2.62, "IONISATION", C, w=1.50)
    ax.add_patch(FancyArrowPatch((2.45, 2.90), (2.45, yb - 0.02),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))

    # vacuum pump stub
    ax.plot([3.50, 3.50], [yt, yt + 0.52], color=C["hair"], lw=0.9)
    ax.text(3.64, yt + 0.44, "to vacuum pump", fontsize=7.8, color=C["faint"],
            ha="left", va="center")

    # acceleration slits
    for dx in (4.15, 4.31):
        ax.plot([dx, dx], [yb - 0.06, yt + 0.06], color=C["ink"], lw=1.6, zorder=3)
    station_label(ax, 4.23, 2.62, "ACCELERATION", C, w=1.72)
    ax.add_patch(FancyArrowPatch((4.23, 2.90), (4.23, yb - 0.02),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))

    # deflection: 90° bend, centre of curvature below the tube end
    cx_arc, cy_arc = 5.60, 2.02
    r_out, r_in = yt - cy_arc, yb - cy_arc          # 1.39 / 1.17
    ts = np.linspace(math.radians(3), math.radians(87), 60)
    xs_o = cx_arc + r_out * np.cos(ts); ys_o = cy_arc + r_out * np.sin(ts)
    xs_i = cx_arc + r_in * np.cos(ts); ys_i = cy_arc + r_in * np.sin(ts)
    ax.fill(np.concatenate([xs_o, xs_i[::-1]]), np.concatenate([ys_o, ys_i[::-1]]),
            color=C["acc_tint"], edgecolor="none", zorder=1)
    ax.add_patch(Arc((cx_arc, cy_arc), 2 * r_out, 2 * r_out, angle=0,
                     theta1=0, theta2=90, color=C["hair"], lw=1.1, zorder=2))
    ax.add_patch(Arc((cx_arc, cy_arc), 2 * r_in, 2 * r_in, angle=0,
                     theta1=0, theta2=90, color=C["hair"], lw=1.1, zorder=2))

    # electromagnet shoe outside the bend
    ax.add_patch(Arc((cx_arc, cy_arc), 2 * (r_out + 0.17), 2 * (r_out + 0.17),
                     angle=0, theta1=32, theta2=68, color=C["neutron"], lw=5.0, zorder=2))
    ax.text(7.30, 3.62, "electromagnet", fontsize=8.0, color=C["muted"], ha="left", va="center")
    ax.annotate("", xy=(cx_arc + (r_out + 0.17) * math.cos(math.radians(64)),
                        cy_arc + (r_out + 0.17) * math.sin(math.radians(64))),
                xytext=(7.26, 3.62),
                arrowprops=dict(arrowstyle="-", color=C["faint"], lw=0.9))

    station_label(ax, 5.70, 2.42, "DEFLECTION", C, w=1.55)
    ax.add_patch(FancyArrowPatch((6.02, 2.66), (6.42, 2.88),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))

    # short vertical run from the end of the bend down to the detector
    dx_det = cx_arc + (r_out + r_in) / 2          # beam centreline x ≈ 6.88
    ax.fill([dx_det - 0.11, dx_det + 0.11, dx_det + 0.11, dx_det - 0.11],
            [cy_arc, cy_arc, 1.57, 1.57], color=C["acc_tint"], edgecolor="none", zorder=1)
    ax.plot([dx_det - 0.11, dx_det - 0.11], [cy_arc, 1.57], color=C["hair"], lw=1.1, zorder=2)
    ax.plot([dx_det + 0.11, dx_det + 0.11], [cy_arc, 1.57], color=C["hair"], lw=1.1, zorder=2)
    small_box(ax, dx_det, 1.35, "detector", C, w=1.05)
    ax.add_patch(FancyArrowPatch((dx_det, 1.13), (dx_det, 0.84),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))
    small_box(ax, dx_det, 0.60, "amplifier", C, w=1.15)
    ax.add_patch(FancyArrowPatch((dx_det + 0.58, 0.60), (dx_det + 0.92, 0.60),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))
    small_box(ax, dx_det + 1.68, 0.60, "chart\nrecorder", C, w=1.20, h=0.56, fs=7.6)
    station_label(ax, 5.55, 1.35, "DETECTION", C, w=1.50)
    ax.add_patch(FancyArrowPatch((6.32, 1.35), (dx_det - 0.55, 1.35),
                                 arrowstyle="-|>", mutation_scale=9, color=C["faint"], lw=1.0))

    ax.text(0.40, 0.18, "The recorder converts the detected current into the peaks of the mass spectrum.",
            fontsize=9.0, color=C["muted"], ha="left", va="center")
    save(fig, "mass-spectrometer", C)


# ────────────────────────────────────────────────────────────────────
# 3) Neon mass spectrum
# ────────────────────────────────────────────────────────────────────
def neon_spectrum(C):
    fig = new_fig(8.8, 4.4)
    ax = fig.add_axes([0.13, 0.17, 0.84, 0.74])
    xs = [20, 21, 22]
    hs = [90.92, 0.26, 8.82]
    for x, h in zip(xs, hs):
        ax.plot([x, x], [0, h], color=C["acc"], lw=2.2, solid_capstyle="butt")
        ax.plot(x, h, "o", color=C["acc"], ms=3.2)
    labs = ["90.92%", "0.26%", "8.82%"]
    offs = [2.5, 2.5, 2.5]
    for x, h, lab, off in zip(xs, hs, labs, offs):
        ax.text(x, h + off, lab, fontsize=9.5, color=C["ink"], ha="center", va="bottom")
    ax.set_xlim(19.2, 22.8)
    ax.set_ylim(0, 108)
    ax.set_xticks([19, 20, 21, 22, 23])
    style_axes(ax, C, xlabel="mass-to-charge ratio,  m/z", ylabel="Relative abundance / %")
    ax.text(22.75, 96, "²⁰Ne, ²¹Ne and ²²Ne", fontsize=9.5, color=C["muted"], ha="right", va="center")
    save(fig, "neon-spectrum", C)


# ────────────────────────────────────────────────────────────────────
# 4) Chlorine mass spectrum (diatomic)
# ────────────────────────────────────────────────────────────────────
def chlorine_spectrum(C):
    fig = new_fig(9.0, 4.9)
    ax = fig.add_axes([0.11, 0.235, 0.87, 0.68])
    peaks = [(35, 3, "A"), (37, 1, "B"), (70, 9, "C"), (72, 6, "D"), (74, 1, "E")]
    for x, h, lab in peaks:
        ax.plot([x, x], [0, h], color=C["acc"], lw=2.4, solid_capstyle="butt")
        ax.plot(x, h, "o", color=C["acc"], ms=3.2)
        ax.text(x, h + 0.42, lab, fontsize=10.5, color=C["ink"], ha="center", va="bottom",
                fontweight="bold")
    ax.set_xlim(28, 80)
    ax.set_ylim(-1.9, 10.6)
    ax.set_xticks([30, 40, 50, 60, 70])
    ax.set_yticks([])
    style_axes(ax, C, xlabel="m/z")
    ax.set_ylabel("Relative abundance", fontsize=10, color=C["muted"])
    # brackets: atomic ions / molecular ions
    def bracket(x0, x1, y, label):
        d = 0.22
        ax.plot([x0, x0, x1, x1], [y - d, y, y, y - d], color=C["faint"], lw=1.0)
        ax.text((x0 + x1) / 2, y - d - 0.28, label, fontsize=9.5, color=C["ink"],
                ha="center", va="top")
    bracket(33.5, 38.5, -0.55, "Atomic ions")
    bracket(68.5, 75.5, -0.55, "Molecular ions")
    save(fig, "chlorine-spectrum", C)


# ────────────────────────────────────────────────────────────────────
# 5) Ethanol mass spectrum (polyatomic)
# ────────────────────────────────────────────────────────────────────
def ethanol_spectrum(C):
    fig = new_fig(9.0, 4.7)
    ax = fig.add_axes([0.10, 0.17, 0.88, 0.74])
    peaks = [(15, 8), (26, 10), (27, 32), (28, 14), (29, 24), (31, 100),
             (42, 8), (43, 12), (45, 55), (46, 60)]
    for x, h in peaks:
        col = C["acc"] if x == 46 else C["neutron"]
        lw = 2.4 if x == 46 else 1.8
        ax.plot([x, x], [0, h], color=col, lw=lw, solid_capstyle="butt")
    ax.annotate("M peak at m/z of 46", xy=(46, 60), xytext=(50.5, 74),
                fontsize=9.5, color=C["acc"], ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=C["acc"], lw=1.0))
    ax.set_xlim(8, 62)
    ax.set_ylim(0, 112)
    ax.set_xticks([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
    ax.tick_params(axis="x", labelsize=8)
    style_axes(ax, C, xlabel="m/z", ylabel="Relative intensity")
    save(fig, "ethanol-spectrum", C)


# ────────────────────────────────────────────────────────────────────
# 6) Shapes of s, p and d orbitals
# ────────────────────────────────────────────────────────────────────
def axes_tripod(ax, cx, cy, L, C, labels=True):
    ax.annotate("", xy=(cx, cy + L), xytext=(cx, cy - L * 0.62),
                arrowprops=dict(arrowstyle="-|>", color=C["faint"], lw=0.9))
    ax.annotate("", xy=(cx + L * 0.86, cy + L * 0.50), xytext=(cx - L * 0.62, cy - L * 0.36),
                arrowprops=dict(arrowstyle="-|>", color=C["faint"], lw=0.9))
    ax.annotate("", xy=(cx + L * 0.86, cy - L * 0.50), xytext=(cx - L * 0.62, cy + L * 0.36),
                arrowprops=dict(arrowstyle="-|>", color=C["faint"], lw=0.9))
    if labels:
        ax.text(cx, cy + L * 1.10, "z", fontsize=8, color=C["faint"], ha="center", va="center")
        ax.text(cx + L * 0.95, cy + L * 0.55, "y", fontsize=8, color=C["faint"], ha="center", va="center")
        ax.text(cx + L * 0.95, cy - L * 0.55, "x", fontsize=8, color=C["faint"], ha="center", va="center")


def lobe(ax, cx, cy, w, h, angle, C, positive=True):
    grey = (141/255, 144/255, 150/255, 0.85) if theme_is_light(C) else (163/255, 166/255, 173/255, 0.85)
    acc = matplotlib.colors.to_rgba(C["acc"], 0.80)
    col = grey if positive else acc
    ax.add_patch(Ellipse((cx, cy), w, h, angle=angle, facecolor=col,
                         edgecolor=C["fill"], lw=0.6, zorder=5))


def theme_is_light(C):
    return C is LIGHT


def orbitals(C):
    fig = new_fig(10.6, 5.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.6); ax.set_ylim(0, 5.6); ax.axis("off")

    # ── s orbital (spherical)
    sx, sy = 1.95, 3.30
    axes_tripod(ax, sx, sy, 1.50, C)
    ax.add_patch(Circle((sx, sy), 0.95, facecolor=C["grey_tint"], edgecolor=C["neutron"],
                        lw=1.0, zorder=4))
    ax.add_patch(Circle((sx, sy), 0.09, facecolor=C["acc"], edgecolor="none", zorder=6))
    ax.text(sx, 5.22, "s orbital", fontsize=11.5, color=C["ink"], ha="center", va="center",
            fontweight="bold")
    ax.text(sx, 1.22, "spherical —\nthe 2s orbital is larger than 1s", fontsize=9.0,
            color=C["muted"], ha="center", va="center", linespacing=1.45)

    # ── p orbitals: three dumbbells sharing one centre
    px, py = 5.45, 3.30
    axes_tripod(ax, px, py, 1.58, C)
    L = 0.74          # lobe centre distance
    lw_, lh = 1.16, 0.42
    # each orbital gets ONE colour so the three dumbbells read separately
    ax_x = math.radians(-30)
    ax_y = math.radians(30)
    grey_hi = (163/255, 166/255, 173/255, 0.85) if theme_is_light(C) else (141/255, 144/255, 150/255, 0.85)
    grey_lo = (141/255, 144/255, 150/255, 0.55) if theme_is_light(C) else (120/255, 122/255, 128/255, 0.60)
    acc_pair = matplotlib.colors.to_rgba(C["acc"], 0.72)
    lobes = [
        # p_z (vertical) — grey
        (px, py + L, 0, grey_hi), (px, py - L, 0, grey_hi),
        # p_x (along the lower-right axis, −30°) — coral
        (px + L * math.cos(ax_x), py + L * math.sin(ax_x), -30, acc_pair),
        (px - L * math.cos(ax_x), py - L * math.sin(ax_x), -30, acc_pair),
        # p_y (along the upper-right axis, +30°) — soft grey
        (px + L * math.cos(ax_y), py + L * math.sin(ax_y), 30, grey_lo),
        (px - L * math.cos(ax_y), py - L * math.sin(ax_y), 30, grey_lo),
    ]
    for lx, ly, ang, col in lobes:
        ax.add_patch(Ellipse((lx, ly), lh, lw_, angle=ang, facecolor=col,
                             edgecolor=C["fill"], lw=0.6, zorder=5))
    ax.add_patch(Circle((px, py), 0.06, facecolor=C["acc"], edgecolor="none", zorder=6))
    ax.text(px, 5.22, "p orbitals", fontsize=11.5, color=C["ink"], ha="center", va="center",
            fontweight="bold")
    ax.text(px, 1.22, "three dumbbells at right angles:\n$p_x$   ·   $p_y$   ·   $p_z$",
            fontsize=9.0, color=C["muted"], ha="center", va="center", linespacing=1.45)

    # ── d orbitals: two representative shapes
    d1x, d1y = 8.45, 3.42
    axes_tripod(ax, d1x, d1y, 1.15, C, labels=False)
    for ang in (45, 135, 225, 315):
        lx = d1x + 0.52 * math.cos(math.radians(ang))
        ly = d1y + 0.52 * math.sin(math.radians(ang))
        lobe(ax, lx, ly, 0.34, 0.80, ang, C, ang in (45, 225))
    ax.text(d1x, 1.78, "$d_{xy}$", fontsize=9.5, color=C["ink"], ha="center", va="center")

    d2x, d2y = 9.95, 3.42
    lobe(ax, d2x, d2y + 0.60, 0.36, 0.92, 0, C, True)
    lobe(ax, d2x, d2y - 0.60, 0.36, 0.92, 0, C, False)
    ax.add_patch(Ellipse((d2x, d2y), 0.82, 0.24, facecolor=C["grey_tint"],
                         edgecolor=C["neutron"], lw=0.9, zorder=4))
    ax.text(d2x, 1.78, "$d_{z^2}$", fontsize=9.5, color=C["ink"], ha="center", va="center")

    ax.text(9.20, 5.22, "d orbitals", fontsize=11.5, color=C["ink"], ha="center", va="center",
            fontweight="bold")
    ax.text(9.20, 1.22, "five four-lobed shapes —\ntwo of them shown here", fontsize=9.0,
            color=C["muted"], ha="center", va="center", linespacing=1.45)

    # rule strip
    ax.plot([0.75, 10.0], [0.62, 0.62], color=C["hair_soft"], lw=1.0)
    ax.text(5.3, 0.30, "Each orbital holds a maximum of two electrons, with opposite spins  ( ↑↓ )",
            fontsize=9.6, color=C["ink"], ha="center", va="center")
    save(fig, "orbitals", C)


# ────────────────────────────────────────────────────────────────────
# 7) Successive ionisation energies of sodium
# ────────────────────────────────────────────────────────────────────
def sodium_ie(C):
    ies = [496, 4563, 6913, 9544, 13352, 16611, 20115, 25491, 28934, 141367, 159079]
    logs = [math.log10(v) for v in ies]
    fig = new_fig(8.8, 5.0)
    ax = fig.add_axes([0.12, 0.15, 0.86, 0.78])
    xs = list(range(1, 12))
    ax.plot(xs, logs, "-", color=C["hair"], lw=1.1, zorder=2)
    ax.plot(xs, logs, "o", color=C["acc"], ms=5.5, zorder=3)
    # shell-change markers
    for xj in (1.5, 9.5):
        ax.axvline(xj, color=C["faint"], lw=1.0, linestyle=(0, (3, 3)), zorder=1)
    ax.text(1.5, 5.62, "change of shell\n3rd → 2nd", fontsize=8.6, color=C["muted"],
            ha="center", va="bottom", linespacing=1.4)
    ax.text(9.5, 5.62, "change of shell\n2nd → 1st", fontsize=8.6, color=C["muted"],
            ha="center", va="bottom", linespacing=1.4)
    ax.set_xlim(0.4, 11.6)
    ax.set_ylim(2, 6.3)
    ax.set_xticks(xs)
    style_axes(ax, C, xlabel="Order of electron removed", ylabel="log (ionisation energy)")
    save(fig, "sodium-ie", C)


# ────────────────────────────────────────────────────────────────────
# 8) First ionisation energies across periods 1–3
# ────────────────────────────────────────────────────────────────────
def first_ie_periods(C):
    elems = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
             "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    vals = [1310, 2370, 519, 900, 799, 1090, 1400, 1310, 1680, 2080,
            494, 736, 577, 786, 1060, 1000, 1260, 1520]
    ups   = [False, True, False, True, False, True, True, False, True, True,
             False, True, False, True, True, False, True, True]
    fig = new_fig(9.6, 5.4)
    ax = fig.add_axes([0.11, 0.13, 0.87, 0.80])
    xs = list(range(1, 19))
    ax.plot(xs, vals, "-", color=C["hair"], lw=1.2, zorder=2)
    ax.plot(xs, vals, "o", color=C["acc"], ms=4.6, zorder=3)
    for x, v, sym, up in zip(xs, vals, elems, ups):
        dy = 62 if up else -62
        va = "bottom" if up else "top"
        ax.text(x, v + dy, sym, fontsize=8.6, color=C["ink"], ha="center", va=va)
    ax.set_xlim(0.3, 18.7)
    ax.set_ylim(0, 2650)
    ax.set_xticks(range(2, 19, 2))
    style_axes(ax, C, xlabel="Atomic number", ylabel="Ionisation energy / kJ mol⁻¹")
    save(fig, "first-ie-periods", C)


# ────────────────────────────────────────────────────────────────────
# 9) Blocks of the periodic table (first four periods, up to Xe)
# ────────────────────────────────────────────────────────────────────
def periodic_blocks(C):
    rows = [
        # period 2
        (["Li", "Be"], [], ["B", "C", "N", "O", "F", "Ne"]),
        (["Na", "Mg"], [], ["Al", "Si", "P", "S", "Cl", "Ar"]),
        (["K", "Ca"], ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"],
         ["Ga", "Ge", "As", "Se", "Br", "Kr"]),
        (["Rb", "Sr"], ["Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd"],
         ["In", "Sn", "Sb", "Te", "I", "Xe"]),
    ]
    cw, ch = 0.545, 0.60
    gx, gy = 0.045, 0.075
    x0, y_top = 0.55, 3.78
    fig = new_fig(10.4, 5.0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 11.2); ax.set_ylim(0, 5.0); ax.axis("off")

    def cell(col, row, sym, tint):
        x = x0 + col * (cw + gx)
        y = y_top - (row + 1) * ch - row * gy
        ax.add_patch(FancyBboxPatch((x, y), cw, ch,
                                    boxstyle="square,pad=0",
                                    facecolor=tint, edgecolor=C["hair"], lw=0.9))
        ax.text(x + cw / 2, y + ch / 2, sym, fontsize=8.6, color=C["ink"],
                ha="center", va="center")

    s_tint = C["acc_tint"]
    p_tint = C["grey_tint"]
    d_tint = (C["neutron"][0] if isinstance(C["neutron"], tuple) else 0.55,
              C["neutron"][1] if isinstance(C["neutron"], tuple) else 0.55,
              C["neutron"][2] if isinstance(C["neutron"], tuple) else 0.55, 0.10)
    for r, (sblock, dblock, pblock) in enumerate(rows):
        for c, sym in enumerate(sblock):
            cell(c, r, sym, s_tint)
        for c, sym in enumerate(dblock):
            cell(2 + c, r, sym, d_tint)
        for c, sym in enumerate(pblock):
            cell(12 + c, r, sym, p_tint)

    # block brackets + group numbers
    def brace(c0, c1, label, y):
        x_a = x0 + c0 * (cw + gx)
        x_b = x0 + (c1 + 1) * (cw + gx) - gx
        ax.plot([x_a, x_a, x_b, x_b], [y + 0.10, y + 0.22, y + 0.22, y + 0.10],
                color=C["faint"], lw=1.0)
        ax.text((x_a + x_b) / 2, y + 0.38, label, fontsize=9.6, color=C["ink"],
                ha="center", va="bottom", fontweight="bold")

    brace(0, 1, "s-block", 4.22)
    brace(12, 17, "p-block", 4.22)
    brace(2, 11, "d-block (transition elements)", 4.22)

    # group numbers over s and p columns
    for c, g in ((0, "1"), (1, "2")):
        x = x0 + c * (cw + gx) + cw / 2
        ax.text(x, 4.02, g, fontsize=8.4, color=C["acc"], ha="center", va="center")
    for i in range(6):
        x = x0 + (12 + i) * (cw + gx) + cw / 2
        ax.text(x, 4.02, str(3 + i), fontsize=8.4, color=C["acc"], ha="center", va="center")

    ax.text(0.55, 0.30, "The block tells you which sub-shell the last electron enters — "
                        "f-block (lanthanides and actinides) sits below the main table.",
            fontsize=9.2, color=C["muted"], ha="left", va="center")
    save(fig, "periodic-blocks", C)


# ────────────────────────────────────────────────────────────────────
# 10) Ionic radius: Na → Na⁺ and Cl → Cl⁻
# ────────────────────────────────────────────────────────────────────
def ionic_radius(C):
    fig = new_fig(9.8, 4.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.6); ax.axis("off")

    def ion_circle(cx, cy, r, label, C, tint, edge):
        ax.add_patch(Circle((cx, cy), r, facecolor=tint, edgecolor=edge, lw=1.2, zorder=3))
        ax.text(cx, cy, label, fontsize=11.5, color=C["ink"], ha="center", va="center", zorder=4)

    # row 1 — cation (smaller)
    y1 = 3.28
    ion_circle(1.65, y1, 0.82, "Na", C, C["acc_tint"], C["acc"])
    ax.add_patch(FancyArrowPatch((2.72, y1), (4.10, y1), arrowstyle="-|>",
                                 mutation_scale=13, color=C["acc"], lw=1.5))
    ax.text(3.41, y1 + 0.34, "loses 1 e⁻", fontsize=9.2, color=C["acc"], ha="center")
    ion_circle(4.95, y1, 0.55, "Na⁺", C, C["acc_tint"], C["acc"])
    ax.text(6.05, y1 + 0.10, "11 protons  ·  11 electrons", fontsize=9.2, color=C["muted"],
            ha="left", va="center")
    ax.text(6.05, y1 - 0.36, "→  11 protons  ·  10 electrons", fontsize=9.2, color=C["ink"],
            ha="left", va="center")
    ax.text(1.65, 4.36, "Positive ion — smaller than the atom", fontsize=10.2, color=C["ink"],
            ha="center", va="center", fontweight="bold")

    # divider
    ax.plot([0.7, 9.9], [2.30, 2.30], color=C["hair_soft"], lw=1.0)

    # row 2 — anion (larger)
    y2 = 1.28
    ion_circle(1.65, y2, 0.55, "Cl", C, C["grey_tint"], C["neutron"])
    ax.add_patch(FancyArrowPatch((2.42, y2), (3.80, y2), arrowstyle="-|>",
                                 mutation_scale=13, color=C["acc"], lw=1.5))
    ax.text(3.11, y2 + 0.34, "gains 1 e⁻", fontsize=9.2, color=C["acc"], ha="center")
    ion_circle(4.95, y2, 0.82, "Cl⁻", C, C["grey_tint"], C["neutron"])
    ax.text(6.05, y2 + 0.10, "17 protons  ·  17 electrons", fontsize=9.2, color=C["muted"],
            ha="left", va="center")
    ax.text(6.05, y2 - 0.36, "→  17 protons  ·  18 electrons", fontsize=9.2, color=C["ink"],
            ha="left", va="center")
    ax.text(1.65, 2.02, "Negative ion — larger than the atom", fontsize=10.2, color=C["ink"],
            ha="center", va="center", fontweight="bold")
    save(fig, "ionic-radius", C)


# ────────────────────────────────────────────────────────────────────
# 11) Paired vs unpaired 2p electrons (N vs O)
# ────────────────────────────────────────────────────────────────────
def paired_boxes(C):
    fig = new_fig(9.0, 3.7)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 9.4); ax.set_ylim(0, 3.7); ax.axis("off")

    def draw_row(cy, title, boxes):
        ax.text(2.55, cy + 0.50, title, fontsize=10.4, color=C["ink"], ha="right", va="center")
        ax.text(2.92, cy, "2p", fontsize=9.5, color=C["acc"], ha="right", va="center",
                fontweight="bold")
        bx = 3.05
        for b in boxes:
            ax.add_patch(FancyBboxPatch((bx, cy - 0.26), 0.56, 0.52,
                                        boxstyle="square,pad=0",
                                        facecolor=C["acc_tint"] if len(b) == 2 else "none",
                                        edgecolor=C["hair"], lw=1.0))
            if len(b) == 2:
                ax.text(bx + 0.20, cy, "↑", fontsize=12, color=C["ink"], ha="center", va="center")
                ax.text(bx + 0.38, cy, "↓", fontsize=12, color=C["ink"], ha="center", va="center")
            elif len(b) == 1:
                ax.text(bx + 0.28, cy, "↑", fontsize=12, color=C["ink"], ha="center", va="center")
            bx += 0.72
        return bx

    draw_row(2.62, "N  (Z = 7)", ["↑", "↑", "↑"])
    ax.text(5.45, 2.62, "three unpaired 2p electrons", fontsize=9.4, color=C["muted"],
            ha="left", va="center")
    draw_row(1.28, "O  (Z = 8)", ["↑↓", "↑", "↑"])
    ax.text(5.45, 1.28, "the 4th electron must pair up", fontsize=9.4, color=C["muted"],
            ha="left", va="center")
    ax.plot([0.7, 8.9], [3.28, 3.28], color=C["hair_soft"], lw=1.0)
    ax.text(4.7, 3.50, "Why O < N: paired electrons repel, so the paired electron is easier to remove",
            fontsize=9.6, color=C["ink"], ha="center", va="center")
    save(fig, "paired-boxes", C)


# ────────────────────────────────────────────────────────────────────
# 12) Melting points across Period 3
# ────────────────────────────────────────────────────────────────────
def melting_period3(C):
    elems = ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    vals = [371, 922, 933, 1713, 317, 386, 172, 84]  # K (from the table, +273; Ar from the graph)
    fig = new_fig(8.8, 4.8)
    ax = fig.add_axes([0.12, 0.15, 0.85, 0.78])
    xs = list(range(1, 9))
    ax.plot(xs, vals, "-", color=C["acc"], lw=1.6, zorder=2)
    ax.plot(xs, vals, "o", color=C["ink"], ms=5.0, zorder=3)
    for x, v, sym in zip(xs, vals, elems):
        ax.text(x, v + 62, sym, fontsize=9.6, color=C["ink"], ha="center", va="bottom")
        ax.text(x, -125, "", fontsize=1)
    ax.axhline(0, color=C["hair"], lw=0.0)
    ax.set_xlim(0.4, 8.6)
    ax.set_ylim(0, 1960)
    ax.set_xticks(xs)
    ax.set_xticklabels([])
    style_axes(ax, C, xlabel="", ylabel="Melting point / K")
    save(fig, "melting-period3", C)


# ────────────────────────────────────────────────────────────────────
# 13) log(first ionisation energy) for the elements 1 to 36
# ────────────────────────────────────────────────────────────────────
def ie_1_36_log(C):
    elems = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
             "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
             "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",
             "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"]
    vals = [1310, 2370, 519, 900, 799, 1090, 1400, 1310, 1680, 2080,
            494, 736, 577, 786, 1060, 1000, 1260, 1520,
            418, 590, 632, 661, 648, 653, 716, 762, 757, 736,
            745, 906, 579, 762, 947, 941, 1140, 1351]
    logs = [math.log10(v) for v in vals]
    fig = new_fig(11.8, 5.6)
    ax = fig.add_axes([0.095, 0.13, 0.89, 0.77])
    xs = list(range(1, 37))
    # period separators
    for xj, lab in ((2.5, "period 2"), (10.5, "period 3"), (18.5, "period 4")):
        ax.axvline(xj, color=C["faint"], lw=1.0, linestyle=(0, (3, 3)), zorder=1)
        ax.text(xj + 0.18, 3.60, lab, fontsize=8.2, color=C["faint"], ha="left", va="top")
    ax.plot(xs, logs, "-", color=C["hair"], lw=1.2, zorder=2)
    ax.plot(xs, logs, "o", color=C["acc"], ms=4.4, zorder=3)
    ups = [i % 2 == 0 for i in range(36)]
    for k in (1, 9, 17, 29, 35):        # He, Ne, Ar, Zn, Kr — label above the point
        ups[k] = True
    ups[0] = False                       # H — keep clear of the y-axis
    for x, v, sym, up in zip(xs, logs, elems, ups):
        dy = 0.052 if up else -0.052
        va = "bottom" if up else "top"
        ax.text(x, v + dy, sym, fontsize=8.2, color=C["ink"], ha="center", va=va)
    ax.set_xlim(0.1, 37.2)
    ax.set_ylim(2.35, 3.62)
    ax.set_xticks(range(2, 37, 2))
    style_axes(ax, C, xlabel="Atomic number", ylabel="log (first ionisation energy / kJ mol⁻¹)")
    save(fig, "ie-1-36-log", C)


if __name__ == "__main__":
    for theme in (LIGHT, DARK):
        carbon_isotopes(theme)
        mass_spectrometer(theme)
        neon_spectrum(theme)
        chlorine_spectrum(theme)
        ethanol_spectrum(theme)
        orbitals(theme)
        sodium_ie(theme)
        first_ie_periods(theme)
        periodic_blocks(theme)
        ionic_radius(theme)
        paired_boxes(theme)
        melting_period3(theme)
        ie_1_36_log(theme)
    print("done")
