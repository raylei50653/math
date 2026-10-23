#!/usr/bin/env python3
"""Independent finite calibrations; arbitrary-source theorems are in PROOF.md."""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def frozen():
    m = json.loads((HERE / 'INPUTS.json').read_text())
    require(m['base'] == BASE, 'BASE drift')
    for r in m['inputs']:
        b = (HERE / r['snapshot']).read_bytes()
        require((len(b), sha256(b).hexdigest()) == (r['bytes'], r['sha256']), 'snapshot drift')
        require(b == (ROOT / r['path']).read_bytes(), 'live mathematical authority drift: ' + r['path'])
    for r in m['routing_entry']:
        b = (HERE / r['snapshot']).read_bytes()
        require((len(b), sha256(b).hexdigest()) == (r['bytes'], r['sha256']), 'routing snapshot drift')
    return len(m['inputs'])


def graph(row):
    names = set(row['colors'])
    edges = {frozenset(e) for e in row['edges']}
    require(len(edges) == len(row['edges']) and all(len(e) == 2 and e <= names for e in edges), 'malformed graph')
    require(all(row['colors'][a] != row['colors'][b] for a, b in row['edges']), 'literal coloring changed')
    adj = {v: set() for v in names}
    for a, b in row['edges']:
        adj[a].add(b); adj[b].add(a)
    return adj, edges


def paths(adj, start, end, seed):
    result = []
    rng = random.Random(seed)
    def go(v, word):
        if v == end:
            result.append(word); return
        nxts = sorted(adj[v]); rng.shuffle(nxts)
        for nxt in nxts:
            if nxt not in word:
                go(nxt, word + [nxt])
    go(start, [start])
    return result


def reachable(adj, start, end, deleted_vertex=None, deleted_edge=None):
    seen, todo = {start}, [start]
    while todo:
        a = todo.pop()
        for b in adj[a]:
            if b == deleted_vertex or frozenset((a, b)) == deleted_edge or b in seen:
                continue
            seen.add(b); todo.append(b)
    return end in seen


def separators(rows, seed):
    summary = []
    for row in rows:
        adj, edges = graph(row)
        endpoint = row['endpoint_b']
        require(reachable(adj, 'Y', endpoint), 'complete B control disconnected')
        require(set(row['colors'].values()) <= {1, 3}, 'B13 palette changed')
        require(row['colors']['Y'] == row['colors'][endpoint] == 1 and row['colors']['q'] == 3, 'ordered literal endpoints changed')
        require(frozenset(('Y', 'q')) in edges and frozenset(('q', 'c')) in edges, 'boundary Y-q-c lost')
        pp = paths(adj, 'Y', endpoint, seed)
        unavoidable = sorted(set.intersection(*(set(p) for p in pp)) - {'Y', endpoint})
        by_delete = sorted(v for v in adj if v not in ('Y', endpoint) and not reachable(adj, 'Y', endpoint, deleted_vertex=v))
        require(unavoidable == by_delete == row['unavoidable_Y_b_vertices'], 'all-path / complete deletion mismatch')
        if row['b_is_c']:
            require(endpoint == 'c', 'b=c literal endpoint mismatch')
            require(row['color3_unavoidable_vertices'] == ['q'], 'boundary endpoint conclusion changed')
        else:
            got = sorted(v for v in unavoidable if row['colors'][v] == 3)
            require(got == row['color3_unavoidable_vertices'], 'color3 cutpoint changed')
        summary.append(dict(name=row['name'], simple_paths=len(pp), unavoidable_vertices=unavoidable))
    return summary


def c_bridges(rows, seed):
    summary = []
    for row in rows:
        adj, _ = graph(row)
        require(set(row['colors'].values()) <= {1, 2}, 'C12 palette changed')
        pp = paths(adj, 'r', 'e', seed)
        require(pp, 'C r/e control disconnected')
        common = set.intersection(*({frozenset((a, b)) for a, b in zip(p, p[1:])} for p in pp))
        deletion = {frozenset(e) for e in row['edges'] if not reachable(adj, 'r', 'e', deleted_edge=frozenset(e))}
        wanted = {frozenset(e) for e in row['r_e_bridges']}
        require(common == deletion == wanted, 'same edge in every C path differs from bridge deletion')
        summary.append(dict(name=row['name'], simple_paths=len(pp), r_e_bridges=sorted(sorted(e) for e in common)))
    return summary


def area(poly):
    return sum(a[0]*b[1]-a[1]*b[0] for a, b in zip(poly, poly[1:]+poly[:1])) / 2


def inside(point, polygon):
    # Ray casting independent of stored side labels and local wedge descriptions.
    x, y = point; state = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if (a[1] > y) != (b[1] > y):
            crossing = (b[0]-a[0]) * (y-a[1]) / (b[1]-a[1]) + a[0]
            if x < crossing:
                state = not state
    return state


def wedge(row):
    coords, faces = row['coordinates'], row['actual_faces']
    edge_count = Counter(frozenset((a, b)) for f in faces for a, b in zip(f, f[1:]+f[:1]))
    boundary = {frozenset((a, b)) for a, b in zip(row['boundary'], row['boundary'][1:]+row['boundary'][:1])}
    require({e for e, n in edge_count.items() if n == 1} == boundary and all(n in (1, 2) for n in edge_count.values()), 'actual face/boundary incidences changed')
    require(len(coords) - len(edge_count) + len(faces) == 1, 'triangulated disk Euler mismatch')
    for f in faces:
        require(len(f) == 3 and abs(area([coords[v] for v in f])) > 0, 'degenerate actual triangle')
        require(len({row['colors'][v] for v in f}) == 3, 'actual triangle not literally colored')
    polygon = [coords[v] for v in row['Gamma']]
    face_area = sum(abs(area([coords[v] for v in f])) for f in faces)
    require(face_area == abs(area([coords[v] for v in row['boundary']])), 'disk geometric area changed')
    qfaces = [f for f in faces if 'q' in f]
    labels = [inside([sum(coords[v][i] for v in f)/3 for i in (0, 1)], polygon) for f in qfaces]
    if row['q_is_boundary_corner']:
        require('q' in row['boundary'], 'boundary q premise missing')
        i = row['boundary'].index('q'); n = len(row['boundary'])
        require({row['boundary'][(i-1)%n],row['boundary'][(i+1)%n]} == {'Y', 'c'}, 'boundary q contacts changed')
        j = row['Gamma'].index('q'); n = len(row['Gamma'])
        require({row['Gamma'][(j-1)%n],row['Gamma'][(j+1)%n]} == {'Y', 'c'}, 'Gamma does not use both q boundary edges')
        require(labels and all(labels), 'boundary q has a face outside Gamma')
    else:
        require('q' not in row['boundary'] and any(labels) and not all(labels), 'interior-q negative control failed to show both sides')
    require(labels == row['incident_q_face_inside_labels'], 'stored actual q-face side labels changed')
    return dict(name=row['name'], q_faces=len(qfaces), inside=sum(labels), outside=len(labels)-sum(labels))


def validate(c, seed=0):
    require(c['schema'] == '941-wrong-side-general-v1' and c['base'] == BASE, 'certificate scope drift')
    require(c['scope'] == dict(finite_calibration='triggered and holds', source_control='not triggered', source_realized=False, initial_pair_exclusions=0, smaller_bad=False, new_Lean=False, Gamma_length_bound=None, E_may_be_rootless=True, Wstar_may_equal_q=True, repeated_P_S_meetings_retained=True, general_wrong_side='OPEN'), 'source/exception boundary changed')
    require(c['paper_claims'] == ['fixed_S_inside_centers_independent_of_L', 'opposite_side_shared01_is_C_r_e_bridge', 'opposite_side_shared13_is_same_e_Wstar', 'exact_two_shared_b3_separates_all_B_intersection_C_from_b', 'exact_two_b_equals_c_excludes_shared_b3', 'h_equals_c_implies_b_equals_c_only'], 'paper claim labels changed')
    require(len(c['B13_controls']) == 3 and len(c['C12_controls']) == 2 and len(c['wedge_controls']) == 2, 'control coverage incomplete')
    return dict(B13=separators(c['B13_controls'], seed), C12=c_bridges(c['C12_controls'], seed), wedges=[wedge(r) for r in c['wedge_controls']])


def negative(c):
    mutations = [
        ('promote_source', lambda d:d['scope'].update(source_realized=True)),
        ('erase_rootless_E', lambda d:d['scope'].update(E_may_be_rootless=False)),
        ('erase_q_exception', lambda d:d['scope'].update(Wstar_may_equal_q=False)),
        ('remove_private_cutpoint', lambda d:d['B13_controls'][1].update(unavoidable_Y_b_vertices=[])),
        ('invent_cycle_cutpoint', lambda d:d['B13_controls'][2].update(unavoidable_Y_b_vertices=['q'])),
        ('lose_boundary_Yq', lambda d:d['B13_controls'][0]['edges'].remove(['Y','q'])),
        ('invent_C_bridge', lambda d:d['C12_controls'][1]['r_e_bridges'].append(['r','u'])),
        ('erase_actual_q_face', lambda d:d['wedge_controls'][0]['actual_faces'].pop(0)),
        ('move_boundary_q_face_outside', lambda d:d['wedge_controls'][0]['incident_q_face_inside_labels'].__setitem__(0,False)),
        ('use_interior_q_as_boundary', lambda d:d['wedge_controls'][1].update(q_is_boundary_corner=True)),
        ('swap_one_direction_identity', lambda d:d['paper_claims'].__setitem__(-1,'b_equals_c_implies_h_equals_c_for_all_S')),
    ]
    results=[]
    for name, mutate in mutations:
        bad=deepcopy(c);mutate(bad)
        try: validate(bad)
        except (ValueError,KeyError,TypeError,IndexError): results.append(dict(name=name,status='rejected'))
        else: raise ValueError('corruption accepted: '+name)
    return results


def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');a=p.parse_args()
    count=frozen();c=json.loads(a.certificate.read_text());stats=validate(c,a.seed)
    result=dict(status='PASS',authority_inputs=count,seed=a.seed,finite_calibration='triggered and holds',source_control='not triggered',statistics=stats)
    if a.negative: result['negative_controls']=negative(c)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
