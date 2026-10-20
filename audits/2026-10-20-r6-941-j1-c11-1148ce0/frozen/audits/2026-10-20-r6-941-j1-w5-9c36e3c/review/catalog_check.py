#!/usr/bin/env python3
"""Check that the four-row certificate is disjoint from the frozen K132 table."""
from pathlib import Path
import argparse,hashlib,json
D=Path(__file__).resolve().parent
P=D.parent/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
def compute():
 raw=P.read_bytes();d=json.loads(raw);assert tuple(''.join(map(str,r)) for r in d['pattern_order'])==ROWS
 masks=sorted(map(int,d['cells']));assert len(masks)==d['distinct_sigma']==132
 matches=[m for m in masks if m&(1<<9) and not any(m&(1<<j) for j in (1,4,6))];assert not matches
 return {'status':'PASS','frozen_catalogue_sha256':hashlib.sha256(raw).hexdigest(),'K132_count':len(masks),'same_original_pattern_order':ROWS,'required_positive_bit':9,'required_zero_bits':[1,4,6],'matching_K132_masks':matches,'consequence':'The verified n=5 candidate has support outside K132; the inherited global minimality forces every strictly smaller legal C5 disk into K132.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--certificate',type=Path,default=D/'catalog-check.json');a=p.parse_args();out=json.loads(json.dumps(compute()))
 if a.build:
  with a.certificate.open('x') as f:json.dump(out,f,sort_keys=True,indent=2);f.write('\n')
 else:assert json.loads(a.certificate.read_text())==out
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
