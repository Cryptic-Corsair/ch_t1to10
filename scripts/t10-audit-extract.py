#!/usr/bin/env python3
"""Extract text from Topic 10 source PDFs for verbatim audit."""
import fitz, json, re, os

UP = '/home/z/my-project/upload'
OUT = '/home/z/my-project/scripts/t10-sources'
os.makedirs(OUT, exist_ok=True)

sources = ['Halogenoalkane.pdf', 'Alcohols.pdf', 'Mass spectra with ans.pdf', 'Infrared with ans.pdf']

for name in sources:
    doc = fitz.open(os.path.join(UP, name))
    pages = []
    for i, page in enumerate(doc):
        txt = page.get_text('text')
        n_imgs = len(page.get_images(full=True))
        pages.append({'page': i + 1, 'text': txt, 'images': n_imgs})
    out_name = name.replace('.pdf', '.json')
    with open(os.path.join(OUT, out_name), 'w') as f:
        json.dump({'file': name, 'pages_total': len(doc), 'pages': pages}, f, indent=1)
    total_imgs = sum(p['images'] for p in pages)
    total_chars = sum(len(p['text']) for p in pages)
    print(f"{name}: {len(doc)} pages, {total_imgs} images, {total_chars} chars")
    doc.close()
