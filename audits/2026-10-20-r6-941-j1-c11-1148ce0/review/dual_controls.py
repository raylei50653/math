#!/usr/bin/env python3
"""Regenerate independent model once and reject substantive integer corruptions."""
from pathlib import Path
import importlib.util,json,os
D=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('independent_dual',D/'dual_check.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
source=D.parent/'geometry/orbit-farkas-certificate.json'
normal=m.verify(source)
source_json=json.loads(source.read_text())
def drop_active_equation(c):
 i=next(i for i,(r,v) in enumerate(c['equality_multipliers']) if v==-1)
 del c['equality_multipliers'][i]
def enlarge_positive(c):
 c['positive_row_multipliers']=[[9,17]];c['positive_weight_sum']=17
def omit_zero_equations(c):
 c['equality_multipliers']=[row for row in c['equality_multipliers'] if row[1]!=8]
def signed_span_error(c):
 c['equality_multipliers'].append([22143,1])
checks=[]
for name,mut in [('drop-active-halfrow',drop_active_equation),('excess-witness-weight',enlarge_positive),('omit-zero-halfrows',omit_zero_equations),('uncancelled-signed-span',signed_span_error)]:
 cert=json.loads(json.dumps(source_json));mut(cert);path=D/f'dual-negative-{name}.json'
 with path.open('x') as dst:json.dump(cert,dst,separators=(',',':'));dst.write('\n')
 rejected=False;message=''
 try:m.verify(path)
 except AssertionError as err:rejected=True;message=str(err)
 assert rejected,name
 checks.append({'name':name,'rejected':True,'reason':message})
 print(json.dumps(checks[-1]),flush=True)
out={'independent_normal':normal,'negative_controls':checks,'all_passed':True,'python_hash_seed':os.environ.get('PYTHONHASHSEED')}
with (D/'dual-checks.json').open('x') as dst:json.dump(out,dst,indent=2);dst.write('\n')
print(json.dumps({'all_passed':True,'negative_controls':len(checks)}),flush=True)
