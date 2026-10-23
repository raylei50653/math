#!/usr/bin/env python3
"""Independent original-D-first H* projection and full old-lift gates.

Finite relations only. The paper supplies the two actual cofacial identifications
and global minimum-source hypothesis; this script does not realize that source.
"""
from itertools import product
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
D = ('a','n','R','L','q','c','s','v','w','t')
E = ('a','n','R','L','q','c','x','y')
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
FACES = (('x','y','r'),('y','t','r'),('t','w','r'),('w','v','r'),
         ('v','s','r'),('s','x','r'),('x','s','c'),('y','a','t'))
CAP = {tuple(sorted((a,b))) for face in FACES for a,b in zip(face,face[1:]+face[:1])}


def canonical(word):
    names = {}
    return tuple(names.setdefault(c,len(names)) for c in word)


def words(n, prefix=(0,)):
    if len(prefix)==n:
        if prefix[-1]!=prefix[0]:
            yield prefix
        return
    for c in range(min(4,max(prefix)+2)):
        if c!=prefix[-1]:
            yield from words(n,prefix+(c,))


def full_cap(colours):
    result=[]
    for r,x,y in product(range(4),repeat=3):
        c={**colours,'r':r,'x':x,'y':y}
        if all(c[a]!=c[b] for a,b in CAP):
            result.append((r,x,y,tuple(c[v] for v in E)))
    return result


def main():
    authority=REPO/'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
    src=json.loads(authority.read_text());ewords=list(words(8));eindex={t:i for i,t in enumerate(ewords)}
    if ewords!=[tuple(t) for t in src['tuples']]:
        raise ValueError('literal E row order mismatch')
    live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
    forbidden=set(range(274))-live
    dwords=list(words(10));zero=set();raw=[[] for _ in ROWS];caps={}
    for j,d in enumerate(dwords):
        colours=dict(zip(D,d));lifts=full_cap(colours);caps[j]=lifts
        if any(eindex[canonical(e)] in forbidden for r,x,y,e in lifts):
            zero.add(j)
        if d[0]==d[2]==d[5]:
            row=''.join(map(str,canonical((d[0],)+d[6:])))
            raw[ROWS.index(row)].append(j)
    surviving=[[j for j in ids if j not in zero] for ids in raw]
    mask=sum(1<<i for i,ids in enumerate(surviving) if ids)
    if len(dwords)!=2461 or len(zero)!=552 or mask!=319:
        raise ValueError('wrong full H* necessary projection')
    catalogue=json.loads((REPO/'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json').read_text())
    accepted=sorted(int(m) for m in catalogue['cells'] if int(m)&~mask==0)
    if accepted!=[271,314,319]:
        raise ValueError('wrong complete catalogue restriction')
    mandatory=[i for i in range(10) if all(m>>i&1 for m in accepted)]
    if mandatory!=[1,3,8]:
        raise ValueError('wrong simultaneously required complete rows')
    for i in (1,3):
        if not surviving[i] or any(caps[j] for j in raw[i]):
            raise ValueError('new positive family must have entirely empty rxy lift')
    gates=[]
    for n,L,q in product(range(4),repeat=3):
        c={'a':0,'c':0,'R':0,'n':n,'L':L,'q':q}
        if any(c[a]==c[b] for a,b in [('a','n'),('n','R'),('R','L'),('L','q'),('q','c')]):
            continue
        lifts=[]
        for b,p,h in product(range(4),repeat=3):
            cc={**c,'b':b,'p':p,'h':h}
            edges=[('b',v) for v in ('a','c','p','q')]+[('p',v) for v in ('a','q','h','n')]+[('h',v) for v in ('q','L','R','n')]
            if all(cc[a]!=cc[b] for a,b in edges):
                lifts.append([b,p,h])
        if bool(lifts)!=(n==q):
            raise ValueError('full bph gate is not n=q')
        if lifts:
            missing=next(iter(set(range(4))-{0,n,L}))
            if lifts!=[[missing,L,missing]]:
                raise ValueError('missing exact unique bph lift')
        gates.append({'nLq':[n,L,q],'all_bph_lifts':lifts})
    print(json.dumps({'status':'PASS','D_rows':len(dwords),'original_D_zero_ids':sorted(zero),
                      'raw_Hstar_D_groups':raw,'surviving_Hstar_D_groups':surviving,
                      'necessary_Hstar_support_upper_bound':mask,'catalogue_masks':accepted,
                      'forced_positive_rows':[ROWS[i] for i in mandatory],
                      'first_two_positive_groups_have_no_rxy_lifts':True,
                      'full_bph_gates':gates,'source_status':'not triggered',
                      'smaller_bad_constructed':False},sort_keys=True))


if __name__=='__main__':
    main()
