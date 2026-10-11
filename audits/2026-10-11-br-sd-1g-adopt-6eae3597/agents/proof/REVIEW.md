# BR-SD-1g-ADOPT：独立数学 proof review

2026-10-11；固定审查 BASE／HEAD `c15a635e17d4be814e19aeeeeb765f3d6024099a`。
裁决：**ACCEPTABLE（精确子域纸面证明）**。阻断 findings：0。

本 reviewer 先直接读取原 [PROOF](../../../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)，
从原边、完整 lists 与 block incidence tree 重建 §3–5，再核
[MAPPING](../../../2026-10-11-br-sd-1g-dbdc4c35/MAPPING.md) 和
[canonical §1／§2.11](../../../../docs/c5_excess_two_nonadjacent_unit_core45.md) 的合同。
本审查没有读取原 `agents/paper/REVIEW.md` 或 `ACCEPTANCE.json`；裁决不沿用其结论。
审查输入的当前 bytes 与固定 BASE blobs 逐一相同，见 [INPUT_HASHES](INPUT_HASHES.json)。
本 reviewer 只写本 `agents/proof/`；没有改原证明、seal、canonical、STATUS 或 HANDOFF。

## 1. 接受范围及独立性

接受的是原 PROOF§1 **七项完整合同全部成立时，不存在该原来源**：

- 同一有限简单 ordered induced-C5 disk 原 G、完整有序 Σ933／941 或共同整图 D5 像，
  ε=2、逐非框边 Σ-critical 和完整原删边 witnesses；非相邻原 degree5 roots r/s，
  其余有效原内点完整 degree4、full B-touch、one-sided、非空 actual support。
- 原 U=0、`H_G−{r,s}=L⊔S` 两份完整 mixed，L long、S actual support 恰一真框边 pair。
  所有 W1／W2 原 attachments 分别纳入同一 L／S 的完整 support。
- exact-S 只删 r 的唯一原 spoke e，`X=M=G−e`；M 自己对同一 literal proper 三色 β
  inclusion-minimal 且拒绝，保 M 自己全部 retained-edge 同 β full witnesses。
  G 的 critical 性没有替代 M 的这项前提。
- s 恰有原有序 p∈L、q∈S 两个内邻，原三条 B-spokes 全留；sole connected
  `C=H_M−s={r}∪L∪S`，r split22、C-degree4、M 无 B-spoke。
- 原 J1 triangle `(r,a1,x1)`、任意奇长≥3的原 J2／J3、`J1∩J2={r}`、
  disjoint J3、唯一原环间 bridge uv、任意长度≥0的原 p/q simple bridge arms。
  保 p=a1／q=a3 的零臂身份及 a3=v 的合法重合。
- 两份有限非空 off-skeleton 原 Wi、`C[Wi]` 连通、唯一接点分别 x1、
  `x2∈J3∪q-arm`，W1 属 L、W2 属 S；无额外 s-contact、第二骨架接点、
  Wi 间接线、第三旁支、cross edge 或改变骨架的原边。
- 同一原点／边、附件、具名／有序／shared contacts、ownership、bridges、rotation、
  字面 Col／β，以及 G/M 各自完整 relations、fibres（含空 fibres）、full lifts
  和 effective-H 忽略点的全部原坐标及因子，始终保留。

本定理的证明使用上述完整合同的一部分；这没有授权缩短登记量词。
各必要 degree／attachment 容量列没有被当作 actual source realization。
本裁决只处理纸面证明；finite controls、custody 和 publication 由另行独立审查负责。

## 2. 独立重建：原边 lists、degree assignment、完整接合

令 Z 是 effective-H 省略的原内图孤立点，先保留它们为原坐标；其内部邻居为空。
对每个原 `y∈C`，全部 M 邻居恰分为 C 内邻、B 附件及可能的 s 邻居。
定义原 `A(y)=N_B^M(y)`、`k(y)=|A(y)|`、
`t(y)=1[sy∈E(M)]`，则完整 degree4 给

`d_C(y)+k(y)+t(y)=4`。

Col 恰四色。β 是同一 proper 三色列，D 是它唯一未用色；因此

`L^D(y)=Col \ (β(A(y)) ∪ ({D} if t(y)=1 else ∅))`。

β(A(y)) 的基数至多 k(y)，且 D 不在此集合，所以
`|L^D(y)|=4−|β(A(y))|−t(y) ≥ 4−k(y)−t(y)=d_C(y)`。
所有附件被统计；重复 β 色造成 slack，不可预先假设等式。
r 也在 C 中：其 k=t=0、d_C=4，list 正确地是全部 Col。
Wi 的全部原内边、接入边和附件没有遗漏。

在固定 β／s=D 的完整 assignments 上，限制与接回给出精确双射

`Col_β,s=D(M) ≅ Col_LD(C) × ∏_(z∈Z)(Col \ β(A(z)))`。

这里右方保留各 z 的原标号，而不是仅保存颜色数。B-only 孤立内点 z 没有 C／s 内邻，
其 factor 含 D，故非空；真正无任何原邻居的 z 的 factor 才是全部 Col。
反向接合逐类检查 B–B（β proper）、s–B（D 未用）、B–C／s–C（lists）、
C–C（完整 C coloring）和 B–Z（原 factor）；其余边不存在。
该双射也保存按任意指定原坐标投影后的完整 fibres，空 assignment sets 保持为空。
不能把右方投影后忘掉 Z，再声称完整 assignments 一一对应。

M 自己拒绝 β，因此左方为空。所有 Z factors 非空，于是 C 不可 L^D-coloring。
这一步只用 M 自己的拒绝；没有把 G 的 Σ-critical 当成 M 自己拒绝或 minimality。
M 自身 minimality 和两套 witnesses 虽非此短推论所需，仍保留在最终来源量词。

## 3. 外部 Gallai 前提与 maximal-block palettes

独立浏览作者大学网站的 [Dvořák 2018 讲义](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
印刷 p.5 的 degree-assignment 定义、p.6 的 blockwise-uniform 定义和 Theorem10。
作者版本的条件是 connected graph 与逐点 `|L(v)|≥deg(v)`，无需二连通、list-critical、
planarity 或预先全部 list 紧。非可染时得到 Gallai tree 和完整 incident-union palettes。
桥 K2 是 clique block，palette 大小1；奇环大小2；clique Kn 大小 n−1。
相交的不同 blocks 的 palettes 互斥，逐点 list 是所有 incident palettes 的完整联合。
此项是外部纸面数学依赖；非 Lean theorem。[FETCH](FETCH.json) 留存 fresh primary PDF，
bytes/hash 与原 frozen PDF 一致；[FETCH_REPLAY](FETCH_REPLAY.json) 留存可重播命令结果。

应用对象 C 是原有限简单图、非空且连通，由上一节有 degree assignment 和不可染性，
所有前提成立。C 至少含原 triangle 和更多骨架点，故没有单点 block 边界问题。
每份 Wi 的所有 maximal blocks 一起受刻画，不能遗漏 branch blocks。
若原 Wi 使 C 不是 Gallai tree，已与上述不可染 degree assignment 矛盾；
否则对每个真实 maximal block K 固定同一原色框 palette P_K。

原三环仍为 maximal blocks，uv／外臂仍为 bridges：任何绕过骨架 bridge 或把两个
骨架 blocks 合并的 simple cycle 必须通过 Wi 的唯一接点两次，违反 simple cycle；
原合同又排除了额外 cross edges。这也涵盖同一 xi 到 Wi 的多条接入边。
palette 在同一 literal Col 中选取，不对 blocks 独立换色。
triangle 同时是 clique K3 与 odd cycle，两个定义均要求 palette 大小2，无冲突。

## 4. J2 private witness、固定 T/D 与屏障

设 actual pair 为 `{b_i,b_(i+1)}`。两端在 proper β 下异色，命名为 A／B′；
T 为 β 的第三已用色，D 为未用色。于是 `Col={A,B′,T,D}`，四者不同。
对每个原 `y∈S−{q}`，全部 B 附件在此 pair、t=0，所以完整 list 同时含 T、D。
q 的 list 含 T 而不含 D；不要求 q 的 C-degree 为1，也不要求其 list 只有 T。

任意奇長≥3的 J2 有 `w2∈J2−{r,u}`，包括最小 triangle 情形。
正长臂与 J2 不交；零臂 contacts 只位于 J1／J3；W1 接 J1 的 x1，
W2 接 J3／q 臂。因此 w2 无新增 C 邻边、不是 s-contact、只 incident 原 J2。
`d_C(w2)=2` 与完整 degree4 迫 k=2；原图简单且 S actual support 是同一 pair，
故其两个原附件恰此 pair，`L^D(w2)={T,D}`。
它不是 C 割点：移去该环上非 r/u 点仍保 r–u 路径及所有附接结构。
因此完整 incident union 给出 `P_J2=L^D(w2)={T,D}`。

由完整原接线，`C−r=L⊔S`；唯一含 r 和 S 点的原 block 是 J2。
W2 仅在 S 接入、W1 仅在 L 接入；S 到 L 的任何 C／incidence 路径必须经过 J2。
如果某个 block palette 含 T、D 中恰一色，它不可能与 J2 共原顶点：
若不同，违反相交 blocks 的 palette 互斥；若相同，违反 `P_J2={T,D}`。
所以此类 block 不能包含 r，也不能从 S 跨入 L。此屏障使用两色全部在 J2，
并非只依据边际禁色或某个 cutpoint 的 D-presence。

## 5. 有限树矛盾：逐步不回头且没有隐藏终止前提

取 C 的全部原 vertices 与全部 maximal blocks 构成二部 incidence graph I。
标准 block-cut tree 为树，给每个非割点附上其唯一 incident block 的叶子，
就得到 I；C 连通且有限，故 I 是有限树。没有省略非割点或 Wi 深处的原点。
每个 block 至少含两个不同原顶点。

从 q 的完整 list 含 T，选 incident block K0 含 T；q 的 list 不含 D，
其每个 incident palette 均不含 D，所以 K0 含 T 而不含 D。
「T-only」在本证明只指对固定 pair `{T,D}` 的 exclusivity，**不是**宣称
`P_K0={T}`；palette 可以另含 A／B′。该起始 block 与 q 的实际度数无关。
由上一节，K0 不碰 J2，全部点仍在 S 且不含 r。

若走入 block Kn，保持其 palette 恰含 T／D 一色；从该 block 选不同于进来点的原
`y_(n+1)`。block 至少两点，所以选择始终存在。该点仍在 S，不在 J2、不为 r。
在 I 的树中，每次于 block 选不同出点、于 vertex 选不同出 block，形成不回头 walk；
树中的不回头 walk 无重复节点，否则最短重复段成环。因此新点不会再次是 q。

新点在 `S−{q}`，完整 list 同时含 T／D。Kn 缺少的另一色只能由某个真实 incident
block `K_(n+1)≠Kn` 提供。相交 palettes 互斥使 K_(n+1) 不含原 Kn 已含的色，
所以 exclusivity 交替保持。新 block 也不能碰 J2，因而不能离开 S。
若新点只有一个 incident block，完整 list 的另一色立即无处提供，已经矛盾；
这正是非割点终止情况，而非需要额外前提排除的遗漏。

可避免任何「无限选择」假设：在有限 I 中取满足上述规则、从 q 起、结束于 block 的
最长不回头 path。末 block 有不同出点；树性保证这个出点未出现；该点的另一色又迫
新的不同 incident block，且树性保证它未出现，于是路径可再延伸两条 incidence edges，
违反最长性。所有选择均在有限集合内。这证明有限 C 本身已给矛盾。

该推论始终从完整 incident union 选**另一份** palette。
从未使用 `D∈L^D(x1) ⇒ D∈P_J1`，也没有把原 list 中某色分给每份 incident palette。

## 6. Corner cases 与非阻断精度核对

| 情形 | 独立处理 |
| --- | --- |
| J2 为 triangle | r／u 之外仍有一个 w2，J2 witness 精确保留 |
| J3 为 triangle、W2 佔用其唯一 private witness | 完整证明不选 J3 witness，仍从 J2 与 q 出发 |
| h=0、p=a1 | p 留在 L；S 唯一 s-contact 仍为 q，主路径不使用 J1 witness |
| ℓ=0、q=a3 | q 的 list 禁 D 且含 T，足以构造 K0；不需 q leaf 身份 |
| a3=v，包括 ℓ=0 | 允许在原点身份上重合；J2 witness 与 S–L 接口不受影响 |
| x2=q／正长臂内点／普通 J3 点 | q 或臂点可有新 C 邻居；主证明仅用完整 list 与 ownership |
| x2=a3=v | 原完整 degree 先排超度，主证明无需把非法列装成合法 source |
| 非割点、leaf block | 缺色没有另一个 incident block，立即矛盾 |
| W2 含 triangle／K4／更深 blocks | 刻画逐 block 適用；至少两顶点与相交 palette 互斥即可，无大小枚举 |
| 任意有限非空 W2 | I 仍有限；最长路径证明覆盖任意大小，没有从六个 fixtures 外推 |
| W1 bridge／首 triangle | 可合法把 D 路由到 W1；其不能构成 J1 的 D 矛盾 |
| β 附件重色造成 slack | 初始 degree inequality 保留；Gallai 只在确有不可染时推完整 palettes |
| true free isolated／B-only isolated 原点 | 前节完整 factors 均留原坐标，不把它们忘掉后声称双射 |

PROOF§6 的局部 W1 示例正确：J1 palette 可为 {A,B′}、J2 为 {T,D}，
x1 的 D 全由 W1 首 block 提供；m1=1 的首 bridge 取 {D}，
m1=2 的首 odd cycle 取 {T,D}。W1 连通且唯一接点，使 x1 在其 branch 子图中非割点，
只有一个首 block；m1=2 的 Gallai block 是 odd cycle（triangle 也在内）。
这些只是局部 degree/list/palette 机制，不是完整 disk／Σ／witness 来源。
因此原失效推论有保留的 counterexample，主证明独立避开它。

## 7. 裁决、依赖与未完成义务

**ACCEPTABLE**：完整精确 BR-SD-1g 子域的纸面排除经过独立推导，阻断 findings 为0。
可在 root 完成 mapping、custody、finite replay 和最终 bytes 审查后准备 owner 审批提案；
本裁决本身没有正式采用或修改 canonical。

核心数学信任链为原合同／原边定义 → 完整 lists／full join → 作者讲义 Gallai
Theorem10／blockwise-uniform 定义 → 保留 J2 原 witness／S ownership 接口
→ 本 proof 独立重建的有限 all-vertex incidence-tree 矛盾。
既採 BR-SD-1a／1c／1e 的精确合同定义与旧局部引理界线已核对；
新 §3–5 的最终排除不需要借用三者排除结论，不依 SD-A、二连通、R31 或 minor replacement。

六份旧 synthetic fixtures 或 root 的新 independent controls 仅证明各自具名有限测例。
本 reviewer 没有提交 actual source；actual target source 保持 `not triggered`。
没有新增 Lean theorem。完整 N45-S-NOU-LS-PAIR 父身份、其他 split22／非 split22、
一般多旁支／其他三环形状、R31、ε≥3、一般 N45／N2／E 及 K∞=K≤5 均保持 OPEN。
**新增完整 OPEN 身份的无条件关闭数 = 0。**

[READS](READS.json) 保存实际文档读取 argv、stdout／stderr 和 exit codes；
最初误查 `docs/c5`（不存在）的 exit2／stderr 保留为 read-04，后续改用实际 docs 路径，
其余文档读取及 primary fetch 成功。本 finding 不涉及证明或历史输入。

