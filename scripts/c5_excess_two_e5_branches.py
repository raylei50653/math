#!/usr/bin/env python3
"""E5 branch/D5 arithmetic and exact 935 retained-core controls.

This replays only the four completed branch calculations, a scalar guard
identity, and nine saved-graph subgraphs. No new source keys, graph search,
four-colour oracle, or historical exact-target screens are used.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e5/branches.json'
B = tuple(range(5))
COLOURS = frozenset(range(4))
BASE = '2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac'


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def edge(u, v):
    return tuple(sorted((u, v)))


def normalize(row):
    # Orbit-index identification of the literal transported boundary row only.
    # No component relation or coloring witness is separately normalized.
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


def fixed_935_core_controls(graph, rows, q_index):
    assert graph['sigma_mask'] == 935 and graph['vertices'] == list(range(8))
    original = tuple(map(tuple, graph['all_edges']))
    cycle = tuple(edge(i, (i + 1) % 5) for i in B)
    controls = []
    for ha, hb in product((1, 2, 3), (0, 1, 4)):
        omitted = {edge(5, ha), edge(6, hb)}
        kept = tuple(e for e in original if e not in omitted)
        ds = {v: sum(v in e for e in kept) for v in (5, 6, 7)}
        assert ds == {5: 4, 6: 4, 7: 4}
        # Only the actual private vertex identities 5,6,7 are permitted.
        def fixed_tuples(edges, row):
            out = []
            for colours in product(range(4), repeat=3):
                f = dict(zip(B, row)); f.update(zip((5, 6, 7), colours))
                if all(f[u] != f[v] for u, v in edges):
                    out.append(colours)
            return out
        full = [fixed_tuples(kept, row) for row in rows]
        sigma = sum(1 << i for i, tuples in enumerate(full) if tuples)
        missing = [i for i in q_index.values() if not (sigma >> i & 1)]
        assert len(missing) <= 1
        witnesses = []
        if missing:
            i, = missing
            for e in kept:
                if e in cycle:
                    continue
                released = fixed_tuples(tuple(f for f in kept if f != e), rows[i])
                assert released
                colours = released[0]
                f = dict(zip(B, rows[i])); f.update(zip((5, 6, 7), colours))
                assert f[e[0]] == f[e[1]]
                witnesses.append(dict(deleted_actual_edge=e, literal_row_index=i,
                                      complete_original_vertex_colouring=f))
        # Original H is the same named triangle in every one of these controls.
        assert all(edge(u, v) in kept for u, v in ((5, 6), (5, 7), (6, 7)))
        controls.append(dict(omitted_original_spokes=[[5, ha], [6, hb]],
            remaining_original_edges=kept, degrees=ds, sigma=sigma,
            rejected_row_indices=missing, complete_ordered_roles=[5, 6, 7],
            full_relations=[[list(t) for t in tuples] for tuples in full],
            q_critical_edge_witnesses=witnesses,
            original_retained_mixed_contacts=dict(a=[7], b=[7]),
            status='Omega' if not missing else 'actual minimal-q all-degree-four core'))
    assert len(controls) == 9
    assert sum(c['sigma'] == 1023 for c in controls) == 4
    assert sorted((c['omitted_original_spokes'][0][1], c['omitted_original_spokes'][1][1],
                   c['rejected_row_indices'][0]) for c in controls if c['rejected_row_indices']) == [
        (1, 0, 6), (1, 1, 4), (2, 1, 3), (2, 4, 3), (3, 0, 6)]
    return controls


def build():
    paths = ('artifacts/c5_cells/cells.json',
             'artifacts/c5_excess_two_e3/positive_control_inputs.json',
             'artifacts/c5_excess_two_e3/adjacent_notes.md',
             'docs/c5_excess_two_mixed_core_spokes.md',
             'docs/c5_excess_two_mixed_core_four_spoke_mixed12.md',
             'docs/c5_two_spoke_three_contacts.md')
    raw = {p: (ROOT / p).read_bytes() for p in paths}
    cells = json.loads(raw[paths[0]])
    rows = tuple(map(tuple, cells['pattern_order']))
    q_index = {int(q): int(i) for i, q in cells['singleton_of_three_colour'].items()}
    assert q_index == {0: 6, 1: 4, 2: 3, 3: 1, 4: 0}
    phi = (1, 0, 4, 3, 2)
    transport_rows = []
    index_map = {}
    for i, row in enumerate(rows):
        literal = [None] * 5
        for v in B:
            literal[phi[v]] = row[v]
        j = rows.index(normalize(literal))
        index_map[i] = j
        transport_rows.append(dict(original_row_index=i, original_literal_row=row,
            literal_transported_row=literal, transported_orbit_index=j))
    branch_rows = []
    for mask in (941, 933, 940, 932):
        q = [v for v in B if not (mask >> q_index[v] & 1)]
        assert {0, 1, 3} <= set(q)
        transported = sum(1 << index_map[i] for i in range(10) if mask >> i & 1)
        assert transported == {941: 941, 933: 940, 940: 933, 932: 932}[mask]
        branch_rows.append(dict(mask=mask, rejected_singletons=q,
            accepted_three_colour_row_indices=[q_index[v] for v in B if v not in q],
            optional_q2_accepted=bool(mask >> q_index[2] & 1),
            optional_q4_accepted=bool(mask >> q_index[4] & 1),
            common_D5_transported_mask=transported,
            common_D5_transported_rejected_singletons=sorted(phi[v] for v in q),
            transported_selected_triple=sorted(phi[v] for v in (0, 1, 3))))
    guards = []
    domains = [frozenset(c for c in COLOURS if bits >> c & 1) for bits in range(1, 16)]
    for p_domain, u_domain in product(domains, repeat=2):
        if any(a != u for a, u in product(p_domain, u_domain)):
            continue
        assert p_domain == u_domain and len(p_domain) == 1
        guards.append(dict(P_N=sorted(p_domain), R_U=sorted(u_domain)))
    assert len(guards) == 4
    exact = json.loads(raw[paths[1]])
    rec, = [r for r in exact['records'] if r['graph']['sigma_mask'] == 935]
    assert sha256(canonical(rec['graph'])).hexdigest() == rec['record_sha256']
    actual = fixed_935_core_controls(rec['graph'], rows, q_index)
    return dict(schema='e5-completed-branch-arithmetic-v1', base=BASE,
        sources_sha256={p: sha256(v).hexdigest() for p, v in raw.items()},
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        four_exact_branches=branch_rows,
        common_D5=dict(phi=phi, boundary_rows=transport_rows,
            role_transport='Interior/root/contact names are retained; every actual boundary attachment h is moved to phi(h). Colors stay literal before orbit indexing.'),
        full_relation_scalar_guard=dict(nonempty_domain_pairs_checked=225,
            all_rejecting_domain_pairs=guards,
            premise='Complete N and U relations are independent after deleting the original a-u edge; no coordinate marginals.'),
        exact_935_original_record_sha256=rec['record_sha256'],
        nine_actual_935_degree_four_predecessors=actual,
        E3_table_scope_finding=dict(location='adjacent_notes.md A identity row and REPORT.md portability A row',
            issue='The asserted need to finish general spoke+unary (4,4) predecessors is too strong for retained mixed incidence (1,2).',
            distinction='The historical proof did cite general (4,4) exclusion. E5 supplies its incidence-specific derivation; no historical certificate is invalidated or rewritten.',
            stop='No additional mathematical investigation after this finding; only saved-graph replay and delivery.'),
        evidence_boundary='Finite branch/guard/control checks only. Unbounded graph exclusions and applicability finding are paper arguments.',
        no_four_colour_or_planarity_oracle=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    payload = (json.dumps(build(), sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    if args.check:
        assert OUT.read_bytes() == payload, 'E5 branch artifact byte mismatch'
        print('CHECK OK: four branches, literal common D5, 225 guards, nine actual 935 retained cores')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open('xb') as f:
            f.write(payload)
        print('CREATED', OUT)
    print('sha256', sha256(payload).hexdigest(), 'bytes', len(payload))


if __name__ == '__main__':
    main()
