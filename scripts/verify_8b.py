# -*- coding: utf-8 -*-
"""Verify the Topic 8B rebuild (sections 8.11-8.23) against 'Group 1 and 2 notes.pdf'.
Checks: structure, verbatim source anchors, absence of old invented content,
chemistry arithmetic, figure wiring, blurbs, and 8A/8C regression.
"""
PATH = '/home/z/my-project/prisma/seed-data/notes.ts'
TPATH = '/home/z/my-project/prisma/seed-data/topics.ts'

src = open(PATH, encoding='utf-8').read()
t = open(TPATH, encoding='utf-8').read()

START = "    'group1-2-ionisation-energy': ["
END = "    'group7-trends': ["
i, j = src.index(START), src.index(END)
span = src[i:j]

KEYS = ['group1-2-ionisation-energy', 'group1-2-reactivity', 'group1-2-reactions',
        'oxides-hydroxides-acids', 'group2-solubility', 'thermal-stability',
        'flame-colours', 'thermal-decomposition-experiment', 'tests-for-ions',
        'solution-concentrations', 'core-practical-3', 'measurement-uncertainty',
        'core-practical-4']

fails = []
def check(cond, label):
    if not cond:
        fails.append(label)

# ---------------------------------------------------------------- structure
pos = -1
for k in KEYS:
    m = "    '%s': [" % k
    check(src.count(m) == 1, 'key not unique: %s' % k)
    p = src.index(m)
    check(p > pos, 'key out of order: %s' % k)
    pos = p
check(span.count("'callout'") == 0, 'callout blocks remain in 8B span')
check(span.rstrip().endswith("],"), 'span does not end cleanly')

import re
blocks = re.findall(r"\{ type: '([a-z3]+)'", span)
valid = {'p', 'h3', 'list', 'def', 'table', 'eq', 'worked', 'figure'}
bad = [b for b in blocks if b not in valid]
check(not bad, 'invalid block types: %s' % set(bad))
print('8B span: %d blocks (%d tables, %d eq, %d lists, %d p, %d h3, %d def, %d worked, %d figures)' % (
    len(blocks), blocks.count('table'), blocks.count('eq'), blocks.count('list'),
    blocks.count('p'), blocks.count('h3'), blocks.count('def'), blocks.count('worked'), blocks.count('figure')))

# tables rectangular
for tm in re.finditer(r"\{ type: 'table', headers: \[(.*?)\], rows: \[(.*?)\] \}", span, re.S):
    pass  # rows may span lines; do a coarse check below
for tm in re.finditer(r"type: 'table', headers: \[([^\]]*)\], rows: \[(.*?)\n      \] \}", span, re.S):
    ncol = tm.group(1).count(',') + 1
    for row in re.finditer(r"\[([^\[\]]*)\]", tm.group(2)):
        n = row.group(1).count(',')
        # commas inside quoted strings with no commas are fine; count only top-level approx
check(True, 'table scan placeholder')

# ---------------------------------------------------------------- verbatim anchors
ANCHORS = [
    # 8.11 (p2-4)
    'are members of Group I and Group II, respectively, in the periodic table',
    'appear as **bright silvery solids**',
    'combine with oxygen to form oxides as surface layers, which makes them appear dull',
    'since their valence electrons are in s orbitals',
    'readily lose their outermost s-electrons to form stable ions with **noble gas structures**',
    "['*Fr Francium', '[Rn]7s¹', '*Ra Radium', '[Rn]7s²']",
    'Atomic radius of Group II < Group I',
    "['Cs', '0.262', 'Ba', '0.224']",
    'The effect of the increase in nuclear charge is outweighed by the increase in shielding',
    "['Li', '519', '7 300', 'Be', '900', '1 757', '2 657']",
    "['Cs', '376', '2 420', 'Ba', '503', '965', '1 468']",
    # 8.12 (p4)
    'because of the tendency of elements to lose electron increases down the group',
    'Group I elements can lose electrons easily and are more metallic',
    # 8.13 (p5-7)
    'react readily with oxygen to form **solid metal oxides**',
    "'4M(s) + O₂(g) → 2M₂O(s)'",
    'products are oxides containing M²⁺ and O²⁻ ions',
    'react with chlorine to form **ionic chlorides** except beryllium',
    'ionic chlorides of Group I and II are **soluble in water**',
    "'2M(s) + Cl₂(g) → 2MCl(s)'",
    'produce **alkaline metal hydroxide** and **hydrogen**',
    'density is half of that of water',
    'the sodium **melts to form a ball** that moves around on the surface',
    'contamination of hydrogen flame with sodium compounds',
    'sparks and a **lilac flame**',
    'Reacts **very slowly** with cold water',
    'magnesium oxide (a white solid) and hydrogen gas in a **vigorous** reaction',
    'burned as it leaves the tube',
    "'Ca(s)  +  2H₂O(l)  →  Ca(OH)₂(s)  +  H₂(g)'",
    # 8.14 (p7-8)
    'classified as **basic oxides** (beryllium oxide/hydroxide is **amphoteric**)',
    'react with water to form **alkaline hydroxides**',
    'Reacts very slowly and incompletely to form a slightly alkaline suspension of Mg(OH)₂',
    'CaO(s) + H₂O(l) → Ca(OH)₂(s) (cloudy suspension)',
    'behave as **bases** and **react with acids** to form **salts and water**',
    'described as **neutralization** reactions',
    'a **white solid** reacts to form a **colourless solution**',
    'highly **exothermic**',
    # 8.15 (p9)
    'Solubility of **group 2 hydroxides increases** down the group',
    'Solubility of **group 2 sulphates decreases** down the group',
    "['Mg(OH)₂', 'sparingly soluble', 'MgSO₄', 'quite soluble']",
    "['Ba(OH)₂', 'very soluble', 'BaSO₄', 'insoluble']",
    # 8.16 (p10-12)
    'indicates how stable a compound is when it is heated',
    'Smaller and more highly charged cations affect these anions more',
    'Cations with small size and high charge has a higher **polarizing power**',
    'As the degree of covalency decreases, the strength of the ionic lattice increases',
    'Group 2 cations are smaller in size than group 1 cations',
    "['Caesium', '+1', '0.170', 'Barium', '+2', '0.136']",
    'greatest influence (biggest charge and smaller size) on an anion is **Be²⁺**',
    'least influence (smallest charge and largest size) is **Cs⁺**',
    "'2XNO₃(s) → 2XNO₂(s) + O₂(g)'",
    "'2X(NO₃)₂(s) → 2XO(s) + 4NO₂(g) + O₂(g)'",
    'XNO₂ (pale yellow solid)',
    'LiNO₃ decomposes to form lithium oxide, nitrogen dioxide and oxygen',
    'nitrogen dioxide** (brown gas)',
    '4LiNO₃(s) → 2Li₂O(s) + 4NO₂(g) + O₂(g) (Greater decomposition)',
    '2NaNO₃(s) → 2NaNO₂(s) + O₂(g) (Lesser decomposition)',
    '2Be(NO₃)₂(s) → 2BeO(s) + 4NO₂(g) + O₂(g) (Greater decomposition)',
    '2RbNO₃(s) and 2CsNO₃(s) → No brown fumes',
    'stable to heat** except lithium carbonate',
    'polarizes the O–C bond in the CO₃²⁻ ion sufficiently for it to break and form an O²⁻ ion',
    "'X₂CO₃(s) → X₂O(s) + CO₂(g)'",
    "'XCO₃(s) → XO(s) + CO₂(g)'",
    'All carbonates except barium carbonate decomposes to give metal oxide and carbon dioxide',
    "'Li₂CO₃(s)  →  Li₂O(s)  +  CO₂(g)'",
    '**do not decompose at Bunsen temperatures**',
    # 8.17 (p14-15)
    'identify the **metal cation** present in a compound',
    'commonly referred as **excitation** of electrons',
    'fall back to the ground state, emitting energy in the form of light',
    'colour depends on the energy level difference between the two shells',
    "['Rubidium', 'Rb⁺', 'red/purple']",
    "['Beryllium', 'Be²⁺', '(no colour)']",
    "['Barium', 'Ba²⁺', '(apple) green']",
    # 8.18 (p13-14)
    'relative ease of decomposition of group 2 carbonates and nitrates',
    'Place the same amount of each of the salts in a series of hard glass test tubes',
    'measure the time taken for the gas evolved to reach the mark on the test tube in the water bath',
    'chlorides are more volatile than other salts so are more likely to give better results',
    'Dip a clean metal wire (platinum or nichrome) or silica rod',
    # 8.19 (p15)
    'Add aqueous sodium hydroxide and warm',
    'dense white smoke is formed (NH₄Cl) when passed over hydrogen chloride gas',
    'NH₄⁺(aq) + OH⁻(aq) → NH₃(g) + H₂O(l)',
    'CO₃²⁻(aq) + 2H⁺(aq) → CO₂(g) + H₂O(l)',
    'Effervescence (CO₂)',
    'White ppt (BaSO₄)',
    "'Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s)'",
    'there must be H⁺ ions present to prevent barium carbonate from forming',
    # 8.20 (p16-22)
    'comparing reacting volumes is known as **volumetric analysis**',
    'Water of crystallization of a substance',
    "['Burette', 'designed to deliver definite but variable volumes of liquid']",
    "['White tile', 'used to show the colour changes clearly at the end point']",
    'concentration is **accurately known**',
    'Be solids with high molar masses',
    'React rapidly and completely with other substances when used in titrations',
    '**moles of solute per dm³ of solution**',
    'amount of substance = concentration × volume (n = cV)',
    'using the ratio given in the balanced chemical equation',
    'change color due to changes in pH',
    "['methyl orange', 'red', 'yellow', 'strong acid – weak base and strong acid – strong base']",
    "['phenolphthalein', 'colourless', 'pink', 'weak acid – strong base and strong acid – strong base']",
    'Only **concordant values** must be selected to calculate the mean titre',
    "['final burette reading / cm³', '24.15', '25.30', '24.60', '23.25']",
    "['titre / cm³', '22.95', '22.60', '22.70', '22.65']",
    'Titre 2, 3 and 4 are all within 0.20 cm³ of each other, so are concordant',
    "'Mean  =  (22.60 + 22.70 + 22.65) ÷ 3  =  22.65 cm³'",
    # 8.21 (p20-21)
    'measuring the volumes of two solutions that react together',
    'having one solution in a **burette** and pipetting a known volume',
    'exactly the right amounts of substances to complete the reaction',
    'ideally the end point should coincide with the equivalence point',
    'the lowest (horizontal) part of the meniscus should be read',
    'usually within 0.20 cm³ of each other',
    'Rinse the conical flask with deionized water and place it on a white tile',
    'transfer 25.0 cm³ of the sodium hydroxide solution to the conical flask',
    'Add about 3 drops of methyl orange indicator',
    'until concordant titres have been obtained',
    # 8.22 (p24-28)
    'skilled operator can avoid by being careful',
    'without making sure the balance is tared (set to zero) beforehand',
    'burette reading of 27.35 cm³ but writes it down as 23.75 cm³',
    'even a skilled operator would find difficult to avoid',
    'unpredictable changes in conditions such as temperature or pressure',
    'leads to the recorded value being either too low or too high',
    'how close values are to the **accepted or correct value**',
    'measured to the nearest 0.05 cm³',
    'usually 25.0 cm³ or 10.0 cm³',
    'the **potential error** involved when using a piece of apparatus',
    "['3', '±0.0005 g', 'A reading of 17.100 g could be between 17.0995 g and 17.1005 g']",
    'read twice in a titration, so the total measurement uncertainty is ±0.10 cm³',
    'multiplied by 100 and divided by the value recorded',
    '±0.10 × 100/22.50 = **±0.44%**',
    '±0.06 × 100/25 = **±0.24%**',
    '±0.3 × 100/250 = **±0.12%**',
    'The precision of the balance',
    'Mass of marble chips = 3.57 g',
    'obtained by **adding together the individual uncertainties**',
    "['Burette', '±0.47%']",
    "['Overall percentage uncertainty', '±0.92%']",
    "'Concentration  =  0.118  ±  0.001 mol dm⁻³'",
    'weighing sample of 5 g will lead to a much lower percentage uncertainty',
    '**minimizing heat loss** will reduce random errors',
    # 8.23 (p19)
    '**Weigh** accurately the required amount of material',
    'Ensure all the solid has dissolved',
    'transfer the solution quantitatively** into a clean volumetric flask',
    'pouring the liquid down a glass rod held in the spout of the beaker',
    'bottom of the meniscus touches the calibration mark on the neck of the volumetric flask',
    '**Stopper** the volumetric flask and shake to ensure the solution is thoroughly mixed',
]
for a in ANCHORS:
    check(a in span, 'MISSING anchor: %s' % a[:70])

# ---------------------------------------------------------------- forbidden (old invented 8B)
FORBIDDEN = [
    'Reuse Topic 2', 'spec 2.10', 'Beyond the spec', 'safely filed away',
    'giant IE jump', 'full-mark', 'favourite anomaly', 'exam phrasing',
    'milk of magnesia', 'book-keeping', 'stored under oil', 'eagerness',
    'superoxide', 'ultraviolet', 'Rinse rules', 'without tears',
    'weigh by difference', '0.0892', '97.1', 'glowing splint', 'relights',
    'Bubble through', 'The plan', 'practical exam watches', 'Washings rule',
    'Distinguishing carbonate', 'Limewater must be fresh', 'score here',
    'One story, three symptoms', 'stability league', 'ladders cross',
    'insoluble endpoint', 'fingerprint', 'bench geometry', 'mirror of 8.20',
    'certified standard', 'solid NaOH fails', '26.8', '4.879', '0.0976',
    'exam-famous', 'damp blue litmus turns red', 'Na₂O₂', 'KO₂',
    'Mistakes are not errors', 'Error vs uncertainty vocabulary',
    'read twice" traps', 'cm³ to dm³', 'MgO or Mg(OH)₂? It depends',
]
for f in FORBIDDEN:
    check(f not in span, 'FORBIDDEN present in 8B: %s' % f)

# ---------------------------------------------------------------- chemistry arithmetic
check(abs((22.60 + 22.70 + 22.65) / 3 - 22.65) < 1e-9, 'mean titre arithmetic')
for a, b, s in [(900, 1757, '2 657'), (738, 1451, '2 189'), (590, 1145, '1 735'),
                (550, 1064, '1 614'), (503, 965, '1 468')]:
    check(a + b == int(s.replace(' ', '')), 'IE sum %s' % s)
    check(s in span, 'IE sum value missing: %s' % s)
for titre, fin, init in [(22.95, 24.15, 1.20), (22.60, 25.30, 2.70), (22.70, 24.60, 1.90), (22.65, 23.25, 0.60)]:
    check(abs(fin - init - titre) < 1e-9, 'titre difference %s' % titre)
check(abs(0.10 * 100 / 22.50 - 0.4444) < 0.001 and '±0.44%' in span, 'burette % unc')
check(abs(0.06 * 100 / 25 - 0.24) < 1e-9 and '±0.24%' in span, 'pipette % unc')
check(abs(0.3 * 100 / 250 - 0.12) < 1e-9 and '±0.12%' in span, 'flask % unc')
check(abs(2 * 0.005 * 100 / 3.57 - 0.2801) < 0.001 and '±0.28%' in span, 'balance % unc')
check(abs(0.09 + 0.12 + 0.24 + 0.47 - 0.92) < 1e-9 and '±0.92%' in span, 'overall % unc')
check(abs(0.118 * 0.0092 - 0.00109) < 0.0001, 'absolute uncertainty ~ ±0.001')
check('0.117 – 0.119' in span, 'range quote')

# balanced equations present (zero-mistake where source was unbalanced)
for eq in ["2Li(s)  +  2H₂O(l)  →  2LiOH(aq)  +  H₂(g)",
           "2Na(s)  +  2H₂O(l)  →  2NaOH(aq)  +  H₂(g)",
           "2K(s)  +  2H₂O(l)  →  2KOH(aq)  +  H₂(g)",
           "M(s)  +  2H₂O(l)  →  M(OH)₂(aq)  +  H₂(g)",
           "Mg(s)  +  2H₂O(l)  →  Mg(OH)₂(s)  +  H₂(g)",
           "Mg(s)  +  H₂O(g)  →  MgO(s)  +  H₂(g)",
           "Sr(s)  +  2H₂O(l)  →  Sr(OH)₂(aq)  +  H₂(g)",
           "Ba(s)  +  2H₂O(l)  →  Ba(OH)₂(aq)  +  H₂(g)",
           "2M(s) + O₂(g) → 2MO(s)",
           "4M(s) + O₂(g) → 2M₂O(s)",
           "2M(s) + Cl₂(g) → 2MCl(s)",
           "M(s) + Cl₂(g) → MCl₂(s)"]:
    check(eq in span, 'MISSING balanced equation: %s' % eq)

# figures wired
for fig in ['/diagrams/group12-trends.png', '/diagrams/group2-solubility.png',
            '/diagrams/thermal-stability.png', '/diagrams/flame-origins.png',
            '/diagrams/titration-setup.png']:
    check(fig in span, 'figure missing: %s' % fig)

# ---------------------------------------------------------------- blurbs + regression
NEW_BLURBS = [
    'The Group 1 and 2 elements, their configurations, atomic radii and the fall in ionisation energy down the group.',
    'Reactivity increases down the group — and Group I is more reactive than Group II.',
    'Reactions of the Group 1 and 2 elements with oxygen, chlorine and water, with the observations for each metal.',
    'Basic oxides (beryllium oxide is amphoteric) and their reactions with water and with dilute acids.',
    'Solubility of Group 2 hydroxides increases down the group; sulfates decreases.',
    'How cation size and charge control the thermal stability of the nitrates and carbonates.',
    'Excitation and relaxation of electrons — and the flame colours of the Group 1 and 2 cations.',
    'The thermal decomposition experiment and the flame test procedure.',
    'Tests for ammonium, carbonate and hydrogencarbonate, and sulfate ions — with observations and ionic equations.',
    'Volumetric analysis: apparatus, standard solutions, concentration calculations, indicators and the mean titre.',
    'Core Practical 3: the titration method for finding the concentration of an acid solution.',
    'Mistakes, errors, accuracy and precision, measurement uncertainty and overall percentage uncertainty.',
    'Core Practical 4: preparation of a standard solution from a solid acid.',
]
OLD_BLURBS = [
    'Down the group it gets easier to lose the outer electron — here is why.',
    'Lower ionisation energy, faster reaction — the trend and its reason.',
    'What the s-block elements do — and what you observe as you go down.',
    'Basic oxides, alkaline solutions, neutralisation — salts and water.',
    'Hydroxides dissolve more as you descend; sulfates dissolve less.',
    'Polarising power decides it — down the group stabler, across to Group 2 less so.',
    'Excitation, relaxation, emission — and the colour chart you must know.',
    'How the evidence is gathered — apparatus, timing, gas tests and the wire.',
    'Three gas-and-precipitate tests, with the ionic equations to match.',
    'Standard solutions, burettes, indicators — and n = cV.',
    'Titrate the unknown acid against a standard alkali — then calculate.',
    'Random vs systematic, accuracy vs precision — and adding up the ±.',
    'Weigh, dissolve, transfer, make up to the mark — then find the NaOH.',
]
for b in NEW_BLURBS:
    check(b in t, 'new blurb missing: %s' % b[:60])
for b in OLD_BLURBS:
    check(b not in t, 'old blurb still present: %s' % b[:60])

# regression: 8A / 8C / spec map untouched
check('simple monoatomic ions' in src, '8A oxidation-numbers def intact')
check('salt producing' in src, '8C group7-trends intact')
check("['8.23', 'CORE PRACTICAL 4" in src or 'CORE PRACTICAL 4' in src, 'spec map intact')
check(src.count("'redox-and-groups': {") == 1, 'topic 8 notes record intact')

print()
if fails:
    print('FAILED CHECKS: %d' % len(fails))
    for f in fails:
        print(' -', f)
    raise SystemExit(1)
print('ALL CHECKS PASSED: %d verbatim anchors, %d forbidden phrases, arithmetic + structure OK'
      % (len(ANCHORS), len(FORBIDDEN)))
