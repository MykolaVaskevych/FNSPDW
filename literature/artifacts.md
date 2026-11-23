# Code and data

Which papers ship something runnable. This is the `To reproduce` field in `summaries.md`,
answered up front, because it decides which baseline is worth attempting and reading alone
will not tell you.

Checked and extended 2026-11-23: links came out of the PDFs themselves, not a search engine, and every one
below returned HTTP 200. To redo it, pull the `https://github...` and `doi.org/10.5281` strings
out of the PDFs in Zotero storage, keep the ones next to an availability sentence, and curl each.
Repos get renamed, so follow redirects rather than trusting the string in the paper.

## Start here

**`github.com/jpcsmith/wf-in-the-age-of-quic`** — Smith, Mittal and Perrig's dataset: about
117,000 QUIC *and* TCP page traces, described in the paper as the first publicly available
QUIC-TCP fingerprinting dataset. This project is about QUIC, and this is the only large public
dataset that is. It outranks the Tor benchmarks below for the end-November gate.

**`github.com/websitefingerprinting/WebsiteFingerprinting`** — Gong and Wang's release for FRONT:
simulation code for the defences *and* the attacks they evaluate against, plus datasets. The
cheapest way to get a defence and an attacker in the same harness.

**`github.com/deep-fingerprinting/df`** — Sirinam's code and the DF dataset. Tor, not QUIC, but it
is the field's common denominator: `wang2026cease` states outright that its 2026 experiments run
on it. Use it to check the pipeline against published numbers, not to answer the QUIC question.

**`github.com/FIND-Lab/Website-Fingerprinting-Library`** — WFlib, the harness the recent Tsinghua
work builds on, and `jansen2026cellshift` reaches for it too. Note it moved from `Xinhao-Deng/`,
so the URL printed in the papers redirects.

**`github.com/robshahla/VisQUIC`** — QUIC pcaps with the TLS keys. Public Dropbox links, no request
needed. See `README.md` for which archive to take.

**`github.com/jpcsmith/neqo-qcsd`** — QCSD: FRONT and Tamaraw implemented client-side on a fork of
Mozilla's neqo. A working QUIC defence to measure against, and the client-side comparator to
Maybenot.

## Per paper

| paper | code | data | where |
|---|---|---|---|
| `sirinam2018deep` | yes | yes | `deep-fingerprinting/df` |
| `smith2021quicage` | yes | yes, ~117k QUIC+TCP traces | `jpcsmith/wf-in-the-age-of-quic` |
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
| `pulls2023maybenot` | the framework itself | — | `maybenot-io/maybenot` |
| `witwer2026dodge` | yes | — | `trafnex/dodge-framework` |
| `hasselquist2024raising` | yes, incl. their reimplementations | — | `trafnex/raising-the-bar` |
| `cheng2026star` | yes | STAR-200K | `2654400439/STAR-Website-Fingerprinting` |
| `vanderlinden2026tcpts` | — | yes | `doi.org/10.5281/zenodo.17098889` |
| `gahtan2024visquic` | yes | yes, pcaps + keys | `robshahla/VisQUIC` |
| `weiss2024prompt` | yes | — | `royweiss1/GPT_Keylogger` |

## Worth knowing before you plan around them

- **`siby2023quic` ships nothing.** No availability statement, no artifact section, and the only
  repositories it cites are other people's tools. The paper closest to this dissertation is one to
  argue with, not one to reproduce.
- **`zhan2021earlyquic` ships nothing either.** No repository, no availability statement. It was the
  obvious QUIC baseline to rebuild; `smith2021quicage` is the one that comes with data.
- **`pulls2023maybenot` has two versions and they are not the same paper.** arXiv 2304.09510v1
  (April 2023) is the WPES 2023 paper that `pulls2023maybenot` cites. v2 (September 2024) documents
  *framework version 2*, which is what to read before writing strategies in April. The attachment in
  Zotero is v1 so that it matches the citation.
- **`deng2025realistic` ships nothing.** The paper that systematically re-evaluates everyone else's
  attacks has no availability statement and no repo. Its *axes* are reusable; its harness is not.
- **`wang2026cease` contradicts itself** — one sentence says "The complete implementation code will
  be made available shortly", another gives a live URL. The repo exists; check it has content
  before relying on it.
- **`jansen2024genuine` is request-only.** GTT23, 13M+ genuine Tor traces, "available to researchers
  upon request since 2024". The one dataset here with real lead time, so ask early if you want it.
- **`sabzi2024netshaper` has no artifact link in the paper.** Only its dependencies are linked. If
  the NetShaper code matters, the USENIX artifact appendix is the place to look, not the PDF.
- **`hasselquist2024raising` reimplemented three attacks** because the authors would not share code,
  and published those reimplementations. That is a reusable act of generosity, and also a warning
  about what "we compare against prior work" can quietly mean.
