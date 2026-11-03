"""The decisive combination: strongest attack (real BPE tokens, strict
length+byte matching) against the stage-3 defence."""
import corpus
import experiment as E
import proxy

b = corpus.byte_matched(tok=corpus.bpe, tol_char=0.02, per_text=4)
print(f"bpe strict corpus: {len(b)} samples, {len({x['group'] for x in b})} groups")
X, y, g = E.collect(b, 1, seed=80)
E.report(X, y, g, "bpe strict: NO defence")
proxy.STATS.clear()
X, y, g = E.collect(b, 1, defence={"mode": "full", "min_chunks": 96}, seed=81)
E.report(X, y, g, "bpe strict: FULL defence (fixed count=96)")
E.defence_cost("bpe strict, fixed=96")
