#!/usr/bin/env python3
"""Print the list of configurations to run, as JSON, for the Actions matrix.

With no argument (or an empty / "all" argument) it prints every *enabled*
configuration. With a single configuration name it prints just that one
(regardless of its enabled flag), which is how the workflow_dispatch
single-config input is honored. An unknown name is an error.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    with open(REPO_ROOT / "configs.toml", "rb") as fh:
        conf = tomllib.load(fh)
    configs = conf["configs"]

    requested = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if requested and requested.lower() != "all":
        if requested not in configs:
            print(f"unknown config '{requested}'; known: "
                  f"{', '.join(configs)}", file=sys.stderr)
            return 1
        names = [requested]
    else:
        names = [n for n, c in configs.items() if c.get("enabled", False)]

    print(json.dumps(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
