#!/usr/bin/env python3
"""Extract text from the Infrared source PDF, page by page."""
import fitz

doc = fitz.open("/home/z/my-project/upload/Infrared with ans.pdf")
for i, page in enumerate(doc):
    text = page.get_text("text")
    print(f"========== PAGE {i+1} ==========")
    print(text)
