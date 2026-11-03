"""Is the residual leak under the stage-3 defence real, or a localhost artefact?

The defended strict-matched traces still classified at ~0.60 using TIMING
features, even though every chunk is the same size and released on a fixed
clock. Localhost gives microsecond-accurate arrival times that no real network
observer would have. This adds synthetic network jitter to the SAME traces and
re-trains: if the signal dies under realistic jitter, it was an artefact of
measuring on loopback.
"""

import numpy as np

import corpus
import experiment as E
import features as F


def jittered(traces, sd, rng):
    """Re-time a trace as a network observer would see it."""
    out = []
    for tr, lab, grp in traces:
        t = np.array([x[1] for x in tr]) + rng.normal(0, sd, len(tr))
        t = np.maximum.accumulate(t)  # arrivals cannot reorder
        t -= t[0]
        out.append(([(tr[k][0], float(t[k])) for k in range(len(tr))], lab, grp))
    return out


def run(traces, label):
    print(f"\n  {label}")
    print(f"  {'jitter sd':>10} | {'accuracy':>8} | 95% CI")
    rng = np.random.default_rng(0)
    for sd in (0.0, 0.0001, 0.0005, 0.001, 0.005, 0.020):
        js = jittered(traces, sd, rng) if sd else traces
        X = np.array([F.featurize(t) for t, _, _ in js])
        y = np.array([l for _, l, _ in js])
        g = np.array([gg for _, _, gg in js])
        acc, ci, n, k = E.evaluate(X, y, g)
        tag = "none (loopback)" if sd == 0 else f"{sd * 1000:.1f} ms"
        print(f"  {tag:>15} | {acc:>8.3f} | [{ci[0]:.3f}, {ci[1]:.3f}]")


if __name__ == "__main__":
    strict = corpus.byte_matched(tol_char=0.02, per_text=4)
    print("=" * 62)
    print("RESIDUAL LEAK vs NETWORK JITTER (strict-matched corpus)")
    print("=" * 62)
    tr = E.collect(strict, 2, defence={"mode": "full", "min_chunks": 96},
                   seed=70, raw=True)
    run(tr, "WITH stage-3 defence (pad+clock+cover+fixed count=96)")
    tr = E.collect(strict, 2, seed=71, raw=True)
    run(tr, "NO defence (for comparison)")
