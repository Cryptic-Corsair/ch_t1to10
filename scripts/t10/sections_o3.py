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
    "The –OH group, the -ol suffix, the bond angles and the position number.",
    25, "10.15", "understand the nomenclature of alcohols and be able to draw their structural, displayed and skeletal formulae",
    [],
    [
        {"type": "def", "term": "Alcohols", "text": "**Alcohols** have the **general formula CₙH₂ₙ₊₁OH**. The **functional group is –OH**. They are **good organic solvents**, and are also used as **raw materials in organic synthesis**."},
        {"type": "h3", "text": "Bond angles in alcohols"},
        {"type": "list", "items": [
            "All the **H–C–H bonds** and the **C–C–O** bonds are **109.5°** (**tetrahedral shape**) — there are **4 bond pairs of electrons** repelling to a position of **minimum repulsion**.",
            "The **H–O–C bond is 104.5°** (**bent line shape**) — the oxygen has **2 bond pairs and 2 lone pairs**. **Lone pairs repel more than bond pairs**, so the bond angle is reduced.",
        ]},
        {"type": "h3", "text": "Naming an alcohol"},
        {"type": "p", "text": "In the IUPAC system:"},
        {"type": "list", "items": [
            "Identify the **longest chain of carbon atoms containing the –OH group**.",
            "To show that the compound is an alcohol, the **suffix –e of the parent alkane is changed to -ol**.",
            "The **carbon number is added** to show the **location of the –OH group**. **No locant is needed with only two carbons** — with longer chains, a locant tells us where on the chain the –OH group is situated.",
        ]},
        {"type": "table", "headers": ["Compound", "Name"], "rows": [
            ["CH₃OH", "methanol"],
            ["CH₃CH₂OH", "ethanol"],
            ["CH₃CH₂CH₂OH", "propan-1-ol"],
            ["CH₃CH(OH)CH₃", "propan-2-ol"],
        ]},
        {"type": "h3", "text": "Branched chains"},
        {"type": "p", "text": "If the carbon chain is branched, the **longest continuous carbon chain containing the –OH group** is given the **parent name**, and the side chains are named as **alkyl groups**."},
        {"type": "worked", "title": "Name it step by step", "problem": "Name the alcohol CH₃CH(OH)CH(CH₃)CH₃.", "steps": [
            "**Parent chain: butane** — the longest chain containing the –OH group has four carbons.",
            "**–OH group location: 2** — the –OH sits on carbon 2 (counting from the nearer end).",
            "**Substituents location: 3-methyl** — a methyl group on carbon 3.",
            "The alkane name is **3-methylbutane**, so the alcohol name is **3-methylbutan-2-ol**.",
        ], "answer": "3-methylbutan-2-ol"},
        {"type": "h3", "text": "More than one –OH group"},
        {"type": "list", "items": [
            "If there is **more than one –OH group**, use **di-, tri-, tetra-**, with **locants** to say where they are.",
            "In this case the **root word ends with ‘ane’**: CH₃CH(OH)CH(OH)CH₃ is **butane-2,3-diol**.",
        ]},
        {"type": "h3", "text": "The three formulae"},
        {"type": "list", "items": [
            "**Structural** — atoms in order, bonds implied: CH₃CH₂CH₂OH.",
            "**Displayed** — **every bond drawn** out, atom by atom.",
            "**Skeletal** — the zig-zag line drawing; carbons at every bend and end, hydrogens left out — but the **O–H is always shown**.",
        ]},
    ],
)

S1016 = _sec(
    16, "alcohol-classes", "10.16", "Primary, Secondary and Tertiary Alcohols",
    "Count the alkyl groups on the C–OH carbon — the class decides the oxidation.",
    18, "10.16", "understand the distinction between primary, secondary and tertiary alcohols",
    [],
    [
        {"type": "p", "text": "Alcohols are **classified into different classes depending on how the –OH group is positioned on the chain of carbon atoms**. The **chemical behaviour, especially oxidation, often depends on the structural type**."},
        {"type": "table", "headers": ["Class", "The carbon carrying the –OH is…", "Examples"], "rows": [
            ["**Primary (1°)**", "**only attached to one alkyl group**", "ethanol, propan-1-ol, 2-methylpropan-1-ol"],
            ["**Secondary (2°)**", "**joined directly to two alkyl groups**", "propan-2-ol, butan-2-ol, pentan-3-ol"],
            ["**Tertiary (3°)**", "**joined directly to three alkyl groups**", "2-methylpropan-2-ol, 2-methylbutan-2-ol"],
        ]},
        {"type": "figure", "src": "/diagrams/t10-alcohol-classes.png", "srcDark": "/diagrams/t10-alcohol-classes-dark.png",
         "alt": "General structures of primary, secondary and tertiary alcohols with examples",
         "caption": "One, two or three alkyl groups on the carbon holding the –OH — the class that decides the oxidation products (section 10.18)."},
        {"type": "h3", "text": "Melting and boiling temperatures"},
        {"type": "list", "items": [
            "Alcohols have melting and boiling temperatures **much higher than those of alkanes and haloalkanes of comparable relative molecular mass**.",
            "Alcohols form **hydrogen bonding between molecules**, while only **weak London forces** exist between alkanes and **dipole–dipole forces** between haloalkanes.",
            "Since **hydrogen bonding is stronger, it requires more energy to break the bonds**.",
        ]},
        {"type": "h3", "text": "Solubility"},
        {"type": "list", "items": [
            "Alcohols with **relatively short carbon chains dissolve in water** — they form **hydrogen bonds with water**, which is stronger than the **London forces between the carbon chains** of the alcohols.",
            "Solubility in water **gradually decreases with increasing carbon chain length** — the **non-polar group becomes bigger**, increasing the strength of the London forces between the carbon chains.",
            "**More than one –OH group in the molecule increases solubility**, since **more hydrogen bonds** can be formed between the alcohol and water.",
        ]},
        {"type": "table", "headers": ["Alcohol", "Solubility in water"], "rows": [
            ["methanol", "**very soluble**"],
            ["butanol", "**slightly soluble**"],
            ["octanol", "**very insoluble**"],
        ]},
    ],
)

S1017 = _sec(
    17, "alcohol-reactions", "10.17", "Reactions of Alcohols",
    "Combustion, three halogenating agents, and dehydration to an alkene.",
    40, "10.17",
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
        {"type": "list", "items": [
            "**Alcohols make useful fuels** — like almost all organic chemicals, they **burn in oxygen to form carbon dioxide and water**.",
        ]},
        {"type": "eq", "code": "C₂H₅OH(l)  +  3O₂(g)  →  2CO₂(g)  +  3H₂O(l)", "caption": "Complete combustion of ethanol."},
        {"type": "h3", "text": "Halogenating agents — replace the –OH with a halogen"},
        {"type": "p", "text": "In **halogenation** reactions, the **–OH group of the alcohol molecule is replaced by a halogen atom**."},
        {"type": "table", "headers": ["Reagent", "Condition", "Reaction type", "Product"], "rows": [
            ["**PCl₅** (primary and secondary alcohols)", "room temperature", "substitution", "**chloroalkane**"],
            ["**concentrated HCl** (tertiary alcohols)", "room temperature", "substitution", "**chloroalkane**"],
            ["**KBr + 50% concentrated H₂SO₄**", "heat under reflux", "substitution", "**bromoalkane**"],
            ["**iodine + moist red phosphorus**", "warm", "substitution", "**iodoalkane**"],
        ]},
        {"type": "h3", "text": "Chlorination"},
        {"type": "eq", "code": "CH₃CH₂OH  +  PCl₅  →  CH₃CH₂Cl  +  POCl₃  +  HCl", "caption": "Primary and secondary alcohols + PCl₅, at room temperature — misty fumes of HCl are the observation."},
        {"type": "list", "items": [
            "The reaction with **PCl₅ is used as a qualitative test for the –OH group** in a molecule.",
            "**Tertiary alcohols** are chlorinated with **concentrated hydrochloric acid** instead — the alcohol is **mixed (by shaking)** with the acid:",
        ]},
        {"type": "eq", "code": "(CH₃)₃COH  +  HCl  →  (CH₃)₃CCl  +  H₂O", "caption": "2-methylpropan-2-ol + concentrated HCl at room temperature (Core Practical 6)."},
        {"type": "h3", "text": "Bromination — HBr made in the flask"},
        {"type": "eq", "code": "KBr  +  H₂SO₄  →  KHSO₄  +  HBr", "caption": "The acid and the potassium bromide supply the HBr in situ (or 2KBr + H₂SO₄ → K₂SO₄ + 2HBr)."},
        {"type": "eq", "code": "C₂H₅OH(l)  +  HBr(aq)  →  C₂H₅Br(l)  +  H₂O(l)", "caption": "Substitution, heated under reflux — the product is a bromoalkane."},
        {"type": "callout", "variant": "exam", "title": "Why 50% concentrated H₂SO₄?", "text": "Because **100% concentrated sulfuric acid oxidises bromide ions to bromine** — and then **no hydrogen bromide is produced** for the reaction."},
        {"type": "h3", "text": "Iodination — via phosphorus triiodide"},
        {"type": "eq", "code": "2P(s)  +  3I₂(s)  →  2PI₃(s)", "caption": "Iodine and moist red phosphorus, warmed."},
        {"type": "eq", "code": "3C₂H₅OH(l)  +  PI₃(aq)  →  3C₂H₅I(l)  +  H₃PO₃(l)", "caption": "Substitution — the product is an iodoalkane."},
        {"type": "h3", "text": "Dehydration — forming an alkene"},
        {"type": "list", "items": [
            "**Excess concentrated H₂SO₄ or concentrated H₃PO₄**, heated **under reflux at 170 °C** — an **elimination (dehydration)** that removes water and forms an **alkene**.",
        ]},
        {"type": "eq", "code": "C₂H₅OH  →  CH₂=CH₂  +  H₂O", "caption": "Ethanol → ethene with concentrated phosphoric acid at 170 °C."},
        {"type": "list", "items": [
            "For **unsymmetrical alcohols containing more than three C atoms, a mixture of isomeric products** can be formed — dehydrating **butan-2-ol** gives both **but-2-ene** and **but-1-ene**:",
        ]},
        {"type": "eq", "code": "2CH₃CH₂CH(OH)CH₃  →  CH₃CH=CHCH₃  +  CH₃CH₂CH=CH₂  +  2H₂O", "caption": "Dehydration of butan-2-ol — two isomeric alkenes."},
        {"type": "callout", "variant": "tip", "title": "Not required", "text": "**Descriptions of the mechanisms of these reactions are not required** by the specification — reagents, conditions, reaction type and products are what earn the marks."},
    ],
)

S1018 = _sec(
    18, "oxidation-of-alcohols", "10.18", "Oxidation of Alcohols",
    "Dichromate decides by class — and by distil-or-reflux.",
    32, "10.18",
    "understand that potassium dichromate(VI) in dilute sulfuric acid can oxidise:",
    [
        "i    primary alcohols to produce aldehydes (which give a positive result with Benedict's or Fehling's solution) if the product is distilled as it forms",
        "ii    primary alcohols to produce carboxylic acids (which give a positive result with sodium carbonate or sodium hydrogencarbonate) if the reagents are heated under reflux",
        "iii    secondary alcohols to produce ketones",
        "In equations, the oxidising agent can be represented by [O].",
    ],
    [
        {"type": "p", "text": "Oxidation of alcohols using **acidified potassium dichromate(VI)** — or **potassium manganate(VII)** — solution leads to the formation of **aldehydes, ketones and carboxylic acids**. It provides a way of **differentiating between primary, secondary and tertiary alcohols**."},
        {"type": "table", "headers": ["Oxidising agent", "Observation"], "rows": [
            ["**potassium dichromate(VI) + dilute sulfuric acid**", "**orange to green**"],
            ["**potassium manganate(VII)**", "purple to colourless"],
        ]},
        {"type": "figure", "src": "/diagrams/t10-oxidation-flow.png", "srcDark": "/diagrams/t10-oxidation-flow-dark.png",
         "alt": "Flow diagram: primary alcohol to aldehyde by distillation then to carboxylic acid by reflux; secondary alcohol to ketone; tertiary alcohol not oxidised",
         "caption": "Primary → aldehyde → carboxylic acid; secondary → ketone; tertiary stops."},
        {"type": "h3", "text": "Primary alcohols — aldehyde or carboxylic acid"},
        {"type": "list", "items": [
            "Primary alcohols can be oxidised to **either aldehydes or carboxylic acids, depending on the reaction conditions** — **first to the aldehyde**, which is then **oxidised further** to the **carboxylic acid**.",
            "An **aldehyde** belongs to the homologous series with the **R–CHO** functional group; a **ketone** has the **R–CO–** functional group.",
        ]},
        {"type": "eq", "code": "CH₃CH₂OH  +  2[O]  →  CH₃CHO  +  H₂O", "caption": "Heat and distil — the aldehyde (ethanal) is distilled as it forms, so it escapes before it can be oxidised further."},
        {"type": "eq", "code": "CH₃CH₂OH  +  2[O]  →  CH₃COOH  +  H₂O", "caption": "Heat under reflux — the aldehyde condenses back into the mixture and is oxidised to the carboxylic acid (ethanoic acid)."},
        {"type": "h3", "text": "Secondary alcohols — ketones only"},
        {"type": "eq", "code": "CH₃CHOHCH₃  +  2[O]  →  CH₃COCH₃  +  H₂O", "caption": "Propan-2-ol → propanone (a ketone). Ketones cannot be further oxidised."},
        {"type": "list", "items": [
            "Secondary alcohols **can only be oxidised to ketones** — and **ketones cannot be further oxidised**.",
        ]},
        {"type": "h3", "text": "Tertiary alcohols — no reaction"},
        {"type": "eq", "code": "tertiary alcohol  +  [O]  →  no reaction", "caption": "Tertiary alcohols cannot be oxidised — the dichromate stays orange."},
        {"type": "h3", "text": "Test for aldehydes — Benedict's or Fehling's"},
        {"type": "list", "items": [
            "**Fehling's solution is blue** in colour due to its **Cu²⁺ ions**; **gently heat** with the sample.",
            "**Aldehyde:** the blue solution (Cu²⁺) changes to a **brick red precipitate** — the aldehyde is **oxidised to the carboxylic acid**, and the **Cu²⁺ ions are reduced to Cu⁺**.",
            "**Ketone:** the **blue solution remains unchanged**.",
        ]},
        {"type": "h3", "text": "Test for carboxylic acids — carbonate"},
        {"type": "list", "items": [
            "Add **sodium carbonate or sodium hydrogencarbonate**: **effervescence** — colourless gas bubbles that **turn limewater milky** (CO₂).",
        ]},
        {"type": "eq", "code": "2CH₃CO₂H  +  Na₂CO₃  →  2CH₃CO₂Na  +  H₂O  +  CO₂", "caption": "Carboxylic acid + sodium carbonate."},
        {"type": "table", "headers": ["Class", "Product", "Condition", "Positive test"], "rows": [
            ["Primary", "**aldehyde**", "**distil as it forms**", "Benedict's or Fehling's: blue → **brick red precipitate**"],
            ["Primary", "**carboxylic acid**", "**heat under reflux**", "sodium carbonate / sodium hydrogencarbonate: **effervescence**"],
            ["Secondary", "**ketone**", "reflux", "— (ketone unchanged by Fehling's)"],
            ["Tertiary", "no oxidation", "—", "dichromate stays **orange**"],
        ]},
        {"type": "worked", "title": "Why the apparatus decides the product", "problem": "Ethanol is oxidised with acidified potassium dichromate(VI). Explain fully why ethanal, rather than ethanoic acid, is produced and collected when the product is distilled as it forms.", "steps": [
            "Ethanal has a **lower boiling temperature** than the reaction mixture, so it **distils off as it forms**.",
            "Distillation **removes the aldehyde from contact with the oxidising agent** — the oxidation cannot continue.",
            "Under **reflux** the aldehyde would **condense back into the mixture** and be **oxidised further to ethanoic acid**.",
        ], "answer": "Distilling as it forms removes ethanal before it can be oxidised further — so ethanal, not ethanoic acid, is collected."},
    ],
)

S1019 = _sec(
    19, "preparation-and-purification", "10.19", "Preparation and Purification of a Liquid Organic Compound",
    "Why the crude product is impure — and the techniques that clean it up.",
    35, "10.19",
    "understand, the following techniques in the preparation and purification of a liquid organic compound:",
    [
        "i    heating under reflux",
        "ii    extraction with a solvent using a separating funnel",
        "iii    distillation",
        "iv    drying with an anhydrous salt",
        "v    boiling temperature determination",
    ],
    [
        {"type": "p", "text": "The organic products obtained from these reactions are **not pure**. The crude product could be contaminated with:"},
        {"type": "list", "items": [
            "**unreacted starting materials**",
            "**other organic products**",
            "**the inorganic reagents** used, or products formed from them",
            "**water**",
        ]},
        {"type": "p", "text": "The techniques used are based on the **physical state (solid, liquid or gas)** of the product. For a liquid, a preparation runs: **heating under reflux → distillation → solvent extraction → drying → boiling temperature determination**."},
        {"type": "h3", "text": "Heating under reflux"},
        {"type": "list", "items": [
            "Used when **heating organic reaction mixtures for long periods** — the **condenser prevents organic vapours from escaping** by **condensing them back to liquids**.",
            "**Anti-bumping granules** are added to the flask in both distillation and reflux — they **prevent vigorous, uneven boiling** by making **small bubbles form instead of large bubbles**.",
            "**Electric heaters** are used to heat organic chemicals — they are normally **highly flammable** and could **set on fire with a naked flame**.",
        ]},
        {"type": "callout", "variant": "warning", "title": "Never seal the condenser", "text": "**Never seal the end of the condenser** — the **build-up of gas pressure could cause the apparatus to explode**."},
        {"type": "h3", "text": "Distillation"},
        {"type": "list", "items": [
            "**Distillation** separates the components of a liquid mixture using **selective boiling and condensation** — collect the **distillate of the approximate boiling point range** of the desired product.",
            "The **bulb of the thermometer sits at the T-junction** connecting to the condenser, so it measures the **correct boiling point**.",
            "**Water goes in the bottom of the condenser** — it goes **against gravity**, which gives **more efficient cooling** and **prevents back flow of water**.",
        ]},
        {"type": "h3", "text": "Fractional distillation"},
        {"type": "list", "items": [
            "The separation of a liquid mixture into **fractions differing in boiling point**, typically using a **fractionating column**.",
        ]},
        {"type": "h3", "text": "Extraction with a separating funnel"},
        {"type": "list", "items": [
            "A mixture of **two immiscible liquids** can be separated with a separating funnel — it has a **stop-cock** in its stem to allow or stop the flow of liquid, and **two layers** are seen.",
            "The **denser solvent will be the bottom layer** — most **halogenated solvents are denser than water**, most **non-halogenated solvents are less dense**.",
        ]},
        {"type": "p", "text": "**Solvent extraction — method:**"},
        {"type": "list", "items": [
            "Place the reaction mixture in the separating funnel and **add the solvent** — it should form **two separate layers**.",
            "**Place the stopper** in the neck of the funnel and **gently shake** the contents, **releasing pressure by opening the tap** from time to time.",
            "**Allow the contents to settle** into two layers.",
            "**Remove the stopper, open the tap** and **collect the desired organic layer** into a flask — **discard the unwanted aqueous layer**.",
        ]},
        {"type": "h3", "text": "Drying with an anhydrous salt"},
        {"type": "list", "items": [
            "**Final traces of water** are removed by treating the organic solution with a **drying agent** — an **inorganic salt which readily takes up water to become hydrated**.",
            "Add **three spatula loads** of drying agent (e.g. **anhydrous sodium sulfate, calcium chloride**) to the organic liquid — when dry, the liquid should **appear clear**.",
            "The drying agent is removed by **decanting or filtration**. It must be **insoluble in the organic liquid** and **must not react with it**.",
        ]},
        {"type": "table", "headers": ["Drying agent", "Applications"], "rows": [
            ["anhydrous **calcium chloride, CaCl₂**", "used for **hydrocarbons**"],
            ["anhydrous **calcium sulfate, CaSO₄**", "**generally useful**"],
            ["anhydrous **magnesium sulfate, MgSO₄**", "not for **very acid-sensitive** compounds"],
            ["anhydrous **potassium carbonate, K₂CO₃**", "not for **acidic** compounds"],
            ["anhydrous **sodium sulfate, Na₂SO₄**", "**generally useful**"],
        ]},
        {"type": "h3", "text": "Boiling temperature determination"},
        {"type": "list", "items": [
            "**Purity of a liquid can be determined by measuring a boiling point** — in a distillation set-up, or by boiling a tube of the sample in a **heating oil bath**.",
            "Once the boiling point is found, the value is **compared with the data booklet values** — and the **purity of the compound is determined**.",
            "For a correct measure, the thermometer should be **above the level of the surface of the boiling liquid**, measuring the temperature of the **saturated vapour**.",
            "**Pressure should be noted** — changing pressure can change the boiling point of a liquid.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Reflux first, distil later", "text": "**Reflux** keeps everything in the flask so the reaction can be heated for a long period; **distillation** then separates the product by its boiling temperature. Same idea, two different jobs."},
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
