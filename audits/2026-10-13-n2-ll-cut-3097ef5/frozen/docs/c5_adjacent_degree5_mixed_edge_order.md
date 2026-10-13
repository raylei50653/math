---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-order
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge
  requires:
    - c5.no-spoke-supports
  related:
    - c5.single-sided-exit
---
# 相鄰雙 degree-5：原四環外側次序排除唯一 mixed K2 各一接點型

後續（2026-09-28）：[共鄰端點型](c5_adjacent_degree5_mixed_edge_shared.md) 已完成
P*ᶻ={u,v}、P*ʷ={u} 的完整關係與逐邊 minimality，強迫 z 無 spoke 且
恰一個二接點 unary 分量；w 容量飽和，原路徑 K5 後保留 288 筆必要資料。
其中 [w 側兩條 spoke](c5_adjacent_degree5_mixed_edge_shared_t2.md) 的支援／環序
及雙列分離已完成，其餘 w 分拆仍保留；下文保留各一接點排除輪的語境。

2026-09-28。接續 [K2 必要化約](c5_adjacent_degree5_mixed_edge.md)。
**在該報告的 induced-C5 disk、edge-minimal q-core 前提下，唯一 mixed
原分量為 uv、root incidence 恰為 zu、wv 的來源不存在。** 不需接受 T4，
不限制 unary 分量大小；未處理 K2 端點同時接兩 root 的其他接線。

原定窄題一色側 t=2、(1) 已由四環外側的跨度矛盾排除。同一引理接著
排除前輪 576 筆中的 552 筆；剩餘 24 筆必飽和 C5 周長，其原次序與
q 支援不相容，亦全排除。原 816／576 抽象資料不改寫，新證書逐筆引用
原 ID；這是新增 disk 來源排除，不是把原有限必要表稱為圖枚舉。

信任層為任意大小紙面證明、沿用外部 degree-list 定理與 Python 有限
控制；沒有新增 Lean theorem。一般單側／共同出口及主命題仍未證。
研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源、完整關係及局部支援

G 有限簡單，B=(b0,…,b4) 是 induced disk 外框；有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}，G 拒絕 q，刪任一非框邊後接受 q。
z、w 相鄰且完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量為 C*={u,v}，原邊 uv 存在，且
P*ᶻ={u}、P*ʷ={v}。因此 N_B(u)、N_B(v) 各有兩個不同原框點。

各 unary 原分量 C 的全部邊、接點、旁支與 actual support S_C 保留。
F_C 是其完整有序 tuple 關係中所有 tuple 色集的交集；不使用端點
marginals。前輪已證 F_C 非空、容量不超過接點數，原四環 z–u–v–w–z
內側為空，且平面來源每份 unary 接點數至多二。

用角色 r_s、r_l 表示 residual 一色、兩色的原 root；相應 mixed 端點
為 p_s、p_l。若 r_s=z，則 (p_s,p_l)=(u,v)；若 r_s=w，則為 (v,u)。
這是記號對應，沒有交換一個分量的色框。寫

\[
E_s=\{d\},\quad E_l=\{d,e\},\quad d\ne e,\qquad
q(S_{p_s})=\{0,1,2\}\setminus\{d\},\quad
q(S_{p_l})=\{0,1,2\}\setminus\{e\}. \tag{1}
\]

**每份 unary 支援至少見兩個 q 色。** 沿用前輪原 r–p_r–B 的連通
外部 hub，拒絕的 C 是 K4-free Gallai tree。若 q(S_C) 只有一色 a，
固定 a 的另外三色置換與 0<|F_C|≤2 迫使 F_C={a}。固定 root=a 後，
每個外鄰色均為 a；拒絕 degree lists 的 tightness 使每點最多一個
外鄰居，故 deg_C≥3。但 K4-free Gallai tree 的 leaf block 有內度≤2
的非 cut 點，矛盾；singleton C 同樣不可能。空支援由全色對稱排除。

這與 [既有支援引理](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)
使用相同局部論證，外部 hub 改由原四環端點提供。tightness 與 Gallai
結構沿用 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪核對原文；未在 Python 或 Lean 重新證明此外部定理。

若 F_C={3}，則 **q(S_C)={0,1,2}**：缺少任一 q 色 h 時，交換 h 與 3
會固定所有實際 boundary 色卻改變 F_C，矛盾。這對單／二接點均成立，
使用整份關係的置換不變性。

## 2. 原四環外側的同序區塊與周長界

以原四環及其空的閉內部取小正則鄰域，外側是 annulus。內圓周的外側
入射邊保留 z、u、v、w 的循環區塊次序，或其整體反向。稱每個 unary
原分量為一個單位；u、v 各連同自己的兩條 boundary spokes 作一個
單位；每條 root-spoke 另作零跨度單位。所有單位都接內、外兩個邊界。

**同一 unary 的接點不能夾住另一單位。** 若二接點被另一單位分開，
取 C 內連接兩接點的原簡單路徑，連同兩條 root-contact 邊成 Jordan
曲線。它完全在 B 內部，不含 B 側的被夾單位不能到達 B。若該側是
四環的方向，則 u／v 的實際 spokes 亦不能到 B。因此每份原 C 的
contact 在 root 外側成連續區塊；兩接點內部方向仍可任選。

**外框附件也成同序區塊。** 在每個 b_i 的小鄰域內分開不同原入射
邊端，保持它們是同一框點、同一 q 色。沿 u／v 的內圓周短區塊接起
其兩條截短 spokes，只是用來讀取原星狀鄰域，沒有新增著色接線。
各 unary 區塊與這兩個星狀區塊可取兩兩不交、同時碰 annulus 兩邊界
的連通細鄰域。

在任一單位內連接兩個外端，得到外圓周 crosscut；不含內圓周的一側
不能有另一單位的外端，因它還須連回內圓周。同理，內端與外端的
區塊序不同會給交錯的兩條不交 crosscuts。這是既有 annulus 引理的
同一 Jordan 論證，但內圓周次序由**原四環**而非三角形決定。
共享 b_i 只允許區塊端點重合；不能使兩個正跨度單位重用同一開框邊。

因此沿某個起點提升所有單位的 actual supports 為整數集 T_i，可令

\[
\max T_i\le\min T_{i+1},\qquad
\max T_{\rm last}\le\min T_0+5,\qquad
T_i\bmod5=S_i. \tag{2}
\]

令 ℓ_i=max T_i−min T_i。unary、u、v 都至少有兩個支援點，故 ℓ_i≥1；
禁 {3} 的 unary 至少有三個支援點，故 ℓ_i≥2。每條 root-spoke 為
ℓ=0。正跨度單位不可能獨佔整圈，因其他單位也有正跨度；故同一
支援內的不同框點各提升一次。支援允許有間隙，沒有假設填滿區間。
由 (2) 得

\[
\boxed{\ \sum_{C\ {m unary}}\ell_C+\ell_u+\ell_v\le5.\ } \tag{3}
\]

此論證保留任意橋長、分叉及 block 數；只提取來源必要的外側次序。

## 3. 先完成 t=2，再消去其餘超周長型

一色側 t=2、(1) 的唯一 C_s 禁 {3}。兩色側 (2) 或 (2,1) 也都有
一份原 C_l 恰禁 {3}，且它與 C_s、u、v 是四個不同單位。因此

\[
\ell_{C_s}+\ell_u+\ell_v+\ell_{C_l}\ge2+1+1+2=6>5.
\]

**原定窄題已作來源排除。** 其他 unary 支援或 root-spokes 只會增加
限制，無須跨列挑選任何新 F。共享框點已由 §2 的端點等號保留。

同一界可直接用在前輪的全部正常形。以下各下界對整型有效，某些
禁色分配的實際下界更高；checker 保存每筆原 ID 的精確局部下界。

| 一色側 t／分拆 | unary 總跨度下界 | 兩色側 (2) 時含 u、v 的總下界 | 兩色側 (2,1) 時總下界 |
| --- | ---: | ---: | ---: |
| 2／(1) | 2 | 6 | 7 |
| 1／(2) | 1 | 5 | 6 |
| 1／(1,1) | 3 | 7 | 8 |
| 0／(2,1) | 2 | 6 | 7 |
| 0／(1,1,1) | 4 | 8 | 9 |

兩色側 (2) 的 F={3}，下界二；(2,1) 的兩份 F 分別為 {f}、{3}，
下界至少三。一色側 (1,1)、(1,1,1) 各有一份 singleton F={3}，
其他分量至少一。因此唯一可能不超周長的型為

\[
t_s=t_l=1,\qquad P_s=P_l=(2). \tag{4}
\]

576 筆中，552 筆已由 (3) 排除；(4) 保留 24 筆抽象資料。原定 t=2
的 36 筆包含在 552 筆內，沒有與獨立 u／v 支援表相乘稱為來源數。

## 4. 飽和型的原次序與六個矛盾

記兩側二接點原分量為 C_s、C_l，一色側 spoke 的 q 色為 h。
由前輪容量飽和與 root-spoke minimality，

\[
F_{C_s}=U\setminus\{d,h\}=\{g,3\},\quad d\ne h,\qquad F_{C_l}=\{3\}.
\tag{5}
\]

固定支援色的置換須保持 F_{C_s}，因此 **d、h 均出現在 q(S_{C_s})**。
例如若缺 d，交換 d 與 3 就固定該支援卻改變 F。這仍是整份完整
tuple 關係的推論，並未把兩接點獨立選色。

(3) 此時恰為 1+1+1+2=5，全部跨度取等且框弧沒有間隙。所以：

- C_s、p_s、p_l 各支援一條原框邊的兩端；
- C_l 支援三個連續框點，且三個 q 色皆見；
- 四單位沿原四環的次序為 C_s,p_s,p_l,C_l 或整體反向。

原 root-spokes 保持在各 root 區塊，落點只能是相應 C_s／C_l 弧的
端點。下列矛盾在加入 spoke 色限制之前已成立，故同時涵蓋其兩種
側位置及每份二接點的兩個內部方向。

q=01012 的三色連續三點只有 234、340、401。每份配合兩種原次序，
得到全部六種必要幾何；表中支援按框點編號寫出，340 寫作 034。

| S_Cs | S_ps | S_pl | S_Cl | (d,e) 由原 mixed 支援決定 | 矛盾 |
| --- | --- | --- | --- | --- | --- |
| 04 | 01 | 12 | 234 | (2,2) | 違反 d≠e |
| 12 | 01 | 04 | 234 | (2,1) | C_s 支援未見 d=2 |
| 01 | 12 | 23 | 034 | (2,2) | 違反 d≠e |
| 23 | 12 | 01 | 034 | (2,2) | 違反 d≠e |
| 12 | 23 | 34 | 014 | (2,0) | C_s 支援未見 d=2 |
| 34 | 23 | 12 | 014 | (2,2) | 違反 d≠e |

四行直接違反 mixed K2 的必要非對角禁對；另兩行違反 (5) 的整分量
支援不變性。無論 r_s 是原 z 或原 w，角色次序都是同一原四環的
正向／反向，所以全部涵蓋。**(4) 亦不存在，完成此 K2 接線型的來源排除。**

## 5. 證書、接合與停止點

[checker](../scripts/c5_adjacent_degree5_mixed_edge_order.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_order/observations.json) 與
[排除表](../artifacts/c5_adjacent_degree5_mixed_edge_order/exclusion_table.md) 保存：

- 十種非空容量≤2 禁色集合的實際支援穩定子及最小跨度；任意大小
  支援必要性仍由 §1–2 的紙面論證承擔。
- 獨立按 cyclic hull 的框邊 mask 互斥重算 360 份四單位幾何，再按
  原四環次序及跨度 1,1,1,2 抽出十份；與直接生成的十份完全一致。
  此處只有 C_l 的三個點全佔其弧，其餘一般支援仍允許有間隙。
- 原定 t=2 的放寬四支援域：兩份 {3} 支援各九種、mixed 有序支援
  四十種，共 3,240 組，零組能放入上述 360 份幾何；此數與 576 筆
  抽象資料分層，不代表完整來源枚舉。
- 576 個繼承 ID：552 份周長矛盾，24 份各核對十種飽和幾何，共
  240 次同來源資料比對，全部矛盾。原 z/w/u/v 身份、spoke 落點候選、
  二接點內部方向均保存；沒有 target 接受或來源可實現性宣稱。
- 576 份原資料及十份幾何的反射，另保留允許共享端點的周長五正控制。
  所有排除均未使用 T4；未產生跨列拼湊的 coloring。

本結果加入 [單側出口的失敗核心限制](c5_single_sided_exit.md#5-為何尚不是無條件的一般定理)：
該 minimal core 接線型不存在。既有七類條件式出口不須增加空的第八類，
也不由來源排除推論一般出口已證。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [本輪紀錄](history/2026-09-28-adjacent-mixed-edge-order.md)。
`lake build` 不表示原四環的 Jordan／Gallai 證明已 Lean 化。

**下一窄入口：** 唯一 mixed 原 K2 的共鄰端點接線，例如
P*ᶻ={u,v}、P*ʷ={u}。先重推保留共鄰 u 的完整 ordered tuple 關係與
逐邊 minimality；該型不滿足本頁的各一接點前提，不能套用 (1) 或
兩端各兩條 boundary spokes。無 mixed、其他較大／多 mixed、非相鄰
雙 root、degree≥6 與一般出口仍保留，不重啟唯一 degree-5 圖枚舉。
