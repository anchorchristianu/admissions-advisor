# System Prompt — Injection Variables

The production prompt ([`system-prompt.md`](system-prompt.md)) is voice-complete but not self-contained:
governed content is injected at runtime so that policy and facts can change without editing the persona.
Assemble the final prompt by replacing each `{{VARIABLE}}` with content from the layer named below.

| Variable | Replace with | Source layer | Status |
|---|---|---|---|
| `{{KNOWLEDGE_BASE}}` | The approved, sourced facts the bot may state (only the confirmed slots) | [`docs/knowledge-base/knowledge-base.md`](../docs/knowledge-base/knowledge-base.md) | 🚧 stub |
| `{{HANDOFF_CHANNEL}}` | How a hand-off (D4) actually reaches a human (warm async packet by default; live handoff if the staff toggle is on) + what context is passed | ops / integration | ❌ undefined |
| `{{ESTIMATOR_TOOL}}` | Name + link of the preliminary-estimate tool for D3 (transcript-eval / PLA; voice spec §9) | KB / [`/VERIFY.md`](../VERIFY.md) #13 | 🚧 stub |

> **Guardrails are no longer an injection variable.** The full decision procedure (dispositions D1–D5,
> the spine, category routing, the faith block, and the pre-send self-check) is inlined directly in
> `system-prompt.md`, because the taxonomy's §F specifies instruction-based enforcement at this scale. The
> governed source of record remains [`docs/guardrails/guardrail-taxonomy.md`](../docs/guardrails/guardrail-taxonomy.md);
> keep the two in sync when the taxonomy is versioned. The taxonomy's §E testing harness (innocent / pushy /
> reframed-to-sound-safe probes) is QA, not prompt content — run it against the assembled prompt before ship.

## Assembly rules

1. **Guardrails and KB are inlined, not summarized.** Paste the governed text; do not let the model
   paraphrase policy or facts.
2. **Inject only *confirmed* KB slots.** Any slot still marked `UNCONFIRMED` in the knowledge base must be
   omitted from `{{KNOWLEDGE_BASE}}` — its absence is what makes the bot hand the topic off, which is the
   correct behavior. Never inject a `TODO`/`VERIFY` value as if it were fact.
3. **Precedence at assembly time:** guardrails ▸ knowledge base ▸ voice. If a phrasing in the voice layer
   would violate an injected guardrail, the guardrail text wins.
4. **Do not ship** until [`/VERIFY.md`](../VERIFY.md) is clear. Before that point the assembled
   `{{KNOWLEDGE_BASE}}` is nearly empty and the bot is honest-but-thin by design — fine for testing voice,
   not for production.

## Suggested runtime shape (non-binding)

For an Anthropic Messages API deployment, the assembled prompt goes in the `system` field; the estimator
and hand-off channel are natural **tool** definitions rather than prose, so the model can invoke them
instead of describing them. That refactor belongs to the application layer and is out of scope here.
