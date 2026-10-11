---
docgraph:
  id: c5.single-spoke-two-contact-bounds
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-root-sweep
    - c5.single-spoke-completion
    - c5.single-spoke-branch-minor
---
# Single-spoke：剩餘二接點上界的共同分類

後續（2026-09-27）：[單接點上界分類](c5_single_spoke_single_contact_bounds.md)
已關閉剩餘 16 個查詢，114 筆全部接受兩個指定 p；下文保留本輪數字。

2026-09-27。從 [root sweep](c5_single_spoke_root_sweep.md) 的 34 個
`open_queries` **只抽取含 component 0 unknown bound 的 18 個**。
研究優先序見 [HANDOFF](HANDOFF.md)。

**18 個查詢全部接受：4 個由完整關係的色對稱／容量、6 個由外部路徑與
既有旁支 K5 抽取、8 個由二接點未用色對的 bridge 障礙。**
直接落入原 3,492 項 completion 的是 **0 個**；不能把新關閉歸功於該有限 cover。
114 筆現為 **98 筆兩列已證、4 筆只證 p₁、12 筆只證 p₂**，剩餘 16 查詢
全是單接點上界。本輪沒有刪除支援型，也不斷言支援型可實現或來源不存在。

## 1. 前提、關係與反射的精確意義

完整沿用 [completion §1](c5_single_spoke_completion.md#1-前提與保留的完整關係)：
有限簡單 induced-C5 disk、連通有效內部 H、edge-minimal q=01012 obstruction、
唯一完整 degree-5 點 z、唯一 spoke zb_s，其餘內點完整 degree=4，H−z
分拆 (2,1,1)，並接受 T4。C=C₀ 的有序接點是 (u,v)，其餘 C₁、C₂ 各有
原接點 r₁、r₂。Sⱼ 是 actual support，F_C(q)={a}。
依既有 R10，C 是 K4-free Gallai tree，blocks 為 bridges／odd cycles。

全程保留 `R_C(b)⊆U²`，
`F_C(b)={d : 每個 (x,y)∈R_C(b) 都有 d∈{x,y}}`；不以 marginals 替代。
R 非空給 |F|≤2。若 F={d,e}，R10 的逐接點解除另給
`R={(d,e),(e,d)}`，不是從兩個投影獨立拼接而來。
來源圖未知，不能列出每一頂點的實際路徑或未知 R 的數值表；artifact
保存原 placements、接點座標、條件式完整 relation 與各路徑的具名分量／末邊來源。

反射用既有 ρ=(3,2,1,0,4)、π=(0 1)，在**同一圖**搬運支援、環序、
路徑及每個完整 tuple，`R'(Tb)={(πx,πy):(x,y)∈R(b)}`。
接點座標仍具名 (u,v)，幾何環序反轉不等於丟掉或任選 tuple 座標。

特別區分兩種 orbit：表中 9 組可按 **target 的相等分割**分成 6 個
幾何／角色 reflection orbits；但 `Tp₁=21010`、`Tp₂=02012`，不是原
具名的 p₂、p₁。這 6 組不能直接當作固定 q 的逐色查詢等價。
若連 target 的字面色也保留，9 組各有反射像，像不在原兩個 target 列中。
artifact 同時存 raw transported target；以下需要的推論均直接驗證前提，
不偷偷只對 target 換色而固定 q。本輪沒有重新枚舉反射來源。

## 2. 九組與 completion 失敗原因

支援欄依 q 禁色角色遞增排列；a 是其中二接點角色。每列兩個 index
只交換 C₁、C₂ 名字，兩份原 slit-disk 次序都保留。

| s | 支援（依 q 角色） | a | target | source_index | 失敗原因 | 關閉方法 |
| --- | --- | ---: | --- | --- | --- | --- |
| 0 | 012 / 04 / 234 | 1 | p₂ | 4,9 | 碰 singleton；q 角色不符；路徑缺口 | 未用色對 |
| 1 | 123 / 34 / 014 | 0 | p₁ | 40,51 | 碰 singleton；反射 q 角色不符；路徑缺口 | 未用色對 |
| 1 | 01 / 04 / 1234 | 3 | p₁ | 84,95 | 碰 singleton；路徑缺口 | 外部路徑 K5 |
| 4 | 123 / 34 / 014 | 0 | p₁ | 107,127 | 碰 singleton；反射 q 角色不符；路徑缺口 | 未用色對 |
| 4 | 014 / 12 / 234 | 0 | p₁ | 113,133 | 反射 q 角色不符 | 色對稱容量 |
| 4 | 04 / 012 / 234 | 1 | p₂ | 146,166 | 碰 singleton；q 角色不符；路徑缺口 | 未用色對 |
| 4 | 12 / 234 / 014 | 1 | p₂ | 155,175 | q 角色不符 | 色對稱容量 |
| 4 | 23 / 34 / 0124 | 3 | p₂ | 186,206 | 碰 singleton；路徑缺口 | 反射後外部路徑 K5 |
| 4 | 04 / 01 / 1234 | 3 | p₁ | 195,215 | 碰 singleton；路徑缺口 | 外部路徑 K5 |

幾何 orbit 的非平凡配對為 (107,146)、(113,155)、(186,195)，代表 index
各自包含交換單接點名字的一筆；其餘 4、40、84 的反射 spoke 是 3、2、2，
不在三個代表 spoke 的表中。逐色限制如 §1，不能由幾何配對直接宣稱接受搬運。

先逐筆嘗試原 completion：p₂ 用原 frame，p₁ 用既有 completion 的反射
frame，檢查 C 避 b0、q 禁 0 或 3、外部 z–b1／z–b4 路徑。
4 個容量分支有指定路徑，但 q 禁色角色不符；其餘 14 筆除碰 singleton
外，還缺少這組指定端點的路徑證據。表中「路徑缺口」只指原 completion
frame 的 z–b1／z–b4，不能和 §4 的 K5 frame 混用，也不宣稱沒有其他 minor。
全部 3,492 接線的 q、p₂ 完整 tuples 及反向座標仍重播核對，但無一查詢
能直接引用這個 cover。尤其不能刪掉 C 接 singleton 的實際邊來強行套用：
那會改動完整關係及 degree／minimality 前提。

## 3. 色對稱容量：四個查詢

若 p 在 S_C 不用某組色 D，D 的任意置換都逐點作用於**整份** R_C(p)，
故 F_C(p) 對它不變。反設整圖拒絕 p，先以其他兩分量的已知 F 算出
C 必禁的集合 B，再取 B 在這些置換下的閉包。閉包超過兩色即矛盾。

- 113、133：C 支援 014，p₁ 未用色為 {2,3}。原 spoke 與其餘兩分量
  迫使 B={0,2}，對称閉包 {0,2,3} 超過二接點容量。
- 155、175：C 支援 234，p₂ 未用色為 {0,3}。必禁 B={0,1}，
  閉包 {0,1,3} 同樣不可能。

這裡不能將 F 的逐色上界各自刪小後冒稱固定 z 色可用；結論是 B 中
至少有一色不被禁，取該色在三個原分量各選完整 tuple 再接合。
不需要 topology，也沒有聲稱 C 的 F 全空。

## 4. 旁支 K5 的共同版本：六個查詢

既有 [bridge 路徑](c5_single_spoke_bridge_path.md)、
[旁支 palettes](c5_single_spoke_branch_palettes.md) 與
[K5 抽取](c5_single_spoke_branch_minor.md) 的實際局部前提可寫成：

- C 支援 1234，q 禁 3，原有序接點 (u,v)；
- 目標在此支援為 `p=(0,t,0,h,t)`，{t,h}={1,2}（b0 的色不參與 C）；
- C 在 p 同時禁 h、3；
- C 外有只交於 z 的實際 z–b1、z–b4 路徑。

這些前提已足夠給 K5；不需原 spoke 是 b0，也不需外部單接點禁色相等。
原證明是 t=1。t=2 不藉由不合法的「只換 target 色」推出，而如下共同證明。
兩個目標拒絕 lists 比較，迫使 u–v 是奇數 bridge 路徑，P-palettes
依序在 h、3 間交替，路徑沒有 b3 鄰點。每個旁支的 Q、P palette 對
0、3 守恆，因兩列在 C 都只有 b2 使用 0、都不用 3。
旁支 P⊆{0,t}，相應五種 (Q,P) 是

```
({0},{0}), ({1},{t}), ({2},{t}), ({0,1},{0,t}), ({0,2},{0,t}).
```

Q 含 0 迫使實際碰 b2，含 2 迫使碰 b4，皆由 q 的未用 3 對稱及 rooted
palette 唯一性。Q 含 1 則必碰 b1：若不碰，在 234 上 q→p 的色置換
固定 0、3 且把 1 送 h、2 送 t，與上述 P 含 t 而不含 h 矛盾。
故原五種旁支 tether 引理對 t=1、2 均成立。

q 路徑 palettes 仍是奇數邊 a∈{1,2}、偶數邊 3。任一奇數 bridge
兩端連同各自全部旁支成 W、W'，均碰 b2 及 b4（a=1）或 b1（a=2）。
其餘 cycle 路徑加兩條外部路徑的內點成 Z₀。以下五個原圖連通集合給
既有十條 K5 鄰接，邊與連通／不交證明完全沿用原抽取：

| a | 五個 branch sets |
| --- | --- |
| 1 | W，W'，Z₀∪{b1}，{b2}，{b3,b4} |
| 2 | W，W'，Z₀∪{b3,b4}，{b2}，{b1} |

zb0 不在任何必要鄰接中。checker 從舊控制刪去這條邊，並允許外部路徑
內點數 0（原 spoke），重驗 540 份抽取控制。它們不是來源圖 cover。

84、95 與 195、215 在原圖使用 t=1：其他分量與 spoke 使 C 必禁 {2,3}。
84 可由原 spoke 到 b1、支援 04 的分量到 b4；195 可由支援 01 的分量
到 b1、原 spoke 到 b4（也保留其他選擇）。
186、206 必禁 {0,3}；反射原圖後，C 支援 1234，q 仍禁 3，
**實際 target 是 02012、必禁 {1,3}**，正是 t=2、h=1。
反射後支援 01 的分量通 b1，原 spoke b4 或支援 04 的分量通 b4。
沒有重新枚舉反射側或誤稱 target 已是 p₁。

所有路徑都從對應原接點沿其連通分量至實際 boundary 鄰點，再走原末邊。
兩條非 spoke 路徑使用不同分量，故只交 z，避開 C；不假設同分量可提供
兩條內點不交路徑。接合著色時，外部分量仍各用自己的完整單接點關係。

## 5. 二接點未用色對的 bridge 障礙：八個查詢

**引理。** 在同一二接點 Gallai 分量 C，假設 q 禁 a，d≠a，
d 不在 q(S_C)∪p(S_C)，並存在 e≠a,d 也不在 q(S_C)。則 d∉F_C(p)。
此結論不需外部路徑，也不需猜測來源大小或逐 source_index 分類。

反設 p 禁 d。令 M=(q,z=a)、N=(p,z=d)，兩份均為既有 tight 拒絕
lists，具 block palettes Q、P。在 u、v，色 d 的 membership 是 M 有、
N 無；其餘所有頂點兩份 lists 都有 d。

在 block incidence tree 的 u–v 路徑外，從葉向根消去；單接點 root
守恆的同一歸納保證所有旁支 Q、P 對 d 的 membership 相等。
第一個路徑 block 在 u 的 membership 差因此是 +1。
每個中間點的 incident palettes 是不交聯集；原 list 的 d membership
相等，扣掉旁支後，下一路徑 block 的差是前一個的負值，始終非零。
若遇 odd-cycle block，其路徑外的第三頂點不是 u、v，扣掉其旁支後
兩份 residual 對 d 相等，迫使該 cycle 的差為零，矛盾。
故 u–v 之間只能是 bridges；第一條 bridge 的 Q palette 必含 d
（繼續傳遞還會給奇數長，但不需要用這個更強結論）。

另一方面，M 的**每個頂點 list** 都在交換 d、e 下不變：boundary 不用
兩色，接點只額外刪去 a。Rooted palette 唯一性（任取頂點作根）迫使
每個 Q block palette 都在該交換下不變。一個 bridge 的 palette 是
singleton，不能含 d 或 e。與第一條 bridge 含 d 矛盾，證畢。

這是同圖 block-tree 障礙；無需額外 K5。若只套原單 root 引理會失敗，
因另一接點的 membership 也變了；這裡正面處理兩接點間的唯一路徑。

本表八個查詢均取 d=3、e=2：C 的 q 支援只見 {0,1}，a 是 0 或 1。
在 p 下其他兩分量的已知 F／必要上界均不含 3，且 spoke 不用 3。
因此引理直接給共同 **z=3**，三個原完整 tuples 接合證延拓。
C 支援012的四筆為4、9、146、166；支援123的四筆為40、51、107、127。
實際 singleton 接線、全部中間 bridges、旁支、contact order 均未刪除。

## 6. 重播、信任範圍與停止點

[checker](../scripts/c5_single_spoke_two_contact_bounds.py) 與
[artifact](../artifacts/c5_single_spoke_two_contact_bounds/observations.json)
保留輸入 SHA256、18 個完整繼承記錄、9 組／6 幾何 orbits、raw 反射列、
actual supports、placements、ordered contacts、路徑分量身份、completion
失敗原因及三種關閉證據。重播 3,492 項既有完整 relation cover；另核對
65,535 個非空 ordered binary relations 的容量、membership 交替局部代數、
兩種 target 的旁支 tether 必要支援，以及 540 份不使用 zb0 的 K5 控制。
這些有限核對不取代 §4–5 的任意大小證明。

證據層：**紙面任意大小論證＋沿用外部 degree-list／既有 K4-free 結構＋
Python 完整關係與局部 minor 控制**；反射使用既有關係搬運。
未新增 Lean theorem；`lake build` 不形式化新 palette／disk 論證。
原 sweep、completion 及 3,492 項 artifacts 均保持原樣，新表另存。

```bash
python3 scripts/c5_single_spoke_two_contact_bounds.py --check
python3 scripts/c5_single_spoke_root_sweep.py --check
python3 scripts/c5_single_spoke_branch_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證見 [本輪紀錄](history/2026-09-27-single-spoke-two-contact-bounds.md)。
下一步只看新 artifact 的 16 個 `open_queries`：二接點未知上界已全部
處理，剩單接點支援見滿色的實際 root 接線／他分量路徑問題。
其餘 t=1 分拆、t=0、高 degree／多 degree-5、一般核心存在／分離、
一般單側／共同出口及 K∞=K≤5 仍未證。
