#!/usr/bin/env python3
"""Read-only custody and eight-current-U cross-check for C8-TERMINAL-S1."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT / 'frozen'


def frozen_bytes(path):
    storage_file = ROOT / 'STORAGE.json'
    storage = json.loads(storage_file.read_text())['files'] if storage_file.exists() else {}
    if path not in storage:
        return (FROZEN / path).read_bytes()
    item = storage[path]
    assert not (FROZEN / path).exists(), 'ambiguous uncompressed input'
    compressed = (ROOT / item['stored_path']).read_bytes()
    assert len(compressed) == item['stored_bytes']
    assert hashlib.sha256(compressed).hexdigest() == item['stored_sha256']
    data = gzip.decompress(compressed)
    assert len(data) == item['source_bytes']
    assert hashlib.sha256(data).hexdigest() == item['source_sha256']
    return data


def read(path):
    return json.loads(frozen_bytes(path))


def reconstruct():
    manifest = json.loads((ROOT / 'INPUTS.json').read_text())
    for entry in manifest['inputs']:
        data = frozen_bytes(entry['path'])
        assert len(data) == entry['bytes'], ('size', entry['path'])
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], ('hash', entry['path'])
    terminal = FROZEN / 'audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/check.py'
    spec = importlib.util.spec_from_file_location('frozen_terminal_authority', terminal)
    tk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tk)
    repaired = read('audits/2026-10-13-c5-no4ct-c8-6cafdfb/finite/certificate.json')
    current = read('audits/2026-10-13-c8-struct-243a125/kempe/certificate.json')
    old = read('audits/2026-10-13-c8-struct-243a125/classification/quotient.json')
    interface = repaired['interface']
    patterns = interface['pattern_order']
    assert patterns == current['pattern_order'] == old['patterns']
    assert len(patterns) == 274
    assert [''.join(map(str, p)) for p in interface['outer_pattern_order']] == list(tk.B_ROWS)
    rows = []
    for name, extras, target in tk.QUERIES:
        ledger = next(q for q in repaired['query_ledger'] if q['query_id'] == name)
        case = next(c for c in interface['cases'] if c['id'] == ledger['case_id'])
        kernel = next(q for q in current['queries'] if f"{q['case_id']}-{q['target']}" == name)
        legacy = next(q for q in old['queries'] if q['query_id'] == name)
        assert ledger['fixed_split_query'] == kernel
        assert ledger['status'] == 'necessary_condition_residual'
        assert target == ledger['target']
        assert list(extras) == ledger['extras'] == case['extras'] == kernel['extras']
        faces, names = tk.collar_faces(extras)
        assert names == ledger['boundary_order'] == case['boundary_order'] == kernel['boundary_order']
        rename = dict(zip(names, tk.C))
        def mapped(v):
            return rename.get(v, v)
        def edge_set(fs):
            return {tk.edge(mapped(a), mapped(b)) for f in fs
                    for a, b in zip(f, f[1:] + f[:1])}
        assert edge_set(case['annulus_faces']) == edge_set(faces)
        support = kernel['support']
        assert support.bit_count() == ledger['necessary_support_size']
        assert support & ~legacy['final_upper_mask'] == 0
        rows.append(dict(query=name, target=target, extras=list(extras),
                         original_C_names=names, named_C=list(tk.C),
                         U=support, U_size=support.bit_count(),
                         U_rows=[i for i in range(274) if support >> i & 1],
                         historical_quotient_U_size=legacy['final_upper_mask'].bit_count(),
                         annulus_faces=faces))
    return json.loads(json.dumps(dict(schema='c8-terminal-s1-authority-v1',
        base=manifest['base'], input_files=len(manifest['inputs']),
        color_frame=[0, 1, 2, 3], B_rows=tk.B_ROWS, C_patterns=patterns, queries=rows,
        support_scope='necessary upper bounds only; no source realizability',
        no4ct_dependency='frozen no4ct C8 geometry sections 1-6; no unconditional 4CT')))


def verify(value):
    assert value == reconstruct(), 'authority certificate mismatch'
    return dict(status='PASS', frozen_files=value['input_files'],
                queries=len(value['queries']),
                U_sizes={q['query']: q['U_size'] for q in value['queries']})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'AUTHORITY.json'
    if args.write:
        value = reconstruct()
        with path.open('x') as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write('\n')
    value = json.loads(path.read_text())
    result = verify(value)
    if args.negative:
        for kind in ('upper', 'collar', 'target'):
            bad = copy.deepcopy(value)
            if kind == 'upper':
                bad['queries'][3]['U'] ^= 1
            elif kind == 'collar':
                bad['queries'][0]['original_C_names'].reverse()
            else:
                bad['queries'][0]['target'] = 941
            try:
                verify(bad)
            except AssertionError:
                continue
            raise AssertionError(('negative control accepted', kind))
        result['negative_controls_rejected'] = 3
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
