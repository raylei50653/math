#!/usr/bin/env python3
"""Plateau exits and cut cycle accounting on the certified fixed Kempe closure."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_cut_interfaces import check_transition

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
OUT = ROOT / 'artifacts/c5_cells/strategy_barriers.json'


def induced(source, keep):
    graph = nx.Graph()
    graph.add_nodes_from(i for i in range(len(source['states'])) if keep(i))
    graph.add_edges_from((i, e['target']) for i in list(graph)
                        for e in source['transitions'][i]
                        if e['boundary_roots'] and e['target'] in graph)
    return graph


def path_events(source, path):
    return [dict(source=s, **next(e for e in source['transitions'][s]
                if e['target'] == t and e['boundary_roots'])) for s, t in zip(path, path[1:])]


def quotient(model, retained, added):
    """Contract retained components, keeping loops, parallel edges and isolates."""
    h = nx.MultiGraph()
    h.add_nodes_from(range(model.dual.f + 5))
    h.add_edges_from((*model.dual.ends[e], {'edge': e}) for e in retained)
    blocks = sorted(map(sorted, nx.connected_components(h)))
    owner = {v: i for i, block in enumerate(blocks) for v in block}
    q = nx.MultiGraph()
    q.add_nodes_from(range(len(blocks)))
    qedges = [(owner[model.dual.ends[e][0]], owner[model.dual.ends[e][1]], e) for e in added]
    q.add_edges_from((u, v, {'edge': e}) for u, v, e in qedges)
    nullity = q.number_of_edges() - q.number_of_nodes() + nx.number_connected_components(q)
    beta_h = h.number_of_edges() - h.number_of_nodes() + len(blocks)
    return dict(blocks=blocks, edges=qedges, retained_nullity=beta_h,
                quotient_nullity=nullity, cycles=beta_h + nullity)


def cut_audit(source, model, event, detailed=False):
    s, t = event['source'], event['target']
    c, d = tuple(source['states'][s]), tuple(source['states'][t])
    action = Move(tuple(event['pair']), tuple(event['component']))
    assert model.apply(c, action) == d
    block = set(action.component)
    cut = [e for e, (u, v) in enumerate(model.edges) if (u in block) != (v in block)]
    old = [c[u] ^ c[v] for u, v in model.edges]
    new = [d[u] ^ d[v] for u, v in model.edges]
    systems = []
    for i, types in enumerate(TYPE_PAIRS):
        retained = [e for e, typ in enumerate(old) if typ in types and e not in cut]
        assert retained == [e for e, typ in enumerate(new) if typ in types and e not in cut]
        before = quotient(model, retained, [e for e in cut if old[e] in types])
        after = quotient(model, retained, [e for e in cut if new[e] in types])
        assert before['blocks'] == after['blocks']
        assert before['cycles'] == source['cycle_vectors'][s][i]
        assert after['cycles'] == source['cycle_vectors'][t][i]
        delta = after['quotient_nullity'] - before['quotient_nullity']
        assert delta == after['cycles'] - before['cycles']
        row = dict(types=types, retained_cycles=before['retained_nullity'],
                   restored_old=before['quotient_nullity'], closed_new=after['quotient_nullity'],
                   delta=delta)
        if detailed:
            row.update(retained_edges=retained, before=before, after=after)
        systems.append(row)
    assert sum(r['delta'] for r in systems) == source['chi'][t] - source['chi'][s]
    answer = dict(**event, cut_edges=cut, systems=systems)
    if detailed:
        answer['interfaces'] = check_transition(model, c, action)
        answer['edge_replay'] = model.edge_replay(c, action)
    return answer


def plateau(source, start, k):
    chi, goals = source['chi'], set(source['goals'])
    low = induced(source, lambda i: chi[i] <= k)
    basin = set(nx.node_connected_component(low, start))
    assert not basin & goals and {chi[i] for i in basin} == {k}
    exits = [dict(source=s, **e) for s in sorted(basin) for e in source['transitions'][s]
             if e['boundary_roots'] and e['target'] not in basin]
    assert all(chi[e['target']] > k for e in exits)
    outside = induced(source, lambda i: chi[i] <= k + 1 and i not in basin)
    # Multi-source BFS entirely outside the plateau; suffix never returns.
    dist, successor = {}, {}
    queue = deque(sorted(goals & set(outside)))
    for g in queue:
        dist[g] = 0
    while queue:
        t = queue.popleft()
        for s in sorted(outside[t]):
            if s not in dist:
                dist[s], successor[s] = dist[t] + 1, t
                queue.append(s)
    good = [e for e in exits if e['target'] in dist]
    assert good and all(e in good for e in exits if chi[e['target']] == k + 1)
    choices = {}
    for e in good:
        choices.setdefault(e['source'], e)
    neutral_dist, neutral_next = {}, {}
    queue = deque(sorted(choices))
    for s in queue:
        neutral_dist[s] = 0
    while queue:
        t = queue.popleft()
        for s in sorted(low[t]):
            if s not in neutral_dist:
                neutral_dist[s], neutral_next[s] = neutral_dist[t] + 1, t
                queue.append(s)
    assert set(neutral_dist) == basin
    paths = []
    for start_id in sorted(basin):
        s, path = start_id, [start_id]
        while s not in choices:
            s = neutral_next[s]
            path.append(s)
        exit_offset = len(path) - 1
        s = choices[s]['target']
        path.append(s)
        while s not in goals:
            s = successor[s]
            path.append(s)
        assert all(i not in basin for i in path[exit_offset + 1:])
        assert max(chi[i] for i in path) == k + 1
        assert source['kappa'][start_id] == k + 1
        paths.append(dict(start=start_id, path=path, exit_offset=exit_offset))
    return dict(start=start, level=k, states=sorted(basin), exits=exits,
        good_exits=good, routes=paths,
        summary=dict(states=len(basin), exits=len(exits),
            exit_levels=dict(sorted(Counter(chi[e['target']] for e in exits).items())),
            good_exits=len(good), exit_sources=len(choices),
            max_neutral_steps=max(neutral_dist.values()),
            max_total_steps=max(len(r['path']) - 1 for r in paths)))


def report():
    source = json.loads(SOURCE.read_text())
    for path, digest in source['hashes'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    # Using undirected components requires actual reversibility of every edge.
    keys = {(s, e['target'], tuple(e['pair']), tuple(e['component']))
            for s, es in enumerate(source['transitions']) for e in es if e['boundary_roots']}
    assert all((t, s, p, b) in keys for s, t, p, b in keys)
    model = EdgeModel(source['graph'])
    basins = [plateau(source, 126, 3), plateau(source, 84, 2)]
    replayed_steps = 0
    for basin in basins:
        for route in basin['routes']:
            c = tuple(source['states'][route['start']])
            for event in path_events(source, route['path']):
                c = model.apply(c, Move(tuple(event['pair']), tuple(event['component'])))
                assert c == tuple(source['states'][event['target']])
                replayed_steps += 1
    detailed = []
    for start in (126, 247):
        witness = next(w for w in source['witnesses'] if w['state'] == start)
        detailed.append(dict(start=start, events=[cut_audit(source, model, e, True)
                            for e in witness['optimal_peak']['events']]))
    exits = [cut_audit(source, model, e) for basin in basins for e in basin['good_exits']]
    # Real negative control: collapsing parallel quotient edges loses a cycle.
    q = detailed[0]['events'][0]['systems'][0]['after']
    simple = nx.Graph()
    simple.add_nodes_from(range(len(q['blocks'])))
    simple.add_edges_from((u, v) for u, v, _ in q['edges'])
    wrong = simple.number_of_edges() - simple.number_of_nodes() + nx.number_connected_components(simple)
    assert wrong != q['quotient_nullity']
    # A second barrier shows that the valley is necessary, not just a poor route.
    chi, goals = source['chi'], set(source['goals'])
    band = induced(source, lambda i: 3 <= chi[i] <= 4)
    upper = set(nx.node_connected_component(band, 247))
    assert not upper & goals
    band_exits = [dict(source=s, **e) for s in sorted(upper) for e in source['transitions'][s]
                  if e['boundary_roots'] and e['target'] not in upper and chi[e['target']] <= 4]
    assert band_exits and all(chi[e['target']] == 2 for e in band_exits)
    assert all(source['thresholds']['2']['rank'][e['target']] is None for e in band_exits)
    assert all(source['kappa'][e['target']] == 3 for e in band_exits)
    # Exact endpoints cannot be rejoined while skipping this low region.
    replacements = []
    for target in (2026, 4147):
        g = induced(source, lambda i: 3 <= chi[i] <= 4 or i == target)
        reached = sorted(nx.node_connected_component(g, 247))
        assert target not in reached
        replacements.append(dict(start=247, target=target, reachable=reached,
                                 rule='All intermediate chi in [3,4]; target exempt from lower bound'))
    files = {SOURCE, Path(__file__).resolve(), ROOT / 'scripts/c5_cut_interfaces.py',
             *(ROOT / p for p in source['hashes'])}
    return dict(trust='Fixed-graph Python certificates; cycle-nullity and barrier lemmas proved on paper in companion document, not Lean.',
        source=str(SOURCE.relative_to(ROOT)), plateaus=basins,
        witness_cut_replays=detailed, exit_cut_audits=exits,
        parallel_edge_negative_control=dict(source=126, target=14, system=0,
            correct_nullity=q['quotient_nullity'], simplified_nullity=wrong),
        forced_valley=dict(start=247, band_states=sorted(upper), exits=band_exits,
                           exact_endpoint_replacement_failures=replacements),
        summary=dict(plateaus=[b['summary'] for b in basins], audited_exit_transitions=len(exits),
            audited_witness_transitions=sum(len(w['events']) for w in detailed),
            replayed_macro_steps=replayed_steps,
            upper_band_states=len(upper), upper_band_exits=len(band_exits),
            upper_band_exit_targets=len({e['target'] for e in band_exits})),
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
