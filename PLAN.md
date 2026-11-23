# Dissertation plan

**Does padding actually help?** What encrypted web traffic still reveals through packet
size, timing and direction, and what padding defences buy — measured against their cost
in bandwidth and latency.

Mykola (Nick) Vaskevych · MSc Future Networked Systems · Supervisor: Stephen Farrell
Submission: late August 2027

**This file is the only source of truth for topic and scope.** Where any other document in this
repo disagrees — including `notes/PROJECT.md` — this one wins, and the other one is stale and
should be corrected. `DECISIONS.md` records when and why the scope changed.

## Scope

**In.** Plain web traffic over TLS and QUIC. An attacker that classifies activity from
encrypted metadata, evaluated honestly. Padding defences: Mullvad's DAITA as a deployed
example, and my own strategies on the Maybenot framework. The cost curve of each.

**Out.** LLM traffic — checked in October and dropped, after Farrell asked what makes LLM
traffic different and suggested plain web traffic instead. Measured: OpenAI pads every streamed
event to a constant size with a random filler field, which closed the token-length channel I was
going to attack (`experiments/token-batching`).

That measurement is the motivation for this project rather than part of it. Note it does not
claim the channel is *gone*: `zhang2025netecho` reports recovering a large share of conversation
content from deployed streaming services despite that padding. Whether residual leakage survives
production padding is exactly the open question — which is the argument for measuring what
deployed padding buys, on traffic that can be collected honestly.

**Also out.** Anything needing payload decryption. Traffic from anyone who has not opted
in — my own devices only, unless ethics approval is in place first.

## Time available

Taught modules are heavier this semester and lighten from January, so the rest of this
year is part-time research and the real work starts in the new year. Exam dates are not
published yet; December and May are assumed to be reduced months and this plan will be
corrected once the dates are known.

Rough effort: ~10 h/week to December, ~20 h/week January to April, full-time from May.

## Month by month

**October–November 2026** — agree this plan. Make the repo readable: LaTeX and built PDF committed
where they can be opened directly. Read the padding and website-fingerprinting canon
(Dyer on coarse features defeating naive padding, FRONT and Tamaraw as the two defences everyone
measures against, NetShaper, Maybenot) and write a one-page summary of what each actually claims.

There are no DAITA papers to read. That absence is the finding — see Gaps below.

**November** — reproduce a published baseline. The candidate is `smith2021quicage`: about
117,000 QUIC and TCP traces, released with code. It is the only large public dataset that is
actually QUIC rather than Tor. `siby2023quic` is the closest work to this project but ships no
code and no data, so it cannot be reproduced; `zhan2021earlyquic` ships nothing either.

**December** — reduced month, two jobs. Re-evaluate the November result with deduplicated,
time-split data; a lot of published accuracy here is inflated by leaky splits, so this doubles as a
methods chapter and a check that the pipeline is sound, and `deng2025realistic` supplies the axes.
Then the capture pipeline end to end: dumpcap to features to classifier on my own hardware, with
small first captures of generated traffic.

**January 2027** — first version of the Rust flow-feature extractor, validated field by
field against tshark. Python has nfstream; Rust has nothing comparable, so this is a
reusable output as well as a tool.

**February** — collect my own dataset: scripted browsing over TLS and QUIC, captured off
a switch mirror port so the observer is genuinely passive. Train the attacker on it and
report accuracy with bootstrap intervals over groups rather than over traces.

**March** — DAITA on and off, over a real VPN path, against my own attacker. Measure the
accuracy drop and the bandwidth and latency it costs. Five things have to hold for this to be a
contribution rather than a repeat, each one an axis the only existing measurement did not cover:
many websites rather than one, Linux rather than Windows, the current DAITA version, **accuracy
reported as well as cost**, and the adversary retrained against each configuration.

**April** — my own padding strategies on Maybenot. Begin the cost curve: leakage against
overhead, several configurations, adversary retrained for each.

**May** — reduced month, exams assumed. Finish the remaining configurations and complete
the cost curve.

**June** — one extension (see below). Start writing: methods and results chapters first,
while the experiments are fresh.

**July** — full draft to Farrell. Fill gaps the draft exposes.

**August** — revise, build the demo, submit.

## The gap this fills

Stated precisely, because the whole project rests on it and a loose version will not survive a viva.

The only public measurement of DAITA is `pulls2024daitaeval`, a June 2024 blog post by Tobias
Pulls, who wrote Maybenot and states on that page that he works with Mullvad on DAITA. It is
therefore not independent. It covers **one website** (kau.se, chosen to avoid CDN variability),
from **Windows clients**, across eight servers, against **DAITA v1**, over 80,000 traces. It
reports cost — around 2–4 MiB and 1–3 seconds per website visit — and publishes **no attack
accuracy figures**. Mullvad's own commissioned GotaTun audit, by Assured Security Consultants,
explicitly excluded the DAITA code. A newer DAITA version has since shipped. Consumer review sites
quote overhead percentages with no stated source.

So: no measurement of DAITA by anyone unaffiliated with Mullvad exists, and the protection it
provides has never been publicly quantified by anyone at all. Checked 2026-11-23.

## Gates

Each one is a decision point with the threshold written down before the data is collected. The
numeric threshold for a gate lives in that experiment's `README.md`, written before the experiment
runs — this table only names the decision.

Two gates where one used to be: reproducing somebody's number and re-evaluating it honestly are
separate jobs with separate failure modes, and bundling them hid the fact that the second is the
one with intellectual content.

| when | gate | if it fails |
|---|---|---|
| end Nov | a published baseline reproduces — their code, their data, their number | the methods finding becomes the first contribution and the schedule shifts right |
| mid Dec | that result survives honest re-evaluation on deduplicated, time-split data | the gap between the two numbers *is* the methods contribution |
| end Feb | my own captures reproduce published-level accuracy | simplify the capture path rather than perfecting it; fall back to public datasets |
| end Mar | DAITA produces a measurable accuracy drop | report the null honestly; the cost measurement stands on its own |
| end Apr | a defensible cost curve exists, whatever its shape | the deployment-failure analysis carries the evaluation chapter instead |

## Deliverables

**Minimum.** The attacker, evaluated honestly, plus the DAITA measurement. These two are
the dissertation.

**Extensions, in rough priority order.** My own padding strategies and their cost curve.
Whether a shaper under load leaks its own scheduling state — a defence that cannot keep
its schedule when the link is busy is leaking through the defence itself. A strongest
possible adversary that knows the padding parameters. The Rust extractor released as a
crate. A live terminal demonstrator.

## Standing commitments

- Every number comes off the wire, never from application logs.
- The failure threshold is written before the data is collected.
- A well-measured negative result is an acceptable outcome and will be reported as one.
- Re-check the literature every two months — this area moves fast and being surprised in
  the viva is avoidable.
- Any claim that nobody has done something gets written with its evidence and the date it was
  checked, in the same sentence. Negative claims rot and they drift when restated, and this one
  is load-bearing.
