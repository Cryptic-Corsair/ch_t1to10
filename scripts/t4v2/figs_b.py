#!/usr/bin/env python3
"""Topic 4 v2 — plates: chain isomers of the alkanes, cycloalkane ring isomers."""
import math
from common import (shell, svg, text, line, polyline, zig, poly, COS30, SIN30)

def bond_svg(pts_or_lines, w=3.0):
    out = ''
    for seg in pts_or_lines:
        out += polyline(seg, w=w) if len(seg) > 2 else line(seg[0][0], seg[0][1], seg[1][0], seg[1][1], w=w)
    return out

def segs_from_verts(verts, extra=None):
    """segments: chain polyline + optional extra single-bond segments."""
    segs = [verts]
    if extra:
        segs += extra
    return segs

def place(w, h, segs, w_stroke=3.0):
    """Center a set of segments (abs coords from generators) into an svg box."""
    xs = [pt[0] for s in segs for pt in s]
    ys = [pt[1] for s in segs for pt in s]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    inner = ''
    for s in segs:
        if len(s) > 2:
            moved = [(p[0] - cx + w / 2, p[1] - cy + h / 2) for p in s]
            inner += polyline(moved, w=w_stroke)
        else:
            (a, b) = s
            inner += line(a[0] - cx + w / 2, a[1] - cy + h / 2,
                          b[0] - cx + w / 2, b[1] - cy + h / 2, w=w_stroke)
    return svg(w, h, inner)

# ---------------------------------------------------------- structures ----
def st_butane(L=46):
    return segs_from_verts(zig(0, 0, 4, L=L))

def st_2methylpropane(L=46):
    c = (0, 0)
    up = (0, -L); dl = (-L * COS30, L * SIN30); dr = (L * COS30, L * SIN30)
    return [[c, up], [c, dl], [c, dr]]

def st_pentane(L=46):
    return segs_from_verts(zig(0, 0, 5, L=L))

def st_2methylbutane(L=46):
    v = zig(0, 0, 4, L=L)
    c2 = v[1]
    return segs_from_verts(v, [[c2, (c2[0], c2[1] - L)]])

def st_neopentane(L=46):
    return [[(0, -L), (0, L)], [(-L, 0), (L, 0)]]

def st_hexane(L=46):
    return segs_from_verts(zig(0, 0, 6, L=L))

def st_2methylpentane(L=46):
    v = zig(0, 0, 5, L=L)
    c2 = v[1]
    return segs_from_verts(v, [[c2, (c2[0], c2[1] - L)]])

def st_3methylpentane(L=46):
    v = zig(0, 0, 5, L=L)
    c3 = v[2]
    return segs_from_verts(v, [[c3, (c3[0], c3[1] + L)]])

def st_22dimethylbutane(L=46):
    v = zig(0, 0, 4, L=L)
    c2 = v[1]
    m1 = (c2[0] - L * COS30, c2[1] - L * SIN30)
    m2 = (c2[0] + L * COS30, c2[1] - L * SIN30)
    return segs_from_verts(v, [[c2, m1], [c2, m2]])

def st_23dimethylbutane(L=46):
    v = zig(0, 0, 4, L=L)
    c2, c3 = v[1], v[2]
    return segs_from_verts(v, [[c2, (c2[0], c2[1] - L)], [c3, (c3[0], c3[1] + L)]])

# ------------------------------------------------------------------ plate ----
def build_alkane_isomers(pal):
    css = """
.ai-band{display:grid;grid-template-columns:170px 1fr;gap:18px;align-items:center;
  padding:15px 0;border-top:1px solid var(--faint)}
.ai-band:first-child{border-top:none;padding-top:2px}
.ai-rail{display:flex;flex-direction:column;gap:9px;align-items:flex-start}
.ai-formula{font-family:'GeistMono',monospace;font-weight:600;font-size:17px;color:var(--ink)}
.ai-cells{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:10px;min-width:0}
.ai-cell{display:flex;flex-direction:column;align-items:center;gap:5px;padding:8px 4px 6px;
  border:1px solid var(--faint);border-radius:12px;background:var(--card)}
.ai-name{font-size:13px;font-weight:500;color:var(--muted);white-space:nowrap}
.ai-cells.sm .ai-name{font-size:11.3px}
.ai-wrap{flex:1;display:flex;flex-direction:column;justify-content:space-evenly}
"""
    bands = [
        ('C<sub>4</sub>H<sub>10</sub>', '2 ISOMERS', 200, 132, 46, 3.0, '',
         [('butane', st_butane), ('2-methylpropane', st_2methylpropane)]),
        ('C<sub>5</sub>H<sub>12</sub>', '3 ISOMERS', 200, 132, 46, 3.0, '',
         [('pentane', st_pentane), ('2-methylbutane', st_2methylbutane),
          ('2,2-dimethylpropane', st_neopentane)]),
        ('C<sub>6</sub>H<sub>14</sub>', '5 ISOMERS', 150, 96, 33, 2.6, 'sm',
         [('hexane', st_hexane), ('2-methylpentane', st_2methylpentane),
          ('3-methylpentane', st_3methylpentane), ('2,2-dimethylbutane', st_22dimethylbutane),
          ('2,3-dimethylbutane', st_23dimethylbutane)]),
    ]
    html = ''
    for formula, count, cw, ch, L, stroke, sm, cells in bands:
        cell_html = ''
        for name, fn in cells:
            cell_html += ('<div class="ai-cell">%s<span class="ai-name">%s</span></div>'
                          % (place(cw, ch, fn(L=L), w_stroke=stroke), name))
        html += ('<div class="ai-band"><div class="ai-rail">'
                 '<span class="ai-formula">%s</span><span class="chip acc">%s</span></div>'
                 '<div class="ai-cells %s">%s</div></div>' % (formula, count, sm, cell_html))
    body = ('<style>%s</style><div class="ai-wrap">%s</div>' % (css, html))
    return shell(1248, 960, pal, 'SPEC 4.11 · CHAIN ISOMERS',
                 'Same formula, different skeletons', body,
                 footer='Enumerate systematically: draw the straight chain, shorten it and place '
                        'methyl branches at every distinct position — then cross out duplicates. '
                        'Every carbon must still show exactly four bonds.', fkey='METHOD')

# ---------------------------------------------------------- cycloalkanes ----
def ring_svg(n, r, methyl=False, L=44, w=210, h=150):
    pts = poly(0, 0, n, r)
    inner = polyline(pts + [pts[0]], w=3.0)
    top = min(pts, key=lambda p: p[1])
    if methyl:
        inner += line(top[0], top[1], top[0], top[1] - L, w=3.0)
    inner = '<g transform="translate(%.1f,%.1f)">' % (w / 2, h / 2 + (10 if methyl else 0)) + inner + '</g>'
    return svg(w, h, inner)

def build_cyclo(pal):
    css = """
.cy-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;flex:1;align-content:center}
.cy-cell{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;padding:14px 8px}
.cy-name{font-size:13px;font-weight:500;color:var(--body);white-space:nowrap}
.cy-rows{display:flex;flex-direction:column;gap:8px;align-items:center}
"""
    cells = [
        ('cyclopropane', 'C<sub>3</sub>H<sub>6</sub>', ring_svg(3, 36)),
        ('cyclobutane', 'C<sub>4</sub>H<sub>8</sub>', ring_svg(4, 44)),
        ('methylcyclopropane', 'C<sub>4</sub>H<sub>8</sub>', ring_svg(3, 34, methyl=True)),
        ('cyclopentane', 'C<sub>5</sub>H<sub>10</sub>', ring_svg(5, 46)),
        ('methylcyclobutane', 'C<sub>5</sub>H<sub>10</sub>', ring_svg(4, 42, methyl=True)),
    ]
    grid = ''
    for name, formula, ring in cells:
        grid += ('<div class="cy-cell"><div class="cy-rows">%s</div>'
                 '<span class="cy-name">%s</span><span class="chip">%s</span></div>'
                 % (svg(210, 148, ring), name, formula))
    body = '<style>%s</style><div class="cy-grid">%s</div>' % (css, grid)
    return shell(1248, 576, pal, 'SPEC 4.9 & 4.11 · RING ISOMERS',
                 'Vary the ring, then the substituents', body,
                 footer='A ring needs at least three carbons — cyclopropane is the smallest. '
                        'For C<sub>5</sub>H<sub>10</sub> the list keeps going: ethylcyclopropane, '
                        '1,1- and 1,2-dimethylcyclopropane — the guide\u2019s examples are not exhaustive.',
                 fkey='NOTE')

ALKANE = ('alkane-isomers', 1248, 960, build_alkane_isomers)
CYCLO = ('cycloalkane-isomers', 1248, 576, build_cyclo)
