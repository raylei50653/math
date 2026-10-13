# C5 雙拒絕分類：指定 disk sector 的一般 3903 排除

系列索引：[3903 導讀與推導順序](c5_sector_3903_guide.md)。

Lean 後續（2026-09-28）：[BoundaryDegree](lean_boundary_degree.md) 已形式化
§1 的實際接線、完整度數與拒絕迫緊／框色單射；Gallai palettes 及後續
disk 分類仍是下述紙面／外部定理層。

文件導引（2026-09-23）：本報告為雙拒絕分類的證據入口；
[Lean 共用引理](lean_two_rejection_tools.md) 僅形式化部分步驟，完整分類仍未形式化。
整合發布與驗證範圍見 [發布紀錄](STATUS_HISTORY.md#73-雙拒絕-lean-工具整合發布)；
下文「本次未 commit／push」保留匯入核對當時的語境。當前研究入口見
[HANDOFF](HANDOFF.md)。

日期：2026-09-22。狀態：**已逐節紙面核對並獨立重現有限主表；依賴外部 degree-list 定理，完整分類未 Lean 形式化；部分共用步驟已有 Lean 工具。**

使用者原稿完整保存在 [v1 原件](sources/c5_two_rejection_proof_zh_v1.md)，
SHA-256 `321dfa1204979c01eb5ee867aaa2afc53d8a5e8e56ef4e8bee4d060a7c3778e7`。
本整理版補明證明接點、區分原稿計算聲稱與本次重播，並新增
[獨立 checker](../scripts/c5_two_rejection_audit.py)／
[有限報告](../artifacts/c5_two_rejection_audit/observations.json)。
一般大小的結論來自 §1–7 的論證，有限零命中只作找錯；本次未 commit／push。

## 0. 精確命題與適用範圍

令 K 是有限簡單圖，指定 induced 框圈 Γ=(b0,b1,b2,b3,b4)，且有以 Γ 為外邊界的 disk embedding。這裡 b0 就是原 sector 的 z。令 C=K−V(Γ) 非空連通；每個內點在 K 中的完整度數至多 4，且 b0 恰有兩個不同內部鄰點。

令 G=K−{b0b1,b0b4}，只刪去這兩條框邊。顏色集合 U={0,1,2,3}，框染色依序為：

- α=(0,1,2,1,2)=01212；
- δ=(0,1,2,1,3)=01213。

α、δ 都是 K 的 proper 框染色，所以在 K 或 G 上問延拓，答案相同。

**分類定理。** 若 α、δ 都不能延拓，則交換兩個內點的名字後，必有

```
V(C)={u,v}, E(C)={uv},
A(u)={b0,b1,b2}, A(v)={b0,b2,b3},
A(w):=N_K(w)∩V(Γ).
```

換言之，剩下的不是某個抽象小代表，而是整張 sector 的實際接線只能如此。

**3903 推論。** 上圖的開口列 ε=01210 也被拒絕，因它和 α 只差 b4 的顏色，而 C 不鄰接 b4。因此不存在指定圖類中的 3903。完整十二位簽章的獨立計算為 1855。

這個命題不需要 minimality、397/330/331、Kempe 交換歷史，也不預設其餘八個 proper 列接受。它不適用於任意非平面圖；附件保留了簽章 3903 的非平面正控制。

## 1. 拒絕列使所有 lists 緊，並得到 block palettes

對 β∈{α,δ}，令 Lβ(v)=U\β(A(v))。有

```
|Lβ(v)| ≥ 4−|A(v)| ≥ deg_C(v).
```

若某點 x 有嚴格餘量，以 x 為根取生成樹，按子點先、父點後的次序貪婪染色。每個非根點至少留有一個未染父點；根最後因嚴格餘量也可染。這和拒絕矛盾。因此

```
deg_K(v)=4,
|Lβ(v)|=deg_C(v),
β 在 A(v) 上單射。
```

C 若只有一點，α 最多禁掉三色，仍至少留一色，所以此情形不可能。

使用 degree-list 不可染圖的標準 block 分解定理 [R1,R2]：C 是 Gallai tree；每個 block B 可配一個共同 palette P_B，使

```
Lα(v) = 不交聯集 {P_B : v∈V(B)}。
```

橋 block 的 palette 大小 1，奇圈大小 2，K4 大小 3。平面性排除 K5。不交性也可直接由度數等式核對：各 block 在 v 的度數之和等於
`deg_C(v)=|Lα(v)|`，各 palette 大小恰為該 block 度數；聯集已是 Lα(v)，
因此不可能有重疊。普通圖取 [R2] 的全正邊特例，Lemma 2.2 給共同
palette，Lemma 2.4 給各 block 的聯集分解。
δ 有自己的 palette 分解，且使用同一張 C、同一批實際 attachments；不把兩列的 root 資料混合。

**重要：P_B 是不可染 degree-list 的 block palette，不是假設 α 有一份完整染色，也不是從某次 Kempe 交換抽取的雙色分量。**

## 2. 兩缺口引理：唯一的 0/3 橋鏈

令 a,b 為 b0 的兩個內部鄰點。由 α 的特殊形狀：

```
3∈Lα(v) 對所有 v∈C 成立；
0∉Lα(v) 恰當 v∈{a,b}。
```

取所有 palette 恰含 0、3 其中一色的 blocks，組成輔助圖 D：

1. 每個這樣的 block 是 D 的一個節點。
2. 對 v∉{a,b}，若色 0 與色 3 分屬兩個 blocks，則在這兩個 block 節點間加一條以 v 標記的邊。
3. 對 a,b，各在其含 3 的 block 節點留一個半邊端口。

palette 的不交分解保證每種顏色所屬的 block 唯一。對任何 D 節點 B，其每個原頂點恰貢獻一條普通邊或一個端口，所以

```
deg_D(B)+ports(B)=|V(B)|。
```

D 是森林：把它的普通邊用相應割點細分，便是原 block-cut tree 的子圖。

對 D 的任一非空樹分量 T，數度數得到

```
ports(T)
 = Σ_{B∈T}|V(B)| − 2(|V(T)|−1)
 = 2 + Σ_{B∈T} (|V(B)|−2)。
```

每個 block 至少有兩點，因此每個分量至少需要兩個端口。全圖只有 a,b 兩個端口，故 D 恰一個分量，且所有節點的 block 都只有兩點。

因此，D 中全部 blocks 是 C 的真正橋邊，並串成 a 到 b 的簡單路徑 P：

```
a —— b        （最短情形）

一般情形的橋 palettes：{3},{0},{3},{0},...,{3}。
```

特別地，P 有奇數條邊、偶數個頂點。所有不在 P 的非橋 blocks，其 palette 要麼同時含 0、3，要麼兩色都不含。

這一步不使用平面性，也不使用 δ。

## 3. 非橋末端 block 最多一個

首先，每個 C 葉點的 list 只有一色。α 在其三個框鄰點上必須單射，因而其中必有 b0。所以所有 C 葉點都在 {a,b}，從而都在 P 上。

第 2 節已給出非空橋鏈；因此 C 若只有一個 block，該 block 只能是
單一橋邊，直接屬於後面的 C=P 情形。討論非橋末端 block 時，C 必有
多個 blocks，故可以令 B 是非橋末端 block，x 是唯一割點。其私有點的 Lα 恰為 P_B；所有 Lα 都含 3。由第 2 節，非橋 palette 不能只含 3 而不含 0，所以 P_B 必也含 0。於是 B 的任何頂點都不鄰接 b0。

因此 C 中存在一條從 x 經 B 外部到 a 或 b、再接 b0 的簡單路徑 Z。Z 除 x 外不碰 B，除終點 b0 外不碰框。

下面的拓撲排除是對 repo `c5_sector_terminal_blocks.md` 的末端 block 論證作前提抽離：需要的是兩列拒絕、實際 attachments、以及上述 Z；不需要原 397→330 的具名 w/b/corner。[R3]

### 3.1 K4 不可能

B 的三個私有點各有一個框鄰點。於 disk 外加 apex h，接全部五個框點，仍應平面。

把 K4 四點保留為四個 singleton branch sets。第五組取 h、私有點所接的框點、b0 及 Z 的內部；它連通，並鄰接 K4 的每個頂點。因此得到 K5 minor，矛盾。

這只是非平面證書，不宣稱是保持 boundary relation 的圖化約。

### 3.2 奇圈必有共同的實際 j∈{b2,b4}

奇圈的 P_B 大小 2，故 P_B={0,3}。每個私有點的實際框鄰集因此為

```
A(v)={i(v),j(v)}, i(v)∈{b1,b3}, j(v)∈{b2,b4}。
```

對 δ，其私有 list 是 {0,3}（j=b2）或 {0,2}（j=b4）。δ 也拒絕，故末端 block 的私有 lists 必共同。因此 j(v) 必在整個 block 一致，記為 j。

此處保留 b2/b4 的身份，沒有因 α 中兩者同色而合併。

### 3.3 長奇圈與其餘 triangle 類型排除

若圈長至少 5，將圈分成三個兩兩相鄰的連通 branch sets，各含一個私有點。另取 {j} 及 {h,b1,b3}。後兩組互相相鄰，且都鄰接前三組，構成 K5 minor。

故 B=xuvx 是 triangle。若 u,v 都選同一 i∈{b1,b3}，則兩側

```
{u}, {v}, {h,b0}∪int(Z)    versus    {i}, {j}, {x}
```

構成 K3,3 minor。故交換 u,v 名稱後，必為 A(u)={b1,j}、A(v)={b3,j}。

若 j=b4，路徑 b1−u−b4 與 b0−Z−x−v−b3 頂點互斥，卻有沿 Γ 交錯的端點 b0,b1,b3,b4，違反 disk 的 Jordan 分離。

因此任何非橋末端 block 只能是

```
B=xuvx,
A(u)={b1,b2}, A(v)={b2,b3}。
```

它在實際圖上鄰接三個不同框點 b1,b2,b3。

### 3.4 不能有兩個這樣的末端 blocks

若兩個末端 triangles 頂點互斥，將各 triangle 整體收成一個 branch set，再加外部 apex h；這三組與 {b1},{b2},{b3} 構成 K3,3 minor。

若兩者共享割點 x，x 的四條圈邊用盡度數，其他點均是私有點。C 連通便迫使 C 恰由這兩個 triangles 組成，沒有橋邊，與第 2 節的非空橋鏈矛盾。

所以：**C 至多有一個非橋末端 block。**

## 4. 橋鏈外至多一個分量

P 的每條邊都是 C 的橋。因此 C−V(P) 的任何連通分量 Q，最多只接到 P 的一個頂點 t；接到兩個不同頂點會繞過其中一條橋。

把 block-cut tree 朝 t 定根，Q 方向至少有一個末端 block。它不能是末端 bridge，因那會產生 P 以外的 C 葉點。故它必是第 3 節的非橋末端 triangle。

由非橋末端 block 至多一個，得到

```
C=P，或者 C−V(P) 恰有一個非空連通分量 Q。
```

在後一情形，Q（即使連同其接點 t 計算）確實接到框點 b1,b2,b3。若末端 triangle 的 root 恰是 t，其兩個私有點已在 Q 中提供全部三個 attachments；所以不需要另假設 root 位於 Q。

這一步沒有把 Q 的染色關係壓成 singleton，也沒有丟掉其內部 bridges。下一節的收縮只作拓撲限制。

## 5. 平面附件的次序引理

寫 P=p1…pn，其中 p1=a、pn=b。加上 b0p1、b0pn 得簡單圈 Ω。Γ\{b0} 在 Ω 的外側，因此所有從 P 接向 b1,…,b4 的邊都在 Ω 的同一外側。

將 b0 的接觸點切成兩個相鄰端點，可把兩圈之間的區域視為一條 disk strip。一側依序是 b1,b2,b3,b4，另一側是 P。在 b0 附近取足夠小的半圓鄰域，兩條 b0–P 邊都位於兩條框邊之間；
Γ−b0 連通且不碰 Ω，故全在 Ω 的同一側。沿 Ω 外側切開 b0 的接觸點，
得到 strip 的兩條相對邊界弧；它們在 disk 邊界的遍歷方向相反。
以下沿兩弧的同向橫向次序讀取框點與 P，因此可以只反轉 P 的編號，
不置換任何具名框點。把 P 的方向選對後，令

```
S_i={j∈{1,2,3,4}: p_i 鄰接 b_j}。
```

只要 S_i 都非空，就必有

```
max S_i ≤ min S_{i+1}。
```

理由：若某前點接較後的框點、某後點接較前的框點，這兩條邊在 strip 邊界上的端點交錯，必相交。這是對同一嵌入的 Jordan 論證，沒有拼接不同染色的路徑。

從而

```
Σ_i (max S_i−min S_i) ≤ 4−1=3。
```

若一個連通內部子圖只接 P 的一個頂點 t，把它收進 t 後仍有固定框圈的 disk embedding，這個次序引理仍適用；S_t 會包含該子圖的全部框附件。

## 6. 排除 Q 非空

假設第 4 節的 Q 非空，將 Q 收進它唯一的 P 接點 t。所得 S_t 至少含 {1,2,3}，寬度至少 2。

對 P 上其他每點，由完整度數 4 與 α 的單射性：內點有兩個框鄰點，端點有 b0 及另外兩個框鄰點；除 b0 外，必各選一個 {b1,b3} 和一個 {b2,b4}。所以每個其他 S_i 的寬度至少 1。

第 5 節便給出

```
(n−1)×1+2≤3，故 n≤2。
```

P 本來至少有兩點，故 P 恰為 t−u。次序引理進一步迫使

```
S_t⊆{1,2,3}，且包含 {1,2,3}；
S_u={3,4}。
```

因此在未收縮的實際圖中，b4 唯一的內部鄰點是 C 葉點 u，且

```
A(u)={b0,b3,b4}, Lα(u)={3}, Lδ(u)={2}。
```

令 H=C−u。H 連通，且 H 上 α、δ 的 lists 完全相同，因為 H 沒有 b4 附件。u 的唯一內鄰點是 t；刪 u 後 t 有嚴格 list 餘量 1，其餘點仍有至少 degree 個可用色，故由第 1 節的生成樹貪婪法，H 至少有一份 list 染色。

α 拒絕表示每份 H 染色都必令 t=3，否則可補 u=3。δ 拒絕又表示每份**同一個 H list 問題**的染色都必令 t=2，否則可補 u=2。

H 的染色集合非空，不能同時被要求 t=3 與 t=2。矛盾。

故 Q 不存在。

## 7. 剩下的路徑必是二內點控制

現在 C=P。每個 S_i 都是從 {1,3} 與 {2,4} 各取一個的二元集合，寬度至少 1。次序引理給 n≤3。第 2 節又給 n 為偶數，故 n=2。

兩個 C 葉點均接 b0，另外的框附件記為 {i_u,j_u}、{i_v,j_v}，其中 i∈{b1,b3}、j∈{b2,b4}。

在 δ 下，葉點 list 是 {3}（j=b2）或 {2}（j=b4）。兩點以一條邊相接而不可染，恰要求 j_u=j_v。

若都取 b4，兩個附件區間都具有右端 4，且各有另一個較小端點，違反次序引理。若都取 b2，唯一可排序的組合是

```
{b1,b2}，{b2,b3}。
```

故分類定理所列接線是唯一可能。其 b4 沒有內部鄰點，所以 ε=01210 的內部 list 問題與 α 相同，也被拒絕。一般 3903 排除隨之得到。∎

## 8. 與五個既有目標的關係

十二位順序沿用 repo `c5_sector_targets.md`。以下由位元直接計算：

| mask | 被拒絕的測試索引 |
|---:|---|
| 3647 | 6,7,8 |
| 3703 | 3,7,8 |
| 3895 | 3,6,7 |
| 3901 | 1,6,7 |
| 3903 | 6,7 |

第 6、7 列是 α、δ，第 11 列是 ε。

因此本文分類定理在 §0 的圖類內同時排除 3647、3895、3901、3903：這四個都拒絕 α、δ 卻要求 ε 接受。3703 沒有拒絕 α，不在本引理的涵蓋範圍。

這不等於已證 K∞=K≤5，也沒有自動解決 R31 或共同出口的其他缺口。

## 9. 本次獨立有限重播

原稿只提供 Markdown，未附所述 Python 程式。本次重新撰寫
[c5_two_rejection_audit.py](../scripts/c5_two_rejection_audit.py)，不匯入 repo
著色／palette helpers，也不讀舊 JSON。NetworkX 固定為 3.6.1。
從至多七點的 atlas 取所有必要 Gallai skeletons，枚舉各 block palettes
及所有實際 attachments；只使用緊 degree-list 必要條件，不預先用橋鏈
或本分類定理篩掉候選。相同 lists 去重，避免 palette 表示重複計數。
每份 α 以直接回溯核對拒絕；每份 δ 的直接回溯與完整 root block peeling
逐筆比對。disk 判定使用加外部框 apex 的 planarity。

| 內點數 | α 拒絕的接線指派 | α、δ 都拒絕 | 其中 disk |
|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 16 | 8 | 2 |
| 3 | 0 | 0 | 0 |
| 4 | 256 | 64 | 0 |
| 5 | 512 | 96 | 0 |
| 6 | 4,224 | 552 | 0 |
| 7 | 24,576 | 1,920 | 0 |
| 合計 | 29,584 | 2,640 | 2 |

完整重現原稿主表。兩個 disk 接線只是內點換名，逐一驗證全部十二列，
簽章均為 1855；另獨立找到並保存四內點非平面 3903 正控制。
上表是 atlas representatives 的附件指派數，不是完整圖同構類數。

原稿另聲稱 1,548 個路徑／1,968 個旁支模板，因未附模板定義與腳本，
**不將這兩個數字視為已重播**。本次另明確枚舉 n=2,…,5：每普通路徑點
從 {12,14,23,34} 選一對；旁支收縮點改選 {123,1234}，遍歷全部位置。
共 1,360 個純路徑、3,184 個旁支模板，逐一比較 disk 與正／反向單調
區間判準，全部一致。這些收縮模板只檢查拓撲，不聲稱保持 degree 或 lists。

```bash
uv run --with networkx==3.6.1 python scripts/c5_two_rejection_audit.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
lake build
git diff --check
```

不帶 `--check` 僅重建本報告 JSON；`--check` 重新計算並比對，含程式 hash。
兩份前置 checker 重播使用已存證書，不重建舊 artifacts。其餘 sector／R 系列
standalone 未重跑。atlas 完備性與 planarity 信任 NetworkX；外部定理與
任意大小 Jordan／minor 論證仍是紙面層，Lean build 不驗證本文定理。

## 10. 紙面 review 結論與停止點

本次逐節核對 §1–7，未發現論證缺口，並作以下明確化：

- §1 的 palette 不交性由聯集分解與緊度數求和推出，兩列各用自己的分解。
- §2 的每個 D 節點逐原頂點貢獻一次；普通邊細分嵌入 block-cut tree，
  兩端口計數強迫唯一橋鏈。此步不依賴平面性或第二拒絕列。
- §3 的非橋末端 block 必有唯一割點；非空橋鏈排除整圖只有一個非橋 block。
  palette 含 0 使 a,b 不在 B，因此到 b0 的實際 Z 在 B 外，舊 topology 可適用。
- §5–6 的收縮僅限制實際附件聯集。刪葉後的 H 使用原圖相同 lists，
  先由嚴格餘量證有染色，再用互斥 root 強迫矛盾；不在收縮圖上做 list 推論。

因此接受本文為 §0 圖類的**一般大小紙面分類**：四個目標
3647、3895、3901、3903 排除。這使舊 3903／331 分支不再是優先入口；
不需要逐個枚舉 397 的抽象後繼，也不自動刪除 603 profiles 或重算閉包。

下一個窄入口是 [五目標](c5_sector_targets.md) 中仍未涵蓋的 **3703**：
它接受 α、拒絕 δ，不能使用兩拒絕前提。先研究其實際 disk 接線與額外
開口列限制，不重開已完成的 3903 分支枚舉。
R31、一般 degree-5、共同出口與 `K∞=K≤5` 未由本文解決；未新增 Lean theorem。

## 11. 後續 Lean 證明工具

[共用工具與依賴表](lean_two_rejection_tools.md) 已補九個普通 Lean 引理，
涵蓋 §1 的連通圖貪婪餘量與拒絕迫緊、§2 的兩端口計數核心、
§5 的區間寬度求和、§6 的同圖刪葉矛盾及 §7 的框列 list 等式。
這不改變 §10 當輪的歷史核對紀錄；完整分類仍需外部 degree-list、
block-cut 橋鏈與 disk 拓撲的形式化，具體缺口逐項列在新報告。

## 來源

[R1] Cranston–Rabern, *Beyond Degree Choosability*, arXiv:1511.00350。標準 Gallai/degree-choosability 敘述。
[arXiv](https://arxiv.org/abs/1511.00350)

[R2] Schweser–Stiebitz, *Degree choosable signed graphs*, arXiv:1507.04569，Lemma 2.2、2.4。取所有邊為正的普通圖特例，得到共同 block palettes 與不交拼接。
[Lemma 2.2、2.4 原文](https://arxiv.org/html/1507.04569v1)

[R3] `raylei50653/math/docs/c5_sector_terminal_blocks.md`，本次讀取的 blob SHA：`7bbcfb60305c2642165cca76ba7f1702a2d56afc`。使用其末端 odd-cycle/K4 root 與拓撲論證，重新列明抽離後前提。
[本地報告](c5_sector_terminal_blocks.md)

[R4] `raylei50653/math/docs/c5_sector_rejection_lists.md`，blob SHA：`1e3fc43199f9fa50160fe094897964f990104871`。緊 list 與實際框鄰集。
[本地報告](c5_sector_rejection_lists.md)

[R5] `raylei50653/math/docs/c5_sector_331_barriers.md`，blob SHA：`fbfbecb714ca24ac11a76dd6fa71c0b2e8396c9f`。本次起始的 331 分支前提；本文最終不以它作分類定理的依賴。
[本地報告](c5_sector_331_barriers.md)

[R6] NetworkX `graph_atlas_g` 官方說明：至多七點的 graph atlas。
`https://networkx.org/documentation/stable/reference/generated/networkx.generators.atlas.graph_atlas_g.html`
