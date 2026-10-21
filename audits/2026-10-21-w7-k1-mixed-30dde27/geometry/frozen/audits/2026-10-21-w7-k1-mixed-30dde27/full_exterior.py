#!/usr/bin/env python3
"""Exact full-fibre necessary closure on the SAME original exposed E.

The universal C13 columns are rebuilt without the old D cap-zero filter.
Empty strip-extension fibres are retained, never asserted to be zero E fibres.
"""
import argparse
from hashlib import sha256
from itertools import product
import gzip
import importlib.util
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COUNT = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
P = ['n','u4','u3','u2','u1','L']
RIM = ['a',*P,'q','c','s','v','w','t']
EXPECTED_FULL = '530aeac43e108f7c94f1e120ec341c18528d36dc3fd41356b5f3b79b3b94a7d5'
UNIVERSAL_PAYLOAD_SHA = '7848b0e32119294241d36ff7668a49b3cff05f4865bbf61b568c1fc39f4e6c83'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def digest(x):
    return sha256(packed(x)).hexdigest()


def canonical(t):
    seen = {}
    return tuple(seen.setdefault(x,len(seen)) for x in t)


def encode(t):
    value = 0
    for c in t:
        value = 4*value+c
    return value


def half(t):
    a = t[0]; b = next(x for x in t if x//2 != a//2)
    p = {a:0,a^1:1,b:2,b^1:3}
    return tuple(p[x] for x in t)


def nc(n,t=(0,),stack=(0,),b=1):
    if len(t)==n:
        yield t
        return
    for j,x in enumerate(stack):
        yield from nc(n,t+(x,),stack[:j+1],b)
    yield from nc(n,t+(b,),stack+(b,),b+1)


def inputs():
    manifest = json.loads((HERE/'BASE.json').read_text())
    for row in manifest['inputs']:
        raw = (HERE/'frozen'/row['path']).read_bytes()
        require(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],'frozen input drift')
        require(raw==(ROOT/row['path']).read_bytes(),'live mathematical input drift')
    caps = json.loads(gzip.decompress((HERE/'frozen'/COUNT/'caps.json.gz').read_bytes()))
    old = json.loads(gzip.decompress((HERE/'frozen'/COUNT/'orbits.json.gz').read_bytes()))
    return caps,old


def build_universal(caps):
    states = caps['states']; rowids = {}
    for sid,t in enumerate(states):
        for mate in (1,2,3):
            other=[x for x in (1,2,3) if x!=mate]
            p={0:0,mate:1,other[0]:2,other[1]:3}
            row=encode(half(tuple(p[x] for x in t)))
            require(row not in rowids or rowids[row]==sid,'row map conflict')
            rowids[row]=sid
    cols=set(); family=sha256(); parts=0; admissible=0; generated=0
    for p in nc(13):
        parts+=1; b=max(p)+1
        if b==1 or sum(p[i]!=p[(i+1)%13] for i in range(13))!=2*(b-1):
            continue
        adjacent=[set() for _ in range(b)]
        for i in range(13):
            x,y=p[i],p[(i+1)%13]
            if x!=y:
                adjacent[x].add(y); adjacent[y].add(x)
        side=[None]*b; side[0]=0; todo=[0]; okay=True
        while todo:
            x=todo.pop()
            for y in adjacent[x]:
                if side[y] is None:
                    side[y]=1-side[x];todo.append(y)
                elif side[y]==side[x]:
                    okay=False
        if not okay:
            continue
        admissible+=1
        first=[p.index(x) for x in range(b)]
        anchor=next(x for x in p if side[x])
        masks=[sum(1<<(2*(12-i)) for i in range(13) if p[i]==x)
               for x in range(b) if x not in (0,anchor)]
        free=[i for i in range(1,13) if p[i]!=p[i-1] and i!=first[p[i]]]
        for choice in product((0,1),repeat=len(free)):
            chosen=dict(zip(free,choice));bits=[0]*13
            for i in range(1,13):
                if p[i]==p[i-1]:bits[i]=1-bits[i-1]
                elif i in chosen:bits[i]=chosen[i]
            if p[-1]==p[0] and bits[-1]==bits[0]:continue
            t=tuple(2*side[p[i]]+bits[i] for i in range(13))
            require(all(t[i]!=t[(i+1)%13] for i in range(13)) and half(t)==t,'invalid universal tuple')
            orbit=[encode(t)]
            for mask in masks:orbit += [x^mask for x in orbit]
            orbit=tuple(sorted(orbit));generated+=1
            family.update(packed(orbit)+b'\n');cols.add(orbit)
    require(parts==742900 and admissible==41834 and generated==428506,'universal NC coverage changed')
    require(family.hexdigest()==EXPECTED_FULL,'unfiltered full family does not match original generated SHA')
    return {'rowids':sorted(rowids.items()),'columns':sorted(cols),
            'all_states':len(states),'noncrossing_count':parts,'admissible_partitions':admissible,
            'generated_columns':generated,'full_family_sha256':family.hexdigest(),
            'old_D_zero_filter_used':False}


def source_collar():
    path=HERE/'frozen/audits/2026-10-21-w7-profile0-13e51db/check.py'
    spec=importlib.util.spec_from_file_location('frozen_collar',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def zero_seeds(center,caps,old,module):
    shape=[int(x==center) for x in P]
    data,graph=module.collar(0,shape,with_graph=True)
    A=data['boundary'][1:]; boundary=[*A,'c','s','v','w','t']
    require(len(boundary)==13,'the complete E interface must be C13')
    state_index={tuple(t):i for i,t in enumerate(caps['states'])}
    oldlive=set(old['live']); zero=[]; no_extension=[]; witnesses=[]; D_images=[]; all_P_lifts=[]
    for eid,sigma in enumerate(caps['states']):
        fixed=dict(zip(boundary,sigma))
        domains=[sorted(set(range(4))-{fixed[x] for x in graph[t] if x in fixed}) for t in P]
        images=[]; full_P=[]; bad=None
        for colors in product(*domains):
            if any(a==b for a,b in zip(colors,colors[1:])):continue
            D=tuple([fixed['a'],*colors,fixed['q'],fixed['c'],fixed['s'],fixed['v'],fixed['w'],fixed['t']])
            sid=state_index[canonical(D)];images.append(sid)
            full_P.append([list(colors),sid])
            if sid not in oldlive and bad is None:
                bad={'E_state':eid,'P':list(colors),'D_literal':list(D),'old_zero_state':sid}
        if not images:no_extension.append(eid)
        if bad is not None:zero.append(eid);witnesses.append(bad)
        D_images.append(sorted(set(images)))
        all_P_lifts.append(full_P)
    # Encode the ORIGINAL b=1 target boundary, without normalizing pieces.
    Y=next(x for x in A if x.startswith('H')); cut=A.index(Y)
    fixed={'a':0,'q':3,Y:3-[1,2,1,2,1,2][P.index(center)]}
    for i in range(1,cut):fixed[A[i]]=3-fixed[A[i-1]]
    for i in range(len(A)-2,cut,-1):fixed[A[i]]=3-fixed[A[i+1]]
    targets=[]
    for e0,e1 in ((0,1),(1,0)):
        fixed.update({'c':1,'s':2,'v':e0,'w':e1,'t':2})
        literal=[fixed[x] for x in boundary]
        targets.append({'literal':literal,'E_state':state_index[canonical(literal)]})
    return {'center':center,'shape':shape,'ordered_E_boundary':boundary,'all_extension_D_state_ids':D_images,
            'all_extension_P_literal_lifts':all_P_lifts,
            'P_lift_columns':['ordered_P_literal_colors','canonical_D_state_id'],
            'zero_seeds':zero,'zero_seed_witnesses':witnesses,
            'empty_D_extension_E_fibres_retained':no_extension,'original_targets':targets}


def close(universal,seeds):
    rowids=universal['rowids']; keys=np.array([r for r,s in rowids],dtype=np.int64)
    row_state=np.array([s for r,s in rowids],dtype=np.int32)
    lengths=np.array([len(c) for c in universal['columns']],dtype=np.int32)
    offsets=np.r_[0,np.cumsum(lengths)[:-1]]
    raw=np.array([r for c in universal['columns'] for r in c],dtype=np.int64)
    incidence=np.searchsorted(keys,raw)
    require(np.array_equal(keys[incidence],raw),'universal incidence is incomplete')
    flat_state=row_state[incidence]
    results=[]
    for seed in seeds:
        live=np.ones(universal['all_states'],dtype=bool);live[seed['zero_seeds']]=False
        history=[]; proof=[]
        while True:
            col_live=np.logical_and.reduceat(live[flat_state],offsets)
            supported=np.zeros(len(keys),dtype=bool)
            np.logical_or.at(supported,incidence,np.repeat(col_live,lengths))
            next_live=live.copy();np.logical_and.at(next_live,row_state,supported)
            dead=np.flatnonzero(live & ~next_live).tolist()
            history.append({'states':int(next_live.sum()),'columns':int(col_live.sum()),'new_zero':len(dead)})
            if not dead:break
            proof.append(dead);live=next_live
        final_ids=np.flatnonzero(live).tolist(); final_columns=np.flatnonzero(col_live).tolist()
        results.append({'center':seed['center'],'zero_seeds':len(seed['zero_seeds']),
                        'empty_D_extension_E_fibres_initially_retained':len(seed['empty_D_extension_E_fibres_retained']),
                        'rounds':history,'new_zero_state_ids_by_round':proof,
                        'final_live_E_state_ids':final_ids,'final_live_column_ids':final_columns,
                        'final_live_state_sha256':digest(final_ids),'final_live_column_sha256':digest(final_columns),
                        'targets':[t|{'survives':bool(live[t['E_state']])} for t in seed['original_targets']]})
    return results


def boundary_blocks(column, reference):
    groups = {}
    for i,c in enumerate(reference):
        signature = tuple(((h^encode(reference)) >> (2*(12-i))) & 1 for h in column)
        groups.setdefault((c//2,signature),[]).append(i)
    blocks = sorted(groups.values(),key=lambda b:b[0])
    # Recreate the complete projected orbit, with the two global anchors fixed.
    anchors = [next(j for j,b in enumerate(blocks) if reference[b[0]]//2 == p) for p in (0,1)]
    generated = [column[0]]
    for j,b in enumerate(blocks):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in b)
            generated += [h^mask for h in generated]
    require(sorted(generated) == column,'boundary blocks lose complete component flips')
    return blocks


def L_residual(universal, seed, closed):
    names = seed['ordered_E_boundary']; y = next(i for i,n in enumerate(names) if n.startswith('H'))
    live = set(closed['final_live_column_ids']); initial_zero = set(seed['zero_seeds'])
    rowmap = dict(universal['rowids']); results = []
    for target in seed['original_targets']:
        for mate in (1,2,3):
            other = [c for c in (1,2,3) if c != mate]
            p = {0:0,mate:1,other[0]:2,other[1]:3}
            reference = half(tuple(p[c] for c in target['literal'])); h = encode(reference)
            initial = []; after_seeds = []; final = []
            for j,column in enumerate(universal['columns']):
                if h not in column:continue
                initial.append(j)
                if all(rowmap[r] not in initial_zero for r in column):after_seeds.append(j)
                if j in live:
                    blocks = boundary_blocks(column,reference)
                    y_block = next(b for b in blocks if y in b)
                    final.append({'column_id':j,'whole_column':column,
                                  'component_blocks':[[names[i] for i in b] for b in blocks],
                                  'Y_component_contacts':[names[i] for i in y_block]})
            require(len(final) == {1:4,2:2,3:1}[mate], 'L residual partition count changed')
            if mate == 1:
                require(all({'a','z4','c',names[y]} <= set(r['Y_component_contacts']) for r in final),
                        'L Y-to-a,z4,c necessity was lost')
            results.append({'literal_E_target':target['literal'],'E_state':target['E_state'],
                            'split_containing_0':[0,mate],'all_incident_columns':initial,
                            'incident_after_zero_seeds':after_seeds,'complete_surviving_columns':final})
    return results


def validate_universal(raw):
    require(sha256(raw).hexdigest() == UNIVERSAL_PAYLOAD_SHA,'universal E family corrupted or filtered')


def verify(actual,expected):
    require(actual == expected,'damaged exterior full fibres or enlarged source claim')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-universal',action='store_true')
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'full-exterior-v3.json.gz')
    args=parser.parse_args();caps,old=inputs()
    upath=HERE/'universal-C13.json.gz'
    if args.build_universal:
        data=build_universal(caps)
        with upath.open('xb') as stream:
            with gzip.GzipFile(fileobj=stream,mode='wb',mtime=0) as z:z.write(packed(data))
        print(json.dumps({'universal_columns':len(data['columns']),'full_family_sha256':data['full_family_sha256']}),flush=True)
        if not args.build:return
    raw = gzip.decompress(upath.read_bytes());validate_universal(raw)
    universal=json.loads(raw)
    require(universal['old_D_zero_filter_used'] is False and universal['full_family_sha256']==EXPECTED_FULL,'wrong E authority')
    module=source_collar();seeds=[zero_seeds(t,caps,old,module) for t in ['u3','u1','L']]
    closures = close(universal,seeds)
    result={'zero_seed_relations':seeds,'closures':closures,
            'L_complete_residual':L_residual(universal,seeds[2],closures[2]),
            'source_realized':False,'general_profile0_excluded':False,'new_Lean':False,'LP_run':False,
            'scope':'complete necessary support closure for the same original E, with whole strip fibres'}
    path=args.certificate
    if args.build:
        with path.open('xb') as stream:
            with gzip.GzipFile(fileobj=stream,mode='wb',mtime=0) as z:z.write(packed(result))
    else:verify(json.loads(gzip.decompress(path.read_bytes())),result)
    print(json.dumps({'result':'PASS','results':[{k:v for k,v in r.items() if k not in ('final_live_E_state_ids','final_live_column_ids','new_zero_state_ids_by_round')} for r in result['closures']]},sort_keys=True),flush=True)


if __name__=='__main__':main()
