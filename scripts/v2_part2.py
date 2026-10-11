# -*- coding: utf-8 -*-
"""Topic 2 Version 2 (digest edition) — sections 2.8 to 2.14.

Same sourcing rules as v2_part1.py: facts, terms, equations and figures come
only from the source notes and the specification; presentation is re-chunked.
"""

S2_8 = {
    "id": "v2-2-8",
    "sectionKey": "ie-definitions",
    "number": "2.8",
    "title": "Defining Ionisation Energies",
    "blurb": "First, second, third — same pattern every time, and all of them endothermic.",
    "estMinutes": 10,
    "spec": "2.8",
    "specText": "be able to define first, second and third ionisation energies and understand that all ionisation energies are endothermic",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Each ionisation energy removes **one mole of electrons from one mole of gaseous** particles — atoms first, then increasingly positive ions — and **every ionisation energy is endothermic**."},
        {"type": "p", "text": "**Ionization energy** is a measure of the energy required to remove electrons from an atom. There are as many ionization energies as there are electrons in the atom."},
        {"type": "h3", "text": "First ionization energy"},
        {"type": "def", "term": "First ionization energy",
         "text": "The energy required to remove one mole of electrons from one mole of gaseous atoms to form one mole of gaseous uni-positive ions."},
        {"type": "eq", "code": "Na(g) → Na⁺(g) + e⁻", "caption": "Example"},
        {"type": "eq", "code": "Mg(g) → Mg⁺(g) + e⁻", "caption": "Example"},
        {"type": "list", "items": [
            "Its value gives an idea of how strongly the nucleus pulls on the electron being removed — the stronger the pull, the more energy needed.",
        ]},
        {"type": "h3", "text": "Second ionization energy"},
        {"type": "def", "term": "Second ionization energy",
         "text": "The energy required to remove 1 mole of electrons from 1 mole of the gaseous uni-positive ions to form one mole of gaseous di-positive ions."},
        {"type": "eq", "code": "Na⁺(g) → Na²⁺(g) + e⁻", "caption": "Example"},
        {"type": "eq", "code": "Mg⁺(g) → Mg²⁺(g) + e⁻", "caption": "Example"},
        {"type": "h3", "text": "Third ionization energy"},
        {"type": "def", "term": "Third ionization energy",
         "text": "The energy required to remove 1 mole of electrons from 1 mole of the gaseous di-positive ions to form one mole of gaseous tri-positive ions."},
        {"type": "eq", "code": "Na²⁺(g) → Na³⁺(g) + e⁻", "caption": "Example"},
        {"type": "eq", "code": "Mg²⁺(g) → Mg³⁺(g) + e⁻", "caption": "Example"},
        {"type": "callout", "variant": "warning", "title": "Always gaseous",
         "text": "Ionisation energies are defined for gaseous atoms and ions — every species in the equation carries the state symbol (g)."},
        {"type": "callout", "variant": "key", "title": "All ionisation energies are endothermic",
         "text": "Every ionisation needs energy to overcome the attraction between the nucleus and the electron, so ionisation energies always have positive (endothermic) values."},
    ],
}

S2_9 = {
    "id": "v2-2-9",
    "sectionKey": "shells-orbitals",
    "number": "2.9",
    "title": "Quantum Shells and Orbitals",
    "blurb": "Shell → sub-shell → orbital: three levels of organisation, ending at 'max two electrons'.",
    "estMinutes": 10,
    "spec": "2.9",
    "specText": "know that an orbital is a region within an atom that can hold up to two electrons with opposite spins",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Quantum shells divide into **sub-shells** (s, p, d, f); sub-shells divide into **orbitals**; each orbital holds **up to two electrons with opposite spins**."},
        {"type": "h3", "text": "Quantum shells"},
        {"type": "p", "text": "Max Planck first presented the quantum theory in 1900. Electrons exist around the nucleus in certain regions of the atom called shells or energy levels — these well-defined energy levels are the **quantum shells**."},
        {"type": "list", "items": [
            "Each shell is described by a number, the **principle quantum number (n)**. The larger the value of n, the further the electron is from the nucleus.",
        ]},
        {"type": "h3", "text": "From shells to sub-shells to orbitals"},
        {"type": "list", "items": [
            "Apart from the first, each quantum shell is divided into **sub-shells** of slightly different energy, described by the letters **s, p, d and f**.",
            "The energy of each sub-shell increases from **s to p to d to f**.",
            "Each sub-shell is made up of **orbitals**.",
        ]},
        {"type": "def", "term": "Orbital",
         "text": "An orbital is a region within an atom that can hold up to two electrons with opposite spins."},
        {"type": "list", "items": [
            "An orbital is the region where the electrons are most likely to be found.",
            "Orbitals are 3-dimensional statistical maps showing the likeliest places to find electrons — they come in different shapes and sizes.",
            "Each orbital holds a **maximum of two electrons** — one spinning clockwise, the other anti-clockwise.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Quick recap",
         "text": "Shell (energy level, n) → sub-shell (s, p, d, f) → orbital (holds max 2 electrons, opposite spins)."},
    ],
}

S2_10 = {
    "id": "v2-2-10",
    "sectionKey": "ie-factors",
    "number": "2.10",
    "title": "Factors Affecting Ionisation Energy",
    "blurb": "Four factors decide the energy: protons, shielding, distance and sub-shell.",
    "estMinutes": 10,
    "spec": "2.10",
    "specText": "understand how ionisation energies are influenced by the number of protons in the nucleus, the electron shielding and the sub-shell from which the electron is removed",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "The ionisation energy depends on the **distance of the electron from the nucleus** and the **effective nuclear charge** — four factors decide the value: protons, shielding, distance, and the sub-shell the electron leaves."},
        {"type": "def", "term": "Nuclear charge (NC)",
         "text": "The actual charge (relative) due to the protons in the nucleus."},
        {"type": "def", "term": "Effective nuclear charge (ENC)",
         "text": "The effectiveness of nuclear charge after passing through filled shells."},
        {"type": "callout", "variant": "tip", "title": "Comparing effective nuclear charges",
         "text": "A simple way to compare effective nuclear charges is to knock off a + for every electron in a filled inner level."},
        {"type": "h3", "text": "The four factors"},
        {"type": "table", "headers": ["Factor", "What happens", "Effect on ionisation energy"], "rows": [
            ["Number of protons (nuclear charge)", "As the effective nuclear charge increases, the force of attraction between nucleus and outer electrons increases.", "Electrons are harder to remove → higher IE"],
            ["Electron shielding", "Outer electrons experience inter-electron repulsion from the inner shells — the more inner-shell electrons, the greater the shielding (screening) effect, so attraction is weaker.", "Less energy needed → lower IE"],
            ["Distance (atomic size)", "As atoms get larger, the outermost electrons are further from the nucleus and held less strongly.", "Less energy needed → lower IE"],
            ["Sub-shell the electron leaves", "Sub-shells sit at slightly different energies: a 2p electron (boron) is easier to remove than a 2s electron (beryllium), and a 3p electron (aluminium) than a 3s electron (magnesium). A paired electron is also easier to remove — the two electrons in one orbital repel each other.", "Higher-energy or paired electron → lower IE"],
        ]},
        {"type": "callout", "variant": "tip", "title": "Quick recap",
         "text": "More protons → higher IE · More shielding → lower IE · Bigger distance → lower IE · Higher-energy or paired sub-shell electron → lower IE."},
    ],
}

S2_11 = {
    "id": "v2-2-11",
    "sectionKey": "ie-evidence",
    "number": "2.11",
    "title": "Ionisation Energies as Evidence",
    "blurb": "Big jumps reveal shells and the group; dips in first IE reveal sub-shells.",
    "estMinutes": 15,
    "spec": "2.11",
    "specText": "know that ideas about electronic structure developed from:",
    "outline": [
        "i   an understanding that successive ionisation energies provide evidence for the existence of quantum shells and the group to which the element belongs",
        "ii   an understanding that the first ionisation energy of successive elements provides evidence for electron sub-shells",
    ],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "**Big jumps** between successive ionisation energies prove **quantum shells** (and count the outer electrons, giving the group); **dips** in first ionisation energies across a period prove **sub-shells**."},
        {"type": "h3", "text": "Successive ionisation energies: evidence for shells"},
        {"type": "p", "text": "When successive ionization energies of an element are listed, there are steady increases and big jumps at defined places — evidence that electrons sit in **quantum shells**. Sodium has 11 electrons; its values jump after the 1st and the 9th:"},
        {"type": "table", "headers": ["", "1st", "2nd", "3rd", "4th", "5th", "6th"], "rows": [
            ["IE / kJ mol⁻¹", "496", "**4563**", "6913", "9544", "13352", "16611"],
        ]},
        {"type": "table", "headers": ["", "7th", "8th", "9th", "10th", "11th"], "rows": [
            ["IE / kJ mol⁻¹", "20115", "25491", "28934", "**141367**", "159079"],
        ]},
        {"type": "list", "items": [
            "**Successive ionization energies are always greater than the previous one** — each electron is removed from an increasingly positive ion, so the nucleus attracts the remaining electrons more.",
            "**Large increases occur when there is a change of shell** — the electron comes from an inner main shell, closer to the nucleus, where nuclear attraction is greater.",
            "Counting the electrons removed **before the first big jump** gives the number of outer-shell electrons — so you can predict the **group** of an unknown element.",
        ]},
        {"type": "figure", "src": "/diagrams/sodium-ie.png",
         "alt": "Graph of log ionisation energy against number of electrons removed for sodium",
         "caption": "Successive ionization energies of sodium, plotted as log(IE) against the order of electron removed — the big jumps after the 1st and 9th electrons mark the changes of quantum shell."},
        {"type": "h3", "text": "Why sodium's ionisation energies increase"},
        {"type": "list", "items": [
            "The first electron is in the **3s** orbital (third quantum shell), so the least energy is needed — the first ionization energy is the lowest.",
            "The **big jump to the 2nd** happens because the second electron is in the **2nd quantum shell**, lower in energy than the 3rd.",
            "The **steady rise from the 2nd to the 9th** shows eight electrons in the same shell — as each is removed, electron–electron repulsion within the shell decreases.",
            "The **big jump from the 9th to the 10th** shows that electron is being removed from the **first quantum shell (1s)**.",
        ]},
        {"type": "h3", "text": "First ionisation energies of successive elements: evidence for sub-shells"},
        {"type": "list", "items": [
            "Plotting the **first ionisation energy against atomic number** gives a repeating saw-tooth: rising across each period to a peak at each noble gas, then falling steeply at the start of the next period.",
            "The rise is not smooth — there are **dips after Group 2** (Be → B, Mg → Al) and **dips after Group 5** (N → O, P → S).",
            "The dips are evidence for **sub-shells**: boron's removed electron is a 2p electron, higher in energy than beryllium's 2s; oxygen's removed electron is a paired 2p electron that repels its partner.",
            "Because the pattern **repeats across every period**, it is strong evidence that every element fills its shells and sub-shells in the same order.",
        ]},
        {"type": "figure", "src": "/diagrams/first-ie-periods.png",
         "alt": "First ionization energies plotted against atomic number for the elements hydrogen to argon",
         "caption": "First ionization energies for periods 1–3 — a periodic property: rising to a peak at each noble gas, with dips after Group 2 and Group 5."},
    ],
}

S2_12 = {
    "id": "v2-2-12",
    "sectionKey": "orbital-shapes",
    "number": "2.12",
    "title": "Shapes of s and p Orbitals",
    "blurb": "Spheres and dumbbells — that is the whole story.",
    "estMinutes": 4,
    "spec": "2.12",
    "specText": "be able to describe the shapes of s and p orbitals",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "**s orbitals are spherical**; **p orbitals are dumbbell-shaped**, three of them along the x, y and z axes."},
        {"type": "list", "items": [
            "The orbitals in different sub-levels have different shapes.",
            "**s orbitals** are spherical — electron density is spread evenly in all directions. Every shell contains one s orbital (1s, 2s, 3s …), each larger than the one before.",
            "**p orbitals** are dumbbell-shaped, with two lobes either side of the nucleus. Each p sub-shell holds **three** p orbitals — pₓ, p_y and p_z — at right angles along the x, y and z axes.",
            "The five d orbitals have four-lobed shapes (their study is beyond the requirements of this specification).",
        ]},
        {"type": "figure", "src": "/diagrams/orbitals.png",
         "alt": "Shapes of s, p and d orbitals",
         "caption": "Shapes of orbitals — s orbitals are spherical; each p sub-shell holds three dumbbell-shaped orbitals (pₓ, p_y, p_z) along the x, y and z axes; the five d orbitals have four-lobed shapes."},
    ],
}

S2_13 = {
    "id": "v2-2-13",
    "sectionKey": "filling-rules",
    "number": "2.13",
    "title": "Rules for Filling Orbitals",
    "blurb": "Singly first with parallel spins (Hund), then pair with opposite spins (Pauli).",
    "estMinutes": 6,
    "spec": "2.13",
    "specText": "know that orbitals in sub-shells:",
    "outline": [
        "i   each take a single electron before pairing up",
        "ii   pair up with two electrons of opposite spin",
    ],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Orbitals **fill singly before they pair up**, and paired electrons must have **opposite spins**."},
        {"type": "def", "term": "Hund's rule",
         "text": "Electrons fill orbitals singly before they start pairing up."},
        {"type": "def", "term": "Pauli Exclusion Principle",
         "text": "Two electrons cannot occupy the same orbital unless they have opposite spin. This is due to the repulsion between electron pairs."},
        {"type": "list", "items": [
            "Each orbital in a sub-shell **takes a single electron before any orbital gets a second** — nitrogen's three 2p orbitals fill as 2p¹ 2p¹ 2p¹, not 2p² 2p¹.",
            "When a second electron does enter an orbital, it **pairs with opposite spin** — one clockwise, one anti-clockwise.",
            "Electrons in separate orbitals have **parallel spins**.",
        ]},
    ],
}

S2_14 = {
    "id": "v2-2-14",
    "sectionKey": "electronic-configuration",
    "number": "2.14",
    "title": "Electronic Configuration",
    "blurb": "Lowest energy first, 4s before 3d — then spdf, boxes, and the Cr/Cu exceptions.",
    "estMinutes": 16,
    "spec": "2.14",
    "specText": "be able to predict the electronic configuration of atoms of the elements from hydrogen to krypton inclusive and their ions, using s, p, d notation and electron-in-boxes notation",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "Key idea",
         "text": "Electrons fill the **lowest energy orbital first** (Aufbau) — so **4s fills before 3d** — and configurations can be written in **spdf notation** or **electron-in-boxes notation**."},
        {"type": "def", "term": "Aufbau principle",
         "text": "Electrons fill up the lowest energy orbital first."},
        {"type": "eq", "code": "1s  2s  2p  3s  3p  4s  3d  4p  …", "caption": "The order in which sub-shells fill"},
        {"type": "list", "items": [
            "Sub-shells that are half filled or completely filled are more stable — orbitals are not filled in numerical order.",
            "**4s is filled before 3d**, because the 4s orbital is at a lower energy level than the 3d orbital.",
            "A shortened version writes the noble gas configuration in square brackets, e.g. [Ne] 3s² 3p⁴.",
        ]},
        {"type": "h3", "text": "Worked examples: atoms"},
        {"type": "worked", "title": "Electronic configuration of carbon",
         "problem": "Write down the electronic configuration of ₆C using spdf notation and box notation.",
         "steps": [
             "Carbon has 6 electrons. Fill the lowest energy orbitals first: 1s, then 2s, then 2p.",
             "**spdf notation:** 1s² 2s² 2p²",
             "**Box notation:** 1s [↑↓] · 2s [↑↓] · 2p [↑] [↑] [ ] — the two 2p electrons occupy separate orbitals singly, with parallel spins (Hund's rule).",
         ],
         "answer": "1s² 2s² 2p²"},
        {"type": "worked", "title": "Electronic configuration of sulfur",
         "problem": "Write down the electronic configuration of ₁₆S using spdf notation and box notation.",
         "steps": [
             "Sulfur has 16 electrons: fill 1s, 2s, 2p, 3s, then 3p.",
             "**spdf notation:** 1s² 2s² 2p⁶ 3s² 3p⁴",
             "**Box notation:** 1s [↑↓] · 2s [↑↓] · 2p [↑↓] [↑↓] [↑↓] · 3s [↑↓] · 3p [↑↓] [↑] [↑]",
             "**Noble gas notation:** [Ne] 3s² 3p⁴",
         ],
         "answer": "1s² 2s² 2p⁶ 3s² 3p⁴  — or  [Ne] 3s² 3p⁴"},
        {"type": "h3", "text": "The exceptions: chromium and copper"},
        {"type": "list", "items": [
            "The electronic structures of **Cr** and **Cu** are exceptional: one of their 4s electrons is donated to the 3d sub-shell, making it half filled or completely filled — a more stable configuration.",
            "**Chromium** is 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹ — not 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁴ 4s².",
            "**Copper** is 1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s¹ — not 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁹ 4s².",
        ]},
        {"type": "h3", "text": "Electronic configuration of ions"},
        {"type": "list", "items": [
            "**Cations (positive ions)** are formed by loss of electrons; **anions (negative ions)** by gain of electrons.",
        ]},
        {"type": "worked", "title": "Sodium atom and sodium ion",
         "problem": "Write down the electronic configuration of the sodium atom and the sodium ion using spdf notation.",
         "steps": [
             "Sodium atom, Na (Z = 11): 1s² 2s² 2p⁶ 3s¹",
             "The Na⁺ ion is formed by losing the single 3s electron.",
         ],
         "answer": "Na⁺: 1s² 2s² 2p⁶ — the same configuration as neon"},
        {"type": "worked", "title": "Chlorine atom and chloride ion",
         "problem": "Write down the electronic configuration of the chlorine atom and the chloride ion using spdf notation.",
         "steps": [
             "Chlorine atom, Cl (Z = 17): 1s² 2s² 2p⁶ 3s² 3p⁵",
             "The Cl⁻ ion is formed by gaining one electron into the last 3p orbital.",
         ],
         "answer": "Cl⁻: 1s² 2s² 2p⁶ 3s² 3p⁶ — the same configuration as argon"},
    ],
}

SECTIONS_B = [S2_8, S2_9, S2_10, S2_11, S2_12, S2_13, S2_14]
