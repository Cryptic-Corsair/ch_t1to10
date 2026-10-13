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

# ---------- flashcards: append alcohol cards (11-14) if missing ----------
NEW_CARDS = [
    (11, "CORE", "Name the reagent and condition to make a chloroalkane, a bromoalkane and an iodoalkane from an alcohol.",
     "Chloro: PCl₅, room temperature (tertiary alcohols: concentrated HCl, shake to mix). Bromo: KBr + 50% concentrated H₂SO₄, heat under reflux. Iodo: iodine + moist red phosphorus, warm. All substitution."),
    (12, "TRAP", "Why must the H₂SO₄ be 50% — not 100% concentrated — when making HBr from KBr?",
     "100% concentrated sulfuric acid oxidises bromide ions to bromine, so no hydrogen bromide is produced for the reaction."),
    (13, "CORE", "Why do alcohols have much higher boiling temperatures than alkanes of comparable relative molecular mass?",
     "Alcohols form hydrogen bonding between molecules; alkanes only have weak London forces and haloalkanes dipole–dipole forces. Hydrogen bonding is stronger, so it requires more energy to break the bonds."),
    (14, "EXAM", "Put the purification techniques for a liquid organic product in order.",
     "Heating under reflux (the reaction) → distillation (collect the distillate at the product's approximate boiling point range) → solvent extraction with a separating funnel → drying with an anhydrous salt → boiling temperature determination against the data booklet values."),
    (15, "DEFINITION", "What is the base peak of a mass spectrum?",
     "The most abundant fragment ion — each fragment ion's abundance is quoted as a percentage of it, and by convention the base peak has a relative abundance of 100%. Only the fragments with the positive charge are detected; the neutral radical is lost."),
    (16, "EXAM", "The mass spectrum shows molecular ion peaks two m/z units apart. What does that tell you?",
     "A halogen with two isotopes is present. One Br atom (⁷⁹Br, ⁸¹Br equal): M and M+2 in 1:1; two Br atoms: M, M+2, M+4 in 1:2:1. One Cl atom (³⁵Cl : ³⁷Cl = 3:1): M and M+2 in 3:1; two Cl atoms: 9:6:1. Iodoalkanes give a single molecular ion peak — iodine has only one stable isotope."),
]
existing_fronts = {c["front"] for c in topic.get("cards", [])}
other_card_ids = {c["id"] for t in data if t["slug"] != slug for c in t.get("cards", [])}
for ordn, tag, front, back in NEW_CARDS:
    cid = f"cmv1eoi8l00gt10card{ordn:02d}"
    if cid in other_card_ids:
        print("CARD ID CLASH:", cid)
        sys.exit(1)
    if front not in existing_fronts:
        topic.setdefault("cards", []).append({"id": cid, "ord": ordn, "front": front, "back": back, "tag": tag})
        existing_fronts.add(front)

# align the M/M+1 card with the source notes wording (carbon-13 ≈ 1%, n% rule)
for c in topic.get("cards", []):
    if c["id"] == "cmv1eoi8p00gpjfqk48446fqe":
        c["back"] = ("M⁺• (molecular ion) m/z = molecular mass of the molecule. "
                     "M+1 comes from carbon-13 (about 1% of naturally occurring carbon-12): "
                     "height of M+1 = (number of C atoms ÷ 100) × height of the M peak.")
        print("card 8 back updated to notes wording")

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
