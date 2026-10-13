#!/usr/bin/env python3
"""Render the Topic 10 IR figure set — light + dark transparent PNGs.

Renders the 4 new IR plates and re-renders t10-ir-spectrum (updated labels).
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t10')
from common import LIGHT, DARK, OUT  # noqa: E402
import figs  # noqa: E402
import figs_ir  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t10/html')

FIGS = [
    ('t10-ir-spectrum', 1240, 640, figs.build_ir_spectrum),
    ('t10-ir-vibrations', 1240, 560, figs_ir.build_vibrations),
    ('t10-ir-examples', 1240, 820, figs_ir.build_examples),
    ('t10-ir-halides-amines', 1240, 820, figs_ir.build_halides_amines),
    ('t10-ir-q1', 1240, 560, figs_ir.build_q1),
]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--force-color-profile=srgb'])
        ctx = browser.new_context(device_scale_factor=2,
                                  viewport={'width': 1500, 'height': 1200})
        page = ctx.new_page()
        for name, w, h, build in FIGS:
            if only and only not in name:
                continue
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
