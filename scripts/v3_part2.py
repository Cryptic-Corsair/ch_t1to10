# -*- coding: utf-8 -*-
"""Topic 2 Version 2 — REFINED quick-revision edition. Sections 2.8 to 2.14.

Same sourcing rules as v3_part1.py: facts, terms, equations and figures come
only from the source notes and the specification; wording rephrased only for
clarity; mark-scheme vocabulary kept exact; nothing unnecessary.
"""

S2_8 = {
    "id": "v2-2-8",
    "sectionKey": "ie-definitions",
    "number": "2.8",
    "title": "Defining Ionisation Energies",
    "blurb": "One pattern, three definitions, one rule: always gaseous, always endothermic.",
    "estMinutes": 8,
    "spec": "2.8",
    "specText": "be able to define first, second and third ionisation energies and understand that all ionisation energies are endothermic",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "Every ionisation energy removes **one mole of electrons from one mole of gaseous** particles — and **all ionisation energies are endothermic**."},
        {"type": "p", "text": "**Ionization energy** measures the energy required to remove electrons from an atom. There are as many ionization energies as there are electrons in the atom — first, second, third…"},
        {"type": "h3", "text": "The three definitions"},
        {"type": "def", "term": "First ionization energy",
         "text": "The energy required to remove one mole of electrons from one mole of gaseous atoms to form one mole of gaseous uni-positive ions."},
        {"type": "def", "term": "Second ionization energy",
         "text": "The energy required to remove 1 mole of electrons from 1 mole of the gaseous uni-positive ions to form one mole of gaseous di-positive ions."},
        {"type": "def", "term": "Third ionization energy",
         "text": "The energy required to remove 1 mole of electrons from 1 mole of the gaseous di-positive ions to form one mole of gaseous tri-positive ions."},
        {"type": "h3", "text": "Watch the chain on sodium"},
        {"type": "eq", "code": "Na(g) → Na⁺(g) + e⁻", "caption": "First IE — from the atom"},
        {"type": "eq", "code": "Na⁺(g) → Na²⁺(g) + e⁻", "caption": "Second IE — from the uni-positive ion"},
        {"type": "eq", "code": "Na²⁺(g) → Na³⁺(g) + e⁻", "caption": "Third IE — from the di-positive ion"},
        {"type": "list", "items": [
            "Each step removes one more electron — and the ion left behind gets **more and more positive**. The same chain for magnesium: Mg → Mg⁺ → Mg²⁺ → Mg³⁺.",
            "Each value says how strongly the nucleus pulls on the electron being removed — **the stronger the pull, the more energy needed**.",
        ]},
        {"type": "callout", "variant": "warning", "title": "Always gaseous",
         "text": "Ionisation energies are defined for **gaseous** atoms and ions — every species in your equation carries the state symbol **(g)**. Missing (g) loses the mark."},
        {"type": "callout", "variant": "key", "title": "All ionisation energies are endothermic",
         "text": "Energy must be supplied to overcome the attraction between the nucleus and the electron — so every ionisation energy has a **positive (endothermic) value**."},
        {"type": "callout", "variant": "exam", "title": "Mark scheme wording",
         "text": "First IE = **energy required to remove one mole of electrons from one mole of gaseous atoms to form one mole of gaseous uni-positive ions**. Second = from the gaseous **uni-positive ions**… third = from the **di-positive ions**. Keep 'one mole … one mole' and the (g) symbols."},
        {"type": "qa", "items": [
            {"q": "Define the second ionisation energy.", "a": "The energy required to remove **1 mole of electrons from 1 mole of gaseous uni-positive ions** to form one mole of gaseous di-positive ions."},
            {"q": "Write the equation for the third ionisation energy of magnesium.", "a": "**Mg²⁺(g) → Mg³⁺(g) + e⁻** — from the di-positive ion, all species gaseous."},
            {"q": "Why is every ionisation energy endothermic?", "a": "Energy is needed to **overcome the attraction between the nucleus and the electron** — so the values are always positive."},
        ]},
    ],
}

S2_9 = {
    "id": "v2-2-9",
    "sectionKey": "shells-orbitals",
    "number": "2.9",
    "title": "Quantum Shells and Orbitals",
    "blurb": "Shell → sub-shell → orbital: three levels of organisation, ending at 'max two electrons'.",
    "estMinutes": 7,
    "spec": "2.9",
    "specText": "know that an orbital is a region within an atom that can hold up to two electrons with opposite spins",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "Quantum shells divide into **sub-shells** (s, p, d, f) · sub-shells divide into **orbitals** · each orbital holds **up to two electrons with opposite spins**."},
        {"type": "h3", "text": "Level 1 — quantum shells"},
        {"type": "list", "items": [
            "Max Planck presented the quantum theory in 1900 — it describes how electrons are arranged around the nucleus.",
            "Electrons exist in certain regions of the atom called shells or energy levels. These well-defined energy levels are the **quantum shells**.",
            "Each shell is described by a number: the **principle quantum number (n)**. The larger n is, the **further the electron is from the nucleus**.",
        ]},
        {"type": "h3", "text": "Level 2 — sub-shells"},
        {"type": "list", "items": [
            "Apart from the first, each shell divides into **sub-shells** of slightly different energy, described by the letters **s, p, d and f**.",
            "Sub-shell energy rises in the order **s → p → d → f**.",
        ]},
        {"type": "h3", "text": "Level 3 — orbitals"},
        {"type": "def", "term": "Orbital",
         "text": "An orbital is a region within an atom that can hold up to two electrons with opposite spins."},
        {"type": "list", "items": [
            "An orbital is the region where the electrons are **most likely to be found** — a 3-dimensional statistical map, with different shapes and sizes.",
            "Maximum **two electrons** per orbital — one spins **clockwise**, the other **anti-clockwise**.",
        ]},
        {"type": "callout", "variant": "tip", "title": "60-second recap",
         "text": "Shell (energy level, n — bigger n = further out) → sub-shell (s < p < d < f) → orbital (**max 2 electrons, opposite spins**)."},
        {"type": "qa", "items": [
            {"q": "Define an orbital.", "a": "**A region within an atom that can hold up to two electrons with opposite spins.**"},
            {"q": "What does the principle quantum number (n) tell you?", "a": "Which shell the electron is in — the larger n is, the **further from the nucleus**."},
            {"q": "Put s, p, d and f in order of increasing energy.", "a": "**s → p → d → f**."},
        ]},
    ],
}

S2_10 = {
    "id": "v2-2-10",
    "sectionKey": "ie-factors",
    "number": "2.10",
    "title": "Factors Affecting Ionisation Energy",
    "blurb": "Four factors set the value: protons, shielding, distance, sub-shell.",
    "estMinutes": 8,
    "spec": "2.10",
    "specText": "understand how ionisation energies are influenced by the number of protons in the nucleus, the electron shielding and the sub-shell from which the electron is removed",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "IE depends on the **distance** of the electron from the nucleus and the **effective nuclear charge** — four factors decide the value: **protons · shielding · distance · sub-shell**."},
        {"type": "def", "term": "Nuclear charge (NC)",
         "text": "The actual charge (relative) due to the protons in the nucleus."},
        {"type": "def", "term": "Effective nuclear charge (ENC)",
         "text": "The effectiveness of nuclear charge after passing through filled shells."},
        {"type": "callout", "variant": "tip", "title": "Comparing effective nuclear charges",
         "text": "Knock off a **+** for every electron in a filled inner level — what's left is the effective nuclear charge felt by the outer electrons."},
        {"type": "h3", "text": "The four factors"},
        {"type": "table", "headers": ["Factor", "The idea", "Effect on IE"], "rows": [
            ["Number of protons (nuclear charge)", "More effective nuclear charge → stronger attraction between nucleus and outer electrons.", "Harder to remove → **higher IE**"],
            ["Electron shielding", "Inner-shell electrons repel the outer electron (inter-electron repulsion). More inner-shell electrons → more shielding (screening) → weaker attraction.", "Easier to remove → **lower IE**"],
            ["Distance from the nucleus", "Bigger atoms hold their outer electrons further away — held less strongly.", "Easier to remove → **lower IE**"],
            ["Sub-shell the electron leaves", "A 2p electron (boron) is easier to remove than a 2s electron (beryllium); a 3p (aluminium) than a 3s (magnesium). A **paired** electron is also easier to remove — two electrons sharing an orbital repel each other.", "Higher-energy or paired electron → **lower IE**"],
        ]},
        {"type": "callout", "variant": "tip", "title": "60-second recap",
         "text": "More protons → higher IE · more shielding → lower IE · bigger distance → lower IE · higher-energy or paired sub-shell electron → lower IE."},
        {"type": "qa", "items": [
            {"q": "Name the four factors that affect ionisation energy.", "a": "**Number of protons · electron shielding · distance from the nucleus · the sub-shell the electron is removed from.**"},
            {"q": "Why does more shielding lower the ionisation energy?", "a": "Inner-shell electrons **repel** the outer electron (inter-electron repulsion), weakening the nucleus's pull — so less energy is needed."},
            {"q": "Why is boron's first IE lower than beryllium's?", "a": "Boron's outer electron is a **2p** electron — **higher in energy** than beryllium's 2s — so it is easier to remove."},
        ]},
    ],
}

S2_11 = {
    "id": "v2-2-11",
    "sectionKey": "ie-evidence",
    "number": "2.11",
    "title": "Ionisation Energies as Evidence",
    "blurb": "Big jumps reveal shells — and the group. Dips in first IEs reveal sub-shells.",
    "estMinutes": 12,
    "spec": "2.11",
    "specText": "know that ideas about electronic structure developed from:",
    "outline": [
        "i   an understanding that successive ionisation energies provide evidence for the existence of quantum shells and the group to which the element belongs",
        "ii   an understanding that the first ionisation energy of successive elements provides evidence for electron sub-shells",
    ],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "**Big jumps** between successive ionisation energies → evidence for **quantum shells** (and they count the group) · **dips** in first ionisation energies across a period → evidence for **sub-shells**."},
        {"type": "h3", "text": "Evidence 1 — successive ionisation energies of one element"},
        {"type": "p", "text": "Sodium has 11 electrons. List its successive ionisation energies and you see steady increases — and **big jumps** at defined places. That is evidence the electrons sit in **quantum shells**:"},
        {"type": "table", "headers": ["", "1st", "2nd", "3rd", "4th", "5th", "6th"], "rows": [
            ["IE / kJ mol⁻¹", "496", "**4563**", "6913", "9544", "13352", "16611"],
        ]},
        {"type": "table", "headers": ["", "7th", "8th", "9th", "10th", "11th"], "rows": [
            ["IE / kJ mol⁻¹", "20115", "25491", "28934", "**141367**", "159079"],
        ]},
        {"type": "list", "items": [
            "**Successive ionization energies are always greater than the previous one** — each electron is removed from an increasingly positive ion, so the nucleus attracts the remaining electrons more.",
            "**Large increases happen when there is a change of shell** — the electron comes from an inner main shell, closer to the nucleus, where the attraction is greater.",
            "**Count the electrons before the first big jump** → that is the number of outer-shell electrons → the **group** of the element.",
        ]},
        {"type": "figure", "src": "/diagrams/sodium-ie.png",
         "alt": "Graph of log ionisation energy against number of electrons removed for sodium",
         "caption": "Sodium's successive ionisation energies, plotted as log(IE) — the big jumps after the 1st and 9th electrons mark the changes of quantum shell."},
        {"type": "h3", "text": "Sodium's numbers, explained"},
        {"type": "list", "items": [
            "**1st electron — lowest value:** it sits in the **3s** orbital (third quantum shell), furthest out.",
            "**Big jump to the 2nd:** the second electron is in the **2nd quantum shell** — lower in energy, closer in.",
            "**Steady rise from the 2nd to the 9th:** eight electrons from the same shell — as each leaves, the electron–electron repulsion within the shell decreases.",
            "**Big jump from the 9th to the 10th:** that electron is being pulled from the **first quantum shell (1s)**.",
        ]},
        {"type": "h3", "text": "Evidence 2 — first ionisation energies across a period"},
        {"type": "list", "items": [
            "Plot the **first ionisation energy against atomic number**: a repeating **saw-tooth** — rising across each period to a peak at each noble gas, then falling steeply at the start of the next period.",
            "The rise is not smooth — there are **dips after Group 2** (Be → B, Mg → Al) and **dips after Group 5** (N → O, P → S).",
            "Why the dips? Boron's removed electron is a **2p** electron — higher in energy than beryllium's 2s. Oxygen's removed electron is a **paired** 2p electron — it repels its partner.",
            "Because the same pattern **repeats across every period**, it is strong evidence that every element fills its shells and sub-shells in the same order — the dips are evidence for **electron sub-shells**.",
        ]},
        {"type": "figure", "src": "/diagrams/first-ie-periods.png",
         "alt": "First ionization energies plotted against atomic number for the elements hydrogen to argon",
         "caption": "First ionisation energies for periods 1–3 — a periodic property: rising to a peak at each noble gas, with dips after Group 2 and Group 5."},
        {"type": "qa", "items": [
            {"q": "What do the big jumps in successive ionisation energies prove?", "a": "That electrons sit in **quantum shells** — a jump means the next electron comes from an inner shell, closer to the nucleus."},
            {"q": "How can successive ionisation energies give you an element's group?", "a": "Count the electrons removed **before the first big jump** — that number is the number of **outer-shell electrons**, which is the group."},
            {"q": "What do the dips in first ionisation energies across a period prove?", "a": "The existence of **electron sub-shells** — the Group 3 electron is in a higher-energy p sub-shell, and the Group 6 electron is **paired**."},
        ]},
    ],
}

S2_12 = {
    "id": "v2-2-12",
    "sectionKey": "orbital-shapes",
    "number": "2.12",
    "title": "Shapes of s and p Orbitals",
    "blurb": "Spheres and dumbbells — that is the whole story.",
    "estMinutes": 3,
    "spec": "2.12",
    "specText": "be able to describe the shapes of s and p orbitals",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "**s orbitals are spherical · p orbitals are dumbbell-shaped** — three of them, along the x, y and z axes."},
        {"type": "list", "items": [
            "**s orbitals**: spherical — electron density spreads evenly in all directions. Every shell has one s orbital (1s, 2s, 3s …), each **larger than the one before**.",
            "**p orbitals**: **dumbbell-shaped**, two lobes either side of the nucleus. Each p sub-shell holds **three** — pₓ, p_y and p_z — at **right angles** along the x, y and z axes.",
            "The five **d orbitals** have four-lobed shapes — their study is beyond the requirements of this specification.",
        ]},
        {"type": "figure", "src": "/diagrams/orbitals.png",
         "alt": "Shapes of s, p and d orbitals",
         "caption": "s — spherical · p — three dumbbells along x, y and z · d — four-lobed (beyond the spec)."},
        {"type": "qa", "items": [
            {"q": "Describe the shape of an s orbital.", "a": "**Spherical** — electron density spread evenly in all directions around the nucleus."},
            {"q": "Describe p orbitals.", "a": "**Dumbbell-shaped**, two lobes either side of the nucleus; **three per p sub-shell** at right angles along the x, y and z axes."},
        ]},
    ],
}

S2_13 = {
    "id": "v2-2-13",
    "sectionKey": "filling-rules",
    "number": "2.13",
    "title": "Rules for Filling Orbitals",
    "blurb": "Singly first (Hund), then pair with opposite spins (Pauli).",
    "estMinutes": 4,
    "spec": "2.13",
    "specText": "know that orbitals in sub-shells:",
    "outline": [
        "i   each take a single electron before pairing up",
        "ii   pair up with two electrons of opposite spin",
    ],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "Orbitals **fill singly before they pair up** — and a paired pair must have **opposite spins**."},
        {"type": "def", "term": "Hund's rule",
         "text": "Electrons fill orbitals singly before they start pairing up."},
        {"type": "def", "term": "Pauli Exclusion Principle",
         "text": "Two electrons cannot occupy the same orbital unless they have opposite spin. This is due to the repulsion between electron pairs."},
        {"type": "list", "items": [
            "Nitrogen's three 2p orbitals fill as **2p¹ 2p¹ 2p¹** — each orbital takes a single electron first, never 2p² 2p¹.",
            "When a second electron does enter an orbital, it **pairs with opposite spin** — one clockwise, one anti-clockwise.",
            "Electrons sitting in separate orbitals have **parallel spins**.",
        ]},
        {"type": "qa", "items": [
            {"q": "State Hund's rule.", "a": "Electrons **fill orbitals singly** before they start **pairing up**."},
            {"q": "State the Pauli Exclusion Principle.", "a": "Two electrons **cannot occupy the same orbital unless they have opposite spin** — because of the repulsion between electron pairs."},
            {"q": "How do nitrogen's three 2p electrons fill the sub-shell?", "a": "One per orbital: **2p¹ 2p¹ 2p¹**, with parallel spins."},
        ]},
    ],
}

S2_14 = {
    "id": "v2-2-14",
    "sectionKey": "electronic-configuration",
    "number": "2.14",
    "title": "Electronic Configuration",
    "blurb": "Lowest energy first, 4s before 3d — then spdf, boxes, and the Cr/Cu exceptions.",
    "estMinutes": 12,
    "spec": "2.14",
    "specText": "be able to predict the electronic configuration of atoms of the elements from hydrogen to krypton inclusive and their ions, using s, p, d notation and electron-in-boxes notation",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key", "title": "In one line",
         "text": "Fill the **lowest energy orbital first** (Aufbau) — so **4s fills before 3d**. Write configurations in **spdf notation** or **electron-in-boxes**. **Cr and Cu** are the exceptions."},
        {"type": "def", "term": "Aufbau principle",
         "text": "Electrons fill up the lowest energy orbital first."},
        {"type": "eq", "code": "1s  2s  2p  3s  3p  4s  3d  4p  …", "caption": "The order in which sub-shells fill"},
        {"type": "list", "items": [
            "Half-filled or completely filled sub-shells are **more stable** — that is why orbitals are not filled in numerical order.",
            "**4s is filled before 3d** — the 4s orbital sits at a lower energy level than the 3d.",
            "Shortened version: write the noble gas configuration in square brackets — e.g. **[Ne] 3s² 3p⁴**.",
        ]},
        {"type": "worked", "title": "Electronic configuration of carbon",
         "problem": "Write down the electronic configuration of ₆C using spdf notation and box notation.",
         "steps": [
             "Carbon has 6 electrons. Fill the lowest energy orbitals first: 1s, then 2s, then 2p.",
             "**spdf notation:** 1s² 2s² 2p²",
             "**Box notation:** 1s [↑↓] · 2s [↑↓] · 2p [↑] [↑] [ ] — the two 2p electrons sit in separate orbitals, singly, with parallel spins (Hund's rule).",
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
            "**Chromium:** 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹ — *not* 3d⁴ 4s².",
            "**Copper:** 1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s¹ — *not* 3d⁹ 4s².",
            "In both, one 4s electron is **donated to the 3d sub-shell** — making it **half filled (Cr) or completely filled (Cu)**, a more stable configuration.",
        ]},
        {"type": "h3", "text": "Electronic configuration of ions"},
        {"type": "list", "items": [
            "**Cations (positive ions)** — formed by **loss** of electrons · **anions (negative ions)** — formed by **gain** of electrons.",
        ]},
        {"type": "worked", "title": "Sodium atom and sodium ion",
         "problem": "Write down the electronic configuration of the sodium atom and the sodium ion using spdf notation.",
         "steps": [
             "Sodium atom, Na (Z = 11): 1s² 2s² 2p⁶ 3s¹",
             "The Na⁺ ion forms by **losing the single 3s electron**.",
         ],
         "answer": "Na⁺: 1s² 2s² 2p⁶ — the same configuration as neon"},
        {"type": "worked", "title": "Chlorine atom and chloride ion",
         "problem": "Write down the electronic configuration of the chlorine atom and the chloride ion using spdf notation.",
         "steps": [
             "Chlorine atom, Cl (Z = 17): 1s² 2s² 2p⁶ 3s² 3p⁵",
             "The Cl⁻ ion forms by **gaining one electron** into the last 3p orbital.",
         ],
         "answer": "Cl⁻: 1s² 2s² 2p⁶ 3s² 3p⁶ — the same configuration as argon"},
        {"type": "callout", "variant": "warning", "title": "Watch out",
         "text": "For ions, follow the worked pattern: Na⁺ forms by **losing the 3s electron**, Cl⁻ forms by **gaining into the last 3p orbital**. Cations = loss, anions = gain — never touch the nucleus."},
        {"type": "qa", "items": [
            {"q": "State the Aufbau principle.", "a": "Electrons **fill up the lowest energy orbital first**."},
            {"q": "Why is 4s filled before 3d?", "a": "The **4s orbital is at a lower energy level** than the 3d."},
            {"q": "Write the electronic configuration of chromium.", "a": "**1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s¹** — one 4s electron donated to make the 3d sub-shell half filled (more stable)."},
            {"q": "Write the configuration of Cu.", "a": "**1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s¹** — a completely filled 3d sub-shell is more stable."},
            {"q": "Na⁺ has the configuration of which noble gas?", "a": "**Neon** — 1s² 2s² 2p⁶."},
        ]},
    ],
}

SECTIONS_B = [S2_8, S2_9, S2_10, S2_11, S2_12, S2_13, S2_14]
