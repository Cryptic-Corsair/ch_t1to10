#!/usr/bin/env python3
"""Verify the Topic 9 (9A Kinetics) build: verbatim source anchors, spec-text
fidelity vs the official specification, structure, figures, banned patterns."""
import re
import sys
from pathlib import Path

ROOT = Path('/home/z/my-project')
notes = (ROOT / 'prisma/seed-data/notes.ts').read_text()
topics = (ROOT / 'prisma/seed-data/topics.ts').read_text()
spec = (ROOT / 'scripts/spec_full.txt').read_text()

ok, fail = 0, 0


def check(name, cond, detail=''):
    global ok, fail
    if cond:
        ok += 1
        print('  PASS %s' % name)
    else:
        fail += 1
        print('  FAIL %s %s' % (name, detail))


# ---- locate the topic 9 spans -------------------------------------------------
tstart = topics.index("slug: 'kinetics-and-equilibria'")
tend = topics.index("slug: 'halogenoalkanes-alcohols-spectra'")
tspan = topics[tstart:tend]

nstart = notes.index("'kinetics-and-equilibria': {")
nspan = notes[nstart:]
nspan = nspan[:nspan.index("\n}\n") + 1] if "\n}\n" in nspan else nspan
nplain = nspan.replace('**', '')  # anchors match content regardless of bold markers
# 9A (kinetics) span ends where the 9B (equilibria) sections begin
_n9b = nspan.index("'reversible-dynamic-equilibrium': [")
nspan9a = nspan[:_n9b]

print('== topics.ts structure ==')
for key in ['specification-map', 'collision-theory-rate-factors', 'activation-energy',
            'calculating-rate', 'maxwell-boltzmann-temperature', 'catalysts-alternative-routes',
            'reaction-profiles-catalysed', 'catalysts-industry', 'maxwell-boltzmann-catalyst',
            'reversible-dynamic-equilibrium', 'conditions-equilibrium-position',
            'reversible-reactions-industry']:
    check('section %s' % key, key in tspan)
for num in ['9.0', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10', '9.11']:
    check("number '%s'" % num, ("'%s'" % num) in tspan)
check('old key collision-theory gone', "sectionKey: 'collision-theory'," not in tspan)
check('old key maxwell-boltzmann gone', "sectionKey: 'maxwell-boltzmann'," not in tspan)
check('old key catalysts gone', "sectionKey: 'catalysts'," not in tspan)
check('old key dynamic-equilibrium gone', "sectionKey: 'dynamic-equilibrium'," not in tspan)
check('old key kc gone', "sectionKey: 'kc'," not in tspan)
check('no Kc in topic span', 'Kc' not in tspan, '(Kc is not in IAL Topic 9)')
check('no Haber named in 9A notes', 'Haber' not in nspan9a, '(Haber belongs to 9.11 only)')

print('== spec text fidelity (verbatim vs official spec) ==')
spec_statements = {
    '9.1': 'understand, in terms of the collision theory, the effect of changes in concentration, temperature, pressure and surface area on the rate of a chemical reaction',
    '9.2': 'understand that reactions take place only when collisions have sufficient energy, known as the activation energy',
    '9.3': 'be able to calculate the rate of a reaction from:\ni   the time taken for a reaction, using rate = 1/time\nii   the gradient of suitable graph, by drawing a tangent, either for initial rate, or at a time, t',
    '9.4': 'understand qualitatively, in terms of the Maxwell-Boltzmann distribution of molecular energies, how changes in temperature affect the rate of a reaction',
    '9.5': 'understand the role of catalysts in providing alternative reaction routes of lower activation energy',
    '9.6': 'be able to draw the reaction profiles for uncatalysed and catalysed reactions, including the energy level of the intermediate formed with the catalyst',
    '9.7': 'understand the use of catalysts in industry to make processes more sustainable by using less energy and/or higher atom economy',
    '9.8': 'be able to interpret the action of a catalyst in terms of a qualitative understanding of the Maxwell-Boltzmann distribution of molecular energies',
    '9.9': 'know that many reactions are readily reversible and that they can reach a state of dynamic equilibrium in which:\ni   the rate of the forward reaction is equal to the rate of the backward reaction\nii   the concentrations of the reactants and the products remain constant',
    '9.10': 'be able to predict and justify the qualitative effects of changes of temperature, pressure and concentration on the position of equilibrium in a homogeneous system',
    '9.11': 'evaluate data to explain the necessity, for many industrial processes, to reach a compromise between the yield and the rate of reaction',
}
# each statement must exist in the official spec text (normalized) and in topics.ts specText
def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\\n', ' ')).strip().lower()

spec_n = norm(spec)
for num, st in spec_statements.items():
    check('spec %s in official spec' % num, norm(st) in spec_n)
    esc = st.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    # topics.ts stores literal \n sequences inside the TS string
    ts_literal = st.replace('\n', '\\n')
    check('spec %s in topics.ts specText' % num, ts_literal in tspan or st in tspan)
    check('spec %s in notes.ts map row' % num, ts_literal in nspan or st in nspan)

print('== verbatim source anchors (Kinetics.pdf) ==')
anchors = [
    # 9A-1 rate + collision theory (p2-5)
    'Chemical kinetics is concerned with the dynamics of chemical reactions such as the way reactions take place and the rate (speed) of the process.',
    'The decrease in the concentration of any one of the reactants per unit time',
    'OR the increase in the concentration of any one of the product per unit time',
    'change in concentration / time for change to happen',
    'the concentration of the reactants decreases or the concentration of the products increases',
    'the slope of the graph measures the rate of the reaction',
    'How fast one of the reactants is used up',
    'How fast one of the products is formed',
    'The gradient decreases as the rate decreases and becomes zero when all reactants are used up.',
    'drawing a tangent at a point (eg point A) and measuring its gradient',
    'Y = change of concentration (mol dm⁻³)',
    'Unit of rate = mol dm⁻³ s⁻¹',
    'The slope at the start of the reaction will give the initial rate',
    'The slope gets less (showing the rate is slowing down) as the reaction proceeds.',
    'must collide',
    'not all collisions will lead to a reaction',
    'approach each other in the correct orientation',
    'certain minimum amount of energy referred to as the activation energy (Ea)',
    'A reaction occurs when the reactants collide each other in the correct orientation',
    'Such collisions are effective or successful collisions',
    'Collisions will result in reaction only if the molecules collide in the proper geometry',
    # activation energy (p4)
    'Activation energy is the minimum energy that colliding particles must possess for a reaction to occur.',
    'they simply bounce apart and no reaction occurs',
    'Only those collisions that have energies equal to or greater than activation energy result in a reaction.',
    'Activation energy is involved in breaking some of the original bonds.',
    'If collisions are relatively gentle, there is not enough energy available to break the bonds and so particles do not react.',
    # 9A-2 factors (p6-8)
    'reactant particles must collide with sufficient energy before they can react',
    'increasing the frequency of collision with sufficient energy between reacting particles',
    'Collisions that result in a reaction are called successful collisions',
    'Reactant particles per unit volume increases.',
    'Reactant particles per unit volume decreases.',
    'reactions start off at their fastest then slow as the reactant concentration drops',
    'CaCO₃(s) + 2HCl → CaCl₂ + CO₂(g)',
    'Curve A is steeper therefore rate of reaction is faster than curve B.',
    'Gradient of curve A is greater than gradient of curve B.',
    'Curve A levels off quickly compared to curve B indicating faster completion of reaction.',
    'Increasing the pressure of gaseous reacting particles or decreasing the volume of the reaction vessel increases the rate of the reaction',
    'Same number of gaseous molecules in smaller space',
    'makes gas particles get closer together',
    'Changing the pressure has almost no effect on reactions in solid or liquid phase',
    'For heterogeneous reactions increasing surface area leads to more chances of a collision.',
    'Greater surface area of the solid is exposed for collision.',
    'catalytic converters',
    'More surface is exposed for reaction',
    'only collisions with magnesium atoms on the surface result in a reaction',
    'powdered magnesium gives off hydrogen more quickly',
    # temperature (p12)
    'Average kinetic energy of the particles increases.',
    'Speed of the particles also increases.',
    'So the frequency of effective collisions increases.',
    'trapped in a',
    'solvent cage',
    'by a process of diffusion, in the same solvent cage',
    'They have to react.',
    'proportional to their concentrations, same as in gas phase',
    # 9A-3 Maxwell-Boltzmann (p10-11)
    'The molecules in a sample of gas have a wide range of energies.',
    'there is a spread of molecular velocities and energies',
    'No particles have zero velocity (all the particles have some amount of energy).',
    'Some have very low and some have very high velocities.',
    'Most have intermediate velocities.',
    'Area under the curve represents the total number of particles in the system.',
    'distribution of energies of the molecules in a gas (but can also be applied for particles in a solution)',
    'area under the curve beyond this Ea value is proportional to the number of particles with energy greater than activation energy',
    'only about 1 in 10¹² molecules possesses this energy',
    'kinetically stable',
    'Such reactions occur only if the temperature is increased.',
    'higher energies/velocities',
    'broader and flatter',
    'Area under the curve stays constant',
    'A small rise in temperature can lead to a large increase in rate.',
    'Neither curve is symmetrical.',
    'start at the origin and finish by approaching the X axis and do not touch the X axis',
    'The area under both curves is the same.',
    'The peak of the T₂ distribution is to the right and lower than the peak of the T₁ distribution.',
    # 9A-4 catalysts (p13-17)
    'A catalyst alters rate of reaction by providing an alternative path with lower activation energy',
    'they do not undergo any permanent chemical change',
    'Catalysts are specific to reactions and they cause the reaction rate to increase.',
    'the energy levels of the reactants and the products of the reaction and of the transition state',
    'The activation energy (Ea) and the enthalpy change (ΔHr) are also shown on the diagram.',
    'exothermic and endothermic reaction are shown in the reaction profile diagram',
    'takes place using a different route from the uncatalyzed reaction',
    'If an intermediate is formed between the reactant and the catalyst then the reaction takes place in at least two steps',
    'peroxydisulphate ions and iodide ions, catalyzed by Fe²⁺ ions',
    'Enthalpy profile diagram for a catalyzed reaction involving the formation of an intermediate',
    'Catalysts have been increasingly used in the chemical industry.',
    'political and environmental reasons as well',
    'Two major economic advantages of the use of catalysts are:',
    'more of the desired product can be made in a given period of time',
    'decrease in the energy costs to the manufacturer',
    'A homogeneous catalyst is one that is in the same phase (physical state) as the reactants.',
    'Fe²⁺ ion catalyst in oxidation of iodide ions',
    'persulphate ions S₂O₈²⁻',
    'Both the reactants and the iron(II) catalyst are in the aqueous phase.',
    'Most catalysts used in industry are heterogeneous catalysts.',
    'in a different phase from the reactants',
    'Solids are commonly used as heterogeneous catalysts for reactions involving gases.',
    'many reactions between gases are catalyzed using a solid catalyst',
    'N₂(g)  +  3H₂(g)  ⇌  2NH₃(g)',
    'Iron powder as a catalyst',
    'the reactants are in the gaseous state, but the catalyst is in the solid state',
    'active sites on the surface of a solid (e.g. a metal)',
    'Gases are adsorbed onto the surface and form weak bonds with metal atoms',
    'use some of the electrons from bonds within the gas molecules thus weakening these bonds',
    'held on the surface of the metal in just the right orientation',
    'The products are then released from the active sites.',
    'waste is produced when products are formed',
    'little or no co-product (waste)',
    'phenol can be manufactured by the oxidation of dinitrogen monoxide (N₂O)',
    'zeolite catalyst',
    'nitrogen as the only by-product',
    'Manufacture of phenol using benzene via cumene has a very low atom economy.',
    'Fewer steps are involved in the manufacture',
    'The percentage yield of each step may be higher',
    'Less product is lost in the separation after each step',
    'more product is obtained in a given time',
    # 9.8 MB + catalyst (p14)
    'Catalysts provide an alternative pathway with lower activation energy.',
    'Since activation energy is reduced, more particles have sufficient energy for effective collisions.',
    'the number of effective collisions increases, thus increasing the rate of reaction',
    'Using catalysts avoids the need to supply extra heat',
    'Catalysts remain chemically unchanged at the end of the reaction.',
    # specification map extras
    'decomposition of hydrogen peroxide, reaction of marble chips with acid, reaction of thiosulfate ions with acid',
]
for a in anchors:
    check('anchor: %s…' % a[:58], a in nplain)

print('== chemistry correctness ==')
check('persulphate equation balanced (2I⁻)', 'S₂O₈²⁻(aq)  +  2I⁻(aq)' in nspan)
check('ammonia equilibrium equation present', 'N₂(g)  +  3H₂(g)  ⇌  2NH₃(g)' in nspan)
check('rate unit correct', 'mol dm⁻³ s⁻¹' in nspan)

print('== banned patterns ==')
banned = ['Checkpoint', 'CHECKPOINT', 'exam-trap', 'Beyond the spec', "exam's favourite",
          'book-keeping', 'household bleach', 'worked', 'Kc expression',
          'Le Chatelier']
for b in banned:
    check('absent: %r' % b, b not in nspan)
# 9A-scoped bans (legitimate in 9B: the source boxes a key-point note and the spec
# itself reads "dynamic equilibrium in which:")
check('absent in 9A: callout blocks', "type: 'callout'" not in nspan9a)
_n9a_content = nspan9a.index("'collision-theory-rate-factors': [")
check('absent in 9A content: spec echo "dynamic equilibrium in which"',
      'dynamic equilibrium in which' not in nspan9a[_n9a_content:])

print('== block types valid ==')
types = set(re.findall(r"type: '([a-z]+)'", nspan))
check('only valid block types', types <= {'p', 'h3', 'def', 'eq', 'list', 'worked', 'table', 'figure', 'callout'},
      'found %s' % types)
check('no worked blocks in topic 9 (no invented answers)', 'worked' not in types)

print('== figures wired ==')
srcs = re.findall(r"src: '(/diagrams/[^']+)'", nspan)
check('18 figures referenced (12 9A + 6 9B)', len(srcs) == 18, 'found %d' % len(srcs))
for s in srcs:
    p = ROOT / ('public' + s)
    check('exists %s' % Path(s).name, p.exists())
    d = p.with_name(p.stem + '-dark.png')
    check('exists %s' % d.name, d.exists())

print('== regression: topics 1-8 intact ==')
for a in ["'amount-of-substance': {", "'atomic-structure': {", "'bonding-and-structure': {",
          "'alkenes': {", "'organic-intro-and-alkanes': {", "'energetics': {",
          "'intermolecular-forces': {", "'redox-and-groups': {"]:
    check('notes key %s' % a, a in notes)
check('topic 8 spec map intact', '8.28' in notes)
check('topic 8 anchor intact', 'know what is meant by the term' in notes)

print()
print('RESULT: %d passed, %d failed' % (ok, fail))
sys.exit(1 if fail else 0)
