const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto('http://localhost:3000/#/', { waitUntil: 'networkidle' });
  await m.evaluate(() => {
    localStorage.clear();
    localStorage.setItem('ialchem-settings', JSON.stringify({
      state: { uiMode: 'lab', theme: 'carbon', accent: 'violet' }, version: 0,
    }));
  });
  await m.reload({ waitUntil: 'networkidle' });
  await m.goto('http://localhost:3000/#/topic/energetics', { waitUntil: 'networkidle' });
  await m.waitForTimeout(300);
  await m.reload({ waitUntil: 'networkidle' });
  await m.waitForTimeout(900);
  await m.screenshot({ path: '/home/z/my-project/scripts/v3-studio-mobile-topic.png' });
  const sec = await m.$('.sec-giant');
  if (sec) { await sec.scrollIntoViewIfNeeded(); await m.waitForTimeout(400); }
  await m.screenshot({ path: '/home/z/my-project/scripts/v3-studio-mobile-sec.png' });
  await browser.close();
  console.log('ok');
})();
