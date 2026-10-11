# 多個長 odd-cycle 的遞迴與連續縮減

文件整理（2026-09-23）：R8 的 odd-cycles／bridges 類別完成；[R9 K4 與合成](c5_k4_blocks.md) 已補含 K4 的缺口及全 degree-4 單缺失結論。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

後續（2026-09-18）：[K4／degree-4 報告](c5_k4_blocks.md) 已完成本文 R9
停止點，並合成接受 T4 的全 degree-4 disk minimal obstruction 只缺 q。
本文 odd-cycle 定理、證書與當時停止點保留。

2026-09-17。接續 [長環 root 報告](c5_odd_cycle_roots.md) 的 R8；接手
HEAD `7fdc19e`，前輪長環研究仍在工作樹，未 commit／push。

**兩個長 odd-cycle 的情形已排除；同一歸納與終止論證涵蓋任意有限個長環。**
確切前提是：固定三色 boundary pattern q，G 是 C5 disk minimal
q-obstruction，所有有效內點完整 degree=4、內部圖 H 連通，H 的 blocks
只有 odd cycles 與 bridges。則 H **沒有長度至少 5 的 cycle block**。
再用既有 triangle-tree 結論，所有 cycle blocks 都是頂點互斥的 triangles，
且總數至多二。不需 T4；沒有 triangle 數、環長、外枝大小或 bridge 路徑長度上限。

成果層級是紙面歸納／minor 論證，加 Python 控制及既有 topology 證書。
**未新增 Lean theorem，未宣稱完整 Σ 保持，未處理含 K4 的 block tree。**

## 1. 十一種介面在任意深度封閉

先使用 [bridge pruning](c5_shared_pair_bridge.md) 隔離含長環的 maximal
共用點 cluster。被移除的 bridge 側可以含其他長環；替換引理只用兩側
singleton forcing，不要求移除側為樹或只有 triangles。所得仍為 boundary
固定的 minor，且保留 degree-4、固定 q 不可延拓、逐非 boundary 邊 minimality。

以環為節點、共用點為邊得到有限樹 T。因完整 degree=4，共用點恰屬兩環，
沒有 spoke 或外枝，list=U={0,1,2,3}；私有環點扣除外枝後有二色 residual
list。這裡完全沿用 [前報告 §2–3](c5_odd_cycle_roots.md) 的正規化：
私有點二色 residual list 含 D=3 時有兩條異色 spokes，不含 D 時有一條
spoke 及一個三-spoke 的 D 葉點。此時尚未假定不同私有點 lists 相同。

對 T 的有向邊 t→s，以共用點 r 為 root，令 A(t→s) 是整個 t 側可延拓的
root 色集合，不施加 s 側限制。刪去 r 後沿 t 的路徑讀 lists：每個位置
若私有，取原二色 list；若接子環 u，取整個子樹的 A(u→t)。不同子樹只在
相應共用點碰到 t；boundary 已固定 q，故這是精確的存在量詞消去。

前報告的 cycle-list 引理允許所有輸入 lists 大小至少二，並非只允許七種。
因此可對子樹大小歸納：

1. 葉環每個非 root 點有二色 list。
2. 假設子環訊息各至少二色，t 的每個非 root 有效 list 也至少二色。
3. 若 A(t→s) 禁兩個不同色 a,b，把 r 的 list 改為 {a,b}，所得奇環不可
   著色。cycle-list 引理迫使每個非 root list 都是同一 pair {a,b}。
4. 反過來，非 root lists 同為 pair P 時，A(t→s)=U\P。
   其餘情形至多禁一色，故 A 是三色集合或 U。

所以任意深度仍只有六種二色集合、四種三色集合與 U，共十一種；不出現
empty 或 singleton。triangle 即使吃進三色訊息，輸出也仍是原七種之一。
這是任意有限樹、任意奇環長度的歸納，不由 C5 控制的個數外推。

三色訊息確實能接到另一個長環，不能先行丟掉。例如兩個共用 root 的 C5，
各自其餘四點依序為 `01,01,02,02`，兩側 root 集合都是 `123`；整圖可著色。
checker 另保存三個 C5 的鏈，最下游傳回 `123`，中間長環實際消去此訊息後
再向上傳遞，並以整個具體子圖回溯核對每個方向。

## 2. 不可著色的充要條件仍是互補 palettes

任選 T 的一個環 t₀ 作根。每個有效 list 都至少二色。
整個 cluster 不可著色，當且僅當根環的所有有效 lists 都是同一 pair P₀。
對每個子環 t，A(t→t₀)=P₀ 是二色；§1 的等號條件便迫使 t 的所有
非 root 有效 lists 同為 U\P₀。逐層回推得到：

> 每個環 t 有二色 palette P_t；其私有點 residual list 都等於 P_t；
> 相鄰環 s,t 的 palettes 互補：P_s=U\P_t。

充分性由相同規則從葉向根歸納，根奇環最後使用共同 pair，所以不可著色。
必要性不要求每個環都有私有點；有效 lists 全由子訊息提供時同樣成立。
樹的葉環必有私有點，故選定根 palette 的六種選擇給出六個不同的拒絕配置。

重新定根於任意切口可得 `A(t→s)=U\P_t=P_s`。另一個核對方式是：
接合在 root 可著色 iff 兩側可取色集合有交集；兩個至少二色的四色子集
不相交 iff 它們是互補 pairs。任何三色訊息都與對側相交，無法存在於
不可著色 cluster 的切口。因此新增三色狀態在一般遞迴中保留，但在這個
obstruction 判準中被不可著色性排除。

## 3. 一步縮減的保持條件

在任一長環 t 選三個不同環點，稱為保留點。對未選點刪除它的 spokes、
D 葉點，若它與鄰環共用，則刪去該鄰環方向的整個子樹（不刪 t 上該點）。
保留點的全部外接部分保留。將三個保留點之間的三段路徑縮成三條邊。

沿定向環路，從每個保留點到下一個保留點之前的點構成一個 branch set；
其餘保留頂點各為 singleton。這些 sets 不交、連通；boundary 五點始終
是 singleton，沒有同色 boundary 識別。

- 每個保留環點仍有兩條環邊，外接部分全部保留，所以完整 degree 仍為 4。
  中間點的外接邊先刪掉，收縮不會帶入額外 spokes 或鄰環邊。
- 環樹只刪去完整分枝；保留點若原本共用，仍保留其鄰環。故剩餘私有點
  lists 與共用點身份不變，palettes 直接限制到剩餘樹，仍滿足 §2。
- 新環是 triangle，使用同一 palette。剩餘整個 cluster 仍不可著色。
- 正規化的異色 spokes 條件及內部連通性保留，故每點仍有
  `|L(v)|=deg_H(v)`。套 [degree-list 貪婪引理](c5_odd_cycle_roots.md)
  可獨立推出逐非 boundary 邊 minimality。

最後一項不是從「minor」推出 minimality。刪 spoke 會增加一色；刪內部
非 bridge 會在連通圖產生有餘量的端點；刪 bridge 則兩側各產生一個。
以有餘量點為 spanning-tree root，子先父後貪婪著色，即得到各刪邊延拓。
以上四項每一步都重新成立，所以可接續收縮。

## 4. 兩個長環與任意多長環的終止論證

**恰兩個長環、同一 cluster：** 在 T 中保留它們之間的唯一路徑。
縮減任一長環時，選三點須包括此路徑所用的共用點（端點只需一點）。
第二長環及其接合位置因此完整保留。先縮第一環，再縮第二環，或反序，
每步均滿足 §3。最後只有 triangles，且仍有至少兩個環共用點，與既有
[任意 triangle-tree 排除](c5_triangle_tree_palettes.md) 矛盾。
這不聲稱不同次序給出同一 minor 或相同完整 relation。

**恰兩個長環、不同 clusters：** 先對含任一長環的 cluster 作 §1 的
bridge pruning；另一長環所在側可整體替換。隔離後若 cluster 只有一環，
直接套單環排除；若非平凡，縮該長環後套 triangle-tree 排除。
無須保持 bridge 對側長環的身份，也無須重搜 bridge 路徑。

**任意有限多個長環：** 選含長環的 cluster。單環 cluster 直接由
[單環排除](c5_pentagon_branches.md) 處理。非平凡 cluster 固定一條 T 邊作
保留標記。每次縮減長環 t：若 t 是標記邊端點，保留該共享點；否則保留
從 t 朝標記邊的唯一路徑上的第一個共享點。再補足三點。
於是標記邊及兩端環永不刪去，所有步驟均有 §3 的保持條件。

每步至少把一個長環改為 triangle，可能另刪若干含長環的完整分枝；長環
數嚴格下降。有限次後只剩 triangles，仍有標記的共用點鄰環，矛盾。
這補齊任意長環數的覆蓋與終止，並非由兩環控制直接外推。

因此 odd-cycles／bridges 類別中完全沒有長環；剩餘 triangles／bridges
再由既有定理得到 triangles 頂點互斥且至多二。

## 5. 證書與重播

產物：[checker](../scripts/c5_multi_odd_cycles.py)、
[certificate](../artifacts/c5_multi_odd_cycles/observations.json)。

| 核對 | 範圍 |
| --- | --- |
| 十一種輸入的 rooted transfer | C3 的 121 個、C5 的 14,641 個配置，全部與完整色指派交叉核對 |
| 接合 | 121 對介面，恰六個有向互補 pairs 無交集 |
| 三色遞迴 | 兩個具體可著色控制，完整子圖回溯核對各有向 root 色集 |
| 連續縮減 | 60 個具名控制、138 次縮減；環長 5／7／9、六種 palettes、兩種收縮次序 |
| 結構 | 兩長環直接相接、隔 triangle、雙側接枝、三長環鏈、五點全共享且刪除含長環分枝 |
| 每個來源／中間圖／目標 | degree-4、異色 spokes、內部連通、q 不可延拓、逐邊 criticality、每個有向 root 色集 |
| 真正 minor | 每步與合成 branch sets、刪除點、每條目標邊的來源；boundary 固定 |
| 接回 topology | 最終 triangle tree 與既有正規形 boundary 固定同構，再重播閉鄰域 pruning 及既有 subdivision；小目標 branch sets 另合成回原始多長環圖 |

rooted C3 輸出：6 個 pair、115 個 U；rooted C5：6 個 pair、72 個 triple、
14,563 個 U。控制不是 boundary lifts 全枚舉；spokes 選每色第一個實際
boundary 代表。任意 attachments 的覆蓋由 §3 的 boundary 固定紙面 minor
及既有 triangle-tree／單環一般排除承擔。沒有呼叫新 planarity search。

證書保存程式來源及三份直接依賴證書 hashes；`--check` 重算後逐 byte 比對。

```bash
uv run --with networkx==3.5 python scripts/c5_multi_odd_cycles.py --check
uv run --with networkx==3.5 python scripts/c5_odd_cycle_roots.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_tree_palettes.py --check
uv run --with networkx==3.5 python scripts/c5_pentagon_branches.py --check
lake build
git diff --check
```

四份 checker 與 `lake build`（8,821 jobs，僅既有 lint）均通過。
另核對 636 個本地檔案連結、70 份報告索引、新檔 whitespace 及
`git diff --check`。未改 Lean 原始碼，未重跑公理審計或更早六份 triangle
依賴的全量枚舉。前輪長環 script／artifact 保持原樣。

## 6. 停止點

R8 的兩長環問題完成，並以明確有限樹歸納與終止證明涵蓋任意多長環。
下一個窄問題改為 **全 degree-4 情形中的 K4 block 與 bridge 介面**：先確認
其四個頂點的三色 residual lists 與 bridge forcing，再檢查是否有 boundary
固定的必要 minor 或 disk 排除。共享 K4／cycle 點已會有內部 degree≥5，
所以在目前 degree=4 範圍內，K4 與其他 blocks 的連接應先從 bridges 入手。

含 K4 的一般 block tree、degree≥5、一般單側／共同出口、候選 A 及
`K∞=K≤5` 均未在本輪證明。紙面 minor／topology 未 Lean 化；沒有宣稱
完整 Σ、T4 或其他 boundary patterns 的可延拓性在縮減時保持。
本輪與前輪長環研究的程式、證書及文件一併納入發布提交。
