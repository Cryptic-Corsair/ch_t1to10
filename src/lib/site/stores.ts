'use client'

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

// ============================================================
// SETTINGS — the Control Room
// ============================================================

export type ThemeName = 'midnight' | 'carbon' | 'paper' | 'sepia'
export type AccentName = 'coral' | 'amber' | 'mint' | 'rose' | 'violet' | 'cyan'
export type FontFamily = 'sans' | 'serif' | 'mono'
export type UiMode = 'terminal' | 'lab' | 'hybrid'

/* Three interfaces, three different websites:
   terminal ("Focus")  — the control desk homepage + a warm student reading room for notes
   lab ("Studio")      — a glassmorphic neon instrument panel (floating glass, glow)
   hybrid ("Hybrid")   — Studio's glass aesthetics wrapped around Focus's reading room:
                         glass nav + aurora up front, Focus's card system inside the topics */
export const UI_MODES: { value: UiMode; label: string; blurb: string }[] = [
  { value: 'terminal', label: 'Focus', blurb: 'The control desk — mono, hairlines and dot grid up front; a warm, focused reading room inside the topics.' },
  { value: 'lab', label: 'Studio', blurb: 'A glass instrument panel — floating glass nav, aurora glow, gradient type, pill chrome.' },
  { value: 'hybrid', label: 'Hybrid', blurb: 'Studio’s glass and glow wrapped around Focus’s reading room — glass nav and aurora up front, Focus’s cards and floating contents inside the topics.' },
]

/* Each interface is a different site with its own native palette.
   themeByMode / accentByMode remember what you chose per interface. */
export const MODE_PRESETS: Record<UiMode, { theme: ThemeName; accent: AccentName }> = {
  terminal: { theme: 'midnight', accent: 'coral' },
  lab: { theme: 'carbon', accent: 'violet' },
  hybrid: { theme: 'carbon', accent: 'violet' },
}

interface SettingsState {
  uiMode: UiMode
  theme: ThemeName
  accent: AccentName
  fontFamily: FontFamily
  fontSize: number      // 0..3 → 15 / 16 / 17.5 / 19 px
  lineHeight: number    // 0..2 → 1.5 / 1.65 / 1.8
  width: 'normal' | 'wide'
  focusMode: boolean
  motion: 'normal' | 'reduced'
  showOutline: boolean  // show "what's covered" lists on queued sections
  themeByMode: Record<UiMode, ThemeName>    // per-interface palette memory
  accentByMode: Record<UiMode, AccentName>
  set: (patch: Partial<Omit<SettingsState, 'set' | 'reset' | 'themeByMode' | 'accentByMode'>>) => void
  reset: () => void
}

const DEFAULTS = {
  uiMode: 'terminal' as UiMode,
  theme: 'midnight' as ThemeName,
  accent: 'coral' as AccentName,
  fontFamily: 'sans' as FontFamily,
  fontSize: 1,
  lineHeight: 1,
  width: 'normal' as const,
  focusMode: false,
  motion: 'normal' as const,
  showOutline: true,
}

export const useSettings = create<SettingsState>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      themeByMode: { terminal: 'midnight', lab: 'carbon', hybrid: 'carbon' },
      accentByMode: { terminal: 'coral', lab: 'violet', hybrid: 'violet' },
      set: (patch) =>
        set((st) => {
          const next = { ...st, ...patch }
          if (patch.uiMode && patch.uiMode !== st.uiMode) {
            // switching interface: restore that interface's remembered palette
            next.theme = st.themeByMode[patch.uiMode] ?? MODE_PRESETS[patch.uiMode].theme
            next.accent = st.accentByMode[patch.uiMode] ?? MODE_PRESETS[patch.uiMode].accent
          }
          if (patch.theme) next.themeByMode = { ...st.themeByMode, [next.uiMode]: patch.theme }
          if (patch.accent) next.accentByMode = { ...st.accentByMode, [next.uiMode]: patch.accent }
          return next
        }),
      reset: () =>
        set({
          ...DEFAULTS,
          themeByMode: { terminal: 'midnight', lab: 'carbon', hybrid: 'carbon' },
          accentByMode: { terminal: 'coral', lab: 'violet', hybrid: 'violet' },
        }),
    }),
    {
      name: 'ialchem-settings',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
    }
  )
)

/* Align the per-interface palette memory with whatever the user had saved
   before this feature existed (their active theme belongs to their mode). */
export function alignModeMemory() {
  const s = useSettings.getState()
  useSettings.setState({
    themeByMode: { ...s.themeByMode, [s.uiMode]: s.theme },
    accentByMode: { ...s.accentByMode, [s.uiMode]: s.accent },
  })
}

// ============================================================
// PROGRESS — read sections + activity log
// ============================================================

interface ProgressState {
  read: Record<string, true>            // key: `${topicSlug}/${sectionKey}`
  activity: string[]                    // ISO date strings (yyyy-mm-dd), one entry per action
  lastTopic: string | null
  markRead: (topicSlug: string, sectionKey: string) => void
  markUnread: (topicSlug: string, sectionKey: string) => void
  markAll: (topicSlug: string, sectionKeys: string[], read: boolean) => void
  touch: (topicSlug: string) => void
  reset: () => void
}

const today = () => new Date().toISOString().slice(0, 10)

export const useProgress = create<ProgressState>()(
  persist(
    (set) => ({
      read: {},
      activity: [],
      lastTopic: null,
      markRead: (t, s) =>
        set((st) => ({
          read: { ...st.read, [`${t}/${s}`]: true },
          activity: [...st.activity.slice(-499), today()],
        })),
      markUnread: (t, s) =>
        set((st) => {
          const next = { ...st.read }
          delete next[`${t}/${s}`]
          return { read: next }
        }),
      markAll: (t, keys, read) =>
        set((st) => {
          const next = { ...st.read }
          for (const k of keys) {
            if (read) next[`${t}/${k}`] = true as const
            else delete next[`${t}/${k}`]
          }
          return { read: next, activity: read ? [...st.activity.slice(-499), today()] : st.activity }
        }),
      touch: (t) => set({ lastTopic: t }),
      reset: () => set({ read: {}, activity: [], lastTopic: null }),
    }),
    {
      name: 'ialchem-progress',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
    }
  )
)

// ============================================================
// FLASHCARD STATS
// ============================================================

export type CardVerdict = 'known' | 'again'

interface CardStat { known: number; again: number; last?: CardVerdict }

interface CardsState {
  stats: Record<string, CardStat>      // key: cardId
  sessions: number
  grade: (cardId: string, v: CardVerdict) => void
  reset: () => void
}

export const useCards = create<CardsState>()(
  persist(
    (set) => ({
      stats: {},
      sessions: 0,
      grade: (id, v) =>
        set((st) => {
          const cur = st.stats[id] ?? { known: 0, again: 0 }
          const next: CardStat = {
            known: cur.known + (v === 'known' ? 1 : 0),
            again: cur.again + (v === 'again' ? 1 : 0),
            last: v,
          }
          return { stats: { ...st.stats, [id]: next } }
        }),
      reset: () => set({ stats: {}, sessions: 0 }),
    }),
    {
      name: 'ialchem-cards',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
    }
  )
)

// ============================================================
// SPEC PICKS — the points behind custom revision notes
// ============================================================

export interface SpecSet {
  id: string
  name: string
  picks: string[]                      // spec point codes, e.g. ["5.6", "8.3"]
  savedAt: string                      // ISO timestamp
}

interface SpecPicksState {
  picks: string[]                       // the working selection, e.g. ["5.6", "8.3"]
  sets: SpecSet[]                       // named selections saved for later
  activeSetId: string | null            // the loaded set (null = free selection)
  toggle: (code: string) => void
  setPicks: (codes: string[]) => void
  clear: () => void
  saveSet: (name: string) => string     // returns the new set's id
  overwriteSet: (id: string) => void
  loadSet: (id: string) => void
  renameSet: (id: string, name: string) => void
  deleteSet: (id: string) => void
}

const newSetId = () => `set-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`

export const useSpecPicks = create<SpecPicksState>()(
  persist(
    (set) => ({
      picks: [],
      sets: [],
      activeSetId: null,
      toggle: (code) =>
        set((st) => ({
          picks: st.picks.includes(code) ? st.picks.filter((c) => c !== code) : [...st.picks, code],
          // editing a loaded set by hand detaches it — the saved copy stays as-is
          activeSetId: null,
        })),
      setPicks: (codes) => set({ picks: codes, activeSetId: null }),
      clear: () => set({ picks: [], activeSetId: null }),
      saveSet: (name) => {
        const id = newSetId()
        set((st) => ({
          sets: [...st.sets, { id, name: name.trim(), picks: [...st.picks], savedAt: new Date().toISOString() }],
          activeSetId: id,
        }))
        return id
      },
      overwriteSet: (id) =>
        set((st) => ({
          sets: st.sets.map((s) => (s.id === id ? { ...s, picks: [...st.picks], savedAt: new Date().toISOString() } : s)),
          activeSetId: id,
        })),
      loadSet: (id) =>
        set((st) => {
          const target = st.sets.find((s) => s.id === id)
          return target ? { picks: [...target.picks], activeSetId: id } : {}
        }),
      renameSet: (id, name) =>
        set((st) => ({ sets: st.sets.map((s) => (s.id === id ? { ...s, name: name.trim() } : s)) })),
      deleteSet: (id) =>
        set((st) => ({
          sets: st.sets.filter((s) => s.id !== id),
          activeSetId: st.activeSetId === id ? null : st.activeSetId,
        })),
    }),
    {
      name: 'ialchem-spec-picks',
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
    }
  )
)

// ============================================================
// UI STORE — transient
// ============================================================

interface UiState {
  settingsOpen: boolean
  paletteOpen: boolean
  openSettings: () => void
  closeSettings: () => void
  toggleSettings: () => void
  setPalette: (open: boolean) => void
}

export const useUi = create<UiState>((set) => ({
  settingsOpen: false,
  paletteOpen: false,
  openSettings: () => set({ settingsOpen: true }),
  closeSettings: () => set({ settingsOpen: false }),
  toggleSettings: () => set((s) => ({ settingsOpen: !s.settingsOpen })),
  setPalette: (open) => set({ paletteOpen: open }),
}))

// ============================================================
// hydration (client-only, after mount)
// ============================================================

export function hydrateStores() {
  useSettings.persist.rehydrate()
  useProgress.persist.rehydrate()
  useCards.persist.rehydrate()
  useSpecPicks.persist.rehydrate()
  migrateRemovedModes()
  alignModeMemory()
}

/* Old interfaces ('scholar' Atlas, 'minimal' Print, 'classic') were removed.
   If a browser ever saved one, snap it back to a valid interface. */
export function migrateRemovedModes() {
  const s = useSettings.getState()
  if (s.uiMode === 'terminal' || s.uiMode === 'lab' || s.uiMode === 'hybrid') return
  const legacy = s.themeByMode as Record<string, ThemeName | undefined>
  const legacyAcc = s.accentByMode as Record<string, AccentName | undefined>
  useSettings.setState({
    uiMode: 'terminal',
    theme: legacy.terminal ?? MODE_PRESETS.terminal.theme,
    accent: legacyAcc.terminal ?? MODE_PRESETS.terminal.accent,
    themeByMode: { ...s.themeByMode, terminal: legacy.terminal ?? 'midnight' },
    accentByMode: { ...s.accentByMode, terminal: legacyAcc.terminal ?? 'coral' },
  })
}

// ---------- helpers ----------

export function applySettingsToDom(s: SettingsState) {
  if (typeof document === 'undefined') return
  const d = document.documentElement
  d.dataset.uimode = s.uiMode
  d.dataset.theme = s.theme
  d.dataset.accent = s.accent
  d.dataset.font = s.fontFamily
  d.dataset.motion = s.motion
  d.dataset.focusmode = s.focusMode ? 'on' : 'off'
  const r = d.style
  r.setProperty('--content-fs', ['15px', '16px', '17.5px', '19px'][s.fontSize] ?? '16px')
  r.setProperty('--content-lh', ['1.5', '1.65', '1.8'][s.lineHeight] ?? '1.65')
  r.setProperty('--content-max', s.width === 'wide' ? '840px' : '720px')
  if (s.fontFamily === 'serif') r.setProperty('--font-read-face', 'Lora, Georgia, serif')
  else if (s.fontFamily === 'mono') r.setProperty('--font-read-face', 'var(--font-geist-mono), ui-monospace, monospace')
  else r.removeProperty('--font-read-face')
}

export function cycleUiMode(): UiMode {
  const order: UiMode[] = ['terminal', 'lab', 'hybrid']
  const cur = useSettings.getState().uiMode
  const next = order[(order.indexOf(cur) + 1) % order.length]
  useSettings.getState().set({ uiMode: next })
  applySettingsToDom(useSettings.getState())
  return next
}
