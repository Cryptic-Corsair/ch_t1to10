'use client'

import React, { useState } from 'react'
import {
  BookMarked,
  Check,
  CheckCircle2,
  Copy,
  Eye,
  EyeOff,
  Image as ImageIcon,
  KeyRound,
  Lightbulb,
  PencilRuler,
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

/* ---------- worked example — the method sheet ----------
   Problem → numbered method → answer, with the maths set apart.
   Each line of a step is classified: prose, calculation chips
   ("Q = mcΔT = …"), or a lead-in label above its calculation
   ("Molar masses: …"). A cover toggle hides the working so the
   problem can be attempted on paper first. Text is never altered —
   every classification only restyles what is already there. */

const WX_ARROW = /→|⇌|⇒/

/** does this line read as a calculation / equation rather than prose? */
function wxIsEq(l: string): boolean {
  if (WX_ARROW.test(l)) return true
  if (!l.includes('=')) return false
  if (l.length <= 78 && !/[.!?]['")\]]?$/.test(l)) return true
  // longer sentences that are still mostly maths:
  // "Q = mcΔT = 50 × 4.18 × 6.7 = 1400.3 J = 1.4003 kJ."
  if (/[÷×√]/.test(l)) return true
  if (/\d\s*[+−]\s*[(\d−]/.test(l)) return true
  const s = l.replace(/\s/g, '')
  const mathy = (s.match(/[\d+=÷×−√().,°]/g) ?? []).length
  return s.length > 0 && mathy / s.length >= 0.45
}

/** "Molar masses: M(CuCO₃) = …" → the label + the calculation.
    Ratio colons like "Cu : H₂O" (space on both sides) never split. */
function wxSplitLead(line: string): { lead: string; rest: string } | null {
  for (let i = 0; i < line.length; i++) {
    if (line[i] !== ':') continue
    if (line[i + 1] !== ' ') return null
    if (i > 0 && line[i - 1] === ' ') continue
    const lead = line.slice(0, i + 1)
    if (lead.length < 3 || lead.length > 47) return null
    return { lead, rest: line.slice(i + 1).trim() }
  }
  return null
}

/** "p = 120 × 10³ = … Pa; V = …; T = …" → one chip per calculation.
    Only when every segment is a short calculation, so nothing is
    lost — the ';' stays with its segment. */
function wxSplitMulti(line: string): string[] | null {
  if (!line.includes(';')) return null
  const parts = line.split(';').map((p) => p.trim()).filter(Boolean)
  if (parts.length < 2 || parts.length > 3) return null
  if (parts.some((p) => !p.includes('=') || p.length > 64)) return null
  return parts.map((p, i) => (i < parts.length - 1 ? p + ';' : p))
}

type WxSeg =
  | { kind: 'lead'; lead: string; chips: string[] }
  | { kind: 'eq'; chips: string[] }
  | { kind: 'li'; text: string }
  | { kind: 'p'; text: string }

function wxSegs(step: string): WxSeg[] {
  const out: WxSeg[] = []
  const lines = step.split('\n').map((l) => l.trim()).filter(Boolean)
  for (const line of lines) {
    if (/^[-•*]\s+/.test(line)) {
      out.push({ kind: 'li', text: line.replace(/^[-•*]\s+/, '') })
      continue
    }
    const lead = wxSplitLead(line)
    if (lead && wxIsEq(lead.rest)) {
      out.push({ kind: 'lead', lead: lead.lead, chips: wxSplitMulti(lead.rest) ?? [lead.rest] })
      continue
    }
    if (wxIsEq(line)) {
      out.push({ kind: 'eq', chips: wxSplitMulti(line) ?? [line] })
      continue
    }
    out.push({ kind: 'p', text: line })
  }
  return out
}

function WxChips({ chips }: { chips: string[] }) {
  return (
    <div className="space-y-2">
      {chips.map((chip, j) => (
        <p key={j} className="wx-eq">
          <Inline text={chip} />
        </p>
      ))}
    </div>
  )
}

function WxLines({ text }: { text: string }) {
  return (
    <div className="space-y-2">
      {wxSegs(text).map((seg, i) => {
        if (seg.kind === 'lead') {
          return (
            <div key={i} className="space-y-2">
              <p className="text-[13px] font-medium leading-snug text-fg/75">
                <Inline text={seg.lead} />
              </p>
              <WxChips chips={seg.chips} />
            </div>
          )
        }
        if (seg.kind === 'eq') return <WxChips key={i} chips={seg.chips} />
        if (seg.kind === 'li') {
          return (
            <p key={i} className="wx-li">
              <span aria-hidden>–</span>
              <span className="min-w-0"><Inline text={seg.text} /></span>
            </p>
          )
        }
        return (
          <p key={i} className="leading-relaxed">
            <Inline text={seg.text} />
          </p>
        )
      })}
    </div>
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

/* ---------- worked example card ----------
   The method sheet: header → problem → numbered method → answer.
   "Cover" hides the working and the answer so the problem can be
   attempted first — active recall, one tap away. */

function WorkedCard({ block }: { block: Extract<Block, { type: 'worked' }> }) {
  const [covered, setCovered] = useState(false)
  const nSteps = block.steps.length
  return (
    <div className="blk blk-worked focus-block overflow-hidden rounded-xl border border-line bg-surface">
      {/* header — skill title up front, cover control on the right */}
      <div className="flex items-start justify-between gap-4 px-5 py-4">
        <div className="min-w-0">
          <p className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
            <span className="flex items-center gap-1.5">
              <PencilRuler size={12} strokeWidth={1.75} className="shrink-0 text-acc" aria-hidden />
              <span className="mono text-[9.5px] font-semibold uppercase tracking-[0.2em] text-acc">
                Worked example
              </span>
            </span>
            <span className="mono text-[9.5px] uppercase tracking-[0.14em] text-faint">
              · {nSteps} {nSteps === 1 ? 'step' : 'steps'}
            </span>
          </p>
          <p className="mt-1 text-[15.5px] font-semibold leading-snug text-fg">{block.title}</p>
        </div>
        {!covered && (
          <button
            type="button"
            onClick={() => setCovered(true)}
            aria-label="Cover the working and answer to try the problem yourself first"
            title="Cover — try it yourself first"
            className="mono flex shrink-0 items-center gap-1.5 rounded-full border border-line px-3 py-1.5 text-[9.5px] font-medium uppercase tracking-[0.14em] text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc"
          >
            <EyeOff size={11} strokeWidth={1.75} aria-hidden />
            Cover
          </button>
        )}
      </div>

      {/* the problem — stays visible even when the method is covered */}
      <div className="px-5 pb-5">
        <div className="rounded-xl border border-line/70 border-l-2 border-l-acc/60 bg-elev/40 px-4 py-3.5">
          <p className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-faint">Problem</p>
          <p className="mt-1.5 text-[15px] leading-relaxed text-fg/90">
            <Inline text={block.problem} />
          </p>
        </div>
      </div>

      {covered ? (
        /* covered — attempt it on paper, then reveal */
        <div className="px-5 pb-5">
          <div className="rounded-xl border border-dashed border-line-strong bg-elev/30 px-4 py-6 text-center">
            <EyeOff size={16} strokeWidth={1.75} className="mx-auto text-faint" aria-hidden />
            <p className="mt-2.5 text-[14px] font-medium text-fg">Working and answer covered</p>
            <p className="mx-auto mt-1 max-w-[38ch] text-[13px] leading-relaxed text-muted">
              Try the problem on paper first, then check the method.
            </p>
            <button
              type="button"
              onClick={() => setCovered(false)}
              className="mt-4 inline-flex items-center gap-2 rounded-full bg-acc px-4 py-2 text-[12.5px] font-semibold text-on-acc t-fast hover:opacity-90 focus-visible:outline-acc"
            >
              <Eye size={13} strokeWidth={2} aria-hidden />
              Reveal the method
            </button>
          </div>
        </div>
      ) : (
        <>
          {/* the method — numbered timeline, the maths set apart */}
          <div className="px-5 pb-5">
            <ol className="steps space-y-4">
              {block.steps.map((s, i) => (
                <li key={i} className="flex items-start gap-3.5">
                  <span className="step-dot" aria-hidden>{i + 1}</span>
                  <div className="min-w-0 flex-1 pt-0.5 text-[14px] leading-relaxed text-muted">
                    <WxLines text={s} />
                  </div>
                </li>
              ))}
            </ol>
          </div>

          {/* the answer — full-bleed result band, one tap to copy */}
          <div className="flex items-start gap-3.5 border-t border-line bg-[color-mix(in_srgb,var(--acc)_10%,transparent)] px-5 py-4">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-acc text-on-acc shadow-md">
              <CheckCircle2 size={15} strokeWidth={2.25} aria-hidden />
            </span>
            <div className="min-w-0 flex-1">
              <p className="mono text-[10px] font-medium uppercase tracking-[0.18em] text-acc">Answer</p>
              <p className="mt-1 text-[15px] font-semibold leading-relaxed text-fg [font-variant-numeric:tabular-nums]">
                <Inline text={block.answer} />
              </p>
            </div>
            <EqCopy text={block.answer} />
          </div>
        </>
      )}
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
        <h3 className="mt-10! flex items-center gap-3 text-[17px] font-semibold tracking-tight text-fg">
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
      return <WorkedCard block={block} />

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
