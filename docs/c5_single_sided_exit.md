# 五目標排除到 single-sided exit：接合定理與一般化界線

後續（2026-09-24）：[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md)
將 t=2 的 (3)／(2,1) 收窄為 24 個必要配置；
[未接內點引理](c5_unattached_boundary.md) 再完成 (3) 非相鄰型的分離，
並將下述定理擴至有未接內點 boundary 頂點的核心，內點 degree 不受限。

2026-09-24。接續 [五目標](c5_sector_targets.md)、
[雙拒絕分類](c5_two_rejection_proof_zh.md) 與
[3703 排除](c5_sector_3703_exclusion.md)。
**已完成三-spoke 核心的單側出口接合；無結構假設的一般單側出口仍未證。**
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
3. 某個 boundary 頂點沒有有效內鄰點（內點 degree 不受限）。

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
同樣得到 Σ(M)=Ω\{q}。以下只處理第二種。

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
或該點恰三條 boundary spokes。五目標窮盡的是 §2 的 sector 接合，
並不窮盡任意 minimal obstruction 的結構。

**失敗側的必要條件。** 若 Ω\{q}∉W(G)，則 G 的每一個 minimal
q-obstruction 都仍拒絕 p，**都必碰到全部五個 boundary 頂點**，
且每一個都至少符合下列一項：

- 有完整 degree≥6 的有效內點；
- 至少兩個完整 degree=5 的有效內點；
- 恰一個完整 degree=5 的有效內點，其 boundary spokes 數 t≤2。

證明：未接內點引理給出五點皆須被碰到；有效內點 degree≥4，
上述 degree 條件以外的情形恰被 §1 前兩類覆蓋，與定理矛盾。
最後一類的接點數分拆還有 R10 的十二型：t=2 的 (3)、(2,1)，
t=1 的四型，以及 t=0 的六型。五目標排除解決 t=3、(2)；t=2 的 (3) 非相鄰支另由
[未接內點引理](c5_unattached_boundary.md#2-完成兩-spoke-的非相鄰三接點支)
完成分離，餘下 23 個兩-spoke 必要配置尚未分離。

要完成使用者要求的**無條件一般 single-sided exit 定理**，仍須證明
每個候選 A 來源 G、每個定向缺失對 (p,q)，至少存在一個接受 p 的
minimal q-obstruction。證明存在一個 §1 可處理核心是充分途徑，但不是
已知必要條件；也可以直接處理上述剩餘類型，證其分離。
不能為取得 degree 界任意縮圖，因縮圖可能失去 p 的延拓性或來源刪邊關係。

因此本輪完成局部排除到條件式出口的全部橋接，並將一般問題收窄至上述
核心存在／分離缺口；沒有聲稱一般定理被反駁。共同 pivotal edge、候選 A
全部三出口及 K∞=K≤5 仍各需額外證明。

## 6. 證據層與重播

本輪新增紙面接合、五目標 Boolean 窮盡推導與失敗側必要條件。
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
