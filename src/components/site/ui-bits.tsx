'use client'

import React, { useState } from 'react'
import { Check, Copy } from 'lucide-react'
import type { UiMode } from '@/lib/site/stores'

/* ---------- mode-aware layout helpers ----------
   terminal keeps the joined hairline grid (gap-px on bg-line);
   lab + hybrid get separated glass cells (studio aesthetics). */

export function gridShell(mode: UiMode, extra = ''): string {
  if (mode === 'terminal') return `grid grid-cols-1 gap-px overflow-hidden rounded-xl border border-line bg-line ${extra}`
  return `grid grid-cols-1 gap-4 ${extra}`
}

export function cardCell(mode: UiMode): string {
  if (mode === 'terminal') return 'bg-bg'
  return 'cell-glass'
}

export function hoverCell(mode: UiMode): string {
  if (mode === 'terminal') return 'hover:bg-elev focus-visible:bg-elev'
  return 'focus-visible:outline-acc'
}

/* eyebrow voice: terminal prefixes "///", studio + hybrid stay plain */
export function eyebrowText(mode: UiMode, text: string): string {
  return mode === 'terminal' ? `/// ${text}` : text
}

/* ---------- buttons (mono, 8px radius, one accent) ---------- */

export function BtnSolid({
  children, onClick, className = '', type = 'button', ariaLabel,
}: {
  children: React.ReactNode; onClick?: () => void; className?: string
  type?: 'button' | 'submit'; ariaLabel?: string
}) {
  return (
    <button
      type={type}
      aria-label={ariaLabel}
      onClick={onClick}
      className={`btn-solid mono inline-flex items-center gap-2 rounded-lg bg-acc px-4 py-2.5 text-xs font-medium uppercase tracking-[0.12em] text-on-acc t-fast hover:opacity-85 focus-visible:outline-acc active:translate-y-px ${className}`}
    >
      {children}
    </button>
  )
}

export function BtnGhost({
  children, onClick, className = '', ariaLabel, as = 'button', href,
}: {
  children: React.ReactNode; onClick?: () => void; className?: string; ariaLabel?: string
  as?: 'button' | 'a'; href?: string
}) {
  const cls = `btn-ghost mono inline-flex items-center gap-2 rounded-lg border border-line bg-transparent px-4 py-2.5 text-xs font-medium uppercase tracking-[0.12em] text-fg t-fast hover:border-line-strong hover:bg-elev focus-visible:outline-acc active:translate-y-px ${className}`
  if (as === 'a') {
    return (
      <a href={href} aria-label={ariaLabel} className={cls} onClick={(e) => { e.preventDefault(); onClick?.() }}>
        {children}
      </a>
    )
  }
  return (
    <button type="button" aria-label={ariaLabel} onClick={onClick} className={cls}>
      {children}
    </button>
  )
}

export function BtnSubtle({
  children, onClick, className = '', ariaLabel, title,
}: {
  children: React.ReactNode; onClick?: () => void; className?: string; ariaLabel?: string; title?: string
}) {
  return (
    <button
      type="button" aria-label={ariaLabel} title={title} onClick={onClick}
      className={`btn-subtle mono inline-flex items-center gap-1.5 rounded-md border border-transparent px-2 py-1 text-[11px] uppercase tracking-[0.1em] text-muted t-fast hover:border-line hover:bg-elev hover:text-fg focus-visible:outline-acc ${className}`}
    >
      {children}
    </button>
  )
}

/* ---------- chips / badges ---------- */

export function Chip({ children, accent = false, className = '' }: { children: React.ReactNode; accent?: boolean; className?: string }) {
  return (
    <span
      className={`chip mono inline-flex items-center rounded-md border px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.14em] ${
        accent ? 'border-acc/40 text-acc' : 'border-line text-muted'
      } ${className}`}
    >
      {children}
    </span>
  )
}

/* ---------- section header pattern: eyebrow over heading ---------- */

export function SectionHeader({
  eyebrow, title, sub, action,
}: {
  eyebrow: string; title: React.ReactNode; sub?: string; action?: React.ReactNode
}) {
  return (
    <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <p className="eyebrow mb-3">{eyebrow}</p>
        <h2 className="text-[clamp(22px,2.4vw,28px)] font-semibold leading-[1.2] tracking-tight">{title}</h2>
        {sub && <p className="mt-2 max-w-xl text-sm text-muted">{sub}</p>}
      </div>
      {action}
    </div>
  )
}

/* ---------- copy affordance ---------- */

export function CopyBtn({ text, label = 'Copy', className = '' }: { text: string; label?: string; className?: string }) {
  const [done, setDone] = useState(false)
  return (
    <button
      type="button"
      aria-label={done ? 'Copied' : `Copy ${label}`}
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text)
        } catch {
          // clipboard may be unavailable; still show feedback
        }
        setDone(true)
        setTimeout(() => setDone(false), 1400)
      }}
      className={`mono inline-flex items-center gap-1 rounded-md border border-line px-1.5 py-1 text-[10px] uppercase tracking-[0.1em] text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc ${className}`}
    >
      {done ? <Check size={11} className="text-acc" /> : <Copy size={11} />}
      {done ? 'Copied' : label}
    </button>
  )
}

/* ---------- progress ---------- */

export function ProgressBar({ value, className = '' }: { value: number; className?: string }) {
  const pct = Math.max(0, Math.min(100, value))
  return (
    <div
      role="progressbar"
      aria-valuenow={Math.round(pct)}
      aria-valuemin={0}
      aria-valuemax={100}
      className={`h-1 w-full overflow-hidden rounded-full bg-code ${className}`}
    >
      <div
        className="h-full rounded-full bg-acc t-med"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

export function ProgressRing({
  value, size = 120, stroke = 5, children,
}: {
  value: number; size?: number; stroke?: number; children?: React.ReactNode
}) {
  const pct = Math.max(0, Math.min(100, value))
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--line)" strokeWidth={stroke} />
        <circle
          cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke="var(--acc)" strokeWidth={stroke} strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c - (pct / 100) * c}
          className="t-med"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">{children}</div>
    </div>
  )
}

/* ---------- mono read toggle [ ] / [x] ---------- */

export function ReadToggle({
  read, onToggle, label,
}: {
  read: boolean; onToggle: () => void; label: string
}) {
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={read}
      aria-label={label}
      onClick={onToggle}
      title={read ? 'Mark as not read' : 'Mark as read'}
      className={`mono inline-flex h-7 items-center gap-2 rounded-md border px-2 text-[11px] uppercase tracking-[0.12em] t-fast focus-visible:outline-acc ${
        read
          ? 'border-acc/40 bg-acc/10 text-acc'
          : 'border-line text-muted hover:border-line-strong hover:text-fg'
      }`}
    >
      <span className="text-[12px] leading-none">{read ? '[x]' : '[ ]'}</span>
      {read ? 'read' : 'mark read'}
    </button>
  )
}

/* ---------- (ornaments live in view files) ---------- */
