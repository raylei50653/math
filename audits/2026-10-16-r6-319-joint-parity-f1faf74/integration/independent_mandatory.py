#!/usr/bin/env python3
"""Recheck all58 absence tests using A's independent engine, not C's."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
helper = AUDIT/'A/review_c_independent.py'
spec = importlib.util.spec_from_file_location('independent_h', helper)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
source = AUDIT/'C/combined-source-exploration.json'
candidate = AUDIT/'C/final-step-certificate.json'
records = json.loads(source.read_text())
assert all(x['H_fixed'] == records[0]['H_fixed'] for x in records)
rows = {tuple('ABCD'.index(c) for c in s) for s in records[0]['H_fixed']}
assert len(rows) == 58
claimed = {x['deleted']: x for x in json.loads(candidate.read_text())['single_row_deletions']}
result = []
for row in sorted(rows):
    stable, rounds = h.close(rows - {row})
    support = h.support(stable)
    entry = {'deleted':h.name(row), 'stable_count':len(stable),
             'stable_supports':support, 'mandatory':support != [1022,1022,319]}
    assert all(claimed[entry['deleted']][key] == value for key,value in entry.items())
    if entry['mandatory']:
        assert len(stable) == 40 and support == [1022,1022,63]
        assert len(set(row[1:5])) == 4
    result.append(entry)
mandatory = [x['deleted'] for x in result if x['mandatory']]
assert mandatory == ['ABACDBCD','ABACDBDC','ABCADBCD','ABCADBDC','ABCDABCD','ABCDABDC']
print(json.dumps({'status':'PASS','independent_of':'C necessary-screen implementation',
                  'bindings':{str(p.relative_to(AUDIT)):sha256(p.read_bytes()).hexdigest()
                              for p in (helper,source,candidate)},
                  'all58_deletions':result,'mandatory_rows':mandatory,
                  'full_literal_fibres_with_fixed_z_s_colours':12,
                  'v5_exclusion':'OPEN'}, sort_keys=True))
