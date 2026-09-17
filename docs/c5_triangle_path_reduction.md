# Triangle 加任意長路徑枝：bridge 介面化約

後續狀態（2026-09-17 文件整理）：本文的外掛樹分叉停止點已由
[第一分叉排除](c5_triangle_forks.md) 處理；下文「仍未解」指本輪當時狀態。現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [root 介面探索](c5_root_interfaces.md)。
**路徑枝的長度缺口已可封口；外掛樹的分叉仍未解。**
結論是紙面 forcing／minor／transfer 化約加 Python 有限證書，未新增 Lean theorem。

## 1. 條件式一般結論

設 G 是接受全部 T4 的 C5 disk minimal q-obstruction，全部有效內點完整
degree=4，內部圖的唯一 cycle 是 triangle。若每個掛在 triangle 上的 tree
都是從接枝點開始的一條路徑，則

`Σ(G)=Ω\{q}`。

路徑長度沒有上界。任一枝可用保留其原 root 與末端 leaf 的兩點枝取代：
這保持全部 boundary rows 的 bridge 介面，且縮圖是 boundary 不識別的 minor，
因此仍是 disk。可依序縮全部枝，再套用既有 canonical triangle 分類。
本結論不涵蓋接枝 root 或更深處有分叉的樹、更多 cycle blocks 或 degree≥5。

前輪 standalone disk 四點反例仍有效；新的正結論需要整個 triangle context。
「同 palette 必有相同 attachments」也不是正確的中間引理：前輪 108 個
合法接合中，有 32 個包含實際接線改變。

## 2. 先取 canonical endpoint minor

固定 q=01012，D=3。由 [triangle 報告 §1](c5_triangle_branches.md)，
共同 triangle palette 含 D，外接 branches 至多兩條，且在不同 triangle 頂點。
每條 bridge 刪除後兩側各唯一強迫同色；初始 branch 色 c 不在 triangle palette，
所以 c≠D。

在路徑內點，incident edge palettes 兩兩不同並覆蓋其 q list：否則刪某條邊
不會釋放顏色，違反 minimality。每個非葉 path 點的 list 含 D 且大小為 2，
leaf list 是 {D}。因此從 virtual parent edge 到 leaf 的 palettes 必為

`c,D,a₁,D,a₂,D,…,D`。

Root list 是 `{D,c}`；其後每個 a 對應一對 `{D,a}` 點；末端為 `{D}`。
特別地，非葉點總數是奇數，枝至少有兩點。

刪去所有中間點的 boundary spokes，再把 root 到 leaf 間的路段收縮，保留
root、leaf 的原 spokes，得到兩點 c-forcer。對全部枝做此操作，所得圖就是
上一輪 one／two_distinct canonical grammar 的一個 lift。其 q lists 仍是該
minimal obstruction 的 canonical lists；disk 由 minor 閉性保持。
故（經 triangle 標號對齊）必為已完整分類的 **18 個 disk templates** 之一。
這一步只用 minor，還沒有宣稱完整 relation 保持。

零枝的 triangle 已在既有 [小核心分類](c5_weak_list_cores.md) 處理。
以下均固定至少一枝，並保留 canonical base 的原 root／leaf 接線。

## 3. 排除 palette 切換：120 個固定 minor

假如某條枝有 palette a≠c 的非葉點，保留：

1. 該枝 root，list={D,c}；
2. 一個較後的 `{D,a}` 點；
3. 原末端 leaf，list={D}。

其餘枝縮成 canonical 兩點枝；目標枝其餘非葉點先刪 spokes，再沿路徑收縮。
保留三點依次形成 path。它不必仍是 q-obstruction：只要它是非 disk minor
就足以排除原圖。

對 18 個 canonical bases 的 20 個 slots，固定原 root、leaf，完整列出 a≠c
及中間點實際 boundary 鄰居，共 **120 個模板，全部非 disk**。
每個都保存並逐路徑核對 boundary-apex 圖內的 K5／K3,3 subdivision。
所以任意長原枝的全部非葉點，palette 都是 c。

18 個 bases 只有 c=0 或 c=1，且 triangle palette 都是 {D,2}。
對固定 c，非葉點只有兩種實際 neighborhoods：

- c=0：{1,4} 或 {3,4}；
- c=1：{0,4} 或 {2,4}。

這是固定 q 與有序 boundary 下的陳述；其他 singleton 可旋轉並整體換色對齊。

## 4. 接線最多換一次，而且第一段只有一點

令 X 是原 root 的 neighborhood，Y 是另一種；把非葉點的 neighborhoods
依路徑寫成 X/Y word。

若至少三個 runs，可保留最前方的 X、稍後 Y、再後 X 及 leaf，得到
`X,Y,X,leaf` minor。20 個 slots 的這種模板**全部非 disk**，均保存 subdivisions。
因此最多兩個 runs。

兩個 runs 若存在，把各自收縮成一點，得到 `X,Y,leaf` minor。
20 個模板有 8 個 disk，其餘 12 個保存 subdivisions；8 個 disk 全在單枝 base。
所以雙枝 triangle 的每條枝都只能有一個 run。

在上述 8 個單枝 contexts，若第一 run 至少有兩點，可取
`X,X,Y,leaf` minor。**8 個全非 disk**，也都保存 subdivisions。
故兩-run 的唯一可能形狀是

`X,Y^(2m),leaf`，m≥1。

偶數指數由非葉總數為奇數推出。接線確實可以變，但只能在 root 後改變一次。
這個形狀是必要條件；本輪不另外聲稱所有長度的這類擴張都有 disk drawing。

## 5. 保持 bridge 介面的有限縮減

固定任意 proper boundary coloring b。同 neighborhood run 的共同可用色集 S
至少有兩色，因它只有兩個 boundary 鄰居。固定 run 兩側外部端點色後：

- |S|=2 時，run 沿路徑交替，可延拓性只依長度奇偶；
- |S|≥3 時，任意兩側端點色都有延拓，任意正 run 長度皆成立。

故奇數 run 可縮成一點，正偶數 run 可縮成兩點，保持兩側端點的完整 relation。
相應縮減也是路徑 minor：保留所需的一／兩個同 neighborhood 點，刪其他
spokes 再收縮。此公式同樣適用 run 包含 branch root 的情形；左端是 triangle
上的 parent，而非把 root 顏色固定，所以保存的是 **bridge** 介面。

單 run 的非葉長度為奇數，直接縮成原 root 加 leaf 的兩點枝。
兩-run 必為 `X,Y^(2m),leaf`，縮成 `X,Y,Y,leaf`。
對 §4 的 8 個 contexts，這八個四點枝的全部 **240 rows bridge 介面**，
逐一等於原 endpoint 短枝 `X,leaf`；完整接合圖的 relation 及逐邊 minimality
也重新核對。故這兩種縮減都可最後改成原 endpoint 兩點枝。

Bridge 介面等價的拼接理由沿用前報：外側 parent 色 a 可行 iff root 有某個
可取色 c≠a。兩側只共用 boundary 和此一條 bridge，故可以拼回完整 coloring。
多枝時可依序做此操作。所得 endpoint 圖是 §2 的某個 disk base，18 個 bases
都只缺 q，證得 §1。這裡不靠僅保存 q 強迫色來推其他 patterns。

## 6. 證書、重播與信任範圍

產物：[checker](../scripts/c5_triangle_path_reduction.py)、
[證書](../artifacts/c5_triangle_path_reduction/observations.json)。

| 有限模板 | 數量 | disk |
| --- | ---: | ---: |
| palette 切換 minor | 120 | 0 |
| 三-run minor | 20 | 0 |
| 兩-run minor | 20 | 8 |
| `X,X,Y,leaf` | 8 | 0 |
| `X,Y,Y,leaf` | 8 | 8 |

合計 160 個拒絕模板都保存 subdivision；接受端保存 apex rotation。
八個正常形核對完整 relation、q-criticality、bridge masks；root DP 另與
pinned-root 回溯比較全部 240 rows。沿用的 18-base 完備性仍依賴前輪
canonical template 枚舉與 NetworkX 排除，沒有替前輪所有拒絕端補 subdivisions。

任意長度的覆蓋由 §2–5 紙面 minor／transfer 推論提供；計算沒有窮舉無界路徑。
Checker 對所有 |S|≥2 色集與兩側端點色另核對 1..6 長度的 transfer，作為
公式控制；這個有限核對本身不是無界歸納證明。沒有新增 Lean theorem。

```bash
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
uv run --with networkx==3.5 python scripts/c5_root_interfaces.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_branches.py --check
lake build
git diff --check
```

## 7. 下一個窄問題

剩下的是**triangle 外掛樹內部的分叉**。樹核心報告的 Y-minor 排除不能直接
套用：朝 triangle 的那一側已含 cycle，不是 forcing tree，未必能壓成原來
的一／兩點 forcer。應保留 triangle 側，取距離 triangle 最近的分叉，將其
向外的純樹分支壓成 canonical forcers，測試所得有限 triangle–path–fork 模板。
這些壓縮只先用作 minor；若有 disk 存活者，再研究完整 bridge 介面。

不要再增加無分叉 tails 長度；也不要把本輪結果稱為任意 Gallai tree 的分類。
其他 odd cycles、多 blocks、degree≥5、共同 pivotal edge、候選 A 與 K∞=K≤5
仍是獨立缺口。root-interface 與本輪的 scripts、證書、報告及入口文件一併發布。

驗證通過：新 checker 逐 byte 重播、root-interface 與 triangle checkers、
`lake build`（8,820 jobs，僅既有 lint）、154 個文件連結、11 個來源／輸入
hashes 與 `git diff --check`。沒有背景研究程序或未完成的實驗。
