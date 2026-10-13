# 六點 C6 cap 的獨立覆核

2026-10-13。覆核範圍是本包的三型分類、新 cap 域的完整性及同一原列／
同一色框的全部 fibres。不修改 producer、證書或前輪輸入。程式為
[independent_check.py](independent_check.py)；它不 import producer 或
任何前輪 audit 程式，只讀 frozen 原始權威輸入與本包證書。

**結論：通過。** 三型分類的紙面推導成立；独立 annulus 生成式恰給
三個 cap 同構類，與 plantri 的三份保留圖完全一致。全 2,304 個
「cap、原短 Eq、具名 alignment、原 U」交集非空。本輪完成這個精確
方法域的無拒絕檢查；八份必要上界、來源實現與主命題仍 OPEN。

## 紙面分類覆核

已逐節讀 [PROOF.md](../theory/PROOF.md)。全接框分支沿每條原接框邊
辨識私人核心的無界面，再由 `9<=eII<=9` 迫 maximal outerplane、
全私人度五及每點核心度至多四，沒有把原 boundary 平均度改成最低度。
四三角面的 weak dual 只有 star 或 path；path 的兩耳若共端點，該點
是中間 quadrilateral diagonal 的端點，其核心度五，故被排除。
留下的 star 與 path 恰是型 A、B。

Deep 分支的 induced 性論證有效：spanning W5 使私人核心二連通，
故外面 cycle 簡單；原 B 全在核心外側、沒有遺失的內部頂點，所以
核心每個 bounded face 保持三角面。額外 t 條 chord 給外面長 `5-t`，
恰有 t 個 hidden 環點；它們的最低度需要全部 2t 個額外端點 incidences。
若 t>0，縮短後的原外面 cycle 必使用一條 chord，而其兩端 visible，
造成矛盾。故 t=0，核心確為 induced W5，中心唯一。

Annulus 沒有同環 chord 或其他頂點，因此每個三角面恰含一條環邊、
兩條 spoke；跨 spokes 的面 dual 連通且二正則，故為一個 cycle。
其 O/I word 給每個私人環點連續且完整的 boundary 鄰點區間，
`deg_B(x_i)=r_i+1` 且 `sum r_i=6`。各型已知度數迫定 r-vector，
餘下自由度恰由全 12 個 C6 rotations/reflections 覆蓋。這裡保留
實際各條接線，沒有用只記 degree sequence 的計算代替接線分類。

以上提供直接生成式的完備性證明。下述有限生成控制核對這份論證的
具體域，有限控制本身不代替任意 plane cap 的紙面分類。

## 不依賴 plantri 的有限域控制

Checker 先從 labeled hexagon 的九條可能 diagonals 中取三條，
以交錯端點判据排除 crossing，得到 **14** 份 triangulations。
其中八份的最大核心度至多四；依 `r_i=4-deg_Q(x_i)` 逐條補出全部
annular spokes。另對五環 wheel 的唯一三接框環點取五個位置，
生成五份具體接線。這 8+5 份均有恰 27 邊且六私人度至少五。

對每份圖，checker 窮舉全 12 個 boundary dihedral maps 及全 720 個
私人 relabelings，以完整 edge set 求確切同構類，恰得三類；
三類與證書的全部三 cap 完全相等。此生成式沒有讀取 plantri 圖來
反推候選，亦不使用 graph-isomorphism 套件或 producer 的排序算法。

另對保存的 89,038 行 plantri raw rotations 獨立 face walk，檢查
每份的 27 邊、16 三角面及唯一六邊面，再從其實際外面判斷無弦及
私人最低度五。僅保留零起算 lines `43569,43570,81910`，與證書相同。
Checker 核對 source rotation、完整 relabel map、named rotation、
全部 edges、degrees、core edges、接框 edges 及 deep wheel ring。
新 cap 域的完備性可依直接分類與生成式；前輪 signed 五點域的
plantri 依賴仍照原樣保留。

## 完整原列與同一色框

權威 rows、literal assignments、literal-to-pattern 與八份 U 均取自
本包 frozen `predecessor-authority`，不僅取前輪整理過的 cap 證書。
所有 frozen inputs 的長度與 SHA256 均重新核對。

每份 cap 的全部 `4^6` 個私人 tuples 由 Cartesian product 生成，
先對私人邊過濾，再逐個 literal boundary row 對所有接框邊檢查。
這是獨立於 producer 動態 DFS 的完整 assignment 枚舉。每 cap 的
31 個 canonical C6 fibres 及全部 732 個 literal C6 fibres 均重算，
包括空 fibre 及每份完整六色 tuple。

每 cap 保留八個具名短 Eq × 12 alignments，共 96 attachments。
每 attachment 核對原 Eq pair、六 pin 的順序、兩個 Eq pins 的共用
cap pin、omitted digon pin 的 `-1`、私人順序與全部 274 個原 C8
fibres；Eq 不合的 182 個 cells 必須明列為空。其餘 92 個 cells 的
完整 colour-transfer permutation 逐一核對，未出現的色也必須
延伸成全四色 bijection。

再將每個 canonical C8 fibre 以**同一**原 row 的全四色 permutation
還原，與該 literal row 直接邊約束所得的完整 tuples 比較。全部
6,564 個 literal C8 rows 均包含在內，並重新計算保存的逐列 digest
與 lift count。因此 lossless codec 經過實際全域重算，非僅比較
support masks、單點 marginals 或各段獨立正規化。

| 核對項 | 數目 |
| --- | ---: |
| 三 cap 的 canonical C6 完整 fibres | 93 |
| 直接 literal C6 完整 fibres | 2,196 |
| 原 C8 canonical 完整 fibres | 78,912 |
| 其中 Eq mismatch 空 cells | 52,416 |
| 原 Eq 全四色 transfer records | 26,496 |
| 原 C8 literal 完整 fibres | 1,890,432 |
| 原 C8 literal 完整私人 lifts | 857,088 |
| 同一原 row 的非空 U 交集 | 2,304 |

每個 U 交集保存全部原 C8 indices，並核對第一個完整 witness 的
原 row 加六私人色值。這些非空 witness 各屬自己的固定 gadget／U；
沒有推成一份共同 row 同時滿足任意多個 gadgets。

## 重跑與破損證書

[正常結果](INDEPENDENT_CHECK.json) 與
[seed17 結果](INDEPENDENT_CHECK_SEED17.json) 均通過；seed17 改變
cap、attachment 及原 row 的處理順序，最終計數完全相同。
兩份結果都記錄證書、checker 與 INPUTS 的 SHA256。

五項負控制只改記憶體中的證書副本，再送入同一 verifier；磁碟上的
來源證書保持不變。缺一份 graph、缺一份 fibre、缺一個實際 private
tuple、交換 rotation 的兩個鄰點、破壞原 pin map，五項全部拒絕。
拒絕理由分別為域缺漏、fibre 缺漏、tuple 不相等、rotation custody
不符及原 pin map 不符。沒有把 seed 變序或負控制當作數學完整性證明。

可重跑而不寫證書：

```sh
python audits/2026-10-13-c6-cap-completion-6943561/review/independent_check.py
python audits/2026-10-13-c6-cap-completion-6943561/review/independent_check.py --seed 17
```

## 採納界線

可採納三型 cap 完備分類與全部接線的同列 full-fibre 無拒絕。
合併前輪受限 C4/C5 代表與 signed 五點化約後，可關閉同一空側、
只識別原 C8 pins、`a-d<=5` 的這個直接空交 gadget 方法域，並保留
前輪 plantri 依賴。這不排除八份必要上界，不實現未知 H，不處理
任意其他原面／免費原頂點／超預算操作，不建立一般主命題或 Lean
定理。沒有做 commit、push 或更改共享研究狀態。
