'use client'

import { useEffect, useRef } from 'react'
import * as THREE from 'three'

/* ============================================================
   ATOM SCENE — a live Carbon-12 model.
   6 protons + 6 neutrons packed into a breathing nucleus,
   6 electrons riding two tilted shells (2 + 4), glow sprites
   for light without postprocessing.

   Interaction: drag to spin (pointer + touch), inertia on
   release, slow auto-rotation when idle. Electrons follow the
   Control Room accent live.

   Performance doctrine (must not crash phones):
   - raw three, ~22 low-poly meshes, no shadows, no postprocessing
   - devicePixelRatio capped (1.75 mobile / 2 desktop)
   - the render loop STOPS when the tab is hidden or the stage
     scrolls out of view (IntersectionObserver)
   - reduced motion → one static frame, drag re-renders on demand
   - full dispose on unmount
   ============================================================ */

export interface AtomCanvasProps {
  accent: string
  dark: boolean
  motion: 'normal' | 'reduced'
}

const PROTON_HEX = '#e8532f'
const NUCLEON_GEO_SEGMENTS = [22, 14] as const
const ELECTRON_SEGMENTS = [12, 9] as const
const SHELL_A_R = 2.28
const SHELL_B_R = 3.42
const ELECTRON_R = 0.088
const DRAG_ROT = 0.0042
const PITCH_LIMIT = 1.25

/* 12 nucleon anchors: the vertices of an icosahedron, slightly
   squashed — an even, natural packing for 6 + 6 */
const PHI = (1 + Math.sqrt(5)) / 2
const NUCLEON_ANCHORS: [number, number, number][] = (() => {
  const raw: [number, number, number][] = []
  for (const s1 of [-1, 1]) for (const s2 of [-1, 1]) {
    raw.push([0, s1, s2 * PHI], [s1, s2 * PHI, 0], [s2 * PHI, 0, s1])
  }
  return raw.map(([x, y, z]) => {
    const l = Math.hypot(x, y, z)
    const j = 1 + (((Math.abs(x * 31 + y * 17 + z * 7) * 13) % 10) - 5) / 100
    return [(x / l) * 0.56 * j, (y / l) * 0.56 * j, (z / l) * 0.5 * j] as [number, number, number]
  })
})()

function makeGlowTexture(): THREE.Texture {
  const c = document.createElement('canvas')
  c.width = c.height = 128
  const g = c.getContext('2d')!
  const grad = g.createRadialGradient(64, 64, 2, 64, 64, 62)
  grad.addColorStop(0, 'rgba(255,255,255,1)')
  grad.addColorStop(0.25, 'rgba(255,255,255,0.55)')
  grad.addColorStop(0.6, 'rgba(255,255,255,0.12)')
  grad.addColorStop(1, 'rgba(255,255,255,0)')
  g.fillStyle = grad
  g.fillRect(0, 0, 128, 128)
  const tex = new THREE.CanvasTexture(c)
  tex.colorSpace = THREE.SRGBColorSpace
  return tex
}

export default function AtomCanvas({ accent, dark, motion }: AtomCanvasProps) {
  const hostRef = useRef<HTMLDivElement>(null)

  /* If WebGL is unavailable the canvas simply never mounts and the
     static SVG fallback (rendered behind us by the hero) stays visible. */

  /* live props land in a ref so the one-time init never goes stale
     (kept fresh by an effect; the scene polls it at 350 ms) */
  const propsRef = useRef({ accent, dark, motion })
  useEffect(() => {
    propsRef.current = { accent, dark, motion }
  })

  useEffect(() => {
    const host = hostRef.current
    if (!host) return

    let renderer: THREE.WebGLRenderer
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      })
    } catch {
      return
    }

    const { accent: a0, dark: d0 } = propsRef.current
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 60)
    camera.position.set(0, 0, 11.2)

    /* ---------- renderer ---------- */
    renderer.setClearColor(0x000000, 0)
    const canvas = renderer.domElement
    canvas.className = 'atom-canvas'
    canvas.setAttribute('aria-hidden', 'true')
    host.appendChild(canvas)

    /* ---------- lights ---------- */
    const ambient = new THREE.AmbientLight(0xffffff, d0 ? 1.15 : 1.45)
    const key = new THREE.DirectionalLight(0xffffff, 2.5)
    key.position.set(5, 7, 9)
    const accentLight = new THREE.DirectionalLight(new THREE.Color(a0), d0 ? 1.15 : 0.7)
    accentLight.position.set(-6, -2, -4)
    scene.add(ambient, key, accentLight)

    /* ---------- shared resources ---------- */
    const glowTex = makeGlowTexture()
    const nucleonGeo = new THREE.SphereGeometry(0.42, ...NUCLEON_GEO_SEGMENTS)
    const protonMat = new THREE.MeshStandardMaterial({ color: PROTON_HEX, roughness: 0.34, metalness: 0.08 })
    const neutronMat = new THREE.MeshStandardMaterial({ color: d0 ? '#a9b0bc' : '#848b96', roughness: 0.42, metalness: 0.05 })
    const electronGeo = new THREE.SphereGeometry(ELECTRON_R, ...ELECTRON_SEGMENTS)
    const electronMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(a0) })
    const electronGlowMat = new THREE.SpriteMaterial({
      map: glowTex, color: new THREE.Color(a0), transparent: true,
      opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending,
    })
    const ringMat = new THREE.MeshBasicMaterial({
      color: d0 ? '#ffffff' : '#101828', transparent: true, opacity: d0 ? 0.2 : 0.13,
    })
    const nucleusGlowMat = new THREE.SpriteMaterial({
      map: glowTex, color: new THREE.Color(a0), transparent: true,
      opacity: d0 ? 0.3 : 0.16, depthWrite: false, blending: d0 ? THREE.AdditiveBlending : THREE.NormalBlending,
    })

    /* ---------- atom graph ---------- */
    const atom = new THREE.Group()
    scene.add(atom)

    const nucleus = new THREE.Group()
    atom.add(nucleus)

    const nucleons: { mesh: THREE.Mesh; base: THREE.Vector3; ph: number }[] = []
    NUCLEON_ANCHORS.forEach((p, i) => {
      const mesh = new THREE.Mesh(nucleonGeo, i % 2 === 0 ? protonMat : neutronMat)
      mesh.position.set(...p)
      nucleons.push({ mesh, base: mesh.position.clone(), ph: i * 2.399963 })
      nucleus.add(mesh)
    })

    const nucleusGlow = new THREE.Sprite(nucleusGlowMat)
    nucleusGlow.scale.setScalar(3.1)
    nucleus.add(nucleusGlow)

    interface Shell { group: THREE.Group; radius: number; speed: number; electrons: { pivot: THREE.Object3D; glow: THREE.Sprite; off: number; wob: number }[] }
    const shells: Shell[] = []

    function buildShell(radius: number, tiltX: number, tiltY: number, tiltZ: number, count: number, speed: number): Shell {
      const group = new THREE.Group()
      group.rotation.set(tiltX, tiltY, tiltZ)
      const ring = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.014, 6, 140), ringMat)
      group.add(ring)
      const electrons: Shell['electrons'] = []
      for (let i = 0; i < count; i++) {
        const pivot = new THREE.Group()
        const core = new THREE.Mesh(electronGeo, electronMat)
        const glow = new THREE.Sprite(electronGlowMat)
        glow.scale.setScalar(0.62)
        pivot.add(core, glow)
        group.add(pivot)
        electrons.push({ pivot, glow, off: (i / count) * Math.PI * 2, wob: i * 1.7 })
      }
      atom.add(group)
      shells.push({ group, radius, speed, electrons })
      return { group, radius, speed, electrons }
    }

    buildShell(SHELL_A_R, 1.22, 0.38, 0.1, 2, 1.05)
    buildShell(SHELL_B_R, 0.42, -0.52, 0.24, 4, 0.6)

    /* ---------- palette (live) ---------- */
    function applyPalette(accent: string, dark: boolean) {
      const c = new THREE.Color(accent)
      electronMat.color.copy(c)
      electronGlowMat.color.copy(c)
      nucleusGlowMat.color.copy(c)
      accentLight.color.copy(c)
      nucleusGlowMat.blending = dark ? THREE.AdditiveBlending : THREE.NormalBlending
      nucleusGlowMat.opacity = dark ? 0.3 : 0.15
      nucleusGlowMat.needsUpdate = true
      ringMat.color.set(dark ? '#ffffff' : '#101828')
      ringMat.opacity = dark ? 0.2 : 0.13
      neutronMat.color.set(dark ? '#a9b0bc' : '#848b96')
      ambient.intensity = dark ? 1.15 : 1.45
      accentLight.intensity = dark ? 1.15 : 0.7
    }
    applyPalette(a0, d0)

    /* ---------- interaction state ---------- */
    let yaw = 0.35
    let pitch = 0.22
    let velX = 0        // rad/s around Y
    let velY = 0        // rad/s around X
    let dragging = false
    let lastX = 0
    let lastY = 0
    let lastMoveT = 0
    let lastDragAt = 0
    let idleW = 0

    const onDown = (e: PointerEvent) => {
      dragging = true
      lastX = e.clientX
      lastY = e.clientY
      lastMoveT = performance.now()
      velX = velY = 0
      canvas.setPointerCapture?.(e.pointerId)
      canvas.classList.add('is-grabbing')
    }
    const onMove = (e: PointerEvent) => {
      if (!dragging) return
      const now = performance.now()
      const dtm = Math.max(8, now - lastMoveT) / 1000
      const dx = e.clientX - lastX
      const dy = e.clientY - lastY
      lastX = e.clientX
      lastY = e.clientY
      lastMoveT = now
      lastDragAt = now
      yaw += dx * DRAG_ROT
      pitch = Math.max(-PITCH_LIMIT, Math.min(PITCH_LIMIT, pitch + dy * DRAG_ROT))
      velX = (dx * DRAG_ROT) / dtm
      velY = (dy * DRAG_ROT) / dtm
      if (propsRef.current.motion === 'reduced') renderOnce()
    }
    const onUp = (e: PointerEvent) => {
      dragging = false
      lastDragAt = performance.now()
      canvas.classList.remove('is-grabbing')
      try { canvas.releasePointerCapture?.(e.pointerId) } catch { /* released */ }
      // calm flicks: tiny velocities just stop
      if (Math.abs(velX) < 0.02) velX = 0
      if (Math.abs(velY) < 0.02) velY = 0
    }
    canvas.addEventListener('pointerdown', onDown)
    canvas.addEventListener('pointermove', onMove)
    canvas.addEventListener('pointerup', onUp)
    canvas.addEventListener('pointercancel', onUp)

    /* ---------- sizing ---------- */
    let W = 1
    let H = 1
    const applySize = () => {
      W = Math.max(1, host.clientWidth)
      H = Math.max(1, host.clientHeight)
      const aspect = W / H
      camera.aspect = aspect
      camera.position.z = aspect < 1.05 ? 12.6 : 11.2
      // wide hero: atom sits right of the headline; narrow: centred
      atom.position.x = aspect > 1.7 ? 2.35 : aspect > 1.05 ? 1.65 : 0
      camera.updateProjectionMatrix()
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, W < 768 ? 1.75 : 2))
      renderer.setSize(W, H, false)
    }
    applySize()
    const ro = new ResizeObserver(applySize)
    ro.observe(host)

    /* ---------- render gating ---------- */
    let inView = true
    let raf = 0
    let last = 0
    let disposed = false

    const media = window.matchMedia('(prefers-reduced-motion: reduce)')

    function motionReduced(): boolean {
      return propsRef.current.motion === 'reduced' || media.matches
    }

    function tick(now: number) {
      if (disposed) return
      raf = 0
      if (document.hidden || !inView || motionReduced()) return
      const dt = Math.min(0.05, last ? (now - last) / 1000 : 0.016)
      last = now

      // spin physics
      if (!dragging) {
        yaw += velX * dt
        pitch = Math.max(-PITCH_LIMIT, Math.min(PITCH_LIMIT, pitch + velY * dt))
        const damp = Math.exp(-dt * 3.1)
        velX *= damp
        velY *= damp
        // idle → gentle auto-rotation eases in
        const idle = now - lastDragAt > 2200
        idleW = idle ? Math.min(1, idleW + dt / 1.4) : 0
        yaw += 0.12 * idleW * dt
      } else {
        idleW = 0
      }
      atom.rotation.set(pitch, yaw, 0)

      // live nucleus: breathing + nucleon wiggle
      const t = now / 1000
      nucleus.scale.setScalar(1 + Math.sin(t * 1.25) * 0.022)
      for (const n of nucleons) {
        n.mesh.position.set(
          n.base.x + Math.sin(t * 2.2 + n.ph) * 0.024,
          n.base.y + Math.sin(t * 1.9 + n.ph * 1.7) * 0.024,
          n.base.z + Math.sin(t * 2.6 + n.ph * 0.6) * 0.022
        )
      }
      nucleusGlow.scale.setScalar(3.1 + Math.sin(t * 1.25) * 0.14)

      // electrons
      for (const s of shells) {
        for (const e of s.electrons) {
          const a = t * s.speed + e.off
          e.pivot.position.set(Math.cos(a) * s.radius, Math.sin(a) * s.radius, 0)
          e.glow.scale.setScalar(0.62 + Math.sin(t * 3 + e.wob) * 0.09)
        }
      }

      renderer.render(scene, camera)
      raf = requestAnimationFrame(tick)
    }

    function startLoop() {
      if (disposed || raf || document.hidden || !inView || motionReduced()) return
      last = 0
      raf = requestAnimationFrame(tick)
    }
    function stopLoop() {
      if (raf) cancelAnimationFrame(raf)
      raf = 0
    }
    function renderOnce() {
      if (disposed) return
      atom.rotation.set(pitch, yaw, 0)
      renderer.render(scene, camera)
    }

    const onVis = () => {
      if (document.hidden) stopLoop()
      else startLoop()
    }
    const onMedia = () => {
      if (motionReduced()) { stopLoop(); renderOnce() } else startLoop()
    }
    document.addEventListener('visibilitychange', onVis)
    media.addEventListener?.('change', onMedia)

    const io = new IntersectionObserver(
      (entries) => {
        inView = entries[0]?.isIntersecting ?? true
        if (inView) startLoop()
        else stopLoop()
      },
      { threshold: 0.02 }
    )
    io.observe(host)

    /* ---------- first paint ---------- */
    applySize()
    renderOnce()
    if (!motionReduced()) startLoop()

    /* ---------- palette / motion reactions ---------- */
    const sync = { accent: a0, dark: d0, motion: propsRef.current.motion }
    const palTimer = window.setInterval(() => {
      const p = propsRef.current
      if (p.accent !== sync.accent || p.dark !== sync.dark) {
        sync.accent = p.accent
        sync.dark = p.dark
        applyPalette(p.accent, p.dark)
        if (motionReduced()) renderOnce()
      }
      if (p.motion !== sync.motion) {
        sync.motion = p.motion
        if (motionReduced()) { stopLoop(); renderOnce() }
        else startLoop()
      }
    }, 350)

    /* ---------- dispose ---------- */
    return () => {
      disposed = true
      stopLoop()
      window.clearInterval(palTimer)
      ro.disconnect()
      io.disconnect()
      document.removeEventListener('visibilitychange', onVis)
      media.removeEventListener?.('change', onMedia)
      canvas.removeEventListener('pointerdown', onDown)
      canvas.removeEventListener('pointermove', onMove)
      canvas.removeEventListener('pointerup', onUp)
      canvas.removeEventListener('pointercancel', onUp)
      scene.traverse((obj) => {
        const any = obj as THREE.Mesh
        if (any.geometry) any.geometry.dispose()
        const m = (any as THREE.Mesh).material as THREE.Material | THREE.Material[] | undefined
        if (Array.isArray(m)) m.forEach((x) => x.dispose())
        else m?.dispose()
      })
      glowTex.dispose()
      renderer.dispose()
      canvas.remove()
    }
  }, [])

  return (
    <div ref={hostRef} className="absolute inset-0" aria-hidden />
  )
}
