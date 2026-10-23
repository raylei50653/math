"""Save isolated read-only replay receipts; never regenerate evidence in place."""
import concurrent.futures,copy,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def write(path,obj):
 with path.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2);f.write('\n')
def main():
 run_dir=HERE/'runs-v2';negative_dir=HERE/'negative-inputs-v2'
 run_dir.mkdir();negative_dir.mkdir()
 cert=json.loads((HERE/'certificate.json').read_text())
 jobs=[('normal',[],{},0),('seed17',['--seed','17'],{'PYTHONHASHSEED':'17'},0),('negative',['--negative'],{},0)]
 mutations=[
  ('missing-frame',lambda x:x['contract'].pop('same_rotation_attachments_B14_literal_frame')),
  ('missing-alias-context',lambda x:x['source_star_contexts'].pop(1)),
  ('invent-source',lambda x:x['boundaries'].update(source_realizability='triggered and holds')),
  ('corrupt-full-lift',lambda x:next(r for r in x['caps'][0]['complete_fibres'] if r['full_lifts'])['full_lifts'][0].__setitem__(0,3)),
  ('corrupt-quotient',lambda x:x['caps'][0]['safe_candidates'][0]['port_map'].__setitem__(0,7)),
  ('erase-residual',lambda x:x['caps'][0].update(residual_accepting_words=[]))]
 for name,mutate in mutations:
  bad=copy.deepcopy(cert);mutate(bad);p=negative_dir/f'{name}.json';write(p,bad)
  jobs.append(('external-'+name,['--certificate',str(p)],{},1))
 def run(job):
  name,args,env,expected=job
  cmd=[sys.executable,'-B']+(['-O'] if name=='seed17' else [])+[str(HERE/'check.py')]+args
  started=time.monotonic();r=subprocess.run(cmd,env={**os.environ,**env},capture_output=True,text=True)
  for suffix,body in [('stdout',r.stdout),('stderr',r.stderr)]:
   with (run_dir/f'{name}.{suffix}').open('x') as f:f.write(body)
  expected_reason={'external-missing-frame':'same-source/same-H contract','external-missing-alias-context':'domain incomplete',
   'external-invent-source':'authority boundary','external-corrupt-full-lift':'complete seven-point lift',
   'external-corrupt-quotient':'actual quotient graph','external-erase-residual':'residual accepting witness'}.get(name)
  reason_match=expected_reason is None or expected_reason in r.stdout
  receipt=dict(name=name,command=cmd,environment=env,expected_exit=expected,exit_code=r.returncode,seconds=round(time.monotonic()-started,3),expected_rejection_reason=expected_reason,passed=r.returncode==expected and reason_match)
  print(name,'PASS' if receipt['passed'] else 'FAIL',flush=True);return receipt
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(run,jobs))
 normal=json.loads((run_dir/'normal.stdout').read_text());seed=json.loads((run_dir/'seed17.stdout').read_text());normal.pop('seed',None);seed.pop('seed',None)
 require_same=normal==seed
 result=dict(status='PASS' if all(r['passed'] for r in receipts) and require_same else 'FAIL',normal_seed17_equal_except_seed=require_same,
  semantic_negative_count=len(json.loads((run_dir/'negative.stdout').read_text()).get('negative_controls',[])),external_negative_count=len(mutations),runs=receipts)
 write(HERE/'VERIFICATION.json',result)
 if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
