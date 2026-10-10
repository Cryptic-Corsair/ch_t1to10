# -*- coding: utf-8 -*-
"""Rebuild Topic 8A notes (8.0 closing paragraph + sections 8.1-8.10) verbatim from
'upload/Redox notes.pdf'. Anchor-based replacement in prisma/seed-data/notes.ts.
Every block below is derived strictly from the source PDF wording, examples and tables."""
import sys

PATH = '/home/z/my-project/prisma/seed-data/notes.ts'
src = open(PATH, encoding='utf-8').read()

# ---------------------------------------------------------------- helpers
def replace_section(s, key, next_key, block):
    start = "    '%s': [" % key
    end = "    '%s': [" % next_key
    assert s.count(start) == 1, 'start marker not unique: %s (%d)' % (key, s.count(start))
    assert s.count(end) == 1, 'end marker not unique: %s (%d)' % (next_key, s.count(end))
    i = s.index(start)
    j = s.index(end)
    assert i < j, 'order wrong for %s' % key
    return s[:i] + block.rstrip() + '\n\n' + s[j:]

# ---------------------------------------------------------------- 8.0 closing paragraph
old_para_marker = 'This is the topic where the whole of Year 1 clicks together.'
lines = src.split('\n')
hits = [k for k, ln in enumerate(lines) if old_para_marker in ln]
assert len(hits) == 1, '8.0 paragraph marker not found uniquely'
lines[hits[0]] = ("      { type: 'p', text: 'The topic is built from three sources: **8A Redox Chemistry** "
                  "(8.1 \\u2013 8.10), **8B The Elements of Groups 1 and 2** (8.11 \\u2013 8.23) and "
                  "**8C Inorganic Chemistry of Group 7** (8.24 \\u2013 8.28). Each assessment statement has its "
                  "own section below, in specification order.' },")
src = '\n'.join(lines)

# ---------------------------------------------------------------- 8.1 oxidation-numbers
B = r"""    'oxidation-numbers': [
      { type: 'def', term: 'Oxidation number', text: 'The charge on an atom of the element in a compound calculated assuming that all the atoms in the compound are simple monoatomic ions.' },
      { type: 'p', text: 'Oxidation numbers are assigned to elements in covalent compounds so that the oxidation number of an atom is the charge it would have if the electrons in each of its bonds belonged to the more electronegative atom.' },
      { type: 'p', text: 'Oxidation numbers are used to tell whether oxidation or reduction has taken place.' },
      { type: 'list', items: [
        'In **MgO** the oxidation number of magnesium is **+2** since the charge on the magnesium ion is 2+. Similarly the oxidation number of oxygen is **\u22122**.',
        'In **SO\u2082** the oxidation number of sulfur is **+4** because if the compound were fully ionic the sulfur ion would have a charge of 4+. The oxidation number of oxygen is once again **\u22122**.',
      ] },
      { type: 'p', text: 'Here are the rules for determining oxidation number:' },
      { type: 'table', headers: ['Atom', 'Oxidation number', 'Example'], rows: [
        ['Uncombined element', '0', 'O in O\u2082 = 0'],
        ['Simple monoatomic ion', 'charge on ion', 'Na in Na\u207a = +1'],
        ['Group 1, 2 & 3 element in a compound', '+1, +2 & +3 respectively', 'Na = +1; Mg = +2'],
        ['Fluorine in a compound', '\u22121', 'F in BF\u2083 = \u22121'],
        ['Hydrogen in a compound (except in metal hydrides, where it is \u22121)', '+1', 'H in HCl = +1; H in NaH = \u22121'],
        ['Oxygen in a compound (except in F\u2082O, peroxides and superoxides)', '\u22122', 'O in MgO = \u22122; O in F\u2082O = +2; peroxide: \u22121 (e.g. K\u2082O\u2082); superoxide: \u2212\u00bd (e.g. KO\u2082)'],
        ['Halogens', '\u22121', 'Cl in HCl = \u22121'],
        ['Other halogens with fluorine', '+1', 'Cl in ClF = +1'],
        ['Halogens (except fluorine) with oxygen', '+1, +3, +5 & +7', 'Cl in ClO\u207b = +1; Cl in ClO\u2083\u207b = +5'],
        ['Sum of the oxidation numbers of the elements in a compound or molecule', '0', 'In CO\u2082 the oxidation number of C is +4 and of O is \u22122, i.e. +4 + (2 \u00d7 \u22122) = 0'],
        ['Sum of the oxidation numbers of the elements in a polyatomic ion', 'charge on the ion', 'In SO\u2084\u00b2\u207b the oxidation number of S is +6 and of O is \u22122, i.e. +6 + (4 \u00d7 \u22122) = \u22122'],
      ] },
    ],"""

src = replace_section(src, 'oxidation-numbers', 'calculating-oxidation-numbers', B)

# ---------------------------------------------------------------- 8.2 calculating-oxidation-numbers
B = r"""    'calculating-oxidation-numbers': [
      { type: 'p', text: 'To calculate an unknown oxidation number, fill in the elements whose oxidation numbers you know from the rules, then use the fact that the oxidation numbers add up to **0** in a compound, or to the **charge on the ion**.' },
      { type: 'worked', title: 'Oxidation numbers of chlorine', problem: 'Deduce the oxidation number of chlorine in: (a) NaCl  (b) NaClO  (c) NaClO\u2083.', steps: [
        '(a) Na is +1: +1 + x = 0, so **x = \u22121**.',
        '(b) Na is +1 and O is \u22122: +1 + x + (\u22122) = 0, so **x = +1**.',
        '(c) Na is +1 and 3 O at \u22122 give \u22126: +1 + x + (\u22126) = 0, so **x = +5**.',
      ], answer: 'Cl is \u22121 in NaCl, +1 in NaClO and +5 in NaClO\u2083.' },
      { type: 'worked', title: 'Oxidation numbers of nitrogen', problem: 'Deduce the oxidation number of nitrogen in: (a) NH\u2083  (b) NO\u2082\u207b  (c) NO\u2083\u207b.', steps: [
        '(a) H is +1: x + 3(+1) = 0, so **x = \u22123**.',
        '(b) O is \u22122 and the charge on the ion is \u22121: x + 2(\u22122) = \u22121, so **x = +3**.',
        '(c) x + 3(\u22122) = \u22121, so **x = +5**.',
      ], answer: 'N is \u22123 in NH\u2083, +3 in NO\u2082\u207b and +5 in NO\u2083\u207b.' },
      { type: 'h3', text: 'Peroxides, superoxides, metal hydrides and F\u2082O' },
      { type: 'worked', title: 'Calculating the exceptions', problem: 'Find the oxidation number of: (a) O in H\u2082O\u2082  (b) O in K\u2082O\u2082  (c) O in KO\u2082  (d) H in NaH  (e) O in F\u2082O.', steps: [
        '(a) H is +1: 2(+1) + 2x = 0, so **x = \u22121**.',
        '(b) K is +1: 2(+1) + 2x = 0, so **x = \u22121** \u2014 in a **peroxide** oxygen is \u22121.',
        '(c) K is +1: +1 + x = 0, so **x = \u2212\u00bd** \u2014 in a **superoxide** oxygen is \u2212\u00bd.',
        '(d) Na is +1: +1 + x = 0, so **x = \u22121** \u2014 in a **metal hydride** hydrogen is \u22121.',
        '(e) F is \u22121: x + 2(\u22121) = 0, so **x = +2**.',
      ], answer: 'O is \u22121 in the peroxides, \u2212\u00bd in the superoxide and +2 in F\u2082O; H is \u22121 in the metal hydride.' },
    ],"""

src = replace_section(src, 'calculating-oxidation-numbers', 'roman-numerals', B)

# ---------------------------------------------------------------- 8.3 roman-numerals
B = r"""    'roman-numerals': [
      { type: 'p', text: 'Oxidation numbers are often included in naming compounds and ions that contain elements with varying oxidation numbers. This name is often referred to as a **systematic name**.' },
      { type: 'list', items: [
        'If the **cation** shows variable oxidation state, the Roman numeral is written in brackets following the name of the cation. **Manganese(IV) oxide** shows Mn is in the +4 oxidation state.',
        'If the **anion** contains an element of variable oxidation state, the Roman numeral is written in brackets following the name of the anion. **Potassium manganate(VII)** shows Mn is in the +7 oxidation state.',
        'Names of **oxoanions** end with the suffix **-ate**.',
      ] },
      { type: 'table', headers: ['Formula of compound or ion', 'Relevant oxidation number', 'Systematic name of compound or ion'], rows: [
        ['FeCl\u2082', 'Fe +2', 'iron(II) chloride'],
        ['FeCl\u2083', 'Fe +3', 'iron(III) chloride'],
        ['KMnO\u2084', 'Mn +7', 'potassium manganate(VII)'],
        ['K\u2082MnO\u2084', 'Mn +6', 'potassium manganate(VI)'],
        ['CrO\u2084\u00b2\u207b', 'Cr +6', 'chromate(VI)'],
        ['Cr\u2082O\u2087\u00b2\u207b', 'Cr +6', 'chromate(VI)'],
      ] },
      { type: 'p', text: 'Sodium and magnesium have only one oxidation number in their compounds (+1 and +2 respectively), so it is not necessary to refer to sodium chloride as sodium(I) chloride or magnesium oxide as magnesium(II) oxide.' },
    ],"""

src = replace_section(src, 'roman-numerals', 'formulae-from-oxidation-numbers', B)

# ---------------------------------------------------------------- 8.4 formulae-from-oxidation-numbers
B = r"""    'formulae-from-oxidation-numbers': [
      { type: 'p', text: 'It is equally important to be able to work out the formula of the compound or ion by looking at the systematic name with its oxidation number: take the oxidation numbers from the name, then choose the numbers of each ion that make the total charge zero.' },
      { type: 'worked', title: 'Formulae of the iron sulfates', problem: 'Deduce the formula of (a) iron(II) sulfate  (b) iron(III) sulfate.', steps: [
        '(a) Iron(II) is Fe\u00b2\u207a and sulfate is SO\u2084\u00b2\u207b. One of each balances the charges (+2 and \u22122): **FeSO\u2084**.',
        '(b) Iron(III) is Fe\u00b3\u207a. Two Fe\u00b3\u207a (+6) balance three SO\u2084\u00b2\u207b (\u22126): **Fe\u2082(SO\u2084)\u2083**.',
      ], answer: 'FeSO\u2084 and Fe\u2082(SO\u2084)\u2083.' },
      { type: 'table', headers: ['Systematic name', 'Ions involved', 'Formula'], rows: [
        ['copper(I) oxide', 'Cu\u207a and O\u00b2\u207b', 'Cu\u2082O'],
        ['copper(II) oxide', 'Cu\u00b2\u207a and O\u00b2\u207b', 'CuO'],
        ['chromium(III) sulfate(VI)', 'Cr\u00b3\u207a and SO\u2084\u00b2\u207b', 'Cr\u2082(SO\u2084)\u2083'],
        ['lead(IV) iodide', 'Pb\u2074\u207a and I\u207b', 'PbI\u2084'],
        ['cobalt(III) nitrate(V)', 'Co\u00b3\u207a and NO\u2083\u207b', 'Co(NO\u2083)\u2083'],
      ] },
    ],"""

src = replace_section(src, 'formulae-from-oxidation-numbers', 'electron-transfer', B)

# ---------------------------------------------------------------- 8.5 electron-transfer
B = r"""    'electron-transfer': [
      { type: 'h3', text: 'Background to oxidation and reduction' },
      { type: 'p', text: '\'Oxidation\' is known as the addition of oxygen and \'reduction\' is known as the removal of oxygen.' },
      { type: 'p', text: 'An example of such a reaction is the reaction between iron(III) oxide and carbon monoxide that takes place in the blast furnace.' },
      { type: 'eq', code: 'Fe\u2082O\u2083  +  3CO  \u2192  2Fe  +  3CO\u2082', caption: 'Iron(III) oxide loses oxygen (reduction); carbon monoxide gains oxygen (oxidation).' },
      { type: 'p', text: 'Oxidation can also be described as removal of hydrogen and reduction can be described as addition of hydrogen.' },
      { type: 'p', text: 'An example of such a reaction is the reaction between chlorine and hydrogen sulfide.' },
      { type: 'eq', code: 'H\u2082S  +  Cl\u2082  \u2192  S  +  2HCl', caption: 'H\u2082S loses hydrogen (oxidation); Cl\u2082 gains hydrogen (reduction).' },
      { type: 'h3', text: 'Oxidation and reduction in terms of electron loss and gain' },
      { type: 'p', text: 'Oxidation and reduction involve the transfer of electrons.' },
      { type: 'p', text: 'When magnesium burns in oxygen it forms magnesium oxide.' },
      { type: 'eq', code: '2Mg  +  O\u2082  \u2192  2MgO', caption: 'The reaction results in the formation of Mg\u00b2\u207a and O\u00b2\u207b ions.' },
      { type: 'eq', code: 'Mg  \u2192  Mg\u00b2\u207a  +  2e\u207b', caption: 'Each of the two magnesium atoms has lost two electrons.' },
      { type: 'eq', code: 'O\u2082  +  4e\u207b  \u2192  2O\u00b2\u207b', caption: 'The oxygen molecule has gained four electrons to become oxide ions.' },
      { type: 'p', text: 'The magnesium has been **oxidised** because it has **lost** electrons. Oxygen has been **reduced** because it has **gained** electrons.' },
      { type: 'p', text: 'We now have new definitions of oxidation and reduction:' },
      { type: 'def', term: 'Oxidation', text: 'Oxidation is the **loss** of electrons.' },
      { type: 'def', term: 'Reduction', text: 'Reduction is the **gain** of electrons.' },
      { type: 'callout', variant: 'key', title: 'OIL RIG', text: 'These definitions are easily remembered using the mnemonic **OIL RIG**: **O**xidation **I**s **L**oss (of electrons), **R**eduction **I**s **G**ain (of electrons).' },
      { type: 'h3', text: 'Redox reaction' },
      { type: 'list', items: [
        'A redox reaction is a chemical reaction in which oxidation and reduction occur at the same time.',
        'Electrons are transferred in such reactions.',
        'The reaction between zinc and copper(II) sulfate solution is an example of a redox reaction.',
      ] },
      { type: 'p', text: 'In the following reaction, zinc metal gives up electrons:' },
      { type: 'eq', code: 'Zn(s)  \u2192  Zn\u00b2\u207a(aq)  +  2e\u207b', caption: 'Oxidation' },
      { type: 'p', text: 'The electrons are then taken up by the copper ions:' },
      { type: 'eq', code: 'Cu\u00b2\u207a(aq)  +  2e\u207b  \u2192  Cu(s)', caption: 'Reduction' },
      { type: 'eq', code: 'Zn(s)  +  Cu\u00b2\u207a(aq)  \u2192  Zn\u00b2\u207a(aq)  +  Cu(s)', caption: 'The two half-equations added together \u2014 the electrons cancel.' },
      { type: 'p', text: 'The overall equation for the reaction is:' },
      { type: 'eq', code: 'Zn(s)  +  CuSO\u2084(aq)  \u2192  ZnSO\u2084(aq)  +  Cu(s)', caption: '' },
      { type: 'figure', src: '/diagrams/redox-electron-transfer.png', srcDark: '/diagrams/redox-electron-transfer-dark.png', alt: 'Zinc atoms transferring electrons to copper(II) ions, with the oxidation and reduction half-equations and the overall ionic equation', caption: 'Electron transfer in the reaction between zinc and copper(II) sulfate solution.' },
    ],"""

src = replace_section(src, 'electron-transfer', 'oxidising-reducing-agents', B)

# ---------------------------------------------------------------- 8.6 oxidising-reducing-agents
B = r"""    'oxidising-reducing-agents': [
      { type: 'list', items: [
        'An **oxidising agent** is a species (atom, molecule or ion) that oxidises another species by removing one or more electrons and itself gets reduced.',
        'Non-metals are oxidising agents, e.g. F\u2082, Cl\u2082, O\u2082.',
        'A **reducing agent** is a species that reduces another species by giving it one or more electrons and itself gets oxidised.',
        'Metals are reducing agents, e.g. Na, Fe, Zn.',
      ] },
      { type: 'def', term: 'Oxidising agent', text: 'It is an **electron acceptor**. It oxidises another substance. The oxidation number of the element in it **decreases**.' },
      { type: 'def', term: 'Reducing agent', text: 'It is an **electron donor**. It reduces another substance. The oxidation number of the element in it **increases**.' },
      { type: 'p', text: 'In the reaction between chlorine and potassium bromide:' },
      { type: 'eq', code: 'Cl\u2082  +  2KBr  \u2192  2KCl  +  Br\u2082', caption: 'Cl\u2082 is reduced (0 \u2192 \u22121) \u2014 the oxidising agent. Br\u207b is oxidised (\u22121 \u2192 0) \u2014 the reducing agent.' },
      { type: 'figure', src: '/diagrams/redox-agents-map.png', srcDark: '/diagrams/redox-agents-map-dark.png', alt: 'The reaction of chlorine with potassium bromide labelled with oxidation numbers, showing chlorine as the oxidising agent and bromide as the reducing agent', caption: 'Cl\u2082 gains the electrons (oxidising agent, itself reduced); Br\u207b gives the electrons (reducing agent, itself oxidised).' },
    ],"""

src = replace_section(src, 'oxidising-reducing-agents', 'disproportionation', B)

# ---------------------------------------------------------------- 8.7 disproportionation
B = r"""    'disproportionation': [
      { type: 'def', term: 'Disproportionation', text: 'A disproportionation reaction takes place when the same element is both oxidised and reduced **simultaneously**.' },
      { type: 'p', text: 'Example: when chlorine gas is passed into aqueous sodium hydroxide, a disproportionation reaction takes place. One atom of chlorine is oxidised and the other is reduced.' },
      { type: 'eq', code: '2NaOH  +  Cl\u2082  \u2192  NaOCl  +  NaCl  +  H\u2082O', caption: 'Cl: 0 \u2192 +1 in NaOCl (oxidised); Cl: 0 \u2192 \u22121 in NaCl (reduced).' },
      { type: 'figure', src: '/diagrams/redox-disproportionation.png', srcDark: '/diagrams/redox-disproportionation-dark.png', alt: 'Disproportionation of chlorine in aqueous sodium hydroxide, with one chlorine atom oxidised from 0 to +1 and the other reduced from 0 to \u22121', caption: 'One atom of chlorine is oxidised and the other is reduced.' },
      { type: 'worked', title: 'Heating potassium bromate(I)', problem: 'When potassium bromate(I) is heated it decomposes: 3KOBr \u2192 2KBr + KBrO\u2083. Using the oxidation numbers of the element involved, explain why this is a disproportionation reaction.', steps: [
        'Br in KOBr is **+1**; Br in KBr is **\u22121**; Br in KBrO\u2083 is **+5**.',
        'Bromine starts at +1 in the single species KOBr and finishes at \u22121 and +5.',
        'Bromine has been reduced (+1 \u2192 \u22121) and oxidised (+1 \u2192 +5) at the same time.',
      ], answer: 'The same element (Br), in a single species (KOBr), is simultaneously oxidised and reduced \u2014 disproportionation.' },
      { type: 'worked', title: 'Decomposition of hydrogen peroxide', problem: 'Is the decomposition 2H\u2082O\u2082 \u2192 2H\u2082O + O\u2082 a disproportionation reaction? Justify your answer.', steps: [
        'O in H\u2082O\u2082 is **\u22121** (a peroxide); O in H\u2082O is **\u22122**; O in O\u2082 is **0**.',
        'Oxygen starts at \u22121 in the single species H\u2082O\u2082 and finishes at \u22122 and 0.',
        'Oxygen has been reduced (\u22121 \u2192 \u22122) and oxidised (\u22121 \u2192 0) at the same time.',
      ], answer: 'Yes \u2014 oxygen in H\u2082O\u2082 is simultaneously oxidised and reduced, so the decomposition is a disproportionation reaction.' },
    ],"""

src = replace_section(src, 'disproportionation', 'classifying-reactions', B)

# ---------------------------------------------------------------- 8.8 classifying-reactions
B = r"""    'classifying-reactions': [
      { type: 'h3', text: 'Using oxidation numbers to classify reactions' },
      { type: 'p', text: 'Consider the following ionic half-equations:' },
      { type: 'eq', code: 'Zn(s)  \u2192  Zn\u00b2\u207a(aq)  +  2e\u207b', caption: '' },
      { type: 'eq', code: 'Fe\u00b2\u207a(aq)  \u2192  Fe\u00b3\u207a(aq)  +  e\u207b', caption: '' },
      { type: 'eq', code: '2I\u207b(aq)  \u2192  I\u2082(aq)  +  2e\u207b', caption: '' },
      { type: 'p', text: 'Electrons have been lost, so the reactions are oxidations. The oxidation number of the element has increased in each case: Zn from **0 to +2**, Fe from **+2 to +3**, I from **\u22121 to 0**.' },
      { type: 'p', text: 'Another definition of oxidation and reduction:' },
      { type: 'list', items: [
        '**Oxidation** occurs when there is an **increase** in oxidation number.',
        '**Reduction** occurs when there is a **decrease** in oxidation number.',
      ] },
      { type: 'p', text: 'Now consider the following ionic half-equations:' },
      { type: 'eq', code: 'Cl\u2082(aq)  +  2e\u207b  \u2192  2Cl\u207b(aq)', caption: 'Cl changes from 0 to \u22121.' },
      { type: 'eq', code: 'MnO\u2084\u207b(aq)  +  8H\u207a(aq)  +  5e\u207b  \u2192  Mn\u00b2\u207a(aq)  +  4H\u2082O(l)', caption: 'Mn changes from +7 to +2.' },
      { type: 'eq', code: '2H\u2082O(l)  +  2e\u207b  \u2192  2OH\u207b(aq)  +  H\u2082(g)', caption: 'H changes from +1 to 0.' },
      { type: 'p', text: 'In each case the oxidation number of one of the elements involved has decreased, so reduction has taken place.' },
      { type: 'worked', title: 'Redox or not?', problem: 'Use oxidation numbers to show whether the following reactions are examples of redox reactions: (a) H\u2082S(g) + Cl\u2082(g) \u2192 2HCl(g) + S(s)  (b) NaOH(aq) + HCl(aq) \u2192 NaCl(aq) + H\u2082O(l)  (c) 2NaOH(aq) + Cl\u2082(aq) \u2192 NaCl(aq) + NaClO(aq) + H\u2082O(l).', steps: [
        '(a) Cl: 0 \u2192 \u22121 (decrease, reduced); S: \u22122 \u2192 0 (increase, oxidised). Oxidation and reduction occur at the same time \u2192 **redox**.',
        '(b) Na is +1, O is \u22122, H is +1, Cl is \u22121 \u2014 no element changes its oxidation number \u2192 **not redox**.',
        '(c) Cl: 0 \u2192 \u22121 in NaCl and 0 \u2192 +1 in NaOCl. The same element is oxidised and reduced \u2192 **redox, and a disproportionation**.',
      ], answer: '(a) redox; (b) not redox; (c) redox \u2014 and a disproportionation.' },
    ],"""

src = replace_section(src, 'classifying-reactions', 'metals-nonmetals', B)

# ---------------------------------------------------------------- 8.9 metals-nonmetals
B = r"""    'metals-nonmetals': [
      { type: 'h3', text: 'Reactions of s-block elements' },
      { type: 'p', text: 'Reactive metals in groups 1 and 2 lose electrons when they react.' },
      { type: 'table', headers: ['Element', 'Electrons lost', 'Half equation', 'Change in oxidation number'], rows: [
        ['Sodium (Na) \u2014 Group 1', '1', 'Na \u2192 Na\u207a + e\u207b', 'increase in oxidation number from 0 to +1'],
        ['Magnesium (Mg) \u2014 Group 2', '2', 'Mg \u2192 Mg\u00b2\u207a + 2e\u207b', 'increase in oxidation number from 0 to +2'],
      ] },
      { type: 'p', text: 'All group 1 and 2 elements undergo oxidation.' },
      { type: 'h3', text: 'Reactions of p-block elements' },
      { type: 'p', text: 'Predictions about the reactions of p-block elements can be made in terms of redox reactions. However it is not as straightforward as for s-block elements, because the p-block contains elements with different characteristics.' },
      { type: 'list', items: [
        'The group 3 element **aluminium** is a metal with reactivity nearly as high as magnesium, so it reacts in a similar way: Al \u2192 Al\u00b3\u207a + 3e\u207b \u2014 an **increase** in oxidation number from 0 to +3.',
        'The group 7 element **fluorine** is the most reactive halogen: F\u2082 + 2e\u207b \u2192 2F\u207b \u2014 a **decrease** in oxidation number from 0 to \u22121.',
        '**Nitrogen** is a p-block element in group 5, with an electronegativity higher than aluminium but lower than fluorine. The change in oxidation number for nitrogen therefore depends on which element it reacts with.',
      ] },
      { type: 'p', text: 'Nitrogen reacts with the group 1 metal sodium: 6Na + N\u2082 \u2192 2Na\u2083N. In this redox reaction the oxidation number of sodium increases from 0 to +1 and that of nitrogen decreases from 0 to \u22123.' },
      { type: 'p', text: 'Now consider the reaction of nitrogen with fluorine: N\u2082 + 3F\u2082 \u2192 2NF\u2083. The oxidation number of fluorine decreases from 0 to \u22121, but this time the oxidation number of nitrogen increases from 0 to +3.' },
      { type: 'eq', code: '6Na  +  N\u2082  \u2192  2Na\u2083N          N\u2082  +  3F\u2082  \u2192  2NF\u2083', caption: 'With sodium, nitrogen is reduced (0 \u2192 \u22123); with fluorine, nitrogen is oxidised (0 \u2192 +3).' },
    ],"""

src = replace_section(src, 'metals-nonmetals', 'half-equations', B)

# ---------------------------------------------------------------- 8.10 half-equations
B = r"""    'half-equations': [
      { type: 'p', text: 'A half equation represents either an oxidation or a reduction.' },
      { type: 'list', items: [
        '**Oxidation** half equations have electrons on the **right hand side**: X \u2192 X\u207a + 1e\u207b.',
        '**Reduction** half equations have electrons on the **left hand side**: X + 1e\u207b \u2192 X\u207b.',
      ] },
      { type: 'h3', text: 'Balancing simple half equations' },
      { type: 'list', ordered: true, items: [
        'Write down the formula of the reactants and products.',
        'Balance the atoms.',
        'Add electrons to the right hand side if it is oxidation, and to the left hand side if it is reduction.',
        'Change the number of electrons to balance the charge on both sides of the equation.',
      ] },
      { type: 'table', headers: ['Step', 'Iron(II) being oxidised to iron(III)', 'Chlorine being reduced to chloride'], rows: [
        ['1', 'Fe\u00b2\u207a \u2192 Fe\u00b3\u207a', 'Cl\u2082 \u2192 Cl\u207b'],
        ['2', 'Fe\u00b2\u207a \u2192 Fe\u00b3\u207a (atom already balanced)', 'Cl\u2082 \u2192 2Cl\u207b'],
        ['3', 'Fe\u00b2\u207a \u2192 Fe\u00b3\u207a + e\u207b', 'Cl\u2082 + e\u207b \u2192 2Cl\u207b'],
        ['4', 'Fe\u00b2\u207a \u2192 Fe\u00b3\u207a + e\u207b (already balanced)', 'Cl\u2082 + 2e\u207b \u2192 2Cl\u207b'],
      ] },
      { type: 'h3', text: 'Balancing half equations in acidic medium' },
      { type: 'list', ordered: true, items: [
        'Write down the formula of the reactants and products.',
        'Balance the atoms other than oxygen and hydrogen.',
        'Balance oxygen atoms by adding H\u2082O to the side which requires oxygen atoms.',
        'Balance hydrogen atoms by adding H\u207a to the side which requires hydrogen atoms.',
        'Add electrons to balance the charge on both sides of the equation.',
      ] },
      { type: 'p', text: 'Example: MnO\u2084\u207b being reduced to Mn\u00b2\u207a in acidic medium.' },
      { type: 'table', headers: ['Step', 'Half-equation'], rows: [
        ['1', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a'],
        ['2', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a (Mn balanced)'],
        ['3', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O'],
        ['4', 'MnO\u2084\u207b + 8H\u207a \u2192 Mn\u00b2\u207a + 4H\u2082O'],
        ['5', 'MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O \u2014 +7 on the left side and +2 on the right, so the charge is balanced by adding 5e\u207b to the left side'],
      ] },
      { type: 'h3', text: 'Balancing half equations in alkaline medium' },
      { type: 'list', ordered: true, items: [
        'Write down the formula of the reactants and products.',
        'Balance the atoms other than oxygen and hydrogen.',
        'Add OH\u207b to the side which requires oxygen atoms, and double the number of OH\u207b to the required number of oxygen atoms.',
        'Balance hydrogen atoms by adding H\u2082O to the side which requires hydrogen atoms.',
        'Add electrons to balance the charge on both sides of the equation.',
      ] },
      { type: 'p', text: 'Example: MnO\u2084\u207b being reduced to Mn\u00b2\u207a in alkaline medium.' },
      { type: 'table', headers: ['Step', 'Half-equation'], rows: [
        ['1', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a'],
        ['2', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a (Mn balanced)'],
        ['3', 'MnO\u2084\u207b \u2192 Mn\u00b2\u207a + 8OH\u207b \u2014 4 oxygen atoms on the left side, so 4 \u00d7 2 = 8 OH\u207b'],
        ['4', 'MnO\u2084\u207b + 4H\u2082O \u2192 Mn\u00b2\u207a + 8OH\u207b'],
        ['5', 'MnO\u2084\u207b + 4H\u2082O + 5e\u207b \u2192 Mn\u00b2\u207a + 8OH\u207b \u2014 \u22121 on the left side and \u22126 on the right, so the charge is balanced by adding 5e\u207b to the left side'],
      ] },
      { type: 'h3', text: 'Writing balanced overall equations' },
      { type: 'list', ordered: true, items: [
        'Write the balanced half equation for oxidation and for reduction.',
        'Multiply the equations so that the number of electrons in each is the same.',
        'Add the equations and cancel out the electrons on either side of the equation.',
        'If necessary, cancel out any other species which appear on both sides.',
      ] },
      { type: 'p', text: 'Example: the reaction between manganate(VII) and iron(II).' },
      { type: 'table', headers: ['Step', 'Equations'], rows: [
        ['1', 'Fe\u00b2\u207a \u2192 Fe\u00b3\u207a + e\u207b (oxidation) \u00b7 MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O (reduction)'],
        ['2', '5Fe\u00b2\u207a \u2192 5Fe\u00b3\u207a + 5e\u207b (multiply by 5) \u00b7 MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O (multiply by 1)'],
        ['3', '5Fe\u00b2\u207a + MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 5Fe\u00b3\u207a + 5e\u207b + Mn\u00b2\u207a + 4H\u2082O (add the equations, then cancel the electrons)'],
      ] },
      { type: 'eq', code: '5Fe\u00b2\u207a  +  MnO\u2084\u207b  +  8H\u207a  \u2192  5Fe\u00b3\u207a  +  Mn\u00b2\u207a  +  4H\u2082O', caption: 'The overall equation \u2014 the electrons have cancelled.' },
    ],"""

src = replace_section(src, 'half-equations', 'group1-2-ionisation-energy', B)

# ---------------------------------------------------------------- write back
open(PATH, 'w', encoding='utf-8').write(src)
print('notes.ts rebuilt: 8.0 paragraph + sections 8.1-8.10 replaced')
