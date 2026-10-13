#!/usr/bin/env python3
"""Render Infrared PDF pages to PNG images for visual reading."""
import fitz
import os

doc = fitz.open("/home/z/my-project/upload/Infrared with ans.pdf")
outdir = "/home/z/my-project/scripts/t10/ir_pages"
os.makedirs(outdir, exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=140)
    path = os.path.join(outdir, f"ir_p{i+1:02d}.png")
    pix.save(path)
    print(path, pix.width, "x", pix.height)
