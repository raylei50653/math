---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared-t1-pair
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge-shared
  requires:
    - c5.adjacent-degree5-mixed-edge-shared-t2
    - c5.single-spoke-two-two-external
    - c5.adjacent-degree5-singleton-long-arc
  related:
    - c5.single-sided-exit
---
# 共鄰端點 mixed K2：t_w=1、(2) 的局部 K5 與指定雙列分離

後續（2026-09-29）：[t_w=1、(1,1)](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md)
已由三份 unary 的局部支援下界與飽和環序完成雙列分離：原 72 筆接合為
32 筆必要支援，64 查詢全接受，不需 T4 或新 K5 排除。共鄰端點型 t_w≥1
全部接回出口；下文保留本輪語境，下一入口見 HANDOFF。

2026-09-28，基準 main@e83f614。審核使用者提出的相鄰支援對／外部路徑
方案，直接從 repo 原 observations.json 重建並綁定 36 筆來源正常形。
訊息中的 ZIP 未掛載於本環境；本輪 checker 是獨立重建，沒有讀取或重播附件。

**本型完成任意大小的指定雙列分離，不需 T4，也不需新增跨列 first-bridge
引理。** 兩套幾何枚舉均得 1,140 份必要支援；接合原正常形得 356 筆，
其中 292 筆由原 diamond／w-spoke 路徑給來源 K5，保留 64 筆的
p₁=01021、p₂=01212 共 128 個查詢全部接受。這些是必要資料數，並非圖數。

證據為下面兩段任意大小紙面搬運、外部 degree-list 定理、有限 Python
證書。未新增 Lean theorem；必要表未證 disk 可實現性，一般單側／共同
出口及 K∞=K≤5 仍未證。研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與原 36 筆正常形

G 有限簡單，B=(b0,…,b4) 是 induced disk 外框；有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}。G 拒絕 q，刪任一非框邊後接受 q。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4。H−{z,w} 的唯一
mixed 原分量是 uv，root incidences **恰為 zu、zv、wu**。
本型 w 有唯一原 spoke wb_s，且 w 側 unary 接點分拆為 (2)。

[前報告](c5_adjacent_degree5_mixed_edge_shared.md) 已證 z 無 spoke，
兩側各有一份原二接點 unary 分量 C_z、C_w。固定具名接點
(x₀,x₁)、(y₀,y₁)、actual supports S_z、S_w，並寫
N_B(u)={b_i}、N_B(v)={b_j,b_k}，j≠k。全部原邊、旁支、bridges
與接點身份保留。以下 h、e、d 是 {0,1,2} 的一個排列：

\[
q_i=h,\quad\{q_j,q_k\}=\{h,e\},\quad c=q_s\in\{h,d\},
\qquad F_z(q)\in\{\{h\},\{h,d\},\{h,3\}\},\quad F_w(q)=U\setminus\{c,e\}.
\tag{1}
\]

這正是 6×3×2=36 種正常形。F 是**完整有序接點關係**中全部 tuple
色集的交集。非空關係與兩接點容量給 |F|≤2；若 |F(q)|=2，逐接點
解除給兩個相反次序的完整關係；若 F_z(q)={h}，保留前報告的 95 種
完整 schema，並再以 S_z 的 q 色穩定子篩選整份 tuple 集合。
所有必要支援至少留一種 schema，沒有為湊數額外放寬來源模型。

checker 對正常形 key 與原 JSON 的 36 筆作一對一集合核對，保留原 ID、
完整原記錄、原局部 K2 支援 ID、schema IDs 及全部原 schema。輸入 JSON
SHA256 為 `6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`；
新證書 `original_source_ids_bound=true`。原 306／288 筆證書未改寫。

## 2. 局部 degree-list 前提與 K4 排除

先抽出一份只接 r∈{z,w} 的原 unary C。C 內每點仍完整 degree=4，
外鄰只在 B∪{r}，另一 degree-5 root **不在 C 內，也不鄰接 C**。
忽略 r 顏色的 boundary lists 在接點有 slack，所以 C 可著色，R_C 非空。
若 a∈F_C(q)，再從兩接點刪色 a 得不可著色 degree lists M_a，逐點
|M_a(v)|≥deg_C(v)。沿用 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的 tightness 與 Gallai／blockwise-uniform palettes；本輪核對原文第 5–6 頁。

**解除前提同樣局部。** 刪 C 內一條非 bridge 邊，連通來源兩端有 slack；
刪 bridge，兩個連通部分各在斷口有 slack；刪 boundary／root incidence，
原 q 外鄰色互異，該點多一可用色。因此每種刪除後皆可著色。
對 a∈F 的 root incidence，a 不重複 boundary 色，否則 M_a 已有 slack。
這也恢復飽和 pair 的兩個解除 tuple，沒有忽略另一 root 的全圖限制來
宣稱整圖可著色；這裡只證原 C 的完整關係。

C 的 K4 block 也可局部排除。設 J≅K4 是 block，每點除其三條 clique
邊外恰有一個方向：直達 B∪{r}，或一條進入 C 旁支的 bridge。
不同點的這些旁支不交。刪這條 bridge 後兩側都可著色；若根能取不同
顏色即可接回，故兩側根被迫為同一 singleton 色。旁支必碰 B∪{r}，
否則其無預著色根可任意換色。於是 J 的四點各有到 B∪{r} 的路徑，
四條路徑的內點互不相交。

原 r–u–b_i 路徑對 r=z、w 都存在，避開 C，使 B∪{r,u} 為連通外部 hub。
將四條路徑的內點併入 hub，J 四點與 hub 給 K5，矛盾。故 C K4-free；
更大 clique 已由平面性排除，blocks 只剩 bridges／odd cycles。
此證明完全未要求 C 外所有內點 degree=4。

**兩份支援都至少見兩個 q 色。** S_w 由 pair F_w 的色穩定子立即得到。
若 S_z 空，全色對稱與 0<|F_z|≤2 矛盾；若只見一色 a，穩定子迫使
F_z={a}。固定 r=a 後只有一種外鄰色，tightness 給每點 deg_C≥3，
卻與 K4-free Gallai tree 的葉塊私有點內度≤2 矛盾。故兩份支援非空，
跨度各至少一。這是在 annulus 前先完成的局部論證，不循環引用有限域。

## 3. C_w 二接點的 annulus 同序搬運

原 diamond D 的邊為 zw、wu、uv、vz、zu。四點各有內部避開 D 的
B 路徑：u、v、w 用原 spokes，z 用連通 C_z 及一個 actual attachment。
故四點都在 D 的外面；D 二連通，唯一含四點的外面 cycle 是
Q_D=z–w–u–v–z，原 chord zu 在內側。每份 C 都碰 B，且分量內連通、
不含 root，所以整份在 Q_D 外側；不可能部分留在其有界面。

取 Q_D 閉內部的細正則鄰域，外側為 annulus。C_z 的兩條 contact
同屬 z 外側區塊。對 C_w，若唯一 w-spoke 夾在其兩條 contacts 間，
取 C_w 內連接 y₀、y₁ 的簡單路徑，與 wy₀、wy₁ 成 Jordan 曲線。
曲線完全在 B 內部。若不含 B 的一側容納 spoke，它無法到 B；若該側
容納 D，則 u、v 的 spokes 無法到 B。因此 C_w 的 contacts 也必連續，
spoke 在整個 C_w 區塊之前或之後。兩 contact 的具名方向仍都保留。

五個原單位的次序遂為

\[
C_z,\quad\operatorname{perm}(C_w,s),\quad u,\quad v
\tag{2}
\]

或整體反向。在同一 b_i 的小鄰域內分開原邊端，顏色及框點身份不變。
每個單位都有連通細鄰域接 annulus 兩邊界，單位之間不交。單位中
連接兩個外端的 crosscut，其不含內圓周一側不能有另一單位的外端，
因後者必連回內圓周；內外端的次序不同也會迫使 crosscuts 相交。
這給與 (2) 同序的外端區塊，補足 C_w 由一接點改為二接點的前提。

從 C_z 第一個外端起讀，actual supports 可各提升一次為整數集 T_A：

\[
\min T_{C_z}=a,\quad \max T_{O_r}\le\min T_{O_{r+1}},\quad
\max T_{O_4}\le a+5,\quad T_A\bmod5=S_A.
\tag{3}
\]

不同單位可共享框點端點；各支援內可有間隙，不將其填成整弧。
同一支援若首尾重複同一框點就佔滿一圈，與其他正跨度單位矛盾，故
每份跨度<5。C_z、C_w、v 各跨度≥1，s、u 跨度零；總跨度≤5。
不要求選最短 cyclic hull。checker 的遞增整數 lifts 與獨立 hull-edge
mask／w 整體區間兩算法，均完全列出 (2)–(3) 的 **1,140** 份資料。
每份保存全部 placements 與兩個 binary 區塊的四種具名 contact words。

## 4. 飽和雙禁色 bridge 與外部 K5 的局部版本

取 §2 的 C、r，假設 F_C(q)={a,d}。比較 M_a、M_d 的既存 palettes。
在 block incidence tree 的 x₀–x₁ 路徑外，由葉向內消去旁支；非 root
lists 相同，故每個旁支 palette 相同。路徑端點的 residual 差為 {d}/{a}，
沿路每個 block 的 palette 差都非零。odd cycle 的第三個頂點既非接點，
扣掉其旁支後卻迫使兩份 cycle palettes 相同，矛盾。因此路徑全部是
**原 C 的 bridges**；singleton palette 對交替 (d,a)、(a,d)，另一端
要求 (d,a)，所以原路徑 P=(x₀,…,x_ℓ) 長度為奇數且 ℓ≥1。

刪 P 所有邊，令 W_j 為包含 x_j 及其全部旁支的原連通塊，T_j⊆S_C
為其實際 boundary 支援。原 bridges 保證各 W_j 不交，只含一個路徑點。
令 D_j=q(N_B(x_j))，Q_j 為路徑外 palettes 聯集。由非 root lists
向上歸納，每個 rooted branch palette 唯一，且兩拒絕證書給同一 Q_j。
內點兩個路徑 palettes 聯集為 {a,d}；端點的 E=U∖(D_j∪Q_j) 同時滿足
E∖{a}={d}、E∖{d}={a}，也得 E={a,d}。故

\[
D_j\cup Q_j=U\setminus F_C(q),\qquad
\sigma F_C(q)=F_C(q)\quad\text{若 }\sigma\text{逐色固定 }q(T_j).
\tag{4}
\]

後式由同一 rooted palette 唯一性得到；不需要 root 的 list 在換色下
固定。因 q 不用色 3，(4) 恰要求每塊見到

\[
E(F)=F\quad(3\notin F),\qquad E(F)=U\setminus F\quad(3\in F).
\tag{5}
\]

若這兩色在 **actual S_C** 各只有一個供應點 b_a、b_b，則每塊都有到
兩點的原附件。多供應點時只能保留選言，不能任選代表。

再假設 a、b 相鄰，D_B=B∖{b_a,b_b} 為連通補弧；有原簡單路徑 L
由 r 到 b_h∈D_B，內部避開 C、B、r。L 可經另一 degree-5 root，
其 degree 不出現在下列圖論構造的前提中。取任一原 bridge x_jx_(j+1)，
J=P∪{rx₀,rx_ℓ}，五個 branch sets 為

\[
A=W_j,\quad A'=W_{j+1},\quad
Z=(V(J)\setminus\{x_j,x_{j+1}\})\cup V(L)\cup D_B,\quad
X=\{b_a\},\quad Y=\{b_b\}.
\tag{6}
\]

A、A' 連通；J 刪相鄰兩點後經 r 連通，ℓ=1 時就是 {r}，L 再連至
D_B，故 Z 連通。各 W 不含其他路徑點，L 避開 C，而三份框點集不交；
五組因此非空、連通、兩兩不交。十條鄰接逐一為：

| branch-set pair | 原邊 witness |
| --- | --- |
| A–A' | 原 bridge x_jx_(j+1) |
| A–Z、A'–Z | J 上各自另一條邊，端點處是原 root-contact |
| A–X、A'–X、A–Y、A'–Y | 兩塊各自到 b_a、b_b 的實際附件 |
| X–Y | 相鄰框邊 b_ab_b |
| Z–X、Z–Y | 補弧兩端的原框邊 |

因此原 G 含 K5 minor。這是 [相鄰支援對與外部路徑引理](c5_single_spoke_two_two_external.md)
的局部化：§2 核對 degree-list／K4／解除，§4 核對 bridge、逐塊支援與
minor；沒有直接繼承舊報告「全圖唯一 degree-5」的整套假設。

## 5. 292 筆來源排除與 64 筆雙列接受

將 (1) 與兩份完整 F 的 q 支援穩定子、q(S_z) 至少兩色接合，得 356 筆。
原 36 正常形有 20 筆無相容支援。對每份 pair F，按 (5) 找唯一供應
的相鄰框點對；只在原 diamond、ub_i、vb_j、vb_k、wb_s 中尋找 L。
**292 筆均有這種原路徑，無一需要穿過另一份任意大小 unary。**
其中只用 C_z 可排除 44 筆、只用 C_w 146 筆、兩者都適用 102 筆。
這是來源排除，不能計作新增 target 延拓，也沒有用 target 拒絕作前提。

使用者的例子在新表為 record 53：S_z=0134、S_w=12、s=i=2、{j,k}=23，
F_z={0,2}、F_w={2,3}。C_w 的 E(F_w)={0,1} 唯一供應為 b2、b1，
L=w–z–v–b3 是原路徑，(6) 的 Z 接上補弧 034。完整路徑選擇保存在
證書中；即使此例 target 有拒絕上界，也不成為新的來源障礙。

排除後的 64 筆只來自四個原正常形：

| 原 source ID | h/e/d | F_z(q) | c | F_w(q) | 排除前支援數 | 保留數 |
| ---: | --- | --- | ---: | --- | ---: | ---: |
| 61 | 0/1/2 | {0} | 0 | {2,3} | 74 | 30 |
| 163 | 1/0/2 | {1} | 1 | {2,3} | 74 | 30 |
| 251 | 2/1/0 | {2,3} | 2 | {0,3} | 12 | 2 |
| 302 | 2/0/1 | {2,3} | 2 | {1,3} | 12 | 2 |

對 target β，若 σq|S_C=β|S_C，搬運的是整份原 relation，故
F_C(β)=σF_C(q)。無此置換時，使用 `component_options` 的完整 F 上界：
枚舉所有容量≤2、受 β(S_C) 逐色穩定子保持的禁色集合，包括空集。
真實 F 一定在其中；不宣稱每份候選都來自某圖或能跨列獨立實現。

對每一組完整候選 F_z′、F_w′，在同一色框定義

\[
E_z=U\setminus F_z',\quad E_w=U\setminus\{\beta_s\}\setminus F_w',\quad
X=U\setminus\{\beta_i\},\quad Y=U\setminus\{\beta_j,\beta_k\}.
\]

前報告的精確 mixed 禁對 F_* 在 |Y|=2、Y⊂X 時為 Y×(X∖Y)，否則為空。
逐份核對 (E_z×E_w)∖(Δ∪F_*) 非空；638 組保留 target 候選全部通過。
另直接枚舉同一 (z,w,u,v)，包含原 **chord zu** 及全部原 boundary 邊，
所得 root 色對集合與公式完全相同。固定見證 (a,b) 後，a∉F_z′、b∉F_w′
依完整 F 定義各給一份原 unary 的完整 tuple／著色，然後才接合不同分量。
這不乘同一分量的 contact marginals，也不複製共鄰 u。

## 6. 反射、證書與出口接合

ρ(i)=3−i mod5、π=(0 1) 同時搬運全部原支援、禁色、路徑與字面列
Tβ=π∘β∘ρ，Tq=q；356 筆閉合，來源排除見證也逐路徑反射核對。
712 個反射 target 查詢不只正規化 target 的相等分割。

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_pair/observations.json) 與
[全表](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_pair/support_table.md)
保存輸入 SHA256、36 筆原記錄、幾何／contact words、q 與 target 完整
禁色候選、原 diamond 路徑、反射 ID 及局部著色 witnesses。有限核對包括：

- 2,578 次 q／target 公式與原四點直接著色集合比對。
- 保留資料的 638×24=15,312 次共同色框見證核對；連排除前候選中
  仍有局部見證的項目一起核對則為 52,368 次，兩種口徑分開保存。
- 48 份端點／內點 residual、192 份逐塊支援穩定子控制。
- 每份排除一個含原 diamond、兩 unary 接點及原 spoke 的 K5 skeleton，
  加例子長度 1／3／5、每條 bridge 及共用 tether 的 18 控制，共 310 份。
  逐份核對連通、不交及十對原邊鄰接。它們不是 degree/list 來源 cover。
- 缺原 bridge、缺 tether、缺相鄰框邊、缺補弧外部接合及重疊 branch sets
  均使指定 witness 失效；另核對多供應點不能任選、spoke 不能在 C_z 開弧。
  幾何域明確含共享端點、間隙及非最短 cyclic hull。

**出口接合另用來源假設。** 若本型 M 是 Σ(G₀)=Ω∖{p,q} 的 minimal
q-core，刪邊繼承給 Σ(M)⊇Ω∖{p,q}。對齊同一 q 後，p 為 p₁ 或 p₂，
本輪證接受 p，且 M 仍拒絕 q，才推出 **Σ(M)=Ω∖{q}**。
[條件式單側出口](c5_single_sided_exit.md) 第八類因而擴至本型，沿既有
刪邊序列得到單側出口；不由一般來源接受兩列直接推完整 Σ。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行及未重跑範圍見 [本輪紀錄](history/2026-09-28-adjacent-mixed-edge-shared-t1-pair.md)。
停止點是 **t_w=1、(2) 完成指定雙列分離**；接續 t_w=1、(1,1) 的 72 筆。
t_w=0 兩型、其他 mixed、一般雙 root、degree≥6、非相鄰 roots 與更一般
核心分離均保留。本輪沒有獨立第二審稿者或 Lean 形式化；上述紙面搬運
與有限證書是不同信任層，`lake build` 不能替代任意大小證明的審閱。
