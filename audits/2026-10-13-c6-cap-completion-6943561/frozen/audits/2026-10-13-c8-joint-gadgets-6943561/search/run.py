#!/usr/bin/env python3
"""Generate and replay the complete bounded C8 cap search.

The plantri source and documentation are frozen in vendor/ before generation.
All 16 dihedral boundary identifications are checked; they are counted with
duplicates, not advertised as distinct named caps. Stored counts are full
literal extension counts, not existence-only summaries.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parent.parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def norm(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def inputs():
    frozen = AUDIT / 'frozen/audits'
    rows = json.loads((frozen / '2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']
    rows = list(map(tuple, rows))
    all_rows = sorted({norm(p) for p in itertools.product(range(4), repeat=8)
                       if all(p[i] != p[(i+1) % 8] for i in range(8))})
    assert rows == all_rows and len(rows) == 274
    queries = [q for q in json.loads((frozen / '2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    assert len(queries) == 8
    return rows, queries


def configuration(rows, queries):
    row_index = {p: i for i, p in enumerate(rows)}
    values = [' '.join(map(str, row)) for row in rows]
    for query in queries:
        for direction in (1, -1):
            for shift in range(8):
                accept = []
                for row in rows:
                    transformed = [None] * 8
                    for j in range(8):
                        transformed[(shift + direction*j) % 8] = row[j]
                    accept.append((query['support'] >> row_index[norm(transformed)]) & 1)
                values.append(' '.join(map(str, accept)))
    return '\n'.join(values) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rows, queries = inputs()
    data_dir = HERE / 'data'
    if not args.check:
        data_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c8-allcaps-') as scratch:
        tmp = Path(scratch)
        plantri = tmp / 'plantri'
        scanner = tmp / 'scan'
        subprocess.run(['cc', '-O3', '-o', str(plantri), str(HERE / 'vendor/plantri.c')], check=True)
        subprocess.run(['g++', '-O3', '-std=c++17', '-o', str(scanner), str(HERE / 'scan.cpp')], check=True)
        config = configuration(rows, queries)
        (tmp / 'config.txt').write_text(config)
        all_results = []
        for h in range(6):
            graph = tmp / f'h{h}.ascii'
            counts = tmp / f'h{h}.counts.u16le'
            tuples = tmp / f'h{h}.tuples.u16le'
            result = tmp / f'h{h}.json'
            generated = subprocess.run([str(plantri), '-aP8c2m2', str(8+h), str(graph)],
                                       check=True, capture_output=True, text=True)
            subprocess.run([str(scanner), str(tmp / 'config.txt'), str(graph), str(counts), str(result), str(tuples)], check=True)
            record = json.loads(result.read_text())
            record['private_vertices'] = h
            for entry, query in zip(record['queries'], queries):
                entry['query_id'] = query['query_id']
            record['files'] = {}
            for path in (graph, counts, tuples):
                raw = path.read_bytes()
                name = path.name + '.gz'
                record['files'][name] = {'raw_bytes': len(raw), 'raw_sha256': sha(raw)}
                if args.check or (data_dir / name).exists():
                    assert gzip.decompress((data_dir / name).read_bytes()) == raw
                else:
                    with (data_dir / name).open('xb') as output:
                        output.write(gzip.compress(raw, compresslevel=9, mtime=0))
            all_results.append(record)
            print(json.dumps(record), flush=True)
        result = {'schema': 'c8-all-caps-five-private-v1',
                  'generator': 'plantri -aP8c2m2 n for n=8,...,13',
                  'configuration_sha256': sha(config.encode()),
                  'rows': rows,
                  'queries': queries,
                  'transform_convention': 't=0..7: direction=1,shift=t; t=8..15: direction=-1,shift=t-8. Cap boundary j maps to query boundary (shift+direction*j)%8.',
                  'fibre_count_encoding': 'Each generated cap has 274 consecutive unsigned 16-bit little-endian literal complete fibre counts in stored row order; zeros retained. Private vertices ordered by original plantri vertex label after removing the outer cycle.',
                  'full_tuple_encoding': 'hN.tuples.u16le.gz stores all private tuples sequentially in graph order then row order. Consume the number of uint16LE entries specified by each corresponding fibre count. Bits 2*i and 2*i+1 encode private vertex i in the same fixed color frame as the row. Zero-count fibres consume no tuples. The h=0 empty tuple is integer zero. Within each fibre tuple order is DFS order, not lexical.',
                  'by_private_vertices': all_results,
                  'graphs': sum(r['graphs'] for r in all_results),
                  'named_orientations_with_duplicates': 16*sum(r['graphs'] for r in all_results),
                  'newly_excluded': [q['query_id'] for i, q in enumerate(queries)
                                     if any(r['queries'][i]['minimum_intersection'] == 0 for r in all_results)],
                  'minimum_intersections': {q['query_id']: min(r['queries'][i]['minimum_intersection'] for r in all_results)
                                            for i, q in enumerate(queries)},
                  'scope': 'All simple plane disk caps on the named C8 with at most five private vertices, by edge augmentation to disk triangulations. Enumeration completeness depends on frozen plantri generator; every emitted embedding and full extension support is directly checked.',
                  'source_status': 'Eight necessary support bounds only; actual source realizability remains OPEN.',
                  'four_colour_theorem_assumed': False,
                  'new_Lean_theorem': False}
        result = json.loads(json.dumps(result))
        if args.check:
            assert json.loads((HERE / 'RESULTS.json').read_text()) == result
        else:
            with (HERE / 'RESULTS.json').open('w') as output:
                json.dump(result, output, indent=2, sort_keys=True)
                output.write('\n')
        print(json.dumps({'status': 'PASS', 'graphs': result['graphs'],
                          'newly_excluded': result['newly_excluded'],
                          'minimum_intersections': result['minimum_intersections']}), flush=True)


if __name__ == '__main__':
    main()
