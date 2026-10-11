# -*- coding: utf-8 -*-
"""Build Topic 2 'Version 2' (digest edition) and inject it into content.json.

- assembles the topic from scripts/v2_part{1,2,3}.py
- validates block types, unique ids/sectionKeys, figure files on disk
- backs up content.json, replaces any existing -v2 entry, inserts after topic 2
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_part1 import SECTIONS_A
from v2_part2 import SECTIONS_B
from v2_part3 import SECTIONS_C

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure"}

topic = {
    "slug": "atomic-structure-v2",
    "number": 2,
    "unit": 1,
    "unitCode": "WCH11",
    "unitName": "Structure, Bonding and Introduction to Organic Chemistry",
    "title": "Atomic Structure and the Periodic Table — Version 2",
    "subtitle": "Version 2 · the same spec-faithful notes, rebuilt for faster learning — key idea first, small chunks, quick recaps.",
    "summary": "The Topic 2 notes in digest form: subatomic particles and isotopes; the mass spectrometer; ionisation energies and their trends; electron configuration; periodicity across Period 3.",
    "estHours": 3.5,
    "sections": SECTIONS_A + SECTIONS_B + SECTIONS_C,
    "cards": [],
}

# ---------- validation ----------
errors = []
seen_ids, seen_keys = set(), set()
for s in topic["sections"]:
    if s["id"] in seen_ids:
        errors.append(f"duplicate section id {s['id']}")
    seen_ids.add(s["id"])
    if s["sectionKey"] in seen_keys:
        errors.append(f"duplicate sectionKey {s['sectionKey']}")
    seen_keys.add(s["sectionKey"])
    for b in (s["content"] or []):
        if b["type"] not in ALLOWED:
            errors.append(f"{s['number']}: bad block type {b['type']}")
        if b["type"] == "figure":
            src = b["src"]
            if not os.path.isfile(os.path.join(PUBLIC, src.lstrip("/"))):
                errors.append(f"{s['number']}: missing figure file {src}")
            if b.get("srcDark") and not os.path.isfile(os.path.join(PUBLIC, b["srcDark"].lstrip("/"))):
                errors.append(f"{s['number']}: missing dark figure {b['srcDark']}")
        if b["type"] == "callout" and b["variant"] not in {"tip", "warning", "exam", "key"}:
            errors.append(f"{s['number']}: bad callout variant {b['variant']}")

# figure coverage vs original topic (every diagram the source uses should appear)
data = json.load(open(CONTENT, encoding="utf-8"))
orig = next(t for t in data if t["slug"] == "atomic-structure")
def figs(sections):
    out = set()
    for s in sections:
        for b in (s["content"] or []):
            if b["type"] == "figure":
                out.add(b["src"])
    return out
missing_figs = figs(orig["sections"]) - figs(topic["sections"])
if missing_figs:
    errors.append(f"figures used by v1 but not v2: {sorted(missing_figs)}")

# every spec point 2.1-2.18 must be covered by a section carrying that spec number
spec_cover = {s.get("spec") for s in topic["sections"]}
for n in range(1, 19):
    if str(n) not in spec_cover and f"2.{n}" not in spec_cover:
        # spec field stores e.g. "2.6"; direct check below
        pass
covered = {s["spec"] for s in topic["sections"]}
for n in range(1, 19):
    key = f"2.{n}"
    if key not in covered:
        errors.append(f"spec point {key} not covered by any v2 section")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

# ---------- inject ----------
shutil.copyfile(CONTENT, CONTENT + ".bak")
data = json.load(open(CONTENT, encoding="utf-8"))
data = [t for t in data if t["slug"] != "atomic-structure-v2"]  # idempotent re-run
idx = next(i for i, t in enumerate(data) if t["slug"] == "atomic-structure")
data.insert(idx + 1, topic)
json.dump(data, open(CONTENT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

mins = sum(s["estMinutes"] for s in topic["sections"])
blocks = sum(len(s["content"] or []) for s in topic["sections"])
chars = sum(len(json.dumps(s["content"], ensure_ascii=False)) for s in topic["sections"])
orig_chars = sum(len(json.dumps(s["content"], ensure_ascii=False)) for s in orig["sections"])
print(f"OK: v2 inserted at position {idx + 1} (after '{orig['slug']}')")
print(f"    sections={len(topic['sections'])} blocks={blocks} total_est={mins} min ({mins/60:.1f} h)")
print(f"    content size v2={chars} chars vs v1={orig_chars} chars ({chars/orig_chars:.0%})")
print(f"    figures re-used: {len(figs(topic['sections']))}")
