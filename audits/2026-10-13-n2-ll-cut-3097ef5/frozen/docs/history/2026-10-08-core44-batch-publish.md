# 2026-10-08：U2–U4與M4／M5證據整批整理發布

基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
使用者在U4推進完成後明確要求「整理後整批 commit + push」。本批將接手前已有的
U2／U3與四包交付稽核，連同U4完整來源、證書及文件整合為一份提交，推送至`origin/main`。
各研究輪的「未提交」與M4／M5的截點狀態保留當時語境；最終SHA與遠端狀態以Git為準。

## 提交範圍與停止點

| 成果 | 來源、完整證書及當輪紀錄 |
| --- | --- |
| U2 相鄰兩mixed44 | [專題報告](../c5_excess_two_adjacent_two_mixed_core44.md)、[研究紀錄](2026-10-08-u2-two-mixed-core44.md) |
| U3 非相鄰sole mixed11 | [專題報告](../c5_excess_two_nonadjacent_one_mixed_core44.md)、[研究紀錄](2026-10-08-u3-one-mixed-core44.md) |
| U3 sole mixed12／21 | [專題報告](../c5_excess_two_nonadjacent_mixed12_core44.md)、[研究紀錄](2026-10-08-u3-mixed12-core44.md) |
| U4 非相鄰兩mixed | [專題報告](../c5_excess_two_nonadjacent_two_mixed_core44.md)、[研究紀錄](2026-10-08-u4-two-mixed-core44.md) |
| M4-L監督 | [原報告](../../audits/2026-10-07-m4-supervisor/REPORT.md)，141檔／7,894,140 bytes |
| M4-R交付 | [原報告](../../audits/2026-10-07-m4-remote/REPORT.md)，342檔／8,811,898 bytes |
| M4-R監督 | [原報告](../../audits/2026-10-07-m4-remote-supervisor/REPORT.md)，40檔／99,008 bytes |
| M5合併回讀 | [原報告](../../audits/2026-10-08-m5-merge/REPORT.md)，72檔／92,154 bytes |

連同原來源scripts、各artifact資料夾的小型reports／證書／validation、
[MANIFEST](../../artifacts/MANIFEST.json)、[封存index](../../audits/ARCHIVE.json)、
六個新compressed blobs與相應ignore規則，更新README入口、STATUS、Kempe導覽與
兩份上游artifact reports及U1後續狀態。HANDOFF研究線與tags未變，依文件治理保持原入口。

完整Σ933／941及整圖D₅像、Σ-critical、ε=2、指定有序induced-C₅ disk等明列前提下，
U1–U4與前序相鄰唯一mixed結果完成兩-root(4,4)身份排除。U4保留原O11的盾弧、
ordered contacts、ownership、原附件及完整tuple／含空fibres／witnesses；828必要標記的
8,280目標比較零殘留。共同五個三色列相等只在證明需要的介面成立，
全部十列Σ相等與全部contact joint等價的反例仍保存。

紙面化約、Python必要有限域與Lean狀態分開。本批未新增Lean theorem；
無44 core來源、單-root、45／54／55、E5新證明、三列一般推廣、ε≥3、一般出口及
`K∞=K≤5`仍保留。精確停止點與後續入口由[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 原bytes保存與新checkout

四包M4／M5共595檔、16,897,200 bytes；591項原inventory與四份manifest自身全數核對。
零missing／extras／byte或hash漂移，465份普通文字whitespace零診斷；130份binary
保留原bytes。詳細完整清單見[獨立完整性紀錄](../../audits/2026-10-08-core44-batch-publication/historical-audits-integrity.json)。

五份新增大型證書共39,787,232 bytes，以原SHA256登錄MANIFEST並追加封存blobs；
另收錄D₈兩份既有大型還原副本及M3一份歷史whitespace log的原路徑。
ARCHIVE原2385項與1460個blob records全部不變，新增三個原路徑及六個blobs，
增加2,285,087 compressed bytes。現行ARCHIVE有2388個原路徑、1466個blobs；
`--artifacts`包含160份live大型產物，共核對2548個materialized paths。

既有`scratch/task-c44-delivery/`的489MB local clone、bundle及receipt保留本地，
以精確目錄規則忽略。它們是原交付暫存，不是本批Git來源；清單與hash亦見上述完整性紀錄。
原全worktree的DocGraph仍有62個scratch duplicate IDs；本批不刪除scratch來改寫此FAIL。
提交候選以Git index匯出到新的空目錄，再從候選自己的封存還原所有原路徑及160份live產物。

```sh
python3 tools/audit_archive.py restore --artifacts
python3 tools/audit_archive.py verify --artifacts
UV_CACHE_DIR=/tmp/u3-single-uv-cache uv run --offline --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --cached --check
```

新checkout實際驗證及完整argv／stdout／stderr／exit codes見
[publication validation](../../audits/2026-10-08-core44-batch-publication/publication-validation.json)。
候選fresh還原與verify全部通過2548 paths／1466 blobs，MANIFEST `ok=160`；
文件檢查通過582份Markdown／6864本地連結，預設DocGraph通過62 documents／
213 relations／5 families；staged whitespace通過。
這份新驗證不替換M4的歷史文件CI FAIL、五份strict FAIL、M1缺失或M5當輪Lean pending。
本批未dispatch文件workflow或驗收新push的遠端CI。

## 實際重播與未重跑範圍

U2／U3七支checkers各default及seed17，共14次通過，七份輸出及66份輸入／scripts
前後hash零漂移；命令與完整stdout見[replay](../../audits/2026-10-08-core44-batch-publication/u2-u3-replay.json)。
U4 primary／auditor各以default、seed17及`python3 -S`重播，共6次通過；
`lake build`通過8,831 jobs，僅既有lint。
結果與輸入前後hash見[U4與build紀錄](../../audits/2026-10-08-core44-batch-publication/u4-build-validation.json)。
U4研究輪的空輸出fresh生成逐byte一致證據沿用原
[fresh rebuild](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/fresh_rebuild.json)，
發布輪只重播check，不再次生成同一證書。

未重跑U1及其上游全部degree-4／triangle／topology枚舉、ES／ER有限搜尋、
LC全部native targets／558公理程序，未重演歷史M4／M5外部寫入或merge。
本批只有已授權的commit與push；沒有開PR、另行合併、刪分支或修改原稽核包。
完整提交路徑、bytes與hash見[提交清單](../../audits/2026-10-08-core44-batch-publication/staged-inventory.json)。
