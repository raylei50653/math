#!/usr/bin/env python3
"""All fibres of candidates rejected only after retaining the interior p,q pins."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import search

def independent(adj,word):
    # Independent full recursion, recomputing available colors from actual
    # colored neighbors. No domain bit sets or production solver imports.
    colors=list(map(int,word))+[-1]*(len(adj)-5);answers=[]
    if any(colors[u]==colors[v]>=0 for u in range(5) for v in adj[u]):return []
    def visit(left):
        if not left:
            answers.append(''.join(map(str,colors)));return
        choices={v:set(range(4))-{colors[w] for w in adj[v]} for v in left}
        v=min(left,key=lambda u:(len(choices[u]),u))
        for c in choices[v]:
            colors[v]=c;visit(left-{v})
        colors[v]=-1
    visit(set(range(5,len(adj))))
    return sorted(answers)

def main():
    p=argparse.ArgumentParser();p.add_argument('n',type=int);a=p.parse_args();h=search.HERE;search.seal()
    d=h/'runs'/f'n{a.n}';s=json.loads((d/'SUMMARY.json').read_text());records=[]
    for i in s['parts_completed']:
        prefix=d/f'{i:03d}';receipt=json.loads(Path(str(prefix)+'.receipt.json').read_text())
        if not receipt['search']['counts'].get('forbidden_joint'):continue
        with search.open_read(str(prefix)+'.input.jsonl.gz') as inp,search.open_read(str(prefix)+'.certificate.jsonl.gz') as cert:
            for left,right in zip(inp,cert,strict=True):
                source=json.loads(left);c=json.loads(right)
                for result in c['results']:
                    if result['outcome']!='forbidden_joint':continue
                    f=result['frame'];order,adj=search.make_u(source['rotation'],f);fibres={};joint=Counter();mask=0
                    for j,w in enumerate(search.WORDS):
                        lifts=sorted(search.solve(adj,list(map(int,w)),True))
                        assert lifts==independent(adj,w), 'independent complete-fibre disagreement'
                        assert all(search.proper(adj,v) for v in lifts)
                        fibres[w]=lifts;joint.update(v[:7] for v in lifts)
                        if lifts:mask|=1<<j
                    assert mask&~319==0
                    records.append({'part':i,'sphere':source['sphere'],'rotation':source['rotation'],'frame':f,
                                    'u_original_order':order,'u_edges':[[i,j] for i,ns in enumerate(adj) for j in sorted(ns) if i<j],
                                    'outer_mask':mask,'complete_fibres':fibres,'joint_counts':dict(sorted(joint.items())),
                                    'rejection':result,'degrees_B_in_G':[len(source['rotation'][v])-1 for v in f['B']],
                                    'degrees_apices_in_G':[len(source['rotation'][v]) for v in f['apices']]})
    assert len(records)==s['search_counts'].get('forbidden_joint',0)
    out=h/'validation'/f'n{a.n}-near-misses.json.gz'
    with gzip.open(out,'xt') as stream:json.dump({'n':a.n,'records':records},stream,separators=(',',':'));stream.write('\n')
    summary={'n':a.n,'frames':len(records),'spheres':len({(r['part'],r['sphere']) for r in records}),
             'masks':dict(Counter(r['outer_mask'] for r in records)),
             'full_lifts':sum(len(lifts) for r in records for lifts in r['complete_fibres'].values()),
             'details':[{'part':r['part'],'sphere':r['sphere'],'frame':r['frame'],'mask':r['outer_mask'],
                         'fibre_counts':{w:len(v) for w,v in r['complete_fibres'].items()},
                         'violating_joint_row':r['rejection']['lift'][:7],
                         'degrees_B':r['degrees_B_in_G'],'degrees_apices':r['degrees_apices_in_G']} for r in records]}
    (h/'validation'/f'n{a.n}-near-misses.summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
