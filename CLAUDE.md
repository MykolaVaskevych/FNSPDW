# FNSPDW

Paper lives in the `paper/` git submodule. Its rules are in `paper/CLAUDE.md` — read it before touching anything in `paper/`.

No comments in LaTeX unless I ask.

## Project — read this before advising on anything

**The topic:** does padding actually help? What encrypted web traffic over TLS and QUIC still
reveals through packet size, timing and direction, and what padding defences buy measured against
what they cost in bandwidth and latency. Mullvad's DAITA is the deployed case; my own strategies on
Maybenot are the extension; the deliverable is a leakage-against-overhead cost curve.

**Precedence, because this repo has misled assistants before:**

1. `PLAN.md` is the only source of truth for topic and scope.
2. `DECISIONS.md` says when and why the scope changed, and what each change superseded.
3. `notes/PROJECT.md` is subordinate reasoning. Useful, but it has been stale before — check it
   against `PLAN.md` before believing it.

**LLM traffic is out of scope and stays out.** Farrell asked what made it different and suggested
plain web traffic; `experiments/token-batching` then measured that OpenAI pads every streamed event
to a constant size. Dropped 2026-10-20. It is the motivation, not the project. Do not reopen it
unless I say Farrell has agreed.

**The gap the whole project rests on** is stated once, in `PLAN.md` under *The gap this fills*.
Restate it from there, never from memory — it is a negative claim about DAITA and a loose version
of it will not survive a viva.

**The Rust flow-feature extractor is mine alone, written without AI.** Do not write it, draft it or
hand me snippets. Offer to validate it against `tshark` instead.

`CONTEXT.md` is the same briefing in self-contained form, for pasting into an assistant that cannot
read this repo.

## Code

- Comment to carry the domain knowledge, not the syntax. `TCP_NODELAY` earns a note about Nagle; `rows = []` earns nothing. Never restate what a line obviously does.
- Every file opens with a docstring: what it does and why it exists.
- Don't over-engineer. No classes, abstractions or extra files unless they pay for themselves.
- Reuse over duplication, but no shared package until two experiments genuinely need the same code. Until then it lives with the experiment that uses it.
- Docs stay current with the code they describe.

## Bibliography

Zotero owns it. The `disertation` collection is the source of truth, and Better BibTeX
auto-exports it to `paper/src/bibs/ref.bib`, which is what `main.tex` reads.

- Never hand-edit `paper/src/bibs/ref.bib`. It is machine-written and will be overwritten.
- To add a reference, put it in Zotero. The export follows on change.
- Verify every citation against OpenAlex, the arXiv API or the publisher before it goes in.
  DBLP and Google Scholar block scripts; those two work.

## Captures

- No personal traffic, ever. Only traffic the lab generated on purpose.
- Always capture with a filter pinned to the lab port or host, so other traffic never reaches the file.
- Need realistic traffic we cannot generate? Use a public dataset, not my own browsing.
- Captures and datasets stay out of git.

## Experiments

Each gets its own directory. Nothing dumped in the repo root.

```
experiments/<name>/
    README.md    what it tests, why, and the failure threshold — written BEFORE it runs
    run.py       the experiment
    out/         its own output: pcaps, numbers, plots
```

The failure threshold goes in writing first, every time. A pre-registered negative result is science; an unregistered one looks like incompetence.

## Commits (this repo and `paper/`)

- I name commits myself. Every time, ask me how to commit (the message). Never commit on your own.
- Commit messages: short, one line, never any description/body.
- Never mention Claude/AI in commits: no `Co-Authored-By`, no "Generated with" lines, nothing.
