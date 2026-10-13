"""Extract complete text (page by page) from all four Topic 10 source PDFs."""
import fitz, os

SRC = "/home/z/my-project/upload"
OUT = "/home/z/my-project/scripts/t10"
files = {
    "halogenoalkane": "Halogenoalkane.pdf",
    "alcohols": "Alcohols.pdf",
    "mass_spectra": "Mass spectra with ans.pdf",
    "infrared": "Infrared with ans.pdf",
}

for key, fname in files.items():
    doc = fitz.open(os.path.join(SRC, fname))
    out_path = os.path.join(OUT, f"source_{key}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc):
            f.write(f"\n===== PAGE {i+1} =====\n")
            f.write(page.get_text("text"))
    print(f"{fname}: {len(doc)} pages -> {out_path} ({os.path.getsize(out_path)} bytes)")
    doc.close()
