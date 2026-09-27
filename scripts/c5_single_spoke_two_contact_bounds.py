#!/usr/bin/env python3
"""Classify only the 18 open queries with an unknown two-contact bound.

Source paths are existential routes through named actual components, not
invented vertex paths. Arbitrary-size block-tree proofs are in the report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

from c5_single_spoke_cores import PI, Q, RHO, reflect
from c5_single_spoke_completion import audit_completion, exterior_routes
from c5_single_spoke_branch_minor import control, verify_minor, tether_audit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_root_sweep/observations.json'
COVER = ROOT / 'artifacts/c5_two_spoke_nonadjacent/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_two_contact_bounds/observations.json'
U = set(range(4))


def routes(r, endpoints):
    choices = []
    for b in endpoints:
        choices.append(([dict(kind='spoke', boundary=b)] if r['spoke'] == b else []) +
                       [dict(kind='component', component=j, boundary=b,
                             path=['z', f'r{j}', f'path_in_C{j}', f'actual_neighbor_of_b{b}', f'b{b}'])
                        for j in (1, 2) if b in r['supports'][j]])
    return [list(ps) for ps in product(*choices)
            if len([p['component'] for p in ps if p['kind'] == 'component']) ==
            len({p['component'] for p in ps if p['kind'] == 'component'})]


def role_key(r, t):
    return (r['spoke'], tuple(sorted((f[0], tuple(s)) for f, s in zip(r['bans'], r['supports']))),
            r['bans'][0][0], t)


def relation_audit():
    # All nonempty ordered binary relations, not endpoint marginals.
    pairs = list(product(range(4), repeat=2))
    count = 0
    symmetry_checks = Counter()
    swap_indices = {}
    for d, e in ((2, 3), (0, 3)):
        perm = list(range(4)); perm[d], perm[e] = e, d
        swap_indices[d, e] = [4*perm[x]+perm[y] for x, y in pairs]
    for mask in range(1, 1 << 16):
        f = U.copy()
        for i, pair in enumerate(pairs):
            if mask >> i & 1:
                f &= set(pair)
        assert len(f) <= 2
        if len(f) == 2:
            assert all(set(pairs[i]) == f for i in range(16) if mask >> i & 1)
        for (d, e), indices in swap_indices.items():
            moved = sum(1 << indices[i] for i in range(16) if mask >> i & 1)
            if moved == mask:
                assert (d in f) == (e in f)
                symmetry_checks[f'{d},{e}'] += 1
        count += 1
    # Membership propagation through disjoint incident palettes: after equal
    # off-path membership is removed, equal vertex membership forces opposite
    # differences on its two path blocks. A cycle's third vertex forces zero.
    transitions = []
    for q1, p1, q2, p2 in product((0, 1), repeat=4):
        if q1 + q2 <= 1 and p1 + p2 <= 1 and q1 + q2 == p1 + p2:
            assert q1-p1 == -(q2-p2)
            transitions.append([q1, p1, q2, p2])
    for d, e in combinations(range(4), 2):
        perm = list(range(4)); perm[d], perm[e] = e, d
        for c in range(4):
            if {perm[c]} == {c}:
                assert c not in (d, e)
    return dict(nonempty_ordered_relations=count, symmetric_relations_checked=dict(symmetry_checks),
                membership_transitions=transitions,
                invariant_bridge_cannot_contain_swapped_color=True)


def generalized_tether_audit():
    """Both literal target rows used by the K5 proof, with q held fixed."""
    from c5_single_spoke_branch_palettes import mask, transport, disjoint_unions
    pairs = [(q, p) for q in range(1, 16) for p in range(1, 16)
             if q.bit_count() == p.bit_count() in (1, 2) and q & 9 == p & 9]
    result = []
    for t in (1, 2):
        h = 3-t
        target = (0, t, 0, h, t)
        root_supports = {}
        for q, p in pairs:
            if p & ~mask((0, t)):
                continue
            allowed = []
            for bits in range(16):
                support = [i for i in range(1, 5) if bits >> (i-1) & 1]
                valid = True
                for perm in permutations(range(4)):
                    for row, palette in ((Q, q), (target, p)):
                        if all(perm[row[i]] == row[i] for i in support):
                            valid &= transport(palette, perm) == palette
                    if all(perm[Q[i]] == target[i] for i in support):
                        valid &= transport(q, perm) == p
                if valid:
                    required = ({2} if q & 1 else set()) | ({1} if q & 2 else set()) | ({4} if q & 4 else set())
                    assert required <= set(support)
                    allowed.append(support)
            assert allowed
            root_supports[q, p] = allowed
        assert len(root_supports) == 5
        path_rows = []
        for contact, bits in product((False, True), range(16)):
            support = [i for i in range(1, 5) if bits >> (i-1) & 1]
            lists = [U - {row[i] for i in support} - ({z} if contact else set())
                     for row, z in ((Q, 3), (target, h), (target, 3))]
            degree = 4-len(support)-int(contact)
            if any(len(l) != degree for l in lists) or degree < (1 if contact else 2):
                continue
            lq, lh, l3 = map(mask, lists)
            rh, r3 = (8, 1 << h) if contact else (mask((h, 3)),)*2
            for count in range(3):
                for children in combinations_with_replacement(pairs, count):
                    unions = disjoint_unions(children)
                    if unions is None: continue
                    cq, cp = unions
                    if cq & ~lq or cp & ~lh or cp & ~l3 or lh ^ cp != rh or l3 ^ cp != r3: continue
                    residual = lq ^ cq
                    assert residual in ((2, 4) if contact else (10, 12))
                    a, = [c for c in (1, 2) if residual >> c & 1]
                    supplied = set(support)
                    for pair in children:
                        supplied |= set.intersection(*(set(x) for x in root_supports[pair]))
                    assert {2, 4 if a == 1 else 1} <= supplied
                    path_rows.append(dict(contact=contact, support=support, children=children, q_residual=residual))
        assert path_rows
        result.append(dict(target=target, root_supports=[dict(q=q, p=p, supports=v) for (q, p), v in root_supports.items()],
                           path_rows=path_rows))
    return result


def k5_controls():
    result = []
    # Reuse every old shape, remove the unused b0 spoke, and verify all ten
    # adjacencies again. Zero-length exterior interiors cover an actual spoke.
    for length in (1, 3, 5, 7):
        for i in range(1, length+1, 2):
            for a, styles, n in product((1, 2), product(('direct', 'separate_bridges', 'shared_cycle'), repeat=2), (0, 1, 3)):
                r = control(length, i, a, styles, n)
                r['edges'] = [e for e in r['edges'] if set(e) != {'z', 'b0'}]
                r['adjacencies'] = verify_minor(set(map(tuple, r['edges'])), list(map(set, r['branch_sets'])))
                result.append(r)
    assert len(result) == 540
    assert len(tether_audit()) == 20
    return result


def build():
    source = json.loads(SOURCE.read_text())
    lookup = {r['source_index']: r for r in source['records']}
    selected, groups = [], {}
    for query in source['open_queries']:
        r = lookup[query['source_index']]
        t = ('p1', 'p2').index(query['target'])
        e = r['targets'][t]
        if not any(b['component'] == 0 for b in e['bounds']):
            continue
        p = e['row']; support = set(r['supports'][0]); a, = r['bans'][0]
        other = set().union(*(set(k['forbidden']) for k in e['known']),
                            *(set(b['forbidden_upper_bound']) for b in e['bounds'] if b['component'] != 0))
        required = U - {p[r['spoke']]} - other
        assert required
        # Rejection forces all these colours into the SAME forbidden set.
        absent = U - {p[i] for i in support}
        symmetry_closure = required | (absent if required & absent else set())
        old_frame = r if t == 1 else reflect(r)
        failures = []
        if 0 in old_frame['supports'][0]: failures.append('actual_support_meets_target_singleton')
        if list(old_frame['bans'][0]) not in ([0], [3]): failures.append('q_forbidden_role_outside_3492_hypothesis')
        old_paths = routes(old_frame, (1, 4))
        if not old_paths: failures.append('no_distinct_component_route_certificate')
        direct = exterior_routes(old_frame)
        assert direct is None  # no direct closure by the inherited certificate
        cuts = [d for d in required if d != a and d not in {Q[i] for i in support} | {p[i] for i in support}
                and U - {Q[i] for i in support} - {a, d}]
        proof = {}
        if len(symmetry_closure) > 2:
            method = 'unused_target_color_orbit_capacity'
            proof = dict(required=sorted(required), absent=sorted(absent), forced_closure=sorted(symmetry_closure))
        elif cuts:
            method = 'two_contact_unused_pair_bridge_obstruction'
            d = cuts[0]; h = min(U - {Q[i] for i in support} - {a, d})
            proof = dict(excluded_color=d, q_unused_pair=[d, h], q_ban=a,
                         guaranteed_z_colors=sorted(set(cuts)))
        else:
            method = 'external_paths_branch_K5'
            # Reflect p2 sources as full labelled graphs; DO NOT silently
            # normalize the target while holding q fixed.
            frame = r if t == 0 else reflect(r)
            fp = p if t == 0 else [PI[p[RHO[i]]] for i in range(5)]
            fr = required if t == 0 else {PI[c] for c in required}
            assert set(frame['supports'][0]) == {1, 2, 3, 4} and list(frame['bans'][0]) == [3]
            assert fp[2] == 0 and fp[1] == fp[4] and {fp[1], fp[3]} == {1, 2}
            assert fr == {fp[3], 3}
            paths = routes(frame, (1, 4)); assert paths
            proof = dict(reflected=t == 1, frame=frame, actual_target_row=fp,
                         required=sorted(fr), all_route_choices=paths,
                         conditional_ordered_relation=[[fp[3], 3], [3, fp[3]]])
        k = role_key(r, t)
        g = groups.setdefault(k, dict(spoke=r['spoke'], support_by_forbidden_role=k[1],
                                      two_contact_role=a, target=query['target'], method=method, source_indices=[]))
        assert g['method'] == method
        g['source_indices'].append(r['source_index'])
        reflected = reflect(r)
        selected.append(dict(source_index=r['source_index'], target=query['target'],
                             spoke=r['spoke'], bans=r['bans'], actual_supports=r['supports'],
                             placements=r['placements'], ordered_contacts=['u', 'v'],
                             single_contact_path_sources=[dict(component=j, root=f'r{j}',
                                 actual_endpoints=r['supports'][j],
                                 meaning='for each b in actual_endpoints, take a simple root-to-actual-b-neighbor path inside this unchanged connected component, then its original boundary edge')
                                 for j in (1, 2)],
                             contact_words=[sum(([('u' if j == 0 else f'r{j}'), 'v'] if j == 0 else [f'r{j}']
                                                 for j in pl['order']), []) for pl in r['placements']],
                             inherited_query=e, forced_component_0_colors=sorted(required),
                             direct_completion=dict(frame=old_frame, route_choices=old_paths, failures=failures),
                             original_external_route_choices=routes(r, (1, 4)),
                             reflection=dict(frame=reflected, actual_target_row=[PI[p[RHO[i]]] for i in range(5)],
                                             placements=[dict(order=list(reversed(pl['order'])),
                                                              lifted_supports=[sorted(5-x for x in s) for s in pl['lifted_supports']])
                                                         for pl in r['placements']],
                                             geometric_contact_words=[list(reversed(sum((["u", "v"] if j == 0 else [f'r{j}']
                                                                        for j in pl['order']), [])))
                                                                      for pl in r['placements']],
                                             contact_coordinates=['u', 'v'], coordinate_color_map=PI),
                             method=method, proof=proof, accepted=True))
    assert len(selected) == 18 and len(groups) == 9
    # Six geometric/role orbits after canonicalizing the TARGET PARTITION.
    # Exact target colours stay in reflection records; these are not nine
    # queries identified by a q-preserving global colour permutation.
    orbit_keys = {}
    for k, g in sorted(groups.items()):
        r = lookup[g['source_indices'][0]]
        orbit = min(k, role_key(reflect(r), 1-k[3]))
        orbit_keys.setdefault(orbit, []).append(g)
    assert len(orbit_keys) == 6
    updated = {r['source_index']: [e['accept'] for e in r['targets']] for r in source['records']}
    for r in selected: updated[r['source_index']][('p1', 'p2').index(r['target'])] = True
    names = {(True, True): 'both', (True, False): 'p1_only', (False, True): 'p2_only'}
    counts = Counter(names[tuple(flags)] for flags in updated.values())
    remaining = [q for q in source['open_queries'] if not updated[q['source_index']][('p1', 'p2').index(q['target'])]]
    assert len(remaining) == 16
    assert all(not any(b['component'] == 0 for b in lookup[q['source_index']]['targets'][('p1', 'p2').index(q['target'])]['bounds']) for q in remaining)
    methods = Counter(r['method'] for r in selected)
    assert sorted(methods.values()) == [4, 6, 8]
    paths = [SOURCE, COVER, Path(__file__)] + [ROOT / 'scripts' / n for n in
             ('c5_single_spoke_cores.py', 'c5_single_spoke_completion.py', 'c5_single_spoke_branch_minor.py',
              'c5_single_spoke_branch_palettes.py', 'c5_single_spoke_bridge_path.py', 'c5_two_spoke_middle_21.py')]
    return dict(scope='paper arbitrary-size lemmas plus finite necessary-relation and extracted-minor audits; no source realizability claim',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_complete_relation_cover=audit_completion(json.loads(COVER.read_text())),
                relation_audit=relation_audit(), generalized_tethers=generalized_tether_audit(), minor_controls=k5_controls(),
                direct_completion_closed=0, methods=dict(methods), counts=dict(counts),
                groups=list(groups.values()), geometric_reflection_orbits=list(orbit_keys.values()),
                records=selected, open_queries=remaining)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build(); payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check: assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps({k: result[k] for k in ('methods', 'counts', 'direct_completion_closed')}, sort_keys=True))


if __name__ == '__main__': main()
