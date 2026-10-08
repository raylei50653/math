#!/usr/bin/env python3
"""E5 fixed E1 graph controls only; no source search and no four-colour oracle.

All colouring loops below are bounded to the two exact, saved E1 representatives.
The arbitrary-size arguments remain paper arguments in REPORT.md. Generation
uses exclusive create; --check replays bytes without modifying any file.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

B = tuple(range(5))
CYCLE = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in B))
COLOURS = frozenset(range(4))
TRIPLE = (0, 1, 3)
E1_SHA = '23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e'
BASE = '2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def edge(u, v):
    return tuple(sorted((u, v)))


def profile(mask, singleton_indices):
    return sorted(q for q, i in singleton_indices.items() if not (mask >> i & 1))


def adjacent_profile(q):
    return len(q) <= 1 or (len(q) == 2 and edge(*q) in CYCLE)


def fixed_control(record, patterns, singleton_indices):
    graph = record['graph']
    assert sha256(canonical(graph)).hexdigest() == record['record_sha256']
    sigma = graph['sigma_mask']
    assert sigma in (935, 951)
    verts = tuple(graph['vertices'])
    private = tuple(v for v in verts if v not in B)
    assert (sigma, private) in ((935, (5, 6, 7)), (951, (5, 6, 7, 8, 9)))
    nonframe = tuple(map(tuple, graph['nonframe_edges']))
    edges = CYCLE + nonframe
    assert sorted(edges) == list(map(tuple, graph['all_edges']))
    full_bits = (1 << len(nonframe)) - 1
    # A finite assignment certificate for exactly these saved controls. A bit
    # denotes an actual, named control edge whose endpoints have equal colours.
    candidates = []
    for row in patterns:
        row_candidates = []
        for colours in product(range(4), repeat=len(private)):
            f = dict(zip(B, row))
            f.update(zip(private, colours))
            equal_bits = sum(1 << j for j, (u, v) in enumerate(nonframe) if f[u] == f[v])
            row_candidates.append((equal_bits, colours))
        candidates.append(row_candidates)

    def relations(bits, roles=private):
        indices = [private.index(v) for v in roles]
        return [sorted({tuple(colours[j] for j in indices)
                        for equal, colours in row if not (equal & bits)})
                for row in candidates]

    def mask(bits):
        return sum(1 << i for i, row in enumerate(candidates)
                   if any(not (equal & bits) for equal, _ in row))

    def edge_bits(kept_edges):
        return sum(1 << i for i, e in enumerate(nonframe) if e in kept_edges)

    assert mask(full_bits) == sigma
    full_relations = relations(full_bits)
    assert profile(sigma, singleton_indices) == graph['Q']
    degrees = Counter(v for e in edges for v in e)
    assert sorted(degrees[v] for v in private) == graph['private_degree_sequence']
    assert sum(degrees[v] - 4 for v in private) == 2
    assert sigma & 932 == 932
    critical = []
    for old in graph['critical_edges']:
        e = tuple(old['edge'])
        i = nonframe.index(e)
        after = mask(full_bits ^ (1 << i))
        assert after == old['sigma_after_deletion'] and after != sigma
        f = {int(v): c for v, c in old['colouring'].items()}
        assert tuple(f[b] for b in B) == patterns[old['pattern_index']]
        assert all(f[u] != f[v] for u, v in edges if (u, v) != e)
        assert f[e[0]] == f[e[1]]
        critical.append(old)

    result = dict(source_pointer=record['pointer'], record_sha256=record['record_sha256'],
                  original_graph=graph, recomputed_sigma=sigma,
                  complete_same_frame_private_relations=[dict(index=i, boundary=list(patterns[i]),
                      roles=list(private), tuples=[list(t) for t in tuples])
                      for i, tuples in enumerate(full_relations)],
                  critical_edge_count=len(critical), selected_triple_hypothesis=False)
    assert not set(TRIPLE) <= set(graph['Q'])
    if sigma == 951:
        omissions = []
        for piece in ((6, 9), (7, 8)):
            kept = {e for e in nonframe if not (set(e) & set(piece))}
            roles = tuple(v for v in private if v not in piece)
            bits = edge_bits(kept)
            omissions.append(dict(original_piece=list(piece), kept_roles=list(roles),
                kept_nonframe_edges=[list(e) for e in nonframe if e in kept], sigma=mask(bits),
                complete_private_relations=[[list(t) for t in row] for row in relations(bits, roles)]))
        assert [r['sigma'] for r in omissions] == [959, 1015]
        result['binary_omissions_are_not_Omega'] = omissions
        result['scope'] = 'Exact 951 edge witnesses and two original binary omissions; not all 65536 subgraphs.'
        return result

    assert private == (5, 6, 7) and degrees[7] == 4
    # Every edge subset of the exact 935 graph is a positive control, not a
    # source-key/graph census. Preserve bit-to-named-edge provenance above.
    proper = []
    valid = []
    q_counts = Counter()
    for bits in range(full_bits + 1):
        kept = tuple(e for i, e in enumerate(nonframe) if bits >> i & 1)
        ds = Counter(v for e in CYCLE + kept for v in e)
        active = tuple(v for v in private if ds[v])
        eps = sum(ds[v] - 4 for v in active)
        value = mask(bits)
        q = profile(value, singleton_indices)
        row = dict(kept_nonframe_bits=bits, sigma=value, Q=q)
        if bits != full_bits:
            assert adjacent_profile(q)
            proper.append(row)
            q_counts[','.join(map(str, q))] += 1
        if all(ds[v] >= 4 for v in active):
            assert eps <= 2
            if eps == 2:
                assert bits == full_bits
            if eps == 0:
                assert len(q) <= 1
            if eps == 1:
                assert adjacent_profile(q)
            valid.append(dict(**row, effective_vertices=list(active), epsilon=eps,
                degrees={str(v): ds[v] for v in active},
                nonframe_edges=[list(e) for e in kept]))
    assert len(proper) == 2047 and len(valid) == 19
    result['proper_subgraphs'] = dict(edge_subsets_checked=2048, proper_count=len(proper),
        Q_profile_histogram=dict(sorted(q_counts.items())), degree_valid=valid,
        all_proper_subgraph_profiles=proper, same_epsilon_two_subgraphs=1)

    # General leaf slack tested on the actual 935 K=C+a and actual contacts
    # (a,7), retaining the shared-contact identity C={7}.
    leaf_records = []
    for a, b in ((5, 6), (6, 5)):
        sa = tuple(h for h in B if edge(a, h) in edges)
        for i, row in enumerate(patterns):
            for j in sa:
                if not any(row[j] == row[k] for k in sa if k != j):
                    continue
                lset = COLOURS - {row[k] for k in sa if k != j}
                assert len(lset) == 2
                kept = {e for e in nonframe if b not in e and e != edge(a, j)}
                tuples = relations(edge_bits(kept), (a, 7))[i]
                assert tuples
                forbidden = set.intersection(*(set(t) for t in tuples))
                assert forbidden <= lset
                avoid = []
                for d in sorted(COLOURS - lset):
                    witness = next(t for t in tuples if d not in t)
                    avoid.append(dict(fixed_b_colour=d, complete_K_tuple=list(witness)))
                leaf_records.append(dict(row_index=i, boundary=list(row), roots=[a, b],
                    omitted_actual_spoke=[a, j], contacts=[a, 7], L=sorted(lset),
                    complete_K_relation=[list(t) for t in tuples], F_K=sorted(forbidden),
                    witnesses_avoiding_each_colour_outside_L=avoid))
    assert leaf_records
    result['actual_leaf_slack'] = leaf_records

    pins = []
    counts = Counter()
    outside_edges = tuple(e for e in edges if 7 not in e)
    for i, row in enumerate(patterns):
        for a_colour, b_colour in product(range(4), repeat=2):
            f = dict(zip(B, row)); f.update({5: a_colour, 6: b_colour})
            if not all(f[u] != f[v] for u, v in outside_edges):
                continue
            actual_neighbours = [v for v in verts if edge(7, v) in edges]
            used = {f[v] for v in actual_neighbours}
            allowed = sorted(COLOURS - used)
            assert bool(allowed) == (len(used) <= 3)
            counts[len(used)] += 1
            pins.append(dict(row_index=i, boundary=list(row), complete_outside_colouring=f,
                actual_neighbours=actual_neighbours, neighbour_colours=sorted(used),
                complete_C_relation=[[c] for c in allowed], extension_exists=bool(allowed)))
    assert dict(counts) == {2: 1, 3: 6, 4: 4}
    result['singleton_external_pins'] = pins
    result['external_colour_histogram'] = {str(k): v for k, v in sorted(counts.items())}

    # One whole-graph D5 transport, preserving literal colours and all roles.
    phi = (1, 0, 4, 3, 2)
    relabel = {v: phi[v] if v in B else v for v in verts}
    transported_edges = sorted(edge(relabel[u], relabel[v]) for u, v in edges)
    transported_rotation = {str(relabel[int(v)]): [relabel[w] for w in ns]
        for v, ns in graph['embedding']['disk_rotation'].items()}
    transported_relations = []
    for i, row in enumerate(patterns):
        literal = [None] * 5
        for v in B:
            literal[phi[v]] = row[v]
        witnesses = []
        for colours in full_relations[i]:
            f = dict(zip(B, row)); f.update(zip(private, colours))
            transported = {relabel[v]: c for v, c in f.items()}
            assert all(transported[u] != transported[v] for u, v in transported_edges)
            assert [transported[v] for v in B] == literal
            witnesses.append(transported)
        transported_relations.append(dict(original_index=i, literal_transported_row=literal,
            private_roles=list(private), entire_graph_witnesses=witnesses))
    result['actual_common_D5_transport'] = dict(phi=list(phi), original_graph_role_map=relabel,
        edges=[list(e) for e in transported_edges], transported_original_rotation=transported_rotation,
        complete_literal_relations=transported_relations)
    result['not_applicable_conditions'] = dict(
        selected_triple='Q935={0,1,2}; q3 is accepted',
        J2_J3='935 has three spokes at both roots, not the five/four-spoke incidence patterns',
        A_equal_pair='Original 935 spoke sets are 123 and 014, not equal',
        B_terminal_leaf='Original C={7}, incidence (1,1), deg_C(7)=0; no bridge/odd-cycle terminal block',
        shared_leaf_parity='C-v empty and degree_C(v)=0, not the required nonempty bridge remainder')
    return result


def build(root):
    source_paths = ('artifacts/c5_cells/cells.json',
                    'artifacts/c5_excess_two_e3/positive_control_inputs.json',
                    'artifacts/c5_excess_one_e2/REPORT.md',
                    'artifacts/c5_excess_two_e3/REPORT.md',
                    'artifacts/c5_excess_two_e3/adjacent_notes.md')
    source_raw = {p: (root / p).read_bytes() for p in source_paths}
    cells = json.loads(source_raw[source_paths[0]])
    patterns = tuple(map(tuple, cells['pattern_order']))
    singles = {next(v for v in B if row.count(row[v]) == 1): i
               for i, row in enumerate(patterns) if len(set(row)) == 3}
    assert singles == {4: 0, 3: 1, 2: 3, 1: 4, 0: 6}
    inputs = json.loads(source_raw[source_paths[1]])
    assert inputs['source_sha256'] == E1_SHA
    controls = [fixed_control(r, patterns, singles) for r in inputs['records']]
    assert [c['recomputed_sigma'] for c in controls] == [951, 935]
    return dict(schema='e5-fixed-controls-v1', base=BASE,
        source_sha256={p: sha256(raw).hexdigest() for p, raw in source_raw.items()},
        evidence_boundary='Finite checks of the two exact saved E1 graphs only. Paper arbitrary-size lemmas are not proved by these loops.',
        four_colour_oracle_used=False, source_key_enumeration=False, positive_controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = args.output or args.root / 'artifacts/c5_excess_two_e5/controls.json'
    raw = (json.dumps(build(args.root), sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    if args.check:
        if output.read_bytes() != raw:
            raise SystemExit('CHECK FAILED: fixed controls artifact byte mismatch')
        print('CHECK OK: exact 935 all 2048 subgraphs, complete leaf/pin/D5 controls; 951 omissions 959/1015')
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as stream:
            stream.write(raw)
        print('CREATED', output)
    print('sha256', sha256(raw).hexdigest(), 'bytes', len(raw))


if __name__ == '__main__':
    main()
