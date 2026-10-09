'use client'

import React, { useEffect, useState } from 'react'
import { FlaskConical, LayoutGrid, Menu, Search, SlidersHorizontal, X } from 'lucide-react'
import { useRoute, type Route } from '@/lib/site/router'
import { useUi, useSettings, cycleUiMode, UI_MODES } from '@/lib/site/stores'

const LINKS: { label: string; to: string; match: (r: Route) => boolean }[] = [
  { label: 'Topics', to: '/topics', match: (r) => r.name === 'topics' || r.name === 'topic' },
  { label: 'Flashcards', to: '/flashcards', match: (r) => r.name === 'flashcards' || r.name === 'deck' },
  { label: 'Progress', to: '/progress', match: (r) => r.name === 'progress' },
]

/* quick interface cycler — one click to jump to the next site */
function ModeCycle({ className, labelStyle }: { className?: string; labelStyle?: string }) {
  const mode = useSettings((s) => s.uiMode)
  const current = UI_MODES.find((m) => m.value === mode)
  return (
    <button
      onClick={() => cycleUiMode()}
      aria-label={`Switch interface — current: ${current?.label}. Click to cycle.`}
      title={`Interface: ${current?.label} — click to switch`}
      className={className}
    >
      <LayoutGrid size={13} strokeWidth={1.75} aria-hidden />
      <span className={labelStyle}>{current?.label}</span>
    </button>
  )
}

/* ============================================================
   NAV — TERMINAL (the control desk)
   ============================================================ */

function Brand({ mode }: { mode: string }) {
  if (mode === 'lab') {
    return (
      <span className="nav-brand flex items-center gap-2.5 text-[13px] text-fg">
        <span aria-hidden className="h-2.5 w-2.5 rounded-full bg-acc" style={{ boxShadow: '0 0 14px 2px color-mix(in srgb, var(--acc) 70%, transparent)' }} />
        IAL&nbsp;STUDIO
      </span>
    )
  }
  return (
    <span className="nav-brand mono text-[13px] font-semibold tracking-[0.08em] text-fg">
      IAL<span className="text-acc">{'//'}</span>CHEM
    </span>
  )
}

function TerminalNav({ route }: { route: Route }) {
  const openPalette = useUi((s) => s.setPalette)
  const openSettings = useUi((s) => s.openSettings)
  const [menuOpen, setMenuOpen] = useState(false)
  const [, go] = useRoute()
  const mode = useSettings((s) => s.uiMode)

  const [prevPath, setPrevPath] = useState<string | null>(null)
  const pathKey = `${route.name}:${route.slug ?? ''}`
  if (prevPath !== pathKey) {
    setPrevPath(pathKey)
    if (menuOpen) setMenuOpen(false)
  }

  return (
    <header
      className="sticky top-0 z-50 border-b border-line backdrop-blur-md print:hidden"
      style={{ backgroundColor: 'var(--nav-bg)' }}
    >
      <div className="mx-auto flex h-14 max-w-[1200px] items-center gap-3 px-6">
        <a href="#/" onClick={(e) => { e.preventDefault(); go('/') }} className="flex shrink-0 items-center gap-2 focus-visible:outline-acc" aria-label="IAL CHEM home">
          <span className="flex h-7 w-7 items-center justify-center rounded-md border border-acc/40 text-acc">
            <FlaskConical size={14} />
          </span>
          <Brand mode={mode} />
        </a>
        <nav className="ml-6 hidden items-center gap-1 md:flex" aria-label="Primary">
          {LINKS.map((l) => {
            const active = l.match(route)
            return (
              <a key={l.to} href={`#${l.to}`} onClick={(e) => { e.preventDefault(); go(l.to) }}
                aria-current={active ? 'page' : undefined}
                className={`nav-link mono rounded-md px-2.5 py-1.5 text-[11px] uppercase tracking-[0.16em] t-fast focus-visible:outline-acc ${active ? 'text-acc' : 'text-muted hover:text-fg'}`}>
                {l.label}
              </a>
            )
          })}
        </nav>
        <div className="ml-auto flex items-center gap-2">
          <button onClick={() => openPalette(true)} className="mono hidden items-center gap-2 rounded-lg border border-line px-2.5 py-1.5 text-[11px] text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc sm:flex" aria-label="Open command palette">
            <Search size={12} />
            <span className="uppercase tracking-[0.14em]">Search</span>
            <kbd className="kbd ml-1">⌘K</kbd>
          </button>
          <ModeCycle className="mono hidden items-center gap-1.5 rounded-lg border border-line px-2.5 py-1.5 text-[11px] uppercase tracking-[0.12em] text-muted t-fast hover:border-acc hover:text-acc focus-visible:outline-acc lg:flex" labelStyle="" />
          <button onClick={() => openPalette(true)} aria-label="Search" className="rounded-lg border border-line p-2 text-muted t-fast hover:border-line-strong hover:text-fg sm:hidden focus-visible:outline-acc">
            <Search size={14} />
          </button>
          <button onClick={openSettings} aria-label="Open control room — reading preferences" title="Control room" className="rounded-lg border border-line p-2 text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc">
            <SlidersHorizontal size={14} />
          </button>
          <button onClick={() => setMenuOpen((o) => !o)} aria-label={menuOpen ? 'Close menu' : 'Open menu'} aria-expanded={menuOpen} className="rounded-lg border border-line p-2 text-muted t-fast hover:border-line-strong hover:text-fg md:hidden focus-visible:outline-acc">
            {menuOpen ? <X size={14} /> : <Menu size={14} />}
          </button>
        </div>
      </div>
      {menuOpen && (
        <nav className="border-t border-line px-6 py-3 md:hidden" aria-label="Mobile">
          {LINKS.map((l) => (
            <a key={l.to} href={`#${l.to}`} onClick={(e) => { e.preventDefault(); go(l.to); setMenuOpen(false) }}
              className={`nav-link mono block rounded-md px-2 py-2.5 text-[12px] uppercase tracking-[0.16em] t-fast ${l.match(route) ? 'text-acc' : 'text-muted hover:text-fg'}`}>
              {l.label}
            </a>
          ))}
        </nav>
      )}
    </header>
  )
}

/* ============================================================
   NAV — LAB (a glass instrument panel)
   floating glass pill, glow brand dot, pill links
   ============================================================ */

function LabNav({ route }: { route: Route }) {
  const openPalette = useUi((s) => s.setPalette)
  const openSettings = useUi((s) => s.openSettings)
  const [menuOpen, setMenuOpen] = useState(false)
  const [, go] = useRoute()
  const mode = useSettings((s) => s.uiMode)

  const [prevPath, setPrevPath] = useState<string | null>(null)
  const pathKey = `${route.name}:${route.slug ?? ''}`
  if (prevPath !== pathKey) {
    setPrevPath(pathKey)
    if (menuOpen) setMenuOpen(false)
  }

  return (
    <div className="fixed inset-x-0 top-3 z-50 px-3 print:hidden">
      <nav className="lab-nav mx-auto flex h-[52px] max-w-[1080px] items-center gap-2 rounded-full px-3 sm:px-5" aria-label="Primary">
        <a href="#/" onClick={(e) => { e.preventDefault(); go('/') }} className="flex shrink-0 items-center focus-visible:outline-acc" aria-label="IAL Studio — home">
          <Brand mode={mode} />
        </a>
        <div className="mx-2 hidden h-4 w-px bg-[color-mix(in_srgb,var(--fg)_14%,transparent)] md:block" aria-hidden />
        <div className="hidden items-center gap-1 md:flex">
          {LINKS.map((l) => (
            <a key={l.to} href={`#${l.to}`} onClick={(e) => { e.preventDefault(); go(l.to) }}
              aria-current={l.match(route) ? 'page' : undefined}
              className={`nav-link t-fast ${l.match(route) ? 'bg-[color-mix(in_srgb,var(--acc)_14%,transparent)] text-acc' : 'text-muted'}`}>
              {l.label}
            </a>
          ))}
        </div>
        <div className="ml-auto flex items-center gap-1.5">
          <button onClick={() => openPalette(true)} aria-label="Search" className="flex h-9 w-9 items-center justify-center rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-muted t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc">
            <Search size={14} />
          </button>
          <button onClick={openSettings} aria-label="Open control room — reading preferences" title="Control room" className="flex h-9 w-9 items-center justify-center rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-muted t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc">
            <SlidersHorizontal size={14} />
          </button>
          <ModeCycle className="hidden h-9 items-center gap-1.5 rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] px-3.5 text-[11px] font-medium text-muted t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc lg:flex" labelStyle="font-[family-name:var(--font-grotesk)]" />
          <button onClick={() => setMenuOpen((o) => !o)} aria-label={menuOpen ? 'Close menu' : 'Open menu'} aria-expanded={menuOpen} className="flex h-9 w-9 items-center justify-center rounded-full border border-[color-mix(in_srgb,var(--fg)_14%,transparent)] text-muted t-fast hover:text-fg md:hidden focus-visible:outline-acc">
            {menuOpen ? <X size={14} /> : <Menu size={14} />}
          </button>
        </div>
      </nav>
      {menuOpen && (
        <nav className="lab-nav mx-auto mt-2 max-w-[1080px] rounded-3xl px-4 py-3 md:hidden" aria-label="Mobile">
          {LINKS.map((l) => (
            <a key={l.to} href={`#${l.to}`} onClick={(e) => { e.preventDefault(); go(l.to); setMenuOpen(false) }}
              className={`block rounded-full px-4 py-2.5 text-[13px] t-fast ${l.match(route) ? 'bg-[color-mix(in_srgb,var(--acc)_14%,transparent)] text-acc' : 'text-muted'}`}>
              {l.label}
            </a>
          ))}
        </nav>
      )}
    </div>
  )
}

export function Nav({ route }: { route: Route }) {
  const mode = useSettings((s) => s.uiMode)
  if (mode === 'lab') return <LabNav route={route} />
  return <TerminalNav route={route} />
}

/* ============================================================
   FOOTERS — two different colophons
   ============================================================ */

function Flask() {
  return (
    <span className="flex h-7 w-7 items-center justify-center rounded-md border border-acc/40 text-acc">
      <FlaskConical size={14} />
    </span>
  )
}

function TerminalFooter({ go }: { go: (to: string) => void }) {
  const mode = useSettings((s) => s.uiMode)
  return (
    <footer className="mt-auto border-t border-line print:hidden">
      <div className="mx-auto grid max-w-[1200px] gap-10 px-6 py-12 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <div className="flex items-center gap-2">
            <Flask />
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
              <span aria-hidden className="h-2.5 w-2.5 rounded-full bg-acc" style={{ boxShadow: '0 0 14px 2px color-mix(in srgb, var(--acc) 70%, transparent)' }} />
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
