# 原邊 u1v 的兩步完整來源排除

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
本輪 [BASE](../BASE.json) 凍結 83 份依賴。承接[原來源契約](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
的任意大小原 plane C5 disk、941、最小性、完整 stars／rotation／附件，
以及嚴格 only-R／W7 子型。本項另固定 **原圖實際有邊 u1v**。

**定理。** 在這個同一實際原核心上，`Z44459=Z44466=0`，並有
`X48617=X67755=0`。因此排除原 profiles
**68,69,78,79,88,89,92,93**。

以下證明逐項重建原凍結完整 orbit family 的 component forcing，然後
檢查所得 forbidden tuple 的 **u1、v**。它不假設原圖有任何頂點對稱，
不交換 u1、u3 的名稱，也不使用 u3v 子型已證的排除或其新增零值。

## 1. 固定字面 tuple 與作用域

原核心始終為 `D=G−{b,p,h,R,x,y,r}`，rim 順序固定為
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`。三份 tuple 如下，本身均已 canonical：

| 名稱、ID | 原有序 rim 字面 tuple |
| --- | --- |
| A，44459 | `(0,1,2,1,2,1,2,3,1,2,0,1,2)` |
| M，44111 | `(0,1,2,1,2,1,2,0,2,1,3,1,2)` |
| F，44127 | `(0,1,2,1,2,1,2,0,2,3,1,3,2)` |

對 D 的任意完整 A 著色 φ，交換兩個**完整實際 components**：

- `K03(q)` 的 0/3，其原 boundary contacts 恰為 `{q,v}`；
- `K12(c)` 的 1/2，其原 boundary contacts 恰為 `{c,s}`。

確切 component forcing 見第 2 節。兩個 palettes 相互不交；各自的
induced graph 與 component vertex sets 不因這些交換而變，兩作用交換
次序不影響結果，合成為 involution。作用得到 M 的完整 D 著色：
`q:3→0,v:0→3,c:1→2,s:2→1`，其餘原 rim 色不變。

在該份**當前同一張 D 完整著色**上，重新取完整實際 13-component
`K13(v)`。其 boundary contacts 必恰為 `{s,v,w}`。交換整個 component
的 1/3，亦為 involution，得到 F：`s:1→3,v:3→1,w:1→3`。

這兩步都攜帶 component 的全部原私有頂點，不是在 rim 上單獨翻點。
它們分別給出完整 fibres 的 injections，因而

\[
\operatorname{Col}_D(A)\hookrightarrow\operatorname{Col}_D(M)
\hookrightarrow\operatorname{Col}_D(F),
\qquad
Z_{44459}\le Z_{44111}\le Z_{44127}.
\]

檢查字面 tuple 即見：兩步都沒有改 **u1 的色 1**，而第二步後
**v 的色亦為 1**。原實際邊 u1v 迫 `Col_D(F)=∅`。所以

\[
\boxed{Z_{44459}\le Z_{44111}\le Z_{44127}=0.}
\]

每一步只作用於原固定核心 D 的全部完整著色，不是固定某一份完整 G
cap-lift assignment 的雙射。q、v、c、s 的改色可以改變特定 cap assignment
的合法性；G／Q1／J1 caps 一直使用同一原圖、原 stars 及完整附件，對
每份當前 D 著色重新量化全部原 cap lifts。凍結零值與 orbit coverage
量詞涵蓋 D 的**全部**完整 fibres，包含無法延回 G 的合法 D 著色。
因此 M 的重新分類無需維持原選定 type III 歷史標籤或 residual membership，
也未逐步補滿觀測 fibre。原 selected witness 只供應最初的 target 正量。

## 2. Component forcing 只讀原完整 family

來源權威為[原完整計數證明](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)。
其凍結 `orbits.json.gz` 的 bytes SHA256 為
`542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad`。
這是新增 u3v 或 u1v 零值**之前**的原 307,197 欄完整 surviving family。
下面的完整 incident-column 分類沒有再用任何可選原弦去過濾 family。

A 的 `03|12` half-row 為 **12302027**，完整 family 中唯一 incident
column 是 **306985**。其全部 boundary components 為

```
03: {a}, {q,v};
12: {n,u4,u3,u2,u1,L,w,t}, {c,s}.
```

故第一步兩個實際 components 的 contacts 完全確定。該欄含 M 的
另一 half-row **12301211**。

M 的 `02|13` half-row 為 **10064313**。完整 incident columns 恰為：

| 原欄 | 02-components | 13-components |
| ---: | --- | --- |
| 147448 | `{a,L,q,c,t}`, `{u4}`, `{u2}` | `{n,u3,u1}`, `{s,v,w}` |
| 147449 | `{a,L,q,c,t}`, `{u4,u2}` | `{n,u1}`, `{u3}`, `{s,v,w}` |
| 167802 | `{a,u2,L,q,c,t}`, `{u4}` | `{n,u3}`, `{u1}`, `{s,v,w}` |
| 226130 | `{a,u4,L,q,c,t}`, `{u2}` | `{n}`, `{u3,u1}`, `{s,v,w}` |
| 231666 | `{a,u4,u2,L,q,c,t}` | `{n}`, `{u3}`, `{u1}`, `{s,v,w}` |

五種完整可能型全部迫 `K13(v)` 的 boundary contacts 恰為 `{s,v,w}`，
**不含 u1**。它們亦全部含同一份 F half-row **10064365**。

各實際來源若存在，其完整 actual orbit 必屬於這個完整必要 family。
不存在從兩個 independently feasible partitions 拼見證的步驟：先對
任一實際 φ 作第一個完整作用，得到同一 D 的實際 φ1，再於該 φ1 上
重新取實際 `K13(v)`，其所屬五型每一型都給出相同 boundary contacts。

Component 的恢復方法是：在全欄的每個位置記錄相對 reference row 的
XOR variation profile，同一 palette 中 profiles 相等恰當同一 boundary
component。正向因同 component 共同翻色；反向因每個 palette 只有一個
固定 anchor，不同 components 至少有一個可獨立翻色。private components
只改變原 X 的重數。checker 另固定兩個 anchors，逐一翻轉恢復的其餘
blocks，再生整欄全部 rows，要求與原完整支持恰相等。

## 3. 兩欄、另一個 target 與八型覆蓋

原欄 **48617、67755** 都含 A 的 `01|23` half-row **6712710**。
同源非負方程 `2ZA=Σ_{j:6712710∈Cj}Xj` 與已證 `ZA=0` 立即給出

\[
X_{48617}=X_{67755}=0.
\]

另一個 target 44466 的原 tuple 是
`(0,1,2,1,2,1,2,3,1,2,1,0,2)`，本來就在原邊 u1v 上滿足 `u1=v=1`，
所以亦為零。所選原五邊路 witness 要求
`Z44459+Z44466>0`，矛盾。

八型 ID 及其**完整原弦集合**逐一存在 [certificate.json](certificate.json)。
每份都實際包含 u1v；其餘不同原弦全留在同一原圖。完整 component
交換保持該原圖全部邊的合法性，因此額外原弦無需另找相容的外部圖。
沒有把不同 profile 的來源、cap 或私有著色合併。

## 4. 獨立驗證與界線

[check.py](check.py) 從本輪 BASE 所列的原 SOURCE_CONTRACT、counting
PROOF、caps、完整 orbit family 及前輪逐型原弦證書核對 bytes／SHA。
它不讀 u3v audit，不讀任何 support-closure transcript，也不用對稱性。
完整掃描 307,197 欄，核對兩個 half-row 的**全部** incident columns，
重生六欄的完整 component flips，核對三份 literal tuples、兩步正反作用、
全部 state／half-row 對應、u1v 同色終點及要求排除的兩欄。

負控制確認：漏掉五型之一被完整 incidence 檢查拒絕；只翻 v 不翻整個
`{s,v,w}` 被實際 component 邊界檢查拒絕；只有 u3v 而沒有 u1v 的來源
profile 被本輪 source gate 拒絕。normal、seed17、seed17 加 `-O` 唯讀
重播均通過。

本項排除共同原邊 **u1v** 的八型嚴格 W7 子支。沒有聲稱任意一般 C13
disk 都有這些 component forcing，也沒有排除其餘 strict W7 profiles、
一般 J1／J2、smaller bad 或主命題，未新增 Lean 定理。
