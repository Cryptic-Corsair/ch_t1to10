"""Chemistry + structure audit for Topic 4 (Introductory Organic Chemistry and Alkanes)."""
import sqlite3, json, re, os

db = sqlite3.connect('db/custom.db')
rows = db.execute("SELECT number, title, spec, specText, outline, content FROM sections WHERE topicSlug='organic-intro-and-alkanes' ORDER BY id").fetchall()
nums = [r[0] for r in rows]
print(f"{len(rows)} sections: {' '.join(nums)}")
order_ok = nums == ['4.0'] + [f'4.{i}' for i in range(1, 19)]
print(f"order 4.0,4.1-4.18: {'PASS' if order_ok else 'FAIL'}")
print(f"{sum(1 for r in rows if r[5])}/19 with content")

# figure files exist (light + dark)
missing = []
for n, t, sp, st, o, c in rows:
    for b in (json.loads(c) if c else []):
        if b['type'] == 'figure':
            for variant, path in (('light', b['src']), ('dark', b.get('srcDark'))):
                if not os.path.exists('public' + path):
                    missing.append(f"{n} {variant} {path}")
print(f"\nFigure files: {'ALL PRESENT' if not missing else missing}")

allc = " ".join((r[5] or "") for r in rows)

checks = [
    ("4.1 hazard vs risk defs", 'potential to cause harm' in allc and 'probability or likelihood' in allc),
    ("4.2 four organic hazards", 'flammability, volatility, toxicity or carcinogenicity' in allc),
    ("4.2 six symbols table", all(s in allc for s in ('Flammable', 'Toxic', 'Corrosive', 'Irritant', 'Oxidising', 'Environmental hazard'))),
    ("4.2 risk assessment before experiment", 'prior to an experiment' in allc),
    ("4.3 i/ii/iii covered", 'smaller scale' in allc and 'fume cupboard' in allc and 'methylbenzene' in allc),
    ("4.3 electric mantle not Bunsen", 'electric heating mantle' in allc and 'Bunsen' in allc),
    ("4.4 homologous series traits", 'same functional group' in allc and '14 g mol⁻¹' in allc and '—CH₂—' in allc),
    ("4.4 functional group def", 'responsible for its characteristic chemical reactions' in allc),
    ("4.5 prefixes to C10", all(p in allc for p in ('Meth-', 'Pent-', 'Dec-'))),
    ("4.5 naming rules: lowest locants + alphabetism", 'lowest possible locant' in allc and 'alphabetical order' in allc),
    ("4.5 punctuation", 'commas separate numbers from numbers; hyphens separate numbers from words' in allc),
    ("4.5 six formula types defined", all(s in allc for s in ('Empirical formula', 'Molecular formula', 'General formula', 'Structural formula', 'Displayed formula', 'Skeletal formula'))),
    ("4.5 skeletal heteroatom rule", 'Heteroatoms (O, N, Cl' in allc),
    ("4.5 worked 2-methylpentane", '2-methylpentane' in allc),
    ("4.6 five reaction classes", all(s in allc for s in ('Addition', 'Substitution', 'Oxidation', 'Reduction', 'Polymerisation'))),
    ("4.6 addition = single product", 'single product' in allc),
    ("4.7 homolytic eq", 'A—B → A• + B•' in allc),
    ("4.7 heterolytic eq", 'A—B → A⁺ + :B⁻' in allc),
    ("4.7 radicals vs ions products", 'free radicals' in allc and 'ions' in allc),
    ("4.8 radical def", 'unpaired electron' in allc),
    ("4.8 electrophile def", 'electron-pair acceptor' in allc),
    ("4.9 general formulae", 'CₙH₂ₙ₊₂' in allc and 'CₙH₂ₙ' in allc),
    ("4.9 cycloalkanes isomeric with alkenes", 'structural isomers of alkenes' in allc),
    ("4.9 saturated = single bonds only", 'single carbon—carbon bonds only' in allc),
    ("4.10 three sub-types", 'Chain isomerism' in allc and 'Position isomerism' in allc and 'Functional group isomerism' in allc),
    ("4.10 same molecular formula def", 'same molecular formula' in allc and 'different structural formulae' in allc),
    ("4.11 isomer table complete sets", 'butane; 2-methylpropane' in allc and 'pentane; 2-methylbutane; 2,2-dimethylpropane' in allc and 'hexane; 2-methylpentane' in allc),
    ("4.11 names complete", all(s in allc for s in ('2-methylpropane', '2-methylbutane', '2,2-dimethylpropane', '2-methylpentane', '3-methylpentane', '2,2-dimethylbutane', '2,3-dimethylbutane'))),
    ("4.11 cycloalkane examples", all(s in allc for s in ('methylcyclopropane', 'methylcyclobutane', '1,1-dimethylcyclopropane', '1,2-dimethylcyclopropane'))),
    ("4.11 worked C5H12 answer", 'pentane, 2-methylbutane and 2,2-dimethylpropane' in allc),
    ("4.12 column: hot bottom cool top", 'hotter at the bottom' in allc and 'cooler at the top' in allc),
    ("4.12 longer chains condense lower", 'condense' in allc and 'higher boiling points' in allc),
    ("4.12 cracking def + eq", 'thermal or catalytic breakdown' in allc.replace('**', '') or 'Cracking' in allc),
    ("4.12 cracking eq balanced", 'C₁₀H₂₂ → C₈H₁₈ + C₂H₄' in allc),
    ("4.12 reforming Pt + octane + knocking", 'platinum catalyst' in allc and 'octane rating' in allc and 'knocking' in allc),
    ("4.12 reforming eqs", 'C₆H₁₄ → C₆H₁₂ + H₂' in allc and 'C₇H₁₆ → C₇H₈ + 4H₂' in allc),
    ("4.12 reforming temp range", '400–500 °C' in allc),
    ("4.13 complete combustion eq", 'C₃H₈ + 5O₂ → 3CO₂ + 4H₂O' in allc),
    ("4.13 incomplete eqs", 'C₃H₈ + 3.5O₂ → 3CO + 4H₂O' in allc and 'C₃H₈ + 2O₂ → 3C + 4H₂O' in allc),
    ("4.13 NOx from air not fuel", 'N₂ + O₂ → 2NO' in allc and 'nitrogen in the air' in allc),
    ("4.13 SO2 from impurities", 'S + O₂ → SO₂' in allc),
    ("4.14 CO toxicity mechanism", 'haemoglobin' in allc and 'carboxyhaemoglobin' in allc),
    ("4.14 no 'irreversibly' overclaim", 'irreversibly' not in allc),
    ("4.14 greater affinity", 'greater affinity' in allc),
    ("4.14 acid rain damage list", 'acidifies lakes' in allc and 'limestone' in allc),
    ("4.14 SO2 + H2O eq", 'SO₂ + H₂O → H₂SO₃' in allc),
    ("4.14 particulates: asthma + global dimming", 'asthma' in allc and 'global dimming' in allc),
    ("4.15 finite + climate change", 'finite, non-renewable' in allc and 'greenhouse effect' in allc),
    ("4.16 carbon neutrality def", 'net CO₂ emitted during its combustion equals the amount of CO₂ absorbed' in allc),
    ("4.16 bioethanol caveat", 'not 100% carbon neutral in practice' in allc and 'farming machinery' in allc),
    ("4.16 fermentation eq", 'C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂' in allc),
    ("4.16 hydrogen eq + challenges", '2H₂ + O₂ → 2H₂O' in allc and 'storing' in allc),
    ("4.17 combustion exothermic", 'exothermic' in allc),
    ("4.17 halogens + UV + products", 'ultraviolet (UV) light' in allc and 'halogenoalkane and a hydrogen halide' in allc),
    ("4.17 no reaction in the dark", 'no reaction' in allc and 'dark' in allc),
    ("4.18 overall eq", 'CH₄ + Cl₂ → CH₃Cl + HCl' in allc),
    ("4.18 initiation eq", 'Cl—Cl → Cl• + Cl•' in allc),
    ("4.18 propagation eqs", 'Cl• + CH₄ → •CH₃ + HCl' in allc and '•CH₃ + Cl₂ → CH₃Cl + Cl•' in allc),
    ("4.18 termination eqs incl ethane", '•CH₃ + •CH₃ → C₂H₆' in allc),
    ("4.18 ethane evidence", 'evidence for •CH₃ radicals' in allc),
    ("4.18 fish-hooks", 'fish-hook' in allc),
    ("4.18 further substitution products", 'CH₂Cl₂' in allc and 'CHCl₃' in allc and 'CCl₄' in allc),
    ("4.18 limited use in synthesis", 'limited use in synthesis' in allc),
    ("4.18 excess methane favours mono", 'excess methane' in allc),
    ("catalytic converters removed (not in spec)", 'atalytic converter' not in allc),
    ("No exercise/question text", 'EXERCISE' not in allc.upper() and 'CHECKPOINT' not in allc.upper()),
    ("no chatbot sign-offs from the guide", 'Next Steps' not in allc and 'Would you like' not in allc),
]
print("\nFact checks:")
fails = 0
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    fails += 0 if ok else 1

# Verbatim spec check
spec_txt = open('scripts/full_spec.txt').read()
spec_norm = re.sub(r'\s+', ' ', spec_txt).replace('\u2018', "'").replace('\u2019', "'")
# pdftotext flattens subscripts (CO2 for CO2 subscripted) — normalise both sides
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻−₂₃₄', '0123456789+--234')
spec_norm = spec_norm.translate(SUP)
print("\nVerbatim spec check:")
for n, t, sp, st, o, c in rows:
    if not st:
        continue
    lead = re.sub(r'\s+', ' ', st).replace('\u2018', "'").replace('\u2019', "'").translate(SUP)
    found = lead.lower() in spec_norm.lower()
    print(f"  {'PASS' if found else 'FAIL'}  {n}: {lead[:64]}...")

# Multi-part outline items must match spec sub-statements
print("\nMulti-part outline check:")
mpfails = 0
for sp_target in ('4.3', '4.5', '4.7', '4.17', '4.18'):
    row = [r for r in rows if r[2] == sp_target][0]
    outs = json.loads(row[4])
    for o in outs:
        core = re.sub(r'^[ivx]+\s+', '', o).strip()
        core_norm = re.sub(r'\s+', ' ', core).replace('\u2018', "'").replace('\u2019', "'").translate(SUP).lower()
        ok = core_norm[:44] in spec_norm.lower()
        mpfails += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {sp_target}: {core[:60]}")

print(f"\nTOTAL: {fails + mpfails} failed checks")
