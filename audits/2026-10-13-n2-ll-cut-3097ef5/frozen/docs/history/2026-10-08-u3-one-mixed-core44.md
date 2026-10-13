# 2026-10-08：U3 非相鄰 sole mixed11 的44身份排除

基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
使用者要求「推進 U3」。從 HANDOFF、STATUS、Git 與 Kempe 導覽的既有窄提議接續；
工作區已有 U2 及 audits／scratch 變更，全部保留。
證明與依賴見 [U3 mixed11 報告](../c5_excess_two_nonadjacent_one_mixed_core44.md)，
目前停止點由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 成果與精確範圍

在完整Σ933／941或整圖D₅像、disk、Σ-critical、ε=2、非相鄰雙degree-5 roots、
sole mixed incidence11 的來源下，不存在保留兩roots的 (4,4) minimal core。
每側unit的spoke／unary省略全部涵蓋。
兩份原unary的容量11給外側apex K₃,₃，容量22違反雙triangle的直接原bridge；
容量12／21由原star face將C全部實際框附件迫成同一非相鄰pair，
指定拒絕列使pair重色，兩份原側及完整C均有slack，可同框拼回。

獨立紙面覆核驗收上述飽和、star face、原C路徑、任意root pins延拓及拒絕pair覆蓋。
明確保留 U_w 額外path tail；不假定capacity-two unary就是K₂，不聲稱H−z連通。
U3 mixed12／21 incidence、U4、單-root例外及45／54／55 core保留。
沒有擴大k搜尋、重新開逐source key或推升猜想E任意大小。

## 新產物與固定控制

- [Checker](../../scripts/c5_excess_two_nonadjacent_one_mixed_core44.py)
- [證書](../../artifacts/c5_excess_two_nonadjacent_one_mixed_core44/observations.json)
- [獨立 auditor](../../scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py) 與 [獨立證書](../../artifacts/c5_excess_two_nonadjacent_one_mixed_core44/independent_audit.json)
- 24張完整degree原圖：C有1–4點，unit unary有singleton／path，capacity-two unary有原triangle及額外tail，含root交換。
- 240份完整十列joins、720份整piece tuples、3,840個root fibres，包含空fibres及shared C contact。
- 每個joint tuple索引三份整piece witness，拼接後驗全部原邊；所有root fibres另由独立全圖回溯核對。
- 72份實際端點重色查詢全接受；10份原apex K₃,₃邊證書、84份slack算術、50份拒絕pair×D₅ mask覆蓋。
- 控制Σ為759×16及1023×8，目標命中0；這些圖沒有宣稱disk、Σ-critical或來源實現。

```sh
python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44.py --check
python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_one_mixed_core44_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

Primary證書為666,135 bytes，SHA256
`1ba290846949126b5b3cc8c1e3dea1a99057663396026ed28638e9331fdbe4b0`；
checker為18,105 bytes，SHA256
`1ad2bf2344ab4af9f990cfea42aa6c8530babfd5486d22c33f0aa31c34b31e2a`。
Primary與獨立auditor的default／seed17逐byte replay均通過，兩份script syntax check通過。
獨立auditor沒有import primary；完整piece暴力枚舉驗1,886份整piece witnesses，
另一份全圖枚舉得到1,952份完整染色，核對全部1,232份joint composites及352份全圖witnesses。
全部3,840fibres中352非空／3,488空，50pair-mask與五個source hashes一致，primary bytes無漂移。
`lake build`通過8,831 jobs，只有既有lint；沒有新增Lean theorem。
`check_docs.py`通過577份Markdown／6,771個local links；正式docs的DocGraph
通過62份metadata documents／213 relations／5 families，0 errors。
預設全worktree的DocGraph仍因既有`scratch/task-c44-delivery/repository/docs/`
複本duplicate-id而exit1；保留scratch與此FAIL，不寫成全樹通過。
`git diff --check`通過。

未重跑上游全部分類／topology枚舉、ES／ER搜尋、U1／U2大證書與LC額外Lean targets／公理審計。
README／HANDOFF入口及線標記不變，依DOCUMENTATION由guide維護停止點。
新證書低於1,000,000 bytes，依既有門檻保留普通檔案，不改MANIFEST／ignore接受舊漂移。
未commit／push／開PR。
