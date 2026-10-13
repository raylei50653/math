# N2 原55：殘餘統一、unary 採納與 long 同步整理發布

2026-10-11；整理開始時 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
使用者授權「整理後 commit + push」。本輪整理四輪相連成果、原證據、直接現況
文件及重播依賴；沒有新增研究命題、來源搜尋或 Lean theorem。
原報告保留生成基準及当輪「未提交」語境；發布以包含本文的 Git commit 定位。

首次 staged whitespace check 指出一份故意毀損負控制的末尾空白；這正是原 byte
mismatch 的方式。原檔及失敗證據不改，以 `.gitattributes` 僅對該具名 fixture
豁免 `blank-at-eol`／`blank-at-eof`，其他來源及文件仍照常檢查。

## 1. 成果與精確停止點

全部來源推論沿用完整原 N2-55 契約：同一 induced-C₅ disk、有序 B、完整
Σ933／941 或整圖共同 D₅ 像、T4 全收、非框邊 Σ-critical、ε=2、有效 H
連通且 full B-touch、非相鄰原完整 degree5 roots、其餘有效內點原完整 degree4、
恰兩份原 mixed 及 one-sided pieces。所有 ordered／shared contacts、ownership、
actual attachments、rotation、bridges、字面色框、完整 relations／空 fibres／full lifts
均保留，不把不同列的局部存在性拼成來源。

| 權威報告 | 本次發布範圍 |
| --- | --- |
| [殘餘統一](../c5_excess_two_n2_residual_unification.md) | 原55逐欄容量為1、singleton mixed迫u=t=0、兩unary子族排除；精確大小式 `|H|=35−6u−3t−Δ`，有限下界10不直接矛盾 |
| [unary 三列候選](../c5_excess_two_n2_unary_three_row_escape.md) | 原接線2／3的任意大小 block-tree case split、字面 palette signatures及局部完整 fibres；保留候選輪語境 |
| [獨立 diagonal 採納](../c5_excess_two_n2_diagonal_three_row.md) | unary出口及同列兩short完整lifts排(0,1)，第三relation族原55全排，九格六格增至七格；shared contact及k≤3 long限定縮減 |
| [long 同步與 tree](../c5_excess_two_n2_long_synchrony.md) | 兩long都k≤3全排；無U的全葉接點tree long任意k排除；含U低接點Eq／Diff異類同列接回，同類縮七個必要字面弧模板 |

證據是任意大小紙面證明、既有外部 Gallai／degree-list 輸入及另人獨立審查。
有限 Python 控制只核具名原圖、完整 tuple equality、minor bags及字面算術。
全部完整 target sources 仍 `not triggered`；新紙面成果未 Lean 化。

**Remaining OPEN：** 九格仍七格；(2,0)至少一long k≥4；(1,0)無shared的
k≥4 long含cycle或原cutpoint接root；(1,1)高接點或低接點七個同類弧模板。
一般原55／N2／E-ARC2、N1／相鄰／單-root例外、一般出口及 K∞=K≤5 都未完成。
大小與 Δ 门檻不改，未搜尋10–35點；當前窄入口由
[Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 2. 相連證據與驗證

四個完整 audit 目錄共同發布，保留原 BASE、凍結 snapshots、checkers、完整
observations、紙面審查、初版／失敗 receipts、故意毀損負控制、外部原 PDF／文字
及實際命令 logs；沒有刪掉失敗或獨立換色／縮圖來改證據。

- [residual-unification](../../audits/2026-10-11-n2-residual-unification/verification.json)：共同容量、鬆弛算術及原 controls。
- [unary-three-row-escape](../../audits/2026-10-11-n2-unary-three-row-escape/verification.json)：97原U、15,520完整ambient cells及任意大小候選的當輪核對。
- [unary-adoption-long-joint](../../audits/2026-10-11-n2-unary-adoption-long-joint/REPORT.md)：另人紙面採納、37原long及63原整圖完整joins。
- [long-mask-sync](../../audits/2026-10-11-n2-long-mask-sync/REPORT.md)：179原pieces的28,640 cells（3,372空）、63原圖10,080完整joint cells、四形mask、800固定附件控制、45完整fibres exemplars、原K₅bags及四接點path三列全拒局部反控制。

本次出版重播的精確命令、exit codes、stdout／stderr、產物bytes／SHA及既有
Lean build 見 [publication receipt](../../audits/2026-10-11-n2-long-mask-sync/publication/verification.json)。
只用 `--check`，保留所有原 artifact bytes。未重跑上游全部44／N45／SD-A、
ES／ER生成、來源rotation或全工作樹DocGraph；後者的歷史duplicate-ID界線保留。
正式docs檢查與全工作樹檢查分開；build只核既有Lean，不形式化新paper。

bounds checker 另讀既有大型 `NA_k9_validate.json`（1,152,495 bytes），原檔由
tracked MANIFEST／producer 管理而未入 Git。本次保存[原 bytes 快照與來源](../../audits/2026-10-11-n2-long-mask-sync/publication/prerequisites.json)，
SHA `0b08675df72ecd21415d8fb54df567fc2daa7b802df9bc22c97f4cd6f89dc9bb`
對回原 MANIFEST，不重建有限搜尋、不改原 artifact／MANIFEST／ignore 規則。
獨立還原僅在暫存 tree 內由這份提交快照補到原 canonical 路徑後 read-only 重播。

本輪亦核對提交tree的相連檔案，與工作區逐byte相同；從工作樹外獨立還原提交tree
重播同一組限定checkers的normal模式及正式docs DocGraph，以確認沒有遺漏local-only相連依賴。
未從還原tree重新生成原來源或大枚舉。結果及範圍同樣記錄於publication receipt。

## 3. 文件核對與發布界線

Closure scope：完整N2契約內的明列子族及限定long形狀，不提升父命題或九格數。
Updated：四份權威報告、四個audit、N45直接入口／停止點、size-bound後續入口、
Kempe導覽、STATUS及已有synthesis摘要；發布紀錄與dated links說明前輪未提交语境。
Reviewed-unchanged：README及HANDOFF仍正確路由原研究線；一般Phase B／B-C2、
舊凍結evidence及其他研究線沒有語義變動。Propagation stop：實際直接consumers，
父N2／E-ARC2仍OPEN，不重寫歷史或新增總帳。

只暫存相連證據／文件，commit後push main。實際完成以
`HEAD=origin/main=remote main`及工作樹乾淨的readback為準；SHA由包含本文的commit定位。
