#!/usr/bin/env python3
"""E3 adjacent-root row necessities, without a four-colour oracle.

Finite scope: common D5 transports, repeated-spoke queries, and exact
external-neighbour tightness tables for the named B2/B3 01/23 skeleton.
These necessary local tables are not a census or a realizability assertion.
All files written by the producer are exclusively created; --check reads.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e3/adjacent_rows.json'
COLORS = tuple(range(4))
TRIPLE = (1, 4, 6)


def normalize(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


ROWS = tuple(sorted({normalize(x) for x in product(COLORS, repeat=5)
                     if all(x[i] != x[(i+1) % 5] for i in range(5))}))
FRAME = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}


def subsets(items):
    values = tuple(items)
    return [tuple(values[i] for i in range(len(values)) if m >> i & 1)
            for m in range(1 << len(values))]


def singleton(row):
    return next(i for i, c in enumerate(row) if row.count(c) == 1)


def root_pairs(row):
    # One literal colour frame, original a-spokes 01 and b-spokes 23.
    return [(a, b) for a, b in product(COLORS, repeat=2)
            if a != b and a not in (row[0], row[1])
            and b not in (row[2], row[3])]


def table(face):
    records = []
    for owners in subsets(('a', 'b')):
        possible = []
        excluded = []
        for attachments in subsets(face):
            if len(owners) + len(attachments) > 4:
                continue
            violations = []
            for ri in TRIPLE:
                q = ROWS[ri]
                for a, b in root_pairs(q):
                    outside = [q[v] for v in attachments]
                    outside += [a] if 'a' in owners else []
                    outside += [b] if 'b' in owners else []
                    if len(set(outside)) != len(outside):
                        violations.append(dict(row_index=ri, row=q,
                            original_root_pair=[a, b], external_colours=outside,
                            exact_list=sorted(set(COLORS)-set(outside)),
                            original_degree_C=4-len(outside)))
            if not violations:
                possible.append(list(attachments))
            else:
                excluded.append(dict(actual_boundary_attachments=attachments,
                    first_literal_slack_witness=violations[0],
                    all_literal_slack_witnesses=violations))
        # Every owner is a real original vertex, not duplicated incidences.
        max_outside = max(len(owners) + len(s) for s in possible)
        assert 4-max_outside >= 2
        records.append(dict(owners=owners, actual_attachment_options=possible,
            minimum_degree_C=4-max_outside, excluded_attachment_options=excluded))
    return records


def leaf_signatures(face, records):
    # Row1 fixed, two different legitimate pins in the same original C.
    q = ROWS[1]
    pins = ((3, 1), (2, 3))
    assert all(p in root_pairs(q) for p in pins)
    result = []
    for rec in records:
        owners = rec['owners']
        for attachments in rec['actual_attachment_options']:
            if len(owners)+len(attachments) != 2:
                continue
            lists = []
            for a, b in pins:
                outside = [q[v] for v in attachments]
                outside += [a] if 'a' in owners else []
                outside += [b] if 'b' in owners else []
                lists.append(sorted(set(COLORS)-set(outside)))
            result.append(dict(owners=owners, actual_boundary_attachments=attachments,
                original_row_index=1, original_row=q, original_pins=pins,
                joint_exact_list_signature=lists))
    signatures = [json.dumps(r['joint_exact_list_signature']) for r in result]
    assert len(set(signatures)) == len(signatures)
    return result


def build():
    cells = json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())
    assert tuple(map(tuple, cells['pattern_order'])) == ROWS
    assert [singleton(ROWS[i]) for i in TRIPLE] == [3, 1, 0]
    t4 = [i for i, q in enumerate(ROWS) if len(set(q)) == 4]
    assert t4 == [2, 5, 7, 8, 9]
    spoke_queries = []
    for support in combinations(range(5), 3):
        witnesses = []
        for ri in TRIPLE:
            q = ROWS[ri]
            for j, k in combinations(support, 2):
                if q[j] == q[k]:
                    witnesses.append(dict(row_index=ri, singleton_position=singleton(q),
                        literal_row=q, original_omitted_spoke_endpoint=j,
                        original_retained_same_colour_spoke_endpoint=k,
                        original_remaining_spoke_endpoints=[v for v in support if v != j],
                        root_a_available_colours=sorted(set(COLORS)-{q[v] for v in support})))
        assert witnesses  # Directly supplies the quaternary leaf-slack query.
        spoke_queries.append(dict(original_three_spoke_support=support,
            selected_triple_queries=witnesses))
    pair_queries = []
    for support in combinations(range(5), 2):
        witnesses = [dict(row_index=ri, literal_row=ROWS[ri]) for ri in TRIPLE
                     if ROWS[ri][support[0]] == ROWS[ri][support[1]]]
        assert bool(witnesses) == (support not in FRAME)
        pair_queries.append(dict(original_spoke_pair=support,
            selected_triple_repeated_colour_witnesses=witnesses,
            is_original_boundary_edge=support in FRAME))
    # Common D5 transport: every coordinate, row, and colour frame moves once.
    transports = []
    for sign, shift in product((1, -1), range(5)):
        phi = [(sign*i+shift) % 5 for i in range(5)]
        rows = []
        for ri in range(10):
            literal = [None]*5
            for i, j in enumerate(phi):
                literal[j] = ROWS[ri][i]
            target = normalize(literal)
            colour_map = {}
            for c, d in zip(literal, target):
                assert c not in colour_map or colour_map[c] == d
                colour_map[c] = d
            rows.append(dict(original_row_index=ri, transported_literal_row=literal,
                transported_row_index=ROWS.index(target),
                one_global_colour_map=colour_map))
        transports.append(dict(original_boundary_map=phi,
            selected_triple_target_indices=[rows[ri]['transported_row_index'] for ri in TRIPLE],
            complete_row_transport=rows))
    short = table((1, 2))
    long = table((0, 3, 4))
    assert [r['actual_attachment_options'] for r in short] == [
        [[], [1], [2], [1, 2]], [[], [1]], [[], [2]], [[]]]
    assert [r['actual_attachment_options'] for r in long] == [
        [[], [0], [3], [4], [0, 4], [3, 4]], [[], [0]], [[], [3]], [[]]]
    short_sig = leaf_signatures((1, 2), short)
    long_sig = leaf_signatures((0, 3, 4), long)
    assert len(short_sig) == 4 and len(long_sig) == 5
    shared_leaf_slack = []
    for v, ri, pin in [(0, 6, (2, 0)), (3, 1, (2, 1)), (4, 1, (2, 1))]:
        q = ROWS[ri]
        assert pin in root_pairs(q)
        outside = [pin[0], pin[1], q[v]]
        exact = sorted(set(COLORS)-set(outside))
        assert len(exact) > 1
        shared_leaf_slack.append(dict(actual_extra_boundary_neighbor=v,
            selected_row_index=ri, literal_row=q, original_root_pair=pin,
            exact_leaf_list=exact, original_degree_C=1))
    return dict(schema='c5-excess-two-e3-adjacent-row-necessities-v1',
        scope='Finite common row/attachment algebra. No graph census, no topology proof, no realizability oracle.',
        pattern_order=ROWS, T4_indices=t4, selected_triple=TRIPLE,
        selected_singleton_positions=[3, 1, 0],
        optional_three_colour_acceptance_is_unconstrained=[0, 3],
        complete_D5_transports=transports,
        all_original_three_spoke_queries=spoke_queries,
        all_original_spoke_pair_queries=pair_queries,
        B2_short_face_table=short, B3_long_face_table=long,
        B2_leaf_joint_signatures=short_sig, B3_leaf_joint_signatures=long_sig,
        B3_shared_leaf_slack_witnesses=shared_leaf_slack,
        general_lemma_positive_controls='Validated by sibling E3 controls checker on exact E1 951/935 graphs; these local B2/B3 tables require original mixed incidence(2,2), absent in both controls.',
        summary=dict(complete_D5_transports=len(transports),
            original_three_spoke_supports=len(spoke_queries),
            original_spoke_pairs=len(pair_queries),
            short_leaf_signatures=len(short_sig), long_leaf_signatures=len(long_sig),
            shared_leaf_slack_witnesses=len(shared_leaf_slack)))


def encoded(data):
    return json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    payload = encoded(data)
    if args.check:
        assert OUT.read_text() == payload, 'saved artifact bytes differ'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open('x') as stream:
            stream.write(payload)
    print(json.dumps(dict(**data['summary'], sha256=sha256(payload.encode()).hexdigest(),
        check=args.check), sort_keys=True))


if __name__ == '__main__':
    main()
