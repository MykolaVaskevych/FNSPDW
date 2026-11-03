"""Shaping proxy between server and client.

Defence layers, cumulative:
  pad      - every forwarded chunk padded to a fixed size
  clock    - chunks released on a fixed tick, not when they arrive
  cover    - a padding-only chunk on every IDLE tick (stage 3): without this
             the clock skips ticks whenever the buffer is empty, and the skip
             pattern still leaks structure
  quantum  - keep emitting cover until the chunk count reaches a multiple of
             `quantum` (and at least `min_chunks`), so count and total duration
             are quantised rather than exact

No TLS, no framework -- a socket relay.
"""

import argparse
import queue
import socket
import threading
import time

FIXED_SIZE = 64
TICK = 0.022

STATS = []  # one dict per completed connection (in-process instrumentation)
LIVE = {"queue": 0, "emitted": 0, "blocked_s": 0.0}  # live view of one connection
_LOCK = threading.Lock()


def pad(chunk):
    if len(chunk) >= FIXED_SIZE:
        return chunk[:FIXED_SIZE]
    return chunk + b":" + b"x" * (FIXED_SIZE - len(chunk) - 2) + b"\n"


def cover():
    return b":" + b"x" * (FIXED_SIZE - 2) + b"\n"


def handle(client, up_host, up_port, mode="full", quantum=0, min_chunks=0):
    use_cover = mode == "full"
    up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    up.connect((up_host, up_port))
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    try:  # forward the client's request line so the server picks the response
        req = client.recv(64)
        up.sendall(req if req else b"0\n")
    except (BrokenPipeError, ConnectionResetError, OSError):
        req = b""

    q, done = queue.Queue(), threading.Event()

    def reader():
        while True:
            try:
                d = up.recv(65536)
            except OSError:
                break
            if not d:
                break
            q.put(d)
        done.set()

    threading.Thread(target=reader, daemon=True).start()

    t0 = time.perf_counter()
    emitted = real = cov = 0
    t_first_real = None
    target = None
    disconnected = False
    blocked = 0.0
    next_t = t0 + TICK
    max_q = 0
    while True:
        now = time.perf_counter()
        if now < next_t:
            time.sleep(next_t - now)
        next_t += TICK
        max_q = max(max_q, q.qsize())
        LIVE["queue"], LIVE["emitted"] = q.qsize(), emitted
        try:
            chunk = q.get_nowait()
        except queue.Empty:
            chunk = None
        if chunk is None and done.is_set():
            if target is None:  # upstream finished: decide the padded target
                target = max(min_chunks,
                             -(-emitted // quantum) * quantum if quantum else emitted)
            if emitted >= target:
                break
        if chunk is None and not use_cover:
            if done.is_set() and target is not None and emitted >= target:
                break
            continue  # skip the tick -- the leak stage 3 is meant to close
        payload = pad(chunk) if chunk is not None else cover()
        _tb = time.perf_counter()
        try:
            client.sendall(payload)   # blocks once the socket buffer fills
        except (BrokenPipeError, ConnectionResetError, OSError):
            disconnected = True
            break
        blocked += time.perf_counter() - _tb
        LIVE["blocked_s"] = blocked
        emitted += 1
        if chunk is not None:
            real += 1
            if t_first_real is None:
                t_first_real = time.perf_counter() - t0
        else:
            cov += 1

    dur = time.perf_counter() - t0
    up.close()
    client.close()
    with _LOCK:
        STATS.append({"real": real, "cover": cov, "emitted": emitted,
                      "bytes": emitted * FIXED_SIZE, "cover_bytes": cov * FIXED_SIZE,
                      "t_first_real": t_first_real, "duration": dur,
                      "disconnected": disconnected, "max_queue": max_q,
                      "blocked_s": blocked,
                      "upstream_done": done.is_set()})


def serve(port, up_host, up_port, host="127.0.0.1", mode="full", quantum=0,
          min_chunks=0, threaded=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(16)
    while True:
        conn, _ = s.accept()
        args = (conn, up_host, up_port, mode, quantum, min_chunks)
        if threaded:
            threading.Thread(target=handle, args=args, daemon=True).start()
        else:
            handle(*args)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9101)
    ap.add_argument("--up-host", default="127.0.0.1")
    ap.add_argument("--up-port", type=int, default=9001)
    ap.add_argument("--mode", choices=("basic", "full"), default="full")
    ap.add_argument("--quantum", type=int, default=0)
    ap.add_argument("--min-chunks", type=int, default=0)
    ap.add_argument("--threaded", action="store_true")
    a = ap.parse_args()
    serve(a.port, a.up_host, a.up_port, mode=a.mode, quantum=a.quantum,
          min_chunks=a.min_chunks, threaded=a.threaded)
