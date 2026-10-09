#!/usr/bin/env python3
"""Topic 8 plates, set A: electron transfer, agents map, disproportionation, Group 1/2 trends."""
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
.eqrow{display:flex;justify-content:center;gap:26px;margin-top:12px;font-family:'GeistMono',monospace;
  font-size:13px;color:var(--body);flex-wrap:wrap}
.eqrow b{color:var(--ink);font-weight:600}
.eqrow .ox{color:var(--acc)}
.eqrow .rd{color:var(--cool)}
"""

def eq_band(lines):
    rows = ''
    for i, (code, tag) in enumerate(lines):
        rows += ('<div class="eqrow"><span>%s</span><span class="%s">%s</span></div>'
                 % (code, 'ox' if tag == 'ox' else ('rd' if tag == 'rd' else ''), tag if tag in ('ox', 'rd') else ''))
    return rows

# ---------------------------------------------------------- 1. electron transfer ----
def build_electron_transfer(pal):
    W, H = 1180, 470
    inner = ''
    # zinc atom
    zx, zy = 250, 190
    inner += '<circle cx="%d" cy="%d" r="46" fill="var(--card2)" stroke="var(--ink)" stroke-width="2.4"/>' % (zx, zy)
    inner += text(zx, zy + 7, 'Zn', 26, 'var(--ink)', 700)
    inner += text(zx, zy + 92, 'zinc atom', 13.5, 'var(--body)', 600)
    # copper ion
    cx_, cy_ = 930, 190
    inner += '<circle cx="%d" cy="%d" r="40" fill="var(--coolsoft)" stroke="var(--cool)" stroke-width="2.4"/>' % (cx_, cy_)
    inner += text(cx_, cy_ + 2, 'Cu', 20, 'var(--cool)', 700)
    inner += text(cx_, cy_ + 22, '2+', 13, 'var(--cool)', 700)
    inner += text(cx_, cy_ + 86, 'copper(II) ion', 13.5, 'var(--body)', 600)
    # electron arrow (two e-)
    inner += ('<path d="M %d %d Q %d %d %d %d" fill="none" stroke="var(--acc)" stroke-width="2.4" marker-end="url(#arwacc)"/>'
              % (zx + 66, zy - 20, (zx + cx_) / 2, zy - 96, cx_ - 62, cy_ - 14))
    inner += text((zx + cx_) / 2, zy - 66, '2e⁻ transferred', 14.5, 'var(--acc)', 700, family='GeistMono')
    inner += text((zx + cx_) / 2, zy - 46, 'zinc is the reducing agent', 12.5, 'var(--muted)', 500)
    # products
    inner += text(zx + 10, 330, '→  Zn²⁺(aq)   +   Cu(s)   (red-brown coat)', 15, 'var(--ink)', 600, family='GeistMono')
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:4px 10px 0">%s</div>'
            '<div class="eqrow"><span class="ox">Zn(s) → Zn²⁺(aq) + 2e⁻&nbsp;&nbsp;[oxidation]</span>'
            '<span class="rd">Cu²⁺(aq) + 2e⁻ → Cu(s)&nbsp;&nbsp;[reduction]</span></div>'
            '<div class="eqrow" style="margin-top:6px"><b>Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)</b></div>'
            '</div>' % (CARD_CSS, svg(W, H, inner)))
    return shell(1340, 640, pal, 'SPEC 8.5 · 8.6 · ELECTRON TRANSFER',
                 'Zinc displacing copper from copper(II) sulfate',
                 body, tag='redox = transfer',
                 footer='Each zinc atom gives two electrons directly to a copper(II) ion. The half-equations '
                        'are added with the electrons cancelling — electrons never appear in the overall ionic equation.',
                 fkey='MODEL')

# ---------------------------------------------------------- 2. agents map ----
def build_agents_map(pal):
    W, H = 500, 420
    inner = ''
    y0 = 120
    xs = [80, 210, 340, 452]
    labels = ['Cl₂', 'KBr', 'KCl', 'Br₂']
    ons = ['0', '+1 −1', '+1 −1', '0']
    colors = ['var(--ink)', 'var(--ink)', 'var(--ink)', 'var(--ink)']
    for x, lb, on in zip(xs, labels, ons):
        inner += text(x, y0, lb, 20, 'var(--ink)', 700)
        inner += text(x, y0 + 26, on, 12.5, 'var(--muted)', 600, family='GeistMono')
    inner += text(146, y0, '+', 16, 'var(--muted)', 500)
    inner += text(276, y0, '→', 18, 'var(--ink)', 700)
    inner += text(398, y0, '+', 16, 'var(--muted)', 500)
    # reduction arrow: Cl2 -> Cl- (top)
    inner += ('<path d="M 80 %d Q 160 %d 328 %d" fill="none" stroke="var(--cool)" stroke-width="2.2" marker-end="url(#arw)"/>'
              % (y0 - 44, y0 - 88, y0 - 44))
    inner += text(204, y0 - 100, 'reduction (0 → −1)', 13, 'var(--cool)', 600, family='GeistMono')
    # oxidation arrow: Br- -> Br2 (bottom)
    inner += ('<path d="M 224 %d Q 330 %d 446 %d" fill="none" stroke="var(--acc)" stroke-width="2.2" marker-end="url(#arwacc)"/>'
              % (y0 + 52, y0 + 96, y0 + 52))
    inner += text(336, y0 + 116, 'oxidation (−1 → 0)', 13, 'var(--acc)', 600, family='GeistMono')
    # agent boxes
    inner += ('<rect x="30" y="%d" width="150" height="74" rx="10" fill="var(--coolsoft)" stroke="var(--cool)" stroke-width="1.4"/>'
              % (y0 + 150))
    inner += text(105, y0 + 178, 'OXIDISING AGENT', 11.5, 'var(--cool)', 700, family='GeistMono')
    inner += text(105, y0 + 200, 'Cl₂ gains the electrons', 12.5, 'var(--body)', 500)
    inner += ('<rect x="230" y="%d" width="150" height="74" rx="10" fill="var(--accsoft)" stroke="var(--acc)" stroke-width="1.4"/>'
              % (y0 + 150))
    inner += text(305, y0 + 178, 'REDUCING AGENT', 11.5, 'var(--acc)', 700, family='GeistMono')
    inner += text(305, y0 + 200, 'Br⁻ gives the electrons', 12.5, 'var(--body)', 500)
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 6px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner)))
    return shell(1240, 600, pal, 'SPEC 8.6 · NAMING THE AGENTS',
                 'Oxidising and reducing agents in Cl₂ + KBr',
                 body, tag='oxidising agent: electron acceptor · reducing agent: electron donor',
                 footer='The oxidising agent (Cl₂) is itself reduced; the reducing agent (Br⁻) is itself oxidised.',
                 fkey='READ IT OFF')

# ---------------------------------------------------------- 3. disproportionation ----
def build_disproportionation(pal):
    W, H = 540, 430
    inner = ''
    y0 = 110
    # equation: 2NaOH + Cl2 -> NaOCl + NaCl + H2O
    items = [('2NaOH', 'var(--ink)'), ('+', None), ('Cl₂', 'var(--ink)'), ('→', None),
             ('NaOCl', 'var(--acc)'), ('+', None), ('NaCl', 'var(--cool)'), ('+', None), ('H₂O', 'var(--ink)')]
    x = 60
    for lb, col in items:
        if col is None:
            inner += text(x + 10, y0, lb, 17, 'var(--muted)', 500)
            x += 34
        else:
            inner += text(x + 24, y0, lb, 19, col, 700)
            x += 72
    # oxidation numbers
    cl2_x = 60 + 34 + 72 + 24
    naocl_x = 60 + 34 + 72 + 34 + 72 + 34 + 24
    nacl_x = naocl_x + 72 + 34 + 24
    inner += text(cl2_x, y0 + 26, '0', 12.5, 'var(--muted)', 600, family='GeistMono')
    inner += text(naocl_x, y0 + 26, '+1', 12.5, 'var(--acc)', 700, family='GeistMono')
    inner += text(nacl_x, y0 + 26, '−1', 12.5, 'var(--cool)', 700, family='GeistMono')
    # oxidation arrow (0 -> +1)
    inner += ('<path d="M %d %d Q %d %d %d %d" fill="none" stroke="var(--acc)" stroke-width="2.2" marker-end="url(#arwacc)"/>'
              % (cl2_x + 6, y0 + 52, (cl2_x + naocl_x) / 2 + 8, y0 + 108, naocl_x - 4, y0 + 52))
    inner += text((cl2_x + naocl_x) / 2 + 14, y0 + 124, 'oxidation  0 → +1', 13, 'var(--acc)', 600, family='GeistMono')
    # reduction arrow (0 -> -1), routed below the oxidation arc so they never cross
    inner += ('<path d="M %d %d Q %d %d %d %d" fill="none" stroke="var(--cool)" stroke-width="2.2" marker-end="url(#arw)"/>'
              % (cl2_x + 2, y0 + 58, (cl2_x + nacl_x) / 2 - 6, y0 + 208, nacl_x - 2, y0 + 46))
    inner += text((cl2_x + nacl_x) / 2, y0 + 232, 'reduction  0 → −1', 13, 'var(--cool)', 600, family='GeistMono')
    inner += text(270, y0 + 262, 'cold, dilute aqueous NaOH', 12.5, 'var(--muted)', 500)
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 6px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner)))
    return shell(1280, 610, pal, 'SPEC 8.7 · DISPROPORTIONATION',
                 'Chlorine in cold dilute sodium hydroxide',
                 body, tag='one element · one species · both ways',
                 footer='Both chlorine atoms start at 0 inside Cl₂. One climbs to +1 (sodium chlorate(I)), '
                        'the other falls to −1 (sodium chloride). Oxidised and reduced simultaneously.',
                 fkey='THE TEST')

# ---------------------------------------------------------- 4. Group 1/2 trends ----
def build_group12_trends(pal):
    def ladder(entries, ie_head, tag, color):
        inner = ''
        x0, y0, step = 92, 96, 62
        for i, (name, cfg, ie) in enumerate(entries):
            y = y0 + i * step
            inner += text(x0 - 30, y, name, 15, 'var(--ink)', 600, anchor='end')
            inner += text(x0 - 30, y + 18, cfg, 11, 'var(--muted)', 500, anchor='end', family='GeistMono')
            r = 7 + i * 1.6
            inner += '<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="%.2f" stroke="%s" stroke-width="1.6"/>' % (x0, y, r, color, .25, color)
            inner += text(x0 + 148, y, ie, 13, 'var(--body)', 600, anchor='end', family='GeistMono')
        inner += text(x0 + 148, y0 - 34, ie_head, 11, 'var(--muted)', 600, anchor='end', family='GeistMono')
        # down arrows
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--acc)" stroke-width="2" marker-end="url(#arwacc)"/>'
                  % (x0 + 40, y0 - 16, x0 + 40, y0 + len(entries) * step - 26))
        inner += text(x0 + 58, y0 + len(entries) * step / 2 + 4, 'radius ↑  reactivity ↑', 12, 'var(--acc)', 600, family='GeistMono')
        inner += text(x0 + 58, y0 + len(entries) * step / 2 + 24, 'IE ↓', 12, 'var(--acc)', 600, family='GeistMono')
        return inner

    g1 = ladder([('Li', '[He]2s¹', '519'), ('Na', '[Ne]3s¹', '494'), ('K', '[Ar]4s¹', '418'),
                 ('Rb', '[Kr]5s¹', '402'), ('Cs', '[Xe]6s¹', '376')],
                '1st IE / kJ mol⁻¹', 'Group 1', 'var(--acc)')
    g2 = ladder([('Be', '[He]2s²', '900'), ('Mg', '[Ne]3s²', '738'), ('Ca', '[Ar]4s²', '590'),
                 ('Sr', '[Kr]5s²', '550'), ('Ba', '[Xe]6s²', '503')],
                '1st IE / kJ mol⁻¹', 'Group 2', 'var(--cool)')

    def card(name, tag, art, sub):
        return ('<div class="card"><div class="ct"><span class="name">%s</span><span class="sig">%s</span></div>'
                '<div class="art">%s</div><div class="sub">%s</div></div>' % (name, tag, art, sub))

    W, H = 470, 400
    body = ('<style>%s</style><div class="duo">%s%s</div>'
            % (CARD_CSS,
               card('Group 1 — the alkali metals', 'ns¹', svg(W, H, g1),
                    'One outer s-electron, held ever more weakly: radius and reactivity rise, ionisation energy falls.'),
               card('Group 2 — the alkaline-earth metals', 'ns²', svg(W, H, g2),
                    'Two outer s-electrons and a higher 1st IE at every step — still falling, still easing down the group.')))
    return shell(1360, 640, pal, 'SPEC 8.11 · 8.12 · WHY REACTIVITY RISES',
                 'Down Groups 1 and 2: the outer electron escapes more easily',
                 body, tag='IE ↓ ⇒ cation formation easier',
                 footer='More shells → greater distance + greater shielding → weaker hold on the outer electron → lower '
                        'ionisation energy → the cation forms more readily → more reactive. Group 1 is ahead of Group 2 at every step.',
                 fkey='THE CHAIN')

# ---------------------------------------------------------- 5. Group 2 solubility ----
def build_group2_solubility(pal):
    W, H = 540, 400
    def build_inner():
        inner = ''
        names = ['Be', 'Mg', 'Ca', 'Sr', 'Ba']
        hyd = ['insoluble', 'sparingly soluble', 'slightly soluble', 'quite soluble', 'very soluble']
        sul = ['very soluble', 'quite soluble', 'slightly soluble', 'sparingly soluble', 'insoluble']
        x0, y0, step = 150, 110, 52
        inner += text(52, y0 - 42, 'M(OH)₂', 13, 'var(--ink)', 700)
        inner += text(248, y0 - 42, 'MSO₄', 13, 'var(--ink)', 700)
        for i, n in enumerate(names):
            y = y0 + i * step
            inner += text(x0 - 52, y + 5, n, 15, 'var(--ink)', 600, anchor='end')
            inner += text(x0 + 34, y + 5, hyd[i], 12, 'var(--body)', 500, anchor='start')
            inner += text(x0 + 172, y + 5, sul[i], 12, 'var(--body)', 500, anchor='start')
            inner += line(x0 - 40, y + 14, x0 + 118, y + 14, w=1, color='var(--faint)')
            inner += line(x0 + 158, y + 14, x0 + 296, y + 14, w=1, color='var(--faint)')
        # hydroxide up arrow
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--acc)" stroke-width="2.2" marker-end="url(#arwacc)"/>'
                  % (x0 - 72, y0 + 4 * step + 4, x0 - 72, y0 - 22))
        inner += text(x0 - 88, y0 + 4 * step + 26, 'hydroxides:', 11.5, 'var(--acc)', 700, family='GeistMono')
        inner += text(x0 - 88, y0 + 4 * step + 44, 'more soluble ↓ group', 11.5, 'var(--acc)', 600, family='GeistMono')
        # sulfate down arrow
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--cool)" stroke-width="2.2" marker-end="url(#arw)"/>'
                  % (x0 + 208, y0 - 22, x0 + 208, y0 + 4 * step + 4))
        inner += text(x0 + 188, y0 + 4 * step + 26, 'sulfates:', 11.5, 'var(--cool)', 700, family='GeistMono')
        inner += text(x0 + 162, y0 + 4 * step + 44, 'less soluble ↓ group', 11.5, 'var(--cool)', 600, family='GeistMono')
        return inner
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 4px 0">%s</div></div>' % (CARD_CSS, svg(W, H, build_inner())))
    return shell(1280, 600, pal, 'SPEC 8.15 · TWO OPPOSING LADDERS',
                 'Solubility of Group 2 hydroxides vs sulfates',
                 body, tag='know both directions',
                 footer='Hydroxides dissolve more readily down the group (Mg(OH)₂ suspension → Ba(OH)₂ strong alkali); '
                        'sulfates dissolve less (MgSO₄ soluble → BaSO₄ insoluble — the basis of the sulfate test).',
                 fkey='THE LADDERS')
