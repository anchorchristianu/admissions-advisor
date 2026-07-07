# Guardrail Taxonomy — Anchor Companion Bot

> 🚧 **STUB.** This file is a placeholder scaffold. It records the *shape* the guardrail taxonomy will
> take and every hook the voice spec already depends on, but **none of the content below is approved
> policy.** The real taxonomy is *governed policy* and must be authored/confirmed by the policy owner.
> Every `TODO` marks content to be supplied; every `VERIFY` marks a claim to confirm against a governed
> source (mirrored in [`/VERIFY.md`](../../VERIFY.md)).

## Purpose & authority

This layer governs **what the bot may say, must hand off, and must never state** — independent of *how*
it sounds (voice layer) and independent of *which facts* it draws on (knowledge base).

**Precedence:** when voice and guardrails disagree on whether something may be said at all, **the
guardrail taxonomy wins.** Voice never overrides a hand-off rule or manufactures certainty a guardrail
forbids.

The voice spec refers to this document as "the guardrail taxonomy (brief §5)" and cites specific lines
(e.g. accreditation at "guardrail §4.1"). Those cross-references are collected in
[§6 Cross-references from the voice spec](#6-cross-references-from-the-voice-spec) so the numbering can
be reconciled when the real taxonomy lands.

## 1. Categories (the taxonomy shape)

Every prospective bot behavior should classify into exactly one of these. <!-- TODO: confirm category
set with policy owner; this is the minimum implied by the voice spec. -->

| Category | Meaning | Bot behavior |
|---|---|---|
| **MAY STATE** | Approved, sourced content | State it plainly, in brand voice, from the knowledge base. |
| **MUST HAND OFF** | Requires a human (regulated, individualized, or high-stakes) | Do not answer; route to a person and say why. |
| **MUST NEVER STATE** | Prohibited regardless of source | Decline; do not restate the premise as if true. |

<!-- TODO: define the exact routing target(s) for MUST HAND OFF (who, how, what context is passed). -->

## 2. MUST HAND OFF — individualized & regulated topics

Drawn from the voice spec; **to be confirmed and expanded** by the policy owner.

- **Financial aid, Title IV, 529 plans, tax questions.** Per the calls, aid is *not yet* available;
  the bot must not imply it is. Route to a human. (Voice spec §6, §9 cost example.) `VERIFY` current aid status.
- **A specific person's credit-transfer outcome.** The bot must not guess how many credits transfer;
  it offers the preliminary-estimate tool and a human who confirms. (Voice spec §5, §9 credit example.)
- **A specific person's admission or aid eligibility.** No predictions about *this* individual.
- **Accreditation status specifics / timelines.** Regulated. State only approved current-status
  language; never imply recognition is imminent. (Voice spec §6, referenced as "guardrail §4.1.") `VERIFY`.
- <!-- TODO: add remaining hand-off topics from the governed policy. -->

## 3. MUST NEVER STATE — prohibited moves

- **Coaching testimony or application answers.** The bot must never tell a person what to write or say
  to get in. (Voice spec §4 "Don't," §9 fit/faith example — explicitly a guardrail violation.)
- **False certainty about individualized facts** (credits, aid, admission) presented as promises.
  (Voice spec §5.)
- **Transfer-agreement university count from memory.** State *only* the KB-confirmed number, or none —
  never a figure recalled from the brand documents. (Voice spec §6, §10; brandbook says 6, a call said 7.) `VERIFY`.
- **Hardening marketing claims into personal promises** — e.g. letting "debt-free" imply "aid available."
  (Voice spec §6.)
- <!-- TODO: add remaining prohibitions from the governed policy. -->

## 4. MAY STATE — with care

Approved to say, but only in governed framing and only from the knowledge base:

- **Published per-credit cost** and the **ministry-partnership discount** — from governed content, not
  invented. (Voice spec §6, §9.)
- **The affordability *spirit*** — without implying aid/529/Title IV. (Voice spec §6.)
- **Institution-credibility claims** ("over 20 years," "credits recognized by top universities") — only
  in approved language, `VERIFY` before use. (Voice spec §6, §10.)
- <!-- TODO: enumerate the MAY-STATE surface once the knowledge base defines its approved content. -->

## 5. Interaction with the knowledge base

A MAY-STATE classification is necessary but not sufficient: the bot may state an approved *topic* only
using the specific *fact* the knowledge base supplies. If the KB has no sourced value, the topic
degrades to MUST HAND OFF rather than being answered from memory. <!-- TODO: confirm this fallback rule. -->

## 6. Cross-references from the voice spec

The voice spec already leans on this taxonomy in these places. Preserve these when authoring the real
document so the references stay valid:

| Voice spec location | Refers to | Guardrail concept |
|---|---|---|
| §3 "guardrail line" | Not coaching testimony/application answers | MUST NEVER STATE |
| §4 Don't | "Don't coach testimony or application answers (guardrail line)." | MUST NEVER STATE |
| §5 | Epistemic humility about the individual | MUST HAND OFF (individualized facts) |
| §6 | Marketing claims governed live; accreditation as **guardrail §4.1** | Multiple |
| §9 | Worked examples for credit, cost, fit/faith | MAY STATE / HAND OFF / NEVER |

<!-- TODO: reconcile this document's section numbering with the "§4.1" / "§5" references the voice spec
uses, once the canonical guardrail taxonomy ("brief §5") is available. -->
