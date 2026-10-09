#!/usr/bin/env python3
"""Topic 6 plates, set D: bond enthalpy (CH4 sequential dissociation + H2O(g) cycle)."""
from common import shell, svg, text, line
from figs_c import CARD_CSS, box, arr, alab, seg_point

# ------------------------------------------------------- CH4 dissociation ----
DIRS = {'N': (0, -44), 'E': (44, 0), 'S': (0, 44), 'W': (-44, 0)}

def h_glyph(cx, cy, dx, dy, faded=False):
    """One H atom attached to a central C at (cx,cy), offset (dx,dy)."""
    op = '0.32' if faded else '1'
    dash = ' stroke-dasharray="3 3"' if faded else ''
    out = line(cx, cy, cx + dx * 0.62, cy + dy * 0.62, w=2.4 if not faded else 2.0,
               color='var(--body)' if not faded else 'var(--muted)',
               dash='3 3' if faded else None)
    out += ('<g opacity="%s"><circle cx="%.1f" cy="%.1f" r="13" fill="var(--card2)" '
            'stroke="var(--muted)" stroke-width="1.8"%s/>' % (op, cx + dx, cy + dy, dash))
    out += text(cx + dx, cy + dy + 4.5, 'H', size=12.5, weight=600, color='var(--body)')
    out += '</g>'
    return out

def species(cx, cy, keep, leaving):
    """Central C with kept H atoms; optional faded H that is leaving."""
    out = ''
    for d in keep:
        dx, dy = DIRS[d]
        out += h_glyph(cx, cy, dx, dy)
    if leaving:
        dx, dy = DIRS[leaving]
        out += h_glyph(cx, cy, dx, dy, faded=True)
    out += ('<circle cx="%.1f" cy="%.1f" r="15.5" fill="var(--card2)" '
            'stroke="var(--ink)" stroke-width="2"/>' % (cx, cy))
    out += text(cx, cy + 5, 'C', size=14.5, weight=700, color='var(--ink)')
    return out

def build_dissociation(pal):
    W, H = 1120, 268
    inner = ''
    # transition i removes leave[i] from species i
    leave = ['E', 'W', 'S', 'N']
    keeps = [['N', 'E', 'S', 'W'], ['N', 'S', 'W'], ['N', 'S'], ['N'], []]
    labels = ['CH₄(g)', 'CH₃(g)', 'CH₂(g)', 'CH(g)', 'C(g)']
    values = ['+423', '+480', '+425', '+335']
    xs = [110, 345, 580, 815, 1050]
    cy = 108
    for i, cx in enumerate(xs):
        leaving = leave[i] if i < 4 else None
        inner += species(cx, cy, keeps[i], leaving)
        inner += text(cx, cy + 76, labels[i], size=14, weight=600, color='var(--ink)')
        if i < 4:
            x1 = cx + 74
            x2 = xs[i + 1] - 74
            inner += arr(x1, cy, x2, cy, marker='arwacc')
            inner += text((x1 + x2) / 2, cy - 14, '+ H(g)', size=12, weight=500,
                          color='var(--muted)', family='GeistMono')
            inner += text((x1 + x2) / 2, cy + 30, values[i], size=14.5, weight=700,
                          color='var(--acc)')
    strip = ('<div class="cycle-strip" style="margin-top:14px"><span class="cycle-eq">'
             'E(C–H) = (423 + 480 + 425 + 335) ÷ 4 = 415.75 &nbsp;≈&nbsp; '
             '<b>+416 kJ mol⁻¹</b></span></div>')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div>%s</div>' % (svg(W, H, inner), strip))
    return shell(1248, 500, pal, 'SPEC 6.9 · BOND ENTHALPY',
                 'The four C–H bonds of methane break one at a time',
                 body, tag='ΔBH, stepwise',
                 footer='Each successive bond breaks with a different enthalpy because the strength '
                        'of a bond depends on its environment — so MEAN values are quoted. The C–H '
                        'bond in different compounds has slightly different values, so an average is '
                        'used.',
                 fkey='WHY MEANS')

# --------------------------------------------------------- H2O(g) cycle ----
def build_bond_cycle(pal):
    W, H = 1120, 372
    inner = ''
    tl = (56, 36, 300, 62)     # H2(g) + 1/2 O2(g)
    tr = (772, 36, 232, 62)    # H2O(g)
    bb = (410, 252, 316, 62)   # 2H(g) + O(g)
    inner += box(*tl, 'H₂(g) + ½O₂(g)', 'reactant bonds to be broken')
    inner += box(*tr, 'H₂O(g)')
    inner += box(*bb, '2H(g) + O(g)', 'gaseous atoms')
    # direct route
    inner += arr(tl[0] + tl[2] + 6, tl[1] + tl[3] / 2, tr[0] - 6, tr[1] + tr[3] / 2)
    inner += alab((tl[0] + tl[2] + tr[0]) / 2, tl[1] + 14, 'ΔHr°')
    # down arrows: break reactant bonds, labels BETWEEN the arrows
    x1 = tl[0] + 96
    x2 = tl[0] + 190
    p1s, p1e = (x1, tl[1] + tl[3] + 6), (bb[0] + 60, bb[1] - 8)
    p2s, p2e = (x2, tl[1] + tl[3] + 6), (bb[0] + 150, bb[1] - 8)
    inner += arr(*p1s, *p1e)
    inner += arr(*p2s, *p2e)
    m1 = seg_point(*p1s, *p1e, 0.42)
    m2 = seg_point(*p2s, *p2e, 0.42)
    inner += alab(m1[0] - 12, m1[1] + 5, 'E(H–H) = +436', anchor='end')
    inner += alab(m2[0] + 12, m2[1] + 5, '½E(O=O) = +249', anchor='start')
    # up arrow: form product bonds
    x3 = tr[0] + 96
    inner += arr(bb[0] + bb[2] - 80, bb[1] - 8, x3, tr[1] + tr[3] + 6)
    m3 = seg_point(bb[0] + bb[2] - 80, bb[1] - 8, x3, tr[1] + tr[3] + 6, 0.42)
    inner += alab(m3[0] + 12, m3[1] + 5, '2E(O–H) = +924', anchor='start')
    strip = ('<div class="cycle-strip"><span class="cycle-eq">ΔHr° = 436 + 249 − 924'
             ' &nbsp;→&nbsp; <b>ΔHr° = −239 kJ mol⁻¹</b></span></div>')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div>%s</div>'
            % (svg(W, H, inner), strip))
    return shell(1248, 560, pal, 'SPEC 6.9 – 6.10 · BOND-ENTHALPY CYCLE',
                 'Formation of gaseous water through gaseous atoms',
                 body, tag='route through E(bonds)',
                 footer='ΔH[reaction] = Σ E[reactants] − Σ E[products] — break all the reactant bonds, '
                        'then form all the product bonds. Bond enthalpies are measured in the gaseous '
                        'state only, and they are mean values — so the result differs from the true '
                        'measured ΔH.',
                 fkey='FORMULA')

DISSOCIATION = ('bond-dissociation-ch4', 1248, 500, build_dissociation)
BOND_CYCLE = ('bond-enthalpy-cycle', 1248, 560, build_bond_cycle)
