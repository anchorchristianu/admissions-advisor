#!/usr/bin/env python3
"""Scrape the counselor directory directly from its JSON backend (clean path).

Use this ONLY once you've found the endpoint in DevTools -> Network -> Fetch/XHR
(see README Step 1). Fill in ENDPOINT, PARAMS, and the response-shape helpers
below to match what you observed, then run:

    pip install requests
    python api_scrape.py

Writes counselors.json / counselors.csv. This is a template because the exact
endpoint and JSON shape have to be read off the live site.
"""

import csv
import json
import os
import time

import requests

# --- Fill these in from the Network tab -------------------------------------
ENDPOINT = "https://biblicalcounseling.com/wp-admin/admin-ajax.php"  # <-- replace
METHOD = "GET"                      # "GET" or "POST"
# Static params that don't change between pages:
BASE_PARAMS = {
    # "action": "find_counselor_search",
}
PAGE_PARAM = "paged"               # the param that increments per page
FIRST_PAGE = 1
DELAY = 1.0                         # seconds between requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://biblicalcounseling.com/find-a-counselor/",
}


def rows_from_response(data):
    """Return the list of record dicts from one page's JSON response.

    Adjust the path to match the real shape, e.g. data["data"]["results"].
    If the endpoint returns HTML instead of JSON, parse it here with
    BeautifulSoup instead (or just use browser_scrape.py).
    """
    if isinstance(data, list):
        return data
    for key in ("results", "data", "counselors", "items", "posts"):
        if isinstance(data, dict) and key in data:
            inner = data[key]
            return inner if isinstance(inner, list) else inner.get("results", [])
    return []


def normalize(rec):
    """Map one raw record to output columns. Adjust keys to the real payload."""
    def pick(*keys):
        for k in keys:
            if isinstance(rec, dict) and rec.get(k):
                return rec[k]
        return ""
    return {
        "name": pick("name", "title", "display_name"),
        "location": pick("location", "city", "address", "state"),
        "phone": pick("phone", "telephone"),
        "email": pick("email"),
        "certification": pick("certification", "level", "membership"),
        "profile_url": pick("url", "permalink", "link"),
    }


def has_more(data, page_rows, page_num):
    """Decide whether to fetch another page."""
    if not page_rows:
        return False
    if isinstance(data, dict):
        for k in ("max_pages", "total_pages", "pages"):
            if k in data:
                return page_num < int(data[k])
    return True  # otherwise: stop when a page returns zero rows


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    rows, page = [], FIRST_PAGE
    while True:
        params = dict(BASE_PARAMS, **{PAGE_PARAM: page})
        if METHOD == "POST":
            resp = session.post(ENDPOINT, data=params, timeout=30)
        else:
            resp = session.get(ENDPOINT, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        page_rows = rows_from_response(data)
        rows.extend(normalize(r) for r in page_rows)
        print(f"[page {page}] {len(page_rows)} rows, {len(rows)} total")
        if not has_more(data, page_rows, page):
            break
        page += 1
        time.sleep(DELAY)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir, "counselors.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    cols = ["name", "location", "phone", "email", "certification", "profile_url"]
    with open(os.path.join(out_dir, "counselors.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {len(rows)} records.")


if __name__ == "__main__":
    main()
