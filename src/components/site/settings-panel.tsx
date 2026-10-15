'use client'

import React, { useEffect } from 'react'
import { X } from 'lucide-react'
import { applySettingsToDom, useSettings, useUi, UI_MODES, MODE_PRESETS, type AccentName, type FontFamily, type ThemeName, type UiMode } from '@/lib/site/stores'
import { BtnGhost } from './ui-bits'
import { useProgress, useCards } from '@/lib/site/stores'

/* ---------- interface mode previews (fixed colours — theme-independent) ---------- */

function ModePreview({ mode }: { mode: UiMode }) {
  if (mode === 'terminal') {
    return (
      <span aria-hidden className="block h-[64px] w-full overflow-hidden rounded-md border border-[#2a2a2a] bg-[#141414] p-2.5 text-left">
        <span className="block h-[5px] w-3/5 rounded-sm bg-[#4a4a4a]" />
        <span className="mt-[6px] block h-[5px] w-4/5 rounded-sm bg-[#3a3a3a]" />
        <span className="mt-[6px] block h-[5px] w-2/5 rounded-sm bg-[#F5654A]" />
        <span className="mt-[6px] block h-[5px] w-3/5 rounded-sm bg-[#3a3a3a]" />
      </span>
    )
  }
  if (mode === 'hybrid') {
    /* studio glass + focus's bullet-card rows */
    return (
      <span aria-hidden className="block h-[64px] w-full overflow-hidden rounded-md border border-[#241c3f] bg-[#0d0b1a] p-2.5 text-left">
        <span className="block h-[6px] w-3/5 rounded-full bg-gradient-to-r from-[#a78bfa] to-[#38d5ee] opacity-90" />
        <span className="mt-[6px] block rounded-md border border-white/15 bg-white/[0.07] px-1.5 py-1">
          <span className="flex items-center gap-1">
            <span className="block h-[4px] w-[4px] rounded-full bg-[#a78bfa]" />
            <span className="block h-[4px] w-3/5 rounded-full bg-white/25" />
          </span>
          <span className="mt-[3px] ml-[8px] block h-[3px] w-2/5 rounded-full bg-white/15" />
        </span>
        <span className="mt-[5px] flex items-center gap-1">
          <span className="block h-[4px] w-[4px] rounded-full bg-[#38d5ee]" />
          <span className="block h-[4px] w-2/5 rounded-full bg-white/20" />
        </span>
      </span>
    )
  }
  return (
    <span aria-hidden className="block h-[64px] w-full overflow-hidden rounded-md border border-[#241c3f] bg-[#0d0b1a] p-2.5 text-left">
      <span className="block h-[7px] w-11/12 rounded-full bg-gradient-to-r from-[#a78bfa] to-[#38d5ee] opacity-90" />
      <span className="mt-2 flex gap-1.5">
        <span className="block h-[16px] w-1/3 rounded-full border border-white/15 bg-white/10" />
        <span className="block h-[16px] w-1/4 rounded-full border border-white/15 bg-white/10" />
      </span>
      <span className="mt-2 block h-[5px] w-3/5 rounded-full bg-white/15" />
    </span>
  )
}

/* ---------- atoms ---------- */

function Group({ label, children, hint }: { label: string; children: React.ReactNode; hint?: string }) {
  return (
    <section className="border-b border-line py-5 first:pt-0 last:border-0">
      <p className="mono mb-3.5 text-[10px] font-medium uppercase tracking-[0.2em] text-faint">{label}</p>
      {children}
      {hint && <p className="mono mt-3 text-[10px] leading-relaxed text-faint">{hint}</p>}
    </section>
  )
}

function Segmented<T extends string | number>({
  options, value, onChange, ariaLabel,
}: {
  options: { value: T; label: string }[]
  value: T
  onChange: (v: T) => void
  ariaLabel: string
}) {
  return (
    <div role="radiogroup" aria-label={ariaLabel} className="flex gap-px overflow-hidden rounded-lg border border-line bg-line">
      {options.map((o) => (
        <button
          key={String(o.value)}
          role="radio"
          aria-checked={value === o.value}
          onClick={() => onChange(o.value)}
          className={`mono flex-1 px-2 py-2 text-[10.5px] uppercase tracking-[0.12em] t-fast focus-visible:outline-acc ${
            value === o.value ? 'bg-acc text-on-acc' : 'bg-bg text-muted hover:bg-elev hover:text-fg'
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}

/* ---------- theme + accent swatches ---------- */

const THEMES: { value: ThemeName; label: string; swatch: string; fg: string }[] = [
  { value: 'midnight', label: 'Midnight', swatch: '#111111', fg: '#fafafa' },
  { value: 'carbon', label: 'Carbon', swatch: '#0b0b0c', fg: '#f4f4f5' },
  { value: 'paper', label: 'Paper', swatch: '#fafafa', fg: '#161616' },
  { value: 'sepia', label: 'Sepia', swatch: '#f4eee1', fg: '#2c261b' },
]

const ACCENTS: { value: AccentName; label: string; hex: string }[] = [
  { value: 'coral', label: 'Coral', hex: '#F5654A' },
  { value: 'amber', label: 'Amber', hex: '#e6a23c' },
  { value: 'mint', label: 'Mint', hex: '#3ecf8e' },
  { value: 'rose', label: 'Rose', hex: '#ef5d80' },
  { value: 'violet', label: 'Violet', hex: '#a78bfa' },
  { value: 'cyan', label: 'Cyan', hex: '#38d5ee' },
]

/* ---------- the content (shared by slide-over + page) ---------- */

export function SettingsContent() {
  const s = useSettings()
  const set = useSettings((st) => st.set)
  const { reset: resetProgress } = useProgress()
  const { reset: resetCards } = useCards()
  const [confirmReset, setConfirmReset] = React.useState(false)

  // live-apply on every change
  useEffect(() => {
    applySettingsToDom(s)
  }, [s])

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <Group label="Interface" hint="Each interface has its own layout and palette. Notes, progress and preferences are shared across all three.">
          <div role="radiogroup" aria-label="Interface mode" className="grid grid-cols-3 gap-2">
            {UI_MODES.map((m) => {
              const active = s.uiMode === m.value
              const preset = MODE_PRESETS[m.value]
              return (
                <button
                  key={m.value}
                  role="radio"
                  aria-checked={active}
                  onClick={() => set({ uiMode: m.value })}
                  title={m.blurb}
                  className={`rounded-lg border p-2 text-left t-fast focus-visible:outline-acc ${
                    active ? 'border-acc bg-acc/5' : 'border-line bg-bg hover:border-line-strong'
                  }`}
                >
                  <ModePreview mode={m.value} />
                  <span className={`mono mt-2 block text-[10px] uppercase tracking-[0.12em] ${active ? 'text-acc' : 'text-fg'}`}>
                    {m.label}
                  </span>
                  <span className="mono block text-[8.5px] uppercase tracking-[0.14em] text-faint">
                    default: {preset.theme} · {preset.accent}
                  </span>
                </button>
              )
            })}
          </div>
          <p className="mt-2.5 text-[11.5px] leading-relaxed text-muted">
            {UI_MODES.find((m) => m.value === s.uiMode)?.blurb}
          </p>
        </Group>

        <Group label="Theme" hint="Remembered per interface — switching interfaces restores each one's palette.">
          <div className="grid grid-cols-4 gap-px overflow-hidden rounded-lg border border-line bg-line">
            {THEMES.map((t) => (
              <button
                key={t.value}
                onClick={() => set({ theme: t.value })}
                aria-pressed={s.theme === t.value}
                className="flex flex-col items-center gap-2 bg-bg px-1 py-3 t-fast hover:bg-elev focus-visible:outline-acc"
              >
                <span
                  className={`flex h-8 w-8 items-center justify-center rounded-md border ${
                    s.theme === t.value ? 'border-acc' : 'border-line'
                  }`}
                  style={{ backgroundColor: t.swatch }}
                >
                  <span className="mono text-[11px]" style={{ color: t.fg }}>Aa</span>
                </span>
                <span className={`mono text-[9.5px] uppercase tracking-[0.1em] ${s.theme === t.value ? 'text-acc' : 'text-muted'}`}>
                  {t.label}
                </span>
              </button>
            ))}
          </div>
        </Group>

        <Group label="Accent" hint="One hue, everywhere — also remembered per interface.">
          <div className="flex gap-2.5">
            {ACCENTS.map((a) => (
              <button
                key={a.value}
                onClick={() => set({ accent: a.value })}
                aria-pressed={s.accent === a.value}
                aria-label={`Accent ${a.label}`}
                title={a.label}
                className={`h-9 w-9 rounded-full border-2 t-fast focus-visible:outline-acc ${
                  s.accent === a.value ? 'border-fg scale-105' : 'border-transparent hover:scale-105'
                }`}
                style={{ backgroundColor: a.hex }}
              />
            ))}
          </div>
        </Group>

        <Group label="Typeface">
          <Segmented<FontFamily>
            ariaLabel="Typeface"
            value={s.fontFamily}
            onChange={(v) => set({ fontFamily: v })}
            options={[
              { value: 'sans', label: 'Sans' },
              { value: 'serif', label: 'Serif' },
              { value: 'mono', label: 'Mono' },
            ]}
          />
        </Group>

        <Group label="Text size">
          <Segmented<number>
            ariaLabel="Text size"
            value={s.fontSize}
            onChange={(v) => set({ fontSize: v })}
            options={[
              { value: 0, label: 'S' },
              { value: 1, label: 'M' },
              { value: 2, label: 'L' },
              { value: 3, label: 'XL' },
            ]}
          />
        </Group>

        <Group label="Line height">
          <Segmented<number>
            ariaLabel="Line height"
            value={s.lineHeight}
            onChange={(v) => set({ lineHeight: v })}
            options={[
              { value: 0, label: '1.5' },
              { value: 1, label: '1.65' },
              { value: 2, label: '1.8' },
            ]}
          />
        </Group>

        <Group label="Reading width">
          <Segmented<'normal' | 'wide'>
            ariaLabel="Reading width"
            value={s.width}
            onChange={(v) => set({ width: v })}
            options={[
              { value: 'normal', label: 'Normal' },
              { value: 'wide', label: 'Wide' },
            ]}
          />
        </Group>

        <Group label="Focus mode" hint="Dims surrounding blocks while you read — hover brings them back.">
          <Segmented<'off' | 'on'>
            ariaLabel="Focus mode"
            value={s.focusMode ? 'on' : 'off'}
            onChange={(v) => set({ focusMode: v === 'on' })}
            options={[
              { value: 'off', label: 'Off' },
              { value: 'on', label: 'On' },
            ]}
          />
        </Group>

        <Group label="Motion">
          <Segmented<'normal' | 'reduced'>
            ariaLabel="Motion preference"
            value={s.motion}
            onChange={(v) => set({ motion: v })}
            options={[
              { value: 'normal', label: 'Normal' },
              { value: 'reduced', label: 'Reduced' },
            ]}
          />
        </Group>

        <Group label="Specification outlines">
          <Segmented<'show' | 'hide'>
            ariaLabel="Show specification outlines"
            value={s.showOutline ? 'show' : 'hide'}
            onChange={(v) => set({ showOutline: v === 'show' })}
            options={[
              { value: 'show', label: 'Show' },
              { value: 'hide', label: 'Hide' },
            ]}
          />
        </Group>

        <Group label="Data">
          {confirmReset ? (
            <div className="flex flex-wrap gap-2">
              <BtnGhost onClick={() => { resetProgress(); resetCards(); setConfirmReset(false) }} className="border-acc/50 text-acc">
                Confirm — wipe progress
              </BtnGhost>
              <BtnGhost onClick={() => setConfirmReset(false)}>Cancel</BtnGhost>
            </div>
          ) : (
            <BtnGhost onClick={() => setConfirmReset(true)}>Reset reading progress + cards</BtnGhost>
          )}
        </Group>
      </div>

      <div className="border-t border-line px-6 py-4">
        <p className="mono text-[10px] leading-relaxed text-faint">
          {s.uiMode === 'terminal'
            ? '// preferences persist locally in this browser · nothing is uploaded'
            : 'Preferences persist locally in this browser · nothing is uploaded.'}
        </p>
      </div>
    </div>
  )
}

/* ---------- slide-over shell ---------- */

export function SettingsPanel() {
  const open = useUi((s) => s.settingsOpen)
  const close = useUi((s) => s.closeSettings)
  const mode = useSettings((s) => s.uiMode)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, close])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-[70] print:hidden" role="dialog" aria-modal="true" aria-label="Control room settings">
      <div
        className="absolute inset-0 bg-black/55 t-fast"
        onClick={close}
        aria-hidden
      />
      <div className="absolute right-0 top-0 flex h-full w-full max-w-[400px] flex-col border-l border-line bg-surface shadow-2xl t-med" style={{ animation: 'slide-in 220ms cubic-bezier(0.4,0,0.2,1)' }}>
        <style>{`@keyframes slide-in { from { transform: translateX(24px); opacity: 0 } to { transform: translateX(0); opacity: 1 } }`}</style>
        <div className="flex items-center justify-between border-b border-line px-6 py-4">
          <div>
            <p className={`text-[10px] uppercase tracking-[0.2em] text-acc ${mode === 'terminal' ? 'mono' : ''}`}>
              {mode === 'terminal' ? '/// Control room' : 'Control room'}
            </p>
            <p className="mt-1 text-[15px] font-semibold tracking-tight">Revision preferences</p>
          </div>
          <button
            onClick={close}
            aria-label="Close settings"
            className="mono rounded-md border border-line p-2 text-muted t-fast hover:border-line-strong hover:text-fg focus-visible:outline-acc"
          >
            <X size={14} />
          </button>
        </div>
        <SettingsContent />
      </div>
    </div>
  )
}
