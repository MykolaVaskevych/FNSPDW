"""Passive capture: connect, then record only what an on-path observer sees --
per-chunk byte size and arrival time, read off the socket (not server logs)."""

import argparse
import socket
import time


def capture(host, port, index=0, timeout=15.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.settimeout(timeout)
    s.connect((host, port))
    s.sendall(f"{index}\n".encode())  # request line selects the response
    trace = []  # list of (byte_size, arrival_time)
    try:
        while True:
            data = s.recv(65536)
            if not data:
                break
            trace.append((len(data), time.perf_counter()))
    except socket.timeout:
        pass
    finally:
        s.close()
    if trace:  # normalise timestamps to first arrival
        t0 = trace[0][1]
        trace = [(sz, t - t0) for sz, t in trace]
    return trace


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9001)
    tr = capture(ap.parse_args().host, ap.parse_args().port)
    print(f"{len(tr)} chunks, {sum(s for s, _ in tr)} bytes, "
          f"{tr[-1][1]*1000:.0f} ms" if tr else "no data")
