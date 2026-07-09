# Counselor directory scraper

Extracts the paginated counselor listing at
<https://biblicalcounseling.com/find-a-counselor/> (ACBC) into structured
`counselors.json` / `counselors.csv`.

The directory is a JavaScript-driven widget with a **Next** button and hundreds
of entries, so a plain `curl` of the page returns markup with no data (or a 403).
There are two ways in — try the clean one first, fall back to the robust one.

> **Run this locally.** It talks directly to `biblicalcounseling.com`, which is
> not reachable from the Claude Code web sandbox (its egress policy allowlists
> only package registries, GitHub, etc.). On your own machine there's no such
> restriction.

---

## Step 1 — Look for a JSON API (the clean path)

Most "load more / next" directories fetch their rows from a backend endpoint
that returns JSON. If it exists, hitting it directly is faster, complete, and
doesn't depend on any HTML layout.

1. Open <https://biblicalcounseling.com/find-a-counselor/> in Chrome.
2. Open **DevTools → Network**, filter to **Fetch/XHR**.
3. Click **Next** (or type in the search box). Watch for a request that returns
   a JSON body full of counselor records. Likely shapes for this stack
   (WordPress):
   - `…/wp-admin/admin-ajax.php?action=…&paged=2`
   - `…/wp-json/<plugin>/v1/…?page=2`
   - a search provider like Algolia / a map plugin (`store-locator`, etc.)
4. If you find one, note the URL, the query/body params that change with the
   page (`page`, `paged`, `offset`, `start`), and any pagination total in the
   response. Then loop it with `api_scrape.py` (edit the endpoint + params at
   the top). This is the preferred method — use it if an endpoint exists.

If you only see the page HTML being replaced (no JSON XHR), the data is rendered
server-side per page — go to Step 2.

## Step 2 — Drive the browser (the robust path)

`browser_scrape.py` opens the real page in a headless browser, reads every card
on the page, clicks **Next**, and repeats until the button disappears/disables.
It works regardless of how the data arrives because it reads the rendered DOM.

```bash
python -m venv .venv && source .venv/bin/activate
pip install playwright
playwright install chromium
python browser_scrape.py
```

Outputs `counselors.json` and `counselors.csv` in this folder.

### Tuning the extraction

The script uses generic selectors because the exact class names need to be read
off the live DOM. To make it precise:

1. Run once with `HEADLESS=0 python browser_scrape.py` so you can watch it.
2. In DevTools, inspect one counselor card. Note the selector that wraps a
   single entry (e.g. `.counselor-card`, `article.result`, `li.directory-item`).
3. Set `CARD_SELECTOR` at the top of the script, and map each field
   (`name`, `location`, `phone`, `email`, `certification`) to its selector in
   `FIELD_SELECTORS`. Everything else stays the same.

The default run still works without tuning — it captures each card's full text
and any links (so emails/phones survive), just less tidily columned.

## Etiquette

- Both scripts pause between pages (`DELAY` seconds) so you don't hammer the
  site. Keep it at 1s+.
- This is public directory data; scrape it for your own use, and respect the
  site's terms and robots.txt.
