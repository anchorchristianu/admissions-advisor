# Anchor Companion Bot

An admissions-advisor companion bot for **Anchor Christian University**. This repository holds the
governing documents the bot runs on — the layers that decide *how it sounds*, *what it may say*, and
*what facts it states* — plus the composed system prompt that assembles them.

> Speak as Anchor's guide: bold about the model, humble about the person; direct, warm, and practical;
> the prospect's calling is the hero and Anchor is the help along the way — move people from *torn* to
> *resolved* by telling the truth, even when the truth points elsewhere.

This is currently a **specification and scaffolding** repo. There is no application code yet; the goal
of this pass is to give every layer a home so the pieces can be filled in and later wired into a bot.

## The three-layer model

The bot's behavior is governed by three separate concerns, deliberately kept apart so each can be owned
and updated independently. This separation comes straight from the voice spec (§1).

| Layer | Governs | Source of authority | Status |
|---|---|---|---|
| **Voice / persona** | *How* the bot sounds and carries itself | Brand guidebook (vocabulary, naming, tone ceiling) + call transcripts (conversational rhythm) | ✅ Placed — [`docs/voice/`](docs/voice/) |
| **Guardrail taxonomy** | *What* the bot may say, must hand off, must never state | Governed policy | ✅ Placed — [`docs/guardrails/`](docs/guardrails/) (5-tier decision procedure) |
| **Knowledge base** | The *facts* the bot states | Catalog / program pages / aid & registrar's approved language | 🚧 Stub — [`docs/knowledge-base/`](docs/knowledge-base/) |

Two **source inputs** feed the voice layer and are captured for traceability:

- **Brand guidebook** — the 2023 Anchor Christian University Brand Guidebook (voice, strategy, personas, messaging).
- **Transcript distillation** — the distillation of 10 admissions calls (conversational rhythm). 🚧 Stub — [`docs/inputs/`](docs/inputs/)

### How conflicts are settled

From the voice spec's **voice-sourcing rule**: the **guidebook wins on word choice, naming, and tone
boundaries**; the **transcripts win on how a real exchange flows**. When a polished brand line would
sound stiff spoken aloud, keep the brand *vocabulary* but let the *rhythm* follow the counselor's live
cadence.

When the layers disagree on **whether something may be said at all**, the **guardrail taxonomy wins over
voice**, and the **knowledge base is the sole source of stated facts**. Voice never invents a fact or
overrides a hand-off rule.

## Repository layout

```
admissions-advisor/
├── README.md                     ← you are here
├── VERIFY.md                     ← consolidated list of claims that must be confirmed against governed sources
├── docs/
│   ├── voice/
│   │   └── brand-voice-persona-spec.md    ← the voice & persona spec (complete)
│   ├── guardrails/
│   │   └── guardrail-taxonomy.md          ← governed: 5-tier decision procedure (D1–D5)
│   ├── knowledge-base/
│   │   └── knowledge-base.md              ← STUB: the approved facts the bot may state
│   └── inputs/
│       └── transcript-distillation.md     ← STUB: conversational-rhythm source input
└── prompts/
    ├── system-prompt.md              ← DRAFT: full production prompt (voice-complete; guardrails/KB injected)
    └── system-prompt.variables.md    ← how the runtime injection variables are assembled
```

## Status & next steps

- [x] Repo scaffolding — every layer has a home; the voice spec is placed.
- [x] Place the **guardrail taxonomy** (governed 5-tier decision procedure) and inline it into the system prompt.
- [ ] Fill in the **knowledge base** with approved, sourced facts (`docs/knowledge-base/knowledge-base.md`).
- [ ] Fill in the **transcript distillation** (`docs/inputs/transcript-distillation.md`).
- [ ] Resolve every open item in [`VERIFY.md`](VERIFY.md).
- [x] Draft the production **system prompt** from the voice layer (`prompts/system-prompt.md`) — voice-complete; awaits guardrail/KB injection before it can ship.
- [ ] Wire the composed prompt into a runnable bot (application layer — out of scope for this pass).

> 🚧 **Stub files** describe the shape of the content they will hold and mark every unknown with a
> `TODO` or `VERIFY` note. Nothing in a stub should be treated as approved content.
