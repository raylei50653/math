#!/usr/bin/env python3
"""General mask13 returns: full disk controls and necessary partition states."""
import argparse
import itertools
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

PINS = ("z", "s", "r", "t", "p", "q")
EDGES = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 5), (5, 0))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
WORDS = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def name(row):
    return "".join("ABCD"[c] for c in row)


def admissible(row, edges):
    if any(row[a] == row[b] for a, b in edges):
        return False
    kind = normalize(row[:4])
    if kind == WORDS[0]:
        return set(row[4:]) == set(range(4)) - set(row[:4])
    if kind == WORDS[2]:
        return set(range(4)) - set(row[:4]) <= set(row[4:])
    if kind == WORDS[3]:
        return set(row[4:]) == {row[1], row[3]}
    return False


def partitions(items):
    if not items:
        yield ()
        return
    first = items[0]
    for rest in partitions(items[1:]):
        yield ((first,),) + rest
        for i, block in enumerate(rest):
            yield rest[:i] + ((first,) + block,) + rest[i + 1:]


def pair_partitions(row, pair, edges):
    vertices = tuple(v for v, c in enumerate(row) if c in pair)
    for part in partitions(vertices):
        labels = {v: i for i, block in enumerate(part) for v in block}
        if all(labels[a] == labels[b] for a, b in edges if a in labels and b in labels):
            yield tuple(sorted(tuple(sorted(block)) for block in part))


def outer_planar(parts):
    labels = {v: i for i, block in enumerate(parts[0] + parts[1]) for v in block}
    return not (labels[0] == labels[2] and labels[1] == labels[3]
                and labels[0] != labels[1])


def switch(row, block, pair):
    a, b = pair
    return tuple(b if c == a and v in block else a if c == b and v in block else c
                 for v, c in enumerate(row))


def orbit(row, parts, split):
    operations = [(block, pair) for groups, pair in zip(parts, split) for block in groups]
    result = set()
    for flags in itertools.product((False, True), repeat=len(operations)):
        target = row
        for use, (block, pair) in zip(flags, operations):
            if use:
                target = switch(target, block, pair)
        result.add(target)
    return frozenset(result)


def block_of(state, vertex, pair):
    for split, parts in zip(SPLITS, state[1]):
        if pair in split:
            return next(block for block in parts[split.index(pair)] if vertex in block)
    raise AssertionError("pair missing")


def partition_case(label, extra):
    edges = EDGES + extra
    rows = [row for row in itertools.product(range(4), repeat=6) if admissible(row, edges)]
    initial = set()
    orbits = {}
    for row in rows:
        options = []
        for j, split in enumerate(SPLITS):
            choices = []
            for parts in itertools.product(*(pair_partitions(row, pair, edges) for pair in split)):
                targets = orbit(row, parts, split)
                if outer_planar(parts) and all(admissible(target, edges) for target in targets):
                    choices.append(parts)
                    orbits[row, j, parts] = targets
            options.append(choices)
        for chosen in itertools.product(*options):
            initial.add((row, chosen))
    live, rounds = set(initial), []
    while True:
        keys = {(row, j, parts[j]) for row, parts in live for j in range(3)}
        dead = {state for state in live if any(
            any((target, j, state[1][j]) not in keys
                for target in orbits[state[0], j, state[1][j]]) for j in range(3))}
        rounds.append({"live_states": len(live), "removed_states": len(dead)})
        if not dead:
            break
        live -= dead
    canonical_states = sorted(state for state in live if normalize(state[0]) == state[0])
    assert len(live) == 24 * len(canonical_states)
    sector_checks = []
    for state in canonical_states:
        row = state[0]
        if row[:4] != WORDS[2]:
            continue
        d_vertex = 4 if row[4] == 3 else 5
        palette = set(row[4:])
        if palette == {2, 3}:
            assert {1, 3} <= set(block_of(state, d_vertex, (1, 3)))
            assert 0 not in block_of(state, 2, (0, 2))
            mobile = 4 if row[4] == 2 else 5
        else:
            assert palette == {1, 3}
            assert 2 in block_of(state, d_vertex, (2, 3))
            assert 0 in block_of(state, 2, (0, 2))
            assert 1 not in block_of(state, 3, (1, 3))
            mobile = 4 if row[4] == 1 else 5
        block = block_of(state, mobile, (1, 2))
        target = switch(row, block, (1, 2))
        assert switch(target, block, (1, 2)) == row
        free = 2 not in block
        if free:
            assert target[:4] == WORDS[2] and set(target[4:]) != palette
        else:
            assert {1, 2, 3} <= set(block)
            reset = tuple(2 if c == 1 else 1 if c == 2 else c for c in target)
            assert reset == row
        sector_checks.append({"row": name(row), "BC_block": block,
                              "free": free, "target": name(target),
                              "same_pair_inverse_recovers_row": True})
    payload = json.dumps(sorted(live), separators=(",", ":")).encode()
    return {"case": label, "extra_edges": extra, "labelled_rows": len(rows),
            "rounds": rounds, "surviving_states": len(live),
            "surviving_pin_orbits": sorted({name(normalize(row)) for row, _ in live}),
            "all_simultaneous_states_in_canonical_frame": canonical_states,
            "sector_return_checks": sector_checks, "all_live_states_sha256": sha256(payload).hexdigest()}


def validate_disk(faces):
    edges = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)])))
                    for f in faces for i in range(len(f))})
    vertices = sorted({v for edge in edges for v in edge})
    darts = Counter((f[i], f[(i + 1) % len(f)])
                    for f in faces for i in range(len(f)))
    assert darts == Counter({d: 1 for a, b in edges for d in ((a, b), (b, a))})
    assert len(vertices) - len(edges) + len(faces) == 2
    adj = {v: {w for a, b in edges if v in (a, b) for w in (a, b) if w != v}
           for v in vertices}
    for v in vertices:
        links = [(f[(i - 1) % len(f)], f[(i + 1) % len(f)])
                 for f in faces for i in range(len(f)) if f[i] == v]
        successor = dict(links)
        assert len(successor) == len(links)
        seen, at = set(), min(adj[v])
        while at not in seen:
            seen.add(at)
            at = successor[at]
        assert seen == adj[v] and at == min(adj[v])
    nonfacial = [triangle for triangle in itertools.combinations(vertices, 3)
                if all(tuple(sorted(edge)) in edges for edge in itertools.combinations(triangle, 2))
                and set(triangle) not in [set(f) for f in faces[1:]]]
    return vertices, edges, adj, nonfacial


def component(adj, row, root, pair):
    reached, pending = {root}, [root]
    while pending:
        for nxt in adj[pending.pop()]:
            if nxt not in reached and row[nxt] in pair:
                reached.add(nxt)
                pending.append(nxt)
    return tuple(sorted(reached))


def graph_control(label, faces, extra):
    vertices, edges, adj, nonfacial = validate_disk(faces)
    assert {edge for edge in edges if max(edge) < 6} == {tuple(sorted(e)) for e in EDGES + extra}
    assert adj[0] & adj[2] == {1, 3}
    fibres = {name(outer): sorted(outer + inner
                                for inner in itertools.product(range(4), repeat=len(vertices) - 4)
                                if all((outer + inner)[a] != (outer + inner)[b] for a, b in edges))
              for outer in WORDS}
    assert [len(fibres[name(outer)]) for outer in WORDS] == [2, 0, 7, 5]
    x0, y0 = [], []
    for row in fibres["ABCB"]:
        if set(row[4:6]) not in ({1, 3}, {2, 3}):
            continue
        mobile_colour = 2 if 2 in row[4:6] else 1
        mobile = 4 if row[4] == mobile_colour else 5
        if 2 not in component(adj, row, mobile, (1, 2)):
            (x0 if mobile_colour == 2 else y0).append(row)
    maps = []
    images = []
    for row in x0:
        mobile = 4 if row[4] == 2 else 5
        block = component(adj, row, mobile, (1, 2))
        target = switch(row, block, (1, 2))
        assert target in y0 and component(adj, target, mobile, (1, 2)) == block
        assert switch(target, block, (1, 2)) == row
        images.append(target)
        maps.append({"source": name(row), "component": block, "target": name(target)})
    assert set(images) == set(y0) and len(images) == len(set(images))
    source_rows = [all(set(row[4:6]) == palette for row in fibres[kind])
                   for kind, palette in (("ABAB", {2, 3}), ("ABCD", {1, 3}))]
    assert source_rows == [False, False]
    return {"label": label, "extra_edges": extra, "oriented_faces_including_outer": faces,
            "edges": edges, "degrees": [len(adj[v]) for v in vertices],
            "six_pin_induced_skeleton_exact": True,
            "z_r_common_neighbors_exactly_s_t": True, "nonfacial_triangles": nonfacial,
            "complete_fixed_frame_fibres": {key: [name(row) for row in rows]
                                              for key, rows in fibres.items()},
            "source_universal_ABAB_and_ABCD_palette_conditions": source_rows,
            "X0": [name(row) for row in x0], "Y0": [name(row) for row in y0],
            "full_colouring_bijection": maps, "actual_target_source": False}


def calculate():
    cases = [partition_case(label, extra) for label, extra in (
        ("none", ()), ("tp", ((3, 4),)), ("qs", ((1, 5),)))]
    assert [case["surviving_states"] for case in cases] == [648, 240, 240]
    qs_faces = [(0, 3, 2, 1), (0, 1, 5), (0, 5, 4), (0, 4, 7), (7, 3, 0),
                (1, 2, 6), (2, 3, 6), (3, 7, 6), (7, 4, 6), (4, 5, 6), (5, 1, 6)]
    none_faces = [(0, 3, 2, 1), (0, 1, 8), (8, 5, 0), (0, 5, 4), (0, 4, 7),
                  (7, 3, 0), (1, 2, 6), (2, 3, 6), (3, 7, 6), (5, 8, 6),
                  (8, 1, 6), (7, 4, 5), (7, 5, 6)]
    controls = [graph_control("eight-point qs disk", qs_faces, ((1, 5),)),
                graph_control("nine-point no-optional-edge disk", none_faces, ())]
    assert controls[0]["X0"] and controls[0]["Y0"]
    assert not controls[1]["X0"] and not controls[1]["Y0"]
    assert not controls[0]["nonfacial_triangles"]
    assert controls[1]["nonfacial_triangles"] == [(0, 5, 7)]
    # Negative controls reject the old inadmissible ABCB/BC sector and
    # crossing outer partitions. The graph controls retain nonempty rainbow.
    assert not admissible((0, 1, 2, 1, 1, 2), EDGES)
    assert not outer_planar((((0, 2),), ((1, 3), (4, 5))))
    return {"status": "PASS: general sector bijection; general exclusion OPEN",
            "pins": PINS, "honest_jordan_boundary": PINS[:4], "mandatory_edges": EDGES,
            "partition_model_scope": "necessary abstraction; no graph or full-fibre realization",
            "partition_cases": cases, "explicit_disk_controls": controls,
            "actual_target_sources": 0,
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).with_name("general-final.json"))
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + "\n"
    output = args.certificate
    if args.check:
        assert output.read_text() == payload, "general certificate differs"
    else:
        with output.open("x") as handle:
            handle.write(payload)
    print(json.dumps({"status": result["status"], "partition_survivors": [648, 240, 240],
                      "explicit_disk_controls": 2, "actual_target_sources": 0}))


if __name__ == "__main__":
    main()
