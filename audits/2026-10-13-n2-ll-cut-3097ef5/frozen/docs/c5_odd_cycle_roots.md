# 較長 odd-cycle 與 triangles 共用點的 root 介面

文件整理（2026-09-23）：R7 的單長環排除完成；[R8 多長環](c5_multi_odd_cycles.md) 已補任意有限長環數的歸納與終止論證。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

後續：[多長環遞迴與連續縮減](c5_multi_odd_cycles.md) 已完成本文的兩長環
停止點，並用明確歸納及終止論證涵蓋任意多長環；本文原定理及證書範圍不變。

2026-09-17。從乾淨 HEAD `7fdc19e` 接續
[triangle-tree palettes](c5_triangle_tree_palettes.md) 的 R7。

**一般 rooted 長奇環的七種介面不封閉：須增加四種三色集合，共十一種。
但固定 q 的不可著色 mixed cluster 仍強迫互補二色 palettes。據此可將長環
收縮為保留共用點的 triangle，接回既有 triangle-tree 排除。**

因此，C5 disk minimal q-obstruction 若所有有效內點完整 degree=4、內部
連通，blocks 恰有一個長度至少 5 的 odd-cycle，其餘為 triangles 或 bridges，
則不存在。不需 T4；triangle 數、bridge 連接樹與外掛樹皆不限大小。
這是紙面論證配合 Python 控制及既有 topology 證書，**未新增 Lean theorem**。

## 1. Root 定義與一般介面的精確範圍

固定 U={0,1,2,3}、q=01012、D=3。從某環刪除 root r，剩下依序為
v₁,…,vₙ，原環長 n+1 為奇數。在 r 不施加對側限制，list 為 U。
各 vᵢ 的有效 list Sᵢ 是私有點二色 residual list，或下游 triangle tree
給出的二色集合／U。令 A 為整個 r 側可著色時 r 的可取色集合。

精確計算可以用 path transfer：對每個 r 色 c，令 X₀={c}，

```
Xᵢ = {a∈Sᵢ : Xᵢ₋₁ \ {a} 非空}；
c∈A ⇔ Xₙ \ {c} 非空。
```

以下論證甚至允許任意 |Sᵢ|≥2。先用一個基本 cycle-list 引理：

> 環上各 list 至少二色時，不可著色當且僅當環長為奇數、所有 lists
> 都是同一二色集合 P。

所有 lists 都二色但不全同時，選相鄰 u,v 有不同 lists，給 u 一個不在
v list 的色，再沿反向路徑貪婪染到 v；v 最後只受另一鄰點有效限制。
若某 list 至少三色，先替各點選二色子集，並在該點選擇使各子集不全相同，
再用前一論證。共同二色 list 的奇偶判準則直接由交替染色得到。

如果 a,b 是兩個不同的 root 禁色，把 r 的 list 限制為 {a,b}；整環不可
著色，故引理強迫所有 Sᵢ={a,b}。反過來，共同 pair P 在長奇環上恰有
A=U\P。因此：

- 所有 Sᵢ 同為二色 P 時，A=U\P。
- 其餘情形至多禁一色，A 是三色集合或 U。

這排除空集與 singleton，且證明任意長度奇環只可能出現十一種 A。
triangle 的非 root 點只有兩個，非共同 pair 情形永遠是 U，故只有原七種。
對每個奇數長度至少 5，十一種皆可在純 list 層出現：共同 pair 得六種
二色集合；下例及顏色置換得四種三色集合；全 U 得 U。

### 七種封閉性的最小反控制

root 外的 C5 路徑 lists 依序為

```
{0,1}, {0,1}, {0,2}, {0,2}。
```

root=0 時路徑被迫成 `1,0,2,0`，末點與 root 衝突；其餘三色皆可取，
故 A={1,2,3}。在第一段增加偶數個 {0,1} 點，可得到每個更長奇環的同型例。
這是一般 list 配置，**不是 disk minimal obstruction 的反例**。

| 原環長 | 七種輸入的配置數 | A 二色 | A 三色 | A=U |
| --- | ---: | ---: | ---: | ---: |
| 3 | 49 | 6 | 0 | 43 |
| 5 | 2,401 | 6 | 72 | 2,323 |
| 7 | 117,649 | 6 | 720 | 116,923 |

表格只是有界控制；任意長度的範圍由上面的 cycle-list 論證負責。
這個 fixed-q 共用點介面也不同於 [單 bridge root 介面](c5_root_interfaces.md)。

## 2. 不可著色時，新增的三色介面無法存活

選包含長環的 maximal 共用點 cluster；其他內部 blocks 只經 bridges
連到它。用 [bridge pruning §1](c5_shared_pair_bridge.md) 逐條處理外向
bridge，允許被刪側含其他 cycles：非 D 強迫色吸收為一條 spoke，D 強迫色
化成一個有三條 spokes 的 D 葉點。每步保留 boundary 固定的 minor、
degree-4、固定 q 不可延拓及逐邊 minimality。

共享點恰屬兩個 cycle blocks，內部 degree=4、沒有 spoke 或外枝，list=U。
其餘 cycle 點扣除外枝後恰有二色 residual list。理由是原始
|L(v)|=deg_H(v)，bridge 強迫色在 L(v) 中且互異；見既有 triangle-tree §1。
同色重複 spokes 與 boundary chords 由 minimality 排除，無須 T4。

將 cluster 的環視為節點，共用點視為邊，得到樹 T，以唯一長環 t₀ 作根。
其下所有子樹只含 triangles，所以它們給 t₀ 的有效 lists 屬原七種。
整圖不可著色，§1 引理便強迫 t₀ 每點的有效 list 都是同一 pair P₀；
向各 triangle 子樹回推原有規則，得到：

```
每環有二色 palette P_t；私有點 residual list=P_t；
相鄰環 palettes 互補。
```

此條件也充分：triangle 子樹由葉回推，長環最後使用共同 pair，故不能
著色。沿任意切口重新定根，§1 的共同 pair 規則與 triangle 規則共同給出

```
A(t→s)=U\P_t=P_s。
```

因此所有實際出現在此 obstruction 的共用點介面均為二色。三色集合與
對側任何二色集合必相交，不能作為一次不可著色接合的兩側。
這裡沒有把一般 list 配置的十一種誤縮為七種：較強限制來自全 cluster
不可著色。minimality 的作用是先把原圖送進上述 residual-list 模型。

## 3. 正規化與刪邊 minimality 的獨立理由

在 §2 的 bridge pruning 完成後，私有 cycle 點的形狀只有：

- D∈P_t：list=P_t，另有兩條不同 q 色的 spokes。
- D∉P_t：list=P_t∪{D}，有一條 spoke，另接一個 list={D} 的葉點。

理由是非 D 外枝已吸收，原始 lists 必含 D，而 bridge 強迫色不得重複。
共享點仍為 U，沒有外枝。實際 boundary 接點保留，未識別同色 boundary 點。

後面要刪去部分整枝並收縮長環；不能僅從「是 minor」斷言 minimality 保留。
此處使用以下獨立引理：

> H 連通，|L(v)|=deg_H(v)，lists 來自四色扣掉互異色的 boundary spokes。
> 若 H 不可 list-color，則刪任一內部邊或任一 spoke 都可著色。

證明：連通圖若各 list 大小至少 degree，且有一點嚴格大於 degree，以該
點作 spanning tree 的 root，子點先於父點貪婪染色。非 root 點至少有父點
尚未染色，root 則有額外一色，因此可完成。刪 spoke 使一點多一個可用色；
刪內部非 bridge 邊使端點有餘量；刪 bridge 時兩個分量各有一個有餘量的
端點。逐分量套用即可。不同色 spokes 的前提不可省略。

故只須另外核對縮圖的 degree、spokes 互異色及不可著色，就能得到所需的
逐邊 minimality；不需要把原圖刪邊後的染色沿 contraction 強行投影。

## 4. 保留三點的長環 minor

如果 t₀ 沒有共用點鄰環，§2 後只剩一個長奇環及 D 葉點，直接由
[單環排除](c5_pentagon_branches.md) 矛盾。

否則在 t₀ 選三個不同頂點，其中至少一個與 triangle 共用。對每個未選
cycle 點，刪掉它的 spokes、D 葉點，以及掛在它的整個 triangle 子樹。
保留三個選點及其全部外接部分，將相鄰選點間的三段環路收縮為三條邊。
可將每個選點至下一選點之前的整段作為其 branch set；三者互不相交、
內部連通，各含且只含一個保留點，boundary 各自是 singleton branch set。

所得圖的長環已變成 triangle，至少仍與一個 triangle 共用點。逐項核對：

1. **boundary／disk：** 只刪除內點或邊、收縮內部環邊，是 boundary 固定
   的真正 minor。原圖 disk 便使縮圖 disk。
2. **degree：** 每個選點仍有兩條環邊；其全部外接部分不變。中間點的
   spokes／枝已刪除，不會因收縮增加選點 degree。所有內點仍完整 degree=4。
3. **固定 q：** 保留的 triangle 子樹仍給選點 P₀；私有選點亦有 residual
   list P₀。新 triangle 使用共同二色 P₀，所以仍不可著色。
4. **minimality：** 縮圖內部連通、spokes 顏色互異且 |L|=degree，由 §3
   引理推出逐非 boundary 邊 minimality。

縮圖的 blocks 只有 triangles 與 bridges，且有非平凡共用點 cluster，
與 [任意 triangle tree 排除](c5_triangle_tree_palettes.md) 矛盾。這完成
開頭的恰一個長 odd-cycle 定理，包括只經 bridges 接到 triangles 的情況。

本輪不需要把含 D 的二色禁集硬換成 spokes。若重播既有 triangle-tree
的閉鄰域縮減，其中每次兩-spoke 替換仍使用不含 D 的禁集與對側全 pair
可取的前提。**本輪的刪枝／收縮沒有宣稱保持完整 Σ。**

## 5. 證書、驗證與下一個窄問題

產物：[checker](../scripts/c5_odd_cycle_roots.py)、
[certificate](../artifacts/c5_odd_cycle_roots/observations.json)。

- C3／C5 的全部 rooted 輸入以 path transfer 與獨立完整色指派交叉核對；
  C7 用 transfer 核對分類、保存枚舉 hash 與每個輸出介面的首個 witness。
- 另以獨立圖回溯核對全部 7⁵=16,807 個 unrooted C5 輸入，恰六個不可著色。
- 30 個具名結構控制：長度 5／7／9、六種 palettes、單鄰環、分散雙鄰環、
  五點皆共享、深層分叉與保留三個鄰環；不是 boundary lifts 全枚舉。
  每例核對完整來源／縮圖 degree 及逐邊 criticality、所有有向 cut root 色集、
  真正 contraction branch sets、刪除點及 boundary 固定的目標邊來源。
- 每個縮圖與既有 triangle-tree 正規形作 boundary 固定的完整圖同構，再
  重播其閉鄰域 pruning，落到既有二／三／四環模板及 K3,3 subdivision。
  沒有呼叫新 planarity search；控制的 boundary 接點採每色第一個代表，
  任意 attachments 的覆蓋由紙面 minor 與既有一般排除承擔。
- 保存來源及兩份直接依賴證書 hashes；`--check` 重算並逐 byte 比對。

```bash
uv run --with networkx==3.5 python scripts/c5_odd_cycle_roots.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_tree_palettes.py --check
uv run --with networkx==3.5 python scripts/c5_pentagon_branches.py --check
lake build
git diff --check
```

上述三份 checker 與 `lake build`（8,821 jobs，僅既有 lint）均通過。
另核對 623 個本地檔案連結、69 份報告索引、新檔 whitespace 與
`git diff --check`；本輪未改 Lean 原始碼，未重跑公理審計或更早六份
triangle 依賴的全量枚舉。

下一個窄問題：**兩個長 odd-cycle blocks 的 mixed cluster root 介面**。
先核對含三色訊息的遞迴，以及全圖不可著色能否仍迫使互補 palettes；再檢查
保留兩個長環接合位置的連續縮減是否保存 §3 的條件。不直接重跑更大
triangle catalog。本輪定理只聲稱恰一個長環，其餘 cycle blocks 為 triangles；
一般多長環／K4 混合 blocks、degree≥5、單側與共同出口、候選 A 及
K∞=K≤5 均未在此證明。本輪成果與後續多長環研究一併納入發布提交。
