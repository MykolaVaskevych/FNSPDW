# Literature

**Zotero holds the library. This file is for reviewing what is in it and why.**

The `disertation` collection is the source of truth. Better BibTeX auto-exports it to
`../paper/src/bibs/ref.bib`, the file `main.tex` reads. That export is machine-written — never
hand-edit it. Add a paper in Zotero and the bibliography follows within seconds.

Verified 2026-11-03 against OpenAlex, the arXiv API, and the NDSS, PoPETs, USENIX and INFOCOM
proceedings directly. Nothing from memory, nothing from a GitHub reading list.

Reading order and the four fields to fill per paper: `summaries.md`.
Which papers ship runnable code or a usable dataset: `artifacts.md`.

## Subcollections

| | holds |
|---|---|
| `1 intro and basics` | foundations and the motivation story. Age does not matter |
| `2 learn and try` | read it, then reproduce it. Mechanics worth getting hands on |
| `3 needed for experiments` | datasets, frameworks, cost-curve method. The working set |
| `4 state of the art` | 2026 work to argue with and not be scooped by |

## Where each paper goes

Zotero's connector cannot move an item between collections, only create collections and add items
to the selected one. Papers imported after the subcollections existed carry a `sub:` tag — filter
on it and drag. The first 18 predate the tags, so they are listed out here.

**1 intro and basics** — two drags: filter tag `background` (6 items), then tag `motivation` (2).
Dyer `peek-a-boo`, Juarez `critical evaluation`, Wright `spot me if you can`,
Sirinam `deep fingerprinting`, Askarov and Zhang on timing channels, plus Weiss
`what was your prompt` and `NetEcho` as the motivation pair.

**2 learn and try** — `zhan2021earlyquic`, `jolles2026nym` (attack and defense in one paper),
plus tag `sub:learn`.

**3 needed for experiments** — `siby2023quic`, `sabzi2024netshaper`, `pulls2023maybenot`,
`gahtan2024visquic`, `witwer2026dodge`, `hasselquist2024raising`, plus tag `sub:experiments`.

**4 state of the art** — `song2026llmwf`, `pulls2026ephemeral`, plus tag `sub:sota`.

Four canonical papers were added on 2026-11-23 after reading `siby2023quic`, which cites all of
them as the work it builds on. They carry `sub:experiments` or `sub:learn`, so they sort by tag.
`gong2020front` and `cai2014tamaraw` are the original FRONT and Tamaraw papers — the two defences
Siby prices and `cebere2026http2` reproduces, so they are prerequisites rather than background.
`smith2022qcsd` and `smith2021quicage` are Smith's QUIC pair, and Siby positions itself directly
against the first.

## What the recent half is for

The question is "does padding actually help, and at what cost". Five papers answer parts of it:

- **`siby2023quic`** — Siby, Barman and Troncoso with Cloudflare. The question, already asked for
  QUIC: padding alone is not sufficient. The closest published work to this dissertation.
- **`khajavi2026lightening`** — NDSS 2026, Khajavi and Tao Wang. A *provable* defense at *lower*
  overhead. This is the number a new cost curve has to beat, and the strongest single find here.
- **`cebere2026http2`** — CISPA, September 2026. Reproduces FRONT, Tamaraw and ALPaCA using HTTP/2's
  own features, then measures leakage against overhead. A cost curve that already exists.
- **`wang2026cease`** — NDSS 2026. Efficient defense by iteratively minimising mutual information.
- **`hasselquist2024raising`** — what honest overhead looks like when published: constant-rate
  defense at 462 % receive bandwidth. Useful for knowing when a cost is absurd.
- **`pulls2024daitaeval`** — grey literature, and required reading. The only existing DAITA
  measurement: 2–4 MiB and 1–3 s per visit, one website, Windows, v1, no accuracy figures. Its
  method (20 VMs, Selenium, tshark, 80,000 traces) is also the template for February.

And four on why published accuracy does not survive contact with reality — the methods spine:

- **`deng2025realistic`** — the first systematic evaluation of existing attacks across defenses,
  traffic drift, multi-tab, early-stage, open-world and few-shot at once. Attacks that score above
  90 % in isolation fall over when the conditions combine. This is the end-November gate, already
  framed by someone else. Use their axes.
- **`yu2026proxydrift`** — the same website looks different through a different proxy protocol, and
  models trained on one protocol fail on another. That confound sits inside the March measurement,
  where DAITA on and off means traffic through a VPN either way.
- **`deng2026drift`** — NDSS 2026. Traffic drift degrades attacks over time.
- **`jansen2026cellshift`** and **`jansen2024genuine`** — Rob Jansen on real traces versus lab
  traces, and how to make lab traces behave. Read with `juarez2014critical`.

One on the attack side worth watching:

- **`cheng2026star`** — INFOCOM 2026. Zero-shot: identifies sites with no per-site training traces,
  through ECH and encrypted DNS, at 87.9 % top-1 on 1,600 unseen sites. If an attacker needs no
  training data per target, "the adversary could not collect traces for my site" stops being a
  defence. Datasets and code released.

## Data

**VisQUIC is downloadable now — no request needed.** An earlier note here said the dataset was
available on request. That was wrong: `gahtan2024visquic` ships it from
`github.com/robshahla/VisQUIC`, which links two public Dropbox folders (both reachable,
checked 2026-11-03).

Two kinds of archive are there, and the choice matters:

- `VisQUIC*.zip` — **take these.** PCAP traces, each with a matching `.key` file for decryption, so
  ground-truth labels come off the wire rather than out of a log. Not every trace decrypts; the
  authors say some were captured under a key they do not ship.
- `rgb_images*.zip` — skip. These are the authors' own visual feature encoding. Taking their images
  means inheriting their feature choices, and building features is the point of the January
  extractor.

## Still open

**DAITA has been measured exactly once, by someone who is not independent of it.** That is the
gap, and the full statement of it lives in `../PLAN.md` under *The gap this fills* — one canonical
wording, so it cannot drift from being restated. In short: `pulls2024daitaeval` is a blog post by
the author of Maybenot, who says on that page that he works with Mullvad on DAITA; it covers one
website from Windows clients against DAITA v1 and publishes cost but no accuracy; Mullvad's own
GotaTun audit excluded the DAITA code. Read that post early — it is the thing your March
measurement has to improve on, and it tells you how.

Other gaps:

- `zhao2026llmwf` (WWW 2026) is the only paper left with no PDF. Paywalled at the ACM, no preprint
  under that title and none under a different one from the same group. TCD proxy.
- Four PDFs are sitting in `~/Zotero/fnspdw-import/` waiting to be dragged onto their items:
  `zhan2021earlyquic`, `wright2008spot`, `pulls2023maybenot`, `zhang2011predictive`. The connector
  can attach a PDF to a new item but not to one that already exists, so this is a drag each.
- Does NetShaper's threat model exclude colocation and shared-link leakage? Answer from the paper.

Re-check the field every two months per `../PLAN.md`. Next: January 2027. NDSS, PoPETs and INFOCOM
are where this work lands; search engines rank them badly, so read the proceedings listings
directly. Searching an author's recent arXiv output works better than searching a title — three of
the papers above came out of one such listing and none had surfaced in a title search.
