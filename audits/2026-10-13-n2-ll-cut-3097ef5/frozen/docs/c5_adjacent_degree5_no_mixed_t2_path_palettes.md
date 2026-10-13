---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-path-palettes
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-endpoints
  requires:
    - c5.adjacent-degree5-no-mixed-t2-bridge
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
---
# 無 mixed 兩側 t=2：整條原 bridge 路徑迫使第二禁色

三輪成果的整合提交與驗證見 [發布紀錄](history/2026-09-29-adjacent-no-mixed-t2-publish.md)。

2026-09-29。接續 [原雙端點層](c5_adjacent_degree5_no_mixed_t2_endpoints.md)
的 record 54／p₁；Git 基準 `51ef494`，保留前兩輪未提交成果。
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 54／p₁ 必延拓。** 首橋 β=2 的支援選言不必逐項強化成 K5：
把既有 β=1 的反證套到每條奇數位置原 bridge，便迫使整條路徑的
q palettes 交替為 2、3。只交換這些原 bridge 的 palettes，保持所有
旁支，得到同一 C_z 的第二個 q 禁色 2，與 F_z(q)={3} 矛盾。

同一引理也關閉 68／p₂、173／p₂、256／p₁。**新增 4 個延拓，原
322 份全保留，644／644 個查詢全證、322 份雙列皆證、0 個未決。**
新增來源排除為 0；無 mixed 兩側 t=2,(2) 的指定雙列分離完成，接入
[條件式出口](c5_single_sided_exit.md) 第九類。不需 T4。

證據為任意大小紙面歸納、外部 degree-list 定理及 Python 有限控制。
未新增 Lean theorem，未證必要表 disk 實現、任意來源完整 Σ、一般
單側／共同出口或 `K∞=K≤5`。

## 1. 前提與同一原路徑

完整沿用 [必要表 §1–3](c5_adjacent_degree5_no_mixed_t2.md#1-同一來源與原-88-份資料)：
G 有限簡單，B=(b0,…,b4) 為 induced disk 外框；有效 H 非空連通。
G 是 edge-minimal q=01012 obstruction，z、w 相鄰且完整 degree=5，
其餘內點完整 degree=4。H−{z,w} 無 mixed；每側有兩條原 spokes
與唯一二接點 unary C_r。保留原 zw、四 spokes、兩原分量、四個
具名有序接點、全部附件、bridges、旁支、placements 與 rotations。

U={0,1,2,3}，p₁=01021、p₂=01212。完整接點關係 T_r(t) 非空，
F_r(t) 是其 tuples 色集的交集；精確接合為

\[
 E_r(t)=U\setminus(t(B_r)\cup F_r(t)),\qquad
 Z_G(t)=(E_z(t)\times E_w(t))\setminus\Delta.
\]

固定 C=C_r，F_C(q)={d}。反設 target t 的 F_C(t)=D 是 pair。
既有雙禁色引理給兩原接點間的奇數長原 bridge 路徑
P=(x₀,…,xℓ)，ℓ≥1。刪全部 P 邊所得 W_j 保留 x_j、全部旁支與
全部實際 boundary 支援 T_j⊆S_C，包括 x_j 的直接附件。

在 q 與 t 的既存拒絕證書中，D_j^s 為 x_j 的直接 boundary 色，
Q_j^s 為路徑外 incident palettes 的聯集，記尚未扣 root 色的
局部 residual 為 L_j^s=U\(D_j^s∪Q_j^s)。target 給 L_j^t=D。
這個 L 與整分量 F、root 可用色 E 分開。

拒絕證書的存在、tightness 及下文重建後不可著色，依賴
[Dvořák 的 Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本輪核對定理的兩個方向：連通圖上的 degree assignment 不可著色，
等價於 Gallai tree 上的 blockwise-uniform assignment。相交 blocks
的 palettes 必不交，頂點 list 必恰為其 incident palettes 的聯集。
不要求 target minimality；外部定理不是本專案 Python／Lean 所證。

## 2. 每條奇數原 bridge 共用一個 β

令 K={a:∀i∈S_C, q_i=a ⇔ t_i=a}。假設 d∈K∩D；這正是本輪
四個未決候選的情形。既有 [固定色歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
在每個原 W_j 給出 L_j^q∩K=D∩K，故 d∈L_j^q。

令 q 拒絕證書在 e_i=x_(i−1)x_i 上的 singleton palette 為 {γ_i}。
端點 tightness 補回被扣的 d，得 L₀^q={d,γ₁}、γ₁≠d；另一端同理。
每個內點的 residual 是其兩個相異 incident bridge palettes 的聯集：

\[
 L_j^q=\{\gamma_j,\gamma_{j+1}\},\quad
 \gamma_j\ne\gamma_{j+1},\quad d\in L_j^q.
\]

從第一條原邊歸納，即得

\[
 \gamma_{2h+1}=\beta_{2h+1}\ne d,\qquad
 \gamma_{2h}=d. \tag{1}
\]

不同奇數邊的 β **尚可不同**。但每條奇數邊 e_i 的兩端恰有同一
L_(i−1)^q=L_i^q={d,β_i}，包括 i=ℓ 與 ℓ=1。
因此 [首橋層 §4](c5_adjacent_degree5_no_mixed_t2_bridge.md#4-同一首橋-β-的跨列限制)
的 β 域與兩份穩定子支援族，原封不動適用於每條奇數原邊：

\[
 \mathcal B=\{\beta\ne d:\{d,\beta\}\cap K=D\cap K\},\quad
 \mathcal T_\beta=
 \mathcal T(q,S_C,\{d,\beta\})\cap\mathcal T(t,S_C,D). \tag{2}
\]

兩端的實際 T 都屬於同一 𝒯_β；不把族中支援當作可獨立實現的選擇。
若同一份三框弧 X,Y,D_B 與原外部路徑 L 排除該族，對 e_i 使用

\[
 W_{i-1},\ W_i,\quad
 (V(J)\setminus\{x_{i-1},x_i\})\cup V(L)\cup D_B,\quad X,\ Y,
 \quad J=P\cup\{rx_0,rx_\ell\}. \tag{3}
\]

J 刪相鄰兩點後的餘部經 r 連通；L 內部避開 C、B，將第三組接到
D_B。兩個 W、原分量身份及框弧分割保證五組不交。原 bridge、
兩條朝外 J 邊、四份實際附件及三個 C5 切口給十對鄰接，即來源 K5。
這是既有任意 bridge 的原圖引理，沒有另造 spoke 或更換供應點。

## 3. 唯一剩餘 β 迫使第二個 source 禁色

若 (2) 的所有 β 都由 (3) 或空支援族排除，則非空 P 已不可能。
若只剩一個 b，(1) 迫使全部奇數邊 palette={b}、全部偶數邊={d}，
從而每個 L_j^q={d,b}。

在同一 C 上構造 root 色改為 b 的 list 證書：**只交換 P 邊 palettes
中的 d、b；全部路徑外 block palettes 保持原值。**

- 非路徑頂點不鄰接 r，其 boundary lists 及所有 incident palettes 均未變。
- 路徑內點原有兩個 palettes {d}、{b}；交換後聯集及不交性均未變。
  旁支 palettes 與 {d,b} 不交，因 L_j^q={d,b}。
- 兩端原 list 的路徑部分是 {b}，root 色由 d 改為 b 後變成 {d}。
  新端邊 palette 恰為 {d}；直接附件及全部旁支 palettes 都不含 d、b。
  奇數長度保證兩個原端邊原先同為 {b}。

故每點的新 list 仍恰是 incident palettes 的不交聯集，每個原 block
仍有正確 palette 大小。Theorem 10 的充分方向給同一 C 不可著色，
亦即 b∈F_C(q)。b≠d 與原完整 F_C(q)={d} 矛盾。

這不是把局部 L 直接當成 F；第二禁色經**整個原 C 的拒絕證書**證成。
也不是全圖改色：兩 root、boundary 色框、另一原分量及染色關係定義
都未變，只為另一個 root 色建立 lists 不可著色的證明。
此處 b 可以是原 spoke 色：F_C 按完整 T_C 定義，對全部四色都有意義；
不宣稱整張 G 能將 r 染成 b，也不移除原 spoke 約束。

## 4. Record 54 及另外三個查詢

record 54 原 sides=(146,146)，B_z=B_w=24、S_z=0124、S_w=234，
F_z(q)=F_w(q)={3}。p₁ 唯一失敗完整候選為 ({2,3},{3})；取 C=C_z。
d=3、D={2,3}、K={0,3}，故所有奇數邊 β∈{1,2}。

β=1 的族為 04、24、014、024、124、0124。每塊碰 b4 並碰 b0／b2。
固定 X={b0,b1,b2}、Y={b4}、D_B={b3}，取原路徑
**L=z–w–C_w–b3**；C_w 的實際 234 支援保證此路徑存在，內部避開
C_z 及 B。式 (3) 排除任何位置的 β=1，容許兩塊各用不同的 b0／b2。

因此全路徑 β=2。§3 迫使 2∈F_z(q)，矛盾。β=2 的原族
01、12、012、014、124、0124 仍沒有統一三弧；本輪沒有誤記它為
K5 族，亦不要求其兩塊使用同一個 q 色 0 供應點。

| 原 record／列 | pair 分量 | 奇數 β 域 | 由原外部路徑排除 | 剩餘 β／強迫 source F 包含 |
| --- | --- | --- | --- | --- |
| 54／p₁ | C_z | 1,2 | 1；z–w–C_w–b3 | 2／{2,3} |
| 256／p₁ | C_w | 1,2 | 1；w–z–C_z–b3 | 2／{2,3} |
| 68／p₂ | C_w | 0,2 | 0；w–z–C_z–b0 | 2／{2,3} |
| 173／p₂ | C_z | 0,2 | 0；z–w–C_w–b0 | 2／{2,3} |

後兩項固定框弧為 123／4／0，target pair 是 {0,3}。強迫的 source
pair 不必等於 target pair，§3 只用 source palettes。每項都與原
F_C(q)={3} 矛盾。root 交換與 q-preserving 反射保持字面 target，
不將反射後的等色分割正規化來替代實際色列。

## 5. 套表、指定分離與出口接合

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py) 只讀前層
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/observations.json)，
驗 SHA256，保留原 IDs、原 side／frontier、完整 q schemas、placements、
四個具名接點的 rotations 與原每份完整 join。前層證據由原檔 hash
綁定，原 artifacts 不改寫；新 JSON 另存逐候選繼承結果及新證據。

重算 644 個查詢的 2,892 組完整 joins，逐項核對 160 組原失敗候選的
bridge／endpoint 證據；繼承 156 組反證，新增 4 組。全部完整候選
都有 root 色對或反證後，才標該 target 延拓。

| 階段 | target 已證 | 雙列皆證 | 未決 | 新來源排除 |
| --- | ---: | ---: | ---: | ---: |
| 原雙端點層 | 640 | 318 | 4 | 0 |
| 整條原路徑 palettes | 644 | 322 | 0 | 0 |

必要表的任意大小覆蓋配合本結果，證成 §1 圖類全部接受 p₁、p₂。
這是指定雙列分離；322 份必要資料不因而成為 disk 實現。
在 [出口定理](c5_single_sided_exit.md) 額外的來源假設
Σ(G)=Ω\{p,q} 下，minimal q-core M 繼承其他八列；本定理給 p，
而 q 仍拒絕，才得 Σ(M)=Ω\{q}，接上第一個 strict deletion。

下一窄入口為無 mixed 的 **t_z=2,(2)，t_w=1,(2,1)**；先從原同色
join 表的 3,548 份中已讀出此有序型 136 份，首項原 sides=(133,91)；
B_z=01、F_z(q)={2}，B_w=0、(F_Cw,F_Dw)=({1},{2})、共同 c=3。
先綁定這個子表，保留 C_z、C_w 的二接點分量及 w 的 singleton
分量，建立 actual-support／rotation 必要覆蓋。交換 roots 覆蓋反向。
此處不重新枚舉圖，也不把兩側 t=2 的六單位次序直接套到不同分拆。
其他 t=0、兩側 t=1、較大／多 mixed 與一般出口保留。

## 6. 有限控制與重播

- 獨立枚舉四個 source 色、長度 1／3／5／7 的全部 edge words，
  核對 (1)；96 個直接附件／旁支 palette 聯集控制核對 §3 的 list 等式。
- 192 份 abstract Gallai controls：12 個有序 (d,b)、長度 1／3／5／9，
  無旁支、bridge 葉、triangle、巢狀 bridge／triangle 四型；獨立 list
  solver 算完整有序端點 relation，再取禁色交集，均得到 {d,b}。
- 704 份 K5 skeletons：長度 1／3／5／9 的每條奇數邊、16 種雙塊
  tether 形狀、b0／b2 的四種雙塊供應方式；每份核對原五組、十鄰接、
  root 交換及反射。原 zw、四 spokes、兩原分量及實際外部路徑均保留。
- 322 次 target root 交換、4 組新候選的完整 root 交換／字面反射。
  13 個負控制包含首橋 β 不約束後續奇數 β、非守恆 d、singleton
  target、偶數路徑，以及刪 bridge／zw／外部 tether／附件、框弧斷裂
  與 branch-set 重疊。變動奇數 palettes 的完整 relation 仍可只禁 d。

資料見 [JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_path_palettes/observations.json)
與 [完整表](../artifacts/c5_adjacent_degree5_no_mixed_t2_path_palettes/support_table.md)。
有限 Gallai 控制不宣稱具備原 boundary／degree 全部前提；minor skeletons
亦非來源實現。任意大小覆蓋由 §1–3 的紙面論證承擔。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-path-palettes.md)。
`--check` 重算並逐 byte 比對；無參數只生成本層。`lake build` 不將
新紙面證明、外部 degree-list 定理或 disk 拓撲形式化。
