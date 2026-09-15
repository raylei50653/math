#!/usr/bin/env python3
"""Source-only guard repair interfaces on the existing 72 B2 preparations."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_singleton_preparation import tail_guard, success_boundary
from c5_strategy_barriers import quotient

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
PREPARATION = ROOT / 'artifacts/c5_cells/singleton_preparation.json'
OUT = ROOT / 'artifacts/c5_cells/guard_repair.json'


def blocks(model, vertices):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from((u, v) for u, v in model.edges if u in vertices and v in vertices)
    return sorted(map(sorted, nx.connected_components(g)))


def rooted(model, vertices, root):
    return set(next(b for b in blocks(model, vertices) if root in b))


def source_cost(model, c, pair, component):
    """Cut types and retained owners only; no apply, target, or cycle table."""
    component = set(component)
    cut = {e for e, (u, v) in enumerate(model.edges) if (u in component) != (v in component)}
    old = [c[u] ^ c[v] for u, v in model.edges]
    k = pair[0] ^ pair[1]
    assert all(old[e] != k for e in cut)
    charts = []
    for types in TYPE_PAIRS:
        retained = [e for e, t in enumerate(old) if t in types and e not in cut]
        before, after = [quotient(model, retained, sorted(e for e in cut if (old[e] ^ x) in types))
                         for x in (0, k)]
        charts.append(dict(types=types, retained_edges=retained, before=before, after=after,
                           delta=after['quotient_nullity'] - before['quotient_nullity']))
    return dict(cut_edges=sorted(cut), charts=charts,
                predicted_delta=[r['delta'] for r in charts])


def repair_source(model, c):
    """Common roles A/B/C/D=0/1/2/3; sufficient predicate P from source sets."""
    assert c[:5] == (0, 3, 2, 0, 1)
    V = [{v for v, color in enumerate(c) if color == i} for i in range(4)]
    Q = rooted(model, V[1] | V[2], 2)
    # After BC repair AND common B/C role renaming, these are the role classes.
    Bstar = (V[1] & Q) | (V[2] - Q)
    Cstar = (V[2] & Q) | (V[1] - Q)
    Sstar = rooted(model, V[0] | Bstar, 0)
    Wstar = Cstar | (V[0] - Sstar) | (Bstar & Sstar)
    trace = sorted(Q & set(range(5)))
    neighbors_in_W = sorted(set(model.adj[2]) & Wstar)
    cost = source_cost(model, c, (1, 2), Q)
    ranks = [[r['before']['quotient_nullity'], r['after']['quotient_nullity']]
             for r in cost['charts']]
    # X=D13 closes exactly one cycle on each side; Y=D23 loses one.
    P = trace == [2, 4] and not neighbors_in_W and ranks[1:] == [[1, 1], [1, 0]]
    return dict(Q=sorted(Q), Bstar=sorted(Bstar), Cstar=sorted(Cstar),
                Sstar=sorted(Sstar), Wstar=sorted(Wstar),
                Wstar_components=blocks(model, Wstar), trace=trace,
                neighbors2_in_Wstar=neighbors_in_W, cost=cost, predicate=P)


def exact_guard_replay(model, c):
    g = tail_guard(model, c)
    A, B, C, D = g['role_colors']
    first = next(a for a in model.actions(c) if set(a.pair) == {A, B} and 0 in a.component)
    d = model.apply(c, first)
    assert d[:5] == (B, D, C, B, A)
    last = next(a for a in model.actions(d) if set(a.pair) == {A, C} and 4 in a.component)
    end = model.apply(d, last)
    expected = (B, D, C, B, C) if g['separated'] else (B, D, A, B, C)
    assert end[:5] == expected and success_boundary(end) == g['separated']
    return dict(guard=g['separated'], final_boundary=end[:5],
                last_boundary_trace=sorted(set(last.component) & set(range(5))))


def report():
    source, prep = [json.loads(p.read_text()) for p in (SOURCE, PREPARATION)]
    for artifact in (source, prep):
        for p, digest in artifact['hashes'].items():
            assert sha256((ROOT / p).read_bytes()).hexdigest() == digest, p
    model = EdgeModel(source['graph'])
    orbits, repairs, guards, cost_rows = Counter(), [], [], []
    failed_orbits = set()
    for row in prep['preparations']:
        sid = row['path'][1]
        raw = tuple(source['states'][sid])
        A, D, C, _, B = raw[:5]
        roles = {A: 0, B: 1, C: 2, D: 3}
        c = tuple(roles[x] for x in raw)
        orbits[c] += 1
        checked = exact_guard_replay(model, c)
        guards.append(dict(source=sid, **checked))
        if not checked['guard']:
            failed_orbits.add(c)
            audit = repair_source(model, c)
            assert audit['predicate']
            action = next(a for a in model.actions(c) if a.pair == (1, 2) and 2 in a.component)
            assert list(action.component) == audit['Q']
            d = model.apply(c, action)
            actual = tail_guard(model, d)
            assert actual['first_component'] == audit['Sstar']
            assert actual['predicted_AC_vertices'] == audit['Wstar']
            assert actual['predicted_AC_components'] == audit['Wstar_components']
            assert actual['separated'] and [2] in actual['predicted_AC_components']
            assert audit['cost']['predicted_delta'] == [0, 0, -1]
            assert exact_guard_replay(model, d)['guard']
            repairs.append(dict(source=sid, **audit))
        # Independently replay every saved tail action, without search/rank solving.
        current = raw
        for event in row['events'][1:]:
            a = next(a for a in model.actions(current)
                     if list(a.pair) == event['pair'] and list(a.component) == event['component'])
            predicted = source_cost(model, current, a.pair, a.component)
            target = model.apply(current, a)
            vectors = [[sum(not terminals for terminals, _ in system)
                        for system in model.dual.systems(z)] for z in (current, target)]
            delta = [b - a for a, b in zip(*vectors)]
            assert delta == predicted['predicted_delta'] and sum(delta) <= 0
            assert target == tuple(source['states'][event['target']])
            cost_rows.append(dict(source=event['source'], target=event['target'], **predicted))
            current = target
    assert len(guards) == 72 and len(repairs) == 24 and len(cost_rows) == 168
    assert len(orbits) == 3 and set(orbits.values()) == {24}
    assert len(failed_orbits) == 1
    files = {SOURCE, PREPARATION, Path(__file__).resolve(),
             *(ROOT / p for a in (source, prep) for p in a['hashes'])}
    return dict(trust='Conditional source-interface lemmas on paper, not Lean; fixed B2 replay only.',
                summary=dict(prepared_sources=72, exact_guard_true=48, exact_guard_false=24,
                             repaired_guard_replays=24, repair_predicate_passes=24,
                             source_cost_replays=168, common_color_orbits=3,
                             failed_common_color_orbits=1),
                color_orbits=[dict(role_coloring=c, multiplicity=n) for c, n in sorted(orbits.items())],
                guards=guards, repairs=repairs, tail_costs=cost_rows,
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
