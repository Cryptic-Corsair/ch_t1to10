#!/usr/bin/env python3
"""Topic 6 plates, set C: Hess's Law cycles (combustion data + formation data)."""
from common import shell, svg, text, line, arrow_marker

CARD_CSS = """
.solo{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 12px;margin-top:20px;flex:1;min-height:0}
.solo .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.cycle-strip{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:4px}
.cycle-eq{font-family:'GeistMono',monospace;font-size:14px;font-weight:600;color:var(--ink);
  background:var(--card2);border:1px solid var(--hair);border-radius:9px;padding:9px 16px}
.cycle-eq b{color:var(--acc);font-weight:600}
"""

def box(x, y, w, h, main, sub=None):
    """Species box with hairline border; optional sub-line."""
    out = ('<rect x="%d" y="%d" width="%d" height="%d" rx="11" fill="var(--card2)" '
           'stroke="var(--hair)" stroke-width="1.6"/>' % (x, y, w, h))
    cy = y + (h / 2 + (0 if sub else 5.5))
    out += text(x + w / 2, cy, main, size=15.5, weight=600, color='var(--ink)')
    if sub:
        out += text(x + w / 2, cy + 20, sub, size=11.5, weight=500, color='var(--muted)',
                    family='GeistMono')
    return out

def arr(x1, y1, x2, y2, marker='arwacc'):
    return ('<path d="M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="var(--acc)" '
            'stroke-width="2.6" marker-end="url(#%s)"/>' % (x1, y1, x2, y2, marker))

def alab(x, y, s, size=13.5, color='var(--acc)', anchor='start'):
    return text(x, y, s, size=size, weight=600, color=color, family='GeistMono', anchor=anchor)

def seg_point(x1, y1, x2, y2, t):
    return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)

# NOTE: common.svg() already defines the 'arwacc' (accent) marker in <defs>.

# ------------------------------------------------------ combustion-data cycle ----
def build_hess_combustion(pal):
    W, H = 1120, 372
    inner = ''
    tl = (56, 36, 300, 62)     # C(s, graphite) + 2H2(g)
    tr = (772, 36, 232, 62)    # CH4(g)
    bb = (410, 252, 316, 62)   # CO2(g) + 2H2O(l)
    inner += box(*tl, 'C(s, graphite) + 2H₂(g)', 'elements in their standard states')
    inner += box(*tr, 'CH₄(g)')
    inner += box(*bb, 'CO₂(g) + 2H₂O(l)', 'combustion products')
    # direct route
    inner += arr(tl[0] + tl[2] + 6, tl[1] + tl[3] / 2, tr[0] - 6, tr[1] + tr[3] / 2)
    inner += alab((tl[0] + tl[2] + tr[0]) / 2, tl[1] + 14, 'ΔfH°(CH₄)')
    # down-left arrows (two, parallel) with labels BETWEEN them, clear of the lines
    x1 = tl[0] + 96
    x2 = tl[0] + 190
    p1s, p1e = (x1, tl[1] + tl[3] + 6), (bb[0] + 60, bb[1] - 8)
    p2s, p2e = (x2, tl[1] + tl[3] + 6), (bb[0] + 150, bb[1] - 8)
    inner += arr(*p1s, *p1e)
    inner += arr(*p2s, *p2e)
    m1 = seg_point(*p1s, *p1e, 0.42)
    m2 = seg_point(*p2s, *p2e, 0.42)
    inner += alab(m1[0] - 12, m1[1] + 5, '−394', anchor='end')
    inner += alab(m2[0] + 12, m2[1] + 5, '2 × (−286)', anchor='start')
    # down-right arrow
    x3 = tr[0] + 96
    inner += arr(x3, tr[1] + tr[3] + 6, bb[0] + bb[2] - 80, bb[1] - 8)
    inner += alab(x3 + 14, (tr[1] + tr[3] + bb[1]) / 2 + 4, '−890')
    strip = ('<div class="cycle-strip"><span class="cycle-eq">ΔfH° + (−890) = (−394) + 2 × (−286)'
             ' &nbsp;→&nbsp; <b>ΔfH° = −76 kJ mol⁻¹</b></span></div>')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div>%s</div>'
            % (svg(W, H, inner), strip))
    return shell(1248, 560, pal, 'SPEC 6.6 · HESS’S CYCLE — COMBUSTION DATA',
                 'Formation of methane from combustion enthalpies',
                 body, tag='route through ΔcH°',
                 footer='ΔH[reaction] = Σ ΔcH°[reactants] − Σ ΔcH°[products]. When the products are '
                        'burned, the amount of CO₂ and H₂O produced is the same as when the reactants '
                        'are burned — that is what closes the cycle.',
                 fkey='FORMULA')

# ------------------------------------------------------ formation-data cycle ----
def build_hess_formation(pal):
    W, H = 1120, 372
    inner = ''
    tl = (56, 36, 210, 62)      # CaCO3(s)
    tr = (700, 36, 300, 62)     # CaO(s) + CO2(g)
    bb = (300, 252, 460, 62)    # elements
    inner += box(*tl, 'CaCO₃(s)')
    inner += box(*tr, 'CaO(s) + CO₂(g)')
    inner += box(*bb, 'elements in their standard states', 'Ca(s) + C(s, graphite) + O₂(g)')
    # direct route
    inner += arr(tl[0] + tl[2] + 6, tl[1] + tl[3] / 2, tr[0] - 6, tr[1] + tr[3] / 2)
    inner += alab((tl[0] + tl[2] + tr[0]) / 2, tl[1] + 14, 'ΔrH°')
    # up-left arrow: elements -> CaCO3 (ΔfH of reactant)
    x1 = bb[0] + 70
    inner += arr(x1, bb[1] - 8, tl[0] + 70, tl[1] + tl[3] + 6)
    m1 = seg_point(x1, bb[1] - 8, tl[0] + 70, tl[1] + tl[3] + 6, 0.52)
    inner += alab(m1[0] + 16, m1[1] + 5, '−1207', anchor='start')
    # up-right arrows: elements -> products (ΔfH of products, two parallel)
    x2 = bb[0] + 300
    x3 = bb[0] + 390
    p2s, p2e = (x2, bb[1] - 8), (tr[0] + 110, tr[1] + tr[3] + 6)
    p3s, p3e = (x3, bb[1] - 8), (tr[0] + 200, tr[1] + tr[3] + 6)
    inner += arr(*p2s, *p2e)
    inner += arr(*p3s, *p3e)
    m2 = seg_point(*p2s, *p2e, 0.42)
    m3 = seg_point(*p3s, *p3e, 0.42)
    inner += alab(m2[0] - 12, m2[1] + 5, '−635', anchor='end')
    inner += alab(m3[0] + 12, m3[1] + 5, '−394', anchor='start')
    strip = ('<div class="cycle-strip"><span class="cycle-eq">ΔrH° = [(−635) + (−394)] − (−1207)'
             ' &nbsp;→&nbsp; <b>ΔrH° = +178 kJ mol⁻¹</b></span></div>')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div>%s</div>'
            % (svg(W, H, inner), strip))
    return shell(1248, 560, pal, 'SPEC 6.6 · HESS’S CYCLE — FORMATION DATA',
                 'Decomposition of calcium carbonate from formation enthalpies',
                 body, tag='route through ΔfH°',
                 footer='ΔH[reaction] = Σ ΔfH°[products] − Σ ΔfH°[reactants]. Draw the cycle through '
                        'the elements required to form the reactants and products.',
                 fkey='FORMULA')

HESS_COMBUSTION = ('hess-cycle-combustion', 1248, 560, build_hess_combustion)
HESS_FORMATION = ('hess-cycle-formation', 1248, 560, build_hess_formation)
