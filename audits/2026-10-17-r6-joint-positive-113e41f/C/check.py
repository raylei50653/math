#!/usr/bin/env python3
"""Finite algebra calibration for the split-source pivotal-component proof.

This does not enumerate or assert a realizable minimum source.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
COLOURS=tuple(range(4))
PINS=('z','s','v','w','t','u','d')
EDGES=((0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(5,6),(6,0))
JEDGES=((0,1),(0,2),(0,3),(2,3),(1,4),(1,5),(4,5))
E=(0,2,0,1,2,2,1)
F=(0,2,0,1,2,3,1)
H=(0,2,3,1,2,3,1)
AUTHORITIES=(
'audits/2026-10-16-r6-319-complete-e98a1cc/A/PROOF.md',
'audits/2026-10-16-r6-319-continuation-f1faf74/A/PROOF.md',
'audits/2026-10-16-r6-319-joint-parity-f1faf74/A/PROOF.md')


def need(condition,message):
    if not condition: raise ValueError(message)


def digest(path): return sha256(path.read_bytes()).hexdigest()


def proper(row): return all(row[a]!=row[b] for a,b in EDGES)


def lifts(row): return [c for c in COLOURS if c not in row[1:5]] if proper(row) else []


def direct_return(row,r):
    z,s,v,w,t,u,d=row
    if z==r: return s==t and {u,d}==set(COLOURS)-{z,s}
    if s==t: return bool({u,d} & (set(COLOURS)-{z,s,r}))
    return {u,d}=={s,t}


def fj(row):
    z,m,v,w,t,u,d=row
    need(m==t,'not a J row')
    e,f,g=v^w,u^d,m^z
    return (e==f)==(e==g)


def swap(row,component,palette):
    out=list(row)
    for v in component:
        need(out[v] in palette,'component contains wrong colour')
        out[v]=sum(palette)-out[v]
    return tuple(out)


def partitions(vertices,edges):
    if not vertices: return ((),)
    result=[]
    def extend(labels):
        if len(labels)<len(vertices):
            for k in range(max(labels)+2): extend(labels+(k,))
            return
        lab=dict(zip(vertices,labels))
        if any(a in lab and b in lab and lab[a]!=lab[b] for a,b in edges): return
        result.append(tuple(tuple(v for v in vertices if lab[v]==k) for k in range(max(labels)+1)))
    extend((0,))
    return tuple(result)


def component(parts,v): return next(part for part in parts if v in part)


def calculate():
    base=json.loads((AUDIT/'BASE.json').read_text())
    records={r['path']:r for r in base['inputs']}
    authorities=[]
    for rel in AUTHORITIES:
        need(digest(AUDIT/'frozen'/rel)==records[rel]['sha256'],'frozen authority drift')
        authorities.append(records[rel])
    slots=[]
    jrows=0
    for row in product(COLOURS,repeat=7):
        ll=lifts(row)
        outcomes=[int(direct_return(row,r)) for r in ll]
        isj=proper(row) and row[1]==row[4]
        if isj:
            jrows+=1
            need(len(ll)==1,'lost full J lift')
            need(all(outcomes)==fj(row),'direct all-r/FJ mismatch')
        slots.append([int(proper(row)),ll,outcomes,int(isj)])
    need(len(slots)==16384,'missing zero or improper slot')

    rules=[]
    for reflected in (False,True):
        # Reflection carries the original labels, without asserting symmetry.
        order=(0,4,3,2,1,5,6) if reflected else tuple(range(7))
        er=tuple(E[i] for i in order)
        fr=tuple(F[i] for i in order)
        hr=tuple(H[i] for i in order)
        target=3 if reflected else 2
        for family,row,palette,point,other in (
            ('E_AD',er,(0,3),target,0),
            ('F_BC',fr,(1,2),4 if reflected else 1,1 if reflected else 4)):
            vertices=tuple(i for i,c in enumerate(row) if c in palette)
            for pp in partitions(vertices,EDGES):
                separated=component(pp,point)!=component(pp,other)
                image=swap(row,component(pp,point),palette)
                image_lifts=lifts(image)
                if separated:
                    need(proper(image),'full component image lost edge')
                    need(image_lifts,'the alleged contradiction lost its r lift')
                    need(not all(direct_return(image,r) for r in image_lifts),'source-forbidden component split survived')
                rules.append({'reflection':reflected,'family':family,'partition':pp,
                              'separated':separated,'whole_component_image':image,
                              'full_r_lifts':image_lifts,
                              'all_r_rule':all(direct_return(image,r) for r in image_lifts)})
        # The actual outer positions alternate z,s,v,t (or z,s,w,t).
        pair1=(0,target);pair2=(1,4)
        a,c=sorted(pair1)
        need(any(a<b<c for b in pair2) and any(b<a or b>c for b in pair2),'lost original Jordan alternation')
        # F AD separation follows the source BC connection and Jordan.
        pp=partitions(tuple(i for i,c in enumerate(fr) if c in (0,3)),EDGES)
        for pattern in pp:
            if component(pattern,target)==component(pattern,0): continue
            image=swap(fr,component(pattern,target),(0,3))
            need(image==hr,'wrong F to H full-component image')
            need(swap(image,component(pattern,target),(0,3))==fr,'F/H inverse lost')
            need(lifts(image)==[0] and all(direct_return(image,r) for r in lifts(image)),'H lost its explicit r=A')
            rules.append({'reflection':reflected,'family':'F_to_H','partition':pattern,'image':image})
        # H CD m-u lock: the displayed m-v edge fixes v with m.
        for pattern in partitions(tuple(i for i,c in enumerate(hr) if c in (2,3)),EDGES+((1,4),)):
            if component(pattern,5)==component(pattern,1): continue
            image=swap(hr,component(pattern,5),(2,3))
            need(proper(image) and image[1]==image[4],'H CD image lost J row')
            need(not fj(image) and not all(direct_return(image,r) for r in lifts(image)),'H CD separation was not forbidden')
            rules.append({'reflection':reflected,'family':'H_CD','partition':pattern,'image':image})

    # Ordered p/q equality transport in the remaining BC pairing.
    ej=(2,0,0,1,2,1)
    equality_transports=[]
    for pattern in partitions((0,3,4,5),JEDGES):
        if component(pattern,4)==component(pattern,0): continue
        image=swap(ej,component(pattern,4),(1,2))
        need(image==(2,0,0,1,1,2),'third transport lost original pq order')
        need(swap(image,component(pattern,4),(1,2))==ej,'third transport not inverse')
        equality_transports.append({'partition':pattern,'image':image})

    # The visible row type is exact throughout a full CD cube fixing m.
    # Three additional actual components miss the pins: their multiplicity
    # is retained instead of silently deleting those component flips.
    cube=[]
    for orientations in product((0,1),repeat=4):
        row=swap(E,(5,),(2,3)) if orientations[0] else E
        need(row in (E,F),'CD cube lost its whole-row type')
        need(lifts(row)==[3] and all(direct_return(row,r) for r in lifts(row)),'CD cube lost its full r lift')
        cube.append({'orientations':orientations,'row':row,
                     'source_forced_AD_zv':not bool(orientations[0]),
                     'source_forced_BC_st':bool(orientations[0])})
    counts=Counter(tuple(r['row']) for r in cube)
    need(counts=={E:8,F:8},'private-component multiplicity lost')

    return {'schema':'source319-split-pivotal-component-v1','base':base['base'],
            'binding':{'checker_sha256':digest(Path(__file__)),'proof_sha256':digest(HERE/'PROOF.md'),
                       'base_sha256':digest(AUDIT/'BASE.json')},
            'frozen_authorities':authorities,
            'universe':{'ordered_pins':PINS,'retained_edges':EDGES,
                        'columns':['proper','full_r_lifts','return_per_lift','is_J'],
                        'all_16384_slots_including_empty':slots},
            'literal_component_calibrations':rules,
            'third_ordered_equality_transport':equality_transports,
            'whole_CD_cube_with_private_multiplicities':cube,
            'summary':{'seven_pin_slots':len(slots),'proper_J_rows':jrows,
                       'literal_component_cases':len(rules),'CD_cube_members':len(cube),
                       'actual_minimum_sources':0,'source_realizability':'not triggered',
                       'joint_even_complement_positivity':'OPEN'}}


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true')
    p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=p.parse_args();result=calculate()
    if args.write:
        with args.certificate.open('x') as out: json.dump(result,out,separators=(',',':'));out.write('\n')
    else:
        need(json.loads(args.certificate.read_text())==json.loads(json.dumps(result)),
             'certificate mismatch: complete fibres, component updates or binding changed')
    print(json.dumps({'ok':True,**result['summary']},sort_keys=True))


if __name__=='__main__':main()
