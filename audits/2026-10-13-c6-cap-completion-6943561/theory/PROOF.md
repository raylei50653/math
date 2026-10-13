# 六私人點 C6 cap 的三型完備分類

2026-10-13。本文件只屬本獨占 audit。直接依據本包 frozen 的前輪
`c8-pocket-reduction-6943561/theory/PROOF.md`、`review/CORE_REVIEW.md`
及 `review/PROOF_REVIEW.md`。以下分類有紙面證明及一份很小的直接
生成式；**不使用 plantri 的完備性來證明三型完備**。最終擴充回先前
signed 五點域的推論，仍保留該先前枚舉的 plantri 依賴。

## 1. 精確 cap 契約

P 是 finite simple plane disk triangulation，原外框是具名無弦
`B=(c0,c1,c2,c3,c4,c5)`，恰有六個嚴格私人點 I，且
`deg_P(x)>=5` 對每個 x∈I 成立。所有 bounded faces 皆三角。
度數指 P 中的不同鄰点數，並非未知原圖 H 的度數。沒有假設任何
boundary pin 的度至少四。

**分類定理。** 保留外框的 cyclic order，容許 boundary rotation／
reflection 及私人點改名時，這樣的 P 恰有三型。兩型的私人核心是
六點 maximal outerplane graph；第三型的私人核心是 induced W5，
其 deep 中心唯一。每型到原外框的全部實際接線由下文明列。

這裡的「恰有三型」是 plane cap 的分類，不是未知原 H 的實現定理。
原 C8 的八個短 Eq、八份 U 與原列 indices 仍須逐一作完整 pullback
檢查，不能由這個無標號數目直接宣布沒有拒絕。

## 2. 全接框分支的核心

令 Q=P[I]，eII=|E(Q)|，eIB 是私人到 B 的邊數。Euler 給

```
|E(P)| = 3*12-6-3 = 27,
eII+eIB = 21,
30 <= sum_{x in I} deg_P(x) = 2*eII+eIB = 21+eII.
```

所以 eII>=9。若每私人點都有 boundary neighbor，每個私人點都
incident 於 Q 的 unbounded face：沿一條該點到 B 的邊，其開邊不
遇 Q，而 B 在 Q 的無界區域。故 Q 在所繼承的實際 drawing 中
outerplane。六點 outerplane 邊界給 eII<=9，因此

```
eII=9, eIB=12, deg_P(x)=5 for every x in I.
```

達到 outerplane 上界的 simple graph 是 maximal outerplane：
不連通、cutvertex 或非三角 bounded face 都容許再加一條保持
outerplane 的 simple edge，違反上界。故 Q 有 simple 外六環，
且 Q 的各私人點至少有一條接框邊，遂 `deg_Q(x)<=4`。

六邊形三角化有四個三角形，weak dual 是四點、最大度三的 tree，
故只可能是三葉 star 或四點 path。

* Star 型：中間三角形的三條邊各接一個 ear。其三條 diagonals
  形成交替頂點的三角形，核心 degree sequence 沿環為
  `(4,2,4,2,4,2)`。
* Path 型：兩個 middle triangles 合成一個 quadrilateral，剩下
  兩個 ear 分別接在這兩個 middle triangles 的一條外邊。
  若两條接 ear 的邊共端點，該端點會有核心度五，已被排除。
  因此這兩邊相對；只剩一型，沿環核心 degree sequence 可取
  `(4,2,3,4,2,3)`。

這也直接證明六點 maximal outerplane、最大度至多四的核心只剩
上述兩型，不需要借用無標號圖表。

## 3. Deep W5 的中心唯一，鄰環沒有外側 chord

若某私人 z 不接 B，它只能接其他五個私人點；最低度五迫
`N_P(z)=I\{z}`、`deg_P(z)=5`。其原 rotation 的五鄰點
`x0,...,x4` 組成一份 simple 五環，五個 incident 三角面填滿
該環內側，給實際 wheel W5。

下面補上前輪尚未聲稱的 induced 性。Q 已含 spanning wheel，
故 Q 二連通，其 unbounded-face boundary 是 simple cycle。
z 被自己的五鄰環隔在內側，不在此外面邊界上。記 Q 在 wheel
以外的邊數為 t；這些邊只能是五鄰環的非鄰點 chords，並位於
輪的外側。記 Q 的外面長度為 l。

Q 的每個 bounded face 都是 P 的一份原三角面：所有私人點已在
Q，所有原 B 點都在 Q 的無界面，所以任何 bounded face 都沒有
被刪掉的 P 頂點或邊。因此 Euler 給

```
10+t = |E(Q)| = 3*6-3-l = 15-l,
l=5-t.
```

外面 boundary 恰含五鄰點中的 l 個；其餘 `5-l=t` 個鄰點
不 incident 於 Q 的無界面，故不可能有到 B 的邊。每個這樣的
hidden 鄰點在 wheel 中的 degree 是三，而在 P 中至少五，
所以至少需要兩個額外 chord incidences。這 t 個 hidden 點
合共已需要至少 2t incidences，正好耗盡 t 條 chords 的全部
2t 個端點 incidences。因此每條额外 chord 的兩端都必須 hidden。

但若 t>0，則 l<5；Q 的 simple 外面 cycle 不可能只用原五環
邊，因原五環沒有更短的 cycle。因此該外面 cycle 至少用一條
額外 chord，而這條 chord 的兩端都是外面 boundary 上的 visible
點，矛盾。故 **t=0，Q 就是 induced W5**。

每個鄰環點在 Q 中恰度三，最低 P-degree 五迫它至少接兩個
原 B 點。因此所有五個環點都接 B，deep 中心 z 唯一。
現在 eII=10、eIB=11，五個環點的 boundary degrees 至少二，
合計十一，所以恰為 `(3,2,2,2,2)`，其位置容許輪轉。
中心 P-degree 五，四個環點 P-degree 五，餘下一個環點
P-degree 六。這不是把輔助 cap 度數套到未知來源圖。

## 4. Annulus 接線由一個 cyclic word 完全決定

三型私人核心的外面 cycle 分別長 n=6、6、5；原外框長 m=6。
兩環之間是沒有其他頂點的 triangulated annulus。該 annulus
沒有任何同環 chord：原 B 無弦，私人核心的外面已是該 simple
cycle。故每個 annular triangle 有且只有一條環邊，另兩邊
都是跨兩環的 spokes。

以 annular triangles 為頂點、共同 spoke 為 dual edge。每個
triangle 在此 dual 中 degree 二；annulus 連通且每條內側
adjacency 都經 spoke，故 dual 是單一 cycle。沿此 dual cycle
走一圈，每跨過一個 triangle，恰沿 outer ring 前進一步 O，
或沿 inner ring 前進一步 I。可同時選兩環的 cyclic orientation
使兩種步皆向前。每份原環邊用恰一次，故 word 有 m 個 O、n 個 I。

對 inner vertex xi，令 r_i 是相鄰兩個 I 步之間 O 的個數。
若第一份 spoke 接 `(xi,c_s)`，則 xi 的全部 boundary neighbors
依次且恰為

```
c_s, c_(s+1), ..., c_(s+r_i),
```

然後下一個 inner vertex 從 `c_(s+r_i)` 開始。因此

```
deg_B(xi)=r_i+1,   r_i>=0,   sum_i r_i=6.
```

不會有 r_i>=6，否則 dual traversal 在走到下一個 inner
vertex 之前已重複同一條 spoke，違反它是 simple adjacency
cycle。這同時排除把接框鄰點數偷偷當成有重複的 boundary walk
長度。所有下列 r_i 更直接地都至多二。

反過來，給定這些 r_i，從 s=0 開始依該規則加入 spokes，
再令 `s←s+r_i (mod 6)`，便重建所有 annular triangles。
因此同一私人 cyclic order 及同一 r-vector 的 annulus 唯一，
只剩整體 boundary rotation／reflection。這裡沒有只保存
各點度數：公式保存每一條具名 attachment 及其 rotation。

## 5. 三份完整代表

外框一律是具名 C6 `c0,...,c5`。私人點為 `x0,...,x5`；
所有列出的下標按其環長取模。每型都保留外六環的六條原邊。

| 型 | 私人核心 | 核心外環順序 | r-vector |
| --- | --- | --- | --- |
| A | 私人 C6 加 chords `x0x2,x2x4,x4x0` | x0,...,x5 | `(0,2,0,2,0,2)` |
| B | 私人 C6 加 chords `x0x2,x0x3,x3x5` | x0,...,x5 | `(0,2,1,0,2,1)` |
| W | 私人 C5，加中心 x5 接 x0,...,x4 | x0,...,x4 | `(2,1,1,1,1)` |

型 A、B 的公式來自 `deg_P(xi)=5`，故
`r_i=deg_B(xi)-1=4-deg_Q(xi)`。型 W 來自 §3 的五份
boundary degrees，將唯一三份 attachment 的環點命名 x0。

各私人點的**全部具名原 B 鄰點**如下，空白表示不接 B：

| 私人點 | 型 A | 型 B | 型 W |
| --- | --- | --- | --- |
| x0 | c0 | c0 | c0,c1,c2 |
| x1 | c0,c1,c2 | c0,c1,c2 | c2,c3 |
| x2 | c2 | c2,c3 | c3,c4 |
| x3 | c2,c3,c4 | c3 | c4,c5 |
| x4 | c4 | c3,c4,c5 | c5,c0 |
| x5 | c4,c5,c0 | c5,c0 | |

三圖都是 simple chordless-C6 disk triangulations、恰 27 邊，
且六私人點均度至少五。原 B 的 degree sequences 分別為

```
A: (5,3,5,3,5,3)
B: (5,3,4,5,3,4)
W: (4,3,4,4,4,4).
```

故 A、B 由 boundary degree multiset 可區分；W 則有唯一
不接框的私人點。這证明至少三型；前面證明至多三型，分類完成。
每型都存在 boundary degree 三，也實際否定了直接加 cone 後
套用十三點最低度五球面分類的前提。

另一份可機器獨立生成的等價 recipe 是：枚舉 labeled hexagon
全部三條兩兩不交的 diagonals，保留 max core-degree<=4 的
triangulations，按 `r_i=4-deg_Q(xi)` 補 spokes；再加唯一 W 型。
有限核對應驗證每份結果確實同構於 A、B、W，而非從 plantri
的輸出反推這份 recipe 完備。

本輪獨立實作重算全部 14 份 labeled hexagon triangulations，
其中八份通過 max core-degree<=4；加上五份 wheel 特殊環點
位置，合共十三份直接 annulus 參數列。依 C6 dihedral 與
私人改名比較，恰得 A、B、W 三個 classes，並與證書圖集相等。

## 6. 原 C8 完整 pullback 與有限核對義務

保留原 C8 頂點名 `b0,...,b7`、原 274 份 canonical rows
及八份 U 的原 indices。對每個 i=0,...,7，原短 Eq 是
`b_i=b_(i+2)`，其 C6 pocket 的具名順序是

```
(b_i,b_(i+3),b_(i+4),b_(i+5),b_(i+6),b_(i+7)).
```

還有 digon pin `b_(i+1)`；它必須留在完整 C8 row 中，且因
原 C8 properness 與共用 Eq pin 異色。任何 cap alignment
只作用於這六份具名 C6 pins，必須保留原 Eq 與完整 C8 row。
每型保留全部 12 份 D6 alignments 是充分覆蓋；因 automorphism
產生重複是允許的，不能在不知道原 row map 的情況下合併。

對每一份原 C8 row，若 Eq 不成立，pullback fibre 為空；
若成立，抽取上述六個**原 literal 色值**並按指定 alignment
測全部 `4^6` 份具名私人 assignments。其完整 tuple set
就是該 row 的 cap fibre。因 digon 已清空，沒有遺失的私人
指派；它仍保留其原 pin 的顏色及原 C8 properness。

可以先把 C6 word 作一次全域正規化來重用 fibre 資料，但須
保存該次 colour bijection，將私人色名整份反映回原 C8 色框；
不能逐頂點或逐段另正規化。八份 U 各自與同一個完整 pullback
relation 作交集。若每型、每 alignment、每短 Eq、每份 U
均有一份完整原 row 加六私人點的 full lift，就得到

```
for every tested cap G and each j=1,...,8:
    U_j intersect R_G is nonempty.
```

這項新有限核對需由獨立 checker 從原邊、原 row map 和全部
private tuples 重算，包含空 fibres。另跑 plantri 可作獨立
圖集 cross-check；因 §§2–5 已直接完備分類，**新六點 cap
域的完備性不必依賴 plantri**。seed 變序與破損證書拒絕是
有限核對控制，不能代替分類證明或原來源實現。

**本輪已完成的有限核對。** [結果](../search/RESULTS.json)
與[獨立覆核](../review/REVIEW.md)記錄全部
`3*12*8=288` 份具名 cap attachments；與八份 U 的
`288*8=2,304` 份交集全部非空。獨立 checker 重算三圖
93 份 canonical C6 fibres（另直接重算 2,196 份 literal
C6 fibres）、78,912 份 canonical C8 cells，以及經 S4
全色框解碼核對的 1,890,432 份 literal C8 cells，保留全部
完整私人 tuple sets 與空 cells。normal 與 seed17 的
[獨立結果](../review/INDEPENDENT_CHECK.json)、
[變序結果](../review/INDEPENDENT_CHECK_SEED17.json)均通過，
五份破損證書也全部被拒絕。因此本節有限前提已被實際核對，
不是尚待執行的預測。

## 7. 與前輪合併時，能夠關閉的精確方法域

前輪所需背景假設照原樣保留：原 H 有 induced named C8、
`|V(H)|=k>=19`；來源最小性給相對 C4/C5 代表引理與
至多 k+5 點的 loopless planar 可染性；八份 U 僅是
`Sigma_C8(H) subset U_j` 的必要上界。

gadget 的所有新增點、Diff 邊和 Eq scaffold 均同時畫在
這個 C8 的**同一空側 disk**，只識別原 C8 pins。收縮後
有 a 個私人點，原 boundary identification 淨省 d 點，
`a-d<=5`。全 Eq partition 必 independent、noncrossing，
全 Diff 圖收縮後不得有 loop。其他原 H 頂點不參與操作。

前輪紙面化約給 `d<=3`，所以 `a<=8`；a<=5 已由 frozen
signed 域覆蓋。a=7、8 均化回五私人點；a=6 除唯一
`d=1`、`(2,6)` profile 且全六私人點均在 C6 pocket
之外也化回五點。其 C6 有 chord 或低度私人點時，再化回
五點。所以只剩 §1 的三型。

**合併推論（以 §6 全部 finite checks 通過為前提）。**
對以上明列契約中的每份 gadget G 及每份 U_j，
`U_j intersect R_G` 非空。也就是在此預算內、同一空側、
只識別原 C8 pins 的所有合法 gadget 都不能直接空交拒絕
這八份必要上界。引用既有五點 signed 域的那一部分仍有
前輪 plantri 完備性依賴；三型分類及新 cap 的直接生成域
沒有新增這項依賴。

§6 的實際結果及獨立 normal／seed17 覆核已滿足此有限前提，
故上述**精確方法域的無拒絕推論在本輪成立**。這項採納仍
依明列的來源最小性／相對小圈引理，以及先前 signed 五點
域的既有完備性證據；没有把本輪 direct annulus enumeration
說成重跑或取代了那份先前大域。

這是方法域的無拒絕結論，不是八份候選的來源排除，也不是
原 H 的存在。量詞是 `forall G forall j exists row(G,j)`，
不是一份共同 row 同時通過全部任意 gadgets，更不是已知
該 row 属於未知 `Sigma_C8(H)`。多個 gadget 若要同時施加，
合成後仍須核對共同 drawing、總預算與同一 full row。

以下都不在這個方法域內：操作／識別／刪除其他原 H 頂點；
把其他原 H 頂點當成免費輔助點；在其他原面或 C8 兩側共同
接線；增加預算；未知來源的共同計數與 full-fibre constraints；
尚未證明 simultaneous drawing 的任意 abstract attachments。
本分類未建立 same-source realization、主命題、一般
`K_infinity=K_<=5`、無界三支或 Lean 形式化。八項與主命題
必須保留 OPEN，除非另有獨立且足夠的來源證明。
