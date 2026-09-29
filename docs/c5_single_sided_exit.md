---
docgraph:
  id: c5.single-sided-exit
  family:
    - c5
---
# 五目標排除到 single-sided exit：接合定理與一般化界線

後續（2026-09-29）：[整條原 bridge 路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)
完成無 mixed 兩側 t=2,(2) 的指定雙列分離：322 份必要資料的 644 個查詢
全證，不需 T4。新增第九類可處理核心；完整 Σ 仍明用來源雙缺失與刪邊繼承。

後續（2026-09-29）：[原 K4 與實際外部路徑](c5_adjacent_degree5_mixed_edge_k4.md)
完成唯一 mixed K2 的最後四 incidence 型，一般平面來源排除、不需 T4。
九組具名接線均已處理，出口第八類移除 root incidence 限制；一般出口仍未證。

後續（2026-09-29）：[t_w=0、(1,1,1) 六跨度排除](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)
已逐筆排除原 108 筆：四份 unary、v 的總跨度至少 6>5，不需 T4，0 target 查詢。
zu、zv、wu 共鄰端點接線的全部五型已完成，出口第八類移除 w 分拆限制。
原資料保持；下列通知與正文保留各輪語境，現行入口見 [HANDOFF](HANDOFF.md)。

後續（2026-09-29）：[t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) 完成 102 筆的 204 查詢全接受，
另以原路徑 K5 排除 94、保留 8，不需 T4。第八類擴至 w 無 spoke、unary 分拆 (2,1)；
此接線只剩 t_w=0、(1,1,1)。完整 Σ 仍明用來源雙缺失與刪邊繼承。

後續（2026-09-29）：[共鄰端點 K2 的 t_w=1、(1,1)](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md)
由同序支援與五邊飽和完成 32 筆／64 查詢，不需 T4；第八類已涵蓋此接線
的全部 t_w≥1。完整 Σ 仍明用來源雙缺失與刪邊繼承，t_w=0 兩型保留。

後續（2026-09-28）：[共鄰端點 K2 的 t_w=1、(2)](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md)
完成局部 K5 搬運與指定雙列分離：356 筆必要支援排除 292，保留 64 的
128 查詢全接受，不需 T4。第八類擴至此型；完整 Σ 仍另用來源雙缺失與
刪邊繼承，其餘三種 w 分拆與一般出口保留。下列通知保留各輪語境。

後續（2026-09-28）：[共鄰端點 K2 的 w 側兩條 spoke](c5_adjacent_degree5_mixed_edge_shared_t2.md)
完成任意大小指定雙列分離，不需 T4；38 筆必要支援的 76 個查詢全接受。
§1 新增第八類，§2 接合來源雙缺失與刪邊繼承；其餘 w 分拆與一般出口仍保留。

後續（2026-09-28）：[唯一 mixed K2 的原四環次序](c5_adjacent_degree5_mixed_edge_order.md)
已排除兩 root 各一接點的全部 disk minimal q-core，不需 T4。§5 的
失敗核心限制已加入此結果；當輪七類條件式出口保持原範圍，現況以上段為準。

後續（2026-09-28）：[34／40 長弧來源排除](c5_adjacent_degree5_singleton_end_arc.md)
完成唯一 mixed 共鄰單點的全部支援；§1 第七類已移除 x 支援限制。
01／12／23 指定雙列分離及非相鄰支援結果一併接合；較大／多 mixed
分量及一般雙 root 仍保留，未新增 Lean theorem。

後續（2026-09-28）：[no-spoke 首橋與固定框弧](c5_no_spoke_first_bridge.md)
完成 (2,2,1) 剩餘 12 個指定列，116 筆保留配置全接受雙列，來源排除仍為
500 筆。§1 第六類擴至全部 t=0，新增 §3f；唯一 degree-5 全部分支
接回條件式出口。失敗側只剩 degree≥6 或至少兩個 degree-5；未 Lean 化。
下列較早後續通知保留各輪數字，現況以本通知及定理正文為準。

後續（2026-09-28）：[(2,2,1) 原外部路徑 K5](c5_no_spoke_path_minor.md)
排除含 record 599 的 500 筆來源；剩 116 筆中 108 筆雙列已證、12 查詢
未決。尚未完成該分拆，故本頁條件式出口的六類範圍不擴大，未 Lean 化。

後續（2026-09-28）：[no-spoke 環狀支援與指定分離](c5_no_spoke_supports.md)
完成 (2,1,1,1) 的 48 筆必要配置雙列延拓；新增 §1 第六類與 §3e，
失敗側唯一 degree-5 只剩 t=0 的 (2,2,1)。一般定理仍未證，未 Lean 化。

後續（2026-09-28）：[t=0 外部連通與四型排除](c5_no_spoke_exterior.md)
以另一原分量的 z–B 路徑恢復 K4／triangle 的外部 hub；(5) 另由四列
palettes 的偶數接點障礙排除。失敗側唯一 degree-5 只剩 t=0 的
(2,2,1)、(2,1,1,1)，各分量 K4-free；尚未新增這兩型的 p 分離。

後續（2026-09-28）：[single-spoke (4) 排除](c5_single_spoke_four.md)
由三份 palettes 的共同係數迫使兩 triangle 加單 bridge，再以原 tethers
給 K5。t=1 四型全部接合，§1 第五類已刪去分拆限制；失敗側唯一
degree-5 只剩 t=0 六型，一般定理仍未證。

後續（2026-09-28）：[single-spoke (3,1) 排除](c5_single_spoke_three_one.md)
以三接點 active triangle、實際 tethers 及唯一 spoke 得 K5，不需 T4。
該輪留下 t=0 六型及 t=1 的 (4)，後者已由上述後續排除。

後續（2026-09-28）：[局部 residual 與 (2,2) 完成](c5_single_spoke_residual_locality.md)
關閉最後 record 90／282 的 p₂。連同既已完成的 (2,1,1)，新增 single-spoke
兩類可處理核心；該輪保留 (3,1)、(4)，前者已由上述後續排除。

後續（2026-09-27）：[非相鄰 two-spoke 分離](c5_two_spoke_nonadjacent.md)
完成唯一 degree-5 的全部 t=2 分支；本頁定理及失敗側必要條件已相應更新。

後續（2026-09-24）：[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md)
將 t=2 的 (3)／(2,1) 收窄為 24 個必要配置；
[未接內點引理](c5_unattached_boundary.md) 再完成 (3) 非相鄰型的分離，
並將下述定理擴至有未接內點 boundary 頂點的核心，內點 degree 不受限。

2026-09-24。接續 [五目標](c5_sector_targets.md)、
[雙拒絕分類](c5_two_rejection_proof_zh.md) 與
[3703 排除](c5_sector_3703_exclusion.md)。
**已完成唯一 degree-5 全部核心的單側出口接合；一般單側出口仍未證。**
下文給出任意大小來源圖的條件式定理、五目標窮盡性的紙面推導，以及
尚不能消去的核心存在性假設。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 定義與定理

令 G 是有限簡單 C5 disk 圖，外圈 B 的次序固定；Ω 是十個色置換等價類
的 proper 四色 boundary patterns。p、q 為三色 patterns，其 singleton
位置在 B 上相鄰，且 Σ(G)=Ω\{p,q}。令 E 為全部非外圈邊。
對 A⊆E，以 G[A] 表示保留全部頂點、外圈及 A 的圖；忽略孤立內點時稱其
餘下內點為有效內點。所有以下 degrees 都在 **G[A] 自己**計算。

稱一個 minimal q-obstruction A 為本文的可處理核心，如果它滿足以下任一項：

1. 全部有效內點完整 degree=4；
2. 恰一個有效內點 z 完整 degree=5，其餘完整 degree=4，且 z 恰有
   三個 boundary 鄰居；
3. 某個 boundary 頂點沒有有效內鄰點（內點 degree 不受限）；
4. 恰一個有效內點 z 完整 degree=5，其餘完整 degree=4，且 z 恰有
   兩個 boundary 鄰居；
5. 恰一個有效內點 z 完整 degree=5，其餘完整 degree=4，z 恰有一個
   boundary 鄰居，不限制 H−z 的接點分拆；
6. 恰一個有效內點 z 完整 degree=5，其餘完整 degree=4，z 沒有
   boundary 鄰居，不限制 H−z 的接點分拆；
7. 恰兩個有效內點 z、w 完整 degree=5 且相鄰，其餘完整 degree=4；
   H−{z,w} 的唯一 mixed 分量是共鄰 singleton {x}，不限制其 boundary 支援；
8. 恰兩個有效內點 z、w 完整 degree=5 且相鄰，其餘完整 degree=4；
   H−{z,w} 的唯一 mixed 原分量為 K2={u,v}，不限制 root incidence
   接線、boundary spoke 數或 unary 接點分拆；
9. 恰兩個有效內點 z、w 完整 degree=5 且相鄰，其餘完整 degree=4；
   H−{z,w} 無 mixed，z、w 各有兩個 boundary 鄰居。

minimality 使同一內點的 q-spokes 異色，q 只用三色，故唯一 degree-5
的 t≤3。第二、四、五、六類因此涵蓋全部唯一 degree-5 核心。

**定理（條件式 single-sided exit，來源圖大小與 degree 不受限）。**
若 G 有一個上述可處理的 minimal q-obstruction，則存在非外圈邊刪除序列

```
G = G₀ → G₁ → ⋯ → Gⱼ → Gⱼ₊₁
Σ(Gᵢ)=Ω\{p,q}  (0≤i≤j)，    Σ(Gⱼ₊₁)=Ω\{q}。
```

因此 Ω\{q}∈W(G)：先 silent deletions，再以一條邊只釋放 p。
交換 p、q 得另一方向；若兩側各有一個可處理核心，就有兩個單側出口。
兩個核心不必相同，亦不要求唯一阻礙。結論不含共同出口。

## 2. 核心繼承的條件與三-spoke 區域

選定 minimal q-obstruction A，記 M=G[A]。刪邊保留 disk embedding，
且 Σ(G)⊆Σ(M)。因此若 M 仍拒絕 p，就必有 **Σ(M)=Ω\{p,q}**。
這個等式是五目標 screen 的必要輸入，不能只用「接受全部 T4」取代。
來源接受全部 T4，故沒有 boundary chord；M 同樣沒有。

由 [minimal-core 基礎](c5_weak_list_cores.md#1-精確的-list-coloring-翻譯)，
M 的有效內點誘導圖 H 非空連通、每點完整 degree≥4，且每點的
boundary spokes 在 q 下顏色互異。第一種核心由
[全 degree-4 定理](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
已有 Σ(M)=Ω\{q}；第三種由
[未接內點引理](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)
同樣得到 Σ(M)=Ω\{q}。第二種由下文 §2–3 處理，第四種見 §3a。

第七種先將整張來源與 q 共同對齊為 q=01012。
[同側限制](c5_adjacent_degree5_singleton_sectors.md) 排除不合 T4／minimality
的位置，非相鄰 03 唯一保留側因 b4 未接而只缺 q；
[34／40 排除](c5_adjacent_degree5_singleton_end_arc.md#4-整張來源反射與全部-singleton-出口)
再排除最後兩個相鄰支援。其餘由 [01／23](c5_adjacent_degree5_singleton_long_arc.md#5-全來源反射與出口接合)
及 [12 分離](c5_adjacent_degree5_singleton_middle_arc.md#4-自反射核對與條件式出口)
接受 p₁=01021、p₂=01212；對齊後的缺失 p 必為其中一列。來源雙缺失與
刪邊繼承遂給 Σ(M)=Ω\{q}，再用下文 §4 的刪邊序列；不由兩列接受單獨推完整 Σ。

第八種先用 [K2 全部接線覆蓋](c5_adjacent_degree5_mixed_edge_k4.md#4-唯一-mixed-原-k2-的接線覆蓋與出口)：
九組具名接線經整張來源重新命名分成四型；各一接點異端型、同端點型
及四 incidence 型皆已作來源排除。因此可存在的 disk 來源必可整圖
重新命名成 zu、zv、wu 型；這保持 boundary、顏色、全部原分量與附件。
再共同對齊 q=01012，保持共鄰 u、原 chord zu 與全部附件。
[共鄰端點化約](c5_adjacent_degree5_mixed_edge_shared.md) 已排除 w 側 (3)，
[無 spoke／(1,1,1) 六跨度排除](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)
再排除最後一型；實際來源只可能落在下列四種分拆。
[兩條 spoke 分離](c5_adjacent_degree5_mixed_edge_shared_t2.md#5-反射出口接合與停止點)、
[單 spoke／二接點分離](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md#6-反射證書與出口接合)、
[單 spoke／兩個單接點分離](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md#5-出口接合證書與停止點)
及 [無 spoke／(2,1) 分離](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md#6-出口接合重播與停止點)
各自不需 T4 就接受 p₁、p₂，故接受對齊後的 p。來源雙缺失與刪邊繼承再給
Σ(M)=Ω\{q}，可用同一 §4 序列；不要求必要支援表的每筆資料可實現。

第九種由 [無 mixed 化約](c5_adjacent_degree5_no_mixed.md) 得每側恰有唯一
二接點 unary，F_C(q) 是 singleton。共同對齊 q=01012 後，
[支援／環序必要覆蓋](c5_adjacent_degree5_no_mixed_t2.md) 落在原 322 份之一；
[整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) 完成
全部 p₁、p₂ 分離，故 M 接受對齊後的 p。再由來源雙缺失與刪邊繼承得
Σ(M)=Ω\{q}，進入 §4；必要表可實現性與任意來源完整 Σ 均未另行假設。

將 q 對齊為 01012，稱其三色 A、B、C，第四色 D。
z 有三條 spokes，顏色互異，故 A_z(q)={D}；它還有恰兩個內鄰點。
H−z 的每個連通分量都接 z。由
[不可刪減覆蓋](c5_degree5_interfaces.md#4-minimality-的充要條件與接點限制)，
分量數 r≤(5−3)−1=1。因此 H−z 恰為一個非空連通 C，接 z 的兩點不同，
且 **F_C(q)={D}**。這裡用到 minimality，而非由 degree 序列單獨推出。

沿用 [三-spoke 區域化約](c5_degree5_sectors.md#1-三條-spokes-將連通分量限制在同一區域)：
同一嵌入中 C 全在一個 spoke 區域；缺色交換和未碰頂點改色排除十個位置。
兩個剩餘位置互為鏡像，故可取

```
N_B(z)={b0,b1,b4}，   Γ=(z,b1,b2,b3,b4)，   K=M[C∪Γ]。
```

反射及全域色置換同時搬運 p、q 及所有接點，保持 singleton 相鄰性。
K 的 Γ 是 induced C5 disk 外框，C 非空連通；每個 C 點仍完整 degree=4，
因其全部鄰居都在此區域閉包。框點 z 恰有兩個不同內鄰點。
所以兩份 sector 排除定理的**全部圖層假設**在此成立。
原來的 b0 不鄰接 C，M 恰由 K 加 b0 及 b0b1、b0b4、b0z 三邊而成。

## 3. 五目標在此支的紙面窮盡性

令 xᵢ 是 K 刪去 zb1、zb4 後，第 i 個開口列是否可延拓的 0/1 值；
列序沿用 [十二列定義](c5_sector_targets.md#1-查詢域與五個目標)。
令 yᵢ 是 M 的第 i 個 proper-C5 列是否接受。直接在同一色框量化 z 色得

```
(y0,…,y9) = (x7, x3∨x8, x5, x1∨x8, x9,
              x2, x6, x0, x1∨x3, x4)。
```

這是任意來源圖的精確接合式：對 boundary row b，允許的 z 色恰為
U\{b0,b1,b4}，並測試 (z,b1,b2,b3,b4) 能否延拓 K。
不是把不同列的 colorings 拼在一起。
F_C(q)={D} 又給出

```
x0=x10=x11=1，x7=0。
```

q 是第 0 列。其相鄰 singleton 缺失 p 只可能是第 1 或第 6 列。
假設 M 仍拒絕 p；§2 已證 y 恰缺這兩列。

| p | 接合式強迫的其餘條件 | 所有可能的 x mask |
| --- | --- | --- |
| 第 1 列 01021 | x3=x8=0；x1=x2=x4=x5=x6=x9=1 | 3703 |
| 第 6 列 01212 | x6=0；x2=x4=x5=x9=1；x1、x3、x8 至少兩個為 1 | 3647、3895、3901、3903 |

第二列的三個 OR 都必為 1，等價於三位至少兩個為 1，因此恰四種。
十九個開口列中其餘七列不參與任何一個 y 或 F_C(q) 查詢，沒有遺漏
對此接合有影響的自由度。此推導獨立於 |C|、block 數及任何圖枚舉。

四個 masks 都拒絕 x6、x7，雙拒絕分類強迫完整 mask=1855，矛盾；
3703 拒絕 x3、x7、x8，由任意長度三拒絕排除得矛盾。
所以 M 接受 p，從而 **Σ(M)=Ω\{q}**。這完成三-spoke 核心的分離。

## 3a. 全部 two-spoke 核心接回同一出口

對第四種核心，以 q=01012 對齊後，指定相鄰 singleton p 只有
01021、01212。M 的 minimality 與 T4 acceptance 給出
[兩-spoke 必要位置表](c5_degree5_two_spoke_sectors.md) 的 24 個配置。
全部六個 (3) 型由 [三接點定理](c5_two_spoke_three_contacts.md) 排除。
(2,1) 的六個相鄰表項由 [相鄰](c5_two_spoke_adjacent_21.md)、
[中間相鄰](c5_two_spoke_middle_21.md) 及 [反射](c5_two_spoke_reflection.md)
排除；另四個相鄰表項由 [split-support](c5_two_spoke_split_support.md)
證只缺 q。剩八個非相鄰表項由
[指定列分離](c5_two_spoke_nonadjacent.md) 證兩個 p 均可延拓。

因此任一實際存在的第四種核心 M 都接受指定 p。再用
Σ(G)⊆Σ(M) 與 M 拒絕 q，得到 **Σ(M)=Ω\{q}**，可直接進入 §4。
這個完整 Σ 結論使用來源雙缺失前提；新非相鄰定理自身只斷言兩個指定 p
延拓，未把所有 T4-accepting 非相鄰來源分類成單缺失。反射側僅搬運，
且搬運同時交換兩個 p 的色置換等價類，不獨立枚舉。

## 3b. Single-spoke (2,1,1) 與 (2,2) 核心

對第五種核心，§2 同樣給 induced-C5 disk、有效 H 連通、T4 acceptance
及 q 下異色 spokes，符合 [single-spoke 必要覆蓋](c5_single_spoke_cores.md)。
將 q 對齊為 01012 後，相鄰 singleton 的指定 p 恰為 p₁=01021 或 p₂=01212。
接點均為原不同內鄰點，degree 與全部 boundary 附件在核心 M 自己計算。

(2,1,1) 的任意大小來源落入 114 筆必要表，兩列已由
[單接點上界分類及前序結果](c5_single_spoke_single_contact_bounds.md) 全證。
(2,2) 的任意大小來源落入原 T4 保留 380 筆，其中 278 筆已由來源 K5
排除，剩 102 筆的兩列由 [residual 局部性及前序結果](c5_single_spoke_residual_locality.md)
全證。反射同時搬運原關係、接點、boundary 與字面 target 色列；不更換來源。

故第五種核心在這兩種分拆下接受指定 p；其餘分拆由 §3c–3d 排除。
再用來源的 Σ(G)=Ω\{p,q}、刪邊繼承及 M 拒絕 q，
才得到 **Σ(M)=Ω\{q}**，適用 §4。單獨的 T4-accepting 核心指定雙列定理
不表示其完整 Σ 已分類，也不證必要表各型可以實現。

## 3c. Single-spoke (3,1) 不存在

[三接點定理](c5_single_spoke_three_one.md) 使用同一 minimal q-core 的
F₃(q)=A\{c}、F₁(q)={c}。兩份拒絕 palettes 強迫一個 triangle 加三條
同 parity bridge arms；triangle 三點各有原 boundary tether，連同唯一
spoke 得 K5。另一原分量及四個原接點全保留；不需 T4 或 p 拒絕。

因此 (3,1) 不可能出現在任一這類 minimal core。這是來源排除，沒有
新增可實現核心、target 計數或完整 Σ 分類。

## 3d. Single-spoke (4) 不存在與全部 t=1 接合

[四接點三拒絕定理](c5_single_spoke_four.md) 使用 F_C(q)=U\{q_s}。
同一 block incidence matrix 的欄獨立性使三組 palette 差共用 τ；
正係數 block 不能是 bridge，四葉共同樹因而恰為兩 triangle 加單 bridge。
把右 triangle 與 z 合為 Z，左 triangle 三點各有原 boundary tether，
連同唯一 spoke 得 K5。此來源排除不需 T4 或第二列拒絕。

由必要覆蓋，t=1 只有 (4)、(3,1)、(2,2)、(2,1,1) 四型；前兩型不存在，
後兩型由 §3b 接受指定 p。因此 §1 第五類可不附接點分拆限制，任意大小
實際核心皆有 Σ(M)=Ω\{q}。此處的完整 Σ 使用原出口來源的雙缺失前提，
不是將任意 T4 核心的完整關係或可實現性全部分類。

## 3e. No-spoke (2,1,1,1) 核心

第六類中 (2,1,1,1) 核心繼承 §2 的 induced-C5 disk、連通有效 H、T4 acceptance
及全部在 M 自己計算的 degrees。以 q=01012 對齊後，
[環狀支援定理](c5_no_spoke_supports.md) 使其落入兩種必要支援型，
四種二接點角色及三個具名單接點排列共 48 筆，全部接受兩個指定 p。
最後 12 個查詢用不同原分量的實際外部路徑套既有 degree-4 completion，
保留五個原接點及每份完整 relation，不在原圖任意添加 spoke。

因此 M 接受指定 p；再以來源雙缺失及刪邊繼承得 Σ(M)=Ω\{q}，
進入 §4。同樣不將只假設 T4 的指定雙列定理提升為任意來源的完整 Σ。

## 3f. No-spoke (2,2,1) 與唯一 degree-5 完成

[首橋與固定框弧定理](c5_no_spoke_first_bridge.md) 完成 t=0、(2,2,1)：
環狀必要支援表的 616 筆 T4 保留配置中，500 筆由原外部路徑 K5 排除，
其餘 116 筆全部接受 p₁=01021、p₂=01212。首橋共用 β 關閉四個查詢，
同一份三框弧與原外部路徑再關閉八個，保留全部五接點及完整關係。
固定 q 後，相鄰 singleton 的兩個指定 p 正是此兩列；反射與色框搬運
仍在同一來源圖上進行。

[No-spoke 外部連通](c5_no_spoke_exterior.md) 已排除 t=0 其餘四型；
§3e、§3f 分離最後兩型，故第六類不再要求接點分拆。M 接受指定 p，
來源雙缺失及刪邊繼承才給 Σ(M)=Ω\{q}，接上 §4。這不分類任意
T4 核心的完整 Σ，也不宣稱必要支援配置可實現。

## 4. 從核心分離到實際第一個 strict step

按任意次序刪去 E\A。每個中間圖都包含 M，故始終拒絕 q；
原先接受的 Ω\{p,q} 始終可延拓。終點 M 接受 p，所以必有第一個接受
p 的中間圖。它的前一步仍恰拒絕 p、q，而該步只釋放 p。
這正是 [一般出口充要條件](c5_weak_critical_cores.md#2-三種出口的精確充要條件紙面證明)
的構造性充分方向，證畢。

注意刪除的是 E\A，不是先刪 A 中的 critical edge；後者會釋放 q，
無法用來證「只釋放 p」。也不需要刪到 M 的最後一條邊恰是 strict step。

## 5. 為何尚不是無條件的一般定理

一般 minimality 只給完整 degree≥4，沒有給 degree≤5 或 degree-5 點唯一。
五目標窮盡的是 §2 的 sector 接合，
並不窮盡任意 minimal obstruction 的結構。

**失敗側的必要條件。** 若 Ω\{q}∉W(G)，則 G 的每一個 minimal
q-obstruction 都仍拒絕 p，**都必碰到全部五個 boundary 頂點**，
且每一個都至少符合下列一項：

- 有完整 degree≥6 的有效內點；
- 至少兩個完整 degree=5 的有效內點。

證明：未接內點引理給出五點皆須被碰到；有效內點 degree≥4，
上述 degree 條件以外，只可能全 degree-4 或唯一 degree-5，其餘 degree-4，
均被 §1 第一、二、四、五、六類覆蓋，與定理矛盾。
五目標排除解決 t=3、(2)；§3a 完成 t=2 的 (3)、(2,1)；§3b 再完成
t=1 的 (2,1,1)、(2,2)；§3c–3d 排除 (3,1)、(4)，完成全部 t=1；
no-spoke 四型排除加 §3e–3f 完成全部 t=0。
若恰有相鄰的兩個 degree-5 點，失敗側核心亦不能屬第七類唯一 mixed
singleton 子類，無論 x 的 boundary 支援；亦不能以原 uv 為唯一 mixed
分量且 root incidence 恰為 zu、wv。[原四環次序排除](c5_adjacent_degree5_mixed_edge_order.md)
先用支援跨度排除 552／576 筆必要資料，再以飽和環序排除剩餘 24 筆，
證明後一接線型的 disk minimal q-core 不存在，不需 T4。這是來源排除，
不須新增空的核心類別。[K2 共鄰端點型](c5_adjacent_degree5_mixed_edge_shared.md)
P*ᶻ={u,v}、P*ʷ={u} 另已迫使 z 無 spoke、唯一二接點 unary、w 容量飽和；
原 288 筆是必要關係資料；其中 [w 側 t=2、(1)](c5_adjacent_degree5_mixed_edge_shared_t2.md)、
[t=1、(2)](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md)、
[t=1、(1,1)](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md) 與
[t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) 已由支援／環序、
適用的來源 K5 與完整禁色上界證雙列，故失敗側核心亦不能屬第八類。
[t_w=0、(1,1,1)](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md) 再以 6>5
的跨度矛盾排除全部 108 筆，故此接線全部五型已完成；必要表仍未證
可實現性。[同端點 K2](c5_adjacent_degree5_mixed_edge_same_endpoint.md) 再排除
P*ᶻ=P*ʷ={u}：240 筆正常形中 105 筆由原 r–u–B 的 K5 排除，135 筆
平面必要資料再以跨度排除 123、五邊飽和及原 v-star 排除 12。此型的
disk minimal q-core 不存在，不需 T4、沒有 target 查詢，不新增空的
出口類別。[四 incidence 原 K4](c5_adjacent_degree5_mixed_edge_k4.md) 再由
原 unary 完整改色證明實際外部路徑存在，將 P*ᶻ=P*ʷ={u,v} 作一般
平面來源排除；本步不需 T4、degree-list 定理或 disk 次序。唯一 mixed
K2 的全部接線均已處理，第八類移除接線限制；失敗側核心不能有唯一
mixed K2。[無 mixed 化約](c5_adjacent_degree5_no_mixed.md) 另已證兩側
E_z(q)=E_w(q)={c}、容量缺額加重疊恰一及逐邊 minimality；原 zw
外部路徑使平面來源每側只剩 t=2:(2)、t=1:(2,1)、t=0:(2,2)／(2,1,1)。
[兩側 t=2 的支援與環序](c5_adjacent_degree5_no_mixed_t2.md) 再給 322 份
必要資料；[原 bridge 與框弧](c5_adjacent_degree5_no_mixed_t2_bridge.md) 新增
68 個延拓後，[原雙端點](c5_adjacent_degree5_no_mixed_t2_endpoints.md) 再新增 60 個，
[整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) 關閉最後 4 項。
原 322 份全保留、644／644 個 target 全證，新增第九類；失敗側核心不能
是無 mixed 且兩側 t=2。其他無 mixed 分拆、較大／多 mixed 與一般雙 root 仍保留。

要完成使用者要求的**無條件一般 single-sided exit 定理**，仍須證明
每個候選 A 來源 G、每個定向缺失對 (p,q)，至少存在一個接受 p 的
minimal q-obstruction。證明存在一個 §1 可處理核心是充分途徑，但不是
已知必要條件；也可以直接處理上述剩餘類型，證其分離。
不能為取得 degree 界任意縮圖，因縮圖可能失去 p 的延拓性或來源刪邊關係。

因此本輪完成局部排除到條件式出口的全部橋接，並將一般問題收窄至上述
核心存在／分離缺口；沒有聲稱一般定理被反駁。共同 pivotal edge、候選 A
全部三出口及 K∞=K≤5 仍各需額外證明。

## 6. 證據層與重播

原接合輪新增紙面接合、五目標 Boolean 窮盡推導與失敗側必要條件。
sector 圖層排除沿用既有紙面證明、外部 degree-list 定理及 Python 局部
證書；沒有新增 Lean theorem。既有 checker 另核對 4,096 個投影、
五目標的全部 240 個有標號 boundary rows，與 §3 相符。

```bash
uv run --with networkx==3.5 python scripts/c5_sector_targets.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
uv run python scripts/c5_sector_3703_exclusion.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證與沿用範圍見 [本輪紀錄](history/2026-09-24-single-sided-exit.md)。
未改抽象 603 profiles 或固定點；提交與發布核對見同一紀錄。

2026-09-27 的 t=2 擴充另有任意大小紙面化約、74／3,492 個局部候選證書，
以及 Lean 有限列代數與反射證明；圖層定理未 Lean 化。
實際重播見 [本輪紀錄](history/2026-09-27-nonadjacent-two-spoke.md)。

2026-09-28 的 §3b 是指定雙列分離到同一刪邊出口的紙面接合；未新增 Lean
theorem。新 (2,2) 證書及沿用的 (2,1,1) 檢查範圍見
[residual 局部性紀錄](history/2026-09-28-residual-locality.md)。

2026-09-28 的 §3c 以任意大小紙面三接點排除縮小失敗側；外部 degree-list
及 one-spoke K5 的有限控制見 [三接點紀錄](history/2026-09-28-three-one.md)，未 Lean 化。

2026-09-28 的 §3d 是三拒絕共同結構、實際 tethers 與 K5 的任意大小紙面
證明；960 份 minor 控制及實際重播見 [四接點紀錄](history/2026-09-28-four-contact.md)。
未新增 Lean theorem，也未新增 t=0 結論。

2026-09-28 的 §3e 以 no-spoke 環狀實際支援、原分量外部雙路徑及既有
completion 完成 (2,1,1,1) 指定分離。48 筆及實際驗證見
[no-spoke 支援紀錄](history/2026-09-28-no-spoke-supports.md)；未 Lean 化。

2026-09-28 的 §3f 用首橋共用 palette 與固定三框弧完成 (2,2,1)，
接回全部唯一 degree-5 核心；12 個新延拓、1,536 份 minor 與實際重播見
[首橋／框弧紀錄](history/2026-09-28-no-spoke-first-bridge.md)。證據為任意
大小紙面＋外部 degree-list＋Python，未新增 Lean theorem。

2026-09-28 的第七類使用原三角形外側次序、原 x 路徑 K5 與完整禁色
集合的接合上界；01／23、12 各自保留 296 筆必要配置、592 查詢全接受。
實際驗證見 [01／23 紀錄](history/2026-09-28-adjacent-singleton-long-arc.md)
與 [12 紀錄](history/2026-09-28-adjacent-singleton-middle-arc.md)；未 Lean 化。

同日 [34／40 排除](c5_adjacent_degree5_singleton_end_arc.md) 將第七類擴至
全部 x 支援：兩位置各 152 筆，K5／T4 各排除 120／32，無保留來源。
任意大小化約與原圖 minor 仍為紙面＋外部定理，有限重播見
[本輪紀錄](history/2026-09-28-adjacent-singleton-end-arc.md)；未 Lean 化。

同日第八類新增原 diamond 外側的支援化約與完整禁色集合上界接合；
38 筆、76 個指定查詢及實際驗證見
[兩條 spoke 紀錄](history/2026-09-28-adjacent-mixed-edge-shared-t2.md)。不需 T4，未 Lean 化。

同日第八類再接入 t_w=1、(2)：兩段任意大小局部化、356→292＋64 的
原 ID 綁定與全部 128 指定查詢，見 [單 spoke／二接點紀錄](history/2026-09-28-adjacent-mixed-edge-shared-t1-pair.md)。
紙面＋外部 degree-list 定理＋Python，不需 T4，未新增 Lean theorem。

2026-09-29 第八類接入 t_w=1、(1,1)，完成此接線的 t_w≥1。三份 unary
支援下界與原 diamond 外側同序給五邊飽和，原 72 筆接合成 32 筆必要
資料，64 查詢全接受，見 [兩個單接點紀錄](history/2026-09-29-adjacent-mixed-edge-shared-t1-singles.md)。
不需 T4 或新來源 minor，紙面＋外部定理＋Python，未 Lean 化。

同日第八類再接入 t_w=0、(2,1)：原 diamond／u、v 附件給 94 筆來源 K5，
保留 8 筆的 16 target 以完整關係精確搬運接受，見
[無 spoke／(2,1) 紀錄](history/2026-09-29-adjacent-mixed-edge-shared-t0-pair-single.md)。
紙面＋外部定理＋Python，不需 T4，未 Lean 化。
