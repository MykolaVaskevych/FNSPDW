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

## What it actually costs — checked 2026-11-24, before collecting anything

The gate as originally written, "their code, their data, their number", is **not a one-evening
job**, and that is worth knowing before starting rather than after.

From the workflow's own README: *"Each of the 330 train-test splits takes around 30-60 minutes for
a sequential runtime of around 165-330 hours."* That is one to two weeks of compute for the full
sweep — four classifiers, ten repetitions, nine QUIC deployment levels.

What the 871 MB archive actually ships, verified by listing it: eleven files, of which the only one
that matters here is `generalisability-analysis/results/open-world-dataset.hdf`, **3.0 GB
uncompressed**. Domain lists and a feature-rank CSV make up the rest. **No splits and no
predictions.** So the number has to be computed; the notebook cannot simply re-plot it.

And `confusion-matrix.ipynb` — the notebook that makes Table 2, the source of the 4,801 of 5,000
figure — reads `predictions-varcnn-quic-all.csv`. That is **Var-CNN**, a deep-learning model, over
ten repetitions. Not one of the cheap classifiers. The config lists `dfnet, varcnn, p1fp, kfp` with
`n_repetitions: 10`, and per-job times of roughly 70 for dfnet and 10 for kfp.

The 4090 has 24 GB, so Var-CNN on GPU is viable. It is a question of hours, not minutes.

### So the gate narrows, and the threshold narrows with it

Pick one of these and write the choice down before running:

1. **Var-CNN, fewer repetitions.** Run the Table 2 experiment with 1-2 repetitions instead of 10.
   Compares directly against 96 % but with wider variance than the paper's, so the +/- 3 pp band
   above may be too tight for a single repetition. This is the honest reproduction.
2. **k-FP instead.** Roughly 10 per job, so quick, but **Table 2 is not k-FP** — comparing a k-FP
   result against the Var-CNN figure would be measuring the wrong thing. Only valid if reported
   explicitly as the same experiment with a cheaper classifier.

Either way the threshold has to name the classifier and the number of repetitions. The version
above does not, which is a defect in the pre-registration found before any data was collected —
which is the point of writing it first.

### The 4090 cannot be used, verified

TensorFlow 2.2.0 detects the card and then refuses it, in its own words:

```
name: NVIDIA GeForce RTX 4090  computeCapability: 8.9
Skipping registering GPU devices...
GPUs visible: []
```

TF 2.2.0 ships CUDA 10.1 kernels and tops out at compute capability 7.5. Ada Lovelace is 8.9, two
generations later. So Var-CNN trains on **CPU**, and the choice is CPU time or porting the code to
a modern TensorFlow — which would no longer be "their code".

### Two things the artifact needs that its own instructions do not mention

Both are reproducibility findings in their own right, and both are the kind of thing
`deng2025realistic` predicts:

1. **`requirements.txt` is under-pinned.** It does not pin protobuf, so a current resolver installs
   protobuf 5.x and TensorFlow 2.2.0 dies with `TypeError: Descriptors cannot be created
   directly`. Fix: `protobuf<3.21`. Nothing in the repo says this.
2. **The workflow cannot start from the published dataset alone.** `select_traces` declares inputs
   from the *removing-control-packets* workflow, which the 871 MB archive does not contain, so
   Snakemake refuses to build a DAG even though `results/open-world-dataset.hdf` is present and is
   what the rule would produce. Workaround: create empty placeholders at the two declared input
   paths and touch the dataset so it is newest. `select_traces` then drops out of the DAG.

### The run as actually configured

Target `results/plots/confusion-matrix.tex` with `n_repetitions=1` resolves to **8 jobs**, of which
**2 are Var-CNN trainings** (`varcnn-sizes` and `varcnn-time`, which are combined to make the
Var-CNN prediction set). `select_traces` is correctly absent.

```bash
cd out/repo/workflows/generalisability-analysis
../../env/bin/snakemake -j1 results/plots/confusion-matrix.tex --config n_repetitions=1
```

Note the target must come *before* `--config`, or Snakemake 5.20.1 swallows it as a config pair.

**Threshold for this run, given 1 repetition on CPU instead of 10 on GPU:** the +/- 3 pp band above
is too tight for a single repetition. Widen to **+/- 10 pp of 96 %**, i.e. 4,300-5,000 of 5,000,
and report it as "one repetition, CPU, wider interval than the paper's" rather than as a clean
reproduction. If the single run lands inside that, the pipeline is sound and the gate is met.

### Already done, so the run can start cold

- Dataset downloaded and extracted to `out/repo/workflows/generalisability-analysis/results/`
- `github.com/jpcsmith/wf-in-the-age-of-quic` cloned to `out/repo` (shallow)
- `git-lfs` is **not** installed and is **not needed** for this workflow — LFS there covers
  chromedriver binaries and data files, not the Snakefile, rules, scripts or notebooks
- Python 3.8.20 venv at `out/repo/env`, built with `uv`, all requirements installed plus
  `protobuf<3.21` and `snakemake==5.20.1`. Verified: numpy, sklearn, pandas, h5py, tensorflow and
  the authors' own `lab` and `doceasy` packages all import
- Both VCS dependencies still resolve at their pinned tags (`doceasy@v0.4.0`, `wf-tools@v0.3.0`)
- Docker is installed but **not needed** — it is only used by the trace-collection workflow

## Result

*Empty until the run. Record the number, the date, the classifier and repetition count, whether the
threshold was met, and anything that had to be changed to make the workflow run.*
