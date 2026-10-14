#!/usr/bin/env python3
"""Mutation controls use the same independent certificate validator."""
import json,copy
from pathlib import Path
from independent_verify import check_record,controls
P=Path(__file__).resolve().parent
base=json.loads((P/'twohole_PINCH_0.json').read_text())['records'][0]
bridge=json.loads((P/'twohole_BRIDGE_0.json').read_text())['records'][0]
check_record(base);check_record(bridge)
results={}
def must_reject(name,record,mutate):
 x=copy.deepcopy(record);mutate(x)
 try:check_record(x)
 except (AssertionError,KeyError,ValueError):results[name]='REJECTED'
 else:raise AssertionError('corruption accepted: '+name)
def flip_matrix(x):x['matrix'][0][0]^=1
def drop_rectangle(x):x['rectangles'].pop()
def false_prune(x):x['rectangles'][0][2]^=1
def false_coverage(x):x['rectangles'][0][4]=x['target'];x['rectangles'][0][5]=0
def wrong_order(x):x['interfaces'][0][1],x['interfaces'][0][2]=x['interfaces'][0][2],x['interfaces'][0][1]
def omit_bridge(x):x['edges'].remove(['x','y'])
def split_shared(x):x['interfaces'][1][0]='split_x'
def wrong_count(x):x['shell_lift_counts'][0]+=1
for name,record,fn in [
 ('changed_outer_row_mask',base,flip_matrix),('omitted_maximal_rectangle',base,drop_rectangle),
 ('corrupt_pruned_support',base,false_prune),('fabricated_target_coverage',base,false_coverage),
 ('reordered_original_interface',base,wrong_order),('removed_original_bridge',bridge,omit_bridge),
 ('split_shared_original_vertex',base,split_shared),('changed_full_lift_count',base,wrong_count)]:
 must_reject(name,record,fn)
out={'negative_controls':results,'positive_actual_disk_controls':controls(),'status':'PASS'}
(P/'controls.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
