#!/usr/bin/env python3
"""Excess-one subcover controls, with one fixed same-source ten-row replay.

The arbitrary-size argument is in docs/c5_excess_one_subcovers.md.
Abstract set controls are necessary-condition relaxations, not graph sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, colorings, components

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_one_subcovers/observations.json"
SOURCE = ROOT / "artifacts/c5_independent_support_capacity/observations.json"
SINGLETON_ROWS = tuple(q for q in ROWS if len(set(q)) == 3)


def singleton(q):
    return next(i for i in range(5) if q.count(q[i]) == 1)


def union(factors):
    return set().union(*factors)


def redundant(factors):
    return [i for i in range(len(factors))
            if union(factors[:i] + factors[i + 1:]) == U]


def partitions(n, maximum=None):
    if n == 0:
        yield ()
    else:
        for k in range(min(n, maximum or n), 0, -1):
            for tail in partitions(n - k, k):
                yield (k,) + tail


def capacity_controls():
    records = []
    for caps in partitions(5):
        counts, examples, digest = Counter(), {}, sha256()
        options = [[set(c) for size in range(min(k, 4) + 1)
                    for c in combinations(range(4), size)] for k in caps]
        for fs in product(*options):
            fs = list(fs)
            if union(fs) != U:
                continue
            deficit = sum(k - len(f) for k, f in zip(caps, fs))
            overlap = sum(map(len, fs)) - 4
            assert deficit + overlap == 1
            omitted = redundant(fs)
            assert all(caps[i] == 1 for i in omitted) and len(omitted) <= 2
            if deficit:
                j, = [i for i, (k, f) in enumerate(zip(caps, fs)) if len(f) < k]
                expected = [j] if caps[j] == 1 else []
                case = "one_deficit_unit" if caps[j] == 1 else "one_deficit_nonunit"
            else:
                d, = [c for c in U if sum(c in f for f in fs) == 2]
                assert all(sum(c in f for f in fs) == 1 for c in U - {d})
                expected = [i for i, f in enumerate(fs) if f == {d}]
                case = f"one_overlap_{len(expected)}_unit_omissions"
            assert omitted == expected
            row = dict(factors=[sorted(f) for f in fs], omitted=omitted,
                       deficit=deficit, overlap=overlap)
            counts[case] += 1
            examples.setdefault(case, row)
            digest.update(json.dumps(row, sort_keys=True).encode())
        records.append(dict(capacities=caps, counts=dict(sorted(counts.items())),
                            examples=examples, enumeration_sha256=digest.hexdigest()))
    return records


def unit_scenarios(conserve=True):
    """All possible rejection subsets in a deliberately enlarged Boolean model.

    Actual components are not generated. Each factor's D-status persists over
    all five rows when conserve=True; a unit omission belongs to at most one
    rejected row. Degree-four topology disallows spoke omissions when t=2.
    """
    records = []
    for t in (2, 3):
        for spokes in combinations(range(5), t):
            m = 5 - t
            types = product((False, True), repeat=m) if conserve else [None]
            for d_types in types:
                states = {(0, 0): []}
                row_options = []
                for q in SINGLETON_ROWS:
                    choices = ([(-1, 3) if d else (-1, 0, 1, 2) for d in d_types]
                               if conserve else [(-1, 0, 1, 2, 3)] * m)
                    options = {}
                    for colors in product(*choices):
                        fs = [{q[b]} for b in spokes]
                        fs += [set() if c < 0 else {c} for c in colors]
                        if union(fs) != U:
                            continue
                        omitted = redundant(fs)
                        assert omitted
                        if t == 2 and any(i < t for i in omitted):
                            continue
                        bits = sum(1 << i for i in omitted)
                        options.setdefault(bits, dict(row=q, singleton=singleton(q),
                                                      factors=[sorted(f) for f in fs],
                                                      omitted=omitted))
                    row_options.append(dict(row=q, options=[options[b] for b in sorted(options)]))
                    following = dict(states)
                    for (qs, used), witness in sorted(states.items()):
                        for bits, option in sorted(options.items()):
                            if not (used & bits):
                                key = (qs | (1 << singleton(q)), used | bits)
                                following.setdefault(key, witness + [option])
                    states = following
                best = max(qs.bit_count() for qs, _ in states)
                key = min(k for k in states if k[0].bit_count() == best)
                if conserve:
                    assert best <= 2
                records.append(dict(spokes=spokes, component_D_types=d_types,
                                    row_options=row_options,
                                    possible_rejected_position_masks=sorted({qs for qs, _ in states}),
                                    maximum_rejections=best, maximum_witness=states[key]))
    return records


def sector_implications():
    # Exact twelve-row gluing, without assuming a double-missing source.
    def joined(x):
        return (x[7], x[3] or x[8], x[5], x[1] or x[8], x[9],
                x[2], x[6], x[0], x[1] or x[3], x[4])

    controls = []
    for bits in range(1 << 12):
        x = tuple(bool(bits >> i & 1) for i in range(12))
        if x[7] or not all(x[i] for i in (0, 10, 11)):
            continue
        y = joined(x)
        if not y[1]:
            assert not any(x[i] for i in (3, 7, 8))
        if not y[6]:
            assert not x[6] and not x[7] and x[11]
        controls.append(dict(mask=bits, joined_mask=sum(int(v) << i for i, v in enumerate(y)),
                             triggers_3703_theorem=not y[1],
                             triggers_two_rejection_theorem=not y[6]))
    return controls


def fixed_source():
    source = json.loads(SOURCE.read_text())
    saved = source['fixed_graphs'][0]
    assert saved['name'] == 'existing_943_k3_t382_submask_2045'
    n, r = saved['vertices'], saved['roots'][0]
    edges = {tuple(e) for e in saved['edges']}
    interior = set(range(5, n))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    factors = [dict(name=f"spoke_{r}_{b}", capacity=1, edges=[(b, r)], boundary=b)
               for b in sorted(neighbors[r] & B)]
    for vs in components(interior - {r}, edges):
        factors.append(dict(name="component_" + "_".join(map(str, vs)),
                            capacity=len(neighbors[r] & set(vs)), vertices=vs,
                            edges=sorted(e for e in edges if set(e) & set(vs))))
    assert sum(f['capacity'] for f in factors) == 5
    assert union([set(map(tuple, f['edges'])) for f in factors]) == edges - FRAME
    factor_rows = []
    for row in ROWS:
        fixed = dict(enumerate(row))
        values, relations = [], []
        for f in factors:
            if 'boundary' in f:
                values.append({row[f['boundary']]})
                continue
            vs = f['vertices']
            contacts = sorted(neighbors[r] & set(vs))
            choices = colorings(vs, edges, fixed)
            tuples = sorted({tuple(c[v] for v in contacts) for c in choices})
            forbidden = set.intersection(*(set(t) for t in tuples))
            values.append(forbidden)
            relations.append(dict(factor=f['name'], contacts=contacts, tuples=tuples,
                                  support=sorted(union([neighbors[v] & B for v in vs])),
                                  tuple_witnesses=[dict(tuple=t, interior_order=vs,
                                      coloring=[next(c for c in choices
                                          if tuple(c[v] for v in contacts) == t)[v] for v in vs])
                                      for t in tuples]))
        factor_rows.append(dict(row=row, factors=[sorted(f) for f in values],
                                component_relations=relations,
                                omitted=redundant(values) if union(values) == U else []))
    descendants = []
    for mask in range(1 << len(factors)):
        retained = [i for i in range(len(factors)) if mask >> i & 1]
        child = FRAME | union([set(map(tuple, factors[i]['edges'])) for i in retained])
        rows = []
        for record in factor_rows:
            q = tuple(record['row'])
            choices = colorings(interior, child, dict(enumerate(q)))
            actual = {c[r] for c in choices}
            expected = U - union([set(record['factors'][i]) for i in retained])
            assert actual == expected
            rows.append(dict(row=q, root_colors=sorted(actual),
                             coloring_witnesses=[dict(root_color=a,
                                 coloring=[next(c for c in choices if c[r] == a)[v] for v in range(n)])
                                 for a in sorted(actual)]))
        sigma = sum(1 << i for i, row in enumerate(rows) if row['root_colors'])
        descendants.append(dict(retained=retained, edges=sorted(child), sigma=sigma, rows=rows))
    assert descendants[-1]['sigma'] == 943
    omitted_rows = {}
    for record in factor_rows:
        for i in record['omitted']:
            assert i not in omitted_rows
            omitted_rows[i] = record['row']
    assert {factors[i]['name'] for i in omitted_rows} == {'spoke_5_0', 'spoke_5_1'}
    return dict(source_name=saved['name'], vertices=n, root=r, edges=sorted(edges),
                factors=factors, full_ten_rows=factor_rows, factor_descendants=descendants,
                omitted_factor_rows={factors[i]['name']: q for i, q in omitted_rows.items()},
                topology="inherited disk provenance; rotation not rerun")


def build():
    capacity = capacity_controls()
    unit = unit_scenarios()
    no_conservation = next(r for r in unit_scenarios(False) if r['maximum_rejections'] >= 3)
    sector = sector_implications()
    fixed = fixed_source()
    candidates = []
    for mask in (933, 941):
        missing = sorted(singleton(q) for i, q in enumerate(ROWS) if not (mask >> i & 1))
        proper = [i for i in missing if (i - 1) % 5 in missing or (i + 1) % 5 in missing]
        isolated = sorted(set(missing) - set(proper))
        candidates.append(dict(mask=mask, rejected_positions=missing,
                               forced_proper_core_positions=proper,
                               possible_whole_core_positions=isolated))
    assert candidates[0]['forced_proper_core_positions'] == [0, 1, 2, 3]
    assert candidates[1]['forced_proper_core_positions'] == [0, 1]
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py', SOURCE]
    return dict(schema=1, scope="finite set controls and one fixed graph; paper reduction has separate dependencies",
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
                pattern_order=ROWS, capacity_controls=capacity, unit_scenarios=unit,
                without_conservation_abstract_countercontrol=no_conservation,
                three_spoke_sector_controls=sector, fixed_graph=fixed, candidates=candidates,
                summary=dict(capacity_partitions=len(capacity),
                    covered_set_families=sum(sum(r['counts'].values()) for r in capacity),
                    unit_scenarios=len(unit), unit_maximum_rejections=max(r['maximum_rejections'] for r in unit),
                    sector_boolean_controls=len(sector), fixed_graphs=1,
                    fixed_graph_factor_subsets=len(fixed['factor_descendants']),
                    fixed_graph_row_checks=len(ROWS) * len(fixed['factor_descendants']),
                    candidate_933_excess_lower_bound=2, candidate_941_excess_lower_bound=1,
                    candidate_941_epsilon_one_component_partitions_by_spokes={
                        '1': [2, 1, 1], '2': [2, 1], '3': [2]},
                    general_candidate_exclusions=0, new_graph_enumeration=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
