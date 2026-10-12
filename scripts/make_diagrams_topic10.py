#!/usr/bin/env python3
"""Render the Topic 10 figure set — 7 plates x light/dark = 14 transparent PNGs.

Pipeline identical to the approved Topic 6/7/8/9 sets.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t10')
from common import LIGHT, DARK, OUT  # noqa: E402
import figs  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t10/html')

FIGS = [
    ('t10-nucleophile-attack', 1240, 560, figs.build_nucleophile),
    ('t10-halo-classes', 1240, 560, figs.build_halo_classes),
    ('t10-substitution-mechanism', 1300, 620, figs.build_mechanism),
    ('t10-alcohol-classes', 1240, 560, figs.build_alcohol_classes),
    ('t10-oxidation-flow', 1340, 660, figs.build_oxidation),
    ('t10-mass-spectrum', 1240, 640, figs.build_mass_spectrum),
    ('t10-ir-spectrum', 1240, 640, figs.build_ir_spectrum),
]


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
