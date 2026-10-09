#!/usr/bin/env python3
"""Splice the Topic 6 energetics notes entry into prisma/seed-data/notes.ts.

Inserts scripts/t6/notes_block_a.txt + notes_block_b.txt just before the
closing '}' of the NOTES export (after the organic-intro-and-alkanes entry).
"""
from pathlib import Path

ROOT = Path('/home/z/my-project')
notes = ROOT / 'prisma/seed-data/notes.ts'
a = (ROOT / 'scripts/t6/notes_block_a.txt').read_text()
b = (ROOT / 'scripts/t6/notes_block_b.txt').read_text()

text = notes.read_text()
tail = text.rstrip()
assert tail.endswith('}'), 'unexpected tail'
# the file ends with "  },\n}" — insert before the final closing brace
assert tail.endswith('\n  },\n}') or tail.endswith('},\n}'), tail[-40:]

idx = tail.rfind('\n}')
out = tail[:idx] + '\n' + a + b + tail[idx:] + '\n'
notes.write_text(out)
print('spliced notes.ts; new line count:', out.count('\n') + 1)
