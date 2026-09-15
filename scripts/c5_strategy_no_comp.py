#!/usr/bin/env python3
"""Delete all directed compensating rises in the existing fixed closure."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_strategy_safe import solve, route

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
BARRIERS = ROOT / 'artifacts/c5_cells/strategy_barriers.json'
OUT = ROOT / 'artifacts/c5_cells/strategy_no_comp.json'


def report():
    source, barriers = [json.loads(p.read_text()) for p in (SOURCE, BARRIERS)]
    for artifact in (source, barriers):
        for path, digest in artifact['hashes'].items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    rows, states = source['transitions'], source['states']
    chi, vectors, goals = source['chi'], source['cycle_vectors'], set(source['goals'])
    model = EdgeModel(source['graph'])
    # Recompute ordered systems once per complete coloring. Keep system identity.
    systems = [model.dual.systems(tuple(c)) for c in states]
    assert vectors == [[sum(not terminals for terminals, _ in system)
                        for system in triple] for triple in systems]
    banned, audited = [], 0
    def delta(s, e):
        return [b - a for a, b in zip(vectors[s], vectors[e['target']])]
    def comp(s, e):
        return sorted(delta(s, e)) == [-1, 0, 2]
    for s, edges in enumerate(rows):
        c = tuple(states[s])
        for a, e in enumerate(edges):
            if not e['boundary_roots']:
                continue
            t = e['target']
            assert model.apply(c, Move(tuple(e['pair']), tuple(e['component']))) == tuple(states[t])
            assert e['boundary_roots'] == [v for v in e['component'] if v < 5]
            p = e['pair'][0] ^ e['pair'][1]
            preserved = tuple(x for x in (1, 2, 3) if x != p)
            si = TYPE_PAIRS.index(preserved)
            assert systems[s][si] == systems[t][si]
            audited += 1
            if comp(s, e):
                banned.append(dict(source=s, edge_index=a, target=t, delta=delta(s, e),
                                   preserved_system=preserved))
    rooted = lambda s, e: bool(e['boundary_roots'])
    allowed = lambda s, e: rooted(s, e) and not comp(s, e)
    thresholds, summary = {}, {}
    for k in (3, 4):
        safe = lambda s: chi[s] <= k
        baseline = solve(rows, goals, rooted, safe)
        assert baseline == source['thresholds'][str(k)]
        sol = solve(rows, goals, allowed, safe)
        # Independent directed graph calculation; inverse rises remain allowed.
        graph = nx.DiGraph()
        graph.add_nodes_from(i for i in range(len(states)) if safe(i))
        graph.add_edges_from((s, e['target']) for s, es in enumerate(rows) for e in es
                            if safe(s) and safe(e['target']) and allowed(s, e))
        sentinel = len(states)
        graph.add_node(sentinel)
        graph.add_edges_from((g, sentinel) for g in goals if safe(g))
        distances = nx.single_source_shortest_path_length(graph.reverse(), sentinel)
        assert sol['rank'] == [distances[i] - 1 if i in distances else None for i in range(len(states))]
        win = [i for i, r in enumerate(baseline['rank']) if r is not None]
        new_win = [i for i, r in enumerate(sol['rank']) if r is not None]
        lost = sorted(set(win) - set(new_win))
        assert set(new_win) <= set(win)
        penalty = Counter(sol['rank'][i] - baseline['rank'][i] for i in new_win)
        assert all(d >= 0 for d in penalty)
        # If deletion loses states, give a forward-closed unreachable witness
        # and all deleted outgoing edges, alongside the old successful route.
        witness = None
        if lost:
            start = lost[0]
            reached = {start} | nx.descendants(graph, start)
            assert not reached & goals and sentinel not in reached
            deleted_exits = [e for e in banned if e['source'] in reached
                             and safe(e['target']) and e['target'] not in reached]
            assert deleted_exits
            witness = dict(start=start, reachable=sorted(reached), deleted_exits=deleted_exits,
                           baseline_route=route(rows, baseline, start),
                           reachable_equals_lost=sorted(reached) == lost,
                           reachable_chi_histogram=dict(sorted(Counter(chi[i] for i in reached).items())))
        thresholds[str(k)] = dict(**sol, winning=new_win, lost=lost,
            safe_losing=[i for i in range(len(states)) if safe(i) and sol['rank'][i] is None],
            witness=witness, example_routes=[route(rows, sol, i) for i in (126, 247, 3022)],
            summary=dict(initially_safe=sum(map(safe, range(len(states)))),
                baseline_winning=len(win), no_comp_winning=len(new_win), lost=len(lost),
                deleted_safe_edges=sum(safe(e['source']) and safe(e['target']) for e in banned),
                distance_penalty_histogram=dict(sorted(penalty.items())),
                max_distance=max(sol['rank'][i] for i in new_win)))
        summary[str(k)] = thresholds[str(k)]['summary']
    plateaus = []
    for b in barriers['plateaus']:
        ordinary = [e for e in b['good_exits'] if sorted(delta(e['source'], e)) == [0, 0, 1]]
        compensating = [e for e in b['good_exits'] if comp(e['source'], e)]
        assert ordinary and len(ordinary) + len(compensating) == len(b['good_exits'])
        plateaus.append(dict(level=b['level'], ordinary_exits=len(ordinary),
                             compensating_exits=len(compensating)))
    files = {SOURCE, BARRIERS, Path(__file__).resolve(),
             *(ROOT / p for a in (source, barriers) for p in a['hashes'])}
    return dict(scope='Fixed certified 5952-state closure; boundary-root directed edges; Python evidence, not Lean.',
        forbidden='sorted(target cycle vector - source cycle vector) == [-1,0,2]',
        system_order=TYPE_PAIRS, banned_edges=banned, thresholds=thresholds,
        summary=dict(thresholds=summary, deleted_rooted_edges=len(banned),
                     replayed_rooted_edges=audited, plateaus=plateaus),
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
