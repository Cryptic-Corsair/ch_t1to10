#!/usr/bin/env python3
"""Topic 9B (Equilibria) figure plates — built on the approved Topic 4/6/7/8/9A pipeline."""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
from common import LIGHT, DARK, shell, svg, line, polyline, arrow, text  # noqa: E402,F401

GRID_CSS = """
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


def card(name, art, sig=None, sub=None):
    s = '<div class="sig">%s</div>' % sig if sig else ''
    sb = '<div class="sub">%s</div>' % sub if sub else ''
    return ('<div class="card"><div class="ct"><span class="name">%s</span>%s</div>'
            '<div class="art">%s</div>%s</div>' % (name, s, art, sb))


def rot(x, y, s, size=10.5):
    """Rotated (bottom-to-top) mono label for multi-line y-axis titles."""
    return ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
            'style="font-family:GeistMono;font-size:%.1fpx;font-weight:600;fill:var(--body);letter-spacing:1px">%s</text>'
            % (x, y, x, y, size, s))


def axes2(x0, y0, w, h, xlabel, ylabel, xlabel_y=26):
    """L-shaped axis; origin (x0,y0) bottom-left; returns svg fragment."""
    out = line(x0, y0, x0 + w, y0, w=2, color='var(--ink)')
    out += line(x0, y0, x0, y0 - h, w=2, color='var(--ink)')
    if xlabel:
        out += text(x0 + w / 2, y0 + xlabel_y, xlabel, 12.5, 'var(--body)', 600, family='GeistMono', spacing=1)
    if ylabel:
        out += ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
                'style="font-family:GeistMono;font-size:11.5px;font-weight:600;fill:var(--body);letter-spacing:1px">%s</text>'
                % (x0 - 30, y0 - h / 2, x0 - 30, y0 - h / 2, ylabel))
    return out


def ytick(x0, y, label, cool=False):
    col = 'var(--cool)' if cool else 'var(--muted)'
    return (line(x0 - 6, y, x0, y, w=1.4, color=col)
            + text(x0 - 12, y + 4, label, 11, col, 600, family='GeistMono', anchor='end'))


def xtick(x, y0, label, cool=False):
    col = 'var(--cool)' if cool else 'var(--muted)'
    return (line(x, y0, x, y0 + 6, w=1.4, color=col)
            + text(x, y0 + 22, label, 11, col, 600, family='GeistMono'))


# --------------------------------------- 1 · how equilibrium is established ----
def build_established_rates(pal):
    W, H = 540, 300

    def forward():
        x0, y0, w, h = 56, 252, 440, 190
        s = axes2(x0, y0, w, h, 'Time', 'Reaction rate')
        pts = []
        for i in range(61):
            t = i / 60.0
            y = y0 - (0.32 + 0.60 * math.exp(-3.2 * t)) * h
            pts.append((x0 + t * w, y))
        s += polyline(pts, w=2.8, color='var(--ink)')
        s += arrow(x0 + 128, y0 - 0.80 * h, x0 + 236, y0 - 0.52 * h, w=1.8, color='var(--acc)', marker='arwacc')
        s += text(x0 + 244, y0 - 0.62 * h, 'rate of A + B reaction', 12, 'var(--acc)', 700, anchor='start')
        s += text(x0 + 244, y0 - 0.62 * h + 16, 'falls with time', 12, 'var(--acc)', 700, anchor='start')
        return svg(W, H, s)

    def backward():
        x0, y0, w, h = 56, 252, 440, 190
        s = axes2(x0, y0, w, h, 'Time', 'Reaction rate')
        pts = []
        for i in range(61):
            t = i / 60.0
            y = y0 - (1 - math.exp(-2.9 * t)) * h * 0.88
            pts.append((x0 + t * w, y))
        s += polyline(pts, w=2.8, color='var(--ink)')
        s += arrow(x0 + 92, y0 - 0.30 * h, x0 + 188, y0 - 0.58 * h, w=1.8, color='var(--acc)', marker='arwacc')
        s += text(x0 + 200, y0 - 0.36 * h, 'rate of C + D reaction', 12, 'var(--acc)', 700, anchor='start')
        s += text(x0 + 200, y0 - 0.36 * h + 16, 'increases with time', 12, 'var(--acc)', 700, anchor='start')
        s += text(x0 + 220, y0 + 44, 'A + B  \u21cc  C + D', 12.5, 'var(--body)', 600, family='GeistMono')
        return svg(W, H, s)

    body = ('<style>%s</style><div class="duo">%s%s</div>'
            % (GRID_CSS, card('Rate of the forward reaction', forward(), sig='FIG A'),
               card('Rate of the backward reaction', backward(), sig='FIG B')))
    return shell(1340, 610, pal, 'SPEC 9.9 · HOW IS EQUILIBRIUM ESTABLISHED?',
                 'One rate falls, the other rises — until they are equal', body,
                 tag='A + B \u21cc C + D',
                 footer='As the reaction continues the concentration of the reactants decreases and the rate of the '
                        'forward reaction also decreases · the rate of the backward reaction is initially slow — as '
                        'the concentration of the product increases it increases too · eventually the two rates become '
                        'equal: a dynamic equilibrium has been reached.',
                 fkey='FORWARD vs BACKWARD')


# ------------------------------------------------------ 2 · fig A curve ----
def build_dynamic_equilibrium(pal):
    W, H = 760, 380
    x0, y0, w, h = 96, 312, 590, 258
    s = axes2(x0, y0, w, h, 'Time', 'Rate of reaction')
    ye = 0.32 * h
    xm = 0.42 * w

    pts_f = []
    for i in range(101):
        t = xm * i / 100.0
        y = ye + (0.95 * h - ye) * math.exp(-3.4 * i / 100.0)
        pts_f.append((x0 + t, y0 - y))
    pts_b = []
    for i in range(101):
        t = xm * i / 100.0
        y = ye * (1 - math.exp(-3.2 * i / 100.0))
        pts_b.append((x0 + t, y0 - y))
    s += polyline(pts_f, w=2.8, color='var(--acc)')
    s += polyline(pts_b, w=2.8, color='var(--cool)')
    s += line(x0 + xm, y0 - ye, x0 + w, y0 - ye, w=2.8, color='var(--accmid)')
    s += text(x0 + 96, y0 - 0.80 * h, 'forward reaction', 12.5, 'var(--acc)', 700, anchor='start')
    s += text(x0 + 120, y0 - 0.10 * h, 'backward reaction', 12.5, 'var(--cool)', 700, anchor='start')
    s += arrow(x0 + w * 0.62, y0 - ye - 74, x0 + w * 0.55, y0 - ye - 10, w=1.5, color='var(--muted)')
    s += text(x0 + w * 0.63, y0 - ye - 84, 'equilibrium established', 12.5, 'var(--body)', 700, anchor='start')
    s += text(x0 + w * 0.63, y0 - ye - 68, 'rates equal · concentrations constant', 11.5,
              'var(--muted)', 600, anchor='start', family='GeistMono')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Rate of reaction against time', svg(W, H, s), sig='FIG A'))
    return shell(1300, 620, pal, 'SPEC 9.9 · DYNAMIC EQUILIBRIUM',
                 'Forward and backward rates become equal', body, tag='closed system',
                 footer='Two conditions must be met: the reaction must be reversible, and the reaction mixture must '
                        'be in a closed container · the reactions continue to occur in both directions · the '
                        'concentrations of the reactants and products remain constant · rate of the forward reaction '
                        'is equal to the rate of the backward reaction.',
                 fkey='FIG A')


# ------------------------------------------- 3 · chromate / dichromate beakers ----
def _beaker(x0, ytop, w, hgt, fill):
    """Open beaker with liquid; returns svg fragment."""
    s = ''
    lip = 10
    s += ('<path d="M%.0f,%.0f L%.0f,%.0f Q%.0f,%.0f %.0f,%.0f L%.0f,%.0f Q%.0f,%.0f %.0f,%.0f L%.0f,%.0f" '
          'fill="none" stroke="var(--ink)" stroke-width="2.2" stroke-linecap="round"/>'
          % (x0 - lip, ytop, x0, ytop + 14, x0, ytop + 18, x0, ytop + hgt,
             x0 + w, ytop + hgt, x0 + w, ytop + 18, x0 + w, ytop + 14, x0 + w + lip, ytop))
    liq_h = hgt * 0.42
    lx0, lx1 = x0 + 5, x0 + w - 5
    yliq = ytop + hgt - liq_h
    s += ('<path d="M%.0f,%.0f L%.0f,%.0f Q%.0f,%.0f %.0f,%.0f L%.0f,%.0f Q%.0f,%.0f %.0f,%.0f L%.0f,%.0f Z" '
          'fill="%s" fill-opacity=".75"/>'
          % (lx0, yliq, lx0, ytop + hgt - 6, lx0, ytop + hgt, lx0 + 8, ytop + hgt,
             lx1 - 8, ytop + hgt, lx1, ytop + hgt, lx1, ytop + hgt - 6, lx1, yliq, fill))
    return s


def build_chromate(pal):
    W, H = 880, 340
    s = ''
    bw, bh = 210, 190
    ytop = 44
    yel = '#e3c94f' if pal is DARK else '#edd44f'
    org = '#e8934f' if pal is DARK else '#e2893d'
    bx1, bx2 = 90, 560
    s += _beaker(bx1, ytop, bw, bh, yel)
    s += _beaker(bx2, ytop, bw, bh, org)
    s += text(bx1 + bw / 2, ytop + bh - 56, 'CrO\u2084\u00b2\u207b(aq)', 14.5, 'var(--ink)', 700)
    s += text(bx1 + bw / 2, ytop + bh + 26, 'yellow', 13, 'var(--body)', 600, family='GeistMono')
    s += text(bx2 + bw / 2, ytop + bh - 56, 'Cr\u2082O\u2087\u00b2\u207b(aq)', 14.5, 'var(--ink)', 700)
    s += text(bx2 + bw / 2, ytop + bh + 26, 'orange', 13, 'var(--body)', 600, family='GeistMono')
    s += text((bx1 + bw + bx2) / 2, ytop + bh - 74, '\u21cc', 44, 'var(--acc)', 700)
    s += text(bx1 + bw / 2, ytop - 14, 'chromate(VI)', 11.5, 'var(--muted)', 600, family='GeistMono')
    s += text(bx2 + bw / 2, ytop - 14, 'dichromate(VI)', 11.5, 'var(--muted)', 600, family='GeistMono')
    s += text(W / 2, 300, '2CrO\u2084\u00b2\u207b(aq)  +  2H\u207a(aq)   \u21cc   Cr\u2082O\u2087\u00b2\u207b(aq)  +  H\u2082O(l)',
              16, 'var(--ink)', 600)
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Chromate(VI) ions and dichromate(VI) ions in solution', svg(W, H, s),
                       sig='CrO\u2084\u00b2\u207b / Cr\u2082O\u2087\u00b2\u207b'))
    return shell(1300, 590, pal, 'SPEC 9.10 · CHANGING THE POSITION OF EQUILIBRIUM',
                 'Chromate(VI) — dichromate(VI) equilibrium', body, tag='concentration',
                 footer='If acid (H\u207a) is added to the system, equilibrium moves to the right and the solution '
                        'becomes orange · if alkali (OH\u207b) is added to the system, equilibrium moves to the left '
                        'and the solution becomes yellow.',
                 fkey='YELLOW \u21cc ORANGE')


# ------------------------------------- 4 · % ammonia vs pressure (9.10) ----
def build_ammonia_pressure(pal):
    W, H = 780, 400
    x0, y0, w, h = 110, 318, 580, 250
    s = axes2(x0, y0, w, h, 'Pressure/atm', '', xlabel_y=46)
    s += rot(x0 - 44, y0 - h / 2 + 50, 'Percentage of ammonia')
    s += rot(x0 - 30, y0 - h / 2 + 50, 'in equilibrium mixture')
    for gy in (0, 20, 40, 60, 80, 100):
        yy = y0 - gy / 100.0 * h
        s += ytick(x0, yy, str(gy))
        if gy:
            s += line(x0, yy, x0 + w, yy, w=0.8, color='var(--faint)')
    for gx in (0, 100, 200, 300, 400, 500, 600):
        s += xtick(x0 + gx / 620.0 * w, y0, str(gx))
    data = ((0, 0), (50, 12), (100, 25), (150, 39), (200, 52), (250, 62), (300, 70),
            (350, 76), (400, 80), (450, 83), (500, 85.5), (550, 87), (600, 88.5))
    pts = [(x0 + P / 620.0 * w, y0 - pc / 100.0 * h) for P, pc in data]
    s += polyline(pts, w=2.8, color='var(--acc)')
    s += text(x0 + 380, y0 - 0.30 * h, 'at high pressure more ammonia', 12, 'var(--acc)', 700, anchor='start')
    s += text(x0 + 380, y0 - 0.30 * h + 16, 'is produced at equilibrium', 12, 'var(--acc)', 700, anchor='start')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Effect of pressure changes — nitrogen and hydrogen to form ammonia',
                       svg(W, H, s), sig='N\u2082 + 3H\u2082 \u21cc 2NH\u2083'))
    return shell(1300, 640, pal, 'SPEC 9.10 · EFFECT OF PRESSURE',
                 'Percentage of ammonia in the equilibrium mixture against pressure', body,
                 tag='4 moles \u21cc 2 moles',
                 footer='At high pressure more ammonia is produced at equilibrium · high pressure shifts equilibrium '
                        'to the side having fewer moles of gas.',
                 fkey='PRESSURE \u2191')


# --------------------------------------------- 5 · Haber yield vs T and P ----
def build_haber_yield(pal):
    W, H = 800, 420
    x0, y0, w, h = 104, 330, 540, 268
    s = axes2(x0, y0, w, h, 'Pressure/atm', '', xlabel_y=46)
    s += rot(x0 - 44, y0 - h / 2 + 50, 'Percentage')
    s += rot(x0 - 30, y0 - h / 2 + 50, 'yield of ammonia')

    def X(P):
        return x0 + P / 430.0 * w

    def Y(pc):
        return y0 - pc / 75.0 * h

    for gy in range(10, 80, 10):
        s += ytick(x0, Y(gy), str(gy))
        s += line(x0, Y(gy), x0 + w, Y(gy), w=0.8, color='var(--faint)')
    for gx in (0, 100, 200, 300, 400):
        s += xtick(X(gx), y0, str(gx))
    s += line(X(250), y0, X(250), y0 + 6, w=1.4, color='var(--cool)')

    k = 0.001237
    for T, yv in ((350, 68), (400, 57), (450, 44), (500, 35), (550, 26)):
        a = yv / (1 - math.exp(-400 * k))
        pts = []
        for i in range(101):
            P = 400.0 * i / 100.0
            pts.append((X(P), Y(a * (1 - math.exp(-k * P)))))
        s += polyline(pts, w=2.5, color='var(--acc)')
        s += text(X(400) + 12, Y(a * (1 - math.exp(-400 * k))) + 4, '%d \u00b0C' % T, 12,
                  'var(--acc)' if T == 450 else 'var(--body)', 700 if T == 450 else 600, anchor='start')
    a450 = 44 / (1 - math.exp(-400 * k))
    s += line(x0, Y(30), X(250), Y(30), w=1.3, color='var(--cool)', dash='4 4')
    s += line(X(250), y0, X(250), Y(30), w=1.3, color='var(--cool)', dash='4 4')
    s += ytick(x0, Y(30), '30', cool=True)
    s += text(X(125), Y(30) - 10, '450 \u00b0C at 250 atm', 11, 'var(--cool)', 700, anchor='middle', family='GeistMono')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('The graph shows the equilibrium yield of ammonia at different temperatures and pressures',
                       svg(W, H, s), sig='\u0394H = \u221292.4 kJ mol\u207b\u00b9'))
    return shell(1300, 660, pal, 'SPEC 9.11 · THE HABER PROCESS',
                 'N\u2082(g) + 3H\u2082(g) \u21cc 2NH\u2083(g)', body, tag='low T · high P = max yield',
                 footer='If the reaction mixture were to reach equilibrium, maximum yield is obtained by low '
                        'temperature (forward reaction is exothermic) and high pressure · conditions used: '
                        'temperature 450 \u00b0C, pressure 250 atm — a compromise between yield and rate.',
                 fkey='350 – 550 \u00b0C')


# ----------------------------------------- 6 · Contact yield vs temperature ----
def build_contact_yield(pal):
    W, H = 780, 400
    x0, y0, w, h = 110, 318, 580, 250
    s = axes2(x0, y0, w, h, 'Temperature/\u00b0C', '', xlabel_y=46)
    s += rot(x0 - 44, y0 - h / 2 + 50, 'Percentage')
    s += rot(x0 - 30, y0 - h / 2 + 50, 'yield of SO\u2083')

    def X(T):
        return x0 + (T - 320) / 350.0 * w

    def Y(pc):
        return y0 - (pc - 78) / 24.0 * h

    for gy in (80, 85, 90, 95, 100):
        s += ytick(x0, Y(gy), str(gy))
        if gy != 80:
            s += line(x0, Y(gy), x0 + w, Y(gy), w=0.8, color='var(--faint)')
    for gx in (350, 450, 550, 650):
        s += xtick(X(gx), y0, str(gx))
    s += xtick(X(450), y0, '450', cool=True)
    pts = [(X(350), Y(100)), (X(400), Y(99)), (X(450), Y(97)), (X(500), Y(93)),
           (X(550), Y(86)), (X(600), Y(80)), (X(645), Y(77.5))]
    s += polyline(pts, w=2.8, color='var(--acc)')
    s += line(x0, Y(97), X(450), Y(97), w=1.3, color='var(--cool)', dash='4 4')
    s += line(X(450), y0, X(450), Y(97), w=1.3, color='var(--cool)', dash='4 4')
    s += ytick(x0, Y(97), '97', cool=True)
    s += text(x0 + 14, Y(97) - 8, '97% at 450 \u00b0C, 1 atm', 11, 'var(--cool)', 700, anchor='start',
              family='GeistMono')
    body = '<style>%s</style><div class="duo" style="grid-template-columns:1fr">%s</div>' % (
        GRID_CSS, card('Graph showing the percentage yield of sulphur trioxide against temperature, '
                       'at a pressure of 1 atm', svg(W, H, s), sig='\u0394H = \u221296 kJ mol\u207b\u00b9'))
    return shell(1300, 640, pal, 'SPEC 9.11 · THE CONTACT PROCESS',
                 'SO\u2082(g) + \u00bdO\u2082(g) \u21cc SO\u2083(g)', body, tag='450 \u00b0C · 1 atm',
                 footer='Since the forward reaction is exothermic, low temperature would result in a high yield of '
                        'SO\u2083(g) · at 1 atm pressure the yield is already very high at 97% · conditions used: '
                        'temperature 450 \u00b0C, pressure 2 atm.',
                 fkey='VANADIUM(V) OXIDE CATALYST')
