#!/usr/bin/env python3
"""Replay 132 frozen controls for the named C4 quotient, preserving full lifts.

The default input is ../frozen/artifacts/c5_cells/cells.json relative to this
script's directory. --input permits relocation but enforces the frozen hash.
Default output creation is exclusive; --check reads and compares JSON only.
This script does not enumerate source graphs or certify arbitrary-size claims.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = '04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8'
A, B, C, D = range(4)


def edge_set(edges):
    return {tuple(sorted(e)) for e in edges}


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for v, w in edges:
        adj[v].add(w)
        adj[w].add(v)
    return adj


def fibre(vertices, edges, pins):
    """Direct complete assignment enumeration, without source-mask shortcuts."""
    vs = tuple(sorted(vertices))
    adj = adjacency(vs, edges)
    if any(v == w for v, w in edges):
        return set()
    if any(v in pins and w in pins and pins[v] == pins[w] for v, w in edges):
        return set()
    free = sorted((v for v in vs if v not in pins), key=lambda v: (-len(adj[v]), v))
    colors = dict(pins)
    out = set()

    def go(i):
        if i == len(free):
            out.add(tuple(colors[v] for v in vs))
            return
        v = free[i]
        for color in range(4):
            if all(colors.get(w) != color for w in adj[v]):
                colors[v] = color
                go(i + 1)
        colors.pop(v, None)

    go(0)
    return out


def component(vs, edges, t, root, pair):
    adj = adjacency(vs, edges)
    color = dict(zip(vs, t))
    assert color[root] in pair
    found, todo = {root}, [root]
    while todo:
        for w in adj[todo.pop()] - found:
            if color[w] in pair:
                found.add(w)
                todo.append(w)
    return found


def kempe_moves(vs, edges, t, pins):
    color = dict(zip(vs, t))
    for pair in combinations(range(4), 2):
        unseen = {v for v in vs if color[v] in pair}
        while unseen:
            comp = component(vs, edges, t, min(unseen), pair)
            unseen -= comp
            if comp & pins:
                continue
            result = tuple(pair[1] if v in comp and color[v] == pair[0]
                           else pair[0] if v in comp else color[v] for v in vs)
            yield result, {'pair': list(pair), 'component': sorted(comp)}


def digest(rows):
    return sha256(json.dumps(sorted(rows), separators=(',', ':')).encode()).hexdigest()


def cd_swap(row):
    return tuple(D if color == C else C if color == D else color for color in row)


def compute(source):
    raw = source.read_bytes()
    assert sha256(raw).hexdigest() == SOURCE_SHA256, 'Frozen source hash differs'
    data = json.loads(raw)
    records, negatives = [], []
    counters = Counter()
    witness = None
    cyc = edge_set((i, (i + 1) % 5) for i in range(5))
    for key, entry in sorted(data['cells'].items(), key=lambda item: int(item[0])):
        n = 5 + entry['k_eff']
        vs, u = tuple(range(n)), n
        edges = cyc | edge_set(entry['edges'])
        h_vs = tuple(range(n + 1))
        h_edges = edges | {(v, u) for v in (0, 1, 2, 4)}
        h_abcb = fibre(h_vs, h_edges, {u: A, 2: B, 3: C, 4: B})
        h_abab = fibre(h_vs, h_edges, {u: A, 2: B, 3: A, 4: B})
        # x=0, y=1, a=2, b=3, c=4, z retains label 2.
        def quotient(v):
            return 2 if v == 4 else v
        t_vs = tuple(v for v in vs if v != 4)
        t_edges = edge_set((quotient(v), quotient(w)) for v, w in edges)
        t_all = fibre(t_vs, t_edges, {2: B, 0: C, 1: D})
        b_index = t_vs.index(3)
        subsets = {r: {t for t in t_all if t[b_index] == r} for r in (A, C, D)}
        assert t_all == set().union(*subsets.values())
        branches = {r: set() for r in (A, C, D)}
        for r, rows in subsets.items():
            for t in rows:
                col = dict(zip(t_vs, t))
                lifted = tuple(col[quotient(v)] for v in vs) + (A,)
                branches[r].add(cd_swap(lifted) if r == D else lifted)
        pull_abcb = branches[C] | branches[D]
        pull_abab = branches[A] | {cd_swap(row) for row in branches[A]}
        assert not branches[C] & branches[D]
        assert not branches[A] & {cd_swap(row) for row in branches[A]}
        assert h_abcb == pull_abcb, (key, 'ABCB full lift mismatch')
        assert h_abab == pull_abab, (key, 'ABAB full lift mismatch')
        assert len(h_abcb) == len(subsets[C]) + len(subsets[D])
        assert len(h_abab) == 2 * len(subsets[A])
        counters['graphs'] += 1
        counters['full_fibre_equalities'] += 2
        counters['ABCB_lifts'] += len(h_abcb)
        counters['ABAB_lifts'] += len(h_abab)
        counters['pinned_triangle_lifts'] += len(t_all)
        counters['empty_H_fibres'] += int(not h_abcb) + int(not h_abab)
        counters['empty_T_b_colour_fibres'] += sum(not subsets[r] for r in (A, C, D))
        # Fixed-triangle Kempe graph: each node is a complete colouring of the
        # same T; each allowed component avoids the three fixed vertices.
        moves = {t: list(kempe_moves(t_vs, t_edges, t, {0, 1, 2})) for t in sorted(t_all)}
        assert all(s in t_all for transitions in moves.values() for s, _ in transitions)
        terminal = subsets[C] | subsets[D]
        dist = {t: 0 for t in terminal}
        todo, prev = deque(sorted(terminal)), {}
        while todo:
            t = todo.popleft()
            for s, move in moves[t]:
                if s not in dist:
                    dist[s] = dist[t] + 1
                    prev[s] = (t, move)
                    todo.append(s)
        blocks, escapes, no_exit = 0, 0, 0
        for t in sorted(subsets[A]):
            ac = component(t_vs, t_edges, t, 3, (A, C))
            ad = component(t_vs, t_edges, t, 3, (A, D))
            direct = any(s[b_index] != A for s, _ in moves[t])
            assert direct == (0 not in ac or 1 not in ad), (key, 'exit criterion')
            counters['one_step_criterion_checks'] += 1
            if not direct:
                blocks += 1
                if t in dist:
                    escapes += 1
                    if int(key) == 823 and witness is None:
                        path, steps, cur = [t], [], t
                        while dist[cur]:
                            cur, move = prev[cur]
                            path.append(cur)
                            steps.append(move)
                        witness = {'source_mask': int(key), 'G_vertices': vs,
                                   'G_edges': sorted(edges), 'H_vertices': h_vs,
                                   'H_edges': sorted(h_edges), 'T_vertices': t_vs,
                                   'T_edges': sorted(t_edges),
                                   'roles': {'u': u, 'a': 2, 'b': 3, 'c': 4, 'x': 0, 'y': 1, 'z': 2},
                                   'colors': {'A': A, 'B': B, 'C': C, 'D': D},
                                   'start_AC_component_at_b': sorted(ac),
                                   'start_AD_component_at_b': sorted(ad),
                                   'path': path, 'steps': steps, 'distance': dist[t],
                                   'scope': 'Real near-triangulation control; inner degree>=5 is not assumed or certified.'}
                else:
                    no_exit += 1
        counters['one_step_blocked'] += blocks
        counters['blocked_one_step_but_escapes'] += escapes
        counters['no_exit_in_fixed_triangle_Kempe_class'] += no_exit
        common = adjacency(h_vs, h_edges)[2] & adjacency(h_vs, h_edges)[4]
        records.append({'source_mask': int(key), 'T_counts': [len(subsets[r]) for r in (A, C, D)],
                        'H_counts_ABAB_ABCB': [len(h_abab), len(h_abcb)],
                        'T_fibre_hashes': [digest(subsets[r]) for r in (A, C, D)],
                        'H_fibre_hashes': [digest(h_abab), digest(h_abcb)],
                        'H_common_neighbors_a_c': sorted(common),
                        'source_neartriangulation_edge_count': len(edges) == 3 * n - 8,
                        'one_step_blocked': blocks, 'blocked_but_escapes': escapes,
                        'no_exit_in_fixed_triangle_Kempe_class': no_exit,
                        'max_finite_exit_distance': max((dist[t] for t in subsets[A] if t in dist), default=None)})
        if int(key) == 1012:
            assert branches[C] and branches[D] and branches[A]
            assert branches[C] != h_abcb
            negatives.append({'name': 'omit_D_branch', 'source_mask': 1012,
                              'rejected': branches[C] != h_abcb,
                              'expected_lifts': len(h_abcb), 'malformed_lifts': len(branches[C])})
            raw_d = {cd_swap(t) for t in branches[D]}
            assert branches[C] | raw_d != h_abcb
            negatives.append({'name': 'omit_D_branch_color_swap', 'source_mask': 1012,
                              'rejected': branches[C] | raw_d != h_abcb,
                              'malformed_extra_lifts': len((branches[C] | raw_d) - h_abcb)})
            assert branches[A] != h_abab
            negatives.append({'name': 'omit_ABAB_second_orientation', 'source_mask': 1012,
                              'rejected': branches[A] != h_abab,
                              'expected_lifts': len(h_abab), 'malformed_lifts': len(branches[A])})
            assert common == {u, 3}
            assert len(edges) == 3 * n - 8 and len(t_edges) == 3 * len(t_vs) - 6
            for edge in sorted(t_edges):
                relaxed = fibre(t_vs, t_edges - {edge}, {2: B, 0: C, 1: D})
                if relaxed != t_all:
                    negatives.append({'name': 'delete_quotient_edge', 'source_mask': 1012,
                                      'deleted_edge': edge, 'rejected': True,
                                      'spurious_lifts': len(relaxed - t_all)})
                    break
            else:
                raise AssertionError('No quotient edge deletion negative control')
        if int(key) == 165:
            assert (2, 2) in t_edges and not t_all
            unlooped = fibre(t_vs, {e for e in t_edges if e[0] != e[1]}, {2: B, 0: C, 1: D})
            assert unlooped
            negatives.append({'name': 'erase_loop_from_illegal_ac_identification', 'source_mask': 165,
                              'rejected': unlooped != t_all, 'spurious_lifts': len(unlooped)})
    assert witness is not None and witness['distance'] == 2
    assert counters['graphs'] == 132 and counters['full_fibre_equalities'] == 264
    assert all(item['rejected'] for item in negatives)
    return {'source_file': 'artifacts/c5_cells/cells.json', 'source_sha256': SOURCE_SHA256,
            'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'T_color_order': ['A', 'C', 'D'], 'summary': dict(counters),
            'records': records, 'malformed_negative_controls': negatives,
            'one_step_counterexample': witness,
            'scope': '132 fixed catalogue graphs only; no source enumeration; no target 932/933/941 realization; no arbitrary-size exclusion.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE.parent / 'frozen/artifacts/c5_cells/cells.json')
    parser.add_argument('--output', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--check', action='store_true', help='Read-only JSON replay of an existing certificate')
    args = parser.parse_args()
    result = compute(args.input)
    # Normalize tuples to JSON arrays before in-memory comparison.
    result = json.loads(json.dumps(result))
    if args.check:
        assert json.loads(args.output.read_text()) == result, 'Certificate differs'
    else:
        with args.output.open('x') as handle:
            json.dump(result, handle, indent=2)
            handle.write('\n')
    print(json.dumps({'ok': True, 'mode': 'check' if args.check else 'exclusive-create',
                      'summary': result['summary'],
                      'malformed_negative_controls': len(result['malformed_negative_controls']),
                      'counterexample_source_mask': result['one_step_counterexample']['source_mask'],
                      'counterexample_distance': result['one_step_counterexample']['distance']}, indent=2))


if __name__ == '__main__':
    main()
