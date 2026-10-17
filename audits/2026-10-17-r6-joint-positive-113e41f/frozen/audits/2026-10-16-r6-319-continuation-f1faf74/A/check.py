#!/usr/bin/env python3
"""Replay finite algebra for the full-source all-distinct theorem; no 4CT.

No earlier checker is imported. Actual source instances: zero, not triggered.
The unbounded graph/Jordan/Kempe proof is PROOF.md, not this finite table.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PINS = ("z", "s", "v", "w", "t", "p", "q")
EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (5, 6), (6, 0))
PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
COLOURS = tuple(range(4))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def name(row):
    return "".join("ABCD"[c] for c in row)


def from_name(row):
    return tuple("ABCD".index(c) for c in row)


def proper(row):
    return all(row[a] != row[b] for a, b in EDGES)


def raw_r(row):
    return tuple(c for c in COLOURS if c not in row[1:5])


def old_rule(row, r):
    z, s, _, _, t, p, q = row
    if z == r:
        return s == t and {p, q} == set(COLOURS) - {z, s}
    if s == t:
        return bool({p, q} & (set(COLOURS) - {z, s, r}))
    return {p, q} == {s, t}


def allowed(row):
    return proper(row) and all(old_rule(row, r) for r in raw_r(row))


def independent_allowed(row):
    if not proper(row):
        return False
    table = {
        (0, 1, 0, 1): {(2, 3), (3, 2)},
        (0, 1, 0, 2): set(),
        (0, 1, 2, 1): {(1, 3), (2, 3), (3, 1), (3, 2)},
        (0, 1, 2, 3): {(1, 3), (3, 1)},
    }
    for r in COLOURS:
        if r not in (row[1], row[2], row[3], row[4]):
            rr = canonical((row[0], row[1], r, row[4], row[5], row[6]))
            if rr[4:] not in table[rr[:4]]:
                return False
    return True


def all_distinct(row):
    return proper(row) and row[1] == row[4] and len(
        {row[2] ^ row[3], row[5] ^ row[6], row[1] ^ row[0]}
    ) == 3


def partitions(items):
    if not items:
        yield ()
        return
    first = items[0]
    for part in partitions(items[1:]):
        yield ((first,),) + part
        for i, block in enumerate(part):
            yield part[:i] + ((first,) + block,) + part[i + 1:]


@lru_cache(None)
def pair_partitions(row, pair):
    vertices = tuple(i for i, c in enumerate(row) if c in pair)
    answer = []
    for part in partitions(vertices):
        labels = {v: i for i, block in enumerate(part) for v in block}
        if all(labels[a] == labels[b] for a, b in EDGES
               if a in labels and b in labels):
            answer.append(part)
    return tuple(answer)


def noncrossing(parts):
    labels = {v: i for i, block in enumerate(parts) for v in block}
    return all(not (labels[a] == labels[c] and labels[b] == labels[d]
                    and labels[a] != labels[b])
               for a, b, c, d in combinations(range(5), 4))


def swap(row, part, pair):
    result = list(row)
    for v in part:
        result[v] = pair[1] if row[v] == pair[0] else pair[0]
    return tuple(result)


def orbit(row, parts, pairing):
    blocks = [(block, pair) for group, pair in zip(parts, pairing)
              for block in group]
    result = set()
    for mask in range(1 << len(blocks)):
        successor = row
        for i, (block, pair) in enumerate(blocks):
            if mask >> i & 1:
                successor = swap(successor, block, pair)
        result.add(canonical(successor))
    return frozenset(result)


@lru_cache(None)
def options(row, pairing):
    result = []
    for parts in product(*(pair_partitions(row, pair) for pair in pairing)):
        if noncrossing(parts[0] + parts[1]):
            result.append((parts, orbit(row, parts, pairing)))
    return tuple(result)


def fixed_point(rows):
    live = set(rows)
    rounds = []
    while True:
        dead = {row for row in live if any(
            not any(successors <= live for _, successors in options(row, pairing))
            for pairing in PAIRINGS)}
        rounds.append({"live": [name(r) for r in sorted(live)],
                       "removed": [name(r) for r in sorted(dead)]})
        if not dead:
            return live, rounds
        live -= dead


def paper_maps(upper):
    pairing = PAIRINGS[2]
    records = []
    for source, target, pin, path_pin in (
        ("ABABC", "ACABC", 1, 2),
        ("ACABC", "ABABC", 1, 2),
        ("ABCAC", "ABCAB", 4, 3),
        ("ABCAB", "ABCAC", 4, 3),
    ):
        for pq in ((1, 2), (2, 1)):
            row = from_name(source) + pq
            need(allowed(row), "paper source is outside entire all-r relation")
            admissible = []
            for parts, successors in options(row, pairing):
                if not successors <= upper:
                    continue
                labels = [{v: i for i, block in enumerate(ps) for v in block}
                          for ps in parts]
                need(labels[0][0] == labels[0][path_pin], "forced AD path absent")
                bc = labels[1]
                other_pair = (3, 4) if pin == 1 else (1, 2)
                need(bc[other_pair[0]] == bc[other_pair[1]], "retained BC edge split")
                need(bc[pin] != bc[other_pair[0]], "Jordan crossing allowed")
                component = next(b for b in parts[1] if pin in b)
                image = swap(row, component, (1, 2))
                need(image[:5] == from_name(target), "wrong literal image boundary")
                need(set(image[5:]) == {1, 2}, "pq palette lost")
                need(swap(image, component, (1, 2)) == row, "component involution failed")
                need(allowed(image), "image lost an actual r lift constraint")
                if target in ("ACABC", "ABCAB"):
                    need(all_distinct(image), "image is not actual J all-distinct sector")
                    need(raw_r(image) == (3,), "image did not retain unique r=D")
                admissible.append({"parts": parts, "s_component" if pin == 1
                                   else "t_component": component,
                                   "image": name(image),
                                   "successors": [name(r) for r in sorted(successors)]})
            need(bool(admissible), "no calibration component option")
            records.append({"row": name(row), "target_boundary": target,
                            "swapped_pin": PINS[pin], "all_admissible_options": admissible})
    return records


def calculate():
    manifest = json.loads((AUDIT / "BASE.json").read_text())
    frozen = []
    for record in manifest["authority_inputs"]:
        path = AUDIT / "frozen" / record["path"]
        if path.exists():
            need(digest(path) == record["sha256"], "frozen authority drift: " + record["path"])
            frozen.append(record)
    assignments = list(product(COLOURS, repeat=7))
    need(len(assignments) == 16384, "lost seven-pin universe")
    need(all(allowed(r) == independent_allowed(r) for r in assignments),
         "independent full all-r table disagrees")
    upper = {canonical(r) for r in assignments if allowed(r)}
    need(len(upper) == 26, "initial upper relation changed")
    local = []
    for row in assignments:
        is_proper = proper(row)
        legal = raw_r(row) if is_proper else ()
        local.append([int(is_proper), list(raw_r(row)), list(legal),
                      [int(old_rule(row, r)) for r in legal],
                      int(allowed(row)), int(all_distinct(row))])
    full_live, full_rounds = fixed_point(upper)
    no_distinct, rounds = fixed_point({r for r in upper if not all_distinct(r)})
    expected = {"ABACBCD", "ABACBDC", "ABCABCD", "ABCABDC", "ABCDBCD", "ABCDBDC"}
    need({name(r) for r in no_distinct} == expected, "all-distinct-free fixed point changed")
    patterns = sorted({canonical(r[:5]) for r in assignments if proper(r)})
    support = sum(1 << i for i, p in enumerate(patterns)
                  if any(canonical(r[:5]) == p for r in no_distinct))
    need(support == 266 and support & 1 == 0 and support & 16 == 0,
         "incorrect 319 contradiction")
    maps = paper_maps(upper)
    # Local characterization used by the exact all-distinct count formula.
    for r in assignments:
        if not proper(r) or r[1] != r[4]:
            continue
        z, m, v, w, _, p, q = r
        characterization = ((z == v and {p, q} == {m, w})
                            or (z == w and {p, q} == {m, v}))
        need(all_distinct(r) == characterization, "all-distinct classification failed")
    need(not noncrossing(((0, 2), (1, 3), (4,), (5,), (6,))), "crossing control accepted")
    # A tempting reverse proof using outer support alone fails; full all-r
    # keeps the actual r=A lift and rejects its incompatible palette.
    reverse_obstruction = from_name("ACDBCBC")
    need(proper(reverse_obstruction) and raw_r(reverse_obstruction) == (0,),
         "reverse obstruction not proper with r=A")
    need(not allowed(reverse_obstruction), "reverse bad all-r palette accepted")
    return {
        "schema": "source319-forces-two-all-distinct-sectors-v1",
        "base": manifest["base"],
        "binding": {"checker_sha256": digest(Path(__file__)),
                    "proof_sha256": digest(HERE / "PROOF.md"),
                    "base_sha256": digest(AUDIT / "BASE.json")},
        "verified_frozen_authorities": frozen,
        "pins": PINS, "retained_edges": EDGES,
        "local_universe": {"size": 16384, "order": "lexicographic 0,1,2,3 on all seven original pins",
                           "columns": ["proper", "raw_avoiding_r_colours", "all_legal_local_r_lifts",
                                       "old_full_rule_per_r_lift", "upper_allowed", "J_all_distinct"],
                           "all_positions_including_empty": local},
        "upper_26": [name(r) for r in sorted(upper)],
        "ordinary_upper_fixed_point": {"survivors": [name(r) for r in sorted(full_live)],
                                       "rounds": full_rounds},
        "full_colouring_bijections_finite_component_check": maps,
        "all_distinct_free_fixed_point": {"rounds": rounds,
                                           "survivors": sorted(expected), "outer_support": support},
        "count_formula": {"n0": "complete U colourings of literal ABABC",
                          "n4": "complete U colourings of literal ABCAC",
                          "all_distinct_J": "24*(n0+n4)",
                          "under_full_source_FJ": "W010=W001=2*(n0+n4)>0",
                          "target_W110_plus_W101": "OPEN"},
        "negative_controls": {"all_16384_slots_independently_checked": True,
                              "crossing_rejected": True,
                              "reverse_actual_r_A_bad_palette_rejected": True},
        "actual_minimum_source_instances": {"count": 0, "status": "not triggered"},
        "authority": "paper arbitrary-size source theorem; finite algebra does not certify source realizability",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + "\n"
    if args.check:
        need(args.certificate.read_text() == payload, "certificate differs from independent recomputation")
    else:
        with args.certificate.open("x") as handle:
            handle.write(payload)
    print(json.dumps({"ok": True, "seven_pin_slots": 16384,
                      "all_distinct_free_survivors": 6, "all_distinct_free_support": 266,
                      "full_colour_bijection_rows": len(result["full_colouring_bijections_finite_component_check"]),
                      "actual_minimum_sources": "0; not triggered",
                      "target_W110_plus_W101": "OPEN"}, sort_keys=True))


if __name__ == "__main__":
    main()
