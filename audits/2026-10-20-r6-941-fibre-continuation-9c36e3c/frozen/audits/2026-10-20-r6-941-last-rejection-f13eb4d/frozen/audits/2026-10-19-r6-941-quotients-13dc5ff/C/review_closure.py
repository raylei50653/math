#!/usr/bin/env python3
"""Independent run-partition generation of every C10 component column and closure.

Unlike A/model.py, this enumerates partitions separately on the two sets of
monochromatic side-runs, then checks noncrossing and the region-count rule.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_cap_check',HERE/'check.py')
cap=importlib.util.module_from_spec(spec);spec.loader.exec_module(cap)
GROUP=tuple(p for p in itertools.permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2)
FOUR=tuple(itertools.combinations(range(10),4))

def hcanonical(t):
    return min(tuple(p[x] for x in t) for p in GROUP)

@lru_cache(None)
def partitions(n):
    if n==0:return ((),)
    if n==1:return ((0,),)
    return tuple(p+(j,) for p in partitions(n-1) for j in range(max(p)+2))

@lru_cache(None)
def templates(side):
    # Cyclic adjacent boundary vertices on one side lie in one actual component.
    n=len(side)
    parent=list(range(n))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for i in range(n):
        j=(i+1)%n
        if side[i]==side[j]:parent[root(j)]=root(i)
    runs=[root(i) for i in range(n)]
    roots=[sorted({runs[i] for i in range(n) if side[i]==s}) for s in (0,1)]
    required=sum(side[i]!=side[(i+1)%n] for i in range(n))//2+1
    answer=set()
    for p0,p1 in itertools.product(partitions(len(roots[0])),partitions(len(roots[1]))):
        labels={r:(s,p) for s,part in enumerate((p0,p1)) for r,p in zip(roots[s],part)}
        p=cap.canonical(tuple(labels[r] for r in runs))
        if max(p)+1!=required:continue
        if any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in itertools.combinations(range(n),4)):continue
        answer.add(p)
    return tuple(sorted(answer))

def compute(extra_cases=False):
    literal=list(cap.literal_cycle(10))
    ten=sorted({cap.canonical(t) for t in literal});index={t:i for i,t in enumerate(ten)}
    hnames={t:hcanonical(t) for t in literal};hrows=sorted(set(hnames.values()));hi={t:i for i,t in enumerate(hrows)}
    hindex={t:hi[hnames[t]] for t in literal}
    rowids=[index[cap.canonical(t)] for t in hrows]
    columns=set()
    for t in hrows:
        for p in templates(tuple(c//2 for c in t)):
            values=Counter()
            for mask in range(1<<(max(p)+1)):
                changed=tuple(c^1 if mask&(1<<p[i]) else c for i,c in enumerate(t))
                values[hindex[changed]]+=1
            columns.add(tuple(sorted(values.items())))
    columns=sorted(columns)
    assert len(columns)==10798 and len(hrows)==7382 and len(literal)==59052
    core=json.loads((HERE/'certificate-v2.json').read_text())
    G=core['query_matrices']['G']
    forbidden={i for ri in (1,4,6) for i,n in G[ri] if n}
    qs={i for i,t in enumerate(ten) if t[4]==t[6]}
    live=set(range(2461))-forbidden-qs;initial=sorted(live);rounds=[]
    while True:
        possible=set()
        for col in columns:
            if all(rowids[h] in live for h,mult in col):possible.update(h for h,mult in col)
        witnesses={}
        for h,i in enumerate(rowids):
            if i in live and h not in possible:witnesses.setdefault(i,h)
        if not witnesses:break
        rounds.append([[i,witnesses[i]] for i in sorted(witnesses)])
        live.difference_update(witnesses)
    alpha=set(i for i,n in G[9] if n)
    assert not live&alpha
    result={'status':'PASS','literal_rows':59052,'H_rows':7382,'orbit_columns':10798,
            'independent_method':'partition cyclic side-runs separately, combine and check noncrossing; direct cap G coefficients',
            'columns_sha256':hashlib.sha256(json.dumps(columns,separators=(',',':'),sort_keys=True).encode()).hexdigest(),
            'initial':initial,'rounds':rounds,'live':sorted(live),'source_alpha_zero':True,
            'source_reject_zero_core_ids':sorted(forbidden),'extra_zero_core_ids':sorted(qs)}
    if extra_cases:
        extra={}
        for name,a,b in (('Rv',2,7),('Lw',3,8),('qt',4,9)):
            zero={i for i,t in enumerate(ten) if t[a]==t[b]}
            current=set(range(2461))-forbidden-zero
            start=sorted(current);steps=[]
            while True:
                covered=set()
                for col in columns:
                    if all(rowids[h] in current for h,mult in col):covered.update(h for h,mult in col)
                missing={}
                for h,i in enumerate(rowids):
                    if i in current and h not in covered:missing.setdefault(i,h)
                if not missing:break
                steps.append([[i,missing[i]] for i in sorted(missing)])
                current.difference_update(missing)
            assert not current&alpha
            extra[name]={'extra_edge':name,'extra_zero_core_ids':sorted(zero),'initial':start,'rounds':steps,'live':sorted(current),'source_alpha_zero':True}
        result['additional_chords']=extra
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path);ap.add_argument('--additional-chords',action='store_true');args=ap.parse_args()
    if args.certificate is None:args.certificate=HERE/('closure-review-v2.json' if args.additional_chords else 'closure-review.json')
    result=compute(args.additional_chords)
    if args.build:
        with args.certificate.open('x') as f:json.dump(result,f,separators=(',',':'));f.write('\n')
    assert json.loads(args.certificate.read_text())==result
    certificate=HERE.parent/'A/certificate.json'
    if certificate.exists():
        other=json.loads(certificate.read_text())['c_degree4_exclusion']
        for key in ('literal_rows','H_rows','orbit_columns','columns_sha256','initial','rounds','live','source_alpha_zero','source_reject_zero_core_ids','extra_zero_core_ids'):
            assert result[key]==other[key],key
        if args.additional_chords:
            more=json.loads((HERE.parent/'A/chord-closures.json').read_text())
            assert set(more)==set(result['additional_chords'])
            for name,case in result['additional_chords'].items():
                for key in case:assert case[key]==more[name][key],(name,key)
    print(json.dumps({'status':'PASS','columns':result['orbit_columns'],'columns_sha256':result['columns_sha256'],
                      'initial_live':len(result['initial']),'removed_per_round':[len(r) for r in result['rounds']],
                      'final_live':len(result['live']),'source_alpha_zero':True,
                      'A_certificate_compared':certificate.exists(),'additional_chords':{name:{'removed':[len(r) for r in c['rounds']],'live':len(c['live']),'source_alpha_zero':True} for name,c in result.get('additional_chords',{}).items()}},sort_keys=True))

if __name__=='__main__':main()
