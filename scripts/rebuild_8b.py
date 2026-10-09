# -*- coding: utf-8 -*-
"""Rebuild Topic 8B notes (sections 8.11-8.23) verbatim from 'upload/Group 1 and 2 notes.pdf'.
Anchor-based replacement in prisma/seed-data/notes.ts + blurb cleanup in topics.ts.
Method identical to rebuild_8a.py / rebuild_8c.py (user-accepted 8A & 8C rebuilds).

Iron rules: verbatim to source; no unnecessary terminology; nothing outside the
syllabus; zero mistakes. Worksheet exercises left blank in the source (EXERCISE
1-6, element/oxygen + chlorine worksheets, acid worksheets, K/Rb/Cs nitrate rows,
Group II carbonate rows, SrO/BaO rows, unworked worked examples) are NOT answered
or included. Equations the source leaves unbalanced are presented balanced.
"""
import sys
sys.path.insert(0, '/home/z/my-project/scripts')
from importlib import import_module
b1 = import_module('8b_blocks1') if False else None

# importlib can't import names starting with digits easily; use exec instead
ns1, ns2 = {}, {}
exec(open('/home/z/my-project/scripts/8b_blocks1.py', encoding='utf-8').read(), ns1)
exec(open('/home/z/my-project/scripts/8b_blocks2.py', encoding='utf-8').read(), ns2)

PATH = '/home/z/my-project/prisma/seed-data/notes.ts'
TPATH = '/home/z/my-project/prisma/seed-data/topics.ts'

src = open(PATH, encoding='utf-8').read()

KEYS = ['group1-2-ionisation-energy', 'group1-2-reactivity', 'group1-2-reactions',
        'oxides-hydroxides-acids', 'group2-solubility', 'thermal-stability',
        'flame-colours', 'thermal-decomposition-experiment', 'tests-for-ions',
        'solution-concentrations', 'core-practical-3', 'measurement-uncertainty',
        'core-practical-4']
BLOCKS = [ns1['B_811'], ns1['B_812'], ns1['B_813'], ns1['B_814'], ns1['B_815'], ns1['B_816'],
          ns2['B_817'], ns2['B_818'], ns2['B_819'], ns2['B_820'], ns2['B_821'],
          ns2['B_822'], ns2['B_823']]
assert len(KEYS) == len(BLOCKS) == 13


def replace_span(s, start_marker, end_marker):
    assert s.count(start_marker) == 1, 'start not unique: %s (%d)' % (start_marker[:60], s.count(start_marker))
    assert s.count(end_marker) == 1, 'end not unique: %s (%d)' % (end_marker[:60], s.count(end_marker))
    i = s.index(start_marker)
    j = s.index(end_marker)
    assert i < j, 'order wrong for %s' % start_marker[:40]
    return s[:i] + block_for(start_marker) + '\n\n' + s[j:]


CURRENT_BLOCK = {}

for key, block in zip(KEYS, BLOCKS):
    CURRENT_BLOCK["    '%s': [" % key] = block.rstrip()


def block_for(marker):
    return CURRENT_BLOCK[marker]


# apply from last to first so earlier spans are unaffected by later edits
for key in reversed(KEYS):
    start = "    '%s': [" % key
    if key != KEYS[-1]:
        nxt = "    '%s': [" % KEYS[KEYS.index(key) + 1]
    else:
        nxt = "    'group7-trends': ["
    src = replace_span(src, start, nxt)

open(PATH, 'w', encoding='utf-8').write(src)
print('notes.ts: 13 sections replaced')

# ---------------------------------------------------------------- topics.ts blurbs
t = open(TPATH, encoding='utf-8').read()
BLURBS = [
    ("blurb: 'Down the group it gets easier to lose the outer electron — here is why.',",
     "blurb: 'The Group 1 and 2 elements, their configurations, atomic radii and the fall in ionisation energy down the group.',"),
    ("blurb: 'Lower ionisation energy, faster reaction — the trend and its reason.',",
     "blurb: 'Reactivity increases down the group — and Group I is more reactive than Group II.',"),
    ("blurb: 'What the s-block elements do — and what you observe as you go down.',",
     "blurb: 'Reactions of the Group 1 and 2 elements with oxygen, chlorine and water, with the observations for each metal.',"),
    ("blurb: 'Basic oxides, alkaline solutions, neutralisation — salts and water.',",
     "blurb: 'Basic oxides (beryllium oxide is amphoteric) and their reactions with water and with dilute acids.',"),
    ("blurb: 'Hydroxides dissolve more as you descend; sulfates dissolve less.',",
     "blurb: 'Solubility of Group 2 hydroxides increases down the group; sulfates decreases.',"),
    ("blurb: 'Polarising power decides it — down the group stabler, across to Group 2 less so.',",
     "blurb: 'How cation size and charge control the thermal stability of the nitrates and carbonates.',"),
    ("blurb: 'Excitation, relaxation, emission — and the colour chart you must know.',",
     "blurb: 'Excitation and relaxation of electrons — and the flame colours of the Group 1 and 2 cations.',"),
    ("blurb: 'How the evidence is gathered — apparatus, timing, gas tests and the wire.',",
     "blurb: 'The thermal decomposition experiment and the flame test procedure.',"),
    ("blurb: 'Three gas-and-precipitate tests, with the ionic equations to match.',",
     "blurb: 'Tests for ammonium, carbonate and hydrogencarbonate, and sulfate ions — with observations and ionic equations.',"),
    ("blurb: 'Standard solutions, burettes, indicators — and n = cV.',",
     "blurb: 'Volumetric analysis: apparatus, standard solutions, concentration calculations, indicators and the mean titre.',"),
    ("blurb: 'Titrate the unknown acid against a standard alkali — then calculate.',",
     "blurb: 'Core Practical 3: the titration method for finding the concentration of an acid solution.',"),
    ("blurb: 'Random vs systematic, accuracy vs precision — and adding up the ±.',",
     "blurb: 'Mistakes, errors, accuracy and precision, measurement uncertainty and overall percentage uncertainty.',"),
    ("blurb: 'Weigh, dissolve, transfer, make up to the mark — then find the NaOH.',",
     "blurb: 'Core Practical 4: preparation of a standard solution from a solid acid.',"),
]
for old, new in BLURBS:
    assert t.count(old) == 1, 'blurb not unique: %s (%d)' % (old[:60], t.count(old))
    t = t.replace(old, new)
open(TPATH, 'w', encoding='utf-8').write(t)
print('topics.ts: 13 blurbs replaced')
