# My Dissertation

What encrypted web traffic still reveals through packet size, timing and direction, and
whether padding defences actually help.

MSc Future Networked Systems, Trinity College Dublin. Supervisor: Stephen Farrell.

## Read

- **[Plan](PLAN.md)** — month by month to submission in August 2027, with the gates and their
  failure thresholds
- **[Literature](literature/README.md)** — the library, and why each paper is in it
  · **[reading order](literature/summaries.md)** · **[code and data](literature/artifacts.md)**
- **Paper** — [PDF](https://github.com/MykolaVaskevych/Paper/blob/main/build/default/default.pdf)
  · [LaTeX source](https://github.com/MykolaVaskevych/Paper)
  · [live on Overleaf](https://www.overleaf.com/read/gpwqvbpkffkp#9d77de)

The paper is its own repo, pulled in here as a submodule, because Overleaf syncs straight into
it. GitHub shows it above as a pointer rather than a folder, so the three links go there
directly. The PDF is committed, so it can be read without a LaTeX setup.

## References

Zotero owns the bibliography. The `disertation` collection is the single source of truth, and
Better BibTeX auto-exports it to **`paper/src/bibs/ref.bib`**, which is the file `main.tex` reads
through `\bibliography{bibs/ref}`. Add a paper in Zotero and the export follows within seconds.

`ref.bib` is therefore machine-written and must never be hand-edited — anything typed into it is
lost on the next export. There are currently 33 entries, matching the 33 papers in the collection
exactly, sorted into four subcollections by what they are for: foundations, read-and-reproduce,
needed for the experiments, and current work to argue with.

Every entry was verified against OpenAlex, the arXiv API, or the publisher's own proceedings
listing before it went in. [literature/artifacts.md](literature/artifacts.md) records which of
those papers ship runnable code or a usable dataset, with every link checked.

## Experiments

One folder each. Every README says what it asked, what the threshold was, and what came back.

- **[first-look](experiments/first-look)** — TLS record sizes read off real packets. Encryption
  hides what is in a record, not how big it is.
- **[token-batching](experiments/token-batching)** — does one streamed event carry one token?
  Yes, but OpenAI pads every event to a constant size, which closes the channel.
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
