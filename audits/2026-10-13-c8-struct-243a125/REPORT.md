# C8-STRUCT：十項殘留的原來源結構排除

2026-10-13。Repository `raylei50653/math`，指定 BASE 與開始 HEAD 均為
`243a125a80e4d8de40957f59d8da0bdbc974cf69`，開始工作樹乾淨。
本輪只作本地研究、程式、證明、文件與驗證，沒有 commit、push、PR 或 Issue。

## 1. 結果：排除 2 項，保留 8 項

**c16-941、c32-941 已對任意大小原來源排除。** 它們都是原最終支援 102 列
的查詢。新增原圖小分隔環定理先證 C₈ 無內弦；同圖 cofacial 識別與四色定理
再迫 `a1=a4` 的完整內側染色存在，但兩項的全部必要上界均禁止這個等式。
這不是有限圖搜尋，也不是只否定原先選中的計數向量。

其餘八項保留 **necessary-condition residual**。新的可逆 Kempe 計數條件
否定六份舊計數向量，並在 c15-941、c20-941 各普遍迫零兩個具名完整 fibres；
但這八項都有通過新增計數条件的精確新向量，因此沒有再計入整項排除。

| 查詢 | e 分配 | 舊最終支援 | 新結果 | 新必要支援 |
| --- | --- | ---: | --- | ---: |
| c15-933 | (0,1,2,0,0) | 134 | necessary-condition residual | 134 |
| c18-933 | (0,2,1,0,0) | 134 | necessary-condition residual | 134 |
| c04-941 | (0,0,1,0,2) | 193 | necessary-condition residual | 193 |
| c07-941 | (0,0,2,0,1) | 193 | necessary-condition residual | 193 |
| c15-941 | (0,1,2,0,0) | 173 | necessary-condition residual | 171 |
| c16-941 | (0,2,0,0,1) | 102 | **proved：來源排除** | — |
| c18-941 | (0,2,1,0,0) | 175 | necessary-condition residual | 175 |
| c20-941 | (1,0,0,0,2) | 173 | necessary-condition residual | 171 |
| c30-941 | (2,0,0,0,1) | 175 | necessary-condition residual | 175 |
| c32-941 | (2,0,1,0,0) | 102 | **proved：來源排除** | — |

連同上游 60 項，完整 70 項現為 **62 項排除、8 項未排**。
共同下界仍是 **h≥3、n₅≥9**；沒有採納 h≥4、n₅≥10、K≤13=K≤5 或 K∞=K≤5。
最終逐項狀態與八份完整新殘留（全部274座標、計數展開、軌道權重、十列
外框計數及迫零證書）集中於 [RESULTS.json](RESULTS.json)，由
[check_results.py](check_results.py) 對各份獨立子證書核對。

## 2. 完整原來源及具名分類

[SOURCE_CONTRACT.md](SOURCE_CONTRACT.md) 記錄全部來源量詞、原 B、具名 C₈、
三個私人點、完整附件、rotation、內面、同一 H 及同一 literal 色框。
沿用全域最小目錄外來源與既有度數／二邊 crosscut／分離三角形排除；
沒有加入 N2、ε=2、edge-critical、degree-4／degree-5 roots 或 Gallai 前提。

[完整具名分類](classification/CLASSIFICATION.md) 與
[分類證書](classification/classification.json) 保存十份原 274 座標向量、
全部十列外框計數、原邊、附件、完整支援及標號映射。只有下列五對等價：

* 933：c15 ↔ c18，原 B 反射 `b_i↦b_(3-i)`。
* 941：c04 ↔ c07、c15 ↔ c20、c18 ↔ c30、c16 ↔ c32，
  原 B 反射 `b_i↦b_(1-i)`。

每份映射同时搬運 apex、私人區間順序、全圖 embedding 與全部 full lifts；
checker 核對全部 13,700 個 transfer 係數。只有 c16/c32 的原計數向量在
搬運後相等，其餘對的原向量不成比例。等價依據是完整契約，而非支援大小。

## 3. 新普遍原圖定理及兩項排除

[小分隔環與無內弦證明](geometry/PROOF.md) 對任意有限大小來源成立：

1. 不含原 B 點於嚴格內側的 C₄ cap 沒有嚴格內點。
2. 完全在原 B 內側的 C₅ cap 為空，或恰為一個五度中心的 W₅。
3. 本域的具名 C₈ 必為 induced cycle。

證明先以既有 C₄／C₅ 小代表作保留完整 literal 關係的替換。全域最小性
把小 cap 的嚴格內點數分別界為 3／5。Euler 度數式與 outerplane 邊界
排除 C₄ 的所有非空核心及 C₅ 的 2–5 內點核心。C₈ 任一弦的短側長度
只能為 3、4、5；空 cap 產生違反度數的 ear，兩側皆 W₅ 則迫某私人點
在 H 中度數只有三，違反其原完整度數至少五。這是有普遍完備證明的有限核心。

進一步，任意具有 induced 外 C₈ 的平面 H，對每個不把相鄰點放在同一
block 的 noncrossing boundary partition，都有一份完整染色在各 block
上同色。理由是在 H 的外側嵌入各 block 的互不相交樹並收縮；無內弦
保證 quotient 沒有 loop，四色定理給染色，再拉回**同一原 H**。
這是 **proved** 的非空 fibre 必要條件，不是 equality 展開係數的正性假設。

兩項排除只需其中一個等式：

| 查詢 | 原 C₈ 中 a1、a4 的位置（0 起算） | 必要上界大小 | 上界內 a1=a4 列數 |
| --- | --- | ---: | ---: |
| c16-941 | 3、7 | 102 | 0 |
| c32-941 | 1、5 | 102 | 0 |

無內弦使 `a1a4` 不是原邊。單條外側弧的識別 quotient 已足以迫一份
`a1=a4` 的 H 完整染色；上界卻使該 fibre 為空，矛盾。
精確完整 preimages 與 91 個適用 partitions 的核對見
[quotient.json](classification/quotient.json)，普遍證明見
[QUOTIENT_PROOF.md](classification/QUOTIENT_PROOF.md)。
沒有使用實際來源枚舉，也沒有把 102 列上界當成實際完整關係。

## 4. 新普遍可逆 Kempe 計數條件

[Kempe 紙面證明](kempe/PROOF.md) 與 [精確證書](kempe/certificate.json)
使用固定互補色對 `01|23`。同一圖中的二色分量，在交換其任意子集後
保持同一頂點分割；交換是可逆的，完整軌道上的邊界 multiplicities 必
同步。於是共同延伸計數必為這些完整軌道向量的非負組合。

為保留固定 split 與共同 literal 色框，先使用其八元素色名穩定群的
821 列，而非把不同 splits 獨立正規化；再要求它們由同一 274 座標 x
拉回。一般 disk 的完整有限介面有 1,552 個不同軌道生成向量。
若 H 內面三角化，兩組色頂點之間的面內介面是互不相交弧與閉曲線；
碰邊界的分量 block 數為「邊界跨組邊数的一半加一」，得到 981 個生成向量。
所有內部大小只影響非負軌道權重，不影響此有限必要介面的完備性。

新證书逐项保存精確 x、共同有號 equality 係數、非負軌道權重、全部外框
計數與自身支援閉包；沒有假設 noncrossing equality 係數非負。
六份舊向量的精確分離泛函在全部 1,552 個一般 planar 生成向量上非負，
卻在舊向量上為負。因此它們是「舊必要條件已足以表示同圖可逆交換計數」
這個較弱宣稱的 **counterexample to weakened claim**，不是實際來源反例。

新的普遍迫零 fibres 為：

| 查詢 | 原 274 列索引 | 依原具名 C₈ 順序的 literal word |
| --- | --- | --- |
| c15-941 | 98、159 | `01201201`、`01210201` |
| c20-941 | 34、54 | `01020121`、`01021021` |

此處的迫零證明使用共同計數空間、原必要零列與可逆軌道非負性；在一般
1,552 生成向量中，逐一核對支援包含於該查詢原上界 U 的所有生成向量。
其餘生成向量因原零列已不能有正權重；不需要三角化加強。它排除四個完整 fibre 子域，
不能把相應兩項來源全排。其 171 列新向量在所有保留座標上同時為正。

Kempe 證書刻意保留十項的獨立計數階段：c16/c32 能通過此階段，但已在
§3 被原圖結構與四色定理排除。最終八份計數殘留还逐一滿足全部 91 個
cofacial 同色 fibre 的非空條件。這仍不構造任何圖。

## 5. 精確剩餘缺口

剩餘八項必須由一個**無內弦、內面三角化**的 H，同時實現原 apex 度數至少三、
三個私人點度數至少四、嚴格內點度數至少五、小分隔環定理、原附件及全部
十列 Σ。新殘留保存完整向量及軌道權重，但尚未證明這些權重來自同一 H
的實際分量、原面與跨不同 splits 的共同交換作用。

特別地，固定 split 的各個完整軌道之間，以及三個 complementary splits
之間，還沒有共同圖層的實現／不可能性定理。H 的原三角面第三點與 rotation
必須跨所有染色固定；度數及分隔限制尚未轉成能否定這八份殘留的新条件。
不能因各個軌道向量分別合法，就將其拼成同一圖。

既有五度輪 J_e 完整 fibre 雙射仍成立，但本輪沒有從 C₈ 向量選出同一
原五度輪的共同外部 full lift，也沒有迫出單步 escape 所需的 singleton
分量分離且避開 B。這是精確未證的同步結構條件，沒有被本輪的計數改善取代。

## 6. 驗證、控制與信任界線

根重播與實際驗證紀錄見 [VERIFICATION.md](VERIFICATION.md)；獨立 checker
使用 Python 標準庫及精確 Fraction，不以浮點 LP 狀態驗收。
SciPy 僅發現 Kempe 候選；完整有限介面另行獨立枚舉並核對每份原始軌道。
正常／seed17整包重播、負控制、59份凍結輸入雜湊及正式文件檢查通過。
全工作樹DocGraph仍有62項既有duplicate-ID失敗，完整輸出保留。

幾何的兩份有限圖是 **finite graph calibration**：去掉一點的二十面體
給六內點 C₅ cap，顯示局部度數本身不足以替代全域最小性；兩個 W₅ 沿邊
黏合顯示不能把私人點 H 度數四弱化為三。兩者均為
**counterexample to weakened claim**，不是最小 933／941 來源。
實際目標來源的構造控制為 **not triggered**。證書破壞控制與正常／seed17
重播分開記錄，不以零實際來源樣本宣稱排除。

新定理為紙面证明與經證明完備的有限介面／核心；沿用既有目錄與外部依賴，
並明列四色定理。沒有新增 Lean theorem，沒有以 `lake build` 代替本輪形式化。
所有舊證據、frozen inputs、manifest 及失敗紀錄保留。後續路由只更新
完整外圈權威入口、Kempe 導覽與 STATUS；README／HANDOFF 的研究線不變。
其他 session 的獨立 audit 不在本輪修改範圍。
本輪產物及允許修改範圍的精確雜湊見 [MANIFEST.json](MANIFEST.json)。
