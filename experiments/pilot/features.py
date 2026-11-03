"""Feature extraction from a trace = [(byte_size, arrival_time), ...].

Features are grouped so we can ask which channel the classifier is using:
  VOL  - chunk count, total bytes, duration  (the "easy" channels)
  SIZE - per-chunk size distribution/sequence (the token-length channel)
  TIME - inter-chunk timing distribution/sequence
"""

import numpy as np

HEAD = 12  # leading chunks kept in order
SIZE_BINS = list(range(8, 26)) + [40, 80]  # chunk size = token len + 8
GAP_BINS = [0.004, 0.008, 0.012, 0.016, 0.020, 0.030, 0.050, 0.080, 0.150]


def _stats(a):
    return [a.mean(), a.std(), a.min(), a.max(),
            *np.percentile(a, [10, 25, 50, 75, 90])]


_SN = ["mean", "std", "min", "max", "p10", "p25", "p50", "p75", "p90"]

NAMES = (
    ["n_chunks", "total_bytes", "duration"]
    + [f"size_{s}" for s in _SN]
    + [f"sizehist_{b}" for b in SIZE_BINS]
    + [f"size@{i}" for i in range(HEAD)]
    + [f"gap_{s}" for s in _SN]
    + [f"gaphist_{b}" for b in GAP_BINS]
    + [f"gap@{i}" for i in range(HEAD)]
)

VOL = {"n_chunks", "total_bytes", "duration"}


def group_of(name):
    if name in VOL:
        return "VOL"
    return "SIZE" if name.startswith("size") else "TIME"


GROUPS = [group_of(n) for n in NAMES]


def featurize(trace):
    sizes = np.array([s for s, _ in trace], float)
    ts = np.array([t for _, t in trace], float)
    gaps = np.diff(ts) if len(ts) > 1 else np.array([0.0])
    n = len(sizes)
    sh = np.histogram(sizes, bins=SIZE_BINS + [10**9])[0][:len(SIZE_BINS)] / max(n, 1)
    gh = np.histogram(gaps, bins=GAP_BINS + [10**9])[0][:len(GAP_BINS)] / max(len(gaps), 1)
    head = lambda a, k: list(a[:k]) + [0.0] * (k - min(k, len(a)))
    return np.array(
        [float(n), sizes.sum(), ts[-1]]
        + _stats(sizes) + list(sh) + head(sizes, HEAD)
        + _stats(gaps) + list(gh) + head(gaps, HEAD)
    )


def cols(keep=None, drop=None):
    """Column indices, filtered by feature-group name."""
    return [i for i, g in enumerate(GROUPS)
            if (keep is None or g in keep) and (drop is None or g not in drop)]
