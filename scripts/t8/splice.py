#!/usr/bin/env python3
"""Splice the Topic 8 redox-and-groups block into topics.ts and notes.ts."""
from pathlib import Path

ROOT = Path('/home/z/my-project')

# ---- topics.ts: replace the whole Topic 8 object --------------------------------
topics = ROOT / 'prisma/seed-data/topics.ts'
lines = topics.read_text().splitlines(keepends=True)

slug_idx = next(i for i, l in enumerate(lines) if "slug: 'redox-and-groups'" in l)
assert lines[slug_idx - 2].strip() == '{', lines[slug_idx - 2]
start = slug_idx - 2

next_idx = next(i for i, l in enumerate(lines) if "slug: 'kinetics-and-equilibria'" in l)
end = next_idx - 3
assert lines[end].strip() == '},', lines[end]
assert lines[end + 1].strip() == '{', lines[end + 1]

new_block = (ROOT / 'scripts/t8/topics_block.txt').read_text()
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
parts = [(ROOT / ('scripts/t8/notes_%s.txt' % n)).read_text() for n in ('a', 'b', 'c', 'd', 'e')]
combined = ''.join(parts)
idx = tail.rfind('\n}')
notes.write_text(tail[:idx] + '\n' + combined + tail[idx:] + '\n')
print('notes.ts spliced: new line count', (tail[:idx] + '\n' + combined + tail[idx:] + '\n').count('\n') + 1)
