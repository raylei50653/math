#!/usr/bin/env python3
"""Independent replay of artifacts/automata without importing the generator.

Checks, per word: brute-force Sigma bits against the ColorDFA output, and the
apex-planarity test against GeometryDFA acceptance. Per accepted word: the
stored rotation system is a valid NetworkX planar embedding of the right edge
set, its face count satisfies Euler's formula per component, and C5 is a face.
Nerode partitions are recomputed from suffix signatures. Pair counts, Z5
profile statistics and file hashes are recomputed from words.jsonl alone.

Run: uv run --with networkx==3.5 python scripts/check_automata.py
"""
import hashlib
import itertools as it
import json
from collections import Counter
from pathlib import Path

import networkx as nx
from search_boundary import CYCLE, REPS

ROOT = Path('artifacts/automata')
INNER = (5, 6, 7)
BASE = sorted(CYCLE + ((5, 6), (5, 7), (6, 7)))
THREE = [j for j, b in enumerate(REPS) if len(set(b)) == 3]
T3 = sum(1 << j for j in THREE)
T4 = 1023 & ~T3


def load_lines(name):
    return [json.loads(l) for l in (ROOT / name).read_text().splitlines()]


def sigma_bits(edges):
    bits = 0
    for j, b in enumerate(REPS):
        for t in it.product(range(4), repeat=3):
            c = b + t
            if all(c[u] != c[v] for u, v in edges):
                bits |= 1 << j
                break
    return bits


def unique_position(b):
    return next(i for i in range(5) if b.count(b[i]) == 1)


def hall_rejected(att, b):
    """Closed colour semantics (Math/HallTriangle.lean): pair pinned to the free colour, or
    all three interior vertices restricted to two colours."""
    free = next(c for c in range(4) if c not in b)
    avail = [{free} | ({0, 1, 2, 3} - {free} - {b[i] for i, v in att if v == 5 + k}) for k in range(3)]
    pinned = sum(1 for a in avail if a == {free}) >= 2
    restricted = any(all(a <= {free, x} for a in avail) for x in range(4) if x != free)
    return pinned or restricted


def check_words():
    words = load_lines('words.jsonl')
    assert [w['mask'] for w in words] == list(range(1 << 15))
    accept = {}
    for w in words:
        m = w['mask']
        att = [(i, v) for i in range(5) for v in INNER if m >> (3 * i + v - 5) & 1]
        for j in THREE:
            assert hall_rejected(att, REPS[j]) == (not w['sigma_bits'] >> j & 1), ('hall', m, j)
        assert w['attachments'] == [list(e) for e in att]
        assert w['letters'] == [m >> (3 * i) & 7 for i in range(5)]
        bits = sigma_bits(BASE + att)
        assert w['sigma_bits'] == bits == w['sigma_bits_bruteforce'], m
        assert w['three_profile'] == ''.join('1' if bits >> j & 1 else '0' for j in THREE)
        apex = False
        if len(att) <= 8:
            g = nx.Graph()
            g.add_nodes_from(range(9))
            g.add_edges_from(BASE + att + [(i, 8) for i in range(5)])
            apex = bool(nx.check_planarity(g)[0])
        assert w['apex_planar'] == apex, m
        assert w['geometry_accept'] == apex, ('geometry/apex disagreement', m)
        accept[m] = apex
    return words, accept


def check_embeddings(words, accept):
    rows = load_lines('disk_embeddings.jsonl')
    assert [r['mask'] for r in rows] == [m for m in range(1 << 15) if accept[m]]
    cycle = {(i, (i + 1) % 5) for i in range(5)}
    for r in rows:
        m = r['mask']
        att = [(i, v) for i in range(5) for v in INNER if m >> (3 * i + v - 5) & 1]
        edges = sorted(BASE + att)
        assert r['edges'] == [list(e) for e in edges]
        assert sorted(map(tuple, r['winding_sequence'])) == sorted(att)
        emb = nx.PlanarEmbedding()
        emb.set_data({u: ring for u, ring in enumerate(r['rotation'])})
        emb.check_structure()  # raises unless every component is a valid planar rotation system
        assert {tuple(sorted(e)) for e in emb.edges()} == set(edges)
        seen, faces = set(), []
        for u, ring in enumerate(r['rotation']):
            for v in ring:
                if (u, v) not in seen:
                    faces.append(emb.traverse_face(u, v, seen))
        comps = nx.number_connected_components(nx.Graph(edges))
        assert r['components'] == comps
        assert r['face_count'] == len(faces) == len(r['faces'])
        assert 8 - len(edges) + len(faces) == 2 * comps, m
        darts = [{(f[k], f[(k + 1) % len(f)]) for k in range(len(f))} for f in faces]
        assert any(d == cycle or d == {(v, u) for u, v in cycle} for d in darts), ('C5 not a face', m)
        # the generator orients faces the other way round; NetworkX reads rotations clockwise
        stored = [{(v, u) for u, v in map(tuple, f)} for f in r['faces']]
        assert sorted(map(sorted, stored)) == sorted(map(sorted, darts))
    return rows


def check_states(words, accept):
    data = json.loads((ROOT / 'disk_states.json').read_text())
    groups = {}
    for w in words:
        if accept[w['mask']]:
            groups.setdefault(w['sigma_bits'], []).append(w['mask'])
    assert data['count'] == len(groups) == len(data['states'])
    for s in data['states']:
        bits = s['state_bits']
        assert s['masks'] == groups[bits] and s['mask_count'] == len(groups[bits])
        assert s['three_profile'] == ''.join('1' if bits >> j & 1 else '0' for j in THREE)
        assert s['z5_positions'] == sorted(unique_position(REPS[j]) for j in THREE if bits >> j & 1)
        assert s['full_four_colour'] == ((bits & T4) == T4)
        best = min(groups[bits], key=lambda m: (m.bit_count(), m))
        assert s['min_edge_witness']['mask'] == best
    counts = {bits: len(ms) for bits, ms in groups.items()}
    pairs = json.loads((ROOT / 't4_pairs.json').read_text())
    expected = [(s, t) for s, t in it.combinations_with_replacement(sorted(counts), 2) if s & t == T4]
    assert [(p['left_state'], p['right_state']) for p in pairs['pairs']] == expected
    ordered = sum(counts[s] * counts[t] * (1 if s == t else 2) for s, t in expected)
    assert pairs['state_pairs'] == len(expected) and pairs['ordered_mask_pairs'] == ordered
    z5 = json.loads((ROOT / 'z5_profiles.json').read_text())
    profile_states = Counter(s['three_profile'] for s in data['states'])
    profile_masks = Counter()
    for s in data['states']:
        profile_masks[s['three_profile']] += s['mask_count']
    assert len(z5['profiles']) == 32
    for p in z5['profiles']:
        assert p['realized'] == (profile_states[p['profile']] > 0)
        assert p['disk_state_count'] == profile_states[p['profile']]
        assert p['disk_mask_count'] == profile_masks[p['profile']]
        pos = [unique_position(REPS[THREE[k]]) for k in range(5) if p['profile'][k] == '1']
        assert p['z5_positions'] == sorted(pos) and p['size'] == len(pos)
        assert p['adjacent_pair'] == (len(pos) == 2 and (max(pos) - min(pos)) in (1, 4))
    assert z5['realized_profiles'] == sum(1 for c in profile_states.values() if c)
    assert not z5['empty_realized'] and not z5['singleton_realized']
    assert z5['all_realized_pairs_adjacent'] and z5['all_adjacent_pairs_realized']
    return counts


def check_nerode(words, accept):
    bits = {w['mask']: w['sigma_bits'] for w in words}

    def mask_of(pre):
        return sum(l << (3 * i) for i, l in enumerate(pre))
    outputs = dict(
        geometry=lambda m: accept[m],
        color=lambda m: bits[m],
        moore=lambda m: (True, bits[m]) if accept[m] else None,
        three_colour=lambda m: (bits[m] & T3) if accept[m] else None,
        single_bad=lambda m: accept[m] and bits[m] & T3 == 0)
    result = {}
    for name, f in outputs.items():
        machine = json.loads((ROOT / f'nerode_{name}.json').read_text())
        sizes = []
        for i in range(6):
            classes = {}
            for idx, pre in enumerate(it.product(range(8), repeat=i)):
                sig = tuple(f(mask_of(pre + suf)) for suf in it.product(range(8), repeat=5 - i))
                classes.setdefault(sig, set()).add(machine['prefix_classes'][i][idx])
            sizes.append(len(classes))
            # the stored partition must be exactly the Nerode partition
            assert all(len(v) == 1 for v in classes.values()), (name, i)
            assert len({next(iter(v)) for v in classes.values()}) == len(classes)
            assert len(machine['layers'][i]) == len(classes)
        assert machine['states_per_layer'] == sizes
        for layer in machine['layers'][:5]:
            for c in layer:
                if 'raw_states' in c:
                    assert c['raw_states_merged'] == len(c['raw_states']) <= c['prefixes']
                    assert c['raw_state_of_representative'] in c['raw_states']
        for i in range(5):
            for c in machine['layers'][i]:
                pre = tuple(c['representative'])
                idx = sum(l * 8 ** (i - 1 - j) for j, l in enumerate(pre))
                assert machine['prefix_classes'][i][idx] == c['id']
                for l in range(8):
                    nxt = machine['prefix_classes'][i + 1][idx * 8 + l]
                    assert c['transitions'][l] == nxt
        result[name] = sizes
    return result


def check_pair(counts):
    moore = json.loads((ROOT / 'nerode_moore.json').read_text())
    pair = json.loads((ROOT / 'nerode_pair.json').read_text())
    final = {c['id']: c['output'] for c in moore['layers'][5]}
    trans = [{c['id']: c['transitions'] for c in layer} for layer in moore['layers'][:5]]
    accept_final = {c['id'] for c in pair['layers'][5] if c['accept']}
    member_class = [{tuple(p): c['id'] for c in layer for p in c['members']} for layer in pair['layers']]
    for c in pair['layers'][5]:
        for a, b in c['members']:
            x, y = final[a], final[b]
            assert c['accept'] == (x is not None and y is not None and (x[1] & y[1]) == T4)
    for i in range(5):
        for c in pair['layers'][i]:
            for a, b in c['members']:
                for l1 in range(8):
                    for l2 in range(8):
                        assert c['transitions'][8 * l1 + l2] == member_class[i + 1][(trans[i][a][l1], trans[i][b][l2])]
    live = [set() for _ in range(6)]
    live[5] = accept_final
    for i in range(4, -1, -1):
        live[i] = {c['id'] for c in pair['layers'][i] if any(t in live[i + 1] for t in c['transitions'])}
        for c in pair['layers'][i]:
            assert c['live'] == (c['id'] in live[i])
            expected = [[k // 8, k % 8] for k, t in enumerate(c['transitions']) if c['live'] and t in live[i + 1]]
            assert c['admissible_letter_pairs'] == expected
    assert pair['states_per_layer'] == [len(l) for l in pair['layers']]
    # every layer must be a genuine quotient: distinct classes have distinct behaviour
    for i in range(5):
        rows = [tuple(c['transitions']) for c in pair['layers'][i]]
        assert len(set(rows)) == len(rows)


def main():
    summary = json.loads((ROOT / 'summary.json').read_text())
    for name, digest in summary['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    words, accept = check_words()
    rows = check_embeddings(words, accept)
    counts = check_states(words, accept)
    sizes = check_nerode(words, accept)
    check_pair(counts)
    assert summary['agreement']['geometry_accept'] == summary['agreement']['apex_planar'] == len(rows)
    assert summary['nerode_states_per_layer'] == sizes
    assert summary['disk_states'] == len(counts)
    print(json.dumps(dict(words=len(words), disk=len(rows), states=len(counts), nerode=sizes,
                          t4_ordered_pairs=summary['t4']['ordered_mask_pairs']), sort_keys=True))


if __name__ == '__main__':
    main()
