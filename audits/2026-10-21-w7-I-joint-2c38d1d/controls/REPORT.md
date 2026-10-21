# 普通型 I：同一圖的 03×02 正控制及來源反控制

2026-10-21；exclusive BASE `2c38d1dcb4490017312467deb19d9da02b7bb2a6`。

本目錄只處理父審核凍結的兩個 B14 literal，每個 literal 的 03 二型乘 02 四型。
**03 與 02 並非單憑共同平面三角化就互斥。** target44459 的第二個 03 型，
與第一或第三個 02 型各有一張同一著色、同一 disk 的明確共同控制圖。
這兩張控制圖均不符合原來源：原 01 gate 不過，且接回原 strip 後 U、V 各為四度。
沒有原941來源實現，亦沒有據此排除任何一般八對或型 I。

## 固定範圍及有限控制

完整有序框為父審核原 B14：

```text
(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)
```

只做零個或一個內點的三角化動態規劃，沒有任意大小圖枚舉。
對新增內點，其每個 split 的分量身分可為同側任一既有 boundary block，
或全新的不碰框分量；每對均測 7×8=56 個內點分量身分。
因此沒有把「不碰框分量」錯略成必屬既有 boundary block。
允許邊以實際色與兩份完整 partition 同時判定；任何同 palette 邊不能合併不同指定塊。
零內點以 polygon DP，單內點以全部 cyclic star 起點及 star 弧上的 polygon DP 判定。
每張輸出圖再逐邊檢查 proper 色、面 incidence、唯一原 C14 邊界、Euler 與各點完整 link，
並從同一圖重新計算三個 split 的完整實際分量。

| literal | 03 型 | 有一內點 completion 的 02 型 |
| --- | --- | --- |
| 44459 | 第一：U03 接 a，V12 只有 V 的框接觸 | 無 |
| 44459 | 第二：U03 只有 U 的框接觸，V12 接 Y,w,t | 第一、第三 |
| 44466 | 第一 | 無 |
| 44466 | 第二 | 無 |

兩個 literal 的全部16對都沒有零內點 completion；只有上述兩對有一內點 completion。
這些失敗僅限零／一內點控制，不能作任意大小原圖的排除。
型次序逐字沿用父證書 `surviving_types_after_same_initial_E_gate`；程式索引從0起算。

## 一張共同圖的完整面

target44459、03第二型 × 02第一型，加一點 X，色2；其14個三角面為：

```text
z3 z4 X       z4 V X        V U X         U Y X
Y q X         c s v         q c v         q v X
v w X         t a z1        t z1 z2       t z2 z3
w t z3        w z3 X
```

全部 boundary 色仍為 `03030101312012`，新增 X 色2；沒有獨立挑選 palette 的私有色。
其完整分量為：

```text
02/13:
 {a,z2,t}; {z1}; {z3,w}; {z4,U,s,v,X}; {V}; {Y,q,c}

03/12:
 {a,z1,z2,z3,z4}; {U}; {q,v}; {V,Y,w,t,X}; {c,s}

01/23:
 {a}; {z2}; {z4,V,U,Y}; {c,v,w}; {s}; {z1,z3,q,t,X}
```

所以同一張圖精確實現所指定的 02、03 完整 boundary partition。
01 卻把 a 與 z4、Y 分開，原四個必要型都不容許。
另一張控制只把上方部分改為 `z1 z2 X, z2 z3 X, t a z1, w t z1, w z1 X`，
完整面與分量逐份見證書；它實現第二個 03 型 × 第三個 02 型，01 同樣不過。

## 原來源反控制及完整內部 fibre

兩控制均不含原 S 非相鄰點之間的 chord，也不含 V–Y；失敗可更精確定位。
兩圖中 X 同時是 U、z4 的共同鄰點，也是 V、Y 的共同鄰點。
接回原 strip 的15個面及 z5 原六度 star 後：

```text
N(U)={V,Y,z5,X}，N(V)={z4,U,z5,X}。
```

故 U、V 各完整度4，違原來源最低內度5；亦正好違反
父審核幾何子項所證的原來源等式
`N_F(U)∩N_F(z4)={V}`、`N_F(V)∩N_F(Y)={U}`。
原 G 的兩個共同鄰點還各包含 z5；控制圖的 X 才是原 G 中被禁止的第三個共同鄰點。
這是實際同一圖的來源反控制，不能將控制圖當作原941完成。

固定每張控制圖完整 F 著色，接回原 P 與 z5 的所有原邊後，七點的完整 fibre 恰為父證書同六列。
證書逐列保存全部七點 tuple、原 D literal rim，以及原 G／Q1／J1 cap 的所有完整 assignments，
包含所有空列。各 canonical cap state 逐字對原凍結 authority 比較：
`43912,43912,44459,45552,43975,45615`。
這個初始同框的完整 fibre 接合未出現 forbidden cap，不能抵銷原01分量及度數失敗。

## 重播

```sh
python3 -B audits/2026-10-21-w7-I-joint-2c38d1d/controls/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-I-joint-2c38d1d/controls/check.py
```

兩次均 PASS；五個負控制拒絕冒稱來源實現、從有限失敗宣稱來源排除、冒稱01 gate通過、
刪面及刪完整七點 lift。`certificate-v2.json.gz` 的 SHA256 是
`d5ba42905c85acc9ac6b04fbd0a70dfd3d91ad0ba425f91dda9c1d7e1594205e`。
首版保留；v2增加原 canonical cap state 的明列與逐份 authority 比較，首版不再符合這個擴充 schema，
沒有數學結果改變。

結論限於：有兩個真正同圖的02／03共同控制，來源01及最低度門檻會拒絕它們。
任意大小共同來源、各 literal 的八對、V=w別名、整個型 I 均未由本子項關閉。
