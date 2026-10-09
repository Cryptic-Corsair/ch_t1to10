# -*- coding: utf-8 -*-
"""8B rebuild blocks part 2: sections 8.17-8.23.
Source-page traceability:
  8.17 <- 8B/6 flame test + origin + colours table (p14-15)
  8.18 <- Experiment to study thermal decomposition (p13) + flame test procedure (p14)
  8.19 <- Test for ions table + note (p15)
  8.20 <- 8D/1 (p16-18) + Concentration & Calculations (p22) + Indicator & Mean titre (p21-22)
  8.21 <- 8D/2 (p20-21)
  8.22 <- 8D/4 (p24-25) + 8D/5 (p26) + 8D/6 (p27-28)
  8.23 <- Preparation of a standard solution (p19)
Worked examples the source leaves blank (sodium carbonate p19, sulfamic acid steps p22)
are NOT answered or included. Fully worked source examples are kept verbatim.
"""

B_817 = r"""    'flame-colours': [
      { type: 'h3', text: 'Flame test' },
      { type: 'list', items: [
        'It is an important test to identify the **metal cation** present in a compound.',
      ] },
      { type: 'h3', text: 'Origin of flame colours' },
      { type: 'list', items: [
        'Metal cations of the metals in Groups I and II give **characteristic colours**.',
        'This arises due to **electronic transitions** within the cation.',
        'When a compound is heated, electrons gain energy and move to higher energy levels. This is commonly referred as **excitation** of electrons.',
        'Excited electrons in higher energy levels are not stable. So, they fall back to the ground state, emitting energy in the form of light.',
        'The light emitted is of a characteristic frequency and hence colour depends on the energy level difference between the two shells.',
      ] },
      { type: 'figure', src: '/diagrams/flame-origins.png', srcDark: '/diagrams/flame-origins-dark.png', alt: 'An energy level diagram showing excitation from the ground state and relaxation with photon emission, beside the flame colour chart for Group 1 and 2 cations', caption: 'Heat promotes the electron to a higher energy level (excitation); it falls back to the ground state, emitting light of a characteristic frequency — the colour depends on the energy level difference between the two shells.' },
      { type: 'h3', text: 'Flame colours of Group I and II metal cations' },
      { type: 'table', headers: ['Metal cation', 'Formula', 'Colour'], rows: [
        ['Lithium', 'Li⁺', 'red'],
        ['Sodium', 'Na⁺', 'yellow/orange'],
        ['Potassium', 'K⁺', 'lilac'],
        ['Rubidium', 'Rb⁺', 'red/purple'],
        ['Caesium', 'Cs⁺', 'blue/violet'],
        ['Beryllium', 'Be²⁺', '(no colour)'],
        ['Magnesium', 'Mg²⁺', '(no colour)'],
        ['Calcium', 'Ca²⁺', '(brick) red'],
        ['Strontium', 'Sr²⁺', '(crimson) red'],
        ['Barium', 'Ba²⁺', '(apple) green'],
      ] },
    ],"""

B_818 = r"""    'thermal-decomposition-experiment': [
      { type: 'h3', text: 'Experiment to study thermal decomposition' },
      { type: 'list', items: [
        'The relative ease of decomposition of group 2 carbonates and nitrates can be studied by the following experiment.',
      ] },
      { type: 'list', ordered: true, items: [
        'Place the same amount of each of the salts in a series of hard glass test tubes.',
        'Fix a delivery tube to the test tube and clamp in a stand.',
        'Light the burner and measure the time taken for the gas evolved to reach the mark on the test tube in the water bath.',
        'Repeat the experiments by changing the salts.',
      ] },
      { type: 'h3', text: 'Flame test procedure' },
      { type: 'list', ordered: true, items: [
        'Wear a safety glasses and a lab coat. Within a fume cupboard light a Bunsen burner.',
        'Using a dropper, add a few drops of concentrated hydrochloric acid to the solid and mix together so that the metal compound begins to dissolve. (One reason for using hydrochloric acid is to convert any metal compound to a chloride — chlorides are more volatile than other salts so are more likely to give better results.)',
        'Dip a clean metal wire (platinum or nichrome) or silica rod into the mixture to obtain a sample of the compound.',
        'Hold the end of wire or rod in the flame and observe the colour.',
      ] },
    ],"""

B_819 = r"""    'tests-for-ions': [
      { type: 'h3', text: 'Test for ions' },
      { type: 'table', headers: ['Ion', 'Test', 'Observations', 'Equations'], rows: [
        ['Ammonium NH₄⁺', 'Add aqueous sodium hydroxide and warm', 'pungent smell (NH₃); damp litmus paper turns blue; or dense white smoke is formed (NH₄Cl) when passed over hydrogen chloride gas', 'NH₄⁺(aq) + OH⁻(aq) → NH₃(g) + H₂O(l); NH₃(g) + HCl(g) → NH₄Cl(s)'],
        ['Carbonate or hydrogen carbonate CO₃²⁻ or HCO₃⁻', 'Add dilute acid (HCl, H₂SO₄, HNO₃)', 'Effervescence (CO₂); gas turns limewater (Ca(OH)₂) milky (CaCO₃)', 'CO₃²⁻(aq) + 2H⁺(aq) → CO₂(g) + H₂O(l); CO₂(g) + Ca(OH)₂(aq) → CaCO₃(s) + H₂O(l)'],
        ['Sulphate SO₄²⁻', '(To a solution of a compound) add aqueous barium chloride followed by dilute hydrochloric acid or nitric acid', 'White ppt (BaSO₄); insoluble in hydrochloric acid', 'Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s)'],
      ] },
      { type: 'p', text: 'Note: there are other ions that could form white precipitate with barium ions, especially carbonate ions, so in the test there must be H⁺ ions present to prevent barium carbonate from forming as a white precipitate. Dilute nitric acid or dilute hydrochloric acid is therefore added as part of the test.' },
    ],"""

B_820 = r"""    'solution-concentrations': [
      { type: 'h3', text: 'Volumetric analysis' },
      { type: 'list', items: [
        'The quantitative investigation of chemical reactions by comparing reacting volumes is known as **volumetric analysis**.',
        'The procedure by which reacting volumes are determined is known as a **titration**. One substance needed in a titration is a **standard solution**.',
        'Volumetric analysis can be used to determine:',
        'Concentration of a solution',
        'Formula of a compound',
        'Number of moles of a substance',
        'Percentage yield of a substance',
        'Percentage purity of a substance',
        'Water of crystallization of a substance',
      ] },
      { type: 'h3', text: 'Apparatus used' },
      { type: 'table', headers: ['Apparatus', 'Use'], rows: [
        ['Pipette', 'designed to deliver a fixed volume accurately'],
        ['Pipette filler', 'used to fill the pipette'],
        ['Burette', 'designed to deliver definite but variable volumes of liquid'],
        ['Conical flask', 'used to mix solutions'],
        ['Volumetric flask', 'used to prepare standard solutions'],
        ['Beaker', 'used to measure solutions approximately'],
        ['Funnel', 'used to transfer solutions without spilling'],
        ['Dropper', 'used to deliver small volumes of solution'],
        ['White tile', 'used to show the colour changes clearly at the end point'],
        ['Stand', 'used to attach the burette'],
      ] },
      { type: 'figure', src: '/diagrams/titration-setup.png', srcDark: '/diagrams/titration-setup-dark.png', alt: 'A titration bench setup with stand, burette, stopcock, conical flask on a white tile, and a meniscus reading guide', caption: 'Burette above the conical flask on a white tile; the burette reading is taken from the lowest part of the meniscus.' },
      { type: 'h3', text: 'Standard solution' },
      { type: 'list', items: [
        'A **standard solution** is a solution whose concentration is **accurately known**. One way to prepare a standard solution is to take a known mass of a substance (primary standards) and dissolve it in water to make a known volume of solution.',
        'These substances are known as **primary standards**. Ideally primary standards should:',
        'Be solids with high molar masses',
        'Be available in a high degree of purity',
        'Be chemically stable',
        'Not absorb water from the atmosphere',
        'Be soluble in water',
        'React rapidly and completely with other substances when used in titrations',
      ] },
      { type: 'h3', text: 'Concentration' },
      { type: 'list', items: [
        '**Concentration** of a solution is usually expressed as the amount of solute dissolved in a given amount of solvent or solution.',
        'It is usually measured in **moles of solute per dm³ of solution** or in **grams of solute per dm³ of solution**.',
      ] },
      { type: 'h3', text: 'Calculations in titration' },
      { type: 'list', items: [
        'Write a balanced chemical equation.',
        'Calculate the amount/moles of the reagent of known concentration: **amount of substance = concentration × volume (n = cV)**.',
        'Calculate the number of moles of the unknown substance, using the ratio given in the balanced chemical equation.',
        'Calculate the concentration of the unknown solution: **concentration = moles/volume (c = n/V)**.',
      ] },
      { type: 'h3', text: 'Indicator' },
      { type: 'list', items: [
        '**Indicators** are substances whose solutions change color due to changes in pH (by adding acid or alkali).',
        'Two common indicators are **methyl orange** and **phenolphthalein**.',
      ] },
      { type: 'table', headers: ['Indicator', 'Colour in acid', 'Colour in alkali', 'Acid–base combination'], rows: [
        ['methyl orange', 'red', 'yellow', 'strong acid – weak base and strong acid – strong base'],
        ['phenolphthalein', 'colourless', 'pink', 'weak acid – strong base and strong acid – strong base'],
      ] },
      { type: 'h3', text: 'Mean titre' },
      { type: 'list', items: [
        'Mean is the set of values added to give a total, which is then divided by the number of values.',
        'Only **concordant values** must be selected to calculate the mean titre.',
      ] },
      { type: 'table', headers: ['Titration number', '1', '2', '3', '4'], rows: [
        ['final burette reading / cm³', '24.15', '25.30', '24.60', '23.25'],
        ['initial burette reading / cm³', '1.20', '2.70', '1.90', '0.60'],
        ['titre / cm³', '22.95', '22.60', '22.70', '22.65'],
        ['concordant titres', '✗', '✓', '✓', '✓'],
      ] },
      { type: 'list', items: [
        'Titre 2, 3 and 4 are all within 0.20 cm³ of each other, so are concordant.',
      ] },
      { type: 'eq', code: 'Mean  =  (22.60 + 22.70 + 22.65) ÷ 3  =  22.65 cm³', caption: 'Only the concordant titres are averaged' },
    ],"""

B_821 = r"""    'core-practical-3': [
      { type: 'h3', text: 'Titration' },
      { type: 'list', items: [
        'A **titration** is a practical method with the aim of measuring the volumes of two solutions that react together, and using the results to calculate the concentration of one of the solutions.',
        'It involves having one solution in a **burette** and pipetting a known volume of the other solution (**standard solution**) into a **conical flask**.',
        'An **indicator** is then added to the solution in the conical flask and is titrated from the burette until the indicator changes colour.',
      ] },
      { type: 'h3', text: 'Key vocabulary' },
      { type: 'list', items: [
        '**Equivalence point**: the point at which there are exactly the right amounts of substances to complete the reaction.',
        '**End point**: the point at which the indicator just changes colour; ideally the end point should coincide with the equivalence point.',
        '**Meniscus**: the curving of the upper surface of the liquid in a container; the lowest (horizontal) part of the meniscus should be read.',
        '**Titre**: the volume added from the burette during a titration.',
        '**Concordant titres**: titres that are close together (usually within 0.20 cm³ of each other).',
      ] },
      { type: 'h3', text: 'Outline of the titration method' },
      { type: 'list', items: [
        'Add the acid to the alkali or vice versa until the equivalence point of the titration and the end point of the indicator is reached.',
        'Record the burette reading using the lowest part of the meniscus.',
        'Calculate the titre.',
        'Repeat the titration until concordant titres are obtained.',
      ] },
      { type: 'h3', text: 'Titration method (sulfamic acid and sodium hydroxide)' },
      { type: 'list', ordered: true, items: [
        'Rinse the conical flask with deionized water and place it on a white tile.',
        'Using a pipette filler, rinse the pipette with deionized water and then with some of the sodium hydroxide solution.',
        'Use the pipette to transfer 25.0 cm³ of the sodium hydroxide solution to the conical flask.',
        'Add about 3 drops of methyl orange indicator.',
        'Rinse the burette with deionized water and then with sulfamic acid solution.',
        'Fill the burette with sulfamic acid solution and set it up in the stand above the conical flask.',
        'Record the burette reading.',
        'Add the sulfamic acid solution to the conical flask until the indicator just changes colour, and again record the burette reading.',
        'Empty and rinse the conical flask with deionized water, and repeat the titration until concordant titres have been obtained.',
      ] },
    ],"""

B_822 = r"""    'measurement-uncertainty': [
      { type: 'h3', text: 'Mistake' },
      { type: 'list', items: [
        'A **mistake** is something that a skilled operator can avoid by being careful.',
        'Some examples of mistakes:',
        'A chemist weighs a beaker on a balance without making sure the balance is tared (set to zero) beforehand. The reading on the balance could be very different from the actual mass of the beaker.',
        'A student sees a burette reading of 27.35 cm³ but writes it down as 23.75 cm³. This is the students mistake, and nothing to do with the apparatus.',
      ] },
      { type: 'h3', text: 'Error' },
      { type: 'list', items: [
        '**Error** is something that even a skilled operator would find difficult to avoid, and is a consequence of the way the apparatus has been constructed and how readings can be made using it.',
        'Measurement errors can be divided into **random errors** and **systematic errors**:',
      ] },
      { type: 'table', headers: ['Term', 'Meaning'], rows: [
        ['Random error', 'This is an error caused by unpredictable changes in conditions such as temperature or pressure, or by a difference in recording that is difficult to get exactly right.'],
        ['Systematic error', 'This is an error caused by the apparatus, and leads to the recorded value being either too low or too high.'],
      ] },
      { type: 'h3', text: 'Accuracy' },
      { type: 'list', items: [
        '**Accuracy** is a measure of how close values are to the **accepted or correct value**.',
        'If the pipette is wrongly calibrated, it is not **accurate** even if it is precise. It delivers the same amount of liquid but not the amount it claims to have delivered.',
      ] },
      { type: 'h3', text: 'Precision' },
      { type: 'list', items: [
        '**Precision** is a measure of how close values are to **each other**.',
        '**Burette** is a **precise** device to deliver variable amounts of a liquid measured to the nearest 0.05 cm³.',
        '**Pipette** is a **precise** device to deliver a fixed amount of a liquid, usually 25.0 cm³ or 10.0 cm³.',
      ] },
      { type: 'h3', text: 'Measurement uncertainty' },
      { type: 'list', items: [
        'It is the **potential error** involved when using a piece of apparatus to make a measurement.',
        'The size of measurement uncertainty is determined by the **precision of the apparatus**.',
        'Digital balances can have various degree of precision. A balance that measures to three decimal places is more precise than one that measures to only one decimal place.',
        'The greater the degree of precision of the balance, the smaller the measurement uncertainty in the recorded mass.',
      ] },
      { type: 'table', headers: ['Number of decimal places', 'Measurement uncertainty', 'Example'], rows: [
        ['1', '±0.05 g', 'A reading of 17.1 g could be between 17.05 and 17.15 g'],
        ['2', '±0.005 g', 'A reading of 17.10 g could be between 17.095 g and 17.105 g'],
        ['3', '±0.0005 g', 'A reading of 17.100 g could be between 17.0995 g and 17.1005 g'],
      ] },
      { type: 'h3', text: 'Examples of measurement uncertainties in glassware' },
      { type: 'table', headers: ['Apparatus', 'Capacity', 'Measurement uncertainty'], rows: [
        ['burette', '50 cm³', '±0.05 cm³ (but the burette is read twice in a titration, so the total measurement uncertainty is ±0.10 cm³)'],
        ['pipette', '25 cm³', '±0.06 cm³'],
        ['volumetric flask', '250 cm³', '±0.3 cm³'],
      ] },
      { type: 'h3', text: 'Percentage uncertainty' },
      { type: 'list', items: [
        'Percentage uncertainty is the actual measurement uncertainty in an experiment multiplied by 100 and divided by the value recorded.',
      ] },
      { type: 'eq', code: '% uncertainty  =  (actual measurement uncertainty in an experiment ÷ value recorded)  ×  100', caption: 'Percentage uncertainty' },
      { type: 'h3', text: 'Percentage uncertainty of burette, pipette and volumetric flask' },
      { type: 'table', headers: ['Apparatus', 'Capacity', 'Uncertainty', 'Percentage uncertainty'], rows: [
        ['burette', '50 cm³', '±0.05 cm³', 'Note that two burette values are read in a titration, so the total measurement uncertainty is ±0.10 cm³. If the titre is 22.50 cm³, then the percentage uncertainty is: ±0.10 × 100/22.50 = **±0.44%**'],
        ['pipette', '25 cm³', '±0.06 cm³', 'The reading is taken only once, and for the same volume each time, so the percentage uncertainty is always: ±0.06 × 100/25 = **±0.24%**'],
        ['volumetric flask', '250 cm³', '±0.3 cm³', 'The reading is taken only once, and for the same volume each time, so the percentage uncertainty is always: ±0.3 × 100/250 = **±0.12%**'],
      ] },
      { type: 'h3', text: 'Percentage uncertainty of balance' },
      { type: 'list', items: [
        'The percentage uncertainty using a balance depends on:',
        'The precision of the balance',
        'The mass being weighed',
      ] },
      { type: 'worked', title: 'Worked example', problem: 'Mass of marble chips = 3.57 g. The measurement uncertainty in a two decimal place balance is ±0.005 g. We have to count this uncertainty twice — there is a ±0.005 g uncertainty when calibrating the balance to zero, as well as a ±0.005 g uncertainty when measuring mass.', steps: [
        'Total uncertainty = 2 × 0.005 g.',
        'So the percentage uncertainty is ±(2 × 0.005 × 100) ÷ 3.57.',
      ], answer: '±0.28%' },
      { type: 'h3', text: 'Total measurement uncertainty' },
      { type: 'list', items: [
        '**Total measurement uncertainty** is obtained by **adding together the individual uncertainties**.',
        'For example, if a concentration of 0.118 mol dm⁻³ has been calculated from a titration that has involved balance and glassware uncertainties, then the uncertainties might be:',
      ] },
      { type: 'table', headers: ['', 'Percentage uncertainty'], rows: [
        ['Balance', '±0.09%'],
        ['Volumetric flask', '±0.12%'],
        ['Pipette', '±0.24%'],
        ['Burette', '±0.47%'],
        ['Overall percentage uncertainty', '±0.92%'],
      ] },
      { type: 'list', items: [
        'This means there is an overall uncertainty in the concentration of 0.92% of 0.118, which is about ±0.001, so the final value can be quoted like this:',
      ] },
      { type: 'eq', code: 'Concentration  =  0.118  ±  0.001 mol dm⁻³', caption: 'The exact value is in range 0.117 – 0.119 mol dm⁻³' },
      { type: 'h3', text: 'Minimizing uncertainty and errors' },
      { type: 'list', items: [
        'Percentage uncertainty can be minimized by using a **higher value** rather than a lower one.',
        'For example, in using a balance, weighing sample of 5 g will lead to a much lower percentage uncertainty than weighing a 0.5 g sample.',
        '**Minimizing random errors:** for example, in a thermochemistry experiment, **minimizing heat loss** will reduce random errors in the measurement of temperature change.',
      ] },
    ],"""

B_823 = r"""    'core-practical-4': [
      { type: 'h3', text: 'Preparation of a standard solution' },
      { type: 'list', ordered: true, items: [
        '**Weigh** accurately the required amount of material (see section 3.2).',
        '**Transfer** the material to a beaker and dissolve in a small amount of solvent (usually deionised water). Ensure all the solid has dissolved.',
        'Using a clean glass funnel, **transfer the solution quantitatively** into a clean volumetric flask. Wash out the beaker with the solvent a number of times and transfer the washings to the flask. Hint: pouring the liquid down a glass rod held in the spout of the beaker can help prevent liquid running down the side of the beaker.',
        '**Make sure the flask and contents are at ambient temperature.** Carefully add solvent to the flask. Use a pasteur pipette to slowly add solvent until the bottom of the meniscus touches the calibration mark on the neck of the volumetric flask (see section 3.1 for information on the correct use of volumetric flasks).',
        '**Stopper** the volumetric flask and shake to ensure the solution is thoroughly mixed.',
      ] },
    ],"""
