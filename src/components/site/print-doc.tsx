import React from 'react'
import type { Block, SectionData, TopicData } from '@/lib/site/types'

/* ════════════════════════════════════════════════════════════════════
   PRINT DOC — a dedicated A4 revision document, NOT the webpage.
   Rendered at /print/[slug]; headless Chromium turns it into the PDF
   the SAVE PDF buttons download. Self-contained paper styles (literal
   colours, no theme tokens) so it ignores the reader's site theme.
   ════════════════════════════════════════════════════════════════════ */

const PD_CSS = `
  body { margin: 0 !important; background: #FCFBF8 !important; color: #201E1A !important; }

  .pd-doc {
    --pd-ink: #201E1A;
    --pd-body: #2E2B26;
    --pd-muted: #6B665C;
    --pd-faint: #98938A;
    --pd-line: #E5E1D6;
    --pd-line-strong: #CFCABB;
    --pd-tint: #F4F1E9;
    --pd-acc: #D9482E;
    --pd-acc-tint: #FBEFEA;
    --pd-display: 'Playfair Display', Georgia, serif;
    --pd-bodyface: 'Lora', var(--font-geist-sans), Georgia, serif;
    --pd-mono: var(--font-geist-mono), 'DejaVu Sans Mono', monospace;
    --pd-grotesk: 'Space Grotesk', var(--font-geist-sans), sans-serif;
    color: var(--pd-body);
    font-family: var(--pd-bodyface);
    font-size: 10pt;
    line-height: 1.62;
  }
  .pd-doc * { box-sizing: border-box; }

  /* ---- shared atoms ---- */
  .pd-eyebrow { font-family: var(--pd-mono); font-size: 6.8pt; letter-spacing: 0.22em; text-transform: uppercase; color: var(--pd-faint); }
  .pd-hairline { border: 0; border-top: 0.8pt solid var(--pd-line); margin: 0; }
  .pd-rule-ink { border: 0; border-top: 1.6pt solid var(--pd-ink); margin: 0; }
  .pd-strong { font-weight: 600; color: var(--pd-ink); }
  .pd-code { font-family: var(--pd-mono); font-size: 0.82em; background: var(--pd-tint); padding: 0.5pt 3pt; border-radius: 2pt; color: var(--pd-ink); }

  /* ---- cover ---- */
  .pd-cover { min-height: 253mm; display: flex; flex-direction: column; break-after: page; }
  .pd-brandbar { display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 8pt; border-bottom: 1.6pt solid var(--pd-ink); }
  .pd-brand { font-family: var(--pd-mono); font-size: 7.5pt; font-weight: 700; letter-spacing: 0.18em; color: var(--pd-ink); }
  .pd-brand em { font-style: normal; color: var(--pd-acc); }
  .pd-cover-eyebrow { margin-top: 30pt; font-family: var(--pd-mono); font-size: 7.2pt; letter-spacing: 0.24em; text-transform: uppercase; color: var(--pd-muted); }
  .pd-ghost { font-family: var(--pd-grotesk); font-weight: 700; font-size: 118pt; line-height: 0.9; text-align: right; color: transparent; -webkit-text-stroke: 1pt #DCD7C9; margin: 6pt -2pt 0 0; user-select: none; }
  .pd-cover-title { font-family: var(--pd-display); font-weight: 600; font-size: 33pt; line-height: 1.12; color: var(--pd-ink); margin: -14pt 0 0; max-width: 150mm; }
  .pd-cover-bar { width: 30pt; height: 3.2pt; background: var(--pd-acc); margin: 16pt 0; }
  .pd-cover-sub { font-style: italic; font-size: 12pt; color: var(--pd-muted); margin: 0 0 14pt; max-width: 135mm; }
  .pd-cover-summary { font-size: 10pt; max-width: 128mm; margin: 0 0 22pt; }
  .pd-meta { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 0.8pt solid var(--pd-line-strong); border-bottom: 0.8pt solid var(--pd-line-strong); }
  .pd-meta-cell { padding: 9pt 10pt; border-left: 0.8pt solid var(--pd-line-strong); }
  .pd-meta-cell:first-child { border-left: 0; padding-left: 0; }
  .pd-meta-k { font-family: var(--pd-mono); font-size: 6.4pt; letter-spacing: 0.2em; text-transform: uppercase; color: var(--pd-faint); }
  .pd-meta-v { font-family: var(--pd-grotesk); font-weight: 600; font-size: 13.5pt; color: var(--pd-ink); margin-top: 3pt; }
  .pd-meta-v small { font-size: 9pt; font-weight: 500; color: var(--pd-muted); }
  .pd-cover-note { margin-top: 14pt; font-family: var(--pd-mono); font-size: 6.8pt; letter-spacing: 0.16em; text-transform: uppercase; color: var(--pd-faint); }
  .pd-cover-note b { color: var(--pd-acc); font-weight: 700; }
  .pd-cover-foot { margin-top: auto; padding-top: 10pt; border-top: 0.8pt solid var(--pd-line); display: flex; justify-content: space-between; gap: 20pt; font-size: 8pt; color: var(--pd-faint); }
  .pd-cover-foot .r { font-family: var(--pd-mono); font-size: 6.6pt; letter-spacing: 0.14em; text-transform: uppercase; white-space: nowrap; }

  /* ---- contents ---- */
  .pd-toc { break-after: page; }
  .pd-toc-title { font-family: var(--pd-display); font-weight: 600; font-size: 21pt; color: var(--pd-ink); margin: 4pt 0 2pt; }
  .pd-toc-list { margin-top: 12pt; }
  .pd-toc-row { display: flex; align-items: baseline; gap: 8pt; padding: 4pt 0; border-bottom: 0.6pt solid var(--pd-line); }
  .pd-toc-no { font-family: var(--pd-mono); font-size: 8.5pt; font-weight: 700; color: var(--pd-acc); min-width: 22pt; }
  .pd-toc-name { font-size: 10pt; color: var(--pd-ink); font-weight: 500; }
  .pd-toc-dots { flex: 1; border-bottom: 1pt dotted var(--pd-line-strong); transform: translateY(-2.5pt); min-width: 14pt; }
  .pd-toc-spec { font-family: var(--pd-mono); font-size: 7pt; letter-spacing: 0.06em; color: var(--pd-faint); white-space: nowrap; }
  .pd-toc-min { font-family: var(--pd-mono); font-size: 7pt; color: var(--pd-faint); white-space: nowrap; min-width: 34pt; text-align: right; }
  .pd-toc-wip { font-family: var(--pd-mono); font-size: 6.4pt; letter-spacing: 0.1em; text-transform: uppercase; color: var(--pd-faint); border: 0.7pt solid var(--pd-line-strong); border-radius: 2pt; padding: 1pt 3.5pt; white-space: nowrap; }
  .pd-howto { margin-top: 14pt; background: var(--pd-tint); border-left: 2.5pt solid var(--pd-acc); padding: 9pt 12pt; font-size: 9.3pt; break-inside: avoid; }
  .pd-howto .pd-eyebrow { display: block; margin-bottom: 4pt; color: var(--pd-acc); }
  .pd-howto p { margin: 0; color: var(--pd-muted); }

  /* ---- section ---- */
  .pd-sec { margin-top: 24pt; }
  .pd-sec:first-of-type { margin-top: 0; }
  .pd-sec-chips { display: flex; align-items: center; gap: 7pt; }
  .pd-chip-spec { font-family: var(--pd-mono); font-size: 7.2pt; font-weight: 700; letter-spacing: 0.14em; color: #fff; background: var(--pd-acc); border-radius: 2.5pt; padding: 2.5pt 6pt; }
  .pd-chip-min { font-family: var(--pd-mono); font-size: 6.8pt; letter-spacing: 0.14em; color: var(--pd-faint); border: 0.7pt solid var(--pd-line-strong); border-radius: 2.5pt; padding: 2.5pt 6pt; }
  .pd-sec-title { font-family: var(--pd-display); font-weight: 600; font-size: 16.5pt; line-height: 1.2; color: var(--pd-ink); margin: 8pt 0 7pt; break-after: avoid; }
  .pd-sec-head { break-after: avoid; break-inside: avoid; }
  .pd-statement { background: var(--pd-tint); border-left: 2.8pt solid var(--pd-acc); padding: 9pt 12pt; break-inside: avoid; }
  .pd-statement .pd-eyebrow { display: block; margin-bottom: 3.5pt; color: var(--pd-acc); }
  .pd-statement p { margin: 0; font-size: 10.3pt; font-weight: 500; line-height: 1.5; color: var(--pd-ink); }
  .pd-blurb { font-style: italic; font-size: 9.6pt; color: var(--pd-muted); margin: 8pt 0 0; }

  /* ---- blocks ---- */
  .pd-p { margin: 0 0 7pt; }
  .pd-h3 { display: flex; align-items: center; gap: 7pt; font-family: var(--pd-display); font-weight: 600; font-size: 12.5pt; color: var(--pd-ink); margin: 15pt 0 6pt; break-after: avoid; }
  .pd-h3::before { content: ''; width: 3.2pt; height: 11pt; background: var(--pd-acc); border-radius: 1pt; flex: none; }
  .pd-def { background: var(--pd-tint); border: 0.7pt solid var(--pd-line); border-left: 2.8pt solid var(--pd-acc); border-radius: 2.5pt; padding: 8pt 11pt; margin: 9pt 0; break-inside: avoid; }
  .pd-def-term { font-weight: 700; color: var(--pd-ink); font-size: 10.3pt; margin: 3pt 0 2pt; }
  .pd-def-text { margin: 0; font-size: 9.6pt; color: var(--pd-muted); }
  .pd-eq { text-align: center; border-top: 0.8pt solid var(--pd-line-strong); border-bottom: 0.8pt solid var(--pd-line-strong); background: var(--pd-tint); padding: 10pt 8pt; margin: 10pt 0; break-inside: avoid; }
  .pd-eq-code { font-family: var(--pd-mono); font-size: 10.5pt; color: var(--pd-ink); margin: 0; white-space: pre-wrap; }
  .pd-eq-cap { margin: 5pt 0 0; font-style: italic; font-size: 8.4pt; color: var(--pd-muted); }
  .pd-list { margin: 7pt 0 9pt; padding: 0; list-style: none; }
  .pd-li { display: flex; gap: 8pt; padding: 2.6pt 0; }
  .pd-li-mark { flex: none; width: 5.6pt; height: 5.6pt; background: var(--pd-acc); opacity: 0.75; transform: rotate(45deg); margin-top: 5.4pt; }
  .pd-li-num { flex: none; font-family: var(--pd-mono); font-size: 8.6pt; font-weight: 700; color: var(--pd-acc); min-width: 13pt; padding-top: 1.2pt; }
  .pd-li-text { min-width: 0; }
  .pd-callout { border-radius: 2.5pt; padding: 8.5pt 11pt; margin: 9pt 0; break-inside: avoid; background: var(--pd-tint); border-left: 2.8pt solid var(--pd-line-strong); }
  .pd-callout.exam { background: var(--pd-acc-tint); border-left-color: var(--pd-acc); }
  .pd-callout-label { font-family: var(--pd-mono); font-size: 6.6pt; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--pd-acc); }
  .pd-callout:not(.exam) .pd-callout-label { color: var(--pd-muted); }
  .pd-callout-title { font-weight: 700; color: var(--pd-ink); font-size: 10pt; margin: 3pt 0 2pt; }
  .pd-callout-text { margin: 0; font-size: 9.4pt; color: var(--pd-muted); }
  .pd-worked { border: 0.9pt solid var(--pd-line-strong); border-radius: 3pt; margin: 11pt 0; break-inside: avoid; overflow: hidden; }
  .pd-worked-head { display: flex; align-items: baseline; gap: 8pt; background: var(--pd-tint); border-bottom: 0.7pt solid var(--pd-line); padding: 7pt 11pt; }
  .pd-worked-label { font-family: var(--pd-mono); font-size: 7pt; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--pd-acc); white-space: nowrap; }
  .pd-worked-title { font-weight: 600; font-size: 9.8pt; color: var(--pd-ink); }
  .pd-worked-body { padding: 10pt 11pt; }
  .pd-worked-problem { background: var(--pd-tint); border-radius: 2.5pt; padding: 7.5pt 10pt; }
  .pd-worked-problem p { margin: 2pt 0 0; font-size: 9.6pt; color: var(--pd-body); }
  .pd-step { display: flex; gap: 9pt; padding: 3pt 0; }
  .pd-step-n { flex: none; font-family: var(--pd-mono); font-size: 8.4pt; font-weight: 700; color: var(--pd-acc); border: 0.8pt solid var(--pd-line-strong); border-radius: 50%; width: 14pt; height: 14pt; display: flex; align-items: center; justify-content: center; margin-top: 1pt; }
  .pd-step-text { font-size: 9.5pt; color: var(--pd-body); }
  .pd-answer { display: flex; gap: 9pt; background: var(--pd-acc-tint); border-radius: 2.5pt; padding: 8pt 10pt; margin-top: 8pt; align-items: flex-start; }
  .pd-answer-k { font-family: var(--pd-mono); font-size: 6.6pt; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--pd-acc); white-space: nowrap; padding-top: 2.6pt; }
  .pd-answer-v { font-weight: 600; font-size: 10pt; color: var(--pd-ink); }
  .pd-table { width: 100%; border-collapse: collapse; margin: 10pt 0; font-size: 9.2pt; }
  .pd-table thead { display: table-header-group; }
  .pd-table th { font-family: var(--pd-mono); font-size: 6.8pt; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--pd-muted); text-align: left; padding: 5pt 6pt; border-top: 1.4pt solid var(--pd-ink); border-bottom: 0.8pt solid var(--pd-ink); }
  .pd-table td { padding: 5pt 6pt; vertical-align: top; border-bottom: 0.6pt solid var(--pd-line); color: var(--pd-body); }
  .pd-table tr:last-child td { border-bottom: 1.4pt solid var(--pd-ink); }
  .pd-table td:first-child { font-weight: 600; color: var(--pd-ink); }
  .pd-fig { margin: 11pt 0; break-inside: avoid; text-align: center; }
  .pd-fig img { width: 100%; height: auto; }
  .pd-fig-cap { margin: 5pt 8pt 0; font-size: 8.5pt; font-style: italic; color: var(--pd-muted); text-align: center; }
  .pd-fig-cap::before { content: 'FIG — '; font-family: var(--pd-mono); font-style: normal; font-size: 6.8pt; letter-spacing: 0.14em; color: var(--pd-acc); }
  .pd-outline { margin: 7pt 0 9pt; padding: 0; list-style: none; }
  .pd-wip-note { margin: 8pt 0; font-size: 9pt; font-style: italic; color: var(--pd-faint); }

  /* ---- end matter ---- */
  .pd-end { margin-top: 30pt; padding-top: 12pt; border-top: 1.6pt solid var(--pd-ink); break-inside: avoid; }
  .pd-end-k { text-align: center; font-family: var(--pd-mono); font-size: 7.2pt; font-weight: 700; letter-spacing: 0.3em; color: var(--pd-ink); }
  .pd-end-next { display: flex; flex-wrap: wrap; gap: 4pt; justify-content: center; margin-top: 9pt; }
  .pd-end-chip { font-family: var(--pd-mono); font-size: 6.6pt; letter-spacing: 0.08em; color: var(--pd-muted); border: 0.7pt solid var(--pd-line-strong); border-radius: 2pt; padding: 2pt 5pt; white-space: nowrap; }
  .pd-end-disc { text-align: center; font-size: 7.8pt; color: var(--pd-faint); margin: 10pt 0 0; }
`

/* tiny inline markdown (**bold**, *italic*, `code`) — server-safe, pd-styled */
function PInline({ text }: { text: string }) {
  const nodes: React.ReactNode[] = []
  const re = /(\*\*[^*]+\*\*|\*[^*\n]+\*|`[^`]+`)/g
  let last = 0
  let m: RegExpExecArray | null
  let k = 0
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) nodes.push(text.slice(last, m.index))
    const tok = m[0]
    if (tok.startsWith('**')) nodes.push(<strong key={k++} className="pd-strong">{tok.slice(2, -2)}</strong>)
    else if (tok.startsWith('`')) nodes.push(<code key={k++} className="pd-code">{tok.slice(1, -1)}</code>)
    else nodes.push(<em key={k++}>{tok.slice(1, -1)}</em>)
    last = m.index + tok.length
  }
  if (last < text.length) nodes.push(text.slice(last))
  return <>{nodes}</>
}

const CALLOUT_LABEL: Record<string, string> = {
  tip: 'Tip', warning: 'Watch out', exam: 'Exam alert', key: 'Key point',
}

function PBlock({ block }: { block: Block }) {
  switch (block.type) {
    case 'p':
      return <p className="pd-p"><PInline text={block.text} /></p>

    case 'h3':
      return <h3 className="pd-h3">{block.text}</h3>

    case 'def':
      return (
        <div className="pd-def">
          <span className="pd-eyebrow" style={{ color: 'var(--pd-acc)' }}>Definition</span>
          <p className="pd-def-term">{block.term}</p>
          <p className="pd-def-text"><PInline text={block.text} /></p>
        </div>
      )

    case 'eq':
      return (
        <div className="pd-eq">
          <p className="pd-eq-code">{block.code}</p>
          {block.caption && <p className="pd-eq-cap">{block.caption}</p>}
        </div>
      )

    case 'list':
      return (
        <ul className="pd-list">
          {block.items.map((it, i) => (
            <li className="pd-li" key={i}>
              {block.ordered
                ? <span className="pd-li-num">{i + 1}.</span>
                : <span className="pd-li-mark" />}
              <span className="pd-li-text"><PInline text={it} /></span>
            </li>
          ))}
        </ul>
      )

    case 'callout': {
      const exam = block.variant === 'exam'
      return (
        <div className={`pd-callout${exam ? ' exam' : ''}`}>
          <span className="pd-callout-label">{CALLOUT_LABEL[block.variant] ?? 'Tip'}</span>
          <p className="pd-callout-title">{block.title}</p>
          <p className="pd-callout-text"><PInline text={block.text} /></p>
        </div>
      )
    }

    case 'worked':
      return (
        <div className="pd-worked">
          <div className="pd-worked-head">
            <span className="pd-worked-label">Worked example</span>
            <span className="pd-worked-title">{block.title}</span>
          </div>
          <div className="pd-worked-body">
            <div className="pd-worked-problem">
              <span className="pd-eyebrow">Problem</span>
              <p><PInline text={block.problem} /></p>
            </div>
            <div style={{ marginTop: '7pt' }}>
              {block.steps.map((s, i) => (
                <div className="pd-step" key={i}>
                  <span className="pd-step-n">{i + 1}</span>
                  <span className="pd-step-text"><PInline text={s} /></span>
                </div>
              ))}
            </div>
            <div className="pd-answer">
              <span className="pd-answer-k">Answer</span>
              <span className="pd-answer-v"><PInline text={block.answer} /></span>
            </div>
          </div>
        </div>
      )

    case 'table':
      return (
        <table className="pd-table">
          <thead>
            <tr>{block.headers.map((h, i) => <th key={i}>{h}</th>)}</tr>
          </thead>
          <tbody>
            {block.rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => <td key={j}><PInline text={cell} /></td>)}
              </tr>
            ))}
          </tbody>
        </table>
      )

    case 'figure':
      return (
        <figure className="pd-fig">
          {/* block.src is the light variant — right choice for paper */}
          <img src={block.src} alt={block.alt} />
          <figcaption className="pd-fig-cap">{block.caption ?? block.alt}</figcaption>
        </figure>
      )

    default:
      return null
  }
}

function PSection({ s }: { s: SectionData }) {
  return (
    <section className="pd-sec">
      <div className="pd-sec-head">
        <div className="pd-sec-chips">
          {s.spec && <span className="pd-chip-spec">SPEC {s.spec}</span>}
          <span className="pd-chip-min">≈ {s.estMinutes} MIN</span>
        </div>
        <h2 className="pd-sec-title">{s.title}</h2>
        {s.specText && (
          <div className="pd-statement">
            <span className="pd-eyebrow">The specification says</span>
            <p>{s.specText}</p>
          </div>
        )}
        {s.blurb && <p className="pd-blurb">{s.blurb}</p>}
      </div>

      {s.content
        ? s.content
            // the verbatim statement already leads the section in print —
            // drop a first paragraph that merely repeats it
            .filter((b, i) => !(i === 0 && b.type === 'p' && s.specText && b.text.trim() === s.specText.trim()))
            .map((b, i) => <PBlock key={i} block={b} />)
        : (
          <>
            {s.outline.length > 0 && (
              <ul className="pd-outline">
                {s.outline.map((o, i) => (
                  <li className="pd-li" key={i}>
                    <span className="pd-li-mark" />
                    <span className="pd-li-text"><PInline text={o} /></span>
                  </li>
                ))}
              </ul>
            )}
            <p className="pd-wip-note">Full notes for this section are being written — read and test yourself on the site.</p>
          </>
        )}
    </section>
  )
}

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

export function PrintDoc({ topic, topics }: { topic: TopicData; topics: TopicData[] }) {
  const nn = String(topic.number).padStart(2, '0')
  const specCount = topic.sections.filter((s) => s.spec).length
  const now = new Date()
  const generated = `${MONTHS[now.getMonth()]} ${now.getFullYear()}`

  return (
    <div className="pd-doc" lang="en">
      <style dangerouslySetInnerHTML={{ __html: PD_CSS }} />

      {/* ── cover ─────────────────────────────────────────── */}
      <div className="pd-cover">
        <div className="pd-brandbar">
          <span className="pd-brand">IAL CHEM<em>{'//'}</em>DECODED</span>
          <span className="pd-eyebrow" style={{ color: 'var(--pd-acc)' }}>Print edition</span>
        </div>

        <p className="pd-cover-eyebrow">
          Pearson Edexcel International A Level · Chemistry · {topic.unitCode}
        </p>
        <div className="pd-ghost" aria-hidden>{nn}</div>
        <h1 className="pd-cover-title">{topic.title}</h1>
        <div className="pd-cover-bar" aria-hidden />
        <p className="pd-cover-sub">{topic.subtitle}</p>
        <p className="pd-cover-summary">{topic.summary}</p>

        <div className="pd-meta">
          <div className="pd-meta-cell">
            <p className="pd-meta-k">Unit</p>
            <p className="pd-meta-v">{topic.unit} <small>· {topic.unitCode}</small></p>
          </div>
          <div className="pd-meta-cell">
            <p className="pd-meta-k">Sections</p>
            <p className="pd-meta-v">{topic.sections.length}</p>
          </div>
          <div className="pd-meta-cell">
            <p className="pd-meta-k">Study time</p>
            <p className="pd-meta-v">~{topic.estHours} <small>h</small></p>
          </div>
          <div className="pd-meta-cell">
            <p className="pd-meta-k">Flashcards</p>
            <p className="pd-meta-v">{topic.cards.length}</p>
          </div>
        </div>
        <p className="pd-cover-note">
          Covers <b>{specCount} specification points</b> — statements quoted verbatim from the specification
        </p>

        <div className="pd-cover-foot">
          <span>
            Compiled from the Pearson Edexcel International A Level Chemistry (2018) specification.
            Independent study tool — not affiliated with or endorsed by Pearson Edexcel.
          </span>
          <span className="r">Generated {generated}</span>
        </div>
      </div>

      {/* ── contents ──────────────────────────────────────── */}
      <div className="pd-toc">
        <p className="pd-eyebrow">Topic {nn} · {topic.unitName}</p>
        <h2 className="pd-toc-title">Contents</h2>
        <div className="pd-toc-list">
          {topic.sections.map((s) => (
            <div className="pd-toc-row" key={s.sectionKey}>
              <span className="pd-toc-no">{s.number}</span>
              <span className="pd-toc-name">{s.title}</span>
              <span className="pd-toc-dots" aria-hidden />
              {!s.content && <span className="pd-toc-wip">Notes in progress</span>}
              {s.spec && <span className="pd-toc-spec">SPEC {s.spec}</span>}
              <span className="pd-toc-min">{s.estMinutes} min</span>
            </div>
          ))}
        </div>
        <div className="pd-howto">
          <span className="pd-eyebrow">How to use this document</span>
          <p>
            Every section opens with the specification statement, worded exactly as Edexcel words it —
            that is what the examiner marks against. Definitions, equations and exam alerts are boxed;
            worked examples walk the full method step by step. Read a section, shut the page and
            recall its bullets from memory, then grind the topic&rsquo;s flashcard deck on the site.
          </p>
        </div>
      </div>

      {/* ── sections ──────────────────────────────────────── */}
      {topic.sections.map((s) => <PSection key={s.sectionKey} s={s} />)}

      {/* ── end matter ────────────────────────────────────── */}
      <div className="pd-end">
        <p className="pd-end-k">END OF TOPIC {nn}</p>
        <div className="pd-end-next">
          {topics.filter((t) => t.slug !== topic.slug).map((t) => (
            <span className="pd-end-chip" key={t.slug}>
              {String(t.number).padStart(2, '0')} · {t.title}
            </span>
          ))}
        </div>
        <p className="pd-end-disc">
          IAL CHEM//DECODED — flashcards, progress tracking and the interactive version of these notes live on the site.
          Not affiliated with or endorsed by Pearson Edexcel.
        </p>
      </div>
    </div>
  )
}
