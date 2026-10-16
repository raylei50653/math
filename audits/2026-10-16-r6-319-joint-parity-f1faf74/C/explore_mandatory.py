from pathlib import Path
src=Path(__file__).with_name('explore_shared_caps.py').read_text()
exec(compile(src.split('upper={')[0],str(Path(__file__).with_name('explore_shared_caps.py')),'exec'))
base=json.loads((P/'combined-source-exploration.json').read_text())[0]
rows={tuple('ABCD'.index(c) for c in s) for s in base['H_fixed']}
mandatory=[];optional=[]
for row in sorted(rows):
 live,rr=fixed(rows-{row})
 supports=[support(live,w) for w in ('i','j','u')]
 if supports!=[1022,1022,319]:mandatory.append(name(row))
 else:optional.append({'absent':name(row),'remaining':len(live)})
print('mandatory',len(mandatory),mandatory)
print('optional',len(optional),optional)
(P/'mandatory-exploration.json').write_text(json.dumps({'mandatory':mandatory,'optional':optional},indent=2)+'\n')
