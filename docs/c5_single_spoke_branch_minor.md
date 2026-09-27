# Single-spoke：旁支實際支援給 K5 minor 與 p₁ 延拓

後續（2026-09-27）：[單接點未用色守恆](c5_single_spoke_root_conservation.md)
已證 (012,04,234)、禁 3 者二接點的 p₂ 延拓；目前 66 筆兩列已證、
48 查詢未決。下文數字與停止點保留各原輪次語境。

2026-09-27。接續 [旁支 palette 守恆](c5_single_spoke_branch_palettes.md)
及 [奇數 bridge 路徑](c5_single_spoke_bridge_path.md)；研究優先序見
[HANDOFF](HANDOFF.md)。

**指定分支已證 p₁=01021 延拓。** 在 s=0、(S₁,S₂,S₃)=(01,04,1234)、
禁 3 者為二接點分量的原來源，若拒絕 p₁，任取主路徑的一條奇數位置
bridge 即給同圖 K5 minor。任意長旁支，包括所有 b3 接線，都可保留在
各自所屬的連通 branch set 中；不需逐一分類或刪除。
這排除的是額外拒絕 p₁，**不是排除此支援型的所有 q-obstruction**。

114 個具名配置中，交換兩個單接點分量名字的兩筆新接受查詢，使兩列
皆已證由 62 增至 **64**；20 筆只證 p₁、30 筆只證 p₂，尚有 **50** 個
指定查詢未決。19 種必要支援型不變。本輪未新增 Lean 定理。

## 1. 同一來源與反證前提

完整沿用 [completion §1](c5_single_spoke_completion.md#1-前提與保留的完整關係)：
finite simple induced-C5 disk、連通有效內點 H、edge-minimal q=01012
obstruction、唯一完整 degree-5 點 z、唯一 spoke zb0，其餘內點完整
degree=4，H−z 的接點分拆為 (2,1,1)，來源接受 T4。
按 q 禁色命名 C₁、C₂、C=C₃；其實際支援分別為 01、04、1234，
C 的原有序接點為 (u,v)。C₁、C₂ 各一接點，C 有兩接點。

若原 G 拒絕 p₁，則 C₁、C₂ 在 p₁ 都禁 1，且
F_C(p₁)={2,3}、R_C(p₁)={(2,3),(3,2)}；同時 F_C(q)={3}。
沿用前兩報告的三份同圖拒絕 lists、外部 degree-list 定理與其既存
block palettes。C 的 u–v 路徑 P=(x₀,…,xℓ) 全是原 C 的 bridges，
ℓ 為奇數，路徑點均不接 b3。Q 表 q,z=3 的 block palette。
P 的第 i 條邊在 i 奇數時 Q={aᵢ}、aᵢ∈{1,2}，偶數時 Q={3}。
這是 palette 證書，沒有把它解讀成 proper vertex coloring。

在 C₁、C₂ 中分別取一條實際 z–b1 路徑 D₁、z–b4 路徑 D₄。
各路徑從自己的原接點出發、終於實際 boundary 邊，內點在各自分量，
不經其他 boundary 點。兩路徑僅交於 z，且內點避開 C。

## 2. 每個路徑點的連通支撐

從 C 刪去 P 的全部 ℓ 條 bridge；令 Wⱼ 為含 xⱼ 的連通分量。
每條路徑邊都是 bridge，故 W₀,…,Wℓ 兩兩不交，且 Wⱼ 正是 xⱼ
加上其全部路徑外旁支。沒有合併不同路徑點，也沒有更改任何 boundary 邊。

**支撐引理。** 若奇數位置邊的 Q-palette 是 {a}，其兩端對應的 W
均有實際邊連至以下兩個具名框點：

| a | 兩個 W 各自必碰到 |
| --- | --- |
| 1 | b2、b4 |
| 2 | b2、b1 |

證明：在其中任一端 x，扣掉全部旁支 Q-palettes 後，q residual 是
{a}（x 是接點），或 {a,3}（x 是路徑內點）。令 d 為 {1,2} 中不同於
a 的色。色 0、d 都不在 residual 中，所以各自必由下列之一供應：

1. x 的原 boundary 接線已刪去該色；或
2. 某個路徑外 incident block 的 Q-palette 含該色。

原接點的 z=3 只刪去 3，不能供應 0 或 d。第一種中，色 0 只能來自
b2，因 C 不碰 b0；色 2 只能來自 b4；色 1 只能來自 b1，因路徑不碰 b3。
第二種使用前報告 §4 的五種入口配對：含 0 必有非 root 的 b2 實際鄰點，
含 2 必有 b4，含 1 必有 b1。該旁支全包含於同一 W，故結論成立。

此處只要求 W 連通並碰兩個框點，**不要求通往兩框點的路徑內點不交**。
尤其入口 odd cycle 的兩種接線可以在同一旁支內；把整個 W 作一個
branch set 即可。b3 接線可任意留在這些 W 內，不影響互不相交性。

## 3. 兩種 palette 的十條 K5 鄰接

固定任一奇數位置邊 xy=xᵢ₋₁xᵢ，令 A=Wᵢ₋₁、D=Wᵢ。
原路徑 P 加上 zu、zv 形成 simple cycle J；xy 是其一邊。
J−{x,y} 是非空連通路徑，包含 z；即使 ℓ=1，仍為 singleton {z}。
令 Z₀ 為此剩餘路徑加 D₁、D₄ 的所有內點（不含 b1、b4）。
Z₀ 連通、避開 A、D 及全部 boundary，且分別以原邊鄰接 A、D、b1、b4。
後兩條來自 D₁、D₄ 最後的 boundary 邊。

用以下五個 branch sets：

| Q(xy) | A | D | Z | X | Y |
| --- | --- | --- | --- | --- | --- |
| {1} | Wᵢ₋₁ | Wᵢ | Z₀∪{b1} | {b2} | {b3,b4} |
| {2} | Wᵢ₋₁ | Wᵢ | Z₀∪{b3,b4} | {b2} | {b1} |

它們皆非空、連通且兩兩不交。Z 中新增的 boundary 點，分別靠 D₁
或 D₄ 末邊及 b4b3 接回；第一列的 Y 由 b3b4 連通。
十條 pairwise adjacencies 如下，全部使用原來源邊：

| 所需鄰接 | Q(xy)={1} | Q(xy)={2} |
| --- | --- | --- |
| A–D | xy | xy |
| A–Z、D–Z | J 中 xy 兩端各自的另一條 cycle 邊 | 同左 |
| A–X、D–X | 支撐引理的兩條 b2 接線 | 同左 |
| A–Y、D–Y | 支撐引理的兩條 b4 接線 | 支撐引理的兩條 b1 接線 |
| Z–X | b1b2 | b3b2 |
| Z–Y | D₄ 的最後一邊 | D₁ 的最後一邊 |
| X–Y | b2b3 | b2b1 |

因此兩種 a 都給 K5 minor，與來源 disk embedding 的平面性矛盾。
boundary 次序用在 b1b2、b2b3、b3b4 這些**原框邊**；沒有新增跨框邊。
最後的非平面 witness 可以把 boundary 點放進 branch sets，這不是
宣稱保持完整 boundary 關係的壓縮。C₁、C₂ 與 C 的著色關係從未合併。

故 p₁ 必延拓原 G。具體說 F_C(p₁) 不能同時含 2、3，至少一個可作
共同 z 色；在三個原分量各選避開此色的完整 tuple／內部 coloring 再
接合。此論證不指定永遠可用 z=2 或永遠可用 z=3，也不取接點 marginals
的乘積。p₂ 延拓沿用已完成的外部雙路徑 completion。

## 4. 重播證書與更新範圍

[checker](../scripts/c5_single_spoke_branch_minor.py) 與
[artifact](../artifacts/c5_single_spoke_branch_minor/observations.json) 包含：

- 前報告全部 20 個路徑局部型，逐一由實際接線／旁支必要支援推出 §2。
- 360 份具名 K5 控制：路徑長 1、3、5、7 的每條奇數邊、兩種 palette、
  兩端各三種支撐形狀（直接邊、分開 bridges、共用 cycle）與兩種外部路徑長。
  每份保存原邊、五個 branch sets、連通／不交檢查及全部十條鄰接 witness。
- 繼承 completion 的 114 筆具名配置及輸入 SHA256，只更新 source_index
  24、29 的 p₁ 接受結論；兩筆只差單接點分量名字，未另枚舉反射來源。

360 份是抽取形狀的拓撲控制，**不是完整 degree-4 來源、list 實現或來源圖
cover**。任意長度、任意大小旁支的證明是 §2–3 的同圖連通集合抽取。
信任層是紙面證明＋沿用外部 degree-list 定理＋Python 局部／minor 證書；
未新增 Lean theorem，`lake build` 不將上述 disk／minor 論證形式化。

```bash
python3 scripts/c5_single_spoke_branch_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證見 [研究紀錄](history/2026-09-27-single-spoke-branch-minor.md)。
下一窄入口是 s=0、(S₁,S₂,S₃)=(012,04,234)、C₃ 二接點的 p₂ 查詢
（原 source_index 23、交換單接點名字為 28）：completion 已證 C₃ 不禁
0、3，但 C₁(p₂) 的單接點完整關係尚未控制；p₁ 已證。
先研究 C₁ 在 p₂ 能否禁 3；若不禁，z=3 即給原圖延拓。保留其 b0、b1、b2
實際支援及與 C₂／C₃ 的次序。
其餘 t=1 分拆、t=0、一般單側／共同出口與 `K∞=K≤5` 仍未證。
