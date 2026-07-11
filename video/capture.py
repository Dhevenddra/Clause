"""Record demo footage of the deployed app with timestamped scene marks.

Run: python video/capture.py
Outputs: video/raw/<hash>.webm + video/marks.json + video/cards/card{1,7,8}.png
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://clause-4vv4.onrender.com"
HERE = Path(__file__).parent
RAW = HERE / "raw"
CARDS = HERE / "cards"
RAW.mkdir(exist_ok=True)
CARDS.mkdir(exist_ok=True)

ADVERSARIAL = (HERE.parent / "demo" / "claim_adversarial.md").read_text(encoding="utf-8")

marks: dict[str, float] = {}
t0 = 0.0


def mark(name: str) -> None:
    marks[name] = round(time.time() - t0, 2)
    print(f"  mark {name}: {marks[name]}s")


def main() -> None:
    global t0
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ---- title cards (no recording needed) ----
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto((HERE / "cards.html").as_uri())
        page.wait_for_timeout(3500)  # fonts
        for cid in ("card1", "card7", "card8"):
            page.locator(f"#{cid}").screenshot(path=str(CARDS / f"{cid}.png"))
        page.close()
        print("cards done")

        # ---- footage ----
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(RAW),
            record_video_size={"width": 1280, "height": 720},
        )
        page = ctx.new_page()
        t0 = time.time()
        page.goto(BASE)
        page.wait_for_timeout(3000)  # fonts + hero
        mark("hero")

        # s2 — load the deny case file
        page.wait_for_timeout(1500)
        page.click('button[data-demo="deny"]')
        mark("deny_loaded")
        page.wait_for_timeout(2500)

        # s3 — adjudicate: loading state, then verdict
        page.click("#adjudicate")
        mark("adjudicate_click")
        page.wait_for_selector("#result:not([hidden])", timeout=300_000)
        mark("result_visible")
        page.wait_for_timeout(5000)  # cascade plays

        # s4 — ledger + citation highlight
        page.eval_on_selector(".ledger-head", "el => el.scrollIntoView({behavior:'smooth', block:'start'})")
        page.wait_for_timeout(1500)
        mark("ledger")
        page.wait_for_timeout(2000)
        page.click(".point.clickable >> nth=0")
        mark("highlight_click")
        page.wait_for_timeout(5000)  # sweep + read

        # s6 footage (captured before s5; reordered in edit) — audit row
        page.eval_on_selector(".auditrow", "el => el.scrollIntoView({behavior:'smooth', block:'center'})")
        page.wait_for_timeout(1500)
        mark("audit")
        page.wait_for_timeout(3500)

        # s5 — adversarial claim
        page.eval_on_selector("#claim", "el => el.scrollIntoView({behavior:'smooth', block:'center'})")
        page.wait_for_timeout(1000)
        mark("adversarial_paste")
        page.evaluate(
            """(text) => { const c = document.getElementById('claim');
                 c.value = text; c.dispatchEvent(new Event('input')); }""",
            ADVERSARIAL,
        )
        page.wait_for_timeout(2000)
        page.eval_on_selector("#adjudicate", "el => el.scrollIntoView({behavior:'smooth', block:'center'})")
        page.wait_for_timeout(800)
        page.click("#adjudicate")
        mark("adv_click")
        page.wait_for_selector("#result:not([hidden])", timeout=300_000)
        mark("adv_result")
        page.wait_for_timeout(4500)
        page.eval_on_selector(".ledger-head", "el => el.scrollIntoView({behavior:'smooth', block:'start'})")
        page.wait_for_timeout(3000)
        page.eval_on_selector("#missing", "el => el.scrollIntoView({behavior:'smooth', block:'center'})")
        mark("adv_missing")
        page.wait_for_timeout(4000)
        mark("end")

        video_path = page.video.path()
        ctx.close()  # flushes video
        browser.close()
        marks["_video_file"] = str(video_path)
        (HERE / "marks.json").write_text(json.dumps(marks, indent=2))
        print(json.dumps(marks, indent=2))


if __name__ == "__main__":
    main()
