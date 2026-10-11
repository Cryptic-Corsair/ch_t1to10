# -*- coding: utf-8 -*-
"""Topic 2 Version 2 (digest edition) — sections 2.15 to 2.18.

Same sourcing rules as v2_part1.py: facts, terms, equations and figures come
only from the source notes and the specification; presentation is re-chunked.
"""

S2_15 = {
    "id": "v2-2-15",
    "sectionKey": "config-properties",
    "number": "2.15",
    "title": "Configuration and Chemical Properties",
    "blurb": "Nucleons identify the atom — but electrons decide how it reacts.",
    "estMinutes": 4,
    "spec": "2.15",
    "specText": "understand that electronic configuration determines the chemical properties of an element",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Atoms can be identified by the mass of their nucleons, but it is their **electronic structure** that determines their behaviour and chemical properties."},
        {"type": "list", "items": [
            "All the elements within a group have the **same number of electrons in their outer shell** — and they have similar properties.",
            "It is the **outer (valence) electrons** that take part in chemical reactions, so the configuration of the outer shell decides how an element reacts.",
            "The position of an element in the Periodic Table is determined by its electronic structure; its physical and chemical properties depend on the electronic configuration.",
        ]},
    ],
}

S2_16 = {
    "id": "v2-2-16",
    "sectionKey": "periodic-blocks",
    "number": "2.16",
    "title": "Blocks of the Periodic Table",
    "blurb": "The block names the sub-shell the last electron enters — and every sub-shell has a fixed capacity.",
    "estMinutes": 10,
    "spec": "2.16",
    "specText": "know that the Periodic Table is divided into blocks, such as s, p and d, and know the number of electrons that can occupy s, p and d sub-shells in the first four quantum shells",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "The Periodic Table is split into blocks named after the sub-shell the last electron enters — and the sub-shell capacities are fixed: **s 2, p 6, d 10, f 14**."},
        {"type": "list", "items": [
            "In the modern periodic table the elements are arranged in order of **atomic number**.",
            "Vertical columns are **groups**; horizontal rows are **periods**.",
            "All the elements within a period have the same number of electron shells — period 2 elements have 2 electron shells.",
        ]},
        {"type": "table", "headers": ["Group", "1", "2", "3", "4", "5", "6", "7", "8"], "rows": [
            ["Outer electronic configuration", "ns¹", "ns²", "ns²np¹", "ns²np²", "ns²np³", "ns²np⁴", "ns²np⁵", "ns²np⁶"],
        ]},
        {"type": "h3", "text": "The four blocks"},
        {"type": "table", "headers": ["Block", "Where", "Outermost electrons"], "rows": [
            ["s – block", "Groups 1 and 2", "Found in the s sub-shell"],
            ["p – block", "Groups 3 to 8", "Found in the p sub-shell"],
            ["d – block", "Transition elements, between groups 2 and 3", "Found in the d sub-shell"],
            ["f – block", "Lanthanides and actinides", "Found in the f sub-shell"],
        ]},
        {"type": "figure", "src": "/diagrams/periodic-blocks.png",
         "alt": "The s, p, d and f blocks of the periodic table",
         "caption": "The first four periods of the table — the block an element sits in tells you which sub-shell its last electron enters."},
        {"type": "h3", "text": "Electrons in the first four quantum shells"},
        {"type": "table", "headers": ["Quantum shell or energy level", "Sub-shells"], "rows": [
            ["1", "1s"],
            ["2", "2s   2p"],
            ["3", "3s   3p   3d"],
            ["4", "4s   4p   4d   4f"],
        ]},
        {"type": "table", "headers": ["Sub-shell", "Number of orbitals", "Total number of electrons"], "rows": [
            ["s", "1  (1 × 2)", "2"],
            ["p", "3  (3 × 2)", "6"],
            ["d", "5  (5 × 2)", "10"],
            ["f", "7  (7 × 2)", "14"],
        ]},
        {"type": "table", "headers": ["Shell", "Principle quantum number (n)", "Sub-shells", "Total number of electrons"], "rows": [
            ["1st", "1", "1s", "2"],
            ["2nd", "2", "2s   2p", "8"],
            ["3rd", "3", "3s   3p   3d", "18"],
            ["4th", "4", "4s   4p   4d   4f", "32"],
        ]},
    ],
}

S2_17 = {
    "id": "v2-2-17",
    "sectionKey": "periodic-graphs",
    "number": "2.17",
    "title": "Graphing Periodic Data",
    "blurb": "Plot first IE with logarithms for elements 1–36 — the repeating pattern is a periodic property.",
    "estMinutes": 10,
    "spec": "2.17",
    "specText": "be able to represent data, in a graphical form (including the use of logarithms of first ionisation energies on a graph) for elements 1 to 36 and hence explain the meaning of the term 'periodic property'",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "A **periodic property** is any property whose values repeat in a regular pattern when the elements are arranged by atomic number — first ionisation energy is one."},
        {"type": "h3", "text": "Plotting the data"},
        {"type": "list", "items": [
            "The first ionisation energies of elements 1 to 36 are plotted using **logarithms**.",
            "Logarithms are used because the ionisation energies span a wide range — taking log(IE) keeps the saw-tooth shape visible without the later periods dwarfing the first.",
        ]},
        {"type": "table", "headers": ["Z", "Element", "First IE / kJ mol⁻¹", "Z", "Element", "First IE / kJ mol⁻¹"], "rows": [
            ["1", "H", "1310", "15", "P", "1060"],
            ["2", "He", "2370", "16", "S", "1000"],
            ["3", "Li", "519", "17", "Cl", "1260"],
            ["4", "Be", "900", "18", "Ar", "1520"],
            ["5", "B", "799", "19", "K", "418"],
            ["6", "C", "1090", "20", "Ca", "590"],
            ["7", "N", "1400", "21", "Sc", "632"],
            ["8", "O", "1310", "22", "Ti", "661"],
            ["9", "F", "1680", "23", "V", "648"],
            ["10", "Ne", "2080", "24", "Cr", "653"],
            ["11", "Na", "494", "25", "Mn", "716"],
            ["12", "Mg", "736", "26", "Fe", "762"],
            ["13", "Al", "577", "27", "Co", "757"],
            ["14", "Si", "786", "28", "Ni", "736"],
        ]},
        {"type": "figure", "src": "/diagrams/ie-1-36-log.png",
         "alt": "Logarithm of first ionisation energy plotted against atomic number for elements 1 to 36",
         "caption": "log(first ionisation energy) for the elements 1 to 36 — the same saw-tooth repeats across each period: rising to a peak at each noble gas (He, Ne, Ar, Kr), with small dips after Group 2 and Group 5, then a steep fall at each new period (Na, K)."},
        {"type": "h3", "text": "What 'periodic property' means"},
        {"type": "def", "term": "Periodic property",
         "text": "Any property of the elements whose values repeat in a regular pattern when the elements are arranged in order of atomic number."},
        {"type": "list", "items": [
            "First ionisation energy is a periodic property — the same pattern repeats across Periods 1, 2, 3 and 4.",
            "Other examples: atomic radius, ionic radius, and melting and boiling temperatures.",
        ]},
        {"type": "h3", "text": "Atomic radius"},
        {"type": "def", "term": "Atomic radius",
         "text": "The measurement of the size of an atom — the distance from the center of the nucleus to the boundary of the electron cloud. Since atoms do not have a well defined boundary, it is found by determining the distance between two nuclei and dividing by 2."},
        {"type": "list", "items": [
            "**Across a period, atomic radius generally decreases:** nuclear charge (proton number) increases, shielding stays constant (electrons enter the same shell), so attraction between nucleus and electrons increases and the electrons are pulled closer.",
            "**Down a group, atomic radius generally increases:** electrons enter new energy levels, shielding increases, and the attraction between the electrons and the nucleus decreases.",
        ]},
        {"type": "h3", "text": "Ionic radius"},
        {"type": "list", "items": [
            "A **positive ion is smaller** than the element's atomic radius — as electrons are removed, the remaining electrons are more strongly attracted to the positive nucleus.",
            "A **negative ion is larger** than the element's atomic radius — as electrons are gained, the number of electrons increases and they are bound less tightly to the nucleus.",
        ]},
        {"type": "figure", "src": "/diagrams/ionic-radius.png",
         "alt": "Comparison of the radii of sodium and its ion, and chlorine and its ion",
         "caption": "Na (11 protons, 11 electrons) shrinks to Na⁺ (11 protons, 10 electrons) · Cl (17 protons, 17 electrons) expands to Cl⁻ (17 protons, 18 electrons)."},
    ],
}

S2_18 = {
    "id": "v2-2-18",
    "sectionKey": "period-trends",
    "number": "2.18",
    "title": "Trends Across Periods and Down Groups",
    "blurb": "Melting points and ionisation energies — the patterns and the reasons behind them.",
    "estMinutes": 18,
    "spec": "2.18",
    "specText": "be able to explain:",
    "outline": [
        "i   the trends in melting and boiling temperatures of the elements of Periods 2 and 3 of the Periodic Table in terms of the structure of the element and the bonding between its atoms or molecules",
        "ii   the general increase and the specific trends in ionisation energy of the elements across Periods 2 and 3 of the Periodic Table",
        "iii   the decrease in first ionisation energy down a group",
    ],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Across Periods 2 and 3: melting points **rise to the giant structures, then collapse** for simple molecules; first ionisation energy **generally rises, with two dips**. Down a group: first ionisation energy **decreases**."},
        {"type": "h3", "text": "i · Melting and boiling temperatures"},
        {"type": "p", "text": "Moving left to right, the elements go from highly electropositive metals through metalloids with giant structures to the simple molecular structure of the non-metals — and both periods show similar trends in melting and boiling points, linked to structure and bond strength."},
        {"type": "table", "headers": ["Period 2", "Li", "Be", "B", "C (diamond)", "N", "O", "F"], "rows": [
            ["Melting temperature / °C", "181", "1278", "2300", "3550", "−210", "−218", "−220"],
            ["Boiling temperature / °C", "1342", "2970", "3927", "4827", "−196", "−183", "−188"],
            ["Type of bonding", "metallic", "metallic", "covalent", "covalent", "covalent", "covalent", "covalent"],
            ["Structure", "giant lattice", "giant lattice", "giant lattice", "giant lattice", "simple molecular", "simple molecular", "simple molecular"],
        ]},
        {"type": "table", "headers": ["Period 3", "Na", "Mg", "Al", "Si", "P", "S", "Cl"], "rows": [
            ["Melting temperature / °C", "98", "649", "660", "1440", "44", "113", "−101"],
            ["Boiling temperature / °C", "883", "1107", "2467", "2355", "280", "445", "−35"],
            ["Type of bonding", "metallic", "metallic", "metallic", "covalent", "covalent", "covalent", "covalent"],
            ["Structure", "giant lattice", "giant lattice", "giant lattice", "giant lattice", "simple molecular", "simple molecular", "simple molecular"],
        ]},
        {"type": "figure", "src": "/diagrams/melting-period3.png",
         "alt": "Melting points across Period 3 in kelvin",
         "caption": "Melting points across Period 3 (in kelvin, from the table above) — rising to a maximum at silicon, then falling sharply for the simple molecular elements."},
        {"type": "h3", "text": "Explaining the melting point trend"},
        {"type": "table", "headers": ["Element(s)", "Structure and bonding", "Why the melting point behaves this way"], "rows": [
            ["Metals (e.g. Na, Mg, Al)", "Metallic bonding — giant lattice structure", "Melting point **increases** across the period: ionic size decreases, more electrons join the 'sea', so the metallic bonding gets stronger."],
            ["Macromolecules (e.g. Si)", "Covalent bonding — giant covalent structure", "Melting point is **very high**: strong covalent bonds link every atom, and a lot of energy is needed to break them."],
            ["Simple molecules (e.g. P₄, S₈, Cl₂)", "Covalent bonding — simple molecular structure", "Melting point is **low**: it depends on the weak London forces between molecules. London forces are stronger in S₈ (more electrons) and stronger in P₄ than Cl₂."],
            ["Noble gases (e.g. Ar)", "Simple atomic structure", "**Lowest** melting and boiling points — individual atoms, so only very weak London forces between them."],
        ]},
        {"type": "callout", "variant": "key", "title": "Melting point order among the simple molecules",
         "text": "S₈ > P₄ > Cl₂ > Ar — bigger molecules have more electrons, creating stronger London dispersion forces."},
        {"type": "h3", "text": "ii · Ionisation energies across a period"},
        {"type": "list", "items": [
            "The 1st ionization energy **increases gradually** across the period:",
            "Atomic size decreases, so the nucleus–outer-electron distance decreases.",
            "Nuclear attraction increases while the shielding effect stays the same.",
            "So attraction between the outer electrons and the nucleus increases — more energy is required to remove them.",
        ]},
        {"type": "h3", "text": "The specific trends — explaining the deviations"},
        {"type": "list", "items": [
            "**Helium > hydrogen (He > H):** helium has one extra proton (greater nuclear charge) and the extra electron enters the same energy level — increased attraction makes the electron harder to remove.",
            "**Boron < beryllium (B < Be) and aluminium < magnesium (Al < Mg):** despite the increased nuclear charge, the outer electron sits in a **2p (or 3p) orbital, higher in energy** than the 2s (or 3s) — and it experiences greater electron–electron repulsion (greater shielding). Less energy is needed to remove it.",
            "·  Be [4]: 1s² 2s²   vs   B [5]: 1s² 2s² 2p¹",
            "·  Mg [12]: 1s² 2s² 2p⁶ 3s²   vs   Al [13]: 1s² 2s² 2p⁶ 3s² 3p¹",
            "**Oxygen < nitrogen (O < N) and sulfur < phosphorous (S < P):** the electron removed is a **paired** p-electron, whereas the element before has an unpaired one — the extra mutual repulsion in the pair means less energy is needed.",
            "·  N [7]: 1s² 2s² 2p³   vs   O [8]: 1s² 2s² 2p⁴",
            "·  P [15]: 1s² 2s² 2p⁶ 3s² 3p³   vs   S [16]: 1s² 2s² 2p⁶ 3s² 3p⁴",
        ]},
        {"type": "figure", "src": "/diagrams/paired-boxes.png",
         "alt": "Box notation comparing the 2p orbitals of nitrogen and oxygen",
         "caption": "Nitrogen's three 2p electrons sit unpaired; oxygen's fourth 2p electron must pair up — the extra mutual repulsion makes it easier to remove."},
        {"type": "h3", "text": "iii · Ionisation energies down the group"},
        {"type": "list", "items": [
            "Ionization energy **decreases** down the group:",
            "Atomic size and the number of shells increase, so the nucleus–outer-electron distance increases.",
            "The outer electrons are more shielded by the inner-shell electrons.",
            "The increase in nuclear charge is **outweighed** by the increase in shielding.",
            "So the outer electrons are less attracted — less energy is required to remove them.",
        ]},
    ],
}

SECTIONS_C = [S2_15, S2_16, S2_17, S2_18]
