#!/usr/bin/env python3
"""Create T1 acceptance and a new integrated ledger; keep old bytes immutable."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-t1-rfibre'
PRIOR = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q2-restore-review'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write(name, obj):
    with (HERE / name).open('x') as stream:
        stream.write(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def main():
    for name in ('T1-paper-review.md', 'T1-stabilizer-review.md', 'T1-custody-algebra-review.md'):
        assert (HERE / name).is_file(), 'required independent review incomplete: ' + name
    checks = read(HERE / 'checks.json')
    independent = read(HERE / 'logs/independent-custody-calibration.stdout.log')
    assert checks['checks_pass'] and independent['status'] == 'passes with required coverage overlay'
    assert independent['custody']['delivery_sha256'] == checks['reviewed_delivery']['sha256']
    additional = read(HERE / 'extra-authority-inputs.json')['inputs']
    requested = read(HERE / 'extra-authority-pins.json')['additional_base_pins']
    for r in requested:
        match = next(i for i in additional if i['path'] == r['path'])
        assert all(match[k] == r[k] for k in ('base', 'git_blob', 'bytes', 'sha256'))
    for item in additional:
        assert pin(HERE / item['frozen_path'])['sha256'] == pin(REPO / item['path'])['sha256'] == item['sha256']

    overlay = read(HERE / 'T1-coverage-corrections.json')
    assert overlay['target_sha256'] == pin(TARGET / 'coverage.json')['sha256']
    corrected = read(TARGET / 'coverage.json')
    changes = Counter()
    pointers = set()
    for change in overlay['corrections']:
        pointer = change['field_json_pointer']
        assert pointer not in pointers
        pointers.add(pointer)
        parts = pointer.split('/')[1:]
        parent = corrected
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        field = parts[-1]
        assert field in ('X_fibre', 'G_fibre') and parent[field] == change['original_value']
        assert [parent['r'], parent['s']] == change['ordered_pin']
        assert parent['source_preimages'] is None
        parent[field] = change['corrected_value']
        changes[field] += 1
    assert dict(changes) == {'X_fibre': 352, 'G_fibre': 780}
    assert len(pointers) == 1132
    for query in corrected['queries']:
        for row in query['all_ten_literal_obligations']:
            for p in row['pins']:
                assert p['source_preimages'] is None
                if row['literal'][:3] == [0, 1, 0] and p['s'] in (2, 3):
                    assert p['X_fibre'].startswith('necessarily empty')
                if p['X_fibre'].startswith('necessarily empty'):
                    assert p['G_fibre'].startswith('necessarily empty')
    write('accepted-coverage.json', {'authority': 'original coverage plus independently checked 1132-field overlay',
                                     'original_coverage': pin(TARGET / 'coverage.json'),
                                     'correction_overlay': pin(HERE / 'T1-coverage-corrections.json'),
                                     'original_modified': False, 'coverage': corrected})

    before = read(PRIOR / 'remaining-schedules.json')
    assert before['counts']['remaining'] == 14 and all(r['t_s'] == 1 for r in before['remaining_schedules'])
    removed = deepcopy(before['remaining_schedules'])
    for row in removed:
        row['restoration_excluded'] = row['beta_q'] == 3
        row['source_minor_excluded'] = row['beta_q'] == 4
        row['source_excluded'] = True
        row['excluded_original_s_spokes'] = [[0], [2]]
        row['adoption_authority'] = 'acceptance.json in this fresh T1 review'
        if row['beta_q'] == 3:
            row['restored_Delta_rows'] = sorted(set(row['Delta']) & {0, 1})
            assert row['restored_Delta_rows']
            row['reason'] = 'complete same-source q0/q1 restorable r!=2 lift'
        else:
            assert row['beta_q'] == 4
            row['reason'] = 'retained original-edge K5 minor from complete S path blocks'
    prior_reviews = [REPO / 'audits' / name for name in
                     ('2026-10-11-n45-s-long-s-t2-q0-restore-review',
                      '2026-10-11-n45-s-long-s-t2-q2-restore-review',
                      '2026-10-11-n45-s-long-s-block-transfer-review')]
    wave_pins = [pin(p / n) for p in prior_reviews for n in ('acceptance.json', 'delivery.json')]
    ledger = {'base': BASE,
              'scope': 'only the raw28 necessary schedules within complete inherited K1-K12 U-owner-s/X-own-beta long-S contract',
              'previous_ledger': pin(PRIOR / 'remaining-schedules.json'),
              'new_worker_delivery': pin(TARGET / 'delivery.json'),
              'counts': {'raw': 28, 'previously_remaining': 14, 'newly_excluded': 14, 'total_excluded': 28,
                         'remaining': 0, 'remaining_schedule_spoke_combinations': 0,
                         'this_dispatch_wave_schedules': 24, 'this_dispatch_wave_spoke_combinations': 38,
                         'this_dispatch_wave_all_excluded': True},
              'excluded_schedules': before['excluded_schedules'] + removed,
              'newly_excluded_schedules': removed, 'remaining_schedules': [],
              'wave_acceptance_pins': wave_pins,
              'same_wave_other_new_proofs_used_as_T1_premises': False,
              'same_wave_accepted_outputs_used_only_for_integrated_ledger': True,
              'D_new_source_exclusions': 0,
              'source_execution_Lean_general_closure_established': False}
    assert len(ledger['excluded_schedules']) == 28
    write('remaining-schedules.json', ledger)
    claims = read(TARGET / 'claims.json')['claims']
    assert len(claims) == 9
    acceptance = {
        'task_id': 'N45-S-LONG-S-T1-RFIBRE-INDEPENDENT-REVIEW', 'base': BASE,
        'status': 'accepted within assigned contract with coverage correction overlay', 'adoption_layer': 'fresh exclusive audit review only',
        'reviewed_worker_files': [pin(TARGET / n) for n in ('delivery.json', 'REPORT.md', 'claims.json', 'coverage.json', 'calibration-certificate.json')],
        'claims': [{'id': c['id'], 'verdict': 'accepted under stated assigned-contract/paper/calibration quantifier; symbolic coverage with overlay',
                    'quantifier': c['quantifier'], 'conclusion': c['conclusion'], 'conclusion_type': c['conclusion_type']} for c in claims],
        'blocking_findings': [],
        'required_corrections': [{'finding': 'missing U010 and G-subset-X necessary-empty classifications',
                                  'new_X_empty': 352, 'new_G_empty': 780, 'changed_fields': 1132,
                                  'overlay': pin(HERE / 'T1-coverage-corrections.json'),
                                  'accepted_coverage': pin(HERE / 'accepted-coverage.json'), 'original_modified': False}],
        'paper_scope': {'K1_K12_all_retained': True, 'arbitrary_size': True, 'owner': 's', 't_s': 1,
                        'n_U': 2, 'm_s': 2, 'beta_q_domain': [3, 4], 'original_s_spoke_variants': [[0], [2]],
                        'U_support': [0, 1, 2], 'L_support': [2, 3, 4], 'S_support': [4, 0],
                        'original_r_split': [2, 2], 'original_e': ['r', 'b4'], 'retained_r_spokes': [],
                        'X_is_own_beta_minimal_core': True},
        'paper_results': {'beta_q3': {'schedules': 7, 'queries': 14, 'restored_q_rows': [0, 1],
                                     'pins': 'exists b in {1,3}, a !=2; no individual source-specific pin nonempty asserted',
                                     'T1_P22_both_spokes_closed': True},
                          'beta_q4': {'schedules': 7, 'queries': 14, 'retained_original_edge_K5_minor': True,
                                     'omitted_rb4_used_in_minor': False}},
        'inherited_dependencies': ['sealed beta role/column/private/split statements',
                                   'K4-free C block structure', 'original short-S N-diagonal',
                                   'pinned primary Gallai Lemma7/Theorem10'],
        'extra_direct_authority': additional,
        'new_full_restoration_exists_by_paper_construction_not_old_finite_terminal': True,
        'native_readonly_checks': checks, 'independent_check': independent,
        'independent_native_record': read(HERE / 'logs/independent-custody-calibration.command.json'),
        'paper_reviews': [pin(HERE / n) for n in ('T1-paper-review.md', 'T1-stabilizer-review.md')],
        'evidence_layers': {'paper': '14 schedules/28 original-spoke queries excluded under complete assigned contract and explicit inherited authorities',
                            'finite_calibration': 'fixed palettes/widgets/minor skeletons only; triggered and holds',
                            'target_source': {'executed': False, 'status': 'not triggered', 'trigger_count': None},
                            'source_realizability': 'not established', 'Lean': 'not established', 'general_N45_N2_E': 'not established'},
        'missing_BASE_findings': independent['custody']['missing_BASE_blobs'],
        'old_19_controls_reexecuted': False, 'shared_documents_updated': False,
        'old_deliveries_modified': False, 'commit_push_PR': False}
    write('acceptance.json', acceptance)
    report = '''# N45-S-LONG-S-T1-RFIBRE 獨立驗收與本輪整合

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

A／T1 的14 schedules、28個原spoke查詢全部通過任意大小紙面排除驗收。
九項 claims 在指定完整 K1–K12 範圍採納，coverage附1132-field更正overlay；無紙面阻斷。
與已驗收B/q0、C/q2整合後，本輪24份剩餘schedules／38個spoke查詢全部排除。
這只關閉完整指定契約下的必要域；未建立一般N45/N2/E closure。

## 同源紙面論證

限定原 U owner=s、U012/L234/pair S40、t_s=1、n_U=2、m_s=2、
原r-split(2,2)、原 s-spoke b0或b2、β=q3或q4、X=G−原rb4且X自己β-minimal。
所有原vertices/edges/rotation/ordered與shared contacts、attachments、旁支、完整
tuple preimages與空fibres保留，來源大小沒有上界。

獨立核雙真拒palette引理：完整degree4給lists≥degree，拒絕迫tight；兩root
queries僅在原端contacts改色。完整off-path非root lists相同，leaf-to-root唯一
palettes排路徑odd-cycle，bridge差交替迫正奇長與完整W residual pair。
固定s-contact在path、旁支或shared vertex均只作用同一list；穩定子核W全actual支援。
原U的Gallai／K4-free推廣另核fixedβ真拒、incident-edge slack、四原tethers與
由retained s-spoke接通的B∪s hub，沒有借原rb4或未證T4前提。

β=q4迫每個完整S path block都actual touch04；相鄰兩塊與原L的r→b2路、
原frame給connected/disjoint的K5五bags，全部十鄰接均原X retained edges，原rb4不用。
β=q3同樣minor與leaf-block degree論證，從任意大小原S推得恰兩原點u/v及原uv；
不是預設小S或刪旁支。q0/q1的actual U附件同為012；若同拒s1/3，當前列
的真palette反設即給U原K5 minor。故存在共同b∈{1,3}的完整U preimage；
原S在該b对全部r色相容，actual L完整assignment至少避兩個r色，選其一a≠2，
完整L/S/U/Col^I同pins接合，q0/q1每列均有同源full lift恢復原rb4。
每份q3 schedule的Δ至少含一恢復列；T1-P22兩spokes均由q0閉合。

逐claim主驗收見 [T1-paper-review.md](T1-paper-review.md)，獨立難點複核見
[T1-stabilizer-review.md](T1-stabilizer-review.md)。額外BASE E4 N-diagonal proof與
原pinned Gallai PDF已凍結於authority/；PDF p5–6 Lemma7/Theorem10原文亦已直接核閱。
保留明列上游紙面／外部依賴，未用同輪其它新結論作T1證明前提。

## Coverage更正、校準與custody

原U query010與兩β和literal01012/01021/01023同附件，FU={2,3}迫s2/3空。
原672位置中320已空，補352個X空欄位；G⊆X再補780個G空欄位，其中540由
原X已空、240由新U空推出。合1132個去重field pointers，保conditional空標籤、
原rb4 filter／rejection、collective恢復語義及全部null source preimages。
更正見 [T1-coverage-corrections.json](T1-coverage-corrections.json)，採納副本見
[accepted-coverage.json](accepted-coverage.json)。原交付bytes不動。

獨立無workerimports核48S/8U palette穩定子、8conditional widgets、18path及2leaf
minor skeletons，100bags connected/disjoint、200實際adjacency witnesses、兩structural
負控制及精確corrupt certificate。完整28queries／280列／4480pins／1120diagonal相符。
普通／seed17原生校準均exit0、stdout/stderr byte相同；負證書exit1命中指定階段，
contents/manifest及獨立custody-calibration亦exit0。校準不驗任意大小主證或來源實現。

custody核54payload/1,938,723bytes、55regular files/1directory、唯一排根delivery。
12BASE+11sealed authorities、一份external primary PDF、49immutable inputs與846份
old B payload／原證書全相符。整原target、root guarded union、HEAD/tracked diff零漂移。
詳見 [T1-custody-algebra-review.md](T1-custody-algebra-review.md)、[checks.json](checks.json)、logs。
root首份guard parser在執行重播前遇舊manifest欄名不匹配；失敗script與tool-call
capture限制保在failed-generations/，修正後上述原生重播全通過，未觸原交付。
原 delivery SHA：`2af82d9afdeaa5509dd211a8c6a64b84520dc379efce9fdd48f84832619d2898`。

## 本輪整合與停止點

前次raw28必要schedules已有四份q0→q1排除。本輪B新增q0三份、C新增q2七份，
A新增T1十四份；28=4+3+7+14，完整指定必要域剩0。本輪派出的是24schedules／
38spoke combinations，均有獨立採納的窄域來源矛盾。D另採納任意大小full transfer
恆等式及1,344 assignments校準，新增來源排除仍0；D自身保凍結時24/38歷史ledger。
整合只在新的 [remaining-schedules.json](remaining-schedules.json)，不改舊證書。

兩份缺BASE observations findings保留，dependent finite replay及舊19controls未跑。
target source executed=false、trigger_count=null、not triggered；source realizability、
新Lean與一般N45/N2/E closure均未建立。所有採納只在專屬review，未改共享文件、
原交付或舊證書；未commit/push/PR。見 [acceptance.json](acceptance.json) 及封存
[delivery.json](delivery.json)。
'''
    with (HERE / 'REPORT.md').open('x') as stream:
        stream.write(report)
    print(json.dumps({'accepted_claims': 9, 'newly_excluded_schedules': 14, 'queries': 28,
                      'coverage_changed_fields': 1132, 'wave_remaining_schedules': 0}))


if __name__ == '__main__':
    main()
