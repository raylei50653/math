# C5 edge／alternating-path state：精確轉換與第一輪不足見證

2026-09-15。接續 [三個完整 AB|CD survivor](c5_corner_disks.md)，實作使用者提出的
edge-type／pairing／polygon 候選表示之最小固定圖實驗。

**結論**：edge 表示提供對称的 connectivity 語言，且能精確寫出 Kempe move；
但 `T=(w,π₁₂,π₁₃,π₂₃)` **不能單獨決定後續 transition**。
同圖、同 boundary、同 T 可以有不同的最短 escape 距離；加上三組 cycle 數仍不足。
因此先保留這個觀察層，下一步需補跨系統的 incidence／region interface，不能直接
把 T 當成 future-sufficient 的有限狀態。

**信任範圍**：下列一般轉換與 disk separation 為紙面論證；固定圖數值是精確 Python
重播。沒有新增 Lean 定理、沒有證明 H1–H5，也沒有排除新的 boundary relation。
既有 [C5ParityWord.lean](../Math/C5ParityWord.lean) 已證 boundary edge word 加基準色
可恢復 boundary；本輪全圖／dual／transition 論證沒有自動繼承該形式化保證。

## 1. 完整 edge 表示與 terminal 壓縮要分開

固定 `A=0, B=1, C=2, D=3`，`α=1, β=2, γ=3`，`δ(uv)=c(u) xor c(v)`。

對**連通的固定圖**，完整 δ 加上一個基準色 `c(v₀)` 可沿任意路徑積分恢復 c。
若 δ 來自染色，閉路 XOR 為零，故路徑無關。反向若是在三角化 disk 上指定每個
三角形恰有三種 type，則每個面 XOR 為零；disk 的 cycle space 由面邊界生成，
因此可積分。非零 δ 保證 proper。這是完整表示的可逆性，並不是 T 的可逆性。

在完整 edge 表示中，只需一個全域 anchor，毋須為 AB 與 CD 各放一個 phase。
若把完整 δ 壓成 boundary pairings，anchor 不會恢復已丟失的內部資訊。
下文所有不足見證甚至都有同一 `c(0)=0`、同一完整 boundary word。

保持 ordered terminals：terminal i 位於 primal edge `(i,i+1 mod 5)`。
五條邊的 XOR 為零，所以三個非零 type 各出現奇數次，multiplicities 恰為 `(3,1,1)`。
每組 two-type system 因而有一條或兩條 terminal paths，另可有任意數量的 cycles。
固定 w，兩組四端點 systems 各最多兩種 noncrossing matching，兩端點 system 唯一：
所以純 T 最多有 `60 × 2 × 2 = 240` 種（不附 anchor；這是上界，非全部可實現性）。

此表示與文獻的 cubic graph edge-Kempe 語言相接；
[belcastro–Haas, arXiv:1209.1730](https://arxiv.org/abs/1209.1730)
研究 edge-Kempe equivalence。本文以下的 disk component-cut 規則是直接推導並重播，
不把閉合 cubic 圖的結果直接當成 ordered 5-pole 定理。

## 2. 精確的 Kempe transition：翻轉整個 cut，不一定只有一條曲線

令 S 是 primal 的 `{a,b}` induced graph 中一個完整 component，`k=a xor b`。
交換 S 內的 a、b，等價於

```
c'(v) = c(v) xor k     if v in S
        c(v)           otherwise.
```

於是逐邊精確得到

```
δ'(uv) = δ(uv) xor k   if exactly one endpoint lies in S
         δ(uv)         otherwise.
```

cut 邊不可能有 type k：若有，外端也是 a 或 b，便應屬於同一 component。
故 cut 上另外兩種 types 互換，其他邊不變。

每個三角面穿過 cut 的邊數為 0 或 2；若為 2，它們恰是非 k 的兩條邊。
因此在 dual 上 `∂S` 是該 two-type system 的**若干完整 connected components 的聯集**：
每個是 alternating path 或 cycle。一次 primal move 可能同時選多條；內部洞也可
貢獻 cycles。checker 逐 move 對照 cut 的完整 edge set，而非只比較端點。

對應的 two-type system **整個無標號邊集合不變**，所以其 pairing 不變；另外
兩組 pairing 可變。以 AD swap 為例，`k=γ`，保留 `π₁₂`，可能改變 `π₁₃,π₂₃`。
這是指定 split 的保留性，不能當作全 Kempe class 的 invariant。

反過來任選一條 dual alternating path 翻轉，不能直接稱為「交換某個單一 primal
component」。要先恢復它所界定的區域／cut，核對需要交換哪些 components。

## 3. Pairing 已足以恢復 boundary connectivity，但不夠恢復其更新

固定 missing type k，取另兩種 type 的 dual paths。每條都是嵌入 disk 的 simple
proper arc；同一 system 中 paths 互不相交。terminal pair `(i,j)`（`i<j`）的指定一側
包含 boundary vertices `i+1,…,j`。

給每個 boundary vertex 記錄它對所有這些 arcs 的 side bit vector。兩個 boundary
vertices 的 bit vectors 相同，恰好表示它們屬於同一個 primal type-k component。

紙面理由：在每個三角形中，非 k 的兩條 dual 半邊分隔出 k-edge 的兩端與另一頂點；
沿此局部切割拼接，所得 regions 對應 primal type-k components。closed dual cycles
只能切出不接觸外 boundary 的 regions，不會再區分 boundary vertices。互不相交的
proper arcs 所形成的 boundary regions 正由上述 side vectors 決定。

一個 type-k component 只使用一個 coset `{a,a xor k}`；boundary w 加 anchor 決定
是哪個色對。因此 T 同時決定六種色對在 boundary 上的 component partition。
據此可列出所有 boundary-touching Kempe swaps 的 boundary 結果，特別是：

- 當前是否 forbidden singleton：**w 本身**就能判斷，毋須 pairings。
- 非 forbidden 狀態是否有一步 escape：**T 足夠判斷**。
- 換色後完整 T 是什麼、是否有兩步／三步 escape：**T 不足**（§5）。

checker 用實際 primal components 獨立核對 34,053 個 boundary partitions，
並將由 dual arcs 預測的一步 escape 與完整 Kempe BFS 比較。

### 五個 fibres 的共同必要條件，固定原 boundary 位置

全圖 `P(G)⊆{0,2}` 下，每個四色 fibre 的每個 extension 都必滿足以下 blockers。
表中顏色依該列明示的 normalized boundary；不是把不同 fibres 的 internal states
各自任意重命名後拼接。完整 forbidden component traces 存於證書 `boundary_obligations`。

| 重複位置 | boundary | 避免一步 forbidden singleton 的必要且充分條件 |
|---|---|---|
| 02 | ABACD | BC 1↔3，BD 1↔4 |
| 03 | ABCAD | CD 2↔4 |
| 13 | ABCBD | AC 0↔2 |
| 14 | ABCDB | AC 0↔2 |
| 24 | ABCDC | AD 0↔3 |

這個表只判斷**從當前四色染色出發的一步 safety**。由 §3 可逐項改寫為相應
missing-type system 的 boundary regions 相同。它沒有保證後繼染色仍滿足下一列。
已知 classwise counting 在全图假設下強迫同一 K 中五個 fibres 都非空；
需要的是該 K 中**所有**相關 extensions 的 safety，而非每個 fibre 任選一個安全代表。

## 4. 固定圖實驗與 survivor escape

使用既有三個 survivor、原 complementary 證書中的 120 個 Errera 刪點／D₅ controls，
以及原 catalogue 的 132 個 witnesses。總共 255 個標號圖實例，沒有生成新圖或重新
枚舉 catalogue。Errera 的不同對齊可同構，統計不代表互不同構的圖數。

其中 199 個實例是三角化 disk：3 survivors＋120 Errera＋76 catalogue witnesses。
其餘 56 個保留作 primal XOR controls；沒有偷偷補三角形。對一個特定染色做可延伸
的 triangulation 並不自動給出供整個 Kempe class 共用的同一 network，故不能用
coloring-dependent completion 支撐 H1。

| 檢查 | 數量 |
|---|---:|
| 完整染色 representatives（S₄ quotient，每個 boundary 用固定 canonical frame） | 12,301 |
| 實際單一 component swaps，逐邊核對 XOR 規則 | 118,690 |
| 三角化 disk 上逐 cut 核對 dual 規則 | 109,660 |
| 由 dual arcs 預測並用 primal 重算的 boundary partitions | 34,053 |

逐 move 的 before／after **使用相同 edge-type frame**。BFS 用 normalize 合併全域
色置換，但 survivor escape 在输出時把每一步的 named pair 轉回連續的原色框架；
不能拿 normalize 前後的 pairing 差直接當成實際變動。

三個 survivors 的全部五個 aligned 起始狀態同為

```
w   = (1,1,2,1,3)
π12 = ((0,3),(1,2))
π13 = ((0,4),(1,3))
π23 = ((2,4))
```

| survivor | 起始狀態數 | 最短 escape | 第一步 | 第一步 pairing 變動 |
|---|---:|---:|---|---|
| 590 | 1 | 3 | AD component containing 2 | 保留 π12；改變 π13、π23 |
| 811 | 2 | 2 | AD component containing 0,4 | 保留 π12；改變 π13、π23 |
| 891 | 2 | 2 | AD component containing 0,4 | 保留 π12；改變 π13、π23 |

590 第一步仍未到一步 escape 層；811／891 第一步已到一步 escape 層。
這些是既有完整立方體 survivor 的重新觀察，並非真正反例。

## 5. 決定性的不足見證：同圖、同 T，未來不同

### 5.1 T 本身

原 catalogue witness 1001，9 vertices，兩個 proper colorings

```
c = (0,1,2,1,3,0,1,2,2)
d = (0,1,2,1,3,0,3,2,2)
```

具有完全相同的 T：

```
w   = (1,3,3,2,3)
π12 = ((0,3))
π13 = ((0,1),(2,4))
π23 = ((1,2),(3,4))
```

但到 forbidden singleton `{1,3,4}` 的最短 Kempe 距離為 **2、3**。
這是本次 corpus 中保存的 distance-collision 見證之最少頂點數，非一般最小性定理。
此外 7-vertex witness 167 已有同 T 但 successor T 集合不同的見證，惟兩個起點
本身皆 forbidden singleton；因此更直接與 safety 相關的是上述 9-vertex 見證。

### 5.2 加 cycle counts 仍不足：固定 Errera 控制例

既有 16-vertex Errera disk（`errera-0`，與前輪 AB 證書同一邊表）中：

```
c = (0,1,0,2,3,2,3,0,3,1,3,1,1,2,2,0)
d = (0,1,0,2,3,3,2,0,2,1,2,1,1,3,3,0)
```

两者 boundary 同為 ABACD，T 同為 §4 的 survivor signature，三組 alternating
cycle 數也同為 **(0,0,2)**，但最短 escape 距離是 **3、2**，而且一步 successor T
集合不同。两者正由前輪指定的內部 CD component `{5,6,8,10,13,14}` 交換相連。
因此差異發生在**同圖、同 Kempe class、同 fibre、同 anchor**，不是比較不同圖或
相互不對齊的顏色造成的假象。

對指定 component 的 path/cycle 位置、與其他 systems 的 incidence，cycle **數目**
沒有保存。這否定 `T + 三組 cycle counts` 的 future sufficiency；没有否定包含完整
cycle embeddings／joint interfaces 的更精細 state。

| 發現 collision 的標號圖實例 | 數量（199 個 cubic controls 中） |
|---|---:|
| 同 T，escape distance 不同 | 105 |
| 同 T，一步 successor T 集合不同 | 173 |
| 同 T＋cycle counts，escape distance 不同 | 102 |
| 同 T＋cycle counts，一步 successor T 集合不同 | 122 |

這裡 successor 集合甚至忽略 action 名稱仍然不同，所以也否定更強的、逐 action
保持後繼狀態的等價性。cycle-enriched source 的比較使用 base T 後繼；base T 已不同，
enriched 後繼集合當然不可能相同。

這不排除 T 用作 sound overapproximation：將同 T 的所有具體後繼取聯集，仍可
包含每一條真實 transition。但這種聯集可能把不同 extensions 的選項接成虛假路徑，
因此不能把抽象可達性直接反推為同一具體染色的可達性。是否已足夠推出 forcing，
仍需另外論證；本輪否定的是精確的後繼充分性。

## 6. Polygon 與 H1–H5：保留什麼，還缺什麼

**H1 必須改寫量詞。** 是同一個 *uncoloured embedded 5-pole* 上的多個 edge
colourings、由精確 Kempe transitions 連在一起。五個 fibres 不是同一個染色的五套
同時存在的曲線。也不能只挑每個 fibre 一個 safe signature 而忽略 class 的其他 states。

**H2 仍是候選。** 本輪沒有證明某組 individually noncrossing pairings 不可共同實現。
T 已編碼 boundary 色對 connectivity，但並未保存三組曲線如何共享 edges、vertices
和 regions；§5 表明這些遺失資訊對 transition 有影響，值得精確補入。

**H3 需保留共同幾何。** 在固定三角化 disk、固定染色、同一 two-type system 內，
terminal path 確為 proper simple separator；這部分可以證。
不同 systems 的 paths 會共用 dual edges／vertices，不能直接當作互不相交的 chords。
不同染色的 paths 更不能只因疊畫後 crossing 就判矛盾。

**H4 尚無有限 cell 定理。** terminal 位於原 boundary **邊的內部**，不是原頂點；
切割會產生新的 interface positions。把任意長 alternating path 壓成一條有效 edge，
必須先指定兩側完整、對齊的 interface relation，以及何種 context 能讀取它。
所以 `C5→C3+C4` 不是由 dual path 自動得到的原圖分解公式。多個 systems 的重疊還
需額外切分／gluing 規則；本輪不宣稱辨認出完備的 C3/C4/C5 polygon grammar。

**H5 只有指定 split 的保留性，未找到全 move invariant。** boundary type 的奇數
parity、每組 pairing 的 noncrossing 都是共同必要條件，但本輪未由它們導出矛盾。
若 I 真正對完整 Kempe class 不變，它必須經過 AC、AD、BC、BD 的 cross moves；
不能只在 AB|CD cube 內驗證。

環形 propagation 可保留作語言設計方向，但外 boundary 長度 5 不代表掃描時的
active interface 寬度有固定上界。若未證可壓縮，`q₅=q₀` 只能是候選 closure 條件，
不能逕稱得到有限且充分的自動機。

## 7. 下一個有界入口與重播

**研究停在表示的充分性檢查。** 不擴大 catalogue、不繼續造 survivor。
下一輪最小入口是先分開 §5.2 的兩個 Errera states：保留三組 systems 的 shared
edge／region incidence，或每個 region 對其他 systems 的完整 interface relation；
先驗證能否區分這一對，再測是否仍存在同 state、不同 successor 的 collision。
這是下一輪方向，本輪沒有執行新的 polygon grammar 搜尋。

**直接接手的資料／函數**：

- 證書頂層 `same_class_regression`：兩個 Errera 完整染色、連接它們的 CD component、
  獨立有標號 BFS routes。邊表／面表取 `graphs` 中 `name="errera-0"` 的物件。
- `Dual.systems(c)`：三組 systems 的 components，逐項保留 terminal tuple 與 primal
  edge indices；可由此開始設計跨系統 incidence。edge indices 對應排序後的 `edges`。
- `Dual.state(c, cycles=False)`：本輪被否定的候選觀察量；`cycles=True` 加三組 cycle counts。
- `Dual.boundary_partition(c, missing)`：從另兩種 types 的 paths 讀出 boundary regions。
- `audit_graph(g)`：同圖按候選 state 分組，比較 escape distance 與原色框架的後繼 T 集合。
  新觀察量先區分固定見證，再重做 collision 檢查；沒有 collision 仍只是固定 corpus 的結果。

```bash
uv run --with networkx==3.5 python scripts/c5_edge_states.py --check
lake build
git diff --check
```

[checker](../scripts/c5_edge_states.py)／[證書](../artifacts/c5_cells/edge_states.json)。
證書保存 source／input hashes、255 個圖的邊表與可用的定向面、各 fibre 的 observed
signatures、五個 fibres 的禁止 component traces、各類 collision 見證，以及五條
survivor 最短 escape。三個 survivor 圖的**全部** moves 保存 compact rows（source
colouring、色對、component、target、原 frame 色映射、cut components、pairing 變動）。
其他 controls 逐 move 重播並保存 deterministic transition-trace hash；沒有把
109,660 次 dual checks 寫成 109,660 個獨立新證書。NetworkX 3.5 只恢復既有圖的
embedding，所有 cubic 輸入再以既有定向 disk 複形 checker 核對。
