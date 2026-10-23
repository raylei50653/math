#!/usr/bin/env python3
"""Bounded exploratory closure of only the inherited four residuals."""
import ast
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PREV='audits/2026-10-23-three-mask-methods-cb8f859/933'
spec=importlib.util.spec_from_file_location('previous',HERE/'frozen'/PREV/'check.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
src=json.loads((HERE/'frozen'/p.SOURCE).read_text())
old=json.loads((HERE/'frozen'/PREV/'certificate.json').read_text())
tuples=[tuple(t) for t in src['tuples']]
four=list(p.itertools.combinations(range(8),4))
nc=[part for part in p.partitions() if not any(part[i]==part[k] and part[j]==part[l] and part[i]!=part[j] for i,j,k,l in four)]
columns=[]
for part in nc:
    col=[int(all(part[i]!=part[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in tuples]
    if any(col):columns.append(col)
A=list(map(list,zip(*columns)))
live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
B=p.mm(A,p.kernel([row for j,row in enumerate(A) if j not in live],91))
M=old['count_matrices']
algorithm=(HERE/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe_consistency.py').read_text()
tree=ast.parse(algorithm)
needed={'options'}
option_ast=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in needed],type_ignores=[])
namespace={'NONCROSSING':nc,'INDEX':{t:i for i,t in enumerate(tuples)},'canonical':p.canonical}
exec(compile(option_ast,'frozen-original-options','exec'),namespace)
splits=src['palette_splits']
start=time.monotonic()
OPTIONS=[[namespace['options'](t,split) for split in splits] for t in tuples]
print('options',time.monotonic()-start,flush=True)
results=[]
for name in ('Q1','Q2'):
    for ri in (49,55):
        rule=old['prime_rules'][ri]
        zeros={j for i,row in enumerate(M[name]) if rule['absent_mask']>>i&1 for j,x in enumerate(row) if x}
        rounds=[]
        while True:
            S,steps,known=p.close_zeros(B,zeros)
            # Zero identities without negative signs also remove support.
            zero_linear={j for j,row in enumerate(S) if not any(row)} if S else set(range(274))
            zeros=set(known)|zero_linear
            remove=[]
            for j in sorted(set(range(274))-zeros):
                for split,choices in enumerate(OPTIONS[j]):
                    if not any(not (set(orbit)&zeros) for orbit,_ in choices):
                        remove.append((j,split));break
            rounds.append({'dimension':len(S[0]) if S else 0,'linear_zero_count':len(zeros),'sign_rounds':len(steps),'kempe_remove':remove})
            if not remove:break
            zeros|={j for j,_ in remove}
        G=p.mm(M['G'],S) if S else [[] for _ in p.ROWS]
        H=p.mm(M[name],S) if S else [[] for _ in p.ROWS]
        out={'candidate':name,'rule':ri,'rounds':rounds,'killed_original':[p.ROWS[i] for i,row in enumerate(G) if 933>>i&1 and not any(row)],'killed_candidate':[p.ROWS[i] for i,row in enumerate(H) if rule['required_mask']>>i&1 and not any(row)],'live':sorted(set(range(274))-zeros)}
        print(json.dumps(out),flush=True);results.append(out)
with (HERE/'probe.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')
