#!/usr/bin/env python3
"""E2/951: named necessary interfaces, local controls, and a bounded realization probe.

No graph-size theorem follows from the probe.  The (2,2) ledger treats the
subcase where BOTH rejected rows have the full original graph as minimal core;
the proper-core t=2 branch is recorded separately as open.
Paper documentation inputs are pinned to the assigned ca3870f baseline so
unrelated concurrent wording edits cannot rewrite this task's provenance.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess

import networkx as nx

import c5_single_spoke_two_two as old

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_one_e2_951_remaining/observations.json'
SUBOUT = OUT.with_name('subdivisions.json')
SIDEOUT = OUT.with_name('interior_bridges_and_sidebranches.json')
FINALOUT = OUT.with_name('final_sidebranch_terminal_blocks.json')
SOURCE = ROOT / 'artifacts/c5_single_spoke_residual_locality/observations.json'
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
U = frozenset(range(4))
Q = tuple(old.Q)
PERMS = tuple(permutations(range(4)))
FAR = (((0, 1, 2, 0, 1), 2), ((0, 1, 2, 0, 2), 1))


def key(r):
    return r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans']))


def align(s, supports, bans, row, singleton):
    """ONE whole-graph D5/S4 map; both component names/coordinates persist."""
    shift = (4-singleton) % 5
    moved = [row[(i-shift) % 5] for i in range(5)]
    pi = {c: Q[i] for i, c in enumerate(moved)}
    pi[3] = 3
    assert len(pi) == 4 and len(set(pi.values())) == 4
    ns = (s+shift) % 5
    ss = [sorted((i+shift) % 5 for i in x) for x in supports]
    fs = [sorted(pi[c] for c in x) for x in bans]
    reflected = ns not in (0, 1, 4)
    if reflected:
        ns = old.RHO[ns]
        ss = [sorted(old.RHO[i] for i in x) for x in ss]
        fs = [sorted(old.PI[c] for c in x) for x in fs]
    return (ns, tuple(map(tuple, ss)), tuple(map(tuple, fs))), dict(
        rotation=shift, colour_map=[pi[c] for c in range(4)],
        q_preserving_reflection=reflected)


@lru_cache(None)
def local_supports(support, q, p, eq, ep):
    """Rooted side-branch residual constraints, with all actual T retained."""
    result = []
    for n in range(len(support)+1):
        for t in combinations(support, n):
            if any({pi[c] for c in eq} != set(eq) for pi in PERMS
                   if all(pi[q[i]] == q[i] for i in t)):
                continue
            if any({pi[c] for c in ep} != set(ep) for pi in PERMS
                   if all(pi[p[i]] == p[i] for i in t)):
                continue
            fixed = {c for c in U if all((q[i] == c) == (p[i] == c) for i in t)}
            if set(eq) & fixed != set(ep) & fixed:
                continue
            if any({pi[c] for c in eq} != set(ep) for pi in PERMS
                   if all(pi[q[i]] == p[i] for i in t)):
                continue
            result.append(t)
    return tuple(result)


def arc_partitions():
    result = []
    for cuts in combinations(range(5), 3):
        arcs = [tuple(i % 5 for i in range(a, b))
                for a, b in zip(cuts, (*cuts[1:], cuts[0]+5))]
        result.extend(permutations(arcs))
    assert len(result) == 60
    return tuple(result)


PARTITIONS = arc_partitions()


def common_minor(t0, t1, exterior):
    for x, y, d in PARTITIONS:
        if set(d) & set(exterior) and all(set(t) & set(x) and set(t) & set(y)
                                        for t in (*t0, *t1)):
            landing = min(set(d) & set(exterior))
            return dict(frame_arcs=[x, y, d], exterior_landing=landing,
                        branch_sets=['W0', 'W1', 'X', 'Y',
                                     '(original root cycle minus x0,x1) + '
                                     'original exterior path + D'])
    return None


def component_locality(record, k):
    qban, pban = record['q_forbidden'][k], record['far_forbidden'][k]
    if len(qban) == len(pban) == 1:
        return None
    q, p = Q, tuple(record['far_row'])
    support = tuple(record['supports'][k])
    exterior = sorted({record['spoke']} | set(record['supports'][1-k]))
    variants = []
    if len(qban) == len(pban) == 2:
        e = local_supports(support, q, p, tuple(qban), tuple(pban))
        minor = common_minor(e, e, exterior) if e else None
        variants.append(dict(kind='both_pair', E_q=qban, E_p=pban,
                             T0=e, T1=e, exclusion='empty_support_family' if not e
                             else 'original_first_bridge_K5' if minor else None,
                             minor=minor))
    else:
        swapped = len(qban) == 1
        if swapped:
            q, p, qban, pban = p, q, pban, qban
        c = pban[0]
        for beta in sorted(U-{c}):
            for gamma in sorted(U-{beta}):
                ep0, ep1 = tuple(sorted((c, beta))), tuple(sorted((beta, gamma)))
                t0 = local_supports(support, q, p, tuple(qban), ep0)
                t1 = local_supports(support, q, p, tuple(qban), ep1)
                minor = common_minor(t0, t1, exterior) if t0 and t1 else None
                variants.append(dict(kind='pair_then_singleton', pair_row=q,
                                     singleton_row=p, pair_forbidden=qban,
                                     singleton_forbidden=c,
                                     first_bridge_palette=beta,
                                     next_bridge_palette=gamma,
                                     E_singleton_x0=ep0, E_singleton_x1=ep1,
                                     T0=t0, T1=t1,
                                     exclusion='empty_support_family' if not t0 or not t1
                                     else 'original_first_bridge_K5' if minor else None,
                                     minor=minor))
    return dict(component=f'C{k}', original_contacts=[f'C{k}.0', f'C{k}.1'],
                original_path='the unique bridge path between these original contacts',
                original_blocks=['W0 at first original path vertex',
                                 'W1 at second original path vertex'],
                exterior_boundary_support=exterior, variants=variants,
                excluded=all(v['exclusion'] is not None for v in variants))


def necessary_ledger():
    prior = json.loads(SOURCE.read_text())
    records = [z['original_record'] for z in prior['table']['retained']]
    lookup = {key(r): r['id'] for r in records}
    shield_pass, schedules = [], []
    for r in records:
        supports = list(map(set, r['supports']))
        shields = [{i for i in range(5) if i in x and (i+1) % 5 in x}
                   for x in supports]
        if not all(len(x) >= 3 and len(e) == len(x)-1
                   for x, e in zip(supports, shields)):
            continue
        if shields[0] & shields[1]:
            continue
        s = r['spoke']
        if any({(s-1) % 5, s, (s+1) % 5} <= x for x in supports):
            continue
        shield_pass.append(r['id'])
        for row, singleton in FAR:
            allowed = old.row_record(s, tuple(map(tuple, r['supports'])),
                                     tuple(map(tuple, r['bans'])), row)
            for fs in allowed['rejection_options']:
                if set(fs[0]) & set(fs[1]) or sum(map(len, fs)) != 3:
                    continue
                aligned, move = align(s, supports, fs, row, singleton)
                if aligned not in lookup:
                    continue
                item = dict(id=len(schedules), name=f'951-T1-{r["id"]}-{singleton}-'
                            + '-'.join(''.join(map(str, f)) for f in fs),
                            original_source_id=r['id'], spoke=s,
                            supports=r['supports'], shield_edges=[sorted(e) for e in shields],
                            ordered_contacts=r['ordered_contacts'],
                            original_placements=r['placements'],
                            q_row=Q, q_forbidden=r['bans'], far_row=row,
                            far_singleton=singleton, far_forbidden=fs,
                            whole_graph_alignment=move,
                            aligned_far_minimal_source_id=lookup[aligned],
                            q_ordered_relation_schema_ids=r['relation_schema_ids'],
                            far_relation_schema_ids=[[
                                z['id'] for z in old.SCHEMAS
                                if tuple(z['forbidden']) == tuple(f)
                                and all({tuple(pi[c] for c in t) for t in z['tuples']}
                                        == set(z['tuples']) for pi in PERMS
                                        if all(pi[row[i]] == row[i] for i in support))]
                                for support, f in zip(r['supports'], fs)],
                            relation_scope='each row schema is a necessary FULL ordered '
                            'two-contact relation; cross-row realizability is unknown')
                locality = [component_locality(item, k) for k in range(2)]
                item['component_locality'] = locality
                item['excluded'] = any(z is not None and z['excluded'] for z in locality)
                schedules.append(item)
    assert len(shield_pass) == 30 and len(schedules) == 54
    assert sum(not r['excluded'] for r in schedules) == 18
    return dict(prior_retained_source_records=len(records),
                shield_pass_source_ids=shield_pass,
                scopes='t=1,(2,2), BOTH rejected rows have full G as minimal core',
                ordered_relation_schemas=old.SCHEMAS, schedules=schedules)


def all_unit_controls(rows):
    three = [tuple(b) for b in rows if len(set(b)) == 3]
    t4 = [tuple(b) for b in rows if len(set(b)) == 4]
    result = []
    for rotation in range(5):
        spokes = sorted((rotation+i) % 5 for i in (0, 2, 4))
        supports = [sorted((rotation+i) % 5 for i in inds)
                    for inds in ((0, 1, 2), (2, 3, 4))]
        rainbow = [b for b in three if len({b[i] for i in spokes}) == 3]
        assert len(rainbow) == 1
        for q in three:
            if q in rainbow:
                continue
            carrier = [k for k, support in enumerate(supports)
                       if len({q[i] for i in support}) == 3]
            assert len(carrier) == 1
            k = carrier[0]
            witness = next((dict(row=b, common_S4_permutation=pi,
                                 available_root_colours=sorted(U-{b[i] for i in spokes}),
                                 transported_full_unary_forbidden=[pi[3]])
                            for b in t4 for pi in PERMS
                            if all(pi[q[i]] == b[i] for i in supports[k])
                            and U-{b[i] for i in spokes} <= {pi[3]}), None)
            assert witness
            result.append(dict(name=f'951-T3-UU-{rotation}-{three.index(q)}',
                               spokes=spokes, original_unary_supports=supports,
                               q=q, unique_possible_D_carrier=f'U{k}',
                               conditional_full_unary_forbidden=[3], T4_rejection=witness))
    assert len(result) == 20
    return dict(scope='arbitrary-size paper support transport plus these 20 finite controls',
                implication='t=3,(1,1), accepting T4 => at most one rejected singleton row',
                controls=result)


def relation(vs, edges, attachments, contacts, row):
    """Exact ordered relation plus a complete coloring witness for EVERY tuple."""
    adj = {v: set() for v in vs}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    lists = {v: sorted(U-{row[i] for i in attachments[v]}) for v in vs}
    assignment, result = {}, {}
    def visit(j):
        if j == len(vs):
            pair = tuple(assignment[v] for v in contacts)
            result.setdefault(pair, tuple(assignment[v] for v in vs))
            return
        v = vs[j]
        for c in lists[v]:
            if all(assignment.get(w) != c for w in adj[v]):
                assignment[v] = c
                visit(j+1)
                del assignment[v]
    visit(0)
    return dict(tuples=sorted(result),
                witnesses=[dict(tuple=t, colours=result[t]) for t in sorted(result)],
                forbidden=sorted(set.intersection(*(set(t) for t in result))
                                 if result else U))


@lru_cache(None)
def probe_piece(support, q_forbidden, p_forbidden, p):
    """Only paths on 2/4 points and one triangle; this is NOT a normal-form theorem."""
    retained, counts = [], Counter()
    for kind, n, es, contacts, sizes in [
            ('path2', 2, ((0, 1),), (0, 1), (2, 2)),
            ('path4', 4, ((0, 1), (1, 2), (2, 3)), (0, 3), (2, 2, 2, 2)),
            ('triangle3', 3, ((0, 1), (0, 2), (1, 2)), (0, 1), (1, 1, 2))]:
        for aa in product(*(tuple(combinations(support, z)) for z in sizes)):
            counts[kind+':assignments'] += 1
            if set().union(*map(set, aa)) != set(support):
                continue
            att = dict(enumerate(aa))
            qr = relation(list(range(n)), es, att, contacts, Q)
            if tuple(qr['forbidden']) != q_forbidden:
                continue
            pr = relation(list(range(n)), es, att, contacts, p)
            if tuple(pr['forbidden']) != p_forbidden:
                continue
            counts[kind+':retained'] += 1
            retained.append(dict(kind=kind, vertices=list(range(n)), edges=es,
                                 actual_attachments=aa, ordered_contacts=contacts,
                                 q_full_relation=qr, far_full_relation=pr))
    return retained, dict(sorted(counts.items()))


def realization_probe(ledger, rows):
    schedules, shapes, seen_shapes, candidates = [], [], set(), []
    total = Counter()
    for r in ledger['schedules']:
        if r['excluded']:
            continue
        pieces = []
        for k in range(2):
            args = tuple(r['supports'][k]), tuple(r['q_forbidden'][k]), \
                tuple(r['far_forbidden'][k]), tuple(r['far_row'])
            forms, counts = probe_piece(*args)
            pieces.append(forms)
            if args not in seen_shapes:
                seen_shapes.add(args)
                shapes.append(dict(support=args[0], q_forbidden=args[1],
                                   far_forbidden=args[2], far_row=args[3],
                                   counts=counts, surviving_original_forms=forms))
                total.update(counts)
        joined = Counter()
        for left, right in product(*pieces):
            all_rel = []
            for b in rows:
                rels = [relation(z['vertices'], z['edges'],
                                 dict(enumerate(z['actual_attachments'])),
                                 z['ordered_contacts'], b) for z in (left, right)]
                tuples = [(a, *t0, *t1) for a in sorted(U-{b[r['spoke']]})
                          for t0 in rels[0]['tuples'] for t1 in rels[1]['tuples']
                          if a not in t0 and a not in t1]
                all_rel.append(dict(row=b, full_piece_relations=rels,
                                    ordered_joint_contacts=['r', 'C0.0', 'C0.1',
                                                            'C1.0', 'C1.1'],
                                    full_joint_tuples=tuples))
            mask = sum(1 << i for i, z in enumerate(all_rel) if z['full_joint_tuples'])
            joined[str(mask)] += 1
            total['joined_fixed_graphs'] += 1
            if not all(mask >> i & 1 for i in (2, 5, 7, 8, 9)):
                continue
            es = {tuple(sorted((i, (i+1) % 5))) for i in range(5)} | {(r['spoke'], 5)}
            actual, next_vertex = [], 6
            for k, z in enumerate((left, right)):
                move = {v: next_vertex+v for v in z['vertices']}
                es |= {tuple(sorted((move[u], move[v]))) for u, v in z['edges']}
                es |= {tuple(sorted((move[v], i))) for v in z['vertices']
                       for i in z['actual_attachments'][v]}
                es |= {(5, move[v]) for v in z['ordered_contacts']}
                actual.append(dict(name=f'C{k}', original_vertices=list(move.values()),
                                   original_contacts=[move[v] for v in z['ordered_contacts']],
                                   actual_attachments={str(move[v]): z['actual_attachments'][v]
                                                       for v in z['vertices']}))
                next_vertex += len(z['vertices'])
            assert sum(5 in e for e in es) == 5
            assert all(sum(v in e for e in es) == 4 for v in range(6, next_vertex))
            assert mask in (1014, 1006)
            g = nx.Graph()
            g.add_edges_from(sorted(es))
            g.add_edges_from((next_vertex, i) for i in range(5))
            disk, cert = nx.check_planarity(g, counterexample=True)
            candidates.append(dict(name=r['name']+f'-graph-{len(candidates)}',
                                   ordered_boundary=list(range(5)), edges=sorted(es),
                                   original_components=actual, full_sigma_mask=mask,
                                   ten_full_relations=all_rel, boundary_apex=next_vertex,
                                   disk=disk,
                                   apex_rotation=dict(cert.get_data()) if disk else None,
                                   nonplanar_subgraph_edges=sorted(tuple(sorted(e))
                                                                  for e in cert.edges())
                                   if not disk else None))
        schedules.append(dict(name=r['name'], original_source_id=r['original_source_id'],
                              candidate_piece_counts=list(map(len, pieces)),
                              joined_full_sigma_distribution=dict(sorted(joined.items()))))
    return dict(scope='directed ORIGINAL fixed graphs only; paths2/4 or triangle3 in '
                'each original component; NO arbitrary-size exclusion',
                counts=dict(sorted(total.items())), unique_piece_shapes=shapes,
                named_schedule_results=schedules, T4_accepting_graph_candidates=candidates)


def failed_concrete_control(rows):
    """A disk graph rejecting nonadjacent q4/q2, but additionally rejecting T4."""
    es = {tuple(sorted((i, (i+1) % 5))) for i in range(5)} | {
        (0, 5), (2, 5), (4, 5), (5, 6), (5, 9), (6, 7), (6, 8), (7, 8),
        (0, 6), (0, 7), (1, 7), (1, 8), (2, 8), (2, 9), (3, 9), (4, 9)}
    vs = list(range(5, 10))
    inner = [e for e in es if min(e) >= 5]
    att = {v: sorted(w for e in es if v in e for w in e if w < 5) for v in vs}
    rels = [relation(vs, inner, att, vs, row) for row in rows]
    mask = sum(1 << i for i, rel in enumerate(rels) if rel['tuples'])
    assert mask == 982 and not (mask >> 5 & 1)
    g = nx.Graph()
    g.add_edges_from(sorted(es))
    g.add_edges_from((10, i) for i in range(5))
    disk, rotation = nx.check_planarity(g)
    assert disk
    return dict(name='951-failed-T3-UU-triangle-plus-leaf', ordered_boundary=list(range(5)),
                edges=sorted(es), original_root=5, original_contacts=[6, 9],
                original_components=[dict(vertices=[6, 7, 8], actual_support=[0, 1, 2]),
                                     dict(vertices=[9], actual_support=[2, 3, 4])],
                complete_inner_degrees=[sum(v in e for e in es) for v in vs],
                epsilon=1, full_sigma_mask=mask, ten_complete_relations=rels,
                reason='rejects T4 pattern_order[5]=01203 as well as q4/q2; '
                'therefore NOT a counterexample to E',
                boundary_apex=10, apex_rotation=rotation.get_data())


def build():
    assert nx.__version__ == '3.5'
    rows = json.loads(CELLS.read_text())['pattern_order']
    ledger = necessary_ledger()
    inputs = [SOURCE, CELLS, ROOT / 'scripts/c5_single_spoke_two_two.py',
              ROOT / 'scripts/c5_single_spoke_cores.py',
              ROOT / 'docs/c5_single_spoke_branch_palettes.md',
              ROOT / 'docs/c5_unary_shield_budget.md']
    return dict(schema=1, evidence=dict(paper='conditional rooted residual and '
                                      'support-transport arguments; full E2(b) unresolved',
                                      external='inherited degree-list/Gallai characterization',
                                      python='finite controls and explicitly bounded realization probe',
                                      lean='none added'),
                input_sha256={str(p.relative_to(ROOT)): sha256(
                    subprocess.check_output(['git', 'show', 'ca3870f:'+str(p.relative_to(ROOT))],
                                            cwd=ROOT)
                    if str(p.relative_to(ROOT)).startswith('docs/') else p.read_bytes()).hexdigest()
                              for p in inputs},
                t1_double_minimal_ledger=ledger,
                all_unit_t3=all_unit_controls(rows),
                bounded_realization_probe=realization_probe(ledger, rows),
                concrete_failed_control=failed_concrete_control(rows),
                additional_unresolved_branches=[dict(
                    name='951-T2-C2-U-omit-U', root_degree=5, root_spokes=2,
                    original_contacts=['C2.x', 'C2.y', 'U.u'],
                    original_contact_partition=[2, 1],
                    proper_core='G minus original unary U, preserving both original spokes '
                    'and complete original C2; every remaining inner degree4',
                    status='not covered by archived added-SPOKE (592) certificate; '
                    'needs actual ordered binary relation with unary reattachment')])


def build_subdivisions(result):
    """Replay subdivisions from actual saved edges; no planarity oracle here."""
    controls = []
    for record in result['bounded_realization_probe']['T4_accepting_graph_candidates']:
        assert not record['disk']
        source = {tuple(e) for e in record['edges']} | {
            tuple(sorted((i, record['boundary_apex']))) for i in range(5)}
        es = {tuple(e) for e in record['nonplanar_subgraph_edges']}
        assert es <= source
        adj = {}
        for u, v in es:
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
        branch = sorted(v for v in adj if len(adj[v]) != 2)
        paths, visited = [], set()
        for start in branch:
            for first in sorted(adj[start]):
                edge = tuple(sorted((start, first)))
                if edge in visited:
                    continue
                path, previous, current = [start, first], start, first
                visited.add(edge)
                while current not in branch:
                    nxt = next(iter(adj[current]-{previous}))
                    visited.add(tuple(sorted((current, nxt))))
                    path.append(nxt)
                    previous, current = current, nxt
                paths.append(path)
        assert visited == es
        internals = [v for path in paths for v in path[1:-1]]
        assert len(internals) == len(set(internals)) and not set(internals) & set(branch)
        reduced = {tuple(sorted((p[0], p[-1]))) for p in paths}
        assert len(reduced) == len(paths)
        if len(branch) == 5:
            assert reduced == set(combinations(branch, 2))
            kind, parts = 'K5 subdivision', None
        else:
            assert len(branch) == 6 and len(reduced) == 9
            left = next((part for part in combinations(branch, 3)
                         if reduced == {tuple(sorted((u, v))) for u in part
                                        for v in set(branch)-set(part)}), None)
            assert left is not None
            kind, parts = 'K3,3 subdivision', [list(left), sorted(set(branch)-set(left))]
        controls.append(dict(name=record['name'], full_sigma_mask=record['full_sigma_mask'],
                             kind=kind, branch_vertices=branch, bipartition=parts,
                             actual_paths=paths, boundary_apex=record['boundary_apex'],
                             scope='nonplanarity of this ORIGINAL boundary-apex graph only'))
    assert len(controls) == 14
    return dict(schema=1, evidence='finite actual-path subdivisions, independently replayed '
                'from source edges without a planarity oracle', controls=controls)


def terminal_K5_controls():
    controls = []
    for length in (3, 5, 7):
        for a, b in ((1, 2), (2, 3)):
            cycle = list(range(5, 5+length))
            parent, original_root = 5+length, 6+length
            u, v, cut = cycle[:3]
            es = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
            es |= {tuple(sorted((cycle[i], cycle[(i+1) % length])))
                   for i in range(length)}
            es |= {tuple(sorted(e)) for e in ((u, a), (u, b), (v, a), (v, b),
                                              (cut, parent), (parent, original_root),
                                              (original_root, 0))}
            vertices = set().union(*map(set, es))
            sets = [[u], [v], [a], [b], sorted(vertices-{u, v, a, b})]
            adj = {x: set() for x in vertices}
            for x, y in es:
                adj[x].add(y)
                adj[y].add(x)
            for part in sets:
                reached, stack = set(), [part[0]]
                while stack:
                    x = stack.pop()
                    if x in reached:
                        continue
                    reached.add(x)
                    stack.extend(adj[x] & set(part)-reached)
                assert reached == set(part)
            witnesses = []
            for i, j in combinations(range(5), 2):
                edge = next((e for e in sorted(es)
                             if set(e) & set(sets[i]) and set(e) & set(sets[j])), None)
                assert edge is not None
                witnesses.append(dict(branches=[i, j], actual_edge=edge))
            controls.append(dict(cycle_length=length, actual_private_attachment_pair=[a, b],
                                 ordered_boundary=list(range(5)), source_edges=sorted(es),
                                 parent=parent, original_root=original_root,
                                 actual_root_spoke=[0, original_root],
                                 adjacent_private_vertices=[u, v], branch_sets=sets,
                                 ten_adjacencies=witnesses,
                                 scope='minor skeleton only, not a complete degree/list realization'))
    return controls


def sidebranch_palette_controls():
    q = (0, 1, 0, 1, 2)
    p = (0, 1, 2, 0, 1)
    controls = []
    for pi in PERMS:
        rq, rp = tuple(pi[c] for c in q), tuple(pi[c] for c in p)
        for pin, contact_attachment, private_pair in product((0, 1), (1, 3), ((1, 2), (2, 3))):
            qcontact = U-{rq[contact_attachment], pi[0]}
            pcontact = U-{rp[contact_attachment], pi[pin]}
            qprivate = U-{rq[i] for i in private_pair}
            pprivate = U-{rp[i] for i in private_pair}
            assert qcontact == qprivate == {pi[2], pi[3]}
            slack = len(pcontact) > 2
            assert slack or pcontact != pprivate
            controls.append(dict(common_S4_permutation=pi, actual_support=[1, 2, 3],
                                 q_row=rq, p_row=rp, parent_q_colour=pi[0],
                                 parent_p_colour=pi[pin],
                                 original_contact_attachment=contact_attachment,
                                 actual_private_attachment_pair=private_pair,
                                 q_contact_list=sorted(qcontact), q_private_list=sorted(qprivate),
                                 p_contact_list=sorted(pcontact), p_private_list=sorted(pprivate),
                                 obstruction='target contact list slack' if slack
                                 else 'target cycle palettes differ on original adjacent vertices'))
    assert len(controls) == 192
    return dict(scope='finite local controls for paper terminal-block proof; '
                'no cutoff on original sidebranch size',
                sole_odd_cycle_contact_private_controls=controls,
                terminal_noncontact_bridge=dict(actual_boundary_support=[1, 2, 3],
                                                q_seen_colours=[0, 1], boundary_edges=3,
                                                required_distinct_colours=3,
                                                obstruction='q degree-list slack'),
                terminal_noncontact_cycle_private_table=[
                    dict(actual_pair=[1, 2], q_list=[2, 3], p_list=[0, 3]),
                    dict(actual_pair=[2, 3], q_list=[2, 3], p_list=[1, 3])],
                terminal_odd_cycle_K5_controls=terminal_K5_controls())


def build_interior_and_sidebranches(result):
    ledger = result['t1_double_minimal_ledger']
    closed, last = [], []
    for r in ledger['schedules']:
        if r['excluded']:
            continue
        proofs = []
        for k in range(2):
            fq, fp = tuple(r['q_forbidden'][k]), tuple(r['far_forbidden'][k])
            q, p = Q, tuple(r['far_row'])
            if sorted(map(len, (fq, fp))) != [1, 2]:
                continue
            if len(fq) == 1:
                q, p, fq, fp = p, q, fp, fq
            c = fp[0]
            if 3 not in fq or c == 3:
                continue
            variants = []
            for a in sorted(U-{3, c}):
                t = local_supports(tuple(r['supports'][k]), q, p, fq,
                                   tuple(sorted((3, a))))
                minor = common_minor(t, t, {r['spoke']} | set(r['supports'][1-k])) if t else None
                variants.append(dict(non_root_colour_even_bridge_palette=a,
                                     E_pair=fq, E_singleton=[a, 3], actual_T0=t, actual_T1=t,
                                     exclusion='empty_support_family' if not t
                                     else 'original_internal_bridge_K5' if minor else None,
                                     minor=minor))
            if all(z['exclusion'] is not None for z in variants):
                proofs.append(dict(original_component=f'C{k}', pair_row=q,
                                   singleton_row=p, pair_forbidden=fq,
                                   singleton_forbidden=c, variants=variants,
                                   paper_mechanism='D belongs to every singleton-row residual; '
                                   'path palettes alternate D/non-D.  If every even bridge '
                                   'were c, exact rooted branch queries would forbid both c,D. '
                                   'Thus an original even bridge has a outside {c,D}.'))
        if proofs:
            closed.append(dict(name=r['name'], original_source_id=r['original_source_id'],
                               original_supports=r['supports'], proofs=proofs))
        else:
            last.append(r)
    assert len(closed) == 14 and {r['original_source_id'] for r in last} == {82, 317, 477, 817}
    sidebranches = []
    for r in last:
        k = next(i for i in range(2) if len(r['q_forbidden'][i]) == 2)
        eq, ep = tuple(r['q_forbidden'][k]), tuple(r['far_forbidden'][k])
        assert eq == ep == (2, 3)
        ts = local_supports(tuple(r['supports'][k]), Q, tuple(r['far_row']), eq, ep)
        singleton_common = set.intersection(*(set(t) for t in ts))
        assert len(singleton_common) == 1
        middle = next(iter(singleton_common))
        edge_incidences = [{middle, (middle-1) % 5}, {middle, (middle+1) % 5}]
        assert all(any(set(e) <= set(t) for e in edge_incidences) for t in ts)
        long_support = set(r['supports'][k])
        long_edges = {i for i in range(5) if i in long_support and (i+1) % 5 in long_support}
        assert len(long_edges) == 3
        # TWO disjoint one-sided blocks cover this entire original C.  Their
        # supports must partition the three shield edges into a 1-edge and
        # a 2-edge interval; exhaust those named possibilities below.
        split_options = []
        for a, b in product(ts, repeat=2):
            sa = {i for i in range(5) if i in a and (i+1) % 5 in a}
            sb = {i for i in range(5) if i in b and (i+1) % 5 in b}
            if sa & sb or sa | sb != long_edges or set(a) | set(b) != long_support:
                continue
            if len(sa) != len(a)-1 or len(sb) != len(b)-1:
                continue
            split_options.append(dict(original_W0_support=a, original_W1_support=b,
                                      original_W0_shield_edges=sorted(sa),
                                      original_W1_shield_edges=sorted(sb)))
        assert len(split_options) == 2
        sidebranches.append(dict(name=r['name'], original_source_id=r['original_source_id'],
                                 original_binary_component=f'C{k}', original_root_spoke=r['spoke'],
                                 q_row=Q, far_row=r['far_row'], original_supports=r['supports'],
                                 common_actual_support_vertex=middle,
                                 every_original_path_block_support_options=ts,
                                 odd_original_path_has_at_most_two_vertices=True,
                                 original_two_block_split_options=split_options,
                                 superseded_by='final_sidebranch_terminal_blocks.json',
                                 historical_mechanism_status='SUPERSEDED (D7 audit): the one-pendant '
                                 'claim below is unproven and carries no arbitrary-size closure; '
                                 'the final terminal-block layer carries it',
                                 paper_mechanism='shield exclusivity applies to the original '
                                 'one-sided Wj; each uses a different edge incident to the common '
                                 'support vertex.  The short block is a singleton.  The long block '
                                 'has one pendant component; its two-contact case contradicts the '
                                 'two-hub principle and its one-contact case contradicts the '
                                 'terminal-block two-row palettes.'))
    return dict(schema=1,
                scope='conditional arbitrary-size paper closure of t=1,(2,2), BOTH rows '
                'having full G as minimal core; this does NOT close all E2/951 branches',
                evidence=dict(paper='original path, rooted exact queries, generalized '
                              'one-sided shields, short-support and hub arguments',
                              external='inherited degree-list/Gallai theorem',
                              python='finite complete local support and actual minor controls',
                              lean='none added'),
                interior_bridge_closed_schedules=closed,
                final_four_sidebranch_schedules=sidebranches,
                sidebranch_local_controls=sidebranch_palette_controls(),
                canonical_two_contact_pendant_hub=dict(
                    q=[0, 1, 0, 1, 2], forbidden_parent_colours=[0, 1],
                    tested_parent_colour=1,
                    outside_colours=dict(r=2, xA=3, xB=1),
                    hubs=['(H minus original pendant P) union (B minus b2)', '{b2}'],
                    neighbour_colours_on_hubs=[1, 0],
                    connecting_original_root_spoke='r-b0',
                    adjacency_original_frame_edges=['b1-b2', 'b2-b3'],
                    parent_outside_pin_existence='other original component forbids only 1 '
                    'and thus has a full tuple avoiding r=2; xA=3,xB=1 satisfy the '
                    'remaining original triangle and attachments'),
                open_schedules_after_this_layer=len(sidebranches),
                superseded_by='final_sidebranch_terminal_blocks.json',
                closure_note='this layer reduces 54 schedules to the four named sidebranch '
                'schedules only; their closure is carried by the final terminal-block layer '
                '(D7 audit, 2026-10-04)')


def build_final_terminal_blocks(result):
    """Cleaner final-four proof: simultaneous WHOLE-C palettes on offpath leaves."""
    side = build_interior_and_sidebranches(result)
    cases = []
    for name, support, source, partner, pairs, spoke in [
            ('canonical-82-317', (1, 2, 3), Q, FAR[0][0], ((1, 2), (2, 3)), 0),
            ('canonical-477-817', (0, 3, 4), FAR[0][0], Q, ((0, 4), (3, 4)), 1)]:
        private_rows = []
        for pi, pair in product(PERMS, pairs):
            qs, ps = tuple(pi[c] for c in source), tuple(pi[c] for c in partner)
            qlist = sorted(U-{qs[i] for i in pair})
            plist = sorted(U-{ps[i] for i in pair})
            assert qlist == sorted((pi[2], pi[3]))
            private_rows.append(dict(common_S4_permutation=pi, actual_support=support,
                                     two_colour_row=qs, partner_row=ps,
                                     actual_private_attachment_pair=pair,
                                     source_private_palette=qlist, partner_private_palette=plist))
        for pi in PERMS:
            values = [r['partner_private_palette'] for r in private_rows
                      if tuple(r['common_S4_permutation']) == pi]
            assert len(values) == 2 and values[0] != values[1]
        # Transport the SIX actual terminal-cycle skeletons where needed.
        skeletons = []
        for base in terminal_K5_controls():
            if spoke == 0:
                moved = base
            else:
                # Reflection i -> 1-i transports {12,23} to {04,34}, 0 -> 1.
                move = lambda v: (1-v) % 5 if v < 5 else v
                moved = dict(cycle_length=base['cycle_length'],
                             actual_private_attachment_pair=sorted(move(v) for v in
                                                                    base['actual_private_attachment_pair']),
                             source_edges=sorted(tuple(sorted((move(u), move(v))))
                                                 for u, v in base['source_edges']),
                             branch_sets=[sorted(move(v) for v in s) for s in base['branch_sets']],
                             actual_root_spoke=[spoke, base['original_root']],
                             ten_adjacencies=[dict(branches=z['branches'],
                                                  actual_edge=sorted(move(v) for v in z['actual_edge']))
                                              for z in base['ten_adjacencies']],
                             scope=base['scope'])
                es = set(map(tuple, moved['source_edges']))
                for witness in moved['ten_adjacencies']:
                    assert tuple(witness['actual_edge']) in es
            skeletons.append(moved)
        cases.append(dict(name=name, actual_long_block_support=support,
                          source_two_colour_row=source, partner_row=partner,
                          original_root_spoke=spoke, terminal_cycle_private_rows=private_rows,
                          terminal_bridge_private_boundary_edges=3,
                          source_seen_boundary_colours=sorted({source[i] for i in support}),
                          terminal_bridge_obstruction='three external boundary edges see only '
                          'two colours, so tight degree lists are impossible',
                          terminal_cycle_mechanism='partner whole-component palette is uniform '
                          'on all private vertices; distinct table palettes force the SAME actual '
                          'boundary pair at every private vertex.  Two adjacent private vertices '
                          'plus this pair and the connected exterior give the actual K5 minor.',
                          actual_terminal_cycle_K5_skeletons=skeletons))
    return dict(schema=1,
                scope='finite controls for the arbitrary-size paper final-four closure; '
                'the arbitrary-size step is a terminal-block argument, not a graph cutoff',
                original_final_four_schedules=side['final_four_sidebranch_schedules'],
                cases=cases, conclusion='no offpath block exists in the original long W block; '
                'its sole original vertex has only two boundary incidences, contradicting '
                'the three-point actual support.  Thus all four schedules are excluded.',
                supersedes='interior_bridges_and_sidebranches.json one-pendant mechanism',
                remaining_t1_double_minimal_schedules=0,
                hypotheses=['same original odd bridge path and original W blocks',
                            'each W block one-sided in H; pure shield lemmas apply',
                            'both binary forbidden projections equal {2,D}',
                            'both whole-C refusal palettes from the external Gallai theorem',
                            'no original root contact lies in a private offpath vertex',
                            'K4 blocks excluded by inherited connected exterior lemma'],
                evidence=dict(paper='arbitrary-size topology and terminal blocks',
                              external='inherited degree-list/Gallai characterization',
                              python='96 joint palette table rows and 12 actual-edge K5 skeletons',
                              lean='none added'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    subdata = json.dumps(build_subdivisions(result), ensure_ascii=False,
                         sort_keys=True, indent=2) + '\n'
    side = build_interior_and_sidebranches(result)
    sidedata = json.dumps(side, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    final = build_final_terminal_blocks(result)
    finaldata = json.dumps(final, ensure_ascii=False,
                           sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
        assert SUBOUT.read_text() == subdata, 'subdivision certificate differs'
        assert SIDEOUT.read_text() == sidedata, 'interior/sidebranch certificate differs'
        assert FINALOUT.read_text() == finaldata, 'terminal-block certificate differs'
    else:
        if OUT.exists() or SUBOUT.exists() or SIDEOUT.exists() or FINALOUT.exists():
            raise SystemExit('refusing to overwrite existing artifact; use --check')
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
        SUBOUT.write_text(subdata)
        SIDEOUT.write_text(sidedata)
        FINALOUT.write_text(finaldata)
    ledger = result['t1_double_minimal_ledger']
    probe = result['bounded_realization_probe']
    print(json.dumps(dict(shield_support_records=len(ledger['shield_pass_source_ids']),
                          double_minimal_schedules=len(ledger['schedules']),
                          local_open_schedules=sum(not r['excluded'] for r in ledger['schedules']),
                          after_interior_bridge_open_schedules=len(side['final_four_sidebranch_schedules']),
                          final_t1_double_minimal_open_schedules=final['remaining_t1_double_minimal_schedules'],
                          all_unit_T4_controls=len(result['all_unit_t3']['controls']),
                          probe_counts=probe['counts'],
                          T4_accepting_fixed_graphs=len(probe['T4_accepting_graph_candidates']),
                          failed_control_mask=result['concrete_failed_control']['full_sigma_mask'],
                          checked=args.check), sort_keys=True))


if __name__ == '__main__':
    main()
