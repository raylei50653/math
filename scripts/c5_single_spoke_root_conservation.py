#!/usr/bin/env python3
"""Audit fixed-color palette induction and the two named single-root queries."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_root_conservation/observations.json'
SOURCES = [ROOT / 'artifacts/c5_single_spoke_branch_minor/observations.json',
           ROOT / 'artifacts/c5_single_spoke_completion/observations.json']


def union(parts):
    result = 0
    for part in parts:
        assert not result & part
        result |= part
    return result


def decompositions(limit):
    palettes = [m for m in range(1, 16) if m.bit_count() in (1, 2)]
    for n in range(limit + 1):
        for parts in combinations(palettes, n):
            if sum(m.bit_count() for m in parts) <= limit:
                acc = 0
                for m in parts:
                    if acc & m:
                        break
                    acc |= m
                else:
                    yield from permutations(parts)



def local_audit():
    # At a nonroot vertex: parent palette = list minus child palettes.
    residuals = []
    for listing in range(16):
        for parts in decompositions(4):
            children = union(parts)
            parent = listing & ~children
            if children & ~listing or parent.bit_count() not in (1, 2):
                continue
            residuals.append((listing, parts, parent))
    checks = Counter()
    for left, right in product(residuals, repeat=2):
        lm, lc, lp = left
        rm, rc, rp = right
        if len(lc) != len(rc) or lp.bit_count() != rp.bit_count():
            continue
        if any(a.bit_count() != b.bit_count() for a, b in zip(lc, rc)):
            continue
        for color in range(4):
            bit = 1 << color
            if bool(lm & bit) != bool(rm & bit):
                continue
            if any(bool(a & bit) != bool(b & bit) for a, b in zip(lc, rc)):
                continue
            assert bool(lp & bit) == bool(rp & bit)
            checks[str(color)] += 1
    # Root has internal degree <=3. An empty family covers singleton C too.
    root_checks = Counter()
    for left, right in product(list(decompositions(3)), repeat=2):
        if len(left) != len(right):
            continue
        if any(a.bit_count() != b.bit_count() for a, b in zip(left, right)):
            continue
        for color in range(4):
            bit = 1 << color
            if all(bool(a & bit) == bool(b & bit) for a, b in zip(left, right)):
                assert bool(union(left) & bit) == bool(union(right) & bit)
                root_checks[str(color)] += 1
    # Actual root boundary attachments: retain all subsets of {b0,b1,b2}.
    q, p = (0, 1, 0, 1, 2), (0, 1, 2, 1, 2)
    roots = []
    for n in range(4):
        for support in combinations(range(3), n):
            qm = 15 & ~sum(1 << c for c in {1} | {q[i] for i in support})
            pm = 15 & ~sum(1 << c for c in {3} | {p[i] for i in support})
            assert qm & 8 and not pm & 8
            roots.append(dict(support=support, q_rejected_list=qm,
                              p_rejected_list=pm, internal_degree=3-n,
                              both_tight=qm.bit_count() == pm.bit_count() == 3-n))
    return dict(nonroot_induction_checks=dict(checks),
                root_union_checks=dict(root_checks), root_attachments=roots)


def build():
    prior = json.loads(SOURCES[0].read_text())['table']['records']
    completion = {r['source_index']: r for r in json.loads(SOURCES[1].read_text())['records']}
    records, changed, counts = [], [], Counter()
    for row in prior:
        flags = list(row['accepted_targets'])
        roles = {tuple(b): tuple(s) for b, s in zip(row['bans'], row['supports'])}
        applies = (row['spoke'] == 0 and row['bans'][0] == [3] and
                   roles == {(1,): (0, 1, 2), (2,): (0, 4), (3,): (2, 3, 4)})
        witness = None
        if applies:
            assert flags == [True, False]
            target = completion[row['source_index']]['targets'][1]
            assert target['row'] == [0, 1, 2, 1, 2]
            one = row['bans'].index([1])
            two = row['bans'].index([2])
            assert one != 0 and two != 0  # Only component 0 has two contacts.
            assert target['completion']['component'] == 0
            assert 3 in target['completion']['excluded_original_colors']
            assert any(k['component'] == two and k['forbidden'] == [2]
                       for k in target['known'])
            flags[1] = True
            changed.append(row['source_index'])
            witness = dict(root_component=one, q_forbidden=1,
                           excluded_p2_color=3, guaranteed_z_color=3)
        counts[{(True, True): 'both', (True, False): 'p1_only',
                (False, True): 'p2_only', (False, False): 'neither'}[tuple(flags)]] += 1
        records.append(dict(**{k: v for k, v in row.items() if k != 'accepted_targets'},
                            accepted_targets=flags, root_conservation=witness))
    assert changed == [23, 28]
    assert counts == {'both': 66, 'p1_only': 18, 'p2_only': 30}
    paths = SOURCES + [Path(__file__)]
    return dict(scope='local induction algebra; arbitrary-size proof in report; only named branch updated',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                local=local_audit(), table=dict(records=records, counts=dict(counts), newly_accepted_p2=changed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(dict(local=result['local'], counts=result['table']['counts']), sort_keys=True))


if __name__ == '__main__':
    main()
