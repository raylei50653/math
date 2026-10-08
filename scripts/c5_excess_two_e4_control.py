#!/usr/bin/env python3
"""E4 read-only stored-record scan and nineteen fixed control attempts.

This is not a source-family enumeration or a Four Color Theorem oracle.
Generation exclusively creates a new certificate; --check is read-only.
Only literal assignments in the listed finite graphs are checked.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import networkx as nx
import c5_excess_two_e3_nonadjacent as helper

ROOT = Path(__file__).resolve().parents[1]
FRAME = helper.FRAME
B = helper.B
OUT = ROOT / 'artifacts/c5_excess_two_e4/control.json'
E1_REL = Path('artifacts/c5_excess_rejection_law/observations.json')
E1_SHA = '23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()

def edges(items):
    return {tuple(sorted(e)) for e in items}

def degree_record(vertices, graph_edges):
    ns = helper.neighbors(set(vertices), graph_edges)
    ds = {str(v): len(ns[v]) for v in sorted(set(vertices) - B)}
    roots = sorted(v for v in set(vertices) - B if len(ns[v]) > 4)
    eps = sum(d - 4 for d in ds.values())
    candidate = (eps == 2 and len(roots) == 2 and
        all(d >= 4 for d in ds.values()) and
        all(ds[str(r)] == 5 for r in roots) and tuple(roots) not in graph_edges)
    return dict(private_degrees=ds, epsilon=eps, roots=roots,
        roots_adjacent=len(roots) == 2 and tuple(roots) in graph_edges,
        requested_degree_and_nonadjacency=candidate)

def stored_record(pointer, rec, vertices, graph_edges):
    return dict(pointer=pointer, record_sha256=sha(canonical(rec)),
        vertices=sorted(vertices), nonframe_edges=[list(e) for e in sorted(graph_edges - FRAME)],
        **degree_record(vertices, graph_edges))

def disk_embedding(vertices, graph_edges):
    apex = max(vertices) + 1
    graph = nx.Graph()
    graph.add_nodes_from(sorted(vertices) + [apex])
    graph.add_edges_from(sorted(graph_edges) + [(b, apex) for b in sorted(B)])
    planar, embedding = nx.check_planarity(graph)
    if not planar:
        return None
    embedding.check_structure()
    rotations = {v: [w for w in embedding.neighbors_cw_order(v) if w != apex]
                 for v in sorted(vertices)}
    plane = nx.PlanarEmbedding()
    plane.set_data(rotations)
    plane.check_structure()
    outer = None
    for u, v in sorted(FRAME):
        for a, b in ((u, v), (v, u)):
            face = plane.traverse_face(a, b)
            if len(face) == 5 and set(face) == B:
                outer = face
                break
        if outer is not None:
            break
    assert outer is not None
    return dict(apex=apex, apex_rotation=list(embedding.neighbors_cw_order(apex)),
        disk_rotation={str(v): rotations[v] for v in sorted(vertices)}, outer_face=outer)

def attempt(name, vertices, graph_edges, rows, provenance):
    vertices = set(vertices)
    graph_edges = set(graph_edges)
    order = sorted(vertices)
    degree = degree_record(vertices, graph_edges)
    assert degree['requested_degree_and_nonadjacency']
    assert {e for e in graph_edges if set(e) <= B} == FRAME
    actual, choices = helper.sigma_and_witnesses(vertices, graph_edges, rows)
    complete_rows = [dict(row_index=i, boundary=row, accepted=bool(fs),
        complete_coloring_order=order,
        complete_literal_colorings=[[f[v] for v in order] for f in fs])
        for i, (row, fs) in enumerate(zip(rows, choices))]
    deletion_records = []
    noncritical = []
    for e in sorted(graph_edges - FRAME):
        after, child = helper.sigma_and_witnesses(vertices, graph_edges - {e}, rows)
        gained = [i for i in range(10) if after >> i & 1 and not actual >> i & 1]
        witnesses = []
        for i in gained:
            f = child[i][0]
            assert f[e[0]] == f[e[1]]
            assert all(f[u] != f[v] for u, v in graph_edges - {e})
            witnesses.append(dict(row_index=i, complete_coloring_order=order,
                coloring=[f[v] for v in order]))
        if not gained:
            noncritical.append(list(e))
        deletion_records.append(dict(deleted_edge=list(e), child_sigma=after,
            all_new_row_indices=gained, critical=bool(gained), gained_row_witnesses=witnesses))
    disk = disk_embedding(order, graph_edges)
    accepted_t4 = all(choices[i] for i in helper.T4)
    failures = []
    if disk is None:
        failures.append('No induced-C5 disk embedding: the exterior frame cone is nonplanar.')
    if not accepted_t4:
        failures.append('T4 is not fully accepted.')
    if noncritical:
        failures.append('The named noncritical nonframe edges prevent Sigma-edge-minimality.')
    successful = disk is not None and accepted_t4 and not noncritical
    assert not successful, 'Save the first actual control and stop further attempts.'
    ns = helper.neighbors(vertices, graph_edges)
    pieces = []
    for j, comp in enumerate(helper.components(vertices - B - set(degree['roots']), graph_edges)):
        pv = set(comp)
        pieces.append(dict(id=f'P{j}', vertices=comp,
            root_contacts={str(r): sorted(ns[r] & pv) for r in degree['roots']},
            actual_support=sorted(set().union(*(ns[v] & B for v in pv))),
            boundary_attachments={str(v): sorted(ns[v] & B) for v in comp},
            original_internal_edges=[list(e) for e in sorted(graph_edges) if set(e) <= pv]))
    return dict(name=name, provenance=provenance, vertices=order,
        all_edges=[list(e) for e in sorted(graph_edges)], frame_edges=[list(e) for e in sorted(FRAME)],
        **degree, source_sigma=actual, sigma_indices=[i for i in range(10) if choices[i]],
        all_T4_accepted=accepted_t4, Sigma_edge_minimal=not noncritical,
        noncritical_edges=noncritical, complete_rows=complete_rows,
        original_components=pieces, edge_deletions=deletion_records,
        disk_embedding=disk, is_requested_positive_control=successful,
        failures=failures)

def build(source):
    assert nx.__version__ == '3.5', 'Use the shared .venv for deterministic disk rotations.'
    source_bytes = source.read_bytes()
    assert sha(source_bytes) == E1_SHA
    e1 = json.loads(source_bytes)
    cell_path = ROOT / 'artifacts/c5_cells/cells.json'
    cell_bytes = cell_path.read_bytes()
    cells = json.loads(cell_bytes)
    rows = cells['pattern_order']
    assert rows == e1['pattern_order']
    minima = []
    scratch = []
    cell_records = []
    for i, part in enumerate(e1['exhaustive']):
        for sig, rec in sorted(part['minima_by_sigma'].items(), key=lambda x: int(x[0])):
            minima.append(stored_record(f'/exhaustive/{i}/minima_by_sigma/{sig}', rec,
                rec['vertices'], edges(rec['all_edges'])))
    for i, rec in enumerate(e1['scratch']):
        witness = rec['witness']
        scratch.append(stored_record(f'/scratch/{i}/witness', witness,
            witness['vertices'], edges(witness['all_edges'])))
    for sig, rec in sorted(cells['cells'].items(), key=lambda x: int(x[0])):
        cell_records.append(stored_record(f'/cells/{sig}', rec,
            range(5 + rec['k_eff']), FRAME | edges(rec['edges'])))
    assert (len(minima), len(scratch), len(cell_records)) == (50, 20, 132)
    assert not any(rec['requested_degree_and_nonadjacency'] for rec in minima + scratch + cell_records)
    attempts = []
    base951 = FRAME | edges(cells['cells']['951']['edges'])
    split951 = {e for e in base951 if 5 not in e} | edges([
        (5,3),(5,4),(5,6),(5,9),(5,11),
        (10,3),(10,4),(10,7),(10,8),(10,11),(11,3),(11,4)])
    attempts.append(attempt('951-degree6-hub-split', list(range(10)) + [10,11],
        split951, rows, dict(source='artifacts/c5_cells/cells.json', pointer='/cells/951',
        operation='Split the degree6 hub into nonadjacent degree5 roots and a degree4 connector.')))
    base935 = FRAME | edges(cells['cells']['935']['edges'])
    for p, q in combinations(range(5), 2):
        graph_edges = base935 - {(6,7)} | edges([(6,8),(7,8),(8,p),(8,q)])
        attempts.append(attempt(f'935-subdivide-root-edge-spokes-{p}{q}', range(9),
            graph_edges, rows, dict(source='artifacts/c5_cells/cells.json', pointer='/cells/935',
            operation='Subdivide the root edge and give the inserted degree4 vertex the stated two frame attachments.')))
    for b in (3,4):
        graph_edges = base935 - {(6,7),(b,5)} | edges([(6,8),(7,8),(8,1),(8,5)])
        attempts.append(attempt(f'935-root-edge-contact-insertion-remove-{b}5', range(9),
            graph_edges, rows, dict(source='artifacts/c5_cells/cells.json', pointer='/cells/935',
            operation='Insert degree4 vertex on the root edge; attach it to old mixed contact5 and boundary1; remove the stated old contact spoke.')))
    core = FRAME | edges([(5,7),(5,8),(6,7),(6,8),(7,8),
        (5,0),(5,1),(5,2),(6,2),(6,3),(6,4)])
    for x, y in ((2,0),(2,4),(2,1),(1,4),(3,0)):
        attempts.append(attempt(f'fixed-K4-minus-root-edge-supports-{x}{y}', range(9),
            core | edges([(7,x),(8,y)]), rows,
            dict(source='E4 hand construction', operation='Keep the original K4 minus nonadjacent root edge and root spokes012/234; use the named contact supports.')))
    final_edges = FRAME | edges([(5,7),(5,8),(7,8),(6,9),(6,10),(9,10),
        (5,11),(6,11),(5,0),(5,2),(6,2),(6,4),
        (7,0),(7,1),(8,1),(8,2),(9,2),(9,3),(10,3),(10,4),(11,0),(11,4)])
    attempts.append(attempt('two-unary-triangles-separating-singleton', range(12),
        final_edges, rows, dict(source='E4 hand construction',
        operation='Two original unary triangles, one separating mixed singleton supported on04, roots spokes02/24.')))
    assert len(attempts) == 19
    return dict(schema_version=1, task='E4 nonadjacent degree5 positive-control search boundary',
        base_commit='2ac279b', no_four_color_theorem_oracle=True,
        source_inputs=[dict(path=str(E1_REL), sha256=E1_SHA,
            scope='Only the stored 50 minima representatives and 20 scratch witnesses; no qualifying graph stream was searched.'),
            dict(path='artifacts/c5_cells/cells.json', sha256=sha(cell_bytes),
            scope='132 stored representatives; no source enumeration.'),
            dict(path='scripts/c5_excess_two_e4_control.py', sha256=sha(Path(__file__).read_bytes())),
            dict(path='scripts/c5_excess_two_e3_nonadjacent.py',
                 sha256=sha((ROOT / 'scripts/c5_excess_two_e3_nonadjacent.py').read_bytes()))],
        row_order=rows, T4_row_indices=sorted(helper.T4),
        stored_catalogue_audit=dict(E1_minima=minima, E1_scratch=scratch, tracked_cells=cell_records),
        fixed_attempts=attempts, successful_controls=[], requested_control_found=False,
        status='No requested positive control found in the stated stored records and nineteen fixed local attempts.',
        missing_control='Every E4 intermediate lemma that does not use the selected triple lacks validation on a Sigma-edge-minimal epsilon2 nonadjacent degree5 control.',
        evidence_boundary='This finite failure is neither a theorem excluding such controls nor a search of all k<=5 graphs.',
        abandoned_path_spoke_construction=dict(status='Rejected by the planar disk edge bound, before graph search.',
            proof='For H a k-vertex tree and epsilon2, private degree sum4k+2 gives B attachments2k+4; with k-1 H edges and5 frame edges, total3k+8 exceeds3(k+5)-3-5=3k+7. This applies to every induced-C5 disk with connected tree H, independently of row identities.'))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--e1-source', type=Path)
    args = parser.parse_args()
    source = args.e1_source
    if source is None:
        own = ROOT / E1_REL
        shared = ROOT.parent / 'math' / E1_REL
        source = own if own.is_file() else shared
    result = build(source)
    encoded = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert args.output.read_bytes() == encoded
        print('CHECK OK: 202 stored representatives and nineteen fixed attempts; no requested nonadjacent control found.')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as stream:
            stream.write(encoded)
        print(f'WROTE {args.output}: {len(encoded)} bytes; SHA256 {sha(encoded)}')

if __name__ == '__main__':
    main()
