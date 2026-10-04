#!/usr/bin/env python3
"""D3 independent C relation/identity audit; no production imports or flags.

Only standard-library graph coloring and literal named vertices are used.
The arbitrary unary components in C have role data, not serialized graphs.
Their role joins are audited as semantics, never as source realizations.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

Q = (0, 1, 0, 1, 2)
U = set(range(4))
PAIRS = list(product(range(4), repeat=2))
CYCLE = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
ALIASES = {i: f"b{i}" for i in range(5)} | {5: "z", 6: "w", 7: "x0", 8: "x1", 9: "x2"}


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1) + "\n")


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def normalized_rows(rows, label):
    result = [tuple(row) for row in rows]
    check(len(result) == len(set(result)), f"duplicate rows: {label}")
    return set(result)


def original_edges(supports, roots=True, zw=False, sides=None):
    edges = set(CYCLE) | {(7, 8), (8, 9)}
    for v, bs in zip((7, 8, 9), supports):
        edges.update(tuple(sorted((v, b))) for b in bs)
    if roots:
        edges.update({(5, 9), (6, 9)})
    if zw:
        edges.add((5, 6))
    if sides is not None:
        for v, bs in zip((5, 6), sides):
            edges.update(tuple(sorted((v, b))) for b in bs)
    return edges


def colorings(vertices, edges, pins):
    """Independent MRV search over the actual edge set, returning all colorings."""
    vertices = set(vertices)
    neighbors = {v: set() for v in vertices}
    for a, b in edges:
        check(a in vertices and b in vertices and a != b, "edge outside graph")
        neighbors[a].add(b)
        neighbors[b].add(a)
    if any(a in pins and b in pins and pins[a] == pins[b] for a, b in edges):
        return []
    current = dict(pins)
    remaining = vertices - current.keys()
    answers = []

    def visit(todo):
        if not todo:
            answers.append(dict(current))
            return
        domains = {v: U - {current[n] for n in neighbors[v] if n in current} for v in todo}
        vertex = min(todo, key=lambda v: (len(domains[v]), -len(neighbors[v]), v))
        for color in sorted(domains[vertex]):
            current[vertex] = color
            visit(todo - {vertex})
        current.pop(vertex, None)

    visit(remaining)
    return answers


def brute_relation(supports, roots=True, zw=False):
    edges = original_edges(supports, roots=roots, zw=zw)
    vertices = set(range(10)) if roots else set(range(5)) | {7, 8, 9}
    witnesses = colorings(vertices, edges, dict(enumerate(Q)))
    order = (5, 6, 7, 8, 9) if roots else (7, 8, 9)
    rows = sorted(tuple(w[v] for v in order) for w in witnesses)
    check(len(rows) == len(set(rows)), "duplicate independent coloring")
    return rows


def pinned_fibres(rows):
    return [dict(roots=list(pair), complete_triples=[list(t[2:]) for t in rows if t[:2] == pair])
            for pair in PAIRS]


def powerset(values):
    return [tuple(c) for size in range(len(values)+1) for c in combinations(values, size)]


def integer_partitions(total, ceiling=None):
    if not total:
        return [()]
    ceiling = total if ceiling is None else min(total, ceiling)
    out = []
    for first in range(ceiling, 0, -1):
        out.extend((first,) + rest for rest in integer_partitions(total-first, first))
    return out


def derive_roles():
    """Degree 5: zw + one mixed contact + 3 remaining actual incidences.

    Each color role uses distinct spoke colors and an ordered partition of
    unary incidences. Unary forbidden sets must be nonempty, at most their
    contact counts, disjoint from spokes and each other; residual size is 1/2.
    No saved role, mask, or source-exclusion flag determines this domain.
    """
    roles = []
    color_sets = powerset(tuple(range(4)))[1:]
    for spokes in powerset((0, 1, 2)):
        for contacts in integer_partitions(3-len(spokes)):
            options = [[s for s in color_sets if len(s) <= k] for k in contacts]
            for fs in product(*options):
                occupied = list(spokes) + [c for f in fs for c in f]
                if len(occupied) != len(set(occupied)):
                    continue
                residual = sorted(U - set(occupied))
                if len(residual) not in (1, 2):
                    continue
                roles.append(dict(spoke_colors=list(spokes), unary_contacts=list(contacts),
                                  unary_forbidden=[list(f) for f in fs], residual=residual))
    check(len(roles) == len({canon(r) for r in roles}), "duplicate derived roles")
    return roles


def derive_joins(roles, triples):
    """Literal source criteria; release each named unary/spoke constraint.

    zw deletion must accept a diagonal, intact zw must reject, and every
    nonempty side constraint release must permit a non-diagonal P3 extension.
    A release uses its original forbidden color set in the common color frame.
    """
    accepts = {(z, w) for z, w in PAIRS if any(t[2] not in (z, w) for t in triples)}
    out = []
    for zid, zrole in enumerate(roles):
        for wid, wrole in enumerate(roles):
            Ez, Ew = zrole['residual'], wrole['residual']
            original_pairs = set(product(Ez, Ew))
            if any(z != w and (z, w) in accepts for z, w in original_pairs):
                continue
            if not any(z == w and (z, w) in accepts for z, w in original_pairs):
                continue
            if not any(z != w for z, w in original_pairs):
                continue
            success = True
            for side, role in enumerate((zrole, wrole)):
                constraints = role['unary_forbidden'] + [[c] for c in role['spoke_colors']]
                for released in constraints:
                    candidates = product(released, Ew) if side == 0 else product(Ez, released)
                    if not any(z != w and (z, w) in accepts for z, w in candidates):
                        success = False
                        break
                if not success:
                    break
            if success:
                out.append((zid, wid))
    return out


def local_audit(data):
    saved = data['local']
    roles = derive_roles()
    check(roles == saved['side_roles'], "complete named side roles differ")
    controls, derived_cases, saved_relations = [], [], []
    joins_by_a = {}
    counts = Counter()
    supported = list(product(combinations(range(5), 3), combinations(range(5), 2), combinations(range(5), 1)))
    check(len(saved['configurations']) == len(supported) == 500, "500 attachment domain")
    check(len({tuple(map(tuple,r['actual_supports'])) for r in saved['configurations']}) == 500,
          "duplicate saved attachment identities")
    for local_id, supports in enumerate(supported):
        r = saved['configurations'][local_id]
        check(r['id'] == local_id and tuple(map(tuple,r['actual_supports'])) == supports,
              f"actual attachment identity {local_id}")
        triples = brute_relation(supports, roots=False)
        check(normalized_rows(r['complete_triples'], f"local {local_id}") == set(triples),
              f"complete triples {local_id}")
        lists = [sorted(U - {Q[b] for b in s}) for s in supports]
        check(lists == r['lists'], f"lists {local_id}")
        mask = sum(1 << (16*t[0]+4*t[1]+t[2]) for t in triples)
        check(mask == r['vertex_tuple_mask'], f"tuple mask {local_id}")
        root_rows = brute_relation(supports)
        root_rows_zw = brute_relation(supports, zw=True)
        expected = sorted((z,w,*t) for z,w in PAIRS for t in triples if t[2] != z and t[2] != w)
        check(root_rows == expected, f"same shared x2 root relation {local_id}")
        check(root_rows_zw == [t for t in root_rows if t[0] != t[1]], f"zw relation {local_id}")
        fibres = pinned_fibres(root_rows)
        forbidden = [f['roots'] for f in fibres if not f['complete_triples']]
        counts['base_literal_fibres'] += 16
        counts['base_empty_fibres'] += len(forbidden)
        counts['base_zw_literal_fibres'] += 16
        counts['base_zw_empty_fibres'] += sum(not f['complete_triples'] for f in pinned_fibres(root_rows_zw))
        check(sum(1 << (4*z+w) for z,w in forbidden) == r['forbidden_pair_mask'], f"forbidden {local_id}")
        record = dict(local_id=local_id, actual_supports=supports, aliases=ALIASES,
                      actual_P3_attachment_edges=sorted(original_edges(supports, roots=False)-CYCLE-{(7,8),(8,9)}),
                      original_context_edges_without_zw=sorted(original_edges(supports)),
                      ordered_vertices=[7,8,9], lists=lists, complete_triples=triples,
                      root_fibres_without_zw=fibres, root_fibres_with_zw=pinned_fibres(root_rows_zw))
        saved_relations.append(record)
        if forbidden:
            counts['nonempty_forbidden_local'] += 1
            a = next(c for c in range(3) if (c,3) in map(tuple, forbidden))
            c = Q[supports[2][0]]
            d = next(color for color in range(3) if color not in (a,c))
            check((r['a'],r['c'],r['d']) == (a,c,d), f"color role {local_id}")
            check(triples == [(3,d,a),(3,d,3)], f"two-row identity {local_id}")
            joins = derive_joins(roles, triples)
            check(len(joins) == 125, f"full side join domain {local_id}")
            check(joins == [tuple(j) for j in saved['joins_by_a'][str(a)]], f"ordered join identity a={a}")
            if a in joins_by_a:
                check(joins_by_a[a] == joins, f"join role stability {a}")
            else:
                joins_by_a[a] = joins
            residuals = (([a,3],[a,3]),([a],[a,3]),([3],[a,3]),([a,3],[a]),([a,3],[3]))
            for branch, (Ez,Ew) in enumerate(residuals):
                jids = [jid for jid,(zid,wid) in enumerate(joins) if roles[zid]['residual'] == Ez and roles[wid]['residual'] == Ew]
                check(len(jids) == 25, f"branch role count {local_id}/{branch}")
                case = dict(id=len(derived_cases),name=f"CPP-{local_id:03d}-{branch}",local_id=local_id,
                            branch=branch,z_residual=Ez,w_residual=Ew,side_join_ids=jids)
                derived_cases.append(case)
    check(derived_cases == saved['cases'], "complete named case set/side identities")
    check(len(derived_cases) == 560, "560 local/residual cases")
    # Every side-role joint keeps the complete P3 tuples and all 16 literal
    # fibres. Empty entries also include roots outside either side residual.
    for case in derived_cases:
        local = saved_relations[case['local_id']]
        a = data['local']['configurations'][case['local_id']]['a']
        for jid in case['side_join_ids']:
            zid,wid = joins_by_a[a][jid]
            Ez,Ew = roles[zid]['residual'],roles[wid]['residual']
            rows = [(z,w,*t) for z,w in product(Ez,Ew) for t in local['complete_triples'] if t[2] not in (z,w)]
            fibres = pinned_fibres(sorted(rows))
            counts['role_joints'] += 1
            counts['role_literal_fibres'] += 16
            counts['role_empty_fibres'] += sum(not f['complete_triples'] for f in fibres)
            check(not any(row[0] != row[1] for row in rows), f"intact abstract join {case['name']}/{jid}")
            controls.append(dict(case_id=case['id'],case_name=case['name'],local_id=case['local_id'],
                                 side_join_id=jid,side_ids=[zid,wid],z_role=roles[zid],w_role=roles[wid],
                                 complete_root_P3_rows=sorted(rows),fibres_without_zw=fibres,
                                 fibres_with_zw=[dict(roots=list(p),complete_triples=[]) for p in PAIRS]))
    check(len(controls) == 14000, "14000 necessary full role joins")
    return roles, derived_cases, joins_by_a, saved_relations, controls, counts


def geometry_audit(data, roles, cases, local_relations):
    """Re-derive equations (7)--(9), not saved geometry/exclusion flags."""
    subsets = powerset(tuple(range(5)))[1:]
    perms = list(permutations(range(4)))
    candidate_supports = {}
    for residual in {tuple(c[k]) for c in cases for k in ('z_residual','w_residual')}:
        candidate_supports[residual] = [s for s in subsets if all(
            set(residual) == {p[c] for c in residual}
            for p in perms if all(p[Q[b]] == Q[b] for b in s))]
    retained = []
    counts = Counter()
    for case in cases:
        supports = local_relations[case['local_id']]['actual_supports']
        S0,S1,S2 = supports
        possible = []
        for left in S0:
            right = min(v if v>left else v+5 for v in S0 if v != left)
            lift1 = sorted(v if v>=left else v+5 for v in S1)
            lift2 = S2[0] if S2[0]>=left else S2[0]+5
            if max(lift1)>right or lift2>right:
                continue
            cuts = [left] + lift1 + [right]
            for child in range(3):
                if cuts[child] <= lift2 <= cuts[child+1]:
                    possible.append((left,right,lift1,lift2,child,cuts[child],cuts[child+1]))
        choices = [candidate_supports[tuple(case[k])] for k in ('z_residual','w_residual')]
        counts['support_candidates'] += len(choices[0])*len(choices[1])
        count = 0
        for Az,Aw in product(*choices):
            found = None
            for left,right,lift1,lift2,child,jleft,jright in possible:
                blocks = [sorted(v if v>=left else v+5 for v in s) for s in (Az,Aw,S2)]
                if any(min(b)<jleft or max(b)>jright for b in blocks):
                    continue
                # x2 tether sits first or last; only the two root collars may
                # exchange. Shared original boundary endpoints remain legal.
                orders = [(2,0,1),(2,1,0),(0,1,2),(1,0,2)]
                valid = [o for o in orders if all(max(blocks[i]) <= min(blocks[j]) for i,j in zip(o,o[1:]))]
                if valid:
                    found = dict(id=len(retained),case_id=case['id'],case_name=case['name'],local_id=case['local_id'],
                                 actual_side_supports=[list(Az),list(Aw)],anchor=left,I=[left,right],
                                 S1_lifts=lift1,child=child,J=[jleft,jright],S2_lift=lift2,
                                 block_lifts=blocks,named_order=[['A_z','A_w','S2'][i] for i in valid[0]])
                    break
            if found:
                retained.append(found)
                count += 1
        counts['retained_cases' if count else 'empty_cases'] += 1
    saved = data['geometry']['retained_geometries']
    check(len({canon(g) for g in saved}) == len(saved), "duplicate saved geometry rows")
    check(retained == saved, "complete geometry identities/supports/lifts differ")
    check(dict(counts) == {'support_candidates':114048,'empty_cases':524,'retained_cases':36}, "geometry candidate counts")
    check(len(retained) == 140, "140 complete geometry records")
    actual_case_map = {cid: sorted(g['id'] for g in retained if g['case_id']==cid) for cid in range(560)}
    for row in data['geometry']['case_results']:
        check(row['geometry_ids'] == actual_case_map[row['case_id']], "complete per-case geometry ledger")
    retained_ids = {g['case_id'] for g in retained}
    check(sum(len(cases[cid]['side_join_ids']) for cid in retained_ids) == 900, "900 retained role joins")
    return retained, dict(counts)


def symmetry_audit(data, local_relations):
    outputs = []
    counts = Counter()
    local = data['local']['configurations']
    rho,pi = (3,2,1,0,4),(1,0,2,3)
    lookup = {tuple(map(tuple,r['actual_supports'])):r for r in local_relations}
    for row in data['local']['symmetries']:
        lid = row['local_id']
        supports = local_relations[lid]['actual_supports']
        reverse = row['path_reverse']
        mapped = tuple(reversed(supports)) if reverse else supports
        triples = brute_relation(mapped, roots=False)
        check(set(triples) == {tuple(reversed(t)) if reverse else tuple(t) for t in local_relations[lid]['complete_triples']},
              f"path reversal complete relation {lid}")
        contact = 7 if reverse else 9
        edges = original_edges(mapped, roots=False)|{(5,contact),(6,contact)}
        witnesses = colorings(range(10),edges,dict(enumerate(Q)))
        rows = sorted(tuple(w[v] for v in (5,6,7,8,9)) for w in witnesses)
        fibres = pinned_fibres(rows)
        F = [f['roots'] for f in fibres if not f['complete_triples']]
        check(sum(1<<(4*z+w) for z,w in F)==row['forbidden_pair_mask'], "symmetry forbidden relation")
        check(sum(1<<(16*t[0]+4*t[1]+t[2]) for t in triples)==row['vertex_tuple_mask'], "symmetry triple mask")
        if row['root_swap']:
            check({(w,z,*t) for z,w,*t in rows} == set(rows), f"same-frame root exchange {lid}")
        counts['literal_fibres'] += 16
        counts['empty_fibres'] += len(F)
        outputs.append(dict(local_id=lid,root_swap=row['root_swap'],path_reverse=reverse,
                            actual_supports=mapped,actual_edges=sorted(edges),complete_triples=triples,
                            fibres_without_zw=fibres))
    check(len(outputs)==336, "336 full symmetry controls")
    reflection = []
    for r in local:
        if not r['forbidden_pair_mask']:
            continue
        new_supports=tuple(tuple(sorted(rho[v] for v in s)) for s in r['actual_supports'])
        reflected=lookup[new_supports]
        expected={tuple(pi[c] for c in t) for t in r['complete_triples']}
        check(expected==set(map(tuple,reflected['complete_triples'])), "shared-color reflection relation")
        check(reflected['local_id']==r['reflected_local_id'], "named reflection local ID")
        reflection.append(dict(local_id=r['id'],reflected_local_id=reflected['local_id'],vertex_map=rho,color_map=pi,
                               complete_reflected_triples=sorted(expected)))
    return outputs,reflection,dict(counts)


def narrow_identity_audit(c,c2,roles,cases,joins,geometries):
    i=c2['identity']
    lid=134; cid=86; gid=30; jid=20
    check(i['local']==c['local']['configurations'][lid], "C2 full parent local JSON")
    check(i['case']==cases[cid], "C2 full parent case JSON")
    check(i['geometry']==geometries[gid], "C2 full parent geometry JSON")
    check(i['parent_entry']==c['next_entry'], "C2 parent entry full JSON")
    check(joins[1][jid]==(8,1), "named join 20 original side IDs")
    check(roles[8]==dict(spoke_colors=[],unary_contacts=[3],unary_forbidden=[[0,2,3]],residual=[1]), "z original unary identity")
    check(roles[1]==dict(spoke_colors=[],unary_contacts=[3],unary_forbidden=[[0,2]],residual=[1,3]), "w original unary identity")
    check(geometries[gid]['actual_side_supports']==[[1],[2,4]], "original actual own/side support")
    e=i['next_entry']
    check(e['case_name']=='CPP-134-1' and e['side_join_id']==20 and e['geometry_id']==34, "successor remains same case/join")
    check(e['geometry']==geometries[34] and e['geometry']['actual_side_supports']==[[1,2],[2,4]], "successor actual support is preserved")
    check(e['z_role']==roles[8] and e['w_role']==roles[1], "successor keeps complete unary identities")
    expected_context=original_edges(((0,1,4),(1,4),(4,)),zw=True)
    check(set(map(tuple,i['original_context_edges']))==expected_context, "full original B/P3/root context edges")
    check(i['original_P3_lists']==[[3],[0,3],[0,1,3]], "C2 original lists")
    check(normalized_rows(i['original_P3_forbidden'],'C2 P3 forbidden')=={(1,3),(3,1)}, "C2 full P3 forbidden")
    check(i['original_root_join_with_zw']==[] and i['original_root_join_without_zw']==[[1,1]], "C2 diagonal/no intact join")
    predecessor_counts=(len({g['case_id'] for g in geometries}),len(geometries),sum(len(cases[cid]['side_join_ids']) for cid in {g['case_id'] for g in geometries}))
    check(predecessor_counts==(36,140,900), "predecessor actual arrays remain intact")
    summary=c2['summary']
    check((summary['predecessor_cases'],summary['predecessor_geometries'],summary['predecessor_joins'])==predecessor_counts, "C2 preserved predecessor counts")
    check(summary['named_source_branches_closed']==1 and summary['predecessor_deletions']==0, "one named source branch, zero predecessor deletions")
    same_case=[g for g in geometries if g['case_id']==cid]
    check(len(same_case)==6, "whole case retains six geometries")
    expanded=[(g['id'],j) for g in same_case for j in cases[cid]['side_join_ids']]
    remaining=[entry for entry in expanded if entry!=(30,20)]
    check(len(expanded)==150 and len(remaining)==149, "only one geometry/side identity closure")
    geometry30_other_joins=[j for j in cases[cid]['side_join_ids'] if j!=20]
    check(len(geometry30_other_joins)==24, "geometry 30 other 24 side joins preserved")
    return dict(closed_identity=dict(case_id=cid,case_name='CPP-134-1',geometry_id=gid,side_join_id=jid,side_ids=[8,1]),
                predecessor_actual_counts=dict(cases=36,geometries=140,case_role_joins=900),
                retained_case_geometry_ids=[g['id'] for g in same_case],retained_case_side_join_ids=cases[cid]['side_join_ids'],
                same_case_geometry_side_domain=expanded,remaining_same_case_geometry_side_domain=remaining,
                geometry30_other_side_join_ids=geometry30_other_joins,
                successor=i['next_entry'],
                note='150 geometry/side combinations are a Cartesian necessary domain, not 150 serialized original graph sources; the historical 900 count is case/side roles.')


def negative_controls(c,c2):
    triples=[tuple(t) for t in c['local']['configurations'][134]['complete_triples']]
    roots=(1,3)
    literal=[t for t in triples if t[2] not in roots]
    separately=[ [t for t in triples if t[2]!=r] for r in roots ]
    check(not literal and all(separately), "shared contact negative control premise")
    duplicate_contact=[(left,right) for left,right in product(*separately) if left[:2]==right[:2]]
    check(duplicate_contact==[((3,0,3),(3,0,1))], "literal false duplicated-port witness")
    # A color permutation is legal only when the entire graph, all fixed
    # boundary colors, both roots, and every other relation move together.
    pi=(1,0,2,3)
    moved=[tuple(pi[v] for v in t) for t in triples]
    false_fibre=[t for t in moved if t[2] not in roots]
    check(false_fibre==[(3,1,0)], "independent frame mutation witness")
    witness=dict(enumerate(Q))|{5:roots[0],6:roots[1]}|dict(zip((7,8,9),false_fibre[0]))
    original=original_edges(((0,1,4),(1,4),(4,)))
    bad_edges=sorted(e for e in original if witness[e[0]]==witness[e[1]])
    check(bad_edges==[(1,8)], "wrong frame actual original-edge conflict")
    unary=[tuple(t) for t in c2['forced_triangle']['complete_contact_tuples']]
    marginals=[sorted({t[i] for t in unary}) for i in range(3)]
    product_rows=list(product(*marginals))
    fake=(0,0,0)
    check(len(unary)==6 and len(product_rows)==27 and fake in product_rows and fake not in unary,
          "complete unary tuple negative control")
    actual_forbidden=set.intersection(*(set(t) for t in unary))
    false_forbidden=set.intersection(*(set(t) for t in product_rows))
    check(actual_forbidden=={0,2,3} and not false_forbidden, "marginals lose unary forbidden relation")
    return dict(shared_contact=dict(local_id=134,roots=roots,complete_triples=triples,complete_fibre=literal,
                                    separate_root_fibres=separately,false_duplicate_x2_pair=duplicate_contact,
                                    lost_identity='x2 is one original vertex shared by both roots'),
                wrong_independent_frame=dict(local_id=134,roots=roots,original_Q=Q,permutation=pi,
                                             permuted_C_only_triples=moved,false_fibre=false_fibre,
                                             false_original_coloring=witness,violated_actual_edges=bad_edges),
                unary_marginals=dict(ordered_contacts=[10,11,12],complete_tuples=unary,marginals=marginals,
                                     marginal_cartesian_product=product_rows,false_tuple=fake,
                                     original_forbidden=sorted(actual_forbidden),false_forbidden=sorted(false_forbidden)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',default='.')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    root=Path(args.repo).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    inputs=['artifacts/c5_mixed_p3_common_endpoint/observations.json','artifacts/c5_mixed_p3_common_endpoint/rotation_controls.json',
            'artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json']
    hashes={p:sha256((root/p).read_bytes()).hexdigest() for p in inputs}
    write(out/'input_sha256.json',hashes)
    try:
        c=json.loads((root/inputs[0]).read_bytes());c2=json.loads((root/inputs[2]).read_bytes())
        roles,cases,joins,local,role_controls,counts=local_audit(c)
        write(out/'local_relations.json',local)
        write(out/'role_joints.json',dict(scope='complete C P3 relation plus literal abstract unary side-role constraints; no unary source graph is serialized',ordered_vertices=[5,6,7,8,9],records=role_controls))
        geometries,gcounts=geometry_audit(c,roles,cases,local)
        write(out/'derived_geometries.json',geometries)
        symmetries,reflections,scounts=symmetry_audit(c,local)
        write(out/'symmetry_relations.json',dict(root_path=symmetries,reflection=reflections))
        narrow=narrow_identity_audit(c,c2,roles,cases,joins,geometries)
        write(out/'narrow_scope.json',narrow)
        negatives=negative_controls(c,c2)
        write(out/'negative_controls.json',negatives)
        check(hashes=={p:sha256((root/p).read_bytes()).hexdigest() for p in inputs}, "input bytes changed during audit")
        result=dict(status='PASS',input_root=str(root),input_sha256=hashes,
                    audit_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                    complete_P3_relations=500,complete_side_roles=len(roles),
                    complete_named_cases=len(cases),counts=dict(counts),geometry_counts=gcounts,symmetry_counts=scounts,
                    retained_actual_geometries=len(geometries),narrow_scope=narrow['closed_identity'],
                    negative_controls=3,
                    boundaries=['No production imports, enumerator, join helper, or witness validator.',
                                'The complete triples use one fixed q and original named graph edges.',
                                'C arbitrary unary relations are not serialized; role joints do not establish their realization.',
                                'Paper topology, arbitrary-size Gallai arguments, full source minimality, targets, and Lean are outside this finite audit.'])
        write(out/'results.json',result)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    except Exception as error:
        write(out/'failure.json',dict(status='FAIL',error=repr(error),input_sha256=hashes))
        raise


if __name__=='__main__':
    main()
