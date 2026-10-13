# C5 組合、對稱與可實現關係圖譜

2026-10-13。本頁整理固定有序 C5 邊界的完整十 bit 關係，並以可重播程式建立
**1,023 個帶標號 mask／135 個 D5 類**的資料索引。單側 disk 已知實現為
132 個帶標號關係／24 類；必要條件後仍有 933、941 兩個 OPEN 類。
本圖譜不新增來源排除、不修改 Σ 定義，也不證明一般 `K∞=K≤5`。

互動入口：[完整分類圖譜](../artifacts/c5_combinatorial_atlas/index.html)。
資料入口：[atlas.json](../artifacts/c5_combinatorial_atlas/atlas.json)、
[135 類表](../artifacts/c5_combinatorial_atlas/classes.csv)、
[1,023 個原始 mask 表](../artifacts/c5_combinatorial_atlas/labelled_masks.csv)。
以下圖表及 HTML 均由同一個
[產生器／checker](../scripts/c5_combinatorial_atlas.py) 生成，沒有手工維護的第二份分類資料。

![C5 組合與實現篩選總覽](../artifacts/c5_combinatorial_atlas/overview.svg)

## 1. 對象與證據邊界

沿用 [cell 與 Σ 規格](c5_cell_enumerator.md#0-十-bit-mask-的規格specification與-bridge-驗證)：
有限簡單圖 G 有指定 disk 邊界 `B=(v₀,v₁,v₂,v₃,v₄)`，內點私有，允許內側 chords。
Σ(G) 記錄每個合法邊界染色的 S4 類是否至少有一個完整延伸，保留邊界位置。
bit 不記延伸數量，也不記各染色的 Kempe 分量或完整 fibres。

圖譜分成兩個不同問題：

- **單側 C5 disk relation**：研究一張 disk 圖的 Σ；目前已知 132 個關係、24 類。
- **separating C5 對齊交集**：兩張真實 disk 沿同一個有序 C5 黏合，關係為
  `Σ(G) & g·Σ(H)`。已知 132 個關係的全部相對 D5 對齊即可產生全部
  1,023 個非空 masks。這是兩側限制的結果，不是全部 masks 的單側實現證明。

「Kempe／exterior 通過」只標記必要條件；「known disk」必須連到具體圖 witness。
未通過必要条件的類，依紙面 soundness 論證排除；這些拓撲論證沒有因圖譜程式而新增 Lean 證明。
exterior 必要性使用四色定理（4CT），不能把此圖譜當作 4CT 的無循環證明。

當前研究已有 [十五內點界](c5_k15_sphere.md) `K≤15=K≤5`，其紙面、外部定理及
有限證書依原入口分層。本圖譜只重播既有小 witness 與關係分類，沒有重證該界。
933／941 的任意大小來源、`K≤16=K≤5` 及一般主命題保持 OPEN；後續停止點以
[Kempe 導覽](c5_kempe_guide.md) 為準。

## 2. 從 240 個染色到十個固定 bits

直接枚舉 `{0,1,2,3}⁵`，要求相鄰邊界頂點不同色，得到 240 個 proper colourings。
獨立的環染色公式也給

\[
P(C_5,4)=(4-1)^5-(4-1)=3^5-3=240.
\]

每個合法染色至少用三色，色重數只能為 `(2,2,1)` 或 `(2,1,1,1)`。
S4 對這些染色的 stabilizer 都只有恆等：用三色時剩下一個未用色，不能單獨交換它。
所以每個 S4 orbit 有 24 個帶色名染色，`240/24=10`。
checker 另外列出全部 24 個顏色置換，逐個核對其 orbit，而不是僅使用除法。

代表元取「從左至右首次出現的顏色依序改為 0、1、2、3」，再按字典序排序。
順序完全等於既有 `cells.json.pattern_order`；bit j 的權重為 `2ʲ`。

| bit j | 代表元 | 用色數 | 同色位置對 | 三色 singleton 位置 |
|---:|---|---:|---|---:|
| 0 | 01012 | 3 | 02、13 | 4 |
| 1 | 01021 | 3 | 02、14 | 3 |
| 2 | 01023 | 4 | 02 | — |
| 3 | 01201 | 3 | 03、14 | 2 |
| 4 | 01202 | 3 | 03、24 | 1 |
| 5 | 01203 | 4 | 03 | — |
| 6 | 01212 | 3 | 13、24 | 0 |
| 7 | 01213 | 4 | 13 | — |
| 8 | 01231 | 4 | 14 | — |
| 9 | 01232 | 4 | 24 | — |

`02` 表示 `{v₀,v₂}`；這些對在 C5 上的最短環距均為 2。
三色模式的 singleton 唯一決定其 S4 類；四色模式的唯一重複色位置對唯一決定其類。
若問題只問**一個邊界染色模式**，十個 S4 類再取 D5 商只有兩類：
三色 `(2,2,1)` 與四色 `(2,1,1,1)`。本圖譜的 135 類則是**模式集合／完整關係**的 D5 類，
兩種計數的對象不同。

全部三色集合 `T3=91`，全部四色集合 `T4=932`，全關係為 `1023`。
因此十 bit 子集合共 `2¹⁰=1,024` 個；去掉空關係 0，留下 1,023 個。
這是完整**組合空間**，尚未要求存在平面 disk witness。
若只按三色／四色模式數 `(a,b)` 分組，帶標號 mask 數為
`choose(5,a)·choose(5,b)`，但相同 `(a,b)` 通常不屬同一個 D5 類。

## 3. D5 作用、orbit 與 canonical 表示

以下名稱沿用 production enumerator 的 `r{a}s{s}`，`a∈{0,…,4}`，`s∈{0,1}`。
對 boundary word b，定義

\[
(g_{a,s}\cdot b)_i=b_{(-1)^s(i+a)\bmod5},
\]

再做 S4 首次出現正規化，得到十態中的另一個 bit。
下表每列的第 j 項就是 **舊 bit j 搬到的新 bit index**，不是逆置換。

| 轉換 | bit 0–9 的完整像 |
|---|---|
| r0s0 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| r1s0 | 1, 3, 8, 4, 6, 9, 0, 2, 5, 7 |
| r2s0 | 3, 4, 5, 6, 0, 7, 1, 8, 9, 2 |
| r3s0 | 4, 6, 9, 0, 1, 2, 3, 5, 7, 8 |
| r4s0 | 6, 0, 7, 1, 3, 8, 4, 9, 2, 5 |
| r0s1 | 4, 3, 5, 1, 0, 2, 6, 9, 8, 7 |
| r1s1 | 6, 4, 9, 3, 1, 8, 0, 7, 5, 2 |
| r2s1 | 0, 6, 7, 4, 3, 5, 1, 2, 9, 8 |
| r3s1 | 1, 0, 2, 6, 4, 9, 3, 8, 7, 5 |
| r4s1 | 3, 1, 8, 0, 6, 7, 4, 5, 2, 9 |

舊 Kempe screen 的 reflected action 使用 `b[(-i+a) mod5]`；相同實際轉換的名稱
需要把 reflected offset 改為 `−a mod5`。checker 核對完整置換，而不把名稱相同當作作用相同。

對非空 mask M，圖譜定義

\[
\mathcal O(M)=\{g\cdot M:g\in D_5\},\qquad
\operatorname{can}(M)=\min\mathcal O(M).
\]

每個 orbit 記錄全部帶標號 members、canonical representative 的完整 stabilizer，
以及 canonical 搬到各 member 的全部等價轉換；原始 mask 紀錄另保存搬回 canonical 的全部轉換。
轉換可能不唯一，全部保留。
orbit size 與 stabilizer order 滿足 `|O(M)|·|Stab(M)|=10`。

### 3.1 Burnside 的独立計數

十 bit 置換中，恆等有十個 cycles；每個非零旋轉有兩個 5-cycles；每個鏡射有
兩個 fixed bits 及四個 2-cycles，共六個 cycles。
一個置換固定的 bit 子集合必是其 cycles 的聯集，故有 `2^{cycle_count}` 個，扣掉空集即得：

\[
\#\text{非空 D5 類}
=\frac{1023+4(2^2-1)+5(2^6-1)}{10}
=\frac{1023+12+315}{10}=135.
\]

直接 orbit 枚舉與此值一致；含空集時則是 136 類。

| orbit size | stabilizer order | 非空類數 | 帶標號 masks |
|---:|---:|---:|---:|
| 1 | 10 | 3 | 3 |
| 5 | 2 | 60 | 300 |
| 10 | 1 | 72 | 720 |
| 合計 | — | 135 | 1,023 |

三个 size-1 類恰為 `T3=91`、`T4=932`、`T3∪T4=1023`。
兩種五態各自為 D5 的傳遞作用集合，非空全對稱 relation 必收某個完整五態集合。

### 3.2 Canonical key 只作索引，不能代替原 Σ

原始 132 個 catalogue keys、1,023 個 mask keys 及接合時的邊界次序全部保留。
圖譜另加 `canonical` 索引，沒有把 production Σ 改成對稱商。
必須先依實際接點搬運兩側，再計算原始 mask 交集；交集完成後才可為分類查 canonical。

具體已知 witness 的負控制：95 與 123 都屬 canonical 95 類，但在原有序框上

\[
95\cap123=91,\qquad
\operatorname{can}(95)\cap\operatorname{can}(123)=95.
\]

91 與 95 屬不同類。把兩側各自正規化會改變接合結果，連交集的對稱類都不能保存。
相同問題也適用於包含、聯集和任何指定位置的 boundary forcing。

## 4. 必要條件、排除與 witness 狀態

產生器讀取原始程式與保存 artifacts，重算完整 relation 清單，再逐項比較舊證書。
沒有把文件中的預期數字當成驗證結果。

| 階段 | 帶標號 masks | D5 類 | 意義 |
|---|---:|---:|---|
| 全部非空組合 | 1,023 | 135 | 尚未要求 disk 來源 |
| 平面 Kempe 必要條件通過 | 153 | 29 | 每個 allowed pattern／split 各存在合法 swap orbit |
| 再通過已知 exterior 接合必要條件 | 142 | 26 | 與全部已知、已對齊外側關係非空相交；使用 4CT |
| 既有 k≤5 witness | 132 | 24 | 每個原始 mask 都有具體單側 disk 圖證據 |
| 前兩種必要條件通過、未有 witness | 10 | 2 | 933／941；一般來源 OPEN |

最後一步 `142 → 132` 是「取已有 witness 的子集」，不是另一個已證必要條件篩選。
如果假設尚未證明的 adjacent-singleton lemma，才可條件式排除剩下十個 masks；
圖譜不把這項假設轉成既有實現／排除狀態。

全部 135 類分為：106 類 Kempe 拒絕、3 類 exterior 拒絕、24 類 known disk、2 類 OPEN。
exterior 拒絕的 11 個 masks 分成 canonical 7、63、932 三類；932 的外側反證是
wheel relation 91，兩者交集為空。

Kempe screen 的每份拒絕證據保留具體 pattern、complementary split 及全部可選
noncrossing swap-orbit masks。通过並不表示不同 split 的抽象 partitions 能同時來自
同一張圖或同一次完整染色。詳見 [screen 紙面條件](c5_kempe_screen.md)。
exterior 拒絕保留一個實際已知外側 key 及其圖 witness；兩側固定標號先對齊再交集。

### 4.1 已知 24 類與最小已知內點數

自動生成的 [24 類與最小已知 k 表](../artifacts/c5_combinatorial_atlas/known_classes.md)
列出每類的 canonical、orbit size、三色／四色模式數、最小已知內點數及證據來源。
其 k 是該 orbit 在**目前保存 catalogue witnesses 中**的最小 `k_eff`。
它不是圖譜新證明的任意來源最小性下界；每個 class 的原帶標號 members
仍各連到自己的原始 witness edges、原始 key 與獨立重驗結果。

known 類的 orbit histogram 是 size 1：2 類、size 5：18 類、size 10：4 類，
帶標號總數 `2+18·5+4·10=132`。
對 132 份保存圖，checker 重新加入框的五條邊，逐邊驗證 proper coloring，
以完整回溯覆蓋 `4^{k_eff}` 個內點指派（不相容前綴剪枝），重算完整十 bit Σ；
十列各保存精確 fibre count（包括零）及非空列的一份字面 full lift。
另用 NetworkX 的
boundary-apex planarity 測試確認指定框可暴露為 disk 邊界。
沒有重跑 cell graph DFS，也沒有改寫原 witness／proof artifacts。

## 5. 統一结构紀錄與比較方式

每個 class 的資料包含 canonical 與全部 orbit members、allowed／forbidden pattern indices、
三色／四色數、orbit size、stabilizer、等價轉換、必要條件結果、拒絕證據或
known witness 來源，以及最小已知 k。每個原帶標號 mask 有唯一 class 指向，
可回查原 Σ、具體證據與接合對齊。

額外特徵均是可重算的描述，不預設為可實現性判準：

- **同色位置與距離**：每個模式列出全部同色 pairs；三色記 singleton support P，
  四色記唯一重複色 chord pair。P 的大小、原框上的相鄰 pair 數及距離分布可比較。
- **共同 forcing**：對五個非相鄰 boundary pairs，列出所有 allowed patterns 是否均同色、
  均異色或兩者皆有；這是關係本身的共同限制，不能推出某條原圖邊實際存在。
- **chord-compatible**：若所有 allowed patterns 都使 uv 異色，則 uv 通過單邊
  染色相容測試。這不表示 uv 在 witness 中，也不證明一條 uv 能在該 witness 的
  指定 disk embedding 中加入，更不保證多條 chords 能同時平面加入。
  T4 全收時五條 chords 均不相容，任何實際單側 witness 的 C5 必無 chord。
- **集合關係**：包含、交集、聯集先在相同有序框的 raw masks 上計算；
  class 間比較列出實際 members／D5 對齊，不用各自 canonical 代表的交集充當所有對齊。
- **圖結構指紋**：保存 witness 的原 attachments、內部邊數、分量及 degree 等資訊，
  對相同 relation 類做描述性比較。這些只代表保存圖，沒有聲稱任意實現具有相同骨架。
- **Kempe 特徵**：記錄既有三種 split 的必要 obligations 及其可選交換結果；
  沒有把抽象選項當作保存 witness 的實際 Kempe 分量。
- **投影階數**：將 allowed S4 states 展開色名，在固定四色色盤的全部 `4⁵` 個
  boundary assignments 上比較各階完整 projections，
  找出重建該 relation 所需的最小階數；這是有限關係特徵，不是 disk 可實現性判準。
  已知132個原 keys 的2／4／5階數分布為11／101／20，與
  [來源階數報告](c5_relation_arity.md)一致。

`interior_skeleton_key` 以內點數和內部誘導圖的邊碼表示無標號 private graph；
每份 k≤5 witness 枚舉全部 k! 個內點置換（最多120個）後取最小邊碼。
它保留內部誘導圖的孤立點，但不編入 boundary attachments 或 chords；
這些仍以原始頂點／邊完整保存在 witness 紀錄。
`witness_internal_shape_groups` 列出共用這個 key 的原 masks 及 D5 類。

目前132份保存圖共有12種 private skeleton；每個已知 D5 類的**已選 witness**
具有相同內部骨架。相同骨架卻可以對應不同關係：內部 triangle（key `3:7`）
對應231、429、935、943等類；零內點（key `0:0`）對應165、431、1023。
這顯示框附件／chords仍決定完整Σ，不能由private skeleton單獨判定relation。
上述共同骨架只是這批已選圖的觀察，沒有斷言同一Σ的全部實現必有相同內部圖。

### 5.1 兩個 OPEN 類與已知類的差別

| 類 | allowed 三色／四色數 | canonical 的 P | orbit／stabilizer order | 實現狀態 |
|---:|---|---|---|---|
| 933 | 1／5 | {4} | 5／2 | 通過必要 screen；未知 disk witness |
| 941 | 2／5 | {2,4}，非相鄰 | 5／2 | 通過必要 screen；未知 disk witness |
| 935 | 2／5 | {3,4}，相鄰 | 5／2 | 已知 k=3 witness |
| 943 | 3／5 | {2,3,4} | 5／2 | 已知 k=3 witness |
| 951 | 3／5 | {1,3,4} | 5／2 | 已知 k=5 witness |
| 959 | 4／5 | {1,2,3,4} | 5／2 | 已知 k=2 witness |
| 1023 | 5／5 | 全部框點 | 1／10 | C5 本身，k=0 |
| 429 | 2／4 | {2,4}，非相鄰 | 5／2 | 已知 k=3 witness；未全收 T4 |

933 的 members 為 `933, 934, 940, 948, 996`；941 的 members 為
`941, 949, 950, 998, 1004`。兩類均全收 T4，但三色 support 是非空獨立集。
已知全收 T4 的五類均具有相鄰 singleton pair；這是有限 catalogue 上的觀察。
429 表明若拿掉 T4 全收前提，不相鄰二點 support 可以由 disk 實現。

「全收 T4 的任意 disk 都有相鄰 singleton pair」正是既有未證
[adjacent-singleton lemma](c5_kempe_screen.md#4-c5-adjacent-singleton-problemunproved)。
兩個 OPEN 類是這個命題的候選來源關係，不是已構造的反例。
它們的內部圖結構目前無 witness 可比較；能比較的是完整邊界 relation 和必要條件。
[抽象計數向量](c5_adjacent_singleton_counts.md) 與
[循環流分解](c5_circulation.md) 也不能代替同一張圖的實現證据。

### 5.2 可反駁的分類問題

「singleton support P 決定 relation」已被已知 95、127 等同 P、不同 relation 的
保存 witnesses 反駁。「三色／四色數決定 D5 類」也被 127／223、189／231 反駁。
因此這些粗特徵只用來索引與比較。

後續若猜想某個組合特徵決定內部結構，應先精確列出特徵、圖類及欲強迫的結構，
搜尋相同特徵而不同保存骨架的負控制，並在具名圖上重算完整 Σ。
要驗證 adjacent-singleton lemma，則須給出任意大小同圖證明，或構造完整 Σ 為
933／941 某個 member 的平面 disk 圖並獨立驗證；只提供 partitions 或計數向量不足。
本次不採納新的普遍結構猜想，也不增加 OPEN 類的排除數。

## 6. 五種圖譜與資料流

互動圖譜的各視圖共用 atlas 資料：

1. **Combination Map**：1,023 个帶標號 mask 的唯一 orbit 歸屬，按三色／四色數及 class 篩選。
2. **Symmetry Map**：十個轉換、bit 置換、orbit members 與搬到 canonical 的全部轉換。
3. **Screening Map**：1,023 → 153 → 142，另標示其中 132 已知／10 OPEN；
   同時顯示 135 → 29 → 26 → 24+2 的 D5 計數。
4. **Realization Map**：24 個 known disk 類的最小已知 k、全部原 key 的 witness，及兩個 OPEN 類。
5. **Structure Comparison**：模式限制、support／forcing、對稱性與保存 witness 指紋；
   比較接合時列出 raw masks 及相對 D5 轉換。

[overview.svg](../artifacts/c5_combinatorial_atlas/overview.svg) 為可嵌入既有 research atlas
的總覽入口，HTML 提供完整展開與比較。CSV 適合外部分析；JSON 是生成資料，
權威輸入仍是現有程式及原研究 artifacts。修改輸入後必須重新生成並核對，不能只手改圖表。

## 7. 重播、來源與核對範圍

由 repository root 執行；使用 [requirements.txt](../requirements.txt) 的固定版本環境
（本次倉庫 `.venv` 已可用，NetworkX 為 3.5）。新 checkout 可先以
`python3 -m venv .venv` 及 `.venv/bin/python -m pip install -r requirements.txt` 建立環境：

```bash
.venv/bin/python scripts/c5_combinatorial_atlas.py --write
.venv/bin/python scripts/c5_combinatorial_atlas.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_combinatorial_atlas.py --check
.venv/bin/python scripts/c5_kempe_screen.py --check
.venv/bin/python scripts/c5_cell_enumerator.py --check
python3 scripts/check_docs.py
git diff --check
```

新 checkout 尚未建立 `.venv` 時，可用既有依賴 pin 直接重播：

```bash
uv run --with networkx==3.5 python scripts/c5_combinatorial_atlas.py --write
uv run --with networkx==3.5 python scripts/c5_combinatorial_atlas.py --check
```

`--write` 只寫新的圖譜目錄；`--check` 重新計算並比對生成產物。
來源 paths／SHA-256 見
[source_manifest.json](../artifacts/c5_combinatorial_atlas/source_manifest.json)，
逐項結果見 [verification.json](../artifacts/c5_combinatorial_atlas/verification.json)。
固定來源為 [GitHub repository](https://github.com/raylei50653/math) main
`acd2b1beea6c909edade565a00eeeeac05d2b3a7` 的程式與 artifacts；本次已即時核對
遠端 main 與此來源 SHA 一致。此 SHA 只記此次來源版本，不宣稱未來 main 永遠停在此處。

| 權威輸入／路由 | 用途 |
|---|---|
| [cells.json](../artifacts/c5_cells/cells.json) | 十態順序、132 個原始 keys、literal witness edges 與 k_eff |
| [cell enumerator](../scripts/c5_cell_enumerator.py) | 既有 D5／Σ 約定；圖譜不改寫 enumerator |
| [view generator](../scripts/c5_combinatorial_atlas_views.py) | 由同一 atlas 資料產生 HTML 與 SVG |
| [Kempe screen](../scripts/c5_kempe_screen.py)、[原證書](../artifacts/c5_cells/kempe_screen.json) | 重算必要 obligations、完整153／142／10清單及拒絕證據 |
| [edge-pair 座標](c5_edge_pair_coordinates.md)、[程式](../scripts/c5_edge_pair_coordinates.py)、[證書](../artifacts/c5_cells/edge_pair_coordinates.json) | 二十條獨立有限判準與 screen 結果相符 |
| [雙側與 Σ 定義](c5_cell_enumerator.md)、[主命題](c5_boundary_relations.md) | 保留原邊界接合語義與一般 OPEN 身份 |

完成核對以 verification 及實際命令 exit status 為準，包含：

- [x] 240 proper colourings、全部 S4 作用及十個完整 orbits 重算。
- [x] 1,023 个非空 masks 恰好分到一個 D5 orbit；Burnside 與直接枚舉一致。
- [x] 全部群置換的合成、旋轉／鏡射封閉、orbit-stabilizer 與 canonical 冪等成立。
- [x] Kempe／exterior 的全清單與原 artifacts 相符，而非只比對總數。
- [x] 全部132個原 keys 各有圖譜紀錄、原 witness、apex-planarity及暴力完整Σ重驗。
- [x] 對齊交集覆蓋全部1,023個非空 masks；已知95／123負控制保留。
- [x] 圖譜生成前後來源 artifacts hashes 保持不變。
- [x] 正常及 hashseed17 的完整生成產物 byte replay 相同。

另在隔離暫存目錄只放來源 main 的六份原始輸入與兩支新產生器，
重生八份圖譜檔案，全部與工作目錄產物逐 byte 一致。沒有依賴其他本機研究 artifacts。
文件連結、正式 docs 範圍 DocGraph、`git diff --check` 與既有 `lake build` 均通過。
全工作樹 DocGraph 仍因 audits／scratch 保存快照的 62 個既有重複 ID 失敗；
本次未改動其 metadata 或凍結檔案。瀏覽器實測圖譜查詢、計數篩選、原框搬運及手機版面，
沒有 JavaScript page／console errors。

未新增 Lean 模組；若執行 `lake build`，只屬既有 Lean 回歸，不能視為本圖譜
的 disk／Kempe 拓撲證明。本頁的計數是有限枚舉與群作用的核對，必要性、已有
一般紙面结果及未解命題保留各自證據層。本次整理與驗證記錄見
[歷史紀錄](history/2026-10-13-c5-combinatorial-atlas.md)。
