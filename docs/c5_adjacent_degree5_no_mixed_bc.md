# 無 mixed B–C：飽和分量原路徑排除與雙列分離

後續（2026-09-29）：[B–D 雙飽和來源排除](c5_adjacent_degree5_no_mixed_bd.md)
完成 180 份原接合的 312 份必要支援，全以 source K5 排除，含 root 交換型；
八份需原分量外部路徑，0 target 查詢，不需 T4。累計十類／2,396 份覆蓋，
五類／1,152 份保留；下文保留當輪語境，目前停止點見研究線導覽。


2026-09-29。**B–C 及整圖 root 交換型的指定雙列分離完成。**
180 份原有序接合接上 780 份幾何，得到 608 份必要支援；584 份由
source 原路徑 K5 排除，保留 24 份的 48 個指定 target 全由完整關係搬運／
容量上界接受，沒有 target minor 查詢或未決查詢。不需 T4。

證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域證書；
未新增 Lean theorem，不宣稱必要支援或 minor skeleton 可實現為 disk。
一般出口、任意來源完整 Σ 及 K∞=K≤5 仍未證。
目前停止點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 同一來源及完整關係

沿用 [no-mixed](c5_adjacent_degree5_no_mixed.md)、[root 預算](c5_root_degree_excess.md)
與 [A–C 缺額型](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md) 的前提與引理。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通；
M 拒絕 q=01012，刪任一非框邊後接受。相鄰 z,w 完整 degree=5，其餘
內點完整 degree=4，H−{z,w} 無 mixed。z 有一條原 spoke z–b_i、二接點
Cz 及單接點 Dz；w 無 spoke，有二接點 Cw、Dw。四分量任意大小，保留
七具名 contacts、zw、全部原 bridges／旁支／actual attachments 及共同色框。

寫 U={0,1,2,3}、完整有序接點關係 T_C(t)、F_C(t)=⋂_{τ∈T_C(t)}set(τ)。
接點 slack 與既有 degree-list 引理使 T_C 非空、|F_C|≤接點數。
兩側 source (D,O,κ)=(1,0,0)，故存在 c，使

\[
(F_{Cz},F_{Dz})(q)=(\{a\},\{d\}),\quad \{a,d\}=U\setminus\{q_i,c\},
\]
\[
(F_{Cw},F_{Dw})(q)=(\{h\},U\setminus\{c,h\})\quad\text{或反序}.
\]

i 有五選擇、c 三選擇、z 禁色兩次序、w 六種缺額／飽和排列，共 180 份。
獨立重建後逐 ID 比對 [E–E frontier](../artifacts/c5_adjacent_degree5_no_mixed_ee/observations.json)。
不把 Cw、Dw 排序商掉。逐邊 minimality 的 release witnesses 給 singleton
binary 每色 95 份完整 schema；pair 禁色 {a,b} 的完整關係恰為
{(a,b),(b,a)}。Dz 的 unary 關係為 {(d)}。Checker 重核全部 65,535 個
非空 binary relations，得到 380 份 singleton 及六份 pair schemas，
再以 actual support 的 q 穩定子篩選完整關係。

## 2. 四份正跨度與環序覆蓋

對 Cz、Dz，原 z–b_i 避開當前分量；對 Cw、Dw，原 w–z–b_i 避開它。
沿用 A–C §2 的外部 hub 與 degree-list 論證：各分量 K4-free；非空禁色
迫其拒絕 residual 為 tight Gallai tree。空支援違反全色對稱；只見一色
時，pair 禁色違反穩定子，singleton 禁色則等於該色，tightness 迫每點
內度至少三，違反 K4-free Gallai leaf block 的私有點內度至多二。
故四份 actual supports 都至少見兩個 q 色，各有正跨度。

取原 zw 的細正則鄰域，兩 root incidences 各成一段。每份 binary 的
兩 contacts 必連續，否則其原內部路徑與 root 邊圍住另一 incidence，
而該 incidence 能避開當前分量通往 B，矛盾。原 zw 的另一側亦可經其
他原分量到 B。必要 cyclic word 因而是

\[
\operatorname{perm}(Cz,Dz,z0)\operatorname{perm}(Cw,Dw).
\]

Annulus crosscut 次序給同序 supports，可共端點。切在 Cz 首端後，
各稀疏支援 lift 在 [0,5]，前一 max≤後一 min，四正跨度總和≤5。
因此每份跨度為一或二；不填補 actual support 的缺口。
按 lifts 生成及獨立按兩側 hull／框邊 masks 生成，均得 780 份且各一
placement。12 個 cyclic words 各保留三 binary 的八種方向，七 contacts
及 spoke 在兩 degree-5 rotations 中均完整保留。

接合顏色與完整 schema 穩定子後為 608 份必要支援。180 個原 ID 中
100 個有支援、80 個空纖維；空纖維表示不相容 disk 支援，不計 target
接受，也不計新增 minor 排除。

## 3. 原飽和分量的來源 K5

直接套用 [A–C §3](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)
於 w 側唯一 source pair 分量 C。雙禁色給原兩 contacts 間的奇數 bridge
路徑 P；每個刪除 P 邊後的路徑塊 W_j，其 rooted residual palette 為
該 pair。若 T_j 是全部 actual support，則逐色固定 q(T_j) 的每個置換
必保持該 pair。這給完整必要族，包含不同路徑塊的不同實際附件。

固定同一三連通框弧分割 B=X⊔Y⊔D_B，若所有允許 T_j 都碰 X、Y，
且有避開 C 的原 w–B 路徑 L 落在 D_B，第一條 bridge 的兩塊、X、Y 及

\[
(V(P\cup\{wu,wv\})\setminus\{u,x_1\})\cup V(L)\cup D_B
\]

給五個不交連通 branch sets（u,x₁ 是第一條 bridge 端點）。原 bridge、
朝兩端的路徑邊、四份到 X/Y 的附件及 C5 三個切口給全部十鄰接。
L 可以經原 spoke、同側其他分量或 zw 加另一側原分量；不新增邊。
新增 Dz 只提供另一條合法外部路徑，不改變此任意大小引理。

608 份中 584 份由此排除。例 record 0：原 join 2124、sides=(91,16)，
支援依 Cz/Dz/z0/Cw/Dw 為 01/04/0/12/234，禁色 ({1},{2},{0},{1,2})。
飽和 Dw 的路徑塊必碰 b3、b4；取 X=123、Y=4、D_B=0、L=w–z–b0。
這是 source 排除；未對其查 target。

## 4. 保留支援的指定雙列

令 p₁=01021、p₂=01212。若 actual support 上 q、p 可由同一四色置換
對齊，精確搬運整個 T_C 及 F_C；否則保留所有大小≤接點數、由 p 支援
穩定子保持的禁色集合，包含空集。它是包含真實 F 的上界，不是假定
不同分量可獨立實現。逐組重算

\[
E_z(p)=U\setminus(\{p_i\}\cup F_{Cz}(p)\cup F_{Dz}(p)),\quad
E_w(p)=U\setminus(F_{Cw}(p)\cup F_{Dw}(p)),
\]
\[
Z_M(p)=(E_z(p)\times E_w(p))\setminus\Delta.
\]

24 份保留支援的 48 個查詢，每組候選 Z_M(p) 均非空，不需 target minor。
例 record 8（join 2127、sides=(91,28)）：支援 01/04/0/123/34，
source 禁色 ({1},{2},{0,1},{2})。p₁ 下 Cz、Dz 均禁 1，故 E_z={2,3}；
w 的一 pair 上界加 unary 至多禁三色，E_w 非空，必能選異色 root pair。
p₂ 下禁色 ({1},{2},{1,2},{2})，可取 (z,w)=(3,0)。

整份來源交換 roots、spoke、分量歸屬及 contacts 時 Z 轉置，C–B 亦完成。
連同既有覆蓋，新增正反向 360 個原 IDs：累計九類／2,036 份覆蓋，
六類／1,512 份仍開放。接回 [出口第九類](c5_single_sided_exit.md) 時，
仍另用來源 Σ(G)=Ω∖{p,q} 及刪邊繼承其餘八列，才得到 Σ(M)=Ω∖{q}。
兩個指定 target 本身不推出任意來源完整 Σ。

## 5. 證書、驗證與剩餘界線

[Checker](../scripts/c5_adjacent_degree5_no_mixed_bc.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_bc/observations.json)、
[逐筆支援表](../artifacts/c5_adjacent_degree5_no_mixed_bc/support_table.md)
保存來源 IDs／SHA、完整 schemas、空纖維、rotations、逐候選完整接合及
584 份長度一 K5 skeleton；重播另核對每份長度三、五，共 1,752 次 minor
控制（均再驗反射與 root 交換）。另有 1,704 次完整關係搬運、48 次字面
target 反射、全部支援的 w 分量交換。四個控制檢查 unary 不能變 spoke、
跨度上限、pair 不能換成 marginals、原 zw 必排除對角線。
有限 skeleton 只核對原 incidences、實際 support、branch sets 與十鄰接，
不是任意大小拓撲引理或 degree-list 定理的機器證明。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_bc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際檢查見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-bc.md)。
下一窄入口 B–D：同分拆但 w 側 D=0、O=1，兩份 binary 都飽和；180 份
原 IDs 已綁定，首項 join 2128、sides=(91,30)。尚未生成其支援／target 表。
其餘 C–C、C–D、C–E、D–D、D–E 保留。
