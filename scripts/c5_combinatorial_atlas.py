#!/usr/bin/env python3
"""Replay the finite C5 relation atlas without changing its source evidence.

Use the pinned requirements.txt environment. --write creates only the new
atlas directory; --check recomputes and compares every derived file bytewise.
No graph catalogue search, hypothetical exclusion, or change to Sigma keys.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from hashlib import sha256
from importlib.metadata import version
from io import StringIO
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import c5_cell_enumerator as enumerator
import c5_kempe_screen as screen
from c5_combinatorial_atlas_views import render

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_combinatorial_atlas'
SOURCE_BASE = 'acd2b1beea6c909edade565a00eeeeac05d2b3a7'
CATALOGUE = 'artifacts/c5_cells/cells.json'
SCREEN = 'artifacts/c5_cells/kempe_screen.json'
INPUTS = (CATALOGUE, SCREEN, 'scripts/c5_cell_enumerator.py',
          'scripts/c5_kempe_screen.py', 'scripts/boundary_relations.py',
          'requirements.txt')
SOURCES = INPUTS + ('scripts/c5_combinatorial_atlas.py',
                    'scripts/c5_combinatorial_atlas_views.py')
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
CHORDS = tuple(pair for pair in combinations(range(5), 2)
               if (pair[1] - pair[0]) not in (1, 4))
DOCS = ['docs/c5_cell_enumerator.md', 'docs/c5_kempe_screen.md',
        'docs/c5_boundary_relations.md', 'docs/c5_combinatorial_atlas.md']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def digest(path):
    return sha256((ROOT / path).read_bytes()).hexdigest()


def encoded(data, compact=False):
    return json.dumps(data, ensure_ascii=False, sort_keys=True,
                      indent=None if compact else 1,
                      separators=(',', ':') if compact else None) + '\n'


def act(mask, permutation):
    return sum(1 << permutation[j] for j in range(10) if mask >> j & 1)


def permutation_cycles(permutation):
    remaining = set(range(len(permutation)))
    cycles = []
    while remaining:
        start = min(remaining)
        cycle, vertex = [], start
        while vertex not in cycle:
            cycle.append(vertex)
            remaining.remove(vertex)
            vertex = permutation[vertex]
        require(vertex == start, 'invalid permutation cycle')
        cycles.append(cycle)
    return cycles


def replay_witness(mask, cell, patterns):
    """Exhaust all private assignments for each fixed canonical boundary word.

    This backtracker uses actual edges, independently of the enumerator's
    compatibility-bitset evaluator. Global S4 expansion covers all 240 words.
    It saves one literal full lift per accepted word, and exact fibre counts.
    """
    import networkx as nx
    optional = tuple(tuple(e) for e in cell['edges'])
    edges = sorted({tuple(sorted(e)) for e in CYCLE + optional})
    vertices = sorted(set(range(5)) | {v for edge in edges for v in edge})
    private = [v for v in vertices if v >= 5]
    require(len(private) == cell['k_eff'] <= 5, f'witness size {mask}')
    require(all(u != v for u, v in edges), f'witness loop {mask}')
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)
    apex = max(vertices) + 1
    disk = graph.copy()
    disk.add_edges_from((apex, i) for i in range(5))
    planar, embedding = nx.check_planarity(disk)
    require(planar, f'non-disk witness {mask}')
    embedding.check_structure()
    adjacency = {v: set(graph[v]) for v in vertices}
    order = sorted(private, key=lambda v: (-len(adjacency[v]), v))
    fibres, lifts = [], {}
    for bit, boundary in enumerate(patterns):
        assignment = dict(enumerate(boundary))
        first = []

        def visit(index):
            if index == len(order):
                if not first:
                    first.append([assignment[v] for v in vertices])
                return 1
            v = order[index]
            forbidden = {assignment[w] for w in adjacency[v] if w in assignment}
            count = 0
            for colour in range(4):
                if colour not in forbidden:
                    assignment[v] = colour
                    count += visit(index + 1)
                    del assignment[v]
            return count

        count = (visit(0) if all(boundary[u] != boundary[v]
                 for u, v in edges if v < 5) else 0)
        fibres.append(count)
        if first:
            lifts[str(bit)] = first[0]
    actual = sum(1 << bit for bit, count in enumerate(fibres) if count)
    require(actual == mask, f'full witness relation differs {mask}: {actual}')
    interior = graph.subgraph(private)
    interior_pairs = list(combinations(range(len(private)), 2))
    skeleton_code = min((sum(1 << bit for bit, (i, j) in enumerate(interior_pairs)
                        if graph.has_edge(perm[i], perm[j]))
                        for perm in permutations(private)), default=0)
    return {
        'mask': mask, 'inner_vertices': len(private),
        'source': f'{CATALOGUE}#/cells/{mask}',
        'vertices': vertices, 'edges': [list(e) for e in edges],
        'chords': [list(e) for e in edges if e[1] < 5 and e in CHORDS],
        'attachments': [list(e) for e in edges if e[0] < 5 <= e[1]],
        'interior_edges': [list(e) for e in edges if e[0] >= 5],
        'interior_components': sorted(sorted(c) for c in nx.connected_components(interior)),
        'interior_degree_sequence': sorted(graph.degree(v) for v in private),
        'interior_skeleton_key': f'{len(private)}:{skeleton_code}',
        'boundary_degree_sequence': [graph.degree(v) for v in range(5)],
        'attachment_sets': {str(v): sorted(adjacency[v] & set(range(5))) for v in private},
        'apex_planar': True, 'recomputed_mask': actual,
        'fibre_counts': fibres, 'full_lifts': lifts,
        'count_semantics': 'fixed boundary word; exhaustive private assignments; vertices indexes each lift',
    }


def projection_arity(mask, expanded, domain):
    relation = set().union(*(expanded[j] for j in range(10) if mask >> j & 1))
    for arity in range(1, 6):
        scopes = list(combinations(range(5), arity))
        views = [{tuple(row[i] for i in scope) for row in relation} for scope in scopes]
        if all(row in relation or any(tuple(row[i] for i in scope) not in view
               for scope, view in zip(scopes, views)) for row in domain):
            return arity
    raise ValueError('full projection reconstruction failed')


def build():
    initial_hashes = {path: digest(path) for path in SOURCES}
    catalogue = json.loads((ROOT / CATALOGUE).read_text())
    saved_screen = (ROOT / SCREEN).read_text()
    replayed_screen = screen.report()
    require(json.dumps(replayed_screen, indent=2) + '\n' == saved_screen,
            'original Kempe/exterior certificate differs on replay')
    domain = tuple(product(range(4), repeat=5))
    proper = {b for b in domain if all(b[i] != b[(i + 1) % 5] for i in range(5))}
    patterns = tuple(sorted({normalize(b) for b in proper}))
    require(len(proper) == 3**5 - 3 == 240, 'proper C5 count')
    require(len(patterns) == 10, 'S4 orbit count')
    require([list(b) for b in patterns] == catalogue['pattern_order']
            == [list(b) for b in replayed_screen['pattern_order']], 'labelled pattern order drift')
    colour_permutations = tuple(permutations(range(4)))
    expanded = [{tuple(p[c] for c in b) for p in colour_permutations} for b in patterns]
    require(all(len(rows) == 24 for rows in expanded), 'S4 action not free')
    require(set().union(*expanded) == proper and sum(map(len, expanded)) == len(proper),
            'S4 orbits fail disjoint complete coverage')
    index = {b: j for j, b in enumerate(patterns)}
    pattern_records = []
    for bit, b in enumerate(patterns):
        same = [[i, j] for i, j in combinations(range(5), 2) if b[i] == b[j]]
        pattern_records.append(dict(bit=bit, word=''.join(map(str, b)), colours=len(set(b)),
            singleton=next((i for i in range(5) if b.count(b[i]) == 1), None)
                      if len(set(b)) == 3 else None,
            equal_pairs=same, equal_pair_distances=[min(j-i, 5-(j-i)) for i,j in same],
            colour_multiplicities=sorted(Counter(b).values(), reverse=True),
            labelled_colourings=len(expanded[bit])))
    group = []
    for reflection in (0, 1):
        for rotation in range(5):
            source_indices = [((-1 if reflection else 1) * (i + rotation)) % 5
                              for i in range(5)]
            permutation = [index[normalize(tuple(b[i] for i in source_indices))]
                           for b in patterns]
            name = f'r{rotation}s{reflection}'
            require(tuple(permutation) == enumerator.D5[name], f'production D5 map {name}')
            screen_offset = (-rotation if reflection else rotation) % 5
            require(all(act(1 << bit, permutation)
                    == screen.act(1 << bit, screen_offset, bool(reflection)) for bit in range(10)),
                    f'screen D5 convention {name}')
            group.append(dict(name=name, rotation=rotation, reflection=bool(reflection),
                source_indices=source_indices, bit_permutation=permutation,
                screen_rotation_offset=screen_offset,
                cycles=permutation_cycles(permutation)))
    group_maps = {tuple(g['bit_permutation']) for g in group}
    require(len(group_maps) == 10, 'D5 action must be faithful')
    require(all(tuple(p[q[j]] for j in range(10)) in group_maps
            for p in group_maps for q in group_maps), 'D5 composition closure')
    by_name = {g['name']: g['bit_permutation'] for g in group}
    def apply_name(mask, name):
        return act(mask, by_name[name])
    require(all(apply_name(apply_name(mask, 'r0s1'), 'r0s1') == mask
                for mask in range(1024)), 'reflection square')
    require(all(apply_name(apply_name(apply_name(apply_name(apply_name(
                mask, 'r1s0'), 'r1s0'), 'r1s0'), 'r1s0'), 'r1s0') == mask
                for mask in range(1024)), 'rotation fifth power')
    require(all(apply_name(apply_name(apply_name(mask, 'r0s1'), 'r1s0'), 'r0s1')
                == apply_name(mask, 'r4s0') for mask in range(1024)), 'srs=r^-1')
    orbit_of = {mask: sorted({act(mask, g['bit_permutation']) for g in group})
                for mask in range(1024)}
    canonical = {mask: min(orbit) for mask, orbit in orbit_of.items()}
    require(all(canonical[canonical[mask]] == canonical[mask] for mask in range(1024)),
            'canonicalization idempotence')
    require(all(orbit_of[m] == orbit_of[member] for m in range(1024) for member in orbit_of[m]),
            'overlapping or incomplete D5 orbits')
    reps = sorted({canonical[m] for m in range(1, 1024)})
    require(len(reps) == 135, 'nonempty D5 orbit count')
    require(sum(len(orbit_of[m]) for m in reps) == 1023, 'orbit coverage')
    histogram = dict(sorted(Counter(len(orbit_of[m]) for m in reps).items()))
    require(histogram == {1: 3, 5: 60, 10: 72}, 'orbit size histogram')
    require(len({canonical[1 << bit] for bit in range(10)}) == 2,
            'individual boundary-pattern S4 times D5 quotient')
    burnside = []
    for g in group:
        fixed = sum(act(m, g['bit_permutation']) == m for m in range(1, 1024))
        formula = 2**len(g['cycles']) - 1
        require(fixed == formula, f'Burnside cycle formula {g["name"]}')
        burnside.append(dict(element=g['name'], cycles=g['cycles'], fixed_nonempty=fixed,
                             cycle_formula_nonempty=formula))
    require(sum(r['fixed_nonempty'] for r in burnside) == 10 * len(reps), 'Burnside sum')
    known = set(map(int, catalogue['cells']))
    witnesses = {mask: replay_witness(mask, catalogue['cells'][str(mask)], patterns)
                 for mask in sorted(known)}
    kempe = {m for m in range(1, 1024) if screen.failure(m, replayed_screen['obligations']) is None}
    failures = {m: screen.failure(m, replayed_screen['obligations']) for m in range(1, 1024)}
    exterior_bad = {m: next((t for t in sorted(known) if not m & t), None) for m in range(1, 1024)}
    combined = {m for m in kempe if exterior_bad[m] is None}
    require(kempe == set(replayed_screen['kempe_masks']), 'Kempe membership')
    require({str(m): failures[m] for m in range(1, 1024) if m not in kempe}
            == replayed_screen['kempe_rejections'], 'all Kempe rejection certificates')
    require({str(m): exterior_bad[m] for m in sorted(kempe) if exterior_bad[m] is not None}
            == replayed_screen['exterior_rejections'], 'exterior rejection witnesses')
    require(known <= combined, 'witness rejected by necessary conditions')
    require(sorted(combined - known) == replayed_screen['remaining_extra'], 'open labelled masks')
    require([orbit_of[r] for r in sorted({canonical[m] for m in combined-known})]
            == replayed_screen['remaining_extra_orbits'], 'open orbits')
    status = {m: ('kempe_rejected' if m not in kempe else 'exterior_rejected'
                 if m not in combined else 'realized' if m in known else 'open')
              for m in range(1, 1024)}
    require(all(len({status[m] for m in orbit_of[r]}) == 1 for r in reps), 'status D5 invariance')
    require(all(len({exterior_bad[m] is None for m in orbit_of[r]}) == 1 for r in reps),
            'exterior D5 invariance')
    # Literal two-side intersections. Every record keeps both raw side keys and
    # an explicit alignment in the production enumerator convention.
    separating, separating_cost = {}, {}
    covariant_cases = 0
    for left in sorted(known):
        for g in group:
            for right in sorted(known):
                aligned = act(right, g['bit_permutation'])
                meet = left & aligned
                cost = (witnesses[left]['inner_vertices'] + witnesses[right]['inner_vertices'],
                        left, g['name'], right)
                if meet not in separating_cost or cost < separating_cost[meet]:
                    separating_cost[meet] = cost
                    separating[meet] = dict(left=left, right=right, alignment=g['name'],
                                             inner_vertices=cost[0])
    require(set(separating) == set(range(1, 1024)), 'separating intersections coverage')
    require(len(separating) == catalogue['separating_c5']['distinct_meets']
            and int(0 in separating) == catalogue['separating_c5']['empty_meets'],
            'separating source summary')
    # Check algebra covariance over ALL pairs of raw keys, including empties;
    # this preserves shared alignment, rather than quotienting each operand.
    for g in group:
        mapping = [act(m, g['bit_permutation']) for m in range(1024)]
        for a in range(1024):
            for b in range(1024):
                require(mapping[a & b] == mapping[a] & mapping[b], 'intersection covariance')
                require(mapping[a | b] == mapping[a] | mapping[b], 'union covariance')
                covariant_cases += 1
    require(95 in known and 123 in known and canonical[95] == canonical[123]
            and canonical[95 & 123] != canonical[canonical[95] & canonical[123]],
            'alignment-loss negative control')
    classes = []
    arities = {}
    for representative in reps:
        members = orbit_of[representative]
        allowed = [j for j in range(10) if representative >> j & 1]
        forbidden = [j for j in range(10) if not representative >> j & 1]
        rows = [patterns[j] for j in allowed]
        support = sorted(pattern_records[j]['singleton'] for j in allowed
                         if pattern_records[j]['colours'] == 3)
        forced_equal = [list(pair) for pair in CHORDS if all(b[pair[0]] == b[pair[1]] for b in rows)]
        forced_unequal = [list(pair) for pair in CHORDS if all(b[pair[0]] != b[pair[1]] for b in rows)]
        stabilizer = [g['name'] for g in group if act(representative, g['bit_permutation']) == representative]
        require(len(members) * len(stabilizer) == 10, 'orbit-stabilizer theorem')
        arity = projection_arity(representative, expanded, domain)
        arities[representative] = arity
        distance = min((representative ^ m).bit_count() for m in known)
        attached = [witnesses[m] for m in members if m in known]
        evidence = DOCS.copy()
        if status[representative] == 'kempe_rejected':
            evidence.append(f'{SCREEN}#/kempe_rejections/{representative}')
        elif status[representative] == 'exterior_rejected':
            evidence.extend([f'{SCREEN}#/exterior_rejections/{representative}',
                             f'{CATALOGUE}#/cells/{exterior_bad[representative]}'])
        elif status[representative] == 'open':
            evidence.extend([f'{SCREEN}#/remaining_extra_orbits',
                'docs/c5_independent_support_capacity.md', 'docs/c5_k13_collar.md'])
        else:
            evidence.extend(w['source'] for w in attached)
        classes.append(dict(canonical=representative, canonical_bits=f'{representative:010b}',
            orbit_members=members, orbit_size=len(members), stabilizer=stabilizer,
            member_transformations={str(m): [g['name'] for g in group
                if act(representative, g['bit_permutation']) == m] for m in members},
            allowed_bits=allowed, forbidden_bits=forbidden,
            three_count=len(support), four_count=len(allowed)-len(support),
            status=status[representative], screens=dict(kempe=representative in kempe,
                                                       exterior=exterior_bad[representative] is None),
            kempe_supporting_options=({str(j): [[option for option in options
                 if representative & option == option] for options in replayed_screen['obligations'][j]]
                 for j in allowed} if representative in kempe else None),
            minimum_known_inner_vertices=min((w['inner_vertices'] for w in attached), default=None),
            witnesses=attached, evidence=evidence,
            features=dict(singleton_support=support,
                singleton_adjacent_edges=[list(e) for e in CYCLE if e[0] in support and e[1] in support],
                singleton_pair_distances=sorted(min(j-i,5-(j-i)) for i,j in combinations(support,2)),
                all_four=all(j in allowed for j in range(10) if len(set(patterns[j])) == 4),
                forced_equal_pairs=forced_equal, forced_unequal_pairs=forced_unequal,
                chord_compatible_pairs=forced_unequal,
                minimum_projection_arity=arity,
                aligned_immediate_subsets=sorted(representative ^ (1<<j) for j in allowed
                                                 if representative ^ (1<<j)),
                aligned_immediate_supersets=sorted(representative | (1<<j) for j in forbidden),
                known_subsets=sorted(m for m in known if m & representative == m),
                known_supersets=sorted(m for m in known if m & representative == representative),
                nearest_known_masks=dict(distance=distance, masks=sorted(m for m in known
                    if (representative ^ m).bit_count() == distance)))))
    require(Counter(arities[canonical[m]] for m in known) == {2:11,4:101,5:20}, 'known arity classification')
    class_by_rep = {c['canonical']: c for c in classes}
    labelled = [dict(mask=m, canonical=canonical[m],
        to_canonical=[g['name'] for g in group if act(m,g['bit_permutation']) == canonical[m]],
        status=status[m], kempe_failure=failures[m], exterior_disjoint_witness=exterior_bad[m],
        witness_source=witnesses[m]['source'] if m in known else None,
        separating_witness=separating[m]) for m in range(1,1024)]
    require({w['mask'] for c in classes for w in c['witnesses']} == known, '132 evidence records coverage')
    counts = dict(proper_colourings=len(proper), s4_orbits=len(patterns), all_masks=1<<len(patterns),
        individual_pattern_s4_d5_orbits=len({canonical[1 << bit] for bit in range(10)}),
        nonempty_masks=len(labelled), d5_orbits=len(classes), kempe_masks=len(kempe),
        kempe_orbits=len({canonical[m] for m in kempe}), screened_masks=len(combined),
        screened_orbits=len({canonical[m] for m in combined}), known_masks=len(known),
        known_orbits=len({canonical[m] for m in known}), open_masks=len(combined-known),
        open_orbits=len({canonical[m] for m in combined-known}),
        kempe_rejected_masks=1023-len(kempe), exterior_rejected_masks=len(kempe-combined),
        separating_masks=len(separating))
    require([counts[k] for k in ('proper_colourings','s4_orbits','all_masks','nonempty_masks',
                'd5_orbits','kempe_masks','screened_masks','known_masks','known_orbits','open_orbits')]
            == [240,10,1024,1023,135,153,142,132,24,2], 'requested independent count cross-check')
    for level in range(6):
        require(sum(w['inner_vertices'] <= level for w in witnesses.values())
                == catalogue['nested_by_k_eff'][str(level)], 'minimum stored witness distribution')
    atlas = dict(schema='c5-combinatorial-atlas-v1',
        semantics=dict(boundary='ordered b0,b1,b2,b3,b4; original Sigma keys retained',
            group='r(a)s(f) pulls input from (-1)^f*(i+a) mod5; production enumerator convention',
            canonical='minimum integer in D5 orbit; display index only',
            binary='MSB first for displayed 10-bit strings; bit j corresponds to pattern_order[j]',
            single_disk='known iff an original replayed disk witness is present; candidates are OPEN',
            separating='left & act(right,alignment); independent private interiors on opposite sides',
            exterior='uses disk gluing and 4CT; finite catalogue contexts only',
            features='descriptive relation data and selected witness fingerprints; no realization oracle'),
        summary=counts, orbit_size_histogram={str(k):v for k,v in histogram.items()},
        status_class_counts=dict(Counter(c['status'] for c in classes)),
        minimum_known_inner_histogram={str(k):v for k,v in sorted(Counter(
            w['inner_vertices'] for w in witnesses.values()).items())},
        patterns=pattern_records, group=group, burnside=burnside,
        kempe_obligations=replayed_screen['obligations'],
        complementary_splits=replayed_screen['complementary_splits'],
        classes=classes, labelled_masks=labelled,
        alignment_loss_control=dict(left=95,right=123,canonical_left=canonical[95],
            canonical_right=canonical[123],raw_meet=95&123,raw_meet_canonical=canonical[95&123],
            independently_quotiented_meet=canonical[95]&canonical[123]),
        open_comparison=[dict(canonical=r,features=class_by_rep[r]['features'])
                         for r in reps if status[r]=='open'],
        descriptive_controls=dict(nonadjacent_support_known=429,
            support_only_not_sufficient=[95,127],
            hypotheses='Adjacent-singleton assertion remains UNPROVED; no observational feature promoted to theorem'))
    shape_keys = sorted({w['interior_skeleton_key'] for w in witnesses.values()})
    atlas['witness_internal_shape_groups'] = [dict(interior_skeleton_key=key,
        labelled_masks=sorted(m for m,w in witnesses.items() if w['interior_skeleton_key']==key),
        classes=sorted({canonical[m] for m,w in witnesses.items() if w['interior_skeleton_key']==key}))
        for key in shape_keys]
    atlas['witness_shape_semantics'] = ('Interior graph isomorphism only, over all private relabellings; '
        'boundary attachments and chords remain in each original witness and are not implied by this key.')
    atlas['classes_with_multiple_witness_interior_shapes'] = [c['canonical'] for c in classes
        if len({w['interior_skeleton_key'] for w in c['witnesses']}) > 1]
    require({path:digest(path) for path in SOURCES} == initial_hashes, 'source evidence or generator mutated')
    manifest = dict(schema='c5-atlas-source-manifest-v1', source_base_commit=SOURCE_BASE,
        source_base_repository='https://github.com/raylei50653/math',
        source_base_note='Snapshot provenance; replay gates are file hashes, not current branch identity.',
        inputs={path:dict(sha256=initial_hashes[path],bytes=(ROOT/path).stat().st_size) for path in SOURCES},
        networkx_version=version('networkx'), dependency_pin='requirements.txt',
        reproduction=['python scripts/c5_combinatorial_atlas.py --write',
                      'python scripts/c5_combinatorial_atlas.py --check'],
        legacy_evidence_policy='read only; original cells.json and kempe_screen.json never regenerated')
    verification = dict(schema='c5-atlas-verification-v1', result='PASS', counts=counts,
        checks=dict(proper_and_s4_recomputed=True,s4_disjoint_coverage=True,
            nonempty_orbit_exact_coverage=True,burnside_formula_and_enumeration=True,
            rotation_and_reflection_closure=True,canonicalization_idempotent=True,
            orbit_stabilizer=True,production_and_screen_group_conventions=True,
            original_screen_byte_match=True,all_kempe_rejections_match=True,
            all_original_exterior_witnesses_match=True,full_witness_relations=True,
            witness_apex_planarity=True,witness_evidence_coverage=True,
            separating_all_nonempty=True,intersection_and_union_covariance=True,
            independent_canonicalization_alignment_loss_detected=True,
            source_evidence_unchanged=True),
        witness_checks=len(witnesses), algebra_pair_group_checks=covariant_cases,
        burnside_fixed_sum=sum(r['fixed_nonempty'] for r in burnside),
        source_sha256=initial_hashes,
        limits=['Finite classification; disk Kempe soundness is inherited paper topology.',
            'Exterior exclusion invokes 4CT; existential Kempe choices are not jointly certified lifts.',
            'Stored minimum witness sizes are not independently re-enumerated graph-minimum proofs.',
            'No new Lean theorem; no general source classification or K_infinity=K_le5 proof.',
            'All 1023 separating relations do not imply single-disk realizability.'])
    outputs = {'atlas.json':encoded(atlas,compact=True),
        'verification.json':encoded(verification), 'source_manifest.json':encoded(manifest)}
    outputs.update(render(atlas))
    csv_file = StringIO(newline='')
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['mask','canonical','orbit_size','status','to_canonical',
                     'witness_source','separating_left','separating_right','alignment'])
    for r in labelled:
        sep = r['separating_witness']
        writer.writerow([r['mask'],r['canonical'],len(orbit_of[r['mask']]),r['status'],
                         ';'.join(r['to_canonical']),r['witness_source'],
                         sep['left'],sep['right'],sep['alignment']])
    outputs['labelled_masks.csv'] = csv_file.getvalue()
    csv_file = StringIO(newline='')
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['canonical','orbit_members','orbit_size','stabilizer','three_count',
        'four_count','status','kempe','exterior','minimum_known_inner_vertices',
        'singleton_support','minimum_projection_arity','witness_sources'])
    for r in classes:
        writer.writerow([r['canonical'],';'.join(map(str,r['orbit_members'])),r['orbit_size'],
            ';'.join(r['stabilizer']),r['three_count'],r['four_count'],r['status'],
            r['screens']['kempe'],r['screens']['exterior'],r['minimum_known_inner_vertices'],
            ';'.join(map(str,r['features']['singleton_support'])),
            r['features']['minimum_projection_arity'],';'.join(w['source'] for w in r['witnesses'])])
    outputs['classes.csv'] = csv_file.getvalue()
    known_table = ['# 已知單側 disk D5 類（自動生成）', '',
        '由 `c5_combinatorial_atlas.py` 的同一份分類資料產生；k 只表示保存目錄的最小已知值。', '',
        '| canonical | orbit members | orbit size | 三色／四色 | 最小已知 k | 原證據 |',
        '|---:|---|---:|---|---:|---|']
    for c in classes:
        if c['status'] == 'realized':
            source = f'../c5_cells/cells.json#/cells/{c["canonical"]}'
            known_table.append(f'| {c["canonical"]} | {", ".join(map(str,c["orbit_members"]))} | '
                f'{c["orbit_size"]} | {c["three_count"]}／{c["four_count"]} | '
                f'{c["minimum_known_inner_vertices"]} | [原 witness]({source}) |')
    outputs['known_classes.md'] = '\n'.join(known_table) + '\n'
    require(all(len(value.encode()) < 1_000_000 for value in outputs.values()),
            'new file needs the repository large-artifact manifest workflow')
    return outputs, verification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    parser.add_argument('--output',type=Path,default=OUT)
    args = parser.parse_args()
    outputs, verification = build()
    if args.check:
        for name, content in sorted(outputs.items()):
            path = args.output/name
            require(path.exists() and path.read_bytes()==content.encode(),
                    f'generated file differs: {path}; inspect before --write')
    else:
        args.output.mkdir(parents=True,exist_ok=True)
        for name, content in sorted(outputs.items()):
            (args.output/name).write_bytes(content.encode())
    print(json.dumps(verification['counts'],sort_keys=True))
    print(f'PASS: {len(outputs)} derived files; 132 original witnesses; OPEN preserved')


if __name__ == '__main__':
    main()
