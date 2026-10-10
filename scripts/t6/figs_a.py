#!/usr/bin/env python3
"""Topic 6 plates, set A: enthalpy level diagrams, reaction profiles, cooling curve."""
import math
from common import shell, svg, text, line, polyline, arrow_marker

CARD_CSS = """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
.card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 12px;min-height:0}
.card .ct{display:flex;align-items:baseline;gap:10px}
.card .ct .name{font-weight:600;font-size:15.5px;color:var(--ink);letter-spacing:-.01em}
.card .ct .sig{font-family:'GeistMono',monospace;font-size:11.5px;font-weight:600;
  color:var(--acc);letter-spacing:.06em;margin-left:auto}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.card .art svg{max-width:100%;max-height:100%}
"""

def axis_v(x, y0, y1, w=2.2):
    """Vertical axis arrow from y0 (bottom) to y1 (top)."""
    return (line(x, y0, x, y1 + 10, w=w, color='var(--muted)')
            + '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="var(--muted)"/>'
              % (x - 5, y1 + 11, x + 5, y1 + 11, x, y1))

def axis_h(x0, x1, y, w=2.2):
    return (line(x0, y, x1 - 10, y, w=w, color='var(--muted)')
            + '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="var(--muted)"/>'
              % (x1 - 11, y - 5, x1 - 11, y + 5, x1, y))

def darrow(x, y0, y1, color='var(--acc)', w=3.4):
    """Vertical double-headed measurement arrow between y0 and y1."""
    s = 6.0
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f"/>'
            % (x, y0, x, y1, color, w)
            + '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="%s"/>'
              % (x - s, y0 + s * 1.6, x + s, y0 + s * 1.6, x, y0, color)
            + '<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="%s"/>'
              % (x - s, y1 - s * 1.6, x + s, y1 - s * 1.6, x, y1, color))

def rot_label(x, y, s, size=12):
    return ('<text transform="rotate(-90 %d %d)" x="%d" y="%d" text-anchor="middle" '
            'style="font-family:GeistMono;font-size:%.1fpx;font-weight:500;fill:var(--muted);'
            'letter-spacing:.05em">%s</text>' % (x, y, x, y + 4, size, s))

def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)

def bump(x0, y0, x1, y1, x2, y2, n=56):
    """Smooth curve: flat shoulder at (x0,y0), hump peak (x1,y1), plateau (x2,y2)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        # flat shoulder for the first 26%, then rise
        u = ease(max(0.0, (t - 0.26) / 0.74)) if t > 0.26 else 0.0
        pts.append((x, y0 + (y1 - y0) * u))
    for i in range(1, n + 1):
        t = i / n
        x = x1 + (x2 - x1) * t
        u = ease(min(1.0, t / 0.74))  # settle on the plateau, flat tail
        pts.append((x, y1 + (y2 - y1) * u))
    return polyline(pts, w=3.4, color='var(--ink)')

def sub_text(x, y, main, sub_, size, color, weight=600, anchor='start'):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" style="font-family:Geist;'
            'font-size:%.1fpx;font-weight:%d;fill:%s">%s'
            '<tspan dy="3.2" style="font-size:.68em">%s</tspan></text>'
            % (x, y, anchor, size, weight, color, main, sub_))

# ---------------------------------------------------------- enthalpy levels ----
def level_diagram(exo=True):
    W, H = 470, 292
    ax_x = 92
    y_r, y_p = (74, 216) if exo else (216, 74)
    inner = axis_v(ax_x, 252, 36)
    inner += rot_label(ax_x - 58, 150, 'Enthalpy, H')
    lx0, lx1 = 150, 428
    inner += line(lx0, y_r, lx1, y_r, w=3.4, color='var(--ink)')
    inner += line(lx0 + 26, y_p, lx1, y_p, w=3.4, color='var(--ink)')
    inner += text(lx0 + 22, y_r - 13, 'Reactants', size=14.5, weight=600, anchor='start')
    inner += text(lx0 + 48, y_p + 27, 'Products', size=14.5, weight=600, anchor='start')
    ax_ = 352
    inner += darrow(ax_, y_r, y_p)
    inner += text(ax_ + 16, (y_r + y_p) / 2 + 5, 'ΔH &lt; 0' if exo else 'ΔH &gt; 0',
                  size=15.5, color='var(--acc)', weight=600, anchor='start')
    return svg(W, H, inner)

def build_levels(pal):
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="duo" style="margin-top:22px">'
            + '<div class="card"><div class="ct"><span class="name">Exothermic</span>'
              '<span class="sig">ΔH &lt; 0</span></div><div class="art">%s</div></div>'
            % level_diagram(exo=True)
            + '<div class="card"><div class="ct"><span class="name">Endothermic</span>'
              '<span class="sig">ΔH &gt; 0</span></div><div class="art">%s</div></div>'
            % level_diagram(exo=False)
            + '</div>')
    return shell(1248, 500, pal, 'SPEC 6.3 · ENTHALPY LEVEL DIAGRAMS',
                 'Enthalpy level diagrams — exothermic and endothermic',
                 body, tag='construct &amp; interpret',
                 footer='Only the difference between the two levels matters — an enthalpy level '
                        'diagram has no zero and no scale. The ΔH arrow points down for exothermic, '
                        'up for endothermic.',
                 fkey='HOW TO READ')

# -------------------------------------------------------- reaction profiles ----
def profile_diagram(exo=True):
    W, H = 470, 316
    ax_x, ax_y = 84, 268
    inner = axis_v(ax_x, ax_y, 32) + axis_h(ax_x, 444, ax_y)
    inner += rot_label(ax_x - 54, 142, 'Potential energy')
    inner += text(266, ax_y + 22, 'Reaction progress', size=12, color='var(--muted)',
                  family='GeistMono', weight=500)
    x0 = 126
    if exo:
        y_r, y_p, y_peak = 118, 220, 54
    else:
        y_r, y_p, y_peak = 220, 120, 54
    inner += bump(x0, y_r, x0 + 150, y_peak, x0 + 292, y_p)
    # dashed reference levels
    inner += line(x0 - 12, y_r, x0 + 96, y_r, w=1.5, color='var(--muted)', dash='5 5')
    inner += line(x0 + 200, y_p, x0 + 316, y_p, w=1.5, color='var(--muted)', dash='5 5')
    # labels: reactants below its dashed level, products above its dashed level
    inner += text(x0 - 14, y_r + 27, 'Reactants', size=14.5, weight=600, anchor='start')
    inner += text(x0 + 254, y_p - 13, 'Products', size=14.5, weight=600, anchor='start')
    # Ea arrow (reactant level -> peak)
    eax = x0 + 150
    inner += darrow(eax, y_r, y_peak, color='var(--acc)', w=3.0)
    inner += sub_text(eax + 12, (y_r + y_peak) / 2 + 5, 'E', 'a', 15, 'var(--acc)')
    # ΔH arrow (reactant level -> product level)
    dhx = x0 + 292
    inner += darrow(dhx, y_r, y_p, color='var(--acc)', w=3.0)
    inner += text(dhx + 14, (y_r + y_p) / 2 + 5, 'ΔH &lt; 0' if exo else 'ΔH &gt; 0',
                  size=14.5, color='var(--acc)', weight=600, anchor='start')
    return svg(W, H, inner)

def build_profiles(pal):
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="duo" style="margin-top:22px">'
            + '<div class="card"><div class="ct"><span class="name">Exothermic profile</span>'
              '<span class="sig">ΔH &lt; 0</span></div><div class="art">%s</div></div>'
            % profile_diagram(exo=True)
            + '<div class="card"><div class="ct"><span class="name">Endothermic profile</span>'
              '<span class="sig">ΔH &gt; 0</span></div><div class="art">%s</div></div>'
            % profile_diagram(exo=False)
            + '</div>')
    return shell(1248, 560, pal, 'SPEC 6.3 · REACTION PROFILES',
                 'Reaction profiles — the activation energy hump',
                 body, tag='Ea + ΔH',
                 footer='Ea is measured from the reactant level to the top of the hump — the energy '
                        'barrier that must be overcome. ΔH is measured between the reactant and '
                        'product levels.',
                 fkey='HOW TO READ')

# --------------------------------------------------------------- cooling curve ----
def build_cooling(pal):
    W, H = 1096, 348
    ax_x, ax_y = 78, 292
    inner = axis_v(ax_x, ax_y, 30) + axis_h(ax_x, 1058, ax_y)
    inner += rot_label(ax_x - 46, 156, 'Temperature / °C')
    # time -> x mapping: 0..9 min over 120..1020 px
    def X(t):
        return 120 + t * 100.0
    # temperature -> y mapping: 0..70 °C over 280..40 px
    def Y(temp):
        return 280 - temp * (240.0 / 70.0)
    # before mixing: 20.2 -> 20.0 (essentially steady), 0..3 min
    before = [(X(3.0 * i / 25.0), Y(20.2 - 0.2 * (i / 25.0))) for i in range(26)]
    inner += polyline(before, w=3.0, color='var(--ink)')
    # rise from (3.0, 20) to peak (4.0, 60)
    rise = []
    for i in range(25):
        t = i / 24
        x = X(3.0 + t)
        u = ease(t)
        rise.append((x, Y(20.0 + (60.0 - 20.0) * u)))
    inner += polyline(rise, w=3.4, color='var(--ink)')
    # cooling 4..9 min: 60 -> 43 decaying (exponential-ish)
    cool = []
    for i in range(51):
        t = i / 50
        tm = 4.0 + 5.0 * t
        temp = 43.0 + (60.0 - 43.0) * math.exp(-2.2 * t) * (1 + 0.0)
        # start matches 60 at t=0
        cool.append((X(tm), Y(temp)))
    inner += polyline(cool, w=3.4, color='var(--ink)')
    # extrapolated cooling line (dashed accent) back to mixing time 3.0
    # slope from cooling curve near t=4..5: linear approx from (4.0,60) to (9.0,44.2)
    slope = (44.2 - 60.0) / 5.0
    ex_pts = [(X(3.0), Y(60.0 - 1.0 * slope)), (X(4.0), Y(60.0))]
    inner += polyline(ex_pts, w=2.0, color='var(--acc)')
    # dashed before-line continuation to 3.0 handled; mixing guide line
    inner += line(X(3.0), ax_y, X(3.0), Y(64.5), w=1.5, color='var(--muted)', dash='5 5')
    # ΔT bracket at t = 3.0 between before-line (20.0) and extrapolated point
    xt = X(3.0)
    inner += darrow(xt - 46, Y(20.0), Y(60.0 - 1.0 * slope), color='var(--acc)', w=2.6)
    inner += text(xt - 58, (Y(20.0) + Y(60.0 - slope)) / 2 + 5, 'ΔT', size=15,
                  color='var(--acc)', weight=700, anchor='end')
    # labels
    inner += text(X(0.08), Y(15.0), 'before mixing — steady', size=12.5,
                  color='var(--body)', weight=500, anchor='start')
    inner += text(X(6.7), Y(50.0) - 14, 'after mixing — the mixture cools', size=12.5,
                  color='var(--body)', weight=500)
    inner += text(X(4.15), Y(63.0), 'cooling line extrapolated back', size=12,
                  color='var(--acc)', weight=600, anchor='start')
    inner += text(X(3.0), Y(66.5), 'mix at 3.0 min', size=12,
                  color='var(--muted)', weight=600, family='GeistMono')
    # tick labels on time axis
    for t in (0, 3, 9):
        inner += text(X(t), ax_y + 18, str(t), size=11, color='var(--muted)',
                      family='GeistMono', weight=500)
    inner += text(700, ax_y + 18, 'Time / min', size=12, color='var(--muted)',
                  family='GeistMono', weight=500)
    body = '<style>%s</style><div class="card" style="margin-top:20px;flex:1">' \
           '<div class="art" style="padding:6px 4px 4px">%s</div></div>' % (CARD_CSS, svg(W, H, inner))
    return shell(1248, 560, pal, 'SPEC 6.8 · COOLING CURVE CORRECTION',
                 'The graphical method — correcting for heat loss',
                 body, tag='cooling correction',
                 footer='Temperature every half minute before mixing · mix at 3.0 min · keep reading '
                        'as the mixture cools · extrapolate both lines back to the moment of mixing '
                        'and read ΔT there — the extrapolation compensates for heat lost to the '
                        'surroundings.',
                 fkey='METHOD')

LEVELS = ('enthalpy-level-diagrams', 1248, 500, build_levels)
PROFILES = ('reaction-profiles', 1248, 560, build_profiles)
COOLING = ('cooling-curve', 1248, 560, build_cooling)
