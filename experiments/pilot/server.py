"""Fake SSE streaming server: emits a chosen response token-by-token with
realistic inter-token delays. The client sends a one-line index selecting which
text from the registry to stream, so one server can serve a whole corpus."""

import argparse
import random
import socket
import time

import corpus

# Inter-token delay model. A real decoder emits at a near-constant rate set by
# the forward pass; PAUSE adds structural hesitation at clause boundaries,
# which is the part most likely to be an artefact of this fake server.
GAP_MEAN, GAP_SD = 0.013, 0.004
PAUSE = (0.02, 0.05)


def read_line(conn, limit=64):
    buf = b""
    while b"\n" not in buf and len(buf) < limit:
        d = conn.recv(limit)
        if not d:
            break
        buf += d
    return buf.split(b"\n")[0].decode(errors="replace")


def stream(conn, text, pause=True):
    """`text` is either a string (split on whitespace) or a pre-tokenized list
    of pieces, so the caller can stream real subword tokens."""
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    for tok in (text.split() if isinstance(text, str) else text):
        if not tok:
            continue
        try:
            conn.sendall(f"data: {tok}\n\n".encode())
        except (BrokenPipeError, ConnectionResetError):
            return
        gap = random.gauss(GAP_MEAN, GAP_SD)
        if pause and tok[-1] in ".!?;:,":
            gap += random.uniform(*PAUSE)
        time.sleep(max(0.003, gap))


def serve(port, texts, host="127.0.0.1", pause=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(16)
    while True:
        conn, _ = s.accept()
        try:
            idx = int(read_line(conn) or 0)
        except ValueError:
            idx = 0
        stream(conn, texts[idx % len(texts)], pause)
        conn.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", choices=("MED", "GEN"), default="MED")
    ap.add_argument("--port", type=int, default=9001)
    a = ap.parse_args()
    serve(a.port, corpus.MED if a.topic == "MED" else corpus.GEN)
