'use client'

/*
 * CUSTOM NOTES — the revision set you build yourself. Tick spec points in
 * the spec index and this page gathers the full notes behind them: every
 * selected point's sections, in syllabus order, rendered whole.
 */

import React, { useMemo } from 'react'
import { ArrowUpRight, ListChecks, NotebookPen, PencilRuler, SlidersHorizontal } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { buildSpecIndex, sectionsForPicks } from '@/lib/site/spec'
import { useSettings, useSpecPicks } from '@/lib/site/stores'
import { BlockRenderer, BulletCard, Inline, groupBlocks } from './blocks'
import { BtnGhost, BtnSolid, eyebrowText } from './ui-bits'

export function CustomNotes({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const mode = useSettings((s) => s.uiMode)
  const picks = useSpecPicks((s) => s.picks)
  const clear = useSpecPicks((s) => s.clear)

  const groups = useMemo(() => sectionsForPicks(topics, picks), [topics, picks])
  /* verbatim statements, straight from each topic's specification-map table */
  const statementOf = useMemo(() => {
    const m = new Map<string, string>()
    for (const p of buildSpecIndex(topics)) m.set(p.code, p.statement)
    return m
  }, [topics])
  const sectionCount = groups.reduce((a, g) => a + g.sections.length, 0)
  const anyContent = groups.some((g) => g.sections.some((s) => s.section.content))

  return (
    <div className="mx-auto max-w-[900px] px-6 pb-20 pt-12">
      {/* ---------- masthead ---------- */}
      <p className="eyebrow">{eyebrowText(mode, 'Revision set')}</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        Custom <span className="serif-accent text-acc">notes</span>.
      </h1>
      {picks.length > 0 ? (
        <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
          {picks.length} specification point{picks.length === 1 ? '' : 's'} · {sectionCount} section
          {sectionCount === 1 ? '' : 's'} of notes, pulled together in syllabus order. Everything
          below is your normal topic notes — assembled around the points you picked.
        </p>
      ) : (
        <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
          Pick the specification points you want to revise and their full notes appear here as one
          personalised set.
        </p>
      )}

      {/* ---------- actions ---------- */}
      <div className="mt-7 flex flex-wrap items-center gap-2.5">
        <BtnGhost onClick={() => go('/spec')} ariaLabel="Edit the selected specification points">
          <SlidersHorizontal size={14} />
          Edit selection
        </BtnGhost>
        {picks.length > 0 && (
          <BtnGhost onClick={clear} ariaLabel="Clear the selection">
            <ListChecks size={14} />
            Clear selection
          </BtnGhost>
        )}
      </div>

      {/* ---------- empty state ---------- */}
      {picks.length === 0 && (
        <div
          className={`mt-10 px-8 py-14 text-center ${
            mode === 'terminal' ? 'rounded-xl border border-dashed border-line-strong bg-surface/40' : 'lab-glass rounded-[20px]'
          }`}
        >
          <span className="mx-auto flex h-11 w-11 items-center justify-center rounded-full border border-acc/30 bg-acc/10 text-acc">
            <NotebookPen size={18} strokeWidth={1.75} />
          </span>
          <h2 className="mt-5 text-lg font-semibold tracking-tight text-fg">Nothing picked yet</h2>
          <p className="mx-auto mt-2 max-w-[420px] text-[14px] leading-relaxed text-muted">
            Head to the spec index and tick, say, <span className="mono text-[13px] text-fg">5.6</span> and{' '}
            <span className="mono text-[13px] text-fg">8.3</span> — the notes covering those points
            will assemble here automatically.
          </p>
          <div className="mt-6 flex justify-center">
            <BtnSolid onClick={() => go('/spec')}>
              <ListChecks size={14} />
              Browse the spec index
            </BtnSolid>
          </div>
        </div>
      )}

      {/* ---------- the notes ---------- */}
      {picks.length > 0 && !anyContent && (
        <p className="mono mt-10 rounded-xl border border-dashed border-line px-5 py-4 text-[12px] text-muted">
          {'// the picked points don’t have written notes behind them yet — pick more points or check back soon'}
        </p>
      )}

      <div className="mt-12 space-y-14">
        {groups.map((g) => (
          <section key={g.topic.slug} aria-label={`Topic ${g.topic.number} — ${g.topic.title}`}>
            {/* topic divider */}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-line pb-4">
              <h2 className="flex items-baseline gap-3 text-[17px] font-semibold tracking-tight text-fg">
                <span className="mono text-[13px] text-faint">{String(g.topic.number).padStart(2, '0')}</span>
                {g.topic.title}
              </h2>
              <span className="mono text-[10px] uppercase tracking-[0.16em] text-faint">
                {g.topic.unitCode} · {g.sections.length} section{g.sections.length === 1 ? '' : 's'}
              </span>
            </div>

            {/* sections */}
            <div className="mt-6 space-y-10">
              {g.sections.map(({ section: s, viaPicks }) => (
                <article key={s.sectionKey} className="blk-wrap">
                  {/* section head */}
                  <div className="flex flex-wrap items-start justify-between gap-x-6 gap-y-3">
                    <div className="min-w-0">
                      <p className="mono text-[10.5px] uppercase tracking-[0.18em] text-faint">
                        Section {s.number}
                      </p>
                      <h3 className="mt-1.5 text-[19px] font-semibold tracking-tight text-fg">{s.title}</h3>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                      {viaPicks.map((code) => (
                        <span
                          key={code}
                          className="mono rounded-full border border-acc/40 bg-acc/10 px-2.5 py-1 text-[10.5px] font-semibold tracking-[0.06em] text-acc"
                        >
                          {code}
                        </span>
                      ))}
                      <BtnGhost onClick={() => go(`/topic/${g.topic.slug}/${s.sectionKey}`)} ariaLabel={`Open ${s.title} in its topic`}>
                        <ArrowUpRight size={14} />
                        Topic {String(g.topic.number).padStart(2, '0')}
                      </BtnGhost>
                    </div>
                  </div>

                  {/* the picked statements, worded exactly as the spec words them */}
                  {viaPicks.map((code) =>
                    statementOf.get(code) ? (
                      <div key={code} className="spec-point spec-point-flat mt-4" aria-label={`Specification point ${code}`}>
                        <div className="spec-point-summary">
                          <div className="spec-point-head">
                            <span className="spec-point-label">Specification point {code}</span>
                            <span className="spec-point-statement text-pretty whitespace-pre-line">
                              <Inline text={statementOf.get(code)!} />
                            </span>
                          </div>
                        </div>
                      </div>
                    ) : null
                  )}

                  {/* content */}
                  {s.content ? (
                    <div className="mt-6">
                      {groupBlocks(s.content).map((seg, segI) =>
                        seg.kind === 'group' ? (
                          <BulletCard key={segI} blocks={seg.blocks} />
                        ) : (
                          <BlockRenderer key={segI} block={seg.block} lead={segI === 0} />
                        )
                      )}
                    </div>
                  ) : (
                    <div className="mt-6 rounded-2xl border border-dashed border-line-strong bg-surface/50 px-6 py-7">
                      <div className="flex items-center gap-3">
                        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-acc/30 bg-acc/10 text-acc">
                          <PencilRuler size={15} strokeWidth={1.75} />
                        </span>
                        <p className="text-[14px] font-medium text-fg">Full notes for this section are on the way</p>
                      </div>
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
