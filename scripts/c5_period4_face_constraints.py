#!/usr/bin/env python3
"""Exact five-face histories and S5 source necessities; no source census.

The computation is a pointwise relaxation of actual complete component moves.
The source-side shortcut/rim implications are justified by the accompanying
paper proof, never inferred from the history compatibility complex alone.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audits/2026-10-30-c5-period4-s5/face-certificate.json'
SOURCE = ROOT / 'audits/2026-10-29-kempe-realizability/source/controls.json'
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
ROOTS = (2, 4, 1, 3, 0)
ALIGN = (2, 3, 1, 0)
BOUNDARY = ((0, 0, 0, 0, 0, 3), (1, 1, 1, 2, 2, 2),
            (0, 3, 3, 3, 3, 3), (2, 2, 2, 2, 0, 0), (3, 3, 1, 1, 1, 1))


def words():
    answer = []
    for start in range(4):
        rows = [(start,)]
        for a, b in PAIRS:
            new = []
            for row in rows:
                new.append(row + (row[-1],))
                if row[-1] in (a, b):
                    new.append(row + (a + b - row[-1],))
            rows = new
        answer.extend((row, ALIGN[row[-1]]) for row in rows)
    assert len(answer) == len(set(answer)) == 28
    return sorted(answer)


def compatible(a, b):
    return all(x != y for x, y in zip(a, b))


def face_domains():
    answer = []
    for i in range(5):
        domain = [(row, successor) for row, successor in words()
                  if compatible(row, BOUNDARY[i]) and compatible(row, BOUNDARY[(i + 1) % 5])]
        assert len(domain) == 2
        assert {row[0] for row, target in domain} == {target for row, target in domain}
        assert all(row[0] != target for row, target in domain)
        answer.append(domain)
    return answer


def repeat_domain(domain, start, period):
    lookup = {row[0]: (row, target) for row, target in domain}
    answer, current = (), start
    for _ in range(period):
        row, current = lookup[current]
        answer += row
    assert current == start
    return answer


def all_closed_histories(period):
    answer = []
    by_start = defaultdict(list)
    for row, target in words():
        by_start[row[0]].append((row, target))
    for start in range(4):
        states = [((), start)]
        for _ in range(period):
            states = [(prefix + row, target) for prefix, old in states for row, target in by_start[old]]
        answer.extend(row for row, target in states if target == start)
    return sorted(answer)


def finite_history_certificate():
    domains = face_domains()
    four = [[repeat_domain(d, row[0], 4) for row, _ in d] for d in domains]
    phases = []
    closed = all_closed_histories(4)
    assert len(closed) == 2090
    for phase in product(range(2), repeat=5):
        histories = [four[i][phase[i]] for i in range(5)]
        edges = [(i, j) for i, j in combinations(range(5), 2) if compatible(histories[i], histories[j])]
        equalities = [(i, j) for i, j in combinations(range(5), 2) if histories[i] == histories[j]]
        rim = all(tuple(sorted((i, (i + 1) % 5))) in edges for i in range(5))
        cap = [j for j, h in enumerate(closed) if all(compatible(h, w) for w in histories)]
        initial_colors = [h[0] for h in histories]
        rounds = [[h[6*r] for h in histories] for r in range(4)]
        phases.append(dict(phase=phase, compatible_original_w_edges=edges,
                           possible_history_equalities=equalities, complete_rim=rim,
                           compatible_cap_history_ids=cap, initial_w_colors=initial_colors,
                           normalized_round_start_w_colors=rounds))
    rim = [p for p in phases if p['complete_rim']]
    assert [p['phase'] for p in rim] == [(0, 1, 0, 0, 0), (1, 0, 1, 1, 1)]
    assert not any(p['compatible_cap_history_ids'] for p in rim)
    one_round_rim = []
    for phase in product(range(2), repeat=5):
        rows = [domains[i][phase[i]][0] for i in range(5)]
        if all(compatible(rows[i], rows[(i+1) % 5]) for i in range(5)):
            color_sets = [sorted({row[t] for row in rows}) for t in range(6)]
            assert any(len(s) == 4 for s in color_sets)
            one_round_rim.append(dict(phase=phase, w_colors_by_time=[[row[t] for row in rows] for t in range(6)],
                                      times_using_four_colors=[t for t,s in enumerate(color_sets) if len(s)==4]))
    return dict(one_round_domains=[dict(edge=(i,(i+1)%5), words=[dict(history=h, normalized_successor=t) for h,t in d])
                                   for i,d in enumerate(domains)],
                four_round_domains=four, four_round_pointwise_history_count=len(closed),
                four_round_history_sha256=sha256(json.dumps(closed,separators=(',',':')).encode()).hexdigest(),
                phase_assignments=phases, one_round_complete_rim=one_round_rim)


def embedding(edges, faces, n):
    es = {tuple(sorted(e)) for e in edges}
    incidence = defaultdict(list)
    successors = [dict() for _ in range(n)]
    for j, face in enumerate(faces):
        for i in range(3):
            u,a,b = face[i],face[(i+1)%3],face[(i+2)%3]
            assert a not in successors[u]
            successors[u][a] = b
            incidence[tuple(sorted((u,a)))].append(j)
    assert set(incidence)==es and all(len(x)==2 for x in incidence.values())
    assert n-len(es)+len(faces)==2
    rotation=[]
    for s in successors:
        first=min(s); r=[first]
        while s[r[-1]]!=first:
            r.append(s[r[-1]])
            assert len(r)<=len(s)
        assert len(r)==len(s)
        rotation.append(r)
    return incidence,rotation


def sides_of_cycle(cycle, faces, incidence):
    cut={tuple(sorted((cycle[i],cycle[(i+1)%len(cycle)]))) for i in range(len(cycle))}
    assert cut<=set(incidence)
    unseen=set(range(len(faces)));result=[]
    while unseen:
        root=min(unseen);unseen.remove(root);queue=[root]
        for j in queue:
            f=faces[j]
            for i in range(3):
                e=tuple(sorted((f[i],f[(i+1)%3])))
                if e not in cut:
                    for k in incidence[e]:
                        if k in unseen:
                            unseen.remove(k);queue.append(k)
        result.append(sorted({v for j in queue for v in faces[j]}-set(cycle)))
    assert len(result)==2
    return sorted(result,key=lambda x:(len(x),x))


def inspect_geometry(source):
    edges=source['original_edges'];faces=source['sphere_faces'];v=source['deleted_vertex'];B=source['boundary']
    n=max(max(e) for e in edges)+1; incidence,rotation=embedding(edges,faces,n)
    es={tuple(sorted(e)) for e in edges};adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    w=[]
    for i in range(5):
        candidates=[f for f in faces if B[i] in f and B[(i+1)%5] in f and v not in f]
        assert len(candidates)==1
        w.append(next(x for x in candidates[0] if x not in (B[i],B[(i+1)%5])))
    assert len(set(w))==5 and not(set(w)&set(B))
    assert all(adj[w[i]]&set(B)=={B[i],B[(i+1)%5]} for i in range(5))
    shortcuts=[]
    for i in range(5):
        for x in sorted(adj[B[i]]-set(B)-{v}):
            for y in sorted(adj[B[(i+2)%5]]-set(B)-{v}):
                if x!=y and y in adj[x]:
                    cycle=[v,B[i],x,y,B[(i+2)%5]]
                    sides=sides_of_cycle(cycle,faces,incidence)
                    middle=next(s for s in sides if B[(i+1)%5] in s)
                    exact=len(middle)==1 and x==w[i] and y==w[(i+1)%5] and len(adj[B[(i+1)%5]])==5
                    if source['topology']['satisfies_structural_class']:
                        assert exact
                    shortcuts.append(dict(i=i,path=[B[i],x,y,B[(i+2)%5]],cycle=cycle,sides=sides,
                                          S5_forced_facial_wheel=exact))
    w_edges=[(i,j) for i,j in combinations(range(5),2) if w[j] in adj[w[i]]]
    nonadj=[(i,j) for i,j in w_edges if (j-i)%5 not in (1,4)]
    if source['topology']['satisfies_structural_class']:
        assert not nonadj
    full_rim=all(tuple(sorted((i,(i+1)%5))) in w_edges for i in range(5))
    rim_sides=sides_of_cycle(w,faces,incidence) if full_rim else None
    if full_rim:
        assert sorted(B+[v]) in rim_sides
    return dict(name=source['name'],S5=source['topology']['satisfies_structural_class'],
                center=v,boundary=B,third_points=w,original_rotation=rotation,
                third_point_original_edges=w_edges,forbidden_nonadjacent_w_edges=nonadj,
                external_three_edge_shortcuts=shortcuts,complete_third_point_rim=full_rim,rim_sides=rim_sides)


def errera_replay(source):
    geometry=inspect_geometry(source); B=source['boundary']; w=geometry['third_points']
    states=source['normalized_colorings']; returns={r['source']:r for r in source['H_returns']}
    cycle=source['H_cycles'][0]; assert len(cycle)==4
    edges=source['exterior_edges'];n=len(states[0]);adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    histories=[[] for _ in range(n)];moves=[]
    domains=face_domains();four=[[repeat_domain(d,row[0],4) for row,_ in d] for d in domains]
    for round_index,state_id in enumerate(cycle):
        q=tuple(states[state_id]); stages=[q]
        ret=returns[state_id]; assert ret['target']==cycle[(round_index+1)%4]
        for step,((a,b),root,stored) in enumerate(zip(PAIRS,ROOTS,ret['moves'])):
            seen={root};queue=[root]
            for u in queue:
                for z in adj[u]:
                    if q[z] in (a,b) and z not in seen:
                        seen.add(z);queue.append(z)
            assert seen==set(stored['component'])
            assert set(B)&seen=={B[root]}
            q=tuple(a+b-c if z in seen else c for z,c in enumerate(q))
            assert list(q)==stored['coloring'] and all(q[u]!=q[z] for u,z in edges)
            assert tuple(q[z] for z in B)==tuple(BOUNDARY[j][step+1] for j in range(5))
            stages.append(q)
            moves.append(dict(round=round_index,step=step,pair=(a,b),root=root,component=sorted(seen),coloring=q))
        assert tuple(ALIGN[c] for c in q)==tuple(states[ret['target']])
        for z in range(n):histories[z].extend(c[z] for c in stages)
    assert [tuple(histories[z]) for z in B]==[h*4 for h in BOUNDARY]
    phase=[four[i].index(tuple(histories[z])) for i,z in enumerate(w)]
    assert geometry['complete_third_point_rim'] and not geometry['S5']
    assert [len(side) for side in geometry['rim_sides']]==[6,6]
    return dict(source=source['name'],original_edges=source['original_edges'],sphere_faces=source['sphere_faces'],
                deleted_vertex=source['deleted_vertex'],boundary=B,initial_coloring=states[cycle[0]],
                cycle_state_ids=cycle,moves=moves,all_vertex_four_round_histories=histories,
                five_third_point_phase=phase,geometry=geometry,
                blocked=any(c['blocked'] for c in source['classes']))


def report():
    old=json.loads(SOURCE.read_text())['controls']
    return dict(schema='c5-period4-common-face-necessities-v1',
                evidence='Exact finite pointwise histories and actual Errera replay; S34/S5 implications are paper topology. No source census or Lean.',
                source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                history_relaxation=finite_history_certificate(),
                fixed_source_geometry=[inspect_geometry(s) for s in old],
                Errera_negative_control=errera_replay(old[0]),
                open='Missing one rim edge is necessary only, not sufficient. No proof excluding S5 period four and no blocked counterexample from these face conditions.')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=report();encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.check:
        assert OUT.read_text()==encoded,'Certificate differs'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(encoded)
    h=result['history_relaxation']
    print(json.dumps(dict(check='OK',phases=len(h['phase_assignments']),closed_four_round_histories=h['four_round_pointwise_history_count'],
                         complete_rim_phases=[p['phase'] for p in h['phase_assignments'] if p['complete_rim']],
                         cap_histories_for_complete_rim=0,fixed_sources=len(result['fixed_source_geometry']),
                         Errera_S5=False,Errera_complete_moves=20),sort_keys=True))


if __name__=='__main__':main()
