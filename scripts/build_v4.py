#!/usr/bin/env python3
"""build_v4.py — Humanize Topic 2 v2 (atomic-structure-v2).

User feedback: "the new key point and tips ui could be better and more
natural. The headings and subheadings should be more 'human', direct
and natural."

What this does (idempotent — safe to re-run):
  1. Every v2 callout gets style='note' → the new human note UI.
  2. The lead 'In one line' key callout of every section becomes a direct
     statement (title = the takeaway itself, text = the supporting line).
  3. 'Mark scheme wording' → 'Say it like this'; '60-second recap' → 'The short version'.
  4. Mechanical h3s ('The idea', 'Level 1 — …', 'i · …') become human ones.
  5. Meta headings that carried no content ('The must-know table',
     'The counting rules') are dropped; 2.8's duplicate endothermic key
     callout is folded into the lead callout.
  6. Section 2.0's rhythm map + topic subtitle rewritten to match.

Mark-scheme vocabulary inside the bodies is untouched.

Usage: python3 scripts/build_v4.py
"""
import json
import sys

PATH = '/home/z/my-project/src/lib/site/content.json'
SLUG = 'atomic-structure-v2'

data = json.load(open(PATH, encoding='utf-8'))
topic = next((t for t in data if t['slug'] == SLUG), None)
if topic is None:
    sys.exit(f'ERROR: topic {SLUG!r} not found')
secs = {s['number']: s for s in topic['sections']}


def blocks(n):
    return secs[n].get('content') or []


def callouts(n):
    return [b for b in blocks(n) if b['type'] == 'callout']


def rename_h3(n, olds, new):
    """Rename the h3 whose text is any of olds → new. Idempotent."""
    for b in blocks(n):
        if b['type'] == 'h3' and b['text'] in olds:
            b['text'] = new
            return
    if not any(b['type'] == 'h3' and b['text'] == new for b in blocks(n)):
        sys.exit(f'ERROR: h3 {olds!r} not found in section {n}')


def rename_callout(n, olds, new, variant=None):
    for b in callouts(n):
        if b['title'] in olds and (variant is None or b['variant'] == variant):
            b['title'] = new
            return
    if not any(b['title'] == new for b in callouts(n)):
        sys.exit(f'ERROR: callout {olds!r} not found in section {n}')


def drop(n, btype, title):
    """Remove first matching block; no-op if already gone."""
    for i, b in enumerate(blocks(n)):
        if b['type'] == btype and b.get('text' if btype == 'h3' else 'title') == title:
            secs[n]['content'].pop(secs[n]['content'].index(b))
            return


# ------------------------------------------------------------------
# 1 · note style on every v2 callout
# ------------------------------------------------------------------
for s in topic['sections']:
    for b in (s.get('content') or []):
        if b['type'] == 'callout':
            b['style'] = 'note'

# ------------------------------------------------------------------
# 2 · lead key callouts — title becomes the direct statement
# ------------------------------------------------------------------
KEY = {
    '2.1': ("Protons and neutrons sit in the nucleus; electrons occupy quantum shells around it.",
            "An atom is the smallest, **electrically neutral** particle of an element that can take part in a chemical change."),
    '2.2': ("Three values — learn them by heart.",
            "**Proton** — mass 1, charge +1 · **Neutron** — mass 1, charge 0 · **Electron** — mass 1/1840, charge −1."),
    '2.3': ("Z names the element; A counts the nucleus.",
            "**Z** = the number of protons · **A** = the protons + neutrons · **neutrons = A − Z**."),
    '2.4': ("Protons = Z · neutrons = A − Z · electrons = Z ± charge.",
            "For an ion, **add** electrons for a negative charge and **take away** for a positive one."),
    '2.5': ("Same protons, different neutrons.",
            "Isotopes are atoms of the same element — identical proton number, different neutron number."),
    '2.6': ("Ionise the atoms, then separate the ions by mass.",
            "On the spectrum: a peak's **position** → its **mass** · its **height** → its **abundance**."),
    '2.7': ("Atomic-ion peaks split 3 : 1; molecular-ion peaks line up 9 : 6 : 1.",
            "Chlorine is **75%** ³⁵Cl and **25%** ³⁷Cl — atomic ions at m/z 35 and 37; molecular ions at m/z 70, 72 and 74."),
    '2.8': ("One mole of electrons, from one mole of gaseous particles — every time.",
            "Energy must be supplied to overcome the attraction between the nucleus and the electron — so **every ionisation energy is endothermic**."),
    '2.9': ("Shell → sub-shell → orbital — and an orbital holds just two electrons.",
            "Sub-shells are the **s, p, d and f** divisions of a shell; orbitals are their subdivisions. The two electrons in an orbital must have **opposite spins**."),
    '2.10': ("Four things set the value: protons, shielding, distance, sub-shell.",
             "Ionisation energy depends on how far the outer electron is from the nucleus and on the **effective nuclear charge** it feels."),
    '2.11': ("Big jumps reveal shells; dips reveal sub-shells.",
             "**Big jumps** between successive ionisation energies → evidence for **quantum shells** (count them and you get the group) · **dips** in first ionisation energies across a period → evidence for **sub-shells**."),
    '2.12': ("s orbitals are spheres; p orbitals are dumbbells.",
             "Every shell has one s orbital, each one larger than the last · every p sub-shell has three p orbitals, at right angles along the x, y and z axes."),
    '2.13': ("Fill singly first; pair only with opposite spins.",
             "Hund's rule fills them singly; the Pauli Exclusion Principle insists that a pair has opposite spins."),
    '2.14': ("Lowest energy orbital first — so 4s fills before 3d.",
             "Write configurations in **spdf notation** or **electron-in-boxes** — and watch for chromium and copper, the two exceptions."),
    '2.15': ("Nucleons identify the atom; electrons decide how it reacts.",
             "It is the **electronic structure** that determines an atom's behaviour and chemical properties."),
    '2.16': ("The block names the sub-shell the last electron enters.",
             "Sub-shell capacities: **s 2 · p 6 · d 10 · f 14** electrons."),
    '2.17': ("Plot log(first IE) and the same saw-tooth repeats every period.",
             "Any property whose values repeat in a regular pattern, in order of atomic number, is a **periodic property**."),
    '2.18': ("Melting points rise to the giant structures, then collapse.",
             "First ionisation energy **generally rises** across a period — with two dips — and **falls** down a group."),
}
for n, (title, text) in KEY.items():
    lead = blocks(n)[0] if blocks(n) else None
    if lead is None or lead.get('type') != 'callout' or lead.get('variant') != 'key':
        sys.exit(f'ERROR: section {n} does not open with a key callout')
    lead['title'], lead['text'] = title, text

# ------------------------------------------------------------------
# 3 · exam + recap callout titles
# ------------------------------------------------------------------
for n in ('2.1', '2.3', '2.5', '2.8'):
    rename_callout(n, ('Mark scheme wording',), 'Say it like this', variant='exam')
for n in ('2.2', '2.6', '2.7', '2.9', '2.10', '2.16', '2.18'):
    rename_callout(n, ('60-second recap',), 'The short version', variant='tip')

# ------------------------------------------------------------------
# 4 · human h3 subheadings
# ------------------------------------------------------------------
H3 = [
    ('2.1', ('The idea',), 'The three particles, and where they are'),
    ('2.1', ('What each part does',), 'What each particle does'),
    ('2.2', ('The same table, in full',), 'In full — with units'),
    ('2.5', ('Same chemistry, different physics',), 'What stays the same, and what changes'),
    ('2.6', ("First — why masses are called 'relative'", "Why 'relative'?"), "Why 'relative'?"),
    ('2.6', ('Four mass definitions to know', 'The four mass definitions'), 'The four mass definitions'),
    ('2.6', ('The instrument', 'Inside the machine'), 'Inside the machine'),
    ('2.6', ('What it is used for', "What it's used for"), "What it's used for"),
    ('2.6', ('The five stages — in order', 'The five stages, in order'), 'The five stages, in order'),
    ('2.6', ('Reading a spectrum', 'How to read a spectrum'), 'How to read a spectrum'),
    ('2.6', ('Molecular ions — finding the RMM', 'Molecular ions: finding the RMM'), 'Molecular ions: finding the RMM'),
    ('2.9', ('Level 1 — quantum shells', 'Start with the shells'), 'Start with the shells'),
    ('2.9', ('Level 2 — sub-shells', 'Inside a shell: sub-shells'), 'Inside a shell: sub-shells'),
    ('2.9', ('Level 3 — orbitals', 'Inside a sub-shell: orbitals'), 'Inside a sub-shell: orbitals'),
    ('2.10', ('The four factors', 'The four factors, one by one'), 'The four factors, one by one'),
    ('2.16', ('How many electrons fit — the first four shells', 'How many electrons fit in each shell'), 'How many electrons fit in each shell'),
    ('2.17', ('Why logarithms', 'Why logarithms?'), 'Why logarithms?'),
    ('2.18', ('i · Melting and boiling temperatures', 'Melting and boiling temperatures'), 'Melting and boiling temperatures'),
    ('2.18', ('Explaining the melting point trend',), 'Explaining the melting point trend'),  # already human
    ('2.18', ('ii · First ionisation energy across a period', 'First ionisation energy across a period'), 'First ionisation energy across a period'),
    ('2.18', ('The specific trends — explaining the deviations', 'The two dips, explained'), 'The two dips, explained'),
    ('2.18', ('iii · First ionisation energy down the group', 'First ionisation energy down a group'), 'First ionisation energy down a group'),
]
for n, olds, new in H3:
    rename_h3(n, olds, new)

# ------------------------------------------------------------------
# 5 · drop meta headings + the duplicate endothermic callout
# ------------------------------------------------------------------
drop('2.2', 'h3', 'The must-know table')
drop('2.4', 'h3', 'The counting rules')
drop('2.8', 'callout', 'All ionisation energies are endothermic')

# ------------------------------------------------------------------
# 6 · section 2.0's flow map + topic subtitle
# ------------------------------------------------------------------
b0 = blocks('2.0')
p0 = next((b for b in b0 if b['type'] == 'p' and b['text'].startswith('Every section')), None)
if p0 is not None:
    p0['text'] = 'Every section has the same shape, so you always know what to do next:'
ul0 = next((b for b in b0 if b['type'] == 'list'), None)
if ul0 is not None and len(ul0['items']) == 5:
    ul0['items'] = [
        "Every section **opens with the key point** — the one thing it is really about.",
        "Then the idea is **built up in short steps**, with the figures and tables that carry it.",
        "Where wording matters, an **In the exam** note shows the words the mark scheme wants.",
        "A **tip** closes most sections with the short version — everything worth remembering at a glance.",
        "And every section ends with a **quick check** — answer from memory first, then tap to reveal.",
    ]
topic['subtitle'] = ('The quick-revision edition — each section opens with its key point, builds the idea '
                     'in short steps, points out the words the mark scheme wants, and ends with a quick check.')

# ------------------------------------------------------------------
# validate + save
# ------------------------------------------------------------------
errors = []
for s in topic['sections']:
    for b in (s.get('content') or []):
        if b['type'] == 'callout':
            if b.get('style') != 'note':
                errors.append(f"{s['number']}: callout {b['title']!r} missing note style")
            if b['title'] in ('In one line', '60-second recap', 'Mark scheme wording'):
                errors.append(f"{s['number']}: robot callout title survived: {b['title']!r}")
        if b['type'] == 'h3' and b['text'] in ('The idea', 'The must-know table', 'The counting rules',
                                               'Level 1 — quantum shells', 'i · Melting and boiling temperatures'):
            errors.append(f"{s['number']}: mechanical h3 survived: {b['text']!r}")
    # every content section 2.1–2.18 must still open with its key callout
    if s['number'] != '2.0':
        lead = (s.get('content') or [None])[0]
        if not lead or lead.get('type') != 'callout' or lead.get('variant') != 'key':
            errors.append(f"{s['number']}: lead key callout lost")
if errors:
    sys.exit('VALIDATION FAILED:\n' + '\n'.join(errors))

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')

n_callouts = sum(1 for s in topic['sections'] for b in (s.get('content') or []) if b['type'] == 'callout')
print(f'OK: {len(topic["sections"])} sections, {n_callouts} note-style callouts, subtitle + flow map updated.')
print('Robot labels remaining: 0')
