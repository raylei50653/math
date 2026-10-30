#!/usr/bin/env python3
"""Same-source controls for the two-return difference separator audit.

This producer retains complete literal ABACD fibres, every full-O component
action in the whole common-S4 quotient class, and the actual prescribed
exchanges.  The legal source is a two-return prefix, not a period-four or
fully blocked counterexample.  Errera is expressly an S5-negative control.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audits/2026-10-30-c5-d2-separation/controls.json'
INPUT = ROOT / 'audits/2026-10-30-c5-period4-s5/search-inputs/n17.ascii'
OLD = ROOT / 'audits/2026-10-29-kempe-realizability/source/controls.json'
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
ROOT_POSITIONS = (2, 4, 1, 3, 0)
FRAME = (0, 1, 0, 2, 3)
ALIGN = (2, 3, 1, 0)


def parts(adj, allowed):
    unseen, ans = set(allowed), []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo = [first]
        for u in todo:
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                todo.append(v)
        ans.append(tuple(sorted(todo)))
    return sorted(ans)


def canonical(c):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in c)


def faces_of(rotation):
    unseen = {(u, v) for u, row in enumerate(rotation) for v in row}
    faces = []
    while unseen:
        u, v = first = min(unseen)
        f = []
        while True:
            unseen.remove((u, v))
            f.append(u)
            row = rotation[v]
            u, v = v, row[(row.index(u) - 1) % len(row)]
            if (u, v) == first:
                break
        assert len(f) == len(set(f)) == 3
        faces.append(f)
    assert len(rotation) - sum(map(len, rotation)) // 2 + len(faces) == 2
    return faces


def rotation_of(n, faces):
    links = defaultdict(dict)
    for f in faces:
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            links[a][c] = b
    rotation = []
    for v in range(n):
        start, row = min(links[v]), []
        w = start
        while w not in row:
            row.append(w)
            w = links[v][w]
        assert w == start and set(row) == set(links[v])
        rotation.append(row)
    return rotation


def topology(rotation, faces):
    """Independent vertex-deletion check for every original short cycle."""
    adj = list(map(set, rotation))
    short, bad34, bad5 = [], [], []
    for first in range(len(adj)):
        def visit(path):
            u = path[-1]
            if len(path) >= 3 and first in adj[u] and path[1] < u:
                # In a triangulation a chorded short cycle has an empty
                # side unless a shorter separating cycle already fails S34.
                components = parts(adj, set(range(len(adj))) - set(path))
                if len(components) > 1:
                    row = dict(cycle=path, deletion_components=components)
                    short.append(row)
                    if len(path) < 5:
                        bad34.append(row)
                    elif min(map(len, components)) > 1:
                        bad5.append(row)
            if len(path) < 5:
                for v in sorted(adj[u]):
                    if v > first and v not in path:
                        visit(path + [v])
        visit([first])
    return dict(S34=not bad34, S5=not bad5,
                minimum_degree5=min(map(len, rotation)) >= 5,
                short_separators=short, forbidden34=bad34, forbidden5=bad5)


def all_fibre(adj, order, boundary):
    ix = {v: j for j, v in enumerate(order)}
    c = [-1] * len(order)
    for v, color in zip(boundary, FRAME):
        c[ix[v]] = color
    answer = []
    def visit():
        todo = [v for v in order if c[ix[v]] < 0]
        if not todo:
            answer.append(tuple(c))
            return
        domains = {v: set(range(4)) - {c[ix[w]] for w in adj[v]} for v in todo}
        v = min(todo, key=lambda v: (len(domains[v]), -len(adj[v]), v))
        for color in sorted(domains[v]):
            c[ix[v]] = color
            visit()
        c[ix[v]] = -1
    visit()
    return sorted(answer)


def actual_round(adj, order, boundary, colors):
    ix = {v: j for j, v in enumerate(order)}
    c, moves = tuple(colors), []
    assert tuple(c[ix[v]] for v in boundary) == FRAME
    for pair, k in zip(PAIRS, ROOT_POSITIONS):
        root = boundary[k]
        comp = next(p for p in parts(adj, [v for v in order if c[ix[v]] in pair]) if root in p)
        hit = sorted(set(comp) & set(boundary))
        c = tuple(sum(pair) - x if v in comp else x for v, x in zip(order, c))
        assert all(c[ix[u]] != c[ix[v]] for u in order for v in adj[u])
        moves.append(dict(pair=pair, root=root, component=comp, colors=c,
                          boundary_intersection=hit))
        if hit != [root]:
            return None, dict(source_colors=colors, moves=moves,
                              defined=False, failure='component-boundary-intersection-not-single-root')
    target = tuple(ALIGN[x] for x in c)
    assert tuple(target[ix[v]] for v in boundary) == FRAME
    return target, dict(source_colors=colors, moves=moves,
                        defined=True, normalized_colors=target)


def complete_class(adj, order, boundary, start):
    ix = {v: j for j, v in enumerate(order)}
    first = canonical(start)
    states, ids, previous, via, actions = [first], {first: 0}, [None], [None], []
    extending = []
    for sid, c in enumerate(states):
        if len({c[ix[v]] for v in boundary}) == 3:
            extending.append(sid)
        rows = []
        for pair in combinations(range(4), 2):
            for comp in parts(adj, [v for v in order if c[ix[v]] in pair]):
                raw = tuple(sum(pair) - x if v in comp else x for v, x in zip(order, c))
                target = canonical(raw)
                tid = ids.get(target)
                action = dict(pair=pair, component=comp)
                if tid is None:
                    tid = len(states)
                    ids[target] = tid
                    states.append(target)
                    previous.append(sid)
                    via.append(action)
                rows.append(dict(target=tid, **action))
        actions.append(rows)
    escape = []
    if extending:
        q = extending[0]
        while previous[q] is not None:
            escape.append(dict(source=previous[q], target=q, **via[q]))
            q = previous[q]
        escape.reverse()
    assert all(len(set(c)) == 4 for c in states)
    return dict(normalized_states=states, all_actual_component_actions=actions,
        normalized_size=len(states), literal_size=24 * len(states),
        extending_state_ids=extending, blocked=not extending,
        all_six_pairs_all_components_complete=True, escape_quotient_route=escape,
        quotient_contract='One common global S4 permutation; all 24 literal lifts of each state. Every global transposition is realized by swapping all its actual components, so the full quotient closure lifts to the whole literal class.')


def full_boundary_fibres(adj, order, boundary, klass):
    """Directly enumerate all proper O colorings, then certify every B fibre.

    Quotient-state/permutation references encode whole complete colorings;
    one permutation acts on every original exterior vertex simultaneously.
    """
    ix = {v: j for j, v in enumerate(order)}
    c, direct = [-1] * len(order), []
    def visit():
        todo = [v for v in order if c[ix[v]] < 0]
        if not todo:
            direct.append(tuple(c))
            return
        domains = {v: set(range(4)) - {c[ix[w]] for w in adj[v]} for v in todo}
        v = min(todo, key=lambda v: (len(domains[v]), -len(adj[v]), v))
        for color in sorted(domains[v]):
            c[ix[v]] = color
            visit()
        c[ix[v]] = -1
    visit()
    direct.sort()
    proper_words = [word for word in product(range(4), repeat=5)
                    if all(word[i] != word[(i + 1) % 5] for i in range(5))]
    assert len(proper_words) == 240
    fibres = {word: [] for word in proper_words}
    lifted = {}
    for sid, state in enumerate(klass['normalized_states']):
        for perm in permutations(range(4)):
            colors = tuple(perm[x] for x in state)
            assert colors not in lifted
            ref = dict(normalized_state=sid, global_permutation=perm)
            lifted[colors] = ref
    assert set(direct) == set(lifted)
    for colors in direct:
        word = tuple(colors[ix[v]] for v in boundary)
        fibres[word].append(lifted[colors])
    digest = sha256(json.dumps(direct, separators=(',', ':')).encode()).hexdigest()
    return dict(proper_boundary_words=240,
        rows=[dict(boundary_word=word, complete_lifts=fibres[word]) for word in proper_words],
        empty_proper_boundary_fibres=sum(not fibres[word] for word in proper_words),
        full_original_edge_enumeration_count=len(direct),
        full_original_edge_enumeration_sha256=digest,
        class_lifts_sha256=sha256(json.dumps(sorted(lifted), separators=(',', ':')).encode()).hexdigest(),
        original_edge_enumeration_equals_class_lifts=True,
        all_proper_colorings_in_single_kempe_component=True,
        nonproper_boundary_words=4 ** 5 - 240,
        nonproper_boundary_fibres_empty_by_original_B_edges=True,
        contract='Every proper original B word, including empty fibres, is listed. Each lift is one whole quotient state under one common S4 permutation applied simultaneously to every original exterior vertex. These lifts equal direct unrestricted original-edge enumeration; no endpoint projections are composed.')


def retain(name, scope, rotation, faces, center, boundary, order, iterates,
           rounds, comparisons, **extra):
    n = len(rotation)
    adj = {v: set(rotation[v]) - {center} for v in order}
    edges = [(u, v) for u, row in enumerate(rotation) for v in row if u < v]
    fib = all_fibre(adj, order, boundary)
    assert all(tuple(c) in fib for c in iterates)
    klass = complete_class(adj, order, boundary, iterates[0])
    geo = topology(rotation, faces)
    period4 = (len(iterates) == 4 and len(set(map(tuple, iterates))) == 4
               and rounds[-1]['normalized_colors'] == iterates[0])
    return dict(name=name, scope=scope, n=n, original_edges=edges,
        sphere_faces=faces, rotation=rotation, center=center, boundary=boundary,
        exterior_vertices=order, exterior_edges=[e for e in edges if center not in e],
        complete_ABACD_fibre=fib, normalized_iterates=iterates, rounds=rounds,
        full_kempe_component=klass,
        full_boundary_fibres=full_boundary_fibres(adj, order, boundary, klass), topology=geo,
        premise_flags=dict(S34=geo['S34'], S5=geo['S5'],
            minimum_degree5=geo['minimum_degree5'], fully_blocked=klass['blocked'],
            least_h_period4=period4), comparisons=comparisons, **extra)


def produce():
    # Concrete saved original graph, not an abstract boundary relation.
    line = INPUT.read_text().splitlines()[0]
    n, raw = line.split()
    rotation = [[ord(x) - ord('a') for x in row] for row in raw.split(',')]
    assert len(rotation) == int(n) == 17
    faces, center = faces_of(rotation), 2
    boundary = rotation[center]
    order = boundary + sorted(set(range(17)) - set(boundary) - {center})
    adj = {v: set(rotation[v]) - {center} for v in order}
    fib = all_fibre(adj, order, boundary)
    for c in fib:
        d, r0 = actual_round(adj, order, boundary, c)
        if d is None:
            continue
        e, r1 = actual_round(adj, order, boundary, d)
        if e is not None and e != c:
            break
    else:
        raise AssertionError('frozen two-return witness disappeared')
    target, failed = actual_round(adj, order, boundary, e)
    assert target is None and len(failed['moves']) == 3
    prefix = retain('LEGAL-S5-SIX-ATTACHMENT-TWO-RETURN-PREFIX',
        'Legal S34/S5 sphere and two actual prescribed full-O returns. No third return, no period four, and the full class is not blocked. This refutes only the stronger claim that a nonempty two-return difference must have a fixed separating C5 without blockedness/period-four premises.',
        rotation, faces, center, boundary, order, [c, d, e], [r0, r1],
        [dict(source_iterate=0, target_iterate=2, c=c, d=e)],
        source_record=dict(input=str(INPUT.relative_to(ROOT)), zero_based_graph=0,
                           original_ascii_line=line), failed_next_round=failed)
    assert all(prefix['premise_flags'][key] for key in ('S34', 'S5', 'minimum_degree5'))
    assert not prefix['premise_flags']['fully_blocked']
    changed = {v for v, x, y in zip(order, c, e) if x != y}
    assert changed == {12, 16}
    assert set().union(*(adj[v] for v in changed)) - changed == {5, 6, 10, 11, 13, 15}

    old = json.loads(OLD.read_text())['controls'][0]
    n = old['deleted_vertex'] + 1
    center, faces = old['deleted_vertex'], old['sphere_faces']
    rotation = rotation_of(n, faces)
    order, boundary = list(range(n - 1)), old['boundary']
    adj = {v: set(rotation[v]) - {center} for v in order}
    iterates = [tuple(old['normalized_colorings'][sid]) for sid in old['H_cycles'][0]]
    rounds = []
    for i, c in enumerate(iterates):
        target, row = actual_round(adj, order, boundary, c)
        assert target == iterates[(i + 1) % 4]
        rounds.append(row)
    errera = retain('ERRERA-S5-NEGATIVE-PERIOD4',
        'Actual least period-four full-O orbit; S34 and minimum degree five hold, S5 fails, and the full Kempe class is not blocked. Never a legal S5 or fully blocked period-four counterexample.',
        rotation, faces, center, boundary, order, iterates, rounds,
        [dict(source_iterate=i, target_iterate=(i + 2) % 4,
              c=iterates[i], d=iterates[(i + 2) % 4]) for i in range(4)])
    assert not errera['premise_flags']['S5']
    assert errera['premise_flags']['least_h_period4']
    assert not errera['premise_flags']['fully_blocked']
    return dict(schema='c5-d2-same-source-controls-v1',
        provenance_inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                           for p in (INPUT, OLD)},
        evidence='Exact finite concrete-source controls. No legal fully blocked period-four witness is claimed.',
        controls=[prefix, errera])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = produce()
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='CHECK OK' if args.check else 'CREATED',
        controls=[dict(name=r['name'], fibre=len(r['complete_ABACD_fibre']),
                      kempe_quotient=r['full_kempe_component']['normalized_size'],
                      premises=r['premise_flags']) for r in result['controls']]), sort_keys=True))


if __name__ == '__main__':
    main()
