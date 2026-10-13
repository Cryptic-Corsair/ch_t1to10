'use client'

import React, { useState } from 'react'
import {
  BookMarked,
  Check,
  CheckCircle2,
  Copy,
  Image as ImageIcon,
  KeyRound,
  Lightbulb,
  PenLine,
  Sigma,
  Target,
  TriangleAlert,
} from 'lucide-react'
import type { Block } from '@/lib/site/types'

/* ---------- tiny inline markdown: **bold**, *italic*, `code` ---------- */

export function Inline({ text }: { text: string }) {
  const nodes: React.ReactNode[] = []
  const re = /(\*\*[^*]+\*\*|\*[^*\n]+\*|`[^`]+`)/g
  let last = 0
  let m: RegExpExecArray | null
  let k = 0
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) nodes.push(text.slice(last, m.index))
    const tok = m[0]
    if (tok.startsWith('**')) nodes.push(<strong key={k++} className="font-semibold text-fg">{tok.slice(2, -2)}</strong>)
    else if (tok.startsWith('`')) nodes.push(<code key={k++} className="mono rounded bg-code px-1.5 py-0.5 text-[0.85em] text-fg">{tok.slice(1, -1)}</code>)
    else nodes.push(<em key={k++}>{tok.slice(1, -1)}</em>)
    last = m.index + tok.length
  }
  if (last < text.length) nodes.push(text.slice(last))
  return <>{nodes}</>
}

/* ---------- icon-only copy affordance ---------- */

function EqCopy({ text }: { text: string }) {
  const [done, setDone] = useState(false)
  return (
    <button
      type="button"
      aria-label={done ? 'Copied to clipboard' : 'Copy equation'}
      title={done ? 'Copied' : 'Copy'}
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text)
        } catch {
          // clipboard may be unavailable; still show feedback
        }
        setDone(true)
        setTimeout(() => setDone(false), 1400)
      }}
      className={`inline-flex h-7 w-7 items-center justify-center rounded-md border t-fast focus-visible:outline-acc ${
        done
          ? 'border-acc/40 text-acc'
          : 'border-line text-faint hover:border-line-strong hover:text-fg'
      }`}
    >
      {done ? <Check size={12} /> : <Copy size={12} />}
    </button>
  )
}

/* ---------- callout vocabulary ---------- */

const CALLOUT_META: Record<string, { label: string; Icon: React.ComponentType<{ size?: number; strokeWidth?: number; className?: string }> }> = {
  tip: { label: 'Tip', Icon: Lightbulb },
  warning: { label: 'Watch out', Icon: TriangleAlert },
  exam: { label: 'Exam alert', Icon: Target },
  key: { label: 'Key point', Icon: KeyRound },
}

/* ---------- background bullet cards (terminal reading room) ----------
   Consecutive def / list blocks merge into ONE card that floats on the
   canvas: each row = accent dot + (optional bold lead term) + a thin rail
   holding the explanation, rows separated by hairlines. */

export type BlockSegment =
  | { kind: 'single'; block: Block }
  | { kind: 'group'; blocks: Block[] }

export function groupBlocks(blocks: Block[]): BlockSegment[] {
  const out: BlockSegment[] = []
  for (const b of blocks) {
    if (b.type === 'def' || b.type === 'list') {
      const last = out[out.length - 1]
      if (last && last.kind === 'group') last.blocks.push(b)
      else out.push({ kind: 'group', blocks: [b] })
    } else {
      out.push({ kind: 'single', block: b })
    }
  }
  return out
}

/* "**Negative ion** has more electrons…" → term "Negative ion", rest the rail text */
function splitLead(text: string): { term?: string; rest: string } {
  const m = /^\*\*([^*]+?)\*\*\s*[,;:]?\s+([^\s].*)$/s.exec(text.trim())
  if (m) return { term: m[1], rest: m[2] }
  return { rest: text }
}

type BulletRowData = { num?: number; term?: string; text?: string }

function rowsFromGroup(blocks: Block[]): BulletRowData[] {
  const rows: BulletRowData[] = []
  for (const b of blocks) {
    if (b.type === 'def') {
      rows.push({ term: b.term, text: b.text })
    } else if (b.type === 'list') {
      b.items.forEach((it, i) => {
        if (b.ordered) {
          rows.push({ num: i + 1, text: it })
        } else {
          const { term, rest } = splitLead(it)
          rows.push({ term, text: rest })
        }
      })
    }
  }
  return rows
}

export function BulletCard({ blocks }: { blocks: Block[] }) {
  const rows = rowsFromGroup(blocks)
  return (
    <div className="bullet-card focus-block">
      {rows.map((r, i) => (
        <div className="bullet-row" key={i}>
          {r.num !== undefined ? (
            <span className="bullet-num mono" aria-hidden>{r.num}.</span>
          ) : (
            <span className="bullet-dot" aria-hidden />
          )}
          <div className="min-w-0 flex-1">
            {r.term && <p className="bullet-term">{r.term}</p>}
            {r.text && (
              <div className={r.term ? 'rail' : 'bullet-text'}>
                <Inline text={r.text} />
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

/* ---------- note-style callout (quick-revision edition) ----------
   Quieter and more human than the default card. Four distinct,
   natural treatments instead of four identical boxes:
   · key     — highlighter swipe, "The key point", statement up front
   · exam    — marked note, "In the exam", the wording front and centre
   · warning — amber margin scribble, icon + lead, no label
   · tip     — dashed aside, icon + lead, no label, lightest of all   */

const NOTE_META: Record<string, { label?: string; Icon: React.ComponentType<{ size?: number; strokeWidth?: number; className?: string }>; iconClass: string }> = {
  key: { label: 'The key point', Icon: KeyRound, iconClass: 'text-acc' },
  exam: { label: 'In the exam', Icon: Target, iconClass: 'text-acc' },
  warning: { Icon: TriangleAlert, iconClass: 'text-amber-500' },
  tip: { Icon: Lightbulb, iconClass: 'text-acc' },
}

function NoteCallout({ block }: { block: Extract<Block, { type: 'callout' }> }) {
  const meta = NOTE_META[block.variant] ?? NOTE_META.tip
  const { label, Icon, iconClass } = meta
  const inline = block.variant === 'tip' || block.variant === 'warning'
  return (
    <div className={`blk blk-callout callout-note callout-note-${block.variant} focus-block rounded-xl px-5 py-4`}>
      {inline ? (
        <p className="flex items-center gap-2 text-[14.5px] font-semibold leading-snug text-fg">
          <Icon size={14} strokeWidth={1.75} className={`shrink-0 ${iconClass}`} />
          {block.title}
        </p>
      ) : (
        <>
          <p className={`flex items-center gap-1.5 text-[11.5px] font-medium ${block.variant === 'exam' ? 'text-acc' : 'text-faint'}`}>
            <Icon size={12} strokeWidth={1.75} className={`shrink-0 ${iconClass}`} />
            {label}
          </p>
          <p className="mt-2 text-[16.5px] font-semibold leading-snug text-fg">{block.title}</p>
        </>
      )}
      <p className={`leading-relaxed text-muted ${inline ? 'mt-1.5 text-[13.5px]' : 'mt-1.5 text-[14px]'}`}>
        <Inline text={block.text} />
      </p>
    </div>
  )
}

/* ---------- check-yourself card (reveal answers from memory) ---------- */

function QaCard({ block }: { block: Extract<Block, { type: 'qa' }> }) {
  const [open, setOpen] = useState<boolean[]>(() => block.items.map(() => false))
  const shown = open.filter(Boolean).length
  return (
    <div className="blk blk-qa focus-block overflow-hidden rounded-xl border border-line bg-surface">
      <div className="flex items-center justify-between gap-3 border-b border-line bg-elev/50 px-5 py-3">
        <p className="flex items-center gap-2.5 text-[13px] font-semibold text-fg">
          <Target size={14} className="shrink-0 text-acc" strokeWidth={1.75} />
          {block.title ?? 'Quick check'}
          <span className="font-normal text-muted">— answer from memory first</span>
        </p>
        {shown > 0 && (
          <span className="mono shrink-0 text-[10px] uppercase tracking-[0.14em] text-acc">
            {shown}/{block.items.length}
          </span>
        )}
      </div>
      <div className="divide-y divide-line/60">
        {block.items.map((it, i) => (
          <button
            key={i}
            type="button"
            aria-expanded={open[i]}
            onClick={() => setOpen((o) => o.map((v, j) => (j === i ? !v : v)))}
            className="block w-full px-5 py-3.5 text-left t-fast hover:bg-elev/40 focus-visible:outline-acc"
          >
            <span className="flex items-start gap-3">
              <span className={`mono mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[10px] t-fast ${
                open[i] ? 'border-acc/50 bg-acc/10 text-acc' : 'border-line text-faint'
              }`}>
                {open[i] ? <Check size={11} strokeWidth={2} /> : i + 1}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block text-[14px] font-medium leading-snug text-fg">
                  <Inline text={it.q} />
                </span>
                {open[i] && (
                  <span className="mt-1.5 block border-l-2 border-acc/40 pl-3 text-[13.5px] leading-relaxed text-muted">
                    <Inline text={it.a} />
                  </span>
                )}
              </span>
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}

/* ---------- the renderer ---------- */

export function BlockRenderer({ block, lead = false }: { block: Block; lead?: boolean }) {
  switch (block.type) {
    case 'p':
      return (
        <p className={`text-fg/90 ${lead ? 'reading-lead' : ''}`}>
          <Inline text={block.text} />
        </p>
      )

    case 'h3':
      return (
        <h3 className="!mt-10 flex items-center gap-3 text-[17px] font-semibold tracking-tight text-fg">
          <span aria-hidden className="h-4 w-1 rounded-full bg-acc/70" />
          <span className="display-serif text-[19px] font-medium [letter-spacing:0]">{block.text}</span>
        </h3>
      )

    case 'def':
      return (
        <div className="blk blk-def focus-block rounded-xl border border-line border-l-2 border-l-acc bg-surface px-5 py-4">
          <p className="mono flex items-center gap-1.5 text-[10px] font-medium uppercase tracking-[0.18em] text-faint">
            <BookMarked size={12} className="text-acc" strokeWidth={1.75} />
            Definition
          </p>
          <p className="blk-def-term mt-2 font-semibold text-fg">{block.term}</p>
          <p className="mt-1 text-[0.95em] leading-relaxed text-muted">
            <Inline text={block.text} />
          </p>
        </div>
      )

    case 'eq':
      return (
        <figure className="blk blk-eq focus-block overflow-hidden rounded-xl border border-line bg-surface">
          <div className="blk-eq-bar flex items-center justify-between border-b border-line px-4 py-2">
            <span className="mono flex items-center gap-1.5 text-[10px] font-medium uppercase tracking-[0.18em] text-faint">
              <Sigma size={12} className="text-acc" strokeWidth={1.75} />
              Equation
            </span>
            <EqCopy text={block.code} />
          </div>
          <div className="overflow-x-auto px-5 py-5">
            <p className="equation-display mx-auto w-max max-w-full whitespace-nowrap text-[17px] leading-relaxed text-fg">
              {block.code}
            </p>
            {block.caption && (
              <figcaption className="mt-3 text-center text-[12.5px] italic leading-relaxed text-muted">
                <Inline text={block.caption} />
              </figcaption>
            )}
          </div>
        </figure>
      )

    case 'list': {
      if (block.ordered) {
        return (
          <ol className="space-y-2.5">
            {block.items.map((it, i) => (
              <li key={i} className="flex gap-3 text-fg/90">
                <span className="w-6 shrink-0 select-none pt-px text-right text-[13.5px] font-semibold leading-[1.6] text-acc">
                  {i + 1}.
                </span>
                <span className="min-w-0 flex-1"><Inline text={it} /></span>
              </li>
            ))}
          </ol>
        )
      }
      return (
        <ul className="space-y-2.5">
          {block.items.map((it, i) => (
            <li key={i} className="flex gap-3 text-fg/90">
              <span aria-hidden className="mt-[0.62em] h-1.5 w-1.5 shrink-0 rotate-45 bg-acc/80" />
              <span className="min-w-0 flex-1"><Inline text={it} /></span>
            </li>
          ))}
        </ul>
      )
    }

    case 'callout': {
      if (block.style === 'note') return <NoteCallout block={block} />
      const { label, Icon } = CALLOUT_META[block.variant] ?? CALLOUT_META.tip
      return (
        <div className="blk blk-callout callout focus-block rounded-xl border border-line px-5 py-4">
          <div className="flex gap-3.5">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-acc/30 bg-acc/10 text-acc">
              <Icon size={15} strokeWidth={1.75} />
            </span>
            <div className="min-w-0 flex-1">
              <p className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-acc">{label}</p>
              <p className="mt-1.5 font-semibold leading-snug text-fg">{block.title}</p>
              <p className="mt-1 text-[0.95em] leading-relaxed text-muted">
                <Inline text={block.text} />
              </p>
            </div>
          </div>
        </div>
      )
    }

    case 'worked':
      return (
        <div className="blk blk-worked focus-block overflow-hidden rounded-xl border border-line bg-surface">
          <div className="flex items-center gap-2.5 border-b border-line bg-elev/50 px-5 py-3">
            <PenLine size={14} className="shrink-0 text-acc" strokeWidth={1.75} />
            <p className="text-[13px] font-semibold text-fg">
              Worked example
              <span className="font-normal text-muted"> — {block.title}</span>
            </p>
          </div>
          <div className="px-5 py-5">
            <div className="rounded-lg border border-line/70 bg-elev/50 px-4 py-3.5">
              <p className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-faint">Problem</p>
              <p className="mt-1.5 text-[0.95em] leading-relaxed text-fg/90">
                <Inline text={block.problem} />
              </p>
            </div>

            <ol className="steps mt-5 space-y-4">
              {block.steps.map((s, i) => (
                <li key={i} className="flex items-start gap-3.5">
                  <span className="step-dot" aria-hidden>{i + 1}</span>
                  <span className="min-w-0 flex-1 overflow-x-auto whitespace-pre-wrap pt-0.5 text-[13.5px] leading-relaxed text-muted">
                    <Inline text={s} />
                  </span>
                </li>
              ))}
            </ol>

            <div className="mt-5 flex items-start gap-3 rounded-lg border border-acc/30 bg-acc/10 px-4 py-3.5">
              <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-acc" strokeWidth={1.75} />
              <div className="min-w-0">
                <p className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-acc">Answer</p>
                <p className="mt-1 text-[14px] font-medium leading-relaxed text-fg">{block.answer}</p>
              </div>
            </div>
          </div>
        </div>
      )

    case 'qa':
      return <QaCard block={block} />

    case 'table':
      return (
        <div className="blk blk-table focus-block overflow-hidden rounded-xl border border-line">
          <div className="overflow-x-auto">
            <table className="reading-table w-full min-w-[520px] border-collapse text-left text-[13.5px]">
              <thead>
                <tr className="border-b border-line-strong bg-elev/50">
                  {block.headers.map((h, i) => (
                    <th key={i} className="px-4 py-3 text-[10.5px] uppercase tracking-[0.16em] text-muted">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {block.rows.map((row, i) => (
                  <tr key={i} className="border-b border-line/60 t-fast last:border-0 hover:bg-elev/40">
                    {row.map((cell, j) => (
                      <td key={j} className={`whitespace-pre-line px-4 py-3 align-top leading-relaxed ${j === 0 ? 'font-medium text-fg' : 'text-muted'}`}>
                        <Inline text={cell} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )

    case 'figure':
      return (
        <figure className="blk blk-fig focus-block overflow-hidden rounded-xl border border-line bg-surface">
          <div className="relative border-b border-line bg-elev/30">
            {block.srcDark ? (
              <>
                {/* eager (not lazy): lazy figures load mid-scroll and shift the
                    page, which throws off TOC jumps and the scroll-spy */}
                <img src={block.src} alt={block.alt} className="fig-light h-auto w-full" />
                <img src={block.srcDark} alt="" aria-hidden className="fig-dark h-auto w-full" />
              </>
            ) : (
              <img src={block.src} alt={block.alt} className="h-auto w-full" />
            )}
          </div>
          <figcaption className="flex items-start gap-2.5 px-5 py-3.5 text-[12.5px] leading-relaxed text-muted">
            <ImageIcon size={13} strokeWidth={1.75} className="mt-0.5 shrink-0 text-acc" />
            <span className="min-w-0"><Inline text={block.caption ?? block.alt} /></span>
          </figcaption>
        </figure>
      )

    default:
      return null
  }
}
