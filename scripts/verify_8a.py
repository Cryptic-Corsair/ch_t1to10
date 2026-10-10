# -*- coding: utf-8 -*-
"""Verify the rebuilt Topic 8A notes in prisma/seed-data/notes.ts against
'upload/Redox notes.pdf': coverage 8.1-8.10, verbatim source anchors,
absence of invented terminology, and chemistry spot-checks."""
import json, re, sys

PATH = '/home/z/my-project/prisma/seed-data/notes.ts'
src = open(PATH, encoding='utf-8').read()

# Extract the 8A half of the redox-and-groups topic (8.0 paragraph + sections 8.1-8.10)
# as plain text for checks. Stops at the first 8B section (group1-2-ionisation-energy).
i = src.index("  'redox-and-groups': {")
j = src.index("    'group1-2-ionisation-energy': [")
tail = src[i:j]
# Decode TS \uXXXX escapes so decoded Unicode matches the anchors below.
tail = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), tail)
# Normalize for matching: drop markdown bold markers and TS escaped quotes.
tail = tail.replace('**', '').replace("\\'", "'")

fail = []
def check(cond, label):
    print(('PASS' if cond else 'FAIL'), '-', label)
    if not cond:
        fail.append(label)

# ---------- 1. section keys present (8.1-8.10) ----------
for k in ['oxidation-numbers','calculating-oxidation-numbers','roman-numerals',
          'formulae-from-oxidation-numbers','electron-transfer','oxidising-reducing-agents',
          'disproportionation','classifying-reactions','metals-nonmetals','half-equations']:
    check(("    '%s': [" % k) in tail, 'section present: %s' % k)

# ---------- 2. verbatim source anchors ----------
anchors = [
  # 8.1 definition + covalent rule + examples (source p6)
  'The charge on an atom of the element in a compound calculated assuming that all the atoms in the compound are simple monoatomic ions',
  'the oxidation number of an atom is the charge it would have if the electrons in each of its bonds belonged to the more electronegative atom',
  'used to tell whether oxidation or reduction has taken place',
  'the oxidation number of magnesium is +2 since the charge on the magnesium ion is 2+',
  'the oxidation number of sulfur is +4 because if the compound were fully ionic the sulfur ion would have a charge of 4+',
  # rules table (source p7)
  'Uncombined element', 'Simple monoatomic ion', 'Group 1, 2 & 3 element in a compound',
  'Fluorine in a compound', 'except in metal hydrides, where it is', 'except in F',
  'peroxide:', 'superoxide:', 'Other halogens with fluorine', 'Halogens (except fluorine) with oxygen',
  'Sum of the oxidation numbers of the elements in a compound or molecule',
  'Sum of the oxidation numbers of the elements in a polyatomic ion',
  'Cl in ClO', 'Cl in ClF = +1', 'F in BF', 'H in NaH =', 'O in F',
  'In CO', 'In SO', 'i.e. +4 + (2', 'i.e. +6 + (4',
  # 8.5 (source p2-3)
  "'Oxidation' is known as the addition of oxygen and 'reduction' is known as the removal of oxygen",
  'iron(III) oxide and carbon monoxide that takes place in the blast furnace',
  'removal of hydrogen and reduction can be described as addition of hydrogen',
  'reaction between chlorine and hydrogen sulfide',
  'When magnesium burns in oxygen it forms magnesium oxide',
  'Each of the two magnesium atoms has lost two electrons',
  'gained four electrons to become oxide ions',
  'Oxidation is the', 'Reduction is the',
  'easily remembered using the mnemonic', 'OIL RIG',
  'chemical reaction in which oxidation and reduction occur at the same time',
  'Electrons are transferred in such reactions',
  'zinc and copper(II) sulfate solution is an example of a redox reaction',
  'zinc metal gives up electrons', 'taken up by the copper ions',
  'The overall equation for the reaction is',
  # 8.6 (source p4)
  'oxidises another species by removing one or more electrons and itself gets reduced',
  'Non-metals are oxidising agents, e.g.',
  'reduces another species by giving it one or more electrons and itself gets oxidised',
  'Metals are reducing agents, e.g. Na, Fe, Zn',
  'electron acceptor', 'electron donor',
  'The oxidation number of the element in it', 'decreases', 'increases',
  # 8.7 (source p5)
  'when the same element is both oxidised and reduced',
  'chlorine gas is passed into aqueous sodium hydroxide',
  'One atom of chlorine is oxidised and the other is reduced',
  # 8.8 (source p9)
  'Electrons have been lost, so the reactions are oxidations',
  'Oxidation', 'occurs when there is an', 'increase', 'decrease',
  'Cl changes from 0 to', 'Mn changes from +7 to +2', 'H changes from +1 to 0',
  'the oxidation number of one of the elements involved has decreased, so reduction has taken place',
  'Use oxidation numbers to show whether the following reactions are examples of redox reactions',
  # 8.9 (source p10-11)
  'Reactive metals in groups 1 and 2 lose electrons when they react',
  'All group 1 and 2 elements undergo oxidation',
  'Predictions about the reactions of p-block elements can be made in terms of redox reactions',
  'the p-block contains elements with different characteristics',
  'reactivity nearly as high as magnesium',
  'the most reactive halogen',
  'electronegativity higher than aluminium but lower than fluorine',
  'the oxidation number of sodium increases from 0 to +1 and that of nitrogen decreases from 0 to',
  'oxidation number of fluorine decreases from 0 to', 'nitrogen increases from 0 to +3',
  # 8.10 (source p14-17)
  'A half equation represents either an oxidation or a reduction',
  'half equations have electrons on the', 'right hand side', 'left hand side',
  'Write down the formula of the reactants and products',
  'Balance the atoms other than oxygen and hydrogen',
  'to the side which requires oxygen atoms',
  'to the side which requires hydrogen atoms',
  'Add electrons to balance the charge on both sides of the equation',
  'double the number of OH',
  'Multiply the equations so that the number of electrons in each is the same',
  'cancel out the electrons on either side of the equation',
  'cancel out any other species which appear on both sides',
  'the reaction between manganate(VII) and iron(II)',
  # 8.3 (source p12)
  'naming compounds and ions that contain elements with varying oxidation numbers',
  'the Roman numeral is written in brackets following the name of the cation',
  'the Roman numeral is written in brackets following the name of the anion',
  'end with the suffix', '-ate',
  'Manganese(IV) oxide', 'Potassium manganate(VII)',
  'iron(II) chloride', 'iron(III) chloride', 'potassium manganate(VI)', 'chromate(VI)',
  # 8.4 (source p12 + exercise p13)
  'Deduce the formula of (a) iron(II) sulfate', 'iron(III) sulfate',
  'copper(I) oxide', 'chromium(III) sulfate(VI)', 'lead(IV) iodide', 'cobalt(III) nitrate(V)',
  # 8.2 worked (source p8 + exercises)
  'Deduce the oxidation number of chlorine in', 'Deduce the oxidation number of nitrogen in',
  'NH', 'NO', 'H',
  # worked extras from source exercises (p6, p8)
  'potassium bromate(I)', '3KOBr', 'KBrO', 'Justify your answer',
  # 8.0 paragraph
  '8A Redox Chemistry', '8B The Elements of Groups 1 and 2', '8C Inorganic Chemistry of Group 7',
]
for a in anchors:
    check(a in tail, 'anchor: %s' % (a[:64]))

# ---------- 3. equations verbatim (with normalized spacing) ----------
eqs = [
  'Fe\u2082O\u2083 + 3CO \u2192 2Fe + 3CO\u2082',
  'H\u2082S + Cl\u2082 \u2192 S + 2HCl',
  '2Mg + O\u2082 \u2192 2MgO',
  'Mg \u2192 Mg\u00b2\u207a + 2e\u207b',
  'O\u2082 + 4e\u207b \u2192 2O\u00b2\u207b',
  'Zn(s) \u2192 Zn\u00b2\u207a(aq) + 2e\u207b',
  'Cu\u00b2\u207a(aq) + 2e\u207b \u2192 Cu(s)',
  'Zn(s) + Cu\u00b2\u207a(aq) \u2192 Zn\u00b2\u207a(aq) + Cu(s)',
  'Zn(s) + CuSO\u2084(aq) \u2192 ZnSO\u2084(aq) + Cu(s)',
  '2NaOH + Cl\u2082 \u2192 NaOCl + NaCl + H\u2082O',
  'Cl\u2082 + 2KBr \u2192 2KCl + Br\u2082',
  'MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O',
  'MnO\u2084\u207b + 4H\u2082O + 5e\u207b \u2192 Mn\u00b2\u207a + 8OH\u207b',
  '5Fe\u00b2\u207a + MnO\u2084\u207b + 8H\u207a \u2192 5Fe\u00b3\u207a + Mn\u00b2\u207a + 4H\u2082O',
  '6Na + N\u2082 \u2192 2Na\u2083N',
  'N\u2082 + 3F\u2082 \u2192 2NF\u2083',
  'Al \u2192 Al\u00b3\u207a + 3e\u207b',
  'F\u2082 + 2e\u207b \u2192 2F\u207b',
  'Na \u2192 Na\u207a + e\u207b',
  'Mg \u2192 Mg\u00b2\u207a + 2e\u207b',
  '3KOBr \u2192 2KBr + KBrO\u2083',
  '2H\u2082O\u2082 \u2192 2H\u2082O + O\u2082',
  'Cl\u2082(aq) + 2e\u207b \u2192 2Cl\u207b(aq)',
  '2H\u2082O(l) + 2e\u207b \u2192 2OH\u207b(aq) + H\u2082(g)',
]
def norm(t):
    return re.sub(r'\s+', ' ', t)
tailn = norm(tail)
for e in eqs:
    check(norm(e) in tailn, 'equation: %s' % e)

# ---------- 4. forbidden invented phrases removed ----------
forbidden = [
  'book-keeping', 'household bleach', 'electronegativates', 'naming trap',
  'classic', 'gatekeeper', 'Strength vocabulary', 'Sign convention marks',
  'metallurgy', 'impossible-looking', 'heavy lifting', 'free information',
  'Why the spec cares', 'The peroxide that everyone gets wrong',
  'grammar for all of it', 'Topic 16', '(3.13)', '(8.25', '(8.27', '(2.10)',
  'chlorate(V), as in', 'nitrate(III), nitrite', 'Cross over the charges',
  'Sanity-check', 'beautiful case', 'grand pattern', 'eagerness',
  'one-minute', 'two-minute', 'jokey', 'trap',
]
for f in forbidden:
    check(f not in tail, 'forbidden absent in 8A: %s' % f)

# ---------- 5. chemistry spot checks (oxidation numbers quoted correctly) ----------
chem = [
  ('so x = \u22121', 'NaCl: Cl = -1'),
  ('+1 + x + (\u22122) = 0, so x = +1', 'NaClO: Cl = +1'),
  ('+1 + x + (\u22126) = 0, so x = +5', 'NaClO3: Cl = +5'),
  ('x + 3(+1) = 0, so x = \u22123', 'NH3: N = -3'),
  ('x + 2(\u22122) = \u22121, so x = +3', 'NO2-: N = +3'),
  ('x + 3(\u22122) = \u22121, so x = +5', 'NO3-: N = +5'),
  ('2(+1) + 2x = 0, so x = \u22121', 'peroxide O = -1'),
  ('+1 + x = 0, so x = \u2212\u00bd', 'superoxide O = -1/2'),
  ('x + 2(\u22121) = 0, so x = +2', 'F2O: O = +2'),
  ('Br in KOBr is +1', 'KOBr: Br = +1'),
  ('Br in KBr is \u22121', 'KBr: Br = -1'),
  ('Br in KBrO\u2083 is +5', 'KBrO3: Br = +5'),
  ('O in H\u2082O\u2082 is \u22121', 'H2O2: O = -1'),
  ('Cl: 0 \u2192 +1 in NaOCl (oxidised)', 'NaOCl: Cl = +1'),
  ('0 \u2192 \u22121 in NaCl (reduced)', 'NaCl: Cl = -1'),
]
for s, label in chem:
    check(s in tailn, 'chemistry: %s' % label)

# ---------- 6. block-type sanity for 8A sections ----------
block_types = {'p','h3','def','eq','list','callout','worked','table','figure'}
obj = tail
types = set(re.findall(r"\{ type: '([a-z]+)'", obj))
check(types <= block_types, 'block types valid: %s' % sorted(types))

# ---------- 7. figures unchanged ----------
for f in ['redox-electron-transfer.png','redox-agents-map.png','redox-disproportionation.png']:
    check(('/diagrams/%s' % f) in tail, 'figure kept: %s' % f)

print('\n%d checks, %d failed' % (len(anchors)+len(eqs)+len(forbidden)+len(chem), len(fail)))
if fail:
    print('FAILURES:'); [print(' -', f) for f in fail]; sys.exit(1)
print('ALL PASSED')
