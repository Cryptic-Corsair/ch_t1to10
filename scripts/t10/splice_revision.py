#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Topic 10 full revision — close every gap between the four source notes and
the built content. Verbatim additions from:
  - Halogenoalkane.pdf  -> 10.6 isomerism + Ex1/Ex2, 10.7 check point,
        10.8 missing equations + amine chain + KCN sodium + Ex3, 10.9 Ex4 scheme,
        10.10 Ex4 Q2, 10.13 fine
  - Alcohols.pdf        -> 10.15 bond-angle figure + Ex1, 10.16 solubility figure,
        10.18 Ex2 MCQs, 10.19 five apparatus figures + Ex3 Q1/Q2
  - Mass spectra with ans.pdf -> 10.21 ethane fragmentation + Ex1/Q2/Q3/Q4/Q6/
        Q7/Ex2-Q1/Q14 worked examples + two figures
New flashcards 20-22. estMinutes bumped for expanded sections."""
import json
import os
import shutil
import sys

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure"}
errors = []


def fig(src, alt, caption):
    return {"type": "figure", "src": src, "srcDark": src.replace(".png", "-dark.png"),
            "alt": alt, "caption": caption}


def worked(title, problem, steps, answer):
    return {"type": "worked", "title": title, "problem": problem,
            "steps": steps, "answer": answer}


def h3(t):
    return {"type": "h3", "text": t}


def p(t):
    return {"type": "p", "text": t}


def lst(items):
    return {"type": "list", "items": items}


def eq(code, caption):
    return {"type": "eq", "code": code, "caption": caption}


def callout(variant, title, text):
    return {"type": "callout", "variant": variant, "title": title, "text": text}


# --------------------------------------------------------------- 10.6 ----
ADD_106 = [
    worked("Exercise 1 — write the IUPAC names",
           "From the notes: write the IUPAC names of 1. CH₃Br · 2. C₂H₅F · "
           "3. IH₂C–CH₂–CH₂–I · 4. H₃C–CH₂–CH(Cl)–CH₃ · 5. H₃C–CH(Cl)–CH(Cl)–CH₂Cl "
           "(and the three drawn structures 6–8, each a skeletal drawing to name).",
           ["**CH₃Br → bromomethane** — no locant is needed with only two carbons.",
            "**C₂H₅F → fluoroethane** — the halogen is fluoro- on the only possible position.",
            "**IH₂C–CH₂–CH₂–I → 1,3-diiodopropane** — two iodine atoms, di- plus locants.",
            "**H₃C–CH₂–CH(Cl)–CH₃ → 2-chlorobutane** — four-carbon chain, chloro on C2.",
            "**H₃C–CH(Cl)–CH(Cl)–CH₂Cl → 1,2-dichlorobutane** — number from the end "
            "nearer the substituents, so the locants are the lowest: 1 and 2."],
           "1 bromomethane · 2 fluoroethane · 3 1,3-diiodopropane · 4 2-chlorobutane · "
           "5 1,2-dichlorobutane."),
    h3("Isomers of halogenoalkanes"),
    p("**Isomers** are the organic compounds which have the **same molecular formula but "
      "different structural formula and properties**. The phenomenon is called "
      "**isomerism**. Haloalkanes can exhibit the following types of isomerism:"),
    lst([
        "**Chain isomerism** — occurs due to **branching in carbon chains**.",
        "**Position isomerism** — occurs due to the **position in which the functional "
        "group is present**.",
    ]),
    worked("Exercise 2 — draw, name and classify all the isomers",
           "From the notes: draw the displayed formula and skeletal formula for all the "
           "possible isomers of C₄H₉Br and C₅H₁₁Br, and name and classify each isomer "
           "as primary, secondary or tertiary.",
           ["**C₄H₉Br — four isomers:** 1-bromobutane (primary, one alkyl group on the "
            "C–Br carbon) · 2-bromobutane (secondary, two) · 1-bromo-2-methylpropane "
            "(primary) · 2-bromo-2-methylpropane (tertiary, three).",
            "**C₅H₁₁Br — eight isomers:** 1-bromopentane (1°) · 2-bromopentane (2°) · "
            "3-bromopentane (2°) · 1-bromo-2-methylbutane (1°) · 1-bromo-3-methylbutane "
            "(1°) · 2-bromo-2-methylbutane (3°) · 2-bromo-3-methylbutane (2°) · "
            "1-bromo-2,2-dimethylpropane (1°).",
            "The class is decided by the **number of carbon atoms attached to the carbon "
            "holding the halogen** — the classification of section 10.7."],
           "Four isomers of C₄H₉Br and eight of C₅H₁₁Br — one tertiary (2-bromo-2-"
           "methylpropane for C₄H₉Br; 2-bromo-2-methylbutane for C₅H₁₁Br)."),
]

# --------------------------------------------------------------- 10.7 ----
ADD_107 = [
    worked("Check point — fluoroalkanes vs chloroalkanes",
           "From the notes: why are nucleophiles more strongly attracted to "
           "fluoroalkanes than to chloroalkanes?",
           ["Fluorine has a **greater electronegativity** than chlorine, so the C–F bond "
            "is **more polar** than the C–Cl bond.",
            "The carbon in C–F therefore carries a **larger δ+ charge** — it is more "
            "**electron-deficient**.",
            "Nucleophiles are **electron-pair donors** attracted to electron-deficient "
            "(δ+) carbon atoms — the more δ+ the carbon, the stronger the attraction.",
            "Note the flip side (section 10.13): despite this polarity, fluoroalkanes "
            "react **most slowly**, because the C–F bond is the **strongest**."],
           "Because fluorine is the most electronegative halogen — the C–F bond is the "
           "most polar, so its carbon is the most electron-deficient (δ+) and attracts "
           "nucleophiles most strongly."),
]

# --------------------------------------------------------------- 10.8 ----
EQ_2CHLOROPROPANE = eq(
    "CH₃CH(Cl)CH₃  +  :OH⁻(aq)  →  CH₃CH(OH)CH₃  +  :Cl⁻",
    "2-chloropropane + aqueous potassium hydroxide, heated under reflux → propan-2-ol.")
EQ_ETHANOLIC_BRomo = eq(
    "CH₃CH₂Br  +  OH⁻  →  CH₂=CH₂  +  Br⁻  +  H₂O",
    "Bromoethane + ethanolic potassium hydroxide, heated under reflux → ethene.")
EQ_2CHLOROBUTANE = eq(
    "CH₃CH₂CH(Cl)CH₃  +  OH⁻  →  CH₃CH=CHCH₃  +  CH₃CH₂CH=CH₂  +  H₂O  +  Cl⁻",
    "2-chlorobutane (unsymmetrical) → a mixture of isomeric alkenes: but-2-ene and "
    "but-1-ene.")
P_AMINE_FURTHER = p("**Amino propane can further react with 1-chloropropane** — the "
                    "amine formed is itself a nucleophile, so the chain keeps growing:")
EQ_DIPROPYL = eq(
    "CH₃CH₂CH₂NH₂  +  CH₃CH₂CH₂Cl  →  (CH₃CH₂CH₂)₂NH  +  HCl",
    "A second substitution — the product is dipropylamine (a secondary amine).")
EQ_TRIPROPYL = eq(
    "(CH₃CH₂CH₂)₂NH  +  CH₃CH₂CH₂Cl  →  (CH₃CH₂CH₂)₃N  +  HCl",
    "And again — the product is tripropylamine (a tertiary amine).")
ADD_108_AFTER_PROPYLAMINE = [P_AMINE_FURTHER, EQ_DIPROPYL, EQ_TRIPROPYL]
ADD_108_EX3 = [
    worked("Exercise 3 — chloroethane two ways",
           "From the notes: complete the table for the reaction of chloroethane with "
           "aqueous NaOH and with ethanolic NaOH — condition, type of reaction, role of "
           "the OH⁻ ion (given: acts as a nucleophile / acts as a base), product and "
           "equation.",
           ["**Aqueous NaOH:** heat under reflux in aqueous solution · **nucleophilic "
            "substitution** · OH⁻ acts as a **nucleophile** · product **ethanol** · "
            "CH₃CH₂Cl + OH⁻ → CH₃CH₂OH + Cl⁻.",
            "**Ethanolic NaOH:** heat under reflux in ethanolic solution · "
            "**elimination** · OH⁻ acts as a **base** · product **ethene** · "
            "CH₃CH₂Cl + OH⁻ → CH₂=CH₂ + H₂O + Cl⁻.",
            "Same reagent ion, different solvent — the solvent decides the role of "
            "OH⁻ and therefore the whole reaction."],
           "Aqueous → substitution, ethanol. Ethanolic → elimination, ethene."),
]

# --------------------------------------------------------------- 10.9 ----
ADD_109 = [
    h3("Exercise 4 — the halogenoalkane scheme"),
    fig("/diagrams/t10-halo-scheme.png",
        "Reaction scheme: C4H9Br connected by arrows A, B, C and D to C4H8, C4H9OH and C4H9NH2",
        "Halogenoalkanes are important intermediates in organic chemistry — identify the "
        "reagents and conditions for A, B, C and D, then classify the type of reaction "
        "in A and D."),
    worked("Exercise 4 — reagents, conditions and reaction types",
           "Identify the reagents and any specific conditions required for A, B, C and D "
           "(a suitable temperature is maintained in each reaction), then classify the "
           "type of reaction in each of A and D.",
           ["**A (C₄H₉Br → C₄H₈):** **ethanolic potassium hydroxide**, heated under "
            "reflux — OH⁻ acts as a **base**.",
            "**B (C₄H₉Br → C₄H₉OH):** **aqueous potassium hydroxide (KOH(aq))**, heated "
            "under reflux — OH⁻ acts as a **nucleophile**.",
            "**C (C₄H₉OH → C₄H₉Br):** **50% concentrated sulfuric acid and potassium "
            "bromide**, heated under reflux (the bromination of an alcohol, section "
            "10.17).",
            "**D (C₄H₉Br → C₄H₉NH₂):** **alcoholic ammonia**, heated **under pressure in "
            "a sealed tube** — NH₃ acts as a **nucleophile**.",
            "**Classify:** A is **elimination**; D is **nucleophilic substitution**."],
           "A ethanolic KOH, reflux (elimination) · B aqueous KOH, reflux "
           "(nucleophilic substitution) · C KBr + 50% concentrated H₂SO₄, reflux · "
           "D alcoholic NH₃, pressure, sealed tube (nucleophilic substitution)."),
]

# --------------------------------------------------------------- 10.10 ----
ADD_1010 = [
    h3("Exercise 4, Q2 — isomers and a yellow precipitate"),
    worked("Exercise 4, Q2 — 1-iodobutane with hot aqueous silver nitrate",
           "1-iodobutane, dissolved in ethanol, reacts with hot aqueous silver nitrate "
           "to form a yellow precipitate. The reaction involves two steps. (a) Draw "
           "skeletal formulae of the four structural isomers of C₄H₉I. (b)(i) In the "
           "first step, 1-iodobutane forms butan-1-ol — identify the attacking reagent, "
           "and state the type and mechanism of this reaction. (ii) Write the ionic "
           "equation for the formation of the precipitate.",
           ["**(a)** The four structural isomers of C₄H₉I: **1-iodobutane · "
            "2-iodobutane · 1-iodo-2-methylpropane · 2-iodo-2-methylpropane** — drawn as "
            "skeletal zig-zags with the I label on C1, C2, C2 of a branched chain, and "
            "the central carbon respectively.",
            "**(b)(i) Attacking reagent: water** (water acts as the nucleophile in "
            "aqueous silver nitrate — the ethanol is only the solvent). **Type: "
            "hydrolysis** — water or hydroxide ions replace an atom in a molecule with "
            "an –OH group. **Mechanism: nucleophilic substitution.**",
            "**(b)(ii)** The yellow precipitate is silver iodide: "
            "**Ag⁺(aq) + I⁻(aq) → AgI(s)** — yellow, so the halogen is iodine."],
           "(a) 1-iodobutane, 2-iodobutane, 1-iodo-2-methylpropane, 2-iodo-2-"
           "methylpropane · (b)(i) water; hydrolysis; nucleophilic substitution · "
           "(b)(ii) Ag⁺ + I⁻ → AgI."),
]

# --------------------------------------------------------------- 10.15 ----
FIG_BOND_ANGLES = fig(
    "/diagrams/t10-alcohol-bond-angles.png",
    "Ethanol displayed with the 109.5° tetrahedral angles at carbon and the 104.5° "
    "bent angle at the oxygen, with its two lone pairs",
    "All the H–C–H bonds and C–C–O are 109.5° (tetrahedral). The H–O–C bond is 104.5° "
    "(bent line shape) — the oxygen's lone pairs repel more than bond pairs.")
ADD_1015_EX1 = [
    worked("Exercise 1 — name them, then draw them",
           "From the notes: write the IUPAC names of 2. CH₃OH · 3. C₂H₅OH · "
           "4. H₃C–CH₂–CH₂–OH · 5. H₃C–CH₂–CH(OH)–CH₃ · 6. (CH₃)₃COH. Then draw the "
           "displayed and skeletal structure of 3-methylpentan-3-ol, 2,2-dimethylpropan-"
           "1-ol, cyclopentanol, 3-chloro-2-methylhexan-1-ol, cyclohexanol and "
           "2-methylpentan-2-ol.",
           ["**CH₃OH → methanol** · **C₂H₅OH → ethanol** — no locant needed with only "
            "two carbons.",
            "**H₃C–CH₂–CH₂–OH → propan-1-ol** · **H₃C–CH₂–CH(OH)–CH₃ → butan-2-ol** — "
            "the locant shows where the –OH sits.",
            "**(CH₃)₃COH → 2-methylpropan-2-ol** — the longest chain containing the "
            "–OH group is propane, with a methyl on C2 and the –OH on C2.",
            "For the drawing tasks: pick the **longest chain containing the –OH group**, "
            "number from the end that gives the –OH the lowest locant, then place every "
            "alkyl and halo substituent. In the skeletal formula only the O–H bond is "
            "labelled; in the displayed formula every bond is drawn."],
           "2 methanol · 3 ethanol · 4 propan-1-ol · 5 butan-2-ol · 6 2-methylpropan-2-ol."),
]

# --------------------------------------------------------------- 10.16 ----
FIG_SOLUBILITY = fig(
    "/diagrams/t10-alcohol-solubility.png",
    "Methanol, butanol and octanol chains with the non-polar carbon chain bracketed: "
    "very soluble, slightly soluble, very insoluble",
    "The non-polar carbon chain grows from methanol to butanol to octanol — solubility "
    "in water falls as the London forces between the chains strengthen.")

# --------------------------------------------------------------- 10.18 ----
ADD_1018_EX2 = [
    worked("Exercise 2 — three quick questions",
           "From the notes: 1. Which of the following is a secondary alcohol — A butan-"
           "1-ol · B butan-2-ol · C 2-methylpropan-1-ol · D 2-methylpropan-2-ol? "
           "2. Propan-1-ol and propan-2-ol are separately oxidized under mild conditions "
           "by acidified sodium dichromate(VI) and the product immediately distilled "
           "off — what is the oxidation product in each case? 3. The best method of "
           "converting ethanol into iodoethane is — A heat iodine and ethanol under "
           "reflux · B react ethanol and potassium iodide in the presence of dilute "
           "acid · C heat potassium iodide and ethanol with concentrated sulfuric acid "
           "· D heat red phosphorus, ethanol and iodine under reflux.",
           ["**1 → B, butan-2-ol** — the carbon carrying the –OH is joined directly to "
            "**two alkyl groups** (butan-1-ol and 2-methylpropan-1-ol are primary; "
            "2-methylpropan-2-ol is tertiary).",
            "**2 → A: propanal from propan-1-ol, propanone from propan-2-ol** — "
            "distilling the product as it forms stops at the aldehyde, and a secondary "
            "alcohol can only be oxidised to a ketone.",
            "**3 → D** — iodination needs **iodine and moist red phosphorus**, warmed: "
            "2P + 3I₂ → 2PI₃, then 3C₂H₅OH + PI₃ → 3C₂H₅I + H₃PO₃. Concentrated "
            "sulfuric acid would oxidise the iodide (the same reason it must be 50% for "
            "bromide)."],
           "1 B butan-2-ol · 2 A propanal + propanone · 3 D red phosphorus, ethanol and "
           "iodine under reflux."),
]

# --------------------------------------------------------------- 10.19 ----
FIG_DISTILLATION = fig(
    "/diagrams/t10-apparatus-distillation.png",
    "Labelled distillation apparatus: thermometer with bulb at the T junction, Liebig "
    "condenser with water in at the bottom, distillate collected, round-bottomed flask "
    "with anti-bumping granules over heat",
    "Distillation — the thermometer bulb sits at the T junction connecting to the "
    "condenser, water goes in the bottom of the condenser against gravity, and the "
    "distillate is collected in a flask.")
FIG_REFLUX = fig(
    "/diagrams/t10-apparatus-reflux.png",
    "Labelled reflux apparatus: vertical Liebig condenser with open top, water out at "
    "the top and water in at the bottom, pear-shaped flask with anti-bumping granules "
    "over heat, vapour condensing back",
    "Heat under reflux — the condenser prevents organic vapours from escaping by "
    "condensing them back to liquids; never seal the end of the condenser.")
FIG_FRACTIONAL = fig(
    "/diagrams/t10-apparatus-fractional.png",
    "Fractional distillation apparatus: fractionating column packed with glass beads on "
    "a flask, side-arm condenser with water out and water in, receiver flask",
    "Fractional distillation — separation of a liquid mixture into fractions differing "
    "in boiling point, typically using a fractionating column.")
FIG_SEPARATING = fig(
    "/diagrams/t10-apparatus-separating.png",
    "Separating funnel clamped to a stand with oil as the top layer and water as the "
    "bottom layer, stop-cock open above a conical flask",
    "Separating funnel — two immiscible liquids form two layers; the denser solvent "
    "will be the bottom layer, and the stop-cock controls the flow.")
FIG_BP = fig(
    "/diagrams/t10-bp-determination.png",
    "Boiling point determination: sample tube with capillary tube inside a heating oil "
    "bath, thermometer through glass tubing with the bulb above the liquid surface",
    "Boiling point determination — the thermometer bulb must sit above the level of the "
    "surface of the boiling liquid, measuring the temperature of the saturated vapour.")

ADD_1019_EX = [
    h3("Exercise 3 — from the notes"),
    worked("Exercise 3, Q1 — ethanol oxidised, collected and tested",
           "Alcohols, such as ethanol, undergo a number of reactions. (a) Write the "
           "balanced equation for the oxidation of ethanol to ethanoic acid using "
           "displayed formulae and the symbol [O]. (b) Ethanol can be oxidized to the "
           "aldehyde, ethanal, using the distillation apparatus: (i) state the class of "
           "alcohols that can be oxidized to aldehydes; (ii) explain fully why ethanal, "
           "rather than ethanoic acid, is produced and collected; (iii) state the "
           "purpose of the part of the apparatus labelled A (the receiver). (c) The "
           "distillation product, ethanal, is dried — suggest one reagent that could "
           "test for both ethanol and ethanoic acid in the presence of ethanal. (d) "
           "Write the equation for the complete combustion of propane-1,2,3-triol "
           "(glycerol, C₃H₈O₃), and a possible equation for its combustion in a limited "
           "supply of oxygen with a likely observation. (e) Halogenoalkanes react with "
           "aqueous hydroxide ions to form the corresponding alcohol — name the type of "
           "reaction and mechanism, and choose a halogenoalkane that will react in this "
           "way to form ethanol.",
           ["**(a)** CH₃CH₂OH + 2[O] → CH₃COOH + H₂O — drawn with **every bond shown** "
            "in the displayed formulae of reactants and products.",
            "**(b)(i) Primary alcohols.** **(ii)** Ethanal has a **lower boiling "
            "temperature** than the reaction mixture, so it **distils off as it forms** "
            "— distillation **removes it from contact with the oxidising agent**, so the "
            "oxidation cannot continue (under reflux it would condense back and be "
            "oxidised further to ethanoic acid). **(iii) A collects (and condenses) the "
            "distillate.**",
            "**(c) PCl₅** — misty fumes of HCl form with the **–OH group** of ethanol or "
            "ethanoic acid; ethanal has **no –OH group**, so it gives no fumes.",
            "**(d)** Complete: **C₃H₈O₃ + 3.5O₂ → 3CO₂ + 4H₂O**. Limited oxygen: "
            "**C₃H₈O₃ + 2O₂ → 3C + 4H₂O** — observation: a **smoky (yellow) flame with "
            "carbon (soot) formed**.",
            "**(e) Nucleophilic substitution** — the hydroxide ion acts as a "
            "**nucleophile** (mechanism in section 10.9). Use **bromoethane, CH₃CH₂Br** "
            "+ :OH⁻(aq) → CH₃CH₂OH + Br⁻."],
           "(a) CH₃CH₂OH + 2[O] → CH₃COOH + H₂O · (b) primary; distilled off as it "
           "forms, removed from the oxidant; A collects the distillate · (c) PCl₅, "
           "misty fumes · (d) C₃H₈O₃ + 3.5O₂ → 3CO₂ + 4H₂O; C₃H₈O₃ + 2O₂ → 3C + 4H₂O, "
           "smoky flame · (e) nucleophilic substitution; bromoethane."),
    worked("Exercise 3, Q2 — isomers, reflux and halogenoalkanes",
           "This is a question about alcohols. (a) There are two alcohol structural "
           "isomers with the molecular formula C₃H₈O — give the skeletal formula, "
           "systematic name and classification of each. (b) Ethanol can be oxidised by "
           "acidified sodium dichromate(VI) to ethanal and then to ethanoic acid: "
           "(i) complete the ionic half-equation for the reduction of the dichromate(VI) "
           "ions to chromium(III) ions; (ii) describe how the reflux apparatus ensures "
           "that any ethanal initially produced is further oxidised. (c) Write the "
           "equation for the reaction between methanol and PCl₅ and state the "
           "observation. (d) Draw the mechanism for the reaction of 1-bromopropane with "
           "aqueous alkali; the reaction with concentrated alcoholic alkali forms a "
           "different organic product — name the type of reaction and give the displayed "
           "formula of the product. (e) How would you test for the OH group in "
           "2-methylpropan-2-ol without using phosphorus(V) chloride? Name the reagent "
           "and state the observation for a positive test.",
           ["**(a)** **Propan-1-ol, CH₃CH₂CH₂OH — primary** (the –OH carbon is attached "
            "to one alkyl group) and **propan-2-ol, CH₃CH(OH)CH₃ — secondary** (attached "
            "to two); drawn as three-carbon skeletal zig-zags with –OH on the end or "
            "middle carbon.",
            "**(b)(i)** **Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O** — orange to green. "
            "**(ii)** The condenser **prevents the ethanal escaping**: it condenses "
            "**back into the mixture**, so it stays in contact with the oxidising agent "
            "and is **oxidised further** to ethanoic acid.",
            "**(c)** **CH₃OH + PCl₅ → CH₃Cl + POCl₃ + HCl** — observation: **misty "
            "fumes of HCl** (this is the qualitative test for the –OH group).",
            "**(d)** Lone pair of **:OH⁻** attacks the δ+ carbon of CH₃CH₂CH₂Br, the "
            "C–Br bond breaks heterolytically → **propan-1-ol** (mechanism: figure in "
            "section 10.9). With concentrated alcoholic alkali: **elimination** — the "
            "product is **propene**, displayed formula H₂C=CH–CH₃ with every bond drawn.",
            "**(e) Concentrated hydrochloric acid**, mixed by shaking at room "
            "temperature (the tertiary-alcohol chlorination) — a **positive test is the "
            "mixture turning cloudy as insoluble 2-chloro-2-methylpropane forms** "
            "(Core Practical 6)."],
           "(a) propan-1-ol (1°) and propan-2-ol (2°) · (b) Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → "
           "2Cr³⁺ + 7H₂O; aldehyde condenses back and is oxidised further · (c) "
           "CH₃OH + PCl₅ → CH₃Cl + POCl₃ + HCl, misty fumes · (d) nucleophilic "
           "substitution → propan-1-ol; elimination → propene · (e) concentrated HCl, "
           "mixture goes cloudy."),
]

# --------------------------------------------------------------- 10.21 ----
FIG_ETHANE = fig(
    "/diagrams/t10-ms-ethane.png",
    "Ethane displayed formula bombarded by an electron, fragmenting into the molecular "
    "ion at m/z 30, CH3CH2+ at 29 plus H radical, and CH3+ at 15 plus CH3 radical not "
    "detected",
    "Fragmentation of the ethane molecular ion — the charged fragment is detected, the "
    "neutral radical is not.")
FIG_PENTANE = fig(
    "/diagrams/t10-ms-pentane.png",
    "Mass spectrum of pentane with labelled peaks C at m/z 15, B at 29, A at 43, D at "
    "57 and the molecular ion at 72",
    "Exercise 1 — the mass spectrum of pentane, C₅H₁₂: peaks C (15), B (29), A (43), "
    "D (57) and the molecular ion (72).")

ADD_1021_ETHANE = [
    h3("Fragmentation step by step — ethane"),
    FIG_ETHANE,
    worked("Ethane under the beam",
           "Ethane is ionised and fragmented in the mass spectrometer. Account for the "
           "peaks at m/z 30, 29 and 15, and state which species is not detected.",
           ["**Ionisation:** CH₃CH₃ + e⁻ → **CH₃CH₃⁺•** + 2e⁻ — the **molecular ion**, "
            "**m/z = 30**.",
            "**First fragmentation:** the molecular ion breaks into **CH₃CH₂⁺ (m/z 29)** "
            "plus a neutral **H•** radical.",
            "**Further fragmentation:** CH₃CH₂⁺ → **CH₃⁺ (m/z 15)** plus **•CH₃** — the "
            "methyl radical carries no charge, so it is **not detected by MS**.",
            "Only the fragments with the **positive charge** are detected by the "
            "spectrometer."],
           "30 = CH₃CH₃⁺• (molecular ion) · 29 = CH₃CH₂⁺ · 15 = CH₃⁺ — the neutral "
           "partners (H•, •CH₃) are not detected."),
]

ADD_1021_EX = [
    h3("The exercises — spectrum by spectrum"),
    FIG_PENTANE,
    worked("Exercise 1 — the pentane spectrum",
           "The mass spectrum of pentane (C₅H₁₂) shows peaks C (15), B (29), A (43), "
           "D (57) and the molecular ion (72). (a) Write an equation for the formation "
           "of the molecular ion of pentane. (b) The molecular ion can fragment in "
           "several ways — label the species which has given rise to each of the "
           "labelled peaks.",
           ["**(a)** **C₅H₁₂ + e⁻ → C₅H₁₂⁺• + 2e⁻** — loss of one electron.",
            "**(b)** Breaking the chain between carbons gives: **CH₃⁺ (15, peak C)** + "
            "•CH₂CH₂CH₂CH₃, or CH₃• + **CH₃CH₂CH₂CH₂⁺ (57, peak D)**; and **CH₃CH₂⁺ "
            "(29, peak B)** + •CH₂CH₂CH₃, or CH₃CH₂• + **CH₃CH₂CH₂⁺ (43, peak A)**.",
            "**The molecular ion at 72** is C₅H₁₂⁺• — the peak furthest to the right."],
           "C 15 = CH₃⁺ · B 29 = CH₃CH₂⁺ · A 43 = CH₃CH₂CH₂⁺ (base peak) · "
           "D 57 = CH₃CH₂CH₂CH₂⁺ · 72 = C₅H₁₂⁺•."),
    worked("Question 2 — the decane spectrum",
           "The mass spectrum of decane (CH₃CH₂CH₂CH₂CH₂CH₂CH₂CH₂CH₂CH₃) shows a base "
           "peak and successive peaks 14 units apart, with the molecular ion at 142. "
           "Give the formula of the species that has given rise to the peaks at m/z 43, "
           "57, 71, 85, 99, 113 and 142.",
           ["Successive peaks **14 units apart** mean **CH₂ units** along a chain.",
            "**43 → CH₃CH₂CH₂⁺ (C₃H₇⁺)** — the base peak · **57 → C₄H₉⁺** · "
            "**71 → C₅H₁₁⁺** · **85 → C₆H₁₃⁺** · **99 → C₇H₁₅⁺** · **113 → C₈H₁₇⁺**.",
            "**142 → C₁₀H₂₂⁺•** — the **molecular ion** (Mᵣ of decane = 142)."],
           "43 C₃H₇⁺ · 57 C₄H₉⁺ · 71 C₅H₁₁⁺ · 85 C₆H₁₃⁺ · 99 C₇H₁₅⁺ · 113 C₈H₁₇⁺ · "
           "142 C₁₀H₂₂⁺•."),
    worked("Question 3 — the ethanol spectrum",
           "The mass spectrum of ethanol shows peaks A (15), B (17), C (29), D (31), "
           "E (45) and F (46). Give the formula of the species that has given rise to "
           "each peak.",
           ["**A 15 → CH₃⁺** · **B 17 → OH⁺** · **C 29 → CH₃CH₂⁺**.",
            "**D 31 → CH₂OH⁺** · **E 45 → CH₃CH₂O⁺** · **F 46 → CH₃CH₂OH⁺** — the "
            "**molecular ion**.",
            "Read each as a subtraction from M = 46: 46 − 15 → 31 (loss of CH₃), "
            "46 − 17 → 29 (loss of OH), 46 − 45 → 1 (loss of H)."],
           "15 CH₃⁺ · 17 OH⁺ · 29 CH₃CH₂⁺ · 31 CH₂OH⁺ · 45 CH₃CH₂O⁺ · 46 CH₃CH₂OH⁺."),
    worked("Question 4 — the pentan-3-one spectrum",
           "The mass spectrum of pentan-3-one shows peaks at m/z 29, 57 and 86. Give "
           "the formula of the species that has given rise to these peaks.",
           ["**29 → CH₃CH₂⁺** — the ethyl cation.",
            "**57 → CH₃CH₂CO⁺** — the acyl fragment, split off one side of the C=O.",
            "**86 → CH₃CH₂COCH₂CH₃⁺** — the **molecular ion** (Mᵣ of pentan-3-one, "
            "C₅H₁₀O, = 86)."],
           "29 CH₃CH₂⁺ · 57 CH₃CH₂CO⁺ · 86 CH₃CH₂COCH₂CH₃⁺."),
    worked("Question 6 — which compound is it?",
           "A simplified mass spectrum of an organic compound shows peaks at m/z 15, 43 "
           "and 58. Which of the following produces this spectrum — A propane · "
           "B propan-1-ol · C propan-2-ol · D propanone?",
           ["**m/z 15 → CH₃⁺** — a methyl fragment.",
            "**m/z 43 → CH₃CO⁺** — the acylium fragment, characteristic of a ketone.",
            "**m/z 58 → CH₃COCH₃⁺** — the **molecular ion**; Mᵣ = 58 fits C₃H₆O "
            "(propanone). Propane (44) and the propanols (60) do not match."],
           "D — propanone (15 CH₃⁺ · 43 CH₃CO⁺ · 58 CH₃COCH₃⁺)."),
    worked("Question 7 — compound S",
           "A compound S with the molecular formula C₃H₆O gave a mass spectrum with "
           "peaks at m/z 58, 43 and 15. Identify the species responsible for the peaks "
           "and give the structural formula of S.",
           ["**15 → CH₃⁺** · **43 → CH₃CO⁺** · **58 → CH₃COCH₃⁺** — the **molecular "
            "ion** (C₃H₆O = 58).",
            "CH₃⁺ and CH₃CO⁺ join through the carbonyl carbon — the skeleton is "
            "CH₃–CO–CH₃.",
            "The peak at 43 (CH₃CO⁺) is what ketones characteristically show."],
           "S is propanone, CH₃COCH₃ — structural formula CH₃–C(=O)–CH₃."),
    worked("Exercise 2, Q1 — two identical peaks for C₄H₉Br",
           "An alkene, C₄H₈, reacts with HBr to form compound B, C₄H₉Br. Suggest why "
           "the mass spectrum obtained for B has two identical peaks at m/z values 136 "
           "and 138, and write the formula of the species which produced these peaks.",
           ["Bromine has **two isotopes, ⁷⁹Br and ⁸¹Br**, which exist in **equal "
            "quantities**.",
            "The molecular ion peaks **M and M+2** therefore appear in the ratio "
            "**1 : 1**, two m/z units apart.",
            "**(C₄H₉–⁷⁹Br)⁺ → m/z 136** (57 + 79) · **(C₄H₉–⁸¹Br)⁺ → m/z 138** "
            "(57 + 81)."],
           "M and M+2 in a 1 : 1 ratio — (C₄H₉–⁷⁹Br)⁺ at 136 and (C₄H₉–⁸¹Br)⁺ at 138."),
    worked("Question 14 — methanol and ethanol compared",
           "Methanol and ethanol have a number of fragment peaks which appear in the "
           "mass spectra of both compounds but, somewhat surprisingly, the OH⁺ peak at "
           "m/e = 17 is not one of them. (i) Suggest the formulae and m/e values of two "
           "fragment ions that you would expect to occur in both spectra. (ii) Give the "
           "formula of one fragment ion that you would expect to be present in the mass "
           "spectrum of ethanol but absent from that of methanol.",
           ["**(i)** Both molecules contain **CH₃–O–** … and a methyl group: "
            "**CH₃⁺ at m/e 15** and **CH₂OH⁺ (or CH₃O⁺) at m/e 31**.",
            "**(ii)** **CH₃CH₂⁺ at m/e 29** — only ethanol has the extra CH₂ to give the "
            "ethyl fragment."],
           "(i) CH₃⁺ (15) and CH₂OH⁺/CH₃O⁺ (31) · (ii) CH₃CH₂⁺ (29)."),
]

# ----------------------------------------------------------- flashcards ----
NEW_CARDS = [
    (20, "CORE", "What are the two types of isomerism shown by halogenoalkanes?",
     "Chain isomerism — occurs due to branching in carbon chains — and position "
     "isomerism — occurs due to the position in which the functional group is present. "
     "Isomers have the same molecular formula but different structural formula and "
     "properties."),
    (21, "EXAM", "Which labels must a correct distillation or reflux apparatus show?",
     "Thermometer bulb at the T junction connecting to the condenser; water in at the "
     "bottom of the condenser (against gravity — efficient cooling, prevents back flow); "
     "anti-bumping granules in the flask; never seal the end of the condenser; electric "
     "heaters because organic chemicals are highly flammable."),
    (22, "EXAM", "The mass spectrum of C4H9Br shows two peaks of equal height at m/z "
     "136 and 138. Explain.",
     "M and M+2 molecular ion peaks in a 1:1 ratio — bromine has two isotopes, 79Br and "
     "81Br, in equal quantities. (C4H9–79Br)+ = 136 and (C4H9–81Br)+ = 138."),
]

# ------------------------------------------------------------- the plan ----
# (section number, estMinutes, list of (anchor_substring, anchor_kind, [blocks]))
# anchor_kind: 'after-block-with-text' — insert AFTER the block containing the text
PLAN = [
    ("10.6", 30, [
        ("2,3-dichlorobutane", ADD_106),
    ]),
    ("10.7", 14, [
        ("difference in the rate", [ADD_107[0]]),
    ]),
    ("10.8", 40, [
        ("Bromoethane + aqueous potassium hydroxide", [EQ_2CHLOROPROPANE]),
        ("Ethanolic potassium hydroxide — elimination", [EQ_ETHANOLIC_BRomo]),
        ("1-chloropropane + ethanolic KOH → propene", [EQ_2CHLOROBUTANE]),
        ("1-chloropropane + concentrated ammonia → propylamine", ADD_108_AFTER_PROPYLAMINE),
        ("Same reagent, different solvent", ADD_108_EX3),
    ]),
    ("10.9", 30, [
        ("Phrases that carry the marks", ADD_109),
    ]),
    ("10.10", 28, [
        ("test to identify the halogen", ADD_1010),
    ]),
    ("10.15", 32, [
        ("Lone pairs repel more than bond pairs", [FIG_BOND_ANGLES]),
        ("root word ends with ‘ane’", ADD_1015_EX1),
    ]),
    ("10.16", 18, [
        ("octanol", [FIG_SOLUBILITY]),
    ]),
    ("10.18", 40, [
        ("Distilling as it forms removes ethanal", ADD_1018_EX2),
    ]),
    ("10.19", 50, [
        ("Never seal the condenser", [FIG_REFLUX]),
        ("selective boiling and condensation", [FIG_DISTILLATION]),
        ("fractionating column", [FIG_FRACTIONAL]),
        ("discard the unwanted aqueous layer", [FIG_SEPARATING]),
        ("changing pressure can change the boiling point", [FIG_BP]),
        ("Reflux first, distil later", ADD_1019_EX),
    ]),
    ("10.21", 55, [
        ("Read right to left", ADD_1021_ETHANE),
        ("E is ethanal, CH₃CHO", ADD_1021_EX),
    ]),
]

MINUTE_BUMPS = {"10.6": 30, "10.7": 14, "10.8": 40, "10.9": 30, "10.10": 28,
                "10.15": 32, "10.16": 18, "10.18": 40, "10.19": 50, "10.21": 55}


def block_text(b):
    parts = []
    for key in ("text", "code", "caption", "title", "problem", "answer", "src", "alt"):
        if key in b and isinstance(b[key], str):
            parts.append(b[key])
    if "items" in b:
        parts.append(" ".join(b["items"]))
    if "rows" in b:
        parts.append(" ".join(" ".join(str(c) for c in r) for r in b["rows"]))
    return " ".join(parts)


def main():
    with open(CONTENT, encoding="utf-8") as f:
        data = json.load(f)
    slug = "halogenoalkanes-alcohols-spectra"
    topic = next(t for t in data if t["slug"] == slug)

    for b in [b for _, _, ins in PLAN for _a, blocks in ins for b in blocks]:
        if b["type"] not in ALLOWED:
            errors.append("bad block type %s" % b["type"])
        if b["type"] == "figure":
            for key in ("src", "srcDark"):
                if not os.path.isfile(os.path.join(PUBLIC, b[key].lstrip("/"))):
                    errors.append("missing figure file %s" % b[key])
        if b["type"] == "worked" and set(b.keys()) != {"type", "title", "problem", "steps", "answer"}:
            errors.append("worked keys off-spec: %s" % sorted(b.keys()))
        if b["type"] == "callout" and set(b.keys()) != {"type", "variant", "title", "text"}:
            errors.append("callout keys off-spec")

    applied = 0
    for secnum, mins, insertions in PLAN:
        sec = next(s for s in topic["sections"] if s["number"] == secnum)
        used_anchors = set()
        for anchor, blocks in insertions:
            hits = [i for i, b in enumerate(sec["content"]) if anchor in block_text(b)]
            hits = [i for i in hits if i not in used_anchors]
            if not hits:
                errors.append("anchor not found in %s: %r" % (secnum, anchor))
                continue
            pos = hits[0] + 1
            sec["content"][pos:pos] = blocks
            used_anchors.add(pos - 1)
            applied += 1
        sec["estMinutes"] = MINUTE_BUMPS[secnum]

    # KCN sodium note in the reactions table of 10.8
    s8 = next(s for s in topic["sections"] if s["number"] == "10.8")
    patched_kcn = False
    for row in [b for b in s8["content"] if b["type"] == "table"]:
        row["rows"] = [[c.replace("**alcoholic KCN** |", "**alcoholic KCN (or NaCN)** |")
                        if isinstance(c, str) else c for c in r] for r in row["rows"]]
        for r in row["rows"]:
            for j, c in enumerate(r):
                if isinstance(c, str) and "alcoholic KCN" in c and "NaCN" not in c:
                    r[j] = c.replace("alcoholic KCN", "alcoholic KCN (or NaCN)")
                    patched_kcn = True
    if not patched_kcn:
        # search generically
        for b in s8["content"]:
            if b["type"] == "table":
                for r in b["rows"]:
                    for j, c in enumerate(r):
                        if isinstance(c, str) and "alcoholic KCN" in c and "NaCN" not in c:
                            r[j] = c.replace("alcoholic KCN", "alcoholic KCN (or NaCN)")
                            patched_kcn = True
    if not patched_kcn:
        errors.append("KCN row not found")

    # flashcards
    other_card_ids = {c["id"] for t in data if t["slug"] != slug for c in t.get("cards", [])}
    existing_fronts = {c["front"] for c in topic.get("cards", [])}
    added_cards = 0
    for ordn, tag, front, back in NEW_CARDS:
        cid = "cmv1eoi8l00gt10card%02d" % ordn
        if cid in other_card_ids:
            errors.append("card id clash %s" % cid)
            continue
        if front not in existing_fronts:
            topic.setdefault("cards", []).append(
                {"id": cid, "ord": ordn, "front": front, "back": back, "tag": tag})
            existing_fronts.add(front)
            added_cards += 1

    total_min = sum(s["estMinutes"] for s in topic["sections"])
    topic["estHours"] = round(total_min / 60, 1)

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    shutil.copyfile(CONTENT, CONTENT + ".bak3")
    with open(CONTENT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print("OK — %d insertion groups applied, %d cards added, estHours=%s, cards=%d"
          % (applied, added_cards, topic["estHours"], len(topic["cards"])))
    for s in topic["sections"]:
        print("  %s %-70s %3d min  %d blocks"
              % (s["number"], s["title"][:70], s["estMinutes"], len(s["content"])))


if __name__ == "__main__":
    main()
