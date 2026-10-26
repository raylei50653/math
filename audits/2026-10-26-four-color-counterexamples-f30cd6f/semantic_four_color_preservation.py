import sys, random, json, time, itertools, traceback
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from four_color_constraints import solve_constraints
rng=random.Random(26027); stats=Counter();start=time.time();failure=None
for i in range(120):
    n=rng.randrange(5,9); vs=rng.sample(range(-30,70),n);p=rng.uniform(.25,.75)
    g={'vertices':vs,'edges':[[u,v] for u,v in itertools.combinations(vs,2) if rng.random()<p], 'fixed':[[v,rng.randrange(4)] for v in vs if rng.random()<.15]}
    fixed=dict(g['fixed']); all_solutions=[]
    for row in itertools.product(*[(fixed[v],) if v in fixed else range(4) for v in vs]):
        a=dict(zip(vs,row))
        if all(a[u]!=a[v] for u,v in g['edges']): all_solutions.append(a)
    opts=dict(use_intersections=True,use_interface_cache=True,interface_cache_max_rows=rng.choice([0,1,12,24,100,100000]),use_cycles=True,use_cycle_contexts=True,cycle_context_search='partial',use_c5=True,c5_method=rng.choice(['table','structure']),use_joint_constraints=True,bucket_method=rng.choice(['prefix','anchor']),use_substructures=rng.choice([False,True]),use_conflicts=rng.choice([False,True]),record_relations=True,trace_limit=20000,max_checks=3_000_000,max_table_rows=1_000_000)
    try:
        r=solve_constraints(g,**opts);stats[r['status']]+=1
        for rec in r['elimination_records']:
            ds={x['vertex']:x['colors'] for x in rec['source_domains']}
            rs={tuple(x['boundary']):set(x['colors']) for x in rec['rows']}
            for a in all_solutions:
                if not all(a[v] in colors for v,colors in ds.items()):raise AssertionError('domain lost original solution')
                if a[rec['vertex']] not in rs.get(tuple(a[v] for v in rec['scope']),set()):raise AssertionError('fibre lost original solution')
                stats['solution_fibre_checks']+=1
            stats['fibres']+=1
        for event in r['events']:
            if event.get('phase')!='reduce':continue
            for a in all_solutions:
                if any(a[v] not in ds for v,ds in zip(vs,event['domains'])):raise AssertionError('event domain lost solution')
                stats['solution_event_checks']+=1
        if bool(all_solutions)!=(r['status']=='colored') and r['status']!='limit':raise AssertionError('verdict mismatch')
    except Exception as e:
        failure=dict(graph=g,options=opts,error=repr(e),traceback=traceback.format_exc());break
    stats['graphs']+=1;stats['solutions']+=len(all_solutions)
result=dict(seed=26027,elapsed=time.time()-start,stats=stats,failure=failure)
open('/tmp/semantic_four_color_preservation.json','w').write(json.dumps(result,indent=2));print(json.dumps(result))
