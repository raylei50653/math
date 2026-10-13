# 八份 C8 殘留：共同計數與完整 Kempe 交換軌道

本子包只使用本 audit frozen C8 `interface.json`、no4ct `RESULTS.json` 及
frozen 舊計數發現工具。保留原 274 列與每份來源具名 C8 次序，沒有分別搬色。

**八份殘留均有一份在其整個 U 上嚴格正、U 外為零的精確共同計數向量。**
這也涵蓋較舊 count certificate 之後 `c15-941`、`c20-941` 各刪去兩列的
精煉。新增的完整 Kempe 交換軌道非負分解亦全部可行。沒有新來源排除。

| 查詢 | U 大小 | equality span 內、U 外零的維數 | 交換錐證書非零係數數 |
| --- | ---: | ---: | ---: |
| c04-941 | 193 | 21 | 304 |
| c07-941 | 193 | 21 | 304 |
| c15-933 | 134 | 2 | 165 |
| c15-941 | 171 | 10 | 236 |
| c18-933 | 134 | 2 | 163 |
| c18-941 | 175 | 13 | 249 |
| c20-941 | 171 | 10 | 241 |
| c30-941 | 175 | 13 | 255 |

## 1. 同一 count 向量可滿足全部 cap 非空不等式

對任意 cap F，令 y_p 是固定原 literal C8 列 p 的完整延伸數。
其同圖非空性條件為

\[
\sum_p |\operatorname{Orb}_{S_4}(p)|x_p y_p>0.
\]

若 x 在 U 全正、U 外零，該條件等價於 `U∩Σ(F)≠∅`。因此，任何有限或
無限 cap 家族，只要逐份都與 U 相交，這**同一份數值 x** 便同時滿足該
家族所有非空性不等式。這不是同一列同時接受所有 caps，也不是來源 H。

[count_feasibility.py](count_feasibility.py)從 1,430 份 NC partitions 重建
274×91 非零 equality matrix，逐格 exact 檢查八份向量、十個原外列 transfer
及支援 Kempe 閉包。[完整證書](count_feasibility.json)保留全部座標及有號
equality 展開係數。`c15/c20-941` 的新 U 仍全正，沒有新的 count 迫零。

故對本 audit 所測任何仍與 U 相交的 gadgets，單純加入其非空不等式不會
使這套共同條件不可行，也不會縮小其最大可行支援 U。若某 gadget 與 U 空交，當然仍可
按相對頂點預算排除；本觀察沒有預先宣告所有 planar gadgets 均相交。

## 2. 固定互補色對的完整交換計數錐

以下必要條件對任意有限 plane disk H 成立，不需要四色定理或最小性。
固定全域互補色對 `01|23`。H 的每份完整四色染色把全部頂點分成兩個
二色誘導圖，取其所有連通分量。可分別交換每個分量的兩色；這個作用把
所有完整染色分成真正的全圖交換軌道。

設某軌道有 b 個接觸 C8 的分量、h 個不接觸 C8 的分量。其邊界 restrictions
恰為完整 `2^b` 個 literal rows 的交換軌道 O；每個 row 恰有 `2^h` 個該
全圖軌道的 lifts。因每個接邊界分量非空，這些 boundary rows 互異。
各分量在 disk 中互不相交，所以其 C8 blocks 是 NC partition；同色對的
相鄰 C8 頂點由原環邊相連，必在同一 block。

令 G8 是保留無序色對集合 `{{0,1},{2,3}}` 的八個顏色置換。以 G8 分類
literal C8 rows 得 821 個 states：273 份三／四色 S4 列各對應三個 state，
唯一二色 S4 列對應兩個 state。state 大小是 4 或 8，不能一律當作 8。

因 H 的計數 x 對 G8 不變，可把上述軌道分解在 G8 上平均。對每個可能的 O
定義整數欄

\[
g_O(s)=\frac{8|O\cap s|}{|s|}.
\]

因此把 x 提升成 821 個 state 座標後，有必要條件

\[
\boxed{\widetilde x\in\operatorname{cone}_{\mathbb Q_{\ge0}}
       \{g_O:\ O\text{ 滿足上述 NC 與原環邊條件}\}.}
\]

實際圖的原軌道在此分解貢獻 `2^h/8` 倍相應欄。可能的 NC partition
只是一個必要拓撲條件；枚舉沒有宣稱每欄都來自一份完整來源。
這個錐把不同 boundary rows 的計數綁在同一份完整交換軌道，不只檢查
逐 row 是否找得到一個保支援的交換方式。本包未另證此條件相對既有
共同線性計數條件的**嚴格**強弱。

## 3. 精確結果與控制

[kempe_cone_check.py](kempe_cone_check.py)從原 literal rows、全部 NC partitions
及 8 個 literal 色置換重建全部 1,552 個不同非零欄；每欄保存一份原列、
原 component partition 及**全部** literal flip orbit。
[精確證書](kempe_cone_certificate.json)對八份 U 分別給非負有理錐係數及
91 個有號 equality 係數，且兩個表示逐座標相等。所有 U 列全正、拒絕外列
零、接受外列正。證書分母至多 128；checker 只用 int／Fraction。

[四份實際圖控制](kempe_cone_controls.json)為空 C8、fan、W8、相鄰雙 hub。
控制直接枚舉固定 literal 列的全部內點指派；另按全圖每份色對 membership
重建真正二色分量，從全圖交換軌道取得非負係數。两條途徑的 821 個計數
逐格相同，特別核對二色 state 的 orbit 權重及不接框分量的 `2^h` 倍數。

SciPy/HiGHS 只發現候選；浮點值經有理重建後，零誤差證書才被接受。
[count discovery](kempe_cone_discovery.py)及其[原始診斷](kempe_cone_discovery.json)
另存，不能以其 solver success 取代 exact checker。

```bash
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/count_feasibility.py --check --negative
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/kempe_cone_check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/count_feasibility.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/kempe_cone_check.py --check
```

[實際驗證 receipt](VERIFICATION.json)記錄正常與 seed17 重播及六項破損控制。
[初次失敗紀錄](VERIFICATION.initial_failure.json)保留 controls receipt 的
JSON list／Python tuple 比較錯誤；修正序列化後重播，沒有改動任何數學計數。

这些數值向量仍未提供同一 H、全圖邊子集 equality 展開、不同互補色對間的
共同分量資料、原度數／面配置或來源最小性。任意放大為整數不補足這些義務。
八項來源可實現性、一般 `K∞=K≤5` 及新增論證 Lean 化全部 OPEN。
