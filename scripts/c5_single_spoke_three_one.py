#!/usr/bin/env python3
"""Local controls for the arbitrary-size (3,1) exclusion proved in the report.

The skeletons are source-minor controls, not degree-list disk realizations.
Only this layer's artifact is written; predecessor evidence is read-only.
"""
import argparse
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_three_one/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)


def subsets(xs):
    return [frozenset(c) for n in range(len(xs) + 1)
            for c in combinations(sorted(xs), n)]


def covers_and_attachments():
    records = []
    for s in range(5):
        available = U - {Q[s]}
        found = []
        for f3, f1 in product(subsets(U), repeat=2):
            if (not f3 or len(f3) > 3 or len(f1) != 1
                    or f3 | f1 != available or not f3 - f1 or not f1 - f3):
                continue
            assert len(f3) == 2 and f3 == available - f1
            a, b = sorted(f3)
            rows = []
            for contact, support in product((False, True), subsets(range(5))):
                degree = 4 - len(support) - int(contact)
                if degree < 1:
                    continue
                external = [Q[i] for i in sorted(support)]
                ea = external + ([a] if contact else [])
                eb = external + ([b] if contact else [])
                if len(set(ea)) != len(ea) or len(set(eb)) != len(eb):
                    continue
                ma, mb = U - set(ea), U - set(eb)
                assert len(ma) == len(mb) == degree
                assert ma - mb == ({b} if contact else set())
                assert mb - ma == ({a} if contact else set())
                rows.append(dict(contact=contact, support=sorted(support),
                                 degree_in_C=degree, lists=[sorted(ma), sorted(mb)]))
            found.append(dict(spoke=s, bans=[sorted(f3), sorted(f1)],
                              tight_attachment_rows=rows))
        assert len(found) == 3
        records.extend(found)
    # Reflection transports the entire named assignment, including attachment
    # indices and the same two rejected colors. It does not identify contacts.
    lookup = {(r['spoke'], tuple(r['bans'][0]), tuple(r['bans'][1])): r
              for r in records}
    reflected = []
    for r in records:
        key = (RHO[r['spoke']], tuple(sorted(PI[c] for c in r['bans'][0])),
               tuple(sorted(PI[c] for c in r['bans'][1])))
        target = lookup[key]
        target_rows = {(x['contact'], tuple(x['support'])): x
                       for x in target['tight_attachment_rows']}
        reverse = PI[r['bans'][0][0]] > PI[r['bans'][0][1]]
        for row in r['tight_attachment_rows']:
            moved = [sorted(PI[c] for c in ls) for ls in row['lists']]
            if reverse:
                moved.reverse()
            actual = target_rows[(row['contact'], tuple(sorted(RHO[i] for i in row['support'])))]
            assert actual['lists'] == moved
        reflected.append(dict(source=[r['spoke'], r['bans']],
                              target=[target['spoke'], target['bans']]))
    return records, reflected


def local_incidence():
    palettes = [p for p in subsets(U) if len(p) in (1, 2)]
    records = []
    for a, b in permutations(range(4), 2):
        pairs = [(x, y) for x, y in product(palettes, repeat=2)
                 if len(x) == len(y) and x - {a, b} == y - {a, b}
                 and int(a in x) - int(a in y) == -(int(b in x) - int(b in y))]
        for count in range(1, 5):
            for ids in combinations_with_replacement(range(len(pairs)), count):
                ps = [pairs[i] for i in ids]
                degree = sum(len(x) for x, _ in ps)
                if degree > 4:
                    continue
                ma = frozenset().union(*(x for x, _ in ps))
                mb = frozenset().union(*(y for _, y in ps))
                if len(ma) != degree or len(mb) != degree:
                    continue
                if ma == mb:
                    kind = 'noncontact'
                elif ma - mb == {b} and mb - ma == {a} and degree <= 3:
                    kind = 'contact'
                else:
                    continue
                signs = [int(b in x) - int(b in y) for x, y in ps if x != y]
                assert sorted(signs) in ([[], [-1, 1]] if kind == 'noncontact' else [[1]])
                records.append(dict(rejected=[a, b], kind=kind,
                                    palettes=[[sorted(x), sorted(y)] for x, y in ps],
                                    active_signs=signs))
    return records


def edge(u, v):
    return tuple(sorted((u, v)))


def connected(group, edges):
    if not group:
        return False
    seen = {min(group)}
    while True:
        enlarged = seen | {v for u in seen for v in group if edge(u, v) in edges}
        if enlarged == seen:
            return seen == group
        seen = enlarged


def validate_minor(record):
    es = {tuple(e) for e in record['edges']}
    vertices = set().union(*(set(e) for e in es))
    groups = [set(g) for g in record['branch_sets']]
    if len(groups) != 5 or sum(map(len, groups)) != len(set().union(*groups)):
        return False
    if any(not g <= vertices or not connected(g, es) for g in groups):
        return False
    for i, j in combinations(range(5), 2):
        if not any(edge(u, v) in es for u in groups[i] for v in groups[j]):
            return False
    return True


def minor(s, lengths, subdivide, targets):
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    es.add(edge('z', f'b{s}'))  # Exactly one z-boundary spoke.
    es.update(edge(f'v{i}', f'v{j}') for i, j in combinations(range(3), 2))
    groups = [{'z'}] + [{f'v{i}'} for i in range(3)] + [{f'b{i}' for i in range(5)}]
    ports, arms, tethers = [], [], []
    for i, length in enumerate(lengths):
        arm = [f'v{i}'] + [f'a{i}_{j}' for j in range(1, length + 1)]
        es.update(edge(u, v) for u, v in zip(arm, arm[1:]))
        es.add(edge('z', arm[-1]))
        groups[i+1].update(arm)
        ports.append(arm[-1])
        arms.append(arm)
        tether = ([f'v{i}'] + ([f'w{i}_0', f'w{i}_1'] if subdivide[i] else [])
                  + [f'b{targets[i]}'])
        es.update(edge(u, v) for u, v in zip(tether, tether[1:]))
        groups[4].update(tether[1:-1])
        tethers.append(tether)
    # The fourth original z-contact remains in a separate component C1.
    # Its edges are present but not used in any of the five branch sets.
    singleton_path = ['z', 'd0', 'd1', f'b{(s+2)%5}']
    es.update(edge(u, v) for u, v in zip(singleton_path, singleton_path[1:]))
    record = dict(spoke=s, lengths=list(lengths), ports=ports, arms=arms,
                  tethers=tethers, singleton_contact='d0', singleton_path=singleton_path,
                  edges=sorted(es), branch_sets=[sorted(g) for g in groups])
    assert validate_minor(record)
    assert len(set(ports + ['d0'])) == 4
    assert {v if u == 'z' else u for u, v in es if 'z' in (u, v)} == set(ports + ['d0', f'b{s}'])
    assert not {'d0', 'd1'} & set().union(*groups)
    record['adjacency'] = [dict(pair=[i, j], edge=next(
        edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j]) if edge(u, v) in es))
        for i, j in combinations(range(5), 2)]
    return record


def negative_controls():
    base = minor(0, (0, 0, 0), (False,) * 3, (0, 0, 0))
    results = []
    failures = [('missing_spoke', [edge('z', 'b0')]),
                ('missing_original_contact', [edge('z', 'v0')]),
                ('missing_triangle_edge', [edge('v0', 'v1')]),
                ('missing_actual_tether', [edge('v0', 'b0')]),
                ('disconnected_boundary_hub', [edge('b1', 'b2'), edge('b2', 'b3')])]
    for name, removed in failures:
        damaged = dict(base, edges=[e for e in base['edges'] if e not in removed])
        assert not validate_minor(damaged)
        results.append(name)
    groups = [list(g) for g in base['branch_sets']]
    groups[1].append('z')
    assert not validate_minor(dict(base, branch_sets=groups))
    results.append('overlapping_branch_sets')
    groups = [list(g) for g in base['branch_sets']]
    groups[4].append('absent_vertex')
    assert not validate_minor(dict(base, branch_sets=groups))
    results.append('invented_hub_vertex')
    # A connected block tree on four contacts can have two active components:
    # the two end edges of a length-three path are active, its middle edge is
    # unchanged. Check full palettes/lists, rather than just the leaf count.
    blocks = [('u0', 'u1'), ('u1', 'u2'), ('u2', 'u3')]
    pa = [{1}, {2}, {1}]
    pb = [{0}, {2}, {0}]
    lists = []
    for v in ('u0', 'u1', 'u2', 'u3'):
        ids = [i for i, block in enumerate(blocks) if v in block]
        ma, mb = set().union(*(pa[i] for i in ids)), set().union(*(pb[i] for i in ids))
        assert len(ma) == len(mb) == len(ids)
        assert ma - mb == {1} and mb - ma == {0}
        lists.append([sorted(ma), sorted(mb)])
    active = [i for i in range(3) if pa[i] != pb[i]]
    assert active == [0, 2] and set(blocks[0]).isdisjoint(blocks[2])
    results.append(dict(name='four_contacts_allow_two_active_components',
                        blocks=blocks, palettes=[[sorted(x), sorted(y)] for x, y in zip(pa, pb)],
                        lists=lists, active_blocks=active,
                        scope='two-rejection abstract lists only; no three-rejection disk claim'))
    return results


def run():
    covers, reflection = covers_and_attachments()
    local = local_incidence()
    parity = []
    for lengths in product(range(8), repeat=3):
        signs = [sign for sign in (-1, 1)
                 if all(sign * (-1)**length == 1 for length in lengths)]
        assert bool(signs) == (len({length % 2 for length in lengths}) == 1)
        parity.append(dict(lengths=list(lengths), central_signs=signs))
    lengths = list(product((0, 2), repeat=3)) + [(1, 1, 1), (1, 3, 1)]
    minors = []
    for s, ls, bits, coincident in product(range(5), lengths, product((False, True), repeat=3), (False, True)):
        targets = (s, s, s) if coincident else tuple((s+i) % 5 for i in (1, 3, 4))
        minors.append(minor(s, ls, bits, targets))
    moved_minors = 0
    for r in minors:
        def move(v):
            return f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
        reflected = dict(r, edges=sorted(edge(move(u), move(v)) for u, v in r['edges']),
                         branch_sets=[[move(v) for v in g] for g in r['branch_sets']])
        assert validate_minor(reflected)
        # Boundary reflection leaves the named original contact identities.
        assert all(move(v) == v for v in r['ports'])
        moved_minors += 1
    negatives = negative_controls()
    inputs = ['scripts/c5_two_spoke_three_contacts.py',
              'artifacts/c5_two_spoke_three_contacts/observations.json',
              'scripts/c5_single_spoke_cores.py',
              'artifacts/c5_single_spoke_cores/observations.json']
    return dict(scope='paper arbitrary-size exclusion; finite local/minor controls only; no disk realization or Lean theorem',
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                covers=covers, reflected_covers=reflection, local_incidence=local,
                parity_controls=parity, minors=minors, negative_controls=negatives,
                summary=dict(covers=len(covers), tight_attachment_rows=sum(len(r['tight_attachment_rows']) for r in covers),
                             local_incidence_states=len(local), arm_parity_controls=len(parity),
                             one_spoke_K5_certificates=len(minors), reflected_minors=moved_minors,
                             negative_controls=len(negatives)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
