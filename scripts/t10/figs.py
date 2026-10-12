#!/usr/bin/env python3
"""Topic 10 figure plates — built on the approved Topic 4/6/7/8/9 pipeline."""
import math
import sys

sys.path.insert(0, '/home/z/my-project/scripts/t6')
from common import (LIGHT, DARK, shell, svg, line, polyline, arrow, text,  # noqa: E402,F401
                    pts_path)

GRID_CSS = """
.duo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;align-content:stretch;margin-top:20px}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;flex:1;align-content:stretch;margin-top:20px}
.card{border:1px solid var(--hair);border-radius:14px;background:var(--card);
  display:flex;flex-direction:column;padding:18px 22px 14px;min-height:0}
.card .ct{display:flex;align-items:baseline;gap:10px}
.card .ct .name{font-weight:600;font-size:15.5px;color:var(--ink);letter-spacing:-.01em}
.card .ct .sig{font-family:'GeistMono',monospace;font-size:11.5px;font-weight:600;
  color:var(--acc);letter-spacing:.06em;margin-left:auto}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.card .art svg{max-width:100%;max-height:100%}
.card .sub{color:var(--body);font-size:12.5px;line-height:1.5;margin-top:10px}
.flow{display:flex;flex-direction:column;gap:14px;flex:1;margin-top:20px;justify-content:center}
.frow{display:flex;align-items:center;gap:14px}
.fbox{border:1px solid var(--hair);border-radius:12px;background:var(--card);
  padding:12px 16px;min-width:150px}
.fbox .t{font-weight:600;font-size:14px;color:var(--ink)}
.fbox .s{font-family:'GeistMono',monospace;font-size:11px;color:var(--muted);margin-top:3px}
.fbox.hot{border-color:var(--accmid);background:var(--accsoft)}
.fbox.hot .t{color:var(--acc)}
.fbox.dead{opacity:.62}
.farr{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:130px}
.farr .l{font-family:'GeistMono',monospace;font-size:10px;font-weight:600;color:var(--acc);
  letter-spacing:.05em;text-transform:uppercase;text-align:center;line-height:1.35}
"""


def card(name, art, sig=None, sub=None):
    s = '<div class="sig">%s</div>' % sig if sig else ''
    sb = '<div class="sub">%s</div>' % sub if sub else ''
    return ('<div class="card"><div class="ct"><span class="name">%s</span>%s</div>'
            '<div class="art">%s</div>%s</div>' % (name, s, art, sb))


def curly(x1, y1, x2, y2, bend=26, color='var(--acc)', w=2.0):
    """Curly-arrow stand-in: a curved electron-pair arrow."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = (y2 - y1), -(x2 - x1)
    n = math.hypot(nx, ny) or 1
    cx, cy = mx + nx / n * bend, my + ny / n * bend
    return ('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" '
            'stroke-width="%.1f" stroke-linecap="round" marker-end="url(#arwacc)"/>'
            % (x1, y1, cx, cy, x2, y2, color, w))


def lonepair(x, y, ang, ln=9, gap=7, color='var(--acc)', w=2.2):
    """A lone pair: two short parallel strokes at angle ang (degrees)."""
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    s = ''
    for off in (-gap / 2, gap / 2):
        s += line(x + px * off, y + py * off, x + px * off + dx * ln, y + py * off + dy * ln,
                  w=w, color=color)
    return s


def bond(x1, y1, x2, y2, w=2.2):
    return line(x1, y1, x2, y2, w=w, color='var(--ink)')


def atom(x, y, s, size=15, color='var(--ink)', weight=700, dx=0, dy=5):
    return text(x + dx, y + dy, s, size, color, weight)


def hilite(cx, cy, r=17):
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--accsoft)" '
            'stroke="var(--accmid)" stroke-width="1.2"/>' % (cx, cy, r))


def txt(x, y, s, size=14, color='var(--ink)', weight=500, anchor='middle',
        family='Geist', spacing=None, italic=False, dx=0, dy=0):
    return text(x + dx, y + dy, s, size, color, weight, anchor, family, spacing, italic)


# ------------------------------------------------- 1 · nucleophilic attack ----
def build_nucleophile(pal):
    W, H = 1240, 560

    def inner(cnum, layout):
        art1 = svg(430, 240,
                   atom(48, 135, 'H₃C', size=14, dx=-4) +
                   bond(74, 130, 122, 130) +
                   atom(140, 130, 'CH₂', size=13.5, dy=5) +
                   bond(158, 130, 206, 130) +
                   atom(224, 130, 'CH₂', size=13.5, dy=5) +
                   hilite(224, 130, r=17) +
                   bond(242, 130, 290, 130) +
                   atom(308, 130, 'Br', size=15.5) +
                   text(224, 92, 'δ+', 16, 'var(--acc)', 700) +
                   text(276, 92, 'δ−', 16, 'var(--cool)', 700) +
                   arrow(228, 158, 262, 158, w=1.4, color='var(--cool)', marker='arw') +
                   text(248, 182, 'bonding electrons pulled towards Br', 10.5,
                        'var(--muted)', 500) +
                   text(224, 216, 'the carbon is electron-deficient — a target', 11,
                        'var(--acc)', 600))
        art2 = svg(430, 240,
                   text(64, 168, 'Nu⁻', 16, 'var(--acc)', 700) +
                   lonepair(64, 140, 90) +
                   curly(92, 158, 148, 148, bend=-14) +
                   hilite(170, 140, r=15) +
                   text(170, 145, 'C', 13.5, 'var(--ink)', 700) +
                   text(170, 104, 'δ+', 13, 'var(--acc)', 700) +
                   bond(185, 140, 250, 140) + text(270, 145, 'X', 14.5, 'var(--ink)', 700) +
                   text(270, 104, 'δ−', 13, 'var(--cool)', 700) +
                   curly(218, 128, 258, 112, bend=-16) +
                   arrow(300, 140, 334, 140, w=1.6, color='var(--muted)') +
                   text(376, 132, 'C–Nu', 12.5, 'var(--acc)', 700) +
                   text(376, 150, '+ X⁻', 12.5, 'var(--cool)', 700) +
                   text(240, 196, 'C–Nu forms', 11, 'var(--acc)', 600) +
                   text(330, 196, 'X leaves as X⁻', 11, 'var(--cool)', 600) +
                   text(240, 226, 'the C–X pair goes with X — heterolytic fission', 10.5,
                        'var(--muted)', 500))
        return ('<div class="duo">'
                + card('The polar C–X bond', art1, 'δ+ / δ−',
                       'The halogen is more electronegative than carbon, so the '
                       'shared electrons sit closer to it. The carbon is left '
                       'electron-deficient — and electron-rich species home in on it.')
                + card('The nucleophilic attack', art2, 'Nu:⁻',
                       'A nucleophile donates a lone pair to the δ+ carbon, forming a '
                       'new covalent bond. The C–X bonding pair leaves with the halogen '
                       '— heterolytic fission, again.') + '</div>')

    body = '<style>%s</style>%s' % (GRID_CSS, inner(0, 'x'))
    return shell(W, H, pal, 'TOPIC 10 · GENERAL PRINCIPLES',
                 'Polarity is the trigger for nucleophilic attack', body,
                 tag='10.3 – 10.5',
                 fkey='SPEC',
                 footer='10.3 heterolytic bond breaking gives electrophiles or '
                        'nucleophiles · 10.4 nucleophile = electron-pair donor · '
                        '10.5 bond polarity decides the mechanism a compound undergoes')


# ------------------------------------------------------- 2 · halo classes ----
def _halo_mol(kind):
    """Displayed formulae of the three classification examples."""
    s = ''
    if kind == 'primary':
        s += hilite(258, 150, r=16)
        s += atom(44, 155, 'H₃C', size=13, dx=-4)
        s += bond(66, 150, 106, 150)
        s += atom(124, 155, 'CH₂', size=13, dy=0)
        s += bond(144, 150, 184, 150)
        s += atom(202, 155, 'CH₂', size=13, dy=0)
        s += bond(222, 150, 240, 150)
        s += atom(258, 155, 'CH₂', size=13, dy=0)
        s += bond(276, 150, 300, 150)
        s += atom(318, 155, 'Br', size=14)
        s += text(180, 96, 'CH₃CH₂CH₂CH₂Br', 12.5, 'var(--muted)', 500, family='GeistMono')
        s += text(240, 200, 'the C–Br carbon has', 11, 'var(--body)', 500) + \
            text(240, 216, 'ONE alkyl chain', 11, 'var(--acc)', 600)
    elif kind == 'secondary':
        c2 = (170, 130)
        s += hilite(*c2, r=15)
        s += txt(96, 135, 'H₃C', 13.5, 'var(--ink)', 600, dx=-8)
        s += bond(112, 130, 156, 130) + text(170, 135, 'C', 14, 'var(--ink)', 700)
        s += bond(184, 130, 228, 130) + txt(244, 135, 'CH₂', 13.5, 'var(--ink)', 600, dx=6)
        s += bond(262, 130, 306, 130) + txt(322, 135, 'CH₃', 13.5, 'var(--ink)', 600, dx=6)
        s += bond(170, 130, 170, 186) + text(170, 204, 'Br', size=14.5)
        s += text(190, 84, 'CH₃CHBrCH₂CH₃', 12.5, 'var(--muted)', 500, family='GeistMono')
        s += text(170, 240, 'TWO alkyl groups', 11, 'var(--acc)', 600)
    else:  # tertiary
        c = (170, 140)
        s += hilite(*c, r=19)
        for tx, lab, ddx in ((110, 'H₃C', -12), (230, 'CH₃', 12)):
            s += bond(c[0], c[1], tx, 140) + txt(tx, 145, lab, 13.5, 'var(--ink)', 600, dx=ddx)
        s += bond(c[0], c[1], c[0], 196) + text(170, 214, 'CH₃', 13.5, 'var(--ink)', 600)
        s += bond(c[0], c[1], c[0], 84) + text(170, 68, 'Br', size=14.5)
        s += text(170, 252, '(CH₃)₃CBr', 12.5, 'var(--muted)', 500, family='GeistMono')
        s += text(170, 272, 'THREE alkyl groups', 11, 'var(--acc)', 600)
    return s


def build_halo_classes(pal):
    W, H = 1240, 560

    def inner(cnum, layout):
        return ('<div class="trio">'
                + card('1-bromobutane', svg(380, 290, _halo_mol('primary')),
                       'PRIMARY', 'Bromine sits on the end carbon — that carbon touches '
                       'one alkyl group.')
                + card('2-bromobutane', svg(380, 290, _halo_mol('secondary')),
                       'SECONDARY', 'The C–Br carbon touches two alkyl groups, one '
                       'either side.')
                + card('2-bromo-2-methylpropane', svg(380, 290, _halo_mol('tertiary')),
                       'TERTIARY', 'Three methyl groups surround the C–Br carbon.')
                + '</div>')

    body = '<style>%s</style>%s' % (GRID_CSS, inner(0, 'x'))
    return shell(W, H, pal, 'TOPIC 10 · HALOGENOALKANES',
                 'Classify by counting the alkyl groups on the C–X carbon', body,
                 tag='10.7',
                 fkey='RULE',
                 footer='Count only the alkyl groups attached to the carbon that '
                        'carries the halogen — then 1°, 2°, 3° is instant.')


# --------------------------------------------------- 3 · substitution mech ----
def build_mechanism(pal):
    W, H = 1300, 620

    def stage1():
        s = svg(360, 300,
                text(96, 96, 'CH₃', 13.5, 'var(--ink)', 600) +
                bond(126, 100, 182, 100) +
                hilite(196, 100, r=15) +
                text(196, 105, 'C', 14.5, 'var(--ink)', 700) +
                text(196, 62, 'δ+', 13, 'var(--acc)', 700) +
                bond(210, 100, 266, 100) + text(286, 105, 'Br', 14.5, 'var(--ink)', 700) +
                text(262, 62, 'δ−', 13, 'var(--cool)', 700) +
                text(64, 208, 'HO⁻', 15, 'var(--acc)', 700) +
                lonepair(56, 188, 90) +
                curly(96, 196, 182, 126, bend=24) +
                curly(220, 88, 258, 78, bend=-20) +
                text(160, 258, 'the lone pair attacks Cδ+…', 11, 'var(--body)', 500) +
                text(160, 274, '…while the C–Br pair leaves with Br', 11, 'var(--body)', 500))
        return card('Stage 1 — attack', s, 'Nu⁻ → Cδ+')

    def stage2():
        s = svg(360, 300,
                text(180, 78, '‡', 30, 'var(--acc)', 600) +
                text(78, 152, 'HO', 14, 'var(--acc)', 700) +
                line(112, 146, 160, 146, w=2, color='var(--acc)', dash='3.5,4.5') +
                text(178, 152, 'C', 14.5, 'var(--ink)', 700) +
                line(196, 146, 244, 146, w=2, color='var(--cool)', dash='3.5,4.5') +
                text(262, 152, 'Br', 14.5, 'var(--cool)', 700) +
                text(74, 176, 'δ−', 12.5, 'var(--acc)', 600) +
                text(268, 176, 'δ−', 12.5, 'var(--cool)', 600) +
                text(180, 196, 'CH₂CH₃', 12, 'var(--muted)', 500) +
                text(180, 244, 'one bond half-made,', 11, 'var(--body)', 500) +
                text(180, 260, 'one half-broken — in the same step', 11, 'var(--body)', 500))
        return card('Stage 2 — transition state', s, '[Br···C···OH]‡')

    def stage3():
        s = svg(360, 300,
                text(118, 128, 'CH₃CH₂', 13.5, 'var(--ink)', 600) +
                text(176, 128, 'OH', 14.5, 'var(--acc)', 700) +
                arrow(204, 122, 240, 122, w=1.6, color='var(--muted)') +
                text(278, 128, 'Br⁻', 14.5, 'var(--cool)', 700) +
                text(180, 196, 'ethanol + bromide', 11.5, 'var(--ink)', 600) +
                text(180, 236, 'substitution complete —', 11, 'var(--body)', 500) +
                text(180, 252, 'OH has taken Br’s place', 11, 'var(--body)', 500))
        return card('Stage 3 — products', s, 'C₂H₅OH + Br⁻')

    def inner(cnum, layout):
        return ('<div class="trio">' + stage1() + stage2() + stage3() + '</div>')

    body = '<style>%s</style>%s' % (GRID_CSS, inner(0, 'x'))
    return shell(W, H, pal, 'TOPIC 10 · HALOGENOALKANES',
                 'Nucleophilic substitution: bromoethane meets aqueous KOH', body,
                 tag='10.9',
                 fkey='MECHANISM',
                 footer='For primary halogenoalkanes with KOH(aq) — and with ammonia — '
                        'substitution runs in this one step. SN1 vs SN2 detail is a '
                        'Unit 4 story.')


# ---------------------------------------------------- 4 · alcohol classes ----
def _alcohol_mol(kind):
    s = ''
    if kind == 'primary':
        s += hilite(230, 150, r=16)
        s += txt(96, 155, 'H₃C', 13.5, 'var(--ink)', 600, dx=-6)
        s += bond(112, 150, 168, 150)
        s += txt(182, 155, 'CH₂', 13.5, 'var(--ink)', 600, dx=4)
        s += bond(206, 150, 246, 150)
        s += txt(264, 155, 'OH', 14.5, 'var(--acc)', 700, dx=4)
        s += text(200, 96, 'CH₃CH₂OH', 12.5, 'var(--muted)', 500, family='GeistMono') + \
            text(230, 202, 'the C–OH carbon has', 11, 'var(--body)', 500) + \
            text(230, 218, 'ONE alkyl chain', 11, 'var(--acc)', 600)
    elif kind == 'secondary':
        s += hilite(170, 130, r=16)
        s += txt(96, 135, 'H₃C', 13.5, 'var(--ink)', 600, dx=-8)
        s += bond(112, 130, 156, 130)
        s += text(170, 135, 'C', 14, 'var(--ink)', 700)
        s += bond(184, 130, 228, 130) + txt(244, 135, 'CH₃', 13.5, 'var(--ink)', 600, dx=6)
        s += bond(170, 130, 170, 186) + text(170, 204, 'OH', 14.5, 'var(--acc)', 700)
        s += text(170, 84, 'CH₃CHOHCH₃', 12.5, 'var(--muted)', 500, family='GeistMono') + \
            text(170, 238, 'TWO alkyl groups', 11, 'var(--acc)', 600)
    else:
        s += hilite(170, 140, r=18)
        for tx, lab, ddx in ((110, 'H₃C', -12), (230, 'CH₃', 12)):
            s += bond(170, 140, tx, 140) + txt(tx, 145, lab, 13.5, 'var(--ink)', 600, dx=ddx)
        s += bond(170, 140, 170, 196) + text(170, 214, 'CH₃', 13.5, 'var(--ink)', 600)
        s += bond(170, 140, 170, 84) + text(170, 68, 'OH', 14.5, 'var(--acc)', 700)
        s += text(170, 248, '(CH₃)₃COH', 12.5, 'var(--muted)', 500, family='GeistMono') + \
            text(170, 270, 'THREE alkyl groups', 11, 'var(--acc)', 600)
    return s


def build_alcohol_classes(pal):
    W, H = 1240, 560

    def inner(cnum, layout):
        return ('<div class="trio">'
                + card('ethanol', svg(380, 290, _alcohol_mol('primary')),
                       'PRIMARY', '–CH₂OH at the end of the chain.')
                + card('propan-2-ol', svg(380, 290, _alcohol_mol('secondary')),
                       'SECONDARY', 'The –OH carbon bridges two alkyl groups.')
                + card('2-methylpropan-2-ol', svg(380, 290, _alcohol_mol('tertiary')),
                       'TERTIARY', 'Three methyl groups on the –OH carbon.')
                + '</div>')

    body = '<style>%s</style>%s' % (GRID_CSS, inner(0, 'x'))
    return shell(W, H, pal, 'TOPIC 10 · ALCOHOLS',
                 'Classify by counting the alkyl groups on the C–OH carbon', body,
                 tag='10.16',
                 fkey='RULE',
                 footer='Same counting rule as halogenoalkanes — and the class you '
                        'assign decides the oxidation product.')


# ----------------------------------------------------- 5 · oxidation flow ----
def build_oxidation(pal):
    W, H = 1340, 580

    def box(t, s, hot=False, dead=False):
        cls = 'fbox' + (' hot' if hot else '') + (' dead' if dead else '')
        return ('<div class="%s"><div class="t">%s</div><div class="s">%s</div></div>'
                % (cls, t, s))

    def arr(l1, l2):
        return ('<div class="farr"><div class="l">%s</div>%s<div class="l">%s</div></div>'
                % (l1, arrow(0, 0, 64, 0, w=1.8, color='var(--acc)'), l2))

    def inner(cnum, layout):
        r1 = ('<div class="frow">' + box('propan-1-ol', 'PRIMARY', hot=True)
              + arr('distil the product', 'as it forms')
              + box('propanal', 'ALDEHYDE · Benedict’s / Fehling’s positive', hot=True)
              + arr('reflux with', 'excess [O]')
              + box('propanoic acid', 'CARBOXYLIC ACID · fizzes with Na₂CO₃', hot=True)
              + '</div>')
        r2 = ('<div class="frow">' + box('propan-2-ol', 'SECONDARY', hot=True)
              + arr('reflux', '[O]')
              + box('propanone', 'KETONE · no further oxidation', hot=True)
              + '<div style="flex:1"></div></div>')
        r3 = ('<div class="frow">' + box('2-methylpropan-2-ol', 'TERTIARY')
              + arr('acidified dichromate', 'warmed')
              + box('no reaction', 'dichromate stays ORANGE', dead=True)
              + '<div style="flex:1"></div></div>')
        note = ('<div class="chip" style="margin-top:16px;align-self:flex-start">'
                'oxidant: K₂Cr₂O₇ / dilute H₂SO₄ · written [O] in equations · '
                'observation: orange → green</div>')
        return ('<div class="flow">' + r1 + r2 + r3 + note + '</div>')

    body = '<style>%s</style>%s' % (GRID_CSS, inner(0, 'x'))
    return shell(W, H, pal, 'TOPIC 10 · ALCOHOLS',
                 'The class decides the oxidation product', body,
                 tag='10.18',
                 fkey='EXAM',
                 footer='Two phrases carry the marks — aldehyde: “distil off as it '
                        'forms”; carboxylic acid: “heat under reflux”.')


# ------------------------------------------------------- 6 · mass spectrum ----
def build_mass_spectrum(pal):
    W, H = 1240, 640
    X0, Y0, AW, AH = 110, 452, 1000, 300

    peaks = [
        (15, 0.16, 'var(--muted)'),
        (29, 0.52, 'var(--ink)'),
        (43, 1.00, 'var(--acc)'),
        (57, 0.07, 'var(--muted)'),
        (58, 0.30, 'var(--acc)'),
        (59, 0.025, 'var(--muted)'),
    ]

    def inner(cnum, layout):
        s = line(X0, Y0, X0 + AW, Y0, w=2, color='var(--ink)')
        s += line(X0, Y0, X0, Y0 - AH, w=2, color='var(--ink)')
        s += text(X0 + AW / 2, Y0 + 44, 'm/z', 12.5, 'var(--body)', 600, family='GeistMono')
        s += ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
              'style="font-family:GeistMono;font-size:11.5px;font-weight:600;'
              'fill:var(--body);letter-spacing:1px">relative abundance</text>'
              % (X0 - 40, Y0 - AH / 2, X0 - 40, Y0 - AH / 2))
        scale = (AW - 40) / 70.0
        for mz, h, col in peaks:
            x = X0 + 20 + mz * scale
            y = Y0 - h * (AH - 46)
            s += line(x, Y0, x, y, w=3.4, color=col, cap='butt')
            if mz in (15, 29, 43, 58):
                s += text(x, Y0 + 18, str(mz), 11.5, 'var(--muted)', 600, family='GeistMono')
            elif mz == 59:
                s += text(x + 14, Y0 + 18, '59', 11.5, 'var(--muted)', 600, family='GeistMono')

        def leader(mz, h, tx, ty, lines, col, anchor='start'):
            x = X0 + 20 + mz * scale
            y = Y0 - h * (AH - 46)
            out = line(x, y - 6, tx, ty + 4, w=1.1, color='var(--faint)')
            for i, ln in enumerate(lines):
                out += text(tx, ty + i * 16, ln, 11, col, 600 if i == 0 else 500,
                            anchor=anchor)
            return out
        s += leader(29, 0.52, X0 + 40, Y0 - AH - 6, ['C₂H₅⁺ = M − 29'], 'var(--ink)')
        s += leader(43, 1.0, X0 + 300, Y0 - AH - 6,
                    ['C₃H₇⁺ = M − 15', '(CH₃ lost)'], 'var(--acc)')
        s += leader(58, 0.30, X0 + 660, Y0 - AH + 8,
                    ['M⁺ peak — m/z = Mᵣ = 58', 'the molecule’s size'], 'var(--acc)')
        s += leader(59, 0.025, X0 + 560, Y0 - 74, ['M+1 — the ¹³C peak'], 'var(--muted)',
                    anchor='end')
        x15 = X0 + 20 + 15 * scale
        y15 = Y0 - 0.16 * (AH - 46)
        s += text(x15, y15 - 12, 'CH₃⁺', 11, 'var(--muted)', 600)
        return ('<div style="flex:1;display:flex;align-items:center;justify-content:center">'
                + svg(1160, 520, s) + '</div>')

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · MASS SPECTRA',
                 'Butane: read the spectrum right to left', body,
                 tag='10.21',
                 fkey='METHOD',
                 footer='Size first — M⁺ gives Mᵣ. Then subtract: each fragment peak '
                        'tells you which piece broke off. M+1 counts the carbons.')


# ----------------------------------------------------------- 7 · IR spectrum ----
def build_ir_spectrum(pal):
    W, H = 1240, 640
    X0, Y0, AW, AH = 110, 452, 1000, 300

    def inner(cnum, layout):
        s = line(X0, Y0, X0 + AW, Y0, w=2, color='var(--ink)')
        s += line(X0, Y0, X0, Y0 - AH, w=2, color='var(--ink)')
        s += text(X0 + AW / 2, Y0 + 44, 'wavenumber / cm⁻¹   (4000 → 600)',
                  12.5, 'var(--body)', 600, family='GeistMono')
        s += ('<text x="%.0f" y="%.0f" text-anchor="middle" transform="rotate(-90 %.0f %.0f)" '
              'style="font-family:GeistMono;font-size:11.5px;font-weight:600;'
              'fill:var(--body);letter-spacing:1px">transmittance</text>'
              % (X0 - 40, Y0 - AH / 2, X0 - 40, Y0 - AH / 2))

        def wx(wn):
            return X0 + (4000 - wn) / (4000 - 600) * AW
        for wn in (4000, 3500, 3000, 2500, 2000, 1500, 1000, 600):
            s += line(wx(wn), Y0, wx(wn), Y0 + 6, w=1.2, color='var(--faint)')
            s += text(wx(wn), Y0 + 20, str(wn), 10.5, 'var(--muted)', 500, family='GeistMono')

        pts = []
        n = 560
        for i in range(n + 1):
            wn = 4000 - (4000 - 600) * i / n
            y = 0.86
            d = (wn - 3370) / 190.0
            if 3000 <= wn <= 3700:
                y -= 0.20 * math.exp(-d * d)
            d = (wn - 2950) / 34.0
            y -= 0.13 * math.exp(-d * d)
            d = (wn - 1715) / 21.0
            y -= 0.52 * math.exp(-d * d)
            if wn < 1500:
                t = (1500 - wn) / 900.0
                y -= (0.06 + 0.05 * math.sin(wn / 47.0) + 0.045 * math.sin(wn / 13.7)) * t
                y -= 0.10 * t
            pts.append((wx(wn), Y0 - y * (AH - 40)))
        s += polyline(pts, w=2.6, color='var(--ink)')

        s += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--accsoft)"/>'
              % (wx(1500), Y0 - AH + 16, wx(600) - wx(1500), AH - 16))
        s += line(wx(1500), Y0 - AH + 16, wx(1500), Y0, w=1.2,
                  color='var(--accmid)', dash='4,4')
        s += text(wx(1050), Y0 - AH + 42, 'fingerprint region  < 1500 cm⁻¹',
                  11.5, 'var(--acc)', 600)
        s += text(wx(1050), Y0 - AH + 60, 'unique to each molecule', 10.5,
                  'var(--muted)', 500)

        def tag(wn, frac, lines, col='var(--acc)', anchor='middle'):
            x, y = wx(wn), Y0 - (0.86 - frac) * (AH - 40)
            out = ''
            for i, ln in enumerate(lines):
                out += text(x, y - 18 - i * 16, ln, 11, col, 600 if i == 0 else 500,
                            anchor=anchor)
            return out
        s += tag(3370, 0.66, ['O–H (alcohol)', '3200–3550 · BROAD'])
        s += tag(2950, 0.73, ['C–H 2850–3300'], 'var(--muted)')
        # C=O label offset right of the narrow dip, with a leader to the trough
        xc, yc = wx(1715), Y0 - (0.86 - 0.34) * (AH - 40)
        s += line(xc + 10, yc + 6, xc + 40, yc - 12, w=1.1, color='var(--faint)')
        s += text(xc + 46, yc - 8, 'C=O', 11, 'var(--acc)', 600, anchor='start')
        s += text(xc + 46, yc + 8, '1630–1820 · SHARP', 11, 'var(--acc)', 500, anchor='start')
        return ('<div style="flex:1;display:flex;align-items:center;justify-content:center">'
                + svg(1160, 520, s) + '</div>')

    body = inner(0, 'x')
    return shell(W, H, pal, 'TOPIC 10 · INFRARED',
                 'Every dip names a bond', body,
                 tag='10.22',
                 fkey='METHOD',
                 footer='Broad dip = O–H. Sharp dip = C=O. Both together, with the '
                        'O–H reaching below 3000 — a carboxylic acid.')
