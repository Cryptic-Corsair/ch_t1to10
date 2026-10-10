#!/usr/bin/env python3
"""Render the Topic 4 v2 figure set — 8 plates × light/dark = 16 transparent PNGs.

Same filenames as v1 → seed data unchanged. 2× device scale for crispness.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t4v2')
from common import (LIGHT, DARK, OUT, HTML_DIR, shell)  # noqa: E402
import figs_a, figs_b, figs_c, figs_d  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

FIGS = [figs_a.HAZARD, figs_a.FORMULA, figs_a.SKELETAL,
        figs_b.ALKANE, figs_b.CYCLO,
        figs_c.COLUMN, figs_c.POLLUTANTS,
        figs_d.MECH]

def main():
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--force-color-profile=srgb'])
        ctx = browser.new_context(device_scale_factor=2,
                                  viewport={'width': 1400, 'height': 1100})
        page = ctx.new_page()
        for name, w, h, build in FIGS:
            for variant, pal in (('light', LIGHT), ('dark', DARK)):
                html = build(pal)
                hp = HTML_DIR / ('%s-%s.html' % (name, variant))
                hp.write_text(html)
                page.goto(hp.as_uri())
                page.evaluate('() => document.fonts.ready.then(() => true)')
                page.wait_for_timeout(60)
                fname = name + ('-dark' if variant == 'dark' else '') + '.png'
                page.locator('.plate').screenshot(path=str(OUT / fname),
                                                  omit_background=True)
                print('rendered', fname)
        browser.close()

if __name__ == '__main__':
    main()
