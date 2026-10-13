#!/usr/bin/env python3
"""Composite the new t10 IR plates onto white for visual QA."""
from PIL import Image
from pathlib import Path

OUT = Path('/home/z/my-project/public/diagrams')
QA = Path('/home/z/my-project/scripts/t10/qa')
QA.mkdir(parents=True, exist_ok=True)

for name in ['t10-ir-spectrum', 't10-ir-vibrations', 't10-ir-examples',
             't10-ir-halides-amines', 't10-ir-q1']:
    src = OUT / (name + '.png')
    img = Image.open(src).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    bg.convert('RGB').save(QA / (name + '-white.png'))
    print('composited', name)
