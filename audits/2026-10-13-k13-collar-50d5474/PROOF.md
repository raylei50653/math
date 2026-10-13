# K13-COLLAR：來源化約、外圈完備性與球面生成覆蓋

固定 BASE：`50d5474f2446403f3b3001d5943571184c8c9936`。
本文先證來源覆蓋，再以本輪完整有限證書與獨立核對證成有界等式；
實際執行及信任邊界集中於 [REPORT](REPORT.md)。

## 1. 全域最小來源及既有前提的適用性

反設某個至多十三內點的有限簡單 disk-C5 圖的完整關係不在 K132。
在**全部**目錄外來源中先取內點數 k 最小者，再於該 k 取邊數最多者 G。
這個集合非空，k 是非負整數；固定 k 的簡單圖邊數有上界，所以兩步極值存在。
由既有 `K_{≤12}=K_{≤5}=K132`，以及反設提供的 k≤13，恰有 k=13。
這不是固定 mask 或固定 h 的極小化。

正式來源的具體作用如下。

* [共面正規形](../../docs/c5_cofacial_normal_form.md) §2：K132 對二元聯集封閉；
  至少一端內部的共面識別減少 k。識別／加邊的完整關係聯集式與最大邊數
  共同給簡單、二連通、無外框 chord、所有內面三角化的 G。
* [度數界](../../docs/c5_saturation_degree_bound.md) §1–4：同一全域選擇給
  原框點完整 degree≥4，原內點完整 degree≥5。低度替換允許改變 mask 的
  中間分支，但其完整聯集或具名介面接合保持原 Σ，因此必須使用全域最小性。
* [完整外圈](../../docs/c5_neartri_boundary_collar.md) §1–2，以及其
  [原始證明](../2026-10-12-neartri-complete-relation-reductions-5d70a399/REPORT.md)
  §3–6：無二邊非相鄰 B crosscut，無含頂點的分離三角形，並存在下面的
  實際具名簡單內圈。既有完整 transfer／Kempe／共同計數證明排 h≤2。
* [C8 apex 定理](../../docs/c5_c8_apex_degree.md) 及其
  [證明](../2026-10-13-c8-apex-degree-45bc1c3/PROOF.md)：只在 h=3 的八份
  完整剩餘來源契約下，所有五個 apex 的 H-degree≥4，從而 k≥14。
  本文只使用其 `h=3 ⇒ k≥14` 推論，不向更長 C 移植無弦或 apex 度數。

普遍候選 screen 允許把**整張** G、原有序 B、全部染色共同以 D5 搬運到
Σ=933 或 941。這個步驟只用於上述上游結果的適用性。本輪有限核心最後
直接計算全部十列並比對 K132，不只測試兩個 masks。沒有加入 N2、ε=2、
edge-critical、Gallai、兩個 roots 或其他 session 的新結果。

## 2. Euler 式及完整四分支

一般外面為 C_b、嚴格內點數 m 的三角化 disk，令內面數為 f、邊數為 E。
Euler 式 `(m+b)−E+(f+1)=2` 與面邊計數 `3f+b=2E` 給

\[
 E=3m+2b-3. \tag{1}
\]

對原 G，b=5、m=k=13，故 `|V(G)|=18`、`|E(G)|=46`。
寫 `D_B=Σ_{b∈B}d_G(b)=20+h`。握手式給

\[
\sum_{v\notin B}(6-d_G(v))=6k-(2E-D_B)=D_B-14=6+h.
\]

全部原內点 degree≥5，故將 degree 5、6、≥7 分開，精確得到

\[
 n_5=6+h+\sum_{v\notin B,\ d_G(v)\ge7}(d_G(v)-6). \tag{2}
\]

因 n5≤13，h≤7。既有 h≤2 排除，h=3 又迫 k≥14，故本反設恰只剩
h∈{4,5,6,7}。下節原內圈有 5+h 個不同原內點，所以其內側 H 滿足
`|V(H)|=13`、`|I|=8−h`。再以 (1) 取 b=5+h、m=8−h：

\[
 |E(H)|=3(8-h)+2(5+h)-3=31-h. \tag{3}
\]

| h | 原內圈 C | 嚴格內側點 | E(H) | 全部具名超額配置數 |
|---:|---|---:|---:|---:|
| 4 | C9 | 4 | 27 | 70 |
| 5 | C10 | 3 | 26 | 126 |
| 6 | C11 | 2 | 25 | 210 |
| 7 | C12 | 1 | 24 | 330 |

此表首先是窮盡來源的化約，不自行構成排除。

## 3. 每份具名超額如何決定原環帶

固定原 B 的方向及起點，令 `e_i=d_G(b_i)−4≥0`，`Σe_i=h`。
令 a_i 為原框邊 `b_i b_(i+1)` 內側原三角面的第三點。
若原內點同時接非相鄰 B 點，會違反既有二邊 crosscut 定理。
若它同時接相鄰 B 點而不是該框邊的 a_i，這三點圍成的三角形包住原面
apex，違反分離三角形排除。因此各 a_i 互異，每個恰接兩個 B 點；
其他 B 鄰點恰接一個 B 點。

沿 b_i 原 rotation 的內側 sector，其所有內鄰點依序是

```
a_(i−1), y_(i,1), …, y_(i,e_i), a_i.
```

度數式保證恰有 e_i 個 y。依原 rotation 排序**定義**這些名稱，因此沒有
額外未列入的 y 排列。三角面使連續鄰點相連；不同 i 的 y 彼此不同，也不與
任何 a 相同。五條鏈拼成實際簡單環

```
C = (a0, y_(1,1), …, y_(1,e1), a1,
         y_(2,1), …, y_(2,e2), a2,
         y_(3,1), …, y_(3,e3), a3,
         y_(4,1), …, y_(4,e4), a4,
         y_(0,1), …, y_(0,e0)).
```

環帶的原邊完整包含 B、C、`b_i a_(i−1)`、`b_i a_i` 及全部 `b_i y_(i,j)`。
原面完整包含 `(b_i,b_(i+1),a_i)`，以及 b_i 與上述鄰鏈每條邊的三角形。
這些三角形逐側填滿 B 與 C 之間的環帶，決定其 rotation；任何額外 B 附件
已在定義鏈中，任何額外環帶內邊都必切開其中某個原三角面，不可能。
**唯一尚未決定的幾何自由度是 C 的嚴格內側，包括所有 C chords、內邊、
邊界—內側附件及其 embedding。** 本輪球面生成完整保留這個自由度。

故 `d_G(a_i)=d_H(a_i)+2`、`d_G(y)=d_H(y)+1`，得到且只得到

\[
d_H(a_i)\ge3,\quad d_H(y)\ge4,\quad d_H(v)=d_G(v)\ge5\ (v\in I). \tag{4}
\]

具名配置就是五份非負整數合成，數目 `binom(h+4,4)`，得表中四個數字。
若採用 D5 代表，作用必為一份共同的 `i↦s+δi (mod5)`，δ∈{1,−1}，並同時
搬運 B、a、y 的原 rotation、C、所有原邊及全部 literal 染色。反射時 a 的
下標及每條 y 鏈方向按實際框邊／rotation 誘導，不可只反射 e 而保留附件。
具體地，若新 `b'_i=b_(s+δi)`，則 `e'_i=e_(s+δi)`；δ=1 時
`a'_i=a_(s+i)`、`y'_(i,j)=y_(s+i,j)`；δ=−1 時
`a'_i=a_(s−i−1)`、`y'_(i,j)=y_(s−i,e_(s−i)+1−j)`。
所有下標均模五，反射同時反轉全部頂點的 rotation。
全部具名配置至代表的映射由本包配置資料保存；orbit 數為 10、16、26、38。
本輪生成並不以代表數取代具名覆蓋。

## 4. 可獨立紙面排除的最小內側域

本節不參與球面生成剪枝；它另行排除 h=7、h=6 及 h=5 無 chord 子域。
全程固定同一 H、原 C、原邊與原 rotation，沒有替換來源或接合不同染色。
因此屬純結構不存在定理，不需另聲稱完整關係保持的局部改圖。

### 4.1 空側弦與葉 cell 引理

H 的每個 C 點都至少三度。若 C chord uv 的某側没有嚴格內點，该側就是
多邊形三角剖分。三角形時 uv 以外的頂點是 degree 2 ear；較大多邊形的
剖分有至少兩個非相鄰 ears，而 u、v 在該側多邊形相鄰，故至少一個 ear
不是端點。這個 ear 的整個 H 內側 sector 位於該側，迫其 H-degree=2，
矛盾。所以**每條 chord 的兩側都必含 I 點**。

也可一次切開全部 C chords。非交叉 chord 對偶是一棵 cell 樹；每個葉 cell
只以一條 chord 接其餘部分。若葉 cell 不含 I，因全部 chords 已切開，
它必為三角形，其兩條 C 邊夾出的頂點 H-degree=2。因此每個葉 cell 都含 I。
不同 leaf 的非附件端點集合不交。

### 4.2 無弦的精確附件預算

設 H 無 C chord，`m=|I|≥1`、`q=|E(H[I])|`、`s=|E(C,I)|`。
每個 C 點的內鄰點沿原三角面形成 I 中的一條非空路徑；相鄰 C 點的路徑
共用該 C 邊的原三角面第三點。其聯集因此連通。I 的任何其他分量亦須沿
H 的路徑接到 C，從而接到這個聯集，故 H[I] 連通，q≥m−1。
由 (1)，`b+s+q=3m+2b−3`，所以

\[
\sum_{v\in C}(d_H(v)-3)=s-b=3m-3-q\le2m-2. \tag{5}
\]

每個 y 在左邊至少貢獻一，因此 h≤2m−2。m=1、2、3 時，分別不能有
h=7、6、5。注意這只在**已證無弦的子域**使用，不向所有 H 偷加無弦前提。

### 4.3 h=7 的全部來源

此時 |I|=1。任一 chord 的兩側不可能同時含 I，故由 §4.1 沒有 chord。
H 是唯一內點接全部 C 的輪，全部 C 點 H-degree=3，違反七個 y 的 (4)。
等價地，(5) 左邊必為零卻至少七。故 h=7 的全部 330 份配置均排除。

### 4.4 h=6 的全部來源

此時 |I|=2。無 chord 時 (5) 已排除。若有 chord，將全部 chords 切開。
cell 樹每個葉均需含 I，而全圖只有兩個 I，所以樹恰有兩個葉，是一條路徑；
兩個葉各有唯一 I 點，其餘 cell 沒有 I。每個葉 cell 無額外 chord，故是
一個輪。其內點的全部原 H 邊都在此 cell，degree≥5，輪的外環至少五點。
除了與其餘 cells 接合的 chord 兩端，至少三個 C 點的 H-degree 恰三。
兩葉合計至少六個不同的 H-degree 3 原 C 點，但 (4) 允許 degree 3 的只有
五個 apices，矛盾。因此 h=6 的全部 210 份配置亦排除。

### 4.5 本節不排除的域

h=5 無 chord 的全部子域由 (5) 排除；有 chord 的 h=5 以及 h=4 的全部
內側域留給下面的**完整**有限分類。沒有把本節必要條件當作無證剪枝。

## 5. 十九點最小度五球面三角化的覆蓋定理

對 §1 的任何 G，在 B 外面的 disk 加新點 z，僅加五條 `z b_i`。
外側五個三角面 `(z,b_i,b_(i+1))` 與原 G 組成簡單球面三角化 T。
`|V(T)|=19`、`|E(T)|=51`、所有面皆三角形；z degree 5，原 B 的 T-degree
為其 G-degree 加一，其他點 degree 不變。因此 T 的最小 degree 至少五。

反之，取任一十九點簡單球面三角化 T 及任一 degree 5 頂點 z。
其原 rotation 中五個不同鄰點 `(b0,…,b4)` 由五個三角面相連成簡單 C5。
刪 z 和它的五條邊，原星形 disk 成為**指定外面**，得到原邊界恰為該 C5
的簡單三角化 disk G，十三內點、46 邊、邊界 degree≥4、內部 degree≥5。
鄰環可能有 chords；它們全部保留。此逆向敘述故意容許比最小來源更大的類。

所以，生成全部 T，再取**每一個** degree 5 root，已包含每一個可能的原 G。
生成資料保留 sphere rotation；checker 刪除 root 後沿 darts 重建 faces，
確認外面恰為所指定的 B。這不是只檢查抽象 planarity。

每個 sphere 同構類可以只輸出一份，因任一嵌入同構將原 z 搬到某個已取的
root；原 B 的起點與方向恰有十個可能，完整 D5 輸運全部保存。對稱只作用於
整張具名圖。即使重複取到同構 root，亦不影響覆蓋或關係檢驗。
這提供完整內側分類：對每份實際來源，先唯一外加 z，再落入 sphere 代表與
root，最後由具名 B／C map 還原其全部 chords、內邊、附件、rotation 及原面。
不需要從低度插點族猜測所有近三角化來源。

### 5.1 直接內側分類的第二條完備路徑

還可直接從每個待排除的 H 出發，在指定 C 外面加新點 q 接全部 C。
所得 sphere U 有十四點；q 的 degree 是 5+h∈{9,10,11,12}，各 C 點的
U-degree 是其 H-degree 加一，I 點 degree 不變，所以 U 的最小 degree≥4。
原所有 chords 留在 U，q 的星形面記錄原 C 的指定外面。

因此 `plantri -m4 14` 的全部 2,472 份 sphere，每份每個 degree 9–12 的
root q，涵蓋全部四分支 H。刪 q 時取原星形 disk 為外面並保存原 rotation。
之後恰使用兩項 degree 必要篩選：

1. 不鄰接 q 的頂點就是 I；其 degree 若小於五，違反原完整內點 degree。
2. q 的 degree 4 鄰點在 H 中 degree 3，必是 apex。因此這些
   `forced_apices` 若多於五，無合法五個 apex 配置。

剩下的 root 上，枚舉 C 的**全部**五點子集 A，要求包含所有 forced apices。
這條件充分保證 (4)：A 各點 H-degree≥3，而 C\A 各點 H-degree≥4。
沿 C 的原循環依序把五點命名為 a0,…,a4；兩 apices 之間的點全部作其唯一
B 附件的 y。§3 已證明這恰決定原環帶。任一來源必出現在其中一份子集，
起點／方向則由十份共同 D5 映射還原。這條路徑沒有丟棄任何 chord，沒有
其他未證小 cap、連通性或 adjacency 剪枝。

每份 A 都依原有向面接回五個 B，再在 B 外加 z，得到十九點最小度五 sphere；
程式保存到 §5 主生成代表的完整頂點映射、全域 orientation、root 與 B-frame。
所以它的十列及全部 full lifts 可由同一映射拉回主證書，而不是另取某份
具有相同邊際 mask 的 H。反方向，主生成所有 h=4–7 roots 的具 root 嵌入
同構類與這條內側生成路徑的 completed 圖**集合相等**，合計 26 類。

| h | 原始 q roots | 通過 degree 的 q roots | 五個 apex 子集 cores | 全部具名 e | 有 degree 合格 core 的具名 e |
|---:|---:|---:|---:|---:|---:|
| 4 | 629 | 19 | 27 | 70 | 55 |
| 5 | 214 | 1 | 1 | 126 | 10 |
| 6 | 41 | 0 | 0 | 210 | 0 |
| 7 | 2 | 0 | 0 | 330 | 0 |

所有 736 份具名 e 均列入 [named_configurations](generation/named_configurations.json)，
包括沒有任何 core 的空域；各 core 保留完整 embedding 及到主來源的映射，見
[inner_cores](generation/inner_cores.json)。
例如 h=4 的另外 15 份 e、h=5 的另外 116 份 e，沒有滿足原 degree 契約的 H；
其他 65 份非空配置的所有 core 則由完整 Σ=1023 排除目錄外身份。
這裡「無 core」的普遍性來自上面的 cone／root／全部 A 覆蓋證明及外部生成
完備性，不是從有限隨機零命中推論。

## 6. 生成完備性的外部部分與本輪重播部分

採用固定的 plantri 5.8 `-m5 19`。其 guide 明定 `-m5` 是所有三連通、最小
degree 五的 plane triangulations；一般簡單球面三角化本來三連通。
沒有使用 `-c5` 或把五連通當作來源前提。

外部構造完備性依賴 Brinkmann–McKay，*Construction of planar triangulations
with minimum degree 5*，Discrete Mathematics 301 (2005), 147–163，
[DOI](https://doi.org/10.1016/j.disc.2005.06.019)、
[作者全文](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf)。
其 Theorem 2 的更正證明，結合 Theorems 1、3、4，包含有分離三環與四環的
全部最小度五類；不是僅有滿足某個較高連通性子類的構造。生成的同構刪除
另依賴作者程式的 canonical construction path 實作。Table 1 的十九點計數
為 23，Table 2 的保向同構計數為 33，可供外部計數交叉核對。
本包保存的 [作者全文](generation/min5paper_sc.pdf) SHA256 為
`d9a1c671d189965a3de57b2ec004cee6c7bea8bf24f0cccb17a1e7172b33d97f`。

最小度四入口的外部依賴另見 Brinkmann–McKay，*Fast generation of planar
graphs*，[作者 expanded version](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf)
§2，Figure 6：从 octahedron 以 R4、R5、S 生成全部三連通 min4
triangulations。這是 §5.1 的十四點內側分類及下述十九點交叉生成的依據。
本輪不把它與 min5 構造稱為兩個獨立軟體實作。

本輪另外由最小度四生成入口枚舉，再對**完成圖**作全部頂點 degree≥5 的
終端篩選；其內部生成路徑不同，兩份輸出以獨立嵌入 canonical 化比對。
這項交叉重播是生成／實作校準，不被冒稱為完全獨立的新生成定理。
具體命令、source hashes、編譯版本、輸出 counts、正常與 seed17 核對及未
重播部分由 [REPORT](REPORT.md) 與驗證資料記錄。本文不以作者計數表單獨
代替本輪候選圖的結構和完整染色重算。

本輪未逐條形式化外部生成演算法，也未重播既有 Dvořák–Lidický 的外部
計算證書。後者只用於 §1 的既有十二內點界；對十三內點 `2k+4=30`，不能
套用其「少於三十」界。十九點球面 T 也不是那個三十點 near-cubic 對偶。

## 7. 完整關係驗收如何推出有界等式

對每個 root 刪除圖 G，固定原 B 的十份 canonical proper 四色指派。
逐份枚舉 G 的全部延伸；接受列保存全部完整 lifts，拒絕列保存空列表並由
另一套回溯完整重算。完整搜尋因逐點列舉可用的四種顏色而有完备性：每份
proper coloring 在其前綴所對應的搜尋分支唯一出現；只剪去已違反原邊的
前綴，故不漏有效 lift。主 checker 和獨立 checker 的不同搜尋順序／資料
結構不是兩份局部關係，兩者都重算**同一整張圖**的十列完整 fibres。

實際主 checker 與獨立 checker 比較全部 306 份 root 刪除圖：每一份 mask
均為 **1023**，即全部十列接受，合計 3,060 份接受 fibres、41,021 份完整 lifts。
沒有被截斷的接受列或未查的拒絕列；這批圖的拒絕 fibres 數確為零。
另有含拒絕列的小型校準圖核對空 fibres 與 D5 變換，不以這批全 mask 圖
掩蓋拒絕／搬運程式未觸發的分支。十份 D5 frame 的完整映射分別保存；
41,021 的數目只計各 root 的指定 canonical B，不重複乘以十個 frames。

其中 h=4 有 41 份 roots（39 份無 C chord、2 份一條 chord），h=5 有四份
roots（每份兩條 chords），h=6、7 沒有 roots；以上涵蓋表與 §5.1 的全部
內側分類、具名配置映射一致。這些 graph counts 是包含重複同構 roots 的
證書份數，不能與 27+1 份內側 apex placements 或 26 個 rooted 同構類混用。

1023 屬於固定 K132，所以 §5 覆蓋的全域最小目錄外 G 也在 K132，矛盾。
由每個 K132 元素已有至多五內點 witness，得到

\[
K_{\le13}=K_{\le5}.
\]

這個採納同時依賴全部來源選擇、四分支、sphere 生成及 root／D5 覆蓋、
每份完整關係的獨立驗證；其實際執行紀錄以 [REPORT](REPORT.md) 為準。
在此明列的紙面／外部生成／本輪有限驗證信任邊界內，沒有尚未覆蓋的
h=4、5、6、7 十三內點域。
結論是一般目錄外來源至少十四內點，不是一般 h≥4、`K_{≤14}=K_{≤5}`
或 `K∞=K_{≤5}`。本包沒有新增 Lean theorem。
