#!/usr/bin/env python3
"""Complete chorded-seven cap relation; no source-realizability claim."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys


BASE = "5b9a7b3190c84bc10ff99608e372a9b4be57a0f6"
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parent.parent
VERTICES = tuple(range(7))
PORTS = (1, 2, 4, 5, 6)
CHORD = (0, 3)
CYCLE = tuple(sorted(tuple(sorted((i, (i + 1) % 7))) for i in VERTICES))
EDGES = tuple(sorted(CYCLE + (CHORD,)))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def subsets(values):
    for count in range(len(values) + 1):
        yield from itertools.combinations(values, count)


def recursive_matchings(remaining):
    if not remaining:
        return [()]
    first = min(remaining)
    result = []
    for second in sorted(remaining - {first}):
        edge = tuple(sorted((first, second)))
        if edge in EDGES:
            for rest in recursive_matchings(remaining - {first, second}):
                result.append(tuple(sorted((edge,) + rest)))
    return sorted(result)


def exhaustive_matchings(selected):
    """Independent 2^8 internal-edge-subset reconstruction, no recursion."""
    result = []
    for candidate in subsets(EDGES):
        degrees = {vertex: int(vertex in selected) for vertex in VERTICES}
        for u, v in candidate:
            degrees[u] += 1
            degrees[v] += 1
        if all(degree == 1 for degree in degrees.values()):
            result.append(tuple(candidate))
    return sorted(result)


def fragments(edges, vertices):
    """Retain complete labelled paths/cycles, including isolated vertices."""
    adjacency = {vertex: set() for vertex in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(all(len(neighbours) <= 2 for neighbours in adjacency.values()),
            "a retained relation is not a disjoint union of paths and cycles")
    unseen = set(vertices)
    answer = []
    while unseen:
        first = min(unseen)
        component = {first}
        queue = [first]
        while queue:
            vertex = queue.pop()
            for neighbour in adjacency[vertex] - component:
                component.add(neighbour)
                queue.append(neighbour)
        unseen -= component
        endpoints = sorted(v for v in component if len(adjacency[v]) < 2)
        internal_edges = sorted(e for e in edges if set(e) <= component)
        if not internal_edges:
            kind = "isolated"
        elif endpoints:
            require(len(endpoints) == 2, "a path has the wrong endpoint count")
            kind = "path"
        else:
            kind = "cycle"
        answer.append({"kind": kind, "vertices": sorted(component),
                       "endpoints": endpoints, "edges": internal_edges,
                       "length": len(internal_edges),
                       "parity": len(internal_edges) % 2})
    return answer


def input_seals():
    manifest_bytes = (AUDIT / "INPUTS.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest["base"] == BASE, "unexpected frozen BASE")
    result = []
    for entry in manifest["entries"]:
        frozen = (AUDIT / entry["frozen_path"]).read_bytes()
        original = subprocess.run(
            ["git", "show", BASE + ":" + entry["path"]], cwd=REPO,
            check=True, capture_output=True).stdout
        digest = hashlib.sha256(frozen).hexdigest()
        require(digest == entry["sha256"], "frozen input hash drift: " + entry["path"])
        require(frozen == original, "frozen input differs from Git BASE: " + entry["path"])
        result.append({"path": entry["path"], "sha256": digest})
    return {"manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "files": result}


def reconstruct():
    seals = input_seals()
    rows = []
    matchings_count = 0
    three_total = 0
    three_even_allowed = 0
    active_f = []
    for selected in subsets(PORTS):
        recursive = recursive_matchings(set(VERTICES) - set(selected))
        exhaustive = exhaustive_matchings(selected)
        require(recursive == exhaustive, "independent complete matching relations disagree")
        records = []
        for internal in exhaustive:
            matchings_count += 1
            complement = fragments(set(EDGES) - set(internal), VERTICES)
            odd_closed = [part for part in complement
                          if part["kind"] == "cycle" and part["parity"] == 1]
            changed = sorted(set(PORTS) - set(selected))
            # Outer stub of port i has label 7+i.  It is an actual endpoint
            # label, not an independently selectable external witness.
            difference = {CHORD} ^ set(internal)
            difference |= {(port, 7 + port) for port in changed}
            diff_vertices = set(itertools.chain.from_iterable(difference))
            difference_parts = fragments(difference, diff_vertices)
            require(all(part["kind"] == "path" for part in difference_parts),
                    "unexpected detached internal alternating cycle")
            require(len(difference_parts) == len(changed) // 2,
                    "wrong complete difference path count")
            require(sorted(itertools.chain.from_iterable(
                part["endpoints"] for part in difference_parts)) ==
                [7 + port for port in changed], "changed-port endpoint loss")
            for part in difference_parts:
                require(part["length"] % 2 == 1, "local difference path is not odd")
            record = {"internal_matching": internal,
                      "changed_ports": changed,
                      "complement_fragments": complement,
                      "difference_fragments": difference_parts,
                      "compatible_with_local_necessities_of_even_endpoint": not odd_closed}
            records.append(record)
            if len(selected) == 3:
                three_total += 1
                require(len(difference_parts) == 1, "three-spoke difference must be one path")
                if not odd_closed:
                    three_even_allowed += 1
                    closed = [part for part in complement if part["kind"] == "cycle"]
                    paths = [part for part in complement if part["kind"] == "path"]
                    require(len(paths) == 1, "even-endpoint cap must have one complement path")
                    require(paths[0]["length"] in (2, 6), "unexpected even cap path")
                    require([part["length"] for part in closed] in ([], [4]),
                            "unexpected closed even cap component")
                    for f_edge in ((0, 1), (1, 2), (2, 3)):
                        if f_edge in internal:
                            require(f_edge in difference, "active f was lost from the unique path")
                            active_f.append({"f": f_edge, "selected_spokes": selected,
                                             "internal_matching": internal})
            if len(selected) == 5:
                require(internal == (CHORD,), "all-spoke local matching must use the chord")
                require([part["length"] for part in odd_closed] == [7],
                        "all-spoke endpoint must retain the seven-cycle")
        # Every one of the 32 complete spoke rows is retained, even if empty.
        rows.append({"selected_spokes": selected, "matchings": records})
    require(len(rows) == 32 and sum(bool(row["matchings"]) for row in rows) == 12,
            "incomplete complete-row relation")
    require(matchings_count == 15 and three_total == 7 and three_even_allowed == 6,
            "unexpected complete local relation counts")
    require(len(active_f) == 3 and len({tuple(item["f"]) for item in active_f}) == 3,
            "active quadrilateral f specialization incomplete")
    return json.loads(canonical({
        "schema": "r6-seven-cap-complete-local-relation-v1", "base": BASE,
        "authority": "finite local relation; arbitrary-size source input not triggered",
        "input_seals": seals,
        "cap": {"vertices": VERTICES, "cycle_edges": CYCLE, "chord": CHORD,
                "internal_edges": EDGES, "ordered_ports": PORTS,
                "stub_label": "port i has exterior stub 7+i"},
        "rows": rows, "active_quadrilateral_f_cases": active_f,
        "summary": {"spoke_rows": 32, "nonempty_spoke_rows": 12,
                    "internal_matchings": 15, "three_spoke_internal_matchings": 7,
                    "three_spoke_locally_even_compatible_matchings": 6,
                    "source_input_status": "not triggered"}}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--write", type=Path,
                        help="exclusive-create a complete certificate at this new path")
    arguments = parser.parse_args()
    expected = reconstruct()
    if arguments.write is not None:
        with arguments.write.open("x", encoding="utf-8") as output:
            output.write(canonical(expected))
        path = arguments.write
    else:
        path = arguments.certificate
        actual = json.loads(path.read_text(encoding="utf-8"))
        require(actual == expected, "certificate disagrees with full independent reconstruction")
        require(path.read_text(encoding="utf-8") == canonical(expected),
                "certificate bytes are not canonical")
    print(canonical({"result": "PASS", "certificate_sha256":
                     hashlib.sha256(path.read_bytes()).hexdigest(),
                     "frozen_input_drift": 0, **expected["summary"]}).strip())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
