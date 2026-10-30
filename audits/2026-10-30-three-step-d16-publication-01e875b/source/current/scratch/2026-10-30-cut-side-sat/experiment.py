from __future__ import annotations

from itertools import product, permutations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import ck_kempe_obstruction as old
from pysat.solvers import Solver


def run(m):
    # Union IDs: C0=(z,a,b,w,c,d)=(0,1,2,3,4,5),
    # path L=(b,6,...,m+4,c), m edges.
    path = (2,) + tuple(range(6, m+5)) + (4,)
    left = path + (5,0,1)
    right = (2,3,4) + tuple(reversed(path[1:-1]))
    boundaries = (left,right)
    patterns = tuple(old.patterns(len(b)) for b in boundaries)
    indices = tuple({p:i for i,p in enumerate(ps)} for ps in patterns)
    print('m', m, 'boundaries', boundaries, 'pattern counts', list(map(len,patterns)), flush=True)
    varsides = []
    nvar = 0
    clauses = []
    for side,ps in enumerate(patterns):
        vs = []
        for _ in ps:
            nvar += 1
            vs.append(nvar)
        varsides.append(vs)
    optsides = []
    for side,ps in enumerate(patterns):
        allopts = []
        for i,p in enumerate(ps):
            opts = []
            for s in range(3):
                orbits = sorted(set(mask for mask,_ in old.partition_options(len(p),i,s)))
                choicevars = []
                for mask in orbits:
                    nvar += 1
                    choicevars.append(nvar)
                    clauses.extend([-nvar, varsides[side][j]] for j in old._indices(mask))
                clauses.append([-varsides[side][i]] + choicevars)
                opts.append(orbits)
            allopts.append(opts)
        optsides.append(allopts)
    S = {tuple(perm[c] for c in p) for i,p in enumerate(old.patterns(6))
         if 2075405200>>i&1 for perm in permutations(range(4))}
    edges = set(tuple(sorted((a,b))) for bdy in boundaries
                for a,b in zip(bdy,bdy[1:]+bdy[:1]))
    forbidden = set()
    compatible = set()
    for f in product(range(4), repeat=m+5):
        if any(f[a]==f[b] for a,b in edges):
            continue
        ijs = tuple(indices[s][old.normalize(tuple(f[v] for v in b))]
                    for s,b in enumerate(boundaries))
        compatible.add(ijs)
        if f[:6] not in S:
            forbidden.add(ijs)
    clauses.extend([-varsides[0][i],-varsides[1][j]] for i,j in sorted(forbidden))
    seed = [0,1,2,1,2,1] + [3 if i%2==0 else 2 for i in range(m-1)]
    seed_indices = [indices[s][old.normalize(tuple(seed[v] for v in b))]
                    for s,b in enumerate(boundaries)]
    clauses.extend([[varsides[s][seed_indices[s]]] for s in range(2)])
    print('variables',nvar,'clauses',len(clauses),'forbidden',len(forbidden),'compatible',len(compatible),'seed',seed_indices,flush=True)
    started = time.time()
    with Solver(name='g4', bootstrap_with=clauses) as solver:
        sat = solver.solve()
        model = set(solver.get_model()) if sat else None
        if sat:
            for vs in varsides:
                for v in vs:
                    if v not in model or solver.solve(assumptions=[-v]):
                        solver.add_clause([-v])
                        assert solver.solve()
                        model = set(solver.get_model())
        stats = solver.accum_stats()
    result = dict(path_length=m,boundaries=boundaries,seed=seed,seed_indices=seed_indices,
                  n_vars=nvar,n_clauses=len(clauses),forbidden_pairs=len(forbidden),
                  compatible_pairs=len(compatible),sat=sat,stats=stats,seconds=time.time()-started)
    if sat:
        supports = [[i for i,v in enumerate(vs) if v in model] for vs in varsides]
        assert all(seed_indices[s] in supports[s] for s in range(2))
        assert not any((i,j) in forbidden for i in supports[0] for j in supports[1])
        for s, supp in enumerate(supports):
            mask = sum(1<<i for i in supp)
            assert all(any(mask & orbit == orbit for orbit in choices)
                       for i in supp for choices in optsides[s][i])
        result['support_indices'] = supports
        result['support_patterns'] = [[patterns[s][i] for i in supp] for s,supp in enumerate(supports)]
        print('SAT supports',list(map(len,supports)),flush=True)
    else:
        print('UNSAT',flush=True)
    out = Path(__file__).with_name(f'm{m}.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    for m in map(int, sys.argv[1:] or ['2','4']):
        run(m)
