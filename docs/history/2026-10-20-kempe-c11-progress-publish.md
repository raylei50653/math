# J1 原 W5 整支排除與 Kempe 精確迭代整理發布

2026-10-20。發布前 HEAD 為 `af0df8081e79b51f8b24e17e01b2bd5572e46a0a`，
遠端 main 為 `1148ce026aaf764e6e2766aebc096eebe193ed13`。
使用者明確要求整理目前進展並 `commit + push`；本次包含既有未推送的
`af0df80` 聯合 Kempe 初驗提交，以及三組後續審核與文件整理。
各輪報告「未提交／推送」保留當輪語境，不改寫凍結證據。

## 成果與停止點

| 研究線 | 本次整理的結果 | 保留缺口 |
| --- | --- | --- |
| J1 原 W5 三邊路 | [C11 殘支](../../audits/2026-10-20-r6-941-j1-c11-1148ce0/REPORT.md)的 132 條整數等式在 20,794 個存活交換 columns 完全相消，迫 `16(Z5093+Z5100)=0`，與同一實際完整 fibre 正值矛盾。保留 n 的全部額外附件；合前輪 n=5，完成此具名三邊路整支。 | type III 的 12 色 n–L 路皆至少五邊；一般 type I／III 長路、J1 兩項、J2 六項、H4 與較小 bad 仍 OPEN。 |
| 聯合 Kempe 狀態 | [已提交初驗](../../audits/2026-10-20-joint-kempe-state-1148ce0/REPORT.md)用八點真 disk 反駁六分割摘要的一般逐步充分性。[三台同步](../../audits/2026-10-20-multi-kempe-machines-af0df80/REPORT.md)在固定 cell95 上給單／雙／三台 160／176／192 類，並定位 384 條跨步換見證的假路徑。 | 固定圖分類及兩輪全未來細分不提供一般 disk 深度界；cell95 不觸發完整 r6／941／J1 來源前提。 |
| 精確殘餘迭代 | [傳輸再共同篩選](../../audits/2026-10-20-kempe-residual-iteration-af0df80/REPORT.md)對任意有限歷史保完整共同軌跡；固定 cell95 的閉包 192→288→336，拒絕全部 384 假路徑、接受全部 45,888 真路徑。72 個雙候選皆可試探、篩選後反序還原。 | 一般小狀態表示、候選界、J1 來源排除及計入接回成本的圖大小下降仍 OPEN；phase 合併必保留中途觀測。 |

紙面同源全稱論證、有限完整 fibres／整數證書與 Lean 分開。
本次沒有新 Lean theorem；一般 `K≤22`、固定 r6 的 `k≥25` 不變。
`W110+W101>0`、`omega_e=0`、完整319、一般同候選三拒絕及
`K∞=K≤5` 均未閉合。

## 發布範圍與保存

三組新增 audit 的 1,509 份非快取來源檔案逐 bytes／SHA 保存於
[SOURCE_FILES](../../audits/2026-10-20-kempe-c11-publication-af0df80/SOURCE_FILES.json)，
合計 163,778,814 bytes，含原凍結依賴、完整證書、負控制及失敗探索。
39 份被既有 ignore 規則遮蔽的來源依
[精確清單](../../audits/2026-10-20-kempe-c11-publication-af0df80/required-ignored-inputs.json)
納入；快取不屬於來源清單。七份超過 1 MB 的 JSON 依原政策登記確切大小與 SHA，見
[新增例外](../../audits/2026-10-20-kempe-c11-publication-af0df80/artifact-exceptions-added.json)。
政策門檻與 checker 不變；探索 pickle／npz 不作最終證明依據。

Updated：Kempe／state 導覽及 STATUS 的精確停止點與直接後續索引；
舊 C11 介面段落明列當輪範圍，避免把本次具名子支排除擴大到其他介面。
Reviewed-unchanged：README／HANDOFF 的入口與活躍標記；研究線並未增減。
Propagation stop：L2，兩條父研究線與全域主命題仍 OPEN。
接續入口為 [Kempe 導覽](../c5_kempe_guide.md)及 [state 導覽](../c5_state_guide.md)。

## 本次驗證

三組新增 audit 的正常／`PYTHONHASHSEED=17` 重播通過；
同源、完整 fibres、證據 seal、污染負控制及排他建立控制分別核對。
既有 `af0df80` 的聯合 Kempe 入口亦完成唯讀重播。
逐項命令、退出碼與原始輸出見
[C11 審核](../../audits/2026-10-20-kempe-c11-publication-af0df80/review-c11/summary.json)、
[Kempe 審核](../../audits/2026-10-20-kempe-c11-publication-af0df80/review-kempe/summary.json)及
[項目檢查](../../audits/2026-10-20-kempe-c11-publication-af0df80/review-project/summary.json)。

`lake build` 完成 8832 jobs，只有既有 linter warnings；工具測試 94 項、
DocGraph 測試 18 項通過。最終文件、正式 docs DocGraph、staged artifact policy、
index custody 及空白檢查結果見
[發布檢查](../../audits/2026-10-20-kempe-c11-publication-af0df80/publication-checks.json)。
完整 staged 空白檢查有 29 個警告，限八份原始 stdout、探索日誌及 frozen diff；
保留其原始 bytes／SHA，僅排除這八個精確路徑後，其餘 staged 檔案通過。
全工作樹 DocGraph 仍有 72 個 frozen／scratch／歷史副本的 duplicate-id 診斷；
不宣稱全樹通過，也不刪除證據消除診斷。新紙證與計數引理沒有因此 Lean 化。

最終 commit、push、本地／tracking／遠端 SHA 及工作樹狀態以完成發布時的
即時 Git 核對為準；本紀錄不預先宣稱遠端 CI 成功。
