'use client'

/*
 * LEGAL & DISCLAIMERS — the fine print, deliberately reachable from the
 * footer and nowhere else. One reading column, numbered sections, same
 * masthead vocabulary as the rest of the site: flat eyebrow in Focus,
 * glass panel in Studio and Hybrid. The copy is written to be read once
 * and understood — no small print about the small print.
 */

import React from 'react'
import { eyebrowText } from './ui-bits'
import { useSettings } from '@/lib/site/stores'

const UPDATED = '16 October 2026'

const SECTIONS: { title: string; body: React.ReactNode }[] = [
  {
    title: 'What this app is',
    body: (
      <>
        <p>
          IAL Chem is an independent revision aid for Pearson Edexcel International A Level
          Chemistry. It covers the 2018 specification, topics 1 to 10, across both exam units
          WCH11 and WCH12, and gathers topic notes, a specification index, flashcards and
          revision sets in one place.
        </p>
        <p>
          It is built to sit alongside your official materials — the specification itself,
          past papers and mark schemes, and your teachers — not to replace any of them. Where
          the app and the official specification ever appear to disagree, the official
          specification wins.
        </p>
      </>
    ),
  },
  {
    title: 'Independence and trademarks',
    body: (
      <>
        <p>
          IAL Chem is not affiliated with, endorsed by, sponsored by or connected to Pearson
          Education Ltd or Edexcel in any way. Pearson Edexcel, Edexcel and the unit codes
          WCH11 and WCH12 are the property of Pearson Education Ltd and are used here purely
          to identify the qualification these notes are written for.
        </p>
        <p>
          Specification point numbers and statements are referenced so you can check every
          claim against the published specification. That specification remains the property
          of Pearson Education Ltd, and the version published by Pearson is the authoritative
          one in all cases.
        </p>
      </>
    ),
  },
  {
    title: 'Accuracy of the notes',
    body: (
      <>
        <p>
          Every effort goes into keeping the notes correct, complete and faithful to the
          specification — but they are provided as-is, and no warranty of accuracy,
          completeness or fitness for a particular purpose is given. Mistakes can survive
          review, and examinable content can change between exam series.
        </p>
        <p>
          Always check anything that matters against the official specification and past
          papers, and treat your teachers and tutors as the final word on what the exam will
          demand. Relying on this app alone for exam-critical detail is done at your own
          risk.
        </p>
      </>
    ),
  },
  {
    title: 'Revision tools are not exam advice',
    body: (
      <>
        <p>
          Progress tracking, read ticks, flashcard ratings and revision sets are general
          study tools. They reflect only what you have done in this app, not what any future
          exam paper will contain, and nothing here predicts or claims to predict exam
          content or emphasis.
        </p>
        <p>
          Your results depend on many factors outside this app, and no particular grade,
          outcome or improvement is promised by using it. Any revision strategy the interface
          suggests is common practice, not professional or educational advice tailored to
          you.
        </p>
      </>
    ),
  },
  {
    title: 'Your data stays with you',
    body: (
      <>
        <p>
          The app has no accounts, no sign-ups and no tracking. Everything you generate —
          read ticks, flashcard ratings, specification picks, saved revision sets, interface
          settings — is stored in your own browser's local storage and never leaves your
          device.
        </p>
        <p>
          That also means the data is only as durable as your browser storage: clearing site
          data, private windows and aggressive browser clean-ups will erase your progress
          permanently. Anything you care about should be exported first — a revision set
          prints or copies cleanly from its own page.
        </p>
      </>
    ),
  },
  {
    title: 'Limitation of liability',
    body: (
      <>
        <p>
          To the fullest extent permitted by law, IAL Chem and its author accept no liability
          for any loss or damage — including grades, opportunities, time or money — arising
          from using the app, from relying on its content, or from any errors or omissions
          in it.
        </p>
        <p>
          Use the app as one tool among several, and verify anything exam-critical
          independently. If your school or institution requires official materials, those
          always take precedence over anything written here.
        </p>
      </>
    ),
  },
  {
    title: 'Changes',
    body: (
      <>
        <p>
          The notes, the features and this page can change at any time without notice. The
          content is checked against the 2018 Edexcel specification; future reforms to the
          qualification are out of scope until they take effect.
        </p>
        <p>
          Continued use of the app after a change counts as acceptance of the version in
          force at that time. The date below is the last review of this page.
        </p>
      </>
    ),
  },
]

export function Legal() {
  const mode = useSettings((s) => s.uiMode)
  const glass = mode !== 'terminal'

  const intro = (
    <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-muted">
      The terms below cover your use of IAL Chem. They are written to be read once and
      understood, not hidden in the small print — so if anything here surprises you, that is
      a bug in the copy, not a feature.
    </p>
  )

  return (
    <div className="mx-auto max-w-[820px] px-6 pb-24 pt-12">
      {/* ---------- masthead ---------- */}
      {glass ? (
        <header className="lab-glass rounded-[26px] p-7 sm:p-10">
          <span className="lab-chip">{eyebrowText(mode, 'The fine print')}</span>
          <h1 className="mt-5 text-3xl font-semibold tracking-tight sm:text-4xl">
            Legal &amp; <span className="serif-accent text-acc">disclaimers</span>.
          </h1>
          {intro}
        </header>
      ) : (
        <header>
          <p className="eyebrow">{eyebrowText(mode, 'The fine print')}</p>
          <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
            Legal &amp; <span className="serif-accent text-acc">disclaimers</span>.
          </h1>
          {intro}
        </header>
      )}

      {/* ---------- numbered sections ---------- */}
      <div className="reading mt-12 space-y-12">
        {SECTIONS.map((sec, i) => (
          <section key={sec.title} aria-label={sec.title}>
            {glass ? (
              <>
                <span aria-hidden className="warm-dash block" />
                <p className="mono mt-4 text-[13px] font-bold tracking-tight text-acc">
                  {String(i + 1).padStart(2, '0')}
                </p>
                <h2 className="display-serif mt-2 text-[21px] font-semibold tracking-tight text-fg">
                  {sec.title}
                </h2>
              </>
            ) : (
              <>
                <p className="mono text-[10.5px] uppercase tracking-[0.18em] text-faint">
                  {String(i + 1).padStart(2, '0')} / {SECTIONS.length}
                </p>
                <h2 className="mt-1.5 text-[19px] font-semibold tracking-tight text-fg">
                  {sec.title}
                </h2>
              </>
            )}
            <div className="mt-4 space-y-3 text-[14.5px] leading-relaxed text-muted [&_strong]:font-semibold [&_strong]:text-fg">
              {sec.body}
            </div>
          </section>
        ))}
      </div>

      {/* ---------- colophon ---------- */}
      <p className="mono mt-14 border-t border-line pt-5 text-[10px] uppercase tracking-[0.16em] text-faint">
        last updated {UPDATED} · applies to this site and its content
      </p>
    </div>
  )
}
