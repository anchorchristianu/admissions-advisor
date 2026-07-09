#!/usr/bin/env python3
"""Scrape the paginated ACBC counselor directory by driving a real browser.

Reads every card on a page, clicks the "Next" control, and repeats until there
are no more pages. Writes counselors.json and counselors.csv.

Usage:
    pip install playwright && playwright install chromium
    python browser_scrape.py
    HEADLESS=0 python browser_scrape.py   # watch it run / tune selectors
"""

import csv
import json
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

URL = "https://biblicalcounseling.com/find-a-counselor/"
DELAY = 1.5          # seconds to wait between page turns (be polite)
MAX_PAGES = 500      # safety cap so a broken "next" can't loop forever
HEADLESS = os.environ.get("HEADLESS", "1") != "0"

# --- Tune these after inspecting one card in DevTools (see README Step 2). -----
# CARD_SELECTOR wraps ONE counselor entry. If left as None, the script falls
# back to a set of common patterns and, failing that, dumps raw card text.
CARD_SELECTOR = None
# Map output columns -> a CSS selector *within* a card. Leave a value as None to
# skip it. Emails/phones are also auto-detected from text as a backstop.
FIELD_SELECTORS = {
    "name": None,
    "location": None,
    "phone": None,
    "email": None,
    "certification": None,
}
# Candidate selectors tried, in order, when CARD_SELECTOR is None.
CARD_FALLBACKS = [
    ".counselor", ".counselor-card", ".directory-item", ".search-result",
    "article.result", "li.result", ".wpbdp-listing", ".geodir-post",
    ".fl-post-grid-post", ".elementor-post", ".et_pb_ajax_pagination_container .item",
]
# Candidate selectors for the "next page" control, tried in order.
NEXT_FALLBACKS = [
    "a[rel='next']", ".next", "a.next", "li.next a", ".pagination .next",
    "a:has-text('Next')", "button:has-text('Next')", ".nav-next a",
    ".page-numbers.next", "[aria-label='Next']",
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")


def find_card_selector(page):
    if CARD_SELECTOR:
        return CARD_SELECTOR
    for sel in CARD_FALLBACKS:
        if page.locator(sel).count() > 1:
            print(f"[cards] using fallback selector: {sel}", file=sys.stderr)
            return sel
    return None


def text_of(card, selector):
    if not selector:
        return ""
    loc = card.locator(selector)
    return loc.first.inner_text().strip() if loc.count() else ""


def extract_card(card):
    raw = card.inner_text().strip()
    row = {}
    for field, sel in FIELD_SELECTORS.items():
        row[field] = text_of(card, sel)
    # Backstops from raw text + links so nothing important is lost.
    if not row.get("email"):
        m = EMAIL_RE.search(raw)
        row["email"] = m.group(0) if m else ""
    if not row.get("email"):
        mailto = card.locator("a[href^='mailto:']")
        if mailto.count():
            row["email"] = mailto.first.get_attribute("href").replace("mailto:", "")
    if not row.get("phone"):
        m = PHONE_RE.search(raw)
        row["phone"] = m.group(0) if m else ""
    if not row.get("name"):
        # First non-empty line is usually the name/heading.
        row["name"] = next((ln.strip() for ln in raw.splitlines() if ln.strip()), "")
    row["raw_text"] = raw
    profile = card.locator("a[href]")
    row["profile_url"] = profile.first.get_attribute("href") if profile.count() else ""
    return row


def click_next(page):
    for sel in NEXT_FALLBACKS:
        loc = page.locator(sel)
        if not loc.count():
            continue
        el = loc.first
        try:
            if not el.is_visible():
                continue
        except Exception:
            continue
        # Treat disabled / aria-disabled controls as "no more pages".
        disabled = el.get_attribute("disabled") is not None
        aria = (el.get_attribute("aria-disabled") or "").lower() == "true"
        cls = (el.get_attribute("class") or "").lower()
        if disabled or aria or "disabled" in cls:
            return False
        el.scroll_into_view_if_needed()
        el.click()
        return True
    return False


def main():
    rows = []
    seen = set()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        print(f"[open] {URL}", file=sys.stderr)
        page.goto(URL, wait_until="networkidle", timeout=60000)

        card_sel = find_card_selector(page)
        if not card_sel:
            print("[!] Could not auto-detect a card selector. Set CARD_SELECTOR "
                  "after inspecting the page (see README).", file=sys.stderr)
            browser.close()
            sys.exit(1)

        for page_num in range(1, MAX_PAGES + 1):
            page.wait_for_selector(card_sel, timeout=30000)
            cards = page.locator(card_sel)
            n = cards.count()
            new_this_page = 0
            for i in range(n):
                row = extract_card(cards.nth(i))
                key = (row.get("name", ""), row.get("email", ""), row.get("raw_text", "")[:80])
                if key in seen:
                    continue
                seen.add(key)
                rows.append(row)
                new_this_page += 1
            print(f"[page {page_num}] {n} cards, {new_this_page} new, {len(rows)} total",
                  file=sys.stderr)

            time.sleep(DELAY)
            if not click_next(page):
                print("[done] no further Next control.", file=sys.stderr)
                break
            page.wait_for_load_state("networkidle", timeout=60000)

        browser.close()

    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, "counselors.json")
    csv_path = os.path.join(out_dir, "counselors.csv")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    cols = ["name", "location", "phone", "email", "certification", "profile_url", "raw_text"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {len(rows)} records to:\n  {json_path}\n  {csv_path}")


if __name__ == "__main__":
    main()
