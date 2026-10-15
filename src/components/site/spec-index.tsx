'use client'

/*
 * SPEC INDEX — every assessment statement, worded exactly as the
 * specification words it, grouped by topic. Tick the points you want
 * and the same ticks drive the custom revision notes at #/notes.
 */

import React, { useMemo } from 'react'
import { Check, CheckCheck, ListChecks, NotebookPen, X } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { buildSpecIndex, type SpecPoint } from '@/lib/site/spec'
import { useSettings, useSpecPicks } from '@/lib/site/stores'
import { BtnGhost, BtnSolid, eyebrowText } from './ui-bits'

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

  const index = useMemo(() => buildSpecIndex(topics), [topics])

  const groups = useMemo(() => {
    const out: { topicSlug: string; topicNumber: number; topicTitle: string; points: SpecPoint[] }[] = []
    for (const p of index) {
      const last = out[out.length - 1]
      if (last && last.topicSlug === p.topicSlug) last.points.push(p)
      else out.push({ topicSlug: p.topicSlug, topicNumber: p.topicNumber, topicTitle: p.topicTitle, points: [p] })
    }
    return out
  }, [index])

  const pickedSet = useMemo(() => new Set(picks), [picks])

  const toggleTopic = (g: { points: SpecPoint[] }) => {
    const selectable = g.points.filter((p) => p.sections.length > 0).map((p) => p.code)
    if (selectable.length === 0) return
    const all = selectable.every((c) => pickedSet.has(c))
    setPicks(all ? picks.filter((c) => !selectable.includes(c)) : [...new Set([...picks, ...selectable.filter((c) => !pickedSet.has(c))])])
  }

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-12">
      {/* ---------- masthead ---------- */}
      <p className="eyebrow">{eyebrowText(mode, 'Specification')}</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        The spec <span className="serif-accent text-acc">index</span>.
      </h1>
      <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
        Every assessment statement from the 2018 specification, worded exactly as it words them —
        all {index.length} points across topics 1–10. Tick the points you want to revise and build a
        custom note set; the full notes behind each ticked point are pulled together for you at{' '}
        <button onClick={() => go('/notes')} className="text-acc underline decoration-acc/40 underline-offset-2 t-fast hover:decoration-acc">
          custom notes
        </button>
        .
      </p>

      {/* ---------- action bar ---------- */}
      <div
        className={`mt-8 flex flex-wrap items-center gap-x-6 gap-y-4 rounded-xl px-5 py-4 ${
          mode === 'terminal' ? 'border border-line bg-surface' : 'lab-glass rounded-[16px]'
        }`}
      >
        <p className="flex items-center gap-2.5 text-[14px] text-fg">
          <ListChecks size={15} strokeWidth={1.75} className="text-acc" />
          <span className="font-semibold">{picks.length}</span>
          <span className="text-muted">of {index.length} points selected</span>
        </p>
        <div className="ms-auto flex flex-wrap items-center gap-2.5">
          {picks.length > 0 && (
            <BtnGhost onClick={clear} ariaLabel="Clear selection">
              <X size={14} />
              Clear
            </BtnGhost>
          )}
          <BtnSolid
            onClick={() => go('/notes')}
            ariaLabel="Build custom notes from the selected points"
            className={picks.length === 0 ? 'pointer-events-none opacity-40' : ''}
          >
            <NotebookPen size={14} />
            Custom notes{picks.length > 0 ? ` · ${picks.length}` : ''}
          </BtnSolid>
        </div>
      </div>

      {/* ---------- per-topic point lists ---------- */}
      <div className={mode === 'terminal' ? 'mt-10 space-y-10' : 'mt-10 space-y-12'}>
        {groups.map((g) => {
          const selectable = g.points.filter((p) => p.sections.length > 0).map((p) => p.code)
          const allPicked = selectable.length > 0 && selectable.every((c) => pickedSet.has(c))
          const somePicked = selectable.some((c) => pickedSet.has(c))
          return (
            <section key={g.topicSlug} aria-label={`Topic ${g.topicNumber} — ${g.topicTitle}`}>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
                <h2 className="flex items-baseline gap-3 text-[17px] font-semibold tracking-tight text-fg">
                  <span className="mono text-[13px] text-faint">{String(g.topicNumber).padStart(2, '0')}</span>
                  {g.topicTitle}
                </h2>
                <span className="mono text-[10px] uppercase tracking-[0.16em] text-faint">
                  {g.points.length} points
                </span>
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
                {g.points.map((p, i) => (
                  <PointRow
                    key={p.code}
                    point={p}
                    index={i}
                    count={g.points.length}
                    selected={pickedSet.has(p.code)}
                    onToggle={() => toggle(p.code)}
                    mode={mode}
                  />
                ))}
              </div>
            </section>
          )
        })}
      </div>
    </div>
  )
}

function PointRow({
  point: p, index: i, count, selected, onToggle, mode,
}: {
  point: SpecPoint
  index: number
  count: number
  selected: boolean
  onToggle: () => void
  mode: string
}) {
  const disabled = p.sections.length === 0
  const rowBase = 'group flex w-full items-start gap-4 px-4 py-3.5 text-left sm:gap-5 sm:px-5'
  const rowSkin =
    mode === 'terminal'
      ? [
          i > 0 ? 'border-t border-line' : '',
          selected ? 'bg-elev' : '',
          disabled ? 'opacity-45' : 't-fast hover:bg-elev/60 focus-visible:bg-elev',
        ].join(' ')
      : [
          'lab-glass rounded-[14px]',
          selected ? '!border-[color-mix(in_srgb,var(--acc)_55%,transparent)]' : '',
          disabled ? 'opacity-45' : 't-fast hover:!border-[color-mix(in_srgb,var(--acc)_35%,transparent)] focus-visible:outline-acc',
        ].join(' ')

  return (
    <button
      type="button"
      onClick={disabled ? undefined : onToggle}
      disabled={disabled}
      aria-pressed={selected}
      aria-label={`Specification point ${p.code}${selected ? ' — selected' : ''}`}
      className={`${rowBase} ${rowSkin} focus-visible:outline-acc`}
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
        <span className="mono mt-2 block text-[10.5px] uppercase tracking-[0.12em] text-faint">
          {disabled
            ? '// no section notes cover this point yet'
            : p.sections.length === 1
              ? `covered in: ${p.sections[0].title}`
              : `covered in: ${p.sections.map((s) => s.title).join(' · ')}`}
        </span>
      </span>
    </button>
  )
}
