#!/usr/bin/env python3
"""Singleton four-colour diagonal Kempe transport; exclusive-create/replay.

Only pure functions are imported from the two existing Kempe modules.
No screen report, exterior test, catalogue search, or four-colour oracle runs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx
from c5_kempe_screen import REPS, normalize, partitions
from c5_kempe_transport_table import (
    admissible_partitions, block_swap, canonical_partition, disk_embedding,
    independent_partitions,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_kempe_diagonal_transport'
BASE = '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090'
INDEX = {q: i for i, q in enumerate(REPS)}
FRAME = tuple(range(5))
FRAME_EDGES = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in FRAME))
LITERAL_ROWS = tuple(q for q in product(range(4), repeat=5)
                     if all(q[i] != q[(i + 1) % 5] for i in FRAME))


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


@lru_cache(None)
def compatible(q, split):
    rows = admissible_partitions(q, split, partitions)
    assert rows == admissible_partitions(q, split, independent_partitions)
    return tuple(rows)


def swap_record(q, pair, block, endpoint, sigma):
    literal = block_swap(q, pair, block)
    index = INDEX[normalize(literal)]
    return dict(endpoint=endpoint, colour_pair=pair, frame_block=block,
                q_prime=literal, normalized_q_prime=normalize(literal),
                q_prime_index=index, in_sigma=bool(sigma >> index & 1))


def table(sigma):
    counts = Counter()
    records = []
    grouped = {}
    serial_l2 = 0
    for q in LITERAL_ROWS:
        qi = INDEX[normalize(q)]
        if sigma >> qi & 1:
            continue
        counts['literal_rejects'] += 1
        for a in FRAME:
            b = (a + 1) % 5
            group = grouped.setdefault((qi, a), Counter())
            remaining = sorted(set(range(4)) - {q[a], q[b]})
            for cz, cw in permutations(remaining):
                left = tuple(sorted((q[a], cz)))
                right = tuple(sorted((q[b], cw)))
                split = tuple(sorted((left, right)))
                for pi_index, pi in enumerate(compatible(q, split)):
                    counts['partition_contexts'] += 1
                    ab = next(bl for bl in pi if a in bl)
                    bb = next(bl for bl in pi if b in bl)
                    z_options = (None,) + tuple(bl for bl in pi if q[bl[0]] in left)
                    w_options = (None,) + tuple(bl for bl in pi if q[bl[0]] in right)
                    for zb, wb in product(z_options, w_options):
                        counts['assignments_including_empty'] += 1
                        if zb is None or wb is None:
                            # Lemma 3: an empty root block is disconnected, and
                            # its useful swap would leave the rejected q fixed.
                            counts['excluded_empty_root_block'] += 1
                            continue
                        counts['nonempty_assignments'] += 1
                        az, bw = ab == zb, bb == wb
                        if az and bw:
                            counts['excluded_both_connected'] += 1
                            continue
                        swaps = []
                        if not az:
                            swaps.extend((swap_record(q, left, ab, 'a', sigma),
                                          swap_record(q, left, zb, 'z', sigma)))
                        if not bw:
                            swaps.extend((swap_record(q, right, bb, 'b', sigma),
                                          swap_record(q, right, wb, 'w', sigma)))
                        if not all(s['in_sigma'] for s in swaps):
                            counts['excluded_required_swap_outside_sigma'] += 1
                            continue
                        case = ('az_connected' if az else 'bw_connected' if bw
                                else 'both_disconnected')
                        counts['L1'] += 1
                        counts['L1_' + case] += 1
                        group['L1'] += 1
                        group['L1_' + case] += 1
                        l2 = not az and not bw
                        if l2:
                            serial_l2 += 1
                            counts['L2'] += 1
                            group['L2'] += 1
                            rid = f'KD{sigma}-{serial_l2:04d}'
                        else:
                            rid = f'KD{sigma}-L1-{counts["L1"]:04d}'
                        records.append(dict(
                            id=rid, sigma=sigma, q=q, q_index=qi, a=a, b=b,
                            directed_frame_edge=(a, b), root_colours=dict(z=cz, w=cw),
                            diagonal_pairs=dict(az=left, bw=right), split=split,
                            compatible_partition_index=pi_index, pi=pi,
                            endpoint_blocks=dict(a=ab, b=bb, z=zb, w=wb),
                            connected=dict(az=az, bw=bw), case=case,
                            required_swaps=swaps, L1=True, L2=l2,
                            L2_reason=('both_disconnected_no_connected_diagonal_curve'
                                       if l2 else 'connected_diagonal_traps_opposite_root_component_off_frame')))
    counts.setdefault('L1', 0)
    counts.setdefault('L2', 0)
    assert counts['nonempty_assignments'] == (counts['excluded_both_connected']
            + counts['excluded_required_swap_outside_sigma'] + counts['L1'])
    summary = dict(sigma=sigma, rejected_indices=[i for i in range(10) if not sigma >> i & 1],
                   counts=dict(sorted(counts.items())),
                   results_by_q_index_and_edge=[dict(q_index=qi, representative=REPS[qi],
                       edge=(a, (a + 1) % 5), counts=dict(sorted(group.items())))
                       for (qi, a), group in sorted(grouped.items())])
    return summary, records


def finite_sigma(g):
    """Elementary finite backtracking, followed by one global S4 orbit."""
    inner = sorted(set(g) - set(FRAME), key=lambda v: (-g.degree(v), v))
    witnesses = {}
    for qi, q in enumerate(REPS):
        f = dict(enumerate(q))
        def visit(i):
            if i == len(inner):
                return dict(f)
            v = inner[i]
            for c in range(4):
                if all(f.get(w) != c for w in g[v]):
                    f[v] = c
                    found = visit(i + 1)
                    if found is not None:
                        return found
                    del f[v]
            return None
        found = visit(0)
        if found is not None:
            witnesses[str(qi)] = {str(v): c for v, c in sorted(found.items())}
    indices = sorted(map(int, witnesses))
    rows = sorted({tuple(perm[c] for c in REPS[qi]) for qi in indices
                   for perm in permutations(range(4))})
    return dict(mask=sum(1 << qi for qi in indices), accepted_indices=indices,
                complete_ordered_rows=rows, representative_extensions=witnesses)


def extract_control(name, graph_data, p, a, b, z, w, psi, sigma, records):
    g = nx.Graph()
    g.add_nodes_from(graph_data['vertices'])
    g.add_edges_from(graph_data['edges'])
    assert set(g[p]) == {a, b, z, w}
    assert g.has_edge(a, b) and g.has_edge(z, w)
    assert g.degree(z) == g.degree(w) == 5 and g.degree(p) == 4
    assert all(psi[u] != psi[v] for u, v in g.edges() if p not in (u, v))
    q = tuple(psi[v] for v in FRAME)
    assert len({psi[v] for v in g[p]}) == 4
    assert not sigma >> INDEX[normalize(q)] & 1
    actual_sigma = finite_sigma(g)
    assert actual_sigma['mask'] == sigma
    rotations = graph_data['embedding']['rotation']
    rotation = (rotations[str(p)] if isinstance(rotations, dict)
                else next(r['clockwise'] for r in rotations if r['vertex'] == p))
    desired = [a, b, z, w]
    assert any((rotation + rotation)[i:i + 4] == desired for i in range(4)) or any(
        (rotation[::-1] + rotation[::-1])[i:i + 4] == desired for i in range(4))
    ext = g.subgraph(set(g) - {p})
    split = tuple(sorted((tuple(sorted((psi[a], psi[z]))),
                          tuple(sorted((psi[b], psi[w]))))))
    chains = []
    blocks = []
    endpoints = {}
    for pair in split:
        sub = ext.subgraph(v for v in ext if psi[v] in pair)
        for chain in sorted(tuple(sorted(c)) for c in nx.connected_components(sub)):
            block = tuple(v for v in chain if v in FRAME)
            if block:
                blocks.append(block)
            chains.append(dict(colour_pair=pair, vertices=chain, frame_block=block))
            for role, v in (('a', a), ('b', b), ('z', z), ('w', w)):
                if v in chain:
                    endpoints[role] = block
    pi = canonical_partition(blocks)
    matches = [r for r in records if r['q'] == q and r['a'] == a and r['b'] == b
               and r['root_colours'] == dict(z=psi[z], w=psi[w]) and r['pi'] == pi
               and r['endpoint_blocks'] == endpoints]
    assert len(matches) == 1 and matches[0]['L2'], (name, matches)
    row = matches[0]
    actual_swaps = []
    for swap in row['required_swaps']:
        chain = next(c['vertices'] for c in chains if c['frame_block'] == swap['frame_block'])
        pair = swap['colour_pair']
        new = dict(psi)
        for v in chain:
            new[v] = pair[1] if psi[v] == pair[0] else pair[0]
        missing = sorted(set(range(4)) - {new[v] for v in g[p]})
        assert missing and tuple(new[v] for v in FRAME) == swap['q_prime']
        new[p] = missing[0]
        assert all(new[u] != new[v] for u, v in g.edges())
        actual_swaps.append(dict(endpoint=swap['endpoint'], vertices=chain,
            extension_colour=missing[0], full_extension={str(v): c for v, c in sorted(new.items())},
            **{k: v for k, v in swap.items() if k != 'endpoint'}))
    return dict(name=name, graph_vertices=list(g), graph_edges=sorted(tuple(sorted(e)) for e in g.edges()),
                vertex_roles=dict(a=a, b=b, z=z, w=w, p=p), psi={str(v):c for v,c in sorted(psi.items())},
                rotation_at_p=rotation, matching_assignment_id=row['id'], assignment=row,
                actual_chains=chains, actual_useful_swaps=actual_swaps,
                recomputed_full_sigma=actual_sigma, L1=True, L2=True)


def controls(all_records):
    p1 = json.loads((ROOT / 'artifacts/c5_kempe_transport/P1-witness-001.json').read_bytes())
    psi = {int(v): c for v, c in p1['psi'].items()}
    first = extract_control(p1['id'], p1, 7, 0, 1, 5, 6, psi, 1012, all_records[1012])
    # Literal, point-by-point checks against Task K's saved useful swaps.
    for swap in first['actual_useful_swaps']:
        old = next(s for s in p1['kempe_swaps'] if tuple(s['vertices']) == tuple(swap['vertices'])
                   and tuple(s['color_pair']) == tuple(swap['colour_pair']))
        assert old['extends'] and old['q_prime_in_actual_sigma']
        assert tuple(old['q_prime']) == swap['q_prime'] and old['pattern_prime'] == swap['q_prime_index']
        assert old['psi_prime'] == {k: v for k, v in swap['full_extension'].items() if k != '7'}
    s935 = json.loads((ROOT / 'artifacts/c5_shield_calibration/counterexample_S935.json').read_bytes())
    others = []
    for rejected in s935['rejected_pattern_G_minus_P_witnesses']:
        for wi, witness in enumerate(rejected['witnesses']):
            psi = dict(witness['colours_by_vertex'])
            others.append(extract_control(f'S935-q{rejected["pattern_index"]}-psi{wi}',
                s935['graph'], 5, 3, 4, 6, 7, psi, 935, all_records[935]))
    assert len(others) == 2
    return [first] + others


def bounded_realization(named):
    """Smallest disk attempt: exactly B, z=5, w=6, p=7; no enlargement."""
    counts = Counter()
    disk_rows = []
    match_rows = {r['id']: [] for r in named}
    for a in FRAME:
        b = (a + 1) % 5
        for z_spokes, w_spokes in product(combinations(FRAME, 3), repeat=2):
            counts['wirings'] += 1
            g = nx.Graph()
            g.add_nodes_from(range(8))
            g.add_edges_from(FRAME_EDGES)
            g.add_edges_from(((5, 6), (7, a), (7, b), (7, 5), (7, 6)))
            g.add_edges_from((5, v) for v in z_spokes)
            g.add_edges_from((6, v) for v in w_spokes)
            assert [g.degree(v) for v in (5, 6, 7)] == [5, 5, 4]
            if any(not (set(g[v]) - set(FRAME)) for v in FRAME):
                continue
            counts['full_frame_contact'] += 1
            embedding = disk_embedding(g)
            if embedding is None:
                continue
            counts['disk'] += 1
            sig = finite_sigma(g)
            counts['disk_sigma_' + str(sig['mask'])] += 1
            assert sig['mask'] & 932 == 932
            deletions = []
            for e in sorted(tuple(sorted(e)) for e in g.edges()):
                if e in FRAME_EDGES:
                    continue
                h = nx.Graph(g)
                h.remove_edge(*e)
                ds = finite_sigma(h)
                gained = sorted(set(ds['accepted_indices']) - set(sig['accepted_indices']))
                deletions.append(dict(edge=e, full_sigma=ds, gained_indices=gained, critical=bool(gained)))
            critical = all(d['critical'] for d in deletions)
            counts['T4_and_sigma_critical'] += int(critical)
            rid = f'KD-disk8-{counts["disk"]:03d}'
            disk_rows.append(dict(id=rid, a=a, b=b, z_spokes=z_spokes, w_spokes=w_spokes,
                vertices=list(g), edges=sorted(tuple(sorted(e)) for e in g.edges()),
                degrees={str(v): g.degree(v) for v in sorted(g)}, embedding=embedding,
                full_sigma=sig, nonframe_edge_deletions=deletions, sigma_critical=critical))
            for candidate in named:
                if candidate['a'] != a:
                    continue
                psi = dict(enumerate(candidate['q'])) | {5: candidate['root_colours']['z'],
                                                        6: candidate['root_colours']['w']}
                proper = all(psi[u] != psi[v] for u, v in g.edges() if 7 not in (u, v))
                match_rows[candidate['id']].append(dict(graph_id=rid, proper_external_psi=proper,
                    sigma_matches_target=sig['mask'] == candidate['sigma']))
    assert counts['wirings'] == 500
    return dict(domain=dict(vertices=list(range(8)), private_vertices=[5, 6, 7],
        P=[7], roots=[5, 6], roots_degree=5, P_degree=4,
        all_five_directed_frame_edges=True, each_root_spoke_subsets_of_size=3,
        full_frame_contact=True, no_graph_or_D5_quotient=True,
        no_additional_private_vertices=True), counts=dict(sorted(counts.items())),
        disk_graphs=disk_rows, named_candidate_attempts=match_rows,
        realized_target_count=sum(r['full_sigma']['mask'] in (933, 941) for r in disk_rows),
        conclusion='No fixed 933/941 source in this eight-vertex domain; larger realizations remain untested.')


def build():
    assert nx.__version__ == '3.5', 'Replay requires networkx==3.5.'
    cells = ROOT / 'artifacts/c5_cells/cells.json'
    assert json.loads(cells.read_bytes())['pattern_order'] == [list(q) for q in REPS]
    assert len(LITERAL_ROWS) == 240
    for n, bell in enumerate((1, 1, 2, 5, 15, 52)):
        recursive = {canonical_partition(p) for p in partitions(list(range(n)))}
        assert recursive == independent_partitions(list(range(n))) and len(recursive) == bell
    summaries = []
    all_records = {}
    for sigma in (933, 941, 1012, 935):
        summary, records = table(sigma)
        summaries.append(summary)
        all_records[sigma] = records
    assert [(s['counts']['L1'], s['counts']['L2']) for s in summaries] == [
        (2112, 192), (2304, 384), (1728, 192), (1728, 192)]
    control_rows = controls(all_records)
    named = [next(r for r in all_records[s] if r['L2']) for s in (933, 941)]
    attempt = bounded_realization(named)
    flat = [r for s in (933, 941, 1012, 935) for r in all_records[s]]
    record_bytes = b''.join((json.dumps(r, sort_keys=True, separators=(',', ':')) + '\n').encode() for r in flat)
    inputs = (cells, ROOT / 'scripts/c5_kempe_screen.py',
        ROOT / 'scripts/c5_kempe_transport_table.py', Path(__file__),
        ROOT / 'artifacts/c5_kempe_transport/P1-witness-001.json',
        ROOT / 'artifacts/c5_shield_calibration/counterexample_S935.json')
    observations = dict(schema='c5-kempe-diagonal-transport-v1', base_commit=BASE,
        inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        networkx_version=nx.__version__,
        trust=dict(paper='Necessary diagonal-swap incidence plus connected-diagonal Jordan side lemma.',
            external='Jordan curve theorem; no 4CT/Gallai/hub inference.',
            python='All 240 literal frame rows, exact endpoint-block choices and bounded eight-vertex attempts.',
            lean='No new theorem; no lake build.'),
        domain=dict(P_size=1, four_distinct_neighbor_colours=True,
            neighbor_roles=['a', 'b', 'z', 'w'], roots_adjacent=True, roots_degree=5,
            frame=list(FRAME), directed_edges=[(a, (a+1)%5) for a in FRAME],
            all_literal_rows=True, D5_quotient=False, S4_quotient=False,
            S4_normalization_only_for_mask_lookup=True, empty_root_blocks_enumerated_then_rejected=True),
        tables=summaries, controls=[dict(name=r['name'], assignment_id=r['matching_assignment_id'],
            L1=r['L1'], L2=r['L2'], useful_swaps=len(r['actual_useful_swaps'])) for r in control_rows],
        assignments=dict(file='assignments.jsonl', rows=len(flat), sha256=sha256(record_bytes).hexdigest()),
        named_target_survivors=[r['id'] for r in named],
        bounded_realization_summary=dict(counts=attempt['counts'], realized_target_count=attempt['realized_target_count']),
        conclusion='STOP: L2 survivors remain for both targets. Neither fixed-source exclusion nor Kprime is proved.')
    files = {'observations.json': encoded(observations), 'assignments.jsonl': record_bytes,
             'controls.json': encoded(control_rows), 'bounded_realization.json': encoded(attempt)}
    files.update({r['id'] + '.json': encoded(r) for r in named})
    return observations, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    observations, files = build()
    if args.check:
        for name, payload in files.items():
            assert (args.output / name).read_bytes() == payload, f'Byte mismatch: {name}'
    else:
        assert not any((args.output / name).exists() for name in files), 'Refusing existing output.'
        args.output.mkdir(parents=True, exist_ok=True)
        for name, payload in files.items():
            with (args.output / name).open('xb') as f:
                f.write(payload)
    print(json.dumps(dict(tables={str(s['sigma']): dict(L1=s['counts']['L1'], L2=s['counts']['L2'])
        for s in observations['tables']}, controls=observations['controls'],
        bounded_realization=observations['bounded_realization_summary']), sort_keys=True))
    print('CHECK OK' if args.check else f'CREATED {len(files)} files')


if __name__ == '__main__':
    main()
