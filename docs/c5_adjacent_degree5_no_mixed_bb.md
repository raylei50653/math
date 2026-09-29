# 無 mixed B–B：四分量支援、環序與完整 target 分離

後續（2026-09-29）：[B–E 五分量支援及完整關係搬運](c5_adjacent_degree5_no_mixed_be.md)
已完成下文所列下一入口：144 份必要支援、288 個 target 全接受。
本頁及原 artifacts 保留 B–B 當輪資料；目前排程見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

2026-09-29，Git 基準 `f2496f5`。完成兩側 **t=1,(2,1)**：原 236 份
IDs／sides 接成 **888 份必要支援，1,776／1,776 個指定 target 全接受**。
原資料 92 份有支援、144 份纖維空；888 份支援全保留，沒有額外 source
minor 排除。完整關係上界先接受 1,656 個 target；只對剩下 120 個失敗
候選套幾何：48 個由原路徑／固定框弧排除，72 個由原雙端點排除。
不需新增 palette 交換論證或 T4；本型接回[出口第九類](c5_single_sided_exit.md)。

證據為任意大小紙面必要化約、沿用外部 degree-list 定理與 Python 固定域
證書。必要支援、完整關係上界的組合、minor skeletons 都不是 disk 實現。
未新增 Lean theorem；未證一般交換／幾何機制完備性、任意來源完整 Σ、
一般單側／共同出口或 `K∞=K≤5`。目前排程見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 原來源與四份完整關係

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
固定 U={0,1,2,3}、q=01012；M 拒絕 q，刪任一非框邊後接受。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4；H−{z,w} 沒有 mixed
分量。兩側各一條原 spoke，B_z={i}、B_w={j}；各有二接點 C_r 與單接點
D_r。保留六個具名接點 Cz_0、Cz_1、Dz_0、Cw_0、Cw_1、Dw_0、兩條
原 spokes、zw、所有原 bridges／旁支／實際附件及共同色框。
D_z、D_w 是任意大小原分量；即使 i=j，兩條原 root-spokes 也不能合併。

沿用[無 mixed 化約](c5_adjacent_degree5_no_mixed.md)與
[Root 預算](c5_root_degree_excess.md)，每側 (D,O,κ)=(1,0,0)，分量缺額
為 (1,0)。存在共同 c，使

\[
E_z(q)=E_w(q)=\{c\},\quad
F_{C_r}(q)=\{a_r\},\quad F_{D_r}(q)=\{d_r\},\quad
\{a_r,d_r\}=U\setminus\{q(B_r),c\},\ a_r\ne d_r. \tag{1}
\]

Checker 以原 retained IDs 過濾，另直接選 i、j、c 與兩側有序 (a_r,d_r)
獨立重建同一 236 份。原 SHA、side 記錄及 236 個纖維逐筆保存。第 0 筆
retained-join ID=2142、sides=(91,91)，兩 spoke 都到 b0，其纖維為空。
空纖維分類是「無相容 disk 支援」，不算 target 接受或新增 minor 排除。

對每份原 C，完整非空有序接點關係 T_C(t) 定義
F_C(t)=交集_{τ∈T_C(t)} set(τ)。接點 slack 給 T 非空及 |F_C(t)|≤接點數。
兩份 binary C 保留各禁色的 95 份 singleton-ban 完整 schema：每個座標
都有 minimality release witness，並由全部 65,535 份非空 binary relations
獨立核對。按 actual support 的 q 色穩定子保留 17 或 95 個 IDs；兩個
D 的完整 unary 關係分別為 {(d_z)}、{(d_w)}。不同 component 的 schema
選擇仍只是含真實來源的必要上界，不宣稱可獨立實現。

## 2. Actual-support span 與 cyclic-order 必要覆蓋

每份分量均有避開它的原 r–s–b_j 外部路徑，使用 zw 與另一 root 的
原 spoke。因此[三分量支援引理](c5_adjacent_degree5_no_mixed_t2_t1.md)
的 K4-block 原圖 K5 排除、degree-list tightness 與 Gallai tree 論證逐份
適用：四分量皆 K4-free，且各自 q(S_C) 至少兩色。
具體地，空支援不能有 singleton F；只見色 d 時，色穩定子迫使 F={d}，
固定 root=d 的 tightness 使每點至多一個外鄰，故內度至少三，與 K4-free
Gallai leaf block 私有點內度至多二矛盾。故四份 actual supports 各有
至少兩個框點、cyclic span 至少一。

取原 zw 的細正則鄰域 N。沿 ∂N 兩 root incidences 各成一段。
同一 C_r 的兩個 contacts 必連續：原接點間路徑與 root 邊的 Jordan
曲線不能在不含外框的一側夾入另一原分量或 spoke，因其有避開 C_r
的原路徑通往 B。故六單位的必要 cyclic word 為

\[
\operatorname{perm}(C_z,D_z,z0)\,
\operatorname{perm}(C_w,D_w,w0). \tag{2}
\]

Annulus crosscut 次序使各 actual support 沿同一 word 成區塊。從 C_z
首個外端切開，以 0≤lift≤5 表示，min T_Cz=0，相鄰單位 max T_i≤min
T_{i+1}，再以 anchor∈{0,…,4} 模五還原支援。允許共端點和支援中的間隙；
不將支援填成整弧。四個正跨度總和≤5，故各跨度≤2，沒有同單位重複
框點提升。spokes 跨度零，兩側不得互換或合併身份。

Ordered lifts 與獨立的「整側 support hull／互不交框邊 masks」兩算法均得
**2,520 份 supports／placements**。每份保留兩個 degree-5 rotations、
六具名接點及兩份 binary 的四個方向組合，共 10,080 次 rotation 核對。
接入 (1)、支援色與 schema 穩定子後得 **888 份**必要記錄；這給任意大小
來源的覆蓋，沒有證明逆向實現。

## 3. 完整 target 接合及第一層結果

固定 p₁=01021、p₂=01212。對每個原分量，若色置換 π 在全部 actual
support 上滿足 π(q_i)=p_i，則 T_C(p)=πT_C(q)，F 同步搬運。
Checker 保存置換與完整 source schema IDs，逐份核對 67,104 個 relation
搬運，另核對整份 relation 的 contact reversal／字面反射；不使用 endpoint
marginals。這些分量搬運最後共同接在同一字面 p 與 root 色框上。

無可用 π 時，保留所有 |F|≤接點數、且被 p(S_C) 穩定子保持的完整禁色
集合，包括空集。來源 q 的缺額預算不施加到 p。候選集合包含真實 F，
但各候選跨分量／跨列是否共同可實現不作假設。精確 root 接合是

\[
E_r(p)=U\setminus(p(B_r)\cup F_{C_r}(p)\cup F_{D_r}(p)),\qquad
Z_M(p)=(E_z(p)\times E_w(p))\setminus\Delta. \tag{3}
\]

每個完整候選均直接枚舉 16 個有序 root 色對核對 (3)。失敗恰為 empty_z、
empty_w 或 same_singleton，所有成立原因一起保存。

| 第一層計數 | 數量 |
| --- | ---: |
| 所有 target 查詢／完整候選接合 | 1,776／3,504 |
| 全部四份關係可搬運而接受 | 1,296 |
| 搬運與容量上界合用而接受 | 360 |
| 未決查詢／失敗候選 | 120／120 |
| empty_z／empty_w／same_singleton | 60／60／0 |
| A/A、A/?、?/A 記錄 | 768、60、60 |

`targets` 保存此第一層，`final_targets` 保存下節精化；不得把第一層的
上界失敗稱為原圖拒絕。只對這 120 個失敗候選呼叫 obstruction checker。

## 4. 原路徑、固定框弧與雙端點

固定 C=C_z 或 C_w，F_C(q)={d}，失敗候選若 F_C(p)=A 為 pair，沿用
[原路徑／首橋](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md)與
[原雙端點](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md)的局部引理。
它們只要求當前原 binary C、source singleton、target pair、實際支援及
避開 C 的外部路徑；外部是三個還是四個原分量不改變前提。
本輪使用四分量 context，沒有使用舊三分量的 hard-coded 整表迴圈。

Target pair 迫使兩接點間為奇數長原 bridge 路徑 P=(x₀,…,xℓ)。刪 P 邊後
各 W_j 保留原旁支與附件。Target 局部 residual 是 A；其 actual support
T_j 必在 target 穩定子容許族內。如果同一份連通三框弧分割 B=X⊔Y⊔D_B
使全族都碰 X、Y，並有原 root 到 D_B 的外部路徑 L，就有 K5 minor。
L 的四類是本側 spoke、經 zw 的另一側 spoke、另一同側原分量、經 zw
再經另一側原分量；分量路徑止於第一次到 B，全部使用原邊。
**48 個候選**由此直接排除。

只對餘下候選使用端點 tightness。令 K 是 q、p 在 S_C 上逐色位置不變的
色集，則同一 W_j 的固定色 palette 歸納給 L_j^q∩K=A∩K。兩個原端點
各只有一條 P 邊，拒絕 (q,root=d) 的 tightness 給
L_j^q={d,β_j}，β_j≠d。兩端的支援均屬

\[
\mathcal E=\bigcup_{\beta\ne d,\ \{d,\beta\}\cap K=A\cap K}
 [\mathcal T(q,S_C,\{d,\beta\})\cap\mathcal T(p,S_C,A)], \tag{4}
\]

其中 𝒯 是保持 residual 的支援穩定子必要族。保留全部 β，不假設兩端
β 相等，也不把端點 residual 套給下一頂點。若固定 X、Y 都碰全族，取

\[
V_0=\bigcup_{j<\ell}W_j,\quad V_1=W_\ell,\quad
Z=V(L)\cup D_B,\quad X,\quad Y. \tag{5}
\]

原中間 bridges 使 V₀ 連通，最後 bridge 給 V₀–V₁，兩 contacts 給二者
到 Z，實際附件給二者到 X、Y，三框切口補足十個鄰接。五組不交，故
得到原圖 K5 minor；空族另記端點不存在，不能當成空泛 minor。
本輪餘下 **72 個候選**皆由非空端點族與固定框弧排除，不需 palette 交換。

兩份可重播的具名例子（以下 support 次序為 Cz／Dz／z0／Cw／Dw／w0）：

- Record 14：原 join=2148、sides=(91,118)，support=01／04／0／123／34／3。
  q 的四份 F 為 ({1},{2},{0},{2})。p₁ 唯一失敗候選為
  ({1},{1},{0,3},{1})，E_z={2,3}、E_w=∅。Cw 的 target 族為 {13,123}；
  X=12、Y=34、D_B=0 及原 w–z–b0 給直接 K5。
  JSON 亦保留經原 Dz 或 Dw 到 b4 的不同固定分割／路徑。
- Record 22：原 join=2145、sides=(91,102)，support=01／04／0／234／12／1。
  q 的四份 F 為 ({1},{2},{2},{0})。p₂ 唯一失敗候選為
  ({1},{2},{0,3},{2})，E_z={3}、E_w=∅。對 Cw，d=2、K={1,3}，
  (4) 只容 β=3，𝒠={23,234}。同一 X=12、Y=34、D_B=0 與原 w–z–b0
  用 (5) 排除候選。這裡 d 不守恆，第一層 target-only 族沒有統一框弧。

## 5. 出口、證據與下一入口

每個 target 的全部完整候選都有 root 色對或上述反證，故 888 份支援
全部接受 p₁、p₂。144 空纖維無 disk 來源；另 888 份不作 source minor
刪除。這證明 §1 的任意大小 B–B 型雙列分離。

[出口定理](c5_single_sided_exit.md) 仍額外使用來源 Σ(G)=Ω\{p,q} 與
minimal q-core 的刪邊繼承：其餘八列已接受，再由本結果接受對齊的 p，
才得到 Σ(M)=Ω\{q}。不得由兩列分離單獨推出任意來源完整 Σ。

原 3,548 份必要接合中，新增 B–B 的 236 個 IDs，與原 936 個不交；
合計 **六種 root 交換型／1,172 份**覆蓋，九種／2,376 份仍開放。
原範圍矩陣與 artifacts 保留快照，本層 `coverage_extension` 記累計 IDs。
下一窄入口選 **B–E：t_z=1,(2,1)，t_w=0,(2,1,1)**，只綁定 180 份 IDs，
首項 join=2136、sides=(91,64)，未做其支援或 target 遍歷。須保留五原分量、
七接點、一條原 spoke 與 zw；目前排程由導覽維護。

[Checker](../scripts/c5_adjacent_degree5_no_mixed_bb.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_bb/observations.json)、
[逐筆表與全部纖維](../artifacts/c5_adjacent_degree5_no_mixed_bb/support_table.md)
保存完整 source schemas、兩個 unary relations、rotations、原 target 候選及
逐候選反證。1,016 份 minor skeletons 保留四分量實際支援與 root degree-5
incidences；包含路徑長 1／3／5／9、16 種 tether 形狀、外部分量鏈長 1／3。
每份核對十鄰接、反射及 root 交換；它們不是 degree-list 來源實現。
另有 21 個負控制，包括 Dz 非 spoke、兩 unary 不合併、marginals 失真、
缺少 zw／原 spoke／中間 bridge／contact／附件、Dz／Dw 原路徑刪邊與重疊
branch sets。3,504 個完整 root joins、888 個整來源 root swaps 皆核對。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見[當輪紀錄](history/2026-09-29-adjacent-no-mixed-bb.md)。
`--check` 重算並逐 byte 比對；無參數只生成本層。外部 degree-list 定理與
固定色 palette 引理沿用上述既有報告，未重新查核文獻；`lake build` 不代表
本輪 disk、minor 或任意大小論證已形式化。
