#!/usr/bin/env python3
"""Literal graph calibrations and destructive-certificate controls in temporary files."""
import contextlib,io,itertools,json,shutil,tempfile
from pathlib import Path
import check
HERE=Path(__file__).resolve().parent

def normalize_edge(u,v):return tuple(sorted((u,v)))

def graph_count(edges, fixed, internal):
 total=0
 for colors in itertools.product(range(4),repeat=len(internal)):
  assignment=dict(fixed);assignment.update(zip(internal,colors))
  total+=all(assignment[u]!=assignment[v] for u,v in edges)
 return total

def main():
 # W8 is a finite planar calibration for the lemma, not a target source.
 cycle={normalize_edge(i,(i+1)%8) for i in range(8)}
 wheel=cycle|{(i,8) for i in range(8)}
 contexts=0;nonzero=0;tight_nonzero=0
 for rest in itertools.product(range(4),repeat=7):
  fixed=dict(zip(range(1,8),rest))
  if fixed[1]!=fixed[7] or any(fixed[i]==fixed[i+1] for i in range(1,7)):continue
  contexts+=1;c=fixed[1];options=[i for i in range(4) if i!=c]
  counts=[graph_count(wheel,dict(fixed,**{})|{0:i},[8]) for i in options]
  z={d:graph_count({e for e in wheel if 0 not in e},fixed|{8:d},[]) for d in range(4)}
  assert z[c]==0
  assert all(counts[i]==sum(z[d] for d in options if d!=color) for i,color in enumerate(options))
  assert all(2*x<=sum(counts) for x in counts)
  nonzero+=sum(counts)>0;tight_nonzero+=sum(counts)>0 and any(2*x==sum(counts) for x in counts)
 assert contexts==732 and nonzero>0 and tight_nonzero>0
 # Split-center planar triangulated C8: vertex0 has degree4 and a singleton fibre.
 split=cycle|{normalize_edge(8,i) for i in [0,1,2,3,4]}|{normalize_edge(9,i) for i in [4,5,6,7,0]}|{(8,9)}
 fixed=dict(zip(range(1,8),[0,1,2,0,1,3,0]))
 values=[graph_count(split,fixed|{0:c},[8,9]) for c in [1,2,3]]
 assert values==[1,0,0] and sum(0 in e for e in split)==4
 negatives=[]
 with tempfile.TemporaryDirectory(prefix='c8-apex-controls-') as td:
  temp=Path(td)
  for name in ['dual-c04-a1.json','dual-c07-a4.json']:shutil.copyfile(HERE/name,temp/name)
  cert=json.loads((HERE/'certificate.json').read_text());cert['queries'][0]['apex_position']+=1;(temp/'certificate.json').write_text(json.dumps(cert))
  try:
   with contextlib.redirect_stdout(io.StringIO()):check.check(certificate_path=temp/'certificate.json')
  except AssertionError:negatives.append('changed named apex position rejected')
  else:raise AssertionError('corrupt certificate accepted')
  name='dual-c04-a1.json';d=json.loads((temp/name).read_text());d['degree3_dual'][0][2]='-1';(temp/name).write_text(json.dumps(d))
  try:
   with contextlib.redirect_stdout(io.StringIO()):check.check(dual_dir=temp)
  except AssertionError:negatives.append('negative degree3 inequality multiplier rejected')
  else:raise AssertionError('negative degree3 multiplier accepted')
  d=json.loads((HERE/name).read_text());d['normalizer_dual'].pop();(temp/name).write_text(json.dumps(d))
  try:
   with contextlib.redirect_stdout(io.StringIO()):check.check(dual_dir=temp)
  except AssertionError:negatives.append('deleted exact normalizer coefficient rejected')
  else:raise AssertionError('missing normalizer coefficient accepted')
 out={'degree3_W8_control':{'status':'triggered and holds','literal_contexts':contexts,'nonzero_contexts':nonzero,'nonzero_tight_contexts':tight_nonzero},'degree4_weakened_claim':{'status':'counterexample','fixed_boundary_except_v0':[None,0,1,2,0,1,3,0],'v0_color_order':[1,2,3],'complete_extension_counts':values,'edges':sorted(map(list,split))},'certificate_negative_controls':negatives,'actual_minimal_target_source':'not triggered'}
 (HERE/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: literal W8 calibration, degree4 weakened-claim counterexample, 3 certificate negative controls')
if __name__=='__main__':main()
