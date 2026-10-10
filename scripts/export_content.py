#!/usr/bin/env python3
"""Export the authoring database (db/custom.db) into src/lib/site/content.json.

The site reads its topic corpus from this JSON (bundled into the JS build),
which removes the runtime filesystem/database dependency entirely — required
for serverless platforms like Vercel where SQLite cannot persist.

The mapping replicates src/lib/site/load.ts exactly:
  - topics ordered by number ASC
  - sections ordered by number ASC (string), then natural-sorted on "1.2"/"1.10"
  - outline: JSON string -> string[] (safe parse -> [])
  - content: JSON string -> Block[] (safe parse -> null)
  - flashcards ordered by ord ASC

Re-run after ANY content change to the DB, then commit the refreshed JSON:
    python3 scripts/export_content.py
"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db", "custom.db")
OUT = os.path.join(ROOT, "src", "lib", "site", "content.json")


def natural_key(number: str):
    """Replicates load.ts: am - bm || (ai || 0) - (bi || 0)."""
    main, _, rest = number.partition(".")
    return (int(main), int(rest) if rest else 0)


def safe_parse(text, fallback):
    if text is None:
        return fallback
    try:
        return json.loads(text)
    except Exception:
        return fallback


def main() -> int:
    if not os.path.exists(DB):
        print(f"ERROR: authoring DB not found at {DB}", file=sys.stderr)
        return 1

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    topics = con.execute(
        "SELECT slug, number, unit, unitCode, unitName, title, subtitle, summary, estHours "
        "FROM topics ORDER BY number ASC"
    ).fetchall()

    out = []
    for t in topics:
        slug = t["slug"]
        sections = con.execute(
            "SELECT id, sectionKey, number, title, blurb, estMinutes, spec, specText, outline, content "
            "FROM sections WHERE topicSlug = ? ORDER BY number ASC",
            (slug,),
        ).fetchall()
        cards = con.execute(
            "SELECT id, ord, front, back, tag FROM flashcards WHERE topicSlug = ? ORDER BY ord ASC",
            (slug,),
        ).fetchall()

        mapped_sections = sorted(
            (
                {
                    "id": s["id"],
                    "sectionKey": s["sectionKey"],
                    "number": s["number"],
                    "title": s["title"],
                    "blurb": s["blurb"],
                    "estMinutes": s["estMinutes"],
                    "spec": s["spec"],
                    "specText": s["specText"],
                    "outline": safe_parse(s["outline"], []) or [],
                    "content": safe_parse(s["content"], None),
                }
                for s in sections
            ),
            key=lambda s: natural_key(s["number"]),
        )

        out.append(
            {
                "slug": t["slug"],
                "number": t["number"],
                "unit": t["unit"],
                "unitCode": t["unitCode"],
                "unitName": t["unitName"],
                "title": t["title"],
                "subtitle": t["subtitle"],
                "summary": t["summary"],
                "estHours": t["estHours"],
                "sections": mapped_sections,
                "cards": [
                    {
                        "id": c["id"],
                        "ord": c["ord"],
                        "front": c["front"],
                        "back": c["back"],
                        "tag": c["tag"],
                    }
                    for c in cards
                ],
            }
        )

    con.close()

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Exported {len(out)} topics -> {os.path.relpath(OUT, ROOT)}")
    total_sections = total_cards = total_content = 0
    for t in out:
        n_content = sum(1 for s in t["sections"] if s["content"])
        total_sections += len(t["sections"])
        total_cards += len(t["cards"])
        total_content += n_content
        print(
            f"  T{t['number']:>2} {t['slug']:<34} sections={len(t['sections']):>3} "
            f"(with content={n_content:>3})  cards={len(t['cards']):>3}"
        )
    print(
        f"TOTAL: {total_sections} sections ({total_content} with content), "
        f"{total_cards} flashcards, file size {os.path.getsize(OUT) // 1024} KB"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
