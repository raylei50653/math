# State／grammar／topology 與枚舉導覽

## 最新進度

現況核對：2026-10-16；既有必要表／Layer0成果保留；[319續進](../audits/2026-10-16-r6-319-complete-e98a1cc/REPORT.md)補全U的紙面fibre雙射及平面ordinary/even反控制，原來源偶補正值仍OPEN；完整720態平面cover暫緩，一般state充分性仍OPEN。

| 欄位 | 現況 |
| --- | --- |
| 階段／生命週期 | 研究中；完整表示、指定 grammar 與有界枚舉已有成果，一般可迭代 state 充分性待證。F／Z 為待初驗提案，域外構造研究已交付。 |
| 最近研究更新 | 2026-10-15：[四輪具名模型](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)分開必要表階數、抽象交換相容性、單值section障礙及Layer0二層共同原圖。 |
| 上次完成 | 固定26列必要表階數恰6；720態交換公理模型存在但無相容單值共同圖；Layer0有75／121點二層共同圖，各864份完整染色，兩圖非平面。 |
| 目前停止點 | 域外無界例不觸發原低超額 critical 前提；F／Z 仍 OPEN。一般 context／future、刪內邊與 Kempe 的後繼充分性、grammar 外 topology 及全部來源必要分類均未完成。 |
| 下一步 | 接續 §3：在具名前提觸發的實際來源量測半徑與完整證書寬度；同一 β 下檢查非 clique 分隔介面的支援／超額。Z 另查完整不增轉移圖的終端平台。 |
| 接手入口 | 先讀本頁 §3，再讀 [F／Z 的量詞與初驗計畫](c5_forcing_transport_conjectures.md)、[異色構造及原域界線](c5_forced_inequality_transport.md)；多步接口見 [Phase B](c5_phase_b_common_lemmas.md)，兩點接合見 [專線導覽](c5_two_vertex_overlap_guide.md)。 |

### 近期里程碑

| 日期／階段 | 進展與來源 |
| --- | --- |
| 2026-10-15／共同原圖與二層cover | [必要表階數](../audits/2026-10-15-f4-relation-6ddea32/REPORT.md)及[二層共同圖](../audits/2026-10-15-kempe-state-covers-6ddea32/REPORT.md)分開精確關係、抽象交換與真圖多值lift；原平面來源及一般充分性仍OPEN。 |
| 2026-10-02／來源階數初驗 | [階數報告](c5_relation_arity.md)將 132 來源分為 11 個二階、101 個四階、20 個五階，證精確兩來源接合 r*≤來源最大階數≤5；忘掉接點及多步上界未證。 |
| 2026-10-08／共通接口 | [Phase B](c5_phase_b_common_lemmas.md)分開密封外部接合、保 action 的後繼充分性與刪邊 weak bisimulation；接續義務為指定 grammar、幾何 residual 與同一染色 fibre 匹配。 |
| 2026-10-11／提案形成 | [強迫同色與閉環一致](c5_forcing_transport_conjectures.md)明確化 F 的有界介面證書與 Z 的零邊數不增修復；當輪只整理提案，兩項均未初驗。 |
| 2026-10-13／域外構造與原域收窄 | [強迫異色](c5_forced_inequality_transport.md)證一般距離無界、寬度≤5及不交叉限制，排巢狀 clique／割點接力作原 critical 來源；下一入口收窄至固定 β 的非 clique 介面。 |

來源投影階數與精確接合上界及跨線整理見
[全線進展與高階假設](c5_research_synthesis.md)，實際重播範圍見專題報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

釐清完整 boundary relation 的表示、接合與可安全迭代的 state，並維護
固定 grammar、cell 枚舉與 topology 橋接。固定模型的完備性不等於所有 disk 圖的完備性。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 七接點必要表與Kempe共同圖 | 固定26列上界的投影階數恰6；全部五點投影誤收96份賦色。特定720交換模型無單值共同圖，但Layer0有非平面二層真圖；未證完整720、平面來源或一般後繼充分性 | [有限域與階數](../audits/2026-10-15-f4-relation-6ddea32/REPORT.md)、[單值障礙](../audits/2026-10-15-kempe-common-graph-6ddea32/REPORT.md)、[二層共同圖](../audits/2026-10-15-kempe-state-covers-6ddea32/REPORT.md) |
| 來源階數／接合上界 | 132類有11個二階、101個四階、20個五階；精確接合r*≤來源最大階數≤5，T4全收來源≤4；六圖回歸，不證忘掉接點後或多步的同一上界，未Lean化 | [階數報告](c5_relation_arity.md) |
| C₅ class 兩點重疊 | 新十三點 D₁₃ 完整四接點替換給任意大小同 class 族，私有四度點只成孤點及配對，輪環與偶長雙扇都無縮減起點；保持完整 J/P、全部外框、十五組 repairs／r*=4；加入 D₁₃ 後其餘骨架、必要分類／政策與多步充分性未證 | [兩點重疊導覽](c5_two_vertex_overlap_guide.md)、[D₁₃ 定理](c5_two_vertex_repair_caps.md) |
| 完整 relation／表示法 | Interface、State、Branch、Choice 及接合語意已有；pair projections 漏掉高階限制 | [state language](state_language.md)、[extension effects](extension_effects.md) |
| 單點強迫／閉環一致猜想 | F 問低超額刪邊強迫對的統一介面寬度；Z 問固定可延拓邊界的零邊數不增修復，均未初驗。半徑與寬度分開；邊差可積分沿用已有等價，不新增閉包或來源排除 | [完整猜想與驗證計畫](c5_forcing_transport_conjectures.md) |
| 強迫異色的距離／不交叉 | 一般平面圖有任意遠強迫對且證書寬度≤5；共用雙支援樹恰 path 可平面、交錯獨立 Diff×Diff 不可實現。邊界外 clique 分隔枝塊對 Σ 透明，原 critical／低超額來源未觸發，無新 Lean | [構造、證明及完整 fibres](c5_forced_inequality_transport.md) |
| 逐步充分性／closure | strip／fan 有界控制與 separator 引理可用；一般移動前緣、context／future 充分性及 C6／C7 轉接待證或未啟動 | [充分性](stepwise_state_sufficiency.md)、[closure](local_closure.md)、[介面提案](c5_interface_idea.md) |
| Triangle grammar | 染色語義、attachment normal form、GeoReject 與 endpoint-order 編譯已有形式化；只限指定 grammar | [automata](automata.md)、[normal form](attachment_normal_form.md) |
| Embedding 到 grammar | 固定 C5＋K3 接線的紙面 topology 論證依賴 Jordan–Schoenflies 等事實；embedding 抽取與 topology soundness 未 Lean 化 | [topology](topology_completeness.md) |
| 固定 relation 庫／pp | 固定 grammar 的 87 states 與完整 relation 查詢保存；pp 求值器屬 Python，87 不等於一般 cell catalogue 的 132 | [relation 庫](boundary_relations.md)、[pp](pp_relations.md)、[fan](fan_pentagon.md) |
| Cell 枚舉 | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈及外部信任已明列；k=6、7 重現只是有界證據 | [enumerator](c5_cell_enumerator.md) |
| C₅ 組合與結構分類 | 完整 1,023 個 raw masks 分成 135 個 D₅ 類；必要條件 153→142、已知 132／24 類與 OPEN 10／2 類分層。Burnside、全部 witness 與原證書重播；兩側對齊交集覆蓋 1,023 不等於單側實現 | [圖譜、資料與重播](c5_combinatorial_atlas.md) |
| Cell 翻邊／編碼 | 四格完整關係給保 Σ 充要條件；五格加五格座標使旋轉及加邊界弦成 bit 操作。同 Σ、同操作反例及同逐列計數反例排除一般直接更新；指定 flip 可用四十位元四格 support，迭代仍保存實圖／full lifts；未 Lean 化 | [翻邊引理、工具與編碼](c5_cell_flip.md) |
| Cell 翻邊分類 | 132 份原代表作三步實圖 BFS：20,531 圖、29 組距離特徵，完整 132×132 有向距離表；1,179 個初始翻邊全改 Σ。120 份一步到較小目錄代表的關係，W5 要兩步；限指定代表與嵌入規則，未得一般縮減 | [距離與分類](c5_cell_flip_classification.md) |
| K₄ 非平面障礙偵測 | K₄＋同一外部分量四接點輸出原圖 K₅ minor；Atlas 161／237、平面零誤報，603 命中；漏判含無 K₅ minor 及無字面 K₄ 兩類，不能取代完整判定，未 Lean 化 | [效果、證書與漏判分類](k4_nonplanarity.md) |
| 基礎構造與 gadgets | exact relations、有限 Lean 證書與 gadget synthesis 已保存；一般 planar／separating C5 的 BAD 不是 disk 反例 | [phase 1](phase1.md)、[構造](construction.md)、[gadgets](gadgets.md) |

## 3. 停止點與保留缺口

2026-10-15的[具名模型續進](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)
沒有把抽象state指定成真來源。Layer0二層共同圖只覆18列，完整720／22列、
其他平面實現及原degree／collar來源均OPEN；不能假設每份cover有交換相容單值section。
其原來源接回義務由[Kempe導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護，
不取代本頁F／Z的具名初驗及一般多步充分性問題。
2026-10-16的[319完整fibres續進](../audits/2026-10-16-r6-319-complete-e98a1cc/REPORT.md)
為舊22列screen補上實際Kempe分量紙面雙射，未縮小舊screen；新平面反控制的完整U支持為
1016／967且有違規lifts，不是完整319來源，也不供應完整720態cover。

新增提案見[強迫同色與閉環一致](c5_forcing_transport_conjectures.md)：先在具名前提觸發的
實際來源量測局部半徑及完整關係證書寬度；零邊修復另檢查完整不增轉移圖的終端平台。
F／Z 的原來源域仍未完成初驗，亦不據此退役既有窄定理。
後續[異色構造研究](c5_forced_inequality_transport.md)已證一般平面圖距離無界，
並排除其巢狀 clique／割點接力作原 critical 來源；下一步限縮到同一 β 下
非 clique 分隔介面的完整支援與超額，不能把域外無界例當成原域反例。

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

組合分類由[圖譜入口](c5_combinatorial_atlas.md)展開原始 masks、對稱轉換、必要條件、
witness 與描述性結構；`.venv/bin/python scripts/c5_combinatorial_atlas.py --check`
重算並逐 byte 比對全部圖譜產物，不修改 production Σ 或原證書。

跨線初驗以 `python3 scripts/c5_relation_arity_audit.py --check` 重播132份既有
關係、20個五階原圖及六個具名接合；詳見[紀錄](history/2026-10-02-c5-research-synthesis.md)。
若後續試找r*=5，至少一個來源須在已列出的20類中；實際合法框族仍另證。
