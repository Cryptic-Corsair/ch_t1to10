// Specification index — the assessment statements, worded exactly as the
// specification words them, plus the machinery behind the custom notes page.
//
// Every topic ships a "specification-map" section holding a two-column table
// (Spec | Assessment statement) lifted verbatim from the Edexcel 2018 spec.
// That table is the canonical verbatim source for the index. Each content
// section then declares which point(s) it covers via its `spec` field, e.g.
// "1.8(iii)" or "1.1, 1.2 & 1.4" or a range like "1.1 – 1.12".
import type { TopicData, SectionData } from './types'

// ---------- spec-code parsing ----------

/** Split a section's `spec` string into individual point codes.
 *  Handles comma/ampersand lists, en-dash ranges ("1.1 – 1.12") and
 *  roman-numeral sub-parts ("1.12(ii)"). */
export function parseSpecCodes(spec: string | null | undefined): string[] {
  if (!spec) return []
  const out: string[] = []
  for (const part of spec.split(/[,;&]/)) {
    const t = part.trim()
    if (!t) continue
    // range "1.1 – 1.12" (also plain hyphen) → every integer point inside
    const range = t.match(/^(\d+)\.(\d+)\s*[–-]\s*(?:\d+\.)?(\d+)$/)
    if (range) {
      const topic = range[1]
      for (let i = Number(range[2]); i <= Number(range[3]); i++) out.push(`${topic}.${i}`)
      continue
    }
    // "1.12(ii)" / "5.6"
    const m = t.match(/^(\d+\.\d+)(\([a-z0-9]+\))?$/i)
    out.push(m ? m[1] + (m[2] ?? '') : t)
  }
  return out
}

/** Does a selection of point `pick` cover a section-level code `code`?
 *  Selecting the parent "1.12" also pulls in "1.12(i)"…"1.12(iii)";
 *  selecting "5.6" matches exactly "5.6". */
export function codeCoveredBy(pick: string, code: string): boolean {
  return code === pick || code.startsWith(pick + '(')
}

// ---------- the index ----------

export interface SpecPointRef {
  slug: string
  sectionKey: string
  title: string
}

export interface SpecPoint {
  /** verbatim point code, e.g. "5.6" or "1.12" */
  code: string
  /** the assessment statement, worded exactly as the specification words it */
  statement: string
  topicSlug: string
  topicNumber: number
  topicTitle: string
  /** the note sections that cover this point (in topic order) */
  sections: SpecPointRef[]
}

function specMapTable(t: TopicData): { rows: string[][] } | null {
  const map = t.sections.find((s) => s.sectionKey === 'specification-map')
  if (!map?.content) return null
  const table = map.content.find((b) => b.type === 'table')
  return table && table.type === 'table' ? table : null
}

function sectionCoversPoint(s: SectionData, code: string): boolean {
  return parseSpecCodes(s.spec).some((c) => codeCoveredBy(code, c))
}

/** Build the full index: one entry per specification point, grouped by topic.
 *  Statements come verbatim from each topic's specification-map table. */
export function buildSpecIndex(topics: TopicData[]): SpecPoint[] {
  const out: SpecPoint[] = []
  for (const t of [...topics].sort((a, b) => a.number - b.number)) {
    const table = specMapTable(t)
    if (!table) continue
    for (const [code, statement] of table.rows) {
      if (!code) continue
      const sections = t.sections
        .filter((s) => s.sectionKey !== 'specification-map' && sectionCoversPoint(s, code))
        .map((s) => ({ slug: t.slug, sectionKey: s.sectionKey, title: s.title }))
      out.push({ code, statement: statement ?? '', topicSlug: t.slug, topicNumber: t.number, topicTitle: t.title, sections })
    }
  }
  return out
}

// ---------- custom notes (sections behind picked points) ----------

export interface CustomSection {
  topic: TopicData
  section: SectionData
  /** the picked points this section satisfies, e.g. ["5.6"] */
  viaPicks: string[]
}

export interface CustomTopicGroup {
  topic: TopicData
  sections: CustomSection[]
}

/** The note sections to render for a set of picked spec points, grouped by
 *  topic in syllabus order, sections in natural order within each topic. */
export function sectionsForPicks(topics: TopicData[], picks: string[]): CustomTopicGroup[] {
  if (picks.length === 0) return []
  const groups: CustomTopicGroup[] = []
  for (const t of [...topics].sort((a, b) => a.number - b.number)) {
    const sections: CustomSection[] = []
    for (const s of t.sections) {
      if (s.sectionKey === 'specification-map') continue
      const codes = parseSpecCodes(s.spec)
      const viaPicks = picks.filter((p) => codes.some((c) => codeCoveredBy(p, c)))
      if (viaPicks.length > 0) sections.push({ topic: t, section: s, viaPicks })
    }
    if (sections.length > 0) groups.push({ topic: t, sections })
  }
  return groups
}
