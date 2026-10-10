#!/usr/bin/env python3
"""Render the Topic 6 figure set — 9 plates × light/dark = 18 transparent PNGs.

Playwright pipeline identical to the approved Topic 4 v2 set:
device_scale_factor 2, omit_background transparent PNGs, Geist typography.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
from common import LIGHT, DARK, OUT, HTML_DIR, shell  # noqa: E402
import figs_a, figs_b, figs_c, figs_d  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

FIGS = [figs_a.LEVELS, figs_a.PROFILES, figs_a.COOLING,
        figs_b.SOLUTION, figs_b.COMBUSTION,
        figs_c.HESS_COMBUSTION, figs_c.HESS_FORMATION,
        figs_d.DISSOCIATION, figs_d.BOND_CYCLE]

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
