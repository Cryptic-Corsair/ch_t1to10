#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Topic 10 IR figure plates — built from 'Infrared with ans.pdf'.

Four plates rendered through the approved house pipeline:
  t10-ir-vibrations        stretching vs bending (H–O–H)
  t10-ir-examples          butanone · ethanol · propanoic acid · propene
  t10-ir-halides-amines    C–Cl · C–Br · 2° amine · 3° amine (no N–H)
  t10-ir-q1                the three-spectra identification question
"""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t10')
from common import (LIGHT, DARK, shell, svg, line, polyline, arrow, text,  # noqa: E402,F401
                    pts_path)
from figs import GRID_CSS, card  # noqa: E402


# ------------------------------------------------------- mini IR helper ----
def _mini_ir(dips, w=460, h=180, lo=4000, hi=600, baseline=0.84, ah=112):
    """Mini IR spectrum.

    dips: (wavenumber, depth01, sigma, label, color, anchor, level)
      · label/color/anchor/level optional — level 0..2 = 20/36/52 px above
        the baseline; a label without a level sits at its dip bottom.
    Returns (svg_inner, wx, Y0, baseline, ah).
    """
    X0, Y0, AW = 36, 148, w - 72

    def wx(wn):
        return X0 + (lo - wn) / (lo - hi) * AW

    s = line(X0, Y0, X0 + AW, Y0, w=1.5, color='var(--faint)')
    for wn, anch in ((lo, 'start'), (hi, 'end')):
        s += line(wx(wn), Y0, wx(wn), Y0 + 4, w=1.2, color='var(--faint)')
        s += text(wx(wn), Y0 + 17, str(wn), 9.5, 'var(--muted)', 500,
                  anchor=anch, family='GeistMono')
    n = 220
    pts = []
    for i in range(n + 1):
        wn = lo - (lo - hi) * i / n
        t = baseline
        for d in dips:
            t -= d[1] * math.exp(-((wn - d[0]) / d[2]) ** 2)
        pts.append((wx(wn), Y0 - max(t, 0.06) * ah))
    s += polyline(pts, w=2.2, color='var(--ink)')

    LEVEL = (20, 36, 52)
    for d in dips:
        wn, depth, sig = d[0], d[1], d[2]
        label = d[3] if len(d) > 3 else None
        if not label:
            continue
        col = d[4] if len(d) > 4 else 'var(--acc)'
        anchor = d[5] if len(d) > 5 else 'middle'
        lvl = d[6] if len(d) > 6 else None
        x = wx(wn)
        ydip = Y0 - (baseline - depth) * ah
        if lvl is None:                       # at the dip bottom
            s += text(x, ydip - 9, label, 10, col, 600, anchor=anchor)
        else:                                 # floating above the baseline
            y = Y0 - baseline * ah - LEVEL[lvl]
            s += line(x, y + 4, x, ydip - 3, w=1.0, color='var(--faint)')
            s += text(x, y, label, 10, col, 600, anchor=anchor)
    return s, wx, Y0, baseline, ah


# ------------------------------------------------- 1 · stretching/bending ----
def _h2o_art(mode):
    ox, oy = 170, 62
    h1x, h1y, h2x, h2y = 96, 148, 244, 148
    s = line(ox - 13, oy + 10, h1x + 9, h1y - 11, w=2.4, color='var(--ink)')
    s += line(ox + 13, oy + 10, h2x - 9, h2y - 11, w=2.4, color='var(--ink)')
    s += text(ox, oy + 6, 'O', 17, 'var(--ink)', 700)
    s += text(h1x, h1y + 6, 'H', 15, 'var(--ink)', 700)
    s += text(h2x, h2y + 6, 'H', 15, 'var(--ink)', 700)
    if mode == 'sym':
        # both H atoms move out along the bonds at the same time
        s += arrow(126, 118, 102, 144, w=1.8, color='var(--acc)', marker='arwacc')
        s += arrow(214, 118, 238, 144, w=1.8, color='var(--acc)', marker='arwacc')
    elif mode == 'bend':
        # the H atoms move towards and away from each other
        s += arrow(88, 166, 132, 166, w=1.8, color='var(--acc)', marker='arwacc')
        s += arrow(252, 166, 208, 166, w=1.8, color='var(--acc)', marker='arwacc')
    else:  # asym
        s += arrow(126, 118, 102, 144, w=1.8, color='var(--acc)', marker='arwacc')
        s += arrow(226, 136, 202, 112, w=1.8, color='var(--acc)', marker='arwacc')
    return s


def build_vibrations(pal):
    W, H = 1240, 560
    body = ('<style>%s</style>' % GRID_CSS
            + '<div class="trio">'
            + card('Symmetric stretching', svg(340, 190, _h2o_art('sym')), 'STRETCHING',
                   'Both O–H bonds <b>stretch and contract together</b> — the '
                   'molecule grows longer and shorter with the bond angle unchanged.')
            + card('Bending', svg(340, 190, _h2o_art('bend')), 'BENDING',
                   'The bond angle opens and closes — the H atoms move '
                   '<b>towards and away from each other</b>.')
            + card('Asymmetric stretching', svg(340, 190, _h2o_art('asym')), 'STRETCHING',
                   'One bond stretches <b>while the other contracts</b> — the two '
                   'vibrations are out of phase.')
            + '</div>')
    return shell(W, H, pal, 'TOPIC 10 · INFRARED',
                 'Two ways a bond can vibrate', body,
                 tag='10.22',
                 fkey='WHY',
                 footer='Molecules convert energy from infra-red radiation into energy '
                        'to vibrate their bonds — the frequency of vibration is found '
                        'by detecting when the molecules absorb electromagnetic radiation.')


# ------------------------------------------------------ 2 · four families ----
def build_examples(pal):
    W, H = 1240, 820

    def art(dips):
        s, _, _, _, _ = _mini_ir(dips)
        return svg(460, 175, s)

    body = ('<style>%s</style>' % GRID_CSS
            + '<div class="duo">'
            + card('Butanone · CH₃COCH₂CH₃',
                   art([(2950, 0.16, 34, 'C–H 3000–2850', 'var(--muted)', 'middle', 0),
                        (1740, 0.55, 20, 'C=O 1740', 'var(--acc)', 'middle', 0)]),
                   'C=O 1680–1750',
                   'A <b>sharp, strong C=O absorption</b> — aldehydes and ketones '
                   'alike, with the alkyl C–H peaks at 3000 – 2850 cm⁻¹.')
            + card('Ethanol · CH₃CH₂OH',
                   art([(3300, 0.30, 190, 'O–H 3300', 'var(--acc)', 'middle', 0),
                        (2950, 0.14, 34, None),
                        (1010, 0.45, 26, 'C–O 1010', 'var(--acc)', 'middle', 0)]),
                   'O–H 3230–3550',
                   'The <b>broad O–H absorption</b> and the <b>C–O absorption</b> '
                   'appear together — both fingerprints of the alcohol group.')
            + card('Propanoic acid · CH₃CH₂COOH',
                   art([(2900, 0.46, 360, 'very broad O–H', 'var(--acc)', 'middle', 0),
                        (1680, 0.50, 20, 'C=O 1680', 'var(--acc)', 'middle', 0),
                        (1115, 0.30, 1, 'C–O', 'var(--muted)', 'middle', 0),
                        (1200, 0.28, 22, None),
                        (1030, 0.33, 20, None)]),
                   'O–H 2500–3500',
                   'A <b>very broad O–H absorption</b> reaching down to 2500 cm⁻¹, '
                   'plus C=O at 1680 cm⁻¹ and C–O absorptions at 1200 and 1030 cm⁻¹.')
            + card('Propene · CH₃CH=CH₂',
                   art([(3050, 0.20, 30, '=C–H 3100–3000', 'var(--muted)', 'middle', 0),
                        (1660, 0.42, 22, 'C=C 1669–1645', 'var(--acc)', 'middle', 0)]),
                   'C=C 1669–1645',
                   'The <b>C=C stretch</b> and the <b>=C–H stretch</b> — the double '
                   'bond shows both.')
            + '</div>')
    return shell(W, H, pal, 'TOPIC 10 · INFRARED',
                 'Four spectra to recognise on sight', body,
                 tag='10.22',
                 fkey='READ',
                 footer='An infra-red spectrum is particularly useful for identifying '
                        'the C=O and the O–H bonds in compounds — the broadness of the '
                        'O–H dip separates the acid from the alcohol.')


# ------------------------------------------------ 3 · halides and amines ----
def build_halides_amines(pal):
    W, H = 1240, 820

    def art(dips, extra=''):
        s, wx, Y0, base, ah = _mini_ir(dips)
        return svg(460, 175, s + extra)

    tri_extra = text(230, 148 - 0.84 * 112 + 22, 'no N–H stretch', 10, 'var(--acc)', 600)

    body = ('<style>%s</style>' % GRID_CSS
            + '<div class="duo">'
            + card('1-chloro-2-methylpropane',
                   art([(2976, 0.34, 40, 'C–H stretch 2976', 'var(--muted)', 'middle', 0),
                        (1271, 0.22, 30, 'C–H wag 1271', 'var(--muted)', 'middle', 0),
                        (743, 0.30, 16, 'C–Cl 743', 'var(--acc)', 'middle', 1)]),
                   'C–Cl 800–600',
                   'The <b>C–Cl stretches absorb at 743 cm⁻¹</b>; the C–H wag '
                   '(–CH₂X) at 1271 cm⁻¹ is seen <b>only in terminal alkyl halides</b>.')
            + card('1-bromopropane',
                   art([(2976, 0.40, 40, 'C–H stretch', 'var(--muted)', 'middle', 0),
                        (1230, 0.26, 30, 'C–H wag 1230', 'var(--muted)', 'middle', 0),
                        (651, 0.38, 16, 'C–Br 651', 'var(--acc)', 'middle', 1)]),
                   'C–Br 690–515',
                   'The <b>C–Br stretch absorbs at 651 cm⁻¹</b>. C–H stretches are '
                   '<b>not specific</b> to alkyl halides.')
            + card('Diethylamine · a 2° amine',
                   art([(3288, 0.45, 55, 'N–H 3288', 'var(--acc)', 'middle', 0),
                        (2969, 0.40, 40, 'C–H', 'var(--muted)', 'middle', 1),
                        (1143, 0.30, 26, 'C–N 1143', 'var(--muted)', 'middle', 0),
                        (733, 0.25, 18, 'N–H wag 733', 'var(--muted)', 'middle', 1)]),
                   '2° · ONE N–H BAND',
                   'A secondary amine — <b>one N–H band</b> (3350 – 3310 cm⁻¹), the '
                   'C–N stretch and the N–H wag.')
            + card('Triethylamine · a 3° amine',
                   art([(2969, 0.50, 40, 'C–H', 'var(--muted)', 'middle', 0),
                        (1214, 0.35, 26, 'C–N 1214', 'var(--muted)', 'middle', 0)], tri_extra),
                   '3° · NO N–H BANDS',
                   'A tertiary amine — <b>note the absence of an N–H stretch</b>. '
                   'Only the C–N stretch shows where the nitrogen is.')
            + '</div>')
    return shell(W, H, pal, 'TOPIC 10 · INFRARED',
                 'C–X below 850 · the N–H region counts the hydrogens', body,
                 tag='10.22',
                 fkey='PATTERN',
                 footer='C–X stretches: C–F 1400–1000 · C–Cl 800–600 · C–Br 600–500 · '
                        'C–I about 500. N–H stretch 3400–3250: two bands (1°), one '
                        'band (2°), none (3°).')


# ------------------------------------------------------- 4 · question one ----
def build_q1(pal):
    W, H = 1240, 560

    def art(dips):
        s, _, _, _, _ = _mini_ir(dips, w=300, h=170)
        return svg(300, 170, s)

    body = ('<style>%s</style>' % GRID_CSS
            + '<div class="trio">'
            + card('Spectrum A',
                   art([(2900, 0.42, 300, 'very broad O–H', 'var(--acc)', 'middle', 0),
                        (1680, 0.48, 20, 'C=O 1680', 'var(--acc)', 'middle', 0),
                        (1050, 0.34, 30, 'C–O', 'var(--muted)', 'middle', 1)]),
                   '3500 – 2500',
                   'A <b>very broad dip</b> reaching down to 2500 cm⁻¹, with a sharp '
                   'dip near 1700 and C–O absorptions.')
            + card('Spectrum B',
                   art([(3000, 0.32, 36, 'C–H 3000', 'var(--muted)', 'middle', 0),
                        (1700, 0.58, 20, 'C=O 1700', 'var(--acc)', 'middle', 0)]),
                   'SHARP AT 1700',
                   'A <b>sharp strong dip near 1700</b> and C–H at 3000 — and '
                   '<b>no O–H anywhere</b>.')
            + card('Spectrum C',
                   art([(3300, 0.38, 150, 'O–H 3200–3500', 'var(--acc)', 'middle', 0),
                        (3000, 0.28, 34, None),
                        (1010, 0.48, 24, 'C–O 1010', 'var(--acc)', 'middle', 0)]),
                   'BROAD AT 3300',
                   'A <b>broad dip at 3300</b> with C–H at 3000 and a C–O at '
                   '1010 cm⁻¹ — and no C=O.')
            + '</div>')
    return shell(W, H, pal, 'TOPIC 10 · INFRARED',
                 'Butanal, propanoic acid and butan-1-ol — in some order', body,
                 tag='10.22',
                 fkey='MATCH',
                 footer='Match each spectrum against the absorption table — shape '
                        'first (broad vs sharp), then wavenumber.')
