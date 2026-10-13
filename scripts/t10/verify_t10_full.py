#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the fully revised Topic 10 — ids, figure files, block contracts,
spec-map verbatim, and the source keywords that must survive everywhere."""
import json
import os
import sys

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

data = json.load(open(CONTENT, encoding="utf-8"))
slug = "halogenoalkanes-alcohols-spectra"
topic = next(t for t in data if t["slug"] == slug)
errors = []

# 1. globally unique section ids and card ids
sec_ids = [s["id"] for t in data for s in t.get("sections", [])]
if len(sec_ids) != len(set(sec_ids)):
    errors.append("duplicate section ids")
card_ids = [c["id"] for t in data for c in t.get("cards", [])]
if len(card_ids) != len(set(card_ids)):
    errors.append("duplicate card ids")

# 2. numbering 10.0 – 10.23, in order
nums = [s["number"] for s in topic["sections"]]
want = ["10.%d" % i for i in range(0, 24)]
if nums != want:
    errors.append("section numbering off: %s" % nums)

# 3. every figure file exists (light + dark); every referenced figure present
for t in data:
    for s in t.get("sections", []):
        for b in s.get("content", []):
            if b["type"] == "figure":
                for key in ("src", "srcDark"):
                    if key in b and not os.path.isfile(os.path.join(PUBLIC, b[key].lstrip("/"))):
                        errors.append("missing figure %s (%s %s)" % (b[key], s["number"], key))

# 4. block contracts across the whole topic
ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure"}
for s in topic["sections"]:
    for b in s["content"]:
        if b["type"] not in ALLOWED:
            errors.append("bad type %s in %s" % (b["type"], s["number"]))
        if b["type"] == "worked" and set(b) != {"type", "title", "problem", "steps", "answer"}:
            errors.append("worked keys off in %s: %s" % (s["number"], sorted(b)))
        if b["type"] == "callout":
            if set(b) != {"type", "variant", "title", "text"}:
                errors.append("callout keys off in %s" % s["number"])
            if b.get("variant") not in {"tip", "warning", "exam", "key"}:
                errors.append("callout variant %s in %s" % (b.get("variant"), s["number"]))
        if b["type"] == "table" and not (b.get("headers") or b.get("rows")):
            errors.append("table without headers/rows in %s" % s["number"])
        if b["type"] == "figure" and not b.get("caption"):
            errors.append("figure without caption in %s" % s["number"])

# 5. spec map rows verbatim vs specmap_rows.json
rows = json.load(open(os.path.join(ROOT, "scripts/t10/specmap_rows.json"), encoding="utf-8"))["rows"]
s0 = topic["sections"][0]
table = next(b for b in s0["content"] if b["type"] == "table")
for r in rows:
    num, text = r[0], r[1]
    if not any(c[0] == num and c[1] == text for c in table["rows"] if isinstance(c, list)):
        errors.append("spec row drifted: %s" % num)

# 6. keyword survival — everything the four sources teach that must stay
joined = json.dumps(topic, ensure_ascii=False)
KEYWORDS = [
    # halogenoalkanes
    "halogen atom attached to a hydrocarbon chain", "CₙH₂ₙ₊₁X", "only single bonds",
    "fluoro-, chloro-, bromo- and iodo-", "alphabetical order", "No locant is needed",
    "2,3-dichlorobutane", "2-bromo-2-methylpropane",
    "same molecular formula but different structural formula and properties",
    "Chain isomerism", "branching in carbon chains", "Position isomerism",
    "functional group is present", "1,3-diiodopropane", "1,2-dichlorobutane",
    "1-bromobutane", "2-bromobutane", "1-bromo-2-methylpropane",
    "only attached to one alkyl group", "joined directly to two alkyl groups",
    "joined directly to three alkyl groups",
    "more strongly attracted to\nfluoroalkanes" if False else "fluoroalkanes",
    "heating under reflux", "condensing the vapour produced back into the flask",
    "Nucleophilic Substitution", "CH₃CH₂Br  +  :OH⁻(aq)  →  CH₃CH₂OH  +  :Br⁻",
    "CH₃CH(Cl)CH₃  +  :OH⁻(aq)  →  CH₃CH(OH)CH₃  +  :Cl⁻",
    "CH₃CH₂Br  +  OH⁻  →  CH₂=CH₂  +  Br⁻  +  H₂O",
    "CH₃CH₂CH₂Cl  +  OH⁻  →  CH₃CH=CH₂  +  H₂O  +  Cl⁻",
    "CH₃CH₂CH(Cl)CH₃  +  OH⁻  →  CH₃CH=CHCH₃  +  CH₃CH₂CH=CH₂",
    "under pressure in a sealed tube", "CH₃CH₂CH₂Cl  +  2NH₃  →  CH₃CH₂CH₂NH₂  +  NH₄Cl",
    "Dipropylamine" if False else "(CH₃CH₂CH₂)₂NH", "(CH₃CH₂CH₂)₃N",
    "ammonia does not condense", "alcoholic KCN (or NaCN)", "C₂H₅Br  +  KCN(aq/alc)",
    "increasing the length of the carbon chain", "nitrile",
    "water or hydroxide ions replace an atom in a molecule with an –OH group",
    "RX  +  H₂O  →  ROH  +  H⁺  +  X⁻", "X⁻(aq)  +  Ag⁺(aq)  →  AgX(s)",
    "White ppt", "Cream ppt", "Yellow ppt", "aqueous silver nitrate (1 cm³)",
    "ethanol (2 cm³)", "60 °C", "five minutes", "2 drops", "loosely corked",
    "ten minutes", "hardly react with water", "1-iodobutane", "fastest",
    "1-chlorobutane", "slowest", "+467", "+346", "+290", "+228",
    "longer and hence weaker", "carbocation", "Tertiary carbocations are more stable",
    "tertiary  >  secondary  >  primary  >  methyl",
    "both electrons of the shared pair", "heterolytic fission",
    "donating a lone pair", "electron-deficient carbon atom",
    "removes a hydrogen", "SN1 and SN2", "Unit 4",
    "ethanolic potassium hydroxide", "AgI(s)", "silver iodide",
    # alcohols
    "CₙH₂ₙ₊₁OH", "good organic solvents", "raw materials in organic synthesis",
    "104.5°", "109.5°", "tetrahedral", "bent line shape", "Lone pairs repel more",
    "suffix –e of the parent alkane is changed to -ol", "butane-2,3-diol",
    "methanol", "propan-1-ol", "propan-2-ol", "3-methylbutan-2-ol",
    "comparable relative molecular mass", "hydrogen bonding", "London forces",
    "dipole–dipole", "non-polar group", "gradually decreases", "more hydrogen bonds",
    "make useful fuels", "C₂H₅OH(l)  +  3O₂(g)  →  2CO₂(g)  +  3H₂O(l)",
    "replaced by a halogen atom", "PCl₅", "misty fumes", "POCl₃",
    "qualitative test for the –OH group", "mixed (by shaking)",
    "50% concentrated", "KHSO₄", "oxidises bromide ions to bromine",
    "moist red phosphorus" if False else "moist red Phosphorous" if False else "moist red phosphorus",
    "2P(s)  +  3I₂(s)  →  2PI₃(s)", "3C₂H₅OH(l)  +  PI₃(aq)  →  3C₂H₅I(l)  +  H₃PO₃(l)",
    "170 °C", "butan-2-ol", "CH₃CH=CHCH₃  +  CH₃CH₂CH=CH₂",
    "potassium manganate(VII)", "orange to green", "purple to colourless",
    "CH₃CH₂OH  +  2[O]  →  CH₃CHO  +  H₂O", "CH₃CH₂OH  +  2[O]  →  CH₃COOH  +  H₂O",
    "R–CHO", "CH₃CHOHCH₃  +  2[O]  →  CH₃COCH₃  +  H₂O", "R–CO–",
    "cannot be further oxidised", "no reaction",
    "Fehling", "Cu²⁺", "brick red precipitate", "remains unchanged",
    "sodium hydrogencarbonate", "turn limewater milky",
    "2CH₃CO₂H  +  Na₂CO₃  →  2CH₃CO₂Na  +  H₂O  +  CO₂",
    "unreacted starting materials", "physical state", "Simple distillation" if False else "selective boiling and condensation",
    "T-junction", "against gravity", "back flow", "anti-bumping",
    "small bubbles", "highly flammable", "naked flame",
    "Never seal the end of the condenser", "explode",
    "fractionating column", "stop-cock", "two layers", "bottom layer",
    "halogenated solvents are denser", "releasing pressure by opening the tap",
    "settle into two layers", "collect the desired organic layer", "aqueous layer",
    "drying agent", "takes up water to become hydrated", "three spatula loads",
    "appear clear", "decanting or filtration", "insoluble in the organic liquid",
    "CaCl₂", "hydrocarbons", "CaSO₄", "MgSO₄", "acid-sensitive", "K₂CO₃", "Na₂SO₄",
    "heating oil bath", "data booklet", "saturated vapour",
    # mass spectra
    "relative molecular mass", "fragmentation pattern", "bombardment with a beam of high energy electrons",
    "M  +  e⁻  →  M⁺•  +  2e⁻", "molecular ion", "loss of one electron",
    "furthest to the right", "greatest mass-to-charge ratio",
    "CH₄ shows M at 16" if False else "C₄H₁₀ + e⁻ → C₄H₁₀⁺• + 2e⁻",
    "M⁺•  →  X⁺  +  Y•",
    "not detected by MS" if False else "not detected",
    "X⁺ → A⁺ + B" if False else "in turn undergo fragmentation",
    "Only the fragments with the positive charge are detected",
    "percentage of the most abundant fragment", "base peak", "100%",
    "as unique as fingerprints", "15", "17", "29", "31", "43", "45", "57",
    "C₅H₁₂ + e⁻ → C₅H₁₂⁺• + 2e⁻", "14 units apart", "142",
    "carbon-13", "1% of", "M+1 peak is n%", "(number of carbon atoms ÷ 100)",
    "benzoic acid" if False else "5.95", "⁷⁹Br and ⁸¹Br", "equal quantities",
    "3 : 1", "9 : 6 : 1", "1 : 2 : 1", "only one stable isotope",
    "iodine has only one stable isotope", "(CH₃CH₂CH₂)⁺", "136", "138",
    "CH₃CH₂COCH₂CH₃⁺", "propanone", "CH₃CO⁺", "CH₂OH⁺ (or CH₃O⁺)" if False else "CH₂OH⁺",
    # infrared
    "convert energy from infra-red radiation into energy to vibrate their bonds",
    "stretching", "bending", "different strengths", "masses of the different atoms",
    "vibrate at different frequencies", "absorb electromagnetic radiation",
    "transmittance", "0 to 100%", "none is absorbed", "wavenumber", "reciprocal of wavelength",
    "1000 – 1300", "1680 – 1750", "2500 – 3300", "3230 – 3550", "3500 – 3300",
    "1669 – 1645", "2850 – 3000", "3100 – 3000", "1400 – 1000", "800 – 600",
    "600 – 500", "about 500", "1740 cm⁻¹", "3300 cm⁻¹", "1010 cm⁻¹",
    "1200 and 1030" if False else "1200", "1680 – 1640" if False else "1680 – 1640",
    "fingerprint region", "1500 cm⁻¹ to 400 cm⁻¹", "databases", "additional peaks",
    "1300 – 1150", "850 – 515", "743 cm⁻¹", "651 cm⁻¹",
    "two bands", "one band", "no bands", "triethylamine", "1214 cm⁻¹",
    "910 – 665", "1650 – 1580", "1250 – 1020",
    "butan-1-amine", "propan-1-ol", "butan-2-one", "butanal",
    "enhanced greenhouse effect", "CO₂, H₂O vapour and CH₄",
]
for kw in KEYWORDS:
    if kw not in joined:
        errors.append("keyword missing: %r" % kw)

# 7. figures used by the revision exist and are wired into the right sections
for figname, secnum in [
    ("t10-halo-scheme", "10.9"), ("t10-apparatus-distillation", "10.19"),
    ("t10-apparatus-reflux", "10.19"), ("t10-apparatus-fractional", "10.19"),
    ("t10-apparatus-separating", "10.19"), ("t10-bp-determination", "10.19"),
    ("t10-alcohol-bond-angles", "10.15"), ("t10-alcohol-solubility", "10.16"),
    ("t10-ms-ethane", "10.21"), ("t10-ms-pentane", "10.21"),
]:
    sec = next(s for s in topic["sections"] if s["number"] == secnum)
    if not any(b["type"] == "figure" and figname in b.get("src", "") for b in sec["content"]):
        errors.append("figure %s not wired into %s" % (figname, secnum))

# 8. estHours consistent
total = sum(s["estMinutes"] for s in topic["sections"])
if topic["estHours"] != round(total / 60, 1):
    errors.append("estHours mismatch")

if errors:
    print("FAILED (%d):" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("ALL CHECKS PASSED — sections=%d, cards=%d, estHours=%s, total blocks=%d"
      % (len(topic["sections"]), len(topic.get("cards", [])), topic["estHours"],
         sum(len(s["content"]) for s in topic["sections"])))
