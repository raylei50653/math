#!/usr/bin/env python3
"""Fresh fixed-fixture controls. Imports no historical checker or theorem code."""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import sys

AUDIT = Path(__file__).resolve().parents[1]
ORIGINAL = AUDIT.parent / '2026-10-11-br-sd-1g-dbdc4c35/agents/controls/certificate.normal.json'
COL = set(range(4))

def require(value, message):
    if not value:
        raise ValueError(message)

def graph(vertices, edges):
    require(len(vertices) == len(set(vertices)), 'duplicate vertex')
    adj = {v: set() for v in vertices}
    for a, b in edges:
        require(a != b and a in adj and b in adj and b not in adj[a], 'invalid edge')
        adj[a].add(b)
        adj[b].add(a)
    return adj

def coloring(vertices, edges, domains):
    adj = graph(vertices, edges)
    answer = []
    assigned = {}
    def visit():
        if len(assigned) == len(vertices):
            answer.append(tuple(assigned[v] for v in vertices))
            return
        candidates = {v: set(domains[v]) - {assigned[w] for w in adj[v] if w in assigned}
                      for v in vertices if v not in assigned}
        v = min(candidates, key=lambda w: (len(candidates[w]), -len(adj[w]), w))
        for c in sorted(candidates[v]):
            assigned[v] = c
            visit()
            del assigned[v]
    visit()
    return sorted(answer)

def blocks(vertices, edges):
    """Union fundamental-cycle edges in a BFS spanning tree (not Tarjan)."""
    adj = graph(vertices, edges)
    normalized = sorted(tuple(sorted(e)) for e in edges)
    leader = {e: e for e in normalized}
    def find(e):
        while leader[e] != e:
            leader[e] = leader[leader[e]]
            e = leader[e]
        return e
    def union(a, b):
        leader[find(a)] = find(b)
    parent = {}
    tree_edges = set()
    for start in vertices:
        if start in parent:
            continue
        parent[start] = None
        todo = deque([start])
        while todo:
            v = todo.popleft()
            for w in sorted(adj[v]):
                if w not in parent:
                    parent[w] = v
                    tree_edges.add(tuple(sorted((v, w))))
                    todo.append(w)
    for e in normalized:
        if e in tree_edges:
            continue
        a, b = e
        ancestors = set()
        v = a
        while v is not None:
            ancestors.add(v)
            v = parent[v]
        v, tail = b, []
        while v not in ancestors:
            tail.append(tuple(sorted((v, parent[v]))))
            v = parent[v]
        lca = v
        v = a
        while v != lca:
            tail.append(tuple(sorted((v, parent[v]))))
            v = parent[v]
        for f in tail:
            union(e, f)
    result = {}
    for e in normalized:
        result.setdefault(find(e), []).append(e)
    return sorted(tuple(sorted(es)) for es in result.values())

def incidence(vertices, bs):
    nodes = [('v', v) for v in vertices] + [('b', str(i)) for i in range(len(bs))]
    edges = [(('v', v), ('b', str(i))) for i, es in enumerate(bs) for v in sorted({x for e in es for x in e})]
    adj = graph(nodes, edges)
    seen, todo = set(), [nodes[0]]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(adj[v] - seen)
    require(len(seen) == len(nodes) and len(edges) == len(nodes) - 1, 'all-vertex incidence not a tree')
    return {'nodes': len(nodes), 'edges': len(edges), 'status': 'triggered and holds'}

def palette_count(vertices, bs, lists):
    bvertices = [set(x for e in es for x in e) for es in bs]
    choices = []
    for es, vs in zip(bs, bvertices):
        n = len(vs)
        if len(es) == n * (n - 1) // 2:
            k = n - 1
        else:
            deg = graph(sorted(vs), es)
            require(n % 2 == 1 and len(es) == n and all(len(deg[v]) == 2 for v in vs), 'non-Gallai fixed block')
            k = 2
        allowed = set.intersection(*(set(lists[v]) for v in vs))
        choices.append([set(p) for p in itertools.combinations(sorted(allowed), k)])
    incident = {v: [i for i, vs in enumerate(bvertices) if v in vs] for v in vertices}
    order = sorted(range(len(bs)), key=lambda i: len(choices[i]))
    current, count = {}, 0
    def visit(j):
        nonlocal count
        if j == len(order):
            if all(set(lists[v]) == set().union(*(current[i] for i in incident[v])) for v in vertices):
                count += 1
            return
        i = order[j]
        for p in choices[i]:
            if all(p.isdisjoint(current[k]) for v in bvertices[i] for k in incident[v] if k in current):
                current[i] = p
                visit(j + 1)
                del current[i]
    visit(0)
    return count

def beta_lifts(vertices, edges, beta):
    return coloring(vertices, edges, {v: {beta[v]} if v in beta else COL for v in vertices})

def check_certificate(data):
    require(data['actual_target_source_count'] == 0 and data['actual_target_source_status'] == 'not triggered', 'source label drift')
    rows = []
    for f in data['source_like_fixtures']:
        cv, ce = f['C']['vertex_order'], f['C']['all_edges']
        mv, me, ge = f['M_G_vertex_order'], f['all_M_edges'], f['all_G_edges']
        beta = f['literal_beta']
        ca, ma = graph(cv, ce), graph(mv, me)
        p, q = f['ordered_s_contacts']
        attachments = {v: sorted(ma[v] & set(beta)) for v in cv}
        require(attachments == f['all_boundary_attachments'], 'attachment identity')
        lists = {v: sorted(COL - {beta[b] for b in attachments[v]} - ({3} if v in (p, q) else set())) for v in cv}
        require(lists == f['all_LD_lists'], 'complete original lists')
        require(all(len(ma[v]) == 4 and len(ca[v]) + len(attachments[v]) + int(v in (p, q)) == 4 for v in cv), 'degree equation')
        require(all(len(lists[v]) >= len(ca[v]) for v in cv), 'degree-list lower bound')
        ct = coloring(cv, ce, lists)
        mt = beta_lifts(mv, me, beta)
        gt = beta_lifts(mv, ge, beta)
        for actual, key in [(ct, 'complete_C_LD_coloring_tuples'), (mt, 'complete_M_beta_lift_tuples'), (gt, 'complete_G_beta_lift_tuples')]:
            require([list(t) for t in actual] == f[key], 'full tuple mismatch: ' + key)
        joined = sorted(tuple((beta | {'s': 3} | dict(zip(cv, t)))[v] for v in mv) for t in ct)
        require(joined == mt, 'complete extension equivalence')
        expected_pins = [list(t) for t in itertools.product(range(4), repeat=2)]
        fibres = f['all_16_ordered_pq_fibres_including_empty']
        require([g['ordered_pq_tuple'] for g in fibres] == expected_pins, 'missing ambient fibre')
        empty = 0
        for g in fibres:
            pin = tuple(g['ordered_pq_tuple'])
            for tuples, order, key in [(ct, cv, 'complete_C_tuples'), (mt, mv, 'complete_M_tuples'), (gt, mv, 'complete_G_tuples')]:
                exact = [list(t) for t in tuples if (t[order.index(p)], t[order.index(q)]) == pin]
                require(exact == g[key], 'incomplete fibre: ' + key)
            empty += not g['complete_M_tuples']
        bs = blocks(cv, ce)
        require(bs == sorted(tuple(sorted(tuple(sorted(e)) for e in b['all_edges'])) for b in f['C']['blocks'].values()), 'maximal block reconstruction')
        tree = incidence(cv, bs)
        pc = palette_count(cv, bs, lists)
        require(pc == 0, 'unexpected compatible palettes')
        require(mt and not f['M_rejects_literal_beta'] and not f['M_beta_inclusion_minimal'], 'synthetic rejection label')
        rows.append({'name': f['name'], 'C_M_G_lift_counts': [len(ct), len(mt), len(gt)], 'empty_M_fibres': empty,
                     'compatible_palette_count': pc, 'incidence': tree, 'status': 'triggered and holds',
                     'actual_source_status': 'not triggered'})
    require(len(rows) == 6, 'fixture count')
    return rows

def extra_controls(data):
    f = data['source_like_fixtures'][0]
    vertices = f['M_G_vertex_order'] + ['ignored-z', 'free-f']
    edges = f['all_M_edges'] + [['ignored-z', 'B0'], ['ignored-z', 'B2']]
    beta = f['literal_beta']
    actual = beta_lifts(vertices, edges, beta)
    old = [tuple(t) for t in f['complete_M_beta_lift_tuples']]
    factors = [(z, c) for z in sorted(COL - {beta['B0'], beta['B2']}) for c in sorted(COL)]
    require(actual == sorted(t + factor for t in old for factor in factors), 'ignored full-lift factor lost')
    factor_control = {'status': 'triggered and holds', 'scope': 'one extended synthetic fixture',
                      'ignored_B_only_neighbors': ['B0', 'B2'], 'ignored_allowed_colors': [1, 2, 3],
                      'free_allowed_colors': [0, 1, 2, 3], 'factor': len(factors), 'full_lifts': [list(t) for t in actual],
                      'projection_bijective': False, 'actual_source_status': 'not triggered'}
    mechanics = []
    for name, n in [('triangle', 3), ('odd-cycle-5', 5), ('K4', 4)]:
        vs = ['q'] + [f'v{i}' for i in range(1, n)]
        es = [[vs[i], vs[(i + 1) % n]] for i in range(n)] if n != 4 else [list(e) for e in itertools.combinations(vs, 2)]
        palette = {0, 1, 2} if n == 4 else {0, 2}
        allv, alle = list(vs), list(es)
        for v in vs[1:]:
            allv.append('leaf-' + v)
            alle.append([v, 'leaf-' + v])
        bs = blocks(allv, alle)
        tree = incidence(allv, bs)
        require(2 in palette and 3 not in palette, 'exclusive starting palette')
        mechanics.append({'name': name, 'palette': sorted(palette), 'next_bridge_palette': [3], 'incidence': tree,
                          'first_step': 'triggered and holds', 'leaf_missing_T': True,
                          'scope': 'local palette/walk mechanics; global S universality absent', 'actual_source_status': 'not triggered'})
    neg = data['negative_controls']['cutpoint_and_W1_D_routing']
    require(3 in neg['all_lists']['x1'] and 3 not in neg['all_block_palettes']['J1'], 'old invalid implication counterexample lost')
    # A path with bad degree lists can escape to r if the J2 two-color barrier is absent.
    ev, ee = ['q', 'x', 'r'], [['q', 'x'], ['x', 'r']]
    el = {'q': [2], 'x': [2, 3], 'r': [3]}
    require(coloring(ev, ee, el) == [], 'barrier-omission local bad assignment')
    # A second s-contact defeats the S-minus-q universal D premise at the terminal vertex.
    require(coloring(['q', 'y'], [['q', 'y']], {'q': [2], 'y': [2]}) == [], 'extra-contact negative')
    return {'ignored_coordinate_factor': factor_control, 'bridge_triangle_oddcycle_K4_walk_mechanics': mechanics,
            'invalid_x1_implication': {'status': 'counterexample', 'actual_source_status': 'not triggered'},
            'barrier_omission': {'status': 'counterexample', 'edges': ee, 'lists': el, 'palettes': [[2], [3]],
                                 'scope': 'shows J2 barrier necessary for this walk argument; no original source'},
            'extra_s_contact': {'status': 'counterexample', 'scope': 'local bad assignment with universal D premise absent; no original source'}}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate', type=Path, default=ORIGINAL)
    p.add_argument('--write', type=Path)
    p.add_argument('--check', type=Path)
    a = p.parse_args()
    data = json.loads(a.certificate.read_text())
    rows = check_certificate(data)
    out = {'schema': 'br-sd-1g-adopt-finite-v1', 'status': 'triggered and holds',
           'scope': 'six named synthetic fixtures plus named finite mechanism/factor controls',
           'source_certificate_sha256': hashlib.sha256(a.certificate.read_bytes()).hexdigest(),
           'rows': rows, 'extra_controls': extra_controls(data), 'actual_source_status': 'not triggered',
           'new_Lean_theorem': False, 'unbounded_theorem_proved_by_controls': False}
    encoded = (json.dumps(out, sort_keys=True, indent=2) + '\n').encode()
    if a.write:
        with a.write.open('xb') as stream:
            stream.write(encoded)
    if a.check:
        require(a.check.read_bytes() == encoded, 'new control certificate mismatch')
    print(json.dumps({'status': out['status'], 'scope': out['scope'], 'sha256': hashlib.sha256(encoded).hexdigest(),
                      'C_M_counts': [r['C_M_G_lift_counts'][:2] for r in rows], 'ignored_factor': 12,
                      'actual_source_status': 'not triggered'}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        print('FAIL: ' + repr(exc), file=sys.stderr)
        raise SystemExit(1)
