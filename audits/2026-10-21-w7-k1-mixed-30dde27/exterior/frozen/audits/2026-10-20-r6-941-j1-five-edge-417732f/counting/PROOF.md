# W7 五邊路嚴格子型：完整 cap 與同源 orbit 的精確停止點

本目錄只處理 [geometry 證明](../geometry/PROOF.md) 的嚴格子型：同一實際
J1 type III 完整著色，選定 12 五邊路
`n–u4–u3–u2–u1–L`；原 C7 `n–h–L–u1–u2–u3–u4–n` 內部恰為
原 R，且承接幾何證明用原 C3/C4/C5 pocket 與已排除三邊路所得的全部結論。
因此完整原 star 為

```
N_G(R) = (n,h,L,u1,u2,u3,u4),   d_G(R)=7.
```

這不是一般五邊路必然具有的形狀。四個 ui 是原 F 的私有點。固定整張
實際 `F*=G−{b,p,h,R,x,y,r}`，ordered rim 為
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`。它是原嵌入中的三角 disk；可能有的
原外弦、每一額外原附件及全部私有點都留在 F*，沒有改成任意可獨立選的外部圖。
本輪不強加 a–u4 不存在，也不把其餘可能原外弦刪掉。這些弦只會使對應
同色 rim fibre 的實際計數為零；將它們暫不加入必要零值，會放寬必要條件。

## 完整同列 cap

對每個 canonical proper C13 state i，`z_i` 是 F* 中該**固定字面色框**的全部
完整著色數；空 fibre 計零。全域色置換作用於所有原私有點，故同一 canonical
state 的不同字面代表具有相同完整計數。所有下列 candidate 使用同一向量 z。

左側保留原 b,p,h,R 全部邊，完整 G lifts `(b,p,h,R)` 的條件是

```
b ∉ {a,c,q,p};   p ∉ {a,q,n,h};   h ∉ {q,L,R,n};
R ∉ {n,u4,u3,u2,u1,L}.
```

Q1 lifts `(b,R)` 另要求 `b=n, R=q, b∉{a,c,q}`；J1 lifts `(b,R)`
另要求 `b=L, a≠R, b∉{a,c,q}`。兩者均保留同一完整 R 鄰接條件。
這裡沒有把 R 固定為選定 witness 的色 3。右側完整 lifts `(x,y,r)` 為

```
r ∉ {s,v,w,t,x,y};   x ∉ {c,s,y};   y ∉ {a,t}.
```

逐份完整左右 lifts 配對後，才由原 ordered frame `(x,y,a,b,c)` 取 canonical
五框 row。故 `N_row(M)=Σ_i M[row,i] z_i`，沒有結合獨立可行 marginals。
[caps.json.gz](caps.json.gz) 保留全部 66,430 states、三份 10×66,430
整數矩陣及原 G 的兩個 `01232, h=a/b` sector rows。
[check.py](check.py) 從原完整 stars 重建；root 的獨立原邊枚舉亦逐項確認三矩陣相同。
矩陣 canonical JSON SHA256 為
`e3b20638a9e75a7575c3b0c325e49cd94be6505f62534ab76b8acc5f3591b855`。

繼承同源的 `G[01021,01202,01212]=0`、`Q1[01232]=0`、
`J1[01202,01212]=0`，有任何違反完整 lift 的 core fibre 必為零。
這得到 2,942 個 cap-zero states。另對每個合法 R lift，將同一完整 F*
著色連同該 R 色還原成舊 F 的完整著色；若其 C10 state 已由 frozen
J1 certificate 證零，原 F* fibre 亦為零。共有 5,098 states 有這類 R lift。
兩集合的聯集為 5,098，餘下 61,332 個必要 states。即使某 state 沒有任何
R lift，也沒有據此把 F* fibre 判零：它仍可能是一份無法延伸回 G 的合法
F* 完整著色，而其 G cap 係數只是零。

## 同一實際完整來源的非負 orbit 方程

固定 palette split `01|23`，在 F* 的每份**完整**著色中，分別取兩個 palette
induced subgraphs 的全部連通分量。獨立交換任一完整分量內的兩色，形成真正的
有限著色 orbit；包含所有不碰 rim 的私有分量。若有 b 個分量碰 rim、c 個
不碰 rim，orbit 大小為 `2^(b+c)`，每份 rim literal tuple 恰有 `2^c` 個
完整 lifts。這一步使用整個 `Col4(F*)`，沒有把選定五邊路 witness 的子集當成
Kempe invariant 來源。

繼承 frozen C11 orbit lemma 的平面三角 disk 論證：實際 boundary contact
partition 非交叉，palette transition 數為 `2(b−1)`，block adjacency 是二分圖。
此論證允許原 rim chords，無需 induced C13。窮舉全部符合這些必要條件的
noncrossing partitions，至少包含每一實際完整 orbit；額外的必要 partition
只放寬 count cone。

令 H 為保持 unordered palette pair `{{0,1},{2,3}}` 的八個全域色置換。
proper C13 必用至少三色，所以 H 的每個 rim orbit 有八份字面 tuple。
每一 actual Kempe orbit 的 rim 投影與一個 H-half-row 相交時，恰含四份
tuple：兩個 palette 的全域內部翻色各可獨立選；交換兩個 palette 則改變每個
位置的 palette membership，離開該 actual orbit。故每個非零 orbit entry 是 4。
將完整 actual orbits 依其 boundary column 合併、以 `2^c` 加權，得到

```
8 z[i(h)] = 4 Σ_{j : h lies in column j} X_j,   z≥0, X≥0.
```

實際來源的 X 是非負整數。方程每個 half-row 共用同一 z，包含所有空 fibres
與 hidden components；不允許每個 palette 或每一個 row 各選一份來源。

[orbits.py](orbits.py) 以 active-block stack 完整產生 742,900 個 noncrossing
C13 partitions，其中 41,834 個通過必要條件；逐份固定各 block 的初見 bit，
再枚舉其餘 boundary run bits 及 component flips，生成 428,506 份完整整數
columns（零值刪除前）。每個 column entry 為 4，H-half-row size 為 8。
這個較快枚舉器與 frozen 原 C11 演算法的全部 36,487 columns 逐項相同，
見 [校準記錄](c11-calibration.log)。

任何 column 若碰到已證零的 half-row，非負性迫該 X 為零。刪去這些 columns，
再將無 surviving column 支持的 half-row 所屬整個 canonical state 證零，迭代
至穩定。這是必要**支持**閉包；其存活不提供共同方程的可行解。
精確閉包再刪 24 個 states，留下 61,308 個 states 與 307,197 個 columns。
[orbits.json.gz](orbits.json.gz) 保存全部 surviving 整數 columns、row-to-state
map、每一輪刪除及 full-family/row-map/live-column SHA256；預設 replay
完整重建並逐項核對。

## 嚴格正性與本輪沒有得到的結論

選定 actual 五邊路著色供應 rim
`(0,1,2,1,2,1,2,3,1,2,e0,e1,2)`，其中 `(e0,e1)` 為 `(0,1)` 或
`(1,0)`。其 canonical IDs 為 44459、44466，因此

```
z[44459] + z[44466] > 0.
```

兩個 IDs 均在精確支持閉包中存活；原 941 的七個 positive rows 亦各有
存活支持。這些只是各必要支持非空，**不是**它們已在同一可行 z 上同時成立。
本輪一次 LP 將原七個正量、兩個 h sectors 及上述 witness sum 全部放在同一 z，
矩陣為 183,924×368,505、4,448,132 個非零 entries。在約 120 秒範圍停止前，
沒有產生可用 primal 或 dual。其原始輸入腳本及 [停止記錄](discovery.json)
保留；沒有數值或精確 feasibility / infeasibility 結論。

凍結 C11 的 132-term λ 也不能直接沿用。把 C13 half-row 刪去 u4,u3，再對
proper C11 投影拉回舊 λ、非 proper 投影取零，會在 surviving C13 column
21020 得到 pairing −4，在 column 21029 得到 +4。
[tensor_control.py](tensor_control.py) 精確重播這四個反例；這只否決該特定
直接 deletion pullback，沒有否決其他廣義 identity。

因此本輪已獲 W7 完整 cap、正確的同源非負 orbit 必要方程、精確零值閉包，
但尚無來源排除、精確共同計數可行模型、來源實現、smaller bad 或 Lean 結果。
一般五邊路與 C7 內含其他原點的情形也不在本目錄結論範圍。

`python3 -B .../counting/controls.py` 完整重播，並確認改一份 column 的 half-row
整數與把 entry multiplicity 4 改成 5 均遭拒絕；見 [checks.json](checks.json)。
