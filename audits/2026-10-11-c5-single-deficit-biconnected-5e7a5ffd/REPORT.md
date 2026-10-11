# 二連通單 degree-5 induced-C5 disk：獨立紙面查證

**裁定：指定前提下成立，無須補 minimality、T4 或 lists 全緊等前提。**
任意大小的結論依正式版外部定理與下列參數化原圖 branch sets；有限控制只核對明列構造。
這是本專屬 audit 的紙面裁定，沒有修改共享文件的採納狀態，也沒有新增 Lean 定理。

BASE／起始 HEAD：`4dd11f422c6fa49265a412085116b088786d0344`。
專屬交付目錄：`audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/`。
起始建立目錄前的 `git status --short` 為空。只在本目錄建立產物；無 commit、push 或發布。

## 1. 精確定理與用語

設 M 是有限簡單圖，具有 disk 嵌入，有序外框
`B=(b0,b1,b2,b3,b4)` 是 induced C5；其餘頂點均在 disk 內。
設 `H=M−V(B)` **二連通**。採標準定義：H 至少三點，連通，刪任一點仍連通。
恰一內點 s 滿足 `d_M(s)=5`，所有其他內點 v 滿足 `d_M(v)=4`。
這裡 degree 是此原 M 的完整 degree，包含全部原 boundary 附件。
令 `U={0,1,2,3}`，β 是原 B 的 proper U-coloring；不要求 β 使用全部四種色。

**定理。** 若 β 不能延拓為 M 的 proper U-coloring，則

\[
d_H(s)=2,\qquad H-s\text{ 是 Gallai tree}.
\]

Gallai tree 指連通圖，每個 block 是 complete graph 或 odd cycle；bridge 視為 K2 block。
同時可讀出 s 恰有三個原 B 鄰居，H−s 是一個連通的兩接點分量。
兩接點為 s 在 H 的兩個不同鄰居，保留其原名字及原 attachments。
定理不假設 β-critical、edge-minimal、接受全部 T4、Σ 的大小、excess、內點數上限或完整後繼分類。

## 2. 正式版文獻、頁碼與核讀方法

Daniel W. Cranston and Landon Rabern, *Beyond Degree Choosability*,
**The Electronic Journal of Combinatorics 24(3) (2017), #P3.29**，DOI `10.37236/6179`。
[期刊書目頁](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v24i3p29)；
[正式 PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/)；
[凍結本](literature/cranston-rabern-2017-final.pdf)。
正式 PDF 首頁載明 Published: Aug 11, 2017，共 14 頁。
SHA-256：`8b6b26981671cb839f96667653913e63b690d917a891483d32a44e1d1adc2271`。
[下載來源與 HTTP receipt](literature/download.json)。

以下均用**正式版印刷頁碼**，與 PDF 頁數一致；已直接視讀頁面，文字抽取只用於定位。

| 正式版項目 | 頁碼 | 本 audit 使用的內容與界線 |
| --- | --- | --- |
| Theorem A、f-AT／f-choosable 定義、Theorem B | 2 | 非 Gallai 連通圖 degree-choosable；f-AT 推出 f-choosable；後者定義量化恰 f-sized lists |
| stretch、D 定義、Main Lemma | 3 | stretch 是 subdivision **twice**；二連通單 deficit 的分類，詳見 §4 |
| Figure 1、Proposition 1.1 | 4 | 三 seed；粗邊數 **3／6／0**；Proposition 給 D 的不可 choosable lists |
| Theorem 3.6 | 11 | 只有 connected 時另有 Gallai、degree-1、Gallai 分量及 block／lobe 例外；不能改讀成原二連通結論 |
| Theorem 4.1 | 12 | connected **單 deficit** pair 的非 choosable 與非 AT 等價；不把此等價套到雙 root |

[視讀 p.2](literature/final-page-02.png)、[p.3](literature/final-page-03.png)、
[p.4](literature/final-page-04.png)、[p.11](literature/final-page-11.png)、
[p.12](literature/final-page-12.png)。
[Figure 1 高解析裁圖](agents/literature_minor_review/figure-04.png)及
[原 PDF 向量轉出](agents/literature_minor_review/figure-page4.svg)再交叉核對粗線。
三 seed 粗邊 stroke width 為 `2.98883`，細邊為 `0.79701`；細節與行定位保存在
[獨立文獻核讀](agents/literature_minor_review/REVIEW.md)。

注意網頁工具的文字抽取把 Main Lemma 的 `≥3` 誤顯為 `>3`；本報告採視讀的 `≥3`，
保存的本地 pdftotext 版本則正確顯示 `⩾3`。
作者首頁連出的 2015 PDF 是預印本，本次沒有用其 theorem 編號或圖頁代替正式版。
正式版 Theorems **3.6／4.1** 的位置是 **11／12** 頁。

## 3. 從原 boundary 附件到非 f-choosable

对每個原內點定義

\[
N_B(v)=N_M(v)\cap V(B),\quad t(v)=|N_B(v)|,
\quad L_\beta(v)=U\setminus\{\beta(b):b\in N_B(v)\}.
\]

H 是刪 B 後的 induced graph，故同一原 M 內的 degree 恆等式為

\[
t(v)=d_M(v)-d_H(v).
\]

原附件使用的**相異色數**至多 t(v)，即使兩條 spokes 落在 β 同色的 B 點也成立。
因此

\[
|L_\beta(v)|
=4-|\beta(N_B(v))|
\ge4-t(v)
=d_H(v)-\mathbf1[v=s]. \tag{1}
\]

因 β proper、B induced 且邊分成 B 邊、H 邊及原 spokes，β 可延拓到 M
當且僅當 H 有 proper Lβ-coloring。這裡沒有刪 spokes、替換接點、改色框或先做 minor。

設 `f(v)=d_H(v)−1[v=s]`。二連通給每點內度至少二，故 f(v)≥1。
若 β 拒絕，H 沒有 Lβ-coloring。逐點任取
`L′(v)⊆Lβ(v)` 且 `|L′(v)|=f(v)`，由 (1) 可以選取。
任一 L′-coloring 也會是 Lβ-coloring，所以這個恰 f-sized assignment 仍不可著色。
它便是一份證實 H **非 f-choosable** 的 assignment。

正式版 Theorem B 的反向否定因此給出 `(H,h_s)` **非 AT**，其中 h_s 在 s 為一、其餘為零。
此步完全不要求原 Lβ 全緊；沒有從「一份 list 拒絕」跳成「所有 lists 拒絕」。
Theorem 4.1 另外確認此單根非 choosable／非 AT 分類一致；主證明只需 Theorem B 的這個方向。

## 4. 二連通、高內度的例外恰為 complete 或 D

正式版 Main Lemma 對二連通 H 給出 `(H,h_s)` 為 AT 當且僅當以下之一：

1. `d_H(s)=2`，且 H−s 不是 Gallai tree；
2. `d_H(s)≥3`，H 不是 complete，且 `(H,h_s)∉D`。

由 §3 的非 AT，若 `d_H(s)≥3`，便只能是 H complete 或 `(H,h_s)∈D`。
沒有額外高內度 odd-cycle 例外：odd cycle 的每點 degree 為二，已屬第一分支的否定。
這是**指定 root 的 pair** 分類，不能只認出無 root 的 graph 或換一個 degree-5 點。

D 僅由 Figure 1 三 seed 的 **bold edges** 反覆 stretch 形成：

- 左 seed：triangle `a1a2a3` 加根 s，三條 `sai` 均為 bold。stretch 後是三條
  internally disjoint paths P_i 從 s 到 a_i，每條長度 `1+2k_i`，k_i≥0；triangle 不 stretch。
- 中 seed：三條 `sai` 各先 subdivide once，記為 `s−u_i−a_i`；六條 spoke 段均為 bold。
  六段各 stretch 任意非負次數後，P_i 長度為 `2+2(k_i^0+k_i^1)`；triangle 不 stretch。
- 右 seed：Moser spindle，**零條 bold edges**，此支沒有允許 stretch。

不把「任意圖的任意邊可以 subdivision」當成 D 的定義；下段 minor 證明涵蓋全部上述允許參數。

## 5. 三 seed 及所有 stretch 的原 H K4 minor

### 5.1 左、中 seed 的任意長 spoke paths

在同一原 H，令

\[
Q_0=\{s\},\qquad Q_i=V(P_i)\setminus\{s\},\quad i=1,2,3.
\]

四組非空、互斥、connected：三路徑內點互斥，a_i 也互異。
`Q0−Qi` 的來源邊取 P_i 的第一邊；`Qi−Qj` 取原 triangle 邊 `a_i a_j`。
六個 bag pairs 全部相鄰，故是 K4 minor。路徑長度不限，證明沒有有限上界或奇偶上的漏洞。
相同構造可合成每次 stretch：只把新增的兩個路徑點留在該路徑的原 bag，不會與其他 bags 混合。

### 5.2 Moser spindle

固定原名字：根 s；左 diamond 其餘三點 a,b,e；右 diamond 其餘三點 c,d,f。
Figure 1 的原邊恰為

`sa,sb,ab,ae,be,sc,sd,cd,cf,df,ef`。

令

\[
Q_0=\{s,c,d,f\},\quad Q_1=\{a\},\quad Q_2=\{b\},\quad Q_3=\{e\}.
\]

Q0 可用 `sc,sd,cf` 作 spanning tree，其餘都是 singleton，四組互斥。
六個 bag-pair 來源邊依次可取 `sa,sb,fe,ab,ae,be`。
故此 seed 也在原 H 有 K4 minor，未使用任何不允許的 spindle stretch。

## 6. 完整原 degrees 與加入原 B 的 K5 minor

§3 的 `t(v)=d_M(v)−d_H(v)` 逐點給出：

| D 中原點類型 | d_H | d_M | 原 B 附件數 t |
| --- | ---: | ---: | ---: |
| 左／中 seed 的 s | 3 | 5 | 2 |
| 三個 triangle 錨點 a_i | 3 | 4 | 1 |
| 路徑內點，含中 seed 的 u_i 及所有 stretch 新點 | 2 | 4 | 2 |
| spindle 的 s | 4 | 5 | 1 |
| spindle 其餘六點 | 3 | 4 | 1 |

**所以每個 D 頂點確實有至少一条原 B-spoke。**
此處使用完整原 M degrees，並非任意抽象 lists 的緊性、G 中的 degree 或另一個 reduced graph 的附件。

在 §5 的四個原 H bags 上，加入

\[
Q_4=V(B).
\]

原 C5 邊使 Q4 connected；它與四個內部 bags 互斥。
每個 Qi 至少含一個原點 v_i，選它的一條真實原 spoke `v_i b_i`。
此邊給 `Qi−Q4` 的 adjacency。前六條 K4 witness edges 仍在原 H，
四條 spoke edges 也都在同一原 M，故十個 bag pairs 全部相鄰，形成 M 的 K5 minor。
不同 spoke 可以共用 B 端點；因整個 B 只是一個 bag，沒有互斥性衝突。
未要求每個 attachment 有相異顏色，也未替原 spoke 補一條方便的新邊。

M 為 planar disk，而 planar 圖的 minors 仍 planar、K5 非 planar，矛盾。
因此所有 D 高內度例外都排除。收縮 B 在此只是一份非平面性證書；不聲稱保持 boundary states 或完整 Σ。

**Complete 情況另處理。** 若 H complete 且 `d_H(s)≥3`，令 n=|V(H)|，則 n≥4。
任何非根點的 `n−1=d_H(v)≤d_M(v)=4` 給 n≤5。
若 n=5，原 H 已是 K5 subgraph；若 n=4，s 有兩條原 B 附件，其餘三點各有一條。
取四個 H singleton bags 與第五 bag V(B)，便直接得到同一 M 的 K5 minor。
n≥6 與完整 degree 條件不相容。故 complete 高內度例外也全排除。

## 7. d_H(s)=2 與 H−s Gallai 的最後一步

二連通給 `d_H(s)≥2`；§4–6 已排除全部 `d_H(s)≥3`，因此 `d_H(s)=2`。
若 H−s 不是 Gallai tree，Main Lemma 的第一分支會使 `(H,h_s)` 為 AT，
與 §3 矛盾。故 H−s 為 Gallai tree，完成主證明。

最後結論也可獨立重證，免把 Main Lemma 當作黑箱的全部輸出：
二連通使 C=H−s connected，且 (1) 使 Lβ(s) 非空。
任取 `a∈Lβ(s)` 著色 s，對每個 v∈C，從 Lβ(v) 刪 a 當且僅當 vs 是原邊。
所得 list Lβ,a 滿足

\[
|L_{\beta,a}(v)|\ge d_H(v)-\mathbf1[vs\in E(H)]=d_C(v).
\]

若 C 非 Gallai，正式版 Theorem A p.2 經逐點取 degree-sized sublists 後便可著色 C，
從而延拓同一 β 與 s=a，矛盾。
這個直接論證其實在尚未證出 d_H(s)=2 前就成立；它使用的是二連通給連通與非空 root list，
而非 obstruction minimality。

## 8. 前提篩選與保存的反例

所有圖均是明列的 named constructions，沒有搜尋或擴大來源目錄。
每張圖保留 B 的字面次序、全部原 edges／attachments、β、rotation、faces，以及全部 `4^|H|` 色指派的結果。
反例只反駁表中明寫的變更版本；不將域外小圖稱為原定理反例。
程式與證書入口見 §10。

| 變更／控制 | 狀態 | 精確結果 |
| --- | --- | --- |
| 原前提 named triangle | **triggered and holds** | 有 proper 拒絕列，s 內度二、H−s=K2，證明原域非空 |
| 撤除二連通，仍要求 H connected | **counterexample** | 下例 A 完整 degrees 5/4/4、proper 拒絕列，但 d_H(s)=1 |
| 增加第二個完整 degree-5 點 | **counterexample** | 下例 B 的 H 二連通，兩 root 內度三；兩色 diamond 拒絕 |
| 允許 improper β | **counterexample** | 下例 C 的圖滿足原 graph 前提，但 boundary 自身衝突即拒絕，d_H(s)=3 |
| 混用完整 G／M degrees | **not triggered**（定理反例） | 保存 honest M⊆G 的 bookkeeping 控制，兩者 degree 不同；此例的結論仍成立，未取得此變更版本的反例，不宣稱完整 M equality 的必要性 |
| 丟失原附件後，只從 H 有 K4 推得 M 有 K5 | **counterexample**（此中間推論） | 下例 D 是 planar、H=K4，只一條 B 附件；第五 bag 缺三個 adjacencies；此圖不满足原完整 degrees |

### 原域非空控制

H 是 triangle `sxy`。附件為
`s:{b0,b1,b2}, x:{b3,b4}, y:{b2,b3}`，β=`(0,1,2,1,2)`。
完整 degrees 為 5/4/4；lists 是 `{3},{0,3},{0,3}`，所以 triangle 無法著色。
H 二連通，`d_H(s)=2`、H−s=xy，符合結論。disk rotation 在完整證書中。

### A. 撤除二連通

H 是 path `s−x−y`；附件為
`s:{b0,b1,b2,b3}, x:{b0,b3}, y:{b0,b3,b4}`。
β=`(0,1,2,3,1)` proper；完整 degrees 5/4/4，但 `d_H(s)=1`。
s 的四個附件使用四種色，Lβ(s)=∅，故 β 拒絕。
這裡空 list 是被撤除二連通後合法出現的情形，沒有暗中加入非空 lists 前提。

紙面 disk 嵌入：先作 s 到 b0,b1,b2,b3 的 fan，留下四邊面 `(s,b3,b4,b0)`；
在此面放 x，接 s,b3,b0，留下 `(x,b3,b4,b0)`；再放 y，接 x,b3,b4,b0。
所有邊位於原 disk，沒有 B chord。Theorem 3.6 p.11 的 degree-1 及 Gallai 分支容許此例。

### B. 第二個 degree-5 點

H 是 diamond：`sx,xt,ty,ys,st`。
附件為 `s:{b0,b1}, x:{b1,b2}, t:{b2,b3}, y:{b3,b0}`。
完整 degrees 為 s=5、t=5、x=y=4；H 二連通，s、t 的內度均為三。
β=`(0,1,0,1,2)` proper，四個 lists 全為 `{2,3}`，triangle sxt 已不可著色。
故「容許第二個 degree-5，仍推 s 內度二」為假。

紙面 disk 嵌入：內 cycle `(s,x,t,y)` 對外連向依序 `(b0,b1)`、`(b1,b2)`、
`(b2,b3)`、`(b3,b0)`，b3 到 b0 的外路經 b4；在內 cycle 內放 diagonal st。
這份有序嵌入沒有 crossing，完整 faces 在證書中。

### C. Improper β

仍用上述 diamond H；附件改為
`s:{b0,b1}, x:{b1,b2}, t:{b3}, y:{b4,b0}`。
完整 degrees 為 5/4/4/4，H 二連通、`d_H(s)=3`。
令 β=`(0,0,0,0,0)`，外框邊已衝突，故無 proper extension。
但 H 的 lists 全為 `{1,2,3}`，且有 proper list-coloring，例如 `(s,x,t,y)=(1,2,3,2)`。
這精確顯示 §3 的 extension iff list-coloring 必须 β proper。
disk 嵌入可按四個內點依序連到所列外側弧，再放內 diagonal st；rotation／faces 已保存。

### D. 丟失原附件的中間推論

H=K4，只有 s 接 b0，其餘三點沒有 B 附件；B 還是原 induced C5。
這是 planar disk：將 K4 畫在 B 內，再以一條 bridge 接 b0。
H 的四個 singleton bags 給 K4，加入 B 的第五 bag 卻只與 s 相鄰。
所以「有 K4」本身不能補足三條缺失的原 edges。
這張圖的完整 degrees 為 4/3/3/3，且 proper β 可延拓；它是**中間推論**的反例，
原定理域為 **not triggered**。在原定理內附件已由完整 degrees 推得，
不是可以一面保留 degrees、一面刪去附件的獨立假設。

### G／M bookkeeping 的界線

從原域 triangle 控制的 G 刪除原 spoke `sb0` 得到 M。
在 G 中 degree 是 5/4/4，在 M 中是 4/4/4；兩張圖保留相同 H、B 與 β。
M 仍拒絕該 β，且結論仍成立。
此 named 控制以 **triggered and holds** 標記「正確辨識 degree 差異」，
以 **not triggered** 標記「原定理及混用 degrees 的反例」。
若 M 是 G 的真實子圖，G 的 upper bounds 可傳給 M，但不能將 equality 或精確 t(v) 原樣傳遞。
本次沒有證出、也沒有反駁所有其他明確寫法的 G-degree 版本；不以這個 bookkeeping 控制宣稱該前提必要。

未做其他前提的必要性分類。特別是 K5 排除只用 planarity、B connected、原附件；
這個觀察不自動給出任何撤除 C5／disk／degree 前提的完整推廣定理。

## 9. 與既有 degree-5／block 成果的重疊

BASE 的文字與雜湊均已凍結，見 [authority/input-hashes.json](authority/input-hashes.json)。
較詳細對照見 [独立重疊核讀](agents/existing_results_overlap/OVERLAP.md)。

| 既有成果 | 重疊 | 本次新增／沒有新增的內容 |
| --- | --- | --- |
| `c5_weak_list_cores.md:101–107` | degree-4 誘導分量的 Gallai 化約 | 舊證明用 minimality 著色 exterior；此處直接取合法 s 色，故不需 minimality |
| `c5_degree5_interfaces.md:108–125` | 固定 root 色後 residual lists ≥ 分量 degree；tight/slack 分析 | residual 下界是重述；二連通使 H−s 成一個分量，無須先給 minimal core |
| `c5_k4_blocks.md:78–100` | 原圖 K4 bags 配真實通 B 路徑，加入 B 得 K5 | minor 原理是重述；D 每點完整 degree 直接迫原 B-spokes，不需 minimality 的 bridge forcing |
| `c5_degree5_guide.md:16–31,44–49` 的 R 系列 | `d_H(s)=2` 正是三-spoke、單一兩接點 C 的 (2) 型 | 新排除任意 proper β、非 minimal、二連通 H 的所有高內度 complete／D 例外；不完成三環／更多環的來源 minors |
| `c5_single_sided_exit.md:170–224` | 唯一 degree-5 的條件式出口已有成果 | 此定理只從一列拒絕推出結構，沒有第二列分離、adjacent patterns、Σ=Ω\{p,q} 或出口結論 |

新增覆蓋是**二連通 H 的單 degree-5 結構限制**及不需 minimality／T4 的適用範圍；
H−s 的 Gallai 結論與 K4+B minor 方法均有既有前身。
本定理不是逐一排除 H−s 的 Gallai block 型，故不補 R31 任意長來源 minor 缺口。
不從此提升為全部 45/54/55、ε≥3、一般單側／共同出口或 `K∞=K≤5`。

## 10. 計算控制、完整證書與重播

兩组控制各自標明正在檢查的 claim；原定理觸發與域外 lemma 觸發分開。

1. [前提控制程式](agents/premise_controls/replay.py)：六張 named graphs，
   共 960 個完整 interior assignments；逐 assignment 保存成功或所有衝突，
   並以 list-restricted 的獨立次序搜索核對 counts。
   所存 rotations、逐 face 邊與 Euler characteristic 核對 disk；NetworkX 只用於生成／核對這些固定 named rotations。
   [完整前提證書](agents/premise_controls/certificates-final-v1.json)。
2. [minor 控制程式](agents/existing_results_overlap/minor_controls.py)：只對每條指定 bold edge
   stretch 0/1/2 次，左 seed 27 筆、中 seed 729 筆，再加 spindle 與 complete K4，共 758 筆。
   每筆保存全部原 edges、stretch 參數、degrees、真實合成附件、bags、bag trees 與全部十對來源 edge witnesses。
   這些合成附件使圖已含 K5，故其 minor claim 是 **triggered and holds**，
   原 disk 定理則逐筆是 **not triggered**；沒有把它們稱為 disk 來源或 rejection/coloring 控制。
   [完整 minor 證書](agents/existing_results_overlap/minor-controls/certificates.json)。

這 758 筆不是任意圖枚舉、不是把任意 edge stretch 混入 D，也不負責無界量詞；
§5–6 的原圖參數化構造才負責所有 stretch 次數。
replay 使用原證書逐 byte 比較；正常與 `PYTHONHASHSEED=17` 重播及損壞證書負控制見
[驗證紀錄](VALIDATION.md)。未重新跑既有 source catalog、舊全量研究 checker、DocGraph 或 lake build。
後兩者不能驗證本次未形式化的紙面 Gallai／AT／disk minor 論證。

## 11. 依賴、證據分層與最終裁定

主證明依賴：原 M degree 恆等式與原 proper β 的 list 翻譯；正式版 Theorem B＋Main Lemma；
Figure 1 的精確 D 定義；原圖 branch-set 構造；planarity 對 minor 封閉及 K5 非 planar。
§7 的獨立 Gallai 證明另使用 Theorem A。Theorems 3.6／4.1 用來核對 connected 與 choosability 的界線，
沒有誤用成雙 degree-5 theorem。這些外部定理未在此 audit 從頭重證。

| 證據層 | 本次狀態 |
| --- | --- |
| 正式版文獻與圖像核讀 | 已核讀指定五項與 Theorem A，保存正式 PDF、hash、頁面與向量圖 |
| 任意大小紙面命題 | **成立**，在 §1 明列前提下完成證明 |
| 有限 named graph／minor 控制 | 保存完整證書与可重播程式，逐 claim 使用三種狀態 |
| 來源實現性 | 只有明列原域控制及前提反例的 named disk embeddings；不枚舉全部來源 |
| Lean | **本次未新增、未形式化** Main Lemma、Gallai 分解或本 minor 證明；既有 Lean 状態不因此提升 |
| 45/54/55、ε≥3、一般出口、K∞=K≤5 | 本 audit 不裁定、不提升 |

最終裁定為：**原推論成立；不需補 lists 全緊、minimality 或 T4 前提。**
撤除二連通、容許第二個 degree-5、容許 improper β 的具體變更版本已有保存反例。
G／M bookkeeping 與失去原附件分別按實際檢查的 claim 記錄，未取得的反例不寫成必要性結論。

輸入與權限稽核见 [initial-receipt.json](initial-receipt.json)、
[BASE 凍結输入 hashes](authority/input-hashes.json)、[最終封存 receipt](seal.json)及
[產物 SHA-256 清單](MANIFEST.sha256)。
