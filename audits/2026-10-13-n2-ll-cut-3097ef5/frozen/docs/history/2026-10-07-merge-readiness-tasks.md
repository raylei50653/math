# 2026-10-07：integrate-kprime-e3 合併任務與驗收台帳

使用者負責發布任務並回傳結果，本對話負責範圍、依賴、驗收與缺口管理。
本表以 **部分研究成果分支合併至 main** 為目標，並非宣告猜想 E 或一般出口完成。
研究停止點仍由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口) 維護。
以下是派工及驗收要求；未完成項不表示已經執行，也不表示 GitHub 設有相同保護規則。

## 接手基準與本次確認

| 項目 | 2026-10-07 接手狀態 |
| --- | --- |
| 本地整合 HEAD | `a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42` |
| 同名遠端分支 | `1d026ee949d07a5b20bd60ec2f1e6d4329341cdf`；本地多12個提交 |
| 遠端 main | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090` |
| 未提交成果 | C44″覆核修訂、唯一 mixed 指定稽核、U1 no-mixed44 checker／證書／報告／索引及兩份歷史紀錄 |
| PR／保護規則 | 查不到此 head branch 的 PR；main 未受保護，required checks 為空 |
| 最新遠端 Lean CI | 舊 HEAD `1d026ee` 的 run `37280911752` 成功；不能驗收本地新成果 |
| 文件檢查 | 本次實跑 PASS：571份 Markdown、6693本地連結及 anchors／index／HANDOFF |
| 大型產物 | 本次 `python3 tools/artifacts.py status` exit0，`ok=155` |
| DocGraph | 正式 docs 範圍 PASS；預設命令 exit1，scratch 交付副本造成62個 duplicate-id |
| 目前 tracked diff | 本次 `git diff --check` exit0；未代替新增檔或整分支差異檢查 |
| U1 普通重播 | 本次 `--check` exit0：344核心、3498接回、34980逐列查詢、target hits=0 |

以上檢查針對接手工作樹，尚不是凍結候選提交的驗收。即時 SHA、CI 及 PR 狀態須重新查詢。
本次未重跑 seed17、mixed verifier、C44／C44′／D9、封存還原或 Lean build。

## 發布順序與狀態

| 任務 | 依賴 | 工作 | 初始狀態 |
| --- | --- | --- | --- |
| M1 | 無 | 整理完整交付包，凍結候選提交 | 待發布 |
| M2 | M1 | U1 新排除的獨立紙面與有限證書稽核 | 等待候選 SHA |
| M3 | M1 | 全新 checkout 的還原、重播及顯式 LC 驗證 | 等待候選 SHA |
| M4 | M2、M3 | 整合 findings、最終提交／PR／遠端 CI 核對 | 等待驗收 |

先發布 M1；回傳候選 SHA 後，M2／M3可在各自獨立 checkout 同時進行。
禁止共寫同一 `.olean`；M2／M3不修改候選來源或原證書。
本對話收到每次回報後，以「待發布／執行中／待補件／已驗收」管理。
發現問題時開具名修正項，不自行把未觸發控制或失敗改成 PASS。

## M1：交付包整理與候選凍結

**可直接發布的任務：** 在 `integrate-kprime-e3` 整理現有成果，不開新證明輪。
先讀 HANDOFF／STATUS／DOCUMENTATION 和目前 Git 狀態，保留所有既有變更。
只納入下列連通交付包，以明確路徑 staging；建立本地候選提交，回傳 SHA，停止於本地交付。

- 八份既有 tracked 修訂：README、STATUS、Kempe導覽、C44″報告及四份 mixed 報告。
- `scripts/c5_excess_two_no_mixed_core44.py`、對應 artifact 與專題報告。
- `audits/2026-10-07-c44pp-mixed-audit/` 的 verifier、REPORT、validation。
- 兩份 `2026-10-07` 整合／U1歷史紀錄，以及本任務台帳／STATUS索引。

確認新增 artifact 的實際大小與大型產物政策；目前 U1證書992965 bytes，低於1000000門檻。
不得廣泛 `git add .`；不得納入 `scratch/task-c44-delivery` 的 clone、bundle、交付暫存。
scratch 留存不妨礙獨立 checkout 驗收，毋須刪除原交付資料。
HANDOFF保持薄入口；沒有研究線變更就不增加摘要。不得改寫歷史hash或生成器產物消除失敗。

**回傳／驗收：** 候選完整 SHA、base SHA、納入檔案清單、來源與產物 SHA256／大小、
候選相對 main 的 diffstat、未納入資料清單、實際檢查及未跑項。
文件、staged diff及新增檔 whitespace／syntax檢查通過；其他既有變更不得遺失。

## M2：U1 的独立稽核

**可直接發布的任務：** 對 M1候選 SHA 的
[U1報告](../c5_excess_two_no_mixed_core44.md) 作獨立稽核，不推進U2–U4，
不修原報告／checker／證書。新輸出放獨立 audit 目錄；不import原checker決策邏輯。

紙面核對須逐項指出來源前提及依賴：原zw保留、piece全取／全不取、省略身份完備性；
941三-spoke側的收窄更正；spoke＋unit-U的D-forcer／triangle palette矛盾；
344域化約是否適用no-mixed、singleton bridge markers和完整十列root-pair relation；
零gap／正奇偶run、leaf及triangle是否保持同源joint；同一整圖D₅／S₄搬運及spoke字面接回。
分清被省略U的任意大小與核心的有限正常形，不把拓撲收縮當染色替換。

有限部分以自己的回溯／證書驗證重算344核心及3498接回的完整Σ；
逐列核對完整root pairs、全圖witnesses及空fibres，核對兩目標整圖D₅軌道無交集。
核對64雙triangle子型的1024接回及Σ直方圖，但不得只驗該子型。
沿用既有mixed指定稽核可以明列，不必重新證明全部上游分類；
上游有限拓撲／NetworkX信任界線須照實保留。

**回傳／驗收：** REPORT、独立checker、結果、命令／exit／logs／hash、
候選SHA與輸入SHA256、輸入零byte漂移核對；逐項判定成立／缺口／反例。
實際控制分成 `triggered and holds`、`not triggered`、`counterexample`。
任意大小化約和有限重算各有獨立結論；若有finding，列具名重現與所需修正，停止擴張。

## M3：候選的還原與驗證

**可直接發布的任務：** 在沒有scratch交付clone的全新獨立 checkout 檢出M1候選SHA。
使用已鎖定toolchain及原報告指定Python環境；不得lake update、重生成或覆寫歷史產物。
依 [封存說明](../../audits/README.md) exclusive還原並核對原bytes，所有新logs寫fresh目錄。

先執行以下還原／一般檢查：

```sh
python3 tools/audit_archive.py restore --artifacts
python3 tools/audit_archive.py verify --artifacts
python3 tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新增／尚未發布證據的重播要求：

- U1普通與seed17 `--check`，完整344／3498／34980域。
- mixed指定 `verify.py` 使用新的 `--output` 路徑，核對原validation的輸入hash及數量。
- D9三個 `audit_e*_controls.py --check`，普通與seed17；記錄三列來源前提的零觸發界線。
- C44 input audit、small／full `--check`及algorithm audit；full另跑seed17，依C44報告命令。
- C44′ screen、two_private、independent各普通／seed17 `--check`，依C44′報告命令。
- LC exporter `--check`；顯式執行下面build與公理稽核，不以預設CI替代LC。

```sh
lake build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit
lake env lean -j 1 Math/ExcessTwoCertificatesAudit.lean
```

主Lean及LC共用同一checkout時依序執行，不並行寫cache。
558項公理核對無sorryAx，179 positive無native；rejected／valid及S₄ cover的native信任明列。
本批維持LC顯式target，不要求接入Math.lean／CI，也不宣稱遠端CI涵蓋LC。
ES／ER及前序E3–E6等已驗證輸入如來源hash未變，可沿用
[分支review紀錄](2026-10-05-integrate-branch-review.md)；列出實際依賴hash及未重跑項。
若輸入有變，針對受影響項重播；不無條件重開k搜尋。

歷史E4／E5／E4C byte FAIL仍保持FAIL。
若現版guide增加新hash漂移，用fresh輸出只比對具名差異路徑，不能整批忽略provenance。
整分支whitespace另查與新更動分開：既有vendor／原logs診斷可列精確例外；
來源bytes保持，不把新診斷混入舊86項紀錄。

**回傳／驗收：** 候選SHA、完整命令／exit／耗時／logs及SHA256、還原與輸入inventory、
數學payload差異、provenance差異、whitespace例外和未跑項分列。
全新checkout的預設DocGraph須通過；正式docs局部PASS不代替此項。
新增來源／證書不得有未解差異；歷史例外須可重現且只限明列來源。

## M4：最終整合與遠端驗收

**可直接發布的任務：** 收到M2／M3結果後整理findings及fresh驗證包，
將通過的audit納入連通交付；有缺口先修正並重驗受影響項。
凍結最終提交SHA，回傳候選到最終的變更表及證據沿用理由。
任何來源／證書／前提變動均重跑對應檢查；僅新增紀錄也須重驗文件／DocGraph／新增diff。

本地收尾後由使用者發布同名分支及PR，base為main。
PR描述只宣稱限定前提下的部分成果，明列歷史byte FAIL、上游信任和LC未入預設CI。
文件workflow目前僅workflow_dispatch；push不會自動執行文件workflow。
可回傳相同最終SHA的本地文件證據，或手動觸發並回傳該SHA的文件run。

**回傳／驗收：** PR URL、base／head完整SHA、local／tracking／remote分支SHA、
同一最終SHA的Lean CI成功run、文件證據、local LC／axioms證據及fresh驗證bundle。
檢查PR仍OPEN、無conflict，main沒有未審查的新差異；main若前進，重判差異與驗證。
空checks或舊SHA成功不能通過遠端驗收。
本地暫存資料留存須列明；最終乾淨驗收以獨立checkout及無遺漏交付為準。
監督端收到完整資料才判「可合併」；本表不執行merge或auto-merge。

## 不列為本次合併阻斷的研究殘留

U2相鄰m=2、U3非相鄰N1 incidence11／12／21、U4非相鄰N2五族，
no-mixed其他core、單-root例外、(5,4)/(4,5)/(5,5)、E5要求的新證明、
三列推廣、ε≥3、猜想E任意大小、一般出口及K∞=K≤5仍保留。
只要合併的結論及PR如實限定範圍，這些不要求在本批全部解決。
若稽核發現它們其實是本批已宣稱結論的必要缺失前提，轉為具名阻斷finding。

## 統一回報格式

```text
任務：M1／M2／M3／M4
狀態：完成／待補件／發現阻斷
base SHA／受驗候選 SHA／交付 SHA：
新增／修改檔案與來源 inventory：
結論、精確前提及未涵蓋範圍：
實跑命令、exit code、logs／hash與證據路徑：
未跑項及沿用理由：
findings／byte漂移／provenance／控制未觸發：
PR URL／CI run與head SHA（僅M4）：
```

本次只建立任務台帳及STATUS歷史入口，未commit／push／建立PR／合併。
