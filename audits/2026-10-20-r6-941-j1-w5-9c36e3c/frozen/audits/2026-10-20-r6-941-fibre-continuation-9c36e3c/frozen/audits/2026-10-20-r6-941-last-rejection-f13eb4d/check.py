"""Read-only integrated replay, input custody and exact output seal."""
import argparse,hashlib,json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE='f13eb4d0887d962021992ae7afe3323af4d79cd3'
SCRIPTS=[['J1/check.py'],['J2/check.py'],['B/check.py'],['D/check.py','--negative-controls'],
 ['J1/review_j2.py'],['J2/review_j1.py'],['J2/review_d.py'],['review/review_b.py']]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seal',type=Path,default=HERE/'OUTPUTS.json');args=ap.parse_args()
 manifest=json.loads((HERE/'INPUTS.json').read_text());assert len(manifest)==996
 assert len({r['path'] for r in manifest})==len(manifest)
 routing={'docs/STATUS.md','docs/c5_kempe_guide.md'}
 for rec in manifest:
  rel=Path(rec['path']);assert not rel.is_absolute() and '..' not in rel.parts
  raw=(HERE/'frozen'/rel).read_bytes()
  assert len(raw)==rec['bytes'] and hashlib.sha256(raw).hexdigest()==rec['sha256'],('frozen drift',str(rel))
  if str(rel) not in routing:assert (ROOT/rel).read_bytes()==raw,('historical input drift',str(rel))
 seal=json.loads(args.seal.read_text());assert seal['base']==BASE and seal['main_target']=='OPEN'
 assert seal['source_realized'] is False and seal['smaller_bad_constructed'] is False and seal['new_Lean_theorem'] is False
 def verify():
  for rel,sha in seal['files'].items():
   p=Path(rel);assert not p.is_absolute() and '..' not in p.parts
   assert hashlib.sha256((HERE/p).read_bytes()).hexdigest()==sha,('output drift',rel)
 verify()
 def run(spec):
  ans=subprocess.run([sys.executable,'-B',str(HERE/spec[0]),*spec[1:]],cwd=ROOT,capture_output=True,text=True)
  assert ans.returncode==0,(spec,ans.stdout,ans.stderr)
  return {'command':spec,'exit_code':0,'stdout_sha256':hashlib.sha256(ans.stdout.encode()).hexdigest()}
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,SCRIPTS))
 verify()
 print(json.dumps({'pass':True,'base':BASE,'frozen_inputs':len(manifest),'frozen_drift':0,'historical_input_drift':0,
  'output_drift':0,'checks':results,'main_target':'OPEN','source_realized':False,'smaller_bad_constructed':False,'new_Lean_theorem':False},sort_keys=True))
if __name__=='__main__':main()
