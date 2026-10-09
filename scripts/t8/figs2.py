#!/usr/bin/env python3
"""Topic 8 plates, set B: thermal stability, flame origins, titration, displacement grid, halide ladder."""
import math
from common import shell, svg, text, line, polyline

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
.eqrow{display:flex;justify-content:center;gap:26px;margin-top:10px;font-family:'GeistMono',monospace;
  font-size:13px;color:var(--body);flex-wrap:wrap}
.eqrow b{color:var(--ink);font-weight:600}
"""

# ---------------------------------------------------------- 6. thermal stability ----
def build_thermal_stability(pal):
    def anion(cx, cy, distort):
        """Carbonate ion: central C, three O; distorted = electron cloud pulled toward cation side."""
        inner = ''
        # distortion halo
        off = -distort * 26
        inner += ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="var(--accsoft)" opacity="%.2f"/>'
                  % (cx + off, cy, 108 - distort * 6, 62, .9))
        # C
        inner += '<circle cx="%.1f" cy="%.1f" r="10" fill="var(--ink)"/>' % (cx, cy)
        inner += text(cx, cy + 4, 'C', 10.5, 'var(--diafill)', 700)
        # three O around
        import math as m
        for k, ang in enumerate((150, 30, 262)):
            ox = cx + 64 * m.cos(m.radians(ang)) - distort * 18
            oy = cy - 56 * m.sin(m.radians(ang))
            inner += '<circle cx="%.1f" cy="%.1f" r="12" fill="var(--card2)" stroke="var(--ink)" stroke-width="1.8"/>' % (ox, oy)
            inner += text(ox, oy + 4, 'O', 10.5, 'var(--ink)', 700)
        inner += text(cx, cy + 84, 'CO₃²⁻', 12.5, 'var(--muted)', 600, family='GeistMono')
        return inner

    def cation(cx, cy, r, label, color):
        inner = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2.2"/>' % (cx, cy, r, color, color)
        inner += text(cx, cy + 4.5, label, 11.5, 'var(--diafill)' if color in ('var(--acc)', 'var(--cool)') else 'var(--ink)', 700)
        return inner

    def panel(title, tag, cx_cat, r, clabel, color, distort, sub):
        art = ''
        ax, ay = 235, 168
        art += cation(cx_cat, ay, r, clabel, color)
        art += anion(ax + 118, ay, distort)
        art += ('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="var(--acc)" stroke-width="1.8" marker-end="url(#arwacc)"/>'
                % (cx_cat + r + 4, ay - 8, (cx_cat + r + ax + 60) / 2, ay - 64, ax + 52, ay - 26))
        art += text((cx_cat + ax + 90) / 2, ay - 78, 'polarises', 12, 'var(--acc)', 600, family='GeistMono')
        return ('<div class="card"><div class="ct"><span class="name">%s</span><span class="sig">%s</span></div>'
                '<div class="art" style="padding-top:6px">%s</div><div class="sub">%s</div></div>'
                % (title, tag, svg(470, 296, art), sub))

    body = ('<style>%s</style><div class="duo">%s%s</div>'
            % (CARD_CSS,
               panel('Be²⁺ — small +2: polarises most', 'least stable end', 66, 17, 'Be²⁺', 'var(--acc)', 1.0,
                     'The tiny, doubly charged cation drags the anion\'s cloud hard — O–C bonds weaken and CO₂ breaks away easily.'),
               panel('Cs⁺ — large +1: polarises least', 'most stable end', 60, 30, 'Cs⁺', 'var(--cool)', 0.12,
                     'The large, singly charged cation barely distorts the anion — its nitrates and carbonates survive a Bunsen flame.')))
    return shell(1360, 600, pal, 'SPEC 8.16 · POLARISING POWER',
                 'Cation size and charge set the thermal stability',
                 body, tag='stability ↑ down group · ↓ across to Group 2',
                 footer='Small, highly charged cations distort the big nitrate/carbonate anions, weakening the bonds inside '
                        'them and easing decomposition. Stability increases down each group and falls from Group 1 to Group 2 — '
                        'with Li⁺ behaving like the Group 2 end and Be²⁺ the extreme.',
                 fkey='THE MECHANISM')

# ---------------------------------------------------------- 7. flame origins ----
def build_flame_origins(pal):
    def levels():
        inner = ''
        x0, w = 96, 210
        # excited states
        for i, y in enumerate((52, 74, 96)):
            inner += line(x0, y, x0 + w - i * 26, y, w=3, color='var(--ink)')
        inner += text(x0 + w + 14, 78, 'excited states', 11.5, 'var(--muted)', 500)
        # ground state cluster
        for y in (238, 252, 266):
            inner += line(x0, y, x0 + w, y, w=3, color='var(--ink)')
        inner += text(x0 + w + 14, 256, 'ground state', 11.5, 'var(--muted)', 500)
        # excitation up
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--acc)" stroke-width="2.2" marker-end="url(#arwacc)"/>'
                  % (x0 + 62, 230, x0 + 62, 104))
        inner += text(x0 + 46, 172, 'excitation', 12, 'var(--acc)', 600, anchor='end', family='GeistMono')
        inner += text(x0 + 46, 190, '(heat)', 12, 'var(--acc)', 600, anchor='end', family='GeistMono')
        # emission down
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--cool)" stroke-width="2.2" marker-end="url(#arw)"/>'
                  % (x0 + 150, 100, x0 + 150, 232))
        inner += text(x0 + 162, 172, 'photon emitted', 12, 'var(--cool)', 600, anchor='start', family='GeistMono')
        inner += text(x0 + 150, 300, 'colour = the energy gap ΔE', 12.5, 'var(--body)', 600)
        return inner

    def chart():
        rows = [('Li⁺', 'red', '#c0392b'), ('Na⁺', 'yellow/orange', '#e67e22'),
                ('K⁺', 'lilac', '#9b7fc0'), ('Ca²⁺', '(brick) red', '#b0522d'),
                ('Sr²⁺', '(crimson) red', '#a02c3f'), ('Ba²⁺', '(apple) green', '#5d8a3a')]
        inner = ''
        x0, y0, step = 76, 42, 40
        for i, (ion, name, col) in enumerate(rows):
            y = y0 + i * step
            inner += text(x0 - 18, y + 5, ion, 13, 'var(--ink)', 700, anchor='end', family='GeistMono')
            inner += ('<rect x="%d" y="%d" width="86" height="18" rx="6" fill="%s" opacity=".85"/>' % (x0, y - 9, col))
            inner += text(x0 + 104, y + 5, name, 12.5, 'var(--body)', 500)
        inner += text(x0 + 6, y0 + 6 * step + 16, 'Be²⁺ and Mg²⁺: no colour (ΔE emits in the UV)', 11.5, 'var(--muted)', 500)
        return inner

    W, H = 400, 340
    body = ('<style>%s</style><div class="duo">'
            '<div class="card"><div class="ct"><span class="name">Origin of the colour</span><span class="sig">8.17</span></div>'
            '<div class="art">%s</div></div>'
            '<div class="card"><div class="ct"><span class="name">Flame colours to know</span><span class="sig">CHART</span></div>'
            '<div class="art">%s</div></div></div>'
            % (CARD_CSS, svg(W, H, levels()), svg(360, 320, chart())))
    return shell(1360, 600, pal, 'SPEC 8.17 · ELECTRON TRANSITIONS',
                 'Excitation, relaxation, emission — the flame test',
                 body, tag='each cation has its own ΔE fingerprint',
                 footer='Heat promotes cation electrons to higher levels; they fall back and emit light whose frequency '
                        'matches the gap. Bigger gaps emit bluer light; Be²⁺ and Mg²⁺ gaps are so large their emission is ultraviolet.',
                 fkey='PHYSICS')

# ---------------------------------------------------------- 8. titration setup ----
def build_titration_setup(pal):
    W, H = 560, 470
    inner = ''
    # stand: base + pole + clamp arm
    inner += line(46, 440, 250, 440, w=5, color='var(--ink)')
    inner += line(70, 440, 70, 70, w=5, color='var(--ink)')
    inner += line(70, 100, 206, 100, w=4, color='var(--ink)')
    inner += ('<rect x="200" y="92" width="12" height="20" rx="3" fill="var(--ink)"/>')
    # burette
    bx = 212
    inner += ('<rect x="%d" y="56" width="26" height="252" rx="7" fill="var(--card2)" stroke="var(--ink)" stroke-width="2.2"/>' % bx)
    for i in range(9):
        y = 74 + i * 27
        inner += line(bx + 4, y, bx + (12 if i % 2 else 8), y, w=1.4, color='var(--muted)')
    # stopcock + jet
    inner += ('<rect x="%d" y="308" width="44" height="11" rx="4" fill="var(--muted)"/>' % (bx - 9))
    inner += ('<rect x="%d" y="319" width="9" height="18" rx="2" fill="var(--muted)"/>' % (bx + 8.5))
    inner += line(bx + 13, 337, bx + 13, 348, w=2.2, color='var(--acc)')
    # labels (anchored start, right of the burette)
    inner += text(bx + 44, 70, 'burette \u2014 50 cm\u00b3', 12.5, 'var(--ink)', 600, anchor='start')
    inner += text(bx + 44, 88, 'read to 0.05 cm\u00b3', 11, 'var(--muted)', 500, anchor='start', family='GeistMono')
    inner += text(bx + 46, 318, 'stopcock', 11.5, 'var(--muted)', 500, anchor='start')
    # conical flask under the jet: outline + liquid band
    fx = bx + 13
    inner += ('<path d="M %d 354 L %d 378 L %d 424 L %d 424 L %d 378 L %d 354 Z" fill="none" '
              'stroke="var(--ink)" stroke-width="2.2" stroke-linejoin="round"/>'
              % (fx - 15, fx - 15, fx - 66, fx + 66, fx + 15, fx + 15))
    inner += ('<path d="M %d 404 L %d 424 L %d 424 L %d 404 Z" fill="var(--coolsoft)"/>'
              % (fx - 47, fx - 66, fx + 66, fx + 47))
    inner += text(fx, 419, '25.0 cm\u00b3 + indicator', 10, 'var(--cool)', 600, family='GeistMono')
    # white tile
    inner += ('<rect x="%d" y="436" width="160" height="9" rx="2" fill="var(--card2)" stroke="var(--hair)"/>' % (fx - 80))
    inner += text(fx, 460, 'white tile', 11.5, 'var(--muted)', 500)
    # meniscus card
    inner += ('<rect x="384" y="170" width="180" height="150" rx="12" fill="var(--card)" stroke="var(--hair)"/>')
    inner += text(474, 196, 'read the meniscus', 12.5, 'var(--ink)', 600)
    inner += ('<rect x="424" y="216" width="100" height="70" rx="6" fill="var(--coolsoft)" opacity=".5"/>')
    inner += ('<path d="M 424 236 Q 474 248 524 236" fill="none" stroke="var(--cool)" stroke-width="2.2"/>')
    inner += line(410, 236, 538, 236, w=1.2, color='var(--acc)')
    inner += text(474, 266, 'bottom, at eye level', 11, 'var(--body)', 500)
    inner += text(474, 284, 'against the mark', 11, 'var(--body)', 500)
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 8px 0">%s</div></div>' % (CARD_CSS, svg(W, H, inner)))
    return shell(1300, 620, pal, 'SPEC 8.20 \u00b7 8.21 \u00b7 8.23 \u00b7 VOLUMETRIC ANALYSIS',
                 'The titration bench \u2014 burette, pipette, conical flask',
                 body, tag='n = cV \u00b7 concordant within 0.20 cm\u00b3',
                 footer='Standard solution in one vessel, unknown in the other; end point when the indicator just changes. '
                        'Mean titre from concordant titres only, then c = n/V \u2014 with uncertainties counted (burette read twice).',
                 fkey='THE BENCH')

# ---------------------------------------------------------- 9. displacement grid ----
def build_displacement_grid(pal):
    W, H = 640, 430
    inner = ''
    cols = ['Cl⁻', 'Br⁻', 'I⁻']
    rows = ['Cl₂', 'Br₂', 'I₂']
    cells = [[None, ('Br₂', '#8a4a1f', 'aq'), ('I₂', '#5d4a8a', 'aq')],
             [None, None, ('I₂', '#5d4a8a', 'aq')],
             [None, None, None]]
    x0, y0, cw, ch = 150, 92, 150, 84
    for j, c in enumerate(cols):
        inner += text(x0 + cw / 2 + j * cw, y0 - 18, c, 15, 'var(--ink)', 700)
    for i, r in enumerate(rows):
        inner += text(x0 - 24, y0 + ch / 2 + 6 + i * ch, r, 15, 'var(--ink)', 700, anchor='end', family='GeistMono')
    for i in range(4):
        inner += line(x0, y0 + i * ch, x0 + 3 * cw, y0 + i * ch, w=1.2, color='var(--hair)')
    for j in range(4):
        inner += line(x0 + j * cw, y0, x0 + j * cw, y0 + 3 * ch, w=1.2, color='var(--hair)')
    import math as m
    for i in range(3):
        for j in range(3):
            cx = x0 + j * cw + cw / 2
            cy = y0 + i * ch + ch / 2
            cell = cells[i][j]
            if cell:
                nm, col, tag = cell
                inner += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="9" fill="%s" opacity=".22"/>'
                          % (x0 + j * cw + 8, y0 + i * ch + 8, cw - 16, ch - 16, col))
                inner += ('<circle cx="%.1f" cy="%.1f" r="11" fill="%s" opacity=".85"/>' % (cx, cy - 12, col))
                inner += text(cx, cy + 16, nm + ' formed', 12, 'var(--ink)', 600)
                inner += text(cx, cy + 32, 'displaces ' + cols[j], 10.5, 'var(--muted)', 500, family='GeistMono')
            else:
                inner += text(cx, cy + 5, 'no reaction', 12, 'var(--muted)', 500)
    inner += text(x0 + 3 * cw / 2, y0 + 3 * ch + 34, 'halogen must sit ABOVE the halide to displace it', 12, 'var(--muted)', 500)
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 8px 0">%s</div>'
            '<div class="eqrow"><b>Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂</b><b>Cl₂ + 2I⁻ → 2Cl⁻ + I₂</b><b>Br₂ + 2I⁻ → 2Br⁻ + I₂</b></div>'
            '</div>' % (CARD_CSS, svg(W, H, inner)))
    return shell(1380, 640, pal, 'SPEC 8.25 · DISPLACEMENT = OXIDISING POWER',
                 'Cl₂, Br₂ and I₂ against aqueous halide ions',
                 body, tag='iodine: violet in cyclohexane',
                 footer='A more reactive halogen oxidises the ions of any halogen below it and is itself reduced '
                        '(0 → −1) while the halide is oxidised (−1 → 0). Colours are sharpest in the cyclohexane layer.',
                 fkey='THE GRID')

# ---------------------------------------------------------- 10. halide power ladder ----
def build_halide_ladder(pal):
    W, H = 470, 400
    def build_inner():
        inner = ''
        x1, x2, y0, step = 130, 340, 70, 62
        # 5 rungs, matching the source table: fluorine -> astatine
        items = [('F₂ / F⁻', 'strongest oxidising agent', 'no significant reducing properties'),
                 ('Cl₂ / Cl⁻', '', ''),
                 ('Br₂ / Br⁻', '', ''),
                 ('I₂ / I⁻', '', ''),
                 ('At₂ / At⁻', 'weakest oxidising agent', 'strongest reducing power')]
        n = len(items) - 1
        for i, (pair, top_note, bot_note) in enumerate(items):
            y = y0 + i * step
            inner += text(x1, y, pair.split(' / ')[0], 16, 'var(--ink)', 700)
            inner += text(x2, y, pair.split(' / ')[1], 16, 'var(--ink)', 700)
            if i < n:
                inner += line(x1 - 40, y + 12, x1 - 40, y + step - 10, w=1, color='var(--faint)')
                inner += line(x2 + 40, y + 12, x2 + 40, y + step - 10, w=1, color='var(--faint)')
        # arrows point toward the strongest species
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--cool)" stroke-width="2.4" marker-end="url(#arw)"/>'
                  % (x1 - 66, y0 + n * step + 8, x1 - 66, y0 - 8))
        inner += text(x1 - 80, y0 - 26, 'oxidising power increases ↑', 12, 'var(--cool)', 700, family='GeistMono')
        inner += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--acc)" stroke-width="2.4" marker-end="url(#arwacc)"/>'
                  % (x2 + 66, y0 - 8, x2 + 66, y0 + n * step + 8))
        inner += text(x2 + 30, y0 - 26, 'reducing power increases ↓', 12, 'var(--acc)', 700, family='GeistMono')
        inner += text((x1 + x2) / 2, y0 - 44, 'top of the group', 11, 'var(--muted)', 500, family='GeistMono')
        inner += text((x1 + x2) / 2, y0 + n * step + 40, 'down the group: more shells, more shielding, outer electrons lost more easily', 11.5, 'var(--muted)', 500)
        return inner
    body = ('<style>%s</style><div class="card" style="margin-top:20px;flex:1">'
            '<div class="art" style="padding:2px 8px 0">%s</div></div>' % (CARD_CSS, svg(W, H, build_inner())))
    return shell(1300, 580, pal, 'SPEC 8.25 · 8.27(i) · TWO MIRROR LADDERS',
                 'Oxidising power of halogens vs reducing power of halides',
                 body, tag='oxidising power rises towards F₂ · reducing power rises towards At⁻',
                 footer='With concentrated H₂SO₄ the ladder shows itself: Cl⁻ stops at HCl fumes, Br⁻ adds Br₂ + SO₂, '
                        'I⁻ drives the acid down to SO₂, S and even H₂S — while F⁻ has no significant reducing power at all.',
                 fkey='ONE TREND, TWO SIGNS')
