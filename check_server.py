#!/usr/bin/env python3
"""Quick check that a llama-server is up.

Usage: python check_server.py http://localhost:8080 [--timeout 5]
Accepts the base URL with or without a trailing /v1. Exit 0 if healthy, 1 otherwise.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request


def get(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--timeout", type=float, default=5)
    args = p.parse_args()

    base = args.url.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]

    try:
        status, _ = get(f"{base}/health", args.timeout)
    except urllib.error.HTTPError as e:
        # llama-server returns 503 while the model is still loading
        print(f"NOT READY: /health returned {e.code}")
        return 1
    except Exception as e:
        print(f"DOWN: {e}")
        return 1

    print(f"UP: /health returned {status}")
    try:
        _, body = get(f"{base}/v1/models", args.timeout)
        for m in json.loads(body).get("data", []):
            print(f"model: {m['id']}")
    except Exception as e:
        print(f"(could not list models: {e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
