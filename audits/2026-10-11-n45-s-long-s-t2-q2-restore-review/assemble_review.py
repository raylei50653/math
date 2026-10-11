#!/usr/bin/env python3
"""Create q2 acceptance and its required overlay in this fresh review only."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q2-restore'
PRIOR = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q0-restore-review'
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
    checks = read(HERE / 'checks.json')
    independent = read(HERE / 'logs/independent-custody-algebra.stdout.log')
    assert checks['checks_pass'] and independent['status'] == 'passes with required coverage overlay'
    overlay = read(HERE / 'q2-coverage-corrections.json')
    assert overlay['target_sha256'] == pin(TARGET / 'coverage.json')['sha256']
    assert len(overlay['corrections']) == 112
    corrected = read(TARGET / 'coverage.json')
    modified = set()
    for change in overlay['corrections']:
        s, r, p = change['schedule_index'], change['literal_index'], change['pin_index']
        key = (s, r, p)
        assert key not in modified
        modified.add(key)
        cell = corrected['schedules'][s]['all_ten_literal_obligations'][r]['pins'][p]
        assert cell['X_necessary_under_true_source'] == change['original_value']
        assert cell['necessary_empty_reasons'] == change['original_reasons']
        assert [cell['r'], cell['s']] == change['ordered_pin']
        assert corrected['schedules'][s]['all_ten_literal_obligations'][r]['literal'] == change['literal']
        cell['X_necessary_under_true_source'] = change['corrected_value']
        cell['necessary_empty_reasons'] = change['corrected_reasons']
    write('accepted-coverage.json', {'authority': 'original coverage plus independently checked 112-cell correction overlay',
                                     'original_coverage': pin(TARGET / 'coverage.json'),
                                     'correction_overlay': pin(HERE / 'q2-coverage-corrections.json'),
                                     'original_modified': False, 'coverage': corrected})

    old = read(PRIOR / 'remaining-schedules.json')
    assert old['counts']['remaining'] == 21
    removed = [deepcopy(r) for r in old['remaining_schedules'] if r['t_s'] == 2 and r['beta_q'] == 2]
    remaining = [r for r in old['remaining_schedules'] if not (r['t_s'] == 2 and r['beta_q'] == 2)]
    assert len(removed) == 7 and len(remaining) == 14 and all(r['t_s'] == 1 for r in remaining)
    for r in removed:
        r['restoration_excluded'] = True
        r['reason'] = 'direct full q3/q4 pin(0,3) product nonempty and restores original rb4'
        r['restored_Delta_rows'] = sorted(set(r['Delta']) & {3, 4})
        assert r['restored_Delta_rows']
        r['adoption_authority'] = 'acceptance.json in this fresh q2 review'
    write('remaining-schedules.json', {
        'base': BASE, 'scope': 'necessary schedules only within complete inherited K1-K12 U-owner-s/X-own-beta contract',
        'previous_ledger': pin(PRIOR / 'remaining-schedules.json'),
        'new_worker_delivery': pin(TARGET / 'delivery.json'),
        'counts': {'raw': 28, 'previously_remaining': 21, 'newly_excluded': 7,
                   'total_excluded': 14, 'remaining': 14, 'remaining_schedule_spoke_combinations': 28},
        'excluded_schedules': old['excluded_schedules'] + removed, 'newly_excluded_schedules': removed,
        'remaining_schedules': remaining, 'remaining_partition': {'t_s_1_beta_q3': 7, 't_s_1_beta_q4': 7},
        't_s_2_branch': 'all fourteen raw necessary schedules excluded under complete assigned contract',
        'same_wave_q0_proof_used_as_new_q2_premise': False,
        'same_wave_q0_acceptance_used_only_for_integrated_ledger': True})
    claims = read(TARGET / 'claims.json')['claims']
    accepted = []
    for c in claims:
        verdict = 'accepted under complete assigned K1-K12 contract'
        if c['id'] == 'CQ2-COVER7':
            verdict += '; adopt coverage only with 112-cell overlay'
        if c['id'] == 'CQ2-CALIBRATION':
            verdict = 'accepted bounded literal/pin arithmetic and native runtime; original checker does not validate necessary-empty classification'
        accepted.append({'id': c['id'], 'verdict': verdict, 'quantifier': c['quantifier'], 'conclusion': c['conclusion']})
    assert len(accepted) == 9
    write('acceptance.json', {
        'task_id': 'N45-S-LONG-S-T2-Q2-RESTORE-INDEPENDENT-REVIEW', 'base': BASE,
        'status': 'accepted within assigned contract with coverage correction overlay', 'adoption_layer': 'fresh exclusive audit review only',
        'reviewed_worker_files': [pin(TARGET / n) for n in ('delivery.json', 'REPORT.md', 'claims.json', 'coverage.json', 'calibration.json')],
        'claims': accepted, 'blocking_findings': [],
        'required_corrections': [{'finding': '112 known-empty T4 X cells omitted from coverage',
                                  'overlay': pin(HERE / 'q2-coverage-corrections.json'),
                                  'accepted_coverage': pin(HERE / 'accepted-coverage.json'),
                                  'scope': '7 schedules x4 literals x4 r pins at s1', 'original_modified': False}],
        'paper_scope': {'owner': 's', 't_s': 2, 'beta_q': 2, 'U_support': [0, 1, 2], 'L_support': [2, 3, 4],
                        'S_support': [4, 0], 'original_s_spokes': [0, 2], 'original_r_split': [2, 2],
                        'original_s_split': [1, 1], 'original_e': ['r', 'b4'], 'retained_r_spokes': [],
                        'X_is_own_beta_minimal_core': True, 'all_K1_K12_retained': True, 'arbitrary_size': True},
        'new_nonempty_restored_full_fibres': [{'q': 3, 'literal': '01021', 'pins': [0, 3], 'b4_colour': 1},
                                            {'q': 4, 'literal': '01012', 'pins': [0, 3], 'b4_colour': 2}],
        'new_restoration_exists_by_direct_construction': True,
        'inherited_dependencies': {'beta_U_role': 'sealed SF-T2-ROLE with full preimage avoiding3 and its inherited paper/external authority',
                                   'QX_used_for_new_target_fibre_existence': False,
                                   'finite_terminal_chain_used_for_new_target_fibre_existence': False,
                                   'other_coverage_row_acceptance_labels': 'retain explicit inherited QX/SF-T2-EXTEND/E2 trust chain'},
        'schedules_excluded': [{'SigmaG_orbit': r['SigmaG_orbit'], 'QG': r['QG']} for r in removed],
        'native_readonly_checks': checks,
        'independent_check': independent,
        'independent_native_record': read(HERE / 'logs/independent-custody-algebra.command.json'),
        'evidence_layers': {'paper': 'seven arbitrary-size assigned necessary schedules excluded',
                            'finite_calibration': '720 S4 comparisons,6 partitions,1120 symbolic pin cells; no actual graph assignments',
                            'target_source': {'executed': False, 'status': 'not triggered', 'trigger_count': None},
                            'source_realizability': 'not established', 'Lean': 'not established', 'general_N45_N2_E': 'not established'},
        'missing_BASE_findings': independent['custody']['missing_BASE_blobs'],
        'old_19_controls_reexecuted': False, 'shared_documents_updated': False,
        'old_deliveries_modified': False, 'commit_push_PR': False})
    report = '''# N45-S-LONG-S-T2-Q2-RESTORE 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

七份 schedules 的任意大小紙面排除通過；九項 claims 在指定完整 K1–K12 範圍採納。
coverage 須附112-cell更正 overlay，無紙面阻斷。採納只記在本新 review。

## 同源完整非空 fibres

固定原 U owner=s、U012/L234/pair S40、r-split(2,2)、s-split(1,1)、
t_s=2/spokes02、β=q2、X=G−原 rb4 且 X 自己 β-minimal。
complete-degree/slack 給全 assignment 存在性和禁 r 欄至多二色。S 在 β 的
attachment 色10，完整 (2 3) map 固定 r0/r1，讓唯一 actual s-contact 避3，
故 S(β;0,3)、S(β;1,3) 均非空。原 U 的已採納 β 避3 preimage 及 Xβ拒絕
迫 S 禁欄={2,3}、L 禁欄={0,1}。得到不同 r 的局部種子 L(β;2,3)、S(β;0,3)，
不把它們當作同一 β whole lift。

全頂點色雙射將兩種子帶到共同 q3／q4 frame 與共同 pins(0,3)。目標 U 的
actual query010 另由 strict slack 及 (2 3) 證完整避3 preimages 非空。
全部 actual L/S/U preimage sets 與原 Col^I 的 restriction/union 給精確
L_X(q3;0,3)、L_X(q4;0,3) 非空完整 fibres。每份 lift 的原 r=0 不等於
本列 b4 色1／2，故原 rb4 全部恢復；所有 original/shared contacts、空 fibres、
tuple preimages 和旁支保留，大小沒有上界。

選 q4 覆蓋933/0124、933/0234、933/1234、941/024、941/124；選 q3 覆蓋
933/0123、941/023。每份選定列都在原 Δ，與原 G 拒絕矛盾。
详證見 [q2-paper-review.md](q2-paper-review.md)。新目標 fibres 的存在性直接構造，
不使用 Q(X) 或舊 finite-terminal 供存在性；仍繼承已採納 SF-T2-ROLE 的 β U 角色。
其它未構造列的 QX metadata 另保舊信任邊界。

## 必要更正與獨立校準

原 coverage 漏標四份 T4 literals 01203/01213/01231/01232 的 U012 identity：
F_U(β)={1} 使其 s=1 的全部 X pins 空。7 schedules×4列×4 r pins 共112個
cells，原全標 source-specific，須改 empty；原 G filter/rejection flags 不動。
[q2-coverage-corrections.json](q2-coverage-corrections.json) 逐項綁原 SHA、JSON pointer、
原值與修正理由；[accepted-coverage.json](accepted-coverage.json) 保存採納副本。
此更正不影響兩份非空 fibres、七份 Δ 覆蓋或校準計數，原交付 bytes 不動。

普通／seed17原生只讀重播 exit0、stdout/stderr byte相同；兩個負控制均exit1，
manifest verifier exit0。另一份無 worker imports 的獨立腳本核720 S4 comparisons、
6 partitions、4 full ordered-pin transports（64 maps）、70列/1120pins/280diagonal，
以及112-cell遺漏；不把只檢位置與色 maps 的 worker checker 說成已驗必要空分類。
原始校準值與更正採納範圍詳見 [q2-custody-algebra-review.md](q2-custody-algebra-review.md)。

custody 通過90 payload/5,015,240 bytes、92 regular files、14 directories，
唯一排除是根 delivery.json 和 seal-receipt.json；frozen同名manifest照列payload。
12 BASE、11 sealed physical authorities及一份外部 PDF 全相符。原1037 records
對應1036 distinct files（同一 Gallai PDF 重複記兩次且同 hash），全live零漂移；
原樹、HEAD、tracked diff不變。失敗 manifest-generation 與 exit1 原生紀錄已保留。
原 delivery SHA：`79dc6912fbd13f863986d1d85e6f4b9490920711e023d8c2ab33feb8cd454605`。

## 剩餘域與停止點

整合已驗收 q0 ledger 僅用於計數，未作本證明前提：21→14 necessary schedules，
剩 t_s=1 的 βq3七份／βq4七份及28 spoke combinations；原 t_s=2 的14份
必要 schedules 已在完整指定契約內全排。見 [remaining-schedules.json](remaining-schedules.json)。

兩份缺 BASE observations findings 保留，dependent finite replay與舊19 controls
均未執行。target source executed=false、trigger_count=null、not triggered；
source realizability、新 Lean、一般 N45/N2/E closure 均未建立。
只新增本review，未修改共享文件、原交付或舊證書；未commit/push/PR。
機讀判定見 [acceptance.json](acceptance.json)，review由 [delivery.json](delivery.json) 封存。
'''
    with (HERE / 'REPORT.md').open('x') as stream:
        stream.write(report)
    print(json.dumps({'accepted_claims': 9, 'correction_cells': 112, 'newly_excluded': 7, 'remaining': 14}))


if __name__ == '__main__':
    main()
