---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared-t0-pair-single
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge-shared
  requires:
    - c5.adjacent-degree5-mixed-edge-shared-t1-pair
    - c5.adjacent-degree5-singleton-long-arc
    - c5.single-spoke-two-two-external
  related:
    - c5.single-sided-exit
---
# 共鄰端點 mixed K2：t_w=0、(2,1) 的原 diamond 路徑與雙列分離

後續（2026-09-29）：[t_w=0、(1,1,1) 六跨度排除](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)
已逐筆排除原 108 筆：四份 unary、v 的總跨度至少 6>5，不需 T4，0 target 查詢。
zu、zv、wu 共鄰端點接線的全部五型已完成，出口第八類移除 w 分拆限制。
原資料保持；下列通知與正文保留各輪語境，現行入口見 [HANDOFF](HANDOFF.md)。

2026-09-29，接手 main@c178cf1 及上一輪尚未提交的 t_w=1、(1,1) 完整變更。
**本型必接受 p₁=01021、p₂=01212，不需 T4，不限制原 unary 分量大小。**
原 54 筆正常形與 240 份同序幾何接合成 102 筆必要支援，**204 個指定
查詢全接受**。另由原 diamond 的 u／v 附件路徑給 94 筆來源 K5 排除，
保留 8 筆的 16 查詢均可精確搬運；雙列分離本身不依賴這份 pair K5 排除。
不需 root-spoke、穿過其他 unary 的外部路徑或新增跨列 first-bridge 引理。

證據為任意大小紙面化約、外部 degree-list 定理與有限 Python 證書。
必要支援及 minor skeletons 不是 disk 來源實現；未新增 Lean theorem，
一般單側／共同出口及 K∞=K≤5 仍未證。優先序見 [HANDOFF](HANDOFF.md)。

## 1. 固定來源與原 54 筆完整關係

G 有限簡單，B=(b0,…,b4) 為 induced disk 外框，有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}；G 拒絕 q，刪任一非框邊後接受 q。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4。H−{z,w} 的唯一
mixed 原分量恰為 uv，root incidences 恰為 **zu、zv、wu**。本型 w
無 boundary spoke，w 側 unary 接點分拆是 (2,1)。

[共鄰端點化約](c5_adjacent_degree5_mixed_edge_shared.md) 給 z 亦無 spoke，
且有唯一二接點原分量 C_z，接點 (x₀,x₁)。w 的兩份不同原分量記為
C_wp、C_ws，具名接點分別是 (y₀,y₁)、t。記 actual supports 為
S_z、S_p、S_s，另有 N_B(u)={b_i}、N_B(v)={b_j,b_k}，j≠k。
保留原分量、全部接點、實際附件、bridges、框點身份及共同色框。

存在 {h,e,d}={0,1,2} 與 c∈U∖{e}，使

\[
q_i=h,\qquad \{q_j,q_k\}=\{h,e\},\qquad
F_z(q)\in\{\{h\},\{h,d\},\{h,3\}\},
\quad F_p(q)=U\setminus\{e,c\},\quad F_s(q)=\{c\}.
\tag{1}
\]

這是 6×3×3=54 筆。F 是原完整 ordered relation 的全部 tuple 色集交集。
C_wp 的完整 q 關係是 F_p 兩色的兩個次序，C_ws 是 {(c)}；C_z 禁兩色
時亦保留兩個次序，禁一色時保留原 95 種 schemas，另按 actual S_z 的
q 色穩定子篩選**整份** relation。未拆成接點 marginals，也未合併 w 的
兩份分量。checker 對 (1) 與原 54 筆逐一核對，綁定 ID、完整原記錄、
局部 K2 支援 ID、全部 schemas 及相容 IDs。

原 JSON SHA256 保持
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`；
原 306／288 筆與 9,312 份完整 schemas 不改寫。

## 2. 無 root-spoke 時的局部支援與 diamond 外側

對 C=C_z、C_wp 或 C_ws，唯一相鄰 root 為 r=z 或 w；另一 root 不在
C 內也不鄰接 C。忽略 r 色時，接點有 slack，完整 relation 非空。
若 a∈F_C(q)，從原接點 lists 刪 a 得不可著色 degree lists M_a。
[Dvořák 的 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness、Gallai tree 及 blockwise-uniform palettes；本輪核對原文第 5–6 頁。

[前輪的局部 K4 與解除論證](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md#2-局部-degree-list-前提與-k4-排除)
只需 C 內每點完整 degree=4、外鄰在 B∪{r}，以及一條避開 C 的 r–B
原路徑。此處仍有 **r–u–b_i**，r=z 用原 zu，r=w 用原 wu，完全不需
root-spoke。因此 K4 block 的四個互不相交外向分枝，可接到連通外部
hub B∪{r,u}，給 K5 minor；C 是 K4-free Gallai tree。刪 bridge 的兩側
各有 slack；刪非 bridge、boundary incidence 或 root incidence 亦給
局部解除。另一個 degree-5 root 的存在未被藏進 degree-4 前提。

每份 **q(S_C) 至少含兩色**。空支援的全色對稱不容許非空、容量≤2 的
F_C。若僅見色 a，固定 a 的穩定子迫使 F_C={a}；固定 r=a 後，tightness
使每點最多一個外鄰，故 deg_C≥3，與 K4-free Gallai tree 的葉塊私有點
內度≤2 矛盾；singleton C 內度零亦矛盾。三份 actual supports 均非空，
cyclic span 至少一，這個結論在使用 annulus 之前已成立。

保留原 diamond D={zw,wu,uv,vz,zu}。u、v 經原附件到 B，z 經 C_z、
w 經 C_ws 到 B，路徑內部避開 D。因此四點都在 D 面向 B 的面界上；
唯一含四點的 face cycle 是 Q_D=z–w–u–v–z，原 chord zu 位於內側。
三份 C 連通且碰 B，故都在 Q_D 外側。取 Q_D 閉內部的細正則鄰域，
外側成 annulus；不增加任意 root-spoke，也不把 C_ws 壓成實際 spoke。

## 3. 二接點區塊與 actual supports 的完整環序

z 外側只有 C_z 的兩條 contacts。對 w，取 C_wp 內連接 y₀、y₁ 的
簡單原路徑 P；J=w–y₀–P–y₁–w 是完全在 B 內的 Jordan 曲線。
D−{w} 連通且避開 J，u／v 的原附件使 D−{w} 與 B 位於 J 同側。
若 w–t 夾在兩條 C_wp contacts 的外側區間內，它進入另一側；C_ws
與 J 不交且必碰 B，矛盾。因此 C_wp 的 contacts 是連續區塊，C_ws
在其前或後。保留兩份 pair 的全部具名接點方向。

五個原單位的次序遂為

\[
C_z,\quad\operatorname{perm}(C_{wp},C_{ws}),\quad u,\quad v
\tag{2}
\]

或整體反向。每個單位的連通細鄰域連接 annulus 的兩邊界；同一框點的
不同附件可在其小鄰域分開，仍保留框點身份與顏色。沿用前輪 crosscut
論證：單位內連接兩外端的 crosscut 所切下、不含內圓周的一側，不能
含另一單位的外端，因後者亦須連回內圓周。故 actual supports 按 (2)
同序，不能在另一支援區塊內穿插。

從 C_z 第一個外端切開，每份支援提升為整數集 T_A，滿足

\[
\min T_{C_z}=a,\qquad \max T_{O_r}\le\min T_{O_{r+1}},\qquad
\max T_{O_4}\le a+5,\qquad T_A\bmod5=S_A.
\tag{3}
\]

不同單位可共享框點端點，actual support 內可有間隙，不填成整弧。
首尾重複同一框點會佔滿一圈，與其他正跨度單位矛盾，故每份跨度<5。
三份 unary 與 v 各跨度至少一，總跨度≤5。遞增 lifts 與獨立 cyclic
hull-edge masks／整個 w 區間兩算法均給 **240 份**幾何及 placements；
每份保存兩個 pair 的四種具名 contact words。

與 (1)、三份支援至少兩色、完整 relation 穩定子接合，得到 **102 筆**
必要資料。原 54 正常形只有 12 筆有相容支援，42 筆纖維為空。這是
任意大小來源的必要覆蓋；有限算法本身不證拓撲覆蓋或 disk 實現性。

## 4. 原 diamond 附件替代 root-spoke 的 K5

對 C_z 或 C_wp，若 F_C(q)={a,d}，沿用已局部化的
[雙禁色 bridge 與外部 K5 引理](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md#4-飽和雙禁色-bridge-與外部-k5-的局部版本)。
§2 已核對其 degree-list、解除與 K4-free 前提，沒有套用全圖唯一 degree-5
的假設。兩拒絕 palettes 的差沿兩接點 block 路徑傳播，odd cycle 的第三
頂點會迫使差為零；故接點之間是奇數長原 bridge 路徑 P=(x₀,…,x_ℓ)。
刪 P 邊後，W_j 為含 x_j 及全部原旁支的連通塊；這些塊互不相交。

局部 residual 與 rooted palette 唯一性使每個 W_j 的 actual support
至少供應下列兩個 q 色：

\[
E(F)=F\quad(3\notin F),\qquad E(F)=U\setminus F\quad(3\in F).
\tag{4}
\]

若兩色在 **S_C 本身**各只有一個供應點 b_a、b_b，則每個 W_j 都有
到這兩個具名點的原附件。多供應點不能任選代表。只在 a、b 相鄰且有
原路徑 L 從 r 到 B∖{b_a,b_b}、內部避開 C∪B 時使用排除。

本輪所有 L 都在 **D 加 ub_i、vb_j、vb_k** 內找到。每筆保存全部簡單
候選路徑與選定 L，沒有 root-spoke，也不需穿過任何其他 unary。
對任一原 bridge x_jx_(j+1)，令 J=P∪{rx₀,rx_ℓ}，五個 branch sets 是

\[
W_j,\quad W_{j+1},\quad
Z=(V(J)\setminus\{x_j,x_{j+1}\})\cup V(L)\cup(B\setminus\{b_a,b_b\}),
\quad\{b_a\},\quad\{b_b\}.
\tag{5}
\]

J 刪相鄰兩點後經 r 連通（ℓ=1 時剩 {r}），L 接到連通補弧，所以 Z
連通。原 bridges 保證兩 W 不含其他路徑點，L 避開 C，固定框分割互不
相交，因此五組連通且不交。十對鄰接依次為原 bridge、J 上兩側邊、
四份具名附件、框邊 b_ab_b，以及補弧兩端的兩條框邊。故原圖含 K5 minor。

此為獨立的來源收窄結果，§5 的雙列接受不以本節排除為前提。
102 筆中，只有 C_z 可排除 4 筆，只有 C_wp 可排除 52 筆，兩者都可
排除 38 筆，合計 **94 筆來源排除**。這不以 target 拒絕為前提，亦不
計作 target 延拓。保留 8 筆只來自原 ID 54、156，各四筆。

## 5. 全部雙列接受與保留八筆的精確搬運

對 target β，若 σq|S_C=β|S_C，搬運整份 relation，得到
F_C(β)=σF_C(q)。無此置換時，枚舉容量≤k_C、受 β(S_C) 逐色穩定子
保持的全部完整 F 上界，包括空集；k_C 依次為 **2、2、1**。真實 F
一定在其中，不聲稱各候選可實現或同一來源可跨列自由選擇 relation。

在同一色框，對每組 F_z′、F_p′、F_s′ 定義

\[
E_z=U\setminus F_z',\qquad E_w=U\setminus(F_p'\cup F_s'),\qquad
X=U\setminus\{\beta_i\},\quad Y=U\setminus\{\beta_j,\beta_k\}.
\]

|E_z|≥2、|E_w|≥1。原 mixed 精確禁對在 |Y|=2、Y⊂X 時為
F_*=Y×(X∖Y)，否則為空；接受恰在

\[
(E_z\times E_w)\setminus(\Delta\cup F_*)\ne\varnothing.
\tag{6}
\]

**排除前全部 102 筆的 204 查詢，共 348 組完整禁色候選均滿足 (6)。**
其中 176 個查詢的三份關係均精確搬運；其餘 28 個查詢使用上述完整
F 上界仍全部接受。因此指定雙列分離不需 §4 的 pair K5 排除；§2
支援下界所用的局部 K4-free 論證仍保留，不能省略其平面性前提。

另看排除後保留的八筆，三份 relation 在兩個 target 都可整份置換搬運，
故每個 target 恰有一組精確禁色資料；**16 組全滿足 (6)**，不需使用
較寬的非置換上界。另直接枚舉同一 z、w、u、v，保留原
zw、wu、uv、vz、zu 與 u／v 附件，核對 root 色對集合完全一致。
固定 root 見證後，每份原 unary 各由自己的完整 relation 取得全部
接點避開 root 色的 tuple／coloring，才接合不同分量。沒有複製共鄰 u。

例如 record 0 的 S_z=01、S_p=03、S_s=23、i=2、{j,k}=12，原 ID=54，
q 禁色為 {0}、{2,3}、{0}。S_p=03 保留經 b4 的支援間隙，沒有填成 034。
p₁ 的禁色為 {0}、{1,3}、{0}，見證 (z,w,u,v)=(1,2,3,2)；
p₂ 的禁色為 {0}、{2,3}、{2}，見證為 (1,0,3,0)。其餘保留資料見
[全表](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single/support_table.md)。
每個 target 均保存一份對該列全部候選通用的 (z,w,u,v) 見證。

ρ(i)=3−i mod5、π=(0 1) 同時搬運具名支援、禁色、原外部路徑與字面列
Tβ=π∘β∘ρ，Tq=q。102 筆閉合，204 個字面反射 target 逐份核對，
並保留 p₁、p₂ 的直接計算，沒有僅比較正規化後的相等分割。

## 6. 出口接合、重播與停止點

若本型 M 是 Σ(G₀)=Ω∖{p,q} 來源的 minimal q-core，刪邊繼承給
Σ(M)⊇Ω∖{p,q}。共同對齊 q 後 p 是 p₁ 或 p₂；本輪接受 p 而 M 仍
拒絕 q，才推出 **Σ(M)=Ω∖{q}**，接回 [條件式出口](c5_single_sided_exit.md)
第八類。不由一般來源接受兩列單獨推出完整 Σ。

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py) 與
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single/observations.json)
綁定原資料／直接輸入 SHA256、完整 schemas、所有 placements、具名
contact words、q／target 接合、反射、路徑與 minor branch sets。
有限核對共 450 次 q／target 公式與直接著色比較、204 次字面反射，
保留列的 16×24=384 次共同色框見證；全部 348 組 target 候選則為
8,352 次，兩種口徑分開記錄。94 份排除各保存一份 skeleton；兩種 root
再測長度 1／3／5 的每條
bridge 與直接／共幹 tethers，共 36 份附加控制。每份均檢查五組連通、
不交及十對原邊鄰接；它們不是 degree/list 來源 cover。
負控制包括缺 bridge、缺 tether、缺框邊、缺外部接合、branch sets 重疊，
以及多供應點不能任選與支援交錯。48 份 residual、192 份逐塊穩定子控制
沿用既有實作。有限控制不能替代上述任意大小證明。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [本輪紀錄](history/2026-09-29-adjacent-mixed-edge-shared-t0-pair-single.md)。
停止點為 t_w=0、(2,1) 完成指定雙列分離；共鄰端點型只剩
**t_w=0、(1,1,1) 的原 108 筆**，須保留 C_z 二接點及 w 的三份不同
單接點原分量、全部 actual supports 與原 diamond 次序。一般雙 root、
其他 mixed、degree≥6 及更一般核心仍保留。沒有獨立第二審稿者，未新增
Lean theorem；`lake build` 不形式化本輪拓撲或證明 disk 可實現性。
