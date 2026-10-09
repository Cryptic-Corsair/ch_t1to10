#!/usr/bin/env python3
"""Topic 7 plates, set A: London force origin, contact area, H-bond geometry, hydride graph."""
import math
from common import shell, svg, text, line, polyline, wavy

CARD_CSS = """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
.trio{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
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

def dash(x1, y1, x2, y2, w=2.4, color='var(--acc)', dash='7 7'):
    return line(x1, y1, x2, y2, w=w, color=color, dash=dash)

def blob(cx, cy, rx, ry, color, op=.85):
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f"/>'
            % (cx, cy, rx, ry, color, op))

def mol_pair():
    """Two molecules: A instantaneous dipole, B induced dipole. Both δ− left / δ+ right."""
    inner = ''
    # molecule A
    ax, ay = 300, 170
    inner += blob(ax - 52, ay, 74, 52, 'var(--cool)', .55)
    inner += blob(ax + 52, ay, 74, 52, 'var(--acc)', .35)
    inner += '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--ink)"/>' % (ax - 14, ay)
    inner += '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--ink)"/>' % (ax + 30, ay)
    inner += text(ax - 74, ay - 66, 'δ−', 21, 'var(--cool)', 700)
    inner += text(ax + 74, ay - 66, 'δ+', 21, 'var(--acc)', 700)
    inner += text(ax, ay + 96, 'instantaneous dipole in molecule A', 13.5, 'var(--body)', 600)
    # molecule B (same orientation — facing ends opposite)
    bx, by = 900, 170
    inner += blob(bx - 52, by, 74, 52, 'var(--cool)', .55)
    inner += blob(bx + 52, by, 74, 52, 'var(--acc)', .35)
    inner += '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--ink)"/>' % (bx - 14, by)
    inner += '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--ink)"/>' % (bx + 30, by)
    inner += text(bx - 74, by - 66, 'δ−', 21, 'var(--cool)', 700)
    inner += text(bx + 74, by - 66, 'δ+', 21, 'var(--acc)', 700)
    inner += text(bx, by + 96, 'induced dipole in molecule B', 13.5, 'var(--body)', 600)
    # curved 'induces' arrow above the pair
    mx = (ax + bx) / 2
    inner += ('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="var(--acc)" '
              'stroke-width="2.2" marker-end="url(#arwacc)"/>'
              % (ax + 90, ay - 74, mx, ay - 128, bx - 90, by - 74))
    inner += text(mx, ay - 140, 'induces', 13, 'var(--acc)', 600, family='GeistMono')
    # attraction between facing ends
    inner += dash(ax + 118, ay, bx - 108, by, w=2.6, color='var(--ink)', dash='4 6')
    inner += text(mx, ay + 30, 'δ+  ····  δ−   attraction', 12.5, 'var(--muted)', 500, family='GeistMono')
    return inner

def molecules_strip():
    """Many molecules held together by instantaneous dipoles (all same orientation — facing ends opposite)."""
    inner = ''
    y0 = 360
    for i in range(7):
        cx = 120 + i * 172
        inner += blob(cx - 34, y0, 44, 26, 'var(--cool)', .38)
        inner += blob(cx + 34, y0, 44, 26, 'var(--acc)', .38)
        if i < 6:
            inner += dash(cx + 80, y0, cx + 92, y0, w=2.0, color='var(--muted)', dash='3 5')
    inner += text(732, y0 + 58, 'fluctuations come and go — but at every instant there are attractions',
                  12.5, 'var(--muted)', 500)
    return inner

def build_london(pal):
    W, H = 1248, 520
    inner = mol_pair() + molecules_strip()
    body = '<style>%s</style><div class="card" style="margin-top:20px;flex:1">' \
           '<div class="art" style="padding:8px 10px 2px">%s</div></div>' % (CARD_CSS, svg(W, H, inner))
    return shell(W + 80, 660, pal, 'SPEC 7.1 · LONDON FORCES',
                 'Instantaneous dipole – induced dipole attraction',
                 body, tag='all molecules · noble gases',
                 footer='Electrons move constantly and randomly; the electron density fluctuates and a temporary '
                        '(transient) dipole forms. It induces an opposite dipole in its neighbour — the facing δ+ / δ− '
                        'ends attract. No molecule can escape London forces; ionic substances have none.',
                 fkey='ORIGIN')

# ---------------------------------------------------------------- contact ----
def pentane(x0, y0, n=5, L=40):
    dx, dy = L * math.cos(math.radians(60)), L * math.sin(math.radians(60))
    pts, x, y, up = [(x0, y0)], x0, y0, True
    for _ in range(n - 1):
        x += dx; y += -dy if up else dy
        pts.append((x, y)); up = not up
    return pts

def contact_art(cx, cy, straight):
    inner = ''
    if straight:
        top = pentane(cx - 130, cy - 34)
        bot = pentane(cx - 130, cy + 66)
        inner += '<ellipse cx="%.1f" cy="%.1f" rx="190" ry="30" fill="var(--accsoft)"/>' % (cx, cy + 14)
        inner += polyline(top, w=3.2, color='var(--ink)')
        inner += polyline(bot, w=3.2, color='var(--ink)')
        inner += text(cx, cy - 84, 'long parallel chains — contact along the whole length', 12.5, 'var(--body)', 500)
    else:
        # two compact crosses touching at one point
        def cross(mx, my):
            s = ''
            for ang in (0, 90, 180, 270):
                x2 = mx + 34 * math.cos(math.radians(ang))
                y2 = my + 34 * math.sin(math.radians(ang))
                s += line(mx, my, x2, y2, w=3.2, color='var(--ink)')
            return s
        inner += '<circle cx="%.1f" cy="%.1f" r="52" fill="var(--accsoft)"/>' % (cx, cy)
        inner += cross(cx, cy - 60)
        inner += cross(cx, cy + 60)
        inner += text(cx + 118, cy - 6, 'compact, roughly spherical —', 12.5, 'var(--body)', 500, anchor='start')
        inner += text(cx + 118, cy + 16, 'touching at one small region', 12.5, 'var(--body)', 500, anchor='start')
    return inner

def build_contact(pal):
    body = '<style>%s</style><div class="duo">' % CARD_CSS
    body += ('<div class="card"><div class="ct"><span class="name">pentane</span>'
             '<span class="sig">bp 36 °C</span></div>'
             '<div class="art">%s</div>'
             '<div class="sub">Same formula C₅H₁₂, same electrons — but the straight chain gives '
             '<b>more points of contact</b>, so the overall London force is greater.</div></div>'
             % svg(600, 300, contact_art(300, 148, True)))
    body += ('<div class="card"><div class="ct"><span class="name">2,2-dimethylpropane</span>'
             '<span class="sig">bp 9.5 °C</span></div>'
             '<div class="art">%s</div>'
             '<div class="sub">The branched isomer is compact: <b>fewer points of contact</b>, '
             'weaker London forces — it boils 26.5 °C lower.</div></div>'
             % svg(600, 300, contact_art(270, 148, False)))
    body += '</div>'
    return shell(1328, 560, pal, 'SPEC 7.1 · LONDON FORCES', 'Contact area decides the strength',
                 body, tag='shape effect',
                 footer='The more points of contact there are between molecules, the greater the overall '
                        'London force — one of the two features (with electron-cloud size) you quote in '
                        'boiling-point explanations.',
                 fkey='FEATURE 2')

# ------------------------------------------------------------- h-bond geo ----
def atom(x, y, r, label, size=15):
    return ('<circle cx="%.1f" cy="%.1f" r="%d" fill="var(--diafill)" stroke="var(--ink)" stroke-width="2.2"/>'
            % (x, y, r) + text(x, y + size * .36, label, size, 'var(--ink)', 600))

def lone_dots(x, y, ang, r=22, sep=9):
    """A lone pair: two dots just outside an atom of radius r, direction ang (deg)."""
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    gap = r + 12
    mx, my = x + dx * gap, y + dy * gap
    return ('<circle cx="%.1f" cy="%.1f" r="3.4" fill="var(--acc)"/>'
            '<circle cx="%.1f" cy="%.1f" r="3.4" fill="var(--acc)"/>'
            % (mx + px * sep, my + py * sep, mx - px * sep, my - py * sep))

def hbond_geo_water():
    inner = ''
    o1x, o1y, o2x, o2y = 150, 78, 242, 190
    # O1: lone pairs up-left and up-right
    inner += lone_dots(o1x, o1y, -125) + lone_dots(o1x, o1y, -55)
    # O1 H atoms: down-left (135°) and down-right (45°)
    for ang in (135, 45):
        a = math.radians(ang)
        bx, by = o1x + 22 * math.cos(a), o1y + 22 * math.sin(a)
        hx, hy = o1x + 36 * math.cos(a), o1y + 36 * math.sin(a)
        inner += line(bx, by, hx, hy, w=2.4)
        inner += atom(hx, hy, 11, 'H', 10)
    inner += atom(o1x, o1y, 22, 'O')
    inner += text(o1x - 44, o1y - 20, 'δ−', 15, 'var(--cool)', 700)
    # O2: accepting lone pair up-left (toward H of O1), second pair up-right
    inner += lone_dots(o2x, o2y, -135) + lone_dots(o2x, o2y, -45)
    # O2 H atoms: right (0°) and down-left (145°)
    for ang in (0, 145):
        a = math.radians(ang)
        bx, by = o2x + 22 * math.cos(a), o2y + 22 * math.sin(a)
        hx, hy = o2x + 36 * math.cos(a), o2y + 36 * math.sin(a)
        inner += line(bx, by, hx, hy, w=2.4)
        inner += atom(hx, hy, 11, 'H', 10)
    inner += atom(o2x, o2y, 22, 'O')
    inner += text(o2x + 52, o2y - 34, 'δ−', 15, 'var(--cool)', 700, anchor='start')
    # hydrogen bond: O1's down-right H to O2's up-left lone pair
    inner += dash(o1x + 40, o1y + 38, o2x - 34, o2y - 34, w=2.8)
    inner += text(236, 96, 'hydrogen bond', 12, 'var(--acc)', 600)
    inner += text(236, 112, 'O–H···O ≈ 180°', 10.5, 'var(--muted)', 600, family='GeistMono')
    inner += text(14, 24, 'each O: 2 lone pairs — donates 2, accepts 2', 11.5, 'var(--muted)', 500, anchor='start')
    inner += text(14, 246, '2 δ+ H atoms → up to 4 hydrogen bonds per molecule', 12, 'var(--body)', 600, anchor='start')
    return inner

def hbond_geo_ammonia():
    inner = ''
    n1x, n1y, n2x, n2y = 130, 100, 285, 175
    # N1 lone pair straight up
    inner += lone_dots(n1x, n1y, -90)
    inner += text(n1x, 52, 'lone pair', 11.5, 'var(--acc)', 600)
    # N1 H atoms: down-left 135°, down 90°, down-right 45°
    for ang in (135, 90, 45):
        a = math.radians(ang)
        bx, by = n1x + 22 * math.cos(a), n1y + 22 * math.sin(a)
        hx, hy = n1x + 36 * math.cos(a), n1y + 36 * math.sin(a)
        inner += line(bx, by, hx, hy, w=2.4)
        inner += atom(hx, hy, 11, 'H', 10)
    inner += atom(n1x, n1y, 22, 'N')
    # N2 lone pair pointing up-left toward N1's down-right H
    inner += lone_dots(n2x, n2y, 205)
    # N2 H atoms: 25°, 90°, 155°
    for ang in (25, 90, 155):
        a = math.radians(ang)
        bx, by = n2x + 22 * math.cos(a), n2y + 22 * math.sin(a)
        hx, hy = n2x + 36 * math.cos(a), n2y + 36 * math.sin(a)
        inner += line(bx, by, hx, hy, w=2.4)
        inner += atom(hx, hy, 11, 'H', 10)
    inner += atom(n2x, n2y, 22, 'N')
    # hydrogen bond from N1's down-right H to N2 lone pair
    a = math.radians(45)
    hx, hy = n1x + 36 * math.cos(a), n1y + 36 * math.sin(a)
    inner += dash(hx + 4, hy + 2, n2x - 36, n2y - 16, w=2.8)
    inner += text(210, 96, 'hydrogen bond', 12, 'var(--acc)', 600)
    inner += text(hx - 4, hy + 26, 'δ+', 13, 'var(--acc)', 700)
    inner += text(n2x + 30, n2y - 24, 'δ−', 15, 'var(--cool)', 700)
    inner += text(14, 24, 'N has one lone pair to donate', 11.5, 'var(--muted)', 500, anchor='start')
    inner += text(14, 246, 'one lone pair — on average only 2 H-bonds per molecule', 12, 'var(--body)', 600, anchor='start')
    return inner

def hbond_geo_hf():
    inner = ''
    # properly bent zig-zag: each F–H···F angle ≈ 134°
    f1 = (110, 150); h1 = (147, 124); f2 = (191, 132); h2 = (230, 118); f3 = (270, 138)
    for (fx, fy) in (f1, f2, f3):
        inner += atom(fx, fy, 20, 'F')
        inner += text(fx - 6, fy - 30, 'δ−', 14, 'var(--cool)', 700)
    # one lone pair on each F, pointing away from the chain
    inner += lone_dots(f1[0], f1[1], 205, r=20)
    inner += lone_dots(f2[0], f2[1], -90, r=20)
    inner += lone_dots(f3[0], f3[1], -25, r=20)
    inner += line(f1[0] + 19, f1[1] - 5, h1[0] - 8, h1[1] + 3, w=2.4)
    inner += atom(h1[0], h1[1], 11, 'H', 10)
    inner += dash(h1[0] + 9, h1[1] + 3, f2[0] - 17, f2[1] + 3, w=2.8)
    inner += line(f2[0] + 19, f2[1] - 8, h2[0] - 8, h2[1] + 2, w=2.4)
    inner += atom(h2[0], h2[1], 11, 'H', 10)
    inner += dash(h2[0] + 9, h2[1] + 3, f3[0] - 17, f3[1] + 1, w=2.8)
    inner += text(h1[0] - 10, h1[1] + 30, 'δ+', 13, 'var(--acc)', 700)
    inner += text(h2[0] - 12, h2[1] + 30, 'δ+', 13, 'var(--acc)', 700)
    inner += text(h1[0] + 26, h1[1] - 22, '134°', 11, 'var(--muted)', 600, family='GeistMono')
    inner += text(14, 24, 'solid HF: zig-zag chains, written (HF)n', 11.5, 'var(--muted)', 500, anchor='start')
    inner += text(14, 246, 'each HF donates 1 and accepts 1 → chains, not rings', 12, 'var(--body)', 600, anchor='start')
    return inner

def build_hbond_geo(pal):
    body = '<style>%s</style><div class="trio">' % CARD_CSS
    body += ('<div class="card"><div class="ct"><span class="name">water</span><span class="sig">bp 373 K</span></div>'
             '<div class="art" style="padding-top:6px">%s</div></div>' % svg(400, 262, hbond_geo_water()))
    body += ('<div class="card"><div class="ct"><span class="name">ammonia</span><span class="sig">bp 240 K</span></div>'
             '<div class="art" style="padding-top:6px">%s</div></div>' % svg(400, 262, hbond_geo_ammonia()))
    body += ('<div class="card"><div class="ct"><span class="name">hydrogen fluoride</span><span class="sig">bp 293 K</span></div>'
             '<div class="art" style="padding-top:6px">%s</div></div>' % svg(400, 262, hbond_geo_hf()))
    body += '</div>'
    return shell(1328, 560, pal, 'SPEC 7.2 · HYDROGEN BONDING', 'Drawing the hydrogen bond — N, O and F only',
                 body, tag='δ+ H ··· lone pair',
                 footer='The lone pair on N/O/F of one molecule is attracted to the exposed δ+ hydrogen of an '
                        'O–H, N–H or F–H bond in another. The bond is directional — X–H···Y is usually close '
                        'to 180°. Draw the lone pairs and the δ charges every time.',
                 fkey='GEOMETRY')

# ------------------------------------------------------------ hydride graph --
HYD = {
    14: [('CH₄', 112), ('SiH₄', 161), ('GeH₄', 185), ('SnH₄', 221)],
    15: [('NH₃', 240), ('PH₃', 185), ('AsH₃', 211), ('SbH₃', 255)],
    16: [('H₂O', 373), ('H₂S', 213), ('H₂Se', 232), ('H₂Te', 271)],
    17: [('HF', 293), ('HCl', 188), ('HBr', 206), ('HI', 238)],
}
ANOM = {('H₂O', 373), ('NH₃', 240), ('HF', 293)}

def build_hydrides(pal):
    W, H = 1090, 430
    ox, oy = 96, 368
    sx, sy = (W - 190) / 3.6, (H - 90) / 400.0
    def X(p): return ox + (p - 2) * sx
    def Y(t): return oy - t * sy
    inner = ''
    # grid + axes
    for t in (100, 200, 300, 400):
        inner += line(ox, Y(t), W - 80, Y(t), w=1, color='var(--faint)')
        inner += text(ox - 14, Y(t) + 4, str(t), 11.5, 'var(--muted)', 500, anchor='end', family='GeistMono')
    inner += line(ox, oy, ox, Y(430), w=2, color='var(--muted)')
    inner += line(ox, oy, W - 70, oy, w=2, color='var(--muted)')
    inner += ('<text transform="rotate(-90 34 220)" x="34" y="220" text-anchor="middle" '
              'style="font-family:GeistMono;font-size:12.5px;font-weight:600;fill:var(--muted);'
              'letter-spacing:.05em">boiling temperature / K</text>')
    for p in (2, 3, 4, 5):
        inner += text(X(p), oy + 24, 'period %d' % p, 11.5, 'var(--muted)', 500, family='GeistMono')
    colors = {14: 'var(--muted)', 15: 'var(--cool)', 16: 'var(--acc)', 17: 'var(--ink)'}
    below = {14: True, 15: True, 16: False, 17: False}  # label side per series
    for g, series in HYD.items():
        pts = [(X(2 + i), Y(t)) for i, (_, t) in enumerate(series)]
        inner += polyline(pts, w=2.8, color=colors[g])
        for i, ((nm, t), (px, py)) in enumerate(zip(series, pts)):
            isanom = (nm, t) in ANOM
            inner += ('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s" stroke="var(--diafill)" stroke-width="2"/>'
                      % (px, py, 6 if isanom else 4.4, 'var(--acc)' if isanom else colors[g]))
            if isanom:
                inner += text(px + 12, py - 12, '%s  %d K' % (nm, t), 12.5, 'var(--acc)', 700, anchor='start')
            else:
                inner += text(px, py + (20 if below[g] else -15), nm, 10.5, 'var(--muted)', 500)
        # series label to the right of the line end
        ex, ey = pts[-1]
        inner += text(W - 84, ey + 4, 'Group %d' % g, 12.5, colors[g], 700, anchor='end')
    body = '<style>%s</style><div class="card" style="margin-top:20px;flex:1">' \
           '<div class="art" style="padding:6px 6px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner))
    return shell(1248, 620, pal, 'SPEC 7.3 · THE HYDRIDE GRAPH',
                 'Boiling temperatures of the hydrides — three anomalies',
                 body, tag='H₂O · NH₃ · HF',
                 footer='Along every series the boiling temperature climbs as the electron cloud grows — but '
                        'H₂O, NH₃ and HF sit far above their group trends. Their molecules are hydrogen bonded '
                        'in addition to London forces, and the extra forces need more energy to break.',
                 fkey='EVIDENCE')
