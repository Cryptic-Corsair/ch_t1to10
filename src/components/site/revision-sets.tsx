'use client'

/*
 * REVISION SETS — save the current selection of spec points under a name,
 * reload it whenever the revision mood strikes. One popover shared by the
 * spec index and the revision notes pages, so sets are always within reach.
 */

import React, { useEffect, useRef, useState } from 'react'
import { BookmarkPlus, Check, Pencil, Save, Trash2, X } from 'lucide-react'
import type { UiMode } from '@/lib/site/stores'
import { useSpecPicks } from '@/lib/site/stores'

const fmtDate = (iso: string) => {
  try {
    return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
  } catch {
    return ''
  }
}

export function RevisionSets({ mode }: { mode: UiMode }) {
  const picks = useSpecPicks((s) => s.picks)
  const sets = useSpecPicks((s) => s.sets)
  const activeSetId = useSpecPicks((s) => s.activeSetId)
  const saveSet = useSpecPicks((s) => s.saveSet)
  const overwriteSet = useSpecPicks((s) => s.overwriteSet)
  const loadSet = useSpecPicks((s) => s.loadSet)
  const renameSet = useSpecPicks((s) => s.renameSet)
  const deleteSet = useSpecPicks((s) => s.deleteSet)

  const [open, setOpen] = useState(false)
  const [pos, setPos] = useState({ top: 0, right: 12 })
  const [naming, setNaming] = useState(false)
  const [nameValue, setNameValue] = useState('')
  const [renamingId, setRenamingId] = useState<string | null>(null)
  const [renameValue, setRenameValue] = useState('')
  const [confirmDel, setConfirmDel] = useState<string | null>(null)

  const wrapRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)
  const nameRef = useRef<HTMLInputElement>(null)
  const renameRef = useRef<HTMLInputElement>(null)

  /* anchor the panel to the trigger in viewport coordinates so it can never
     spill past either screen edge, wherever the trigger happens to wrap */
  const openPanel = () => {
    const r = triggerRef.current?.getBoundingClientRect()
    if (r) {
      const width = Math.min(window.innerWidth * 0.92, 340)
      const maxRight = Math.max(12, window.innerWidth - 12 - width)
      const right = Math.min(Math.max(12, window.innerWidth - r.right), maxRight)
      const top = Math.max(12, Math.min(r.bottom + 8, window.innerHeight - 440))
      setPos({ top, right })
    }
    setOpen(true)
  }

  /* close on outside pointer-down or Escape */
  useEffect(() => {
    if (!open) return
    const onDown = (e: PointerEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) setOpen(false)
    }
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    window.addEventListener('pointerdown', onDown)
    window.addEventListener('keydown', onKey)
    return () => {
      window.removeEventListener('pointerdown', onDown)
      window.removeEventListener('keydown', onKey)
    }
  }, [open])

  /* focus the inline input the moment it appears */
  useEffect(() => {
    if (naming) setTimeout(() => nameRef.current?.focus(), 20)
  }, [naming])
  useEffect(() => {
    if (renamingId) setTimeout(() => renameRef.current?.focus(), 20)
  }, [renamingId])

  /* saving under an existing name (any case) rewrites that set */
  const commitSave = () => {
    const name = nameValue.trim()
    if (!name || picks.length === 0) return
    const existing = sets.find((s) => s.name.toLowerCase() === name.toLowerCase())
    if (existing) overwriteSet(existing.id)
    else saveSet(name)
    setNameValue('')
    setNaming(false)
  }

  const commitRename = () => {
    const name = renameValue.trim()
    if (renamingId && name) renameSet(renamingId, name)
    setRenamingId(null)
  }

  return (
    <div ref={wrapRef} className="relative print:hidden">
      <button
        ref={triggerRef}
        type="button"
        onClick={() => (open ? setOpen(false) : openPanel())}
        aria-expanded={open}
        aria-label="Saved revision sets"
        className={`mono inline-flex items-center gap-2 rounded-lg border px-4 py-2.5 text-xs font-medium uppercase tracking-[0.12em] t-fast focus-visible:outline-acc active:translate-y-px ${
          open
            ? 'border-acc/50 bg-acc/10 text-acc'
            : 'border-line bg-transparent text-fg hover:border-line-strong hover:bg-elev'
        }`}
      >
        <BookmarkPlus size={14} />
        Sets
        {sets.length > 0 && (
          <span className="rounded-full bg-acc/15 px-1.5 py-0.5 text-[10px] font-semibold leading-none text-acc">
            {sets.length}
          </span>
        )}
      </button>

      {open && (
        <div
          className="fixed z-50 w-[min(92vw,340px)] overflow-hidden rounded-xl border border-line-strong bg-surface shadow-2xl"
          style={{ top: pos.top, right: pos.right }}
          role="dialog"
          aria-label="Revision sets"
        >
          {/* header */}
          <div className="flex items-center justify-between border-b border-line px-4 py-3">
            <p className="mono text-[10px] uppercase tracking-[0.2em] text-faint">
              Revision sets · {sets.length}
            </p>
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Close revision sets"
              className="t-fast text-faint hover:text-fg focus-visible:outline-acc"
            >
              <X size={14} />
            </button>
          </div>

          {/* save the current selection */}
          <div className="border-b border-line px-4 py-3.5">
            {naming ? (
              <div className="flex items-center gap-2">
                <input
                  ref={nameRef}
                  value={nameValue}
                  onChange={(e) => setNameValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') commitSave()
                    if (e.key === 'Escape') {
                      setNaming(false)
                      setNameValue('')
                    }
                  }}
                  placeholder="Name this selection…"
                  aria-label="Name for the current selection"
                  maxLength={48}
                  className="mono w-full rounded-lg border border-line-strong bg-transparent px-3 py-2 text-[12.5px] text-fg placeholder:text-faint focus:border-acc/60 focus:outline-none"
                />
                <button
                  type="button"
                  onClick={commitSave}
                  disabled={!nameValue.trim() || picks.length === 0}
                  aria-label="Save the current selection as a set"
                  className="mono flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-acc text-on-acc t-fast hover:opacity-85 disabled:opacity-40 focus-visible:outline-acc"
                >
                  <Check size={14} />
                </button>
              </div>
            ) : (
              <button
                type="button"
                onClick={() => {
                  setNameValue('')
                  setNaming(true)
                }}
                disabled={picks.length === 0}
                className="mono flex w-full items-center gap-2.5 rounded-lg border border-dashed border-line px-3 py-2.5 text-[11px] uppercase tracking-[0.12em] text-muted t-fast hover:border-acc/40 hover:text-acc disabled:pointer-events-none disabled:opacity-40 focus-visible:outline-acc"
              >
                <Save size={13} />
                {picks.length > 0
                  ? `Save current selection · ${picks.length} point${picks.length === 1 ? '' : 's'}`
                  : 'Tick points to save a set'}
              </button>
            )}
          </div>

          {/* the saved sets */}
          <div className="max-h-[300px] overflow-y-auto p-1.5">
            {sets.length === 0 ? (
              <p className="mono px-3 py-6 text-center text-[11.5px] leading-relaxed text-faint">
                {'// no sets yet\n// tick some spec points and save them here for later'}
              </p>
            ) : (
              sets.map((s) => {
                const loaded = activeSetId === s.id
                const stale = loaded && s.picks.join(',') !== picks.join(',')
                return (
                  <div
                    key={s.id}
                    className={`group/set flex items-center gap-1 rounded-lg px-2 py-1.5 t-fast ${
                      loaded ? 'bg-acc/8' : 'hover:bg-elev'
                    }`}
                  >
                    {renamingId === s.id ? (
                      <input
                        ref={renameRef}
                        value={renameValue}
                        onChange={(e) => setRenameValue(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') commitRename()
                          if (e.key === 'Escape') setRenamingId(null)
                        }}
                        onBlur={commitRename}
                        maxLength={48}
                        aria-label="Rename the set"
                        className="mono w-full rounded-md border border-acc/50 bg-transparent px-2 py-1.5 text-[12.5px] text-fg focus:outline-none"
                      />
                    ) : confirmDel === s.id ? (
                      <>
                        <p className="min-w-0 flex-1 truncate text-[12.5px] text-fg">
                          Delete “{s.name}”?
                        </p>
                        <button
                          type="button"
                          onClick={() => {
                            deleteSet(s.id)
                            setConfirmDel(null)
                          }}
                          aria-label={`Confirm deleting ${s.name}`}
                          className="mono rounded-md border border-acc/40 px-2 py-1 text-[10px] uppercase tracking-[0.1em] text-acc t-fast hover:bg-acc/10 focus-visible:outline-acc"
                        >
                          yes
                        </button>
                        <button
                          type="button"
                          onClick={() => setConfirmDel(null)}
                          aria-label="Cancel deleting"
                          className="mono rounded-md border border-line px-2 py-1 text-[10px] uppercase tracking-[0.1em] text-muted t-fast hover:text-fg focus-visible:outline-acc"
                        >
                          no
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          type="button"
                          onClick={() => loadSet(s.id)}
                          title={`Load ${s.name}`}
                          className="min-w-0 flex-1 rounded-md px-1.5 py-1 text-left focus-visible:outline-acc"
                        >
                          <span className="flex items-center gap-2">
                            <span className={`truncate text-[12.5px] font-medium ${loaded ? 'text-acc' : 'text-fg'}`}>
                              {s.name}
                            </span>
                            {loaded && (
                              <span className="mono shrink-0 rounded-full border border-acc/40 px-1.5 py-px text-[9px] uppercase tracking-[0.1em] text-acc">
                                {stale ? 'loaded · edited' : 'loaded'}
                              </span>
                            )}
                          </span>
                          <span className="mono mt-0.5 block text-[10px] text-faint">
                            {s.picks.length} point{s.picks.length === 1 ? '' : 's'} · {fmtDate(s.savedAt)}
                          </span>
                        </button>
                        <span className="flex shrink-0 items-center opacity-0 t-fast group-hover/set:opacity-100 focus-within:opacity-100">
                          <button
                            type="button"
                            onClick={() => overwriteSet(s.id)}
                            title="Overwrite with the current selection"
                            aria-label={`Overwrite ${s.name} with the current selection`}
                            disabled={s.picks.join(',') === picks.join(',')}
                            className="rounded-md p-1.5 text-faint t-fast hover:text-acc disabled:pointer-events-none disabled:opacity-30 focus-visible:outline-acc"
                          >
                            <Save size={13} />
                          </button>
                          <button
                            type="button"
                            onClick={() => {
                              setRenamingId(s.id)
                              setRenameValue(s.name)
                            }}
                            title="Rename"
                            aria-label={`Rename ${s.name}`}
                            className="rounded-md p-1.5 text-faint t-fast hover:text-fg focus-visible:outline-acc"
                          >
                            <Pencil size={13} />
                          </button>
                          <button
                            type="button"
                            onClick={() => setConfirmDel(s.id)}
                            title="Delete"
                            aria-label={`Delete ${s.name}`}
                            className="rounded-md p-1.5 text-faint t-fast hover:text-fg focus-visible:outline-acc"
                          >
                            <Trash2 size={13} />
                          </button>
                        </span>
                      </>
                    )}
                  </div>
                )
              })
            )}
          </div>
        </div>
      )}
    </div>
  )
}
