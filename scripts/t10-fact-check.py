#!/usr/bin/env python3
"""Fact-coverage check: are the unmatched source facts present in T10 corpus (any phrasing)?"""
import json, re

CJ = '/home/z/my-project/src/lib/site/content.json'
content = json.load(open(CJ))
t10 = content[9]

corpus_parts = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('src', 'path', 'href', 'id'): continue
            walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)
    elif isinstance(o, str): corpus_parts.append(o)
walk(t10)
corpus = ' '.join(corpus_parts)
cl = re.sub(r'\s+', ' ', corpus.lower())

# key facts from the unmatched source lines -> search patterns (regex, flexible)
facts = [
    ("halogenoalkanes only single bonds",       r"only single bonds"),
    ("prefixes fluoro/chloro/bromo/iodo",       r"fluoro.*chloro.*bromo.*iodo"),
    ("locants used to show position",           r"locant"),
    ("halogens more electronegative than C",    r"more electronegative than (the )?carbon|greater electronegativity"),
    ("dipole induced in C-X / polar C-X",       r"dipole|polar.*c-?x|c-?x bond.*polar"),
    ("same reagent, rate varies two factors",   r"same (type of )?reaction|rate.{0,40}(two|2) factors"),
    ("heating under reflux",                    r"under reflux"),
    ("aqueous NaOH / KOH (substitution)",       r"aqueous (sodium|potassium) hydroxide|naoh\(aq\)|koh\(aq\)"),
    ("PCl5 with ethanol equation",              r"pch5|pcl5|phosphorus\(v\) chloride"),
    ("PCl3 / PI3 with alcohol",                 r"pi3|phosphorus triiodide|phosphorus\(iii\) iodide"),
    ("SOCl2 chlorination",                      r"socl2|thionyl"),
    ("NaBr/KBr + 50% H2SO4 (bromination)",     r"50% concentrated|sodium bromide|potassium bromide"),
    ("dehydration 170 C (conc H2SO4)",          r"170\s*(°|degrees|˚)|conc(entrated)? (sulphuric|sulfuric) acid.*170|170.*dehydration"),
    ("elimination produces alkene mixture",     r"mixture of alkenes|but-1-ene.*but-2-ene|but-2-ene.*but-1-ene"),
    ("alcohols general formula CnH2n+1OH",      r"c[nₙ]h|general formula"),
    ("isomerism types of haloalkanes",          r"isomerism"),
    ("solubility: non-polar chain grows",       r"solubility|non-?polar (hydrocarbon )?(chain|group|tail)"),
    ("lone pairs repelling / bond angle",       r"lone pair"),
]
print(f"corpus chars: {len(corpus)}")
for label, pat in facts:
    m = re.search(pat, cl)
    if m:
        s = max(0, m.start()-40); e = min(len(cl), m.end()+60)
        print(f"  COVERED  | {label:44s} | ...{cl[s:e]}...")
    else:
        print(f"  MISSING  | {label}")
