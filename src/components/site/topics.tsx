'use client'

import React, { useMemo, useState } from 'react'
import { ArrowRight, ChevronRight, Search } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { Chip, ProgressBar, eyebrowText } from './ui-bits'
import { useProgress, useSettings } from '@/lib/site/stores'

type Filter = 'all' | 'u1' | 'u2'

export function Topics({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const read = useProgress((s) => s.read)
  const readMap = hydrated ? read : ({} as Record<string, true>)
  const mode = useSettings((s) => s.uiMode)
  const [filter, setFilter] = useState<Filter>('all')
  const [q, setQ] = useState('')

  const shown = useMemo(() => {
    const needle = q.trim().toLowerCase()
    return topics.filter((t) => {
      if (filter === 'u1' && t.unit !== 1) return false
      if (filter === 'u2' && t.unit !== 2) return false
      if (!needle) return true
      return (
        t.title.toLowerCase().includes(needle) ||
        t.summary.toLowerCase().includes(needle) ||
        t.sections.some((s) => s.title.toLowerCase().includes(needle))
      )
    })
  }, [topics, filter, q])

  const units: { key: Filter; label: string }[] = [
    { key: 'all', label: 'All' },
    { key: 'u1', label: 'Unit 1 · WCH11' },
    { key: 'u2', label: 'Unit 2 · WCH12' },
  ]

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-12">
      <p className="eyebrow">{eyebrowText(mode, 'Syllabus map')}</p>
      <div className="mt-4 flex flex-wrap items-end justify-between gap-4">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          All {shown.length}{' '}
          <span className="serif-accent text-acc">topics</span>.
        </h1>
        <div className="flex items-center gap-2">
          {units.map((u) => (
            <button
              key={u.key}
              onClick={() => setFilter(u.key)}
              aria-pressed={filter === u.key}
              className={`mono rounded-md border px-2.5 py-1.5 text-[11px] uppercase tracking-[0.12em] t-fast focus-visible:outline-acc ${
                filter === u.key ? 'border-acc/50 bg-acc/10 text-acc' : 'border-line text-muted hover:border-line-strong hover:text-fg'
              }`}
            >
              {u.label}
            </button>
          ))}
        </div>
      </div>

      <div className="relative mt-6 max-w-md">
        <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-faint" />
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="filter topics or sections…"
          aria-label="Filter topics"
          className="mono w-full rounded-lg border border-line bg-surface py-2.5 pl-9 pr-3 text-[13px] text-fg placeholder:text-faint t-fast focus:border-line-strong focus:outline-none focus-visible:outline-acc"
        />
      </div>

      {(['u1', 'u2'] as const).map((uk) => {
        const unitNo = uk === 'u1' ? 1 : 2
        const list = shown.filter((t) => t.unit === unitNo)
        if (list.length === 0) return null
        const t0 = list[0]
        return (
          <section key={uk} className="mt-10">
            <div className="mb-4 flex flex-wrap items-center gap-3">
              <h2 className="mono text-[12px] font-medium uppercase tracking-[0.18em] text-fg">
                Unit {unitNo} — {t0.unitCode}
              </h2>
              <span className="hidden h-px flex-1 bg-line sm:block" aria-hidden />
              <span className="mono hidden text-[11px] text-faint md:inline">{t0.unitName}</span>
            </div>

            <div className={`overflow-hidden ${
              mode === 'lab'
                ? 'lab-glass rounded-[22px]'
                : 'rounded-xl border border-line'
            }`}>
              {list.map((t, i) => {
                const done = hydrated ? t.sections.filter((s) => readMap[`${t.slug}/${s.sectionKey}`]).length : 0
                const pct = t.sections.length ? (done / t.sections.length) * 100 : 0
                const hasNotes = t.sections.some((s) => s.content)
                return (
                  <button
                    key={t.slug}
                    onClick={() => go(`/topic/${t.slug}`)}
                    className={`topic-row group grid w-full grid-cols-[auto_1fr_auto] items-center gap-4 px-4 py-5 text-left t-fast hover:bg-elev focus-visible:bg-elev focus-visible:outline-acc sm:grid-cols-[auto_1fr_auto_auto] sm:gap-6 sm:px-6 ${
                      i > 0 ? 'border-t border-line' : ''
                    }`}
                  >
                    <span className="mono w-8 text-[15px] text-faint t-fast group-hover:text-acc">
                      {String(t.number).padStart(2, '0')}
                    </span>
                    <span className="min-w-0">
                      <span className="flex items-center gap-2">
                        <span className="block truncate text-[15px] font-medium text-fg t-fast group-hover:text-acc">
                          {t.title}
                        </span>
                        {t.slug.endsWith('-v2') && (
                          <span className="mono shrink-0 rounded border border-acc/40 bg-acc/10 px-1 py-0.5 text-[8.5px] uppercase tracking-[0.14em] text-acc">
                            version 2
                          </span>
                        )}
                      </span>
                      <span className="mt-1 block truncate text-[12.5px] text-muted">
                        {t.subtitle}
                      </span>
                      <span className="mt-2.5 block max-w-xs">
                        <ProgressBar value={pct} />
                      </span>
                    </span>
                    <span className="hidden flex-col items-end gap-1.5 sm:flex">
                      <span className="mono text-[11px] text-faint">
                        {t.sections.length} sections{t.cards.length ? ` · ${t.cards.length} cards` : ''} · ~{t.estHours}h
                      </span>
                      <span className="flex gap-1.5">
                        <Chip accent={hasNotes}>{hasNotes ? 'notes live' : 'queued'}</Chip>
                        {hydrated && done === t.sections.length && t.sections.length > 0 && <Chip accent>✓ done</Chip>}
                      </span>
                    </span>
                    <ChevronRight size={16} className="text-faint t-fast group-hover:translate-x-0.5 group-hover:text-acc" />
                  </button>
                )
              })}
            </div>
          </section>
        )
      })}

      {shown.length === 0 && (
        <div className="mono mt-12 rounded-xl border border-line bg-surface px-6 py-12 text-center text-[13px] text-muted">
          {mode === 'terminal' && <>$ filter --no-match<br /></>}
          <span className="text-faint">{mode === 'terminal' ? '// ' : ''}nothing matches “{q}” — try another term</span>
        </div>
      )}

      <div className="mt-12 flex justify-center">
        <button
          onClick={() => go('/flashcards')}
          className="mono inline-flex items-center gap-2 text-[12px] uppercase tracking-[0.14em] text-muted t-fast hover:text-acc"
        >
          Prefer testing yourself? Open the decks <ArrowRight size={13} />
        </button>
      </div>
    </div>
  )
}
