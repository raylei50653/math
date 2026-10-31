"""Verify rendered colors, period choices, shifts and responsive layout."""
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
    page.goto((directory / "color-preview.html").as_uri())
    frame = page.frame_locator("iframe")
    frame.locator("#cp-gallery button").last.wait_for()
    checked = 0
    for i in range(12):
        frame.locator("#cp-gallery button").nth(i).click()
        assert frame.locator("#cp-summary").inner_text().startswith(f"P{i+1:02d}")
        for value in ["1,1", "2,1", "1,2", "2,2", "3,1", "1,3"]:
            frame.locator("#cp-period").select_option(value)
            assert frame.locator("#cp-map .cp-edges").get_attribute("d")
            if "無法" in frame.locator("#cp-status").inner_text():
                assert frame.locator("#cp-map [data-color]").count() == 0
                assert frame.locator("#cp-shift-x").is_disabled()
                assert frame.locator("#cp-shift-y").is_disabled()
            else:
                assert frame.locator("#cp-map [data-color]").count() > 0
            checked += 1
    # P09: shift one cell swaps two colors; shift twice restores the original.
    frame.locator("#cp-gallery button").nth(8).click()
    frame.locator("#cp-period").select_option("2,1")
    original = frame.locator("#cp-map [data-color]").evaluate_all("xs=>xs.map(x=>x.dataset.color)")
    frame.locator("#cp-shift-x").click()
    assert "整體換色後重合" in frame.locator("#cp-status").inner_text()
    assert frame.locator("#cp-map [data-color]").evaluate_all("xs=>xs.map(x=>x.dataset.color)") != original
    frame.locator("#cp-shift-x").click()
    assert "原色完全重合" in frame.locator("#cp-status").inner_text()
    assert frame.locator("#cp-map [data-color]").evaluate_all("xs=>xs.map(x=>x.dataset.color)") == original
    # P05: independently compare every drawn mark to the stored witness while shifted.
    frame.locator("#cp-gallery button").nth(4).click()
    frame.locator("#cp-period").select_option("3,1")
    for shift in [1, 2, 0]:
        frame.locator("#cp-shift-x").click()
        assert frame.locator("#triangle-color-periods").evaluate("""(root,shift)=>{
            const d=JSON.parse(root.querySelector('#cp-colorings').textContent);
            const p=d.examples.find(e=>e.id==='P05').periods.find(p=>p.p===3&&p.q===1);
            const w=p.witnesses.find(w=>w.id===root.querySelector('#cp-witness').value);
            return [...root.querySelectorAll('#cp-map [data-color]')].every(mark=>{
              const [id,x,y]=mark.dataset.vertex.split(',').map(Number);
              return +mark.dataset.color===w.colors[0][((x-shift)%3+3)%3][id];
            });
        }""", shift)
    frame.locator("#cp-boxes").uncheck()
    assert frame.locator("#cp-map .cp-colorcell").count() == 0
    frame.locator("#cp-boxes").check()
    assert frame.locator("#cp-map .cp-colorcell").count() == 1
    frame.locator("#triangle-color-periods").screenshot(path=str(directory / "color-desktop.png"))
    dimensions = []
    for width in [780, 560, 360, 320]:
        page.set_viewport_size({"width":width,"height":1100})
        page.wait_for_timeout(120)
        dimensions.append(frame.locator("#triangle-color-periods").evaluate("el=>({available:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth})"))
        assert dimensions[-1]["scroll"] <= dimensions[-1]["available"] + 1
    assert not errors, errors
    print(json.dumps({"period_views":checked,"P09_two_step_color_swap":"PASS","P05_three_step_rendered_colors":"PASS","period_frames":"PASS","responsive":dimensions,"javascript_errors":errors}))
    browser.close()
