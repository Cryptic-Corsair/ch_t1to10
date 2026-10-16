// Generates the favicon / PWA icon set from the IAL Chem mark (public/logo.svg).
// - "mark" style: dark rounded square + white stroke, transparent corners
//   (favicon fallbacks + manifest "any" icons)
// - "bleed" style: full-bleed dark square, glyph centered — no transparency
//   (apple-touch-icon — iOS black-fills transparent PNGs — and maskable icons,
//   cropped by launcher masks, so the glyph stays inside the 80% safe zone)
import { mkdirSync, writeFileSync } from "node:fs";
import sharp from "sharp";

const OUT = "/home/z/my-project";

// Path data copied verbatim from public/logo.svg
const SQUARE =
  "M24.51,28.51H5.49c-2.21,0-4-1.79-4-4V5.49c0-2.21,1.79-4,4-4h19.03c2.21,0,4,1.79,4,4v19.03C28.51,26.72,26.72,28.51,24.51,28.51z";
const G1 =
  "M15.47,7.1l-1.3,1.85c-0.2,0.29-0.54,0.47-0.9,0.47h-7.1V7.09C6.16,7.1,15.47,7.1,15.47,7.1z";
const G2 = "24.3,7.1 13.14,22.91 5.7,22.91 16.86,7.1";
const G3 =
  "M14.53,22.91l1.31-1.86c0.2-0.29,0.54-0.47,0.9-0.47h7.09v2.33H14.53z";

function svg(size, { bleed = false, glyphScale = 1 } = {}) {
  const bg = bleed
    ? `<rect width="30" height="30" fill="#2D2D2D"/>`
    : `<path fill="#2D2D2D" stroke="#FFFFFF" stroke-width="0.6317" stroke-miterlimit="10" d="${SQUARE}"/>`;
  const glyphOpen =
    bleed && glyphScale !== 1
      ? `<g fill="#FFFFFF" transform="translate(15,15) scale(${glyphScale}) translate(-15,-15)">`
      : `<g fill="#FFFFFF">`;
  return `<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" width="${size}" height="${size}">
${bg}
${glyphOpen}
<path d="${G1}"/>
<polygon points="${G2}"/>
<path d="${G3}"/>
</g>
</svg>`;
}

async function emit(file, size, opts) {
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

// NOTE: icons are served from public/ and wired via metadata.icons in
// src/app/layout.tsx. The app-dir file conventions (src/app/icon.png,
// apple-icon.png, manifest.ts) crash `next build` with a Turbopack panic
// ("Dependency tracking is disabled...") in this Next version — do not
// reintroduce them.

// Favicon fallback + manifest "any" icons — rounded mark
await emit(OUT + "/public/icons/icon-256.png", 256);
await emit(OUT + "/public/icons/icon-192.png", 192);
await emit(OUT + "/public/icons/icon-512.png", 512);

// apple-touch-icon + maskable — full-bleed, glyph centered
await emit(OUT + "/public/icons/apple-touch-icon.png", 180, { bleed: true, glyphScale: 0.78 });
await emit(OUT + "/public/icons/icon-maskable-192.png", 192, { bleed: true, glyphScale: 0.72 });
await emit(OUT + "/public/icons/icon-maskable-512.png", 512, { bleed: true, glyphScale: 0.72 });

console.log("done");
