#!/usr/bin/env python3
"""Aggregate per-config results into summary.json and enforce cross-config
invariants.

Reads every <artifacts>/<config>/results.json, then:

  * writes <artifacts>/summary.json keyed by configuration name, carrying the
    .text size and panic-site count for each pass -- suitable for diffing runs;
  * asserts the profile-equality invariant: debug-assertions and overflow-checks
    must be identical across all measured configurations (they generate panic
    sites directly, so if they differ the comparison is meaningless). If they
    differ, this fails the run.

This step never invents numbers; it only reads what run_config.py recorded.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


def load_results(artifacts: Path) -> Dict[str, dict]:
    results = {}
    for results_json in sorted(artifacts.glob("*/results.json")):
        data = json.loads(results_json.read_text())
        results[data["config"]] = data
    return results


def build_summary(results: Dict[str, dict]) -> dict:
    summary = {}
    for name, data in results.items():
        passes = data["passes"]
        summary[name] = {
            "enabled": data.get("enabled", False),
            "description": data.get("description", ""),
            "text_size": {
                "pass1": passes[0]["sizes"][".text"],
                "pass2": passes[1]["sizes"][".text"],
            },
            "panic_sites": {
                "pass1": passes[0]["panic_sites"]["branch_call_sites_total"],
                "pass2": passes[1]["panic_sites"]["branch_call_sites_total"],
            },
            "determinism_ok": (
                data["determinism"]["text_size_match"]
                and data["determinism"]["panic_sites_match"]
            ),
            "effective_profile": {
                k: v["value"] for k, v in data["effective_profile"].items()
            },
        }
    return summary


def check_profile_equality(results: Dict[str, dict]) -> List[str]:
    """debug-assertions and overflow-checks must match across all configs."""
    failures = []
    for field in ("debug-assertions", "overflow-checks"):
        seen = {
            name: data["effective_profile"][field]["value"]
            for name, data in results.items()
        }
        distinct = set(seen.values())
        if len(distinct) > 1:
            failures.append(
                f"{field} differs across configurations (must be identical): "
                + ", ".join(f"{n}={v}" for n, v in seen.items())
            )
    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts", help="dir containing <config>/results.json")
    args = ap.parse_args()

    artifacts = Path(args.artifacts).resolve()
    results = load_results(artifacts)
    if not results:
        print(f"::error::no results.json found under {artifacts}",
              file=sys.stderr)
        return 1

    summary = build_summary(results)
    (artifacts / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

    failures = check_profile_equality(results)
    # Also surface any per-config determinism failure at the summary level.
    for name, data in results.items():
        if not (data["determinism"]["text_size_match"]
                and data["determinism"]["panic_sites_match"]):
            failures.append(f"{name}: determinism check failed "
                            f"({data['determinism']})")

    if failures:
        print("::error::cross-config invariant(s) violated:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\nprofile-equality invariant holds; determinism holds for all configs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
