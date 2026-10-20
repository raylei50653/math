#!/usr/bin/env python3
"""Independent finite cap/deletion replay. Default is read-only; stdlib only."""
import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'audits/2026-10-19-r6-941-leakage-b89c591'
BASE = '13dc5ff163045c85b5c82dde438eb5f275dab999'
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
PINS = ('a','n','R','L','q','c','s','v','w','t')
QUERIES = ('G','Q1','Q2','GB','delete_p','delete_h')
K = range(4)
REJECTS = (1,4,6)

def canonical(t):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in t)

def proper(t):
    return all(t[i] != t[(i+1) % len(t)] for i in range(len(t)))

def literal_cycle(n, prefix=()):
    if len(prefix) == n:
        if prefix[-1] != prefix[0]:
            yield prefix
        return
    for c in K:
        if not prefix or prefix[-1] != c:
            yield from literal_cycle(n, prefix+(c,))

def caps(t):
    a,n,r,l,q,c,s,v,w,tt = t
    left = [[b,p,h] for b,p,h in itertools.product(K,repeat=3)
            if b not in (a,c,q,p) and p not in (a,b,q,n,h)
            and h not in (p,q,l,r,n)]
    right = [[x,y,z] for x,y,z in itertools.product(K,repeat=3)
             if x not in (y,c,s,z) and y not in (a,tt,z)
             and z not in (s,v,w,tt)]
    qp = [[b,h] for b,h in itertools.product(K,repeat=2)
          if b not in (a,c,q) and h not in (q,l,r,n)]
    qh = [[b,p] for b,p in itertools.product(K,repeat=2)
          if b not in (a,c,q,p) and p not in (a,b,q,n)]
    return {'G':left,'right':right,'delete_p':qp,'delete_h':qh,
            'Q1':[[n]] if r==q and n not in (a,c,q) else [],
            'Q2':[[n]] if l==n and n not in (a,c,q) else [],
            'GB':[[b] for b in K if b not in (a,c,q,n,r,l)]}

def old_lifts(e,b):
    a,n,r,l,q,c,x,y=e
    return [[p,h] for p,h in itertools.product(K,repeat=2)
            if p not in (a,b,q,n,h) and h not in (p,q,l,r,n)]

def full_edges_test(t, cc):
    # All original incident edges, written independently of cap formulas.
    values = dict(zip(PINS,t))
    a,n,r,l,q,c,s,v,w,tt=t
    leftedges=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),
               ('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'))
    rightedges=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),
                ('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
    for triple in cc['G']:
        v0=dict(values,**dict(zip(('b','p','h'),triple)))
        assert all(v0[u]!=v0[v] for u,v in leftedges)
    for triple in cc['right']:
        v0=dict(values,**dict(zip(('x','y','r'),triple)))
        assert all(v0[u]!=v0[v] for u,v in rightedges)
    return len(cc['G'])*len(cc['right'])

def reconstruct():
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    assert manifest['base']==BASE
    for item in manifest['inputs']:
        data=(ROOT/item['path']).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'], 'frozen input drift: '+item['path']
    ten=sorted({canonical(t) for t in literal_cycle(10)})
    index={t:i for i,t in enumerate(ten)}
    assert len(ten)==2461
    records=[]; cartesian=0
    for t in ten:
        cc=caps(t)
        cartesian+=full_edges_test(t,cc)
        records.append({'core':list(t),**cc})
    mats={name:[Counter() for _ in ROWS] for name in QUERIES}
    rowindex={tuple(map(int,row)):i for i,row in enumerate(ROWS)}
    # Every literal core assignment once. No orbit-size division or marginal join.
    for t in literal_cycle(10):
        j=index[canonical(t)]; cc=caps(t); a,n,r,l,q,c,*_=t
        for x,y,z in cc['right']:
            if (x,y)!=(0,1):
                continue
            for name in QUERIES:
                for lift in cc[name]:
                    b=lift[0]
                    ri=rowindex.get((x,y,a,b,c))
                    if ri is not None:
                        mats[name][ri][j]+=1
    sparse={name:[sorted(row.items()) for row in matrix] for name,matrix in mats.items()}
    eq=[]
    # Complete quotient local interfaces in every literal row, including empties.
    for name in ('Q1','Q2'):
        for ri,row in enumerate(ROWS):
            x,y,a,b,c=map(int,row)
            for n,r,l,q in itertools.product(K,repeat=4):
                e=(a,n,r,l,q,c,x,y)
                if not proper(e) or b in (a,c,q):
                    continue
                if not (n==b and (r==q if name=='Q1' else l==b)):
                    continue
                lifts=old_lifts(e,b)
                expected=(l!=a) if name=='Q1' else (a==q or r!=a)
                assert bool(lifts)==expected
                if ri in REJECTS and not lifts:
                    assert a!=q
                    d=next(iter(set(K)-{a,b,q}))
                    # Exact injective, disjoint images in both deletion graphs.
                    assert [b,d] in caps((a,n,r,l,q,c,0,1,0,1))['delete_p']
                    assert [b,d] in caps((a,n,r,l,q,c,0,1,0,1))['delete_h']
                eq.append({'candidate':name,'row':row,'E':list(e),'old_lifts':lifts})
    catalog=json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())
    known=set(map(int,catalog['cells']))
    supersets=sorted(m for m in known if m&941==941)
    assert supersets==[943,957,959,1005,1007,1021,1023]
    source=json.loads((OLD/'A/source-positive-certificate.json').read_text())
    controls=[]
    for control in source['records']:
        z=control['core_counts']
        counts={name:[sum(z[i]*n for i,n in row) for row in sparse[name]] for name in QUERIES}
        masks={name:sum(1<<i for i,n in enumerate(ns) if n) for name,ns in counts.items()}
        assert counts['G']==control['graph_counts']['G']
        for name in ('Q1','Q2','GB'):
            assert counts[name]==control['graph_counts'][name]
        assert masks['G']==941
        for ri in REJECTS:
            leak=counts['Q1'][ri]+counts['Q2'][ri]
            assert leak<=counts['delete_p'][ri]
            assert leak<=counts['delete_h'][ri]
        controls.append({'name':control['name'],'counts':counts,'masks':masks,
                         'deletion_minimality_admissible':all(masks[name] in supersets for name in ('delete_p','delete_h')),
                         'source_realized':False})
    negatives=negative_controls(eq,controls)
    return {'base':BASE,'pin_order':PINS,'rows':ROWS,'scope':'finite full cap algebra and two genuine deletion-graph necessary conditions; no source realization',
            'core_count':len(ten),'canonical_cartesian_members':cartesian,'cores':records,
            'query_matrices':sparse,'complete_quotient_interfaces':eq,
            'source941_deletion_supports_in_K132':supersets,'controls':controls,'negative_controls':negatives}

def candidate_target(counts):
    return any(counts[name][9]>0 and all(counts[name][j]==0 for j in REJECTS) for name in ('Q1','Q2'))

def negative_controls(eq, controls):
    # Explicit invalid witnesses, separate from the true-source theorem.
    bad={'Q1':[0]*10,'Q2':[0]*10}
    bad['Q1'][9]=bad['Q2'][9]=1
    bad['Q1'][1]=1;bad['Q2'][4]=1
    assert all(any(bad[q][j]==0 for q in bad) for j in REJECTS)
    assert not candidate_target(bad)
    positive_counts={c['name']:c['source_positive_subset_counts'] for c in json.loads((OLD/'A/source-positive-certificate.json').read_text())['records']}
    assert all(all(n>0 for n in vals.values()) for vals in positive_counts.values())
    zero_core=[0]*2461
    assert not any(zero_core), 'zero control lacks every required positive source fibre'
    aq=next(r for r in eq if r['candidate']=='Q2' and r['E'][0]==r['E'][4]==r['E'][2] and r['old_lifts'])
    multiple=next(r for r in eq if len(r['old_lifts'])>1)
    # A valid ordered switch must recompute the next component on its new colouring.
    edge=[(0,1),(1,2)];before=(0,1,2);after=(1,0,2)
    def component(col,palette,start):
        reached={start};todo=[start]
        while todo:
            u=todo.pop()
            for x,y in edge:
                v=y if x==u else x if y==u else None
                if v is not None and col[v] in palette and v not in reached:
                    reached.add(v);todo.append(v)
        return sorted(reached)
    old_component=component(before,{0,2},0)
    new_component=component(after,{0,2},1)
    assert old_component==[0] and new_component==[1,2]
    assert len(multiple['old_lifts'])>1
    d={'status':'all negative controls detected','cross_candidate':bad,
       'Q2_a_equals_q_equals_R':aq,'multiple_old_lifts':multiple,
       'cross_colouring_path':{'edges':edge,'before':before,'after':after,'old_02_component_from_0':old_component,'new_02_component_from_1':new_component},
       'source_positive_counts':positive_counts,
       'zero_control_source_positive':False,
       'source_positive_required':True,'completion_costs':{'Q1':-4,'Q2':-4,'delete_p':-1,'delete_h':-1}}
    assert d['completion_costs']['Q1']==-4
    assert all(not c['source_realized'] for c in controls)
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate-v2.json');ap.add_argument('--negative-control',action='store_true')
    args=ap.parse_args();got=reconstruct()
    if args.build:
        with args.certificate.open('x') as f:json.dump(got,f,separators=(',',':'));f.write('\n')
    expected=json.loads(args.certificate.read_text())
    assert expected==json.loads(json.dumps(got)), 'certificate differs from independent exact reconstruction'
    if args.negative_control:
        mutations=[]
        m=copy.deepcopy(expected);m['negative_controls']['completion_costs']['Q1']=-5;mutations.append(m)
        m=copy.deepcopy(expected);m['complete_quotient_interfaces'][0]['old_lifts']=[];mutations.append(m)
        m=copy.deepcopy(expected);m['controls'][0]['source_realized']=True;mutations.append(m)
        for mutation in mutations:
            rejected=False
            try:
                assert mutation==json.loads(json.dumps(got)), 'corrupted certificate rejected'
            except AssertionError:
                rejected=True
            assert rejected
        print(json.dumps({'corrupted_certificate_negative_controls_rejected':len(mutations)},sort_keys=True))
    print(json.dumps({'pass':True,'core_count':got['core_count'],'local_interfaces':len(got['complete_quotient_interfaces']),
                      'deletion_minimality_controls':[{ 'name':c['name'],'masks':c['masks'],'admissible':c['deletion_minimality_admissible']} for c in got['controls']],
                      'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
                      'negative_controls':args.negative_control},sort_keys=True))

if __name__=='__main__':main()
