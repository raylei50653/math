#!/usr/bin/env python3
"""Independent whole-domain check of signed-chord face-hub certificates.

Uses recursive base-face decomposition and quotient-graph DFS. Does not import
the producer. Hub identity is 8+j in the stored hub_faces order.
"""
import argparse
import copy
import gzip
import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(e):
    require(len(e) == 2 and e[0] != e[1], 'invalid original edge')
    return tuple(sorted(e))


def face(f):
    require(len(set(f)) == len(f), 'repeated dissection face vertex')
    return tuple(sorted(f))


@lru_cache(None)
def recursive_disks(vertices):
    """Choose the unique face incident with the last-first base edge."""
    if len(vertices) == 2:
        return (((), ()),)
    output = []
    for count in range(1, len(vertices) - 1):
        for selected in itertools.combinations(range(1, len(vertices) - 1), count):
            indices = (0,) + selected + (len(vertices) - 1,)
            base_face = tuple(vertices[i] for i in indices)
            parts = []
            base_chords = []
            for lo, hi in zip(indices, indices[1:]):
                if hi - lo > 1:
                    base_chords.append(edge((vertices[lo], vertices[hi])))
                    parts.append(recursive_disks(vertices[lo:hi + 1]))
            for choices in itertools.product(*parts):
                chords = tuple(sorted(base_chords +
                                      [c for sub, _ in choices for c in sub]))
                faces = tuple(sorted((base_face,) +
                                     tuple(f for _, fs in choices for f in fs)))
                output.append((chords, faces))
    require(len(output) == len(set(output)), 'recursive dissection duplicates')
    return tuple(output)


def blocks_for(equalities):
    # Independent connectivity closure: no producer union-find algorithm.
    adjacency = [set() for _ in range(8)]
    for a, b in equalities:
        adjacency[a].add(b)
        adjacency[b].add(a)
    blocks = []
    unseen = set(range(8))
    while unseen:
        todo = [min(unseen)]
        component = set()
        while todo:
            v = todo.pop()
            if v in component:
                continue
            component.add(v)
            todo.extend(adjacency[v] - component)
        unseen -= component
        blocks.append(tuple(sorted(component)))
    return tuple(sorted(blocks))


def make_domain():
    domain = {}
    total = 0
    loops = 0
    histogram = Counter()
    dissections = recursive_disks(tuple(range(8)))
    require(len(dissections) == 903, 'unexpected independent dissection count')
    cycle = [edge((v, (v + 1) % 8)) for v in range(8)]
    for chords, faces in dissections:
        eligible = [f for f in faces if len(f) >= 4]
        for chosen in itertools.product((False, True), repeat=len(chords)):
            eq = tuple(c for c, flag in zip(chords, chosen) if flag)
            diff = tuple(c for c, flag in zip(chords, chosen) if not flag)
            blocks = blocks_for(eq)
            index = {v: i for i, b in enumerate(blocks) for v in b}
            loop = any(index[a] == index[b] for a, b in cycle + list(diff))
            for chosen_hubs in itertools.product((False, True), repeat=len(eligible)):
                hubs = tuple(f for f, flag in zip(eligible, chosen_hubs) if flag)
                total += 1
                if loop:
                    loops += 1
                    continue
                key = (eq, diff, hubs)
                require(key not in domain, 'duplicate independent gadget')
                domain[key] = (chords, faces, blocks)
                histogram[(len(hubs), 8 - len(blocks))] += 1
    return domain, {'total': total, 'valid': len(domain),
                    'invalid_inequality_loop': loops,
                    'histogram': {f'h{h}-d{d}': n
                                  for (h, d), n in sorted(histogram.items())}}


def quotient_fibres(entry, rows, domain, full=True):
    require(entry['boundary_order'] == list(range(8)), 'original boundary names changed')
    chords = tuple(sorted(edge(e) for e in entry['chords']))
    eq = tuple(sorted(edge(e) for e in entry['equality_chords']))
    diff = tuple(sorted(edge(e) for e in entry['inequality_chords']))
    require(not set(eq) & set(diff), 'edge simultaneously equality and inequality')
    require(tuple(sorted(eq + diff)) == chords, 'signed chords do not partition chords')
    trial_blocks = blocks_for(eq)
    trial_index = {v: i for i, b in enumerate(trial_blocks) for v in b}
    require(all(trial_index[a] != trial_index[b]
                for a, b in [(v, (v + 1) % 8) for v in range(8)] + list(diff)),
            'original inequality becomes quotient loop')
    hubs_in_order = [face(f) for f in entry['hub_faces']]
    key = (eq, diff, tuple(sorted(hubs_in_order)))
    require(key in domain, 'invalid, loop-producing or missing grammar member')
    expect_chords, expect_faces, blocks = domain[key]
    require(chords == expect_chords, 'chord mismatch')
    require(tuple(sorted(face(f) for f in entry['dissection_faces'])) == expect_faces,
            'original dissection faces changed')
    require(entry['identification_reduction'] == 8 - len(blocks), 'wrong reduction')
    require(entry['added_vertices'] == len(hubs_in_order), 'wrong private point budget')
    require(len(hubs_in_order) - (8 - len(blocks)) <= 5, 'budget exceeded')
    if not full:
        return key
    block_index = {v: i for i, b in enumerate(blocks) for v in b}
    q = len(blocks)
    n = q + len(hubs_in_order)
    graph_edges = set()
    for a, b in [(v, (v + 1) % 8) for v in range(8)] + list(diff):
        a, b = block_index[a], block_index[b]
        require(a != b, 'inequality becomes loop')
        graph_edges.add(tuple(sorted((a, b))))
    for j, f in enumerate(hubs_in_order):
        for v in f:
            graph_edges.add(tuple(sorted((q + j, block_index[v]))))
    adjacency = [set() for _ in range(n)]
    for a, b in graph_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    fibres = []
    for p in rows:
        values = [-1] * n
        valid = True
        for v, color in enumerate(p):
            a = block_index[v]
            if values[a] != -1 and values[a] != color:
                valid = False
                break
            values[a] = color
        if valid:
            valid = all(values[a] == -1 or values[b] == -1 or values[a] != values[b]
                        for a, b in graph_edges)
        lifts = []
        if valid:
            def visit(v):
                if v == n:
                    lifts.append(values[q:].copy())
                    return
                forbidden = {values[w] for w in adjacency[v] if values[w] >= 0}
                for color in range(4):
                    if color not in forbidden:
                        values[v] = color
                        visit(v + 1)
                values[v] = -1
            visit(q)
        fibres.append(lifts)
    require(fibres == entry['full_hub_lifts_by_literal_row'],
            'full quotient graph DFS fibres mismatch')
    relation = sum(1 << i for i, lifts in enumerate(fibres) if lifts)
    require(relation == entry['relation'], 'relation mismatch')
    return key, relation, sum(len(x) for x in fibres), sum(not x for x in fibres)


def run(negative=False):
    path = ROOT / 'quotients/certificate.v2.json.gz'
    raw = path.read_bytes()
    certificate = json.loads(gzip.decompress(raw))
    interface = json.loads((ROOT / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())
    rows = interface['pattern_order']
    require(certificate['boundary_rows'] == rows, 'literal row order mismatch')
    queries = [q for q in json.loads((ROOT / 'frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    domain, summary = make_domain()
    entries = certificate.get('entries', certificate.get('gadgets'))
    require(entries is not None, 'missing full gadget entries')
    require(len(entries) == len(domain), 'gadget domain size mismatch')
    seen = set()
    relations = set()
    minima = {q['query_id']: 275 for q in queries}
    lifts = empty = 0
    for i, entry in enumerate(entries):
        require(entry['id'] == i, 'wrong entry identity')
        key, relation, count, zeros = quotient_fibres(entry, rows, domain)
        require(key not in seen, 'repeated named gadget')
        seen.add(key)
        relations.add(relation)
        lifts += count
        empty += zeros
        for query in queries:
            qid = query['query_id']
            minima[qid] = min(minima[qid], (relation & query['support']).bit_count())
    require(seen == set(domain), 'independent grammar not fully represented')
    summary.update(distinct_relations=len(relations), minimum_intersections=minima,
                   newly_excluded=[k for k, v in minima.items() if v == 0])
    for key, value in summary.items():
        require(certificate['summary'][key] == value, 'summary mismatch: ' + key)
    require(set(certificate['witnesses']) == set(minima), 'missing minimum witness')
    for query in queries:
        qid = query['query_id']
        witness = certificate['witnesses'][qid]
        require(0 <= witness['gadget_id'] < len(entries), 'invalid minimum witness ID')
        rel = entries[witness['gadget_id']]['relation']
        indices = [i for i in range(len(rows)) if rel & query['support'] & (1 << i)]
        require(indices == witness['intersection_rows'], 'wrong minimum intersection rows')
        require(len(indices) == minima[qid], 'witness does not attain minimum')
    controls = {}
    if negative:
        zero = copy.deepcopy(entries[0])
        zero['boundary_order'][0], zero['boundary_order'][1] = 1, 0
        loop = copy.deepcopy(entries[0])
        loop['chords'] = [[0, 2], [0, 3]]
        loop['equality_chords'] = [[0, 2], [0, 3]]
        loop['inequality_chords'] = []
        fibre = copy.deepcopy(entries[0])
        fibre['full_hub_lifts_by_literal_row'][0] = [[9]]
        for name, mutated in [('original_name', zero), ('inequality_loop', loop),
                              ('literal_fibre', fibre)]:
            try:
                quotient_fibres(mutated, rows, domain)
            except ValueError as exc:
                controls[name] = {'rejected': True, 'reason': str(exc)}
            else:
                raise AssertionError('negative control not rejected: ' + name)
    return {'status': 'PASS', 'method': 'recursive base-face domain plus quotient-graph DFS',
            'certificate_sha256': hashlib.sha256(raw).hexdigest(),
            'row_cells': len(entries) * len(rows), 'empty_fibres': empty,
            'full_lifts': lifts, 'summary': summary, 'negative_controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = run(args.negative)
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
