#!/usr/bin/env python3
"""Geometric calibration only; original minimum-source trigger is absent."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def edge(u, v):
    return tuple(sorted((u, v)))


def components(vertices, edges):
    adj = {u: set() for u in vertices}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    unseen, out = set(vertices), []
    while unseen:
        todo, found = [min(unseen)], set()
        while todo:
            u = todo.pop()
            if u in found:
                continue
            found.add(u); unseen.discard(u)
            todo.extend(adj[u] - found)
        out.append(sorted(found))
    return sorted(out)


def canonical_cycle(c):
    c = tuple(c)
    choices = []
    for d in (c, c[::-1]):
        choices.extend(d[i:] + d[:i] for i in range(len(d)))
    return min(choices)


def cycles(adj, length):
    found = set()
    def visit(path):
        if len(path) == length:
            if path[0] in adj[path[-1]]:
                found.add(canonical_cycle(path))
            return
        for v in sorted(adj[path[-1]]):
            if v > path[0] and v not in path:
                visit(path + [v])
    for u in sorted(adj):
        visit([u])
    return sorted(found)


def from_faces(n, faces):
    succ = {u: {} for u in range(n)}
    for face in faces:
        for a, b, c in (face, face[1:] + face[:1], face[2:] + face[:2]):
            assert b not in succ[a]
            succ[a][b] = c
    rotation = []
    for u in range(n):
        a = min(succ[u]); path = [a]
        while succ[u][path[-1]] != a:
            path.append(succ[u][path[-1]])
        assert len(path) == len(succ[u])
        rotation.append(path)
    return rotation


def reconstruct(rotation):
    adj = {u: set(nbrs) for u, nbrs in enumerate(rotation)}
    edges = sorted({edge(u, v) for u in adj for v in adj[u]})
    assert all(u in adj[v] for u in adj for v in adj[u])
    unseen = {(u, v) for u in adj for v in adj[u]}
    faces = []
    while unseen:
        start = min(unseen); dart = start; face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart; face.append(u)
            nbrs = rotation[v]
            dart = (v, nbrs[(nbrs.index(u) - 1) % len(nbrs)])
            if dart == start:
                break
        assert len(face) == 3
        faces.append(tuple(sorted(face)))
    faces.sort()
    assert len(rotation) - len(edges) + len(faces) == 2
    assert len(components(adj, edges)) == 1
    triangles = sorted(c for c in combinations(adj, 3)
                       if all(edge(u, v) in edges for u, v in combinations(c, 2)))
    assert triangles == faces
    dual_edges = []
    for u, v in edges:
        fs = [i for i, f in enumerate(faces) if u in f and v in f]
        assert len(fs) == 2
        dual_edges.append(tuple(fs))
    return adj, edges, faces, dual_edges


def controls():
    ico = [[1,5,11,7,8], [0,8,2,6,5], [1,8,9,3,6], [2,9,10,4,6],
           [3,10,11,5,6], [4,11,0,1,6], [5,1,2,3,4], [11,10,9,8,0],
           [7,9,2,1,0], [8,7,10,3,2], [9,7,11,4,3], [5,4,10,7,0]]
    yield ('icosahedron', ico, dict(m=0,z=1,v=7,w=11,p=6,q=2),
           dict(s=[7,8],t=[5,11],a=[5,6],c=[2,8]))
    pm, pz = [2,4,5,6,7,3], [2,8,9,10,3]
    boundary = pm + pz[-2:0:-1]
    fs = [(0, pm[i], pm[i+1]) for i in range(len(pm)-1)]
    fs += [(1, pz[i+1], pz[i]) for i in range(len(pz)-1)]
    fs += [(0,1,2), (1,0,3)]
    fs += [(11, boundary[(i+1)%len(boundary)], boundary[i])
           for i in range(len(boundary))]
    cone = from_faces(12, fs)
    for name, p, q, la, lc in [
            ('cone-generic',8,9,[2,8],[9,10,3]),
            ('cone-alpha-p',2,8,[2],[8,9,10,3]),
            ('cone-beta-q',10,3,[2,8,9,10],[3])]:
        yield (name, cone, dict(m=0,z=1,v=6,w=5,p=p,q=q),
               dict(s=[6,7,3],t=[2,4,5],a=la,c=lc))


def audit(name, rotation, pins, sectors):
    adj, edges, faces, dual_edges = reconstruct(rotation)
    m,z,v,w,p,q = (pins[k] for k in ('m','z','v','w','p','q'))
    ls,lt,la,lc = (set(sectors[k]) for k in ('s','t','a','c'))
    assert len({m,z,v,w,p,q}) == 6
    assert not ls & lt and ls | lt == adj[m] - {z}
    assert not la & lc and la | lc == adj[z] - {m}
    assert not ls & la and not lt & lc
    assert len(lt & la) == len(ls & lc) == 1
    alpha, beta = next(iter(lt & la)), next(iter(ls & lc))
    assert {edge(a,b) for a in ls for b in lt if b in adj[a]} == {edge(v,w)}
    assert {edge(a,b) for a in la for b in lc if b in adj[a]} == {edge(p,q)}
    assert not any(j in adj[i] for i in (v,w) for j in (p,q))
    assert v not in adj[z] and w not in adj[z]
    assert tuple(sorted((m,v,w))) in faces and tuple(sorted((z,p,q))) in faces
    marked = {edge(v,w):'e', edge(p,q):'f', edge(m,z):'g'}
    records = []
    for length in (4,5):
        for cyc in cycles(adj, length):
            ce = {edge(cyc[i],cyc[(i+1)%length]) for i in range(length)}
            chords = sorted(edge(a,b) for a,b in combinations(cyc,2)
                            if b in adj[a] and edge(a,b) not in ce)
            cut_ids = [edges.index(e) for e in sorted(ce)]
            remaining = [e for i,e in enumerate(dual_edges) if i not in cut_ids]
            sides = components(range(len(faces)), remaining)
            assert len(sides) == 2
            cyclic = all(sum(a in side and b in side for a,b in remaining) >= len(side)
                         for side in sides)
            centres = sorted(h for h in adj if h not in cyc and set(cyc) == adj[h])
            types, sector = '', None
            hubset = set(cyc) & {m,z}
            if hubset == set():
                types = 'no-hub'
            elif hubset == {m}:
                i=cyc.index(m); a,b=cyc[(i-1)%length],cyc[(i+1)%length]
                sector = 's' if {a,b} <= ls else 't' if {a,b} <= lt else None
                types = 'm-same' if sector else 'm-cross'
            elif hubset == {z}:
                i=cyc.index(z); a,b=cyc[(i-1)%length],cyc[(i+1)%length]
                sector = 'a' if {a,b} <= la else 'c' if {a,b} <= lc else None
                types = 'z-same' if sector else 'z-cross'
            else:
                if not chords:
                    i=cyc.index(m); d=list(cyc[i:]+cyc[:i])
                    if d[1] != z:
                        d=[d[0]]+d[:0:-1]
                    assert d[1] == z
                    a,c=d[2],d[-1]
                    sector=('a' if a in la else 'c')+('s' if c in ls else 't')
                types='both-'+str(sector)
            marks=sorted(marked[e] for e in ce if e in marked)
            assert not {'e','f'} <= set(marks)
            if not chords and length >= 4:
                assert not ({m,v,w} <= set(cyc))
                assert not ({z,p,q} <= set(cyc))
                assert len(marks) <= 1
            rec=dict(cycle=cyc,chords=chords,dual_sides=sides,cyclic_cut=cyclic,
                     star_centres=centres,source_sector_type=types,marked_edges=marks)
            if length == 5 and not chords:
                if types in ('both-at','both-cs'):
                    expected = alpha if types == 'both-at' else beta
                    assert all(h == expected for h in centres)
                    if centres:
                        assert expected != (p if types=='both-at' else q)
                elif types == 'both-ct':
                    assert all(h == alpha == p for h in centres)
                elif types == 'both-as':
                    assert all(h == beta == q for h in centres)
                rec['original_cap_needed'] = (types in ('no-hub','m-same','z-same',
                                                        'both-at','both-cs'))
                rec['control_lacks_forced_cap'] = rec['original_cap_needed'] and not centres
            if length == 5 and chords and cyclic:
                ears=[]
                for chord in chords:
                    u,t=chord
                    for a in adj[u] & adj[t] & set(cyc):
                        ear=tuple(sorted((u,t,a)))
                        if ear not in faces or edge(u,a) not in ce or edge(t,a) not in ce:
                            continue
                        core=tuple(x for x in cyc if x != a)
                        core_edges={edge(core[i],core[(i+1)%4]) for i in range(4)}
                        assert not any(edge(b,c) in edges and edge(b,c) not in core_edges
                                       for b,c in combinations(core,2))
                        core_ids={edges.index(e) for e in core_edges}
                        core_remaining=[e for i,e in enumerate(dual_edges) if i not in core_ids]
                        core_sides=components(range(len(faces)),core_remaining)
                        assert len(core_sides)==2
                        assert all(sum(b in side and c in side for b,c in core_remaining)>=len(side)
                                   for side in core_sides)
                        fi=faces.index(ear)
                        assert any(set(s)^set(t)=={fi} for s in sides for t in core_sides)
                        ears.append(dict(face=ear,face_dual_vertex=fi,core=core,
                                         core_sides=core_sides))
                assert ears
                rec['ear_cores']=ears
                if {'e','g'} <= set(marks):
                    assert any(set(r['face'])=={m,v,w} and {m,z} <= set(r['core']) for r in ears)
                if {'f','g'} <= set(marks):
                    assert any(set(r['face'])=={z,p,q} and {m,z} <= set(r['core']) for r in ears)
            records.append(rec)
    summary = Counter()
    for r in records:
        l=len(r['cycle'])
        summary[f'cycles_{l}']+=1
        if not r['chords']:
            summary[f'induced_{l}']+=1
        if r['cyclic_cut']:
            summary[f'cyclic_cuts_{l}']+=1
        if r.get('ear_cores'):
            summary['chorded_cyclic_five_cuts']+=1
        if r.get('control_lacks_forced_cap'):
            summary['noncrossed_controls_lacking_original_cap']+=1
        if l==5 and not r['chords'] and r['star_centres']:
            summary['star_'+r['source_sector_type']]+=1
    if name == 'icosahedron':
        assert not summary['noncrossed_controls_lacking_original_cap']
        assert summary['star_both-at'] == summary['star_both-cs'] == 1
    else:
        assert summary['noncrossed_controls_lacking_original_cap'] > 0
    if name=='cone-alpha-p':
        assert summary['star_both-ct'] == 1
    if name=='cone-beta-q':
        assert summary['star_both-as'] == 1
    return dict(name=name,rotation=rotation,pins=pins,sectors=sectors,
                alpha=alpha,beta=beta,faces=faces,edges=edges,dual_edges=dual_edges,
                summary=dict(sorted(summary.items())),records=records,
                original_minimum_source='not triggered',full_colouring_relation_claimed=False)


def calculate():
    authority=['BASE.json', 'frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md',
               'frozen/audits/2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md',
               'frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md']
    hashes={p:sha256((BASE/p).read_bytes()).hexdigest() for p in authority}
    frozen=json.loads((BASE/'BASE.json').read_text())
    assert frozen['base']=='f1faf743833c51ddc5efbe9e0f390b87b9f2311d'
    for record in frozen['authority_inputs']:
        assert sha256((BASE/'frozen'/record['path']).read_bytes()).hexdigest()==record['sha256']
    return dict(base=frozen['base'],authority_sha256=hashes,
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                proof_sha256=sha256((HERE/'PROOF.md').read_bytes()).hexdigest(),
                source_trigger='not triggered',controls=[audit(*c) for c in controls()])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate-v2.json')
    args=parser.parse_args()
    actual=calculate()
    actual=json.loads(json.dumps(actual))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(actual,f,indent=2,sort_keys=True); f.write('\n')
    else:
        expected=json.loads(args.certificate.read_text())
        assert actual==expected,'independent reconstruction differs from certificate'
    print(json.dumps({c['name']:c['summary'] for c in actual['controls']},sort_keys=True))
    print('source: not triggered; geometric calibration PASS')


if __name__=='__main__':
    main()
