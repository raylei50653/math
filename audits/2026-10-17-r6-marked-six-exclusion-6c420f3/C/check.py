#!/usr/bin/env python3
"""Reconstruct the frozen finite weak-premise control, never a source graph.

Stdlib only; no prior checker is imported. --write creates exclusively;
--check recomputes the entire certificate and rejects any difference.
"""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import random
import sys

BASE = '6c420f3ca77d60952ed76f93dff7449c522715ca'
ROOT = Path(__file__).resolve().parent.parent
CONTROL = 'audits/2026-10-16-r6-319-joint-parity-f1faf74/B/'
GRAPH_REL = CONTROL + 'input_graph.json'
PROOF_REL = CONTROL + 'PROOF.md'
GRAPH_SHA = 'c07c851ee37e1f327d19042a6216a085e546aa27dd72f67366083b1dab7b60ca'
PROOF_SHA = '20aaa426fdc83d087dc98587dce8608a33fd7fafa0c657d8be274168bce993f5'
AUTHORITY = 'not triggered; finite weak-premise control fails literal source layout'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def canonical_cycle(vertices):
    seq = tuple(vertices)
    choices = [seq[i:] + seq[:i] for i in range(len(seq))]
    rev = seq[::-1]
    choices += [rev[i:] + rev[:i] for i in range(len(seq))]
    return min(choices)


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    unseen = set(vertices)
    answer = []
    while unseen:
        todo = [min(unseen)]
        found = set()
        while todo:
            v = todo.pop()
            if v not in found:
                found.add(v)
                todo.extend(adj[v] - found)
        unseen -= found
        answer.append(sorted(found))
    return sorted(answer)


def read_inputs(input_path):
    manifest = json.loads((ROOT / 'INPUTS.json').read_text())
    require(manifest['base'] == BASE, 'wrong frozen BASE')
    for rel, wanted in ((GRAPH_REL, GRAPH_SHA), (PROOF_REL, PROOF_SHA)):
        entries = [e for e in manifest['entries'] if e['path'] == rel]
        require(len(entries) == 1, 'missing or duplicate frozen source ID')
        entry = entries[0]
        require(entry['frozen_path'] == 'frozen/' + rel, 'wrong frozen path')
        require(entry['sha256'] == wanted, 'wrong manifest source hash')
        require(hashlib.sha256((ROOT / entry['frozen_path']).read_bytes()).hexdigest()
                == wanted, 'frozen source bytes changed')
    data = input_path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == GRAPH_SHA, 'input graph hash mismatch')
    graph = json.loads(data)
    require(set(graph) == {'J_vertices', 'J_edges', 'J_faces',
                          'marked_original_edges', 'marks', 'name', 'source'},
            'unexpected input schema or inherited source pins')
    require(graph['name'] == 'all_distinct_and_marked_small_cuts_positive_oddness_control',
            'wrong graph identity')
    require(graph['source'] == 'not triggered: does not have the source two-face and hub-bridge layout',
            'wrong source authority')
    require(graph['marks'] == [0, 29, 6], 'wrong literal marking')
    require(graph['marked_original_edges'] == [[0, 2], [10, 11], [1, 9]],
            'wrong marked primal endpoints')
    return graph


def reconstruct(graph, seed):
    rng = random.Random(seed)
    vertices = graph['J_vertices']
    edges = [tuple(e) for e in graph['J_edges']]
    faces = [tuple(f) for f in graph['J_faces']]
    require(vertices == list(range(12)), 'wrong primal vertex labels')
    require(len(edges) == 30 and len(set(edges)) == 30, 'wrong primal edges')
    require(all(a < b and a in vertices and b in vertices for a, b in edges),
            'invalid primal edge')
    require(len(faces) == 20 and len({tuple(sorted(f)) for f in faces}) == 20,
            'wrong face list')
    edge_id = {e: i for i, e in enumerate(edges)}
    incidence = defaultdict(list)
    for fi, face in enumerate(faces):
        require(len(face) == len(set(face)) == 3, 'nontriangular face')
        for i in range(3):
            incidence[edge(face[i], face[(i + 1) % 3])].append(fi)
    require(set(incidence) == set(edges), 'face/edge mismatch')
    require(all(len(fs) == 2 for fs in incidence.values()), 'edge has wrong face count')
    require(len(vertices) - len(edges) + len(faces) == 2, 'wrong Euler characteristic')
    require(len(components(vertices, edges)) == 1, 'primal disconnected')

    # Orient the actual triangular face complex, fixing face 0. A consistent
    # orientation plus cyclic links and Euler 2 certifies this sphere map.
    def directed_edges(face):
        return [(face[i], face[(i + 1) % 3]) for i in range(3)]
    oriented = {0: faces[0]}
    queue = deque([0])
    while queue:
        fi = queue.popleft()
        for a, b in directed_edges(oriented[fi]):
            fj = next(f for f in incidence[edge(a, b)] if f != fi)
            candidate = faces[fj]
            if (a, b) in directed_edges(candidate):
                candidate = candidate[::-1]
            require((b, a) in directed_edges(candidate), 'face orientation failed')
            if fj in oriented:
                require(set(directed_edges(oriented[fj])) == set(directed_edges(candidate)),
                        'nonorientable face complex')
            else:
                oriented[fj] = candidate
                queue.append(fj)
    require(len(oriented) == len(faces), 'face adjacency disconnected')
    successor = {v: {} for v in vertices}
    for fi in range(len(faces)):
        face = oriented[fi]
        for i in range(3):
            v, a, b = face[i], face[(i + 1) % 3], face[(i + 2) % 3]
            require(a not in successor[v], 'repeated corner at primal vertex')
            successor[v][a] = b
    rotation = {}
    for v in vertices:
        adj = sorted(b if a == v else a for a, b in edges if v in (a, b))
        require(set(successor[v]) == set(adj), 'vertex link misses neighbour')
        seq = [min(adj)]
        while successor[v][seq[-1]] != seq[0]:
            nxt = successor[v][seq[-1]]
            require(nxt not in seq, 'disconnected vertex link')
            seq.append(nxt)
        require(sorted(seq) == adj, 'vertex link is not one circle')
        rotation[str(v)] = seq
    predecessor = {v: {b: a for a, b in successor[v].items()} for v in vertices}
    unused = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    replayed_faces = []
    while unused:
        first = min(unused)
        darts = []
        dart = first
        while not darts or dart != first:
            require(dart in unused, 'rotation face replay repeats a dart')
            unused.remove(dart)
            darts.append(dart)
            a, b = dart
            dart = (b, predecessor[b][a])
        replayed_faces.append(canonical_cycle([a for a, _ in darts]))
    require(sorted(replayed_faces) == sorted(canonical_cycle(f) for f in faces),
            'rotation does not replay the actual faces')

    # Preserve all twenty original face IDs and all thirty original edge IDs.
    dual = [tuple(sorted(incidence[e])) for e in edges]
    require(len(set(dual)) == len(dual), 'dual has parallel edges')
    dual_adj = defaultdict(list)
    for i, (a, b) in enumerate(dual):
        require(a != b, 'dual loop')
        dual_adj[a].append((i, b))
        dual_adj[b].append((i, a))
    require(len(components(range(20), dual)) == 1, 'dual disconnected')
    require(all(len(dual_adj[v]) == 3 for v in range(20)), 'dual not cubic')
    for options in dual_adj.values():
        rng.shuffle(options)
    pms = []
    def matching(left, chosen):
        if not left:
            pms.append(tuple(sorted(chosen)))
            return
        a = min(left)
        for i, b in dual_adj[a]:
            if b in left:
                matching(left - {a, b}, chosen + [i])
    matching(set(range(20)), [])
    pms.sort()
    require(len(pms) == len(set(pms)) == 38, 'wrong complete PM enumeration')

    def complement_cycles(pm):
        adj = {v: [] for v in range(20)}
        for i, (a, b) in enumerate(dual):
            if i not in pm:
                adj[a].append(b)
                adj[b].append(a)
        require(all(len(adj[v]) == 2 for v in adj), 'PM complement not 2-regular')
        remaining = set(range(20))
        cycles = []
        while remaining:
            start = min(remaining)
            seq = [start]
            previous, current = start, min(adj[start])
            while current != start:
                require(current not in seq, 'complement traversal repeats vertex')
                seq.append(current)
                nxt = next(v for v in adj[current] if v != previous)
                previous, current = current, nxt
            seq = canonical_cycle(seq)
            remaining -= set(seq)
            ids = [dual.index(edge(seq[i], seq[(i + 1) % len(seq)]))
                   for i in range(len(seq))]
            cycles.append({'vertices': list(seq), 'edges': ids, 'length': len(seq)})
        cycles.sort(key=lambda c: (c['length'], c['vertices']))
        require(sorted(i for c in cycles for i in c['edges'])
                == [i for i in range(30) if i not in pm], 'incomplete complement')
        return cycles

    rows = []
    ordinary = Counter({f'{b:03b}': 0 for b in range(8)})
    weights = Counter({f'{b:03b}': 0 for b in range(8)})
    e, f, g = graph['marks']
    for pm in pms:
        status = ''.join('1' if mark in pm else '0' for mark in (e, f, g))
        cycles = complement_cycles(pm)
        oddness = sum(c['length'] % 2 for c in cycles)
        rows.append({'matching': list(pm), 'status': status,
                     'complement_cycles': cycles, 'oddness': oddness})
        ordinary[status] += 1
        if oddness == 0:
            weights[status] += 2 ** len(cycles)
    joint = [r for r in rows if r['status'] in ('110', '101')]
    require(len(joint) == 3 and all(r['status'] == '101' for r in joint), 'wrong joint family')
    require(sorted([c['length'] for c in r['complement_cycles']] for r in joint)
            == [[5, 5, 10], [5, 15], [7, 13]], 'wrong whole complement lengths')
    require(all(r['oddness'] == 2 for r in joint), 'wrong joint oddness')

    # Exhaust every simple primal six-cycle by DFS; canonical rotation and
    # reversal remove only multiple traversals of the same actual cycle.
    primal_adj = {v: [] for v in vertices}
    for a, b in edges:
        primal_adj[a].append(b)
        primal_adj[b].append(a)
    for options in primal_adj.values():
        rng.shuffle(options)
    cycles6 = set()
    def extend(path):
        if len(path) == 6:
            if path[0] in primal_adj[path[-1]]:
                cycles6.add(canonical_cycle(path))
            return
        for v in primal_adj[path[-1]]:
            if v > path[0] and v not in path:
                extend(path + [v])
    for start in vertices:
        extend([start])
    marked_cycles = []
    for cycle in sorted(cycles6):
        ids = [edge_id[edge(cycle[i], cycle[(i + 1) % 6])] for i in range(6)]
        if not {e, f} <= set(ids):
            continue
        cs = components(range(20), [uv for i, uv in enumerate(dual) if i not in ids])
        require(len(cs) == 2, 'simple primal cycle did not separate into two dual sides')
        sides = []
        for vs in cs:
            vset = set(vs)
            inside = [i for i, uv in enumerate(dual) if set(uv) <= vset]
            boundary = [i for i, (a, b) in enumerate(dual) if (a in vset) != (b in vset)]
            require(sorted(boundary) == sorted(ids), 'cycle dual is not exact cut boundary')
            require(len(components(vs, [dual[i] for i in inside])) == 1, 'dual side disconnected')
            sides.append({'vertices': vs, 'edges': inside,
                          'V': len(vs), 'E': len(inside),
                          'contains_cycle': len(inside) >= len(vs)})
        marked_cycles.append({'primal_cycle': list(cycle), 'boundary': sorted(ids),
                              'sides': sides, 'cyclic': all(s['contains_cycle'] for s in sides)})
    require(len(marked_cycles) == 5, 'wrong marked simple six-cycle census')
    require(sum(row['cyclic'] for row in marked_cycles) == 2, 'wrong cyclic six-cut census')
    examples = {(0, 2, 11, 10, 5, 4): [(14, 18), (6, 6)],
                (0, 2, 11, 10, 9, 4): [(12, 15), (8, 9)]}
    for cycle, expected in examples.items():
        row = next(r for r in marked_cycles if tuple(r['primal_cycle']) == cycle)
        require(row['cyclic'] and sorted((s['V'], s['E']) for s in row['sides'])
                == sorted(expected), 'user example side sizes fail')
    # Literal source faces require m adjacent to both e endpoints; neither
    # endpoint of the actual g edge has even one such adjacency.
    absent = [{'candidate_m': m, 'actual_neighbours_among_e_endpoints':
               sorted(set(primal_adj[m]) & set(edges[e]))} for m in edges[g]]
    require(all(not r['actual_neighbours_among_e_endpoints'] for r in absent),
            'source-layout absence assertion failed')
    return {'schema': 'r6-marked-six-control-v1', 'base': BASE,
            'source_authority': AUTHORITY,
            'input': {'path': 'frozen/' + GRAPH_REL, 'sha256': GRAPH_SHA,
                      'prior_proof_sha256': PROOF_SHA},
            'marks': [{'name': name, 'edge_index': mark,
                       'primal_endpoints': list(edges[mark]),
                       'dual_endpoints': list(dual[mark])}
                      for name, mark in zip(('e', 'f', 'g'), (e, f, g))],
            'oriented_faces': [list(oriented[i]) for i in range(20)],
            'primal_rotation': rotation, 'dual_edges': [list(uv) for uv in dual],
            'all_matching_rows': rows, 'ordinary_counts': dict(sorted(ordinary.items())),
            'even_complement_weights': dict(sorted(weights.items())),
            'joint_matching_indices': [i for i, r in enumerate(rows) if r in joint],
            'joint_minimum_oddness': 2, 'all_simple_six_cycle_count': len(cycles6),
            'marked_simple_six_cycles': marked_cycles,
            'marked_cyclic_six_cut_count': 2,
            'literal_source_layout_absence': absent,
            'stopping_point': 'finite control excluded by new source restriction; joint positivity remains OPEN'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--check', nargs='?', const=str(Path(__file__).with_name('certificate.json')))
    action.add_argument('--write', nargs='?', const=str(Path(__file__).with_name('certificate.json')))
    parser.add_argument('--input', type=Path, default=ROOT / 'frozen' / GRAPH_REL)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    try:
        result = reconstruct(read_inputs(args.input), args.seed)
        payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
        if args.write:
            with Path(args.write).open('x') as output:
                output.write(payload)
        if args.check:
            require(json.loads(Path(args.check).read_text()) == result, 'certificate mismatch')
        print('PASS: 38 PMs; 3 joint101; omega=2; 5 marked six-cycles; 2 actual cyclic six-cuts; source not triggered')
    except (ValueError, KeyError, TypeError, StopIteration, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
