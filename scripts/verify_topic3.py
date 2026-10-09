import sqlite3, json, re
db = sqlite3.connect('db/custom.db')
rows = db.execute("SELECT number, title, spec, specText, content FROM sections WHERE topicSlug='bonding-and-structure' ORDER BY id").fetchall()
print(f"{len(rows)} sections:")
for n, t, sp, st, c in rows:
    blocks = json.loads(c) if c else []
    kinds = {}
    for b in blocks: kinds[b['type']] = kinds.get(b['type'], 0) + 1
    figs = sum(1 for b in blocks if b['type']=='figure')
    print(f"  {n:5} {t:32} spec={sp}  blocks={len(blocks)} figs={figs}")

# Chemistry fact checks in content
allc = " ".join((r[4] or "") for r in rows)
checks = [
    ("BeCl₂ 4 electrons", '"4"' in allc and 'Beryllium chloride, BeCl₂' in allc),
    ("PCl₅ 10 electrons", "'10'" in allc or '"10"' in allc),
    ("NaCl ΔX 2.1", 'ΔX = 3.0 − 0.9 = 2.1' in allc),
    ("LiF ΔX 3.0", 'ΔX = 4.0 − 1.0 = 3.0' in allc),
    ("SrBr₂ ΔX 1.8", 'ΔX = 2.8 − 1.0 = 1.8' in allc),
    ("H₂O ΔX 0.9", 'ΔX = 3.0 − 2.1 = 0.9' in allc),
    ("NH₃ 107°", '107°' in allc),
    ("H₂O 104.5°", '104.5°' in allc),
    ("PCl₅ 90° and 120°", '90° and 120°' in allc),
    ("SO₂ 117.5°", '117.5°' in allc),
    ("2.5° lone-pair rule", '2.5°' in allc),
    ("F 4.0 / Cs 0.7", '4.0' in allc and '0.7' in allc),
    ("LP-LP > LP-BP > BP-BP", 'lone pair–lone pair > lone pair–bond pair > bond pair–bond pair' in allc),
    ("No exercise/question text", 'EXERCISE' not in allc.upper() or allc.upper().count('EXERCISE')==0),
    ("No checkpoint text", 'CHECKPOINT' not in allc.upper()),
]
print("\nFact checks:")
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")

# Spec statement verbatim check vs official spec
spec_txt = open('scripts/full_spec.txt').read()
spec_norm = re.sub(r'\s+', ' ', spec_txt)
rows2 = db.execute("SELECT spec, specText FROM sections WHERE topicSlug='bonding-and-structure' AND specText IS NOT NULL").fetchall()
print("\nVerbatim spec check:")
import unicodedata
for sp, st in rows2:
    # statements with sub-parts: compare only the lead sentence (before ':')
    lead = st.split(':')[0].strip()
    lead_norm = re.sub(r'\s+', ' ', lead).replace('\u2018',"'").replace('\u2019',"'")
    spec_n2 = spec_norm.replace('\u2018',"'").replace('\u2019',"'")
    found = lead_norm.lower() in spec_n2.lower()
    print(f"  {'PASS' if found else 'FAIL'}  {sp}: {lead[:60]}...")
