#!/usr/bin/env python3
"""Independent small combinatorial checks; not a topology/completeness proof."""
import argparse
import collections
import itertools
import json
from pathlib import Path


def compute():
    triangle_tables = {}
    for n in range(4, 7):
        classes = {}
        triangles = list(itertools.combinations(range(n), 3))
        for triple in itertools.combinations(triangles, 3):
            if set().union(*map(set, triple)) != set(range(n)):
                continue
            edge_uses = collections.Counter(
                edge for triangle in triple
                for edge in itertools.combinations(triangle, 2)
            )
            if max(edge_uses.values()) > 2:
                continue
            degrees = collections.Counter(v for edge in edge_uses for v in edge)
            lower_excess = sum(max(degrees[v], 3) - 2 for v in range(n))
            if lower_excess > 6:
                continue
            key = (tuple(sorted(degrees.values())), lower_excess, len(edge_uses))
            if key not in classes:
                classes[key] = {"count": 0, "example": [list(t) for t in triple]}
            classes[key]["count"] += 1
        triangle_tables[str(n)] = [
            {"degree_sequence": list(key[0]), "lower_excess": key[1],
             "edges": key[2], **value}
            for key, value in sorted(classes.items())
        ]
    assert [x["degree_sequence"] for x in triangle_tables["4"]] == [[3, 3, 3, 3]]
    assert [x["degree_sequence"] for x in triangle_tables["5"]] == [[2, 2, 3, 3, 4]]
    assert triangle_tables["6"] == []

    counts = []
    for r in range(8, 14):
        # Coefficients of (1+x+y+xy)^2 (x+y+xy)^(r-5).
        coefficients = {(0, 0): 1}
        for position in range(r - 3):
            choices = ((0, 0), (1, 0), (0, 1), (1, 1)) if position < 2 else ((1, 0), (0, 1), (1, 1))
            following = collections.defaultdict(int)
            for (b, u), multiplicity in coefficients.items():
                for db, du in choices:
                    following[b + db, u + du] += multiplicity
            coefficients = following
        by_d = [coefficients.get((5 - d, 3), 0) for d in (0, 1)]
        counts.append({"r": r, "apex_increment_0": by_d[0],
                       "apex_increment_1": by_d[1], "both_orientations": 2 * sum(by_d)})
    assert [x["both_orientations"] for x in counts] == [96, 408, 840, 912, 504, 112]
    return {"scope": "Triangle incidence and attachment-word count corroboration only; no graph coloring or topology oracle.",
            "triangle_classes": triangle_tables, "attachment_counts": counts,
            "templates": sum(x["both_orientations"] for x in counts)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Exclusive-create the results file.")
    args = parser.parse_args()
    results = compute()
    target = Path(__file__).with_name("triangle_and_count_results.json")
    if args.write:
        with target.open("x") as stream:
            json.dump(results, stream, indent=2, sort_keys=True)
            stream.write("\n")
    else:
        assert json.loads(target.read_text()) == results
    print(json.dumps({"status": "PASS", "templates": results["templates"],
                      "triangle_vertex_counts": [4, 5, 6]}, sort_keys=True))


if __name__ == "__main__":
    main()
