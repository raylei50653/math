#!/usr/bin/env python3
"""Finite necessary contact interfaces in one literal original C5 frame.

This does not generate source graphs. A profile carries three rows from ONE
spoke/contact interface. Contact-fibre members canonically name contact slots;
a source ledger retains the bijection to original vertices and all forgotten
edges, rotations, block roles and free coordinates.
"""
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse, hashlib, importlib.util, json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SPEC = importlib.util.spec_from_file_location('frozen_matrix', BASE / 'frozen/audits/2026-10-13-n2-double-long-joint/joint/matrix.py')
MATRIX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATRIX)
ROWS = {0: (0,1,2,1,2), 1: (0,1,2,0,2), 3: (0,1,0,2,1)}


def subsets(values):
    values=tuple(sorted(values))
    return [tuple(c) for n in range(len(values)+1) for c in combinations(values,n)]


def arc(start, length):
    vertices=tuple((start+j)%5 for j in range(length+1))
    return {'walk': list(vertices), 'edges': sorted((start+j)%5 for j in range(length)), 'support': sorted(vertices), 'interior': sorted(vertices[1:-1])}


def geometries():
    """Only simultaneous whole-source r/s and P/Q names may be exchanged."""
    result=[]
    for a in range(5):
        for b in range(5):
            for lq in (2,3):
                p,q=arc(a,2),arc(b,lq)
                if set(p['edges']) & set(q['edges']): continue
                if lq==2 and tuple(p['edges']) >= tuple(q['edges']): continue
                sites=sorted(set(range(5))-set(p['interior'])-set(q['interior']))
                for tr,ts in ((2,0),(1,1),(2,1)) if lq==2 else ((1,1),):
                    for r in combinations(sites,tr):
                        if tr==2 and ((r[0]-r[1])%5 not in (1,4)): continue
                        for s in combinations(sites,ts):
                            result.append({'P':p,'Q':q,'T_r':list(r),'T_s':list(s),'t':[tr,ts]})
    result.sort(key=lambda g: json.dumps(g,sort_keys=True))
    for n,g in enumerate(result): g['id']=f'g{n:03d}'
    return result


def closure(spokes):
    return tuple(h for h in range(5) if all(q[h] in {q[t] for t in spokes} for q in ROWS.values()))


def contact_types(support):
    """(owner bitmask, literal B neighbors). Empty attachments are retained."""
    aa=[a for a in subsets(support) if len(a)<=2 and (len(a)<2 or (a[0]-a[1])%5 in (1,4))]
    return tuple((owner,a) for owner in (1,2,3) for a in aa if len(a)+(2 if owner==3 else 1)<=3)


def boundary_edge_mask(a):
    if len(a)!=2:return 0
    return 1 << next(e for e in range(5) if {e,(e+1)%5}==set(a))


def expand_contact_slots(types,mults):
    slots=[]
    for (owner,a),mult in zip(types,mults):
        for _ in range(mult):
            slots.append({'slot':len(slots),'owners':[v for bit,v in ((1,'r'),(2,'s')) if owner&bit],
                          'B':list(a),'degree_in_C':4-(2 if owner==3 else 1)-len(a)})
    return slots


@lru_cache(None)
def contact_fibre(support, kr, ks, wr, ws, shared):
    """Finite exact contact multiset family, grouped by used B-edge pairs.

    Distinct actual contacts retain separate slots even for identical types.
    At least two contacts can be private leaf contacts (degree in C <= 2).
    Degree-in-H=2 boundary-edge attachments are injective. This constrains
    contacts only: hidden ordinary vertices remain in the source ledger.
    """
    types=tuple((o,a) for o,a in contact_types(support)
                if (not (o&1) or set(a)<=set(wr)) and (not(o&2) or set(a)<=set(ws))
                and (shared or o!=3))
    targetr=sum(1<<x for x in wr); targets=sum(1<<x for x in ws)
    @lru_cache(None)
    def rec(j,r,s,mr,ms,nleaf,nshared,pairs):
        if j==len(types):
            good=(r==kr and s==ks and mr==targetr and ms==targets and nleaf>=2
                  and (not shared or nshared>=1))
            return ((pairs,1,()),) if good else ()
        owner,a=types[j]; ar=int(bool(owner&1)); ass=int(bool(owner&2)); mask=sum(1<<h for h in a)
        pair=boundary_edge_mask(a);leaf=(4-ar-ass-len(a)<=2)
        upper=min((kr-r)//ar if ar else kr+ks,(ks-s)//ass if ass else kr+ks)
        if pair:upper=min(upper,0 if pairs&pair else 1)
        out={}
        for mult in range(upper+1):
            result=rec(j+1,r+mult*ar,s+mult*ass,mr|(mask if mult and ar else 0),ms|(mask if mult and ass else 0),
                    min(2,nleaf+(mult if leaf else 0)),min(1,nshared+(mult if owner==3 else 0)),pairs|(pair if mult else 0))
            for finalmask,count,suffix in result:
                if finalmask not in out:out[finalmask]=[0,(mult,)+suffix]
                out[finalmask][0]+=count
        return tuple((mask,count,first) for mask,(count,first) in sorted(out.items()))
    groups=rec(0,0,0,0,0,0,0,0)
    bymask=[{'pair_mask':mask,'count':count,'example':expand_contact_slots(types,mults)} for mask,count,mults in groups]
    return {'count':sum(g['count'] for g in bymask),'by_pair_mask':bymask,
            'definition':{'support':list(support),'k':[kr,ks],'W_r':list(wr),'W_s':list(ws),'shared':shared},
            'types':[[o,list(a)] for o,a in types]}


def iter_contact_fibre(definition):
    """Enumerate EVERY contact-slot member of the recorded finite fibre."""
    support=definition['support'];kr,ks=definition['k'];wr=set(definition['W_r']);ws=set(definition['W_s']);shared=definition['shared']
    types=tuple((o,a) for o,a in contact_types(support) if (not(o&1) or set(a)<=wr)
                and (not(o&2) or set(a)<=ws) and (shared or o!=3))
    def rec(j,r,s,mr,ms,leaf,has_shared,pairs,mults):
        if j==len(types):
            if r==kr and s==ks and mr==wr and ms==ws and leaf>=2 and (not shared or has_shared):
                yield {'pair_mask':pairs,'contacts':expand_contact_slots(types,mults)}
            return
        o,a=types[j];ar=int(bool(o&1));ass=int(bool(o&2));pair=boundary_edge_mask(a)
        upper=min((kr-r)//ar if ar else kr+ks,(ks-s)//ass if ass else kr+ks)
        if pair:upper=min(upper,0 if pairs&pair else 1)
        for mult in range(upper+1):
            yield from rec(j+1,r+mult*ar,s+mult*ass,mr|(set(a) if mult and ar else set()),ms|(set(a) if mult and ass else set()),
                leaf+(mult if 4-ar-ass-len(a)<=2 else 0),has_shared or (mult>0 and o==3),pairs|(pair if mult else 0),mults+(mult,))
    yield from rec(0,0,0,set(),set(),0,False,0,())


def piece_options(support, kr, ks, tr, ts):
    ar=set(support)&set(closure(tr)) if ks>=2 else set(support)
    ass=set(support)&set(closure(ts)) if kr>=2 else set(support)
    for wr,ws in product(subsets(ar),subsets(ass)):
        for shared in (False,True):
            if not shared and not (wr or ws): continue
            yield {'k':[kr,ks],'W_r':list(wr),'W_s':list(ws),'shared':shared}


def candidate_profiles():
    for g in geometries():
        for kr in range(1,5-g['t'][0]):
            for ks in range(1,5-g['t'][1]):
                opts=[list(piece_options(g[c]['support'],a,b,g['T_r'],g['T_s'])) for c,a,b in
                      [('P',kr,ks),('Q',5-g['t'][0]-kr,5-g['t'][1]-ks)]]
                for p,q in product(*opts):
                    yield {'geometry':g['id'],'P':dict(p),'Q':dict(q)}


def row_data(profile, geometry, row):
    q=ROWS[row]
    er=[x for x in range(4) if x not in {q[h] for h in geometry['T_r']}]
    es=[y for y in range(4) if y not in {q[h] for h in geometry['T_s']}]
    safe={}; sources={}
    for c in ('P','Q'):
        p=profile[c]; safe[c]=[]; sources[c]={}
        for x,y in product(er,es):
            reasons=[]
            for v,pin in (('r',x),('s',y)):
                for h in p['W_'+v]:
                    if q[h]==pin: reasons.append({'mechanism':'contact_boundary_slack','root':v,'boundary':h})
            if x==y and p['shared']: reasons.append({'mechanism':'shared_contact_slack'})
            if reasons:
                safe[c].append([x,y]); sources[c][f'{x},{y}']=reasons
    return {'row':row,'q':list(q),'rows':er,'columns':es,'S_P':safe['P'],'S_Q':safe['Q'],
            'fixed_sources':sources,'row_bounds':[profile['P']['k'][1]-1,profile['P']['k'][1]],
            'column_bounds':[profile['P']['k'][0]-1,profile['P']['k'][0]]}


@lru_cache(None)
def cached_matrix(rows,columns,kr,ks,sp,sq):
    return MATRIX.analyze(rows,columns,kr,ks,sp,sq)


def analyze_profile(profile, geometry):
    out=[]
    for i in ROWS:
        d=row_data(profile,geometry,i)
        result=cached_matrix(tuple(d['rows']),tuple(d['columns']),*profile['P']['k'],tuple(map(tuple,d['S_P'])),tuple(map(tuple,d['S_Q'])))
        out.append({**d,**result})
    return out


def generate():
    gs=geometries();gm={g['id']:g for g in gs}
    catalog={};profiles=[];stats={};cuts={};row_catalog={};digest=hashlib.sha256();contact_reject_digest=hashlib.sha256()
    for p in candidate_profiles():
        g=gm[p['geometry']]; results=analyze_profile(p,g)
        key=f"{len(g['P']['support'])}{len(g['Q']['support'])}-t{g['t'][0]}{g['t'][1]}"
        stat=stats.setdefault(key,{'raw_Z_candidates':0,'basic_cut':0,'contact_incompatible':0,'common_feasible':0,'full_contact_interfaces':0})
        stat['raw_Z_candidates']+=1
        if not all(r['feasible'] for r in results):
            stat['basic_cut']+=1
            chosen=next(r for r in results if not r['feasible'])
            kind='overlap' if chosen['common_safe_cells'] else chosen['violated_cut']['kind'] if chosen['violated_cut'] else 'unexplained'
            shape={'kind':kind,'row_bounds':chosen['row_bounds'],'column_bounds':chosen['column_bounds'],
                   'cut':chosen['violated_cut'],'overlap':chosen['common_safe_cells']}
            ck=json.dumps(shape,sort_keys=True,separators=(',',':'))
            cid='cut'+hashlib.sha256(ck.encode()).hexdigest()[:12]
            entry=cuts.setdefault(cid,{'count':0,'shape':shape,'example_profile':p,'example_row':chosen})
            entry['count']+=1
            digest.update((json.dumps(p,sort_keys=True,separators=(',',':'))+' '+cid+'\n').encode())
            continue
        fibres={c:contact_fibre(tuple(g[c]['support']),*p[c]['k'],tuple(p[c]['W_r']),tuple(p[c]['W_s']),p[c]['shared']) for c in ('P','Q')}
        compatible=[[a['pair_mask'],b['pair_mask'],a['count']*b['count']] for a in fibres['P']['by_pair_mask'] for b in fibres['Q']['by_pair_mask'] if not (a['pair_mask']&b['pair_mask'])]
        if not compatible:
            stat['contact_incompatible']+=1
            contact_reject_digest.update((json.dumps(p,sort_keys=True,separators=(',',':'))+'\n').encode())
            continue
        stat['common_feasible']+=1
        stat['full_contact_interfaces']+=sum(x[2] for x in compatible)
        for c in ('P','Q'):
            fibre=fibres[c];ck=json.dumps(fibre['definition'],sort_keys=True,separators=(',',':'))
            cid='c'+hashlib.sha256(ck.encode()).hexdigest()[:12];catalog[cid]=fibre;p[c]['contact_fibre']=cid
        rids=[]
        for row in results:
            # Literal fixed-cell reasons are recovered from this profile's W and
            # the contact-fibre source map; do not replace actual attachments.
            compact={k:v for k,v in row.items() if k!='fixed_sources'}
            rk=json.dumps(compact,sort_keys=True,separators=(',',':'));rid='m'+hashlib.sha256(rk.encode()).hexdigest()[:12]
            row_catalog[rid]=compact;rids.append(rid)
        p['id']=f'p{len(profiles):05d}';p['status']='common_feasible_projection';p['row_certificates']=rids;p['compatible_contact_pair_masks']=compatible
        profiles.append(p)
    return {'schema':'original55-LL-CUT-necessary-projection-v2','base':'3097ef5be241b7777451a5ef8a663f3987d6b866',
            'rows':{str(k):list(v) for k,v in ROWS.items()},'geometry_count':len(gs),'geometries':gs,
            'summary':stats,'cut_catalog':cuts,'cut_profile_digest':digest.hexdigest(),'contact_incompatible_digest':contact_reject_digest.hexdigest(),
            'contact_catalog':catalog,'row_catalog':row_catalog,'profiles':profiles,
            'coverage':'Every full-source LL-CUT failure projects here. Outside the Z screen a named full row/column gives the analytic capacity cut. Contact fibres retain same-source owners and B attachments; internal realization is NOT asserted.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    payload=generate();encoded=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n';path=HERE/'profiles.json'
    if args.check:
        assert path.read_text()==encoded,'generated interface certificate differs'
    else:
        with path.open('x') as stream:stream.write(encoded)
    print(json.dumps({'geometries':payload['geometry_count'],'summary':payload['summary'],'cut_shapes':len(payload['cut_catalog']),
                      'contact_catalog':len(payload['contact_catalog']),'profiles':len(payload['profiles']),
                      'sha256':hashlib.sha256(encoded.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
