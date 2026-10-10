# -*- coding: utf-8 -*-
"""8B rebuild blocks part 1: sections 8.11-8.16.
Every block is derived strictly from 'upload/Group 1 and 2 notes.pdf' wording,
tables and equations (page trace noted per section).
Source-page traceability:
  8.11 <- 8B/1 (p2-4)   8.12 <- Reactivity (p4)
  8.13 <- 8B/2 and 3 (p5-7)   8.14 <- 8B/4 (p7-8)
  8.15 <- Solubility (p9)     8.16 <- 8B/5 (p10-12)
Worksheet exercises left blank in the source are NOT answered or included.
Equations that the source leaves unbalanced are presented balanced (zero-mistake rule).
"""

B_811 = r"""    'group1-2-ionisation-energy': [
      { type: 'h3', text: 'Introduction to the Group 1 and 2 elements' },
      { type: 'list', items: [
        'The **alkali metals** and **alkaline-earth metals** are members of Group I and Group II, respectively, in the periodic table.',
        'They are **solids at room temperature**.',
        'The pure elements in these groups (except Francium and Radium) appear as **bright silvery solids**. However, when exposed to air, they combine with oxygen to form oxides as surface layers, which makes them appear dull.',
        'They are **s-block elements** since their valence electrons are in s orbitals.',
        'All Group I metals have **one outermost s-electron**, whereas Group II metals have **two** outermost s-electrons. These electrons are situated much further from the nucleus than all other electrons in the metals, so they are only weakly held by the positive nucleus. As a result, Group I and II elements readily lose their outermost s-electrons to form stable ions with **noble gas structures**.',
      ] },
      { type: 'table', headers: ['Group I — The alkali metals', 'Group II — The alkaline-earth metals'], rows: [
        ['Lithium Li', 'Beryllium Be'],
        ['Sodium Na', 'Magnesium Mg'],
        ['Potassium K', 'Calcium Ca'],
        ['Rubidium Rb', 'Strontium Sr'],
        ['Caesium Cs', 'Barium Ba'],
      ] },
      { type: 'table', headers: ['Group I', 'Electronic configuration', 'Group II', 'Electronic configuration'], rows: [
        ['Li Lithium', '[He]2s¹', 'Be Beryllium', '[He]2s²'],
        ['Na Sodium', '[Ne]3s¹', 'Mg Magnesium', '[Ne]3s²'],
        ['K Potassium', '[Ar]4s¹', 'Ca Calcium', '[Ar]4s²'],
        ['Rb Rubidium', '[Kr]5s¹', 'Sr Strontium', '[Kr]5s²'],
        ['Cs Caesium', '[Xe]6s¹', 'Ba Barium', '[Xe]6s²'],
        ['*Fr Francium', '[Rn]7s¹', '*Ra Radium', '[Rn]7s²'],
      ] },
      { type: 'h3', text: 'Atomic radius' },
      { type: 'list', items: [
        'Atomic radius **increases** down the Group I and II as the outer most electrons are further away from the nuclei.',
        'Atomic radius of Group II < Group I.',
      ] },
      { type: 'table', headers: ['Group 1 element', 'Atomic radius / nm', 'Group II element', 'Atomic radius / nm'], rows: [
        ['Li', '0.152', 'Be', '0.112'],
        ['Na', '0.186', 'Mg', '0.160'],
        ['K', '0.231', 'Ca', '0.197'],
        ['Rb', '0.244', 'Sr', '0.215'],
        ['Cs', '0.262', 'Ba', '0.224'],
      ] },
      { type: 'h3', text: 'Ionisation energy' },
      { type: 'list', items: [
        '**Ionisation energy decreases** down the Group I and II.',
        'Down the group, the atomic size increases and the number of shells increases.',
        'Distance between the nucleus and the outer electrons increases.',
        'The outer electrons are more shielded by the electrons in the inner shells.',
        'The effect of the increase in nuclear charge is outweighed by the increase in shielding.',
        'Therefore, the outer electrons are less attracted by the nucleus.',
        'Hence, less energy is required to remove the electrons.',
      ] },
      { type: 'table', headers: ['Group I element', '1st IE / kJ mol⁻¹', '2nd IE / kJ mol⁻¹', 'Group II element', '1st IE / kJ mol⁻¹', '2nd IE / kJ mol⁻¹', '1st and 2nd IE / kJ mol⁻¹'], rows: [
        ['Li', '519', '7 300', 'Be', '900', '1 757', '2 657'],
        ['Na', '494', '4 560', 'Mg', '738', '1 451', '2 189'],
        ['K', '418', '3 070', 'Ca', '590', '1 145', '1 735'],
        ['Rb', '402', '2 370', 'Sr', '550', '1 064', '1 614'],
        ['Cs', '376', '2 420', 'Ba', '503', '965', '1 468'],
      ] },
      { type: 'figure', src: '/diagrams/group12-trends.png', srcDark: '/diagrams/group12-trends-dark.png', alt: 'Paired trend arrows for Groups 1 and 2: atomic radius and reactivity increasing, ionisation energy decreasing down the group, with first-ionisation-energy data anchors', caption: 'Down the group the outer electron is held more weakly — radius and reactivity rise, ionisation energy falls.' },
    ],"""

B_812 = r"""    'group1-2-reactivity': [
      { type: 'h3', text: 'Reactivity' },
      { type: 'list', items: [
        'The reactivity of elements **increases down the group** because of the tendency of elements to lose electron increases down the group. This is because ionization energy decreases, meaning **less energy is required to form the cations**.',
        '**Group I elements are more reactive than Group II** because Group I elements can lose electrons easily and are more metallic.',
      ] },
    ],"""

B_813 = r"""    'group1-2-reactions': [
      { type: 'h3', text: 'Oxygen' },
      { type: 'list', items: [
        'S-block elements react readily with oxygen to form **solid metal oxides**.',
      ] },
      { type: 'table', headers: ['', 'Group I metal with oxygen', 'Group II metal with oxygen'], rows: [
        ['General equation', '4M(s) + O₂(g) → 2M₂O(s)', '2M(s) + O₂(g) → 2MO(s)'],
        ['Products', 'products are oxides containing M⁺ and O²⁻ ions', 'products are oxides containing M²⁺ and O²⁻ ions'],
      ] },
      { type: 'h3', text: 'Chlorine' },
      { type: 'list', items: [
        'All s-block elements react with chlorine to form **ionic chlorides** except beryllium.',
        'The ionic chlorides of Group I and II are **soluble in water**.',
      ] },
      { type: 'table', headers: ['', 'Group I metal with chlorine', 'Group II metal with chlorine'], rows: [
        ['General equation', '2M(s) + Cl₂(g) → 2MCl(s)', 'M(s) + Cl₂(g) → MCl₂(s)'],
        ['Products', 'products are chlorides containing M⁺ and Cl⁻ ions', 'products are chlorides containing M²⁺ and Cl⁻ ions'],
      ] },
      { type: 'h3', text: 'Water' },
      { type: 'list', items: [
        'S-block elements react with water to produce **alkaline metal hydroxide** and **hydrogen**.',
        '**Group 1:** the general equation is',
      ] },
      { type: 'eq', code: '2M(s)  +  2H₂O(l)  →  2MOH(aq)  +  H₂(g)', caption: 'Group 1 metals with water' },
      { type: 'h3', text: 'Lithium' },
      { type: 'list', items: [
        'When a small piece of lithium is added to a beaker or trough of water, it **floats** on the surface of the water (density is half of that of water), gently fizzing and giving off hydrogen.',
        'It gradually reacts and disappears forming a colorless solution of lithium hydroxide.',
      ] },
      { type: 'eq', code: '2Li(s)  +  2H₂O(l)  →  2LiOH(aq)  +  H₂(g)', caption: 'Lithium with cold water' },
      { type: 'h3', text: 'Sodium' },
      { type: 'list', items: [
        'When sodium is added to water, the sodium **melts to form a ball** that moves around on the surface. It fizzes rapidly, and the hydrogen produced may burn with an **orange flame** (the colour is due to the contamination of hydrogen flame with sodium compounds) before the sodium disappears.',
        'The flame is caused by the heat of the reaction igniting the hydrogen.',
      ] },
      { type: 'eq', code: '2Na(s)  +  2H₂O(l)  →  2NaOH(aq)  +  H₂(g)', caption: 'Sodium with cold water' },
      { type: 'h3', text: 'Potassium' },
      { type: 'list', items: [
        'Potassium behaves rather like sodium except that the reaction is **faster** and enough heat is given off to set light to the hydrogen.',
        'When potassium is added to water, the metal melts and floats. It moves around very quickly on the surface of the water. The hydrogen ignites instantly. The metal is also set on fire, with sparks and a **lilac flame**.',
      ] },
      { type: 'eq', code: '2K(s)  +  2H₂O(l)  →  2KOH(aq)  +  H₂(g)', caption: 'Potassium with cold water' },
      { type: 'list', items: [
        '**Group II:** the general equation for all these reactions is',
      ] },
      { type: 'eq', code: 'M(s)  +  2H₂O(l)  →  M(OH)₂(aq)  +  H₂(g)', caption: 'Group 2 metals with cold water' },
      { type: 'h3', text: 'Magnesium' },
      { type: 'list', items: [
        'Reacts **very slowly** with cold water to form magnesium hydroxide and hydrogen gas.',
      ] },
      { type: 'eq', code: 'Mg(s)  +  2H₂O(l)  →  Mg(OH)₂(s)  +  H₂(g)', caption: 'Magnesium with cold water' },
      { type: 'h3', text: 'Magnesium and steam' },
      { type: 'list', items: [
        'Magnesium reacts differently when heated in steam.',
        'It rapidly forms magnesium oxide (a white solid) and hydrogen gas in a **vigorous** reaction. The equation for the reaction is',
      ] },
      { type: 'eq', code: 'Mg(s)  +  H₂O(g)  →  MgO(s)  +  H₂(g)', caption: 'Magnesium with steam' },
      { type: 'list', items: [
        'The hydrogen formed is burned as it leaves the tube. This is for safety reasons to prevent the escape of highly flammable gas into the laboratory.',
      ] },
      { type: 'h3', text: 'Calcium, Strontium and Barium' },
      { type: 'list', items: [
        'React **rapidly** with cold water to form metal hydroxide and hydrogen gas.',
      ] },
      { type: 'eq', code: 'Ca(s)  +  2H₂O(l)  →  Ca(OH)₂(s)  +  H₂(g)', caption: 'Calcium with cold water' },
      { type: 'eq', code: 'Sr(s)  +  2H₂O(l)  →  Sr(OH)₂(aq)  +  H₂(g)          Ba(s)  +  2H₂O(l)  →  Ba(OH)₂(aq)  +  H₂(g)', caption: 'Strontium and barium with cold water' },
    ],"""

B_814 = r"""    'oxides-hydroxides-acids': [
      { type: 'h3', text: 'Oxides' },
      { type: 'list', items: [
        'Group one and two oxides are classified as **basic oxides** (beryllium oxide/hydroxide is **amphoteric**).',
        'They react with water to form **alkaline hydroxides**.',
      ] },
      { type: 'h3', text: 'Reactions of Group I oxides with water' },
      { type: 'table', headers: ['Group I oxide', 'Nature of oxide', 'Reaction with water'], rows: [
        ['M₂O (in general)', 'Basic', 'M₂O(s) + H₂O(l) → 2MOH(aq)'],
      ] },
      { type: 'h3', text: 'Reactions of Group II oxides with water' },
      { type: 'table', headers: ['Group II oxide', 'Nature of oxide', 'Reaction with water'], rows: [
        ['MO (in general)', 'Basic', 'MO(s) + H₂O(l) → M(OH)₂(aq)'],
        ['MgO(s)', 'Basic', 'Reacts very slowly and incompletely to form a slightly alkaline suspension of Mg(OH)₂. MgO(s) + H₂O(l) → Mg(OH)₂(s) (white ppt)'],
        ['CaO(s)', 'Basic', 'CaO(s) + H₂O(l) → Ca(OH)₂(s) (cloudy suspension)'],
      ] },
      { type: 'h3', text: 'Hydroxides and oxides with acids' },
      { type: 'list', items: [
        'All of the **Group 1 and 2 oxides and hydroxides** behave as **bases** and **react with acids** to form **salts and water**.',
        'These reactions can be described as **neutralization** reactions.',
        'During the reactions, the only observations to be made are that a **white solid** reacts to form a **colourless solution**.',
        'The reactions are highly **exothermic**.',
      ] },
    ],"""

B_815 = r"""    'group2-solubility': [
      { type: 'h3', text: 'Solubility of Group II hydroxides and sulphates' },
      { type: 'list', items: [
        'Solubility of **group 2 hydroxides increases** down the group.',
        'Solubility of **group 2 sulphates decreases** down the group.',
      ] },
      { type: 'table', headers: ['Solubility of hydroxides', '', 'Solubility of sulphates', ''], rows: [
        ['Be(OH)₂', 'insoluble', 'BeSO₄', 'very soluble'],
        ['Mg(OH)₂', 'sparingly soluble', 'MgSO₄', 'quite soluble'],
        ['Ca(OH)₂', 'slightly soluble', 'CaSO₄', 'slightly soluble'],
        ['Sr(OH)₂', 'quite soluble', 'SrSO₄', 'sparingly soluble'],
        ['Ba(OH)₂', 'very soluble', 'BaSO₄', 'insoluble'],
      ] },
      { type: 'figure', src: '/diagrams/group2-solubility.png', srcDark: '/diagrams/group2-solubility-dark.png', alt: 'Opposing solubility trends for Group 2 hydroxides and sulfates from beryllium to barium', caption: 'Hydroxide solubility increases Be(OH)₂ → Ba(OH)₂ down the group; sulfate solubility decreases BeSO₄ → BaSO₄.' },
    ],"""

B_816 = r"""    'thermal-stability': [
      { type: 'h3', text: 'Thermal stability' },
      { type: 'list', items: [
        '**Thermal stability** is a term that indicates how stable a compound is when it is heated. If it does not decompose at all, it is very thermally stable. If decompose as much as possible then it is not thermally stable.',
        'The stabilities of the nitrate and carbonate anions are influenced by the **charge and size of the cations** present. Smaller and more highly charged cations affect these anions more.',
        'In general:',
        'Cations with small size and high charge has a higher **polarizing power**.',
        'So they can **polarize the anion** more effectively, which weakens the bonds in anions.',
        'This assists decomposition and makes the compound **less stable** to heat.',
      ] },
      { type: 'h3', text: 'Trends in thermal stability of Group I and II nitrates and carbonates' },
      { type: 'list', items: [
        '**Thermal stability increases down the group.** This is because:',
        'Size of the cation increases and charge density decreases.',
        'So polarizing power decreases.',
        'The cation cannot polarize the anion effectively.',
        'So the bonds in the anion are not weakened.',
        'As the degree of covalency decreases, the strength of the ionic lattice increases.',
        'Therefore, more energy is required to break the lattice structure.',
        '**Thermal stability decreases across the period from Group I to II.** This is because:',
        'Group 2 cations are smaller in size than group 1 cations.',
        'Charge on group 2 cations are higher.',
        'So, polarizing power of group 2 cations are larger.',
        'They can polarize the anion more effectively, weakening the bonds in it.',
        'So less energy is required to break the bonds.',
      ] },
      { type: 'table', headers: ['Group 1 element', 'Charge on ion', 'Ionic radius / nm', 'Group 2 element', 'Charge on ion', 'Ionic radius / nm'], rows: [
        ['Lithium', '+1', '0.074', 'Beryllium', '+2', '0.027'],
        ['Sodium', '+1', '0.102', 'Magnesium', '+2', '0.072'],
        ['Potassium', '+1', '0.138', 'Calcium', '+2', '0.100'],
        ['Rubidium', '+1', '0.149', 'Strontium', '+2', '0.113'],
        ['Caesium', '+1', '0.170', 'Barium', '+2', '0.136'],
      ] },
      { type: 'p', text: 'The cation with the greatest influence (biggest charge and smaller size) on an anion is **Be²⁺**, and the one with the least influence (smallest charge and largest size) is **Cs⁺**.' },
      { type: 'figure', src: '/diagrams/thermal-stability.png', srcDark: '/diagrams/thermal-stability-dark.png', alt: 'A small highly charged cation polarising a nitrate electron cloud, weakening one bond until decomposition occurs, contrasted with a large cation leaving the anion undistorted', caption: 'The bond is weakened due to polarisation of the electron cloud by the cation — decomposition of the Group II nitrate occurs.' },
      { type: 'h3', text: 'Decomposition of Group I and II nitrates' },
      { type: 'table', headers: ['', 'Decomposition of Group I nitrates', 'Decomposition of Group II nitrates'], rows: [
        ['General equation', '2XNO₃(s) → 2XNO₂(s) + O₂(g)', '2X(NO₃)₂(s) → 2XO(s) + 4NO₂(g) + O₂(g)'],
        ['Pattern', 'All Group I nitrates, except LiNO₃, decomposes to form **metal nitrites**, XNO₂ (pale yellow solid) and **oxygen gas**. LiNO₃ decomposes to form lithium oxide, nitrogen dioxide and oxygen.', 'All Group II nitrates decompose to form **metal oxide**, **nitrogen dioxide** (brown gas) and **oxygen**.'],
        ['Description of nitrates', 'Group I nitrates are white solids.', 'Group II nitrates are white solids.'],
        ['Equations', '4LiNO₃(s) → 2Li₂O(s) + 4NO₂(g) + O₂(g) (Greater decomposition); 2NaNO₃(s) → 2NaNO₂(s) + O₂(g) (Lesser decomposition)', '2Be(NO₃)₂(s) → 2BeO(s) + 4NO₂(g) + O₂(g) (Greater decomposition)'],
        ['Observation', '4LiNO₃(s) → Brown fumes; 2NaNO₃(s), 2KNO₃(s), 2RbNO₃(s) and 2CsNO₃(s) → No brown fumes', '2Be(NO₃)₂(s), 2Mg(NO₃)₂(s), 2Ca(NO₃)₂(s), 2Sr(NO₃)₂(s) and 2Ba(NO₃)₂(s) → Brown fumes'],
      ] },
      { type: 'h3', text: 'Decomposition of Group I and II carbonates' },
      { type: 'list', items: [
        'Group 1 carbonates are **stable to heat** except lithium carbonate, which decomposes in a similar manner to group 2 carbonates.',
        'Lithium carbonate decompose when heated because the **Li⁺ cation is very small** and polarizes the O–C bond in the CO₃²⁻ ion sufficiently for it to break and form an O²⁻ ion.',
      ] },
      { type: 'table', headers: ['', 'Decomposition of Group I carbonates', 'Decomposition of Group II carbonates'], rows: [
        ['General equation', 'X₂CO₃(s) → X₂O(s) + CO₂(g)', 'XCO₃(s) → XO(s) + CO₂(g)'],
        ['Pattern', 'All carbonates except lithium carbonate do not decompose at Bunsen temperature. Lithium carbonate decomposes to form lithium oxide and carbon dioxide.', 'All carbonates except barium carbonate decomposes to give metal oxide and carbon dioxide.'],
        ['Description of carbonates', 'Group I carbonates are white solids.', 'Group II carbonates are white solids.'],
      ] },
      { type: 'eq', code: 'Li₂CO₃(s)  →  Li₂O(s)  +  CO₂(g)', caption: 'Lithium carbonate decomposes on heating — the Group I exception' },
      { type: 'list', items: [
        'Na₂CO₃, K₂CO₃, Rb₂CO₃ and Cs₂CO₃ **do not decompose at Bunsen temperatures**.',
        'BaCO₃ **does not decompose at Bunsen temperatures**; BeCO₃, MgCO₃, CaCO₃ and SrCO₃ decompose to give the metal oxide and carbon dioxide.',
      ] },
    ],"""
