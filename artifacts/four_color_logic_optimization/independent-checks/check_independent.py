#!/usr/bin/env python3
"""Independent original-edge and Cartesian-fibre checks of three solver sources.

Each source runs in its own process. No production verifier supplies an oracle.
Replay: python3 check_independent.py --out-dir /tmp/new-independent-replay
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random
import subprocess
import sys

SOURCE_ROOT = Path(__file__).resolve().parents[1] / 'exploration-sources'
SOURCES = {mode: str(SOURCE_ROOT / mode / 'scripts')
           for mode in ('baseline', 'prefix', 'join')}

WORK_KEYS = {'checks', 'candidate_checks', 'relation_checks'}
COMMON = dict(use_conflicts=False, record_relations=True, trace_limit=10000,
              max_checks=1000000, max_table_rows=1000000)
CONFIGS = {
    'bare': dict(use_substructures=False, use_intersections=False),
    'combined': dict(use_substructures=True, use_intersections=True,
                     use_interface_cache=True, use_cycles=True,
                     use_cycle_contexts=True, cycle_context_search='partial'),
}

def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()

def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()

def semantic(value):
    if isinstance(value, dict):
        return {k:semantic(v) for k,v in value.items() if k not in WORK_KEYS}
    if isinstance(value, (list, tuple)):
        return [semantic(v) for v in value]
    return value

def manifest(path):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.glob('four_color*.py'))}

def make_cases():
    cases=[]
    for mask in range(64):
        pairs=list(combinations(range(4), 2))
        edges=[list(e) for i,e in enumerate(pairs) if mask & (1 << i)]
        cases.append(dict(name=f'n4-all-{mask:02d}', vertices=list(range(4)), edges=edges, fixed=[]))
        ids=[42,-9,103,8]
        mapped=[[ids[b],ids[a]] for a,b in reversed(edges)]
        cases.append(dict(name=f'n4-all-{mask:02d}-literal-fixed',
                          vertices=list(reversed(ids)) if mask % 2 else ids,
                          edges=mapped, fixed=[[ids[0],0],[ids[3],mask % 4]]))
    for seed in range(32):
        rng=random.Random(88000+seed)
        ids=[-31,5,1007,42,-200,88]
        p=0.10+0.12*(seed % 8)
        edges=[[a,b] for a,b in combinations(ids,2) if rng.random()<p]
        rng.shuffle(edges)
        vertices=ids[:]
        rng.shuffle(vertices)
        fixed=[[v,rng.randrange(4)] for v in rng.sample(ids,seed % 4)]
        cases.append(dict(name=f'n6-seed-{seed:02d}', vertices=vertices, edges=edges, fixed=fixed))
    cases.extend([
        dict(name='empty', vertices=[], edges=[], fixed=[]),
        dict(name='isolated-literal-fixed', vertices=[42,-9,100], edges=[], fixed=[[100,2]]),
        dict(name='K5-bucket-unsat', vertices=list(range(5)), edges=[list(e) for e in combinations(range(5),2)], fixed=[]),
        dict(name='K6-bucket-unsat', vertices=list(range(6)), edges=[list(e) for e in combinations(range(6),2)], fixed=[]),
    ])
    return cases

def original_solutions(graph):
    vertices=graph['vertices']
    positions={v:i for i,v in enumerate(vertices)}
    fixed=dict(graph['fixed'])
    sols=[]
    for colors in product(*(tuple([fixed[v]]) if v in fixed else range(4) for v in vertices)):
        if all(colors[positions[a]] != colors[positions[b]] for a,b in graph['edges']):
            sols.append(dict(zip(vertices,colors)))
    return sols

def inspect_records(result, solutions):
    metrics=Counter()
    for record in result['elimination_records']:
        variables=[record['vertex'],*record['scope']]
        domains={entry['vertex']:entry['colors'] for entry in record['source_domains']}
        assert set(domains)==set(variables)
        assert record['complete'] is True
        assert record['absent_boundary']=='empty fibre within the recorded source_domains'
        inputs=[(rel['scope'],{tuple(row) for row in rel['rows']}) for rel in record['input_relations']]
        expected={}
        for colors in product(*(domains[v] for v in variables)):
            metrics['cartesian_assignments']+=1
            assignment=dict(zip(variables,colors))
            if all(tuple(assignment[v] for v in scope) in rows for scope,rows in inputs):
                boundary=tuple(assignment[v] for v in record['scope'])
                expected.setdefault(boundary,set()).add(assignment[record['vertex']])
        actual={tuple(row['boundary']):set(row['colors']) for row in record['rows']}
        assert len(actual)==len(record['rows'])==record['relation_rows']
        assert actual==expected
        assert [tuple(row['boundary']) for row in record['rows']]==sorted(actual)
        for row in record['rows']:
            assert row['colors']==sorted(set(row['colors']))
        for boundary in product(*(domains[v] for v in record['scope'])):
            metrics['ambient_fibres']+=1
            assert actual.get(boundary,set())==expected.get(boundary,set())
            if boundary not in actual:
                metrics['empty_fibres']+=1
        for solution in solutions:
            assert all(solution[v] in domains[v] for v in variables)
            for scope,rows in inputs:
                assert tuple(solution[v] for v in scope) in rows
            boundary=tuple(solution[v] for v in record['scope'])
            assert solution[record['vertex']] in actual[boundary]
            metrics['source_solution_record_checks']+=1
        metrics['records']+=1
    return metrics

def inspect_result(graph,result,solutions,allow_limit=False):
    assert result['graph']['vertices']==graph['vertices']
    assert result['trace_truncated'] is False
    expected='colored' if solutions else 'unsatisfiable'
    assert result['status']==expected or (allow_limit and result['status']=='limit')
    vertices=result['graph']['vertices']
    for event in result['events']:
        if event['phase']=='reduce':
            assert event['colors']==[dict(graph['fixed']).get(v,-1) for v in vertices]
            for solution in solutions:
                assert all(solution[v] in domain for v,domain in zip(vertices,event['domains']))
    if result['status']=='colored':
        assignment=dict(zip(vertices,result['colors']))
        assert all(assignment[a]!=assignment[b] for a,b in graph['edges'])
        assert all(assignment[v]==c for v,c in graph['fixed'])
        assert all(c in range(4) for c in result['colors'])
    else:
        assert result['stats']['writebacks']==0
        assert result['colors']==[dict(graph['fixed']).get(v,-1) for v in vertices]
    return inspect_records(result,solutions)

def worker(mode,source,out):
    before=manifest(source)
    sys.path.insert(0,str(source))
    from four_color_constraints import solve_constraints
    rows=[]
    totals=Counter()
    solutions_counts={}
    for case in make_cases():
        solutions=original_solutions(case)
        solutions_counts[case['name']]=len(solutions)
        untouched=deepcopy(case)
        for config,options in CONFIGS.items():
            result=solve_constraints(case,**dict(COMMON,**options))
            assert case==untouched
            measures=inspect_result(case,result,solutions)
            totals.update(measures)
            rows.append(dict(name=case['name'],config=config,status=result['status'],
                             source_solutions=len(solutions),semantic_sha256=digest(semantic(result)),
                             records_sha256=digest(result['elimination_records']),
                             stats=result['stats'],checks=dict(measures)))
    cycle=dict(name='cutoff-c4',vertices=[9,-2,40,17],edges=[[9,-2],[-2,40],[40,17],[17,9]],fixed=[[9,0]])
    solutions=original_solutions(cycle)
    options=dict(COMMON,use_substructures=False,use_intersections=True,use_interface_cache=True)
    full=solve_constraints(cycle,**options)
    assert full['status']=='colored'
    cutoff_rows=[]
    for budget in range(full['stats']['checks']+1):
        result=solve_constraints(cycle,**dict(options,max_checks=budget))
        measures=inspect_result(cycle,result,solutions,allow_limit=True)
        records=result['elimination_records']
        assert records==full['elimination_records'][:len(records)]
        assert len(records)==result['stats']['eliminations']
        if budget<full['stats']['checks']:
            assert result['status']=='limit'
            assert not any(event['phase']=='writeback' for event in result['events'])
            assert all(event['colors']==[0,-1,-1,-1] for event in result['events'])
        else:
            assert result['status']=='colored'
        cutoff_rows.append(dict(budget=budget,status=result['status'],records=len(records),checks=dict(measures)))
    cap_complete=max(full['stats']['table_rows'],full['stats']['certificate_rows'])
    storage_rows=[]
    for cap in range(cap_complete+1):
        result=solve_constraints(cycle,**dict(options,max_table_rows=cap))
        measures=inspect_result(cycle,result,solutions,allow_limit=True)
        records=result['elimination_records']
        assert records==full['elimination_records'][:len(records)]
        assert len(records)==result['stats']['eliminations']
        if result['status']=='limit':
            assert not any(event['phase']=='writeback' for event in result['events'])
        storage_rows.append(dict(cap=cap,status=result['status'],records=len(records),checks=dict(measures)))
    assert storage_rows[-1]['status']=='colored'
    assert manifest(source)==before
    loaded={name:str(Path(module.__file__).resolve()) for name,module in sys.modules.items()
            if name.startswith('four_color') and getattr(module,'__file__',None)}
    assert all(Path(file).parent==source.resolve() for file in loaded.values())
    receipt=dict(mode=mode,source=str(source),source_hashes=before,loaded=loaded,
                 cases=rows,case_count=len(solutions_counts),runs=len(rows),totals=dict(totals),
                 source_solution_counts=solutions_counts,original_solutions_total=sum(solutions_counts.values()),
                 statuses=dict(Counter(row['status'] for row in rows)),
                 cutoff_graph=cycle,cutoff_full_checks=full['stats']['checks'],work_cutoffs=cutoff_rows,
                 storage_cutoffs=storage_rows,complete=True)
    (out/f'{mode}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(mode,len(rows),'runs',dict(Counter(row['status'] for row in rows)),
          'cutoffs',len(cutoff_rows),'storage',len(storage_rows),flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--worker',choices=SOURCES)
    args=parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=True)
    if args.worker:
        worker(args.worker,Path(SOURCES[args.worker]),args.out_dir)
        return
    for mode in SOURCES:
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',mode,'--out-dir',str(args.out_dir)],check=True)
    receipts={mode:json.loads((args.out_dir/f'{mode}.json').read_text()) for mode in SOURCES}
    baseline={(row['name'],row['config']):row for row in receipts['baseline']['cases']}
    comparisons={}
    for mode in ['prefix','join']:
        rows=receipts[mode]['cases']
        differences=[]
        for row in rows:
            old=baseline[(row['name'],row['config'])]
            for field in ['status','source_solutions','semantic_sha256','records_sha256']:
                if row[field]!=old[field]:
                    differences.append(dict(name=row['name'],config=row['config'],field=field))
        assert not differences,(mode,differences)
        comparisons[mode]=dict(runs=len(rows),semantic_differences=differences,
                               work_cutoffs=len(receipts[mode]['work_cutoffs']),
                               storage_cutoffs=len(receipts[mode]['storage_cutoffs']))
    report=dict(complete=True,case_count=len(make_cases()),configurations=CONFIGS,
                source_original_solutions=receipts['baseline']['original_solutions_total'],
                modes={mode:{k:receipt[k] for k in ['runs','statuses','totals','source','source_hashes','cutoff_full_checks']}
                       for mode,receipt in receipts.items()},
                comparison=comparisons,ignored_telemetry_fields=sorted(WORK_KEYS),
                oracle='Independent Cartesian enumeration of original edges/fixed colors and every recorded full input-relation join; all absent frontier tuples checked as empty fibres.',
                scope='Finite cases beyond frozen forty, no general performance or formal implementation proof.',
                driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                receipt_sha256={mode:hashlib.sha256((args.out_dir/f'{mode}.json').read_bytes()).hexdigest() for mode in SOURCES})
    (args.out_dir/'receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    (args.out_dir/'inputs.json').write_text(json.dumps(make_cases(),ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k in ['complete','case_count','source_original_solutions','comparison']},sort_keys=True))

if __name__=='__main__':
    main()
