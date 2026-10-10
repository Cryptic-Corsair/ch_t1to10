#!/usr/bin/env python3
"""Design system + SVG helpers + shell for the Topic 4 figure set v2.

Concept: every figure is a "specimen plate" — transparent-background PNG that
sits on the site's elevated figure band, typographically locked to the site
(Geist / Geist Mono), brand coral accents, hairline borders, generous space.
"""
import math
from pathlib import Path

ROOT = Path('/home/z/my-project')
OUT = ROOT / 'public/diagrams'
HTML_DIR = ROOT / 'scripts/t4v2/html'
FONT_SANS = ROOT / 'node_modules/geist/dist/fonts/geist-sans'
FONT_MONO = ROOT / 'node_modules/geist/dist/fonts/geist-mono'

LIGHT = {
    'ink': '#1b1d23', 'body': '#3a3e47', 'muted': '#7b8290',
    'hair': 'rgba(27,29,35,.22)', 'faint': 'rgba(27,29,35,.12)',
    'card': 'rgba(27,29,35,.040)', 'card2': 'rgba(27,29,35,.075)',
    'acc': '#dd4f37', 'accsoft': 'rgba(221,79,55,.10)', 'accmid': 'rgba(221,79,55,.55)',
    'oz': '#d0453f', 'diafill': '#ffffff', 'diaedge': '#e2483d', 'pic': '#26282f',
    'cool': '#3d7fa6', 'coolsoft': 'rgba(61,127,166,.22)',
}
DARK = {
    'ink': '#eef0f5', 'body': '#c9cdd6', 'muted': '#98a1b0',
    'hair': 'rgba(238,240,245,.24)', 'faint': 'rgba(238,240,245,.11)',
    'card': 'rgba(238,240,245,.055)', 'card2': 'rgba(238,240,245,.10)',
    'acc': '#ff7052', 'accsoft': 'rgba(255,112,82,.14)', 'accmid': 'rgba(255,112,82,.6)',
    'oz': '#ff7b6e', 'diafill': '#242730', 'diaedge': '#ff5449', 'pic': '#eef0f5',
    'cool': '#7db4d8', 'coolsoft': 'rgba(125,180,216,.20)',
}

# ---------------------------------------------------------------- fonts ----
def fontfaces():
    faces = [
        (FONT_SANS / 'Geist-Regular.woff2', 'Geist', 400),
        (FONT_SANS / 'Geist-Medium.woff2', 'Geist', 500),
        (FONT_SANS / 'Geist-SemiBold.woff2', 'Geist', 600),
        (FONT_SANS / 'Geist-Bold.woff2', 'Geist', 700),
        (FONT_MONO / 'GeistMono-Regular.woff2', 'GeistMono', 400),
        (FONT_MONO / 'GeistMono-Medium.woff2', 'GeistMono', 500),
        (FONT_MONO / 'GeistMono-SemiBold.woff2', 'GeistMono', 600),
    ]
    css = ''
    for path, fam, w in faces:
        if path.exists():
            css += ("@font-face{font-family:'%s';src:url('file://%s') format('woff2');"
                    "font-weight:%d;font-style:normal}\n" % (fam, path, w))
        else:
            print('  ! missing font:', path)
    return css

BASE_CSS = fontfaces() + """
*{margin:0;padding:0;box-sizing:border-box}
body{background:transparent;-webkit-font-smoothing:antialiased}
.plate{background:transparent;color:var(--ink);display:flex;flex-direction:column;
  font-family:'Geist','DejaVu Sans',sans-serif}
.hd{display:flex;align-items:baseline;gap:14px}
.kick{font-family:'GeistMono',monospace;font-weight:600;font-size:11px;
  letter-spacing:.17em;color:var(--acc);text-transform:uppercase;white-space:nowrap}
.hd h1{font-size:19px;font-weight:600;color:var(--ink);letter-spacing:-.01em;white-space:nowrap}
.hd .rule{flex:1;height:1px;background:var(--hair);transform:translateY(-4px)}
.hd .tag{font-family:'GeistMono',monospace;font-size:11px;font-weight:500;color:var(--muted);
  letter-spacing:.04em;white-space:nowrap}
.ft{margin-top:auto;display:flex;align-items:baseline;gap:12px;border-top:1px solid var(--faint);
  padding-top:13px;color:var(--muted);font-size:12.5px;line-height:1.45}
.ft .fkey{font-family:'GeistMono',monospace;font-size:10px;font-weight:600;color:var(--acc);
  letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
sub{font-size:.60em;vertical-align:baseline;position:relative;top:.34em;letter-spacing:0}
sup{font-size:.60em;vertical-align:baseline;position:relative;top:-.42em}
.rd{color:var(--acc);font-size:1.12em;line-height:0;position:relative;top:.10em;margin:0 1px}
.chip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--hair);
  border-radius:8px;padding:5px 10px;font-family:'GeistMono',monospace;font-weight:500;
  font-size:11px;color:var(--body);letter-spacing:.02em;background:var(--card)}
.chip.acc{color:var(--acc);border-color:var(--accmid);background:var(--accsoft)}
"""

# ------------------------------------------------------------ svg helpers ----
def pts_path(pts, close=False):
    d = 'M' + ' L'.join('%.2f,%.2f' % p for p in pts)
    return d + (' Z' if close else '')

def line(x1, y1, x2, y2, w=2.6, color='var(--ink)', dash=None, cap='round'):
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="%.2f" stroke-linecap="%s"%s/>' % (x1, y1, x2, y2, color, w, cap, da))

def polyline(pts, w=2.8, color='var(--ink)'):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (pts_path(pts), color, w))

def arrow_marker(id_, color='var(--muted)'):
    return ('<marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (id_, color))

def arrow(x1, y1, x2, y2, w=1.6, color='var(--muted)', mid=None, marker='arw'):
    d = 'M%.2f,%.2f' % (x1, y1) + (' L%.2f,%.2f' % mid if mid else '') + ' L%.2f,%.2f' % (x2, y2)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
            'marker-end="url(#%s)"/>' % (d, color, w, marker))

def wavy(x0, y0, x1, y1, color='var(--acc)', w=2.2, waves=4.5, amp=5.5, marker='arwacc'):
    dx, dy = x1 - x0, y1 - y0
    dist = math.hypot(dx, dy)
    px, py = -dy / dist, dx / dist
    steps = int(waves * 8)
    d = []
    for i in range(steps + 1):
        t = i / steps
        bx, by = x0 + dx * t, y0 + dy * t
        off = 0 if (i == 0 or i == steps) else amp * math.sin(t * waves * 2 * math.pi)
        d.append('%.2f,%.2f' % (bx + px * off, by + py * off))
    return ('<path d="M' + ' L'.join(d) + '" fill="none" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="round" marker-end="url(#%s)"/>' % (color, w, marker))

def fishhook(x0, y0, cx, cy, x1, y1, color='var(--acc)', w=2.2, side=1):
    """Half-headed (fish-hook) curved arrow: quad curve + one-sided barb."""
    tx, ty = x1 - cx, y1 - cy
    n = math.hypot(tx, ty); tx, ty = tx / n, ty / n
    bx = tx * math.cos(math.radians(150 * side)) - ty * math.sin(math.radians(150 * side))
    by = tx * math.sin(math.radians(150 * side)) + ty * math.cos(math.radians(150 * side))
    bl = 10
    out = ('<path d="M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f" fill="none" stroke="%s" '
           'stroke-width="%.2f" stroke-linecap="round"/>' % (x0, y0, cx, cy, x1, y1, color, w))
    out += line(x1, y1, x1 + bx * bl, y1 + by * bl, w=w, color=color)
    return out

def svg(w, h, inner):
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
            'style="overflow:visible"><defs>%s%s</defs>%s</svg>'
            % (w, h, w, h, arrow_marker('arw'), arrow_marker('arwacc', 'var(--acc)'), inner))

def text(x, y, s, size=14, color='var(--ink)', weight=500, anchor='middle', family='Geist',
         spacing=None, italic=False):
    st = 'font-family:%s;font-size:%.1fpx;font-weight:%d;fill:%s;' % (family, size, weight, color)
    if spacing: st += 'letter-spacing:%.2fpx;' % spacing
    if italic: st += 'font-style:italic;'
    return '<text x="%.2f" y="%.2f" text-anchor="%s" style="%s">%s</text>' % (x, y, anchor, st, s)

# -------------------------------------------------- structure generators ----
COS30, SIN30 = math.cos(math.radians(30)), math.sin(math.radians(30))

def zig(x0, y0, n, L=46, first='up'):
    """n-vertex skeletal zig-zag starting at (x0,y0); 120-degree angles."""
    dx, dy = L * COS30, L * SIN30
    pts = [(x0, y0)]
    x, y = x0, y0
    going_up = (first == 'up')
    for _ in range(n - 1):
        x += dx
        y += -dy if going_up else dy
        pts.append((x, y))
        going_up = not going_up
    return pts

def poly(cx, cy, n, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 360 * i / n)),
             cy + r * math.sin(math.radians(rot + 360 * i / n))) for i in range(n)]

# --------------------------------------------------------------- shell ----
def shell(w, h, pal, kicker, title, body, tag=None, footer=None, fkey=None):
    css_vars = ';'.join('--%s:%s' % (k, v) for k, v in pal.items())
    tag_html = '<div class="tag">%s</div>' % tag if tag else ''
    foot = ''
    if footer:
        foot = ('<div class="ft"><span class="fkey">%s</span><span>%s</span></div>'
                % (fkey or 'NOTE', footer))
    return ('<!doctype html><html><head><meta charset="utf-8"><style>'
            + BASE_CSS + '</style></head><body>'
            + '<div class="plate" style="%s;width:%dpx;height:%dpx;padding:34px 40px 26px">'
            % (css_vars, w, h)
            + '<div class="hd"><span class="kick">%s</span><h1>%s</h1>'
              '<div class="rule"></div>%s</div>' % (kicker, title, tag_html)
            + body + foot + '</div></body></html>')
