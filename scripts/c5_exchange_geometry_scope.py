#!/usr/bin/env python3
"""Audit the finite coverage of exchange-or-geometric-obstruction mechanisms.

This partitions existing necessary source data, replays complete target joins,
and applies existing local rules. It does not enumerate realizing disk graphs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2_bridge import evidence as bridge2
from c5_adjacent_degree5_no_mixed_t2_endpoints import evidence as endpoints2
from c5_adjacent_degree5_no_mixed_t2_path_palettes import evidence as path2, gallai_control
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import context, evidence as bridge21
from c5_adjacent_degree5_no_mixed_t2_t1_endpoints import evidence as endpoints21
from c5_root_degree_excess import budget

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_exchange_geometry_scope/observations.json'
TABLE = OUT.with_name('scope_table.md')
PREFIX = 'c5_adjacent_degree5_no_mixed'
TYPES = ('t2', 't1', 't0_pair_deficit', 't0_pair_overlap', 't0_singles')
LABELS = ('2:(2)', '1:(2,1)', '0:(2,2),D=1', '0:(2,2),O=1', '0:(2,1,1)')
CLOSED = {('t2', 't2'), ('t2', 't1'), ('t1', 't2'),
          ('t2', 't0_singles'), ('t0_singles', 't2')}


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))


def evidence_excerpt(value):
    """Keep all cases/supports, with one sufficient witness per fixed frame test."""
    if isinstance(value, list):
        return [evidence_excerpt(v) for v in value]
    if isinstance(value, dict):
        result = {k: evidence_excerpt(v) for k, v in value.items() if k != 'witnesses'}
        if 'witnesses' in value:
            result.update(witness_count=len(value['witnesses']),
                          first_witness=value['witnesses'][0] if value['witnesses'] else None)
        return result
    return value


def side_type(side):
    b = budget(side)
    assert b['kappa'] == 0 and b['D'] + b['O'] == 1
    shape = len(side['root_boundary']), side['ports']
    if shape == (2, [2]):
        return 't2'
    if shape == (1, [2, 1]):
        return 't1'
    if shape == (0, [2, 1, 1]):
        return 't0_singles'
    assert shape == (0, [2, 2])
    return 't0_pair_deficit' if b['D'] else 't0_pair_overlap'


def matrix(source):
    sides, joins = source['side_normal_forms'], source['abstract_conditions']['retained']
    lookup = {tuple(pair): i for i, pair in enumerate(joins)}
    assert len(lookup) == len(joins)
    groups = {(a, b): [] for a, b in product(TYPES, repeat=2)}
    for join_id, (i, j) in enumerate(joins):
        assert sides[i]['common'] == sides[j]['common']
        assert (j, i) in lookup
        groups[side_type(sides[i]), side_type(sides[j])].append(join_id)
    rows = []
    for (a, b), ids in groups.items():
        assert ids
        assert len(ids) == len(groups[b, a])
        pair = joins[ids[0]]
        rows.append(dict(z_type=a, w_type=b, count=len(ids), retained_join_ids=ids,
                         status='covered' if (a, b) in CLOSED else 'support_coverage_not_built',
                         first=dict(retained_join_id=ids[0], side_ids=pair,
                                    sides=[sides[i] for i in pair],
                                    budgets=[budget(sides[i]) for i in pair])))
    assert sorted(i for row in rows for i in row['retained_join_ids']) == list(range(3548))
    return rows


def choose_closure(base, record, target, bans):
    if base == 't2':
        bridge = bridge2(record, target, bans)
        endpoint = lambda: endpoints2(record, target, bans)
    else:
        bridge = bridge21(record, target, bans)
        endpoint = lambda: endpoints21(record, target, bans)
    direct = [c for c in bridge['components'] if c['direct_frame']['eliminated']]
    if direct:
        return 'direct_frame', bridge
    if bridge['eliminated']:
        return 'first_bridge', bridge
    end = endpoint()
    if end['eliminated']:
        return 'original_endpoints', end
    assert base == 't2', 'uncovered candidate in the completed t2/t1 family'
    path = path2(record, target, bans)
    assert path['eliminated']
    return 'whole_path_exchange', path


def audit_family(name, original, final, source, groups):
    sources = original['original_records']
    base_joins = source['abstract_conditions']['retained']
    by_pair = {tuple(pair): i for i, pair in enumerate(base_joins)}
    bound = [by_pair[tuple(s['side_ids'])] for s in sources]
    shape = ('t2', {'t2': 't2', 't2_t1': 't1', 't2_t0_singles': 't0_singles'}[name])
    expected = next(r['retained_join_ids'] for r in groups
                    if (r['z_type'], r['w_type']) == shape)
    assert sorted(bound) == expected
    for s in sources:
        assert [s['z'], s['w']] == [source['side_normal_forms'][i] for i in s['side_ids']]
    assert len(original['records']) == len(final['records'])
    query_rows, failures = [], []
    join_count = 0
    priority = {'root_pairs': 0, 'direct_frame': 1, 'first_bridge': 2,
                'original_endpoints': 3, 'whole_path_exchange': 4}
    for record, last in zip(original['records'], final['records'], strict=True):
        assert record['id'] == last['id']
        src = sources[record['source_id']]
        owners = ['z'] + ['w'] * (len(src['w']['ports']))
        assert len(src['z']['ports']) == 1
        ctx = context(record, src) if name == 't2_t1' else record
        for ti, (target, final_target) in enumerate(zip(record['targets'], last['targets'], strict=True)):
            row = target['row']
            assert row == final_target['row'] and final_target['status'] == 'accept'
            stages = []
            for ji, join in enumerate(target['joins']):
                bans = join['forbidden_sets']
                assert len(bans) == len(owners)
                # Independent literal root-color solver; no product of contact marginals.
                pairs = [(a, b) for a, b in product(range(4), repeat=2)
                         if a != b
                         and all(c != row[h] for root, c in [('z', a), ('w', b)]
                                 for h in src[root]['root_boundary'])
                         and all((a if owner == 'z' else b) not in f
                                 for owner, f in zip(owners, bans, strict=True))]
                assert canonical(pairs) == join['root_pairs']
                join_count += 1
                if pairs:
                    stages.append('root_pairs')
                    continue
                assert name != 't2_t0_singles'
                stage, evidence = choose_closure(name, ctx, row, bans)
                stages.append(stage)
                failures.append(dict(record_id=record['id'], target_index=ti, join_index=ji,
                                     row=row, original_join=join, closure=stage,
                                     evidence_excerpt=evidence_excerpt(evidence),
                                     full_evidence_sha256=sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()))
            assert stages
            stage = max(stages, key=priority.get)
            assert (stage == 'root_pairs') == (target['status'] == 'accept')
            query_rows.append(dict(record_id=record['id'], target_index=ti, closure=stage))
    return dict(name=name, source_join_ids=bound, support_records=len(original['records']),
                source_records_with_support=len({r['source_id'] for r in original['records']}),
                empty_source_fibers=len(sources)-len({r['source_id'] for r in original['records']}),
                complete_joins=join_count, queries=query_rows, failing_candidates=failures,
                query_closures=dict(sorted(Counter(q['closure'] for q in query_rows).items())),
                candidate_closures=dict(sorted(Counter(q['closure'] for q in failures).items())))


def path_sweep():
    """All alternating words in a stated domain, using full endpoint relations."""
    controls = []
    for d, length, style in product(range(4), (1, 3, 5, 7), ('bare', 'leaf', 'triangle', 'nested')):
        for odd in product([c for c in range(4) if c != d], repeat=(length+1)//2):
            word = tuple(odd[i//2] if i % 2 == 0 else d for i in range(length))
            graph = gallai_control(d, word, style)
            controls.append(dict(source_color=d, edge_palettes=word, branch_style=style,
                                 relation=graph['ordered_endpoint_relation'], forbidden=graph['forbidden'],
                                 constant_odd_palettes=len(set(odd)) == 1,
                                 full_control_sha256=sha256(json.dumps(graph, sort_keys=True).encode()).hexdigest()))
    counts = Counter('second_ban' if len(c['forbidden']) == 2 else 'singleton_only' for c in controls)
    assert len(controls) == 1920 and counts == {'second_ban': 192, 'singleton_only': 1728}
    return dict(scope='abstract Gallai list controls; not boundary degree-four disk sources',
                counts=dict(sorted(counts.items())), controls=controls)


def build():
    hashes, loaded = {}, {}

    def read(name):
        path = ROOT / 'artifacts' / name / 'observations.json'
        data = json.loads(path.read_text())
        hashes[str(path.relative_to(ROOT))] = sha256(path.read_bytes()).hexdigest()
        script = ROOT / 'scripts' / (name + '.py')
        assert data['source_sha256'] == sha256(script.read_bytes()).hexdigest()
        hashes[str(script.relative_to(ROOT))] = data['source_sha256']
        for rel, digest in data.get('inputs_sha256', {}).items():
            assert sha256((ROOT / rel).read_bytes()).hexdigest() == digest, rel
            hashes[rel] = digest
        loaded[name] = data
        return data

    source = read(PREFIX)
    groups = matrix(source)
    families = []
    for name, final_name in [('t2', 't2_path_palettes'), ('t2_t1', 't2_t1_endpoints'),
                             ('t2_t0_singles', 't2_t0_singles')]:
        base = read(PREFIX + '_' + name)
        final = base if name == final_name else read(PREFIX + '_' + final_name)
        families.append(audit_family(name, base, final, source, groups))
    # Bind and inspect all intermediate certificates, rather than skipping their inputs.
    for suffix in ('t2_bridge', 't2_endpoints', 't2_t1_bridge'):
        read(PREFIX + '_' + suffix)
    read('c5_root_degree_excess')
    query_counts, candidate_counts = Counter(), Counter()
    for family in families:
        query_counts.update(family['query_closures'])
        candidate_counts.update(family['candidate_closures'])
    # First-edge information alone does not force the remaining odd palettes.
    variable = gallai_control(3, (2, 3, 1), 'nested')
    constant = gallai_control(3, (2, 3, 2), 'nested')
    assert variable['forbidden'] == [3] and constant['forbidden'] == [2, 3]
    original21 = loaded[PREFIX + '_t2_t1']
    r22 = original21['records'][22]
    ctx22 = context(r22, original21['original_records'][r22['source_id']])
    row, bans = [0, 1, 2, 1, 2], [[1], [0, 3], [2]]
    br22, ep22 = bridge21(ctx22, row, bans), endpoints21(ctx22, row, bans)
    assert not br22['eliminated'] and ep22['eliminated']
    assert all(not c['first_bridge']['applicable'] for c in br22['components'])
    guards = dict(variable_odd_palettes=variable, constant_odd_palettes=constant,
                  nonconserved_source_ban=dict(record_id=22, row=row, forbidden_sets=bans,
                                              bridge=br22, endpoints=ep22))
    sweep = path_sweep()
    covered = sum(g['count'] for g in groups if g['status'] == 'covered')
    summary = dict(source_sides=118, ordered_source_joins=3548, refined_side_types=5,
                   ordered_shape_cells=25, unordered_shape_cells=15,
                   covered_ordered_cells=len(CLOSED), covered_unordered_cells=3,
                   covered_source_joins=covered, source_joins_without_support_coverage=3548-covered,
                   audited_support_records=sum(f['support_records'] for f in families),
                   audited_target_queries=sum(len(f['queries']) for f in families),
                   complete_candidate_joins=sum(f['complete_joins'] for f in families),
                   originally_failing_candidates=sum(candidate_counts.values()),
                   query_closures=dict(sorted(query_counts.items())),
                   candidate_closures=dict(sorted(candidate_counts.items())),
                   abstract_path_controls=len(sweep['controls']),
                   abstract_path_outcomes=sweep['counts'],
                   new_target_accepts=0, new_source_exclusions=0)
    assert covered == 552 and summary['audited_target_queries'] == 2004
    assert summary['complete_candidate_joins'] == 6376
    assert summary['originally_failing_candidates'] == 306
    assert query_counts['root_pairs'] == 1754 and query_counts['whole_path_exchange'] == 4
    return dict(schema=1, scope='coverage audit of existing necessary data; no new source theorem',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(), inputs_sha256=hashes,
                summary=summary, matrix=groups, families=families, guard_controls=guards,
                abstract_path_sweep=sweep)


def render(data):
    cells = {(r['z_type'], r['w_type']): r for r in data['matrix']}
    lines = ['# 交換或幾何阻斷：有限覆蓋表', '',
             '由 checker 生成；數字是原必要接合份數，✓ 表示已有整型雙列分離。',
             '未標記者尚缺完整支援覆蓋，不是反例；未聲稱任何一筆可實現。', '',
             '| z \\ w | ' + ' | '.join(LABELS) + ' |',
             '| --- | ' + ' | '.join(['---:'] * 5) + ' |']
    for kind, label in zip(TYPES, LABELS, strict=True):
        values = [str(cells[kind, other]['count']) + (' ✓' if (kind, other) in CLOSED else '')
                  for other in TYPES]
        lines.append('| ' + label + ' | ' + ' | '.join(values) + ' |')
    lines.extend(['', '| 子表 | 必要支援 | 完整候選 joins | 查詢 | 原失敗候選 |',
                  '| --- | ---: | ---: | ---: | ---: |'])
    for f in data['families']:
        lines.append(f"| {f['name']} | {f['support_records']} | {f['complete_joins']} | "
                     f"{len(f['queries'])} | {len(f['failing_candidates'])} |")
    lines.extend(['', '機制前提、未覆蓋領域與重播見 [報告](../../docs/c5_exchange_geometry_scope.md)。', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    outputs = {OUT: json.dumps(result, sort_keys=True, indent=2) + '\n', TABLE: render(result)}
    for path, payload in outputs.items():
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
