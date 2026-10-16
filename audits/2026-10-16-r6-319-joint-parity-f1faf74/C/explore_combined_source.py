from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
F=json.loads((P/'full-source-exploration.json').read_text())
base=json.loads((P/'shared-caps-exploration.json').read_text())
results=[]
for ff in F['results']:
 h={canon(tuple('ABCD'.index(c) for c in (s[:6]+s[7:]))) for s in ff['fixed_rows'] if s[0]==s[6]}
 live,rr=fixed(h)
 print('source',ff['source_mask'],'H',len(h),'fixed',len(live),[support(live,w) for w in ('i','j','u')],rr,flush=True)
 survivors=[]
 for mi,mj in product(*base['cap_candidates']):
  good,r2=fixed({r for r in live if projection(r,'i')&~mi==0 and projection(r,'j')&~mj==0})
  ss=[support(good,w) for w in ('i','j','u')]
  if ss==[mi,mj,319]:survivors.append({'caps':[mi,mj],'rows':[name(r) for r in sorted(good)]})
 print('survivors',[(d['caps'],len(d['rows'])) for d in survivors],flush=True)
 results.append({'source':ff['source_mask'],'H_upper':[name(r) for r in sorted(h)],'H_fixed':[name(r) for r in sorted(live)],'rounds':rr,'survivors':survivors})
out=results
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path)
a=ap.parse_args()
if a.check:
 if json.loads(a.check.read_text())!=json.loads(json.dumps(out)):raise ValueError('certificate differs from exhaustive recomputation')
 print('certificate verified')
elif a.output:
 with a.output.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')

