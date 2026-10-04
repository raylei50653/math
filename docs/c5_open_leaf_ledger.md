# Weak-deletion 開放葉 ledger

2026-10-04，基準 `0b5e00a`。本頁回應一至兩天建立 ledger、觀察開放葉趨勢的工作；
先交付可重算基準，再累積有實際觀測時間的每日樣本。
目前研究入口仍由 [weak-deletion 導覽](c5_weak_deletion_guide.md) 維護。

**後續（2026-10-04，W 合併）：** 依 [D₆ 合併計畫](../audits/2026-10-04-task-d6/scope_history/MERGE_PLAN.md)
新增版本化 ledger [cw-v1](../artifacts/c5_open_leaf_ledger/cw-v1/trend.csv)：在本頁的 C₄ ledger 上套用
[任務 W 的 batch verdict](c5_qcore_shield_budget.md)，階段趨勢為 **3500→3499→3498→3497→0**，
新關閉 0、1、1、1、3497；固定目錄全部 3500 葉閉合，36 cases／140 geometries 無開放。
本頁下文的 C₄ ledger（`ledger.json`、`trend.csv`、10-04 樣本）逐 byte 不變，作為 W 的 predecessor；
若原地覆寫，W 將讀到零開放而無法重播，所以兩版並存。
重算器的 `STAGES` 改為具名規格（C₂–C₄ 為 single），W 為 batch：逐筆核對 leaf ID、verdict 字串、
D₅ scope row 的完整 canonical hash、predecessor leaf pointer 與 certificate hash，並要求 key 集合
**恰等於**當時開放集合；缺 key、重複 key、外來 key、把繼承閉合算成新增四個負控制都被拒絕。
`--dry-run` 只建兩版並列出候選 hash。W 事件的發布 commit 為 `e959125`；
數學依據是紙面定理 C-W＋外部 Gallai＋有限 Python，經 [D₆ 稽核](../audits/2026-10-04-task-d6/REPORT.md)，無 Lean。

## 範圍與計數單位

首批追蹤域是任務 C 的[共鄰端點 P₃](c5_mixed_p3_common_endpoint.md)，
不是整條 weak-deletion 主線的完備案例樹。原 36 個 cases、140 份具名 geometries、
900 個 case-side joins 展開成 **3,500 個互異 `(case, geometry, side_join)` keys**。
每個 key 算一個目錄葉；尚未逐份排除者算開放，包含未稽核、原完整 unary relation
未知及來源實現未知者。開放不表示存在 disk 來源。

目錄樹是 `C → case → geometry → side_join`。case 與 geometry 是分組節點，
不另外加進葉數；同一葉的支援、contact 或 relation 也不另算葉。
這份展開是身份索引，不是新證明的數學分拆。它沒有計入[導覽保留的](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)
較大／多 mixed、更多 incidence、其他 root 結構、逐染色 repair 及一般出口；
**全主線開放葉總數仍未知**。A／B 的 frame 數與本目錄的 key 數不相加。

## 已算出的階段趨勢

| 依賴階段 | 開放葉 | 本階段關閉 | 累計關閉 | 開放 cases | 開放 case-geometries |
| --- | ---: | ---: | ---: | ---: | ---: |
| C0：固定目錄的重建基準 | 3500 | 0 | 0 | 36 | 140 |
| C₂：geometry30／join20 | 3499 | 1 | 1 | 36 | 140 |
| C₃：geometry34／join20 | 3498 | 1 | 2 | 36 | 140 |
| C₄：geometry34／join60 | **3497** | 1 | 3 | 36 | 140 |

三份關閉都限於 `CPP-134-1`，分別由
[C₂](c5_mixed_p3_one_color_ternary_unary.md)、
[C₃](c5_mixed_p3_two_frame_ternary_unary.md)、
[C₄](c5_mixed_p3_two_frame_two_unary.md) 及
[D₅ 精確 scope](../audits/2026-10-04-task-d5/REPORT.md) 支持。
固定目錄淨減 **3 葉（3/3500，約 0.086%）**，沒有整份 case 或 geometry 封閉。
本序列無新葉、拆分或重開事件；初次建目錄不算研究中新增葉。

一般帳務式是 `ΔL = 新葉 + Σ(拆成 k 葉的 k−1) + 重開 − 關閉`。
目前只在固定目錄內觀察到三次關閉，故 `ΔL=−3`。
若後續更改粒度或擴充目錄，必須另建 scope 版本與覆蓋對應；
不可把目錄膨脹、改名或重新正規化當成研究開放葉的增減。

## 最近兩天與每日速度的界線

| 日期（Asia/Taipei） | 同一目錄的可核對開放葉 | 時間證據 |
| --- | ---: | --- |
| 2026-10-03 | 未知 | 沒有同一固定目錄的已存日期樣本 |
| 2026-10-04 | 3497 | C／C₂／C₃／C₄ 與稽核於 `83ca618` 一起發布；本輪另存實際觀測樣本 |

C0 是把目前固定域重播到關閉前的基準，**不是已觀測到的前一天數值**。
C₂→C₃→C₄ 是依賴次序；报告日期都為 10-04，Git 的
`2026-10-04T12:17:13+08:00` 是發布時間，無法還原各項證明完成時間。
因此目前只有階段淨變化，**尚不能估每日下降率、加速度或完工日期**。
待明天取得第二個真實樣本，才比較實際觀測間隔；若未登記新排除，葉數仍為 3497。

## Ledger、來源與證據層

- [完整 ledger](../artifacts/c5_open_leaf_ledger/ledger.json)：176 個分組節點、
  3500 個 stable leaf IDs、精確 key、關閉事件、來源 SHA256／大小與 JSON pointers。
- [階段趨勢 CSV](../artifacts/c5_open_leaf_ledger/trend.csv)：可直接分析或繪圖。
- [第一個實際觀測樣本](../artifacts/c5_open_leaf_ledger/snapshots/2026-10-04.json)：
  含實際時間、當時 HEAD、固定域 hash、完整開放 IDs 與來源 hashes。
- [重算器](../scripts/c5_open_leaf_ledger.py)：標準函式庫，無來源圖枚舉、不執行 producer。

每個葉的 `scope_pointer` 指向 SHA256 綁定的
[D₅ 完整 ledger](../audits/2026-10-04-task-d5/c4/scope_ledger.json) 原列，保存 actual
attachments／supports、original components／ownership、ordered contacts、
共同色框、完整 tuples／root fibres／lifts、bridges 與未知 relation 的界線。
`common_geometry_pointer`、`common_case_pointer` 另指回
[原 C artifact](../artifacts/c5_mixed_p3_common_endpoint/observations.json)。
索引不取代原完整 payload，不自行拼接 marginals、正規化來源或刪除原表。
新 checkout 若缺封存來源，先依[還原說明](../audits/README.md)還原。

這份 ledger 只重播目錄與既有 verdict 的計數，來源排除仍沿用各報告的
任意大小紙面、外部 Gallai 定理、Python 有限控制及既有獨立稽核；
本輪沒有重新證明其拓撲、重跑 producer 或新增 Lean theorem。
`K∞=K≤5`、一般單側／共同出口與 disk 實現未因這份帳目得到新結論。

## 一至兩天的落地與重播

第一天已完成固定域、stable IDs、精確閉合事件、依賴階段趨勢及首個觀測樣本。
第二天使用新檔名追加觀測，再比較同域 IDs。這是後續手動工作入口，未設排程。

```bash
python3 scripts/c5_open_leaf_ledger.py --check
PYTHONHASHSEED=17 python3 scripts/c5_open_leaf_ledger.py --check
python3 scripts/c5_open_leaf_ledger.py --snapshot artifacts/c5_open_leaf_ledger/snapshots/2026-10-05.json
python3 scripts/c5_open_leaf_ledger.py --compare artifacts/c5_open_leaf_ledger/snapshots/2026-10-04.json artifacts/c5_open_leaf_ledger/snapshots/2026-10-05.json
```

10-05 的 snapshot 命令應在該日實際執行，不能預先寫成明天的觀測。
Snapshot 只允許新檔，已有樣本不覆寫；時間來自實際執行時刻。
新排除需先加入具名 producer／獨立 scope verdict，更新重算器的 `STAGES`、
scope 來源及本輪固定數字檢查，再以 `--write` 更新衍生 ledger；舊 snapshot 保留。
比較器拒絕 domain、unit 或完整 leaf-ID 集合不一致的样本，
列出 closed／reopened IDs，按實際觀測間隔計算速度，不外推收斂。

本輪驗證：一般／seed17 的 ledger byte-check、3500-key 全覆蓋／無重複、
三份 producer 的精確身份與 D₅ verdict 一致、同源 case／geometry／role／P₃
tuples 相同；整 case、整 geometry、同 join 跨 geometry 的過寬刪除負控制
分別抓出 149、24、5 個多刪 keys。
另以合成樣本檢查日期比較、三次閉合差、domain drift、重複 ID 及非递增時間；
合成樣本不寫入研究觀測。文件、DocGraph 與 whitespace 檢查亦通過。
未重跑數學 checkers、研究枚舉、Lean build 或 axiom audit；沿用封存證據。

停止於可重算目錄基準及已知階段趨勢；第二個實際日期樣本仍待取得。
研究下一具名入口 `CPP-134-1／geometry35／join20` 保持開放，沒有分析或新增排除。
