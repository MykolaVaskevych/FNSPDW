"""Stages 1/3/4 of the traffic-analysis feasibility study.

  stage1 - length-matched baseline, no defence: is there signal left?
  stage3 - cover traffic + quantised count/duration: does the defence work,
           and what does it cost?
  stage4 - disconnect / concurrency / slow-client behaviour under stage 3.
"""

import argparse
import itertools
import math
import random
import socket
import threading
import time

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedGroupKFold

import corpus
import server
from capture import capture
import features as F
import proxy

_port = itertools.count(9300)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def start_server(texts, pause=True):
    p = next(_port)
    threading.Thread(target=server.serve, args=(p, texts),
                     kwargs={"pause": pause}, daemon=True).start()
    return p


def start_proxy(up, **kw):
    p = next(_port)
    threading.Thread(target=proxy.serve, args=(p, "127.0.0.1", up),
                     kwargs=kw, daemon=True).start()
    return p


def collect(samples, reps, defence=None, pause=True, seed=0, raw=False):
    """Capture traces. Order is shuffled so that drift in machine load over the
    run cannot correlate with class label."""
    sp = start_server([s["toks"] for s in samples], pause=pause)
    port = start_proxy(sp, **defence) if defence else sp
    time.sleep(0.4)
    jobs = [(r, i) for r in range(reps) for i in range(len(samples))]
    random.Random(seed).shuffle(jobs)
    rows, raws = {}, []
    for _, i in jobs:
        tr = capture("127.0.0.1", port, index=i)
        if tr:
            rows.setdefault(i, []).append(F.featurize(tr))
            raws.append((tr, samples[i]["label"], samples[i]["group"]))
    if raw:
        return raws
    X, y, g = [], [], []
    for i, feats in rows.items():
        for f in feats:
            X.append(f)
            y.append(samples[i]["label"])
            g.append(samples[i]["group"])
    return np.array(X), np.array(y), np.array(g)


def evaluate(X, y, g, cols=None, splits=5, seed=0):
    """Out-of-fold accuracy with a GROUP-aware split: no source text appears in
    both train and test, otherwise near-duplicate traces leak the answer."""
    Xc = X[:, cols] if cols is not None else X
    n_g = len(set(g))
    k = min(splits, n_g // 2) if n_g >= 4 else 2
    cv = StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=seed)
    pred = np.empty(len(y), dtype=object)
    for tr, te in cv.split(Xc, y, groups=g):
        m = GradientBoostingClassifier(random_state=seed).fit(Xc[tr], y[tr])
        pred[te] = m.predict(Xc[te])
    correct = int((pred == y).sum())
    return correct / len(y), wilson(correct, len(y)), len(y), k


def report(X, y, g, title):
    print(f"\n--- {title} ---")
    print(f"    n={len(y)} traces, {len(set(g))} groups, "
          f"classes={dict(zip(*np.unique(y, return_counts=True)))}")
    acc, ci, n, k = evaluate(X, y, g)
    print(f"    ALL features      acc={acc:.3f}  95% CI [{ci[0]:.3f}, {ci[1]:.3f}]"
          f"  ({k}-fold grouped)")
    for keep in ("VOL", "SIZE", "TIME"):
        a, c, _, _ = evaluate(X, y, g, F.cols(keep={keep}))
        print(f"    {keep:<4} only         acc={a:.3f}  95% CI [{c[0]:.3f}, {c[1]:.3f}]")
    a, c, _, _ = evaluate(X, y, g, F.cols(drop={"VOL"}))
    print(f"    SIZE+TIME (no VOL) acc={a:.3f} 95% CI [{c[0]:.3f}, {c[1]:.3f}]")
    m = GradientBoostingClassifier(random_state=0).fit(X, y)
    top = sorted(zip(F.NAMES, F.GROUPS, m.feature_importances_),
                 key=lambda t: -t[2])[:8]
    print("    top features: " + ", ".join(f"{n}[{gr}]={v:.2f}"
                                           for n, gr, v in top if v > 0.001))
    return acc, ci


def stage1(reps):
    print("=" * 70)
    print("STAGE 1 - length-matched baseline, NO defence")
    print("=" * 70)
    a = corpus.count_matched(40)
    b = corpus.byte_matched(tol_char=0.02, per_text=4)
    mc = np.mean([sum(len(w) for w in s["toks"])
                  for s in b if s["label"] == "MED"])
    gc = np.mean([sum(len(w) for w in s["toks"])
                  for s in b if s["label"] == "GEN"])
    print(f"cond A: token count matched EXACTLY (40), bytes free to differ")
    print(f"cond B: token count matched EXACTLY, chars matched to "
          f"{abs(mc - gc) / mc * 100:.2f}%")
    Xa, ya, ga = collect(a, reps, seed=1)
    report(Xa, ya, ga, "A: count-matched only")
    Xb, yb, gb = collect(b, reps, seed=2)
    report(Xb, yb, gb, "B: count- AND byte-matched (strict)")
    print("\n  [B, no structural pauses in the generator]")
    Xc, yc, gc2 = collect(b, reps, pause=False, seed=3)
    report(Xc, yc, gc2, "B: strict, flat inter-token timing")
    return {"A": (Xa, ya, ga), "B": (Xb, yb, gb)}


def defence_cost(tag):
    s = [x for x in proxy.STATS if not x["disconnected"]]
    proxy.STATS.clear()
    if not s:
        return
    f = lambda k: np.mean([x[k] for x in s])
    print(f"    cost[{tag}]: bytes={f('bytes'):.0f} "
          f"(cover {f('cover_bytes'):.0f} = "
          f"{100 * f('cover_bytes') / max(f('bytes'), 1):.0f}%), "
          f"chunks={f('emitted'):.1f} (real {f('real'):.1f}, cover {f('cover'):.1f}), "
          f"t_first_content={f('t_first_real') * 1000:.0f}ms, "
          f"completion={f('duration'):.2f}s")


def stage2(reps):
    print("=" * 70)
    print("STAGE 2 - real subword tokenization vs the synthetic assumption")
    print("=" * 70)
    print("No live llama.cpp/ollama generation: see the write-up for what that")
    print("needs. This isolates the half that matters -- token boundaries.")
    for nm, tok in (("ws (synthetic)", corpus.ws), ("bpe cl100k_base", corpus.bpe)):
        parts = []
        for lab, ts in (("MED", corpus.MED), ("GEN", corpus.GEN)):
            n = [len(tok(t)) for t in ts]
            L = [len(x) for t in ts for x in tok(t)]
            ch = [sum(len(x) for x in tok(t)) for t in ts]
            parts.append(f"{lab} {np.mean(n):5.1f} tok/resp, len "
                         f"{np.mean(L):.2f}+-{np.std(L):.2f}, "
                         f"tok/char {np.mean(n) / np.mean(ch):.4f}")
        print(f"  {nm:<17} " + "  |  ".join(parts))

    for nm, tok, cm in (("ws", corpus.ws, 40), ("bpe", corpus.bpe, 60)):
        a = corpus.count_matched(cm, tok=tok)
        b = corpus.byte_matched(tok=tok, tol_char=0.02, per_text=4)
        X, y, g = collect(a, reps, seed=11)
        report(X, y, g, f"{nm}: count-matched ({cm} tokens)")
        X, y, g = collect(b, reps, seed=12)
        report(X, y, g, f"{nm}: count+byte-matched (strict)")


def stage3(reps, quantum):
    print("\n" + "=" * 70)
    print(f"STAGE 3 - full defence (pad + clock + cover + count padding)")
    print("=" * 70)
    FIXED = 96  # pad every response to exactly this many chunks
    unmatched = corpus.full_corpus()
    strict = corpus.byte_matched(tol_char=0.02, per_text=4)

    arms = [
        ("unmatched (variable length)", unmatched, None, "no defence"),
        ("unmatched (variable length)", unmatched,
         {"mode": "full", "quantum": quantum}, f"quantum={quantum}"),
        ("unmatched (variable length)", unmatched,
         {"mode": "full", "min_chunks": FIXED}, f"fixed count={FIXED}"),
        ("strict matched", strict, None, "no defence"),
        ("strict matched", strict,
         {"mode": "full", "min_chunks": FIXED}, f"fixed count={FIXED}"),
    ]
    for i, (name, samples, defence, tag) in enumerate(arms):
        proxy.STATS.clear()
        X, y, g = collect(samples, reps, defence=defence, seed=40 + i)
        report(X, y, g, f"{name}  [{tag}]")
        if defence:
            defence_cost(tag)
        else:
            tb = X[:, F.NAMES.index("total_bytes")].mean()
            td = X[:, F.NAMES.index("duration")].mean()
            nc = X[:, F.NAMES.index("n_chunks")].mean()
            print(f"    cost[{tag}]: bytes={tb:.0f}, chunks={nc:.1f}, "
                  f"completion={td:.2f}s  (baseline)")


def stage4(quantum):
    print("\n" + "=" * 70)
    print("STAGE 4 - failure modes under the stage 3 defence")
    print("=" * 70)
    sp = start_server([corpus.ws(t) for t in corpus.MED])
    pp = start_proxy(sp, mode="full", quantum=quantum)
    ppt = start_proxy(sp, mode="full", quantum=quantum, threaded=True)
    time.sleep(0.4)

    # --- 1. client disconnects mid-response
    proxy.STATS.clear()
    s = socket.socket(); s.connect(("127.0.0.1", pp)); s.sendall(b"0\n")
    got, t0 = 0, time.perf_counter()
    while time.perf_counter() - t0 < 0.35:
        try:
            d = s.recv(65536)
        except OSError:
            break
        if not d:
            break
        got += 1
    s.close()
    time.sleep(2.0)
    st = proxy.STATS[-1] if proxy.STATS else None
    print(f"\n[disconnect] client read {got} chunks then closed.")
    if st:
        print(f"    proxy emitted {st['emitted']} (real {st['real']}, cover {st['cover']}), "
              f"noticed disconnect={st['disconnected']}, "
              f"upstream_finished={st['upstream_done']}, stopped after {st['duration']:.2f}s")

    # --- 2. three concurrent requests, serial vs threaded accept loop
    for lab, port in (("serial", pp), ("threaded", ppt)):
        proxy.STATS.clear()
        res, lock = [], threading.Lock()

        def one(i):
            t0 = time.perf_counter()
            tr = capture("127.0.0.1", port, index=i)
            with lock:
                res.append((time.perf_counter() - t0,
                            tr[0][1] if tr else None, len(tr)))

        ths = [threading.Thread(target=one, args=(i,)) for i in range(3)]
        t0 = time.perf_counter()
        for t in ths:
            t.start()
        for t in ths:
            t.join()
        wall = time.perf_counter() - t0
        res.sort()
        print(f"\n[concurrency x3, {lab}] wall={wall:.2f}s  per-client total: "
              + ", ".join(f"{r[0]:.2f}s({r[2]}ch)" for r in res))
        if proxy.STATS:
            gaps = [x["duration"] / max(x["emitted"], 1) for x in proxy.STATS]
            print(f"    mean realised tick = {np.mean(gaps) * 1000:.1f}ms "
                  f"(target {proxy.TICK * 1000:.0f}ms), "
                  f"max={max(gaps) * 1000:.1f}ms")

    # --- 3. slow client that never reads, against a long response
    proxy.STATS.clear()
    proxy.LIVE.update({"queue": 0, "emitted": 0, "blocked_s": 0.0})
    long_toks = corpus.ws(" ".join(corpus.MED) * 3)  # ~1500 tokens
    sp2 = start_server([long_toks])
    pp2 = start_proxy(sp2, mode="full", quantum=quantum, threaded=True)
    time.sleep(0.4)
    s = socket.socket()
    s.connect(("127.0.0.1", pp2))
    s.sendall(b"0\n")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
    print(f"\n[slow client] upstream response = {len(long_toks)} tokens; "
          f"client never reads")
    t_start = time.perf_counter()
    for t in (1.0, 2.0, 4.0, 6.0):
        time.sleep(max(0.0, t_start + t - time.perf_counter()))
        print(f"    t={t:>4.1f}s  internal queue={proxy.LIVE['queue']:>4} chunks, "
              f"emitted={proxy.LIVE['emitted']:>4}, "
              f"blocked_in_sendall={proxy.LIVE['blocked_s']:.2f}s")
    s.close()
    time.sleep(1.0)
    if proxy.STATS:
        st = proxy.STATS[-1]
        print(f"    final: emitted={st['emitted']}, max_queue={st['max_queue']} "
              f"chunks (~{st['max_queue'] * 64 / 1024:.0f}KiB held in RAM), "
              f"blocked={st['blocked_s']:.2f}s, disconnected={st['disconnected']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("1", "2", "3", "4"), required=True)
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--quantum", type=int, default=64)
    a = ap.parse_args()
    if a.stage == "1":
        stage1(a.reps)
    elif a.stage == "2":
        stage2(a.reps)
    elif a.stage == "3":
        stage3(a.reps, a.quantum)
    else:
        stage4(a.quantum)
