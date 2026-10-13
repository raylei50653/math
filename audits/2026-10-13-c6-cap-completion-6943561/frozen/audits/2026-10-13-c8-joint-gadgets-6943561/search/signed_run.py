#!/usr/bin/env python3
"""Complete Eq/Diff boundary-chord signatures of the frozen pure caps."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import run

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rows, queries = run.inputs()
    all_results = []
    data_dir = HERE / 'signed_data'
    if not args.check:
        data_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c8-signed-caps-') as scratch:
        tmp = Path(scratch)
        (tmp / 'config').write_text(run.configuration(rows, queries))
        subprocess.run(['g++', '-O3', '-std=c++17', '-o', str(tmp / 'scanner'), str(HERE / 'signed_scan.cpp')], check=True)
        for h in range(6):
            graph = tmp / f'h{h}.ascii'
            graph.write_bytes(gzip.decompress((HERE / f'data/h{h}.ascii.gz').read_bytes()))
            result = tmp / f'h{h}.jsonl'
            counts = tmp / f'h{h}.counts.u16le'
            tuples = tmp / f'h{h}.tuples.u16le'
            signatures = tmp / f'h{h}.signatures.u8'
            subprocess.run([str(tmp / 'scanner'), str(tmp / 'config'), str(graph), str(result), str(counts), str(tuples), str(signatures)], check=True)
            records = [json.loads(line) for line in result.read_text().splitlines()]
            assert records[-1]['kind'] == 'summary'
            record = records[-1]
            record['private_vertices'] = h
            record['minimum_intersections'] = {q['query_id']: value for q, value in zip(queries, record['minimum_intersections'])}
            record['forced_rows'] = {q['query_id']: value for q, value in zip(queries, record['forced_rows'])}
            record['files'] = {}
            for path in (counts, tuples, signatures):
                raw = path.read_bytes()
                name = path.name+'.gz'
                record['files'][name] = {'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest()}
                if args.check or (data_dir / name).exists():
                    assert gzip.decompress((data_dir / name).read_bytes()) == raw
                else:
                    with (data_dir / name).open('xb') as output:
                        output.write(gzip.compress(raw, compresslevel=6, mtime=0))
            all_results.append(record)
            target = HERE / f'signed_h{h}.jsonl'
            if args.check:
                assert target.read_bytes() == result.read_bytes()
            else:
                with target.open('xb') as output:
                    output.write(result.read_bytes())
            print(json.dumps(record), flush=True)
        result = {'schema': 'c8-signed-chord-caps-v1', 'by_private_vertices': all_results,
                  'queries': [q['query_id'] for q in queries],
                  'scope': 'All Eq/Diff assignments to boundary chords of all frozen simple C8 disk triangulations with h<=5. All other edges retain Diff. Equality chords are contracted simultaneously; signatures creating a loop from a C8 edge or Diff chord are rejected. This is a bounded grammar, not all budget-admissible quotient gadgets.',
                  'graphs': sum(r['graphs'] for r in all_results),
                  'valid_signed_graphs': sum(r['valid_signed_graphs'] for r in all_results),
                  'rejections': sum(r['rejections'] for r in all_results),
                  'raw_fibre_encoding': 'signed_data/hN.counts.u16le.gz and hN.tuples.u16le.gz use the pure-cap encoding but ignore all boundary chords. hN.signatures.u8.gz stores one byte per graph and row: bit j=1 exactly when endpoints of lexicographically sorted chord j have equal colors. A signed cap fibre is the raw full fibre if this byte equals its Eq mask, and empty otherwise. All original private edges and spokes retain Diff.',
                  'full_lifts_ignoring_chords': sum(r['full_lifts_ignoring_chords'] for r in all_results),
                  'empty_fibres_ignoring_chords': sum(r['empty_fibres_ignoring_chords'] for r in all_results),
                  'forced_rows': {q['query_id']: sorted(set().union(*(r['forced_rows'][q['query_id']] for r in all_results))) for q in queries},
                  'minimum_intersections': {q['query_id']: min(r['minimum_intersections'][q['query_id']] for r in all_results) for q in queries}}
        target = HERE / 'SIGNED_RESULTS.json'
        if args.check:
            assert json.loads(target.read_text()) == result
        else:
            with target.open('x') as output:
                json.dump(result, output, sort_keys=True, indent=2)
                output.write('\n')
        print(json.dumps({'status': 'PASS', **result}), flush=True)


if __name__ == '__main__':
    main()
