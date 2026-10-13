#!/usr/bin/env python3
"""Read-only independent parser/topology and propagated-domain full-lift replay.

Uses the frozen K13 independent implementation, not the new primary checker.
The predecessor's dimension-specific entrypoint and pruning are never called.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = parser.parse_args()
    source = HERE / 'frozen/audits/2026-10-13-k13-collar-50d5474/independent/check.py'
    base = json.loads((HERE / 'BASE.json').read_text())
    for name, digest in base['sha256'].items():
        assert hashlib.sha256((HERE / 'frozen' / name).read_bytes()).hexdigest() == digest, name
    spec = importlib.util.spec_from_file_location('prior_independent', source)
    impl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(impl)
    data = json.loads(gzip.decompress(args.certificate.read_bytes()))
    spheres = impl.planar_code(HERE / 'generation/spheres20.pc')
    assert len(spheres) == data['summary']['spheres']
    records = {(r['sphere'], r['root']): r for r in data['records']}
    assert len(records) == len(data['records']), 'duplicate record'
    visited = set()
    total = 0
    hist = Counter()
    masks = Counter()
    known = set(map(int, json.loads((HERE / 'frozen/artifacts/c5_cells/cells.json').read_text())['cells']))
    for sid, sphere in enumerate(spheres):
        fs = impl.faces(sphere)
        assert len(sphere) == 20 and len(impl.edges(sphere)) == 54
        assert len(fs) == 36 and all(len(f) == 3 for f in fs)
        assert min(map(len, sphere.values())) >= 5
        for z, B in sphere.items():
            if len(B) != 5:
                continue
            record = records[(sid, z)]
            visited.add((sid, z))
            adj = {u: [v for v in ns if v != z] for u, ns in sphere.items() if u != z}
            faces = impl.faces(adj)
            outer = [f for f in faces if len(f) != 3]
            assert len(adj) == 19 and len(impl.edges(adj)) == 49
            assert len(outer) == 1 and impl.cycle_key(B[::-1]) == impl.cycle_key(outer[0])
            mapping = B + sorted(set(adj) - set(B))
            inverse = {v: i for i, v in enumerate(mapping)}
            assert mapping == record['canonical_to_original']
            assert [[inverse[v] for v in adj[u]] for u in mapping] == record['rotation']
            assert sorted(sorted((inverse[u], inverse[v])) for u, v in impl.edges(adj)) == record['edges']
            converted_faces = sorted(list(impl.cycle_key([inverse[v] for v in f])) for f in faces)
            assert converted_faces == record['faces']
            assert [len(adj[u]) for u in mapping] == record['degree']
            h = sum(len(adj[b]) - 4 for b in B)
            assert h == record['h']
            hist[h] += 1
            original_order = sorted(adj)
            positions = {v: i for i, v in enumerate(original_order)}
            rs = []
            for word, saved in zip(impl.WORDS, record['rows'], strict=True):
                full, _ = impl.colourings(adj, B, word)
                canonical = sorted(''.join(f[positions[v]] for v in mapping) for f in full)
                assert saved == {'pattern': word, 'count': len(full), 'lifts': canonical}, (sid, z, word)
                rs.append({'count': len(full)})
                total += len(full)
            mask = sum(1 << i for i, row in enumerate(rs) if row['count'])
            assert mask == record['mask'] and mask in known
            masks[mask] += 1
            f2 = impl.d5_relation(B, rs)
            assert len(record['frames']) == 10
            for actual, saved in zip(f2, record['frames'], strict=True):
                assert actual['B'] == saved['canonical_to_original'][:5]
                assert actual['counts'] == saved['counts'] and actual['mask'] == saved['mask']
    assert visited == set(records), 'omitted or spurious root'
    assert data['summary']['rooted_disks'] == len(visited)
    assert data['summary']['full_lifts'] == total
    assert data['summary']['literal_rows'] == len(visited) * 10
    assert data['summary']['h_histogram'] == {str(k): v for k, v in sorted(hist.items())}
    assert data['summary']['mask_histogram'] == {str(k): v for k, v in sorted(masks.items())}
    print(json.dumps(dict(spheres=len(spheres), roots=len(visited), literal_rows=10*len(visited),
                          complete_lifts_compared=total, all_masks=dict(masks)), sort_keys=True))
    print('PASS independent original-label propagated-domain replay')


if __name__ == '__main__':
    main()
