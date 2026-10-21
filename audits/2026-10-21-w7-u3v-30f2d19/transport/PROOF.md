# 原邊 u3v 的兩步完整來源排除

2026-10-21。Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`；全部依賴由
[BASE](../BASE.json) 凍結。承接任意大小原 plane C5 disk、941、最小性、
原 stars／rotation／完整附件，以及[來源契約](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
中嚴格 only-R／W7 子型的所有前提。本項另固定**原圖實際有邊 u3v**。

**定理。** 在同一實際完整核心 D 上，`Z44459=0`。另一 target 44466 因
原邊 u3v 已直接為零，故排除這個嚴格 W7 原分支。此結論逐一適用於原
profiles 10,11,12,13,14,15,43,44；證明只使用它們共同的原邊 u3v，
不混用其餘不同原弦，也不要求一張新的原圖存在。

## 固定字面框與兩個實際作用

原核心始終是
`D=G−{b,p,h,R,x,y,r}`，rim 依序為
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`。以下三份字面框本身已 canonical；
作用中沒有逐片換色框或重新量化一張來源。

| 名稱、ID | 同一原有序 rim 的字面 tuple |
| --- | --- |
| A，44459 | `(0,1,2,1,2,1,2,3,1,2,0,1,2)` |
| M，44111 | `(0,1,2,1,2,1,2,0,2,1,3,1,2)` |
| F，44127 | `(0,1,2,1,2,1,2,0,2,3,1,3,2)` |

對任一份 A 的**整張 D 完整著色** φ，作以下操作。

1. 在同一原 D 上，取完整實際 03-component `K03(q)` 與完整實際
   12-component `K12(c)`。它們的原 boundary contacts 分別恰是
   `{q,v}` 與 `{c,s}`，完整性依據見下節。交換前者的 0/3，並交換後者
   的 1/2。兩個 palettes 相互不交；兩個 induced graphs 及各自的
   component vertex sets 都不變，故兩作用交換次序不影響結果。得到 M。

2. 在第一步得到的**同一張 D、同一份當前完整著色**上，重新取完整實際
   13-component `K13(v)`。它的 boundary contacts 恰是 `{s,v,w}`，
   完整性依據亦見下節。交換整個實際 component 的 1/3，得到 F。

作用域是固定原核心 D 的**完整著色**，並非固定某一份原 G cap-lift
assignment 的雙射。q、v、c、s 的改色可以改變給定 cap assignment 的
合法性；原 G／Q1／J1 cap 始終使用同一原圖、原 stars 與完整附件，對每份
當前 D 著色重新量化全部原 cap lifts。此處不聲稱固定 cap 見證保持。
凍結零值與完整 orbit 覆蓋的量詞涵蓋 D 的全部完整 fibres，也包含無法
接回 G 的合法 D 著色。因此在 M 重新套用完整 orbit family 不需假設
原來選定的 type III 歷史標籤或 residual membership 不變，也未逐步補滿
觀測 fibre。原 selected witness 只用來提供最初的 target 正量。

兩步作用都攜帶全部原私有頂點。第一步同時改 `q:3→0,v:0→3` 與
`c:1→2,s:2→1`；第二步改 `s:1→3,v:3→1,w:1→3`。
其餘原 rim 色保持表內所示；並未只在 boundary 上單獨翻點。

每個 component 交換都保持 properness。第一步是兩個互相交換次序的
involutions；第二步亦為 involution，因為 13-induced graph 不因其
component 內交換 1/3 而改變。兩步因而分別給出**完整 fibres 的 injection**

\[
\operatorname{Col}_D(A)\hookrightarrow\operatorname{Col}_D(M)
\hookrightarrow\operatorname{Col}_D(F).
\]

但 F 在**原實際邊** u3v 上滿足 `u3=v=1`，故 `Col_D(F)` 為空。
於是

\[
\boxed{Z_{44459}\le Z_{44111}\le Z_{44127}=0.}
\]

此為同一原來源的全稱反證。若假設 φ 存在，第二步的 component 分類
已與原邊 u3v 強迫 u3、v 同在一個 13-component 衝突；把作用寫到 F
則將同一矛盾具體呈現為原邊同色。

## 完整 component 分類的六欄證據

分類使用[已證完整 orbit 覆蓋引理](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)
及完整凍結 family；沒有從各自可行的 marginals 拼出一份見證。
每份實際完整著色在所選 palette 的 **整個 actual orbit** 必屬於該完整
必要 family；已證零 fibres 不能在其任何一份 actual orbit 投影中出現。

A 的 `03|12` half-row 是 **12302027**。掃描全部原 307,197 個 columns，
它只屬於一欄 **306985**；其四個完整 boundary components 為

```
03: {a}, {q,v};
12: {n,u4,u3,u2,u1,L,w,t}, {c,s}.
```

因此第一步指定的兩個實際 components 有上述確定的 boundary contacts。
該欄含 M 的另一 half-row **12301211**。

M 的 `02|13` half-row 是 **10064313**。完整 incident columns 恰為

```
147448, 147449, 167802, 226130, 231666.
```

它們的完整 boundary partitions 為：

| 欄 | 02-components | 13-components |
| ---: | --- | --- |
| 147448 | `{a,L,q,c,t}`, `{u4}`, `{u2}` | `{n,u3,u1}`, `{s,v,w}` |
| 147449 | `{a,L,q,c,t}`, `{u4,u2}` | `{n,u1}`, `{u3}`, `{s,v,w}` |
| 167802 | `{a,u2,L,q,c,t}`, `{u4}` | `{n,u3}`, `{u1}`, `{s,v,w}` |
| 226130 | `{a,u4,L,q,c,t}`, `{u2}` | `{n}`, `{u3,u1}`, `{s,v,w}` |
| 231666 | `{a,u4,u2,L,q,c,t}` | `{n}`, `{u3}`, `{u1}`, `{s,v,w}` |

所以全部實際可能型都迫 `K13(v)` 的 boundary contacts 恰是 `{s,v,w}`。
五欄亦全都含 **同一份** F half-row **10064365**；不需四個不同的
同色種子，更不需長期 support-closure transcript。

另一個來源幾何讀法是：五欄全迫 a,t,L,q,c 在同一 02-component。
然而原 chord u3v 的兩端在 M 中是 1,3，將 D 的 C7／C8 兩側隔開；
a,t 與 L,q,c 分在兩側，02 路不能通過 chord 的端點。這正是上述
component 反證的同源平面分離版本；主證使用明確的完整 component
involutions，不需額外假設 side gluing。

## 對 X66582、X67755 與另一個 target 的後果

兩個原欄 66582、67755 都含 A 的 `01|23` half-row 6712710。
原同源非負方程為 `2ZA=Σ_{j:hA∈Cj}Xj`；既已證 `ZA=0`，非負性立即給出

\[
X_{66582}=X_{67755}=0.
\]

44466 的字面 tuple 是 `(0,1,2,1,2,1,2,3,1,2,1,0,2)`，其中
`u3=v=1`，所以此固定原邊下本來便有 `Z44466=0`。原 selected witness
要求 `Z44459+Z44466>0`，矛盾，遂排除此八個固定 profiles。

這不代表其餘 strict W7 profiles 被排除，也不代表任意含 chord u3v 的
一般 C13 disk 沒有 A 著色。完整零值與 orbit 覆蓋來自本來源契約；不能
把它們從 941／J1／strict W7 前提中拆除。

## 獨立重播與父 closure 審核

[check.py](check.py) 不讀 support-closure 輸出。它釘死 BASE 所列原
SOURCE_CONTRACT、counting PROOF、caps、complete orbit family 與前輪
逐 profile 證書的 bytes／SHA；獨立掃描完整 family，核對兩個 half-row
的**全部** incident columns，恢復六欄的完整 component partitions，
重生每欄全部 component flips，核對三份 literal tuples、兩步 boundary
作用、逆作用與四個 half-row/state 對應。完整原 rows 及 partitions
均存在 [certificate.json](certificate.json)。

component 恢復以同 palette 各位置在全欄的 XOR variation profiles 分組。
一個 palette 只有一個固定 anchor；不同 components 至少有一個可獨立
翻色，因此 profiles 必異。private components 只改變重數，不改變這個
邊界分量判準。checker 另從恢復的 blocks 固定兩個 anchors，逐一再生
全部 normalized rows，要求與完整原欄相等。

另外獨立審核父層 `closure/check.py`：每個新增同色原弦種子先將**整個**
shared state 判零；一欄碰到任何零 fibre 後僅刪一次；每個 half-row 的
原 surviving degree 精確扣減；任何 half-row 空便由同一 Z 方程將
該 state 判零，再沿它的全部三個 half-rows 傳播。原 family 已完整覆蓋，
且該算法不新增欄或刪除來源前提。沒有發現 soundness flaw。本項短證
獨立重播同一結論，不依賴這套大 transcript 的處理順序。

本證書只裁定共同原邊 u3v 的八型子支。任意大小原核心與所有 private
multiplicities 均保留；一般 strict W7、一般 J1/J2、smaller bad、主命題
及 Lean 尚未由此完成。
