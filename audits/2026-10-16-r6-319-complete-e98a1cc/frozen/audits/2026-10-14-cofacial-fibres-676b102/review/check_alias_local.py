"""Independent labelled all-lift check of the p=5,a=4 quotient obstruction.

This checks the finite restoration fact directly from edges, without reading
the R or H relation tables. The quotient topology remains a paper argument.
"""
from itertools import product
import json

pins=('z','s','r','t','ell','q')
d_edges=(('z','s'),('s','r'),('r','t'),('t','z'),
         ('z','q'),('q','ell'),('ell','t'))
cap_edges=(('x','z'),('x','s'),('x','r'),('x','y'),
           ('y','z'),('y','r'),('y','t'),
           ('p','z'),('p','q'),('p','ell'),('p','t'))

rows=[]
for colors in product(range(4),repeat=len(pins)):
    f=dict(zip(pins,colors))
    if f['z']!=f['r'] or f['q']!=f['t']: continue
    if any(f[a]==f[b] for a,b in d_edges): continue
    lifts=[]
    for cs in product(range(4),repeat=3):
        g=f | dict(zip(('x','y','p'),cs))
        if any(g[a]==g[b] for a,b in cap_edges): continue
        good={g['x'],g['y']}!={g['p'],g['q']}
        lifts.append({'xyp':cs,'target_palette_inequality':good})
    assert lifts and any(l['target_palette_inequality'] for l in lifts)
    rows.append({'pins':colors,'lifts':lifts})

out={'scope':'direct local extension for every labelled D row with z=r,q=t',
     'pins':pins,'d_edges':d_edges,'cap_edges':cap_edges,
     'proper_pin_rows':len(rows),
     'all_restoration_lifts':sum(len(r['lifts']) for r in rows),
     'target_lifts':sum(l['target_palette_inequality'] for r in rows for l in r['lifts']),
     'no_target_rows':0,'rows':rows}
print(json.dumps(out,indent=2))
