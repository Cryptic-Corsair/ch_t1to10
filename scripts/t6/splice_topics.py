#!/usr/bin/env python3
"""Splice the new Topic 6 energetics block into prisma/seed-data/topics.ts.

Replaces lines 839-899 (the old 5-section placeholder entry) with the new
12-section gold-standard entry from scripts/t6/topics_block.txt.
"""
from pathlib import Path

ROOT = Path('/home/z/my-project')
topics = ROOT / 'prisma/seed-data/topics.ts'
block = ROOT / 'scripts/t6/topics_block.txt'

lines = topics.read_text().splitlines(keepends=True)
new_block = block.read_text()

# sanity anchors
assert "slug: 'energetics'" in lines[840], lines[840]
assert "slug: 'intermolecular-forces'" in lines[901], lines[901]

# lines[838] is line 839 ('  {') ... lines[898] is line 899 ('  },')
out = lines[:838] + [new_block] + lines[899:]
topics.write_text(''.join(out))
print('spliced. new length lines:', len(''.join(out).splitlines()))
