# My Dissertation

What encrypted web traffic still reveals through packet size, timing and direction, and
whether padding defences actually help.

MSc Future Networked Systems, Trinity College Dublin. Supervisor: Stephen Farrell.

## Read

- **[Plan](PLAN.md)** — month by month to submission in August 2027
- **Paper** — [PDF](https://github.com/MykolaVaskevych/Paper/blob/main/build/default/default.pdf)
  · [LaTeX source](https://github.com/MykolaVaskevych/Paper)
  · [live on Overleaf](https://www.overleaf.com/read/gpwqvbpkffkp#9d77de)

The paper is its own repo, pulled in here as a submodule, because Overleaf syncs straight into
it. GitHub shows it above as a pointer rather than a folder, so the three links go there
directly. The PDF is committed, so it can be read without a LaTeX setup.

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
