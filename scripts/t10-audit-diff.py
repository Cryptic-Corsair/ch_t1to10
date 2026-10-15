#!/usr/bin/env python3
"""Verbatim audit v2: tokenized corpus + tokenized chunks, fair 6-word window match."""
import json, re, os

SRC = '/home/z/my-project/scripts/t10-sources'
CJ = '/home/z/my-project/src/lib/site/content.json'

content = json.load(open(CJ))
t10 = content[9]

corpus_parts = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('src', 'path', 'href', 'id'):  # skip file paths/ids (not prose)
                continue
            walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)
    elif isinstance(o, str):
        corpus_parts.append(o)
walk(t10)

TOK = re.compile(r'[a-z0-9\u2080-\u2099\u2070-\u209f\u00b0\'\-\+]+')
def toks(s):
    s = s.lower().replace('\u2013','-').replace('\u2014','-').replace('\u2019',"'").replace('\xa0',' ')
    return TOK.findall(s)

corpus_toks = []
for p in corpus_parts: corpus_toks.extend(toks(p))
# build set of all 6-grams and 4-grams from corpus
def gramset(toks_list, n):
    return {' '.join(toks_list[i:i+n]) for i in range(len(toks_list)-n+1)}
G6 = gramset(corpus_toks, 6)
G4 = gramset(corpus_toks, 4)
print(f"corpus tokens: {len(corpus_toks)}, 6-grams: {len(G6)}")

report = {}
for fname in ['Halogenoalkane.json', 'Alcohols.json']:
    data = json.load(open(os.path.join(SRC, fname)))
    full = ' '.join(p['text'] for p in data['pages'])
    chunks = re.findall(r'[^.\n•·]{25,240}', full)
    checked = 0; strong = 0; weak = 0; misses = []
    for ch in chunks:
        words = [w for w in toks(ch) if not re.fullmatch(r'\d{1,3}', w)]
        if len(words) < 6: continue
        checked += 1
        hits6 = hits4 = total = 0
        for i in range(len(words) - 5):
            total += 1
            g = ' '.join(words[i:i+6])
            if g in G6: hits6 += 1
            if g[:None] and ' '.join(words[i:i+4]) in G4: hits4 += 1
        # strong: >=35% of 6-word windows verbatim; weak: any 4-gram hit
        if total and hits6 / total >= 0.35: strong += 1
        elif hits4 > 0: weak += 1
        else: misses.append(ch.strip()[:110])
    report[fname] = {'checked': checked, 'strong_verbatim': strong, 'partial_4gram': weak, 'no_match': checked - strong - weak}
    print(f"\n=== {fname}: strong-verbatim {strong}/{checked} ({round(100*strong/checked)}%), partial {weak}, unmatched {checked-strong-weak} ===")
    for m in misses[:18]:
        print(f"  UNMATCHED: {m}")
json.dump(report, open('/home/z/my-project/scripts/t10-audit-results.json','w'), indent=1)
