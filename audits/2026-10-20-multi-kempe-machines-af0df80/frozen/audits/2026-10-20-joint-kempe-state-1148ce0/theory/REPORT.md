# 同一染色的聯合 Kempe 狀態：精確契約與 J1 接口

本頁固定父 audit 的 BASE 與凍結輸入。結果是**一個精確的狀態／操作契約**：
六個色對分割必須由同一份完整染色共同產生；它們決定接框 component
swap 的新框色，以及兩個不變色對，但四個混合色對必須另有刪除後的
分量及實際附件資料。本頁整理一個足夠的單步 descriptor，沒有證明它能
有限閉合成遞迴狀態機，也沒有排除 J1 的兩個殘餘 fibres。

單步 surgery 使用既有
[connectivity §1](../frozen/docs/c5_kempe_connectivity.md#1-一次交換的六個色對)
及該頁記載的既有普通 Lean 結果；不是本輪新證或新 Lean。
J1 則完整承接凍結
[來源契約](../frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/SOURCE_CONTRACT.md)、
[八 fibre 證明](../frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/J1/PROOF.md)、
[兩 fibre 與分層雙射](../frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/REPORT.md#2-j1兩個目標之間只有分層雙射)、
[同染色幾何](../frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/geometry/PROOF.md)。

## 1. 狀態以一份完整染色為單位

固定一張實際有限圖 H、具名且有序的 interface T，以及完整 proper
四色染色 `c:V(H)→{0,1,2,3}`。若 H 是來源核心 F，H 包含全部原私有點；
原 plane embedding、rotation、附件及其來源身份另保留，沒有被狀態取代。

對每個無序色對 ab，定義

```
T_ab(c) = {t in T : c(t) in {a,b}},
π_ab(c) = partition of T_ab(c) induced by all actual ab components of H.
J_T(c) = (c|T, π_01(c), π_02(c), π_03(c), π_12(c), π_13(c), π_23(c)).
```

每個 block 含該實際 component 的全部 interface contacts；空 `T_ab`
給空分割。私有點不出現在 block 名單中，卻全部參與判定連通。
六個分割與 `c|T` 共用**同一個 c、H、字面色框及接點身份**。

對固定字面 `f` 和摘要 `j`，完整 joint fibre 是

```
Ω_H(f,j) = {c in Col_4(H) : c|T=f and J_T(c)=j}.
```

必要時保留其基數；空 fibre 不刪除。整個來源的 joint relation 必須先
由實際 `c` 形成，再作投影。不能把逐色對可行分割作 Cartesian product，
也不能把兩個不同 c 所給的路或 component 當成共同存在。

此摘要保存了六色對的**觀測相容性**，尚未保存 swap 後繼的充分資料。
即使兩份染色有同一 J，也不因此有相同一步後繼。

## 2. Action grammar 與六分割確定的部分

先明確區分兩種 grammar。

* **接點指定的 action** `(ab,t)`：要求 `t∈T_ab(c)`，交換唯一實際
  `ab` component `S=Comp_ab^c(t)`。若 t,u 在同一 block，兩個名字
  指同一實際操作；若枚舉 moves 或計數，應按 component 去重。
* **全部實際 component actions** `(ab,S)`：亦含 `S∩T=∅` 的 hidden
  components。六分割看不到它們的數目、身份與 mixed-pair 影響。
  不能將多個 hidden components 合為一個空 block。

對第一種 grammar，J 確定 S 的接點集合 B，以及逐接點新字面色：
恰在 B 內交換 a,b。J 也確定交換後 `π_ab` 與互補色對 `π_de`：
兩個 induced graphs 均不變。其餘四個色對的分割未由此推得。

hidden action 的框色完全不變；其 mixed-pair 分割仍可能改變。
因此若只准接點指定 actions，這是明列的 grammar 限制；若目標是
完整 Kempe 可達性，須保留 hidden actions 或另外證明可消去它們。
「框色不變」不等於摘要不變，更不等於可刪去該步。

### 六分割恰等於深度一的字面框色觀測

此處 grammar 包含所有 `(ab,t)`，且不因新框色離開某個特定 fibre
而刪去 action。非法 action 的輸出以 `⊥` 記錄。定義

```
O_1(c) = (c|T, ((c^(ab,t))|T or ⊥)_(ab,t)).
```

對同一組具名 T、同一字面色框的任意兩份完整染色 c,d，

```
J_T(c)=J_T(d)  if and only if  O_1(c)=O_1(d).
```

**證明。** J 決定每個 root 的色，因而決定 action 合法性；合法時，
π_ab 給出含 t 的 block，而輸出恰在該 block 交換 a,b，故 J 決定
O_1。反過來，對每個 `t∈T_ab(c)`，比較原字面與 `(ab,t)` 輸出；
所有且只有 t 所在實際 component 的 interface 頂點改色，因 a≠b，
故其差異位置集合恰為 π_ab 中含 t 的 block。逐 root 取這些集合並
去重，重建 π_ab；若 T_ab 為空，重建空分割。六個色對同理。□

所以這份 joint 摘要是精確的**一次動作觀測**，不是任意深度的未來
行為碼。它把同一染色的六種 component 觀察綁在一起；要讀出第二步
或更多步的字面結果，仍可能需要額外內部資料。
上述等價不適用於先刪除「離開固定 J1 fibre」actions 的受限 grammar。
此命題是本輪對狀態觀測深度的紙面整理，沒有新增 Lean。

若另外把私有頂點加為觀測 pin，卻仍只允許原邊界作 root，需區分
「觀測 interface」與「action roots」。O_1 只能恢復碰到某個允許
root 的接點 blocks；新增 pins 之間、且不碰任何允許 root 的
component 分割未必能恢復。這時擴大後的完整 J 一般比該 grammar
的一次觀測更強，不能直接套用上面的雙向等價。

## 3. 精確單步 descriptor：刪除後分量與 attachment quotient

固定一次實際 ab component S。對每個外部色 d，重建新色對 ad：

```
H_ad^- = H[(c^-1(a) \ S) union c^-1(d)],
U_b = S intersect c^-1(b).
```

descriptor `Q_ad(c,S)` 保存：

1. `H_ad^-` 的**全部** connected components，每份收縮成一個節點；
2. U_b 的每個實際頂點各一個新節點；
3. 若 z∈U_b 的實際 d 鄰居在 residual component K 中，加入邊 zK；
4. 每個將出現在新 ad interface 的具名接點，指向其 residual 節點
   或其新增頂點節點。新 isolated 節點及無 interface 的節點也保留。

由既有 surgery，將 Q 的連通分量拉回接點，恰得 `π_ad(c^S)`。
另三個 mixed pairs 作同一構造：新 bd 刪原 b∩S、加入原 a∩S；
外部色 d 逐一取兩種。四個 quotient 共用同一 c,S，不能獨立挑選。

所以 action-marked descriptor

```
D(c;ab,S) = (J_T(c), S∩T, Q_ad, Q_ae, Q_bd, Q_be)
```

在 S 已驗為合法實際 component 的契約下，精確決定 `J_T(c^S)`。
這是既有 surgery 的直接 corollary，無額外平面性前提。

這裡有兩項不能省略的界線：

* 必須先刪 S 的相應顏色頂點，再取 residual components。舊 component
  可在刪除後分裂；先收縮舊 component 會遺失此資訊。
* residual 節點上保留的單個 attachment 非空性不夠；新連通可經過
  多個 stars。完整 quotient 的連通關係才是精確答案。

Q 並非宣稱最小充分摘要。對一個指定 action，只保留 Q 在新 interface
上的連通分割也足以讀出輸出，但那等於把該一步的答案存入狀態，
未解決如何從較小、可更新的來源資料算出它。

而且 D 僅為**單步充分**：知道 D(c;S) 並沒有給出下一份
`D(c^S;S')`。若要多步使用，必須保留可重算的實際染色與圖，
或另證 descriptor 的合法性與後繼更新在同摘要間相容。

## 4. 固定 J1 來源的必要 joint 類型

只在原 `a1=N01232(Q1)=0` 分支。原圖、全部附件、私有點、plane
rotation、非邊、完整 stars、口袋定理與全域最小性完整承接上述來源
契約；不增加 matching 前提，不使用四色定理。

共同實際核心與 ordered rim 固定為

```
F=G-{b,p,h,x,y,r},
T=(a,n,R,L,q,c,s,v,w,t).
```

此節不變換 F 或色框。兩個目標是

```
B_e = Col_4(F; (0,1,3,2,3,1,2,e0,e1,2)),
e=(0,1) or (1,0).
```

每份染色以原 `b=2,x=0,y=1,r=3` 及原附件唯一接回相同 J1 的
字面 `01021`。前輪只證最後拒絕為零等價於兩個 B 都空；
**沒有**證明原 J1 每份拒絕著色都直接落在這兩個 B，或其拒絕計數
等於 `|B_01|+|B_10|`。八 fibre 的完整計數式仍按原證明保留。

以下固定同一份 `c∈B_e`。記 z0,z1 為原 v,w 中色為0,1者。
凍結來源結論給 `01|23` 恰有兩個必要接框型：

| 名字 | π_01 | π_23 |
| --- | --- | --- |
| S（分開） | {a,n,c}, {v,w} | {R,L,q}, {s,t} |
| M（合併） | {a,n,c,v,w} | {R,L,q}, {s}, {t} |

同一份 c 的 `03|12` 又必屬以下三型：

| 名字 | π_03 | π_12（尚須插入 z1） |
| --- | --- | --- |
| I | {a}, {R,q,z0} | {n,t}, {L}, {c,s} |
| II | {a}, {R,z0}, {q} | {n,t}, {L,c,s} |
| III | {a}, {R}, {q,z0} | {n,L,t}, {c,s} |

若 z1=w，插入包含 t 的12 block；若 z1=v，插入包含 s 的12 block。
故所有十個具名 rim 頂點在相應色對中均有位置，未把 v,w 的原身份
丟掉。其餘 `02|13` 仍屬完整 J 的一部分，並未被這個二座標投影替代。

定義實際 joint 子fibres

```
B_e^(u,v) = {c in B_e : its 01|23 type is u and its 03|12 type is v},
u in {S,M}, v in {I,II,III}.
```

這六格是**共同染色的分類索引**，每格可以是空的；沒有宣稱六格各有
來源實現，也沒有把兩個必要 family 的乘積當成充分條件。
只有實際 `c` 才能為一格提供見證。既有來源幾何逐格適用為：

| joint 格 | 來自同一 c 的必要條件 |
| --- | --- |
| S,I | 真實03 R—q路≥4；23 s—t路≥4；01/03/23三路有相容交會 |
| S,II | q 的03 rim block 是 singleton；可作下節的01次序交換 |
| S,III | 12 n—L路為≥5或具名原R的W5三邊例外；另有三路相容交會 |
| M,I | 真實03 R—q路≥4；01含a,c,v,w；23的s,t分開 |
| M,II | q 的03 rim block 是 singleton；01含a,c,v,w；23的s,t分開 |
| M,III | 同一n—L路長/W5分支；01含a,c,v,w；23的s,t分開 |

表中「三路相容交會」精確沿用凍結幾何：在S且I/III時，取同一 c
的01 a—c路P、03 q—z0路Q、23 s—t路S23，Q上依序存在私有
`x0∈P`、`y3∈S23`，中間開段避開另兩路。它是來源必要幾何，
不是矛盾，亦未給任何路長上界。

## 5. 固定字面 J1 fibre 的單步 action 邊界

若只觀察 `B_01 union B_10` 中、單次 component swap 前後均留在該
集合的 actions，則可從字面色列直接確定全部**可見**動作：

* 兩個目標字面只差原 v,w 的0/1次序。所以任何可見單步必為01 swap，
  必須同時改 v,w，且不能改 a,n,c；其 component 的 rim block
  必為 `{v,w}`。
* 這一 block 恰在 S 層存在。交換其實際完整01 component 得到另一個
  B 的 S 層著色，且操作為對合。這重述既有分層完整-fibre雙射。
* M 層沒有這個可見單步：含 v,w 的01 component 也含 a,n,c，
  會改原字面框，不能算作所要求的固定框次序交換。
* 每個與 T 不相交的 hidden component swap 都保留完整字面 f，
  也保留原固定 cap 可接回性。它可能改變 mixed-pair 分割及所在
  joint 格，必須在完整 grammar 中保留。

交換S層的01 component雖保留01與23分割，**未證保留I/II/III型**；
03與12都是這次操作的混合色對。不能把已有S層總雙射升格成六格中
逐格的雙射。反過來，hidden mixed swaps 也未證保持S/M分層。

一般 root swap 若離開這兩個字面目標，仍可能是 F 上合法的 Kempe
move；但它沒有因此成為原框固定的 J1 fibre transition。更大的探索
grammar 可容納它，前提是逐步保留實際 F 染色、完整 cap lifts 與
對應的字面目標；不能自動用全域換色或改框補回同一列。

## 6. 遇到六分割碰撞後的下一個具體 refinement

第一步保留實際染色作 ground truth，在同一實際圖上比較同一摘要的
兩份 c,d，固定相同 root action `(ab,t)`，核對新 J 是否相等。
此為一般狀態充分性的負控制；小 disk 的碰撞不等於原941來源反例。
若碰撞，逐個 mixed pair 比較四個 surgery quotients，區分：

1. 刪除相應 S 顏色後，接點在 residual components 中的分裂不同；
2. residual 分裂相同，但新增 stars 的附件與連通不同。

先加入導致該碰撞的 action-marked residual/attachment 資料，再測試
相同動作的一步 congruence。若希望把所有 root actions 一起做成候選
狀態，可保存全部 action 的此類描述，但仍須測試它在 swap 後能否
相容更新；descriptor 數量亦沒有一般有界性結論。

在一張固定有限圖上，可另外以實際完整 colouring action graph
反覆細分 J，直到同塊 states 對每個標籤具有相同合法性與後繼塊集合。
這符合既有
[Phase B §4.2](../frozen/docs/c5_phase_b_common_lemmas.md#42-b-rd允許操作與完整fibre的多步充分性)
的 bisimulation 準則。其有限終止只因該固定圖有有限份染色；不給任意
大小 F 的有限狀態定理，也不給 bad→success∨smaller-bad。

因此目前最適合保留的三層是：

* 實際完整染色與實際 action edges：正確性基準；
* 六分割 J：同染色 joint 觀測層，可用來找碰撞；
* action-marked surgery descriptor：精確單步解釋層，遞迴充分性仍待證。

本頁沒有新的來源實現、最後拒絕為零、較小 bad、或 Lean 結果。
