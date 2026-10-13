# C8 同側識別的 pocket 化約

2026-10-13。只屬本獨占 audit。直接工作樹輸入及 SHA 見
[INPUTS](../INPUTS.json)；未把未提交的前輪報告當成 BASE 內容。

## 1. 精確契約

沿用全域最小目錄外 C5 disk 的內點數 k；本 h=3 分支有 k≥19。
原 H 有 k 個總頂點，外面為具名 induced C8
`(b0,b1,b2,b3,b4,b5,b6,b7)`。保留原圖、原環序、完整四色關係與同一
literal 色框。既有下降引理保證至多 k+5 點的 loopless planar 圖可四色。
八份 U 只是 `Σ_C8(H)⊆U` 的必要上界。

本論證的共同 gadget 域為：在原 C8 的同一空側，畫一份 boundary-pin
equality scaffold，以及普通不等式邊和私人頂點；只識別原 C8 pins，
不識別其他原 H 點。等式的 connected components 給一份 independent
noncrossing partition π，淨省 d 點；等式 scaffold 可取同側 chord forest。
所有不等式與 scaffold **同時**有指定 disk drawing，收縮後無 loop。
私人點數為 a，且 `a−d≤5`。重邊保留其幾何角色，但不改 proper colouring。
此處不把別的原面、任意 list constraints 或未知可畫性納入契約。

欲排除某 U，需要一份 gadget G 的完整原環 pullback 關係 R_G 滿足
`U∩R_G=∅`。以下使用 **R_small⊆R_G** 的較強 gadget；若 G 拒絕 U，
small gadget 也拒絕 U。只聲稱完整關係包含，不聲稱替換前後的 fibres
或計數相等；私人指派不可由不同列拼接。

既有 [signed 結果](../frozen/audits/2026-10-13-c8-joint-gadgets-6943561/search/SIGNED_RESULTS.json)
覆蓋 C8 三角化 disk、至多五私人點、全部 boundary chords 的 Eq／Diff
指派及全部 16 個環序對齊，八份 U 均沒有拒絕。使用該結論時仍保留
前輪 plantri 完備性依賴；本輪沒有重跑那個大域。

## 2. 收縮外圈是 cactus，面長度總和仍為八

在實際共同 drawing 中取 Eq chord forest T。其 d 條弦把 exterior disk
切成 d+1 份。收縮各 tree component 後，原 C8 邊形成一份 connected
plane multigraph Q。每個 pocket 的 boundary 為 simple cycle，允許兩條
平行原環邊構成的 digon。

可逐弦證明：加入一條 tree chord 時，兩端尚未同一 Eq component；
它切開一份原 complementary face。收縮此 chord，恰把該面環在兩個
不同端點黏成兩個 cycle，只共用新的具名商點。不同 blocks 的非交叉性
保證後續識別不會把已有不同 cycles 的開弧交錯黏合。等價地，依每個
block 的 consecutive terminal gaps 分解原環：每條原 C8 邊屬於恰一份
pocket cycle，任兩個 cycles 至多共用一個商點，block incidence 為樹。
因此 Q 是 cactus；其 cycle 數為 `8−(8−d)+1=d+1`。

某 pocket 不可能有零條原環邊，否則 T 有 cycle；不可能只有一條 uv，
否則 forest 中的其餘路徑識別原相鄰 pins u,v，造成 loop。故各長度≥2，
而全部原 C8 邊恰被用一次，長度總和為八。唯一可能的無序 profiles 是：

| d | pocket 長度 |
| ---: | --- |
| 0 | (8) |
| 1 | (2,6)、(3,5)、(4,4) |
| 2 | (2,2,4)、(2,3,3) |
| 3 | (2,2,2,2) |

每個私人點與不等式邊按原 drawing 落入一份 pocket；它們不能跨過
scaffold 或原環。pieces 只在具名商 boundary points 相接。固定一份原環
literal row 後，完整私有 lifts 是各 pocket fibres 的 Cartesian product，
共用 pin 直接使用該 row 的同一色值。這是同列 full join，不是邊緣關係
的獨立成功。任意選一份抽象 chord fan 的有限控制只核對 partition 組合；
實際來源的分面必須使用其共同 drawing，不得以新 fan 穿過舊 gadget。

## 3. C2／C3 免費；C4 至多一點的較強關係

C2 pocket 的兩個 boundary pins 因原邊而異色，C3 pocket 的三個 pins
兩兩異色。各自的 proper boundary assignments 只有一個全域 S4 orbit。
局部 pocket graph 至多 a+3≤11 點，且 loopless planar；相對可染性給
一份完整染色。全域換色把它送到任意指定的 proper pin colours，因此
每份 proper row 都有 full lift。刪去其所有私人點保持 boundary relation，
但通常不保持 full lift 數量。

對 C4 pocket，私人點數 s≤8<k。既有 **受限** C4 引理只在 s<k 下給
七個完整 masks `7,10,11,12,13,14,15`；不可改稱任意大小 C4 定理。
原 C4 pattern order 為 `0101,0102,0121,0123`。下表選一份非空子關係：

| 原完整 mask M | 選定 mask S⊆M | 所需新點 |
| ---: | ---: | ---: |
| 7 | 7 | 1 |
| 10 | 10 | 0 |
| 11 | 10 | 0 |
| 12 | 12 | 0 |
| 13 | 12 | 0 |
| 14 | 10 | 0 |
| 15 | 10 | 0 |

mask 7 是四輪 W4；mask 10／12 分別是在指定四環上加其中一條對角線。
它們都畫在同一 pocket，不改 boundary names；同一 literal row 的 S
完整延伸必屬 M。故為了尋找空交拒絕，C4 pocket 可強化到至多一私人點。
不需要原 mask 14 的三點**精確**代表，也不把 subset 偷寫成 equality。

C5 pocket 的 s≤6<k；由全域最小性其完整關係在 K132，已有至多五內點的
同 boundary disk witness。此步保留完整關係，仍不保證 fibre counts 相等。
其 drawing 可放回原 pocket，與其餘 pieces 共用原具名 pins。

## 4. 強化後確實落入舊 signed 五點域

先在每個 cactus pocket 內作上述替換，再把商 boundary points 依**原**
scaffold drawing 展開成原 C8 pins。每個 pocket cycle 的 merged vertex
展開為沿該 face boundary 的 Eq-tree path；incident 不等式邊可在其原面角
接到此 path 的任一適當原 pin。path 上所有點被同時識別，故此展開不改
原環 pullback 關係。新私人點數等於各替換 pocket 的總和。

得到一份含 C8 與原 Eq forest 的 simple disk drawing；重複不等式邊可
去重，不改染色。把 Eq forest 暫時當普通 geometric edges，依既有同點集
增廣引理補成 C8 disk triangulation。保留已有 Eq edges；新 boundary chord
若两端在同一 π block，標 Eq，否則標 Diff。所有其他新增邊標 Diff。
沒有新 Eq block，也不把同 block 的 chord 標成 Diff，所以收縮後無 loop。
新增邊只縮小 pullback 關係。若強化後用至多五私人點，便是一份舊 signed
完備域中的合法構造。其與 U 相交，迫原 G 與 U 相交。

由 profiles 與 a≤5+d：

| profile | 原 a 的上限 | 化約後所需新點上限 |
| --- | ---: | ---: |
| d=1：(3,5) | 6 | 5 |
| d=1：(4,4) | 6 | 2 |
| d=2：(2,2,4) | 7 | 1 |
| d=2：(2,3,3) | 7 | 0 |
| d=3：(2,2,2,2) | 8 | 0 |

**化約結論。** 在 §1 的同側、boundary-pin-only 域中，七、八新點的
gadget 不會給八份 U 新的空交拒絕。六新點只可能在 d=1、profile (2,6)
且全部六點位於 C6 pocket 時尚未被上述化約覆蓋。若 digon 中至少有一點，
清空該 pocket 後 C6 至多五點，亦已落入舊 signed 域。

## 5. 六點 C6 中低度私人點與外圈弦仍可處理

先說明 §4 展開所需的更一般接口。若在實際 exterior drawing 中再收縮
一條合法面內弧，原 C8 images 仍形成一份 plane cactus K，並保留原
H-side boundary word。對 K 的每份 pocket，記錄其全部普通邊、私人點與
cycle 上的面角次序。可在實現相同原 pin partition 的 boundary chord
forest 各 face 中重畫這些 **同一具名 pocket graphs**，再將每個 merged
boundary vertex 展開為該 face boundary 上的 Eq-tree path，接邊仍按原
面角排序。收縮這些 paths 後，得到同一 pocket graph、同一 pin map 與
同一完整 pullback 關係。這是重新構造 quotient 的 disk realization，
不是把固定 scaffold 作可能穿過舊邊的 isotopy；其他原 H 點不被移動或
識別。若兩個私人點合併，合併點仍普通私人點；若私人點併入 boundary，
其所有 incident edges 留在該 boundary image 的原 exterior 面角內。

令 P 為 §4 唯一剩餘 C6 pocket，恰有六私人點。可以同點集补邊三角化；
完整關係只縮小。如果 P 是拒絕 U 的候選，任一這樣的強化仍拒絕 U。

私人點 v 度至多三時，每份 P−v 染色可接回 v，故刪 v 保持關係，
只有五私人點，落回舊 signed 域。

私人四度點 v 的原 link 是四個不同鄰點的原四環
`u0,u1,u2,u3`。兩對 opposite neighbors 不可能都已有邊，否則 v 及
其鄰點形成 K5。選一對沒有原邊的 opposite neighbors，在刪 v 後的原
面內加 Eq 弧並收縮。此商圖 loopless、planar。其任一染色拉回 P−v，
四鄰只用至多三色，故可接回 v；因而商圖關係包含於 P 的關係。
此處只用一份合法分支的支援包含，不需要把兩分支計數相加。

若兩鄰都是私人點，刪 v、再併一點後有四私人點；若一鄰私人、一鄰
boundary，也有四私人點。若兩鄰都是 boundary，有五私人點，且原
boundary partition 多省一點。沒有原 C6 邊連這兩鄰，因此原 C8 image
的邊也不成 loop；原 H 的 C8 induced 性排除額外原 H 邊成 loop。
由本節重構接口，每種商圖都有至多五私人點的 boundary-scaffold
realization，再依 §4 強化，與任一 U 都相交。故六點直接拒絕候選的
三角化中，每个私人點必须度至少五。

若 C6 三角化有 boundary chord，該 chord 分成 C3+C5 或 C4+C4。
每份私人點數 s≤6<k；用 §3 清空 C3、以五點精確代表替換 C5，或用
至多一點的子關係替換各 C4。兩側在同一原 chord 的兩端共用同色值，
私人點總和至多五，落回舊 signed 域。所以尚未被處理的候選可限為
**外框 C6 無弦、六個私人點度均至少五的 disk triangulation**。

## 6. 六點私人核心的兩個結構入口

對此 C6 三角化 P 記私人集合 I，`|I|=6`；eII 為私人間邊数、eIB 為
私人到 boundary 的邊数，q 為 boundary chords 數。Euler 給總邊
`3·12−6−3=27`，所以

\[
e_{II}+e_{IB}=21-q,
\qquad \sum_{v\in I}\deg_P(v)=2e_{II}+e_{IB}\ge30,
\qquad e_{II}\ge9+q. \tag{1}
\]

本節候選已有 q=0。若每個私人點都有 boundary neighbor，在原 drawing
中每個私人點都接觸 P[I] 的 unbounded face：否則某個 P[I] cycle 會把
它與原 C6 分開，其 boundary edge 將穿過此 cycle。故 P[I] 是 outerplane，
六點 outerplanar 邊界 `eII≤2·6−3=9` 與 (1) 合起來给

\[
e_{II}=9,\qquad e_{IB}=12,\qquad
\deg_P(v)=5\quad(v\in I). \tag{2}
\]

因此其私人核心是六點 maximal outerplane graph，外面為 simple C6。
每私人點仍有 boundary incidence，故私人核心最大度至多四。
若存在一個私人點 v 完全不接 boundary，它至多接其他五私人點；度至少
五迫它恰接全五點。原三角面在其 rotation 中給五鄰環，故這六私人點
含一份 deep W5，中心及環都是實際具名頂點，環內只剩中心及原 spokes。
鄰環外側仍可能有原 chords；本論證沒有把這個 W5 稱為 induced。

兩種入口是「每私人點均接原 C6」及「至少一個 deep wheel 中心」。
沒有假設原 C6 邊界度數至少四；(2) 只給 boundary 總度二十四，不能
把平均四寫成逐點至少四。因此不能直接 cone 後套用 min-degree-five
的十三點球面分類。上述兩型尚未被本輪完整測試或排除。

## 7. 下一個具名入口

剩餘 Eq 恰為 `b_i=b_(i+2)`，i=0..7。digon 為
`(b_i,b_(i+1))`；C6 pocket 的有序 boundary 是
`(b_i,b_(i+3),b_(i+4),b_(i+5),b_(i+6),b_(i+7))`，下標模八。
不能忘掉 digon pin `b_(i+1)`：它仍與 shared pin 異色，完整 C8 rows 及其
原 indices 必须保留。證書逐列保存 equality 適用性、literal C6 word、
唯一一次全域正規化的 colour bijection，以及每個 C6 row 的完整 C8 preimages。
這是對**明確 pocket factorization**的介面轉移，不是用一般 projection
替代未知原 H 的 full lifts。

此論證收窄 gadget 方法的剩餘域；沒有刪去八份 U，沒有構造未知原 H，
沒有新的 same-source count contradiction。一般 `K∞=K≤5`、無界三支與
Lean 均仍 OPEN／未做。plantri 依賴只出現在引用舊 signed 域的無拒絕時；
pocket 拓撲及 C4 子關係論證是紙面引理，有限控制不代替任意 drawing 證明。
