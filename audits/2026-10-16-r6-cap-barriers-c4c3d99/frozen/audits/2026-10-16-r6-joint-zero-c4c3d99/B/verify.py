#!/usr/bin/env python3
"""Independent complete finite checks of B1/B3; no source claims."""
import argparse
from collections import deque
from itertools import combinations
import hashlib
import json
from pathlib import Path


def edge(u, v):
    return tuple(sorted((u, v)))


def components(vertices, edges):
    adj = {u: [] for u in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    result, unseen = [], set(vertices)
    while unseen:
        start = min(unseen)
        comp, todo = set(), [start]
        unseen.remove(start)
        while todo:
            u = todo.pop()
            comp.add(u)
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    todo.append(v)
        result.append(comp)
    return result


def perfect_matchings(vertices, edges):
    adj = {u: [] for u in vertices}
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    def visit(left, selected):
        if not left:
            yield frozenset(selected)
            return
        u = min(left)
        for v, i in adj[u]:
            if v in left:
                yield from visit(left - {u, v}, selected + [i])
    return list(visit(set(vertices), []))


def oddness(vertices, edges, matching):
    comps = components(vertices, [uv for i, uv in enumerate(edges) if i not in matching])
    return sum(len(c) % 2 for c in comps), comps


def bit_assignment(vertices, edges, wanted):
    adj = {u: [] for u in vertices}
    for (u, v), bit in zip(edges, wanted):
        adj[u].append((v, bit))
        adj[v].append((u, bit))
    bits = {}
    for root in vertices:
        if root in bits:
            continue
        bits[root] = 0
        todo = deque([root])
        while todo:
            u = todo.popleft()
            for v, bit in adj[u]:
                value = bits[u] ^ bit
                if v in bits:
                    if bits[v] != value:
                        return None
                else:
                    bits[v] = value
                    todo.append(v)
    return bits


def full_colourings(vertices, edges):
    adj = {u: [] for u in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    order = sorted(vertices, key=lambda u: (-len(adj[u]), u))
    colours, result = {}, []
    def visit(i):
        if i == len(order):
            result.append(dict(colours))
            return
        u = order[i]
        forbidden = {colours[v] for v in adj[u] if v in colours}
        for c in range(4):
            if c not in forbidden:
                colours[u] = c
                visit(i + 1)
        colours.pop(u, None)
    visit(0)
    return result


def joint_connectivity(vertices, edges, pms, marks):
    e, f, g = marks
    family = [m for m in pms if e in m and ((f in m) != (g in m))]
    traces = []
    for left in family:
        for right in family:
            difference = left ^ right
            used = {v for i in difference for v in edges[i]}
            cs = components(used, [edges[i] for i in difference])
            batches = [set(i for i in difference if edges[i][0] in c) for c in cs]
            marked = [b for b in batches if f in b or g in b]
            if len(marked) == 2:
                batches = [b for b in batches if b not in marked] + [marked[0] | marked[1]]
            current, trace = left, []
            for batch in batches:
                assert e not in batch
                assert len(batch & {f, g}) in (0, 2)
                current = current ^ batch
                assert current in family
                trace.append(sorted(current))
            assert current == right
            traces.append({'from': sorted(left), 'to': sorted(right), 'path': trace})
    return family, traces


def planar_control(graph):
    vertices = graph['J_vertices']
    jedges = [tuple(e) for e in graph['J_edges']]
    faces = graph['J_faces']
    incident = {e: [] for e in jedges}
    for i, face in enumerate(faces):
        for j in range(3):
            incident[edge(face[j], face[(j + 1) % 3])].append(i)
    assert all(len(fs) == 2 for fs in incident.values())
    dedges = [tuple(incident[e]) for e in jedges]
    dv = list(range(len(faces)))
    marks = [jedges.index(tuple(e)) for e in graph['marked_original_edges']]
    pms = perfect_matchings(dv, dedges)
    colours = full_colourings(vertices, jedges)
    family, traces = joint_connectivity(dv, dedges, pms, marks)
    rows = []
    for pm in pms:
        omega, cs = oddness(dv, dedges, pm)
        bits = bit_assignment(vertices, jedges, [int(i not in pm) for i in range(len(jedges))])
        assert bits is not None
        mono_edges = [e for i, e in enumerate(jedges) if i in pm]
        assert mono_edges == [e for e in jedges if bits[e[0]] == bits[e[1]]]
        mono_comps = components(vertices, mono_edges)
        assert len(mono_comps) == len(cs) + 1
        bipartite = bit_assignment(vertices, mono_edges, [1] * len(mono_edges)) is not None
        assert bipartite == (omega == 0)
        fibre = [c for c in colours if all((c[u] >> 1) == bits[u] for u in vertices)]
        assert len(fibre) == (2 ** len(mono_comps) if bipartite else 0)
        pins = graph['pins']
        if pm in family:
            b = {name: bits[v] for name, v in pins.items()}
            e, f, g = marks
            if f in pm:
                assert b['m'] == b['p'] == b['q']
                assert b['z'] == b['v'] == b['w'] != b['m']
            else:
                assert g in pm and b['m'] == b['z'] != b['v'] == b['w']
                assert b['p'] != b['q']
        rows.append({'matching': sorted(pm), 'oddness': omega,
                     'complement_cycles': [sorted(c) for c in cs],
                     'bits': bits, 'monochromatic_components': [sorted(c) for c in mono_comps],
                     'bipartite': bipartite, 'full_colour_fibre': fibre})
    return {'name': graph['name'], 'source': 'not triggered',
            'matching_count': len(pms), 'joint_family_count': len(family),
            'joint_minimum': min((oddness(dv, dedges, m)[0] for m in family), default=None),
            'empty_fibres': sum(not r['full_colour_fibre'] for r in rows),
            'full_colour_count': len(colours), 'rows': rows, 'paths': traces}


def petersen_control(graph):
    vertices, edges = list(range(graph['Q_n'])), graph['Q_edges']
    pms = perfect_matchings(vertices, edges)
    # Pick the first literal disjoint marking with a nonempty joint family.
    for marks in combinations(range(len(edges)), 3):
        if len({v for i in marks for v in edges[i]}) != 6:
            continue
        family, traces = joint_connectivity(vertices, edges, pms, marks)
        if family:
            break
    assert family
    values = [oddness(vertices, edges, m)[0] for m in family]
    assert min(values) == 2
    return {'name': 'Petersen_positive_joint_minimum', 'source': 'not triggered; nonplanar',
            'edges': edges, 'marks': marks, 'matching_count': len(pms),
            'joint_family': [sorted(m) for m in family], 'joint_minimum': min(values),
            'paths': traces}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    inputs = base / 'frozen/audits/2026-10-15-three-edge-matchings-6ddea32/graphs.json'
    data = json.loads(inputs.read_text())
    controls = [planar_control(g) if 'J_vertices' in g else petersen_control(g) for g in data]
    certificate = {'input_sha256': hashlib.sha256(inputs.read_bytes()).hexdigest(),
                   'controls': controls, 'paper_theorems_verified_by': 'B/PROOF.md',
                   'finite_scope': 'all PMs, all complete colourings, all ordered joint pairs of literal controls'}
    if args.check is not None:
        # Reconstruct everything before reading the candidate; JSON normalization
        # handles integer vertex keys without accepting missing or altered rows.
        expected = json.loads(json.dumps(certificate))
        actual = json.loads(args.check.read_text())
        if actual != expected:
            raise SystemExit('FAIL: candidate differs from complete independent reconstruction')
    else:
        with args.output.open('x') as f:
            json.dump(certificate, f, indent=2, sort_keys=True)
            f.write('\n')
    print(json.dumps({'status': 'PASS', 'controls': [
        {k: c[k] for k in ('name', 'source', 'matching_count', 'joint_minimum')}
        for c in controls]}, sort_keys=True))


if __name__ == '__main__':
    main()
