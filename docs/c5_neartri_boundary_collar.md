# 933／941 近三角化來源的完整外圈限制

2026-10-13 最新後續：[K14-SPHERE](c5_k14_sphere.md) 已證 `K≤14=K≤5`，
一般目錄外來源至少十五內點；同份新紙面證明給 `h=3 ⇒ k≥16`。
下文先前界線與證書保留當輪語境，h≥3、n₅≥9不提高。


2026-10-13 後續：[K13-COLLAR](c5_k13_collar.md) 完整排除十三內點剩餘外圈，
得到 `K≤13=K≤5`，一般目錄外來源至少十四內點；`h≥3`、`n₅≥9` 不提高。
下文原輪次的十三內點 OPEN／k≥13 保留歷史語境；新結果未 Lean 化。

更新：2026-10-13。本頁接續 [共面正規形](c5_cofacial_normal_form.md) 與
[最小來源度數界](c5_saturation_degree_bound.md)，是完整外圈限制的權威入口。
紙面論證、固定輸入、證書與重播集中於
[隔離報告](../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/REPORT.md)。
941 最後 h=2 的 C₇ 上界已由
[共同計數恆等式](../audits/2026-10-13-c7-joint-kempe-19209f4c/REPORT.md) 普遍排除。
同日 [C₈ 完整 transfer 與共同計數](../audits/2026-10-13-c8-joint-count-3097ef5/REPORT.md)
覆蓋 h=3 全部 35 份具名外圈、70 項查詢：57 項由 transfer／Kempe 排除，
3 項由精確計數恆等式排除，10 項保留通過共同計數與自身 Kempe 閉包的
必要條件向量。這些向量不代表實際來源；共同下界仍為 h≥3、n5≥9。
後續 [C8-STRUCT 原來源結構](../audits/2026-10-13-c8-struct-243a125/REPORT.md)
證明小 C4 cap 為空、內側 C5 cap 為空或五輪，進而證具名 C8 無內弦；
cofacial 識別與四色定理排除 c16-941、c32-941。70 項現為 62 排除、8 殘留。
同圖可逆 Kempe 計數另在 c15-941／c20-941 各迫零兩列，支援由173降至171；
八項仍有精確必要向量，下界不提高。
後續 [C₈ apex 度數](c5_c8_apex_degree.md)排除八項各五個apex的全部三度H假設，
迫原五個apex均degree≥6、H嚴格內側至少六個五度點，故 **h=3時k≥14**。
八項仍留；一般k≥13、h≥3、n₅≥9不提高。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

2026-10-13 後續：[跨原邊缺陷搬運](c5_cross_edge_kempe.md) 把五度中心的
拒絕列 witnesses 接成共同外部 lift 的三元組；五度點下界另迫一個拒絕列在至少
六條不同原邊有單邊缺陷。一般同步與 933／941 排除仍 OPEN。

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

完整外圈關係、內側必要 Kempe 閉包與共同計數恆等式給出：

| 完整 Σ | 邊界超額 h | 五度內點 n5 | h=2 的必要邊界度數 |
|---|---:|---:|---|
| 933 | ≥3 | ≥9 | 全部排除 |
| 941 | ≥3 | ≥9 | 最後 `(4,4,5,4,5)` 亦已排除 |

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
2026-10-12 兩候選共 42 項查詢排除 41 項；2026-10-13 以下共同計數引理
排除最後一項。這是完整關係運算接一般紙面引理，非來源圖枚舉。

## 3. C₇ 上界的普遍不可實現性與重接限制

舊 screen 唯一保留的 `(4,4,5,4,5)`，對具名 C₇
`(a0,a1,y2,a2,a3,y4,a4)` 給出 55／91 列必要上界 U，mask 為
`755425272170557940120206052`。原完整外列聯集仍為 941，3,383 個既有
cap 仍均與 U 相交；這些原始資料與完整接受／拒絕列保留。

令 x_p 為**同一實際內側圖**在固定邊界指派 p 下的延伸數。逐邊
inclusion–exclusion 把其全計數向量表示成 noncrossing boundary-component
equality vectors 的共同線性組合。全部 429 個 partitions 的精確恆等式
在 U 外計數為零時給出

\[
x_{0101212}+x_{0120131}=0,\qquad
x_{0121202}=x_{0123231}=x_{0101212}.
\]

非負性迫 `0101212,0121202,0123231` 全部拒絕；它們卻是 U 內能經原
完整外圈接到 `01232` 的全部三列，故不能產生 941。另一份恆等式迫
`0120231` 拒絕，而在 transfer=941 的假設下，七個完整 Kempe 軌道又迫它接受，
提供第二條重播路徑。此論證對**任意大小的合法簡單平面內側圖**成立，
不假設 U 恰為實際關係。

更強地，既有七點 fan cap 的完整關係與 U 只相交於 `0123231`。
4CT 黏合迫實際內側接受此列，與上述零計數矛盾。因此 **沒有任何 disk C₇
圖的完整關係包含於 U**。完整紙面證明、全部列、獨立覆核及反控制見
[新隔離報告](../audits/2026-10-13-c7-joint-kempe-19209f4c/REPORT.md)。

每份 `01232` 的完整延伸中，每個五度內點恰有两條相鄰 spokes 的 opposite
vertices 同色。故 933／941 現均至少九條不同原邊觸發既有 J_e 拒絕列見證；
各邊的拒絕列與完整染色可不同，仍不能拼成共同見證或 simultaneous quotient。
933 的 `01231` 可獨立套用同一論證，不能將兩次邊數相加。

941 的上述 h=2 C₇ 身份已排除。h=3 的 C₈ 查詢現留 933 的兩份、941 的六份
必要條件殘留，完整具名清單與新向量見
[C8-STRUCT 結果](../audits/2026-10-13-c8-struct-243a125/REPORT.md)。
原十項表與舊向量保留；新增排除適用於整個 c16-941／c32-941 來源契約，
不只排除所選的102列向量。其餘八項後由[C₈ apex度數](c5_c8_apex_degree.md)證原apex均至少六度、
h=3時k≥14；仍缺同一無內弦 H 的原面／度數與跨 splits 的共同分量實現或不可能性定理。
h≥3 的一般外圈及十三內點以上來源仍 **OPEN**，不能採納 h≥4 或 n5≥10。
本輪沒有證明 K∞=K≤5，也没有證明所有 near-cubic 圖的計數猜想。

## 4. 證據與重播

```bash
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/checker.py --check
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/collar_checker.py --check
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/independent_review.py
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/joint/count_identity.py --check
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/topology/count_review.py
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/caps/independent_verify.py
python3 audits/2026-10-13-c7-joint-kempe-19209f4c/counts/controls.py --check
```

正常／seed17、刪除完整 lift 或竄改固定點的負控制及獨立重算結果見
[verification.json](../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/verification.json)。
沿用 K witnesses、一般 screen 與 4CT；本輪不依賴通用 count-cone 猜想。
紙面拓撲、有限證書與既有 Lean 回歸分開；沒有新增 Lean theorem，实际目標來源
為 `not triggered`。整理及上下游核對見 [本輪紀錄](history/2026-10-12-neartri-boundary-collar.md)。
2026-10-13 的 normal／seed17、完整 3,383 cap 重算、計數／full-lift 反控制與
文件接入結果見 [新驗證紀錄](../audits/2026-10-13-c7-joint-kempe-19209f4c/verification.json) 及
[C₇ 排除紀錄](history/2026-10-13-c7-count-exclusion.md)。共同計數引理尚未 Lean 化。
