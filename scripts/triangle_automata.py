#!/usr/bin/env python3
"""Finite-state synthesis of triangle disk gadgets.

Grammar: ordered C5 (vertices 0..4) + one interior K3 (vertices 5,6,7) +
arbitrary boundary-to-K3 attachments. An attachment set is a word of five
letters; letter i is the subset of {5,6,7} adjacent to boundary vertex i,
encoded as mask bits 3*i + (v-5).

Two deterministic automata read the word along the boundary:

* ColorDFA: per canonical pattern, the triple of forbidden colour sets of the
  K3 vertices. Terminal acceptance is a proper injective K3 colouring.
* GeometryDFA: non-crossing chords in the annulus between C5 and K3. An
  accepting run is a cyclic monotone winding sequence and is turned into an
  explicit rotation system whose faces are checked with Euler's formula.

Everything here is computationally observed unless replayed in Lean
(Math/ColorDFA.lean, Math/GeometryDFA.lean). Only the forward direction of
the geometry automaton is claimed: accept implies an explicit rotation
system; agreement with the apex-planarity test is exhaustive enumeration, not
a completeness theorem. No four-colour theorem or boundary conjecture is used.

Run: uv run --with networkx==3.5 python scripts/triangle_automata.py
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

import networkx as nx
from search_boundary import CYCLE, REPS

INNER = (5, 6, 7)
BASE = tuple(sorted(CYCLE + ((5, 6), (5, 7), (6, 7))))
ATTACHMENTS = tuple(it.product(range(5), INNER))  # bit index 3*i + (v-5)
LETTERS = tuple(frozenset(v for v in INNER if l >> (v - 5) & 1) for l in range(8))
THREE = tuple(j for j, b in enumerate(REPS) if len(set(b)) == 3)
T3_BITS = sum(1 << j for j in THREE)
T4_BITS = sum(1 << j for j in range(10)) & ~T3_BITS
ORIENTATIONS = ({5: 0, 6: 1, 7: 2}, {5: 0, 7: 1, 6: 2})
INSIDE = tuple(it.permutations(range(4), 3))


def letters(mask):
    return tuple(mask >> (3 * i) & 7 for i in range(5))


def mask_of(word):
    return sum(l << (3 * i) for i, l in enumerate(word))


def chords(mask):
    return tuple(e for i, e in enumerate(ATTACHMENTS) if mask >> i & 1)


def edges_of(mask):
    return tuple(sorted(BASE + chords(mask)))


# ---------------------------------------------------------------- ColorDFA
def color_step(forbidden, letter, colour):
    return tuple(f | ({colour} if 5 + k in letter else frozenset()) for k, f in enumerate(forbidden))


def color_run(word, pattern):
    state = (frozenset(), frozenset(), frozenset())
    for i, l in enumerate(word):
        state = color_step(state, LETTERS[l], pattern[i])
    return state


def color_accept(forbidden):
    available = [set(range(4)) - f for f in forbidden]
    return any(len({x, y, z}) == 3 for x in available[0] for y in available[1] for z in available[2])


def sigma_bits(word):
    return sum(1 << j for j, b in enumerate(REPS) if color_accept(color_run(word, b)))


def sigma_bits_bruteforce(mask):
    edge_list = chords(mask)
    bits = 0
    for j, b in enumerate(REPS):
        if any(all(c[u] != c[v] for u, v in edge_list) for c in (b + t for t in INSIDE)):
            bits |= 1 << j
    return bits


def three_profile(bits):
    return ''.join('1' if bits >> j & 1 else '0' for j in THREE)


def unique_position(pattern):
    """The boundary vertex carrying the colour used once; defined for 3-colour patterns."""
    counts = {c: pattern.count(c) for c in pattern}
    singles = [i for i, c in enumerate(pattern) if counts[c] == 1]
    assert len(singles) == 1
    return singles[0]


# ------------------------------------------------------------- GeometryDFA
def fan_choices(letter, pos):
    vs = sorted(letter, key=lambda v: pos[v])
    return [vs[k:] + vs[:k] for k in range(len(vs))] or [[]]


def geometry_run(word):
    """First accepting run in a fixed order: (orientation, winding sequence) or None."""
    for orient, pos in enumerate(ORIENTATIONS):
        for choice in it.product(*(fan_choices(LETTERS[l], pos) for l in word)):
            seq = [(i, v) for i, fan in enumerate(choice) for v in fan]
            if not seq:
                return orient, seq
            positions = [pos[v] for _, v in seq]
            winding = sum((positions[(k + 1) % len(seq)] - positions[k]) % 3 for k in range(len(seq)))
            if winding in (0, 3):
                return orient, seq
    return None


def geometry_states(word):
    """Reachable GeometryDFA states after each prefix: (orient, first, last, winding)."""
    states = frozenset({(o, None, None, 0) for o in range(2)})
    trace = [states]
    for l in word:
        new = set()
        for o, first, last, wind in states:
            pos = ORIENTATIONS[o]
            for fan in fan_choices(LETTERS[l], pos):
                f, la, w = first, last, wind
                for v in fan:
                    p = pos[v]
                    if f is None:
                        f = la = p
                    else:
                        w += (p - la) % 3
                        la = p
                if w <= 3:
                    new.add((o, f, la, w))
        states = frozenset(new)
        trace.append(states)
    return trace


def geometry_accept_states(states):
    return any(f is None or w + (f - l) % 3 in (0, 3) for _, f, l, w in states)


def rotation_of(word, orient, seq):
    """Counterclockwise rotation system built from an accepting winding sequence."""
    pos = ORIENTATIONS[orient]
    by_pos = {p: v for v, p in pos.items()}
    rotation = {}
    for i in range(5):
        fan = [v for j, v in seq if j == i]
        rotation[i] = [(i - 1) % 5, (i + 1) % 5] + fan[::-1]
    for v in INNER:
        p = pos[v]
        mine = [k for k, (_, w) in enumerate(seq) if w == v]
        if mine and mine[0] == 0 and mine[-1] == len(seq) - 1 and len(mine) < len(seq):
            # the fan wraps around the cyclic sequence: start after the gap
            gap = next(k for k in range(len(mine)) if mine[k] + 1 not in mine and k + 1 < len(mine))
            mine = mine[gap + 1:] + mine[:gap + 1]
        rotation[v] = [seq[k][0] for k in mine] + [by_pos[(p + 1) % 3], by_pos[(p - 1) % 3]]
    return [rotation[u] for u in range(8)]


def faces_of(rotation):
    """Face orbits: dart (v,u) is followed by (u, successor of v around u)."""
    succ = {}
    for u, ring in enumerate(rotation):
        for k, v in enumerate(ring):
            succ[(v, u)] = (u, ring[(k + 1) % len(ring)])
    seen, faces = set(), []
    for u, ring in enumerate(rotation):
        for v in ring:
            dart = (u, v)
            if dart in seen:
                continue
            face = []
            while dart not in seen:
                seen.add(dart)
                face.append(dart)
                dart = succ[dart]
            faces.append(face)
    return faces


def components(rotation):
    seen, count = set(), 0
    for s in range(len(rotation)):
        if s in seen:
            continue
        count += 1
        stack = [s]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack.extend(rotation[u])
    return count


def check_rotation(mask, rotation):
    edge_set = set(edges_of(mask))
    darts = {(u, v) for u, ring in enumerate(rotation) for v in ring}
    assert all(len(set(ring)) == len(ring) and u not in ring for u, ring in enumerate(rotation))
    assert {tuple(sorted(d)) for d in darts} == edge_set and len(darts) == 2 * len(edge_set)
    faces = faces_of(rotation)
    # face orbits are per component, so each spherical component contributes 2
    euler = 8 - len(edge_set) + len(faces) == 2 * components(rotation)
    cycle = [(i, (i + 1) % 5) for i in range(5)]
    reverse = [(v, u) for u, v in cycle]
    c5_face = any(set(f) == set(cycle) or set(f) == set(reverse) for f in faces)
    return euler and c5_face, faces


def apex_planar(mask):
    if mask.bit_count() > 8:
        return False  # apex graph: 9 vertices, at most 21 edges
    g = nx.Graph()
    g.add_nodes_from(range(9))
    g.add_edges_from(edges_of(mask) + tuple((i, 8) for i in range(5)))
    return bool(nx.check_planarity(g)[0])


# ------------------------------------------------------------ Nerode quotient
def nerode(output, alphabet=8, length=5):
    """Layered minimal Moore machine for a function on complete words.

    Returns per layer: list of classes with representative prefix, prefix count,
    and transition row; plus prefix->class arrays in base-`alphabet` order.
    """
    layers, prefix_classes = [], []
    sig = {pre: output(pre) for pre in it.product(range(alphabet), repeat=length)}
    outputs = sorted(set(sig.values()), key=repr)
    ids = {s: k for k, s in enumerate(outputs)}
    cls = {pre: ids[s] for pre, s in sig.items()}
    layers.append([dict(id=k, output=s) for s, k in ids.items()])
    prefix_classes.append([cls[pre] for pre in it.product(range(alphabet), repeat=length)])
    for i in range(length - 1, -1, -1):
        sigs = {pre: tuple(cls[pre + (l,)] for l in range(alphabet))
                for pre in it.product(range(alphabet), repeat=i)}
        ids = {s: k for k, s in enumerate(sorted(set(sigs.values())))}
        cls = {pre: ids[s] for pre, s in sigs.items()}
        layer = []
        for s, k in ids.items():
            members = [pre for pre, s2 in sigs.items() if s2 == s]
            layer.append(dict(id=k, transitions=list(s), prefixes=len(members),
                              representative=list(members[0])))
        layers.insert(0, sorted(layer, key=lambda c: c['id']))
        prefix_classes.insert(0, [cls[pre] for pre in it.product(range(alphabet), repeat=i)])
    for layer in layers[:-1]:
        for c in layer:
            c['representative'] = list(c['representative'])
    return dict(states_per_layer=[len(l) for l in layers], layers=layers,
                prefix_classes=prefix_classes)


def raw_state(word, parts=('geometry', 'color')):
    """Unminimised product state: geometry state set and forbidden triples per pattern."""
    state = {}
    if 'geometry' in parts:
        geo = geometry_states(word)[-1]
        state['geometry'] = sorted(([o, f, l, w] for o, f, l, w in geo), key=repr)
    if 'color' in parts:
        state['forbidden'] = [[sorted(f) for f in color_run(word, b)] for b in REPS]
    return state


def attach_raw_states(machine, parts):
    """Record which unminimised product states each Nerode class merges."""
    for i, layer in enumerate(machine['layers'][:-1]):
        raw_of_class = {}
        for pre in it.product(range(8), repeat=i):
            k = machine['prefix_classes'][i][sum(l * 8 ** (i - 1 - j) for j, l in enumerate(pre))]
            raw_of_class.setdefault(k, set()).add(json.dumps(raw_state(pre, parts), sort_keys=True))
        for c in layer:
            raws = sorted(raw_of_class[c['id']])
            c['raw_states_merged'] = len(raws)
            c['raw_state_of_representative'] = raw_state(tuple(c['representative']), parts)
            c['raw_states'] = [json.loads(r) for r in raws]


def dump(path, obj, indent=None):
    text = json.dumps(obj, sort_keys=True, indent=indent, separators=None if indent else (',', ':')) + '\n'
    path.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()


def dump_lines(path, rows):
    text = ''.join(json.dumps(r, sort_keys=True, separators=(',', ':')) + '\n' for r in rows)
    path.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='artifacts/automata')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    hashes = {}

    # 1. every word: colour automaton vs brute force, geometry automaton vs apex test
    words, embeddings = [], []
    accept = {}
    disk_states = {}
    for mask in range(1 << 15):
        word = letters(mask)
        bits = sigma_bits(word)
        brute = sigma_bits_bruteforce(mask)
        run = geometry_run(word)
        trace = geometry_states(word)
        dfa_accept = geometry_accept_states(trace[-1])
        apex = apex_planar(mask)
        assert (run is not None) == dfa_accept
        accept[mask] = run is not None
        row = dict(mask=mask, letters=list(word), attachments=[list(e) for e in chords(mask)],
                   sigma_bits=bits, sigma_bits_bruteforce=brute, three_profile=three_profile(bits),
                   geometry_accept=run is not None, apex_planar=apex)
        words.append(row)
        if run is not None:
            orient, seq = run
            rotation = rotation_of(word, orient, seq)
            ok, faces = check_rotation(mask, rotation)
            assert ok, mask
            embeddings.append(dict(mask=mask, orientation=orient, winding_sequence=[list(e) for e in seq],
                                   rotation=rotation, faces=[[list(d) for d in f] for f in faces],
                                   face_count=len(faces), components=components(rotation),
                                   edges=[list(e) for e in edges_of(mask)]))
            disk_states.setdefault(bits, []).append(mask)
    agreement = dict(geometry_accept=sum(r['geometry_accept'] for r in words),
                     apex_planar=sum(r['apex_planar'] for r in words),
                     disagreements=[r['mask'] for r in words if r['geometry_accept'] != r['apex_planar']],
                     sigma_disagreements=[r['mask'] for r in words if r['sigma_bits'] != r['sigma_bits_bruteforce']],
                     words=len(words))
    hashes['words.jsonl'] = dump_lines(out / 'words.jsonl', words)
    hashes['disk_embeddings.jsonl'] = dump_lines(out / 'disk_embeddings.jsonl', embeddings)

    # 2. disk states, three-colour profiles, Z5 statistics
    states = []
    for bits in sorted(disk_states):
        masks = disk_states[bits]
        witness = min(masks, key=lambda m: (m.bit_count(), m))
        states.append(dict(state_bits=bits, three_profile=three_profile(bits),
                           accepted_patterns=[list(REPS[j]) for j in range(10) if bits >> j & 1],
                           accepted_three=[list(REPS[j]) for j in THREE if bits >> j & 1],
                           z5_positions=sorted(unique_position(REPS[j]) for j in THREE if bits >> j & 1),
                           full_four_colour=(bits & T4_BITS) == T4_BITS,
                           mask_count=len(masks), masks=masks,
                           min_edge_witness=dict(mask=witness, edges=[list(e) for e in edges_of(witness)])))
    hashes['disk_states.json'] = dump(out / 'disk_states.json', indent=1, obj=dict(
        pattern_order=[list(b) for b in REPS], three_colour_order=[list(REPS[j]) for j in THREE],
        unique_position_of_three_colour_pattern={''.join(map(str, REPS[j])): unique_position(REPS[j]) for j in THREE},
        count=len(states), states=states))

    profiles = []
    realized = {}
    for s in states:
        realized.setdefault(s['three_profile'], []).append(s)
    for subset in range(32):
        profile = ''.join('1' if subset >> k & 1 else '0' for k in range(5))
        positions = sorted(unique_position(REPS[THREE[k]]) for k in range(5) if subset >> k & 1)
        adjacent_pair = len(positions) == 2 and (positions[1] - positions[0]) % 5 in (1, 4)
        hits = realized.get(profile, [])
        profiles.append(dict(profile=profile, size=bin(subset).count('1'), z5_positions=positions,
                             adjacent_pair=adjacent_pair, realized=bool(hits),
                             disk_state_count=len(hits), disk_mask_count=sum(s['mask_count'] for s in hits),
                             witness=None if not hits else dict(state_bits=hits[0]['state_bits'],
                                                                mask=hits[0]['min_edge_witness']['mask'])))
    by_size = {}
    for p in profiles:
        d = by_size.setdefault(p['size'], dict(subsets=0, realized=0))
        d['subsets'] += 1
        d['realized'] += p['realized']
    z5 = dict(profiles=profiles, realized_profiles=sum(p['realized'] for p in profiles),
              by_size={str(k): v for k, v in sorted(by_size.items())},
              realized_pairs=[p['profile'] for p in profiles if p['size'] == 2 and p['realized']],
              all_realized_pairs_adjacent=all(p['adjacent_pair'] for p in profiles if p['size'] == 2 and p['realized']),
              all_adjacent_pairs_realized=all(p['realized'] for p in profiles if p['adjacent_pair']),
              empty_realized=any(p['realized'] for p in profiles if p['size'] == 0),
              singleton_realized=any(p['realized'] for p in profiles if p['size'] == 1),
              scope='Observed inside the C5 + K3 attachment grammar only; not a statement about arbitrary disk patches.')
    hashes['z5_profiles.json'] = dump(out / 'z5_profiles.json', z5, indent=1)

    # 3. T4 pairs
    count_of = {s['state_bits']: s['mask_count'] for s in states}
    pairs, ordered = [], 0
    for s, t in it.combinations_with_replacement(sorted(count_of), 2):
        if s & t != T4_BITS:
            continue
        n = count_of[s] * count_of[t]
        ordered += n if s == t else 2 * n
        pairs.append(dict(left_state=s, right_state=t, left_masks=count_of[s], right_masks=count_of[t],
                          unordered_realizations=n, left_three=three_profile(s), right_three=three_profile(t)))
    hashes['t4_pairs.json'] = dump(out / 't4_pairs.json', indent=1, obj=dict(
        target_bits=T4_BITS, state_pairs=len(pairs), ordered_mask_pairs=ordered,
        disk_masks=len(embeddings), all_ordered_mask_pairs=len(embeddings) ** 2, pairs=pairs))

    # 4. Nerode quotients of the layered automata
    bits_of = {r['mask']: r['sigma_bits'] for r in words}
    def out_full(pre):
        m = mask_of(pre)
        return (True, bits_of[m]) if accept[m] else None
    machines = dict(
        geometry=nerode(lambda pre: accept[mask_of(pre)]),
        color=nerode(lambda pre: bits_of[mask_of(pre)]),
        moore=nerode(out_full),
        three_colour=nerode(lambda pre: (bits_of[mask_of(pre)] & T3_BITS) if accept[mask_of(pre)] else None),
        single_bad=nerode(lambda pre: accept[mask_of(pre)] and bits_of[mask_of(pre)] & T3_BITS == 0),
    )
    parts = dict(geometry=('geometry',), color=('color',), moore=('geometry', 'color'))
    for name, m in machines.items():
        m['output'] = name
        m['alphabet'] = [sorted(l) for l in LETTERS]
        if name in parts:
            attach_raw_states(m, parts[name])
    raw_counts, live_counts = [], []
    for i in range(6):
        raws = {json.dumps(raw_state(pre), sort_keys=True): pre for pre in it.product(range(8), repeat=i)}
        raw_counts.append(len(raws))
        live_counts.append(sum(1 for r in raws if json.loads(r)['geometry']))
    machines['moore']['raw_product_states_per_layer'] = raw_counts
    machines['moore']['raw_product_states_with_live_geometry_per_layer'] = live_counts
    for name, m in machines.items():
        hashes[f'nerode_{name}.json'] = dump(out / f'nerode_{name}.json', m)

    # 5. two-component lockstep machine with target Σ_L ∩ Σ_R = T4
    moore = machines['moore']
    final_out = {c['id']: c['output'] for c in moore['layers'][5]}
    def pair_out(a, b):
        x, y = final_out[a], final_out[b]
        return x is not None and y is not None and (x[1] & y[1]) == T4_BITS
    trans = [{c['id']: c['transitions'] for c in layer} for layer in moore['layers'][:-1]]
    cur = {(a, b): pair_out(a, b) for a in final_out for b in final_out}
    ids = {v: k for k, v in enumerate(sorted(set(cur.values())))}
    cur = {k: ids[v] for k, v in cur.items()}
    pair_layers = [[dict(id=k, accept=v, members=sorted(p for p, c in cur.items() if c == k))
                    for v, k in ids.items()]]
    for i in range(4, -1, -1):
        sigs = {}
        for a in trans[i]:
            for b in trans[i]:
                sigs[(a, b)] = tuple(cur[(trans[i][a][l1], trans[i][b][l2])]
                                     for l1 in range(8) for l2 in range(8))
        ids = {s: k for k, s in enumerate(sorted(set(sigs.values())))}
        cur = {k: ids[s] for k, s in sigs.items()}
        pair_layers.insert(0, [dict(id=k, transitions=list(s),
                                    members=sorted(p for p, s2 in sigs.items() if s2 == s))
                               for s, k in ids.items()])
    live = [None] * 6
    live[5] = {c['id'] for c in pair_layers[5] if c['accept']}
    admissible = []
    for i in range(4, -1, -1):
        live[i] = {c['id'] for c in pair_layers[i] if any(t in live[i + 1] for t in c['transitions'])}
    for i in range(5):
        moves = 0
        for c in pair_layers[i]:
            c['live'] = c['id'] in live[i]
            c['admissible_letter_pairs'] = [[k // 8, k % 8] for k, t in enumerate(c['transitions'])
                                            if c['live'] and t in live[i + 1]]
            moves += len(c['admissible_letter_pairs'])
        admissible.append(dict(layer=i, live_classes=len(live[i]), classes=len(pair_layers[i]),
                               admissible_moves=moves, possible_moves=64 * len(live[i])))
    pair_machine = dict(target_bits=T4_BITS, alphabet='pairs of single-component letters (L, R), index 8*L+R',
                        states_per_layer=[len(l) for l in pair_layers], layers=pair_layers,
                        admissible=admissible, member_semantics='members are pairs of moore-class ids of the same layer')
    hashes['nerode_pair.json'] = dump(out / 'nerode_pair.json', pair_machine)

    summary = dict(
        phase='Finite-state synthesis of triangle disk gadgets',
        grammar='ordered C5 + interior K3 + arbitrary boundary-to-K3 attachments; words of 5 letters over 8 subsets',
        networkx=nx.__version__,
        agreement=agreement,
        disk_states=len(states),
        realized_three_profiles=z5['realized_profiles'],
        t4=dict(state_pairs=len(pairs), ordered_mask_pairs=ordered),
        raw_product_states_per_layer=raw_counts,
        raw_product_states_with_live_geometry_per_layer=live_counts,
        nerode_states_per_layer={name: m['states_per_layer'] for name, m in machines.items()},
        pair_states_per_layer=pair_machine['states_per_layer'],
        pair_admissible=admissible,
        trust=dict(
            color_dfa='exact semantics replayed in Lean (Math/ColorDFA.lean)',
            geometry_dfa='forward direction only: each accepted word carries an explicit rotation system checked by Euler/face traversal; agreement with the apex test is exhaustive observation, not a completeness proof',
            nerode='computationally observed minimal state counts inside this grammar',
            z5='observed profile statistics; not a theorem about arbitrary disk patches'),
        sha256=hashes)
    (out / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'sha256'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
