#!/usr/bin/env python3
"""Independent local interface calibration; no source-realization claim."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
COL = frozenset(range(4))


def subsets(items):
    items = sorted(items)
    for bits in range(1 << len(items)):
        yield frozenset(c for i, c in enumerate(items) if bits & (1 << i))


def original_r_rule(v, w, p, q, m, z):
    """Direct ABAB/ABCB R palette rule, without XOR."""
    r, = COL - {m, v, w}
    if z == r:
        return {p, q} == COL - {z, m}
    missing, = COL - {z, m, r}
    return frozenset((p, q)) in (
        frozenset((r, missing)), frozenset((m, missing))
    )


def compute():
    local = collections.Counter()
    for v, w, p, q, m, z in itertools.product(range(4), repeat=6):
        if len({m, v, w}) != 3 or len({z, p, q}) != 3 or m == z:
            continue
        direct = original_r_rule(v, w, p, q, m, z)
        e, f, g = v ^ w, p ^ q, m ^ z
        assert direct == ((e == f) == (e == g))
        local['proper_rows'] += 1
        local['allowed' if direct else ('E1' if e == f else 'E2')] += 1
    assert dict(local) == {'proper_rows': 432, 'allowed': 240, 'E2': 96, 'E1': 96}

    counts = collections.Counter()
    witnesses = {}
    digest = hashlib.sha256()
    full_relation = []
    for v, w, p, q, alpha, beta in itertools.product(range(4), repeat=6):
        if v == w or p == q:
            continue
        for am in subsets(COL - {v, w, alpha, beta}):
            for az in subsets(COL - {p, q, alpha, beta}):
                lifts = sorted((a, b) for a in am for b in az if a != b)
                diffs = {a ^ b for a, b in lifts}
                e, f = v ^ w, p ^ q
                criterion = diffs <= {e} if e == f else e not in diffs
                direct = [original_r_rule(v, w, p, q, a, b) for a, b in lifts]
                assert criterion == all(direct)
                counts['interface_rows'] += 1
                counts['lifts'] += len(lifts)
                counts['empty_fibres'] += not lifts
                counts['violating_fibres'] += not criterion
                counts['violating_lifts'] += direct.count(False)
                record = [v, w, p, q, alpha, beta, sorted(am), sorted(az), lifts, direct]
                full_relation.append(record)
                digest.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
                if not criterion:
                    key = f'{len(am)},{len(az)}'
                    witnesses.setdefault(key, record)
                if len(am) == len(az) == 2 and am != az:
                    assert len(lifts) == 3 and not criterion
    assert {'1,1', '1,2', '2,1', '2,2'} <= set(witnesses)

    # The distinguished role of e blocks an unsupported symmetric linkage.
    # A,B,C,D=0,1,2,3. Start m=B,z=A,v=p=C,w=q=D.
    initial = (2, 3, 2, 3, 1, 0)
    separate_v_switch = (0, 3, 2, 3, 1, 0)
    assert original_r_rule(*initial)
    assert original_r_rule(*separate_v_switch)
    payload = {
        'scope': 'local algebra only; original source existence not triggered',
        'local_rows': dict(sorted(local.items())),
        'complete_interface': dict(sorted(counts.items())),
        'ordered_full_relation_sha256': digest.hexdigest(),
        'violating_fibres_by_missing_set_sizes': witnesses,
        'rejected_symmetric_linkage_control': {
            'order': ['v', 'w', 'p', 'q', 'm', 'z'],
            'initial': initial,
            'separate_v_switch': separate_v_switch,
            'both_satisfy_full_all_r': True,
        },
    }
    return payload, full_relation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    payload, full_relation = compute()
    relation_path = ROOT / 'complete-interface.json.gz'
    relation_data = json.dumps(full_relation, separators=(',', ':')).encode()
    if args.check:
        assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(payload))
        assert gzip.decompress(relation_path.read_bytes()) == relation_data
    else:
        for output_path in (args.certificate, relation_path):
            if output_path.exists():
                raise FileExistsError(f'refusing existing audit output: {output_path}')
        with args.certificate.open('x') as stream:
            stream.write(json.dumps(payload, indent=2, sort_keys=True) + '\n')
        with relation_path.open('xb') as stream:
            stream.write(gzip.compress(relation_data, mtime=0))
    print(json.dumps({'result': 'PASS', **payload['local_rows'], **payload['complete_interface']}, sort_keys=True))


if __name__ == '__main__':
    main()
