#!/usr/bin/env python3
"""Literal original-label comparison with separately computed main certificates."""
import argparse
from copy import deepcopy
import gzip
import json
from check import HERE,AUDIT,WORDS,cycle_key,encode,sha,faces
from review import assert_faces


def compare(main,ind):
    mapping=main['canonical_to_original']
    assert mapping==ind['B']+sorted(set(ind['vertices'])-set(ind['B'])),'wrong original B mapping'
    assert main['B']==list(range(5)),'wrong canonical B labels'
    assert sorted([sorted([mapping[u],mapping[v]]) for u,v in main['edges']])==ind['edges'],'wrong original edges'
    assert {str(mapping[u]):[mapping[v] for v in ns] for u,ns in enumerate(main['rotation'])}==ind['rotation'],'wrong original rotation'
    assert {str(mapping[u]):d for u,d in enumerate(main['degree'])}==ind['degree'],'wrong complete degree'
    assert_faces([[mapping[v] for v in f] for f in main['faces']],ind['faces'])
    assert len(main['outer_face'])==5,'wrong outer face size'
    assert cycle_key([mapping[v] for v in main['outer_face']]) in (cycle_key(ind['B']),cycle_key(ind['B'][::-1])),'wrong specified outer face'
    assert main['mask']==ind['mask'],'wrong full relation mask'
    assert len(main['rows'])==10,'missing complete relation row'
    pos={v:i for i,v in enumerate(ind['vertices'])}
    for mr,ir in zip(main['rows'],ind['rows']):
        assert mr['pattern']==ir['word'],'wrong row pattern'
        expected=sorted(''.join(lift[pos[v]] for v in mapping) for lift in ir['lifts'])
        assert mr['lifts']==expected,'missing or invalid accepted full lift'
        assert mr['count']==ir['count'],'wrong complete fibre count'
    assert len(main['frames'])==10,'missing D5 frame'
    for mf,expected in zip(main['frames'],ind['d5_frames']):
        assert mf['start']==expected['shift'] and mf['sign']==expected['direction'],'wrong D5 frame'
        assert mf['counts']==expected['counts'] and mf['mask']==expected['mask'],'wrong D5 full relation'
        assert mf['canonical_to_original']==expected['B']+sorted(set(ind['vertices'])-set(expected['B'])),'wrong D5 graph mapping'
        assert [mapping[v] for v in mf['new_to_base']]==mf['canonical_to_original'],'wrong D5 base mapping'
        assert mf['counts']==[main['rows'][i]['count'] for i in mf['row_new_to_base']],'wrong D5 row mapping'
    col=ind['collar']
    for key in ('h','e'):assert main[key]==col[key],'wrong h or e'
    for key in ('apex','I'):assert [mapping[v] for v in main[key]]==col[key],f'wrong {key}'
    assert sorted(mapping[v] for group in main['y'] for v in group)==col['y'],'wrong collar Y'
    assert cycle_key([mapping[v] for v in main['C']]) in (cycle_key(col['C']),cycle_key(col['C'][::-1])),'wrong inner C'
    assert sorted(sorted(mapping[v] for v in edge) for edge in main['C_chords'])==col['chords'],'missing collar chord'
    assert sorted(sorted(mapping[v] for v in edge) for edge in main['H_edges'])==col['H_edges'],'missing H edge'
    H={int(u):[v for v in row if v not in ind['B']] for u,row in ind['rotation'].items() if int(u) not in ind['B']}
    assert {mapping[u+5]:[mapping[v+5] for v in ns] for u,ns in enumerate(main['H_rotation'])}==H,'wrong H rotation'
    assert [len(H[mapping[v]]) for v in range(5,18)]==main['H_degree'],'wrong H degree'
    assert_faces([[mapping[v+5] for v in f] for f in main['H_faces']],faces(H))
    for v in range(5,18):
        actual=[i for i,b in enumerate(ind['B']) if b in ind['rotation'][str(mapping[v])]]
        assert main['attachments'][str(v)]==actual,'wrong original attachment'
    assert main['n5']==sum(ind['degree'][str(v)]==5 for v in ind['vertices'] if v not in ind['B']),'wrong n5'


def run():
    independent=json.loads(gzip.decompress((HERE/'relations.json.gz').read_bytes()))
    inds={r['id']:r for r in independent['records']}; mains={};hashes={}
    for file in sorted((AUDIT/'cores').glob('sphere-*.json.gz')):
        hashes[str(file.relative_to(AUDIT))]=sha(file)
        for record in json.loads(gzip.decompress(file.read_bytes())):
            rid=f"S{record['sphere']:03d}-z{record['root']:02d}"
            assert rid not in mains,'duplicate main core';mains[rid]=record
    assert set(mains)==set(inds),'main core coverage differs'
    for rid in sorted(mains):compare(mains[rid],inds[rid])
    controls=[];first=sorted(mains)[0];chord=next(rid for rid in sorted(mains) if mains[rid]['C_chords'])
    def reject(name,rid,mutator):
        damaged=deepcopy(mains[rid]);mutator(damaged)
        try:compare(damaged,inds[rid])
        except AssertionError as err:controls.append({'control':name,'source':rid,'result':'rejected','reason':str(err)})
        else:raise AssertionError('control survived: '+name)
    reject('missing collar chord',chord,lambda r:r['C_chords'].pop())
    reject('wrong outer face',first,lambda r:r.__setitem__('outer_face',next(f for f in r['faces'] if len(f)==3)))
    def wrong_mapping(r):r['canonical_to_original'][0],r['canonical_to_original'][1]=r['canonical_to_original'][1],r['canonical_to_original'][0]
    reject('wrong B labels',first,wrong_mapping)
    reject('wrong degree',first,lambda r:r['degree'].__setitem__(0,r['degree'][0]+1))
    def omit_lift(r):r['rows'][0]['lifts'].pop();r['rows'][0]['count']-=1
    reject('missing accepted full lift',first,omit_lift)
    reject('wrong relation mask',first,lambda r:r.__setitem__('mask',r['mask']^1))
    return {'status':'pass','sources':len(mains),'full_lifts_compared':independent['total_full_lifts'],'row_fibres':len(mains)*10,'all_D5_frames':len(mains)*10,'core_sha256':hashes,'independent_relation_sha256':sha(HERE/'relations.json.gz'),'controls':controls}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run();path=HERE/'compare_main.json';data=encode(result)+b'\n'
    if args.check:assert path.read_bytes()==data,'main comparison differs'
    else:
        with path.open('xb') as f:f.write(data)
    print(json.dumps(result,indent=2,sort_keys=True))
