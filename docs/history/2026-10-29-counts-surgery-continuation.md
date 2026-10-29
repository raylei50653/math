# 計數／手術共同切口續進紀錄

2026-10-29。接手時基準 `4476049`，前輪四項驗證已在工作樹暫存；本輪期間該前輪
由其他工作提交為 `f5bedfd`。本輪未執行 commit／push，亦未改寫先前 frozen 證據。
與本題無關的 shelling 續進屬同工作樹其他工作，不計入本輪成果或驗證。

後續依使用者要求，兩批續進一同整理提交；[發布紀錄](2026-10-29-continuations-publication.md)
保存本次重播、封存與檢查。以上「未提交」仍記原研究階段，發布狀態以即時 Git 為準。

權威來源：[共同切口與完整分量反例](../four_color_counts_surgery_continuation.md)。

## 成果與信任範圍

本輪不改 932／4CT 的 OPEN 裁決。新增的是：

1. 同一標記五角星 pole 的完整 30 態／150 交換 automaton，逐態 noncrossing，
   與既有 B5 的十個正共同權重逐項一致；用實際來源證明若省略共同嵌入，
   連全部有限交換歷史閉合都不足。
2. 把既有共同切口條件施於此完整反模型：60 actions 被共同側別拒、90 被側內交錯拒；
   真 disk 五環正控制的 150 actions 全過。刪任一 E 的負控制可行，兩 E 共同卻不可行。
3. 固定五環 pole 的 120 port orders 分類，只有 10 真 disk orders 與另 10 五角星
   orders 能讓所有態的三系統各自 noncrossing。
4. 固定真 disk 的全具名分量分割反例，含相同第一條 22 原邊 path 及相同一步端點接口；
   另有全 boundary-rooted 四步字面區分，八份切口均符合共同側別與精確重接。

一般 crosscut soundness 與 Petersen cap 非平面性是紙面；固定域窮盡為 Python 整數／
圖遍歷證書。未新增 Lean；未聲稱 ray 完備性或共同切口拓撲在本輪形式化。

## 實際研究重播

四份新 checker 的 `--check` 逐 byte 比對均通過：

| checker | 實際核對 |
| --- | --- |
| `four_color_counts_face.py` | 30 完整染色、180 B5 式、150 交換、300 mixed 更新、40 座標擾動負控制、1,024 rotations |
| `four_color_port_order_obstruction.py` | 120 orders、10,800 系統核對、100 crossing order 負控制 |
| `four_color_shared_cut_obstruction.py` | 150 負 actions 全拒、150 正 actions 全過、兩份系統各自可行的刪除控制 |
| `four_color_surgery_continuation.py` | 491 舊表染色、465 states、26 collision buckets、兩份指定完整 witnesses、同原邊第一步、兩步內點規則及四步 boundary 規則 |

全部證書與來源 hashes 在
[本輪 audit 目錄](../../audits/2026-10-29-counts-surgery-continuation/)；
精確命令見權威報告 §5。沒有重建或覆寫舊 `artifacts/`。

## 治理傳播

Closure scope / Canonical Source + Evidence：只收尾上述固定反模型與指定候選 state 的
不足性；來源為新專題報告及四份 JSON 證書，不收尾一般 932 或有限充分 state。

Updated：原計數／手術驗證加續進入口；舊 cut-interface 報告加 stronger counterexample
後續；4CT guide 加來源連結；STATUS 加直接報告與本歷史索引。

Reviewed-unchanged：B5 face 的射線／普通 gluing 限制、既有一步 cut 重建引理、
LOCK-NO-GAIN 限定範圍均未改；新反控制不構成一般 mask 排除。

Remaining OPEN：由任意同一 plane 932 來源推出禁止的共同接線、能生成下次切口的
有限充分資料、不可避免性及共同解存在性。

Propagation stop：L1 導覽與索引，加 L2 直接接口 consumer 的 dated 後續；
父命題仍 OPEN，研究線沒有增減或活躍狀態變動，故不改 HANDOFF／README 或跨線 synthesis。

文件檢查：`check_docs.py` 通過；掃描數量與輸出見 audit 中 `document-checks.json`。正式 docs
DocGraph 通過（98 documents／386 relations／0 errors）。全工作樹 DocGraph 失敗，
為保留的 audits／scratch snapshots 所宣告的 72 個 duplicate IDs；不刪快照，也不將
正式 docs 通過誤記為全樹通過。`git diff --check` 通過。本輪沒有新增 DocGraph IDs。

獨立交叉審閱核對了 port-order／crosscut soundness、Petersen 紙證及四步 boundary trace。
另一份分層 BFS 在深度 0／1／2 分別得到 1／5／18 個新 paired states、皆無 pairing
分歧；深度 3 的 54 個新 states 中有 6 個分歧，確認 checker 的最短性範圍。
