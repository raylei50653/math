#!/usr/bin/env python3
"""Four damaged first records must fail before any end-of-stream check.

The fixtures intentionally contain only header and first graph. Both checkers
must reject the first graph itself; incomplete-coverage failure is forbidden.
"""
import argparse
import copy
import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT/'controls/negative'


def encode(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def fixtures():
    with gzip.open(ROOT/'controls/certificate.jsonl.gz', 'rt') as f:
        header, first = json.loads(next(f)), json.loads(next(f))
    bad = copy.deepcopy(first)
    bad['faces'][-1].reverse()
    yield 'invalid_U_embedding', header, bad
    bad = copy.deepcopy(first)
    size = len(first['parameters']['diamond'])
    shared = [10+size, 11+size]
    assert shared in bad['edges']
    bad['edges'].remove(shared)
    bad['wheel_edges'].remove(shared)
    yield 'omitted_original_diamond_edge', header, bad
    bad = copy.deepcopy(first)
    bad['ownership']['pin_map'][5], bad['ownership']['pin_map'][6] = 6, 5
    yield 'wrong_named_U_pin_map', header, bad
    bad = copy.deepcopy(first)
    removed = False
    for row in bad['rows']:
        for i, cell in enumerate(row['cells']):
            if cell and len(set(cell[0][5:10])) == 3:
                eta = cell.pop()
                centre = next(c for c in '0123' if c not in eta[5:10])
                row['wheel_full_lifts'].remove(eta+centre)
                removed = True
                break
        if removed:
            break
    assert removed
    yield 'omitted_full_A_and_G_lift', header, bad


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.write:
        DEST.mkdir(exist_ok=False)
    outcomes = []
    for name, header, graph in fixtures():
        path = DEST/(name+'.jsonl.gz')
        data = encode(header)+encode(graph)
        if args.write:
            with path.open('xb') as f:
                f.write(gzip.compress(data, mtime=0))
        else:
            assert gzip.decompress(path.read_bytes()) == data
        for who, command in [
            ('primary', [sys.executable, '-B', str(ROOT/'controls/check.py'), '--check', '--certificate', str(path)]),
            ('independent', [sys.executable, '-B', str(ROOT/'independent/check.py'), '--certificate', str(path), '--limit', '1'])]:
            result = subprocess.run(command, capture_output=True, text=True)
            output = result.stdout+result.stderr
            assert result.returncode != 0 and 'AssertionError' in output
            assert 'incomplete template coverage' not in output and 'EOFError' not in output
            if who == 'primary':
                assert 'certificate mismatch: {' in output
            if args.write:
                with (DEST/(name+'-'+who+'.log')).open('x') as f:
                    f.write(output)
            outcomes.append({'control': name, 'checker': who, 'returncode': result.returncode,
                             'status': 'triggered and holds: malformed first graph rejected',
                             'command': command})
    # Interpreter path can vary between checkouts; commands are evidence of
    # this run, not a portable mathematical equality field.
    if args.write:
        with (DEST/'summary.json').open('x') as f:
            json.dump(outcomes, f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        old = json.loads((DEST/'summary.json').read_text())
        assert [(x['control'], x['checker'], x['returncode'], x['status']) for x in outcomes] == [
            (x['control'], x['checker'], x['returncode'], x['status']) for x in old]
    print(json.dumps({'malformed_fixtures': 4, 'rejections': len(outcomes),
                      'status': 'triggered and holds',
                      'Sigma_equal_R3_different': 'counterexample in representatives.json.gz'}, sort_keys=True))


if __name__ == '__main__':
    main()
