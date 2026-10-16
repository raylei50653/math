#!/usr/bin/env python3
"""Independent finite transition-parity calibration; no source assertion."""
import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

BASE = "e98a1cc1afd9a428600dcf4027d8138078c01650"


def components(vertices, edge_ids, edges):
    adj = {u: [] for u in vertices}
    for i in edge_ids:
        u, v = edges[i]
        adj[u].append(v)
        adj[v].append(u)
    unseen, out = set(vertices), []
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            u = todo.pop()
            if u in seen:
                continue
            seen.add(u)
            todo.extend(v for v in adj[u] if v not in seen)
        unseen -= seen
        out.append(sorted(seen))
    return out


def perfect_matchings(vertices, edges, rng):
    incident = defaultdict(list)
    for i, (u, v) in enumerate(edges):
        incident[u].append((v, i))
        incident[v].append((u, i))
    for a in incident.values():
        rng.shuffle(a)
    def visit(left, chosen):
        if not left:
            yield tuple(sorted(chosen))
            return
        u = min(left)
        for v, i in incident[u]:
            if v in left:
                yield from visit(left - {u, v}, chosen + [i])
    return sorted(set(visit(set(vertices), [])))


def colourings(vertices, edges, rng):
    adj = {u: set() for u in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    tie = {u: rng.random() for u in vertices}
    order = sorted(vertices, key=lambda u: (-len(adj[u]), tie[u]))
    chosen, out = {}, []
    def visit(k):
        if k == len(order):
            out.append([chosen[u] for u in vertices])
            return
        u = order[k]
        forbidden = {chosen[v] for v in adj[u] if v in chosen}
        for c in range(4):
            if c not in forbidden:
                chosen[u] = c
                visit(k + 1)
        chosen.pop(u, None)
    visit(0)
    return sorted(out)


def reconstruct(graph, rng):
    vertices = graph['J_vertices']
    edges = [tuple(uv) for uv in graph['J_edges']]
    faces = graph['J_faces']
    incident = defaultdict(list)
    for i, face in enumerate(faces):
        assert len(face) == 3
        for j in range(3):
            incident[tuple(sorted((face[j], face[(j + 1) % 3])))].append(i)
    assert set(incident) == set(edges)
    assert all(len(v) == 2 for v in incident.values())
    dedges = [tuple(sorted(incident[e])) for e in edges]
    dv, all_edges = list(range(len(faces))), set(range(len(edges)))
    assert all(sum(u in uv for uv in dedges) == 3 for u in dv)
    pms = perfect_matchings(dv, dedges, rng)
    full = colourings(vertices, edges, rng)
    vindex = {u: j for j, u in enumerate(vertices)}
    row_colours = [[c[vindex[u]] ^ c[vindex[v]] for u, v in edges] for c in full]
    fibres = defaultdict(list)
    for j, col in enumerate(row_colours):
        fibres[tuple(i for i, value in enumerate(col) if value == 1)].append(j)
    pm_rows = []
    for pm in pms:
        cs = components(dv, all_edges - set(pm), dedges)
        omega = sum(len(c) % 2 for c in cs)
        fibre = fibres[pm]
        assert bool(fibre) == (omega == 0)
        assert len(fibre) == (4 * 2 ** len(cs) if omega == 0 else 0)
        pm_rows.append({'matching': list(pm), 'complement_cycles': cs,
                        'oddness': omega, 'complete_fixed_alpha_colour_fibre': fibre})
    assert set(fibres) == set(pms)
    counts = defaultdict(int)
    traces = []
    marks = graph.get('marks')
    for base in pms:
        # All complete beta/gamma choices, once per root translation.
        for ci in fibres[base]:
            if full[ci][0] != 0:
                continue
            col = row_colours[ci]
            old = set(base)
            for endpoint in pms:
                delta = old ^ set(endpoint)
                used = {u for i in delta for u in dedges[i]}
                batches = [set(delta)] if delta else []
                batches += [{i for i in delta if dedges[i][0] in vs}
                            for vs in components(used, delta, dedges)]
                for batch in {tuple(sorted(b)) for b in batches}:
                    batch = set(batch)
                    a, b = old & batch, batch - old
                    b_at = {}
                    for i in b:
                        for u in dedges[i]:
                            assert u not in b_at
                            b_at[u] = i
                    transitions = {i for i in a if col[b_at[dedges[i][0]]] != col[b_at[dedges[i][1]]]}
                    assert len(transitions) % 2 == 0
                    switched = old ^ batch
                    assert tuple(sorted(switched)) in pms
                    cs = components(dv, all_edges - switched, dedges)
                    rows = []
                    for c in cs:
                        t = sorted(i for i in transitions if dedges[i][0] in c)
                        assert len(c) % 2 == len(t) % 2
                        if len(c) == 5:
                            assert len(t) <= 1
                        rows.append({'vertices': c, 'transitions': t})
                    omega = sum(len(c) % 2 for c in cs)
                    assert omega <= len(transitions)
                    counts[(len(transitions), omega)] += 1
                    if marks is not None:
                        e, f, g = marks
                        if {e, f, g} <= old and e in switched and g in switched and f not in switched:
                            traces.append({'colour_index': ci, 'even_111': list(base),
                                           'batch': sorted(batch), 'ordinary_101': sorted(switched),
                                           'transitions': sorted(transitions), 'new_complement': rows})
    if graph['name'] == 'four_connected_fj_locked_control':
        e, f, g = marks
        assert all((col[e] == col[f]) == (col[e] == col[g]) for col in row_colours)
        joint = [r for r in pm_rows if e in r['matching'] and
                 ((f in r['matching']) != (g in r['matching']))]
        assert len(joint) == 1 and joint[0]['oddness'] == 2
        wanted = (1, 3, 6, 10, 13, 16, 19, 21)
        first = [r for r in traces if tuple(r['even_111']) == wanted]
        second = [r for r in traces if tuple(r['even_111']) != wanted]
        assert len(first) == 4 and len(second) == 2
        assert all(len(r['transitions']) == 2 and
                   sorted(len(c['transitions']) for c in r['new_complement']) == [1, 1]
                   for r in first)
        assert all(len(r['transitions']) == 4 and
                   sorted(len(c['transitions']) for c in r['new_complement']) == [1, 3]
                   for r in second)
        pins = graph['pins']
        assert all(sum(u in uv for uv in edges) == 5 for u in (pins['m'], pins['z']))
    return {'name': graph['name'], 'source': 'not triggered', 'primal_edges': [list(e) for e in edges],
            'dual_edges': [list(e) for e in dedges], 'all_complete_J_colourings': full,
            'all_matching_rows': pm_rows, 'transition_oddness_histogram':
            [{'transitions': t, 'oddness': o, 'checks': n} for (t, o), n in sorted(counts.items())],
            'complete_111_to_101_transition_traces': traces}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = root / 'frozen/audits/2026-10-15-three-edge-matchings-6ddea32/graphs.json'
    control = Path(__file__).with_name('countercontrol.json')
    inputs = json.loads(source.read_text())
    inputs = [g for g in inputs if 'J_vertices' in g] + [json.loads(control.read_text())]
    rng = random.Random(args.seed)
    result = {'BASE': BASE, 'source_authority': 'not triggered; finite controls only',
              'input_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (source, control)},
              'controls': [reconstruct(g, rng) for g in inputs]}
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, sort_keys=True, indent=2)
            stream.write('\n')
    else:
        if json.loads(args.check.read_text()) != result:
            raise SystemExit('FAIL: candidate differs from complete independent reconstruction')
    print(json.dumps({'status': 'PASS', 'controls': [
        {'name': c['name'], 'PMs': len(c['all_matching_rows']),
         'colours': len(c['all_complete_J_colourings']),
         'transition_histogram': c['transition_oddness_histogram']} for c in result['controls']]}))


if __name__ == '__main__':
    main()
