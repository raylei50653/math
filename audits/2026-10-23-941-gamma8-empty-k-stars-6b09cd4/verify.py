#!/usr/bin/env python3
"""Write exclusive normal/shuffled/negative and external-corruption receipts."""
import concurrent.futures,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def write(p,v):
 with p.open('x') as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def run(name,args,expected=0,seed17=False):
 env=dict(os.environ)
 if seed17:env['PYTHONHASHSEED']='17'
 start=time.monotonic();p=subprocess.run([sys.executable,'-B',*(['-O'] if seed17 else []),str(HERE/'check.py'),*args],capture_output=True,text=True,env=env)
 for suffix,data in [('stdout',p.stdout),('stderr',p.stderr)]:
  with (HERE/'runs'/f'{name}.{suffix}').open('x') as f:f.write(data)
 if p.returncode!=expected:raise ValueError(f'{name}: exit {p.returncode}, wanted {expected}; {p.stderr[-1000:]}')
 if expected==0:
  result=json.loads(p.stdout)
  if result['status']!='PASS':raise ValueError(name+' no PASS')
 return dict(name=name,command=[sys.executable,'-B',*(['-O'] if seed17 else []),str(HERE/'check.py'),*args],returncode=p.returncode,expected_returncode=expected,seconds=round(time.monotonic()-start,3),status='PASS')
def main():
 (HERE/'runs').mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  jobs=[pool.submit(run,'normal',[]),pool.submit(run,'seed17',['--seed','17'],0,True),pool.submit(run,'negative',['--negative'])]
  receipts=[j.result() for j in jobs]
 c=json.loads((HERE/'certificate.json').read_text());c['cap_substitutions'].pop();write(HERE/'runs/corrupted-certificate.json',c)
 with (HERE/'runs/malformed-certificate.json').open('x') as f:f.write('{"schema":')
 for name in ['corrupted','malformed']:receipts.append(run('external-'+name,['--certificate',str(HERE/'runs'/f'{name}-certificate.json')],1))
 hashes=[]
 for p in sorted(HERE.rglob('*')):
  if p.is_file() and p.name not in {'VERIFICATION.json','FINAL_MANIFEST.json'}:
   b=p.read_bytes();hashes.append(dict(path=str(p.relative_to(HERE)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 write(HERE/'VERIFICATION.json',dict(schema='941-empty-k-verification-v1',status='PASS',receipts=receipts,semantic_negative_controls=10,external_negative_controls=2,artifact_hashes=hashes))
 print('normal / seed17 / 10 semantic / 2 external controls PASS')
if __name__=='__main__':main()
