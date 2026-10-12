# -*- coding: utf-8 -*-
"""Topic 10 rebuild — sections 10.6 – 10.14 (10B Halogenoalkanes).

Style matches the original topic versions; wording stays verbatim to the
source notes (upload/Halogenoalkane.pdf) and the specification.
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


S106 = _sec(
    6, "halogenoalkanes-nomenclature", "10.6", "Halogenoalkanes: Nomenclature and Formulae",
    "CₙH₂ₙ₊₁X — naming, locants and the three formulae.",
    20, "10.6", "understand the nomenclature of halogenoalkanes and be able to draw their structural, displayed and skeletal formulae",
    [],
    [
        {"type": "def", "term": "Halogenoalkanes", "text": "**Halogenoalkanes** (also called **haloalkanes**) have a **halogen atom attached to a hydrocarbon chain**. They have the **general formula CₙH₂ₙ₊₁X**, where X is a halogen atom (F, Cl, Br or I). The halogen atom may sit at the end of the chain or on any of the carbons, and the molecule has **only single bonds**."},
        {"type": "h3", "text": "Nomenclature"},
        {"type": "p", "text": "In the IUPAC system:"},
        {"type": "list", "items": [
            "Identify the **longest chain of carbon atoms containing the halogen**.",
            "Halogen substituents take the prefixes **fluoro-, chloro-, bromo- and iodo-**, listed in **alphabetical order** with the other substituents.",
            "A **number (locant)** shows the position of the halogen. **No locant is needed with only two carbons** — with longer chains, a locant is needed to say where on the chain the halogen atom is situated.",
        ]},
        {"type": "table", "headers": ["Compound", "Name"], "rows": [
            ["CH₃Cl", "chloromethane"],
            ["CH₃CH₂Br", "bromoethane"],
            ["CH₃CH₂CH₂I", "1-iodopropane"],
            ["CH₃CH(I)CH₃", "2-iodopropane"],
        ]},
        {"type": "h3", "text": "Branched chains and several halogens"},
        {"type": "list", "items": [
            "If the chain is branched, the **longest continuous chain containing the halogen atom** gives the parent name and the side chains are named as **alkyl groups** — (CH₃)₃CBr is **2-bromo-2-methylpropane**.",
            "With **more than one halogen atom**, use **di-, tri-, tetra-** and locants to say where they are: CH₃CH(Cl)CH(Cl)CH₃ is **2,3-dichlorobutane**.",
        ]},
        {"type": "h3", "text": "The three formulae"},
        {"type": "list", "items": [
            "**Structural** — atoms in order, bonds implied: CH₃CH₂Br.",
            "**Displayed** — **every bond drawn** out, atom by atom.",
            "**Skeletal** — the zig-zag line drawing; carbons at every bend and end, hydrogens left out, the halogen labelled.",
        ]},
        {"type": "callout", "variant": "exam", "title": "Which formula is being asked for?", "text": "Command words matter — ‘displayed’ means **every bond drawn**, ‘structural’ means the CH₃CH₂… text form, ‘skeletal’ means the zig-zag. Drawing the wrong one loses the mark even if the molecule is right."},
    ],
)

S107 = _sec(
    7, "halogenoalkane-classes", "10.7", "Primary, Secondary and Tertiary Halogenoalkanes",
    "Count the alkyl groups on the carbon that carries the halogen.",
    12, "10.7", "understand the distinction between primary, secondary and tertiary halogenoalkanes",
    [],
    [
        {"type": "p", "text": "Halogenoalkanes are classified as **primary, secondary or tertiary**, depending on the **number of alkyl groups attached to the carbon that carries the halogen** (the C–X carbon)."},
        {"type": "table", "headers": ["Class", "The C–X carbon is joined to", "Example"], "rows": [
            ["**Primary (1°)**", "**one** alkyl group", "1-chloroethane, CH₃CH₂Cl"],
            ["**Secondary (2°)**", "**two** alkyl groups", "2-bromopropane, CH₃CHBrCH₃"],
            ["**Tertiary (3°)**", "**three** alkyl groups", "2-iodo-2-methylpropane, (CH₃)₃CI"],
        ]},
        {"type": "figure", "src": "/diagrams/t10-halo-classes.png", "srcDark": "/diagrams/t10-halo-classes-dark.png",
         "alt": "General structures of primary, secondary and tertiary halogenoalkanes with examples",
         "caption": "One, two or three alkyl groups on the carbon holding the halogen — that is the whole classification."},
        {"type": "p", "text": "The **same types of reaction** are open to all three classes — but there is a **difference in the rate** at which they react (sections 10.10 and 10.12)."},
    ],
)

S108 = _sec(
    8, "halogenoalkane-reactions", "10.8", "Reactions of Halogenoalkanes",
    "Five reagents, one target — the solvent decides the role of OH⁻.",
    30, "10.8",
    "understand the reactions of halogenoalkanes with:",
    [
        "i    aqueous alkali, including KOH(aq) to produce alcohols (where the hydroxide ion acts as a nucleophile)",
        "ii    ethanolic potassium hydroxide to produce alkenes by an elimination reaction (where the hydroxide ion acts as a base)",
        "iii    aqueous silver nitrate in ethanol (where water acts as a nucleophile)",
        "iv    alcoholic ammonia under pressure to produce amines (where the ammonia acts as a nucleophile)",
        "v    alcoholic potassium cyanide to produce nitriles (where the cyanide ion acts as a nucleophile)",
        "Students should know this is an example of increasing the length of the carbon chain.",
    ],
    [
        {"type": "p", "text": "Warm the halogenoalkane with the reagent and note three things every time: the **reagent and its solvent**, the **role of the attacking species**, and the **product**. Many organic reactions are slow and the reagents volatile, so they are carried out by **heating under reflux** — boiling the mixture and condensing the vapour back into the flask continuously."},
        {"type": "table", "headers": ["Reagent", "Condition", "The attacker", "Product"], "rows": [
            ["**KOH(aq)** — aqueous alkali", "heat under reflux, aqueous solution", "OH⁻ acts as a **nucleophile**", "**alcohol**"],
            ["**ethanolic KOH**", "heat under reflux, ethanolic solution", "OH⁻ acts as a **base**", "**alkene** (elimination)"],
            ["**aqueous AgNO₃ in ethanol**", "ethanol as solvent", "H₂O acts as a **nucleophile**", "**alcohol** (hydrolysis) + AgX precipitate"],
            ["**alcoholic NH₃**", "heat **under pressure in a sealed tube**", "NH₃ acts as a **nucleophile**", "**amine** (amino alkane)"],
            ["**alcoholic KCN**", "reflux, aqueous alcoholic solution", "CN⁻ acts as a **nucleophile**", "**nitrile**"],
        ]},
        {"type": "h3", "text": "Aqueous alkali — nucleophilic substitution"},
        {"type": "eq", "code": "CH₃CH₂Br  +  :OH⁻(aq)  →  CH₃CH₂OH  +  :Br⁻", "caption": "Bromoethane + aqueous potassium hydroxide, heated under reflux → ethanol."},
        {"type": "h3", "text": "Ethanolic potassium hydroxide — elimination"},
        {"type": "eq", "code": "CH₃CH₂CH₂Cl  +  OH⁻  →  CH₃CH=CH₂  +  H₂O  +  Cl⁻", "caption": "1-chloropropane + ethanolic KOH → propene. For unsymmetrical halogenoalkanes, a mixture of isomeric alkenes can form: CH₃CH₂CH(Cl)CH₃ gives but-2-ene and but-1-ene."},
        {"type": "h3", "text": "Aqueous silver nitrate in ethanol — hydrolysis"},
        {"type": "p", "text": "**Water acts as the nucleophile** and replaces the halogen with an –OH group. The halide ion released then forms a **silver halide precipitate** with the silver ions — the basis of the rate comparisons in section 10.10."},
        {"type": "h3", "text": "Alcoholic ammonia — amines"},
        {"type": "eq", "code": "CH₃CH₂CH₂Cl  +  2NH₃  →  CH₃CH₂CH₂NH₂  +  NH₄Cl", "caption": "1-chloropropane + concentrated ammonia → propylamine. The reaction needs a sealed tube: ammonia does not condense in a heat-under-reflux apparatus, so it escapes unless sealed."},
        {"type": "h3", "text": "Alcoholic potassium cyanide — nitriles"},
        {"type": "eq", "code": "C₂H₅Br  +  KCN(aq/alc)  →  C₂H₅CN  +  KBr(aq)", "caption": "Bromoethane + potassium cyanide → propanenitrile — the nitrile has one more carbon atom than the halogenoalkane."},
        {"type": "p", "text": "The KCN reaction is an example of **increasing the length of the carbon chain** — the carbon skeleton grows by one."},
        {"type": "callout", "variant": "warning", "title": "Same reagent, different solvent", "text": "KOH gives two different reactions: **aqueous** → substitution (OH⁻ = nucleophile); **ethanolic** → elimination (OH⁻ = base). Name the solvent **and** the role of the hydroxide ion in every answer."},
    ],
)

S109 = _sec(
    9, "nucleophilic-substitution-mechanisms", "10.9", "Nucleophilic Substitution Mechanisms",
    "Curly arrows for primary halogenoalkanes with OH⁻ and with NH₃.",
    25, "10.9",
    "understand the mechanisms of the nucleophilic substitution reactions between primary halogenoalkanes and:",
    [
        "i    aqueous potassium hydroxide",
        "ii    ammonia",
        "SN1 and SN2 substitution mechanisms will be tested in Unit 4.",
    ],
    [
        {"type": "p", "text": "In these reactions the attacking species is a **nucleophile** — hydroxide ions or ammonia molecules — and the substrate is a **primary** halogenoalkane."},
        {"type": "h3", "text": "Bromoethane with aqueous potassium hydroxide"},
        {"type": "figure", "src": "/diagrams/t10-substitution-mechanism.png", "srcDark": "/diagrams/t10-substitution-mechanism-dark.png",
         "alt": "Curly arrow mechanism: hydroxide donates its lone pair to the δ+ carbon of bromoethane, the C–Br bond breaks heterolytically, ethanol and Br− form",
         "caption": "One step: lone pair in from OH⁻, C–O bond forms, C–Br bond breaks heterolytically."},
        {"type": "list", "items": [
            "The reaction starts by **donating a lone pair of electrons** from the **oxygen of the hydroxide** to the **electron-deficient carbon atom**.",
            "A **C–O bond forms** and at the same time the electrons in the C–Br bond move to the Br atom — the **C–Br bond breaks**.",
            "This type of bond breaking, where **both electrons of the shared pair are kept by one atom**, is **heterolytic fission**. The organic product is **ethanol**.",
        ]},
        {"type": "h3", "text": "1-bromopropane with ammonia — two steps"},
        {"type": "list", "items": [
            "**First step** — the **nitrogen of an ammonia molecule donates its lone pair** to the electron-deficient carbon; a **C–N bond forms** and the C–Br bond breaks heterolytically, leaving a **positively charged ion**.",
            "**Second step** — a **second ammonia molecule acts as a base** and **removes a hydrogen** from the ion formed.",
            "The products are the **amine** (propylamine, CH₃CH₂CH₂NH₂) and **NH₄Br**.",
        ]},
        {"type": "callout", "variant": "exam", "title": "Phrases that carry the marks", "text": "**lone pair donated** · **attacked the electron-deficient (δ+) carbon** · **C–X bond breaks heterolytically** · **second NH₃ acts as a base**. The labels **SN1 and SN2** for these mechanisms are tested in Unit 4."},
    ],
)

S1010 = _sec(
    10, "comparing-hydrolysis-rates", "10.10", "Comparing Rates of Hydrolysis",
    "Water as the nucleophile — and what the precipitate shows.",
    22, "10.10",
    "understand that experimental observations and data can be used to compare the relative rates of hydrolysis of:",
    [
        "i    primary, secondary and tertiary structural isomers of a halogenoalkane",
        "ii    primary chloro-, bromo- and iodoalkanes using aqueous silver nitrate in ethanol",
    ],
    [
        {"type": "def", "term": "Hydrolysis", "text": "A reaction in which **water or hydroxide ions replace an atom in a molecule with an –OH group**."},
        {"type": "eq", "code": "RX  +  H₂O  →  ROH  +  H⁺  +  X⁻", "caption": "R is an alkyl group and X a halogen — e.g. CH₃CH₂Cl + H₂O → CH₃CH₂OH + H⁺ + Cl⁻ (or written as ROH + HX)."},
        {"type": "p", "text": "In **aqueous silver nitrate in ethanol** the halogenoalkane hydrolyses, and the **halide ion** released reacts with the silver ions to form a **precipitate of silver halide**:"},
        {"type": "eq", "code": "X⁻(aq)  +  Ag⁺(aq)  →  AgX(s)", "caption": "The sooner the precipitate appears, the faster the hydrolysis."},
        {"type": "table", "headers": ["Precipitate", "Colour", "From"], "rows": [
            ["**AgCl**", "**white**", "chloroalkane"],
            ["**AgBr**", "**cream**", "bromoalkane"],
            ["**AgI**", "**yellow**", "iodoalkane"],
        ]},
        {"type": "h3", "text": "What the observations show"},
        {"type": "list", "items": [
            "**Same structure, different halogen:** 1-**iodobutane is fastest**, 1-bromobutane is in between, 1-**chlorobutane is slowest** — the weaker the C–X bond, the faster the hydrolysis (section 10.13).",
            "**Same halogen, different class:** **tertiary** halogenoalkanes react **rapidly** — a precipitate is seen as soon as the silver nitrate is added; **secondary** halogenoalkanes react **slowly**; **primary** halogenoalkanes **hardly react with water** (section 10.12).",
        ]},
        {"type": "p", "text": "Rate of hydrolysis can be compared by noting the **time taken for the precipitate to appear** — and the precipitate colour doubles as a **test to identify the halogen** in the halogenoalkane."},
    ],
)

S1011 = _sec(
    11, "core-practical-5", "10.11", "Core Practical 5: Rates of Hydrolysis",
    "The silver nitrate investigation that ranks hydrolysis rates.",
    15, "10.11", "CORE PRACTICAL 5\nInvestigation of the rates of hydrolysis of some halogenoalkanes.",
    [],
    [
        {"type": "p", "text": "**Core Practical 5** investigates the rates of hydrolysis of some halogenoalkanes — comparing halogenoalkanes that differ in the **halogen they carry** or in their **class** (primary, secondary, tertiary)."},
        {"type": "h3", "text": "Method"},
        {"type": "list", "items": [
            "To each of three test tubes add **aqueous silver nitrate (1 cm³)** and **ethanol (2 cm³)**, and stand them in a **water bath at 60 °C** — the **ethanol dissolves the halogenoalkane**, which is insoluble in water.",
            "After **five minutes**, add **2 drops** of a different halogenoalkane to each tube — e.g. 1-chlorobutane, 1-bromobutane, 1-iodobutane.",
            "**Shake, loosely cork**, and observe each tube at 60 °C for **ten minutes**, noting the **time taken for the precipitate to appear** and its colour.",
        ]},
        {"type": "h3", "text": "Results and conclusions"},
        {"type": "table", "headers": ["Halogenoalkane", "Observation", "Conclusion"], "rows": [
            ["1-iodobutane", "yellow precipitate — appears **fastest**", "**C–I is the weakest bond** → fastest hydrolysis"],
            ["1-bromobutane", "cream precipitate — slower", "in between"],
            ["1-chlorobutane", "white precipitate — **slowest**", "**C–Cl is the strongest bond** → slowest hydrolysis"],
        ]},
        {"type": "p", "text": "The **colour** of the precipitate identifies the halogen; the **time taken** to appear ranks the rates. The same experiment therefore doubles as the suggested practical that uses **silver nitrate solution to identify the halogen present in halogenoalkanes**."},
    ],
)

S1012 = _sec(
    12, "halogenoalkane-reactivity-trend", "10.12", "Reactivity of Primary, Secondary and Tertiary Halogenoalkanes",
    "Tertiary > secondary > primary — carbocation stability decides.",
    8, "10.12", "know the trend in reactivity of primary, secondary and tertiary halogenoalkanes",
    [],
    [
        {"type": "p", "text": "For the **same halogen**, the trend in reactivity is:"},
        {"type": "eq", "code": "tertiary  >  secondary  >  primary  >  methyl", "caption": "Rate of reaction increases as the carbocation becomes more stable."},
        {"type": "list", "items": [
            "The rate of reaction increases due to the **increase in stability of the carbocations** formed as the C–X bond breaks.",
            "**Tertiary carbocations are more stable than secondary carbocations**, which are **more stable than primary carbocations**.",
        ]},
        {"type": "callout", "variant": "tip", "title": "Compare like with like", "text": "Hold the **halogen constant** when you compare the classes (10.12), and hold the **class constant** when you compare the halogens (10.13). One variable at a time."},
    ],
)

S1013 = _sec(
    13, "bond-enthalpy-reactivity", "10.13", "Bond Enthalpy and Reactivity",
    "Down the group the C–X bond gets longer, weaker — and faster to break.",
    10, "10.13", "understand, in terms of bond enthalpy, the trend in reactivity of chloro-, bromo- and iodoalkanes",
    [],
    [
        {"type": "list", "items": [
            "Down the halogen group the **carbon–halogen bond becomes longer and hence weaker**, so **less energy is required to break it**.",
            "The rate of reaction therefore **increases** from chloroalkane to bromoalkane to iodoalkane.",
        ]},
        {"type": "table", "headers": ["Bond", "Mean bond enthalpy / kJ mol⁻¹"], "rows": [
            ["C–F", "+467"],
            ["C–Cl", "+346"],
            ["C–Br", "+290"],
            ["C–I", "+228"],
        ]},
        {"type": "list", "items": [
            "A **strong bond requires more energy to break** the bond; a **weaker bond requires less** — so **iodoalkanes hydrolyse fastest** and fluoroalkanes hardly react at all.",
        ]},
        {"type": "callout", "variant": "warning", "title": "Bond enthalpy wins — not polarity", "text": "C–F is the **most polar** C–X bond, yet fluoroalkanes are the **least reactive**, because C–F is the **strongest** bond (+467 kJ mol⁻¹). Rates here depend on **bond enthalpy**, not on polarity."},
    ],
)

S1014 = _sec(
    14, "core-practical-6", "10.14", "Core Practical 6: Chlorination of 2-methylpropan-2-ol",
    "From a tertiary alcohol to a halogenoalkane with concentrated HCl.",
    10, "10.14",
    "CORE PRACTICAL 6\nChlorination of 2-methylpropan-2-ol with concentrated hydrochloric acid.",
    [
        "Further suggested practicals:",
        "i    the use of silver nitrate solution to identify the halogen present in halogenoalkanes",
        "ii    preparation of 1-bromobutane from butan-1-ol, potassium bromide and sulfuric acid",
    ],
    [
        {"type": "p", "text": "**Core Practical 6** chlorinates **2-methylpropan-2-ol** (a **tertiary alcohol**) with **concentrated hydrochloric acid** — the –OH group is **replaced by chlorine**:"},
        {"type": "eq", "code": "(CH₃)₃COH  +  HCl  →  (CH₃)₃CCl  +  H₂O", "caption": "2-methylpropan-2-ol + concentrated hydrochloric acid → 2-chloro-2-methylpropane."},
        {"type": "p", "text": "This is the halogenoalkane-forming twin of section 10.8: the alcohol supplies the carbon skeleton and the halogen takes the place of the –OH group."},
        {"type": "h3", "text": "Further suggested practicals"},
        {"type": "list", "items": [
            "Use **silver nitrate solution** to identify the **halogen present in halogenoalkanes** — the precipitate colours of section 10.10 (white AgCl, cream AgBr, yellow AgI).",
            "**Preparation of 1-bromobutane** from **butan-1-ol, potassium bromide and sulfuric acid**.",
        ]},
    ],
)

SECTIONS_O2 = [S106, S107, S108, S109, S1010, S1011, S1012, S1013, S1014]
