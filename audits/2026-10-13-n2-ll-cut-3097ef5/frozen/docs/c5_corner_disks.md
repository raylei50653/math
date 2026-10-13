# C5：高度數設計 disk——corner 條件之外的 CD 機制，與完整 AB|CD 立方體 survivor

2026-09-15。接續 [complementary 立方體報告 §8](c5_complementary_cube.md) 的入口 (i)。

**結論**：在 0、2 內部度數 ≥ 4 的固定 disk 家族（2,000 個偽隨機三角化 disk，保留 1,318 個，
25,288 個 `x₀₂` extensions、7,750 個對齊 `AB|CD` 立方體）上：

1. **corner collapse 不再是 CD 翻轉的主要機制**。接口層狀態的 502 次 CD 翻轉中只有 6 次
   是 corner violation；其餘 496 次全部通過 corner 檢查，結果分成六種：保留接口 208 次、
   接口消失 182 次、打破 blockers 106 次。「CD 必破接口」與「CD 必保留 blockers」
   都是前輪低度數樣本的產物。
2. **從最強狀態出發的 4 次 CD 翻轉全部保留最強條件**（前輪 Errera 家族 40 次全部 collapse）。
3. **存在完整立方體 survivor**：三個對齊立方體（維度 0、1、1，三張不同 disk，20、22、23 頂點）
   在**所有**對齊狀態同時維持 blockers、接口與兩次新生連通。它們的最短 escape 一律以
   split 之外的交換開始：`Comp_AD(0)∋4`（兩例，2 步到 singleton-1）或 `T=Comp_AD(2)`
   （一例，3 步到 singleton-3）。因此「固定 `AB|CD` 立方體的獨立交換必打破局部條件」
   這個候選局部引理**被固定圖證書否定**；主引理若成立，矛盾必須用到 split 之外的
   色對，也就是 §8 入口 (ii) 的 class 層分析。

**信任範圍**：對齊立方體完備性與 disk separation 是紙面引理；家族由固定 seed 的
偽隨機生成器產生，每個 disk 以定向三角複形檢查確認；所有狀態、paths、翻轉結果、
最短 escape 與 cross moves 是精確 Python 證書；三個 survivor 連同邊表、面表與逐步
escape 完整保存。零與非零計數都是有限觀察。Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

## 1. 家族：怎麼「設計」高度數 disk

前輪的 corner 條件只涉及 0、2 的鄰域，樣本中 0、2 只有 2–3 個內部鄰點。本輪不擴大
低度數樣本，而是固定一個生成器：從 C5 上的錐開始，把其餘內部頂點依序插入面中，
再做 120 次隨機邊翻轉；拒絕會產生 boundary chord、重邊或度數 < 4 頂點的提案，
並以機率 1/2 拒絕新邊不碰 `{0,2}` 的提案。`random.Random(seed·1000+n_int)`，
`n_int∈{11,…,20}`，seed `0…199`，共 2,000 個 disk；只保留 0 與 2 的內部度數皆 ≥ 4 者，
得 1,318 個（無重複邊表；同構者未合併）。每個 disk 都通過前輪的
`orient_and_verify`：定向三角複形、單一 C5 boundary、`χ=1`、每個頂點 link 正確。

每個 disk 列舉全部 S₄-normalized 染色、由禁止 singleton 出發的多源 Kempe BFS、
全部 `x₀₂` extensions，並沿用 `scripts/c5_complementary_cube.py` 的 `aligned_cube`、
`observe`、`scan_graph`：每個對齊狀態在其實際染色上重算 blockers、`S`、`T`、接口、
兩次新生連通、corner 檢查與最短 escape。

| 層 | 狀態數（共 25,288） | 立方體全程通過（共 7,750） | AB 子立方體全程通過（共 20,787） |
|---|---|---|---|
| blockers | 763 | 226 | 629 |
| blockers＋接口 | 352 | 67 | 297 |
| blockers＋接口＋兩次新生 | 16 | **3** | 5 |

`first_failure`：blockers 24,525、interface 411、newborn_AD 279、newborn_AC 57、none 16。
escape：1 步 24,525、2 步 762、3 步 1。維度最大 `ab4_cd0`、`ab0_cd6`；
`ab0_cd0` 1,838 個。全部對齊狀態都有 escape，所以每個立方體仍是控制例（§5）。

## 2. corner 檢查之外的 CD 機制

接口層（blockers＋接口）狀態的全部 CD 翻轉共 502 次。corner 檢查仍精確預測
`S'={0}`／`T'={2}`（6 次 violation，6 次 trivialisation，逐一對應），但其餘
496 次都 **通過** corner 檢查，checker 對每一次分類如下（`cd_flip_mechanism`）：

| 機制 | 次數 | 定義 |
|---|---|---|
| `kept_outside_edge` | 202 | 某接口邊落在未翻轉的 CD component，且兩端仍在 `S'`、`T'`，接口保留 |
| `swallowed` | 179 | 全部接口邊在被翻轉的 V 內，翻轉後沒有任何 `C'∩S'`–`D'∩T'` 邊；blockers 保留，escape 2 |
| `relocated_inside` | 6 | 全部接口邊在 V 內，但翻轉後出現另一組接口邊（三張 disk 各一對互逆翻轉） |
| `ends_detached` | 3 | 有接口邊在 V 外，但其一端離開了 `S'` 或 `T'` |
| `blocker_broken_BC` | 59 | 翻轉後 BC 1↔3 path 消失，escape 1 |
| `blocker_broken_BD` | 47 | 翻轉後 BD 1↔4 path 消失，escape 1 |

**可證的小事實（紙面）**：V 內的接口邊 `(u,v)`（u∈C∩S、v∈D∩T）翻轉後 u 變 D、v 變 C，
不可能以同一方向留在接口；它只能以反向 `(v,u)` 重新出現，前提是 `v∈S'` 且 `u∈T'`。
checker 對全部 496 次 assert 此事，反向重現只有 4 條邊（都在 `kept_outside_edge` 類）。
所以「接口全在 V 內」幾乎總是 swallowed（179：6），但不是必然。

**沒有單一機制**：同一層的 CD 翻轉可以保留接口（208）、吞掉接口（182）或打破
blockers（106）；而前輪 Errera 家族的 160 次全是 corner collapse 且 blockers 全保留。
故不存在「CD bit 必破接口」的引理可抽；corner 條件也只是 trivialisation 的精確判準，
對其餘結果沒有預測力。

從 16 個最強狀態出發的單 bit 翻轉：AB → 打破 blockers 14、只失新生 AC 2、保留 2；
CD → **保留 4、失敗 0**。這與前輪「CD bit 一律 collapse」相反。

## 3. 三個完整立方體 survivor

| disk | seed, n_int | 頂點／邊／面 | 0、2 內部度數 | 維度 (AB, CD) | 內部 CD component | escape |
|---|---|---|---|---|---|---|
| 590 | 166, 15 | 20／52／33 | 6, 4 | (0, 0) | — | 3 步，先交換 `T=Comp_AD(2)`，到 singleton-3 |
| 811 | 93, 17 | 22／58／37 | 8, 4 | (0, 1) | `{8,14}` | 2 步，先交換 `Comp_AD(0)={0,4,7,15,18}∋4`，到 singleton-1 |
| 891 | 16, 18 | 23／61／39 | 4, 6 | (0, 1) | `{13,18,20,22}` | 2 步，先交換 `Comp_AD(0)={0,4,18}∋4`，到 singleton-1 |

每個 survivor 的每個狀態：兩條 blockers、`S∩C5={0}`、`T∩C5={2}`、接口非空、
交換 S 後 AD 2↔4、交換 T 後 AC 0↔3 都成立，corner 檢查無 violation，
沒有 1 步 escape。

**escape 全走 split 之外**：立方體在 `AB|CD` 交換下封閉且沒有 1 步 escape，所以從
距離最小的狀態出發，最短 escape 的第一步必是 AC／AD／BC／BD 交換（紙面三行）。
證書列出每個 survivor 狀態的全部 cross moves：碰 boundary 的六個 component
（`S`、`Comp_AC(2)∋3`、`Comp_AD(0)∋4`、`T`、`Comp_BC(1)∋3`、`Comp_BD(1)∋4`）交換後的
boundary 與 escape 距離；**沒有任何內部 cross component 的交換縮短 escape**。
兩例經 `Comp_AD(0)∋4` 到達 `2=4` 的四色 fibre `(D,B,A,C,A)`，再一步得 singleton-1；
一例經 `T` 到 `(A,B,D,C,D)`，再兩步。BC／BD 交換 `Comp(1)∋3`、`Comp(1)∋4` 把
`x₀₂` fibre 映到自身（另一個 extension），不在同一對齊立方體內。

因此**候選局部引理「完整 AB|CD 立方體必在某狀態失敗」為假**。這不觸及主引理：
三張 disk 的全圖 P 都含禁止 singleton，只說明 split 內的獨立交換不足以造成矛盾，
矛盾（若有）必須用到跨 split 的色對與 class 內其他四色 fibres。

## 4. 沒有禁止 singleton 的 Kempe classes

七張 disk 共有 8 個 Kempe class 不含任何 singleton-1／3／4 染色（大小 4 或 12）。
它們的 boundary 只有 singleton-0、singleton-2 與四條非 `{0,2}` chord 的四色 pattern，
**沒有 `x₀₂` extension**——與 catalogue masks 424、960、1000 的 `P⊆{0,2}` 但 `x₀₂=0`
同型，並符合 class 恆等式 `x_uv+y_u+y_v=L_K`（`y₁=y₃=y₄=0` 給 `x₀₂=L−y₀−y₂=0`）。
它們不是候選；記錄於證書 `closed_classes`。

## 5. 範圍限制

本輪沒有枚舉新的 k≥6 catalogue、沒有重跑 production 枚舉、沒有修改 relation
catalogue、前輪證書或 Lean。家族由固定 seed 生成，不是圖搜尋的完備列舉；同構 disk
未合併；沒有全圖 `P(G)⊆{0,2}` 的真正候選（每個對齊狀態都有 escape）。
三個 survivor 是控制反例，只否定局部命題。

## 6. 對 §8 兩個入口的回答與下一步

入口 (i) 已回答：高度數 disk 上 CD bit 可以、也可以不破壞接口，機制不唯一（§2），
沒有可抽的「CD 必破」引理；而且完整立方體可以全程存活（§3）。

下一步只剩入口 (ii)：固定全圖 `P(G)⊆{0,2}`，在同一 class 內同時使用五個四色
fibres。survivor 給出具體的第二層必要條件：`Comp_AD(0)∋4` 時交換得到 `2=4` fibre
`(D,B,A,C,A)`，該染色再不得有 1 步 escape；對 `T`、`Comp_AC(2)∋3`、`S` 同理。
可直接沿用本證書 survivor 的 `cross_moves` 表當測試資料，先列出每個四色 fibre 的
blockers 條件，再檢查它們在 survivor 上如何被違反。不要再擴大本家族或改 seed 找
更多 survivor；三個已足夠否定局部命題。

## 7. 重播

```bash
python3 scripts/c5_corner_disks.py --check   # 約 20 秒
python3 scripts/c5_complementary_cube.py --check
python3 scripts/c5_ab_swap_cube.py --check
python3 scripts/c5_kempe_connectivity.py --check
git diff --check
```

[checker](../scripts/c5_corner_disks.py)／[證書](../artifacts/c5_cells/corner_disks.json)
保存 source hashes、生成參數、逐 disk 摘要（seed、邊表 hash、度數、extensions、
closed classes、各層立方體數）、達 blockers 層的 384 個立方體摘要、全部 496 次
corner-compliant CD 翻轉的機制記錄、16 個最強狀態、三個 survivor 的完整邊表／面表／
定向面／所有狀態 paths／cross moves／逐步驗證的最短 escape。重播不需網路、Sage 或 NetworkX。
