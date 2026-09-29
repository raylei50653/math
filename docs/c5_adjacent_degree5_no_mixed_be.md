# 無 mixed B–E：五份正跨度與完整關係搬運

後續（2026-09-29）：[E–E 六份正跨度](c5_adjacent_degree5_no_mixed_ee.md)
已排除兩側 t=0,(2,1,1) 的全部 disk 來源；144 份原接合全無必要支援，
0 target 查詢。累計八類／1,676 份原接合覆蓋，七類／1,872 份保留；
下文及既有 artifacts 保留當輪語境，目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

2026-09-29，Git 基準 `47ebbbc`。B–E 指 **t_z=1,(2,1)，t_w=0,(2,1,1)**。
原 180 份有序接合中，60 份有相容支援、120 份纖維空；兩個獨立算法給
180 份幾何，接合後得 **144 份必要支援、288／288 個指定 target 接受**。
五份正跨度恰好用滿五條框邊，所有 actual supports 都是一條相鄰框邊，
所以完整關係可逐份精確搬運。沒有 target 失敗候選、沒有額外 source
minor 排除，不需 T4。本型及整圖 root 交換型接回[出口第九類](c5_single_sided_exit.md)。

證據是任意大小的紙面必要化約、沿用外部 degree-list 定理及 Python
固定域完整接合證書；不是 disk 實現，也未新增 Lean theorem。
一般單側／共同出口、任意來源完整 Σ 與 `K∞=K≤5` 仍未證。
目前排程見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 同一來源與五份完整關係

沿用 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、
[Root 預算](c5_root_degree_excess.md)及 [B–B 的接合介面](c5_adjacent_degree5_no_mixed_bb.md)。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
固定 U={0,1,2,3}、q=01012；M 拒絕 q，刪任一非框邊後接受。
相鄰 z、w 的完整 degree=5，其餘內點完整 degree=4，H−{z,w} 無 mixed。
z 有原 spoke z–b_i、二接點 C_z 與單接點 D_z；w 無 spoke，
有二接點 C_w 及單接點 D_w、E_w。後三個單接點分量皆可為任意大小，
不視作 root-spokes。保留七具名接點 Cz_0、Cz_1、Dz_0、Cw_0、Cw_1、
Dw_0、Ew_0、原 zw、全部 bridges／旁支／實際附件及共同色框。

兩側 source (D,O,κ)=(1,0,0)，分量缺額分別 (1,0)、(1,0,0)。存在共同 c：

\[
E_z(q)=E_w(q)=\{c\},\quad
(F_{C_z},F_{D_z})(q)=(\{a\},\{d\}),\quad
\{a,d\}=U\setminus\{q_i,c\},
\]
\[
(F_{C_w},F_{D_w},F_{E_w})(q)=(\{h\},\{e\},\{f\}),\quad
\{h,e,f\}=U\setminus\{c\}.
\]

各組右側顏色互異。選 i、c 及兩組有序排列獨立重建 5·3·2·6=180 份，
逐筆對回原 retained-join IDs、side IDs、完整 side 記錄及 B–B 的 frontier。
D_w、E_w 的次序沒有合併或排序商掉。

完整非空有序接點關係 T_C(β) 定義 F_C(β)=交集_{τ∈T_C(β)} set(τ)。
接點 slack 與外部 degree-list 定理給 T_C 非空、|F_C|≤接點數。
Binary 的逐邊 minimality 保證兩座標各有 release witness，沿用每禁色
95 份 singleton-ban 完整 schemas；checker 從全部 65,535 份非空 binary
relations 重核此表。每條相鄰支援的 q 色穩定子再篩成 17 份。
三個 unary 的完整關係各為單一 tuple {(d)}、{(e)}、{(f)}。
這些 schema 選擇是包含真實同源關係的必要上界，未宣稱可獨立實現。

## 2. 五份正跨度恰好飽和外框

[既有支援引理](c5_adjacent_degree5_no_mixed_t2_t1.md#2-三份原分量的支援及完整-q-schemas)
只需每份原 C 有從其 root 到 B 且避開 C 的原外部路徑。
本型對 C_z、D_z 用 z–b_i，對 C_w、D_w、E_w 用 w–z–b_i；
不需要虛構 w 的 spoke。連同 B 的外部 hub 排除 C 中原 K4 block。
固定 singleton 禁色後，degree-list obstruction 使 C 是 tight Gallai tree。
空支援與全色對稱不相容；若 q(S_C) 只見 d，穩定子迫使 F_C={d}。
令 root=d，tightness 使每點至多一個外鄰，故 deg_C≥3；與 K4-free
Gallai leaf block 的私有點內度≤2 矛盾。故五份分量都至少見兩個 q 色，
每份 actual support 至少兩框點、正 cyclic span 至少一。

取 zw 的細正則鄰域。兩 root incidences 各成一段；每個 binary 的兩個
contacts 必連續。否則原接點間路徑與 root 邊形成的 Jordan 曲線在不含 B
的一側夾住另一 incidence；該 incidence 的原分量／spoke 可避開當前 C
通往 B，矛盾。原 zw 對 w 側直接經 z–b_i 通往 B；對 z 側則經 w 的
任一其他原分量通往 B，仍避開當前 C。故必要 cyclic word 為

\[
\operatorname{perm}(C_z,D_z,z0)\,
\operatorname{perm}(C_w,D_w,E_w).
\]

Annulus crosscut 次序使五份 supports 與 spoke 按此 word 排列成區塊，
允許共端點。以 C_z 首端切開，所有 lifts 在 [0,5]，相鄰區塊滿足
max T_j≤min T_{j+1}。五個整數正跨度的總和≤5，遂全部等於一，
且無未用間隙。因此每份 actual support 恰為一條框邊的兩端，五份分量
的支援弧覆蓋不同的五條框邊，原 spoke 位於兩相鄰區塊的共端點。
這是由完整 actual support 推得的飽和結論，沒有先把稀疏支援填滿。

Checker 一路列舉全部有序 lifts，另一路列舉整側 support hulls 及互不交
框邊 masks，兩者同得 **180 份 supports／placements**。每份保存兩個
degree-5 rotations 及兩 binary 的四種具名方向，共 720 次 rotation 核對。
接入原 180 份 source 色與支援穩定子後得 144 份記錄。120 個空纖維表示
無相容 disk 支援，不能算作 target 接受或額外 source minor 排除。

## 3. 指定雙列的精確搬運與接合

固定 p₁=01021、p₂=01212。每份 S_C 是相鄰框點，q 與兩個 p 在 S_C
都異色，故存在 U 的置換 π_C 滿足 π_C(q_j)=p_j（j∈S_C）。
對同一原 C 的全部內點施 π_C，得到雙射

\[
T_C(p)=\pi_C T_C(q),\qquad F_C(p)=\pi_C F_C(q).
\]

未見色的置換選擇由完整關係的支援穩定子消除歧義。各分量在同一字面 p
及同一 root 色框下接合；保留所有有序 tuples，不以 endpoint marginals
代替。沒有跨列獨立實現假設，也沒有把 source 缺額預算套到 target。

令搬運後五禁色為 a',d',h',e',f'，則

\[
E_z(p)=U\setminus\{p_i,a',d'\},\quad
E_w(p)=U\setminus\{h',e',f'\},\quad
Z_M(p)=(E_z(p)\times E_w(p))\setminus\Delta.
\]

144 份支援逐列直接檢查全部 16 個有序 root 色對，**288 個 Z_M(p) 全非空**，
每個查詢保存一個 witness 及所有合法色對。因必要覆蓋含每個實際來源，
這個固定域證書接上 §2 的任意大小化約，給本型指定雙列分離。
不需呼叫 target obstruction、原路徑 minor 或 T4。

首個支援 record 0 的原 join=2136、sides=(91,64)，依 Cz／Dz／z0／Cw／Dw／Ew
次序，supports=01／04／0／12／23／34。Source 五禁色為 (1,2,0,1,2)，c=3。
在 p₁ 下為 (1,1,0,2,1)，residuals=({2,3},{3})，取 (z,w)=(2,3)；
p₂ 下為 (1,2,2,1,2)，residuals=({3},{0,3})，取 (3,0)。
這也顯示 source 的互異禁色不能直接強加到 target。

## 4. 出口、驗證與界線

本型及交換整份來源的 E–B 型皆接受指定 p₁、p₂。[出口定理](c5_single_sided_exit.md)
仍須來源 Σ(G)=Ω\{p,q} 及 minimal q-core 刪邊繼承，才由其餘八列與
對齊後 p 的接受得到 Σ(M)=Ω\{q}。不能僅憑兩列分離推出任意來源完整 Σ。
原必要接合新增 B–E 180 個 IDs 與 E–B 180 個 IDs，和此前 1,172 個不交；
累計 **七種 root 交換型／1,532 份**已覆蓋，八種／2,016 份保留。
既有 scripts／artifacts 不改寫。下一窄入口為 E–E 的六份正跨度是否矛盾；
本輪未綁定或計算 E–E 的資料，也未將其列入覆蓋。

[Checker](../scripts/c5_adjacent_degree5_no_mixed_be.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_be/observations.json)、
[逐筆支援及所有 ID 纖維](../artifacts/c5_adjacent_degree5_no_mixed_be/support_table.md)
保存完整 schemas、三個 unary、七接點 rotations、spoke、zw 及輸入 SHA。
核對 10,656 次完整關係搬運、4,896 次完整 contact reversal、288 個字面
反射查詢、144 份整來源 root 交換 context 及 432 個含 q 的 root 交換接合。
六項負控制涵蓋跨度超額、三個 unary 不可當 spoke、marginals 失真及原 zw
不可刪去。沒有新 minor skeleton，也不把必要表稱作來源實現。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`--check` 重算並逐 byte 比對；不帶參數只生成本層。實際驗證及未重跑
範圍見[當輪紀錄](history/2026-09-29-adjacent-no-mixed-be.md)。外部 degree-list
定理沿用既有報告，未重新查核文獻；`lake build` 不代表新紙面拓撲或有限表
已 Lean 化。一般交換／幾何完備性、一般／共同出口及 `K∞=K≤5` 均仍開放。
