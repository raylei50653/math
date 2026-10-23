#!/usr/bin/env python3
"""Read-only, independently enumerated original and quotient graph full lifts.

The checker certifies fixed finite relations, not the paper's source premises.
"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CAP = 'audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json'
CAT = 'artifacts/c5_cells/cells.json'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(w):
    names = {}
    return tuple(names.setdefault(c,len(names)) for c in w)


def custody():
    data = json.loads((HERE/'INPUTS-v2.json').read_text())
    require(data['base'] == BASE, 'input BASE')
    for row in data['inputs']:
        raw = (HERE/row['snapshot']).read_bytes()
        require((len(raw),sha256(raw).hexdigest()) == (row['bytes'],row['sha256']), 'snapshot drift')
        if row['authority'] == 'immutable':
            require((ROOT/row['path']).read_bytes() == raw,'live input drift '+row['path'])
    prior = json.loads((HERE/'entry/audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/FINAL_MANIFEST.json').read_text())
    for row in prior['entries']:
        raw = (ROOT/row['path']).read_bytes()
        require((len(raw),sha256(raw).hexdigest()) == (row['bytes'],row['sha256']),'predecessor drift')
    return len(data['inputs']),len(prior['entries'])


def topology(cap):
    boundary,inner = cap['boundary'],cap['inner']
    edges = {tuple(sorted(e)) for e in cap['edges']}
    faces = [tuple(f) for f in cap['faces']]
    rim = {tuple(sorted((boundary[i],boundary[(i+1)%6]))) for i in range(6)}
    incidence = {e:[] for e in edges}
    for j,f in enumerate(faces):
        for a,b in combinations(f,2):
            require(tuple(sorted((a,b))) in edges,'face nonedge')
            incidence[tuple(sorted((a,b)))].append(j)
    require({e for e,uses in incidence.items() if len(uses)==1}==rim,'actual disk rim')
    require(all(len(fs)==(1 if e in rim else 2) for e,fs in incidence.items()),'edge manifold')
    require(len(boundary)+len(inner)-len(edges)+len(faces)==1,'Euler disk')
    dual = {j:set() for j in range(len(faces))}
    for fs in incidence.values():
        if len(fs)==2:
            a,b=fs;dual[a].add(b);dual[b].add(a)
    seen={0};todo=[0]
    while todo:
        for j in dual[todo.pop()]-seen:
            seen.add(j);todo.append(j)
    require(len(seen)==len(faces),'face connectivity')
    # Links are single circles at all eight old interior vertices, paths at rim.
    for v in boundary+inner:
        link={}
        for f in faces:
            if v in f:
                a,b=[z for z in f if z!=v]
                link.setdefault(a,set()).add(b);link.setdefault(b,set()).add(a)
        require(all(len(s) in (1,2) for s in link.values()),'link branches')
        require(sum(len(s)==1 for s in link.values())==(2 if v in boundary else 0),'link ends')
        seen={next(iter(link))};todo=list(seen)
        while todo:
            for z in link[todo.pop()]-seen:
                seen.add(z);todo.append(z)
        require(seen==set(link),'link connectivity')
    return edges


def original(cap,words):
    edges=topology(cap)
    boundary,inner=cap['boundary'],cap['inner']
    within=[(inner.index(a),inner.index(b)) for a,b in edges if a in inner and b in inner]
    crossing=[]
    for a,b in edges:
        if (a in inner)!=(b in inner):
            if a in boundary:
                a,b=b,a
            crossing.append((inner.index(a),boundary.index(b)))
    # Cartesian full enumeration, independent of producer's frozen lift lists.
    tuples=[t for t in product(range(4),repeat=8) if all(t[a]!=t[b] for a,b in within)]
    return {w:sorted([list(t) for t in tuples if all(t[a]!=w[b] for a,b in crossing)]) for w in words}


def candidate(g,words):
    constraints=g['constraints'];spokes=g['spokes']
    require(len({tuple(e) for e,s in constraints})==len(constraints),'duplicate operation')
    for e,s in constraints:
        require(len(e)==2 and 0<=e[0]<e[1]<6 and e[1]-e[0] not in (1,5) and type(s) is int and s in (0,1),'malformed diagonal')
    for (a,b),_ in constraints:
        for (c,d),_ in constraints:
            require(not (a<c<b<d),'crossed disk diagonals')
    # The only one-new-point filling is the explicitly drawn five-wheel+ear.
    require(not spokes or (spokes==list(range(5)) and constraints==[[[0,4],1]]),'unproved hub embedding')
    groups=[{i} for i in range(6)]
    for (a,b),s in constraints:
        if s==0:
            ga=next(t for t in groups if a in t);gb=next(t for t in groups if b in t)
            if ga is not gb:
                groups.remove(ga);groups.remove(gb);groups.append(ga|gb)
    mapping=[min(next(t for t in groups if i in t)) for i in range(6)]
    vertices=sorted({min(t) for t in groups}|({6} if spokes else set()))
    edges={tuple(sorted((mapping[i],mapping[(i+1)%6]))) for i in range(6)}
    edges|={tuple(sorted((mapping[a],mapping[b]))) for (a,b),s in constraints if s==1}
    edges|={(mapping[i],6) for i in spokes}
    require(all(a!=b for a,b in edges),'candidate loop')
    require(g['vertex_map']==mapping and g['vertices']==vertices and g['edges']==[list(e) for e in sorted(edges)],'quotient graph drift')
    saving=8+6-len(groups)-bool(spokes)
    require(g['completed_interior_saving']==saving and saving>=7,'strict completed size')
    result={w:[] for w in words}
    # Enumerate the actual graph assignments, then pull through its contact map.
    for t in product(range(4),repeat=len(vertices)):
        colors=dict(zip(vertices,t))
        if any(colors[a]==colors[b] for a,b in edges):
            continue
        w=tuple(colors[v] for v in mapping)
        if canonical(w)==w:
            require(w in result,'inherited proper rim lost')
            result[w].append(list(t))
    for row in g['relations']:
        require(set(row)=={'word','full_lifts'},'unexpected candidate fields')
    expected=[dict(word=list(w),full_lifts=result[w]) for w in words]
    require(g['relations']==expected,'complete candidate fibres/lifts drift')
    return result


def validate(cert,seed=0):
    input_count,manifest_count=custody()
    old=json.loads((HERE/'entry'/CAP).read_text())
    words=sorted({canonical(w) for w in product(range(4),repeat=6) if all(w[i]!=w[(i+1)%6] for i in range(6))})
    require(len(words)==31 and cert['words']==[list(w) for w in words],'complete 31-word domain')
    require(cert['schema']=='941-eight-inner-safe-cover-v1' and cert['base']==BASE,'schema/BASE')
    require(cert['ordered_boundary']==old['boundary']==['U','p_d','d','zeta','x','p_x'],'same ordered boundary')
    require(cert['ordered_inner']==old['inner']==['r','T','s','tau','m','n','u','v'],'same complete interior')
    require(cert['source_controls']=='not triggered' and cert['selection']=='one genuine original 01232 full witness selects one graph once; every rejection backfills through that same graph','same-source declarations')
    require([g['id'] for g in cert['candidates']]==list(range(len(cert['candidates']))),'candidate identity')
    new={g['id']:candidate(g,words) for g in cert['candidates']}
    require([c['cap_id'] for c in cert['caps']]==list(range(16)),'all sixteen caps')
    checks=0;counts=[];totals=[];used=set()
    caps=list(cert['caps']);random.Random(seed).shuffle(caps)
    for record in caps:
        cap=old['caps'][record['cap_id']]
        relation=original(cap,words)
        normalized=[dict(word=r['word'],full_lifts=sorted(r['full_lifts'])) for r in record['relations']]
        require(normalized==[dict(word=list(w),full_lifts=relation[w]) for w in words],'original complete fibres/lifts drift')
        chosen=record['candidates']
        require(len(chosen)==len(set(chosen)) and all(i in new for i in chosen),'selected candidate domain')
        support={w for w in words if relation[w]}
        cover=set()
        for i in chosen:
            rows={w for w in words if new[i][w]}
            require(rows<=support,'same-candidate backfill leakage')
            cover|=rows;used.add(i)
        require(cover==support,'accepted witness coverage gap')
        for w in support:
            selected=next(i for i in chosen if new[i][w])
            require(all(not new[selected][z] or relation[z] for z in words),'one selected graph must backfill all rows')
            checks+=len(words)
        counts.append(len(support));totals.append(sum(map(len,relation.values())))
    require(used==set(new),'unused certificate candidates')
    catalogue=json.loads((HERE/'entry'/CAT).read_text())
    require(len(set(catalogue['cells']))==132,'K132 scope')
    require([''.join(map(str,w)) for w in catalogue['pattern_order']]==['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232'],'catalogue literal frame')
    require(not any((int(m)&594)==512 for m in catalogue['cells']),'four-row countermodel')
    return dict(status='PASS',seed=seed,frozen_inputs=input_count,previous_manifest_entries=manifest_count,immutable_drift=0,
        caps=16,complete_proper_words=31,original_relation_sizes=sorted(Counter(counts).items()),
        complete_original_lifts=sum(totals),candidates=len(new),all_backfill=True,complete_safe_cover=True,
        same_candidate_all_row_checks=checks,savings=sorted({g['completed_interior_saving'] for g in cert['candidates']}),
        source_controls='not triggered',paper='conditional sealed cap, planarity, actual accepted witness and global minimum: PROOF.md')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,default=HERE/'reduction-certificate.json')
    p.add_argument('--seed',type=int,default=0)
    p.add_argument('--negative',action='store_true')
    a=p.parse_args();cert=json.loads(a.certificate.read_text())
    result=validate(cert,a.seed)
    if a.negative:
        tests=[('missing_empty_fibre',lambda c:c['caps'][0]['relations'].pop(1)),
            ('lost_original_lift',lambda c:c['caps'][0]['relations'][0]['full_lifts'].pop()),
            ('wrong_original_frame',lambda c:c['ordered_boundary'].reverse()),
            ('wrong_quotient_map',lambda c:c['candidates'][0]['vertex_map'].__setitem__(0,5)),
            ('missing_cover',lambda c:c['caps'][0].update(candidates=[])),
            ('wrong_size',lambda c:c['candidates'][0].update(completed_interior_saving=100)),
            ('false_source',lambda c:c.update(source_controls='triggered and holds')),
            ('changed_candidate_lift',lambda c:c['candidates'][0]['relations'][0]['full_lifts'].append([0])),
            ('missing_cap',lambda c:c['caps'].pop()),
            ('unproved_hub',lambda c:next(g for g in c['candidates'] if g['spokes']).update(spokes=list(range(6))))]
        rejected=[]
        for name,mutate in tests:
            bad=deepcopy(cert);mutate(bad)
            try:
                validate(bad,a.seed)
            except (ValueError,KeyError,IndexError,StopIteration):
                rejected.append(name)
            else:
                raise ValueError('negative accepted: '+name)
        result=dict(status='PASS',semantic_negatives_rejected=rejected,source_controls='not triggered')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps(dict(status='FAIL',reason=str(e)),sort_keys=True))
        raise SystemExit(1)
