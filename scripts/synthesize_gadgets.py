#!/usr/bin/env python3
"""Target-directed synthesis in the complete C5 + one triangle attachment grammar.

All 2^15 attachment sets are considered. D5 positions stay labelled. Two copies
have disjoint interiors. A cofacial test guards one-sided disk admissibility.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

import networkx as nx
from construct_boundary import certificate
from search_boundary import CYCLE, REPS, COLORINGS, normalize


def relation_data(n, edges, state):
    data = certificate(n, edges, tuple(b for i, b in enumerate(REPS) if state >> i & 1))
    data['state_bits'] = state
    data.pop('sha256')
    data['sha256'] = hashlib.sha256(json.dumps(data, sort_keys=True,
                                             separators=(',', ':')).encode()).hexdigest()
    return data


def explain(edges, state):
    neighbors = {v: [u for u, w in edges if u < 5 and w == v] for v in (5, 6, 7)}
    rejections = []
    for i, b in enumerate(REPS):
        if len(set(b)) != 3 or state >> i & 1:
            continue
        allowed = {v: set(range(4)) - {b[u] for u in neighbors[v]} for v in neighbors}
        deficits = [(sub, sorted(set().union(*(allowed[v] for v in sub))))
                    for k in (1, 2, 3) for sub in it.combinations((5, 6, 7), k)
                    if len(set().union(*(allowed[v] for v in sub))) < k]
        assert deficits, 'Every claimed rejection must have a finite pigeonhole explanation'
        sub, colors = deficits[0]
        rejections.append(dict(boundary=b, allowed={v: sorted(a) for v, a in allowed.items()},
                               vertices=sub, available_union=colors,
                               reason='These pairwise adjacent vertices have too few available colors.'))
    return dict(neighbors=neighbors, rejections=rejections,
                accepted_three=[b for i, b in enumerate(REPS) if len(set(b)) == 3 and state >> i & 1])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='artifacts/gadgets')
    a = p.parse_args()
    out = Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    base = tuple(sorted(CYCLE + ((5, 6), (5, 7), (6, 7))))
    attachments = tuple(it.product(range(5), range(5, 8)))
    inside = tuple(it.permutations(range(4), 3))
    assignments = [b + t for b in REPS for t in inside]
    edge_masks = [sum(1 << i for i, c in enumerate(assignments) if c[u] != c[v])
                  for u, v in attachments]
    states = [(1 << len(assignments)) - 1] * (1 << 15)
    library = {}
    counts = dict(attachment_sets=1 << 15, disk_edge_bound=0, disk_graphs=0,
                  distinct_disk_states=0, direct_target=0, state_pairs=0,
                  target_pairs=0, disk_target_representatives=0)
    target = sum(1 << i for i, b in enumerate(REPS) if len(set(b)) == 4)
    for mask in range(1 << 15):
        if mask:
            bit = mask & -mask
            states[mask] = states[mask ^ bit] & edge_masks[bit.bit_length()-1]
        if mask.bit_count() > 8:
            continue  # apex: 9 vertices, at most 21 edges
        counts['disk_edge_bound'] += 1
        edges = tuple(sorted(base + tuple(e for i, e in enumerate(attachments) if mask >> i & 1)))
        apex = nx.Graph()
        apex.add_nodes_from(range(9))
        apex.add_edges_from(edges + tuple((i, 8) for i in range(5)))
        if not nx.check_planarity(apex)[0]:
            continue
        counts['disk_graphs'] += 1
        state = sum(1 << i for i in range(10)
                    if states[mask] >> (24*i) & ((1 << 24)-1))
        counts['direct_target'] += state == target
        old = library.get(state)
        if old is None or (len(edges), edges) < (len(old), old):
            library[state] = edges
    counts['distinct_disk_states'] = len(library)
    # Search inverse image of the exact target, not just arbitrary BAD states.
    successful = []
    for s, t in it.combinations_with_replacement(sorted(library), 2):
        counts['state_pairs'] += 1
        if s & t != target:
            continue
        counts['target_pairs'] += 1
        left, right = library[s], library[t]
        shifted = tuple((u if u < 5 else u+3, v if v < 5 else v+3) for u, v in right)
        union = tuple(sorted(set(left) | set(shifted)))
        # Every successful candidate gets a deterministic complete certificate.
        cert = relation_data(11, union, target)
        counts['disk_target_representatives'] += cert['cofacial_test']
        successful.append((len(union), union, s, t, cert))
    successful.sort(key=lambda item: item[:4])
    witnesses = [relation_data(8, edges, state) for state, edges in sorted(library.items())]
    (out / 'library.jsonl').write_text(''.join(json.dumps(c, sort_keys=True,
        separators=(',', ':'))+'\n' for c in witnesses))
    (out / 'bad_certificates.jsonl').write_text(''.join(json.dumps(item[4], sort_keys=True,
        separators=(',', ':'))+'\n' for item in successful))
    summary = dict(grammar='C5 + one K3 + arbitrary boundary-to-K3 edges; two-copy composition',
                   networkx=nx.__version__, counts=counts, orbit_order=REPS,
                   target_bits=target, target_orbits=[b for b in REPS if len(set(b)) == 4],
                   best=None if not successful else dict(n=11, m=successful[0][0],
                       left_state=successful[0][2], right_state=successful[0][3],
                       sha256=successful[0][4]['sha256']),
                   scope='Cost optimum only inside this finite grammar, not among all graphs.')
    summary['geometry_scope'] = ('Only one minimum-edge witness is retained per exact state. '
        'Disk tests of pair representatives do not cover all physical realizations of each state.')
    if successful:
        s, t = successful[0][2:4]
        explanation = dict(left=explain(library[s], s), right=explain(library[t], t))
        (out/'explanation.json').write_text(json.dumps(explanation, sort_keys=True, indent=2)+'\n')
    (out / 'summary.json').write_text(json.dumps(summary, sort_keys=True, indent=2)+'\n')
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
