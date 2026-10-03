#!/usr/bin/env python3
"""Exclude a rejected binary omission for t=2, original partition (2,2).

Full ordered binary relations are joined in one literal boundary frame.
Arbitrary-size coverage uses the inherited original-contact tail transfer.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, U, components, normalize
from c5_941_two_spoke import base_record, component_record, search
from c5_941_three_spoke import bare_triangles
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_two_binary/observations.json'
CORES = ROOT / 'artifacts/c5_941_three_spoke/observations.json'
FORBIDDEN = tuple(tuple(c) for k in range(3) for c in combinations(range(4), k))
PERMS = tuple(tuple((sign*j+shift) % 5 for j in range(5))
              for sign, shift in product((-1, 1), range(5)))


def literal(x):
    return json.loads(json.dumps(x))


def verify_source():
    source = json.loads(CORES.read_text())
    for name, digest in source['source_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    assert source['pattern_order'] == literal(ROWS)
    bare = bare_triangles()
    assert source['bare_triangle_controls'] == literal(bare)
    bases = source['bases']
    assert bases[:36] == literal([b for b in bare if b['accepts_T4']])
    for base in bases[36:]:
        assert base == literal(base_record(base['family'], base['input_index'], base))
    expected = set()
    for bi, base in enumerate(bases):
        edges = set(map(tuple, base['edges']))
        for r in range(5, base['vertices']):
            contacts = sorted(v for v in range(5, base['vertices'])
                              if tuple(sorted((v, r))) in edges)
            if len(contacts) == 2 and tuple(contacts) in edges:
                expected.add((bi, r))
    marks = source['marked_models']
    assert len(marks) == len(expected) == 398
    assert {(m['base_id'], m['root']) for m in marks} == expected
    for m in marks:
        base = bases[m['base_id']]
        edges = set(map(tuple, base['edges']))
        r, n = m['root'], base['vertices']
        binary, = components(set(range(5, n)) - {r}, edges)
        contacts = sorted(v for v in binary if tuple(sorted((v, r))) in edges)
        spokes = sorted(b for b in B if (b, r) in edges)
        assert m['binary_vertices'] == binary and m['binary_contacts'] == contacts
        assert m['port_order'] == [r] + contacts
        assert m['existing_spokes'] == [[b, r] for b in spokes]
        assert len(spokes) == 2
        for q, row in zip(ROWS, m['rows'], strict=True):
            assert row['row'] == list(q)
            assert row['binary'] == literal(component_record(binary, contacts, edges, q))
            full = list(search(range(5, n), edges, dict(enumerate(q))))
            joined = {(a, x, y) for x, y in row['binary']['ordered_relation']
                      for a in U - {q[b] for b in spokes} - {x, y}}
            assert joined == {tuple(f[v] for v in m['port_order']) for f in full}
            assert joined == set(map(tuple, row['ordered_port_relation']))
            for t, w in zip(row['ordered_port_relation'], row['tuple_witnesses'], strict=True):
                assert len(w) == n and w[:5] == list(q) and set(w) <= U
                assert [w[v] for v in m['port_order']] == t
                assert all(w[a] != w[b] for a, b in edges)
    return source


def non_disk_bare(bases):
    """Explicit K3,3 subdivisions in the outer-apex graph, no oracle."""
    result = {}
    for bi, base in enumerate(bases[:36]):
        neighborhoods = base['neighborhoods']
        repeated = [(i, j) for i, j in combinations(range(3), 2)
                    if neighborhoods[i] == neighborhoods[j]]
        if not repeated:
            continue
        i, j = repeated[0]
        k, = set(range(3)) - {i, j}
        a, b = neighborhoods[i]
        c = min(set(neighborhoods[k]) - {a, b})
        p, q, z, apex = 5+i, 5+j, 5+k, 8
        left, right = [a, b, z], [p, q, apex]
        paths = [[x, y] if (x, y) != (z, apex) else [z, c, apex]
                 for x in left for y in right]
        edges = set(map(tuple, base['edges'])) | {(v, apex) for v in range(5)}
        branches = set(left + right)
        internal = []
        assert len(branches) == 6
        for path in paths:
            assert all(tuple(sorted(e)) in edges for e in zip(path, path[1:]))
            assert not branches & set(path[1:-1])
            internal.extend(path[1:-1])
        assert len(internal) == len(set(internal))
        result[bi] = dict(left=left, right=right, paths=paths, apex=apex)
    assert len(result) == 12
    return result


def options(mark, target):
    """Necessary row choices for the same omitted C; all |F_C|<=2 allowed."""
    spokes = [e[0] for e in mark['existing_spokes']]
    rows = []
    for i, q in enumerate(ROWS):
        fa = set(mark['rows'][i]['binary']['forbidden'])
        sc = {q[b] for b in spokes}
        choices = []
        for colors in FORBIDDEN:
            fc = set(colors)
            if (sc | fa | fc != U) != bool(target >> i & 1):
                continue
            if fa | fc == U:  # Both original spokes omitted must accept.
                continue
            choices.append(dict(forbidden=list(colors), other_omission_rejects=sc | fc == U))
        rows.append(choices)
    return rows


def transport(mark, perm):
    """Pull back the literal row, then undo its one canonical S4 renaming."""
    rows = []
    for q in ROWS:
        pulled = tuple(q[perm[b]] for b in range(5))
        canonical = normalize(pulled)
        color_map = dict(zip(canonical, pulled))
        if len(color_map) == 3:
            color_map[3] = 3
        assert set(color_map) == U and set(color_map.values()) == U
        ri = ROWS.index(canonical)
        rel = [tuple(color_map[c] for c in t)
               for t in mark['rows'][ri]['binary']['ordered_relation']]
        rows.append(dict(source_row=ri, color_map=[color_map[c] for c in range(4)],
                         relation=rel, forbidden=sorted(set.intersection(*(set(t) for t in rel)))))
    return rows


def join_certificate(source, mi, ni, pi, target, transported):
    """One mismatching row suffices; verify its FULL five-port relation."""
    marks, bases = source['marked_models'], source['bases']
    m, n = marks[mi], marks[ni]
    perm = PERMS[pi]
    spokes = [e[0] for e in m['existing_spokes']]
    sigma = 0
    for i, q in enumerate(ROWS):
        fa = set(m['rows'][i]['binary']['forbidden'])
        fc = set(transported[i]['forbidden'])
        if U - {q[b] for b in spokes} - fa - fc:
            sigma |= 1 << i
    assert sigma != target
    ri = next(i for i in range(10) if (sigma ^ target) >> i & 1)
    q = ROWS[ri]
    ar = m['rows'][ri]['binary']['ordered_relation']
    cr = transported[ri]['relation']
    joined = sorted((a, x, y, u, v) for x, y in ar for u, v in cr
                    for a in U - {q[b] for b in spokes} - {x, y, u, v})
    # Copy the two *classified cores*, identifying only literal B and r.
    # This does not claim the glued graph is a disk realization.
    bm, bn = bases[m['base_id']], bases[n['base_id']]
    mapping = dict(enumerate(perm))
    mapping[n['root']] = m['root']
    mapping.update({v: bm['vertices']+j for j, v in enumerate(n['binary_vertices'])})
    edges = set(map(tuple, bm['edges'])) | {
        tuple(sorted((mapping[a], mapping[b]))) for a, b in bn['edges']}
    count = bm['vertices'] + len(n['binary_vertices'])
    ports = m['port_order'] + [mapping[v] for v in n['binary_contacts']]
    actual = list(search(range(5, count), edges, dict(enumerate(q))))
    assert {tuple(f[v] for v in ports) for f in actual} == set(joined)
    witnesses = [[next(f for f in actual if tuple(f[v] for v in ports) == t)[v]
                  for v in range(count)] for t in joined]
    assert bool(joined) == bool(sigma >> ri & 1)
    return dict(second_mark=ni, permutation_index=pi, sigma=sigma, mismatch_row=ri,
                ordered_five_port_relation=joined, full_coloring_witnesses=witnesses)


def build():
    source = verify_source()
    marks, bases = source['marked_models'], source['bases']
    non_disk = non_disk_bare(bases)
    counts = Counter()
    records, residuals = [], []
    for mi, m in enumerate(marks):
        for candidate in (933, 941):
            for target in orbit(candidate):
                rows = options(m, target)
                empty = [i for i, row in enumerate(rows) if not row]
                forced = [i for i, row in enumerate(rows)
                          if row and all(c['other_omission_rejects'] for c in row)]
                record = dict(mark=mi, candidate=candidate, target=target)
                if target & 1:
                    reason = 'first_core_rejects_required_row'
                elif empty:
                    reason = 'empty_necessary_row'
                    record['row'] = empty[0]
                elif len(forced) > 1:
                    reason = 'other_omission_rejects_two_rows'
                    record['rows'] = forced
                elif m['base_id'] in non_disk:
                    reason = 'first_core_has_apex_K33'
                    record['non_disk_base'] = m['base_id']
                else:
                    assert len(forced) == 1
                    reason = 'forced_second_classified_core'
                    record.update(forced_second_row=forced[0], row_options=rows)
                    residuals.append(record)
                record['reason'] = reason
                counts[f'{candidate}_{reason}'] += 1
                records.append(record)
    # Explicitly shared spoke endpoints, rejection row, boundary frame, root.
    transformed = {}
    histogram = Counter()
    pair_checks = 0
    for record in residuals:
        mi, target, forced = record['mark'], record['target'], record['forced_second_row']
        sp = tuple(e[0] for e in marks[mi]['existing_spokes'])
        certificates = []
        for ni, n in enumerate(marks):
            for pi, perm in enumerate(PERMS):
                if tuple(sorted(perm[e[0]] for e in n['existing_spokes'])) != sp:
                    continue
                if normalize(tuple(ROWS[forced][perm[b]] for b in range(5))) != ROWS[0]:
                    continue
                key = (ni, pi)
                if key not in transformed:
                    transformed[key] = transport(n, perm)
                cert = join_certificate(source, mi, ni, pi, target, transformed[key])
                certificates.append(cert)
                histogram[cert['sigma']] += 1
                pair_checks += 1
        if not certificates:
            counts["forced_second_core_with_no_matching_spokes"] += 1
        record['second_core_comparisons'] = certificates
    assert len(records) == 3980 and len(residuals) == 36 and pair_checks == 2376
    assert all(r['candidate'] == 941 for r in residuals)
    paths = [Path(__file__).resolve(), CORES,
             ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_941_two_spoke.py', ROOT / 'scripts/c5_941_three_spoke.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1, scope='conditional t=2 (2,2) rejected original binary omission',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, target_orbits={str(m): orbit(m) for m in (933, 941)},
        port_order=['r', 'original_A_x', 'original_A_y', 'original_C_u', 'original_C_v'],
        source_mark_semantics='indices in the hashed original three-spoke marked_models; no additions used',
        second_core_permutations=PERMS, non_disk_bare_core_certificates=non_disk,
        exclusions=records,
        paper_dependencies=['connected all-degree-four disk single-missing classification',
            'original ordered binary relation and contact-preserving tail transfer',
            'arbitrary original binary slack and exact five-port gluing',
            'same other binary omission rejects at most one row',
            'candidate unique degree-six double-spoke omission accepts all rows'],
        summary=dict(sorted(counts.items()), bases=118, marked_roots=398,
            candidate_comparisons=len(records), abstract_survivors_before_disk=90,
            bare_apex_K33_certificates=len(non_disk), forced_second_cores=len(residuals),
            same_frame_second_core_comparisons=pair_checks,
            full_five_port_mismatch_checks=pair_checks,
            second_core_sigma_histogram=dict(sorted(histogram.items())), remaining=0,
            omitted_component_graph_enumeration=False, new_lean_theorem=False,
            full_source_disk_realizability_claimed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=1, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
