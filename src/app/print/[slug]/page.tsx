import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import { loadTopics } from '@/lib/site/load'
import { PrintDoc } from '@/components/site/print-doc'

export const dynamic = 'force-dynamic'

export const metadata: Metadata = {
  title: 'Print edition',
  robots: { index: false, follow: false },
}

// The paper document headless Chromium renders into the downloadable PDF.
// Not linked anywhere in the site chrome — reached via /api/pdf/[slug].
export default async function PrintPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const topics = await loadTopics()
  const topic = topics.find((t) => t.slug === slug)
  if (!topic) notFound()
  return <PrintDoc topic={topic} topics={topics} />
}
