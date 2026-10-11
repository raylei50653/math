# BR-SD-1c：一份原旁支與 pair-support 的局部 palette 排除

2026-10-11，BASE `fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。
這是新 audit 的任意大小紙面結果，canonical 採納另行裁決。
外部數學依賴為 [Dvořák 作者講義 Theorem 10／blockwise-uniform 定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)；
版本、原頁核查與 hash 見 [SOURCE](external/SOURCE.md)。

## 1. 精確原來源域

保留 BASE 的 N45§1、§2.11 BR-SD-1a 合同1–3及5：有限簡單 ordered induced-C5 disk
原 G、完整 Σ933／941 或共同整圖 D5 像、ε=2、逐非框邊 Σ-critical 原 witnesses；
原非相鄰 degree5 roots r/s，其餘有效原內點完整 degree4；
`H_G−{r,s}=L⊔S`，無原 unary U，L long，S actual support 恰真框邊兩端。
exact-S 只省略 r 的唯一原 spoke e，`X=M=G−e` 自身拒絕同一 proper 三色 β、
自身同 β inclusion-minimal，保全部原 retained-edge witnesses。
M 唯一 degree5 內點是 s，其餘有效內點完整 degree4；
s 恰有不同原有序內鄰 p∈L、q∈S，三原 B-spokes 全留。
同一 `C=H_M−s={r}∪L∪S` 是實際 sole connected component。

取 BR-SD-1a 合同4的原骨架：三個任意奇長≥3的原 cycle blocks J1/J2/J3；
J1∩J2={r}，J3 與兩者不交；J2 私有 u≠r 與 J3 私有 v 的唯一原環間 bridge uv；
原 p/q 外臂分別從 J1/J3 私有錨點 a1/a3 通到 p/q，各為任意非負長的 simple bridge path。
不假定 a3≠v。

唯一放寬是允許一份非空的**原** pendant branch W：
其內點與骨架互斥，W 連通，`N_C(W)={x}`，x∈J1∪J2；
沒有其他新增接入骨架的位置、cross edge 或 s-contact。
W 若在 J1 側，屬完整原 L；若在 J2 側，屬完整原 S，並繼承該 piece 全部原附件合同。
W∪{x} 的 blocks、內點、實際 B 附件、rotation 都由候選原 G 指定；
不預先構造、重接或認定一張抽象 Gallai tree 是 disk 來源。
若拒絕成立，外部定理本身迫 W 所屬的 C-blocks 為 Gallai blocks。

所有 named/ordered/shared contacts、ownership、原邊、actual attachments/supports、rotation、
同一 literal β／四色集 Col、完整 relations／fibres（含空 fibres）及 full lifts 均保留。
這是對上述假想原來源的全稱反證；沒有提交滿足合同的 actual source。

## 2. 先核原 degree 與來源身份

令 m=|N_C(x)∩W|≥1，k(x)=|N_B^M(x)|，t(x)=1[sx∈E(M)]。
所有數據從該原來源取，不能為接入 W 移除既有附件。完整度4要求

`d_骨架(x)+m+k(x)+t(x)=4`。

| 原接點 x | 原骨架 d_C／s-contact | 必要局部限制 |
| --- | --- | --- |
| r | 4／0 | m≥1 已超度；結構排除，不進 palette 路線 |
| a1 | 正臂時3／0，零臂時2／1 | m≤1；非空時第一 incident W-block 只能是 bridge，且 k=0 |
| u | 3／0 | m≤1；非空時第一 W-block 只能是 bridge，且 k=0 |
| 其他 J1/J2 私有點 | 2／0 | m≤2；若拒絕，首 block 可為 bridge 或 odd cycle，不能為 K4 |

在 ordinary 私有點 m=1 時 k=1，m=2 時 k=0；任意 W 其他點各有
`d_C(y)+|N_B^M(y)|=4`。以上都是必要条件，並不證 actual attachment 或 disk 可實現。
W 不改 r 的 split22 或原 p/q；刪 r/s 後 W 留在其 owner L/S 內，不成為原 unary U。
詳細逐項對照見 [MAPPING](MAPPING.md)。

## 3. 同一原 M 給 degree lists 與不可著色

對每個原點 y∈C 定義

\[
L^D(y)=Col\setminus\bigl(\beta(N_B^M(y))\cup
(\{D\}\text{ if }sy\in E(M)\text{ else }\varnothing)\bigr),
\]

其中 D 是同一 β 未用的第四色。原 M 的完整 degree4 及 sole C 給

\[
4=d_C(y)+k(y)+t(y),\qquad |L^D(y)|\ge4-k(y)-t(y)=d_C(y).
\]

不先假定 β 在不同附件上異色或 lists 全緊。D 未在 β 出現，s=D 與全部原 s–B 邊相容。
若 C 有完整 L^D-coloring f，`β∪{s↦D}∪f` 覆蓋 M 全部原點，逐類滿足
B–B、B–C、s–B、s–C、C–C 全部原邊，包含 W 邊和 W 的原附件。
若 effective-H 慣例另忽略原孤立自由內點，它們沿同一原 M 的自由因子填入任意 Col 色，
保留全部 full-lift 坐標。
這與 M 自身拒絕 β 矛盾。因此 C 不可 L^D-著色。
這是完整原 assignment 接合，不使用 marginals、不替換 pieces 或獨立正規化色框。

依 Theorem 10，存在 C 各 block K 的 palettes P_K，使

\[
L^D(y)=\bigcup_{K\ni y}P_K,
\quad K\cap K'\ne\varnothing\Longrightarrow P_K\cap P_{K'}=\varnothing.
\]

奇環 palette 大小2，bridge palette 大小1；triangle 作 clique 也給2。
尤其每個 incident block 的 palette 都包含於該點 list，但 cutpoint list 不等於每個 incident palette。

## 4. 路線 A：private witnesses 精確保留範圍

W 不接入的環沿用原選點；接入 J_i 時，再排除 x：

`w1∈J1−{r,a1,x}`，`w2∈J2−{r,u,x}`，其中 x 只在實際接入的環排除。

非接入環至多排除兩點，必有 witness。接入環長≥5 時至多排除三點，仍有 witness；
triangle 若 x 等於原已排除的 a1 或 u，也仍有 witness。
每個所選點只屬自己的 cycle block，非 C 割點、非 s-contact，d_C=2、k=2，
故 D∈L^D(w_i)=P_Ji。J1/J2 在 r 相交要求 palettes 互斥，矛盾。

唯一可能失去這條選點證明的情況，是接入環為 triangle，x 為與 r/a1 或 r/u
都不同的第三點。不能把這時的 D∈L^D(x) 升成 D∈P_Ji。

## 5. 路線 B1：J2 witness 失去後的合法 D-routing

若 W 接在 J2 triangle 的唯一 witness x，則 u 沒有 W 接入。
未受 W 影響的 J3 有 `w3∈J3−{v,a3}`，它非割點、非 s-contact，因此 D∈P_J3。
原 bridge uv 的 singleton palette 不含 D，否則在 v 與 P_J3 相交。
u 非 s-contact，且只 incident J2 與 uv；所以

`D∈L^D(u)=P_J2 ⊔ P_uv`，迫 D∈P_J2。

J1 原 witness 未受影響，D∈P_J1，仍在 r 矛盾。若 W 接 u，J2 原 witness本就保留。
這條 routing 完整記錄所有 incident blocks，沒有將 D 分給全部 palettes。

## 6. 路線 B2：保 actual pair support 的局部末端引理

J1 triangle 的唯一 witness x 被 W 佔用時，抽象 D-routing 可失敗；見§7。
原來源還保有 S 的實際真框邊支援，足以給另一條任意大小的局部矛盾，
且它同時涵蓋前面所有未因 degree 排除的 W 接點。

設 S 的實際支援是 `{b_i,b_{i+1}}`。這是原鄰點集合 `N_B^G(S)`，
不是顏色 marginal 或盾弧名稱。exact-S 只删 r-spoke，故每個原 y∈S 仍有

`N_B^M(y)⊆{b_i,b_{i+1}}`。

令 A=β(b_i)、B'=β(b_{i+1})；proper β 與真框邊給 A≠B'。
以 T 記 β 的第三個已用色，因此 `Col={A,B',T,D}`。這只是同一字面色框的名稱，沒有另作色置換。

**局部引理。** 在§3的 degree-list／拒絕前提下，若一個原奇環 J 與原 q 外臂的
全部 B 附件都位於這兩個異色原框點，J 的其他接入至多在 v、a，
q 是該側唯一 s-contact，外臂各邊都是 C 的 bridges，且 a 以外的每個外臂點
在 C 只有該原路徑的鄰居（正長時 q 的 d_C=1、內部臂點 d_C=2），則這份末端配置不可能。
其他 C-blocks 可有旁支；它們不能接到 J 或該外臂的其他點。

**證明。** 本輪套用 J=J3、a=a3。
選原 `w3∈J3−{v,a3}`。奇環至少三點，排除至多兩點，任意環長均存在；a3=v 時仍成立。
W 只接 J1/J2，故 w3 只屬 J3、非 s-contact，原 C 內鄰恰兩個 cycle 鄰點。
完整 degree4 迫 k(w3)=2；simple graph 與原支援限制迫附件**恰為**那兩個框點。
因此

\[
L^D(w3)=\{T,D\},\qquad P_{J3}=\{T,D\}.
\]

分原 q 外臂的**原邊數** ℓ：

1. **ℓ=0。** q=a3，原 sq 邊在 L^D(q) 禁 D。P_J3 是 q 的 incident palette，
   必含於 L^D(q)，卻含 D，矛盾。a3=v 只增加另一個 incident block，不能消除此包含關係。
2. **ℓ=1。** 唯一外臂原 bridge a3q 的 q 端，d_C(q)=1、t(q)=1；
   完整 degree4 迫 k(q)=2，兩附件恰為原 pair，故 L^D(q)={T}。
   該 bridge 的非空 singleton palette 等於 {T}，與 P_J3 在 a3 不互斥，矛盾。
3. **ℓ≥2。** 以 z 命名原外臂中緊鄰 a3 的第一個原點；z≠q，非 s-contact，
   原 C-degree2（兩條臂邊），完整 degree4 迫其兩 B 附件恰為原 pair。
   故 L^D(z)={T,D}。第一原 bridge a3z 的非空 singleton palette
   包含於 L^D(z)={T,D}=P_J3，與 J3 在 a3 相交又須互斥，矛盾。

三類涵蓋任意非負 ℓ；不需縮臂、枚舉 parity 或把 D 傳入 J1。
此證明只使用原 J3 私有點及原外臂的首點／末端，保留任意大小 W、J1/J2/J3 及 p 外臂。
局部引理已完成證明；它在本 audit 的應用仍只聲稱上述精確 one-W 來源域。

## 7. 無 pair-support 時第一個失敗推論

在 J1=(r,a1,x)、p=a1、W 為原形狀的 bridge xy 時，僅從 D∈L^D(x)
不能得到 D∈P_J1。以下明列 abstract palettes 即可反駁該推論：

`P_J1={A,B}, P_J2={C,D}, P_xy={D}, P_uv={A}, P_J3={B,D}, P_tq={A}`，

其中 J2=(r,u,w)、J3=(v,z,t)，q 的正長1外臂為 tq。
所有相交 palettes 互斥；非 s-contact lists 全含 D，而 contacts a1/q lists 不含 D；
x 的 list={A,B,D}，D 完全屬於 xy palette。
因此這是對「cutpoint 有 D ⇒ 本環 palette 有 D」的 **counterexample**。
具名全邊、實際 synthetic 附件、原列表與完整 fibres 見 [controls](agents/controls/REPORT.v2.md)。

其 synthetic M 的 S 框附件實際使用三個框點，違反本輪 actual pair-support；
未提供 disk embedding、完整 Σ 或逐來源合同。因此它不是本輪 scoped exclusion 的反例，
也不把抽象 list 相容性升格 actual disk source。
若另研究失去 pair support／J3 或 q-arm 也有旁支的合同，§6不適用；
須另證 palette routing 或原 attachment／embedding 排除，不能從本輪結果直接推廣。

## 8. 結論與停止點

指定 `N45-S-NOU-LS-PAIR` split22 原骨架多一份接在 J1/J2 的原 pendant W，
若保全部上述原來源合同，則不可能存在。r 接入已由完整 degree 排除；
其餘接點由 degree-list／Gallai 刻畫及未受影響的 actual pair-supported J3 末端排除，
任意環長、任意原外臂長及任意有限 W 大小均包含。

這提供可重用的 **pair-supported 奇環／唯一 s-contact 外臂局部排除引理**，
及 witness／J2 routing 的獨立機制。泛用 cutpoint D 傳遞本身仍是假推論。
沒有實際 target source 或新 Lean theorem；有限 fixtures 只校準這些機制。
不依 SD-A、H_M 二連通、R27 minor、T4 定位或四-query 變換；
原 Σ/minimality/embedding 等完整身份仍保留，但不是這段短證明的使用依賴。
canonical 採納、父身份 closure、一般三環／Gallai trees／非二連通圖、R31、55、ε≥3、
一般 N45／N2／E、一般出口及主命題均不由本 audit 宣稱完成。
