# Knowledge Base — Anchor Companion Bot

> 🚧 **STUB.** This file is a placeholder scaffold. It defines the *slots* for the facts the bot may
> state, but **every value is unfilled and unconfirmed.** The knowledge base is the *sole source of
> stated facts* — the bot may not state any fact that is not sourced here. Do not populate a slot
> without an approved governed source. Every open item is mirrored in [`/VERIFY.md`](../../VERIFY.md).

## Purpose & authority

This layer holds **the facts the bot states** — drawn from the catalog, program pages, and the aid &
registrar's approved language. If a fact is not here, the bot does not state it (it hands off instead).

**Precedence:** the knowledge base is authoritative for facts. Neither the voice layer nor the bot's
training may supply a number, name, price, or status that this file does not.

## Fact slots

Each entry needs a **value**, an **approved-language phrasing**, and a **source**. Until all three are
present, the entry stays `UNCONFIRMED` and the bot must hand off the topic.

### Institution & credibility

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| Institution name | Anchor Christian University (short: "Anchor") | — | Voice spec §8 naming | ✅ confirmed |
| Years of experience | `TODO` ("over 20 years" — VERIFY) | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| "Credits recognized by top universities" | `TODO` | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Accreditation status | `TODO` (regulated — approved current-status language only; no timeline) | `TODO` | `TODO` | ⛔ UNCONFIRMED |

### Transfer agreements

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| # of 1-to-1 transfer-agreement universities | `TODO` — **brandbook says 6; a call said 7 — RESOLVE** | State only this confirmed number, or none | `TODO` | ⛔ UNCONFIRMED |
| Are they regionally accredited Christian universities? | `TODO` | `TODO` | `TODO` | ⛔ UNCONFIRMED |

### Cost & discounts

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| Published per-credit cost | `TODO` | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Ministry-partnership discount | `TODO` (who qualifies, how much) | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| "Half the price of traditional schools" | `TODO` — confirm current, approved phrasing | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Financial aid / Title IV / 529 | **Not available (per calls) → HAND OFF, do not state as available** | n/a — route to human | `TODO` VERIFY current status | ⛔ UNCONFIRMED |

### Product, framework & system names

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| Learning framework name | "Learning Blueprint" (confirm exact capitalization/wording) | `TODO` | Voice spec §8 | ⛔ UNCONFIRMED |
| Student Information System (SIS) product | `TODO` — confirm before the bot names it | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Learning Management System (LMS) product | `TODO` — confirm before the bot names it | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Application URL | `TODO` — confirm before the bot names it | `TODO` | `TODO` | ⛔ UNCONFIRMED |
| Preliminary credit-estimate tool | `TODO` (name + link — referenced in voice spec §9) | `TODO` | `TODO` | ⛔ UNCONFIRMED |

### Faith & community

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| Statement of faith | `TODO` (link/text the bot may point to) | `TODO` | Voice spec §9 fit example | ⛔ UNCONFIRMED |
| Community covenant | `TODO` (link/text) | `TODO` | Voice spec §9 fit example | ⛔ UNCONFIRMED |
| Application components | `TODO` — e.g. ministry-leader reference + faith/testimony account (confirm) | `TODO` | Voice spec §9 | ⛔ UNCONFIRMED |

### Programs

| Fact | Value | Approved phrasing | Source | Status |
|---|---|---|---|---|
| Program list (gap-year / degree-completion / master's / professional tracks) | `TODO` | `TODO` | Catalog / program pages | ⛔ UNCONFIRMED |

<!-- TODO: expand into per-program entries (degree, length, format, requirements) once catalog access
is available. Personas in voice spec §7: Grace (gap-year/young-ministry), John (master's/professional),
plus the underweighted transfer-in finisher. -->

## Naming guardrails (from voice spec §8)

- Always "Anchor" or "Anchor Christian University." **Never** the ASR manglings ("Ankor") or other misfires.
- Do not name the SIS, LMS, or application URL until the values above are confirmed.
