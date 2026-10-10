// Verify the two remaining interfaces: Focus (terminal) + Studio (lab)
// lab gets the big ghost section numeral; print/classic are gone.
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  const base = 'http://localhost:3000';
  const out = '/home/z/my-project/scripts/';

  // ---------- FOCUS (terminal, default) ----------
  await page.goto(base + '/#/', { waitUntil: 'networkidle' });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(600);
  await page.screenshot({ path: out + 'v2-focus-home.png' });

  // ---------- STUDIO (lab) ----------
  await page.evaluate(() => {
    localStorage.setItem('ialchem-settings', JSON.stringify({
      state: { uiMode: 'lab', theme: 'carbon', accent: 'violet' }, version: 0,
    }));
  });
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(600);
  await page.screenshot({ path: out + 'v2-studio-home.png' });

  // studio topic page — big section numerals
  await page.goto(base + '/#/topic/energetics', { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  await page.screenshot({ path: out + 'v2-studio-topic-top.png' });
  // scroll to a section header to see the numeral
  const sec = await page.$('[data-uimode] .sec-giant');
  console.log('sec-giant present:', !!sec);
  if (sec) {
    await sec.scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    const head = await page.$('.sec-head');
    await head.screenshot({ path: out + 'v2-studio-sec-numeral.png' });
  }
  // count numerals on the page
  const n = await page.$$eval('.sec-giant', els => els.map(e => getComputedStyle(e).display + ':' + e.textContent));
  console.log('sec-giant items:', JSON.stringify(n));

  // studio: open settings panel (interface picker should show 2 modes)
  await page.goto(base + '/#/', { waitUntil: 'networkidle' });
  await page.evaluate(() => document.querySelector('button[title="Control room"], button[aria-label*="control room" i]')?.click());
  await page.waitForTimeout(700);
  await page.screenshot({ path: out + 'v2-studio-settings.png' });

  // ---------- mobile studio topic ----------
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto(base + '/#/', { waitUntil: 'networkidle' });
  await m.evaluate(() => {
    localStorage.setItem('ialchem-settings', JSON.stringify({
      state: { uiMode: 'lab', theme: 'carbon', accent: 'violet' }, version: 0,
    }));
  });
  await m.goto(base + '/#/topic/energetics', { waitUntil: 'networkidle' });
  await m.waitForTimeout(800);
  await m.screenshot({ path: out + 'v2-studio-mobile-topic.png' });

  // legacy mode snap-back: saved 'minimal' should land on terminal
  await page.evaluate(() => {
    localStorage.setItem('ialchem-settings', JSON.stringify({
      state: { uiMode: 'minimal', theme: 'paper', accent: 'coral' }, version: 0,
    }));
  });
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const mode = await page.evaluate(() => document.documentElement.dataset.uimode);
  console.log('legacy minimal resolves to:', mode);

  await browser.close();
  console.log('done');
})();
