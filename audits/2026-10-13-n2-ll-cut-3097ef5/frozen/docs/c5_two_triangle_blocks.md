# 兩個 triangle blocks：直接 bridge 的有限正常形

文件整理（2026-09-23）：直接 bridge 六內點存活型保留；恰三環由 [互斥型](c5_three_triangle_blocks.md) 與 [共用點型](c5_shared_triangle_blocks.md) 排除，任意總數由 [triangle tree](c5_triangle_tree_palettes.md) 補完。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

後續狀態（2026-09-17 文件整理）：[互斥三環](c5_three_triangle_blocks.md) 與
[共用點三環](c5_shared_triangle_blocks.md) 已補齊恰三環；最新四環成果見 [交接](HANDOFF.md)。

2026-09-17。接續 [cycle-5 接枝排除](c5_pentagon_branches.md)。
**兩個 triangle 不必被排除：有 disk minimal q-obstructions。**
但全 degree-4 時，共用 cut vertex、較長的連接路徑、以及任何額外外掛樹
均可排除。只剩兩個 triangle 由一條 bridge 相連的六內點圖，所有存活者只缺 q。
這是紙面 minor 化約加 Python 有限證書，未新增 Lean theorem。

## 1. 範圍與結果

固定 boundary `q=01012`，未用色 `D=3`。G 是 C5 disk minimal q-obstruction，
全部有效內點的完整 degree=4。假設內部圖 H 連通，其 blocks 中恰有兩個
triangle，其餘 blocks 全是 bridges。等價地，兩個 triangle 共用一個頂點，
或由一條內部頂點不在兩環上的路徑連接；除此之外只掛樹。
外掛樹的大小、深度、分叉及連接路徑長度均不限。

則兩個 triangle 必須頂點互斥、由**一條直接 bridge**相連，且沒有任何額外
外掛樹。因此 H 恰有六個頂點。固定 q 及模板標號，共有 **64 個 disk lifts**，
全部逐邊 q-critical，完整 relation 均為 `Σ(G)=Ω\{q}`。
不需要額外假設接受全部 T4；這反而是分類的結果。

不涵蓋三個以上 cycle blocks、含較長 odd-cycle／K4 blocks 的組合、degree≥5，
也不證一般候選 A、共同 pivotal edge 或 `K∞=K≤5`。

## 2. 可用的 forcing 壓縮，及不可混用的部分

由 minimality，每條 bridge 切開後的兩側 root 都唯一強迫同一個色。
同一內點的 boundary spokes q 色互異，`D∈L(v)` 且 `|L(v)|=deg_H(v)`。
在一個不屬於 cycle 的內點，各 incident bridge palettes 互異並覆蓋 L(v)：
切去該點後各分量獨立；若重複或色不在 L(v)，刪該邊無法釋放新色。

以下兩個 minor 操作其實只需要**連通且可著色的 forcing component**，不需要是樹：

- 非 D 的 c-forcer 必碰到 c 色 boundary，否則交換 component 內 c、D
  會破壞唯一強迫性。可將它連同 bridge 吸收到母點，只保留一條 c 色 spoke。
- D-forcer 必碰到全部三個 q 色，否則交換 D 與缺失色即可矛盾。
  可把 component 收縮成一點，每色留一條 spoke，得到 list={D} 的單點。

這兩個論證在 component 含另一個 triangle 時仍成立。
但 [樹核心 §3](c5_tree_cores.md) 的**保留 root 的兩點非 D-forcer**化約依賴樹，
不能把含 cycle 的 component 當成樹來用。本輪只在 §5 的真正外掛樹使用它。
所有操作只保 minor，不宣稱保持其他 boundary patterns 的完整介面。

## 3. 共用頂點與 cycle palette

### 共用 cut vertex

共同頂點 v 的內部 degree 已為 4，故沒有 boundary spoke 或外掛枝，`L(v)` 是四色。
各 triangle 的另外兩點扣除外樹強迫色後，各剩一個兩色 list。
若這兩個 lists 不同，任意 v 色都能延拓該 triangle；若相同為 P，恰好禁止
v 使用 P 的兩色。這可直接檢查：給定 v 色 c，兩點各去掉 c 後，只有兩者
都成為同一 singleton 才不能染色。

兩邊的禁止集合必合起來覆蓋四色，因此它們各有兩色且互補。交換兩環標號後，
左 palette 為 `{D,a}`，右 palette 為其補集。左側所有外枝均非 D，可吸收；
右側兩個非共用頂點各保留一點 D-forcer，其他枝吸收。
共用點 list=四色，左兩點 list={D,a}，右兩點 list=右 palette∪{D}。
三種 a 的 **768 個 lifts 全非 disk**，故不能共用 cut vertex。

### 由 bridge path 相連

每個 triangle 扣除所有外接 bridge 的強迫色後，三個剩餘兩色 lists 必為共同 P；
否則可先著色 triangle，再獨立拼回所有外接 components。

若 D 不在 P，每個 triangle 頂點必有一個 D-forcing component。
用 §2 的連通版本壓成三個 D 葉點，吸收其他枝，得到 **1,088 個 no_D minors**，
全非 disk。某個被壓縮的 component 可以含另一個 triangle；這裡沒有使用
兩點樹 forcer lemma。故兩環的 palettes 都含 D。

記兩環 palettes 為 `{D,a}`、`{D,b}`；連接路徑在兩端的 bridge palettes
分別為 c、d，則 `c≠a,D`、`d≠b,D`。其餘外樹枝全部非 D，先吸收成 spokes。

## 4. 連接路徑必須只是一條邊

### 先縮整條路徑，保留兩個 cycle 端點

刪掉連接路徑中間點的 spokes／外樹，再收縮成一條邊。得到兩個 triangles：
端點 lists 分別 `{D,a,c}`、`{D,b,d}`，其餘兩點各為對應的兩色 palette。

枚舉刻意允許 `c≠d`，因為收縮可能破壞 q-obstruction。
**7,744 個 lifts 中有 128 個 disk**；保存其 apex rotation 及全部 240-row relation。
其中 64 個 c=d，只缺 q；另 64 個 c≠d 可延拓 q，但各缺另一個 singleton。
所以不能從「縮圖 disk」或「原圖是 obstruction」偷推縮圖 c=d。

原圖若已是一條直接 bridge，由 bridge forcing 必有 c=d，便落入前 64 個基底。
若有中間點，固定所得的 128 個 disk 基底之一，繼續保留路徑資訊如下。

### 恰一個中間點 u

u 的兩條路徑邊 palettes c、d 必不同。兩者都非 D，而 incident palettes
覆蓋 L(u)，故 u 必另有強迫 D 的外樹。保留成單點 D-forcer，吸收其他枝，
得到 `list(u)={D,c,d}`，u 同時接兩個 cycle 端點與 D 葉點。
只需對 c≠d 的 64 個基底展開，**512 個 minors 全非 disk**。

### 至少兩個中間點

保留最靠左與最靠右的中間點 u、w。u 的第一條 bridge palette 是 c，
另一條路徑邊 palette 記 x。吸收其他非 D 枝後：

- 若 x=D，u 的 list 恰為 `{D,c}`。
- 若 x≠D，u 必有 D-forcing 外樹。將它吸收到 u，便取得全部三個 q 色的
  spokes；只留 c 以外的兩色 spokes，也得到 list={D,c}。

右端同理得到 `list(w)={D,d}`。兩點及其外樹互斥，因此可以同時操作。
刪去 u、w 間其餘中間點的 spokes／外枝，再收縮成 u—w 一條邊，保留 u、w
不同。得到 `triangle—u—w—triangle`，不要求中段收縮保持 edge palettes。
128 個基底的 **768 個這類 minors 全非 disk**。

兩種情形都矛盾，所以兩個 triangles 必由直接 bridge 相連。
這個結論涵蓋原連接路徑沿途有任意外樹分叉的情形。

## 5. 直接 bridge 的外掛樹也全部排除

此時 c=d，吸收外樹後必落入那 64 個 q-critical 基底。
假如原圖仍有一棵外掛樹 F，保留其中一棵，其他外枝全部吸收。
F 的強迫色 f 不在其 triangle 的 `{D,a}`，所以 f≠D。
對 F 使用真正的樹 lemma，壓成 root list={D,f}、leaf list={D} 的兩點 forcer。

再把這個兩點 forcer 吸收到 triangle 頂點，保留 leaf 的一條 f 色 spoke，
便得到某個上述 disk 基底。因此必要擴張可完整地從基底反向列出：
選一條 spoke、刪它、接上該色的兩點 forcer，枚舉新 root／leaf 的所有接線。
允許 leaf 的 f 色鄰居與刪除的 spoke 不同，這只增加覆蓋，不會漏掉必要 minor。

64 個基底各有十條 spokes，共 **5,120 個擴張，全非 disk**。
故原圖沒有任何額外外掛樹。這是 minor 排除，不靠兩點 forcer 保存完整 relation。
原圖現在就是六內點基底本身，可以直接讀其完整 relation，得到只缺 q。

## 6. 存活者與證書

一個具名例子，內點為 5..10：

```
triangles: 56, 57, 67；89, 8-10, 9-10
bridge: 58
boundary neighborhoods:
5:{1}, 6:{0,1}, 7:{0,3}, 8:{1}, 9:{1,2}, 10:{2,3}
```

兩環 palette 都是 `{D,2}`，bridge palette 是 0；此圖只缺 q。
全部 q-critical lifts 的 metadata 為 `(a,c,b,d)=(2,0,2,0)` 或 `(2,1,2,1)`，
各 32 個。64 是有內部模板標號的數目，不是 64 個同構類。

| 模板 | lifts | disk |
| --- | ---: | ---: |
| triangle palette 不含 D | 1,088 | 0 |
| 共用 cut vertex | 768 | 0 |
| 整條連接路徑縮成一邊，c、d 獨立 | 7,744 | 128 |
| 一個中間點加 D-forcer | 512 | 0 |
| 保留兩端中間點 | 768 | 0 |
| 直接 bridge 基底增加一棵外樹 | 5,120 | 0 |
| **合計** | **16,000** | **128** |

產物：[checker](../scripts/c5_two_triangle_blocks.py)、
[證書](../artifacts/c5_two_triangle_blocks/observations.json)。
15,872 個拒絕 lifts 各有 witness index，共用 **649 份 subdivisions**
（626 個 K3,3、23 個 K5）。接受端保存 rotation，檢查真實鄰接、dart faces
與 Euler characteristic；完整 240 rows 由回溯核對，另與十個代表的內點枚舉比較。
64 個 q-obstructions 全部逐非 boundary 邊核對 minimality。
具 q-obstruction lists 的拒絕模板，每種 list assignment 留一個 q-criticality
代表；其他同色鄰居選擇
有相同 q lists。共用頂點的兩色-list 禁色規則另有 36 個完整控制。

`--check` 重建全部模板，驗證保存的拓撲證書、枚舉 digests、八個來源 hashes
及 JSON 逐 byte 一致，不呼叫 planarity search。無界覆蓋依賴 §2–5 紙面
化約、minor 閉性與 Kuratowski 障礙；本輪沒有 Lean 形式化。

```bash
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_pentagon_branches.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
lake build
git diff --check
```

## 7. 停止點與下一個窄問題

恰兩個 triangle blocks、其餘皆 bridges 的全 degree-4 核心，已在上述信任
範圍內分類到六內點正常形。不要再增加兩環間 path 長度或外掛樹深度。

下一步可固定**三個 triangle blocks**，先研究 cut-vertex／bridge 連接型態。
兩環分類不能直接排除第三環：連向第三環的 component 含 cycle，§5 的兩點
非 D-forcer 樹壓縮不適用。應保留第三個 triangle 作必要 minor，或先建立
其 rooted forcing 介面，避免把它當普通外掛樹。
較長 odd-cycle／K4 blocks 的組合、degree≥5、候選 A 與 K∞=K≤5 仍獨立未解。

驗證通過：新 checker、cycle-5 checker、triangle-fork checker、`lake build`
（8,820 jobs，僅既有 lint）、161 個本地文件連結、兩輪合計九個來源 hashes
與 `git diff --check`。沒有背景研究程序；本輪及前輪 cycle-5 均未提交或推送。
