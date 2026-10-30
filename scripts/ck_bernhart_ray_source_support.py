#!/usr/bin/env python3
"""Exact support factorization and a common-token action relaxation of ray r2.

Tokens are NOT graph colorings: no original edges, rotation, or retained systems
are supplied. The construction works at every positive even scale and therefore
cannot prove either actual realizability or actual-source nonrealizability.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ck_bernhart_benchmark as benchmark
from four_color_counts_cone_verification import compatible, signatures

SOURCE = ROOT / 'audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json'
DEFAULT = ROOT / 'audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json'
PAIRS = ((1, 2), (1, 3), (2, 3))
REST = (0, 1, 4, 5, 6, 7)


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))


def report():
    receipt = json.loads((SOURCE.parent / 'RECEIPT.json').read_text())
    source_hash = sha256(SOURCE.read_bytes()).hexdigest()
    assert source_hash == receipt['sources_sha256'][str(SOURCE.relative_to(ROOT))]
    words, sigs, states, rows, columns = benchmark.cone_data()
    ray = json.loads(SOURCE.read_text())['exact_nonextremality']['parts'][1]
    y = {r['index']: r['weight'] for r in ray['signature_weights']}
    n = {r['index']: r['count'] for r in ray['pattern_counts']}
    assert len(n) == 41 and len(y) == 46 and set(y.values()) == {1}
    actual = [0] * len(rows)
    for signature, value in y.items():
        for row in columns[signature]:
            actual[row] += value
    assert all(actual[row] == n.get(states[wi], 0) for row, (wi, _) in enumerate(rows))
    counts = {w: n.get(states[i], 0) for i, w in enumerate(words)}
    all_words = tuple(product((1, 2, 3), repeat=8))
    assert all(not counts.get(w, 0) for w in all_words if w[2] != w[3])
    six_counts = {}
    factors = []
    for u in product((1, 2, 3), repeat=6):
        vv = []
        for color in (1, 2, 3):
            w = [None] * 8
            for port, value in zip(REST, u):
                w[port] = value
            w[2] = w[3] = color
            vv.append(counts.get(tuple(w), 0))
        assert len(set(vv)) == 1
        six_counts[u] = vv[0]
        factors.append(dict(six_word=u, three_cap_colors=vv))
    assert Counter(six_counts.values()) == {0: 648, 1: 75, 2: 6}
    compress = {v: i for i, v in enumerate(REST)}
    reduced = {}
    signature_pairs = []
    for s in sorted(y):
        touching = [p for p in sigs[s] if 2 in p[:2] or 3 in p[:2]]
        assert touching in ([], [(2, 3, -1)])
        short = tuple((compress[a], compress[b], sign) for a, b, sign in sigs[s] if (a, b) != (2, 3))
        key = (short, bool(touching))
        assert key not in reduced
        reduced[key] = s
    six_sigs = tuple(signatures(6))
    for short in sorted({key[0] for key in reduced}):
        assert (short, False) in reduced and (short, True) in reduced
        signature_pairs.append(dict(six_signature_index=six_sigs.index(short), six_signature=short,
                                    without_23=reduced[short, False], with_23=reduced[short, True], weight=1))
    six_y = {r['six_signature_index']: 1 for r in signature_pairs}
    assert len(six_y) == 23
    six_equations = 0
    for u in product((1, 2, 3), repeat=6):
        for pair in PAIRS:
            assert sum(v for s, v in six_y.items() if compatible(u, pair, six_sigs[s])) == six_counts[u]
            six_equations += 1

    positive = {w: value for w, value in counts.items() if value}
    choices = {w: tuple(tuple(s for s in sorted(y) if compatible(w, pair, sigs[s])) for pair in PAIRS)
               for w in positive}
    assert all(all(len(ss) == positive[w] for ss in three) for w, three in choices.items())
    # Primitive token ranks pair simultaneously with each of the three sorted
    # signature lists. This creates one common triple, rather than independent
    # marginal universes. Two orientation copies make the global color action
    # free even at monochromatic words.
    tokens = tuple((w, rank, bit) for w, value in positive.items()
                   for rank in range(value) for bit in (0, 1))
    token_set = set(tokens)

    def sig_of(token, pair_index):
        w, rank, _ = token
        return choices[w][pair_index][rank]

    def path_flip(token, pair_index, subset):
        w, rank, bit = token
        signature = sig_of(token, pair_index)
        a, b = PAIRS[pair_index]
        changed = list(w)
        for j, (u, v, _) in enumerate(sigs[signature]):
            if subset >> j & 1:
                changed[u] = a + b - changed[u]
                changed[v] = a + b - changed[v]
        target_word = tuple(changed)
        assert target_word in choices and signature in choices[target_word][pair_index]
        target = (target_word, choices[target_word][pair_index].index(signature), bit)
        assert target in token_set
        return target

    def loop_flip(token):
        w, rank, bit = token
        return (w, rank, 1 - bit)

    def permutation_parity(p):
        return sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3)) % 2

    def global_color(token, p):
        w, rank, bit = token
        return (tuple(p[c - 1] for c in w), rank, bit ^ permutation_parity(p))

    subset_actions = composition_checks = global_checks = 0
    conjugation_checks = 0
    marginal_checks = 0
    for w, value in positive.items():
        here = [t for t in tokens if t[0] == w]
        assert len(here) == 2 * value
        for j, pair in enumerate(PAIRS):
            observed = Counter(sig_of(t, j) for t in here)
            assert observed == Counter({s: 2 for s in choices[w][j]})
            marginal_checks += 1
    permutations3 = tuple(permutations((1, 2, 3)))
    for token in tokens:
        for j, pair in enumerate(PAIRS):
            s = sig_of(token, j)
            size = len(sigs[s])
            full = (1 << size) - 1
            for subset in range(1 << size):
                target = path_flip(token, j, subset)
                assert sig_of(target, j) == s
                assert path_flip(target, j, subset) == token
                assert loop_flip(target) == path_flip(loop_flip(token), j, subset)
                subset_actions += 1
                for other in range(1 << size):
                    assert path_flip(target, j, other) == path_flip(token, j, subset ^ other)
                    composition_checks += 1
            a, b = pair
            transposition = tuple(b if c == a else a if c == b else c for c in (1, 2, 3))
            assert loop_flip(path_flip(token, j, full)) == global_color(token, transposition)
        for p in permutations3:
            target = global_color(token, p)
            assert target in token_set
            if p != (1, 2, 3):
                assert target != token
            for j, pair in enumerate(PAIRS):
                target_j = PAIRS.index(tuple(sorted(p[c - 1] for c in pair)))
                assert sig_of(token, j) == sig_of(target, target_j)
                for subset in range(1 << len(sigs[sig_of(token, j)])):
                    assert global_color(path_flip(token, j, subset), p) == path_flip(target, target_j, subset)
                    conjugation_checks += 1
            assert global_color(loop_flip(token), p) == loop_flip(target)
            for q in permutations3:
                composed = tuple(q[p[c - 1] - 1] for c in (1, 2, 3))
                assert global_color(target, q) == global_color(token, composed)
                global_checks += 1
    joint_rows = [dict(word=w, count=positive[w],
                       triples=[dict(rank=rank, signatures=[choices[w][j][rank] for j in range(3)])
                                for rank in range(positive[w])]) for w in positive]
    return canonical(dict(
        selected_ray='r2, second saved primitive full-lift ray', source_sha256=source_hash,
        complete_B8_incidence_equations_checked=len(rows),
        word_factorization=dict(locked_ports=[2, 3], six_port_order=REST,
            formula='n8(w)=delta(w2,w3)*h(w0,w1,w4,w5,w6,w7)',
            six_word_count=729, positive_six_words=81, six_word_mass=87,
            six_count_histogram=dict(sorted(Counter(six_counts.values()).items())), rows=factors),
        signature_factorization=dict(positive_six_signatures=23, pairs=signature_pairs,
            six_B6_incidence_equations_checked=six_equations,
            scope='Exact tensor/count factorization only; no graph decomposition is inferred.'),
        common_token_action_relaxation=dict(
            base_scale=2, number_of_tokens=len(tokens), joint_rows=joint_rows,
            word_split_marginals_checked=marginal_checks,
            path_subset_actions_checked=subset_actions,
            same_pair_xor_compositions_checked=composition_checks,
            global_S3_compositions_checked=global_checks,
            global_S3_path_conjugations_checked=conjugation_checks,
            global_S3_loop_conjugations_checked=len(tokens) * len(permutations3),
            all_global_nonidentity_actions_fixed_point_free=True,
            loop_slot='One formal binary closed-component flip per pair; all three may act by the same bit flip.',
            all_positive_even_scales='For lambda=2m take m disjoint labelled copies; formulas and actions preserve copy index.',
            scope='Formal common tokens only. No original graph, original edges, retained wiring, cut sides, or rotation.'),
        actual_source_capping_obligation=dict(
            nonfree_case='When e2,e3 have distinct stems, delete the two leaves and join the remaining stem ends into a new marked edge f through their adjacent outer boundary interval, retaining both original stem identities as its provenance.',
            nonfree_six_lift='All six-terminal n and y are 3*lambda times the reduced h and k; the three f-color fibres each have lambda times the corresponding original count.',
            marked_edge_constraint='In every complete six-pole coloring, f lies on a closed component of each two-color system containing its color.',
            free_edge_case='If e2,e3 are the two ends of one free edge, delete that whole component instead; the remaining actual six-pole lift is lambda times (k,h), with no marked edge f.',
            scope='Paper necessary condition for every actual source at every positive even scale. It does not delete f, split off a source component, or shrink a two-colored circle.'),
        actual_source_conclusion='OPEN. The construction neither realizes an actual source nor refutes an actual-source exclusion theorem.',
        universal_necessary_condition='In every actual coloring, terminals e2/e3 have equal color and are paired in each two-color system containing that color.',
        forbidden_promotions=['A factored tensor does not split the actual source graph.',
                              'A common-token action relaxation is not a retained-wiring realization.',
                              'No even scale has been excluded as an actual graph by this certificate.',
                              'No conclusion about 76-face coordinate zeros or ordinary PM counts.']
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    if args.check:
        assert json.loads(args.check.read_text()) == result
        print(f'PASS exact support factorization and common-token actions: {args.check}')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
        print(f'Wrote {args.output}')
    model = result['common_token_action_relaxation']
    print(json.dumps({k: v for k, v in model.items() if k.endswith('checked') or k in ('base_scale', 'number_of_tokens')}, sort_keys=True))


if __name__ == '__main__':
    main()
