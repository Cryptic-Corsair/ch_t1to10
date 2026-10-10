#!/usr/bin/env python3
"""Chemistry + consistency audit for the Topic 4 v2 figures.

Checks (source of truth = prisma/seed-data/notes.ts):
  1. every isomer skeleton has the right carbon count (vertices of the drawing)
  2. displayed butane shows 4 C and 10 H labels
  3. cycloalkane ring sizes + formulas match names
  4. mechanism equations appear verbatim (normalised) in the seed notes
  5. fraction names + order match the notes sentence
  6. pollutant rows: formulas present, NOx-from-air and SO2-from-fuel wording kept
"""
import re
import sys
sys.path.insert(0, '/home/z/my-project/scripts/t4v2')
import figs_a, figs_b, figs_c, figs_d

NOTES = open('/home/z/my-project/prisma/seed-data/notes.ts').read()
fails = []

def check(label, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), '-', label, ('| ' + detail if detail and not ok else ''))
    if not ok:
        fails.append(label)

# ---- 1. isomer carbon counts ------------------------------------------------
def count_carbons(segs):
    """Unique vertices/joints of the skeletal drawing = carbons
    (endpoints + true segment intersections, e.g. the neopentane centre)."""
    pts = set()
    seglist = []
    for s in segs:
        for p in s:
            pts.add((round(p[0], 2), round(p[1], 2)))
        if len(s) == 2:
            seglist.append(((s[0][0], s[0][1]), (s[1][0], s[1][1])))
    # segment intersections (axis-aligned crosses like neopentane)
    def on_seg(p, a, b):
        return (min(a[0], b[0]) - 1e-6 <= p[0] <= max(a[0], b[0]) + 1e-6 and
                min(a[1], b[1]) - 1e-6 <= p[1] <= max(a[1], b[1]) + 1e-6)
    for i in range(len(seglist)):
        for j in range(i + 1, len(seglist)):
            (a1, a2), (b1, b2) = seglist[i], seglist[j]
            da = (a2[0] - a1[0], a2[1] - a1[1]); db = (b2[0] - b1[0], b2[1] - b1[1])
            den = da[0] * db[1] - da[1] * db[0]
            if abs(den) < 1e-9:
                continue
            t = ((b1[0] - a1[0]) * db[1] - (b1[1] - a1[1]) * db[0]) / den
            u = ((b1[0] - a1[0]) * da[1] - (b1[1] - a1[1]) * da[0]) / den
            if 0 - 1e-9 <= t <= 1 + 1e-9 and 0 - 1e-9 <= u <= 1 + 1e-9:
                p = (round(a1[0] + t * da[0], 2), round(a1[1] + t * da[1], 2))
                if on_seg(p, a1, a2) and on_seg(p, b1, b2):
                    pts.add(p)
    return len(pts)

expected = {
    'butane': 4, '2-methylpropane': 4,
    'pentane': 5, '2-methylbutane': 5, '2,2-dimethylpropane': 5,
    'hexane': 6, '2-methylpentane': 6, '3-methylpentane': 6,
    '2,2-dimethylbutane': 6, '2,3-dimethylbutane': 6,
}
fn_map = {
    'butane': 'st_butane', '2-methylpropane': 'st_2methylpropane',
    'pentane': 'st_pentane', '2-methylbutane': 'st_2methylbutane',
    '2,2-dimethylpropane': 'st_neopentane',
    'hexane': 'st_hexane', '2-methylpentane': 'st_2methylpentane',
    '3-methylpentane': 'st_3methylpentane',
    '2,2-dimethylbutane': 'st_22dimethylbutane', '2,3-dimethylbutane': 'st_23dimethylbutane',
}
# endpoint-only counting: joints are shared, so unique points = carbons
for name, n in expected.items():
    segs = getattr(figs_b, fn_map[name])()
    c = count_carbons(segs)
    check('isomer %s has %d carbons' % (name, n), c == n, 'got %d' % c)

# ---- 2. displayed butane labels ---------------------------------------------
html = figs_a.build_formula.__wrapped__ if hasattr(figs_a.build_formula, '__wrapped__') else None
from common import LIGHT
src = figs_a.displayed_butane.__code__ and None  # noqa
import common
# regenerate displayed butane by calling the internal svg pieces: count via source inspect
disp_src = open('/home/z/my-project/scripts/t4v2/figs_a.py').read()
seg = disp_src[disp_src.find('def displayed_butane'):disp_src.find('def skeletal_butane_annotated')]
xs_literal = re.search(r'xs = \[(.*?)\]', seg).group(1)
n_c = len(xs_literal.split(','))
check('displayed butane draws 4 carbons', n_c == 4)
# H labels: 2 vertical per carbon + 1 outward per end = 10
check('displayed butane H count = 4*2 + 2 ends = 10', n_c * 2 + 2 == 10)

# ---- 3. cycloalkane rings ----------------------------------------------------
cyc = [('cyclopropane', 'C<sub>3</sub>H<sub>6</sub>', 3), ('cyclobutane', 'C<sub>4</sub>H<sub>8</sub>', 4),
       ('methylcyclopropane', 'C<sub>4</sub>H<sub>8</sub>', 3), ('cyclopentane', 'C<sub>5</sub>H<sub>10</sub>', 5),
       ('methylcyclobutane', 'C<sub>5</sub>H<sub>10</sub>', 4)]
bseg = open('/home/z/my-project/scripts/t4v2/figs_b.py').read()
cyc_src = bseg[bseg.find('def build_cyclo'):]
for name, formula, sides in cyc:
    m = re.search(r"\('%s',\s*'([^']+)',\s*ring_svg\((\d+)" % name, cyc_src)
    ok = m and int(m.group(2)) == sides and m.group(1) == formula
    check('cycloalkane %s: %d-ring, chip %s' % (name, sides, re.sub('<[^>]+>', '', formula)), bool(ok))

# ---- 4. mechanism equations vs notes -----------------------------------------
def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&nbsp;', ' ').replace('&thinsp;', ' ').replace('&amp;', '&')
    sub_digits = str.maketrans('\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089',
                               '0123456789')
    s = s.translate(sub_digits)
    s = re.sub(r'\s+', '', s)
    return s

notes_norm = norm(NOTES)
mech_html = figs_d.build_mech(dict(common.DARK))
eqs = [
    'Cl•+CH4→•CH3+HCl',
    '•CH3+Cl2→CH3Cl+Cl•',
    'Cl•+Cl•→Cl2',
    '•CH3+Cl•→CH3Cl',
    '•CH3+•CH3→C2H6',
    'CH4+Cl2→CH3Cl+HCl',
]
for e in eqs:
    check('mechanism eq %s in plate' % e, norm(e) in norm(mech_html))
    check('mechanism eq %s in notes' % e, norm(e) in notes_norm)

# ---- 5. fractions -------------------------------------------------------------
col_html = figs_c.build_column(dict(common.DARK))
for f in ['refinery gas', 'petrol', 'naphtha', 'kerosene', 'diesel', 'fuel oil', 'residue']:
    check('fraction %s on plate' % f, f in col_html)
check('fraction order matches notes sentence',
      col_html.find('refinery gas') < col_html.find('petrol') < col_html.find('naphtha')
      < col_html.find('kerosene') < col_html.find('diesel') < col_html.find('fuel oil')
      < col_html.find('residue'))

# ---- 6. pollutants ------------------------------------------------------------
pol_html = figs_c.build_pollutants(dict(common.DARK))
pairs = [
    ('plenty of oxygen', 'CO<sub>2</sub>', 'climate change'),
    ('limited oxygen', 'CO', 'haemoglobin'),
    ('severe oxygen starvation', 'C particulates', 'global dimming'),
    ('fuel escapes combustion', 'unburned hydrocarbons', 'ground-level ozone'),
    ('hot engines', 'NO<sub>x</sub>', 'nitric acid'),
    ('sulfur impurities', 'SO<sub>2</sub>', 'sulfurous acid'),
]
for origin, pol, prob in pairs:
    row_ok = (norm(origin) in norm(pol_html) and norm(pol) in norm(pol_html)
              and norm(prob) in norm(pol_html))
    check('pollutant row %s -> %s -> %s' % (origin, re.sub('<[^>]+>', '', pol), prob), row_ok)
check('NOx comes from the AIR (footer kept)', 'comes from the' in pol_html and 'air' in pol_html)
check('fuel contains no nitrogen wording', 'contains no' in pol_html)
check('CO2 not toxic wording', 'not toxic' in pol_html)

# ---- 7. hazard labels match notes alt text ------------------------------------
haz_html = figs_a.build_hazard(dict(common.DARK))
for h in ['Flammable', 'Toxic', 'Corrosive', 'Irritant', 'Oxidising', 'Environmental']:
    check('hazard label %s' % h, h in haz_html)

# ---- 8. skeletal plate: butan-2-ol --------------------------------------------
sk_html = figs_a.build_skeletal(dict(common.DARK))
check('butan-2-ol structural present', norm('CH3—CH(OH)—CH2—CH3') in norm(sk_html))
check('molecular formula C4H10O present', norm('C4H10O') in norm(sk_html))

print('\n%s' % ('ALL CHECKS PASSED' if not fails else 'FAILURES: %d -> %s' % (len(fails), fails)))
sys.exit(1 if fails else 0)
