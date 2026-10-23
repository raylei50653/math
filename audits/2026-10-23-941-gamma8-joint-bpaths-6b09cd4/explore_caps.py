#!/usr/bin/env python3
"""Reconstruct the exact eight-interior-point K6 caps from complete source stars."""
import json
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'
BOUNDARY=['U','p_d','d','zeta','x','p_x']
INNER=['r','T','s','tau','m','n','u','v']


def caps():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    cellcert=prior['complete_predecessor_certificate']['complete_predecessor_certificate']
    for _ in range(3):cellcert=cellcert['complete_predecessor_certificate']
    cells={r['id']:r for r in cellcert['candidates']}
    out={}
    for row in prior['star_restrictions']:
        cell=cells[row['cell']]
        links=dict(row['full_links'],m=['r','T','n','u','v'],T=['r','tau','s','n','m'])
        la={w:set() for w in cellcert['original_colors'] if w!='tau'}
        for face in cell['faces']:
            if 'tau' in face:
                a,b=[z for z in face if z!='tau'];la[a].add(b);la[b].add(a)
        tl=['r'];prev=None
        while True:
            nxt=next(z for z in sorted(la[tl[-1]]) if z!=prev)
            if nxt==tl[0]:break
            prev=tl[-1];tl.append(nxt)
        links['tau']=tl
        faces={tuple(sorted([z,a,b])) for z in INNER for a,b in zip(links[z],links[z][1:]+links[z][:1])}
        edges={tuple(sorted((a,b))) for face in faces for a,b in combinations(face,2)}
        key=tuple(sorted(edges))
        if key not in out:out[key]=dict(boundary=BOUNDARY,inner=INNER,edges=[list(e) for e in sorted(edges)],faces=[list(f) for f in sorted(faces)],source_rows=[])
        out[key]['source_rows'].append(dict(cell=row['cell'],family=row['family'],nx=row['n_x_edge']))
    return list(out.values())


def words(n=6):
    out=[]
    def rec(v):
        if len(v)==n:
            if v[-1]!=v[0]:out.append(v)
            return
        for c in range(max(v)+2):
            if c<4 and c!=v[-1]:rec(v+[c])
    rec([0]);return out


def lifts(cap,word):
    adj={v:set() for v in cap['boundary']+cap['inner']}
    for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
    colors=dict(zip(cap['boundary'],word));out=[]
    def rec():
        if len(colors)==len(adj):out.append([colors[v] for v in cap['inner']]);return
        pools={v:[c for c in range(4) if c not in {colors[w] for w in adj[v] if w in colors}] for v in adj if v not in colors}
        v=min(pools,key=lambda v:(len(pools[v]),-len(adj[v]),v))
        for c in pools[v]:colors[v]=c;rec();del colors[v]
    rec();return out


def main():
    data=caps();ws=words()
    for i,cap in enumerate(data):
        cap['id']=i
        cap['relations']=[dict(word=w,full_lifts=lifts(cap,w)) for w in ws]
        cap['statistics']=dict(vertices=14,edges=len(cap['edges']),faces=len(cap['faces']),nonempty=sum(bool(r['full_lifts']) for r in cap['relations']),total_lifts=sum(len(r['full_lifts']) for r in cap['relations']))
    (HERE/'EXACT_CAPS.json').write_text(json.dumps(dict(boundary=BOUNDARY,inner=INNER,proper_S4_words=ws,caps=data),sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(caps=len(data),statistics=[r['statistics'] for r in data]),sort_keys=True))


if __name__=='__main__':main()
