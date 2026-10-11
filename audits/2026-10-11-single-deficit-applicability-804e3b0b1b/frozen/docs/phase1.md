# 五邊界染色狀態：第一階段

本階段限於定義、有限枚舉、反例及 composition 契約。不假設 boundary-state conjecture，不證明四色定理，不把有限範圍的無反例結果外推。

後續更新：[反例構造續篇](construction.md) 找到 11 頂點、26 邊的 induced-C5 planar BAD；仍不是 BAD disk patch。以下 n≤6 結果保留原搜尋範圍。

## 語意與信任分類

`Color = Fin 4`，有序邊界為 injection `Fin k ↪ Fin n`。`Col4` 是 proper coloring 的 subtype，`restrictionMap` 是限制映射，`SigmaAt` 是其 image；`Sigma` 是 k=5 的存在量詞版本。`sigma_is_image` 連接兩者。指定 C5 可以有 chord；「induced C5」及「C5 是同一個面的邊界」是額外條件。

所有結論採以下分類：

| 類別 | 本專案的意義 |
| --- | --- |
| proved in Lean | 具名 theorem，無 `sorry`，無手寫 boundary conjecture 或四色定理公理。大型有限檢查使用 `native_decide`：此工具鏈產生具名的 `...native_decide.ax_...` 計算公理，因此額外信任 Lean 原生編譯；不宣稱全是 kernel reduction。 |
| computationally observed | Python/NetworkX 搜尋的平面性、同面性、範圍統計與結構條件測試。不能當成 Lean 平面性定理。 |
| conjectured | 尚待提出及驗證的 relevant-patch 生成文法、較小的 quotient、變動邊界 transition 規則。本階段沒有將其當前提。 |

## C5 枚舉

Lean 的 `Enumeration.lean` 分別檢查 cardinality、orbit 覆蓋、orbit 互斥及 representative 的 base-4 code 最小性。D5 定義為 C5 在五個位置上的 adjacency-preserving permutations，具有群運算、逆、染色作用及作用律，並計算其大小為 10。

| 項目 | 結果 |
| --- | ---: |
| labeled proper 4-colorings | 240 |
| S4 color orbits | 10 |
| 再容許 D5 位置作用 | 2 |

顏色 orbit canonical representatives，依 lexicographic order：

```text
01012  01021  01023  01201  01202
01203  01212  01213  01231  01232
```

完整 S4 × D5 representatives 是 `01012`、`01023`。這是計算輸出，不是預設。前述十類中五類用三色、五類用四色。

## 原始 Σ 與安全壓縮

搜尋證書同時保存完整 labeled Σ 與 240-bit mask。bit i 對應 `summary.json` 的 `c5.raw_bit_order[i]`，即 proper tuples 的 lexicographic order；十六進位字串最低位是 bit 0。Lean 的 `RawState` 是 240 個合法 labeled assignments 上的 Boolean function，`raw_intersection` 驗證逐 bit AND 的語意。

當兩個 interior 互不相交、只共用同一個有序 boundary，組合就是 relation intersection。`independent_gluing` 證明對任意兩個 interior-extension relations 的存在量詞黏合法則。此式不適用於還有其他共享內部頂點的情形；`sigma_union_same_vertices` 只說同一個完整 coloring 同時滿足兩張圖，並不誤稱一般 Σ 的 intersection 等式。

在**沒有預染色、list-color constraints、指定顏色意義**的模型中，全體 Σ 對 S4 封閉（`sigma_color_invariant`）。因此十個固定位置的顏色 orbit 可以做無損壓縮：

* `color_abstraction_exact`：對 proper 且 S4-saturated 的 Σ，decode(encode(Σ)) = Σ。
* `abstract_intersection`：encode(s ∩ t) = encode(s) ∩ encode(t)。
* `color_state_count`：十個 orbit 的所有子集共 1024 個，包括 empty state；不是說全部可由 planar patches 實現。

這裡保留 boundary labels；不同位置的相等模式仍是不同 bit。這個 S4 壓縮並未獨立選取兩邊的某個完整 coloring。D5 會置換邊界位置，不能對兩側各自忘掉位置後直接交集。若對**整個 state**用 D5 canonicalize，仍須攜帶相對 boundary permutation。個別 coloring 的兩類 orbit 也不等於只有兩個 patch states。

## 有限反例搜尋

範圍：n=5,6；頂點為 0..n−1，B=(0,1,2,3,4)，枚舉包含 C5 五條邊的每個 simple labelled graph，允許 disconnected graphs、chords。沒有把 isomorphic labelled copies 去重，因此計數不是同構類數。

| n | 所有候選 | NetworkX 判 planar | BAD |
| --- | ---: | ---: | ---: |
| 5 | 32 | 31 | 10 |
| 6 | 1024 | 852 | 240 |
| 合計 | 1056 | 883 | 250 |

所有 250 個 BAD 候選均輸出 deterministic JSON certificate，含 edges、ordered B、完整 Σ、240-bit mask、orbit representatives、rotation system、faces、SHA-256。hash 僅確保資料一致，不提供數學信任。

`export_certificates.py` 將 graph 與完整 Σ 轉成閉合 Lean 資料。`checkCertificate` 重新枚舉**全部** 4^n colorings，檢查 edge validity、C5 boundary、Σ 的相等及 BAD；不採用搜尋器給的 witness 作為否定性結論。`checker_sound` 把 checker 通過連到數學定義 BAD。JSON 的 rotation/face 與 NetworkX planarity 結論目前不提升為 Lean 平面性定理。

## 最小 BAD（不是 disk patch）

以頂點數優先、再邊數最小，並固定保留 boundary C5，得到：

```text
V = {0,1,2,3,4}, B = (0,1,2,3,4)
E = {01,02,03,04,12,13,23,34}
Σ = S4·01231 ∪ S4·01232
|Σ| = 48
```

其 boundary color orbits 是 `01231`、`01232`；若把個別 coloring 再允許 D5，代表是 `01023`（此 canonical representative 不必屬於原圖的 Σ，因為 D5 改變位置）。Lean 驗證 exact Σ、BAD、boundary 及 n=5 時少於 8 邊的所有 C5-supergraphs 均 GOOD。Boundary injection 證明至少要五個頂點。這是此 C5-supergraph 問題的 **lexicographic (n,m) 最小性**，不宣稱任意頂點數下獨立最少邊的另一種最小性。

圖含 K4[0,1,2,3]，所以這四個 boundary vertices 必須四個異色；頂點 4 鄰接 0、3，只能重用 1 或 2 的顏色。這說明兩個 S4-orbits。圖可畫成 planar，但 C5 不 cofacial；不存在以這個 C5 作為外面的 disk embedding。不能把此結果當成 planar disk patch 的 BAD 反例。

與「刪去四色最小反例中的一個 degree-5 頂點」相比，它未滿足必要的來源條件：

* 這個 C5 不是面邊界。補上一個鄰接全部 B 的中心後，頂點 {0,1,2,3,center} 形成 K5，無法是該平面來源。
* Boundary degrees 是 (4,3,3,4,2)，補回中心後仍有頂點 degree < 5。
* 它有 boundary chords、2-vertex cut {0,3}；不能被當成 internally 6-connected triangulation 的最小反例本身。圖的整體連通條件應套在補回中心的來源圖，不能不加區分地套在刪點 patch。

最小反例的結構背景參考 Robertson–Sanders–Seymour–Thomas 的原始論文 [The Four-Colour Theorem](https://thomas.math.gatech.edu/PAP/fc.pdf)。此引用僅供 constraints 的背景，不是枚舉或 Lean 證明的依賴。

## 逐項條件實驗

下表是**依序累積**條件；計數屬 computationally observed。cofacial 以「加入鄰接 B 的 apex 後仍 planar」作演算法測試。未把這個測試與 disk embedding 的拓撲等價性形式化。

| 新增條件 | 剩餘圖 | BAD |
| --- | ---: | ---: |
| planar 且含指定 C5 | 883 | 250 |
| C5 cofacial | 223 | 0 |
| C5 induced | 33 | 0 |
| 非 boundary 頂點 degree ≥ 5 | 2 | 0 |
| boundary 頂點 degree ≥ 4 | 0 | 0 |
| 補回 apex 是 triangulation | 0 | 0 |
| 補回 apex 的 vertex connectivity ≥ 5 | 0 | 0 |

在此範圍，第一個 cofacial 條件就排除全部 BAD。其後的零不能算額外成功，尤其空樣本不是證據。induced C5 是候選 filter；這裡不宣稱它對任意所謂「relevant patch」必然成立。5-connectivity 也不是 internally 6-connected 的完整定義。`summary.json` 另有各條件獨立套用的計數，避免順序掩蓋結果。

本階段沒有發現 BAD disk patch，也沒有證明所有 disk patches GOOD。若 C5 確實是 disk boundary，加入一個共鄰接中心仍 planar；GOOD 正是中心可再染色的延伸條件。這說明無界的 disk-BAD 搜尋與四色问题有關，而不是可以先假設無反例的簡化條件。不得將已知四色定理餵進搜尋器當剪枝 oracle。

## composition 反例及 transition 邊界

令 L = C5 + {02}，R = C5 + {03,13}；兩者各自都有 disk embedding，且 GOOD。兩者的個別 coloring orbit 摘要均是 {三色類, 四色類}，但

```text
Σ(L) ∩ Σ(L)  是 GOOD
Σ(L) ∩ Σ(R)  = 上述 48 個 coloring，是 BAD
```

`coarse_equal`、`coarse_not_congruent`、`glued_bad` 機械驗證這個反例。因此「只記出現哪些 S4×D5 coloring 類」不是 aligned gluing 的 congruence。這不排除攜帶 alignment 的其他 quotient，也不排除對整個 state 的更細 quotient。

只把 transition 定義為 s ↦ s∩p 時，狀態只能縮小，且 BAD 不可能因此產生新的三色 assignment（`intersection_cannot_repair`、`intersection_step_decreases`）。`intersection_scc_singleton` 進一步證明任意允許元件集下，這種 transition 的 SCC 不含兩個不同 exact states。它並未指定哪些 singleton 是 closed。這種 transition 無法表達期待的「修復到 GOOD」。加入黏合元件也未必保持指定外邊界仍是 disk boundary：L 與 R 就說明這一點。

下一階段應先指定保留 disk/source constraints 的生成操作，以及 boundary relabel/forget/introduce 或替換操作的精確語意，再檢查是否能在固定 5-boundary 上封閉。現在的 1024-state 上界只對固定 interface 成立，沒有證明任意 relevant planar patches 都有不增加 frontier 的建構方式。尚未定義這些 transition guards，所以不宣稱已排除不通往 GOOD 的 closed SCC。

## 重現

```bash
uv run --with networkx==3.5 python scripts/search_boundary.py
python3 scripts/export_certificates.py
lake build
uv run --with networkx==3.5 python scripts/check_search.py
lake env lean Math/Audit.lean
```

工具鏈及 mathlib revision 由專案既有 `lean-toolchain`、`lake-manifest.json` 鎖定。搜尋器預設完整枚舉 n≤6；提高 `--max-n` 是新的、更大搜尋，不能沿用此報告的範圍統計。

2026-09-11 驗證：`lake build`、250 份證書的獨立 full-colouring replay 及 `Math/Audit.lean` 均通過。實際 axiom dependencies 保存於 [lean-audit.txt](../artifacts/boundary/lean-audit.txt)。`checker_sound` 不依賴 native 計算公理；`all_certificates_bad` 依賴批次 checker 的 native 計算公理。無損色彩壓縮的 exactness 使用已計算的 orbit coverage，所以同樣有此依賴；intersection homomorphism 與 intersection-only SCC 單點性則沒有。
