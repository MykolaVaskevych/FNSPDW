#!/bin/bash
# Save packets to a file, then show what is in them.
#
# usage:  ./capture.sh <iface> <seconds> <filter>
# e.g.    ./capture.sh lo 10 'tcp port 9443'
#
# The filter is required. The kernel applies it before packets reach dumpcap,
# so anything that does not match is never written to the file. Point it at the
# lab port only. Nothing personal then ends up in a capture.
#
# dumpcap writes packets down and nothing else, so it keeps up with fast
# traffic. tshark reads the file afterwards. Neither needs sudo: dumpcap has
# cap_net_raw and the user is in the wireshark group.

set -euo pipefail

IFACE=${1:?need an interface, e.g. lo}
SECS=${2:?need a duration in seconds}
FILTER=${3:?need a filter, e.g. 'tcp port 9443' - do not capture everything}

mkdir -p out
OUT="out/$(date +%Y%m%d-%H%M%S).pcap"

dumpcap -i "$IFACE" -a duration:"$SECS" -f "$FILTER" -w "$OUT" -q

echo "saved $OUT"
echo

echo "--- packets ---"
tshark -r "$OUT" 2>/dev/null | head -30

echo
echo "--- TLS record sizes ---"
# The record length is sent in the clear. Encryption hides what is inside a
# record, not how big it is. One packet can hold several records.
tshark -r "$OUT" -Y 'tls.record.length' -T fields \
	-e frame.number -e frame.len -e tls.record.length 2>/dev/null | head -20
