#!/usr/bin/env python3
"""Verify the Topic 9B (Equilibria, 9.9-9.11) build against upload/Equibria.docx (1).pdf.

Iron rules: verbatim to source (documented typo normalizations only), no unnecessary
terminology, nothing outside the syllabus, zero mistakes (machine-balanced equations).
"""
import re
import sys
from pathlib import Path

ROOT = Path('/home/z/my-project')
notes = (ROOT / 'prisma/seed-data/notes.ts').read_text()
topics = (ROOT / 'prisma/seed-data/topics.ts').read_text()
spec = (ROOT / 'scripts/spec_full.txt').read_text()

ok, fail = 0, 0


def check(name, cond, detail=''):
    global ok, fail
    if cond:
        ok += 1
        print('  PASS %s' % name)
    else:
        fail += 1
        print('  FAIL %s %s' % (name, detail))


tstart = topics.index("slug: 'kinetics-and-equilibria'")
tend = topics.index("slug: 'halogenoalkanes-alcohols-spectra'")
tspan = topics[tstart:tend]

nstart = notes.index("'kinetics-and-equilibria': {")
nspan = notes[nstart:]
nspan = nspan[:nspan.index("\n}\n") + 1] if "\n}\n" in nspan else nspan
_b = nspan.index("'reversible-dynamic-equilibrium': [")
nspan9b = nspan[_b:]
nplain = nspan9b.replace('**', '')
nplain_full = nspan.replace('**', '')  # includes the 9.0 specification map

# ------------------------------------------------------------- structure ----
print('== structure ==')
for key in ['reversible-dynamic-equilibrium', 'conditions-equilibrium-position',
            'reversible-reactions-industry']:
    check('sectionKey %s' % key, ("sectionKey: '%s'" % key) in tspan)
for num in ('9.9', '9.10', '9.11'):
    check('spec %s registered' % num, ("spec: '%s'" % num) in tspan)
for key in ['reversible-dynamic-equilibrium', 'conditions-equilibrium-position',
            'reversible-reactions-industry']:
    check('notes entry %s' % key, ("'%s': [" % key) in nspan)
check('topic summary completed (no "next part")', 'next part' not in tspan)
check('topic summary mentions Haber and Contact', 'Haber and Contact processes' in tspan)
check('9.0 outline covers 9.1 - 9.11', 'Every statement 9.1 – 9.11 has its own section below' in tspan)

print('== spec text fidelity (verbatim vs official spec) ==')
spec_statements = {
    '9.9': 'know that many reactions are readily reversible and that they can reach a state of dynamic equilibrium in which:\ni   the rate of the forward reaction is equal to the rate of the backward reaction\nii   the concentrations of the reactants and the products remain constant',
    '9.10': 'be able to predict and justify the qualitative effects of changes of temperature, pressure and concentration on the position of equilibrium in a homogeneous system',
    '9.11': 'evaluate data to explain the necessity, for many industrial processes, to reach a compromise between the yield and the rate of reaction',
}


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\\n', ' ')).strip().lower()


spec_n = norm(spec)
for num, st in spec_statements.items():
    check('spec %s in official spec' % num, norm(st) in spec_n)
    ts_literal = st.replace('\n', '\\n')
    check('spec %s verbatim in topics.ts' % num, ts_literal in tspan)
    check('spec %s verbatim in notes.ts map row' % num, ts_literal in nspan)

print('== verbatim source anchors (Equibria.docx (1).pdf) ==')
anchors = [
    # 9B-1 reversible reactions and dynamic equilibrium (p2-4)
    'When a mixture of hydrogen and oxygen in a 2:1 ratio is ignited with a spark, water is produced and no uncombined hydrogen and oxygen is left',
    'This is an example of a complete or irreversible reaction',
    'But many reactions do not go to completion',
    'only about 90% of hydrogen and iodine reacts',
    'A reversible reaction is one that goes in both directions at the same temperature.',
    'The symbol ⇌ is used to indicate reactions that are reversible.',
    'Many reactions go to completion if they are performed in an open container.',
    'would completely decompose into CaO(s) and CO₂(g) on heating at 900 °C in an open container',
    'only a small portion of CaCO₃ decomposes, no matter how long the temperature was maintained at 900 °C.',
    'The reason for this is that the products CaO and CO₂ can also react together at this temperature to form the reactants CaCO₃',
    'known as the forward reaction',
    'the reverse (backward) reaction',
    'the concentration of the reactants decreases and the rate of the forward reaction also decreases',
    'proceeds in the forward direction because no products are yet present',
    'the products formed react together to re-form the reactants',
    'Since the concentration of the product is initially low, the rate of the backward reaction is also slow',
    'Eventually the rates of the forward reaction and backward reaction become equal. At this point a dynamic equilibrium has been reached.',
    'Two conditions must be met for dynamic equilibrium to be established;',
    'The reaction must be reversible.',
    'The reaction mixture must be in a closed container.',
    'Three important features of a system in dynamic equilibrium:',
    'The reactions continue to occur in both directions.',
    'The concentration of the reactants and products remain constant.',
    'Rate of the forward reaction is equal to the rate of the backward reaction.',
    # 9B-2 conditions and equilibrium composition (p5-13)
    'all reactants and products are in the same physical state (e.g. all gases or all liquids)',
    'All reactants and products in gaseous state.',
    'All reactants and products in liquid state.',
    'all reactants and products are in different physical states',
    'All reactants and products in solid and aqueous state.',
    'the concentration of each component will not alter as long as the conditions remain constant',
    'adding more of or removing one of the reactants or products',
    'changing the position of equilibrium',
    'reaction between chromate(VI), CrO₄²⁻ ions with acid turns orange',
    'an increase of dichromate(VI) ions, Cr₂O₇²⁻',
    'If acid (H⁺) is added to the system, equilibrium moves to the right and solution becomes orange.',
    'If alkali (OH⁻) is added to the system, equilibrium moves to the left and solution becomes yellow.',
    'Concentration of component.',
    'Pressure of the system.',
    'Temperature of the system.',
    'Addition of a catalyst.',
    'Increasing concentration of reactants drives the forward reaction. Therefore, the equilibrium shifts to the right.',
    'Increasing concentration of products drives the backward reaction. Therefore, the equilibrium shifts to the left.',
    'the rate of backward reaction increases and a new equilibrium is established',
    'with slightly more products than at the original position of equilibrium',
    'Effect of pressure only applies to equilibrium reactions involving gases.',
    'changes of pressure have no effect on the composition of equilibrium mixture',
    'the total number of moles of gas on the reactant side is different from that on the product side',
    'the number of moles of a gas is proportional to the pressure',
    'the side with fewer number of gas molecules, so that the total pressure is decreased',
    'reducing the volume, or adding more gas into the same volume',
    'the side with greater number of gas molecules, so that the total pressure is increased',
    'Position of equilibrium moves to restore equilibrium.',
    'Moves to side with fewer gaseous molecules',
    'Moves to side with more gaseous molecules',
    'Consider the reaction between nitrogen and hydrogen to form ammonia',
    'At high pressure more ammonia is produced at equilibrium',
    'high pressure shifts equilibrium to the side having fewer moles of gas',
    'The direction of change in equilibrium position depends upon whether the reaction is exothermic or endothermic.',
    'shifts towards the endothermic direction',
    'shifts towards the exothermic direction',
    'Position of equilibrium moves to establish a new equilibrium.',
    'Moves to LEFT',
    'Moves to RIGHT',
    'A catalyst works by providing an alternative route that has lower activation energy than that of uncatalysed reaction.',
    'rate of a reaction with a catalyst is much faster than the rate without the catalyst',
    'A catalyst has NO EFFECT on the position of equilibrium of a reversible reaction.',
    'Catalyst speeds up the forward and backward reactions equally, so equilibrium is reached sooner than without catalyst.',
    'The qualitative predictions made about the effect of concentration, pressure and temperature on the position of equilibrium are just predictions',
    'The arguments are not explanations of why changes sometimes occur.',
    'impossible to predict the direction of change or indeed when predictions turn out to be incorrect',
    'the equilibrium mixture of NO₂(g) (brown) and N₂O₄(g) (colourless) in a closed container is placed into a beaker of hot water',
    'both the temperature and the pressure of the gaseous mixture will rise',
    'Forward reaction is exothermic so we would predict an increase in temperature would shift equilibrium to the left',
    'an increase in pressure would shift the equilibrium to the right',
    'We do not know which effect is greater, so we cannot make a prediction of which way equilibrium will shift.',
    'the temperature effect must be greater than the pressure effect',
    'The equilibrium must have shifted to the left to produce more NO₂(g).',
    # 9B-3 reversible reactions in industry (p14-16)
    'The principles of reaction rates and reversibility are important in the design and conditions of many industrial processes.',
    'To maximize profits, it is important to convert reactants to products',
    'as quickly as possible and (2) as completely as possible.',
    'The first one relates to the kinetics (rate of reaction) and the second is related to reversibility.',
    'The solution to the problem is a careful choice of reaction conditions.',
    'The best conditions in an industry are known as compromise conditions.',
    'Ammonia is manufactured in industry by direct synthesis from nitrogen and hydrogen.',
    'maximum yield is obtained by low temperature (forward reaction is exothermic) and high pressure',
    '4 mol of gas on the left; 2 mol of gas on the right',
    'the reaction mixture does not reach equilibrium in the reaction chamber',
    'The graph shows the equilibrium yield of ammonia at different temperatures and pressures.',
    'Why are conditions of 450 °C and 250 atm used?',
    'very strong nitrogen to nitrogen triple bond [E(N≡N) = 945 kJ mol⁻¹]',
    'producing a high activation energy for the reaction',
    'Even at high temperature the reaction is slow in the absence of a suitable catalyst.',
    'Many metals including tungsten and platinum catalyse this reaction',
    'so iron is used in the industrial process',
    'Catalysts require high temperatures to function efficiently',
    'high temperatures are not economical because of the extra energy costs involved',
    'a decrease in yield as the forward reaction is exothermic',
    'leading to an increase in the rate of backward reaction',
    'not in equilibrium because the products are removed from the system as they are formed',
    'Hence a compromised temperature of 450 °C is used.',
    'The higher the pressure the larger is the yield',
    'the larger costs for compressing gases makes the process less economical',
    'a pressure of 250 atm is used',
    'Conditions used in the Haber process are;',
    'Sulphuric acid is manufactured by the Contact process.',
    'Since forward reaction is exothermic, low temperature would result in a high yield of SO₃(g).',
    'The catalyst vanadium(V) oxide requires high temperature to be effective',
    'a moderately high temperature of 450 °C and 1 atm pressure is used',
    'the yield is already very high at 97%',
    'Higher pressures would increase the yield as there are fewer molecules on the right hand side',
    'Pressures above 2 atm are unnecessary since the yield is already very high.',
    'The mechanism of action of the vanadium(V) oxide is different from iron in the Haber process',
    'The vanadium changes its oxidation state during the reaction but converts back to its original oxidation state',
    'The mechanism for the reaction is',
    'Conditions used in the Contact process are;',
    # spec-map additions (live in the 9.0 map, checked against the whole topic span)
    'chlorine reacting with iodine to form iodine(I) chloride, which then reacts with chlorine to form iodine(III) chloride',
    'the equilibrium system between nitrogen dioxide (NO₂) and dinitrogen tetroxide (N₂O₄)',
]
for a in anchors:
    check('anchor: %s…' % a[:58], a in nplain or a in nplain_full)

print('== equations present verbatim ==')
eqs = [
    '2H₂(g)  +  O₂(g)    →    2H₂O(l)',
    'H₂(g)  +  I₂(g)    ⇌    2HI(g)',
    'CaCO₃(s)    →    CaO(s)    +    CO₂(g)',
    'CaCO₃(s)    ⇌    CaO(s)    +    CO₂(g)',
    'A  +  B    →',
    'A  +  B    ⇌    C  +  D',
    '2SO₂(g)  +  O₂(g)    ⇌    2SO₃(g)',
    'CH₃COOH(l)  +  CH₃CH₂OH(l)    ⇌    CH₃COOCH₂CH₃(l)  +  H₂O(l)',
    'H₂O(g)  +  C(s)    ⇌    H₂(g)  +  CO(g)',
    'Cu(s)  +  2Ag⁺(aq)    ⇌    Cu²⁺(aq)  +  2Ag(s)',
    'N₂(g)  +  3H₂(g)    ⇌    2NH₃(g)',
    'N₂(g)  +  3H₂(g)    ⇌    2NH₃(g)    ΔH = −92.4 kJ mol⁻¹',
    'SO₂(g)  +  ½O₂(g)    ⇌    SO₃(g)    ΔH = −96 kJ mol⁻¹',
    '2NO₂(g)    ⇌    N₂O₄(g)    ΔH = −57.2 kJ mol⁻¹',
    'Reactants    ⇌    Products',
    'SO₂(g)  +  V₂O₅(s)    ⇌    SO₃(g)  +  V₂O₄(s)',
    'V₂O₄(s)  +  ½O₂(g)    ⇌    V₂O₅(s)',
    'Forward reaction: ΔH = −ve · Backward reaction: ΔH = +ve',
    '2 moles ⇌ 2 moles',
    '3 moles ⇌ 2 moles',
    '4 moles ⇌ 2 moles',
]
for e in eqs:
    check('eq: %s' % e[:52], e in nspan9b)

print('== machine balance check ==')
SUBS = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}
SUPD = {'⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4, '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9}


def parse_side(side):
    """Parse one side of an equation into a {element: count} dict + total charge."""
    import collections
    counts = collections.Counter()
    charge = 0.0
    # split into species on '+' that is not part of a charge
    species = re.split(r'\s*\+\s*', side.strip())
    for sp in species:
        sp = sp.strip()
        if not sp:
            continue
        # strip state symbols
        sp = re.sub(r'\((s|g|l|aq)\)', '', sp)
        # coefficient: leading regular digits or 1/2 or ½
        m = re.match(r'^([0-9]+/[0-9]+|½|[0-9]+\.?[0-9]*)\s*', sp)
        coeff = 1.0
        if m:
            tok = m.group(1)
            if tok == '½':
                coeff = 0.5
            elif '/' in tok:
                num, den = tok.split('/')
                coeff = float(num) / float(den)
            else:
                coeff = float(tok)
            sp = sp[m.end():]
        # walk the formula
        i = 0
        while i < len(sp):
            ch = sp[i]
            if ch in SUPD or ch in '⁺⁻':
                # charge marker(s)
                j = i
                mag = 1
                sign = 0
                while j < len(sp) and (sp[j] in SUPD or sp[j] in '⁺⁻'):
                    if sp[j] in SUPD:
                        mag = SUPD[sp[j]]
                    elif sp[j] == '⁺':
                        sign = 1
                    else:
                        sign = -1
                    j += 1
                if sign:
                    charge += coeff * mag * sign
                i = j
                continue
            if ch.isupper():
                elem = ch
                i += 1
                while i < len(sp) and sp[i].islower():
                    elem += sp[i]
                    i += 1
                num = ''
                while i < len(sp) and (sp[i] in SUBS or '0' <= sp[i] <= '9'):
                    num += SUBS.get(sp[i], sp[i])
                    i += 1
                counts[elem] += coeff * (float(num) if num else 1.0)
                continue
            i += 1  # skip anything else (·, spaces, etc.)
    return counts, charge


def balance_check(name, eq):
    m = re.match(r'^(.*?)\s{2,}(?:⇌|→|—Fe²⁺\(aq\)→)\s{2,}(.*)$', eq)
    if not m:
        m = re.match(r'^(.*?)(?:⇌|→)(.*)$', eq)
    left, right = m.group(1), m.group(2)
    lc, lq = parse_side(left)
    rc, rq = parse_side(right)
    check('balanced: %s' % name, lc == rc and abs(lq - rq) < 1e-9,
          'left %s q=%s | right %s q=%s' % (dict(lc), lq, dict(rc), rq))


balance_check('water formation', '2H₂ + O₂ → 2H₂O')
balance_check('HI equilibrium', 'H₂ + I₂ ⇌ 2HI')
balance_check('calcium carbonate decomposition', 'CaCO₃ → CaO + CO₂')
balance_check('contact process (doubled)', '2SO₂ + O₂ ⇌ 2SO₃')
balance_check('esterification (completed with H₂O)', 'CH₃COOH + CH₃CH₂OH ⇌ CH₃COOCH₂CH₃ + H₂O')
balance_check('water gas shift', 'H₂O + C ⇌ H₂ + CO')
balance_check('silver displacement (balanced)', 'Cu + 2Ag⁺ ⇌ Cu²⁺ + 2Ag')
balance_check('haber', 'N₂ + 3H₂ ⇌ 2NH₃')
balance_check('contact process (halved)', 'SO₂ + ½O₂ ⇌ SO₃')
balance_check('NO₂ dimerisation', '2NO₂ ⇌ N₂O₄')
balance_check('V₂O₅ step 1', 'SO₂ + V₂O₅ ⇌ SO₃ + V₂O₄')
balance_check('V₂O₅ step 2', 'V₂O₄ + ½O₂ ⇌ V₂O₅')
balance_check('chromate-dichromate (figure plate)', '2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O')

check('chromate equation rendered inside figure plate',
      '2CrO\u2084\u00b2\u207b(aq)  +  2H\u207a(aq)' in (ROOT / 'scripts/t9b/html/eq-chromate-dichromate-light.html').read_text())

print('== structure & honesty ==')
check('exactly one callout (the source key-point box)', nspan9b.count("type: 'callout'") == 1,
      'found %d' % nspan9b.count("type: 'callout'"))
check('callout text verbatim', 'Catalyst speeds up the forward and backward reactions equally, '
      'so equilibrium is reached sooner than without catalyst.' in nspan9b)
check('no worked blocks in 9B', "type: 'worked'" not in nspan9b)
check('three Summary tables', nspan9b.count("text: '**Summary**'") == 3)
check('concentration summary table present', "'Concentration change', 'Effect on equilibrium'" in nspan9b)
check('pressure summary table present', "'Pressure change', 'Effect on equilibrium'" in nspan9b)
check('temperature summary table present', "'Type of forward reaction', 'ΔH', 'Increase temperature', 'Decrease temperature'" in nspan9b)
check('haber conditions table', "['450 °C', '250 atm']" in nspan9b)
check('contact conditions table', "['450 °C', '2 atm']" in nspan9b)
for b in ['CHECKPOINT', 'EXERCISE', 'Kc', 'Le Chatelier', 'next part', 'Checkpoint']:
    check('absent from 9B: %r' % b, b not in nspan9b)
check('absent from 9B: standalone exam mention', re.search(r'\bexam\b', nspan9b) is None)

print('== figures wired ==')
srcs = re.findall(r"src: '(/diagrams/eq-[^']+)'", nspan9b)
check('6 9B figures referenced', len(srcs) == 6, 'found %d' % len(srcs))
for s in srcs:
    p = ROOT / ('public' + s)
    check('exists %s' % Path(s).name, p.exists())
    d = p.with_name(p.stem + '-dark.png')
    check('exists %s' % d.name, d.exists())

print()
print('RESULT: %d passed, %d failed' % (ok, fail))
sys.exit(1 if fail else 0)
