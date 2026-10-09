#!/usr/bin/env python3
"""Re-render ONLY the Topic 8C halide-power-ladder plate (light + dark),
after adding the astatine rung to match the source table (Group 7 notes.pdf p9).
Does not touch any other plate."""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t8')
from common import LIGHT, DARK, OUT  # noqa: E402
import figs2  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t8/html')

LADDER = ('halide-power-ladder', 1300, 580, figs2.build_halide_ladder)

def main():
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    name, w, h, build = LADDER
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--force-color-profile=srgb'])
        ctx = browser.new_context(device_scale_factor=2,
                                  viewport={'width': 1500, 'height': 1200})
        page = ctx.new_page()
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
