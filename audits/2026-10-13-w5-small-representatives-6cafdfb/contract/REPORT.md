# W5 最弱保存契約、可執行的嚴格縮小與普遍量詞界線

2026-10-13。父包 frozen BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`。
本報告只使用父包凍結入口與既有 K15 前提；新證書在本目錄，沒有改動舊證據。

**最弱精確契約是補中心後的完整 B 關係 Σ 相等。保完整 B/U 三色 support
R³ 是較強充分條件，染色數、fibre 重數及私人 assignment 的可逆性都不是義務。
下面給出所有私人點數 m≥1 的合法 `m→0` 代表族；m=10 的控制是補中心後
`16→6`，Σ 相等而 R³ 不等。這是一般環帶的構造族，不排除真正最小來源。**

## 1. 幾何及介面先於關係

色集固定 C={0,1,2,3}。B=(b0,…,b4)、U=(u0,…,u4) 是十個互異的具名原 pins，
各誘導有序 C5。A、A′ 是有限簡單、連通的 plane annulus 圖，B 為指定外面、
U 為指定空內面。两圈的次序、方向、内外侧与槽位已共同对齐。所有其余顶点、
边和面都在两圈之间；每份图的原边、定向面、rotation 与 ownership 须明确，
没有隐藏界面接点。把 annulus 换掉时只保留这十个 pin 的身份与两圈的边；
被替换的环带内部边允许改变，来源自身的证据仍保留全部原边。

在各自 U 空面加入同名中心 v，恰加五条 vu_i，得 G、G′；v 没有其他禁色或
邻点。环带以外可有的其他图只沿 B 接入。本节的最弱目标若用于沿 U 或 v
另加限制的环境，必须把那些 pins 纳入实际界面，不能沿用仅 B 的目标。

合法代表须保以上几何和界面，还须满足选定的语义关系。仅有抽象平面性、
顶点数变小、边数变小、或一种染色的存在，都不足以作为合法替换证据。

## 2. 最弱契約與較強充分條件

对每个 literal proper B tuple β 与每个 literal U tuple τ 定义

\[
J_A(\beta,\tau)=\{\eta:\eta\text{ 是 A 的完整 proper 四色染色},
 \eta|_B=\beta,\ \eta|_U=\tau\},
\quad
R_A^3=\{(\beta,\tau):J_A(\beta,\tau)\ne\varnothing,
 |\operatorname{im}\tau|=3\}.
\]

全部 1,024 個 U tuples 必須留下其完整 fibres，包括不 proper 与其他空 cells。
采用十个正规 B 行时，仅可把同一次 S4 换色作用在整份 lift；不能独立正规化 U。

U 是奇五圈，所以每份能补中心的 annulus 染色在 U 恰用三色，中心取唯一缺色。
反之每份三色 U lift 都能这样补中心。因此對每個原 β 有 literal 全染色分解

\[
\mathcal C_G(\beta)\cong
\bigsqcup_{\tau:\,|\operatorname{im}\tau|=3}J_A(\beta,\tau),
\qquad \Sigma(G)=\operatorname{pr}_B R_A^3.                 \tag{1}
\]

于是以下条件等价：

1. Σ(G)=Σ(G′)，保同一原 B 色框的完整接受／拒绝关系。
2. 对每个 β，存在 source/target 完整 capped lifts 的双向 total 对照，逐个保 B
   pin 的颜色；U、v 与私人点的颜色可以改变。
3. 对每个 β，source 有某个三色 U full lift，当且仅当 target 有某个三色 U full
   lift。两侧可以使用不同 τ。

证明：由 (1)，条件 1 与 3 正是同一存在命题。条件 2 的 total 性给出双向非空。
条件 1 下在每个非空行选择一份完整目标 lift，就得到两向函数；空行是空函数。
它们不要求互逆、单射或满射。任何沿 B 接入的外部图也可搬运完整染色：保留外部
lift，使用同一 β 的目标内部 lift，接合边因只沿 B 接口而仍 proper。

若要求搬运额外保每个 U pin 的颜色，精确条件升为 R_A³=R_A′³：每个非空
(β,τ) cell 两侧选一份完整 lift 可给两向函数，中心色因 τ 的唯一缺色而自动相同。
这仍不要求任一 cell 的 fibre 数量相同。一般四色 U support 更强，cap 不使用
其四色 U cells；逐份内部全染色双射又更强，均非本目标的必要条件。

## 3. 通用且可验的局部充分操作

**私人低度点删除。** 若 x 不属于 B∪U，degree_A(x)≤3，而且 A−x 仍是上节
的合法 annulus，则删除 x 保完整 unrestricted B/U 四色 support，故保 R³ 与 Σ。
任意 A lift 限制成 A−x lift；反向先保整个 A−x lift，x 至多看见三色，在四个
颜色中选一个未出现者即可。它可能有多个选择，因此不能宣称计数相等。x 不是
cut vertex 是足够的连通性保证；私人 cut vertex 连着两圈时不能忽略删除后的
几何合法性。本操作不适用于内点 degree≥5 的真正全域最小来源。

**完整介面 patch 替換。** 将 A 写成 E∪H，交集是完整列出的具名界面 T，且
H 的内部点没有遗漏的外接边。若 H、H′ 能在同一实际面内合法嵌入，逐个保 T
及其外接 slots，且全部四色情形的 support

\[
S_H(T)=\{\alpha\in C^T: \alpha\text{ 有 H 的完整 lift}\}
\]

与 S_H′(T) 相等，则 E∪H 与 E∪H′ 的完整 B/U support 相等。证明是在每份 E
lift 使用它同一完整 T assignment 的目标 H′ lift，反向同理。T 的单点、双点
marginals 或分别可行的碎片不能替代完整 T support。若私人数减少就是合法严
格缩小；保四色 T support 是可复用充分条件，不声称它是 cap 专用最弱条件。

**私人合并的精确义务。** 若 x,y 是两个不同且不相邻的私人点，可在实际环带
面内画边并收缩成一个私人点（删去新增收缩 loop 与平行重复边），且所得嵌入
仍满足两圈的全部合法条件，则商图的 lifts 正是原图中 x=y 的 lifts。因此：对
每个 β∈Σ(G) 只须证明原图存在一份完整 capped lift 使 x=y，就能保 Σ 并少一点。
若对每个 (β,τ)∈R³ 有这样的完整 lift，才保 R³。可取的 x,y 及共同面须在来源
中实际给出；把 adjacent edge 随意收缩、只证明个别 β、或把不同时刻的可行
片段合起来，都不建立此义务。本节未宣称在任意最小来源总可找到这样的点对。

## 4. 一个新的合法 `r=m→r′=0` 弱保存族

以 B/U 的 literal pins 定义 prism P：除两条 C5 的十边以外，恰加五条 b_i u_i。
定向面为

```
(b0,b4,b3,b2,b1)                               outer
(b_i,b_(i+1),u_(i+1),u_i), i=0,…,4            annulus quadrilaterals
(u0,u1,u2,u3,u4)                               empty inner face
```

下标模五。每条 directed edge 恰出现一次，V−E+F=10−15+7=2；每个 vertex
link 单圈。两圈 induced，所有交叉连边在显式四边形中，P 是合法 r=0 annulus。

目标 T 为每个该四边形加入对角边 b_i u_(i+1)，分成两面
(b_i,b_(i+1),u_(i+1)) 与 (b_i,u_(i+1),u_i)。因此 V−E+F=10−20+12=2；
完整 rotation 检查也通过。T 仍 r′=0，中心补回后内点为六。

来源 A_m（任意整数 m≥1）：在 P 的四边形 (b0,b1,u1,u0) 内插私人 x1，恰接
b0,b1,u1，产生三面 (b0,b1,x1)、(b1,u1,x1)、(u1,u0,b0,x1)。再在三角面
(b0,b1,x1) 中插入 x2，此后每次在 (b0,b1,x_j) 内插入 x_(j+1)，恰接该面
三点。每次是真实面内操作，保持指定 B/U 面、边与身份，故每个 A_m 合法。

任何 P 的完整 lift 都可延伸到 A_m：x1 的邻点至多用三色，至少可选一种；此后
每个三角面的三个颜色不同，新点恰取其唯一缺色。限制回 P 给反方向。故全部 m
都满足 R_A_m³=R_P³，甚至 unrestricted B/U support 相等；这个结论来自任意
长度的构造证明，不来自把 m=10 的有限检查外推。

T 补中心后接受十个完整 B 行，以下逐行 literal τ 见证均满足所有 target 边、
U 恰三色及中心五条边：

| β | τ | v 色 |
|---|---|---|
| 01012 | 12323 | 0 |
| 01021 | 23213 | 0 |
| 01023 | 23230 | 1 |
| 01201 | 32032 | 1 |
| 01202 | 12313 | 0 |
| 01203 | 12012 | 3 |
| 01212 | 13030 | 2 |
| 01213 | 13030 | 2 |
| 01231 | 32302 | 1 |
| 01232 | 12010 | 3 |

每个 proper 四色 C5 tuple 经一次共同 S4 换色恰正规化为表中的一行，所以表
覆盖全部 240 个 literal β。T 增加的边使其 R³ 包含于 P 的 R³，表已证明 T 的
projection 包含全部合法 β，因此 P 与每个 A_m 的 projection 也包含全部。
得到严格缩小及完整关系定理

\[
\boxed{\ \Sigma(A_m+v)=\Sigma(T+v)=1023,
\quad r=m\longrightarrow r′=0,
\quad k=6+m\longrightarrow k′=6.\ }                 \tag{2}
\]

這是单一普通图 T 的代表，不使用多分支聯集、额外禁色或识别 B/U pins。
保每个 B pin 的双向 total full-lift maps 在证书中逐份存下：给每个 source lift
同一行 target 的 lex 最小 lift，反向取同一行 source 的 lex 最小 lift。

**R³ 确实不同。** β=01012、τ=10103 是 P 的 supported 三色 U cell，也支持
每个 A_m；但 b0=u1=0，T 新边 b0u1 拒绝它。因此 (2) 只保所需的完整 Σ，
不能提升成 R³ 保存。该 cell 的 P fibre 有一份 lift，A_m fibre 有两份（x1 可
取 2 或 3，其余插入唯一延伸），也展示 R³ 相同并不要求计数相同。

**适用界线。** 此族来源存在可移除 degree-three 私人点；从 m≥2 起有 occupied
triangles。它不触发最小目錄外来源的 degree≥5／无 occupied 小圈前提。
它给出任意大的实际可缩小来源和显式 r′≤9 代表，不能供给任意来源的九点
存在定理，更不能排除私人圈秩至少五的所有真正最小来源。

## 5. 普遍九点代表的强度：与主命题的条件等价

以下使用已接受的 FCT、最小来源 chordless 正规形、K15=K5=K132，以及每份
K132 关系的 ≤5 内点 witness；这些是上游依赖，本包未重证 FCT 或目录完备性。

令 P9 是「每个本契约的合法 annulus A 都有一个合法同槽位 annulus A′，r′≤9，
且 Σ(A+v)=Σ(A′+v)」。P9 会给出任意大小的主命题 K∞=K132。

证明：若目錄外 disk 来源存在，取全域最小来源 H；已接受正规形给 induced 原
B。在 H 的任一内面内放入一个新的 W5，U 的五点与 H 互异，另加唯一桥 t u0，
t 是该面的一个旧点。每份 H lift 都能延伸：若 t 色 c，以模四写
U=(c+1,c,c+1,c,c+2)、v=c+3，满足新桥和整份 W5；限制也给反向。
故新图 G 有 Σ(G)=Σ(H)，删中心就是合法 annulus（桥导致 repeated facial
walk 是合法的）。由 P9 有 ≤15 内点的 equal-Σ capped disk，由 K15 其关系
属于 K132，与 H 目錄外矛盾。

反向也成立，且可给更强的私人五点界。假设 K∞=K132。任取 A 的 capped G。
取同一完整 Σ 的 ≤5 内点目录 witness H。必须先核对 H 的 B 是否 induced，
不能默许目录本身没有 B chords；凍結 edge_universe 实际包含它们。所需核对
由以下一般 lemma 自动成立。

**Cofacial 非边 lemma。** 若 finite planar 图 X 的同一面上两个点 a,b 不相邻，
可在该面画一条新边并收缩，删去该新增边的 contraction loop 与平行重复边。
因没有原 ab 边，不会产生原边 loop；商图仍平面且可按 FCT 四色。其完整 lift
拉回 X 就给 a=b。因此 induced B 的每个非相邻 pair，都在某一份完整 X lift
中同色。共同 S4 正规化保这份 equality 和它同一完整 B row。

把 lemma 用于 G 的 actual 外面：若 equal-Σ witness H 有 chord b_i b_j，H 会
拒绝上述同色 row，G 却接受，违反完整 Σ 相等。因此 H 不含任何 B chord。
在 H 的一个内面插入上述自由 W5 和桥，保持 induced B，得到 Σ 相等的合法
annulus A′，其私人点恰为 H 的 ≤5 内点。U 的名字、次序与内外侧可在插入时
逐个按原槽位匹配。故

\[
K_\infty=K132\quad\Longrightarrow\quad P5\quad\Longrightarrow\quad P9,
\qquad P9\quad\Longrightarrow\quad K_\infty=K132.       \tag{3}
\]

这里 P5/P9 仅要求本报告的最弱完整 Σ；不要求 R³，也不要求代表是 near-
triangulation、edge-critical、degree≥5 或同数染色。式 (3) 說明一般九点存在
不能由既有 K15 界加计数直接得到：它已具有主命题的普遍强度。针对一个受限
来源族的构造、单份有证据的严格缩小、或额外有明确源关系的代表不等同 P9。

## 6. 新控制與重播

```
python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/contract/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/contract/check.py --check
```

控制图为 P、T、A10 及各自实际补中心图，存六份完整 10×1024 fibre 表，共
61,440 cells，空格完整保留。DFS 与独立 pins＋显式 owned insertions 枚举逐份
full lift 字串相等；cap 又以独立 DFS 与「三色 U 唯一缺色」规则逐格比对。
全部 original faces/rotations/ownership 已存，指定中心只接五个 U 的证据也核对。
normal 与 seed17 都通过；复制证书删掉一份 A10 capped full lift 的负控制被
checker 以 AssertionError 拒绝。结果保存于 `verification.json`，临时破损副本已清除。

| 图 | r | capped 内点 | 非空 R³ cells | annulus full lifts | capped full lifts | Σ |
|---|---:|---:|---:|---:|---:|---:|
| P | 0 | 6 | 340 | 670 | 340 | 1023 |
| T | 0 | 6 | 20 | 50 | 20 | 1023 |
| A10 | 10 | 16 | 340 | 950 | 485 | 1023 |

这些数量为十个 canonical B 行；literal 240 行由统一 S4 色作用涵盖，未把来源
和代表分别归一化。纸面结论为任意 m≥1 的族，有限控制状态为 `triggered and
holds`；R³ 保存及计数保存的更强目标状态为 `counterexample`。真正最小来源
为 `not triggered`，一般 r′≤9 为 `OPEN`，没有新增 Lean theorem。
