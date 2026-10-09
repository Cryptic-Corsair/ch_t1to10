import React from 'react'

/* ============================================================
   DOODLES — a hand-drawn chemistry margin, inked in SVG.
   Every doodle is stroke-only (currentColor), round-capped and
   deliberately a little wobbly, like the sketches in a student's
   notebook. Fields are scatter layers: deterministic positions
   (no Math.random → no hydration drift), tiny opacity, a few
   gently floating. Pure SVG + compositor transforms only.
   ============================================================ */

type D = { key: string; svg: React.ReactNode }

const S = { fill: 'none', stroke: 'currentColor', strokeWidth: 2.6, strokeLinecap: 'round', strokeLinejoin: 'round' } as const

/* pointy-top hexagon path — used by the ring doodles */
function hexPath(cx: number, cy: number, r: number): string {
  const pts = Array.from({ length: 6 }, (_, i) => {
    const a = (Math.PI / 180) * (i * 60 + 30)
    return `${(cx + r * Math.cos(a)).toFixed(1)} ${(cy + r * Math.sin(a)).toFixed(1)}`
  })
  return 'M' + pts.join(' L') + ' Z'
}

export const DOODLES: Record<string, D> = {
  /* Erlenmeyer flask, bubbling */
  flask: {
    key: 'flask',
    svg: (
      <g {...S}>
        <path d="M40 12 L40 33 M56 12 L56 33 M36 12 H60" />
        <path d="M40 33 L23 72 Q21 78 28 78 H68 Q75 78 73 72 L56 33" />
        <path d="M31 60 Q38 56.5 45 60 T59 60 T66 60" />
        <circle cx="45" cy="49" r="2.6" />
        <circle cx="53" cy="42" r="1.8" />
        <circle cx="47.5" cy="35.5" r="1.3" />
      </g>
    ),
  },
  /* beaker with graduations */
  beaker: {
    key: 'beaker',
    svg: (
      <g {...S}>
        <path d="M29 14 V69 Q29 78 38 78 H58 Q67 78 67 69 V14" />
        <path d="M24 14 H34 M62 14 H72" />
        <path d="M38 32 H48 M38 45 H52 M38 58 H45" />
        <path d="M29 61 Q35 57.5 41 61 T53 61 T65 61" />
      </g>
    ),
  },
  /* tilted test tube, dripping */
  testtube: {
    key: 'testtube',
    svg: (
      <g {...S}>
        <g transform="rotate(-26 50 44)">
          <path d="M40 13 V61 Q40 72 50 72 Q60 72 60 61 V13" />
          <path d="M36 13 H64" />
          <path d="M40 46 Q45 43 50 46 T60 46" />
          <circle cx="50" cy="57" r="2" />
          <circle cx="54.5" cy="51" r="1.4" />
        </g>
        <path d="M73 66 Q70.5 70.5 73 72.5 Q75.5 70.5 73 66 Z" />
        <path d="M67 80 Q73 77 79 80" />
      </g>
    ),
  },
  /* benzene ring, aromatic */
  benzene: {
    key: 'benzene',
    svg: (
      <g {...S}>
        <path d={hexPath(48, 50, 26)} />
        <circle cx="48" cy="50" r="13.5" />
      </g>
    ),
  },
  /* fused rings (naphthalene-ish) */
  hexchain: {
    key: 'hexchain',
    svg: (
      <g {...S}>
        <path d={hexPath(32.5, 48, 20)} />
        <path d={hexPath(66.5, 48, 20)} />
        <circle cx="32.5" cy="48" r="7.5" />
      </g>
    ),
  },
  /* three atoms bonded */
  molecule: {
    key: 'molecule',
    svg: (
      <g {...S}>
        <circle cx="24" cy="62" r="9" />
        <circle cx="51" cy="38" r="7" />
        <circle cx="76" cy="58" r="10" />
        <path d="M31 56 L45 43 M58 42 L67 51" />
        <circle cx="88" cy="33" r="4.5" />
        <path d="M83 50 L86.5 39" />
      </g>
    ),
  },
  /* water, 104.5° */
  water: {
    key: 'water',
    svg: (
      <g {...S}>
        <circle cx="39" cy="51" r="13" />
        <path d="M50 45 L60 33 M50 57 L60 69" />
        <circle cx="66" cy="28" r="6" />
        <circle cx="66" cy="74" r="6" />
      </g>
    ),
  },
  /* crossed orbits + nucleus — a small echo of the hero atom */
  orbits: {
    key: 'orbits',
    svg: (
      <g {...S}>
        <ellipse cx="48" cy="48" rx="31" ry="12.5" transform="rotate(26 48 48)" />
        <ellipse cx="48" cy="48" rx="31" ry="12.5" transform="rotate(-26 48 48)" />
        <circle cx="48" cy="48" r="3.6" fill="currentColor" stroke="none" />
        <circle cx="72" cy="33" r="2.6" fill="currentColor" stroke="none" />
        <circle cx="25" cy="63" r="2.6" fill="currentColor" stroke="none" />
      </g>
    ),
  },
  /* droplet */
  droplet: {
    key: 'droplet',
    svg: (
      <g {...S}>
        <path d="M48 15 C42 30 30 44 30 58 A18 18 0 0 0 66 58 C66 44 54 30 48 15 Z" />
        <path d="M39 52 Q37.5 60 43 65.5" />
      </g>
    ),
  },
  /* bubbles */
  bubbles: {
    key: 'bubbles',
    svg: (
      <g {...S}>
        <circle cx="35" cy="59" r="12.5" />
        <circle cx="58" cy="41" r="9" />
        <circle cx="67" cy="64" r="6" />
        <circle cx="47" cy="24" r="4.5" />
        <path d="M24 25 V35 M19 30 H29" />
      </g>
    ),
  },
  /* thermometer */
  thermometer: {
    key: 'thermometer',
    svg: (
      <g {...S}>
        <path d="M43 15 Q43 10 48 10 Q53 10 53 15 V57" />
        <circle cx="48" cy="67" r="10.5" />
        <path d="M48 26 V59" />
        <path d="M57 28 H63 M57 41 H63" />
      </g>
    ),
  },
  /* pipette dropping */
  pipette: {
    key: 'pipette',
    svg: (
      <g {...S}>
        <path d="M39 17 Q48 8 57 17" />
        <path d="M41 17 V40 Q41 46 48 58 Q55 46 55 40 V17" />
        <path d="M48 66 Q45.5 70.5 48 73 Q50.5 70.5 48 66 Z" />
        <path d="M41 81 Q48 78 55 81" />
      </g>
    ),
  },
  /* bunsen burner + flame */
  burner: {
    key: 'burner',
    svg: (
      <g {...S}>
        <path d="M42 33 H54 L51.5 53 H44.5 Z" />
        <path d="M37 78 L41.5 61 H54.5 L59 78" />
        <path d="M30 78 H66" />
        <circle cx="48" cy="57.5" r="2" />
        <path d="M48 9 Q41.5 19 43.5 27 Q45 32 48 32 Q51 32 52.5 27 Q54.5 19 48 9 Z" />
      </g>
    ),
  },
  /* periodic-table cell */
  cell: {
    key: 'cell',
    svg: (
      <g {...S}>
        <rect x="25" y="20" width="46" height="56" rx="5" />
        <path d="M32 31 H41" />
        <path d="M33 49 Q39 43 45 49 T57 49" />
        <circle cx="36" cy="64" r="1.7" fill="currentColor" stroke="none" />
        <circle cx="44" cy="64" r="1.7" fill="currentColor" stroke="none" />
      </g>
    ),
  },
  /* reaction arrow with delta */
  reaction: {
    key: 'reaction',
    svg: (
      <g {...S}>
        <path d="M16 50 H70 M62 42 L72 50 L62 58" />
        <path d="M42 20 L49 32 H35 Z" />
      </g>
    ),
  },
  /* four-point sparkle */
  sparkle: {
    key: 'sparkle',
    svg: (
      <g {...S}>
        <path d="M48 28 L52.5 43.5 L68 48 L52.5 52.5 L48 68 L43.5 52.5 L28 48 L43.5 43.5 Z" />
      </g>
    ),
  },
}

/* ---------- scatter items ---------- */

export interface DoodleSpec {
  d: keyof typeof DOODLES
  x: number // % left
  y: number // % top
  s: number // px size
  r?: number // rotation deg
  acc?: boolean
  float?: boolean
  dur?: number // float seconds
  delay?: number
  op?: number // opacity override
}

export const HERO_DOODLES: DoodleSpec[] = [
  { d: 'flask', x: 7, y: 16, s: 92, r: -8, float: true, dur: 11 },
  { d: 'benzene', x: 89, y: 9, s: 78, r: 12, float: true, dur: 13, delay: -4 },
  { d: 'orbits', x: 4.5, y: 64, s: 76, r: -6, float: true, dur: 12, delay: -7 },
  { d: 'droplet', x: 95.5, y: 44, s: 44, r: 9 },
  { d: 'testtube', x: 13, y: 37, s: 62, r: 4 },
  { d: 'water', x: 71, y: 10, s: 60, r: -10 },
  { d: 'bubbles', x: 80, y: 78, s: 66, acc: true, float: true, dur: 10, delay: -2 },
  { d: 'sparkle', x: 31, y: 87, s: 24, r: 12, acc: true, op: 0.5 },
  { d: 'thermometer', x: 60, y: 84, s: 56, r: 7, float: true, dur: 14, delay: -9 },
  { d: 'reaction', x: 87, y: 27, s: 58, r: -5 },
  { d: 'beaker', x: 43, y: 7, s: 54, r: 3 },
  { d: 'molecule', x: 22, y: 72, s: 58, r: -7 },
]

export const TOPIC_DOODLES: DoodleSpec[] = [
  { d: 'benzene', x: 93, y: 3, s: 72, r: 9 },
  { d: 'hexchain', x: 3.5, y: 12, s: 92, r: -6, float: true, dur: 13 },
  { d: 'flask', x: 91, y: 33, s: 78, r: 10, float: true, dur: 11, delay: -5 },
  { d: 'orbits', x: 5, y: 47, s: 66, r: 4, float: true, dur: 12, delay: -3 },
  { d: 'beaker', x: 7, y: 80, s: 74, r: -8 },
  { d: 'bubbles', x: 89, y: 62, s: 56, acc: true, float: true, dur: 10, delay: -6 },
  { d: 'pipette', x: 71, y: 92, s: 60, r: 8, float: true, dur: 12, delay: -8 },
  { d: 'cell', x: 24, y: 95, s: 54, r: 5 },
  { d: 'droplet', x: 47, y: 99, s: 40, r: -6 },
  { d: 'sparkle', x: 55, y: 2.5, s: 22, r: 14, acc: true, op: 0.5 },
  { d: 'molecule', x: 96, y: 82, s: 60, r: -9 },
]

/* ---------- components ---------- */

export function Doodle({ spec }: { spec: DoodleSpec }) {
  const item = DOODLES[spec.d]
  if (!item) return null
  const style: React.CSSProperties & Record<string, string | number> = {
    left: `${spec.x}%`,
    top: `${spec.y}%`,
    width: spec.s,
    height: spec.s,
    transform: `translate(-50%, -50%) rotate(${spec.r ?? 0}deg)`,
    ...(spec.op != null ? { opacity: spec.op } : null),
    ...(spec.float ? { '--dd': `${spec.dur ?? 12}s`, '--ddl': `${spec.delay ?? 0}s` } : null),
  }
  return (
    <svg
      viewBox="0 0 96 96"
      className={`doodle${spec.acc ? ' doodle-acc' : ''}${spec.float ? ' doodle-float' : ''}`}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      {item.svg}
    </svg>
  )
}

/* A scatter layer — sized to its positioned parent, prints nothing. */
export function DoodleField({ items, className = '' }: { items: DoodleSpec[]; className?: string }) {
  return (
    <div className={`doodle-field ${className}`} aria-hidden>
      {items.map((it, i) => (
        <Doodle key={`${it.d}-${i}`} spec={it} />
      ))}
    </div>
  )
}
