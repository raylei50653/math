#!/usr/bin/env python3
"""Replay saved single-component moves and audit mixed-pair surgery interfaces."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx
from boundary_relations import normalize
from c5_sector_cross_row import relabel
from c5_sector_forced_connectivity import PAIRS, observed_partition

ROOT = Path(__file__).resolve().parents[1]
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
SOURCE = ROOT / 'artifacts/c5_sector_positive_control/observations.json'
OUT = ROOT / 'artifacts/c5_sector_mixed_transition/observations.json'


def frozen(x):
    return tuple(map(frozen, x)) if isinstance(x, (list, tuple)) else x


def digest(x):
    return sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def components(g):
    return sorted(sorted(c) for c in nx.connected_components(g))


def partition(blocks):
    return sorted(sorted(v for v in b if v < 5) for b in blocks if any(v < 5 for v in b))


def surgery(g, c, selected, a, b, d, raw):
    """Build quotient from OLD coloring only; compare to independent NEW induced graph."""
    retained = sorted(v for v in g if c[v] == d or (c[v] == a and v not in selected))
    deleted = sorted(v for v in selected if c[v] == a)
    inserted = sorted(v for v in selected if c[v] == b)
    blocks = components(g.subgraph(retained))
    owner = {v: i for i, block in enumerate(blocks) for v in block}
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(blocks) + len(inserted)))
    stars = []
    for i, v in enumerate(inserted, len(blocks)):
        owner[v] = i
        neighbors = sorted(w for w in g[v] if c[w] == d)
        stars.append(dict(vertex=v, neighbors=neighbors,
                          retained_blocks=sorted({owner[w] for w in neighbors})))
        quotient.add_edges_from((i, owner[w]) for w in neighbors)
    qowner = {v: i for i, block in enumerate(components(quotient)) for v in block}
    predicted = {}
    for v in retained + inserted:
        predicted.setdefault(qowner[owner[v]], []).append(v)
    predicted = sorted(sorted(block) for block in predicted.values())
    actual_graph = g.subgraph(v for v in g if raw[v] in (a, d))
    actual = components(actual_graph)
    assert predicted == actual
    rebuilt_edges = {tuple(sorted(e)) for e in g.subgraph(retained).edges()}
    rebuilt_edges.update(tuple(sorted((s['vertex'], w))) for s in stars for w in s['neighbors'])
    assert rebuilt_edges == {tuple(sorted(e)) for e in actual_graph.edges()}
    # Both splitting and merging must be computed, including components missing the frame.
    return dict(mixed_pair=[a, d], deleted=deleted, retained_blocks=blocks,
                inserted_stars=stars, quotient_edges=sorted(sorted(e) for e in quotient.edges()),
                before_components=components(g.subgraph(v for v in g if c[v] in (a, d))),
                after_components=actual, after_frame_partition=partition(actual))


def build():
    saved = json.loads(CROSS.read_text())
    # Attest that the upstream certificate still names the checked source/code versions.
    for path, expected in saved['input_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    records = {r['source_index']: r for r in json.loads(SOURCE.read_text())['proper_hits']}
    abstract = saved['abstract']
    states = abstract['states']
    ids = {(tuple(s['row']), frozen(s['partitions'])): i for i, s in enumerate(states)}
    alive = {w['state']: w for w in abstract['closed_successors']}
    buckets, collision, audits = {}, None, []
    totals = Counter()
    for control in saved['controls']:
        source_index = control['source_index']
        g = nx.Graph(records[source_index]['sector_edges'])
        g.remove_edges_from([(0, 1), (0, 4)])
        vertices = control['vertices']
        assert sorted(g) == vertices
        profiles = []
        for coloring in control['colorings']:
            c = dict(zip(vertices, coloring, strict=True))
            assert all(c[u] != c[v] for u, v in g.edges())
            profiles.append([observed_partition(g, c, p) for p in PAIRS])
        traces, counts = [], Counter()
        for ci, coloring in enumerate(control['colorings']):
            c = dict(zip(vertices, coloring, strict=True))
            state = ids.get((tuple(coloring[:5]), frozen(profiles[ci])))
            expected_moves = {(p, tuple(block)) for p in PAIRS
                              for block in components(g.subgraph(v for v in g if c[v] in p))}
            actual_moves = {(tuple(e['pair']), tuple(e['component'])) for e in control['moves'][ci]}
            assert actual_moves == expected_moves
            assert len(actual_moves) == len(control['moves'][ci])
            for ei, edge in enumerate(control['moves'][ci]):
                pair = tuple(edge['pair'])
                selected = set(edge['component'])
                a, b = pair
                raw = {v: (b if c[v] == a else a) if v in selected else c[v] for v in g}
                target = control['colorings'][edge['target']]
                assert normalize(tuple(raw[v] for v in vertices)) == tuple(target)
                assert all(raw[u] != raw[v] for u, v in g.edges())
                complement = tuple(d for d in range(4) if d not in pair)
                for unchanged in (pair, complement):
                    assert observed_partition(g, c, unchanged) == observed_partition(g, raw, unchanged)
                interfaces = [surgery(g, c, selected, x, y, d, raw)
                              for x, y in (pair, pair[::-1]) for d in range(4) if d not in pair]
                target_row, mapping = relabel(tuple(raw[v] for v in range(5)))
                assert target_row == tuple(target[:5])
                # Full-color normalization can use internal occurrences for absent frame colors.
                # Here compare raw partitions with the frame-based total permutation directly.
                normalized_profile = [None] * 6
                for p in PAIRS:
                    k = PAIRS.index(tuple(sorted(mapping[v] for v in p)))
                    normalized_profile[k] = observed_partition(g, raw, p)
                counts['moves'] += 1
                counts['mixed_pair_checks'] += len(interfaces)
                counts['interior_only_moves'] += not bool(selected & set(range(5)))
                traces.append([ci, ei, interfaces])
                block = tuple(sorted(selected & set(range(5))))
                if state in alive and block:
                    key = (source_index, state, pair, block)
                    example = dict(source_index=source_index, coloring_id=ci, move_id=ei,
                                   source_state=state, source_coloring=coloring, move=edge,
                                   raw_target=[raw[v] for v in vertices],
                                   frame_color_mapping=mapping,
                                   normalized_target_profile=normalized_profile,
                                   interfaces=interfaces)
                    previous = buckets.get(key)
                    if (collision is None and previous is not None
                            and previous['move']['component'] == edge['component']
                            and previous['normalized_target_profile'] != normalized_profile):
                        collision = [previous, example]
                    buckets.setdefault(key, example)
        audits.append(dict(source_index=source_index, colorings=len(control['colorings']),
                           **counts, full_recomputed_trace_sha256=digest(traces)))
        totals.update(counts)
    assert collision is not None
    left, right = collision
    state = left['source_state']
    pair = tuple(left['move']['pair'])
    block = sorted(v for v in left['move']['component'] if v < 5)
    # Locate the exact already-saved abstract successor for this SINGLE maximal block.
    action_index = 0
    chosen = None
    for j, p in enumerate(PAIRS):
        for bits in product((0, 1), repeat=len(states[state]['partitions'][j])):
            selected_blocks = [bl for bl, bit in zip(states[state]['partitions'][j], bits) if bit]
            if p == pair and selected_blocks == [block]:
                chosen = action_index
            action_index += 1
    assert chosen is not None
    successor = alive[state]['successors'][chosen]
    assert state == 397 and chosen == 2 and successor == 330
    assert [left['coloring_id'], right['coloring_id']] == [19, 24]
    assert left['source_index'] == right['source_index'] == 41
    assert left['move']['component'] == right['move']['component'] == [0, 1, 2, 9]
    collision_vertices = next(c['vertices'] for c in saved['controls']
                              if c['source_index'] == left['source_index'])
    checks = []
    for example in collision:
        for interface in example['interfaces']:
            raw_pair = interface['mixed_pair']
            mapping = example['frame_color_mapping']
            target_pair = tuple(sorted(mapping[c] for c in raw_pair))
            wanted = states[successor]['partitions'][PAIRS.index(target_pair)]
            observed = interface['after_frame_partition']
            checks.append(dict(coloring_id=example['coloring_id'], raw_pair=raw_pair,
                               normalized_pair=target_pair, successor_partition=wanted,
                               actual_partition=observed, compatible=observed == wanted))
    assert any(not c['compatible'] for c in checks)
    # The collision differs on a mixed pair, not merely on unobserved internal vertices.
    assert any(x['after_frame_partition'] != y['after_frame_partition']
               for x, y in zip(left['interfaces'], right['interfaces'], strict=True))
    inputs = [CROSS, SOURCE, Path(__file__).resolve(), ROOT / 'Math/KempeSurgery.lean']
    inputs += [ROOT / p for p in saved['input_sha256'] if p.startswith('scripts/')]
    return dict(schema=1, baseline='e097be67487bd3d455733e4fab1a1ab2744e557c',
                scope='General graph single maximal-component mixed-pair surgery; fixed saved corpus only; no new graph, no history state, no disk test on nonplanar controls.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in sorted(set(inputs))},
                lemma=dict(preconditions=['proper four-coloring', 'one maximal a/b component S',
                                          'a,b,d distinct'],
                           interface=['components of G[(a outside S) union d]',
                                      'each b-in-S vertex and its incidence to retained components',
                                      'frame vertex ownership'],
                           conclusion='New a/d connectivity equals retained-component quotient wired by inserted b-in-S stars; all four mixed pairs use the same coloring and S.'),
                control_audits=audits,
                selected_abstract_move=dict(state=state, source=states[state], action_index=chosen,
                                            pair=pair, block=block, successor=successor,
                                            successor_profile=states[successor]),
                collision=dict(vertices=collision_vertices,
                               sector_edges=records[left['source_index']]['sector_edges'],
                               examples=collision, saved_successor_checks=checks),
                closure_effect=dict(status='not filtered: profile does not determine the surgery interface',
                                    conditional_failures=sum(not c['compatible'] for c in checks),
                                    globally_excluded_successors=[], profile_deletions=0,
                                    inherited_fixed_point=len(alive), fixed_point_recomputed=False),
                summary=dict(controls=len(audits), colorings=sum(a['colorings'] for a in audits),
                             **totals, collision_source=left['source_index'],
                             collision_state=state, saved_action=chosen, saved_successor=successor,
                             profile_deletions=0, inherited_profiles=len(alive)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
