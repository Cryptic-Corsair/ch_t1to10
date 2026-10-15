'use client'

import { useCallback, useEffect, useLayoutEffect, useState } from 'react'

export interface Route {
  name: 'home' | 'topics' | 'topic' | 'flashcards' | 'deck' | 'progress' | 'spec' | 'notes' | 'settings' | 'not-found'
  slug?: string
  section?: string
}

export function parseHash(hash: string): Route {
  const h = hash.replace(/^#/, '').replace(/^\/+/, '')
  if (!h) return { name: 'home' }
  const parts = h.split('/').filter(Boolean)
  switch (parts[0]) {
    case 'topics':
      return { name: 'topics' }
    case 'topic':
      if (parts[1]) return { name: 'topic', slug: parts[1], section: parts[2] }
      return { name: 'topics' }
    case 'flashcards':
      return { name: 'flashcards' }
    case 'deck':
      if (parts[1]) return { name: 'deck', slug: parts[1] }
      return { name: 'flashcards' }
    case 'progress':
      return { name: 'progress' }
    case 'spec':
      return { name: 'spec' }
    case 'notes':
      return { name: 'notes' }
    case 'settings':
      return { name: 'settings' }
    default:
      return { name: 'home' }
  }
}

export function navigate(to: string) {
  const target = to.startsWith('#') ? to : `#${to}`
  if (window.location.hash === target) return
  window.location.hash = target
}

// layout effect on the client (runs before paint — no route flash),
// plain effect on the server (never runs, keeps SSR clean)
const useIsomorphicLayoutEffect =
  typeof window !== 'undefined' ? useLayoutEffect : useEffect

export function useRoute(): [Route, (to: string) => void] {
  // First client render deliberately mirrors the server ('home') so the
  // hydrated HTML matches; the real hash is aligned before first paint.
  const [route, setRoute] = useState<Route>({ name: 'home' })

  useIsomorphicLayoutEffect(() => {
    const onChange = () => setRoute(parseHash(window.location.hash))
    onChange()
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])

  const go = useCallback((to: string) => {
    navigate(to)
    // hashchange handles state; immediate update for snappiness
    setRoute(parseHash(to))
  }, [])

  return [route, go]
}
