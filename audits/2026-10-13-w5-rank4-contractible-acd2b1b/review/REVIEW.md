# W5-RANK4-C：計帳、覆蓋與保存契約的獨立審查

2026-10-13，BASE `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。
本審查獨立重推 [FORMULAS](../structure/FORMULAS.md)，逐節檢查
[CORE](../structure/CORE.md) 與 [ATTACHMENTS](../structure/ATTACHMENTS.md)，
並比較兩套有限域與具名原圖構造。證據範圍在本文逐項明列。

## 1. 紙面必要域與分類

一般 annulus Euler 計帳給 `e(A)=3r+20`、`f=2r+10`。以 t_P 記 PPP
原面數，私人邊 incidence、原環邊 incidence、B–U 邊 incidence 分別給

\[
M=2(c-\rho+t_P),\quad p=a+c-\rho+t_P,\quad
\sum_{P}d_G=4r+10+\rho-c-p.
\]

contractible 假設使全部 terminal/v 在 F 無界面；每個有界 F 面本身是
原 G 面，故 t_P=ρ=4。這一步包含不連通、內藏分量及 bridge slit 的排除，
不把「四個獨立環」誤當「四個原三角面」。接完整私人 degree≥5、k≥14 得
`8≤r≤14−2c−a`。附件界先排孤立點；c=3 只可能 r=8 的 4+2+2 或3+3+2，
簡單邊上限8或7，小於所需9。c≥4 又迫 r≤6。故 c≤2 的表格確為新推論。

CORE 先證每個私人點 incident 於原無界面：否则該點只見四份 bounded
PPP faces，完整 degree 至多四。因而所有 cyclic blocks 是原 embedding
中的三角化 polygon；rank-four 的全部六邊形三角化只有 fan、zigzag、
central 三型。任一三-ear block 相對每分量至少兩份的 BUP 基本額，多要
一份 M；但全圖恰 M=2c。這排除 triangle blocks 與 central hexagon。

block-cut tree 的 incidence 界 `Σdeg_S(H)≤2(m−1)` 對共 cutvertex、
多條實際 bridge 及分支 skeleton 均適用。未被 skeleton 使用的 ears
各有不同原點或不同附樹 leaf 供應不同 BUP 面。等號迫非 ear 不接附樹、
ear 附樹只能是單一路徑。故存活恰為 H-fan、H-zigzag、同分量 DD、
分離分量 D+D，另允許表中原 path 分量。rank-zero 分量沒有被先行刪去。

此分類由原面與完整 degree 證明，先於有限 r 上界；沒有發現依賴生成器
零結果、額外 edge-critical/Gallai 身份，或未聲明的私人連通假設。

## 2. 原 rotation、附件及具名覆蓋

每個私人分量恰兩個 BUP 面，且只在兩個指定 ends。沿原外面 contour
（bridge 兩側分別走）讀出 B/U 兩段。任何 pin 前進都使用原環邊唯一的
annular 三角面；倒退重用環邊會分配第二份原面，故原方向連續。所有原
B–U edges 切出 c 個私人 strips 與 a 個 terminal triangles，沒有其他
可能 region。這給全環五步的條件，也涵蓋相鄰 crosscuts 共 pin 與 p=1。

特別核對以下易漏界點：

* H-fan 的私人 degree-five apex 仍至少接一個 terminal；原 exposed
  edge 的第三點迫此附件。generator 用 `d_F+1+bit`，沒有容許零附件。
* 四個 rooted hexagons H0–H3 恰覆蓋 ear 起點及 B/U 側固定後的全部
  fan/zigzag 次序。主程式從三角化構造，獨立程式用 noncrossing chords
  枚舉；兩者沒有以一個方向替代另一個方向。
* DD 中相鄰兩 D atoms 共享同一 backbone 原點，私人 degree四、完整
  degree `6+δB+δU`；其最少私人點七。插入一個 E 才是不同兩 ears
  之間的原橋；更長字保留全部 subdivision 點。
* c=2 的 H+P、DD+P 以含環 strip 作循環起點；D+D 允許重複描述。
  每個 strip 後放任意 terminal triangle word，覆蓋兩 strips 間及
  循環接回處的所有原次序。

任意 source 到 template 是逐點、逐邊、逐面同構，沒有刪點或換代表。
pin map 必有共同方向 ε，B/U 起點可分別平移；U 若按面邊界方向命名，
先保存固定換算。共同 S4 重命名才把外框 literal β 搬到十個代表；U 不
獨立正規化。這個完整圖同構保全部 A/G lifts、所有十 pins 及空 fibres。

canonical 外框到原外框可能另有 D5 搬運，故僅檢查 canonical Σ 的目錄
membership 尚需 K132 對完整外框 D5 封閉。獨立 checker 對凍結132 masks
及全部10個 D5 動作直接重算該封閉性。此處不用相同 Σ ⇒ 相同 R³。

## 3. 兩套程式的有限域及 geometry 實際核對

本審查執行

```bash
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/review/domain_check.py
```

輸出原文保存於 [domain-review.json](domain-review.json)。兩套生成器都
得到6,389個不同完整 parameter keys，鍵集合相等。逐圖主構造的有向面
所得 edges，与獨立程式直接由 neighbours 得到的 edges 完全相同；
另以獨立 rotation walk 重建全部原面，核對 wheel 恢復、components、
完整 degrees、附件、ρ=t_P=4、M=2c、p=a+c。這次沒有染色搜尋。

| 私人族 | 模板數 |
|---|---:|
| H | 4,256 |
| DD | 1,665 |
| H+P | 212 |
| DD+P | 4 |
| D+D | 252 |
| 合計 | 6,389 |

全參數鍵按排序串接的 SHA-256 是
`02636314081bdda3f0cbd5c3ef7675f1340175a04ae750c013ad4809a0f8d1ed`。
這是本次有限域比較的 receipt，不替代前两節任意來源的完備性證明。

## 4. 必要模板與完整 source degree 的分層

兩套程式重算完整 G 的 degree，而非只重算 F-degree。全部模板均滿足
私人點完整 degree≥5；原 B 的 degree≥4 與原 U 的 degree≥5 另保存為
兩個 flags。審查由 literal edges 重新導出以下完整表：

| B 全部 degree≥4 | U 全部 degree≥5 | 模板數 |
|---|---|---:|
| 是 | 是 | 5,573 |
| 否 | 是 | 396 |
| 是 | 否 | 396 |
| 否 | 否 | 24 |

所以816個模板已不符合至少一項原 source degree 條件。保留它們形成
可重播的必要域超集；不能稱6,389份皆是真正最小來源，或稱5,573份均可
實現目錄外關係。全超集若逐份完整 Σ∈K132，則其子集來源自然也被排除。
這項控制是 `triggered and holds`；真正最小目錄外來源仍 `not triggered`。

## 5. 染色契約及採納閘口

逐圖證書必保全部10個 β rows、每列全部1,024個 literal U cells（含空格），
以及全部 A full lifts 和補中心後 G full lifts。主 MRV DFS 直接另算 G，
核對由三色 U fibres 恢復的全部 lifts；獨立 DFS 先固定次序枚舉 U、
中心、私人點，其完整結果逐字比較材料化 rows。因比較的是完整列表，
沒有用 hash 相同或非空 flags 代替 full-lift equality。

本審查程式只執行§3的有限域／geometry核對；完整主染色、seed17不同搜尋
次序、獨立逐列染色、破損負控制的實際完成狀態，以本 audit 的
[REPORT](../REPORT.md) 與驗證 receipts 為準。只有這些全部通過，才能
由紙面覆蓋＋全部模板Σ∈K132採納 contractible rank-four 完整排除。

## 6. 信任界線與剩餘

這是固定 BASE 的條件性來源定理鏈。沿用 K132、K≤13=K≤5、原最小來源
正規形、內點 degree≥5、原小 C4 cap 與外框附件限制；上游 4CT 及有界
外部計數定理的計算證明沒有由本輪重播。本審查沒有新增外部依賴，沒有
把 `lake build` 當本紙面定理的 Lean 形式化。

BASE 的 essential 結果只排除 rank-three，未排除 rank-four。即使本輪
contractible rank-four 完成，任取合法 W5 的一般私人圈秩下界仍保持四；
其等號來源必留在 essential 分支。不得提高為五，也不得將一般 annulus
小代表、R³ 等價或 K∞=K≤5 宣稱完成。

本審查未修改任何舊證據、原始 seal 或 shared source 文件；只交付本 audit
的新紙面證明及本 review 子目錄。沒有 commit、push、PR 或 merge。
