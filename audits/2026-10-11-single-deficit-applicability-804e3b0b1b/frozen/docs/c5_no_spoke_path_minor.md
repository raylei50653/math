---
docgraph:
  id: c5.no-spoke-path-minor
  family:
    - c5
    - c5.no-spoke
  requires:
    - c5.no-spoke-supports
    - c5.no-spoke-exterior
    - c5.single-spoke-frame-arc
    - c5.single-spoke-cross-row
---
# No-spoke (2,2,1)：原外部路徑 K5 與 record 599 來源排除

後續（2026-09-28）：[首橋與固定框弧](c5_no_spoke_first_bridge.md) 已關閉最後
12 個指定查詢；來源排除仍 500 筆，保留 116 筆全部接受雙列、0 查詢未決。
唯一 degree-5 全部分支已接回條件式出口；必要型可實現性、完整 Σ 與 Lean
形式化仍未完成。下列數字及停止點保留各原輪語境。

2026-09-28。接續 [環狀支援表](c5_no_spoke_supports.md) 的 record 599／p₂；
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 599 在 q 下已不存在，不需要反設 p₂ 拒絕。** C₁ 的禁色
{0,2} 及實際支援 04 迫使每個原路徑塊都碰 b0、b4；C₀ 到 b1 的
原路徑把剩餘框弧接回 z，給來源 K5 minor。

將同一引理套到 (2,2,1) 的 616 筆 T4 保留必要配置，排除 **500 筆
來源**；其餘 **116 筆**再新增 **104 個指定列延拓**，現為 **108 筆
雙列已證、12 個查詢未決**。原 (2,1,1,1) 的 48 筆雙列結論不變。
這尚未完成 (2,2,1) 指定分離，也沒有證保留型可實現或完整 Σ。

證據是任意大小紙面抽取、外部 degree-list 定理及 Python 有限控制；
沒有新增 Lean theorem。來源排除與條件式延拓分開計數。

## 1. 前提、完整關係與共用路徑塊

完整沿用 [必要表 §1](c5_no_spoke_supports.md#1-前提與完整關係)：有限簡單
induced-C5 disk，B=(b0,…,b4)，有效內部 H 非空連通，edge-minimal
q=01012 obstruction；唯一完整 degree-5 點 z 沒有 boundary spoke，
其餘內點完整 degree=4。H−z 的具名原分量為 C₀、C₁、C₂，接點數
為 (2,2,1)，S_k 是全部實際 boundary 支援。套保留表另假設 T4 acceptance。

每個二元關係 R_k(t) 的 tuple 來自同一 C_k coloring，原接點座標、
五個原接點、全部附件、旁支、bridges 與環序始終保留。非空關係給

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\quad
|F_k(t)|\le |P_k|,\qquad
Z_G(t)=U\setminus\bigcup_k F_k(t),\quad U=\{0,1,2,3\}.
\]

最後接合先固定同一 t、同一 z 色，再選各原分量的一份完整 tuple；
不乘 endpoint marginals，也不把支援表宣稱為完整 relation state。

由 [no-spoke 外部連通](c5_no_spoke_exterior.md)，每個 C_k 都是 K4-free
Gallai tree。對任意 proper row t 及 d∈F_k(t)，刪去接點色 d 得不可著色
degree lists。[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 blockwise-uniform palettes；本輪已核對原文。
這一步不需要 target minimality，亦不把此外部定理算作 Python／Lean 證明。

若 |F_k(t)|=2，既有 [雙禁色 bridge 化約](c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)
只用 C_k 的兩個原接點、兩份拒絕 palettes 及 K4-free，與 z 有無 spoke
無關。因此兩接點間為奇數長的原 bridge 路徑 P=(x₀,…,x_ℓ)，ℓ≥1。
刪除全部 P 邊，得兩兩不交的原路徑塊 W_j；每塊保留 x_j、全部旁支
及全部實際 boundary 接線，T_j⊆S_k 為其實際支援。

[逐塊 residual 引理](c5_single_spoke_frame_arc.md) 給
E_t=U\(D_t∪Q_t)=F_k(t)，其中 D_t 是 root 的直接 boundary 色，Q_t 是
旁支 palettes 聯集。端點同時使用兩份拒絕證書求 E_t，不能只取一個 z 色。
rooted palette 唯一性於是給兩種必要條件：

1. 每個逐點固定 t(T_j) 的全域色置換，都保持 F_k(t)。
2. 若 q、t 的 F_k 都是 pair，兩列使用同一條唯一原 bridge 路徑與同一
   W_j；若 t|T_j=π∘q|T_j，則 F_k(t)=π(F_k(q))。

第二條沿用 [跨列 residual 歸納](c5_single_spoke_cross_row.md#2-跨列-residual-換色引理)，
對全部對齊置換成立；沒有對齊置換時不產生限制。任一列為 singleton
時，不套這份雙列 pair 引理。兩條均涵蓋任意有限旁支與任意奇數 ℓ。

## 2. 沒有 spoke 的原外部路徑 K5

固定雙禁色分量 C=C_k，假設每塊 W_j 都實際碰同一對不同框點 b_a、b_b。
若另一原分量 D=C_d 的實際支援包含 h∉{a,b}，由 D 連通，從指定原
接點取簡單路徑到 b_h 的實際鄰點，加首末邊得 L=z…b_h。
L 內部在 D，避開 C 及其他 boundary 點，不要求 D 只有一個接點。

在 C5 上以 a、b、h 分出三份非空連通框弧 X、Y、D_B，分別含這三點；
三弧分割全部 B、兩兩有原框邊相鄰。令 J=P∪{zx₀,zx_ℓ}，任取原
bridge xy=x_ix_(i+1)，取五個 branch sets

\[
A=W_i,\quad A'=W_{i+1},\quad
Z=(V(J)\setminus\{x_i,x_{i+1}\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

J 刪相鄰兩點後的其餘部分經 z 連通，ℓ=1 時就是 {z}；L 將它接到
D_B。W_i、W_(i+1) 與其他原路徑點不交，L 在另一原分量；故五組
非空、連通、兩兩不交。十對鄰接逐一為：

| pair | 原邊 witness |
| --- | --- |
| A–A' | 原 bridge xy |
| A–Z、A'–Z | J 上朝外的兩條邊，端點時為原 z-contact 邊 |
| A–X、A–Y、A'–X、A'–Y | 兩塊各到 b_a、b_b 的實際附件 |
| X–Y、X–Z、Y–Z | 三份框弧間的三條原 C5 邊 |

因此 G 含 K5 minor，與 planarity 矛盾。這是既有 frame-arc 引理的
no-spoke 適用範圍：Z 的連通性完全由原 D 路徑提供。
第三原分量、D 的其餘接點與附件仍在來源圖中；minor witness 不必使用
每個原頂點。沒有改寫任何 R_k、刪去原 coloring 約束或虛構一條 spoke。

## 3. record 599 的較強來源反證

該必要記錄有

```
(S₀,S₁,S₂) = (012,04,234)
(F₀,F₁,F₂)(q) = ({0,1},{0,2},{3})。
```

取 **C=C₁**。F₁(q)={0,2} 給原奇數 bridge 路徑與每塊 residual {0,2}。
若 T_j 不含 b0，支援最多只見 q 色 2，交換 0、3 就會改變 residual；
若不含 b4，支援最多只見 0，交換 2、3 同樣矛盾。因此 **每個 T_j=04**。
這一點只用 q，不涉及 C₀ 的 p₂ palette。

**C₀** 有實際 b1 附件，取其原接點到 b1 的路徑 L。
§2 用 X={b0}、Y={b4}、D_B={b1,b2,b3}，即得 K5。
R₀(q)={(0,1),(1,0)}、R₁(q)={(0,2),(2,0)} 的原 tuple 座標未合併；
C₂ 與其原接點亦保留。故 record 599 沒有符合前提的來源。

原入口中「若 p₂ 拒絕則 F₀(p₂)={1,3}」仍是有效必要條件；但新結果
在 q 下已排除來源，所以 **不另記一個 p₂ 延拓**，也不重複增加 A/A 數。
此具名反證不需要 T4；T4 只用於決定本輪掃描的必要表域。

## 4. 套表、跨列相容性與分開計數

[Checker](../scripts/c5_no_spoke_path_minor.py) 只讀原 no-spoke 支援 artifact，
核對其輸入 SHA256，另存 [新 JSON](../artifacts/c5_no_spoke_path_minor/observations.json)
及 [116 筆保留表](../artifacts/c5_no_spoke_path_minor/support_table.md)。
每筆保留原記錄、所有整數 lifts、五接點環序、完整 F 候選及前層證據。

先在 q 下，對每個 pair 分量枚舉其逐塊穩定子容許的 T⊆S_k。若共同
必接點含 a、b，且另一原分量實際碰第三點 h，就套 §2。
**500 筆均在 q 下直接排除**；其中 264 筆原先條件式 A/A 也須移出。
舊表全部 96 個條件式 reject 查詢的來源均在此步排除，未找到反例。

對其餘 116 筆，從各分量的**整份 F 候選集合**重新列出所有覆蓋 U 的
拒絕組合。共有 116 個原未決查詢、148 組完整候選；136 組被排除，
12 組保留。target pair 用該列穩定子，source 亦為 pair 時再用同一
W_j 的跨列置換；全部拒絕候選都消去才證 target 接受。

| 階段 | 來源數 | A/A | A/? | ?/A | ?/? | 未決查詢 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| q 下排除 500 筆後 | 116 | 4 | 54 | 54 | 4 | 116 |
| 新增 104 個延拓後 | 116 | 108 | 2 | 2 | 4 | 12 |

104 個新增延拓中，88 個由單列／兩列穩定子即可得到；另外 16 個需要
真正的跨列置換條件。500 個來源排除、104 個延拓都包含具名 C₀、C₁
交換記錄，並非圖的數量。checker 核對交換後狀態一致；反射用
ρ(i)=3−i、π=(0 1) 搬全部支援、禁色、框弧與**字面 target 色列**，
不只比較正規化相等分割。

## 5. 剩餘查詢與下一窄入口

| 原 record ID | 尚未決的指定列 |
| ---: | --- |
| 84、1472 | p₁ |
| 408、1561 | p₂ |
| 127、419、1390、1564 | p₁、p₂ |

下一入口為 **record 84／p₁**：支援 (014,123,34)，q 禁色
({0},{2,3},{1})；p₂ 已可取 z=2。p₁ 的七組完整拒絕候選已消去六組，
只剩

\[
(F_0,F_1,F_2)(p_1)=(\{0,1\},\{3\},\{2\}).
\]

此時 C₀ 的 p₁ 原路徑塊支援只能為 01、04、014：每塊碰 b0，並碰
b1／b4 至少一點。q 在同一 C₀ 卻只有 singleton {0}，不能套雙列 pair
residual 等式。C₁、C₂ 的外部支援合為 1234，沒有 b0 附件；必須保留
同一 C₀ 的 source palette、原首橋、完整兩個接點關係與 C₁／C₂
實際外部路徑，再處理 singleton／pair 相容性。

另外四筆雙列未決仍保留，不宣稱它們需要同一種新引理；本輪只套 §1–2，
沒有重開來源圖枚舉或自動套用尚未核對 no-spoke 前提的首橋／兩框弧規則。

## 6. 控制與重播

- 重播 48 個 residual 端點／內點控制、576 個單列支援穩定子控制、
  2,304 個跨列支援控制與 1,944 個 residual 換色代數控制；保存數目與摘要。
- 1,368 份 no-spoke minor skeletons 及其反射：全部 60 種具名三框點、
  長度 1／3／5 的每個相鄰 bridge 位置、外部分量一／二接點角色；
  record 599 的 04／1 再核對 16 種兩塊 tether 形狀與兩種外部路徑長度。
  每份保留三個原分量、五個接點、零 spoke、五個 branch sets 與十條原邊鄰接。
- 12 個負控制，含缺外部邊／tether／bridge／框邊、不交性破壞、沒有第三
  落點、singleton 不套 pair 引理、無對齊不排除、部分候選未決不接受。

上述 skeletons 不要求滿足完整 degree=4 lists，故不是來源可實現性證書。
刪邊負控制只核對指定 minor witness 失效，不宣稱刪邊後整圖平面。
任意大小由原圖 bridge／palette 歸納及 §2 的 composed branch sets 承擔。

```bash
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 無參數時只生成本輪 JSON／表，有 `--check` 時逐 byte 重算比對。
實際驗證及未重跑項目見 [本輪紀錄](history/2026-09-28-no-spoke-path-minor.md)。
`lake build` 不形式化本輪紙面拓撲；一般單側／共同出口、degree≥6、
多 degree-5、(2,2,1) 完整分離與 `K∞=K≤5` 仍未證。
