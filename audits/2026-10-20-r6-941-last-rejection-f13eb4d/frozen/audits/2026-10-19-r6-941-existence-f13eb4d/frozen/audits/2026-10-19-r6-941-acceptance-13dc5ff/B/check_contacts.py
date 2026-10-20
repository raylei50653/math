#!/usr/bin/env python3
"""Rebuild a complete necessary envelope of private contacts to the original C10."""
import argparse,copy,hashlib,itertools,json
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
PINS=('a','n','R','L','q','c','s','v','w','t')
MINDEG=(3,3,4,4,3,3,4,4,4,4)
INPUTS=(D/'certificate.json',D.parent/'D/certificate.json',ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/SOURCE_CONTRACT.md',ROOT/'audits/2026-10-19-r6-941-quotients-13dc5ff/B/CHORDS.md')

def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS}

def compute():
 seal=json.loads((D/'CONTACT_INPUTS.json').read_text());assert seal==hashes(),'same B/D branch proofs and frozen source inputs'
 b=json.loads(INPUTS[0].read_text());d=json.loads(INPUTS[1].read_text())
 assert b['n5_a6_exclusion']['source_alpha_zero'] and b['n5_a6_exclusion']['source_projection_upper_mask']==429
 assert all(b['literal_source_count_matrix'][9][i]==0 for i in b['n5_a6_exclusion']['live'])
 assert d['q6_c5_exclusion']['original_support_upper']==429 and not d['q6_c5_exclusion']['original_alpha_cells']
 allowed=[];records=[]
 for mask in range(1<<10):
  s={i for i in range(10) if mask>>i&1};violations=[]
  if {0,5}<=s:violations.append({'rule':'nonadjacent-original-B-contacts','pair':['a','c']})
  for i in range(10):
   if i in s and (i+2)%10 in s:
    mid=(i+1)%10
    if MINDEG[mid]>=4:violations.append({'rule':'C4-empty-pocket-high-middle','arc':[PINS[i],PINS[mid],PINS[(i+2)%10]]})
    elif mid not in s:violations.append({'rule':'C4-forced-middle-contact','arc':[PINS[i],PINS[mid],PINS[(i+2)%10]]})
   if i in s and (i+3)%10 in s:
    arc=[PINS[(i+k)%10] for k in range(4)]
    if i==9:reason='B-n5-a6-exclusion'
    elif i==3:reason='D-q6-c5-exclusion'
    else:
     assert any(MINDEG[(i+k)%10]>=4 for k in (1,2));reason='C5-empty-or-W5-high-middle'
    violations.append({'rule':reason,'arc':arc})
  entries=[PINS[i] for i in range(10) if i in s]
  if not violations:allowed.append(entries)
  records.append({'contacts':entries,'necessary_allowed':not violations,'violations':violations})
 counts={str(k):v for k,v in sorted(Counter(map(len,allowed)).items())}
 four=[s for s in allowed if len(s)==4]
 assert counts=={'0':1,'1':10,'2':24,'3':20,'4':5}
 assert four==[['a','n','R','s'],['n','R','s','v'],['R','L','v','w'],['L','q','c','t'],['L','q','w','t']]
 return {'original_core_order':list(PINS),'original_core_minimum_degrees':list(MINDEG),
 'input_hashes':seal,'complete_contact_subsets':records,'allowed_by_cardinality':counts,
 'allowed_four_contact_sets':four,'all_original_distance_two_or_three_pairs_at_least_three':[['t','R'],['L','s']],
 'private_vertex_contact_upper_bound':4,'source_realizations_asserted':False,'main_target_closed':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'contacts.json');args=ap.parse_args()
 if args.build:
  with (D/'CONTACT_INPUTS.json').open('x') as out:json.dump(hashes(),out,sort_keys=True,indent=2);out.write('\n')
 expected=compute()
 if args.build:
  with args.certificate.open('x') as out:json.dump(expected,out,ensure_ascii=False,separators=(',',':'));out.write('\n')
 assert json.loads(args.certificate.read_text())==expected,'all 1024 complete private contact subsets'
 tests=[]
 for label,mutate in (
  ('drop-empty-contact-fibre',lambda z:z['complete_contact_subsets'].pop(0)),
  ('allow-a-six-n-five-pocket',lambda z:z['complete_contact_subsets'][sum(1<<i for i in (2,9))].__setitem__('necessary_allowed',True)),
  ('forget-W5-compatible-degree-three',lambda z:z['original_core_minimum_degrees'].__setitem__(0,4)),
  ('claim-every-necessary-contact-set-realized',lambda z:z.__setitem__('source_realizations_asserted',True))):
  wrong=copy.deepcopy(expected);mutate(wrong)
  assert wrong!=expected;tests.append(label)
 print(json.dumps({'pass':True,'complete_subsets':1024,'necessary_allowed_subsets':60,'maximum_private_contacts':4,
 'four_contact_sets':expected['allowed_four_contact_sets'],'negative_controls_rejected':tests,
 'source_realizations_asserted':False,'main_target':'OPEN'},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
