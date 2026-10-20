#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('dual',D/'dual_check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
base=json.loads((D.parent/'geometry/orbit-farkas-certificate.json').read_text())
def flip(c):
 row=next(row for row in c['equality_multipliers'] if row[1]==-1);row[1]=1
def drop(c):c['positive_row_multipliers']=[];c['positive_weight_sum']=0
def omit(c):c['nonnegative_slacks'].pop()
checks=[]
for name,fn in [('flip-live-multiplier',flip),('drop-positive-witness',drop),('omit-orbit-slack',omit)]:
 c=json.loads(json.dumps(base));fn(c);p=D/f'dual-negative-{name}.json'
 with p.open('x') as dst:json.dump(c,dst,separators=(',',':'));dst.write('\n')
 rejected=False;reason=''
 try:m.verify(p)
 except AssertionError as err:rejected=True;reason=str(err)
 assert rejected,name
 checks.append({'name':name,'rejected':True,'reason':reason});print(json.dumps(checks[-1]),flush=True)
with (D/'dual-requested-checks.json').open('x') as dst:json.dump({'all_passed':True,'negative_controls':checks},dst,indent=2);dst.write('\n')
