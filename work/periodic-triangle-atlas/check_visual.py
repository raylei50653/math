"""Bounded browser checks for the specimen atlas; run with uv --with playwright."""
from pathlib import Path
import json
import os
import shutil
from playwright.sync_api import sync_playwright

directory = Path(__file__).resolve().parent
with sync_playwright() as p:
    chromium = os.environ.get("TRIANGLE_ATLAS_CHROMIUM") or shutil.which("chromium") or shutil.which("google-chrome")
    browser = p.chromium.launch(executable_path=chromium, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 780, "height": 1100}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((directory / "preview.html").as_uri())
    frame = page.frame_locator("iframe")
    frame.locator("#tc-gallery button").last.wait_for()
    assert frame.locator("#tc-gallery button").count() == 12
    for i in range(12):
        frame.locator("#tc-gallery button").nth(i).click()
        assert frame.locator("#tc-summary").inner_text().startswith(f"P{i+1:02d}")
        assert frame.locator("#tc-main .tc-edge").get_attribute("d")
    frame.locator("#tc-gallery button").nth(9).click()
    frame.locator("#tc-degree").check()
    assert frame.locator("#tc-main text.tc-number").count() > 30
    frame.locator("#tc-cell").uncheck()
    assert frame.locator("#tc-main .tc-boundary").count() == 0
    frame.locator("#tc-cell").check()
    assert frame.locator("#tc-main .tc-boundary").count() == 1
    frame.locator("#tc-degree").uncheck()
    frame.locator("#triangle-crystals-atlas").screenshot(path=str(directory / "preview-desktop.png"))
    dimensions = []
    for width in [780, 560, 360, 320]:
        page.set_viewport_size({"width": width, "height": 1100})
        page.wait_for_timeout(120)
        dimensions.append(frame.locator("#triangle-crystals-atlas").evaluate("el => ({available:document.documentElement.clientWidth, root:el.getBoundingClientRect().width, scroll:document.documentElement.scrollWidth})"))
        assert dimensions[-1]["scroll"] <= dimensions[-1]["available"] + 1, dimensions[-1]
        frame.locator("#tc-gallery button").nth(11).click()
        assert frame.locator("#tc-summary").inner_text().startswith("P12")
    frame.locator("#triangle-crystals-atlas").screenshot(path=str(directory / "preview-mobile.png"))
    assert not errors, errors
    print(json.dumps({"all_12_selections": "PASS", "degree_toggle": "PASS", "period_toggle": "PASS", "viewport_dimensions": dimensions, "javascript_errors": errors}))
    browser.close()
