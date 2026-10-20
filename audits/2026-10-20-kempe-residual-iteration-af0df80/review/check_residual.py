#!/usr/bin/env python3
"""Independently reconstruct fixed-cell95 residuals from its graph.

Only the source graph and literal action order are read before reconstruction.
No saved transition or observation table supplies algorithmic results.
"""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / (
    "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/"
    "experiment/certificate.json"
)
PAIRS = tuple(combinations(range(4), 2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raw = SOURCE.read_bytes()
    frozen = json.loads(raw)
    n, edges, boundary = frozen["n"], frozen["edges"], frozen["boundary"]
    assert n == 8 and boundary == list(range(5))
    colors = [c for c in product(range(4), repeat=n)
              if all(c[u] != c[v] for u, v in edges)]
    color_ids = {c: i for i, c in enumerate(colors)}
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    partitions, components = [], []
    for c in colors:
        full, observed = [], []
        for pair in PAIRS:
            remaining = {v for v in range(n) if c[v] in pair}
            blocks = []
            while remaining:
                start = min(remaining)
                remaining.remove(start)
                reached, pending = {start}, deque([start])
                while pending:
                    u = pending.popleft()
                    fresh = adjacency[u] & remaining
                    remaining -= fresh
                    reached |= fresh
                    pending.extend(fresh)
                blocks.append(tuple(sorted(reached)))
            full.append(tuple(blocks))
            observed.append(tuple(sorted(tuple(v for v in block if v < 5)
                                         for block in blocks if any(v < 5 for v in block))))
        components.append(full)
        partitions.append(tuple(observed))
    actions = [(*p, r) for p in PAIRS for r in range(5)]
    trans = []
    for i, c in enumerate(colors):
        row = []
        for a, b, root in actions:
            if c[root] not in (a, b):
                row.append(-1)
                continue
            block = next(block for block in components[i][PAIRS.index((a, b))]
                         if root in block)
            after = tuple(a + b - c[v] if v in block else c[v] for v in range(n))
            row.append(color_ids[after])
        trans.append(row)
    observations = [(c[:5], partitions[i]) for i, c in enumerate(colors)]
    observation_keys = sorted(set(observations))
    observation_lookup = {key: i for i, key in enumerate(observation_keys)}
    obs = [observation_lookup[key] for key in observations]
    fibres = [tuple(i for i, q in enumerate(obs) if q == o)
              for o in range(len(observation_keys))]
    assert len(fibres) == 192

    # Explicit set BFS over reachable nonempty complete-current-coloring sets.
    # Each (R, action, observed_J) has exactly one resulting set or empty.
    reached = set(fibres)
    pending = deque(fibres)
    residual_edges = {}
    while pending:
        residual = pending.popleft()
        for action in range(30):
            buckets = defaultdict(set)
            for source in residual:
                target = trans[source][action]
                if target >= 0:
                    buckets[obs[target]].add(target)
            for observed, values in buckets.items():
                target_set = tuple(sorted(values))
                assert len(target_set) <= len(residual)
                residual_edges[residual, action, observed] = target_set
                if target_set not in reached:
                    reached.add(target_set)
                    pending.append(target_set)
    residuals = sorted(reached, key=lambda r: (len(r), r))
    residual_ids = {r: i for i, r in enumerate(residuals)}
    edge_rows = sorted((residual_ids[r], a, o, residual_ids[t])
                       for (r, a, o), t in residual_edges.items())
    enabled_rows = Counter((r, a) for r, a, o in residual_edges)
    assert all(len({obs[i] for i in r}) == 1 for r in residuals)
    assert all(t in reached for t in residual_edges.values())

    # Compare concrete traces with quotient trace composition without importing
    # old path counts or witnesses.
    quotient_edges = {(obs[i], a, obs[t])
                      for i, row in enumerate(trans)
                      for a, t in enumerate(row) if t >= 0}
    outgoing = defaultdict(set)
    for source, a, target in quotient_edges:
        outgoing[source].add((a, target))
    abstract = {(q0, a, q1, b, q2)
                for q0, a, q1 in quotient_edges
                for b, q2 in outgoing[q1]}
    concrete = {(obs[i], a, obs[j], b, obs[k])
                for i, row in enumerate(trans)
                for a, j in enumerate(row) if j >= 0
                for b, k in enumerate(trans[j]) if k >= 0}
    assert concrete <= abstract

    def run_trace(q0, a, q1, b, q2):
        middle = residual_edges.get((fibres[q0], a, q1), ())
        return residual_edges.get((middle, b, q2), ())

    accepted = {path for path in abstract if run_trace(*path)}
    rejected = abstract - accepted
    assert accepted == concrete
    assert rejected == abstract - concrete
    false = min(rejected)
    q0, a, q1, b, q2 = false
    after_first = residual_edges[fibres[q0], a, q1]
    assert residual_edges.get((after_first, b, q2), ()) == ()
    incompatible = next(i for i in fibres[q1]
                        if trans[i][b] >= 0 and obs[trans[i][b]] == q2)

    # A residual contains present colorings, not unchanged original witnesses.
    moving = next((r, a, o, t)
                  for (r, a, o), t in sorted(residual_edges.items())
                  if set(r).isdisjoint(t))
    r, a, o, t = moving
    assert not set(r) & set(fibres[o])
    assert t

    dense_count = len(residuals) * len(actions) * len(observation_keys)
    result = {
        "source_sha256": sha256(raw).hexdigest(),
        "algorithm": "4^8 proper edge filter; adjacency BFS; direct swaps; residual-set BFS",
        "scope": "Fixed cell95, original ordered B and literal colors, B-rooted actions",
        "source_provenance": "Frozen uncommitted previous-audit input bytes, not Git BASE contents",
        "coloring_count": len(colors),
        "initial_observation_fibre_count": len(fibres),
        "initial_fibre_size_histogram": dict(sorted(Counter(map(len, fibres)).items())),
        "nonempty_residual_count": len(residuals),
        "residual_size_histogram": dict(sorted(Counter(map(len, residuals)).items())),
        "empty_residual": [],
        "state_count_including_empty_reject": len(residuals) + 1,
        "nonempty_observation_transition_count": len(edge_rows),
        "enabled_residual_action_rows": len(enabled_rows),
        "successor_observation_count_histogram": dict(sorted(Counter(enabled_rows.values()).items())),
        "dense_residual_action_observation_domain": dense_count,
        "empty_reject_transition_count": dense_count - len(edge_rows),
        "empty_reject_is_absorbing": True,
        "all_retained_transitions_closed": True,
        "all_retained_transitions_cardinality_nonincreasing": True,
        "two_step": {
            "abstract_paths": len(abstract), "concrete_paths": len(concrete),
            "concrete_accepted": len(accepted), "false_rejected": len(rejected),
            "false_accepted": len(accepted - concrete),
            "concrete_rejected": len(concrete - accepted),
        },
        "negative_controls": {
            "first_false_quotient_trace": {
                "observation_ids": [q0, q1, q2],
                "actions": [actions[a2] for a2 in (false[1], false[3])],
                "initial_lifts": [colors[i] for i in fibres[q0]],
                "actual_middle_lifts": [colors[i] for i in after_first],
                "incompatible_middle_lift": colors[incompatible],
                "actual_residual_after_second_observation": [],
            },
            "unchanged_original_witness_intersection": {
                "original_lifts": [colors[i] for i in r],
                "action": actions[a],
                "observed_after": o,
                "correct_current_residual": [colors[i] for i in t],
                "incorrect_intersection_with_original_lifts": [],
            },
        },
        "colors": colors, "actions": actions, "concrete_transitions": trans,
        "observation_values": observation_keys, "observation_ids_by_coloring": obs,
        "initial_fibres": fibres, "residuals": residuals, "nonempty_edges": edge_rows,
    }
    target = HERE / "independent_residual_certificate.json"
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        assert target.read_bytes() == encoded, "Certificate differs from independent reconstruction"
    else:
        with target.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ("colors", "actions", "concrete_transitions", "observation_values",
                      "observation_ids_by_coloring", "initial_fibres", "residuals",
                      "nonempty_edges")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
