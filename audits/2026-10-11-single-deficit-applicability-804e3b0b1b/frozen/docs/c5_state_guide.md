# State／grammar／topology 與枚舉導覽

更新：2026-10-02。新增來源投影階數與精確接合上界；跨線整理見
[全線進展與高階假設](c5_research_synthesis.md)，實際重播範圍見專題報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

釐清完整 boundary relation 的表示、接合與可安全迭代的 state，並維護
固定 grammar、cell 枚舉與 topology 橋接。固定模型的完備性不等於所有 disk 圖的完備性。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 來源階數／接合上界 | 132類有11個二階、101個四階、20個五階；精確接合r*≤來源最大階數≤5，T4全收來源≤4；六圖回歸，不證忘掉接點後或多步的同一上界，未Lean化 | [階數報告](c5_relation_arity.md) |
| C₅ class 兩點重疊 | 新十三點 D₁₃ 完整四接點替換給任意大小同 class 族，私有四度點只成孤點及配對，輪環與偶長雙扇都無縮減起點；保持完整 J/P、全部外框、十五組 repairs／r*=4；加入 D₁₃ 後其餘骨架、必要分類／政策與多步充分性未證 | [兩點重疊導覽](c5_two_vertex_overlap_guide.md)、[D₁₃ 定理](c5_two_vertex_repair_caps.md) |
| 完整 relation／表示法 | Interface、State、Branch、Choice 及接合語意已有；pair projections 漏掉高階限制 | [state language](state_language.md)、[extension effects](extension_effects.md) |
| 逐步充分性／closure | strip／fan 有界控制與 separator 引理可用；一般移動前緣、context／future 充分性及 C6／C7 轉接待證或未啟動 | [充分性](stepwise_state_sufficiency.md)、[closure](local_closure.md)、[介面提案](c5_interface_idea.md) |
| Triangle grammar | 染色語義、attachment normal form、GeoReject 與 endpoint-order 編譯已有形式化；只限指定 grammar | [automata](automata.md)、[normal form](attachment_normal_form.md) |
| Embedding 到 grammar | 固定 C5＋K3 接線的紙面 topology 論證依賴 Jordan–Schoenflies 等事實；embedding 抽取與 topology soundness 未 Lean 化 | [topology](topology_completeness.md) |
| 固定 relation 庫／pp | 固定 grammar 的 87 states 與完整 relation 查詢保存；pp 求值器屬 Python，87 不等於一般 cell catalogue 的 132 | [relation 庫](boundary_relations.md)、[pp](pp_relations.md)、[fan](fan_pentagon.md) |
| Cell 枚舉 | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈及外部信任已明列；k=6、7 重現只是有界證據 | [enumerator](c5_cell_enumerator.md) |
| 基礎構造與 gadgets | exact relations、有限 Lean 證書與 gadget synthesis 已保存；一般 planar／separating C5 的 BAD 不是 disk 反例 | [phase 1](phase1.md)、[構造](construction.md)、[gadgets](gadgets.md) |

## 3. 停止點與保留缺口

跨線接續（2026-10-08）：[Phase B 分析](c5_phase_b_common_lemmas.md)區分
可反覆使用的密封外部接合、保action的後繼充分性與刪邊weak bisimulation。
窄義務是固定允許grammar、exact幾何residual及同一中間染色fibre的匹配；
一般context／future、內邊刪除與Kempe充分性仍未證。

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
本次沒有重新生成 catalogue，也未重跑舊 local-closure 實驗或 Lean axiom audit。

跨線初驗以 `python3 scripts/c5_relation_arity_audit.py --check` 重播132份既有
關係、20個五階原圖及六個具名接合；詳見[紀錄](history/2026-10-02-c5-research-synthesis.md)。
若後續試找r*=5，至少一個來源須在已列出的20類中；實際合法框族仍另證。
