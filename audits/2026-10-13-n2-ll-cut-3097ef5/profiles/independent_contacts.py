#!/usr/bin/env python3
"""Second implementation: enumerate owner-group attachment multisets directly.

No import from domain.py and no reuse of its dynamic programming. The output
lists ALL finite contact-interface members of each retained catalogue entry.
These are necessary contact interfaces, never complete source graphs.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent


def members(d):
    sup=d['support'];kr,ks=d['k'];wr=set(d['W_r']);ws=set(d['W_s'])
    a=[()]+[(h,) for h in sup]+[tuple(x) for x in combinations(sup,2) if (x[0]-x[1])%5 in (1,4)]
    ra=[x for x in a if set(x)<=wr];sa=[x for x in a if set(x)<=ws]
    both=[x for x in a if len(x)<=1 and set(x)<=wr&ws]
    out=[]
    for n in range(1,min(kr,ks)+1) if d['shared'] else (0,):
        for rr,ss,bb in product(combinations_with_replacement(ra,kr-n),combinations_with_replacement(sa,ks-n),combinations_with_replacement(both,n)):
            if set(h for aa in rr+bb for h in aa)!=wr or set(h for aa in ss+bb for h in aa)!=ws:continue
            rows=[(1,aa) for aa in rr]+[(2,aa) for aa in ss]+[(3,aa) for aa in bb]
            if sum(4-(2 if owner==3 else 1)-len(aa)<=2 for owner,aa in rows)<2:continue
            pairids=[next(e for e in range(5) if set(aa)=={e,(e+1)%5}) for _,aa in rows if len(aa)==2]
            if len(set(pairids))!=len(pairids):continue
            rows.sort(key=lambda row:(row[0],len(row[1]),row[1]))
            out.append({'pair_mask':sum(1<<e for e in pairids),'contacts':[{'slot':j,'owners':[v for bit,v in ((1,'r'),(2,'s')) if owner&bit],
                'B':list(aa),'degree_in_C':4-(2 if owner==3 else 1)-len(aa)} for j,(owner,aa) in enumerate(rows)]})
    out.sort(key=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')))
    assert len({json.dumps(x,sort_keys=True) for x in out})==len(out)
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    source=(HERE/'profiles.json').read_bytes();p=json.loads(source);catalog={};count=0
    for cid,f in sorted(p['contact_catalog'].items()):
        mm=members(f['definition']);assert len(mm)==f['count'],cid
        expected={g['pair_mask']:g['count'] for g in f['by_pair_mask']}
        assert dict(Counter(m['pair_mask'] for m in mm))==expected,cid
        for group in f['by_pair_mask']:
            assert {'pair_mask':group['pair_mask'],'contacts':group['example']} in mm,cid
        catalog[cid]=mm;count+=len(mm)
    payload={'profile_sha256':hashlib.sha256(source).hexdigest(),'status':'necessary_contact_interfaces_not_source_graphs',
             'catalogue_count':len(catalog),'member_count':count,'members':catalog}
    encoded=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n';path=HERE/'contact_members.json'
    if args.check:assert path.read_text()==encoded,'contact member artifact mismatch'
    else:
        with path.open('x') as stream:stream.write(encoded)
    print(json.dumps({'catalogues':len(catalog),'members':count,'sha256':hashlib.sha256(encoded.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
