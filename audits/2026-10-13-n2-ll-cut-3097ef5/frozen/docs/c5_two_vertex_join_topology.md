# C₅ 兩點接合主例：原框、側別與區域重疊的拓撲稽核

2026-09-30。接續[八點接合](c5_two_vertex_join.md)，只處理保存的
`reference`：A=B=R1023 的兩份純 C₅ 代表，`(a0,a2)=(b0,b1)`。
同一八點十邊圖的全部環序、原框與側別已完成稽核。證據為紙面構造及
Python 固定圖證書；未新增 Lean theorem。現在的研究停止點見
[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

2026-09-30 後續：[私有內點接合](c5_two_vertex_private_topology.md)已完成
另一固定控制的原框可行性：整圖平面，但兩個原框皆受原交錯路徑阻斷。
本文的全部環序分類仍只限下述純 C₅ 主例。

## 1. 結論與前提

保留兩側全部邊、原 C₅ 環序、共享點雙射與完整八點 relation；不增加
共同邊或其他頂點識別，不預先指定來源 disk 的方向或接合後外面。
本例沒有私有內點，兩條原框除了共享頂點 x、y 外互不相交。

- 整圖抽象平面。A 原框、B 原框**各自存在**作為整圖 disk 外界的嵌入。
- 在同一平面嵌入中，A、B 原框不能同時作整圖外界；兩者可以同時為
  球面嵌入的面界，這是不同的命題。
- 兩份原框所圍的有界 disk，可有內部互斥、B 包含於 A、A 包含於 B，
  或有內部重疊但互不包含。這四種均有明確環序及外面見證。
- 若另規定「兩份 disk 的內部必須互斥」，恰保留下面 24 份配置中的
  8 份。使用者尚未指定接合政策，故一般 `prescribed_transition_legality`
  保持 `unknown`，不將所有平面配置標成合法 transition。
- 同一份完整 J 在所有配置中仍是 **140 軌道／3,360 份賦色**，
  `π_A=R1016`、`π_B=R1023`。J 與實際圖均未改動。

這些是**指定代表圖**的結論，不是 R1023 所有實現的拓撲分類。
其餘五份既有控制本輪未作拓撲判定。

## 2. 四條原路徑與平面環序的完備性

令 x=a0=b0、y=a2=b1，依原圖分成四條內部互斥的 x–y 路徑：

| 路徑 | 原具名頂點，從 x 到 y | 邊數 | 來源 |
| --- | --- | ---: | --- |
| P₀ | a0–a1–a2 | 2 | A |
| P₁ | a0–a4–a3–a2 | 3 | A |
| P₂ | a0–a2 | 1 | B 原框邊 b0–b1 |
| P₃ | a0–b4–b3–b2–a2 | 4 | B |

A 原框為 P₀∪P₁，B 原框為 P₂∪P₃。這只是追蹤原邊的分解；
六個度數二的原頂點仍保留於 relation、面界及證書。

只有 x、y 的度數為四，其餘頂點度數為二，沒有環序選擇。
在每個端點把 P₀ 固定於循環串首，各有 3!=6 份環序，共 36 組。
在球面挖去 x、y 的小開圓盤，四條原路徑成為 annulus 的四條互斥
跨接弧；不交叉要求兩端由同一球面方向讀到的環序互為反序。
反向充分性可把四條弧畫成球面上的四條經線，再依原路徑插回原頂點。
因此恰有六份球面環序；各面由循環相鄰的兩條路徑圍成。

Checker 不把反序公式當作篩選輸入：它先遍歷全部 36 組，沿有向邊
逐面行走，核對每條有向邊恰被使用一次，再算 V−E+F。結果是六組
F=4、Euler=2；另外三十組 F=2、Euler=0，不是此圖的平面嵌入。
最後才核對 Euler=2 iff 原路徑次序反向。
三十組失敗是**環序不適用於球面**，不表示同一抽象圖非平面。

有向邊反向後取端點 clockwise 串的前一項，是本證書的右側面行走
慣例；逐面／Euler 檢查方式亦可對照
[NetworkX 官方 PlanarEmbedding 原始碼](https://networkx.org/documentation/stable/_modules/networkx/algorithms/planarity.html#PlanarEmbedding.check_structure)。
本 checker 僅使用標準函式庫，沒有呼叫 NetworkX 或 planarity oracle。
球面弧構造、Jordan 曲線分側與平面／球面的對應仍是紙面拓撲，未 Lean 化。

## 3. 指定外面後的 disk 與合法性條件

每份球面環序有四個面，逐一指定哪個面含無窮遠，得到 24 份具名配置。
保留鏡像，不按反射或圖自同構去重；這些數字不是新 class 數。
以下 D_A、D_B 是兩條原框在該平面嵌入中所圍的**有界閉 disk**。
包含型的兩條邊界仍在 x、y 相觸，不表示小閉 disk 與大 disk 邊界完全分離。

| D_A／D_B 關係 | 配置數 | A 是整圖外框 | B 是整圖外框 | 內部互斥政策 |
| --- | ---: | --- | --- | --- |
| 內部互斥，閉 disk 只交於 x、y | 8 | 否 | 否 | 通過 |
| D_B⊊D_A | 4 | 是 | 否 | 不通過 |
| D_A⊊D_B | 4 | 否 | 是 | 不通過 |
| 內部相交，兩側都有未重疊區 | 8 | 否 | 否 | 不通過 |

紙面分類如下。在端點環序中，若兩條 A 路徑相鄰，兩條 B 路徑也
相鄰，原框各圍出一個面。若外面選 A 面，有界 A disk 包住 B；
若選 B 面則反向。若外面選另外兩個混合面之一，兩個原 disk 內部
互斥。這種非交替環序共有四份，分別貢獻 4、4、8 份配置。

其餘兩份環序是 A、B 交替。每個原框在球面各分出兩面；無論四個面
中哪個選為外面，有界 A、B disk 都各佔兩面，交集恰佔一面，且各有
一個私有面。因此有八份真正重疊配置。兩條原框在共享頂點交替通過，
沒有邊內部交叉，整份圖仍是平面圖。

計算側別時，checker 在面對偶中刪去跨越原框邊的鄰接，獨立核對
剩下恰有兩個連通分量；含指定外面的分量就是 outside，另一個是
inside。它逐原邊保存 inside／outside／boundary，並保存按原具名
框序行走時，有界 disk 位於左側或右側。再直接比較兩個 inside 面集，
不從 relation mask 或預設合法 flag 決定區域類型。

### 具名見證

[Artifact](../artifacts/c5_two_vertex_overlap/reference_topology.json)的
`r5` 在 x 的路徑序是 `(0,1,2,3)`，在 y 是 `(0,3,2,1)`；四個面為：

| 面 ID | 循環頂點串 |
| --- | --- |
| 0 | a0,a1,a2,a3,a4，即 A 原框 |
| 1 | a0,a2,b2,b3,b4，即 B 原框 |
| 2 | a0,a4,a3,a2 |
| 3 | a0,b4,b3,b2,a2,a1 |

`r5-f0` 取面 0 為外面，給 D_B⊊D_A；`r5-f1` 給 D_A⊊D_B；
`r5-f2` 給內部互斥，此時 inside_A={0}、inside_B={1}。
只改外面就已改變兩份原 disk 的包含關係，故單存頂點 rotations 尚不足以
指定有界區域側別。

重疊見證 `r16-f0` 在 x、y 的路徑序分別是 `(0,2,1,3)`、`(0,3,1,2)`；
外面是三角形 a0–a1–a2，inside_A={2,3}、inside_B={1,2}，共同面為 2。
所有面界、原邊位置、框方向與完整 J 均可由 artifact 查回。

## 4. 八點 relation 不能直接解讀成一個八點 disk 框

此圖任何 simple cycle 都只能使用兩條完整的 x–y 路徑：度數二點
不能中途離開原路徑，而 simple cycle 在 x、y 各只使用兩條 incident 邊。
因此只有六種原邊 simple cycles，長度依序為 3、4、5、5、6、7；
沒有通過全部八個接口點的 simple cycle。平面嵌入的四個面界也都在此六者中。

所以完整八點 J 是具名接口 relation，不能將其欄序視為整圖的八點外框。
另一方面，在 `r5-f0` 的具體嵌入中，三個 B 私有接口點都位於 A disk
內部，確實給出原 A 框上 R1016 的 disk 實現。要在後續施工只保留
這五點投影，仍需明定被隱藏的三點及內部不再被未來操作接觸；本輪未
把這個存在見證提升為一般多步可替換性。

## 5. 證書、重播與信任界線

[新 checker](../scripts/c5_two_vertex_join_topology.py)讀取舊接合 artifact
並核對其來源 SHA；只選 `reference`，不修改舊六例的 geometry 欄位。
新 companion artifact 同時綁定舊 artifact 及新 checker 的 SHA-256，
保存原圖、原雙射、完整 J、兩份完整投影、全部 36 組環序、逐面串及
24 份指定外面的配置。所有統計均由重算結果比較，不讀取保存的接受 flag。

本輪另對主例全部 65,536 份八點賦色作逐邊重算，確認完整 J 及兩側
投影仍相等；這條計算不把既有 `geometry=unknown` 當作篩選條件。

```bash
python3 scripts/c5_two_vertex_join_topology.py
python3 scripts/c5_two_vertex_join_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-topology.md)。
本輪完成主例的固定圖拓撲分類；一般 transition 政策、其餘代表的原框
可行性、完整後繼表、多步摘要充分性、任意大小目錄完備性與
`K∞=K≤5` 均未完成。`lake build` 只驗既有 Lean，不形式化上述拓撲。
