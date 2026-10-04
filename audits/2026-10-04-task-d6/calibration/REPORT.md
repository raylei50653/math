# D₆ 項 7：保存真圖的獨立合理性對照

**判定：確認，限於兩份 observations 實際保存的具名圖。沒有保存真圖含有第三份長支援 one-sided piece 加兩份不同 unary。**
字面「任何平面 disk 圖只要有一份長支援分量與兩份 unary 就不可能存在」則**錯誤**，因為刪掉了 q-criticality 等必要前提；下面給出兩個符合 degree-four piece 定義的平面負控制。這不是定理 C-W 在其原前提下的反例。

## 輸入、邊界與重播

輸入為任務 snapshot 中 `c5_shield_calibration/observations.json` 與
`c5_excess_rejection_law/observations.json`。讀入前保存 SHA-256，另複製到本子目錄。
結束時重新讀取所有使用的來源 snapshot，五份檔案均無漂移：見
`hash_before.json`、`hash_after.json`。這是對父任務 snapshot 的核對；原工作區檔案的前後 hash 由 D₆ 主稽核承擔。

```sh
python3 audits/2026-10-04-task-d6/calibration/check_calibration.py
```

Checker 僅用 Python 標準庫，不 import 任一既有 checker 或圖庫。
它只處理已保存的 edges 及兩個具名負控制，不重跑 E1 大枚舉、S greedy producer，或尋找新圖。
輸出為 `results.json`。

## 如何獨立核對

以完整 edges 重建鄰接、每点的完整 degree、H、R={內點 degree≥5}，再用 BFS 重建 H−R 的原連通分量；own-support 僅取該分量原來的框鄰點，不讀 producer 的 roots、pieces、unary_count 或 support 判斷。
Unary 是原分量恰鄰接一個 root；one-sided 另驗 H−P 非空連通。
「長支援」是原支援不包含於任何框邊的兩端點。長分量與兩份 unary 必須是三個不同的 H−R components；不能把長 unary 自己再算入那兩份。

獨立生成所有 proper 四色 C₅ 列，按同一 color permutation 的 restricted-growth 形式取十個 orbit；這十列與輸入 pattern_order 一致。
每圖用小型 DFS 重算十列的延拓及每條非框邊刪除後的延拓，不信任保存的 Σ 或 critical_edges。
保存 rotation 則重新走全部有向 darts，驗每點 rotation 恰為原鄰接、全圖連通、Euler characteristic=2、指定 induced C₅ 是完整面。這提供每個保存圖的組合 disk realization；不讀 producer 的 embedding/planarity 成功標記。

## 保存真圖結果

| 保存來源 | graph occurrences |
| --- | ---: |
| S 的 graphs | 21 |
| E 的 exhaustive/minima_by_sigma | 50 |
| E 的 scratch original_edges | 20 |
| E 的 scratch outcomes | 20 |
| E 的 scratch witness | 20 |
| 合計 | 131 |
| 依有標號 vertices、edges 去重 | 71 |

71 圖全部通過獨立 disk rotation 核對；有效內點全部 degree≥4，且對原完整 Σ 的每條非框邊確實 critical。
按獨立重建的 unary 數，0/1/2 份分別有 41/15/15 圖。
那 15 個兩-unary 圖全都只有一個 root、恰好兩個 H−R components，兩份 unary 就是全部 pieces，因此没有第三份長分量。
S 內五個短支援 mixed piece 的保存反例均沒有 unary，亦不違反本次三份盾弧推論。

對單列 q 的 minimality 與完整 Σ 的 minimality 不可混淆：71 圖中，25 圖對某一個被拒絕 pattern 是單列 q-critical；另外 46 圖對任何單列都不是 q-critical（其中包括 Σ 全收的框-only 圖）。因此不能從「保存圖都是 Σ-edge-minimal」寫成「保存圖全部滿足 C-W 的 q-critical 接點前提」。本次無候選三分量，已可完成 saved-domain 的反例檢查，不需要把任何非 q-critical 真圖硬套入 C-W。

此結果只覆蓋兩份 JSON 實際保存的 71 個有標號圖，並不覆蓋 E1 先前枚舉中未逐一保存的所有圖，也不是任意大小來源排除的證明。

## 不帶 criticality 的字面外推反例

以下圖不是來源 observations 的內容，僅作稽核負控制。完整 edges、rotation、著色及刪邊核對保存在 `results.json` 的 `unconditional_paraphrase_negative_controls`。

第一例 B=0,…,4，r=5，長 piece C={6} 的 support={0,3,4}；D₁={7,8,9}、D₂={10,11,12} 是兩個 triangle unary，其 supports 分別是 {0,1}、{2,3}。
所有 piece 點完整 degree 恰4，唯一 root r 的 degree 恰5。
H 連通且三份 pieces 均 one-sided，disk rotation 滿足 V−E+F=13−27+16=2，指定 C₅ 為外面。
q=01012 的合法延拓為

```text
0:0, 1:1, 2:0, 3:1, 4:2, 5:1, 6:3,
7:2, 8:0, 9:3, 10:2, 11:0, 12:3.
```

所以只剩 degree-four、long support、one-sided 與 unary 數量的無條件句子已是假的；缺少拒絕見證時短 unary 可以存在。

第二例 B=0,…,4，r=5 有 spokes 到 {0,1,2,4}。
D₁ triangle={6,7,8}：6 鄰接 r、0，7 鄰接 r、1，8 鄰接 0、1；D₂ triangle={9,10,11}：9 鄰接 r、1，10 鄰接 r、2，11 鄰接 1、2。
第三 piece C={12} 鄰接 r、2、3、4，support={2,3,4} 長。
兩份 triangle 的全部內邊及框五邊均包含於圖中；沒有其他邊。
所有 piece 點完整 degree 恰4，r 的 degree9；三份 pieces 均 one-sided。
Disk rotation 滿足 V−E+F=13−31+20=2。

這一圖確實拒絕 q=01012：r 的四個框鄰點見到 {0,1,2}，迫 r=3；12 的框鄰點亦見到 {0,1,2}，迫12=3，與 r12 衝突。
然而刪掉 D₁ 或 D₂ 的任一邊，原拒絕仍由 r12 保留。獨立 DFS 核對全部 18 條 unary 相關邊刪除後均拒絕 q，尤其四條 root-contact 邊都不 q-critical。
所以即使補上「拒絕 q」仍不夠，接點 criticality 不能省略。刪掉 r12 後則可延拓 q。

## 證據分層與整合建議

- 紙面：上述第二反例的 q 拒絕与 noncriticality 可直接由 r、12 被迫同色重推；第一例著色可逐邊核對。
- Python 有限域：71 保存圖的完整 edges/rotation/延拓/degree/components 重算及兩個固定负控制。
- 外部定理：本小核對沒有使用 degree-choosability、Gallai 或四色定理；rotation 的 sphere/disk 解讀使用標準 rotation-system 拓撲。
- Lean：無。

整合者應把合理性對照寫成「保存真圖中未找到違反 C-W 原前提的例子」，並保留「三個不同 components」「拒絕見證來自 q-critical 接點」「unary 每點完整 degree 恰4」「C 的原 degree-5 共鄰 P₃ 來源條件」等限制。
不得寫成無條件的任意平面 disk 圖禁配，也不得把本次 71 圖重播升級成任意大小證明。
