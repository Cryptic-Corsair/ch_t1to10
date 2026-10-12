# -*- coding: utf-8 -*-
"""Topic 10 rebuild — sections 10.15 – 10.23 (10C Alcohols, 10D Mass spectra and IR).

Style matches the original topic versions; wording stays verbatim to the
specification statements and keeps the approved mark-scheme vocabulary.
"""


def _sec(i, key, number, title, blurb, est, spec, specText, outline, content):
    return {
        "id": f"cmv1eoi5t10r{i:03d}00000",
        "sectionKey": key,
        "number": number,
        "title": title,
        "blurb": blurb,
        "estMinutes": est,
        "spec": spec,
        "specText": specText,
        "outline": outline,
        "content": content,
    }


S1015 = _sec(
    15, "alcohols-nomenclature", "10.15", "Alcohols: Nomenclature and Formulae",
    "The –OH group, the -ol suffix and the position number.",
    15, "10.15", "understand the nomenclature of alcohols and be able to draw their structural, displayed and skeletal formulae",
    [],
    [
        {"type": "def", "term": "Alcohols", "text": "**Alcohols** carry a **hydroxyl group, –OH**, attached to a saturated carbon chain. They take the suffix **-ol** with a **position number** showing which carbon bears the –OH group."},
        {"type": "list", "items": [
            "With only **two carbons**, no locant is needed: **ethanol**, CH₃CH₂OH — the same rule as the halogenoalkanes.",
            "Draw them as **structural** (CH₃CH₂CH₂OH), **displayed** (every bond drawn) and **skeletal** (zig-zag) formulae, exactly as in Topic 4 — skeletal formulae never hide the **oxygen atom**.",
        ]},
        {"type": "table", "headers": ["Formula", "Name"], "rows": [
            ["CH₃OH", "methanol"],
            ["CH₃CH₂OH", "ethanol"],
            ["CH₃CH₂CH₂OH", "propan-1-ol"],
            ["CH₃CH(OH)CH₃", "propan-2-ol"],
            ["(CH₃)₃COH", "2-methylpropan-2-ol"],
        ]},
    ],
)

S1016 = _sec(
    16, "alcohol-classes", "10.16", "Primary, Secondary and Tertiary Alcohols",
    "The same counting rule as the halogenoalkanes.",
    10, "10.16", "understand the distinction between primary, secondary and tertiary alcohols",
    [],
    [
        {"type": "p", "text": "Alcohols are classified by the **number of alkyl groups attached to the carbon that carries the –OH group**:"},
        {"type": "table", "headers": ["Class", "The C–OH carbon is joined to", "Example"], "rows": [
            ["**Primary (1°)**", "**one** alkyl group", "ethanol, butan-1-ol"],
            ["**Secondary (2°)**", "**two** alkyl groups", "propan-2-ol"],
            ["**Tertiary (3°)**", "**three** alkyl groups", "2-methylpropan-2-ol"],
        ]},
        {"type": "figure", "src": "/diagrams/t10-alcohol-classes.png", "srcDark": "/diagrams/t10-alcohol-classes-dark.png",
         "alt": "General structures of primary, secondary and tertiary alcohols with examples",
         "caption": "One, two or three alkyl groups on the carbon holding the –OH — the class that decides the oxidation products."},
        {"type": "p", "text": "The class matters because it decides what oxidation gives (section 10.18): primary alcohols give aldehydes and carboxylic acids, secondary alcohols give ketones — and tertiary alcohols are **not oxidised** under these conditions."},
    ],
)

S1017 = _sec(
    17, "alcohol-reactions", "10.17", "Reactions of Alcohols",
    "Combustion, three halogenating agents, and elimination to an alkene.",
    25, "10.17",
    "understand the reactions of alcohols with:",
    [
        "i    oxygen in air (combustion)",
        "ii    halogenating agents",
        "•    PCl5 to produce chloroalkanes (including its use as a qualitative test for the presence of the –OH group)",
        "•    50% concentrated sulfuric acid and potassium bromide to produce bromoalkanes",
        "•    red phosphorus and iodine to produce iodoalkanes",
        "iii    concentrated phosphoric acid to form alkenes by elimination",
        "Descriptions of the mechanisms of these reactions are not required.",
    ],
    [
        {"type": "h3", "text": "Combustion"},
        {"type": "p", "text": "Alcohols burn in air (**combustion**). Complete combustion gives **carbon dioxide and water**:"},
        {"type": "eq", "code": "C₂H₅OH  +  3O₂  →  2CO₂  +  3H₂O", "caption": "Complete combustion of ethanol."},
        {"type": "h3", "text": "Halogenating agents — swap the –OH for a halogen"},
        {"type": "table", "headers": ["Reagent", "Product", "Remember"], "rows": [
            ["**PCl₅**", "chloroalkane", "also a **qualitative test for the –OH group**"],
            ["**50% concentrated H₂SO₄ + KBr**", "bromoalkane", "the acid and potassium bromide supply HBr"],
            ["**red phosphorus + iodine**", "iodoalkane", ""],
        ]},
        {"type": "eq", "code": "C₂H₅OH  +  PCl₅  →  C₂H₅Cl  +  POCl₃  +  HCl", "caption": "Misty fumes of HCl are given off — a positive test for the presence of the –OH group."},
        {"type": "h3", "text": "Elimination — forming an alkene"},
        {"type": "list", "items": [
            "Hot **concentrated phosphoric acid** (a catalyst) forms **alkenes by elimination** of water from the alcohol.",
        ]},
        {"type": "eq", "code": "C₂H₅OH  →  CH₂=CH₂  +  H₂O", "caption": "Ethanol → ethene with concentrated H₃PO₄."},
        {"type": "callout", "variant": "tip", "title": "Not required", "text": "**Descriptions of the mechanisms of these reactions are not required** by the specification — products, reagents and conditions are what earn the marks."},
    ],
)

S1018 = _sec(
    18, "oxidation-of-alcohols", "10.18", "Oxidation of Alcohols",
    "Dichromate decides by class — and by distil-or-reflux.",
    28, "10.18",
    "understand that potassium dichromate(VI) in dilute sulfuric acid can oxidise:",
    [
        "i    primary alcohols to produce aldehydes (which give a positive result with Benedict's or Fehling's solution) if the product is distilled as it forms",
        "ii    primary alcohols to produce carboxylic acids (which give a positive result with sodium carbonate or sodium hydrogencarbonate) if the reagents are heated under reflux",
        "iii    secondary alcohols to produce ketones",
        "In equations, the oxidising agent can be represented by [O].",
    ],
    [
        {"type": "p", "text": "The oxidising agent is **potassium dichromate(VI), K₂Cr₂O₇, in dilute sulfuric acid**. In equations it is written **[O]**. The **class** of the alcohol and the **apparatus** decide the product."},
        {"type": "figure", "src": "/diagrams/t10-oxidation-flow.png", "srcDark": "/diagrams/t10-oxidation-flow-dark.png",
         "alt": "Flow diagram: primary alcohol to aldehyde by distillation then to carboxylic acid by reflux; secondary alcohol to ketone; tertiary alcohol not oxidised",
         "caption": "Primary → aldehyde → carboxylic acid; secondary → ketone; tertiary stops."},
        {"type": "h3", "text": "Primary → aldehyde (distil as it forms)"},
        {"type": "list", "items": [
            "If the product is **distilled as it forms**, the oxidation stops at the **aldehyde** — aldehydes give a **positive result with Benedict's or Fehling's solution**.",
        ]},
        {"type": "eq", "code": "CH₃CH₂CH₂OH  +  [O]  →  CH₃CH₂CHO  +  H₂O", "caption": "Propan-1-ol → propanal."},
        {"type": "h3", "text": "Primary → carboxylic acid (heat under reflux)"},
        {"type": "list", "items": [
            "If the reagents are **heated under reflux**, the aldehyde stays in the mixture and oxidation continues to the **carboxylic acid** — carboxylic acids give a **positive result with sodium carbonate or sodium hydrogencarbonate** (effervescence of CO₂).",
        ]},
        {"type": "eq", "code": "CH₃CH₂CHO  +  [O]  →  CH₃CH₂COOH", "caption": "Propanal → propanoic acid."},
        {"type": "h3", "text": "Secondary → ketone"},
        {"type": "eq", "code": "CH₃CHOHCH₃  +  [O]  →  CH₃COCH₃  +  H₂O", "caption": "Propan-2-ol → propanone — there is no further oxidation."},
        {"type": "list", "items": [
            "**Tertiary alcohols are not oxidised** — the orange dichromate stays orange.",
        ]},
        {"type": "table", "headers": ["Class", "Product", "Condition", "Positive test"], "rows": [
            ["Primary", "**aldehyde**", "**distil as it forms**", "Benedict's or Fehling's solution"],
            ["Primary", "**carboxylic acid**", "**heat under reflux**", "sodium carbonate / sodium hydrogencarbonate"],
            ["Secondary", "**ketone**", "reflux", "—"],
            ["Tertiary", "no oxidation", "—", "dichromate stays orange"],
        ]},
        {"type": "callout", "variant": "exam", "title": "Two phrases carry the marks", "text": "**‘distilled as it forms’** → aldehyde; **‘heated under reflux’** → carboxylic acid. Quote the colour change too: **orange dichromate to green** (Cr₂O₇²⁻ → Cr³⁺)."},
    ],
)

S1019 = _sec(
    19, "preparation-and-purification", "10.19", "Preparation and Purification of a Liquid Organic Compound",
    "Five techniques, in the order a preparation uses them.",
    20, "10.19",
    "understand, the following techniques in the preparation and purification of a liquid organic compound:",
    [
        "i    heating under reflux",
        "ii    extraction with a solvent using a separating funnel",
        "iii    distillation",
        "iv    drying with an anhydrous salt",
        "v    boiling temperature determination",
    ],
    [
        {"type": "p", "text": "The specification names **five techniques** for the preparation and purification of a liquid organic compound. In a preparation they usually run in this order:"},
        {"type": "list", "items": [
            "**Heating under reflux** — boil the reaction mixture and condense the vapour **back into the flask continuously**, so volatile reagents are not lost and the heating can be carried out for a longer period of time.",
            "**Distillation** — the liquid with the **lowest boiling temperature distils over first**; collect the fraction that is your product (this is how an aldehyde is distilled as it forms, section 10.18).",
            "**Extraction with a solvent using a separating funnel** — shake the product with an **immiscible solvent**; the layers separate and the layer holding the product can be **run off**.",
            "**Drying with an anhydrous salt** — an **anhydrous** (water-free) salt **binds the traces of water** left in the organic liquid; the dried liquid is then decanted off.",
            "**Boiling temperature determination** — a **pure liquid boils at a fixed temperature**; a sharp, steady boiling temperature confirms the identity and purity of the product.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Why reflux first, distil later", "text": "**Reflux** keeps everything in the flask so the reaction goes to completion; **distillation** then separates the product by its boiling temperature. Same apparatus idea, two different jobs."},
    ],
)

S1020 = _sec(
    20, "core-practical-7", "10.20", "Core Practical 7: Oxidation of Propan-1-ol",
    "One alcohol, two techniques, two different products.",
    15, "10.20",
    "CORE PRACTICAL 7\nThe oxidation of propan-1-ol to produce propanal and propanoic acid.",
    [
        "Further suggested practical:",
        "Investigation of reactions of primary and secondary alcohols, including propan-1-ol and propan-2-ol",
    ],
    [
        {"type": "p", "text": "**Core Practical 7** oxidises **propan-1-ol** with acidified **potassium dichromate(VI)** to produce **propanal** and **propanoic acid** — which one you get depends on the apparatus:"},
        {"type": "list", "items": [
            "**Distil the product as it forms** → **propanal** (the aldehyde) — it leaves the reaction mixture before it can be oxidised further.",
            "**Heat under reflux** → **propanoic acid** (the carboxylic acid) — the aldehyde stays in contact with the oxidising agent.",
        ]},
        {"type": "eq", "code": "CH₃CH₂CH₂OH  +  [O]  →  CH₃CH₂CHO  +  H₂O", "caption": "Then, under reflux: CH₃CH₂CHO + [O] → CH₃CH₂COOH."},
        {"type": "list", "items": [
            "Check which product you have: propanal gives a **positive Benedict's or Fehling's** test; propanoic acid **effervesces with sodium carbonate or sodium hydrogencarbonate**.",
            "The preparation runs through the techniques of section 10.19: **reflux → distillation → extraction → drying → boiling temperature**.",
        ]},
        {"type": "p", "text": "Further suggested practical: investigating the reactions of **primary and secondary alcohols**, including propan-1-ol and propan-2-ol."},
    ],
)

S1021 = _sec(
    21, "mass-spectra", "10.21", "Mass Spectra of Organic Compounds",
    "The molecular ion gives Mᵣ — the fragments give the structure.",
    22, "10.21", "be able to interpret data from mass spectra to suggest possible structures of simple organic compounds using the m/z of the molecular ion and fragmentation patterns",
    [],
    [
        {"type": "p", "text": "Inside the **mass spectrometer** (Topic 2), high-energy electrons knock an electron off the molecule, forming the **molecular ion**:"},
        {"type": "eq", "code": "M(g)  →  M⁺(g)  +  e⁻", "caption": "The molecular ion — its m/z equals the relative molecular mass, Mᵣ."},
        {"type": "list", "items": [
            "The **molecular ion peak (M⁺)** has the **largest m/z** in the cluster — its m/z gives the **relative molecular mass** of the compound.",
            "A small **M+1 peak** appears because about **1.1% of carbon atoms are ¹³C**.",
            "The bombardment is violent: some molecular ions **shake apart (fragment)**:",
        ]},
        {"type": "eq", "code": "M⁺  →  fragment⁺  +  radical", "caption": "Only the charged fragments are detected — the radical is lost."},
        {"type": "table", "headers": ["m/z", "Fragment", "Meaning"], "rows": [
            ["**15**", "**CH₃⁺**", "a methyl group broke off and kept the charge"],
            ["**29**", "**C₂H₅⁺**", "an ethyl group"],
            ["**43**", "**C₃H₇⁺**", "a propyl group"],
        ]},
        {"type": "p", "text": "Read every fragment as a subtraction: **fragment m/z = M − the piece that was lost**. Matching the fragments to possible structures is how you **suggest possible structures** of the compound from its spectrum."},
        {"type": "worked", "title": "Same M⁺, different pieces", "problem": "Hydrocarbon A gives M⁺ at m/z 58, with strong peaks at 43 and 29 and a small one at 15. Its isomer B gives M⁺ at 58 too, but a dominant peak at 57. Suggest structures for A and B.", "steps": [
            "M⁺ = 58 → **Mᵣ 58** → the formula is **C₄H₁₀** — butane or methylpropane.",
            "Peak at **43** = 58 − 15: a **CH₃ group** broke off, leaving **C₃H₇⁺**.",
            "Peak at **29** = 58 − 29: the chain split in the middle, leaving **C₂H₅⁺** — the signature of the **straight chain**, butane CH₃CH₂CH₂CH₃.",
            "Isomer B's dominant peak at **57** = 58 − 15 means it mainly loses a methyl from a **central carbon** — the signature of the branched chain, **methylpropane** (CH₃)₃CH.",
        ], "answer": "A = butane (fragments at 43 and 29); B = methylpropane (dominant fragment at 57)."},
        {"type": "figure", "src": "/diagrams/t10-mass-spectrum.png", "srcDark": "/diagrams/t10-mass-spectrum-dark.png",
         "alt": "A mass spectrum showing the molecular ion peak, M+1 peak and fragment peaks",
         "caption": "Read right to left: the molecular ion gives Mᵣ, then subtract the fragments to rebuild the molecule."},
    ],
)

S1022 = _sec(
    22, "infrared-spectroscopy", "10.22", "Infrared Spectroscopy",
    "Bonds absorb characteristic wavenumbers — the functional-group checker.",
    20, "10.22",
    "be able to use infrared spectra, or data from infrared spectra, to deduce functional groups present in organic compounds, and predict infrared absorptions, given wavenumber data, due to familiar functional groups including:",
    [
        "i    C–H stretching absorptions in alkanes, alkenes and aldehydes",
        "ii    C=C stretching absorption in alkenes",
        "iii    O–H stretching absorptions in alcohols and carboxylic acids",
        "iv    C=O stretching absorptions in aldehydes, ketones and carboxylic acids",
        "v    C–X stretching absorption in halogenoalkanes",
        "vi    N–H stretching absorption in amines",
    ],
    [
        {"type": "list", "items": [
            "Covalent bonds **vibrate** at characteristic frequencies.",
            "A bond **absorbs infrared radiation** whose frequency matches one of its vibrations — the spectrum plots **absorbance against wavenumber (cm⁻¹)**.",
            "You are **given wavenumber data** in the exam — use it to **deduce the functional groups** present and to **predict infrared absorptions**.",
        ]},
        {"type": "table", "headers": ["Bond", "Where it occurs", "Wavenumber / cm⁻¹", "Look for"], "rows": [
            ["**C–H**", "alkanes, alkenes, aldehydes", "2850 – 3300", "sharp"],
            ["**C=C**", "alkenes", "1620 – 1680", "sharp"],
            ["**C=O**", "aldehydes, ketones, carboxylic acids", "1630 – 1820", "**sharp and strong**"],
            ["**O–H**", "alcohols", "3200 – 3550", "**broad**"],
            ["**O–H**", "carboxylic acids", "2500 – 3300", "**very broad** — overlaps C–H"],
            ["**N–H**", "amines", "3300 – 3500", "sharp"],
            ["**C–X**", "halogenoalkanes", "about 500 – 800", "at the edge of the fingerprint"],
        ]},
        {"type": "figure", "src": "/diagrams/t10-ir-spectrum.png", "srcDark": "/diagrams/t10-ir-spectrum-dark.png",
         "alt": "An infrared spectrum with labelled absorption dips for O–H, C=O and C–H and the fingerprint region",
         "caption": "Each dip is a bond absorbing at its vibration frequency — match the dips to the table."},
        {"type": "h3", "text": "The fingerprint region"},
        {"type": "list", "items": [
            "Below about **1500 cm⁻¹** the absorption pattern is unique to each compound — the **fingerprint** used to match a spectrum against known ones.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Two shapes are worth more than ten numbers", "text": "A **broad** dip near 3200–3550 cm⁻¹ means **O–H (alcohol)**; a **sharp, strong** dip near 1700 cm⁻¹ means **C=O**. A very broad 2500–3300 cm⁻¹ dip **plus** a C=O dip suggests a **carboxylic acid**."},
        {"type": "callout", "variant": "tip", "title": "The same physics, outside the lab", "text": "**CO₂, H₂O vapour and CH₄** absorb outgoing infrared radiation through their **bond vibrations** — the cause of the **enhanced greenhouse effect**."},
    ],
)

S1023 = _sec(
    23, "core-practical-8", "10.23", "Core Practical 8: Analysis of Unknowns",
    "Combine the spectra and the test-tube observations.",
    12, "10.23", "CORE PRACTICAL 8\nAnalysis of some inorganic and organic unknowns.",
    [],
    [
        {"type": "p", "text": "**Core Practical 8** analyses **inorganic and organic unknowns** by combining the evidence of this topic — no single technique is conclusive on its own:"},
        {"type": "list", "items": [
            "**Mass spectrum** — the **molecular ion m/z** gives the Mᵣ; the **fragmentation pattern** suggests the carbon skeleton (section 10.21).",
            "**Infrared spectrum** — the positions and shapes of the absorptions **deduce the functional groups** present (section 10.22).",
            "**Silver nitrate test** — the **precipitate colour** identifies the halogen in a halogenoalkane: white AgCl, cream AgBr, yellow AgI (section 10.10).",
            "**Oxidation tests** — **Benedict's or Fehling's solution** for an aldehyde; **sodium carbonate or sodium hydrogencarbonate** effervescence for a carboxylic acid (section 10.18).",
        ]},
        {"type": "p", "text": "Match **all** the evidence — molecular mass, fragments, functional groups and test-tube observations — before naming the unknown."},
    ],
)

SECTIONS_O3 = [S1015, S1016, S1017, S1018, S1019, S1020, S1021, S1022, S1023]
