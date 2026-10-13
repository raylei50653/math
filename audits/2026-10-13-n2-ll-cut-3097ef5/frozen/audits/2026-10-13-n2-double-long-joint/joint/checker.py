#!/usr/bin/env python3
"""Read-only replay of bounded interface calibration, not source enumeration."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from matrix import analyze

HERE = Path(__file__).resolve().parent


def independent_count(rows, columns, kr, ks, safe_p, safe_q):
    """Enumerate permissible row subsets, independently of free-bit enumeration."""
    choices = []
    for r in rows:
        required = {c for a, c in safe_q if a == r}
        banned = {c for a, c in safe_p if a == r}
        allowed = []
        for size in (ks - 1, ks):
            for subset in itertools.combinations(columns, size):
                if required <= set(subset) and not banned & set(subset):
                    allowed.append(set(subset))
        choices.append(allowed)
    return sum(all(kr - 1 <= sum(c in s for s in subsets) <= kr for c in columns)
               for subsets in itertools.product(*choices))


def case(rows, columns, kr, ks, sp, sq):
    answer = analyze(rows, columns, kr, ks, sp, sq)
    assert answer['count'] == independent_count(rows, columns, kr, ks, sp, sq)
    return {'literal_rows': list(rows), 'literal_columns': list(columns),
            'P_root_incidences': [kr, ks], 'safe_P': sorted(sp), 'safe_Q': sorted(sq),
            'matrix_result': answer}


def generate():
    base = json.loads((HERE / 'BASE.json').read_bytes())
    raw = (HERE / base['frozen']).read_bytes()
    assert len(raw) == base['bytes'] and hashlib.sha256(raw).hexdigest() == base['sha256']
    control = json.loads(raw)
    edges = control['original_edges']
    roots, boundary = control['ordered_original_roots'], set(control['original_boundary'])
    nbr = {v: {b if a == v else a for a, b in edges if v in (a, b)}
           for v in control['original_vertices']}
    source_cases = []
    for i, joint in enumerate(control['same_original_joint_rows']):
        q = joint['beta']
        E = [sorted(set(range(4)) - {q[h] for h in nbr[v] & boundary}) for v in roots]
        grid = list(itertools.product(*E))
        safes = []
        for piece in control['same_original_piece_records']:
            vertices = piece['original_vertices']
            shared = any(set(roots) <= nbr[v] for v in vertices)
            W = [set().union(*(nbr[v] & boundary for v in vertices if z in nbr[v])) for z in roots]
            safe = {(a, b) for a, b in grid
                    if a in {q[h] for h in W[0]} or b in {q[h] for h in W[1]}
                    or (shared and a == b)}
            for a, b in safe:
                assert piece['rows'][i]['full_lifts_by_ordered_pins'][4 * a + b]
            safes.append(safe)
        kr, ks = control['same_original_piece_records'][0]['root_incidence_by_ordered_root']
        result = case(*E, kr, ks, *safes)
        assert not result['matrix_result']['feasible']
        actual = joint['complete_accepting_ordered_pins']
        assert actual
        result.update({'beta': q, 'actual_same_source_joint_pins': actual,
                       'full_lift_reference': {'source_sha256': base['sha256'],
                                              'json_pointer': '/same_original_joint_rows/' + str(i)},
                       'status': 'triggered and holds', 'full_target_source': 'not triggered'})
        source_cases.append(result)
    # All degree-compatible incidence profiles; no hypothetical graphs are generated.
    arithmetic = [case(range(a), range(b), kr, ks, set(), set())
                  for a in range(2, 5) for b in range(2, 5)
                  for kr in range(1, a + 1) for ks in range(1, b + 1)]
    # Separate accepted cells need not produce a joint or an infeasible matrix.
    separate = case([0, 3], [1, 2, 3], 2, 2, {(0, 1)}, {(3, 1)})
    assert separate['matrix_result']['feasible']
    # A whole accepted row and surplus opposite incidence force infeasibility,
    # even when there is no directly overlapping certified cell.
    surplus = case([0, 1, 3], [0, 2, 3], 2, 2,
                   {(0, 0), (0, 2), (0, 3)}, set())
    assert not surplus['matrix_result']['feasible']
    assert not surplus['matrix_result']['common_safe_cells']
    assert surplus['matrix_result']['violated_cut'] is not None
    target_rows = [(0, 1, 2, 1, 2), (0, 1, 2, 0, 2), (0, 1, 0, 2, 1)]
    spoke_sets = [()] + [(v,) for v in range(5)] + [tuple(sorted((v, (v + 1) % 5))) for v in range(5)]
    closure = [{'spokes': list(t), 'Z': [h for h in range(5)
                if all(q[h] in {q[v] for v in t} for q in target_rows)]} for t in spoke_sets]
    residual = []
    for tr, ts in [(2, 0), (1, 1), (2, 1)]:
        a, b = 4 - tr, 4 - ts
        for kr in range(1, a + 1):
            for ks in range(1, b + 1):
                if max(kr + ks, a + b + 2 - kr - ks) < 4:
                    continue
                rec = case(range(a), range(b), kr, ks, set(), set())
                rec['root_spoke_counts'] = [tr, ts]
                residual.append(rec)
    assert max(len(c['literal_rows']) * len(c['literal_columns']) for c in residual) == 9
    return {'scope': 'finite literal interface calibration only; no graph-source census',
            'source_control_sha256': base['sha256'], 'full_target_source_status': 'not triggered',
            'same_original_control_rows': source_cases, 'all_81_incidence_profiles': arithmetic,
            'abstract_separate_witness_negative_control': separate,
            'surplus_cut_positive_control': surplus, 'literal_signature_closures': closure,
            'positive_spoke_residual_incidence_profiles': residual,
            'remaining_maximum_binary_cells': 9, 'remaining_maximum_assignments': 512,
            'warning': 'a feasible capacity matrix is not an original relation or source realization'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'observations.json')
    args = parser.parse_args()
    data = (json.dumps(generate(), sort_keys=True, separators=(',', ':')) + '\n').encode()
    if args.check:
        if args.artifact.read_bytes() != data:
            raise SystemExit('artifact mismatch')
    else:
        with args.artifact.open('xb') as out:
            out.write(data)
    print(json.dumps({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                      'original_control_rows': 10, 'abstract_incidence_profiles': 81,
                      'target_sources': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
