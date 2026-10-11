#!/usr/bin/env python3
"""Create the fresh, evidence-bound q0 acceptance; never update prior results."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q0-restore'
OLD = REPO / 'audits/2026-10-11-n45-s-long-s-review'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def write(name, obj):
    with (HERE / name).open('x') as stream:
        stream.write(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def main():
    checks = read(HERE / 'checks.json')
    algebra = read(HERE / 'logs/independent-algebra.stdout.log')
    custody = read(HERE / 'logs/independent-custody.stdout.log')
    assert checks['checks_pass'] and algebra['status'] == 'independent arithmetic passes'
    assert custody['status'] == 'independent custody checks passed'
    assert custody['target_delivery']['sha256'] == checks['reviewed_delivery_sha256']
    extra = read(HERE / 'extra-authority-inputs.json')['inputs']
    paper_extra = read(HERE / 'paper-extra-authority-pins.json')['additional_base_pins']
    for item in paper_extra:
        frozen = next(record for record in extra if record['path'] == item['path'])
        assert all(item[k] == frozen[k] for k in ('base', 'bytes', 'git_blob', 'sha256'))
        assert pin(HERE / frozen['frozen_path'])['sha256'] == item['sha256']

    before = read(OLD / 'remaining-schedules.json')
    assert before['counts'] == {'raw': 28, 'remaining': 24, 'restoration_excluded': 4}
    selected = {(941, (0, 2, 3)), (941, (0, 2, 4)), (933, (0, 2, 3, 4))}
    new_excluded, remaining = [], []
    for row in before['remaining_schedules']:
        key = (row['SigmaG_orbit'], tuple(row['QG']))
        if row['t_s'] == 2 and row['beta_q'] == 0 and key in selected:
            row = copy.deepcopy(row)
            row.update(restoration_excluded=True,
                       reason='original q1 acceptance forces beta S r=2 empty; q2 all full X lifts restore original rb4',
                       restored_Delta_rows=[2],
                       adoption_authority='acceptance.json in this fresh q0 review')
            new_excluded.append(row)
        else:
            remaining.append(row)
    assert len(new_excluded) == 3 and len(remaining) == 21
    assert all(not (r['t_s'] == 2 and r['beta_q'] == 0) for r in remaining)
    assert sum(r['t_s'] == 1 for r in remaining) == 14
    assert sum(r['t_s'] == 2 and r['beta_q'] == 2 for r in remaining) == 7
    ledger = {
        'base': BASE,
        'scope': 'Necessary schedules only, under the complete inherited K1-K12 U-owner-s/X-own-beta contract; not actual sources',
        'previous_ledger': pin(OLD / 'remaining-schedules.json'),
        'new_worker_delivery': pin(TARGET / 'delivery.json'),
        'counts': {'raw': 28, 'previously_remaining': 24, 'newly_excluded': 3,
                   'total_excluded': 7, 'remaining': 21, 'remaining_schedule_spoke_combinations': 35},
        'excluded_schedules': before['excluded_schedules'] + new_excluded,
        'newly_excluded_schedules': new_excluded,
        'remaining_schedules': remaining,
        'remaining_partition': {'t_s_1': 14, 't_s_2_beta_q2': 7},
        't_s_2_beta_q0_branch': {'status': 'paper excluded within this complete contract and raw schedule domain',
                                'raw_schedules': 7, 'previously_excluded': 4, 'newly_excluded': 3},
        'same_wave_other_deliveries_used': False,
    }
    write('remaining-schedules.json', ledger)

    claims = read(TARGET / 'claims.json')['claims']
    accepted = []
    for claim in claims:
        verdict = 'accepted under complete assigned K1-K12 contract'
        if claim['id'] == 'T2Q0-Q2-RESTORE':
            verdict += '; q2 existence relative to inherited SF-QX/SF-T2-EXTEND/E2 trust chain'
        if claim['id'] == 'T2Q0-CALIBRATION':
            verdict = 'accepted only as bounded abstract interface arithmetic and metadata calibration'
        accepted.append({'id': claim['id'], 'verdict': verdict,
                         'conclusion': claim['conclusion'], 'quantifier': claim['quantifier'],
                         'evidence': ['paper-review.md', 'algebra-review.md', 'checks.json'],
                         'new_source_execution': False})
    assert len(accepted) == 9
    acceptance = {
        'task_id': 'N45-S-LONG-S-T2-Q0-RESTORE-INDEPENDENT-REVIEW', 'base': BASE,
        'status': 'accepted within assigned contract', 'adoption_layer': 'fresh audit review only',
        'reviewed_worker_files': [pin(TARGET / name) for name in ('delivery.json', 'REPORT.md', 'claims.json', 'coverage.json', 'proof-calibration.json')],
        'claims': accepted, 'blocking_findings': [], 'required_corrections': [],
        'schedules_excluded': [{'SigmaG_orbit': orbit, 'QG': list(qg)} for orbit, qg in sorted(selected)],
        'restored_row': {'q': 2, 'literal': '01201', 'original_edge': ['r', 'b4'], 'literal_b4_colour': 1,
                         'all_full_X_lifts_restore': True,
                         'collective_nonempty_pool': [[0, 3], [2, 3], [3, 3]],
                         'individual_pool_fibre_nonempty_claimed': False},
        'contract': {'K': list(range(1, 13)), 'owner': 's', 'U_support': [0, 1, 2],
                     'L_support': [2, 3, 4], 'S_support': [4, 0], 'S_may_have_arbitrary_size': True,
                     't_s': 2, 'beta_q': 0, 'original_s_spokes': [0, 2],
                     'original_r_split': [2, 2], 'original_s_split': [1, 1],
                     't_r': 1, 'retained_r_spokes': [], 'X_is_own_beta_minimal_core': True},
        'inherited_trust_boundary': read(TARGET / 'claims.json')['SF_QX_trust_boundary'],
        'missing_BASE_findings': custody['expected_missing_BASE_blobs'],
        'dependent_finite_replay_executed': False,
        'extra_BASE_authority': extra,
        'checks': {'worker_readonly_native': checks,
                   'independent_algebra': algebra['counts'],
                   'independent_custody': {'payload_files': 76, 'payload_bytes': 1665969,
                                           'target_files': 77, 'recorded_custody_files': 60,
                                           'root_guarded_authority_union': 63,
                                           'input_authorities': {'BASE_blobs': 12, 'sealed_physical_audits': 11},
                                           'dispatch_metadata_pins': 3},
                   'independent_native_records': [read(HERE / f'logs/{name}.command.json') for name in ('independent-algebra', 'independent-custody')]},
        'evidence_layers': {'paper': 'three arbitrary-size necessary schedules excluded under assigned contract and inherited dependencies',
                            'finite_calibration': 'three abstract column cases, two transports, 480 metadata pins; no actual graph assignments',
                            'target_source': {'executed': False, 'status': 'not triggered', 'trigger_count': None},
                            'source_realizability': 'not established', 'Lean': 'not established',
                            'general_N45_N2_E': 'not established'},
        'scope_exclusions': ['t_s=1', 'beta=q2', 'other cores', 'general U-owner-s exclusion', 'individual q3/q4 restoration'],
        'shared_documents_updated': False, 'old_deliveries_modified': False,
        'commit_push_PR': False,
    }
    write('acceptance.json', acceptance)
    report = '''# N45-S-LONG-S-T2-Q0-RESTORE 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

三份 schedules 933/0234、941/023、941/024 的任意大小紙面排除通過獨立驗收。
九項 claims 在指定完整 K1–K12 範圍採納，無阻斷 finding、無需修正文義。
採納只記在本新 review；原 worker 的 pending bytes 與所有共享文件保持原樣。

## 完整同源證明

範圍是原 U owner=s、U012/L234/pair S40、原 r-split(2,2)、s-split(1,1)、
t_s=2/spokes02、β=q0、X=G−原 rb4，且 X 本身是 β-minimal core。
原 S 及各件的大小、blocks、bridges、旁支不設上界。所有 K1–K12，包括原 G
的逐邊 Σ witnesses 與 X 的逐邊 β witnesses，均保留。

原 actual U 和 spokes 在 β/q1/q2 強制 s=3。直接 complete-degree/contact
list-slack 論證給每個 L/S 完整 forbidden r 欄至多兩色；β 拒絕迫兩欄各二色且
互補。原 S 的 N-diagonal 必要充分介面已對回 BASE E4 及 Phase B B-SD：
原外側連通並具全部所需 B-touch，故 S(β;3,3) 非空、3 不在 S 的禁色欄。
三份原 G 均接受 q1；L 的完整 (0 1) 雙射排除 S 禁色欄={0,1}，迫 β 下 S 禁 r=2。
S 的完整 (1 2) 雙射遂給 q2 的 r=1 fibre 空。雙射作用於每個原 vertex、全部
ordered/shared contacts、tuples 和每個 preimage；空 fibres 與 diagonal 同時保留。

沿用已採納 Q(X)={β}，q2 的完整 X lift 聯集非空。每份 lift 均有 r≠1=q2(b4)，
故全部恢復同一原 rb4；三份原 Q(G) 均拒 q2，逐份矛盾。非空池是
(r,s)=(0,3),(2,3),(3,3) 的聯集，沒有聲稱每個個別 fibre 非空，也未證個別
q3/q4 恢復。完整論證與充分前提核對見 [paper-review.md](paper-review.md)。

q2 存在性明列繼承 SF-QX、SF-T2-EXTEND 與 E2 paper/finite-terminal 信任鏈；
本輪沒有重新證明或重播該历史鏈。q1 存在性直接由原 K2 得到。額外查用的三份
BASE proof 文件已凍結於 `authority/`，含 Git blob/SHA/size pins。

## 獨立校準及 custody

普通與 seed17 原生只讀重播均 exit0，stdout/stderr 逐 byte 相同；兩個指定負控制
均 exit1 且在指定 certificate/coverage 階段拒絕。delivery verifier exit0。
另一份不 import worker 的算術核對涵蓋三欄案例、兩個唯一 s=3 固定的 support
permutations、32 ordered pin maps、三 schedules 的30列/480 pins，其中120
diagonal。這些是 abstract interface arithmetic，沒有 actual source assignments。
詳見 [algebra-review.md](algebra-review.md)、[checks.json](checks.json) 和 `logs/`。

獨立 inventory 核對通過76份 payload/1,665,969 bytes；整樹77個 regular files、
5個 directories，唯一 manifest exclusion 為 delivery.json。無 symlink、special
entry、重複/缺漏/額外 payload 或 hash mismatch。12份 BASE 與11份 sealed
physical audit 權威分列，3份 dispatch metadata pins 相符；60份原 recorded inputs/
舊證書 before/after/live 相等。root另加三份 BASE proof，63份 guarded authority
及整個原 target tree 均零漂移，HEAD/所有 tracked diff 不變。
原16份 metadata-initial/history 已保留，不能替代 final authority。
詳見 [custody-review.md](custody-review.md) 與 native independent-custody logs。

原 delivery SHA256：`920a7161ac5c758dea78c45b9360eb00f81bc6f91ea0c39b45e09723e026b349`。

## 剩餘域與證據界線

前次24份必要 schedules 中僅刪除此三份，剩21份：t_s=1 的14份，以及
t_s=2/β=q2 的7份（35份 schedule/spoke combinations）。前次 q1-restoration
已排另四份，合計排盡原 t_s=2/β=q0 的七份必要 schedules；這個分支只在完整
指定契約與已採纳 Q(X) trust 邊界內閉合。ledger 見
[remaining-schedules.json](remaining-schedules.json)。沒有使用同輪其它新成果。

兩個既有 observations 缺 BASE blob findings 由 git show 再確認，physical/
quarantine 均不補作權威；依賴該 bytes 的 finite replay 未執行，舊19 controls
未重跑。target source executed=false、trigger_count=null、not triggered。
未建立 source realizability、新 Lean 或一般 N45/N2/E closure。

本輪只新增專屬 review 目錄，未改共享文件、原交付或舊證書；未 commit/push/PR。
機讀採納及完整範圍見 [acceptance.json](acceptance.json)，本 review payload 由
[delivery.json](delivery.json) 封存。
'''
    with (HERE / 'REPORT.md').open('x') as stream:
        stream.write(report)
    print(json.dumps({'accepted_claims': 9, 'newly_excluded_schedules': 3, 'remaining_schedules': 21}))


if __name__ == '__main__':
    main()
