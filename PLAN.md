# Dissertation plan

**Does padding actually help?** What encrypted web traffic still reveals through packet
size, timing and direction, and what padding defences buy — measured against their cost
in bandwidth and latency.

Mykola (Nick) Vaskevych · MSc Future Networked Systems · Supervisor: Stephen Farrell
Submission: late August 2027

## Scope

**In.** Plain web traffic over TLS and QUIC. An attacker that classifies activity from
encrypted metadata, evaluated honestly. Padding defences: Mullvad's DAITA as a deployed
example, and my own strategies on the Maybenot framework. The cost curve of each.

**Out.** LLM traffic — checked in October and dropped. OpenAI already pads every streamed
event to a constant size with a random filler field, so there is nothing left to recover.
That result is the motivation for this project rather than part of it: padding is being
deployed in production, and the question is whether it works.

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
(Dyer et al. on coarse features defeating naive padding, NetShaper, the Maybenot and DAITA
papers) and write a one-page summary of what each actually claims.

**November** — reproduce a published baseline on a public QUIC or web-fingerprinting
dataset. Then re-evaluate the same result with deduplicated, time-split data. Recent work
suggests a lot of published accuracy in this area is inflated by leaky splits, so this
doubles as a methods chapter and a check that my pipeline is sound.

**December** — reduced month. Capture pipeline end to end: dumpcap to features to
classifier, running on my own hardware. Small first captures of generated traffic.

**January 2027** — first version of the Rust flow-feature extractor, validated field by
field against tshark. Python has nfstream; Rust has nothing comparable, so this is a
reusable output as well as a tool.

**February** — collect my own dataset: scripted browsing over TLS and QUIC, captured off
a switch mirror port so the observer is genuinely passive. Train the attacker on it and
report accuracy with bootstrap intervals over groups rather than over traces.

**March** — DAITA on and off, over a real VPN path, against my own attacker. Measure the
accuracy drop and the bandwidth and latency it costs.

**April** — my own padding strategies on Maybenot. Begin the cost curve: leakage against
overhead, several configurations, adversary retrained for each.

**May** — reduced month, exams assumed. Finish the remaining configurations and complete
the cost curve.

**June** — one extension (see below). Start writing: methods and results chapters first,
while the experiments are fresh.

**July** — full draft to Farrell. Fill gaps the draft exposes.

**August** — revise, build the demo, submit.

## Gates

Each one is a decision point with the threshold written down before the data is collected.

| when | gate | if it fails |
|---|---|---|
| end Nov | a published baseline reproduces, and survives honest re-evaluation | the methods finding becomes the first contribution and the schedule shifts right |
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
