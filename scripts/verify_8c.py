# -*- coding: utf-8 -*-
"""Verify Topic 8C rebuild: verbatim source anchors, forbidden invented phrases,
equation balance, block types, figures, blurbs. Zero-tolerance checks."""
import re
import sys
from pathlib import Path

ROOT = Path('/home/z/my-project')
notes = (ROOT / 'prisma/seed-data/notes.ts').read_text(encoding='utf-8')
topics = (ROOT / 'prisma/seed-data/topics.ts').read_text(encoding='utf-8')

fails = []
def check(cond, msg):
    if cond:
        print('PASS  %s' % msg)
    else:
        fails.append(msg)
        print('FAIL  %s' % msg)

# ---------------------------------------------------------------- region
start = notes.index("    'group7-trends': [")
# stop at the next topic entry (Topic 9) so its blocks are not counted in the 8C region
_end_marks = []
for m in ("  'kinetics-and-equilibria': {",):
    if m in notes[start:]:
        _end_marks.append(notes.index(m, start))
region = notes[start:_end_marks[0]] if _end_marks else notes[start:]
KEYS = ['group7-trends', 'halogen-displacement', 'chlorine-reactions',
        'halide-reactions', 'halogen-predictions']
for k in KEYS:
    check("    '%s': [" % k in region, 'section present: %s' % k)
order = [region.index("    '%s': [" % k) for k in KEYS]
check(order == sorted(order), 'sections in spec order 8.24 -> 8.28')

# ---------------------------------------------------------------- verbatim anchors
ANCHORS = [
    # 8.24 (source p2-3)
    'known as **halogens**', 'salt producing', 'ns² np⁵',
    'diatomic molecules** (F₂, Cl₂, Br₂ and I₂)',
    'Pale yellow', 'Green', 'Red-brown', 'Shiny greyish black',
    'State (at RTP)', 'very pale yellow', 'In hydrocarbon solvents', 'Violet',
    'brown vapour', 'sublimation', 'Br₂(l) → Br₂(g)', 'I₂(s) → I₂(g)',
    'Atomic radius **increases** down the Group 7', '0.064', '0.099', '0.111', '0.128',
    'Melting and boiling temperatures **increase** down the group',
    'instantaneous dipole-induced dipole attraction',
    'more energy is required to overcome the forces between molecules',
    'attract the shared pair of electrons in a covalent bond',
    'The electronegativity of fluorine is the highest of all elements',
    'shielding of the nucleus by the inner shell electrons',
    'Melting temperature / °C', 'Boiling temperature / °C',
    '−220', '−188', '−101', '−35', '114', '184', '302', '337', '2.2',
    'F₂ is most reactive and I₂ is least reactive',
    '**Electron affinity** also decreases down the group',
    # 8.25 (source p5-6)
    'need an electron to complete their outer shell',
    'accept electrons and get reduced',
    'The oxidizing power of the halogen **decreases** as we move down the group from F to I',
    'F₂  >  Cl₂  >  Br₂  >  I₂',
    'As the size of the atoms increases down a group, **shielding increases**',
    'hence their oxidising power decreases',
    '**Chlorine** will displace **bromide and iodide** ions from solution',
    '**Bromine** will displace **iodide** ions from solution, but not chloride ions',
    '**Iodine** cannot displace either bromide or chloride ions from solution',
    'Appearance of aqueous solution', 'Appearance of cyclohexane',
    'Very pale green', 'Reddish brown', 'Pale brown', 'Violet',
    'Cl₂(aq)  +  2Br⁻(aq)  →  2Cl⁻(aq)  +  Br₂(aq)',
    'Cl₂(aq)  +  2I⁻(aq)  →  2Cl⁻(aq)  +  I₂(aq)',
    'Br₂(aq)  +  2I⁻(aq)  →  2Br⁻(aq)  +  I₂(aq)',
    # 8.26 (source p5, p7)
    'Metals react with halogens on heating to form **halides** or white ionic salts',
    'caesium (or francium) and fluorine',
    'beryllium and iodine (or astatine)',
    'the halogen acts as an **oxidizing agent**',
    '**decreases from 0 to −1**', '**increases from 0 to +1 or +2**',
    '2M + X₂ → 2MX', 'M + X₂ → MX₂',
    '2Li  +  Cl₂  →  2LiCl', '2Na  +  Br₂  →  2NaBr',
    'Mg  +  Cl₂  →  MgCl₂', 'Ca  +  Cl₂  →  CaCl₂', 'Sr  +  Br₂  →  SrBr₂',
    'both oxidation and reduction at the same time',
    'chlorine water', 'hydrochloric acid', 'chloric(I) acid', 'hypochlorous acid',
    'Cl₂  +  H₂O  →  HCl  +  HClO',
    'mild oxidising agent', 'killing bacteria', 'sterilize the water',
    'swimming pools', 'water treatment',
    'COLD dilute aqueous sodium hydroxide',
    'sodium chlorate(I)', 'sodium hypochlorite',
    '2NaOH(aq)  +  Cl₂(g)  →  NaCl(aq)  +  NaOCl(aq)  +  H₂O(l)',
    'active ingredient in household bleach',
    'HOT concentrated sodium hydroxide', 'sodium chlorate(V)',
    '6NaOH(aq)  +  3Cl₂(aq)  →  5NaCl(aq)  +  NaClO₃(aq)  +  3H₂O(l)',
    '+5 state', 'weed killer', 'react in similar ways',
    # 8.27 (source p9-12)
    '**reducing agents**, as they can lose electrons and get oxidized',
    'Reducing power of halide ions **increases down the group**',
    '**Iodide ions are the most reducing**, followed by bromide ions',
    'no significant reducing properties',
    'the halide ion is **more readily oxidised**',
    'fluorine F₂', 'fluoride F⁻', 'astatine At₂', 'astatide At⁻',
    'sodium halides with concentrated sulfuric acid',
    '**oxidizing agent** and as well as an **acid**',
    'sulfur dioxide', 'hydrogen sulfide',
    'Misty fumes (HCl)', 'Misty fumes (HBr)', 'Misty fumes (HI)',
    'Brown fumes Br₂', 'choking odour (SO₂)',
    'Purple fumes + black ppt (I₂)', 'Yellow ppt (S)',
    'rotten egg smell (H₂S)',
    'solubilities of the silver halides',
    'especially carbonate ions',
    'dilute or concentrated ammonia',
    'White precipitate of AgCl(s)', 'Cream precipitate of AgBr(s)',
    'Yellow precipitate of AgI(s)',
    'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)', 'Ag⁺(aq) + Br⁻(aq) → AgBr(s)',
    'Ag⁺(aq) + I⁻(aq) → AgI(s)',
    'AgCl(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Cl⁻(aq)',
    'AgBr(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Br⁻(aq)',
    'soluble in concentrated ammonia', 'Precipitate insoluble in both',
    'colourless gases', 'polar diatomic molecules',
    'formed when hydrogen reacts with halogens',
    'acidic solutions',
    'hydrofluoric acid', 'hydrochloric acid', 'hydrobromic acid', 'hydroiodic acid',
    'HF + H₂O ⇌ H₃O⁺ + F⁻', 'HCl + H₂O → H₃O⁺ + Cl⁻',
    'HBr + H₂O → H₃O⁺ + Br⁻', 'HI + H₂O → H₃O⁺ + I⁻',
    'white ionic solids', 'HCl(g)  +  NH₃(g)  →  NH₄Cl(s)',
    # 8.28 (source p12 box + data threads)
    'fluorides and astatides', 'hydrogen astatide',
    'based on the equation for hydrogen iodide',
    'HI  +  H₂O  →  H₃O⁺  +  I⁻', 'HAt  +  H₂O  →  H₃O⁺  +  At⁻',
    'melting temperature 302 °C, boiling temperature 337 °C',
]
for a in ANCHORS:
    check(a in region, 'anchor: %s' % a[:64])

# ---------------------------------------------------------------- forbidden inventions
FORBIDDEN = [
    'less greedy', 'steals from', 'book-keeping', 'peroxodisulfate',
    'wearing different clothes', 'whole trick', 'exam favourite', 'exam-trap',
    'methyl orange', 'mirror image', 'NaHSO₄', 'NaOBr', 'bromate(I)', 'KAt',
    'AgAt', 'brown-purple', 'radioactive', '(3.13)', '(7.1)', '(8.12)',
    'acid–base only', '8.10 taught', 'prediction template',
    'One ladder, three probes', 'classic observation', 'Extrapolate',
    'Heavier, duller', 'redox evidence', 'never seen', 'in exam format',
    'manganate', 'displaces chloride', 'displaces neither', 'three probes',
    'weathered', 'the periodic table lets you',
]
for f in FORBIDDEN:
    check(f not in region, 'forbidden absent: %s' % f)
# no section cross-references like (8.24) inside the rebuilt text
check(re.search(r'\(8\.\d', region) is None, 'no spec cross-references in 8C text')

# ---------------------------------------------------------------- equation balance
SUB = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}
def normalize(eq):
    out = []
    for ch in eq:
        if ch in SUB:
            out.append(SUB[ch])
        elif ch in '⁺':
            out.append('+')
        elif ch in '⁻':
            out.append('-')
        else:
            out.append(ch)
    s = ''.join(out)
    s = re.sub(r'\s+', ' ', s)
    return s

def parse_term(term):
    term = term.strip()
    charge = 0
    m = re.search(r'(\d*)([+-])$', term)
    if m:
        charge = int(m.group(1) or 1) * (1 if m.group(2) == '+' else -1)
        term = term[:m.start()]
    coef = 1
    m = re.match(r'^(\d+)', term)
    if m:
        coef = int(m.group(1)); term = term[m.end():]

    def parse_simple(s):
        d = {}
        for m2 in re.finditer(r'([A-Z][a-z]?)(\d*)', s):
            if m2.group(1):
                d[m2.group(1)] = d.get(m2.group(1), 0) + int(m2.group(2) or 1)
        return d

    def expand(s):
        # resolve innermost bracket groups repeatedly: (NH3)2, [AgN2H6] etc.
        pattern = re.compile(r'[\[\(]([^()\[\]]+)[\]\)](\d*)')
        while True:
            m2 = pattern.search(s)
            if not m2:
                return s
            mult = int(m2.group(2) or 1)
            repl = ''.join('%s%d' % (el, n * mult) for el, n in parse_simple(m2.group(1)).items())
            s = s[:m2.start()] + repl + s[m2.end():]

    flat = expand(term)
    counts = parse_simple(flat)
    return counts, charge, coef

EQUATIONS = [
    'Cl₂ + H₂O → HCl + HClO',
    '2NaOH(aq) + Cl₂(g) → NaCl(aq) + NaOCl(aq) + H₂O(l)',
    '6NaOH(aq) + 3Cl₂(aq) → 5NaCl(aq) + NaClO₃(aq) + 3H₂O(l)',
    '2Li + Cl₂ → 2LiCl', '2Na + Br₂ → 2NaBr', 'Mg + Cl₂ → MgCl₂',
    'Ca + Cl₂ → CaCl₂', 'Sr + Br₂ → SrBr₂',
    'Cl₂(aq) + 2Br⁻(aq) → 2Cl⁻(aq) + Br₂(aq)',
    'Cl₂(aq) + 2I⁻(aq) → 2Cl⁻(aq) + I₂(aq)',
    'Br₂(aq) + 2I⁻(aq) → 2Br⁻(aq) + I₂(aq)',
    'HCl(g) + NH₃(g) → NH₄Cl(s)',
    'HF + H₂O ⇌ H₃O⁺ + F⁻', 'HCl + H₂O → H₃O⁺ + Cl⁻',
    'HBr + H₂O → H₃O⁺ + Br⁻', 'HI + H₂O → H₃O⁺ + I⁻',
    'HAt + H₂O → H₃O⁺ + At⁻',
    'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)', 'Ag⁺(aq) + Br⁻(aq) → AgBr(s)',
    'Ag⁺(aq) + I⁻(aq) → AgI(s)',
    'AgCl(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Cl⁻(aq)',
    'AgBr(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Br⁻(aq)',
]
for eq in EQUATIONS:
    norm = normalize(eq).replace('⇌', '→')
    lhs, rhs = norm.split('→')
    # strip state symbols (aq)/(g)/(l)/(s)
    lhs = re.sub(r'\((aq|g|l|s)\)', '', lhs)
    rhs = re.sub(r'\((aq|g|l|s)\)', '', rhs)
    lt = [parse_term(t) for t in lhs.split(' + ')]
    rt = [parse_term(t) for t in rhs.split(' + ')]
    bal = {}
    ok = True
    for counts, ch, coef in lt:
        for el, n in counts.items():
            bal[el] = bal.get(el, 0) - n * coef
        ok = ok and True
    for counts, ch, coef in rt:
        for el, n in counts.items():
            bal[el] = bal.get(el, 0) + n * coef
    charge_l = sum(ch * coef for _, ch, coef in lt)
    charge_r = sum(ch * coef for _, ch, coef in rt)
    ok = all(v == 0 for v in bal.values()) and charge_l == charge_r
    check(ok, 'balanced: %s  %s' % (eq[:44], '' if ok else str(bal)))

# ---------------------------------------------------------------- block types + counts
ALLOWED = {'p', 'h3', 'def', 'eq', 'list', 'callout', 'worked', 'table', 'figure'}
types = re.findall(r"\{ type: '([a-z3]+)'", region)
bad = [t for t in types if t not in ALLOWED]
check(not bad, 'block types valid (%s)' % (','.join(sorted(set(types)))))
check('worked' not in types and 'callout' not in types,
      'no invented worked/callout blocks in 8C (%d blocks)' % len(types))
check(types.count('table') == 9, '9 tables (got %d)' % types.count('table'))
check(types.count('eq') == 9, '9 eq blocks (got %d)' % types.count('eq'))
check(types.count('figure') == 2, '2 figures (got %d)' % types.count('figure'))
check(types.count('def') == 2, '2 def blocks (got %d)' % types.count('def'))

# ---------------------------------------------------------------- figures on disk
for f in ['displacement-grid.png', 'displacement-grid-dark.png',
          'halide-power-ladder.png', 'halide-power-ladder-dark.png']:
    check((ROOT / 'public/diagrams' / f).exists(), 'figure on disk: %s' % f)

# ---------------------------------------------------------------- blurbs
OLD = ['less greedy', 'steals from', 'redox evidence', 'disproportionation at work',
       'the evidence for the trends', 'you have never seen']
NEW = [
    'The halogens: appearance, changes of state, atomic radius',
    'shown by the displacement reactions with halide ions',
    'disproportionation in terms of oxidation numbers',
    'Halide ions as reducing agents',
    'Predicting reactions of fluorides and astatides',
]
for o in OLD:
    check(o not in topics, 'old blurb gone: %s' % o)
for n in NEW:
    check(n in topics, 'new blurb present: %s' % n[:52])

# ---------------------------------------------------------------- spec text verbatim (source checklist p1)
SPEC = {
    '8.24': 'understand reasons for the trends for Group 7 elements in:',
    '8.25': 'understand the trend in reactivity of Group 7 elements in terms of the redox reactions of Cl₂, Br₂ and I₂ with halide ions in aqueous solution.',
    '8.26': 'understand, in terms of changes in oxidation number, the following reactions of the halogens:',
    '8.27': 'understand the following reactions:',
    '8.28': 'be able to make predictions about fluorine and astatine and their compounds, in terms of knowledge of trends in halogen chemistry',
}
for num, txt in SPEC.items():
    check(txt in topics, 'specText verbatim: %s' % num)

print()
if fails:
    print('%d FAILURES' % len(fails))
    sys.exit(1)
print('ALL CHECKS PASSED')
