# State／grammar／topology 與枚舉導覽

## 最新進度

現況核對：2026-10-20；[殘餘候選迭代](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)以實際傳輸再共同篩選，對任意有限歷史保完整軌跡；固定95圖336個非空殘餘態，384條舊假路徑全拒絕。互補phase可合併翻轉奇偶，但須保中途篩選；一般壓縮與J1仍OPEN。[P/R來源覆蓋](../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md)仍OPEN。

| 欄位 | 現況 |
| --- | --- |
| 階段／生命週期 | 研究中；完整表示、指定 grammar 與有界枚舉已有成果，一般可迭代 state 充分性待證。F／Z 為待初驗提案，域外構造研究已交付。 |
| 最近研究更新 | 2026-10-20：[殘餘迭代](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)完成任意有限歷史正確性、固定圖完整集合閉包及保篩選的phase公式；一般小狀態界與J1仍OPEN。 |
| 上次完成 | 固定95圖336非空殘餘態，384假路徑全拒絕；72個雙候選皆有試探／還原方案，48個用2次交換、24個用4次，染色回原點而候選只留一份。 |
| 目前停止點 | 精確候選集合可迭代，主動辨識有條件嚴格下降，但總狀態數未壓縮；同J不能代替同殘餘集合，phase不能丟中途觀測。一般有界表示、圖大小下降與J1仍OPEN。 |
| 下一步 | 對具名J1動作，以精確殘餘更新作語義基線，尋能保傳輸／篩選的較小surgery描述，並保來源回溯及接回成本；候選數不增不能當較小bad。P/R另尋來源代表。 |
| 接手入口 | 先讀[迭代規則與重播](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)及[一般紙面語義](../audits/2026-10-20-kempe-residual-iteration-af0df80/theory/REPORT.md)；J1沿[來源合同](../audits/2026-10-20-joint-kempe-state-1148ce0/theory/REPORT.md)，P/R讀[來源覆蓋](../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md)。 |

### 近期里程碑

| 日期／階段 | 進展與來源 |
| --- | --- |
| 2026-10-15／共同原圖與二層cover | [必要表階數](../audits/2026-10-15-f4-relation-6ddea32/REPORT.md)及[二層共同圖](../audits/2026-10-15-kempe-state-covers-6ddea32/REPORT.md)分開精確關係、抽象交換與真圖多值lift；原平面來源及一般充分性仍OPEN。 |
| 2026-10-19／三探測完整解碼 | [有限P/R模型](../audits/2026-10-19-c5-observation-depth-ed59843/REPORT.md)中，四列未來行為需要全部132態；三個指定後綴已能還原十列，圖層語義與來源覆蓋另證。 |
| 2026-10-19／任意disk的P/R語義 | [完整fibre雙射](../audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md)將三探測推到任意大小disk的十列固定字面計數；一般文法代表覆蓋保留OPEN。 |
| 2026-10-20／來源覆蓋界線 | [精確合同與反控制](../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md)證一般計數代表不存在；支援覆蓋等價原分類，P吸收及幾何可剝子類皆不關閉一般義務。 |
| 2026-10-20／聯合觀測到精確迭代 | [三台同步](../audits/2026-10-20-multi-kempe-machines-af0df80/REPORT.md)定位384條假路徑；[殘餘迭代](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)以傳輸＋篩選全排，固定圖336個非空集合；一般壓縮及J1仍OPEN。 |

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
| 同染色聯合Kempe狀態 | 六分割不足以逐步更新；精確殘餘經實際傳輸／共同篩選可保任意有限歷史。固定95圖336非空集合、在線最多2候選，384假路徑全排；互補phase保parity及存活遮罩。一般壓縮及J1仍OPEN | [迭代規則與證書](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)、[多機診斷](../audits/2026-10-20-multi-kempe-machines-af0df80/REPORT.md)、[原反例](../audits/2026-10-20-joint-kempe-state-1148ce0/REPORT.md) |
| 七接點必要表與Kempe共同圖 | 固定26列上界的投影階數恰6；全部五點投影誤收96份賦色。特定720交換模型無單值共同圖，但Layer0有非平面二層真圖；未證完整720、平面來源或一般後繼充分性 | [有限域與階數](../audits/2026-10-15-f4-relation-6ddea32/REPORT.md)、[單值障礙](../audits/2026-10-15-kempe-common-graph-6ddea32/REPORT.md)、[二層共同圖](../audits/2026-10-15-kempe-state-covers-6ddea32/REPORT.md) |
| 來源階數／接合上界 | 132類有11個二階、101個四階、20個五階；精確接合r*≤來源最大階數≤5，T4全收來源≤4；六圖回歸，不證忘掉接點後或多步的同一上界，未Lean化 | [階數報告](c5_relation_arity.md) |
| C₅ class 兩點重疊 | 新十三點 D₁₃ 完整四接點替換給任意大小同 class 族，私有四度點只成孤點及配對，輪環與偶長雙扇都無縮減起點；保持完整 J/P、全部外框、十五組 repairs／r*=4；加入 D₁₃ 後其餘骨架、必要分類／政策與多步充分性未證 | [兩點重疊導覽](c5_two_vertex_overlap_guide.md)、[D₁₃ 定理](c5_two_vertex_repair_caps.md) |
| 完整 relation／表示法 | Interface、State、Branch、Choice 及接合語意已有；pair projections 漏掉高階限制 | [state language](state_language.md)、[extension effects](extension_effects.md) |
| 單點強迫／閉環一致猜想 | F 問低超額刪邊強迫對的統一介面寬度；Z 問固定可延拓邊界的零邊數不增修復，均未初驗。半徑與寬度分開；邊差可積分沿用已有等價，不新增閉包或來源排除 | [完整猜想與驗證計畫](c5_forcing_transport_conjectures.md) |
| 強迫異色的距離／不交叉 | 一般平面圖有任意遠強迫對且證書寬度≤5；共用雙支援樹恰 path 可平面、交錯獨立 Diff×Diff 不可實現。邊界外 clique 分隔枝塊對 Σ 透明，原 critical／低超額來源未觸發，無新 Lean | [構造、證明及完整 fibres](c5_forced_inequality_transport.md) |
| 逐步充分性／closure | strip／fan 有界控制與 separator 引理可用；一般移動前緣、context／future 充分性及 C6／C7 轉接待證或未啟動 | [充分性](stepwise_state_sufficiency.md)、[closure](local_closure.md)、[介面提案](c5_interface_idea.md) |
| Triangle grammar | 染色語義、attachment normal form、GeoReject 與 endpoint-order 編譯已有形式化；只限指定 grammar | [automata](automata.md)、[normal form](attachment_normal_form.md) |
| P/R 文法 v0.2 附件 | 所附132態／264轉移模型核對一致；319有56 Live／76 Dead，F及F/C文法最大最小成本為6／5。原程式／測試未隨附；後續以明定實圖操作獨立重建，未證一般覆蓋 | [匯入範圍、原檔與完整性核對](sources/2026-10-19-c5-grammar-v02/README.md) |
| P/R四列三步解碼 | 最小統一深度3，59對需三步；深度≤3唯一最小探測集合RR／PRR／RRR重建全部十列，適用1024形式mask；文法族四列最小機器132態。圖語義及計數升級由下項完成 | [代數證明、見證及三路重播](../audits/2026-10-19-c5-observation-depth-ed59843/REPORT.md) |
| P/R實圖語義與計數解碼 | 任意大小disk上，明定外側push／右轉合法且完整fibre轉移等於附件整數矩陣；三探測解碼十列支援／固定字面計數。5120局部指派與792圖／7920完整fibres重建；一般F/C代表覆蓋及新Lean仍OPEN | [任意大小證明、獨立圖重播及計數證書](../audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md) |
| P/R文法來源覆蓋 | 保全部未來四列支援等價完整十列相等；一般計數代表由C5內葉點反駁。933／941首次P入K、932六態殘留；固定17P外補把任意非空支援送1023，會改框增點。逆P／三角星剝除給充分子類，一般支援及r6覆蓋OPEN，無新Lean | [精確量詞、任意字串定理與真圖證書](../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md) |
| Embedding 到 grammar | 固定 C5＋K3 接線的紙面 topology 論證依賴 Jordan–Schoenflies 等事實；embedding 抽取與 topology soundness 未 Lean 化 | [topology](topology_completeness.md) |
| 固定 relation 庫／pp | 固定 grammar 的 87 states 與完整 relation 查詢保存；pp 求值器屬 Python，87 不等於一般 cell catalogue 的 132 | [relation 庫](boundary_relations.md)、[pp](pp_relations.md)、[fan](fan_pentagon.md) |
| Cell 枚舉 | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈及外部信任已明列；k=6、7 重現只是有界證據 | [enumerator](c5_cell_enumerator.md) |
| C₅ 組合與結構分類 | 完整 1,023 個 raw masks 分成 135 個 D₅ 類；必要條件 153→142、已知 132／24 類與 OPEN 10／2 類分層。Burnside、全部 witness 與原證書重播；兩側對齊交集覆蓋 1,023 不等於單側實現 | [圖譜、資料與重播](c5_combinatorial_atlas.md) |
| Cell 翻邊／編碼 | 四格完整關係給保 Σ 充要條件；五格加五格座標使旋轉及加邊界弦成 bit 操作。同 Σ、同操作反例及同逐列計數反例排除一般直接更新；指定 flip 可用四十位元四格 support，迭代仍保存實圖／full lifts；未 Lean 化 | [翻邊引理、工具與編碼](c5_cell_flip.md) |
| Cell 翻邊分類 | 132 份原代表作三步實圖 BFS：20,531 圖、29 組距離特徵，完整 132×132 有向距離表；1,179 個初始翻邊全改 Σ。120 份一步到較小目錄代表的關係，W5 要兩步；限指定代表與嵌入規則，未得一般縮減 | [距離與分類](c5_cell_flip_classification.md) |
| K₄ 非平面障礙偵測 | K₄＋同一外部分量四接點輸出原圖 K₅ minor；Atlas 161／237、平面零誤報，603 命中；漏判含無 K₅ minor 及無字面 K₄ 兩類，不能取代完整判定，未 Lean 化 | [效果、證書與漏判分類](k4_nonplanarity.md) |
| 基礎構造與 gadgets | exact relations、有限 Lean 證書與 gadget synthesis 已保存；一般 planar／separating C5 的 BAD 不是 disk 反例 | [phase 1](phase1.md)、[構造](construction.md)、[gadgets](gadgets.md) |

## 3. 停止點與保留缺口

2026-10-20的[殘餘候選迭代](../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)
完成`R'=T_a(R)∩J^{-1}(o)`的任意有限歷史正確性；只以完全相同的當前
集合共用未來狀態，回溯原始來源仍另保對應。固定95圖閉包336個非空
集合，已拒絕下列384條假路徑。互補phase可合併分量翻轉，但中途觀測
的存活遮罩不能消掉；主動試探再反序還原可保實際染色並縮小候選，
固定圖72個雙候選全部在至多4次交換後識別。一般較小表示及圖大小下降仍OPEN。

2026-10-20的[三台同步試驗](../audits/2026-10-20-multi-kempe-machines-af0df80/REPORT.md)
把六分割拆成三個互補色對觀測器；各台對自身alphabet可精確更新，
但共同摘要仍不能承擔全alphabet更新。固定95圖靜態同框及單步後繼
乘積均無額外假組合，摘要圖卻有384條無共同完整軌跡的兩步路徑，
甚至可違反同一交換連做兩次返回的對合律。上述後續以精確候選完成
迭代；更小充分表示仍待證，全分支細分不等於任意實際歷史的識別能力。

2026-10-20的[同染色聯合Kempe初驗](../audits/2026-10-20-joint-kempe-state-1148ce0/REPORT.md)
區分同一完整染色的joint觀測與可迭代狀態。六分割精確保存一步框色回應，
但同一八點圖的兩份染色在第二步框色已不同；一般逐步充分性因此否定。
固定95圖的加接點修正為完整染色的單射編碼，未提供一般小狀態界。
下一版可對指定實際分量保存四個混合色對的刪後分量與附件quotient；
既有surgery只保證單步，下一步descriptor仍須由實際染色重算或另證更新。
J1六格須由同一原核心完整染色形成，hidden swaps不能省略；原兩項拒絕仍OPEN。

2026-10-19的[四列三步解碼](../audits/2026-10-19-c5-observation-depth-ed59843/REPORT.md)
完成矩陣層觀察深度及重編碼；後續[實圖語義](../audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md)
證明定外側push／右轉在任意大小disk合法，完整字面fibre雙射給相同整數矩陣，
故三探測可恢復任意這類disk的十列支援與計數；文法族132種四列行為仍不可合併。
2026-10-20的[來源覆蓋審核](../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md)
證這種行為代表恰要求同一來源完整十列支援；一般計數／fibre雙射代表已被真圖反例否定，
不能將它當成原支援覆蓋的必要條件。933／941的每個含P後繼都在K132，
932另留六個K外態；後繼可代表不反推原框可代表。
固定共同字串可用17次P將所有非空支援送1023，但改框且增加17個內點，不能供應原來源下降。
逆P與內三度三角星剝除給任意大小的條件式覆蓋，但無此剝除的真disk仍可有C代表。
下一窄義務仍是具名原來源的同一完整十列支援代表，或計入接回成本的成功／更小bad下降。
原歷史程式仍缺，一般支援來源覆蓋及主命題仍OPEN。

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
