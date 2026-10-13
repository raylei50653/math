# K≤14、C₈ 分支界與 W5 圈秩四排除

後續發布：使用者其後授權整理並 commit + push；本次保存核對與驗證範圍見
[整合發布紀錄](2026-10-13-k14-rank4-atlas-publish.md)。以下保留原研究輪次語境。

2026-10-13。起點 HEAD `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。
使用者要求嘗試排除 C5 剩餘 OPEN；本輪完成三項精確範圍的進展，沒有
commit／push。接手時既有 README、STATUS、state guide、未追蹤圖譜成果
及 rank4-contractible audit 保留；後者在本輪重新驗證後接入合併結論。

## 1. Closure scope 與來源

| 精確結果 | Canonical Source + Evidence | 未涵蓋範圍 |
|---|---|---|
| 一般disk-C₅的K≤14=K≤5 | [K14入口](../c5_k14_sphere.md)、[隔離完整報告](../../audits/2026-10-13-k14-sphere-acd2b1b/REPORT.md) | K≤15及一般K∞ |
| 原h=3八項契約必k≥16 | [同一入口](../c5_k14_sphere.md)、[原面配對／無葉點證明](../../audits/2026-10-13-k14-sphere-acd2b1b/independent/C8_PROOF.md) | 八項無界來源、h≥4 |
| 任取合法W5私人ρ≥5 | [圈秩四合併入口](../c5_w5_private_rank4.md)、[新essential證據](../../audits/2026-10-13-w5-rank4-essential-acd2b1b/REPORT.md)、[既有contractible證據](../../audits/2026-10-13-w5-rank4-contractible-acd2b1b/REPORT.md) | ρ≥5來源、一般小代表／R³縮減 |

每項沿用全部目錄外來源的全域最小內點／最大邊數契約，不能替換為N2、
edge-critical或固定mask極小來源。E-ARC2的一組組合性收窄只保存為
[未採納筆記](../../audits/2026-10-13-w5-rank4-essential-acd2b1b/review/earc2-observations.md)，
沒有增加其完整OPEN分支排除數。

## 2. 已執行的數學驗證

K14：從凍結plantri原始碼重編譯並執行min5及min4＋output filter兩條完整
生成；73嵌入類相等，全部1,001五度root刪除圖、10,010列、180,228完整
lifts由固定次序DFS與獨立propagated-domain搜尋逐字一致，皆Σ1023。
主／獨立normal及seed17重播通過；八次破損拒絕，C5／W5／原chord三份
小控制再驗真正空fibres。紙面覆核見
[K14_REVIEW](../../audits/2026-10-13-k14-sphere-acd2b1b/independent/K14_REVIEW.md)。

W5 essential：2,872完整必要模板皆Σ1023；主normal、改變搜尋次序的seed17、
獨立原邊／rotation／完整fibres重播及28次破損拒絕通過。三PPP面分类与
參數域由另一reviewer獨立審查，normal／seed17係數計數吻合。
其seal由worker完成；主端未改sealed audit。

W5 contractible：主端本輪實際執行`verify.py`、`controls/check.py --check`及
`independent/check.py`，均通過6,389模板、65,423,360 cells與全體lifts。
也讀取其原獨立紙面／幾何分類審查。主端receipts保存於K14 audit的
`logs/rank4-contractible-verify.log`、`logs/rank4-contractible-primary.log`、
`logs/rank4-contractible-independent.log`，原seal及舊證書未動。
原工作樹證據與HEAD依賴由essential的BASE分開記錄後，正式合併ρ≥5。

前三項是新紙面或紙面接有限完整證書；沒有新增Lean theorem。
未重播Dvořák–Lidický外部計算證書，plantri完備性與實作信任亦明列。
實際933／941最小來源仍`not triggered`；排除依完備來源化約。

## 3. 文件反向核對與傳播停止

Updated：兩份新權威入口、Kempe導覽的對應現況／停止點、STATUS直接索引。
K13、cofacial、degree bound、C8 apex、neartri、W5 rank1–3、three-color
support、marked relation與degree5 link的直接舊報告新增具日期後續入口，
原論證／當輪數字與證書保留。相關舊表格保留歷史強度，新列及停止點給
當前最強界線。

Reviewed-unchanged：HANDOFF研究線及進行中狀態未改；README仍作路由，
跨線synthesis／common-language沒有因此變成一般閉合。既有未追蹤atlas
是其原輪次完整mask分類，不改24 known／2 OPEN類或其中歷史K14停止點；
本輪只更新當前Kempe權威入口，保留並行成果。State guide不需改動。

Remaining OPEN：K≤15、K∞=K≤5、933／941任意大小來源、一般五度縮減、
私人ρ≥5、h≥3的八項C8來源及E-ARC2剩餘身份。
Propagation stop：在直接來源／父導覽更新後停止；新結果没有關閉一般父命題，
沒有重寫跨線研究快照、另開一般枚舉或變更研究線標記。

文件與既有Lean回歸的最終執行結果保存於K14 audit的`VERIFICATION.json`。
既有工作樹DocGraph重複ID若仍存在，獨立報告，不能用正式docs通過替代。
