# token-batching — does one SSE event carry one token?

Written after the fact, on 2026-11-03. The run itself was 2026-10-01.

## What it asks

An LLM answer is streamed back token by token over server-sent events. If one event is one
token, and one event becomes one TLS record, then an observer who cannot read the ciphertext
still sees the byte-length of every token in the answer. That sequence of lengths is a strong
fingerprint, and with the tokenizer known it narrows the candidate text sharply.

So, before building anything on top of that idea: does a real provider actually send one token
per event, and does the event size track the token size?

## Threshold

If event sizes do not vary with token length, the channel is closed at the application layer and
the idea is dead as stated. Stated before the run, because the answer looked obvious and obvious
answers are the ones worth pre-committing to.

## What happened

`gpt-4.1-nano`, one short question, `out/events.tsv`:

```
seconds   bytes  token
0.000210    344  ""          <- role delta, opens the stream
0.009014    312  "Red"
0.009031    312  ","
0.022000    312  " blue"
0.022019    312  ","
0.062267    312  " and"
0.062283    312  " green"
0.093017    312  "."
0.093036    296  ""          <- finish_reason: "stop"
```

One token per event, as expected. Every content event exactly 312 bytes, which was not.

Dumping the raw JSON showed why. Each event carries an `obfuscation` field of random characters
whose length compensates for the token:

| token | token chars | `obfuscation` | event bytes |
|---|---|---|---|
| `"Hi"` | 2 | `XllRC` (5) | 312 |
| `"!"` | 1 | `fTs81B` (6) | 312 |

OpenAI pads every streamed event to a constant size on purpose. The token-length channel is
closed before the bytes reach TLS.

## What it means

The threshold was crossed, so token-length recovery against OpenAI is off the table. Two leaks
survive, and both are about shape rather than content:

- **Event count still equals token count**, so answer length is readable.
- **The terminal event is 296 bytes, not 312.** The padding is applied to content events; the
  one that says `finish_reason: "stop"` is a different size, so the end of an answer is visible
  even if the middle is not.

Timing is also not padded. Events arrive in pairs about 17 µs apart (0.009014/0.009031,
0.022000/0.022019, 0.062267/0.062283) with 13–40 ms between pairs. The decoder emits two tokens
per batch and the pair crosses the network together, so a TLS record probably carries two events,
not one. Unconfirmed — it needs a capture, not a client-side timestamp.

This is the measurement behind dropping the LLM angle. The provider already does the defence the
dissertation was going to propose, which is the answer to a narrow question and the motivation
for the broader one: padding exists in production, so the question worth asking is what it costs
and whether it actually helps.

## Still open

- Does Anthropic pad the same way?
- Does any self-hosted server (Ollama, llama.cpp, vLLM)? Expectation: no.
- Does the padding survive to the wire, or do TLS records merge events and undo it?

## Running it

```bash
cd experiments/token-batching
op run --env-file=.env -- uv run ask.py "name three colours" > out/events.tsv
```

Without 1Password, put your own key in `.env` and drop the `op run` prefix. `.env` holds a
reference, not a secret.
