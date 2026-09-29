---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t1-endpoints
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-t1-bridge
  requires:
    - c5.adjacent-degree5-no-mixed-t2-endpoints
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
  related:
    - c5.single-sided-exit
---
# 無 mixed t_z=2、t_w=1：record 22 原雙端點與整型分離

後續（2026-09-29）：[四分量支援與雙列](c5_adjacent_degree5_no_mixed_t2_t0_singles.md)
已完成下文交接的 t_z=2、t_w=0、(2,1,1)：原 96 份接成 120 份必要支援，
240／240 查詢全接受並接入出口第九類。本文與 JSON 保留原輪交接資料。

2026-09-29，Git 基準 `f29b899`；保留前層 record 14 的未提交成果。
**record 22／p₂ 必延拓。** source 禁色 2 雖不守恆，兩個原接點的
tightness 仍迫使兩端 q residual 都是 {2,3}，故兩端路徑塊都碰 b2、b3。
全部中間原 bridges 與原 w–z–b0 路徑給 K5 minor，排除唯一失敗候選。

同一原雙端點引理套回 [前層](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md)
的 66 個未決查詢，**新增 66 個延拓，1,120／1,120 全證、0 未決**。
原 560 份全部保留、560 份雙列皆證、新來源排除為 0；此有序型及整圖
root 交換型接入 [條件式出口](c5_single_sided_exit.md) 第九類。

證據為任意大小紙面論證、外部 degree-list 定理與 Python 有限控制。
不需 T4，未新增 Lean theorem；必要支援不是 disk 實現，未證任意來源
完整 Σ、一般單側／共同出口或 `K∞=K≤5`。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源、完整接合與原雙端點

沿用 [原表 §1–3](c5_adjacent_degree5_no_mixed_t2_t1.md#1-同一來源五接點與-source-預算)：
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 是 edge-minimal q=01012 obstruction；相鄰 z、w 完整 degree=5，其餘
內點完整 degree=4。H−{z,w} 無 mixed；z 有兩條原 spokes 和二接點 C_z，
w 有一條原 spoke、二接點 C_w 及單接點 D_w。U={0,1,2,3}，
p₁=01021、p₂=01212。原 C_z、C_w 均 K4-free，source F 均為 singleton。

保持三原分量、五個具名有序接點、三 spokes、zw、全部實際附件、
bridges、旁支、環序與共同色框。完整非空接點關係 T_C(t) 定義 F_C(t)
為 tuples 色集的交集，故精確接合仍為

\[
E_z(t)=U\setminus(t(B_z)\cup F_z(t)),\qquad
E_w(t)=U\setminus(t(B_w)\cup F_w(t)\cup F_D(t)),\qquad
Z_M(t)=(E_z(t)\times E_w(t))\setminus\Delta. \tag{1}
\]

D_w 是原任意大小單接點分量；不把它改成 spoke，也不對它套雙接點引理。
固定 C=C_z 或 C_w，F_C(q)={d}，反設 F_C(t)=A 是 pair。沿用前層
的雙禁色化約，兩原接點間有奇數長原 bridge 路徑 P=(x₀,…,xℓ)，ℓ≥1。
刪 P 全部邊後的 W_j 保留全部旁支與實際 boundary 支援 T_j⊆S_C。

對 s=q,t，D_j^s 為 x_j 的直接 boundary 色，Q_j^s 為路徑外 palettes
聯集，記 L_j^s=U\(D_j^s∪Q_j^s)，尚未扣 root 色。target 給每點 L_j^t=A。
局部 L、整分量 F、root residual E 是不同對象。

拒絕 (q,r=d) 的 degree lists 由
[Dvořák Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 block palettes；本輪核對原文。不要求 target minimality。
兩個原端點各只有一條 incident P bridge，其 q palette 記 {β_j}。
端點 tightness 迫使 d 不在直接附件色或 incident palettes 中，故

\[
L_j^q=\{d,\beta_j\},\qquad \beta_j\ne d,\quad j\in\{0,\ell\}. \tag{2}
\]

這不需要 d 守恆。一般不能設 β₀=βℓ，也不能把 (2) 套到 x₁ 等內點。
ℓ=1 時兩端用同一條原邊；以下仍保留全部容許值，足以給必要條件。

## 2. 全部端點選擇與固定框弧

令 K={a:∀i∈S_C，q_i=a iff t_i=a}。同一 W_j 的
[固定色 palette 歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
給 L_j^q∩K=A∩K。記 𝒯(s,S,R) 為逐點固定 s(T) 的所有四色置換
都保持 residual R 的支援 T⊆S；原 rooted palettes 的唯一性給此必要條件。
於是兩端實際支援均屬於

\[
\mathcal B=\{\beta\ne d:\{d,\beta\}\cap K=A\cap K\},\qquad
\mathcal E=\bigcup_{\beta\in\mathcal B}
  \bigl(\mathcal T(q,S_C,\{d,\beta\})\cap\mathcal T(t,S_C,A)\bigr). \tag{3}
\]

保留全部 β 的聯集，不假設兩端可獨立實現。若 𝒠 非空，先固定同一份
三個連通框弧 B=X⊔Y⊔D_B，以及避開 C、B 內部的原 r–b_h 路徑 L，
h∈D_B；若所有 T∈𝒠 都碰 X、Y，則兩端 W₀、Wℓ 都碰 X、Y。
原路徑 L 的四類來源沿用 [前層 §2](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md#2-四種原外部路徑與固定三框弧)，
包含經 D_w 的實際路徑；不重用兩側 t=2 的整份四-spoke 幾何表。

在原圖取五個 branch sets

\[
V_0=\bigcup_{j=0}^{\ell-1}W_j,\quad V_1=W_\ell,\quad
Z=V(L)\cup D_B,\quad X,\quad Y. \tag{4}
\]

V₀ 由所有中間原 bridges 連通，最後一條 bridge 給 V₀–V₁；原兩條
contact 給 V₀–Z、V₁–Z。兩端的四份實際附件給 V₀／V₁ 各接 X、Y，
三個 C5 切口給 X、Y、Z 彼此相鄰。原分量身份及固定分割保證五組不交，
因此得到 K5 minor。這是既有 [原雙端點引理](c5_adjacent_degree5_no_mixed_t2_endpoints.md#3-保留完整中間路徑的-k5)
在三分量來源的局部搬運；ℓ=1 同樣成立。空族另作端點不存在處理。

## 3. Record 22／p₂ 的具名反證

原子表 ID=39、retained-join ID=3189、sides=(137,102)，共同 c=3：

\[
B_z=04,\quad B_w=1,\quad(S_z,S_w,S_D)=(01,234,12),\qquad
(F_z,F_w,F_D)(q)=(\{1\},\{2\},\{0\}).
\]

p₂ 下 F_z={1}、F_D={2} 精確；唯一失敗完整候選為 F_w={0,3}，
使 E_z={3}、E_w=∅。其餘四組候選均有原 root 色對 (3,0)。

對 C=C_w，d=2、A={0,3}、K={1,3}。式 (3) 迫使 β₀=βℓ=3，
所以兩端 q residual 都是 {2,3}。q 在 S_w=234 的字面色為 012；
穩定子保持 {2,3} 必見補集色 0、1，即同時碰 b2、b3。與 target
族 {23,34,234} 相交後恰得 𝒠={23,234}。

取 X={b1,b2}、Y={b3,b4}、D_B={b0}，L 為原 **w–z–b0**。
式 (4) 的 Z={w,z,b0} 由原 zw、zb0 連通，十對原鄰接給 K5。
因此 F_w(p₂)≠{0,3}，完整式 (1) 保證 p₂ 延拓；p₁ 沿用前層延拓。

沒有推論 x₁ 的 q residual 也是 {2,3}：邊色序列 3,0,3 的兩端 residual
為 {2,3}，內點為 {0,3}，仍符合固定 K 的局部方程。這是負控制，
不是來源可實現性主張。本證明不需要重新構造第二個 source 禁色。

## 4. 完整套表與出口

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py) 綁定前層與
原表 SHA256，保留原 136 份正常形、560 個 IDs、3,150 份幾何、全部
placements、五接點 rotations、完整 q schemas 與單接點 relation。
重新計算 1,120 個查詢的 3,148 組完整 joins，核對 146 組原失敗候選：
繼承 80 組反證，新增 66 組原雙端點 K5。每個 target 的全部候選都有
原 root 色對或已被反證，才標為接受；未作來源刪除。

| 層 | 已證 target | 雙列皆證 | 未決 | 新來源排除 |
| --- | ---: | ---: | ---: | ---: |
| 原外部路徑／首橋 | 1,054 | 494 | 66 | 0 |
| 原雙端點／完整 bridge 路徑 | 1,120 | 560 | 0 | 0 |

原表的任意大小必要覆蓋配合上述套表，證成 §1 圖類全部接受 p₁、p₂。
交換整張來源的 z、w 同時交換 spokes 與原分量歸屬，保持 boundary、
字面色框、全部接點及 Z 的非對角條件，故也涵蓋反向有序型。

[出口定理](c5_single_sided_exit.md) 額外假設來源 Σ(G)=Ω\{p,q}；
minimal q-core M 繼承其餘八列，本結果給對齊後的 p，而 q 仍拒絕，
才得 Σ(M)=Ω\{q}。第九類擴為無 mixed、兩側 t=(2,2)，或整圖交換後
t_z=2,(2)、t_w=1,(2,1)。不以兩列接受單獨推出完整 Σ。

下一窄入口是 **t_z=2,(2)，t_w=0,(2,1,1)**。只讀原 3,548 份同色
join 得 96 份有序資料；首項 retained-join ID=3048、sides=(133,64)，
B_z=01、F_z={2}，w 無 spoke、F=({0},{1},{2})，c=3。JSON 綁定該
96 份 IDs 與原 hash，尚未建立此型 actual-support／rotation 覆蓋。
須保留四原分量、六接點與兩條 spokes；其他分拆及 O=1 型保留。

## 5. 有限控制與重播

- 重算既有 1,536 份端點色域／穩定子控制及固定色 palette 代數。
- 732 份原圖 K5 skeletons：每個新增反證的四類可用外部路徑，加上
  record 22 的長度 1／3／5／9、16 種雙端點 tether 形狀與外部分量
  內部鏈長 1／3；每份核對十鄰接、字面反射及 root 交換。
- 146 組候選字面反射與完整 root 交換；3,148 組完整 root 色對交換。
- 18 個負控制涵蓋 singleton／D_w guard、非守恆 d、端點不代表下一點、
  固定框弧、空族，以及缺少原 bridge、contact、zw、spoke、附件、
  D_w 內部路徑和 branch sets 重疊。D_w 刪邊負控制用 record 14，
  避免 record 22 的原 wb1 成為 Z 的替代連接。

這些 skeletons 不滿足來源的全部 degree/list 前提，並非 disk 實現；
負控制只否定指定 witness。任意大小覆蓋由紙面論證及外部定理承擔。
完整資料見 [JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints/observations.json)
與 [逐筆表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints/support_table.md)。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t1-endpoints.md)。
`--check` 重算並逐 byte 比對；無參數只生成本層。`lake build` 不形式化
本輪紙面證明、外部定理或 disk 拓撲。
