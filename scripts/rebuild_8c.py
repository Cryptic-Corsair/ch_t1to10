# -*- coding: utf-8 -*-
"""Rebuild Topic 8C notes (sections 8.24-8.28) verbatim from 'upload/Group 7 notes.pdf'.
Anchor-based replacement in prisma/seed-data/notes.ts + blurb cleanup in topics.ts.
Every block below is derived strictly from the source PDF wording, tables and equations.
Source-page traceability:
  8.24 <- /1 TRENDS IN GROUP 7 (p2-3)   8.25 <- 8C/2 displacement part (p5-6)
  8.26 <- 8C/2 metals part (p5) + disproportionation (p7)
  8.27 <- 8C/3 (p9-10) + 8C/4 (p11-12)  8.28 <- Fluorides and Astatides box (p12) + data threads
"""
PATH = '/home/z/my-project/prisma/seed-data/notes.ts'
TPATH = '/home/z/my-project/prisma/seed-data/topics.ts'

src = open(PATH, encoding='utf-8').read()

# ---------------------------------------------------------------- helpers
KEYS = ['group7-trends', 'halogen-displacement', 'chlorine-reactions',
        'halide-reactions', 'halogen-predictions']

def replace_span(s, start_marker, end_marker, block, end_from_tail=False):
    assert s.count(start_marker) == 1, 'start not unique: %s (%d)' % (start_marker[:60], s.count(start_marker))
    i = s.index(start_marker)
    if end_from_tail:
        j = s.rindex(end_marker)
        assert j > i, 'tail end before start'
    else:
        assert s.count(end_marker) == 1, 'end not unique: %s (%d)' % (end_marker[:60], s.count(end_marker))
        j = s.index(end_marker)
        assert i < j, 'order wrong'
    return s[:i] + block.rstrip() + '\n\n' + s[j:]

# ---------------------------------------------------------------- 8.24 group7-trends
B_824 = r"""    'group7-trends': [
      { type: 'h3', text: 'Introduction to the Group 7 elements' },
      { type: 'list', items: [
        'The elements in group VII are known as **halogens** — fluorine, chlorine, bromine, iodine and astatine.',
        'The term **halogen** is derived from Greek meaning **salt producing**. Halogens are very reactive and readily form salts called **halides**.',
        'All have the electronic configuration **ns² np⁵**.',
        'They exist as separate **diatomic molecules** (F₂, Cl₂, Br₂ and I₂).',
      ] },
      { type: 'h3', text: 'Appearance' },
      { type: 'table', headers: ['', 'F₂', 'Cl₂', 'Br₂', 'I₂'], rows: [
        ['Colour', 'Pale yellow', 'Green', 'Red-brown', 'Shiny greyish black'],
        ['State (at RTP)', 'gas', 'gas', 'liquid', 'solid'],
        ['In water', 'very pale yellow', 'Pale green', 'Reddish brown', 'Pale brown'],
        ['In hydrocarbon solvents', '—', 'Pale green', 'Reddish brown', 'Violet'],
      ] },
      { type: 'h3', text: 'Changes of state' },
      { type: 'list', items: [
        'When bromine is left at room temperature it gives off **brown vapour**: Br₂(l) → Br₂(g).',
        'When iodine is left at room temperature, it gives off brown vapour **without melting**. This change is called **sublimation**: I₂(s) → I₂(g).',
      ] },
      { type: 'h3', text: 'Atomic radius' },
      { type: 'list', items: [
        'Atomic radius **increases** down the Group 7 as the outer most electrons are further away from the nuclei.',
      ] },
      { type: 'table', headers: ['F', 'Cl', 'Br', 'I'], rows: [
        ['Atomic radius / nm', '0.064', '0.099', '0.111', '0.128'],
      ] },
      { type: 'h3', text: 'Melting and Boiling temperature' },
      { type: 'list', items: [
        'Melting and boiling temperatures **increase** down the group.',
        'As the size of the halogen increases, the number of electrons also increases.',
        'This increases the strength of **London forces** (instantaneous dipole-induced dipole attraction).',
        'Therefore, more energy is required to overcome the forces between molecules.',
      ] },
      { type: 'h3', text: 'Electronegativity' },
      { type: 'def', term: 'Electronegativity', text: 'The ability of an atom to attract the shared pair of electrons in a covalent bond.' },
      { type: 'list', items: [
        '**Electronegativity decreases** down the group. The electronegativity of fluorine is the highest of all elements.',
        'As the size of the atom increases, the number of shells increases.',
        'This increases the shielding of the nucleus by the inner shell electrons.',
        'As a result, the ability of the nucleus to attract electron pair is reduced.',
      ] },
      { type: 'table', headers: ['Element', 'State at room temperature', 'Melting temperature / °C', 'Boiling temperature / °C', 'Electronegativity'], rows: [
        ['Fluorine', 'gas', '−220', '−188', '4.0'],
        ['Chlorine', 'gas', '−101', '−35', '3.0'],
        ['Bromine', 'liquid', '−7', '59', '2.8'],
        ['Iodine', 'solid', '114', '184', '2.5'],
        ['Astatine', 'solid', '302', '337', '2.2'],
      ] },
      { type: 'h3', text: 'Reactivity' },
      { type: 'list', items: [
        'The reactivity of halogens **decreases down the group**. F₂ is most reactive and I₂ is least reactive.',
        'The decrease in reactivity can be explained with reference to the same factors used to explain the decrease in electronegativity down the group.',
        '**Electron affinity** also decreases down the group, therefore it is less easy to form anions.',
      ] },
    ],"""

# ---------------------------------------------------------------- 8.25 halogen-displacement
B_825 = r"""    'halogen-displacement': [
      { type: 'h3', text: 'Displacement reactions of halogen/halide' },
      { type: 'list', items: [
        'Halogens are strong **oxidizing agents** — as they need an electron to complete their outer shell, they accept electrons and get reduced.',
        'The oxidizing power of the halogen **decreases** as we move down the group from F to I:',
      ] },
      { type: 'eq', code: 'F₂  >  Cl₂  >  Br₂  >  I₂', caption: 'Oxidising power of the halogens' },
      { type: 'list', items: [
        'As the size of the atoms increases down a group, **shielding increases**.',
        'Therefore, the ability of the atoms to accept electrons decreases (form −1 ions) and hence their oxidising power decreases.',
        '**Chlorine** will displace **bromide and iodide** ions from solution.',
        '**Bromine** will displace **iodide** ions from solution, but not chloride ions.',
        '**Iodine** cannot displace either bromide or chloride ions from solution.',
      ] },
      { type: 'h3', text: 'Worked example' },
      { type: 'table', headers: ['Halogen added', 'Observation', 'Potassium chloride(aq)', 'Potassium bromide(aq)', 'Potassium iodide(aq)'], rows: [
        ['chlorine(aq)', 'Appearance of aqueous solution', 'Very pale green', 'Reddish brown', 'Pale brown'],
        ['chlorine(aq)', 'Appearance of cyclohexane', 'Very pale green', 'Reddish brown', 'Violet'],
      ] },
      { type: 'eq', code: 'Cl₂(aq)  +  2Br⁻(aq)  →  2Cl⁻(aq)  +  Br₂(aq)          Cl₂(aq)  +  2I⁻(aq)  →  2Cl⁻(aq)  +  I₂(aq)          Br₂(aq)  +  2I⁻(aq)  →  2Br⁻(aq)  +  I₂(aq)', caption: 'The ionic equations for the three displacements described above' },
      { type: 'figure', src: '/diagrams/displacement-grid.png', srcDark: '/diagrams/displacement-grid-dark.png', alt: 'The halogen displacement grid showing which halogens displace which halide ions, with the three ionic equations', caption: 'Displacement = oxidising power: each halogen oxidises (and displaces) the halide ions of any halogen below it in the group.' },
    ],"""

# ---------------------------------------------------------------- 8.26 chlorine-reactions
B_826 = r"""    'chlorine-reactions': [
      { type: 'h3', text: 'Metals of Group 1 and 2' },
      { type: 'list', items: [
        'Metals react with halogens on heating to form **halides** or white ionic salts.',
        'Reactions are most vigorous between elements at the bottom of Group 1 and 2, and elements at the top of Group 7. The most vigorous reaction should be between **caesium (or francium) and fluorine**, and the least vigorous between **beryllium and iodine (or astatine)**.',
        'These reactions are **redox reactions** in which the halogen acts as an **oxidizing agent**.',
        'The oxidation number of the halogen **decreases from 0 to −1** and the oxidation number of the metal **increases from 0 to +1 or +2**, depending on the group.',
      ] },
      { type: 'table', headers: ['', 'Group I metal', 'Group II metal'], rows: [
        ['General equation', '2M + X₂ → 2MX', 'M + X₂ → MX₂'],
      ] },
      { type: 'eq', code: '2Li  +  Cl₂  →  2LiCl          2Na  +  Br₂  →  2NaBr', caption: 'Group I metal examples' },
      { type: 'eq', code: 'Mg  +  Cl₂  →  MgCl₂          Ca  +  Cl₂  →  CaCl₂          Sr  +  Br₂  →  SrBr₂', caption: 'Group II metal examples' },
      { type: 'h3', text: 'Disproportionation reactions of chlorine' },
      { type: 'def', term: 'Disproportionation', text: 'One element undergoes both oxidation and reduction at the same time.' },
      { type: 'h3', text: 'Chlorine with water' },
      { type: 'list', items: [
        'When chlorine is added to water, it dissolves to form **chlorine water**.',
        'Some of the dissolved chlorine also reacts to form a mixture of two acids, **hydrochloric acid** and **chloric(I) acid** (commonly called **hypochlorous acid**):',
      ] },
      { type: 'eq', code: 'Cl₂  +  H₂O  →  HCl  +  HClO', caption: 'Cl: 0 → −1 (HCl) · 0 → +1 (HClO)' },
      { type: 'list', items: [
        '**HClO is a mild oxidising agent** and effective at killing bacteria without being harmful to humans. For this reason, a small amount of chlorine dissolved in water will sterilize the water, and chlorine is widely used in **swimming pools** and in **water treatment**.',
      ] },
      { type: 'h3', text: 'Chlorine with COLD alkali' },
      { type: 'list', items: [
        'When chlorine is added to **COLD dilute aqueous sodium hydroxide**, it reacts to form the salts of the acids.',
        'These salts are **sodium chloride** and **sodium chlorate(I)**, which is also known as **sodium hypochlorite**.',
        'The disproportionation that occurs can be shown using the oxidation numbers:',
      ] },
      { type: 'eq', code: '2NaOH(aq)  +  Cl₂(g)  →  NaCl(aq)  +  NaOCl(aq)  +  H₂O(l)', caption: 'Cl: 0 → −1 (NaCl) · 0 → +1 (NaOCl)' },
      { type: 'list', items: [
        'The sodium chlorate(I) formed is also a disinfectant, but it is mainly known for its **bleaching action**. It is used extensively in industry and is the **active ingredient in household bleach**.',
      ] },
      { type: 'h3', text: 'Chlorine with HOT alkali' },
      { type: 'list', items: [
        'When chlorine is added to **HOT concentrated sodium hydroxide** solution, it reacts to form sodium chloride and a different product, **sodium chlorate(V)**:',
      ] },
      { type: 'eq', code: '6NaOH(aq)  +  3Cl₂(aq)  →  5NaCl(aq)  +  NaClO₃(aq)  +  3H₂O(l)', caption: 'Cl: 0 → −1 (NaCl) · 0 → +5 (NaClO₃)' },
      { type: 'list', items: [
        'Chlorine is oxidized to the **+5 state**.',
        'The sodium chlorate(V) formed is also used in bleaching, and as a **weed killer**.',
        '**Bromine and iodine react in similar ways.**',
      ] },
    ],"""

# ---------------------------------------------------------------- 8.27 halide-reactions
B_827 = r"""    'halide-reactions': [
      { type: 'h3', text: 'Reducing agent' },
      { type: 'list', items: [
        'The halide ions are **reducing agents**, as they can lose electrons and get oxidized.',
        'Reducing power of halide ions **increases down the group**. **Iodide ions are the most reducing**, followed by bromide ions. Fluoride ions have **no significant reducing properties**.',
        'As the number of shells in the ion increases, there is more **shielding** of the nucleus and the outer electrons become less strongly held.',
        'These electrons are thus **lost more easily** and the halide ion is **more readily oxidised**.',
      ] },
      { type: 'table', headers: ['Oxidising power', 'Halogen', 'Halide', 'Reducing power'], rows: [
        ['High', 'fluorine F₂', 'fluoride F⁻', 'Low'],
        ['↓', 'chlorine Cl₂', 'chloride Cl⁻', '↑'],
        ['↓', 'bromine Br₂', 'bromide Br⁻', '↑'],
        ['↓', 'iodine I₂', 'iodide I⁻', '↑'],
        ['Low', 'astatine At₂', 'astatide At⁻', 'High'],
      ] },
      { type: 'figure', src: '/diagrams/halide-power-ladder.png', srcDark: '/diagrams/halide-power-ladder-dark.png', alt: 'Opposing ladders showing halogen oxidising power increasing towards fluorine while halide reducing power increases towards astatide', caption: 'One trend, two directions: oxidising power of the halogens rises towards fluorine; reducing power of the halide ions rises towards astatide.' },
      { type: 'h3', text: 'Reaction of halide ions with concentrated sulfuric acid' },
      { type: 'list', items: [
        'The variation in reducing strength of the halides can be clearly seen in the reaction of the **sodium halides with concentrated sulfuric acid**.',
        'Concentrated sulfuric acid can act as an **oxidizing agent** and as well as an **acid**.',
        'When it acts as an oxidizing agent, it is reduced, but the extent of its reduction and the products formed depends on the species being oxidized.',
        'The three possible reduction products are **sulfur dioxide**, **sulfur** and **hydrogen sulfide**.',
      ] },
      { type: 'table', headers: ['NaX', 'Observation'], rows: [
        ['NaCl(s)', 'Misty fumes (HCl)'],
        ['NaBr(s)', 'Misty fumes (HBr)'],
        ['NaBr(s)', 'Brown fumes Br₂'],
        ['NaBr(s)', 'Colourless gas with choking odour (SO₂)'],
        ['NaI(s)', 'Misty fumes (HI)'],
        ['NaI(s)', 'Purple fumes + black ppt (I₂)'],
        ['NaI(s)', 'Colourless gas with choking odour (SO₂)'],
        ['NaI(s)', 'Yellow ppt (S)'],
        ['NaI(s)', 'Colourless gas with rotten egg smell (H₂S)'],
      ] },
      { type: 'h3', text: 'Testing for halide ions in solutions' },
      { type: 'list', items: [
        'The analysis of the halide ions is based on the **solubilities of the silver halides**.',
        'The reagent is **silver nitrate** solution, but dilute **nitric acid** is added first to make sure that any other anions (especially carbonate ions) are removed, as they would also form precipitates.',
        'If a precipitate is obtained, **dilute or concentrated ammonia** is added to further confirm the halide ion.',
      ] },
      { type: 'table', headers: ['Halide', 'Add dilute nitric acid, then silver nitrate solution', 'To distinguish the precipitate, add dilute ammonia and concentrated ammonia solution'], rows: [
        ['Chloride', 'White precipitate of AgCl(s)', 'Precipitate soluble in both'],
        ['Chloride', 'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)', 'AgCl(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Cl⁻(aq)'],
        ['Bromide', 'Cream precipitate of AgBr(s)', 'Precipitate slightly soluble in dilute ammonia and soluble in concentrated ammonia'],
        ['Bromide', 'Ag⁺(aq) + Br⁻(aq) → AgBr(s)', 'AgBr(s) + 2NH₃(aq) → [Ag(NH₃)₂]⁺(aq) + Br⁻(aq)'],
        ['Iodide', 'Yellow precipitate of AgI(s)', 'Precipitate insoluble in both'],
        ['Iodide', 'Ag⁺(aq) + I⁻(aq) → AgI(s)', '—'],
      ] },
      { type: 'h3', text: 'Hydrogen halides' },
      { type: 'list', items: [
        'Hydrogen halides are **colourless gases** and exist as **polar diatomic molecules**.',
        'They are formed when hydrogen reacts with halogens.',
      ] },
      { type: 'h3', text: 'Reactions with water' },
      { type: 'list', items: [
        'The hydrogen halides readily react with water to form **acidic solutions**, all of which are colourless.',
      ] },
      { type: 'table', headers: ['Hydrogen halide', 'Acid formed', 'Equation'], rows: [
        ['Hydrogen fluoride', 'hydrofluoric acid', 'HF + H₂O ⇌ H₃O⁺ + F⁻'],
        ['Hydrogen chloride', 'hydrochloric acid', 'HCl + H₂O → H₃O⁺ + Cl⁻'],
        ['Hydrogen bromide', 'hydrobromic acid', 'HBr + H₂O → H₃O⁺ + Br⁻'],
        ['Hydrogen iodide', 'hydroiodic acid', 'HI + H₂O → H₃O⁺ + I⁻'],
      ] },
      { type: 'h3', text: 'Reaction with ammonia' },
      { type: 'list', items: [
        'Hydrogen halides react with ammonia gas to form salts, all of which are **white ionic solids**:',
      ] },
      { type: 'eq', code: 'HCl(g)  +  NH₃(g)  →  NH₄Cl(s)', caption: 'Example — ammonium chloride, a white ionic solid' },
    ],"""

# ---------------------------------------------------------------- 8.28 halogen-predictions
B_828 = r"""    'halogen-predictions': [
      { type: 'p', text: 'If you are asked to predict reactions of **fluorides and astatides** that you are not familiar with, you can use information in this topic to help you.' },
      { type: 'h3', text: 'Fluorides and Astatides' },
      { type: 'list', items: [
        'For example, you could write an equation to show the formation of an acid when **hydrogen astatide** is added to water, based on the equation for hydrogen iodide:',
      ] },
      { type: 'eq', code: 'HI  +  H₂O  →  H₃O⁺  +  I⁻          HAt  +  H₂O  →  H₃O⁺  +  At⁻', caption: 'The hydrogen astatide prediction, based on the equation for hydrogen iodide' },
      { type: 'h3', text: 'Where fluorine and astatine already appear in this topic' },
      { type: 'list', items: [
        '**Appearance and physical state:** fluorine is a pale yellow gas; astatine is a solid at room temperature.',
        '**Melting and boiling temperatures:** astatine continues the increase down the group — melting temperature 302 °C, boiling temperature 337 °C.',
        '**Electronegativity:** fluorine is the highest of all elements (4.0); astatine continues the decrease (2.2).',
        '**Reactivity and oxidising power:** fluorine is the most reactive halogen, at the top of the order F₂ > Cl₂ > Br₂ > I₂; astatine sits at the low end of the oxidising-power ladder, so astatide At⁻ sits at the high end of the reducing-power ladder.',
        '**Reactions with metals:** the least vigorous reaction of all is between beryllium and iodine (or astatine).',
      ] },
    ],"""

# ---------------------------------------------------------------- apply notes.ts
BLOCKS = [B_824, B_825, B_826, B_827, B_828]

# tail marker: the closing of the topic-8 record + closing brace of NOTES (file end)
TAIL = '\n  },\n\n}'

for key, block in zip(KEYS, BLOCKS):
    start = "    '%s': [" % key
    if key != KEYS[-1]:
        nxt = "    '%s': [" % KEYS[KEYS.index(key) + 1]
        src = replace_span(src, start, nxt, block)
    else:
        src = replace_span(src, start, TAIL, block, end_from_tail=True)

open(PATH, 'w', encoding='utf-8').write(src)
print('notes.ts: 5 sections replaced')

# ---------------------------------------------------------------- apply topics.ts blurbs
t = open(TPATH, encoding='utf-8').read()
BLURBS = [
    ("blurb: 'Heavier, duller, less greedy — the halogen trends and their reasons.',",
     "blurb: 'The halogens: appearance, changes of state, atomic radius, melting and boiling temperatures, electronegativity and reactivity — with the reason for each trend.',"),
    ("blurb: 'Cl₂ steals from Br⁻ and I⁻; Br₂ only from I⁻ — the redox evidence.',",
     "blurb: 'Oxidising power decreases F₂ > Cl₂ > Br₂ > I₂ — shown by the displacement reactions with halide ions in aqueous solution.',"),
    ("blurb: 'Water treatment and bleach — disproportionation at work, cold and hot.',",
     "blurb: 'Group 1 and 2 metals with halogens; chlorine with water, with cold dilute alkali and with hot alkali — disproportionation in terms of oxidation numbers.',"),
    ("blurb: 'Sulfuric acid, silver nitrate, ammonia and water — the evidence for the trends.',",
     "blurb: 'Halide ions as reducing agents — the sodium halides with concentrated sulfuric acid, testing for halide ions with silver nitrate and ammonia, and the hydrogen halides with water and ammonia.',"),
    ("blurb: 'Extrapolate the trends — the periodic table lets you meet elements you have never seen.',",
     "blurb: 'Predicting reactions of fluorides and astatides using the trends in halogen chemistry.',"),
]
for old, new in BLURBS:
    assert t.count(old) == 1, 'blurb not unique: %s (%d)' % (old[:50], t.count(old))
    t = t.replace(old, new)
open(TPATH, 'w', encoding='utf-8').write(t)
print('topics.ts: 5 blurbs replaced')
