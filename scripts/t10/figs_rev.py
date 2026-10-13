#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Topic 10 revision figure plates — the diagrams the source notes carry that
the rebuild was missing: labelled apparatus (distillation, reflux, fractional,
separating funnel, boiling point), alcohol bond angles, the C4H9Br reaction
scheme, ethane fragmentation and the pentane spectrum.
Same plate system as the approved Topic 6-10 sets."""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t10')
from common import LIGHT, DARK, shell, svg, line, polyline, arrow, text  # noqa: E402

GRID_CSS = """
.duo{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:16px;min-height:0}
.duo2{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:16px;min-height:0}
.card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:14px 18px 12px;min-height:0}
.card .ct{display:flex;align-items:baseline;gap:8px}
.card .ct .name{font-weight:600;font-size:14.5px;color:var(--ink);letter-spacing:-.01em;white-space:nowrap}
.card .ct .sig{font-family:'GeistMono',monospace;font-size:10.5px;font-weight:600;
  color:var(--acc);letter-spacing:.05em;margin-left:auto;white-space:nowrap}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin-top:6px}
.card .art svg{max-width:100%;max-height:100%}
.card .sub{color:var(--body);font-size:12px;line-height:1.45;margin-top:8px}
.stack{display:flex;flex-direction:column;gap:14px;min-height:0}
.center{display:flex;align-items:center;justify-content:center;min-width:0;min-height:0}
.center svg{max-width:100%;max-height:100%}
.note{border:1px solid var(--accmid);border-radius:12px;background:var(--accsoft);
  padding:10px 16px;color:var(--ink);font-size:12.5px;line-height:1.45;margin-top:14px}
.note b{color:var(--acc)}
"""


def card(name, art, sig=None, sub=None):
    s = '<div class="sig">%s</div>' % sig if sig else ''
    sb = '<div class="sub">%s</div>' % sub if sub else ''
    return ('<div class="card"><div class="ct"><span class="name">%s</span>%s</div>'
            '<div class="art">%s</div>%s</div>' % (name, s, art, sb))


def txt(x, y, s, size=14, color='var(--ink)', weight=500, anchor='middle',
        family='Geist', italic=False):
    return text(x, y, s, size, color, weight, anchor, family, None, italic)


def lead(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, w=1.1, color='var(--faint)')


def lbl(x, y, s, anchor='start', size=12, col='var(--ink)'):
    return txt(x, y, s, size, col, 600, anchor)


def bond(x1, y1, x2, y2, w=2.2):
    return line(x1, y1, x2, y2, w=w, color='var(--ink)')


def lonepair(x, y, ang, ln=9, gap=7, color='var(--acc)', w=2.2):
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    s = ''
    for off in (-gap / 2, gap / 2):
        s += line(x + px * off, y + py * off, x + px * off + dx * ln, y + py * off + dy * ln,
                  w=w, color=color)
    return s


def flask_round(cx, cy, r, liquid=True):
    s = ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--card2)" stroke="var(--ink)" '
         'stroke-width="2.2"/>' % (cx, cy, r))
    if liquid:
        s += ('<path d="M%.2f,%.2f A%.2f,%.2f 0 0 0 %.2f,%.2f Z" fill="var(--accsoft)"/>'
              % (cx - r * 0.82, cy + r * 0.45, r * 0.82, r * 0.82,
                 cx + r * 0.82, cy + r * 0.45))
        s += line(cx - r * 0.82, cy + r * 0.45, cx + r * 0.82, cy + r * 0.45,
                  w=1.6, color='var(--accmid)')
    return s


def flask_pear(cx, cy, r):
    s = ('<path d="M %.1f,%.1f C %.1f,%.1f %.1f,%.1f %.1f,%.1f '
         'C %.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="var(--card2)" stroke="var(--ink)" stroke-width="2.2"/>'
         % (cx - r * 0.42, cy - r * 0.55,
            cx - r * 0.55, cy + r * 0.1, cx - r * 0.98, cy + r * 0.42, cx - r * 0.45, cy + r * 0.98,
            cx + r * 0.45, cy + r * 0.98, cx + r * 0.98, cy + r * 0.42, cx + r * 0.42, cy - r * 0.55))
    s += ('<path d="M%.2f,%.2f A%.2f,%.2f 0 0 0 %.2f,%.2f Z" fill="var(--accsoft)"/>'
          % (cx - r * 0.55, cy + r * 0.48, r * 0.55, r * 0.55, cx + r * 0.55, cy + r * 0.48))
    return s


def heat_arrow(cx, y0, y1, label='HEAT'):
    s = arrow(cx, y0, cx, y1, w=2.2, color='var(--acc)', marker='arwacc')
    s += txt(cx, y1 + 20, label, 11.5, 'var(--acc)', 700)
    return s


def granules(cx, cy, n=7, spread=16):
    s = ''
    for i in range(n):
        a = i * 2.399
        r = spread * math.sqrt((i + 0.5) / n)
        s += ('<circle cx="%.1f" cy="%.1f" r="2.1" fill="var(--muted)"/>'
              % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return s


def drops(x, y0, y1, n=3):
    s = ''
    for i in range(n):
        y = y0 + (y1 - y0) * i / max(n - 1, 1)
        s += ('<path d="M%.1f,%.1f q4,6 0,10 q-4,-4 0,-10" fill="var(--accmid)"/>' % (x, y))
    return s


# ------------------------------------------------ 1 · distillation apparatus ----
def build_distillation(pal):
    W, H = 1240, 800

    def inner(cnum, layout):
        fx, fy, fr = 250, 400, 68
        s = flask_round(fx, fy, fr)
        s += granules(fx, fy + 24)
        tj_x, tj_y = fx, fy - fr - 84
        s += line(fx, fy - fr, tj_x, tj_y, w=2.2, color='var(--ink)')
        s += line(fx, tj_y - 96, fx, tj_y + 4, w=2.4, color='var(--ink)')
        s += ('<circle cx="%.1f" cy="%.1f" r="6" fill="var(--acc)"/>' % (fx, tj_y + 6))
        ax0, ay0 = tj_x + 4, tj_y + 4
        ax1, ay1 = ax0 + 260, ay0 + 102
        dx, dy = ax1 - ax0, ay1 - ay0
        d = math.hypot(dx, dy)
        px, py = -dy / d, dx / d
        jw = 13
        pts = [(ax0 + px * jw, ay0 + py * jw), (ax1 + px * jw, ay1 + py * jw),
               (ax1 - px * jw, ay1 - py * jw), (ax0 - px * jw, ay0 - py * jw)]
        s += ('<path d="M%s Z" fill="var(--card)" stroke="var(--ink)" stroke-width="2"/>'
              % ' L'.join('%.1f,%.1f' % p for p in pts))
        s += line(ax0 + 28, ay0 + 22, ax1 - 40, ay1 - 15, w=1.8, color='var(--faint)')
        wo_x, wo_y = ax0 + 78, ay0 + py * jw + 2
        s += line(wo_x, wo_y, wo_x - 14, wo_y - 24, w=2, color='var(--cool)')
        s += txt(wo_x - 18, wo_y - 28, 'water out', 11, 'var(--cool)', 600, 'end')
        wi_x, wi_y = ax1 - 32, ay1 - py * jw - 2
        s += line(wi_x, wi_y, wi_x + 20, wi_y + 20, w=2, color='var(--cool)')
        s += txt(wi_x + 2, wi_y + 38, 'water in', 11, 'var(--cool)', 600)
        s += line(ax1, ay1, ax1 + 3, ay1 + 28, w=2.2, color='var(--ink)')
        s += drops(ax1 + 3, ay1 + 34, ay1 + 64, 3)
        s += ('<rect x="%.1f" y="%.1f" width="58" height="40" rx="6" fill="var(--card2)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (ax1 - 25, ay1 + 66))
        s += heat_arrow(fx, fy + fr + 52, fy + fr + 10)
        # labels
        s += lead(fx - 4, tj_y - 80, fx - 52, tj_y - 96)
        s += lbl(fx - 58, tj_y - 92, 'thermometer', 'end')
        s += lbl(ax0 + 118, ay0 + 84, 'Liebig condenser', 'middle')
        s += lead(ax0 + 118, ay0 + 52, ax0 + 118, ay0 + 70)
        s += lbl(ax1 + 34, ay1 + 90, 'distillate', 'start')
        s += lead(fx + fr - 8, fy + 30, fx + fr + 30, fy + 12)
        s += lbl(fx + fr + 36, fy + 16, 'round bottomed flask', 'start', 11.5)
        s += lead(fx - 18, fy + 28, fx - fr - 28, fy + 46)
        s += lbl(fx - fr - 34, fy + 52, 'anti-bumping granules', 'end', 11.5)
        s += lead(fx + 8, tj_y + 26, fx + 54, tj_y + 54)
        s += lbl(fx + 58, tj_y + 58, 'bulb at the T junction', 'start', 11, 'var(--acc)')

        art = svg(620, 500, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('Thermometer', svg(330, 84,
                        line(56, 16, 56, 66, w=2.2, color='var(--ink)') +
                        '<circle cx="56" cy="70" r="5.5" fill="var(--acc)"/>' +
                        line(56, 42, 132, 42, w=1.8, color='var(--accmid)') +
                        line(132, 22, 132, 62, w=2.2, color='var(--ink)') +
                        line(56, 42, 210, 42, w=1.8, color='var(--faint)') +
                        line(210, 22, 210, 62, w=2.2, color='var(--ink)') +
                        txt(148, 14, 'T junction', 10.5, 'var(--acc)', 600, 'start')),
                    'T junction',
                    'The <b>bulb sits at the T-junction</b> connecting to the condenser '
                    '— it measures the <b>correct boiling point</b>.')
               + card('Condenser water', svg(330, 96,
                        line(64, 14, 64, 82, w=2.2, color='var(--ink)') +
                        line(88, 14, 88, 82, w=2.2, color='var(--ink)') +
                        arrow(132, 84, 132, 28, w=2, color='var(--cool)', marker='arw') +
                        txt(144, 56, 'in — bottom', 10.5, 'var(--cool)', 600, 'start') +
                        txt(144, 76, 'against gravity', 10, 'var(--muted)', 500, 'start') +
                        arrow(28, 26, 28, 70, w=2, color='var(--cool)', marker='arw') +
                        txt(20, 20, 'out — top', 10, 'var(--cool)', 600, 'end')),
                    'bottom in',
                    '<b>Against gravity</b> — more efficient cooling and it <b>prevents '
                    'back flow of water</b>.')
               + card('Distillate', svg(330, 84,
                        arrow(40, 14, 40, 60, w=2, color='var(--acc)', marker='arwacc') +
                        '<rect x="78" y="30" width="62" height="38" rx="6" fill="var(--card2)" '
                        'stroke="var(--ink)" stroke-width="2"/>' +
                        txt(86, 20, 'collect the fraction', 10.5, 'var(--acc)', 600, 'start')),
                    'b.p. range',
                    'Collect the <b>distillate of the approximate boiling point range</b> '
                    'of the desired product.')
               + '</div></div>'
               + '<div class="note"><b>Draw and label it accurately</b> — thermometer bulb at '
               'the T junction, water in at the bottom of the condenser, anti-bumping '
               'granules in the flask, distillate collected in a flask.</div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · TECHNIQUES',
                 'Distillation — separate the product by boiling point', body,
                 tag='10.19',
                 fkey='APPARATUS',
                 footer='10.19(iii) distillation: separating the components of a liquid '
                        'mixture by selective boiling and condensation')


# ----------------------------------------------------- 2 · reflux apparatus ----
def build_reflux(pal):
    W, H = 1240, 800

    def inner(cnum, layout):
        fx, fy, r = 250, 470, 66
        s = flask_pear(fx, fy, r)
        s += granules(fx, fy + 28)
        top, bot = fy - r - 218, fy - r - 8
        jw = 24
        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="9" fill="var(--card)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (fx - jw, top - 30, jw * 2, bot - top + 62))
        s += line(fx, top - 22, fx, bot + 24, w=2, color='var(--faint)')
        s += line(fx - jw, top + 4, fx - jw - 24, top + 4, w=2, color='var(--cool)')
        s += line(fx + jw, bot - 8, fx + jw + 24, bot - 8, w=2, color='var(--cool)')
        for yy in (top + 40, top + 96, top + 152):
            s += arrow(fx + 9, yy, fx + 9, yy + 24, w=1.6, color='var(--accmid)', marker='arwacc')
        s += heat_arrow(fx, fy + r + 54, fy + r + 12)
        # labels
        s += lbl(fx, top - 44, 'open top', 'middle', 12)
        s += lead(fx, top - 38, fx, top - 26)
        s += lead(fx - jw - 26, top + 10, fx - jw - 44, top + 18)
        s += lbl(fx - jw - 50, top + 24, 'water out', 'end', 11.5, 'var(--cool)')
        s += lead(fx + jw + 26, bot - 2, fx + jw + 44, bot + 6)
        s += lbl(fx + jw + 50, bot + 10, 'water in', 'start', 11.5, 'var(--cool)')
        s += lead(fx + jw + 10, top + 66, fx + 74, top + 84)
        s += lbl(fx + 78, top + 88, 'Liebig condenser', 'start', 11.5)
        s += lead(fx - 30, fy - 26, fx - 74, fy - 40)
        s += lbl(fx - 78, fy - 44, 'pear-shaped flask', 'end', 11.5)
        s += lead(fx + 20, fy + 30, fx + 74, fy + 46)
        s += lbl(fx + 78, fy + 50, 'anti-bumping granules', 'start', 11.5)

        art = svg(560, 540, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('The job of the condenser', svg(330, 92,
                        arrow(48, 14, 48, 74, w=2, color='var(--cool)', marker='arw') +
                        arrow(96, 74, 96, 14, w=2, color='var(--acc)', marker='arwacc') +
                        txt(122, 30, 'vapour condensed back', 10.5, 'var(--acc)', 600, 'start') +
                        txt(122, 50, 'to liquid — nothing escapes', 10.5, 'var(--muted)', 500, 'start') +
                        txt(122, 76, 'heated for long periods', 10.5, 'var(--muted)', 500, 'start')),
                    'vapours return',
                    'Used when <b>heating organic reaction mixtures for long periods</b> — '
                    'the condenser <b>prevents organic vapours escaping</b> by '
                    '<b>condensing them back to liquids</b>.')
               + card('Never seal it', svg(330, 84,
                        line(56, 8, 56, 56, w=2.2, color='var(--ink)') +
                        '<rect x="42" y="56" width="28" height="11" rx="4" fill="var(--acc)"/>' +
                        txt(104, 50, 'sealed — pressure builds', 10.5, 'var(--acc)', 600, 'start') +
                        txt(104, 70, 'apparatus could explode', 10.5, 'var(--muted)', 500, 'start')),
                    'open top',
                    '<b>Never seal the end of the condenser</b> — the <b>build-up of gas '
                    'pressure could cause the apparatus to explode</b>.')
               + card('Two more rules', svg(330, 92,
                        '<circle cx="44" cy="52" r="5" fill="var(--muted)"/>' +
                        '<circle cx="58" cy="44" r="5" fill="var(--muted)"/>' +
                        '<circle cx="50" cy="60" r="5" fill="var(--muted)"/>' +
                        txt(84, 34, 'anti-bumping granules', 10.5, 'var(--ink)', 600, 'start') +
                        txt(84, 54, 'small bubbles, not large', 10, 'var(--muted)', 500, 'start') +
                        txt(84, 80, 'electric heaters — flammable', 10, 'var(--acc)', 600, 'start')),
                    'granules + heat',
                    'Granules <b>prevent vigorous, uneven boiling</b>. Organic chemicals '
                    'are <b>highly flammable</b> — they could <b>set on fire with a naked '
                    'flame</b>, so <b>electric heaters</b> are used.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · TECHNIQUES',
                 'Heat under reflux — keep the vapour in the flask', body,
                 tag='10.19',
                 fkey='APPARATUS',
                 footer='10.19(i) heating under reflux · anti-bumping granules go in the '
                        'flask in both distillation and reflux')


# -------------------------------------------- 3 · fractional distillation ----
def build_fractional(pal):
    W, H = 800, 760

    def inner(cnum, layout):
        fx, fy, r = 300, 470, 56
        s = flask_round(fx, fy, r)
        s += heat_arrow(fx, fy + r + 48, fy + r + 8)
        col_h = 190
        col_top = fy - r - col_h
        s += ('<rect x="%.1f" y="%.1f" width="24" height="%.1f" rx="8" fill="var(--card2)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (fx - 12, col_top, col_h))
        s += granules(fx, fy - r - 36, n=12, spread=8)
        s += granules(fx, fy - r - 86, n=11, spread=7)
        s += granules(fx, fy - r - 136, n=9, spread=6)
        s += lbl(fx - 24, col_top + 64, 'fractionating column', 'end', 11.5)
        s += line(fx - 22, col_top + 60, fx - 14, col_top + 60, w=1.1, color='var(--faint)')
        s += line(fx, col_top - 68, fx, col_top - 2, w=2.2, color='var(--ink)')
        s += ('<circle cx="%.1f" cy="%.1f" r="5.5" fill="var(--acc)"/>' % (fx, col_top - 2))
        ax0, ay0 = fx + 12, col_top + 14
        ax1, ay1 = ax0 + 250, ay0 + 84
        dx, dy = ax1 - ax0, ay1 - ay0
        d = math.hypot(dx, dy)
        px, py = -dy / d, dx / d
        jw = 12
        pts = [(ax0 + px * jw, ay0 + py * jw), (ax1 + px * jw, ay1 + py * jw),
               (ax1 - px * jw, ay1 - py * jw), (ax0 - px * jw, ay0 - py * jw)]
        s += ('<path d="M%s Z" fill="var(--card)" stroke="var(--ink)" stroke-width="2"/>'
              % ' L'.join('%.1f,%.1f' % p for p in pts))
        wo_x, wo_y = ax0 + 64, ay0 + py * jw + 2
        s += line(wo_x, wo_y, wo_x - 12, wo_y - 22, w=2, color='var(--cool)')
        s += txt(wo_x - 16, wo_y - 26, 'water out', 11, 'var(--cool)', 600, 'end')
        wi_x, wi_y = ax1 - 30, ay1 - py * jw - 2
        s += line(wi_x, wi_y, wi_x + 18, wi_y + 18, w=2, color='var(--cool)')
        s += txt(wi_x + 2, wi_y + 34, 'water in', 11, 'var(--cool)', 600)
        s += line(ax1, ay1, ax1 + 2, ay1 + 26, w=2.2, color='var(--ink)')
        s += drops(ax1 + 2, ay1 + 32, ay1 + 58, 2)
        s += ('<circle cx="%.1f" cy="%.1f" r="30" fill="var(--card2)" stroke="var(--ink)" '
              'stroke-width="2"/>' % (ax1 + 2, ay1 + 92))
        s += lbl(ax1 + 40, ay1 + 96, 'receiver', 'start', 11.5)

        art = svg(640, 540, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('What it does', svg(330, 96,
                        txt(18, 26, 'mixed liquids', 11, 'var(--ink)', 600, 'start') +
                        arrow(130, 22, 196, 22, w=2, color='var(--acc)', marker='arwacc') +
                        txt(208, 16, 'fraction 1', 10.5, 'var(--acc)', 600, 'start') +
                        txt(208, 38, 'fraction 2', 10.5, 'var(--cool)', 600, 'start') +
                        txt(208, 60, 'fraction 3', 10.5, 'var(--muted)', 600, 'start') +
                        txt(18, 66, 'boiling points differ', 10, 'var(--muted)', 500, 'start')),
                    'fractions',
                    'The <b>separation of a liquid mixture into fractions differing in '
                    'boiling point</b> by means of distillation, typically using a '
                    '<b>fractionating column</b>.')
               + card('Why the column helps', svg(330, 100,
                        '<rect x="30" y="8" width="18" height="84" rx="7" fill="var(--card2)" '
                        'stroke="var(--ink)" stroke-width="2"/>' +
                        granules(39, 34, 7, 6) + granules(39, 66, 7, 6) +
                        arrow(84, 26, 84, 70, w=2, color='var(--accmid)', marker='arwacc') +
                        txt(106, 38, 'repeated condensing', 10.5, 'var(--ink)', 600, 'start') +
                        txt(106, 58, 'and re-boiling up the column', 10, 'var(--muted)', 500, 'start')),
                    'column',
                    'Vapour condenses and re-evaporates up the column — the fraction with '
                    'the <b>lowest boiling point</b> leaves the top first.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · TECHNIQUES',
                 'Fractional distillation — one column, many fractions', body,
                 tag='10.19',
                 fkey='APPARATUS',
                 footer='A common purification technique, alongside simple distillation, '
                        'reflux, solvent extraction, drying and boiling point determination')


# -------------------------------------------- 4 · separating funnel ----
def build_separating(pal):
    W, H = 1240, 800

    def inner(cnum, layout):
        cx, top = 250, 96
        fw, fh = 140, 280
        s = ''
        s += line(150, 60, 150, 540, w=4, color='var(--muted)')
        s += line(90, 540, 250, 540, w=5, color='var(--muted)')
        s += line(150, 196, cx - fw / 2 - 6, 200, w=5, color='var(--muted)')
        tip_y = top + fh
        s += ('<path d="M%.1f,%.1f C %.1f,%.1f %.1f,%.1f %.1f,%.1f C %.1f,%.1f %.1f,%.1f %.1f,%.1f Z" '
              'fill="var(--card2)" stroke="var(--ink)" stroke-width="2.2"/>'
              % (cx - fw / 2, top, cx - fw / 2, top + fh * 0.55, cx - fw * 0.28, tip_y - 42, cx, tip_y,
                 cx + fw * 0.28, tip_y - 42, cx + fw / 2, top + fh * 0.55, cx + fw / 2, top))
        s += ('<rect x="%.1f" y="%.1f" width="40" height="14" rx="4" fill="var(--card)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (cx - 20, top - 14))
        lay_top = top + 46
        split_y = top + 138
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--accsoft)"/>'
              % (cx - fw / 2 + 5, lay_top, cx + fw / 2 - 5, lay_top,
                 cx + fw / 2 - 22, split_y))
        s += line(cx - fw / 2 + 22, split_y, cx + fw / 2 - 22, split_y, w=2, color='var(--accmid)')
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--coolsoft)"/>'
              % (cx - fw / 2 + 22, split_y, cx + fw / 2 - 22, split_y, cx, tip_y - 4))
        s += lead(cx + fw / 2 - 28, lay_top + 34, cx + fw / 2 + 26, lay_top + 26)
        s += lbl(cx + fw / 2 + 32, lay_top + 30, 'oil (top layer)', 'start', 11.5)
        s += lead(cx + fw / 2 - 34, split_y + 30, cx + fw / 2 + 26, split_y + 24)
        s += lbl(cx + fw / 2 + 32, split_y + 28, 'water (bottom layer)', 'start', 11.5)
        sc_y = tip_y + 8
        s += ('<rect x="%.1f" y="%.1f" width="42" height="18" rx="5" fill="var(--card)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (cx - 21, sc_y))
        s += ('<circle cx="%.1f" cy="%.1f" r="5.5" fill="var(--acc)"/>' % (cx, sc_y + 9))
        s += lead(cx + 24, sc_y + 9, cx + 64, sc_y + 2)
        s += lbl(cx + 70, sc_y + 6, 'stop-cock', 'start', 11.5)
        s += line(cx, sc_y + 18, cx, sc_y + 46, w=2.2, color='var(--ink)')
        s += drops(cx, sc_y + 52, sc_y + 82, 3)
        cf_top = sc_y + 86
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--card2)" '
              'stroke="var(--ink)" stroke-width="2.2"/>'
              % (cx - 48, cf_top, cx + 48, cf_top, cx + 24, cf_top + 100, cx - 24, cf_top + 100))
        s += line(cx - 24, cf_top + 84, cx + 24, cf_top + 84, w=1.6, color='var(--accmid)')
        s += lbl(cx + 58, cf_top + 54, 'conical flask', 'start', 11.5)

        art = svg(560, 560, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('What it is', svg(330, 88,
                        '<path d="M52,10 C 26,42 26,62 52,74 C 78,62 78,42 52,10 Z" '
                        'fill="var(--card2)" stroke="var(--ink)" stroke-width="2"/>' +
                        line(52, 74, 52, 82, w=2.2, color='var(--ink)') +
                        '<circle cx="52" cy="74" r="4.5" fill="var(--acc)"/>' +
                        txt(104, 36, 'stop-cock in the stem', 10.5, 'var(--ink)', 600, 'start') +
                        txt(104, 58, 'allow or stop the flow', 10, 'var(--muted)', 500, 'start')),
                    'stop-cock',
                    'A separating funnel has a <b>stop-cock in its stem</b> to <b>allow or '
                    'stop the flow</b> of liquid from it.')
               + card('Two layers', svg(330, 96,
                        '<rect x="36" y="10" width="42" height="30" fill="var(--accsoft)" '
                        'stroke="var(--accmid)"/>' +
                        '<rect x="36" y="40" width="42" height="36" fill="var(--coolsoft)" '
                        'stroke="var(--cool)"/>' +
                        txt(100, 28, 'less dense — top', 10.5, 'var(--acc)', 600, 'start') +
                        txt(100, 60, 'denser — bottom', 10.5, 'var(--cool)', 600, 'start') +
                        txt(100, 84, 'immiscible liquids', 10, 'var(--muted)', 500, 'start')),
                    'immiscible',
                    'Two <b>immiscible liquids</b> form <b>two layers</b> — the '
                    '<b>denser solvent will be the bottom layer</b>. Most <b>halogenated '
                    'solvents are denser than water</b>.')
               + card('The method', svg(330, 118,
                        txt(16, 20, '1. add the solvent — two layers form', 10.5, 'var(--ink)', 500, 'start') +
                        txt(16, 44, '2. stopper, shake, open tap to vent', 10.5, 'var(--ink)', 500, 'start') +
                        txt(16, 68, '3. let the layers settle', 10.5, 'var(--ink)', 500, 'start') +
                        txt(16, 92, '4. tap open — collect the organic layer', 10.5, 'var(--acc)', 600, 'start') +
                        txt(26, 112, 'discard the unwanted aqueous layer', 10, 'var(--muted)', 500, 'start')),
                    'four steps',
                    'Extraction with a solvent using a separating funnel — release the '
                    'pressure by opening the tap from time to time.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · TECHNIQUES',
                 'Separating funnel — split the layers, keep the organic one', body,
                 tag='10.19',
                 fkey='APPARATUS',
                 footer='10.19(ii) extraction with a solvent using a separating funnel')


# ------------------------------------------- 5 · boiling point determination ----
def build_bp(pal):
    W, H = 1240, 760

    def inner(cnum, layout):
        s = ''
        bx, by, bw, bh = 240, 270, 190, 180
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--card2)" '
              'stroke="var(--ink)" stroke-width="2.2"/>'
              % (bx, by, bx + bw, by, bx + bw - 16, by + bh, bx + 16, by + bh))
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--accsoft)"/>'
              % (bx + 6, by + 38, bx + bw - 6, by + 38, bx + bw - 20, by + bh - 8, bx + 20, by + bh - 8))
        s += line(bx + 20, by + bh - 8, bx + bw - 20, by + bh - 8, w=2, color='var(--accmid)')
        s += lbl(bx + bw + 14, by + 86, 'heating oil bath', 'start', 11.5)
        s += lead(bx + bw - 12, by + 82, bx + bw + 8, by + 84)
        s += line(bx - 60, 84, bx - 60, 470, w=4, color='var(--muted)')
        s += line(bx - 116, 470, bx - 8, 470, w=5, color='var(--muted)')
        s += line(bx - 60, 220, bx - 28, 220, w=4, color='var(--muted)')
        tx, ty, tw, th = bx + 66, by + 26, 36, 134
        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="var(--card)" '
              'stroke="var(--ink)" stroke-width="2.2"/>' % (tx, ty, tw, th))
        s += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="var(--coolsoft)"/>'
              % (tx + 4, ty + 66, tx + tw - 4, ty + 66, tx + tw - 4, ty + th - 6))
        s += line(tx + 4, ty + 66, tx + tw - 4, ty + 66, w=1.8, color='var(--cool)')
        s += lbl(tx + tw + 18, ty + 112, 'sample tube', 'start', 11.5)
        s += lead(tx + tw, ty + 108, tx + tw + 12, ty + 110)
        s += line(tx + 12, ty + 12, tx + 12, ty + 68, w=2, color='var(--accmid)')
        s += line(tx + 19, ty + 12, tx + 19, ty + 68, w=2, color='var(--accmid)')
        s += lbl(tx + tw + 18, ty + 44, 'capillary tube', 'start', 11)
        s += lead(tx + 20, ty + 28, tx + tw + 12, ty + 40)
        thx, th_top = tx + tw / 2, 100
        s += ('<rect x="%.1f" y="%.1f" width="28" height="32" fill="var(--card)" '
              'stroke="var(--ink)" stroke-width="2"/>' % (thx - 14, ty - 34))
        s += line(thx, th_top, thx, ty + 58, w=2.4, color='var(--ink)')
        s += ('<circle cx="%.1f" cy="%.1f" r="5.5" fill="var(--acc)"/>' % (thx, ty + 58))
        s += txt(thx - 38, th_top + 6, 'THERMOMETER', 11, 'var(--ink)', 600, 'end')
        s += lead(thx - 6, th_top + 2, thx - 32, th_top + 4)
        s += txt(thx + 38, ty - 18, 'GLASS TUBING', 11, 'var(--ink)', 600, 'start')
        s += lead(thx + 14, ty - 20, thx + 32, ty - 20)
        s += arrow(tx + tw + 58, ty + 36, tx + tw / 2 + 8, ty + 52, w=1.4,
                   color='var(--acc)', marker='arwacc')
        s += txt(tx + tw + 62, ty + 30, 'bulb above the liquid —', 10.5, 'var(--acc)', 600, 'start')
        s += txt(tx + tw + 62, ty + 48, 'measures the saturated vapour', 10,
                 'var(--muted)', 500, 'start')

        art = svg(600, 480, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('What it is for', svg(330, 84,
                        txt(16, 26, 'measure the boiling point', 11, 'var(--ink)', 600, 'start') +
                        txt(16, 52, 'compare with the data booklet', 10.5, 'var(--acc)', 600, 'start') +
                        txt(16, 78, 'purity is determined', 10, 'var(--muted)', 500, 'start')),
                    'purity',
                    '<b>Purity of a liquid can be determined by measuring a boiling '
                    'point</b> — in a distillation set-up or by simply boiling a tube of '
                    'the sample in a <b>heating oil bath</b>, then <b>compared with the '
                    'data booklet values</b>.')
               + card('Two things to note', svg(330, 100,
                        txt(16, 22, 'thermometer above the liquid surface', 10.5,
                            'var(--acc)', 600, 'start') +
                        txt(30, 42, 'measuring the saturated vapour', 10,
                            'var(--muted)', 500, 'start') +
                        txt(16, 76, 'note the pressure', 10.5, 'var(--ink)', 600, 'start') +
                        txt(30, 96, 'changing pressure changes the b.p.', 10,
                            'var(--muted)', 500, 'start')),
                    'vapour + pressure',
                    'The thermometer should be <b>above the level of the surface of the '
                    'boiling liquid</b>, and <b>pressure should be noted</b>.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · TECHNIQUES',
                 'Boiling point determination — the purity check', body,
                 tag='10.19',
                 fkey='APPARATUS',
                 footer='10.19(v) boiling temperature determination · compared with the '
                        'data booklet values to determine purity')


# ------------------------------------------------- 6 · alcohol bond angles ----
def build_bond_angles(pal):
    W, H = 1240, 640

    def inner(cnum, layout):
        c1x, c1y = 240, 260
        c2x, c2y = 350, 260
        ox, oy = 448, 236
        s = ''
        for hx, hy in ((c1x - 62, c1y - 44), (c1x - 62, c1y + 44), (c1x - 80, c1y)):
            s += bond(c1x - 8, c1y, hx, hy)
            s += txt(hx - 8, hy + 5, 'H', 12.5, 'var(--ink)', 600)
        s += bond(c1x + 8, c1y, c2x - 8, c2y)
        s += txt(c1x - 4, c1y + 5, 'C', 12, 'var(--muted)', 600)
        s += bond(c2x - 2, c2y - 8, c2x - 34, c2y - 72)
        s += txt(c2x - 38, c2y - 78, 'H', 12.5, 'var(--ink)', 600)
        s += bond(c2x + 2, c2y - 8, c2x + 34, c2y - 72)
        s += txt(c2x + 38, c2y - 78, 'H', 12.5, 'var(--ink)', 600)
        s += bond(c2x - 2, c2y + 8, c2x - 34, c2y + 72)
        s += txt(c2x - 38, c2y + 82, 'H', 12.5, 'var(--ink)', 600)
        s += bond(c2x + 2, c2y + 8, c2x + 34, c2y + 72)
        s += txt(c2x + 38, c2y + 82, 'H', 12.5, 'var(--ink)', 600)
        s += txt(c2x + 4, c2y + 5, 'C', 12, 'var(--muted)', 700)
        s += bond(c2x + 8, c2y - 4, ox - 10, oy + 4)
        s += txt(ox + 6, oy + 6, 'O', 14, 'var(--ink)', 700)
        s += bond(ox + 12, oy - 4, ox + 54, oy - 32)
        s += txt(ox + 66, oy - 30, 'H', 12.5, 'var(--ink)', 600)
        s += lonepair(ox + 2, oy - 14, 100)
        s += lonepair(ox - 12, oy + 12, 190)
        s += txt(ox - 30, oy - 38, 'lone pairs', 10.5, 'var(--acc)', 600, 'end')
        s += lead(ox - 26, oy - 32, ox - 6, oy - 16)
        s += ('<path d="M%.1f,%.1f A28,28 0 0 0 %.1f,%.1f" fill="none" stroke="var(--acc)" '
              'stroke-width="1.8"/>' % (c1x - 28, c1y, c1x - 9, c1y - 26))
        s += txt(c1x - 34, c1y - 12, '109.5°', 12, 'var(--acc)', 700, 'end')
        s += ('<path d="M%.1f,%.1f A24,24 0 0 1 %.1f,%.1f" fill="none" stroke="var(--acc)" '
              'stroke-width="1.8"/>' % (ox + 21, oy + 14, ox + 20, oy - 22))
        s += txt(ox + 28, oy + 34, '104.5°', 12, 'var(--acc)', 700, 'start')
        s += txt(300, 130, 'H–O–C is bent — 104.5°', 11.5, 'var(--muted)', 600)
        s += txt(300, 372, 'all H–C–H and C–C–O bonds are 109.5° — tetrahedral',
                 11.5, 'var(--muted)', 600)

        art = svg(560, 420, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('Around each carbon', svg(300, 104,
                        '<circle cx="60" cy="52" r="11" fill="var(--card2)" '
                        'stroke="var(--ink)" stroke-width="2"/>' +
                        line(60, 41, 39, 22, w=2, color='var(--ink)') +
                        line(60, 41, 83, 22, w=2, color='var(--ink)') +
                        line(60, 63, 39, 84, w=2, color='var(--ink)') +
                        line(60, 63, 83, 84, w=2, color='var(--ink)') +
                        txt(60, 104, '4 bond pairs', 10, 'var(--muted)', 500) +
                        txt(190, 56, '109.5°', 14, 'var(--acc)', 700) +
                        txt(190, 76, 'tetrahedral', 10, 'var(--muted)', 500)),
                    '109.5°',
                    'All the <b>H–C–H bonds and C–C–O are 109.5°</b> (tetrahedral shape) '
                    '— <b>4 bond pairs</b> of electrons repelling to a position of '
                    '<b>minimum repulsion</b>.')
               + card('Around the oxygen', svg(300, 104,
                        '<circle cx="60" cy="52" r="11" fill="var(--accsoft)" '
                        'stroke="var(--accmid)" stroke-width="2"/>' +
                        line(60, 41, 39, 24, w=2, color='var(--ink)') +
                        line(60, 63, 39, 82, w=2, color='var(--ink)') +
                        lonepair(74, 38, 30) + lonepair(74, 66, 150) +
                        txt(60, 104, '2 bond + 2 lone pairs', 10, 'var(--muted)', 500) +
                        txt(190, 56, '104.5°', 14, 'var(--acc)', 700) +
                        txt(190, 76, 'bent line shape', 10, 'var(--muted)', 500)),
                    '104.5°',
                    'The <b>H–O–C bond is 104.5° (bent line shape)</b> — the oxygen has '
                    '<b>2 bond pairs and 2 lone pairs</b>. <b>Lone pairs repel more than '
                    'bond pairs</b>, so the bond angle is reduced.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · ALCOHOLS',
                 'Bond angles in alcohols — tetrahedral carbon, bent oxygen', body,
                 tag='10.15',
                 fkey='SHAPES',
                 footer='H–O–C = 104.5° because there are 2 bond pairs and 2 lone pairs '
                        'repelling to a position of minimum repulsion')


# ------------------------------------------- 7 · C4H9Br reaction scheme ----
def build_scheme(pal):
    W, H = 1240, 700

    def inner(cnum, layout):
        bx, by = 420, 330
        ox, oy = 760, 330
        ax, ay = 160, 110
        nx, ny = 160, 550
        s = ''

        def node(x, y, formula, sub):
            out = ('<rect x="%.1f" y="%.1f" width="170" height="56" rx="12" fill="var(--card2)" '
                   'stroke="var(--ink)" stroke-width="2"/>' % (x - 85, y - 28))
            out += txt(x, y - 3, formula, 20, 'var(--ink)', 700)
            out += txt(x, y + 20, sub, 10.5, 'var(--muted)', 500)
            return out

        s += node(bx, by, 'C₄H₉Br', 'bromobutane')
        s += node(ox, oy, 'C₄H₉OH', 'butan-1-ol')
        s += node(ax, ay, 'C₄H₈', 'butene')
        s += node(nx, ny, 'C₄H₉NH₂', 'butylamine')

        mx, my = (bx + ax) / 2, (by + ay) / 2
        s += arrow(bx - 62, by - 34, ax + 72, ay + 40, w=2.4, color='var(--acc)', marker='arwacc')
        s += txt(mx - 44, my + 2, 'A', 16, 'var(--acc)', 700)
        s += ('<path d="M%.1f,%.1f C %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" '
              'stroke="var(--acc)" stroke-width="2.4" marker-end="url(#arwacc)"/>'
              % (bx + 36, by - 32, (bx + ox) / 2, by - 104, (bx + ox) / 2, by - 104,
                 ox - 40, oy - 32))
        s += txt((bx + ox) / 2, by - 112, 'B', 16, 'var(--acc)', 700)
        s += ('<path d="M%.1f,%.1f C %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" '
              'stroke="var(--acc)" stroke-width="2.4" marker-end="url(#arwacc)"/>'
              % (ox - 36, oy + 34, (bx + ox) / 2, oy + 104, (bx + ox) / 2, oy + 104,
                 bx + 40, by + 34))
        s += txt((bx + ox) / 2, oy + 132, 'C', 16, 'var(--acc)', 700)
        s += arrow(bx - 62, by + 34, nx + 72, ny - 40, w=2.4, color='var(--acc)', marker='arwacc')
        s += txt(mx - 44, my + 46, 'D', 16, 'var(--acc)', 700)

        art = svg(880, 600, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('What the letters ask for', svg(330, 118,
                        txt(16, 22, 'A  →  butene', 11.5, 'var(--acc)', 700, 'start') +
                        txt(30, 42, 'elimination', 10, 'var(--muted)', 500, 'start') +
                        txt(16, 66, 'B  →  butanol', 11.5, 'var(--acc)', 700, 'start') +
                        txt(30, 86, 'nucleophilic substitution', 10, 'var(--muted)', 500, 'start') +
                        txt(16, 110, 'C  →  bromobutane, back from the alcohol', 11,
                            'var(--acc)', 700, 'start')),
                    'four arrows',
                    'Halogenoalkanes are <b>important intermediates</b> — identify the '
                    '<b>reagents and any specific conditions</b> for each arrow.')
               + card('Name the reaction type', svg(330, 96,
                        txt(16, 28, 'A — elimination', 11.5, 'var(--ink)', 600, 'start') +
                        txt(16, 56, 'D — nucleophilic substitution', 11.5, 'var(--ink)', 600, 'start') +
                        txt(16, 84, 'classify from what happens', 10, 'var(--muted)', 500, 'start')),
                    'part (b)(i)',
                    'A removes HBr to leave the C=C; D swaps Br for NH₂ using a lone-pair '
                    'donor. A suitable temperature is maintained in each reaction.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · HALOGENOALKANES',
                 'One halogenoalkane, four destinations', body,
                 tag='10.8 – 10.9',
                 fkey='SCHEME',
                 footer='Halogenoalkanes are important intermediates in organic chemistry · '
                        'alcohol · alkene · amine')


# ------------------------------------------------ 8 · ethane fragmentation ----
def build_ms_ethane(pal):
    W, H = 1240, 620

    def inner(cnum, layout):
        ex, ey = 130, 280
        s = ''
        s += txt(ex, ey + 5, 'C', 14, 'var(--ink)', 700)
        s += txt(ex + 74, ey + 5, 'C', 14, 'var(--ink)', 700)
        s += line(ex + 12, ey, ex + 62, ey, w=2.2, color='var(--ink)')
        for dx in (-13, 0, 13):
            s += line(ex + dx, ey - 12, ex + dx, ey - 38, w=1.8, color='var(--ink)')
            s += txt(ex + dx, ey - 46, 'H', 11.5, 'var(--ink)', 600)
            s += line(ex + dx, ey + 12, ex + dx, ey + 38, w=1.8, color='var(--ink)')
            s += txt(ex + dx, ey + 56, 'H', 11.5, 'var(--ink)', 600)
        s += txt(ex + 36, ey + 88, '+ e⁻', 13, 'var(--acc)', 700)

        outs = [
            (330, 110, 'CH₃–CH₃⁺•', 'm/z = 30', 'molecular ion (M⁺•)', 'var(--ink)'),
            (330, 280, 'CH₃–CH₂⁺  +  H•', 'm/z = 29', 'ethyl cation — detected', 'var(--ink)'),
            (330, 450, 'CH₃⁺  +  •CH₃', 'm/z = 15', '(not detected by MS)', 'var(--muted)'),
        ]
        for x, y, top, mz, sub, col in outs:
            s += arrow(212, 280, x - 10, y, w=2, color='var(--accmid)', marker='arwacc')
            s += txt(x + 150, y + 5, top, 14.5, col, 700)
            s += txt(x + 150, y + 30, mz, 13, 'var(--acc)', 700)
            s += txt(x + 150, y + 52, sub, 11, 'var(--muted)', 500)

        art = svg(700, 500, s)
        col = ('<div class="duo">'
               + '<div class="center">' + art + '</div>'
               + '<div class="stack">'
               + card('Ionisation first', svg(330, 84,
                        txt(16, 30, 'M + e⁻ → M⁺• + 2e⁻', 12.5, 'var(--ink)', 600, 'start') +
                        txt(16, 60, 'loss of one electron', 10.5, 'var(--muted)', 500, 'start')),
                    'M⁺•',
                    'The molecules are <b>ionised by bombardment with a beam of high '
                    'energy electrons</b> — the radical cation M⁺• is the molecular ion.')
               + card('Then fragmentation', svg(330, 84,
                        txt(16, 30, 'M⁺• → X⁺ + Y•', 12.5, 'var(--ink)', 600, 'start') +
                        txt(16, 60, 'only X⁺ is detected', 10.5, 'var(--acc)', 600, 'start')),
                    'X⁺ detected',
                    'The impact of the <b>stream of high energy electrons</b> can also '
                    '<b>break the molecule or the radical cation into fragments</b> — one '
                    'fragment carries the positive charge, the other is neutral.')
               + card('Even smaller', svg(330, 84,
                        txt(16, 30, 'X⁺ → A⁺ + B', 12.5, 'var(--ink)', 600, 'start') +
                        txt(16, 60, 'smaller pieces, again', 10.5, 'var(--muted)', 500, 'start')),
                    'successive',
                    'These smaller pieces may <b>in turn undergo fragmentation</b> and '
                    'produce even smaller pieces.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · MASS SPECTRA',
                 'Ethane under the beam — three ways to break', body,
                 tag='10.21',
                 fkey='FRAGMENT',
                 footer='M⁺• at m/z 30 · CH₃CH₂⁺ at 29 · CH₃⁺ at 15 — the neutral partner '
                        'is not detected by the spectrometer')


# --------------------------------------------- 9 · pentane spectrum ----
def build_ms_pentane(pal):
    W, H = 1240, 660
    X0, Y0, AW, AH = 130, 420, 960, 270

    def inner(cnum, layout):
        s = line(X0, Y0, X0 + AW, Y0, w=2, color='var(--ink)')
        s += line(X0, Y0, X0, Y0 - AH, w=2, color='var(--ink)')
        s += txt(X0 + AW / 2, Y0 + 42, 'm / z', 12.5, 'var(--body)', 600, family='GeistMono')
        s += ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
              'style="font-family:GeistMono;font-size:11px;font-weight:600;'
              'fill:var(--body);letter-spacing:1px">relative abundance</text>'
              % (X0 - 40, Y0 - AH / 2, X0 - 40, Y0 - AH / 2))

        def mz(v):
            return X0 + v / 80 * AW

        for v in range(0, 90, 10):
            s += line(mz(v), Y0, mz(v), Y0 + 6, w=1.2, color='var(--faint)')
            s += txt(mz(v), Y0 + 22, str(v), 10, 'var(--muted)', 500, family='GeistMono')

        peaks = [(15, 0.62, 'C'), (29, 0.55, 'B'), (43, 1.0, 'A'), (57, 0.50, 'D'), (72, 0.18, None)]
        for v, h, letter in peaks:
            x, ytop = mz(v), Y0 - h * (AH - 50)
            s += line(x, Y0, x, ytop, w=3, color='var(--ink)')
            if letter:
                s += txt(x, ytop - 14, '%s (%d)' % (letter, v), 11.5, 'var(--acc)', 700)
            else:
                s += txt(x, ytop - 32, '(72)', 11.5, 'var(--acc)', 700)
                s += txt(x, ytop - 14, 'molecular ion', 10.5, 'var(--acc)', 700)
        s += txt(mz(43) - 60, Y0 - 1.0 * (AH - 50) - 14, 'C₅H₁₂', 13, 'var(--ink)', 700, 'end')

        art = svg(1120, 480, s)
        col = ('<div class="stack">'
               + '<div class="center">' + art + '</div>'
               + '<div class="duo2" style="flex:0 0 auto;margin-top:12px">'
               + card('Read it right to left', svg(420, 88,
                        txt(16, 24, 'molecular ion 72 → Mᵣ = 72', 11.5, 'var(--ink)', 600, 'start') +
                        txt(16, 50, '72 − 15 → 57 (C₄H₉⁺) · 57 − 14 → 43 · 29 · 15', 11.5,
                            'var(--acc)', 600, 'start') +
                        txt(16, 76, '14 units apart = CH₂ units', 10, 'var(--muted)', 500, 'start')),
                    'subtract',
                    'Every fragment reads as a subtraction: <b>fragment m/z = M − the '
                    'piece that was lost</b>.')
               + card('The five peaks', svg(420, 88,
                        txt(16, 24, '15 CH₃⁺ · 29 CH₃CH₂⁺ · 43 CH₃CH₂CH₂⁺', 11.5,
                            'var(--ink)', 600, 'start') +
                        txt(16, 50, '57 CH₃CH₂CH₂CH₂⁺ · 72 C₅H₁₂⁺• (M⁺•)', 11.5,
                            'var(--ink)', 600, 'start') +
                        txt(16, 76, 'C₅H₁₂ + e⁻ → C₅H₁₂⁺• + 2e⁻', 10, 'var(--muted)', 500, 'start')),
                    'peaks C·B·A·D',
                    'The molecular ion is the peak <b>furthest to the right</b>; the '
                    'tallest peak (A, m/z 43) is the <b>base peak</b>.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · MASS SPECTRA',
                 'The pentane spectrum — five peaks, one chain', body,
                 tag='10.21',
                 fkey='EXERCISE',
                 footer='Exercise 1 · the molecular ion and the fragments that give rise '
                        'to the labelled peaks')


# ------------------------------------------- 10 · alcohol solubility ----
def build_solubility(pal):
    W, H = 1240, 640

    def inner(cnum, layout):
        s = ''
        rows = [
            (170, 1, 'methanol', 'very soluble in water'),
            (520, 4, 'butanol', 'slightly soluble in water'),
            (940, 8, 'octanol', 'very insoluble in water'),
        ]
        for cx, n, name, note in rows:
            chain_w = 44 * n
            x0 = cx - chain_w / 2 + 10
            y = 300
            for i in range(n):
                x = x0 + 44 * i
                if i > 0:
                    s += line(x - 44 + 8, y, x - 8, y, w=2, color='var(--ink)')
                s += txt(x, y + 5, 'C', 12.5, 'var(--ink)', 700)
                s += line(x, y - 10, x, y - 32, w=1.6, color='var(--ink)')
                s += txt(x, y - 40, 'H', 10, 'var(--muted)', 500)
                s += line(x, y + 10, x, y + 32, w=1.6, color='var(--ink)')
                s += txt(x, y + 50, 'H', 10, 'var(--muted)', 500)
                if i == n - 1:
                    s += line(x + 8, y, x + 36, y - 22, w=2, color='var(--ink)')
                    s += txt(x + 46, y - 18, 'O', 13, 'var(--acc)', 700)
                    s += line(x + 52, y - 26, x + 78, y - 42, w=2, color='var(--ink)')
                    s += txt(x + 88, y - 40, 'H', 12, 'var(--ink)', 600)
            if n >= 4:
                bx0, bx1 = x0 - 20, x0 + 44 * (n - 1) + 8
                midy = 196
                s += line(bx0, midy + 12, bx0, midy, w=1.4, color='var(--accmid)')
                s += line(bx0, midy, bx1, midy, w=1.4, color='var(--accmid)')
                s += line(bx1, midy, bx1, midy + 12, w=1.4, color='var(--accmid)')
                s += txt((bx0 + bx1) / 2, midy - 8, 'non-polar', 11.5, 'var(--acc)', 600)
            s += txt(cx, 386, name, 13.5, 'var(--ink)', 700)
            s += txt(cx, 410, note, 11.5, 'var(--muted)', 500)
        s += txt(330, 486, 'the –OH end forms hydrogen bonds with water', 11.5,
                 'var(--acc)', 600)
        s += txt(880, 486, 'the longer the non-polar chain, the stronger the London forces',
                 11.5, 'var(--muted)', 500)

        art = svg(1120, 520, s)
        col = ('<div class="stack">'
               + '<div class="center">' + art + '</div>'
               + '<div class="duo2" style="flex:0 0 auto;margin-top:10px">'
               + card('Short chains dissolve', svg(420, 84,
                        txt(16, 26, '–OH · · · H₂O — hydrogen bonds with water', 11.5,
                            'var(--acc)', 600, 'start') +
                        txt(16, 52, 'stronger than the London forces between chains', 10.5,
                            'var(--muted)', 500, 'start') +
                        txt(16, 76, '→ relatively short carbon chains dissolve', 10,
                            'var(--ink)', 500, 'start')),
                    'H-bonds',
                    'Alcohols with <b>relatively short carbon chains dissolve in '
                    'water</b>. More than one –OH group <b>increases</b> solubility — '
                    'more hydrogen bonds can be formed.')
               + card('Long chains do not', svg(420, 84,
                        txt(16, 26, 'the non-polar group becomes bigger', 11.5,
                            'var(--ink)', 600, 'start') +
                        txt(16, 52, '→ stronger London forces between the carbon chains', 10.5,
                            'var(--acc)', 600, 'start') +
                        txt(16, 76, '→ solubility gradually decreases with chain length', 10,
                            'var(--muted)', 500, 'start')),
                    'chain wins',
                    'Solubility in water <b>gradually decreases with increasing carbon '
                    'chain length</b>.')
               + '</div></div>')

        return '<style>%s</style>%s' % (GRID_CSS, col)

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · ALCOHOLS',
                 'Solubility — the –OH pulls, the chain pushes', body,
                 tag='10.16',
                 fkey='PHYSICAL',
                 footer='methanol very soluble · butanol slightly soluble · octanol very '
                        'insoluble in water')


FIGS = [
    ('t10-apparatus-distillation', 1240, 800, build_distillation),
    ('t10-apparatus-reflux', 1240, 800, build_reflux),
    ('t10-apparatus-fractional', 1240, 760, build_fractional),
    ('t10-apparatus-separating', 1240, 800, build_separating),
    ('t10-bp-determination', 1240, 760, build_bp),
    ('t10-alcohol-bond-angles', 1240, 640, build_bond_angles),
    ('t10-halo-scheme', 1240, 700, build_scheme),
    ('t10-ms-ethane', 1240, 620, build_ms_ethane),
    ('t10-ms-pentane', 1240, 660, build_ms_pentane),
    ('t10-alcohol-solubility', 1240, 640, build_solubility),
]


def main():
    from pathlib import Path
    from playwright.sync_api import sync_playwright  # noqa: E402
    from common import OUT

    only = sys.argv[1] if len(sys.argv) > 1 else None
    HTML_DIR = Path('/home/z/my-project/scripts/t10/html')
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--force-color-profile=srgb'])
        ctx = browser.new_context(device_scale_factor=2,
                                  viewport={'width': 1500, 'height': 1200})
        page = ctx.new_page()
        for name, w, h, build in FIGS:
            if only and only not in name:
                continue
            for variant, pal_ in (('light', LIGHT), ('dark', DARK)):
                html = build(pal_)
                hp = HTML_DIR / ('%s-%s.html' % (name, variant))
                hp.write_text(html)
                page.goto(hp.as_uri())
                page.evaluate('() => document.fonts.ready.then(() => true)')
                page.wait_for_timeout(60)
                fname = name + ('-dark' if variant == 'dark' else '') + '.png'
                page.locator('.plate').screenshot(path=str(OUT / fname),
                                                  omit_background=True)
                print('rendered', fname)
        browser.close()


if __name__ == '__main__':
    main()
