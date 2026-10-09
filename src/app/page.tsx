import { AppShell, type AppStats } from '@/components/site/app-shell'
import { loadTopics } from '@/lib/site/load'

export const dynamic = 'force-dynamic'

export default async function Page() {
  const topics = await loadTopics()

  const stats: AppStats = {
    sections: topics.reduce((a, t) => a + t.sections.length, 0),
    cards: topics.reduce((a, t) => a + t.cards.length, 0),
    noted: topics.reduce((a, t) => a + t.sections.filter((s) => s.content).length, 0),
  }

  return <AppShell topics={topics} stats={stats} />
}
