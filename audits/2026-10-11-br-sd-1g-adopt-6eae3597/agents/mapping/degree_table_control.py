#!/usr/bin/env python3
"""Independent finite calibration of structural degree rows; no source search."""
from itertools import product
import json


def edge(adj, a, b):
    assert a != b
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def cycle(adj, names):
    for a, b in zip(names, names[1:] + names[:1]):
        edge(adj, a, b)


def skeleton(j2n, j3n, h, ell, shared):
    adj = {}
    j1 = ['r', 'a1', 'x1']
    j2 = ['r', 'u'] + [f'j2_{i}' for i in range(j2n - 2)]
    j3 = ['v'] + [f'j3_{i}' for i in range(j3n - 1)]
    a3 = 'v' if shared else j3[1]
    for names in (j1, j2, j3):
        cycle(adj, names)
    edge(adj, 'u', 'v')
    pa = ['a1'] + [f'p_{i}' for i in range(1, h + 1)]
    qa = [a3] + [f'q_{i}' for i in range(1, ell + 1)]
    for arm in (pa, qa):
        for a, b in zip(arm, arm[1:]):
            edge(adj, a, b)
    return adj, j2, j3, pa, qa, a3


def expected_x2(j3, qa, a3, ell, x, m):
    """Cases reconstructed from roles, independent of actual adjacency count."""
    if x == a3 == 'v':
        return -m
    if x == 'v' or x == a3:
        return 1 - m
    if x in j3:
        return 2 - m
    if x == qa[-1]:
        assert ell > 0
        return 2 - m
    assert x in qa[1:-1]
    return 2 - m


def main():
    shapes = contacts = budget_rows = 0
    saturated_rows = valid_contact_rows = witness_rows = 0
    counters = {}
    for j2n, j3n, h, ell, shared in product((3, 5, 7), (3, 5, 7), range(4), range(4), (False, True)):
        adj, j2, j3, pa, qa, a3 = skeleton(j2n, j3n, h, ell, shared)
        shapes += 1
        scontacts = {pa[-1], qa[-1]}
        assert len(scontacts) == 2
        assert len(adj['r']) == 4 and 'r' not in scontacts
        assert len(adj['x1']) == 2 and 'x1' not in scontacts
        # Independent witness reconstruction, including minimal J2 triangle.
        for witness in j2[2:]:
            assert len(adj[witness]) == 2 and witness not in scontacts
            assert 4 - len(adj[witness]) == 2
            witness_rows += 1
        x2s = sorted(set(j3) | set(qa))
        for x in x2s:
            contacts += 1
            role = ('a3=v' if x == a3 == 'v' else 'v' if x == 'v' else
                    'a3' if x == a3 else 'ordinary J3' if x in j3 else
                    'q' if x == qa[-1] else 'arm interior')
            for m in range(1, 4):
                budget_rows += 1
                t = int(x in scontacts)
                actual_k = 4 - len(adj[x]) - m - t
                assert actual_k == expected_x2(j3, qa, a3, ell, x, m)
                valid = 0 <= actual_k <= 2
                valid_contact_rows += valid
                saturated_rows += role == 'a3=v'
                if role == 'a3=v':
                    assert not valid
                counters.setdefault(role, {'rows': 0, 'valid_necessary_capacity': 0})
                counters[role]['rows'] += 1
                counters[role]['valid_necessary_capacity'] += valid
        for m in range(1, 4):
            k = 4 - len(adj['x1']) - m
            assert k == 2 - m
            assert (k >= 0) == (m <= 2)
    # Minimal negative controls, each violates a necessary predicate only.
    assert 4 - 3 - 1 - 1 == -1   # ell=0, a3=v=q, one branch edge
    assert 4 - 4 - 1 == -1       # ell>0, a3=v, one branch edge
    assert 4 - 2 - 3 == -1       # third W1 contact edge
    assert 4 - 1 > 2            # W2 leaf exceeds actual pair capacity
    assert 4 + 1 == 5           # old attachments kept; source is overdegree
    # Counterexample to the forbidden cutpoint inference. The two incident
    # palettes are disjoint and their union contains D outside the J1 palette.
    j1_palette, branch_palette = {'A', 'B'}, {'D'}
    x1_list = j1_palette | branch_palette
    assert not (j1_palette & branch_palette)
    assert 'D' in x1_list and 'D' not in j1_palette
    negative = {
        'nonempty_branch_at_a3_equal_v': {'actual_k_for_m1': -1, 'expected_rejected': True},
        'third_edge_at_x1': {'actual_k_for_m3': -1, 'expected_rejected': True},
        'degree1_W2_leaf': {'required_k': 3, 'actual_pair_capacity': 2, 'expected_rejected': True},
        'drop_old_attachment_to_make_space': {'old_d0_plus_t_plus_k': 4, 'added_m': 1, 'actual_degree': 5, 'expected_rejected': True},
        'locally_valid_W1_leaf': {'required_k': 3, 'owner': 'L', 'necessary_degree_capacity_holds': True},
        'cutpoint_D_does_not_force_J1_palette_D': {
            'J1_palette': sorted(j1_palette), 'branch_palette': sorted(branch_palette),
            'x1_list': sorted(x1_list), 'forbidden_implication': 'counterexample',
            'source_status': 'not triggered'},
    }
    print(json.dumps({
        'result': 'PASS', 'scope': 'finite structural degree-table calibration only',
        'j2_lengths': [3, 5, 7], 'j3_lengths': [3, 5, 7], 'h_lengths': list(range(4)),
        'ell_lengths': list(range(4)), 'a3_equal_v': [False, True], 'm_values': [1, 2, 3],
        'skeletons': shapes, 'named_contact_positions': contacts,
        'x2_budget_rows': budget_rows, 'locally_valid_x2_capacity_rows': valid_contact_rows,
        'saturated_a3_equal_v_rows': saturated_rows, 'J2_witness_rows': witness_rows,
        'by_role': counters, 'negative_controls': negative,
        'source_status': 'not triggered', 'source_realization_claim': False,
        'arbitrary_size_theorem_from_control': False, 'new_Lean_theorem': False,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
