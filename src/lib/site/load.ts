// Server-side topic loader — shared by the SPA page, the print route and the PDF API.
//
// Content source: src/lib/site/content.json, GENERATED from the authoring
// database (db/custom.db) by scripts/export_content.py. Re-run that script
// after any content change, then commit the refreshed JSON.
//
// Reading the corpus from a bundled JSON module (instead of SQLite at runtime)
// keeps the app self-contained — no filesystem database, no env vars — so the
// site deploys to serverless platforms (Vercel) without a database adapter.
import contentJson from "./content.json";
import type { TopicData } from "./types";

const data = contentJson as unknown as TopicData[];

export async function loadTopics(): Promise<TopicData[]> {
  // content.json is exported pre-sorted; these defensive sorts only matter if
  // the file is hand-edited. They replicate the original DB loader ordering:
  // topics by number ASC, sections natural-sorted on "1.2" / "1.10" numbers.
  return [...data]
    .sort((a, b) => a.number - b.number)
    .map((t) => ({
      ...t,
      sections: [...t.sections].sort((a, b) => {
        const [am, ai] = a.number.split(".").map(Number);
        const [bm, bi] = b.number.split(".").map(Number);
        return am - bm || (ai || 0) - (bi || 0);
      }),
    }));
}
