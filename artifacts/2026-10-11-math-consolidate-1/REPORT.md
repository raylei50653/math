# MATH-CONSOLIDATE-1：N45 已知成果整編與證明壓縮報告

2026-10-11；repository `raylei50653/math`；數學狀態與壓縮預覽的讀取基準為
`8c56b76922a1c7ac4c011096f2041b49c4a67cc8`（`docs(math): adopt BR-SD-1g scoped exclusion`）。
**整編提案已完成；現有canonical與全部既有tracked files未修改，沒有採納新定理或發布。**

## 交付

| 文件 | 審查用途 |
| --- | --- |
| [THEOREM_INVENTORY.md](THEOREM_INVENTORY.md) | 完整來源合同、量詞、目前採納、helper／61 LONG labels及證據等級 |
| [DEPENDENCY_DAG.md](DEPENDENCY_DAG.md) | 77-node／183-edge family依賴、細粒度SF更正、最短路線與被禁止的推論 |
| [COMMON_LEMMAS.md](COMMON_LEMMAS.md) | 12局部interface＋GA；每個焦點端點的原圖應用映射 |
| [COMPRESSION_PROPOSAL.md](COMPRESSION_PROPOSAL.md) | 9個完整replacement、可執行memory-only preview、實際／草案／搬移分開 |
| [SCOPE_AND_RISK.md](SCOPE_AND_RISK.md) | 可安全精簡／需要新證明／不可合併／仍OPEN及來源精度風險 |
| [REPORT.md](REPORT.md) | 交付結論、比較、查證與修改界線 |

## 核實的現況與計數

BR-SD-1a／1c／1e／1g均已正式採納；原audit的candidate/pending措辭留作歷史。LONG-S後續限定採納已完成，不以較早JOINT calibration的OPEN描述代替現況。來源：[N45 canonical](../../docs/c5_excess_two_nonadjacent_unit_core45.md) §2.9–2.11及其具名adoption history／review。

本inventory有13個焦點端點（U-LP/SS2、LOW/HIGH5、LONG2、BR4）、4個前置排除、3個SD二連通適用性subset，合20筆來源排除／適用性記錄；另列4個composition。它們不是20個互斥來源families或20項新closure。canonical33行是bundles；LONG-S61原labels也不是61定理。

全部焦點命題保完整量詞／source contract；共同helper只列已有證明實際使用的充分接口。沒有把finite calibration、zero triggers、seal/custody變成任意大小paper或Lean。

## 四類交付結論

| 類別 | 結果 |
| --- | --- |
| **可安全精簡** | 完整assignment join、原spoke filter、connected list slack、incident-edge release／own-β cover、sole-C BASE分流、同一block incidence與actual-support色雙射可共用。BR共用LD/GA，1a/1e共用DP。1c全合法接點直接TERM；HIGH1主排除不先走supporting MAP |
| **需要新證明** | 一般可恢復Δ r-fibre存在性、多接點／跨接口W、一般多旁支或其他Gallai接線的source分類、失pair後TERM/PB、撤U的all-long／一般minimality繼承。1a/1e private-D局部證明未用pair，較弱來源登記需另scope/adoption review，不能擅改合同 |
| **不可合併** | 13個端點的不同原合同、U/S省略、LOW incidence、HIGH contact分拆、LONG owners、BR零／一／兩W、不同原β／來源／G-X minor、union非空與每個fixed pin非空、X接受與原G恢復 |
| **仍OPEN** | 完整N45-S-NOU-LS-PAIR、未覆蓋splits／multi-W／其他骨架、R31、其他45/54／原55／無45/54來源、一般N45/N2/E、ε≥3、出口、主命題及source realization／新Lean。完整K_LONG下Δ≠∅已證，OPEN的是一般restorable fibre非空 |

SAFE是指數學與引用組織可供採用；本輪不執行canonical重構。新的generic/source theorem及新scope採納均另待授權。

## 量化結果與可實現的壓縮

保守preview保持全部原99個不同Markdown link targets，以9段精確引用／分類精簡，把canonical由800行／71,077 bytes變為**763行／69,804 bytes**：行數減37（4.6%）、bytes減1,273（1.8%）。全部20排除／適用性與4composition、原33行索引、OPEN與更正界線保留。前後逐字重複paragraph excess均0，這是semantic重疊／證明路線精簡；不是找到可批量delete的原文duplicates。

77-node family依賴ledger保183條最短路線依賴；較長主文另顯示的3條alternative route引用移成旁註，呈現edges為186→183。這不是解除3個原來源前提，也不宣稱外部GA／BASE或SF-QX歷史信任減少。

本輪**既有文件實際減少0、搬移0、helper新採納0、Lean新增0、完整OPEN新增關閉0**。四份BR frozen PROOF共693行保持原bytes；LONG canonical段74行／6,005 bytes未做preview替換。六份提案是純新增，增加repo文件量；若未來新建production共同lemma檔，必把其全文與應用映射成本扣回，不能拿canonical節省當總體淨縮短。完整重建方法見COMPRESSION_PROPOSAL。

## 獨立審查及修正

三份獨立只讀分析覆蓋BR、U/LOW/HIGH、LONG，並交叉檢查整合稿。已納入的精度修正包括：

- generic ignored-coordinate因子是 `∏(Col−γ(A(z)))`；只有真正無附件孤點是Col。HIGH frozen自由I合同不因generic Z修正而放寬。
- incidence lemma使用有限connected圖及實際maximal blocks，避免慣用block-graph一詞排掉odd cycles。
- actual components寫H_X−s，保完整X仍含框B；不混root-pair union與每個pin非空。
- T1／q0有直接N-diagonal依賴；q2新seed／target存在性構造不直接使用N-diagonal，但保SFβ-role與上游信任。
- HIGH2禁色角色由同βfull join／witness／release／local diagonal取得；slit/crosscut另外屬BASE pair-bridge/source mapping，未混成角色前提。
- 九段preview保1c三odd-block bullet完整與全部正式採納入口；不留下懸空的「只替換合同4」形狀。

這是證明組織的獨立交叉核查，不是再次完整驗收所有歷史audit或新theorem adoption。

## 驗證、來源與保留界線

已完成memory-only重建與sha assert、9個不重疊spans核對、99個原link目標保留、Markdown表格欄數與渲染連結檢查、family DAG逐edge expansion與Kahn無環檢查。artifact中的replacement code以canonical的docs目錄解析相對source links；本目錄正文的41個本機連結另按artifact位置核對。提交前另通過 `python3 tools/docgraph --include 'docs/**/*.md' check`：62 documents／213 relations／5 families，0 errors／0 notes。

分析階段開始／完成的16,267個既有tracked可讀檔案內容SHA256逐一相同，當時HEAD未變；只新增本目錄的六份文件。後續依使用者「整理後 commit」授權，僅本地提交這六份提案；不push／PR，不改STATUS、HANDOFF、canonical、原audits、seal、certificate或history。

讀取formal status時以目前canonical及後續review/history為準。原實驗/工具/封存通過紀錄是引用既有證據；本輪未重跑歷史checkers／seal adapters，未補缺BASE blob、未跑dependent finite-terminal replay、未測target來源或新增source realization，也未跑Lean。LONG-S q0保SF-QX／SF-T2-EXTEND／E2 paper及historical finite-terminal；T1／q2新存在性另由各自已採paper承擔；D recurrence沒有指向一般非空性。

直接外部來源已核讀 [Dvořák作者Gallai講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 与 [Cranston–Rabern正式期刊PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/)；精確使用與frozen版/hash由原SOURCE及SD-A查證紀錄承擔，不把講義稱期刊或把外部結果稱Lean。CR只供SD-A/APP，不是BR四支的證明依賴。

既有documentation與ordinary file search足以解釋各跨檔依賴；沒有使用Graphify、沒有擴枚舉或重開已排分支。若要實作A/B，後續授權應分別指定文件重構範圍與任何新lemma/source-scope採納流程。

## 讀取基準與交付大小

canonical UTF-8 SHA256：`ec80d3f0b053d6c7776b9b7fc0fdfa8432e0e4aef69feb052d3b69e53aa76be8`。
下列只計本輪六份交付，全部是新增提案，並非「壓縮後production corpus」。

| 新文件 | 行數 | UTF-8 bytes |
| --- | ---: | ---: |
| THEOREM_INVENTORY.md | 435 | 93845 |
| DEPENDENCY_DAG.md | 182 | 13722 |
| COMMON_LEMMAS.md | 171 | 21274 |
| COMPRESSION_PROPOSAL.md | 263 | 21100 |
| SCOPE_AND_RISK.md | 53 | 5538 |
| REPORT.md | 84 | 8106 |

六份新增合計：1188行／163585 bytes。既有production原文減少仍0。
