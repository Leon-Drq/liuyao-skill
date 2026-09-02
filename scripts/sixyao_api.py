#!/usr/bin/env python3
"""Small dependency-free client for documented 6yao calculation endpoints."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENDPOINTS = {
    "liuyao": "/api/divination/calculate-hexagram",
    "meihua": "/api/sixya/meihua/calculate",
    "qimen": "/api/qimen/calculate",
    "bazi": "/api/bazi",
    "ziwei": "/api/ziwei/chart",
}


def load_payload(raw: str | None, file_name: str | None) -> dict:
    if bool(raw) == bool(file_name):
        raise ValueError("provide exactly one of --data or --file")
    text = raw if raw is not None else Path(file_name).read_text(encoding="utf-8")
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("payload must be a JSON object")
    return value


def request_json(capability: str, payload: dict, timeout: float) -> object:
    base_url = os.environ.get("SIXYAO_BASE_URL", "https://www.6yao.ai").rstrip("/")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    api_key = os.environ.get("SIXYAO_API_KEY")
    access_token = os.environ.get("SIXYAO_ACCESS_TOKEN")
    if api_key:
        headers["x-api-key"] = api_key
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    request = Request(
        base_url + ENDPOINTS[capability],
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capability", choices=sorted(ENDPOINTS))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--data", help="request JSON object")
    group.add_argument("--file", help="UTF-8 JSON request file")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    try:
        result = request_json(args.capability, load_payload(args.data, args.file), args.timeout)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": "http_error", "status": exc.code, "body": body}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (URLError, TimeoutError) as exc:
        print(json.dumps({"error": "network_error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 3
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "input_error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 4

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
