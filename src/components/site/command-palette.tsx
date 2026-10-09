'use client'

import React, { useEffect, useMemo, useRef, useState } from 'react'
import { CornerDownLeft } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { downloadTopicPdf } from '@/lib/site/pdf-client'
import { useSettings, useUi, applySettingsToDom, UI_MODES, type AccentName } from '@/lib/site/stores'
import { useRoute } from '@/lib/site/router'

interface Item {
  id: string
  group: 'Pages' | 'Topics' | 'Sections' | 'Decks' | 'Actions'
  label: string
  hint?: string
  run: () => void
}

function score(needle: string, hay: string): number {
  const n = needle.toLowerCase()
  const h = hay.toLowerCase()
  if (!n) return 1
  if (h.includes(n)) return 100 - h.indexOf(n)
  // subsequence
  let i = 0
  for (const ch of h) {
    if (ch === n[i]) i++
    if (i === n.length) return 40
  }
  return 0
}

export function CommandPalette({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const open = useUi((s) => s.paletteOpen)
  const setPalette = useUi((s) => s.setPalette)
  const uiMode = useSettings((s) => s.uiMode)
  const [route] = useRoute()
  const [q, setQ] = useState('')
  const [sel, setSel] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const listRef = useRef<HTMLDivElement>(null)

  // reset query/selection when the palette opens (render-time adjustment)
  const [wasOpen, setWasOpen] = useState(false)
  if (open !== wasOpen) {
    setWasOpen(open)
    if (open) {
      setQ('')
      setSel(0)
    }
  }
  // reset selection when the query changes
  const [prevQ, setPrevQ] = useState(q)
  if (prevQ !== q) {
    setPrevQ(q)
    setSel(0)
  }

  const items = useMemo<Item[]>(() => {
    const pages: Item[] = [
      { id: 'p-home', group: 'Pages', label: 'Home', hint: '~', run: () => go('/') },
      { id: 'p-topics', group: 'Pages', label: 'All topics', hint: '/topics', run: () => go('/topics') },
      { id: 'p-cards', group: 'Pages', label: 'Flashcard decks', hint: '/flashcards', run: () => go('/flashcards') },
      { id: 'p-progress', group: 'Pages', label: 'Progress dashboard', hint: '/progress', run: () => go('/progress') },
    ]
    const titems: Item[] = topics.map((t) => ({
      id: `t-${t.slug}`,
      group: 'Topics',
      label: `${String(t.number).padStart(2, '0')} · ${t.title}`,
      hint: t.unitCode,
      run: () => go(`/topic/${t.slug}`),
    }))
    // every section is reachable — jump straight to a spec point
    const sections: Item[] = topics.flatMap((t) =>
      t.sections.map((s) => ({
        id: `s-${t.slug}-${s.sectionKey}`,
        group: 'Sections' as const,
        label: `${s.number} · ${s.title}`,
        hint: s.spec ? `T${String(t.number).padStart(2, '0')} · ${s.spec}` : `T${String(t.number).padStart(2, '0')}`,
        run: () => go(`/topic/${t.slug}/${s.sectionKey}`),
      }))
    )
    const decks: Item[] = topics.map((t) => ({
      id: `d-${t.slug}`,
      group: 'Decks',
      label: `${String(t.number).padStart(2, '0')} · ${t.title}`,
      hint: `${t.cards.length} cards`,
      run: () => go(`/deck/${t.slug}`),
    }))
    const accents: AccentName[] = ['coral', 'amber', 'mint', 'rose', 'violet', 'cyan']
    const themeNames: { key: 'midnight' | 'carbon' | 'paper' | 'sepia'; label: string }[] = [
      { key: 'midnight', label: 'Midnight' },
      { key: 'carbon', label: 'Carbon' },
      { key: 'paper', label: 'Paper' },
      { key: 'sepia', label: 'Sepia' },
    ]
    const actions: Item[] = [
      {
        id: 'a-settings',
        group: 'Actions' as const,
        label: 'Open control room',
        hint: 'preferences',
        run: () => useUi.getState().openSettings(),
      },
      ...UI_MODES.map((m) => ({
        id: `a-ui-${m.value}`,
        group: 'Actions' as const,
        label: `Interface → ${m.label}`,
        hint: 'switch',
        run: () => {
          useSettings.getState().set({ uiMode: m.value })
          applySettingsToDom({ ...useSettings.getState() })
        },
      })),
      {
        id: 'a-focus',
        group: 'Actions' as const,
        label: 'Toggle focus mode',
        hint: 'dim surroundings',
        run: () => {
          useSettings.getState().set({ focusMode: !useSettings.getState().focusMode })
          applySettingsToDom({ ...useSettings.getState() })
        },
      },
      ...themeNames.map((t) => ({
        id: `a-theme-${t.key}`,
        group: 'Actions' as const,
        label: `Theme → ${t.label}`,
        hint: 'switch',
        run: () => {
          useSettings.getState().set({ theme: t.key })
          applySettingsToDom({ ...useSettings.getState() })
        },
      })),
      ...accents.map((a) => ({
        id: `a-accent-${a}`,
        group: 'Actions' as const,
        label: `Accent → ${a}`,
        hint: 'switch',
        run: () => {
          useSettings.getState().set({ accent: a })
          applySettingsToDom({ ...useSettings.getState() })
        },
      })),
    ]
    // PDF download only makes sense while reading a topic
    if (route.name === 'topic' && route.slug) {
      actions.push({
        id: 'a-print',
        group: 'Actions' as const,
        label: 'Download this topic as PDF',
        hint: 'print edition',
        run: () => {
          setPalette(false)
          // server-rendered PDF download, with print-engine fallback
          // on hosts without headless Chromium (e.g. Vercel)
          void downloadTopicPdf(route.slug)
        },
      })
    }
    return [...pages, ...titems, ...sections, ...decks, ...actions]
  }, [topics, go, route.name, route.slug, setPalette])

  const results = useMemo(() => {
    if (!q.trim()) {
      return items.filter((i) => i.group === 'Pages' || i.group === 'Topics')
    }
    return items
      .map((i) => ({ i, s: score(q.trim(), i.label + ' ' + (i.hint ?? '')) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 12)
      .map((x) => x.i)
  }, [q, items])

  useEffect(() => {
    if (!open) return
    setTimeout(() => inputRef.current?.focus(), 30)
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setPalette(false)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, setPalette])

  if (!open) return null

  const runItem = (item?: Item) => {
    if (!item) return
    setPalette(false)
    item.run()
  }

  const grouped = results.map((item, i) => ({
    item,
    showGroup: i === 0 || results[i - 1].group !== item.group,
  }))

  return (
    <div className="fixed inset-0 z-[80] print:hidden" role="dialog" aria-modal="true" aria-label="Command palette">
      <div className="absolute inset-0 bg-black/60 t-fast" onClick={() => setPalette(false)} aria-hidden />
      <div className="absolute left-1/2 top-[12vh] w-[min(92vw,560px)] -translate-x-1/2 overflow-hidden rounded-xl border border-line-strong bg-surface shadow-2xl">
        <div className="flex items-center gap-3 border-b border-line px-4">
          <span className="mono text-[12px] text-acc">›</span>
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'ArrowDown') {
                e.preventDefault()
                setSel((s) => Math.min(s + 1, results.length - 1))
              } else if (e.key === 'ArrowUp') {
                e.preventDefault()
                setSel((s) => Math.max(s - 1, 0))
              } else if (e.key === 'Enter') {
                e.preventDefault()
                runItem(results[sel])
              }
            }}
            placeholder="jump to a topic, deck, action…"
            aria-label="Command input"
            className="mono w-full bg-transparent py-4 text-[13.5px] text-fg placeholder:text-faint focus:outline-none"
          />
          <kbd className="kbd">esc</kbd>
        </div>
        <div ref={listRef} className="max-h-[46vh] overflow-y-auto p-1.5">
          {results.length === 0 && (
            <p className="mono px-3 py-6 text-center text-[12px] text-faint">
              {uiMode === 'terminal' ? <>{'// no matches for “'}{q}{'”'}</> : <>No matches for “{q}”</>}
            </p>
          )}
          {grouped.map(({ item, showGroup }, i) => {
            return (
              <React.Fragment key={item.id}>
                {showGroup && (
                  <p className="mono px-3 pb-1 pt-2.5 text-[9.5px] uppercase tracking-[0.2em] text-faint">
                    {item.group}
                  </p>
                )}
                <button
                  onMouseEnter={() => setSel(i)}
                  onClick={() => runItem(item)}
                  className={`flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left t-fast ${
                    i === sel ? 'bg-acc/12 text-fg ring-1 ring-acc/30' : 'text-muted'
                  }`}
                >
                  <span className="truncate text-[13px]">{item.label}</span>
                  <span className="flex shrink-0 items-center gap-2">
                    {item.hint && <span className="mono text-[10px] uppercase tracking-[0.1em] text-faint">{item.hint}</span>}
                    {i === sel && <CornerDownLeft size={12} className="text-acc" />}
                  </span>
                </button>
              </React.Fragment>
            )
          })}
        </div>
        <div className="flex items-center gap-4 border-t border-line px-4 py-2.5">
          <span className="mono text-[10px] text-faint"><kbd className="kbd">↑↓</kbd> navigate</span>
          <span className="mono text-[10px] text-faint"><kbd className="kbd">↵</kbd> run</span>
          <span className="mono ml-auto text-[10px] text-faint">{results.length} results</span>
        </div>
      </div>
    </div>
  )
}
