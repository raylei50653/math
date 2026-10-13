#!/usr/bin/env python3
"""Exhaustive arithmetic on the fixed five named boundary vertices, not sources."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = tuple(range(5))
EDGES = tuple((i, (i + 1) % 5) for i in B)
ROWS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}
MAIN_SHA = '516c44fc1480002c4fe358ea5ce0cc69349d55ed463427c685db42ec887ec2a7'


def require(test, message):
    if not test:
        raise ValueError(message)


def generate():
    main_bytes = (HERE / 'observations.json').read_bytes()
    require(hashlib.sha256(main_bytes).hexdigest() == MAIN_SHA, 'main certificate drift')
    main = json.loads(main_bytes)
    entries = []
    survivors = []
    for mask in range(32):
        T = {v for v in B if mask & (1 << v)}
        closure = {v for v in B if all(q[v] in {q[t] for t in T} for q in ROWS.values())}
        saved = main['literal_spoke_contact_signature_closure']['all_32_T_subsets'][mask]
        require(sorted(T) == saved['T_named_vertices'], 'named T mismatch')
        require(sorted(closure) == saved['three_row_signature_closure'], 'closure mismatch')
        leaf_edges = [list(e) for e in EDGES if set(e) <= closure and not set(e) <= T]
        all_distinct_pairs = [list(pair) for pair in itertools.combinations(leaf_edges, 2)]
        entry = {'T_mask_in_boundary_order': mask, 'T_original_named_vertices': sorted(T),
                 'three_row_signature_closure': sorted(closure),
                 'missing_reachable_vertices': sorted(closure - T),
                 'candidate_original_leaf_attachment_edges': leaf_edges,
                 'all_distinct_candidate_leaf_edge_pairs': all_distinct_pairs,
                 'two_distinct_leaf_edges_available': bool(all_distinct_pairs)}
        entries.append(entry)
        if all_distinct_pairs:
            require(len(T) == 4 and len(closure - T) == 1, 'survivor shape')
            h = next(iter(closure - T))
            require(h in (2, 4), 'unexpected omitted boundary vertex')
            require(all(h in e for e in leaf_edges) and len(leaf_edges) == 2,
                    'survivor is not both incident edges')
            survivors.append({'T_original_named_vertices': sorted(T),
                              'omitted_named_vertex_h': h,
                              'exact_original_leaf_attachment_edges': leaf_edges})
    require({s['omitted_named_vertex_h'] for s in survivors} == {2, 4}
            and len(survivors) == 2, 'two-leaf survivor completeness')
    return {'schema': 'n2-one-long-named-boundary-leaf-edge-v1',
            'scope': 'all 32 subsets of the five fixed named boundary vertices; no source enumeration',
            'main_certificate_sha256': MAIN_SHA,
            'literal_boundary_order': list(B), 'literal_boundary_edges': [list(e) for e in EDGES],
            'literal_target_rows': {str(i): list(q) for i, q in ROWS.items()},
            'necessary_leaf_edge_rule': 'e subset cl(T), and e not subset T',
            'topological_premises_are_external': ['leaf attachments are original boundary edges',
                                                  'at least two leaf bridges',
                                                  'distinct leaf edges by attachment injection',
                                                  'every leaf edge satisfies the stated necessary rule'],
            'all_32_T_entries': entries, 'exact_two_leaf_boundary_survivors': survivors,
            'finite_boundary_arithmetic_status': 'triggered and holds',
            'target_source_status': 'not triggered',
            'counts': {'T_subsets': 32, 'T_with_any_candidate_leaf_edge':
                       sum(bool(e['candidate_original_leaf_attachment_edges']) for e in entries),
                       'T_with_two_distinct_candidate_leaf_edges': len(survivors), 'target_sources': 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'boundary_observations.json')
    args = parser.parse_args()
    data = generate()
    encoded = (json.dumps(data, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as stream:
            stream.write(encoded)
    else:
        require(args.artifact.read_bytes() == encoded, 'boundary artifact mismatch')
    print(json.dumps({'mode': 'write' if args.write else 'check',
                      'bytes': len(encoded), 'sha256': hashlib.sha256(encoded).hexdigest(),
                      'counts': data['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
