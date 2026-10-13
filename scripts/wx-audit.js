// Audit: replicate the blocks.tsx worked-example classifier over all
// content.json steps and dump per-line classifications for review.
const data = require('/home/z/my-project/src/lib/site/content.json')

const WX_ARROW = /→|⇌|⇒/
function wxIsEq(l) {
  if (WX_ARROW.test(l)) return true
  if (!l.includes('=')) return false
  if (l.length <= 78 && !/[.!?]['")\]]?$/.test(l)) return true
  if (/[÷×√]/.test(l)) return true
  if (/\d\s*[+−]\s*[(\d−]/.test(l)) return true
  const s = l.replace(/\s/g, '')
  const mathy = (s.match(/[\d+=÷×−√().,°]/g) ?? []).length
  return s.length > 0 && mathy / s.length >= 0.45
}
function wxSplitLead(line) {
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
function wxSplitMulti(line) {
  if (!line.includes(';')) return null
  const parts = line.split(';').map((p) => p.trim()).filter(Boolean)
  if (parts.length < 2 || parts.length > 3) return null
  if (parts.some((p) => !p.includes('=') || p.length > 64)) return null
  return parts.map((p, i) => (i < parts.length - 1 ? p + ';' : p))
}

const topics = Array.isArray(data) ? data : data.topics
let eq = 0, lead = 0, li = 0, p = 0
const proseWithEquals = []
const oddChips = []
for (const t of topics) {
  for (const s of t.sections ?? []) {
    for (const b of s.content ?? []) {
      if (b.type !== 'worked') continue
      for (const step of b.steps) {
        for (const raw of step.split('\n')) {
          const line = raw.trim()
          if (!line) continue
          if (/^[-•*]\s+/.test(line)) { li++; continue }
          const l = wxSplitLead(line)
          if (l && wxIsEq(l.rest)) { lead++; continue }
          if (wxIsEq(line)) {
            eq++
            const multi = wxSplitMulti(line)
            if (multi) multi.forEach(m => oddChips.push([t.slug, m]))
            else if (line.length > 90) oddChips.push([t.slug, '(long chip) ' + line.slice(0, 90)])
            continue
          }
          p++
          if (line.includes('=')) proseWithEquals.push([t.slug, line])
        }
      }
    }
  }
}
console.log(`chips: ${eq}, lead-labelled: ${lead}, bullets: ${li}, prose: ${p}`)
console.log(`\n--- prose lines that still contain '=' (${proseWithEquals.length}) ---`)
for (const [slug, l] of proseWithEquals) console.log(`[${slug}] ${l.slice(0, 118)}`)
console.log(`\n--- long/multi chips (${oddChips.length}) ---`)
for (const [slug, l] of oddChips.slice(0, 20)) console.log(`[${slug}] ${l}`)
