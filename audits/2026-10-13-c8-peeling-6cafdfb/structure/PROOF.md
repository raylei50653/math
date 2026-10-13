# C8 原圖剝層：外面 walk 的三型、十內點校準與遞迴契約

2026-10-13。BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`。
本文件是任意有限大小的紙面結構證明；小型圖計算另在校準子包，不能代替
本文件的普遍論證。本文件不斷言任何局部候選已由原 933／941 最小來源實現。

## 1. 原前提與具名分類資料

沿用 frozen upstream 的同一原圖 G、同一 C8=(c0,...,c7)、內側 H 與
I=V(H)\C8、Q=H[I]。C8 induced，H 是簡單三角化 disk，
d_H(c_i)>=4，d_H(v)>=5 對 v∈I；原內部 C4 cap 空，C5 cap 空或 W5。
另須明列上游的 **無 occupied C3**：任一完全在原 B 內側的三角形所指定
不含 B 的 disk 側無嚴格內點。它已由原全域最小來源得到，見 frozen
`audits/2026-10-13-c8-struct-243a125/geometry/PROOF.md` §1，及
`audits/2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md` §1、§4。
「每個 I 點至多接兩個 C 點」本身不包含這個 C3 前提。

上游已證：每個 I 點至多接兩個 C 點；雙接只可為相鄰或正對；
各原 C 邊 c_i c_(i+1) 的面第三點 t_i 全部相異。下標模 8。

若 x 同接 c_i、c_(i+1)，原三角形 c_i c_(i+1)x 的內側若不是原面，
便包住原面第三點 t_i，違反無 occupied C3。因此 **相鄰雙接點恰為 t_i**，
不會有未列出的相鄰雙接點。

記 S1 為恰接一個 C 點的原內點，s=|S1|；S2 為正對雙接點，p=|S2|；
R 為無 C 接點的原內點，r=|R|。所以

\[
 I=\{t_0,\ldots,t_7\}\mathbin{\dot\cup}S_1
   \mathbin{\dot\cup}S_2\mathbin{\dot\cup}R,
 \qquad m=8+s+p+r.                                      \tag{S1}
\]

所有名字、接點、rotation 及下文的 disk 側均來自這一原圖，不逐列改名。

## 2. LINK-WALK：C 接點精確等於 Q 外面點

在 c_i 的原內側 rotation 中，I 鄰點是一條無重複的 link path

\[
 P_i=(t_{i-1},v_{i,1},\ldots,v_{i,a_i},t_i).              \tag{S2}
\]

相鄰點間的 Q 邊及與 c_i 的原三角面均實際存在。d_H(c_i)>=4 與 t 全異
保證兩個端點不同。沿 C 的順序把八條 path 在共同端點 t_i 黏合，得到
cyclic walk W；共同端點只算一次 occurrence。

**LINK-WALK 定理。** Q 連通，全部有界面是原 H 三角面；W 恰為 Q 的完整
外面 boundary walk（可有重複點或重複邊）。Q 的外面點集合精確是
S={t_i}∪S1∪S2。在 W 中，t_i 與 S1 點各出現一次，S2 點各出現兩次；
R 點不出現。特別有

\[
 |V(W)|_{\rm distinct}=8+s+p,\qquad |W|=8+s+2p.          \tag{S3}
\]

證明：每條 P_i 連通，連續 P_i 共用 t_i，故全部 C 接點在同一 Q component。
每個 Q component 必含 C 接點：否則 H 的連通路首次離開該 component 時既不能
用 Q 邊也不能用 C 邊。這證明 Q 連通。Q 的任何有界面都在 C 內側；刪除的
C 頂點全在該面的外側，而 Q 保留所有 I 點與它們間的原邊，因此其有界面
仍是 H 三角面。另一方面，Q 每條外面邊的每個暴露側在 H 有一個三角面；
該面第三點必在 C，否則 Q 已在這側有界三角面。故其暴露側唯一出現在
相應 P_i 中。每個 Q 外面點有一條外面 incident 邊，因為
d_Q(v)=d_H(v)-|N_C(v)|>=3；因此它必接 C。反向上，原 C-I 邊從 Q 外面
到 C，證明接 C 的點 exposed。逐暴露側的唯一對應證明 W 完整且不漏邊側。
最後，t_i 只在相鄰兩條 P 的共同端點，單接點只在一條 P，正對點只在
兩條 P 的嚴格內部，得到 occurrences 與 (S3)。

**外面重複引理。** 在此連通 Q 中，一個外面點是 cut vertex 當且僅當
它在 W 中重複。若出現 q 次，Q-v 恰有 q 個 components。
局部證明：每個有界面角是三角面，角的兩個鄰點由該三角面的對邊相連。
因此同一對連續外面角之間的全部鄰點，在 Q-v 中形成一個連通 run；任何
Q-v component 必含 v 的鄰點。不同外面角所分隔的兩個 runs 若在 Q-v
仍相連，該路與 v 的兩條 incident 邊形成簡單環，會把兩個原外面角放在
環兩侧，與它們同属無界面矛盾。故 components 與外面角一一對應。
這個證明只用原三角面與 disk 分隔，沒有假設 Q 原先二連通。

因此 **Q 的 cut vertices 精確等於 S2，且每個正對雙接點的 cut-order 恰二**。
沒有額外隱藏的 branch 點；單接點與 t_i 都不是 cut vertex。

## 3. OPP-SAME-PAIR 與三個完整外面型

對 x∈S2，兩條原邊 c_i x、x c_(i+4) 是 H 中的一條簡單 disk crosscut。
若另一正對點 y 使用不同 antipodal pair，四個 C 端點在 C 上交錯，兩條
內部不相交的 crosscuts 不可能同時存在：第一條已把 disk 分成兩側，第二條
的端點位於不同側。故所有正對點必使用同一 pair {c_i,c_(i+4)}。

若有兩個 x,y，原 C4=(c_i,x,c_(i+4),y) 的不含 C 其餘點的側是空 cap。
它的對角線不能是 C chord c_i c_(i+4)，所以必為 xy；兩個原面恰為
c_i x y 與 c_(i+4) x y。刪去 C 後 xy 的兩側均為 Q 外面，故 xy 是 Q bridge。
若有第三個正對點，逐對相同論證會迫三條 Q bridge 成三角形；三角形中的
邊不可能是 bridge。因此 **p<=2**。

下列三型對任意 m 完備，並保留相鄰／正對接點的原名字：

| 名稱 | 精確適用條件 | Q 外面與原子 disk |
|---|---|---|
| **C8-LINK-RING** | p=0 | W 是長 8+s 的簡單環；Q 是以此環為外框的三角化 disk，允許 boundary chords。 |
| **C8-LINK-PINCH(i;x)** | p=1，N_C(x)={c_i,c_(i+4)} | Q 是兩個非平凡三角化 disk 在同一原點 x 的一點黏合；兩個簡單外環各含該半弧的四個 t 及 x，長 5+s_+、5+s_-。 |
| **C8-LINK-BRIDGE(i;x,y)** | p=2，兩點同接 {c_i,c_(i+4)} | Q 有唯一 bridge xy，兩端各接一個三角化 disk；terminal 外環各含四個 t 及其 endpoint，長 5+s_+、5+s_-。外面 W 走 xy 兩次。 |

其中 s_++s_-=s；正負側以原 C 的兩條 i 到 i+4 半弧命名，bridge 型另以
原 rotation 指定哪個 endpoint 在哪側。不能把两個 terminal disk 各自
重新旋轉、改色或交換後認作同一原附件。

完整性理由：LINK-WALK 已定位全部 cut vertices。p=0 無 cut，且 Q 至少
八點、最低度至少三，故其外面 walk 無重複，是簡單環。p=1 的唯一 cut
分成兩 components，且每個半弧有四個不同 t，故不是單 edge block；把 x
放回每個 component 得到無其他 cut 的三角化 disk。p=2 時 xy 是 bridge，
刪去它正好剩兩 terminal components；若有其他 block、bridge 或附枝，必
產生第三 cut 或使 x／y 的 cut-order 大於二，均已排除。

故原 C8 第一剝層的 **simple-cycle iff p=0** 是任意大小定理。分支恰為一個
正對 pinch；重複邊恰為兩個正對點之間的 bridge。圖形的概括「Q outerplane」
不能代替本表：R 點可以在 terminal disk 的严格内部。

## 4. 两 terminal disk 必各有严格內點

PINCH／BRIDGE 的每個 terminal disk 外環除其 distinguished endpoint
x 或 y 外，所有點在 Q 中最低度至少三（t 點）或四（S1 點），且沒有別的
block 鄰點。因此它們在 terminal disk 中也具有同一最低度。若該 disk
沒有严格內點，它是三角化 polygon。polygon 至少有兩個耳，至少一耳不是
唯一 distinguished endpoint，該點在 Q 的度數恰二，矛盾。

耳論證可直接由 polygon 三角面的對偶樹得到：樹的兩個 leaf triangles
各給一個耳；相鄰外環點不能同為耳，否則所需對角線交叉。這也覆蓋三角形。
所以每個 terminal 至少一個 R 點，由 (S1) 得

\[
 \text{PINCH}:m\ge11+s,\qquad
 \text{BRIDGE}:m\ge12+s.                                \tag{S4}
\]

這是小規模校準前的紙面下界；不靠程式生成出零個圖。

## 5. m=10 的紙面完備分類

由 (S4)，m=10 必是 RING，p=0。其簡單外環 D 長 n=8+s；所有 D 點
在 Q 中至少度三，而 S1 點至少度四。Q 的 r 個严格內點就是 R，均至少度五。

若 r=0，Q 是 outerplane 三角化 polygon，有度二耳，矛盾。若 r=1，任何
D chord 的一側無严格內點；該側空 polygon 有一個不在 chord endpoints
的耳，因 endpoints 在該 polygon 上相鄰，該耳在整个 Q 度二，矛盾。
故無 chord，三角化迫唯一中心接全部 D 點，所有 D 點度三。因此不能有
S1；但 m=10 與 r=1 又迫 s=1，矛盾。故 **s=0、r=2**。

寫 R={u,v}，D=T=(t0,...,t7)。三角化 disk Euler 給
|E(Q)|=3r+2|D|-3=19。三類具名候選如下。

**C10-EDGE(a;d)**：T 無 chord，uv 是原邊；uv 的兩個原面第三點為
t_a、t_(a+d)。u 接弧 t_a,t_(a+1),...,t_(a+d) 的全部點，v 接補弧的
全部點（兩端各共同接 u、v）。d=3,4,5；
d_Q(u)=d+2，d_Q(v)=10-d。反射／交換中心辨出兩種未具名同構型
**EDGE-3/5** 與 **EDGE-4/4**，但 literal 判定保留 a、d、u、v 及 rotation。

证明：若無 uv 且無 T chord，每個三角面只能使用一條 T 邊及一個中心，
至多八個面；Euler 所需十個面，矛盾。uv 兩側的原面第三點在 T，且不同，
其兩條 u/v 路將 T 分成兩弧。沒有其他內點或 T chord，面三角化逐點迫
兩側各是單中心 fan。兩中心最低度五迫 3<=d<=5。

**C10-CHORD(a)**：唯一 T chord 是 t_a t_(a+4)，它的兩側各為原 W5；
u 接一個長四 T 弧的五個環點，v 接另一弧的五個環點，uv 不存在。
未具名同構型名 **CHORD-4/4**。

证明：任一 T chord 的每側都必含嚴格內點，否則空側有非 endpoint 耳，
違度至少三。因此它分開 u、v，uv 不能存在。若 q 為 T chord 數，Euler
使中心到 T 的邊數為 11-q；兩中心度至少五使 11-q>=10，因此 q<=1。
有 chord 時恰 q=1，兩中心度恰五。各側僅一中心，無其他 chord，必為
wheel，兩側外環長各五，迫 T chord 正對。

這證明 **m=10 的局部原 H 候選只有上述三個未具名型及其具名位置**。
判定仍須回接八個原 B-to-C collars，保留完整十列、全部空 fibres、同一
色框與 literal full lifts；本節的結構分類並不把候選認作實際來源。

## 6. 任意大小剝層能保證甚麼，以及不能照搬的具名障礙

本次第一層能任意大小剝去原 C，得到上表三型。RING 可把 D 作下一個
**具名 separator**；PINCH 可把兩個具名外環及其共同原點作 separator；
BRIDGE 須另外保留原 bridge xy 及共同端點的同色一致性。對每一 terminal
disk，可再刪除它的完整外面點集合，對所得每個連通 component 按原
rotation 取新的外面 walk。有限原圖每次刪除非空集合，因此這個
**保留具名外面 walk 與所有 attachment edges 的一般剝層**適用於任意大小，
且不遺失 vertex／edge；完整染色轉移須使用主報告的 separator full-fibre
join，不可只保留外環某些 feasibility marginals。

**TRIANGULAR-PEEL 引理。** 設 K 是任一輪保留下來的連通原誘導子圖，
全部有界面均為原三角面，S_K 是其完整外面點集合。刪除 S_K 後，每個
非空 component K' 仍是同一原 embedding 的誘導子圖，全部有界面均為原
三角面；K' 的外面點精確是 K' 中接 S_K 的點。

證明：被刪的 S_K 點原來 incident 於 K 無界面，不能在任何 K' 簡單環
內側。因此 K' 有界面內沒有被刪頂點，亦沒有其他 component 的原頂點：
若有後者，其在連通 K 中通往 S_K 的路必先穿過 K' 的該面邊界，但
K' 與其他 component 無原邊。故所有該面的頂點及邊均完整保留，仍為
原 K 三角面。反向上，一條 K'-S_K 原邊可沿原 S_K 外面角通向外側，
不穿過 K'，故其 K' 端點 exposed。若 K' 外面點 incident 於 K' 外面邊
ab，ab 在 K 中不是外面邊（否則 a,b 已在 S_K）；所以 ab 的每側在 K
原有一個有界三角面。其新暴露側第三點必被刪至 S_K，否则該原三角面
仍在 K' 這側形成有界面。這證明該端點接 S_K。若 K' 是孤點，它在連通
K 中必有鄰點，而所有鄰點已被刪，亦接 S_K。

引理從 Q 及上表各 terminal disk 開始歸納，給任意大小的實際逐層
三角面分解，非只把任意 graph 算式改名為剝層。每輪保留各 component
具名外面 walk 的全部 occurrences 與到前層的全部原邊；新 walk 可有任意
重複點／邊。孤點、單邊或沒有严格內點的 component 其全部點已 exposed，
在當輪刪完，以原邊 properness 或空圖唯一 colouring 作為轉移終端。
這個引理不保證後續 frontier 的度數下界、簡單環、固定長度或接點數上限。

但是「下一層仍是 induced C8、boundary degree>=4、每點最多雙接」的
同型反覆剝層**沒有證得，且不能由本契約推出**。以下七項具名障礙由
m=10 結構候選及獨立具名小圖控制显示；它們是局部契約控制，不是实际
933／941 最小來源。

| 障礙 | 具名觸發與缺失前提 |
|---|---|
| **OPP-PINCH** | C8-LINK-PINCH 的原 x 重複出現在 W，無單一簡單內環；須共享同一 x 的色值做兩 disk join。 |
| **OPP-BRIDGE** | C8-LINK-BRIDGE 的 xy 在 W 出現兩次；须保留 x≠y 顏色約束與兩 endpoint 原 attachment。 |
| **DEGREE-LOSS** | C10-EDGE 的非共同端點 t 在 Q 度三，已不滿足下一圈 boundary degree>=4；上游短弧排除的矛盾不再成立。 |
| **CHORD-INHERITANCE** | C10-CHORD 的下一個 T8 有原 chord t_a t_(a+4)，因此 induced-boundary 前提不傳遞。 |
| **MULTI-CONTACT** | C10-EDGE(a;3) 的 u、v 分別接 T 的四、六點；C10-EDGE(a;4) 各接五點。下一層 at-most-two 前提失效。 |
| **DISCONNECTED-CORE** | C10-CHORD 刪去 T 後只剩不相鄰的 u、v，兩個 components；單一 inner disk 前提失效。 |
| **WIDTH-GROWTH** | 具名 `M11-WIDTH` 的 z 只接 c0，剝去 C 後 exposed 簡單環是 D=(z,t0,...,t7)，長九大於八；固定 C8 frontier 長度不傳遞。 |

WIDTH-GROWTH 的完整原圖、原面與 rotation 見
[獨立 fixture](../independent/check.py) 的 `fixture("M11-WIDTH")`，其驗收
記錄見 [獨立 certificate](../independent/certificate.json) 同名項目。
Q 的兩中心 r、s 相鄰，共同接 D 的 z、t3；沿 D 的兩弧長為四與五，
分別由 r、s 的原面 fans 填滿。z 在 Q 度四，加唯一 c0 接點使 H 度五；
兩中心度六、七，其餘點也符合原度數界。獨立 checker 已驗證全部原面、
無 occupied C3、空 C4 與空／W5 C5 cap。這只證明在有效局部契約內
frontier 可以從八增至九，**不宣稱任意大 frontier 均已構造或由來源實現**。

一般 walk 剝層只產生 exact separator 算式，並不自動給較小、统一的
四色 relation 型錄，也不证明一列可延伸。固定-size／固定-two-contact
剝層若要成為更強任意大小定理，必須另證這些缺失前提的替代结构引理，
或在同一原色框内完整處理 chords、cut points、components 與多接点。

本文件的任意大小 closure 僅是 **原 C8 第一剝層三型及一般具名 separator
剝層**；無界八個 source contracts 的染色排除仍须由完整 transfer 與另加
結構論證完成，不能以 m=10 校準外推。
