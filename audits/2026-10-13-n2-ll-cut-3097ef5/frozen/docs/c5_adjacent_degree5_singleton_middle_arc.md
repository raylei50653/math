---
docgraph:
  id: c5.adjacent-degree5-singleton-middle-arc
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-singleton-long-arc
  requires:
    - c5.adjacent-degree5-shared-singleton
    - c5.single-spoke-two-two-external
  related:
    - c5.single-sided-exit
---
# 相鄰雙 degree-5：共鄰單點 12 長弧的指定雙列分離

後續（2026-09-28）：[34／40 長弧來源排除](c5_adjacent_degree5_singleton_end_arc.md)
已完成本頁下一窄題；各 152 筆必要配置以 K5／T4 排除 120／32，全部排除。
唯一 mixed 共鄰單點的全部支援已接回出口；下文保留 12 輪的證書及停止點。

2026-09-28。接續 [01／23 長弧](c5_adjacent_degree5_singleton_long_arc.md)。
**唯一 mixed 分量為原共鄰 singleton x，且 N_B(x)={b1,b2} 時，接受
T4 的 induced-C5 disk minimal q-core 必接受 p₁=01021、p₂=01212。**
這裡 q=01012，z、w 相鄰且完整 degree=5，其餘內點完整 degree=4。
來源大小不受限；下面保留同一來源的全部接點、實際支援及原三角形 xzw。

728 筆必要配置中，320 筆由原 x 路徑 K5 排除，112 筆違反 T4，保留
296 筆的 592 個 target 查詢全接受、0 未決。這是必要支援與完整禁色
集合的有限上界，並非 296 張來源圖，也不證每筆資料可實現。
結果擴充 [條件式單側出口](c5_single_sided_exit.md) 第七類；相鄰支援
34／40、較大／多 mixed 分量及一般出口仍保留，優先序見 [HANDOFF](HANDOFF.md)。

信任層為任意大小紙面化約、沿用外部 degree-list 定理、Python 固定域
證書。未新增 Lean theorem；不只由 T4 與兩列接受推完整 Σ。

## 1. 固定來源與 12 長弧的必要域

G 是有限簡單 disk 圖，B=(b0,…,b4) 是 induced 外圈；有效內部 H 非空
連通。G 拒絕 q，刪任一非框邊後接受 q，且接受全部四色 proper rows T4。
z、w 是恰兩個完整 degree-5 內點且 zw∈E(G)，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 分量是 {x}，N(x)={z,w,b1,b2}；其餘原分量
各只接一個 root。所有 degrees 都在同一 G 計算。

[同側定理](c5_adjacent_degree5_singleton_sectors.md) 使 H−x 位於
b2–b3–b4–b0–b1 的長弧側；短弧側與 T4 衝突。沿用
[共鄰單點化約](c5_adjacent_degree5_shared_singleton.md)，每側只有：

- (2)：二接點原分量 C_r，加原 root-spoke r–b_s；
- (2,1)：二接點原分量 C_r，加單接點原分量 D_r，沒有 root-spoke。

對任意列 β，令 F_C(β) 為該**整份原分量**所有可延拓接點 tuple 的
色集交集；等價地，它是令 root 取色後使 C 無法著色的 root 色集合。
接點未受 root 色限制時有 slack，故完整 tuple 關係非空，|F_C|≤接點數。
令 E_r(β) 為 root list 扣去該側全部 F；它在每列都非空。

q 下仍有 T=U∖{q₁,q₂}={2,3}。前輪 minimality 逐邊判準精確給
非空 E_z,E_w⊆T，且至少一側等於 T。每側必要禁色為

\[
\begin{array}{ll}
(2):&q_s\in\{0,1\},\quad F_{C_r}(q)=\{1-q_s\}\cup(T\setminus E_r);\\
(2,1):&F_{D_r}(q)=\{h\},\quad
F_{C_r}(q)=\{1-h\}\cup(T\setminus E_r),\quad h\in\{0,1\}.
\end{array} \tag{1}
\]

這不是把 01 的來源旋轉後仍固定 q：本輪 q 不變，全部具名支援在新長弧
重新生成，再以各支援上的 q 顏色檢查式 (1)。因此必要記錄數與前輪不同。

## 2. 任意大小來源仍受同一三角形次序與 K5 限制

[前報告 §2](c5_adjacent_degree5_singleton_long_arc.md#2-原三角形外側給固定長弧次序)
的 unary 支援引理不依賴 x 的具體框點編號。原 hub B∪{r,x} 仍連通且
避開 C，故拒絕的 C 仍是 K4-free。非空禁色容量≤2 排除空支援；若只有
一個外框色 a，色對稱迫使 F={a}，固定 root=a 後 tightness 使 deg_C≥3，
與 K4-free Gallai tree 的 leaf-block 非 cut 點 degree≤2 矛盾。
所以每份原 unary 支援至少兩點，且每個 f∈F_C(q) 滿足 |q(S_C)∪{f}|≥2。
沿用的 tightness 與 blockwise palettes 分別見
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)；
本輪核對原文，仍是外部定理。

每份 unary 都接 B，因此不能在原三角形 xzw 的有界內側。切開三角形
外側 annulus 的兩條原 x-spokes xb2、xb1，得到四個具名單位的線性
次序 O；兩 root 各佔一個區塊，每側 C_r 與 spoke／D_r 相鄰。原 C_r
兩個 contact 的兩種方向都保留。原分量 crosscut 不容其他單位附件交錯，
所以在 L=(2,3,4,0,1) 的提升座標中，所有來源都滿足

\[
\max\widehat S_{O_j}\le\min\widehat S_{O_{j+1}}. \tag{2}
\]

相同框點可被共用，但仍是同一頂點及同一色；支援可有間隙。此處套用
的是原嵌入的次序定理，沒有假定有限支援資料能反向構造 disk 圖。

若 F_C(q)=F 有兩色，原兩接點間的奇數長 bridge 路徑 P 及其全部
旁支塊 W_j 滿足 D(F)⊆q(N_B(W_j))，其中 D(F)=F（3∉F）或 U∖F
（3∈F）。若這兩色在 S_C 各只有唯一供應點 b_a、b_b，且 a,b 相鄰，
每個 W_j 都實際接到兩點。當 h∈{1,2}∖{a,b} 時，原 r–x–b_h
接到補弧；沿用前報告的五組

\[
W_j,\quad W_{j+1},\quad
Z=(V(J)\setminus\{v_j,v_{j+1}\})\cup\{x\}\cup(B\setminus\{b_a,b_b\}),
\quad\{b_a\},\quad\{b_b\}, \tag{3}
\]

其中 J=P 加兩條原 r-contact 邊。Z 由原 rx、xb_h 連通，五組互不相交，
原 P 邊、兩側 cycle 邊、四條 actual tethers 與三條框邊給十條鄰接。
所以式 (3) 是來源 K5 minor。不能把同色多供應點任選為唯一 tether，
也不能在 {a,b}={1,2} 時借用這條外部路徑；checker 保留兩項限制。
證明不限制 bridge 長度或旁支大小，亦不需要 T4。

## 3. p₂ 的 x 色表與完整接合

原三角形要求 z、w、x 互異。因此對任意 β，精確接合為

\[
\exists(a,b,c)\in E_z(\beta)\times E_w(\beta)
\times\bigl(U\setminus\{\beta_1,\beta_2\}\bigr),
\qquad |\{a,b,c\}|=3. \tag{4}
\]

固定這三色後，在各原分量選取所有接點避開其 root 色的**完整 tuple**，
即可著色同一 G。q 與 p₁ 的 x list 是 {2,3}，**p₂ 則是 {0,3}**。
target 不使用 q 的私有色條件。

若同一 σ∈S₄ 在某原分量的全部 actual support 上把 q 搬成 β，則其
完整 F_C(β)=σF_C(q)。否則保留所有容量≤原接點數、且在逐色固定
β(S_C) 的置換下不變的完整集合 F′，包含空集。實際 F 一定在其中；
不同分量及列的未知選擇可以過度放寬，但不得只選有利的選項。
每種完整選項都滿足式 (4) 才標為接受；每種都拒絕某 T4 列才排除來源。

例如必要 record 90（未主張可實現）有 zC 支援 234、z-spoke=2、
wC 支援 04、w-spoke=1，q 禁色分別為 {1}、{0}。在 p₂ 下，zC
的 F′ 可為 ∅、{1}、{2}、{1,2}、{0,3}，不能直接搬運 q。
整份 E_z 因而是 {0,1,3}、{0,3}、{1} 之一，E_w={2,3}。
前兩種有 (z,w,x)=(0,2,3)，最後一種有 (1,2,0)；全部合法。
最後的 x=0 特別使用 p₂ 的實際色表。

固定域核對如下；「幾何」尚未加入 q 禁色，所以兩欄不是同一計數單位。

| 每側分拆 | 幾何支援 | q 必要記錄 | K5 排除 | T4 排除 | 保留且雙列接受 |
| --- | ---: | ---: | ---: | ---: | ---: |
| (2) / (2) | 376 | 376 | 152 | 80 | 144 |
| (2) / (2,1) | 88 | 164 | 76 | 16 | 72 |
| (2,1) / (2) | 88 | 164 | 76 | 16 | 72 |
| (2,1) / (2,1) | 8 | 24 | 16 | 0 | 8 |
| 合計 | 560 | 728 | 320 | 112 | 296 |

K5 後的 408 筆逐筆檢查全部 120 個具名 T4 rows，若找到必拒絕列便
保存見證並停止該筆；排除 112 筆。保留項的兩個 target 各有 456 組
候選 E_z/E_w，每組皆有三色 witness；各有 40 筆含無法精確搬運的分量。
故 **296 筆的 592 查詢全部接受、0 未決**。保留項 q 下二接點 F 都為
singleton 是結果，並未拿來把 target 容量由二錯降為一。

## 4. 自反射核對與條件式出口

ρ(i)=3−i mod 5、π=(0 1) 保持 q 及 x 支援 {1,2}，將整條長弧反向。
對每筆資料一併搬運 supports、F、四個單位次序與全部 contact 方向。
原 target 搬為 Tp₁=21010、Tp₂=02012；後者的 x list 是 {1,3}，
正是 π({0,3})。checker 對每筆保留項驗證搬運後的全部 E 選項和接合，
並找到同一必要表中的反射 record；沒有只正規化 target 而固定來源。
這是 12 分支內的核對，沒有額外解決 34／40。

若 M 是來源 Σ(G)=Ω∖{p,q} 的 minimal q-core，刪邊繼承使
Σ(M)⊇Ω∖{p,q}。整體對齊 q=01012 後，原相鄰 singleton 缺失 p
恰為 p₁ 或 p₂。本報告的 12 核心接受 p，故 **Σ(M)=Ω∖{q}**，
接上既有 silent deletions 後第一次釋放 p 的序列。
因此出口第七類從 01／23 擴成 01／12／23；這一步明用雙缺失來源。

## 5. 證書、重播與停止點

[checker](../scripts/c5_adjacent_degree5_singleton_middle_arc.py)、
[JSON](../artifacts/c5_adjacent_degree5_singleton_middle_arc/observations.json) 與
[728 筆表](../artifacts/c5_adjacent_degree5_singleton_middle_arc/support_table.md)
保存原具名支援、q 禁色、前輪抽象 record index、四種 contact 方向、
排除理由，以及 target 的完整候選 F、E 與三色 witness。source 與直接
輸入均以 SHA256 綁定；前輪 artifacts 保持不變。

幾何域由遞增支援生成與獨立 Cartesian hull 分離兩法核對。另驗 root
交換、整張來源反射，以及 108 份 12 位置原 x 路徑 K5 skeleton；包含
長度 1／3／5 的每個 bridge cut、直接／共幹 tethers，刪原 rx 使指定
witness 失效。skeletons 不代表 degree/list 來源，刪 rx 也不保證全圖平面。
兩個抽象負控制證把 p₂ 的 x list 錯用成 q 的 {2,3} 可同時造成假接受
與假拒絕；它們不是來源反例。完整關係不能換成 marginals 的控制沿用前輪。

```bash
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

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-28-adjacent-singleton-middle-arc.md)。
下一入口是 x 接 {b3,b4}：長弧 L=(4,0,1,2,3)，q、p₁、p₂ 的 x list
皆為 {0,3}，q 的 T 外色改為 {1,2}，須重算禁色與全部具名支援。
完成後才以共同來源反射搬至 40。較大／多 mixed 分量、一般雙 root、
degree≥6、一般單側／共同出口與 K∞=K≤5 仍未證；本輪未 Lean 化。
