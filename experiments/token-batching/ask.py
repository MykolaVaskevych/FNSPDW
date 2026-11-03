"""Ask one question. Print the time, size and token of every stream event.

That list is the ground truth for the capture: if the wire shows as many TLS
records as there are events here, one token is one thing an observer can see.

    op run --env-file=.env -- uv run ask.py "why is the sky blue" > out/events.tsv
"""

import json
import os
import sys
import time
from http.client import HTTPSConnection

for line in open(".env"):
    if "=" in line and not line.startswith("#"):
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip())  # op's value wins

conn = HTTPSConnection("api.openai.com", 443)
conn.request("POST", "/v1/chat/completions",
             json.dumps({"model": "gpt-4.1-nano", "stream": True,
                         "messages": [{"role": "user", "content": sys.argv[1]}]}),
             {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
              "Content-Type": "application/json"})

resp = conn.getresponse()
if resp.status != 200:
    sys.exit(f"HTTP {resp.status}: {resp.read()[:200].decode()}")

start = time.perf_counter()
print("seconds\tbytes\ttoken")
while True:
    # readline returns as soon as a line arrives, so the time is when it came off
    # the network, not when some buffer filled up.
    raw = resp.readline()
    if not raw:
        break
    if not raw.startswith(b"data: "):
        continue
    body = raw[6:].strip()
    if body == b"[DONE]":
        break
    token = json.loads(body)["choices"][0]["delta"].get("content", "")
    print(f"{time.perf_counter() - start:.6f}\t{len(raw)}\t{json.dumps(token)}")
