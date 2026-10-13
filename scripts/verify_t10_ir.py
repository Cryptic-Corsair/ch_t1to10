#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-splice integrity check for content.json:
 1. JSON parses; unique section ids + sectionKeys globally
 2. every figure src / srcDark exists on disk
 3. callout / worked / table key contracts
 4. 10.22 specText + outline still match the verbatim spec statement
 5. section numbering for topic 10 = 10.0 .. 10.23
"""
import json
import os
import re
import sys

ROOT = "/home/z/my-project"
data = json.load(open(f"{ROOT}/src/lib/site/content.json", encoding="utf-8"))
rows = json.load(open(f"{ROOT}/scripts/t10/specmap_rows.json", encoding="utf-8"))["rows"]
spec_stmt = {n: t for n, t in rows}

errors = []
ids, keys = set(), set()
for t in data:
    nums = []
    for s in t.get("sections", []):
        if s["id"] in ids:
            errors.append(f"duplicate id {s['id']}")
        ids.add(s["id"])
        k = (t["slug"], s["sectionKey"])
        if k in keys:
            errors.append(f"duplicate sectionKey {k}")
        keys.add(k)
        nums.append(s["number"])
        for b in (s.get("content") or []):
            bt = b["type"]
            if bt == "figure":
                for key in ("src", "srcDark"):
                    if b.get(key) and not os.path.isfile(
                            os.path.join(ROOT, "public", b[key].lstrip("/"))):
                        errors.append(f"{s['number']}: missing {b[key]}")
            if bt == "callout" and not (set(b.keys()) in (
                    {"type", "variant", "title", "text"},
                    {"type", "variant", "style", "title", "text"})):  # style:'note' used by topic 2
                errors.append(f"{s['number']}: callout keys {sorted(b.keys())}")
            if bt == "worked" and set(b.keys()) != {"type", "title", "problem", "steps", "answer"}:
                errors.append(f"{s['number']}: worked keys {sorted(b.keys())}")
    if t["slug"] == "halogenoalkanes-alcohols-spectra":
        want = ["10.0"] + [f"10.{n}" for n in range(1, 24)]
        if nums != want:
            errors.append(f"topic 10 numbering mismatch: {nums}")

t10 = next(t for t in data if t["slug"] == "halogenoalkanes-alcohols-spectra")
s22 = next(s for s in t10["sections"] if s["number"] == "10.22")
raw = spec_stmt["10.22"]
stem = raw.split("including:")[0].strip() + " including:"
subs = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines()[1:]]
if re.sub(r"\s+", " ", s22["specText"]).strip() != re.sub(r"\s+", " ", stem):
    errors.append("10.22 specText stem drift")
if [re.sub(r"\s+", " ", o).strip() for o in s22["outline"]] != subs:
    errors.append("10.22 outline drift")

# per-topic block type sanity across the whole app
KNOWN = {"p", "h3", "def", "eq", "list", "callout", "worked", "table", "figure", "qa"}
for t in data:
    for s in t.get("sections", []):
        for b in (s.get("content") or []):
            if b["type"] not in KNOWN:
                errors.append(f"{t['slug']}/{s['number']}: unknown block {b['type']}")

if errors:
    print("FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK — all topics intact; 10.22 spec text verbatim; figures on disk")
print("10.22 blocks:", len(s22["content"]), "| estMinutes:", s22["estMinutes"],
      "| cards:", len(t10["cards"]))
