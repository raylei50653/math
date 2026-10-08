# 2026-10-08 U2–U4整批發布驗證

使用者授權：「整理後整批 commit + push」。基準main為
`2971d46d715d213f25f534958bdab499d2573b69`；完整範圍、停止點、還原命令及未重跑項目見
[發布紀錄](../../docs/history/2026-10-08-core44-batch-publish.md)。

本批本地驗證通過：候選fresh還原及verify的2548個檔案／1466個blobs全數吻合，
MANIFEST `ok=160`；文件582份Markdown／6864本地連結、預設DocGraph
62 documents／213 relations／5 families，以及staged whitespace均通過。
原worktree預設DocGraph仍因保留scratch而有62個duplicate IDs、exit1；
這份已知FAIL與候選fresh的PASS分別記錄。

| 證據 | 紀錄 |
| --- | --- |
| 四包M4／M5原bytes完整性 | [historical-audits-integrity.json](historical-audits-integrity.json)，595檔／16,897,200 bytes、零漂移 |
| U2／U3 | [u2-u3-replay.json](u2-u3-replay.json)，14次check PASS、outputs及inputs零漂移 |
| U4／Lean build | [u4-build-validation.json](u4-build-validation.json) |
| 本地與候選fresh還原／文件驗證 | [publication-validation.json](publication-validation.json) |
| 本批提交檔案 | [staged-inventory.json](staged-inventory.json) |

本批按精確路徑提交connected source／scripts／證書／reports／索引／封存；
scratch clone、bundle、receipt依原交付規則保留本地並精確忽略。
提交清單排除本package自己的提交清單、最終publication validation及其stdout／stderr logs，
以避免自指hash；
最終Git tree與commit SHA由Git另行核對。
U4／build紀錄保留當時`/tmp/math-batch-u4-build-validation/`的log路徑；
同名原bytes亦保存於本包`u4-build-logs/`，可按原hash核對。

本次驗證不改寫原strict FAIL、文件CI FAIL、歷史whitespace或M5截點pending；
paper、Python有限必要域、原Lean theorem與新push的遠端CI結論分開。
無新增Lean theorem，ε≥3及一般主命題仍未證。
