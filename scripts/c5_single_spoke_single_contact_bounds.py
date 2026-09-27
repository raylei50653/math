#!/usr/bin/env python3
"""Classify the 16 remaining queries by single-root attachment conservation.

Arbitrary-size coverage is the block-tree argument in the companion report.
Root subsets below are necessary local cases, not realizable source graphs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_single_spoke_cores import Q, PI, RHO
from c5_single_spoke_root_conservation import local_audit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_contact_bounds/observations.json'
SWEEP = ROOT / 'artifacts/c5_single_spoke_root_sweep/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_single_contact_bounds/observations.json'
U = set(range(4))


def root_cases(support, p):
    cases = []
    for n in range(len(support) + 1):
        for attachment in combinations(support, n):
            degree = 3 - n  # one actual z edge; full degree four
            qcolors = {Q[i] for i in attachment}
            pcolors = {p[i] for i in attachment}
            if degree < 0:
                reason = 'exceeds_root_degree'
            elif degree == 0:
                # Connected C would be {r}, so its actual support would be A.
                assert set(attachment) != set(support)
                reason = 'isolated_root_cannot_supply_full_actual_support'
            elif len(qcolors) != n:
                reason = 'q_slack'
            else:
                reason = 'target_slack' if len(pcolors) != n else 'tight_root_candidate'
            comparisons = []
            if reason in ('target_slack', 'tight_root_candidate'):
                mq = U - qcolors - {3}
                assert len(mq) == degree and 3 not in mq
                for d in range(4):
                    mp = U - pcolors - {d}
                    tight = len(mp) == degree
                    conserved = (3 in mq) == (3 in mp)
                    if tight and conserved:
                        assert d == 3
                    comparisons.append(dict(target_z=d, q_list=sorted(mq), target_list=sorted(mp),
                                            tight=tight, unused_color_conserved=conserved,
                                            survives=tight and conserved))
                if reason == 'target_slack':
                    assert not any(c['survives'] for c in comparisons)
            cases.append(dict(actual_root_attachments=attachment, internal_degree=degree,
                              classification=reason, comparisons=comparisons,
                              incident_block_sizes={1: [[1]], 2: [[1, 1], [2]],
                                                    3: [[1, 1, 1], [1, 2]]}.get(degree, [])))
    assert len(cases) == 16
    assert Counter(c['classification'] for c in cases) == {
        'tight_root_candidate': 9, 'target_slack': 1, 'q_slack': 1,
        'isolated_root_cannot_supply_full_actual_support': 4, 'exceeds_root_degree': 1}
    return cases


def build():
    source = json.loads(SOURCE.read_text())
    sweep = json.loads(SWEEP.read_text())
    lookup = {r['source_index']: r for r in sweep['records']}
    flags = {i: [e['accept'] for e in r['targets']] for i, r in lookup.items()}
    for r in source['records']:
        flags[r['source_index']][('p1', 'p2').index(r['target'])] = True
    records, frames = [], {}
    for query in source['open_queries']:
        r = lookup[query['source_index']]
        t = ('p1', 'p2').index(query['target'])
        e = r['targets'][t]
        assert not flags[r['source_index']][t]
        bound, = e['bounds']; j = bound['component']
        assert j in (1, 2) and r['bans'][j] == [3]
        support, p = r['supports'][j], e['row']
        assert 3 not in {Q[i] for i in support} | {p[i] for i in support}
        assert len(support) == 4
        known = set().union(*(set(k['forbidden']) for k in e['known']))
        required = U - {p[r['spoke']]} - known
        assert required == ({2, 3} if t == 0 else {0, 3})
        upper = {3}  # conservation at the unique root, for any putative ban
        witness = sorted(required - upper)
        assert witness == ([2] if t == 0 else [0])
        key = ''.join(map(str, support)) + '/' + ''.join(map(str, p))
        if key not in frames:
            frames[key] = root_cases(support, p)
        # Independent finite audit of nonempty unary relations and capacity.
        relation_options = []
        for mask in range(1, 16):
            relation = [c for c in range(4) if mask >> c & 1]
            forbidden = set(relation) if len(relation) == 1 else set()
            assert len(forbidden) <= 1 and not required <= forbidden
            if forbidden <= upper:
                assert all(any(c != z for c in relation) for z in witness)
                relation_options.append([[c] for c in relation])
        assert len(relation_options) == 12
        records.append(dict(**query, inherited_record=r, unknown_component=j,
                            root=f'r{j}', root_attachment_frame=key,
                            forbidden_upper_bound=[3], required_if_rejected=sorted(required),
                            guaranteed_z_colors=witness, possible_unary_relations=relation_options,
                            relation_scope='necessary possibilities only, not a realizability claim',
                            reflection=dict(actual_target_row=[PI[p[RHO[i]]] for i in range(5)],
                                            guaranteed_z_colors=[PI[c] for c in witness],
                                            meaning='existing whole-relation transport only'),
                            accepted=True))
        flags[r['source_index']][t] = True
    assert len(records) == 16 and len(frames) == 2
    assert Counter(r['target'] for r in records) == {'p1': 12, 'p2': 4}
    assert all(all(f) for f in flags.values()) and len(flags) == 114
    paths = [SOURCE, SWEEP, Path(__file__), ROOT / 'scripts/c5_single_spoke_root_conservation.py',
             ROOT / 'scripts/c5_single_spoke_cores.py']
    return dict(scope='arbitrary-size paper root lemma plus local attachment and full unary relation audit',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_root_induction_audit=local_audit(), root_attachment_frames=frames,
                records=records, counts=dict(both=114, p1_only=0, p2_only=0), open_queries=[])


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
    print(json.dumps(dict(counts=result['counts'], classified=len(result['records']),
                         root_frames=len(result['root_attachment_frames'])), sort_keys=True))


if __name__ == '__main__':
    main()
