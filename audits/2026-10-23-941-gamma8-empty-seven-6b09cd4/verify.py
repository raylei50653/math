#!/usr/bin/env python3
"""Exclusive-create normal, seed17, semantic and external corruption receipts."""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(value,f,sort_keys=True,ensure_ascii=False,indent=2);f.write('\n')
def run(name,extra=(),seed17=False):
 command=[sys.executable,'-B']+(['-O'] if seed17 else [])+[str(HERE/'check.py')]+list(extra)
 env=dict(os.environ)
 if seed17:env['PYTHONHASHSEED']='17'
 result=subprocess.run(command,cwd=HERE.parents[1],env=env,text=True,capture_output=True)
 record=dict(command=command,PYTHONHASHSEED='17' if seed17 else env.get('PYTHONHASHSEED'),returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)
 write(HERE/'runs'/f'{name}.json',record)
 return record
def main():
 normal=run('normal');seed17=run('seed17',['--seed','17'],True);negative=run('semantic-negative',['--negative'])
 if any(r['returncode']!=0 for r in [normal,seed17,negative]):raise ValueError('positive/semantic replay failed')
 a=json.loads(normal['stdout']);b=json.loads(seed17['stdout']);a.pop('seed');b.pop('seed')
 if a!=b:raise ValueError('normal/seed17 evidence differs')
 c=json.loads((HERE/'certificate.json').read_text());external=[]
 for name,change in [
  ('corrupt-empty-fibre',lambda d:d['complete_retained_K6_relation']['relations'].pop()),
  ('corrupt-K8-promotion',lambda d:d['boundaries'].__setitem__('paper_D6_bothK_K8','excluded')),
 ]:
  bad=copy.deepcopy(c);change(bad);path=HERE/'negative-inputs'/f'{name}.json';write(path,bad)
  record=run(name,['--certificate',str(path)])
  if record['returncode']==0:raise ValueError('external corruption accepted '+name)
  external.append(dict(name=name,returncode=record['returncode'],certificate=str(path.relative_to(HERE))))
 receipts=[]
 for p in sorted((HERE/'runs').glob('*.json')):
  raw=p.read_bytes();receipts.append(dict(path=str(p.relative_to(HERE)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 write(HERE/'VERIFICATION.json',dict(status='PASS',normal_seed17_semantic_outputs_match=True,semantic_controls_rejected=len(json.loads(negative['stdout'])['negative_controls_rejected']),external_controls=external,source_realizability='not triggered',receipts=receipts))
if __name__=='__main__':main()
