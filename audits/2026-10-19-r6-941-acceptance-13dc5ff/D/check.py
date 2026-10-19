#!/usr/bin/env python3
"""Exact c=5 cap, q=6 exclusion and completed changed-boundary comparison."""
import argparse
import copy
import hashlib
import importlib.util
from itertools import product
import json
from math import factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
OLD=ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec=importlib.util.spec_from_file_location('frozen_interface',OLD)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
PINS=('a','n','R','L','q','u','s','v','w','t')

def packed(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()

def digest(obj):
    return hashlib.sha256(packed(obj)).hexdigest()

def matrices():
    ten=[t for t in m.growth(10,four=True) if m.proper(t)]
    original=[[0]*len(ten) for _ in m.ROWS]
    changed=[[0]*len(ten) for _ in m.ROWS]
    caps=[]
    def left(a,n,R,L,q,c):
        return [(b,p,h) for b,p,h in product(range(4),repeat=3)
                if b not in (a,c,q,p) and p not in (a,q,n,h) and h not in (q,R,L,n)]
    def right(a,c,s,v,w,t):
        return [(x,y,r) for x,y,r in product(range(4),repeat=3)
                if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t)]
    for i,(a,n,R,L,q,u,s,v,w,t) in enumerate(ten):
        entries=[]
        for c in range(4):
            ls=left(a,n,R,L,q,c) if c not in (q,u,s) else []
            rs=right(a,c,s,v,w,t) if c not in (q,u,s) else []
            entries.append({'c':c,'proper_c':c not in (q,u,s),'left':ls,'right':rs})
            for b,p,h in ls:
                for x,y,r in rs:
                    row=''.join(map(str,m.canonical((x,y,a,b,c))))
                    original[m.ROWS.index(row)][i]+=1
        ls=left(a,n,R,L,q,u)
        rs=right(a,u,s,v,w,t)
        for b,p,h in ls:
            for x,y,r in rs:
                row=''.join(map(str,m.canonical((x,y,a,b,u))))
                changed[m.ROWS.index(row)][i]+=1
        caps.append({'original_by_c':entries,'changed_left':ls,'changed_right':rs})
        # Every fixed C5 word uses >=3 colours; unused core-colour permutations
        # act freely on the normalized full lifts. This converts canonical-word
        # totals to one fixed literal word, without multiplying by orbit size.
        stabilizer=factorial(4-len(set(ten[i])))
        for matrix in (original,changed):
            for row in matrix:
                assert row[i]%stabilizer==0
                row[i]//=stabilizer
    return ten,original,changed,caps

def closure_record(K,initial,C,N):
    live,rounds=m.close(K,initial)
    return {'initial':len(initial),'round_sizes':[len(r) for r in rounds],
            'final_live':len(live),'trace_sha256':digest(rounds),
            'original_support_upper':m.mask([sum(row[i] for i in live) for row in C]),
            'changed_support_upper':m.mask([sum(row[i] for i in live) for row in N]),
            'original_alpha_cells':[i for i in live if C[9][i]],
            'final_live_sha256':digest(live)},live,rounds

def compute():
    ten,C,N,caps=matrices()
    K=m.kempe(10,ten)
    initial=[i for i in range(len(ten)) if all(C[r][i]==0 for r in (1,4,6))]
    general,live,_=closure_record(K,initial,C,N)
    assert general['original_support_upper']==941
    q6_initial=[i for i in initial if ten[i][3]!=ten[i][5]]
    q6,q6_live,q6_rounds=closure_record(K,q6_initial,C,N)
    assert q6['original_support_upper']==429 and not q6['original_alpha_cells']
    catalogue=sorted(map(int,json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())['cells']))
    comparisons=[]
    compatible=[]
    for mask in catalogue:
        seed=[i for i in initial if all(N[r][i]==0 for r in range(10) if not(mask>>r&1))]
        record,_,_=closure_record(K,seed,C,N)
        record['allowed_catalogue_support']=mask
        comparisons.append(record)
        if record['original_alpha_cells']:
            compatible.append(mask)
            assert record['original_support_upper']==941
    assert compatible==[1022,1023]
    cert={'base':BASE,'source_realized':False,'strict_smaller_bad_constructed':False,
          'pin_order':PINS,'literal_words':m.ROWS,'original_boundary':('x','y','a','b','c'),
          'changed_boundary':('x','y','a','b','u'),
          'changed_operation':{'deleted':['c'],'added_edges':[['b','u'],['u','x']],
                               'completed_inner_delta':-1,'new_vertices':0},
          'q6_required_edge':['L','u'],'ten':ten,'original_matrix':C,'changed_matrix':N,
          'caps_sha256':digest(caps),'component_family_sha256':digest(K['columns']),
          'component_columns':len(K['columns']),'general_c5':general,
          'q6_c5_exclusion':q6,'q6_c5_rounds':q6_rounds,
          'catalogue_comparisons':comparisons,'compatible_catalogue_supports':compatible}
    return cert,caps

def verify(actual,expected):
    assert actual==expected,'complete c5 cap, fixed words, same core, actual edge or completed cost mismatch'

def negatives(cert):
    results=[]
    mutations=[('omit_actual_Lu_edge',lambda z:z.__setitem__('q6_required_edge',[])),
               ('forget_boundary_promotion_cost',lambda z:z['changed_operation'].__setitem__('completed_inner_delta',0)),
               ('silently_keep_old_boundary',lambda z:z.__setitem__('changed_boundary',z['original_boundary'])),
               ('drop_one_complete_cap_coefficient',lambda z:z['changed_matrix'][9].__setitem__(next(i for i,v in enumerate(z['changed_matrix'][9]) if v),0)),
               ('claim_c5_excluded',lambda z:z['general_c5'].__setitem__('original_support_upper',429)),
               ('omit_catalogue_mask',lambda z:z['catalogue_comparisons'].pop())]
    for name,mutate in mutations:
        wrong=copy.deepcopy(cert);mutate(wrong)
        try:verify(wrong,cert)
        except AssertionError:results.append({'name':name,'rejected':True})
        else:raise AssertionError('accepted '+name)
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true')
    ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args()
    expected,caps=compute()
    if args.build:
        with args.certificate.open('xb') as f:f.write(packed(expected))
        with (HERE/'cap-lifts.json').open('xb') as f:f.write(packed(caps))
    cert=json.loads(args.certificate.read_text())
    # JSON round trip makes tuple/list representation explicit and deterministic.
    verify(cert,json.loads(packed(expected)))
    assert (HERE/'cap-lifts.json').read_bytes()==packed(caps),'complete cap lift mismatch'
    print(json.dumps({'pass':True,'base':BASE,'original_c5_q6_excluded':True,
                      'c5_implies_q_at_least_7':True,'c5_alone_excluded':False,
                      'changed_candidate_completed_inner_delta':-1,
                      'changed_candidate_supports_if_c5':[1022,1023],
                      'source_realized':False,'smaller_bad_constructed':False,
                      'negative_controls':negatives(cert),
                      'certificate_sha256':hashlib.sha256(packed(expected)).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
