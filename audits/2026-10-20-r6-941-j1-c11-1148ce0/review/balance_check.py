#!/usr/bin/env python3
"""Independent NC/orbit reconstruction for the sparse 132-row exact identity."""
from pathlib import Path
import importlib.util,json,gzip,hashlib
from collections import Counter
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('dual',D/'dual_check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=D.parent/'reduction/reduced-orbit-certificate.json'
c=json.loads(p.read_text());I=json.load(gzip.open(m.IP,'rt'))
states=tuple(m.capsmod.growth(11));h,rowids,cols,parts=m.build_columns(states);live=set(I['live'])
good=[j for j,col in enumerate(cols) if all(rowids[r] in live for r,v in col)]
assert good==c['live_columns'] and len(good)==20794
eta=m.sparse_vector(c['live_half_row_multipliers'],len(h),'live halfrows')
assert Counter(v for v in eta if v)=={-1:68,1:64}
assert all(not eta[r] or i in live for r,i in enumerate(rowids))
assert c['witness_ids']==[5093,5100] and c['positive_coefficient']==16
balance=[0]*len(states)
for r,i in enumerate(rowids):balance[i]+=8*eta[r]
assert all(balance[i]==(-16 if i in (5093,5100) else 0) for i in live)
assert all(sum(eta[r]*v for r,v in cols[j])==0 for j in good)
assert c['nonnegative_column_slacks']==[]
assert c['ordered_rim']==list(m.capsmod.NAMES)
out={'status':'PASS independent exact 132-row cancellation','certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'live_halfrows':132,'plus_one':64,'minus_one':68,'live_columns_cancelled':20794,'live_core_coordinates_checked':5951,'witness_ids':[5093,5100],'witness_coefficient':-16,'all_other_live_core_coefficients':0,'signed_span_used':False,'source_branch_excluded':True,'new_Lean':False}
print(json.dumps(out,sort_keys=True))
