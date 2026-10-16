#!/usr/bin/env python3
"""Replay the necessary six-pin control and exact local return switch."""

import argparse
import itertools
import json
from hashlib import sha256
from pathlib import Path

PINS = ("z", "s", "v", "t", "p", "q")
EDGES = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 5), (5, 0))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
WORDS = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))


def normalize(word):
    seen = []
    result = []
    for colour in word:
        if colour not in seen:
            seen.append(colour)
        result.append(seen.index(colour))
    return tuple(result)


def name(word):
    return "".join("ABCD"[c] for c in word)


def admissible(word):
    if any(word[a] == word[b] for a, b in EDGES):
        return False
    outer = normalize(word[:4])
    if outer == WORDS[0]:
        return set(word[4:]) == set(range(4)) - set(word[:4])
    if outer == WORDS[1]:
        return set(word[4:]) == {word[1], word[3]}
    if outer == WORDS[2]:
        return set(word[4:]) == set(range(4)) - {word[0], word[1]}
    return False


def set_partitions(vertices):
    """Restricted-growth-string enumeration, with every partition once."""
    if not vertices:
        yield ()
        return
    words = [(0,)]
    for _ in range(1, len(vertices)):
        words = [word + (label,) for word in words
                 for label in range(max(word) + 2)]
    for word in words:
        yield tuple(tuple(vertices[i] for i, label in enumerate(word) if label == j)
                    for j in range(max(word) + 1))


def components(word, pair):
    vertices = tuple(i for i, c in enumerate(word) if c in pair)
    for part in set_partitions(vertices):
        block = {v: j for j, group in enumerate(part) for v in group}
        if all(block[a] == block[b] for a, b in EDGES if a in block and b in block):
            yield part


def planar_outer(parts):
    block = {v: j for j, group in enumerate(parts) for v in group}
    return not (block[0] == block[2] and block[1] == block[3]
                and block[0] != block[1])


def switched(word, block, pair):
    target = list(word)
    a, b = pair
    for v in block:
        assert word[v] in pair
        target[v] = b if word[v] == a else a
    return tuple(target)


def orbit(word, parts, split):
    switches = [(block, pair) for groups, pair in zip(parts, split) for block in groups]
    result = set()
    for flags in itertools.product((False, True), repeat=len(switches)):
        target = word
        for use, (block, pair) in zip(flags, switches):
            if use:
                target = switched(target, block, pair)
        result.add(normalize(target))
    return result


def options(word, split):
    result = []
    for parts in itertools.product(*(components(word, pair) for pair in split)):
        if planar_outer(parts[0] + parts[1]):
            result.append((parts, orbit(word, parts, split)))
    return result


def full_component(edges, word, start, pair):
    reached = {start}
    pending = [start]
    while pending:
        current = pending.pop()
        for a, b in edges:
            nxt = b if a == current else a if b == current else None
            if nxt is not None and word[nxt] in pair and nxt not in reached:
                reached.add(nxt)
                pending.append(nxt)
    return tuple(sorted(reached))


def disk_control(label, vertices, edges, faces):
    # A listed disk embedding is verified combinatorially, separately from
    # every full colouring. All faces here are genuine triangles.
    from collections import Counter
    edge_use = Counter(tuple(sorted((face[i], face[(i + 1) % len(face)])))
                       for face in faces for i in range(len(face)))
    boundary = {tuple(sorted(edge)) for edge in EDGES[:4]}
    assert set(edge_use) == {tuple(sorted(edge)) for edge in edges}
    assert all(count == (1 if edge in boundary else 2) for edge, count in edge_use.items())
    assert vertices - len(edges) + len(faces) == 1
    fibres = {name(outer): [outer + inside
                          for inside in itertools.product(range(4), repeat=vertices - 4)
                          if all((outer + inside)[a] != (outer + inside)[b] for a, b in edges)]
              for outer in WORDS}
    e = [word for word in fibres["ABAC"] if set(word[4:6]) == {1, 2}]
    t = [word for word in fibres["ABAB"] if set(word[4:6]) == {1, 2}]
    t0 = [word for word in t if 1 not in full_component(edges, word, 3, (1, 2))]
    maps = []
    if not fibres["ABCD"]:
        images = []
        for word in e:
            block = full_component(edges, word, 3, (1, 2))
            target = switched(word, block, (1, 2))
            assert target in t0
            inverse_block = full_component(edges, target, 3, (1, 2))
            assert block == inverse_block and switched(target, inverse_block, (1, 2)) == word
            images.append(target)
            maps.append({"source": name(word), "component": block, "target": name(target)})
        assert len(set(images)) == len(e) and set(images) == set(t0)
    return {"label": label, "vertices": vertices, "edges": edges,
            "triangular_inner_faces": faces,
            "complete_fixed_frame_fibres": {key: [name(word) for word in value]
                                             for key, value in fibres.items()},
            "E": [name(word) for word in e], "T": [name(word) for word in t],
            "T0": [name(word) for word in t0], "return_bijection": maps}


def graph_controls():
    # Pin order remains z,s,v,t,p,q; w is the seventh vertex when used.
    outer_edges = EDGES[:4]
    no_rainbow_removed = disk_control(
        "without no-rainbow: E nonempty but T empty", 6,
        EDGES + ((1, 4), (3, 5), (2, 4), (2, 5)),
        ((0, 1, 4), (1, 2, 4), (2, 3, 5), (2, 5, 4), (0, 4, 5), (0, 5, 3)))
    assert no_rainbow_removed["E"] and not no_rainbow_removed["T"]
    assert no_rainbow_removed["complete_fixed_frame_fibres"]["ABCD"]

    wheel = outer_edges + tuple((6, i) for i in range(4))
    target_nonempty = disk_control(
        "rainbow-free with nonempty actual return bijection", 7,
        wheel + ((4, 0), (4, 1), (4, 6), (5, 0), (5, 6), (5, 4)),
        ((0, 1, 4), (1, 6, 4), (0, 4, 5), (4, 6, 5),
         (6, 0, 5), (1, 2, 6), (2, 3, 6), (3, 0, 6)))
    assert not target_nonempty["complete_fixed_frame_fibres"]["ABCD"]
    assert target_nonempty["E"] and target_nonempty["T0"]

    wrong_abac_palette = disk_control(
        "rainbow-free ABAB/CD with ABAC outside BC sector", 7,
        wheel + ((5, 0), (5, 1), (5, 6), (4, 0), (4, 1), (4, 5)),
        ((0, 1, 4), (1, 5, 4), (5, 0, 4), (1, 6, 5),
         (6, 0, 5), (1, 2, 6), (2, 3, 6), (3, 0, 6)))
    fibres = wrong_abac_palette["complete_fixed_frame_fibres"]
    assert not fibres["ABCD"] and fibres["ABAC"]
    assert all(set(word[4:6]) == {"C", "D"} for word in fibres["ABAB"])
    assert not wrong_abac_palette["E"] and not wrong_abac_palette["T"]
    return [no_rainbow_removed, target_nonempty, wrong_abac_palette]


def calculate():
    assert len(list(set_partitions(tuple(range(6))))) == 203
    labelled = [word for word in itertools.product(range(4), repeat=6) if admissible(word)]
    initial = sorted({normalize(word) for word in labelled})
    assert len(labelled) == 120 and len(initial) == 5
    choices = {word: [options(word, split) for split in SPLITS] for word in initial}
    live = set(initial)
    rounds = []
    while True:
        dead = {word for word in live if any(
            not any(successors <= live for _, successors in split_choices)
            for split_choices in choices[word])}
        rounds.append({"live": [name(w) for w in sorted(live)],
                       "removed": [name(w) for w in sorted(dead)]})
        if not dead:
            break
        live -= dead
    assert initial == [(0, 1, 0, 1, 2, 3), (0, 1, 0, 2, 1, 2),
                       (0, 1, 0, 2, 2, 1), (0, 1, 2, 1, 2, 3),
                       (0, 1, 2, 1, 3, 2)]
    assert set(initial) - live == {(0, 1, 0, 2, 1, 2), (0, 1, 0, 2, 2, 1)}

    direct_checks = []
    for word in ((0, 1, 0, 2, 1, 2), (0, 1, 0, 2, 2, 1)):
        checks = []
        for ad in components(word, (0, 3)):
            v_block = next(block for block in ad if 2 in block)
            if 0 not in v_block:
                forbidden = switched(word, v_block, (0, 3))
                assert len(set(forbidden[:4])) == 4
                continue
            for bc in components(word, (1, 2)):
                if not planar_outer(ad + bc):
                    continue
                t_block = next(block for block in bc if 3 in block)
                assert 1 not in t_block
                target = switched(word, t_block, (1, 2))
                assert target[:4] == WORDS[0]
                assert set(target[4:]) == {1, 2}
                assert not admissible(target)
                assert switched(target, t_block, (1, 2)) == word
                checks.append({"AD": ad, "BC": bc, "target": name(target),
                               "inverse_recovers_full_pin_row": True})
        assert len(checks) == 3
        direct_checks.append({"row": name(word), "all_possible_partitions": checks})

    # Deliberate local negative controls.
    assert not planar_outer(((0, 2), (1, 3), (4, 5)))
    assert not admissible((0, 1, 0, 1, 1, 2))
    assert not admissible((0, 1, 2, 3, 1, 2))
    assert ((1,), (3,), (4,), (5,)) not in tuple(components((0, 1, 0, 2, 1, 2), (1, 2)))

    survivors = []
    for word in sorted(live):
        records = []
        for split, split_choices in zip(SPLITS, choices[word]):
            passing = [{"parts": parts, "successors": [name(w) for w in sorted(successors)]}
                       for parts, successors in split_choices if successors <= live]
            assert passing
            records.append({"split": split, "options": passing})
        survivors.append({"row": name(word), "splits": records})

    return {
        "status": "PASS: local return injection; mask7 support excluded",
        "pins": PINS, "mandatory_edges": EDGES, "outer_jordan_boundary": PINS[:4],
        "initial_labelled_count": len(labelled),
        "initial_orbits": [name(w) for w in initial], "rounds": rounds,
        "surviving_labelled_count": sum(normalize(w) in live for w in labelled),
        "surviving_outer_mask": 5, "required_outer_mask": 7,
        "direct_return_checks": direct_checks, "survivors": survivors,
        "nonvacuous_full_graph_controls": graph_controls(),
        "actual_target_sources": 0,
        "negative_controls": {"crossing_rejected": True, "edge_split_rejected": True,
                              "bad_ABAB_palette_rejected": True, "rainbow_rejected": True},
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("return.json"))
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + "\n"
    if args.check:
        assert args.certificate.read_text() == payload, "return certificate differs"
    else:
        with args.certificate.open("x") as handle:
            handle.write(payload)
    print(json.dumps({key: result[key] for key in (
        "status", "initial_labelled_count", "surviving_labelled_count",
        "surviving_outer_mask", "required_outer_mask", "actual_target_sources")}))


if __name__ == "__main__":
    main()
