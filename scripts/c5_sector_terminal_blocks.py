#!/usr/bin/env python3
"""Two-row terminal block interfaces and boundary-aware topology certificates."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_terminal_blocks/observations.json'
UP = ROOT / 'artifacts/c5_sector_rejection_lists/observations.json'
U = frozenset(range(4))
ROWS = ((0, 1, 2, 1, 2), (0, 1, 2, 1, 3))


def lists(attachments, row):
    return [U - {row[int(i)] for i in ns} for ns in attachments]


def cycle_root(private):
    result = set()
    for c in U:
        possible = {c}
        for ls in private:
            possible = {d for d in ls if possible - {d}}
        if possible - {c}:
            result.add(c)
    return result


def brute_root(private, clique=False):
    result = set()
    for values in product(U, *private):
        edges = combinations(range(len(values)), 2) if clique else (
            (i, (i+1) % len(values)) for i in range(len(values)))
        if all(values[a] != values[b] for a, b in edges):
            result.add(values[0])
    return result


def edge(a, b):
    return tuple(sorted((str(a), str(b))))


def template(kind, attachments, root_attachment=()):
    private = [f'v{i}' for i in range(len(attachments))]
    vertices = ['x'] + private
    es = {edge(i, (i+1) % 5) for i in range(5)}
    es |= {edge('z', i) for i in range(5)}  # exterior apex, only for disk tests
    if kind == 'K4':
        es |= {edge(a, b) for a, b in combinations(vertices, 2)}
    else:
        es |= {edge(vertices[i], vertices[(i+1) % len(vertices)])
               for i in range(len(vertices))}
    es |= {edge(v, i) for v, ns in zip(private, attachments) for i in ns}
    es |= {edge('x', i) for i in root_attachment}
    # A model of a path through the remainder to frame 0; not a sector realization.
    es |= {edge('x', 't'), edge('t', '0')}
    return es


def connected(vertices, es):
    vertices = set(vertices)
    if not vertices:
        return False
    seen = {next(iter(vertices))}
    while True:
        new = seen | {v for a, b in es for u, v in ((a, b), (b, a))
                      if u in seen and v in vertices}
        if new == seen:
            return seen == vertices
        seen = new


def verify_minor(es, groups, target):
    groups = [set(g) for g in groups]
    assert all(connected(g, es) for g in groups)
    assert sum(map(len, groups)) == len(set().union(*groups))
    assert all(not {'2', '4'} <= g for g in groups)
    pairs = combinations(range(5), 2) if target == 'K5' else product(range(3), range(3, 6))
    for i, j in pairs:
        assert any(edge(a, b) in es for a in groups[i] for b in groups[j]), (i, j)


def minor_case(name, es, groups, target):
    verify_minor(es, groups, target)
    return dict(name=name, edges=sorted(es), branch_sets=[sorted(g) for g in groups], target=target)


def verify_rotation(es, rotation):
    rotation = {v: list(ns) for v, ns in rotation.items()}
    vertices = {v for e in es for v in e}
    assert set(rotation) == vertices
    for v in vertices:
        assert len(rotation[v]) == len(set(rotation[v]))
        assert set(rotation[v]) == {b if a == v else a for a, b in es if v in (a, b)}
    unseen = {(a, b) for a, b in es} | {(b, a) for a, b in es}
    faces = 0
    while unseen:
        start = next(iter(unseen))
        dart = start
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            ns = rotation[b]
            dart = (b, ns[(ns.index(a)-1) % len(ns)])
            if dart == start:
                break
        faces += 1
    assert connected(vertices, es) and len(vertices)-len(es)+faces == 2


def subdivision(es):
    # Generation only. Replay checks the saved source paths without an oracle.
    import networkx as nx
    graph = nx.Graph()
    graph.add_edges_from(sorted(es))
    sub = nx.algorithms.planarity.get_counterexample(graph)
    branch = sorted(v for v in sub if sub.degree(v) != 2)
    paths, used = [], set()
    for v in branch:
        for w in sorted(sub[v]):
            if edge(v, w) in used:
                continue
            path = [v, w]
            used.add(edge(v, w))
            while path[-1] not in branch:
                prev, cur = path[-2:]
                nxt = next(t for t in sub[cur] if t != prev)
                used.add(edge(cur, nxt))
                path.append(nxt)
            paths.append(path)
    return paths


def verify_subdivision(es, paths):
    ends, interiors, reduced = set(), set(), set()
    for path in paths:
        assert len(path) >= 2 and len(path) == len(set(path))
        assert all(edge(a, b) in es for a, b in zip(path, path[1:]))
        assert not interiors.intersection(path[1:-1])
        interiors.update(path[1:-1])
        ends.update((path[0], path[-1]))
        e = edge(path[0], path[-1])
        assert e not in reduced
        reduced.add(e)
    assert not ends.intersection(interiors)
    if len(ends) == 5:
        assert len(reduced) == 10
    else:
        assert len(ends) == 6 and len(reduced) == 9
        assert any(all(edge(a, b) in reduced for a in part for b in ends-set(part))
                   for part in combinations(ends, 3))


def bridge_control(length):
    """Actual attachments and exhaustive list coloring, with the bridge path retained."""
    vertices = ['x','u','v','y','a','d'] + [f'p{i}' for i in range(length-1)]
    path = ['x'] + vertices[6:] + ['y']
    es = {edge('x','u'),edge('u','v'),edge('v','x'),
          edge('y','a'),edge('a','d'),edge('d','y')}
    es |= {edge(a,b) for a,b in zip(path,path[1:])}
    aa = {'x':(1,), 'y':(1,), 'u':(1,2), 'a':(1,2), 'v':(2,3), 'd':(2,3)}
    aa.update({v:(0,3) for v in path[1:-1]})
    assert all(sum(v in e for e in es)+len(aa[v]) == 4 for v in vertices)
    witnesses = []
    for row in ROWS:
        ls = {v:lists([aa[v]],row)[0] for v in vertices}
        solution = None
        for values in product(*(ls[v] for v in vertices)):
            colors = dict(zip(vertices,values))
            if all(colors[a] != colors[b] for a,b in es):
                solution = colors
                break
        assert (solution is not None) == (length % 2 == 0)
        # Independent message propagation along every retained bridge.
        available = {2}
        for v in path[1:]:
            allowed = {2} if v == 'y' else ls[v]
            available = {c for c in allowed if available-{c}}
        assert bool(available) == (solution is not None)
        witnesses.append(solution)
    return dict(bridge_length=length, inner_edges=sorted(es), attachments=aa,
                colorings=witnesses,
                scope='List and bridge control only; not disk, no named w,b or sector transition.')


def build(saved=None):
    upstream = json.loads(UP.read_text())
    for name, digest in upstream['input_sha256'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    pairs = list(map(frozenset, combinations(U, 2)))
    counts = {}
    for length in (3, 5, 7):
        histogram = {2: 0, 3: 0, 4: 0}
        for seq in product(pairs, repeat=length-1):
            available = cycle_root(seq)
            if length <= 5:
                assert available == brute_root(seq)
            common = all(ls == seq[0] for ls in seq)
            assert (len(available) == 2) == common
            if common:
                assert available == U-seq[0]
            histogram[len(available)] += 1
        counts[str(length)] = histogram
    triples = list(map(frozenset, combinations(U, 3)))
    for seq in product(triples, repeat=3):
        available = brute_root(seq, True)
        assert available == (U-seq[0] if len(set(seq)) == 1 else U)
    # Enumerate actual attachments, not independently chosen row lists.
    actual = [tuple(e['boundary_neighbors']) for e in upstream['entries']
              if e['both_tight'] and e['inner_degree'] == 2]
    groups = {}
    for ns in actual:
        key = tuple(tuple(sorted(ls)) for ls in lists([ns], ROWS[0])+lists([ns], ROWS[1]))
        groups.setdefault(key, []).append(ns)
    assert len(groups) == 5
    interfaces = []
    for j in (2, 4):
        palettes = [sorted(U-{row[1], row[j]}) for row in ROWS]
        roots = []
        for ns in [()] + [(i,) for i in range(5)]:
            ls = [lists([ns], row)[0] for row in ROWS]
            if all(set(p) <= l for p, l in zip(palettes, ls)):
                roots.append(dict(attachments=ns, available=[sorted(l-set(p)) for l, p in zip(ls, palettes)]))
        interfaces.append(dict(common_frame=j, private_attachments=[[1, j], [3, j]],
                               forbidden=palettes, algebraic_roots=roots))
    controls = []
    for name, aa in (
        ('same_alpha_but_delta_single_forbidden', [(1,2),(1,2),(1,4),(1,4)]),
        ('same_pointwise_multiset_different_order', [(1,2),(1,4),(1,2),(1,4)]),
    ):
        row_lists = [lists(aa, row) for row in ROWS]
        roots = [sorted(brute_root(ls)) for ls in row_lists]
        assert all(set(r) == cycle_root(ls) for r, ls in zip(roots, row_lists))
        controls.append(dict(name=name, private_attachments=aa,
                             lists=[[sorted(l) for l in ls] for ls in row_lists], root_available=roots))
    assert controls[0]['root_available'] == [[1,2], [1,2,3]]
    assert controls[1]['root_available'] == [[1,2], [0,1,2,3]]
    minors = []
    # Arbitrarily long cycle proof has three connected cycle branch sets.
    for length in (5, 7):
        for j in (2, 4):
            for choices in product((1,3), repeat=length-1):
                aa = [(i,j) for i in choices]
                es = template('cycle', aa)
                groups0 = [{'v0'}, {'v1'}, {'x'} | {f'v{i}' for i in range(2,length-1)},
                           {str(j)}, {'z','1','3'}]
                minors.append(minor_case(f'C{length}-{j}-{choices}', es, groups0, 'K5'))
    for j in (2, 4):
        for i in (1, 3):
            es = template('cycle', [(i,j),(i,j)])
            minors.append(minor_case(f'triangle-same-{i}-{j}', es,
                          [{'v0'}, {'v1'}, {'z','0','t'}, {str(i)}, {str(j)}, {'x'}], 'K33'))
    for aa in product(range(1,5), repeat=3):
        ls = [[row[a] for a in aa] for row in ROWS]
        if not all(len(set(colors)) == 1 for colors in ls):
            continue
        es = template('K4', [(a,) for a in aa])
        minors.append(minor_case(f'K4-{aa}', es,
                      [{'x'}, {'v0'}, {'v1'}, {'v2'}, {'z','0','t'} | set(map(str,aa))], 'K5'))
    # A root spoke to the common frame also fails the disk condition.
    for j in (2, 4):
        es = template('cycle', [(1,j),(3,j)], (j,))
        minors.append(minor_case(f'root-spoke-{j}', es,
                      [{'x'}, {'v0'}, {'v1'}, {str(j)}, {'z','0','1','3','t'}], 'K5'))
    es = template('cycle', [(1,2),(3,2)])
    # Two vertex-disjoint terminal triangles; bridges between them need not be contracted.
    es |= {edge('y', 'a'), edge('a', 'd'), edge('d','y'), edge('a','1'),
           edge('a','2'), edge('d','2'), edge('d','3')}
    minors.append(minor_case('two-disjoint-terminal-triangles', es,
                  [{'x','v0','v1'}, {'y','a','d'}, {'z'}, {'1'}, {'2'}, {'3'}], 'K33'))
    mixed4 = template('cycle', [(1,4),(3,4)])
    paths = saved['mixed4']['paths'] if saved else subdivision(mixed4)
    verify_subdivision(mixed4, paths)
    # Local disk controls: a single surviving terminal triangle can be embedded.
    local = []
    for ns in ((), (1,), (3,)):
        es = template('cycle', [(1,2),(3,2)], ns)
        if saved:
            rot = saved['local_disk_controls'][len(local)]['rotation']
        else:
            import networkx as nx
            graph = nx.Graph()
            graph.add_edges_from(sorted(es))
            ok, embedding = nx.check_planarity(graph)
            assert ok
            rot = {v: list(embedding.neighbors_cw_order(v)) for v in sorted(graph)}
        verify_rotation(es, rot)
        local.append(dict(root_attachment=ns, edges=sorted(es), rotation=rot,
                          scope='Partial local topology only; t and the remainder are not degree-completed.'))
    # With x adjacent to w and only one other-block edge, use the old coloring
    # to check which named root can reach its required frame in J=G-{0,w}.
    named = []
    old = (0,1,0,2,1)
    for name, color, target in (('p',2,3), ('q',3,1), ('r',3,4)):
        for ns in ((1,), (3,)):
            successes = []
            for cu, cv in product(U, repeat=2):
                cs = {str(i): old[i] for i in range(5)} | {'x':color,'v0':cu,'v1':cv}
                es = template('cycle', [(1,2),(3,2)], ns)
                es = {e for e in es if all(v in cs for v in e)}
                if not all(cs[a] != cs[b] for a,b in es):
                    continue
                # v1 is in S via frame 2; v0 has color 3 for p, color 2 for q/r.
                if name == 'p':
                    assert (cu,cv) == (3,1)
                    successes.append([cu,cv])  # x-v1-3 is the new 02 path.
                else:
                    allowed = {v for v in cs if cs[v] in (1,3)}
                    seen = {'x'}
                    while True:
                        new = seen | {v for a,b in es for u,v in ((a,b),(b,a)) if u in seen and v in allowed}
                        if new == seen:
                            break
                        seen = new
                    if str(target) in seen and (name != 'r' or '1' not in seen):
                        successes.append([cu,cv])
            named.append(dict(name=name, root_attachment=ns, local_colorings=successes))
    assert [bool(n['local_colorings']) for n in named] == [True,False,True,False,False,False]
    inputs = {UP, Path(__file__).resolve()} | {ROOT/name for name in upstream['input_sha256']}
    return dict(schema=1, scope='Nonempty 3903 branch only; paper proof plus finite local controls, not Lean.',
                input_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                rows=ROWS, cycle_histograms=counts,
                attachment_groups=[dict(lists=k, attachments=v) for k,v in groups.items()],
                interfaces=interfaces, reverse_controls=controls, minors=minors,
                mixed4=dict(edges=sorted(mixed4),paths=paths), local_disk_controls=local,
                named_bridge_root_controls=named,
                bridge_controls=[bridge_control(n) for n in range(1,6)],
                summary=dict(cycle_list_inputs=sum(sum(v.values()) for v in counts.values()),
                             k4_list_inputs=64, topology_minors=len(minors),
                             topology_subdivisions=1, local_disk_controls=len(local),
                             named_bridge_root_cases=len(named), bridge_controls=5, inherited_profiles=603,
                             profile_deletions=0, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = build(saved)
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
