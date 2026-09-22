#!/usr/bin/env python3
"""Local three-row tables and explicit minors for the 3703 structural reduction.

No graph generator or planarity oracle. Arbitrary-size conclusions are proved
in docs/c5_sector_3703_structure.md, not inferred from these finite controls.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_3703_structure/observations.json'
ROWS = ['01012', '01021', '01023', '01201', '01202', '01203',
        '01212', '01213', '01231', '01232', '00102', '01210']
REJECT = [3, 7, 8]
U = set(range(4))


def available(a, row):
    return U - {int(row[b]) for b in a}


def joint(a):
    return tuple(tuple(sorted(available(a, ROWS[i]))) for i in REJECT)


def edge(a, b):
    return tuple(sorted((str(a), str(b))))


def frame():
    return {edge(i, (i+1) % 5) for i in range(5)} | {edge('h', i) for i in range(5)}


def minor(name, es, groups, target):
    groups = [set(map(str, g)) for g in groups]
    assert sum(map(len, groups)) == len(set().union(*groups))
    vertices = {v for e in es for v in e}
    for group in groups:
        assert group and group <= vertices
        reached = {min(group)}
        while True:
            enlarged = reached | {v for a, b in es for u, v in [(a, b), (b, a)]
                                  if u in reached and v in group}
            if enlarged == reached:
                break
            reached = enlarged
        assert reached == group
    pairs = combinations(range(5), 2) if target == 'K5' else product(range(3), range(3, 6))
    for i, j in pairs:
        assert any(edge(a, b) in es for a in groups[i] for b in groups[j])
    return dict(name=name, target=target, edges=sorted(es),
                branch_sets=[sorted(g) for g in groups])


def root_colors(private, clique=False):
    result = set()
    if clique:
        for values in product(range(4), *private):
            if len(set(values)) == len(values):
                result.add(values[0])
        return result
    for c in range(4):
        possible = {c}
        for ls in private:
            possible = {d for d in ls if possible - {d}}
        if possible - {c}:
            result.add(c)
    return result


def audit():
    tight = {n: [a for a in combinations(range(5), n)
                 if all(len(available(a, ROWS[i])) == 4-n for i in REJECT)]
             for n in range(6)}
    assert tight[2] == [(0,1), (0,2), (0,4), (1,2), (2,3), (2,4), (3,4)]
    assert tight[3] == [(0,1,2), (0,2,4), (2,3,4)]
    assert not tight[4]
    for n in [1, 2, 3]:
        assert len({joint(a) for a in tight[n]}) == len(tight[n])
    tables = {str(n): [dict(attachment=a, lists=joint(a)) for a in tight[n]]
              for n in tight}
    root_counts = {}
    for length in [3, 5]:
        surviving = []
        for assignments in product(tight[2], repeat=length-1):
            roots = [root_colors([available(a, ROWS[i]) for a in assignments]) for i in REJECT]
            if all(len(U-r) == 2 for r in roots):
                assert len(set(assignments)) == 1
                surviving.append(assignments[0])
        assert surviving == tight[2]
        root_counts[f'C{length}'] = dict(tested=len(tight[2])**(length-1), uniform=len(surviving))
    surviving = []
    for assignments in product(tight[1], repeat=3):
        roots = [root_colors([available(a, ROWS[i]) for a in assignments], True) for i in REJECT]
        if all(len(U-r) == 3 for r in roots):
            assert len(set(assignments)) == 1
            surviving.append(assignments[0])
    assert surviving == tight[1]
    root_counts['K4'] = dict(tested=125, uniform=5)

    certificates = []
    for a in tight[3]:
        es = frame() | {edge(v, b) for v in ['u', 'v'] for b in a}
        certificates.append(minor(f'duplicate_leaf_{a}', es,
                                  [['u'], ['v'], ['h']] + [[b] for b in a], 'K33'))
    # Connected C minus its 024 leaf contains the 012 and 234 leaves.
    es = frame() | {edge('t', v) for v in ['a','b','c']}
    es |= {edge(v, j) for v, a in zip(['a','b','c'], tight[3]) for j in a}
    certificates.append(minor('three_distinct_leaves', es,
                              [['b'], ['h'], ['a','t','c'], ['0'], ['2'], ['4']], 'K33'))
    for a, b in tight[2]:
        for k in set(range(5)) - {a, b}:
            es = frame() | {edge('x','u'), edge('u','v'), edge('v','x'),
                            edge('x','t'), edge('t',k)}
            es |= {edge(v, j) for v in ['u','v'] for j in [a,b]}
            certificates.append(minor(f'terminal_triangle_{a}_{b}_exit_{k}', es,
                                      [['u'], ['v'], ['h', str(k), 't'], [a], [b], ['x']], 'K33'))
        for n in [5, 7]:
            vs = [f'v{i}' for i in range(n)]
            for marked in combinations(range(1, n), 3):
                es = frame() | {edge(vs[i], vs[(i+1) % n]) for i in range(n)}
                es |= {edge(vs[i], j) for i in marked for j in [a,b]}
                p, q, r = marked
                groups = [vs[p:q], vs[q:r], vs[r:] + vs[:p], [a], ['h', str(b)]]
                certificates.append(minor(f'cycle_{n}_{a}_{b}_{marked}', es, groups, 'K5'))
    for j in range(1, 5):
        vs = ['x','u','v','w']
        es = frame() | {edge(a,b) for a,b in combinations(vs, 2)}
        es |= {edge(v,j) for v in vs[1:]} | {edge('x','t'), edge('t',0)}
        certificates.append(minor(f'terminal_K4_{j}', es,
                                  [[v] for v in vs] + [['h','0',str(j),'t']], 'K5'))
    # All four exits can coincide at a boundary point: validate this too.
    k4_count = 0
    for ends in product(range(5), repeat=4):
        vs = [f'v{i}' for i in range(4)]
        ts = [f't{i}' for i in range(4)]
        es = frame() | {edge(a,b) for a,b in combinations(vs, 2)}
        es |= {edge(v,t) for v,t in zip(vs,ts)} | {edge(t,b) for t,b in zip(ts,ends)}
        record = minor(f'K4_four_exits_{ends}', es,
                       [[v] for v in vs] + [list(map(str, range(5))) + ts], 'K5')
        if len(set(ends)) in [1,4] and ends == tuple(sorted(ends)):
            certificates.append(record)
        k4_count += 1

    # Same graph and all twelve rows: tightness alone does not imply rejection.
    attachments = [(0,1,2), (0,2,4)]
    mask = sum(any(a != b for a in available(attachments[0], row)
                   for b in available(attachments[1], row)) << i for i,row in enumerate(ROWS))
    assert not mask & (1 << 3) and mask & (1 << 7) and not mask & (1 << 8)
    leaf_slack = {''.join(map(str,a)): [i for i,row in enumerate(ROWS)
                                      if len(available(a,row)) > 1] for a in tight[3]}
    return dict(scope='Local necessary tables and explicit minors only; no sector enumeration',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                rows=ROWS, rejected_indices=REJECT, attachment_tables=tables,
                root_controls=root_counts, leaf_slack_acceptance=leaf_slack,
                minors=certificates, four_exit_K4_checks=k4_count,
                tightness_negative_control=dict(edges=[[0,1]], attachments=attachments, mask=mask))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = json.loads(json.dumps(audit()))
    if args.check:
        assert report == json.loads(OUT.read_text()), 'saved report differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(check=args.check, root_controls=report['root_controls'],
                          saved_minors=len(report['minors']), four_exit_K4_checks=625,
                          negative_control_mask=report['tightness_negative_control']['mask'])))


if __name__ == '__main__':
    main()
