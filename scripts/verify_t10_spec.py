#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify topic 10 rebuilt sections against the official spec text."""
import json
import re
import sys

ROOT = "/home/z/my-project"
spec = open(f"{ROOT}/scripts/spec.txt", encoding="utf-8").read()
data = json.load(open(f"{ROOT}/src/lib/site/content.json", encoding="utf-8"))
t10 = next(t for t in data if t["slug"] == "halogenoalkanes-alcohols-spectra")

# extract raw statements 10.1-10.23 from spec.txt
txt = spec[spec.find("Topic 10"):spec.find("Unit 3: Practical Skills", spec.find("Topic 10"))]
norm = lambda s: re.sub(r"\s+", " ", s).strip().replace("\u2019", "'").replace("\u2018", "'").replace("-", "\u2013")  # spec has one hyphen typo (N-H); app uses en-dash consistently
statements = {}
cur = None
for line in txt.split("\n"):
    m = re.match(r"\s*(10\.\d+)\s+(.*)", line)
    if m:
        cur = m.group(1)
        statements[cur] = m.group(2).strip()
    elif cur and line.strip():
        statements[cur] += " " + line.strip()

fails = 0
for s in t10["sections"]:
    if s["number"] == "10.0":
        continue
    want = norm(statements[s["spec"]])
    # section specText: stem only if outline carries sub-parts; otherwise full statement
    got = norm(s["specText"])
    # CORE PRACTICAL sections store "CORE PRACTICAL N\n<desc>"
    cp = re.match(r"CORE PRACTICAL (\d+)\s+(.*)", got)
    if cp:
        want = norm(f"CORE PRACTICAL {cp.group(1)} {statements[s['spec']].split(maxsplit=2)[2] if False else ''}")  # handled below
        raw = statements[s["spec"]]
        want = norm(re.sub(r"^\s*10\.\d+\s*", "", raw))
        got2 = norm(got.replace("\n", " "))
        if got2 not in want and want not in got2:
            fails += 1
            print(f"MISMATCH {s['number']}: CP")
            print("  spec :", want[:120])
            print("  sect :", got2[:120])
        continue
    # stem-only convention: section specText should be a prefix of the statement
    if not want.startswith(got):
        fails += 1
        print(f"MISMATCH {s['number']}:")
        print("  spec :", want[:110])
        print("  sect :", got[:110])

# outline items for multi-part sections should match statement remainder
for s in t10["sections"]:
    if s["outline"] and s["number"] != "10.0":
        want_full = norm(statements[s["spec"]])
        stem = norm(s["specText"])
        subparts = norm(" ".join(s["outline"]))
        tail = want_full[len(stem):].strip() if want_full.startswith(stem) else ""
        # allow the roman numerals to be reformatted with wider spacing
        t2 = re.sub(r"\s+", " ", tail)
        t3 = re.sub(r"\s+", " ", subparts)
        if t3 and t2 and (t3 not in t2 and t2 not in t3):
            fails += 1
            print(f"OUTLINE MISMATCH {s['number']}:")
            print("  spec tail :", t2[:130])
            print("  outline   :", t3[:130])

print("sections checked:", len(t10["sections"]) - 1, "| fails:", fails)
sys.exit(1 if fails else 0)
