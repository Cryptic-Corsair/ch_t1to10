#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Topic 10 — fill the five empty sections + add the 10.0 Specification Map.

- assembles the topic from scripts/t10/sections_{a,b,c}.py
- validates block types, unique ids/sectionKeys, figure files on disk
- backs up content.json, replaces the halogenoalkanes-alcohols-spectra entry
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t10.sections_a import SECTIONS_A  # noqa: E402
from t10.sections_b import SECTIONS_B  # noqa: E402
from t10.sections_c import SECTIONS_C  # noqa: E402

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure", "qa"}

sections = SECTIONS_A + SECTIONS_B + SECTIONS_C

# ---------- validation ----------
errors = []
seen_ids, seen_keys = set(), set()
for s in sections:
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

# mark-scheme keyword spot-checks (the vocabulary must survive the rewrite)
joined = json.dumps(sections, ensure_ascii=False)
for kw in ["electron-pair donor", "nucleophilic substitution", "bond enthalpy",
           "distil", "reflux", "Benedict's or Fehling's", "sodium carbonate",
           "molecular ion", "fragmentation", "fingerprint", "wavenumber",
           "enhanced greenhouse effect", "nucleophile", "elimination",
           "hydrolysis", "heating under reflux", "separating funnel",
           "anhydrous salt", "boiling temperature"]:
    if kw not in joined:
        errors.append(f"mark-scheme keyword missing: {kw}")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

# ---------- inject ----------
with open(CONTENT, "r", encoding="utf-8") as f:
    data = json.load(f)

shutil.copyfile(CONTENT, CONTENT + ".bak")

slug = "halogenoalkanes-alcohols-spectra"
idx = next(i for i, t in enumerate(data) if t["slug"] == slug)
topic = data[idx]

old_keys = {s["sectionKey"] for s in topic["sections"]}
print("existing sectionKeys:", sorted(old_keys))

# fill the five outlined sections in place, keep id/number/title/blurb/estMinutes
for s_new in sections:
    if s_new["number"] == "10.0":
        continue
    match = next(s for s in topic["sections"] if s["number"] == s_new["number"])
    for k, v in s_new.items():
        match[k] = v

# insert the 10.0 Specification Map at the front
topic["sections"].insert(0, sections[0])

# housekeeping: estHours stays author-set; cards untouched
data[idx] = topic

with open(CONTENT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print(f"OK — topic 10 now has {len(topic['sections'])} sections:")
for s in topic["sections"]:
    n_blocks = len(s["content"] or [])
    print(f"  {s['number']}  {s['title']:<45} blocks: {n_blocks}")
