# -*- coding: utf-8 -*-
"""Build Topic 2 'Version 2' (REFINED quick-revision edition) and inject it.

- assembles the topic from scripts/v3_part{1,2,3}.py
- validates block types (incl. qa), unique ids/sectionKeys, figure files,
  callout variants, qa item sanity
- backs up content.json, replaces any existing -v2 entry, inserts after topic 2
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v3_part1 import SECTIONS_A
from v3_part2 import SECTIONS_B
from v3_part3 import SECTIONS_C, CARDS

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure", "qa"}

topic = {
    "slug": "atomic-structure-v2",
    "number": 2,
    "unit": 1,
    "unitCode": "WCH11",
    "unitName": "Structure, Bonding and Introduction to Organic Chemistry",
    "title": "Atomic Structure and the Periodic Table — Version 2",
    "subtitle": "The quick-revision edition — one idea at a time, mark-scheme wording highlighted, and a check-yourself at the end of every section.",
    "summary": "Topic 2 rebuilt for fast learning: subatomic particles and isotopes; the mass spectrometer; ionisation energies and their trends; electron configuration; periodicity across Period 3.",
    "estHours": 2.5,
    "sections": SECTIONS_A + SECTIONS_B + SECTIONS_C,
    "cards": [],
}

cards = []
for i, c in enumerate(CARDS, start=1):
    cards.append({
        "id": f"v2t2card-{i:02d}",
        "ord": c["ord"],
        "front": c["front"],
        "back": c["back"],
        "tag": c["tag"],
    })
topic["cards"] = cards

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
        if b["type"] == "qa":
            if not b.get("items"):
                errors.append(f"{s['number']}: empty qa block")
            for it in b["items"]:
                if not it.get("q") or not it.get("a"):
                    errors.append(f"{s['number']}: qa item missing q or a")

# every figure used by v1 must appear in v2
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

# every spec point 2.1-2.18 must be covered by a section
covered = {s["spec"] for s in topic["sections"]}
for n in range(1, 19):
    key = f"2.{n}"
    if key not in covered:
        errors.append(f"spec point {key} not covered by any v2 section")

# every section must follow the rhythm: lead key callout + (mostly) a qa block
for s in topic["sections"]:
    if s["number"] == "2.0":
        continue
    blocks = s["content"] or []
    first = next((b for b in blocks if b["type"] == "callout"), None)
    if not first or first["variant"] != "key" or first["title"] != "In one line":
        errors.append(f"{s['number']}: missing lead 'In one line' key callout")
    if not any(b["type"] == "qa" for b in blocks):
        errors.append(f"{s['number']}: missing 'Check yourself' qa block")

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
qa_count = sum(1 for s in topic["sections"] for b in (s["content"] or []) if b["type"] == "qa")
qa_items = sum(len(b["items"]) for s in topic["sections"] for b in (s["content"] or []) if b["type"] == "qa")
print(f"OK: v2 (refined) inserted at position {idx + 1} (after '{orig['slug']}')")
print(f"    sections={len(topic['sections'])} blocks={blocks} qa_blocks={qa_count} qa_items={qa_items}")
print(f"    cards={len(topic['cards'])} total_est={mins} min ({mins/60:.1f} h)")
print(f"    content size v2={chars} chars vs v1={orig_chars} chars ({chars/orig_chars:.0%})")
print(f"    figures re-used: {len(figs(topic['sections']))}")
