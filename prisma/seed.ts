import { PrismaClient } from '@prisma/client'
import { TOPICS } from './seed-data/topics'
import { CARDS } from './seed-data/flashcards'
import { NOTES } from './seed-data/notes'

const db = new PrismaClient()

async function main() {
  console.log('Seeding IAL Chemistry content...')

  // wipe in order (cascade handles children)
  await db.flashcard.deleteMany()
  await db.section.deleteMany()
  await db.topic.deleteMany()

  let sectionCount = 0
  let cardCount = 0
  let notedSections = 0

  for (const t of TOPICS) {
    await db.topic.create({
      data: {
        slug: t.slug,
        number: t.number,
        unit: t.unit,
        unitCode: t.unitCode,
        unitName: t.unitName,
        title: t.title,
        subtitle: t.subtitle,
        summary: t.summary,
        estHours: t.estHours,
      },
    })

    for (const s of t.sections) {
      const blocks = NOTES[t.slug]?.[s.sectionKey] ?? null
      if (blocks) notedSections++
      await db.section.create({
        data: {
          topicSlug: t.slug,
          sectionKey: s.sectionKey,
          number: s.number,
          title: s.title,
          blurb: s.blurb,
          estMinutes: s.estMinutes,
          spec: s.spec ?? null,
          specText: s.specText ?? null,
          outline: JSON.stringify(s.outline),
          content: blocks ? JSON.stringify(blocks) : null,
        },
      })
      sectionCount++
    }

    const cards = CARDS[t.slug] ?? []
    for (let i = 0; i < cards.length; i++) {
      const c = cards[i]
      await db.flashcard.create({
        data: { topicSlug: t.slug, ord: i + 1, front: c.front, back: c.back, tag: c.tag },
      })
      cardCount++
    }
  }

  console.log(`Done: ${TOPICS.length} topics, ${sectionCount} sections (${notedSections} with full notes), ${cardCount} flashcards.`)
}

main()
  .catch((e) => { console.error(e); process.exit(1) })
  .finally(async () => { await db.$disconnect() })
