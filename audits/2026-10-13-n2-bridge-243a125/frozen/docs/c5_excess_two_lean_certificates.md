# ES 179 個 excess-two crit 代表的 Lean soundness 證書

日期：2026-10-04。狀態：**已完成本固定來源 179/179 張的 Lean soundness 證書；不證枚舉 completeness。**

基準為 `integrate-kprime-e3 @ d00aba4`，完整 HEAD 為
`d00aba4e10ea2d05ab216fedd94f5a166b2777ad`。本任務使用獨立 worktree
`/home/ray/developer/ai/math-task-lc-lean-certs`，branch 為 `task-lc-lean-certs`。
依使用者限制，只新增檔案，不修改既有 checker、報告、文件索引或 `Math.lean`，不 commit／push。
Lean／mathlib 鎖定 `v4.34.0-rc2`，未執行 `lake update`。

來源及證據邊界依 [ES 固定搜尋報告](c5_excess_two_finite_search.md) 與
[DOCUMENTATION](DOCUMENTATION.md)；既有染色語意沿用
[Enumeration](../Math/Enumeration.lean)、[State](../Math/State.lean) 及
[SplitCertificate](../Math/SplitCertificate.lean)。輸出格式參考
[Certificates](../Math/Certificates.lean)、[GeneratedCertificates](../Math/GeneratedCertificates.lean)
及 [既有 exporter](../scripts/export_certificates.py)。目前研究線的入口及停止點見
[Lean 導覽](lean_guide.md) 與 [Kempe 導覽](c5_kempe_guide.md)，本任務的精確停止條件列於本文末。

## 結論範圍與目前驗證階段

本任務針對提供的 179 份 ES `crit_orbits` JSON 建立具名 Lean 證書。
目標結論僅是這些 literal labelled graph 滿足有限結構、完整染色關係、每條非框邊的
嚴格新增列 witness，以及組合 rotation／Euler／外框條件。
179 組 positive／rejected／valid theorem 全部通過，`certificate_count`、
`all_certificates_valid` 及 `all_certificates_sound` 編譯成功。完整 `lake build` exit 0，
總耗時 739.551 秒（約 12 分 20 秒）；生成資料模組耗時約 719 秒。
獨立重跑 558 項 `#print axioms` exit 0，耗時 5.214 秒。

179 是此次輸入檔案的數量；本任務不證明 ES 沒有漏掉圖、不證明 canonical
枚舉耗盡、不證明這些代表彼此屬於不同軌道、不重證 orbit size 或 stabilizer size。
它也不證明任意大小來源分類、ε≥3、一般 boundary-state 定理或 `K∞=K≤5`。
組合嵌入的檢查不提升為 Lean 內的拓撲平面性或 disk drawing 定理。

## 固定來源與 provenance

[新 exporter](../scripts/export_excess_two_certificates.py) 只讀取：

```text
artifacts/c5_excess_two_finite_search/*_validate/crit_orbits/orbit_*.json
```

不使用 `*_fast` 代表、brute summary 或另一份枚舉器給的布林答案作 Lean 前提。
每份輸入的相對路徑、原始 bytes 的 SHA-256、大小、NA／AD／D6 類型、k、原 orbit
名稱及輸出的 Lean definition 名稱保存在
[source_inventory.json](../artifacts/c5_excess_two_lean_certificates/source_inventory.json)。
每份生成資料旁也保留對應 source path 與 SHA。

| 類型 | k 與各 bucket 的代表數 | 小計 |
| --- | --- | ---: |
| NA | k6: 3；k7: 2；k8: 22；k9: 27 | 54 |
| AD | k3: 1；k6: 2；k7: 1；k9: 5 | 9 |
| D6 | k4: 2；k5: 9；k6: 4；k7: 25；k8: 41；k9: 35 | 116 |
| 合計 | k 的範圍為 3..9，n=5+k | 179 |

原始輸入共 815,862 bytes。依排序後的相對路徑順序串接各檔的原始 bytes，再取
SHA-256，固定 corpus digest 為：

```text
ceddd15dff11a97015d7bdac892f6c525ee6233d25d7b3916a96a99e7f02fc4a
```

Python 此輪有限來源稽核實際檢查 1,597 個接受列 witness、193 個拒絕列、4,271 個
刪邊新增列 witness，涵蓋 4,138 條具名非框邊。這些是各代表的總和，不能理解為
不重複圖的計數或搜尋覆蓋定理。接受與刪邊 witness 直接在同一份原圖及指定刪邊圖
逐邊驗證；拒絕列使用 exporter 自己的 literal-frame MRV 回溯檢查。
exporter 不 import ES 實作、不使用 planarity package 或四色定理 oracle。

## Lean 定義及逐張條件

全部新定義位於 `FiveBoundary.ExcessTwo`；生成的具名證書位於其 `Generated`
namespace。所有邊、roots、witness、Q 與 rotation 使用原 JSON 的同一份標號圖，
boundary 始終是 0..4，未個別對元件或 relation 重新正規化。

### 結構、degree 與 Q

[ExcessTwoShape.lean](../Math/ExcessTwoShape.lean) 定義 `DegreeType`、`ShapeConditions`、
`checkShape`、`QConditions` 與 `checkQ`。

`ShapeConditions` 逐項要求：n>5；邊按端點 lexicographic 嚴格排序；每邊 a<b<n；
兩端都在框上的邊恰為 `(0,1),(0,4),(1,2),(2,3),(3,4)`；每個內點的實際 degree
等於指定 profile 且 spokes≤3；degree 超過四的總和恰為二；內部連通；root adjacency
符合標籤；另外明確存在一條 frame-to-interior spoke。

NA、AD 的兩個 degree-five roots 是 5、6，其餘內點 degree four；NA 要求 roots
不相鄰，AD 要求相鄰。D6 的 degree-six root 是 5，其餘內點 degree four。
內部連通檢查從 5 起，以內部邊反覆擴展 visited list 至多 k 次，再要求所有內點都
已到達。`reachInterior_sound`、`connectedInterior_sound` 與
`checkShape_interior_paths` 是普通 Lean 歸納證明，將計算結果轉成 `InteriorPath`：
每次延伸都保存實際 adjacency 與新端點確屬內部範圍的證據。

十個列代表的順序恰為 ES 原順序：

```text
0: 01012    1: 01021    2: 01023    3: 01201    4: 01202
5: 01203    6: 01212    7: 01213    8: 01231    9: 01232
```

`maskAccepts` 與 coloring 模組的 `maskBit` 均使用 `Nat.testBit`；每個 bit 指向同一列。
T4 的索引是 `[2,5,7,8,9]`，mask 為 932。框位置 p 的三色 singleton row 索引依序為
`[6,4,3,1,0]`。`QConditions` 要求 mask<1024、T4 全收、Q 恰等於被拒絕的這五個
具名位置、Q 非空、`c_Q` 恰為 cyclic components，且 `|Q|+c_Q≤4`。
對框的 proper subset，components 定義為 `|Q|` 減去兩端都在 Q 的框邊數；整個框
則定義為一個 component。`t4_indices_exact` 以 `decide +kernel` 檢查固定索引恰為
四色列及 bit mask=932。

### 完整染色關係與刪邊 witness

[ExcessTwoColoring.lean](../Math/ExcessTwoColoring.lean) 沿用既有 `Color = Fin 4`、
`BoundaryColoring`、`graphOfEdges`、`Proper` 與 `Sigma` 語意。
`Extends edges i` 是存在 `inside : Fin k → Color`，使
`Fin.append (boundaryRow i) inside` 通過原圖每條邊的 `edgeCheck`。
其 decidability 窮舉全部 `4^k` 個內部函數；拒絕列沒有從 JSON 的 mask 直接推得。

接受列的 `checkAccepted` 直接檢查所附整圖 coloring 每條邊合法，且 restriction
恰等於指定 boundary row。`checkRow` 對接受 bit 用此 witness，對拒絕 bit 要求
`decide (¬ Extends edges i)`。`extends_iff_sigma`、`accepted_sound` 與 `row_sound`
將這些有限結果接到既有 `Sigma` 中的精確 membership。

`expectedSigma mask` 是所有接受代表的完整 S4 color orbit 的聯集。
`rows_exact_sigma` 用**一次全圖共同色置換**把十列的精確 membership 提升為完整
raw `Sigma = expectedSigma mask`；沒有使用 D5 去合併框位置，也沒有獨立正規化
元件。此普通證明使用既有 `Enumeration.color_orbits_cover`，後者由 `native_decide`
證明，因此完整 raw Sigma 的結論繼承該既有 native 信任邊界。

對每條具名非框邊，`DeletionWitness` 保存原 edge 及其新增列 coloring。
`checkDeletion` 要求該 edge 真正在原圖、至少有一個 witness、每個 witness 的原 mask
bit 被拒絕，並直接通過指定 `G-e` 的接受檢查。
`DeletionsCover` 要求每條非框邊都有對應 witness record。`deletion_sound` 將其提升為
某個 b 屬於 `Sigma(G-e)` 而不屬於 `Sigma(G)`，故新增至少一列。
本任務不把刪邊 JSON 的整個 `sigma_mask` 視為已在 Lean 重證的完整刪邊關係；
Lean 所證的是任務要求的嚴格新增列及實際 coloring。

### 組合 rotation、face partition 與 Euler

[ExcessTwoRotation.lean](../Math/ExcessTwoRotation.lean) 定義 `RotationData` 與
`RotationValid`。資料取自原圖的 `embedding.disk_rotation`；exporter 由其 predecessor
rule 算出全部 face walks，再把 rotation、faces、原 outer face 一起交給 Lean。
Lean 不採信 Python 的「已 planar」旗標或 face 數答案。

`RotationValid` 要求每個 clockwise neighbour ring 恰為原圖鄰點且無重複；每條
無向邊的兩個 directed darts 恰由所有 face walks 分割一次；每一步從 `(u,v)` 到
`(v,w)`，其中 w 是 v 的 clockwise ring 中 u 的前一點；每個 face walk 閉合；
`n+F=E+2`；指定 outer face 恰為 `[0,1,2,3,4]` 或其反向，且確實是所列 face
之一，允許循環起點移動。結合 shape 的內部連通、frame C5 與明確 spoke，使這份
rotation 證書適用於所述 connected literal graph。

`checkRotation_sound` 是從 `decide` 結果抽取 `RotationValid` 的普通證明。
此條件證明**存在組合嵌入**；Lean 中沒有把它轉成拓撲平面嵌入、平面 drawing 或
圓盤外邊界的定理。Face walks 可以重複頂點（例如 bridge），但不能重複 directed dart。

### 共同 checker 與 soundness

[ExcessTwoCertificates.lean](../Math/ExcessTwoCertificates.lean) 的 `Certificate`
保存 k、literal edges、degree kind、mask、Q、components、rotation、接受列 coloring
及刪邊 witness。`StructureConditions` 結合 shape、Q、rotation、既有的
`boundaryIsCycle` 與 `DeletionsCover`。

`checkPositive` 檢查全部結構、接受列與刪邊 witness；`checkRejected` 只處理拒絕列。
`check_from_parts` 是普通證明，將這兩部分組合為 `check c = true`。

`check_finite_sound` 的普通證明得到 `FiniteCertificateFacts`：全部結構條件、十個
**exact representatives** 的精確 Sigma membership，以及每條非框邊的實際新增列。
這個 soundness theorem 沒有使用 native 的 S4 cover。
`check_sound` 的證明本身同樣是普通 Lean 證明；其結論 `CertificateFacts` 另外包含
完整 raw Sigma equality，因此繼承前述 `color_orbits_cover` 的 native 公理。
這兩層結論與各張證書的計算證明必須分開閱讀。

## 證據層與公理稽核

[GeneratedExcessTwoCertificates.lean](../Math/GeneratedExcessTwoCertificates.lean) 對每份來源
產生 `cert_<kind>_k<k>_orbit_<index>` 及三個具名 theorem：

| theorem | 方法 | 意義／信任邊界 |
| --- | --- | --- |
| `<cert>_positive` | `decide +kernel` | 結構、rotation、接受列與全部刪邊 witness，由 kernel reduction 檢查 |
| `<cert>_rejected` | `native_decide` | 對拒絕列窮舉內部函數；另含 Lean native compiler 信任 |
| `<cert>_valid` | 普通 `check_from_parts` | 以兩個已證結果組合；繼承該張 rejection 的 native 公理 |
| `check_finite_sound` | 普通 Lean 證明 | reusable implication 不增加 native 計算；具體套用仍繼承輸入證書的 native 公理 |
| `check_sound` | 普通 Lean 證明 | 完整 raw Sigma 層額外繼承既有 S4 cover 的 native 公理 |

`certificate_count` 用 `decide +kernel` 證明生成 list 長度為 179；
`all_certificates_valid` 以逐張具名 theorem 組合；`all_certificates_sound` 以普通 theorem
取得每個 list member 的 `CertificateFacts`。此 list 長度不建立 distinctness 或搜尋 completeness。

[ExcessTwoCertificatesAudit.lean](../Math/ExcessTwoCertificatesAudit.lean) 使用 `#print axioms`
實際列出普通 helpers、既有 `edgeCheck_exact`／`color_orbits_cover`、三個 aggregate
theorem，以及每張的 positive／rejected／valid，逐張共 537 項。
普通標準公理（例如 `propext`、`Quot.sound`）與 native 計算公理依實測輸出分開記錄；
不能只因 tactic 寫成普通 proof 就稱整個 theorem 沒有 native 依賴。

實際完整輸出保存於 [axioms.log](../artifacts/c5_excess_two_lean_certificates/axioms.log)，
逐 theorem 公理清單及計數保存於
[axiom_summary.json](../artifacts/c5_excess_two_lean_certificates/axiom_summary.json)。
以下為原輸出的關鍵結果（保留 Lean 當前 namespace 下顯示的 native 公理名稱）：

```text
'FiveBoundary.ExcessTwo.check_from_parts' depends on axioms: [propext, Classical.choice, Quot.sound]
'FiveBoundary.ExcessTwo.check_finite_sound' depends on axioms: [propext, Classical.choice, Quot.sound]
'FiveBoundary.ExcessTwo.check_sound' depends on axioms: [propext,
 Classical.choice,
 Quot.sound,
 color_orbits_cover._native.native_decide.ax_1]
'FiveBoundary.ExcessTwo.checkShape_sound' does not depend on any axioms
'FiveBoundary.ExcessTwo.checkQ_sound' depends on axioms: [propext]
'FiveBoundary.ExcessTwo.checkRotation_sound' depends on axioms: [propext, Quot.sound]
'FiveBoundary.ExcessTwo.Generated.certificate_count' depends on axioms: [propext]
```

558 項稽核全部完成：普通 helpers／既有基礎 18 項、aggregate 3 項、逐張 537 項。
179 個 `_positive` 全部只含 `[propext, Classical.choice, Quot.sound]`，沒有 native 公理；
每個 `_rejected` 與 `_valid` 除標準公理外，恰有該張的
`<cert>_rejected._native.native_decide.ax_1` 一個 native 公理。
`all_certificates_valid` 共 182 個公理，為三個標準公理及 179 個獨立 rejection 公理；
`all_certificates_sound` 共 183 個公理，再加既有 S4 cover 的一個 native 公理。
完整稽核沒有 `sorryAx`。

因此 finite soundness implication 本身是普通證明；179 張具體結論的拒絕列仍然需要
native compiler 信任，完整 raw Sigma 結論另繼承既有 S4 cover 的 native 信任。
Python exporter 的 MRV、SHA 與 face 生成並不是 Lean 結論的公理前提。


## 產物、重播與實測紀錄

來源與產物入口：

- [exporter](../scripts/export_excess_two_certificates.py)：新 checker，以 exclusive-create 新建；生成三份輸出均使用 exclusive-create。
- [source inventory](../artifacts/c5_excess_two_lean_certificates/source_inventory.json)：179 份原始 SHA、桶數、corpus SHA、輸出 SHA 與固定域稽核範圍。
- [generation.json](../artifacts/c5_excess_two_lean_certificates/generation.json)：首次生成的實際命令、stdout、exit code 與耗時。
- [lake_build.log](../artifacts/c5_excess_two_lean_certificates/lake_build.log) 與 [lake_build.json](../artifacts/c5_excess_two_lean_certificates/lake_build.json)：完整 build 輸出、exit 0 與 739.551 秒耗時。
- [replay.json](../artifacts/c5_excess_two_lean_certificates/replay.json) 與 [seed-17 replay](../artifacts/c5_excess_two_lean_certificates/replay_hashseed17.json)：三份產物逐 byte 相同，均 exit 0。
- [axioms.json](../artifacts/c5_excess_two_lean_certificates/axioms.json)：獨立公理稽核命令、exit 0 與耗時。
- [validation.json](../artifacts/c5_excess_two_lean_certificates/validation.json)：必要命令、文件診斷與 Git exit codes 的本輪彙整。

生成的資料檔為 722,131 bytes，稽核 Lean 檔為 24,840 bytes，inventory 為 60,093 bytes；
三份均小於 1 MB，無需登錄大型產物。其 SHA 精確值以 inventory 為準。
本輪交付的 log／公理摘要也均低於 1 MB，未修改 MANIFEST 或 .gitignore。
建置使用主 checkout `.lake` 的獨立複製，沒有與其他任務共寫 `.olean`；
沒有重建或改寫原 ES 來源證書。

以下命令在本 worktree 根目錄執行。首次生成只適用於三份輸出尚不存在時；
已有輸出用 `--check`，不刪除既有檔案以配合生成。

```bash
cd /home/ray/developer/ai/math-task-lc-lean-certs

# 首次生成（exclusive-create；本輪已執行）
/home/ray/developer/ai/math/.venv/bin/python scripts/export_excess_two_certificates.py

# 日常只讀逐 byte 重播；同時重稽核相同固定來源
/home/ray/developer/ai/math/.venv/bin/python scripts/export_excess_two_certificates.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python scripts/export_excess_two_certificates.py --check

# Math.lean 保持原樣，因此顯式指定兩個新增 target
taskset -c 0,1,2,3,4,5,6,7 lake --no-cache build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit

# 獨立重跑所有 #print axioms（不重跑已編譯的證書計算）
taskset -c 0,1,2,3,4,5,6,7 lake env lean -j 1 Math/ExcessTwoCertificatesAudit.lean

# 文件與 diff 檢查
/home/ray/developer/ai/math/.venv/bin/python scripts/check_docs.py
/home/ray/developer/ai/math/.venv/bin/python tools/docgraph check
git diff --check
```

`--check` 在記憶體重建三份 outputs，重新稽核 179 份輸入，逐 byte 比較全部三份檔案，
不會寫入 outputs。`PYTHONHASHSEED=17` 的相同重播另驗 deterministic bytes。
本工作不並行寫同一個 `.olean`。

| 必要命令 | exit code | 本輪耗時／狀態 | 實際紀錄 |
| --- | ---: | --- | --- |
| 生成 | 0 | 0.146 秒，已完成 | `generation.json` |
| exporter `--check` | 0 | 0.145 秒，三份逐 byte 相同 | `replay.json` |
| `PYTHONHASHSEED=17 --check` | 0 | 0.144 秒，三份逐 byte 相同 | `replay_hashseed17.json` |
| `lake --no-cache build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit`（8-core affinity） | 0 | 739.551 秒；8837 jobs 成功 | `lake_build.json` |
| `#print axioms` 稽核 | 0 | 558 項；獨立重跑 5.214 秒 | `axioms.json` |
| `check_docs` | 1 | 兩個已知 missing-path＋本新增報告未索引 | `validation.json` |
| `docgraph check` | 0 | 完整本輪文件範圍 | `validation.json` |
| `git diff --check` | 0 | 已執行；另掃描所有新增 source 的 whitespace | `validation.json` |

文件檢查的基準已知缺口是 `audits/2026-10-04-task-d5/c4/scope_ledger.json` 與
`audits/2026-10-04-task-d2/integration_doc_changes.diff` 兩個 missing-path；
照實保留其診斷，不為消除基準缺口改寫共享歷史證書。
另因本任務只准新增檔案，本文尚未加入既有 STATUS 的直接索引；因此 `check_docs`
實測另報告此新增報告未索引，共三項診斷；`check_docs` 並未通過。
整合者再依 DOCUMENTATION 處理索引更新。

## 整合入口、停止條件與剩餘範圍

本任務未修改 `Math.lean`。整合者要把 179 張具名證書接入預設 Math target，
可在既有 import 清單新增：

```lean
import Math.GeneratedExcessTwoCertificates
```

公理稽核保留為顯式 target `Math.ExcessTwoCertificatesAudit`，避免每次常規 import
都列印整份稽核。在還未接入 `Math.lean` 時，本文重播命令已顯式 build 新 target。
索引與導覽更新由整合者依文件規則處理；本任務只提供新增報告及證據。

本固定任務已達完成條件：179 張具名 positive／rejected／valid、完整上述 `lake build`
及 558 項公理稽核全部完成，實際輸出與耗時如上。沒有任何圖的 Lean checker 失敗，
未觸發以下來源錯誤停止條件。
若任一具名圖在 Lean 中檢查為 false，立即保存該張原 JSON、其 SHA、生成資料與
最小 Lean 重現，先分辨 ES 證書錯誤與 Lean 定義／匯出錯誤，報告後停止。
若 build 過慢而未能完成全部，必須列出實際已編譯的具名範圍及數量，不能以生成
資料或 Python pass 代替 Lean 完成數。

即使全部固定證書完成，上述 completeness、distinctness、任意大小、拓撲嵌入與
一般定理仍是明確未建立的範圍。本任務沒有以這些較強聲稱作為任何 checker 的前提。
