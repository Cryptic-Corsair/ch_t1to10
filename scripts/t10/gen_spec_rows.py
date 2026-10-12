#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the Topic 10 specification-map table rows.

Reads the verbatim specText/outline of the current sections in content.json
(validated against the official specification earlier) and writes
scripts/t10/specmap_rows.json. Persisted so rebuilds never depend on /tmp.
"""
import json
import os
import re
import sys

ROOT = "/home/z/my-project"
CONTENT = os.path.join(ROOT, "src/lib/site/content.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specmap_rows.json")

data = json.load(open(CONTENT, encoding="utf-8"))
t10 = next(t for t in data if t["slug"] == "halogenoalkanes-alcohols-spectra")

rows = []
for s in sorted(t10["sections"], key=lambda x: float(x["number"].replace("10.", "") or 0)):
    n = s["number"]
    if n == "10.0":
        continue
    text = s.get("specText") or ""
    outline = s.get("outline") or []

    cp = re.match(r"CORE PRACTICAL (\d+)\s*\n\s*(.*)", text, re.S)
    if cp:
        lines = [f"CORE PRACTICAL {cp.group(1)} — {cp.group(2).strip()}"]
    else:
        lines = [re.sub(r"\s+", " ", text).strip()]
    for o in outline:
        lines.append(re.sub(r"^(i{1,3}|iv|v|•)\s{2,}", r"\1   ", o.replace("\n", " ").strip()))
    rows.append([n, "\n".join(lines)])

json.dump({"rows": rows}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK — wrote {len(rows)} rows to {OUT}")
for r in rows:
    print(" ", r[0], "|", r[1].split("\n")[0][:80])
