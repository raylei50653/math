#!/usr/bin/env python3
"""Read-only replay of custody and finite controls, not a source theorem."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(relative, *args):
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *map(str, args)],
        text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interface-certificate", type=Path,
                        default=ROOT / "A/interface-certificate.json")
    parser.add_argument("--controls-certificate", type=Path,
                        default=ROOT / "C/certificate-v2.json")
    args = parser.parse_args()
    custody = run("check_inputs.py")
    interface = run("A/check_interface.py")
    if interface != json.loads(args.interface_certificate.read_text()):
        raise ValueError("interface certificate differs from full replay")
    controls = run("C/check.py", args.controls_certificate)
    print(json.dumps({
        "base": custody["base"],
        "frozen_inputs": custody["frozen_inputs"],
        "immutable_drift": custody["immutable_drift"],
        "spoke_masks": len(interface["all_32_spoke_fibres"]),
        "local_matching_states": interface["local_matching_states"],
        "states_without_internal_odd_cycle":
            interface["states_without_internal_odd_cycle"],
        "interface_negative_checks": interface["negative_checks"],
        "fixed_controls": controls["controls"],
        "source_realizability": "not triggered",
        "paper_status": "conditional repair; universal existence OPEN",
        "new_lean_theorem": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError,
            subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
