# State／grammar／topology 與枚舉導覽

更新：2026-09-30。本頁整理既有研究；新增兩點重疊研究入口，該輪重播範圍見專題報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

釐清完整 boundary relation 的表示、接合與可安全迭代的 state，並維護
固定 grammar、cell 枚舉與 topology 橋接。固定模型的完備性不等於所有 disk 圖的完備性。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| C₅ class 兩點重疊 | 132 類點對、六份完整接合及主例拓撲完成；正反向私有內點例原框皆被阻斷；原 U 無輔助變數局部合取修復所需最大 arity 恰為四；固定 P 的全部 inclusion-minimal 四點修復為一組二份、十四組三份；其餘代表、政策及多步充分性保留 | [兩點重疊導覽](c5_two_vertex_overlap_guide.md)、[全部極小修復](c5_two_vertex_minimal_repairs.md) |
| 完整 relation／表示法 | Interface、State、Branch、Choice 及接合語意已有；pair projections 漏掉高階限制 | [state language](state_language.md)、[extension effects](extension_effects.md) |
| 逐步充分性／closure | strip／fan 有界控制與 separator 引理可用；一般移動前緣、context／future 充分性及 C6／C7 轉接待證或未啟動 | [充分性](stepwise_state_sufficiency.md)、[closure](local_closure.md)、[介面提案](c5_interface_idea.md) |
| Triangle grammar | 染色語義、attachment normal form、GeoReject 與 endpoint-order 編譯已有形式化；只限指定 grammar | [automata](automata.md)、[normal form](attachment_normal_form.md) |
| Embedding 到 grammar | 固定 C5＋K3 接線的紙面 topology 論證依賴 Jordan–Schoenflies 等事實；embedding 抽取與 topology soundness 未 Lean 化 | [topology](topology_completeness.md) |
| 固定 relation 庫／pp | 固定 grammar 的 87 states 與完整 relation 查詢保存；pp 求值器屬 Python，87 不等於一般 cell catalogue 的 132 | [relation 庫](boundary_relations.md)、[pp](pp_relations.md)、[fan](fan_pentagon.md) |
| Cell 枚舉 | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈及外部信任已明列；k=6、7 重現只是有界證據 | [enumerator](c5_cell_enumerator.md) |
| 基礎構造與 gadgets | exact relations、有限 Lean 證書與 gadget synthesis 已保存；一般 planar／separating C5 的 BAD 不是 disk 反例 | [phase 1](phase1.md)、[構造](construction.md)、[gadgets](gadgets.md) |

## 3. 停止點與保留缺口

兩個 class 各取兩點識別的新線，由[兩點重疊導覽](c5_two_vertex_overlap_guide.md)
維護一步接合的窄問題；它不啟動 C₆／C₇ 轉接。

一般 context／future 充分性與 grammar 外的 topology 仍未完成；不把一次重建
或有界實驗提升為多步可安全合併的 state。`geometry=unknown` 的 rows 不是 disk transitions。
Topology 論證只處理原報告的接線圖，不能代表任意較大 patch；形式化依賴見
[Lean 導覽](lean_guide.md)。本次不另啟動枚舉或 C6／C7 轉接工作。

## 4. 閱讀與重播入口

表示法先讀 state language，再讀充分性與 local closure；grammar 先讀 automata、
attachment normal form，再讀 topology 的精確範圍。枚舉的算法、檢查命令與
信任拆分以 enumerator 報告為準。所有 artifacts 保留原範圍與來源；
本次沒有重新生成 catalogue，也未重跑 closure 或 Lean audit。
