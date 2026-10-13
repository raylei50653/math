# 933／941 近三角化來源的完整外圈限制

2026-10-12。本頁接續 [共面正規形](c5_cofacial_normal_form.md) 與
[最小來源度數界](c5_saturation_degree_bound.md)，是完整外圈限制的權威入口。
紙面論證、固定輸入、證書與重播集中於
[隔離報告](../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

## 1. 精確結論

在所有完整關係不屬於 K132 的 disk C5 來源中，先最小化內點數，再最大化邊數，
取既有正規形所得的簡單、二連通、chordless-C5 近三角化圖 G。
整張圖、原五個 labels 與全部染色共同對齊，使 Σ(G)=933 或 941。
不加入 edge-critical、Gallai 或舊 ε 分支的前提。

本輪證明沒有內點 v 同時接兩個非相鄰原框點。結合無 separating triangle，
邊界鄰點形成實際簡單內圈 C_(5+h)，其中

\[
h=\sum_{i=0}^4(\deg(b_i)-4).
\]

完整外圈關係與內側必要 Kempe 閉包給出：

| 完整 Σ | 邊界超額 h | 五度內點 n5 | h=2 的必要邊界度數 |
|---|---:|---:|---|
| 933 | ≥3 | ≥9 | 全部排除 |
| 941 | ≥2 | ≥8 | 只剩 `(4,4,5,4,5)` |

度數下界使用精確 Euler 式
\(n_5=6+h+\sum_{v\notin B,\,d(v)\ge7}(d(v)-6)\)。
這是最小來源的必要條件；不是對任意具有該 Σ 的非最小圖作度數宣稱。

## 2. 兩個直接矛盾與完整閉包

若有 b2–v–b4，沿此路徑把原圖切為具名 C4 與 C5。C4 的七個必要完整關係
與 K132 的 132 個關係，以原 v 的同一顏色接合，共 924 個結果全部回到 K。
長側內點更少，必在 K，故與目錄外身份矛盾。這一結論適用於全部二邊 crosscuts，
不限制 v 的度數；亦已排除 [三份任務](tasks/c5_degree5_link_tasks.md) 中任務 C
所指定的非相鄰兩框接點來源。另訂的 132² cap 計算已由
[任務 C](c5_degree5_link_reductions.md) 獨立完成；兩份證據各按自身前提驗收。

若五個框點都度四，內圈為五個原框邊的三角面 apices。兩候選共同拒絕
`01021,01202,01212`，完整環帶 transfer 迫內圈關係包含於 `{01023,01203}`；
但接受 `01232` 又迫內圈接受 `{01212,01213,01231,01232}` 中至少一列，直接矛盾。

對 h≤2 的全部 21 份具名環帶，保留完整內列到外列的轉移欄。從不會產生
原拒絕列的內列集合開始，反覆刪去無法滿足某組互補色對必要交換軌道的列。
同一真實內側圖的完整關係始終包含於候選集合，因此此刪除有普遍 soundness。
兩候選共 42 項查詢排除 41 項；此為完整關係運算接一般紙面引理，非來源圖枚舉。

## 3. 精確剩餘與重接限制

941、h=2 唯一保留的 `(4,4,5,4,5)`，有一份具名 C7 內側關係的必要上界：
91 個 proper 色軌道中剩 55 列，完整外列聯集仍為 941。實際內側關係只知
**包含於**此上界，不能宣稱它恰有 55 列、已實現或已被排除。
3,383 個實際外側 cap 的完整關係控制均與上界相交，未新增排除。

每份 `01232` 的完整延伸中，每個五度內點恰有两條相鄰 spokes 的 opposite
vertices 同色。故 933／941 分別至少九／八條不同原邊觸發既有 J_e 拒絕列見證；
各邊的拒絕列與完整染色可不同，仍不能拼成共同見證或 simultaneous quotient。
933 的 `01231` 可獨立套用同一論證，不能將兩次邊數相加。

941 的上述 C7 身份、h≥3 的一般外圈，以及十三內點以上來源仍 **OPEN**。
本輪沒有證明 K∞=K≤5，也没有證明所有 near-cubic 圖的計數猜想。

## 4. 證據與重播

```bash
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/checker.py --check
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/collar_checker.py --check
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/independent_review.py
```

正常／seed17、刪除完整 lift 或竄改固定點的負控制及獨立重算結果見
[verification.json](../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/verification.json)。
沿用 K witnesses、一般 screen 與 4CT；本輪不依賴通用 count-cone 猜想。
紙面拓撲、有限證書與既有 Lean 回歸分開；沒有新增 Lean theorem，实际目標來源
為 `not triggered`。整理及上下游核對見 [本輪紀錄](history/2026-10-12-neartri-boundary-collar.md)。
