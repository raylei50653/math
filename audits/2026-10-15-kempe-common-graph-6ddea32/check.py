#!/usr/bin/env python3
"""Exact finite colour-function obstruction, no graph-order cutoff or solver."""
import argparse, hashlib, itertools, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = 'audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'
PAIRS = (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2)))
def need(ok, msg):
    if not ok: raise ValueError(msg)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def custody():
    m = json.loads((HERE/'INPUTS.json').read_text())
    for r in m['inputs']:
        need(digest(HERE/'frozen'/r['path']) == r['sha256'], 'frozen drift: '+r['path'])
        need(digest(ROOT/r['path']) == r['sha256'], 'live drift: '+r['path'])
    return m

def canonical(s):
    d = {}; row = tuple(d.setdefault(c,len(d)) for c in s)
    for c in 'ABCD': d.setdefault(c,len(d))
    inverse = tuple('ABCD'.index(c) for c,n in sorted(d.items(),key=lambda kv:kv[1]))
    return row,inverse

def prepare(states):
    reps = sorted({canonical(s['literal_row'])[0] for s in states})
    data = {s['id']:(reps.index(canonical(s['literal_row'])[0]),canonical(s['literal_row'])[1]) for s in states}
    need(len(data)==len(states), 'duplicate state id')
    need(all(len(set(s['literal_row']))>=3 for s in states), 'nonfree S4 orbit')
    need(len(states)==24*len(reps), 'incomplete S4 expansion')
    for r in reps:
        actual = {s['literal_row'] for s in states if canonical(s['literal_row'])[0]==r}
        expected = {''.join('ABCD'[p[c]] for c in r) for p in itertools.permutations(range(4))}
        need(actual==expected, 'S4 orbit absent')
    constraints = {}
    for s in states:
        u,p = data[s['id']]
        for part in s['pairings']:
            bits = [pair for pair,blocks in zip(part['pairing'],part['terminal_parts']) for _ in blocks]
            for bit,pair in enumerate(bits):
                target = part['cube_targets_by_bitmask'][1<<bit]
                need(target in data, 'switch leaves selected layer')
                v,q = data[target]
                allow = {(a,b) for a in range(4) for b in range(4)
                         if q[b]==p[a] or p[a] in pair and q[b]==sum(pair)-p[a]}
                if u>v: key=(v,u); allow={(b,a) for a,b in allow}
                else: key=(u,v)
                constraints.setdefault(key,set(itertools.product(range(4),repeat=2))).intersection_update(allow)
    return reps,data,constraints

def enumerate_types(n, constraints):
    """Arc-consistency search with checkable value-elimination and branch tree."""
    solutions = []; nodes = 0
    def search(dom):
        nonlocal nodes
        nodes += 1; eliminations=[]
        changed=True
        while changed:
            changed=False
            for (u,v),allowed in sorted(constraints.items()):
                for i,j,reverse in [(u,v,False)] if u==v else [(u,v,False),(v,u,True)]:
                    for a in sorted(dom[i]):
                        supported = (a,a) in allowed if i==j else any(
                            ((b,a) if reverse else (a,b)) in allowed for b in dom[j])
                        if not supported:
                            dom[i].remove(a); eliminations.append([i,a,j]); changed=True
                if not dom[u] or not dom[v]:
                    return {'remove':eliminations,'empty':u if not dom[u] else v}
        branch=[i for i,d in enumerate(dom) if len(d)>1]
        if not branch:
            value=[next(iter(d)) for d in dom]; solutions.append(value)
            return {'remove':eliminations,'solution':value}
        i=min(branch,key=lambda i:(len(dom[i]),i));children=[]
        for a in sorted(dom[i]):
            child=[set(d) for d in dom]; child[i]={a}
            children.append({'value':a,'node':search(child)})
        return {'remove':eliminations,'branch':i,'children':children}
    tree=search([set(range(4)) for _ in range(n)])
    return sorted(solutions),tree,nodes

def expand(values,data): return {sid:perm[values[var]] for sid,(var,perm) in data.items()}
def max_edges(functions,states):
    return [[u,v] for u,v in itertools.combinations(range(len(functions)),2)
            if all(functions[u][s['id']]!=functions[v][s['id']] for s in states)]
def pins_for(functions,states):
    return [next(i for i,f in enumerate(functions) if all(
        f[s['id']]=='ABCD'.index(s['literal_row'][pin]) for s in states))
        for pin in range(len(states[0]['literal_row']))]
def failures(functions,states,edges,pins):
    adj=[set() for _ in functions]
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    out=[]
    for s in states:
        for j,part in enumerate(s['pairings']):
            for pair,blocks in zip(part['pairing'],part['terminal_parts']):
                for block in blocks:
                    reached={pins[block[0]]}; todo=list(reached)
                    while todo:
                        u=todo.pop()
                        for v in sorted(adj[u]-reached):
                            if functions[v][s['id']] in pair:
                                reached.add(v);todo.append(v)
                    if any(pins[p] not in reached for p in block):
                        out.append({'state':s['id'],'row':s['literal_row'],'pairing_index':j,
                            'colour_pair':list(pair),'pin_block':block,'reached_types':sorted(reached)})
    return out

def strict_types(values,functions,states):
    accepted=[]
    for i,f in enumerate(functions):
        okay=True
        for s in states:
            for part in s['pairings']:
                bits=[pair for pair,blocks in zip(part['pairing'],part['terminal_parts']) for _ in blocks]
                chosen=[bit for bit,pair in enumerate(bits) if f[s['id']] in pair
                        and f[part['cube_targets_by_bitmask'][1<<bit]]!=f[s['id']]]
                if len(chosen)!=1:okay=False;break
                bit=chosen[0];pair=bits[bit]
                if any(f[target]!=(sum(pair)-f[s['id']] if mask>>bit&1 else f[s['id']])
                       for mask,target in enumerate(part['cube_targets_by_bitmask'])):
                    okay=False;break
            if not okay:break
        if okay: accepted.append(i)
    return accepted

def k3_control():
    rows=sorted({''.join('ABCD'[c] for c in p[:3]) for p in itertools.permutations(range(4))})
    ids={r:i for i,r in enumerate(rows)};states=[]
    for r in rows:
        rr=tuple('ABCD'.index(c) for c in r);parts=[]
        for pairing in PAIRS:
            groups=[[[v for v,c in enumerate(rr) if c in pair]] for pair in pairing]
            groups=[[] if g==[[]] else g for g in groups]
            bits=[(pair,b) for pair,group in zip(pairing,groups) for b in group];targets=[]
            for mask in range(1<<len(bits)):
                x=list(rr)
                for bit,(pair,block) in enumerate(bits):
                    if mask>>bit&1:
                        for v in block:x[v]=sum(pair)-x[v]
                targets.append(ids[''.join('ABCD'[c] for c in x)])
            parts.append({'pairing':pairing,'terminal_parts':groups,'cube_targets_by_bitmask':targets})
        states.append({'id':ids[r],'literal_row':r,'pairings':parts})
    reps,data,cons=prepare(states);values,tree,nodes=enumerate_types(len(reps),cons)
    fs=[expand(v,data) for v in values];edges=max_edges(fs,states);pins=pins_for(fs,states)
    bad=failures(fs,states,edges,pins)
    need(len(values)==4 and len(edges)==6 and not bad,'K3 positive control failed')
    return {'graph':'K3 with all vertices pinned','states':24,'weak_types':4,'type_graph':'K4','type_edges':6,'failed_blocks':0}

def build():
    manifest=custody(); source=json.loads((HERE/'frozen'/INPUT).read_text())
    need(source['state_count']==720 and source['outer_mask']==319,'wrong source model')
    states=[s for s in source['states'] if s['layer']==0]
    need(len(states)==432,'Layer0 must have 432 states')
    reps,data,constraints=prepare(states);values,tree,nodes=enumerate_types(len(reps),constraints)
    functions=[expand(v,data) for v in values];edges=max_edges(functions,states);pins=pins_for(functions,states)
    bad=failures(functions,states,edges,pins)
    strict=strict_types(values,functions,states);sf=[functions[i] for i in strict]
    se=max_edges(sf,states);sp=pins_for(sf,states);sb=failures(sf,states,se,sp)
    need((len(values),len(edges),len(bad))==(25,41,1056),'weak result changed')
    need((len(strict),len(se),len(sb))==(13,18,1056),'strict result changed')
    return {'schema':'same-state-colour-function-obstruction-v1','base':manifest['base'],
      'input_sha256':digest(HERE/'frozen'/INPUT),'scope':'S4-equivariant single-valued state lift; arbitrary finite graph order',
      'selected_layer':0,'selected_states':432,'canonical_rows':[''.join('ABCD'[c] for c in r) for r in reps],
      'binary_constraints':[{'variables':list(k),'allowed':[list(p) for p in sorted(v)]} for k,v in sorted(constraints.items())],
      'enumeration':{'nodes':nodes,'tree':tree},'weak_functions':values,'maximal_type_edges':edges,'pin_types':pins,
      'failed_blocks':bad,'first_obstruction':bad[0],
      'strict_refinement':{'weak_type_indices':strict,'maximal_type_edges':se,'pin_types':sp,'failed_blocks':sb},
      'positive_control':k3_control(),'exact_state_lift':'impossible','hidden_state_covers':'OPEN',
      'all_22_row_graph_realizability':'OPEN','target_source_exclusion':'not triggered; OPEN','general_claim':'OPEN','new_Lean':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',default=str(HERE/'certificate.json'));parser.add_argument('--write',action='store_true');args=parser.parse_args()
    expected=build();path=Path(args.certificate)
    if args.write:
        with path.open('x') as f:json.dump(expected,f,indent=2);f.write('\n')
    else:need(json.loads(path.read_text())==expected,'certificate mismatch')
    print(json.dumps({'status':'PASS','states':432,'canonical_variables':18,'binary_constraints':53,
      'weak_types':25,'weak_edges':41,'strict_types':13,'strict_edges':18,'failed_blocks':1056,
      'first_obstruction':expected['first_obstruction'],'source_exclusion':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
