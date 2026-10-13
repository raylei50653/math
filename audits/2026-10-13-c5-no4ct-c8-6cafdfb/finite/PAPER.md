# 三支 h=3 的完整有限介面與共同計數

本子證書只用本目錄 [INPUTS.json](INPUTS.json) 所列 15 份凍結來源。
來源幾何契約由前輪 no4ct collar 與本輪主報告提供：同一原圖 G 的
具名外 C5、原附件、原 rotation，以及其內侧三角化 disk H，具有原簡單
C8。此處不預設 H 的完整關係非空；只使用 G 的完整關係恰為所列目標。

**932 的 35 項 h=3 查詢全部排除，殘留清單為空。** 加上舊 933／941 的
70 項完整重算，本有限層共排除 95／105 項；10 項仍為必要條件殘留。
是否可用來源幾何進一步排除 c16／c32，由主報告另證，本有限層不消費舊
cofacial quotient 的四色定理入口。

## 1. 完整介面與五份非空固定點

35 份配置是所有 `t∈N^5, sum(t)=3`，不做對稱縮減。每份依原輪轉保留

```
a0, y1_1,...,y1_t1, a1, y2_1,...,y2_t2, a2,
y3_1,...,y3_t3, a3, y4_1,...,y4_t4, a4, y0_1,...,y0_t0.
```

每個 a_i 接 b_i、b_(i+1)，每個 y_i_j 只接 b_i；原內、外 cycle 邊與
全部 13 個環帶三角面皆保存。對 C8 的 274 份 proper S4 代表，逐一保留
固定原色框 `{0,1,2,3}` 下全部 6,564 份 literal 指派。每份固定內列 q
的十個外列 fibres 保存完整 `(b0,...,b4,C8)` 染色，包含空 fibres。

設 `C_t(q)` 為固定內列 q 的完整外列像。對同一 H 的完整關係 S，精確地
`Sigma(G)=union(q in S) C_t(q)`。初始上界為所有 `C_t(q)⊆R` 的 q。
某 q 在一組互補色對下沒有完整 noncrossing component-swap orbit 留在
當前上界內時才刪除它。真實完整染色的實際分量與所有交換結果總會提供一份
合法 orbit，因此真實 S 的列不會被刪。這不假設不同 splits 的分量
可由抽象表任意拼成同一張圖。

| 932 的查詢 | t | 固定點列数 | 外列像 union |
| --- | --- | ---: | ---: |
| c00 | (0,0,0,0,3) | 100 | 0 |
| c03 | (0,0,0,3,0) | 100 | 0 |
| c09 | (0,0,3,0,0) | 100 | 0 |
| c19 | (0,3,0,0,0) | 100 | 0 |
| c34 | (3,0,0,0,0) | 100 | 0 |
| 其餘 30 項 | 完整清單見 certificate | 0 | 0 |

因此 35 項上界全部無法產生 932 要求的外列索引 `2,5,7,8,9`。
五份 100 列固定點只代表有些內列不產生任何環帶延拓，不代表仍有 932
查詢殘留。其排除不需共同計數或任何可染性存在定理。

## 2. 舊 70 項的精確接入

完整 producer 與另一套不匯入 producer 的 verifier 分别枚舉 literal
指派、原附件、全部 95,900 個 transfer 係數及 Kempe 分量交換表。
舊 70 項的固定點、刪除每一輪及完整 accepted preimages 與凍結資料完全相符。
新 35 項 932 另由兩套 pruning 實作逐欄、逐輪核對。

同一 H 的 x_p 是固定 literal 內列 p 的完整延伸數。逐邊
inclusion–exclusion 給

```
x_p = sum(F subset E(H)) (-1)^|F| 4^k0(F) E_pi(F)(p).
y_r = sum_p T[r,p] x_p.
```

平面性使 pi(F) noncrossing；所有 1,430 個 partitions 的 equality vectors
只有 91 個非零欄且秩為 91。展開係數可有正有負，只有真實 x 保證非負。
外列 transfer 逐 literal 接合；二色內列軌道只有 12 項，其他軌道 24 項，
並未一律使用同一乘數。

舊 c05-941、c13-941、c23-941 的三份正左式／必要零列右式恆等式逐一在全部
1,430 個 equality vectors 上檢查；正左式涵蓋接受外列 `01232` 的全部前像。
故同圖非負計數與外列接受要求給矛盾，不依賴 4CT。其餘十份共用計數殘留
包括全部 274 座標、91 個有號展開係數、十個外列計數、零列及支援 Kempe
閉包；全部資料保存在 [certificate.json](certificate.json) 的 query ledger。

| 目標 | 查詢 | transfer／Kempe 排除 | count 排除 | 有限層殘留 |
| --- | ---: | ---: | ---: | ---: |
| 932 | 35 | 35 | 0 | 0 |
| 933 | 35 | 33 | 0 | 2 |
| 941 | 35 | 24 | 3 | 8 |
| 合計 | 105 | 92 | 3 | 10 |

## 3. 可逆 Kempe 計數不需 4CT

固定 split `01|23`。對同一 H 的完整染色，把使用 01 的原頂點集合 S 固定，
則 H[S] 與 H[V\S] 的實際二色分量不變。每個分量可獨立交換；具有相同
boundary orbit 的完整延伸數同步，於是完整計數向量是 boundary orbit
indicators 的非負組合。這與上節 equality 展開的有號係數不同。

保留 split 的八元素換色群給 821 個具名 rows。獨立枚舉得到 1,552 個一般
平面必要 orbit generators；H 三角化時，面內二組介面弧給邊界分量數
`b=t/2+1`，留下 981 個 generators。各生成向量仍只為必要有限介面，不能
宣稱它們共同由一張 H 實現。

所有十份 residual 的共同 x、orbit coefficients 與展開係數皆以 Fraction
精確核對。通用 cone 上的四份迫零 fibre 證書也重播：

| 查詢 | 索引 | 具名 literal word |
| --- | ---: | --- |
| c15-941 | 98 | 01201201 |
| c15-941 | 159 | 01210201 |
| c20-941 | 34 | 01020121 |
| c20-941 | 54 | 01021021 |

c15-941／c20-941 支援由 173 收為 171，但各有共同精確新向量，不能算作
整項排除。其餘有限層殘留依序為 c04-941(193)、c07-941(193)、
c15-933(134)、c16-941(102)、c18-933(134)、c18-941(175)、
c30-941(175)、c32-941(102)。括號為必要支援列數。

以上不使用來源最小性或 4CT；最小性與 cofacial 可染性可能在主報告另外
使用。程式亦檢查八份舊 residual 在 91 equality fibres 上有正計數，
那只是現有有理向量的算術性質，沒有作為普遍可染性定理的前提。

## 4. 重播、控制及停止点

```
python3 -B audits/2026-10-13-c5-no4ct-c8-6cafdfb/finite/check.py --check --negative-controls
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c5-no4ct-c8-6cafdfb/finite/check.py --check --negative-controls
```

標準庫與 int/Fraction 重播，不需要 LP solver。負控制分別破壞 literal
transfer 係數、具名內圈順序、完整 lift、共同計數座標、整體閉合狀態及
932 判定；checker 皆須拒絕。正常／seed17 日誌及其雜湊見
[VERIFICATION.json](VERIFICATION.json)。獨立本輪覆核另由主 audit 的
review 子目錄提供。

有限層10項都是 **necessary-condition residual**，不是實際來源圖、
反例或完整關係實現。實際目標來源控制 **not triggered**；不把零樣本當作
排除。未提高 h≥3／n5≥9，未採納 h≥4、k≥19 或無界排除。
無界932／933／941、主命題及新論證 Lean 化仍 OPEN。
