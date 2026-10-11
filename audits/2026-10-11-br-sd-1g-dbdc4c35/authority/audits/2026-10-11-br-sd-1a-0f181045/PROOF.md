# BR-SD-1a：同一原 M 的直接 D-palette 證明

本證明逐項保留 [BR-SD-1a 任務原文](authority/current/audits/2026-10-11-single-deficit-publication/NEXT-TASK.md)
及其引用的 [BR-SD-1 合同1–4](authority/current/audits/2026-10-11-single-deficit-applicability-804e3b0b1b/NEXT-TASK.md)。
它證明該合同的來源不可能存在；不是給出一張實際來源圖。
以下所有點、邊、框列與 lists 都屬同一原 M=X=G−e，e 是原 r 的唯一 boundary spoke。
原 G 的完整 Σ／逐邊 witnesses、原 M 自己的 β-minimality、完整附件、rotation、ownership
均留在原來源合同中；本短證明不使用其中的额外強條件。

## 1. 原點與圖形

B=(b0,…,b4) 是原有序框，H=M−B，C=H−s 是唯一實際分量。
每個 v∈C 的完整 M-degree 是4，s 的完整 M-degree 是5，原內鄰恰有序的不同點 p/q；
s 的三條原 boundary spokes 全留。β 是 M 拒絕的同一 proper 三色框列；
Col 是同一字面四色集，D 是 Col 中 β 唯一未使用的色。

C 的 blocks 恰為 J1/J2/J3 三個原奇環與合同中原 bridges。
J1∩J2={r}；J3 與 J1/J2 互斥；J2 私有 u 與 J3 私有 v 由唯一環間 bridge uv 相連，u≠r。
p/q 經兩條末端原外臂分別接到 J1/J3 私有錨點 a1/a3，臂可零長，無其他 blocks／旁支。
正長臂時 p 在 J1 外、q 在 J3 外；零長臂時 p=a1、q=a3。
不額外假定 a3≠v，也不以此圖形冒稱 H 已證二連通。

## 2. 原鄰居給 degree lists，拒絕給不可著色

對每一個原 v∈C，定義 t(v)=1 若原邊 sv∈E(M)，否則0，
N_B^M(v)=N_M(v)∩B，k(v)=|N_B^M(v)|。由完整原度數及 C 的唯一性，

$$4=d_M(v)=d_C(v)+k(v)+t(v).$$

原列表直接為

$$L^D(v)=Col\setminus\bigl(\{\beta(b):b\in N_B^M(v)\}\cup
(\{D\}\text{ if }t(v)=1\text{ else }\varnothing)\bigr).$$

不同原 boundary 鄰點可同 β 色，因此只取上界，而不先宣稱 lists 全緊：

$$|L^D(v)|\ge4-k(v)-t(v)=d_C(v).$$

D 未在 β 上出現，故 s=D 不違反任何原 s–B 邊。若 f 是 C 的完整 L^D-coloring，
則原 assignment β∪{s↦D}∪f 覆蓋 M 全部點，並逐類核原 B–B、B–C、s–B、s–C、C–C 邊。
這給同一 β 的 M 完整著色，與拒絕假設矛盾。因此 C 不可 L^D-著色。
這是完整 assignment 接合；沒有用端點 marginals、獨立色正規化或替換附件。

## 3. 任意環長與零／正長臂下的具名私有 witnesses

選原點

$$w_1\in V(J_1)\setminus\{r,a_1\},\qquad
w_2\in V(J_2)\setminus\{r,u\}.$$

每個簡單奇環至少三點，每個選取集合至多排除兩點，因此各至少有一點。
這個存在性對環長沒有上界；零長臂也包含在內。

J1 在 C 中的其他 blocks 只能在 r、以及正長臂的 a1 接入。
排除這兩點後，w1 只屬 J1 一個 C-block，故不是 C 割點。
若 p=a1，它被排除；若 p 不在 J1，它不會等於 w1。q 在另一末端／外臂，亦不等於 w1。
J2 的其他 C-blocks 只在 r/u 接入；p/q 都不在 J2 私有點。
因此 w2 只屬 J2 一個 block，亦不是 C 割點，且 w1/w2 都不是 s-contact。

兩點的全部原鄰居（保留符號參數，不偽造一張不存在的來源）恰為

$$N_M(w_i)=\{\operatorname{prev}_{J_i}(w_i),\operatorname{next}_{J_i}(w_i)\}
\ \dot\cup\ N_B^M(w_i),\qquad |N_B^M(w_i)|=2.$$

C 內的兩原環鄰點不同；沒有額外原 C 邊或 sv 原邊。
所以 d_C(w_i)=2，而 D 未被任何原 B 附件禁去，D∈L^D(w_i)。
若兩原 boundary 鄰居在 β 下同色，這個 list 有 slack；仍由 §2 的 degree assignment
與不可著色導出下面刻畫，不需先用 minimality 排除同色附件。

## 4. 正式外部刻畫的精確套用

依 [Dvořák 講義 Theorem10／印刷頁6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
及同頁 blockwise uniform 定義，連通 C 的不可著色 degree assignment 可寫為
每個 block K 的 palette S_K，且

$$L^D(x)=\bigcup_{K\ni x}S_K,\qquad
K\cap K'\ne\varnothing\Longrightarrow S_K\cap S_{K'}=\varnothing.$$

奇環的 palette 大小為2（triangle 作 clique 也同為2）；bridge palette 大小為1。
這是外部定理的結論，沒有從奇環名稱自行猜出 palette，亦未將 bridge 與共用割點混用。
來源 PDF／hash／第6頁核查見 [SOURCE](external/SOURCE.md)。

w_i 只屬 J_i 一個 block，故 L^D(w_i)=S_{J_i}。
由 §3，D∈S_{J1}∩S_{J2}；但 J1∩J2={r} 迫 S_{J1}∩S_{J2}=∅。
矛盾。故原 BR-SD-1a 精確來源合同不能同時成立。

## 5. 推論與停止點

此任意大小來源矛盾由原 degree 計算、兩個具名私有點的存在性及正式 Gallai 刻畫負責。
有限控制不承擔無界量詞，也不以零 source 觸發證成排除。
合同保留的 minimality、Σ、disk／T4 等強前提，以及 SD-A／H 二連通／R27 等上游路線條件，
均不是這段短證明的使用依賴；新合同直接明設原形狀，不另明設 H 二連通。
原身份與資料合同仍保留，沒有放大研究宣稱。

舊 BR-SD-1 §5 的 F_C(β)={D}、uv→R27 branch sets、target 四 query 保持、target β-minimality
是舊 minor 路線的額外義務，本次任務明確允許直接矛盾，不使用或宣稱已補完它們。
若另談四 query，其 C 語義固定原 β 與 C–B／s–C 約束，暫不加 s–B spokes；
完整 M 對 β 的所有 s 色延拓空是拒絕假設。這兩種語義不能混用。

結論只對 no-U／long L／真框邊 pair short S、exact-S 45／54 的此具名三環單 bridge 子域。
一般環間 bridges、旁支、其他接點位置、更多環、一般非二連通分支、其他 derivative/core、
55、無45／54來源、一般 N45／N2／E、ε≥3、一般出口及主命題仍不由本證明覆蓋。
沒有新增 actual source 或 Lean theorem，也沒有修改 canonical 覆蓋表或發布採納。
