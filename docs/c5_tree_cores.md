# Degree-4 樹核心：排除分叉與至多一次 palette 切換

2026-09-17。接續 [odd-join 家族](c5_odd_join_cores.md)。
本輪把單缺失分離推進到另一個無界範圍：**內部圖是樹，且每個有效內點
在完整圖中的 degree 都等於 4**。此範圍包含不是 odd-join 的新核心。
方法是紙面 forcing minor 與有限拓撲證書；沒有新增 Lean theorem。

## 1. 結論與限制

設 G 是接受全部 T4 的 C5 disk graph，其非外圈邊集是 minimal q-obstruction，
q 是三色 singleton pattern。忽略孤立內點，令 H 為內部圖。
若 H 是樹，且每個內點的完整 degree 都是 4，則

`Σ(G)=Ω\{q}`。

更強的結構結論是：H 必為偶數頂點的路徑；其 list obstruction 可以寫成
一個非空 palette word，disk 條件使它至多切換一次，從而縮成至多六個內點。
二內點路徑另作空 word 基底。這裡的無界結論依賴以下紙面化約與 Python
模板覆蓋／拓撲證書，並非已形式化的普通定理。

對候選 A：某側若有此型 minimal obstruction，就有相應的單側 weak exit。
因此單側出口失敗時，該側的每個 minimal obstruction 除了不屬於 odd-join，
還必須有 degree≥5 的內點，或內部圖含 cycle。
一般單側、共同 pivotal edge、一般三出口與 K∞=K≤5 均未證。

## 2. 樹上的每條邊都有一個被迫顏色

固定 `q=01012`，D=3 是未使用色。其餘 q 可由 boundary rotation 及顏色置換
對齊。由既有 minimality 化約，每個內點的 boundary 鄰居 q 色互異，故

`L(v) = 四色 \ q(N_B(v))`，`D∈L(v)`，`|L(v)|=deg_H(v)`。

刪除樹邊 uv，得到兩個 rooted components。兩者都能延拓 q，因 G−uv 可延拓。
令它們在 u、v 的可取顏色集合分別為 S、T。原 G 不可延拓，所以任何
`s∈S,t∈T` 都相等；因此 `S=T={c_uv}`。
這定義每條內部邊的 palette `c_uv`。

在任意 v，其 incident palettes 全在 L(v)，且兩兩不同。
否則，某條邊的 palette 不在 L(v)，或與另一條相同，刪掉該邊仍不會釋放
v 的任何合法顏色，違反 minimality。因數量恰為 `|L(v)|=deg_H(v)`，
incident palettes 正好覆蓋 L(v)。這段直接由樹的獨立分支得出，不需額外
援引 Gallai list-assignment 分類定理。

## 3. 把任意 forcing subtree 壓成一點或兩點

以下 lemma 只用拓撲 minor，**不聲稱完整 relation 保持**。
設一個連通 rooted tree component F，在固定 q 下可著色，且 root 唯一可取色為 c。
所有內點 lists 都含 D。

### c=D

F 必須碰到每一個 q 使用色的 boundary 頂點。若未碰到色 A，將 F 內部的
D 與 A 對換不影響任何邊或相鄰 boundary 色，卻令 root 取 A，矛盾。
將 F 的所有內點收縮成一點，每個 q 色只留一條 spoke，就得到 `L={D}` 的單點。

### c=A≠D

Root 可以使用 D（沒有 boundary 使用 D），但 F 不能讓 root 取 D。
因此至少有一個 child component 唯一強迫 D；否則每個 child 都能避開 D，
可各自選 coloring 並拼回 root=D。保留其中一個，按上段收縮成 `L={D}` 的葉點。

對其餘兩個 boundary 色 B、C，root 不能取該色：

- 若 root 原有該色 spoke，直接保留。
- 否則必有 child component 唯一強迫該色。它至少碰到一個該色 boundary
  頂點，否則把該色與 D 對換便破壞唯一強迫性。將整個 child component
  收縮到 root，留下所需的該色 spoke。

強迫 D、B、C 的 children 彼此不同，branch sets 因而互不相交。
刪掉其他分支及多餘 spokes，得到兩點 rooted forcer：
root 的 list 是 `{D,A}`，相鄰葉點的 list 是 `{D}`。
整個操作不識別 boundary 頂點，確實是 disk/apex 圖上的 minor operation。

## 4. 所有分叉都產生同一種非 disk minor

若 H 有 degree-3 點 v，§2 給出三個分支分別強迫 D、A、B，v 有一條 C 色 spoke。
對三個分支用 §3 收縮，得到六內點的 Y 型：

```
內部 edges：01, 02, 23, 04, 45
lists：
0={D,A,B}, 1={D}, 2={D,A}, 3={D}, 4={D,B}, 5={D}.
```

若 v 的 interior degree=4，四個分支強迫 D、A、B、C，v 沒有 boundary spoke。
把 C-forcing 分支整個收縮到 v，保留它必有的一條 C 色 spoke，刪掉其餘 spokes；
其餘三個分支如上處理，仍得到同一個 Y 型。
Interior degree 不超過 4，因此涵蓋全部分叉。

固定 q，枚舉 `{A,B}⊂{0,1,2}` 與每個禁止色的一個實際 boundary 鄰居，
共有 **2,304 個 Y lifts，全部非 disk**。每個都保存 boundary-apex 圖中的
K5／K3,3 subdivision，checker 核對分支路徑真實邊、內部互斥與目標接線。
三種 palette assignments 另核對完整 relation 與逐邊 q-criticality；同一
assignment 的其他 lifts 有完全相同的 q lists。

因此 disk 的 H 不可能分叉。H 連通，所以必為路徑。
這裡 finite minor 的排除只需 disk，不需 minor 接受 T4。

## 5. 路徑可以變 palette，但不能來回切換

由 §2，路徑兩端的 incident palette 都是 D；每個 degree-2 內點的兩個
incident palettes 不同且其中一個是 D。因此整條路徑的 edge palettes 為

`D, a₁, D, a₂, D, …, a_t, D`，其中 `a_i∈{0,1,2}`。

H 有 `2t+2` 點；兩端 lists 是 `{D}`，每個 a_i 對應一對連續的 `{D,a_i}` 點。
稱 `a₁…a_t` 為 palette word。t=0 是既有二內點基底。

### 同 palette 必有相同實際 attachments

若兩個 `{D,a}` 點的 boundary neighborhoods 不同，保留它們和整條路徑兩端，
刪其他 spokes，收縮間隔路段，就得到上一輪 odd-join 型 I 的四內點 lift。
其 256 個不同中段 neighborhoods 的 lifts 都有非 disk 證書。
故對每個 palette a，所有相應中段點共用一組實際 boundary 鄰居。
此步不要求兩點原本相鄰，亦不只要求 q 色相同。

### 至多兩個 runs

任取兩個不同 palettes a、b 在 word 中依序出現的位置，保留各自的一對點
及兩端，收縮其餘路段。所得六內點 word `ab` 的所有 lifts 共 640 個，
只有 `01`、`10` 各一個是 disk；涉及 palette 2 的混合 word 全部非 disk。
這兩個 disk lifts 的完整 relation 都是 `Ω\{q}`。

因此若有混合，只有 palettes 0、1。若壓掉連續重複後至少三個 runs，必含
子序列 `010` 或 `101`。保留那三對點及路徑兩端，得到八內點 minor。
同-palette attachments 恆定後共有 128 個這類 lifts，全部非 disk，亦保存
subdivision 證書。因此只能是 `a…a` 或 `0…01…1`／`1…10…0`。

### 保存完整 relation 的縮減

每個 run 有偶數個中段點，共用相同的兩個實際 boundary 鄰居。
對任意 boundary coloring，允許色集 S 的大小至少 2；固定 run 兩側端點色，
上一輪的 even-path transfer 公式證明可把整個 run 換成兩點，完整 relation 不變。
各 run 可依序替換，外部端點不必在 S 中。另以路徑 minor 保證縮圖仍 disk。

單 run 落入 odd-join 四內點基底；兩 runs 落入上述六內點基底；空 word 落入
二內點基底。接受 T4 的各基底都只拒絕 q，證成 §1。
八個不同 run 長度的較長 lifts 另逐一核對全部 240 boundary rows 與 disk，
作為 relation-preserving 化約的獨立跨長度檢查。

## 6. 新的非 odd-join 家族與下一個循環阻礙

兩-run 基底不是 odd-join：其 quotient 只有一個 universal vertex，
而 `K2 ∨ C_(2m+1)` 至少有兩個。兩個 run 都可增長任意正偶數點，
得到另一個無界的單缺失家族。這些圖仍為 minimal q-obstructions：沿路徑的
edge palettes，由兩端向內的歸納表明，刪一條內部邊後兩個分量均可著色，
兩個新端點都強迫該邊的 palette；刪 spoke 則使其端點 v 獲得不在 L(v)
中的色 c，兩側分量的鄰點各強迫一個 incident palette，均不等於 c，故能拼回。
長度增加的 disk drawing 可在某 run 相同 attachments 的兩個中段點間，
用上一輪三邊路徑替換；兩側三角形 faces 保證此局部增長合法。

本輪也測了第一個有 cycle 的獨立 quotient：

1. 在 `{0,1,2,3}`、`{0,4,5,6}` 各取 K4，刪 `01`、`04`，加入 `14`。
2. 再加入鄰接全部七點的 vertex 7。

這是兩個 `K4−e` 接合後加 universal vertex 的具體八點圖。
全部 90 個 ordered triangles 在八個 automorphisms 下分成 24 個 orbits。
把每個 triangle 當三個 boundary 色類，完整展開得到 2,048 個 lifts；
48 個 disk，其中 32 個接受 T4，32 個全都只缺 q。
其中 16 個的全部內點 degree 為 4，這 16 個均接受 T4；其餘有 degree-5 內點。
所有 disk lifts 均核對完整 240-row relation、逐非外圈邊 q-criticality 與 rotation。
這只完整處理**這一個 quotient**，不是所有五內點的分類。

其中有全 degree-4、內部形狀為「三角形接兩節尾巴」的實例：

```
非外圈 edges：06, 15, 16, 17, 18, 28, 29, 39, 45, 46,
              56, 57, 78, 79, 89.
```

它不在本輪的樹定理內，也不是 odd-join（quotient 有八點），但仍只有一個缺失。
**下一個窄問題：** 對全 degree-4 的 Gallai 核心，加入一個 triangle／odd-cycle
block 後，能否把掛在 block 上的 forcing trees 化為有限 attachments，並保持
足夠資訊證單缺失？§3 只能保證 minor，不能直接拿它代替 relation-preserving
縮減；也不能假設一般 block tree 只有一個 cycle block。
含 degree≥5 的核心與共同 pivotal edge 仍為獨立缺口。

## 7. 重播與信任範圍

產物：[checker](../scripts/c5_tree_cores.py)、
[證書](../artifacts/c5_tree_cores/observations.json)。
新證書包含 2,304 個 Y lifts、768 個 palette-word lifts、2,048 個 cyclic-quotient
lifts 的完整枚舉紀錄，以及接受端 rotation／relation 和必要拒絕端 subdivisions。
另引用上一輪已封存的 256 個同-palette 不同接線排除例，核對來源 hashes。

```bash
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
uv run --with networkx==3.5 python scripts/c5_odd_join_cores.py --check
lake build
git diff --check
```

Python 模板覆蓋與 coloring 檢查、NetworkX 的 witness 搜尋、紙面 minor／disk
soundness、無界 forcing／path 歸納各有不同角色；沒有新增 Lean theorem。
未跑一般 k=5 或 k=6 圖枚舉，未重播全量 deletion audit。

驗證通過：新 checker 逐 byte 重播、odd-join checker、`lake build`
（8,820 jobs，僅既有 lint）、五份入口／報告的 150 個本地連結與 whitespace。
另直接核對兩-run 基底的 quotient 都只有一個 universal vertex，以及八個長圖
合計 272 次非外圈單刪均可延拓 q。本輪產物與 odd-join／tree／triangle 三輪成果一併納入本次發布提交。
