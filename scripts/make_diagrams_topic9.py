#!/usr/bin/env python3
"""Render the Topic 9 figure set — 12 plates × light/dark = 24 transparent PNGs.

Pipeline identical to the approved Topic 6 / 7 / 8 sets.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/z/my-project/scripts/t6')
sys.path.insert(0, '/home/z/my-project/scripts/t9')
from common import LIGHT, DARK, OUT  # noqa: E402
import figs  # noqa: E402
import figs2  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML_DIR = Path('/home/z/my-project/scripts/t9/html')

ORIENT = ('kinetics-orientation', 1300, 610, figs.build_orientation)
RATEGR = ('kinetics-rate-graphs', 1340, 640, figs.build_rate_graphs)
CONC = ('kinetics-concentration-effect', 1240, 620, figs.build_concentration_effect)
PRESS = ('kinetics-pressure-effect', 1300, 600, figs.build_pressure_effect)
SURF = ('kinetics-surface-area', 1340, 800, figs.build_surface_area)
MB = ('kinetics-maxwell-boltzmann', 1300, 660, figs.build_maxwell_boltzmann)
MBT = ('kinetics-mb-temperature', 1300, 660, figs2.build_mb_temperature)
PROF = ('kinetics-reaction-profiles', 1340, 600, figs2.build_reaction_profiles)
CATP = ('kinetics-catalysed-profile', 1300, 620, figs2.build_catalysed_profile)
INTER = ('kinetics-catalyst-intermediate', 1300, 630, figs2.build_catalyst_intermediate)
MBCAT = ('kinetics-mb-catalyst', 1300, 620, figs2.build_mb_catalyst)
HET = ('kinetics-heterogeneous-catalyst', 1380, 660, figs2.build_heterogeneous_catalyst)

FIGS = [ORIENT, RATEGR, CONC, PRESS, SURF, MB, MBT, PROF, CATP, INTER, MBCAT, HET]


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
