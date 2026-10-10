import { PrismaClient } from '@prisma/client'
const db = new PrismaClient()
const s = await db.section.findFirst({ where: { sectionKey: 'group1-2-ionisation-energy' } })
console.log('len:', s?.content?.length)
console.log('has NEW:', s?.content?.includes('members of Group I and Group II, respectively'))
console.log('has OLD:', s?.content?.includes('Reuse Topic 2'))
const blurb = await db.section.findFirst({ where: { sectionKey: 'group1-2-ionisation-energy' }, select: { blurb: true } })
console.log('blurb:', blurb?.blurb)
await db.$disconnect()
