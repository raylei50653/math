# W7 原邊 u3v：兩輪同源 Kempe 作用排除八型

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
承接前輪未提交的結構成果；工作前已將48份依賴的 bytes／SHA256及原 dirty
狀態凍結在 [BASE.json](BASE.json)。前輪產物、原 cap／orbit 證據均未改寫。

**完成：在完整原來源契約的嚴格 only-R／W7 子型，原邊 u3v 不可能存在。**
原八型 `10,11,12,13,14,15,43,44` 全部排除，且

```
X66582=X67755=Z44459=Z44466=0。
```

一般 W7 仍 OPEN；前輪40份必要原接觸因此剩32份。沒有大型 LP、新原圖
枚舉、縮減圖構造、Lean修改、commit或push。

## 1. 定理的完整範圍

承接[原五邊路契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[完整同源計數與 orbit 覆蓋](../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)
及[前輪逐型完整接合](../2026-10-21-w7-structural-30f2d19/review/PROFILE_ORBITS.md)：
原 G 為任意大小 plane C5 disk，原框 `(x,y,a,b,c)`、支持941、全域最小內點數
再最大邊數、p/h/r完整stars、全部原附件／rotation／私有點及短圈前提均保留。
固定原 Q1 接受零的 J1 type III 實際五邊路，其原 induced C7 內部恰只有 R。
只有這個 only-R 子型才使用完整七度 W7。

同一實際核心始終是

```
D=G-{b,p,h,R,x,y,r},
rim(D)=(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)。
```

Z 計數 D 的全部固定字面框完整著色，包括不能接回 G 的完整著色及所有空
fibres。X保留全部實際 Kempe orbits 的原私有分量重數。原 G、Q1、J1的
cap stars 及全部 lifts 不變；換色後各 fibre 的 cap assignments 仍按原模型
完整重新量化。下述作用不宣稱保留某一份固定原 G cap assignment。

本輪只再假設**同一原邊 u3v 存在**。八份 profiles 的其他弦各自保留；
證明只需共同的 u3v，不拼接不同 profiles 的原圖或見證。

## 2. 三份字面色框與兩輪完整分量作用

[完整來源紙證](transport/PROOF.md)給出以下短反證。三份 tuple 本身均為原
canonical states，沒有逐片換框：

| 名稱 | ID | 原 rim 字面色框 |
| --- | ---: | --- |
| A | 44459 | `(0,1,2,1,2,1,2,3,1,2,0,1,2)` |
| M | 44111 | `(0,1,2,1,2,1,2,0,2,1,3,1,2)` |
| F | 44127 | `(0,1,2,1,2,1,2,0,2,3,1,3,2)` |

假設同一 D 有一份 A 完整著色。

1. 原完整 orbit 分類迫實際 `K03(q)` 的 rim 接觸恰為 `{q,v}`，實際
   `K12(c)` 的接觸恰為 `{c,s}`。交換這兩個**完整實際分量**，得到 M。
   兩個互補 palettes 不相交，兩作用交換次序且各自可逆。
2. 在這份實際 M 完整著色上重新分類，全部五種可能型都迫實際 `K13(v)`
   的接觸恰為 `{s,v,w}`。交換它得到 F；作用仍是可逆的完整分量交換。

每一步都攜帶原全部私有點，並保持同一張 D 的 properness。因此是完整 fibres
的 injections，而不是只對 rim 色列作形式變換：

```
Col_D(A) ↪ Col_D(M) ↪ Col_D(F)，
0 ≤ Z44459 ≤ Z44111 ≤ Z44127 = 0。
```

最後的 F 在原實際邊 u3v 上滿足 `u3=v=1`，所以其完整 fibre 空。
等價地，M 的 u3、v 分別是1、3，原邊直接迫它們在同一13分量；但第二輪
的完整來源分類排除了 u3，矛盾。這不是假設兩輪交換後保留最初選路的
歷史標籤；各輪均使用 D 的全部完整 fibres 重新判定當前實際分量。

## 3. 六個原欄足夠驗證全部 forcing

短紙證中的分量 forcing 由**完整原 family** 核對，不依賴長閉包或數值：

- A 的03|12 half-row `12302027` 在全部307,197原欄中只屬於 `306985`。
  它迫03分量 `{a},{q,v}` 及12分量 `{n,u4,u3,u2,u1,L,w,t},{c,s}`。
- M 的02|13 half-row `10064313` 只屬於
  `147448,147449,167802,226130,231666`。五欄都有**同一個**完整13邊界
  分量 `{s,v,w}`，且包含 F 的同一 half-row `10064365`。

[transport checker](transport/check.py)恢復上述六欄的全部 components，
重生每欄全部 normalized rows，並核對字面作用及逆作用。
這是紙面來源作用加精確有限邊界分類；任意大小來源的 orbit 覆蓋沿原紙證，
沒有把它稱為新的 Lean 定理。

另有不讀閉包 transcript 的[三態支配證書](closure/compact-certificate.json)
及[獨立 validator](closure/compact.py)。validator從原 caps、row map及全部原欄
重新掃描完整 incidence，直接核對

```
{columns containing A half-row12302027}
    ⊆ {columns containing M half-row12301211}；
{columns containing M half-row10064313}
    ⊆ {columns containing F half-row10064365}。
```

以原方程 `2Z_i=ΣX_j` 和非負性便得同一支配鏈。它核對全部原欄，不能
漏掉一個未列的 supporting column。七項 malformed-proof 控制涵蓋漏欄、
錯 state、錯共同 row、bool係數、假同色種子、缺型及擴大來源範圍。

## 4. 兩個 X 的排除與具名 closure

原欄66582及67755都含 A 的01|23 half-row `6712710`。由 `ZA=0` 及
該原 half-row 的非負完整同源方程，立即得到

```
X66582=X67755=0。
```

另一原 witness 44466 在 u3v 上本就同色，故也為零。原選定實際五邊路
完整著色卻迫 `Z44459+Z44466>0`，矛盾。所有八份固定原接觸都含共同
原邊 u3v，故這是**整個具名八型分支**的排除，不只一份數值控制。

在同一完整來源契約內可採納為新的原非邊 `u3v∉E(G)`。它不表示一般
帶u3v的C13 disk無法有A著色：941、J1、嚴格W7、完整原零fibres及其
orbit覆蓋前提均不可刪除。

## 5. 發現過程的完整殘餘與獨立驗證

[原邊來源橋接](geometry/PROOF.md)核對：u3v令既有61,308個 live states 中
15,382格同色 fibre 歸零；這是全部完整著色的零值，與能否接回 G 無關。
[逐八型閉包](closure/check.py)在既有完整 family 中傳遞這些零值，沒有新
原圖枚舉或LP。[完整殘餘](closure/result.json.gz)保存每型全部存活state／欄
ID、每個新零格的依據與每個被刪欄的原零state見證。

只用 u3v 的最弱profile10已加傳10,794個零state，最後留35,132 states及
70,343 columns，但兩個target均零。這些餘量不宣稱共同正計數可行。
其餘七型因額外原弦而有各自更小殘餘，並非分別改選來源。

[獨立重算](review/PROOF.md)不用queue或degree counters，改以同步輪次每輪
重建全 family 支援；15輪達同一固定點，逐state／逐欄完全一致。A在第二輪
已零，兩個X在第三輪被刪。另獨立審查短完整來源 injections 及 cap 量詞。
短證不依賴這15輪或其處理順序。

完整 normal／seed17／optimized 重播、負控制、frozen-input drift及文件
檢查的實際結果見 [verification.json](verification.json)。主要只讀重播：

```
python3 -B audits/2026-10-21-w7-u3v-30f2d19/transport/check.py
python3 -B audits/2026-10-21-w7-u3v-30f2d19/closure/compact.py --controls
python3 -B audits/2026-10-21-w7-u3v-30f2d19/review/independent.py
```

五組checker共10次normal／seed17 optimized重播通過；46份數學／前輪證據
輸入零漂移。正式文件與docs範圍DocGraph通過；全樹仍有72項既有frozen／
scratch重複ID，沒有新audit的錯誤，詳[診斷紀錄](docgraph-whole-tree.json)。

## 6. 父題、consumers與停止邊界

Closure scope：原941／J1完整契約下，嚴格only-R／W7且有原u3v之全部八型；
同源兩個X及兩個target皆零。證據為完整來源紙面作用、有限全欄分類與
獨立精確證書；沒有新Lean或較小bad。

父W7的必要 profiles 從40減為32：20份仍是其他joined二欄子型，12份
仍保留全部15欄；A可用profile從28減為20，B的24份不變。這些剩餘型
未宣稱可實現，也沒有排除一般W7、一般C7多內點、type I／更長路或J1／J2。
未加原弦的既有一般W7必要計數錐可行性仍OPEN。
這32份完整原接觸、原弦與既有完整target欄IDs保存於[RESIDUAL](RESIDUAL.json)；
沒有重跑這32型的計數閉包或把其必要支持當成共同可行解。

Updated：Kempe導覽、STATUS，採納具名closure與32型停止點。
Reviewed-unchanged：前輪凍結W7來源／證書保留當時40型語境；State導覽的
完整來源／歷史殘餘量詞及一般J1 OPEN不變；HANDOFF／README的研究線不變。
Propagation stop：L2，僅這個子型關閉，沒有父W7 closure可上推一般主命題。
目前下一個窄義務由 [Kempe導覽](../../docs/c5_kempe_guide.md)維護。
