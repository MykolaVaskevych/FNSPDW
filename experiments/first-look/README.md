# first-look — capture packets and read the TLS record sizes off them

A tool, not a hypothesis, so there is no failure threshold. It exists to make the central claim
of the project visible on real packets before any of it gets measured properly.

## What it shows

TLS encrypts the contents of a record. It does not hide the record's length, which is sent in
the clear in the header. `capture.sh` prints those lengths next to the frame they arrived in, so
you can see the two things that matter:

- the sizes are readable without any key
- one packet often holds several records, so counting packets understates what an observer sees

The first real run put six records in a single 1089-byte packet.

## Running it

```bash
cd experiments/first-look
./capture.sh lo 10 'tcp port 9443'
```

Interface, seconds, filter. The filter is required and the script refuses without one: the
kernel applies it before packets reach `dumpcap`, so anything that does not match is never
written to disk. Point it at the lab port only. That is the whole reason no personal traffic
can end up in a capture.

No `sudo` — `dumpcap` has `cap_net_raw` and the user is in the `wireshark` group.
