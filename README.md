# My Dissertation

What encrypted web traffic still reveals through packet size, timing and direction, and
whether padding defences actually help.

MSc Future Networked Systems, Trinity College Dublin. Supervisor: Stephen Farrell.

## Read

**[PLAN.md](PLAN.md)** is the whole project in one file — the question, the scope, the gap it
fills, month by month to submission in August 2027, the gates and what happens when each one
fails, how I work, the library, and a dated log of every decision that changed any of it.

There is deliberately nothing else to read. Four documents describing one project is how the
plan and the brief drifted apart far enough to contradict each other, so they were merged.

- **[literature/summaries.md](literature/summaries.md)** — reading order, and my notes per paper
- **Paper** — [PDF](https://github.com/MykolaVaskevych/Paper/blob/main/build/default/default.pdf)
  · [LaTeX source](https://github.com/MykolaVaskevych/Paper)
  · [live on Overleaf](https://www.overleaf.com/read/gpwqvbpkffkp#9d77de)

The paper is its own repo, pulled in here as a submodule, because Overleaf syncs straight into
it. GitHub shows it above as a pointer rather than a folder, so the three links go there
directly. The PDF is committed, so it can be read without a LaTeX setup.

## References

Zotero owns the bibliography. The `disertation` collection is the source of truth, and Better
BibTeX auto-exports it to `paper/src/bibs/ref.bib`, which is what `main.tex` reads through
`\bibliography{bibs/ref}`. That file is machine-written — never hand-edit it. Every entry was
verified against OpenAlex, the arXiv API, or the publisher's own proceedings listing before it
went in. Details, including which papers ship runnable code or a usable dataset, are in
[PLAN.md](PLAN.md#the-library).

## Experiments

One folder each. Every README says what it asked, what the threshold was, and what came back —
written before the experiment ran.

- **[first-look](experiments/first-look)** — TLS record sizes read off real packets. Encryption
  hides what is in a record, not how big it is.
- **[token-batching](experiments/token-batching)** — does one streamed event carry one token?
  Yes, but OpenAI pads every event to a constant size, which closes the channel. This is the
  measurement that became the project's motivation.
- **[pilot](experiments/pilot)** — inherited feasibility probe. Superseded, and its numbers are
  not citable. Kept for the method and for the record of why they don't count.

## Running it

One venv at the root, `uv` for everything.

```bash
git clone --recurse-submodules git@github.com:MykolaVaskevych/FNSPDW.git
cd FNSPDW
uv sync
```

Then `cd` into an experiment and follow its README. Output lands in that folder's `out/`, which
is not committed — rerun it instead.

The paper builds with [Tectonic](https://tectonic-typesetting.github.io/), which fetches its own
TeX packages, so nothing else needs installing:

```bash
cd paper && tectonic -X build      # writes build/default/default.pdf
```
