"""Re-screenshot card1 and rebuild s1 + final concat."""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 720})
    page.goto((HERE / "cards.html").as_uri())
    page.wait_for_timeout(3500)
    page.locator("#card1").screenshot(path=str(HERE / "cards" / "card1.png"))
    b.close()
print("card1 reshot")
