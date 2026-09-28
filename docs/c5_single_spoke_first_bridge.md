---
docgraph:
  id: c5.single-spoke-first-bridge
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-two-arc
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
---
# Single-spoke (2,2)：singleton-source 首橋相容性與 record 87 延拓

2026-09-28，審核基準 `b770d21`。本輪從使用者訊息獨立核對首橋推導，
再建立 repo checker 並套剩餘表。所附 `/mnt/data/math_record87_first_bridge_review/`
與 ZIP 在本環境不存在；沒有重播附件。下列控制均在 repo 重新生成與核對。
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 87 的 p₂=01212 必延拓。** target 雙禁色取得原 bridge 路徑，
source 的 singleton 拒絕證書在同一首橋只有一份 palette；其兩端因此共用
局部 residual `{1,β}`，β=0、2 分別迫使兩塊同接 b2、b3 或 b3、b4，給 K5。
沒有把局部 residual 當作整分量的 singleton 禁色，也沒有改動 `joint_supports`。

本輪套表新增 **16 個指定列延拓**：10 個由共用 β 的 K5，6 個由同一引理的
端點固定色矛盾。**來源排除仍為 278 筆，保留 102 筆／51 型**；雙列已證
由 84 增為 **100 筆**，未決查詢由 18 降為 **2 個**，即 record 90、282 的 p₂。
沒有來源移出或新的來源排除。任意大小結論是紙面證明＋外部 degree-list
定理；Python 是有限代數／具名 minor 控制與套表，**未新增 Lean theorem**。

## 1. 完整前提與三份既存拒絕證書

沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) §1–3：G 有限簡單，
B=(b0,…,b4) 為 induced-C5 disk 外框，有效 H 連通。G 是 edge-minimal
q=01012 obstruction，唯一完整 degree-5 點 z 僅有 spoke zb_s，其餘內點
完整 degree=4；H−z 恰有 C0、C1，各保留兩個不同的原有序接點 (u_k,v_k)。
S_k 是整個 C_k 的全部實際 boundary 支援。套保留表時沿用原 T4 篩選。
U={0,1,2,3}，p₁=01021，p₂=01212。

對任意 proper row t，R_k(t) 是同一完整分量著色給出的有序接點 tuples，
不能替換成兩個獨立 marginals。忽略 z 時接點有嚴格 list slack，因此
R_k(t) 非空，且

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\quad |F_k(t)|\le2,
\qquad Z_G(t)=(U\setminus\{t_s\})\setminus(F_0(t)\cup F_1(t)).
\]

取同一 C=C_k，假設 F_C(q)={c}，反設 target r 有 F_C(r)={a,d}。
拒絕 (q,z=c)、(r,z=a)、(r,z=d) 各給 C 上不可著色的 degree lists。
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 blockwise-uniform palettes。本輪重讀原文：條件是連通、
degree assignment 及不可著色，**不需 target minimality**。原 K4-free
化約保證 blocks 僅為 bridges／odd cycles。

**只由 target pair** 取得奇數長原 bridge 路徑 P=(x0=u,…,xℓ=v)，ℓ≥1。
刪去全部 P 邊後的 W_j 是含 x_j 與其全部旁支的原連通分量，彼此不交。
T_j⊆S_C 包含 W_j 全部實際 boundary 接線，包括 root 的直接附件。
每條 P 邊已是原圖 bridge，因此也是 q 證書的 singleton-palette block；
不需從 q 再產生路徑，不逐列重選圖或接點。

## 2. 固定色守恆與端點的額外一色

對 t=q,r，令 D_j^t=t(N_B(x_j))，Q_j^t 為 root 上所有路徑外 palettes
的聯集，並定義尚未扣除 z 色的局部 residual

\[
E_j^t=U\setminus(D_j^t\cup Q_j^t).
\]

target 的兩份拒絕證書在旁支非 root lists 相同，故 Q_j^r 相同；
[既有 pair residual 引理](c5_single_spoke_cross_row.md#2-跨列-residual-換色引理)
給每個 j 的 E_j^r={a,d}，包含兩端點。

令 K 為在 S_C 上逐點保存 membership 的顏色集合：

\[
K=\{h\in U:\ \forall i\in S_C,\ q_i=h\iff r_i=h\}.
\]

旁支非 root 不含其他接點，沒有 z 邊。對 h∈K，它們的 q、r lists 對 h
逐點相同。[Rooted-palette 固定色守恆](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
由葉向 root 歸納：非 root 頂點的 list 是 incident palettes 的不交聯集，
扣除已決定的後代 palettes 後，父 block 對 h 的 membership 也相同。
存在性來自三份既存拒絕證書；歸納不需兩列均為 pair、不需 root list。
直接附件也保存 h，因此

\[
E_j^q\cap K=E_j^r\cap K=\{a,d\}\cap K. \tag{1}
\]

另在接點 x0，完整 degree=4 給 d_C(x0)+|N_B(x0)|+1=4。
q,z=c 的 tightness 給

\[
|D_0^q\cup\{c\}|=|N_B(x0)|+1,
\]

所以 **c 不在 D_0^q**。旁支 palettes 位於扣掉 c 的 root list 中，
故 c 也不在 Q_0^q，亦即 c∈E_0^q。令首橋 x0x1 在 q 證書的 palette
為 {β}，端點僅一個路徑 block，故

\[
E_0^q\setminus\{c\}=\{\beta\},\qquad
\boxed{E_0^q=\{c,\beta\},\quad\beta\ne c.} \tag{2}
\]

只靠第一條集合等式不能補回 c；上述端點 tightness 明確提供這一步。

**端點推論。** 若 c∈K，但 c∉{a,d}，(1)、(2) 直接矛盾。
這正是本輪六個查詢使用的條件；不需 minor。

## 3. 首橋的共用 β 與局部穩定子

以下假設 c∈K∩{a,d}。(1) 給 c∈E_1^q。同一首橋的同一 palette {β}
也屬於 E_1^q。若 ℓ=1，x1 是另一接點，由相同端點等式得 E_1^q={c,β}。
若 ℓ≥3，x1 是路徑內點，E_1^q 是兩個相異 singleton bridge palettes
的聯集，大小為二；既含 c、β，仍得

\[
\boxed{E_0^q=E_1^q=\{c,\beta\}.} \tag{3}
\]

因此可用的 β 必在

\[
\mathcal B=\{\beta\in U\setminus\{c\}:\
\{c,\beta\}\cap K=\{a,d\}\cap K\}. \tag{4}
\]

這只約束首橋；不宣稱其他奇數位置 bridges 共用同一 β。
若 c∉K，本輪通用 checker 跳過此引理，不推論 (3)。

對 j=0,1，若 π 逐色固定 q(T_j)，它保持所有旁支非 root lists。
rooted-palette 唯一性給 πQ_j^q=Q_j^q，root 直接附件給 πD_j^q=D_j^q，
故 πE_j^q=E_j^q。此處 **π 不需固定 z 色或 root 完整 list**。
target 的既有穩定子同時給 πF_C(r)=F_C(r)（對固定 r(T_j) 的 π）。

對每個共用 β，取所有同時符合這兩個穩定子條件的 T⊆S_C，記為 𝒯_β。
同一首橋的 T0、T1 都屬於**同一族 𝒯_β**。這裡 source 受穩定子保持的
是局部 {c,β}，不是 F_C(q)={c}；舊 `joint_supports` 的 pair guard 完全保留。

## 4. record 87 的實際附件與原圖 K5

s=0，S0=234、S1=012，F0(q)={1}、F1(q)={2,3}。p₁ 已證；沿用前層
完整候選消去，反設 p₂ 拒絕只剩 F0(p₂)={1,2}、F1(p₂)={3}。
取 C=C0，c=1；q|234=(0,1,2)，p₂|234=(2,1,2)，故 K={1,3}。
(1) 給所有 E_j^q 含 1、不含 3，(4) 給 β∈{0,2}。

q 不使用色 3。若 c'∈E_j^q 卻不在 q(T_j)，交換 (c' 3) 固定局部
boundary 色、但移動 E_j^q，矛盾。q 在 S0 上的 0、1、2 分別只能
由 b2、b3、b4 提供。因此首橋兩端有

| 共用 β | 兩端共同局部 residual | T0、T1 各自的容許支援 | 必接的框點對 |
| ---: | --- | --- | --- |
| 0 | {0,1} | 23、234 | b2、b3 |
| 2 | {1,2} | 34、234 | b3、b4 |

一端僅接 23、另一端僅接 34，不能支承同一 β。令必接對為 {b_a,b_b}，
J=P∪{zu,zv}，取

\[
A=W_0,\quad A'=W_1,\quad X=\{b_a\},\quad Y=\{b_b\},\qquad
Z=(V(J)\setminus\{x_0,x_1\})\cup(B\setminus\{b_a,b_b\}).
\]

W0、W1 連通不交。J 刪去相鄰兩點的剩餘部分含 z 且連通，ℓ=1 時為 {z}。
兩種補弧分別為 b4–b0–b1、b0–b1–b2，都由原 spoke zb0 接到 z，故 Z
連通。原 W 分割與 C、B、z 身份保證五組兩兩不交。

十條鄰接分別由首橋 A–A'、兩條朝外 cycle 邊 A–Z／A'–Z、四份實際
boundary 附件 A／A'–X／Y，以及三條框側鄰接 X–Y／X–Z／Y–Z 提供。
這是同一原圖的 K5 minor，與平面性矛盾，故 p₂ 延拓。
論證沒有要求新拓撲構造，也不證 record 87 可實現或完整 Σ。

## 5. 套剩餘表與分開計數

[新 checker](../scripts/c5_single_spoke_first_bridge.py) 只讀原必要表與
two-arc artifact，核對前層輸入 SHA256，保留全部原始記錄、完整 relation
schema IDs、有序接點、slit lifts、contact words、反射與舊 target 證據。
不更動來源 ID 集或來源排除。18 個未決查詢的**原完整拒絕候選**共 146 組，
前層已排除 128 組，每個查詢恰剩一組；本輪逐組重算並核對繼承證據。

新層先用 §2 端點矛盾；否則分情況遍歷 (4) 中全部 β。對每個 β，若
𝒯_β 非空，取其共同必接框點對，沿用 [frame-arc 原圖 K5](c5_single_spoke_frame_arc.md#3-三段框弧與任意兩塊的-k5-引理)。
外部路徑只取原 spoke 或另一原分量的實際 z–框點路徑，保存其落點與原分量。
空族或空 β 域另為不可能證據，不能用 vacuous 全稱製造 minor。
**全部 β 排除才消去完整拒絕候選；全部完整候選消去才接受 target。**

| 新證明方式 | 指定查詢 | 數目 |
| --- | --- | ---: |
| 共用 β，逐值 K5 | 87/p₂、281/p₂、1101/p₂、1111/p₂、1524/p₂、1527/p₂；1105/p₁、1115/p₁、1512/p₁、1515/p₁ | 10 |
| 端點固定色矛盾 | 490/p₁、493/p₁、511/p₁、791/p₁、793/p₁、827/p₁ | 6 |

第二列的 singleton 色為 c=0，在 source／p₁ 的支援上逐點守恆，但唯一
剩餘 target pair 為 {2,3}，不含 0，直接違反 §2。

| 階段 | 來源排除累計 | 保留來源／交換型 | A/A | A/? | ?/A | 未決查詢 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| two-arc 輸入 | 278 | 102／51 | 84 | 8 | 10 | 18 |
| 首橋更新後 | 278 | 102／51 | 100 | 2 | 0 | 2 |

新增 16 組候選反證、剩 2 組；無來源移出，沒有把來源排除計成延拓。
checker 逐候選核對交換分量後結果一致，並核對 ρ=(3,2,1,0,4)、π=(0 1)
的**字面 target 色列**、固定色、β、支援、具名框弧與外部落點搬運。
反射側只搬運，不重複計數。資料見 [JSON](../artifacts/c5_single_spoke_first_bridge/observations.json)
及 [套用表](../artifacts/c5_single_spoke_first_bridge/support_table.md)。

## 6. 有限控制、重播與下一入口

- 8 個 record 87 支援子集，以全部 24 色置換獨立核對；8 個共用 β 的
  有序雙塊支援配對，禁止把兩端的 β 分開選。
- 8,748 個固定色歸納局部控制：所有 list／後代 palette 聯集的可能
  membership；36 個 record 87 的 D／Q residual 守恆控制。
- 48 個端點 tightness／residual 控制；24 個首橋接點／內點二色控制。
- 576 個 record 87 具名 minor：兩種必接對、奇數長度 1 至 17、16 種
  兩端 tether 形狀與反射，均取第一條原 bridge。
- 1,344 個套表 minor 控制：覆蓋實際用到的每種框點對／落點／原 spoke
  或外部分量模式，長度 1、3、7 與四種 tether 形狀；逐份保存原邊、
  五組、實際附件路徑與十對鄰接。
- 16 個負控制：缺原邊／附件、補弧斷裂、集合重疊、兩端獨立 β、端點
  忘記 tightness、將局部 E 當作 F、跨全部奇數邊錯用同一 β、移除舊
  singleton guard、只消部分候選／β、未守恆 c 或 target singleton。

```bash
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
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

新 checker 無參數時只生成新層 JSON／表，有 `--check` 時重算逐 byte 比對。
實際驗證與未重跑範圍見 [研究紀錄](history/2026-09-28-first-bridge.md)。
有限控制不建立拒絕證書存在性，不替代任意大小 block-tree 歸納；minor
skeletons 不是 degree/list 來源圖或可實現性證書。`lake build` 不形式化本證明。

下一個窄入口是 **record 90/p₂**（282 只是交換分量）：s=0、S0=0234、
S1=012，q 禁色 ({1},{2,3})；唯一剩餘拒絕候選仍是 ({1,2},{3})。
β=2 已排除，**β=0 仍未決**，首兩塊容許支援為

\[
\{23,023,034,234,0234\},
\]

等價於每塊含 b3，且含 b2 或同時含 b0、b4。共同必接只有 b3；q 色 0
現在可由 b0 或 b2 提供，不能再唯一指派 b2。下一步需保留首橋同一 β、
原接點、全部旁支及實際附件，處理這個供應點選言；本輪不宣稱它們可
獨立選擇、可同時嵌入或構成反例。
一般 (2,2) 分離、其他 t=1 分拆、t=0、更高 degree、多 degree-5、核心
存在／分離、共同出口與 `K∞=K≤5` 仍未證。
