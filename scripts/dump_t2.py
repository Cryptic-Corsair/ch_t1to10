#!/usr/bin/env python3
"""Dump topic 2 content.json as readable plain text for study."""
import json

d = json.load(open('/home/z/my-project/src/lib/site/content.json'))
t2 = [t for t in d if t['slug'] == 'atomic-structure'][0]

out = []
out.append(f"TOPIC: {t2['title']} | subtitle: {t2['subtitle']} | summary: {t2['summary']} | estHours: {t2['estHours']}")
out.append("")
for s in t2['sections']:
    out.append(f"===== {s['number']} {s['title']} [spec {s.get('spec')}] ({s['estMinutes']} min)")
    out.append(f"  blurb: {s['blurb']}")
    if s.get('specText'):
        out.append(f"  specText: {s['specText']}")
    for o in s.get('outline', []):
        out.append(f"  outline: {o}")
    if s['content']:
        for b in s['content']:
            t = b['type']
            if t == 'p':
                out.append(f"  P: {b['text']}")
            elif t == 'h3':
                out.append(f"  H3: {b['text']}")
            elif t == 'def':
                out.append(f"  DEF [{b['term']}]: {b['text']}")
            elif t == 'eq':
                out.append(f"  EQ: {b['code']}  ({b.get('caption','')})")
            elif t == 'list':
                pre = 'OL' if b.get('ordered') else 'UL'
                for i, it in enumerate(b['items'], 1):
                    out.append(f"  {pre}{i}: {it}")
            elif t == 'callout':
                out.append(f"  CALLOUT[{b['variant']}] {b['title']}: {b['text']}")
            elif t == 'worked':
                out.append(f"  WORKED: {b['title']}")
                out.append(f"    problem: {b['problem']}")
                for st in b['steps']:
                    out.append(f"    step: {st}")
                out.append(f"    answer: {b['answer']}")
            elif t == 'table':
                out.append(f"  TABLE headers: {b['headers']}")
                for r in b['rows']:
                    out.append(f"    row: {r}")
            elif t == 'figure':
                out.append(f"  FIG: {b['src']} | alt: {b['alt']} | caption: {b.get('caption','')}")
            else:
                out.append(f"  ?? {t}")
    out.append("")

out.append("===== FLASHCARDS =====")
for c in t2['cards']:
    out.append(f"  [{c['tag']}] {c['front']}  =>  {c['back']}")

open('/home/z/my-project/scripts/t2-readable.txt', 'w').write("\n".join(out))
print(len(out), "lines written")
