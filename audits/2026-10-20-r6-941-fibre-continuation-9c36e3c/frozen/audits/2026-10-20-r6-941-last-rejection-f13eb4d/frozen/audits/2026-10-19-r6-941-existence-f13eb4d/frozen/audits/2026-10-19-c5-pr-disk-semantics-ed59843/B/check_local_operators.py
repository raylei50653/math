#!/usr/bin/env python3
"""Compile fixed-literal C5 transfer counts from six/five-vertex graph patches.

The imported matrices are comparison targets only; neither compilation nor
classification reads their entries. --check does not write any file.
"""

import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
P_SPEC = {'vertex_count': 6, 'old_boundary': (0, 1, 2, 3, 4),
          'new_boundary': (5, 1, 2, 3, 4),
          'edges': CYCLE + ((5, 4), (5, 0), (5, 1))}
R_SPEC = {'vertex_count': 5, 'old_boundary': (0, 1, 2, 3, 4),
          'new_boundary': (4, 0, 1, 2, 3), 'edges': CYCLE}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def canonical_transport(literal):
    """Unique permutation to restricted-growth form, including the fourth colour.

    A proper C5 uses at least three of the four colours, so its unused colour,
    when present, has a unique unused image. The permutation acts globally on
    every vertex of a complete disk colouring, not merely on its boundary.
    """
    transport = {}
    for colour in literal:
        if colour not in transport:
            transport[colour] = len(transport)
    unused_images = iter(sorted(set(range(4)) - set(transport.values())))
    for colour in range(4):
        if colour not in transport:
            transport[colour] = next(unused_images)
    permutation = tuple(transport[colour] for colour in range(4))
    return ''.join(str(permutation[colour]) for colour in literal), permutation


def proper(assignment, edges):
    return all(assignment[u] != assignment[v] for u, v in edges)


def compile_patch(spec, retain_fibres=True, transport=True):
    """Enumerate all 4^n vertex assignments of an actual local graph.

    Every proper target literal has all ten source slots, including empties.
    A slot contains one witness per local colouring. Its source permutation
    gives the bijection from that literal source fibre to the canonical fibre.
    No imported matrix is used here.
    """
    targets = tuple(a for a in product(range(4), repeat=5) if proper(a, CYCLE))
    fibres = {target: [[] for _ in ROWS] for target in targets}
    accepted = 0
    discarded_without_transport = 0
    for assignment in product(range(4), repeat=spec['vertex_count']):
        if not proper(assignment, spec['edges']):
            continue
        old = tuple(assignment[i] for i in spec['old_boundary'])
        new = tuple(assignment[i] for i in spec['new_boundary'])
        require(new in fibres, 'patch did not preserve a proper target C5')
        row, permutation = canonical_transport(old)
        require(row in ROWS, 'patch admitted an improper source C5')
        if not transport:
            literal_name = ''.join(map(str, old))
            if literal_name not in ROWS:
                discarded_without_transport += 1
                continue
            row = literal_name
        witness = {'assignment': assignment,
                   'source_to_canonical': permutation}
        fibres[new][ROWS.index(row)].append(witness)
        accepted += 1
    matrix = [[len(slot) for slot in fibres[tuple(map(int, row))]] for row in ROWS]
    if transport:
        for target, slots in fibres.items():
            row, permutation = canonical_transport(target)
            require([len(slot) for slot in slots] == matrix[ROWS.index(row)],
                    'literal count depends on arbitrary colour names')
            # Check the full transport on each graph vertex; source and target
            # are read off the same assignment before and after this action.
            inverse = tuple(permutation.index(c) for c in range(4))
            for slot in slots:
                for witness in slot:
                    assignment = witness['assignment']
                    moved = tuple(permutation[c] for c in assignment)
                    require(proper(moved, spec['edges']), 'global transport broke an edge')
                    require(tuple(inverse[c] for c in moved) == assignment,
                            'global transport lacks its inverse')
                    moved_source = tuple(moved[i] for i in spec['old_boundary'])
                    require(canonical_transport(moved_source)[0] ==
                            canonical_transport(tuple(assignment[i] for i in spec['old_boundary']))[0],
                            'global transport changed a source colour class')
    return {'spec': spec, 'assignments_enumerated': 4 ** spec['vertex_count'],
            'proper_patch_assignments': accepted,
            'discarded_without_transport': discarded_without_transport,
            'proper_target_literals': len(targets), 'matrix': matrix,
            'literal_fibres': [
                {'target': target, 'canonical_target_row': canonical_transport(target)[0],
                 'target_to_canonical': canonical_transport(target)[1],
                 'source_fibres': fibres[target]}
                for target in targets] if retain_fibres else []}


def compare_matrix(actual, expected, label):
    require(len(actual) == len(expected) == 10, label + ': matrix height')
    for i, (actual_row, expected_row) in enumerate(zip(actual, expected)):
        require(len(actual_row) == len(expected_row) == 10, label + ': matrix width')
        for j, (a, b) in enumerate(zip(actual_row, expected_row)):
            require(type(a) is int and type(b) is int and a >= 0 and b >= 0,
                    label + ': nonnegative integer coefficient')
            require(a == b, f'{label}: target {ROWS[i]}, source {ROWS[j]}: {a} != {b}')


def first_difference(actual, expected):
    for i in range(10):
        for j in range(10):
            if actual[i][j] != expected[i][j]:
                return {'target_row': ROWS[i], 'source_row': ROWS[j],
                        'mutated_coefficient': actual[i][j],
                        'required_coefficient': expected[i][j]}
    raise ValueError('negative control unexpectedly had no difference')


def step(mask, matrix):
    return sum(1 << i for i, row in enumerate(matrix)
               if any(c and mask & (1 << j) for j, c in enumerate(row)))


def replay():
    base = json.loads((AUDIT / 'BASE.json').read_bytes())
    custody = []
    for name, entry in sorted(base['inputs'].items()):
        data = (AUDIT / entry['frozen']).read_bytes()
        require(len(data) == entry['size'] and sha256(data).hexdigest() == entry['sha256'],
                'frozen input custody mismatch: ' + name)
        custody.append({'source': name, 'sha256': entry['sha256'], 'size': len(data)})
    source_path = AUDIT / 'frozen/docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json'
    source = json.loads(source_path.read_bytes())
    model = source['model']
    require(tuple(model['rows']) == ROWS, 'ordered source row contract mismatch')
    require(model['alphabet'] == ['P', 'R'], 'source alphabet contract mismatch')
    require(source['scope']['observed_interface'] == 'ordered_current_C5',
            'source interface contract mismatch')
    require(not source['scope']['complete_for_all_planar_disks'],
            'source wrongly claims general disk coverage')
    all_proper = [literal for literal in product(range(4), repeat=5) if proper(literal, CYCLE)]
    require(len(all_proper) == 240, 'proper C5 literal count')
    require(sorted(set(canonical_transport(literal)[0] for literal in all_proper)) == list(ROWS),
            'ten rows are not the complete proper C5 colour quotient')
    # The full S4 action has exactly these orbits, not just equal supports.
    colour_permutations = tuple(permutations(range(4)))
    for literal in all_proper:
        row, transport = canonical_transport(literal)
        require(tuple(transport[c] for c in literal) == tuple(map(int, row)),
                'transport did not reach the fixed canonical literal')
        orbit = {tuple(p[c] for c in literal) for p in colour_permutations}
        require(len(orbit) == 24 and all(canonical_transport(a)[0] == row for a in orbit),
                'full colour orbit mismatch')
    compiled = {'P': compile_patch(P_SPEC), 'R': compile_patch(R_SPEC)}
    for letter, result in compiled.items():
        compare_matrix(result['matrix'], model['operators'][letter], letter)
        require(result['proper_target_literals'] == 240, 'missing literal target fibre')
        require(sum(len(slot) == 0 for fibre in result['literal_fibres']
                    for slot in fibre['source_fibres']) == 2400 - result['proper_patch_assignments'],
                'empty source fibre accounting mismatch')
    require(compiled['P']['proper_patch_assignments'] == 312, 'P proper local count')
    require(compiled['R']['proper_patch_assignments'] == 240, 'R proper local count')
    formal_outputs = []
    for mask in range(1024):
        outputs = {letter: step(mask, result['matrix']) for letter, result in compiled.items()}
        require(all(outputs[letter] == step(mask, model['operators'][letter]) for letter in 'PR'),
                'all-mask operator support mismatch')
        formal_outputs.append({'source_mask': mask, 'targets': outputs})
    transition_checks = []
    for mask in sorted(model['states']):
        for letter in 'PR':
            actual = step(mask, compiled[letter]['matrix'])
            require(actual == model['transitions'][str(mask)][letter],
                    'derived operator/source transition mismatch')
            transition_checks.append({'source': mask, 'letter': letter, 'target': actual})
    mutations = [
        ('rotate_two_positions', 'R',
         compile_patch(dict(R_SPEC, new_boundary=(3, 4, 0, 1, 2)), False)['matrix']),
        ('omit_attachment_to_old_b0', 'P',
         compile_patch(dict(P_SPEC, edges=CYCLE + ((5, 4), (5, 1))), False)['matrix']),
        ('omit_canonical_colour_transport', 'P',
         compile_patch(P_SPEC, False, False)['matrix']),
        ('transpose_matrix_convention', 'R',
         [list(row) for row in zip(*compiled['R']['matrix'])]),
    ]
    controls = []
    for name, letter, mutated in mutations:
        try:
            compare_matrix(mutated, model['operators'][letter], name)
        except ValueError as error:
            controls.append({'name': name, 'operator': letter, 'rejected': True,
                             'reason': str(error),
                             'first_difference': first_difference(mutated, model['operators'][letter])})
        else:
            raise ValueError('pollution control was accepted: ' + name)
    return {'schema': 'c5-pr-local-graph-compilation/v1',
            'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'base_sha256': sha256((AUDIT / 'BASE.json').read_bytes()).hexdigest(),
            'frozen_inputs': custody, 'rows': ROWS,
            'scope': {'local_graph_semantics': 'explicit reconstructed total collar P and right rotation R',
                      'source_original_generator_replayed': False,
                      'arbitrary_disk_size_enumerated': False,
                      'general_disk_grammar_coverage': False,
                      'full_fixed_literal_fibres': True,
                      'global_colour_transport': True,
                      'new_Lean_theorem': False},
            'proper_C5_literals': 240, 'full_colour_orbit_size': 24,
            'assignments_enumerated': sum(r['assignments_enumerated'] for r in compiled.values()),
            'operators': compiled, 'all_formal_mask_transfers': formal_outputs,
            'source_transition_checks': transition_checks,
            'negative_controls': controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true', help='exclusive-create local certificate')
    mode.add_argument('--check', action='store_true', help='recompute and byte-compare, read-only')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    try:
        result = replay()
        data = encoded(result)
        destination = args.certificate.resolve()
        require(destination.parent == HERE, 'certificate must remain inside exclusive B directory')
        if args.write:
            with destination.open('xb') as handle:
                handle.write(data)
        else:
            require(destination.read_bytes() == data, 'local compilation certificate mismatch')
        print(json.dumps({'pass': True, 'assignments_enumerated': result['assignments_enumerated'],
                          'proper_patch_assignments': {k: v['proper_patch_assignments']
                                                       for k, v in result['operators'].items()},
                          'proper_target_literals_per_operator': 240,
                          'integer_matrix_entries_checked': 200,
                          'formal_mask_transfers_checked': 2048,
                          'source_transitions_checked': len(result['source_transition_checks']),
                          'negative_controls_rejected': len(result['negative_controls'])}, sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, StopIteration) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
