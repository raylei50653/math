# 既有成果查找與使用

## 研究概況與閱讀入口

本頁協助研究者依當輪要做的操作，找到可引用的語義、接口與結構結果。
先選下表的用途，再讀來源的完整前提；目前採納結論與 OPEN 由[活躍結論](../research/CONCLUSIONS.md)維護。
原報告保存完整證明、資料及當輪停止點，不逐輪承擔另一套現況。
接續主攻由 [4CT 研究契約](../research/4ct_guide.md#精確消元主線的研究契約)進入，
查舊結果的後續涵蓋關係由[封存導覽](../archive/archive_guide.md)進入。

## 依用途選來源

| 要完成的工作 | 優先查閱 | 引用前核對 |
| --- | --- | --- |
| 保留全部解，消元後在最後共同回寫 | [完整解空間與接口語義](../tools/solver/four_color_mathematical_model.md)、[精確消元與回寫](../tools/solver/four_color_completeness.md) | 原因子、完整有序 scope、全部歷史 fibres 與同一份回寫見證；保解等式本身不證非空。 |
| 分解一次消元，或比較按需查詢與完整表 | [有限域分解](../tools/solver/four_color_bounded_projection.md)、[工具導覽](../tools/four_color_guide.md) | 至多 q 個原因子的敘述不限制變數數量；需對完整 bucket 核對，成本與執行上限另查。 |
| 判斷局部來源是否能在共同外圖成立 | [跨 split 來源限制](../archive/reports/planar-sources/four_color_three_step_cross_split_exclusion.md)、[分隔路完整 fibres](../archive/reports/planar-sources/four_color_three_step_separator_fibres.md) | 同一原嵌入、同一原側圖、全部附件及所有同切口 lifts；指定來源類排除尚未覆蓋一般多圈外圖。 |
| 在交換後檢查遠端連接與共同限制 | [遠端交換全割準則](../archive/reports/planar-sources/four_color_three_step_remote_cut.md)、[完整 Kempe 回返](../archive/reports/c5/connections/c5_kempe_blocked_realizability.md) | 交換須在同一完整染色上進行，並重算實際雙色分量；全部原 O、空 fibres 與遠端附件都保留。 |
| 調用 C₅ 的局部結構化約或關係替換 | [跨線共通語言與前提對照](c5/c5_common_language.md)、[下節的專門導覽](#按所需結構進一步查找) | 先分清固定 q-core 與完整 Σ 來源、原圖與 core 的臨界性、完整 degree、disk／T4 及密封接觸範圍。 |
| 判斷 E932、4CT 與舊 C₅ 分類的關係 | [E932⇔4CT 的紙面橋樑](../archive/reports/c5/structure/c5_kempe_screen.md)、[原分類主命題對照](../research/4ct_guide.md#與原c5分類主命題的關係) | 已證等價橋樑，尚未獨立證 E932；933／941 及一般有界代表分類保留各自義務。 |
| 檢驗某一具名結論的證明與重播 | [Lean 導覽](../verification/lean_guide.md)及該來源的證據／重播章節 | theorem、公理與 build target、Python 固定域、原資料版本與 SHA 分別核對；`limit` 不作排除證據。 |

這些入口按用途整理，表格不宣告新的蘊涵或完成狀態。引用局部結果時，把適用圖類、
全部假設與證據層一起帶入；需要更詳細的分支或證書時，再沿原報告展開。

## 共通使用契約

一次組合回到**同一原圖、同一色框、同一份共同見證**。有序接口記錄完整可行 tuples，
每一列保存全部延拓的 fibre，包含空 fibre；對齊實際接點與共同色框後再接合。
端點可用色、兩兩投影或各自非空，都不足以選出一份共同指派。
先傳播與消元，最後沿完整歷史倒序回寫；精確定義見[解空間語義](../tools/solver/four_color_mathematical_model.md)。

圖層替換另核 ownership、原附件與後續允許接觸的點。靜態關係相等可在已證上下文中使用；
多步操作、可用框族或新外接點須履行各來源的額外條件。
既有[跨線對照](c5/c5_common_language.md)保留代表性結果、完整前提與共用引理名稱。

## 按所需結構進一步查找

下列原研究線導覽作次級索引，供已定位問題後查依賴、來源與證書。
每次只展開所需分支；導覽中的舊研究更新日期與里程碑保留當時語境。

| 所需結構或操作 | 次級入口 |
| --- | --- |
| 固定 q-core、單側／共同出口、no-mixed 與 mixed 分支 | [Weak-deletion 導覽](../archive/guides/c5_weak_deletion_guide.md) |
| 兩點接合、完整 J／P、repair 與密封替換 | [兩點重疊導覽](../archive/guides/c5_two_vertex_overlap_guide.md) |
| 全 degree-4 的 block 與任意大小化約 | [Degree-4 導覽](../archive/guides/c5_degree4_guide.md) |
| Degree-5 roots、R 系列與實際附件 | [Degree-5 導覽](../archive/guides/c5_degree5_guide.md) |
| 雙拒絕、sector 與原來源分類 | [Sector 導覽](../archive/guides/c5_sector_3903_guide.md) |
| 猜想 E、超額、單／雙 spoke 與 Kempe 來源 | [Kempe 導覽](../archive/guides/c5_kempe_guide.md) |
| Grammar、拓撲與固定域枚舉 | [State 導覽](../archive/guides/c5_state_guide.md) |

## 從局部結果回到研究問題

一般來源覆蓋與共同存在性仍缺。E932⇔4CT 的等價、指定來源子類排除、
有限計算零殘留及具名替換，都須按原範圍引用；子分支收尾不推升父題。
目前主攻及接續義務由[研究契約](../research/4ct_guide.md#第一個接續工作)維護，
本頁僅協助選取能支援該工作的既有能力。

要查特定報告或當輪紀錄，使用[完整索引](../STATUS.md)及[封存導覽](../archive/archive_guide.md)。
文件維護與證據界線見[DOCUMENTATION](../DOCUMENTATION.md)。
