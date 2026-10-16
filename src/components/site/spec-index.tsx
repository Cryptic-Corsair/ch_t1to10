'use client'

/*
 * SPEC INDEX — every assessment statement, worded exactly as the
 * specification words it, grouped by topic. Tick the points you want,
 * save the selection as a named set, and the same ticks drive the custom
 * revision notes at #/notes. Search narrows by code or wording; the chip
 * tray keeps the whole selection visible and one click removable.
 */

import React, { useMemo, useState } from 'react'
import { Check, CheckCheck, ListChecks, NotebookPen, Search, X } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { buildSpecIndex, type SpecPoint } from '@/lib/site/spec'
import { useSettings, useSpecPicks } from '@/lib/site/stores'
import { BtnGhost, BtnSolid, eyebrowText } from './ui-bits'
import { RevisionSets } from './revision-sets'

type PickFilter = 'all' | 'picked' | 'rest'

const PICK_FILTERS: { key: PickFilter; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'picked', label: 'Selected' },
  { key: 'rest', label: 'Not selected' },
]

export function SpecIndex({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const mode = useSettings((s) => s.uiMode)
  const picks = useSpecPicks((s) => s.picks)
  const toggle = useSpecPicks((s) => s.toggle)
  const setPicks = useSpecPicks((s) => s.setPicks)
  const clear = useSpecPicks((s) => s.clear)

  const [q, setQ] = useState('')
  const [filter, setFilter] = useState<PickFilter>('all')

  const index = useMemo(() => buildSpecIndex(topics), [topics])
  const pickedSet = useMemo(() => new Set(picks), [picks])

  /* search (code or statement wording) + picked-state filter */
  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase()
    return index.filter((p) => {
      if (needle && !(p.code.toLowerCase().includes(needle) || p.statement.toLowerCase().includes(needle))) return false
      if (filter === 'picked' && !pickedSet.has(p.code)) return false
      if (filter === 'rest' && pickedSet.has(p.code)) return false
      return true
    })
  }, [index, q, filter, pickedSet])

  const groups = useMemo(() => {
    const out: { topicSlug: string; topicNumber: number; topicTitle: string; points: SpecPoint[] }[] = []
    for (const p of filtered) {
      const last = out[out.length - 1]
      if (last && last.topicSlug === p.topicSlug) last.points.push(p)
      else out.push({ topicSlug: p.topicSlug, topicNumber: p.topicNumber, topicTitle: p.topicTitle, points: [p] })
    }
    return out
  }, [filtered])

  const narrow = q.trim() !== '' || filter !== 'all'
  const emptyHint = !narrow
    ? ''
    : q.trim()
      ? `// no points match “${q.trim()}” — try a code like 5.6 or a word from the statement`
      : filter === 'picked'
        ? '// nothing selected yet — tick some points first'
        : '// every visible point is selected — nothing left to tick'

  const toggleTopic = (g: { points: SpecPoint[] }) => {
    const selectable = g.points.filter((p) => p.sections.length > 0).map((p) => p.code)
    if (selectable.length === 0) return
    const all = selectable.every((c) => pickedSet.has(c))
    setPicks(all ? picks.filter((c) => !selectable.includes(c)) : [...new Set([...picks, ...selectable.filter((c) => !pickedSet.has(c))])])
  }

  const panelSkin = mode === 'terminal' ? 'rounded-xl border border-line bg-surface' : 'lab-glass rounded-[16px]'

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-12">
      {/* ---------- masthead ---------- */}
      <p className="eyebrow">{eyebrowText(mode, 'Specification')}</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        The spec <span className="serif-accent text-acc">index</span>.
      </h1>
      <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
        Every assessment statement from the 2018 specification, quoted verbatim —
        all {index.length} points across topics 1–10. Tick the points you want, save the selection
        as a named set for later, and the full notes behind every ticked point are pulled together
        in{' '}
        <button onClick={() => go('/notes')} className="text-acc underline decoration-acc/40 underline-offset-2 t-fast hover:decoration-acc">
          revision notes
        </button>
        .
      </p>

      {/* ---------- control panel ---------- */}
      <div className={`mt-8 ${panelSkin}`}>
        {/* row 1 — count + actions */}
        <div className="flex flex-wrap items-center gap-x-6 gap-y-4 px-5 py-4">
          <p className="flex items-center gap-2.5 text-[14px] text-fg">
            <ListChecks size={15} strokeWidth={1.75} className="text-acc" />
            <span className="font-semibold">{picks.length}</span>
            <span className="text-muted">of {index.length} points selected</span>
          </p>
          <div className="ms-auto flex flex-wrap items-center gap-2.5">
            <RevisionSets mode={mode} />
            {picks.length > 0 && (
              <BtnGhost onClick={clear} ariaLabel="Clear selection">
                <X size={14} />
                Clear
              </BtnGhost>
            )}
            <BtnSolid
              onClick={() => go('/notes')}
              ariaLabel="Open the revision notes built from the selected points"
              className={picks.length === 0 ? 'pointer-events-none opacity-40' : ''}
            >
              <NotebookPen size={14} />
              Revision notes{picks.length > 0 ? ` · ${picks.length}` : ''}
            </BtnSolid>
          </div>
        </div>

        {/* row 2 — search + picked-state filters */}
        <div className="flex flex-wrap items-center gap-x-4 gap-y-3 border-t border-line/70 px-5 py-3.5">
          <label className="flex min-w-[200px] flex-1 items-center gap-2.5 rounded-lg border border-line bg-transparent px-3 py-2 t-fast focus-within:border-acc/50">
            <Search size={13} className="shrink-0 text-faint" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => e.key === 'Escape' && setQ('')}
              placeholder="Search points — a code like 5.6, or words from the statement…"
              aria-label="Search specification points"
              className="mono w-full bg-transparent text-[12.5px] text-fg placeholder:text-faint focus:outline-none"
            />
            {q !== '' && (
              <button
                type="button"
                onClick={() => setQ('')}
                aria-label="Clear the search"
                className="shrink-0 text-faint t-fast hover:text-fg focus-visible:outline-acc"
              >
                <X size={13} />
              </button>
            )}
          </label>
          <div className="flex items-center gap-1.5" role="group" aria-label="Filter by selection state">
            {PICK_FILTERS.map((f) => (
              <button
                key={f.key}
                type="button"
                onClick={() => setFilter(f.key)}
                aria-pressed={filter === f.key}
                className={`mono rounded-md border px-2.5 py-1.5 text-[10px] uppercase tracking-[0.14em] t-fast focus-visible:outline-acc ${
                  filter === f.key
                    ? 'border-acc/50 bg-acc/10 text-acc'
                    : 'border-line text-muted hover:border-acc/40 hover:text-acc'
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
          {narrow && (
            <p className="mono ms-auto text-[10.5px] uppercase tracking-[0.14em] text-faint">
              {filtered.length} of {index.length} points
            </p>
          )}
        </div>

        {/* row 3 — the selection tray */}
        {picks.length > 0 && (
          <div className="flex flex-wrap items-start gap-x-3 gap-y-2 border-t border-line/70 px-5 py-3.5">
            <span className="mono pt-1 text-[10px] uppercase tracking-[0.16em] text-faint">
              picked
            </span>
            <div className="flex max-h-24 flex-wrap gap-1.5 overflow-y-auto" aria-label="Selected specification points">
              {picks.map((code) => (
                <button
                  key={code}
                  type="button"
                  onClick={() => toggle(code)}
                  aria-label={`Remove specification point ${code} from the selection`}
                  className="mono inline-flex items-center gap-1 rounded-full border border-acc/40 bg-acc/10 px-2.5 py-1 text-[10.5px] font-semibold tracking-[0.06em] text-acc t-fast hover:border-acc hover:bg-acc/20 focus-visible:outline-acc"
                >
                  {code}
                  <X size={10} strokeWidth={2.5} />
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ---------- per-topic point lists ---------- */}
      <div className={mode === 'terminal' ? 'mt-10 space-y-10' : 'mt-10 space-y-12'}>
        {groups.map((g) => {
          const selectable = g.points.filter((p) => p.sections.length > 0).map((p) => p.code)
          const allPicked = selectable.length > 0 && selectable.every((c) => pickedSet.has(c))
          const somePicked = selectable.some((c) => pickedSet.has(c))
          const selCount = g.points.filter((p) => pickedSet.has(p.code)).length
          return (
            <section key={g.topicSlug} aria-label={`Topic ${g.topicNumber} — ${g.topicTitle}`}>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
                <h2 className="flex items-baseline gap-3 text-[17px] font-semibold tracking-tight text-fg">
                  <span className="mono text-[13px] text-faint">{String(g.topicNumber).padStart(2, '0')}</span>
                  {g.topicTitle}
                </h2>
                <span className="mono text-[10px] uppercase tracking-[0.16em] text-faint">
                  {g.points.length} point{g.points.length === 1 ? '' : 's'}
                </span>
                {selCount > 0 && (
                  <span className="mono text-[10px] uppercase tracking-[0.16em] text-acc">
                    {selCount}/{g.points.length} picked
                  </span>
                )}
                {selectable.length > 0 && (
                  <button
                    onClick={() => toggleTopic(g)}
                    className={`mono ms-auto inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1.5 text-[10px] uppercase tracking-[0.14em] t-fast focus-visible:outline-acc ${
                      allPicked ? 'border-acc/50 bg-acc/10 text-acc' : 'border-line text-muted hover:border-acc/40 hover:text-acc'
                    }`}
                    aria-pressed={allPicked}
                  >
                    <CheckCheck size={12} strokeWidth={1.75} />
                    {allPicked ? 'Unselect topic' : somePicked ? 'Select rest' : 'Select topic'}
                  </button>
                )}
              </div>

              <div className={`mt-4 ${mode === 'terminal' ? 'overflow-hidden rounded-xl border border-line' : 'space-y-2.5'}`}>
                {g.points.map((p) => (
                  <PointRow
                    key={p.code}
                    point={p}
                    selected={pickedSet.has(p.code)}
                    onToggle={() => toggle(p.code)}
                    mode={mode}
                    go={go}
                  />
                ))}
              </div>
            </section>
          )
        })}

        {emptyHint !== '' && (
          <p className="mono rounded-xl border border-dashed border-line px-5 py-6 text-center text-[12px] leading-relaxed text-faint">
            {emptyHint}
          </p>
        )}
      </div>
    </div>
  )
}

function PointRow({
  point: p, selected, onToggle, mode, go,
}: {
  point: SpecPoint
  selected: boolean
  onToggle: () => void
  mode: string
  go: (to: string) => void
}) {
  const disabled = p.sections.length === 0
  /* the row is a div now so the covered-in strip can carry real links;
     the toggle button owns everything above the strip */
  const container =
    mode === 'terminal'
      ? [
          'flex w-full flex-col text-left',
          selected ? 'bg-elev' : '',
          disabled ? 'opacity-45' : 't-fast hover:bg-elev/60',
        ].join(' ')
      : [
          'lab-glass group flex w-full flex-col rounded-[14px] text-left',
          selected ? 'border-[color-mix(in_srgb,var(--acc)_55%,transparent)]!' : '',
          disabled ? 'opacity-45' : 't-fast hover:border-[color-mix(in_srgb,var(--acc)_35%,transparent)]!',
        ].join(' ')

  return (
    <div className={container}>
      <button
        type="button"
        onClick={disabled ? undefined : onToggle}
        disabled={disabled}
        aria-pressed={selected}
        aria-label={`Specification point ${p.code}${selected ? ' — selected' : ''}`}
        className="flex w-full items-start gap-4 px-4 py-3.5 text-left sm:gap-5 sm:px-5 focus-visible:outline-acc"
      >
        {/* check indicator */}
        <span
          aria-hidden
          className={`mono mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border t-med ${
            selected ? 'border-acc bg-acc text-on-acc' : 'border-line-strong text-transparent group-hover:border-acc/50'
          }`}
        >
          <Check size={11} strokeWidth={2.5} />
        </span>

        <span className="min-w-0 flex-1">
          <span className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <span className={`mono text-[13px] font-semibold ${selected ? 'text-acc' : 'text-fg/80'}`}>{p.code}</span>
            <span className="block whitespace-pre-line text-pretty text-[14.5px] leading-snug text-fg/90">
              {p.statement}
            </span>
          </span>
        </span>
      </button>

      {/* covered-in strip — real links into the notes */}
      <div className="flex flex-wrap items-center gap-x-2 gap-y-1 border-t border-line/60 px-4 py-2 sm:px-5">
        {disabled ? (
          <span className="mono text-[10.5px] uppercase tracking-[0.12em] text-faint">
            // no section notes cover this point yet
          </span>
        ) : (
          <>
            <span className="mono text-[10px] uppercase tracking-[0.14em] text-faint">covered in</span>
            {p.sections.map((s, idx) => (
              <React.Fragment key={s.sectionKey}>
                {idx > 0 && <span aria-hidden className="text-[10px] text-faint">·</span>}
                <button
                  type="button"
                  onClick={() => go(`/topic/${p.topicSlug}/${s.sectionKey}`)}
                  aria-label={`Open ${s.title} in topic ${p.topicNumber}`}
                  className="mono rounded text-[11px] text-muted underline-offset-2 t-fast hover:text-acc hover:underline focus-visible:outline-acc"
                >
                  {s.title}
                </button>
              </React.Fragment>
            ))}
          </>
        )}
      </div>
    </div>
  )
}
