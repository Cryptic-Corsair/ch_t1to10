"""Chemistry + structure audit for Topic 6 (Energetics) — mirrors verify_topic5.py."""
import sqlite3, json, re, os

db = sqlite3.connect('db/custom.db')
rows = db.execute("SELECT number, title, spec, specText, content FROM sections WHERE topicSlug='energetics' ORDER BY id").fetchall()
print(f"{len(rows)} sections:")
for n, t, sp, st, c in rows:
    blocks = json.loads(c) if c else []
    figs = sum(1 for b in blocks if b['type'] == 'figure')
    print(f"  {n:5} {t:44} spec={sp}  blocks={len(blocks)} figs={figs}")

failures = []

# ---- section order 6.0, 6.1..6.11
nums = [r[0] for r in rows]
expect = ['6.0'] + ['6.%d' % i for i in range(1, 12)]
if nums != expect:
    failures.append('section order: got %s' % nums)

# ---- every figure has a light + dark PNG on disk
for n, t, sp, st, c in rows:
    blocks = json.loads(c) if c else []
    for b in blocks:
        if b['type'] == 'figure':
            for variant, path in (('light', b['src']), ('dark', b.get('srcDark'))):
                fp = 'public' + path
                if not os.path.exists(fp):
                    failures.append(f"figure missing {n} {variant} {fp}")

# ---- verbatim spec checks (normalise ∆/Δ, superscript flattening, quotes)
spec_raw = open('scripts/full_spec.txt').read()
def norm(s):
    s = s.replace('\u2206', '\u0394')  # ∆ -> Δ
    s = s.replace('\u2018', "'").replace('\u2019', "'")
    s = s.replace('\u2013', '-').replace('\u2212', '-')
    s = re.sub(r'[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207b]',
               lambda m: {'\u207b':'-','\u00b9':'1','\u00b2':'2','\u00b3':'3','\u2070':'0','\u2074':'4','\u2075':'5','\u2076':'6','\u2077':'7','\u2078':'8','\u2079':'9'}[m.group(0)], s)
    return re.sub(r'\s+', ' ', s).strip().lower()

spec_norm = norm(spec_raw)

def spec_check(label, statement):
    if norm(statement) not in spec_norm:
        failures.append('SPEC VERBATIM FAIL: ' + label)

spec_check('6.1', 'know that the enthalpy change, \u0394H, is the heat energy change measured at constant pressure and that standard conditions are 100 kPa and a specified temperature, usually 298 K')
spec_check('6.2', 'know that, by convention, exothermic reactions have a negative enthalpy change and endothermic reactions have a positive enthalpy change')
spec_check('6.3', 'be able to construct and interpret enthalpy level diagrams, showing exothermic and endothermic enthalpy changes')
spec_check('6.4 head', 'know the definition of standard enthalpy change of:')
spec_check('6.4-i', 'reaction, \u0394rH')
spec_check('6.4-ii', 'formation, \u0394fH')
spec_check('6.4-iii', 'combustion, \u0394cH')
spec_check('6.4-iv', 'neutralisation, \u0394neutH')
spec_check('6.4-v', 'atomisation, \u0394atH')
spec_check('6.5-i expression', 'energy transferred (J) = mass (g) \u00d7 specific heat capacity (J g-1 \u00b0C-1) \u00d7 temperature change (\u00b0C)')
spec_check('6.5-ii', 'enthalpy change of the reaction in kJ mol-1')
spec_check('6.5 note', 'This will be limited to experiments where substances are mixed in an insulated container and combustion experiments using a suitable calorimeter.')
spec_check('6.6 head', "know Hess's Law and be able to apply it to:")
spec_check('6.6-i', 'constructing enthalpy cycles')
spec_check('6.6-ii', 'calculating enthalpy changes of reaction using data provided, or data selected from a table or obtained from experiments')
spec_check('6.7', "Determination of the enthalpy change of a reaction using Hess's Law.")
spec_check('6.8', 'be able to evaluate the results obtained from experiments and comment on sources of error and uncertainty and any assumptions made in the experiments')
spec_check('6.8 note', 'Students will need to consider experiments where substances are mixed in an insulated container and combustion experiments using, for example, a spirit burner and be able to draw suitable graphs and use cooling curve corrections.')
spec_check("6.9", "understand the terms 'bond enthalpy' and 'mean bond enthalpy', and be able to use bond enthalpies to calculate enthalpy changes, understanding the limitations of this method")
spec_check('6.10', 'be able to calculate mean bond enthalpies from enthalpy changes of reaction')
spec_check('6.11', 'understand that bond enthalpy data gives some indication about which bond will break first in a reaction, how easy or difficult it is and therefore how rapidly a reaction will take place at room temperature')
spec_check('further practical i', 'the enthalpy change for the decomposition of calcium carbonate using the enthalpy changes of reaction of calcium carbonate and calcium oxide with hydrochloric acid')
spec_check('further practical iv', 'the enthalpy of hydration of anhydrous copper(II) sulfate')

# multi-part outlines must be visible in specText/outline of the seeded sections
trows = db.execute("SELECT number, specText, outline FROM sections WHERE topicSlug='energetics' AND number IN ('6.4','6.5','6.6')").fetchall()
outl = {r[0]: (r[1] or '') + ' ' + (r[2] or '') for r in trows}
for lbl, frag in (('6.4 v atomisation', 'atomisation, \u0394atH'),
                  ('6.5 i expression', 'energy transferred (J)'),
                  ('6.5 ii', 'enthalpy change of the reaction in kJ mol\u207b\u00b9'),
                  ('6.5 note', 'This will be limited to experiments'),
                  ('6.6 ii', 'data provided, or data selected from a table')):
    if lbl.startswith('6.5 ii'):
        ok = 'kJ mol' in outl.get('6.5', '')
    else:
        ok = norm(frag) in norm(outl.get(lbl.split()[0], ''))
    if not ok:
        failures.append('OUTLINE FAIL: ' + lbl)

# ---- chemistry fact checks against seeded content
allc = " ".join((r[4] or "") for r in rows)
def has(label, *frags, absent=()):
    if not all(f in allc for f in frags):
        failures.append('FACT FAIL: ' + label)
    for a in absent:
        if a in allc:
            failures.append('FACT ABSENT-FAIL: ' + label + ' (found forbidden ' + repr(a) + ')')

has('energetics = study of energy transfers', 'The study of energy transfers between reacting chemicals')
has('first law: neither created nor destroyed', '**neither created nor destroyed**')
has('chemical energy = KE + PE', '**kinetic energy**, a measure of the motion of particles', '**potential energy**, a measure of how strongly the particles interact')
has('enthalpy def: heat content at constant pressure', 'heat content', 'constant pressure')
has('delta H in kJ per mol', 'kJ mol\u207b\u00b9')
has('standard conditions 100 kPa + 298 K', '**100 kPa**', '**298 K (25 \u00b0C)**')
has('standard conditions solutions 1 mol dm-3', '1 mol dm\u207b\u00b3')
has('100 kPa correction callout (1 atm rejected)', 'Quote 100 kPa \u2014 not 1 atm')
has('exothermic: liberates heat, DH negative', 'liberate heat energy to the surroundings', 'negative')
has('endo: absorbs heat, DH positive', 'absorb heat energy from the surroundings', 'positive')
has('thermodynamically unstable (exo)', 'thermodynamically unstable')
has('kinetic stability / petrol', 'kinetic stability', 'occurs only when ignited')
has('bond making vs breaking criterion', 'energy released for bond making is **greater**', '**less** than the energy absorbed')
has('enthalpy level: no zero no scale', 'no zero and no scale')
has('Ea energy barrier', 'energy barrier that must be overcome')
has('thermochemical equation def', 'thermochemical equation')
has('multiply -> multiply DH', 'multiplied**, ΔH is multiplied')
has('reverse -> sign flips', 'reversed**, the **sign of ΔH changes**')
has('DHr per mole of equation', 'one mole of the equation as written')
has('N2+3H2 = -92', 'N₂(g) + 3H₂(g) → 2NH₃(g)', '\u221292 kJ mol\u207b\u00b9')
has('half equation = -46', '\u221246 kJ mol\u207b\u00b9')
has('C + O2 = -393 thermochemical', 'C(s) + O₂(g) → CO₂(g)', '\u2212393 kJ mol\u207b\u00b9')
has('formation def: elements in standard states', 'elements in their standard states')
has('ethanol formation equation', '2C(s, graphite) + ½O₂(g) + 3H₂(g) → C₂H₅OH(l)')
has('elements DHf = 0', 'zero** enthalpy of formation')
has('carbon = graphite', '**graphite** allotrope')
has('combustion def: completely burnt in excess O2', 'completely burnt in excess oxygen')
has('combustion always exothermic', 'always exothermic')
has('ethanol combustion equation', 'C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l)')
has('neutralisation def: 1 mol water', 'one mole of water')
has('H+ + OH- = -57.9', 'H⁺(aq) + OH⁻(aq) → H₂O(l)', '\u221257.9 kJ mol\u207b\u00b9')
has('strong acid/alkali fully ionised', 'fully ionised')
has('atomisation def: gaseous atoms', 'one mole of gaseous atoms')
has('atomisation always endothermic', 'always endothermic**, as energy is required to break bonds')
has('Cl2 bond enthalpy = 2 x atomisation (242 = 2x121)', '+242 kJ mol\u207b\u00b9', '+121 kJ mol\u207b\u00b9')
has('q = mcDT', 'Q = m × c × ΔT')
has('water c = 4.18', '4.18 J g\u207b\u00b9 \u00b0C\u207b\u00b9')
has('calorimeter def', 'minimises heat exchange')
has('alkali in excess', 'slight **excess**')
has('neutralisation worked: 50 g, 6.7 K', '50 × 4.18 × 6.7 = 1400.3 J')
has('neutralisation worked: 0.025 mol', '0.025 mol')
has('neutralisation worked answer -56', '\u221256 kJ mol\u207b\u00b9')
has('combustion procedure ~20C rise', 'risen by about 20 \u00b0C')
has('ethanol worked: 10 282 J', '10 282 J = 10.28 kJ')
has('ethanol worked: 0.39 g / 46', '0.39 ÷ 46 = 0.00847 mol')
has('ethanol worked answer -1213.7', '\u22121213.7 kJ mol\u207b\u00b9')
has('sign discipline callout', 'the enthalpy change you report is **negative**')
has('Hess statement', 'independent of the path taken')
has('enthalpy cycles named', 'enthalpy cycles')
has('why indirect: high Ea', 'high activation energy')
has('why indirect: side reactions', 'more than one reaction occurring')
has('why indirect: does not stop', 'not stop')
has('combustion-data formula', 'ΔH[reaction] = Σ ΔcH°[reactants] − Σ ΔcH°[products]')
has('formation-data formula', 'ΔH[reaction] = Σ ΔfH°[products] − Σ ΔfH°[reactants]')
has('CO: C+O2 -394, CO+1/2O2 -283', '\u2212394', '\u2212283')
has('CO answer -111', '\u2212111 kJ mol\u207b\u00b9')
has('CO cycle equation', 'ΔfH° + (−283) = −394')
has('CH4 cycle equation', 'ΔfH° + (−890) = (−394) + 2 × (−286)')
has('CH4 answer -76', '\u221276 kJ mol\u207b\u00b9')
has('CaCO3 data -1207/-635/-394', '\u22121207', '\u2212635', '\u2212394')
has('CaCO3 answer +178', '+178 kJ mol\u207b\u00b9')
has('CP2 bracketing logic', 'bracket')
has('CP2 CaCO3/HCl -17 and -195', '\u221217 kJ mol\u207b\u00b9', '\u2212195 kJ mol\u207b\u00b9')
has('CuSO4 hydration +11.3 / -67.0', '+11.3 kJ mol\u207b\u00b9', '\u221267.0 kJ mol\u207b\u00b9')
has('CuSO4 answer -78.3', '\u221278.3 kJ mol\u207b\u00b9')
has('common intermediate pattern', 'common intermediate')
has('combustion errors: heat loss', '**Heat loss** to the surroundings')
has('combustion errors: soot/incomplete', 'black soot', '**Incomplete combustion**')
has('combustion errors: vapour not liquid', 'water vapour is formed instead of liquid water')
has('combustion errors: air + apparatus', 'heats up the **air**', 'beaker and thermometer** absorb')
has('assumption 1 cm3 = 1 g', '1 cm³ of water is equal to **1 g**')
has('assumption: all heat to water', '**All** the heat energy produced by the fuel is absorbed by the water')
has('solution errors: cup + thermometer + pipette', 'polystyrene cup and thermometer** absorb', 'pipette and thermometer')
has('solution assumptions: c and density of water', '4.18 J g\u207b\u00b9 \u00b0C\u207b\u00b9', '1 g cm\u207b\u00b3')
has('improvements: lid + lagging', '**lid**', '**lagging**')
has('cooling curve: half minute before', 'every half minute** before mixing')
has('cooling curve: mix at 3 min', '**3 minutes**')
has('cooling curve: extrapolate compensates', 'compensates for heat loss', 'cooling correction')
has('bond enthalpy def: gaseous state', '1 mol of a bond in the gaseous state')
has('Cl2 243 / HCl 432', '+243 kJ mol\u207b\u00b9', '+432 kJ mol\u207b\u00b9')
has('CH4 steps 423/480/425/335', '+423', '+480', '+425', '+335')
has('mean bond enthalpy def', 'average** quantity of energy required to break **one mole**')
has('mean C-H = 415.75 ~ 416', '415.75', '+416 kJ mol\u207b\u00b9')
has('fH/cH data more accurate than bond enthalpies', 'more accurate** than one calculated from bond enthalpy values')
has('limitations: gas phase + means', 'gaseous state** only', 'they are averages')
has('bond cycle: reactants - products', 'ΔH[reaction] = Σ E[reactants] − Σ E[products]')
has('H2O(g) worked: 436+249-924', '436 + 249 − 924')
has('H2O(g) answer -239', '\u2212239 kJ mol\u207b\u00b9')
has('6.10 rearrangements', 'unknown bond broken', 'unknown bond formed')
has('6.10 mean-value limitation applies', 'gaseous-state and mean-value limitations')
has('6.11 which bond first / how fast', 'which bond will break first', 'room temperature')
has('methane values as evidence', '+423, +480, +425 and +335')

# forbidden content: exercises / questions / artifacts
for bad in ('EXERCISE', 'Checkpoint question', 'answer sheet', '….'):
    if bad in allc:
        failures.append('FORBIDDEN CONTENT: ' + repr(bad))

# arithmetic spot checks
assert abs(10.28 / 0.00847 - 1213.7) < 0.15
assert abs(1.4003 / 0.025 - 56.012) < 0.01
assert (-394 + 2 * -286) - (-890) == -76
assert (-635 + -394) - (-1207) == 178
assert -17 + 195 == 178
assert -67.0 - 11.3 == -78.3
assert (423 + 480 + 425 + 335) / 4 == 415.75
assert abs((436 + 0.5 * 498) - 2 * 462 + 239) < 1e-9

# ---- flashcards
fc = db.execute("SELECT COUNT(*) FROM flashcards WHERE topicSlug='energetics'").fetchone()[0]
print(f"energetics flashcards: {fc}")
if fc < 15:
    failures.append(f'flashcards {fc} < 15')

print('\n%d checks failed' % len(failures))
for f in failures:
    print('  ✗', f)
if not failures:
    print('ALL PASS')
