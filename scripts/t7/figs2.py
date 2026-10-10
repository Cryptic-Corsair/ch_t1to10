#!/usr/bin/env python3
"""Topic 7 plates, set B: ice lattice, NaCl hydration, alcohol solubility."""
import math
from common import shell, svg, text, line, polyline

CARD_CSS = """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
.card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 14px;min-height:0}
.card .ct{display:flex;align-items:baseline;gap:10px}
.card .ct .name{font-weight:600;font-size:15.5px;color:var(--ink);letter-spacing:-.01em}
.card .ct .sig{font-family:'GeistMono',monospace;font-size:11.5px;font-weight:600;
  color:var(--acc);letter-spacing:.06em;margin-left:auto}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.card .art svg{max-width:100%;max-height:100%}
.card .sub{color:var(--body);font-size:12.5px;line-height:1.5;margin-top:10px}
"""

def dash(x1, y1, x2, y2, w=2.2, color='var(--acc)', dash='5 6'):
    return line(x1, y1, x2, y2, w=w, color=color, dash=dash)

def water(x, y, r=13, hb=None):
    """Water molecule: O circle + two H stubs at 104.5°, optional H-bond stub direction."""
    s = '<circle cx="%.1f" cy="%.1f" r="%d" fill="var(--accsoft)" stroke="var(--acc)" stroke-width="2"/>' % (x, y, r)
    s += text(x, y + 4, 'O', 11, 'var(--ink)', 600)
    a1, a2 = math.radians(52), math.radians(128)
    for a in (a1, a2):
        hx, hy = x + (r + 13) * math.cos(a), y - (r + 13) * math.sin(a)
        s += line(x + r * .6 * math.cos(a), y - r * .6 * math.sin(a), hx, hy, w=2)
        s += '<circle cx="%.1f" cy="%.1f" r="5.5" fill="var(--diafill)" stroke="var(--ink)" stroke-width="1.8"/>' % (hx, hy)
    return s

# ------------------------------------------------------------------ ice ------
def hexring(cx, cy, r):
    return [(cx + r * math.cos(math.radians(90 + 60 * i)),
             cy - r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]

def ice_art():
    inner = ''
    r = 58
    # exact honeycomb spacing for pointy-top hexagons
    s = r * math.sqrt(3)  # horizontal centre distance
    centers = [(190, 140), (190 + s, 140), (190 + s / 2, 140 + 1.5 * r)]
    verts, edges, seen = [], [], set()
    for (cx, cy) in centers:
        pts = hexring(cx, cy, r)
        for i in range(6):
            a, b = pts[i], pts[(i + 1) % 6]
            ka = (round(a[0]), round(a[1]), round(b[0]), round(b[1]))
            kb = (round(b[0]), round(b[1]), round(a[0]), round(a[1]))
            if ka in seen or kb in seen:
                continue
            seen.add(ka)
            edges.append((a, b))
    for a, b in edges:
        inner += dash(a[0], a[1], b[0], b[1], w=2.2)
    for (a, b) in edges:
        for (x, y) in (a, b):
            key = (round(x), round(y))
            if key not in verts:
                verts.append(key)
    for (x, y) in verts:
        inner += water(x, y, 11)
    # highlight the open space inside the bottom hexagon
    ccx, ccy = centers[2]
    inner += ('<circle cx="%.1f" cy="%.1f" r="30" fill="none" stroke="var(--muted)" '
              'stroke-width="1.6" stroke-dasharray="4 5"/>' % (ccx, ccy))
    inner += text(ccx, ccy + 92, 'open space inside the rings', 11.5, 'var(--muted)', 600)
    return inner

def liquid_art():
    inner = ''
    pts = [(150, 120), (250, 105), (355, 130), (185, 205), (300, 195), (390, 210),
           (140, 285), (245, 280), (350, 290)]
    bonds = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 7), (5, 8)]
    for a, b in bonds[:5]:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        inner += dash(x1, y1, x2, y2, w=2.0)
    for (x, y) in pts:
        inner += water(x, y, 12)
    inner += text(470, 200, 'rings collapsed —', 11.5, 'var(--muted)', 600, anchor='start')
    inner += text(470, 218, 'molecules sit closer', 11.5, 'var(--muted)', 600, anchor='start')
    return inner

def build_ice(pal):
    body = '<style>%s</style><div class="duo">' % CARD_CSS
    body += ('<div class="card"><div class="ct"><span class="name">ice — rings of six</span>'
             '<span class="sig">ρ ≈ 0.92 g cm⁻³</span></div>'
             '<div class="art">%s</div>'
             '<div class="sub">Hydrogen bonds hold each water at arm\u2019s length in an open '
             'hexagonal lattice: <b>large areas of open space</b> inside the rings.</div></div>'
             % svg(600, 330, ice_art()))
    body += ('<div class="card"><div class="ct"><span class="name">liquid water</span>'
             '<span class="sig">ρ ≈ 1.00 g cm⁻³</span></div>'
             '<div class="art">%s</div>'
             '<div class="sub">On melting the ring structure is destroyed and the average distance '
             'between molecules <b>decreases</b> — so the density <b>increases</b>.</div></div>'
             % svg(600, 330, liquid_art()))
    body += '</div>'
    return shell(1328, 580, pal, 'SPEC 7.3 · DENSITY OF ICE', 'Why ice floats on water',
                 body, tag='anomaly ii',
                 footer='Ice at 0 °C is less dense than water at 0 °C — the open hydrogen-bonded rings '
                        'lock the molecules further apart. Ice floats, lakes freeze from the top down, '
                        'and aquatic life survives below the ice layer.',
                 fkey='STRUCTURE')

# ------------------------------------------------------------ NaCl hydration -
def build_nacl(pal):
    W, H = 1110, 470
    inner = ''
    # lattice (top-left): 4x3 grid of Na+/Cl-
    lx, ly, step = 120, 60, 62
    for row in range(3):
        for col in range(4):
            x, y = lx + col * step, ly + row * step
            na = (row + col) % 2 == 0
            fill = 'var(--accsoft)' if na else 'var(--coolsoft)'
            edge = 'var(--acc)' if na else 'var(--cool)'
            inner += ('<circle cx="%.1f" cy="%.1f" r="17" fill="%s" stroke="%s" stroke-width="2"/>'
                      % (x, y, fill, edge))
            inner += text(x, y + 4, 'Na⁺' if na else 'Cl⁻', 10, 'var(--ink)', 600)
    inner += text(lx + step * 1.5, ly + step * 3 + 34, 'the lattice must first be broken', 12, 'var(--muted)', 600, anchor='end')
    # attacking water molecules
    for (wx, wy, r) in ((430, 70, 40), (415, 190, 190), (455, 130, 320)):
        pass
    inner += water(440, 80, 15)
    inner += water(430, 175, 15)
    inner += text(500, 120, 'polar water molecules', 12, 'var(--muted)', 600, anchor='start')
    inner += text(500, 138, 'attack the lattice: Oδ− toward Na⁺, Hδ+ toward Cl⁻', 12, 'var(--muted)', 600, anchor='start')
    # arrows down
    for x in (290, 760):
        inner += line(x, 252, x, 280, w=2.2, color='var(--muted)')
        inner += ('<path d="M %.1f 280 L %.1f 270 L %.1f 270 z" fill="var(--muted)"/>' % (x, x - 5, x + 5))
    # hydrated Na+ card
    cx, cy, rr = 290, 360, 26
    inner += '<circle cx="%.1f" cy="%.1f" r="%d" fill="var(--accsoft)" stroke="var(--acc)" stroke-width="2.4"/>' % (cx, cy, rr)
    inner += text(cx, cy + 4, 'Na⁺', 13, 'var(--ink)', 700)
    for i, ang in enumerate((90, 162, 234, 306, 18, 54)):
        a = math.radians(ang)
        wx, wy = cx + 66 * math.cos(a), cy + 66 * math.sin(a)
        inner += line(cx + rr * math.cos(a), cy + rr * math.sin(a), wx - 13 * math.cos(a), wy - 13 * math.sin(a), w=1.4, color='var(--faint)')
        inner += '<circle cx="%.1f" cy="%.1f" r="12" fill="var(--diafill)" stroke="var(--acc)" stroke-width="1.8"/>' % (wx, wy)
        inner += text(wx, wy + 4, 'O', 9, 'var(--ink)', 600)
    inner += text(cx, cy + 108, 'oxygen ends (δ−) face the cation', 12, 'var(--body)', 600)
    # hydrated Cl- card
    cx2 = 760
    inner += '<circle cx="%.1f" cy="%.1f" r="%d" fill="var(--coolsoft)" stroke="var(--cool)" stroke-width="2.4"/>' % (cx2, cy, rr)
    inner += text(cx2, cy + 4, 'Cl⁻', 13, 'var(--ink)', 700)
    for i, ang in enumerate((126, 198, 270, 342, 54)):
        a = math.radians(ang)
        wx, wy = cx2 + 66 * math.cos(a), cy + 66 * math.sin(a)
        inner += line(cx2 + rr * math.cos(a), cy + rr * math.sin(a), wx - 13 * math.cos(a), wy - 13 * math.sin(a), w=1.4, color='var(--faint)')
        inner += '<circle cx="%.1f" cy="%.1f" r="12" fill="var(--diafill)" stroke="var(--cool)" stroke-width="1.8"/>' % (wx, wy)
        inner += text(wx, wy + 4, 'H', 9, 'var(--ink)', 600)
    inner += text(cx2, cy + 108, 'hydrogen ends (δ+) face the anion', 12, 'var(--body)', 600)
    body = '<style>%s</style><div class="card" style="margin-top:20px;flex:1">' \
           '<div class="art" style="padding:4px 4px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner))
    return shell(1248, 660, pal, 'SPEC 7.6 · HYDRATION OF THE IONS',
                 'How water dissolves an ionic solid',
                 body, tag='NaCl in water',
                 footer='Ion–dipole attractions release the HYDRATION ENTHALPY as each ion becomes surrounded by '
                        'oriented water molecules. The compound dissolves when hydration enthalpy ≥ lattice energy — '
                        'otherwise the energy released is insufficient to break up the lattice.',
                 fkey='MECHANISM')

# ------------------------------------------------------- alcohol solubility --
def alcohol_row(inner, y, name, formula, ncarbons, verdict, note, tailcolor):
    # OH head at right, chain growing left — compute chain bbox first
    x_head = 700
    L = 46
    dx, dy = L * math.cos(math.radians(60)), L * math.sin(math.radians(60))
    pts = [(x_head, y)]
    x, yv = x_head, y
    up = True
    for _ in range(ncarbons - 1):
        x -= dx; yv += -dy if up else dy
        pts.append((x, yv)); up = not up
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    bx0, bx1 = min(xs) - 30, x_head + 44
    by0, by1 = min(ys) - 26, max(ys) + 26
    inner += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="14" fill="%s"/>'
              % (bx0, by0, bx1 - bx0, by1 - by0, tailcolor))
    inner += polyline(pts, w=3.0, color='var(--ink)')
    if ncarbons == 1:
        inner += text(x_head - 12, y + 4, 'H₃C', 11, 'var(--ink)', 600, anchor='end')
    inner += '<circle cx="%.1f" cy="%.1f" r="13" fill="var(--accsoft)" stroke="var(--acc)" stroke-width="2"/>' % (x_head + 26, y)
    inner += text(x_head + 26, y + 4, 'O', 10, 'var(--ink)', 600)
    inner += '<circle cx="%.1f" cy="%.1f" r="6.5" fill="var(--diafill)" stroke="var(--ink)" stroke-width="1.8"/>' % (x_head + 48, y + 22)
    inner += text(x_head + 48, y + 25, 'H', 8.5, 'var(--ink)', 600)
    inner += line(x_head + 26 + 9, y + 8, x_head + 44, y + 18, w=1.8)
    inner += text(70, y - 18, name, 14.5, 'var(--ink)', 600, anchor='start')
    inner += text(70, y + 2, formula, 11.5, 'var(--muted)', 500, anchor='start', family='GeistMono')
    inner += text(790, y - 4, verdict, 12.5, 'var(--acc)', 600, anchor='start')
    inner += text(790, y + 16, note, 11, 'var(--muted)', 500, anchor='start')
    inner += line(70, y + 46, 1130, y + 46, w=1, color='var(--faint)')
    return inner

def build_solubility(pal):
    W, H = 1200, 400
    inner = text(70, 30, 'the –OH head hydrogen bonds with water · the non-polar tail cannot',
                 12.5, 'var(--body)', 600, anchor='start')
    inner = alcohol_row(inner, 90, 'methanol', 'CH₃OH', 1, 'very soluble',
                        'hydrogen bonds with water in all proportions', 'var(--accsoft)')
    inner = alcohol_row(inner, 210, 'butan-1-ol', 'CH₃CH₂CH₂CH₂OH', 4, 'slightly soluble',
                        'solubility dropping as the tail grows', 'var(--card2)')
    inner = alcohol_row(inner, 330, 'octan-1-ol', 'CH₃(CH₂)₇OH', 8, 'very insoluble',
                        'tail dominates — practically insoluble', 'var(--faint)')
    body = '<style>%s</style><div class="card" style="margin-top:20px;flex:1">' \
           '<div class="art" style="padding:4px 6px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner))
    return shell(1328, 560, pal, 'SPEC 7.6 · ALCOHOLS IN WATER',
                 'Solubility falls as the non-polar tail grows',
                 body, tag='like dissolves like',
                 footer='Water–alcohol hydrogen bonds must replace water–water hydrogen bonds AND alcohol–alcohol '
                        'London forces. Short chains: hydrogen bonding wins. Long chains: the London forces between '
                        'tails dominate and the alcohol separates out. Carboxylic acids behave the same way.',
                 fkey='TREND')
