'use client'

import React, { useEffect, useId, useLayoutEffect, useRef, useState } from 'react'
import { ArrowUpRight, Menu, Search, SlidersHorizontal, X } from 'lucide-react'
import { useRoute, type Route } from '@/lib/site/router'
import {
  useUi, useSettings, useProgress, applySettingsToDom,
  UI_MODES, type UiMode,
} from '@/lib/site/stores'
import type { TopicData } from '@/lib/site/types'

const LINKS: { label: string; to: string; match: (r: Route) => boolean }[] = [
  { label: 'Topics', to: '/topics', match: (r) => r.name === 'topics' || r.name === 'topic' },
  { label: 'Flashcards', to: '/flashcards', match: (r) => r.name === 'flashcards' || r.name === 'deck' },
  { label: 'Progress', to: '/progress', match: (r) => r.name === 'progress' },
]

const isoLayout = typeof window !== 'undefined' ? useLayoutEffect : useEffect

function setUiMode(m: UiMode) {
  useSettings.getState().set({ uiMode: m })
  applySettingsToDom(useSettings.getState())
}

/* ============================================================
   SCROLL INTENT — condensed when scrolled, tucks away when
   reading (scroll down), returns the moment you scroll up.
   ============================================================ */

function useScrollIntent(blockHide: boolean) {
  const [scrolled, setScrolled] = useState(false)
  const [hidden, setHidden] = useState(false)

  useEffect(() => {
    let lastY = window.scrollY
    let raf = 0
    const onScroll = () => {
      if (raf) return
      raf = requestAnimationFrame(() => {
        raf = 0
        const y = window.scrollY
        setScrolled(y > 18)
        if (document.documentElement.dataset.motion === 'reduced') {
          setHidden(false)
        } else if (y <= 320) {
          setHidden(false)
        } else {
          const dy = y - lastY
          if (dy > 8) setHidden(true)
          else if (dy < -8) setHidden(false)
        }
        lastY = y
      })
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', onScroll)
      if (raf) cancelAnimationFrame(raf)
    }
  }, [])

  return { scrolled, hide: hidden && !blockHide }
}

/* ============================================================
   SLIDING INDICATOR — measures the active link and slides a
   marker beneath it. Fresh mounts fade in instead of sliding.
   ============================================================ */

function useSlideIndicator(ref: React.RefObject<HTMLElement | null>, activeKey: string) {
  const [box, setBox] = useState<{ left: number; width: number } | null>(null)

  /* isoLayout is useLayoutEffect on the client — the ref read below is
     effect-phase, but the conditional alias hides that from the linter. */
  // eslint-disable-next-line react-hooks/refs
  isoLayout(() => {
    const root = ref.current
    if (!root) return
    const el = root.querySelector<HTMLElement>('[data-nav-active="true"]')
    if (!el) {
      setBox(null)
      return
    }
    const measure = () => setBox({ left: el.offsetLeft, width: el.offsetWidth })
    measure()
    let ro: ResizeObserver | undefined
    if (typeof ResizeObserver !== 'undefined') {
      ro = new ResizeObserver(measure)
      ro.observe(el)
      ro.observe(root)
    }
    const fonts = (document as Document & { fonts?: { ready?: Promise<unknown> } }).fonts
    fonts?.ready?.then(() => measure()).catch(() => {})
    return () => ro?.disconnect()
  }, [activeKey])

  return box
}

/* ============================================================
   BRAND — benzene hexagon mark + wordmark (per interface)
   ============================================================ */

function HexMark({ lab = false, size = 20, hover = false }: { lab?: boolean; size?: number; hover?: boolean }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden
      className={hover ? 'shrink-0 transition-transform duration-500 ease-out group-hover:rotate-[120deg]' : 'shrink-0'}
      style={lab ? { filter: 'drop-shadow(0 0 7px color-mix(in srgb, var(--acc) 55%, transparent))' } : undefined}
    >
      <path d="M12 2.7 20 7.35v9.3L12 21.3 4 16.65v-9.3L12 2.7Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
      <circle cx="12" cy="12" r="3.1" fill="var(--acc)" />
    </svg>
  )
}

function Brand({ mode }: { mode: string }) {
  const glass = mode !== 'terminal'
  return (
    <span className="nav-brand flex items-center gap-2.5 text-[13px] text-fg">
      <HexMark lab={glass} size={20} hover />
      {mode === 'lab' ? (
        <span className="font-semibold tracking-[0.04em]" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
          IAL&nbsp;STUDIO
        </span>
      ) : mode === 'hybrid' ? (
        <span className="font-semibold tracking-[0.04em]" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>
          IAL&nbsp;HYBRID
        </span>
      ) : (
        <span className="mono text-[13px] font-semibold tracking-[0.08em]">
          IAL<span className="text-acc">{'//'}</span>CHEM
        </span>
      )}
    </span>
  )
}

/* ============================================================
   PROGRESS DIAL — live revision ring wired to the read store
   ============================================================ */

function ProgressDial({
  total, lab, go, className = '',
}: {
  total: number
  lab: boolean
  go: (to: string) => void
  className?: string
}) {
  const read = useProgress((s) => s.read)
  const done = Object.keys(read).length
  const pct = total > 0 ? Math.min(100, Math.round((done / total) * 100)) : 0
  const R = 11
  const C = 2 * Math.PI * R
  const gid = useId().replace(/:/g, '')

  return (
    <button
      onClick={() => go('/progress')}
      aria-label={`Revision progress — ${pct}% of ${total} sections read. Open progress.`}
      title={`${done} of ${total} sections read — open progress`}
      className={
        (lab
          ? 'flex h-9 items-center gap-1.5 rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] px-2 t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc'
          : 'flex h-9 items-center gap-1.5 rounded-lg border border-line px-2 t-fast hover:border-acc focus-visible:outline-acc') +
        ' ' + className
      }
    >
      <svg width="22" height="22" viewBox="0 0 26 26" aria-hidden>
        {lab && (
          <defs>
            <linearGradient id={`dial-${gid}`} x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="var(--acc)" />
              <stop offset="100%" stopColor="#38d5ee" />
            </linearGradient>
          </defs>
        )}
        <circle cx="13" cy="13" r={R} fill="none" stroke="var(--line-strong)" strokeWidth="2.4" />
        <circle
          cx="13" cy="13" r={R} fill="none"
          stroke={lab ? `url(#dial-${gid})` : 'var(--acc)'}
          strokeWidth="2.4" strokeLinecap="round"
          strokeDasharray={C} strokeDashoffset={C * (1 - pct / 100)}
          transform="rotate(-90 13 13)"
          style={{ transition: 'stroke-dashoffset 700ms cubic-bezier(0.2, 0.7, 0.2, 1)' }}
        />
      </svg>
      <span className="mono hidden text-[10px] tabular-nums tracking-[0.06em] text-muted sm:inline">{pct}%</span>
    </button>
  )
}

/* ============================================================
   MODE SEGMENT — Focus | Studio | Hybrid with a sliding thumb
   ============================================================ */

function ModeSegment({ lab, className = '' }: { lab: boolean; className?: string }) {
  const mode = useSettings((s) => s.uiMode)
  const idx = UI_MODES.findIndex((m) => m.value === mode)
  return (
    <div
      role="group"
      aria-label="Interface"
      className={`relative grid grid-cols-3 ${lab
        ? 'rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] p-[3px]'
        : 'rounded-lg border border-line p-[3px]'} ${className}`}
    >
      <span
        aria-hidden
        className="absolute inset-y-[3px] left-[3px] w-[calc(33.333%-2px)] rounded-full t-fast"
        style={{
          transform: `translateX(${Math.max(0, idx) * 100}%)`,
          background: lab ? 'var(--glass-bg-strong)' : 'color-mix(in srgb, var(--acc) 16%, transparent)',
        }}
      />
      {UI_MODES.map((m) => (
        <button
          key={m.value}
          onClick={() => setUiMode(m.value)}
          aria-pressed={mode === m.value}
          title={`Interface: ${m.label}`}
          className={`relative z-10 px-2 py-1 t-fast ${lab
            ? 'text-[10px] font-semibold tracking-[0.02em]'
            : 'mono text-[9px] uppercase tracking-[0.1em]'} ${mode === m.value ? 'text-acc' : 'text-muted hover:text-fg'}`}
        >
          {m.label}
        </button>
      ))}
    </div>
  )
}

/* ============================================================
   TOPIC CHIP — orientation while deep inside a topic
   ============================================================ */

function TopicChip({ topic, lab }: { topic: TopicData | undefined; lab: boolean }) {
  if (!topic) return null
  return (
    <button
      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      title="Back to the top of this topic"
      aria-label={`Reading topic ${topic.number}: ${topic.title} — back to top`}
      className={`ml-2 hidden max-w-[240px] min-w-0 items-center gap-2 t-fast focus-visible:outline-acc xl:flex ${lab
        ? 'rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] py-1.5 pl-2.5 pr-3 hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)]'
        : 'rounded-md border border-line py-1.5 pl-2.5 pr-3 hover:border-line-strong'}`}
    >
      <span className="mono shrink-0 text-[10px] font-semibold tracking-[0.1em] text-acc">
        T{String(topic.number).padStart(2, '0')}
      </span>
      <span className="mono min-w-0 truncate text-[10px] uppercase tracking-[0.14em] text-muted">
        {topic.title}
      </span>
    </button>
  )
}

/* ============================================================
   FULL-SCREEN MENU (mobile) — big links, topic jump grid,
   mode switch + search. Esc closes, scroll is locked.
   ============================================================ */

function MobileMenu({
  open, onClose, route, topics, total, go, mode,
}: {
  open: boolean
  onClose: () => void
  route: Route
  topics: TopicData[]
  total: number
  go: (to: string) => void
  mode: 'terminal' | 'lab' | 'hybrid'
}) {
  const read = useProgress((s) => s.read)
  const openPalette = useUi((s) => s.setPalette)
  const lab = mode !== 'terminal'

  useEffect(() => {
    if (!open) return
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = prev
      window.removeEventListener('keydown', onKey)
    }
  }, [open, onClose])

  if (!open) return null

  const done = Object.keys(read).length
  const hair = lab ? 'border-[color-mix(in_srgb,var(--fg)_10%,transparent)]' : 'border-line'

  const pages = [
    { label: 'Topics', to: '/topics', active: route.name === 'topics' || route.name === 'topic' },
    { label: 'Flashcards', to: '/flashcards', active: route.name === 'flashcards' || route.name === 'deck' },
    { label: 'Progress', to: '/progress', active: route.name === 'progress' },
    { label: 'Control room', to: '/settings', active: route.name === 'settings' },
  ]

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Site menu"
      className={`menu-fade fixed inset-0 z-[60] flex flex-col print:hidden ${lab ? 'menu-glass' : 'bg-[var(--bg)] dotgrid'}`}
    >
      <div className={`flex h-14 shrink-0 items-center justify-between border-b px-5 sm:px-6 ${hair}`}>
        <Brand mode={mode} />
        <button
          autoFocus
          onClick={onClose}
          aria-label="Close menu"
          className={`flex h-9 w-9 items-center justify-center t-fast focus-visible:outline-acc ${lab
            ? 'rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-muted hover:text-acc'
            : 'rounded-lg border border-line text-muted hover:border-acc hover:text-acc'}`}
        >
          <X size={15} />
        </button>
      </div>

      <div className="mx-auto w-full max-w-[620px] flex-1 overflow-y-auto px-6 pb-12 pt-8">
        <nav aria-label="Menu">
          {pages.map((p, i) => (
            <a
              key={p.to}
              href={`#${p.to}`}
              onClick={(e) => { e.preventDefault(); go(p.to); onClose() }}
              aria-current={p.active ? 'page' : undefined}
              className="menu-rise group flex items-baseline gap-4 py-3"
              style={{ animationDelay: `${90 + i * 65}ms` }}
            >
              <span className="mono text-[11px] text-faint">0{i + 1}</span>
              <span
                className={`t-fast ${p.active ? 'text-acc' : 'text-fg group-hover:text-acc'} ${lab
                  ? 'text-[26px] font-bold tracking-[-0.02em]'
                  : 'display-serif text-[30px]'}`}
                style={lab ? { fontFamily: 'var(--font-grotesk), sans-serif' } : undefined}
              >
                {p.label}
              </span>
              <ArrowUpRight size={16} className="ml-auto self-center text-faint opacity-0 t-fast group-hover:text-acc group-hover:opacity-100" />
            </a>
          ))}
        </nav>

        <div className={`menu-rise mt-5 flex items-center gap-3 border-t pt-5 ${hair}`} style={{ animationDelay: '370ms' }}>
          <span aria-hidden className="h-2 w-2 rounded-full bg-acc" style={{ boxShadow: '0 0 12px 2px color-mix(in srgb, var(--acc) 65%, transparent)' }} />
          <p className="mono text-[10.5px] uppercase tracking-[0.16em] text-faint">
            {done} / {total} sections read
          </p>
          <button
            onClick={() => { onClose(); go('/progress') }}
            className="mono ml-auto text-[10.5px] uppercase tracking-[0.16em] text-muted t-fast hover:text-acc focus-visible:outline-acc"
          >
            Open progress →
          </button>
        </div>

        <p className="eyebrow menu-rise mb-1 mt-9" style={{ animationDelay: '430ms' }}>
          Jump to a topic
        </p>
        <div className="grid gap-x-8 sm:grid-cols-2">
          {topics.map((t, i) => (
            <a
              key={t.slug}
              href={`#/topic/${t.slug}`}
              onClick={(e) => { e.preventDefault(); go(`/topic/${t.slug}`); onClose() }}
              className={`menu-rise group flex items-baseline gap-3 border-t py-2.5 ${hair}`}
              style={{ animationDelay: `${470 + i * 28}ms` }}
            >
              <span className="mono shrink-0 text-[10px] font-semibold text-acc">
                {String(t.number).padStart(2, '0')}
              </span>
              <span className="min-w-0 truncate text-[13px] text-muted t-fast group-hover:text-fg">
                {t.title}
              </span>
            </a>
          ))}
        </div>

        <div className="menu-rise mt-10 flex flex-wrap items-center justify-between gap-3" style={{ animationDelay: '820ms' }}>
          <ModeSegment lab={lab} />
          <button
            onClick={() => { onClose(); openPalette(true) }}
            aria-label="Search notes"
            className={`flex items-center gap-2 px-3 py-2 text-muted t-fast hover:text-acc focus-visible:outline-acc ${lab
              ? 'rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-[11px] font-semibold'
              : 'rounded-lg border border-line mono text-[10.5px] uppercase tracking-[0.14em]'}`}
            style={lab ? { fontFamily: 'var(--font-grotesk), sans-serif' } : undefined}
          >
            <Search size={13} />
            Search notes
            <kbd className="kbd">/</kbd>
          </button>
        </div>
      </div>
    </div>
  )
}

/* ============================================================
   NAV — TERMINAL (the control deck)
   Transparent at rest, frosted hairline when scrolled,
   tucks away while you read, returns when you look up.
   ============================================================ */

function TerminalNav({ route, topics, total }: { route: Route; topics: TopicData[]; total: number }) {
  const openPalette = useUi((s) => s.setPalette)
  const openSettings = useUi((s) => s.openSettings)
  const [menuOpen, setMenuOpen] = useState(false)
  const [, go] = useRoute()
  const mode = useSettings((s) => s.uiMode)
  const { scrolled, hide } = useScrollIntent(menuOpen)
  const topic = route.name === 'topic' ? topics.find((t) => t.slug === route.slug) : undefined

  const [prevPath, setPrevPath] = useState<string | null>(null)
  const pathKey = `${route.name}:${route.slug ?? ''}`
  if (prevPath !== pathKey) {
    setPrevPath(pathKey)
    if (menuOpen) setMenuOpen(false)
  }

  const groupRef = useRef<HTMLDivElement>(null)
  const activeIdx = LINKS.findIndex((l) => l.match(route))
  const box = useSlideIndicator(groupRef, String(activeIdx))

  return (
    <>
      <header
        className={`nav-root menu-fade sticky top-0 z-50 border-b print:hidden ${hide ? 'nav-is-hidden' : ''} ${scrolled
          ? 'border-line bg-[var(--nav-bg)] shadow-[0_12px_44px_-26px_rgba(0,0,0,0.65)] backdrop-blur-md'
          : 'border-transparent bg-transparent'}`}
        style={{ animationDelay: '40ms' }}
      >
        <div className="mx-auto flex h-14 max-w-[1200px] items-center gap-2 px-4 sm:px-6">
          <a
            href="#/"
            onClick={(e) => { e.preventDefault(); go('/') }}
            className="group flex shrink-0 items-center focus-visible:outline-acc"
            aria-label="IAL CHEM home"
          >
            <Brand mode={mode} />
          </a>

          <TopicChip topic={topic} lab={false} />

          <nav ref={groupRef} aria-label="Primary" className="relative ml-3 hidden h-full items-center gap-1 md:flex">
            {LINKS.map((l) => {
              const active = l.match(route)
              return (
                <a
                  key={l.to}
                  href={`#${l.to}`}
                  onClick={(e) => { e.preventDefault(); go(l.to) }}
                  aria-current={active ? 'page' : undefined}
                  data-nav-active={active ? 'true' : undefined}
                  className={`mono rounded-md px-2.5 py-1.5 text-[11px] uppercase tracking-[0.16em] t-fast focus-visible:outline-acc ${active ? 'text-fg' : 'text-muted hover:text-fg'}`}
                >
                  {l.label}
                </a>
              )
            })}
            {box && (
              <span
                aria-hidden
                className="nav-ind absolute bottom-0 left-0 h-[2px] rounded-full bg-acc shadow-[0_0_14px_color-mix(in_srgb,var(--acc)_55%,transparent)]"
                style={{ width: box.width, transform: `translateX(${box.left}px)` }}
              />
            )}
          </nav>

          <div className="ml-auto flex items-center gap-1.5 sm:gap-2">
            <button
              onClick={() => openPalette(true)}
              aria-label="Search — Command K"
              className="mono hidden h-9 items-center gap-2 rounded-lg border border-line pl-2.5 pr-1.5 text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc lg:flex"
            >
              <Search size={13} />
              <span className="text-[10px] uppercase tracking-[0.16em]">Search</span>
              <kbd className="kbd">⌘K</kbd>
            </button>
            <button
              onClick={() => openPalette(true)}
              aria-label="Search"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-line text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc lg:hidden"
            >
              <Search size={14} />
            </button>

            <ModeSegment lab={false} className="hidden lg:grid" />

            <ProgressDial total={total} lab={false} go={go} />

            <button
              onClick={openSettings}
              aria-label="Open control room — reading preferences"
              title="Control room"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-line text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc"
            >
              <SlidersHorizontal size={14} />
            </button>

            <button
              onClick={() => setMenuOpen((o) => !o)}
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={menuOpen}
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-line text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc lg:hidden"
            >
              {menuOpen ? <X size={14} /> : <Menu size={14} />}
            </button>
          </div>
        </div>
      </header>

      <MobileMenu
        open={menuOpen}
        onClose={() => setMenuOpen(false)}
        route={route}
        topics={topics}
        total={total}
        go={go}
        mode="terminal"
      />
    </>
  )
}

/* ============================================================
   NAV — GLASS (Studio + Hybrid)
   Floating glass pill with the same scroll intelligence,
   gradient progress dial and glass sliding thumb. Studio and
   Hybrid share the chrome; each wears its own wordmark.
   ============================================================ */

function GlassNav({ route, topics, total, mode }: { route: Route; topics: TopicData[]; total: number; mode: 'lab' | 'hybrid' }) {
  const openPalette = useUi((s) => s.setPalette)
  const openSettings = useUi((s) => s.openSettings)
  const [menuOpen, setMenuOpen] = useState(false)
  const [, go] = useRoute()
  const { scrolled, hide } = useScrollIntent(menuOpen)
  const topic = route.name === 'topic' ? topics.find((t) => t.slug === route.slug) : undefined

  const [prevPath, setPrevPath] = useState<string | null>(null)
  const pathKey = `${route.name}:${route.slug ?? ''}`
  if (prevPath !== pathKey) {
    setPrevPath(pathKey)
    if (menuOpen) setMenuOpen(false)
  }

  const groupRef = useRef<HTMLDivElement>(null)
  const activeIdx = LINKS.findIndex((l) => l.match(route))
  const box = useSlideIndicator(groupRef, String(activeIdx))

  const circle =
    'flex h-9 w-9 items-center justify-center rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-muted t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc'

  return (
    <>
      <div className={`nav-root menu-fade fixed inset-x-0 top-3 z-50 px-3 print:hidden ${hide ? 'nav-is-hidden' : ''}`} style={{ animationDelay: '40ms' }}>
        <nav
          aria-label="Primary"
          className={`lab-nav mx-auto flex h-[56px] max-w-[1080px] items-center gap-2 rounded-full px-3 sm:px-5 ${scrolled ? 'lab-nav-scrolled' : ''}`}
        >
          <a
            href="#/"
            onClick={(e) => { e.preventDefault(); go('/') }}
            className="group flex shrink-0 items-center focus-visible:outline-acc"
            aria-label={mode === 'lab' ? 'IAL Studio — home' : 'IAL Hybrid — home'}
          >
            <Brand mode={mode} />
          </a>

          <TopicChip topic={topic} lab />

          <div ref={groupRef} className="relative ml-1 hidden items-center gap-1 md:flex">
            {LINKS.map((l) => {
              const active = l.match(route)
              return (
                <a
                  key={l.to}
                  href={`#${l.to}`}
                  onClick={(e) => { e.preventDefault(); go(l.to) }}
                  aria-current={active ? 'page' : undefined}
                  data-nav-active={active ? 'true' : undefined}
                  className={`nav-link relative z-10 t-fast ${active ? 'text-acc' : 'text-muted'}`}
                >
                  {l.label}
                </a>
              )
            })}
            {box && (
              <span
                aria-hidden
                className="nav-ind absolute inset-y-[5px] left-0 rounded-full border"
                style={{
                  width: box.width,
                  transform: `translateX(${box.left}px)`,
                  background: 'var(--glass-bg-strong)',
                  borderColor: 'color-mix(in srgb, var(--acc) 38%, transparent)',
                  boxShadow: '0 0 22px -6px color-mix(in srgb, var(--acc) 45%, transparent)',
                }}
              />
            )}
          </div>

          <div className="ml-auto flex items-center gap-1.5">
            <button onClick={() => openPalette(true)} aria-label="Search" className={circle}>
              <Search size={14} />
            </button>
            <ModeSegment lab className="hidden lg:grid" />
            <ProgressDial total={total} lab go={go} />
            <button
              onClick={openSettings}
              aria-label="Open control room — reading preferences"
              title="Control room"
              className={circle}
            >
              <SlidersHorizontal size={14} />
            </button>
            <button
              onClick={() => setMenuOpen((o) => !o)}
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
              aria-expanded={menuOpen}
              className={`${circle} lg:hidden`}
            >
              {menuOpen ? <X size={14} /> : <Menu size={14} />}
            </button>
          </div>
        </nav>
      </div>

      <MobileMenu
        open={menuOpen}
        onClose={() => setMenuOpen(false)}
        route={route}
        topics={topics}
        total={total}
        go={go}
        mode={mode}
      />
    </>
  )
}

export function Nav({
  route, topics, total,
}: {
  route: Route
  topics: TopicData[]
  total: number
}) {
  const mode = useSettings((s) => s.uiMode)
  if (mode === 'terminal') return <TerminalNav route={route} topics={topics} total={total} />
  return <GlassNav route={route} topics={topics} total={total} mode={mode} />
}

/* ============================================================
   FOOTERS — three colophons
   ============================================================ */

function TerminalFooter({ go }: { go: (to: string) => void }) {
  const mode = useSettings((s) => s.uiMode)
  return (
    <footer className="mt-auto border-t border-line print:hidden">
      <div className="mx-auto grid max-w-[1200px] gap-10 px-6 py-12 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <div className="flex items-center gap-2.5">
            <HexMark lab={false} size={22} />
            <Brand mode={mode} />
          </div>
          <p className="mt-4 max-w-sm text-[13px] leading-relaxed text-muted">
            Exam-focused notes for Pearson Edexcel International A Level Chemistry —
            the 2018 specification, topics 1–10 (WCH11 + WCH12).
          </p>
          <p className="mono mt-4 text-[10px] leading-relaxed text-faint">
            {'// independent study tool · not affiliated with or endorsed by Pearson Edexcel'}
          </p>
        </div>
        <div>
          <p className="mono mb-4 text-[10px] uppercase tracking-[0.2em] text-faint">Site</p>
          <ul className="space-y-2.5">
            {[['Topics', '/topics'], ['Flashcards', '/flashcards'], ['Progress', '/progress'], ['Control room', '/settings']].map(([label, to]) => (
              <li key={to}>
                <a href={`#${to}`} onClick={(e) => { e.preventDefault(); go(to) }} className="mono text-[12px] text-muted t-fast hover:text-acc focus-visible:outline-acc">
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <p className="mono mb-4 text-[10px] uppercase tracking-[0.2em] text-faint">Syllabus</p>
          <ul className="space-y-2.5">
            {[['Unit 1 — WCH11', '/topics'], ['Unit 2 — WCH12', '/topics'], ['Topic 01 notes', '/topic/amount-of-substance']].map(([label, to]) => (
              <li key={label}>
                <a href={`#${to}`} onClick={(e) => { e.preventDefault(); go(to) }} className="mono text-[12px] text-muted t-fast hover:text-acc focus-visible:outline-acc">
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="border-t border-line">
        <div className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-2 px-6 py-4">
          <p className="mono text-[10px] uppercase tracking-[0.16em] text-faint">© {new Date().getFullYear()} ial//chem — built for revision</p>
          <p className="mono text-[10px] uppercase tracking-[0.16em] text-faint">your data stays in your browser</p>
        </div>
      </div>
    </footer>
  )
}

function LabFooter({ go }: { go: (to: string) => void }) {
  return (
    <footer className="mt-auto px-3 pb-6 print:hidden sm:px-6">
      <div className="lab-footer mx-auto max-w-[1080px] rounded-[26px] px-7 py-9 sm:px-10">
        <div className="grid gap-8 md:grid-cols-[1.4fr_1fr]">
          <div>
            <div className="flex items-center gap-2.5">
              <HexMark lab size={22} />
              <span className="nav-brand text-[13px] text-fg">IAL&nbsp;STUDIO</span>
            </div>
            <p className="mt-4 max-w-sm text-[13px] leading-relaxed text-muted">
              Exam-focused notes for Pearson Edexcel International A Level Chemistry —
              the 2018 specification, topics 1–10 (WCH11 + WCH12).
            </p>
            <p className="mt-4 text-[11px] italic leading-relaxed text-faint">
              An independent study tool — not affiliated with or endorsed by Pearson Edexcel.
            </p>
          </div>
          <div className="flex flex-wrap gap-x-14 gap-y-6 md:justify-end">
            <div>
              <p className="mb-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-faint" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>Site</p>
              <ul className="space-y-2">
                {[['Topics', '/topics'], ['Flashcards', '/flashcards'], ['Progress', '/progress'], ['Control room', '/settings']].map(([label, to]) => (
                  <li key={to}>
                    <a href={`#${to}`} onClick={(e) => { e.preventDefault(); go(to) }} className="text-[12.5px] text-muted t-fast hover:text-acc">{label}</a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="mb-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-faint" style={{ fontFamily: 'var(--font-grotesk), sans-serif' }}>Syllabus</p>
              <ul className="space-y-2">
                {[['Unit 1 — WCH11', '/topics'], ['Unit 2 — WCH12', '/topics'], ['Topic 01 notes', '/topic/amount-of-substance']].map(([label, to]) => (
                  <li key={label}>
                    <a href={`#${to}`} onClick={(e) => { e.preventDefault(); go(to) }} className="text-[12.5px] text-muted t-fast hover:text-acc">{label}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className="mt-8 flex flex-wrap items-center justify-between gap-2 border-t border-[color-mix(in_srgb,var(--fg)_10%,transparent)] pt-5">
          <p className="text-[10px] uppercase tracking-[0.16em] text-faint">© {new Date().getFullYear()} ial studio — built for revision</p>
          <p className="text-[10px] uppercase tracking-[0.16em] text-faint">your data stays in your browser</p>
        </div>
      </div>
    </footer>
  )
}

export function Footer({ go }: { go: (to: string) => void }) {
  const mode = useSettings((s) => s.uiMode)
  if (mode === 'lab') return <LabFooter go={go} />
  return <TerminalFooter go={go} />
}
