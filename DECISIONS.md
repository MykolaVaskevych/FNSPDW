# Decisions

Append-only. Newest last. One entry per decision that changed the topic, the scope or a
load-bearing claim, with the date and what it supersedes.

This file exists because the repo misled an assistant, which then misled me. `notes/PROJECT.md`
still described a project that had been abandoned two months earlier, and nothing recorded that
it had been abandoned. A reversal that leaves no trace reads as the current plan to anyone — human
or model — who finds the stale file first. Writing the reversal down is the fix.

**Rule: reverse a decision, add a line here in the same sitting.** Say what it supersedes.

---

**2026-09 (to 19 Sept)** — Dropped the original QUIC/padding topic as too close to existing
application-fingerprinting work. Moved to side channels in LLM streaming traffic. A prototype gave
0.81 undefended accuracy, 0.43 with shaping, at roughly 14x bandwidth and 3.9x latency, and found
four deployment failures; the novel one was cover traffic leaking the server's queue delay under
concurrency. *Superseded 2026-10-20.*

**2026-09-22** — Title agreed: *Network Side-Channel Leakage in Encrypted LLM Streaming Traffic:
Assessing Current Attacks and Evaluating a Traffic-Shaping Defence*. Farrell then asked what makes
LLM traffic any different and how it would be generated, and suggested plain web traffic instead.
*Superseded 2026-10-20.*

**2026-09** — Starter pack declared QUIC and Maybenot "permanently out of scope". *Reversed by
Farrell's generality instruction; both are now central.*

**2026-10-20** — **LLM dropped. Topic returned to Farrell's suggestion: does padding actually help,
on plain TLS and QUIC web traffic.** Reason: `experiments/token-batching` measured that OpenAI pads
every streamed event to a constant size, closing the token-length channel the attack depended on.
The measurement is kept as the project's motivation, not as a chapter.
*Supersedes the 2026-09 topic, the 2026-09-22 title, and `notes/PROJECT.md` sections 1 to 3, which
still present leak granularity as the organising concept and LLM content recovery as the final
chapter. `PLAN.md` governs.*

**2026-11-03** — Zotero's `disertation` collection became the single source of truth for references,
auto-exported by Better BibTeX to `paper/src/bibs/ref.bib`. That file is machine-written; editing it
by hand does nothing that survives.

**2026-11-23** — DAITA gap claim tightened. It had been stated as "nobody has independently
evaluated DAITA", which is too strong: `pulls2024daitaeval` exists. The defensible claim is in
`PLAN.md` under *The gap this fills*, and it is stronger, because it names the five axes the
existing measurement did not cover. *Supersedes the loose wording previously in
`literature/README.md`.*

**2026-11-23** — The end-November gate split in two: reproduce a published baseline by end
November, survive honest re-evaluation by mid-December. They are separate jobs with separate
failure modes. Also recorded: `siby2023quic` cannot be reproduced — it ships no code and no data —
so the baseline is `smith2021quicage`.
