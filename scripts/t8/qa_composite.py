#!/usr/bin/env python3
"""Composite the Topic 8 PNGs onto light/dark canvases for visual QA, in montage sheets."""
from pathlib import Path
from PIL import Image

ROOT = Path('/home/z/my-project')
DIA = ROOT / 'public/diagrams'
QA = ROOT / 'scripts/t8/qa'
QA.mkdir(parents=True, exist_ok=True)

BG = {'light': '#f7f6f3', 'dark': '#16181d'}
NAMES = ['redox-electron-transfer', 'redox-agents-map', 'redox-disproportionation',
         'group12-trends', 'group2-solubility', 'thermal-stability', 'flame-origins',
         'titration-setup', 'displacement-grid', 'halide-power-ladder']

# singles for detailed inspection
for variant in ('light', 'dark'):
    for name in NAMES:
        f = DIA / (name + ('-dark' if variant == 'dark' else '') + '.png')
        img = Image.open(f).convert('RGBA')
        bg = Image.new('RGBA', img.size, BG[variant])
        bg.alpha_composite(img)
        bg.convert('RGB').save(QA / (name + ('-dark' if variant == 'dark' else '') + '.jpg'),
                               quality=88)

# montage sheets: light pairs stacked, to inspect quickly
def sheet(names, out, variant):
    imgs = []
    for n in names:
        img = Image.open(DIA / (n + ('-dark' if variant == 'dark' else '') + '.png')).convert('RGBA')
        bg = Image.new('RGBA', img.size, BG[variant])
        bg.alpha_composite(img)
        imgs.append(bg.convert('RGB'))
    w = max(i.width for i in imgs)
    scale = 1200 / w
    imgs = [i.resize((int(i.width * scale), int(i.height * scale))) for i in imgs]
    H = sum(i.height for i in imgs) + 20 * (len(imgs) - 1)
    canvas = Image.new('RGB', (1200, H), BG[variant])
    y = 0
    for i in imgs:
        canvas.paste(i, (0, y))
        y += i.height + 20
    canvas.save(QA / out, quality=85)

for variant in ('light', 'dark'):
    sheet(NAMES[:5], 'sheet-a-%s.jpg' % variant, variant)
    sheet(NAMES[5:], 'sheet-b-%s.jpg' % variant, variant)
print('composited singles + 4 sheets')
