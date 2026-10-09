#!/usr/bin/env python3
"""Topic 4 v2 — plate: free-radical substitution mechanism (chlorination of methane)."""
from common import shell, svg, text, line, wavy, fishhook

def initiation_svg():
    inner = ''
    inner += text(20, 24, 'UV light', size=11, color='var(--acc)', weight=600,
                  family='GeistMono', anchor='start', spacing=0.8)
    inner += wavy(18, 38, 156, 80, color='var(--acc)', w=2.2, waves=4)
    # Cl—Cl
    inner += text(194, 112, 'Cl', size=28, weight=600)
    inner += line(213, 102, 265, 102, w=2.8)
    inner += text(283, 112, 'Cl', size=28, weight=600)
    # fish-hooks from the bond centre, one electron to each atom
    inner += fishhook(237, 96, 204, 62, 191, 56, side=1, w=2.3)
    inner += fishhook(241, 96, 274, 62, 287, 56, side=-1, w=2.3)
    # products
    prod = ('<text x="360" y="112" style="font-family:Geist;font-size:28px;font-weight:600;'
            'fill:var(--ink)">Cl<tspan fill="var(--acc)">•</tspan>'
            '<tspan dx="12">+</tspan><tspan dx="12">Cl</tspan>'
            '<tspan fill="var(--acc)">•</tspan></text>')
    inner += prod
    # note
    inner += text(556, 88, 'homolytic fission:', size=13, color='var(--muted)', weight=500,
                  anchor='start')
    inner += text(556, 110, 'one electron to each atom', size=13, color='var(--muted)',
                  weight=500, anchor='start')
    return svg(860, 175, inner)

def loop_svg():
    inner = ('<path d="M30,24 C132,14 132,142 38,134" fill="none" stroke="var(--acc)" '
             'stroke-width="2" marker-end="url(#arwacc)"/>')
    inner += text(112, 68, 'radical used', size=10.5, color='var(--muted)', weight=600,
                  family='GeistMono', anchor='start', spacing=0.3)
    inner += text(112, 86, 'and regenerated', size=10.5, color='var(--muted)', weight=600,
                  family='GeistMono', anchor='start', spacing=0.3)
    inner += text(112, 112, 'the chain continues', size=10.5, color='var(--acc)', weight=600,
                  family='GeistMono', anchor='start', spacing=0.3)
    return svg(240, 160, inner)

def build_mech(pal):
    css = """
.mx-wrap{display:flex;flex-direction:column;gap:13px;flex:1;margin-top:16px;min-height:0}
.mx-card{flex:1;border:1px solid var(--hair);border-radius:16px;background:var(--card);
  display:grid;grid-template-columns:170px 1fr;gap:18px;padding:16px 22px;align-items:center}
.rail{display:flex;flex-direction:column;align-items:flex-start;gap:7px}
.num{width:30px;height:30px;border-radius:50%;border:1.5px solid var(--accmid);color:var(--acc);
  font-family:'GeistMono',monospace;font-weight:600;font-size:13px;display:flex;
  align-items:center;justify-content:center}
.rn{font-weight:600;font-size:15.5px;color:var(--ink);letter-spacing:-.01em}
.rs{font-family:'GeistMono',monospace;font-size:9.5px;font-weight:500;color:var(--muted);
  letter-spacing:.13em;text-transform:uppercase}
.mx-row{display:flex;align-items:center;gap:16px}
.step{font-family:'GeistMono',monospace;font-size:9.5px;font-weight:600;color:var(--acc);
  letter-spacing:.13em;border:1px solid var(--accmid);border-radius:6px;padding:3px 7px;
  background:var(--accsoft)}
.eq{font-size:19px;font-weight:600;color:var(--ink);white-space:nowrap}
.eq2{font-size:16.5px;font-weight:600;color:var(--ink);white-space:nowrap}
.mx-prop{display:grid;grid-template-columns:1fr 250px;align-items:center;gap:10px}
.mx-prop .stack{display:flex;flex-direction:column;gap:18px}
.tm-grid{display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:8px;align-items:center}
.tm-grid .eq2{justify-self:center}
.tm-note{grid-column:1 / -1;text-align:center;color:var(--muted);font-size:12.5px;margin-top:2px}
.tm-ev{grid-column:1 / -1;display:flex;justify-content:center;margin-top:10px}
.tm-ev .chip{white-space:nowrap}
.init-wrap{display:flex;align-items:center;justify-content:center;width:100%}
"""
    init = ('<div class="mx-card"><div class="rail"><div class="num">1</div>'
            '<div class="rn">Initiation</div><div class="rs">radicals made</div></div>'
            '<div class="init-wrap">%s</div></div>' % initiation_svg())
    prop = ('<div class="mx-card"><div class="rail"><div class="num">2</div>'
            '<div class="rn">Propagation</div><div class="rs">chain carries</div></div>'
            '<div class="mx-prop"><div class="stack">'
            '<div class="mx-row"><span class="step">STEP 1</span>'
            '<span class="eq">Cl<span class="rd">•</span> + CH<sub>4</sub> &nbsp;→&nbsp; '
            '<span class="rd">•</span>CH<sub>3</sub> + HCl</span></div>'
            '<div class="mx-row"><span class="step">STEP 2</span>'
            '<span class="eq"><span class="rd">•</span>CH<sub>3</sub> + Cl<sub>2</sub> '
            '&nbsp;→&nbsp; CH<sub>3</sub>Cl + Cl<span class="rd">•</span></span></div>'
            '</div>%s</div></div>' % loop_svg())
    term = ('<div class="mx-card"><div class="rail"><div class="num">3</div>'
            '<div class="rn">Termination</div><div class="rs">chain ends</div></div>'
            '<div><div class="tm-grid">'
            '<div class="eq2">Cl<span class="rd">•</span> + Cl<span class="rd">•</span> '
            '&nbsp;→&nbsp; Cl<sub>2</sub></div>'
            '<div class="eq2"><span class="rd">•</span>CH<sub>3</sub> + Cl<span class="rd">•</span> '
            '&nbsp;→&nbsp; CH<sub>3</sub>Cl</div>'
            '<div class="eq2"><span class="rd">•</span>CH<sub>3</sub> + <span class="rd">•</span>'
            'CH<sub>3</sub> &nbsp;→&nbsp; C<sub>2</sub>H<sub>6</sub></div>'
            '<div class="tm-note">any two radicals can collide and combine — each pairing ends a chain</div>'
            '<div class="tm-ev"><span class="chip acc">ethane = evidence for '
            '<span class="rd">•</span>CH<sub>3</sub></span></div>'
            '</div></div></div>')
    body = ('<style>%s</style><div class="mx-wrap">%s%s%s</div>' % (css, init, prop, term))
    return shell(1216, 896, pal, 'SPEC 4.18 · FREE-RADICAL SUBSTITUTION',
                 'Chlorination of methane — the chain reaction', body,
                 tag='CH<sub>4</sub> + Cl<sub>2</sub> → CH<sub>3</sub>Cl + HCl · UV',
                 footer='Half-headed fish-hook arrows move <b>one electron</b>; full curly arrows '
                        'move a <b>pair</b> — and the dot always sits on the atom carrying the '
                        'unpaired electron.', fkey='CONVENTION')

MECH = ('mechanism-radical-substitution', 1216, 896, build_mech)
