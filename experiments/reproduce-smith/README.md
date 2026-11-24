# reproduce-smith — the end-November gate

Reproduce a published website-fingerprinting result from someone else's code and someone else's
data, and record whether the number came back. This is the first gate in `../../PLAN.md`: *a
published baseline reproduces — their code, their data, their number.*

Written before anything was downloaded or run, on 2026-11-24.

## What is being reproduced

`smith2021quicage` — *Website Fingerprinting in the Age of QUIC*, Smith, Mittal and Perrig,
PoPETs 2021. Its headline claim is that classifiers trained on TCP traces fail to see QUIC traffic.
The paper states it as an exact count:

> Of the 5,000 tested QUIC samples, 4,801 (96%) of them are incorrectly classified as unmonitored
> traces by the classifier.

That count is the target. It is better than a percentage alone because it is unambiguous and
appears in Table 2's confusion matrix.

- **Paper section:** 6, *From TCP to QUIC*
- **Workflow:** `workflows/generalisability-analysis`
- **Notebook:** `confusion-matrix.ipynb`, output `confusion-matrix.tex`
- **Classifier:** k-FP. The paper reports r20-precision and recall with 95 % bootstrapped
  confidence intervals.

## Threshold — written first, and mine to set

**Proposed, needs my sign-off before the run:**

The reproduction **passes** if the monitored-QUIC-classified-as-unmonitored rate lands within
**±3 percentage points of 96 %**, i.e. between 4,650 and 5,000 of 5,000 samples. ±3 pp is wider
than the paper's own bootstrapped intervals, which is deliberate: this is a check that the pipeline
and data are sound, not a test of the paper.

It **fails** if the rate falls outside that band, or if the workflow cannot be run at all.

Either way the result is written down. A documented failure to reproduce, with the reason, is a
methods contribution — `deng2025realistic` says to expect exactly that. The fallback is a second
baseline, not a second topic.

## Data

**871 MB, not the ~30 GB raw set.** `quic-wf-core.tgz` holds the open-world dataset in HDF5 with
class, protocol and VPN-location labels, arrays of sizes and timestamps, and packets below 175
bytes removed.

Both polybox links in the upstream README are dead. The live copy is the ETH Research Collection
record behind `doi.org/10.3929/ethz-b-000456101`, fetched through the DSpace content endpoint —
verified 2026-11-24 by range-fetching bytes and confirming gzip magic, not by trusting the link:

```bash
curl -L -o quic-wf-core.tgz \
  https://www.research-collection.ethz.ch/server/api/core/bitstreams/ab483811-4adf-4967-9737-43044ca3a149/content
```

A 7.25 GB VM image with code and data preloaded sits in the same record, if environment setup turns
out to be the slow part. The authors ran each experiment on 2–4 cores with 6 GB of memory per core,
so compute is not the obstacle.

Code: `github.com/jpcsmith/wf-in-the-age-of-quic`, which ships a Docker setup. Note it uses git LFS.

## Confirm before trusting the comparison

**Was the published 96 % computed on this processed core set, or on the raw traces?** The core
archive has packets under 175 bytes removed, and removing control packets is itself one of the
paper's analyses (Section 8). If Table 2 was produced from raw traces, then reproducing it from the
core set is not the same experiment and the threshold above is measuring the wrong thing. Check
what `workflows/generalisability-analysis` actually reads before comparing numbers.

If they differ, say so in the result rather than quietly comparing across preprocessing.

## Result

*Empty until the run. Record the number, the date, whether the threshold was met, and anything that
had to be changed to make the workflow run.*
