#!/usr/bin/env python3
"""Topic 9 figure plates 1-6 — built on the approved Topic 4/6/7/8 pipeline."""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
from common import (LIGHT, DARK, shell, svg, line, polyline, arrow, text,  # noqa: E402,F401
                    pts_path)

GRID_CSS = """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;flex:1;align-content:stretch;margin-top:20px}
.mid{display:grid;grid-template-columns:1fr 96px 1fr;gap:0;flex:1;align-content:stretch;margin-top:20px;align-items:stretch}
.card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 14px;min-height:0}
.card .ct{display:flex;align-items:baseline;gap:10px}
.card .ct .name{font-weight:600;font-size:15.5px;color:var(--ink);letter-spacing:-.01em}
.card .ct .sig{font-family:'GeistMono',monospace;font-size:11.5px;font-weight:600;
  color:var(--acc);letter-spacing:.06em;margin-left:auto}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.card .art svg{max-width:100%;max-height:100%}
.card .sub{color:var(--body);font-size:12.5px;line-height:1.5;margin-top:10px}
.arrowcol{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.arrowcol .alab{font-family:'GeistMono',monospace;font-size:10.5px;font-weight:600;color:var(--acc);
  letter-spacing:.1em;text-transform:uppercase}
"""


def card(name, art, sig=None, sub=None):
    s = '<div class="sig">%s</div>' % sig if sig else ''
    sb = '<div class="sub">%s</div>' % sub if sub else ''
    return ('<div class="card"><div class="ct"><span class="name">%s</span>%s</div>'
            '<div class="art">%s</div>%s</div>' % (name, s, art, sb))


def axes2(x0, y0, w, h, xlabel, ylabel):
    """L-shaped axis; origin (x0,y0) bottom-left; returns svg fragment."""
    out = line(x0, y0, x0 + w, y0, w=2, color='var(--ink)')
    out += line(x0, y0, x0, y0 - h, w=2, color='var(--ink)')
    if xlabel:
        out += text(x0 + w / 2, y0 + 26, xlabel, 12.5, 'var(--body)', 600, family='GeistMono', spacing=1)
    if ylabel:
        out += ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
                'style="font-family:GeistMono;font-size:11.5px;font-weight:600;fill:var(--body);letter-spacing:1px">%s</text>'
                % (x0 - 30, y0 - h / 2, x0 - 30, y0 - h / 2, ylabel))
    return out


def mb_pts(x0, y0, w, h, b=8.0, n=72, xmax=1.0):
    """Maxwell-Boltzmann curve, peak height 1 at t=2/b. Returns (pts, tp)."""
    tp = 2.0 / b
    k = math.exp(b * tp) / (tp * tp)
    pts = []
    for i in range(n + 1):
        t = xmax * i / n
        y = k * t * t * math.exp(-b * t)
        pts.append((x0 + t * w, y0 - y * h))
    return pts, tp


# ------------------------------------------------------------ 1 · orientation ----
def _ethene(cx, cy):
    """Ethene displayed formula centred on the C=C at (cx,cy)-(cx+56,cy)."""
    s = ''
    lx, rx = cx, cx + 56
    s += line(lx + 6, cy - 3.5, rx - 6, cy - 3.5, w=2.4, color='var(--ink)')
    s += line(lx + 6, cy + 3.5, rx - 6, cy + 3.5, w=2.4, color='var(--ink)')
    for x, hx, hy in ((lx, lx - 42, cy - 40), (lx, lx - 42, cy + 40),
                      (rx, rx + 42, cy - 40), (rx, rx + 42, cy + 40)):
        s += line(x, cy, hx, hy, w=2, color='var(--ink)')
        s += text(hx, hy + (16 if hy > cy else -8), 'H', 14, 'var(--ink)', 600)
    s += text(lx - 2, cy + 5, 'C', 14, 'var(--ink)', 700)
    s += text(rx + 2, cy + 5, 'C', 14, 'var(--ink)', 700)
    return s


def build_orientation(pal):
    W, H = 400, 296

    def inner(cnum, layout):
        s = ''
        s += _ethene(W / 2 - 50, 108)
        X = W / 2 + 6
        if layout == 'up':        # H–Br vertical below, H end toward the C=C
            s += arrow(X, 232, X, 158, w=1.6, color='var(--acc)', marker='arwacc')
            s += text(X + 4, 256, 'H', 14, 'var(--ink)', 600)
            s += line(X, 262, X, 272, w=2, color='var(--ink)')
            s += text(X + 4, 290, 'Br', 14, 'var(--ink)', 600)
        elif layout == 'down':    # H–Br vertical below, Br end toward the C=C
            s += arrow(X, 232, X, 158, w=1.6, color='var(--muted)', marker='arw')
            s += text(X + 4, 256, 'Br', 14, 'var(--ink)', 600)
            s += line(X, 262, X, 272, w=2, color='var(--ink)')
            s += text(X + 4, 290, 'H', 14, 'var(--ink)', 600)
        else:                     # H–Br horizontal on the right, H end toward the C=C
            s += text(W / 2 + 150, 112, 'H', 14, 'var(--ink)', 600)
            s += text(W / 2 + 186, 112, 'Br', 14, 'var(--ink)', 600)
            s += line(W / 2 + 158, 107, W / 2 + 180, 107, w=2, color='var(--ink)')
            s += arrow(W / 2 + 142, 107, W / 2 + 88, 107, w=1.6, color='var(--muted)', marker='arw')
        return s

    verdicts = ('possible reaction', 'no reaction', 'no reaction')
    layouts = ('up', 'down', 'side')
    cards = ''
    for i in range(3):
        art = svg(W, H, inner(i + 1, layouts[i]))
        col = 'var(--acc)' if i == 0 else 'var(--muted)'
        cards += card('Collision %d' % (i + 1), art,
                      sub='<span style="color:%s;font-weight:600">%s</span>' % (col, verdicts[i]))
    body = '<style>%s</style><div class="trio">%s</div>' % (GRID_CSS, cards)
    return shell(1300, 620, pal, 'SPEC 9.1 · COLLISION GEOMETRY',
                 'Orientation (steric effect) — only the right geometry reacts',
                 body, tag='proper geometry',
                 footer='Collisions will result in reaction only if the molecules collide in the proper geometry. '
                        'Collision 1 brings the H end of H–Br to the C=C in the right orientation — a reaction is possible.',
                 fkey='STERIC EFFECT')


# ---------------------------------------------------------- 2 · rate graphs ----
def build_rate_graphs(pal):
    W, H = 540, 336

    def reactant():
        x0, y0, w, h = 56, 292, 440, 250
        s = axes2(x0, y0, w, h, 'Time', 'Concentration')
        pts = []
        for i in range(61):
            t = i / 60.0
            x = x0 + t * w
            y = y0 - (1 - t) ** 1.7 * h * 0.94
            pts.append((x, y))
        s += polyline(pts, w=2.8, color='var(--ink)')
        ax, ay = pts[27]
        tt = 27 / 60.0
        slope = 1.7 * (1 - tt) ** 0.7 * h * 0.94 / w
        tx1, ty1 = ax - 120, ay + 120 * slope
        tx2, ty2 = ax + 130, ay - 130 * slope
        s += line(tx1, ty1, tx2, ty2, w=1.8, color='var(--acc)')
        by = ty2 + 46
        dx = 46 / slope
        s += line(tx2, ty2, tx2, by, w=1.4, color='var(--muted)', dash='4 4')
        s += line(tx2, by, tx2 - dx, by, w=1.4, color='var(--muted)', dash='4 4')
        s += text(tx2 + 12, (ty2 + by) / 2 + 4, 'y', 13, 'var(--acc)', 700)
        s += text(tx2 - dx / 2, by + 20, 'x', 13, 'var(--acc)', 700)
        s += ('<circle cx="%.0f" cy="%.0f" r="4.5" fill="var(--acc)"/>' % (ax, ay))
        s += text(ax + 12, ay - 10, 'A', 14, 'var(--acc)', 700)
        s += arrow(396, 122, 466, 258, w=1.4, color='var(--muted)')
        s += text(396, 96, 'gradient = zero', 11.5, 'var(--muted)', 600, family='GeistMono', anchor='middle')
        s += text(396, 112, 'when reaction', 11.5, 'var(--muted)', 600, family='GeistMono', anchor='middle')
        s += text(396, 128, 'is complete', 11.5, 'var(--muted)', 600, family='GeistMono', anchor='middle')
        return svg(W, H, s)

    def product():
        x0, y0, w, h = 56, 292, 440, 250
        s = axes2(x0, y0, w, h, 'Time', 'Concentration')
        pts = []
        for i in range(61):
            t = i / 60.0
            x = x0 + t * w
            y = y0 - (1 - math.exp(-3.1 * t)) * h * 0.9
            pts.append((x, y))
        s += polyline(pts, w=2.8, color='var(--ink)')
        s += line(x0 + 4, y0 - 8, x0 + 150, y0 - 236, w=1.8, color='var(--acc)')
        s += text(x0 + 158, y0 - 238, 'initial rate', 12, 'var(--acc)', 700, anchor='start')
        tt = 0.42
        txp = x0 + tt * w
        typ = y0 - (1 - math.exp(-3.1 * tt)) * h * 0.9
        slope = 3.1 * math.exp(-3.1 * tt) * h * 0.9 / w
        s += line(txp - 110, typ + 110 * slope, txp + 110, typ - 110 * slope, w=1.8, color='var(--cool)')
        s += text(txp + 118, typ - 8, 'rate at', 12, 'var(--cool)', 700, anchor='start')
        s += text(txp + 118, typ + 8, 'time, t', 12, 'var(--cool)', 700, anchor='start')
        s += line(txp, typ, txp, y0, w=1.3, color='var(--muted)', dash='3 4')
        s += text(txp, y0 + 20, 't', 13, 'var(--ink)', 700, italic=True)
        s += line(x0 + 262, y0 - h * 0.9, x0 + w, y0 - h * 0.9, w=1.3, color='var(--muted)', dash='3 4')
        s += text(x0 + w, y0 - h * 0.9 - 10, 'rate at end = zero', 11.5, 'var(--muted)', 600,
                  family='GeistMono', anchor='end')
        return svg(W, H, s)

    body = ('<style>%s</style><div class="duo">%s%s</div>'
            % (GRID_CSS, card('With respect to reactants', reactant(), sig='FIG A'),
               card('With respect to products', product(), sig='FIG B')))
    return shell(1340, 640, pal, 'SPEC 9.3 · RATE FROM GRAPHS',
                 'Rate from concentration–time graphs', body, tag='tangent → gradient → rate',
                 footer='The slope of the graph measures the rate of the reaction. Y = change of concentration '
                        '(mol dm⁻³) · X = change in time (seconds) · unit of rate = mol dm⁻³ s⁻¹ · '
                        'rate is determined by drawing a tangent at a point and measuring its gradient.',
                 fkey='GRADIENT = y/x')


# ------------------------------------------------- 3 · concentration effect ----
def build_concentration_effect(pal):
    W, H = 700, 350
    x0, y0, w, h = 70, 300, 560, 250
    hp = 0.72 * h
    s = axes2(x0, y0, w, h, 'Time', 'Volume')
    s += text(x0 + 2, y0 - h - 26, 'of CO₂', 12.5, 'var(--body)', 600, family='GeistMono', anchor='start')
    s += line(x0 + 30, y0 - hp, x0 + w - 6, y0 - hp, w=1.3, color='var(--muted)', dash='3 4')

    def curve(t_end, b):
        pts = []
        for i in range(61):
            t = (i / 60.0) * t_end
            y = (1 - math.exp(-b * t)) * hp
            if y > hp:
                y = hp
            pts.append((x0 + t * w, y0 - y))
        return pts

    s += polyline(curve(0.40, 9.0), w=2.8, color='var(--acc)')
    s += polyline(curve(0.97, 3.2), w=2.8, color='var(--cool)')
    s += text(x0 + 0.055 * w, y0 - hp + 48, 'A', 15, 'var(--acc)', 700)
    s += text(x0 + 0.30 * w, y0 - hp + 70, 'B', 15, 'var(--cool)', 700)
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Volume of carbon dioxide collected against time', svg(W, H, s), sig='HCl CONC ↑'))
    return shell(1240, 620, pal, 'SPEC 9.1 · EFFECT OF CONCENTRATION',
                 'Higher HCl concentration — steeper curve, faster completion', body,
                 tag='CaCO₃(s) + 2HCl → CaCl₂ + CO₂(g)',
                 footer='Curve A is steeper therefore rate of reaction is faster than curve B · gradient of curve A is '
                        'greater than gradient of curve B · curve A levels off quickly compared to curve B indicating '
                        'faster completion of reaction.',
                 fkey='CURVE A vs B')


# ------------------------------------------------------- 4 · pressure effect ----
def build_pressure_effect(pal):
    import random
    W, H = 470, 268

    def vessel(vw, vh, seed):
        rnd = random.Random(seed)
        s = ('<rect x="%.0f" y="14" width="%d" height="%d" rx="16" fill="var(--card2)" '
             'stroke="var(--hair)" stroke-width="1.5"/>' % (W / 2 - vw / 2, vw, vh))
        cols = ('var(--acc)', 'var(--cool)')
        for i in range(14):
            mx = W / 2 - vw / 2 + 24 + rnd.random() * (vw - 48)
            my = 14 + 22 + rnd.random() * (vh - 44)
            r = 11 if i % 3 == 0 else 7
            s += '<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" fill-opacity=".82"/>' % (mx, my, r, cols[i % 2])
        return s

    body = ('<style>%s</style><div class="mid">%s'
            '<div class="arrowcol">%s<span class="alab">increase<br/>pressure</span></div>%s</div>'
            % (GRID_CSS,
               card('Before', svg(W, H, vessel(360, 226, 7)),
                    sub='The molecules have space to move around and there is little chance of a collision.'),
               svg(72, 60, arrow(6, 30, 62, 30, w=2.2, color='var(--acc)', marker='arwacc')),
               card('After', svg(W, H, vessel(256, 226, 7)),
                    sub='Increasing the pressure decreases the volume and increases the concentration. '
                        'The molecules have less space to move in and are more likely to collide.')))
    return shell(1300, 600, pal, 'SPEC 9.1 · EFFECT OF PRESSURE (ONLY FOR GASES)',
                 'Same molecules, smaller space — more collisions', body, tag='gases only',
                 footer='Same number of gaseous molecules in a smaller space, or number of gaseous molecules per unit '
                        'volume increases · increasing the pressure makes gas particles get closer together · this '
                        'increases the frequency of collisions · so frequency of effective collisions increases. '
                        'Changing the pressure has almost no effect on reactions in solid or liquid phase.',
                 fkey='PRESSURE ↑')


# ----------------------------------------------------- 5 · surface area ----
def build_surface_area(pal):
    def cubes_row():
        W, H = 420, 158
        s = ''
        bx, by, r = 56, 34, 54
        s += ('<rect x="%d" y="%d" width="%d" height="%d" fill="var(--card2)" stroke="var(--ink)" stroke-width="2"/>'
              % (bx, by, 2 * r, 2 * r))
        s += text(bx + r, by + 2 * r + 26, 'one large solid', 11.5, 'var(--muted)', 600, family='GeistMono')
        s += arrow(bx + 2 * r + 24, by + r, bx + 2 * r + 88, by + r, w=1.8, color='var(--acc)', marker='arwacc')
        gx, gy, gr = bx + 2 * r + 112, by + 4, 17
        for i in range(3):
            for j in range(3):
                s += ('<rect x="%d" y="%d" width="%d" height="%d" fill="var(--card2)" stroke="var(--ink)" stroke-width="1.6"/>'
                      % (gx + j * (gr + 5), gy + i * (gr + 5), gr, gr))
        s += text(gx + 1.5 * (gr + 5) - 8, gy + 3 * (gr + 5) + 24, 'same volume, powdered', 11.5, 'var(--muted)', 600,
                  family='GeistMono')
        return svg(W, H, s)

    def mg_block(powdered):
        W, H = 470, 240
        s = ('<rect x="8" y="8" width="%d" height="%d" rx="12" fill="var(--diafill)" stroke="var(--hair)" stroke-width="1.4"/>'
             % (W - 16, H - 16))
        red, green = 'var(--oz)', 'var(--acc)'
        rnd = __import__('random').Random(3 if not powdered else 11)
        clusters = []
        if not powdered:
            for i in range(9):
                for j in range(6):
                    s += '<circle cx="%.0f" cy="%.0f" r="10" fill="%s" fill-opacity=".85"/>' % (
                        100 + i * 21, 62 + j * 21, green)
            clusters.append((100 - 12, 62 - 12, 9 * 21 + 4, 6 * 21 + 4))
        else:
            layout = ((80, 60, 3, 3), (200, 50, 4, 2), (330, 70, 3, 3), (90, 150, 3, 2),
                      (210, 130, 3, 3), (330, 150, 4, 2), (150, 96, 2, 2), (268, 96, 2, 2))
            for cx, cy, nx, ny in layout:
                for i in range(nx):
                    for j in range(ny):
                        s += '<circle cx="%.0f" cy="%.0f" r="10" fill="%s" fill-opacity=".85"/>' % (
                            cx + i * 21, cy + j * 21, green)
                clusters.append((cx - 12, cy - 12, nx * 21 + 4, ny * 21 + 4))
        for _ in range(26):
            hx = 24 + rnd.random() * (W - 48)
            hy = 24 + rnd.random() * (H - 48)
            if any(cx <= hx <= cx + cw and cy <= hy <= cy + ch for cx, cy, cw, ch in clusters):
                continue
            s += '<circle cx="%.1f" cy="%.1f" r="6.5" fill="%s" fill-opacity=".9"/>' % (hx, hy, red)
        return svg(W, H, s)

    top = card('One lump → the same mass as powder', cubes_row(),
               sub='<em>More surface is exposed for reaction.</em>')
    c1 = card('Solid magnesium + dilute acid', mg_block(False),
              sub='Only collisions between the hydrogen ions and magnesium atoms on the <em>surface</em> of '
                  'magnesium result in a reaction.')
    c2 = card('Powdered magnesium + dilute acid', mg_block(True),
              sub='If magnesium is powdered, the surface area is increased and hydrogen is given off more quickly.')
    body = ('<style>%s</style><div class="duo" style="grid-template-columns:1fr;margin-bottom:16px">%s</div>'
            '<div class="duo">%s%s</div>' % (GRID_CSS, top, c1, c2))
    return shell(1340, 800, pal, 'SPEC 9.1 · EFFECT OF SURFACE AREA',
                 'Greater surface area — more chances of a collision', body, tag='heterogeneous reactions',
                 footer='Greater surface area of the solid is exposed for collision · frequency of collisions increases '
                        '· so frequency of effective collisions increases · catalysts (in catalytic converters) are used '
                        'in a finely divided form for this reason.',
                 fkey='MORE SURFACE')


# --------------------------------------------- 6 · Maxwell-Boltzmann curve ----
def build_maxwell_boltzmann(pal):
    W, H = 780, 392
    x0, y0, w, h = 96, 330, 610, 264
    s = axes2(x0, y0, w, h, 'MOLECULAR ENERGY', 'NUMBER OF MOLECULES WITH')
    s += text(x0 - 30, y0 - h / 2 + 30, 'A PARTICULAR ENERGY', 10.5, 'var(--body)', 600, family='GeistMono')
    pts, tp = mb_pts(x0, y0, w, h, b=8.0)
    ea_t = 0.62
    ea_x = x0 + ea_t * w
    tail = [p for p in pts if p[0] >= ea_x - 0.5]
    d = 'M%.1f,%.1f ' % tail[0] + 'L'.join('%.1f,%.1f ' % p for p in tail[1:])
    d += 'L%.1f,%.1f Z' % (x0 + w, y0)
    s += '<path d="%s" fill="var(--accsoft)"/>' % d
    s += polyline(pts, w=2.8, color='var(--ink)')
    s += line(ea_x, y0, ea_x, y0 - h - 8, w=1.5, color='var(--acc)', dash='5 5')
    s += text(ea_x + 8, y0 - h - 22, 'Activation Energy', 12.5, 'var(--acc)', 700, anchor='start')
    s += text(ea_x + 8, y0 - h - 6, '(Ea)', 12.5, 'var(--acc)', 700, anchor='start')
    px, py = x0 + tp * w, y0 - h
    s += arrow(px, py - 46, px, py - 10, w=1.5, color='var(--muted)')
    s += text(px - 6, py - 56, 'Most probable energy', 11.5, 'var(--body)', 600, family='GeistMono')
    s += text(x0 + w - 6, y0 - 66, 'few molecules have', 11.5, 'var(--body)', 600, anchor='end', family='GeistMono')
    s += text(x0 + w - 6, y0 - 50, 'extremely high energies', 11.5, 'var(--body)', 600, anchor='end', family='GeistMono')
    s += text(x0 + 4, y0 + 44, 'curve starts from origin · no molecule has zero energy', 11.5, 'var(--muted)', 600,
              family='GeistMono', anchor='start')
    s += arrow(x0 + 214, y0 + 50, x0 + 26, y0 - 6, w=1.2, color='var(--muted)')
    s += text(x0 + w, y0 + 44, 'curve should not touch the X-axis', 11.5, 'var(--muted)', 600,
              family='GeistMono', anchor='end')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Distribution of molecular energies in a gas (also applies to particles in solution)',
                       svg(W, H, s), sig='AREA = TOTAL PARTICLES'))
    return shell(1300, 660, pal, 'SPEC 9.4 · MAXWELL-BOLTZMANN DISTRIBUTION CURVES',
                 'Molecules have a wide range of energies', body, tag='spread of velocities',
                 footer='The area under the curve beyond Ea is proportional to the number of particles with energy '
                        'greater than activation energy · if the activation energy is high, only about 1 in 10¹² '
                        'molecules possesses this energy at room temperature, so the reaction does not take place — '
                        'the system is said to be kinetically stable.',
                 fkey='DISTRIBUTION')
