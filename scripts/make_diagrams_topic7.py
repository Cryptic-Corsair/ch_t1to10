#!/usr/bin/env python3
"""Render the Topic 7 figure set — 7 plates × light/dark = 14 transparent PNGs.

Playwright pipeline identical to the approved Topic 4 v2 / Topic 6 sets:
device_scale_factor 2, omit_background transparent PNGs, Geist typography.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t7')
from common import LIGHT, DARK, OUT, shell  # noqa: E402
import figs  # noqa: E402
import figs2  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t7/html')

# figure tuples: (name, width, height, build_fn)
figs.LONDON = ('imf-london-origin', 1328, 620, figs.build_london)
figs.CONTACT = ('imf-contact-area', 1328, 560, figs.build_contact)
figs.HBOND_GEO = ('imf-hbond-geometry', 1328, 560, figs.build_hbond_geo)
figs.HYDRIDES = ('imf-hydrides-graph', 1248, 620, figs.build_hydrides)
figs2.ICE = ('imf-ice-lattice', 1328, 580, figs2.build_ice)
figs2.NACL = ('imf-nacl-hydration', 1248, 660, figs2.build_nacl)
figs2.SOLUBILITY = ('imf-alcohol-solubility', 1328, 560, figs2.build_solubility)

FIGS = [
    figs.LONDON, figs.CONTACT, figs.HBOND_GEO, figs.HYDRIDES,
    figs2.ICE, figs2.NACL, figs2.SOLUBILITY,
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
