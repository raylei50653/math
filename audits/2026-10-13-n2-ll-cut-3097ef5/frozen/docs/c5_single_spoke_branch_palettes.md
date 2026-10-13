---
docgraph:
  id: c5.single-spoke-branch-palettes
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-bridge-path
---
# Single-spoke：旁支 palette 守恆與 q 路徑限制

後續（2026-09-27）：[旁支 K5 minor](c5_single_spoke_branch_minor.md) 已證
指定 (01,04,1234)、禁 3 者二接點分支的 p₁ 延拓；114 筆現為 64 筆
兩列已證、50 個指定查詢未決。下文保留原輪次結論及數字。

2026-09-27。接續 [奇數 bridge 路徑化約](c5_single_spoke_bridge_path.md)，
研究優先序見 [HANDOFF](HANDOFF.md)。

**結果是任意大小的必要限制，尚非 p₁ 延拓或來源排除。** 同一旁支在 q／p₁
下的每個 block palette 保持色 0、3 的 membership。主路徑上 q 的 bridge
palettes 因而只能依序為 `{a₁},{3},{a₃},{3},…,{aℓ}`，各 aᵢ∈{1,2}。
路徑外的第一個 block 只有下表五種 palette 配對，且各自需要具名實際接線。
114 筆配置的 62 筆雙列已證、52 筆各剩一列未決統計不變。

## 1. 完整前提與 rooted branch

完整沿用前報告 §1：finite simple induced-C5 disk、連通有效 H、
edge-minimal q=01012 obstruction、唯一 degree-5 點 z 及唯一 spoke zb0，
其餘內點完整 degree=4；H−z 分拆 (2,1,1)，實際支援為 (01,04,1234)，
禁 3 的 C=C₃ 有兩個原有序接點 (u,v)，來源接受 T4。假設仍拒絕 p₁=01021。
前報告給 C 的奇數長 bridge 路徑 x₀=u,…,xℓ=v，全部 b3 接線在路徑外。

使用同一 C 的三份拒絕 lists M0=(q,z=3)、M2=(p₁,z=2)、M3=(p₁,z=3)
及各自既存 block palettes；仍依賴 R10 的外部 degree-list 定理。
C 只有 bridges／odd cycles。從任一路徑點 r 向外取 incident block K，
以 K 與其所有遠離路徑的後代作一個 rooted branch，r 是唯一 root。
它不含 u、v（r 本身可以是其中之一）。支援 T 指所有非 root 頂點的
**實際** boundary 鄰點；不把 r 的接線算進 T。

前報告已證旁支的 M2、M3 palettes 相等，以下稱 P-palette；M0 稱 Q-palette。
保留原圖、完整 R_C、有序接點、所有 bridges 和嵌入次序；不把旁支收縮成色點。

## 2. Rooted palette 唯一性與固定色守恆

**唯一性。** 給定 rooted branch 所有非 root 頂點的 lists，其全部 block
palettes（若存在）唯一，不需給 root 的 list。從最遠 block 開始：任取
一個非 root 的 block 頂點，扣除已決定的後代 palettes，其 residual list
就是該 block palette。bridge 有一個這樣的頂點，odd cycle 至少兩個；
既有拒絕證書保證不同選點相容。逐層向 root 遞迴即可。
此為既存證書的唯一性，並不斷言任意 lists 都有證書。

**守恆。** 若兩份非 root lists 對某色 c 的 membership 逐點相同，則每個
block palette 對 c 的 membership 亦相同。用同一遞迴，lists 是 incident
palettes 的不交聯集；扣去後代 palettes 後，c 的剩餘 membership 相同。
這是對有限 rooted block tree 的歸納，不限制 branch 大小或環數。

在本題非 root 頂點沒有 z 邊，q、p₁ 都只有 b2 著色 0，且都不使用 3，
故兩份 lists 對 0、3 的 membership 逐點相同。守恆給每個旁支 block

```
0∈Q_K ⇔ 0∈P_K，   3∈Q_K ⇔ 3∈P_K。
```

bridge palette 大小一、odd-cycle palette 大小二，因此一般旁支內部
恰有 16 種滿足此必要代數條件的配對；不宣稱 16 種皆 disk 可實現。

## 3. 套回原奇數路徑

在路徑非端點，M2、M3 的路徑 residual list 均為 {2,3}；兩端分別
為 {3}、{2}。所以每個路徑點的所有旁支 P-palettes 聯集均包含於 {0,1}。
每個旁支 block 的 Q、P palette 大小相同，且對 0、3 守恆。原 lists
對 0 也相同，故扣除旁支後的 Q residual list 不含 0。

兩端 M0 不含 3，Q residual 大小一，必為 {1} 或 {2}。
非端點 M0 含 3，而所有旁支 Q-palettes 不含 3；Q residual 大小二，
必為 {1,3} 或 {2,3}。於是 q 下兩條 incident 路徑 bridges 恰一條色 3，
另一條色 1 或 2。從 u 端歸納得

```
Q(edge i) = {aᵢ}, aᵢ∈{1,2}，若 i 為奇數；
Q(edge i) = {3}，若 i 為偶數。      (i=1,…,ℓ)
```

這裡是 block palettes，不是已存在的 proper vertex coloring。
不同奇數邊的 aᵢ 尚不能視為相同，也不能各自自由選取。

## 4. 五種 root palette 配對與必要接線

只列與主路徑相接的第一個 block K；更深的 block 仍可使用其他配對。

| K | Q_K | P_K | branch 非 root 頂點必實際碰到 |
| --- | --- | --- | --- |
| bridge | {0} | {0} | b2 |
| bridge | {1} | {1} | b1 |
| bridge | {2} | {1} | b4 |
| odd cycle | {0,1} | {0,1} | b1、b2 |
| odd cycle | {0,2} | {0,1} | b2、b4 |

前兩節與 P_K⊆{0,1} 已窮盡配對。必要接線的證明也不限制 branch 大小：

- 若 Q_K 含 c、不含 3，而 q(T) 未見 c，交換 c、3 固定所有非 root lists。
  唯一性迫使 Q_K 在此交換下不變，矛盾。因此 Q_K 含 0 必碰 b2，含 2 必碰 b4。
- 若 T 不含 b1，則在 T⊆{2,3,4} 上 p₁=(1 2)∘q。
  全分支換色及唯一性迫使 P_K=(1 2)Q_K。兩種 Q_K=P_K 且含 1、不含 2
  的配對皆不滿足此式，故必碰 b1。

這些是原 branch 的實際支援限制，不是允許在 boundary 任意增加的邊。
同一 branch 可以碰更多框點；表中未禁止 b3，也未證全部支援可共同嵌入。

## 5. 局部證書、信任範圍與下一步

[checker](../scripts/c5_single_spoke_branch_palettes.py) 與
[artifact](../artifacts/c5_single_spoke_branch_palettes/observations.json) 核對：
16 個守恆配對、107 個局部 residual closure 案例、20 個路徑局部配置、
五種 root 配對的支援置換限制及四個 q 路徑轉移。
支援核對遍歷 T⊆{1,2,3,4} 及 24 個色置換；這是必要條件表，不是來源圖 cover。
任意大小結論由 §2–4 的歸納承擔；證據為紙面論證＋沿用外部 degree-list
定理＋Python 局部證書。未新增 Lean theorem。

```bash
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際檢查見 [研究紀錄](history/2026-09-27-single-spoke-branch-palettes.md)。
下一步將五種旁支的具名必要接線與原 slit-disk 次序合用，研究帶 b3 的旁支
能否和其餘旁支及 C₁、C₂ 共存。尚未證旁支可刪除、aᵢ 跨邊相等、有限
來源正常形或此分支 p₁ 延拓；一般 single-spoke、單側出口與主命題仍未證。
