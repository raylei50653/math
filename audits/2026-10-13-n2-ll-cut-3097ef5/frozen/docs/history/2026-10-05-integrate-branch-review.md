# 2026-10-05：integrate-kprime-e3 分支 review 與發布

Review 基準為 `main @ 2ddc6b4`，被審提交為 `a484d4c`，共32個提交。
使用者要求「幫我review 後 push」；發布目標為同名分支。
本輪未發現新的數學或證書阻斷問題，修正一項 P3 工作目錄問題。
本 review 不增加任意大小定理，也不代替 D₉ 的完整獨立紙面稽核。

## Finding 與修正

**P3：ER 重播產生未追蹤執行檔。**
[ER 的 plantri 編譯](../../scripts/c5_excess_two_independent_search.py)每次
`--check` 都寫入 `scratch/er/plantri`；接手乾淨工作目錄實際變成
`?? scratch/er/plantri`，可能被後續廣泛 staging 帶入版本庫。
在 `.gitignore` 新增精確的 `/scratch/er/plantri` 規則。
`git check-ignore -v scratch/er/plantri` 已確認命中；vendor source 保持 tracked。

## 審閱範圍與實際驗證

人工重點閱讀 ES／ER 的內部圖生成、附件環序、單調剪枝、canonicalization、
共同框搬運與刪邊判定；LC 的 structure／rotation／colouring、完整刪邊覆蓋及
soundness bridges；K′ 的拒絕見證與 Jordan 側別；E3 的 triple-critical 化約及
DG6-1 補證；E4／E6 的整份 mixed 內外側、hub 前提與殘留介面；
並核對 E5 後更正及 README／導覽的信任界線。全部23份新增 Python source 通過 AST parse。
這不是逐一重新證明所有前序外部定理或全部紙面引理的聲明。

[本輪驗證與完整差異](../../artifacts/c5_integrate_branch_review/validation.json)
保存命令、exit code、原始 log 的 gzip 路徑及 SHA256。

| 檢查 | 本輪結果 |
| --- | --- |
| K′、E3四項、E4兩項、E5三項、E6三項、E4C、D₈補表 | 15個普通 checker：12個逐byte PASS，3個重現歷史文件 provenance FAIL |
| 三份失敗產物在新目錄／記憶體重算 | E4只差E3 REPORT的bytes/hash，E5只差該REPORT的hash，E4C只差Kempe guide hash；其餘完整JSON相同，54份E4C控制逐byte相同 |
| ES acceptance `--check` | exit0；4,710有標號q圖、72,910次刪邊 |
| ER `--check --jobs 8` | exit0；三型k=3–9全量產物逐byte，q／critical集合與計數均一致 |
| LC exporter `--check` | exit0；179份來源與三份輸出逐byte |
| 主checkout顯式LC build | exit0；8837 jobs，730.653秒；179份具名證書於本checkout編譯 |
| 主checkout LC axioms audit | exit0；558項公理稽核無sorryAx，179項positive無native公理 |
| pinned artifact status | exit0，ok=155 |
| 文件、DocGraph、此次diff | 接手文件／DocGraph及修正diff均exit0；新增本紀錄後再重跑，結果見validation的final_checks |
| 整分支相對main的whitespace | exit2；86項既有vendor／原始log診斷，保留bytes |

ER 第一次在 sandbox 因 Python multiprocessing 無法建立本機 socket 而 exit1；
允許該本機程序操作後，原命令全量重播 exit0。這是執行環境限制。
歷史 byte FAIL 保持 FAIL，完整非provenance相等不改寫其 verdict。
Fresh semantic comparison 逐路徑限制差異，沒有整批忽略所有 provenance 欄位。

LC 的拒絕列仍使用 `native_decide`，raw Σ 繼承既有 S₄ cover 的 native 公理；
只保證具名圖的 soundness 與有限組合 embedding，不證搜尋完整性、軌道互異或拓撲 disk 定理。
LC 仍是顯式 target，未接入 `Math.lean`／預設CI；本輪在目前 checkout 重跑該 target。
唯一 degree-6 排除仍限 E3 指定三列並連同 D₈ 補表；一般 ε≥3／猜想E仍未證。

## 沿用證據與停止點

ES 約16分鐘的完整主搜尋及全套seed17重播本輪未重跑；其來源與產物維持被審HEAD，
本輪ER完整重播另提供全部q／critical corpus對照，不能混稱ES主搜尋重播。
E1／E2／D₇、C-W／D₆、舊A／B／C、R系列及其他Lean模組的独立公理稽核沿用原報告。
所有原研究產物、證書、失敗、hash及前序報告保留。

本輪停止於review、精確ignore修正、fresh驗證封存、同名分支commit／push，
以及local／tracking／remote SHA一致與乾淨工作目錄確認。
精確SHA與發布狀態以Git為準；研究停止點仍由[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。
