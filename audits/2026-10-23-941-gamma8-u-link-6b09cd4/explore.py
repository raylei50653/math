#!/usr/bin/env python3
"""Narrow exploratory reconstruction of the six fixed u-link cases."""
import importlib.util
import json
from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = HERE.parent / '2026-10-23-941-gamma8-six-equality-6b09cd4'
spec = importlib.util.spec_from_file_location('previous', PREV / 'check.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def main():
    cert = json.loads((PREV / 'certificate.json').read_text())
    contract, cells = old.cells(cert['complete_predecessor_certificate'])
    out = []
    for cell in cells:
        case = next(row for row in cert['six_point_cases'] if row['cell'] == cell['id'] and row['side'] == 'C' and row['u_color'] == 1 and row['v_color'] == 3)
        for ul in case['complete_u_links']:
            phi, labels, adj, _ = old.graph(contract, cell,
                dict(m=2, n=3, u=1, v=3, p_d=2, p_x=2),
                dict(m='M', n='N', u='N', v='N', p_d='K', p_x='K'),
                [('T','m'),('T','n'),('m','r'),('m','n'),('m','u'),('m','v'),('n','u'),('u','v'),('v','r'),('n','s'),('d','p_d'),('x','p_x')])
            links = dict(m=['r','T','n','u','v'], T=['r','tau','s','n','m'], u=ul)
            for a,b in zip(ul, ul[1:] + ul[:1]):
                adj[a].add(b); adj[b].add(a)
            for w in ul:
                adj['u'].add(w); adj[w].add('u')
            sides = dict(r='C',d='C',e='C',s='E',x='E',h='E',m='C',u='C',U='C')
            gamma = set(contract['boundary'])
            pool = gamma | {'m','n','u','v','p_d','p_x','U'}

            def basic(a,b):
                if a == b or phi[a] == phi[b]: return False
                if {labels[a],labels[b]} == {'M','B'}: return False
                if {phi[a],phi[b]} <= {0,2} and labels[a] != labels[b]: return False
                if {phi[a],phi[b]} <= {1,3} and labels[a] != labels[b]: return False
                psi = {z: c ^ 2 if labels[z] == 'K' else c for z,c in phi.items()}
                if {psi[a],psi[b]} == {1,2} and a in sides and b in sides and sides[a] != sides[b]: return False
                if a in ('tau','zeta') or b in ('tau','zeta'): return b in adj[a]
                if a in gamma and b in gamma: return b in adj[a]
                for z,link in links.items():
                    if a == z and b not in link: return False
                    if b == z and a not in link: return False
                    if a in link and b in link and (link.index(a)-link.index(b)) % len(link) not in (1,len(link)-1): return False
                return True

            def valid(a):
                for z in a:
                    if any(not basic(z,w) for w in a[z]): return False
                for z,w in combinations(a,2):
                    common = a[z] & a[w]
                    if len(common)>2: return False
                return True

            def complete(center,arc,a):
                allowed = sorted(z for z in pool if basic(center,z))
                extras = sorted(set(allowed)-set(arc))
                result = []
                for k in range(max(0,5-len(arc)),len(extras)+1):
                    for chosen in combinations(extras,k):
                        if not a[center] <= set(arc)|set(chosen): continue
                        for seq in permutations(chosen):
                            link = list(arc)+list(seq)
                            edges = list(zip(link,link[1:]+link[:1]))+[(center,w) for w in link]
                            if any(not basic(z,w) for z,w in edges): continue
                            trial = {z:set(nbs) for z,nbs in a.items()}
                            for z,w in edges: trial[z].add(w);trial[w].add(z)
                            if not valid(trial): continue
                            # Complete links have no chords, all C3 are faces.
                            if any(w in trial[z] and (link.index(z)-link.index(w)) % len(link) not in (1,len(link)-1) for z,w in combinations(link,2)): continue
                            result.append((link,trial))
                return allowed,result

            allow_n, nlinks = complete('n',['s','T','m','u'],adj)
            joint=[]
            for nl,na in nlinks:
                links['n']=nl
                allow_v,vlinks=complete('v',['r','m','u'],na)
                for vl,va in vlinks:
                    links['v']=vl
                    def inner_arc(center,start,end):
                        la={w:set() for w in contract['original_colors'] if w != center}
                        for f in cell['faces']:
                            if center in f:
                                z,w=[z for z in f if z != center]
                                la[z].add(w);la[w].add(z)
                        arc=[start]
                        while arc[-1] != end:
                            arc.append(next(z for z in la[arc[-1]] if len(arc)<2 or z != arc[-2]))
                        return arc
                    ra=inner_arc('r','d','T')+['m','v']
                    _,rlinks=complete('r',ra,va)
                    sra=[]
                    for rl,rga in rlinks:
                        links['r']=rl
                        sa=inner_arc('s','T','x')
                        _,slinks=complete('s',sa,rga)
                        sra.extend(dict(r=rl,s=sl) for sl,_ in slinks)
                        del links['r']
                    joint.append(dict(n=nl,v=vl,rs=sra))
                    del links['v']
                del links['n']
            out.append(dict(cell=cell['id'], core=cell['core'], u=ul, allowed_n=allow_n, n_links=[x[0] for x in nlinks], joint=joint, valid_initial=valid(adj)))
    (HERE/'exploration.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(cases=len(out), nv=sum(len(x['joint']) for x in out),
        rs=sum(len(y['rs']) for x in out for y in x['joint']))))


if __name__ == '__main__':main()
