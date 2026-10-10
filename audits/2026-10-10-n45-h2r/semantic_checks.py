"""Independent fixed toy and original-edge role schemas; none is a HIGH2 source."""
import copy
import itertools as it

COL = set(range(4))


def need(value, finding):
    if not value:
        raise ValueError(finding)


def connected(bag, edges):
    if not bag:
        return False
    seen = {min(bag)}
    while True:
        extra = {b for a, b in edges if a in seen and b in bag}
        extra |= {a for a, b in edges if b in seen and a in bag}
        if extra <= seen:
            return seen == bag
        seen |= extra


def minor(control, negative=False):
    edges = {tuple(sorted(e)) for e in control['edges']}
    bags = {k: set(v) for k, v in control['bags'].items()}
    vertices = set(control['vertices'])
    need(control['is_source'] is False, 'H2R-SCHEMA-SOURCE-CONFLATION')
    need(all(set(e) <= vertices and len(set(e)) == 2 for e in edges), 'H2R-ORIGINAL-EDGE')
    need(all(v <= vertices and connected(v, edges) for v in bags.values()), 'H2R-BAG-CONNECTIVITY')
    need(all(not bags[a] & bags[b] for a, b in it.combinations(bags, 2)), 'H2R-BAG-OVERLAP')
    for a, b in control['required_pairs']:
        holds = any((x in bags[a] and y in bags[b]) or
                    (y in bags[a] and x in bags[b]) for x, y in edges)
        if negative and not holds:
            raise ValueError('H2R-NEGATIVE-MISSING-ORIGINAL-ADJACENCY')
        need(holds, 'H2R-MISSING-ORIGINAL-ADJACENCY:' + a + ':' + b)


def run(witness, negative=False):
    scalar = witness['scalar_finding']
    row, T = scalar['gamma'], scalar['T_in_order']
    need(all(row[i] != row[(i + 1) % 5] for i in range(5)), 'H2R-SCALAR-NOT-PROPER')
    need(len({row[i] for i in T}) == 3 and len(set(row)) == 4 and not COL - set(row),
         'H2R-SCALAR-RAW-FINDING-NOT-PRESERVED')
    for control in witness['minor_controls']:
        minor(control)
    if negative:
        control = copy.deepcopy(witness['minor_controls'][1])
        control['edges'].remove(['b1', 'b2'])
        minor(control, negative=True)
        raise ValueError('H2R-NEGATIVE-FAILED-TO-REJECT')

    # One fixed graph, no geometry/source certificate. Its local degree identities
    # are retained, but beta-minimality, full Sigma and criticality are not asserted.
    cv = ['r', 'p0', 'p1', 'q']
    uv = ['uL', 'uR']
    variables = cv + uv + ['s']
    inside = [('r', 'p0'), ('r', 'p1'), ('r', 'q'), ('p0', 'p1'),
              ('uL', 'uR'), ('s', 'p0'), ('s', 'q'), ('s', 'uL'), ('s', 'uR')]
    boundary = [('r', 0), ('s', 3), ('p0', 0), ('p1', 0), ('p1', 1),
                ('q', 3), ('q', 4), ('uL', 1), ('uL', 2), ('uR', 2), ('uR', 3)]
    omitted = ('r', 4)
    summaries = []
    for row in [(0, 1, 0, 1, 2), (0, 1, 2, 3, 1), (0, 1, 2, 0, 1)]:
        components = []
        for vs in [cv, uv]:
            assignments = []
            for colors in it.product(range(4), repeat=len(vs)):
                f = dict(zip(vs, colors))
                if all(f[a] != f[b] for a, b in inside if a in f and b in f) and \
                   all(f[a] != row[b] for a, b in boundary if a in f):
                    assignments.append(tuple(colors))
            components.append(assignments)
        cf = {(t0, t1, c): [] for t0, t1, c in it.product(range(4), repeat=3)}
        uf = {(a, b): [] for a, b in it.product(range(4), repeat=2)}
        for f in components[0]:
            cf[(f[1], f[3], f[0])].append(f)
        for f in components[1]:
            uf[f].append(f)
        need(sum(map(len, cf.values())) == len(components[0]), 'H2R-C-FIBRE-PARTITION')
        need(sum(map(len, uf.values())) == len(components[1]), 'H2R-U-FIBRE-PARTITION')
        joined = set()
        for c, u, s, free in it.product(components[0], components[1], range(4), range(4)):
            if s != row[3] and s not in [c[1], c[3], u[0], u[1]]:
                joined.add(c + u + (s, free))
        direct_X, direct_G = set(), set()
        for colors in it.product(range(4), repeat=7):
            f = dict(zip(variables, colors))
            if all(f[a] != f[b] for a, b in inside) and \
               all(f[a] != row[b] for a, b in boundary):
                for free in range(4):
                    full = colors + (free,)
                    direct_X.add(full)
                    if f[omitted[0]] != row[omitted[1]]:
                        direct_G.add(full)
        need(joined == direct_X, 'H2R-FULL-X-RESTRICTION-UNION')
        restored = {f for f in joined if f[0] != row[4]}
        need(restored == direct_G, 'H2R-ORIGINAL-E-FULL-G-FIBRE')
        # Every ambient r/s pin is compared, including empty intersections.
        pin_counts = []
        for r, s in it.product(range(4), repeat=2):
            jx = {f for f in joined if f[0] == r and f[6] == s}
            dx = {f for f in direct_X if f[0] == r and f[6] == s}
            jg = {f for f in restored if f[0] == r and f[6] == s}
            dg = {f for f in direct_G if f[0] == r and f[6] == s}
            need(jx == dx and jg == dg, 'H2R-AMBIENT-ROOT-PIN-FIBRES')
            pin_counts.append([r, s, len(jx), len(jg)])
        if len(set(row)) == 3 and len({row[i] for i in [1, 2, 3]}) == 3:
            D = min(COL - set(row))
            need(any(f[0] == f[6] == D and f[4] == row[3] and f[5] == row[1]
                     for f in direct_G), 'H2R-QUALIFIED-THREE-COLOR-ORIGINAL-G')
        summaries.append({'row': list(row), 'classification': 'triggered and holds',
                          'C_ambient_fibres': 64, 'C_empty_fibres': sum(not v for v in cf.values()),
                          'U_ambient_fibres': 16, 'U_empty_fibres': sum(not v for v in uf.values()),
                          'X_full_lifts': len(direct_X), 'G_full_lifts': len(direct_G),
                          'all_16_root_pin_counts': pin_counts, 'isolated_free_factor': 4})
    return {'fixed_toy_rows': summaries, 'toy_is_HIGH2_source': False,
            'minor_controls': [{'id': c['id'], 'classification': c['classification']}
                               for c in witness['minor_controls']],
            'scalar_counterexample': 'H2R-EXCLUSION-FOUR-COLOR-UNUSED'}
