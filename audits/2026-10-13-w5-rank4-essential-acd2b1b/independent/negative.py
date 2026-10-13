#!/usr/bin/env python3
"""Read-only corrupted-record controls for both full validators."""
import copy,gzip,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def imp(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=imp('primary',ROOT/'controls/check.py');i=imp('independent',ROOT/'independent/check.py')

def primary(g):
 r,d,f,w=g['key'].split(':');r,d,f=int(r),int(d),int(f)
 assert 8<=r<=13 and d in (0,1) and f in (0,1)
 assert w in set(p.words(r,d))
 expected=p.old.fill(p.graph(r,d,f,w))
 assert g==expected,'complete original graph or full-lift record mismatch'

def mutate(g,kind):
 if kind=='missing_original_edge':g['edges'].pop()
 elif kind=='wrong_pin':g['U'][0],g['U'][1]=g['U'][1],g['U'][0]
 elif kind=='reverse_U_face':g['faces'][-1].reverse()
 elif kind=='wrong_rotation':g['rotation'][10].reverse()
 elif kind=='wrong_rank':g['counts']['rho']=3
 elif kind=='wrong_private_degree':g['degree_F'][0]+=1
 elif kind=='wrong_full_degree':g['degree_G'][10]+=1
 elif kind=='wrong_owner':g['ownership']['short_ring']='U' if g['ownership']['short_ring']=='B' else 'B'
 elif kind=='wrong_degree_flag':g['source_degree_flags']['B_ge4']=not g['source_degree_flags']['B_ge4']
 elif kind=='missing_row':g['rows'].pop()
 elif kind=='missing_A_lift':
  next(c for row in g['rows'] for c in row['cells'] if c).pop()
 elif kind=='missing_G_lift':next(row['wheel_full_lifts'] for row in g['rows'] if row['wheel_full_lifts']).pop()
 elif kind=='false_empty_fibre':next(c for row in g['rows'] for c in row['cells'] if c).clear()
 elif kind=='nonempty_empty_fibre':next(c for row in g['rows'] for c in row['cells'] if not c).append('0'*len(g['vertices']))
 else:raise ValueError(kind)


def main():
 controls={}
 with gzip.open(ROOT/'controls/certificate.jsonl.gz','rt') as stream:
  next(stream)
  for line in stream:
   g=json.loads(line);r,d,f,w=g['key'].split(':');controls.setdefault((d,f),g)
   if len(controls)==4:break
 for g in controls.values():primary(g);i.verify(g)
 base=controls[('0','0')]
 kinds=['missing_original_edge','wrong_pin','reverse_U_face','wrong_rotation','wrong_rank','wrong_private_degree','wrong_full_degree','wrong_owner','wrong_degree_flag','missing_row','missing_A_lift','missing_G_lift','false_empty_fibre','nonempty_empty_fibre']
 results=[]
 for kind in kinds:
  g=copy.deepcopy(base);mutate(g,kind)
  for name,validator in [('primary',primary),('independent',i.verify)]:
   try:validator(g)
   except (AssertionError,ValueError,IndexError,KeyError) as e:results.append({'kind':kind,'validator':name,'rejected':True,'reason':str(e)})
   else:raise AssertionError('corruption accepted: '+kind+' '+name)
 domain=i.domains();missing=set(domain);missing.pop()
 try:i.coverage(missing)
 except AssertionError:pass
 else:raise AssertionError('missing template accepted')
 print(json.dumps({'positive_controls':4,'negative_rejections':results,'missing_template_rejected':True,'source_status':'not triggered; controls do not establish source existence'},indent=2,sort_keys=True))
if __name__=='__main__':main()
