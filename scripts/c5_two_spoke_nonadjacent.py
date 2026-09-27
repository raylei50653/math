#!/usr/bin/env python3
"""Nonadjacent two-spoke exit separation: replay justified finite reductions.

No source-size cutoff and no independent reflected graph enumeration.
The arbitrary-size coverage and preservation proof is in the companion report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_two_spoke_middle_21 import U, Q, colorings, relation, forbidden
from c5_two_spoke_reflection import RHO, PI, row_image, faces

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_nonadjacent/observations.json'
PA = (0, 1, 0, 2, 1)
PB = (0, 1, 2, 1, 2)
CYCLE = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}


def edge(u, v):
    return tuple(sorted((u, v)))


def components(vs, es):
    unseen, result = set(vs), []
    while unseen:
        stack, comp = [min(unseen)], set()
        while stack:
            v = stack.pop()
            if v in comp:
                continue
            comp.add(v)
            stack.extend(w for e in es if v in e for w in e if w in unseen-comp)
        unseen -= comp
        result.append(sorted(comp))
    return result


def witness(es, b):
    vs = sorted({v for e in es for v in e})
    lists = {v: U if v >= 5 else {b[v]} for v in vs}
    f = next(colorings(vs, es, lists), None)
    assert f is not None
    assert all(f[u] != f[v] for u, v in es)
    return [f[v] for v in vs]


def join_record(es, z, b):
    inn = sorted({v for e in es for v in e if v >= 5 and v != z})
    data = []
    for vs in components(inn, es):
        ce = {e for e in es if set(e) <= set(vs)}
        att = {v: sorted(w for e in es if v in e for w in e if w < 5) for v in vs}
        ports = sorted(v for v in vs if edge(z, v) in es)
        r = relation(vs, ce, att, ports, b)
        if len(ports) == 2:
            assert relation(vs, ce, att, ports[::-1], b) == sorted(t[::-1] for t in r)
        data.append(dict(vertices=vs, edges=sorted(ce), attachments=att,
                         ordered_contacts=ports, tuples=r, forbidden=forbidden(r)))
    data.sort(key=lambda d: -len(d['ordered_contacts']))
    assert [len(d['ordered_contacts']) for d in data] == [2, 1]
    spokes = sorted(w for e in es if z in e for w in e if w < 5)
    allowed = U - {b[i] for i in spokes} - set().union(*(set(d['forbidden']) for d in data))
    vs = [*range(5), *inn, z]
    lists = {v: U if v >= 5 else {b[v]} for v in vs}
    direct = {f[z] for f in colorings(vs, es, lists)}
    assert allowed == direct
    return dict(boundary=b, components=data, allowed=sorted(allowed))


def merged_spokes():
    records, counts, sources = [], Counter(), {}
    for name in ('c5_triangle_branches', 'c5_two_triangle_blocks'):
        path = ROOT / 'artifacts' / name / 'observations.json'
        sources[str(path.relative_to(ROOT))] = sha256(path.read_bytes()).hexdigest()
        bases = json.loads(path.read_text())['disk_templates']
        for idx, base in enumerate(bases):
            if name == 'c5_two_triangle_blocks' and base['critical_edges'] is None:
                continue
            old_es = {tuple(e) for e in base['edges']}
            rot = base['apex_rotation']
            apex = len(rot)-1
            ae = old_es | {(i, apex) for i in range(5)}
            assert {edge(v, w) for v, ns in enumerate(rot) for w in ns} == ae
            assert len(rot)-len(ae)+len(faces(rot)) == 2
            # Boundary rotation i -> i-1; swapping 0,1 transports Q to PA.
            move = lambda v: (v+4) % 5 if v < 5 else v
            es = {edge(move(u), move(v)) for u, v in old_es}
            inn = sorted({v for e in es for v in e if v >= 5})
            assert all(sum(v in e for e in es) == 4 for v in inn)
            for z in inn:
                ns = {w for e in es if z in e for w in e if w != z}
                bn = ns & set(range(5))
                if len(bn) != 1 or not bn <= {1, 4}:
                    continue
                added = edge(z, next(iter({1, 4}-bn)))
                aug = es | {added}
                assert sum(z in e for e in aug) == 5
                # Check inherited rejection and every edge deletion at PA.
                vs = list(range(max(inn)+1))
                lists = {v: U if v >= 5 else {PA[v]} for v in vs}
                assert next(colorings(vs, es, lists), None) is None
                deletions = [dict(edge=e, coloring=witness(es-{e}, PA)) for e in sorted(es-CYCLE)]
                rows = [join_record(aug, z, b) for b in (Q, PA, PB)]
                assert rows[0]['allowed'] and not rows[1]['allowed']
                records.append(dict(source=name, source_index=idx, hub=z,
                                    base_edges=sorted(es), added_edge=added,
                                    q_coloring=witness(aug, Q), rows=rows,
                                    base_PA_edge_deletions=deletions))
                counts[name] += 1
    assert counts == {'c5_triangle_branches': 10, 'c5_two_triangle_blocks': 64}
    return records, dict(counts), sources


def two_color_completion():
    records, counts = [], Counter()
    # K has z=5 at a non-bridge triangle vertex, contacts (6,7).
    for kind, vs, es in [
            ('triangle', [6, 7], {(6, 7)}),
            ('two_triangles', list(range(6, 11)),
             {(6, 7), (6, 8), (8, 9), (8, 10), (9, 10)})]:
        opts = [list(combinations((1, 2, 3, 4),
                                 4-sum(v in e for e in es)-int(v in (6, 7)))) for v in vs]
        for aa in product(*opts):
            att = dict(zip(vs, aa))
            qr = relation(vs, es, att, [6, 7], Q)
            pr = relation(vs, es, att, [6, 7], PB)
            fq, fp = forbidden(qr), forbidden(pr)
            assert not (fp == [0, 3] and fq in ([0], [3]))
            full = CYCLE | es | {(5, 6), (5, 7), (1, 5), (4, 5)}
            full |= {edge(v, i) for v in vs for i in att[v]}
            assert all(sum(v in e for e in full) == 4 for v in [5, *vs])
            record = dict(kind=kind, vertices=vs, edges=sorted(es),
                          attachments=att, ordered_contacts=[6, 7],
                          q_tuples=qr, p_tuples=pr, q_forbidden=fq, p_forbidden=fp)
            if fp == [0, 3]:
                record['completion_PB_edge_deletions'] = [
                    dict(edge=e, coloring=witness(full-{e}, PB)) for e in sorted(full-CYCLE)]
                counts['PB_rejecting_completions'] += 1
            records.append(record)
            counts[kind] += 1
    assert counts['triangle'] == 36 and counts['two_triangles'] == 3456
    return records, dict(counts)


def reflection_table():
    result = []
    for name, long_c2, f2, f1 in [('I', True, 0, 3), ('II', True, 3, 0),
                                 ('III', False, 0, 3), ('IV', False, 3, 0)]:
        result.append(dict(case=name, C2_side='pentagon' if long_c2 else 'quadrilateral',
                           spokes=[1, 4], C2_forbidden=[f2], C1_forbidden=[f1],
                           reflected_spokes=sorted(RHO[i] for i in (1, 4)),
                           reflected_C2_forbidden=[PI[f2]], reflected_C1_forbidden=[PI[f1]],
                           reflected_pentagon=[RHO[i] for i in (1, 2, 3, 4)],
                           reflected_quadrilateral=[RHO[i] for i in (4, 0, 1)]))
    assert row_image(Q) == Q
    assert tuple({0: 2, 2: 0}.get(c, c) for c in row_image(PA)) == PB
    assert tuple({1: 2, 2: 1}.get(c, c) for c in row_image(PB)) == PA
    return result


def build():
    a, ac, sources = merged_spokes()
    b, bc = two_color_completion()
    for name in ('c5_two_spoke_nonadjacent.py', 'c5_two_spoke_middle_21.py',
                 'c5_two_spoke_reflection.py'):
        p = ROOT / 'scripts' / name
        sources[str(p.relative_to(ROOT))] = sha256(p.read_bytes()).hexdigest()
    return dict(schema=1, scope='finite reductions; arbitrary-size coverage is paper proof',
                source_sha256=sources, merged_spoke_counts=ac, merged_spoke_forms=a,
                completion_counts=bc, completion_forms=b, reflection=reflection_table())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(merged=result['merged_spoke_counts'], completion=result['completion_counts'],
                         reflected_entries=len(result['reflection']), checked=args.check)))


if __name__ == '__main__':
    main()
