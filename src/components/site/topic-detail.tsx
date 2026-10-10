'use client'

import React, { useEffect, useMemo, useRef, useState } from 'react'
import {
  ArrowLeft,
  ArrowLeftRight,
  ArrowRight,
  ArrowUp,
  BookOpen,
  Check,
  CheckCheck,
  CheckCircle2,
  ChevronDown,
  ChevronsDownUp,
  ChevronsUpDown,
  Clock3,
  Eye,
  EyeOff,
  Layers3,
  Link2,
  ListTree,
  Loader2,
  Minus,
  Plus,
  Printer,
  Type,
  X,
} from 'lucide-react'
import type { SectionData, TopicData } from '@/lib/site/types'
import { downloadTopicPdf } from '@/lib/site/pdf-client'
import { BlockRenderer, BulletCard, Inline, groupBlocks } from './blocks'
import { BtnGhost, BtnSolid, ProgressBar } from './ui-bits'
import { useProgress, useSettings } from '@/lib/site/stores'

const pad = (n: number) => String(n).padStart(2, '0')

/* "1 h 25 min" / "42 min" — remaining reading time, without the tilde */
const fmtLeft = (m: number) =>
  m >= 60 ? `${Math.floor(m / 60)} h${m % 60 ? ` ${m % 60} min` : ''}` : `${m} min`

export function TopicDetail({
  topic, topics, slug, sectionId, go, hydrated,
}: {
  topic: TopicData; topics: TopicData[]; slug: string; sectionId?: string
  go: (to: string) => void; hydrated: boolean
}) {
  const { read, markRead, markUnread, markAll, touch } = useProgress()
  const mode = useSettings((s) => s.uiMode)
  const fontSize = useSettings((s) => s.fontSize)
  const fontFamily = useSettings((s) => s.fontFamily)
  const focusMode = useSettings((s) => s.focusMode)
  const showOutline = useSettings((s) => s.showOutline)
  const setSetting = useSettings((s) => s.set)

  const [activeId, setActiveId] = useState<string>(topic.sections[0]?.sectionKey ?? '')
  const [progress, setProgress] = useState(0)
  const [showTop, setShowTop] = useState(false)
  const [tocOpen, setTocOpen] = useState(false)
  const streamRef = useRef<HTMLDivElement>(null)
  const readMap = hydrated ? read : ({} as Record<string, true>)

  useEffect(() => {
    touch(slug)
  }, [slug])

  // mark the page for terminal topic chrome (fab stack + warm reading room)
  useEffect(() => {
    document.documentElement.dataset.page = 'topic'
    return () => {
      delete document.documentElement.dataset.page
    }
  }, [])

  // close the floating contents on Escape
  useEffect(() => {
    if (!tocOpen) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setTocOpen(false)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [tocOpen])

  // scroll-spy + reading progress + back-to-top visibility (rAF-throttled)
  useEffect(() => {
    let raf = 0
    const ids = topic.sections.map((s) => s.sectionKey)
    const measure = () => {
      raf = 0
      const winH = window.innerHeight
      const y = window.scrollY
      const els = ids
        .map((id) => document.getElementById(`sec-${id}`))
        .filter(Boolean) as HTMLElement[]
      let p = 0
      if (els.length > 0) {
        const start = Math.max(0, els[0].offsetTop - 140)
        const last = els[els.length - 1]
        const end = Math.max(start + 1, last.offsetTop + last.offsetHeight - winH)
        p = Math.max(0, Math.min(100, ((y - start) / (end - start)) * 100))
        let current = els[0]
        for (const el of els) {
          if (el.offsetTop <= y + 170) current = el
        }
        setActiveId(current.id.replace('sec-', ''))
      }
      setProgress(p)
      setShowTop(y > 720)
    }
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(measure)
    }
    measure()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      if (raf) cancelAnimationFrame(raf)
    }
  }, [topic])

  // deep-link to section
  useEffect(() => {
    if (!sectionId) return
    const el = document.getElementById(`sec-${sectionId}`)
    if (el) setTimeout(() => window.scrollTo({ top: el.offsetTop - 90, behavior: 'smooth' }), 60)
  }, [sectionId])

  // keyboard: J / K jump between sections
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return
      if (e.metaKey || e.ctrlKey || e.altKey) return
      const key = e.key.toLowerCase()
      if (key !== 'j' && key !== 'k') return
      const idx = topic.sections.findIndex((s) => s.sectionKey === activeId)
      const nextIdx = key === 'j'
        ? Math.min(topic.sections.length - 1, idx + 1)
        : Math.max(0, idx - 1)
      if (nextIdx === idx) return
      const el = document.getElementById(`sec-${topic.sections[nextIdx].sectionKey}`)
      if (el) {
        e.preventDefault()
        window.scrollTo({ top: el.offsetTop - 90, behavior: 'smooth' })
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [topic, activeId])

  // expand / collapse every collapsible spec point in the stream
  const setAllSpec = (open: boolean) => {
    streamRef.current?.querySelectorAll<HTMLDetailsElement>('details.spec-point').forEach((d) => {
      d.open = open
    })
  }

  // PDF: /api/pdf/[slug] renders the dedicated print document server-side
  // (cover, contents, spec sections); on deployments without headless
  // Chromium (Vercel) pdf-client falls back to the visitor's print engine
  const [pdfBusy, setPdfBusy] = useState(false)
  const downloadPdf = async () => {
    if (pdfBusy) return
    setPdfBusy(true)
    try {
      const nn = String(topic.number).padStart(2, '0')
      const filename = `IAL-Chemistry-Topic-${nn}-${topic.title.replace(/[^a-z0-9]+/gi, '-').replace(/^-+|-+$/g, '').slice(0, 48).replace(/-+$/, '')}.pdf`
      await downloadTopicPdf(slug, filename)
    } finally {
      setPdfBusy(false)
    }
  }

  // printing: open every collapsed spec point so nothing is lost on paper,
  // then restore the reader's state afterwards
  useEffect(() => {
    const onBefore = () => {
      streamRef.current?.querySelectorAll<HTMLDetailsElement>('details').forEach((d) => {
        d.dataset.printOpen = d.open ? '1' : '0'
        d.open = true
      })
    }
    const onAfter = () => {
      streamRef.current?.querySelectorAll<HTMLDetailsElement>('details').forEach((d) => {
        if (d.dataset.printOpen === '0') d.open = false
        delete d.dataset.printOpen
      })
    }
    window.addEventListener('beforeprint', onBefore)
    window.addEventListener('afterprint', onAfter)
    return () => {
      window.removeEventListener('beforeprint', onBefore)
      window.removeEventListener('afterprint', onAfter)
    }
  }, [])

  const scrollToSection = (sectionKey: string) => {
    const el = document.getElementById(`sec-${sectionKey}`)
    if (el) window.scrollTo({ top: el.offsetTop - 90, behavior: 'smooth' })
    else go(`/topic/${slug}/${sectionKey}`)
  }

  const doneCount = useMemo(
    () => (hydrated ? topic.sections.filter((s) => readMap[`${slug}/${s.sectionKey}`]).length : 0),
    [hydrated, readMap, topic, slug]
  )
  const total = topic.sections.length
  const pct = total ? (doneCount / total) * 100 : 0
  const allRead = doneCount === total
  const minLeft = useMemo(
    () => topic.sections.reduce((acc, s) => acc + (readMap[`${slug}/${s.sectionKey}`] ? 0 : s.estMinutes || 0), 0),
    [readMap, topic, slug]
  )
  const hasNotes = topic.sections.some((s) => s.content)
  const firstUnread = topic.sections.find((s) => !readMap[`${slug}/${s.sectionKey}`])

  /* prev/next walk the canonical topics only — version variants sit outside the flow.
     A -v2 page borrows its original's slot: prev = the original topic, next = the topic after it. */
  const isV2 = slug.endsWith('-v2')
  const navTopics = topics.filter((t) => !t.slug.endsWith('-v2'))
  const baseIdx = navTopics.findIndex((t) => t.slug === slug.replace(/-v2$/, ''))
  const prev = isV2
    ? navTopics[baseIdx] ?? null
    : baseIdx > 0
      ? navTopics[baseIdx - 1]
      : null
  const next = baseIdx >= 0 && baseIdx < navTopics.length - 1 ? navTopics[baseIdx + 1] : null

  /* version siblings — Topic 2 has a digest edition living at -v2 */
  const sibSlug =
    slug === 'atomic-structure-v2' ? 'atomic-structure' : slug === 'atomic-structure' ? 'atomic-structure-v2' : null

  /* ---------- shared fragments ---------- */

  const progressActions = (center = false) => (
    <div className={`flex flex-wrap items-center gap-x-8 gap-y-5 ${center ? 'justify-center' : ''}`}>
      <div className="min-w-[240px] flex-1 sm:max-w-sm">
        <div className="mb-2 flex items-baseline justify-between">
          <span className="text-[12.5px] text-muted">
            {doneCount} of {total} sections read
          </span>
          <span className="mono text-[11px] text-faint">{Math.round(pct)}%</span>
        </div>
        <ProgressBar value={pct} />
      </div>
      <div className="flex flex-wrap items-center gap-2.5">
        {firstUnread && doneCount > 0 && (
          <BtnSolid onClick={() => scrollToSection(firstUnread.sectionKey)}>
            <BookOpen size={14} />
            Continue
          </BtnSolid>
        )}
        <BtnGhost onClick={() => go(`/deck/${slug}`)}>
          <Layers3 size={14} />
          Flashcards
        </BtnGhost>
        <BtnGhost
          onClick={() => markAll(slug, topic.sections.map((s) => s.sectionKey), !allRead)}
          ariaLabel={allRead ? 'Mark all sections as not read' : 'Mark all sections as read'}
        >
          <CheckCheck size={14} />
          {allRead ? 'Reset read' : 'Mark all read'}
        </BtnGhost>
        <BtnGhost onClick={downloadPdf} ariaLabel="Download this topic as a PDF revision sheet">
          {pdfBusy ? <Loader2 size={14} className="animate-spin" /> : <Printer size={14} />}
          {pdfBusy ? 'Building…' : 'Save PDF'}
        </BtnGhost>
      </div>
    </div>
  )

  const mobileContents = (
    <details className="group h-fit rounded-xl border border-line bg-surface print:hidden lg:hidden">
      <summary className="flex cursor-pointer list-none items-center justify-between px-5 py-3.5 [&::-webkit-details-marker]:hidden">
        <span className="flex items-center gap-2.5 text-[13.5px] font-medium text-fg">
          <ListTree size={14} strokeWidth={1.75} className="text-acc" />
          Contents
          <span className="font-normal text-muted">· {total} sections · {doneCount} read{minLeft > 0 ? ` · ~${fmtLeft(minLeft)} left` : ''}</span>
        </span>
        <ChevronDown size={15} className="text-muted t-fast group-open:rotate-180" />
      </summary>
      <nav className="border-t border-line px-3 py-2" aria-label="Sections (mobile)">
        {topic.sections.map((s) => {
          const isRead = !!readMap[`${slug}/${s.sectionKey}`]
          return (
            <button
              key={s.sectionKey}
              onClick={(e) => {
                scrollToSection(s.sectionKey)
                e.currentTarget.closest('details')?.removeAttribute('open')
              }}
              className="flex w-full items-baseline gap-3 rounded-lg px-2 py-2.5 text-left t-fast hover:bg-elev focus-visible:outline-acc"
            >
              <span className="shrink-0" aria-hidden>
                {isRead ? (
                  <CheckCircle2 size={13} strokeWidth={2} className="text-acc" />
                ) : (
                  <span className="mt-px block h-[11px] w-[11px] rounded-full border border-line-strong" />
                )}
              </span>
              <span className="mono shrink-0 text-[11px] text-faint">{s.number}</span>
              <span className="min-w-0 flex-1 text-[13px] leading-snug text-muted">{s.title}</span>
            </button>
          )
        })}
      </nav>
    </details>
  )

  const toolsRail = (
    <div className="sticky top-20 flex flex-col items-center gap-1.5">
      <ToolBtn label="Decrease text size" onClick={() => setSetting({ fontSize: Math.max(0, fontSize - 1) })} disabled={fontSize === 0}>
        <Minus size={14} strokeWidth={1.75} />
      </ToolBtn>
      <ToolBtn label="Increase text size" onClick={() => setSetting({ fontSize: Math.min(3, fontSize + 1) })} disabled={fontSize === 3}>
        <Plus size={14} strokeWidth={1.75} />
      </ToolBtn>
      <ToolBtn
        label={fontFamily === 'serif' ? 'Switch to sans font' : 'Switch to serif font'}
        active={fontFamily === 'serif'}
        onClick={() => setSetting({ fontFamily: fontFamily === 'serif' ? 'sans' : 'serif' })}
      >
        <Type size={14} strokeWidth={1.75} />
      </ToolBtn>
      <ToolBtn
        label={focusMode ? 'Turn off focus mode' : 'Turn on focus mode'}
        active={focusMode}
        onClick={() => setSetting({ focusMode: !focusMode })}
      >
        {focusMode ? <EyeOff size={14} strokeWidth={1.75} /> : <Eye size={14} strokeWidth={1.75} />}
      </ToolBtn>
      <ToolBtn
        label={pdfBusy ? 'Building your PDF…' : 'Download this topic as PDF'}
        onClick={downloadPdf}
        disabled={pdfBusy}
      >
        {pdfBusy ? <Loader2 size={14} strokeWidth={1.75} className="animate-spin" /> : <Printer size={14} strokeWidth={1.75} />}
      </ToolBtn>
      <div aria-hidden className="mt-2 h-8 w-px bg-line" />
      <ToolBtn label="Back to top" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} disabled={!showTop}>
        <ArrowUp size={14} strokeWidth={1.75} />
      </ToolBtn>
    </div>
  )

  const endPanelCls =
    mode === 'lab'
      ? 'lab-glass rounded-[26px]'
      : 'rounded-2xl border border-line bg-surface'

  /* ---------- mastheads per interface ---------- */

  let masthead: React.ReactNode
  if (mode === 'lab') {
    masthead = (
      <header className="lab-glass mt-8 rounded-[26px] p-7 sm:p-10">
        <span className="lab-chip">Chapter {pad(topic.number)} · {topic.unitCode}{isV2 ? ' · Version 2' : ''}</span>
        <h1 className="mt-6 max-w-[20ch] text-[clamp(34px,5.2vw,52px)] leading-[1.06] text-fg">
          <span className="lab-grad">{topic.title}</span>
        </h1>
        <p className="mt-4 max-w-[560px] text-[15px] leading-relaxed text-muted">{topic.subtitle}</p>
        <div className="mt-6 flex flex-wrap gap-2">
          {[
            `${total} sections`,
            `~${topic.estHours} h`,
            `${topic.cards.length} cards`,
            `${topic.unitName}`,
          ].map((m) => (
            <span key={m} className="lab-glass rounded-full px-3.5 py-1.5 text-[11.5px] font-medium text-muted" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
              {m}
            </span>
          ))}
        </div>
        <div className="mt-8 flex flex-wrap items-center gap-2.5 print:hidden">
          {sibSlug && (
            <BtnGhost onClick={() => go(`/topic/${sibSlug}`)} ariaLabel="Switch to the other version of this topic">
              <ArrowLeftRight size={14} />
              {isV2 ? 'Original version' : 'Version 2 · digest'}
            </BtnGhost>
          )}
          {topic.cards.length > 0 && (
            <BtnGhost onClick={() => go(`/deck/${slug}`)}>
              <Layers3 size={14} />
              Flashcards
            </BtnGhost>
          )}
        </div>
        <div className="mt-8 print:hidden">{progressActions(false)}</div>
      </header>
    )
  } else {
    /* TERMINAL — the warm reading room: numeral rail, meta dots, pill actions */
    const started = doneCount > 0
    masthead = (
      <header className="relative mt-6 border-b border-line pb-10 sm:mt-8">
        <div className="grid gap-7 sm:grid-cols-[auto_minmax(0,1fr)] sm:gap-8 lg:gap-10">
          <div className="hidden sm:block" aria-hidden>
            <span className="mast-num block select-none">{pad(topic.number)}</span>
          </div>
          <div className="min-w-0 sm:border-l sm:border-line sm:pl-6 lg:pl-10">
            <div className="flex flex-wrap items-center gap-x-3.5 gap-y-2">
              <span className="mono text-[11px] font-bold uppercase tracking-[0.2em] text-acc">
                Topic {pad(topic.number)}
              </span>
              {isV2 && (
                <span className="mono rounded-full border border-acc/40 bg-acc/10 px-2 py-0.5 text-[9px] font-bold uppercase tracking-[0.16em] text-acc">
                  Version 2
                </span>
              )}
              <span aria-hidden className="h-3 w-px bg-line-strong" />
              <span className="mono text-[10.5px] uppercase tracking-[0.18em] text-muted">
                Unit {topic.unit} · {topic.unitCode}
              </span>
              <span aria-hidden className="h-3 w-px bg-line-strong" />
              <span className="mono inline-flex items-center gap-1.5 text-[10.5px] uppercase tracking-[0.18em] text-muted">
                <Clock3 size={12} strokeWidth={1.75} className="text-faint" />
                ~{topic.estHours} h
              </span>
              <span aria-hidden className="hidden h-3 w-px bg-line-strong sm:block" />
              <span
                className="hidden items-center gap-1.5 sm:flex"
                role="img"
                aria-label={`${doneCount} of ${total} sections read`}
              >
                {topic.sections.map((sd) => {
                  const r = !!readMap[`${slug}/${sd.sectionKey}`]
                  const act = activeId === sd.sectionKey && !r
                  return (
                    <span
                      key={sd.sectionKey}
                      aria-hidden
                      className={`h-[7px] w-[7px] rounded-full t-fast ${
                        r ? 'bg-acc' : act ? 'border border-acc bg-acc/25' : 'border border-line-strong'
                      }`}
                    />
                  )
                })}
              </span>
            </div>
            <h1 className="display-serif mt-5 max-w-[22ch] text-[clamp(34px,5.2vw,52px)] leading-[1.07] text-fg">
              {topic.title}
            </h1>
            <p className="mt-5 max-w-[600px] text-[16px] leading-relaxed text-muted">{topic.subtitle}</p>
            <div className="mt-7 flex flex-wrap items-center gap-2.5 print:hidden">
              {allRead ? (
                <BtnGhost onClick={() => scrollToSection(topic.sections[0].sectionKey)}>
                  <BookOpen size={14} />
                  Review from the top
                </BtnGhost>
              ) : (
                <BtnSolid
                  onClick={() => scrollToSection((started && firstUnread ? firstUnread : topic.sections[0]).sectionKey)}
                >
                  <BookOpen size={14} />
                  {started ? 'Continue reading' : 'Start reading'}
                </BtnSolid>
              )}
              {sibSlug && (
                <BtnGhost onClick={() => go(`/topic/${sibSlug}`)} ariaLabel="Switch to the other version of this topic">
                  <ArrowLeftRight size={14} />
                  {isV2 ? 'Original version' : 'Version 2 · digest'}
                </BtnGhost>
              )}
              {topic.cards.length > 0 && (
                <BtnGhost onClick={() => go(`/deck/${slug}`)}>
                  <Layers3 size={14} />
                  Flashcards
                </BtnGhost>
              )}
              <BtnGhost
                onClick={() => markAll(slug, topic.sections.map((s) => s.sectionKey), !allRead)}
                ariaLabel={allRead ? 'Mark all sections as not read' : 'Mark all sections as read'}
              >
                <CheckCheck size={14} />
                {allRead ? 'Reset read' : 'Mark all read'}
              </BtnGhost>
              <BtnGhost onClick={downloadPdf} ariaLabel="Download this topic as a PDF revision sheet">
                {pdfBusy ? <Loader2 size={14} className="animate-spin" /> : <Printer size={14} />}
                {pdfBusy ? 'Building…' : 'Save PDF'}
              </BtnGhost>
            </div>
            <div className="mt-6 flex items-center gap-3.5 print:hidden">
              <span className="mono shrink-0 text-[10px] uppercase tracking-[0.14em] text-faint">
                {doneCount}/{total} read
              </span>
              <ProgressBar value={pct} className="max-w-[280px] flex-1 sm:flex-none" />
              {allRead && (
                <span className="mono inline-flex items-center gap-1 text-[10px] uppercase tracking-[0.14em] text-acc">
                  <Check size={12} strokeWidth={2.5} /> complete
                </span>
              )}
            </div>
          </div>
        </div>
      </header>
    )
  }

  /* ---------- breadcrumbs per interface ---------- */

  const crumb =
    mode === 'lab' ? (
      <nav aria-label="Breadcrumb" className="mt-6 flex items-center gap-2 text-[12.5px] text-muted">
        <button onClick={() => go('/topics')} className="inline-flex items-center gap-1.5 rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] px-3.5 py-1.5 t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
          <ArrowLeft size={12} />
          All topics
        </button>
        <span aria-hidden className="text-faint">/</span>
        <span style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>Chapter {pad(topic.number)}</span>
      </nav>
    ) : (
      <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-[12.5px] text-faint">
        <button onClick={() => go('/topics')} className="inline-flex items-center gap-1.5 t-fast hover:text-fg focus-visible:outline-acc">
          <ArrowLeft size={13} />
          All topics
        </button>
        <span aria-hidden>/</span>
        <span className="text-muted">Topic {pad(topic.number)}</span>
      </nav>
    )

  /* ---------- desktop TOC per interface ---------- */

  const tocLab = (
    <div className="sticky top-24">
      <p className="mb-1.5 text-[10px] font-semibold uppercase tracking-[0.2em] text-faint" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
        On this page
      </p>
      <p className="mb-3 text-[11px] text-faint" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
        {doneCount}/{total} read{minLeft > 0 ? ` · ~${fmtLeft(minLeft)} left` : ' · complete'}
      </p>
      <nav className="space-y-1.5" aria-label="Sections">
        {topic.sections.map((s) => {
          const isRead = !!readMap[`${slug}/${s.sectionKey}`]
          const isActive = activeId === s.sectionKey
          return (
            <button
              key={s.sectionKey}
              onClick={() => scrollToSection(s.sectionKey)}
              aria-current={isActive ? 'true' : undefined}
              className={`w-full rounded-full border px-3.5 py-2 text-left text-[12px] leading-snug t-fast focus-visible:outline-acc ${
                isActive
                  ? 'border-[color-mix(in_srgb,var(--acc)_50%,transparent)] bg-[color-mix(in_srgb,var(--acc)_12%,transparent)] text-acc'
                  : 'border-[color-mix(in_srgb,var(--fg)_10%,transparent)] text-muted hover:border-[color-mix(in_srgb,var(--fg)_22%,transparent)] hover:text-fg'
              }`}
              style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}
            >
              <span className={`mr-1.5 text-[10px] ${isRead ? 'text-acc' : 'text-faint'}`}>{isRead ? '●' : '○'}</span>
              {s.title}
            </button>
          )
        })}
      </nav>
      <button
        onClick={() => go(`/deck/${slug}`)}
        className="lab-glass mt-4 w-full rounded-full px-4 py-2.5 text-[12px] font-semibold text-acc t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] focus-visible:outline-acc"
        style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}
      >
        Deck · {topic.cards.length} cards
      </button>
    </div>
  )

  /* ---------- TERMINAL floating contents — bubble, popover, scroll-top ---------- */

  const unread = total - doneCount
  const floatingToc = mode === 'terminal' && (
    <>
      {tocOpen && <div aria-hidden className="fixed inset-0 z-40 print:hidden" onClick={() => setTocOpen(false)} />}
      {/* scroll back to top (bottom-left) */}
      <button
        type="button"
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        aria-label="Back to top"
        aria-hidden={!showTop}
        tabIndex={showTop ? 0 : -1}
        className={`mono fixed bottom-5 left-5 z-40 flex h-11 w-11 items-center justify-center rounded-full border border-line-strong bg-surface text-muted shadow-lg t-fast hover:border-acc hover:text-acc focus-visible:outline-acc print:hidden ${
          showTop ? 'opacity-100' : 'pointer-events-none opacity-0'
        }`}
      >
        <ArrowUp size={16} strokeWidth={1.75} />
      </button>
      {/* contents cluster (bottom-right) */}
      <div className="fixed bottom-5 right-5 z-50 print:hidden">
        {tocOpen && (
          <div
            role="dialog"
            aria-label="Section contents"
            className="absolute bottom-[62px] right-0 w-[340px] max-w-[calc(100vw-40px)] overflow-hidden rounded-2xl border border-line bg-surface shadow-2xl"
            style={{ animation: 'toc-pop 170ms cubic-bezier(0.33,1,0.68,1)' }}
          >
            <div className="flex items-center justify-between gap-4 border-b border-line px-4 py-3.5">
              <div>
                <p className="mono text-[10px] uppercase tracking-[0.18em] text-faint">Contents</p>
                <p className="mt-0.5 whitespace-nowrap text-[13px] font-semibold text-fg">
                  {doneCount} of {total} read
                </p>
                <p className="mono mt-0.5 whitespace-nowrap text-[10px] text-faint">
                  {minLeft > 0 ? `~${fmtLeft(minLeft)} of reading left` : 'everything read'}
                </p>
              </div>
              <ProgressBar value={pct} className="w-24 shrink-0" />
            </div>
            <nav className="max-h-[44vh] overflow-y-auto px-2.5 py-2.5" aria-label="Sections">
              {topic.sections.map((s) => {
                const r = !!readMap[`${slug}/${s.sectionKey}`]
                const act = activeId === s.sectionKey
                return (
                  <button
                    key={s.sectionKey}
                    onClick={() => {
                      scrollToSection(s.sectionKey)
                      setTocOpen(false)
                    }}
                    aria-current={act ? 'true' : undefined}
                    className={`flex w-full items-center gap-3 rounded-xl px-2.5 py-2.5 text-left t-fast focus-visible:outline-acc ${
                      act ? 'bg-elev' : 'hover:bg-elev'
                    }`}
                  >
                    <span className={`mono w-7 shrink-0 text-[10.5px] font-semibold ${act ? 'text-acc' : 'text-faint'}`}>
                      {s.number}
                    </span>
                    <span className={`min-w-0 flex-1 text-[13px] leading-snug ${act ? 'font-medium text-fg' : 'text-muted'}`}>
                      {s.title}
                    </span>
                    <span className="shrink-0" aria-hidden>
                      {r ? (
                        <CheckCircle2 size={14} strokeWidth={2} className="text-acc" />
                      ) : (
                        <span className="block h-[11px] w-[11px] rounded-full border border-line-strong" />
                      )}
                    </span>
                  </button>
                )
              })}
            </nav>
            <div className="border-t border-line px-3.5 py-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5">
                  <ToolBtn label="Decrease text size" onClick={() => setSetting({ fontSize: Math.max(0, fontSize - 1) })} disabled={fontSize === 0}>
                    <Minus size={14} strokeWidth={1.75} />
                  </ToolBtn>
                  <ToolBtn label="Increase text size" onClick={() => setSetting({ fontSize: Math.min(3, fontSize + 1) })} disabled={fontSize === 3}>
                    <Plus size={14} strokeWidth={1.75} />
                  </ToolBtn>
                  <ToolBtn
                    label={fontFamily === 'serif' ? 'Switch to sans font' : 'Switch to serif font'}
                    active={fontFamily === 'serif'}
                    onClick={() => setSetting({ fontFamily: fontFamily === 'serif' ? 'sans' : 'serif' })}
                  >
                    <Type size={14} strokeWidth={1.75} />
                  </ToolBtn>
                  <ToolBtn
                    label={focusMode ? 'Turn off focus mode' : 'Turn on focus mode'}
                    active={focusMode}
                    onClick={() => setSetting({ focusMode: !focusMode })}
                  >
                    {focusMode ? <EyeOff size={14} strokeWidth={1.75} /> : <Eye size={14} strokeWidth={1.75} />}
                  </ToolBtn>
                  <ToolBtn
                    label={pdfBusy ? 'Building your PDF…' : 'Download this topic as PDF'}
                    onClick={downloadPdf}
                    disabled={pdfBusy}
                  >
                    {pdfBusy ? <Loader2 size={14} strokeWidth={1.75} className="animate-spin" /> : <Printer size={14} strokeWidth={1.75} />}
                  </ToolBtn>
                </div>
                <p className="flex items-center gap-1 text-[10px] text-faint">
                  <kbd className="kbd">J</kbd>
                  <kbd className="kbd">K</kbd>
                </p>
              </div>
              <div className="mt-2.5 flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setAllSpec(true)}
                  className="mono flex flex-1 items-center justify-center gap-1.5 rounded-lg border border-line px-2 py-2 text-[10.5px] uppercase tracking-[0.12em] text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc"
                >
                  <ChevronsUpDown size={12} strokeWidth={1.75} />
                  Expand all
                </button>
                <button
                  type="button"
                  onClick={() => setAllSpec(false)}
                  className="mono flex flex-1 items-center justify-center gap-1.5 rounded-lg border border-line px-2 py-2 text-[10.5px] uppercase tracking-[0.12em] text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc"
                >
                  <ChevronsDownUp size={12} strokeWidth={1.75} />
                  Collapse all
                </button>
              </div>
              <button
                onClick={() => {
                  setTocOpen(false)
                  go(`/deck/${slug}`)
                }}
                className="mt-2.5 flex w-full items-center gap-3 rounded-xl border border-line px-3 py-2.5 text-left t-fast hover:border-acc/40 hover:bg-elev focus-visible:outline-acc"
              >
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-line text-muted">
                  <Layers3 size={14} strokeWidth={1.75} />
                </span>
                <span>
                  <span className="block text-[12.5px] font-medium text-fg">Flashcard deck</span>
                  <span className="mono block text-[10px] text-faint">{topic.cards.length} cards · graded</span>
                </span>
              </button>
            </div>
          </div>
        )}
        <button
          type="button"
          onClick={() => setTocOpen((o) => !o)}
          aria-expanded={tocOpen}
          aria-label={tocOpen ? 'Close section contents' : 'Open section contents'}
          className="relative flex h-12 w-12 items-center justify-center rounded-full bg-acc text-on-acc shadow-xl t-fast hover:opacity-90 focus-visible:outline-acc"
        >
          {tocOpen ? <X size={18} strokeWidth={2} /> : <ListTree size={18} strokeWidth={1.9} />}
          {!tocOpen && unread > 0 && (
            <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full border-2 border-bg bg-fg px-1 text-[10px] font-bold leading-none text-bg">
              {unread}
            </span>
          )}
        </button>
      </div>
    </>
  )

  /* ---------- body layout per interface ---------- */

  let body: React.ReactNode
  if (mode === 'lab') {
    body = (
      <div className="mt-12 grid gap-10 lg:grid-cols-[minmax(0,1fr)_230px] xl:grid-cols-[minmax(0,1fr)_230px_56px] xl:gap-12">
        {mobileContents}
        <div ref={streamRef} className="min-w-0">
          {topic.sections.map((s, si) => (
            <TopicSection
              key={s.sectionKey}
              s={s}
              si={si}
              slug={slug}
              cardCount={topic.cards.length}
              isRead={!!readMap[`${slug}/${s.sectionKey}`]}
              showOutline={showOutline}
              onToggle={() =>
                readMap[`${slug}/${s.sectionKey}`]
                  ? markUnread(slug, s.sectionKey)
                  : markRead(slug, s.sectionKey)
              }
              onDeck={() => go(`/deck/${slug}`)}
            />
          ))}
          <EndPanel cls={endPanelCls} topic={topic} go={go} />
          <PagerNav prev={prev} next={next} go={go} />
        </div>
        <aside className="hidden lg:block print:hidden">{tocLab}</aside>
        <aside className="hidden xl:block print:hidden" aria-label="Reading tools">{toolsRail}</aside>
      </div>
    )
  } else {
    /* TERMINAL — warm reading room: centered stream, floating contents */
    body = (
      <div className="mt-12">
        <div ref={streamRef} className="stream-warm mx-auto w-full max-w-[var(--content-max)]">
          {topic.sections.map((s, si) => (
            <TopicSection
              key={s.sectionKey}
              s={s}
              si={si}
              slug={slug}
              cardCount={topic.cards.length}
              isRead={!!readMap[`${slug}/${s.sectionKey}`]}
              showOutline={showOutline}
              variant="warm"
              onToggle={() =>
                readMap[`${slug}/${s.sectionKey}`]
                  ? markUnread(slug, s.sectionKey)
                  : markRead(slug, s.sectionKey)
              }
              onDeck={() => go(`/deck/${slug}`)}
            />
          ))}
          <EndPanel cls={endPanelCls} topic={topic} go={go} />
          <PagerNav prev={prev} next={next} go={go} />
        </div>
      </div>
    )
  }

  return (
    <div className="relative">
      <div className="read-progress print:hidden" style={{ width: `${progress}%` }} aria-hidden />
      <div className="mx-auto max-w-[1120px] px-5 pb-24 pt-8 sm:px-8 sm:pt-10">
        {crumb}
        {masthead}
        {body}
      </div>
      {floatingToc}
      {mode === 'lab' && (
        <button
          type="button"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          aria-label="Back to top"
          aria-hidden={!showTop}
          tabIndex={showTop ? 0 : -1}
          className={`lab-glass fixed bottom-5 left-5 z-40 flex h-11 w-11 items-center justify-center rounded-full text-muted t-fast hover:text-acc focus-visible:outline-acc print:hidden ${
            showTop ? 'opacity-100' : 'pointer-events-none opacity-0'
          }`}
        >
          <ArrowUp size={16} strokeWidth={1.75} />
        </button>
      )}
    </div>
  )
}

/* ──────────────────────────────────────────────────────────── */

function EndPanel({ cls, topic, go }: { cls: string; topic: TopicData; go: (to: string) => void }) {
  return (
    <section className={`mt-16 overflow-hidden ${cls}`} aria-label="End of topic">
      <div className="px-6 py-10 text-center sm:px-10">
        <p className="kicker">End of topic {pad(topic.number)}</p>
        <h3 className="display-serif mt-3 text-[clamp(24px,2.6vw,30px)] leading-tight text-fg">
          Ready to make it stick?
        </h3>
        <p className="mx-auto mt-3 max-w-md text-[14px] leading-relaxed text-muted">
          Reading shows you the shape of it — recall proves you own it.
          {topic.cards.length > 0 && ` Grind ${topic.cards.length} flashcards and find out.`}
        </p>
        <div className="mt-7 flex flex-wrap items-center justify-center gap-3 print:hidden">
          <BtnSolid onClick={() => go(`/deck/${slugOf(topic)}`)}>
            <Layers3 size={14} />
            Open the deck
          </BtnSolid>
          <BtnGhost onClick={() => go('/topics')}>All topics</BtnGhost>
        </div>
      </div>
    </section>
  )
}

const slugOf = (t: TopicData) => t.slug

function PagerNav({
  prev, next, go,
}: {
  prev: TopicData | null
  next: TopicData | null
  go: (to: string) => void
}) {
  return (
    <nav className="mt-6 grid gap-3 print:hidden sm:grid-cols-2" aria-label="More topics">
      {prev ? (
        <PagerCard dir="prev" num={prev.number} title={prev.title} slug={prev.slug} go={go} />
      ) : (
        <div className="hidden sm:block" aria-hidden />
      )}
      {next ? (
        <PagerCard dir="next" num={next.number} title={next.title} slug={next.slug} go={go} />
      ) : (
        <div className="flex flex-col items-start justify-center gap-2 rounded-xl border border-dashed border-line p-5 sm:items-end sm:text-right">
          <span className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-faint">
            Syllabus complete
          </span>
          <span className="text-[13px] text-muted">That was the last of the ten topics.</span>
        </div>
      )}
    </nav>
  )
}

function TopicSection({
  s, si, slug, cardCount, isRead, showOutline, onToggle, onDeck, variant = 'default',
}: {
  s: SectionData
  si: number
  slug: string
  cardCount: number
  isRead: boolean
  showOutline: boolean
  onToggle: () => void
  onDeck: () => void
  variant?: 'default' | 'warm'
}) {
  const [copied, setCopied] = useState(false)
  const leadIsP = !!s.content && s.content.length > 0 && s.content[0].type === 'p'
  const warm = variant === 'warm'

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(`${window.location.origin}/#/topic/${slug}/${s.sectionKey}`)
    } catch {
      // clipboard may be unavailable; still show feedback
    }
    setCopied(true)
    setTimeout(() => setCopied(false), 1400)
  }

  return (
    <section
      id={`sec-${s.sectionKey}`}
      aria-labelledby={`sec-${s.sectionKey}-title`}
      className={`scroll-mt-24 ${si > 0 ? 'mt-14 border-t border-line pt-14' : ''}`}
    >
      <div className="group/sec sec-head">
        <span aria-hidden className="sec-giant">{s.number}</span>
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            {warm ? (
              <>
                <span aria-hidden className="warm-dash block" />
                <p className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-1.5">
                  <span className="mono text-[15px] font-bold tracking-tight text-acc">{s.number}</span>
                  <span aria-hidden className="h-3 w-px bg-line-strong" />
                  <span className="mono inline-flex items-center gap-1.5 text-[10.5px] uppercase tracking-[0.16em] text-faint">
                    <Clock3 size={11} strokeWidth={1.75} />
                    {s.estMinutes} min
                  </span>
                  {isRead && (
                    <span className="mono inline-flex items-center gap-1 text-[10px] uppercase tracking-[0.14em] text-acc">
                      <Check size={11} strokeWidth={2.5} /> read
                    </span>
                  )}
                </p>
              </>
            ) : (
              <p className="sec-kicker mono flex flex-wrap items-center gap-2 text-[10.5px] font-medium uppercase tracking-[0.18em] text-faint">
                <span className="sec-no text-acc">Section {s.number}</span>
                {s.spec && (
                  <span
                    className="rounded border border-acc/30 bg-acc/10 px-1.5 py-0.5 text-[9.5px] tracking-[0.14em] text-acc"
                    title="Edexcel specification point covered by this section"
                  >
                    Spec {s.spec}
                  </span>
                )}
                <span aria-hidden className="h-px w-4 bg-line-strong" />
                <Clock3 size={11} strokeWidth={1.75} />
                {s.estMinutes} min read
                {isRead && (
                  <span className="inline-flex items-center gap-1 text-acc">
                    <Check size={11} strokeWidth={2.5} /> read
                  </span>
                )}
              </p>
            )}
            <h2 id={`sec-${s.sectionKey}-title`} className="display-serif mt-3 text-[clamp(25px,2.8vw,31px)] leading-[1.15] text-fg">
              {s.title}
            </h2>
            <p className="mt-2 max-w-[52ch] text-[14.5px] leading-relaxed text-muted text-pretty">{s.blurb}</p>
          </div>

          <div className="flex shrink-0 flex-col items-end gap-2 print:hidden sm:flex-row sm:items-center">
            <button
              type="button"
              onClick={copyLink}
              aria-label={copied ? 'Section link copied' : `Copy link to section ${s.number}`}
              title="Copy link to this section"
              className="inline-flex h-8 w-8 items-center justify-center rounded-full text-faint opacity-0 t-fast hover:bg-elev hover:text-fg focus-visible:opacity-100 focus-visible:outline-acc group-hover/sec:opacity-100 max-sm:opacity-100"
            >
              {copied ? <Check size={13} className="text-acc" /> : <Link2 size={13} />}
            </button>
            <ReadPill read={isRead} onToggle={onToggle} sectionNumber={s.number} />
          </div>
        </div>

        {/* collapsible specification point — the statement itself, written as the spec writes it */}
        {variant === 'warm' && showOutline && (s.spec || s.outline.length > 0) && (
          s.specText && s.outline.length === 0 ? (
            /* single-statement spec point — the full statement sits on the bar, nothing hidden */
            <div className="spec-point spec-point-flat mt-6" aria-label={`Specification point ${s.spec}: ${s.specText}`}>
              <div className="spec-point-summary">
                <div className="spec-point-head">
                  <span className="spec-point-label">Specification point {s.spec}</span>
                  <span className="spec-point-statement text-pretty"><Inline text={s.specText} /></span>
                </div>
              </div>
            </div>
          ) : (
            <details className="spec-point mt-6">
              <summary className="focus-visible:outline-acc">
                <div className="spec-point-head">
                  <span className="spec-point-label">
                    {s.spec
                      ? `Specification ${/[,–]/.test(s.spec) ? 'points' : 'point'} ${s.spec}`
                      : 'Specification outline'}
                  </span>
                  {s.specText && (
                    <span className="spec-point-statement text-pretty"><Inline text={s.specText} /></span>
                  )}
                </div>
                <ChevronDown size={15} strokeWidth={1.75} aria-hidden className="spec-caret" />
              </summary>
              <div className="spec-point-body">
                {s.outline.map((o, i) => (
                  <p key={i} className="spec-outline-item">
                    <Inline text={o} />
                  </p>
                ))}
              </div>
            </details>
          )
        )}

        {s.content ? (
          <div className="reading mt-7 space-y-5">
            {variant === 'warm'
              ? groupBlocks(s.content).map((seg, segI) =>
                  seg.kind === 'group' ? (
                    <BulletCard key={segI} blocks={seg.blocks} />
                  ) : (
                    <BlockRenderer key={segI} block={seg.block} lead={segI === 0 && leadIsP} />
                  )
                )
              : s.content.map((b, bi) => (
                  <BlockRenderer key={bi} block={b} lead={bi === 0 && leadIsP} />
                ))}
          </div>
        ) : (
          <div className="mt-7 rounded-2xl border border-dashed border-line-strong bg-surface/50 px-6 py-7 sm:px-8">
            <div className="flex items-center gap-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-acc/30 bg-acc/10 text-acc">
                <BookOpen size={15} strokeWidth={1.75} />
              </span>
              <p className="text-[14px] font-medium text-fg">
                Full notes for this section are on the way
              </p>
            </div>
            <p className="mt-3 text-[13.5px] leading-relaxed text-muted">
              {variant === 'warm'
                ? 'They’re being written right now — the specification outline above lists exactly what they will cover.'
                : 'They’re being written right now. Meanwhile, this is exactly what the specification expects you to master:'}
            </p>
            {variant !== 'warm' && showOutline && (
              <ul className="mt-5 space-y-3 border-t border-line pt-5">
                {s.outline.map((o, i) => (
                  <li key={i} className="flex gap-3.5 text-[13.5px] leading-relaxed text-muted">
                    <span className="mono shrink-0 pt-px text-[11px] font-medium text-acc">
                      {s.number}.{i + 1}
                    </span>
                    <span className="min-w-0 flex-1"><Inline text={o} /></span>
                  </li>
                ))}
              </ul>
            )}
            {cardCount > 0 && (
              <button
                onClick={onDeck}
                className="mono mt-6 inline-flex items-center gap-2 rounded-md text-[11px] font-medium uppercase tracking-[0.14em] text-acc t-fast hover:opacity-80 focus-visible:outline-acc"
              >
                Practise with {cardCount} flashcards
                <ArrowRight size={13} />
              </button>
            )}
          </div>
        )}
      </div>
    </section>
  )
}

/* ── small pieces ─────────────────────────────────────────── */

function ReadPill({ read, onToggle, sectionNumber }: { read: boolean; onToggle: () => void; sectionNumber: string }) {
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={read}
      aria-label={`Mark section ${sectionNumber} as ${read ? 'not read' : 'read'}`}
      onClick={onToggle}
      className={`inline-flex h-8 shrink-0 items-center gap-1.5 rounded-full border px-3.5 text-[12px] font-medium t-fast focus-visible:outline-acc ${
        read
          ? 'border-acc/40 bg-acc/10 text-acc'
          : 'border-line text-muted hover:border-line-strong hover:text-fg'
      }`}
    >
      <CheckCircle2 size={14} strokeWidth={read ? 2 : 1.75} className="shrink-0" />
      {read ? 'Read' : 'Mark read'}
    </button>
  )
}

function ToolBtn({
  label, onClick, children, active = false, disabled = false,
}: {
  label: string
  onClick: () => void
  children: React.ReactNode
  active?: boolean
  disabled?: boolean
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={label}
      aria-label={label}
      aria-pressed={active}
      disabled={disabled}
      className={`flex h-9 w-9 items-center justify-center rounded-lg border t-fast focus-visible:outline-acc disabled:pointer-events-none disabled:opacity-35 ${
        active
          ? 'border-acc/40 bg-acc/10 text-acc'
          : 'border-line bg-bg text-muted hover:border-line-strong hover:text-fg'
      }`}
    >
      {children}
    </button>
  )
}

function PagerCard({
  dir, num, title, slug, go,
}: {
  dir: 'prev' | 'next'
  num: number
  title: string
  slug: string
  go: (to: string) => void
}) {
  const isPrev = dir === 'prev'
  return (
    <button
      onClick={() => go(`/topic/${slug}`)}
      className={`pager-card group flex flex-col gap-2.5 rounded-xl border border-line bg-bg p-5 t-fast hover:border-acc/40 hover:bg-elev focus-visible:outline-acc ${
        isPrev ? 'items-start text-left' : 'items-start text-left sm:items-end sm:text-right'
      }`}
    >
      <span className="mono flex items-center gap-2 text-[10px] font-medium uppercase tracking-[0.18em] text-faint">
        {isPrev ? (
          <>
            <ArrowLeft size={12} className="t-fast group-hover:-translate-x-0.5 group-hover:text-acc" />
            Previous · Topic {pad(num)}
          </>
        ) : (
          <>
            Next · Topic {pad(num)}
            <ArrowRight size={12} className="t-fast group-hover:translate-x-0.5 group-hover:text-acc" />
          </>
        )}
      </span>
      <span className="display-serif text-[17px] leading-snug text-fg t-fast group-hover:text-acc">
        {title}
      </span>
    </button>
  )
}
