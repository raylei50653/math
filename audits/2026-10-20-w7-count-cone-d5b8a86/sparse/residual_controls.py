#!/usr/bin/env python3
"""Negative controls for residual-record accuracy, not feasibility evidence."""
import argparse,copy,gzip,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('artifact',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();original=json.load(gzip.open(a.artifact,'rt'));results=[]
 with tempfile.TemporaryDirectory(prefix='residual-controls-',dir=P) as tmp:
  for name in ('wrong_halfrow_weight','wrong_state_coefficient','omitted_positive_price_column','boolean_dual_coefficient'):
   data=copy.deepcopy(original)
   if name=='wrong_halfrow_weight':data['halfrow_integer_weights'][0][1]+=1
   elif name=='wrong_state_coefficient':
    item=next(x for x in data['state_integer_coefficients'] if x[0]==data['target']);item[1]+=1
   elif name=='omitted_positive_price_column':data['positive_price_columns'].pop()
   else:next(x for x in data['integer_dual_terms'] if x[1]==1)[1]=True
   raw=json.dumps(data,sort_keys=True,separators=(',',':')).encode();path=Path(tmp)/(name+'.json.gz');path.write_bytes(gzip.compress(raw,mtime=0))
   for optimized in (False,True):
    flags=['-O','-B'] if optimized else ['-B']
    cp=subprocess.run([sys.executable,*flags,str(P/'replay_exact_residual.py'),str(path)],text=True,capture_output=True)
    if cp.returncode==0:raise RuntimeError(name+' mutation was accepted under '+str(flags))
    results.append({'control':name,'optimized':optimized,'result':'MUTATED RESIDUAL REJECTED','returncode':cp.returncode,'mutated_payload_sha256':hashlib.sha256(raw).hexdigest(),'last_error_line':cp.stderr.strip().splitlines()[-1]})
 result={'meaning':'these controls only test replay accuracy of an incomplete residual; they provide no cone feasibility verdict','artifact_sha256':hashlib.sha256(a.artifact.read_bytes()).hexdigest(),'controls':results};a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
