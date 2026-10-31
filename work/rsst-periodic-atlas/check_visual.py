#!/usr/bin/env python3
"""Check every displayed HNF decision and literal color against atlas witnesses."""
from pathlib import Path
import json
import os
import shutil

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "atlas.json").read_text())

VERIFY_COLORS = """root => {
  const data=JSON.parse(root.querySelector('#rp-data').textContent);
  const e=data.examples.find(e=>e.id===root.querySelector('#rp-specimen').value);
  const p=e.periods.find(p=>[p.a,p.b,p.d].join(',')===root.querySelector('#rp-period').value);
  const shift=root.querySelector('#rp-status').textContent.match(/平移 \\(([-\\d]+),([-\\d]+)\\)/);
  const sx=shift?+shift[1]:0,sy=shift?+shift[2]:0;
  const mod=(x,n)=>(x%n+n)%n;
  return [...root.querySelectorAll('.rp-node[data-color]')].every(mark=>{
    const[v,x,y]=mark.dataset.vertex.split(',').map(Number);
    const yy=y-sy,q=Math.floor(yy/p.d),xx=mod(x-sx-q*p.b,p.a);
    return +mark.dataset.color===p.witness.colors[(mod(yy,p.d)*p.a+xx)*e.points.length+v];
  });
}"""


def main():
    with sync_playwright() as p:
        executable = os.environ.get("TRIANGLE_ATLAS_CHROMIUM") or shutil.which("chromium") or shutil.which("google-chrome")
        browser = p.chromium.launch(executable_path=executable, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 780, "height": 1000}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto((HERE / "preview.html").as_uri())
        frame = page.frame_locator("iframe")
        root = frame.locator("#rsst-period-explorer")
        frame.locator("#rp-map svg").wait_for()
        checked, sat_count, unsat_count = 0, 0, 0
        distinct_shifts = {"same": 0, "permuted": 0, "other": 0}
        for e in DATA["examples"]:
            frame.locator("#rp-specimen").select_option(e["id"])
            for rec in e["periods"]:
                frame.locator("#rp-period").select_option(",".join(str(rec[k]) for k in ["a", "b", "d"]))
                assert frame.locator("#rp-map .rp-edges").get_attribute("d")
                if rec["status"] == "SAT":
                    assert frame.locator("#rp-map .rp-node[data-color]").count() > 0
                    assert root.evaluate(VERIFY_COLORS)
                    assert "原色完全重合" in frame.locator("#rp-status").inner_text()
                    for axis in ["x", "y"]:
                        frame.locator("#rp-shift-" + axis).click()
                        assert root.evaluate(VERIFY_COLORS)
                        text = frame.locator("#rp-status").inner_text()
                        if "原色完全重合" in text:
                            distinct_shifts["same"] += 1
                        elif "整體換色後重合" in text:
                            distinct_shifts["permuted"] += 1
                        else:
                            distinct_shifts["other"] += 1
                    sat_count += 1
                else:
                    assert frame.locator("#rp-map .rp-node[data-color]").count() == 0
                    assert frame.locator("#rp-shift-x").is_disabled()
                    assert frame.locator("#rp-shift-y").is_disabled()
                    assert "此指定週期不可行" in frame.locator("#rp-status").inner_text()
                    unsat_count += 1
                checked += 1
            sat = next(rec for rec in e["periods"] if rec["status"] == "SAT")
            frame.locator("#rp-period").select_option(",".join(str(sat[k]) for k in ["a", "b", "d"]))
            frame.locator("#rp-view").select_option("source")
            assert frame.locator("#rp-map .rp-node[data-color]").count() == e["source_n"]
            assert root.evaluate(VERIFY_COLORS)
            frame.locator("#rp-view").select_option("plane")
        frame.locator("#rp-specimen").select_option(DATA["examples"][0]["id"])
        root.screenshot(path=str(HERE / "preview-desktop.png"))
        dimensions = []
        for width in [780, 560, 360, 320]:
            page.set_viewport_size({"width": width, "height": 1100})
            page.wait_for_timeout(100)
            size = root.evaluate("el=>({available:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth})")
            assert size["scroll"] <= size["available"] + 1, size
            dimensions.append({"width": width, **size})
        root.screenshot(path=str(HERE / "preview-mobile.png"))
        assert not errors, errors
        result = {"all_hnf_views": checked, "SAT_views": sat_count, "UNSAT_views": unsat_count,
                  "every_drawn_color_matches_literal_witness": True,
                  "original_source_disks_checked": len(DATA["examples"]),
                  "shift_statuses_checked": distinct_shifts, "responsive": dimensions,
                  "javascript_errors": errors}
        (HERE / "visual-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result, ensure_ascii=False))
        browser.close()


if __name__ == "__main__":
    main()
