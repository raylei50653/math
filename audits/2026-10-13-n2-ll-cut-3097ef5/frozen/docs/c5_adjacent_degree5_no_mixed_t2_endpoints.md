---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-endpoints
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-bridge
  requires:
    - c5.single-spoke-first-bridge
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
---
# 無 mixed 兩側 t=2：原雙端點與 60 個新增延拓

三輪成果的整合提交與驗證見 [發布紀錄](history/2026-09-29-adjacent-no-mixed-t2-publish.md)。

後續（2026-09-29）：[整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)
已關閉 record 54／p₁ 及其餘三項；新增 4 個延拓、0 筆來源排除，原 322
份全保留、644／644 查詢全證，接入出口第九類。下文與原 artifacts 保留
本輪 640／644 及 record 54 停止點；現行入口見 HANDOFF。

2026-09-29。接續未提交的 [原 bridge／固定框弧成果](c5_adjacent_degree5_no_mixed_t2_bridge.md)，
Git 基準仍為 `51ef494`；研究優先序見 [HANDOFF](HANDOFF.md)。

**record 5／p₂ 必延拓。** q 禁色不守恆時，首橋的第二個頂點未必與第一點
有相同 residual；但兩個**原接點端點**仍各受 tightness 約束。兩端的實際
支援及完整中間 bridge 路徑給來源 K5 minor。

同一引理套回原 64 個未決查詢，新增 **60 個延拓、0 筆來源排除**。
322 份原資料全部保留，現為 **640／644 個 target 已證、318 份雙列皆證**；
只剩 54／p₁、68／p₂、173／p₂、256／p₁ 四個查詢。
無 mixed 兩側 t=2 尚未整型接回出口。

任意大小結論為紙面 palette 歸納與原圖 branch sets，依賴外部 degree-list
定理；Python 核對有限代數與套表。不需 T4，未新增 Lean theorem，未證
必要表的 disk 實現、完整 Σ、一般單側／共同出口或 `K∞=K≤5`。

## 1. 同一來源及雙端點 residual

沿用 [支援表 §1](c5_adjacent_degree5_no_mixed_t2.md#1-同一來源與原-88-份資料)
的全部前提：有限簡單 G，B=(b0,…,b4) 為 induced disk 外框，有效 H 非空
連通，G 是 edge-minimal q=01012 obstruction。相鄰 roots z、w 完整
degree=5，其餘內點完整 degree=4；H−{z,w} 無 mixed，每側有兩條原
spokes 與唯一二接點 unary C_r。U={0,1,2,3}，p₁=01021、p₂=01212。

完整原關係 T_r(t) 的共同禁色為 F_r(t)，root 可用色及接合為

\[
E_r(t)=U\setminus(t(B_r)\cup F_r(t)),\qquad
Z_G(t)=(E_z(t)\times E_w(t))\setminus\Delta.
\]

固定同一 C=C_r，F_C(q)={d}；反設某 target t 的 F_C(t)=D 是 pair。
沿用前層雙禁色化約，兩個原接點間是奇數長原 bridge 路徑
P=(x₀,…,xℓ)，ℓ≥1。刪全部 P 邊所得 W_j 保留 x_j、全部旁支及實際
boundary 附件 T_j⊆S_C。原 zw、四 spokes、另一原分量、具名接點及
完整 schemas／rotations 均保留；不更換來源或只取 endpoint marginals。

對 s=q,t，令 D_j^s 是 x_j 的直接 boundary 色，Q_j^s 是路徑外 palettes
聯集，L_j^s=U\(D_j^s∪Q_j^s)，尚未扣 root 色。這個局部 L 不等於整個
分量的 F 或 root 可用色 E。target 的兩份拒絕 palettes 給每點 L_j^t=D。

拒絕 (q,r=d) 與兩份 target lists 都是同一 C 上的 degree assignments。
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給逐點 tightness 與 blockwise-uniform palettes；本輪核對第 5–6 頁。
不要求 target minimality；外部定理並非 Python 或本專案 Lean 所證。

在**每個端點** j∈{0,ℓ}，q tightness 使 d 不在直接附件色中，也不在
incident palettes 中。因此 d∈L_j^q。端點僅有一條 incident P bridge，
令其 q palette 為 {β_j}；扣掉 d 後的 residual 正是 {β_j}，故

\[
L_j^q=\{d,\beta_j\},\qquad \beta_j\ne d. \tag{1}
\]

這一步不要求 d 在 q→t 守恆。β₀、βℓ 分別來自兩條原端邊；ℓ=1 時是
同一條，但一般不能先設兩者相等，也不能把 (1) 套在路徑內點。

## 2. 兩端共用容許族，保留端邊色的所有選擇

令 K={a:∀i∈S_C, q_i=a ⇔ t_i=a}。既有
[固定色歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
只使用同一旁支非 root 的 lists，得 L_j^q∩K=L_j^t∩K。於是每個端點的
β_j 都屬於

\[
\mathcal B=\{\beta\ne d:\{d,\beta\}\cap K=D\cap K\}. \tag{2}
\]

對任一 residual A，記 𝒯(s,S_C,A) 為所有 T⊆S_C，使每個逐點固定 s(T)
的四色置換都保持 A。rooted-palette 唯一性使直接附件與旁支 residual
受此穩定子保持。因此兩個實際端點支援都在同一必要族

\[
\mathcal E=\bigcup_{\beta\in\mathcal B}
\bigl(\mathcal T(q,S_C,\{d,\beta\})\cap\mathcal T(t,S_C,D)\bigr). \tag{3}
\]

這裡明確保留全部 β，容許兩端選不同 β；未宣稱它們可獨立實現。
若 𝒠 空，原端點即無可能支援。若非空，先固定同一份三框弧與原外部
路徑，再檢驗**全部** T∈𝒠 都碰兩份指定框弧；不逐 T 重選分割。

## 3. 保留完整中間路徑的 K5

固定 B=X⊔Y⊔D_B，三份非空且沿原 C5 連通。原外部路徑 L 從 r 到
b_h∈D_B，內部避開 C、B；取前層的原 spoke、r–s–b_h，或經另一原
unary 的實際路徑。特別保留原 zw 與另一分量身份。

若兩端 W₀、Wℓ 均實際碰 X、Y，取五個 branch sets

\[
A=\bigcup_{j=0}^{\ell-1}W_j,\quad A'=W_\ell,\quad
Z=V(L)\cup D_B,\quad X,\quad Y. \tag{4}
\]

A 由全部中間原 bridges 連通；A' 連通；Z 由 L 在 r 與 D_B 的落點接合。
原 W 分割、原分量身份及框弧分割保證五組兩兩不交。十份鄰接為：

| 兩組 | 原邊／附件 |
| --- | --- |
| A–A' | 最後一條原 bridge x_(ℓ−1)xℓ |
| A–Z、A'–Z | 兩條原 contact rx₀、rxℓ |
| A／A'–X／Y | 兩端路徑塊各自的實際附件，共四份 |
| X–Y、Y–Z、Z–X | 三個原 C5 框弧切口 |

所以得到來源 G 的 K5 minor。這是
[任意兩塊框弧引理](c5_single_spoke_frame_arc.md#3-三段框弧與任意兩塊的-k5-引理)
在原兩端、容許不同框點供應同一弧的特例。中間 W 併入 minor branch set
不改寫來源染色關係；ℓ=1 時 A=W₀，仍適用。

## 4. record 5／p₂ 的具名反證

原 frontier 28、sides=(137,141)：
B_z=04、S_z=01、F_z(q)={1}；B_w=14、S_w=1234、F_w(q)={0}。
p₂ 下唯一失敗完整候選為 (F_z,F_w)=({1},{0,3})，使 E_w=∅。

取 C=C_w、d=0、D={0,3}；K={1,3}。雖然 0 不守恆，(1) 仍適用於
兩端，而 (2) 迫使 β₀=βℓ=3。因此兩端 q residual 均為 {0,3}。
q 的色 3 不出現於 boundary；穩定子要求兩端都見補集色 1、2。
在 S_w 中，q 色 2 只由 b4 供應，色 1 由 b1／b3 供應。

兩端的容許族恰為

\[
\mathcal E=\{14,34,124,134,234,1234\}. \tag{5}
\]

取 X={b1,b2,b3}、Y={b4}、D_B={b0}，L 為原 **w–z–b0**。
所有 (5) 都碰 X、Y，(4) 給 K5。b1、b3 的供應點可在兩端不同，仍用
同一固定框弧。因此失敗候選不存在，p₂ 必延拓；p₁ 的前層延拓保留。

沒有推論 x₁ 的 q residual 也是 {0,3}：局部橋色序列 3,2,3 與
端點 {0,3}、內點 {2,3} 的代數方程相容。這只是防止誤用首橋的負控制，
不是聲稱存在滿足全部來源前提的圖。

## 5. 完整套表與剩餘四項

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py) 只讀原表及前層
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/observations.json)，
核對來源 SHA256，保留原 322 個 IDs、88 份 frontier／side 記錄、完整
q schemas、全部 placements、四個具名 contact rotations 及前層逐項證據。
重算 644 個查詢的全部 2,892 組完整 joins，逐項重算原 160 組失敗候選
的前層證據；前層已排除 96 組，本層再排除 60 組，四組仍保留。

| 階段 | 已證 target | 雙列皆證 | 未決查詢 | 新增來源排除 |
| --- | ---: | ---: | ---: | ---: |
| 原 bridge／首橋 | 580 | 258 | 64 | 0 |
| 原雙端點／完整中間路徑 | 640 | 318 | 4 | 0 |

A/A、A/?、?/A、?/? 為 **318、2、2、0**。新關閉的 60 組均為 d∉K、
但端點 β 域為 singleton 的情形；不以 q 的 singleton F 充作局部 residual。
每一完整候選都有原 root-pair 見證或反證後，才記 target 延拓。

| 原 record | 未決列 | pair 分量 | 尚未排除的首橋 β |
| ---: | --- | --- | ---: |
| 54 | p₁ | C_z | 2 |
| 68 | p₂ | C_w | 2 |
| 173 | p₂ | C_z | 2 |
| 256 | p₁ | C_w | 2 |

54／256、68／173 是原 root 交換，兩組又由 q-preserving 反射搬運；
checker 使用字面 target 列，不以正規化等色分割取代它。

**下一窄入口：record 54／p₁。** 原 sides=(146,146)，B_z=B_w=24，
S_z=0124、S_w=234，F_z(q)=F_w(q)={3}、E_z(q)=E_w(q)={1}。
p₁ 唯一失敗候選為 ({2,3},{3})，給 (E_z,E_w)=(∅,{2})。
C_z 的 d=3∈K={0,3}；首橋 β=1 已由前層原 C_w 到 b3 路徑排除，
β=2 剩餘。此時兩首橋塊的局部 residual 同為 {2,3}，容許支援為

\[
01,12,012,014,124,0124.
\]

每塊必接 b1，並接 b0／b2 至少一個；現有統一三弧不足。下一步保留
原 zb2、zb4、zw、C_w 的全部 234 支援、首橋同一 β 及完整關係，研究
兩個 q 色 0 供應點的選言與原接線次序。不宣稱上述支援可自由獨立實現。

## 6. 有限控制與重播

[新 JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/observations.json)
與 [完整表](../artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/support_table.md)
另保存：1,536 個 endpoint β 域及穩定子控制；重算既有 8,748 個固定色
歸納步、48 個 tight endpoint、24 個首橋控制；572 份 K5 skeletons 及
反射，含兩 roots／四 spokes、長度 1／3／5／9、16 種雙端 tether 形狀、
兩端不同實際供應點及兩種經 zw 的外部路徑。各驗五組連通不交與十對鄰接。
另有 322 次 root 交換、160 次字面 target 反射、15 個負控制。

負控制包括不守恆 d 不得推出下一點 residual、不同端邊不必同 β、
tightness 不可省略、singleton guard、全部 β 的量詞，以及缺中間 bridge、
末 bridge、contact、zw、spoke、附件、框弧連通或 branch-set 不交性。
刪邊只使指定 witness 失效；有限 skeletons 不要求整份 degree/list 條件，
不是來源實現證書。任意長度及任意旁支由 §1–3 的紙面論證承擔。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-endpoints.md)。
`--check` 重算並逐 byte 比對；無參數只生成本層 artifacts。
`lake build` 不將紙面拓撲與外部 degree-list 定理形式化。
