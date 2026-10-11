#!/usr/bin/env python3
"""Create independent D acceptance only inside this exclusive review."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-block-transfer'


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    checks = read(HERE / 'checks.json')
    custody = read(HERE / 'logs/independent-custody.stdout.log')
    original = read(HERE / 'logs/independent-original-edges.stdout.log')
    assert checks['checks_pass'] and custody['status'] == 'independent D custody passes'
    assert original['status'] == 'independent D original-edge/interface check passed'
    assert original['target_delivery_sha256'] == custody['delivery']['sha256'] == checks['reviewed_delivery']['sha256']
    for name, fragment in [('r-colour', 'original vertex=r'), ('empty-cell', 'missing ambient cell'), ('missing-branch', 'missing original vertex l2'),
                           ('direct-r-colour', 'original vertex r expected colour'), ('direct-empty-cell', 'missing named cell'),
                           ('direct-missing-branch', 'missing original vertex l2')]:
        assert fragment in (HERE / f'logs/{name}.stderr.log').read_text()
    claims = read(TARGET / 'claims.json')['claims']
    assert len(claims) == 7
    acceptance = {
        'task_id': 'N45-S-LONG-S-BLOCK-TRANSFER-INDEPENDENT-REVIEW', 'base': checks['base'],
        'status': 'accepted scoped paper identities and fixed C-interface calibration', 'adoption_layer': 'fresh exclusive audit review only',
        'reviewed_worker_files': [pin(TARGET / n) for n in ('delivery.json', 'REPORT.md', 'transfer-proof.md', 'claims.json', 'cases.json', 'certificate.json', 'coverage.json')],
        'claims': [{'id': c['id'], 'verdict': 'accepted within stated identity/calibration/inherited-domain scope',
                    'quantifier': c['quantifier'], 'premises': c['premises'], 'conclusion': c['conclusion'],
                    'new_source_exclusion': False} for c in claims],
        'blocking_findings': [], 'required_corrections': [],
        'paper': {'arbitrary_size': True, 'all_original_vertices_edges_and_unary_attachments': True,
                  'actual_vertex_block_incidence_tree_required': True,
                  'parent_attachment_checked_once_at_original_vertex': True,
                  'full_assignments_tuple_preimages_empty_fibres_shared_identity_preserved': True,
                  'TF_X_requires_actual_U_and_all_original_X_edges': True,
                  'TF_RESTORE_tests_same_original_r_and_literal_b4_colour': True,
                  'K11_K12_required_for_source_promotion_not_recurrence': True},
        'independent_original_edge_enumeration': original,
        'independent_custody': custody, 'native_readonly_checks': checks,
        'independent_native_records': [read(HERE / f'logs/{n}.command.json') for n in ('independent-custody', 'independent-original-edges')],
        'inherited_ledger': {'necessary_schedules': 24, 'spoke_combinations': 38, 'symbolic_pin_obligations': 6080,
                             'ledger_is_frozen_prior_scope': True, 'same_wave_exclusions_used': False},
        'new_source_exclusions': 0,
        'named_residual': 'same-source-Delta-restorable-r-fibre-nonemptiness',
        'residual_status_for_D_alone': 'OPEN',
        'failed_case': {'id': 'BRIDGE_BAD6', 'retained': True, 'vertex': 'l0', 'full_degree': 5,
                        'control_state': 'counterexample to degree4 microcase premise; not a target source'},
        'evidence_layers': {'paper': 'arbitrary-size full assignment/fibre/factor/filter identities',
                            'finite_controls': 'four valid C fragments; triggered and holds',
                            'target_source': {'executed': False, 'status': 'not triggered', 'trigger_count': None},
                            'actual_U_or_G_supplied': False, 'disk_embedding_verified': False,
                            'finite_nonempty_isolated_factor_executed': False, 'source_realizability': 'not established',
                            'Lean': 'not established', 'general_N45_N2_E': 'not established'},
        'missing_BASE_findings': custody['expected_missing_BASE_blobs'],
        'old_19_controls_reexecuted': False, 'shared_documents_updated': False,
        'old_deliveries_modified': False, 'commit_push_PR': False}
    with (HERE / 'acceptance.json').open('x') as stream:
        stream.write(json.dumps(acceptance, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    report = '''# N45-S-LONG-S-BLOCK-TRANSFER 獨立驗收

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

D 的七項 claims 通過指定範圍驗收：任意大小完整 assignment/fibre transfer 恆等式、
固定 C-interface 校準及歷史 necessary-domain ledger。無阻斷或需更正項；新增來源排除為0。

## 完整 assignment 恆等式

V-REC/K-REC 在 actual vertex/block incidence tree 展開全部原 vertices、原 bridge與
任意長 odd cycles，逐 vertex 核全部 literal attachments一次。child subtree只在具名
cutvertex 相交且同色；full assignment 的 restriction 與相容 union 互逆，故保全部
tuple preimages、空 ambient cells、diagonal、原 r 色、shared-contact單一座標與旁支。
recurrence 恆等式需 actual decomposition，無 degree4或 K11/K12 前提。

TF-X 的 full factorization 要另外供同一原 actual U與完整 X edges/spokes/contacts；
TF-RESTORE 只核同一原 r與 literal γ(b4) 的原 rb4 inequality。把 fragment升為來源
仍須全 K1–K12，特別是原 G Σ-critical 和 X 同β刪邊 witnesses。
完整逐claim核對見 [D-proof-review.md](D-proof-review.md)。

## 獨立原邊枚舉與 custody

另寫不 import worker 的 original-edge MRV DFS，完全不用 blocks作染色：四有效cases、
40列、1,344份 full assignments、2,560 ambient cells（1,966空）、640 ordered pins、
1,920 spoke-filtered pins及所有 restored preimages逐項與原certificate相等。
五份宣告全部保留；BRIDGE_BAD6 的原 l0完整degree5失敗亦精確保留，非target反例。
三份負控制的單一r色、空cell、原旁支座標刪除均由獨立完整重建核實。

checker與原 independent direct各自普通/seed17均exit0、stdout/stderr byte相同；
三負證書兩套validator共六次均exit1且命中指定原cell/vertex。native捕捉與第三套
獨立枚舉見 [checks.json](checks.json) 及 `logs/independent-original-edges.*`。

獨立custody核170 payload/24,839,641 bytes；唯一排除根 delivery.json。12 BASE與
11 sealed audit authorities對原live、本地與dispatch frozen、BASE blob精確相符。
1204份原protected files及加certificate後1205份全live零漂移，整原樹、HEAD與
tracked diff不變。詳細inventory/pins/findings見 `logs/independent-custody.stdout.log`。
原 delivery SHA：`ee7bd0093a4e244ee0d8c1af65f0ddedd95125861b5816c8dcbb7975aa43e0ed`。

## 採納界線

D 保留其輸入凍結時的24 schedules／38 spoke combinations／6080 symbolic pins；
這是歷史 necessary-domain，沒有使用同輪q0/q2/T1新排除作前提或重寫原ledger。
D本身的 same-source-Delta-restorable-r-fibre-nonemptiness 仍 OPEN；恆等式精確描述
所需完整介面，沒有證任何 Δ 可恢復 fibre 非空，沒有建立 actual U/G。

兩份缺 BASE observations findings 保留；dependent finite replay及舊19 controls未跑。
finite fragment controls為triggered and holds；whole-X/G、target source及非空孤立因子
finite controls為not triggered。BRIDGE_BAD6為degree4前提counterexample。
未建立 source realizability、新Lean或一般N45/N2/E closure；disk topology未驗。
只新增本review，未改原交付、共享文件或舊證書；未commit/push/PR。
機讀採納見 [acceptance.json](acceptance.json)，由 [delivery.json](delivery.json) 封存。
'''
    with (HERE / 'REPORT.md').open('x') as stream:
        stream.write(report)
    print(json.dumps({'accepted_claims': 7, 'new_source_exclusions': 0, 'independent_assignments': 1344}))


if __name__ == '__main__':
    main()
