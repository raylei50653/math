---
docgraph:
  id: c5.single-sided-exit
  family:
    - c5
---
# 五目標排除到 single-sided exit：接合定理與一般化界線

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
**已完成唯一 degree-5 的全部 t≥1 及 t=0、(2,1,1,1) 核心之單側出口接合；一般單側出口仍未證。**
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
   boundary 鄰居，H−z 的接點分拆為 (2,1,1,1)。

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

第六類核心繼承 §2 的 induced-C5 disk、連通有效 H、T4 acceptance
及全部在 M 自己計算的 degrees。以 q=01012 對齊後，
[環狀支援定理](c5_no_spoke_supports.md) 使其落入兩種必要支援型，
四種二接點角色及三個具名單接點排列共 48 筆，全部接受兩個指定 p。
最後 12 個查詢用不同原分量的實際外部路徑套既有 degree-4 completion，
保留五個原接點及每份完整 relation，不在原圖任意添加 spoke。

因此 M 接受指定 p；再以來源雙缺失及刪邊繼承得 Σ(M)=Ω\{q}，
進入 §4。同樣不將只假設 T4 的指定雙列定理提升為任意來源的完整 Σ。

## 4. 從核心分離到實際第一個 strict step

按任意次序刪去 E\A。每個中間圖都包含 M，故始終拒絕 q；
原先接受的 Ω\{p,q} 始終可延拓。終點 M 接受 p，所以必有第一個接受
p 的中間圖。它的前一步仍恰拒絕 p、q，而該步只釋放 p。
這正是 [一般出口充要條件](c5_weak_critical_cores.md#2-三種出口的精確充要條件紙面證明)
的構造性充分方向，證畢。

注意刪除的是 E\A，不是先刪 A 中的 critical edge；後者會釋放 q，
無法用來證「只釋放 p」。也不需要刪到 M 的最後一條邊恰是 strict step。

## 5. 為何尚不是無條件的一般定理

一般 minimality 只給完整 degree≥4，沒有給 degree≤5、degree-5 點唯一，
或該點至少一條 boundary spoke。五目標窮盡的是 §2 的 sector 接合，
並不窮盡任意 minimal obstruction 的結構。

**失敗側的必要條件。** 若 Ω\{q}∉W(G)，則 G 的每一個 minimal
q-obstruction 都仍拒絕 p，**都必碰到全部五個 boundary 頂點**，
且每一個都至少符合下列一項：

- 有完整 degree≥6 的有效內點；
- 至少兩個完整 degree=5 的有效內點；
- 恰一個完整 degree=5 的有效內點，且 t=0，H−z 接點分拆為
  (2,2,1)，每個分量皆 K4-free。

證明：未接內點引理給出五點皆須被碰到；有效內點 degree≥4，
上述 degree 條件以外，(3,1)、(4) 由 §3c–3d 排除，其餘被 §1 第一、二、四、五、六類
覆蓋，與定理矛盾。
最後一類先落入 R10 的 t=0 六型，再由
[no-spoke 排除](c5_no_spoke_exterior.md) 消去 (5)、(4,1)、(3,2)、(3,1,1)。
多分量的非空真禁色集迫使每個分量碰 B，另一分量提供外部 z–B 路徑，
故 K4 及三／四接點 active triangle 都給 K5；單分量 (5) 的四份
palettes 則強迫接點數為偶數，這些來源排除不需 T4。§3e 再以 T4
及原分量外部雙路徑完成 (2,1,1,1) 指定分離，剩 (2,2,1) 未證。
五目標排除解決 t=3、(2)；§3a 完成 t=2 的 (3)、(2,1)；§3b 再完成
t=1 的 (2,1,1)、(2,2)；§3c–3d 排除 (3,1)、(4)，完成全部 t=1。

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
