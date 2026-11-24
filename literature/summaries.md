# One-page summaries

`PLAN.md` asks for these by the end of November, and the end-November gate asks whether a
published baseline reproduces. Both are the same job: read a paper, and write down what it
would take to get its number back.

Same four fields every time, so the answers line up into a table later. The last field is the
one that matters — it is what turns reading into the November experiment.

**Claims** — what the paper says it achieved, in its own terms.
**Measured on** — dataset, how many sites, how many traces, protocol, open or closed world.
**Cost reported** — bandwidth and latency overhead, or *none reported* if they did not measure it.
**To reproduce** — is the code public, is the data public, and what is missing. `../PLAN.md`
already answers most of this under *Code and data*; the judgement about what it would take is the
part worth writing.

Stop writing when the four fields are full. This is not an essay.

---

## 0. `pulls2024daitaeval` — Evaluating using the first eight DAITA servers

**Read this one first, and it is ten minutes.** Grey literature, not a paper: a June 2024 blog post
by Tobias Pulls. It is the *only* existing measurement of DAITA, which makes it the thing the March
experiment has to improve on — and it tells you exactly how, because it is explicit about what it
did not cover. Its method is also the template for February: 20 VMs, Selenium, tshark, 80,000
traces.

The four fields still apply, and field 3 is the one to copy out carefully.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 1. `siby2023quic` — Evaluating practical QUIC WF defenses for the masses — **read 2026-11-23**

Closest published work to this dissertation. Ships no code and no data, so it is the paper to
argue with rather than reproduce.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 2. `dyer2012peekaboo` — Peek-a-Boo, I Still See You

Named in `PLAN.md`. Coarse features defeat naive padding, which is the premise the whole project
rests on. Short. Skip if Siby already landed.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 3. `gong2020front` — Zero-delay lightweight defenses (FRONT)

Prerequisite, not background. FRONT is one of the three defences `cebere2026http2` reproduces and
the one Siby prices at 2.31 overhead for a ~70 % F1 drop. Ships code, attacks and datasets.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 4. `cai2014tamaraw` — A systematic approach to developing and evaluating WF defenses

Tamaraw, and a **lower bound on the bandwidth cost of any defence at a given security level**.
That bound is the floor under your cost curve. Also prerequisite for `khajavi2026lightening`,
whose implementation is literally called Adaptive-Tamaraw.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 5. `smith2021quicage` — Website Fingerprinting in the Age of QUIC

**This is the November gate baseline — the one you actually reproduce.** ~117,000 QUIC and TCP traces, publicly released with code. The
only large public dataset that is actually QUIC rather than Tor.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 6. `smith2022qcsd` — QCSD: a QUIC client-side WF defence framework

FRONT and Tamaraw implemented from the client alone using the QUIC PADDING frame, on a fork of
Mozilla's neqo. The nearest existing thing to what you would build, and the client-side comparator
to Maybenot. Siby positions itself directly against this.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 7. `sirinam2018deep` — Deep Fingerprinting

The attack half of the canon, and the DF dataset that half the field still benchmarks on —
`wang2026cease` runs its 2026 experiments on it. Tor, not QUIC, so use it to check your pipeline
against published numbers, not to answer your own question.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 8. `deng2025realistic` — Beyond a Single Perspective

The second half of the gate. Existing attacks run across defences, drift, multi-tab, early-stage,
open-world and few-shot, and the accuracy falls. Use their axes rather than inventing a set. Ships
nothing, so the axes are the deliverable, not the harness.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 9. `juarez2014critical` — A Critical Evaluation of Website Fingerprinting Attacks

Why published accuracy does not survive contact with reality. Read back to back with 8.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 10. `cebere2026http2` — Privacy-preserving potential of HTTP/2

A leakage-against-overhead curve that already exists, for FRONT, Tamaraw and ALPaCA. Read it for
the method. Makes much more sense after 3 and 4.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 11. `khajavi2026lightening` — Lightening the Load

NDSS 2026. A provable defence at lower overhead. The number a new cost curve has to beat.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 12. `sabzi2024netshaper` — NetShaper

Named in `PLAN.md`. Differential privacy applied to traffic shape. Also answer the open question:
does its threat model exclude colocation and shared-link leakage? No artifact link in the paper.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 13. `zhan2021earlyquic` — Website Fingerprinting on Early QUIC Traffic

Demoted. It was the obvious QUIC baseline until it turned out to ship no code and no data. Still
worth reading for the early-traffic framing, but 5 is the one you can actually rebuild.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

## 14. `pulls2023maybenot` — Maybenot

Documentation more than a paper, and it comes out in April. Note the attached PDF is arXiv v1,
matching the WPES 2023 citation; **v2 (September 2024) documents framework version 2** and is the
one to read before writing strategies.

**Claims**
**Measured on**
**Cost reported**
**To reproduce**

---

`PLAN.md` also asks for a summary of "the DAITA papers". There are none. Mullvad has published no
evaluation, and their own GotaTun audit excluded the DAITA code. `pulls2026ephemeral` is the
nearest thing and its author wrote Maybenot. That absence is a result — write it down as one.
