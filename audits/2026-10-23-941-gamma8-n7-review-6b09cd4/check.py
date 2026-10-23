#!/usr/bin/env python3
"""Independent finite review. Never imports the producer or closes a K-star."""
from pathlib import Path
from itertools import combinations, permutations
from collections import Counter
from copy import deepcopy
import argparse, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRACE = 'audits/2026-10-23-941-gamma8-n-stars-6b09cd4/explore-trace.json'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def calculate():
    custody = json.loads((HERE/'INPUTS.json').read_text())
    for row in custody['inputs']:
        b = (HERE/'frozen'/row['path']).read_bytes()
        require(hashlib.sha256(b).hexdigest() == row['sha256'], 'frozen input hash')
        if row['status'] == 'immutable authority':
            require((ROOT/row['path']).read_bytes() == b, 'authority input drift')
    # Independent wheel lemma: an outside point can touch at most two rim
    # vertices, and a two-set must be one actual rim edge. Distinct rim-edge
    # face witnesses therefore need D different actual outside vertices.
    wheels=[]
    for degree in range(6,33,2):
        allowed=[]
        for size in range(4):
            for subset in combinations(range(degree),size):
                if all((i-j)%degree in (1,degree-1) for i,j in combinations(subset,2)):
                    allowed.append(subset)
        edges=[tuple(sorted((i,(i+1)%degree))) for i in range(degree)]
        edge_sets=[s for s in allowed if len(s)==2]
        require(sorted(edge_sets)==sorted(edges), 'wheel edge injectivity')
        wheels.append(dict(D=degree,face_witnesses=degree,minimum_Z=2*degree-7,
                           minimum_Z_if_d_equals_U=2*degree-6))
    # Reconstruct every possible u-cycle in the N1 envelope independently.
    color=dict(m=2,n=3,v=3,p_d=2,p_x=2,U=0,d=0,omega=1)
    ulinks=[]
    for size in (2,3):
        for chosen in combinations(['p_d','p_x','U'],size):
            for seq in permutations(chosen):
                link=['n','m','v',*seq]
                if any(color[a]==color[b] for a,b in zip(link,link[1:]+link[:1])):
                    continue
                require('U' in link, 'N1 Uu forced')
                exits=sorted(set(link)&{'p_d','p_x'})
                require(bool(exits), 'N1 u needs exit')
                for w in ('n','v'):
                    omega={'d','p_d','U','p_x',w}
                    common=sorted(set(link)&omega)
                    require(len(common)>=3,'N1 common-neighbor contradiction')
                ulinks.append(link)
    # Terminal independent review of the sealed common-star snapshot.
    trace=json.loads((HERE/'frozen'/TRACE).read_text())
    totals=Counter(); capacity=Counter(); raw_cycles=Counter(); survivors=[]
    for index,row in enumerate(trace['preomega']):
        kind=row['omega_type']; totals[kind]+=1
        phi=dict(T=0,r=1,s=1,tau=3,x=0,h=1,W=3,e=1,d=0,zeta=2,
                 m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,omega=int(kind[1]))
        if row['d_equals_U']:
            del phi['U']
        graph={v:set() for v in phi}
        for a,b in row['edges']:
            require(a in graph and b in graph,'snapshot actual identity')
            graph[a].add(b);graph[b].add(a)
            require(phi[a]!=phi[b],'snapshot proper coloring')
        links=row['full_links']
        for center,link in links.items():
            require(len(link)==len(set(link)) and len(link)>=5,'snapshot complete simple link')
            require(graph[center]==set(link),'snapshot full-star closure')
            require(all(b in graph[a] for a,b in zip(link,link[1:]+link[:1])), 'snapshot rim edges')
            require(all(b not in graph[a] for i,a in enumerate(link) for j,b in enumerate(link)
                        if i!=j and (i-j)%len(link) not in (1,len(link)-1)), 'snapshot induced full link')
        # Omega is an exterior R13 vertex. All other R02 stars are closed;
        # rooted B/L and every exterior spectator are excluded by ownership.
        pool=[v for v in ('r','s','n','u','v','d','x','U','p_d','p_x') if v in phi and phi[v]!=phi['omega']]
        allowed=[]
        for v in pool:
            if v in links and 'omega' not in links[v]:
                continue
            if any('omega' in link and v in link and
                   (link.index('omega')-link.index(v))%len(link) not in (1,len(link)-1)
                   for link in links.values()):
                continue
            allowed.append(v)
        capacity[(kind,len(allowed))]+=1
        for size in range(5,len(allowed)+1):
            for chosen in combinations(allowed,size):
                if not graph['omega']<=set(chosen):
                    continue
                if {'r','s'}<=set(chosen) or {'d','x'}<=set(chosen):
                    continue
                # Rootless N connectivity: some original N13 neighbor required.
                if not set(chosen)&{'r','s','n','u','v'}:
                    continue
                first=min(chosen)
                for tail in permutations(v for v in chosen if v!=first):
                    cycle=[first,*tail]
                    if cycle[1]>cycle[-1]:
                        continue
                    raw_cycles[kind]+=1
                    trial={v:set(nbs) for v,nbs in graph.items()}
                    proposed=[('omega',v) for v in cycle]+list(zip(cycle,cycle[1:]+cycle[:1]))
                    good=True
                    for a,b in proposed:
                        if phi[a]==phi[b]:good=False;break
                        # All other 02 vertices belong to K. K edges may be
                        # added here; their unknown exterior stars stay open.
                        if a in links and b not in links[a] or b in links and a not in links[b]:
                            good=False;break
                        for link in links.values():
                            if a in link and b in link and (link.index(a)-link.index(b))%len(link) not in (1,len(link)-1):
                                good=False;break
                        if not good:break
                        trial[a].add(b);trial[b].add(a)
                    if not good:continue
                    if any(len(trial[a]&trial[b])>2 for a,b in combinations(trial,2)):
                        continue
                    if any(b in trial[a] for i,a in enumerate(cycle) for j,b in enumerate(cycle)
                           if i!=j and (i-j)%len(cycle) not in (1,len(cycle)-1)):
                        continue
                    survivors.append(dict(index=index,cycle=cycle))
    require(not survivors,'terminal omega complete-star counterexample')
    return dict(schema='independent-n7-review-v1',source_status='not triggered',
                finite_status='triggered and holds',wheel_rows=wheels,
                N1_complete_u_cycles=ulinks,N1_common_neighbor_minimum=3,
                terminal_snapshot_rows=dict(sorted(totals.items())),
                terminal_allowed_capacity=[dict(kind=k[0],allowed=k[1],rows=v) for k,v in sorted(capacity.items())],
                terminal_tested_cycles=dict(sorted(raw_cycles.items())),terminal_complete_omega_stars=survivors)

def validate(cert):
    require(cert==calculate(),'independent certificate mismatch')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--generate',action='store_true');ap.add_argument('--negative',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args()
    if args.generate:
        cert=calculate()
        with args.certificate.open('x') as f:json.dump(cert,f,indent=2,sort_keys=True);f.write('\n')
        print(json.dumps(dict(generated=True,N1=len(cert['N1_complete_u_cycles']),terminal=cert['terminal_snapshot_rows'])));return
    cert=json.loads(args.certificate.read_text());validate(cert)
    if args.negative:
        mutations=[('wheel-bound',lambda x:x['wheel_rows'][1].update(minimum_Z=8)),
                   ('alias-bound',lambda x:x['wheel_rows'][1].update(minimum_Z_if_d_equals_U=9)),
                   ('N1-common',lambda x:x.update(N1_common_neighbor_minimum=2)),
                   ('terminal-source',lambda x:x.update(source_status='triggered and holds')),
                   ('N3-count',lambda x:x['terminal_snapshot_rows'].update(N3=200)),
                   ('fake-star',lambda x:x['terminal_complete_omega_stars'].append(dict(index=0,cycle=['d','p_d','U','p_x','u'])))]
        rejected=[]
        for name,mutate in mutations:
            changed=deepcopy(cert);mutate(changed)
            try:validate(changed)
            except ValueError:rejected.append(name)
            else:raise ValueError('negative accepted: '+name)
        print(json.dumps(dict(status='PASS',rejected=rejected),sort_keys=True))
    else:
        print(json.dumps(dict(status='PASS',N1_u_cycles=len(cert['N1_complete_u_cycles']),terminal_rows=cert['terminal_snapshot_rows'],complete_omega_stars=0,source_status='not triggered'),sort_keys=True))
if __name__=='__main__':main()
