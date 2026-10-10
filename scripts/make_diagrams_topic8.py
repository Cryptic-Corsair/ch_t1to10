#!/usr/bin/env python3
"""Render the Topic 8 figure set — 10 plates × light/dark = 20 transparent PNGs.

Pipeline identical to the approved Topic 6 / Topic 7 sets.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t8')
from common import LIGHT, DARK, OUT, shell  # noqa: E402
import figs  # noqa: E402
import figs2  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t8/html')

figs.ELECTRON = ('redox-electron-transfer', 1340, 640, figs.build_electron_transfer)
figs.AGENTS = ('redox-agents-map', 1240, 600, figs.build_agents_map)
figs.DISPROP = ('redox-disproportionation', 1280, 610, figs.build_disproportionation)
figs.G12TRENDS = ('group12-trends', 1360, 640, figs.build_group12_trends)
figs.SOLUB = ('group2-solubility', 1280, 600, figs.build_group2_solubility)
figs2.THERMAL = ('thermal-stability', 1360, 600, figs2.build_thermal_stability)
figs2.FLAME = ('flame-origins', 1360, 600, figs2.build_flame_origins)
figs2.TITRATE = ('titration-setup', 1300, 610, figs2.build_titration_setup)
figs2.GRID = ('displacement-grid', 1380, 640, figs2.build_displacement_grid)
figs2.LADDER = ('halide-power-ladder', 1300, 580, figs2.build_halide_ladder)

FIGS = [
    figs.ELECTRON, figs.AGENTS, figs.DISPROP, figs.G12TRENDS, figs.SOLUB,
    figs2.THERMAL, figs2.FLAME, figs2.TITRATE, figs2.GRID, figs2.LADDER,
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
