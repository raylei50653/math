# 原邊 u1w：五個完整來源分支規則的排除

2026-10-21；BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。
[BASE.json](BASE.json) 凍結本項八份權威／方法輸入的 bytes、SHA256，
逐份 bytes 與這個 Git BASE 相等。

**定理。** 在[原來源契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
的任意大小原 plane C5 disk、941、最小性、完整 stars／rotation／附件，
及嚴格 only-R／W7 子型下，原圖不能有邊 **u1w**。
若假設有該原邊，則 `Z44459=Z44466=0`、`X48647=X67765=0`，
與所選實際五邊路 witness 的 `Z44459+Z44466>0` 矛盾。
因此四個固定原 profiles **96、97、100、101** 全部排除。

證明直接讀取新增可選弦零值之前的完整 307,197 欄 family，
不假設 v／w 或任何頂點的圖對稱；不承接 u3w、u3v 或 u1v 的排除。
u1v checker 只供完整 component 恢復方法的參考，沒有使用其零值。

## 1. 同一原圖、同一完整 fibres

固定同一實際原核心

```
D = G − {b,p,h,R,x,y,r},
ordered rim = (a,n,u4,u3,u2,u1,L,q,c,s,v,w,t).
```

原 R 的完整七度 star、n 的全部額外附件、原 rim chords、所有原私有點
與原 rotation 始終保留。`Z_i` 計這份 D 的該 canonical 色框下**全部**
完整著色；空 fibre 計零。全域色置換作用在全部私有點。
原 G／Q1／J1 caps 對每份當前完整 D 著色量化原 cap 的全部 lifts；
沒有固定一份選定 cap assignment，沒有在不同圖或不同著色間拼接。

來源的完整 cap 零值與原支持閉包覆蓋 D 的全部完整 fibres，包含不能接回
G 的合法 D 著色。因此交換後無須維持原 type III 的歷史標籤，也無須
每一步補滿觀測 fibre。最初的選定實際 witness 只供應 target 正性。

[原完整計數證明](../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)
已證：對每個 normalized half-row h，

\[
2Z_{i(h)}=\sum_{j:h\in C_j}X_j,\qquad X_j\ge0.
\]

每個實際完整 Kempe orbit 均在原 family 中。碰 rim 的 components
提供整欄的全部 flips；不碰 rim 的私有 components 只提供正重數，已計入
同一個 X。每個 row entry 為 4，H-half-row size 為 8。

本項使用的 `orbits.json.gz` bytes SHA256 固定為
`542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad`。
不是刪除 u1w 衝突欄後的 restricted family。

## 2. 完整覆蓋零傳播引理

固定同一原 D 與 literal half-row h。若 h 的**每一個**原完整 incident
column Cj 都含某個已證為零的完整 fibre half-row kj，則每個該 Xj 都為零，
故由完整非負方程得到 `Z_i(h)=0`。各欄的零見證可以不同，但必須各自
在這個同一來源的完整 orbit 中，不能只用 target row 或獨立 marginal。

等價的紙面操作是：任取該完整 fibre 的實際著色 φ；它的 actual orbit
必屬某個列出的 Cj。在**該份 φ** 的兩個 palette induced subgraphs 上，
翻轉將 h 送到 kj 的整個實際 components，連同所有原私有頂點一起翻轉。
所得是同一 D 的完整合法著色，卻進入已證為空的完整 fibre，矛盾。

每一欄的 component contacts 由全部 rows 的 XOR variation profiles 恢復，
不是由邊界相鄰猜測。相同 palette 的兩個 boundary points 在同一 component
恰當其 variation profiles 相同；固定兩個 palette anchors 後，每個其他
block 均可獨立翻色。checker 逐欄重生所有 rows，要求與原整欄完全相等。
完整 actual contacts、每步 literal 起終 tuple 與全部翻轉 components
逐項保留在 [OPERATIONS.md](OPERATIONS.md) 及 [certificate.json](certificate.json)。

## 3. 三份輔助 fibre 直接撞原邊 u1w

以下皆使用原有序 rim 的 canonical literal tuple：

| fibre | literal tuple | 使用 half-row | 全部 incident columns |
| --- | --- | ---: | --- |
| 44722 | `(0,1,2,1,2,1,3,0,3,1,3,2,3)` | 12292509 | 306623,306626 |
| 45945 | `(0,1,2,1,2,3,1,2,1,3,1,0,3)` | 12283489 | 304587,304588,304669 |
| 65628 | `(0,1,2,3,2,3,1,2,1,3,1,0,3)` | 12021345 | 261890,261893,262147,263979,276925,276926,277007 |

44722 的兩欄都可送到同一個 44740：第一欄翻完整 12-component `{s,w}`；
第二欄翻完整 12-components `{s}` 與 `{w}`。兩者所得 literal tuple 都是
`(0,1,2,1,2,1,3,0,3,2,3,1,3)`，其 **u1=w=1**。因此 `Z44722=0`。

45945 的完整三欄如下：

| 原欄 | 翻轉的完整 03-components contacts | 終點 fibre |
| ---: | --- | ---: |
| 304587 | `{u1}`,`{s}` | 42071 |
| 304588 | `{u1,s}` | 42071 |
| 304669 | `{u1}` | 42118 |

42071=`(0,1,2,1,2,0,1,2,1,0,1,0,3)`；
42118=`(0,1,2,1,2,0,1,2,1,3,1,0,3)`，兩者 **u1=w=0**。
因此 `Z45945=0`。

65628 的完整七欄如下：

| 原欄 | 翻轉的完整 03-components contacts | 終點 fibre |
| ---: | --- | ---: |
| 261890 | `{u3,u1}`,`{s}` | 27309 |
| 261893 | `{u3,u1,s}` | 27309 |
| 262147 | `{u3,u1}` | 27356 |
| 263979 | `{u3,s}`,`{u1}` | 27309 |
| 276925 | `{u3}`,`{u1}`,`{s}` | 27309 |
| 276926 | `{u3}`,`{u1,s}` | 27309 |
| 277007 | `{u3}`,`{u1}` | 27356 |

27309=`(0,1,2,0,2,0,1,2,1,0,1,0,3)`；
27356=`(0,1,2,0,2,0,1,2,1,3,1,0,3)`，兩者 **u1=w=0**。
因此 `Z65628=0`。上述規則沒有重命名 u1 或 u3。

## 4. 十八欄把 45034 送入三個已零 fibre

令

```
T45034 = (0,1,2,1,2,1,3,2,1,3,1,0,3),
half-row = 10073827  (02|13).
```

在完整原 family 中，它的 incident columns **恰有以下十八欄**，分為三組：

| 全部原欄 | 當前完整 components 的作用 | literal 終點 |
| --- | --- | ---: |
| 152303,152304,169872,227655,232035 | 翻 02 `{q,w}` 及 13 `{c,s,v}` | 44722 |
| 152306,152307,152310,170670,170679,227631,227642,227656,232167,232169 | 翻 13 `{u1,L}` | 45945 |
| 152308,228263,228269 | 翻 13 `{u3,u1,L}` | 65628 |

所有終點的 literal tuple 正是第 3 節所列 canonical tuple，沒有逐片改框。
兩個 palettes 不交時兩個實際作用可以任意次序執行；同 palette 的多個
不同 components 取完整聯集翻轉。三組覆蓋全部十八欄，故 `Z45034=0`。

## 5. 兩個 targets 全零、四個完整 profiles 排除

target A44459=`(0,1,2,1,2,1,2,3,1,2,0,1,2)` 本來已有 **u1=w=1**，
所以 `Z44459=0`。

target B44466=`(0,1,2,1,2,1,2,3,1,2,1,0,2)` 的 `01|23`
half-row 為 **6712722**，完整 incident family 是：

| 原欄 | 同一完整 orbit 的零 fibre |
| --- | --- |
| 43335,43336,48620,66584,67756 | A44459，u1=w=1 |
| 43380,43381 | 28064=`(0,1,2,0,2,0,2,3,1,2,1,0,2)`，u1=w=0 |
| 66602 | 42826=`(0,1,2,1,2,0,2,3,1,2,1,0,2)`，u1=w=0 |
| 48647,67765 | 45034，第 4 節已排 |

最後兩欄的實際作用均為：翻完整 23-components `{L,q}`、`{s}`、`{t}`，
得到第 4 節的同一份 T45034。其餘八欄的逐一完整作用見附表，
不是僅觀察 B 本身是否合法。由第 2 節引理得 `Z44466=0`；
而兩欄 48647、67765 都含 half-row 6712722，故 `X48647=X67765=0`。

與原來源的實際正 witness `Z44459+Z44466>0` 矛盾，排除原 u1w 子支。
在原四十份必要 profiles 中，實際含 u1w 的四份完整來源如下：

| 原 profile ID | 全部原可選弦 |
| ---: | --- |
| 96 | u1w |
| 97 | au4, u1w |
| 100 | u1w, u2w |
| 101 | au4, u1w, u2w |

每份的全部原弦始終留在其原圖；完整 actual component 交換自動保持
全部原邊的合法性，無需把其他弦刪掉，亦無需重新選擇另一個外側圖。

## 6. B 的字面 03 首步：已重建但不冒充 A 的鏡像鏈

B 的 `03|12` half-row **12302051** 在原 family 中唯一 incident 欄為
**306993**，其完整 contacts 為：

```
03: {a}, {q,w};
12: {n,u4,u3,u2,u1,L,t}, {c,s,v}.
```

翻完整 `K03(q)` 與 `K12(c)`，得到
44107=`(0,1,2,1,2,1,2,0,2,1,2,3,2)`，half-row 12301239。
這一步與 A 的作用確實不同：第二個 block 含 v。44107 在另一個 split
有十四份可能欄，不能直接把 A 的五欄後繼套過來。因此主證明使用
上面完整重建的五節點分支證書。checker 也獨立重播本節首步。

## 7. 重播、負控制及界線

```
python3 -B audits/2026-10-21-w7-u1w-d23f94f/check.py --controls
PYTHONHASHSEED=17 python3 -B audits/2026-10-21-w7-u1w-d23f94f/check.py --controls
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-u1w-d23f94f/check.py --controls
```

checker 掃描全部 307,197 欄，核對五個 half-rows 的完整 incidence
**2、3、7、18、10**，及另外一欄獨立 B03 首步；重生 41 欄全部 component
flips，核對四十份 literal 整分量操作與五節點證明的拓撲順序。
漏欄、漏零見證、只改 endpoint 卻漏整分量、錯原邊、漏 profile、布林欄號、
假原邊零 fibre、擴張到任意 C13 disk，八份破損證書均遭拒絕。
normal、seed17、seed17 加 `-O` 的唯讀 replay 相同。

這是任意大小、完整來源契約內的 **u1w 四型來源排除**，不是實圖枚舉結果。
沒有 LP，沒有聲稱必要錐已排除或已找到可實現來源；一般 W7 的其他 profiles、
一般 J1／J2、smaller bad 與主命題仍 OPEN，沒有新增 Lean 定理。
