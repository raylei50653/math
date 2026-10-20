from pathlib import Path
import gzip,hashlib,json,os,subprocess
D=Path(__file__).resolve().parent
cases=[]
# Complete relation: filling one empty fibre must fail exact comparison.
a=json.loads((D/'certificate.json').read_text());a['records'][0]['all_p_h_R_lifts']=[[0,0,0]]
p=D/'final-negative-relation.json'
with p.open('x') as f:json.dump(a,f,sort_keys=True);f.write('\n')
cases.append(('check.py',['--certificate',str(p)]))
# Complete cap: a spurious right lift must be rejected before any inference.
a=json.load(gzip.open(D.parent/'interface/certificate-v4.json.gz','rt'));a['caps'][0]['right_xyr'].append([0,0,0]);p=D/'final-negative-interface.json.gz'
with p.open('xb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(a,sort_keys=True).encode())
cases.append(('check_interface.py',['--source',str(p)]))
a=json.loads((D/'chord-check.json').read_text());a['source_excluded']=True;p=D/'final-negative-chord.json'
with p.open('x') as f:json.dump(a,f,sort_keys=True);f.write('\n')
cases.append(('chord_check.py',['--certificate',str(p)]))
a=json.load(gzip.open(D/'diamond-certificate-v2.json.gz','rt'));a['source_excluded']=True;p=D/'final-negative-diamond.json.gz'
with p.open('xb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(a,sort_keys=True).encode())
cases.append(('diamond_check.py',['--certificate',str(p)]))
a=json.load(gzip.open(D/'diamond-reduction-certificate.json.gz','rt'));a['full_W5_branch_excluded']=True;p=D/'final-negative-reduction.json.gz'
with p.open('xb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(a,sort_keys=True).encode())
cases.append(('diamond_reduction_check.py',['--certificate',str(p)]))
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
