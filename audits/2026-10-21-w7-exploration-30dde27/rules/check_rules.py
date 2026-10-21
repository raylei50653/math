#!/usr/bin/env python3
"""Small local controls for the paper phase-slip lemma; no source search."""

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INPUTS = [
    "audits/2026-10-21-w7-remaining-two-13e51db/REPORT.md",
    "audits/2026-10-21-w7-profile0-13e51db/PROOF.md",
    "audits/2026-10-21-w7-private-face-points-d23f94f/PROOF.md",
    "audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md",
]


def compositions(total, slots):
    if slots == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, slots - 1):
            yield (first,) + rest


def arc(profile, lengths):
    """Each item is (name, colour domain); endpoints a=0 and q=3."""
    result = [("a", (0,))]
    offset = 0
    if profile == 0:
        for j in reversed(range(lengths[0])):
            result.append((f"Hn[{j}]", (0, 2, 3)))
        result.append(("z1", (0, 3)))
        offset = 1
    # In profile 1 a=z1, so a is already the first endpoint.
    for i, forbidden in enumerate((2, 1, 2, 1, 2)):
        for j in range(lengths[i + offset]):
            result.append((f"H{i + 1}[{j}]", tuple(c for c in range(4) if c != forbidden)))
        if i < 4:
            result.append((f"z{i + 2}", (0, 3)))
    result.append(("q", (3,)))
    return result


def main():
    stats = []
    for profile in (0, 1):
        row = {
            "profile": profile,
            "shapes": 0,
            "raw_assignments": 0,
            "proper_assignments": 0,
            "barrier_positive_assignments": 0,
            "one_barrier_assignments": 0,
            "wrong_parity_control_rejected": False,
            "K1_wrong_phase_control_rejected": False,
        }
        for total in range(4):
            for lengths in compositions(total, 6 if profile == 0 else 5):
                row["shapes"] += 1
                items = arc(profile, lengths)
                for colours in itertools.product(*(domain for _, domain in items)):
                    row["raw_assignments"] += 1
                    if any(a == b for a, b in zip(colours, colours[1:])):
                        continue
                    row["proper_assignments"] += 1
                    barriers = [j for j, c in enumerate(colours) if c in (1, 2)]
                    if not barriers:
                        continue
                    row["barrier_positive_assignments"] += 1
                    if any(b == a + 1 for a, b in zip(barriers, barriers[1:])):
                        raise ValueError("Two adjacent barriers survived the original local rules")
                    if any(not items[j][0].startswith("H") for j in barriers):
                        raise ValueError("A barrier was placed on a fixed 03 point")
                    slips = [int(colours[j - 1] != colours[j + 1]) for j in barriers]
                    expected = ((1 if profile == 0 else 0) + total) % 2
                    if sum(slips) % 2 != expected:
                        raise ValueError("Paper phase-slip identity failed")
                    # Deliberately use the other profile's identity.
                    if sum(slips) % 2 != 1 - expected:
                        row["wrong_parity_control_rejected"] = True
                    if len(barriers) == 1:
                        row["one_barrier_assignments"] += 1
                        j = barriers[0]
                        if any(c not in (0, 3) for c in colours[:j] + colours[j + 1:]):
                            raise ValueError("A one-barrier arc has another 12 point")
                        if total == 1:
                            required_slip = profile
                            if slips != [required_slip]:
                                raise ValueError("K=1 phase consequence failed")
                            if slips != [1 - required_slip]:
                                row["K1_wrong_phase_control_rejected"] = True
        if not all(row[k] for k in ("wrong_parity_control_rejected", "K1_wrong_phase_control_rejected")):
            raise ValueError("A negative control was not exercised")
        stats.append(row)
    print(json.dumps({
        "scope": "local arc colourings with K <= 3; full source hypotheses not triggered",
        "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS},
        "results": stats,
        "source_exclusion": False,
        "arbitrary_K_authority": "REPORT.md paper proof, not this finite control",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
