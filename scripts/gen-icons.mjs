// Generates the favicon / PWA icon set for IAL Chem.
// The mark is the Erlenmeyer flask used by FlaskMark in
// src/components/site/chrome.tsx (same geometry, scaled into a 30-box):
// white flask outline + coral (#F5654A, the default accent) liquid/bubbles
// on the dark rounded-square tile.
// - "mark" style: rounded square + white stroke, transparent corners
//   (favicon fallbacks + manifest "any" icons)
// - "bleed" style: full-bleed dark square, mark centered — no transparency
//   (apple-touch-icon — iOS black-fills transparent PNGs — and maskable icons,
//   cropped by launcher masks, so the glyph stays inside the 80% safe zone)
// Also (re)writes public/icon.svg (the SVG favicon) from the same paths.
// NOTE: icons are served from public/ and wired via metadata.icons in
// src/app/layout.tsx. The app-dir file conventions (src/app/icon.png,
// apple-icon.png, manifest.ts) crash `next build` with a Turbopack panic
// ("Dependency tracking is disabled...") in this Next version — do not
// reintroduce them.
import { mkdirSync, writeFileSync } from "node:fs";
import sharp from "sharp";

const OUT = "/home/z/my-project";

// Rounded-square tile (copied from the historical public/logo.svg geometry)
const SQUARE =
  "M24.51,28.51H5.49c-2.21,0-4-1.79-4-4V5.49c0-2.21,1.79-4,4-4h19.03c2.21,0,4,1.79,4,4v19.03C28.51,26.72,26.72,28.51,24.51,28.51z";

// Flask mark — FlaskMark (viewBox 24) scaled by 30/24 = 1.25
const FLASK =
  "M12.25 3.75 H17.75 V10.6 L24.5 24.75 Q25.25 26.75 23.1 26.75 H6.9 Q4.75 26.75 5.5 24.75 L12.25 10.6 Z";
const LIQUID =
  "M8.25 19 H21.75 L23.8 24.25 Q24.5 25.75 23.1 25.75 H6.9 Q5.5 25.75 6.2 24.25 Z";
const ACCENT = "#F5654A"; // default coral accent (--acc in globals.css)

function glyph() {
  return `
<path d="${LIQUID}" fill="${ACCENT}"/>
<circle cx="15" cy="14.9" r="1.4" fill="${ACCENT}"/>
<circle cx="17.3" cy="12.5" r="0.85" fill="${ACCENT}"/>
<path d="${FLASK}" fill="none" stroke="#FFFFFF" stroke-width="1.9" stroke-linejoin="round"/>`;
}

function svg(size, { bleed = false, glyphScale = 1 } = {}) {
  const bg = bleed
    ? `<rect width="30" height="30" fill="#2D2D2D"/>`
    : `<path fill="#2D2D2D" stroke="#FFFFFF" stroke-width="0.6317" stroke-miterlimit="10" d="${SQUARE}"/>`;
  const open =
    bleed && glyphScale !== 1
      ? `<g transform="translate(15,15) scale(${glyphScale}) translate(-15,-15)">`
      : `<g>`;
  return `<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" width="${size}" height="${size}">
${bg}
${open}${glyph()}
</g>
</svg>`;
}

async function emitPng(file, size, opts) {
  // No density override: the SVG's width/height attributes define the exact
  // pixel size (librsvg scales attrs by density/72, so a custom density
  // double-scales the raster).
  const png = await sharp(Buffer.from(svg(size, opts))).png().toBuffer();
  const meta = await sharp(png).metadata();
  if (meta.width !== size || meta.height !== size) {
    throw new Error(`${file}: expected ${size}x${size}, got ${meta.width}x${meta.height}`);
  }
  writeFileSync(file, png);
  console.log("wrote", file.replace(OUT + "/", ""), `${meta.width}x${meta.height}`, png.length, "bytes");
}

mkdirSync(OUT + "/public/icons", { recursive: true });

writeFileSync(OUT + "/public/icon.svg", svg(30));
console.log("wrote public/icon.svg");

// Favicon fallback + manifest "any" icons — rounded mark
await emitPng(OUT + "/public/icons/icon-256.png", 256);
await emitPng(OUT + "/public/icons/icon-192.png", 192);
await emitPng(OUT + "/public/icons/icon-512.png", 512);

// apple-touch-icon + maskable — full-bleed, mark centered
await emitPng(OUT + "/public/icons/apple-touch-icon.png", 180, { bleed: true, glyphScale: 0.78 });
await emitPng(OUT + "/public/icons/icon-maskable-192.png", 192, { bleed: true, glyphScale: 0.72 });
await emitPng(OUT + "/public/icons/icon-maskable-512.png", 512, { bleed: true, glyphScale: 0.72 });

console.log("done");
