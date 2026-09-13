#!/usr/bin/env python3
"""Two-layer raw configurations of committed-colour strips: future refinement by depth.

Model (chosen instantiation of the "two-layer locality" assumption, stated explicitly):
the strip grammar of stepwise_strip_width (row r vertex (r,i) sees (r-1, i..i+f_r-1) and
(r, i+-1); row 0 is the boundary), but EVERY introduced vertex has a committed colour, not an
existential one.  Vertex (r,i) is introduced at step s(r,i) = i + sum_{q<=r}(f_q-1); layer t
is the set of vertices with s in [w t, w t + w - 1].  A future vertex only touches layers
t-1, t, t+1 when 2w >= max(f)-1, and layer t-1 is genuinely needed when some f > w+1; both
are asserted.  The raw configuration is x_t = (L_{t-1}, L_t) with all colours, plus the
clipped layer index for the left-end transient.  An action is a legal colouring of the whole
next layer; the successor is (L_t, L_{t+1}).  Stopping is always allowed (every reachable
configuration is a proper colouring), so F_0 is constant and refinement is driven by the
labelled legal-continuation trees.

Everything here is computationally observed on finite shapes; no Lean, no disk claim, no
claim about the existential boundary residuals of the other stepwise scripts (compared only).
"""
from collections import Counter, deque
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys

from stepwise_strip_width import automaton, build

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/layer_refinement.json'
PERMS = list(permutations(range(4)))
SHAPES = [((3,), 1), ((3, 3), 1), ((3, 3, 3), 1), ((3, 3, 3, 3), 1), ((3, 3, 3, 3, 3), 1),
          ((3, 3, 3, 3, 3, 3), 1), ((2, 3), 1), ((2, 2, 3), 1), ((3, 2, 3), 1),
          ((4,), 2), ((5,), 2), ((6,), 3), ((7,), 3), ((4, 4), 2), ((5, 5), 2), ((2, 4), 2)]
EXISTENTIAL = [(3,), (4,), (5,), (6,), (7,), (3, 3), (3, 3, 3), (2, 3), (2, 4)]
WALKS, WALK_LENGTH = 2000, 100


def layout(fans, w):
    offset = [0]
    for f in fans:
        offset.append(offset[-1] + f - 1)
    rows = len(fans) + 1

    def step(v):
        return v[1] + offset[v[0]]

    def layer_vertices(t):
        return [(r, s - offset[r]) for s in range(w * t, w * t + w)
                for r in range(rows) if s - offset[r] >= 0]

    def lower(v):
        """Neighbours introduced no later than v (left neighbour and the fan below)."""
        r, i = v
        out = [(r, i - 1)] if i else []
        if r:
            out += [(r - 1, i + j) for j in range(fans[r - 1])]
        return out

    assert all(2 * w >= f - 1 for f in fans), 'future would reach beyond layer t-1'
    assert any(f > w + 1 for f in fans), 'layer t-1 would never be needed'
    t_full = -(-offset[-1] // w)   # first layer index containing every row
    return dict(step=step, layer_vertices=layer_vertices, lower=lower, t_full=t_full)


def enumerate_model(fans, w):
    """All reachable raw configurations, their legal next layers and successors."""
    L = layout(fans, w)
    ts = L['t_full'] + 1   # from this clipped index on, both layers are full
    start = (-1, (), ())
    states, order, trans, path = {start: 0}, [start], [], {0: []}
    todo = deque([0])
    while todo:
        s = todo.popleft()
        t, prev, cur = order[s]
        verts = L['layer_vertices'](t + 1)
        colour = dict(zip(L['layer_vertices'](t - 1), prev)) if t >= 1 else {}
        colour.update(zip(L['layer_vertices'](t), cur) if t >= 0 else [])
        acts = {}

        def go(k, chosen):
            if k == len(verts):
                nxt = (min(t + 1, ts), cur, tuple(chosen))
                if nxt not in states:
                    states[nxt] = len(order)
                    order.append(nxt)
                    path[len(order) - 1] = path[s] + [tuple(chosen)]
                    todo.append(len(order) - 1)
                acts[tuple(chosen)] = states[nxt]
                return
            v = verts[k]
            forbidden = set()
            for u in L['lower'](v):
                if u in colour:
                    forbidden.add(colour[u])
                else:
                    assert L['step'](u) >= w * (t + 1)   # same layer, coloured later in `go`
            for c in range(4):
                if c not in forbidden:
                    colour[v] = c
                    chosen.append(c)
                    go(k + 1, chosen)
                    chosen.pop()
                    del colour[v]
        go(0, [])
        trans.append(acts)
    return dict(fans=fans, w=w, L=L, ts=ts, order=order, trans=trans, path=path)


def refine(order, trans):
    """Moore refinement by future depth; returns the history of partitions and counts."""
    part = [0] * len(order)   # F_0: every reachable configuration is acceptable now
    history, counts = [part], [1]
    while True:
        ids, new = {}, []
        for s, acts in enumerate(trans):
            key = (part[s],) + tuple(sorted((a, part[t]) for a, t in acts.items()))
            new.append(ids.setdefault(key, len(ids)))
        history.append(new)
        counts.append(len(ids))
        if len(ids) == counts[-2]:
            # Same number of blocks and each new block refines an old one: the partitions
            # coincide, so the next round sees the same successor classes and cannot split.
            assert len({(part[s], new[s]) for s in range(len(order))}) == len(ids)
            return history, counts
        part = new


def horizons(order, trans):
    """Maximum number of further layers; None = unbounded."""
    alive, h, level = set(range(len(order))), {}, 0
    while True:
        sinks = [s for s in alive if all(t not in alive for t in trans[s].values())]
        if not sinks:
            break
        for s in sinks:
            h[s] = level
            alive.discard(s)
        level += 1
    for s in alive:
        h[s] = None
    return h


def tarjan(nodes, edges):
    index, low, stack, on, comps, counter = {}, {}, [], set(), [], 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(edges.get(root, ())))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            for u in it:
                if u not in index:
                    index[u] = low[u] = counter
                    counter += 1
                    stack.append(u)
                    on.add(u)
                    work.append((u, iter(edges.get(u, ()))))
                    break
                if u in on:
                    low[v] = min(low[v], index[u])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        u = stack.pop()
                        on.discard(u)
                        comp.append(u)
                        if u == v:
                            break
                    comps.append(sorted(comp))
    return comps


def independent_proper(fans, w, layers):
    """Full-graph properness of the committed colouring given as a list of layers.

    Uses stepwise_strip_width.build (a separate adjacency implementation) and checks every
    edge in both directions; no use of `layout` or the enumerator.
    """
    L = layout(fans, w)   # only for the vertex order inside a layer
    _, neighbours, _, exists, _ = build(fans)
    colour = {}
    for t, layer in enumerate(layers):
        colour.update(zip(L['layer_vertices'](t), layer))
    return all(colour[u] != colour[v] for v in colour for u in neighbours(v) if u in colour)


def constraint_map(model, s, future):
    L, order = model['L'], model['order']
    t, prev, cur = order[s]
    colour = dict(zip(L['layer_vertices'](t - 1), prev))
    colour.update(zip(L['layer_vertices'](t), cur))
    return tuple(frozenset(colour[u] for u in L['lower'](f) if u in colour) for f in future)


def separate(model, part, x, y):
    """Shortest continuation legal from exactly one of x, y (BFS on the synchronous pair)."""
    trans = model['trans']
    todo, seen = deque([(x, y, ())]), {(x, y)}
    while todo:
        a, b, word = todo.popleft()
        for act in sorted(set(trans[a]) | set(trans[b])):
            if (act in trans[a]) != (act in trans[b]):
                return word + (act,), act in trans[a]
            pair = trans[a][act], trans[b][act]
            if pair not in seen:
                seen.add(pair)
                todo.append((*pair, word + (act,)))
    raise AssertionError('behaviourally distinct raw configurations must be separable')


def analyse_shape(fans, w):
    model = enumerate_model(fans, w)
    order, trans, L, ts, path = (model[k] for k in ('order', 'trans', 'L', 'ts', 'path'))
    history, counts = refine(order, trans)
    part = history[-1]
    depth = len(counts) - 2   # first depth k with P_k = P_{k+1}
    assert depth <= 2, 'two-layer locality bounds the identification depth by 2'
    stationary = [s for s in range(len(order)) if order[s][0] == ts]
    verts = L['layer_vertices'](ts - 1) + L['layer_vertices'](ts)
    future = L['layer_vertices'](ts + 1) + L['layer_vertices'](ts + 2)
    flat = {s: order[s][1] + order[s][2] for s in stationary}
    h = horizons(order, trans)
    live = [s for s in stationary if trans[s]]
    dead = [s for s in stationary if not trans[s]]
    stat_curve = [len({p[s] for s in stationary}) for p in history]
    # Structural signature: the constraint map (forbidden colour set of every vertex of the
    # next two layers) is exactly the behavioural class on live configurations, and all dead
    # configurations form one class.
    maps = {s: constraint_map(model, s, future) for s in stationary}
    map_to_class, class_to_map = {}, {}
    for s in live:
        assert map_to_class.setdefault(maps[s], part[s]) == part[s]
        assert class_to_map.setdefault(part[s], maps[s]) == maps[s]
    assert len({part[s] for s in dead}) <= 1
    assert not ({part[s] for s in dead} & {part[s] for s in live})
    # Colour symmetry: the partition is S4-equivariant; count orbits of stationary classes.
    index = {st: i for i, st in enumerate(order)}

    def act(p, st):
        return (st[0], tuple(p[c] for c in st[1]), tuple(p[c] for c in st[2]))
    image = {}
    for s in stationary:
        for p in PERMS:
            t = index[act(p, order[s])]
            assert image.setdefault((part[s], p), part[t]) == part[t]
    classes = sorted({part[s] for s in stationary})
    orbit_of, orbits = {}, []
    for k in classes:
        if k not in orbit_of:
            orb = sorted({image[k, p] for p in PERMS})
            for j in orb:
                orbit_of[j] = len(orbits)
            orbits.append(orb)
    # Class graph, SCCs, recurrent classes (image iteration), viable core (unbounded horizon).
    edges = {}
    for s in stationary:
        edges.setdefault(part[s], set()).update(part[t] for t in trans[s].values())
    comps = tarjan(classes, edges)
    scc_of = {k: i for i, comp in enumerate(comps) for k in comp}
    cyclic = {i for i, comp in enumerate(comps)
              if len(comp) > 1 or comp[0] in edges.get(comp[0], ())}
    reach, seen, sequence = frozenset([0]), {}, []
    while reach not in seen:
        seen[reach] = len(sequence)
        sequence.append(reach)
        reach = frozenset(t for s in reach for t in trans[s].values())
    recurrent = {part[s] for s in frozenset().union(*sequence[seen[reach]:])}
    core = {part[s] for s in stationary if h[s] is None}
    for k in core:   # strategy core: every core class has a move staying inside
        assert any(t in core for t in edges[k])
    # Robust core: greatest set in which EVERY legal move stays (no lookahead needed).
    safe = set(core)
    while True:
        shrunk = {k for k in safe if edges[k] and edges[k] <= safe}
        if shrunk == safe:
            break
        safe = shrunk
    core_on_cycle = {k for k in core if scc_of[k] in cyclic}
    class_h = {}
    for s in stationary:
        assert class_h.setdefault(part[s], h[s]) == h[s]
    # Which raw coordinates matter: all minimal subsets of the 2-layer tuple that determine
    # the class (over stationary configurations), and the vertices with future neighbours.
    def determined(S, pool):
        m = {}
        return all(m.setdefault(tuple(flat[s][i] for i in S), part[s]) == part[s] for s in pool)
    minimal = []
    for size in range(len(verts) + 1):
        for S in combinations(range(len(verts)), size):
            if not any(set(m) <= set(S) for m in minimal) and determined(S, stationary):
                minimal.append(S)
    active = sorted({u for f in future for u in L['lower'](f) if u in verts})
    # Distinguishing examples, each replayed on the full graph by independent code.
    examples = []

    def witness(x, y, kind):
        word, x_side = separate(model, part, x, y)
        ok, bad = (x, y) if x_side else (y, x)
        good_layers = path[ok] + list(word)
        bad_layers = path[bad] + list(word)
        assert independent_proper(fans, w, good_layers)
        assert not independent_proper(fans, w, bad_layers)
        assert independent_proper(fans, w, bad_layers[:-1])
        examples.append(dict(kind=kind, accepting=flat[ok], rejecting=flat[bad],
                             class_ids=[part[ok], part[bad]], continuation=list(word),
                             accepting_history=path[ok], rejecting_history=path[bad]))
    # (a) first pair split only at depth 2 (same legal next layers, different later)
    groups = {}
    for s in stationary:
        groups.setdefault(history[1][s], []).append(s)
    split2 = [(g, m) for g, m in groups.items() if len({part[s] for s in m}) > 1]
    for _, members in sorted(split2)[:2]:
        by = {}
        for s in members:
            by.setdefault(part[s], s)
        x, y = list(by.values())[:2]
        assert set(trans[x]) == set(trans[y])
        witness(x, y, 'same legal next layers, split only by the second future layer')
    # (b) same current layer L_t, different class
    by_cur = {}
    for s in live:
        by_cur.setdefault(order[s][2], {}).setdefault(part[s], s)
    for cur, by in sorted(by_cur.items()):
        if len(by) > 1:
            x, y = list(by.values())[:2]
            witness(x, y, 'same current layer, different older layer')
            break
    # (c) trap versus core with the same legal next layers, if traps exist
    for _, members in sorted(split2):
        hs = {h[s]: s for s in members}
        if None in hs and len(hs) > 1:
            witness(hs[None], hs[max(k for k in hs if k is not None)],
                    'unbounded versus trapped, same legal next layers')
            break
    # Uniform random legal walks from the left end: survival and class concentration.
    rng = random.Random(0)
    survived, visited = 0, Counter()
    for _ in range(WALKS):
        s = 0
        for _ in range(WALK_LENGTH):
            if not trans[s]:
                break
            s = trans[s][rng.choice(sorted(trans[s]))]
        else:
            survived += 1
            visited[part[s]] += 1
    # Orbit-level (colour-aligned) transition graph: the readable final graph.
    orbit_edges = {}
    for k in classes:
        orbit_edges.setdefault(orbit_of[k], set()).update(orbit_of[t] for t in edges[k])
    orbit_table = []
    for i, orb in enumerate(orbits):
        k = orb[0]
        rep = min(tuple(p[c] for c in flat[s]) for s in stationary if part[s] == k for p in PERMS)
        orbit_table.append(dict(id=i, classes=len(orb), canonical_representative=rep,
            raw_per_class=sum(1 for s in stationary if part[s] == k), actions=len(trans[next(s for s in stationary if part[s] == k)]),
            horizon=class_h[k], core=k in core, robust=k in safe, on_cycle=k in core_on_cycle,
            successors=sorted(orbit_edges[i])))
    return dict(fans=fans, layer_width=w, t_full=L['t_full'], stationary_vertices=verts,
        future_vertices=future, active_vertices=active,
        raw=dict(total=len(order), stationary=len(stationary), stationary_live=len(live),
                 stationary_dead=len(dead)),
        refinement_counts=counts, stationary_refinement_counts=stat_curve, fixed_point_depth=depth,
        stationary_classes=len(classes), stationary_live_classes=len({part[s] for s in live}),
        stationary_dead_classes=len({part[s] for s in dead}),
        horizon_classes=dict(sorted(Counter('inf' if v is None else str(v) for v in class_h.values()).items())),
        constraint_map_is_exact_signature=True, orbits=len(orbits),
        orbit_sizes=dict(sorted(Counter(len(o) for o in orbits).items())),
        core_classes=len(core), robust_core_classes=len(safe), core_on_cycle=len(core_on_cycle),
        core_transient=len(core - core_on_cycle),
        recurrent_classes=len(recurrent), core_is_subset_of_recurrent=core <= recurrent,
        trap_classes=len(set(class_h) - core - {part[s] for s in dead}),
        scc=dict(count=len(comps), with_cycle=len(cyclic),
                 cyclic_sizes=dict(sorted(Counter(len(comps[i]) for i in cyclic).items())),
                 core_scc_count=len({scc_of[k] for k in core})),
        minimal_determining_subsets=[[verts[i] for i in S] for S in minimal],
        random_walks=dict(walks=WALKS, length=WALK_LENGTH, survived=survived,
                          distinct_final_classes=len(visited), distinct_final_orbits=len({orbit_of[k] for k in visited})),
        examples=examples, orbit_graph=orbit_table,
        classes=[dict(id=k, representative=flat[next(s for s in stationary if part[s] == k)],
                      raw_count=sum(1 for s in stationary if part[s] == k),
                      actions=len(trans[next(s for s in stationary if part[s] == k)]),
                      horizon=class_h[k], core=k in core, robust=k in safe, orbit=orbit_of[k], scc=scc_of[k],
                      constraint_map=[sorted(c) for c in class_to_map[k]] if k in class_to_map else None,
                      successors=sorted(edges[k]))
                 for k in classes])


def readable_rules(results):
    """Explicit human-readable rules for (3) and (3,3), checked against every class."""
    r3 = results['fans3']
    # (3): b_{t-1} and u_{t-2} are interchangeable; class = (b_t, {b_{t-1}, u_{t-2}}).
    seen = {}
    for c in r3['classes']:
        b1, _, b0, u = c['representative']
        assert c['horizon'] is None and c['actions'] == 2 and c['raw_count'] == 4
        assert seen.setdefault((b0, frozenset({b1, u})), c['id']) == c['id']
    assert len(seen) == 12
    r33 = results['fans33']
    families = Counter()
    for c in r33['classes']:
        b1, u1, _, b0, u0, v0 = c['representative']
        if c['horizon'] == 0:
            assert v0 == b1 and u1 == b0
            families['dead: v_{t-4}=b_{t-1} and u_{t-3}=b_t'] += 1
        elif v0 == b1:
            assert u1 != b0 and c['raw_count'] == 1 and c['actions'] == 2
            families['B: v_{t-4}=b_{t-1}, u_{t-3} the fourth colour'] += 1
        else:
            assert {u1, v0} == set(range(4)) - {b1, u0} and c['raw_count'] == 4 and c['actions'] == 2
            families['A: {u_{t-3}, v_{t-4}} complementary to {b_{t-1}, u_{t-2}}'] += 1
    assert dict(families) == {'dead: v_{t-4}=b_{t-1} and u_{t-3}=b_t': 1,
                              'B: v_{t-4}=b_{t-1}, u_{t-3} the fourth colour': 24,
                              'A: {u_{t-3}, v_{t-4}} complementary to {b_{t-1}, u_{t-2}}': 24}
    # Family A keeps both legal moves inside A; family B keeps only b_{t+1} = b_{t-1}
    # (successor in B) and dies on b_{t+1} = u_{t-2}.
    fam = {c['id']: ('dead' if c['horizon'] == 0 else 'B' if c['representative'][5] == c['representative'][0] else 'A')
           for c in r33['classes']}
    succ = {c['id']: sorted(fam[t] for t in c['successors']) for c in r33['classes']}
    assert all(succ[k] == ['A', 'A'] for k in fam if fam[k] == 'A')
    assert all(succ[k] == ['B', 'dead'] for k in fam if fam[k] == 'B')
    return dict(fans3='class = (b_t, {b_{t-1}, u_{t-2}}); 12 classes, 1 orbit, never dies',
                fans33=dict(families=dict(families), moves='A -> A on both legal moves; B -> B on b_{t+1}=b_{t-1}, dead on b_{t+1}=u_{t-2}'))


def existential_curves():
    out = {}
    for fans in EXISTENTIAL:
        order, delta, _ = automaton(fans)
        cls = [0 if s else 1 for s in order]
        counts = [len(set(cls))]
        while True:
            sig, new = {}, []
            for i, row in enumerate(delta):
                new.append(sig.setdefault((cls[i],) + tuple(cls[j] for j in row), len(sig)))
            counts.append(len(sig))
            if len(sig) == counts[-2]:
                break
            cls = new
        out['fans' + ''.join(map(str, fans))] = dict(raw_cut_states=len(order), refinement_counts=counts,
                                                     fixed_point_depth=len(counts) - 2)
    return out


def analyse():
    results = {}
    for fans, w in SHAPES:
        results['fans' + ''.join(map(str, fans))] = analyse_shape(fans, w)
    # Observed count laws for n nested fan-3 rows (n <= 6 only; not proved).
    for n in range(1, 7):
        r = results['fans' + '3' * n]
        assert r['stationary_live_classes'] == 12 * n * 2 ** (n - 1)
        assert r['stationary_dead_classes'] == (0 if n == 1 else 1)
        assert r['core_classes'] == 36 * 2 ** (n - 1) - 24
        assert r['robust_core_classes'] == 12 * 2 ** (n - 1)
        assert r['fixed_point_depth'] == min(n, 2)
        traps = {int(h): c for h, c in r['horizon_classes'].items() if h not in ('inf', '0')}
        assert traps == {h: 24 * (n - 1 - h) * 2 ** (n - 2 - h) for h in range(1, n - 1)}
    return dict(status='computationally observed; committed-colour strip layers, not the existential boundary residual, not Lean',
        model='layer t = vertices introduced at steps w t .. w t + w - 1 with committed colours; raw configuration = (L_{t-1}, L_t); action = legal next layer',
        locality='asserted per shape: 2w >= max(f)-1 (future touches only layers t-1, t) and some f > w+1 (layer t-1 is needed)',
        depth_bound='F_2 determines all F_d: only legal(L_{t-1},L_t,L_{t+1}) and legal(L_t,L_{t+1},L_{t+2}) mention the configuration; asserted fixed_point_depth <= 2 on every shape',
        signature='live class = constraint map (forbidden colour set of each vertex of the next two layers); dead configurations form one class; asserted on every shape',
        nested_fan3_laws=dict(scope='n <= 6 nested fan-3 rows, observed only',
            live_classes='12 n 2^(n-1)', strategy_core='36 2^(n-1) - 24', robust_core='12 2^(n-1)',
            trap_classes_with_horizon_h='24 (n-1-h) 2^(n-2-h) for 1 <= h <= n-2', identification_depth='min(n, 2)'),
        shapes=results, readable_rules=readable_rules(results), existential_comparison=existential_curves())


if __name__ == '__main__':
    content = json.dumps(analyse(), indent=2) + '\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('layer refinement: enumeration, closure, constraint-map signature, orbits, cores, independent witnesses and artifact match passed')
    else:
        OUT.write_text(content)
        result = json.loads(content)
        for name, r in result['shapes'].items():
            print(name, 'w', r['layer_width'], 'raw', r['raw'], 'curve', r['refinement_counts'], 'stationary', r['stationary_refinement_counts'],
                  'classes', r['stationary_classes'], 'orbits', r['orbits'], 'horizons', r['horizon_classes'],
                  'core', r['core_classes'], 'robust', r['robust_core_classes'], 'on cycle', r['core_on_cycle'], 'traps', r['trap_classes'], 'walks', r['random_walks']['survived'], r['random_walks']['distinct_final_orbits'])
        print(json.dumps(result['existential_comparison'], indent=1))
