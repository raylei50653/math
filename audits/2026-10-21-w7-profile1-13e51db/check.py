#!/usr/bin/env python3
"""Exact local replacement audit; no source-graph enumeration or source exclusion."""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASE = "13e51db3ec3d8d7ec7eeef60167afdc19ad956c4"
INPUTS = (
    "audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md",
    "audits/2026-10-20-r6-941-j1-five-edge-417732f/geometry/PROOF.md",
    "audits/2026-10-21-w7-private-face-points-d23f94f/PROOF.md",
)
BOUNDARY = ("a", "b", "q", "L", "R", "u4")
BOUNDARY_EDGES = [(i, (i + 1) % 6) for i in range(6)]
SOURCE_EDGES = BOUNDARY_EDGES + [(6, 7), (7, 8), (8, 6)] + [
    (v, b)
    for v, contacts in ((6, (0, 1, 2)), (7, (2, 3, 4)), (8, (4, 5, 0)))
    for b in contacts
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def lifts(state, edges, count):
    return [
        list(t)
        for t in itertools.product(range(4), repeat=count)
        if all((state + t)[a] != (state + t)[b] for a, b in edges)
    ]


def crossing(e, f):
    a, b = e
    c, d = f
    return a < c < b < d or c < a < d < b


def generate():
    custody = []
    for name in INPUTS:
        original = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT)
        current = (ROOT / name).read_bytes()
        frozen_path = HERE / "frozen" / name
        frozen = frozen_path.read_bytes()
        require(original == frozen, f"frozen BASE byte mismatch: {name}")
        require(original == current, f"BASE byte mismatch: {name}")
        custody.append({"path": name, "frozen_path": str(frozen_path.relative_to(HERE)),
                        "bytes": len(original), "sha256": hashlib.sha256(original).hexdigest()})

    states = [
        s for s in itertools.product(range(4), repeat=6)
        if s[0] == 0
        and all(s[i] != s[(i + 1) % 6] for i in range(6))
        and all(s[i] <= max(s[:i], default=-1) + 1 for i in range(6))
    ]
    source_fibres = [lifts(s, SOURCE_EDGES, 3) for s in states]
    source_relation = sum(1 << j for j, fibre in enumerate(source_fibres) if fibre)
    diags = [(a, b) for a in range(6) for b in range(a + 1, 6) if b - a not in (1, 5)]
    equal_witnesses = []
    for a, b in diags:
        j = next(j for j, s in enumerate(states) if s[a] == s[b] and source_fibres[j])
        equal_witnesses.append({"pair": [a, b], "state": j, "lift": source_fibres[j][0]})

    dissections = []
    for bits in itertools.product((0, 1), repeat=len(diags)):
        chords = [d for d, bit in zip(diags, bits) if bit]
        if any(crossing(e, f) for e, f in itertools.combinations(chords, 2)):
            continue
        cells = [tuple(range(6))]
        for a, b in chords:
            for q, cell in enumerate(cells):
                if a not in cell or b not in cell:
                    continue
                i, j = sorted((cell.index(a), cell.index(b)))
                if j - i in (1, len(cell) - 1):
                    continue
                cells.pop(q)
                cells.extend((cell[i:j + 1], cell[j:] + cell[:i + 1]))
                break
            else:
                raise ValueError("chord failed to split a cell")
        dissections.append((chords, cells))

    candidates = []
    for chords, cells in dissections:
        for allocation in itertools.product(range(3), repeat=len(cells)):
            count = sum(allocation)
            if count > 2 or any(t == 0 and len(cell) != 3 for t, cell in zip(allocation, cells)):
                continue
            variants = []
            for t, cell in zip(allocation, cells):
                z = len(cell)
                if t == 0:
                    variants.append([[]])
                elif t == 1:
                    variants.append([[(-1, b) for b in cell]])
                else:
                    variants.append([
                        [(-1, -2)]
                        + [(-1, cell[h]) for h in range(i, j + 1)]
                        + [(-2, cell[h % z]) for h in range(j, z + i + 1)]
                        for i in range(z) for j in range(i + 1, z)
                    ])
            for selected in itertools.product(*variants):
                edges = BOUNDARY_EDGES + chords
                next_vertex = 6
                for t, additional in zip(allocation, selected):
                    edges += [
                        (next_vertex - a - 1 if a < 0 else a, next_vertex - b - 1 if b < 0 else b)
                        for a, b in additional
                    ]
                    next_vertex += t
                edges = sorted({tuple(sorted(e)) for e in edges})
                fibres = [lifts(s, edges, count) for s in states]
                relation = sum(1 << j for j, fibre in enumerate(fibres) if fibre)
                extra = relation & ~source_relation
                require(extra != 0, "found a smaller subset replacement: investigate before publication")
                witness = next(j for j in range(len(states)) if extra >> j & 1)
                candidates.append({
                    "inner_count": count,
                    "edges": [list(e) for e in edges],
                    "relation": relation,
                    "extra_rows": extra.bit_count(),
                    "rejected_by_source": witness,
                    "candidate_lift": fibres[witness][0],
                })
    require(len(states) == 31 and source_relation.bit_count() == 14, "source relation calibration")
    counts = [sum(c["inner_count"] == n for c in candidates) for n in range(3)]
    require(counts == [14, 84, 504], "replacement coverage calibration")
    require(len(dissections) == 45, "dissection coverage calibration")
    require(min(c["extra_rows"] for c in candidates) == 3, "introduced-row calibration")
    require(not source_fibres[states.index((0, 1, 0, 1, 0, 1))], "alternating source row must be empty")
    return {
        "base": BASE,
        "inputs": custody,
        "scope": "profile1 local C6 patch only; source exclusion OPEN",
        "boundary": list(BOUNDARY),
        "source_internal": ["p", "h", "n"],
        "source_edges": [list(e) for e in sorted({tuple(sorted(e)) for e in SOURCE_EDGES})],
        "states": [list(s) for s in states],
        "source_full_fibres": source_fibres,
        "source_relation": source_relation,
        "nonedge_equal_witnesses": equal_witnesses,
        "dissection_count": len(dissections),
        "candidate_counts": counts,
        "candidates": candidates,
        "subset_candidate_count": 0,
        "source_realizability": "not triggered",
        "profile1_exclusion": "OPEN",
    }


def verify(stored, expected):
    require(stored == expected, "certificate differs from independently regenerated complete relation audit")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    expected = generate()
    if args.write:
        with args.certificate.open("x") as handle:
            handle.write(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    verify(json.loads(args.certificate.read_text()), expected)
    if args.controls:
        mutations = []
        value = copy.deepcopy(expected)
        value["source_full_fibres"][0] = [[2, 3, 2]]
        mutations.append(("fabricated alternating source lift", value))
        value = copy.deepcopy(expected)
        value["candidates"].pop()
        mutations.append(("omitted smaller candidate", value))
        value = copy.deepcopy(expected)
        value["candidates"][0]["candidate_lift"] = [0]
        mutations.append(("corrupted complete candidate lift", value))
        value = copy.deepcopy(expected)
        value["subset_candidate_count"] = 1
        mutations.append(("false subset candidate", value))
        value = copy.deepcopy(expected)
        value["profile1_exclusion"] = "CLOSED"
        mutations.append(("unsupported source exclusion", value))
        for label, broken in mutations:
            try:
                verify(broken, expected)
            except ValueError:
                print(f"REJECT {label}")
            else:
                raise ValueError(f"control accepted: {label}")
    print(json.dumps({
        "status": "PASS", "base": BASE, "source_rows": 31,
        "source_nonempty": 14, "source_empty": 17,
        "smaller_candidate_counts": expected["candidate_counts"],
        "subset_candidates": 0, "minimum_introduced_empty_rows": 3,
        "profile1_exclusion": "OPEN", "source_realizability": "not triggered",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
