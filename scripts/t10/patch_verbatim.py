#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verbatim wording touch-ups found by verify_t10_full.py."""
import json
import sys

CONTENT = "/home/z/my-project/src/lib/site/content.json"
data = json.load(open(CONTENT, encoding="utf-8"))
topic = next(t for t in data if t["slug"] == "halogenoalkanes-alcohols-spectra")


def sec(num):
    return next(s for s in topic["sections"] if s["number"] == num)


fixes = []

# 1. 10.8 reflux intro — exact source sentence
s8 = sec("10.8")
for b in s8["content"]:
    if b["type"] == "p" and "condensing the vapour back into the flask" in b.get("text", ""):
        b["text"] = b["text"].replace(
            "boiling the mixture and condensing the vapour back into the flask continuously",
            "boiling the reaction mixture and condensing the vapour produced back into "
            "the flask continuously")
        fixes.append("10.8 reflux wording")

# 2. 10.10 precipitate table — verbatim observation wording
s10 = sec("10.10")
for b in s10["content"]:
    if b["type"] == "table":
        for r in b["rows"]:
            cells = [c for c in r if isinstance(c, str)]
            if any("AgCl" in c for c in cells):
                r[0] = "**White ppt (AgCl)**"
                r[1] = "white"
                r[2] = "chloroalkane"
            elif any("AgBr" in c for c in cells):
                r[0] = "**Cream ppt (AgBr)**"
                r[1] = "cream"
                r[2] = "bromoalkane"
            elif any("AgI" in c for c in cells):
                r[0] = "**Yellow ppt (AgI)**"
                r[1] = "yellow"
                r[2] = "iodoalkane"
        fixes.append("10.10 precipitate table")

# 3. 10.11 loosely corked
s11 = sec("10.11")
for b in s11["content"]:
    if b["type"] == "list":
        b["items"] = [it.replace("**Shake, loosely cork**, and observe",
                                 "**Each test tube is shaken, loosely corked** and observed")
                      for it in b["items"]]
        fixes.append("10.11 loosely corked")

# 4. 10.19 settle into two layers (contiguous)
s19 = sec("10.19")
for b in s19["content"]:
    if b["type"] == "list":
        b["items"] = [it.replace("**Allow the contents to settle** into two layers.",
                                 "Allow the contents to **settle into two layers**.")
                      for it in b["items"]]
        fixes.append("10.19 settle")

# 5. 10.21 sufficient to break (contiguous)
s21 = sec("10.21")
for b in s21["content"]:
    if b["type"] == "p" and "break some of the covalent bonds" in b.get("text", ""):
        b["text"] = b["text"].replace(
            "sufficient to **break some of the covalent bonds** in it",
            "**sufficient to break some of the covalent bonds** in it")
        fixes.append("10.21 sufficient-to-break")

with open(CONTENT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("applied:", fixes)
