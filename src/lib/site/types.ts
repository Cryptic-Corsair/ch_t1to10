// Shared data types (serialized from Prisma → client)

export interface SectionData {
  id: string
  sectionKey: string
  number: string
  title: string
  blurb: string
  estMinutes: number
  /** Edexcel specification point(s) this section covers, e.g. "1.12(ii)" */
  spec?: string | null
  /** The assessment statement, worded exactly as the specification words it */
  specText?: string | null
  outline: string[]
  content: Block[] | null
}

export interface FlashcardData {
  id: string
  ord: number
  front: string
  back: string
  tag: string
}

export interface TopicData {
  slug: string
  number: number
  unit: number
  unitCode: string
  unitName: string
  title: string
  subtitle: string
  summary: string
  estHours: number
  sections: SectionData[]
  cards: FlashcardData[]
}

// ---------- notes content blocks ----------

export type Block =
  | { type: 'p'; text: string }
  | { type: 'h3'; text: string }
  | { type: 'def'; term: string; text: string }
  | { type: 'eq'; code: string; caption?: string }
  | { type: 'list'; items: string[]; ordered?: boolean }
  | { type: 'callout'; variant: 'tip' | 'warning' | 'exam' | 'key'; title: string; text: string }
  | { type: 'worked'; title: string; problem: string; steps: string[]; answer: string }
  | { type: 'qa'; title?: string; items: { q: string; a: string }[] }
  | { type: 'table'; headers: string[]; rows: string[][] }
  | { type: 'figure'; src: string; srcDark?: string; alt: string; caption?: string }
