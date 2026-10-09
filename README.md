# IAL CHEM//DECODED

**Exam-focused notes for Edexcel International A Level Chemistry (WCH11 + WCH12)** — precise definitions, every equation, and a reading experience tuned to you.

Every specification point is covered as its own collapsible section, with headings that mirror the official spec wording, so you always know exactly which statement you are revising. Topics include:

- **Topic 1** — Formulae, Equations and Amount of Substance
- **Topic 2** — Atomic Structure and the Periodic Table
- **Topic 3** — Bonding and Structure
- **Topic 4** — Organic Chemistry I
- **Topic 5** — Organic Chemistry II (Alkenes)
- **Topic 6** — Energetics
- **Topic 7** — Intermolecular Forces
- **Topic 8** — Redox Chemistry and Groups 1, 2 & 7
- **Topic 9** — Kinetics and Equilibria *(in progress)*
- **Topic 10** — Kinetics II *(planned)*

## Features

- **Collapsible spec-point sections** — the full syllabus, structured for active recall
- **Three reading presets** — Focus, Studio and print-friendly layouts (`data-uimode` driven)
- **Save as PDF** — every topic has a print-ready layout via dedicated print entry points
- **Command palette** — press <kbd>Ctrl</kbd>+<kbd>K</kbd> to jump anywhere
- **Print layer** — `@media print` styles with auto-expansion of collapsed sections

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
    └── site/       # Router, topic data registry, site config
prisma/             # Prisma schema
```

## Notes

- Topic content lives in the data registry under `src/lib/site/` and follows the Edexcel IAL specification ordering.
- The `upload/` directory (source study materials) is intentionally excluded from version control.

---

Built with care — *quality matters most.*
