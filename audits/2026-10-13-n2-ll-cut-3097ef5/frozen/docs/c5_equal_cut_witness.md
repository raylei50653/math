# 同一 disk 上同 cut 長度、不同重接的可實現反例

2026-09-15。接續 [cut 粗觀察](c5_cut_observations.md)。
**已構造具體反例：精確有理數平面嵌入＋完整合法染色＋maximal Kempe component
重播。下述是紙面證明與可重播有限證書，尚未 Lean 化。**

## 1. 被否定的充分性命題

即使固定同一 embedded C5 disk、同一 Kempe class、原色 boundary、三組
pairings、三組 cycle counts、同一 rooted 色對交換規則及 cut 長度，
仍不能決定交換後的 pairings、cycle counts 或一步相容性。

固定既有 survivor-811：22 頂點、58 邊、37 個三角面，boundary 為 `0,1,2,3,4`。
顏色 `A=0,B=1,C=2,D=3`；edge types `α=1,β=2,γ=3` 為端點顏色 XOR。
兩個完整染色（位置依序為頂點 0 至 21）為：

```text
c = (0,1,2,0,3,2,1,2,2,3,1,2,1,3,3,0,1,2,3,0,1,0)
d = (0,1,2,0,3,2,1,2,3,3,1,2,1,3,0,0,1,2,3,2,1,0)
```

共同 boundary 是 `(0,1,2,0,3)`，boundary edge word 是 `(1,3,2,3,3)`。
共同 source pairings（terminals 位於 boundary 邊內）為：

| system | source pairing | source cycles |
|---|---|---:|
| αβ | `(0,2)` | 1 |
| αγ | `(0,4),(1,3)` | 1 |
| βγ | `(1,4),(2,3)` | 1 |

兩者皆無一步 singleton-{1,3,4} escape。對兩者施行同一規則 `Comp_AB(0)`：

| source | 當前 maximal AB component | cut 長度 | 目標 αβ pairing | 目標 cycles | 目標無一步 escape |
|---|---|---:|---|---|---|
| c | `{0,1,10,12,15,16}` | **21** | `(0,4),(1,2)` | `(1,3,1)` | 否 |
| d | `{0,1,10,12,14,15,16}` | **21** | `(0,1),(2,4)` | `(1,2,1)` | 是 |

兩個目標 boundary 同為 `(1,0,2,0,3)`；αγ pairing 同為 `(0,3)`，βγ pairing
同為 `(1,4),(2,3)`。所以差異不是 boundary 改色或 system 名稱的全域置換。
c 的目標再交換 BC component `{2,7,20}` 即到 singleton-4。
d 的目標逐一檢查全部六色對的 maximal components，沒有一步禁止 escape。

因此前輪 196 transitions 上的「B + cut 長度無衝突」只是有限表的性質。
本例已在合法圖上反駁一般充分性。兩列各舊 component 的切邊數不同，
所以**沒有**同時反駁「再加各 component 切邊數」的更強觀察。

## 2. 為何確實是合法 disk 染色

[證書](../artifacts/c5_cells/equal_cut_witness.json) 的 `graph` 保存全部邊與有向
三角面，`geometry.coordinates` 給每個頂點一對**精確有理數**座標。
外框固定為 `(0,0),(4,0),(6,3),(3,6),(0,4)`，面積為 `51/2`。
座標由線性方程求出，但正確性不依賴線性方程必產生嵌入的定理：
[checker](../scripts/c5_equal_cut_witness.py) 的 `drawing` 用有理數行列式直接驗證：

1. 外框嚴格凸，17 個內部頂點都嚴格位於五條 boundary 邊的內側，22 個點互異。
2. 任一頂點都不位於非關聯邊上；全部 1,370 對無共同端點的邊不相交。
   這同時排除穿越與共線重疊；共同端點的邊也無重疊。
3. 37 個有向三角面面積皆正，任一面內不含其他頂點；內邊恰被兩面反向使用，
   外邊恰被一面使用，未配對邊正是指定 C5。
4. 三角面面積總和恰為 `51/2`。

**幾何證明。** 第 1–2 項给出在凸五邊形內的直線平面圖。第 2–3 項使三角面
內部兩兩不交：重疊若非共同邊／點，就必有邊交叉或一面的頂點落在另一面內；
共同邊的兩面由有向正面積與反向 incidence 位於兩側。所有面都在凸外框內。
第 4 項保證沒有遺漏區域：有限閉三角形聯集若漏掉內部一點，其補集含非空開集，
必有正面積，與面積相等矛盾；外框邊也已由第 3 項覆蓋。
所以這些三角形恰鋪滿凸五邊形，給出該具體圖的 disk 嵌入。

**染色與交換證明。** 對上列 c、d 逐條檢查 58 邊兩端異色。AB 誘導子圖中，
表列頂點集合連通，且沒有通往集合外 A/B 頂點的邊，因此恰為包含 0 的 maximal
component。交換 A/B 後再次逐邊驗證 proper coloring。其 cut 各有 21 邊，
dual 的三組 two-type 連通分量直接給出表列 endpoints 與 cycles；
另用「先刪 cut、保留 ports 分區、再加邊」的接口獨立重建，與直接結果相同。
這給出實際 disk 染色與合法操作，無需假設抽象 ports 分區可實現。

## 3. 同 class，且中間相容性也有見證

共同 seed 是既有 survivor-811 的第一個 aligned state。由 seed 到 c：
`AC {2,3,7,9,19,21}`，再 `CD {9}`。
由同 seed 到 d：`CD {8,14}`，再 `AD {9}`，再 `AC {2,3,7,14,21}`。
每個指定集合都在當時染色重新驗證 maximal；兩條歷史的每個狀態均無一步 escape。
反轉第一條再接第二條就是 **5 步 c→d** 的合法、逐中間相容路徑。
此相容性只量化一步，並不聲稱整個 Kempe class 封閉。

將 c 的 AB component 直接套到 d 並不合法；checker 有明確負控制拒絕它。
本例固定的是同一 rooted 選取規則，不是固定不變的 component 頂點集合。

## 4. 驗證與下一個缺口

```bash
uv run --with networkx==3.5 python scripts/c5_equal_cut_witness.py --check
uv run --with networkx==3.5 python scripts/c5_cut_observations.py --check
uv run --with networkx==3.5 python scripts/c5_cut_interfaces.py --check
lake build
git diff --check
```

證書保存有理數座標、逐面面積、完整 sources／targets、所有 cut 邊、各系統重接、
retained-port 分區、一步 escapes、同 class 路徑與來源／腳本 hashes。
`--check` 僅重播固定見證並逐 byte 比對，不重跑探索。
發現階段只延伸既有固定圖的 Kempe moves，未生成新圖或擴大 catalogue。

提交前驗證：本 checker、兩個 cut 前序 checkers、四個 edge 系列 checkers、
`lake build`、三份報告連結與 `git diff --check` 均通過；Lean 僅既有 lint 警告。

下一個未解問題是「再保留各舊 component 的切邊數」是否足夠；本例可被該資訊分開。
完整 ports 分區仍提供指定一步的精確重建，但未證最小性、多步充分性或常數大小界。
本成果不排除新的 C5 masks，也不證明 K∞=K≤5。
