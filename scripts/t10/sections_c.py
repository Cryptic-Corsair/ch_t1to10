#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Topic 10 content — part C: 10.4 Mass spectra + 10.5 Infrared."""

S_104 = {
    "id": "cmv1eoi8l00g7jfqkemp1cg6c",
    "sectionKey": "mass-spectrometry",
    "number": "10.4",
    "title": "Mass Spectra of Molecules",
    "blurb": "Fragmentation patterns as molecular fingerprints.",
    "estMinutes": 30,
    "spec": "10.21",
    "specText": "be able to interpret data from mass spectra to suggest possible structures of simple organic compounds using the m/z of the molecular ion and fragmentation patterns",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key",
         "title": "Two clues, one spectrum: the M⁺ peak tells you the molecule's size, the fragment peaks tell you its pieces.",
         "text": "Match the pieces to a structure — that is the whole skill.",
         "style": "note"},

        {"type": "h3", "text": "The molecular ion"},
        {"type": "p",
         "text": "Inside the mass spectrometer (Topic 2), high-energy electrons bombarding the sample knock **one electron off** each molecule, making the **molecular ion**:"},
        {"type": "eq", "code": "M(g) → M⁺(g) + e⁻",
         "caption": "the molecular ion — its m/z equals the relative molecular mass, Mᵣ"},
        {"type": "list", "items": [
            "The peak at the **largest m/z** is the **molecular ion, M⁺**.",
            "Its **m/z value = the relative molecular mass (Mᵣ)** of the compound — size, straight away.",
        ]},

        {"type": "h3", "text": "The M+1 peak"},
        {"type": "list", "items": [
            "A small peak at **M+1** comes from **¹³C** — about **1.1%** of carbon atoms carry it (Topic 1).",
            "The height of the M+1 peak ≈ the **number of carbon atoms** in the molecule.",
        ]},

        {"type": "h3", "text": "Fragmentation"},
        {"type": "p",
         "text": "The bombardment is violent: some molecular ions **shake apart**. Each fragment that keeps the positive charge shows up as its own peak:"},
        {"type": "eq", "code": "M⁺ → fragment⁺ + radical",
         "caption": "only the charged fragments reach the detector — the radicals are lost"},
        {"type": "table",
         "headers": ["m/z", "Fragment", "Meaning"],
         "rows": [
             ["**15**", "**CH₃⁺**", "a methyl group broke off and kept the charge"],
             ["**29**", "**C₂H₅⁺**", "an ethyl group"],
             ["**43**", "**C₃H₇⁺**", "a propyl group"],
         ]},
        {"type": "p",
         "text": "Read each fragment as a subtraction: **fragment m/z = M − what broke off**. A peak at M − 15 means a CH₃ group left; a peak at M − 29 means C₂H₅ left. Rebuild the pieces into a structure that fits."},

        {"type": "h3", "text": "Worked example"},
        {"type": "worked",
         "title": "Same M⁺, different pieces",
         "problem": "Hydrocarbon A gives M⁺ at m/z 58, with strong peaks at 43 and 29 and a small one at 15. Its isomer B gives M⁺ at 58 too, but a dominant peak at 57. Suggest structures for A and B.",
         "steps": [
            "M⁺ = 58 → **Mᵣ 58** → the formula is **C₄H₁₀** — butane or methylpropane.",
            "Peak at **43** = 58 − 15: a **CH₃ group** broke off, leaving **C₃H₇⁺**.",
            "Peak at **29** = 58 − 29: the chain split in the middle, leaving **C₂H₅⁺** — the signature of the **straight chain**, butane CH₃CH₂CH₂CH₃.",
            "Isomer B's dominant peak at **57** = 58 − 15 means it mainly loses a methyl from a **central carbon** — the signature of the branched chain, **methylpropane** (CH₃)₃CH.",
         ],
         "answer": "A = butane (fragments at 43 and 29); B = methylpropane (dominant 57). Same M⁺, different fragmentation — the pieces tell the structures apart."},
        {"type": "figure", "src": "/diagrams/t10-mass-spectrum.png",
         "srcDark": "/diagrams/t10-mass-spectrum-dark.png",
         "alt": "Mass spectrum of butane with peaks at m/z 15, 29, 43 (base peak), 57, 58 (M+) and a tiny M+1 at 59",
         "caption": "Read right to left: M⁺ = 58 gives the size, then subtract to name each piece."},
        {"type": "callout", "variant": "tip",
         "title": "The reading order",
         "text": "**M⁺ first** (the size) → **M+1** (the carbon count) → **subtract each fragment** from M⁺ to see what broke off → **rebuild** the pieces into a structure.",
         "style": "note"},

        {"type": "qa", "items": [
            {"q": "What does the M⁺ peak tell you?",
             "a": "Its **m/z = the relative molecular mass** of the compound — the size of the molecule."},
            {"q": "Where does the M+1 peak come from?",
             "a": "**¹³C** — about 1.1% of carbon atoms. Its height ≈ the **number of carbon atoms**."},
            {"q": "A spectrum shows M⁺ = 46 and a strong peak at 31. What broke off?",
             "a": "46 − 31 = 15 — a **CH₃ group**. (The compound is ethanol: the 31 fragment is CH₂OH⁺, the piece that kept the charge.)"},
            {"q": "Two isomers share M⁺ = 58. How does the spectrum separate them?",
             "a": "By their **fragmentation patterns** — the straight chain splits in the middle (peak at 29); the branched isomer loses one methyl cleanly (dominant peak at 57)."},
        ]},
    ],
}


S_105 = {
    "id": "cmv1eoi8l00g9jfqkbtlusj9x",
    "sectionKey": "infrared-spectroscopy",
    "number": "10.5",
    "title": "Infrared Spectroscopy",
    "blurb": "Bonds vibrate at characteristic frequencies — and absorb IR.",
    "estMinutes": 30,
    "spec": "10.22 – 10.23",
    "specText": "be able to use infrared spectra, or data from infrared spectra, to deduce functional groups present in organic compounds, and predict infrared absorptions, given wavenumber data, due to familiar functional groups including C–H, C=C, O–H, C=O, C–X and N–H stretching absorptions",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key",
         "title": "Every bond vibrates at its own frequency — shine IR through a sample and each bond type absorbs at its own wavenumber.",
         "text": "The dips in the spectrum name the functional groups.",
         "style": "note"},

        {"type": "h3", "text": "How the spectrum forms"},
        {"type": "list", "items": [
            "Covalent bonds **vibrate** — stretching and bending — at **characteristic frequencies**.",
            "A bond **absorbs infrared radiation only when the frequency matches** one of its vibrations.",
            "Position is reported as **wavenumber in cm⁻¹** — higher wavenumber, higher frequency.",
            "The spectrum plots **transmittance against wavenumber**: each absorption shows as a **downward dip**.",
        ]},

        {"type": "h3", "text": "The absorptions to know"},
        {"type": "p",
         "text": "In the exam you are given wavenumber data — but recognising the famous ones on sight is what makes the data usable:"},
        {"type": "table",
         "headers": ["Bond", "Where it occurs", "Wavenumber / cm⁻¹", "Look for"],
         "rows": [
             ["**C–H**", "alkanes, alkenes, aldehydes", "2850 – 3300", "sharp"],
             ["**C=C**", "alkenes", "1620 – 1680", "sharp"],
             ["**C=O**", "aldehydes, ketones, carboxylic acids", "1630 – 1820", "**sharp and strong**"],
             ["**O–H**", "alcohols", "3200 – 3550", "**broad**"],
             ["**O–H**", "carboxylic acids", "2500 – 3300", "**very broad** — overlaps C–H"],
             ["**N–H**", "amines", "3300 – 3500", "sharp"],
             ["**C–X**", "halogenoalkanes", "about 500 – 800", "at the edge of the fingerprint"],
         ]},
        {"type": "callout", "variant": "tip",
         "title": "Two shapes are worth more than ten numbers",
         "text": "**Broad = O–H** (hydrogen bonding smears the absorption). **Sharp = C=O.** Broad 2500 – 3300 **plus** a sharp C=O together = a **carboxylic acid**.",
         "style": "note"},

        {"type": "h3", "text": "The fingerprint region"},
        {"type": "p",
         "text": "Below about **1500 cm⁻¹** the dip pattern is unique to each molecule — the **fingerprint region**. Identify a compound by matching its fingerprint against a known spectrum. It is also where the **C–X absorptions** of halogenoalkanes sit."},

        {"type": "h3", "text": "Worked example"},
        {"type": "worked",
         "title": "Deduce the functional groups",
         "problem": "A liquid's IR spectrum shows a strong sharp dip at 1715 cm⁻¹, a very broad absorption stretching from 2500 to 3300 cm⁻¹, and sharp dips near 2950 cm⁻¹. What is present?",
         "steps": [
            "**1715 cm⁻¹, sharp** — inside the **C=O** window (1630 – 1820).",
            "**2500 – 3300, very broad** — the **O–H of a carboxylic acid** (a plain alcohol's O–H would start at 3200).",
            "**2950, sharp** — ordinary **C–H**.",
         ],
         "answer": "**Carboxylic acid** — C=O + acid O–H + C–H. Consistent with ethanoic acid, CH₃COOH."},
        {"type": "figure", "src": "/diagrams/t10-ir-spectrum.png",
         "srcDark": "/diagrams/t10-ir-spectrum-dark.png",
         "alt": "Infrared spectrum with a broad O–H dip at 3200–3550, a sharp C–H dip near 2950, a deep sharp C=O dip at 1715 and the fingerprint region below 1500",
         "caption": "Each dip names a bond — broad O–H, sharp C=O, and the unique fingerprint below 1500 cm⁻¹."},

        {"type": "h3", "text": "IR and the greenhouse effect"},
        {"type": "p",
         "text": "The same physics runs the climate. **CO₂, H₂O vapour and CH₄** have bonds that vibrate at infrared frequencies — they **absorb the infrared radiation the Earth re-emits**, then re-radiate part of it back towards the surface. More of these gases, more trapped radiation: the **enhanced greenhouse effect** and global warming."},
        {"type": "callout", "variant": "tip",
         "title": "Same cause, different consequence",
         "text": "Lab spectroscopy and the greenhouse effect both come down to one idea: **bonds absorb IR at their vibration frequencies**.",
         "style": "note"},
        {"type": "p",
         "text": "**Core Practical 8** closes the topic: unknowns identified by combining the chemical tests from Topics 8 and 10 with **mass spectra** and **IR spectra** — exactly the toolkit this topic has built."},

        {"type": "qa", "items": [
            {"q": "Which absorptions identify an alcohol? An aldehyde?",
             "a": "Alcohol: **broad O–H at 3200 – 3550 cm⁻¹**. Aldehyde: **sharp C=O at 1630 – 1820 cm⁻¹**."},
            {"q": "What is the fingerprint region and what is it for?",
             "a": "Below about **1500 cm⁻¹** — a dip pattern **unique to each molecule**, used to identify a compound by matching to a known spectrum."},
            {"q": "How do greenhouse gases interact with infrared radiation?",
             "a": "Their bonds **vibrate at IR frequencies**, so **CO₂, H₂O and CH₄ absorb outgoing IR** and re-emit part of it back — the **enhanced greenhouse effect**."},
            {"q": "What does wavenumber measure?",
             "a": "The **frequency of vibration** a bond absorbs, in **cm⁻¹** — higher wavenumber, higher frequency."},
        ]},
    ],
}


SECTIONS_C = [S_104, S_105]
