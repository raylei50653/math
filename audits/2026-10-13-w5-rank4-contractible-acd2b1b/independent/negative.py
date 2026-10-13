#!/usr/bin/env python3
"""Recompute five positive families and reject malformed geometry/full relations.
Also preserve an actual same-Sigma/different-R3 control with its complete lifts.
"""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import check as independent
from kernels import BETAS, colour, rotation_faces
ROOT=Path(__file__).resolve().parent.parent

def encoded(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(obj):return hashlib.sha256(encoded(obj)).hexdigest()
def module(path):
    spec=importlib.util.spec_from_file_location('negative_primary',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def family(record):
    return tuple(''.join('H' if a.startswith('H') else a for a in c['atoms'] if a!='E') or 'P' for c in record['parameters']['components'])

def prism():
    fs=[[0,4,3,2,1]]+[[i,(i+1)%5,5+(i+1)%5,5+i] for i in range(5)]+[list(range(5,10))]
    es=sorted({tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in fs for i in range(len(f))})
    wf=fs[:-1]+[[5+i,5+(i+1)%5,10] for i in range(5)];we=sorted(es+[(i,10) for i in range(5,10)])
    def rotations(n,faces):
        rows=[]
        for v in range(n):
            link={f[i-1]:f[(i+1)%len(f)] for f in faces for i,w in enumerate(f) if v==w}
            first=min(link);row=[first]
            while link[row[-1]]!=first:row.append(link[row[-1]])
            assert len(row)==len(link);rows.append(row)
        return rows
    rot=rotations(10,fs);wr=rotations(11,wf)
    rotation_faces(10,es,fs,rot);rotation_faces(11,we,wf,wr)
    rec={'vertices':list(range(10)),'B':list(range(5)),'U':list(range(5,10)),
         'private':[],'edges':list(map(list,es)),'faces':fs,'rotation':rot,
         'wheel_edges':list(map(list,we)),'wheel_faces':wf,'wheel_rotation':wr,'rows':[]}
    mask=0
    for i,beta in enumerate(BETAS):
        cells=[[] for _ in range(1024)]
        for lift in colour(10,es,beta,False):cells[int(lift[5:10],4)].append(lift)
        gs=colour(10,es,beta,True)
        rec['rows'].append({'beta':list(beta),'cells':cells,'wheel_full_lifts':gs})
        if gs:mask|=1<<i
    rec['Sigma']=mask;assert mask==1023
    return rec

def compute():
    primary=module(ROOT/'controls/check.py');sources={}
    with gzip.open(ROOT/'controls/certificate.jsonl.gz','rt') as stream:
        next(stream)
        for line in stream:
            rec=json.loads(line);fam=family(rec)
            if rec['Sigma']==1023 and fam not in sources:sources[fam]=rec
            if len(sources)==5:break
    assert set(sources)=={('H',),('DD',),('H','P'),('DD','P'),('D','D')}
    def validate(rec):
        p=rec['parameters'];n,es,cs=independent.graph_from_neighbours(p)
        independent.geometry(rec,p,n,es,cs);independent.verify_rows(rec,n,es)
        assert rec['Sigma_in_K132']==(rec['Sigma'] in independent.catalogue())
    positives=[]
    for fam,rec in sources.items():
        expected=primary.fill(primary.make(rec['parameters']))
        expected['Sigma_in_K132']=expected['Sigma'] in primary.catalogue()[0]
        assert expected==rec;validate(rec)
        positives.append({'family':fam,'key':rec['key'],'sha256':digest(rec),'status':'triggered and holds'})
    source=sources[('H',)];bad=[]
    def mutate(name,fn,base=source):
        changed=copy.deepcopy(base);fn(changed)
        bad.append((name,base,changed))
    mutate('omitted_original_private_edge',lambda r:r['edges'].remove(next(e for e in r['edges'] if min(e)>=10)))
    mutate('wrong_catalogue_flag',lambda r:r.__setitem__('Sigma_in_K132',not r['Sigma_in_K132']))
    mutate('wrong_rank',lambda r:r['counts'].__setitem__('rho',3))
    mutate('wrong_M',lambda r:r['counts'].__setitem__('M',0))
    mutate('wrong_U_pin_map',lambda r:r['ownership']['pin_map'].__setitem__(slice(5,7),[6,5]))
    mutate('reverse_U_face',lambda r:r['faces'][-1].reverse())
    mutate('wrong_rotation',lambda r:r['rotation'][10].reverse())
    mutate('delete_component',lambda r:r['components'].pop(),sources[('H','P')])
    mutate('G_degree_confused_with_F',lambda r:r['degree_G'].__setitem__(slice(10,-1),r['degree_F']))
    mutate('wrong_U_degree_flag',lambda r:r.__setitem__('U_degree_at_least_5',not r['U_degree_at_least_5']))
    ri,ci=next((i,j) for i,row in enumerate(source['rows']) for j,cell in enumerate(row['cells']) if cell)
    mutate('omitted_A_lift',lambda r:r['rows'][ri]['cells'][ci].pop())
    gi=next(i for i,row in enumerate(source['rows']) if row['wheel_full_lifts'])
    mutate('omitted_G_lift',lambda r:r['rows'][gi]['wheel_full_lifts'].pop())
    ei,ec=next((i,j) for i,row in enumerate(source['rows']) for j,cell in enumerate(row['cells']) if not cell)
    mutate('empty_fibre_fabricated',lambda r:r['rows'][ei]['cells'][ec].append(source['rows'][ri]['cells'][ci][0]))
    mutate('omitted_row',lambda r:r['rows'].pop())
    checks=[]
    for name,original,changed in bad:
        for which in ('primary','independent'):
            try:
                if which=='primary':assert changed==original
                else:validate(changed)
            except (AssertionError,IndexError,KeyError,ValueError):
                checks.append({'case':name,'validator':which,'source_key':original['key'],'corrupt_sha256':digest(changed),'status':'rejected'})
            else:raise AssertionError('accepted corruption '+name+' '+which)
    # A certificate dropping an entire family is not accepted as complete coverage.
    domain={independent.key(p) for p in independent.parameters()}
    removed=sources[('DD','P')]['key']
    try:independent.verify_coverage(domain,domain-{removed})
    except AssertionError:checks.append({'case':'omitted_template_coverage','validator':'independent-domain','status':'rejected','removed_key':removed})
    else:raise AssertionError('coverage control did not trigger')
    control=prism();assert primary.fill(copy.deepcopy(control))==control
    mismatch=None
    for i,(left,right) in enumerate(zip(source['rows'],control['rows'])):
        for j,(a,b) in enumerate(zip(left['cells'],right['cells'])):
            tau=[];v=j
            for _ in range(5):tau.append(v%4);v//=4
            tau=tuple(reversed(tau))
            if len(set(tau))==3 and bool(a)!=bool(b):
                mismatch={'beta_index':i,'tau_index':j,'tau':tau,'source_lifts':a,'prism_lifts':b};break
        if mismatch:break
    assert mismatch,'same Sigma control must differ in R3 support'
    result={'positive_controls':positives,'corruptions':checks,'both_validators_rejections':2*len(bad),
            'coverage_rejections':1,'same_Sigma_different_R3':{'status':'counterexample','Sigma':1023,'source_key':source['key'],'source_sha256':digest(source),'witness':mismatch},
            'minimal_outside_source':'not triggered','all_template_certification':'triggered and holds'}
    return result,control

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result,control=compute()
    target=ROOT/'independent/negative-results.json';cp=ROOT/'independent/prism-control.json.gz'
    if args.write:
        with target.open('xb') as f:f.write(encoded(result))
        with cp.open('xb') as f:f.write(gzip.compress(encoded(control),mtime=0))
    else:
        assert json.loads(target.read_text())==json.loads(encoded(result))
        assert gzip.decompress(cp.read_bytes())==encoded(control)
    print(json.dumps({'status':'PASS','positive_families':5,'rejections':len(result['corruptions']),'same_Sigma_different_R3':'counterexample'},sort_keys=True))
if __name__=='__main__':main()
