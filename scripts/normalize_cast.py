#!/usr/bin/env python3
"""Normalize six three-coin throws into the 6yao casting payload."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone


def parse_groups(raw: str) -> list[str]:
    groups = [item.strip().upper() for item in raw.split(",") if item.strip()]
    if len(groups) != 6:
        raise SystemExit("coins must contain exactly six comma-separated groups")
    for group in groups:
        if not re.fullmatch(r"[HT]{3}", group):
            raise SystemExit("each coin group must contain exactly three H/T characters")
    return groups


def type_from_heads(heads: int) -> tuple[str, bool, int, str]:
    if heads == 3:
        return "old_yang", True, 9, "━━━"
    if heads == 2:
        return "young_yin", False, 8, "━ ━"
    if heads == 1:
        return "young_yang", False, 7, "━━━"
    return "old_yin", True, 6, "━ ━"


def binary_for(types: list[str]) -> str:
    yang = {"old_yang", "young_yang"}
    return "".join("1" if item in yang else "0" for item in reversed(types))


def normalize(args: argparse.Namespace) -> dict:
    groups = parse_groups(args.coins)
    yaos = []
    for position, group in enumerate(groups, start=1):
        yao_type, changing, score, symbol = type_from_heads(group.count("H"))
        yaos.append({
            "position": position,
            "type": yao_type,
            "symbol": symbol,
            "isChanging": changing,
            "coins": [
                {"id": index, "result": "heads" if value == "H" else "tails", "isAnimating": False}
                for index, value in enumerate(group)
            ],
            "score": score,
        })

    changing_positions = [yao["position"] for yao in yaos if yao["isChanging"]]
    changed_types = []
    for yao in yaos:
        if yao["type"] == "old_yang":
            changed_types.append("young_yin")
        elif yao["type"] == "old_yin":
            changed_types.append("young_yang")
        else:
            changed_types.append(yao["type"])

    timestamp = args.timestamp or datetime.now(timezone.utc).isoformat()
    parsed_timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    time_info = {
        "year": parsed_timestamp.year,
        "month": parsed_timestamp.month,
        "day": parsed_timestamp.day,
        "hour": parsed_timestamp.hour,
        "minute": parsed_timestamp.minute,
    }
    payload = {
        "yaos": yaos,
        "divinationTimestamp": timestamp,
        "timeInfo": time_info,
        "question": args.question,
    }
    return {
        "question": args.question,
        "timestamp": timestamp,
        "raw_coins": groups,
        "yaos": yaos,
        "original_binary": binary_for([yao["type"] for yao in yaos]),
        "changing_positions": changing_positions,
        "changed_binary": binary_for(changed_types) if changing_positions else None,
        "payload": payload,
        "notes": [
            "第一次投掷是初爻，按 position 1 到 6 保存。",
            "本脚本只规范化起卦，不计算六亲、世应、纳甲、旺衰或 AI 解读。",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a Liu Yao six-throw cast")
    parser.add_argument("--coins", required=True, help="six groups, e.g. HHT,THH,TTT,HHH,HTT,THT")
    parser.add_argument("--question", required=True)
    parser.add_argument("--timestamp")
    parser.add_argument("--out", help="optional JSON output path")
    args = parser.parse_args()
    if not args.question.strip():
        raise SystemExit("question cannot be empty")
    result = normalize(args)
    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
