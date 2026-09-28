---
docgraph:
  id: c5.single-spoke-cross-row
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-frame-arc
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-two-two
---
# Single-spoke (2,2)：跨列 residual 換色與 record 16 的 p₁ 延拓

2026-09-28，檢視基準 `0242605`。本輪獨立審查使用者貼出的推導，再接回既有
必要表。所連研究筆記、checker、JSON 不在本工作環境；本頁控制由訊息與 repo
重建，沒有宣稱重播附件的 560 個 minor／6 個負控制。優先序見 [HANDOFF](HANDOFF.md)。

**record 16 的 p₁=01021 延拓成立，兩個指定 p 均已證。** 同一分量的兩列
雙禁色證書共用原 bridge 路徑及全部旁支塊；局部 boundary rows 按置換對齊，
residual 就須按同一置換搬運。這迫使每塊實際接 b1、b2，原 spoke 完成 K5。

掃過 [frame-arc 層](c5_single_spoke_frame_arc.md) 的 66 個未決查詢，新增
**16 個指定列延拓**：2 個只需合併兩列各自的穩定子限制，其餘 14 個用到跨列
置換條件。來源排除仍為 **272 筆**，保留 **108 筆／54 型**；A/A、A/?、?/A、
?/? 為 **74、8、10、16**，即 **34 筆含未決項、50 個單列查詢**。
本輪只有條件式延拓，未排除更多來源、未證可實現性或完整 relation。
任意大小結論是紙面證明＋外部 degree-list 定理；Python 核對有限代數、minor
skeletons 與套表。**沒有新增 Lean theorem。**

## 1. 同一來源、任意拒絕列與共用路徑

完整沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) §1–3：G 有限簡單，
B=(b0,…,b4) 為 induced-C5 disk 外框，有效 H 連通；G 為 edge-minimal
q=01012 obstruction，唯一完整 degree-5 點 z 僅有 spoke zb_s，其餘內點
完整 degree=4。H−z 的 C0、C1 各有兩個不同的原有序接點 (u_k,v_k)，
S_k 是全部實際 boundary 支援。U={0,1,2,3}，p₁=01021、p₂=01212。
套既有保留表才另要求來源接受 T4；record 16 的推導不需要 T4。

對 proper row t，R_k(t) 保留同一完整 C_k coloring 的有序接點 tuple。
忽略 z 色時，boundary lists 至少為內部 degree，在接點嚴格多一色；
連通圖的嚴格多色貪婪引理給 **R_k(t) 非空**。故

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\quad |F_k(t)|\le2,
\qquad Z_G(t)=(U\setminus\{t_s\})\setminus(F_0(t)\cup F_1(t)).
\]

若 c∈F_k(t)，從兩接點 lists 去掉 c，即得到同一連通分量上的不可著色
degree lists。[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 blockwise-uniform palettes；本輪已讀取並核對原文。
前報告已將此步用於任意 target，**不需要 target minimality**。
來源的 K4-free 結構沿用原化約，因此 blocks 只有 bridges／odd cycles。

固定同一 C=C_k 及同一對原接點 u,v。若 proper rows q,r 均有雙禁色
F_q、F_r，分別比較各列的兩份拒絕 palettes，
[雙禁色路徑化約](c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)
給 u–v 的奇數長原 bridge 路徑 P=(x0,…,xℓ)，ℓ≥1。
因它的每條邊都是原圖 bridge，u–v simple path 唯一；**兩列給同一條 P**。
刪除全部 P 邊後，含 x_j 的分量 W_j 因此也完全相同，且兩兩不交。
每塊只含一個路徑點與它的全部旁支；所有 boundary 附件、原 bridges、
接點方向和 component identity 均保留，沒有逐列重選一張圖。

## 2. 跨列 residual 換色引理

T_j⊆S_k 是整個 W_j 的實際 boundary 支援，**包含 root x_j 的直接接線**。
對 t∈{q,r}，令 D_t=t(N_B(x_j))，Q_t 為 root 上所有路徑外 palettes 的聯集。
同列的兩份拒絕證書在旁支的非 root 頂點有相同 lists；這些點沒有 z 邊或
另一接點，故 [rooted palette 唯一性](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
給共同的 Q_t。路徑內點的 residual 為 F_t。

端點需合用兩份證書，不能只拿其中一個 z 色：寫 F_t={a,d}、
E_t=U\(D_t∪Q_t)，兩式 E_t\{a}={d}、E_t\{d}={a} 迫使 E_t={a,d}。
所以所有 j 都有

\[
D_t\cap Q_t=\varnothing,\qquad E_t=U\setminus(D_t\cup Q_t)=F_t. \tag{1}
\]

假設 π∈S₄ 滿足 r(b_i)=π(q(b_i)) 對全部 i∈T_j 成立。對每個旁支非 root
頂點 y，因其全部 boundary 鄰點都在 T_j，r-list 正是 q-list 的 π 像。
將已存在的 q 旁支 palettes 用 π 搬運，會得到符合 r 的全部非 root lists
的 palettes。從葉 block 向 root 歸納，任取非 root block 頂點的 list，
扣掉已決定的後代 palettes，就唯一決定該 block palette；存在性保證不同
選點相容。因此搬運後的 palettes 等於已存在的 r palettes，得 Q_r=π(Q_q)。
T_j 包含 root 接線亦給 D_r=π(D_q)，由 (1) 得

\[
\boxed{\quad r|_{T_j}=\pi\circ q|_{T_j}\ \Longrightarrow\ F_r=\pi(F_q).\quad} \tag{2}
\]

這是對任意有限 rooted block tree 的歸納，不限制旁支大小或主路徑長度。
**π 不必保持 root 完整 list，也不必固定原來的 z 色**：所比較的是各旁支
非 root lists；唯一性不使用 root list。存在性則已分別由兩列的拒絕取得，
並非由 (2) 或 Python 控制創造。

只在 **|F_q|=|F_r|=2** 時套用這份共用路徑／每塊 residual 引理。singleton
情形沒有 (1) 的此種保證，本輪不新增限制。若 T 上沒有任何對齊置換，(2)
是 vacuous，**不排除 T**。即使有一個置換符合，也須核對全部對齊置換。

## 3. record 16 的具名反證

s=0，S0={0,1}、S1={1,2,3,4}，F0(q)={1}、F1(q)={2,3}；p₂ 已由原表接受。
反設 p₁ 拒絕。q、p₁ 在 S0 逐點相同，同一 C0 的完整關係不變，故
F0(p₁)={1}。z 可用色為 {1,2,3}，接合式迫使 {2,3}⊆F1(p₁)，
再由非空 R1 與二接點容量得 **F1(p₁)={2,3}**。

在 q 下，F1={2,3} 的局部穩定子迫使每個 W_j 都見色 0、1；
S1 中 q 色 0 唯一由 b2 提供，所以 b2∈T_j。
若 b1∉T_j，則 T_j⊆{2,3,4}，這三個具名框點上

| 框點 | q | p₁ |
| --- | ---: | ---: |
| b2 | 0 | 0 |
| b3 | 1 | 2 |
| b4 | 2 | 1 |

π=(1 2) 對齊兩列，而 (2) 要求 F1(p₁)=π{2,3}={1,3}，矛盾。
因此每塊實際接 **b1、b2**。有限支援核對為

\[
\{12,123,124,234,1234\}\ \longrightarrow\ \{12,123,124,1234\};
\]

唯一刪掉的是 234；這個支援推理無須先限制 bridge 長度。

任取 P 的一條原 bridge xy，令 J=P∪{zu,zv}。取

\[
A=W_x,\quad A'=W_y,\quad
Z=(V(J)\setminus\{x,y\})\cup\{b0,b3,b4\},\quad X=\{b1\},\quad Y=\{b2\}.
\]

兩個 W 連通且不交。J 刪除相鄰 x,y 的其餘部分經 z 連通，原 spoke zb0
再接框路徑 b0–b4–b3，故 Z 連通；即使 P 只有一條邊，剩餘部分仍含 z。
五組兩兩不交。十條鄰接如下：

| branch-set pair | 原邊 witness |
| --- | --- |
| A–A' | xy |
| A–Z、A'–Z | J 上兩塊向外的 cycle 邊；端點使用原 z 邊 |
| A–X、A–Y、A'–X、A'–Y | 每塊到 b1、b2 的四份實際附件 |
| X–Y、X–Z、Y–Z | b1b2、b1b0、b2b3 |

故同一來源 G 有 K5 minor，與平面性矛盾，p₁ 必延拓。這是
[frame-arc 引理](c5_single_spoke_frame_arc.md#3-三段框弧與任意兩塊的-k5-引理)
的相鄰支援特例，只使用原 spoke，不需要另一分量的外部路徑。
沒有宣稱 record 16 可實現、所有來源共用一個 z 色或完整 Σ 已知。

## 4. 套表規則與分開計數

[Checker](../scripts/c5_single_spoke_cross_row.py) 以原必要表與 frame-arc artifact
為只讀輸入，核對前一層全部輸入 SHA256，保存完整原記錄及上一層 target 證據。
不修改來源 ID 集或既有來源排除；只處理 108 筆中 66 個未知 target。

對每個 target，由原兩份完整 F 候選族重新計算覆蓋 z 可用色的**整組拒絕候選**，
並核對和原 `rejection_options` 逐項一致。對每個候選的每個雙列 pair 分量，
先交集兩列各自容許的 T⊆S，再加入 (2)。若沒有任何 T，該拒絕候選不可能；
若共同必接集合含一對框點，則沿用原 spoke／另一分量原路徑與三框弧給 minor。
原 frame-arc 已排除的候選繼續保留其 witness。**全部候選都被排除才接受 target**。
本輪實際掃描沒有出現空支援族；新增排除皆有 frame-arc minor。

| 階段 | A/A | A/? | ?/A | ?/? | 未決查詢 |
| --- | ---: | ---: | ---: | ---: | ---: |
| frame-arc 輸入 | 58 | 12 | 22 | 16 | 66 |
| 本輪更新後 | 74 | 8 | 10 | 16 | 50 |

新增 p₁ 共 12 個：16、337、432、447、468、477、486、815、816、817、824、826。
新增 p₂ 共 4 個：31、336、449、823。s=0 有 4 個，s=1 有 12 個，s=4 無新增。
全部 16 個各使一筆來源由單列已證成為 A/A。數字包含交換 C0、C1 的具名記錄；
反射側只搬運，不重複計數。

66 個查詢共有 222 組拒絕候選，前層已排除其中 126 組；只合併兩列穩定子
可排除 136 組並新增 record 31、336 的 p₂。再加跨列置換後共排除 168 組，
多出另外 14 個完整 target 延拓。剩下 54 組候選分屬 50 個查詢。
record 493/p₁、827/p₁、1111/p₂、1115/p₁、1515/p₁、1527/p₂ 各消掉 6 組
中的 5 組，仍保留一組；**這六項保持未決**。

每份新 witness 保存原分量、接點、雙列禁色、容許支援、每個跨列刪除的違反置換、
具名框弧及外部路徑落點；未知來源大小使用符號 branch-set 構造，不偽造實際頂點。
核對 ρ=(3,2,1,0,4)、π=(0 1) 的字面 target 色列、禁色、全部支援與框弧搬運，
亦核對交換分量後逐候選判定一致。完整資料見
[JSON](../artifacts/c5_single_spoke_cross_row/observations.json) 與
[套用表](../artifacts/c5_single_spoke_cross_row/support_table.md)。

## 5. 有限控制、重播與下一入口

- 48 個端點／內點 residual 控制，沿用且重播兩份拒絕證書的端點等式。
- 1,944 個 residual 換色代數控制：D、Q 不交的 81 種配置 × 24 色置換。
- 2,304 個跨列支援控制：q 對兩個 p × 六種 F_q × 六種 F_r × 32 個 T，
  每個檢查全部 24 色置換，另以部分單射的所有 residual 像獨立核對。
  包含 record 16 的 16 個支援子集及上述五變四結果。
- 400 個具名 record 16 minor skeletons：奇數長度 1、3、5、7、9 的全部
  25 個 bridge 位置 × 16 種兩側 tether 形狀；固定原 spoke 與框弧
  X={b1}、Y={b2}、D={b0,b3,b4}。逐份核對連通、不交與十條原邊鄰接。
- 12 個負控制：缺 spoke／tether／bridge／cycle edge／框弧邊／框側鄰接、
  集合重疊，以及 vacuous 對齊、全稱量詞、singleton 跳過、部分候選仍未決、
  root list／z 色無須固定。控制範圍與附件所述數字分開記錄。

```bash
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 無 `--check` 時只生成本輪 JSON／套用表；有參數時重算逐 byte 比對。
當輪檢查和未重跑範圍見 [研究紀錄](history/2026-09-28-cross-row.md)。有限 skeletons
不是 degree/list 來源圖或可實現性證書；任意大小由 §1–3 的證書存在性、
block-tree 歸納與原圖 branch sets 承擔。`lake build` 不使其成為 Lean 證明。

下一個具名入口是 **record 17**：s=0，支援 (01,01234)，禁色 ({1},{2,3})，
p₁、p₂ 均未決。反設 p₁ 拒絕，本輪已迫使 C1 每塊碰 b1，並碰 b0、b2 至少
一者；若兩塊都碰 b2，配 spoke 可套任意兩塊 frame-arc 引理矛盾。因 S1 實際
包含 b2，所以恰一塊碰 b2，其餘皆碰 b0。重複的 {b0,b1} 配對無第三個外部落點：
spoke 在 b0，而 C0 只接 01。此窄缺口需保留原 bridge 次序與全部旁支接線，
不能憑共同 b1 任選第二個供應點。p₂ 反設則只迫使每塊碰 b0 及 b1/b3 至少一者。
這些仍是必要限制，未證 record 17 延拓、來源正常形或可實現性。
一般 single-spoke、t=0、更高 degree、多 degree-5、核心存在／分離、共同出口與
`K∞=K≤5` 仍未證。
