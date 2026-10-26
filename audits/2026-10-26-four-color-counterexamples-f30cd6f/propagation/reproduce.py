#!/usr/bin/env python3
"""Replay the fixed-colour planar initial-propagation gap; no solver edits."""
import argparse, copy, hashlib, json, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,default=Path('/tmp/propagation-gap-report.json'));args=p.parse_args()
sys.path.insert(0,str(args.repo/'scripts'))
from four_color_constraints import solve_constraints
import networkx as nx
inputs=json.loads(Path(__file__).with_name('inputs.json').read_text())
g=inputs['graph'];options=inputs['options']

def enumerate_original_edges(graph):
    # Independent exhaustive DFS using only original edges and literal fixed colours.
    adj={v:set() for v in graph['vertices']}
    for a,b in graph['edges']:adj[a].add(b);adj[b].add(a)
    col=dict(graph.get('fixed',[]));nodes=0;count=0;witness=None;pair_counts={}
    def visit():
        nonlocal nodes,count,witness
        nodes+=1
        if len(col)==len(adj):
            count+=1
            if witness is None:witness=[col[v] for v in graph['vertices']]
            key=f'{col[9]},{col[11]}';pair_counts[key]=pair_counts.get(key,0)+1
            return
        v=min((v for v in adj if v not in col),key=lambda v:(len(set(range(4))-{col[u] for u in adj[v] if u in col}),-len(adj[v]),v))
        for c in sorted(set(range(4))-{col[u] for u in adj[v] if u in col}):
            col[v]=c;visit();del col[v]
    if not any(a in col and b in col and col[a]==col[b] for a,b in graph['edges']):visit()
    return dict(solution_count=count,nodes=nodes,first_witness=witness,pair_counts_9_11=pair_counts)

class StopAfterInitialPropagation(Exception):pass
initial={}
def trace_return(frame,event,arg):
    if event=='return':
        loc=frame.f_back.f_locals
        initial.update(consistent=bool(arg),stats=copy.deepcopy(loc['stats']),domains=[sorted(d) for d in loc['domains']],all_factors_nonempty=all(f.rows for f in loc['factors']),factor_count=len(loc['factors']),cycle_scan=copy.deepcopy(loc['cycle_scan']),cycle_context_scan=copy.deepcopy(loc['cycle_context_scan']),joint_scan=copy.deepcopy(loc['joint_scan']),c5_scan=copy.deepcopy(loc['c5_scan']))
        raise StopAfterInitialPropagation
    return trace_return
def trace_calls(frame,event,arg):
    if event=='call' and frame.f_code.co_name=='propagate' and Path(frame.f_code.co_filename).resolve()==(args.repo/'scripts/four_color_constraints.py').resolve():return trace_return
    return None
sys.settrace(trace_calls)
try:solve_constraints(g,**options)
except StopAfterInitialPropagation:pass
finally:sys.settrace(None)
r=solve_constraints(g,**options)
pg=nx.Graph();pg.add_nodes_from(g['vertices']);pg.add_edges_from(g['edges'])
planar,embedding=nx.check_planarity(pg);embedding.check_structure()
fixed=enumerate_original_edges(g);bare=enumerate_original_edges(dict(g,fixed=[]))
assert planar and fixed['solution_count']==0 and bare['solution_count']>0
assert initial['consistent'] and initial['stats']['candidate_checks']==0 and initial['stats']['conflicts']==0
assert initial['all_factors_nonempty'] and all(initial['domains'])
assert not initial['cycle_scan']['truncated'] and not initial['cycle_context_scan']['truncated'] and not initial['joint_scan']['truncated']
assert r['status']=='unsatisfiable' and r['stats']['candidate_checks']>0
conflicts=[e for e in r['events'] if e['kind']=='conflict']
assert conflicts[0]['conflict_shape']=='empty_joint_relation'
sources={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted((args.repo/'scripts').glob('four_color*.py'))}
report=dict(input=inputs,source_sha256=sources,planar=planar,embedding=embedding.get_data(),fixed_oracle=fixed,bare_oracle=bare,initial=initial,full=dict(status=r['status'],stats=r['stats'],first_conflict=conflicts[0],trace_truncated=r['trace_truncated'],event_count=r['event_count']),scope='No scan cap hit for prescribed discovery; all_cycles_complete and all_contexts_complete remain false. This refutes initial propagation completeness, not exact solver correctness.')
args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(report=str(args.out),n=len(g['vertices']),m=len(g['edges']),fixed_solutions=fixed['solution_count'],bare_solutions=bare['solution_count'],initial_consistent=initial['consistent'],status=r['status'],checks=r['stats']['checks'],candidate_checks=r['stats']['candidate_checks'],successful_eliminations=r['stats']['eliminations'])))
