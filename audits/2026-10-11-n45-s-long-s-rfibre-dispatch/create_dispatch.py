#!/usr/bin/env python3
"""Create one reviewable, pinned dispatch packet; never alter prior deliveries."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
REVIEW = 'audits/2026-10-11-n45-s-long-s-review/'
FIBRE = 'audits/2026-10-11-n45-s-long-s-fibre/'
SEALED = [REVIEW + name for name in (
    'REPORT.md', 'acceptance.json', 'corrections.json', 'remaining-schedules.json',
    'fibre-paper-review.md', 'direct-paper-review.md', 'delivery.json')]
SEALED += [FIBRE + name for name in ('REPORT.md', 'claims.json', 'obligations.json', 'delivery.json')]
BASE_PATHS = [
    'audits/2026-10-10-n45-s-long-contract/REPORT.md',
    'docs/c5_excess_two_nonadjacent_unit_core45.md',
    'docs/c5_degree5_interfaces.md', 'docs/c5_degree5_tree_components.md',
    'docs/c5_single_spoke_two_two.md', 'docs/c5_single_spoke_branch_palettes.md',
    'docs/c5_single_spoke_cross_row.md', 'docs/c5_single_spoke_frame_arc.md',
    'docs/c5_single_spoke_two_two_minor.md', 'docs/c5_single_spoke_residual_locality.md',
    'docs/c5_two_spoke_nonadjacent.md', 'docs/c5_multi_odd_cycles.md',
]
EXPECTED_DELIVERIES = {
    REVIEW + 'delivery.json': 'ed08e905575228cf86e839f91fc419f58b552eead0b7f2c461f7db9d4b6cb41b',
    FIBRE + 'delivery.json': '5ef4df9be39637f68bde661d2b724eb9ab7671754dea588938093e76abced0ab',
}


def write(name, raw):
    path = HERE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw.encode() if isinstance(raw, str) else raw)


def write_json(name, data):
    write(name, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def pin(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def verify_sealed_deliveries():
    for name, expected_sha in EXPECTED_DELIVERIES.items():
        path = REPO / name
        raw = path.read_bytes()
        assert sha256(raw).hexdigest() == expected_sha, 'reviewed delivery changed'
        manifest = json.loads(raw)
        assert manifest['base'] == BASE
        folder = path.parent
        names = set()
        for item in manifest['files']:
            assert item['path'] not in names
            names.add(item['path'])
            assert pin((folder / item['path']).read_bytes()) == {k: item[k] for k in ('bytes', 'sha256')}
        exclusions = {item['path'] for item in manifest['metadata_exclusions']}
        assert exclusions == {'delivery.json'}
        assert not names & exclusions
        actual = set()
        for item in folder.rglob('*'):
            assert not item.is_symlink()
            if item.is_file():
                actual.add(item.relative_to(folder).as_posix())
            else:
                assert item.is_dir()
        assert actual == names | exclusions


COMMON = """## 共同契約、權威與工作界線

工作目錄 `/home/ray/developer/ai/math`。本輪 Git BASE 固定為
`f2692089ad4259808e27d9b7e882ac09505b180a`；舊報告內的較早 BASE 是歷史 provenance。
派工包 `audits/2026-10-11-n45-s-long-s-rfibre-dispatch/` 的 `input-pins.json`
列出 BASE Git blobs 與另行封存 audit 輸入，副本分存 `authority/base/`、`authority/sealed/`。
已驗收 review 尚未 tracked；它的 SHA256 是權威 pin，**不得偽稱 BASE blob**。
工作開始先只讀核派工包：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-rfibre-dispatch/check_dispatch.py --check
```

先讀 frozen long-contract §1 的 **K1–K12 全部條款**、已採納 review 的 REPORT／acceptance／
corrections／fibre-paper-review、原 B REPORT §§2–9 與 obligations。
原 B pending 欄位保持歷史 bytes，採納範圍依 review 及 corrections；沿用
`12+4+10+4` query 分類及 SF-RESIDUAL 的恢復引理依賴補列。

本輪只續攻 **U owner=s、原 pair S、原 r-split `(k_L^r,k_S^r)=(2,2)`**。
用一次共同 whole-source normalization 保留 actual U012／L234／S40、原 e=rb4、t_r=1；
X 無 retained r-spoke，actual H_X−s 的完整兩分量 C=`{r}∪L∪S` 與 U 都保留。
r 在 C 上完整 degree4，incident 兩 odd-cycle blocks；任意大小原 pieces、bridges、旁支無上界。
G 仍是具名 ordered induced-C5 disk、完整 Σ=933/941 或全圖 D5 像、ε=2、非相鄰原
degree5 r/s、其餘有效內點完整 degree4、原 H 連通且 full B-touch、原 pieces 恰 U/L/S。
自由孤立內點保完整染色因子，S 不是預設單頂點。
**X=G−e=M 本身**須是固定原拒列 β 的 inclusion-minimal core：每條 retained 非框邊有
同一 β 的 X−f 完整 witness。G 自己的 Σ-critical witnesses 另留，各邊列可不同。

保留同一原圖、同一色框、ordered／shared contacts、actual attachments／supports、ownership、
rotation、bridges、原 edges，以及全部 assignments、tuples／preimages、空 fibres、完整 lifts。
共同十列依序是 `01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`；
q0=01212、q1=01202、q2=01201、q3=01021、q4=01012。
每列保全部16 ordered `(r,s)` pins、diagonal 與 empty cells。原 e 的恢復条件為
`r≠γ(b4)`：q0/q1/q4 的字面色為2，q2/q3為1；T4 列同樣按字面核，不能借未用色。
目前 24 schedules 是必要域，不是來源圖數，不計完整幾何或 t_s=1 的 spoke 變體。

紙面任務 A/B/C 的目標是：對 assigned domain 中**每個符合契約的原來源**，證至少有一個
`γ∈Δ=Q(G)−{β}` 及 ordered pins `(a,b)`，使完整 `L_X(γ;a,b)` 非空且
`a≠γ(b4)`，同步接合 actual C/U 全 preimages 並恢復原 rb4；或直接在同一來源抽取完整
source-minor 矛盾。每個 schedule 一個 Δ 列即可，不要求所有 Δ 列都能恢復。
X 已接受 γ、r 投影非空、鄰列延拓或另一來源的方便 witness 都不足以證 G 接受 γ。
若新增充分前提，須具名標為 conditional，不能宣稱原 assigned domain 全排。

各任務獨立開始，不等待／引用同批其它 worker 的新結論；共用上輪已驗收資料即可。
只新增自己的專屬輸出目錄；若已存在則停下回報 collision，不覆寫。
不得修改共享 docs、原任務交付、舊證書、其他 worker 目錄；不 commit／push／PR，
不發外部訊息。成果全部標 **待獨立驗收**。
缺 `artifacts/c5_no_spoke_exterior/observations.json` 或
`artifacts/c5_single_spoke_residual_locality/observations.json` 的 BASE blob 時保留 finding，
停止依賴該 blob 的有限重播，紙面部分可繼續；physical／quarantine 不替代 BASE 權威。
不重跑上輪19 controls，不作無上限新圖枚舉，不以 zero triggers 宣稱來源排除。

基本交付 `REPORT.md`、`claims.json`、`inputs.json`、`coverage.json`、`delivery.json`。
每個 claim 明列量詞、前提、結論類型、依賴與原 e／r 座標；inputs 分 BASE blobs、封存 audit
SHA256、外部 theorem pins。coverage 列所有 assigned schedule／spoke 變體、完整 Δ、
已證恢復列或 minor、精確 OPEN fibres。未建立 actual source 時不捏造 relations／preimages 數值。
若跑有限控制，先固定具名輸入及上限，保存全部原生 commands／stdout／stderr／exit，
普通／seed17只讀重播一致，負控制與失敗證書保留，輸入／舊證書前後零漂移。
分列紙面、finite calibration、target source、source realizability、Lean、一般 N45/N2/E；
controls 用 `triggered and holds`／`not triggered`／`counterexample`，未執行的 target source
用 executed=false／trigger_count=null。
若未全解，交最小具名 residual、必要空 fibre 與卡住的引理；抽象 relation 反例只否定
該引理，不能稱滿足 K1–K12 的來源反例。完成窄域證明或精確 residual 後停止並交付。
"""


def schedule_key(s):
    return (s['t_s'], s['beta_q'], s['SigmaG_orbit'], tuple(s['QG']))


def schedule_table(schedules, include_beta=False):
    headings = ['Σ orbit', 'Q(G)'] + (['β'] if include_beta else []) + ['Δ', '真來源全部 X lifts 所需 r']
    lines = ['| ' + ' | '.join(headings) + ' |', '| ' + ' | '.join('---' for _ in headings) + ' |']
    for s in sorted(schedules, key=schedule_key):
        values = [str(s['SigmaG_orbit']), ''.join(map(str, s['QG']))]
        if include_beta:
            values.append('q' + str(s['beta_q']))
        values.extend([','.join('q' + str(i) for i in s['Delta']),
                       '；'.join('q' + str(i) + '→' + str(s['all_Delta_X_lifts_required_r'][str(i)])
                               for i in s['Delta'])])
        lines.append('| ' + ' | '.join(values) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip() == BASE
    assert not subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=REPO)
    verify_sealed_deliveries()
    pins = []
    for name in BASE_PATHS:
        raw = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=REPO)
        assert (REPO / name).read_bytes() == raw
        frozen = 'authority/base/' + name
        write(frozen, raw)
        pins.append({'path': name, 'authority': 'BASE Git blob', 'base': BASE,
                     'git_blob': subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=REPO, text=True).strip(),
                     'frozen_path': frozen, **pin(raw)})
    for name in SEALED:
        raw = (REPO / name).read_bytes()
        frozen = 'authority/sealed/' + name
        write(frozen, raw)
        pins.append({'path': name, 'authority': 'sealed audit physical SHA256',
                     'git_blob': None, 'included_in_BASE_claimed': False,
                     'frozen_path': frozen, **pin(raw)})
    write_json('input-pins.json', {'base': BASE, 'inputs': pins, 'sealed_deliveries': EXPECTED_DELIVERIES,
                                  'missing_BASE_blobs_not_admitted': True})
    remaining = json.loads((REPO / (REVIEW + 'remaining-schedules.json')).read_bytes())['remaining_schedules']
    assert len(remaining) == 24
    a = [s for s in remaining if s['t_s'] == 1]
    b = [s for s in remaining if s['t_s'] == 2 and s['beta_q'] == 0]
    c = [s for s in remaining if s['t_s'] == 2 and s['beta_q'] == 2]
    assert (len(a), len(b), len(c)) == (14, 3, 7)

    descriptions = [
        ('A', 'N45-S-LONG-S-T1-RFIBRE', '2026-10-11-n45-s-long-s-t1-rfibre', 'TASK_A_T1.md', a,
         't_s=1 的完整同源原邊恢復',
         """原 profile `(t_s,m_s,n_U)=(1,2,2)`；原 s-spoke b0／b2 兩變體都保留。
已採納 `F_C(β)={1},F_U(β)={2,3},Q(X)={β}`。
β=q3 七個、β=q4 七個，共14 schedules；每個乘兩個 spoke，共28個 schedule×spoke 查詢。

**具名入口 T1-P22：** β=q3=01021、Q(G)=013、s-spoke b0 或 b2。
Δ={q0=01212,q1=01202}；真來源要求兩列全部 X lifts 都 r=2。
須在至少一列找完整 r∈{0,1,3} lift，或給原 source-minor 矛盾。
BASE 鄰列 q2/q4 本已被 G 接受，不能直接反證這份 schedule。

可探索 frozen degree-list tightness／block palettes、private release、branch-palettes 的 rooted
palette 唯一性／色守恆、single-spoke cross-row 及 frame-arc／two-two minor。
每次使用拒絕 palette 都須從當前實際列核其前提，不能把 β 證書直接改名。
不得把 q4 七 schedules 未經整圖、Q(G)、β、原 e 與 r pins 的共同搬運便稱 q3 對稱像。

力求覆蓋下表全部14×2；部分進展也逐項列 remaining domain，保任意大小量詞。
"""),
        ('B', 'N45-S-LONG-S-T2-Q0-RESTORE', '2026-10-11-n45-s-long-s-t2-q0-restore', 'TASK_B_T2_Q0.md', b,
         't_s=2、β=q0 的三個剩餘 schedules',
         """原 profile `(t_s,m_s,n_U)=(2,2,1)`；原 s-spokes b0,b2；β=q0=01212。
已採納 `F_C(β)={3},F_U(β)={1},Q(X)={β}`；只負責剩餘三 schedules。

**具名入口 T2-P22：** Q(G)=024。Δ=q2=01201 須找完整 r≠1 lift，
或 Δ=q4=01012 須找完整 r≠2 lift。若證任意契約來源的 q2 恢復，即覆蓋三 schedules；
q3／q4 的部分恢復須按下表列實際覆蓋。

已採納 q0→q1 完整恢復可作已知引理，但這三 schedules 的 q1 都原已接受，
**重證 q1 不算本任務的原拒列突破**。可研究原兩 odd-cycle palettes、actual L/S pinned
assignments 跨列搬運、原 C 的虛擬五邊框或保 r/s 的 source-minor。
surviving s=3 的虛擬框是四色；不能套三色 singleton theorem，亦不能自行假設繼承 T4。
"""),
        ('C', 'N45-S-LONG-S-T2-Q2-RESTORE', '2026-10-11-n45-s-long-s-t2-q2-restore', 'TASK_C_T2_Q2.md', c,
         't_s=2、β=q2 的七個剩餘 schedules',
         """原 profile `(t_s,m_s,n_U)=(2,2,1)`；原 s-spokes b0,b2；β=q2=01201。
已採納 `F_C(β)={3},F_U(β)={1},Q(X)={β}`；只負責七 schedules。

**獨立具名入口 T2-Q2-P22：** Q(G)=024，Δ={q0=01212,q4=01012}。
須在同一原圖證至少一列有完整 r≠2 lift。q0 在五份 Δ、q4 在五份 Δ；兩列的完整
恢復引理聯集可覆蓋全部七 schedules，但仍須逐項證來源與 pin 前提。

本任務 β 身份是 q2，**不繼承以 q0 作拒絕 β 的 q0→q1 恢復**。
優先獨立推導 q2→q0／q2→q4 的 full-fibre 搬運與原 e 恢復；也可給同源 source-minor。
逐附件核 L234／S40／U012 的 literal queries、pins、shared-contact constraints，不能只交
X 接受、端點 marginal 或丟 r 的 projection。四色虛擬框界線與任意大小旁支同樣保留。
"""),
        ('D', 'N45-S-LONG-S-BLOCK-TRANSFER', '2026-10-11-n45-s-long-s-block-transfer', 'TASK_D_TRANSFER.md', [],
         '原 C block-tree 的完整 assignment／r-fibre transfer',
         """這是三份 paper 任務的獨立輔助工作，不負責任何 schedule 的來源排除，不必等 A/B/C。
任意大小 recurrence 的正確性只依 actual block decomposition 與字面附件；
K11/K12 是提升成來源結論時另需的義務，不是該接合恆等式的前提。

1. 寫出任意大小 actual C block-tree 的精確 restriction／union recurrence：原 bridge、任意長
   odd cycle 各有局部規則，在 actual cutvertex 接合全部 assignments。保原 r 上兩 odd-cycle
   blocks、L/S 身份、所有完整 degree4 旁支與 actual B/s attachments。證與 C 所有 proper
   assignments 有雙射，保存各 ordered contact tuple 的全部 preimages、r 色與空 fibres。
   不要求 finite-template compression，不可把存在性或可用色集合當完整介面。
2. 每個共同 literal γ 產生完整 C interface `Λ_C(γ;a,b)`（含避 actual s-contacts 的 pin b），
   全16 pins與空 cells。精確說明何時可接 actual U 全 preimages／s-spoke factors，及原
   rb4 的恢復 filter。若 finite case 未提供 actual U/G，whole-X/G/source coverage 明列未觸發，
   不用抽象 U 代替來源。跨列必出自同一原 C／附件；piece 色搬運返回字面框再接合。
3. 計算前宣告至多8個具名 interface microcases，每個至多11個 C vertices；包含 r 上兩
   triangles、triangle+5-cycle、非根 articulation 的 bridge／odd-cycle 旁支。
   逐點核 `deg_C(v)+|N_B(v)|+1[sv∈E]=4`，包含 r；提供 vertices、original edges、
   attachments、contacts／ownership、L/S、rotation（若未驗 disk topology，明列）。
   若某預宣告 case 不合條件，保存失敗 case／原因，再用新名稱更正；總数仍≤8。
   不將不合條件的圖偷偷刪除後再宣稱覆蓋。
4. 另寫無 transfer/checker imports 的直接原邊枚舉，逐項比全部十列的 assignments、
   tuple/preimage、ambient pins／r fibres及原旁支頂點。case 形狀／degree4不建立Σ-critical
   或 X 同β minimal；未供 K11/K12 完整刪邊 witnesses 時保持 `not triggered`。
5. 指定三個負控制：改一份完整 preimage 的 r 色、刪一個空 ambient fibre、漏一個原旁支。
   驗收器須分別拒絕並指出 named cell／原頂點；留原證書及失敗證書。普通／seed17只讀重播
   一致，authority／舊證書前後零漂移。這些 controls 驗 transfer，不是 target source search。

另交 `transfer-proof.md`、唯讀 checker、independent direct enumerator、`cases.json`、
完整 certificate／negative certificates 與原生命令 logs。基本交付與共同界線照上文。
成功止於任意大小精確 recurrence＋具名介面校準；若較強 cross-row fibre lemma 失敗，
交完整 relation 反例與精確失敗前提，不提升為滿足 K1–K12 的來源反例。
"""),
    ]
    task_records = []
    for label, task_id, slug, filename, schedules, title, body in descriptions:
        output = 'audits/' + slug + '/'
        assert not (REPO / output).exists(), 'worker output collision: ' + output
        write(filename, f'# 任務 {label}：{title}\n\n任務 ID：`{task_id}`。\n'
                        f'專屬輸出：`{output}`。**本輪可獨立並行；成果待獨立驗收。**\n\n'
                        + COMMON + '\n## 本任務精確範圍與目標\n\n' + body
                        + ('\n## 完整 assigned schedules\n\n' + schedule_table(schedules, include_beta=label == 'A') if schedules else ''))
        record = {'label': label, 'task_id': task_id, 'task_file': filename,
                  'output_directory': output, 'research_started_by_dispatch': False,
                  'depends_on_same_round_results': False, 'assigned_schedule_count': len(schedules),
                  'assigned_schedules': schedules}
        if label == 'A':
            record['s_spoke_variants'] = [[0], [2]]
            record['schedule_spoke_queries'] = 28
        if label == 'D':
            record['role'] = 'independent transfer proof/calibration; no schedule-exclusion verdict'
            record['finite_caps'] = {'named_cases': 8, 'C_vertices_per_case': 11}
        task_records.append(record)
    keys = [schedule_key(s) for record in task_records for s in record['assigned_schedules']]
    assert len(keys) == len(set(keys)) == 24 and set(keys) == {schedule_key(s) for s in remaining}
    write_json('tasks.json', {'date': '2026-10-11', 'base': BASE,
                            'batch_id': 'N45-S-LONG-S-RFIBRE-WAVE', 'tasks': task_records,
                            'coverage': {'remaining_schedules': 24, 'paper_partition': [14, 3, 7],
                                         'paper_partition_disjoint_and_complete': True,
                                         'source_realizations_claimed': False}})
    write('TASKS.md', """# N45-S-LONG-S：下一輪全 r-fibre 缺口派工

2026-10-11。以下四個任務可以同時發布，不需要等其他 worker 結果。
每份任務檔都包含完整共同契約、權威 pins、專屬輸出、交付格式及停止點，可各自整份貼出。

| 任務 | 可發布全文 | 精確工作域 |
| --- | --- | --- |
| A | [T1 原邊恢復](TASK_A_T1.md) | t_s=1；14 schedules × b0/b2 两 spoke，共28個查詢 |
| B | [T2／β=q0](TASK_B_T2_Q0.md) | t_s=2、β=q0；3 schedules |
| C | [T2／β=q2](TASK_C_T2_Q2.md) | t_s=2、β=q2；7 schedules |
| D | [完整 block transfer](TASK_D_TRANSFER.md) | 任意大小精確接合＋至多8個具名 interface cases；不分配來源排除 |

A/B/C 無重疊覆蓋剩下24個必要 schedules；D 是可獨立支援三者的工具／紙面介面。
優先攻 q0 的三件與 q2 的七件，T1同時保 b0/b2與兩β身份。全域以 [tasks.json](tasks.json)
保存，不能把必要 schedules 稱來源圖數。

本輪 Git BASE 為 `f2692089ad4259808e27d9b7e882ac09505b180a`。
新採納 review 用另行封存的 physical SHA256，[input-pins.json](input-pins.json)精確區分。
前輪 [驗收報告](../2026-10-11-n45-s-long-s-review/REPORT.md)及更正被 frozen於本派工包。
沒有依賴缺失 observations 的 BASE blob，也不修改前輪交付。

只新增本派工目錄；未啟動四項研究、未更新共享 docs、未 commit/push/PR。
結果返回後，再獨立驗收所交 paper scope／full fibres／finite controls及新增充分前提。
""")
    write_json('preflight.json', {'base': BASE, 'tracked_diff_empty': True,
                                 'sealed_deliveries_exactly_verified': EXPECTED_DELIVERIES,
                                 'BASE_input_count': len(BASE_PATHS), 'sealed_audit_input_count': len(SEALED),
                                 'partition': [len(a), len(b), len(c)],
                                 'worker_output_directories_absent': True,
                                 'research_execution_started': False})
    print(json.dumps({'created_task_files': 4, 'paper_partition': [14, 3, 7],
                      'BASE_inputs': len(BASE_PATHS), 'sealed_audit_inputs': len(SEALED),
                      'original_deliveries_modified': False}, sort_keys=True))


if __name__ == '__main__':
    main()
