"""Fixed position/color arithmetic only: no source graph and no theorem machine proof."""
from itertools import product, combinations, permutations


def calculate():
    col = set(range(4))
    edges = [frozenset((i, (i + 1) % 5)) for i in range(5)]
    rows = [b for b in product(range(4), repeat=5)
            if all(b[i] != b[(i + 1) % 5] for i in range(5))]
    three = [b for b in rows if len(set(b)) == 3]
    assert len(rows) == 240 and len(three) == 120
    consecutive_tests = []
    for b in three:
        singleton = next(i for i, c in enumerate(b) if b.count(c) == 1)
        for start in range(5):
            T = tuple((start + j) % 5 for j in range(3))
            assert (len({b[i] for i in T}) == 3) == (singleton in T)
            consecutive_tests.append({'row':b,'support':T,'singleton':singleton})
    arcs = []
    for p, q in permutations(range(5), 2):
        if edges[p] & edges[q]:
            continue
        remaining = set(range(5)) - {p,q}
        pairs = [tuple((i+j)%5 for j in range(2)) for i in range(5)
                 if {(i+j)%5 for j in range(2)} <= remaining]
        assert len(pairs) == 1
        arcs.append({'P_edge':p,'Q_edge':q,'remaining':sorted(remaining),
                     'unique_length_two':pairs[0]})
    assert len(arcs) == 10
    k33_tests = 0
    for v in range(5):
        O = set(range(5)) - {v}
        assert len(O) == 4
        for _order in range(2):
            for r_spokes in combinations(range(5),2):
                for s_spokes in combinations(range(5),2):
                    assert set(r_spokes)&O and set(s_spokes)&O
                    k33_tests += 1
    assert k33_tests == 1000
    stabilizer_tests = 0
    for b in three:
        D = next(iter(col - set(b)))
        for start in range(5):
            T = {(start+j)%5 for j in range(3)}
            missing = set(b)-{b[i] for i in T}
            for h in sorted(missing):
                swap=lambda c:h if c==D else D if c==h else c
                assert all(swap(b[i]) == b[i] for i in T)
                for F in [set()] + [{c} for c in range(4)]:
                    if {swap(c) for c in F} == F:
                        assert D not in F
                    stabilizer_tests += 1
    orbit_tests=[]
    for Q in ({0,1,2,3},{0,1,3}):
        for shift in range(5):
            for sign in (-1,1):
                moved={(shift+sign*i)%5 for i in Q}
                for start in range(5):
                    T={(start+j)%5 for j in range(3)}
                    assert not moved <= T
                    orbit_tests.append({'Q':sorted(Q),'shift':shift,'sign':sign,
                                        'support':sorted(T)})
    return {'scope':'fixed position/color arithmetic; no finite HIGH1 source',
            'status':'triggered and holds for calibration only',
            'proper_literal_rows':len(rows),'three_color_literal_rows':len(three),
            'consecutive_support_tests':len(consecutive_tests),
            'disjoint_support_edge_metadata':arcs,'K33_spoke_adjacency_schemas':k33_tests,
            'unary_stabilizer_tests':stabilizer_tests,'rejection_orbit_tests':orbit_tests,
            'machine_proves_paper_claims':False,'source_control_established':False,
            'source_control_executed':False,'trigger_count':None,'new_Lean':False}
