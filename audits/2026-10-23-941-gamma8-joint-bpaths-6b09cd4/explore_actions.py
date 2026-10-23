#!/usr/bin/env python3
"""Apply every inherited literal action to each one-graph joint interface."""
from collections import Counter
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
BOUND=['a','z1','z2','z3','z4','V','U','Y','q','c','s','v','w','t']


def parts(es,co,palette):
    adj={v:set() for v,c in co.items() if c in palette}
    for a,b in es:
        if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
    out=[];unseen=set(adj)
    while unseen:
        part={min(unseen)};todo=list(part)
        while todo:
            v=todo.pop()
            for w in adj[v]-part:part.add(w);todo.append(w)
        unseen-=part;out.append(part)
    return out


def normalize_contacts(gate):return [{('Y' if v=='HL_0' else v) for v in p} for p in gate]


def refines(es,co,palette,gates):
    observed=[p&set(BOUND) for p in parts(es,co,palette)+parts(es,co,set(range(4))-set(palette))]
    return [i for i,gate in enumerate(gates) if all(any(p<=g for g in normalize_contacts(gate)) for p in observed if p)]


def gates03(row):
    p=['w','t'] if row['target']==44459 else ['t']
    q=['q','v'] if row['target']==44459 else ['q','w']
    cs=['c','s'] if row['target']==44459 else ['c','s','v']
    return [[['a','z1','z2','z3','z4','U'],['V'],['Y']+p,q,cs],
            [['a','z1','z2','z3','z4'],['V','Y']+p,['U'],q,cs]]


def main():
    previous=json.loads((HERE/'frozen/audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json').read_text())
    rows=json.loads((HERE/'frozen/audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json').read_text())['source_rows']
    old=previous['complete_predecessor_certificate']['complete_predecessor_certificate']
    for _ in range(3):old=old['complete_predecessor_certificate']
    candidates=json.loads((HERE/'JOINT_EXPLORATION.json').read_text())['survivors']
    stats=Counter();result=[]
    for ci,can in enumerate(candidates):
        b=previous['B_models'][can['B_model']]
        co={('V' if z=='e' and b['e_equals_V'] else 'c' if z=='h' and b['h_equals_c'] else z):c for z,c in old['original_colors'].items()}
        co.update(m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,V=1,Y=1,q=3,c=1)
        frame={'V','U','Y','q','c'}
        mp={v:v if v in frame else 'g_'+v for v in co}
        base_es={tuple(sorted([mp[a],mp[b]])) for a,b in can['edges']}
        base_es|={tuple(sorted([a,b])) for a,b in zip(BOUND,BOUND[1:]+BOUND[:1])}
        M={mp[z] for z in ['T','m']};N={mp[z] for z in ['r','s','tau','n','u','v']};K={mp[z] for z in ['d','x','zeta','p_d','p_x','U']}
        for source in rows:
            failures=[];observations=[]
            for m,n,k in product([0,1],repeat=3):
                colors={('Y' if z=='HL_0' else z):c for z,c in source['original_boundary_colors'].items()}
                colors.update({mp[v]:c for v,c in co.items()})
                colors={v:c^(2 if (m and v in M)or(n and v in N)or(k and v in K) else 0) for v,c in colors.items()}
                action=[m,n,k]
                if any(colors[a]==colors[b] for a,b in base_es):failures.append([*action,'improper']);continue
                if k:
                    gate=source['complete_predecessor_record']['full_03_successor_boundary_contacts']
                    if not refines(base_es,colors,{0,3},[gate]):failures.append([*action,'unique_successor'])
                else:
                    for palette,gates,name in [({0,3},gates03(source),'initial03'),({0,1},source['complete_predecessor_record']['complete_initial_01_gate'],'initial01'),({0,2},[source['complete_predecessor_record']['complete_initial_02_contacts']],'initial02')]:
                        valid=refines(base_es,colors,palette,gates)
                        if not valid:failures.append([*action,name])
                        observations.append(dict(action=action,palette=sorted(palette),matching_gates=valid))
                if action==[0,0,1]:
                    ps=parts(base_es,colors,{1,2})
                    C=next(p for p in ps if 'U' in p)
                    if any(mp[z] not in C for z in ['r','d','u','m']) or any(mp[z] in C for z in ['s','x']):failures.append([*action,'C_E_merge'])
            result.append(dict(joint_interface=ci,target=source['target'],type02=source['initial_02_type'],failures=failures,observations=observations))
            stats['rows']+=1;stats['survivors' if not failures else 'rejected']+=1
            stats.update(f[-1] for f in failures)
    (HERE/'ACTION_EXPLORATION.json').write_text(json.dumps(dict(statistics=dict(stats),rows=result),sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(stats),sort_keys=True))
    print(repr(Counter((candidates[r['joint_interface']]['B_model'],r['target'],r['type02']) for r in result if not r['failures'])))


if __name__=='__main__':main()
