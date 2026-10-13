#!/usr/bin/env python3
"""Independent rank-four domain, neighbour construction, rotation and full DFS.
No import from controls. Polygon triangulations are obtained by a noncrossing
chord test; all words are filtered by original degrees and exact ring totals.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from kernels import BETAS, TAUS, canonical_cycle, rotation_faces, verify_rows

ROOT=Path(__file__).resolve().parent.parent
BASE='acd2b1beea6c909edade565a00eeeeac05d2b3a7'
INC={'O':(0,0),'B':(1,0),'U':(0,1),'D':(1,1)}


def key(p):
    return json.dumps(p,sort_keys=True,separators=(',',':'))


def polygon_specs():
    diagonals=[(i,j) for i in range(6) for j in range(i+1,6)
               if j-i not in (1,5)]
    boundary={(i,i+1) for i in range(5)}|{(0,5)}
    specs={'D':(4,2,[(1,3)])}
    retained=[]
    for ds in itertools.combinations(diagonals,3):
        if any(a<c<b<d or c<a<d<b for (a,b),(c,d) in itertools.combinations(ds,2)):
            continue
        edges=boundary|set(ds)
        degree=[sum(v in e for e in edges) for v in range(6)]
        ears=[v for v in range(6) if degree[v]==2]
        if len(ears)==2 and ears[0]==0:
            retained.append((ds,ears[1]))
    assert len(retained)==4
    for i,(ds,ear) in enumerate(sorted(retained)):
        specs['H'+str(i)]=(6,ear,list(ds))
    return specs

SPECS=polygon_specs()


def block_edges(atom):
    n,end,ds=SPECS[atom]
    return sorted({tuple(sorted((i,(i+1)%n))) for i in range(n)}|set(ds))


def size(atoms):
    return len(atoms)+1+sum(SPECS[a][0]-2 for a in atoms if a!='E')


def skeletons(kind,maximum):
    # Integer compositions enumerated in total-size order, unlike source traversal.
    if kind=='P':
        for n in range(2,maximum+1): yield ['E']*(n-1)
    elif kind in ('H','D'):
        for n in range(6 if kind=='H' else 4,maximum+1):
            tails=n-(6 if kind=='H' else 4)
            for left in range(tails+1):
                for b in ([f'H{i}' for i in range(4)] if kind=='H' else ['D']):
                    yield ['E']*left+[b]+['E']*(tails-left)
    else:
        assert kind=='DD'
        for n in range(7,maximum+1):
            extra=n-7
            for left in range(extra+1):
                for bridge in range(extra-left+1):
                    yield ['E']*left+['D']+['E']*bridge+['D']+['E']*(extra-left-bridge)


def decorated(atoms):
    degrees=[0]*(len(atoms)+1)
    bit_choices=[]
    for i,a in enumerate(atoms):
        contribution=1 if a=='E' else 2
        degrees[i]+=contribution; degrees[i+1]+=contribution
        if a!='E':
            n,end,_=SPECS[a]; es=block_edges(a)
            sides=(list(range(1,end)),list(range(n-1,end,-1)))
            options=[]
            for side in sides:
                choices=[[str(b) for b in range(2) if sum(v in e for e in es)+1+b>=5] for v in side]
                options.append([''.join(x) for x in itertools.product(*choices)])
            bit_choices.append(list(itertools.product(*options)))
    letters=[[s for s in 'OBUD' if degrees[i]+2+sum(INC[s])>=5] for i in range(len(degrees))]
    for word_tuple in itertools.product(*letters):
        word=''.join(word_tuple)
        wb=sum(INC[s][0] for s in word); wu=sum(INC[s][1] for s in word)
        if max(wb,wu)>5: continue
        for bits in itertools.product(*bit_choices):
            b=wb+sum(s[0].count('1') for s in bits)
            u=wu+sum(s[1].count('1') for s in bits)
            if max(b,u)<=5:
                yield {'atoms':atoms,'word':word,'steps':list(map(list,bits))}, b,u


def binary_words(b,u):
    length=b+u
    for positions in itertools.combinations(range(length),b):
        ps=set(positions)
        yield ''.join('B' if i in ps else 'U' for i in range(length))


def parameters():
    for c in (1,2):
        families=[('H',),('DD',)] if c==1 else [('H','P'),('DD','P'),('D','D')]
        for family in families:
            all_skeletons=[list(skeletons(k,14-2*c)) for k in family]
            for atoms in itertools.product(*all_skeletons):
                r=sum(map(size,atoms))
                if not 8<=r<=14-2*c: continue
                decorations=[list(decorated(x)) for x in atoms]
                for ds in itertools.product(*decorations):
                    b=5-sum(d[1] for d in ds); u=5-sum(d[2] for d in ds)
                    if min(b,u)<0 or b+u>14-2*c-r: continue
                    for terminal in binary_words(b,u):
                        splits=[(terminal,)] if c==1 else [(terminal[:s],terminal[s:]) for s in range(len(terminal)+1)]
                        for gaps in splits:
                            yield {'components':[d[0] for d in ds],'gaps':list(gaps),'c':c,'r':r}


def graph_from_neighbours(param):
    edges=set()
    def edge(a,b):
        assert a!=b
        edges.add(tuple(sorted((a,b))))
    for off in (0,5):
        for i in range(5): edge(off+i,off+(i+1)%5)
    b=u=0; label=10
    components=[]
    def cross(): edge(b%5,5+u%5)
    for comp,gap in zip(param['components'],param['gaps']):
        atoms=comp['atoms']; word=comp['word']; steps=iter(comp['steps'])
        xs=list(range(label,label+len(atoms)+1)); label+=len(xs)
        verts=xs[:]
        assert len(word)==len(xs)
        cross()
        for i,x in enumerate(xs):
            db,du=INC[word[i]]
            for y in {b%5,(b+db)%5,5+u%5,5+(u+du)%5}: edge(x,y)
            b+=db;u+=du
            if i==len(atoms): continue
            atom=atoms[i]; y=xs[i+1]
            if atom=='E': edge(x,y);continue
            n,end,_=SPECS[atom]
            mapping={0:x,end:y}
            for z in range(n):
                if z not in mapping: mapping[z]=label;verts.append(label);label+=1
            for z,w in block_edges(atom): edge(mapping[z],mapping[w])
            bbits,ubits=next(steps)
            assert len(bbits)==end-1 and len(ubits)==n-end-1
            for z,bit in zip(range(1,end),bbits):
                delta=int(bit);edge(mapping[z],b%5);edge(mapping[z],(b+delta)%5);b+=delta
            for z,bit in zip(range(n-1,end,-1),ubits):
                delta=int(bit);edge(mapping[z],5+u%5);edge(mapping[z],5+(u+delta)%5);u+=delta
        assert next(steps,None) is None
        components.append(sorted(verts));cross()
        for letter in gap:
            if letter=='B': b+=1
            else: assert letter=='U';u+=1
            cross()
    assert b==u==5 and label==param['r']+10
    assert len(components)==param['c']
    return label,sorted(edges),components


def geometry(record,param,n,edges,components):
    assert record['key']==key(param) and record['parameters']==param
    assert record['vertices']==list(range(n)) and record['private']==list(range(10,n))
    assert record['B']==list(range(5)) and record['U']==list(range(5,10))
    assert record['edges']==list(map(list,edges)), 'original edges mismatch'
    assert sorted(map(sorted,record['components']))==sorted(components)
    fs=record['faces']; assert fs[0]==[0,4,3,2,1] and fs[-1]==list(range(5,10))
    assert all(len(f)==3 for f in fs[1:-1])
    rotation_faces(n,edges,fs,record['rotation'])
    assert record['ownership']=={'outer_face':0,'empty_U_face':len(fs)-1,'centre_after_restoration':n,'pin_map':list(range(10))}
    we=sorted(edges+[(u,n) for u in range(5,10)])
    assert record['wheel_edges']==list(map(list,we))
    rotation_faces(n+1,we,record['wheel_faces'],record['wheel_rotation'])
    wanted=Counter(map(canonical_cycle,fs[:-1]));wanted.update(canonical_cycle([5+i,5+(i+1)%5,n]) for i in range(5))
    assert Counter(map(canonical_cycle,record['wheel_faces']))==wanted
    dg=[sum(x in e for e in we) for x in range(n+1)]
    pe=[e for e in edges if min(e)>=10]; df=[sum(x in e for e in pe) for x in range(10,n)]
    assert record['degree_G']==dg and record['degree_F']==df
    assert record['U_degree_at_least_5']==(min(dg[5:10])>=5)
    assert record['B_degree_at_least_4']==(min(dg[:5])>=4)
    assert all(dg[x]>=5 for x in range(10,n))
    actual=[]; unseen=set(range(10,n))
    while unseen:
        reached=set();todo=[min(unseen)]
        while todo:
            x=todo.pop()
            if x in reached:continue
            reached.add(x);todo.extend(y if x==z else z for z,y in pe if x in (z,y))
        actual.append(sorted(reached));unseen-=reached
    assert sorted(actual)==sorted(components)
    c=len(actual);r=n-10
    h=sum(all(x>=10 for x in f) for f in fs[1:-1]);a=sum(all(x<10 for x in f) for f in fs[1:-1])
    m=sum(any(x<5 for x in f) and any(5<=x<10 for x in f) and any(x>=10 for x in f) for f in fs[1:-1])
    p=sum(x<5<=y<10 for x,y in edges)
    assert record['counts']=={'c':c,'r':r,'t_P':h,'a':a,'p':p,'M':m,'rho':len(pe)-r+c}
    assert len(pe)-r+c==h==4 and m==2*c and p==a+c
    assert sum(dg[10:n])==4*r+14-2*c-a and 8<=r<=14-2*c-a
    for x in range(10,n):
        for off in (0,5):
            ns=[y-off for y in range(off,off+5) if tuple(sorted((x,y))) in edges]
            assert len(ns)<=2
            if len(ns)==2: assert (ns[1]-ns[0])%5 in (1,4)


def catalogue():
    meta=json.loads((ROOT/'CATALOGUE_INPUT.json').read_text());assert meta['base']==BASE
    raw=(ROOT/'frozen'/meta['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==meta['sha256'] and len(raw)==meta['bytes']
    cells=json.loads(raw);assert cells['pattern_order']==list(map(list,BETAS))
    masks=set(map(int,cells['cells']));assert len(masks)==132
    # Complete ordered boundary membership is invariant under whole-graph D5.
    for s in range(5):
        for direction in (-1,1):
            permutation=[]
            for beta in BETAS:
                row=[beta[(s+direction*i)%5] for i in range(5)]
                seen={};row=tuple(seen.setdefault(v,len(seen)) for v in row)
                permutation.append(BETAS.index(row))
            for mask in masks:
                pulled=sum(((mask>>permutation[i])&1)<<i for i in range(10))
                assert pulled in masks
    return masks


def verify_coverage(expected,observed):
    assert observed==expected, 'incomplete template coverage'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--list',action='store_true');ap.add_argument('--certificate',type=Path,default=ROOT/'controls/certificate.jsonl.gz');ap.add_argument('--limit',type=int);args=ap.parse_args()
    domain={}
    for p in parameters():
        k=key(p);assert k not in domain;domain[k]=p
    if args.list:
        counts=Counter((p['c'],p['r'],','.join(''.join(a for a in c['atoms'] if a!='E') for c in p['components'])) for p in domain.values())
        print(json.dumps({'templates':len(domain),'types':{str(k):v for k,v in sorted(counts.items())}},sort_keys=True));return
    masks=catalogue();seen=set();totals=Counter();sigmas=Counter()
    with gzip.open(args.certificate,'rt') as stream:
        header=json.loads(next(stream));assert header['type']=='header' and header['base']==BASE
        assert header['beta_order']==list(map(list,BETAS)) and header['tau_order']==list(map(list,TAUS))
        for line in stream:
            if args.limit is not None and len(seen)>=args.limit:break
            record=json.loads(line);identity=key(record['parameters'])
            assert identity in domain and identity not in seen
            param=domain[identity];n,edges,components=graph_from_neighbours(param)
            geometry(record,param,n,edges,components);totals.update(verify_rows(record,n,edges))
            assert record['Sigma'] in masks, 'outside frozen K132'
            assert record['Sigma_in_K132'] is True
            seen.add(identity);sigmas[record['Sigma']]+=1
            if len(seen)%100==0:print(json.dumps({'done':len(seen),'masks':dict(sigmas)}),flush=True)
    if args.limit is None:verify_coverage(set(domain),seen)
    print(json.dumps({'status':'PASS independent exact comparison','templates':len(seen),'Sigma_counts':dict(sigmas),**dict(totals),'catalogue_D5_closed':True,'minimal_source':'not triggered'},sort_keys=True))

if __name__=='__main__':main()
