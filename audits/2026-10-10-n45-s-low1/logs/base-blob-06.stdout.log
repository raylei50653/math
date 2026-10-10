# E3：非相鄰雙 degree-5 roots 的紙面約化

2026-10-04；`task-e3-excess-two`，基準 main `2ddc6b4`。
本文件、[checker](../../scripts/c5_excess_two_e3_nonadjacent.py)及
[certificate](nonadjacent.json)只新增；原報告、原 artifacts 與共用文件不改。
完整 E3 結論由 [REPORT](REPORT.md)負責。

**本分支仍未全部排除。** 已得到不依賴精確 mask 的原圖必要形、
非相鄰 `(4,4)` cores 的 mixed 數限制，以及空支援 one-sided mixed 的 hub 排除。
唯一 mixed 刪後會斷開 roots；不能借用相鄰案例的 mixed 盾弧。
下列剩餘不是「待 K′」：K′ 指定相鄰 roots，不能填補非相鄰分支。

## 1. 前提與證據邊界

沿 E2 §1：指定有序 induced-C₅ disk；T4 全收；每條非框邊對自身
完整 Σ critical；有效私有點忽略孤立點；ε=2。
選定 941 形三個拒絕位置 `{0,1,3}`，其 canonical pattern indices 是
`{6,4,1}`，字面列分別為 `01212`、`01202`、`01021`。
不假設另兩個三色列接受，也不假設完整 Σ 恰為 941。

本節 roots `z,w` 完整 degree 都是五，沒有原邊 zw；其餘有效點完整 degree 四。
E2 §2 的前提推導直接給 H 連通、每點 degree≥4、G 碰齊 B。
另 T4 直接使每點至多三條 spokes。
這些推導不用三列的具體位置，只需至少兩個拒絕列。

| 證據層 | 本文件與 checker 的作用 |
| --- | --- |
| 任意大小紙面 | §2–6 的原圖飽和、core 省略分類、one-sided 判定、盾弧與 hub 排除 |
| 沿用紙面＋既有有限合成 | 全 degree-4 core 的 path／一 triangle／兩 triangle 分類；E2 ε≤1 結論。没有重跑其枚舉 |
| 外部定理 | hub 原則的 degree-list／Gallai block-palette 依賴；不是 Python 成果 |
| 新 Python | 兩張已可實現控制圖的完整 Σ、逐邊 criticality、具名原分量與全部 contact tuples／root fibres；1,284 份有限整數預算；64 份具名外路 hub 分袋 |
| 未承擔 | 任意大小 mixed relation 分類、disk 實現決策、完整 E3 排除、Lean theorem |

Gallai 外部來源重新打開核對：Dvořák，
[List coloring and Gallai trees，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
connected degree-list 不可染時 lists tight；其 Gallai block palettes 刻畫供 hub 原則使用。
四色回溯只算兩個固定圖與固定 local assignments；未以四色定理作 oracle。

## 2. 原分量、刪 root 與例外：全部可直接移植

P 始終是原 H−{z,w} 的完整連通分量；保存所有原 contacts、shared 頂點、
實際框附件與 support。令 m 是 mixed 原分量數；令 m_z,m_w 是所有 mixed
在兩 roots 上的原 incidence 總數。H 連通且 zw 不在原圖，故

`m≥1, m_z≥1, m_w≥1`。

所以 nonadjacent no-mixed 分支直接不可能。這一步沒有用任何指定拒絕列。

令 S_z 是 B、z、全部 unary-at-z 原分量與其全部原邊、附件；S_w 對称。
[刪 root 報告 §2–3](../../docs/c5_excess_two_root_deletions.md)的證明不讀精確 mask：

- 對同一字面 boundary row，刪 w 後所有原 w-contact 留有 degree slack，
  mixed 與 unary-at-w 各能填入，保留原 z 色；故 `Σ(G−w)=Σ(S_z)`。
- `deg_{S_z}z=5−m_z≤4`。若 S_z 拒絕，自己是全 degree-4 minimal core，
  且 `m_z=1`、完整 Σ 恰只缺該一列。
- S_z、S_w 若同時拒絕，各有四點 actual support、內部互斥；原 disk 的交錯
  路徑矛盾排除。所以全部拒絕列中至多一列有省略任一原 root 的 core。

因此三個指定列中至少兩列的每份 minimal core 都含兩 roots。
當 `m≥2`，自然 `m_z,m_w≥2`；兩個刪 root 圖皆 Ω，所有拒絕列的每份
minimal core 皆含兩 roots。
當 `m=1`，只在其某一側 incidence=1 時可能有一個原 unary-side 例外。
該側仍需至少一份 unary，因 root degree 五而 spoke 數至多三。

「至多一例外」沒有假定三個指定列恰等於 Q；完整 Σ 的其他拒絕列也受同一限制。

## 3. One-sided 與盾弧：區分唯一／多 mixed

每份 unary 都 one-sided。非相鄰配置更有完整判定：

- `m=1`：唯一 mixed C 的刪除使 z、w 斷開，故 C **不是 one-sided**。
  H−C 至少有含 z、w 的兩個分量；只能給 unary 收盾弧費用。
- `m≥2`：刪任一 mixed 仍有另一份原 mixed 給 z–w 路徑；
  unary 也接回 root，所以所有原 pieces 都 one-sided。

[盾弧引理 1、2、定理 A](../../docs/c5_unary_shield_budget.md)的證明只需本題已推導的
H 連通、全框被碰、完整 degree 四及原 critical 拒絕見證。
故每份 unary 的原盾弧至少兩邊，總數至多兩份。
兩份時長度 `(2,2)` 或 `(2,3)`，所有 root spokes、所有 mixed actual support
都避开它们的盾弧內點，分别限制到三个或两个具名框点。

若 `m≥2` 的某份 mixed actual support 不包含於任何框邊兩端，
其盾弧亦至少兩邊。因而

`兩份 unary + 一份長支援 mixed ⇒ 2+2+2>5`，直接排除。

這是三個**不同原 one-sided pieces**，不是把同一 piece 的三個支援角色收费。
`m=1` 不符合 mixed one-sided，故該推論不能使用。
沒有 unary 時，盾弧沒有被消耗；一份短 mixed 也沒有普遍長盾弧下界。

以上不使用三列的具體位置；不會排除 Σ=951／935 兩張正控制。

## 4. 新 hub 引理：空支援的 one-sided mixed 非 critical

**引理 N-empty。** 設兩 roots 配置中的 degree-4 原 mixed P 滿足
`H−P` 連通及 `N_B(P)=∅`。則 P 能延拓 G−P 的每一份合法四色染色。
因此它不可能帶任何 Σ-critical 接點邊。

證明：在同一原 H−P 取簡單 z–w 路徑 L；只有這兩個 roots 是 P 的外鄰點。
固定任意合法外部染色 ψ。若 ψ(z)=ψ(w)，取一個 hub `X=V(L)`。
它在 N(P) 上同色。若两色不同，将 L 在任一原路徑邊切成两袋 X_z、X_w，
各包含对应 root；两袋原連通、互斥且由該原邊相鄰。
每袋在 N(P) 上只見自己 root 的色，两色不同。

若 ψ 不可延拓 P，由完整 degree 四的 lists 及拒絕 tightness，
[hub 原則 B](../../docs/c5_unary_shield_budget.md#4-定理-bhub-原則)给 K₅ minor，矛盾。
因此全部 ψ 都延拓。若 e 是 P 的任一 contact 邊，G−e 新接受的染色限制到
G−P，再填回完整 P，会让 G 接受同一列，與 criticality 矛盾。

不要求 L 内点和 root 同色；hub 的同色条件只针对 `X∩N(P)`。
两 roots 在原圖不相鄰也没有問題，因为 adjacency 来自同一原外路。
这不是凭空补一条 root 邊。

特别地 `m≥2` 時每份 mixed actual support 都非空。
`m=1` 的分離 mixed 缺少避开 P 的 z–w 路徑，不能用本引理。
该引理不读取任何指定拒絕列的身份。
Checker 的64项只核对固定 path/color 分袋，不代替无界 Gallai／平面性论证。

## 5. 每列 q-core 的完整原省略分類

取任一指定拒絕 q 的 minimal core M。原 degree-4 飽和使每份原 piece
只能全部取或全部不取；每個 retained piece 的全部原 root incidences、
框附件及内部边原样保留。

若 M 含两 roots，自己的 root degrees 各为4或5。
若均五，root saturation 和原 H 连通給 `M=G`。
若 degree loss 是 `(1,0)` 或 `(0,1)`，只能省略对应侧的一条原 spoke
或一份容量一 unary；任何 mixed 同時影响两侧，不能省略。
若 loss `(1,1)`，只能有下列两种：

1. 各侧各省略一個單容量 side 因子（spoke 或 unary）；
2. 省略一份 incidence `(1,1)` mixed，且没有其他省略。

这些是原 incidence 级别的穷尽，尚未声称每个形式可实现。
非相鄰 roots 下还必须保留至少一份 mixed，以維持 M 的内部連通；
所以唯一 mixed C 不可能被省略。

| M 的自身 root degrees | 完整原省略身份 | 新增非相鄰限制与状态 |
| --- | --- | --- |
| 仅一 root、degree4 | 只取对应原 S_z／S_w，完整 Σ 单缺失 | 全部列至多一次；只能 m=1 且该侧mixed incidence=1；其他指定列 cores含两roots |
| `(4,4)` | 两侧各一个单位side因子，或一份原 `(1,1)` mixed | 必恰保留一份 mixed；下段給 `m≤2`，来源排除仍开放 |
| `(4,5)` | 一份原 z-spoke 或单接点 unary-at-z | 保留所有 mixed；在 M 自己可用 E2，指定跨列来源接回仍开放 |
| `(5,4)` | 对称 | 同上 |
| `(5,5)` | 没有；M=G | 原双root full-minimal，开放；不可改套唯一degree-5定理 |

**新 `(4,4)` 限制。** 全 degree-4 core 的实际内部只允许路径、一triangle加不分叉枝，
或两个顶点互斥 triangles 以一条直接bridge相连；所有简单环皆triangle。
两个 retained mixed 各给一条 z–w 原路径，内部互斥、长度各至少二。
合成长度至少四的简单环，矛盾。所以恰保留一份 mixed。

结合省略预算：

- `m=1` 的 `(4,4)` core 只能保留该 mixed 并各侧省略单位side因子；
- `m=2` 的 `(4,4)` core 只能省略其中一份 `(1,1)` mixed，保留另一份；
  保留两份的两侧side省略形式不可能。
- `m≥3` 根本不能有 `(4,4)` core；一单位loss预算最多省略一份 mixed。

保留的 mixed 在任一 root 上最多两个原 incidences。若一侧有两个contacts，
该 root 与这两个不同contacts是原triangle，contacts之间有原边；
否则出现长环或同root两个不同cycles，违反原全degree-4分类。
若两侧都是两个contacts，两组三角形不能共用contact（否则给四环）。
core因而是两个原root triangles加一条直接bridge，且没有额外原tails。
这使用实际分类，不將 C 任意压成小图，也不替代其 all-row relation。

对 `(4,5)`／`(5,4)` core，M 的自身 ε=1，q-criticality 蕴含自身
Σ-criticality；E2结论使它拒绝集合至多一点或相邻二点。
故同一个这样的原省略图不能同时拒绝所选 q₃ 与 q₀／q₁。
这是使用指定三列的位置的一步：`3` 与 `0,1` 都不相邻。
同一 `(4,4)` 原省略图只缺一列，不能跨指定列重用。
两项限制没有证明这些省略身份不存在。

## 6. 精确残留与停止点

| 非相鄰来源分支 | 已完成共同约束 | 仍缺什么 |
| --- | --- | --- |
| N1：恰一份 separating mixed | unary≤2；最多一列root-omission例外；不可省略sole mixed；两側单省略與full-minimal按§5分拆 | 保留原两侧／mixed完整relation的跨三列证明；不能给mixed借one-sided盾弧或外路 |
| N2：恰两份mixed | 全 pieces one-sided；empty support排除；两unary加一长mixed排除；`(4,4)`只可省略一份`(1,1)`mixed | 剩余unit-mixed省略的原接回；`(4,5)/(5,4)`各侧单因子；原G的`(5,5)`共同三列 |
| N3：至少三份mixed | 两root删除全Ω；全pieces one-sided；empty support排除；unary预算；无`(4,4)`core | 仍可能的单侧unit省略`(4,5)/(5,4)`與原G的`(5,5)`full-minimal |

没有開始对 mixed joint 的逐 key／逐图分类。1,284份控制仅为两root degree5、
spokes≤3、unary≤2所允许的整数incidence预算；它不含 boundary attachments、
relations、Sigma、rotation或realizability flag，不能从其计数推论没有来源。
这些残留独立于 K′。所以就非相鄰分支而言，现阶段不能写成“E3只条件于K′”。

## 7. 实际正控制与重播

输入为 tracked [cells.json](../c5_cells/cells.json) 的完整具名 951／935 witnesses，
亦为 E1 scratch 所复播的固定代表，不需复制 ignored 历史artifact。
两图分别 ε=2、degrees `(4,4,4,4,6)` 和 `(4,5,5)`；第二图roots相邻。
Root REPORT另外使用 E1 exhaustive 代表作指定主控制。

本 checker 从实际边集补回五框边，独立回溯十个完整ordered patterns。
951／935 的完整 Σ 均吻合；各16／11条非框边全部critical，且每条保存
删边后的完整Σ、新接受列列表和同一字面色框的完整witness。
保存每份原 piece 的 actual attachments、所有具名contacts、root ownership；
对每列、每个完整root assignment保留全部contact tuples及同图见证。
共鄰contact只用一个原顶点坐标；没有将两个root fibres独立相乘。

无指定三列身份的每项新中间约束，都在两图自身适用前提下核验；
neither图被排除。非相鄰／empty-support特定条件不在两图上出现，
checker按蕴含的前提判定，不能把控制上空的前提称为一般证明。

| 命令 | 实际结果 |
| --- | --- |
| `python3 scripts/c5_excess_two_e3_nonadjacent.py` | exit0；新建 `nonadjacent.json`，328844 bytes，SHA256 `0e9b7dad2522ab653e4e98392d55dc79d0eb8da5bf86bbc4bd75d519be2f2e21` |
| `python3 scripts/c5_excess_two_e3_nonadjacent.py --check` | 待本文件生成后执行并由Root REPORT记录 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e3_nonadjacent.py --check` | 同上 |

全域 `check_docs.py`、DocGraph 与 `git diff --check` 由 Root统一执行；
本支线不改共用索引，也不以“新报告未索引”作为修文件的理由。
