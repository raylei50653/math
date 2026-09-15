#!/usr/bin/env python3
"""Designed high-degree C5 disks: CD bits beyond corner collapse, and full AB|CD survivors.

python3 scripts/c5_corner_disks.py [--check]
A fixed pseudo-random family of triangulated disks with C5 boundary (no boundary
chords), kept only when boundary vertices 0 and 2 both have >= DEG_MIN interior
neighbours. Every aligned AB|CD cube through every x02 extension is recomputed with
last round's observers (blockers, S/T, interface, two newborn linkages, shortest
escape, corner test). Finite exact certificates on fixed graphs; no catalogue search,
no new k>=6 enumeration, no Lean. No count here is a theorem about all disks.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random

from c5_kempe_connectivity import CYCLE, PAIRS, adjacency, component, pair_components, swap
from c5_kempe_screen import normalize
from c5_ab_swap_cube import BOUNDARY, orient_and_verify
from c5_complementary_cube import (
    LAYERS, SPLIT, encode, failure_record, layer_counts, proper, scan_graph,
    singleton_distances, singleton_of, state_row, STATE_COLUMNS, SUMMARY_COLUMNS,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/corner_disks.json'
DEG_MIN = 4
SIZES = tuple(range(11, 21))
SEEDS = 200
FLIPS = 120
BIAS = 0.5
CROSS = tuple(p for p in PAIRS if p not in SPLIT)


def random_disk(rng, n_int, flips, bias=BIAS):
    """One pseudo-random triangulated disk on boundary C5 plus n_int interior vertices.

    Start from the cone over C5, insert the remaining interior vertices into faces,
    then perform `flips` random edge flips, rejecting a proposal that would create a
    boundary chord, a multi-edge or a vertex of degree < 4 (so interior degree >= 3),
    and with probability `bias` rejecting a proposal whose new edge misses {0, 2}.
    The result is verified as an oriented triangulated disk with facial C5 boundary.
    """
    n = 5 + n_int
    faces = {(i, (i + 1) % 5, 5) for i in range(5)}
    for v in range(6, n):
        a, b, c = rng.choice(sorted(faces))
        faces.remove((a, b, c))
        faces |= {(a, b, v), (b, c, v), (c, a, v)}
    arcs = {}
    for f in faces:
        for i in range(3):
            arcs[(f[i], f[(i + 1) % 3])] = f
    adj = [set() for _ in range(n)]
    for u, v in arcs:
        adj[u].add(v)
    done = attempts = 0
    while done < flips and attempts < 50 * flips:
        attempts += 1
        u, v = rng.choice(sorted(arcs))
        if (v, u) not in arcs:
            continue
        f1, f2 = arcs[(u, v)], arcs[(v, u)]
        w = next(x for x in f1 if x not in (u, v))
        x = next(y for y in f2 if y not in (u, v))
        if x in adj[w] or (w < 5 and x < 5) or len(adj[u]) <= 3 or len(adj[v]) <= 3:
            continue
        if rng.random() < bias and not {w, x} & {0, 2}:
            continue
        for f in (f1, f2):
            faces.remove(f)
            for i in range(3):
                del arcs[(f[i], f[(i + 1) % 3])]
        for f in ((u, x, w), (v, w, x)):
            faces.add(f)
            for i in range(3):
                arcs[(f[i], f[(i + 1) % 3])] = f
        adj[u].discard(v)
        adj[v].discard(u)
        adj[w].add(x)
        adj[x].add(w)
        done += 1
    edges = sorted({tuple(sorted(e)) for e in arcs})
    faces = sorted(faces)
    oriented = orient_and_verify(n, edges, faces)
    assert {e for e in edges if e[1] < 5} == {tuple(sorted(e)) for e in CYCLE}
    return edges, faces, oriented


def cd_flip_mechanism(s, o, block):
    """Classify one corner-compliant CD flip from interface-layer state s to state o.

    The interface edges inside the flipped block V reverse their C/D roles, so they
    cannot survive as interface edges; edges outside V stay C-D edges and survive iff
    both ends stay in S'/T'.
    """
    old = {tuple(e) for e in s['interface']}
    new = {tuple(e) for e in o['interface']}
    S2, T2 = set(o['S']), set(o['T'])
    outside = sorted(e for e in old if e[0] not in block)
    assert all(e[0] in block for e in old - set(outside))
    assert not (old - set(outside)) & new
    reversed_inside = sorted((v, u) for u, v in old - set(outside) if (v, u) in new)
    ends = [(u in S2, v in T2) for u, v in outside]
    assert all((u, v) in new for (u, v), (a, b) in zip(outside, ends) if a and b)
    if not o['passed']['blockers']:
        kind = 'blocker_broken_' + ('BC' if not o['blocker_BC'] else 'BD')
    elif new:
        kind = 'kept_outside_edge' if any(a and b for a, b in ends) else 'relocated_inside'
    else:
        kind = 'swallowed' if not outside else 'ends_detached'
    return dict(bits=s['bits'], block=sorted(block), kind=kind,
                old_interface=sorted(old), new_interface=sorted(new),
                reversed_inside=reversed_inside,
                edges_outside_block=len(outside), outside_ends_in_new=ends,
                S_before=s['S'], S_after=o['S'], T_before=s['T'], T_after=o['T'],
                first_failure_after=o['first_failure'], escape_after=o['escape_distance'])


def analyse_cube(cube):
    index = {tuple(s['bits']): s for s in cube['states']}
    compliant = []
    for r in cube['interface_layer_cd_flips']:
        if r['corner_violation']:
            continue
        s = index[tuple(r['bits'])]
        other = list(r['bits'])
        other[r['cd_bit']] ^= 1
        block = set(cube['components'][r['cd_bit']]['vertices'])
        m = cd_flip_mechanism(s, index[tuple(other)], block)
        assert (m['new_interface'] == []) == (r['interface_after'] == 0)
        compliant.append(m)
    cube['corner_safe_all_states'] = all(not s['corner_violations'] for s in cube['states'])
    cube['interface_states'] = sum(s['passed']['interface'] for s in cube['states'])
    cube['compliant_cd_flips'] = compliant
    return cube


def cross_moves(adj, c, dist):
    """Every single swap outside the AB|CD split from an aligned state, with its outcome."""
    rows = []
    for pair in CROSS:
        for s in sorted(pair_components(adj, c, pair), key=min):
            c2 = swap(c, s, pair)
            assert proper(adj, c2)
            d = normalize(c2)
            rows.append(dict(pair=pair, component=sorted(s),
                             boundary_in_component=sorted(s & set(range(5))),
                             boundary_after=d[:5], singleton_after=singleton_of(d),
                             escape_after=dist.get(d)))
    return rows


def closed_classes(adj, colours, dist):
    """Kempe classes containing no forbidden singleton, with their boundary profiles.

    Such a class has singletons only at 0 or 2; it never contains an x02 extension,
    the same P in {0,2} with x02 = 0 shape as catalogue masks 424, 960 and 1000.
    """
    unseen = {c for c in colours if c not in dist}
    classes = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        for c in queue:
            for pair in PAIRS:
                for block in pair_components(adj, c, pair):
                    d = normalize(swap(c, block, pair))
                    assert d not in dist
                    if d in unseen:
                        unseen.remove(d)
                        queue.append(d)
        profile = Counter(c[:5] for c in queue)
        assert BOUNDARY not in profile
        assert all(singleton_of(b) in (None, 0, 2) for b in profile)
        classes.append(dict(size=len(queue),
                            boundary={''.join(map(str, b)): k for b, k in sorted(profile.items())}))
    return classes


def survivor_detail(disk, cube, adj, dist):
    """Full certificate of one cube that passes the strongest condition in every state."""
    n = 5 + disk['n_int']
    assert cube['summary']['all_newborn']
    for s in cube['states']:
        c = tuple(s['coloring'])
        assert proper(adj, c) and c[:5] == BOUNDARY
        for name in ('blocker_BC_path', 'blocker_BD_path', 'newborn_AD_path', 'newborn_AC_path'):
            assert s[name]
        assert s['interface'] and not s['corner_violations']
        assert s['escape_distance'] >= 2
        s['cross_moves'] = cross_moves(adj, c, dist)
        # The cube is AB|CD-closed and has no one-step escape, so a shortest escape
        # from its minimum-distance state starts with a cross move.
        assert any(r['escape_after'] == s['escape_distance'] - 1 for r in s['cross_moves'])
        # Only boundary-touching cross components shorten the escape in these examples.
        assert all(r['escape_after'] >= s['escape_distance'] for r in s['cross_moves']
                   if not r['boundary_in_component'])
    esc = cube['shortest_escape']
    first = esc['moves'][0]
    start = tuple(cube['start'])
    assert frozenset(first['component']) in pair_components(adj, start, tuple(first['pair']))
    assert tuple(first['coloring']) == swap(start, set(first['component']), tuple(first['pair']))
    assert tuple(first['pair']) in CROSS
    return dict(disk=disk['index'], seed=disk['seed'], n_int=disk['n_int'], n=n,
                edges=disk['edges'], faces=disk['faces'], oriented_faces=disk['oriented'],
                degrees=[len(adj[v]) for v in range(n)],
                interior_degree_0_2=disk['interior_degree_0_2'],
                start=cube['start'], components=cube['components'],
                ab_dimension=cube['ab_dimension'], cd_dimension=cube['cd_dimension'],
                states=cube['states'], shortest_escape=esc,
                first_escape_move=dict(pair=first['pair'], component=first['component'],
                                       boundary_in_component=sorted(
                                           set(first['component']) & set(range(5)))))


def scan_family():
    disks = []
    all_cubes = []
    survivors = []
    seen = set()
    generated = duplicates = 0
    for n_int in SIZES:
        for seed in range(SEEDS):
            rng = random.Random(seed * 1000 + n_int)
            edges, faces, oriented = random_disk(rng, n_int, FLIPS)
            generated += 1
            n = 5 + n_int
            adj = adjacency(n, edges)
            deg = [len(adj[0]) - 2, len(adj[2]) - 2]
            if min(deg) < DEG_MIN:
                continue
            if tuple(edges) in seen:
                duplicates += 1
                continue
            seen.add(tuple(edges))
            colours, dist, step = singleton_distances(adj, n)
            starts = sorted(c for c in colours if c[:5] == BOUNDARY)
            cubes = [analyse_cube(c) for c in scan_graph(adj, dist, step, starts)]
            disk = dict(index=len(disks), seed=seed, n_int=n_int, edges=edges, faces=faces,
                        oriented=oriented, interior_degree_0_2=deg,
                        min_interior_degree=min(len(adj[v]) for v in range(5, n)),
                        x02_extensions=len(starts), normalized_colorings=len(colours),
                        unreachable_from_forbidden=sum(c not in dist for c in colours),
                        closed_classes=closed_classes(adj, colours, dist), cubes=cubes)
            for c in cubes:
                c['disk'] = disk['index']
                if c['summary']['all_newborn']:
                    survivors.append(survivor_detail(disk, c, adj, dist))
            disks.append(disk)
            all_cubes += cubes
    return dict(generated=generated, kept=len(disks), duplicates=duplicates), disks, all_cubes, survivors


def corner_counts(all_cubes):
    compliant = [m for c in all_cubes for m in c['compliant_cd_flips']]
    strongest = [r for c in all_cubes for r in c['flips']]
    return dict(
        cubes_corner_safe_all_states=sum(c['corner_safe_all_states'] for c in all_cubes),
        cubes_corner_safe_cd_dim_pos=sum(c['corner_safe_all_states'] and c['cd_dimension'] > 0
                                         for c in all_cubes),
        cubes_corner_safe_cd_dim_pos_with_interface_state=sum(
            c['corner_safe_all_states'] and c['cd_dimension'] > 0 and c['interface_states'] > 0
            for c in all_cubes),
        compliant_cd_flips=len(compliant),
        compliant_kinds=dict(sorted(Counter(m['kind'] for m in compliant).items())),
        compliant_interface_kept=sum(bool(m['new_interface']) for m in compliant),
        compliant_interface_emptied=sum(not m['new_interface'] for m in compliant),
        compliant_reversed_inside_edges=sum(len(m['reversed_inside']) for m in compliant),
        compliant_first_failure_after=dict(sorted(Counter(
            m['first_failure_after'] or 'none' for m in compliant).items())),
        compliant_escape_after=dict(sorted(Counter(str(m['escape_after'])
                                                   for m in compliant).items())),
        strongest_state_cd_flips=dict(sorted(Counter(
            (r['after']['first_failure'] or 'none') for r in strongest if r['kind'] == 'CD').items())),
        strongest_state_ab_flips=dict(sorted(Counter(
            (r['after']['first_failure'] or 'none') for r in strongest if r['kind'] == 'AB').items())))


def disk_row(d):
    return [d['index'], d['seed'], d['n_int'], sha256(json.dumps(d['edges']).encode()).hexdigest()[:16],
            *d['interior_degree_0_2'], d['min_interior_degree'], d['x02_extensions'],
            d['normalized_colorings'], d['unreachable_from_forbidden'], len(d['closed_classes']),
            len(d['cubes']),
            sum(c['summary']['all_blockers'] for c in d['cubes']),
            sum(c['summary']['all_interface'] for c in d['cubes']),
            sum(c['summary']['all_newborn'] for c in d['cubes'])]


DISK_COLUMNS = ('disk', 'seed', 'n_int', 'edge_hash16', 'interior_degree_0', 'interior_degree_2',
                'min_interior_degree', 'x02_extensions', 'normalized_colorings',
                'unreachable_from_forbidden', 'closed_classes', 'cubes', 'cubes_all_blockers',
                'cubes_all_interface', 'cubes_all_newborn')
CUBE_COLUMNS = ('disk', 'start', 'ab_dimension', 'cd_dimension', 'corner_safe_all_states',
                *SUMMARY_COLUMNS, 'earliest_failing_bits', 'first_failure', 'shortest_escape')


def cube_row(c):
    e = c['earliest_failure']
    return [c['disk'], ''.join(map(str, c['start'])), c['ab_dimension'], c['cd_dimension'],
            c['corner_safe_all_states'], *[c['summary'][k] for k in SUMMARY_COLUMNS],
            ''.join(map(str, e['bits'])) if e else None,
            e['first_failure'] if e else None, e['shortest_escape'] if e else None]


def report():
    generation, disks, all_cubes, survivors = scan_family()
    assert generation == dict(generated=2000, kept=1318, duplicates=0)
    counts = layer_counts(all_cubes)
    corner = corner_counts(all_cubes)
    assert counts['per_state']['total'] == 25288 and counts['per_cube']['total'] == 7750
    assert counts['per_cube'] == dict(total=7750, all_blockers=226, all_interface=67,
                                      all_newborn=3, full_cube=3)
    assert len(survivors) == 3
    # Every aligned state escapes, so every scanned cube is a control example. The few
    # Kempe classes without a forbidden singleton have x02 = 0 (checked in closed_classes).
    assert all(s['escape_distance'] is not None for c in all_cubes for s in c['states'])
    closed = [dict(disk=d['index'], **k) for d in disks for k in d['closed_classes']]
    assert len(closed) == 8 and len({k['disk'] for k in closed}) == 7
    cd = counts['interface_layer_cd_flips']
    # Corner test still predicts the trivialisations exactly, but most interface-layer
    # CD flips are corner-compliant here, and they split every possible way.
    assert cd['corner_violations'] == cd['either_trivial_after']
    assert corner['compliant_cd_flips'] == cd['total'] - cd['corner_violations']
    assert set(corner['compliant_kinds']) == {'blocker_broken_BC', 'blocker_broken_BD',
                                              'ends_detached', 'kept_outside_edge',
                                              'relocated_inside', 'swallowed'}
    assert corner['compliant_interface_kept'] > 0 and corner['compliant_interface_emptied'] > 0
    assert corner['strongest_state_cd_flips'].get('none', 0) > 0
    # Every survivor: no one-step escape, and the shortest escape starts with a cross move.
    first = Counter((tuple(s['first_escape_move']['pair']),
                     tuple(s['first_escape_move']['boundary_in_component']),
                     s['shortest_escape']['singleton'], len(s['shortest_escape']['moves']))
                    for s in survivors)
    strongest = [(c, s) for c in all_cubes for s in c['states'] if s['passed']['newborn']]
    files = [Path(__file__), ROOT / 'scripts/c5_complementary_cube.py',
             ROOT / 'scripts/c5_kempe_connectivity.py', ROOT / 'scripts/c5_ab_swap_cube.py',
             ROOT / 'scripts/c5_kempe_screen.py']
    return dict(
        trust='Finite exact certificates on fixed pseudo-random disks. Aligned-cube completeness and disk separation are paper lemmas. Nothing here is a theorem about all disks, nothing is Lean, and no zero or nonzero count is a proof of the main lemma.',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
        family=dict(sizes=SIZES, seeds=SEEDS, flips=FLIPS, bias=BIAS, deg_min=DEG_MIN,
                    rng='random.Random(seed * 1000 + n_int)', **generation,
                    boundary=BOUNDARY, split=SPLIT, cross_pairs=CROSS,
                    isomorphic_disks_merged=False),
        counts=counts, corner=corner,
        strongest_states=[dict(disk=c['disk'], ab_dimension=c['ab_dimension'],
                               cd_dimension=c['cd_dimension'], **failure_record(s))
                          for c, s in strongest],
        compliant_cd_flips=[dict(disk=c['disk'], start=c['start'], **m)
                            for c in all_cubes for m in c['compliant_cd_flips']],
        survivors=survivors,
        closed_classes=closed,
        survivor_first_escape_moves=[dict(pair=k[0], boundary_in_component=k[1],
                                          singleton=k[2], length=k[3], count=v)
                                     for k, v in sorted(first.items())],
        disk_columns=DISK_COLUMNS, disks=[disk_row(d) for d in disks],
        cube_columns=CUBE_COLUMNS,
        cubes_reaching_blockers=[cube_row(c) for c in all_cubes
                                 if any(s['passed']['blockers'] for s in c['states'])])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = encode(result) + '\n'
    assert json.loads(encoded) == json.loads(json.dumps(result))
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    print(json.dumps(dict(family=result['family'], per_state=result['counts']['per_state'],
                          per_cube=result['counts']['per_cube'],
                          interface_layer_cd_flips=result['counts']['interface_layer_cd_flips'],
                          corner=result['corner'],
                          strongest_state_flips=result['counts']['strongest_state_flips'],
                          survivor_first_escape_moves=result['survivor_first_escape_moves']),
                     sort_keys=True, indent=1))


if __name__ == '__main__':
    main()
