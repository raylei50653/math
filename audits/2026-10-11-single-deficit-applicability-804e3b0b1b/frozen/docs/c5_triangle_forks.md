# Triangle 外掛樹：第一個分叉的 minor 排除

文件整理（2026-09-23）：任意外掛樹的單 triangle 分支已完成；唯一長環由 [單環報告](c5_pentagon_branches.md) 排除，多 block 由 [合成報告](c5_k4_blocks.md) 補完。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

後續狀態（2026-09-17 文件整理）：本文的下一題 cycle-5 已由
[單環排除](c5_pentagon_branches.md) 處理；後續多 block 進度見 [交接](HANDOFF.md)。

2026-09-17。接續 [路徑枝化約](c5_triangle_path_reduction.md)。
本輪排除任意深度的第一個分叉，因此把前輪單缺失結論推廣到
**內部唯一 cycle 是 triangle、外掛樹任意大小**的全 degree-4 核心。
這是紙面 minor 化約加 Python 有限 subdivision 證書，未新增 Lean theorem。

## 1. 條件式結論

設 G 是接受全部 T4 的 C5 disk minimal q-obstruction，全部有效內點的
完整 degree=4，內部圖 H 連通且唯一 cycle 是 triangle。則外掛樹不分叉，
並且 `Σ(G)=Ω\{q}`。外掛樹的大小與深度沒有預設上界。

分叉排除本身不需要 T4；單缺失 corollary 沿用前輪路徑枝化約與既有
18 個 canonical disk bases。這不涵蓋更長 odd cycles、多個 cycle blocks、
degree≥5，也不是候選 A 或 `K∞=K≤5` 的一般證明。

## 2. 先保留 cycle 側，壓縮朝外樹枝

固定 q=01012、未使用色 D=3。沿用 [triangle 接枝限制](c5_triangle_branches.md)
§1：共同 triangle palette 是 P={D,a}；至多兩條外接 tree edges，
位於不同 triangle 頂點，強迫色 c 不在 P。

假設有分叉，選某枝距 triangle 最近的分叉 v。從 triangle 到 v 的路徑
中間點都沒有其他 tree branches。每條 bridge 切開後兩側端點都唯一強迫
同一色；cycle 側也適用，因為逐邊 minimality 保證刪邊後有 coloring。
在 v，各 incident edge palettes 互異並覆蓋 L(v)：刪 v 後各分量相互獨立，
若重複或有色不在 L(v)，刪相應邊仍不能釋放顏色，違反 minimality。
而 `|L(v)|=deg_H(v)`、`D∈L(v)`。

若 deg_H(v)=3，記朝 triangle 的 palette 為 p，兩個朝外 palettes 為 r,s。
三者互異，且 `{p,r,s}` 含 D；v 有一條剩餘 q 色的 spoke。
若 deg_H(v)=4，選一個朝外且非 D 的 palette t，把其 forcing subtree
收縮到 v，只保留一條 t 色 spoke。該樹必碰到 t 色 boundary，否則在樹內
交換 t、D 便破壞唯一強迫性。這樣得到同樣的 degree-3 fork，仍保留 D。
所選朝外非 D 色一定存在，因為三個朝外 palettes 互異。

對保留的兩個朝外 forcing subtrees，使用 [樹核心報告 §3](c5_tree_cores.md)：
D-forcer 縮成 list={D} 的一點；非 D 的 b-forcer 縮成
list={D,b} 的 root 加 list={D} 的 leaf。這只保持 minor，沒有宣稱
其他 boundary patterns 的 root 介面相等。

Triangle 的其他外掛 branch 若存在，整枝收縮到它的 triangle 頂點，
只留其強迫色的一條 spoke。於是 triangle 上目標接枝點的 list={D,a,c}，
另兩點的 list={D,a}，其中 c≠a 且 c≠D。

## 3. 刪 stem spokes，直接收縮到一條邊

刪掉 triangle 到 v 之間所有中間點的 boundary spokes，再收縮該路徑，
保留 triangle 頂點與 v 為兩個不同端點。若本來相鄰，無須操作。
這一步不需要知道路徑長度、奇偶、palette 或實際 attachments。

**收縮後這條邊不要求兩端 palette c=p。** 它可能不再是 q-obstruction，
也可能破壞 degree-4 或 T4；我們只用它作為非 disk minor。
枚舉刻意容許 p 為全部四色，避免把原路徑的染色限制錯加到縮圖上。
所有收縮只合併內點，不識別 boundary；故若原圖 disk，minor 也必 disk。

最後只剩以下有限模板（內點從 0 編號，實際圖加 5）：

- Triangle 邊 01、02、12，lists 為 {D,a,c}、{D,a}、{D,a}。
- Fork 點 3 接 triangle 點 0，list={p,r,s}。
- r、s 互異且不同於 p，三色集合含 D；各接一個上述 canonical forcer。
- 每個 list 禁止的 q 色，完整枚舉該色的一個實際 boundary 鄰居。

a,c 為不同的已使用色；r,s 按遞增排列即可，因兩條外枝可以交換標號。
這涵蓋任意第一個分叉的上述 minors，無需事先知道原枝可壓到哪個 disk base。

## 4. 完整有限排除與單缺失 corollary

共 **90,112 個 lifts，全部非 disk**。每個 lift 的 boundary-apex 圖均包含
保存的 K5 或 K3,3 subdivision。相同 subdivision 可供多個 lifts 共用；
每個 lift 都有明確的 witness index，checker 逐一驗證實際邊包含關係。

若存在原 disk 分叉圖，§2–3 必給出這 90,112 個之一的 disk minor，矛盾。
因此沒有分叉。所有外掛樹均為路徑，直接套用前輪任意長路徑枝結果，
得到只缺 q。零枝情形沿用既有 triangle 小核心分類。

最初保留 stem root 的較大探測有 226,560 個拒絕例；縮去全部 stem
中間點後得到本輪較小的完整模板集合。較大探測只用於選方向，不是本結論
依賴的證書，不需重跑或保存為第二份枚舉。

## 5. 證書與重播

產物：[checker](../scripts/c5_triangle_forks.py)、
[證書](../artifacts/c5_triangle_forks/observations.json)。

生成時使用 NetworkX 尋找 subdivision；`--check` 不再呼叫 planarity search，
而是重建全部 lifts，檢查 subdivision 的模型、真實邊、路徑內點互斥、
branch vertices 與完整覆蓋。另核對枚舉 digest、來源 hashes 與證書逐 byte 一致。
有限模板的完整性由程式笛卡兒積加 §2–3 的紙面化約提供；拓撲 soundness
依賴標準 minor 閉性和 Kuratowski 障礙，未在 Lean 形式化。

```bash
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
git diff --check
```

驗證通過：新 checker 全量逐 byte 重播、既有 path-reduction checker、
`lake build`（8,820 jobs，僅既有 lint）、三份入口／報告的 153 個本地連結、
七個來源 hashes 與 `git diff --check`。無背景研究程序。

## 6. 停止點與下一個方向

單 triangle、全 degree-4 的任意外掛樹缺口已在上述信任範圍內封口。
下一步建議取**內部唯一 cycle 長度 5**，先研究共同 cycle palette 與接枝
位置的必要 minor 限制。先測有限 obstruction／反例，不直接假設 triangle
的「palette 含 D」或「至多兩枝」會延續。不要再增加 triangle tails 長度，
也不要把本輪升格為所有 Gallai block trees 的分類。
