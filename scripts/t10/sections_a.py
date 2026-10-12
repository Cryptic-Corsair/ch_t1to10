#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Topic 10 content — part A: 10.0 Specification Map + 10.1 General principles.

Wording contract:
- spec/specText = the specification's own words (IAL 2018, WCH12 Topic 10)
- teaching text stays inside the app's established vocabulary; mark-scheme
  keywords are bolded
- digest shape: key point first, short steps, 'In the exam' where wording
  matters, a tip to close, quick check at the end
"""

S_MAP = {
    "id": "t10-0",
    "sectionKey": "specification-map",
    "number": "10.0",
    "title": "Specification Map",
    "blurb": "Every statement the specification assesses in this topic — use it as your revision checklist.",
    "estMinutes": 8,
    "spec": "10.1 – 10.23",
    "specText": "Students will be assessed on their ability to:",
    "outline": [],
    "content": [
        {"type": "p",
         "text": "Topic 10 is the checkpoint for your organic chemistry. It names the reaction types you have already met, then adds two new families — **halogenoalkanes** and **alcohols** — and the two analytical techniques, **mass spectrometry** and **infrared spectroscopy**, that identify what a reaction has made."},
        {"type": "list", "items": [
            "Every section **opens with the key point** — the one thing it is really about.",
            "Then the idea is **built up in short steps**, with the tables and diagrams that carry it.",
            "Where wording matters, an **In the exam** note shows the words the mark scheme wants.",
            "A **tip** closes most sections with the short version — everything worth remembering at a glance.",
            "And every section ends with a **quick check** — answer from memory first, then tap to reveal.",
        ]},
        {"type": "p",
         "text": "Here is the full checklist — every assessment statement for Topic 10, worded exactly as the specification words it:"},
        {"type": "table",
         "headers": ["Spec", "Assessment statement"],
         "rows": [
             ["10.1", "be able to classify reactions (including those in Unit 1) as addition, elimination, substitution, oxidation, reduction, hydrolysis or polymerisation"],
             ["10.2", "understand the concept of a reaction mechanism"],
             ["10.3", "understand that heterolytic bond breaking results in species that are electrophiles or nucleophiles"],
             ["10.4", "know the definition of the term 'nucleophile'"],
             ["10.5", "understand the link between bond polarity and the type of reaction mechanism a compound will undergo"],
             ["10.6", "understand the nomenclature of halogenoalkanes and be able to draw their structural, displayed and skeletal formulae"],
             ["10.7", "understand the distinction between primary, secondary and tertiary halogenoalkanes"],
             ["10.8", "understand the reactions of halogenoalkanes with:\ni   aqueous alkali, including KOH(aq) to produce alcohols (where the hydroxide ion acts as a nucleophile)\nii   ethanolic potassium hydroxide to produce alkenes by an elimination reaction (where the hydroxide ion acts as a base)\niii   aqueous silver nitrate in ethanol (where water acts as a nucleophile)\niv   alcoholic ammonia under pressure to produce amines (where the ammonia acts as a nucleophile)\nv   alcoholic potassium cyanide to produce nitriles (where the cyanide ion acts as a nucleophile)"],
             ["10.9", "understand the mechanisms of the nucleophilic substitution reactions between primary halogenoalkanes and:\ni   aqueous potassium hydroxide\nii   ammonia"],
             ["10.10", "understand that experimental observations and data can be used to compare the relative rates of hydrolysis of:\ni   primary, secondary and tertiary structural isomers of a halogenoalkane\nii   primary chloro-, bromo- and iodoalkanes using aqueous silver nitrate in ethanol"],
             ["10.11", "CORE PRACTICAL 5 — Investigation of the rates of hydrolysis of some halogenoalkanes."],
             ["10.12", "know the trend in reactivity of primary, secondary and tertiary halogenoalkanes"],
             ["10.13", "understand, in terms of bond enthalpy, the trend in reactivity of chloro-, bromo- and iodoalkanes"],
             ["10.14", "CORE PRACTICAL 6 — Chlorination of 2-methylpropan-2-ol with concentrated hydrochloric acid."],
             ["10.15", "understand the nomenclature of alcohols and be able to draw their structural, displayed and skeletal formulae"],
             ["10.16", "understand the distinction between primary, secondary and tertiary alcohols"],
             ["10.17", "understand the reactions of alcohols with:\ni   oxygen in air (combustion)\nii   halogenating agents:\n•   PCl₅ to produce chloroalkanes (including its use as a qualitative test for the presence of the –OH group)\n•   50% concentrated sulfuric acid and potassium bromide to produce bromoalkanes\n•   red phosphorus and iodine to produce iodoalkanes\niii   concentrated phosphoric acid to form alkenes by elimination"],
             ["10.18", "understand that potassium dichromate(VI) in dilute sulfuric acid can oxidise:\ni   primary alcohols to produce aldehydes (which give a positive result with Benedict's or Fehling's solution) if the product is distilled as it forms\nii   primary alcohols to produce carboxylic acids (which give a positive result with sodium carbonate or sodium hydrogencarbonate) if the reagents are heated under reflux\niii   secondary alcohols to produce ketones"],
             ["10.19", "understand the following techniques in the preparation and purification of a liquid organic compound:\ni   heating under reflux\nii   extraction with a solvent using a separating funnel\niii   distillation\niv   drying with an anhydrous salt\nv   boiling temperature determination"],
             ["10.20", "CORE PRACTICAL 7 — The oxidation of propan-1-ol to produce propanal and propanoic acid."],
             ["10.21", "be able to interpret data from mass spectra to suggest possible structures of simple organic compounds using the m/z of the molecular ion and fragmentation patterns"],
             ["10.22", "be able to use infrared spectra, or data from infrared spectra, to deduce functional groups present in organic compounds, and predict infrared absorptions, given wavenumber data, due to familiar functional groups including:\ni   C–H stretching absorptions in alkanes, alkenes and aldehydes\nii   C=C stretching absorption in alkenes\niii   O–H stretching absorptions in alcohols and carboxylic acids\niv   C=O stretching absorptions in aldehydes, ketones and carboxylic acids\nv   C–X stretching absorption in halogenoalkanes\nvi   N–H stretching absorption in amines"],
             ["10.23", "CORE PRACTICAL 8 — Analysis of some inorganic and organic unknowns."],
         ]},
        {"type": "callout", "variant": "tip",
         "title": "How the topic is organised",
         "text": "Four parts: **general principles** (10.1 – 10.5), **halogenoalkanes** (10.6 – 10.14), **alcohols** (10.15 – 10.20) and **spectra** (10.21 – 10.23). The general principles come back in every later section — learn them first.",
         "style": "note"},
    ],
}


S_101 = {
    "id": "cmv1eoi8j00g1jfqkfpnleap0",
    "sectionKey": "mechanism-principles",
    "number": "10.1",
    "title": "Reaction Mechanisms and Nucleophiles",
    "blurb": "How bonds break — and the species that attack.",
    "estMinutes": 30,
    "spec": "10.1 – 10.5",
    "specText": "be able to classify reactions (including those in Unit 1) as addition, elimination, substitution, oxidation, reduction, hydrolysis or polymerisation\nunderstand the concept of a reaction mechanism\nunderstand that heterolytic bond breaking results in species that are electrophiles or nucleophiles\nknow the definition of the term 'nucleophile'\nunderstand the link between bond polarity and the type of reaction mechanism a compound will undergo",
    "outline": [],
    "content": [
        {"type": "callout", "variant": "key",
         "title": "Every organic reaction is a story — which bond breaks, which species attacks, what takes its place.",
         "text": "Name those three things and the mechanism writes itself.",
         "style": "note"},

        {"type": "h3", "text": "Sorting reactions into types"},
        {"type": "p",
         "text": "The specification asks you to classify reactions into seven types. You have already met nearly all of them — now you name them. Two worked labels:"},
        {"type": "table",
         "headers": ["Reaction", "Class", "How to spot it"],
         "rows": [
             ["ethene + Br₂ → 1,2-dibromoethane", "**Addition**", "two molecules become one — nothing is lost"],
             ["C₂H₆ + Br₂ → C₂H₅Br + HBr (UV light)", "**Substitution**", "an atom or group is swapped for another"],
             ["ethanol → ethene + H₂O (conc. H₃PO₄, hot)", "**Elimination**", "a small molecule splits out of one molecule"],
             ["C₂H₅OH + 2[O] → CH₃COOH + H₂O", "**Oxidation**", "oxygen added, hydrogen removed — [O] in equations"],
             ["CuO + H₂ → Cu + H₂O", "**Reduction**", "oxygen removed — the reverse of oxidation"],
             ["C₂H₅Br + H₂O → C₂H₅OH + HBr", "**Hydrolysis**", "a molecule is split apart by water"],
             ["many ethene → poly(ethene)", "**Polymerisation**", "small molecules join end to end into one long chain"],
         ]},
        {"type": "p",
         "text": "Oxidation and reduction travel together — a species is oxidised only if another is reduced (Topic 8). The same reaction can be classified either way depending on which partner you watch."},

        {"type": "h3", "text": "What a mechanism is"},
        {"type": "def", "term": "Reaction mechanism",
         "text": "The **step-by-step account of how a reaction happens** — which bonds break, which bonds form, in what order, and which species attacks which. Curly arrows show where the electron pairs go."},
        {"type": "p",
         "text": "A balanced equation tells you what goes in and what comes out. A **mechanism** tells you how it got there. In this topic the mechanisms are drawn with **curly arrows** (movement of an electron pair) and **partial charges δ+ / δ−**."},

        {"type": "h3", "text": "How the bond breaks decides who attacks"},
        {"type": "p",
         "text": "A covalent bond can split in two ways (Topic 4) — and each way creates a different kind of attacker:"},
        {"type": "table",
         "headers": ["Fission", "What happens", "What it creates"],
         "rows": [
             ["**Homolytic**", "each bonding atom keeps **one** electron", "two **free radicals** — alkanes + halogens in UV light"],
             ["**Heterolytic**", "**one atom takes both** electrons", "a **cation and an anion** — the species that are **electrophiles or nucleophiles**"],
         ]},
        {"type": "callout", "variant": "exam",
         "title": "Say it like this",
         "text": "Heterolytic fission = **one atom takes both of the shared electrons**. The products are charged — and those charged species are exactly what attack in the mechanisms of this topic.",
         "style": "note"},

        {"type": "h3", "text": "The two attackers"},
        {"type": "def", "term": "Nucleophile",
         "text": "An **electron-pair donor**. It attacks an electron-deficient (δ+) carbon atom, using a **lone pair** of electrons to form a new covalent bond. Examples: **OH⁻, CN⁻, :NH₃** and water."},
        {"type": "def", "term": "Electrophile",
         "text": "An **electron-pair acceptor** — attracted to regions of **high electron density**. You met it in Topic 5, attacking the electron-rich C=C double bond."},
        {"type": "figure", "src": "/diagrams/t10-nucleophile-attack.png",
         "srcDark": "/diagrams/t10-nucleophile-attack-dark.png",
         "alt": "The polar C–X bond with δ+ carbon attacked by a nucleophile donating a lone pair, the halogen leaving as X−",
         "caption": "Polarity puts a δ+ on carbon — the nucleophile's lone pair finds it, and the halogen leaves with the bonding pair."},
        {"type": "callout", "variant": "exam",
         "title": "The definition is a mark on its own",
         "text": "A nucleophile is an **electron-pair donor** — write it exactly. 'Something that attacks positive carbon' does not earn the mark. Keep three examples ready: **OH⁻, CN⁻, :NH₃**.",
         "style": "note"},

        {"type": "h3", "text": "Polarity is the trigger"},
        {"type": "p",
         "text": "Why does a halogenoalkane get attacked at all? Because the **C–X bond is polar**:"},
        {"type": "list", "items": [
            "The halogen is **more electronegative** than carbon (Topic 3), so it pulls the bonding electrons towards itself.",
            "The carbon is left with a **partial positive charge, Cδ+** — it is electron-deficient.",
            "An electron-rich **nucleophile is attracted straight to that δ+ carbon** — so bond polarity decides the **type of mechanism** the compound undergoes.",
        ]},
        {"type": "callout", "variant": "tip",
         "title": "One chain to memorise",
         "text": "**electronegativity → polar bond → δ+ carbon → nucleophilic attack.** It explains every reaction in the next section.",
         "style": "note"},

        {"type": "qa", "items": [
            {"q": "Classify: ethene + Br₂, and C₂H₅OH + 2[O] → CH₃COOH + H₂O.",
             "a": "**Addition** (two molecules become one) and **oxidation** ([O] supplies the oxygen)."},
            {"q": "What is a nucleophile — exact wording?",
             "a": "An **electron-pair donor** that attacks electron-deficient (δ+) carbon atoms — e.g. **OH⁻, CN⁻, :NH₃**."},
            {"q": "Heterolytic fission creates which two kinds of attacking species?",
             "a": "**Electrophiles or nucleophiles** — charged species from one atom taking **both** bonding electrons."},
            {"q": "Why is the carbon in a C–Br bond electron-deficient?",
             "a": "Bromine is **more electronegative**, so the bond is **polar** and the carbon carries the **δ+** charge."},
        ]},
    ],
}


SECTIONS_A = [S_MAP, S_101]
