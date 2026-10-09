#!/usr/bin/env python3
"""Composite the Topic 6 PNGs onto light/dark canvases for visual QA."""
from pathlib import Path
from PIL import Image

ROOT = Path('/home/z/my-project')
DIA = ROOT / 'public/diagrams'
QA = ROOT / 'scripts/t6/qa'
QA.mkdir(parents=True, exist_ok=True)

BG = {'light': '#f7f6f3', 'dark': '#16181d'}
NAMES = ['enthalpy-level-diagrams', 'reaction-profiles', 'cooling-curve',
         'calorimetry-solution', 'calorimetry-combustion',
         'hess-cycle-combustion', 'hess-cycle-formation',
         'bond-dissociation-ch4', 'bond-enthalpy-cycle']

for variant in ('light', 'dark'):
    for name in NAMES:
        f = DIA / (name + ('-dark' if variant == 'dark' else '') + '.png')
        img = Image.open(f).convert('RGBA')
        bg = Image.new('RGBA', img.size, BG[variant])
        bg.alpha_composite(img)
        bg.convert('RGB').save(QA / (name + ('-dark' if variant == 'dark' else '') + '.jpg'),
                               quality=88)
print('composited', len(NAMES) * 2, 'QA images')
