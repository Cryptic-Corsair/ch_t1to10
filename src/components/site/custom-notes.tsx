'use client'

/*
 * CUSTOM NOTES — the set you build yourself. Tick spec points in
 * the spec index and this page gathers the full notes behind them: every
 * selected point's sections, in syllabus order, rendered whole. Sections
 * can be ticked off as read, the verbatim statements can be hidden for a
 * cleaner pass, and the whole set prints or copies as plain text.
 * Studio + Hybrid get the glass treatment: masthead panel, topic bands,
 * dash-kickered section heads — same content, studio voice.
 */

import React, { useMemo, useState } from 'react'
import { ArrowUpRight, Eye, EyeOff, ListChecks, NotebookPen, PencilRuler, Printer, SlidersHorizontal } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { buildSpecIndex, sectionsForPicks } from '@/lib/site/spec'
import { useProgress, useSettings, useSpecPicks } from '@/lib/site/stores'
import { BlockRenderer, BulletCard, Inline, groupBlocks } from './blocks'
import { BtnGhost, BtnSolid, CopyBtn, ProgressBar, ReadToggle, eyebrowText } from './ui-bits'
import { RevisionSets } from './revision-sets'

const pad2 = (n: number) => String(n).padStart(2, '0')

export function CustomNotes({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const mode = useSettings((s) => s.uiMode)
  const picks = useSpecPicks((s) => s.picks)
  const clear = useSpecPicks((s) => s.clear)
  const { read, markRead, markUnread } = useProgress()

  const [showStatements, setShowStatements] = useState(true)

  const groups = useMemo(() => sectionsForPicks(topics, picks), [topics, picks])
  /* verbatim statements, straight from each topic's specification-map table */
  const statementOf = useMemo(() => {
    const m = new Map<string, string>()
    for (const p of buildSpecIndex(topics)) m.set(p.code, p.statement)
    return m
  }, [topics])
  const sectionCount = groups.reduce((a, g) => a + g.sections.length, 0)
  const readCount = groups.reduce(
    (a, g) => a + g.sections.filter(({ section }) => read[`${g.topic.slug}/${section.sectionKey}`]).length,
    0
  )
  const anyContent = groups.some((g) => g.sections.some((s) => s.section.content))

  /* studio-skinned chrome (Studio + Hybrid); terminal keeps the flat reading room */
  const glass = mode !== 'terminal'

  /* plain-text export of the whole set, for pasting into a doc or a message */
  const exportText = useMemo(() => {
    const lines: string[] = ['IAL Chemistry — custom notes']
    lines.push(`${picks.length} spec point${picks.length === 1 ? '' : 's'} · ${sectionCount} section${sectionCount === 1 ? '' : 's'}`)
    for (const g of groups) {
      lines.push('', `— Topic ${pad2(g.topic.number)} · ${g.topic.title} —`)
      for (const { section: s, viaPicks } of g.sections) {
        lines.push('', `[${s.number}] ${s.title}  (${viaPicks.join(', ')})`)
        for (const code of viaPicks) {
          const st = statementOf.get(code)
          if (st) lines.push(`  ${code} — ${st.replace(/\s*\n\s*/g, ' ')}`)
        }
      }
    }
    return lines.join('\n')
  }, [groups, picks, statementOf, sectionCount])

  /* ---------- shared masthead fragments (both voices) ---------- */
  const introCopy =
    picks.length > 0 ? (
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
    )

  const pickedRow = (
    <p className="mono flex flex-wrap items-baseline gap-x-2 gap-y-1 text-[11px] text-faint">
      <span className="uppercase tracking-[0.16em]">picked:</span>
      {picks.slice(0, 10).map((code) => (
        <span key={code} className="font-semibold text-acc">{code}</span>
      ))}
      {picks.length > 10 && <span>+ {picks.length - 10} more</span>}
    </p>
  )

  const progressRow = (
    <div className="flex max-w-md items-center gap-3">
      <ProgressBar value={(readCount / sectionCount) * 100} className="flex-1" />
      <span className="mono shrink-0 text-[10px] uppercase tracking-[0.14em] text-faint">
        {readCount}/{sectionCount} read
      </span>
    </div>
  )

  const actionsRow = (
    <div className="flex flex-wrap items-center gap-2.5 print:hidden">
      <BtnGhost onClick={() => go('/spec')} ariaLabel="Edit the selected specification points">
        <SlidersHorizontal size={14} />
        Edit selection
      </BtnGhost>
      <RevisionSets mode={mode} />
      {picks.length > 0 && (
        <BtnGhost
          onClick={() => setShowStatements((v) => !v)}
          ariaLabel={showStatements ? 'Hide the verbatim statements' : 'Show the verbatim statements'}
        >
          {showStatements ? <EyeOff size={14} /> : <Eye size={14} />}
          {showStatements ? 'Hide statements' : 'Show statements'}
        </BtnGhost>
      )}
      {picks.length > 0 && <CopyBtn text={exportText} label="Copy set" className="px-3! py-2.5! text-xs!" />}
      {sectionCount > 0 && (
        <BtnGhost onClick={() => window.print()} ariaLabel="Print this revision set">
          <Printer size={14} />
          Print set
        </BtnGhost>
      )}
      {picks.length > 0 && (
        <BtnGhost onClick={clear} ariaLabel="Clear the selection">
          <ListChecks size={14} />
          Clear selection
        </BtnGhost>
      )}
    </div>
  )

  return (
    <div className="mx-auto max-w-[900px] px-6 pb-20 pt-12">
      {/* ---------- masthead ---------- */}
      {glass ? (
        /* STUDIO — the instrument panel: chip, gradient title, glass controls */
        <header className="lab-glass rounded-[26px] p-7 sm:p-10">
          <span className="lab-chip">{eyebrowText(mode, 'Your set')}</span>
          <h1 className="mt-5 text-3xl font-semibold tracking-tight sm:text-4xl">
            Custom <span className="serif-accent text-acc">notes</span>.
          </h1>
          {introCopy}
          {picks.length > 0 && <div className="mt-6">{pickedRow}</div>}
          {sectionCount > 0 && <div className="mt-5">{progressRow}</div>}
          <div className="mt-7">{actionsRow}</div>
        </header>
      ) : (
        /* FOCUS — the flat reading-room masthead */
        <header>
          <p className="eyebrow">{eyebrowText(mode, 'Your set')}</p>
          <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
            Custom <span className="serif-accent text-acc">notes</span>.
          </h1>
          {introCopy}
          {picks.length > 0 && <div className="mt-3">{pickedRow}</div>}
          {sectionCount > 0 && <div className="mt-5">{progressRow}</div>}
          <div className="mt-7">{actionsRow}</div>
        </header>
      )}

      {/* ---------- empty state ---------- */}
      {picks.length === 0 && (
        <div
          className={`mt-10 px-8 py-14 text-center ${
            !glass ? 'rounded-xl border border-dashed border-line-strong bg-surface/40' : 'lab-glass rounded-[22px]'
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
        <p
          className={`mono mt-10 rounded-xl border px-5 py-4 text-[12px] leading-relaxed text-muted ${
            glass ? 'lab-glass' : 'border-dashed border-line'
          }`}
        >
          {'// the picked points don’t have written notes behind them yet — pick more points or check back soon'}
        </p>
      )}

      <div className="mt-12 space-y-14">
        {groups.map((g) => (
          <section key={g.topic.slug} aria-label={`Topic ${g.topic.number} — ${g.topic.title}`}>
            {/* topic divider — glass band in Studio, hairline in Focus */}
            <div
              className={
                glass
                  ? 'lab-glass flex flex-wrap items-center gap-x-4 gap-y-2.5 rounded-[18px] px-5 py-4'
                  : 'flex flex-wrap items-center gap-x-4 gap-y-2 border-b border-line pb-4'
              }
            >
              {glass ? (
                <span className="lab-num-chip shrink-0" aria-hidden>
                  {pad2(g.topic.number)}
                </span>
              ) : null}
              <h2 className="flex items-baseline gap-3 text-[17px] font-semibold tracking-tight text-fg">
                {!glass && <span className="mono text-[13px] text-faint">{pad2(g.topic.number)}</span>}
                {g.topic.title}
              </h2>
              <span className={`mono text-[10px] uppercase tracking-[0.16em] text-faint ${glass ? 'ms-auto' : ''}`}>
                {g.topic.unitCode} · {g.sections.length} section{g.sections.length === 1 ? '' : 's'}
              </span>
            </div>

            {/* sections */}
            <div className={glass ? 'mt-7 space-y-12' : 'mt-6 space-y-10'}>
              {g.sections.map(({ section: s, viaPicks }) => {
                const isRead = !!read[`${g.topic.slug}/${s.sectionKey}`]
                return (
                  <article key={s.sectionKey} className="blk-wrap">
                    {/* section head */}
                    <div className="flex flex-wrap items-start justify-between gap-x-6 gap-y-3">
                      <div className="min-w-0">
                        {glass ? (
                          <>
                            <span aria-hidden className="warm-dash block" />
                            <p className="mono mt-4 text-[13px] font-bold tracking-tight text-acc">
                              Section {s.number}
                            </p>
                          </>
                        ) : (
                          <p className="mono text-[10.5px] uppercase tracking-[0.18em] text-faint">
                            Section {s.number}
                          </p>
                        )}
                        <h3
                          className={`${glass ? 'display-serif mt-2 text-[21px]' : 'mt-1.5 text-[19px]'} font-semibold tracking-tight ${
                            isRead ? 'text-muted' : 'text-fg'
                          }`}
                        >
                          {s.title}
                        </h3>
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
                        <span className="print:hidden">
                          <ReadToggle
                            read={isRead}
                            onToggle={() =>
                              isRead ? markUnread(g.topic.slug, s.sectionKey) : markRead(g.topic.slug, s.sectionKey)
                            }
                            label={`${isRead ? 'Mark' : 'Mark'} ${s.title} ${isRead ? 'as not read' : 'as read'}`}
                          />
                        </span>
                        <span className="print:hidden">
                          <BtnGhost
                            onClick={() => go(`/topic/${g.topic.slug}/${s.sectionKey}`)}
                            ariaLabel={`Open ${s.title} in its topic`}
                          >
                            <ArrowUpRight size={14} />
                            Topic {pad2(g.topic.number)}
                          </BtnGhost>
                        </span>
                      </div>
                    </div>

                    {/* the picked statements, worded exactly as the spec words them */}
                    {showStatements &&
                      viaPicks.map((code) =>
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
                      <div className={`mt-6 px-6 py-7 ${glass ? 'lab-glass rounded-[18px]' : 'rounded-2xl border border-dashed border-line-strong bg-surface/50'}`}>
                        <div className="flex items-center gap-3">
                          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-acc/30 bg-acc/10 text-acc">
                            <PencilRuler size={15} strokeWidth={1.75} />
                          </span>
                          <p className="text-[14px] font-medium text-fg">Full notes for this section are on the way</p>
                        </div>
                      </div>
                    )}
                  </article>
                )
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
