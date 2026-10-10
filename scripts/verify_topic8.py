#!/usr/bin/env python3
"""Verify Topic 8 content integrity: sections, verbatim specText, notes, figures, cards."""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/home/z/my-project')
db = sqlite3.connect(ROOT / 'db/custom.db')
db.row_factory = sqlite3.Row
fails = []

def check(cond, msg):
    print(('  OK  ' if cond else '  FAIL ') + msg)
    if not cond:
        fails.append(msg)

# ---- pull topic 8 ----
t8 = dict(db.execute("SELECT slug,number,title,subtitle,summary,estHours FROM topics WHERE number=8").fetchone())
print('Topic:', t8['slug'], '|', t8['title'], '| estHours', t8['estHours'])

secs = [dict(r) for r in db.execute(
    "SELECT sectionKey,number,title,spec,specText,estMinutes,outline,content FROM sections "
    "WHERE topicSlug='redox-and-groups' ORDER BY id").fetchall()]
check(len(secs) == 29, f'29 sections (got {len(secs)})')
nums = [s['number'] for s in secs]
check(nums[0] == '8.0', 'first section is 8.0 spec map')
expected_nums = ['8.0'] + ['8.%d' % i for i in range(1, 29)]
check(nums == expected_nums, 'section numbers run 8.0 -> 8.28 in order')

# ---- verbatim spec statements (from the three source checklists) ----
VERBATIM = {
'8.1': "know what is meant by the term 'oxidation number' and understand the rules for assigning oxidation numbers",
'8.2': 'be able to calculate the oxidation number of elements in compounds and ions, including in peroxides and metal hydrides',
'8.3': 'be able to indicate the oxidation number of an element in a compound or an ion, using a Roman numeral',
'8.4': 'be able to write formulae given oxidation numbers',
'8.5': 'understand oxidation and reduction in terms of electron transfer and changes in oxidation number, and the application of these ideas to reactions of s-block and p-block elements',
'8.6': 'know that oxidising agents gain electrons and reducing agents lose electrons',
'8.7': 'understand that a disproportionation reaction involves an element in a single species being simultaneously oxidised and reduced',
'8.8': 'know that oxidation number is a useful concept in terms of the classification of reactions as redox and as disproportionation',
'8.9': 'understand that metals, in general, form positive ions by loss of electrons with an increase in oxidation number whereas non-metals, in general, form negative ions by gain of electrons with a decrease in oxidation number',
'8.10': 'be able to write ionic half-equations and use them to construct full ionic equations',
'8.11': 'understand reasons for the trend in ionisation energy down Groups 1 and 2',
'8.12': 'understand reasons for the trend in reactivity of the elements down Group 1 (Li to K) and Group 2 (Mg to Ba)',
'8.13': 'know the reactions of the elements of Group 1 (Li to K) and Group 2 (Mg to Ba) with oxygen, chlorine and water',
'8.14': 'know the reactions of:\ni   oxides of Group 1 and 2 elements with water and dilute acid\nii   hydroxides of Group 1 and 2 elements with dilute acid',
'8.15': 'know the trends in solubility of the hydroxides and sulfates of Group 2 elements',
'8.16': 'understand the reasons for the trends in thermal stability of the nitrates and the carbonates of the elements in Groups 1 and 2 in terms of the size and charge of the cations involved',
'8.17': 'understand the formation of characteristic flame colours by Group 1 and 2 compounds in terms of electron transitions\nStudents will be expected to know the flame colours for Group 1 and 2 compounds.',
'8.18': 'know experimental procedures to show:\ni   patterns in the thermal decomposition of Group 1 and 2 nitrates and carbonates\nii   flame colours in compounds of Group 1 and 2 elements\nStudents will be expected to know tests for carbon dioxide and oxygen; and to recognise nitrogen dioxide by its colour and acidic pH.',
'8.19': 'know reactions, including ionic equations where appropriate, for identifying:\ni   carbonate ions, CO\u2083\u00b2\u207b, and hydrogencarbonate ions, HCO\u2083\u207b, using an aqueous acid to form carbon dioxide (and testing the gas with limewater)\nii   sulfate ions, SO\u2084\u00b2\u207b, using acidified barium chloride solution\niii   ammonium ions, NH\u2084\u207a, using sodium hydroxide solution and warming to form ammonia (and testing with litmus and HCl fumes)',
'8.20': 'be able to calculate solution concentrations, in mol dm\u207b\u00b3 and g dm\u207b\u00b3, including simple acid\u2013base titrations using the indicators methyl orange and phenolphthalein',
'8.21': 'CORE PRACTICAL 3\nFinding the concentration of a solution of hydrochloric acid.',
'8.22': 'understand how to minimize the sources of measurement uncertainty in volumetric analysis and estimate the overall uncertainty in the calculated result.',
'8.23': 'CORE PRACTICAL 4\nPreparation of a standard solution from a solid acid and use it to find the concentration of a solution of sodium hydroxide.',
'8.24': 'understand reasons for the trends for Group 7 elements in:\ni   melting and boiling temperatures and physical state at room temperature\nii   electronegativity\niii   reactivity down the group',
'8.25': 'understand the trend in reactivity of Group 7 elements in terms of the redox reactions of Cl\u2082, Br\u2082 and I\u2082 with halide ions in aqueous solution.\nStudents are expected to know the colours of the elements in standard conditions, in aqueous solution and in a non-polar organic solvent.',
'8.26': 'understand, in terms of changes in oxidation number, the following reactions of the halogens:\ni   oxidation reactions with Group 1 and 2 metals\nii   the disproportionation reaction of chlorine with water and the use of chlorine in water treatment.\niii   the disproportionation reaction of chlorine with cold, dilute aqueous sodium hydroxide to form bleach\niv   the disproportionation reaction of chlorine with hot alkali\nv   reactions analogous to those specified above',
'8.27': 'understand the following reactions:\ni   solid Group 1 halides with concentrated sulfuric acid, to illustrate the trend in reducing ability of the hydrogen halides\nii   precipitation reactions of the aqueous anions Cl\u207b, Br\u207b and I\u207b with aqueous silver nitrate solution and nitric acid, and the solubility of the precipitates in aqueous ammonia solution\niii   hydrogen halides with ammonia gas (to produce ammonium halides) and with water (to produce acids)',
'8.28': 'be able to make predictions about fluorine and astatine and their compounds, in terms of knowledge of trends in halogen chemistry',
}
for s in secs:
    n = s['number']
    if n == '8.0':
        continue
    check(s['spec'] == n, f'{n} spec ref matches section number')
    check(s['specText'] == VERBATIM[n], f'{n} specText verbatim')
    check(bool(s['title']) and bool(s['estMinutes']), f'{n} has title + minutes')

total_min = sum(s['estMinutes'] for s in secs)
check(abs(total_min / 60 - t8['estHours']) <= 0.34, f'estHours {t8["estHours"]} consistent with {total_min} min')

# ---- notes blocks ----
VALID = {'p', 'h3', 'def', 'eq', 'list', 'callout', 'worked', 'table', 'figure'}
figure_refs = []
for s in secs:
    content = s['content']
    if not content:
        fails.append(f"{s['number']} has NO notes")
        print(f'  FAIL {s["number"]} has no notes')
        continue
    blocks = json.loads(content)
    check(len(blocks) >= (3 if s['number'] == '8.0' else 4), f"{s['number']} notes density ({len(blocks)} blocks)")
    for b in blocks:
        if b.get('type') not in VALID:
            fails.append(f"{s['number']} invalid block type {b.get('type')}")
        if b.get('type') == 'figure':
            figure_refs.append(b['src'])
            figure_refs.append(b.get('srcDark'))

# every referenced figure exists in both variants
for src in set(figure_refs):
    if src:
        check((ROOT / ('public' + src)).exists(), f'figure exists: {src}')

print(f'  -> {len(set(r for r in figure_refs if r and "dark" not in r))} unique figures referenced')

# ---- flashcards ----
cards = [dict(r) for r in db.execute(
    "SELECT front,back FROM flashcards WHERE topicSlug='redox-and-groups' ORDER BY ord").fetchall()]
check(len(cards) == 17, f'17 flashcards (got {len(cards)})')

# ---- key chemistry strings present (spot audit) ----
all_text = ' '.join(s['content'] or '' for s in secs)
SPOTS = [
    'MnO\u2084\u207b + 8H\u207a + 5e\u207b \u2192 Mn\u00b2\u207a + 4H\u2082O',          # permanganate, acidic
    '5Fe\u00b2\u207a + MnO\u2084\u207b + 8H\u207a \u2192 5Fe\u00b3\u207a + Mn\u00b2\u207a + 4H\u2082O',  # overall
    '2NaOH(aq)  +  Cl\u2082(g)  \u2192  NaCl(aq)  +  NaOCl(aq)  +  H\u2082O(l)',  # cold alkali
    '6NaOH(aq)  +  3Cl\u2082(g)  \u2192  5NaCl(aq)  +  NaClO\u2083(aq)  +  3H\u2082O(l)',  # hot alkali
    'Cl\u2082(g)  +  H\u2082O(l)  \u21cc  HCl(aq)  +  HClO(aq)',                 # chlorine water
    '2M(s)  +  2H\u2082O(l)  \u2192  2MOH(aq)  +  H\u2082(g)',                   # group 1 water
    'Mg + H\u2082O(g) \u2192 MgO + H\u2082',                                      # steam
    'H\u2082SO\u2084 + 8H\u207a + 8I\u207b \u2192 H\u2082S + 4H\u2082O + 4I\u2082',  # H2S construction
    'Ag\u207a(aq) + Cl\u207b(aq) \u2192 AgCl(s)',                                  # silver test
    'Br\u2082(aq) + 2At\u207b(aq) \u2192 2Br\u207b(aq) + At\u2082(aq)',           # astatide displacement
    '0.0976 mol dm\u207b\u00b3',                                                   # CP4 calc
    '0.0892 mol dm\u207b\u00b3',                                                   # CP3-related calc
    '\u00b10.92%',                                                                # total uncertainty
    'MnO\u2084\u207b + 4H\u2082O + 5e\u207b \u2192 Mn\u00b2\u207a + 8OH\u207b',   # alkaline permanganate
]
for sp in SPOTS:
    check(sp in all_text, f'chemistry spot: {sp[:44]}')

# forbidden: unbalanced skeleton equations from the source must NOT leak
BAD = ['M(s) + H\u2082O(l) \u2192 M(OH)\u2082(aq) + H\u2082(g)',   # unbalanced source skeleton
       '2KOH  +  HCl']                                            # the fixed-in-time wrong eq
for b in BAD:
    check(b not in all_text, f'absent (source typo guard): {b[:40]}')

print()
print('RESULT:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILURES')
for f in fails:
    print(' -', f)
