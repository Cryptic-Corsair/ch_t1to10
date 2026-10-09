#!/usr/bin/env python3
"""Topic 4 v2 — plates: fractionating column, pollutants map."""
import math
from common import shell, svg, text, line, arrow, arrow_marker, poly

# ------------------------------------------------------ fractionating column ----
def column_zone():
    W, H = 470, 596
    top_w, bot_w, ty, by = 148, 226, 46, 546
    cx = 292
    tx1, tx2 = cx - top_w / 2, cx + top_w / 2
    bx1, bx2 = cx - bot_w / 2, cx + bot_w / 2
    inner = ''
    # temperature sidebar
    inner += ('<defs><linearGradient id="tg" x1="0" y1="0" x2="0" y2="1">'
              '<stop offset="0" stop-color="var(--cool)"/>'
              '<stop offset="1" stop-color="var(--acc)"/></linearGradient>'
              '<linearGradient id="tw" x1="0" y1="0" x2="0" y2="1">'
              '<stop offset="0" stop-color="var(--coolsoft)"/>'
              '<stop offset="0.55" stop-color="rgba(128,128,128,0.05)"/>'
              '<stop offset="1" stop-color="var(--accsoft)"/></linearGradient></defs>')
    inner += ('<rect x="52" y="%d" width="7" height="%d" rx="3.5" fill="url(#tg)"/>' % (ty + 4, by - ty - 8))
    inner += text(40, ty + 14, 'cool', size=10.5, color='var(--cool)', weight=600,
                  family='GeistMono', anchor='end', spacing=1)
    inner += text(40, by - 4, 'hot', size=10.5, color='var(--acc)', weight=600,
                  family='GeistMono', anchor='end', spacing=1)
    # tower body
    inner += ('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" fill="url(#tw)" '
              'stroke="var(--muted)" stroke-width="1.6" stroke-linejoin="round"/>'
              % (tx1, ty, tx2, ty, bx2, by, bx1, by))
    # trays (7)
    tray_ys = []
    for i in range(7):
        t = i / 6
        y = ty + 40 + t * (by - ty - 84)
        xw1 = tx1 + (bx1 - tx1) * t + 20
        xw2 = tx2 + (bx2 - tx2) * t - 20
        inner += line(xw1, y, xw2, y, w=1.5, color='var(--muted)')
        tray_ys.append(y)
    # rising vapour arrow (single, dashed, hand-drawn head)
    inner += line(cx, 505, cx, 182, w=2.2, color='var(--muted)', dash='6,6')
    inner += line(cx, 182, cx - 7, 196, w=2.2, color='var(--muted)')
    inner += line(cx, 182, cx + 7, 196, w=2.2, color='var(--muted)')
    # crude inlet
    inner += arrow(56, 452, 148, 452, w=2.2, color='var(--body)')
    inner += text(40, 484, 'crude oil,', size=11.5, color='var(--muted)',
                  weight=500, family='GeistMono', anchor='start', spacing=0.3)
    inner += text(40, 501, 'heated and vaporised', size=11.5, color='var(--muted)',
                  weight=500, family='GeistMono', anchor='start', spacing=0.3)
    return svg(W, H, inner), tray_ys, W, H, ty, by

def build_column(pal):
    css = """
.fc-grid{display:grid;grid-template-columns:470px 1fr;gap:30px;flex:1;margin-top:10px;min-height:0;
  position:relative;padding-right:34px}
.fc-rows{display:flex;flex-direction:column;justify-content:space-between;padding:8px 0 6px}
.fc-row{display:grid;grid-template-columns:170px 1fr;align-items:center;gap:12px}
.fc-name{font-size:15.5px;font-weight:600;color:var(--ink);white-space:nowrap}
.fc-bar{height:9px;border-radius:5px;background:var(--faint);position:relative;overflow:hidden}
.fc-bar i{position:absolute;inset:0 auto 0 0;border-radius:5px;background:var(--acc);opacity:.85}
.fc-axis{position:absolute;right:0;top:8px;bottom:8px;display:flex;align-items:center;
  justify-content:center}
.fc-axis span{writing-mode:vertical-rl;transform:rotate(180deg);font-family:'GeistMono',monospace;
  font-size:10px;font-weight:600;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;
  border-left:1px solid var(--hair);padding-left:9px}
"""
    colsvg, tray_ys, W, H, ty, by = column_zone()
    fractions = ['refinery gas', 'petrol', 'naphtha', 'kerosene', 'diesel', 'fuel oil', 'residue']
    rows = ''
    n = len(fractions)
    for i, f in enumerate(fractions):
        bw = 34 + i * (172 - 34) / (n - 1)
        rows += ('<div class="fc-row"><span class="fc-name">%s</span>'
                 '<span class="fc-bar"><i style="width:%.0f%%"></i></span></div>'
                 % (f, bw / 172 * 100))
    axis = '<div class="fc-axis"><span>chain length · boiling point increase</span></div>'
    body = ('<style>%s</style><div class="fc-grid">%s<div class="fc-rows">%s</div>%s</div>'
            % (css, colsvg, rows, axis))
    return shell(1152, 768, pal, 'SPEC 4.12 · FRACTIONAL DISTILLATION',
                 'The fractionating column', body,
                 footer='Each fraction is a mixture of hydrocarbons with similar chain lengths — '
                        'long chains condense low where it is hot; short chains rise before '
                        'condensing near the cool top.', fkey='4.12')

# ---------------------------------------------------------- pollutants map ----
def build_pollutants(pal):
    css = """
.pl-head{display:grid;grid-template-columns:1fr 40px 208px 40px 1.12fr;gap:10px;
  margin:20px 0 12px;font-family:'GeistMono',monospace;font-size:10px;font-weight:600;
  letter-spacing:.16em;color:var(--muted);text-transform:uppercase}
.pl-head span:nth-child(2),.pl-head span:nth-child(4){text-align:center}
.pl-row{display:grid;grid-template-columns:1fr 40px 208px 40px 1.12fr;gap:10px;align-items:stretch;flex:1}
.pl-cell{border:1px solid var(--hair);background:var(--card);border-radius:10px;
  display:flex;align-items:center;padding:10px 16px;font-size:13.5px;font-weight:500;
  color:var(--body);line-height:1.4;min-height:62px}
.pl-cell.acc{justify-content:center;background:var(--accsoft);border-color:var(--accmid);
  color:var(--acc);font-weight:600;font-size:15.5px}
.pl-cell .dim{color:var(--muted);font-weight:400}
.pl-arr{display:flex;align-items:center;justify-content:center}
.pl-rows{display:flex;flex-direction:column;gap:12px;flex:1}
"""
    rows = [
        ('plenty of oxygen <span class="dim">— complete combustion</span>', 'CO<sub>2</sub>',
         'greenhouse gas — climate change'),
        ('limited oxygen <span class="dim">— incomplete combustion</span>', 'CO',
         'binds haemoglobin — oxygen transport blocked'),
        ('severe oxygen starvation', 'C particulates',
         'respiratory harm (asthma) · global dimming'),
        ('fuel escapes combustion entirely', 'unburned hydrocarbons',
         'ground-level ozone · smog'),
        ('N<sub>2</sub>&nbsp;+&nbsp;O<sub>2</sub>&nbsp; react in hot engines', 'NO<sub>x</sub>',
         'nitric acid — acid rain · photochemical smog'),
        ('sulfur impurities in the fuel burn', 'SO<sub>2</sub>',
         'sulfurous acid — acid rain'),
    ]
    head = ('<div class="pl-head"><span>Origin</span><span></span><span>Pollutant</span>'
            '<span></span><span>Problem</span></div>')
    body_rows = ''
    for origin, pol, prob in rows:
        arr = svg(30, 20, arrow(2, 10, 26, 10, w=1.7, color='var(--muted)'))
        body_rows += ('<div class="pl-row"><div class="pl-cell">%s</div>'
                      '<div class="pl-arr">%s</div><div class="pl-cell acc">%s</div>'
                      '<div class="pl-arr">%s</div><div class="pl-cell">%s</div></div>'
                      % (origin, arr, pol, arr, prob))
    body = ('<style>%s</style>%s<div class="pl-rows">%s</div>'
            % (css, head, body_rows))
    return shell(1248, 736, pal, 'SPEC 4.13 – 4.14 · COMBUSTION POLLUTANTS',
                 'Origin → pollutant → problem', body,
                 footer='NO<sub>x</sub> comes from the <b>air</b> — the fuel itself contains no '
                        'nitrogen. SO<sub>2</sub> really does come from the fuel\u2019s sulfur '
                        'impurities. CO<sub>2</sub> is not toxic — it is the greenhouse gas.',
                 fkey='TRAP')

COLUMN = ('fractionating-column', 1152, 768, build_column)
POLLUTANTS = ('pollutants-map', 1248, 736, build_pollutants)
