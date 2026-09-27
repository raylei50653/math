#!/usr/bin/env python3
"""Necessary (2,2) support/contact classification, never a graph search."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_single_spoke_cores import (Q, U, PI, RHO, PERMS, SUPPORTS, T4,
                                   TARGETS, covers, lifts, transport)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PAIRS = tuple(product(range(4), repeat=2))


def forbidden(rel):
    return frozenset.intersection(*(frozenset(t) for t in rel))


def released(rel, fs):
    return all(any(t[j] == a and t[1-j] != a for t in rel)
               for a in fs for j in (0, 1))


def schemas():
    result = []
    # Exhaustion is of the sixteen local ordered tuples, not source graphs.
    for mask in range(1, 1 << 16):
        rel = tuple(t for k, t in enumerate(PAIRS) if mask >> k & 1)
        fs = forbidden(rel)
        if fs and released(rel, fs):
            result.append(dict(id=len(result), forbidden=sorted(fs), tuples=rel))
    assert len(result) == 4 * 95 + 6
    for x in result:
        if len(x['forbidden']) == 2:
            assert set(x['tuples']) == set(permutations(x['forbidden']))
    return result


SCHEMAS = schemas()


@lru_cache(None)
def schema_ids(support, ban):
    stabilizer = tuple(p for p in PERMS if all(p[Q[i]] == Q[i] for i in support))
    return tuple(x['id'] for x in SCHEMAS if tuple(x['forbidden']) == ban and all(
        {tuple(p[c] for c in t) for t in x['tuples']} == set(x['tuples'])
        for p in stabilizer))


def placements(s, supports):
    # Save ALL lifts, not only one witness per component order.
    return [dict(order=order, lifted_supports=ls,
                 contact_words=[[f'C{k}.{j}' for k in order for j in orientations[k]]
                                for orientations in product(((0, 1), (1, 0)), repeat=2)])
            for order in permutations(range(2))
            for ls in product(*(lifts(s, x) for x in supports))
            if max(ls[order[0]]) <= min(ls[order[1]])]


@lru_cache(None)
def bounds(support, ban, row):
    images, ps = transport(support, ban, row)
    if images:
        assert len(images) == 1
        return dict(exact=True, forbidden_options=images, upper=images[0],
                    permutation=ps[0], bridge_exclusions=[])
    seen = {row[i] for i in support}
    qseen = {Q[i] for i in support}
    # Arbitrary-size unused-pair bridge lemma, applicable to each q ban.
    excludes = []
    for d in sorted(U - seen - qseen):
        witness = next(((a, e) for a in ban for e in sorted(U - qseen)
                        if len({a, d, e}) == 3), None)
        if witness:
            excludes.append(dict(color=d, q_forbidden=witness[0], unused_partner=witness[1]))
    removed = {x['color'] for x in excludes}
    opts = []
    for n in range(3):
        for f in combinations(range(4), n):
            fs = set(f)
            if fs & removed:
                continue
            if any(len(seen | {a}) < 2 for a in fs):
                continue
            if any({p[c] for c in fs} != fs for p in PERMS
                   if all(p[c] == c for c in seen)):
                continue
            opts.append(f)
    return dict(exact=False, forbidden_options=opts,
                upper=sorted(set().union(*map(set, opts))), bridge_exclusions=excludes)


def row_record(s, supports, bans, row):
    bs = [bounds(x, f, row) for x, f in zip(supports, bans)]
    available = U - {row[s]}
    unions = [set().union(*map(set, fs)) for fs in product(*(x['forbidden_options'] for x in bs))]
    guaranteed = available - set().union(*unions)
    rejecting = [fs for fs in product(*(x['forbidden_options'] for x in bs))
                 if available <= set().union(*map(set, fs))]
    all_reject = all(available <= u for u in unions)
    return dict(row=row, components=bs, guaranteed_z_colors=sorted(guaranteed),
                status='reject' if all_reject else 'unresolved' if rejecting else 'accept',
                rejection_options=rejecting)


def reflect_record(r):
    out = dict(spoke=RHO[r['spoke']],
               supports=[sorted(RHO[i] for i in x) for x in r['supports']],
               bans=[sorted(PI[c] for c in x) for x in r['bans']],
               placements=[dict(order=list(reversed(p['order'])),
                   lifted_supports=[sorted(5-v for v in x) for x in p['lifted_supports']],
                   contact_words=[list(reversed(w)) for w in p['contact_words']]) for p in r['placements']],
               targets=[])
    for e in r['targets']:
        row = tuple(PI[e['row'][RHO[i]]] for i in range(5))
        normalizer = tuple(list(dict.fromkeys(row)).index(c) if c in row else 3 for c in range(4))
        assert sorted(normalizer) == list(range(4))
        out['targets'].append(dict(row=row, status=e['status'],
            canonical_row=[normalizer[c] for c in row],
            canonical_forbidden_options=[sorted([sorted(normalizer[PI[c]] for c in f)
                                                 for f in x['forbidden_options']])
                                         for x in e['components']],
            canonical_guaranteed_z_colors=sorted(normalizer[PI[c]] for c in e['guaranteed_z_colors']),
            forbidden_options=[sorted([sorted(PI[c] for c in f) for f in x['forbidden_options']])
                               for x in e['components']],
            guaranteed_z_colors=sorted(PI[c] for c in e['guaranteed_z_colors'])))
    return out


def local_checks():
    transitions = []
    for a, b in permutations(range(4), 2):
        next_pairs = [(c, d) for c, d in product(range(4), repeat=2)
                      if a != c and b != d and {a, c} == {b, d}]
        assert next_pairs == [(b, a)]
        transitions.append(dict(incoming=[a, b], outgoing=next_pairs[0]))
    # Equal marginals do not determine simultaneous avoidance.
    r = ((0, 1), (1, 0))
    cart = tuple(product({0, 1}, repeat=2))
    assert forbidden(r) == {0, 1} and forbidden(cart) == set()
    # Independently check joins, release and colour transport for every q schema.
    checks = 0
    joins = 0
    for s in range(5):
        for bans in covers(s, (2, 2)):
            choices = [[x['tuples'] for x in SCHEMAS if tuple(x['forbidden']) == f] for f in bans]
            for rels in product(*choices):
                direct = {a for a in U if any(all(a not in t for t in ts)
                                              for ts in product(*rels))}
                assert direct == {Q[s]}
                joins += 1
    assert joins == 2880
    for x in SCHEMAS:
        rel = x['tuples']
        for p in PERMS:
            mapped = tuple(tuple(p[c] for c in t) for t in rel)
            assert forbidden(mapped) == {p[c] for c in x['forbidden']}
            assert released(mapped, forbidden(mapped))
            checks += 1
    return dict(nonempty_binary_relations_checked=65535, schemas=len(SCHEMAS),
                transport_checks=checks, minimal_cover_full_tuple_joins=joins, bridge_transitions=transitions,
                marginal_counterexample=dict(relation=r, cartesian_marginals=cart))


def source_controls(records):
    src = ROOT / 'artifacts/c5_single_spoke_cores/observations.json'
    old = json.loads(src.read_text())['source_controls']['witnesses']
    index = {(r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans']))): r
             for r in records}
    result = []
    for w in old:
        s, ss, fs = w['spoke'], w['supports'], w['q_bans']
        if s not in (0, 1, 4):
            s, ss, fs = RHO[s], [sorted(RHO[i] for i in x) for x in ss], [sorted(PI[c] for c in f) for f in fs]
        r = index[s, tuple(map(tuple, ss)), tuple(map(tuple, fs))]
        assert r['T4_status'] == 'excluded'
        for e in w['rows']:
            rels = e['relations']
            assert [sorted(forbidden(x)) for x in rels] == e['forbidden']
            for k, rel in enumerate(rels):
                assert released(rel, forbidden(rel))
                bound = bounds(tuple(w['supports'][k]), tuple(w['q_bans'][k]), tuple(e['row']))
                assert tuple(e['forbidden'][k]) in map(tuple, bound['forbidden_options'])
            if tuple(e['row']) == Q:
                for k, rel in enumerate(rels):
                    mapped = tuple(sorted(tuple(PI[c] if w['spoke'] not in (0, 1, 4) else c for c in t) for t in rel))
                    assert mapped in {tuple(SCHEMAS[i]['tuples']) for i in r['relation_schema_ids'][k]}
            direct = {a for a in U - {e['row'][w['spoke']]} if any(
                all(a not in t for t in ts) for ts in product(*rels))}
            assert direct == set(e['z_allowed'])
        result.append(dict(source_index=w['source_index'], representative_record=r['id'],
                           checked_rows=len(w['rows'])))
    assert len(result) == 16
    return dict(input_sha256=sha256(src.read_bytes()).hexdigest(), witnesses=result,
                scope='inherited full tuple controls, all fail T4; no new disk audit')


def run():
    records, counts = [], Counter()
    for s in (0, 1, 4):
        for bans in covers(s, (2, 2)):
            choices = [tuple(x for x in SUPPORTS if schema_ids(x, f)) for f in bans]
            for supports in product(*choices):
                counts[f'{s}:relation_stabilizer_pass'] += 1
                pos = placements(s, supports)
                if not pos:
                    counts[f'{s}:order_excluded'] += 1
                    continue
                if any(len({Q[i] for i in x} | {a}) < 2
                       for x, f in zip(supports, bans) for a in f):
                    counts[f'{s}:exterior_excluded'] += 1
                    continue
                r = dict(id=len(records), spoke=s, supports=supports, bans=bans,
                         placements=pos, ordered_contacts=[['C0.0', 'C0.1'], ['C1.0', 'C1.1']],
                         relation_schema_ids=[schema_ids(x, f) for x, f in zip(supports, bans)])
                r['double_forbidden_structure'] = [dict(component=k, ordered_path_endpoints=r['ordered_contacts'][k],
                    path='odd length; every edge is an original bridge',
                    first_palette_pair=[f[1], f[0]],
                    boundary_indices_forbidden_on_path=[i for i in supports[k] if Q[i] in f],
                    actual_support_required_in_side_branches=[i for i in supports[k] if Q[i] in f])
                    for k, f in enumerate(bans) if len(f) == 2]
                r['targets'] = [row_record(s, supports, bans, b) for b in TARGETS]
                fail = next((e for b in T4 if (e := row_record(s, supports, bans, b))['status'] == 'reject'), None)
                r['T4_status'] = 'excluded' if fail else 'retained'
                if fail:
                    r['T4_witness'] = fail
                if not fail:
                    missing = set(range(5)) - {s} - set().union(*map(set, supports))
                    assert missing in (set(), {4})
                    if missing:
                        for e in r['targets']:
                            assert e['status'] != 'reject'
                            t4 = list(e['row'])
                            t4[4] = 3
                            assert tuple(t4) in T4
                            assert all(t4[i] == e['row'][i] for x in supports for i in x)
                            e['local_status'] = e['status']
                            e['status'] = 'accept'
                            e['T4_recoloring_witness'] = t4
                    r['touches_all_boundary'] = not missing
                r['reflection'] = reflect_record(r)
                reflected = r['reflection']
                for place in reflected['placements']:
                    assert all(tuple(x) in lifts(reflected['spoke'], tuple(support))
                               for x, support in zip(place['lifted_supports'], reflected['supports']))
                    a, b = place['order']
                    assert max(place['lifted_supports'][a]) <= min(place['lifted_supports'][b])
                for k, ids in enumerate(r['relation_schema_ids']):
                    target_ids = schema_ids(tuple(reflected['supports'][k]), tuple(reflected['bans'][k]))
                    target_relations = {tuple(SCHEMAS[i]['tuples']) for i in target_ids}
                    for ident in ids:
                        mapped = tuple(sorted(tuple(PI[c] for c in t) for t in SCHEMAS[ident]['tuples']))
                        assert mapped in target_relations
                counts[f'{s}:minimal_q_necessary'] += 1
                counts[f'{s}:T4_{r["T4_status"]}'] += 1
                if not fail:
                    counts['retained_targets:' + '/'.join(e['status'] for e in r['targets'])] += 1
                records.append(r)
    # Swapping component names must preserve every conclusion.
    lookup = {(r['spoke'], r['supports'], r['bans']): r for r in records}
    for r in records:
        rr = lookup[r['spoke'], tuple(reversed(r['supports'])), tuple(reversed(r['bans']))]
        assert r['T4_status'] == rr['T4_status']
        assert [e['status'] for e in r['targets']] == [e['status'] for e in rr['targets']]
    inputs = ['scripts/c5_single_spoke_two_two.py', 'scripts/c5_single_spoke_cores.py', 'docs/c5_single_spoke_cores.md',
              'docs/c5_single_spoke_two_contact_bounds.md', 'docs/c5_single_spoke_bridge_path.md',
              'docs/c5_unattached_boundary.md']
    return dict(scope='necessary arbitrary-size reduction; retained configurations are not realizations',
                inputs={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                counts=dict(sorted(counts.items())), local_checks=local_checks(),
                q_relation_schemas=SCHEMAS, records=records, source_controls=source_controls(records))


def support_table(result):
    lines = ['# (2,2) necessary actual-support table', '',
             'Generated by `scripts/c5_single_spoke_two_two.py`; no realization claim.', '',
             'Only T4-retained representative records; exchanging C0/C1 is suppressed here,',
             'but all labels, all slit lifts and all four contact orientations remain in observations.json.',
             'R means forced rejection, A proved acceptance, ? unresolved. Upper bounds are for C0 / C1.',
             'Each unknown bound also has correlated forbidden-set options in the JSON; U alone loses that information.', '',
             '| id | s | F0(q) / F1(q) | S0 / S1 | p1 upper | p2 upper | p1/p2 |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    def sets(xs):
        return ' / '.join(''.join(map(str, x)) or 'empty' for x in xs)
    for r in result['records']:
        if r['T4_status'] != 'retained' or r['bans'] > tuple(reversed(r['bans'])):
            continue
        bs = [sets([c['upper'] for c in e['components']]) for e in r['targets']]
        status = '/'.join({'accept': 'A', 'reject': 'R', 'unresolved': '?'}[e['status']] for e in r['targets'])
        lines.append(f"| {r['id']} | {r['spoke']} | {sets(r['bans'])} | {sets(r['supports'])} | {bs[0]} | {bs[1]} | {status} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    table = support_table(result)
    table_path = OUT.with_name('support_table.md')
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
        assert table_path.read_text() == table, 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        table_path.write_text(table)
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
