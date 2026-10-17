#!/usr/bin/env python3
"""Complete local calibration for C1; no named source is instantiated."""
import argparse
import json
from pathlib import Path


def edge(a, b):
    return tuple(sorted((a, b)))


def has_cycle(vertices, edges):
    parent = {v: v for v in vertices}

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for a, b in edges:
        if a not in vertices or b not in vertices:
            continue
        x, y = root(a), root(b)
        if x == y:
            return True
        parent[x] = y
    return False


def reconstruct():
    x = set(range(7))
    ports = (1, 2, 4, 5, 6)
    cycle = [edge(i, (i + 1) % 7) for i in range(7)]
    edges = set(cycle) | {edge(0, 3)}
    edges |= {edge(a + 7, b + 7) for a, b in tuple(edges)}
    edges |= {edge(v, v + 7) for v in ports}
    all_vertices = set(range(14))
    assert all(sum(v in ab for ab in edges) == 3 for v in all_vertices)
    records = []
    for f in cycle:
        for p in ports:
            e = edge(p, p + 7)
            if set(e) & set(f):
                continue
            choices = []
            for a in sorted(set(f) - {0, 3}):
                y = x - {a}
                cut = sorted(ab for ab in edges if len(set(ab) & y) == 1)
                assert len(cut) == 6 and e in cut and f in cut
                assert has_cycle(y, edges)
                assert has_cycle(all_vertices - y, edges)
                opposite = (0, 3, 4, 5, 6) if a in {1, 2} else (0, 1, 2, 3)
                assert set(opposite) <= y
                assert all(edge(opposite[i], opposite[(i + 1) % len(opposite)]) in edges
                           for i in range(len(opposite)))
                choices.append({"a": a, "Y": sorted(y), "cut": cut,
                                "intact_cycle": list(opposite)})
            assert choices
            records.append({"e": e, "f": f, "choices": choices})
    assert len(records) == 25
    # The dual nonincidence hypothesis matters: this incident placement
    # loses e from delta(X\{a}) and is not a valid marked-six witness.
    bad_y = x - {1}
    bad_cut = {ab for ab in edges if len(set(ab) & bad_y) == 1}
    assert edge(1, 8) not in bad_cut and edge(0, 1) in bad_cut
    value = {"schema": "C1-cap-calibration-v1", "vertices": sorted(all_vertices),
             "edges": sorted(edges), "placements": records,
             "placement_count": 25, "source_status": "not triggered"}
    return json.loads(json.dumps(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("create", "check"))
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    rebuilt = reconstruct()
    if args.mode == "create":
        with args.certificate.open("x") as handle:
            json.dump(rebuilt, handle, indent=2, sort_keys=True)
            handle.write("\n")
    else:
        assert json.loads(args.certificate.read_text()) == rebuilt, "certificate mismatch"
    print(json.dumps({"result": "PASS", "placements": 25,
                      "source_status": "not triggered"}, sort_keys=True))


if __name__ == "__main__":
    main()
