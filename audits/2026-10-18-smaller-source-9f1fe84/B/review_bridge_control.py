#!/usr/bin/env python3
"""Independent flat-product and sphere-rotation review of C's full disks."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--write', action='store_true')
parser.add_argument('--write-full', action='store_true')
args = parser.parse_args()
certificate = json.loads((ROOT / 'C/certificate.json').read_text())
outer = tuple('xyabc')
rows = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
original_faces = certificate['whole_graph_oriented_faces']
report = {}
all_fibres = {}
for name, graph in certificate['whole_graph_control'].items():
    vertices = graph['vertices']
    assert vertices[:5] == list(outer)
    indexed_edges = [(vertices.index(a), vertices.index(b)) for a,b in graph['edges']]
    fibres = []
    for word in rows:
        beta = tuple(map(int, word))
        ff = [beta + private for private in itertools.product(range(4), repeat=len(vertices)-5)
              if all((beta + private)[a] != (beta + private)[b] for a,b in indexed_edges)]
        assert hashlib.sha256(json.dumps(ff).encode()).hexdigest() == graph['fibres_sha256'][len(fibres)]
        fibres.append(ff)
    assert list(map(len, fibres)) == graph['counts']
    all_fibres[name] = fibres
    if name == 'G':
        inner_faces = original_faces
    else:
        inner_faces = [f for f in original_faces if not set(f) & {'p','h'}]
        boundary = ('a','b','q','L','R','n') if name == 'G_a' else ('b','q','L','R','n','a')
        inner_faces += [(boundary[0], boundary[i], boundary[i+1]) for i in range(1,5)]
    full_faces = list(inner_faces) + [tuple(reversed(outer))]
    successor = {v:{} for v in vertices}
    directed = set()
    for f in full_faces:
        for i,v in enumerate(f):
            pred,nxt = f[i-1], f[(i+1)%len(f)]
            assert pred not in successor[v]
            successor[v][pred] = nxt
            assert (v,nxt) not in directed
            directed.add((v,nxt))
    assert directed == {(a,b) for e in graph['edges'] for a,b in (e, e[::-1])}
    rotations = {}
    for v, succ in successor.items():
        first = min(succ)
        order, t = [], first
        while not order or t != first:
            assert t not in order
            order.append(t)
            t = succ[t]
        assert set(order) == set(succ)
        rotations[v] = order
    assert len(vertices)-len(graph['edges'])+len(full_faces) == 2
    assert len(vertices)-5 == (7 if name == 'G' else 5)
    report[name] = {'full_counts':graph['counts'],'mask':graph['mask'],
                    'inner_vertices':len(vertices)-5,'oriented_faces':inner_faces,
                    'rotations':rotations}

# Direct restriction and inverse-fibre comparison use complete graph assignments.
original_vertices = certificate['whole_graph_control']['G']['vertices']
for row_index, old in enumerate(all_fibres['G']):
    for colouring in old:
        assignment = dict(zip(original_vertices, colouring))
        if row_index == 9:
            chosen = 'G_a' if assignment['h'] == assignment['a'] else 'G_b'
            target_vertices = certificate['whole_graph_control'][chosen]['vertices']
            assert tuple(assignment[v] for v in target_vertices) in all_fibres[chosen][row_index]
    for name in ('G_a','G_b'):
        target_vertices = certificate['whole_graph_control'][name]['vertices']
        for colouring in all_fibres[name][row_index]:
            assignment = dict(zip(target_vertices,colouring))
            exact = [g for g in old if all(g[original_vertices.index(v)]==assignment[v] for v in target_vertices)]
            rainbow = len({assignment[v] for v in ('a','b','q','n')}) == 4
            assert bool(exact) == (not rainbow)
report['status'] = 'PASS'
report['reviewed_certificate_sha256'] = hashlib.sha256((ROOT/'C/certificate.json').read_bytes()).hexdigest()
report['method'] = 'flat Cartesian colour products, independent complete-disk rotations and direct whole-fibre restrictions'
output = ROOT/'B/REVIEW-C-CONTROL.json'
if args.write:
    with output.open('x') as stream:
        json.dump(report,stream,indent=2)
        stream.write('\n')
else:
    assert json.loads(output.read_text()) == json.loads(json.dumps(report))
complete = {'rows': rows, 'outer': outer,
            'vertices': {name: d['vertices'] for name,d in certificate['whole_graph_control'].items()},
            'full_fibres': all_fibres,
            'source_certificate_sha256': report['reviewed_certificate_sha256'],
            'encoding': 'Same literal outer frame for every full assignment. Common S4 expansion of entire full assignments supplies all other proper outer rows; improper outer tuples are empty.'}
full_output = ROOT/'B/REVIEW-C-FULL-FIBRES.json'
if args.write or args.write_full:
    with full_output.open('x') as stream:
        json.dump(complete,stream,indent=2)
        stream.write('\n')
else:
    assert json.loads(full_output.read_text()) == json.loads(json.dumps(complete))
print(json.dumps({name: {'counts': data['full_counts'], 'inner_vertices': data['inner_vertices']}
                  for name,data in report.items() if name in ('G','G_a','G_b')}, sort_keys=True))
