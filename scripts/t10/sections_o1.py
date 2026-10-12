# -*- coding: utf-8 -*-
"""Topic 10 rebuild — sections 10.0 – 10.5 (10A General principles).

Authored to match the original topic versions (1–9): one section per
specification statement, def/list/table/eq/figure/worked blocks, direct
headings, sparse callouts, no qa blocks.
"""
import json

with open("/tmp/t10_specmap_rows.json", "r", encoding="utf-8") as f:
    _SPEC_ROWS = json.load(f)["rows"]


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


S100 = _sec(
    0, "specification-map", "10.0", "Specification Map",
    "Every statement the specification assesses in this topic — use it as your revision checklist.",
    8, "10.1 – 10.23", "Students will be assessed on their ability to:",
    [
        "The full list of assessment statements for Topic 10, worded exactly as the specification words them",
        "Every statement 10.1 – 10.23 has its own section below",
        "Four parts: 10A General principles (10.1 – 10.5), 10B Halogenoalkanes (10.6 – 10.14), 10C Alcohols (10.15 – 10.20), 10D Mass spectra and IR (10.21 – 10.23)",
    ],
    [
        {"type": "p", "text": "Students will be assessed on their ability to:"},
        {"type": "table", "headers": _SPEC_ROWS[0] and ["Spec", "Assessment statement"], "rows": _SPEC_ROWS},
    ],
)

S101 = _sec(
    1, "classifying-reactions", "10.1", "Classifying Reactions",
    "Addition, elimination, substitution, oxidation, reduction, hydrolysis or polymerisation.",
    15, "10.1",
    "be able to classify reactions (including those in Unit 1) as addition, elimination, substitution, oxidation, reduction, hydrolysis or polymerisation",
    [],
    [
        {"type": "p", "text": "Seven labels cover every organic reaction in the course — including all the reactions you met in Unit 1. Classify a reaction by looking at **what happens to the molecules**: bonds formed or broken, atoms or groups swapped, small units joined up."},
        {"type": "def", "term": "Addition", "text": "Two or more reactant molecules react to form a **single product** — nothing else is made."},
        {"type": "def", "term": "Substitution", "text": "An atom or group of atoms in a molecule is **replaced by a different atom or group**."},
        {"type": "def", "term": "Elimination", "text": "A **small molecule** (such as H₂O or HBr) is **removed from** a larger one, leaving a C=C double bond."},
        {"type": "def", "term": "Oxidation", "text": "A reaction involving the **gain of oxygen** or the **loss of hydrogen**."},
        {"type": "def", "term": "Reduction", "text": "A reaction involving the **loss of oxygen** or the **gain of hydrogen**."},
        {"type": "def", "term": "Hydrolysis", "text": "A reaction in which **water or hydroxide ions replace an atom in a molecule with an –OH group**."},
        {"type": "def", "term": "Polymerisation", "text": "Many small **monomer** molecules join together end to end to form one long-chain **polymer**."},
        {"type": "table", "headers": ["Type", "Example equation", "How to spot it"], "rows": [
            ["Addition", "CH₂=CH₂ + Br₂ → CH₂BrCH₂Br", "Two molecules in, one product out"],
            ["Substitution", "CH₄ + Cl₂ → CH₃Cl + HCl (UV light)", "An atom swapped for another"],
            ["Elimination", "CH₃CH₂OH → CH₂=CH₂ + H₂O (conc. H₃PO₄, heat)", "A small molecule splits out"],
            ["Oxidation", "CH₃CH₂OH + 2[O] → CH₃COOH + H₂O", "Oxygen gained / hydrogen lost"],
            ["Reduction", "CuO + H₂ → Cu + H₂O", "Oxygen lost"],
            ["Hydrolysis", "C₂H₅Br + H₂O → C₂H₅OH + HBr", "Water splits the molecule"],
            ["Polymerisation", "n CH₂=CH₂ → (—CH₂—CH₂—)ₙ", "Many monomers → one chain"],
        ]},
        {"type": "callout", "variant": "exam", "title": "One reaction can carry two labels", "text": "Oxidation and reduction happen together — one species is oxidised only if another is reduced. The same reaction can also fit more than one class: hydrogenating ethene (C₂H₄ + H₂ → C₂H₆) is **addition** and **reduction**. Classify from the change, and name both labels when both apply."},
    ],
)

S102 = _sec(
    2, "reaction-mechanisms", "10.2", "Reaction Mechanisms",
    "What a mechanism shows that a balanced equation does not.",
    10, "10.2", "understand the concept of a reaction mechanism",
    [],
    [
        {"type": "def", "term": "Reaction mechanism", "text": "A **step-by-step account of how a reaction happens** — which bonds break, which bonds form, in what order, and which species attacks which."},
        {"type": "p", "text": "A balanced equation tells you **what goes in and what comes out**. A mechanism tells you **how it got there**. Curly arrows show where the electron pairs move during the reaction."},
        {"type": "list", "items": [
            "Which **covalent bond breaks** — and whether one atom keeps both electrons or they are shared out.",
            "Which **species attacks** — the nucleophile or the electrophile.",
            "Which **new bond forms** — shown by a **curly arrow** drawn from the electron pair to the atom it bonds to.",
            "**Partial charges δ+ and δ−** mark the polar bonds that let the attacking species find its target.",
        ]},
        {"type": "p", "text": "In this topic the mechanisms you describe are the **nucleophilic substitution** reactions of **primary** halogenoalkanes (section 10.9)."},
    ],
)

S103 = _sec(
    3, "heterolytic-fission", "10.3", "Heterolytic Fission: Electrophiles and Nucleophiles",
    "Both bonding electrons to one atom — the products that attack.",
    12, "10.3", "understand that heterolytic bond breaking results in species that are electrophiles or nucleophiles",
    [],
    [
        {"type": "def", "term": "Homolytic fission", "text": "A covalent bond splits **evenly** — each bonding atom keeps **one** of the shared electrons. The products are **free radicals** (Topic 4)."},
        {"type": "def", "term": "Heterolytic fission", "text": "A covalent bond splits **unevenly** — **one atom takes both** of the shared electrons. The products are oppositely charged **ions**: a **cation and an anion**."},
        {"type": "eq", "code": "C₂H₅—Br  →  C₂H₅⁺  +  :Br⁻", "caption": "Heterolytic fission of the C–Br bond: both bonding electrons go to the bromine atom."},
        {"type": "p", "text": "Heterolytic bond breaking results in species that are **electrophiles or nucleophiles** — the two attackers of organic chemistry:"},
        {"type": "def", "term": "Electrophile", "text": "An **electron-pair acceptor** — attracted to regions of **high electron density**, such as the electron-rich C=C double bond (Topic 5)."},
        {"type": "def", "term": "Nucleophile", "text": "An **electron-pair donor** — it attacks an electron-deficient (δ+) atom. Full definition in section 10.4."},
        {"type": "callout", "variant": "exam", "title": "Name the fission from where the electrons go", "text": "Both electrons of the shared pair to **one atom** = **heterolytic fission**; one electron each = **homolytic fission**. The ions produced by heterolytic fission are exactly the species that attack in the mechanisms of this topic."},
    ],
)

S104 = _sec(
    4, "nucleophiles", "10.4", "Nucleophiles",
    "The definition, word for word — and the four to know.",
    8, "10.4", "know the definition of the term ‘nucleophile’",
    [],
    [
        {"type": "def", "term": "Nucleophile", "text": "An **electron-pair donor**. It uses a **lone pair** of electrons to form a **covalent bond** with an electron-deficient (δ+) atom."},
        {"type": "list", "items": [
            "**OH⁻** — the hydroxide ion (aqueous alkali).",
            "**:NH₃** — the ammonia molecule (alcoholic ammonia).",
            "**CN⁻** — the cyanide ion (alcoholic potassium cyanide).",
            "**H₂O** — water (aqueous silver nitrate in ethanol).",
        ]},
        {"type": "p", "text": "All four attack the same target in this topic — the δ+ carbon atom of a polar C–X bond."},
        {"type": "callout", "variant": "exam", "title": "The definition is a mark on its own", "text": "A nucleophile is an **electron-pair donor** — the mark is for those words. ‘Something that attacks a positive carbon’ does not earn it. Keep the four examples ready."},
    ],
)

S105 = _sec(
    5, "bond-polarity-and-mechanism", "10.5", "Bond Polarity and Mechanism Type",
    "A polar C–X bond puts a δ+ on carbon — that decides the mechanism.",
    12, "10.5", "understand the link between bond polarity and the type of reaction mechanism a compound will undergo",
    [],
    [
        {"type": "list", "items": [
            "The halogen is **more electronegative** than carbon, so the C–X bond is **polar**: **carbon is always δ+ and the halogen is always δ−**.",
            "The polarity produces an **electron-deficient carbon atom, Cδ+** — the site that **nucleophiles attack**.",
            "So **bond polarity decides the type of mechanism** the compound undergoes: a polar C–X bond invites **nucleophilic substitution**; an electron-rich C=C double bond invites **electrophilic addition** (Topic 5).",
        ]},
        {"type": "figure", "src": "/diagrams/t10-nucleophile-attack.png", "srcDark": "/diagrams/t10-nucleophile-attack-dark.png",
         "alt": "The polar C–X bond with δ+ carbon attacked by a nucleophile donating a lone pair, the halogen leaving as X−",
         "caption": "Polarity puts a δ+ on carbon — the nucleophile's lone pair finds it, and the halogen leaves with the bonding pair."},
        {"type": "callout", "variant": "tip", "title": "The chain that explains the topic", "text": "**electronegativity → polar C–X bond → δ+ carbon → nucleophilic attack.**"},
    ],
)

SECTIONS_O1 = [S100, S101, S102, S103, S104, S105]
