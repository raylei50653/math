# No-mixed 十五類整理：source 預算與外框跨度

後續提交驗證見[同日發布核對](history/2026-09-29-no-mixed-span-budget.md#後續提交與發布核對)；
下文的未提交敘述保留整理輪語境，即時發布狀態以 Git 為準。

2026-09-29，Git 基準 `47ebbbc`，納入工作區已有 B–C 至 E–E 成果。
**十五類可壓成一個 source 必要不等式：兩側的最小框弧跨度之和至多五。**
A／B／C／D／E 的側跨度下界為 **2／2／3／4／3**。超過五的八類全作
來源排除；其餘七類沿用完整關係與原路徑證據完成指定雙列分離。

新增的是下述任意大小的紙面推導與跨表稽核，不新增來源刪除或 target
接受。原十五份完成證書共保存 5,842 份必要支援，3,760 份 source 排除，
2,082 份保留支援的 4,164 個 target 全接受；這些都不是來源圖的計數。
原 3,548 個接合 IDs 含 root 交換方向，支援及查詢只計各報告保存的正向表。

完整[生成總表](../artifacts/c5_no_mixed_span_budget/summary_table.md)、
[逐 ID 證書](../artifacts/c5_no_mixed_span_budget/observations.json)及
[checker](../scripts/c5_no_mixed_span_budget.py)。目前研究入口見
[weak-deletion 導覽](c5_weak_deletion_guide.md)，驗證紀錄見
[本輪歷史](history/2026-09-29-no-mixed-span-budget.md)。

## 1. 適用前提與精確語義

固定有限簡單圖 M，B=(b0,…,b4) 為 induced C5 disk 外框，H=M−B
非空連通。M 拒絕 q=01012，刪任一非框邊後接受 q。恰有相鄰 z,w
完整 degree=5，其餘內點完整 degree=4；H−{z,w} 每個原分量 C 恰接
一個 root。固定 U={0,1,2,3}；targets 為 p₁=01021、p₂=01212。
不需 T4，不另假定來源接受其他列，不限制原分量大小。

保留原分量、具名 contacts、全部 bridges／旁支、實際 boundary 附件、
原 zw、spokes、環序及共同字面色框。T_C(β) 是原 C 的完整有序接點
關係；F_C(β)=⋂_{τ∈T_C(β)}set(τ)，而非端點 marginals 的交集。
接點 slack 保證 T_C(β) 非空。對每列 β，精確接合是

\[
E_r(\beta)=U\setminus\left(\beta(N_B(r))\cup\bigcup_{C\sim r}F_C(\beta)\right),
\qquad Z_M(\beta)=(E_z(\beta)\times E_w(\beta))\setminus\Delta.
\]

[Root 預算](c5_root_degree_excess.md)給 source q 的
D_r+O_r+κ_r=1，κ_r=0，E_z(q)=E_w(q)={c}；spokes 異色且各 F_C(q)
避開同側 spoke 顏色。[原平面化約](c5_adjacent_degree5_no_mixed.md)之後
恰剩下列五種側型。以 m_r 計原分量數，s_r 計禁色為二元集的原分量數：

| 側型 | spokes t_r | 接點分拆 | (D_r,O_r) | 禁色大小 | m_r | s_r | 側跨度下界 ω_r |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| A | 2 | (2) | (1,0) | (1) | 1 | 0 | 2 |
| B | 1 | (2,1) | (1,0) | (1,1) | 2 | 0 | 2 |
| C | 0 | (2,2) | (1,0) | (1,2)，或反序 | 2 | 1 | 3 |
| D | 0 | (2,2) | (0,1) | (2,2)，重疊一色 | 2 | 2 | 4 |
| E | 0 | (2,1,1) | (1,0) | (1,1,1) | 3 | 0 | 3 |

source 缺額／重疊預算不施加到 p₁、p₂。下文「飽和分量」專指二接點且
|F_C(q)|=2；單接點 singleton 分量仍須佔正跨度，不能改作 spoke。

## 2. 從原圖導出框弧成本

### 2.1 同序支援與兩側框弧

每個原 F_C(q) 非空真子集，故 C 有非空 actual support S_C⊆B。
對任一 C，經原 spoke、同側另一原分量或原 zw 加另一側原分量，存在
避開 C 的 root–B 原路徑。沿用[外部 hub](c5_no_spoke_exterior.md)與
[三分量支援引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#2-三分量五單位的任意大小支援覆蓋)，
每個拒絕分量是 K4-free tight Gallai tree。

此處使用外部 [Dvořák 講義 Lemma 7、Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通圖的 degree-list 拒絕迫 tightness 及 blockwise-uniform Gallai 結構。
本輪重新讀取核對前提；它仍是外部定理，非本專案新 Lean 證明。

若 S_C 只見一個 q 色 d，固定 d 的 S3 穩定子不能保持二元禁色；
singleton 禁色則只能是 {d}。將 root 設 d，全部外鄰皆同色，tightness
迫每點內度至少三，與 K4-free Gallai leaf block 的私有點內度至多二
矛盾。因此每個原分量至少見兩個 q 色，支援的整數跨度至少一。

取 zw 的細正則鄰域。其兩側 incidences 各成一段，同一 binary 分量的
兩 contacts 連續；原內部路徑的 Jordan 分離及其他 incidences 的外部
原路徑證明這一點。沿用既有 annulus crosscut 引理，各 actual supports
及 spoke 按單位次序有互不交錯的 lifts；相鄰可共框端點，總跨度連同
間隙至多五。支援本身保持稀疏，沒有先填成整弧。

對 r=z,w，取包含該側全部分量支援與 spoke 的最短區段 I_r，沿這一份
同序 lift 定義長度 ℓ_r。側內間隙計入 ℓ_r；兩側框邊內部不交，所以

\[
\ell_z+\ell_w\le5.\tag{1}
\]

這是保留同一環序後的兩個側弧，不是分別選兩個互相不相容的最短 hull。

### 2.2 飽和二禁色分量不能只佔一條框邊

設 C 飽和，反設其 lift 跨度一，S_C={a,b} 為相鄰框點。
[飽和原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)
給兩原 contacts u,v 間的奇數長 bridge 路徑 P=x₀…xℓ；刪去 P 邊後
各原路徑塊 W_j 保留全部旁支，其 rooted residual palette 恰為 K=F_C(q)。
每塊的支援 T⊆{a,b} 必使逐色固定 q(T) 的置換保持 K。
空集及單點的穩定子均不能保持二元集，故每個 W_j 都碰 a,b。

此時 C 所在側必為 C 或 D 型，總原分量數至少三。其他任一分量的
正跨度至多三，故其支援不能也包含於 {a,b}：使用同一框邊會相交，
使用反向補弧則需跨度四。於是另一原分量 C′ 有附件 b_h∉{a,b}。
從 C 所屬 root r 經 C′，必要時先經 zw，取得避開 C、只在終點碰 B
的原路徑 L。沒有新增 root–B 邊。

取 X={b_a}、Y={b_b}、D_B=B−{b_a,b_b}，令 J=P∪{ru,rv}。以下五組
為原圖的 K5 branch sets：

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.\tag{2}
\]

第三組經 r 連通，P 長度一時仍含 r；五組不交。原 bridge、J 兩個
朝外邊、W₀/W₁ 各至 X/Y 的附件與三框弧切口給全部十對鄰接。
因此平面性迫每個飽和 C 的跨度至少二，且

\[
\ell_r\ge m_r+s_r.\tag{3}
\]

這抽出了 [D–D](c5_adjacent_degree5_no_mixed_dd.md)及
[C–E](c5_adjacent_degree5_no_mixed_ce.md)的共同局部引理。
它不保證跨度二的飽和分量可實現；較長支援仍可能被固定框弧 K5 排除。

### 2.3 A 側還需要一單位

A 側只有一個 singleton 禁色的 binary 原分量 C，但有兩條不同 spokes。
若 ℓ_r≤1，兩個不同 spoke 落點只能是同一框邊的兩端；C 的正跨度又
迫 S_C 恰為該兩端。因 q proper，兩端異色。singleton F_C(q) 受支援
色穩定子保持，只能是這兩個已見色之一；然而 source minimality 要求
F_C(q) 避開兩條 spoke 的顏色，矛盾。故 A 側 ℓ_r≥2。

這一單位可以由 C 自己較長的跨度或側內間隙供應，不能強稱 C 的跨度
必為二。只計 m+s 而忽略兩 spoke 與原關係的相容性，會漏掉 A–D。

### 2.4 統一必要不等式及直接推論

令 a_r=1 若 r 為 A 側，否則為零。由 (1)–(3) 及 A 側論證，得到

\[
\boxed{\omega_r=m_r+s_r+a_r,\qquad
\omega_z+\omega_w\le5.}\tag{4}
\]

等價地，以 m 計全部原分量、s 計全部飽和二禁色分量、a 計兩-spoke
roots，**m+s+a≤5**。這是指定圖類的任意大小 source 必要條件。
沒有加入 target 拒絕假設，也沒有由有限表的全稱替代上面的拓撲證明。

| z \ w | A：2 | B：2 | C：3 | D：4 | E：3 |
| --- | --- | --- | --- | --- | --- |
| A：2 | 4 | 4 | 5 | 6，排除 | 5 |
| B：2 | 4 | 4 | 5 | 6，排除 | 5 |
| C：3 | 5 | 5 | 6，排除 | 7，排除 | 6，排除 |
| D：4 | 6，排除 | 6，排除 | 7，排除 | 8，排除 | 7，排除 |
| E：3 | 5 | 5 | 6，排除 | 7，排除 | 6，排除 |

八個無序排除類恰為 AD、BD、CC、CD、CE、DD、DE、EE，涵蓋 1,848
個原有序接合 IDs。其餘七類涵蓋 1,700 IDs；這不是可實現性分類。
另得到三個易於重用的 source 結論：

- **至少一條 root-spoke：** t_z+t_w≥1，因無 spoke 側的成本至少三。
- **沒有 source 重疊：** D 側不可存在，故兩側 O_r=0、D_r=1。
  每側恰一份二接點 singleton 禁色分量承擔唯一容量缺額。
- **至多一個飽和二禁色分量：** 它若存在，只能在 C 側，另一側為 A 或 B。

## 3. 把十五輪證據放回同一張表

以下「支援」均為各完成報告保存的正向必要表；原接合 IDs 含交換方向。
Source 排除與 target 接受分開，E–E 的空纖維也不記成 K5 或接受。

| 類型／原報告 | 原接合 IDs | 必要支援 | Source 排除 | 保留支援 | Target 接受 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [A–A](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) | 88 | 322 | 0 | 322 | 644 |
| [A–B](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) | 272 | 560 | 0 | 560 | 1,120 |
| [A–C](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md) | 192 | 364 | 340 | 24 | 48 |
| [A–D](c5_adjacent_degree5_no_mixed_t2_t0_overlap.md) | 192 | 212 | 212 | 0 | 0 |
| [A–E](c5_adjacent_degree5_no_mixed_t2_t0_singles.md) | 192 | 120 | 0 | 120 | 240 |
| [B–B](c5_adjacent_degree5_no_mixed_bb.md) | 236 | 888 | 0 | 888 | 1,776 |
| [B–C](c5_adjacent_degree5_no_mixed_bc.md) | 360 | 608 | 584 | 24 | 48 |
| [B–D](c5_adjacent_degree5_no_mixed_bd.md) | 360 | 312 | 312 | 0 | 0 |
| [B–E](c5_adjacent_degree5_no_mixed_be.md) | 360 | 144 | 0 | 144 | 288 |
| [C–C](c5_adjacent_degree5_no_mixed_cc.md) | 144 | 1,176 | 1,176 | 0 | 0 |
| [C–D](c5_adjacent_degree5_no_mixed_cd.md) | 288 | 640 | 640 | 0 | 0 |
| [C–E](c5_adjacent_degree5_no_mixed_ce.md) | 288 | 96 | 96 | 0 | 0 |
| [D–D](c5_adjacent_degree5_no_mixed_dd.md) | 144 | 352 | 352 | 0 | 0 |
| [D–E](c5_adjacent_degree5_no_mixed_de.md) | 288 | 48 | 48 | 0 | 0 |
| [E–E](c5_adjacent_degree5_no_mixed_ee.md) | 144 | 0 | 0 | 0 | 0 |
| 合計 | 3,548 | 5,842 | 3,760 | 2,082 | 4,164 |

獨立側弧 mask 稽核逐筆保留同源支援／原 IDs，全部 5,842 份皆找到同序
兩側配置。八個超額類的非空支援均含一份框邊飽和分量，與 (4) 一致；
E–E 直接因六正跨度而無表。全部表合計 3,624 份支援可用 §2.2 的短
框邊 K5，其中也包含 AC／BC 的部分已排除支援。
其餘 **136 份 source 排除仍需較一般的固定框弧論證**；這具體顯示
簡單跨度條件沒有取代原支援證書，也不是來源存在的充分條件。

對 3,624 份各取一份具名框弧／原外部路徑見證，重播 bridge 長度
1、3、5，共 10,872 次 minor 控制，驗證 branch sets 的不交、連通及
十鄰接。有限 skeleton 不是 degree-list 來源實現證書。新 JSON 綁定
輸入 SHA、逐原 ID 覆蓋、每筆側跨度、見證及控制 hash，並逐筆核對原
target 最終狀態。這不取代原 checker 的完整關係／反射／交換重播。

## 4. 通用結構的兩層，及尚未統一的部分

目前可用的共同組織是：**代數決定需求，幾何限制可容納的需求；保留
來源的跨列結論再使用同源完整關係。**

```mermaid
flowchart LR
  A[Source minimality] --> B[D + O = 1：五側型]
  B --> C[正跨度、飽和原路徑、A 側相容性]
  C --> D[側跨度和至多 5]
  D --> E[八類來源排除]
  D --> F[七類保留為必要入口]
  F --> G[完整關係搬運與容量上界]
  G --> H[原路徑、端點及 palette 交換]
  H --> I[指定 p₁、p₂ 延拓]
```

七類中 AE／BE 的支援與色置換搬運最直接；BC 的保留支援以完整搬運／
容量界完成；AC 仍有八個查詢需要 target 飽和路徑 K5；BB 的 120 個
失敗候選需原路徑或雙端點；AB 需非守恆色的雙端點相容性；AA 最後
四個查詢需整條原 bridge 路徑 palette 交換。這些機制的前提見
[範圍遍歷](c5_exchange_geometry_scope.md)，不能由 (4) 直接推出。

結合七份既有雙列分離與八類來源排除，得到：**§1 全部 no-mixed
minimal q-cores 均接受 p₁、p₂。** 這是十五輪結論的合併，不是本輪新增
4,164 個延拓。接回[出口第九類](c5_single_sided_exit.md)的完整 Σ，仍需
來源雙缺失 Σ(G)=Ω∖{p,q} 及刪邊繼承。

下一個有意義的通用問題是：在保留完整關係與實際路徑的情況下，能否
由「每側一缺額、至多一個 source 飽和分量」給出七類共同的跨列證明，
取代逐表查詢。這裡只提出明確目標，**未證機制完備性**；AA 的最後四個
查詢及 AB 的非守恆色端點應作為不可省略的控制。不能重開已閉合枚舉
來取代該證明工作。

往 root 樹推廣時，同一 root 的 incidences 可能分居多個外周區段，
先要建立相容的區段分配；本輪的兩側弧不自動存在。遇 mixed 原分量，
必保留多 root 有序關係，不能再以 unary F_C 聯集代替。
較大／多 mixed、非相鄰 roots、多 degree-5、degree≥6、一般／共同出口
與 K∞=K≤5 仍未解；此不等式也未證任何必要支援可實現。

## 5. 重播與證據界線

```bash
python3 scripts/c5_no_mixed_span_budget.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_span_budget.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_root_degree_excess.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪另重跑上表十五份完成 checker，確切命令及省略範圍見
[研究紀錄](history/2026-09-29-no-mixed-span-budget.md)。`--check` 逐 byte
比對本層輸出；無參數只生成本層，不重寫舊 artifacts。

證據分層：§2 為依賴既有拓撲／原路徑引理的任意大小紙面推導；Gallai
為外部定理；總表、色穩定子、側弧 masks 及 skeletons 為 Python 固定域
控制。未新增 Lean theorem 或 native_decide；`lake build` 不表示新紙面
拓撲已形式化。本輪未使用獨立第二審稿者，未 commit／push。
