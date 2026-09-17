# 任意 triangle tree 的 palette 規則與共用點排除

後續：[長 odd-cycle 的 root 介面](c5_odd_cycle_roots.md) 已處理本文的下一題：
一般七種介面不封閉，但不可著色時仍有互補 palettes；恰一個長環與任意
triangles／bridges 的情形已排除。本文證書保留為依賴，現況見 [交接](HANDOFF.md)。
再後續的 [多長環報告](c5_multi_odd_cycles.md) 已排除任意 odd-cycles／bridges
類別中的所有長環，並接回本文的 triangles 互斥且至多二結論。

2026-09-17。接手 HEAD `76e6f44`、工作樹乾淨；接續
[bridge pruning](c5_shared_pair_bridge.md) 的任意共用點 cluster 問題。

**固定三色 boundary pattern q=01012。若 G 是 C5 disk minimal q-obstruction，
所有有效內點完整 degree=4、內部圖 H 連通，而且 H 的 blocks 只有 triangles
與 bridges，則 triangles 必頂點互斥，且總數至多二。** 不需 T4，
外掛樹、bridge 連接樹與 triangle 數均不預設上界。

新內容是任意有限 triangle tree 的紙面歸納、二色禁集的局部 minor，
以及把大 cluster 縮到既有二／三／四環排除的規則。
Python 證書核對局部代數、具名控制與既有 subdivisions；無界覆蓋由紙面
證明承擔。**本輪未新增 Lean theorem，也未證一般候選 A 或 K∞=K≤5。**

## 1. 從完整圖到 residual triangle tree

記四色集合 U={0,1,2,3}、D=3。minimality 是 q 不可延拓，而刪任一
非 boundary 邊後皆可延拓。沿用既有 block 報告的簡單圖與 C5 disk 設定。
存在 triangle cluster 時，minimality 本身排除 boundary chord：異色端點
的 chord 在固定 q 下可刪；同色端點的 chord 則使任何另一條非 boundary
邊刪除後仍不可延拓。因此這裡不必借用 T4 來排除 chords。

先選定一個 maximal 共用點 cluster：其中 triangles 透過共享 cut vertex
連接，不跨 bridge。若 cluster 外還有其他內部圖，逐條離開 cluster 的
bridge 套用 [bridge pruning §1](c5_shared_pair_bridge.md)。外側分量可含
任意 cycles；每次替換保留 boundary 固定的 minor、degree-4、固定 q 及
逐邊 minimality。有限次後只剩該 cluster 與外掛樹／新增 D 葉點。
這確認交接 R1 的推論，且不限原圖的總 triangle 數。

把 cluster 的 triangles 視為節點，共享點視為邊，得到有限樹 T。
共享點恰屬兩環，已有四個內部鄰居，故沒有 spoke 或外枝，list=U。
一個 triangle 至多有三個共享點，所以 T 的最大 degree 為 3。

其餘 triangle 頂點稱為私有點。扣除各外掛 bridge 分量的強迫色後，
每個私有點恰剩二色 residual list。理由與既有四環報告相同：

- 同色重複 boundary spokes 違反逐邊 minimality，所以原始
  |L(v)|=deg_H(v)。
- 每個 incident bridge 的外側 root 唯一強迫一色；這些色必在 L(v)
  且互異，否則刪該 bridge 不會釋放母點色。
- 扣掉所有外枝後，留下所屬 triangle 的兩條邊，residual list 大小為 2。

對任何給定的 cluster 染色，外枝可獨立延拓。因此 residual 模型與原圖
在固定 q 下等價；這不是其他 boundary patterns 的介面等價。

## 2. 七種 root 介面及 palette 歸納

沿 T 的有向邊 t→s 看 t 側的整個子樹，以共享點 r 為 root。
在 r 上不施加 s 側限制。令 A(t→s) 為 r 的可取色集合。

根 triangle 的另外兩個點，各自的有效 list 只有兩種來源：私有點的二色
list，或下游子樹給出的 root 可取色集合。以下局部規則使歸納封閉：

```
E(A,B) = U \ P   當 A=B=P 且 |P|=2；
E(A,B) = U       其餘情形，A,B 各是二色集合或 U。
```

E 是可延拓 triangle 的 root 色集合。如果其中一個 list 是 U，先替另
一點選異於 root 的色，再替 U 點選第三色。兩個二色 lists 不同時，
各去掉 root 色後，不可能同時成為同一 singleton；相同為 P 時則恰禁止 P。
所以任意大小子樹的 A 都在「六個二色集合加 U」這七種介面中。
其禁集 U\A 只可能是空集或二色集合。

對整棵樹任選一環作根。它的三個有效 lists 均為二色或 U。
triangle 不可著色，恰在三個 lists 是同一二色 P；若有 U 則可先染另外
兩點，若三個二色 lists 不全相同則可選三個相異代表。
不可著色因此迫使每個下游訊息非空，並沿每條邊繼續套 E 的非空條件。
得到以下**任意有限 T 的充要條件**：

> 存在每環一個二色 palette P_t，使每個私有點的 residual list 等於所屬
> 環的 P_t，且每條 T 邊 ts 都滿足 P_s=U\P_t。

必要性由上述從根向外的回推；充分性由葉到根的 E 歸納，根環三點最後
均只可用 P_root。T 是樹，故選定一環的 palette 後，其他環全部由距離
奇偶決定。T 有私有點（非單點樹有葉），因此恰六種不同的不可著色
residual-list 配置。此判準本身不需 minimality 或平面性；minimality
只在 §1 把原圖送進二色 residual 模型時使用。

尤其對每條有向邊，

```
A(t→s)=U\P_t=P_s。
```

這同時涵蓋既有鏈 transfer、三叉分合與兩環共用點規則。
它不涉及 bridge root 的三色原始 list；[rooted pair](c5_shared_pair_bridge.md)
中 12 個 singleton（含三個 D singleton）仍是不同介面，不被本規則排除。

## 3. 不含 D 的二色禁集可吸收成兩條 spokes

設共享點 r 分隔成 F、K 兩側，兩側共用 boundary 與 r，其他內點互斥。
F-r 的內部圖連通，r 在兩側各有兩條 triangle 邊，沒有 boundary spoke。
假設固定 q 下

```
avail(F,r)=U\P，avail(K,r)=P，|P|=2，D∉P。
```

§2 保證對 palette 為 P 的整個子樹 F 滿足此前提，包括其所有外掛樹。

**每個 c∈P 都有 F-r 到 c 色 boundary 的接點。** 否則在 F 的全部
內點（含 r）交換 c、D，所有 boundary 約束保持不變。由 D∈avail(F,r)
得到 c∈avail(F,r)，矛盾。這是 root 可取色集合的 swap 論證，
不把二色禁集當成 bridge singleton。

把 F 的所有內點收縮到 r，每個 c∈P 保留一條 c 色 spoke，刪掉其他
新增邊、loops 與重複邊；保留 K。兩個 c 不同，所選 boundary 點必不同。
收縮只沿內部邊，沒有識別或刪除 boundary 頂點，因此得到 boundary 固定
的 minor G'。逐項核對：

1. **固定 q 介面：** 新兩條 spokes 恰允許 r∈U\P，與 F 相同。
   更精確地，保留頂點上的染色可延拓到 F，當且僅當滿足這兩條 spokes。
   所以 G' 仍不延拓 q。
2. **degree：** r 的兩條 F 內邊換成兩條新 spokes。r 原先沒有 spokes，
   不會與保留邊重複；r 與其他保留內點的完整 degree 仍為 4。
3. **舊邊 minimality：** 對 K 的任一舊非 boundary 邊 e，限制 G−e
   的延拓。F 未改，故 r∈U\P，得到 G'−e 的延拓。
4. **新邊 minimality：** 若刪 c 色新 spoke，取 K 的 r=c 染色；
   這由 avail(K,r)=P 保證。另一條 spoke 的色不同，故此染色延拓 G'−e。
5. **disk：** boundary 固定的內部 minor 保持 disk 性。內部連通也保持。

因此可以刪去任意大小的此類子樹，同時保存後續小核心排除所需的全部
假設。對一般保留側，前兩條 spokes 仍保存固定 q 介面；但第 4 點的
minimality 需要已明列的 avail(K,r)=P，不能從「是 minor」單獨推出。

此引理只處理 D∉P。若 D∈P，boundary 沒有 D 色，不能作此替換。
也沒有聲稱完整 Σ 或所有 boundary patterns 的 rooted interface 保持。

## 4. 保留閉鄰域，縮到二至四環

設 cluster 有至少兩個 triangles。§2 的互補 palettes 使 T 的兩個部類中，
恰一類 palettes 不含 D。選其中任一環 t，**保留 t 與它的所有鄰環**。

保留子樹 S=T[N[t]] 是星形，節點數為 1+deg_T(t)∈{2,3,4}。
t 的 palette 不含 D，所有鄰環的 palette 都含 D。每條離開 S 的邊，
外側第一環距 t 為 2，palette 因而不含 D。該外側整個子樹對切點的
禁集正是此 palette，故可套 §3 吸收。不同外側分量互斥，操作根點亦不同；
可依次進行，每步都保存固定 q 介面及其餘前提。

新私有點 r 的兩條 spokes 使 residual list 為 U\P，恰等於保留鄰環的
palette。其他私有點與外掛樹不變。最後得到只含 S 的 disk minimal
q-obstruction，所有有效內點仍 degree=4，允許任意外掛樹。

| deg_T(t) | 保留環數／形狀 | 已有排除 |
| --- | --- | --- |
| 1 | 二環共用點 | [兩環 §3](c5_two_triangle_blocks.md) |
| 2 | 三環共用點鏈 | [三環 §2–3](c5_shared_triangle_blocks.md) |
| 3 | 四環共用點 star | [四環分叉 §2–3](c5_four_triangle_star.md) |

三種均矛盾，所以不存在大小至少二的 cluster。此步用的是選定中心的
完整閉鄰域；任意抽出二／三／四環未必有可吸收的外側禁集。

回到 §1，任何原圖的非平凡 cluster 都能先隔離，故原圖 triangles 必
頂點互斥。再套 [互斥多環 §5](c5_three_triangle_blocks.md)，得到總數至多二。
恰二環時接回既有直接 bridge 的六內點分類，存活者只缺 q。
零／一環仍接回樹與單 triangle 報告；本輪不移除其單缺失結論的 T4 假設。

## 5. 證書、驗證及停止點

[checker](../scripts/c5_triangle_tree_palettes.py)、
[certificate](../artifacts/c5_triangle_tree_palettes/observations.json)。

- 全部 49 個 E 輸入、343 個根 triangle 輸入由直接色指派核對；另核對
  48 個兩-spoke／任意保留側色集合控制。
- 具名 pair、三環鏈、四環鏈、四環 star、七環 path、十環 branched 控制，
  各取六種 palettes 與每種可用中心 degree；這是化約測試，不是新 disk catalog。
- 每例由獨立圖回溯求所有有向切口的 root 色集合，核對來源／結果 degree
  及逐邊 q-criticality；保存真正的收縮 branch sets，逐一驗證互斥、內部連通、
  boundary 固定、目標邊的來源，以及兩條新 spokes 的 boundary 色。
- 每個目標與既有二／三／四環模板作 boundary 固定的完整圖同構，並重播
  該模板既存的 K3,3 subdivision；沒有呼叫新的 planarity search。
- 保存來源與六份依賴證書 hashes。`--check` 重建並要求 JSON 逐 byte 一致。

```bash
uv run --with networkx==3.5 python scripts/c5_triangle_tree_palettes.py --check
uv run --with networkx==3.5 python scripts/c5_shared_pair_bridge.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_shared_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_three_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_four_triangle_chain.py --check
uv run --with networkx==3.5 python scripts/c5_four_triangle_star.py --check
lake build
lake env lean Math/ForcingListsAudit.lean
git diff --check
```

一般 palette 歸納、swap 接點、minor 構造與 disk 閉性仍是紙面層。
Lean build 與既有 20 條 forcing-list 定理的審計不會把這些新論證自動形式化。
有限控制亦不能取代任意 T 的證明。

**下一個窄問題：一個長度至少 5 的 odd-cycle block，與 triangles 共用
cut vertices 時的 root 介面。** 先檢查哪些介面可出現、minimality 如何限制
它們，再判斷本輪閉鄰域化約能否使用；不能先假定七種 triangle 介面仍封閉。
較長 odd-cycle／K4 的一般混合 blocks、degree≥5、一般單側出口、共同
pivotal edge、候選 A 與 K∞=K≤5 仍未處理。

本輪上述七份 checkers、`lake build`（8,821 jobs，僅既有 lint）、既有
forcing-list 公理審計、文件連結與 `git diff --check` 均通過。新 checker
包含 48 個結構控制、63 次子樹吸收。本輪產物隨本次 commit 保存，未 push，
沒有背景研究程序。
