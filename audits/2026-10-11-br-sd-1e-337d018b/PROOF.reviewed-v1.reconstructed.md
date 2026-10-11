# BR-SD-1e：J3／q 外臂單一原旁支的 private-witness 保持與來源排除

2026-10-11；研究 BASE `337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`。
本檔證明下面完整原來源合同不能同時成立，狀態為 **candidate scoped exclusion**。
canonical 採納由 owner 另行批准。原 BR-SD-1a／1c 封存及 canonical 全部唯讀。
來源／度數逐項對照見 [MAPPING](MAPPING.md)，外部版本見 [SOURCE](external/SOURCE.md)。

## 1. 完整原來源合同與量詞

保留 BASE [N45§1、§2.11、§3](../../docs/c5_excess_two_nonadjacent_unit_core45.md)
及已採 BR-SD-1a 的原 G、同一 β、原 M 身份：

1. G 是任意大小有限簡單 ordered induced-C5 disk，原框 `B=(b0,…,b4)` 為外邊界。
   完整有序 `Σ(G)=933／941` 或整張具名圖共同搬運的 D5 像，`ε(G)=2`；
   各非框原邊 Σ-critical，保每邊自己的完整刪邊 witnesses。
   非相鄰原 degree5 roots r/s，其餘有效原內點完整 degree4。
2. 原 `H_G−{r,s}=L⊔S` 恰兩份完整 mixed，原 U=0，L long，
   S 的 raw actual support 恰同一真原框邊兩端 `T_B={b_i,b_(i+1)}`。
   保原 full B-touch、one-sided、support 非空等 N45 來源條件。
3. exact-S 只省略 r 唯一原 boundary spoke `e=rb_j`；`X=M=G−e`，原點全部保留。
   M 自身拒絕同一 literal proper 三色框列 β，且自身對 β inclusion-minimal，
   保自己的全部 retained 非框邊同 β witnesses；不由 G 的 Σ-critical 自動推此條件。
   M 唯一完整 degree5 有效內點是 s，其餘有效內點完整 degree4。
4. s 恰有原有序相異內鄰 `p∈L`、`q∈S`，三條原 boundary spokes 全留。
   `C=H_M−s={r}∪L∪S` 是同一實際 sole connected component；r split22，
   原四條 C 邊向 L/S 各兩條，M 中 r 無 B-spoke。
5. 令 C0 為同一原 C 的具名骨架邊子圖：三個任意奇長≥3的原 cycle blocks J1/J2/J3，
   `J1∩J2={r}`，J3 與兩者互斥；J2 私有 `u≠r` 與 J3 私有 v 間恰原環間 bridge uv。
   原 p/q 外臂是從 J1/J3 私有錨點 a1/a3 到 p/q 的 simple bridge paths，
   長度各任意非負整數；零長時 `p=a1`／`q=a3`。允許 `a3=v`。
   除下面唯一 W 外，無其他 blocks、旁支、cross edges 或額外骨架接線。
6. 本轮唯一形狀放寬是一份有限非空的原 off-skeleton 頂點集 W，`C[W]` 連通，
   `V(C)=V(C0)⊔W`，`N_C(W)={x}`，具名 `x∈V(J3)∪V(q-arm)`；
   W 屬同一原 S，`N_B^M(W)⊆T_B`，無任何 W–s 邊或 J1／J2 接線。
   在同一原 C 中，W 的內邊及 x–W 邊全部由候選原來源指定；可有多條 x–W 邊。
   W 的原頂點、邊、附件、ownership、rotation／disk 嵌入不能由抽象 list fixture 代替。
7. 全部 named/ordered/shared contacts、attachments/supports、ownership、rotation、bridges、
   原 G／M 各自的完整 relations／fibres（含空 fibres）／full lifts、同一 literal 四色集 Col
   與原框列均保留；45／54 只共同交换 roots roles 與全部資料。

C0 只是候選原來源內的一份骨架，不是一張已完整 degree4 的舊來源再被加邊。
「W 改接」在此描述來源家族的形狀，不是批准改動一張原 G 的邊或刪除既有附件。
以下對每個滿足全部合同的假想原來源作反證；未提供 actual target disk source。

## 2. 先核全部接點的原 degree 與 support

定義原 `k(y)=|N_B^M(y)|`、`t(y)=1[sy∈E(M)]`，原完整度數給每個 `y∈C`

\[
4=d_M(y)=d_C(y)+k(y)+t(y).
\]

在 x，令 `m=|N_C(x)∩W|≥1`，`d0=d_(C0)(x)`，因此

\[
k(x)=4-d0(x)-m-t(x).
\]

q 外臂記為 `a3=z0,z1,…,zℓ=q`（ℓ=0 時同點）。下表互斥且窮盡允許 x；
其中 ordinary J3 點指排除 v/a3，其餘臂內點指 `z1,…,z_(ℓ−1)`。

| 原接點 x | 原條件 | d0 | t | 非空 W 的必要預算 |
| --- | --- | ---: | ---: | --- |
| a3=v | ℓ=0，亦即 q=a3=v | 3 | 1 | **任何 m≥1 超度，結構排除** |
| a3=v | ℓ>0 | 4 | 0 | **任何 m≥1 超度，結構排除** |
| v≠a3 | 任意 ℓ | 3 | 0 | m=1、k=0 |
| a3≠v | ℓ=0，q=a3 | 2 | 1 | m=1、k=0 |
| a3≠v | ℓ>0 | 3 | 0 | m=1、k=0 |
| ordinary J3 點 | 任意 ℓ | 2 | 0 | m=1、k=1，或 m=2、k=0 |
| q（off-cycle） | ℓ>0 | 1 | 1 | m=1、k=1，或 m=2、k=0 |
| q-arm 內點 | ℓ≥2 | 2 | 0 | m=1、k=1，或 m=2、k=0 |

每個 k 是**候選原來源已有的實際附件數**，不能為容納 m 移除附件。
若原附件已使 `d0+k+t=4`，不論是哪一列，非空 W 都直接結構排除。
表內其餘情況僅為必要容量，並不證明 actual disk、Σ、minimality 或拒絕可實現。
對所有 W 點 y，`t(y)=0` 且原 S support 給 `k(y)≤2`，所以 `2≤d_C(y)≤4`；
具有 C-degree1 的旁支葉不能滿足本合同。W 的其他每個原點仍須逐點滿足完整度4。

只刪 r–B 原 spoke，故 `N_B^M(S)=N_B^G(S)=T_B`；所有 W 附件均須位於此 pair，
原已有兩端支援均保留，support 不因添原旁支而擴大。原 r/s degrees 分別為 G 的5/5、M 的4/5；
p/q、s 的三 spokes、r split22 均未改動。W 刪 r/s 後仍與 S 的 x 相連，不成為新的原 U。

## 3. 可重用 private-witness preservation lemma

**引理（單接點旁支保持）。** C0 是§1具名三環單 bridge／兩外臂骨架；
原 J1/J2 為簡單奇環，共用 r，其他 block 接入在 J1 僅 r/a1、在 J2 僅 r/u。
向 C0 接入一份有限非空 off-skeleton 連通原 W，唯一骨架鄰點 x 在 J3／q 外臂，
除此之外保全部原骨架邊，無 cross edge、額外 s-contact 或 J1/J2 新接線。
则每个原

\[
w_1\in V(J_1)\setminus\{r,a_1\},\qquad
w_2\in V(J_2)\setminus\{r,u\}
\]

仍只屬自己的原 cycle block，非 C 割點，非 s-contact，`d_C(w1)=d_C(w2)=2`。
這兩集合均非空，包括 J1/J2 为 triangle 的情形。

**證明。** 每環至少三點，排除至多兩個不同點，故各至少留一原點。
由锚點「私有」身份，`a1≠r`、`u≠r`，J3／q 臂完全位於 J1/J2 之外，故 `x≠w_i`。
原 p 在正長臂时不在 J1，零長時等於被排除的 a1；q 在 J3／q 外臂，兩者均不等於 w_i。
W 無 s-contact，原 s 的 contacts 恰 p/q，故 w_i 仍非 s-contact。

任何穿過 W、從骨架離開又返回的路徑只能在 x 進出。因而一個同時包含
W 點與 `C0−x` 點的子圖在刪 x 後分離，不能成為跨兩側的二連通 block。
每個 C-block 都在 C0 或 `C[W∪{x}]` 一側；單接點旁支不能合併原 blocks。
原 uv 與兩外臂邊仍是 C bridges，也不能被 W 生成的新 cycle 繞過。
此結論允許 m>1；多條 x–W 邊可以生成 W 側的 block，但其與骨架仍只共用 x。

原 J1 在 r／正長臂 a1 以外無其他 block 接入；J2 在 r/u 以外亦無。
删除 w_i 後，原環剩下一條連通路，包含全部原骨架接入點；其他骨架仍連通，
W 在另一原點 x 接入。因此 `C−w_i` 連通，w_i 非割點且只屬原 J_i 一个 block。
沒有新增邊 incident w_i，所以其全部 C 鄰居仍恰兩個相異原環鄰點，內度2。證畢。

引理的必要限制是：W 不得在 J1/J2 私有 witness 接入、不得有第二骨架接入點、
不得新增跨接線或 s-contact，也不得修改原 cycle/bridge 邊。
若旁支佔用 triangle 的唯一 private witness，該點可成為割點；若有第二接點，原 blocks 可合併。
這些撤前提情況不在本輪來源域，不能由此引理涵蓋。

在本輪完整原 M 的 degree4 下，引理再給全部原鄰居

\[
N_M(w_i)=\{\operatorname{prev}_{J_i}(w_i),\operatorname{next}_{J_i}(w_i)\}
\ \dot\cup\ N_B^M(w_i),\qquad |N_B^M(w_i)|=2.
\]

两份原 B 附件的色全在 β 的三色中，不含 β 未用的第四色 D；兩附件可同色，
不在這一步預設 lists 全緊。以下只需 `D∈L^D(w_i)`。

## 4. 同一原 M 的 degree lists 與完整延拓等價

固定同一 Col 中 β 未用的唯一色 D。對每個原 `y∈C` 定義

\[
L^D(y)=Col\setminus\left(\beta(N_B^M(y))\cup
\begin{cases}\{D\},&sy\in E(M),\\\varnothing,&sy\notin E(M).\end{cases}\right).
\]

因為所有原鄰居恰分成 C、B、以及可能的 s，原完整 degree4 給

\[
|L^D(y)|\ge 4-k(y)-t(y)=d_C(y).
\]

這是含 W 全部原內邊與原附件的 C-degree；不使用改接前的 q 末端度數。
同色 boundary 附件可能使不等號有 slack，外部定理容許 degree assignment 的 ≥ 前提。

完整 C 的 L^D-coloring f 與完整原 M 的 β 延拓且 `s=D` **等價**：
限制 M 延拓所得 f 必避開各原 B 鄰居色及相鄰 s 色，故屬原 lists；反向則
`β∪{s↦D}∪f` 覆蓋全部有效原點，逐類滿足原 B–B、B–C、s–B、s–C、C–C 邊。
B–B 由 proper β，s–B 因 D 未在 β 出現，其餘各類由原 lists 與完整 f 保證，
包含 x–W、W–W、W–B 全部原邊。
若 effective-H 忽略原自由孤立內點，合同中的那些無鄰居原點另外任意填 Col 色；
保其 full-lift 自由因子，不删除原坐標。

因此若 C 可著色便延拓同一 β 到同一 M，違反 M 自身拒絕；C 不可 L^D-coloring。
这里只固定 `s=D` 的完整 assignment，未混用省略 s–B 約束的其他 C 色查詢。
沒有縮臂、換 piece、逐分量色正規化，或由 marginals 代替完整原 assignment。

## 5. 外部 Gallai 刻畫與同一 D 的矛盾

外部依賴是 [Dvořák，*List coloring and Gallai trees*，Theorem 10 與同頁定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本輪實際核對作者 PDF／原頁，版本與 hash 見 [SOURCE](external/SOURCE.md)。
它適用於連通圖的 degree assignment，不要求本轮 C 二連通、planar 或先驗 lists 緊。

C 有限簡單且連通，§4給逐點 list 大小至少 C-degree 和不可著色；因此 C 是 Gallai tree，
并有各原 block K 的 palettes P_K 滿足

\[
L^D(y)=\bigcup_{K\ni y}P_K,\qquad
K\cap K'\ne\varnothing\Longrightarrow P_K\cap P_{K'}=\varnothing.
\]

奇環 palette 大小2，bridge 大小1；triangle 作 clique 時也給2。
W 的 blocks 若不是 Gallai blocks，已在這一步与不可著色矛盾；无需先分類 W。
§3保原 J1/J2 的 block 身份。w_i 各只屬 J_i，故

\[
L^D(w_1)=P_{J_1},\quad L^D(w_2)=P_{J_2},\quad
D\in P_{J_1}\cap P_{J_2}.
\]

但原 `J1∩J2={r}`，刻畫要求 `P_J1∩P_J2=∅`。矛盾。
整个論證只在兩個非割點以 list=單一 palette；沒有從割點 list 含 D 推每個 incident palette 含 D。

## 6. 覆蓋、信任邊界與停止點

对§2飽和接點先有結構排除；對其餘全部允許原 x、任意奇環長≥3、
原 p/q 臂長≥0及任意有限非空 W 大小，兩 private witnesses 均由§3保留，§4–5完成矛盾。
這證明§1完整合同的任意大小 **candidate scoped exclusion**。

W 接 q 或臂內點時，q／臂點的 C-degree 可增加；J3 witness 也可被 W 佔用。
BR-SD-1c terminal lemma 的必要前提因此不能普遍沿用。
這不是本輪 private-witness 路線的失敗：J1/J2 與兩個原 witnesses 仍未被碰觸。
无需 terminal lemma、SD-A、H_M 二連通、R27 minor、四-query變換或 W／J3 大小分類。

原 disk／完整 Σ／ε／G 邊 witnesses、M 自身 β-minimality／retained-edge witnesses、
S actual pair support、ownership／rotation 等仍在來源合同；證明只使用其中的
原 M degree4、同 β 拒絕、sole C、骨架 block separation、p/q-only contacts 與單接點形狀。
其餘強前提不被刪除，也沒有由 lists 推回 actual disk 實現。
有限固定 fixtures 只校準局部機制；actual target source 沒有提交、`not triggered`。
任意大小量詞由本紙面證明與獨立審查承擔，沒有新增 Lean theorem。

下一個最小數學 OPEN 義務可取兩份原旁支分別佔用 J1／J2 triangle 的唯一 private witnesses，
保全部原來源身份，逐點核 degree／support 與合法 palette routing；本輪未開始該題。
這只是具名後續候選，不把單旁支結果擴大至一般多旁支 Gallai trees。
完整 N45-S-NOU-LS-PAIR、其他 splits／形狀、其他45／54／55、ε≥3、R31、
一般 N45／N2／E、一般出口、主命題與 `K∞=K≤5` 均維持 OPEN。
