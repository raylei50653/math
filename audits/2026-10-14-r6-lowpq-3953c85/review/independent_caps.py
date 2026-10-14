#!/usr/bin/env python3
"""Independent direct cap check against the published r6 transfer table."""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'r6' / 'certificate.json'
PINS = 'z s v w t q ell m'.split()
EDGES = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(5,6),(6,7),(7,0)]
TABLE = {
    'ABABC': ('BC','CB'),
    'ABACB': ('BC','CB','CD','DC'),
    'ABACD': ('BC','BD','CB','CD','DB','DC'),
    'ABCAB': ('BC','CB','CD','DC'),
    'ABCAC': ('BC','CB'),
    'ABCAD': ('BC','BD','CB','CD','DB','DC'),
    'ABCBC': (), 'ABCBD': (), 'ABCDB': ('CD','DC'), 'ABCDC': (),
}

def norm(xs):
    seen=[]
    result=''
    for x in xs:
        if x not in seen:
            seen.append(x)
        result += chr(65+seen.index(x))
    return result

def compute():
    all_rows={}
    proper=0
    for f in itertools.product(range(4),repeat=8):
        if any(f[a]==f[b] for a,b in EDGES):
            continue
        proper += 1
        word=norm(f)
        if word != ''.join(chr(65+x) for x in f):
            continue
        pcolors=set(range(4))-set(f[i] for i in (0,5,6,7))
        rcolors=set(range(4))-set(f[i] for i in (1,2,3,4))
        allowed=all(chr(65+p)+chr(65+f[5]) in TABLE[word[:5]]
                    for p in pcolors)
        caps=[]
        for r,p,x,y in itertools.product(range(4),repeat=4):
            if r not in rcolors or p not in pcolors:
                continue
            if x in (f[0],f[1],r,y) or y in (f[0],r,f[4],x):
                continue
            caps.append([r,p,x,y])
        all_rows[word]={'allowed':allowed,'caps':caps}
    original=json.loads(SOURCE.read_text())
    assert set(all_rows)==set(original['rows'])
    for word,row in all_rows.items():
        assert row['allowed']==original['rows'][word]['necessary_row'],word
        assert row['caps']==original['rows'][word]['full_rpxy_lifts'],word
    slices={}
    specs={'sw_zell':((1,3),(0,6)),'vt_zell':((2,4),(0,6)),
           'zvell':((0,2),(0,6)),'zwell':((0,3),(0,6))}
    for name,equalities in specs.items():
        rows=[word for word,row in all_rows.items() if row['allowed']
              and all(word[a]==word[b] for a,b in equalities)]
        assert rows==original['quotient_slices'][name]['necessary_rows'],name
        slices[name]={'count':len(rows),'rows':rows}
    return {'status':'PASS','proper_labelled_rows':proper,
            'canonical_rows':len(all_rows),
            'necessary_rows':sum(row['allowed'] for row in all_rows.values()),
            'quotient_slices':slices,
            'scope':'Independent transfer-table membership and every direct cap lift; no source realization.'}

if __name__=='__main__':
    print(json.dumps(compute(),indent=2))
