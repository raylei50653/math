---
docgraph:
  id: c5.degree5-interfaces
  family:
    - c5
    - c5.degree5
---
# 唯一 degree-5 內點：完整接點介面與不可刪減禁色覆蓋

後續（2026-09-28）：[相鄰雙 degree-5 介面](c5_adjacent_degree5_interfaces.md)
已將原分量接合與 degree-4 刪邊解除推廣到有序 root 色對，另證 root-edge
對角強迫與 root-spoke 條帶條件。保留共鄰點及共同色框；未證雙 root 分離。

後續（2026-09-28）：[首橋與固定框弧](c5_no_spoke_first_bridge.md) 已關閉最後
12 個指定查詢；來源排除仍 500 筆，保留 116 筆全部接受雙列、0 查詢未決。
唯一 degree-5 全部分支已接回條件式出口；必要型可實現性、完整 Σ 與 Lean
形式化仍未完成。下列數字及停止點保留各原輪語境。

後續（2026-09-28）：[no-spoke 環狀支援](c5_no_spoke_supports.md) 已完成
t=0 的 (2,1,1,1) 指定雙列分離並接回出口；唯一 degree-5 的失敗側只剩
(2,2,1)。其原 616 筆必要支援再由 [原外部路徑 K5](c5_no_spoke_path_minor.md)
排除 500 筆；剩 116 筆中 108 筆雙列已證、12 個查詢未決，未證可實現性或 Lean 化。

後續（2026-09-28）：全部 t≥1 已接回 [單側出口](c5_single_sided_exit.md)。
[no-spoke 外部連通與四型排除](c5_no_spoke_exterior.md) 再把 t=0 六型
收窄為 (2,2,1)、(2,1,1,1)，各分量 K4-free；保留 72 份具名必要覆蓋，
未證來源可實現性或指定 p 分離。下文十三型及各後續數字保留當輪語境。

後續（2026-09-27）：[root 守恆全表掃描](c5_single_spoke_root_sweep.md) 將通用
單接點條件套用到 114 筆，新增 14 個接受查詢；目前 80 筆兩列已證、34 查詢未決。

後續（2026-09-27）：[單接點未用色守恆](c5_single_spoke_root_conservation.md)
已證 (012,04,234)、禁 3 者二接點的 p₂ 延拓；目前 66 筆兩列已證、
48 查詢未決。下文數字與停止點保留各原輪次語境。

後續（2026-09-27）：[single-spoke 外部雙路徑 completion](c5_single_spoke_completion.md)
保留同圖二接點分量，沿用 degree-4 分類及既有有限完整關係證書；
(2,1,1) 的 114 筆配置中現有 62 筆兩個指定 p 已證，52 筆各剩一列。


後續（2026-09-27）：[single-spoke 必要化約](c5_single_spoke_cores.md) 完成 t=1
四型不可刪減覆蓋、接點區塊與反射；(2,1,1) 只剩 19 種必要實際支援型，
已完成部分指定 p 延拓，全部 t=1 仍未解。t=2 已由 [非相鄰分離](c5_two_spoke_nonadjacent.md)
及既有結果完成出口接合；下文舊停止點保留歷史語境。


後續（2026-09-24）：[三接點排除](c5_two_spoke_three_contacts.md) 已以同圖
palette 差與實際 boundary tethers 的 K5 minor 排除全部兩-spoke (3) 型；
尚餘 18 個 (2,1) 配置。下文 24／23 個配置及下一題保留當輪語境。

後續（2026-09-24）：[未接內點引理](c5_unattached_boundary.md) 已證 (3) 非相鄰
S={b0,b3} 型只缺 q；雙缺失目標尚餘 23 個兩-spoke 配置待分離。

後續（2026-09-24）：[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md)
將 t=2 的 (3)／(2,1) 收窄為 24 個必要配置；尚未完成這些核心的分離。

後續（2026-09-24）：[單側出口接合](c5_single_sided_exit.md) 已完成五目標到
唯一 degree-5／三-spoke minimal core 的分離及條件式出口；一般核心分離仍未證。
下文當輪停止點保留歷史語境。

文件整理（2026-09-23），R10：染色與 minimality 介面已完成；[R11](c5_degree5_sectors.md) 起處理三-spoke 分拆 (2)，一般 degree-5 幾何排除仍開放。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

2026-09-18。接續 [K4／全 degree-4 報告](c5_k4_blocks.md) 的 R10。
本輪完成任意大小 degree-4 分量的**染色介面與 edge-minimality 充要條件**，
未完成這些介面的 C5 disk／T4 幾何排除。成果是紙面證明及 Python 固定域證書，
沒有新增 Lean theorem，也沒有擴大 graph catalog。

核心結果：各分量的所有接點須共同保留；固定 z 色後才可獨立接合。
每個 degree-4 分量的任一 incident edge 被刪除，該分量的禁色便全部消失。
因此 minimal obstruction 等價於 z 可用色的一個不可刪減覆蓋，且至少一個
分量有多接點。對固定來源圖，全部非 boundary 刪邊後代的 Σ 可由至多四個
二元開關精確重建；這不是跨圖 weak-congruence 或小型 disk 代表定理。

## 1. 設定與完整介面

G 是簡單圖，保留有序 boundary B=C5，沒有 boundary chord。H 是有效內點
誘導圖且連通。唯一完整 degree=5 內點為 z，其餘內點完整 degree=4。
令 C₁,…,Cᵣ 為 H−z 的連通分量，Pᵢ=N(z)∩Cᵢ 為**有序**接點集；每個 Pᵢ 非空。
固定 q=01012、U={0,1,2,3}、D=3。minimal q-obstruction 的每個內點之
boundary spokes 在 q 下顏色互異；其理由沿用 [list-critical 基礎](c5_weak_list_cores.md)。
完整介面以下對任意 proper boundary row b 定義，不限 q，也不假設 b 下 spokes 異色。

```
L_b(v) = U \ {b(w) : w∈N(v)∩B}
R_C(b) = {(f(p))_(p∈P) : f 是 C 的 proper L_b-coloring}
F_C(b) = {a∈U : 不存在 t∈R_C(b) 使每個 t_p≠a}
A_z(b) = U \ {b(w) : w∈N(z)∩B}
Z_G(b) = A_z(b) \ ⋃_C F_C(b).
```

**精確接合式：** b∈Σ(G) iff Z_G(b)≠∅；更精確地，Z_G(b) 就是全部可延拓的
z 色。證明直接將同一 b、同一 a 下的各分量 colorings 拼接。分量間没有邊，
但同分量的不同接點不能各自選取來自不同 coloring 的顏色。

R_C 保留所有接點共同關係，支援任意接點約束；F_C 是只對「共同 z 色必須
與所有接點異色」這種接合的精確投影，不是 R_C 的可逆表示。不同分量不能
各自重新命名四色。十個 canonical b 需以**同一** S4 置換搬運整列及 z 色。

R_C 可用 unary list factors 與 binary inequality factors 作 natural join，
再只存在量化非接點變數。共享 cut vertex 在兩側接合前不能量化；沿 block-cut
tree 消去末端 block 的私有非接點，再向根推進，即給任意有限 Gallai 分量
的精確遞迴。checker 實作一般 factor elimination，另以完整 coloring tuples
交叉核對；沒有把端點一維投影相乘當作原關係。

## 2. Gallai 結構、tight lists 與 block palettes

minimality 與既有 degree-choosability 化約給出每個 C 是 Gallai tree。
此處不能沿用全 degree-4 **整圖**的 K4／long-cycle disk 排除：C 的外側
現在包含同一個 z 的多接點。

給定 b、a，定義 `M_(b,a)(v)=L_b(v)\{a}`（v∈P），否則為 L_b(v)。
每個 C 點完整 degree=4，因此

```
|M_(b,a)(v)| ≥ 4 − |N(v)\C| = deg_C(v).
```

若 C 拒絕 a，所有不等式必為等號：連通 degree-list 圖只要一點有嚴格多出的
顏色，就能以該點為根，按生成樹由葉向根貪婪著色。每個非根點尚有未著色
parent，根最後使用多出的一色即可。這也涵蓋 C 是 singleton 的情形。
所以在拒絕列中，各點外部鄰居的顏色全互異；尤其
`F_C(b) ⊆ ⋂_(p∈P) L_b(p)`，且任一 C 點若有 b 同色的兩條 spokes，F_C(b)=∅。

可用 block palettes 給出禁色的**充要證書**：M tight，且每個 block K 配有
palette S_K，clique 的 |S_K|=|K|−1、odd-cycle 的 |S_K|=2，任一頂點所屬
blocks 的 palettes 兩兩互斥，且它們的聯集恰為該點 M。
singleton C 則以 M=∅、空 block 表處理。
這是標準 blockwise-uniform degree-list characterization；外部定理的精確
敘述見 [Dvořák, Theorem 10／Lemma 7](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
它不屬於本輪 Python 或 Lean 的一般定理證書。

在 tight 前提下，亦可逐 leaf block 核對：私有點必有共同 palette S，S 必
包含於 cut vertex 的 list；消去 leaf block 時從該 cut list 扣掉 S，歸納到
最後 block。這說明需保留共享點對各 block 的共同色框，而非只存 palette 大小。

## 3. 刪除分量任一邊，禁色全部解除

記 E_C 為所有至少一端在 C 的邊，包括 C 內部邊、boundary spokes 及 zP 邊。
固定**任意** proper b 及任意 z 色 a，暫不要求 a∈A_z(b)。

**分量解除引理。** 對任意 e∈E_C，刪 e 後 C 的染色約束對 a 一定可延拓。
若原來能延拓，沿用 coloring；否則 §2 給出所有外部顏色互異及 tight lists。

- e 是 spoke 或 zP 邊：刪邊在其 C 端點新增一個原本確被排除的顏色；C
  仍連通，使用嚴格多色貪婪引理。
- e 是非 bridge 內部邊：lists 不變，C−e 連通，兩端 degree 減一，故有 slack。
- e 是 bridge：C−e 的兩個連通分量各有一個 endpoint 的 degree 減一，
  對兩側各使用同一引理。

所以刪 e 後的整個 C 區域，其禁色對**所有 b**皆為空；不是只在 q 解除。
繼續刪除該區域的邊也不會恢復限制。此引理只用 degree=4、連通性及貪婪法，
不需 planarity、Gallai 定理或 minimality。

令 J 為任意已刪非 boundary 邊集，S 為仍保留的 z-boundary spokes，I 為
完全未被碰到的分量，即 `C∈I iff J∩E_C=∅`。則一般後代的精確公式為

```
Z_(G−J)(b) = (U \ {b(w) : zw∈S}) \ ⋃_(C∈I) F_C(b).       (1)
```

刪除後 C 分裂或出現孤立點也不影響公式：解除引理已涵蓋整個區域，之後
只刪邊保留可著色性。E_C 彼此互斥，其他非 boundary 邊恰是 z 的 spokes。

## 4. Minimality 的充要條件與接點限制

以下假設 q 下各內點的 spokes 顏色互異，令 A=A_z(q)、Fᵢ=F_Cᵢ(q)。
**G 是 minimal q-obstruction iff**

```
⋃ᵢ Fᵢ = A，且每個 Privateᵢ = Fᵢ \ ⋃_(j≠i) Fⱼ 非空。       (2)
```

必要性：q 不延拓給 A⊆⋃Fᵢ。刪去 Cᵢ 的任一邊只解除 Fᵢ，故 minimality
要求 Privateᵢ∩A 非空。刪 z 的任一 spoke，只會給 z 新增該 spoke 的 q 色 c；
它必不被任何分量阻擋。因此 ⋃Fᵢ 不含 U\A，得到等號。
充分性：覆蓋 A 保證拒絕 q；刪 E_Cᵢ 的邊時可取 Privateᵢ；刪 z-spoke 時
可取剛釋放、位於 U\A 的色。故每條非 boundary 邊都 critical。

設 t=|N_B(z)|、m=Σ|Pᵢ|=5−t。q 只有三色，所以 t≤3，且 |A|=4−t=m−1。
不同分量的 private sets 互斥，因而 `r≤m−1`。若每個分量僅一接點，便有
r=m，矛盾；**至少一個分量必須有兩個或以上接點。** 單接點時 R_C 的 root
可取色集非空，F_C 非空恰在 root 是 singleton，且 F_C 就是該 singleton；
這只適用於真的單接點分量。

| z 的 boundary spokes t | 接點總數 m | 尚未由此必要條件排除的分量接點數分拆 |
| --- | --- | --- |
| 3 | 2 | (2) |
| 2 | 3 | (3)、(2,1) |
| 1 | 4 | (4)、(3,1)、(2,2)、(2,1,1) |
| 0 | 5 | (5)、(4,1)、(3,2)、(3,1,1)、(2,2,1)、(2,1,1,1) |

這十三型是必要的接點數分拆，不是 disk realizability 或完整圖分類。
此外 `r+t≤(m−1)+(5−m)=4`，故 (1) 對固定來源圖最多只需四個二元開關，
最多 16 個不同開關配置／Σ 候選，配置間可碰撞。這是任意多次刪邊的固定
來源圖公式，不宣稱只有 16 個跨圖 states，亦不構造具有小內點數的 disk 代表。

## 5. T4／相鄰雙缺失的精確條件與既有控制

任一 boundary b 的拒絕條件都是 `A_z(b)⊆⋃F_C(b)`。
因此同時拒絕 q 與相鄰三色 p 且接受全部 T4，等價於 q、p 的兩列皆被覆蓋，
但每個四色 row t 都有 `A_z(t)\⋃F_C(t)≠∅`；minimal q 的額外條件是 (2)。
各列必須來自同一張圖的實際 boundary 接點，不能獨立指定不同 b 的禁色。
這把待證幾何命題定位為**跨 boundary rows 的共同可實現性**。

沿用 [樹核心報告的 cyclic probe](c5_tree_cores.md) 已封存的 48 個 disk lifts，
只挑其中 32 個 degree 序列為 (5,4,4,4,4) 的 witnesses，不重新生成圖：

- 16 個接受全部 T4，只缺 q，接點數為 (2,1)。
- 16 個有兩個缺失，接點數為 (2,2)；它們的第二個缺失是 **T4 pattern**，
  並非要求的相鄰三色 p，故不滿足目標假設。
- 全部 32 個都有將端點拆成一維 marginals 就誤允許某個 z 色的具體反例。
  例如第一個 witness：z=5；C={7,8,9} 是 triangle，P=(8,9)，q lists 分別為
  {2,3}、{0,2,3}、{0,2,3}。兩接點各自皆可取 0、2、3，但兩者不能同時避開
  0：否則 triangle 只剩 {2,3}。故 F_C(q)={0}，一維投影會漏掉這個禁色。
  另一分量 {6} 強迫 D，z 的 list={0,3}，兩分量正好不可刪減地覆蓋它。

證書為每個 canonical row 保存完整有序端點 tuples、每列 tuple 的內點 coloring、
各禁色的 block palettes，以及全部 q 刪邊 coloring。另以全部 240 proper rows
直接重建、核對完整 Σ 和固定 z 的可延拓色集；四色共同色框沒有被商掉。
拓撲只驗證既有 apex rotation 的來源邊與 Euler 面數，沒有新 planarity search。

## 6. 重播、信任範圍與停止點

[checker](../scripts/c5_degree5_interfaces.py)、
[certificate](../artifacts/c5_degree5_interfaces/observations.json)。
輸入 artifact 與被引用的原始程式均保存 SHA256，`--check` 重算並逐 byte 比對。
局部控制含 singleton、edge、path、C3／C5／C7、K4、triangle 加 bridge、共享
triangle，以及非 Gallai 的 C4 對照；它們只測代數，不聲稱是 disk lifts。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
git diff --check
```

實際驗證數字見 [STATUS 歷史 §10](STATUS_HISTORY.md#10-唯一-degree-5-接點介面接續未提交-r9)。
任意大小的介面、解除引理及 minimality 等價式是紙面論證；有限控制並不
窮盡十三個接點分拆的 graphs，更不能推出一般 degree-5 單缺失定理。

**下一個窄問題：** 先取 t=3、只有一個二接點 Gallai 分量的分拆 (2)。此時
A(q)={D}，(2) 精確要求 F_C(q)={D}；研究同一分量的兩接點及實際 boundary
spokes 的環序，能否同時拒絕另一相鄰三色 p、接受全部 T4。優先推導保留
兩接點的 block／path 化約或構造明確反例，不增加 k catalog。既有控制只有
(2,1)、(2,2)，不能冒充 (2) 的覆蓋。

R10 的完整染色介面已完成，disk／T4 排除仍開放。一般 degree≥5、單側／共同
出口、候選 A、weak-deletion congruence 與 `K∞=K≤5` 仍未證。成果與前輪 R9 一併提交發布。
