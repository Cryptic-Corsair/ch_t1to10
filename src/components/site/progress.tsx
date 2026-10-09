'use client'

import React, { useMemo, useState } from 'react'
import { RotateCcw } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { BtnGhost, Chip, ProgressRing, gridShell, cardCell, eyebrowText } from './ui-bits'
import { useCards, useProgress, useSettings } from '@/lib/site/stores'

export function ProgressView({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const { read, activity, reset } = useProgress()
  const cards = useCards()
  const mode = useSettings((s) => s.uiMode)
  const [confirmReset, setConfirmReset] = useState(false)

  const totalSections = useMemo(() => topics.reduce((a, t) => a + t.sections.length, 0), [topics])
  const doneSections = hydrated
    ? topics.reduce((a, t) => a + t.sections.filter((s) => read[`${t.slug}/${s.sectionKey}`]).length, 0)
    : 0
  const overallPct = totalSections ? (doneSections / totalSections) * 100 : 0

  const cardTotal = useMemo(() => topics.reduce((a, t) => a + t.cards.length, 0), [topics])
  const cardsKnown = hydrated
    ? topics.reduce((a, t) => a + t.cards.filter((c) => cards.stats[c.id]?.last === 'known').length, 0)
    : 0
  const cardsAgain = hydrated
    ? topics.reduce((a, t) => a + t.cards.filter((c) => cards.stats[c.id]?.last === 'again').length, 0)
    : 0
  const cardsUntouched = cardTotal - cardsKnown - cardsAgain

  // last 14 days strip
  const days = useMemo(() => {
    const out: { date: string; count: number }[] = []
    for (let i = 13; i >= 0; i--) {
      const d = new Date()
      d.setDate(d.getDate() - i)
      const key = d.toISOString().slice(0, 10)
      out.push({ date: key, count: hydrated ? activity.filter((x) => x === key).length : 0 })
    }
    return out
  }, [activity, hydrated])
  const maxDay = Math.max(1, ...days.map((d) => d.count))
  const activeDays = days.filter((d) => d.count > 0).length

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-12">
      <p className="eyebrow">{eyebrowText(mode, 'Telemetry')}</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        Your <span className="serif-accent text-acc">progress</span>.
      </h1>
      <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
        Everything here lives in your browser only — no account, no server, no tracking.
        Numbers update the moment you mark a section or grade a card.
      </p>

      {/* overview */}
      <div className={gridShell(mode, 'mt-10 lg:grid-cols-3')}>
        <div className={`flex items-center gap-6 p-7 ${cardCell(mode)}`}>
          <ProgressRing value={overallPct} size={110}>
            <span className="mono text-2xl font-medium text-fg">{Math.round(overallPct)}%</span>
            <span className="mono text-[9px] uppercase tracking-[0.16em] text-faint">syllabus</span>
          </ProgressRing>
          <div>
            <p className="mono text-[10px] uppercase tracking-[0.16em] text-faint">Sections read</p>
            <p className="mono mt-1 text-xl text-fg">{doneSections}<span className="text-faint">/{totalSections}</span></p>
            <p className="mono mt-3 text-[10px] uppercase tracking-[0.16em] text-faint">Active days (14d)</p>
            <p className="mono mt-1 text-xl text-fg">{activeDays}</p>
          </div>
        </div>

        <div className={`flex flex-col justify-center p-7 ${cardCell(mode)}`}>
          <p className="mono mb-4 text-[10px] uppercase tracking-[0.16em] text-faint">Flashcards — verdict on latest grade</p>
          {[
            ['known', cardsKnown, 'text-acc'],
            ['again', cardsAgain, 'text-fg'],
            ['untouched', cardsUntouched, 'text-faint'],
          ].map(([label, n, cls]) => {
            const w = cardTotal ? ((n as number) / cardTotal) * 100 : 0
            return (
              <div key={label as string} className="mb-3 last:mb-0">
                <div className="mb-1 flex items-baseline justify-between">
                  <span className="mono text-[11px] uppercase tracking-[0.12em] text-muted">{label as string}</span>
                  <span className={`mono text-[12px] ${cls as string}`}>{n as number}</span>
                </div>
                <div className="h-1 overflow-hidden rounded-full bg-code">
                  <div className={`h-full rounded-full t-med ${label === 'known' ? 'bg-acc' : label === 'again' ? 'bg-faint' : 'bg-line-strong'}`} style={{ width: `${w}%` }} />
                </div>
              </div>
            )
          })}
        </div>

        <div className={`p-7 ${cardCell(mode)}`}>
          <p className="mono mb-4 text-[10px] uppercase tracking-[0.16em] text-faint">Study log — last 14 days</p>
          <div className="grid grid-cols-7 gap-1.5">
            {days.map((d) => {
              const level = d.count === 0 ? 0 : d.count / maxDay
              return (
                <div
                  key={d.date}
                  title={`${d.date} — ${d.count} action${d.count === 1 ? '' : 's'}`}
                  className="aspect-square rounded-[4px] border border-line"
                  style={{
                    backgroundColor: level === 0 ? 'transparent' : `color-mix(in srgb, var(--acc) ${Math.round(25 + level * 75)}%, transparent)`,
                  }}
                />
              )
            })}
          </div>
          <p className="mono mt-3 text-[10px] text-faint">
            {mode === 'terminal' ? '// one square per day · intensity = activity' : 'One square per day · intensity = activity.'}
          </p>
        </div>
      </div>

      {/* per-topic */}
      <h2 className="mono mb-4 mt-12 text-[12px] font-medium uppercase tracking-[0.18em] text-fg">By topic</h2>
      <div className="overflow-hidden rounded-xl border border-line">
        {topics.map((t, i) => {
          const done = hydrated ? t.sections.filter((s) => read[`${t.slug}/${s.sectionKey}`]).length : 0
          const pct = t.sections.length ? (done / t.sections.length) * 100 : 0
          const known = hydrated ? t.cards.filter((c) => cards.stats[c.id]?.last === 'known').length : 0
          return (
            <button
              key={t.slug}
              onClick={() => go(`/topic/${t.slug}`)}
              className={`group grid w-full grid-cols-[auto_1fr_auto] items-center gap-4 px-4 py-4 text-left t-fast hover:bg-elev sm:px-6 ${
                i > 0 ? 'border-t border-line' : ''
              }`}
            >
              <span className="mono w-7 text-[13px] text-faint t-fast group-hover:text-acc">
                {String(t.number).padStart(2, '0')}
              </span>
              <span className="min-w-0">
                <span className="mb-1.5 block truncate text-[13.5px] font-medium text-fg t-fast group-hover:text-acc">
                  {t.title}
                </span>
                <span className="block h-1 overflow-hidden rounded-full bg-code">
                  {hydrated && pct > 0 && <span className="block h-full rounded-full bg-acc t-med" style={{ width: `${pct}%` }} />}
                </span>
              </span>
              <span className="mono whitespace-nowrap text-[11px] text-faint">
                {done}/{t.sections.length} · {known}/{t.cards.length} cards
              </span>
            </button>
          )
        })}
      </div>

      {/* data controls */}
      <div className="mt-12 rounded-xl border border-line bg-surface p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="mono text-[11px] uppercase tracking-[0.16em] text-fg">Data controls</p>
            <p className="mt-1.5 text-[13px] text-muted">
              Progress and card scores are stored locally. Resetting wipes both — permanently.
            </p>
          </div>
          <div className="flex gap-2">
            {confirmReset ? (
              <>
                <Chip accent>sure?</Chip>
                <BtnGhost onClick={() => { reset(); cards.reset(); setConfirmReset(false) }}>
                  <RotateCcw size={13} /> Yes, wipe it
                </BtnGhost>
                <BtnGhost onClick={() => setConfirmReset(false)}>Cancel</BtnGhost>
              </>
            ) : (
              <BtnGhost onClick={() => setConfirmReset(true)}>
                <RotateCcw size={13} /> Reset all progress
              </BtnGhost>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
