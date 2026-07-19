#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.reunion_flyer import DEFAULT_CONTRACT_PATH, ReunionFlyerError, build_artifacts, validate_artifacts  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate the Onward reunion flyer and phone QR card.")
    parser.add_argument("action", choices=("build", "validate", "all"))
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--skip-independent-decode", action="store_true")
    args = parser.parse_args()
    try:
        result: dict[str, object] = {}
        if args.action in {"build", "all"}:
            result["build"] = build_artifacts(args.contract)
        if args.action in {"validate", "all"}:
            result["validation"] = validate_artifacts(args.contract, decode=not args.skip_independent_decode)
    except ReunionFlyerError as exc:
        parser.exit(1, f"reunion-flyer: ERROR: {exc}\n")
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
