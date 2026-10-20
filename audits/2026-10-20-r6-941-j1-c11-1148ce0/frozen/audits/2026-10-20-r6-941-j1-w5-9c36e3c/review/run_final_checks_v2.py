from pathlib import Path
import gzip,hashlib,json,os,subprocess
D=Path(__file__).resolve().parent
cases=[('check.py',['--certificate',str(D/'final-negative-relation.json')]),('check_interface.py',['--source',str(D/'final-negative-interface.json.gz')]),('chord_check.py',['--certificate',str(D/'final-negative-chord.json')]),('diamond_check.py',['--certificate',str(D/'final-negative-diamond.json.gz')]),('diamond_reduction_check.py',['--certificate',str(D/'final-negative-reduction.json.gz')])]
results=[]
for script,unused in cases:
 for seed in (None,'17'):
  env=os.environ.copy()
  if seed:env['PYTHONHASHSEED']=seed
  q=subprocess.run(['python3','-B',str(D/script)],capture_output=True,text=True,env=env)
  assert q.returncode==0,(script,q.stderr)
  results.append({'script':script,'PYTHONHASHSEED':seed,'exit':q.returncode,'stdout':q.stdout.strip()})
for script,args in cases:
 q=subprocess.run(['python3','-B',str(D/script),*args],capture_output=True,text=True)
 assert q.returncode!=0,script
 results.append({'script':script,'negative_arguments':args,'exit':q.returncode,'last_error':q.stderr.strip().splitlines()[-1]})
with (D/'final-checks.json').open('x') as f:json.dump({'status':'PASS','normal_seed17_runs':10,'rejected_negative_controls':5,'runs':results},f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','normal_seed17_runs':10,'rejected_negative_controls':5}))
