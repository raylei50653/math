# 兩個 target 的完整來源交換與五型殘餘

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
承接 [BASE](../BASE.json)、[原來源契約](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
及[完整計數證明](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)。
本項不求解 LP，不枚舉原圖，不假設外側私有圖有反射或交換 v,w 的自同構。

## 1. 補償不等式的精確地位

既有整數恆等式為

\[
2Z_{44459}=P-N,
\quad P=\sum_{103\text{ 個 }+1\text{ 欄}}X_j,
\quad N=\sum_{95\text{ 個 }-1\text{ 欄}}X_j+
2\sum_{8\text{ 個 }-2\text{ 欄}}X_j.
\]

因此，在既有方程與非負性之下，提議的 `P≤N` **等價於**
`Z44459=0`，並非額外已證的必要條件。這是正確的待證改寫；要有新內容，
必須給出同一原來源上的完整作用、帶私有分量重數的 injection，或新的幾何／
最小性限制。不能僅因列出正價與負價欄就推出補償。

## 2. 不需自同構的條件交換引理

固定同一完整核心
`D=G−{b,p,h,R,x,y,r}`，有序 rim 為
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`。兩個 target 的字面色框為

```
A = (0,1,2,1,2,1,2,3,1,2,0,1,2),  canonical ID 44459;
B = (0,1,2,1,2,1,2,3,1,2,1,0,2),  canonical ID 44466.
```

對 D 的一份完整著色，令 K 為實際 01-induced graph 中含 v,w 的連通分量；
原邊 vw 保證兩點同在 K。稱它為 **separated stratum**，若

\[
K\cap\{a,n,u_3,u_1,c\}=\varnothing.
\]

這正是 K 在 rim 上恰接觸 v,w；其內部可以含任意多原私有點。
交換 **整個實際 K** 的 0,1 色，給出 A 與 B 的 separated strata 之間的
雙射：其餘 rim 顏色不變，v,w 色交換；01-induced graph 本身及其分量不變，
因此再作一次恰回到同一份完整著色。全部私有點保留並隨同作用，不需逐片
正規化，也不需補滿選路殘餘。故

\[
N_A^{\rm sep}=N_B^{\rm sep}.
\]

這是任意固定原核心上真正的完整著色雙射。它只對這個 stratum 成立；
不能推出 `Z44459=Z44466`。若 K 還接觸 a,n,c 等原 rim 點，交換它會改變
那些框色，結果便不是另一個 target。

此計數一直使用 D 的全部完整 fibres。沒有把選定 type III 見證的子集
當作交換不變來源，也沒有宣稱交換後保持該額外歷史標籤。

## 3. 凍結完整 orbit 家族把例外收斂到各五欄

使用兩個 target 的 **01|23** half-row，字面 palette word 相同，均為
`0010101101001`。在全部 307,197 個凍結 surviving columns 中，每個
half-row 恰有 10 個欄；有 5 個共同欄，另外各 5 個專屬欄：

| 類別 | 完整原欄 ID |
| --- | --- |
| A、B 共同 | 43335, 43336, 48620, 66584, 67756 |
| 僅 A | 43330, 43331, 48617, 66582, 67755 |
| 僅 B | 43380, 43381, 48647, 66602, 67765 |

每欄保留 16 個完整 normalized half-rows，對應 6 個 boundary components。
[精確輸出](target_exchange.json) 保存全部 15 個欄的所有 half-rows 與
原 rim component blocks，沒有僅存個別接觸或 pair marginals。

**Component reconstruction.** 對一欄 C 選一份 reference row t0，對每個
rim 點 i 記錄它在整欄各 row 的 XOR variation profile
`d_i(t)=(t_i xor t0_i)&1`。同一 palette 內，i,j 屬於同一實際 component
恰當 `d_i=d_j`。同分量共同翻色，給出正向。若為不同分量，每個 palette
只有一個 normalization anchor component，故兩者至少有一個可獨立翻色，
給出不同 profiles，反向亦成立。比較時必須先限制同一 palette。

因此 anchors 不會混同同 palette 的不同 components；private components
只影響原 X 的重數，不改變這些 profiles。不同 boundary partitions 不會
因為 normalized-column 去重而在此混同。checker 另從恢復的 6 個 blocks，
固定每個 palette 的 anchor，獨立翻其餘 4 個 blocks，逐列重生 16 個 rows
並要求與原欄完全相等。使用 absolute low-bit profiles 會把同分量中原本
異色的相鄰點錯分；本 checker 使用 XOR profiles。

恢復的 15 欄全部具有以下必要結構：

- a,n,c 總在同一 01-component。
- 共同 5 欄：K 的 rim contact 恰為 `{v,w}`，而 s,t 在同一 23-component。
- A／B 專屬各 5 欄：K 與 a,n,c 在同一 01-component，可能另含 u3、u1；
  s,t 則在不同 23-components。

五種中間 block 結構如下。令 C0 為含 a,n,c 的 01-block，Q 為含 L,q 的
23-block；表中未與 C0 合併的 u3／u1 依表列保留。

| 型 | u3,u1 的 01 歸屬 | u4,u2,L,q 的 23 歸屬 | A 專屬 | 共同 | B 專屬 |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | `{u3}`, `{u1}` | `{u4,u2,L,q}` | 43330 | 43335 | 43380 |
| 2 | `{u3,u1}` | `{u4,L,q}`, `{u2}` | 43331 | 43336 | 43381 |
| 3 | `{u3}`, `u1∈C0` | `{u4,u2}`, `{L,q}` | 48617 | 48620 | 48647 |
| 4 | `u3∈C0`, `{u1}` | `{u4}`, `{u2,L,q}` | 66582 | 66584 | 66602 |
| 5 | `u3,u1∈C0` | `{u4}`, `{u2}`, `{L,q}` | 67755 | 67756 | 67765 |

專屬欄的 C0 包含 v,w，且 s,t 各自成 block；共同欄的 C0 不含 v,w，
另有 `{v,w}` 與 `{s,t}` 兩個 blocks。表內「專屬」只指兩個具體 target
half-rows 的 incidence，不表示該欄只含一個 canonical state。

這是凍結完整必要家族的精確有限分類。沿用既有 orbit coverage 紙證，它
適用於每個可能的實際原來源；沒有據此斷言任一欄已被原圖實現。

## 4. 十項差恆等式與後續真正待證的部分

令 U 為共同 5 欄的 X 之和，V_A、V_B 為各自專屬 5 欄的 X 之和。
兩條原 half-row 方程逐項給出

\[
2Z_{44459}=U+V_A,\qquad
2Z_{44466}=U+V_B,
\]

所以

\[
2(Z_{44459}-Z_{44466})=
X_{43330}+X_{43331}+X_{48617}+X_{66582}+X_{67755}
-X_{43380}-X_{43381}-X_{48647}-X_{66602}-X_{67765}.
\]

U 恰是實際 separated-stratum orbit 的共同貢獻；依原方程尺度，
`U=2N_A^sep=2N_B^sep`，與第 2 節的原來源雙射一致。
若以其他論證取得 `Z44459=0`，非負性便同時迫 `U=V_A=0`，留下

\[
2Z_{44466}=X_{43380}+X_{43381}+X_{48647}+X_{66602}+X_{67765}.
\]

故第二個 target 無需籠統假設對稱；剩餘問題明確落在五個 **joined**
接觸型上。然而目前沒有證明 U、V_A、V_B 為零，沒有證明 joined stratum
空，也沒有一般 `Z44459=Z44466` 的等式。

## 驗證與邊界

`target_exchange.py` 僅讀凍結 caps／orbits，釘死 gzip bytes SHA256，逐欄
掃描兩個具體 target 的完整 incidence，重建上述原 component blocks，並在
全部原 X 座標核對差恆等式。改一欄的一個 row 會被完整 coset 重建拒絕。
normal、seed17、seed17 加 `-O` 皆使用同一份唯讀輸出；沒有 solver import。

此結果是一條條件來源雙射與有限必要分類，不是嚴格 W7 排除、共同可行解、
原圖實現、smaller bad、一般 J1/J2 或 Lean 定理。嚴格 W7 仍 OPEN。
