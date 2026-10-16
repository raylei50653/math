"""Direct local all-lift check for the two-face quotient, without tables."""
from itertools import product
import json

pins=('z','s','r','t','q','ell','m')
d_edges=(('z','s'),('s','r'),('r','t'),('t','z'),
         ('z','q'),('q','ell'),('ell','m'),('m','z'))
cap_edges=(('x','z'),('x','s'),('x','r'),('x','y'),
           ('y','z'),('y','r'),('y','t'),
           ('p','z'),('p','q'),('p','ell'),('p','m'))

rows=[]
survivors=[]
for colors in product(range(4),repeat=len(pins)):
    f=dict(zip(pins,colors))
    if f['z']!=f['r'] or f['q']!=f['m']: continue
    if any(f[a]==f[b] for a,b in d_edges): continue
    lifts=[]
    for cs in product(range(4),repeat=3):
        g=f | dict(zip(('x','y','p'),cs))
        if any(g[a]==g[b] for a,b in cap_edges): continue
        lifts.append({'xyp':cs,'target_palette_inequality':
                      {g['x'],g['y']}!={g['p'],g['q']}})
    assert lifts
    survives=all(not lift['target_palette_inequality'] for lift in lifts)
    expected=f['s']==f['t']==f['ell'] and len({f['z'],f['s'],f['q']})==3
    assert survives==expected
    row={'pins':colors,'lifts':lifts,'survives_universal_failure':survives}
    rows.append(row)
    if survives: survivors.append(colors)

out={'scope':'all complete local lifts for z=r,q=m in D; geometry is paper',
     'pins':pins,'d_edges':d_edges,'cap_edges':cap_edges,
     'proper_pin_rows':len(rows),
     'all_restoration_lifts':sum(len(r['lifts']) for r in rows),
     'surviving_rows':survivors,
     'survivor_rule':'z=r; q=m; s=t=ell; these three color classes are distinct',
     'rows':rows}
print(json.dumps(out,indent=2))
