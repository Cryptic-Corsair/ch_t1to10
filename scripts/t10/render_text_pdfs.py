#!/usr/bin/env python3
"""Render Alcohols and Halogenoalkane PDF pages to PNG for diagram reference."""
import fitz, os

for key, fname in [("alcohols", "Alcohols.pdf"), ("halo", "Halogenoalkane.pdf")]:
    doc = fitz.open(f"/home/z/my-project/upload/{fname}")
    outdir = f"/home/z/my-project/scripts/t10/{key}_pages"
    os.makedirs(outdir, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=110)
        pix.save(os.path.join(outdir, f"{key}_p{i+1:02d}.png"))
    print(key, len(doc), "pages rendered")
    doc.close()
