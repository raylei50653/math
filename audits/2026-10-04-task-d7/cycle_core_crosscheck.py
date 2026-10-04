#!/usr/bin/env python3
"""Independent small controls for D7 §§5.1, 5.3, 5.4; no checker imports."""
from itertools import combinations, permutations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('cycle_core_crosscheck.json')
COLORS = set(range(4))
Q = (0, 1, 0, 1, 2)
P = (0, 1, 2, 0, 2)


def normalized(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def lists(root, roles):
    exterior = ((root, *Q[1:]), (root, *P[1:]))
    if any(len({row[i] for i in roles}) != len(roles) for row in exterior):
        return None
    return tuple(tuple(sorted(COLORS - {row[i] for i in roles})) for row in exterior)


def connected(bag, edges):
    bag = set(bag)
    seen = {min(bag)}
    while True:
        grow = seen | {a for a, b in edges if b in seen and a in bag} | {
            b for a, b in edges if a in seen and b in bag}
        if grow == seen:
            return seen == bag
        seen = grow


def main():
    proper = [x for x in product(range(4), repeat=5)
              if all(x[i] != x[(i+1) % 5] for i in range(5))]
    rows = sorted({normalized(x) for x in proper})
    three = [x for x in rows if len(set(x)) == 3]
    four = [x for x in rows if len(set(x)) == 4]
    assert len(proper) == 240 and len(rows) == 10 and len(three) == len(four) == 5
    noncontact = {ij: lists(3, ij) for ij in combinations(range(1, 5), 2)
                  if lists(3, ij) is not None}
    assert set(noncontact) == {(1,2), (1,4), (2,3), (3,4)}
    assert len(set(noncontact.values())) == 4
    chain = {tuple(next(c for c in pair if c != 3) for pair in signature)
             for signature in noncontact.values()} | {(3,3)}
    entry = []
    for ij, palette in noncontact.items():
        allowed = []
        for k in range(1,5):
            cut = lists(3, (k,))
            if all(set(p) <= set(l) for p,l in zip(palette, cut)):
                incoming = tuple(next(iter(set(l)-set(p))) for p,l in zip(palette,cut))
                assert incoming not in chain
                allowed.append(k)
                entry.append(dict(actual_pair=ij, entry_boundary=k,
                                  cycle_palette=palette, incoming_palette=incoming))
        assert tuple(allowed) == ij
    contacts = {}
    for root in (0,3):
        cycle_contacts = {k: lists(root,(0,k)) for k in range(1,5)
                          if lists(root,(0,k)) is not None}
        assert not set(cycle_contacts.values()) & set(noncontact.values())
        noncontact_leaves = [ij for ij in combinations(range(1,5),3)
                            if lists(root,ij) is not None]
        assert not noncontact_leaves
        contact_leaves = [ij for ij in combinations(range(1,5),2)
                          if lists(root,(0,*ij)) is not None]
        if root == 0:
            assert cycle_contacts == {1: ((2,3),(2,3)), 4: ((1,3),(1,3))}
            assert contact_leaves == [(1,4)]
        contacts[root] = dict(cycle_contacts=cycle_contacts, contact_leaf_pairs=contact_leaves)

    all_unit = []
    for r in range(5):
        spokes = tuple(sorted((r+i)%5 for i in (0,2,4)))
        supports = [tuple(sorted((r+i)%5 for i in arc)) for arc in ((0,1,2),(2,3,4))]
        rainbow = [q for q in three if len({q[i] for i in spokes}) == 3]
        assert len(rainbow) == 1
        for q in three:
            if q in rainbow:
                continue
            carriers = [k for k,s in enumerate(supports) if len({q[i] for i in s}) == 3]
            assert len(carriers) == 1
            k = carriers[0]
            witnesses = [(b,pi) for b in four for pi in permutations(range(4))
                         if all(b[i] == pi[q[i]] for i in supports[k])
                         and COLORS-{b[i] for i in spokes} == {pi[3]}]
            assert witnesses
            b,pi = witnesses[0]
            all_unit.append(dict(rotation=r, spokes=spokes, supports=supports,
                                 q=q, carrier=k, T4=b, whole_unary_permutation=pi,
                                 blocked_root=pi[3]))
    assert len(all_unit) == 20
    saved = json.loads((ROOT/'artifacts/c5_excess_one_e2_951_remaining/observations.json').read_text())
    source = saved['all_unit_t3']['controls']
    assert len(source) == 20
    for c in source:
        w = c['T4_rejection']; b = w['row']; pi = w['common_S4_permutation']
        k = int(c['unique_possible_D_carrier'][1:])
        assert len(set(b)) == 4 and all(b[i] != b[(i+1)%5] for i in range(5))
        assert all(b[i] == pi[c['q'][i]] for i in c['original_unary_supports'][k])
        assert COLORS-{b[i] for i in c['spokes']} == {pi[3]}
    bases = json.loads((ROOT/'artifacts/c5_triangle_branches/observations.json').read_text())['disk_templates']
    assert len(bases) == 18
    assert all(any(4 in e and max(e)>=5 for e in b['edges']) for b in bases)

    core = json.loads((ROOT/'artifacts/c5_excess_one_e2_951_unary_core/observations.json').read_text())
    minor_results = []
    for m in core['models']:
        if 'original_K5_minor' not in m:
            continue
        minor = m['original_K5_minor']
        bags = [set(x) for x in minor['branch_sets']]
        edges = {tuple(sorted(x)) for x in m['edges']}
        assert len(bags)==5 and all(connected(x,edges) for x in bags)
        assert all(not a&b for a,b in combinations(bags,2))
        crosses = []
        for i,j in combinations(range(5),2):
            edge = next((e for e in edges if
                         (e[0] in bags[i] and e[1] in bags[j]) or
                         (e[1] in bags[i] and e[0] in bags[j])),None)
            assert edge is not None
            crosses.append(dict(pair=(i,j), original_edge=edge))
        minor_results.append(dict(model_id=m['model_id'], branch_sets=minor['branch_sets'],
                                  ten_edges=crosses))
    assert [m['model_id'] for m in minor_results] == [0,9,35,99]
    result = dict(scope='small local controls and direct stored-minor checks; no arbitrary-size graph enumeration',
                  first_internal_cycle_entries=entry, noncontact_signatures=[
                      dict(pair=k,palette=v) for k,v in noncontact.items()],
                  contact_signatures=contacts, all_unit_T4_controls=all_unit,
                  endpoint_bases_touch_singleton_count=len(bases), original_K5_minors=minor_results)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(cycle_entries=len(entry), all_unit_T4_controls=len(all_unit),
                         endpoint_bases=len(bases), four_original_K5_minors=len(minor_results)),sort_keys=True))


if __name__ == '__main__':
    main()
