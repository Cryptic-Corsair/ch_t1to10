// Server-side topic loader — shared by the SPA page, the print route and the PDF API.
import { db } from '@/lib/db'
import type { TopicData, SectionData, Block } from './types'

function safeArray(json: string): string[] {
  try {
    const v = JSON.parse(json)
    return Array.isArray(v) ? (v as string[]) : []
  } catch {
    return []
  }
}

export async function loadTopics(): Promise<TopicData[]> {
  const rows = await db.topic.findMany({
    orderBy: { number: 'asc' },
    include: {
      sections: { orderBy: { number: 'asc' } },
      cards: { orderBy: { ord: 'asc' } },
    },
  })

  return rows.map((t) => ({
    slug: t.slug,
    number: t.number,
    unit: t.unit,
    unitCode: t.unitCode,
    unitName: t.unitName,
    title: t.title,
    subtitle: t.subtitle,
    summary: t.summary,
    estHours: t.estHours,
    sections: t.sections
      .map<SectionData>((s) => {
        let blocks: Block[] | null = null
        if (s.content) {
          try {
            blocks = JSON.parse(s.content) as Block[]
          } catch {
            blocks = null
          }
        }
        return {
          id: s.id,
          sectionKey: s.sectionKey,
          number: s.number,
          title: s.title,
          blurb: s.blurb,
          estMinutes: s.estMinutes,
          spec: s.spec,
          specText: s.specText,
          outline: safeArray(s.outline),
          content: blocks,
        }
      })
      // natural sort on "1.2" / "1.10" style section numbers (DB string order would put 1.10 before 1.2)
      .sort((a, b) => {
        const [am, ai] = a.number.split('.').map(Number)
        const [bm, bi] = b.number.split('.').map(Number)
        return am - bm || (ai || 0) - (bi || 0)
      }),
    cards: t.cards.map((c) => ({
      id: c.id,
      ord: c.ord,
      front: c.front,
      back: c.back,
      tag: c.tag,
    })),
  }))
}
