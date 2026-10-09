"""Chemistry + structure audit for Topic 3 Part I (ionic 3.1-3.9 + metallic 3.20-3.22)."""
import sqlite3, json, re, os

db = sqlite3.connect('db/custom.db')
rows = db.execute("SELECT number, title, spec, specText, outline, content FROM sections WHERE topicSlug='bonding-and-structure' ORDER BY id").fetchall()
nums = [r[0] for r in rows]
print(f"{len(rows)} sections: {' '.join(nums)}")
order_ok = nums == ['3.0'] + [f'3.{i}' for i in range(1, 10)] + [f'3.{i}' for i in range(10, 20)] + ['3.20', '3.21', '3.22']
print(f"order 3.0,3.1-3.22: {'PASS' if order_ok else 'FAIL'}")

# new Part I sections only
new_rows = [r for r in rows if r[0] in [f'3.{i}' for i in range(1, 10)] + ['3.20', '3.21', '3.22']]
print(f"{len(new_rows)} Part I sections: {sum(1 for r in new_rows if r[5])} with content")
for n, t, sp, st, o, c in new_rows:
    blocks = json.loads(c) if c else []
    figs = sum(1 for b in blocks if b['type'] == 'figure')
    print(f"  {n:5} {t:36} blocks={len(blocks):2} figs={figs}")

# figure files exist (light + dark) for the whole topic
missing = []
for n, t, sp, st, o, c in rows:
    for b in (json.loads(c) if c else []):
        if b['type'] == 'figure':
            for variant, path in (('light', b['src']), ('dark', b.get('srcDark'))):
                if not os.path.exists('public' + path):
                    missing.append(f"{n} {variant} {path}")
print(f"\nFigure files: {'ALL PRESENT' if not missing else missing}")

newc = " ".join((r[5] or "") for r in new_rows)
specmap = json.loads([r for r in rows if r[0] == '3.0'][0][5])
allmap = " ".join(x for row in specmap if row.get('type') == 'table' for r_ in row['rows'] for x in r_)

checks = [
    ("3.1 CuCrO4 dissociation eq", 'CuCrO₄(aq) → Cu²⁺(aq) + CrO₄²⁻(aq)' in newc),
    ("3.1 blue Cu2+ to cathode", 'cathode' in newc and 'Cu²⁺' in newc),
    ("3.1 yellow CrO4 2- to anode", 'anode' in newc and 'CrO₄²⁻' in newc),
    ("3.1 MnO4- to anode (2nd practical)", 'MnO₄⁻' in newc),
    ("3.1 zero density between ions", 'zero electron density' in newc),
    ("3.2 metals lose / non-metals gain", 'noble gas electronic configuration' in newc and 'octet' in newc),
    ("3.2 ion equations", 'Na → Na⁺ + e⁻' in newc and 'Mg → Mg²⁺ + 2e⁻' in newc and 'O + 2e⁻ → O²⁻' in newc and 'Cl + e⁻ → Cl⁻' in newc),
    ("3.2 charge = electrons lost/gained", 'charge on the ion equals the number of electrons lost or gained' in newc),
    ("3.3 brackets + charge top right", 'square brackets' in newc),
    ("3.3 Na2O from charges", 'Na₂O' in newc),
    ("3.4 giant lattice def: alternating + non-directional + all directions", 'alternating positive cations and negative anions' in newc),
    ("3.4 6:6 coordination, octahedral", '6:6 coordination' in newc and 'octahedrally by 6' in newc),
    ("3.4 no discrete molecules / empirical", 'no discrete molecules' in newc),
    ("3.5 net attraction outweighs repulsions", 'outweigh' in newc and 'net' in newc),
    ("3.6 charge + radius factors", 'Higher ionic charge' in newc and 'Smaller ionic radius' in newc),
    ("3.6 MgO vs NaCl worked: 2852 vs 801", '2852' in newc and '801' in newc),
    ("3.6 NaF 993", '993' in newc),
    ("3.6 radii 72/102/140/181 pm in worked", '72 pm' in newc and '102 pm' in newc and '140 pm' in newc and '181 pm' in newc),
    ("3.7 isoelectronic def + 10 electrons", 'Isoelectronic' in newc and '10 electrons' in newc),
    ("3.7 config 1s2 2s2 2p6", '1s² 2s² 2p⁶' in newc),
    ("3.7 protons 7 to 13", '7 protons' in newc and '13 protons' in newc),
    ("3.7 radius table values", all(v in newc for v in ('171', '140', '133', '102', '72', '54'))),
    ("3.7 radius decreases N3- to Al3+", 'decreases' in newc and 'N³⁻' in newc and 'Al³⁺' in newc),
    ("3.7 cation smaller / anion larger than atom", 'cation is smaller' in newc and 'anion is larger' in newc),
    ("3.8 polarisation def: distortion of anion cloud", 'distortion of the electron density cloud of an anion' in newc),
    ("3.8 covalent character between nuclei", 'covalent character' in newc),
    ("3.9 cation: high charge + small radius", 'high charge and a small ionic radius' in newc),
    ("3.9 anion: large radius + high negative charge", 'large radius and a high negative charge' in newc),
    ("3.9 Li+ and Al3+ classic; I- vs F-", 'Li⁺ and Al³⁺' in newc and 'I⁻ is much more polarisable than F⁻' in newc),
    ("3.9 AlCl3 covalent character worked", 'Al₂Cl₆' in newc),
    ("3.9 Al2O3 2072 vs MgO 2852 callout", '2072' in newc),
    ("3.20 sea of delocalised outer-shell electrons", 'delocalised' in newc and 'sea' in newc.lower()),
    ("3.20 Na 1 / Mg 2 / Al 3 donated", 'sodium donates one' in newc and 'magnesium two, aluminium three' in newc),
    ("3.21 metallic bonding def", 'strong electrostatic attraction between the positive metal ions' in newc),
    ("3.22 mp trend Al3+ > Mg2+ > Na+", 'Al³⁺ > Mg²⁺ > Na⁺' in newc),
    ("3.22 mp data 98/650/660", all(v in newc for v in ('98 °C', '650 °C', '660 °C'))),
    ("3.22 conducts solid AND liquid", 'solid and the liquid state' in newc),
    ("3.22 malleable/ductile: layers slide, sea adjusts", 'slide over one another' in newc and 'adjusts' in newc),
    ("no Part-I-pending note left in spec map", 'covered in Part I' not in allmap and 'Part I of the notes' not in allmap),
    ("spec map lists 3.1-3.22", all(f"'{n}'" or n in allmap for n in nums[1:]) and 'migration of ions' in allmap),
    ("No exercise/question text", 'EXERCISE' not in newc.upper() and 'CHECKPOINT' not in newc.upper()),
]
print("\nFact checks:")
fails = 0
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    fails += 0 if ok else 1

# Verbatim spec check for the 12 new sections
spec_txt = open('scripts/full_spec.txt').read()
spec_norm = re.sub(r'\s+', ' ', spec_txt).replace('\u2018', "'").replace('\u2019', "'")
# pdftotext flattens super/subscripts (N3- for N³⁻) — normalise both sides
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻−₂₃₄', '0123456789+--234')
spec_norm = spec_norm.translate(SUP)
print("\nVerbatim spec check (Part I):")
for n, t, sp, st, o, c in new_rows:
    lead = re.sub(r'\s+', ' ', st).replace('\u2018', "'").replace('\u2019', "'").translate(SUP)
    found = lead.lower() in spec_norm.lower()
    print(f"  {'PASS' if found else 'FAIL'}  {n}: {lead[:64]}...")

# 3.10-3.19 untouched sanity: content still present
old = [r for r in rows if r[0] in [f'3.{i}' for i in range(10, 20)]]
print(f"\nPart II untouched: {sum(1 for r in old if r[5])}/10 sections still carry content")

print(f"\nTOTAL: {fails} failed fact checks")
