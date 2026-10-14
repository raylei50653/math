#!/usr/bin/env python3
"""Deterministic local source-geometry calibration, with no colour hypothesis.

Reads only the four explicit sphere samples in geometry-inputs.json. Saved
sample provenance identifies the larger original certificate without requiring
that file for replay. These samples are not minimal noncatalogue sources.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(edges):
    out = defaultdict(set)
    for v, w in edges:
        need(v != w, 'loop')
        out[v].add(w)
        out[w].add(v)
    return dict(out)


def edge(v, w):
    return tuple(sorted((v, w)))


def edge_set(adj):
    return {edge(v, w) for v in adj for w in adj[v]}


def induced(adj, vertices):
    return {v: adj[v] & vertices for v in sorted(vertices)}


def rotations(adj, faces):
    darts = Counter((f[i], f[(i + 1) % len(f)])
                    for f in faces for i in range(len(f)))
    need(all(len(f) >= 3 and len(set(f)) == len(f) for f in faces), 'simple faces')
    need(darts == Counter({(v, w): 1 for v in adj for w in adj[v]}), 'face darts')
    need(len(adj) - len(edge_set(adj)) + len(faces) == 2, 'sphere Euler')
    reached, todo = set(), [min(adj)]
    while todo:
        v = todo.pop()
        if v not in reached:
            reached.add(v)
            todo.extend(adj[v] - reached)
    need(reached == set(adj), 'connected surface')
    result = {}
    for v, ns in sorted(adj.items()):
        link = {}
        for f in faces:
            if v in f:
                i = f.index(v)
                a, b = f[(i - 1) % len(f)], f[(i + 1) % len(f)]
                need(a not in link, 'repeated link dart')
                link[a] = b
        need(set(link) == ns and set(link.values()) == ns, 'complete link')
        seq = [min(ns)]
        while link[seq[-1]] not in seq:
            seq.append(link[seq[-1]])
        need(link[seq[-1]] == seq[0] and set(seq) == ns, 'one link cycle')
        result[str(v)] = seq
    return result


def orient(adj, faces):
    """Orient a closed face complex, rejecting inconsistent edge gluings."""
    incident = defaultdict(list)
    for i, f in enumerate(faces):
        for j, v in enumerate(f):
            incident[edge(v, f[(j + 1) % len(f)])].append(i)
    need(set(incident) == edge_set(adj), 'face edge coverage')
    need(all(len(xs) == 2 for xs in incident.values()), 'two faces per edge')
    chosen, todo = {0: list(faces[0])}, [0]
    while todo:
        i = todo.pop()
        f = chosen[i]
        for j, v in enumerate(f):
            w = f[(j + 1) % len(f)]
            other = next(k for k in incident[edge(v, w)] if k != i)
            g = list(faces[other])
            if g[(g.index(v) + 1) % len(g)] == w:
                g.reverse()
            if other in chosen:
                h = chosen[other]
                need(h[(h.index(w) + 1) % len(h)] == v, 'orientability')
            else:
                chosen[other] = g
                todo.append(other)
    need(len(chosen) == len(faces), 'connected face complex')
    out = [chosen[i] for i in range(len(faces))]
    rotations(adj, out)
    return out


def cycles(adj, length):
    found = []
    for start in sorted(adj):
        def visit(path):
            if len(path) == length:
                if start in adj[path[-1]] and path[1] < path[-1]:
                    found.append(tuple(path))
                return
            for v in sorted(adj[path[-1]]):
                if v > start and v not in path:
                    visit(path + [v])
        visit([start])
    return found


def check_s6(adj, faces):
    incident = defaultdict(list)
    for i, f in enumerate(faces):
        for j, v in enumerate(f):
            incident[edge(v, f[(j + 1) % len(f)])].append(i)
    stats = {}
    for length in (3, 4, 5):
        cs = cycles(adj, length)
        separating = 0
        for c in cs:
            cut = {edge(c[i], c[(i + 1) % length]) for i in range(length)}
            dual = {i: set() for i in range(len(faces))}
            for e, (i, j) in incident.items():
                if e not in cut:
                    dual[i].add(j)
                    dual[j].add(i)
            unseen, sides = set(dual), []
            while unseen:
                todo, verts = [min(unseen)], set()
                while todo:
                    i = todo.pop()
                    if i not in unseen:
                        continue
                    unseen.remove(i)
                    verts.update(faces[i])
                    todo.extend(dual[i] & unseen)
                sides.append(verts - set(c))
            need(len(sides) == 2 and not sides[0] & sides[1], 'Jordan sides')
            counts = sorted(map(len, sides))
            need(counts[0] <= (1 if length == 5 else 0), 'S6 cycle contract')
            separating += int(counts[0] > 0)
        stats[str(length)] = {'cycles': len(cs), 'separating': separating}
    return stats


def opening(sphere, u, B, shift):
    x, y, a, b, c = [B[(i + shift) % 5] for i in range(5)]
    g = induced(sphere, set(sphere) - {u})
    if any(len(g[v]) != 4 for v in (x, y, b)):
        return None
    def apex(v, w):
        common = (g[v] & g[w]) - set(B)
        need(len(common) == 1, 'unique boundary apex')
        return next(iter(common))
    r, t, p, q, s = [apex(B[(i + shift) % 5], B[(i + shift + 1) % 5])
                     for i in range(5)]
    A = {r, t, p, q, s}
    need(len(A) == 5, 'five distinct apexes')
    for v, contacts in zip((r, t, p, q, s), ({x,y}, {y,a}, {a,b}, {b,c}, {c,x})):
        need(g[v] & set(B) == contacts, 'literal B attachments')
    expected = {edge(r,s), edge(r,t), edge(p,q)}
    if len(g[a]) == 4:
        expected.add(edge(t,p))
    if len(g[c]) == 4:
        expected.add(edge(q,s))
    need(edge_set(induced(g, A)) == expected, 'exact apex induced graph')
    project = lambda v: a if v == c else v
    R = adjacency({edge(project(v), project(w)) for v,w in edge_set(g)
                   if v not in {x,y,b} and w not in {x,y,b}})
    z, Q, k = a, [a,s,r,t], len(g)-5
    need(len(R) == k+1 and set(R) == set(g)-{x,y,b,c}, 'R vertex count')
    need(edge_set(induced(R, set(Q))) == {edge(Q[i],Q[(i+1)%4]) for i in range(4)},
         'induced Q')
    triangles = [list(vs) for vs in combinations(sorted(R),3)
                 if all(w in R[v] for v,w in combinations(vs,2))]
    faces = orient(R, triangles + [Q])
    need(R[z] & R[r] == {s,t}, 'full common-neighbour equality')
    h = sum(len(g[v])-4 for v in B)
    degree_expected = {z:h+4, r:len(g[r])-2,
                       **{v:len(g[v])-1 for v in (s,t,p,q)}}
    for v in R:
        need(len(R[v]) == degree_expected.get(v,len(g[v])), 'exact R degree')
    need(all(len(R[v]) >= 5 for v in set(R)-set(Q)-{p,q}), 'other internal degrees')
    if h >= 3:
        need(len(R[z]) >= 7 and not (edge(t,p) in expected and edge(q,s) in expected),
             'h>=3 source consequences')
    merge = lambda v: z if v == r else v
    J = adjacency({edge(merge(v),merge(w)) for v,w in edge_set(R)})
    need(len(edge_set(R))-len(edge_set(J)) == 2, 'only two parallel pairs')
    orient(J, [[merge(v) for v in f] for f in triangles])
    need(len(J) == k, 'J vertex count')
    low_r = None
    if len(g[r]) == 5:
        inner = R[r]-{s,t}
        need(len(inner)==1, 'unique r interior neighbour')
        v = next(iter(inner))
        need(not g[v]&set(B) and z not in R[v], 'v has no B contact')
        R2 = induced(R,set(R)-{r})
        Q2 = [z,s,v,t]
        need(edge_set(induced(R2,set(Q2))) == {edge(Q2[i],Q2[(i+1)%4]) for i in range(4)},
             'induced Q prime')
        orient(R2,[f for f in triangles if r not in f]+[Q2])
        need(len(R2)==k, 'R prime vertex count')
        need(all(len(R2[w])==len(R[w]) for w in set(R2)-set(Q2)), 'R prime inner degrees')
        low_r = {'v':v,'Q_prime':Q2,'vertices':len(R2)}
    return {'shift':shift,'pins':dict(zip(('x','y','a','b','c','z','s','r','t','p','q'),
                                      (x,y,a,b,c,z,s,r,t,p,q))),
            'k':k,'h':h,'apex_edges':sorted(expected),'R_degree':degree_expected,
            'R_vertices':len(R),'J_vertices':len(J),'r_five_deletion':low_r,
            'p_q_high_degree':min(len(g[p]),len(g[q]))>=6}


def calculate():
    raw = (HERE/'geometry-inputs.json').read_bytes()
    data = json.loads(raw)
    need(len(data['samples']) == 4, 'four explicit controls')
    results, count, low = [], 0, 0
    for sample in data['samples']:
        E = [tuple(e) for e in sample['edges']]
        need(len(set(E)) == len(E) and all(v<w for v,w in E), 'simple canonical edges')
        adj = adjacency(E)
        faces = sample['faces']
        need(all(len(f)==3 for f in faces), 'sphere triangulation')
        need(rotations(adj,faces)==sample['rotation'], 'frozen plane rotation')
        need(min(map(len,adj.values()))>=5, 'sphere minimum degree five')
        u, B = sample['u'], sample['B']
        need(len(B)==len(set(B))==5 and adj[u]==set(B), 'root and B')
        need({edge(B[i],B[(i+1)%5]) for i in range(5)}==edge_set(induced(adj,set(B))),
             'induced root link')
        stats = check_s6(adj,faces)
        rows = [r for shift in range(5) if (r:=opening(adj,u,B,shift)) is not None]
        need(rows, 'selected opening triggers')
        count += len(rows)
        low += sum(r['r_five_deletion'] is not None for r in rows)
        results.append({'id':sample['id'],'sphere_vertices':len(adj),'S6':stats,'openings':rows})
    need(low>0, 'r degree-five deletion must trigger')
    # Actual malformed-face and rotation mutations must be rejected.
    rejected = 0
    for corrupt in (faces[:-1],faces+faces[:1]):
        try:
            rotations(adj,corrupt)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('accepted face corruption')
    return {'schema':'c4-mask13-geometry-v1','input_sha256':sha256(raw).hexdigest(),
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'summary':{'sphere_controls':4,'openings':count,'r_five_deletions':low,
                       'rejected_face_corruptions':rejected,'target_source_actual':0},
            'mask_hypotheses_tested':False,'external_enumeration_replayed':False,
            'scope':'S6 and local degrees only; controls are not minimal noncatalogue sources',
            'samples':results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result,indent=2,sort_keys=True)+'\n'
    path = HERE/'geometry.json'
    if args.check:
        need(path.read_text()==payload,'geometry certificate drift')
    else:
        with path.open('x') as f:
            f.write(payload)
    print(json.dumps(result['summary'],sort_keys=True))


if __name__ == '__main__':
    main()
