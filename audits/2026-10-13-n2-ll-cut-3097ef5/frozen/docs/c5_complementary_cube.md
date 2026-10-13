# C5：完整 AB|CD 交換立方體——無 survivor，失敗機制是 corner collapse

2026-09-15。接續 [AB 交換立方體報告 §6](c5_ab_swap_cube.md) 的下一個命題。

**結論**：在固定 complementary split `AB|CD` 的**全部獨立 component 交換**下，
既有 132 witnesses 的 176 個 `x₀₂` extensions（123 個對齊立方體）與 Errera 三角化的
120 個 16 頂點 disk（600 個對齊立方體）中，**沒有任何立方體**能在所有狀態同時維持
blockers、接口與兩次新生連通；Errera 家族連「blockers 加接口」也沒有全程 survivor。
所有由 CD bit 造成的失敗（corpus 2 次、Errera 家族 160 次）都是同一個機制：
被交換的內部 CD component 含頂點 0 的全部 C 鄰點且不含其 D 鄰點（或 2 的 D/C 對偶），
交換後 `S={0}`（或 `T={2}`），接口為空，兩步即得 singleton-1。
這給出一個精確、可證的必要 **corner 條件**（§6），但它是低 boundary 度數的產物，
不是一般 disk 的「CD 必破」定理。

**信任範圍**：對齊立方體完備性與 disk separation 是紙面引理；全部狀態、paths、
最短 escape 是精確 Python 證書；corner 條件的證明是三行紙面推論。
零 survivor 是有限觀察，不是定理。Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

## 1. 對齊立方體：只有內部 components 是自由 bits

固定 `c|C5=(A,B,A,C,D)`。令 `U₀⊇{0,1,2}` 為含 boundary 的 AB component，
`V₀⊇{3,4}` 為含 boundary 的 CD component（邊 01、12、34 保證各在同一 component）。
AB 與 CD 是 complementary pairs：任一 AB 交換不改變 AB 或 CD induced graphs，
CD 交換亦然，故所有 components 在整個 orbit 中固定，任意長序列的結果由每個
component 的交換奇偶決定。交換 U₀ 等於全域 A/B 置換，交換 V₀ 等於全域 C/D 置換。
因此**對齐狀態 ↔ 內部 components 的 bit 向量**，維度 `r_AB−1 + r_CD−1`。

checker 對每個起點：
- 逐 bit 實際交換（每步 assert 該集合仍是當前染色的完整 component）；
- assert 每個狀態 proper、boundary 仍為 `(0,1,0,2,3)`、AB／CD partitions 與起點相同；
- 另枚舉**全部** components 的 `2^r` 個有標號結果，`normalize` 後必須等於上述狀態集
  （對齊只用了 U₀、V₀ 誘導的全域置換，沒有對不同狀態任選 frame）；
- 立方體內部永不出現 singleton（boundary 固定），故 `singleton_reached` 恆為否。

負控制：兩個內部 CD components 的 7 頂點小圖有 4 個對齊狀態，只交換 V₀ 只得 2 個。

## 2. 逐狀態重新計算的觀察量與分層

每個狀態都在其**實際染色**上重算，不沿用前一狀態的 component identity：

| 觀察 | 定義 |
|---|---|
| `blocker_BC` | `G[B∪C]` 中 1↔3 的 BFS path |
| `blocker_BD` | `G[B∪D]` 中 1↔4 的 BFS path |
| `S`, `T` | `Comp_AC(0)`、`Comp_AD(2)`；並檢查 `S∩C5={0}`、`T∩C5={2}` |
| `interface` | `E(C∩S, D∩T)` 的全部邊，及每條邊所在的 CD component |
| `newborn_AD` | 交換 S 後 `G[A∪D]` 中 2↔4 的 path |
| `newborn_AC` | 交換 T 後 `G[A∪C]` 中 0↔3 的 path |
| `escape_distance` | 到任一 singleton∉{0,2} 的最短完整 Kempe 步數 |

分層：`blockers` ⟸ `interface`（blockers 且接口非空）⟸ `newborn`（再加兩次新生連通）。
`first_failure` 記錄最先失敗的層，newborn 再分 AD／AC。
blockers 成立時 checker assert separation（disk 紙面定理的可檢驗後果）；
新生連通成立時 assert 接口非空（前輪接口引理）。兩者全部樣本通過。

escape 距離由 S₄-normalized 染色上的多源 BFS 得到：Kempe move 與全域重命名可交換，
商距離即有標號最短距離。每個立方體起點另重建並逐步驗證一條最短 escape。

## 3. 真正候選與控制例的區分

「真正候選」指全圖 `P(G)⊆{0,2}` 且有 `x₀₂` extension。由 chord-total 恆等式，
`P(G)⊆{0,2}` 且 `x₀₂>0` 強迫五個 `x_f` 全正；catalogue 中沒有這種 Σ。
132 個 masks 中 `P⊆{0,2}` 的只有 424、960、1000，三者 `x₀₂=0`，沒有對齊起點。
**所以本輪掃描的每一個 extension 都是控制例**，只能否定過強的局部命題，
不能支持主引理。Errera 家族亦然（各 disk 的 P 都含禁止 singleton，escape 必存在）。

## 4. 既有 corpus：123 個對齊立方體

| 層 | 狀態數（共 176） | 立方體全程通過（共 123） | AB 子立方體全程通過（共 166） |
|---|---|---|---|
| blockers | 24 | 11 | 20 |
| blockers＋接口 | 5 | 2 | 4 |
| blockers＋接口＋兩次新生 | 1 | **0** | 0 |

AB 子立方體（固定 CD bits、變動 AB bits）的 166／20／4／0 與前輪 AB 報告 §6 逐項相同，
是本輪立方體構造的一致性檢查。

維度分布：`ab0_cd0` 72、`ab0_cd1` 40、`ab0_cd2` 1、`ab1_cd0` 10。
**沒有任何 extension 同時有內部 AB 與內部 CD component**，因此 corpus 本身無法
測試「AB 與 CD bits 同時存在」的情形；這是把 Errera 家族納入的原因。

`first_failure`：blockers 152、interface 19、newborn_AD 3、newborn_AC 1、none 1。
escape 距離：blockers 失敗的 152 個狀態全為 1 步；其餘 24 個全為 2 步。

- 兩個全程「blockers＋接口」的立方體是 mask 956、1012，皆為單狀態（維度 0），
  各只缺一邊新生連通（956 缺 AC、1012 缺 AD）。
- 唯一通過最強條件的狀態是 mask 935、bits `[1]`：染色 `(A,B,A,C,D,B,C,D)`，
  `S={0,6}`、`T={2,7}`、接口 `67`（位於 V₀）、新生 AD `2–7–6–4`、AC `0–6–7–3`。
  其唯一內部 AB component `{5}` 一翻轉，blockers 立刻失敗（`S`、`T` 都含 2 或 0，
  escape 1 步）。
- 「某個 AB 子立方體全過、整個立方體不過」（Errera 型）：blockers 層 7 個
  （693、701、822、886、951、957、1014），接口層 2 個（636、1020），皆由 CD bit 造成。
- 接口層狀態上的 CD 翻轉只有兩次（636、1020 的 bits `[1]→[0]`）：接口邊 `76` 在內部
  CD component `{6,7}` 中，翻轉後 `S={0}`、`T={2}`，接口消失，blockers 保留，escape 2。

每個失敗立方體的 earliest failure（最少 bits 的失敗狀態、失敗層、escape）在證書
`corpus.failures` 與各 `cubes[*].earliest_failure`；達到 blockers 層的立方體保留完整
paths，其餘只留逐狀態摘要列。

## 5. Errera 家族：120 個 disk、600 個立方體

Errera 三角化（Sage 10.6 邊資料）有 17 頂點、45 邊、30 面；12 個 5 度頂點各刪去一個，
boundary 為其 link 五邊形，取 10 個 D₅ 對齊，得到 120 個有標號 16 頂點 disk
（同構者未合併）。每個都以前輪的定向三角複形檢查確認為 disk；第一個 disk 恰為
前輪固定控制圖與其 `START`。

| 層 | 狀態數（共 1040） | 立方體全程通過（共 600） | AB 子立方體全程通過（共 800） |
|---|---|---|---|
| blockers | 400 | 80 | 160 |
| blockers＋接口 | 240 | **0** | 80 |
| blockers＋接口＋兩次新生 | 120 | **0** | 20 |

維度：`ab0_cd0` 320、`ab0_cd1` 120、`ab1_cd0` 80、`ab1_cd1` 80。
`first_failure`：blockers 640、interface 160、newborn_AD 80、newborn_AC 40、none 120。
escape：1 步 640、2 步 360、3 步 40（3 步全是最強狀態）。

從 120 個最強狀態出發的單 bit 翻轉，機制只有三種：

| 翻轉 | 結果 | 次數 |
|---|---|---|
| AB | 仍為最強狀態（`S`、`T` 大小 2↔4，escape 3） | 40 |
| AB | blockers 失敗，`S`、`T` 各 9 點含對側 boundary，escape 1 | 80 |
| CD | 接口失敗，`S={0}`、`T={2}`，接口邊全在被翻轉 component 內，escape 2 | 40 |

接口層（blockers＋接口）狀態上的全部 160 次 CD 翻轉：接口皆變空、blockers 皆保留、
escape 皆為 2；120 次接口邊全在被翻轉 component 內，40 次有邊在 V₀ 但一樣消失；
80 次 `S`、`T` 同時 collapse，其餘 80 次恰一者 collapse。**沒有一次** CD 翻轉保留接口。

## 6. 機制：corner collapse，與由此得到的必要條件

令 c 為對齊狀態，V 為內部 CD component，c′ 為交換 V 的結果。頂點 0 在 c′ 中的
C 鄰點恰為 `(N_C(0)∖V) ∪ (N_D(0)∩V)`。因此

\[
S'=\{0\}\iff N_C(0)\subseteq V\ \wedge\ N_D(0)\cap V=\varnothing,
\]

對 2 與 D/C 對偶得 `T'={2}`。checker 對每個接口層狀態列出滿足此式的 V
（`corner_violations`），並 assert 它**恰好**預測翻轉後的 collapse；
corpus 2 次、家族 160 次 CD 翻轉全部是 corner violation，
且**沒有任何接口層狀態擁有通過 corner 檢查的內部 CD component**。

**Corner 條件（紙面推論，未 Lean 化）**：若全圖 `P(G)⊆{0,2}`，則對每個對齊狀態 c
與每個內部 CD component V，`N_C(0)⊄V` 或 `N_D(0)∩V≠∅`，且 `N_D(2)⊄V` 或
`N_C(2)∩V≠∅`。證明：否則 c′ 是同一 G 的另一個 `(A,B,A,C,D)` extension，
`S'={0}` 使接口為空，與前輪接口引理矛盾（或直接交換 `{0}`、再交換含 2 的 AD
component 得 singleton-1）。特別地每個對齊狀態中 0 必有 C 鄰點、2 必有 D 鄰點。

**為何這不是一般定理**：條件只涉及 0、2 的鄰域。在三角化 disk 中 0 的內部鄰點
按 link 順序分成被 B 鄰點隔開的 C/D 連續段，靠 4 的一段屬於 V₀；只要 0 有一個
C 鄰點在 V₀，或 C 鄰點分布在兩個不同 CD components，或某一段同時含 C 與 D，
corner 條件就成立。本輪所有圖的 0、2 只有 2–3 個內部鄰點（corpus 更少），
所以 collapse 無所不在。這是樣本的低度數產物；一個 boundary 度數較高、
在每個對齊狀態都滿足 corner 條件的 disk 是否存在，本輪沒有回答。

## 7. 對四個指定問題的回答

1. **完整 `AB|CD` 立方體全程維持**：blockers——corpus 11 個立方體（其中 9 個維度 0，
   636、1020 維度 1），家族 80 個；blockers＋接口——corpus 僅 956、1012（維度 0，
   即立方體是單點），家族 0；blockers＋接口＋兩次新生——**兩處皆 0**。
2. **最常先失敗的是 blockers**（狀態層面 152/176、640/1040），但那是低層雜訊；
   在最強狀態上，CD bit 一律以 corner collapse 打破接口，AB bit 則要麼保留一切、
   要麼直接打破 blockers。真正候選在 corpus 中不存在（§3），無法就其失敗方式作陳述。
   CD 交換在**本樣本**中系統性破壞接口與新生連通，但機制是 §6 的低度數 collapse，
   不能外推為「CD 必破」。
3. **沒有 survivor**，故無新控制反例；935 的單一最強狀態被其唯一 AB bit 打破。
4. **與 Errera 對照**：corpus 中 636、1020 呈現與 Errera `START` 完全相同的模式
   （AB 子立方體全過接口層，CD bit 令 `S={0}`、`T={2}`，escape 2）；Errera 家族的
   另外 119 個 disk 只重複這個模式或以 AB bit 打破 blockers。三個來源沒有出現第三種
   失敗機制。

按成功標準，本輪屬於 **B**：一致的失敗模式與一個可精確陳述的必要條件（corner 條件），
同時說明它為何不足以成為一般引理。

## 8. 範圍限制與下一步

（2026-09-15 續：入口 (i) 已在 [c5_corner_disks.md](c5_corner_disks.md) 完成——高度數 disk 上
CD 機制不唯一，且存在三個完整立方體 survivor；本節下一步為歷史入口。）

本輪沒有枚舉新的 k≥6 catalogue、沒有重跑 production 枚舉、沒有修改 relation catalogue、
前輪證書或 Lean。Errera 家族是同一固定來源的刪點控制，不是圖搜尋。

下一步不宜再擴大低度數樣本。可行入口：(i) 設計 boundary 頂點 0、2 內部度數 ≥4、
在所有對齊狀態滿足 corner 條件的固定 disk，檢查 CD bit 是否仍破壞接口——若仍破壞，
機制必然不同於 corner collapse，才值得抽成引理；(ii) 改用全圖 `P(G)⊆{0,2}`，
把 corner 條件與接口引理一起套到同一 class 內全部五個四色 fibres，尋找 disk 結構矛盾。
本輪不把兩處的零外推為一般證明。

## 9. 重播

```bash
python3 scripts/c5_complementary_cube.py --check
python3 scripts/c5_ab_swap_cube.py --check
python3 scripts/c5_kempe_connectivity.py --check
python3 scripts/c5_kempe_class_counts.py --check
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
git diff --check
```

[checker](../scripts/c5_complementary_cube.py)／[證書](../artifacts/c5_cells/complementary_cube.json)
保存 source hashes、catalogue 與 Errera 來源、對齊與 relabel 規則、真正候選判定、
corpus 全部 123 個立方體（達 blockers 層者含全部 paths 與最短 escape）、失敗表、
Errera 家族 120 個 disk 的邊表與逐立方體摘要（第一個 disk 保留完整細節）、
翻轉機制統計、corner 檢查統計與負控制。重播不需網路、Sage 或 NetworkX，約 1 秒。
