# Attachment geometry normal form

2026-09-12 更新。先刻畫 attachment geometry，再把 `GeoReject` 當成 corollary。固定原有 triangle grammar；normal-form 與 incidence 續作均未重跑 word 枚舉。

## 已證的雙向 normal form

`Math/AttachmentNormalForm.lean` 的 `annulusAccept_iff_normalForm`：

```text
AnnulusAccept w ↔ ∃ s : NecklaceCuts, s.Valid ∧ s.word = w
```

`NecklaceCuts` 是純幾何生成參數：

1. 一個全域 triangle orientation `o`。
2. 三個自然數 `a,b,c`，構成環狀 necklace `0^a 1^b 2^c`。
3. 一個旋轉量 `offset`。
4. 五個依有序 boundary `0,1,2,3,4` 排列的切段長度 `widths`，總和恰為 `a+b+c`。

將旋轉後的 necklace 按 widths 切成五個 packet。`Valid` 只要求每段沒有重複的 triangle position。第 i 段經 `pos o` 翻回實際內部頂點，取集合就是 `w i`。

**這個定義沒有 run、fan rotation、winding、colouring 或 Hall witness。** 空段保留未接線的 boundary 頂點；零長 block 允許某個內部頂點無 attachment。參數可以有多個表示，尚未選唯一 canonical representative。boundary labels 保持原序，沒有獨立取 D5 quotient。

與舊 `runOK_iff_blocks` 的差別是：舊定理只描述某個既定 run 的弦序列；新定理以 block 長度、旋轉量和 boundary 切段直接生成 word，並證每個有效生成結果都能重建 accepting run。

## 雙向證明

正向 `normalForm_of_runOK`：把 run 的五個 fan 映到 triangle positions。舊 block theorem 提供環和為 0 或 3 的三個 homogeneous blocks；反向旋轉給出 offset，五個 fan 的長度給出 widths。`cutPackets_of_lengths` 證切回來恰是原 fan，沒有遺失 ordered attachments。

反向 `NecklaceCuts.accept`：有效 cut necklace 的每個 packet 都是整個弦序列的 sublist，所以 cyclic step sum 至多 3。每段 Nodup，故長度至多 3；`packet_realizes_fan` 證每個這樣的局部 packet 能用某個 fan rotation 實現。重建五個 rotation 後，完整弦序列恰等於切段前的 necklace，得到 `RunOK`。

反向只用至多三元素 packet 的局部 kernel 決定，不枚舉 words 或全域 normal-form 參數。

## 參數的幾何語意

| 定理 | 內容 |
| --- | --- |
| `NecklaceCuts.degrees` | `a,b,c` 分別等於 `N_(pos o 0), N_(pos o 1), N_(pos o 2)` 的大小。 |
| `NecklaceCuts.packet_lengths` | widths 恰是五個 packet 的實際長度。 |
| `NecklaceCuts.packet_length_eq_card` | Valid 下 packet 長度恰是 boundary attachment 數；取集合沒有吞掉重複弦。 |
| `NecklaceCuts.total_le_eight` | `a+b+c ≤ 8`，經既有 structural attachment budget 得到。 |

## 三個 degree 都至少二：singleton blocks 與 shared junctions

`annulusAccept_iff_nondegenerate_normalForm` 給出此分支的加強雙向 normal form：`a,b,c ≥ 2`，每個 packet 只能為

```text
[]、[p]、[p,p+1]     （p ∈ Fin 3）
```

每一種順向 pair `[p,p+1]` 最多出現一次。這些 packets 仍然是**同一個三-block necklace 的連續切段**；不能只保留上述 alphabet 與出現次數、丟掉環序後宣稱等價。

三個結構引理：

* `middle_count_eq_one`：若 one-turn 弦環包含連續、互異的 `[p,q,r]`，則 q 在整個環恰出現一次。否則抽出 `[p,q,r,q]`，其 winding 為 6。這個 list 引理不依賴 boundary 長度為五。
* `NecklaceCuts.triple_packet_forces_degree_one`：因此三元素 packet 迫使某個內部 degree 為 1，排除 nondegenerate 分支的 triples。
* `pair_forward_of_all_mem`：若三個 positions 都出現，連續互異 pair 只能順向。`NecklaceCuts.forward_pair_count_le_one` 再排除同一順向 pair 出現兩次，否則有 alternating 子序列 `[p,p+1,p,p+1]`，winding 為 6。

所以 picture 是三個 singleton block，以及三個相鄰 block 的接點各可由一個 boundary 頂點共享。空 boundary packet 仍可插在原有五個位置中。

令 `x_k` 為 singleton `[k]` 的數量，`ε_k` 為 shared packet `[k,k+1]` 的數量。已證 `ε_k ≤ 1`，而 `NecklaceCuts.degree_eq_singletons_add_junctions` 證明：

```text
d_(pos o k) = x_k + ε_(k−1) + ε_k
```

`NecklaceCuts.common_next_eq_junction` 更把共同鄰居集合精確對到 shared packet 所在的 boundary 位置。因此得到：

```text
runOK_common_le_one_of_degrees:
RunOK w ρ ∧ (∀ k, |N_k| ≥ 2) ∧ p ≠ q → |N_p ∩ N_q| ≤ 1
```

這次加上了必要的 degree 前提；沒有推翻一般情況下只能保證 ≤ 2 的舊定理。

## 一個具體 normal form

前輪分類的 `(2,3,3)` 代表 `N₀={0,1}, N₁={0,3,4}, N₂={1,2,3}` 可以用以下參數表示：

```text
orientation = mirror       （pos: 0↦0, 1↦2, 2↦1）
(a,b,c) = (2,3,3)
necklace = 00111222
offset = 7
旋轉後 = 20011122
widths = [2,2,1,2,1]
packets = [2,0] | [0,1] | [1] | [1,2] | [2]
```

這是說明切段參數的例子，不是十二種 shape 已在 Lean 中完成分類的宣稱。

## GeoReject 的第一個 corollary

幾何檔案不 import Hall。`Math/NormalFormHall.lean` 才把上述結果接到拒絕語意：

```text
geoReject_iff_pair_or_opposite:
RunOK w ρ →
  (GeoReject w u ↔
    (∃ p ≠ q, SeesAll w u p ∧ SeesAll w u q)
    ∨ (∀ k, HitsOdd w u k ∧ HitsEven w u k))
```

這對所有 accepting words 成立，不限 degree ≥ 2 分支。原本另外兩個 triple witness 都要求三個內部頂點接到 unique boundary 頂點 u，且各自還接到另一個 colour class；後者使三個 degree 都 ≥ 2，前者使 u 的 fan 有三個元素，與 normal form 矛盾。

尚未證 pair witness 被另一 witness 包含，也尚未證完整 `|R| ≤ 3` 與等號時 cyclic 3-interval。

## Incidence 的六種 regime（2026-09-12）

新增 `Math/AttachmentSignature.lean`。令 `X` 為 singleton packet 總數、`E` 為 shared-junction packet 總數、`Z` 為空 boundary packet 總數，`A = a+b+c` 為 attachment 總數。所有定理仍以 valid normal form、三個 attachment degrees 都 ≥ 2 為前提。

`NecklaceCuts.inventory` 證：

```text
Z + X + E = 5
X + 2E = A
```

加上各 junction 最多一次，所以 `E ≤ 3`；三個 degrees 至少二，所以 `A ≥ 6`。`NecklaceCuts.incidenceRegime` 用普通算術得到恰好以下六種必要的 scalar regimes：

| E | X | Z | A |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 0 | 6 |
| 2 | 2 | 1 | 6 |
| 2 | 3 | 0 | 7 |
| 3 | 0 | 2 | 6 |
| 3 | 1 | 1 | 7 |
| 3 | 2 | 0 | 8 |

這是 incidence 參數的窮盡性，不是十二種 cyclic shape 的窮盡性。`(E,X,Z)` 沒有保留 singleton／空 boundary 的具體環位置。

`eight_iff_three_junctions_two_singletons` 證 `A=8 ↔ E=3 ∧ X=2 ∧ Z=0`。此時三個 junction 各恰一次，`degree_eq_singletons_add_two` 給出 `d_k=x_k+2`。兩個 singleton 只能放在同一 block 或兩個不同 block，故 `saturated_degree_cases` 證出 degree 型 `(4,2,2)` 或 `(2,3,3)`。這是在 normal form 上做的 incidence 推導，沒有按拒絕集合分 case。

## 飽和分支的 cyclic normal form（2026-09-12）

新增 `Math/AttachmentSaturated.lean`。對任意 packet list，只要三種 junction `01,12,20` 都出現、各 packet 非空且 Nodup，`three_junction_normalForm_iff` 證明：

```text
stepSum (flatten packets) ≤ 3
  ↔ ∃ n,x,y,z,
      packets.rotate n = 01 · [1]^y · 12 · [2]^z · 20 · [0]^x
```

這裡 `01` 表示一個 pair packet `[0,1]`，`[1]^y` 表示 y 個 singleton packets `[1]`。這個核心 list theorem **不限制 boundary 長度為五**，也不枚舉 packet 排列。

證明分三步：

1. `junctions_cyclic_order`：旋轉到 `01`；若另兩個 junction 逆序出現，抽出 `01,20,12` 的六弦子序列，winding 為 6，所以只能依 `01→12→20` 排列。
2. `anchored_gaps_constant`：在每對連續 junction 間插入一個 position k。局部 step sum ≤ 3 迫使 k 等於共同端點，故三段分別只能有 1、2、0；packet 非空且無重複，再迫使每個 packet 是 singleton。
3. `junctionPackets_stepSum`：任意 x,y,z 的上述 displayed form 都恰好 winding 3，證反方向。

回到 C5，`NecklaceCuts.saturated_cyclic_normalForm` 證 `A=8` 時上式還有 `x+y+z=2`。`runOK_saturated_normalForm` 把同一結論接回原始 attachment word，保留 `s.word=w`，不只證抽象 packet list。

兩種 singleton 配置的示意代表：

```text
同一 block： 01 | 12 | 20 | 0 | 0       degree 型 (4,2,2)
不同 block： 01 | 1  | 12 | 20 | 0      degree 型 (3,3,2)
```

具名定理給的是帶 triangle orientation、boundary rotation 與 x,y,z 參數的 normal form；沒有另行聲稱已完成 D5×S3 quotient 的唯一代表定理。

## 三 junction 含空 boundary 的雙向環序（2026-09-12 續）

新增 `Math/AttachmentGaps.lean`。`three_junction_gaps_iff` 去掉先前的「每個 packet 非空」前提，對任意長度的 Nodup packet list 證明：三種 junction 都出現時，

```text
stepSum (flatten packets) ≤ 3
  ↔ ∃ n,U,V,W,
      packets.rotate n = 01 · U · 12 · V · 20 · W
      U 的每個 packet 是 [] 或 [1]
      V 的每個 packet 是 [] 或 [2]
      W 的每個 packet 是 [] 或 [0]
```

這是 **proved in Lean** 的雙向 normal form。U、V、W 保留空 packet 的具體位置，沒有刪除空 boundary 再重新編號。正向沿用 junction cyclic order 與 anchored gaps 的結構證明；反向證每個 gap 的 flatten 恰為對應 singleton 數量的 constant block，接回 `junctionPackets_stepSum`。沒有枚舉 words 或完整 packet 排列。

`NecklaceCuts.three_junction_cyclic_gaps` 接回 valid cut-necklace 的原始五個 packets：`|U|+|V|+|W|=2`，三段內空 packet 數之和恰等於 `s.emptyTotal`。此定理只需 `Valid` 與 `junctionTotal=3`，不另外要求 min-degree。

`three_junction_gap_inventory` 再證：

```text
count_U([1]) + count_V([2]) + count_W([0]) + emptyTotal = 2
```

因此六個 incidence regimes 中的 `(E,X,Z)=(3,0,2)` 與 `(3,1,1)` 現在都有保留空位的 cyclic normal form；連同原有 `(3,2,0)`，三-junction 分支已全數涵蓋。這仍是參數化環序定理，未聲稱 D5×S3 唯一代表分類。

## 一／兩 junction 的 ordered gaps（2026-09-12 續）

`Math/AttachmentOrder.lean` 已完成剩餘三個 scalar regimes 的參數化環序（**proved in Lean**）。`junction_tail_ordered` 從 shared junction 錨定其餘弦的線性次序；`singletonPackets_ordered_blocks` 將此順序提升到保留空 packet 的三段分解。`one_junction_tail_iff`、`two_junction_tail_iff` 是不限制 boundary 長度的雙向 list 定理。

在 valid cut-necklace 且三個 degrees 都至少二時，`NecklaceCuts.one_junction_normalForm` 給出 `(E,X,Z)=(1,4,0)` 的 C5 形式（q ∈ Fin 3，允許 boundary rotation）：

```text
[q+2,q] | [q] | [q+1] | [q+1] | [q+2]
```

`NecklaceCuts.two_junction_cyclic_gaps` 與 `two_junction_gap_inventory` 涵蓋 `(2,2,1)`、`(2,3,0)`：

```text
[q+2,q] · U · [q,q+1] · V · W
U、V、W 各只允許空 packet 或 singleton q、q+1、q+2
|U|+|V|+|W| = 3
V 中 [q+1] 至少一個，W 中 [q+2] 至少一個
三段 singleton 總數 + emptyTotal = 3
```

空 packet 的位置保留。連同三-junction 分支，六種 incidence regimes 現在都有參數化環序結果；這不等於 D5×S3 quotient 的十二類唯一代表或窮盡性定理。

## Geometry normal form → GeoReject bridge（2026-09-12）

**proved in Lean**：`Math/GeoRejectBridge.lean` 完成完整上界與等號結構。所有結論以 `RunOK w ρ` 為前提；`normalForm_rejection_bound` 另直接以 `AttachmentNormalForm w` 為前提。

| 定理 | 結論 |
| --- | --- |
| `runOK_rejection_le_three` | `|rejectionSet w| ≤ 3`。 |
| `runOK_three_rejection_degrees` | `|R|=3` 時有一個 degree 2 頂點，其餘兩個 degree 都是 3。 |
| `runOK_three_rejection_structure` | `|R|=3` 時存在 k、t，`N_k={t,t+1}`，其餘 degree 為 3，且 `R={t+2,t+3,t+4}`。保留原 C5 標號。 |
| `normalForm_rejection_bound` | normal form ⇒ `|R|≤3`，等號時 `R={t,t+1,t+2}`。 |
| `runOK_profile_ge_two` | 至少接受兩個三色 orbit。 |
| `runOK_two_profile_adjacent` | 恰好接受兩個時，`threeProfile w={t,t+1}`。 |

證明用 normal form 已推出的 fan 大小 ≤ 2 與共同鄰居 ≤ 1，無須再展開六種環序或十二類 shape：

1. 低 degree 分支沿用原有 `|R|≤2`。其餘分支由總 attachment ≤ 8 得到一個 degree 2 頂點 k。
2. `rejectionSet_subset_compl_of_degree_two` 證 `R⊆N_kᶜ`。在 `N_k` 上，pair witness 必須使用其餘兩點，造成三點 fan；opposite triple witness 則使 k 看到三類，需要 degree ≥ 3。兩者都矛盾，因此 `|R|≤3`。
3. 等號迫使 `R=N_kᶜ`。若還有第二個 degree 2 頂點，其鄰居集也等於 `Rᶜ`，共同鄰居便有兩個，違反 normal form。再用總數 ≤ 8 得到 `(2,3,3)`。
4. k 的兩個 attachment 若不相鄰，局部 C5 位置算術給出 opposite witness 至多一個位置；pair witness 位於另外兩點的共同鄰居，也至多一個。故此時 `|R|≤2`，等號 3 只能出現在相鄰 attachment，其補集正是 cyclic 3-interval。
5. 由既有 `threeProfile_eq_geo` 轉回染色語意，得到 profile 的兩個 corollaries。

`nonadjacent_opposite_le_one` 僅對兩個 `Fin 5` boundary indices 的位置算術用 `decide +kernel`；未枚舉 attachment words，未引用 `z5_profiles_checked` 或十二類觀察。

## 尚未完成與信任範圍

整體 12 個 D5×S3 shape classes 的窮盡性仍為 **computationally observed**；本 bridge 不需要此分類。一般 disk embedding ⇒ `AnnulusAccept` 的 topology completeness 仍為 **unresolved**，本輪不將結論外推到任意 disk patch。

本文件所有列名定理都是無 `sorry`、無 `native_decide` 的 Lean 證明；局部 Fin 3 packet 與 Fin 5 位置事實使用 kernel `decide`。完整依賴見 `artifacts/automata/lean-audit.txt`。normal form 與 `AnnulusAccept` 的等價不補上「任意 disk embedding ⇒ AnnulusAccept」的 topology completeness，也不建立 grammar 外的 graph-wiring soundness。

2026-09-12 驗證：`AttachmentOrder.lean` 已納入 `Math.lean`；補上兩處計數證明的 `List.count_nil` 簡化後，完整 `lake build` 通過（8795 jobs，仍有 linter warnings）。`lake env lean Math/AutomataAudit.lean` 通過；新增八項主要定理的依賴均限於 `propext / Classical.choice / Quot.sound`，沒有 native 依賴。實際審計輸出已更新至 `artifacts/automata/lean-audit.txt`。

2026-09-12 bridge 驗證：完整 `lake build` 通過（8796 jobs；新檔無警告，既有 `AttachmentOrder` linter warnings 保留）。`lake env lean Math/AutomataAudit.lean` 通過；新增 12 個定理的公理依賴均為 `propext / Classical.choice / Quot.sound`，沒有 `sorryAx` 或 native 依賴。實際輸出已更新至 `artifacts/automata/lean-audit.txt`。沒有重跑 word 枚舉或 topology 診斷。
