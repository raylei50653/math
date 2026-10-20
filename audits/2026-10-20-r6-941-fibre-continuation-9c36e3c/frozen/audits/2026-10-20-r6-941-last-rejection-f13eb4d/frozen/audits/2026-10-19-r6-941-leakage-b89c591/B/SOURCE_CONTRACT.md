# 完整 r6／941 原位置來源契約

BASE 及起始 HEAD 同為 `b89c5913cea9df2305845be0f65fa6f1c1aaf55f`。
本頁只使用這個 BASE 的文字；各份字節數及 SHA256 見
[additional-inputs.json](additional-inputs.json)，主凍結表見 [../INPUTS.json](../INPUTS.json)。
下列行號都指 BASE 中的原文件，不把前輪控制向量當成實際來源。

## 1. 全域來源、嵌入及支持

G 是有限、簡單、連同指定外面嵌入的合法 C5 disk，外框順序恰為
`B=(x,y,a,b,c)`。在所有完整支持不屬於 K132 的合法 C5 disk 中，先令
內點數 k 全域最小，再在該 k 中取邊數最大。這是全域來源最小性，並非
某一拒絕列的 edge-critical 最小性。
來源：[SOURCE_GEOMETRY:10–18](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)、
[J 幾何:11–18](../../2026-10-15-j-source-geometry-6ddea32/PROOF.md)。

G 的內面皆三角形；原三角形皆為面；原內點度數至少五，原框點至少四。
每個原 C4 的有界內部為空；每個不同於原 B 的原簡單 C5，其有界內部
為空，或恰有一個原五度點，且該點接該 C5 全部五點。
這些是原全域來源定理，保留其嚴格較小比較前提。
來源：[low-p:22–28](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md)、
[collar:47–53](../../2026-10-14-lowpq-source-676b102/r6/PROOF.md)。

本輪固定原完整支持恰為 941。十列字面順序為

```
01012,01021,01023,01201,01202,01203,01212,01213,01231,01232.
```

因此第 0,2,3,5,7,8,9 列非空，第 1,4,6 列完整 fibre 為空。
所有原框字面值使用同一個四顏色集合；全域色置換搬動整份完整著色。
接受與拒絕是全部實際內點著色的存在或空性，不是邊界局部投影。

## 2. 原附件、完整 stars、原旋轉

原邊 `xy,ya,ab,bc,cx` 的唯一原 apex 依次是 `r,t,p,q,s`。
五點互異，每個 apex 的原 B 鄰點恰為所列兩個相鄰框點。每個原內點至多
接兩個相鄰 B 點。五個非連續 apex 對 `rp,rq,st,sp,tq` 全為原非邊；
`rs,rt,pq` 為原邊；`tp` 存在當且僅當 `d_G(a)=4`，`qs` 存在當且僅當
`d_G(c)=4`。
來源：[SOURCE_GEOMETRY:16–55](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)。

固定原度數及完整 stars 為

```
d_G(x)=d_G(y)=d_G(b)=4, d_G(r)=6,
d_G(s),d_G(t)>=6, d_G(p)=d_G(h)=5,
N_G(x)={y,c,r,s}, N_G(y)={x,a,r,t}, N_G(b)={a,c,p,q},
N_G(r)=(x,y,t,w,v,s),
N_G(p)=(a,b,q,h,n), N_G(h)=(p,q,L,R,n).
```

括號為同一原嵌入的 facial link，容許同時反轉全部方向。h 就是原 pq 邊
上與 `bpq` 不同側的面點 ell。n 是舊 low-p 文件的原點 m，**不是**
J 中的商點 `m=[s=t]`。L,R 就是 active-f p,ell 表的 `u1,u2`。
來源：[原兩商圖:15–28,47–73](../../2026-10-18-smaller-bad-e1617a2/B/PROOF.md)、
[r6 轉移:16–36](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)、
[active-f:28–47,86–99,124–127](../../2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md)。

兩五度中心的原星並集是實際 disk，其簡單六圈為 `(a,b,q,L,R,n)`；
裡面恰有 p,h，沒有遺漏的私有點。原面 `bcq` 接上後，與 B 的交集恰為
原弧 a-b-c，所以補片恰為同一張

```
E=G-{b,p,h},  outer(E)=(a,n,R,L,q,c,x,y).
```

每條非 incident 的原邊及每個私有點原封保留。
來源：[原兩商圖:24–28,70–90](../../2026-10-18-smaller-bad-e1617a2/B/PROOF.md)。

## 3. 來源已有的非邊及相異點

low-p 定理給 `d_G(a)>=6`，並給原非邊 `hs,ht,ns,nt,rh`。
r6 collar 及 low-p 定理另給原非邊

```
pv,pw,qv,qw,nv,nw,hv,hw.
```

來源：[low-p:7–14,61–79,133–145](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md)、
[共同 fibre:125–135](../../2026-10-14-cofacial-fibres-676b102/pq/PROOF.md)、
[r6 collar:9–19,126–142](../../2026-10-14-lowpq-source-676b102/r6/PROOF.md)、
[r6 low-p:8–16,38–44](../../2026-10-14-r6-lowpq-3953c85/r6/PROOF.md)。
這些各自是同一 G 的圖非邊，故可共同保留；其原證明使用的不同著色不能
被拼接成同一完整著色或一組同時存在的 Kempe 路。

h 沒有原框鄰點：hx,hy 由完整四度 stars 及 h 的度數身份排除；ha,hb
會在 ph 產生第三個原三角面；hc 會使 q 的四個原三角面封閉其 link，
迫 q 四度。n,q,L,R 全是原內點。
來源：[原兩商圖:47–74](../../2026-10-18-smaller-bad-e1617a2/B/PROOF.md)。

原 link 與面條件還排除 `qR,nL,bn,bL`；這是候選商類不產生 loop 的
必要原非邊。p 的 induced link 另有 `ah,qn` 為非邊。
來源：[原兩商圖:122–124,160–172](../../2026-10-18-smaller-bad-e1617a2/B/PROOF.md)、
[low-p:36–45](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md)。

保留實際原 fan 的所有其他鄰點及附件；這份契約不假設 L,R 或其他私有點
沒有額外鄰點，也不把任何未列原邊刪掉。完整 h,p stars 已列全；其他點
只有被明言為完整 star 者才可視為無其他鄰點。

## 4. 來源衍生圖的字面映射及存在性邊界

原 a,c 識別為 z、刪原 x,y,b 得 R，外框 `(z,s,r,t)`，完整支持為 mask13。
刪 r 得 U，外框 `(z,s,v,w,t)`，完整支持為 319；七接點為
`(z,s,v,w,t,p,q)`，保留每份 U 全著色的全部原 r lifts，包括空者。
J 是同一 U 的合法 `s=t` 商圖，商點寫 `m_J=[s=t]`，四連通且每個三角形
為面。原 r 旋轉、兩個原 fan 長度、全部 p,q 附件皆保留。
來源：[J 幾何:11–35,42–79](../../2026-10-15-j-source-geometry-6ddea32/PROOF.md)、
[r6 collar:26–44](../../2026-10-14-lowpq-source-676b102/r6/PROOF.md)、
[r6 low-p:25–35](../../2026-10-14-r6-lowpq-3953c85/r6/PROOF.md)。

本輪原位置可獨立以兩個完整五度 stars 指定。若**另**使用 active-f matching
來源，必須一起保留該來源的 matching、兩面星和 induced J 五圈：其 p,ell
分支有 `d_G(a)>=6,d_G(c)>=5`；p,n 分支才有 a>=7，不能移植到 p,ell。
本頁的 C10 core 引理只用較弱且已列出的原五度位置，不使用 matching。
來源：[active-f:19–26,124–145,223–232](../../2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md)。

三候選保留原 B，完整操作及完成後內點數為

| 候選 | 完整原圖操作 | 完成內點數 |
| --- | --- | ---: |
| Q1 | 刪 p,h；識別 n=b、R=q；僅抑制重複邊 | k−4 |
| Q2 | 刪 p,h；識別 n=L=b；僅抑制重複邊 | k−4 |
| G_B | 刪 p,h；在原六角洞內加 bn,bL,bR | k−2 |

商圖先在刪 p 的實際五邊面識別 n=b，再刪 h，在實際四邊面識別一對
對角點。沒有新點、換框或接回費用。兩候選完整回填充要條件分別為
`L!=a`、`a=q or R!=a`，第二式的 a=q 分支完整保留。
來源：[原兩商圖:120–193,225–264](../../2026-10-18-smaller-bad-e1617a2/B/PROOF.md)。

所有剩餘原來源是否具有本輪 p,ell 五度位置仍是獨立存在性問題；這份
契約及後續結論只量化已具名的位置。C8/C10 count 必要控制、普通小支持
代表或三探測解碼均不提供此位置、任意原來源或逆 P 構形的存在性。
