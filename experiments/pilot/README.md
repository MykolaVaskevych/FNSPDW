# Pilot — feasibility probe (historical)

**Status: superseded. None of the numbers in `out/` are citable.** Kept because the methodology and
several non-obvious design decisions are worth reusing, and because the thesis needs an honest account
of where the project started.

## What it asked

Can an on-path observer recover the *topic* of a streaming LLM response from encrypted traffic metadata
alone, and does a shaping proxy close the channel — at what cost?

## What it found

| | |
|---|---|
| undefended, strict length+byte matched, real BPE tokens | 0.818 |
| same, with full defence (pad + fixed clock + cover traffic + count padding) | 0.432 |
| cost of that defence | 67 % cover traffic, completion 0.55 s → 2.13 s |

## Why the numbers are not citable

Five artificial conditions stacked at once:

1. **Synthetic corpus.** One model authored both classes, so the classifier may be separating prose
   register rather than topic. Largest unresolved threat — see `corpus.py`'s own docstring.
2. **Fake generator.** `server.py` invents inter-token delays, including a `PAUSE` at punctuation that
   no real decoder produces.
3. **Loopback only.** `lo` has MTU 65536 and ~10 µs RTT. Every small write became its own segment,
   which flatters the size channel.
4. **No TLS.** Plaintext throughout.
5. **Observer was an endpoint.** `capture.py` times its own `recv()` calls — that is a socket-level
   measurement, not a wire-level one, and it violates the project's own rule that every number comes
   off the wire.

Known bugs, both real: the Wilson interval in `experiment.py` is computed over *traces* when traces
within a group are near-duplicates (n=240 from 18 groups, so the stated precision is several times too
narrow); and `pad()` in `proxy.py` silently truncates any chunk over 64 bytes, dropping
real content.

## What it got right, and what should be carried forward

- **Job order is shuffled**, so drift in machine load cannot correlate with the class label.
- **VOL / SIZE / TIME feature ablation**, so the question "*which channel* carried the signal?" is
  answerable rather than just "it classified". Now in `features.py`.
- **Grouped cross-validation by source text**, so near-duplicate traces cannot straddle a fold.
- **`jitter.py` is a falsification test** — re-time the same traces under synthetic jitter and see
  whether the leak survives. It didn't: defended accuracy sat at chance across every jitter level.
- **The TIME channel was self-disproved.** Re-running with pauses disabled dropped TIME-only accuracy
  from 0.709 to 0.512, which correctly identifies it as an artefact of the fake generator.

## Running it

Flat sibling imports, so run from inside this directory:

```bash
cd experiments/pilot
uv run experiment.py --stage 1     # stages 1-4
uv run jitter.py
uv run stage3_bpe.py
```

`features.py` and `proxy.py` used to live in a shared package. Nothing else ever imported them,
so they moved here with the only code that does.
