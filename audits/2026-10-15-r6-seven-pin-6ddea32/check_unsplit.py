#!/usr/bin/env python3
"""Supplement: enumerate the invalid extra requirement that both z copies connect."""
import argparse,hashlib,itertools,json
from pathlib import Path
import check as base
HERE=Path(__file__).resolve().parent

def unsplit_options(row,pairing):
 cutrow=tuple(row[v] for v in base.CUT_TO_ORIGINAL);domains=[]
 for pair in pairing:
  vs=tuple(i for i,c in enumerate(cutrow) if c in pair);good=[]
  for part in base.independent_partitions(vs):
   labels={v:i for i,b in enumerate(part) for v in b}
   if 0 in labels and labels[0]!=labels[5]:continue
   if any(labels[a]!=labels[b] for a,b in base.CUT_EDGES if a in vs and b in vs):continue
   good.append(part)
  domains.append(good)
 result=set()
 for a,b in itertools.product(*domains):
  if not base.crossing(a+b,8):result.add((base.project(a),base.project(b)))
 return result

def build():
 base.custody();h=base.h
 rows=sorted({h.canonical(r) for r in itertools.product(range(4),repeat=7)
              if all(r[a]!=r[b] for a,b in h.EDGES)})
 cases=[];removed=0
 for row in rows:
  for pairing in h.PAIRINGS:
   old={tuple(base.norm(x) for x in parts) for parts,orb in h.options(row,pairing,h.EDGES)}
   strict=unsplit_options(row,pairing)
   base.need(strict<=old,'unsplit unexpectedly adds partitions')
   diff=old-strict;removed+=len(diff)
   if diff:cases.append({'row':h.name(row),'pairing':pairing,'removed_partitions':sorted(diff)})
 named=next(c for c in cases if c['row']=='ABABCBC' and c['pairing']==((0,1),(2,3)))
 parts=(((0,1,2,3,5),),((4,6),))
 base.need(parts in named['removed_partitions'],'named unsplit countercontrol absent')
 joined=((0,1,2,3,5,6),(4,7))
 base.need(base.crossing(joined,8) is not None,'joined witness not crossing')
 return {'schema':'unsplit-z-shortcut-negative-v1','main_checker_sha256':base.digest(HERE/'check.py'),
  'checker_sha256':base.digest(Path(__file__)),'proper_rows':len(rows),
  'cases_with_rejections':cases,'total_rejected_options':removed,
  'named_negative':{'row':'ABABCBC','pairing':((0,1),(2,3)),
   'old_partition':parts,'only_unsplit_partition':joined,'alternating_positions':(3,4,5,7)},
  'scope':'finite false shortcut test; no graph realization claimed for abstract partitions'}
def main():
 p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
 m.add_argument('--write',action='store_true');m.add_argument('--check',action='store_true')
 p.add_argument('--certificate',type=Path,default=HERE/'unsplit-certificate.json');a=p.parse_args()
 data=build();payload=json.dumps(data,indent=2)+'\n'
 if a.write:
  with a.certificate.open('x') as f:f.write(payload)
 else:base.need(a.certificate.read_text()==payload,'unsplit certificate differs')
 print(json.dumps({'status':'PASS false shortcut identified','rejected_old_options':data['total_rejected_options'],
  'affected_row_pairings':len(data['cases_with_rejections'])},sort_keys=True))
if __name__=='__main__':main()
