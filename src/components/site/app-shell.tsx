'use client'

import React, { useEffect, useMemo, useState, useSyncExternalStore } from 'react'
import type { TopicData } from '@/lib/site/types'
import { hydrateStores, useSettings, useUi, applySettingsToDom } from '@/lib/site/stores'
import { useRoute } from '@/lib/site/router'
import { Nav, Footer } from './chrome'
import { Home } from './home'
import { Topics } from './topics'
import { TopicDetail } from './topic-detail'
import { Flashcards, Deck } from './flashcards'
import { ProgressView } from './progress'
import { SettingsPanel, SettingsContent } from './settings-panel'
import { CommandPalette } from './command-palette'
import { useProgress } from '@/lib/site/stores'

export interface AppStats {
  sections: number
  cards: number
  noted: number
}

export function AppShell({
  topics,
  stats,
}: {
  topics: TopicData[]
  stats: AppStats
}) {
  const [route, go] = useRoute()
  const mode = useSettings((s) => s.uiMode)
  // true on the client after hydration, false on the server (SSR-safe)
  const hydrated = useSyncExternalStore(
    () => () => {},
    () => true,
    () => false
  )

  // hydrate persisted stores from localStorage (external system, no React setState)
  useEffect(() => {
    hydrateStores()
  }, [])

  // apply settings on every change
  const settings = useSettings()
  useEffect(() => {
    if (hydrated) applySettingsToDom(settings)
  }, [settings, hydrated])

  const settingsOpen = useUi((s) => s.settingsOpen)
  const openSettings = useUi((s) => s.openSettings)
  const setPalette = useUi((s) => s.setPalette)
  const paletteOpen = useUi((s) => s.paletteOpen)

  // global keys: ⌘K palette, "/" palette, "s" settings (when not typing)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName
      const typing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT'
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        setPalette(!useUi.getState().paletteOpen)
        return
      }
      if (typing) return
      if (e.key === '/') {
        e.preventDefault()
        setPalette(true)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [setPalette])

  // scroll to top on route change (unless deep-linking a section)
  const routeKey = `${route.name}:${route.slug ?? ''}`
  useEffect(() => {
    if (route.name === 'topic' && route.section) return
    window.scrollTo({ top: 0 })
  }, [routeKey, route.name, route.section])

  const topic = useMemo(
    () => (route.slug ? topics.find((t) => t.slug === route.slug) : undefined),
    [topics, route.slug]
  )

  // settings route: render home beneath + ensure the panel is open
  useEffect(() => {
    if (route.name === 'settings') {
      if (!useUi.getState().settingsOpen) openSettings()
    }
  }, [route.name, openSettings])

  let view: React.ReactNode
  switch (route.name) {
    case 'topics':
      view = <Topics topics={topics} go={go} hydrated={hydrated} />
      break
    case 'topic':
      view = topic ? (
        <TopicDetail
          topic={topic}
          topics={topics}
          slug={topic.slug}
          sectionId={route.section}
          go={go}
          hydrated={hydrated}
        />
      ) : (
        <NotFound go={go} />
      )
      break
    case 'flashcards':
      view = <Flashcards topics={topics} go={go} hydrated={hydrated} />
      break
    case 'deck':
      view = topic ? (
        <Deck topic={topic} topics={topics} go={go} />
      ) : (
        <NotFound go={go} />
      )
      break
    case 'progress':
      view = <ProgressView topics={topics} go={go} hydrated={hydrated} />
      break
    case 'settings':
      view = <Home topics={topics} stats={stats} go={go} openSettings={openSettings} hydrated={hydrated} />
      break
    case 'not-found':
      view = <NotFound go={go} />
      break
    default:
      view = <Home topics={topics} stats={stats} go={go} openSettings={openSettings} hydrated={hydrated} />
  }

  return (
    <div className="app-root flex min-h-screen flex-col dotgrid">
      <a
        href="#main"
        className="mono sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-[90] focus:rounded-md focus:border focus:border-line-strong focus:bg-surface focus:px-3 focus:py-2 focus:text-[12px] focus:text-fg"
      >
        skip to content
      </a>
      <Nav route={route} topics={topics} total={stats.sections} />
      <main id="main" className="flex-1">
        {view}
      </main>
      <Footer go={go} />
      <SettingsPanel />
      <CommandPalette topics={topics} go={go} hydrated={hydrated} />
      {/* floating control-room button (mobile-friendly, voiced per interface) */}
      {!settingsOpen && !paletteOpen && (
        <button
          onClick={openSettings}
          aria-label="Open control room"
          title="Control room"
          className={
            mode !== 'terminal'
              ? 'lab-glass fab-ctl fixed bottom-5 right-5 z-40 flex h-11 items-center gap-2 rounded-full px-4 text-[12px] font-semibold text-muted shadow-lg t-fast hover:border-[color-mix(in_srgb,var(--acc)_45%,transparent)] hover:text-acc focus-visible:outline-acc print:hidden'
              : 'fab-ctl mono fixed bottom-5 right-5 z-40 flex h-11 w-11 items-center justify-center rounded-full border border-line-strong bg-surface text-muted shadow-lg t-fast hover:border-acc hover:text-acc focus-visible:outline-acc print:hidden'
          }
          style={mode !== 'terminal' ? { fontFamily: 'var(--font-grotesk), sans-serif' } : undefined}
        >
          <span className="text-[13px] font-semibold">Aa</span>
          {mode !== 'terminal' && <span className="hidden sm:inline">Control room</span>}
        </button>
      )}
    </div>
  )
}

function NotFound({ go }: { go: (to: string) => void }) {
  const read = useProgress((s) => s.read)
  const mode = useSettings((s) => s.uiMode)
  return (
    <div className="mx-auto max-w-[1200px] px-6 py-24 text-center">
      {mode === 'terminal' && (
        <>
          <p className="mono text-[13px] text-faint">$ cd {typeof window !== 'undefined' ? window.location.hash : ''}</p>
          <p className="mono mt-2 text-[13px] text-faint">{'// no such route — 404'}</p>
        </>
      )}
      <h1 className="mt-8 text-3xl font-semibold tracking-tight">
        This page <span className="serif-accent text-acc">precipitated</span> out.
      </h1>
      <p className="mt-3 text-[15px] text-muted">The link you followed doesn’t exist (read state kept: {Object.keys(read).length} sections).</p>
      <button
        onClick={() => go('/')}
        className="mono mt-8 rounded-lg border border-line px-4 py-2.5 text-[12px] uppercase tracking-[0.14em] text-fg t-fast hover:border-acc hover:text-acc focus-visible:outline-acc"
      >
        ← Back to home
      </button>
    </div>
  )
}
