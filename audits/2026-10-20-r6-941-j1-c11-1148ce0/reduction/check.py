#!/usr/bin/env python3
"""Readonly replay of the exact bounded two-hole searches; no source exclusion."""
from pathlib import Path
import argparse,gzip,json
import full_left,full_right_contractions,full_joint_supports
D=Path(__file__).resolve().parent
def stable(x):
 x=dict(x);x.pop('seconds',None);return json.loads(json.dumps(x,sort_keys=True))
def compute():
 left,counts=full_left.left_relations()
 assert json.loads(json.dumps(left,sort_keys=True))==json.load(gzip.open(D/'full-left-relations.json.gz','rt'))
 right=full_right_contractions.compute();joint=full_joint_supports.compute()
 assert stable(right)==stable(json.loads((D/'full-right-contractions.json').read_text()))
 assert stable(joint)==stable(json.loads((D/'full-joint-supports.json').read_text()))
 assert len(left)==256 and counts=={0:42,1:330,2:4620}
 assert right['right_relations']==82 and not right['hits']
 assert joint['strict_candidate_pairs']==14656 and joint['maximal_mask_not_K132_count']==0
 return {'source_live':5951,'left_relations':256,'right_relations':82,'strict_candidate_pairs':14656,'hits':0,'all_maximal_masks_in_K132':True,'source_excluded':False,'smaller_bad_constructed':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--summary',type=Path);a=ap.parse_args();out=compute()
 if a.summary:assert json.loads(a.summary.read_text())==out
 print(json.dumps(out,sort_keys=True))
