import sys, random, json, time, itertools, traceback
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from four_color_constraints import solve_constraints

# Independent decision oracle: literal original edges only; no project solver helpers.
def oracle(g):
    vs=g['vertices']; adj={v:set() for v in vs}; fixed=dict(g.get('fixed',[])); a=dict(fixed)
    for x,y in g['edges']:
        adj[x].add(y); adj[y].add(x)
        if x in a and y in a and a[x]==a[y]: return None
    def search():
        if len(a)==len(vs): return dict(a)
        avail={v:[c for c in range(4) if all(a.get(w)!=c for w in adj[v])] for v in vs if v not in a}
        v=min(avail,key=lambda v:(len(avail[v]),-len(adj[v])))
        for c in avail[v]:
            a[v]=c
            ans=search()
            if ans is not None: return ans
        a.pop(v,None)
        return None
    return search()

def valid(g, cs):
    if len(cs)!=len(g['vertices']) or any(type(c)!=int or c not in range(4) for c in cs):return False
    a=dict(zip(g['vertices'],cs))
    return all(a[x]!=a[y] for x,y in g['edges']) and all(a[v]==c for v,c in g.get('fixed',[]))

def audit_fibres(r):
    for rec in r['elimination_records']:
        vv=[rec['vertex'],*rec['scope']]
        ds={e['vertex']:e['colors'] for e in rec['source_domains']}
        rels=[(rel['scope'],set(map(tuple,rel['rows']))) for rel in rec['input_relations']]
        expected={}
        for row in itertools.product(*(ds[v] for v in vv)):
            a=dict(zip(vv,row))
            if all(tuple(a[v] for v in scope) in rows for scope,rows in rels):
                expected.setdefault(tuple(a[v] for v in rec['scope']),set()).add(a[rec['vertex']])
        actual={tuple(row['boundary']):set(row['colors']) for row in rec['rows']}
        if expected!=actual: raise AssertionError('incomplete fibre')

rng=random.Random(26026); start=time.time(); stats=Counter(); failure=None; tested=[]
for i in range(1500):
    n=rng.randrange(0,12); vs=rng.sample(range(-50,100),n)
    p=rng.choice([.12,.25,.4,.55,.7,.85])
    es=[[x,y] for x,y in itertools.combinations(vs,2) if rng.random()<p]
    fixed=[[v,rng.randrange(4)] for v in vs if rng.random()<rng.choice([0,.15,.4])]
    g={'vertices':vs,'edges':es,'fixed':fixed}
    witness=oracle(g); sat=witness is not None
    rec=(i%20==0 and n<=8)
    options=[
      dict(bucket_method='anchor',use_intersections=True,use_interface_cache=True,interface_cache_max_rows=rng.choice([0,1,12,24,100,100000])),
      dict(bucket_method='prefix',use_intersections=True,use_interface_cache=True,interface_cache_max_rows=rng.choice([0,1,12,24,100,100000])),
    ]
    if i%5==0:
        options.append(dict(bucket_method='prefix',use_intersections=True,use_interface_cache=True,interface_cache_max_rows=24,use_cycles=True,use_cycle_contexts=True,cycle_context_search='partial',use_c5=True,c5_method='structure',use_joint_constraints=True))
    for opts in options:
        opts.update(max_checks=2_000_000,max_table_rows=1_000_000,trace_limit=0,record_relations=rec,use_substructures=rng.choice([False,True]),use_conflicts=rng.choice([False,True]))
        try:
            r=solve_constraints(g,**opts); stats['runs']+=1; stats[r['status']]+=1; stats['graphs_sat' if sat else 'graphs_unsat']+=1
            if r['status']=='colored' and not valid(g,r['colors']): raise AssertionError('invalid coloring')
            if r['status']=='colored' and not sat: raise AssertionError('false positive')
            if r['status']=='unsatisfiable' and sat: raise AssertionError('false negative')
            if r['status'] not in ('colored','unsatisfiable','limit'): raise AssertionError('unexpected status')
            if r['status']=='limit' and any(c>=0 and v not in dict(fixed) for v,c in zip(vs,r['colors'])):raise AssertionError('partial writeback on limit')
            if rec:
                audit_fibres(r);stats['fibre_records']+=len(r['elimination_records'])
        except Exception as e:
            failure={'i':i,'graph':g,'options':opts,'oracle':witness,'error':repr(e),'traceback':traceback.format_exc()};break
    stats['graphs']+=1
    if failure:break
    if i%100==0:
        print(json.dumps({'i':i,'elapsed':round(time.time()-start,2),'stats':stats}),flush=True)
out={'seed':26026,'elapsed':time.time()-start,'stats':stats,'failure':failure}
open('/tmp/semantic_four_color_audit.json','w').write(json.dumps(out,indent=2))
print(json.dumps(out),flush=True)
