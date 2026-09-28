---
docgraph:
  id: c5.single-spoke-two-two
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-cores
    - c5.single-spoke-bridge-path
    - c5.single-spoke-two-contact-bounds
    - c5.degree5-interfaces
---
# Single-spoke (2,2)：完整關係、actual supports 與接點次序的必要分類

後續（2026-09-28）：[frame-arc K5](c5_single_spoke_frame_arc.md) 放寬支援點
相鄰限制，累計排除 272 筆來源，剩 108 筆／54 型；另證 18 個 target（含
record 15 的 p₂），保留表現為 58 筆雙列已證、50 筆含未決項、66 個單列查詢。
原必要表、完整關係與先前證書維持原內容；下文數字保留各當輪語境。

後續（2026-09-28）：[路徑塊支援與來源 K5](c5_single_spoke_two_two_minor.md)
已排除 record 110、119 及 26 筆／13 型；[外部路徑接合](c5_single_spoke_two_two_external.md)
再排除含 record 104 的 210 筆／105 型，原 380 筆現剩 144 筆／72 型。
原 104 筆條件式雙列延拓中，50 筆來源已排除、54 筆仍保留。下文與原 artifact 保留必要分類
當輪的 380 筆及未解語境，後續排除另有可追溯證書。

2026-09-27。沿用 [四型必要覆蓋](c5_single_spoke_cores.md)，只處理 H−z
有兩個二接點分量。研究優先序見 [HANDOFF](HANDOFF.md)。

**結果：** 任意大小來源先化為兩份完整二元關係、實際支援及 slit-disk
接點區塊；雙禁色分量另有奇數 bridge 路徑必要結構。三個 spoke 代表有
1,530 筆具名必要配置，T4 排除 1,150 筆，保留 **380 筆／190 個交換分量名字
後的型**。其中 104 筆已證兩個指定 p 延拓；其餘的逐分量禁色集合候選、
必要上界及強迫拒絕列逐筆保存。**保留不等於可實現；這不是完整 disk
可實現性分類，也尚未證 (2,2) 出口分離。**

## 1. 前提與精確 minimality 判準

G 有限、簡單，B=(b0,…,b4) 是 induced C5 disk 外框；有效內部 H 連通。
G 是 edge-minimal q=01012 obstruction，唯一完整 degree-5 點 z 恰接一個
boundary 點 b_s，其餘內點完整 degree=4。H−z 的兩個分量分別為 C0、C1，
各有兩個不同的原接點 P_k=(u_k,v_k)。T4 篩選才另要求 G 接受全部四色列。
U={0,1,2,3}，p₁=01021，p₂=01212。沒有假設來源內點數上限或 T4 的實現性。

對每個 proper row b，沿用 [R10](c5_degree5_interfaces.md) 的完整關係：

```
R_k(b)={(f(u_k),f(v_k)): f 是 C_k 的 proper boundary-list coloring},
F_k(b)= intersection_{t in R_k(b)} set(t),
Z_G(b)=(U\{b_s})\(F_0(b) union F_1(b)).
```

R_k 非空；每個 tuple 必來自同一份整分量 coloring。固定同一 b、同一 z 色
後才將 C0、C1 接合。來源給定時，R10 解除引理使 minimal q **恰等價於**
`F0∪F1=U\{q_s}` 且兩者各有 private color（並沿用 q 下實際 spokes 異色
前提）。每條 C_k incident edge 的刪除解除整份 F_k；刪 zb_s 釋放 q_s。
此等價式用實際 R，不能把下列抽象關係／支援候選代入後宣稱存在來源。

令 {a,b,c}=U\{q_s}。可能的禁色角色只有：

| 大小 | F0 / F1 | 固定 s、有標號分量數 |
| --- | --- | ---: |
| (1,2) | {a} / {b,c} | 3 |
| (2,1) | {a,b} / {c} | 3 |
| (2,2) | {a,c} / {b,c} | 6 |

## 2. 完整 ordered relation 的必要 schema

逐接點解除給出：每個 a∈F、每個座標 j，都有一個完整 tuple 恰在 j
出現 a。因此二接點分量的固定 q 關係分為：

- `F={a,b}`：**R={(a,b),(b,a)}**，沒有其他 tuples，也不能只留其中一個。
- `F={a}`：R 是七個含 a 的 ordered pairs 的非空子集，兩側都須有
  非對角解除 witness，而且全部 tuple 色集的交集恰為 {a}。
  恰有 `2(2³−1)²−3=95` 個 schema；允許 (a,a)，不強迫接點相鄰。

故 (1,2)/(2,1) 每個角色覆蓋各有 95 個原始關係組合；(2,2) 每個覆蓋的
兩份 R 均已確定。全部四色角色合計 380 個 singleton schemas 加 6 個
pair schemas。實際支援 S_k 上的 q 色穩定子必**逐 tuple 集合**保持 R_k；
checker 依這個更完整的條件保存每個配置可用的 `relation_schema_ids`。

未知列 b 仍保留原來 R_k(b) 的定義與座標；本報告不捏造其精確数值。
若其 F 是 singleton，仍受同一 95-schema 條件限制；若是 pair，則完整
R 恰為交換 pair。這些跨列 schema 必須來自同一來源，不能逐列獨立挑選。
例如 R={(0,1),(1,0)} 與其 marginals 的乘積具有相同兩個投影，卻分別
禁 {0,1} 與 ∅；checker 保存這個負控制。

## 3. 任意大小的 actual-support／contact 化約

S_k 是 C_k **實際**接到的 boundary index set，不是允許接線的超集。
沿用原必要化約：S_k 非空，C_k 是 K4-free Gallai tree，只有 bridges／
odd-cycle blocks。這依賴既有外部 degree-list 定理及連通外框 K4 排除。

對每個 a∈F_k(q)，必有 `|q(S_k)∪{a}|≥2`。若只有一個外部色，tightness
使所有 C_k 點的內部 degree≥3；但有限 K4-free Gallai tree 有 degree≤2
的 leaf-block 私有點，矛盾。此處是**逐一禁色**檢查，不能只檢查
`q(S_k)∪F_k(q)` 的大小。

沿 zb_s 切開 disk，框線位置 0,…,5 依次為 b_s,…,b_(s+4),b_s。
兩份支援各提升為非空 T_k；每份接點必成一個區塊，且區塊先後滿足
`max T_first ≤ min T_second`。相等容許共用原框點；0、5 是同一 b_s，
不能分配不同色。證明沿用原 slit-disk crosscut 引理，不改動任一接點、
attachment 或 bridge。每份提升及區塊順序都保存，不只存一個見證。

tuple 座標始終具名 (u0,v0)、(u1,v1)。每個區塊可在 embedding 中讀成
(u_k,v_k) 或 (v_k,u_k)，故每個 placement 保存四個 contact words。
它們是必要允許方向，不是四份實現證書；未知拓撲可能繼續排除其中一些。

### 雙禁色的同圖奇數 bridge 路徑

若任意列 b 有 F_k(b)={a,d}，則 u_k 到 v_k 的唯一路徑由**原圖 bridges**
組成，長度為奇數；該路徑上的每一點都沒有顏色 a 或 d 的 boundary 鄰點。
所有其餘 blocks、attachments 保留在沿路旁支，不能刪掉它們來替換 R。

證明是 [既有雙禁色路徑](c5_single_spoke_bridge_path.md) 的任意色版本：
比較同圖 (b,z=a)、(b,z=d) 的兩份 tight palettes。沿 block incidence
樹由外向內消去 u–v 路徑外的 blocks；它們不含接點，兩份 residual lists
相同，故 palettes 相同。在兩接點，差仍是 {d}/{a}。沿路每個 block 都
必有非零差；若遇 odd cycle，第三個頂點及其旁支卻強迫 palette 相同，
矛盾。因此只有 bridges。兩份 singleton palettes 從 (d,a) 開始交替
(d,a)、(a,d)，另一端同樣要求 (d,a)，故長度奇數。中間 residual list
為 {a,d}，端點則由兩份 tightness 排除 a、d 的 boundary 接線。

每個 (2,2) q 覆蓋至少有一份雙禁色分量，因此至少一份這樣的原 bridge
路徑；雙 pair 覆蓋有兩份，始終位於不同 C_k，不可合併。
任意長度由上述歸納承擔，有限 checker 只核對 12 個局部交替轉移。

## 4. p₁、p₂ 的必要 forbidden-colour 上界

對每份 S、F(q) 及同一字面 target b，使用以下規則。

1. 若有四色置換 π 使所有 i∈S 都滿足 b_i=π(q_i)，則完整
   `R(b)=πR(q)`，故 F(b)=πF(q) **精確已知**。若有多個 π，它們給相同 F；
   每個原始 R schema 還須通過 §2 的穩定子。
2. 否則，令 V=b(S)、D=U\V。F(b) 必為大小至多二的集合，且對固定 V
   的色置換不變。因此 D 必全入或全不入 F；|D|>2 時全不入。
   再逐一套外部至少兩色限制。artifact 保存全部候選 F，不只它們的聯集。
3. 沿用 [二接點未用色對引理](c5_single_spoke_two_contact_bounds.md#5-二接點未用色對的-bridge-障礙八個查詢)：
   若 a∈F(q)，d 不在 q(S)∪b(S)，且有 e∉q(S)、a,d,e 互異，則 d∉F(b)。
   對每個 a 都可套用，不要求 F(q) 只有 a；該引理的證明只用 q 禁 a。
   比較兩份 palettes 對 d 的 membership，強迫第一條 bridge 的 q palette
   含 d；但 q,z=a lists 在交換未用的 d,e 下不變，singleton bridge palette
   不可能含其中一色。此論證不需外部分量的兩條不交路徑。

記所得候選族為 B0(b)、B1(b)。逐分量上界為各 Bk 的聯集，但**接合保留
整個候選族**：若所有候選 pair 的聯集都不覆蓋 U\{b_s}，則接受 b；若每個
都覆蓋，則強迫拒絕；其餘未決。這可比逐色聯集上界更強，因容量／換色
限制有相關性。`rejection_options` 保留能導致拒絕的整組 F 候選，仍非實現。

在 T4 上強迫拒絕即可排除配置。T4 保留者若 b4 沒有內鄰點，另由
[未接內點引理](c5_unattached_boundary.md) 證兩個 p 都接受，具體改色列為
01023、01213。這是 T4 的**共同**限制，沒有冒稱縮小某一分量的 F 上界；
artifact 的局部 `rejection_options` 仍只是忽略這項共同限制時的候選。

## 5. 有限必要表與結果

先完成上述任意大小化約，才窮盡 31 個非空 actual-support 子集、12 個
覆蓋及六個切口位置。這不是來源圖枚舉，也不是小圖正常形猜測。
只篩選 s=0、1、4；s=3、2 由既有完整關係反射搬運。

| s | 關係穩定子通過 | 次序排除 | 外部色排除 | minimal-q 必要候選 | T4 排除 | T4 保留 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 2616 | 2114 | 86 | 416 | 284 | 132 |
| 1 | 2616 | 2012 | 90 | 514 | 366 | 148 |
| 4 | 2628 | 1940 | 88 | 600 | 500 | 100 |

380 筆的禁色大小依 (1,2)、(2,1)、(2,2) 分別為 134、134、112。
80 筆不碰 b4；300 筆碰齊五個 boundary 點。以下 A 為已證接受、R 為
條件式強迫拒絕、? 為未決；數目仍含 C0/C1 名字交換。

| p₁ / p₂ | A/A | A/? | ?/A | ?/? | A/R | R/? | ?/R | R/R |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 筆數 | 104 | 58 | 60 | 118 | 6 | 14 | 16 | 4 |

「R」表示**任何具有這份支援與 q 角色的來源若存在**都拒絕該列；不是
已找到來源。A/A 的 104 筆中，80 筆由未接 b4，另 24 筆碰齊框點。
完整 190 行 [支援表](../artifacts/c5_single_spoke_two_two/support_table.md)
列出 actual supports、q 角色、兩個 p 的逐分量上界及狀態；全部具名表項、
所有 contact words／lifts、schema ids、候選禁色集合及 T4 排除列在
[JSON artifact](../artifacts/c5_single_spoke_two_two/observations.json)。

反射使用 ρ=(3,2,1,0,4)、π=(0 1)，沿用既有 Lean 普通關係搬運：
保持 tuple 的具名座標，反轉 contact word／slit lifts。artifact 同時記錄
原始 Tp₁=21010、Tp₂=02012，以及在**反射來源**全域換色後的 canonical
p₂、p₁ 禁色上界。只正規化 target 的著色查詢，不把換色後的 q 角色
偷偷當成原角色，也不獨立枚舉反射側。

## 6. 驗證、信任界線與停止點

[checker](../scripts/c5_single_spoke_two_two.py) 核對全部 65,535 個非空
二元 tuple 子集、386 個非空禁色解除 schemas、9,264 個整關係色搬運、
2,880 個 minimal 覆蓋的完整 tuple 接合及 12 個 bridge 交替轉移。
輸入報告／程式與既有控制保存 SHA256，`--check` 重算並逐 byte 比對 JSON
和支援表。沒有改寫舊 artifact，沒有重開 (2,1,1)。

沿用原 single-spoke 證書的 16 個已封存 (2,2) 來源控制，每個重播 240 列
完整 tuples 的禁色與接合，並全部落入本表的 T4 排除項。這些是繼承的
relation 資料控制；本輪未重新建圖、重驗刪邊 colorings 或全圖 disk rotation。
它們不接受 T4，不能充當新表保留型的正例。

證據為任意大小紙面化約＋沿用外部 degree-list／K4-free 結構與既有反射＋
Python 有限局部代數／支援證書。**未新增 Lean theorem**；lake build
不把新任意大小 palette／disk 化約變成形式化證明。

```bash
python3 scripts/c5_single_spoke_two_two.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證見 [本輪紀錄](history/2026-09-27-single-spoke-two-two.md)。
下一個窄問題可取 record 110：s=0、(S0,S1)=(34,12)、
(F0(q),F1(q))=({1,2},{2,3})，接點區塊 C1 在 C0 前，各有原奇數 bridge
路徑。必要關係迫使兩個 p 都拒絕，但 T4 screen 未排除；應研究兩份原
路徑、旁支實際 tethers 的共同 disk 可實現性／來源 minor，不能宣稱已有反例。
另一個同上界型 record 119 將 S0 擴為 034，仍须保留多出的實際接線。
其餘保留型的可實現性、完整 (2,2) 分離、(3,1)/(4)、t=0、高 degree／
多 degree-5、一般核心存在性與 K∞=K≤5 仍開放。

**2026-09-27 後續：** [同染色有序重接](c5_dual_path_surgery.md) 固定 record 110
任一 α=01023 補完的三份 dual 配對，並給出交換前後須共同滿足的兩個
切口重接等式。同圖反例證明初始三配對不足以決定後繼；尚未把兩份原
bridge 路徑及旁支 tethers 化成違反等式的來源障礙，故 record 110 仍未排除。
