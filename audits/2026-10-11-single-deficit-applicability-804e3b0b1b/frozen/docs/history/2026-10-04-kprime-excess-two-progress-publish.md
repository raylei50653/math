# 2026-10-04：K′、E3–E6、ES／ER 與 LC 進展整理及分支發布

使用者要求「整理目前進展 push」。接手分支為 `integrate-kprime-e3`，
基準 `433dea3`；工作樹乾淨，已有31個尚未推送的整合／任務提交。
遠端 main 基準為 `2ddc6b4`。本次整理既有成果與驗證紀錄，發布至同名分支；
不啟動 D₉／C44、不新增數學排除、不將此分支合併至 main。
完整 SHA、遠端發布及工作樹狀態以即時 Git 為準。

## 成果與停止點

| 項目 | 已完成範圍 | 保留界線 |
| --- | --- | --- |
| [K′](../c5_kempe_diagonal_transport.md) | 同一 G−p 的拒絕見證下，紙面引理1–6及Jordan側別迫兩條對角鏈皆斷；L2仍有933：192、941：384一致指派，同ψ多鏈交換無新排除 | 局部資料與可實現1012／935控制同型；K′未決，K型局部工作停止 |
| [E3](../../artifacts/c5_excess_two_e3/REPORT.md)／[D₈](../../audits/2026-10-04-task-d8/REPORT.md) | ε=2反例約化為拒絕q₀、q₁、q₃，triple-critical及唯一degree-6排除 | 必須引用DG6-1的100份相對spoke位置補表；雙degree-5保留；A前序依賴更正已記於E3 §10 |
| [E4](../../artifacts/c5_excess_two_e4/REPORT.md)／[E5](../../artifacts/c5_excess_two_e5/REPORT.md)／[E6](../../artifacts/c5_excess_two_e6/REPORT.md) | 非相鄰／相鄰mixed數m≤2；N3及J6的m≥3關閉；941／933／940／932四分支的G2–G4與no-mixed收窄 | N1／N2、G1–G4、J6的m≤2、no-mixed、J4及較少spokes／原(5,5)core未全排 |
| [E4C](../../artifacts/c5_excess_two_e4c/REPORT.md) | 54個NA critical orbits×60項不用三列的步驟；42項有控制、18項未觸發前提，0反例 | singleton盾弧、root刪除例外、(4,4)core、根間bridge整側及單重色core仍缺實際控制 |
| [ES](../c5_excess_two_finite_search.md)／[ER](../c5_excess_two_independent_search.md) | 三種root型k≤9的q／critical orbit集合、計數及Q分布逐層一致；179個critical orbits（NA54／AD9／D6 116），無\|Q\|+c(Q)>4 | 有限雙實作完整性證據；ER依賴plantri；不提升為任意大小定理；k≥10未搜尋 |
| [LC](../c5_excess_two_lean_certificates.md) | 179／179個Lean soundness證書，558項axioms audit無sorryAx | 拒絕列用native_decide，raw Σ另繼承既有S₄ cover native信任；只證所列圖為真及組合嵌入，不證枚舉完整性、軌道互異或拓撲disk定理；未接入Math.lean／CI |

共同 ε≥2維持；ε≥3、猜想E的任意大小版、一般單側／共同出口與K∞=K≤5未證。
目前未派提議為D₉紙面稽核及C44的minimal-core統計／條件化證明，
精確停止點由[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。
已在main的C-W／D₆共鄰P₃排除及cw-v1 ledger=0沿用既有結果，
本次只校正README／synthesis的摘要，沒有重驗或擴張其結論。

## 文件與原產物保存

README改為目前入口與短摘要；Kempe導覽把已完成的歷史派工計畫
整理為返回成果表與D₉／C44未派提議，原完整guide仍在Git歷史。
Lean導覽補LC target、native信任及未接入CI的範圍；synthesis頁首補目前整合快照；
STATUS新增本紀錄索引。HANDOFF研究線與tag未變，保持薄索引。

接手的artifact status為 `missing=1 ok=154`，唯一缺檔是ignored
`artifacts/c5_excess_two_e3/degree6.json`。從E3原worktree以exclusive-create
還原2,027,696 bytes；SHA256
`826818db6861ff45696b7a8d69708eb64f0577de54f92ffe9f3c44a30096bd8d`
與既有MANIFEST完全相同。沒有修改MANIFEST或重新登錄此檔。
還原後artifact status為 `ok=155`，degree6普通／seed17重播均通過。

三份歷史byte-check保留失敗：

- E4 reductions：E3 REPORT的hash及bytes（30,573→32,469）因後續D₈／E5補證漂移。
- E5 controls：同一E3 REPORT hash漂移。
- E4C：summary所記Kempe導覽hash因後續整合及本次整理漂移，54份控制JSON均逐byte通過。

上述三項普通／seed17的byte verdict均為FAIL；不重寫舊certificate使它們變PASS。
另在新輸出目錄取得in-memory完整重算結果，僅排除各自明列的provenance欄位後，
完整JSON均相同，沒有數學payload差異。初始degree6缺檔失敗、中途guide版本
及最終漂移比較分開保存於本次驗證包；語意相等不代替historical byte PASS。
最後補明K′的拒絕見證前提後，E4C另跑普通check及語意比較；seed17沿用
本輪前一導覽字句版本，該hash與最終hash分別記錄，不混稱同一版本重播。
整分支相對main的 `git diff --check main...HEAD` 另有86項既有whitespace
診斷，限ER的plantri原始vendor與原執行logs，沒有變更其bytes或source hash。
本次新log若帶原始尾空白，以deterministic gzip保存並核對解壓bytes；
file inventory保留原hash與還原路徑，不因排版檢查改寫原輸出。

## 本次實際驗證與沿用範圍

[驗證彙整](../../artifacts/c5_kprime_excess_two_progress_publish/validation.json)
保存命令、exit、耗時、fresh logs與provenance差異；原任務的validation不改寫。

| 本次檢查 | 實際結果 |
| --- | --- |
| K′、E3四項、E4兩項、E5三項、E6三項、E4C、D₈補表；普通／seed17 | 15個checker的30個最新verdict：24個逐bytePASS，6個上述文件provenance FAIL；三份完整semantic comparison相等 |
| ES acceptance driver `--check` | exit0；4,710個有標號q圖與72,910次刪邊比較 |
| ER全量 `--check --jobs 8` | exit0；k3..9三型全量逐byte，248.247秒 |
| LC exporter普通／seed17 `--check` | exit0；179個來源重新稽核，三份輸出逐byte相同 |
| 主checkout `lake build` | exit0；8831 jobs，既有linter warnings |
| LC顯式build／axioms audit | exit0；8837 jobs增量build，558項公理稽核無sorryAx |
| pinned artifact status | exit0，ok=155 |
| 文件／DocGraph | exit0；562份Markdown／6510個本地連結；62份DocGraph文件／213關係／5families |
| 本次工作樹diff | exit0；舊整分支的86項vendor／log whitespace另保留 |

LC build及axioms audit使用已有獨立cache的原LC worktree；先以Git diff核對
Math sources、exporter、LC產物、toolchain及lake設定與本分支完全相同，
沒有共寫同一 `.olean`。本次是增量建置，沒有從零重做179張native計算。

ES的完整16分鐘主搜尋普通／seed17重播沿用既有紀錄，本次**未重跑**；
已核對ES程式、報告及產物自 `task-es-search @ 1c8642b` 以來未變。
acceptance driver不能代替主搜尋全量重播；ER的本次完整重播另行列出。
未重跑E1／E2／D₇、C-W／D₆、舊A／B／C、R系列、早期全來源枚舉
或其他Lean模組的獨立axioms audit；這些沿用各原報告。

發布前文件、DocGraph、pinned artifact status、本次工作樹及staged diff檢查
均exit0；整分支86項歷史whitespace及6個文件provenance FAIL另列並保留。
本次停止於整理、commit、同名分支push及local／tracking／remote SHA與乾淨工作樹核對。
