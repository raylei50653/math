#!/usr/bin/env python3
"""Periodic plane triangulations made by explicit gluing of RSST free completions.

uv run --with python-sat==1.9.dev17 python work/rsst-periodic-atlas/generate.py
Rational geometry checks concern selected constructions, not every RSST shape.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from four_color_kempe_free_contracts import parse_conf, structure, CONF_SHA256


def load_period_tools():
    spec = importlib.util.spec_from_file_location('period_tools', HERE.parent / 'periodic-triangle-atlas/equivariant_periods.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def boundary(c, kind, side_a=None):
    r = c['r']
    if kind == 'hexagon':
        assert r == 6
        return [(Q(x, 3), Q(y, 3)) for x, y in [(1,1),(-1,2),(-2,1),(-1,-1),(1,-2),(2,-1)]]
    a = side_a if side_a is not None else r // 4
    b = r // 2 - a
    assert a >= 1 and b >= 1 and r == 2*(a+b)
    return ([(Q(t,a), Q(0)) for t in range(a)]
            + [(Q(1), Q(t,b)) for t in range(b)]
            + [(1-Q(t,a), Q(1)) for t in range(a)]
            + [(Q(0), 1-Q(t,b)) for t in range(b)])


def orbit_key(u, v, dx, dy):
    return min((u,v,dx,dy),(v,u,-dx,-dy))


def skeleton(c, kind='square', side_a=None):
    ring = boundary(c, kind, side_a)
    representatives, mapping, keys = [], [], {}
    for x,y in ring:
        dx,dy = x//1,y//1
        key = (x-dx,y-dy)
        if key not in keys:
            keys[key] = len(representatives)
            representatives.append(key)
        mapping.append((keys[key],int(dx),int(dy)))
    for v in range(c['r'],c['n']):
        mapping.append((len(representatives),0,0))
        representatives.append(None)
    _,edges,_,_ = structure(c)
    orbits = set()
    for u,v in edges:
        i,x,y = mapping[u]
        j,s,t = mapping[v]
        orbits.add(orbit_key(i,j,s-x,t-y))
    faces = {}
    for v,neighbors in enumerate(c['adj']):
        for k in range(len(neighbors)-(v<c['r'])):
            face = (v,neighbors[k],neighbors[(k+1)%len(neighbors)])
            faces.setdefault(tuple(sorted(face)), face)
    assert len(faces) == 2*c['n']-2-c['r']
    face_orbits = [[mapping[v] for v in f] for f in faces.values()]
    n = len(representatives)
    degrees = [0]*n
    for u,v,_,_ in orbits:
        degrees[u] += 1
        degrees[v] += 1
    assert len(orbits)==3*n and len(face_orbits)==2*n
    assert all(degrees[mapping[v][0]]==len(c['adj'][v]) for v in range(c['r'],c['n']))
    return {'points':representatives,'edges':sorted(orbits),'faces':face_orbits,'degrees':degrees}, mapping, list(faces.values()), edges


def rational_tutte(c, ring):
    r,n = c['r'],c['n']
    m = n-r
    matrix = [[Q(0) for _ in range(m+2)] for _ in range(m)]
    for v in range(r,n):
        i = v-r
        matrix[i][i] = Q(len(c['adj'][v]))
        for w in c['adj'][v]:
            if w>=r:
                matrix[i][w-r] -= 1
            else:
                matrix[i][-2] += ring[w][0]
                matrix[i][-1] += ring[w][1]
    for col in range(m):
        pivot = next(i for i in range(col,m) if matrix[i][col])
        matrix[col],matrix[pivot] = matrix[pivot],matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x/scale for x in matrix[col]]
        for row in range(m):
            if row==col or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [x-scale*y for x,y in zip(matrix[row],matrix[col])]
    return ring + [(row[-2],row[-1]) for row in matrix]


def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def on_segment(p,a,b):
    return cross(a,b,p)==0 and all(min(x,y)<=z<=max(x,y) for x,y,z in zip(a,b,p))


def geometric_checks(points, edges, faces, example, mapping):
    assert len(set(points))==len(points)
    areas = [cross(*(points[v] for v in f)) for f in faces]
    assert min(areas)>0 and sum(areas)==2
    for i,(u,v) in enumerate(edges):
        for s,t in edges[i+1:]:
            common = {u,v}&{s,t}
            a,b,c,d = points[u],points[v],points[s],points[t]
            ca,cb,cc,cd = cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
            assert not (ca*cb<0 and cc*cd<0)
            for w,x,y in [(s,u,v),(t,u,v),(u,s,t),(v,s,t)]:
                assert w in common or not on_segment(points[w],points[x],points[y])
    # Every lifted edge occurs in two faces, with opposite directions.
    incidence = defaultdict(list)
    links = defaultdict(lambda:defaultdict(set))
    for face in example['faces']:
        for k,(v,x,y) in enumerate(face):
            w,s,t = face[(k+1)%3]
            key = orbit_key(v,w,s-x,t-y)
            incidence[key].append((v,w,s-x,t-y)==key)
            others = [(u,a-x,b-y) for u,a,b in [face[(k+1)%3],face[(k+2)%3]]]
            a,b = others
            links[v][a].add(b)
            links[v][b].add(a)
    assert set(incidence)==set(map(tuple,example['edges']))
    assert all(sorted(v)==[False,True] for v in incidence.values())
    for v,link in links.items():
        assert len(link)==example['degrees'][v] and all(len(a)==2 for a in link.values())
        seen, todo = set(), [next(iter(link))]
        while todo:
            a = todo.pop()
            if a not in seen:
                seen.add(a)
                todo.extend(link[a]-seen)
        assert len(seen)==len(link)
    assert sum(6-d for d in example['degrees'])==0
    assert len(example['points'])-len(example['edges'])+len(example['faces'])==0
    assert all(points[v]==(example['points'][u][0]+x,example['points'][u][1]+y) for v,(u,x,y) in enumerate(mapping))
    return {'rational_positive_faces':True,'rational_cell_area_one':True,
            'rational_no_edge_crossing_or_vertex_on_edge':True,'all_source_edges_retained':True,
            'two_opposite_faces_per_lifted_edge':True,'vertex_links_single_cycles':True,
            'torus_euler_zero':True,'degree_curvature_sum_zero':True,
            'source_interior_degrees_preserved':True,'minimum_double_face_area':str(min(areas))}


def exact_example(c, source_index, kind='square', side_a=None):
    example,mapping,faces,edges = skeleton(c,kind,side_a)
    ring = boundary(c,kind,side_a)
    points = rational_tutte(c,ring)
    for v in range(c['r'],c['n']):
        example['points'][mapping[v][0]] = points[v]
    checks = geometric_checks(points,edges,faces,example,mapping)
    rationals = lambda ps:[[str(x),str(y)] for x,y in ps]
    example['rational_points'] = rationals(example['points'])
    example['points'] = [[float(x),float(y)] for x,y in example['points']]
    a = side_a if side_a is not None else c['r']//4
    example.update(id=f'R{source_index:03d}-{kind}', name=('Birkhoff diamond · 六角接合' if kind=='hexagon' else c['name']+' · 四邊接合'),
                   source_index=source_index,source_name=c['name'],ring_size=c['r'],source_n=c['n'],
                   kind=kind,side_subdivisions=None if kind=='hexagon' else [a,c['r']//2-a,a,c['r']//2-a],
                   basis=[[1.,0.],[.5,3**.5/2]] if kind=='hexagon' else [[1.,0.],[0.,1.]],
                   checks=checks,
                   source_patch={'points':[[float(x),float(y)] for x,y in points],
                                 'rational_points':rationals(points),'edges':edges,'faces':faces,
                                 'ring_size':c['r'],'map':mapping})
    return example


def display_witness(ex, rec, tools):
    a,b,d = rec['a'],rec['b'],rec['d']
    n = len(ex['points'])
    flat = [c for row in rec['witness']['colors'] for cell in row for c in cell]
    def at(v,x,y):
        return flat[tools.quotient_index(v,x,y,n,a,b,d)]
    def shift(dx,dy):
        mapping = {}
        same,valid = True,True
        for y in range(d):
            for x in range(a):
                for v in range(n):
                    p,q = at(v,x,y),at(v,x+dx,y+dy)
                    same &= p==q
                    if p in mapping and mapping[p]!=q:
                        valid=False
                    mapping[p]=q
        if len(set(mapping.values()))!=len(mapping):
            valid=False
        unused = sorted(set(range(4))-set(mapping))
        targets = sorted(set(range(4))-set(mapping.values()))
        mapping.update(zip(unused,targets))
        return same,[mapping[c] for c in range(4)] if valid else None
    same,permuted = [],[]
    for y in range(d):
        for x in range(a):
            equal,permutation = shift(x,y)
            if equal:
                same.append([x,y])
            if permutation is not None:
                permuted.append({'shift':[x,y],'permutation':permutation})
    assert a*d%len(same)==0
    axis = [next(k for k in range(1,a*d+1) if shift(k,0)[0]),
            next(k for k in range(1,a*d+1) if shift(0,k)[0])]
    return {'colors':flat,'same_color_shifts':same,'permuted_shifts':permuted,
            'axis_period':axis,'translation_index':a*d//len(same),
            'checks':rec['witness']['checks']}


def main():
    source = HERE/'sources/unavoidable.conf'
    assert sha256(source.read_bytes()).hexdigest()==CONF_SHA256
    configs = parse_conf(source.read_text())
    assert len(configs)==633
    periods = load_period_tools()
    inventory = []
    print('Scanning balanced square seam constructions for all even rings',flush=True)
    for i,c in enumerate(configs,1):
        row = {'source_index':i,'name':c['name'],'n':c['n'],'r':c['r'],
               'interior_degree_counts':dict(sorted(Counter(map(len,c['adj'][c['r']:])).items()))}
        if c['r']%2:
            row['scope']='Not tested: this one-cell opposite-side seam scheme requires even boundary length.'
        else:
            ex,mapping,_,_ = skeleton(c)
            decisions = [periods.solve_sublattice(ex,a,b,d) for index in range(1,5) for a in range(1,index+1) if index%a==0 for d in [index//a] for b in range(a)]
            row.update(motif_n=len(ex['points']),degrees=ex['degrees'],
                       quotient_has_self_loop=any(u==v for u,v,_,_ in ex['edges']),
                       source_map=mapping,motif_edges=ex['edges'],motif_faces=ex['faces'],
                       side_subdivisions=[c['r']//4,c['r']//2-c['r']//4]*2,
                       hnf_decisions=decisions,
                       minimum_index=next((rec['index'] for rec in decisions if rec['status']=='SAT'),None))
        inventory.append(row)
    selected = [(1,'hexagon'),(3,'square'),(4,'square'),(24,'square'),(9,'square')]
    # One compact representative at each larger even boundary size; prefer
    # nontrivial minimum index, then smaller source size, then original order.
    for r in [12,14]:
        rows = [row for row in inventory if row['r']==r]
        rows.sort(key=lambda row:(-(row['minimum_index'] or 5),row['n'],row['source_index']))
        selected.append((rows[0]['source_index'],'square'))
    examples = []
    for i,kind in selected:
        ex = exact_example(configs[i-1],i,kind)
        result = periods.analyze_example(ex,max_index=4)
        ex['period_analysis'] = result
        ex['minimum_index'] = result['summary']['minimum_literal_index_relative_to_supplied_lattice']
        ex['periods'] = []
        for rec in result['sublattices']:
            entry = {k:v for k,v in rec.items() if k!='witness'}
            entry['witness'] = display_witness(ex,rec,periods) if rec['status']=='SAT' else None
            ex['periods'].append(entry)
        ex['preferred_period'] = next([rec['a'],rec['b'],rec['d']] for rec in ex['periods'] if rec['status']=='SAT')
        quotient_edges = {tuple(sorted((u,v))) for u,v,_,_ in ex['edges']}
        ex['one_cell_k5'] = next((list(vs) for vs in combinations(range(len(ex['points'])),5)
                                 if all(tuple(sorted(edge)) in quotient_edges for edge in combinations(vs,2))),None)
        if ex['one_cell_k5']:
            ex['one_cell_k5_source_edges'] = [
                next([u+1,v+1] for u,v in ex['source_patch']['edges']
                     if sorted((ex['source_patch']['map'][u][0],ex['source_patch']['map'][v][0]))==list(pair))
                for pair in combinations(ex['one_cell_k5'],2)]
        ex['odd_degree_vertex'] = next((v for v,d in enumerate(ex['degrees']) if d%2),None)
        examples.append(ex)
        print(ex['id'],'checked rational geometry and period analysis',flush=True)
    payload = {'schema':'rsst-periodic-atlas/1','source':{'url':'https://arxiv.org/src/1401.6481v1/anc/unavoidable.conf',
                 'sha256':CONF_SHA256,'configuration_count':633},
               'producer_sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in
                                  [Path(__file__),ROOT/'scripts/four_color_kempe_free_contracts.py',
                                   HERE.parent/'periodic-triangle-atlas/equivariant_periods.py']},
               'method':{'scope':'New infinite triangulations glued from RSST free completions. They are not intrinsic periods of finite RSST configurations or a reducibility proof.',
                         'seams':'Each original boundary vertex retains motif ID and integer lattice offset; all original edges retained.',
                         'geometry':'Selected cells: exact rational harmonic embedding, every positive face and every segment pair checked, full periodic edge incidences and links checked.',
                         'scan_scope':'All 349 even-ring free completions: one balanced square boundary split, fixed original start. Combinatorial quotients only for the unselected cases.',
                         'period_scope':'All 15 sublattices of indices 1 through 4 relative to the chosen geometric lattice; solver UNSAT has no archived formal certificate.'},
               'scan_summary':{'ring_counts':dict(sorted(Counter(c['r'] for c in configs).items())),
                               'even_ring_count':sum(c['r']%2==0 for c in configs),
                               'square_minimum_index_counts':dict(Counter(row['minimum_index'] for row in inventory if row['r']%2==0))},
               'inventory':inventory,'examples':examples}
    (HERE/'atlas.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(payload['scan_summary'],ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
