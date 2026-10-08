# D₉：E6-A、E6-B/C、E6-H 紙面與 AD 控制獨立稽核

2026-10-06；固定基準 `b2ca4520da50c9d2898ac6f8f966ac25df3f9609`。
本文所有 `E6:L` 行號均指該基準的
[原 E6 REPORT](../../artifacts/c5_excess_two_e6/REPORT.md)；不改原文件、producer 或證書。
E6-D/E/F/G 的整型推導另見 [E5 與 E6 corollary 稽核](audit_e5.md)。
本文獨立核對其 AD controls 的實際 antecedents，並重算 E6-F 的完整 endpoint queries。

**本附件 verdict：holds。** 相鄰 `m≤2`、`m=2` 的 theta 外界限制、共同原 piece/core 身份、
通用 spoke 冗餘表及 G1 的兩種全四 core 分組均成立；沒有找到新紙面缺口或來源反例。
所有結論保留 C₅ 是 disk 外框、接受 T4、Σ-critical、完整 degree 及各自列前提。
控制中的 9 個 ES AD critical orbits 全部 `m=1`；90 個具名 D₅ 搬運 cases 全部不滿足
固定 triple `{q₀,q₁,q₃}`。有限符合及未觸發分開，不用有限結果證明無界拓撲。

## 1. 前提與逐引理 verdict

共同前提由 E6:13–20 給定：有限簡單 disk 圖、有序 induced 外框 B、全 T4 接受、
每條原非框邊 Σ-critical，H 連通並 full B-touch，兩相鄰完整 degree-five roots，
其餘有效內點完整 degree-four。四個完整 masks 為 941、933、940、932；
E6:19 明示不預填 q₂/q₄ 接受。使用逐步表時仍保留其列身份。

| 引理／子結論 | scope | verdict | 基準行號與理由 |
| --- | --- | --- | --- |
| E6-A，相鄰 m≤2 | 一般上述來源；不讀指定 triple | holds | E6:36–62；四條原互斥路的外界 cycle 封住整份原 mixed，導出 actual 空支援；原 zw 使其 one-sided，critical witness 與合法 root hubs 接回矛盾。 |
| E6-A，m=2 外界必由兩 mixed 路組成 | 同上，另 m=2 | holds | E6:67–69；若 zw 是 theta 的外界路，另一 mixed 的整份原分量封住，同一 N-empty 接回矛盾。 |
| E6-B，incidence、原盾弧與 unary budget | 上述來源；不讀 triple | holds | E6:77–83；原 zw 給所有 pieces one-sided；每 root 先扣原 zw，餘容量四；T4 限 spokes≤3；原 actual 支援／盾弧及互斥≤5。 |
| E6-B，proper-subgraph 拒絕輪廓 | E5 L1 的 ε=2 原連通來源 | holds | E6:85–87；對任意 proper S 保留 B，用自身 minimal pair-core；不是要求 S 自己 critical，也不是省略 Ω。 |
| E6-B，q-core 原省略身份與 mixed44 | m≥1；所選 q 自己的 minimal core | holds | E6:89–102；root/zw 全收迫其保留，原 degree-four pieces 飽和全取或全不取；44 retaining mixed 的原長環排除，11 剩餘 contacts 必同是原 x。 |
| E6-C，通用 spoke 冗餘與四分支表 | 一般原來源及精確 Q_G；不擴張 E5 L3 | holds | E6:104–117；同一 β 刪重色 spoke 不變 root guard；D_e⊆Q_(G−e)，套通用 L1。十個原三-spoke 子集独立重算吻合。 |
| E6-H，retaining spoke＋unit-unary 分組 | 已存在相應 rejecting minimal 全四 core | holds | E6:230–243；自身全四分類、每 root 至多再留一 unit unary；原 budget 排 (1,1)，既有三-piece 六跨度排 (0,1)，留下 G2/J4。 |
| E6-H，只省唯一 mixed11 分組 | G−C 確實拒絕 q，且其自身全四 core | holds | E6:245–263；ab 是 bridge、內度≤3，k≤2；k=2 是同一 triangle 的兩相鄰 contacts；六組全列，未預填 M 拒絕或 Ω。 |

E6-H:242–243 只把 J4 的短共用-contact 入口送交 K′，沒有驗證／宣告 K′，
E6:282–284 亦明示不增加 J4 舊 ledger 的 coverage。

## 2. E6-A 七步核對

| 原步驟 | 基準行號 | 獨立核對 |
| --- | --- | --- |
| 四條道路是原 graph subdivision | E6:36–38 | 各 mixed 是 H−{z,w} 不同連通分量；選 z–w 簡單路，內點在各自 piece 中，互斥且避 B。contact 相同容許長二，原 zw 是第四路。 |
| 找含 B 的唯一外面 | E6:39–45 | 四路子圖全在 disk 內且與 B 不交，B 連通並連到無界側，所以落在同一外面；兩條循環相鄰路構成其 Jordan boundary。zw 是否在該 boundary 的兩個 cases 完整。 |
| 從路升到整份原 C | E6:47–50 | 被封 mixed 的 C 與 J 不交；C 連通且至少一原內點在有界側，所以全部原 C 在該側。actual C–B 邊必穿 J，故支援空。沒有把所取路的支援當作整份 C 的支援。 |
| one-sided 與外部連通 | E6:52–54 | 原 zw 仍在；每個其他 piece 至少接一 root，故 H−C 連通。C 支援空使 full B-touch 保留，B 與 H−C 接合，G−C 連通。 |
| 原 hubs 及 tightness | E6:55–56 | 合法外染色使 z≠w；{z},{w} 是原互斥連通相鄰 hubs，覆蓋 N(C)，各只見其 root 色。degree-four tightness 保持原 lists；hub minor 僅作非平面性反證。 |
| 外部引理適用分支 | E6:58–60 | E3 one-sided N-empty 的全部前提已具備；亦符合 E4 N-empty-separating 的 G−C 連通分支。沒有觸發 separating appendage 分支，也沒有向它收盾弧。 |
| critical witness 接回 | E6:61–62 | 原 root–C 邊存在。G−e 新列 witness 限制到 G−C 是合法外染色；只重染完整 C 接回原 e，得到同一 β 的 G coloring，矛盾。未借 Σ(G−C)=Ω。 |

J6 `m≥3` 的 `(4,5)`、`(5,4)`、`(5,5)` core 型都已在原來源層被排除
(E6:64–65)，不需要對各個 core 另作 minimality 假设。
`m=2` 的三路 theta 子論證與上述七步相同，只有一個內側 mixed 即足矛盾。
E6:71–73 的兩個 straight-line 例子只作拓撲示例；本稽核沒有把它們算作
完整 degree-valid／Σ-critical controls。

## 3. 共同 budgets、core 身份及 spoke 表

1. **扣容量與 one-sided (E6:77–83)。** root degree 五扣原 zw，給
   `t_r+Σ k_r(P)=4`。若 t_r≥4，可選 T4 boundary row 使至少四個 root spokes
   見四色，違全 T4 接受。H−P 中 roots 由 zw 連通，每個其他 piece 接 root，
   所以所有 P one-sided。盾弧引理要求的是同一原嵌入；原 critical 邊的
   witness 給 unary 非空 forbidden set，配 full B-touch 排短支援，故 unary
   actual support≥三點、成本≥2、總 budget≤5。singleton mixed 可成本零；
   兩點 short mixed 成本一，沒有套 unary 的成本給它。
2. **引用 E5 L1 (E6:85–87)。** 完整 Q_G 至少含固定三列；proper Q_S 至多二點且相鄰，
   所以每個 G−e 至少釋放 |Q_G|−2 列，且三個固定列至少釋放一個。
   這只用拒絕集合包含關係，不推出 G 是每列自己的 q-core，也不推出 Ω。
3. **q-core saturation (E6:89–96)。** m≥1 是引用原 root/zw omission 全收的必要前提。
   把指定 q-core 當成自身 minimal obstruction，內點 degree≥4；一個原
   degree-four piece 只要留下任何有效點，完整原 degree 便迫原邊逐點傳播，
   全 piece 取回。兩 roots 各最多 loss 一，故省略向量在 {0,1}²；capacity-two
   unary 不能省，44 只可能兩個 unit side 或整份 mixed11，55 即 G。
4. **44 retaining mixed (E6:98–102)。** 保留兩份不同 mixed 時，兩條原內部互斥
   root–root 路加成原長度≥4 cycle，違全四 minimal q-core 的實際分類。
   若只留一份 mixed，但某側至少兩不同 contacts，一條原 piece 內路加 ab
   同樣造長環；故只留 C11，且兩 contacts 同是 x。原 x 相同為字面 identity，
   不把獨立 contact marginals 合併。m=2 因此只能省略一份 mixed11；被省略
   mixed 的 contacts 無須相同。雙-spoke exclusion 的三列條件只在 m=1 的該入口使用。
5. **冗餘欄位 (E6:104–117)。** β(j)=β(k) 使同一 root guard 在刪 rb_j 後完全相同，
   原整圖拒絕保持。D_e 是实际 Q_G 的子集，不加入 optional 接受列。通用 L1
   只限 D_e 為空／singleton／相鄰 pair；右欄 E5 L3 的 |D_e|≤1 僅供其自身
   J2/G3 antecedent。獨立遍歷十個 S 得下表，與原通用欄逐字吻合。

| 完整 mask | 固定 Q | 通用 L1 必要三-spoke 原位置 |
| --- | --- | --- |
| 941 | 013 | 012、013、014、034、123、234 |
| 933 | 0123 | 012、014、034、123、234 |
| 940 | 0134 | 012、014、034、123、234 |
| 932 | 01234 | 012、014、034、123、234 |

上表是四色／五框點的必要算術；不是任何 source family 的實現或 coverage 證書。
引用的全四分類保留自身 q-minimal、全 T4、完整 degree-four、H 連通及 disk 前提
([分類原入口](../../docs/c5_k4_blocks.md):104–123)，未把任意原 Σ-critical G 直接套進分類。
盾弧與 hub 的通用版本在 [原原則](../../docs/c5_unary_shield_budget.md):54–110、130–142、155–179；
其面論證、critical witness、完整 degree lists 前提與上述使用一致。

## 4. E6-H 两个实际 core 入口

**retaining spoke＋unit-unary (E6:230–243)。** 省略 a-spoke 与 b-unitU 恰各减一个 root unit；
M 自身 minimal 全四 core 含原 abx triangle。全四分類禁止同一 root 同时属于第二个
cycle，也禁止外挂树分叉，因此 each root 最多一份 additional unit unary。
原 unary 数为 `1+u_a+u_b≤2`；原 spokes `(3−u_a,2−u_b)` 的算式直接来自原 degree 五。
四个 `(u_a,u_b)` 全列：00→G2，01→三份 H−b components 的原共同六跨度，10→J4，11→三 unary。
01 引用的六跨度实际把 K=C+a 与两 U,V 当三份互斥 connected branches，K 的三原 spokes
给跨度≥2；不是误给短 mixed C 成本二。原依据
[两原 unary 排除](../../docs/c5_excess_two_mixed_core_four_spoke_singles.md):73–81、105–126、129–161
明确不要求指定拒绝位置或 q-minimality，收缩只用于拓扑、不宣称 Σ invariant。
J4 的两个 unary 已占四条 shield edges，所以 retained C 短；共用 x 的外部引理前提齐全。

**只省唯一 mixed11 (E6:245–263)。** antecedent 是 M=G−C 确实拒绝 q。
M 全四，内图由 ab 与原 unary branches 连通，自身 q-core 飽和传播取回整个 M。
ab 若不为 bridge，其另一路必穿一原 mixed，而 M 已无 mixed，故为 bridge。
全四分类给 internal degree≤3，`1+k_r≤3`；原 degree扣 C incidence1 后给 `t_r=3−k_r`。
k=2 若是两 unitU，将形成原 noncycle fork，违反自身 minimal 全四分类；故是同一 binary-U
两个相邻 contacts，与 r 组成原 triangle。原六组 `{00,10,20,11,12,22}` 已覆盖 root exchange 后
全部 `{0,1,2}²`，没有漏 k=0 边界，也没有以表格存在倒推 M 拒绝。
L1／全四分类只给 M 为 Ω 或缺单列；其 rejecting witness 必保存，不能套 omission 必 Ω。

## 5. 独立 AD checker：实际 trigger 分层

[独立 checker](audit_e6_controls.py) 只读 ES 的原 `canonical_edges`、原 `disk_rotation`，
不用原 checker 的 decision logic／derived masks／piece 分类。标准库 MRV DFS 从原边重算十列
完整 Σ、每个原非框刪边的完整 witness；从原邻接表重算 roots／pieces／原 contacts／supports，
从 rotation 的 dart permutations 重算 Euler、外 C₅ 面与 actual shield。
完整 R_U 保留有序原 contacts（同一边界色框）及全部 tuple，再算
`F_U=⋂ set(tuple)`；没有用 contact marginals 替代 complete relations。
全四 q-cores 遍历原 pieces 全取／全不取及原 spokes 取舍，对每条原非框边重算 q-criticality。

输入是 **9 个 source critical orbits**（k=3:1、k=6:2、k=7:1、k=9:5），各作10个整图 D₅ 搬运，
共 **90 个有标号 transported cases**。这些不是90个独立 orbit。原代表 identity masks 依次为
942、1006、1006、959、1006、959、959、1006、1006；其 D₅ 像仍按同一原 edge/rotation/frame 搬运。
9个代表及90个搬运 cases 全部 m=1；固定 triple 触发 **0/9 orbits、0/90 cases**，counterexample为0。

| 实际检查（计数单位） | triggered and holds | not triggered | counterexample |
| --- | ---: | ---: | ---: |
| m≤2（具名 cases） | 90 | 0 | 0 |
| m≥3 四路反证 antecedent（cases） | 0 | 90 | 0 |
| m=2 theta 外界 antecedent（cases） | 0 | 90 | 0 |
| N-empty 空支援 antecedent（原 pieces） | 0 | 230 | 0 |
| one-sided（原 pieces） | 230 | 0 | 0 |
| actual support=shield vertices（pieces） | 230 | 0 | 0 |
| unary 成本≥2（pieces） | 140 | 90 | 0 |
| long-mixed 成本≥2（pieces） | 0 | 230 | 0 |
| 两点 short-mixed 成本1（pieces） | 90 | 140 | 0 |
| 同原图 shield 互斥与总 budget（cases） | 90 | 0 | 0 |
| original root incidence（root instances） | 180 | 0 | 0 |
| 所引 root/zw omission Ω（cases，m≥1） | 90 | 0 | 0 |
| L1 maximal proper 删除（原边） | 2,050 | 0 | 0 |
| 冗余 spoke D_e（原 spoke queries） | 370 | 0 | 0 |
| retained mixed44 shared-x（q-core queries） | 250 | 0 | 0 |
| 二边 U endpoint（完整原关系／boundary row queries） | 1,400 | 0 | 0 |
| G1 retaining spoke+unitU（自身 q-core queries） | 160 | 0 | 0 |
| 上项附带 J4 mixed 短支援（q-core queries） | 120 | 40 | 0 |
| G1 mixed-only 分组（q-core queries） | 10 | 0 | 0 |
| no-mixed 两 unary antecedent（cases） | 0 | 90 | 0 |
| selected-triple G2 盾弧恰二（cases） | 0 | 90 | 0 |
| selected-triple G3 盾弧恰二（cases） | 0 | 90 | 0 |
| selected-triple G3 named support（cases） | 0 | 90 | 0 |
| selected-triple G4 盾弧恰三（cases） | 0 | 90 | 0 |

L1 最大原刪边的2,050次检查足以覆盖任意 proper 原 edge-subset：每个 proper S 包含于某个
G−e，Q_S⊆Q_(G−e)，空／singleton／相邻pair 对取子集封闭。这里不声称重算原报告的
6,742,364,070 子集计数，也不把它当成独立控制图数。
共有260份实际 rejecting 全四 q-core；其中250 retained C，10只省 C。
160 retaining G1 queries 中 G2=40、J4=120；mixed-only10全 k=00，k=1／2 子步未触发。
二边 U endpoint 的1,400次是 **140个原 U 的D₅ instances×10 boundary rows**，实际触发 **8/9 AD orbits、80/90 D₅ cases**（14份原 U 搬运为140个 U instances）；
它们不代表1,400份 source realizations。chosen-triple 整型 G2/G3/G4 与 no-mixed 没有非空
控制前提，不能把其 paper exclusion 写成被这些 controls 验证。

## 6. 重播与证据范围

[e6_controls.json](e6_controls.json) 保存原边、D₅像、全部原边删除的 Σ／新增 rows／完整 witnesses、
原 pieces、full endpoint tuples、q-cores 与逐查询三值 verdict；
[独立重播记录](validation_e6_independent.json) 保存实际命令、exit及日志SHA。
标准库独立 checker 的生成和普通／seed17 `--check` 均实跑，两个 check exit0 且 stdout 相同。
完整任务的 validation 汇总另记录原 E4/E5/E6 checkers，不改其历史 provenance/hash FAIL。

整型 paper lemmas 依赖既有 Jordan／degree-list／Gallai／原全四分类与原 hubs；
独立 Python 只核对上述固定输入及固定四色／五框点必要算术。
不以四色定理作 oracle、不把 minor 当 boundary/T4 invariant、不混一般 planar 与 disk 外框，
不使用旧 omission必Ω filter，不新增 Lean theorem，也不作 lake build。
本附件没有新 gap 的 minimal reproduction；E6-A/B/C/H 指定审阅已完成，范围外分类未重证。
