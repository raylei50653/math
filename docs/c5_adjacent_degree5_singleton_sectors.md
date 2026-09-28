---
docgraph:
  id: c5.adjacent-degree5-singleton-sectors
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-shared-singleton
  related:
    - c5.single-sided-exit
---
# 相鄰雙 degree-5：共鄰單點的同側限制與 target 重色排除

後續（2026-09-28）：[01 長弧次序與原 x 路徑 K5](c5_adjacent_degree5_singleton_long_arc.md)
已證 x 接 01／23 的指定雙列分離，[12 長弧](c5_adjacent_degree5_singleton_middle_arc.md)
亦已完成；[34／40 來源排除](c5_adjacent_degree5_singleton_end_arc.md) 補齊
全部 singleton 支援並接回條件式出口。
下文二十位置與歷史停止點維持原輪語境。

2026-09-28。接續 [唯一共鄰單點化約](c5_adjacent_degree5_shared_singleton.md)。
**在出口問題繼承的 disk＋T4 前提下，x 接 {b1,b4} 或 {b2,b4} 的來源
皆不存在。** 因此前輪指定的 p₁／p₂ 重色情形，包括兩側剩同色 singleton
的障礙，已作來源排除。證明先用原 zw 保證 H−x 連通，再用同側限制與
未接框點改色；不必分類 unary 分量的 blocks 或猜測 target 禁色。

全部非相鄰 x 支援亦已處理：唯一尚可符合 q 拒絕、T4 接受的位置是
{b0,b3} 的 arc (b0,b1,b2,b3)，它必有完整 Σ=Ω\{q}。
尚未分離的來源只剩五種相鄰支援的長弧位置；不是五張圖或五個完整介面。
研究優先序見 [HANDOFF](HANDOFF.md)。

新結果是任意大小的紙面拓撲／改色證明與 Python 固定域核對；不新增外部
degree-list 依賴或 Lean theorem。此處的 disk、T4 是**明列的額外前提**，
不把前報告只需一般 planarity 的 (2)／(2,1) 化約提升成相同範圍的排除。

## 1. 固定來源與適用前提

G 是有限簡單 induced-C5 disk 圖，具名外圈 B=(b0,…,b4)，
q=01012、p₁=01021、p₂=01212，U={0,1,2,3}。G 接受全部四色列 T4，
是 minimal q-core；有效內部 H 連通。z、w 為相鄰完整 degree-5 roots，
其餘有效內點完整 degree=4。H−{z,w} 中唯一同時接兩 root 的分量為
原 singleton {x}，所以

\[
N_G(x)=\{z,w,b_i,b_j\},\qquad i\ne j.
\]

其餘原分量只接 z 或只接 w，全部具名附件、接點次序、原 zw 及共同色框
維持不變。前報告已證 q_i≠q_j，且每側 unary 接點分拆只剩 (2)／(2,1)。
**下面同側引理不需要這項分拆分類**，也不使用它的 Gallai／K5 證明。

T4 的來源是 [出口接合](c5_single_sided_exit.md) 的雙缺失圖；刪邊到核心
繼承全部已接受列。本報告的 T4 前提不要求完整 Σ(G)=Ω\{p,q}，
除了 §4 的單缺失結論，也不從接受雙列直接推完整 Σ。

## 2. 原 zw 強迫整個 H−x 在同側

**連通補集引理。** H−x 非空連通。

證明：z、w 由原邊 zw 連通。每個其餘 H−{z,w} 原分量至少接一個 root，
因 H 連通，且不同原分量之間沒有邊。刪掉獨立的原分量 {x} 不影響這些
root 邊。將全部原分量接回 zw，得到 H−x 的連通性。這保留整個分量，
沒有只取接點的邊際關係。

在原 disk 嵌入中，P=b_i–x–b_j 是連接兩個不同框點、內部在 disk 內的
簡單弧。它把 disk 分成兩個開區域；各區域閉包的外框部分是 i、j 間的
一條閉 boundary arc。H−x 的頂點與邊全避開 P，且 H−x 連通，故它
全部位於同一開區域。特別是 z、w 不能分居兩側，否則原邊 zw 會穿過 P。

令 I 為該側的閉 boundary arc。任何從 H−x 到 B 的原邊只能終於 I；
否則它從此區域穿過 P 或外框。x 自己只接 b_i、b_j，亦屬 I。因此

\[
N_B(H)\subseteq I. \tag{1}
\]

所有 B\I 頂點在 G 中都沒有有效內鄰點。這是整張來源的支援包含式，
不是各 unary 分量可獨立挑選所在側；也不宣稱 I 的每個點一定被接到。
若有忽略的孤立內點，它們可任意著色，不影響論證。

**精確跨列不變性。** 若 proper rows β、γ 在 I 上相同，則每個原分量的
完整接點關係相同、兩 root lists 相同、x list 相同，故

\[
\mathcal T_C(\beta)=\mathcal T_C(\gamma),\quad
E_z(\beta)=E_z(\gamma),\quad E_w(\beta)=E_w(\gamma),\quad
Z_G(\beta)=Z_G(\gamma). \tag{2}
\]

更直接地，保留同一份內部 coloring，只改 B\I 的顏色；所有內外邊都不
受影響，框邊由兩列 proper 保證。式 (2) 不需色置換，也沒有跨列拼接見證。

## 3. 指定兩個 target 重色情形作來源排除

若 v∉I 且 q_v 在 q 中不是 singleton 色，將它改成未用色 3 得 q′。
q′ proper 且用四色，於 I 上仍與 q 相同。T4 給 q′ 的完整 coloring，
式 (2) 把同一 coloring 搬回 q，矛盾。這就是
[未接內點改色引理](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)
在同一來源的應用；不用四色定理作 oracle。

兩個指定 x 支援的每一側都存在這種 v：

| x 的原 boundary 鄰點 | H−x 所在閉 arc I | 未接框點 v | 被迫與 q 同拒絕的 T4 列 q′ |
| --- | --- | --- | --- |
| {b1,b4} | (b1,b2,b3,b4) | b0 | 31012 |
| {b1,b4} | (b4,b0,b1) | b2 | 01312 |
| {b2,b4} | (b2,b3,b4) | b0 | 31012 |
| {b2,b4} | (b4,b0,b1,b2) | b3 | 01032 |

因此這兩種支援的 disk、T4-accepting minimal q-core **根本不存在**。
不需要再假定 E_z(p)=E_w(p)={c}，也不把 x 全開當作延拓的充分條件。
前輪任意列拒絕公式保持有效；新排除使用的是額外的同側支援限制。

在 q_i≠q_j 前提下，p₁ 使 x 的兩個框鄰點同色恰為 {b1,b4}，p₂ 則
恰為 {b2,b4}。故任一尚待分離的實際來源，其 x 在兩個指定 p 下都仍
有二色 list。**一般 planar 或不接受 T4 的來源不由本節排除。**

## 4. 全部具名位置的必要分類

十個具名 boundary pairs 各有兩側，共二十個位置。紙面分類如下：

| x 支援／所在側 | 位置數 | 結論 |
| --- | ---: | --- |
| {b0,b2} 或 {b1,b3}，任一側 | 4 | q 下 x 的框鄰色重複，使 R_x(q)=U²，違反 x 邊的 minimality |
| 五個相鄰 pair 的短弧 | 5 | I 外有 q 的重複色頂點，與 T4 矛盾 |
| {b1,b4} 或 {b2,b4}，任一側 | 4 | §3 的具體 T4 矛盾 |
| {b0,b3}，arc (b3,b4,b0) | 1 | b1、b2 未接，與 T4 矛盾 |
| {b0,b3}，arc (b0,b1,b2,b3) | 1 | b4 未接，完整 Σ=Ω\{q} |
| 五個相鄰 pair 的長弧 | 5 | I 包含全部五點，本論證未決 |

其中單缺失情形由未接內點引理立即得到：q 的 singleton 正是 b4，T4
已接受，故其餘九個 patterns 皆接受。兩個 target 的具體同圖操作是

\[
p_1=01021\ \leftarrow\ 01023,\qquad
p_2=01212\ \leftarrow\ 01213,
\]

先取右邊 T4 的完整 coloring，再只還原 b4。這證明任何實際存在的此類
來源只缺 q，**沒有證明此位置可實現**。它已屬出口接合的「未接內點」類，
故不需新增第七種可處理核心或改寫出口定理。

剩餘五個長弧位置仍須使用原 unary 分量的 (2)／(2,1)、實際支援及式 (6)
處理 target。前輪 240 筆 q 必要關係沒有附位置，不可直接扣去本表的
排除數或聲稱只剩五筆關係；本輪不改寫其證書。

## 5. 證書、依賴與停止點

[checker](../scripts/c5_adjacent_degree5_singleton_sectors.py) 與
[certificate](../artifacts/c5_adjacent_degree5_singleton_sectors/observations.json)
使用標準 Python，保存程式與直接輸入的 SHA256。

- 保存二十個具名位置與全部適用的單點 T4 改色見證；四個指定 target
  位置都標為來源不存在，不標作已找到 target coloring 的來源。
- 對 q 下異色的十六個位置，獨立遍歷各 1,024 個 S4-invariant signatures，
  以全部 240 proper rows 建立「I 上同列」等接受值約束，再加 q 拒絕及
  T4 接受，共 16,384 次核對。十個位置無相容 mask；{b0,b3} 長弧
  唯一 mask 為 1022；五個相鄰長弧各有十六個抽象 masks。這些 masks
  是必要代數候選，未驗證來源可實現性。
- 沿用 [單 root 介面證書](../artifacts/c5_degree5_interfaces/observations.json)
  的 source_index=8，獨立核對原 disk rotation、全部 240 列（含 120 份
  T4 coloring）及十五份逐邊刪後 q-coloring。該圖的 separator 接 b1,b4，
  刪去它後兩個分量分居兩側，合計碰全部框點，且只缺 q。它說明不可省去
  H−x 連通；其 separator degree=5，**不是本輪雙 root 圖類的反例**。

任意大小同側結論由 §2 的 disk 弧分離證明承擔，有限位置表不驗證 Jordan
分離，也不是圖枚舉；新結果未 Lean 化。T4 被用為來源接受假設，不是外部
四色定理。前輪 (3) 排除的外部 degree-list 依賴仍留在前報告。

```bash
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_unattached_boundary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-28-adjacent-singleton-sectors.md)。

**下一窄入口：** 先取 x 接 {b0,b1}、H−x 在長弧側，保留原六邊形
框 Γ=(x,b1,b2,b3,b4,b0)、原 zw 及兩側 unary 完整關係。
q 下 T={2,3}；p₁、p₂ 的 x list 也都是 {2,3}，但其他原支援的列已變，
不能沿用 q 的私有色條件。需排除 target 的同色 singleton 或兩 E 都落在
{2,3} 的拒絕，並保留每側 (2)／(2,1) 及 root-spoke 的實際位置。
較大／多 mixed 分量、一般相鄰雙 root、degree≥6、共同出口及主命題仍未證。
