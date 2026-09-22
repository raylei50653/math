#!/usr/bin/env python3
"""Independent bounded audit of docs/c5_two_rejection_proof_zh.md.

Atlas completeness and disk testing trust NetworkX; this is not a proof for
arbitrary size. --check recomputes and compares the saved deterministic report.
No repository coloring or palette helpers are imported.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_rejection_audit/observations.json'
ROWS = ['01012', '01021', '01023', '01201', '01202', '01203',
        '01212', '01213', '01231', '01232', '00102', '01210']
U = set(range(4))


def lists(attachments, row):
    return [U - {int(row[b]) for b in a} for a in attachments]


def colorable(g, ls):
    assigned = {}
    def visit():
        if len(assigned) == len(g):
            return True
        options = {v: ls[v] - {assigned[w] for w in g[v] if w in assigned}
                   for v in g if v not in assigned}
        v = min(options, key=lambda x: (len(options[x]), x))
        for c in sorted(options[v]):
            assigned[v] = c
            if visit():
                return True
            del assigned[v]
        return False
    return visit()


def peeling(g, ls):
    """Exact elimination of a leaf block, retaining every root color."""
    g, ls = g.copy(), [set(s) for s in ls]
    while len(g) > 1:
        cuts = set(nx.articulation_points(g))
        blocks = list(nx.biconnected_components(g))
        block = next(b for b in blocks if len(b & cuts) <= 1)
        roots = block & cuts
        if not roots:
            return colorable(nx.convert_node_labels_to_integers(g), [ls[v] for v in g])
        root = next(iter(roots))
        vertices = sorted(block)
        local = nx.relabel_nodes(g.subgraph(block), {v: i for i, v in enumerate(vertices)})
        allowed = set()
        for c in ls[root]:
            local_ls = [{c} if v == root else ls[v] for v in vertices]
            if colorable(local, local_ls):
                allowed.add(c)
        ls[root] = allowed
        g.remove_nodes_from(block - {root})
    return bool(ls[next(iter(g))])


def disk(g, attachments):
    k = nx.relabel_nodes(g, {v: v + 5 for v in g})
    k.add_edges_from((b, (b + 1) % 5) for b in range(5))
    k.add_edges_from((v + 5, b) for v, a in enumerate(attachments) for b in a)
    k.add_edges_from((-1, b) for b in range(5))
    return nx.check_planarity(k)[0]


def strip_audit():
    # Independently compare apex planarity with monotone attachment intervals.
    pairs = [(1, 2), (1, 4), (2, 3), (3, 4)]
    counts = [0, 0]
    def check(sets):
        def ordered(seq):
            return all(max(a) <= min(b) for a, b in zip(seq, seq[1:]))
        attachments = [tuple(s) for s in sets]
        attachments[0] = (0,) + attachments[0]
        attachments[-1] = (0,) + attachments[-1]
        assert disk(nx.path_graph(len(sets)), attachments) == (
            ordered(sets) or ordered(sets[::-1]))
    for n in range(2, 6):
        for sets in product(pairs, repeat=n):
            check(sets)
            counts[0] += 1
        for root in range(n):
            for rest in product(pairs, repeat=n-1):
                for union in [(1, 2, 3), (1, 2, 3, 4)]:
                    sets = list(rest)
                    sets.insert(root, union)
                    check(sets)
                    counts[1] += 1
    assert counts == [1360, 3184]
    return counts


def audit():
    counts = [[0, 0, 0] for _ in range(7)]
    witnesses, positive = [], None
    for atlas_id, g in enumerate(nx.graph_atlas_g()):
        n = len(g)
        if n < 2 or not nx.is_connected(g) or max(dict(g.degree()).values()) > 4:
            continue
        blocks = [sorted(b) for b in nx.biconnected_components(g)]
        sizes = []
        for b in blocks:
            h = g.subgraph(b)
            if h.number_of_edges() == len(b) * (len(b) - 1) // 2:
                sizes.append(len(b) - 1)
            elif len(b) % 2 and all(d == 2 for _, d in h.degree()):
                sizes.append(2)
            else:
                break
        if len(sizes) != len(blocks):
            continue
        # Exhaust palettes first, with only the original degree/list constraints.
        seen = set()
        for palettes in product(*(list(combinations(range(4), s)) for s in sizes)):
            ls = [set() for _ in g]
            valid = True
            for b, palette in zip(blocks, palettes):
                for v in b:
                    if ls[v].intersection(palette):
                        valid = False
                    ls[v].update(palette)
            if not valid or any(3 not in s for s in ls) or sum(0 not in s for s in ls) != 2:
                continue
            key = tuple(tuple(sorted(s)) for s in ls)
            if key in seen:
                continue
            seen.add(key)
            choices = [[a for a in combinations(range(5), 4-g.degree(v))
                        if lists([a], ROWS[6])[0] == ls[v]] for v in g]
            for attachments in product(*choices):
                assert sum(0 in a for a in attachments) == 2
                assert not colorable(g, ls)
                counts[n-1][0] += 1
                dl = lists(attachments, ROWS[7])
                accepted = colorable(g, dl)
                assert accepted == peeling(g, dl)
                if accepted:
                    continue
                counts[n-1][1] += 1
                is_disk = disk(g, attachments)
                if is_disk or (n == 4 and positive is None):
                    mask = sum(colorable(g, lists(attachments, row)) << i for i, row in enumerate(ROWS))
                    record = dict(atlas_id=atlas_id, edges=sorted(sorted(e) for e in g.edges()),
                                  attachments=attachments, mask=mask)
                    if is_disk:
                        assert n == 2 and mask == 1855
                        assert sorted(attachments) == [(0, 1, 2), (0, 2, 3)]
                        witnesses.append(record)
                    elif mask == 3903:
                        positive = record
                counts[n-1][2] += is_disk
    assert counts == [[0,0,0],[16,8,2],[0,0,0],[256,64,0],
                      [512,96,0],[4224,552,0],[24576,1920,0]], counts
    assert positive is not None
    return dict(scope='Atlas representatives up to seven internal vertices; finite audit only',
                networkx=nx.__version__, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                rows=ROWS, counts=counts, strip_counts=strip_audit(), disk_witnesses=witnesses,
                nonplanar_3903=positive,
                target_rejections={str(m): [i for i in range(12) if not (m >> i & 1)]
                                   for m in [3647,3703,3895,3901,3903]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = json.loads(json.dumps(audit()))
    if args.check:
        assert report == json.loads(OUT.read_text()), 'saved report differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'counts': report['counts'], 'disk_masks': [w['mask'] for w in report['disk_witnesses']], 'check': args.check}))


if __name__ == '__main__':
    main()
