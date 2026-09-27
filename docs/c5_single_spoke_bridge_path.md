# Single-spoke：雙禁色強迫奇數 bridge 路徑

後續（2026-09-27）：[旁支 K5 minor](c5_single_spoke_branch_minor.md) 已證
指定 (01,04,1234)、禁 3 者二接點分支的 p₁ 延拓；114 筆現為 64 筆
兩列已證、50 個指定查詢未決。下文保留原輪次結論及數字。

後續（2026-09-27）：[旁支 palette 守恆](c5_single_spoke_branch_palettes.md)
已給 q 路徑交替限制與五種旁支入口配對的實際接線要求；仍未排除本分支。

2026-09-27。接續 [外部雙路徑 completion](c5_single_spoke_completion.md)
的指定入口；研究優先序見 [HANDOFF](HANDOFF.md)。

**結果是任意大小的必要化約，尚非排除。** 若 s=0、支援
(S₁,S₂,S₃)=(01,04,1234)、C=C₃ 為二接點的來源仍拒絕 p₁=01021，
兩個原接點 u、v 間必為奇數長的 bridge 路徑。該路徑沒有 b3 鄰點；
實際支援要求的全部 b3 接線都在路徑外旁支。114 筆的已證查詢數仍為
62 筆兩列已證、52 筆各剩一列，沒有據此刪除支援型。

## 1. 前提與三份同圖 lists

完整沿用 completion §1：finite simple induced-C5 disk 來源、連通有效
內部 H、edge-minimal q=01012 obstruction、唯一 degree-5 點 z，唯一
spoke zb0，其餘內點完整 degree=4，H−z 分拆 (2,1,1)，並接受 T4。
C₁、C₂、C 的實際支援依次為 01、04、1234；C 的有序接點為 (u,v)。

前輪已證 p₂ 延拓。若 p₁ 拒絕，C₁、C₂ 均禁 1，故
F_C(p₁)={2,3}、R_C(p₁)={(2,3),(3,2)}；同一 C 有 F_C(q)={3}。
保留每點實際 boundary 鄰居 A(x)，以及全部中間 bridges。
三份被拒絕的 degree lists 為

```
M0(x) = U \ (q(A(x)) ∪ ({3} if x∈{u,v} else ∅)),
M2(x) = U \ (p₁(A(x)) ∪ ({2} if x∈{u,v} else ∅)),
M3(x) = U \ (p₁(A(x)) ∪ ({3} if x∈{u,v} else ∅)).
```

由 [R10 §2](c5_degree5_interfaces.md#2-gallai-結構tight-lists-與-block-palettes)，
三份 lists 都 tight；C 是只有 bridges／odd cycles 的 Gallai tree，K4
排除沿用 [single-spoke 必要化約](c5_single_spoke_cores.md) §3。
各份 lists 具有 block palettes，交於同點的 palettes 互斥且聯集等於 list。
這裡依賴既有外部 degree-list 定理，不新增該定理的證明或形式化。

在非接點 M2=M3；在兩個接點，tightness 迫使 boundary 色避開 2、3，
所以 M2\M3={3}、M3\M2={2}。尤其接點不接 b3。

## 2. 沿同一 block-cut tree 比較兩份 palettes

考慮同一 C 的 vertex–block incidence tree（保留非 cut 頂點作葉節點），
以及其中 u 到 v 的唯一路徑。先由外向內消去不在這條路徑上的分支。

每個待消去的末端 block 除保留的接合點外都不含 u、v。其私有點經先前
消去後的 residual lists 在 M2、M3 下相等，而該 residual list 恰等於
這個 block 的 palette。因此兩份 palette 相等；從接合點扣除的集合也
相等。逐次消去保持「只有 u、v 的 residual lists 不同」。此過程比較
兩份既存拒絕證書，不收縮來源圖，也不丟棄原分量關係。

路徑上的第一個 block 在 u 的 palette 必不同，因 u 此時只 incident
於它，而 residual lists 仍差 {3}/{2}。若前一個 block 的 palettes
不同，在下一個非接點的同一 residual list 中取補集，下一個 block 的
palettes 也必不同。故 u–v 路徑上的每個 block 都具有不同 palettes。

若其中一個 block 是 odd cycle，它在 incidence 路徑上只使用兩個
頂點。另有至少一個頂點 w 不在路徑上；w 不是 u、v，消去其外掛分支
後，w 的兩份 residual lists 相等，且恰等於此 cycle 的 palette。
這迫使兩份 cycle palettes 相等，矛盾。所以路徑上全部是 bridge blocks。

回到原 C，得到唯一的 u–v 路徑 x₀=u,…,xₗ=v，且每條邊都是原 C
的 bridge。所有 cycle blocks 都在此路徑外；並未將它們刪掉或宣稱不存在。

## 3. 奇偶性與 b3 接線的位置

每條 bridge 的 palette 是 singleton。按 M2、M3 的順序記錄其色對。
u 端只有第一條 bridge 尚未消去，residual lists 大小均為一，故第一條
bridge 的色對是 (3,2)。

在中間點 xᵢ，剩下兩條 bridge；兩份 residual lists 相同，且各份的
兩個 singleton palettes 互斥。因此若入邊色對是 (a,b)、a≠b，出邊
只能是 (b,a)。從 (3,2) 開始，沿路交替 (3,2)、(2,3)。v 端同樣要求
(3,2)，所以 ℓ 必為奇數。這個歸納不限制路徑長度。

每個中間點的 residual list 恰為 {2,3}，故其原 M2、M3 均包含 2、3。
若它實際接 b3，p₁(b3)=2 會刪去 2，矛盾。兩端接點已由 tightness
排除 b3。於是路徑沒有 b3 鄰點。由 S_C=1234，至少一個 b3 鄰點必在
路徑外，且其連通旁支只經一個路徑頂點接回；否則會使路徑邊不再是 bridge。

q 的拒絕尚未用來排除這些旁支。旁支在 p₁ 的兩份 palette 相等，但在
q 下可能改變，不能把它視作固定色的獨立端點條件或任意收縮。

## 4. 有限局部核對與停止點

[checker](../scripts/c5_single_spoke_bridge_path.py) 與
[artifact](../artifacts/c5_single_spoke_bridge_path/observations.json)
窮盡 A(x)⊆{1,2,3,4} 及接點／非接點身份，在完整 degree=4 與三份
lists tight 的条件下恰有 16 個局部型；另核對 12 個不同入邊色對的
交替轉移。長度 1–8 僅是奇偶負／正控制，任意長度由 §3 歸納承擔。
這不是來源圖枚舉、disk 實現證書或任意大小有限 cover。

證據為紙面任意大小 palette 比較＋沿用外部 degree-list 定理＋Python
局部核對。完整有序 R_C 仍保留；沒有新增 Lean theorem。

```bash
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證見 [本輪紀錄](history/2026-09-27-single-spoke-bridge-path.md)。
下一步：在同一奇數 bridge 路徑與實際旁支上，比較 q,z=3 與 p₁,z=2／3
的 residual palettes，處理所有 b3 接線所在的旁支；保留 b1、b2、b4
接線及 slit-disk 次序。尚未證旁支可刪除、有限正常形或本分支 p₁ 延拓。
其他 52 個查詢、一般 single-spoke／單側出口及主命題仍開放。
