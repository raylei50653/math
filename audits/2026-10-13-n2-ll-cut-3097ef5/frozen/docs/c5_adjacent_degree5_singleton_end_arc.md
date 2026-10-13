---
docgraph:
  id: c5.adjacent-degree5-singleton-end-arc
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-singleton-middle-arc
  requires:
    - c5.adjacent-degree5-singleton-long-arc
    - c5.adjacent-degree5-shared-singleton
    - c5.single-spoke-two-two-external
  related:
    - c5.single-sided-exit
---
# 相鄰雙 degree-5：共鄰單點 34／40 長弧的來源排除

後續（2026-09-28）：[唯一 mixed 原 K2](c5_adjacent_degree5_mixed_edge.md) 已完成
本頁下一入口的各一接點必要化約，[原四環次序](c5_adjacent_degree5_mixed_edge_order.md)
再將此接線型全部作 disk 來源排除。[共鄰端點型](c5_adjacent_degree5_mixed_edge_shared.md)
的 [w 側 t=2、(1)](c5_adjacent_degree5_mixed_edge_shared_t2.md) 亦已證雙列、
接入出口第八類；其餘分拆仍保留，下文保留 34／40 輪的語境。

2026-09-28。接續 [12 長弧分離](c5_adjacent_degree5_singleton_middle_arc.md)。
**接受全部 T4 的 induced-C5 disk minimal q-core，若恰兩個相鄰內點
z、w 完整 degree=5，其餘內點完整 degree=4，且唯一 mixed 分量是
共鄰 singleton x，則 N_B(x) 不可能為 {b3,b4} 或 {b4,b0}。**
q=01012 固定，來源大小不受限。

34 長弧的 152 筆必要配置中，原 x 路徑 K5 排除 120 筆；其餘 32 筆
全部必拒絕同一 T4 列 01213。整張來源反射到 40，獨立重算亦為 152
筆、120＋32 全排除。沒有保留來源，也沒有新增 target 著色見證。

結合 [同側限制](c5_adjacent_degree5_singleton_sectors.md)、
[01／23](c5_adjacent_degree5_singleton_long_arc.md) 與 12 結果，
**唯一 mixed 共鄰單點的全部 boundary 支援均已處理**，可將
[條件式出口](c5_single_sided_exit.md) 第七類移除 x 支援限制。
紙面任意大小化約、外部 degree-list 定理與 Python 有限證書分層；
未新增 Lean theorem，也未證一般雙 root、一般出口或 K∞=K≤5。

## 1. 同一來源與 34 的必要禁色

G 是有限簡單 disk 圖，B=(b0,…,b4) 為 induced 外圈；有效內部 H
非空連通。G 拒絕 q，刪任一非框邊後接受 q，並接受全部四色 proper
rows T4。z、w 是恰兩個完整 degree-5 內點且 zw∈E(G)，其餘有效內點
完整 degree=4。H−{z,w} 的唯一 mixed 原分量是 {x}，本節取
N(x)={z,w,b3,b4}。其餘每個原分量只接一個 root。

前報告的單 root 消去與 (3) 排除仍適用。每側只有 (2)（二接點原分量
C_r 加一條原 spoke r–b_s），或 (2,1)（C_r 加單接點原分量 D_r）。
F_C(β) 是**整份原分量**完整可延拓接點 tuple 色集的交集，等價於使
C 無法著色的 root 色集合；容量不超過原接點數。E_r(β) 為 root list
扣去該側所有 F，且每列皆非空。固定 root 色後才選完整 tuple。

這次 q 下 x list 是 T={0,3}，T 外色 O={1,2}。minimality 給

\[
\varnothing\ne E_z,E_w\subseteq T,\qquad E_z=T\text{ 或 }E_w=T.
\tag{1}
\]

每側的必要禁色為

\[
\begin{array}{ll}
(2):&q_s\in O,\quad F_{C_r}(q)=(O\setminus\{q_s\})\cup(T\setminus E_r);\\
(2,1):&F_{D_r}(q)=\{h\},\quad
F_{C_r}(q)=(O\setminus\{h\})\cup(T\setminus E_r),\quad h\in O.
\end{array}\tag{2}
\]

每個 F 另須在逐色固定 q(S_C) 的置換下不變，且對其中每色 f 有
|q(S_C)∪{f}|≥2。式 (2) 使用實際 q，不把前輪 T={2,3} 的公式照抄。
checker 另由既有 80 筆 T={0,3} 抽象 minimality 資料按實際 spoke、
支援穩定子篩選，逐幾何配置核對與式 (1)–(2) 的候選集合完全一致。

## 2. 任意大小的次序與原 x 路徑 K5

同側定理先排除短弧，故 H−x 在長弧 L=(4,0,1,2,3) 一側。
[原三角形次序證明](c5_adjacent_degree5_singleton_long_arc.md#2-原三角形外側給固定長弧次序)
不依賴框點編號：原 hub B∪{r,x} 連通並避開 unary C，使拒絕的 C
為 K4-free；支援只有一點（甚至只有一個 q 色）與非空禁色、tightness
及 Gallai leaf-block degree 矛盾。因此每份 unary actual support 至少
兩點，並滿足 §1 的外部色條件。
拒絕 degree lists 的緊性與 block palettes 沿用
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪核對原文；這仍是外部定理。

每份 unary 都接 B，原三角形 xzw 的有界內側遂無其他有效頂點。
在其外側 annulus 沿 xb4、xb3 切開，兩 root 各佔連續區塊，每側 C_r
與 spoke／D_r 相鄰；同一 C_r 的兩個原 contact 亦相鄰且保留兩方向。
原分量內的 crosscut 使各單位 actual supports 在 L 上滿足

\[
\max\widehat S_{O_j}\le\min\widehat S_{O_{j+1}}.\tag{3}
\]

O 包含兩種 root 次序及每側兩種單位次序。不同單位可共用同一框點，
但不複製該頂點或顏色；支援不必填滿區間。這是讀取原嵌入的必要式，
沒有反向假定符合式 (3) 的資料能實現為圖。

若某二接點 C 有 |F_C(q)|=2，兩 contact 間仍為原奇數長 bridge 路徑
P。刪去 P 的邊後，每個含 v_j 的原旁支塊 W_j 都滿足
D(F)⊆q(N_B(W_j))，其中 D(F)=F（3∉F），否則 D(F)=U∖F。
若兩個必要色在 S_C 各只有一個供應點 b_a、b_b，且 a,b 相鄰，則
每個 W_j 都實際接到兩點。取 h∈{3,4}∖{a,b}，原 r–x–b_h 接到補弧。
令 J 為 P 加兩條原 root-contact 邊。任取 P 上相鄰 v_j,v_{j+1}，五組

\[
W_j,\ W_{j+1},\
Z=(V(J)\setminus\{v_j,v_{j+1}\})\cup\{x\}\cup(B\setminus\{b_a,b_b\}),\
\{b_a\},\ \{b_b\}\tag{4}
\]

給來源 K5 minor。Z 含 r，由原 rx、xb_h 接到三點補弧；五組非空、
連通且互不相交。P 原邊、J 其餘兩側邊、四條 actual tethers 與三條
框邊給全部十條鄰接。此證明不限制 bridge 長度、旁支大小，也不需 T4。
同色多供應點不能任取一點，{a,b}={3,4} 時亦不能使用這條補弧路徑。

## 3. 全部必要配置與共同 T4 矛盾

式 (1)–(3)、支援穩定子與外部色條件給下表。幾何域另由獨立 Cartesian
hull 分離重算；所有記錄保留具名分量、原 contact 的四種方向及 q 禁色。

| 兩側分拆 | 幾何配置 | q 必要記錄 | K5 排除 | T4 排除 | 保留 |
| --- | ---: | ---: | ---: | ---: | ---: |
| (2) / (2) | 376 | 80 | 56 | 24 | 0 |
| (2) / (2,1) | 88 | 32 | 28 | 4 | 0 |
| (2,1) / (2) | 88 | 32 | 28 | 4 | 0 |
| (2,1) / (2,1) | 8 | 8 | 8 | 0 | 0 |
| 合計 | 560 | 152 | 120 | 32 | 0 |

K5 後的 32 筆可完整壓成下列八種近 b4 側 A，乘上兩種遠側 B 的
spoke，再乘 root 名字交換。遠側恆為 (2)，C_B 支援 123、禁色 {2,3}，
spoke 在 b1 或 b3。此八型表與完整 32 筆集合由 checker 核對相等。

| A 的分拆 | C_A actual support | F_C(q) | spoke 或 D_A 的支援與 F_D(q) |
| --- | --- | --- | --- |
| (2) | 04 | {2} | spoke=1 |
| (2) | 014 | {1} | spoke=4 |
| (2) | 014 | {2} | spoke=1 |
| (2) | 14 | {1} | spoke=4 |
| (2) | 14 | {2} | spoke=1 |
| (2) | 01 | {1} | spoke=4 |
| (2,1) | 04 | {2} | D:01，{1} |
| (2,1) | 01 | {1} | D:04，{2} |

取 β=01213∈T4。在 A 的全部 actual supports 上，β=(2 3)q；這個
**同一色置換搬運 A 的全部原分量與 spoke**，使 E_A(β)={0,2}。
在 B 的全部支援 123 上，β=(0 2)q，所以 F_C(β)={0,3}，spoke 色仍
為 1，給 E_B(β)={2}。不同側的置換僅推導各自完整關係在同一 β 下的
值；接合時所有集合均已回到共同的 β 色框，不拼接不同列的 coloring。

x 在 β 的 list 為 U∖{β₃,β₄}={0,2}。原三角形 xzw 要求三色互異，
但 E_A、E_B 與 x list 的聯集只有 {0,2}，故 β 必拒絕，違反 T4。
全部 32 筆的分量搬運皆精確，不需猜測跨列禁色或用有利的上界選項。
於是 **34 的來源不存在**；q、p₁、p₂ 的 x list 雖都為 {0,3}，已無
保留來源需要 target 接合。不得把這輪計作 304 個新 target 延拓。

## 4. 整張來源反射與全部 singleton 出口

取 ρ(i)=3−i mod 5、π=(0 1)，列搬運 (Tβ)_i=π(β_ρ(i))。
Tq=q，{3,4} 搬到 {0,4}，長弧反向成 (0,1,2,3,4)，q 的 x list
從 {0,3} 搬到 {1,3}。對原來源一併搬運所有附件、禁色集合、單位次序、
contact 方向與排除見證；K5 原路徑仍是原路徑，T4 列搬為 Tβ=02013。
所以 40 來源亦不存在。

checker 另按 40 的實際 q 色重新生成 152 筆，證反射是兩表間的雙射，
逐筆核對 K5 類別、路徑 landing 或完整 T4 禁色與 residual 選項。
獨立搜尋找到的首個 T4 見證不必等於反射列，兩份證據均保存。
反射不是只正規化一列而固定其他來源資料。

所有 x 支援現在如下：同側定理排除重色與不合 T4 的位置，非相鄰 03
的唯一保留側因 b4 未接而只缺 q；01／12／23 接受指定 p₁、p₂；34／40
由本報告作來源排除。因此若 M 是雙缺失來源 Σ(G)=Ω∖{p,q} 的 minimal
q-core，且唯一 mixed 為共鄰 singleton，則刪邊繼承給
Σ(M)⊇Ω∖{p,q}；對齊後 p 為 p₁ 或 p₂，前述分類保證 M 接受 p。
故 **Σ(M)=Ω∖{q}**，接回 silent deletions 後第一次釋放 p 的出口。
第七類不再需要 x 支援前提；此步仍明用雙缺失來源與刪邊繼承。

## 5. 證書、重播與停止點

[checker](../scripts/c5_adjacent_degree5_singleton_end_arc.py)、
[JSON](../artifacts/c5_adjacent_degree5_singleton_end_arc/observations.json) 與
[34／40 完整表](../artifacts/c5_adjacent_degree5_singleton_end_arc/support_table.md)
保存 source／直接輸入 SHA256、兩份必要表、前輪 abstract index、全部
接點方向、K5／T4 見證、八型壓縮及反射核對。前輪 source／artifacts 不改寫。

34、40 各有 108 份原 x 路徑 K5 skeleton，涵蓋全部可用 pair／landing、
長度 1／3／5 的每條 bridge cut、直接／共幹 tethers；各份刪 rx 後指定
witness 必失效。216 skeletons 不是 degree/list 來源，也不證刪 rx 後
全圖平面。另有完整 binary 關係與 marginal 乘積不同禁色的負控制。

```bash
python3 scripts/c5_adjacent_degree5_singleton_end_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_middle_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-28-adjacent-singleton-end-arc.md)。
下一窄入口取唯一 mixed 原分量 C={u,v}、uv∈E，每 root 各一個 incidence，
即原 z–u–v–w–z 四環；重新推導完整有序 R_C 與逐邊 minimality，再處理
actual supports。不能把 singleton 的 T、私有色公式或三角形次序沿用
到 K2。研究優先序見 [HANDOFF](HANDOFF.md)；無 mixed、較大／多 mixed、
一般雙 root、degree≥6、一般單側／共同出口及主命題仍保留，未 Lean 化。
