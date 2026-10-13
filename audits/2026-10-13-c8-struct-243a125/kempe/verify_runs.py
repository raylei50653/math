#!/usr/bin/env python3
"""Replay real solver-free checker and require CLI corruption rejection."""
import copy, hashlib, json, os, subprocess, sys, tempfile
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
 records=[];normal=[]
 for seed,name in [(None,'check.log'),('17','check.seed17.log')]:
  env=os.environ.copy()
  if seed:env['PYTHONHASHSEED']=seed
  cmd=[sys.executable,'-B',str(HERE/'checker.py'),'--negative-controls']
  r=subprocess.run(cmd,text=True,capture_output=True,env=env)
  (HERE/name).write_text(r.stdout+r.stderr)
  assert r.returncode==0,r.stderr
  normal.append(r.stdout);records.append({'command':cmd,'hash_seed':seed,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
 assert normal[0]==normal[1]
 cert=json.loads((HERE/'certificate.json').read_text())
 with tempfile.TemporaryDirectory(prefix='c8-struct-kempe-controls-') as tmp:
  for kind in ('count','name'):
   value=copy.deepcopy(cert)
   if kind=='count':
    q=value['queries'][0];j,v=q['orbit_coefficients'][0];q['orbit_coefficients'][0]=[j,str(Fraction(v)+1)]
   else:value['queries'][0]['boundary_order'].reverse()
   path=Path(tmp)/(kind+'.json');path.write_text(json.dumps(value))
   cmd=[sys.executable,'-B',str(HERE/'checker.py'),'--certificate',str(path)]
   r=subprocess.run(cmd,text=True,capture_output=True)
   assert r.returncode!=0,'checker accepted '+kind
   (HERE/('negative.cli.'+kind+'.log')).write_text(r.stdout+r.stderr)
   records.append({'control':kind,'exit_code':r.returncode,'stderr_last_line':r.stderr.strip().splitlines()[-1]})
 result={'status':'PASS','normal_seed17_byte_equal':True,'runs':records}
 (HERE/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
