'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowRight, Layers, RotateCcw, Shuffle } from 'lucide-react'
import type { TopicData } from '@/lib/site/types'
import { BtnGhost, BtnSolid, Chip, ProgressBar, SectionHeader, gridShell, cardCell, hoverCell, eyebrowText } from './ui-bits'
import { useCards, useSettings } from '@/lib/site/stores'

/* ================= DECK GRID ================= */

export function Flashcards({
  topics, go, hydrated,
}: {
  topics: TopicData[]; go: (to: string) => void; hydrated: boolean
}) {
  const stats = useCards((s) => s.stats)
  const mode = useSettings((s) => s.uiMode)

  const deckInfo = (t: TopicData) => {
    const known = hydrated ? t.cards.filter((c) => stats[c.id]?.last === 'known').length : 0
    return { known, pct: t.cards.length ? (known / t.cards.length) * 100 : 0 }
  }

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-12">
      <p className="eyebrow">{eyebrowText(mode, 'Active recall')}</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
        {topics.filter((t) => t.cards.length > 0).length}{' '}
        <span className="serif-accent text-acc">decks</span>, one per topic.
      </h1>
      <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
        Precise, exam-grade flashcards — definitions, equations and traps. Grade yourself
        honestly: the site keeps the score so you know what to revisit.
      </p>

      <div className={gridShell(mode, 'mt-10 sm:grid-cols-2 lg:grid-cols-3')}>
        {topics.filter((t) => t.cards.length > 0).map((t) => {
          const info = deckInfo(t)
          return (
            <button
              key={t.slug}
              onClick={() => go(`/deck/${t.slug}`)}
              className={`group flex min-h-[150px] flex-col items-start p-5 text-left t-fast focus-visible:outline-acc ${cardCell(mode)} ${hoverCell(mode)}`}
            >
              <div className="flex w-full items-center justify-between">
                <span className="mono text-[12px] text-faint">{String(t.number).padStart(2, '0')}</span>
                <Chip>U{t.unit}</Chip>
              </div>
              <h3 className="mt-3 text-[15px] font-medium leading-snug text-fg t-fast group-hover:text-acc">
                {t.title}
              </h3>
              <div className="mt-auto w-full pt-4">
                <div className="mb-2 flex items-center gap-2">
                  <ProgressBar value={info.pct} className="flex-1" />
                  <span className="mono text-[10px] text-faint">
                    {info.known}/{t.cards.length} known
                  </span>
                </div>
                <span className="mono text-[10px] uppercase tracking-[0.16em] text-muted">
                  {t.cards.length} cards →
                </span>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

/* ================= DECK PLAYER ================= */

export function Deck({
  topic, topics, go,
}: {
  topic: TopicData; topics: TopicData[]; go: (to: string) => void
}) {
  const grade = useCards((s) => s.grade)
  const mode = useSettings((s) => s.uiMode)
  const [order, setOrder] = useState<number[]>(() => topic.cards.map((_, i) => i))
  const [pos, setPos] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [sessionKnown, setSessionKnown] = useState(0)
  const [sessionAgain, setSessionAgain] = useState(0)
  const [done, setDone] = useState(false)

  const card = topic.cards[order[pos]]

  const reshuffle = () => {
    setOrder((prev) => {
      const arr = [...prev]
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[arr[i], arr[j]] = [arr[j], arr[i]]
      }
      return arr
    })
    setPos(0)
    setFlipped(false)
    setDone(false)
    setSessionKnown(0)
    setSessionAgain(0)
  }

  const advance = (v: 'known' | 'again') => {
    if (!card) return
    grade(card.id, v)
    if (v === 'known') setSessionKnown((n) => n + 1)
    else setSessionAgain((n) => n + 1)
    if (pos + 1 >= order.length) setDone(true)
    else {
      setPos((p) => p + 1)
      setFlipped(false)
    }
  }

  // keyboard
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === ' ' || e.key === 'Enter') {
        if (document.activeElement?.tagName === 'BUTTON') return
        e.preventDefault()
        if (flipped) advance('known')
        else setFlipped(true)
      } else if (e.key === '1') {
        if (flipped) advance('again')
      } else if (e.key === '2') {
        if (flipped) advance('known')
      } else if (e.key === 'ArrowRight') {
        if (pos + 1 < order.length) { setPos((p) => p + 1); setFlipped(false) }
      } else if (e.key === 'ArrowLeft') {
        if (pos > 0) { setPos((p) => p - 1); setFlipped(false) }
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [flipped, pos, order.length, card])

  if (!card && !done) {
    return (
      <div className="mx-auto max-w-[1200px] px-6 py-20 text-center">
        <p className="mono text-[13px] text-muted">This deck is empty.</p>
      </div>
    )
  }

  const tagLabel = card?.tag ?? 'CORE'

  return (
    <div className="mx-auto max-w-[1200px] px-6 pb-20 pt-10">
      <nav aria-label="Breadcrumb" className="mono mb-8 flex items-center gap-2 text-[11px] uppercase tracking-[0.14em] text-faint">
        <button onClick={() => go('/')} className="t-fast hover:text-fg">~</button>
        <span>/</span>
        <button onClick={() => go('/flashcards')} className="t-fast hover:text-fg">flashcards</button>
        <span>/</span>
        <span className="text-acc">{String(topic.number).padStart(2, '0')}</span>
      </nav>

      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow mb-3">{eyebrowText(mode, `Deck ${String(topic.number).padStart(2, '0')} — unit ${topic.unit}`)}</p>
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{topic.title}</h1>
        </div>
        <div className="flex items-center gap-2">
          <BtnGhost onClick={reshuffle}>
            <Shuffle size={13} /> Shuffle
          </BtnGhost>
          <BtnGhost onClick={() => go('/flashcards')}>
            <ArrowLeft size={13} /> Decks
          </BtnGhost>
        </div>
      </div>

      <div className="mt-6 flex items-center gap-3">
        <ProgressBar value={(done ? 100 : (pos / order.length) * 100)} className="flex-1" />
        <span className="mono text-[11px] text-muted">{done ? order.length : pos + 1}/{order.length}</span>
      </div>

      {done ? (
        <div className="mx-auto mt-14 max-w-xl rounded-xl border border-line bg-surface p-10 text-center dotgrid">
          {mode === 'terminal' && <p className="mono text-[12px] text-faint">$ session --complete</p>}
          <p className="mt-4 text-3xl font-semibold tracking-tight">
            Deck <span className="serif-accent text-acc">cleared</span>.
          </p>
          <p className="mono mt-4 text-[13px] text-muted">
            got it <span className="text-acc">{sessionKnown}</span> · again <span className="text-muted">{sessionAgain}</span>
          </p>
          <p className="mt-2 text-[13px] leading-relaxed text-muted">
            Cards graded “again” will find you — rerun the deck tomorrow and watch the ratio flip.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <BtnSolid onClick={reshuffle}>
              <RotateCcw size={13} /> Run it again
            </BtnSolid>
            <BtnGhost onClick={() => go('/progress')}>See progress</BtnGhost>
            {(() => {
              const decks = topics.filter((t) => t.cards.length > 0)
              const di = decks.findIndex((t) => t.slug === topic.slug)
              return di >= 0 && di < decks.length - 1 ? (
                <BtnGhost onClick={() => go(`/deck/${decks[di + 1].slug}`)}>
                  Next deck <ArrowRight size={13} />
                </BtnGhost>
              ) : null
            })()}
          </div>
        </div>
      ) : (
        <div className="mx-auto mt-10 max-w-2xl">
          <div
            className={`flip-scene ${flipped ? 'is-flipped' : ''}`}
            onClick={() => setFlipped((f) => !f)}
            role="button"
            tabIndex={0}
            aria-label={flipped ? 'Show question' : 'Reveal answer'}
            onKeyDown={(e) => {
              if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault()
                setFlipped((f) => !f)
              }
            }}
          >
            <div className="flip-inner relative min-h-[300px] sm:min-h-[340px]">
              {/* front */}
              <div className="flip-face absolute inset-0 flex cursor-pointer flex-col rounded-xl border border-line bg-surface p-7 sm:p-9">
                <div className="flex items-center justify-between">
                  <span className="mono text-[10px] uppercase tracking-[0.18em] text-faint">
                    card {String(pos + 1).padStart(2, '0')} / {String(order.length).padStart(2, '0')}
                  </span>
                  <Chip accent={tagLabel === 'EXAM'}>{tagLabel}</Chip>
                </div>
                <div className="flex flex-1 items-center justify-center py-6">
                  <p className="text-center text-[19px] font-medium leading-relaxed text-fg sm:text-[21px]">
                    {card.front}
                  </p>
                </div>
                <p className="mono text-center text-[10px] uppercase tracking-[0.16em] text-faint">
                  click or <kbd className="kbd">space</kbd> to reveal
                </p>
              </div>
              {/* back */}
              <div className="flip-face back absolute inset-0 flex cursor-pointer flex-col rounded-xl border border-acc/40 bg-elev p-7 sm:p-9">
                <div className="flex items-center justify-between">
                  <span className="mono text-[10px] uppercase tracking-[0.18em] text-acc">answer</span>
                  <Chip accent={tagLabel === 'EXAM'}>{tagLabel}</Chip>
                </div>
                <div className="flex flex-1 items-center justify-center overflow-y-auto py-6">
                  <p className="max-h-56 overflow-y-auto text-center text-[15px] leading-relaxed text-fg sm:text-base">
                    {card.back}
                  </p>
                </div>
                <p className="mono text-center text-[10px] uppercase tracking-[0.16em] text-faint">
                  be honest — grade yourself below
                </p>
              </div>
            </div>
          </div>

          <div className="mt-5 flex items-center justify-between gap-3">
            <BtnGhost
              onClick={() => { if (pos > 0) { setPos((p) => p - 1); setFlipped(false) } }}
              className={pos === 0 ? 'pointer-events-none opacity-40' : ''}
            >
              <ArrowLeft size={13} /> Prev
            </BtnGhost>

            {flipped ? (
              <div className="flex gap-2">
                <BtnGhost onClick={() => advance('again')} className="border-acc/40 text-acc hover:border-acc hover:bg-acc/10">
                  1 · Again
                </BtnGhost>
                <BtnSolid onClick={() => advance('known')}>
                  2 · Got it
                </BtnSolid>
              </div>
            ) : (
              <BtnSolid onClick={() => setFlipped(true)}>
                <Layers size={13} /> Reveal
              </BtnSolid>
            )}

            <BtnGhost
              onClick={() => { if (pos + 1 < order.length) { setPos((p) => p + 1); setFlipped(false) } }}
              className={pos + 1 >= order.length ? 'pointer-events-none opacity-40' : ''}
            >
              Next <ArrowRight size={13} />
            </BtnGhost>
          </div>

          <p className="mono mt-4 text-center text-[10px] uppercase tracking-[0.14em] text-faint">
            session: {sessionKnown} got it · {sessionAgain} again
          </p>
        </div>
      )}
    </div>
  )
}
