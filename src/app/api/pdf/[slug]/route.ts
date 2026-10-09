import { NextRequest, NextResponse } from 'next/server'
import type { Browser } from 'playwright'
import { loadTopics } from '@/lib/site/load'

export const dynamic = 'force-dynamic'
// Hobby-plan ceiling; the route 501s instantly on serverless hosts anyway
export const maxDuration = 60

// Headless Chromium renders /print/[slug] into a real, downloadable A4 PDF —
// deterministic output, no reliance on the visitor's browser print engine
// (which produced blank files on mobile Chrome).

const g = globalThis as unknown as { __pdfBrowser?: Browser }

async function getBrowser(): Promise<Browser> {
  if (g.__pdfBrowser?.isConnected()) return g.__pdfBrowser
  const { chromium } = await import('playwright')
  g.__pdfBrowser = await chromium.launch({
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-font-subpixel-positioning'],
  })
  return g.__pdfBrowser
}

const escapeHtml = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

function pdfFilename(topic: { number: number; title: string }): string {
  const nn = String(topic.number).padStart(2, '0')
  const clean = topic.title
    .replace(/[^a-z0-9]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48)
    .replace(/-+$/, '')
  return `IAL-Chemistry-Topic-${nn}-${clean}.pdf`
}

// small in-memory cache so repeat taps don't re-render Chromium (10 min TTL)
const cache = new Map<string, { buf: Buffer; at: number }>()
const TTL = 10 * 60 * 1000

export async function GET(req: NextRequest, ctx: { params: Promise<{ slug: string }> }) {
  // headless Chromium can't exist on serverless platforms — degrade cleanly;
  // the client (pdf-client.ts) falls back to the visitor's print engine
  if (process.env.VERCEL) {
    return NextResponse.json(
      { error: 'Server-rendered PDFs are unavailable on this deployment — use the in-page "Save PDF" button instead.' },
      { status: 501 },
    )
  }

  const { slug } = await ctx.params

  const topics = await loadTopics()
  const topic = topics.find((t) => t.slug === slug)
  if (!topic) {
    return NextResponse.json({ error: `Unknown topic: ${slug}` }, { status: 404 })
  }

  const fresh = req.nextUrl.searchParams.has('fresh')
  const hit = cache.get(slug)
  if (!fresh && hit && Date.now() - hit.at < TTL) {
    return pdfResponse(hit.buf, topic)
  }

  try {
    const browser = await getBrowser()
    const page = await browser.newPage()
    try {
      const url = new URL(`/print/${slug}`, req.nextUrl.origin).toString()
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 })
      // make sure webfonts (Playfair/Lora/Geist) are loaded before rasterising
      await page.evaluate(() => document.fonts.ready)
      await page.waitForTimeout(350)

      const nn = String(topic.number).padStart(2, '0')
      const footer = `<div style="width:100%;padding:0 15mm;display:flex;justify-content:space-between;align-items:baseline;font-family:monospace;font-size:6.8px;letter-spacing:0.12em;color:#98938A;">
        <span>IAL CHEM//DECODED &nbsp;·&nbsp; TOPIC ${nn} — ${escapeHtml(topic.title.toUpperCase()).slice(0, 58)}</span>
        <span>PAGE <span class="pageNumber"></span> / <span class="totalPages"></span></span>
      </div>`

      const buf = await page.pdf({
        format: 'A4',
        printBackground: true,
        displayHeaderFooter: true,
        headerTemplate: '<span></span>',
        footerTemplate: footer,
        margin: { top: '13mm', bottom: '17mm', left: '15mm', right: '15mm' },
      })
      cache.set(slug, { buf, at: Date.now() })
      return pdfResponse(buf, topic)
    } finally {
      await page.close()
    }
  } catch (err) {
    console.error('[pdf] generation failed for', slug, err)
    return NextResponse.json(
      { error: 'PDF generation failed — try again in a moment.' },
      { status: 500 },
    )
  }
}

function pdfResponse(buf: Buffer, topic: { number: number; title: string }) {
  return new NextResponse(new Uint8Array(buf), {
    status: 200,
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="${pdfFilename(topic)}"`,
      'Cache-Control': 'no-store',
    },
  })
}
