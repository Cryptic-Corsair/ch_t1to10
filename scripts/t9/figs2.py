#!/usr/bin/env python3
"""Topic 9 figure plates 7-12 — built on the approved Topic 4/6/7/8 pipeline."""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t9')
from common import shell, svg, line, polyline, arrow, text  # noqa: E402,F401
from figs import GRID_CSS, card, axes2, mb_pts  # noqa: E402


def _duo(pal, kicker, title, tag, footer, fkey, W, H, cards, cls='duo'):
    body = '<style>%s</style><div class="%s">%s</div>' % (GRID_CSS, cls, cards)
    return shell(W, H, pal, kicker, title, body, tag=tag, footer=footer, fkey=fkey)


def _plate(pal, kicker, title, tag, footer, fkey, W, H, body):
    return shell(W, H, pal, kicker, title, body, tag=tag, footer=footer, fkey=fkey)


# ------------------------------------------- 7 · MB curve + temperature ----
def build_mb_temperature(pal):
    W, H = 780, 400
    x0, y0, w, h = 96, 330, 610, 258
    s = axes2(x0, y0, w, h, 'MOLECULAR ENERGY', 'NUMBER OF MOLECULES WITH')
    s += text(x0 - 30, y0 - h / 2 + 30, 'A PARTICULAR ENERGY', 10.5, 'var(--body)', 600, family='GeistMono')
    pts1, tp1 = mb_pts(x0, y0, w, h, b=8.0)
    # b=5 with height 0.625 → same area under the curve (0.625/5 = 1/8), broader + flatter
    pts2, tp2 = mb_pts(x0, y0, w, h * 0.625, b=5.0)
    ea_t = 0.58
    ea_x = x0 + ea_t * w
    # shaded region between T2 and T1 curves beyond Ea
    tail2 = [p for p in pts2 if p[0] >= ea_x - 0.5]
    tail1 = [p for p in pts1 if p[0] >= ea_x - 0.5]
    d = 'M%.1f,%.1f ' % tail2[0] + 'L'.join('%.1f,%.1f ' % p for p in tail2[1:])
    d += 'L'.join('L%.1f,%.1f ' % p for p in reversed(tail1)) + 'Z'
    s += '<path d="%s" fill="var(--accsoft)"/>' % d
    s += polyline(pts2, w=2.6, color='var(--cool)')
    s += polyline(pts1, w=2.8, color='var(--ink)')
    s += line(ea_x, y0, ea_x, y0 - h - 4, w=1.5, color='var(--acc)', dash='5 5')
    s += text(ea_x + 6, y0 - h + 4, 'Ea', 13, 'var(--acc)', 700, anchor='start')
    s += text(x0 + tp1 * w, y0 - h - 12, 'T₁', 15, 'var(--ink)', 700)
    s += text(x0 + tp2 * w, y0 - h * 0.625 - 12, 'T₂', 15, 'var(--cool)', 700)
    s += text(x0 + w - 4, y0 - h - 26, 'TEMPERATURE  T₂ > T₁', 12.5, 'var(--body)', 700,
              family='GeistMono', anchor='end', spacing=1)
    s += arrow(x0 + w - 96, y0 - h + 40, ea_x + 92, y0 - 96, w=1.6, color='var(--acc)', marker='arwacc')
    s += text(x0 + w - 6, y0 - h + 52, 'extra molecules with sufficient', 11.5, 'var(--acc)', 600,
              family='GeistMono', anchor='end')
    s += text(x0 + w - 6, y0 - h + 68, 'energy to overcome the', 11.5, 'var(--acc)', 600, family='GeistMono', anchor='end')
    s += text(x0 + w - 6, y0 - h + 84, 'energy barrier', 11.5, 'var(--acc)', 600, family='GeistMono', anchor='end')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Effect of an increase in temperature on the Maxwell-Boltzmann curve',
                       svg(W, H, s), sig='AREA STAYS CONSTANT'))
    return _plate(pal, 'SPEC 9.4 · TEMPERATURE AND THE CURVE',
                  'Higher temperature — more particles beyond Ea', 'T₂ > T₁',
                  'Curve shifts to the RIGHT, higher energies/velocities · curve gets broader and flatter due to the '
                  'greater spread of values · area under the curve stays constant — corresponds to the total no. of '
                  'particles · neither curve is symmetrical · both curves start at the origin and finish by approaching '
                  'the X axis and do not touch the X axis · the area under both curves is same.',
                  'T₂ > T₁', 1300, 660, body)


# ------------------------------------------------- 8 · reaction profiles ----
def _profile(exo):
    W, H = 480, 320
    x0, y0, w, h = 64, 274, 360, 218
    s = axes2(x0, y0, w, h, 'REACTION CO-ORDINATE', 'ENERGY')
    ry = y0 - 0.66 * h          # reactants level
    py = y0 - (0.22 if exo else 0.90) * h   # products level
    pk = y0 - 1.0 * h * (0.98 if exo else 1.02)
    if not exo:
        pk = y0 - 1.06 * h
    rx1, rx2 = x0 + 26, x0 + 150
    px1, px2 = x0 + 236, x0 + 340
    s += line(x0 + 2, ry, rx2, ry, w=2.2, color='var(--ink)')
    s += line(px1, py, x0 + w - 4, py, w=2.2, color='var(--ink)')
    peak_x = (rx2 + px1) / 2
    s += ('<path d="M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" '
          'stroke="var(--ink)" stroke-width="2.6" stroke-linecap="round"/>'
          % (rx2, ry, rx2 + 40, ry, peak_x - 44, pk, peak_x, pk,
             peak_x + 44, pk, px1 - 40, py, px1, py))
    s += text(x0 + 8, ry - 8, 'reactants', 12, 'var(--body)', 600, anchor='start')
    s += text(x0 + w - 8, py - 8, 'products', 12, 'var(--body)', 600, anchor='end')
    # Ea double arrow: reactants level -> peak
    s += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="var(--acc)" stroke-width="1.8" '
          'marker-start="url(#arwacc)" marker-end="url(#arwacc)"/>' % (peak_x + 36, ry, peak_x + 36, pk + 4))
    s += text(peak_x + 46, (ry + pk) / 2 + 4, 'Ea', 13, 'var(--acc)', 700, anchor='start')
    # ΔH arrow: reactants level -> products level
    hx = x0 + w - 96
    s += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="var(--cool)" stroke-width="1.8" '
          'marker-start="url(#arw)" marker-end="url(#arw)"/>' % (hx, ry, hx, py))
    s += text(hx + 10, (ry + py) / 2 + 4, 'ΔH', 13, 'var(--cool)', 700, anchor='start')
    s += text(W / 2, 20, 'EXOTHERMIC REACTION' if exo else 'ENDOTHERMIC REACTION', 12,
              'var(--acc)' if exo else 'var(--cool)', 700, family='GeistMono', spacing=1.2)
    return svg(W, H, s)


def build_reaction_profiles(pal):
    cards = (card('Exothermic', _profile(True), sig='ΔH NEGATIVE') +
             card('Endothermic', _profile(False), sig='ΔH POSITIVE'))
    body = '<style>%s</style><div class="duo">%s</div>' % (GRID_CSS, cards)
    return _plate(pal, 'SPEC 9.6 · REACTION PROFILE DIAGRAMS',
                  'Energy levels from reactants to products', 'Ea and ΔHr shown',
                  'Reaction profile diagram shows the energy levels of the reactants and the products of the reaction '
                  'and of the transition state that the reactants go through · the activation energy (Ea) and the '
                  'enthalpy change (ΔHr) are also shown on the diagram.',
                  'EXO / ENDO', 1340, 600, body)


# ------------------------------------------ 9 · catalysed vs uncatalysed ----
def build_catalysed_profile(pal):
    W, H = 720, 380
    x0, y0, w, h = 84, 320, 560, 250
    s = axes2(x0, y0, w, h, 'PROGRESS OF REACTION', 'ENERGY')
    ry = y0 - 0.62 * h
    py = y0 - 0.10 * h
    peak_u = y0 - 1.02 * h
    peak_c = y0 - 0.55 * h
    rx2, px1 = x0 + 118, x0 + 320
    mid = (rx2 + px1) / 2
    s += line(x0 + 2, ry, rx2, ry, w=2.2, color='var(--ink)')
    s += line(px1, py, x0 + w - 6, py, w=2.2, color='var(--ink)')
    # uncatalysed (tall, cool)
    s += ('<path d="M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" '
          'stroke="var(--cool)" stroke-width="2.6" stroke-linecap="round"/>'
          % (rx2, ry, rx2 + 42, ry, mid - 52, peak_u, mid, peak_u, mid + 52, peak_u, px1 - 42, py, px1, py))
    # catalysed (short, acc)
    s += ('<path d="M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" '
          'stroke="var(--acc)" stroke-width="2.6" stroke-linecap="round"/>'
          % (rx2, ry, rx2 + 34, ry, mid - 30, peak_c, mid, peak_c, mid + 30, peak_c, px1 - 34, py, px1, py))
    s += text(x0 + 8, ry - 8, 'Reactants', 12.5, 'var(--body)', 600, anchor='start')
    s += text(px1 + 10, py - 8, 'Products', 12.5, 'var(--body)', 600, anchor='start')
    s += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="var(--cool)" stroke-width="1.8" '
          'marker-start="url(#arw)" marker-end="url(#arw)"/>' % (mid + 92, ry, mid + 92, peak_u + 4))
    s += text(mid + 102, (ry + peak_u) / 2 - 6, 'Activation Energy', 11.5, 'var(--cool)', 700, anchor='start')
    s += text(mid + 102, (ry + peak_u) / 2 + 10, 'without catalyst', 11.5, 'var(--cool)', 700, anchor='start')
    s += ('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="var(--acc)" stroke-width="1.8" '
          'marker-start="url(#arwacc)" marker-end="url(#arwacc)"/>' % (mid - 92, ry, mid - 92, peak_c + 4))
    s += text(mid - 102, (ry + peak_c) / 2 - 6, 'Activation Energy', 11.5, 'var(--acc)', 700, anchor='end')
    s += text(mid - 102, (ry + peak_c) / 2 + 10, 'with catalyst', 11.5, 'var(--acc)', 700, anchor='end')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Uncatalysed vs catalysed route between the same reactants and products',
                       svg(W, H, s), sig='LOWER Ea'))
    return _plate(pal, 'SPEC 9.6 · ALTERNATIVE ROUTE',
                  'A catalysed reaction takes a different route', 'same ΔH, lower Ea',
                  'A catalyzed reaction takes place using a different route from the uncatalyzed reaction — the '
                  'catalysed hump is lower, so more collisions succeed.',
                  'LOWER Ea', 1300, 620, body)


# --------------------------------------- 10 · catalysed with intermediate ----
def build_catalyst_intermediate(pal):
    W, H = 720, 390
    x0, y0, w, h = 84, 328, 560, 258
    s = axes2(x0, y0, w, h, 'Progress of reaction', 'Enthalpy, H')
    ry = y0 - 0.58 * h
    py = y0 - 0.10 * h
    peak_u = y0 - 1.04 * h
    peak_c1 = y0 - 0.52 * h
    itm = y0 - 0.30 * h
    peak_c2 = y0 - 0.46 * h
    rx2, px1 = x0 + 96, x0 + 344
    mid = (rx2 + px1) / 2
    s += line(x0 + 2, ry, rx2, ry, w=2.2, color='var(--ink)')
    s += line(px1, py, x0 + w - 6, py, w=2.2, color='var(--ink)')
    # uncatalysed single tall hump
    s += ('<path d="M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" '
          'stroke="var(--cool)" stroke-width="2.4" stroke-linecap="round"/>'
          % (rx2, ry, rx2 + 50, ry, mid - 56, peak_u, mid, peak_u, mid + 56, peak_u, px1 - 50, py, px1, py))
    # catalysed two-step curve with intermediate dip
    s += ('<path d="M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f '
          'C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="none" '
          'stroke="var(--acc)" stroke-width="2.6" stroke-linecap="round"/>'
          % (rx2, ry, rx2 + 28, ry, x0 + 140, peak_c1, x0 + 166, itm,
             x0 + 178, itm, x0 + 204, itm, x0 + 232, itm,
             x0 + 246, peak_c2, x0 + 276, peak_c2, x0 + 300, peak_c2,
             x0 + 322, peak_c2, px1 - 30, py, px1, py))
    s += text(x0 + 6, ry - 8, 'reactants', 12, 'var(--body)', 600, anchor='start')
    s += text(px1 + 10, py - 8, 'products', 12, 'var(--body)', 600, anchor='start')
    s += arrow(x0 + 199, itm + 54, x0 + 199, itm + 8, w=1.4, color='var(--acc)', marker='arwacc')
    s += text(x0 + 208, itm + 62, 'intermediate', 11.5, 'var(--acc)', 700, anchor='start')
    # legend
    s += line(x0 + w - 190, 34, x0 + w - 162, 34, w=3, color='var(--cool)')
    s += text(x0 + w - 154, 38, 'uncatalysed', 11.5, 'var(--body)', 600, anchor='start')
    s += line(x0 + w - 76, 34, x0 + w - 48, 34, w=3, color='var(--acc)')
    s += text(x0 + w - 40, 38, 'catalysed', 11.5, 'var(--body)', 600, anchor='start')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Enthalpy profile diagram for a catalyzed reaction involving the formation of an intermediate',
                       svg(W, H, s), sig='TWO STEPS'))
    return _plate(pal, 'SPEC 9.6 · INTERMEDIATE FORMED WITH THE CATALYST',
                  'At least two steps when an intermediate forms', 'Fe²⁺-catalysed S₂O₈²⁻ + I⁻',
                  'If an intermediate is formed between the reactant and the catalyst then the reaction takes place in at '
                  'least two steps — example: the reaction between peroxydisulphate ions and iodide ions, catalyzed by '
                  'Fe²⁺ ions.',
                  'TWO STEPS', 1300, 630, body)


# --------------------------------------- 11 · MB curve for catalysed ----
def build_mb_catalyst(pal):
    W, H = 780, 380
    x0, y0, w, h = 96, 316, 610, 244
    s = axes2(x0, y0, w, h, 'Energy', 'Number of particles')
    pts, tp = mb_pts(x0, y0, w, h, b=8.0)
    ea_cat = 0.44
    ea_unc = 0.68
    xc = x0 + ea_cat * w
    xu = x0 + ea_unc * w
    tail = [p for p in pts if p[0] >= xc - 0.5]
    d = 'M%.1f,%.1f ' % tail[0] + 'L'.join('%.1f,%.1f ' % p for p in tail[1:])
    d += 'L%.1f,%.1f Z' % (x0 + w, y0)
    s += '<path d="%s" fill="var(--accsoft)"/>' % d
    s += polyline(pts, w=2.8, color='var(--ink)')
    s += line(xc, y0, xc, y0 - h - 6, w=1.5, color='var(--acc)', dash='5 5')
    s += line(xu, y0, xu, y0 - h - 6, w=1.5, color='var(--muted)', dash='5 5')
    s += text(xc, y0 - h - 24, 'WITH', 11, 'var(--acc)', 700, family='GeistMono', anchor='middle', spacing=1)
    s += text(xc, y0 - h - 10, 'CATALYST', 11, 'var(--acc)', 700, family='GeistMono', anchor='middle', spacing=1)
    s += text(xc, y0 + 20, 'Ea', 13, 'var(--acc)', 700)
    s += text(xu, y0 - h - 24, 'WITHOUT', 11, 'var(--muted)', 700, family='GeistMono', anchor='middle', spacing=1)
    s += text(xu, y0 - h - 10, 'CATALYST', 11, 'var(--muted)', 700, family='GeistMono', anchor='middle', spacing=1)
    s += text(xu, y0 + 20, 'Ea', 13, 'var(--muted)', 700)
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Maxwell-Boltzmann distribution curve', svg(W, H, s), sig='LOWER Ea LINE'))
    return _plate(pal, 'SPEC 9.8 · CATALYSTS ON THE DISTRIBUTION',
                  'Lower Ea — more particles can react', 'shaded area grows',
                  'Catalysts provide an alternative pathway with lower activation energy · since activation energy is '
                  'reduced, more particles have sufficient energy for effective collisions · therefore, number of '
                  'effective collisions increases, thus increases the rate of reaction · using catalysts avoids the need '
                  'to supply extra heat — it is safer and cheaper · catalysts remain chemically unchanged at the end of '
                  'the reaction.',
                  'LOWER Ea LINE', 1300, 620, body)


# ------------------------------------- 12 · heterogeneous catalyst stages ----
def build_heterogeneous_catalyst(pal):
    W, H = 380, 240

    def surface():
        s = ''
        for i in range(8):
            for j in range(2):
                s += '<circle cx="%.0f" cy="%.0f" r="13" fill="var(--card2)" stroke="var(--hair)" stroke-width="1.4"/>' % (
                    42 + i * 42, 168 + j * 26)
        return s

    def mol(x, y, r1=13, r2=9, col='var(--cool)'):
        return ('<circle cx="%.0f" cy="%.0f" r="%d" fill="%s" fill-opacity=".85"/>'
                '<circle cx="%.0f" cy="%.0f" r="%d" fill="var(--acc)" fill-opacity=".85"/>'
                % (x, y, r1, col, x + r1 + r2 - 3, y + 2, r2))

    def stage(n):
        s = surface()
        if n == 1:      # adsorption
            s += mol(120, 128)
            s += mol(258, 122)
            s += arrow(96, 66, 114, 112, w=1.6, color='var(--muted)')
            s += arrow(282, 60, 264, 106, w=1.6, color='var(--muted)')
            s += line(133, 142, 130, 154, w=1.6, color='var(--acc)', dash='3 3')
            s += line(271, 136, 268, 154, w=1.6, color='var(--acc)', dash='3 3')
        elif n == 2:    # reaction
            s += mol(150, 128)
            s += mol(226, 128)
            s += arrow(186, 96, 194, 116, w=1.8, color='var(--acc)', marker='arwacc')
            s += arrow(194, 158, 186, 140, w=1.8, color='var(--acc)', marker='arwacc')
            s += text(190, 84, 'just the right orientation', 10.5, 'var(--acc)', 600, family='GeistMono')
        else:           # desorption
            s += mol(190, 118)
            s += arrow(202, 108, 214, 52, w=1.8, color='var(--acc)', marker='arwacc')
            s += text(232, 58, 'products released', 10.5, 'var(--acc)', 600, family='GeistMono', anchor='start')
        return svg(W, H, s)

    subs = ('Gases are adsorbed onto the surface and form weak bonds with metal atoms. Formation of bonds with the '
            'metal may use some of the electrons from bonds within the gas molecules thus weakening these bonds and '
            'making a subsequent reaction easier.',
            'Adsorbed gas molecules may be held on the surface of the metal in just the right orientation for a '
            'reaction to occur. This increases the chances of favourable collisions taking place.',
            'The products are then released from the active sites.')
    cards = ''.join(card('%d · %s' % (i + 1, n), stage(i + 1), sub=subs[i])
                    for i, n in enumerate(('Adsorption', 'Reaction', 'Desorption')))
    body = '<style>%s</style><div class="trio">%s</div>' % (GRID_CSS, cards)
    return _plate(pal, 'SPEC 9.7 · HOW HETEROGENEOUS CATALYSTS WORK',
                  'Active sites on the surface of a solid', 'three stages',
                  'Heterogeneous catalysis takes place at active sites on the surface of a solid (e.g. a metal) — in the '
                  'example, H₂ and C₂H₄ adsorb on the metal surface, the H–H bond breaks and H atoms migrate along the '
                  'surface, and ethane (C₂H₆) desorbs.',
                  'ACTIVE SITES', 1380, 660, body)
