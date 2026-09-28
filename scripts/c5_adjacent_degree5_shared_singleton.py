#!/usr/bin/env python3
"""Replay the sole shared-singleton reduction, not a graph catalogue.

Abstract forbidden sets are necessary relation data, never disk realizations.
Fixed graphs and minor skeletons are recorded separately.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_shared_singleton/observations.json"
U = frozenset(range(4))
PARTITIONS = {0: ((),), 1: ((1,),), 2: ((2,), (1, 1)),
              3: ((3,), (2, 1), (1, 1, 1))}


def subsets(xs):
    return [frozenset(c) for k in range(len(xs) + 1)
            for c in combinations(sorted(xs), k)]


def union(sets):
    return frozenset().union(*sets)


def sides():
    result = []
    for spokes in subsets({0, 1, 2}):
        available = U - spokes
        for ports in PARTITIONS[3 - len(spokes)]:
            choices = [[f for f in subsets(U) if 0 < len(f) <= k] for k in ports]
            for forbidden in product(*choices):
                result.append((available, ports, forbidden))
    return result


def residual(side, omitted=None):
    available, _, forbidden = side
    return available - union([f for i, f in enumerate(forbidden) if i != omitted])


def allowed(left, right, pair, edge_present=True, shared_present=True):
    result = set(product(left, right))
    if edge_present:
        result -= base.DELTA
    if shared_present:
        result -= set(product(pair, pair)) - base.DELTA
    return result


def direct_minimality(left, right, pair):
    """Directly evaluate original and each class of single-edge deletion."""
    a, b = residual(left), residual(right)
    if allowed(a, b, pair) or not allowed(a, b, pair, edge_present=False):
        return False
    if not allowed(a, b, pair, shared_present=False):
        return False
    for i in range(len(left[2])):
        if not allowed(residual(left, i), b, pair):
            return False
    for i in range(len(right[2])):
        if not allowed(a, residual(right, i), pair):
            return False
    for c in U - left[0]:
        if not allowed({c} - union(left[2]), b, pair):
            return False
    for c in U - right[0]:
        if not allowed(a, {c} - union(right[2]), pair):
            return False
    return True


def side_form(side, pair):
    available, ports, forbidden = side
    e = residual(side)
    return (pair <= available and bool(e) and e <= pair
            and all(f <= available for f in forbidden)
            and all(f - union([g for j, g in enumerate(forbidden) if i != j]) - pair
                    for i, f in enumerate(forbidden)))


def encode_side(side):
    available, ports, forbidden = side
    return dict(available=sorted(available), spokes_colors=sorted(U - available),
                ports=ports, forbidden=[sorted(f) for f in forbidden],
                residual=sorted(residual(side)))


def abstract_audit():
    options = sides()
    records, count, histogram = [], 0, Counter()
    for missing in range(3):
        pair = frozenset({missing, 3})
        for left, right in product(options, repeat=2):
            direct = direct_minimality(left, right, pair)
            form = (side_form(left, pair) and side_form(right, pair)
                    and (residual(left) == pair or residual(right) == pair))
            assert direct == form, (pair, left, right)
            count += 1
            if not direct:
                continue
            for available, ports, forbidden in (left, right):
                assert len(U - available) <= 1
                assert ports in ((2,), (3,), (2, 1))
                if ports == (2,):
                    assert len(available - pair) == 1
                elif ports == (3,):
                    assert len(forbidden[0]) >= 2
                else:
                    assert available == U and len(forbidden[1]) == 1
                    assert forbidden[1] <= U - pair
                    assert forbidden[0] & (U - pair) == (U - pair) - forbidden[1]
            planar_retained = left[1] != (3,) and right[1] != (3,)
            histogram[str((left[1], right[1]))] += 1
            records.append(dict(pair=sorted(pair), left=encode_side(left), right=encode_side(right),
                                planar_necessary_retained=planar_retained))
    assert records and any(r["planar_necessary_retained"] for r in records)
    # The two excluded singleton/singleton combinations fail different axioms.
    assert not allowed({0}, {0}, {0, 3}, shared_present=False)
    assert not allowed({0}, {3}, {0, 3}, edge_present=False)
    return records, dict(side_candidates=len(options), abstract_cases=count,
                         minimal_relation_records=len(records),
                         planar_necessary_records=sum(r["planar_necessary_retained"] for r in records),
                         partition_pairs=dict(sorted(histogram.items())))


def capacity_audit():
    records, columns, rows, unary = [], 0, 0, 0
    for region in base.controls():
        kz, kw = len(region["ports_z"]), len(region["ports_w"])
        transcript = []
        for row in base.ROWS:
            relation, _, _ = base.joint_interface(region, row)
            forbidden = base.PAIRS - relation
            if kz and kw:
                for b in U:
                    assert sum((a, b) in forbidden for a in U) <= kz
                    columns += 1
                for a in U:
                    assert sum((a, b) in forbidden for b in U) <= kw
                    rows += 1
            elif kz:
                bans = {a for a in U if (a, 0) in forbidden}
                assert forbidden == frozenset(product(bans, U)) and len(bans) <= kz
                unary += 1
            else:
                bans = {b for b in U if (0, b) in forbidden}
                assert forbidden == frozenset(product(U, bans)) and len(bans) <= kw
                unary += 1
            transcript.append([row, base.mask(relation)])
        records.append(dict(name=region["name"], ports_z=region["ports_z"], ports_w=region["ports_w"],
                            relations_sha256=sha256(json.dumps(transcript).encode()).hexdigest()))
    return records, dict(column_capacity_checks=columns, row_capacity_checks=rows,
                         unary_relation_checks=unary)


def cross_row_audit():
    """Exact rejection criterion for arbitrary rows, without q-minimality."""
    nonempty = [s for s in subsets(U) if s]
    cases, rejected = 0, 0
    for xlist in [s for s in subsets(U) if len(s) in (2, 3)]:
        for left, right in product(nonempty, repeat=2):
            forbidden = set(product(xlist, xlist)) - base.DELTA if len(xlist) == 2 else set()
            direct = not (set(product(left, right)) - base.DELTA - forbidden)
            predicted = ((len(left) == 1 and left == right)
                         or (len(xlist) == 2 and left <= xlist and right <= xlist))
            assert direct == predicted
            cases += 1
            rejected += direct
    return dict(cases=cases, rejections=rejected,
                warning="target rows use their own same-source unary relations; q private conditions are not inherited")


def fixed_graph_audit():
    """A true minimal q-core with target degrees; no disk/T4 assertion."""
    x = base.make_region("common_x", [], {7: (base.Z, base.W, 0, 1)})
    left = base.make_region("z_triangle", [(8, 9), (8, 10), (9, 10)],
                            {8: (0, 1), 9: (base.Z, 0), 10: (base.Z, 0)})
    right = base.make_region("w_triangle", [(11, 12), (11, 13), (12, 13)],
                             {11: (0, 1), 12: (base.W, 1), 13: (base.W, 1)})
    regions = [x, left, right]
    edges = base.CYCLE | {base.edge(base.Z, base.W), base.edge(base.Z, 0), base.edge(base.W, 1)}
    edges |= union([r["edges"] for r in regions])
    vertices = tuple(range(14))
    assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * 7
    assert not base.whole_pairs(vertices, edges, base.Q)
    deletion_witnesses = []
    for e in sorted(edges - base.CYCLE):
        coloring = base.first_coloring(vertices, edges - {e}, dict(enumerate(base.Q)))
        assert coloring is not None and coloring[e[0]] == coloring[e[1]]
        deletion_witnesses.append(dict(edge=e, coloring=[coloring[v] for v in vertices]))
    transcript, canonical = [], []
    for row in base.ROWS:
        relations = [base.joint_interface(r, row)[0] for r in regions]
        direct = base.whole_pairs(vertices, edges, row)
        assert direct == base.glued_pairs(regions, relations, edges, row, frozenset())
        lx = U - {row[0], row[1]}
        expected_x = base.PAIRS if len(lx) >= 3 else base.PAIRS - (set(product(lx, lx)) - base.DELTA)
        assert relations[0] == expected_x
        transcript.append([row, base.mask(direct)])
        if row in base.CANONICAL:
            local = []
            for region in regions:
                relation, ports, witnesses = base.joint_interface(region, row)
                local.append(dict(name=region["name"], ports=ports, mask=base.mask(relation),
                                  tuples=[dict(contact=t, coloring=f) for t, f in sorted(witnesses.items())]))
            canonical.append(dict(row=row, root_pairs=sorted(direct),
                                  regions=local))
    # An explicit K5 minor prevents mistaking this finite graph for a disk source.
    groups = [{base.Z, 7, 1}, {8}, {9}, {10}, {0}]
    minor = dict(edges=sorted(edges), branch_sets=[sorted(g) for g in groups])
    assert validate_minor(minor)
    return dict(scope="actual edge-minimal q-core, nonplanar by displayed K5; not a disk/T4 witness",
                vertices=vertices, edges=sorted(edges), canonical_rows=canonical,
                regions=[dict(name=r["name"], vertices=r["vertices"], edges=sorted(r["edges"]),
                              ports_z=r["ports_z"], ports_w=r["ports_w"]) for r in regions],
                q_deletion_witnesses=deletion_witnesses, nonplanar_minor=minor,
                all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest())


def minor_audit():
    records = []
    arm_cases = ((0, 0, 0), (0, 2, 0), (2, 2, 2), (1, 1, 1), (1, 3, 1))
    for i, j in combinations(range(5), 2):
        for lengths, long in product(arm_cases, (False, True)):
            es = {edge(f"b{k}", f"b{(k+1)%5}") for k in range(5)}
            es |= {edge("z", "w"), edge("z", "x"), edge("w", "x"),
                   edge("x", f"b{i}"), edge("x", f"b{j}")}
            core = [f"v{k}" for k in range(3)]
            es |= {edge(a, b) for a, b in combinations(core, 2)}
            groups = [{"z"}] + [{v} for v in core] + [{f"b{k}" for k in range(5)} | {"x"}]
            arms, tethers = [], []
            for k, (v, length) in enumerate(zip(core, lengths)):
                arm = [v] + [f"a{k}_{n}" for n in range(length)]
                es.update(edge(a, b) for a, b in zip(arm, arm[1:]))
                es.add(edge("z", arm[-1]))
                groups[k+1].update(arm)
                tether = [v] + ([f"t{k}_0", f"t{k}_1"] if long else []) + [f"b{(i+k)%5}"]
                es.update(edge(a, b) for a, b in zip(tether, tether[1:]))
                groups[4].update(tether[1:])
                arms.append(arm)
                tethers.append(tether)
            record = dict(edges=sorted(es), branch_sets=[sorted(g) for g in groups],
                          common_boundary=[i, j], arms=arms, tethers=tethers,
                          external_path=["z", "x", f"b{i}"])
            assert validate_minor(record)
            assert not validate_minor(dict(record, edges=sorted(es - {edge("z", "x")})))
            record["adjacency"] = [dict(pair=[a, b], edge=next(
                edge(u, v) for u in sorted(groups[a]) for v in sorted(groups[b]) if edge(u, v) in es))
                for a, b in combinations(range(5), 2)]
            records.append(record)
    return records


def build():
    abstract, summary = abstract_audit()
    capacities, counts = capacity_audit()
    fixed = fixed_graph_audit()
    minors = minor_audit()
    cross_rows = cross_row_audit()
    summary.update(counts)
    summary.update(fixed_graph_rows=len(base.ROWS), fixed_graph_deletions=len(fixed["q_deletion_witnesses"]),
                   K5_skeletons=len(minors), missing_external_edge_controls=len(minors))
    summary["cross_row_relation_cases"] = cross_rows["cases"]
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_single_spoke_three_one.py",
              "docs/c5_no_spoke_exterior.md", "docs/c5_single_spoke_three_one.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="necessary same-source reduction; abstract masks and minor skeletons are not disk realizations",
                summary=summary, abstract_relations=abstract, capacity_controls=capacities,
                cross_row_conditions=cross_rows, fixed_graph=fixed, minor_skeletons=minors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert OUT.read_bytes() == payload.encode(), "certificate differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
