#!/usr/bin/env python3
"""Finite checks of B1, common-cut uncrossing and one weaker-premise countercontrol."""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INPUT_REL = 'audits/2026-10-16-r6-joint-zero-c4c3d99/frozen/audits/2026-10-15-three-edge-matchings-6ddea32/graphs.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v); adj[v].add(u)
    unseen = set(vertices); out = []
    while unseen:
        root = min(unseen); unseen.remove(root); row = {root}; todo = [root]
        while todo:
            for v in adj[todo.pop()] & unseen:
                unseen.remove(v); row.add(v); todo.append(v)
        out.append(sorted(row))
    return out


def perfect_matchings(n, edges):
    incident = {v: [] for v in range(n)}
    for i, (u, v) in enumerate(edges):
        incident[u].append((v, i)); incident[v].append((u, i))
    out = []
    def visit(free, selected):
        if not free:
            out.append(sorted(selected)); return
        u = min(free)
        for v, i in incident[u]:
            if v in free:
                visit(free - {u, v}, selected + [i])
    visit(set(range(n)), [])
    return sorted(out)


def dual(g):
    faces = g['J_faces']; primal = g['J_edges']; verts = g['J_vertices']
    edges = [[i for i, face in enumerate(faces) if set(edge) <= set(face)] for edge in primal]
    require(all(len(edge) == 2 for edge in edges), 'not closed triangular incidence')
    require(len(verts) - len(primal) + len(faces) == 2, 'not sphere Euler')
    for v in verts:
        link = [(face[(face.index(v)+1)%3], face[(face.index(v)+2)%3])
                for face in faces if v in face]
        degree = Counter(u for edge in link for u in edge)
        require(all(d == 2 for d in degree.values()), 'link not 2-regular')
        require(len(components(degree, link)) == 1, 'link disconnected')
    # A connected closed triangulated surface with Euler characteristic two
    # is a sphere. All vertex links and edge incidences were checked above.
    require(len(components(range(len(faces)), edges)) == 1, 'dual disconnected')
    return len(faces), edges


def cut(edges, vertices):
    return [i for i, (u, v) in enumerate(edges) if (u in vertices) != (v in vertices)]


def analyse_family(n, edges, marks, forced, forbidden, pms, m111):
    X = {v for i in forced for v in edges[i]}
    V = sorted(set(range(n)) - X)
    remaining = [(u,v) for i,(u,v) in enumerate(edges)
                 if i != forbidden and u not in X and v not in X]
    family = [i for i,M in enumerate(pms) if set(forced) <= set(M) and forbidden not in M]
    max_size = -1; maximum = []; violations = 0; saturation_checks = 0
    for mask in range(1 << len(V)):
        S = {v for k,v in enumerate(V) if mask >> k & 1}
        comps = components(set(V)-S, remaining)
        odd = [set(c) for c in comps if len(c)%2]
        q = len(odd)
        if q <= len(S):
            continue
        violations += 1
        h = edges[forbidden]
        tau = int(any(h[0] in C for C in odd) and any(h[1] in C for C in odd)
                  and not any(set(h) <= C for C in odd))
        crossings = []
        for pm_index in m111:
            M = set(pms[pm_index])
            require(q == len(S)+2, '111 must force deficiency exactly two')
            require(tau == 1, 'B1 tau must be one')
            row = [sorted(M & set(cut(edges, C))) for C in odd]
            require(all(len(r) == 1 for r in row), 'B1 odd cut not tight')
            require(all(not ({u,v} <= S) and not (u in S and v in X)
                        and not (v in S and u in X) for i in M for u,v in [edges[i]]),
                    'B1 matching uses S-S or S-X')
            for C in (set(c) for c in comps if len(c)%2 == 0):
                require(not (M & set(cut(edges,C))), 'B1 even component not internally matched')
            crossings.append({'matching_index': pm_index, 'odd_component_crossings': row})
            saturation_checks += 1
        if len(S) > max_size:
            max_size = len(S); maximum = []
        if len(S) == max_size:
            maximum.append({'S':sorted(S), 'components':comps, 'tau':tau,
                            'deficiency':q-len(S), 'matching_crossings':crossings})
    require(bool(family) != bool(violations), 'PM/Tutte exhaustive agreement failed')
    return {'forced':forced,'forbidden':forbidden,'family_matching_indices':family,
            'subsets_checked':1 << len(V), 'violating_sets':violations,
            'saturation_checks':saturation_checks, 'maximum_barriers':maximum}


def check_uncrossing(n, edges, pms, m111, families):
    count = 0
    for A in families['110']['maximum_barriers']:
        for B in families['101']['maximum_barriers']:
            for cr in A['components']:
                for kr in B['components']:
                    C,K=set(cr),set(kr); I=C&K; L=C-K; R=K-C; O=set(range(n))-(C|K)
                    if not all([I,L,R,O]):
                        continue
                    if len(I)%2:
                        left,right,zero1,zero2=I,C|K,L,R
                    else:
                        left,right,zero1,zero2=L,R,I,O
                    for i in m111:
                        M=set(pms[i])
                        require(len(M & set(cut(edges,left))) == 1, 'uncrossed left not tight')
                        require(len(M & set(cut(edges,right))) == 1, 'uncrossed right not tight')
                        require(not any((u in zero1 and v in zero2) or (v in zero1 and u in zero2)
                                        for k in M for u,v in [edges[k]]), 'uncrossing zero edge used')
                        count += 1
    return count


def check_small_cuts(n, edges):
    small=[]; cyclic4=[]
    for size in [1,2,3,4]:
        for removed in combinations(range(len(edges)),size):
            left=[edge for i,edge in enumerate(edges) if i not in removed]
            comps=components(range(n),left)
            if len(comps) == 1:
                continue
            if size <= 3:
                small.append({'edges':list(removed),'components':comps})
            if size == 4 and len(comps) == 2 and all(
                sum(u in C and v in C for u,v in left) >= len(C) for C in map(set,comps)):
                cyclic4.append(list(removed))
    return small,cyclic4


def build():
    raw=(ROOT/INPUT_REL).read_bytes(); digest=hashlib.sha256(raw).hexdigest()
    base=json.loads((HERE.parent/'BASE.json').read_text())
    require(any(row.get('path') == INPUT_REL and row['sha256'] == digest
                for row in base['prior_audit_inputs']), 'input custody mismatch')
    data=json.loads(raw); controls=[]
    for index,g in enumerate(data):
        planar='J_vertices' in g
        if planar:
            n,edges=dual(g)
            marks=[g['J_edges'].index(sorted(edge)) for edge in g['marked_original_edges']]
        else:
            n,edges,marks=g['Q_n'],g['Q_edges'],g['marks']
        controls.append((g['name'],g,n,edges,marks,False))
        if index == 1:
            controls.append(('remarked_flipped_icosahedral',g,n,edges,[5,9,29],True))
    result=[]
    for name,g,n,edges,marks,countercontrol in controls:
        pms=perfect_matchings(n,edges)
        comps=[components(range(n),[edge for i,edge in enumerate(edges) if i not in M]) for M in pms]
        even=[i for i,cs in enumerate(comps) if all(len(C)%2 == 0 for C in cs)]
        m111=[i for i,M in enumerate(pms) if set(marks) <= set(M)]
        fam={}
        for label,forced,h in [('110',marks[:2],marks[2]),('101',[marks[0],marks[2]],marks[1])]:
            fam[label]=analyse_family(n,edges,marks,forced,h,pms,m111)
        row={'name':name,'n':n,'edges':edges,'marks':marks,'all_matchings':pms,
             'all_complement_components':comps,'even_matching_indices':even,
             'm111_indices':m111,'even_m111_indices':sorted(set(m111)&set(even)),
             'families':fam,'uncrossing_checks':check_uncrossing(n,edges,pms,m111,fam),
             'source_status':'not triggered'}
        if countercontrol:
            small,cyclic4=check_small_cuts(n,edges)
            require(all(len(r['edges']) == 3 and sorted(map(len,r['components'])) == [1,n-1]
                        for r in small), 'control has nontrivial cut <=3')
            for h in marks[1:]:
                X=set(edges[marks[0]]+edges[h])
                require([i for i,E in enumerate(edges) if set(E)<=X] == sorted([marks[0],h]),
                        'forced pair not induced')
            require(row['even_m111_indices'], 'countercontrol lacks even111')
            require(all(not f['family_matching_indices'] for f in fam.values()), 'joint family nonempty')
            require(cyclic4 == [[9,10,13,17],[17,19,23,28]], 'cyclic4 list changed')
            require(all(not set(marks[1:]) <= set(C) for C in cyclic4), 'fg in cyclic4')
            degree=Counter(u for edge in g['J_edges'] for u in edge)
            require(max(degree.values()) == 6, 'source-failure witness changed')
            row['countercontrol']={'literal_primal_marked_edges':[g['J_edges'][i] for i in marks],
                'all_cuts_at_most_three':small,'all_cyclic_four_cuts':cyclic4,
                'primal_degrees':[[v,degree[v]] for v in sorted(degree)],
                'missing_source_premise':'maximum primal degree is 6; source requires d_J(m)>=7'}
        result.append(row)
    # Explicit non-source algebra control: all odd tight-set pairs for each
    # of the six K3,3 matchings, so uncrossing does not pass vacuously.
    algebra_edges=[[u,v] for u in range(3) for v in range(3,6)]
    algebra_pms=perfect_matchings(6,algebra_edges); algebra_checks=0
    for i,M in enumerate(algebra_pms):
        tight=[list(C) for C in combinations(range(6),3)
               if len(set(M)&set(cut(algebra_edges,set(C)))) == 1]
        barriers=[{'components':[C]} for C in tight]
        fam={'110':{'maximum_barriers':barriers},'101':{'maximum_barriers':barriers}}
        algebra_checks+=check_uncrossing(6,algebra_edges,algebra_pms,[i],fam)
    require(algebra_checks > 0, 'uncrossing algebra control was vacuous')
    return {'input_path':INPUT_REL,'input_sha256':digest,'source_status':'not triggered','controls':result,
            'uncrossing_algebra_control':{'name':'K3,3_all_matching_tight_odd_sets',
                'edges':algebra_edges,'all_matchings':algebra_pms,'checks':algebra_checks,
                'source_status':'not triggered'}}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write',type=Path)
    parser.add_argument('--verify',type=Path); args=parser.parse_args()
    require(bool(args.write) != bool(args.verify), 'exactly one mode required')
    expected=build()
    if args.write:
        with args.write.open('x') as out:
            json.dump(expected,out,indent=2,sort_keys=True); out.write('\n')
    else:
        require(json.loads(args.verify.read_text()) == expected, 'certificate mismatch')
    print(json.dumps({'controls':len(expected['controls']),'source_status':'not triggered',
                      'saturation_checks':sum(f['saturation_checks'] for c in expected['controls'] for f in c['families'].values()),
                      'uncrossing_checks':sum(c['uncrossing_checks'] for c in expected['controls']),
                      'uncrossing_algebra_checks':expected['uncrossing_algebra_control']['checks']},sort_keys=True))


if __name__ == '__main__':
    main()
