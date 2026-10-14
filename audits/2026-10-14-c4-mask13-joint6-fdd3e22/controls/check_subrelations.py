#!/usr/bin/env python3
"""All 128 subrelations of the seven-orbit necessary six-pin control."""
import argparse
import importlib.util
import itertools
import json
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCER = HERE / 'check_interface.py'
spec = importlib.util.spec_from_file_location('interface_model', PRODUCER)
interface = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interface)
BASE_EDGES = interface.EDGES
BASE_NAMES = ('ABABCD', 'ABCBBD', 'ABCBCD', 'ABCBDB', 'ABCBDC', 'ABCDBD', 'ABCDDB')
BASE_ROWS = tuple(tuple('ABCD'.index(c) for c in row) for row in BASE_NAMES)
CORE = frozenset(('ABABCD', 'ABCBCD', 'ABCBDC'))
U = frozenset(('ABCBBD', 'ABCBDB'))
V = frozenset(('ABCDBD', 'ABCDDB'))
CASES = (('none', ()), ('tp', ((3, 4),)), ('qs', ((5, 1),)),
         ('tp+qs', ((3, 4), (5, 1))))


def closed_under_options(subset, options):
    return all(all(any(orbit <= subset for a, b, orbit in choices)
                   for choices in options[row]) for row in subset)


def run_case(case, extra_edges):
    # These imported helpers depend on EDGES. Clear the cache for each literal
    # edge set so no component partition from another case can be reused.
    interface.EDGES = BASE_EDGES + extra_edges
    interface.pair_partitions.cache_clear()
    rows = sorted({interface.canonical(row)
                   for row in itertools.product(range(4), repeat=6)
                   if interface.allowed(row)})
    options = {row: [interface.all_options(row, pairing)
                     for pairing in interface.PAIRINGS] for row in rows}
    live = set(rows)
    rounds = []
    while True:
        dead = {row for row in live if any(
            not any(orbit <= live for a, b, orbit in choices)
            for choices in options[row])}
        rounds.append({'live': [interface.name(row) for row in sorted(live)],
                       'removed': [interface.name(row) for row in sorted(dead)]})
        if not dead:
            break
        live -= dead
    closed = []
    accepted_masks = []
    examined = 0
    support13 = {interface.Q_TYPES[i] for i in (0, 2, 3)}
    for mask in range(1 << len(BASE_ROWS)):
        examined += 1
        subset = {row for i, row in enumerate(BASE_ROWS) if mask & (1 << i)}
        if not subset <= live:
            continue
        if {interface.canonical(row[:4]) for row in subset} != support13:
            continue
        if closed_under_options(subset, options):
            accepted_masks.append(mask)
            closed.append(frozenset(interface.name(row) for row in subset))
    assert examined == 128
    minimal = [subset for subset in closed if not any(other < subset for other in closed)]
    return {'case': case, 'extra_edges': extra_edges,
            'initial_orbits': [interface.name(row) for row in rows],
            'rounds': rounds,
            'surviving_orbits': [interface.name(row) for row in sorted(live)],
            'examined_subsets': examined, 'accepted_masks': accepted_masks,
            'closed_subrelations': [sorted(subset) for subset in closed],
            'minimal_subrelations': [sorted(subset) for subset in minimal]}


def calculate():
    records = [run_case(case, edges) for case, edges in CASES]
    interface.EDGES = BASE_EDGES
    interface.pair_partitions.cache_clear()
    nonempty_u = [frozenset((row,)) for row in sorted(U)] + [U]
    nonempty_v = [frozenset((row,)) for row in sorted(V)] + [V]
    expected = {CORE | u | v for u, v in itertools.product(nonempty_u, nonempty_v)}
    actual = {frozenset(row) for row in records[0]['closed_subrelations']}
    assert actual == expected and len(actual) == 9
    assert sorted(map(len, actual)) == [5, 5, 5, 5, 6, 6, 6, 6, 7]
    assert len(records[0]['minimal_subrelations']) == 4
    assert all(len(row) == 5 for row in records[0]['minimal_subrelations'])
    assert [set(row) for row in records[1]['closed_subrelations']] == [
        set(CORE) | {'ABCBDB', 'ABCDBD'}]
    assert [set(row) for row in records[2]['closed_subrelations']] == [
        set(CORE) | {'ABCBBD', 'ABCDBD'}]
    assert records[3]['closed_subrelations'] == []
    assert set(records[3]['surviving_orbits']) == CORE
    return {'status': 'PASS; necessary abstract subrelations, not graph realizations',
            'base_orbit_order': BASE_NAMES,
            'core': sorted(CORE), 'U': sorted(U), 'V': sorted(V),
            'formula': 'core union a nonempty subset of U union a nonempty subset of V',
            'cases': records, 'actual_target_sources': 0,
            'interface_script_sha256': sha256(PRODUCER.read_bytes()).hexdigest(),
            'interface_certificate_sha256': sha256((HERE / 'interface.json').read_bytes()).hexdigest(),
            'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + '\n'
    certificate = HERE / 'subrelations.json'
    if args.check:
        assert certificate.read_text() == payload, 'Subrelation certificate differs'
    else:
        with certificate.open('x') as handle:
            handle.write(payload)
    print(json.dumps({'ok': True, 'subsets_per_case': 128,
                      'closed_counts_none_tp_qs_both': [9, 1, 1, 0],
                      'minimal_base_subrelations': 4, 'minimal_base_size': 5,
                      'actual_target_sources': 0}))


if __name__ == '__main__':
    main()
