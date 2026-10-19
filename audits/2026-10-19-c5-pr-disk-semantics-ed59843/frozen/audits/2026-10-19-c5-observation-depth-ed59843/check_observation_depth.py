#!/usr/bin/env python3
"""Replay finite P/R observation claims; graph semantics are not an input theorem."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')
OBSERVED = ('01232', '01021', '01202', '01212')
WORDS = tuple(''.join(word) for n in range(4) for word in product('PR', repeat=n))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def replay():
    base = json.loads((ROOT / 'BASE.json').read_text())
    for entry in base['inputs']:
        data = (ROOT / entry['frozen_path']).read_bytes()
        require(sha256(data).hexdigest() == entry['sha256'], 'frozen input custody mismatch')
    source = ROOT / 'frozen/certificate_v02.json'
    cert = json.loads(source.read_bytes())
    model = cert['model']
    require(tuple(model['rows']) == ROWS, 'ordered ten-row contract mismatch')
    require(model['alphabet'] == ['P', 'R'], 'alphabet contract mismatch')
    require(cert['scope']['observed_interface'] == 'ordered_current_C5', 'interface mismatch')
    require(not cert['scope']['complete_for_all_planar_disks'], 'unsupported disk coverage')
    compact = json.dumps(model, sort_keys=True, separators=(',', ':')).encode()
    require(sha256(compact).hexdigest() == cert['model_sha256'], 'model hash mismatch')
    states = sorted(model['states'])
    require(len(states) == len(set(states)) == 132, 'state domain mismatch')
    matrices = model['operators']
    for matrix in matrices.values():
        require(len(matrix) == 10 and all(len(row) == 10 for row in matrix), 'matrix shape')
        require(all(type(x) is int and x >= 0 for row in matrix for x in row), 'matrix coefficient')

    def step(q, letter):
        return sum(1 << i for i, row in enumerate(matrices[letter])
                   if any(coefficient and q & (1 << j) for j, coefficient in enumerate(row)))

    def run(q, word):
        for letter in word:
            q = step(q, letter)
        return q

    bits = [ROWS.index(row) for row in OBSERVED]

    def observe(q):
        return tuple((q >> bit) & 1 for bit in bits)

    require(set(model['transitions']) == set(map(str, states)), 'transition domain')
    for q in states:
        require(set(model['transitions'][str(q)]) == {'P', 'R'}, 'transition alphabet')
        for letter in 'PR':
            target = step(q, letter)
            require(target in states and target == model['transitions'][str(q)][letter],
                    'matrix/transition mismatch')
        construction = model['reachable_words_F'][str(q)]
        require(construction.startswith('F') and run(model['seeds']['F']['mask'], construction[1:]) == q,
                'F construction witness mismatch')

    outputs = {q: tuple(observe(run(q, word)) for word in WORDS) for q in states}
    partitions = []
    for depth in range(4):
        groups = defaultdict(list)
        for q in states:
            groups[outputs[q][:(1 << (depth + 1)) - 1]].append(q)
        partitions.append(sorted(groups.values()))
    require(partitions == cert['refinement']['four_fibres']['rounds'], 'refinement partition mismatch')
    counts = [len(p) for p in partitions]
    require(counts == [15, 66, 97, 132], 'refinement depth counts')

    histogram = Counter()
    depth_three_pairs = []
    pairs = list(combinations(states, 2))
    for q, r in pairs:
        index = next(i for i in range(len(WORDS)) if outputs[q][i] != outputs[r][i])
        word = WORDS[index]
        histogram[len(word)] += 1
        if len(word) == 3:
            depth_three_pairs.append({'states': [q, r], 'shortest_suffix': word,
                                      'terminal_outputs': [outputs[q][index], outputs[r][index]]})
    require(histogram == {0: 7661, 1: 820, 2: 106, 3: 59}, 'shortest depth histogram')

    # Exact experiment subset search. Each four-bit terminal observation is one query.
    failures = []
    subset_counts = []
    minimum_sets = []
    for size in range(4):
        checked = 0
        winners = []
        for indices in combinations(range(len(WORDS)), size):
            checked += 1
            seen = {}
            collision = None
            for q in states:
                key = tuple(outputs[q][i] for i in indices)
                if key in seen:
                    collision = [seen[key], q]
                    break
                seen[key] = q
            if collision is None:
                winners.append([WORDS[i] for i in indices])
            elif size < 3:
                failures.append({'words': [WORDS[i] for i in indices], 'collision': collision})
        subset_counts.append({'size': size, 'subsets_checked': checked, 'separating_subsets': len(winners)})
        if winners:
            minimum_sets = winners
            break
    require(minimum_sets == [['RR', 'PRR', 'RRR']], 'minimum probe basis')
    basis = minimum_sets[0]

    # Boolean support formulas, composed from the frozen nonnegative matrices.
    formulas = []
    for word in basis:
        expressions = [{j} for j in range(10)]
        for letter in word:
            expressions = [set().union(*(expressions[j] for j, c in enumerate(row) if c))
                           for row in matrices[letter]]
        formulas.append([sorted(expressions[i]) for i in bits])
    expected_formulas = [[[2], [4], [0], [1]], [[5], [9], [7], [3, 8]], [[8], [6], [1], [3]]]
    require(formulas == expected_formulas, 'probe Boolean formulas')
    # Each decoder entry is [probe index, output index], both zero-based.
    decoder = [[0, 2], [0, 3], [0, 0], [2, 3], [0, 1],
               [1, 0], [2, 1], [1, 2], [2, 0], [1, 1]]

    def decode(signature):
        return sum(signature[p][i] << j for j, (p, i) in enumerate(decoder))

    formal_signatures = set()
    for q in range(1024):
        signature = tuple(observe(run(q, word)) for word in basis)
        require(decode(signature) == q, 'all-mask decoding failure')
        a, b, c = signature
        require(c[2] == a[3] and b[3] == (c[3] | c[0]), 'output redundancy equation')
        formal_signatures.add(signature)
    require(len(formal_signatures) == 1024, 'all-mask injectivity')
    constrained_outputs = set()
    for raw in product((0, 1), repeat=12):
        a, b, c = raw[:4], raw[4:8], raw[8:]
        if c[2] == a[3] and b[3] == (c[3] | c[0]):
            constrained_outputs.add((a, b, c))
    require(constrained_outputs == formal_signatures, 'exact image characterization')

    q, r, word = 91, 347, 'RRR'
    require(outputs[q][:7] == outputs[r][:7], 'tight witness agrees through depth two')
    require(observe(run(q, word)) != observe(run(r, word)), 'tight witness separates at three')
    witness = {'states': [q, r], 'construction_words': [model['reachable_words_F'][str(s)] for s in (q, r)],
               'all_depth_at_most_two': [{'word': w, 'common_output': outputs[q][i]}
                                          for i, w in enumerate(WORDS[:7])],
               'distinguishing_suffix': word, 'terminal_states': [run(q, word), run(r, word)],
               'terminal_outputs': [observe(run(q, word)), observe(run(r, word))]}
    return {'schema': 'c5-pr-four-row-observation/v1',
            'scope': {'finite_states': 132, 'formal_masks_for_algebra': 1024,
                      'same_start_for_each_probe': True, 'graph_operation_semantics_verified': False,
                      'general_disk_coverage': False, 'counts_reconstructed': False, 'new_Lean_theorem': False},
            'source_sha256': sha256(source.read_bytes()).hexdigest(),
            'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'rows': ROWS, 'observed_rows': OBSERVED, 'words': WORDS,
            'partitions': partitions, 'round_counts': counts, 'minimum_uniform_depth': 3,
            'pair_count': len(pairs), 'shortest_depth_histogram': dict(sorted(histogram.items())),
            'depth_three_pairs': depth_three_pairs, 'tight_depth_witness': witness,
            'minimum_probe_count_within_depth_three': 3, 'all_minimum_probe_sets': minimum_sets,
            'subset_search': subset_counts, 'all_smaller_probe_set_collisions': failures,
            'basis_boolean_formulas_as_source_indices': formulas,
            'decoder_probe_and_output_indices': decoder, 'formal_mask_decoder_checks': 1024,
            'formal_image_constraints': ['c[2] == a[3]', 'b[3] == (c[3] OR c[0])'],
            'formal_image_size': len(constrained_outputs),
            'state_observation_vectors': [{'mask': q, 'outputs': outputs[q]} for q in states]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true', help='exclusive-create replay certificate')
    mode.add_argument('--check', action='store_true', help='recompute and byte-compare without writing')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    try:
        result = replay()
        data = encoded(result)
        if args.write:
            with args.certificate.open('xb') as handle:
                handle.write(data)
        else:
            require(args.certificate.read_bytes() == data, 'replay certificate mismatch')
        print(json.dumps({'pass': True, 'round_counts': result['round_counts'],
                          'pair_histogram': result['shortest_depth_histogram'],
                          'minimum_probe_sets': result['all_minimum_probe_sets'],
                          'formal_masks_decoded': result['formal_mask_decoder_checks']}, sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, StopIteration) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
