"""Preserve official download badges on the existing split-audio tutorial."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "iphone-video-tutorials/14-how-to-split-an-audio-file-on-iphone/index.html"
BADGE = "/assets/brand/app-store-badges/en.svg"
STORE = "https://apps.apple.com/us/app/audio-compressor-mp3-converter/id6769563659"


def render():
    if not (ROOT / BADGE.lstrip("/")).is_file():
        raise ValueError("Official Apple badge asset is required")
    soup = BeautifulSoup(PAGE.read_text(), "html.parser")
    top = soup.select_one("[data-tutorial-library] .guide-cta a")
    bottom = soup.select_one(".tutorial-app-download a[href*='apps.apple.com']")
    if top is None or bottom is None:
        raise ValueError("Expected both existing download destinations")
    for link in (top, bottom):
        if STORE not in link.get("href", ""):
            raise ValueError("Unexpected App Store destination")
        link["class"] = ["guide-store-badge"] if link is top else ["appstore", "guide-store-badge"]
        link.clear()
        badge = soup.new_tag("img", src=BADGE, width="240", height="80", alt="Download on the App Store")
        link.append(badge)
    purchase_note = soup.select_one(".tutorial-app-copy span")
    if purchase_note is not None:
        purchase_note.string = "See the App Store for current access and purchase options."
    css = soup.select_one('link[href^="/assets/tutorial-guides.css"]')
    if css is None:
        raise ValueError("Shared responsive badge stylesheet is required")
    css["href"] = "/assets/tutorial-guides.css?v=20261108-badges"
    PAGE.write_text(str(soup))


if __name__ == "__main__":
    render()
