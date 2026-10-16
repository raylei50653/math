#!/usr/bin/env python3
"""Exact common-neighbour case elimination; source trigger absent."""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def edge(a,b):
    return tuple(sorted((a,b)))


def simple_five_cycles(edges, required):
    out=[]
    for tail in permutations(range(1,5)):
        c=(0,)+tail
        if c[1]>c[-1]:
            continue
        ce={edge(c[i],c[(i+1)%5]) for i in range(5)}
        if ce<=edges and required<=ce:
            out.append(list(c))
    return out


def skeletons():
    out={}
    for kind in ('ef','eg'):
        mandatory=({(0,1),(2,3)} if kind=='ef' else
                   {(0,1),(0,2),(0,3),(2,3)})
        forbidden=({(0,2),(0,3),(1,2),(1,3)} if kind=='ef' else {(1,2),(1,3)})
        optional=sorted(set(combinations(range(5),2))-mandatory-forbidden)
        assert optional==[(0,4),(1,4),(2,4),(3,4)]
        rows=[]
        for bits in product((0,1),repeat=len(optional)):
            es=mandatory|{e for e,b in zip(optional,bits) if b}
            admissible=(kind=='ef' or not ((1,4) in es and
                                          ((2,4) in es or (3,4) in es)))
            cs=simple_five_cycles(es,{(0,1),(2,3)})
            if admissible:
                assert not cs
            rows.append(dict(optional_bits=bits,edges=sorted(es),
                             exact_source_common_neighbours=admissible,cycles=cs))
        if kind=='eg':
            assert any(r['cycles'] for r in rows if not r['exact_source_common_neighbours'])
        out[kind]=rows
    return out


def calculate():
    addition=json.loads((ROOT/'ADDITIONAL_INPUTS.json').read_text())
    assert addition['base']=='f1faf743833c51ddc5efbe9e0f390b87b9f2311d'
    hashes={}
    for r in addition['authority_inputs']:
        p=ROOT/'frozen'/r['path']
        actual=sha256(p.read_bytes()).hexdigest()
        assert actual==r['sha256']
        hashes[r['path']]=actual
    rows=[]
    for ac,cc in product((4,5,'ge6'),repeat=2):
        if ac!='ge6' and cc!='ge6':
            continue # two degrees at most five violate their sum>=11
        a=(max(6,11-cc) if ac=='ge6' and cc!='ge6' else 6 if ac=='ge6' else ac)
        c=(max(6,11-ac) if cc=='ge6' and ac!='ge6' else 6 if cc=='ge6' else cc)
        assert a+c>=11
        for endpoint,other,d,opposite in [('q','p',c,a),('p','q',a,c)]:
            if d==4:
                rows.append(dict(a_case=ac,c_case=cc,core_endpoint=endpoint,
                                 endpoint_is_adjacent_to_m=True,
                                 eliminated_by='core chord m'+endpoint))
                continue
            jname='j_c' if endpoint=='q' else 'j_a'
            universe=['z',other,jname,'other_fresh_vertex']
            present={'z'}
            if d==5: present.add(jname)
            if opposite==4: present.add(other)
            candidates=[]
            for u in universe:
                member=u in present
                chord=(u==jname)
                duplicate=u in ('z',other)
                viable=member and not chord and not duplicate
                assert not viable
                candidates.append(dict(vertex=u,in_common_neighbours=member,
                                       retained_z_edge_is_core_chord=chord,
                                       repeats_original_five_cycle_vertex=duplicate,
                                       viable=viable))
            rows.append(dict(a_case=ac,c_case=cc,core_endpoint=endpoint,
                             endpoint_is_adjacent_to_m=False,
                             common_neighbours=sorted(present),candidates=candidates))
    assert len(rows)==10
    return dict(base=addition['base'],additional_authority_sha256=hashes,
                additional_manifest_sha256=sha256((ROOT/'ADDITIONAL_INPUTS.json').read_bytes()).hexdigest(),
                proof_sha256=sha256((HERE/'MARKED_CUTS.md').read_bytes()).hexdigest(),
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                original_minimum_sources='not triggered',
                degree_classes_and_cores=rows,local_five_vertex_skeletons=skeletons())


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true')
    p.add_argument('--certificate',type=Path,default=HERE/'marked-cuts-certificate.json')
    args=p.parse_args(); actual=json.loads(json.dumps(calculate()))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(actual,f,indent=2,sort_keys=True);f.write('\n')
    else:
        assert actual==json.loads(args.certificate.read_text()),'marked-cut certificate mismatch'
    print('PASS: 5 unbounded degree classes, 10 oriented core cases; e/f 16 and e/g 10 admissible local graphs; source not triggered')


if __name__=='__main__': main()
