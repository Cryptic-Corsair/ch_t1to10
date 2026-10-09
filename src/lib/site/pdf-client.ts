"use client";

// Client-side topic PDF download with graceful degradation.
//
// Preferred path: /api/pdf/[slug] — headless Chromium renders the dedicated
// print document into a real A4 PDF. This needs a Chromium binary, which
// serverless deployments (Vercel) don't provide — there the API answers 501
// and we fall back to the visitor's own print engine (the topic page carries
// full print CSS + auto-expansion of collapsed sections).
export async function downloadTopicPdf(slug: string, filename?: string): Promise<void> {
  try {
    const res = await fetch(`/api/pdf/${slug}`)
    if (res.status === 501) {
      // server-side rendering unavailable — use the browser's print dialog
      window.print()
      return
    }
    if (!res.ok) throw new Error("pdf request failed")
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.download = filename || `IAL-Chemistry-Topic-${slug}.pdf`
    a.href = url
    document.body.appendChild(a)
    a.click()
    a.remove()
    setTimeout(() => URL.revokeObjectURL(url), 4000)
  } catch {
    // fallback: direct navigation still downloads via Content-Disposition
    window.open(`/api/pdf/${slug}`, "_blank")
  }
}
