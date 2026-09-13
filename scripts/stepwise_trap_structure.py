#!/usr/bin/env python3
"""Obstruction / recovery map of the committed-colour strip layers (follow-up of §9j).

Same model as stepwise_layer_refinement (layer = w introduction steps, every introduced
vertex has a committed colour, action = legal next layer).  This script asks what the
irreversible classes I = Q \\ W_exists (dead + finite-horizon traps) look like, and how the
viable-but-not-robust classes R = W_exists \\ W_forall relate to the robust core.

1. Forced cone.  Propagate through the future layers: a vertex whose already-known lower
   neighbours cover 3 colours is forced to the fourth colour in every legal continuation;
   one whose known lower neighbours cover 4 colours is dead.  A configuration whose cone
   contains a dead vertex at layer t+k has horizon <= k-1 (sound).  On the nested fan-3
   strips the cone is exact: horizon == first dead layer - 1 for every stationary
   configuration, so I = {cone has a collision}.
2. Interior case splits.  Where the cone alone is not exact (fan-2 rows), branch on an
   interior vertex whose unknown lower neighbours are all boundary vertices, taking the
   over-approximated option set 4 \\ forbidden; every branch must die.  Boundary vertices
   are never branched on.  With this the certificate is exact on every shape below.
3. (3)^n trap schema.  Horizon-h traps of (3)^n are the unique rigid pattern P_h (the single
   horizon-h orbit of (3)^{h+2}, h+3 rows) placed on rows r-h-2..r, r in [h+2, n], the other
   n-h-2 rows free with 2 choices each: 24 (n-1-h) 2^{n-2-h} classes.  One step moves
   trap(h, r) to trap(h-1, r) (same dying vertex).  Horizon-1 traps are the "echo"
   R_{r-2}(t+1) = R_{r-1}(t), R_r(t+1) = R_{r-2}(t) of forced values.
4. Recovery map.  Q = W_forall + R + trap_h + dead; for R the branching numbers b, g,
   rho = g/b, and the backward basin of K = W_forall (d_K, g_K).  On (3)^n: R is closed
   under the repeat move b_{t+1} = b_{t-1}, the new move b_{t+1} = u_{t-2} always leaves
   W_exists, and R never re-enters W_forall.

Everything is computationally observed on the listed finite shapes; nothing here is a
claim about planar graphs in general or about the existential boundary residuals.
"""
from collections import Counter, deque
from itertools import permutations
import json
from pathlib import Path
import sys

from stepwise_layer_refinement import enumerate_model, refine, horizons

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/trap_structure.json'
PERMS = list(permutations(range(4)))
SHAPES = [((3,), 1), ((3, 3), 1), ((3, 3, 3), 1), ((3, 3, 3, 3), 1), ((3, 3, 3, 3, 3), 1),
          ((3, 3, 3, 3, 3, 3), 1), ((2, 3), 1), ((2, 2, 3), 1), ((3, 2, 3), 1),
          ((4,), 2), ((5,), 2), ((6,), 3), ((7,), 3), ((4, 4), 2), ((5, 5), 2), ((2, 4), 2),
          # new shapes: fan-2 rows between or under fan-3 rows, and fan 4 on top of fan 3
          ((2, 3, 3), 1), ((3, 3, 2), 1), ((3, 2, 3, 3), 1), ((3, 3, 2, 3), 1), ((2, 3, 3, 3), 1),
          ((2, 2, 3, 3), 1), ((3, 2, 2, 3), 1), ((3, 4), 2), ((4, 3), 2), ((3, 3, 4), 2),
          ((4, 3, 3), 2), ((3, 4, 3), 2), ((4, 4, 4), 2), ((2, 3, 4), 2), ((3, 2, 4), 2)]


def name(fans):
    return 'fans' + ''.join(map(str, fans))


def comp(a, b, c):
    """The fourth colour of three distinct ones."""
    assert len({a, b, c}) == 3
    return ({0, 1, 2, 3} - {a, b, c}).pop()


def canon(layers):
    return min(tuple(tuple(p[c] for c in layer) for layer in layers) for p in PERMS)


def committed(model, s):
    L, order = model['L'], model['order']
    t, prev, cur = order[s]
    known = dict(zip(L['layer_vertices'](t - 1), prev))
    known.update(zip(L['layer_vertices'](t), cur))
    return known


def forced_cone(model, s, K):
    """Forced colours of the next K layers and the list of (layer offset, vertex) deaths."""
    L, order = model['L'], model['order']
    t = order[s][0]
    known, deaths = committed(model, s), []
    for k in range(1, K + 1):
        for v in L['layer_vertices'](t + k):
            forb = {known[u] for u in L['lower'](v) if u in known}
            if len(forb) == 4:
                deaths.append((k, v))
            elif len(forb) == 3:
                known[v] = ({0, 1, 2, 3} - forb).pop()
    return known, deaths


def split_certificate(model, s, K):
    """Forced cone plus case splits on interior vertices (never on the boundary).

    Returns (k, splits): every branch is dead by layer t+k, using at most `splits` nested
    splits, or (None, splits) if some branch survives K layers.  Options of a split vertex
    are 4 minus the colours of its known lower neighbours (a superset of the true options,
    so a certified death is sound); a vertex is split only when its unknown lower
    neighbours are all boundary vertices.
    """
    L, order = model['L'], model['order']
    t = order[s][0]
    future = [(k, v) for k in range(1, K + 1) for v in L['layer_vertices'](t + k)]

    def rec(known, start, depth):
        known = dict(known)
        for i in range(start, len(future)):
            k, v = future[i]
            lows = L['lower'](v)
            forb = {known[u] for u in lows if u in known}
            if len(forb) == 4:
                return k, depth
            if len(forb) == 3:
                known[v] = ({0, 1, 2, 3} - forb).pop()
            elif v[0] >= 1 and all(u in known or u[0] == 0 for u in lows):
                worst, deepest = 0, depth
                for c in {0, 1, 2, 3} - forb:
                    known[v] = c
                    kk, dd = rec(known, i + 1, depth + 1)
                    if kk is None:
                        return None, dd
                    worst, deepest = max(worst, kk), max(deepest, dd)
                return worst, deepest
        return None, depth
    return rec(committed(model, s), 0, 0)


def class_graph(model):
    order, trans, ts = model['order'], model['trans'], model['ts']
    history, _ = refine(order, trans)
    part = history[-1]
    h = horizons(order, trans)
    stationary = [s for s in range(len(order)) if order[s][0] == ts]
    classes = sorted({part[s] for s in stationary})
    rep = {}
    for s in stationary:
        rep.setdefault(part[s], s)
    edges = {k: {} for k in classes}
    for s in stationary:
        for a, t in trans[s].items():
            edges[part[s]][a] = part[t]
    class_h = {part[s]: h[s] for s in stationary}
    dead = {k for k in classes if class_h[k] == 0}
    core = {k for k in classes if class_h[k] is None}
    safe = set(core)
    while True:
        shrunk = {k for k in safe if edges[k] and set(edges[k].values()) <= safe}
        if shrunk == safe:
            break
        safe = shrunk
    return dict(part=part, h=h, stationary=stationary, classes=classes, rep=rep, edges=edges,
                class_h=class_h, dead=dead, core=core, safe=safe)


def recovery_map(G):
    """b, g, rho for every viable class and the backward basin of K = W_forall."""
    edges, core, safe, classes = G['edges'], G['core'], G['safe'], G['classes']
    R = core - safe
    trap = {k for k in classes if k not in core and k not in G['dead']}
    b = {k: len(edges[k]) for k in classes}
    g = {k: sum(t in core for t in edges[k].values()) for k in classes}
    # backward basin of the robust core: d_K = fewest moves to enter W_forall
    d = {k: 0 for k in safe}
    frontier = set(safe)
    while frontier:
        nxt = set()
        for k in classes:
            if k not in d and any(t in frontier for t in edges[k].values()):
                nxt.add(k)
        for k in nxt:
            d[k] = 1 + min(d[t] for t in edges[k].values() if t in d)
        frontier = nxt
    gK = {k: sum(1 for t in edges[k].values() if t in d and d[t] == d[k] - 1) for k in d if d[k] > 0}
    rho = Counter(f'{g[k]}/{b[k]}' for k in R)
    return dict(counts=dict(robust=len(safe), viable_not_robust=len(R),
                            trap_by_horizon={str(h): c for h, c in sorted(Counter(G['class_h'][k] for k in trap).items())},
                            dead=len(G['dead'])),
                viable_not_robust=dict(branching={f'b={bb},g={gg}': c for (bb, gg), c in sorted(Counter((b[k], g[k]) for k in R).items())},
                                       rho=dict(sorted(rho.items())),
                                       d_K=dict(sorted(Counter(str(d.get(k, 'inf')) for k in R).items())),
                                       g_K={str(v): c for v, c in sorted(Counter(gK[k] for k in R if k in gK).items())}),
                robust_reachable_from_R=any(k in d for k in R))


def certificates(model, G):
    """Cone and split certificates against the true horizon, over stationary configurations."""
    stationary, h = G['stationary'], G['h']
    K = len(model['fans']) + 3
    cone_ok = Counter()
    split_ok, split_depth = Counter(), {}
    for s in stationary:
        _, deaths = forced_cone(model, s, K)
        pred = min(deaths)[0] - 1 if deaths else None
        cone_ok[pred == h[s]] += 1
        k, splits = split_certificate(model, s, K)
        pred2 = None if k is None else k - 1
        split_ok[pred2 == h[s]] += 1
        if pred2 is not None:
            split_depth.setdefault(pred2, set()).add(splits)
    return dict(lookahead_layers=K,
                cone_exact=not cone_ok[False], cone_mismatches=cone_ok[False],
                interior_split_exact=not split_ok[False], interior_split_mismatches=split_ok[False],
                splits_needed_by_horizon={str(k): sorted(v) for k, v in sorted(split_depth.items())})


def fan3_schema(models, graphs):
    """Trap schema of the nested fan-3 strips: rigid patterns P_h and their placements."""
    P = {}   # h -> canonical (h+3)-row pattern from (3)^{h+2}
    out = {}
    for n in range(2, 7):
        model, G = models[n], graphs[n]
        order, trans, L, ts = model['order'], model['trans'], model['L'], model['ts']
        part, h, stationary = G['part'], G['h'], G['stationary']
        groups = {}
        for s in stationary:
            if h[s] in (None, 0):
                continue
            known, deaths = forced_cone(model, s, n + 2)
            (k, v), = [d for d in deaths if d[0] == min(deaths)[0]]   # exactly one first death
            assert k - 1 == h[s]
            r = v[0]
            groups.setdefault((h[s], r), []).append(s)
            # both successors are traps of horizon h-1 (or dead); the same vertex still dies
            # first (stationary indices are clipped, so the successor's columns shift by one)
            for t in trans[s].values():
                assert h[t] == h[s] - 1
                _, d2 = forced_cone(model, t, n + 2)
                assert (k - 1, (r, v[1] - 1)) in d2 and min(d2)[0] == k - 1
        table = []
        for (hh, r), members in sorted(groups.items()):
            rows = list(range(r - hh - 2, r + 1))
            restricted = {canon([[order[s][1][q] for q in rows], [order[s][2][q] for q in rows]]) for s in members}
            assert len(restricted) == 1, 'the rows carrying the chain form one colour orbit'
            pattern = restricted.pop()
            if r == n and hh == n - 2:
                P[hh] = pattern
            assert pattern == P[hh], 'same rigid pattern P_h at every placement and depth'
            assert len({part[s] for s in members}) == len(members) == 24 * 2 ** (n - 2 - hh)
            table.append(dict(horizon=hh, death_row=r, rows_of_pattern=rows, classes=len(members),
                              orbits=len({canon([order[s][1], order[s][2]]) for s in members})))
        assert sorted({g[0] for g in groups}) == list(range(1, n - 1))
        for hh in range(1, n - 1):
            assert {g[1] for g in groups if g[0] == hh} == set(range(hh + 2, n + 1))
        # horizon-1 traps: echo of forced layer-(t+1) values against layer t
        echo = Counter()
        for s in stationary:
            known, deaths = forced_cone(model, s, n + 2)
            live = not any(k == 1 for k, _ in deaths)
            rows_hit = [r for r in range(3, n + 1)
                        if live and known[(r - 2, ts + 1 - 2 * (r - 2))] == known[(r - 1, ts - 2 * (r - 1))]
                        and known[(r, ts + 1 - 2 * r)] == known[(r - 2, ts - 2 * (r - 2))]]
            assert (h[s] == 1) == bool(rows_hit)
            if rows_hit:
                assert len(rows_hit) == 1 and groups[(1, rows_hit[0])].count(s) == 1
                echo[rows_hit[0]] += 1
        out[name((3,) * n)] = dict(placements=table, echo_rule_horizon1_by_row=dict(sorted(echo.items())),
                                   total_traps=sum(len(m) for m in groups.values()),
                                   law='24 (n-1-h) 2^(n-2-h) = sum over r in [h+2, n] of 24 2^(n-2-h)')
    # Shape of P_h (rows 0..h+2, columns = layers t-1, t): with row 0 = (A, B), the older
    # column alternates A, B, ..., up to row h+1 and is a third colour on top; the current
    # column is B on row 0, alternates over {C, D} on rows 1..h+1, and the top is forced.
    for hh, (prev, cur) in P.items():
        A, B = prev[0], cur[0]
        assert all(prev[r] == (A if r % 2 == 0 else B) for r in range(hh + 2)) and prev[hh + 2] not in (A, B)
        assert {cur[1], cur[2]} == {0, 1, 2, 3} - {A, B} and all(cur[r] == cur[r - 2] for r in range(3, hh + 2))
        assert cur[hh + 2] == comp(prev[hh + 1], cur[hh + 1], prev[hh + 2])
    patterns = {str(hh): dict(rows=len(p[0]), prev_layer=list(p[0]), current_layer=list(p[1]))
                for hh, p in sorted(P.items())}
    return dict(rigid_patterns=patterns, per_depth=out)


def fan333_readable_rule(model, G):
    """(3,3,3): explicit trap rule on x = (b_{t-1},u_{t-3},v_{t-5},w_{t-7}; b_t,u_{t-2},v_{t-4},w_{t-6})."""
    order, h = model['order'], G['h']
    fam = Counter()
    for s in G['stationary']:
        (b1, u1, v1, _), (b0, u0, v0, w0) = order[s][1], order[s][2]
        U = comp(b1, b0, u0)          # forced u_{t-1}
        V = comp(u1, u0, v0)          # forced v_{t-3}
        W = comp(v1, v0, w0)          # forced w_{t-5}
        live = U != V and V != W
        trap = live and U == v0 and W == u0
        assert (h[s] == 0) == (not live)
        assert (h[s] == 1) == trap
        fam['trap' if trap else 'dead' if not live else 'viable'] += 1
    return dict(forced='u_{t-1}=comp(b_{t-1},b_t,u_{t-2}), v_{t-3}=comp(u_{t-3},u_{t-2},v_{t-4}), w_{t-5}=comp(v_{t-5},v_{t-4},w_{t-6})',
                dead='u_{t-1}=v_{t-3} or v_{t-3}=w_{t-5}',
                trap='live and u_{t-1}=v_{t-4} and w_{t-5}=u_{t-2}  (then v_{t-2}=comp(u_{t-2},u_{t-1},v_{t-3}) equals the forced w_{t-4})',
                counts=dict(fam))


def fan3_moves(model, G):
    """Repeat / new move safety on (3)^n at class level."""
    order, edges, core, safe, rep = model['order'], G['edges'], G['core'], G['safe'], G['rep']
    tab = Counter()
    for k in core:
        s = rep[k]
        prev, cur = order[s][1], order[s][2]
        kinds = []
        for a, t in edges[k].items():
            assert a[0] in (prev[0], cur[1])
            kinds.append(('repeat' if a[0] == prev[0] else 'new', 'robust' if t in safe else 'R' if t in core else 'I'))
        tab[('robust' if k in safe else 'R', tuple(sorted(kinds)))] += 1
    assert set(tab) == {('robust', (('new', 'robust'), ('repeat', 'robust'))), ('R', (('new', 'I'), ('repeat', 'R')))}
    return {f'{a}: ' + ', '.join(f'{m}->{d}' for m, d in ks): c for (a, ks), c in sorted(tab.items())}


def analyse():
    shapes, models, graphs = {}, {}, {}
    for fans, w in SHAPES:
        model = enumerate_model(fans, w)
        G = class_graph(model)
        shapes[name(fans)] = dict(fans=fans, layer_width=w, classes=len(G['classes']),
                                  recovery=recovery_map(G), certificates=certificates(model, G))
        if set(fans) == {3}:
            models[len(fans)], graphs[len(fans)] = model, G
            if len(fans) >= 2:
                shapes[name(fans)]['moves'] = fan3_moves(model, G)
    for r in shapes.values():
        assert r['certificates']['interior_split_exact']
    assert all(shapes[name((3,) * n)]['certificates']['cone_exact'] for n in range(1, 7))
    return dict(status='computationally observed; committed-colour strip layers (§9j model); not Lean, not planar graphs in general',
                certificate='forced cone (3 known lower colours force, 4 kill) is exact on (3)^n; with case splits on interior vertices only it is exact on every listed shape; boundary vertices are never split',
                nested_fan3=dict(schema=fan3_schema(models, graphs),
                                 fans333_rule=fan333_readable_rule(models[3], graphs[3])),
                shapes=shapes)


if __name__ == '__main__':
    content = json.dumps(analyse(), indent=2) + '\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('trap structure: certificates, (3)^n schema, readable rules, recovery map and artifact match passed')
    else:
        OUT.write_text(content)
        result = json.loads(content)
        for nm, r in result['shapes'].items():
            c, rec = r['certificates'], r['recovery']
            print(nm, 'classes', r['classes'], 'cone exact', c['cone_exact'], 'splits', c['splits_needed_by_horizon'],
                  'map', rec['counts'], 'R rho', rec['viable_not_robust']['rho'], 'd_K', rec['viable_not_robust']['d_K'])
        for nm, r in result['nested_fan3']['schema']['per_depth'].items():
            print(nm, [(p['horizon'], p['death_row'], p['classes'], p['orbits']) for p in r['placements']], r['echo_rule_horizon1_by_row'])
        print(json.dumps(result['nested_fan3']['schema']['rigid_patterns'], indent=1))
