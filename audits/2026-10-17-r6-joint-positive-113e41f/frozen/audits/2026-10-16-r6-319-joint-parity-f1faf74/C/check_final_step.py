#!/usr/bin/env python3
"""Replay the six compulsory actual H rows and the final K=J-v control."""
import argparse
from hashlib import sha256
from pathlib import Path
import json
P=Path(__file__).resolve().parent
# This layer explicitly reuses the already sealed sound necessary-screen engine.
base=json.loads((P/'certificate.json').read_text())
for item in base['outputs']:
 if sha256((P/item['path']).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('prior worker seal changed: '+item['path'])
src=(P/'explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(P/'explore_shared_caps.py'),'exec'))
relation=json.loads((P/'combined-source-exploration.json').read_text())[0]['H_fixed']
rows={tuple('ABCD'.index(c) for c in s) for s in relation}
cases=[];mandatory=[]
for r in sorted(rows):
 stable,rr=fixed(rows-{r});supports=[support(stable,w) for w in ('i','j','u')]
 forced=supports!=[1022,1022,319]
 if forced:mandatory.append(name(r))
 cases.append({'deleted':name(r),'stable_count':len(stable),'stable_supports':supports,'mandatory':forced,'rounds':rr})
# K's engine is a distinct quadrilateral boundary computation with actual mz/zpq.
qs=(P/'explore_quadrilateral.py').read_text()
ns={'__file__':str(P/'explore_quadrilateral.py')}
exec(compile(qs.split('base=json.loads')[0],str(P/'explore_quadrilateral.py'),'exec'),ns)
kk={ns['toK'](r) for r in rows if r[1]==r[5]}
kl,kr=ns['fixedK'](kk)
want=['ABACDBCD','ABACDBDC','ABCADBCD','ABCADBDC','ABCDABCD','ABCDABDC']
if mandatory!=want:raise ValueError('compulsory row result changed')
if len(kk)!=34 or kl!=kk:raise ValueError('K screen result changed')
if not all(len(set(r[1:5]))==4 for r in rows if name(r) in mandatory):raise ValueError('a compulsory row has a v lift')
out={'pins':['z','s','j','i','w','t','p','q'],'input_rows':relation,'required_supports':[1022,1022,319],'single_row_deletions':cases,'mandatory_rows':mandatory,'all_mandatory_rows_have_empty_v_lifts':True,'K_pins':['m','j','i','w','z','p','q'],'K_boundary':['m','j','i','w'],'K_edges':ns['EDGES_K'],'K_full_necessary_rows':[name(r) for r in sorted(kl)],'K_rounds':kr,'source_instances':0,'source_coverage':'not triggered','v5_exclusion':'OPEN','complete319':'OPEN'}
ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
if args.check:
 if json.loads(args.check.read_text())!=json.loads(json.dumps(out)):raise ValueError('final-step certificate differs from recomputation')
 print(json.dumps({'status':'PASS','mandatory_rows':6,'actual_K_slice_necessary_rows':34,'K_removed':0,'v5_exclusion':'OPEN'}))
elif args.output:
 with args.output.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
else:print(json.dumps(out,indent=2))
