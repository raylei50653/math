#!/usr/bin/env python3
"""Full aligned AB|CD swap cubes on the existing C5 witness corpus and Errera controls.

python3 scripts/c5_complementary_cube.py [--check]
Lemma discovery and counterexample search over fixed graphs. No catalogue
search, no new k>=6 enumeration, no Lean. Every state is recomputed on its own
actual colouring; zero survivors is a finite observation, not a theorem.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

from c5_kempe_connectivity import (
    CAT, CYCLE, PAIRS, THREE, adjacency, colorings, component, pair_components, swap,
)
from c5_kempe_screen import normalize
from c5_adjacent_singleton_counts import FOUR
from c5_ab_swap_cube import (
    BOUNDARY, ERRERA, FACES, NEW_TO_OLD, START, orient_and_verify, path,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/complementary_cube.json'
SPLIT = ((0, 1), (2, 3))
LAYERS = ('blockers', 'interface', 'newborn')
PATTERNS = ((0, 1, 0, 1, 2), (0, 1, 0, 2, 1), (0, 1, 0, 2, 3), (0, 1, 2, 0, 1),
            (0, 1, 2, 0, 2), (0, 1, 2, 0, 3), (0, 1, 2, 1, 2), (0, 1, 2, 1, 3),
            (0, 1, 2, 3, 1), (0, 1, 2, 3, 2))


def proper(adj, c):
    return all(c[u] != c[v] for u in range(len(adj)) for v in adj[u])


def singleton_of(c):
    b = c[:5]
    if len(set(b)) != 3:
        return None
    return next(i for i in range(5) if b.count(b[i]) == 1)


def singleton_distances(adj, n):
    """Multi-source BFS on S4-normalized colourings from every forbidden singleton.

    Kempe moves commute with global recolouring, so the quotient distance is the
    labeled shortest full-Kempe distance to any singleton outside {0,2}.
    """
    colours = set()
    order = sorted(range(5, n), key=lambda v: (-len(adj[v]), v))
    for b in PATTERNS:
        c = list(b) + [-1] * (n - 5)
        if any(c[u] == c[v] for u in range(5) for v in adj[u] if v < 5):
            continue

        def extend(depth):
            if depth == n - 5:
                colours.add(tuple(c))
                return
            v = order[depth]
            forbidden = {c[u] for u in adj[v]}
            for colour in range(4):
                if colour not in forbidden:
                    c[v] = colour
                    extend(depth + 1)
            c[v] = -1

        extend(0)
    dist = {}
    step = {}
    queue = deque()
    for c in sorted(colours):
        if singleton_of(c) not in (None, 0, 2):
            dist[c] = 0
            queue.append(c)
    while queue:
        c = queue.popleft()
        for pair in PAIRS:
            for s in sorted(pair_components(adj, c, pair), key=lambda s: min(s)):
                d = normalize(swap(c, s, pair))
                if d not in dist:
                    dist[d] = dist[c] + 1
                    # A shortest move from d goes back to c (pair renamed by normalize).
                    step[d] = c
                    queue.append(d)
    return colours, dist, step


def route(adj, start, dist, step):
    """Reconstruct and re-verify one shortest actual-component escape from start."""
    if start not in dist:
        return None
    c = start
    moves = []
    while dist[c] > 0:
        target = step[c]
        pair, s = next((pair, s) for pair in PAIRS for s in pair_components(adj, c, pair)
                       if normalize(swap(c, s, pair)) == target)
        c2 = swap(c, s, pair)
        assert proper(adj, c2) and normalize(c2) == target
        moves.append(dict(pair=pair, component=sorted(s), coloring=c2))
        c = target
    assert singleton_of(c) not in (None, 0, 2)
    return dict(singleton=singleton_of(c), moves=moves)


def observe(adj, c, dist):
    """All observables of one aligned state, computed on its actual colouring."""
    assert c[:5] == BOUNDARY and proper(adj, c)
    result = dict(coloring=c, singleton_reached=False, escape_distance=dist.get(c))
    bc = path(adj, {v for v, k in enumerate(c) if k in (1, 2)}, 1, 3)
    bd = path(adj, {v for v, k in enumerate(c) if k in (1, 3)}, 1, 4)
    result.update(blocker_BC=bc is not None, blocker_BD=bd is not None,
                  blocker_BC_path=bc, blocker_BD_path=bd)
    s, t = component(adj, c, (0, 2), 0), component(adj, c, (0, 3), 2)
    result.update(S=sorted(s), T=sorted(t),
                  S_separated=s & set(range(5)) == {0},
                  T_separated=t & set(range(5)) == {2})
    interface = sorted((u, v) for u in s if c[u] == 2 for v in adj[u] & t if c[v] == 3)
    cd_blocks = sorted(pair_components(adj, c, (2, 3)), key=lambda b: min(b))
    cd_owner = {v: j for j, block in enumerate(cd_blocks) for v in block}
    # A C-D edge is an edge of the CD induced graph, so both ends share a block.
    assert all(cd_owner[u] == cd_owner[v] for u, v in interface)
    result.update(interface=interface,
                  interface_cd_components=sorted({cd_owner[u] for u, _ in interface}),
                  interface_in_boundary_cd_component=[cd_owner[u] == cd_owner[3]
                                                      for u, _ in interface])
    # Corner test: an internal CD block V trivialises S after its swap iff it holds
    # every C-neighbour of 0 and no D-neighbour of 0 (dually T, vertex 2, D/C).
    v0 = cd_owner[3]
    corner = []
    for j, block in enumerate(cd_blocks):
        if j == v0:
            continue
        nc0 = {u for u in adj[0] if c[u] == 2}
        nd0 = {u for u in adj[0] if c[u] == 3}
        nd2 = {u for u in adj[2] if c[u] == 3}
        nc2 = {u for u in adj[2] if c[u] == 2}
        kills_S = nc0 <= block and not nd0 & block
        kills_T = nd2 <= block and not nc2 & block
        if kills_S or kills_T:
            corner.append(dict(block=sorted(block), kills_S=kills_S, kills_T=kills_T))
    result.update(corner_violations=corner,
                  C_neighbours_of_0=sorted(u for u in adj[0] if c[u] == 2),
                  D_neighbours_of_2=sorted(u for u in adj[2] if c[u] == 3))
    blockers = bool(bc and bd)
    if blockers:
        # Paper disk-separation consequence; checked, never assumed.
        assert result['S_separated'] and result['T_separated']
    if result['S_separated'] and result['T_separated']:
        cs, ct = swap(c, s, (0, 2)), swap(c, t, (0, 3))
        ad = path(adj, {v for v, k in enumerate(cs) if k in (0, 3)}, 2, 4)
        ac = path(adj, {v for v, k in enumerate(ct) if k in (0, 2)}, 0, 3)
        result.update(newborn_AD=ad is not None, newborn_AC=ac is not None,
                      newborn_AD_path=ad, newborn_AC_path=ac)
        if ad or ac:
            assert interface, 'a newborn linkage must exit through a C-D edge'
    else:
        result.update(newborn_AD=None, newborn_AC=None,
                      newborn_AD_path=None, newborn_AC_path=None)
    passed = dict(blockers=blockers,
                  interface=blockers and bool(interface),
                  newborn=blockers and bool(interface)
                  and bool(result['newborn_AD'] and result['newborn_AC']))
    result['passed'] = passed
    result['first_failure'] = next((name for name in LAYERS if not passed[name]), None)
    if result['first_failure'] == 'newborn':
        result['first_failure'] = 'newborn_' + ('AD' if not result['newborn_AD'] else 'AC')
    return result


def failure_record(state):
    return dict(bits=state['bits'], first_failure=state['first_failure'],
                blocker_BC=state['blocker_BC'], blocker_BD=state['blocker_BD'],
                interface=bool(state['interface']), newborn_AD=state['newborn_AD'],
                newborn_AC=state['newborn_AC'], singleton_reached=state['singleton_reached'],
                shortest_escape=state['escape_distance'],
                S_size=len(state['S']), T_size=len(state['T']))


def aligned_cube(adj, start, dist):
    """Every aligned AB|CD state: one bit per INTERNAL AB or CD component.

    The boundary components U0 (>= {0,1,2}) and V0 (>= {3,4}) stay fixed; toggling
    them is the same as a global A/B or C/D relabel, so this is the full aligned
    orbit of every finite AB|CD swap sequence. Verified below against the labeled
    orbit modulo normalize. Components are re-derived in every state.
    """
    assert start[:5] == BOUNDARY
    entries = []
    boundary = {}
    for pair, anchor in ((SPLIT[0], (0, 1, 2)), (SPLIT[1], (3, 4))):
        blocks = sorted(pair_components(adj, start, pair), key=lambda b: min(b))
        boundary[pair] = next(b for b in blocks if anchor[0] in b)
        assert set(anchor) <= boundary[pair]
        entries += [(pair, b) for b in blocks if b is not boundary[pair]]
    states = {}
    for bits in range(1 << len(entries)):
        c = start
        for j, (pair, block) in enumerate(entries):
            if bits >> j & 1:
                assert block in pair_components(adj, c, pair)
                c = swap(c, block, pair)
        assert proper(adj, c) and c[:5] == BOUNDARY
        for pair in SPLIT:
            assert pair_components(adj, c, pair) == pair_components(adj, start, pair)
        states[bits] = c
    # Cross-check: labeled orbit of ALL components, quotient by global relabel.
    all_blocks = [(pair, b) for pair in SPLIT
                  for b in sorted(pair_components(adj, start, pair), key=lambda b: min(b))]
    labeled = set()
    for bits in range(1 << len(all_blocks)):
        c = start
        for j, (pair, block) in enumerate(all_blocks):
            if bits >> j & 1:
                c = swap(c, block, pair)
        labeled.add(c)
    assert len(labeled) == 1 << len(all_blocks)
    assert {normalize(c) for c in labeled} == set(states.values())
    obs = {}
    for bits, c in states.items():
        o = observe(adj, c, dist)
        o['bits'] = [int(bits >> j & 1) for j in range(len(entries))]
        obs[bits] = o
    ab_bits = [j for j, (pair, _) in enumerate(entries) if pair == SPLIT[0]]
    cd_bits = [j for j, (pair, _) in enumerate(entries) if pair == SPLIT[1]]
    # AB sub-cubes: fix the CD bits, vary the AB bits (last round's AB cubes).
    subcubes = {}
    for bits in states:
        subcubes.setdefault(tuple(bits >> j & 1 for j in cd_bits), []).append(bits)
    summary = {}
    for name in LAYERS:
        summary['all_' + name] = all(o['passed'][name] for o in obs.values())
        summary['ab_subcubes_all_' + name] = sum(all(obs[b]['passed'][name] for b in group)
                                                 for group in subcubes.values())
    summary['ab_subcubes'] = len(subcubes)
    failing = [bits for bits in states if not obs[bits]['passed']['newborn']]
    earliest = None
    if failing:
        bits = min(failing, key=lambda b: (bin(b).count('1'), b))
        earliest = failure_record(obs[bits])
    return dict(start=start,
                boundary_components={str(p): sorted(b) for p, b in boundary.items()},
                components=[dict(pair=p, vertices=sorted(b)) for p, b in entries],
                dimension=len(entries), ab_dimension=len(ab_bits), cd_dimension=len(cd_bits),
                labeled_orbit=len(labeled), aligned_states=len(states),
                states=[obs[bits] for bits in sorted(states)],
                summary=summary, earliest_failure=earliest)


def flip_mechanisms(cube):
    """Single-bit flips out of states that pass the strongest condition."""
    index = {tuple(s['bits']): s for s in cube['states']}
    rows = []
    for bits, s in index.items():
        if not s['passed']['newborn']:
            continue
        for j, entry in enumerate(cube['components']):
            other = list(bits)
            other[j] ^= 1
            o = index[tuple(other)]
            kind = 'AB' if tuple(entry['pair']) == SPLIT[0] else 'CD'
            block = set(entry['vertices'])
            rows.append(dict(bits=list(bits), bit=j, kind=kind,
                             interface_inside_flipped=all(u in block for u, _ in s['interface']),
                             after=failure_record(o),
                             after_S=o['S'], after_T=o['T'], after_interface=o['interface']))
    return rows


def mechanism_key(row):
    a = row['after']
    parts = [row['kind'], a['first_failure'] or 'none', f"S{a['S_size']}", f"T{a['T_size']}"]
    if row['kind'] == 'CD':
        parts.append('interface_inside_flipped' if row['interface_inside_flipped']
                     else 'interface_outside_flipped')
    parts.append(f"escape{a['shortest_escape']}")
    return '|'.join(parts)


def interface_layer_cd_flips(cube):
    """Every CD flip out of a state passing blockers+interface, with the collapse test."""
    index = {tuple(s['bits']): s for s in cube['states']}
    rows = []
    for bits, s in index.items():
        if not s['passed']['interface']:
            continue
        for j, entry in enumerate(cube['components']):
            if tuple(entry['pair']) != SPLIT[1]:
                continue
            other = list(bits)
            other[j] ^= 1
            o = index[tuple(other)]
            block = set(entry['vertices'])
            violation = next((v for v in s['corner_violations'] if set(v['block']) == block), None)
            # The corner test predicts the trivialisation exactly.
            assert (o['S'] == [0]) == bool(violation and violation['kills_S'])
            assert (o['T'] == [2]) == bool(violation and violation['kills_T'])
            rows.append(dict(bits=list(bits), cd_bit=j,
                             interface_inside_flipped=all(u in block for u, _ in s['interface']),
                             corner_violation=violation is not None,
                             blockers_after=o['passed']['blockers'],
                             interface_after=len(o['interface']),
                             S_after=o['S'], T_after=o['T'],
                             collapsed=o['S'] == [0] and o['T'] == [2],
                             escape_after=o['escape_distance']))
    return rows


STATE_COLUMNS = ('bits', 'first_failure', 'escape', 'S_size', 'T_size', 'interface_size')
SUMMARY_COLUMNS = ('all_blockers', 'all_interface', 'all_newborn', 'ab_subcubes_all_blockers',
                   'ab_subcubes_all_interface', 'ab_subcubes_all_newborn', 'ab_subcubes')


def state_row(s):
    return [''.join(map(str, s['bits'])), s['first_failure'], s['escape_distance'],
            len(s['S']), len(s['T']), len(s['interface'])]


def compact_states(cube):
    """Cubes in which no state reaches the blocker layer keep only a row per state."""
    if any(s['passed']['blockers'] for s in cube['states']):
        return cube
    cube['state_columns'] = STATE_COLUMNS
    cube['states'] = [state_row(s) for s in cube['states']]
    return cube


def scan_graph(adj, dist, step, starts):
    """All aligned cubes through the given x02 extensions of one fixed graph."""
    seen = set()
    cubes = []
    for c in starts:
        if c in seen:
            continue
        cube = aligned_cube(adj, c, dist)
        seen.update(s['coloring'] for s in cube['states'])
        cube['shortest_escape'] = route(adj, c, dist, step)
        cube['flips'] = flip_mechanisms(cube)
        cube['interface_layer_cd_flips'] = interface_layer_cd_flips(cube)
        cubes.append(cube)
    assert seen == set(starts)
    return cubes


def catalogue_scan():
    catalog = json.loads(CAT.read_text())
    masks = []
    cubes = []
    for mask, entry in sorted(catalog['cells'].items(), key=lambda p: int(p[0])):
        m = int(mask)
        support = sorted(i for i, j in THREE.items() if m >> j & 1)
        edges = sorted({tuple(sorted(e)) for e in (*CYCLE, *entry['edges'])})
        n = 5 + entry['k_eff']
        adj = adjacency(n, edges)
        colours, dist, step = singleton_distances(adj, n)
        starts = sorted(c for c in colorings(entry['k_eff'], edges) if c[:5] == BOUNDARY)
        assert set(starts) == {c for c in colours if c[:5] == BOUNDARY}
        assert (m >> FOUR[0, 2] & 1) == bool(starts)
        for cube in scan_graph(adj, dist, step, starts):
            cube['mask'] = m
            cubes.append(cube)
        masks.append(dict(mask=m, k_eff=entry['k_eff'], edges=edges, singleton_support=support,
                          interior_degree_0_2=[len(adj[0]) - 2, len(adj[2]) - 2],
                          x02_extensions=len(starts),
                          true_candidate=set(support) <= {0, 2} and bool(starts),
                          normalized_colorings=len(colours),
                          unreachable_from_forbidden=sum(c not in dist for c in colours)))
    return masks, cubes


def layer_counts(cubes):
    states = [s for cube in cubes for s in cube['states']]
    assert all(isinstance(s, dict) for s in states)
    per_state = dict(total=len(states),
                     **{name: sum(s['passed'][name] for s in states) for name in LAYERS})
    per_cube = dict(total=len(cubes),
                    **{'all_' + name: sum(c['summary']['all_' + name] for c in cubes)
                       for name in LAYERS})
    per_cube['full_cube'] = per_cube['all_newborn']
    ab_subcubes = dict(total=sum(c['summary']['ab_subcubes'] for c in cubes),
                       **{'all_' + name: sum(c['summary']['ab_subcubes_all_' + name] for c in cubes)
                          for name in LAYERS})
    errera_pattern = {name: sum(c['summary']['ab_subcubes_all_' + name] > 0
                                and not c['summary']['all_' + name] for c in cubes)
                      for name in LAYERS}
    flips = Counter(mechanism_key(r) for c in cubes for r in c['flips'])
    cd_rows = [r for c in cubes for r in c['interface_layer_cd_flips']]
    return dict(per_state=per_state, per_cube=per_cube, ab_subcubes=ab_subcubes,
                some_ab_subcube_passes_but_cube_fails=errera_pattern,
                first_failure=dict(sorted(Counter(s['first_failure'] or 'none' for s in states).items())),
                escape_distance=dict(sorted(Counter(str(s['escape_distance'])
                                                    for s in states).items())),
                dimensions=dict(sorted(Counter(f"ab{c['ab_dimension']}_cd{c['cd_dimension']}"
                                               for c in cubes).items())),
                strongest_state_flips=dict(sorted(flips.items())),
                interface_layer_cd_flips=dict(
                    total=len(cd_rows),
                    interface_inside_flipped=sum(r['interface_inside_flipped'] for r in cd_rows),
                    interface_empty_after=sum(r['interface_after'] == 0 for r in cd_rows),
                    collapsed_to_singletons=sum(r['collapsed'] for r in cd_rows),
                    S_trivial_after=sum(r['S_after'] == [0] for r in cd_rows),
                    T_trivial_after=sum(r['T_after'] == [2] for r in cd_rows),
                    either_trivial_after=sum(r['S_after'] == [0] or r['T_after'] == [2]
                                             for r in cd_rows),
                    corner_violations=sum(r['corner_violation'] for r in cd_rows),
                    blockers_kept=sum(r['blockers_after'] for r in cd_rows),
                    escape_after=dict(sorted(Counter(str(r['escape_after']) for r in cd_rows).items()))))


def errera_triangulation():
    """The full 17-vertex Errera triangulation in Sage's labels: 45 edges, 30 faces."""
    old = NEW_TO_OLD
    faces = [tuple(old[i] for i in f) for f in FACES]
    ring = (1, 14, 16, 7, 15)
    faces += [(0, ring[i], ring[(i + 1) % 5]) for i in range(5)]
    edges = sorted({tuple(sorted((u, v))) for u, vs in ERRERA.items() for v in vs})
    assert len(edges) == 45 and len(faces) == 30
    adj = {u: set() for u in range(17)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return edges, faces, adj


def link_cycle(adj, v):
    nb = sorted(adj[v])
    cyc = [nb[0]]
    while len(cyc) < len(nb):
        cyc.append(min(w for w in adj[cyc[-1]] & set(nb) if w not in cyc))
    assert cyc[0] in adj[cyc[-1]]
    return cyc


def errera_family():
    """Delete each degree-5 vertex of the Errera triangulation; all 10 D5 alignments.

    Each of the 120 labeled disks is verified as an oriented triangulated disk with
    the specified C5 boundary. Isomorphic disks are NOT merged; this is a control
    family built from one fixed source, not a graph catalogue search.
    """
    edges_old, faces_old, adj_old = errera_triangulation()
    disks = []
    all_cubes = []
    for v in range(17):
        if len(adj_old[v]) != 5:
            continue
        cyc = link_cycle(adj_old, v)
        for rot in range(5):
            for refl in (1, -1):
                b = [cyc[(rot + refl * i) % 5] for i in range(5)]
                interior = [u for u in range(17) if u != v and u not in b]
                new = {u: i for i, u in enumerate(b + interior)}
                edges = sorted(tuple(sorted((new[x], new[y])))
                               for x, y in edges_old if v not in (x, y))
                faces = [tuple(new[x] for x in f) for f in faces_old if v not in f]
                try:
                    orient_and_verify(16, edges, faces)
                except AssertionError:
                    f0 = faces[0]
                    orient_and_verify(16, edges, [(f0[0], f0[2], f0[1])] + faces[1:])
                adj = adjacency(16, edges)
                colours, dist, step = singleton_distances(adj, 16)
                starts = sorted(c for c in colours if c[:5] == BOUNDARY)
                cubes = scan_graph(adj, dist, step, starts)
                first = not disks
                if first:
                    # The first labeled disk is exactly last round's fixed control.
                    assert edges == sorted(tuple(sorted((new[x], new[y])))
                                           for x, vs in ERRERA.items() for y in vs
                                           if x != 0 and y != 0)
                    assert any(c['start'] == START for c in cubes)
                disks.append(dict(deleted_vertex=v, boundary_old_labels=b, rotation=rot,
                                  reflection=refl, edges=edges, x02_extensions=len(starts),
                                  interior_degree_0_2=[len(adj[0]) - 2, len(adj[2]) - 2],
                                  normalized_colorings=len(colours),
                                  cubes=cubes if first else [dict(
                                      start=c['start'],
                                      components=[[*e['pair'], *e['vertices']]
                                                  for e in c['components']],
                                      summary=[c['summary'][k] for k in SUMMARY_COLUMNS],
                                      states=[state_row(s) for s in c['states']])
                                         for c in cubes]))
                all_cubes += cubes
    assert len(disks) == 120
    return disks, all_cubes


def encode(obj, level=0):
    """Deterministic JSON: dicts one key per line, scalar lists inline."""
    pad = ' ' * (level + 1)
    if isinstance(obj, dict):
        if not obj:
            return '{}'
        items = (f'{pad}{json.dumps(str(k))}: {encode(v, level + 1)}' for k, v in obj.items())
        return '{\n' + ',\n'.join(items) + '\n' + ' ' * level + '}'
    if isinstance(obj, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) for x in obj):
            return json.dumps(list(obj))
        return '[\n' + ',\n'.join(pad + encode(x, level + 1) for x in obj) + '\n' + ' ' * level + ']'
    return json.dumps(obj)


def negative_controls():
    """Boundary-only toggling misses aligned states with two internal CD components."""
    adj = adjacency(7, [*CYCLE, (0, 5), (1, 5), (0, 6), (2, 6)])
    start = (*BOUNDARY, 2, 3)
    _, dist, _ = singleton_distances(adj, 7)
    cube = aligned_cube(adj, start, dist)
    assert cube['cd_dimension'] == 2 and cube['aligned_states'] == 4
    v0 = component(adj, start, (2, 3), 3)
    boundary_only = {normalize(start), normalize(swap(start, v0, (2, 3)))}
    assert len(boundary_only) == 2 < cube['aligned_states']
    return dict(two_internal_cd_components_states=cube['aligned_states'],
                boundary_only_states=len(boundary_only))


def report():
    masks, cubes = catalogue_scan()
    assert sum(m['x02_extensions'] for m in masks) == 176
    assert not any(m['true_candidate'] for m in masks)
    assert sum(1 for m in masks if set(m['singleton_support']) <= {0, 2}) == 3
    counts = layer_counts(cubes)
    assert counts['per_cube']['full_cube'] == 0
    # The AB sub-cubes reproduce last round's 166 / 20 / 4 / 0 AB cubes exactly.
    assert counts['ab_subcubes'] == dict(total=166, all_blockers=20, all_interface=4, all_newborn=0)
    assert counts['per_state']['newborn'] == 1
    strongest = [(c['mask'], s) for c in cubes for s in c['states'] if s['passed']['newborn']]
    assert strongest[0][0] == 935
    cd = counts['interface_layer_cd_flips']
    assert cd['total'] == cd['interface_inside_flipped'] == cd['interface_empty_after'] \
        == cd['collapsed_to_singletons'] == 2
    failures = [[c['mask'], ''.join(map(str, c['start'])), c['ab_dimension'], c['cd_dimension'],
                 ''.join(map(str, c['earliest_failure']['bits'])),
                 c['earliest_failure']['first_failure'], c['earliest_failure']['shortest_escape'],
                 c['summary']['ab_subcubes_all_interface']]
                for c in cubes if not c['summary']['all_newborn']]
    assert len(failures) == len(cubes) == 123
    disks, family_cubes = errera_family()
    family = layer_counts(family_cubes)
    assert family['per_cube']['all_interface'] == 0 and family['per_cube']['full_cube'] == 0
    assert family['per_state']['newborn'] == 120
    fcd = family['interface_layer_cd_flips']
    # Every CD flip out of an interface-layer state empties the interface, keeps the
    # blockers, and collapses S or T to its boundary vertex; both collapse in 80.
    assert fcd['total'] == fcd['interface_empty_after'] == fcd['blockers_kept'] \
        == fcd['either_trivial_after'] == 160
    assert fcd['interface_inside_flipped'] == 120 and fcd['collapsed_to_singletons'] == 80
    assert fcd['corner_violations'] == 160 and cd['corner_violations'] == 2
    # No interface-layer state anywhere has an internal CD block that passes the corner test.
    assert all(r['corner_violation'] for c in cubes + family_cubes
               for r in c['interface_layer_cd_flips'])
    assert fcd['escape_after'] == {'2': 160}
    assert set(family['strongest_state_flips']) == {
        'AB|blockers|S9|T9|escape1', 'AB|none|S2|T2|escape3', 'AB|none|S4|T4|escape3',
        'CD|interface|S1|T1|interface_inside_flipped|escape2'}
    start_cube = next(c for c in disks[0]['cubes'] if c['start'] == START)
    assert start_cube['summary']['all_blockers'] and not start_cube['summary']['all_interface']
    assert start_cube['summary']['ab_subcubes_all_newborn'] == 1
    files = [Path(__file__), CAT, ROOT / 'scripts/c5_kempe_connectivity.py',
             ROOT / 'scripts/c5_ab_swap_cube.py', ROOT / 'scripts/c5_kempe_screen.py',
             ROOT / 'scripts/c5_adjacent_singleton_counts.py']
    return dict(
        trust='Finite exact certificates on fixed graphs. Aligned-cube completeness and disk separation are paper lemmas. Nothing here is a theorem about all disks, nothing is Lean, and no zero count is a proof.',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
        alignment=dict(chord=[0, 2], boundary=BOUNDARY, split=SPLIT,
                       relabel='only the global A/B or C/D permutation induced by fixing U0 and V0',
                       singleton_inside_cube='never: every aligned state has boundary (A,B,A,C,D)'),
        provenance=dict(catalogue=str(CAT.relative_to(ROOT)), witnesses=len(masks),
                        x02_extensions=176,
                        errera_source='scripts/c5_ab_swap_cube.py (Sage 10.6 ErreraGraph)',
                        errera_family='12 degree-5 deletions x 10 D5 alignments = 120 labeled disks'),
        candidates=dict(true_candidates_with_x02_extension=0,
                        masks_with_support_in_chord_02=[m['mask'] for m in masks
                                                         if set(m['singleton_support']) <= {0, 2}],
                        reason='P(G) in {0,2} with x_02>0 forces all five x_f>0 by the chord identity; no catalogued Sigma has that shape, so every scanned extension is a control example.'),
        corpus=dict(counts=counts, masks=masks, cubes=[compact_states(c) for c in cubes],
                    failure_columns=('mask', 'start', 'ab_dimension', 'cd_dimension',
                                     'earliest_failing_bits', 'first_failure', 'shortest_escape',
                                     'ab_subcubes_all_interface'),
                    failures=failures,
                    strongest_states=[dict(mask=m, **failure_record(s)) for m, s in strongest]),
        errera_family=dict(counts=family,
                           legend=dict(components='[pair colour, pair colour, vertices...]',
                                       summary=SUMMARY_COLUMNS, states=STATE_COLUMNS,
                                       full_detail='disks[0] only'),
                           disks=disks),
        negative_controls=negative_controls())


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
    print(json.dumps(dict(corpus=result['corpus']['counts'],
                          errera_family=result['errera_family']['counts'],
                          candidates=result['candidates']), sort_keys=True, indent=1))


if __name__ == '__main__':
    main()
