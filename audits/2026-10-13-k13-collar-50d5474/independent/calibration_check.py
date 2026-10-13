#!/usr/bin/env python3
"""Independent full/empty calibration fibres and whole-graph D5 colour lifts."""
import argparse
from copy import deepcopy
import json
from check import AUDIT,HERE,WORDS,colourings,d5_relation,norm,encode,sha


def check_case(case):
    adj={v:[] for v in range(case['n'])}
    for u,v in case['edges']:adj[u].append(v);adj[v].append(u)
    rows=[]
    assert len(case['rows'])==10,'missing row'
    for word,row in zip(WORDS,case['rows']):
        lifts,_=colourings(adj,list(range(5)),word)
        assert row['pattern']==word,'wrong fixed word'
        assert row['lifts']==lifts,'wrong full or empty fibre'
        assert row['count']==len(lifts),'wrong fibre count'
        rows.append({'count':len(lifts),'lifts':lifts})
    mask=sum(1<<i for i,r in enumerate(rows) if r['count'])
    assert mask==case['mask'],'wrong complete relation'
    frames=d5_relation(list(range(5)),rows)
    for frame in frames:
        direct=[colourings(adj,frame['B'],word)[0] for word in WORDS]
        assert frame['counts']==list(map(len,direct)),'incorrect D5 row counts'
        transported=[[] for _ in WORDS]
        for oldword,row in zip(WORDS,rows):
            ordered=[oldword[v] for v in frame['B']]
            names={}
            for color in ordered:names.setdefault(color,str(len(names)))
            for color in '0123':names.setdefault(color,str(len(names)))
            newword=''.join(names[c] for c in ordered)
            dest=WORDS.index(newword)
            transported[dest].extend(''.join(names[c] for c in lift) for lift in row['lifts'])
        assert [sorted(x) for x in transported]==direct,'incorrect whole-graph D5 full-lift colour transport'
    return {'id':case['id'],'mask':mask,'accepted_rows':sum(r['count']>0 for r in rows),'rejected_rows':sum(r['count']==0 for r in rows),'full_lifts':sum(r['count'] for r in rows),'D5_masks':[f['mask'] for f in frames]}

def run():
    path=AUDIT/'calibration.json';cases=json.loads(path.read_text())
    result=[check_case(case) for case in cases]
    assert sum(r['rejected_rows'] for r in result)>0,'empty fibres not triggered'
    damaged=deepcopy(next(c for c in cases if any(r['count']==0 for r in c['rows'])))
    row=next(r for r in damaged['rows'] if r['count']==0);row['count']=1;row['lifts']=[row['pattern']+'0'*(damaged['n']-5)]
    try:check_case(damaged)
    except AssertionError as err:negative={'control':'false accepted lift in empty fibre','result':'rejected','reason':str(err)}
    else:raise AssertionError('empty-fibre corruption survived')
    return {'status':'pass','calibration_sha256':sha(path),'cases':result,'D5_full_lift_comparisons':10*10*len(cases),'negative':negative}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();result=run()
    path=HERE/'calibration_review.json';data=encode(result)+b'\n'
    if args.check:assert path.read_bytes()==data,'calibration review differs'
    else:
        with path.open('xb') as f:f.write(data)
    print(json.dumps(result,indent=2,sort_keys=True))
