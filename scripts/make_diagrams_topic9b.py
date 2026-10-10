#!/usr/bin/env python3
"""Render the Topic 9B figure set — 6 plates × light/dark = 12 transparent PNGs.

Pipeline identical to the approved Topic 6 / 7 / 8 / 9A sets.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t9b')
from common import LIGHT, DARK, OUT  # noqa: E402
import figs  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t9b/html')

EST = ('eq-established-rates', 1340, 610, figs.build_established_rates)
DYN = ('eq-dynamic-equilibrium', 1300, 620, figs.build_dynamic_equilibrium)
CHRO = ('eq-chromate-dichromate', 1300, 590, figs.build_chromate)
AMP = ('eq-ammonia-pressure', 1300, 640, figs.build_ammonia_pressure)
HAB = ('eq-haber-yield', 1300, 660, figs.build_haber_yield)
CON = ('eq-contact-yield', 1300, 640, figs.build_contact_yield)

FIGS = [EST, DYN, CHRO, AMP, HAB, CON]


def main():
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--force-color-profile=srgb'])
        ctx = browser.new_context(device_scale_factor=2,
                                  viewport={'width': 1500, 'height': 1200})
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
