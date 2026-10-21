#!/usr/bin/env python3
"""Two fixed same-disk 02/03 controls; these are not original-source witnesses.

The only search is a dynamic program on the named 14-boundary input, with
zero or one interior vertex.  New interior-only palette components are allowed.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'frozen/audits/2026-10-21-w7-L-path-30dde27/six_degree/certificate-v2.json.gz'
P = ('n', 'u4', 'u3', 'u2', 'u1', 'L')
MUTABLE = (*P, 'z5')
Y = 'HL_0'
B14 = ('a', 'z1', 'z2', 'z3', 'z4', 'V', 'U', Y, 'q', 'c', 's', 'v', 'w', 't')
RIM = ('a', *P, 'q', 'c', 's', 'v', 'w', 't')
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')
ZERO = {'G': {'01021', '01202', '01212'}, 'Q1': {'01232'}, 'J1': {'01202', '01212'}}
STRIP = [('n','a','z1'), ('n','u4','z1'), ('u4','z1','z2'), ('u4','u3','z2'),
         ('u3','z2','z3'), ('u3','u2','z3'), ('u2','z3','z4'), ('u2','u1','z4'),
         ('u1','z4','z5'), ('u1','L','z5'), ('L','z5',Y), ('L',Y,'q'),
         ('z5','z4','V'), ('z5','V','U'), ('z5','U',Y)]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def canonical(word):
    seen = {}
    return [seen.setdefault(x, len(seen)) for x in word]


def graph_from_faces(faces):
    graph = {}
    for face in faces:
        for a, b in combinations(face, 2):
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)
    return graph


def components(graph, colors, mate):
    seen, blocks = set(), []
    for v in graph:
        if v in seen:
            continue
        seen.add(v)
        todo, block = [v], []
        while todo:
            a = todo.pop()
            block.append(a)
            for b in graph[a]:
                if b not in seen and (colors[a] in (0, mate)) == (colors[b] in (0, mate)):
                    seen.add(b)
                    todo.append(b)
        blocks.append(sorted(block))
    blocks.sort()
    partition = canonical([next(i for i, block in enumerate(blocks) if v in block) for v in B14])
    return blocks, partition


def check_disk(faces, names, colors):
    require(all(len(set(f)) == 3 for f in faces), 'degenerate triangle')
    graph = graph_from_faces(faces)
    require(set(graph) == set(names), 'control vertex set changed')
    require(all(colors[a] != colors[b] for a in graph for b in graph[a]), 'improper control coloring')
    incidence = Counter(tuple(sorted(e)) for f in faces for e in combinations(f, 2))
    rim = {tuple(sorted((B14[i], B14[(i+1) % 14]))) for i in range(14)}
    require({e for e, count in incidence.items() if count == 1} == rim, 'wrong disk boundary')
    require(all(count in (1, 2) for count in incidence.values()), 'wrong edge incidence')
    require(len(graph) - len(incidence) + len(faces) == 1, 'disk Euler failure')
    for v in graph:
        link = graph_from_faces([])
        for f in faces:
            if v in f:
                a, b = [z for z in f if z != v]
                link.setdefault(a, set()).add(b)
                link.setdefault(b, set()).add(a)
        reached, todo = set(), [next(iter(link))]
        while todo:
            a = todo.pop()
            if a not in reached:
                reached.add(a)
                todo.extend(link[a] - reached)
        require(reached == set(link), 'disconnected vertex link')
        expected = [1, 1] + [2] * (len(link)-2) if v in B14 else [2] * len(link)
        require(sorted(map(len, link.values())) == sorted(expected), 'wrong disk vertex link')
    return graph


def small_search(colors, A, B):
    """All zero/one-interior completions, with exact no-unwanted-join edges.

    For the single new vertex each palette block is either an existing boundary
    block on the right side, or a fresh interior-only block on that side.
    No common-source inference is made from a failure of this bounded search.
    """
    asp = {a: colors[A.index(a)] in (0, 3) for a in sorted(set(A))}
    bsp = {b: colors[B.index(b)] in (0, 2) for b in sorted(set(B))}
    asp |= {'fresh03': True, 'fresh12': False}
    bsp |= {'fresh02': True, 'fresh13': False}
    vertices = list(product(asp, bsp))
    boundary = list(zip(A, B))

    def edge(v, w):
        return (v != w and (asp[v[0]] != asp[w[0]] or v[0] == w[0])
                and (bsp[v[1]] != bsp[w[1]] or v[1] == w[1])
                and (asp[v[0]], bsp[v[1]]) != (asp[w[0]], bsp[w[1]]))

    def be(i, j):
        return edge(boundary[i % 14], boundary[j % 14])

    @lru_cache(None)
    def polygon(i, j):
        if j-i == 1:
            return ()
        if not be(i, j):
            return None
        for k in range(i+1, j):
            if not (be(i,k) and be(k,j)):
                continue
            a, b = polygon(i,k), polygon(k,j)
            if a is not None and b is not None:
                return (*a, *b, (i % 14, k % 14, j % 14))
        return None

    zero = polygon(0,13)
    witnesses = []
    for center in vertices:
        witness = None
        for start in range(14):
            @lru_cache(None)
            def star(i,k):
                if i == start+14:
                    return () if k >= 3 else None
                if not edge(center, boundary[i % 14]):
                    return None
                for j in range(i+1, start+15):
                    if not edge(center, boundary[j % 14]):
                        continue
                    arc = polygon(i,j)
                    if arc is None:
                        continue
                    tail = star(j,k+1)
                    if tail is not None:
                        return (*arc, (i % 14, j % 14, 14), *tail)
                return None
            witness = star(start,0)
            if witness is not None:
                break
        if witness is not None:
            color = {(True,True):0, (False,False):1, (False,True):2, (True,False):3}[(asp[center[0]],bsp[center[1]])]
            witnesses.append({'center_03_block': center[0], 'center_02_block': center[1],
                              'center_color': color, 'faces_by_index': list(witness)})
    return {'zero_interior_completion_exists': zero is not None,
            'one_interior_center_types_tested': len(vertices),
            'one_interior_completion_exists': bool(witnesses),
            'first_one_interior_witness': witnesses[0] if witnesses else None}


def cap_fibres(rim):
    a,n,u4,u3,u2,u1,L,q,c,s,v,w,t = rim
    right = [(x,y,r) for x,y,r in product(range(4),repeat=3)
             if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t)]
    spokes = {n,u4,u3,u2,u1,L}
    left = {
        'G': [(b,p,h,R) for b,p,h,R in product(range(4),repeat=4)
              if R not in spokes and b not in (a,c,q,p) and p not in (a,q,n,h) and h not in (q,L,R,n)],
        'Q1': [(b,R) for b,R in product(range(4),repeat=2)
               if R not in spokes and b == n and R == q and b not in (a,c,q)],
        'J1': [(b,R) for b,R in product(range(4),repeat=2)
               if R not in spokes and b == L and a != R and b not in (a,c,q)]}
    result = {g:{row:[] for row in ROWS} for g in ZERO}
    for g in ZERO:
        for ls in left[g]:
            for rs in right:
                row = ''.join(map(str, canonical((rs[0],rs[1],a,ls[0],c))))
                result[g][row].append([*ls,*rs])
    for rows in result.values():
        for assignments in rows.values():
            assignments.sort()
    return result


def seven_point_fibres(fixed, faces):
    graph = graph_from_faces(faces)
    domains = [sorted(set(range(4)) - {fixed[w] for w in graph[v] if w in fixed}) for v in MUTABLE]
    result = []
    for row in product(*domains):
        colors = fixed | dict(zip(MUTABLE,row))
        if any(colors[v] == colors[w] for v in graph for w in graph[v]):
            continue
        rim = [colors[v] for v in RIM]
        caps = cap_fibres(rim)
        result.append({'mutable_colors':list(row), 'literal_D_rim':rim,
                       'all_literal_original_cap_fibres':caps,
                       'forbidden_cap_present':any(caps[g][r] for g in ZERO for r in ZERO[g])})
    result.sort(key=lambda row:row['mutable_colors'])
    return result


def build():
    parent = json.loads(gzip.decompress(PARENT.read_bytes()))
    parent_caps = {tuple(row['canonical_D_rim']): row for row in parent['complete_original_cap_kernel']}
    rows, positive = [], []
    for target in (44459,44466):
        cases = {r['split_containing_0'][1]:r for r in parent['ordinary_C14_cases'] if r['target'] == target}
        literal = cases[2]['literal_F_boundary_colors']
        for ai,A in enumerate(cases[3]['surviving_types_after_same_initial_E_gate']):
            for bi,B in enumerate(cases[2]['surviving_types_after_same_initial_E_gate']):
                search = small_search(literal,A,B)
                rows.append({'target':target,'03_index':ai,'02_index':bi,**search})
                if not search['one_interior_completion_exists']:
                    continue
                w = search['first_one_interior_witness']
                names = [*B14,'X']
                faces = [[names[i] for i in face] for face in w['faces_by_index']]
                colors = dict(zip(names,[*literal,w['center_color']]))
                graph = check_disk(faces,names,colors)
                partitions, full_blocks = {}, {}
                for mate in (1,2,3):
                    full_blocks[str(mate)], partitions[str(mate)] = components(graph,colors,mate)
                require(partitions['2'] == B and partitions['3'] == A,'claimed same-graph pair not realized')
                allowed01 = cases[1]['surviving_types_after_same_initial_E_gate']
                full_graph = graph_from_faces([*faces,*STRIP])
                lifts = seven_point_fibres(colors,[*faces,*STRIP])
                expected = cases[2]['complete_initial_seven_point_fibre']['complete_seven_point_fibre']
                require([r['mutable_colors'] for r in lifts] == [r['mutable_colors'] for r in expected], 'seven-point full fibre changed')
                require(not any(r['forbidden_cap_present'] for r in lifts), 'control has a forbidden initial full cap')
                for lift, old_lift in zip(lifts, expected):
                    normalized = canonical(lift['literal_D_rim'])
                    old_cap = parent_caps[tuple(normalized)]
                    require(old_cap['state'] == old_lift['canonical_D_cap_state'], 'original cap state custody changed')
                    require(cap_fibres(normalized) == old_cap['complete_original_cap_fibres'],
                            'full cap assignments differ from frozen original authority')
                    lift['canonical_original_cap_state'] = old_cap['state']
                sourceS = {'a','z1','z2','z3','z4',Y,'q'}
                Sorder = ['a','z1','z2','z3','z4','z5',Y,'q']
                allowedS = {frozenset((Sorder[i],Sorder[i+1])) for i in range(len(Sorder)-1)}
                extraS = sorted([sorted((v,w)) for v in graph for w in graph[v]
                                 if v < w and v in sourceS and w in sourceS and frozenset((v,w)) not in allowedS])
                positive.append({'target':target,'03_index':ai,'02_index':bi,'ordered_boundary':list(B14),
                                 'colors':colors,'triangular_faces':faces,'complete_F_components':full_blocks,
                                 'F_boundary_partitions':partitions,'passes_initial_01_gate':partitions['1'] in allowed01,
                                 'extra_original_S_chords':extraS,'joined_U_degree':len(full_graph['U']),
                                 'joined_V_degree':len(full_graph['V']),
                                 'U_z4_common_F_neighbors':sorted(graph['U'] & graph['z4']),
                                 'V_Y_common_F_neighbors':sorted(graph['V'] & graph[Y]),
                                 'complete_seven_point_fibre_and_caps':lifts,
                                 'actual_941_source_realized':False})
    require(len(positive) == 2,'bounded positive-control count changed')
    require(all(not p['passes_initial_01_gate'] and p['joined_U_degree'] == p['joined_V_degree'] == 4
                and not p['extra_original_S_chords'] for p in positive),'source-negative-control classification changed')
    return {'scope':'Only two fixed B14 literal inputs and zero/one-interior-vertex controls',
            'parent_sha256':sha256(PARENT.read_bytes()).hexdigest(),
            'boundary_only_or_one_interior_search':rows,'same_disk_positive_controls':positive,
            'source_exclusion_inferred_from_bounded_failure':False,'actual_941_source_realized':False,
            'ordinary_type_I_excluded':False}


def verify(candidate, expected):
    require(candidate == expected,'control certificate differs from complete replay')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build',action='store_true')
    args = ap.parse_args()
    expected = json.loads(packed(build()))
    dest = HERE / 'certificate-v2.json.gz'
    if args.build:
        require(not dest.exists(),'refuse to overwrite existing certificate')
        dest.write_bytes(gzip.compress(packed(expected),mtime=0))
    candidate = json.loads(gzip.decompress(dest.read_bytes()))
    verify(candidate,expected)
    controls = []
    def reject(name,mutate):
        corrupted = deepcopy(candidate)
        mutate(corrupted)
        try:
            verify(corrupted,expected)
        except ValueError:
            controls.append(name)
            return
        raise ValueError('negative control accepted: '+name)
    reject('claimed_source_realization',lambda c:c.update(actual_941_source_realized=True))
    reject('claimed_source_exclusion_from_bounded_search',lambda c:c.update(source_exclusion_inferred_from_bounded_failure=True))
    reject('claimed_01_gate',lambda c:c['same_disk_positive_controls'][0].update(passes_initial_01_gate=True))
    reject('missing_face',lambda c:c['same_disk_positive_controls'][0]['triangular_faces'].pop())
    reject('missing_complete_seven_point_lift',lambda c:c['same_disk_positive_controls'][0]['complete_seven_point_fibre_and_caps'].pop())
    result = {'status':'PASS','positive_same_disk_controls':len(candidate['same_disk_positive_controls']),
              'literal_pairs_tested':len(candidate['boundary_only_or_one_interior_search']),
              'negative_controls_rejected':controls,'certificate_sha256':sha256(dest.read_bytes()).hexdigest()}
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
