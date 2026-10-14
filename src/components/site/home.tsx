'use client'

import React, { useEffect } from 'react'
import { ArrowRight, ArrowUpRight } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { BtnGhost, gridShell, cardCell, hoverCell, eyebrowText } from './ui-bits'
import { useProgress, useSettings, type UiMode } from '@/lib/site/stores'
import { DoodleField, TOPIC_DOODLES } from './doodles'

interface HomeProps {
  topics: TopicData[]
  stats: { sections: number; cards: number; noted: number }
  go: (to: string) => void
  openSettings: () => void
  hydrated: boolean
}

const pad = (n: number) => String(n).padStart(2, '0')

/* motion guard — honours both the Control Room switch and the OS setting */
function prefersReduced(): boolean {
  if (typeof window === 'undefined') return true
  return (
    document.documentElement.dataset.motion === 'reduced' ||
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  )
}

/* ============================================================
   ENTRANCE REVEALS — one IntersectionObserver, armed only when
   motion is welcome. No JS → no arming → everything visible.
   ============================================================ */

function useReveal(mode: UiMode) {
  useEffect(() => {
    if (prefersReduced()) return
    if (!('IntersectionObserver' in window)) return
    const root = document.documentElement
    root.classList.add('reveal-armed')
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            e.target.classList.add('is-in')
            io.unobserve(e.target)
          }
        }
      },
      { threshold: 0.1, rootMargin: '0px 0px -7% 0px' }
    )
    document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el))
    return () => {
      io.disconnect()
      root.classList.remove('reveal-armed')
    }
  }, [mode])
}

/* ============================================================
   THE TOPICS — the homepage. Deliberately simple: two units,
   ten rows, one hairline of reading progress each. The doodles
   live in the margins; the list stays calm.
   ============================================================ */

function TopicRow({
  t, go, readMap, hydrated, mode,
}: {
  t: TopicData; go: (to: string) => void
  readMap: Record<string, true>; hydrated: boolean; mode: UiMode
}) {
  const done = hydrated ? t.sections.filter((s) => readMap[`${t.slug}/${s.sectionKey}`]).length : 0
  const pct = t.sections.length ? (done / t.sections.length) * 100 : 0
  const hasNotes = t.sections.some((s) => s.content)
  return (
    <button
      onClick={() => go(`/topic/${t.slug}`)}
      title={t.title}
      aria-label={`Topic ${pad(t.number)}: ${t.title}`}
      className={`group relative flex min-h-[84px] items-center gap-5 p-5 pr-4 text-left focus-visible:outline-acc ${cardCell(mode)} ${hoverCell(mode)}`}
    >
      <span className="mono w-8 shrink-0 text-[13px] text-faint t-fast group-hover:text-acc">{pad(t.number)}</span>
      <span className="min-w-0 flex-1">
        <span className="flex items-center gap-2">
          <span className="truncate text-[15px] font-semibold tracking-tight text-fg">{t.title}</span>
          {!hasNotes && (
            <span className="mono shrink-0 rounded border border-dashed border-line px-1 py-0.5 text-[8.5px] uppercase tracking-[0.14em] text-faint">
              queued
            </span>
          )}
        </span>
        <span className="mono mt-1.5 block text-[10px] uppercase tracking-[0.12em] text-faint">
          {t.sections.length} sections · {t.estHours} h{hydrated && done > 0 ? ` · ${done} read` : ''}
        </span>
      </span>
      <ArrowUpRight
        size={15}
        aria-hidden
        className="shrink-0 text-faint opacity-0 t-fast group-hover:translate-x-0.5 group-hover:text-acc group-hover:opacity-100"
      />
      {hydrated && pct > 0 && <span className="row-progress" style={{ width: `${pct}%` }} aria-hidden />}
    </button>
  )
}

function TopicsSection({
  topics, go, readMap, hydrated, mode,
}: {
  topics: TopicData[]; go: (to: string) => void
  readMap: Record<string, true>; hydrated: boolean; mode: UiMode
}) {
  const units = [1, 2].map((u) => ({
    u,
    topics: topics.filter((t) => t.unit === u),
    code: u === 1 ? 'WCH11' : 'WCH12',
    name: topics.find((t) => t.unit === u)?.unitName ?? '',
  }))
  return (
    <section className="relative overflow-hidden">
      <DoodleField items={TOPIC_DOODLES} />
      <div className="relative mx-auto max-w-[1200px] px-6 py-16 sm:py-24">
        <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow mb-3">{eyebrowText(mode, 'The topics')}</p>
            <h1 className="text-[clamp(24px,2.8vw,32px)] font-semibold leading-[1.2] tracking-tight">
              Ten topics. <span className="serif-accent text-acc">Two papers.</span>
            </h1>
            <p className="mt-2 max-w-xl text-sm text-muted">
              Pick a topic — every section inside sits under its exact specification
              statement, and your reading progress follows you.
            </p>
          </div>
          <BtnGhost onClick={() => go('/topics')}>
            All topics <ArrowRight size={13} />
          </BtnGhost>
        </div>
        <div className="space-y-10">
          {units.map((p) => (
            <div key={p.u} data-reveal>
              <div className="mb-3 flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <span className="mono text-[11px] font-medium uppercase tracking-[0.2em] text-acc">
                  Unit {p.u} — {p.code}
                </span>
                <span className="mono text-[10px] text-faint">{p.name}</span>
              </div>
              <div className={gridShell(mode, p.topics.length % 2 ? 'sm:grid-cols-2 sm:[&>*:nth-child(5)]:col-span-2' : 'sm:grid-cols-2')}>
                {p.topics.map((t) => (
                  <TopicRow key={t.slug} t={t} go={go} readMap={readMap} hydrated={hydrated} mode={mode} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ============================================================
   HOME — the topics, on a doodled margin. Footer lives in the shell.
   ============================================================ */

export function Home({ topics, go, hydrated }: HomeProps) {
  const mode = useSettings((s) => s.uiMode)
  const read = useProgress((st) => st.read)
  const readMap = hydrated ? read : ({} as Record<string, true>)

  useReveal(mode)

  return (
    <div className="home-root relative isolate">
      {/* faint notebook-doodle tile across the entire homepage */}
      <div className="doodle-tile" aria-hidden />
      <TopicsSection topics={topics} go={go} readMap={readMap} hydrated={hydrated} mode={mode} />
    </div>
  )
}
