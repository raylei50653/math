#!/usr/bin/env python3
"""Check all nonempty whole-cap maps without importing either worker model."""
import argparse
from collections import Counter, defaultdict, deque
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = 'audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/'
NEW = 'audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/explore.json'
OLD = 'audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/certificate.json'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def edge(a, b):
    return tuple(sorted((a, b)))


def read(path):
    return json.loads((HERE / 'reviewed' / path).read_text())


def custody():
    manifest = json.loads((HERE / 'REVIEWED-INPUTS.json').read_text())
    for row in manifest['entries']:
        frozen = (HERE / row['snapshot']).read_bytes()
        require(len(frozen) == row['bytes'] and hashlib.sha256(frozen).hexdigest() == row['sha256'], 'reviewed snapshot drift')
    # The finite exchange and transfer files are final; prose was frozen at review time.
    immutable = [NEW, OLD, PREFIX+'analyze_caps.py', PREFIX+'transfer_caps.py', PREFIX+'cap-transfer-certificate.json']
    for name in immutable:
        require((ROOT / name).read_bytes() == (HERE / 'reviewed' / name).read_bytes(), 'final finite input drift '+name)
    return dict(frozen_reviewed_files=len(manifest['entries']), final_finite_inputs=len(immutable), finite_drift=0)


def same_side_obstruction(row):
    color = dict(r=1,T=0,s=1,x=0,h=1,W=3,e=1,d=0,tau=3,zeta=2,m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,omega=int(row['omega_type'][1]))
    K = {'d','x','zeta','p_d','p_x','U','omega'}
    psi = {v: (c ^ 2 if v in K else c) for v, c in color.items()}
    parent = {v: v for v in color if psi[v] in {1, 2}}
    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for a,b in row['edges']:
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    groups = defaultdict(set)
    for v in parent:
        groups[find(v)].add(v)
    blocked = [s for s in groups.values() if s & {'r','d','e','U'} and s & {'s','x','h'}]
    return None if not blocked else sorted(blocked[0])


def complex_from_row(row):
    source_edges = {edge(*e) for e in row['edges']}
    centers = set(row['full_links']) | {'tau'}
    faces = {tuple(sorted((v,a,b))) for v,lk in row['full_links'].items() for a,b in zip(lk,lk[1:]+lk[:1])}
    tau_neighbors = {b if a == 'tau' else a for a,b in source_edges if 'tau' in (a,b)}
    faces |= {tuple(sorted(('tau',a,b))) for a,b in itertools.combinations(tau_neighbors,2) if edge(a,b) in source_edges}
    incidence = defaultdict(list)
    for i,f in enumerate(sorted(faces)):
        for a,b in itertools.combinations(f,2):
            incidence[edge(a,b)].append(i)
    vertices = set().union(*map(set,faces))
    face_edges = set(incidence)
    for v in centers:
        all_known = {b if a == v else a for a,b in source_edges if v in (a,b)}
        full_face_neighbors = {b if a == v else a for a,b in face_edges if v in (a,b)}
        require(all_known == full_face_neighbors, 'missing original full-star edge')
        if v != 'tau':
            require(all_known == set(row['full_links'][v]), 'private link omits source neighbor')
    return vertices, face_edges, faces, incidence


def verify_maps(cert, rows, oldcaps):
    require(len(cert['entries']) == len(rows) == 563, 'complete row domain')
    require([e['row'] for e in cert['entries']] == list(range(563)), 'same complete ordered rows')
    counts = Counter()
    for row,entry in zip(rows,cert['entries']):
        counts[entry['kind']] += 1
        blocked = same_side_obstruction(row)
        if entry['kind'] == 'forbidden_common_C_E_component':
            require(blocked is not None and entry['component'] == blocked, 'literal C/E obstruction')
            continue
        require(blocked is None, 'unremoved C/E obstruction')
        if entry['kind'] == 'forbidden_d_x_exterior_common_neighbor':
            es = {edge(*e) for e in row['edges']}
            require(entry['witness'] == 'p_d' and {edge('d','p_d'),edge('x','p_d'),edge('d','zeta'),edge('x','zeta')} <= es, 'original d/x C4 obstruction')
            continue
        require(entry['kind'] == 'old_cap', 'unknown transfer authority')
        vertices, edges, faces, incidence = complex_from_row(row)
        require((len(vertices),len(edges),len(faces)) == (14,33,20), 'complete cap dimensions')
        require(all(len(fs) in {1,2} for fs in incidence.values()), 'face edge overuse')
        old = oldcaps[entry['old_cap']]
        require(old['id'] == entry['old_cap'], 'old cap literal ID')
        mp = entry['mapping']
        require(set(mp) == vertices and set(mp.values()) == set(old['inner']+old['boundary']) and len(set(mp.values())) == 14, 'one whole-graph bijection')
        require({edge(mp[a],mp[b]) for a,b in edges} == {edge(*e) for e in old['edges']}, 'all mapped cap edges')
        require({tuple(sorted(mp[v] for v in f)) for f in faces} == {tuple(sorted(f)) for f in old['faces']}, 'all mapped cap actual faces')
        boundary_edges = {e for e,fs in incidence.items() if len(fs) == 1}
        bd = entry['boundary']
        require(len(bd) == len(set(bd)) == 6 and boundary_edges == {edge(a,b) for a,b in zip(bd,bd[1:]+bd[:1])}, 'one simple literal collar')
        mapped_bd = [mp[v] for v in bd]
        old_bd = old['boundary']
        dihedral = [seq[i:]+seq[:i] for seq in [old_bd,old_bd[::-1]] for i in range(6)]
        require(mapped_bd in dihedral, 'one whole-boundary dihedral map')
        require({mp[v] for v in row['full_links']} | {mp['tau']} == set(old['inner']), 'all eight private centres are the old interior')
        # Face orientation is one global choice, propagated across shared edges.
        fs = sorted(faces)
        signs = {0: 1}
        pending = deque([0])
        def dart_sign(f,a,b):
            return 1 if any((f[j],f[(j+1)%3]) == (a,b) for j in range(3)) else -1
        while pending:
            i = pending.popleft()
            for a,b in itertools.combinations(fs[i],2):
                for j in incidence[edge(a,b)]:
                    if j == i:
                        continue
                    expected = -signs[i] * dart_sign(fs[i],a,b) * dart_sign(fs[j],a,b)
                    if j in signs:
                        require(signs[j] == expected, 'shared face orientations conflict')
                    else:
                        signs[j] = expected
                        pending.append(j)
        require(len(signs) == 20, 'disconnected actual face union')
    require(counts == {'old_cap':513,'forbidden_common_C_E_component':44,'forbidden_d_x_exterior_common_neighbor':6}, 'transfer counts')
    require(cert['authority'] == dict(source_realizability='not triggered',finite_control='triggered and holds',general_wrong_side='OPEN',all_eleven_types='OPEN',one_candidate_for_all_four_rows=True), 'source/candidate boundary')
    return dict(counts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    ap.add_argument('--certificate', type=Path)
    args = ap.parse_args()
    frozen = custody()
    cert = json.loads(args.certificate.read_text()) if args.certificate else read(PREFIX+'cap-transfer-certificate.json')
    rows = read(NEW)
    oldcaps = {c['id']:c for c in read(OLD)['caps']}
    result = verify_maps(cert,rows,oldcaps)
    rejected = []
    if args.negative:
        for label,mutate in [
            ('omit_source_row',lambda c:c['entries'].pop()),
            ('collapse_actual_boundary',lambda c:c['entries'][0]['mapping'].update(U='d')),
            ('reverse_only_one_contact',lambda c:c['entries'][0]['boundary'].__setitem__(0,c['entries'][0]['boundary'][2])),
            ('invent_source_realization',lambda c:c['authority'].update(source_realizability='triggered and holds'))]:
            bad = copy.deepcopy(cert)
            mutate(bad)
            try:
                verify_maps(bad,rows,oldcaps)
            except (ValueError,KeyError):
                rejected.append(label)
            else:
                raise ValueError('negative accepted '+label)
    print(json.dumps(dict(status='PASS',custody=frozen,independent_transfer=result,
                         complete_bijections=513,edges_per_cap=33,actual_faces_per_cap=20,
                         complete_private_stars_per_cap=8,source_realizability='not triggered',
                         negative_rejected=rejected),sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
