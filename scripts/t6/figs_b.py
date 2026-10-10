#!/usr/bin/env python3
"""Topic 6 plates, set B: calorimetry apparatus (solution + combustion)."""
import math
from common import shell, svg, text, line

CARD_CSS = """
.solo{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 12px;margin-top:20px;flex:1;min-height:0}
.solo .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.solo .art svg{max-width:100%;max-height:100%}
"""

# local palette additions (mode-stable)
COPPER = {'light': ('#c97e54', '#a3603c'), 'dark': ('#d99a70', '#b87f58')}
WATER = {'light': 'rgba(61,127,166,.40)', 'dark': 'rgba(125,180,216,.30)'}
FLAME_OUT = '#e8734a'
FLAME_IN = '#f2b544'

def lab(ink_xy, tip_xy, s, anchor='start'):
    """Label with leader line ending in a dot at the target point."""
    (x1, y1), (x2, y2) = ink_xy, tip_xy
    out = ('<circle cx="%.1f" cy="%.1f" r="2.6" fill="var(--muted)"/>' % (x2, y2)
           + line(x2, y2, x1 - 6 if anchor == 'start' else x1 + 6, y1 - 4, w=1.2,
                  color='var(--hair)'))
    out += text(x1, y1, s, size=13.5, weight=600, anchor=anchor)
    return out

# ------------------------------------------------------------ solution cup ----
def build_solution(pal):
    W, H = 1120, 372
    inner = ''
    mode = 'dark' if pal['ink'].startswith('#e') else 'light'
    copper, copper_edge = COPPER[mode]
    # beaker (outer glass)
    inner += ('<rect x="118" y="118" width="364" height="216" rx="10" fill="none" '
              'stroke="var(--hair)" stroke-width="2.2"/>')
    inner += ('<rect x="118" y="118" width="10" height="216" rx="5" fill="var(--card2)"/>'
              '<rect x="472" y="118" width="10" height="216" rx="5" fill="var(--card2)"/>')
    # polystyrene cup (tapered)
    inner += ('<path d="M150,140 L450,140 L424,312 Q423,320 414,320 L186,320 '
              'Q177,320 176,312 Z" fill="var(--card2)" stroke="var(--muted)" stroke-width="2"/>')
    # cup rim band
    inner += ('<rect x="142" y="128" width="316" height="16" rx="8" fill="var(--card2)" '
              'stroke="var(--muted)" stroke-width="1.6"/>')
    # solution inside the cup
    inner += ('<path d="M156,206 L444,206 L426,308 Q425,314 417,314 L183,314 '
              'Q175,314 174,308 Z" fill="var(--coolsoft)" stroke="none"/>')
    inner += ('<path d="M156,206 Q204,201 252,206 T348,206 T444,206" fill="none" '
              'stroke="var(--cool)" stroke-width="2.6"/>')
    # bubbles
    for bx, by, r in ((225, 250, 4.5), (318, 270, 3.4), (372, 238, 3.8), (262, 292, 3.0)):
        inner += '<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="var(--cool)" stroke-width="1.6"/>' % (bx, by, r)
    # lid
    inner += ('<rect x="136" y="112" width="328" height="20" rx="9" fill="var(--card)" '
              'stroke="var(--muted)" stroke-width="2"/>')
    # thermometer through the lid
    inner += line(268, 34, 268, 258, w=6, color='var(--muted)')
    inner += '<circle cx="268" cy="266" r="10" fill="var(--acc)"/>'
    inner += line(268, 252, 268, 186, w=2.6, color='var(--acc)', cap='butt')
    for ty in range(92, 200, 18):
        inner += line(274, ty, 283, ty, w=1.6, color='var(--muted)')
    # labels
    inner += lab((560, 46), (284, 52), 'Thermometer')
    inner += lab((560, 128), (466, 124), 'Insulating lid')
    inner += lab((560, 210), (442, 226), 'Polystyrene cup')
    inner += lab((560, 288), (424, 282), 'Reaction solution')
    inner += lab((560, 348), (486, 330), 'Beaker for support')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div></div>' % svg(W, H, inner))
    return shell(1248, 560, pal, 'SPEC 6.5 · SOLUTION CALORIMETRY',
                 'The insulated-container experiment',
                 body, tag='mixing two solutions',
                 footer='A polystyrene cup inside a beaker for support — the insulated container '
                        'minimises heat exchange. q = mcΔT with m = total mass of solution, '
                        'c = 4.18 J g⁻¹ °C⁻¹, and the alkali in slight excess.',
                 fkey='APPARATUS')

# --------------------------------------------------------- combustion bench ----
def build_combustion(pal):
    W, H = 1120, 372
    mode = 'dark' if pal['ink'].startswith('#e') else 'light'
    copper, copper_edge = COPPER[mode]
    water = WATER[mode]
    inner = ''
    # draught shield: back panel + side flanges
    inner += ('<rect x="304" y="76" width="330" height="276" rx="10" fill="var(--card)" '
              'stroke="var(--hair)" stroke-width="2"/>')
    inner += ('<rect x="284" y="92" width="20" height="252" rx="6" fill="var(--card2)" '
              'stroke="var(--hair)" stroke-width="1.6"/>')
    inner += ('<rect x="634" y="92" width="20" height="252" rx="6" fill="var(--card2)" '
              'stroke="var(--hair)" stroke-width="1.6"/>')
    # ground line
    inner += line(300, 372, 640, 372, w=2.4, color='var(--muted)')
    # spirit burner
    inner += ('<rect x="412" y="304" width="116" height="64" rx="12" fill="var(--card2)" '
              'stroke="var(--muted)" stroke-width="2.2"/>')
    inner += ('<rect x="446" y="290" width="48" height="16" rx="5" fill="var(--card2)" '
              'stroke="var(--muted)" stroke-width="2"/>')
    inner += line(470, 290, 470, 278, w=5, color='var(--muted)')
    # flame (outer + inner)
    inner += ('<path d="M470,256 C457,266 450,274 450,282 C450,291 459,297 470,297 '
              'C481,297 490,291 490,282 C490,274 483,266 470,256 Z" fill="%s"/>' % FLAME_OUT)
    inner += ('<path d="M470,268 C464,273 461,277 461,281 C461,286 465,289 470,289 '
              'C475,289 479,286 479,281 C479,277 476,273 470,268 Z" fill="%s"/>' % FLAME_IN)
    # tripod legs + ring
    inner += line(352, 254, 320, 372, w=4, color='var(--muted)')
    inner += line(588, 254, 620, 372, w=4, color='var(--muted)')
    inner += line(344, 254, 596, 254, w=4, color='var(--muted)')
    # copper can
    inner += ('<rect x="366" y="112" width="208" height="142" rx="12" fill="%s" '
              'stroke="%s" stroke-width="2.6"/>' % (copper, copper_edge))
    inner += ('<ellipse cx="470" cy="112" rx="104" ry="10" fill="%s" stroke="%s" '
              'stroke-width="2"/>' % (copper, copper_edge))
    # water inside the can (cutaway)
    inner += ('<rect x="380" y="146" width="180" height="94" rx="8" fill="%s"/>' % water)
    inner += ('<ellipse cx="470" cy="146" rx="90" ry="8" fill="%s" '
              'stroke="var(--cool)" stroke-width="2"/>' % water)
    inner += line(380, 148, 380, 234, w=2, color='var(--cool)')
    inner += line(560, 148, 560, 234, w=2, color='var(--cool)')
    inner += ('<path d="M380,236 Q425,241 470,236 T560,236" fill="none" '
              'stroke="var(--cool)" stroke-width="2.4"/>')
    # thermometer into the can
    inner += line(470, 30, 470, 196, w=6, color='var(--muted)')
    inner += '<circle cx="470" cy="204" r="10" fill="var(--acc)"/>'
    for ty in range(70, 170, 18):
        inner += line(476, ty, 485, ty, w=1.6, color='var(--muted)')
    # labels
    inner += lab((700, 44), (486, 44), 'Thermometer')
    inner += lab((700, 148), (566, 156), 'Water')
    inner += lab((700, 214), (578, 208), 'Copper can')
    inner += lab((700, 96), (656, 92), 'Draught shield')
    inner += lab((700, 330), (528, 330), 'Spirit burner')
    body = ('<style>%s</style>' % CARD_CSS
            + '<div class="solo"><div class="art">%s</div></div>' % svg(W, H, inner))
    return shell(1248, 560, pal, 'SPEC 6.5 · COMBUSTION CALORIMETRY',
                 'The spirit-burner experiment',
                 body, tag='burning a fuel',
                 footer='The fuel burns beneath a known mass of water inside a draught shield; the '
                        'copper can conducts heat to the water. Weigh the burner before and after — '
                        'the mass difference is the fuel burned. Reweigh after extinguishing at '
                        'about a 20 °C rise.',
                 fkey='APPARATUS')

SOLUTION = ('calorimetry-solution', 1248, 560, build_solution)
COMBUSTION = ('calorimetry-combustion', 1248, 560, build_combustion)
