#!/usr/bin/env python3
"""Compare independently rebuilt structures and run destructive-copy controls."""
import argparse
from copy import deepcopy
import gzip
import json
from pathlib import Path
from check import AUDIT,HERE,WORDS,planar_code,faces,edges,cycle_key,colourings,d5_relation,encode,sha


def face_family(fs):
    return sorted(min(cycle_key(f),cycle_key(f[::-1])) for f in fs)

def assert_faces(actual,expected):
    assert face_family(actual)==face_family(expected),'wrong faces/outer face'
    oriented=sorted(cycle_key(f) for f in actual)
    assert oriented in (sorted(cycle_key(f) for f in expected),sorted(cycle_key(f[::-1]) for f in expected)),'inconsistent face orientation'

def source_check(src,ind):
    assert src['B']==ind['B'],'wrong B labels'
    assert src['z']==ind['z'],'wrong deleted sphere vertex'
    assert src['vertices']==ind['vertices'],'wrong vertices'
    assert src['canonical_to_original']==ind['B']+sorted(set(ind['vertices'])-set(ind['B'])),'wrong canonical to original mapping'
    assert src['edges']==ind['edges'],'wrong or missing original edges'
    assert src['rotation']==ind['rotation'],'wrong rotation'
    assert src['degree']==ind['degree'],'degree miscalculation'
    assert_faces(src['faces'],ind['faces'])
    col=ind['collar'];assert col['valid'] and src['collar_status']=='holds','collar status'
    for key in ('h','e','apex','I'):
        assert src[key]==col[key],f'wrong collar {key}'
    assert sorted(src['y'])==col['y'],'wrong collar Y'
    assert cycle_key(src['C']) in (cycle_key(col['C']),cycle_key(col['C'][::-1])),'wrong collar cycle'
    assert src['C_chords']==col['chords'],'missing or incorrect collar chord'
    assert src['H_edges']==col['H_edges'],'missing or incorrect H edge'
    H={int(u):[v for v in row if v not in ind['B']] for u,row in ind['rotation'].items() if int(u) not in ind['B']}
    assert src['H_rotation']=={str(u):row for u,row in H.items()},'wrong H rotation'
    assert src['H_degree']=={str(u):len(row) for u,row in H.items()},'wrong H degree'
    assert_faces(src['H_faces'],faces(H))
    for v in H:
        assert src['attachments'][str(v)]==[i for i,b in enumerate(ind['B']) if b in ind['rotation'][str(v)]],'wrong boundary attachments'
    assert not src['B_chords'],'unexpected B chord'
    assert len(src['d5_frames'])==10,'missing whole-graph D5 frame'
    for frame,expected in zip(src['d5_frames'],ind['d5_frames']):
        for key in ('shift','direction','B'):assert frame[key]==expected[key],f'wrong D5 {key}'
        assert frame['canonical_to_original']==frame['B']+sorted(set(ind['vertices'])-set(frame['B'])),'wrong whole graph D5 mapping'


def relation_check(rec):
    adj={int(v):row for v,row in rec['rotation'].items()}
    recomputed=[]
    assert len(rec['rows'])==10,'missing boundary row'
    for word,row in zip(WORDS,rec['rows']):
        lifts,_=colourings(adj,rec['B'],word)
        assert row['word']==word,'wrong boundary word'
        assert row['lifts']==lifts,'incomplete or invalid full lifts'
        assert row['count']==len(lifts),'wrong complete fibre count'
        recomputed.append(len(lifts))
    assert rec['mask']==sum(1<<i for i,n in enumerate(recomputed) if n),'wrong relation mask'


def run():
    independent=json.loads(gzip.decompress((HERE/'relations.json.gz').read_bytes()))
    sources=json.loads((AUDIT/'generation/rooted_sources.json').read_text())
    inds={r['id']:r for r in independent['records']};srcs={r['id']:r for r in sources}
    assert len(inds)==len(independent['records']) and len(srcs)==len(sources),'duplicate root'
    assert set(inds)==set(srcs),'root coverage differs'
    # Read original bytes again, independently of either generated JSON list.
    spheres=planar_code(AUDIT/'generation/spheres19.pc')
    roots={f'S{si:03d}-z{z:02d}' for si,g in enumerate(spheres) for z in g if len(g[z])==5}
    assert set(inds)==roots,'omitted degree-five root'
    for rid in sorted(roots):source_check(srcs[rid],inds[rid])
    controls=[]
    def must_reject(name,source_id,mutator,checker,target):
        damaged=deepcopy(target);mutator(damaged)
        try:checker(damaged)
        except AssertionError as err:
            controls.append({'control':name,'source':source_id,'result':'rejected','reason':str(err)})
        else:raise AssertionError('negative control survived: '+name)
    first=next(iter(inds));colid=next(rid for rid,r in inds.items() if r['collar']['chords'])
    def omit_chord(src):
        chord=src['C_chords'].pop();src['H_edges'].remove(chord)
    must_reject('missing collar chord',colid,omit_chord,lambda s:source_check(s,inds[colid]),srcs[colid])
    def wrong_outer(src):
        i=next(i for i,f in enumerate(src['faces']) if len(f)==5)
        src['faces'][i]=src['faces'][(i+1)%len(src['faces'])].copy()
    must_reject('wrong specified outer face',first,wrong_outer,lambda s:source_check(s,inds[first]),srcs[first])
    def wrong_B(src):src['B'][0],src['B'][1]=src['B'][1],src['B'][0]
    must_reject('wrong original B labels',first,wrong_B,lambda s:source_check(s,inds[first]),srcs[first])
    def wrong_degree(src):src['degree'][str(src['B'][0])]+=1
    must_reject('degree miscalculation',first,wrong_degree,lambda s:source_check(s,inds[first]),srcs[first])
    def omit_lift(rec):
        rec['rows'][0]['lifts'].pop();rec['rows'][0]['count']-=1
    must_reject('missing accepted full lift',first,omit_lift,relation_check,inds[first])
    def wrong_mask(rec):rec['mask']^=1
    must_reject('wrong complete relation mask',first,wrong_mask,relation_check,inds[first])
    # Independent negative universal-root coverage check.
    try:assert set(list(roots)[1:])==roots,'omitted degree-five root'
    except AssertionError as err:controls.append({'control':'omitted root','result':'rejected','reason':str(err)})
    # A non-full relation independently exercises the D5 row permutation.
    cycle={i:[(i-1)%5,(i+1)%5] for i in range(5)}
    cycle[0].append(2);cycle[2].append(0)
    calibration_rows=[{'count':len(colourings(cycle,list(range(5)),w)[0])} for w in WORDS]
    calibration_frames=d5_relation(list(range(5)),calibration_rows)
    for frame in calibration_frames:
        direct=[len(colourings(cycle,frame['B'],w)[0]) for w in WORDS]
        assert direct==frame['counts'],'D5 transported counts differ from direct search'
    assert len({f['mask'] for f in calibration_frames})==5,'nontrivial D5 calibration failed'
    return {'d5_nonfull_calibration_masks':[f['mask'] for f in calibration_frames], 'sources':len(roots),'structures':'all generation source structures match independently rebuilt original sphere deletion','independent_relation_sha256':sha(HERE/'relations.json.gz'),'source_sha256':sha(AUDIT/'generation/rooted_sources.json'),'normal':'pass','controls':controls}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run();path=HERE/'review.json';data=encode(result)+b'\n'
    if args.check:assert path.read_bytes()==data,'review differs'
    else:
        with path.open('xb') as stream:stream.write(data)
    print(json.dumps(result,indent=2,sort_keys=True))
