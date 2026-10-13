# 2026-09-29：t_w=0,(2,2) 缺額型的飽和分量與雙列分離

Git 基準 `f29b899`，工作目錄為專案根目錄。承接使用者「繼續推進」，
沿 HANDOFF 固定 t_z=2,(2)、t_w=0,(2,2)、D_w=1、O_w=0 的 96 份原資料。
保留進場既有未提交成果及原 scripts／artifacts；未 commit／push。
新增 [checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py)、
[JSON／支援表](../../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_pairs/support_table.md)、
[報告](../c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)，接回出口第九類及文件入口。

## 結果

| 項目 | 數量 |
| --- | ---: |
| 原有序資料，(1,2)／(2,1) 各半 | 96 |
| 兩算法一致的 actual supports／placements | 910／910 |
| rotation 模板／六接點方向核對 | 12／7,280 |
| 原有支援／空纖維 | 54／42 |
| 必要支援／source K5 排除／保留 | 364／340／24 |
| 排除後仍非空的原資料纖維 | 16 |
| 完整搬運／搬運加容量上界／target K5 查詢 | 24／16／8 |
| 完整 target joins／原失敗候選 | 640／8 |
| target 全接受／未決 | 48／0 |
| source 反射／字面 target 反射 | 364／48 |
| 完整分量交換／root 色對交換 | 364／1,004 |
| 原接線 K5 skeleton controls／負控制 | 1,812／13 |

所有 target 失敗候選均是 same_singleton，均由 source 飽和分量的 target pair
原路徑反駁；無需第三禁色、singleton 首橋、跨列 pair 聯立或新 palette 交換。
source 340 份排除與 target 8 份候選反證分開記錄。

重新窮盡全部 65,535 份非空二元關係，驗 380 份 singleton schemas 及
6 份完整交換 pair schemas；各支援保存逐 tuple 穩定子。各 minor skeleton
保留三原分量、六接點、兩 spokes、zw 及實際支援；它們不是 degree-list
來源實現。任意大小化約是紙面論證，外部 degree-list 講義 Lemma 7／Theorem 10
本輪重讀核對，來源連結見報告。未新增 Lean theorem。

## 範圍更新

新 JSON 的 coverage_extension 綁定前輪 [範圍表](../c5_exchange_geometry_scope.md)
及原 no-mixed 資料，加入本型正反向 192 個 IDs，與原 552 份互不相交。
現為四種 root 交換型／744 份原接合已覆蓋；11 種／2,804 份仍開放。
未改寫前輪 snapshot checker／artifacts。一般 A 完備性、完整 Σ、共同出口及
K∞=K≤5 仍未證；出口新增本型仍明用來源雙缺失與刪邊繼承。

## 本輪驗證

以下七個 checker 的嚴格 `--check` 均通過；新 checker 另重播舊 (2,2)
數學內容及生成表，文件 SHA 的差異另列於下，不記為舊嚴格檢查通過。
`lake build` 通過（8,827 jobs，既有 linter warnings），未新增 Lean 檔。
文件檢查通過：303 份 Markdown／3,229 個本地連結；DocGraph 通過：
61 文件／206 關係／5 families，0 errors／notes。HANDOFF 149 行，
`git diff --check` 通過。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

另外實際執行 `python3 scripts/c5_single_spoke_two_two.py --check`，回報
`certificate differs`。重算後只有最上層 `inputs` 改變，唯一差異為
`docs/c5_single_spoke_cores.md` 的 SHA；全部數學 payload 與生成支援表相同。
新 JSON 的 `legacy_two_contact_replay` 保存舊／新 SHA、原 artifact SHA、
數學 payload digest 及兩項相等結果；新 checker 每次會重新完整核對。
該文件不在本輪修改範圍，舊 artifacts 保持；沒有以改寫舊證書掩蓋 provenance 差異。

未單獨重跑 t2／t2-t1 endpoints 完整鏈、path-palettes、其他 mixed／唯一
degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。
新 checker 引用或範圍 checker 重算的局部規則，與單獨重播整份 checker 分開。

## 停止點

本型已完成，48 查詢全證。下一型為 t_z=2,(2)、t_w=0,(2,2)、D_w=0、O_w=1：
96 份，首項 retained-join ID=3040、sides=(133,30)，B_z=01、F_Cz={2}，
w 禁色=({0,1},{0,2})、c=3。兩個 pair 都有自己的原完整 relation／bridge 路徑。
本輪只讀取該入口 IDs，未宣稱其支援或 target 已遍歷；優先序見 [HANDOFF](../HANDOFF.md)。
