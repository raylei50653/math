#!/usr/bin/env python3
"""Source cut-interface collisions in the existing fixed closure; no new search."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_guard_repair import ROOT, SOURCE, blocks, repair_source, tail_guard
from c5_edge_choices import EdgeModel

BASE = ROOT / 'artifacts/c5_cells/guard_repair.json'
OUT = ROOT / 'artifacts/c5_cells/repair_interface.json'


def partition(vertices, edges, marks):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    return sorted(sorted(set(b) & marks) for b in nx.connected_components(g) if set(b) & marks)


def wiring(parts, edges):
    owner = {v: i for i, b in enumerate(parts) for v in b}
    g = nx.MultiGraph()
    g.add_nodes_from(range(len(parts)))
    g.add_edges_from((owner[u], owner[v]) for u, v in edges)
    return g, owner


def port_interface(model, c, audit):
    """Only source graphs: restrict retained partitions to marked ports."""
    cut = set(audit['cost']['cut_edges'])
    T = {v for v, color in enumerate(c) if color == 0} | set(audit['Bstar'])
    neighbors = set(model.adj[2])
    na = {v for v in neighbors if c[v] == 0}
    nb = {v for v in neighbors if c[v] == 1}
    added = [model.edges[e] for e in sorted(cut) if set(model.edges[e]) <= T]
    marks = {0} | na | nb | {v for edge in added for v in edge}
    retained = [(u, v) for e, (u, v) in enumerate(model.edges)
                if e not in cut and u in T and v in T]
    parts = partition(T, retained, marks)
    g, owner = wiring(parts, added)
    root = nx.node_connected_component(g, owner[0])
    root_marks = sorted(v for v in marks if owner[v] in root)
    assert root_marks == sorted(marks & set(audit['Sstar']))
    obstruction = sorted((na - set(root_marks)) | (nb & set(root_marks)))
    assert obstruction == audit['neighbors2_in_Wstar']
    dual = []
    for chart in audit['cost']['charts'][1:]:
        ports = {v for e in cut for v in model.dual.ends[e]}
        parts_d = sorted(sorted(set(b) & ports) for b in chart['before']['blocks']
                         if set(b) & ports)
        assert chart['before']['blocks'] == chart['after']['blocks']
        counts, full_counts, edge_counts = [], [], []
        for side in ('before', 'after'):
            q = chart[side]
            edges = [model.dual.ends[e] for _, _, e in q['edges']]
            gd, _ = wiring(parts_d, edges)
            counts.append(nx.number_connected_components(gd))
            full = nx.MultiGraph()
            full.add_nodes_from(range(len(q['blocks'])))
            full.add_edges_from((u, v) for u, v, _ in q['edges'])
            full_counts.append(nx.number_connected_components(full))
            edge_counts.append(len(q['edges']))
        assert counts[1] - counts[0] == full_counts[1] - full_counts[0]
        dual.append(dict(types=chart['types'], port_partition=parts_d,
                         port_kappa=counts, full_kappa=full_counts,
                         edge_counts=edge_counts,
                         omitted_owners=len(chart['before']['blocks']) - len(parts_d)))
    assert sum(d['edge_counts'][1] - d['edge_counts'][0] for d in dual) == 0
    delta = sum(d['port_kappa'][1] - d['port_kappa'][0] for d in dual)
    assert delta == sum(audit['cost']['predicted_delta'])
    return dict(primal_marks=sorted(marks), primal_partition=parts,
                primal_added_edges=added, root_marks=root_marks,
                neighbors_A=sorted(na), neighbors_B=sorted(nb),
                obstruction=obstruction, dual=dual, delta_chi=delta)


def report():
    base = json.loads(BASE.read_text())
    for p, digest in base['hashes'].items():
        assert sha256((ROOT / p).read_bytes()).hexdigest() == digest, p
    source = json.loads(SOURCE.read_text())
    model = EdgeModel(source['graph'])
    orbits = defaultdict(list)
    for sid, raw in enumerate(source['states']):
        a, d, c, aa, b = raw[:5]
        if a != aa or len({a, b, c, d}) != 4:
            continue
        roles = {a: 0, b: 1, c: 2, d: 3}
        orbits[tuple(roles[x] for x in raw)].append(sid)
    assert set(map(len, orbits.values())) == {24}
    rows, groups = [], defaultdict(list)
    for c, ids in sorted(orbits.items(), key=lambda item: item[1][0]):
        model.validate(c)
        audit = repair_source(model, c)
        if audit['trace'] != [2, 4]:
            continue
        signature = dict(Q=audit['Q'], local_colors=[[v, c[v]] for v in
                         sorted(set(range(5)) | set(model.adj[2]))],
                         typed_cut=[[e, c[model.edges[e][0]] ^ c[model.edges[e][1]]]
                                    for e in audit['cost']['cut_edges']])
        interface = port_interface(model, c, audit)
        move = next(a for a in model.actions(c) if a.pair == (1, 2) and 2 in a.component)
        target = model.apply(c, move)
        actual = tail_guard(model, target)
        assert actual['first_component'] == audit['Sstar']
        assert actual['predicted_AC_vertices'] == audit['Wstar']
        assert actual['predicted_AC_components'] == audit['Wstar_components']
        cycles = [[sum(not ts for ts, _ in sys) for sys in model.dual.systems(z)]
                  for z in (c, target)]
        assert [b - a for a, b in zip(*cycles)] == audit['cost']['predicted_delta']
        if not interface['obstruction']:
            assert actual['separated']
        row = dict(source=ids[0], source_ids=ids, role_coloring=c,
                   original_guard=tail_guard(model, c)['separated'],
                   repaired_guard=actual['separated'], isolated=not interface['obstruction'],
                   delta_chi=sum(cycles[1]) - sum(cycles[0]),
                   signature=signature, interface=interface, source_audit=audit)
        rows.append(row)
        groups[json.dumps(signature, sort_keys=True)].append(row)
    collisions = []
    for rs in groups.values():
        failed = [r for r in rs if not r['original_guard']]
        if len({(r['repaired_guard'], r['isolated'], r['delta_chi']) for r in failed}) > 1:
            collisions.append([r['source'] for r in failed])
    by_id = {r['source']: r for r in rows}
    left, right = by_id[7], by_id[17]
    assert left['signature'] == right['signature']
    assert not left['original_guard'] and not right['original_guard']
    assert left['repaired_guard'] and right['repaired_guard']
    assert (left['isolated'], left['delta_chi']) == (True, -1)
    assert (right['isolated'], right['delta_chi']) == (False, 1)
    differences = [v for v, (a, b) in enumerate(zip(left['role_coloring'], right['role_coloring'])) if a != b]
    assert differences == [8]
    assert 8 not in left['signature']['Q'] and 8 not in model.adj[2]
    singleton = next(a for a in model.actions(tuple(left['role_coloring']))
                     if a.pair == (1, 2) and a.component == (8,))
    assert model.apply(tuple(left['role_coloring']), singleton) == tuple(right['role_coloring'])
    assert 8 not in {v for e, _ in left['signature']['typed_cut'] for v in model.edges[e]}
    assert 8 in left['source_audit']['Bstar'] and 8 not in right['source_audit']['Bstar']
    assert 8 in model.adj[0] and 14 in model.adj[8]
    # The safe member is exactly the previously certified B2 failure orbit.
    prepared_failures = {tuple(o['role_coloring']) for o in base['color_orbits']
                         if not tail_guard(model, tuple(o['role_coloring']))['separated']}
    assert tuple(left['role_coloring']) in prepared_failures
    summary = dict(boundary_sources=sum(map(len, orbits.values())), color_orbits=len(orbits),
                   trace_orbits=len(rows), original_failed_orbits=sum(not r['original_guard'] for r in rows),
                   signature_classes=len(groups), failed_collision_classes=len(collisions),
                   repaired_guard_orbits=sum(r['repaired_guard'] for r in rows),
                   safe_repair_orbits=sum(r['repaired_guard'] and r['delta_chi'] <= 0 for r in rows))
    files = {BASE, Path(__file__).resolve(), *(ROOT / p for p in base['hashes'])}
    return dict(trust='Fixed existing closure; paper compression lemmas not Lean; no common mechanism theorem.',
                summary=summary, rows=rows, failed_collisions=collisions, primary_witness=[7, 17], witness_toggle=dict(vertex=8, pair=[1, 2], primal_path=[0, 8, 14]),
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
