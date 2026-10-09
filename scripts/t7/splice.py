#!/usr/bin/env python3
"""Splice the Topic 7 intermolecular-forces block into topics.ts and notes.ts."""
from pathlib import Path

ROOT = Path('/home/z/my-project')

# ---- topics.ts: replace the whole Topic 7 object --------------------------------
topics = ROOT / 'prisma/seed-data/topics.ts'
lines = topics.read_text().splitlines(keepends=True)

slug_idx = next(i for i, l in enumerate(lines) if "slug: 'intermolecular-forces'" in l)
assert lines[slug_idx - 2].strip() == '{', lines[slug_idx - 2]
start = slug_idx - 2

redox_idx = next(i for i, l in enumerate(lines) if "slug: 'redox-and-groups'" in l)
end = redox_idx - 3
assert lines[end].strip() == '},', lines[end]
assert lines[end + 1].strip() == '{', lines[end + 1]

new_block = (ROOT / 'scripts/t7/topics_block.txt').read_text()
if not new_block.endswith('\n'):
    new_block += '\n'
out = lines[:start] + [new_block] + lines[end + 1:]
topics.write_text(''.join(out))
print('topics.ts spliced: replaced lines', start + 1, 'to', end + 1, '-> new total', len(''.join(out).splitlines()))

# ---- notes.ts: insert the notes entry before the final closing brace ------------
notes = ROOT / 'prisma/seed-data/notes.ts'
text = notes.read_text()
tail = text.rstrip()
assert tail.endswith('}'), 'unexpected tail'
a = (ROOT / 'scripts/t7/notes_block_a.txt').read_text()
b = (ROOT / 'scripts/t7/notes_block_b.txt').read_text()
idx = tail.rfind('\n}')
notes.write_text(tail[:idx] + '\n' + a + b + tail[idx:] + '\n')
print('notes.ts spliced: new line count', (tail[:idx] + '\n' + a + b + tail[idx:] + '\n').count('\n') + 1)
