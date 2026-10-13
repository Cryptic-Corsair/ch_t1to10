# -*- coding: utf-8 -*-
"""Topic 10 rebuild — section 10.22 rebuilt from the final source part
('Infrared with ans.pdf', specification objective 10.22).

Style matches the original topic versions; wording stays verbatim to the
source notes and keeps the approved mark-scheme vocabulary.
"""

S1022 = {
    "id": "cmv1eoi5t10r02200000",
    "sectionKey": "infrared-spectroscopy",
    "number": "10.22",
    "title": "Infrared Spectroscopy",
    "blurb": "Bonds absorb characteristic wavenumbers — the functional-group checker.",
    "estMinutes": 40,
    "spec": "10.22",
    "specText": "be able to use infrared spectra, or data from infrared spectra, to deduce functional groups present in organic compounds, and predict infrared absorptions, given wavenumber data, due to familiar functional groups including:",
    "outline": [
        "i    C–H stretching absorptions in alkanes, alkenes and aldehydes",
        "ii    C=C stretching absorption in alkenes",
        "iii    O–H stretching absorptions in alcohols and carboxylic acids",
        "iv    C=O stretching absorptions in aldehydes, ketones and carboxylic acids",
        "v    C–X stretching absorption in halogenoalkanes",
        "vi    N–H stretching absorption in amines",
    ],
    "content": [
        {"type": "p", "text": "Molecules are able to **convert energy from infra-red radiation into energy to vibrate their bonds**. Different bonds **absorb different frequencies** of infra-red radiation. An **infra-red spectrum** is obtained by **passing a range of infra-red frequencies through a compound**, producing **absorption peaks** — the frequencies of the absorption peaks are **matched to those of known bonds** to identify the structural features in an unknown molecule."},

        {"type": "h3", "text": "Why bonds absorb different frequencies"},
        {"type": "list", "items": [
            "Different covalent bonds have **different strengths**, due to the **masses of the different atoms** at either end of the bond.",
            "As a result, the bonds **vibrate at different frequencies**.",
            "The frequency of vibration is found by **detecting when the molecules absorb electromagnetic radiation**.",
            "Various types of vibration are possible — the two you need are **STRETCHING** and **BENDING**.",
        ]},
        {"type": "figure", "src": "/diagrams/t10-ir-vibrations.png", "srcDark": "/diagrams/t10-ir-vibrations-dark.png",
         "alt": "Three diagrams of a water molecule vibrating: symmetric stretching, bending and asymmetric stretching",
         "caption": "Stretching and bending — the two vibration types. Each absorbs its own frequency of infra-red radiation."},
        {"type": "callout", "variant": "key", "title": "Infra-red Spectroscopy is useful for identifying functional groups in a molecule",
         "text": "The peaks are matched to **known bonds** — the pattern of absorptions reveals which **functional groups** the molecule carries."},

        {"type": "h3", "text": "Reading the spectrum: the axes"},
        {"type": "list", "items": [
            "The spectrum is normally shown with the **vertical axis labelled transmittance**, shown as a **percentage from 0 to 100%**.",
            "A value of **100% transmittance** means that **100% of the radiation is transmitted** and **none is absorbed**.",
            "The **horizontal axis** could be labelled either as frequency or wavelength, but a different unit is used: **wavenumber**, in **cm⁻¹** — the **reciprocal of wavelength**.",
        ]},
        {"type": "figure", "src": "/diagrams/t10-ir-spectrum.png", "srcDark": "/diagrams/t10-ir-spectrum-dark.png",
         "alt": "An infrared spectrum with labelled absorption dips for O–H, C=O and C–H and the fingerprint region",
         "caption": "Each peak is characteristic of a vibration of a particular group — match the dips to the table of absorptions."},

        {"type": "h3", "text": "Different ways of using an infrared spectrum"},
        {"type": "list", "items": [
            "**Predicting the absorptions** in the spectrum of an organic compound.",
            "**Deducing the functional group** in a compound **from a list of wavenumbers**.",
            "**Deducing the structure** of a compound from **wavenumber data and the molecular formula**.",
        ]},

        {"type": "h3", "text": "Some important IR absorptions"},
        {"type": "table", "headers": ["Bond", "Functional group", "Wavenumber / cm⁻¹"], "rows": [
            ["**C–O**", "Alcohols, esters", "1000 – 1300 (strong absorption)"],
            ["**C=O**", "Aldehydes, ketones, carboxylic acids", "1680 – 1750 (strong absorption)"],
            ["**O–H**", "Hydrogen bonded in carboxylic acids", "2500 – 3300 (strong **and broad** absorption)"],
            ["**O–H**", "Hydrogen bonded in alcohols", "3230 – 3550 (strong **and broad** absorption)"],
            ["**N–H**", "Amine", "3500 – 3300"],
            ["**C=C**", "Alkene", "1669 – 1645"],
            ["**C–H**", "Alkanes", "2850 – 3000"],
            ["**=C–H**", "Alkenes", "3100 – 3000"],
            ["**C–H**", "Aldehydes", "a unique C–H peak just below 3000"],
            ["**C–F**", "Alkyl halides", "1400 – 1000"],
            ["**C–Cl**", "Alkyl halides", "800 – 600"],
            ["**C–Br**", "Alkyl halides", "600 – 500"],
            ["**C–I**", "Alkyl halides", "about 500"],
        ]},

        {"type": "h3", "text": "The fingerprint region"},
        {"type": "p", "text": "The **1500 cm⁻¹ to 400 cm⁻¹** region of an IR spectrum is called the **fingerprint region**. Each compound produces a **unique IR fingerprint pattern**, which can be used to:"},
        {"type": "list", "items": [
            "**Identify the compound** by comparison of an unknown with the spectra of known compounds, **using databases**.",
            "**Check the purity** of a compound, since **any small impurity present will produce additional peaks**.",
        ]},

        {"type": "h3", "text": "Interpreting infra-red spectra"},
        {"type": "p", "text": "An infra-red spectrum is particularly useful for identifying the **C=O** and the **O–H** bonds in compounds. Four families cover almost every question:"},
        {"type": "figure", "src": "/diagrams/t10-ir-examples.png", "srcDark": "/diagrams/t10-ir-examples-dark.png",
         "alt": "Four infrared spectra: butanone with C=O at 1740, ethanol with O–H at 3300 and C–O at 1010, propanoic acid with very broad O–H and C=O at 1680, propene with C=C and =C–H",
         "caption": "Butanone · ethanol · propanoic acid · propene — the four spectra to recognise on sight."},
        {"type": "list", "items": [
            "**Carbonyl compounds (aldehydes and ketones)** — e.g. butanone, CH₃COCH₂CH₃: a **C=O absorption from 1680 to 1750 cm⁻¹** (at **1740 cm⁻¹** in the spectrum), with the alkyl **C–H peaks at 3000 – 2850 cm⁻¹**.",
            "**Alcohols** — e.g. ethanol, CH₃CH₂OH: an **O–H absorption from 3230 to 3500 cm⁻¹** (at **3300 cm⁻¹**) and a **C–O absorption from 1000 to 1300 cm⁻¹** (at **1010 cm⁻¹**).",
            "**Carboxylic acids** — e.g. propanoic acid, CH₃CH₂COOH: a **very broad O–H absorption from 2500 to 3500 cm⁻¹**, the **C=O absorption at 1680 cm⁻¹** and **C–O absorptions at 1200 and 1030 cm⁻¹**.",
            "**Alkenes** — e.g. propene, CH₃CH=CH₂: the **C=C stretch from 1680 – 1640 cm⁻¹** and the **=C–H stretch from 3100 – 3000 cm⁻¹**.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Two shapes are worth more than ten numbers",
         "text": "A **broad** dip near 3230–3550 cm⁻¹ means **O–H (alcohol)**; a **sharp, strong** dip near 1700 cm⁻¹ means **C=O**. A **very broad** 2500–3300 cm⁻¹ dip **plus** a C=O dip means a **carboxylic acid** — the broadness of the O–H is what separates the acid from the alcohol."},

        {"type": "h3", "text": "Alkyl halides"},
        {"type": "list", "items": [
            "**C–H wag (–CH₂X)** from **1300 – 1150 cm⁻¹** — seen **only in terminal alkyl halides**.",
            "**C–X stretches (general)** from **850 – 515 cm⁻¹** — the **C–Cl stretch 850 – 550 cm⁻¹** and the **C–Br stretch 690 – 515 cm⁻¹**.",
            "In the spectrum of **1-chloro-2-methylpropane** the **C–Cl stretches absorb at 743 cm⁻¹**; in **1-bromopropane** the **C–Br stretch absorbs at 651 cm⁻¹**.",
        ]},

        {"type": "h3", "text": "Amines"},
        {"type": "list", "items": [
            "**N–H stretch 3400 – 3250 cm⁻¹**: a **primary (1°) amine shows two bands** (3400 – 3300 and 3330 – 3250 cm⁻¹); a **secondary (2°) amine one band** (3350 – 3310 cm⁻¹); a **tertiary (3°) amine no bands** in this region.",
            "**N–H bend (primary amines only)** from 1650 – 1580 cm⁻¹.",
            "**C–N stretch (aliphatic amines)** from 1250 – 1020 cm⁻¹.",
            "**N–H wag (primary and secondary amines only)** from 910 – 665 cm⁻¹.",
        ]},
        {"type": "figure", "src": "/diagrams/t10-ir-halides-amines.png", "srcDark": "/diagrams/t10-ir-halides-amines-dark.png",
         "alt": "Four infrared spectra: 1-chloro-2-methylpropane with C–Cl at 743, 1-bromopropane with C–Br at 651, diethylamine with one N–H band, triethylamine with no N–H stretch",
         "caption": "The C–X stretches sit below 850 cm⁻¹. The N–H region counts the hydrogen — one band, two bands, or none."},
        {"type": "callout", "variant": "exam", "title": "Triethylamine: note the absence of an N–H stretch",
         "text": "Triethylamine is a **tertiary amine** — its spectrum shows **no N–H stretch at all**, only the **C–N stretch at 1214 cm⁻¹**. Counting the N–H bands (two, one, none) is how the spectrum distinguishes **1°, 2° and 3° amines**."},

        {"type": "h3", "text": "Putting it to work"},
        {"type": "figure", "src": "/diagrams/t10-ir-q1.png", "srcDark": "/diagrams/t10-ir-q1-dark.png",
         "alt": "Three infrared spectra A, B and C, showing broad and sharp absorptions between 4000 and 650 wavenumbers",
         "caption": "Spectra A, B and C for the worked example — butanal, propanoic acid and butan-1-ol in some order."},
        {"type": "worked", "title": "Three spectra, three compounds", "problem": "IR spectra of three compounds — butanal, propanoic acid and butan-1-ol — are given above. Using the data in the absorption table, identify which spectrum corresponds to which compound and explain your reasoning.", "steps": [
            "**Spectrum A**: a **broad O–H absorption at 3500 – 2500 cm⁻¹** together with **C=O at 1680 cm⁻¹** and **C–O at 1000 – 1300 cm⁻¹** — a carboxylic acid.",
            "**Spectrum B**: **C–H at 3000 cm⁻¹** and a **C=O at 1700 cm⁻¹**, but **no O–H** — an aldehyde.",
            "**Spectrum C**: **O–H at 3200 – 3500 cm⁻¹**, **C–H at 3000 cm⁻¹** and **C–O at 1010 cm⁻¹**, with no C=O — an alcohol.",
        ], "answer": "A = propanoic acid · B = butanal · C = butan-1-ol."},
        {"type": "worked", "title": "IR and the mass spectrum together", "problem": "Compound D is found to have a relative molecular mass of 60. Its infra-red spectrum shows a smooth, narrow O–H absorption at 3200 – 3500 cm⁻¹ and a C–H absorption at 3000 cm⁻¹. The mass spectrum of D has peaks at m/z 60, 31 and 29. Identify the characteristic absorptions and the species producing each m/z peak, and draw the structural formula of D.", "steps": [
            "The **O–H at 3200 – 3500 cm⁻¹** and the **C–H at 3000 cm⁻¹** identify an **alcohol** — narrow O–H, no C=O.",
            "m/z **60** → **CH₃CH₂CH₂OH⁺** — the **molecular ion**, Mᵣ 60.",
            "m/z **31** → **CH₂OH⁺** · m/z **29** → **CH₃CH₂⁺** — the fragments.",
        ], "answer": "D is propan-1-ol, CH₃CH₂CH₂OH — O–H and C–H in the IR, molecular ion at 60, fragments at 31 and 29."},
        {"type": "worked", "title": "The amine from nucleophilic substitution", "problem": "The infra-red spectrum below was obtained from the product of nucleophilic substitution with alcoholic ammonia; its molecular formula is C₄H₁₁N. Identify the characteristic absorptions and name the functional group present.", "steps": [
            "**Two N–H bands**, at 3400 – 3300 and 3300 – 3250 cm⁻¹ — a **primary (1°) amine**.",
            "**C–H at 3000 cm⁻¹** and an **N–H wag** in the 910 – 665 cm⁻¹ region.",
            "C₄H₁₁N carrying a primary amine group — the carbon chain from the substitution of a halogenoalkane by ammonia.",
        ], "answer": "A primary amine — butan-1-amine, CH₃CH₂CH₂CH₂NH₂."},
        {"type": "worked", "title": "No Fehling's reaction means the C=O is a ketone", "problem": "The mass spectrum and IR spectrum of compound S are shown. S shows no reaction with Fehling's solution. Identify S and explain. (Mass spectrum peaks: m/z 15, 29, 43, 57, 72; IR: C–H and a strong C=O.)", "steps": [
            "The IR shows a **C=O**, yet S gives **no reaction with Fehling's solution** — so the carbonyl is a **ketone**, not an aldehyde.",
            "Fragments: **15 CH₃⁺ · 29 CH₃CH₂⁺ · 43 CH₃CO⁺ · 57 CH₃CH₂CO⁺** — and the molecular ion at **72, CH₃CH₂COCH₃⁺** (Mᵣ 72).",
        ], "answer": "S is butan-2-one, CH₃CH₂COCH₃ — a ketone, which is why Fehling's solution gives no reaction."},
        {"type": "worked", "title": "Four isomers, three quick answers", "problem": "This question is about two isomeric alcohols and two isomeric carbonyl compounds: propan-1-ol, CH₃CH₂CH₂OH · propan-2-ol, CH₃CH(OH)CH₃ · propanal, CH₃CH₂CHO · propanone, CH₃COCH₃. (a) Which would not produce a colour change when heated with acidified sodium dichromate(VI) solution? (b) Which pair would you expect to both have a peak at m/z = 29? (c) Which would give a peak at m/z = 31?", "steps": [
            "(a) Ketones are **not easily oxidised** — **propanone** produces no colour change with acidified sodium dichromate(VI).",
            "(b) m/z 29 is **CH₃CH₂⁺** — carried by both **propan-1-ol** and **propanal**.",
            "(c) m/z 31 is **CH₂OH⁺** — only **propan-1-ol** has a terminal CH₂OH group.",
        ], "answer": "(a) propanone · (b) propan-1-ol and propanal · (c) propan-1-ol."},

        {"type": "callout", "variant": "tip", "title": "The same physics, outside the lab",
         "text": "**CO₂, H₂O vapour and CH₄** absorb outgoing infrared radiation through their **bond vibrations** — the cause of the **enhanced greenhouse effect**."},
    ],
}

NEW_CARDS = [
    (17, "CORE", "What is the fingerprint region of an IR spectrum, and what is it used for?",
     "The region from 1500 to 400 cm⁻¹. Each compound produces a unique IR fingerprint pattern, used to identify the compound by comparison with the spectra of known compounds using databases, and to check purity — any small impurity present produces additional peaks."),
    (18, "EXAM", "How would you use IR spectra to tell an aldehyde, an alcohol and a carboxylic acid apart?",
     "Aldehyde: strong C=O (1680–1750 cm⁻¹) and no O–H. Alcohol: broad O–H (3230–3550 cm⁻¹) plus C–O (1000–1300 cm⁻¹), no C=O. Carboxylic acid: a very broad O–H reaching down to 2500–3300 cm⁻¹ together with the C=O. The shape of the O–H dip separates the acid from the alcohol."),
    (19, "CORE", "How do N–H stretches distinguish primary, secondary and tertiary amines?",
     "Primary (1°) amine: two N–H bands, 3400–3300 and 3330–3250 cm⁻¹. Secondary (2°) amine: one band, 3350–3310 cm⁻¹. Tertiary (3°) amine: no bands in this region — like triethylamine, which shows no N–H stretch at all."),
]
