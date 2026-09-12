# Finite-state synthesis of triangle disk gadgets

2026-09-12 topology completeness 續作見 [topology_completeness.md](topology_completeness.md)。annulus 切割與端點環序的紙上論證已落盤；`AttachmentEndpoints.lean` 已證環序到 `AnnulusAccept` 的編譯步驟。一般 embedding 到該環序尚未 Lean 化，原 topology 信任邊界不變。

2026-09-11。延續 [gadgets.md](gadgets.md) 的固定 grammar：

```text
有序 C5 (0..4) + 內部 K3 (5,6,7) + 任意 boundary-to-K3 attachments
```

一個 component 是長度 5 的字：第 i 個字母 `S_i ⊆ {5,6,7}` 是 boundary vertex i 接到的內部頂點（8 個字母，mask bit `3i+(v−5)`）。8⁵ = 32,768 個字就是整個 grammar。本階段把染色語意與平面接線語意都寫成沿邊界掃描的確定性自動機，核心問題是：

> 在這個 grammar 中，color semantics × planar routing semantics 的最小 behavioral state 到底是什麼？

不使用四色定理、boundary-state conjecture 或任何 SAT 黑盒。**所有 finite-state 結論只限這個 triangle grammar，不外推到 arbitrary planar disk patches。**

## 信任分類

* **proved in Lean（無 native）**：`ColorDFA` 的 state invariant、transition correctness、terminal acceptance ⇔ K3 可取三個互異色、對每一個 attachment word 的 exact `Sigma` 語意，以及與 `splitSigma` checker、十-bit `abstractColors` 的對接（`Math/ColorDFA.lean`）。`GeometryDFA` 的搜尋完備性（`geoAccept ↔ AnnulusAccept`）、mask 枚舉的雙射性。`HallTriangle` 的 `k3_uncolorable_iff`（Mathlib Hall）與 `reject_iff_hall`：三色 pattern 的拒絕 ⇔ 兩個具名 Hall witness 之一。
* **proved in Lean（native_decide）**：對全部 32,768 個 mask，geometry 自動機接受 ⇒ 其自建 rotation system 通過 Euler／face-traversal checker 且 C5 為一個 face；接受數 7,194；disk-accepted words 的三色 profile 統計；42 份 library 證書與自動機預測一致（`Math/GeometryDFA.lean`、`Math/AutomataReplay.lean`）。
* **computationally observed**：geometry acceptance 與 NetworkX apex-planarity 測試逐字一致；Nerode 最小狀態數；42 個 disk states 的分佈；1,080 個 T4 ordered realizations；Z5 profile 統計（`artifacts/automata/`）。
* **conjectured / unresolved**：geometry 自動機的 completeness（拒絕 ⇒ 不存在 disk embedding）；「rotation system 球面 + C5 facial ⇒ disk embedding」是標準組合拓撲，本專案未在 Lean 內證明；Z5 完整結構界（低 degree 分支與四型 reduction 已證，見末段）；其他 grammar。

## ColorDFA：exact boundary-coloring semantics 的有限狀態化

固定一個 boundary pattern `b`。狀態是三個內部頂點的禁用色集合 `(F5,F6,F7)`；讀到位置 i、顏色 `b i`，就把 `b i` 加進 `S_i` 中頂點的禁用集。終止接受 ⇔ 存在 injective `t : Fin 3 → Color` 且 `t k ∉ F k`。

Lean 中的定理（皆為普通證明）：

| 定理 | 內容 |
| --- | --- |
| `runFrom_spec` | state invariant：讀完位置清單 `l` 後 `F k = image b (l ∩ links k)` |
| `run_spec` | 讀完全部五個位置後 `F k = image b (links k)` |
| `accept_iff_triangleCan` | 終止接受 ⇔ `TriangleCan links b` |
| `proper_triangle` | compiled graph 的 proper colouring ⇔ C5 proper ∧ K3 injective ∧ 每條 attachment 分色 |
| `mem_sigma_triangle` | 對**每一個** links，`b ∈ Sigma ↔ Proper C5 b ∧ TriangleCan links b`；取代原先只對兩組 links 的 `native_decide` 檢查 `compiled_meaning` |
| `sigma_iff_accept`、`splitSigma_triangle` | 自動機與 `Sigma`／`splitSigma` checker 完全一致 |
| `acceptedReps_exact` | 自動機的十-bit 輸出 = `abstractColors (splitSigma …)`，接上 `State.lean` 的無損壓縮 |

`Math/AutomataReplay.lean` 以 `native_decide` 驗證 42 份 library 證書：每份的邊集恰是 compiled word、儲存的 exact Σ 的 `abstractColors` 等於自動機預測、且 word 被 geometry 自動機接受。

## GeometryDFA：annulus 非交叉的 forward certificate

C5 在外、K3 在內，attachments 是 annulus 裡的弦。一個 run 是三角形定向 `o ∈ {id, mirror}` 加每個 boundary vertex 的 fan rotation；沿 C5 走一圈時弦的內端點在三角形上的 cyclic winding 必須是 0 或 3。`AnnulusAccept w := ∃ run, winding ∈ {0,3}`；`geoRun` 只搜尋 `Π max(1,|S_i|)` 個有效 rotation，`geoAccept_iff` 證明這與全稱定義等價。

接受端 certificate：`rotationOf w run` 由 winding sequence 決定性產生 rotation system——

* boundary vertex i：`[i−1, i+1] ++ fan 反序`；
* interior vertex k：其 outer fan 依（block-aligned）sequence 順序，再接三角形上的下一、上一頂點。

`checkRotation edges rot` 是純組合檢查：rotation 恰列出鄰居、無重複；face traversal（dart `(u,v)` 之後接 `(v, succ_v u)`）的 face 數滿足每個連通分量 `V − E + F = 2`；某個 face 的 dart 集恰是 C5（任一方向）。

`accepted_masks_have_rotation`（native_decide，32,768 個 mask）：`geoRun w = some run → checkRotation … = true`；`accept_certificate` 把它寫成 `AnnulusAccept w → ∃ run, RunOK ∧ checkRotation = true`。

**只主張 forward soundness。** 「球面 rotation system 且 C5 facial ⇒ 存在以 C5 為外邊界的 disk embedding」是標準事實（Edmonds／Mohar–Thomassen），與 §6 的 Jordan 障礙一樣屬於拓撲背景，不是 Lean theorem。反方向（自動機拒絕 ⇒ 不能 disk）**沒有證明**；`accepted_count = 7194` 與 `scripts/check_automata.py` 的 apex-planarity 對照逐字一致，只是完整有限枚舉觀察，不因此提升為 completeness。

## 計算結果（`artifacts/automata/summary.json`）

| 項目 | 結果 |
| --- | ---: |
| 字（attachment sets） | 32,768 |
| geometry 自動機接受 = apex-planar | 7,194（0 個不一致） |
| ColorDFA Σ bits = 暴力枚舉 | 32,768（0 個不一致） |
| distinct disk states | 42 |
| T4 state pairs / ordered mask pairs | 10 / 1,080 |

Nerode 最小化（每層狀態數，layer 0..5）：

| 輸出函數 | 狀態數 |
| --- | --- |
| geometry only（disk?） | `[1, 8, 30, 39, 18, 2]` |
| colour only（exact Σ，不 gate） | `[1, 8, 64, 462, 1940, 273]` |
| Moore：disk? × exact Σ | `[1, 8, 58, 234, 261, 43]` |
| three-colour part, disk-gated | `[1, 8, 58, 207, 165, 22]` |
| single-component BAD language | `[1, 1, 1, 1, 1, 1]`（空語言） |
| 未最小化 product（geometry state set × 10 個 forbidden triples） | `[1, 8, 64, 512, 4096, 32768]`；只留 geometry 仍活的 `[1, 8, 63, 415, 1916, 7194]` |

兩 component 同步、目標 `Σ_L ∩ Σ_R = T4` 的 pair machine：`[1, 37, 469, 613, 73, 2]`；各層可接移動 36/64、468/2304、756/29952、792/39168、108/4608。第 2 層起平均每個活狀態不到兩個可接 `(S_i^L, S_i^R)`。

`nerode_*.json` 保留完整 mapping：每層 `prefix_classes`（base-8 prefix 索引 → class id）、每個 class 的 representative prefix、transition row、以及它合併的未最小化 product states（`raw_states`）。`nerode_pair.json` 的 `members` 是被合併的 `(moore class L, moore class R)` 對。

## Z5 現象（獨立一節；觀察，不是 theorem）

五個三色 canonical patterns 恰由「唯一色頂點的位置」索引（`threeReps_positions`：`01012↦4, 01021↦3, 01201↦2, 01202↦1, 01212↦0`），所以 component 的三色 acceptance subset 是 `Z5` 的子集。

| 子集大小 | 子集數 | 本 grammar 實現數 |
| ---: | ---: | ---: |
| 0 | 1 | 0 |
| 1 | 5 | 0 |
| 2 | 10 | 5 |
| 3 | 10 | 10 |
| 4 | 5 | 5 |
| 5 | 1 | 1 |

* 32 種子集中實現 21 種；empty 與 singleton 都沒有出現（與 single-component BAD 為空語言一致）。
* size = 2 時只出現五個 `{t_i, t_{i+1}}`——C5 上相鄰位置——每個恰由 6 個 mask 實現。
* size ≥ 3 全部實現。

`GeometryDFA.z5_profiles_checked`（native_decide）在 Lean 內確認：每個 disk-accepted word 的 profile 至少 2 個元素，且恰 2 個時是相鄰對。**這是本 grammar 內的有限檢查，不是關於 disk patch 的 lemma**；10 組 T4 target pairs 恰是「兩個不相交的實現 profile」：5 組相鄰對 × 相鄰對、5 組相鄰對 × 其補集三元組。這是下一個最值得嘗試提煉成結構 lemma 的地方。

## Colour semantics closed：`reject_iff_hall`（`Math/HallTriangle.lean`）

Z5 特徵化的第一步是把「哪些 pattern 被拒絕」從 32,768 個 case 壓成一般數學原因。分層如下，前三層全是普通證明（Hall 定理來自 Mathlib `Finset.all_card_le_biUnion_card_iff_exists_injective`），不依賴任何枚舉：

```text
k3_uncolorable_iff        K3 list-colouring，三個 list 共享自由色 d
      ↓
reject_iff_hall           代入自動機的 forbidden sets（availOf w b k = univ \ run w b k）
      ↓
not_mem_sigma_iff_hall    同一敘述對 exact Sigma
      ↓（下一輪）
winding ⇒ block/degree invariant ⇒ profile bound
```

具名 witness：

* `PairPinnedToFourth avail d := ∃ i ≠ j, avail i = {d} ∧ avail j = {d}`——兩個內部頂點只剩自由色；
* `TripleRestrictedToTwo avail d := ∃ x ≠ d, ∀ i, avail i ⊆ {d, x}`——三個內部頂點合計只剩兩色。

`k3_uncolorable_iff`：若 `∀ i, d ∈ avail i`，則 K3 無 injective 選色 ⇔ `PairPinnedToFourth ∨ TripleRestrictedToTwo`。證明就是 Hall 條件對 |s| = 2、3 的兩個 case（|s| ≤ 1 由自由色排除）。

`reject_iff_hall w b (hd : d ∉ usedColors b)`：`¬ Accept (run w b) ↔ PairPinnedToFourth (availOf w b) d ∨ TripleRestrictedToTwo (availOf w b) d`。對任何留有一個未用色的 pattern 成立，三色 pattern 是其特例。`pinned_iff_sees_all`／`restricted_iff_sees_two` 把兩個 witness 翻成「看過哪些 boundary 顏色」，即 `explanation.json` 的 A／B 兩型。

`regression_guard`（native_decide，32,768 mask × 5 個三色 reps）只確認新定理與 `acceptB` 逐點一致；`scripts/check_automata.py` 另以獨立 Python 實作重算。兩者都是 regression guard，不是定理的證明來源。

**此後染色側封口**：幾何側可以完全不談 colouring，只研究在 winding／block 限制下 A／B witness 能同時出現在哪些 `i ∈ Z5`。注意 disk 條件**不**蘊含「每個內部頂點的 boundary 鄰居是 C5 的 interval 且兩兩交集 ≤ 1」：1,350 個 accepted word 有兩個內部頂點共享兩個 boundary 頂點（4-cycle，第三個內部頂點懸空），鄰居集合也可以像 `{0,2}` 一樣跳過未接線頂點。下一個 geometry lemma 必須從 winding 保證的「已接線頂點環序上的 block」出發。

按 attachment degree 分組的觀察（7,194 個 accepted words）：|R| = 3 只在 degree 型 `(2,3,3)` 出現且 R 恆為 cyclic 3-interval；`(2,2,4)`、`(0|1,3,4)` 給 |R| = 2；其餘 ≤ 2。這是下一輪要證的目標，目前仍是觀察。

## Attachment block theorem（`Math/AttachmentBlock.lean`，普通證明，無枚舉）

`winding ⇒ block` 這一步已封口。把弦序列的三角形位置取出來得到 `L : List (Fin 3)`，`winding w ρ = stepSum L`，其中 `stepSum` 是 `Fin 3` 上前進步數的環和。兩個核心事實：

* `stepSum_le_of_sublist`：`l₁ <+ l₂ → stepSum l₁ ≤ stepSum l₂`（三角不等式 `stp a c ≤ stp a b + stp b c` 逐項，加旋轉不變 `stepSum_rotate`）。
* `stepSum_mem_iff_blocks`：`stepSum L ∈ {0,3} ↔ ∃ n a b c, L.rotate n = replicate a 0 ++ replicate b 1 ++ replicate c 2`。正向先旋轉到第一個變化點，再證「總步數等於頭尾環距的路徑不會繞圈」（`blocks_of_pathSteps`）。

由此：

* `runOK_iff_blocks`：`RunOK w ρ ↔` 弦的三角形位置沿 C5 環讀恰是至多三個 block，且按三角形前進方向排列。這是 `RunOK` 的完整刻畫，不只是必要條件。
* `attachment_block`：`RunOK w ρ → k ∈ w i → k ∈ w j →`
  `(∀ m, Between i m j → w m ⊆ {k}) ∨ (∀ m, Between j m i → w m ⊆ {k})`，`Between i m j` 是 `m` 在 `i→j` 的開弧上。證法：否則序列某個旋轉含子序列 `p,q,p,q'`（`q,q' ≠ p`），其環和是 6 > 3。

兩者的公理依賴只有 `propext / Classical.choice / Quot.sound`，見 `lean-audit.txt`。它們**不**宣稱 disk completeness，也還沒推到 `|R|` 的 profile bound；後者要把 `attachment_block` 與 `reject_iff_hall` 的 A／B witness 接起來，是下一步。

## Geometry → Hall witness 層（`Math/GeometryWitness.lean`，普通證明）

三色 pattern 的形狀固定：unique 頂點 `u`，`u+1,u+3` 一色，`u+2,u+4` 另一色（`Shape b u c₀ x y`）。Hall witness 只問 `run w b k = (linksOf w k).image b` 看過哪些顏色，所以整個拒絕條件可以去掉顏色，只剩 `N_k := linksOf w k` 命中哪些位置：

```text
HitsUnique w u k := u ∈ N_k
HitsOdd    w u k := u+1 ∈ N_k ∨ u+3 ∈ N_k
HitsEven   w u k := u+2 ∈ N_k ∨ u+4 ∈ N_k
SeesAll    w u k := HitsUnique ∧ HitsOdd ∧ HitsEven
GeoReject  w u   := (∃ k ≠ k', SeesAll k ∧ SeesAll k')          -- witness A
                  ∨ (∀ k, HitsOdd ∧ HitsEven)                     -- witness B, 缺 unique 色
                  ∨ (∀ k, HitsUnique ∧ HitsEven)                  -- witness B, 缺 odd 色
                  ∨ (∀ k, HitsUnique ∧ HitsOdd)                   -- witness B, 缺 even 色
```

* `reject_iff_geometry (s : Shape b u c₀ x y) : ¬ Accept (run w b) ↔ GeoReject w u`，對任何具此形狀的 b。
* `threeProfile_eq_geo : threeProfile w = univ.filter (fun u => ¬ GeoReject w u)`（`repAt u` 是 `threeReps` 依 `uniquePosition` 重新索引，`repAt_shape` 給每個 u 的形狀）。

於是 §7.3 的目標可以完全用幾何寫：對 `RunOK w ρ`，`#{u | GeoReject w u} ≤ 3`，且等於 3 時是 cyclic 3-interval。可用的幾何前提是 `attachment_block`／`runOK_iff_blocks`；兩邊都不再提顏色。

## Bridge 續作：attachment budget 與低 degree 分支（2026-09-11）

新增 `Math/AttachmentBudget.lean`、`Math/GeometryProfile.lean`。以下均為 Lean 已證，沒有 `native_decide` 或 attachment-word 枚舉；局部有限事實使用 kernel `decide`，其餘使用 list／Finset 引理與算術證明。

令 `d_k = |linksOf w k|`，`A = Σ_i |w i| = Σ_k d_k`，`B` 為有接線的 boundary 頂點數，`R = rejectionSet w = {u | GeoReject w u}`。

| 定理 | 結論與理由 |
| --- | --- |
| `fan_excess_le_winding` | `Σ_i (|w i| − 1) ≤ winding w ρ`，自然數減法。每個 fan 無重複，所以每個內部相鄰步至少為 1；串接只會增加步數。 |
| `runOK_attachmentCount_le`、`runOK_attachmentCount_le_eight` | `RunOK → A ≤ B + 3 ≤ 8`。這是從 winding 推出的結構界，不引用 planar edge bound。 |
| `runOK_eight_all_active` | 若 `A = 8`，則五個 boundary 頂點都接有弦。 |
| `runOK_common_card_le_two` | `p ≠ q → |N_p ∩ N_q| ≤ 2`。若有三個共同鄰居，三個 fan 各可抽取 `pq` 或 `qp`；所得六弦子序列的 winding 至少 6，與 `RunOK` 衝突。沒有把界誤寫成 ≤ 1。 |
| `geoReject_low_degree` | 若某個 `d_k ≤ 1`，所有 triple Hall witness 都被排除，只剩兩個 `SeesAll` 的 pair witness。 |
| `rejectionSet_subset_common_of_low_degree` | 同一前提下，`R ⊆ N_(k+1) ∩ N_(k+2)`；看遍三類至少需要三條 attachment，所以 pair 不可能使用低 degree 頂點。 |
| `runOK_rejection_le_two_of_low_degree` | 因此 `RunOK ∧ d_k ≤ 1 → |R| ≤ 2`。 |
| `runOK_profile_ge_three_of_low_degree` | 經 `threeProfile_eq_geo`，此分支至少接受三個三色 orbit。 |
| `runOK_large_rejection_cases` | 若 `|R| ≥ 3`，degree multiset 只能是 `(2,2,2)`、`(2,2,3)`、`(2,2,4)`、`(2,3,3)`。這四型由 `∀ k, d_k ≥ 2` 與 `Σ_k d_k ≤ 8` 的普通算術證明得到。 |

**本節記錄 2026-09-11 的中間狀態；完整 bridge 已於 2026-09-12 封口（見下節）。** 當時 接下來須用 block／winding 排除前三種 degree 型的 `|R| ≥ 3`，並對 `(2,3,3)` 證 `|R| ≤ 3`、等於 3 時為 cyclic 3-interval。已證的四型 reduction 是必要條件，沒有證明四型都能有三個拒絕位置。現有的 `z5_profiles_checked` 仍是完整目標的 native 有限檢查，不能用它代替這段結構證明。

驗證：完整 `lake build` 通過（8789 jobs），`lake env lean Math/AutomataAudit.lean` 通過；新增主要定理只依賴 `propext / Classical.choice / Quot.sound`，實際輸出已更新至 `artifacts/automata/lean-audit.txt`。沒有重跑搜尋或 generated data。

新增證明不改變 topology 信任範圍：所有結論以 `RunOK` 為前提，沒有補上一般 disk embedding 到 `AnnulusAccept` 的 completeness。

## Attachment normal form 與第一個 Hall corollary（2026-09-11）

依使用者指定，工作順序改為先 geometry normal form，再推 `GeoReject`。詳見 [attachment_normal_form.md](attachment_normal_form.md)。

`AttachmentNormalForm.lean` 已普通證明 `AnnulusAccept w ↔` 三-block necklace `0^a 1^b 2^c` 旋轉後切成五個無重複 packet 所生成的 word。定義只含 orientation、block 長度、offset、五個切段長度，不含 run 或 Hall；反向證明重建 fan rotations。`a,b,c` 恰為 degrees。min-degree ≥ 2 時，packets 只有空、singleton 或順向 pair，每種 pair 最多一次；共同鄰居 ≤ 1 是此 normal form 的 corollary，度數滿足 singleton 數加左右 shared-junction 指示值的公式。

`NormalFormHall.geoReject_iff_pair_or_opposite` 對所有 accepting words 排除兩個涉及 unique 位置的 triple witnesses，只剩 pair witness 與 `∀ k, HitsOdd ∧ HitsEven`。後續 `GeoRejectBridge.lean` 已證完整拒絕集合界與 cyclic 3-interval（見下節）。十二種形狀的窮盡性仍未 Lean 化，也不是 bridge 的前提。

## Incidence 與飽和 cyclic normal form（2026-09-12）

`AttachmentSignature.lean` 從 normal-form packet alphabet 證 `Z+X+E=5`、`X+2E=A`，再推出六種 incidence regimes。`A=8` 恰為三個 junction 全共享、兩個 singleton、無空 boundary。

`AttachmentSaturated.lean` 普通證明三個 junction 的循環順序與中間 gap 的 singleton 類型，得到雙向 normal form `01 · [1]^y · 12 · [2]^z · 20 · [0]^x`。此核心 theorem 不依賴 boundary 長度；C5 飽和時 x+y+z=2，給出同一 block 放兩個 singleton 或兩個 block 各放一個的兩種配置。沒有枚舉 words 或 packet 排列。後續 `AttachmentGaps.lean`／`AttachmentOrder.lean` 已補齊其餘 regimes 的環序，`GeoRejectBridge.lean` 已證 |R| corollary；整體十二類窮盡性仍未證。詳見 [attachment_normal_form.md](attachment_normal_form.md)。

## Geometry normal form → GeoReject 已封口（2026-09-12）

**proved in Lean**：`Math/GeoRejectBridge.lean` 的 `runOK_rejection_le_three` 證 `RunOK → |R|≤3`；`runOK_three_rejection_structure` 證等號時 degree 型為 `(2,3,3)`，degree 2 的鄰居是 `{t,t+1}`，且 `R={t+2,t+3,t+4}`。`normalForm_rejection_bound` 直接從 attachment normal form 得到 bound 與 cyclic 3-interval。

證明使用 normal form 已推出的 fan ≤ 2、共同鄰居 ≤ 1，以及 attachment budget。degree 2 頂點限制 `R` 在其三個非鄰居內；非相鄰的 degree 2 attachment 只能給至多一個 opposite witness，加至多一個 pair witness，故不能有三個拒絕。無 attachment-word 枚舉、無十二類窮盡性假設、無 native profile 依賴。

經 `threeProfile_eq_geo`，`runOK_profile_ge_two` 與 `runOK_two_profile_adjacent` 證至少接受兩個三色 orbit、恰兩個時為原 boundary 標號上的相鄰對。這將先前 Z5 的 profile 大小／最小形狀觀察提升為此 grammar 下的結構定理；21 種 profile 的可實現性統計與十二類 shape quotient 仍各自維持原信任分類。一般 disk completeness 仍 unresolved。證明細節見 [attachment_normal_form.md](attachment_normal_form.md)。

## 檔案與重現

* `scripts/triangle_automata.py`：產生 `artifacts/automata/`（words、disk embeddings、disk states、Z5 profiles、T4 pairs、五台 Nerode 機、pair machine、summary 與 sha256）。
* `scripts/check_automata.py`：不 import 產生器的獨立 replay：暴力 Σ、NetworkX apex 測試、`PlanarEmbedding.check_structure` 與 face traversal、Nerode 分割重算、pair machine 轉移與 live set 重算、Hall witness 對照、hash。
* `Math/ColorDFA.lean`、`Math/GeometryDFA.lean`、`Math/HallTriangle.lean`、`Math/AttachmentBlock.lean`、`Math/GeometryWitness.lean`、`Math/AttachmentBudget.lean`、`Math/GeometryProfile.lean`、`Math/AttachmentNormalForm.lean`、`Math/NormalFormHall.lean`、`Math/GeoRejectBridge.lean`、`Math/AttachmentSignature.lean`、`Math/AttachmentSaturated.lean`、`Math/AutomataReplay.lean`、`Math/AutomataAudit.lean`。

```bash
uv run --with networkx==3.5 python scripts/triangle_automata.py
uv run --with networkx==3.5 python scripts/check_automata.py
lake build
lake env lean Math/AutomataAudit.lean
```

實際信任依賴記錄於 [lean-audit.txt](../artifacts/automata/lean-audit.txt)。
