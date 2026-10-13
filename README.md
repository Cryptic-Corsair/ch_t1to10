# IAL CHEM//DECODED

**Exam-focused notes for Edexcel International A Level Chemistry (WCH11 + WCH12)** — precise definitions, every equation, and a reading experience tuned to you.

Every specification point is covered as its own collapsible section, with headings that mirror the official spec wording, so you always know exactly which statement you are revising. Topics include:

- **Topic 1** — Formulae, Equations and Amount of Substance
- **Topic 2** — Atomic Structure and the Periodic Table *(v1 + quick-revision v2 edition)*
- **Topic 3** — Bonding and Structure
- **Topic 4** — Organic Chemistry I
- **Topic 5** — Organic Chemistry II (Alkenes)
- **Topic 6** — Energetics
- **Topic 7** — Intermolecular Forces
- **Topic 8** — Redox Chemistry and Groups 1, 2 & 7
- **Topic 9** — Kinetics and Equilibria
- **Topic 10** — Halogenoalkanes, Alcohols and Spectra

## Features

- **Collapsible spec-point sections** — the full syllabus, structured for active recall, each section headed by the specification statement worded exactly as Edexcel words it
- **Three interfaces** — Studio (glass panel), Focus (warm reading room) and Hybrid (Focus cards in Studio aesthetics), plus a print-friendly layout — `data-uimode` driven
- **Worked examples** — 100 method sheets with the maths set apart from the prose, and a per-card *Cover* mode: hide the working, attempt the problem, reveal
- **Check-yourself cards & flashcard decks** — reveal-from-memory questions in the notes, plus a per-topic deck view
- **Save as PDF** — every topic has a print-ready layout via dedicated print entry points
- **Command palette** — press <kbd>Ctrl</kbd>+<kbd>K</kbd> to jump anywhere

## Tech Stack

- [Next.js](https://nextjs.org) (App Router) + React + TypeScript
- [Tailwind CSS](https://tailwindcss.com) + shadcn/ui components
- [Prisma](https://prisma.io) + SQLite
- Hash-based client routing for fast topic navigation

## Getting Started

```bash
# 1. Install dependencies (bun or npm both work)
bun install

# 2. Create your local env file
cp .env.example .env

# 3. Set up the database
bun run db:generate
bun run db:push

# 4. Start the dev server
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production

```bash
bun run build
bun run start
```

### Deploying to Vercel

The site is serverless-ready out of the box:

1. Push the repo to GitHub
2. [vercel.com/new](https://vercel.com/new) → import the repository → **Deploy** (framework auto-detected)
3. **No environment variables required** — topic content ships inside the bundle via `src/lib/site/content.json`

Notes:
- `vercel.json` skips Playwright browser downloads during the build (the server-side PDF renderer needs headless Chromium, which serverless doesn't provide — the app automatically falls back to the visitor's print engine there).
- **Content workflow**: edit content in the authoring DB (`db/custom.db`), then run `python3 scripts/export_content.py` to regenerate `content.json`, and commit the result.

## Project Structure

```
src/
├── app/            # App Router entry, global styles, print route
├── components/
│   ├── site/       # Site-specific components (topic pages, palette, settings)
│   └── ui/         # shadcn/ui primitives
├── hooks/          # Shared React hooks
└── lib/
    └── site/       # Router, topic data registry (content.json), site config
public/diagrams/    # Topic figures (light + dark variants), referenced by content.json
prisma/             # Prisma schema
scripts/            # Content build pipeline (export_content.py, diagram generators)
```

## Notes

- Topic content lives in `src/lib/site/content.json` and follows the Edexcel IAL specification ordering.
- Source study materials (`download/`, `upload/`) are intentionally excluded from version control — the repo ships code only.

---

Built with care — *quality matters most.*
