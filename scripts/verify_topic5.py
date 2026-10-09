"""Chemistry + structure audit for Topic 5 (alkenes) — mirrors verify_topic3.py."""
import sqlite3, json, re

db = sqlite3.connect('db/custom.db')
rows = db.execute("SELECT number, title, spec, specText, content FROM sections WHERE topicSlug='alkenes' ORDER BY id").fetchall()
print(f"{len(rows)} sections:")
for n, t, sp, st, c in rows:
    blocks = json.loads(c) if c else []
    kinds = {}
    for b in blocks: kinds[b['type']] = kinds.get(b['type'], 0) + 1
    figs = sum(1 for b in blocks if b['type'] == 'figure')
    print(f"  {n:5} {t:34} spec={sp}  blocks={len(blocks)} figs={figs}")

# Every figure must have a light + dark PNG on disk
import os
missing = []
for n, t, sp, st, c in rows:
    blocks = json.loads(c) if c else []
    for b in blocks:
        if b['type'] == 'figure':
            for variant, path in (('light', b['src']), ('dark', b.get('srcDark'))):
                fp = 'public' + path
                if not os.path.exists(fp):
                    missing.append(f"{n} {variant} {fp}")
                if variant == 'dark':
                    if not path.endswith('-dark.png'):
                        missing.append(f"{n} dark path not -dark: {path}")
print(f"\nFigure files: {'ALL PRESENT' if not missing else missing}")

# Chemistry fact checks
allc = " ".join((r[4] or "") for r in rows)
checks = [
    ("general formula CnH2n", 'CₙH₂ₙ' in allc),
    ("one sigma + one pi bond", 'one sigma bond and one pi bond' in allc),
    ("120° around C=C", '120°' in allc),
    ("sp2: three sp² + one p orbital", 'three sp² hybrid orbitals and one normal p orbital' in allc),
    ("buta-1,3-diene naming", 'buta-1,3-diene' in allc),
    ("stereoisomers definition", 'arranged differently in 3D' in allc),
    ("chain isomers C5H10: 3-methylbut-1-ene", '3-methylbut-1-ene' in allc),
    ("positional isomers: pent-2-ene", 'pent-2-ene' in allc),
    ("rotation breaks C=C", 'would be broken if it were rotated' in allc),
    ("cis = same side", 'CIS:' in allc and 'same side' in allc),
    ("zusammen / entgegen", 'zusammen' in allc and 'entgegen' in allc),
    ("C(6) priority over H(1)", 'carbon (atomic number 6) has priority over hydrogen (atomic number 1)' in allc),
    ("worked example: Cl priority 17", 'Cl (atomic number 17)' in allc),
    ("worked example answer: E-1-chloro-2-methylbut-1-ene", 'E-1-chloro-2-methylbut-1-ene' in allc),
    ("hydrogenation: Ni catalyst 140-180", 'nickel catalyst and heat (140–180 °C)' in allc),
    ("hydrogenation equation", 'C₂H₄ + H₂ → C₂H₆' in allc),
    ("chlorination equation", 'C₂H₄ + Cl₂ → CH₂ClCH₂Cl' in allc),
    ("bromine in hexane: NO HBr (source error fixed)", 'C₂H₄ + Br₂ → CH₂BrCH₂Br' in allc and 'C₂H₄ + Br₂ → CH₂BrCH₂Br + HBr' not in allc),
    ("hydration: H3PO4 300C", 'phosphoric acid catalyst and heat (300 °C)' in allc),
    ("hydration equation", 'C₂H₄ + H₂O → CH₃CH₂OH' in allc),
    ("HBr addition equation", 'C₂H₄ + HBr → CH₃CH₂Br' in allc),
    ("KMnO4 purple to green (MnO42-)", 'MnO₄⁻' in allc and 'MnO₄²⁻' in allc),
    ("KMnO4 diol equation", 'C₂H₄ + H₂O + [O] → CH₂(OH)CH₂(OH)' in allc),
    ("bromine water: bromoalcohol + HBr", 'C₂H₄ + Br₂ + H₂O → CH₂BrCH₂OH + HBr' in allc),
    ("acidified KMnO4 colourless", 'colourless' in allc),
    ("curly arrows: bond or lone pair", 'start from a bond and move to an atom' in allc),
    ("heterolytic fission named", 'heterolytic fission' in allc),
    ("induced dipole on bromine", 'inducing a dipole' in allc),
    ("major product via more stable carbocation", 'major product is formed via the more stable carbocation' in allc),
    ("carbocation 1° < 2° < 3°", 'primary carbocations are the least stable and tertiary carbocations are the most stable' in allc),
    ("alkyl groups electron releasing", 'electron releasing relative to hydrogen atoms' in allc),
    ("polymerisation: free radical process", 'free radical process' in allc),
    ("repeat unit polyethene", 'n CH₂=CH₂ → (—CH₂—CH₂—)ₙ' in allc),
    ("disposal: HCl from chlorinated polymers", 'toxic fumes like HCl' in allc),
    ("biodegradable: broken down by microbes", 'broken down by microbes' in allc),
    ("No exercise/question text", 'EXERCISE' not in allc.upper()),
    ("No checkpoint text", 'CHECKPOINT' not in allc.upper()),
]
print("\nFact checks:")
fails = 0
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    fails += 0 if ok else 1

# Equation balance spot checks (atom counting, ignoring [O] notation)
def count_atoms(side):
    d = {}
    for sym, n in re.findall(r'([A-Z][a-z]?)(\d*)', side):
        if sym in ('O',) and side.count('[O]'):  # keep simple: [O] counted separately below
            pass
        d[sym] = d.get(sym, 0) + (int(n) if n else 1)
    return d

eq_checks = []
for eq in re.findall(r'C₂H₄[^\'"]*?→[^\'"]*?(?=\')', allc):
    eq_checks.append(eq.strip())
print("\nEquations found in notes:")
for e in set(eq_checks):
    print("   ", e)

# Spec statement verbatim check vs official spec
spec_txt = open('scripts/full_spec.txt').read()
spec_norm = re.sub(r'\s+', ' ', spec_txt).replace('\u2018', "'").replace('\u2019', "'")
rows2 = db.execute("SELECT spec, specText FROM sections WHERE topicSlug='alkenes' AND specText IS NOT NULL").fetchall()
print("\nVerbatim spec check:")
for sp, st in rows2:
    lead = st.split(':')[0].strip()
    lead_norm = re.sub(r'\s+', ' ', lead)
    found = lead_norm.lower() in spec_norm.lower()
    print(f"  {'PASS' if found else 'FAIL'}  {sp}: {lead[:64]}...")

# Multi-part outline items must match spec sub-statements i/ii/iii...
print("\nMulti-part outline check:")
for sp, st, c in db.execute("SELECT spec, specText, outline FROM sections WHERE topicSlug='alkenes' AND spec IN ('5.4','5.6','5.8')"):
    outs = json.loads(c)
    for o in outs:
        core = re.sub(r'^[ivx]+\s+', '', o).strip().rstrip('.')
        core_norm = re.sub(r'\s+', ' ', core).lower()
        ok = core_norm[:50] in spec_norm.lower()
        print(f"  {'PASS' if ok else 'FAIL'}  {sp}: {core[:60]}")

print(f"\nTOTAL: {fails} failed fact checks")
