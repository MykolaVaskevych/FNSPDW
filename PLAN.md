# Dissertation

**Does padding actually help?** What encrypted web traffic still reveals through packet size,
timing and direction, and what padding defences buy — measured against their cost in bandwidth
and latency.

Mykola (Nick) Vaskevych · MSc Future Networked Systems, Trinity College Dublin
Supervisor: Stephen Farrell · Submission: late August 2027

**This is the only document.** Topic, scope, schedule, the gap, how I work, the library, and every
decision that changed any of it. If something contradicts this file, this file is right. Paste this
whole file into an assistant that needs context — the last section tells it how to behave.

---

## Scope

**In.** Plain web traffic over TLS and QUIC. An attacker that classifies activity from encrypted
metadata, evaluated honestly. Padding defences: Mullvad's DAITA as a deployed example, and my own
strategies on the Maybenot framework. The cost curve of each.

**Out.** LLM traffic — dropped 2026-10-20, after Farrell asked what makes LLM traffic different
and suggested plain web traffic instead. Measured: OpenAI pads every streamed event to a constant
size with a random filler field, which closed the token-length channel I was going to attack
(`experiments/token-batching`).

That measurement is the motivation for this project rather than part of it. It does not claim the
channel is *gone*: `zhang2025netecho` reports recovering a large share of conversation content from
deployed streaming services despite that padding. Whether residual leakage survives production
padding is exactly the open question — which is the argument for measuring what deployed padding
buys, on traffic that can be collected honestly.

**Also out.** Anything needing payload decryption. Traffic from anyone who has not opted in — my
own devices only, unless ethics approval is in place first.

## The gap this fills

Stated precisely, because the whole project rests on it and a loose version will not survive a
viva. **Restate it from here, never from memory.** Checked 2026-11-24.

**There is no evaluation of DAITA against *website* fingerprinting by anyone unaffiliated with
Mullvad.** Three pieces of work exist and none of them closes that:

- **`pulls2024daitaeval`** — the only website-fingerprinting measurement. A June 2024 blog post by
  Tobias Pulls, who wrote Maybenot and states on the page that he works with Mullvad on DAITA, so
  not independent. One website (kau.se), Windows clients, eight servers, DAITA v1, 80,000 traces.
  It says DAITA "reduces the success rate of both DF and RF attacks" and costs "around 2-4 MiB of
  bandwidth overhead and 1-3 seconds of delay per website visit" — but puts no accuracy numbers in
  the text.
- **`bjorklund2025video`** — the only evaluation by authors with no stated Mullvad affiliation, and
  it is about **video**, not websites. USENIX Security 2025, honourable mention. "A brief
  experiment streaming **five videos** with and without DAITA activated": it "effectively mitigates
  the attack" but "doubles bandwidth usage at best". Their closing line is *"further research is
  required to thoroughly evaluate its efficacy"* — worth quoting, but it is a generic closing
  sentence, not a call for website-fingerprinting work specifically, and should not be oversold as
  one. `bjorklund2024thesis` is the author's MSc thesis behind it and carries the fuller version of
  the same experiment: ten minutes per service, first 100 s discarded, **no** video identified with
  DAITA on.
- **`ridderland2026mole`** — a 2026 Chalmers MSc thesis that **contradicts** the one above: "only
  78% of DAITA streams remain unidentified", which "refutes what was previously thought, that DAITA
  provided full protection". Also video. Its advisor is Odd Stranne of Mullvad VPN, so not
  independent either, and its supervisor is `bjorklund2025video`'s co-author.

On top of that, Mullvad's own commissioned GotaTun audit, by Assured Security Consultants,
**explicitly excluded the DAITA code**; a newer DAITA version has since shipped; and consumer
review sites quote overhead percentages with no stated source.

So the literature on a deployed defence consists of one vendor-adjacent blog post about websites,
one five-video preliminary test, and one thesis that disagrees with it. That is the gap, and it is
narrower and more defensible than "nobody has evaluated DAITA" — which was the wording here until
2026-11-24 and is false.

**What was searched, so the claim can be re-checked rather than trusted.** On 2026-11-23 and
2026-11-24: OpenAlex and the arXiv API by title and by author; the NDSS, PoPETs, USENIX Security
and INFOCOM proceedings listings; web search for independent DAITA evaluation, overhead and
measurement; Mullvad's own blog and help pages (both `/blog/daita-v2` and `/help/daita` 404'd, so
the current version's claims are still unverified from a primary source); and the Chalmers thesis
repository. A claimed thesis by "Henriksson & Liman" on DAITA and video fingerprinting could not be
found in any of those and should not be cited unless someone produces it. Re-check before this goes
in front of an examiner — it is a negative claim about a live product and it has already been
wrong twice.

Five axes make a new measurement a contribution rather than a repeat, each one something no
existing work covers together: **website** fingerprinting rather than video, many websites rather
than one, Linux rather than Windows, the current DAITA version, and **accuracy reported as well as
cost**, with the adversary retrained against each configuration.

## The attacker, graded by ambition

| # | capability | assessment |
|---|---|---|
| 1 | **Flow identification** — is this a web page load at all | near-certain, and survives ECH |
| 2 | **Activity classification** — page load vs video vs call vs idle | near-certain; the general task Farrell's instruction asks for |
| 3 | **Response size** — how much came back | near-free, and a real metadata leak on its own |
| 4 | **Website fingerprinting** — which site | the crowded, well-published task; the baseline to reproduce |
| 5 | **Fine-grained page fingerprinting** — which page within a site | harder, and where the recent work is heading |

Why now: as ECH hides SNI, destination-based classification degrades, which pushes observers toward
traffic-*shape* classification. The question gets more important precisely because the thing it
replaces is being fixed. ECH is Farrell's own territory.

## Why this structure

**Put the robust thing at the foundation and the ambitious thing at the top.**

Rungs 1–4 are near-certain; my own strategies beating the published ones are the gamble. So the
spine is the honestly-evaluated attacker plus the DAITA measurement, with my own Maybenot
strategies and the full cost curve as the final chapter. Structured that way, failing to beat
`khajavi2026lightening` costs one chapter. Structured the other way round — my own defence as the
spine — the same failure costs the dissertation.

This is what Farrell's generality instruction buys. Treat it as de-risking, not as dilution.

Corollary: **make the deliverable something that cannot fail.** If what I am graded on is a
QUIC-aware feature extractor, a rigorous evaluation harness and an honest cost-curve methodology,
then the tool exists and the method is sound whatever the numbers say. A null result measured well
is a pass; a null result measured badly is a fail. Headline findings are upside, not foundation.

## Time available

Taught modules are heavier this semester and lighten from January, so the rest of this year is
part-time research and the real work starts in the new year.

Exam dates are now published, and they are not what this plan originally assumed. From Trinity's
2026-27 academic year calendar: **Semester 1 assessment 10-22 December 2026**; Hilary teaching ends
**9 April 2027**; **Semester 2 assessment 19-30 April 2027**; marking and results to 21 May, with
research time opening up from late May.

So the reduced months are **December and April** — not December and May, which is what this file
said until 2026-11-24. April had been given the cost-curve work and an end-of-month gate, both of
which sat inside the exam period. They moved to May.

Rough effort: ~10 h/week to December, ~20 h/week January to March, reduced through April,
full-time from May.

## Month by month

**October–November 2026** — agree this plan. Make the repo readable: LaTeX and built PDF committed
where they can be opened directly. Read the canon — Dyer on coarse features defeating naive
padding, FRONT and Tamaraw as the two defences everyone measures against, NetShaper, Maybenot — and
write a one-page summary of what each actually claims. There are no DAITA papers to read; that
absence is the finding.

**November** — reproduce a published baseline: `smith2021quicage`, about 117,000 QUIC and TCP
traces with code, the only large public dataset that is actually QUIC rather than Tor.

**The download is 871 MB, not 30 GB**, and that is what makes the gate reachable. The processed
`quic-wf-core.tgz` has the open-world dataset in HDF5 with labels, sizes and timestamps. The raw
tar is ~30 GB in six parts and is not needed. Both the polybox links in the README are dead; the
live copy is the ETH Research Collection record behind `doi.org/10.3929/ethz-b-000456101`, fetched
through the DSpace content endpoint (verified 2026-11-24 by pulling bytes and checking the gzip
magic, not by trusting the link):

```
curl -L -o quic-wf-core.tgz \
  https://www.research-collection.ethz.ch/server/api/core/bitstreams/ab483811-4adf-4967-9737-43044ca3a149/content
```

There is also a 7.25 GB VM image in the same record with code and data preloaded, if setup turns
out to be the slow part. Compute is modest: the authors ran each experiment on 2-4 cores with 6 GB
per core.

`siby2023quic` is the closer work and **does** ship an artifact — `spring-epfl/quic-wf-defenses`,
with capture scripts, feature extraction, a random-forest attack for both adversary models, both
defence setups and a Dockerfile. The reason not to use it as the November baseline is narrower:
**its dataset link is dead** (SWITCHDrive, 404 as of 2026-11-24) and the repo carries no licence,
so reproducing it means collecting the captures first, which is weeks rather than days. Worth
revisiting in February, when captures are the job anyway. `zhan2021earlyquic` ships nothing.

**December** — exams run 10-22 December, so this is a reduced month with the real work in its first
week. By 9 December: re-evaluate the November result with deduplicated, time-split data. A lot of
published accuracy here is inflated by leaky splits, so this doubles as a methods chapter and a
check that the pipeline is sound, and `deng2025realistic` supplies the axes. After exams, if
anything is left: the capture pipeline end to end, dumpcap to features to classifier on my own
hardware.

**January 2027** — first version of the Rust flow-feature extractor, validated field by field
against tshark. Python has nfstream; Rust has nothing comparable, so this is a reusable output as
well as a tool. **I write this one myself, without AI.**

**February** — collect my own dataset: scripted browsing over TLS and QUIC, captured off a switch
mirror port so the observer is genuinely passive. Train the attacker on it and report accuracy with
bootstrap intervals over groups rather than over traces. `pulls2024daitaeval`'s method is the
template: VMs, Selenium, tshark, tens of thousands of traces.

**March** — DAITA on and off, over a real VPN path, against my own attacker. Measure the accuracy
drop and the bandwidth and latency it costs. Five things have to hold for this to be a contribution
rather than a repeat, each one an axis the only existing measurement did not cover: many websites
rather than one, Linux rather than Windows, the current DAITA version, **accuracy reported as well
as cost**, and the adversary retrained against each configuration.

**April** — reduced month: teaching ends 9 April and Semester 2 exams run 19-30 April. Keep it
light and low-risk — write up the March DAITA measurement while it is fresh, and get the Maybenot
strategies written and compiling, without depending on results landing this month.

**May** — the first full-time month. My own padding strategies on Maybenot, and the cost curve:
leakage against overhead, several configurations, adversary retrained for each.

**June** — one extension. Keep writing: methods and results chapters first, while fresh.

**July** — full draft to Farrell. Fill gaps the draft exposes.

**August** — revise, build the demo, submit.

## Gates

Each one is a decision point with the threshold written down before the data is collected. The
numeric threshold lives in that experiment's `README.md`, written before the experiment runs — this
table only names the decision.

| when | gate | if it fails |
|---|---|---|
| end Nov | a published baseline reproduces — their code, their data, their number | the methods finding becomes the first contribution and the schedule shifts right |
| **9 Dec** | that result survives honest re-evaluation on deduplicated, time-split data | slips to early January, and that is acceptable — Semester 1 assessment runs 10-22 December |
| end Feb | my own captures reproduce published-level accuracy | simplify the capture path rather than perfecting it; fall back to public datasets |
| end Mar | DAITA produces a measurable accuracy drop | report the null honestly; the cost measurement stands on its own |
| end May | a defensible cost curve exists, whatever its shape | the deployment-failure analysis carries the evaluation chapter instead |

Reproducing somebody's number and re-evaluating it honestly are separate jobs with separate failure
modes. Bundling them hid the fact that the second is the one with intellectual content.

The second gate sits on **9 December**, the day before Semester 1 assessment opens, not mid-month:
it had been put inside the exam period, the same error that had the cost curve inside the April
exams. The re-evaluation reuses the November dataset and codebase and only changes the splits, so
two weeks is plausible — but the slip to January is pre-registered rather than improvised.

## If a gate fails

"Encryption holds and I found nothing" is the least likely outcome: traffic analysis against
encrypted traffic has decades of positive results, and rungs 1–3 are close to guaranteed. The
realistic failure modes are narrower, and each has a fallback that reuses the same apparatus.

| failure mode | fallback, and why it still counts |
|---|---|
| The published baseline will not reproduce | **That is the finding**, and `deng2025realistic` says to expect it. A documented failure to reproduce, with the reason, is a methods contribution. Fall back to a second baseline, not a second topic. |
| The defence is cheap and effective | Contribution becomes the cost curve itself, plus deployment-failure analysis. A defence that holds in the lab and breaks under load, disconnection or slow clients is a real finding. The inherited pilot saw failures of this kind, but its numbers are not citable, so treat that as a reason to look rather than as evidence. |
| DAITA works well | The first *website*-fingerprinting evaluation of it by anyone unaffiliated with Mullvad still stands. `bjorklund2025video` called for exactly that, and `ridderland2026mole` already found it is not airtight for video — 78 % of streams unidentified, not 100 %. |
| No queueing channel under load | Report the negative with the conditions under which it would appear (loaded relay, shared link, contended uplink). That chapter becomes more cost-curve configurations instead. |
| Someone publishes it first | Independent reproduction on real hardware still stands and is undervalued. Re-check the literature every two months so it is never a surprise in the viva. |
| The testbed eats the year | Hard stop: if it is not producing clean captures by a pre-set date, simplify rather than perfect. |
| Everything fails | Escape hatch that reuses the whole pipeline: *what does ECH actually hide in practice* — deployment measurement and residual leakage. Same capture and feature code, Farrell's own territory. |

**The device that makes null results count: pre-register the failure threshold.** Write down what
result would mean the hypothesis is rejected *before* collecting data. An unregistered null result
reads as incompetence; a pre-registered one reads as science. Single highest-leverage habit here.

Decide now, not in month nine, that a well-measured negative is acceptable — otherwise the project
will quietly tempt me into overclaiming.

## Deliverables

**Minimum.** The attacker, evaluated honestly, plus the DAITA measurement. These two are the
dissertation.

**Extensions, in rough priority order.** My own padding strategies and their cost curve. The
queueing channel. A strongest-possible adversary that knows the padding parameters. The Rust
extractor released as a crate. A live terminal demonstrator.

**The queueing channel.** Any shaper that must emit on a fixed schedule while a variable-rate
source feeds it leaks its own scheduling state. A DAITA-shaped tunnel on a loaded relay has the
problem; so does a shaper in front of any contended backend. Not LLM-specific, which is why it
satisfies the generality requirement while staying the most original idea available.

## Standing commitments

- Every number comes off the wire, never from application logs.
- The failure threshold is written before the data is collected.
- A well-measured negative result is an acceptable outcome and will be reported as one.
- Re-check the literature every two months. Next: January 2027.
- Any claim that nobody has done something gets written with its evidence and the date it was
  checked, in the same sentence. Negative claims rot, and they drift when restated.

## How I work

- I propose, Nick executes. Commands are given to paste, not silently run.
- Every number comes with the command that produced it. Nothing quoted from memory.
- No code lands unread. Small diffs, one file at a time.
- Literature: DOI or arXiv ID, fetched and quoted. "Unsure" is said out loud.
- Time-box the testbed. A minimal real path producing one honest number beats a perfect lab.

**Commits** (this repo and `paper/`). The message is always `update`. One line, no body, no
exceptions, and never a mention of Claude or AI — no `Co-Authored-By`, no "Generated with". Set
2026-11-24, replacing the previous rule of asking for a message every time.

**Code.** Comment to carry domain knowledge, not syntax — `TCP_NODELAY` earns a note about Nagle,
`rows = []` earns nothing. Every file opens with a docstring saying what it does and why it exists.
No classes, abstractions or extra files unless they pay for themselves. Reuse over duplication, but
no shared package until two experiments genuinely need the same code. Python always via `uv`.

**Languages.** Rust for the flow-feature extractor, the shaping engine (it needs real async and
backpressure) and the live detector. Python for classifiers, statistics and plots. ML for the
activity classifier and possibly adversarial training of a defence against a learned attacker —
not ML for its own sake.

**Experiments.** One directory each, nothing in the repo root. `README.md` saying what it tests,
why, and the failure threshold — **written before it runs**. `run.py`, and its own `out/`, which is
not committed.

**Captures.** No personal traffic, ever; only traffic the lab generated on purpose. Always capture
with a filter pinned to the lab port or host. Need realistic traffic I cannot generate? Use a
public dataset, not my own browsing. Captures and datasets stay out of git.

**The paper** lives in the `paper/` submodule and has its own rules in `paper/CLAUDE.md` — read
them before touching anything there. No comments in LaTeX unless I ask.

**Bibliography.** Zotero owns it. The `disertation` collection is the source of truth and Better
BibTeX auto-exports it to `paper/src/bibs/ref.bib`, which is what `main.tex` reads. That file is
machine-written — never hand-edit it; anything typed in is lost on the next export. Add a paper in
Zotero and the export follows within seconds. The auto-export is registered **non-recursively** on
`disertation`, so a paper filed only in a subcollection would vanish from the bibliography: when
sorting, **add, never move**.

## Testbed, and facts to regenerate rather than record

Durable roles — the models are not: 4090 PC = server · TrueNAS box = client · laptop = observer on
the mirror port · Omada L2+ managed switch = port mirroring · OpenWrt router.

```
tooling       tshark -v | head -1 ; uv --version ; getcap /usr/bin/dumpcap
capture OK?   groups | tr ' ' '\n' | grep wireshark
layout        git ls-files ; find experiments -maxdepth 2
bib in step?  grep -c '^@' paper/src/bibs/ref.bib   # compare with Zotero's item count
secrets       notes/OP.md
```

## The library

Zotero holds it, in the `disertation` collection, sorted into four subcollections:

| | holds |
|---|---|
| `1 intro and basics` | foundations and the motivation story. Age does not matter |
| `2 learn and try` | read it, then reproduce it. Mechanics worth getting hands on |
| `3 needed for experiments` | datasets, frameworks, cost-curve method. The working set |
| `4 state of the art` | 2026 work to argue with and not be scooped by |

Every entry was verified against OpenAlex, the arXiv API, or the publisher's own proceedings
listing. Nothing from memory, nothing from a GitHub reading list. Reading order and the four fields
to fill per paper: `literature/summaries.md`.

The sort is done except for the newest few, which carry a `sub:` tag — filter on the tag and drag.
Zotero's connector can add an item to the selected collection but cannot move one, which is why
sorting is manual.

**1 intro and basics** — `dyer2012peekaboo` `juarez2014critical` `sirinam2018deep` `wright2008spot`
`zhang2011predictive` `askarov2010predictive` `weiss2024prompt` `zhang2025netecho`

**2 learn and try** — `smith2021quicage` `zhan2021earlyquic` `jolles2026nym` `deng2026drift`
`vanderlinden2026tcpts`

**3 needed for experiments** — `siby2023quic` `gong2020front` `cai2014tamaraw` `smith2022qcsd`
`khajavi2026lightening` `cebere2026http2` `deng2025realistic` `yu2026proxydrift`
`jansen2024genuine` `jansen2026cellshift` `sabzi2024netshaper` `pulls2023maybenot`
`pulls2024daitaeval` `bjorklund2025video` `bjorklund2024thesis` `ridderland2026mole`
`gahtan2024visquic` `witwer2026dodge` `hasselquist2024raising`

**4 state of the art** — `pulls2026ephemeral` `song2026llmwf` `wang2026cease` `zhao2026llmwf`
`cheng2026star`

### What the recent half is for

- **`siby2023quic`** — Siby, Barman and Troncoso with Cloudflare. The question, already asked for
  QUIC: padding alone is not sufficient. The closest published work to this dissertation. Ships
  code and Docker at `spring-epfl/quic-wf-defenses`; its dataset link is dead. Its numbers, stated
  carefully because the paper's own notation is loose: the undefended random forest scores
  **F1 95.8** on MAIN. FRONT at its heaviest setting brings that to **31.4 at an overhead of
  2.31** — the paper calls that a "≈ 70 % F1-score drop", which is the *relative* fall, not 70
  points. That is on top of a mean 612 kB per trace already spent hiding local and global features.
  And in the NetFlow setting most of the privacy gain came from the observer's own **sampling**
  rather than the padding: at NetFlow 1 %, 54.1 points of F1 lost to sampling against 20.1 to
  padding, from the same 95.8 baseline.
- **`pulls2024daitaeval`** — grey literature, required reading, ten minutes. The only DAITA
  measurement against *website* fingerprinting, and the thing March has to improve on.
- **`bjorklund2025video`**, **`bjorklund2024thesis`** and **`ridderland2026mole`** — the only other
  DAITA evaluations, all three about video, and they disagree. Björklund found no video identified
  with DAITA on; Ridderland and Tagra found 78 % unidentified, i.e. roughly one in five still
  identified, and say so explicitly refutes the earlier "full protection" reading. Read all three
  before the March measurement — they are the nearest thing to prior art, and the disagreement
  between them is itself worth a paragraph.
- **`gong2020front`** and **`cai2014tamaraw`** — FRONT and Tamaraw, the two defences everyone
  measures against. Prerequisites, not background: reading the 2026 papers without these is reading
  arguments without the claims. Cai also derives a lower bound on the bandwidth cost of *any*
  defence at a given security level — the theoretical floor under my cost curve.
- **`smith2022qcsd`** and **`smith2021quicage`** — Smith's QUIC pair. QCSD implements FRONT and
  Tamaraw client-side over the QUIC PADDING frame, which is the nearest existing thing to what I
  would build. Siby positions itself directly against it.
- **`khajavi2026lightening`** — NDSS 2026. A *provable* defence at *lower* overhead. The number a
  new cost curve has to beat.
- **`cebere2026http2`** — CISPA, September 2026. Reproduces FRONT, Tamaraw and ALPaCA using
  HTTP/2's own features, then measures leakage against overhead. A cost curve that already exists.
- **`wang2026cease`** — NDSS 2026. Efficient defence by iteratively minimising mutual information.
- **`hasselquist2024raising`** — what honest overhead looks like when published: constant-rate
  defence at 462 % receive bandwidth. Useful for knowing when a cost is absurd.

The methods spine — why published accuracy does not survive contact with reality:

- **`deng2025realistic`** — the first systematic evaluation of existing attacks across defences,
  traffic drift, multi-tab, early-stage, open-world and few-shot *at once*. Attacks scoring above
  90 % in isolation fall over when the conditions combine. This is the mid-December gate, already
  framed by someone else. Use their axes; they ship no code.
- **`yu2026proxydrift`** — the same website looks different through a different proxy protocol, and
  models trained on one fail on another. That confound sits inside the March measurement, where
  DAITA on and off both mean traffic through a VPN.
- **`deng2026drift`** — NDSS 2026. Traffic drift degrades attacks over time.
- **`jansen2026cellshift`** and **`jansen2024genuine`** — real traces versus lab traces, and how to
  make lab traces behave. Read with `juarez2014critical`.

Worth watching on the attack side:

- **`cheng2026star`** — INFOCOM 2026. Zero-shot: identifies sites with no per-site training traces,
  through ECH and encrypted DNS, at 87.9 % top-1 on 1,600 unseen sites. If an attacker needs no
  training data per target, "nobody could collect traces for my site" stops being a defence.

### Code and data

Links came out of the PDFs themselves, not a search engine, and each returned HTTP 200 on
2026-11-23. To redo it: pull `github.com` and `doi.org/10.5281` strings out of the PDFs in Zotero
storage, keep the ones next to an availability sentence, and curl each. Repos get renamed, so
follow redirects rather than trusting the string in the paper.

**Start here.** `jpcsmith/wf-in-the-age-of-quic` — ~117k QUIC *and* TCP traces with code, the only
large public dataset that is QUIC. `websitefingerprinting/WebsiteFingerprinting` — FRONT's code
plus the attacks it was evaluated against, plus datasets: a defence and an attacker in one harness.
`deep-fingerprinting/df` — the DF dataset, Tor not QUIC, but the field's common denominator;
`wang2026cease` runs its 2026 experiments on it. `FIND-Lab/Website-Fingerprinting-Library` — WFlib,
the harness the recent work builds on (moved from `Xinhao-Deng/`). `jpcsmith/neqo-qcsd` — a working
client-side QUIC defence. `robshahla/VisQUIC` — QUIC pcaps with TLS keys.

| paper | code | data | where |
|---|---|---|---|
| `sirinam2018deep` | yes | yes | `deep-fingerprinting/df` |
| `smith2021quicage` | yes | yes, 871 MB processed / ~30 GB raw | `jpcsmith/wf-in-the-age-of-quic` + `doi.org/10.3929/ethz-b-000456101` (README's polybox links are dead) |
| `siby2023quic` | yes, + Docker | **link dead** | `spring-epfl/quic-wf-defenses` |
| `bjorklund2025video` | yes | yes, incl. DAITA pcaps | `trustcom/endangered-privacy` + `doi.org/10.5281/zenodo.15051891` |
| `bjorklund2024thesis` | — | — | thesis only, `odr.chalmers.se` |
| `ridderland2026mole` | — | — | thesis only, `odr.chalmers.se` |
| `smith2022qcsd` | yes | — | `jpcsmith/neqo-qcsd` |
| `gong2020front` | yes | yes | `websitefingerprinting/WebsiteFingerprinting` |
| `cai2014tamaraw` | yes | yes | `crysp.uwaterloo.ca/software/` |
| `khajavi2026lightening` | yes | — | `khashayarkhaj/Adaptive-Tamaraw` |
| `cebere2026http2` | yes | — | `bcebere/Understanding-the-Privacy-Preserving-Potential-of-HTTP2-Against-Webpage-Fingerprinting` |
| `deng2026drift` | yes | yes | `Xinhao-Deng/Adaptive-WF-Attack` |
| `yu2026proxydrift` | yes | yes, with key material | `wesly2000/PA3` |
| `jolles2026nym` | yes | yes | `spring-epfl/WF4NYM-artifacts` |
| `jansen2026cellshift` | yes, Rust | yes | `robgjansen/cellshift` + `doi.org/10.5281/zenodo.15863906` |
| `pulls2026ephemeral` | yes | yes | `maybenot-io/popets-2026.1-ephemeral-defs-paper-artifacts` |
| `pulls2023maybenot` | the framework | — | `maybenot-io/maybenot` |
| `witwer2026dodge` | yes | — | `trafnex/dodge-framework` |
| `hasselquist2024raising` | yes, incl. reimplementations | — | `trafnex/raising-the-bar` |
| `cheng2026star` | yes | STAR-200K | `2654400439/STAR-Website-Fingerprinting` |
| `vanderlinden2026tcpts` | — | yes | `doi.org/10.5281/zenodo.17098889` |
| `gahtan2024visquic` | yes | yes, pcaps + keys | `robshahla/VisQUIC` |
| `weiss2024prompt` | yes | — | `royweiss1/GPT_Keylogger` |

**VisQUIC is downloadable now, no request needed** — two public Dropbox folders linked from the
repo. Take the `VisQUIC*.zip` archives: PCAP traces each with a matching `.key` file, so
ground-truth labels come off the wire. Skip `rgb_images*.zip` — those are the authors' own visual
feature encoding, and building features is the point of the January extractor. Not every trace
decrypts; some were captured under a key they do not ship.

**Before planning around any of them:**

- **`siby2023quic` ships code but not data.** `spring-epfl/quic-wf-defenses` has the capture
  scripts, the attack, both defences and a Dockerfile; the SWITCHDrive dataset link 404s and there
  is no licence file. Nothing about the artifact appears in the PDF — PoPETs links artifacts from
  the paper's web page — which is why an audit that only reads PDFs misses it. **Check the
  publisher's artifact link, not just the paper.**
- **`zhan2021earlyquic` ships nothing.** No repository, no availability statement.
- **`deng2025realistic` ships nothing.** Its axes are reusable; its harness does not exist.
- **`pulls2023maybenot` has two versions.** arXiv 2304.09510v1 (April 2023) is the WPES 2023 paper
  the citekey refers to; v2 (September 2024) documents *framework version 2*, which is what to read
  before writing strategies in April. The Zotero attachment is v1 so it matches the citation.
- **`wang2026cease` contradicts itself** — "code will be made available shortly" in one sentence, a
  live URL in another. Check the repo has content before relying on it.
- **`jansen2024genuine` is request-only.** GTT23, 13M+ genuine Tor traces. The one dataset with
  real lead time, so ask early.
- **`sabzi2024netshaper` has no artifact link in the paper**, only its dependencies. Try the USENIX
  artifact appendix.
- **`hasselquist2024raising` reimplemented three attacks** because the authors would not share
  code, and published the reimplementations. Useful, and a warning about what "we compare against
  prior work" can quietly mean.

### Housekeeping

- `zhao2026llmwf` is the only paper with no PDF. Paywalled at the ACM, no preprint under that title
  or any other from that group. TCD proxy.
- Four PDFs sit in `~/Zotero/fnspdw-import/` waiting to be dragged onto their items:
  `zhan2021earlyquic`, `wright2008spot`, `pulls2023maybenot`, `zhang2011predictive`. The connector
  can attach a PDF to a new item but not to an existing one, so it is a drag each.
- `cebere2026http2` is typed `@inproceedings` but is a preprint, which produces an empty-booktitle
  warning. Change the Zotero item type to Preprint.
- NDSS, PoPETs and INFOCOM are where this work lands and search engines rank them badly, so read
  the proceedings listings directly. Searching an author's recent arXiv output beats searching a
  title — three papers here came from one such listing and none had surfaced in a title search.

## Open questions

- Does NetShaper's threat model exclude colocation and shared-link leakage? Answer from the paper,
  not the abstract.
- What protocol real browsers negotiate for the February corpus (HTTP/2 over TLS versus HTTP/3 over
  QUIC)? The split decides what fraction of the dataset is actually QUIC.

## Decisions — append only

Newest last. One entry per decision that changed the topic, the scope or a load-bearing claim, with
the date and what it supersedes. **Reverse a decision, add a line here in the same sitting.**

This section exists because the repo once misled an assistant, which then misled me: a file still
described a project that had been abandoned two months earlier, and nothing recorded the
abandonment. A reversal that leaves no trace reads as the current plan to whoever finds the stale
file first.

**2026-09 (to 19 Sept)** — Dropped the original QUIC/padding topic as too close to existing
application-fingerprinting work; moved to side channels in LLM streaming. A prototype gave 0.81
undefended accuracy, 0.43 with shaping, at roughly 14× bandwidth and 3.9× latency, and found four
deployment failures; the novel one was cover traffic leaking the server's queue delay under
concurrency. *Superseded 2026-10-20.*


**2026-09** — Starter pack declared QUIC and Maybenot "permanently out of scope". It was
AI-generated and deleted exactly what the supervisor had asked for. *Reversed; both are central.
It is not authority.*


**2026-09-22** — Title agreed: *Network Side-Channel Leakage in Encrypted LLM Streaming Traffic*.
Farrell then asked what makes LLM traffic any different and how it would be generated, and
suggested plain web traffic instead. *Superseded 2026-10-20.*


**2026-10-01** — Measured that OpenAI sends one token per SSE event but pads every event to a
constant size with an `obfuscation` field whose length compensates for the token. Against
gpt-4.1-nano, `"Hi"` + 5 pad and `"!"` + 6 pad both give 312 bytes. Residual leaks: the terminal
event is 296 bytes not 312, and event count still reveals token count. *This is the measurement
that caused the 2026-10-20 scope change; it was dated 2026-11-03 here until 2026-11-24, which put
the effect two weeks before its cause.*


**2026-10-20** — **LLM dropped. Topic returned to Farrell's suggestion: does padding actually
help, on plain TLS and QUIC web traffic.** Reason: `experiments/token-batching` measured that
OpenAI pads every streamed event to a constant size, closing the channel the attack depended on.
The measurement is kept as motivation, not as a chapter. *Supersedes the 2026-09 topic, the
2026-09-22 title, and the leak-granularity framing.*


**2026-11-03** — Zotero's `disertation` collection became the single source of truth for
references, auto-exported by Better BibTeX to `paper/src/bibs/ref.bib`.


**2026-11-03** — All inherited citations resolved. NetShaper, Dyer, Askarov/Zhang (2010 and 2011),
Wright, Whisper Leak and Weiss all real. **NetEcho is real** — calling it plausibly fabricated was
wrong. **PromptEcho does not resolve**; dropped. Three entries had authors missing.


**2026-11-20** — Closed as out of scope, kept for the record: whether Anthropic pads the same way;
whether self-hosted servers pad at all; whether OpenAI's padding survives to the wire given events
arrive in pairs ~17 µs apart; whether anyone has done the LLM token-length channel over QUIC. All
interesting, none of them this dissertation. *Do not reopen without Farrell agreeing first.*


**2026-11-23** — DAITA gap claim tightened. It had been "nobody has independently evaluated DAITA",
which is too strong — `pulls2024daitaeval` exists. The precise version is above and is *stronger*,
because it names the five axes the existing measurement did not cover.


**2026-11-23** — End-November gate split in two: reproduce by end November, survive honest
re-evaluation by mid-December. *The reason recorded here for choosing the baseline was wrong — see
2026-11-24.*


**2026-11-24** — **`siby2023quic` does ship an artifact.** `spring-epfl/quic-wf-defenses`: capture
scripts, feature extraction, a random-forest attack for both adversary models, both defence setups,
a Dockerfile. This file had said it "ships nothing" in four places. The cause of the error: the
artifact audit extracted links from the PDFs only, and PoPETs links artifacts from the paper's web
page, so nothing about it appears in the paper. **Audit the publisher's artifact link too.**
`smith2021quicage` stays the November baseline, for the narrower and verified reason that Siby's
SWITCHDrive dataset link 404s and the repo has no licence, so running it means capturing first.


**2026-11-24** — **DAITA gap claim corrected and narrowed.** It had read "the protection it
provides has never been publicly quantified by anyone at all", which is false. `bjorklund2025video`
(USENIX Security 2025, honourable mention, no stated Mullvad affiliation) evaluated DAITA on five
videos and `ridderland2026mole` (Chalmers MSc 2026, Mullvad advisor) found 78 % of DAITA streams
unidentified, contradicting it. Both are video fingerprinting. The claim is now "no evaluation
against *website* fingerprinting by anyone unaffiliated with Mullvad", which is narrower, citable,
and strengthened by `bjorklund2025video` asking for exactly this work. Also corrected:
`pulls2024daitaeval` does state DAITA reduces DF and RF success rates, it just prints no numbers in
the text.


**2026-11-24** — **Exam dates published; April is a reduced month, not May.** Semester 2 assessment
is 19-30 April 2027 and Hilary teaching ends 9 April. The cost-curve work and the end-of-month gate
had been put in April, inside the exam period; both moved to May. Semester 1 assessment is 10-22
December 2026, which December already allowed for.


**2026-11-24** — Numbers in the `siby2023quic` entry corrected. The undefended random forest scores
F1 95.8; FRONT's heaviest setting gives 31.4 at overhead 2.31, and the paper's "≈ 70 % drop" is
relative, not 70 points. The sampling-versus-padding figures are F1 points off that 95.8 baseline,
not percentages. Also: the fallback table had cited the inherited pilot's failures as evidence,
which contradicts the pilot's own README saying its numbers are not citable.


**2026-11-24** — Second review of the corrected gap claim, by another assistant. Four findings
held. The **mid-December gate was inside Semester 1 assessment** (10-22 December) — the same error
just fixed for April — and moved to 9 December with a pre-registered slip to January. The claim
that `bjorklund2025video` "asks for your work by name" was an **overstatement**: its closing line
is generic and is now quoted as such. The gap claim now names what was searched and when, per this
file's own rule. A thesis it cited as "Henriksson & Liman, *Evaluating VPN Defenses Against Video
Fingerprinting*" **could not be found** in OpenAlex, arXiv, web search or the Chalmers repository;
the examiner and supervisor names it gave belong to `bjorklund2024thesis`, which is real and has
now been added. `ridderland2026mole` was verified correct from its own title page. Also verified:
Siby's SWITCHDrive link genuinely 404s with a browser user-agent while the site root returns 200,
so it is not a bot block.

**2026-11-24** — **The November gate is reachable.** `smith2021quicage`'s processed dataset is
**871 MB**, not the ~30 GB raw set, and both polybox links in its README are dead. The live copy is
the ETH Research Collection record, verified by range-fetching bytes and confirming gzip magic. The
exact command is in the November entry above.

**2026-11-24** — Collapsed `PLAN.md`, `notes/PROJECT.md`, `DECISIONS.md` and `CONTEXT.md` into this
one file. Four documents describing one project is how the drift started; nothing was lost in the
merge. `literature/summaries.md` stays separate because it is a workspace I write in, not reference.

## Briefing an assistant that cannot read this repo

Paste this whole file, then say which paper or which draft. Everything below applies to you.

**Be a reading partner, not a ghostwriter.** This is an examined dissertation.

- Explain what I say I do not follow. Derivations, threat models, why a metric was chosen.
- Quiz me. After I write something, ask what would have to be true for it to be wrong.
- Check my notes against the paper and say where I have overstated.
- Pull out exact numbers with the table or section they came from, so I can verify them.
- Ask questions rather than filling things in. If I explicitly ask for a draft, say plainly that it
  is a draft for me to rewrite in my own words.
- **Never rewrite my prose.** Comment on it; do not silently improve, reword or fix my grammar.
- **The Rust flow-feature extractor is mine, written without AI.** Do not write it or draft it.
  Offer to help validate it against `tshark` instead.

**Hard rules.**

- **Never invent a citation.** No fabricated titles, authors, years, venues or DOIs. If you are not
  certain a paper exists, say so and stop.
- Verify against **OpenAlex, the arXiv API, or the publisher**. DBLP blocks scripts with bot
  protection and Google Scholar rate-limits immediately; neither is usable.
- Any claim that nobody has done something carries its evidence and check-date in the same sentence.
- Say "I do not know" rather than guessing. A confident wrong answer costs me more than a gap.
- A GitHub "awesome list" is not a source. NDSS, PoPETs, USENIX Security, INFOCOM, CCS and IEEE S&P
  are.

**Notes format — four fields per paper, every time.** *Claims* — what it says it achieved, in its
own terms. *Measured on* — dataset, how many sites, how many traces, protocol, open or closed
world. *Cost reported* — bandwidth and latency overhead, or *none reported*. *To reproduce* — is
the code public, is the data public, what is missing. Field 3 becomes the comparison table in my
results chapter; field 4 decides which baseline I attempt. Those two matter more than good prose.

**How I check you.** Any citation, in one command:

```
curl -s "https://api.openalex.org/works/doi:<DOI>" | head -c 400
curl -sG --data-urlencode 'id_list=<ARXIV_ID>' "https://export.arxiv.org/api/query"
```

If a paper you name does not come back from either, you made it up. Say so first.
