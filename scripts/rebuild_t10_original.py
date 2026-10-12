#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild Topic 10 to match the ORIGINAL topic versions (1–9).

Replaces the five grouped digest-style sections with 24 sections that follow
the house pattern used by every original topic:
  - 10.0 Specification Map (p + verbatim statement table)
  - 10.1 – 10.23: one section per specification statement, numbered to match

Style contract (from topics 1–9):
  - block types: p, h3, def, eq, list, table, figure, worked, callout  (NO qa)
  - callouts: {type, variant, title, text} — no extra keys, used sparingly
  - direct, factual h3 headings; bolded mark-scheme keywords
"""
import json
import os
import shutil
import sys

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t10.sections_o1 import SECTIONS_O1  # noqa: E402
from t10.sections_o2 import SECTIONS_O2  # noqa: E402
from t10.sections_o3 import SECTIONS_O3  # noqa: E402

sections = SECTIONS_O1 + SECTIONS_O2 + SECTIONS_O3

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure"}
FORBIDDEN = {"qa"}

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
        if b["type"] in FORBIDDEN:
            errors.append(f"{s['number']}: forbidden block type {b['type']}")
        if b["type"] not in ALLOWED:
            errors.append(f"{s['number']}: bad block type {b['type']}")
        if b["type"] == "figure":
            if not os.path.isfile(os.path.join(PUBLIC, b["src"].lstrip("/"))):
                errors.append(f"{s['number']}: missing figure file {b['src']}")
            if b.get("srcDark") and not os.path.isfile(os.path.join(PUBLIC, b["srcDark"].lstrip("/"))):
                errors.append(f"{s['number']}: missing dark figure {b['srcDark']}")
        if b["type"] == "callout":
            if b.get("variant") not in {"tip", "warning", "exam", "key"}:
                errors.append(f"{s['number']}: bad callout variant {b.get('variant')}")
            if set(b.keys()) != {"type", "variant", "title", "text"}:
                errors.append(f"{s['number']}: callout keys off-spec: {sorted(b.keys())}")

# spec coverage: every statement 10.1 – 10.23 must own exactly one section
numbers = [s["number"] for s in sections]
expected = ["10.0"] + [f"10.{n}" for n in range(1, 24)]
if numbers != expected:
    errors.append(f"section numbering mismatch:\n  got {numbers}")

# mark-scheme keyword spot-checks (vocabulary must survive the rebuild)
joined = json.dumps(sections, ensure_ascii=False)
for kw in ["electron-pair donor", "nucleophilic substitution", "bond enthalpy",
           "distil", "reflux", "Benedict's or Fehling's", "sodium carbonate",
           "molecular ion", "fragmentation", "fingerprint", "wavenumber",
           "nucleophile", "elimination", "hydrolysis", "heating under reflux",
           "separating funnel", "anhydrous salt", "boiling temperature",
           "heterolytic fission", "electrophile", "polymerisation",
           "nitrile", "carbocation", "halogenating agents",
           "potassium dichromate(VI)", "increasing the length of the carbon chain",
           "electron-pair acceptor", "sealed tube", "qualitative test for the –OH group"]:
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

shutil.copyfile(CONTENT, CONTENT + ".bak2")

slug = "halogenoalkanes-alcohols-spectra"
idx = next(i for i, t in enumerate(data) if t["slug"] == slug)
topic = data[idx]

# every new id must be globally unique too (excluding the topic being replaced)
all_ids = {s["id"] for t in data if t["slug"] != slug for s in t.get("sections", [])}
clash = seen_ids & all_ids
if clash:
    print("ID CLASH with existing sections:", clash)
    sys.exit(1)

old_titles = [s["title"] for s in topic["sections"]]
print("replacing sections:", old_titles)

topic["sections"] = sections

# estHours follows the per-section estimates, as in the original topics
total_min = sum(s["estMinutes"] for s in sections)
topic["estHours"] = round(total_min / 60, 1)

data[idx] = topic
with open(CONTENT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print(f"OK — topic 10 rebuilt with {len(topic['sections'])} sections, estHours={topic['estHours']}:")
for s in topic["sections"]:
    n_blocks = len(s["content"] or [])
    print(f"  {s['number']:>5}  {s['title'][:60]:<62} blocks: {n_blocks}  est: {s['estMinutes']}min")
