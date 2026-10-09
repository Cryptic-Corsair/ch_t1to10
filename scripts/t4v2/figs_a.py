#!/usr/bin/env python3
"""Topic 4 v2 — plates: hazard pictograms, formula types, skeletal heteroatom."""
import math
from common import (shell, svg, text, line, polyline, pts_path, wavy, fishhook,
                    arrow, zig, poly)

# ------------------------------------------------------------- pictograms ----
def flame(color='var(--pic)', s=1.0, dx=0.0, dy=0.0):
    """Classic GHS flame silhouette, 100-box coordinates. Scales about its own centre."""
    d = ("M50,16 C54,26 63,33 65,45 C67,57 60,68 50,68 C40,68 33,57 35,45 "
         "C36,39 40,35 42,30 C43,35 45,37 46,38 C46,30 48,23 50,16 Z")
    d2 = ("M50,42 C54,47 56,51 54,57 C52,62 48,62 46,57 C44,51 46,47 50,42 Z")
    g = '<g transform="translate(%.1f,%.1f) scale(%.3f) translate(-50,-42)">' % (50 + dx, 42 + dy, s)
    return (g + '<path d="%s" fill="%s"/>' % (d, color)
            + '<path d="%s" fill="var(--diafill)"/>' % d2 + '</g>')

def drop(cx, cy, r=3.2, color='var(--pic)'):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, color)

def pict_flammable():
    return (flame(s=1.02, dy=1)
            + line(28, 80, 72, 80, w=6, color='var(--pic)'))

def pict_toxic():
    out = ''
    # crossbones behind
    out += line(26, 28, 74, 72, w=7, color='var(--pic)')
    out += line(74, 28, 26, 72, w=7, color='var(--pic)')
    for x, y in ((26, 28), (74, 28), (26, 72), (74, 72)):
        out += '<circle cx="%d" cy="%d" r="5" fill="var(--pic)"/>' % (x, y)
    # skull
    out += ('<path d="M50,20 C64,20 73,30 73,43 C73,52 68,58 63,61 L63,70 '
            'L37,70 L37,61 C32,58 27,52 27,43 C27,30 36,20 50,20 Z" fill="var(--pic)"/>')
    out += '<circle cx="41.5" cy="44" r="6.2" fill="var(--diafill)"/>'
    out += '<circle cx="58.5" cy="44" r="6.2" fill="var(--diafill)"/>'
    out += '<path d="M50,50 L54,57 L46,57 Z" fill="var(--diafill)"/>'
    out += line(47, 61, 47, 68, w=2.6, color='var(--diafill)', cap='butt')
    out += line(53, 61, 53, 68, w=2.6, color='var(--diafill)', cap='butt')
    return out

def pict_corrosive():
    out = ''
    # two tilted pouring tubes
    out += line(33, 13, 26, 33, w=8, color='var(--pic)')
    out += line(67, 13, 74, 33, w=8, color='var(--pic)')
    out += drop(25, 43) + drop(24, 52, 2.6)
    out += drop(75, 43) + drop(76, 52, 2.6)
    # corroded surface bar (left) with a bite taken out
    out += line(23, 71, 33, 71, w=5.5, color='var(--pic)')
    out += line(43, 71, 53, 71, w=5.5, color='var(--pic)')
    out += drop(38, 75, 2.2)
    # hand (right)
    out += ('<path d="M61,66 L80,66 C83.3,66 86,68.7 86,72 L86,73 C86,76.3 83.3,79 '
            '80,79 L59,79 C56,79 54,77 54,74.5 C54,70 57,66 61,66 Z" fill="var(--pic)"/>')
    out += ('<path d="M59,66 C58,61 62.5,59.6 64.5,61.8 C66,63.4 66.5,66 66.5,66 Z" fill="var(--pic)"/>')
    return out

def pict_irritant():
    return (line(50, 24, 50, 57, w=10.5, color='var(--pic)')
            + '<circle cx="50" cy="74" r="6.4" fill="var(--pic)"/>')

def pict_oxidising():
    return (flame(s=0.76, dy=-15)
            + '<circle cx="50" cy="66" r="13.5" fill="none" stroke="var(--pic)" stroke-width="6.5"/>')

def pict_environmental():
    out = ''
    # dead tree
    out += line(46, 50, 46, 22, w=4.6, color='var(--pic)')
    out += line(46, 30, 37, 21, w=3.6, color='var(--pic)')
    out += line(46, 36, 55, 27, w=3.6, color='var(--pic)')
    out += line(46, 43, 38, 37, w=3.6, color='var(--pic)')
    out += line(46, 41, 54, 35, w=3.6, color='var(--pic)')
    # fish
    out += ('<path d="M54,60 C60,54.5 70,54.5 77,60 C70,65.5 60,65.5 54,60 Z" fill="var(--pic)"/>')
    out += '<path d="M54,60 L47,55 L47,65 Z" fill="var(--pic)"/>'
    out += '<circle cx="72.5" cy="59" r="1.7" fill="var(--diafill)"/>'
    # water line
    out += ('<path d="M30,71 Q35,67 40,71 T50,71 T60,71 T70,71 T80,71" fill="none" '
            'stroke="var(--pic)" stroke-width="3.4" stroke-linecap="round"/>')
    return out

def diamond(pict, size=168):
    return ('<div class="dm-wrap"><div class="dm"></div>'
            '<div class="dm-pic">%s</div></div>' % svg(96, 96, pict))

HAZARD_CSS = """
.hz-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;flex:1;align-content:center}
.hz-cell{display:flex;flex-direction:column;align-items:center;gap:14px}
.dm-wrap{position:relative;width:%dpx;height:%dpx}
.dm{position:absolute;left:50%%;top:50%%;width:71%%;height:71%%;transform:translate(-50%%,-50%%) rotate(45deg);
  background:var(--diafill);border:5.5px solid var(--diaedge);border-radius:13px}
.dm-pic{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.dm-pic svg{width:66%%;height:66%%}
.hz-name{font-weight:600;font-size:14px;color:var(--ink);letter-spacing:-.01em}
""" 

def build_hazard(pal):
    names = [('Flammable', pict_flammable), ('Toxic', pict_toxic),
             ('Corrosive', pict_corrosive), ('Irritant', pict_irritant),
             ('Oxidising', pict_oxidising), ('Environmental', pict_environmental)]
    cells = ''
    for label, fn in names:
        cells += ('<div class="hz-cell">%s<span class="hz-name">%s</span></div>'
                  % (diamond(fn()), label))
    css = HAZARD_CSS % (168, 168)
    body = '<style>%s</style><div class="hz-grid">%s</div>' % (css, cells)
    return shell(1248, 480, pal, 'SPEC 4.1 – 4.2 · HAZARD AND RISK',
                 'The six hazard pictograms',
                 body, tag='know them on sight',
                 footer='The appearance of the symbol is itself the mark — pick the correct '
                        'pictogram for the hazard described, and quote the hazard it signals.',
                 fkey='EXAM')

# ------------------------------------------------------------ formula types ----
def displayed_butane():
    """Every bond drawn AND every atom labelled — the textbook displayed formula."""
    inner = ''
    ys = 78
    xs = [50, 116, 182, 248]
    hb = 30   # label offset from chain
    trim = 10  # bonds stop short of letter glyphs
    for i in range(3):
        inner += line(xs[i] + trim, ys, xs[i + 1] - trim, ys, w=2.6)
    for i, x in enumerate(xs):
        end = i in (0, 3)
        # vertical H bonds (trimmed at C)
        inner += line(x, ys - trim, x, ys - hb + 6, w=2.6)
        inner += line(x, ys + trim, x, ys + hb - 6, w=2.6)
        inner += text(x, ys - hb + 1, 'H', size=15, weight=600)
        inner += text(x, ys + hb + 5, 'H', size=15, weight=600)
        if end:
            sgn = -1 if i == 0 else 1
            inner += line(x + sgn * trim, ys, x + sgn * (hb - 6), ys, w=2.6)
            inner += text(x + sgn * hb, ys + 5.5, 'H', size=15, weight=600)
        inner += text(x, ys + 5.5, 'C', size=15, weight=600)
    return svg(300, 160, inner)

def skeletal_butane_annotated():
    pts = zig(75, 92, 4, L=54)
    inner = polyline(pts, w=3.2)
    # 120-degree arc annotation at vertex 2
    v = pts[2]
    inner += ('<path d="M%.1f,%.1f A40,40 0 0 1 %.1f,%.1f" fill="none" stroke="var(--acc)" '
              'stroke-width="1.6" stroke-dasharray="3,3"/>'
              % (v[0] - 34, v[1] - 20, v[0] + 34, v[1] - 20))
    inner += text(v[0], v[1] - 46, '120°', size=12, color='var(--acc)', weight=600,
                  family='GeistMono', spacing=0.5)
    return svg(290, 160, inner)

def build_formula(pal):
    card_css = """
.f-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;flex:1;margin-top:22px}
.f-card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  padding:16px 16px 13px;display:flex;flex-direction:column}
.f-kick{font-family:'GeistMono',monospace;font-size:10px;font-weight:600;color:var(--acc);
  letter-spacing:.16em;text-transform:uppercase}
.f-zone{flex:1;display:flex;align-items:center;justify-content:center}
.f-zone .big{font-size:40px;font-weight:600;color:var(--ink);letter-spacing:-.01em}
.f-zone .mid{font-size:19px;font-weight:600;color:var(--ink);letter-spacing:.01em;white-space:nowrap}
.f-cap{border-top:1px solid var(--faint);padding-top:9px;font-size:12px;line-height:1.45;
  color:var(--muted);min-height:56px}
"""
    mol = '<div class="big">C<sub>4</sub>H<sub>10</sub></div>'
    struct = '<div class="mid">CH<sub>3</sub>—CH<sub>2</sub>—CH<sub>2</sub>—CH<sub>3</sub></div>'
    caps = ['the actual count of atoms of each element — says nothing about connectivity',
            'the arrangement written carbon by carbon, bonds implied',
            'every single bond drawn as a line — atoms at line ends and joins',
            'only the carbon backbone — each line end and vertex is a carbon']
    kicks = ['Molecular', 'Structural', 'Displayed', 'Skeletal']
    zones = [mol, struct, displayed_butane(), skeletal_butane_annotated()]
    cards = ''
    for k, z, c in zip(kicks, zones, caps):
        cards += ('<div class="f-card"><div class="f-kick">%s</div>'
                  '<div class="f-zone">%s</div><div class="f-cap">%s</div></div>' % (k, z, c))
    body = ('<style>%s</style><div class="f-grid">%s</div>' % (card_css, cards))
    return shell(1280, 704, pal, 'SPEC 4.5 · THE TYPES OF FORMULA',
                 'Butane, drawn four ways', body, tag='C₄H₁₀',
                 footer='Molecular and structural formulae are written as text; displayed and '
                        'skeletal are drawings. The general formula C<sub>n</sub>H<sub>2n+2</sub> '
                        'describes the whole alkane series.', fkey='4.5')

# ------------------------------------------------------- skeletal heteroatom ----
def butan2ol_drawing():
    inner = ''
    L = 84
    dx, dy = L * math.cos(math.radians(30)), L * math.sin(math.radians(30))
    c1 = (128, 268); c2 = (c1[0] + dx, c1[1] - dy); c3 = (c2[0] + dx, c1[1]); c4 = (c3[0] + dx, c2[1])
    inner += polyline([c1, c2, c3, c4], w=3.6)
    # O–H drawn in full from C2
    o = (c2[0], c2[1] - L)
    h = (o[0] + 50, o[1] - 30)
    inner += line(c2[0], c2[1], o[0], o[1] + 14, w=3.6)
    inner += text(o[0], o[1] + 14, 'O', size=34, color='var(--oz)', weight=600)
    inner += line(o[0] + 16, o[1] - 2, h[0] - 12, h[1] + 9, w=3.6)
    inner += text(h[0] + 2, h[1] + 11, 'H', size=30, color='var(--oz)', weight=600)

    def note(lx, ly, sx, sy, s, anchor='start', dot='var(--muted)', w=1.3, ty=None):
        return (line(lx, ly, sx, sy, w=w, color=dot, dash='2,4')
                + '<circle cx="%.1f" cy="%.1f" r="2.8" fill="%s"/>' % (lx, ly, dot)
                + text(sx, ty if ty is not None else sy - 6, s, size=12.5, color=dot,
                       weight=500, family='GeistMono', anchor=anchor, spacing=0.2))

    inner += note(c4[0] + 10, c4[1] + 2, 396, 190, 'line end = carbon')
    inner += note(c3[0] + 12, c3[1] + 10, 396, 262, 'each vertex = carbon')
    inner += note(o[0] + 22, o[1] - 12, 352, 84, 'heteroatom — always drawn,', dot='var(--acc)')
    inner += text(352, 101, 'with the H attached to it', size=12.5, color='var(--acc)',
                  weight=500, family='GeistMono', anchor='start', spacing=0.2)
    mid12 = ((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2)
    inner += note(mid12[0] - 4, mid12[1] + 6, 60, 322, 'hydrogens on carbon: implied', ty=330)
    return svg(560, 346, inner)

def build_skeletal(pal):
    css = """
.sk-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:24px;flex:1;margin-top:12px;min-height:0}
.sk-right{display:flex;flex-direction:column;gap:18px;justify-content:center}
.sk-card{border:1px solid var(--hair);border-radius:14px;background:var(--card);padding:18px 20px}
.sk-kick{font-family:'GeistMono',monospace;font-size:10px;font-weight:600;color:var(--acc);
  letter-spacing:.16em;text-transform:uppercase;margin-bottom:10px}
.sk-eq{font-size:18.5px;font-weight:600;color:var(--ink);white-space:nowrap}
.sk-eq .oh{color:var(--oz)}
.sk-chips{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}
.sk-note{font-size:12.5px;color:var(--muted);line-height:1.5;border-top:1px solid var(--faint);
  padding-top:12px}
"""
    eq = ('CH<sub>3</sub>—CH<span class="oh">(OH)</span>—CH<sub>2</sub>—CH<sub>3</sub>')
    right = ('<div class="sk-right">'
             '<div class="sk-card"><div class="sk-kick">Translation</div>'
             '<div class="sk-eq">%s</div>'
             '<div class="sk-chips"><span class="chip acc">C<sub>4</sub>H<sub>10</sub>O</span>'
             '<span class="chip">butan-2-ol</span></div></div>'
             '<div class="sk-note">The —OH (hydroxyl) group is what makes this an alcohol — in '
             'the skeletal formula it stays fully visible while every C—H bond disappears.</div>'
             '</div>' % eq)
    body = ('<style>%s</style><div class="sk-grid"><div>%s</div>%s</div>'
            % (css, butan2ol_drawing(), right))
    return shell(1088, 512, pal, 'SPEC 4.5 · SKELETAL FORMULAE',
                 'Heteroatoms are never hidden', body,
                 footer='Skeletal rule: carbons and their hydrogens are omitted — heteroatoms '
                        '(O, N, Cl …) and any H atoms attached to them must be drawn.',
                 fkey='RULE')

HAZARD = ('hazard-symbols', 1248, 480, build_hazard)
FORMULA = ('formula-types', 1280, 704, build_formula)
SKELETAL = ('skeletal-heteroatom', 1088, 512, build_skeletal)
