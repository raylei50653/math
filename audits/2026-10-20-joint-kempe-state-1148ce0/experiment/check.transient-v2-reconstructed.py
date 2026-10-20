#!/usr/bin/env python3
"""Frozen 132-cell, same-coloring six-partition Kempe-state falsification.

--generate creates certificate.json exclusively; --check recomputes read-only.
Uses only Python's standard library. Full literal lifts of all ten prescribed
boundary patterns are enumerated, including empty fibres. Targets are never
palette-normalized. The catalogue is the exact scope; no graph search occurs.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
CAT = AUDIT / 'frozen/artifacts/c5_cells/cells.json'
OUT = HERE / 'certificate.json'
PAIRS = tuple(combinations(range(4), 2))
BOUNDARY = tuple(range(5))
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))


def edges_of(entry):
    return tuple(sorted({tuple(sorted(e)) for e in (*CYCLE, *entry['edges'])}))


def adjacency(n, edges):
    answer = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        answer[u].add(v)
        answer[v].add(u)
    return answer


def proper(c, edges):
    return all(x in range(4) for x in c) and all(c[u] != c[v] for u, v in edges)


def lifts(adj, boundary):
    """All literal extensions, each exactly once; boundary is held fixed."""
    c = list(boundary) + [-1] * (len(adj) - len(boundary))
    if any(c[u] == c[v] for u in BOUNDARY for v in adj[u] if v < 5):
        return

    def visit():
        unseen = [u for u, color in enumerate(c) if color < 0]
        if not unseen:
            yield tuple(c)
            return
        u = max(unseen, key=lambda v: (len({c[w] for w in adj[v] if c[w] >= 0}),
                                       len(adj[v]), -v))
        forbidden = {c[v] for v in adj[u]}
        for color in range(4):
            if color not in forbidden:
                c[u] = color
                yield from visit()
        c[u] = -1

    yield from visit()


def components(adj, c, pair):
    unseen = {v for v, color in enumerate(c) if color in pair}
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        for u in queue:
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                queue.append(v)
        answer.append(tuple(sorted(queue)))
    return tuple(answer)


def all_components(adj, c):
    return tuple(components(adj, c, pair) for pair in PAIRS)


def signature(c, full_components):
    """Literal B colors followed by six partitions, from this one full lift."""
    return (c[:5], tuple(tuple(tuple(v for v in block if v < 5)
                               for block in comp if any(v < 5 for v in block))
                         for comp in full_components))


def swap(c, pair, comp):
    return tuple(sum(pair) - color if v in comp else color
                 for v, color in enumerate(c))


def record(adj, c, pair, root):
    before = all_components(adj, c)
    index = PAIRS.index(pair)
    comp = next(block for block in before[index] if root in block)
    target = swap(c, pair, comp)
    after = all_components(adj, target)
    return dict(source=list(c), source_components=before,
                source_signature=signature(c, before), selected_component=comp,
                target=target, target_components=after,
                target_signature=signature(target, after))


def json_form(value):
    return json.loads(json.dumps(value))


def validate_witness(witness, catalogue):
    entry = catalogue['cells'][str(witness['mask'])]
    edges = edges_of(entry)
    assert witness['edges'] == json_form(edges)
    n = 5 + entry['k_eff']
    assert witness['n'] == n
    adj = adjacency(n, edges)
    pair, root = tuple(witness['action']['pair']), witness['action']['root']
    assert pair in PAIRS and root in BOUNDARY
    left, right = witness['lifts']
    for lift in (left, right):
        c = tuple(lift['source'])
        assert len(c) == n and proper(c, edges) and c[root] in pair
        assert c[:5] in [tuple(b) for b in catalogue['pattern_order']]
        assert lift == json_form(record(adj, c, pair, root))
        assert proper(lift['target'], edges)
    assert left['source'] != right['source']
    assert left['source_signature'] == right['source_signature']
    assert left['target_signature'] != right['target_signature']
    assert left['target'][:5] == right['target'][:5]


def disk_faces_control(witness):
    """An oriented combinatorial disk certificate for the first fixed witness."""
    assert witness['mask'] == 95
    faces = ((0, 1, 7), (1, 2, 7), (2, 3, 6), (3, 4, 6), (4, 0, 6),
             (0, 5, 6), (2, 6, 5), (0, 7, 5), (2, 5, 7))
    directed = tuple((f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    assert len(set(directed)) == len(directed)
    assert {tuple(sorted(e)) for e in directed} == {tuple(e) for e in witness['edges']}
    assert {e for e in directed if e[::-1] not in directed} == set(CYCLE)
    assert witness['n'] - len(witness['edges']) + len(faces) == 1
    for v in range(witness['n']):
        link_edges = [tuple(sorted(w for w in face if w != v))
                      for face in faces if v in face]
        link = adjacency(witness['n'], link_edges)
        active = {u for edge in link_edges for u in edge}
        todo = [min(active)]
        reached = set(todo)
        for u in todo:
            for w in link[u] - reached:
                reached.add(w)
                todo.append(w)
        assert reached == active
        expected = [1, 1] + [2] * (len(active) - 2) if v < 5 else [2] * len(active)
        assert sorted(len(link[u]) for u in active) == expected
    return faces


def negative_controls(witness, catalogue):
    controls = {}
    changes = {
        'deleted_source_edge': lambda w: w['edges'].pop(0),
        'improper_full_lift': lambda w: w['lifts'][0]['source'].__setitem__(1, 0),
        'incomplete_selected_component': lambda w: w['lifts'][0]['selected_component'].pop(),
        'forged_equal_target_signature': lambda w: w['lifts'][1].__setitem__(
            'target_signature', deepcopy(w['lifts'][0]['target_signature'])),
    }
    for name, change in changes.items():
        bad = deepcopy(witness)
        change(bad)
        try:
            validate_witness(bad, catalogue)
        except AssertionError:
            controls[name] = 'rejected'
        else:
            raise AssertionError('Negative control accepted: ' + name)
    return controls


def two_step_readout(witness):
    """One shared second action makes the differing hidden partitions visible."""
    adj = adjacency(witness['n'], witness['edges'])
    pair, root = (0, 1), 0
    lifts_after_first = [record(adj, tuple(lift['target']), pair, root)
                         for lift in witness['lifts']]
    assert lifts_after_first[0]['target'][:5] == (1, 2, 1, 0, 2)
    assert lifts_after_first[1]['target'][:5] == (1, 2, 0, 1, 2)
    assert all(proper(lift['target'], witness['edges']) for lift in lifts_after_first)
    return dict(second_action=dict(pair=pair, root=root),
                lifts_after_first=lifts_after_first)


def report():
    catalogue = json.loads(CAT.read_text())
    patterns = tuple(tuple(b) for b in catalogue['pattern_order'])
    assert len(patterns) == 10 and len(catalogue['cells']) == 132
    rows, first_witness = [], None
    for mask_text, entry in sorted(catalogue['cells'].items(), key=lambda item: int(item[0])):
        mask = int(mask_text)
        n, edges = 5 + entry['k_eff'], edges_of(entry)
        adj = adjacency(n, edges)
        transitions = defaultdict(set)
        states_by_boundary = defaultdict(set)
        first_lift = {}
        fibres = []
        action_count = 0
        state_lift_counts = defaultdict(int)
        for b in patterns:
            fibre = sorted(lifts(adj, b))
            assert len(fibre) == len(set(fibre))
            fibres.append([''.join(map(str, c)) for c in fibre])
            for c in fibre:
                assert proper(c, edges)
                before = all_components(adj, c)
                state = signature(c, before)
                states_by_boundary[b].add(state)
                state_lift_counts[state] += 1
                for pair, comp_list in zip(PAIRS, before):
                    for comp in comp_list:
                        roots = [v for v in comp if v < 5]
                        if not roots:
                            continue
                        target = swap(c, pair, comp)
                        assert proper(target, edges)
                        target_state = signature(target, all_components(adj, target))
                        for root in roots:
                            action_count += 1
                            key = (state, pair, root)
                            if first_witness is None and transitions[key] and target_state not in transitions[key]:
                                first_witness = json_form(dict(mask=mask, n=n, edges=edges,
                                    action=dict(pair=pair, root=root),
                                    lifts=[record(adj, first_lift[key], pair, root),
                                           record(adj, c, pair, root)]))
                            transitions[key].add(target_state)
                            first_lift.setdefault(key, c)
        counts = [len(fibre) for fibre in fibres]
        computed_mask = sum(1 << i for i, count in enumerate(counts) if count)
        assert computed_mask == mask
        assert action_count == 15 * sum(counts)
        ambiguous = [key for key, targets in transitions.items() if len(targets) > 1]
        rows.append(dict(mask=mask, n=n, edges=edges,
                         fibres=fibres, fibre_counts=counts,
                         joint_states_by_fibre=[len(states_by_boundary[b]) for b in patterns],
                         joint_states=len(state_lift_counts),
                         states_merging_full_lifts=sum(count > 1 for count in state_lift_counts.values()),
                         enabled_rooted_actions=action_count,
                         state_action_pairs=len(transitions),
                         ambiguous_state_action_pairs=len(ambiguous),
                         ambiguous_joint_states=len({key[0] for key in ambiguous}),
                         max_target_states=max(map(len, transitions.values()), default=0)))
    assert first_witness is not None
    validate_witness(first_witness, catalogue)
    faces = disk_faces_control(first_witness)
    controls = negative_controls(first_witness, catalogue)
    totals = dict(graphs=len(rows), fibres=10 * len(rows),
                  empty_fibres=sum(count == 0 for row in rows for count in row['fibre_counts']),
                  full_lifts=sum(sum(row['fibre_counts']) for row in rows),
                  joint_states=sum(row['joint_states'] for row in rows),
                  boundary_fibres_split_by_joint_state=sum(count > 1 for row in rows for count in row['joint_states_by_fibre']),
                  graphs_with_boundary_fibre_split=sum(any(count > 1 for count in row['joint_states_by_fibre']) for row in rows),
                  enabled_rooted_actions=sum(row['enabled_rooted_actions'] for row in rows),
                  state_action_pairs=sum(row['state_action_pairs'] for row in rows),
                  ambiguous_state_action_pairs=sum(row['ambiguous_state_action_pairs'] for row in rows),
                  ambiguous_joint_states=sum(row['ambiguous_joint_states'] for row in rows),
                  graphs_with_collision=sum(row['ambiguous_joint_states'] > 0 for row in rows))
    return dict(schema='joint-kempe-fixed-catalogue-v1',
                scope='Exactly the 132 saved graphs; all 10 literal canonical C5 boundary fibres, including empties; all full extensions; all enabled (pair, boundary-root) actions. No graph search and no independent palette normalization.',
                trust='Finite exact certificate plus explicit combinatorial disk witness. Not Lean, not a source-941 realization, not a smaller-bad construction.',
                input_sha256=sha256(CAT.read_bytes()).hexdigest(),
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                boundary=BOUNDARY, pair_order=PAIRS, pattern_order=patterns,
                fibre_encoding='Each entry is the entire literal coloring c[0]...c[n-1], one digit per fixed vertex; array position selects pattern_order, even for an empty fibre.',
                totals=totals, cells=rows, counterexample=first_witness,
                counterexample_oriented_disk_faces=faces,
                two_step_boundary_readout=two_step_readout(first_witness),
                negative_controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--generate', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')) + '\n'
    if args.generate:
        with OUT.open('x') as handle:
            handle.write(encoded)
    else:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect without overwriting.'
    print(json.dumps(dict(status='PASS', certificate_bytes=len(encoded.encode()),
                          **result['totals']), sort_keys=True))


if __name__ == '__main__':
    main()
