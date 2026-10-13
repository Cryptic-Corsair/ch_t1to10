#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Splice the rebuilt section 10.22 (Infrared Spectroscopy, from the final
source part 'Infrared with ans.pdf') into content.json, add the IR flashcards
and re-derive estHours. Full validation before writing."""
import json
import os
import shutil
import sys

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
PUBLIC = os.path.join(ROOT, "public")

sys.path.insert(0, os.path.join(ROOT, "scripts/t10"))
from sections_ir import S1022, NEW_CARDS  # noqa: E402

ALLOWED = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure"}
FORBIDDEN = {"qa"}

errors = []
for b in S1022["content"]:
    if b["type"] in FORBIDDEN:
        errors.append("forbidden block type %s" % b["type"])
    if b["type"] not in ALLOWED:
        errors.append("bad block type %s" % b["type"])
    if b["type"] == "figure":
        for key in ("src", "srcDark"):
            if key in b and not os.path.isfile(os.path.join(PUBLIC, b[key].lstrip("/"))):
                errors.append("missing figure file %s" % b[key])
    if b["type"] == "callout":
        if b.get("variant") not in {"tip", "warning", "exam", "key"}:
            errors.append("bad callout variant %s" % b.get("variant"))
        if set(b.keys()) != {"type", "variant", "title", "text"}:
            errors.append("callout keys off-spec: %s" % sorted(b.keys()))
    if b["type"] == "worked":
        if set(b.keys()) != {"type", "title", "problem", "steps", "answer"}:
            errors.append("worked keys off-spec: %s" % sorted(b.keys()))
    if b["type"] == "table":
        if not b.get("headers") or not b.get("rows"):
            errors.append("table missing headers/rows")

# mark-scheme / source keywords that must survive the rebuild
joined = json.dumps(S1022, ensure_ascii=False)
for kw in ["stretching", "bending", "transmittance", "wavenumber", "reciprocal of wavelength",
           "functional group", "fingerprint region", "1500 cm⁻¹ to 400 cm⁻¹",
           "databases", "additional peaks", "1000 – 1300", "1680 – 1750", "2500 – 3300",
           "3230 – 3550", "nucleophilic substitution", "Fehling", "sodium dichromate(VI)",
           "C–H wag", "C–Cl", "C–Br", "N–H stretch", "butan-1-amine", "propan-1-ol",
           "butan-2-one", "CH₂OH⁺", "enhanced greenhouse effect"]:
    if kw not in joined:
        errors.append("keyword missing: %s" % kw)

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

with open(CONTENT, "r", encoding="utf-8") as f:
    data = json.load(f)

slug = "halogenoalkanes-alcohols-spectra"
topic = next(t for t in data if t["slug"] == slug)

# section id must stay the one already registered; number unique
idx = next(i for i, s in enumerate(topic["sections"]) if s["number"] == "10.22")
old = topic["sections"][idx]
print("replacing:", old["number"], old["title"], "(%d blocks)" % len(old["content"]))
if old["id"] != S1022["id"]:
    print("  note: id changes %s -> %s" % (old["id"], S1022["id"]))

# no id clash elsewhere
others = {s["id"] for t in data if t["slug"] != slug for s in t.get("sections", [])}
if S1022["id"] in others:
    print("SECTION ID CLASH")
    sys.exit(1)

topic["sections"][idx] = S1022

# ---- flashcards: append the IR cards if missing ----
other_card_ids = {c["id"] for t in data if t["slug"] != slug for c in t.get("cards", [])}
existing_fronts = {c["front"] for c in topic.get("cards", [])}
for ordn, tag, front, back in NEW_CARDS:
    cid = "cmv1eoi8l00gt10card%02d" % ordn
    if cid in other_card_ids:
        print("CARD ID CLASH:", cid)
        sys.exit(1)
    if front not in existing_fronts:
        topic.setdefault("cards", []).append(
            {"id": cid, "ord": ordn, "front": front, "back": back, "tag": tag})
        existing_fronts.add(front)
        print("card added:", ordn, tag, front[:60])

# ---- estHours follows the per-section estimates ----
total_min = sum(s["estMinutes"] for s in topic["sections"])
topic["estHours"] = round(total_min / 60, 1)

shutil.copyfile(CONTENT, CONTENT + ".bak2")
with open(CONTENT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

s = S1022
print("OK — 10.22 rebuilt: %d blocks, est %d min; topic estHours=%s, cards=%d"
      % (len(s["content"]), s["estMinutes"], topic["estHours"], len(topic["cards"])))
types = {}
for b in s["content"]:
    types[b["type"]] = types.get(b["type"], 0) + 1
print("block mix:", dict(sorted(types.items())))
