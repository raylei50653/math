# 2026-10-08：U4完成與固定完整Σ下兩-root44身份全排

基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
使用者要求「推進 U4」，接續HANDOFF、STATUS、Git與Kempe導覽的N2原mixed11省略身份。
接手時U2／U3及audits、scratch、MANIFEST已有未提交變更，本輪保留。
完整前提、紙面證明與停止點見[U4報告](../c5_excess_two_nonadjacent_two_mixed_core44.md)
及[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)。

## 結果及證據範圍

完整Σ933／941或其整圖D₅像、Σ-critical、ε=2、指定有序induced-C₅ disk，
非相鄰雙degree-5 roots、恰兩原mixed：不存在兩-root44 minimal拒絕列core。
U4恰省略原mixed11 O；原O的盾弧、支援、ordered contacts与完整relation一直計入原G。

核對舊U4支援下界及ℓ+2u≤3，並加強三-spoke star：有一份原unary時，
即使兩mixed都short也需1+1+2=4>3，排除無unary側的retained incidence1。
結合原全四分類，剩餘單triangle帶root marker尾枝及固定六點雙triangle。
任意長run在保留triangle及z singleton下分別縮前後段，保存完整anchor joint。
原O11的整tuple避色查询使每行／每列最多一個禁對；每份M的其餘四個三色列
都有同側座標碰撞的两組完整root pins，O不能再拒這些列，與目標完整Σ矛盾。

有限必要上界為316單triangle標記（含4份已由star排除的放寬控制）＋512雙triangle。
各十個目標D₅ masks共8,280比較：2,484接受空q，5,796容量排除，零殘留。
3,312份非q三色列碰撞全部成立。與U1–U3及前序唯一mixed排除合併，
固定完整Σ下兩-root44身份完成；無44 core來源、單-root、45／54／55、
E5新證明要求、三列一般推廣、ε≥3、一般出口與K∞=K≤5保留。
未新增Lean theorem，未擴大k搜尋或重開K型局部題。

## 完整joint、獨立重播及保留控制

[Primary](../../scripts/c5_excess_two_nonadjacent_two_mixed_core44.py)不import歷史producer；
[artifact](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/observations.json)
保存原邊、完整degree、全部contacts／ownership／附件／支援、完整port tuples及
全圖witnesses。15,460份q-critical刪邊lifts與132,480含空root fibres均保存。

[Independent auditor](../../scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py)不import
primary，另重建必要域、restricted-growth十列、D₅與固定順序全圖回溯。
[audit artifact](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/independent_audit.json)
核對98,096份完整joint witnesses、29,944非空／102,536空fibres，以及全部刪邊与目標判定。
補充二元relation代數控制枚舉65,536份relation，得到65,431份容量相容relation及89份F像。

316張原標記長圖核對3,160份triangle＋root anchor joints、3,160份root-pair relations，
以及33,088份各自的完整contact witnesses。兩圖的全部contact joint在228列不同，
2,932列相同；具名form4／row1保留20份額外long tuples與原圖witness。
這是較強「所有contact座標等價」的反例，沒有把它寫成化約失敗或刪除。
紙面縮減只需共同triangle＋z及兩root joint；原長／短圖的contact資料各自保留。

[控制輸入](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/control_input.json)
逐byte hash追溯舊worktree的U4-SHORT-NEAR-1018。此次重算其原degree、apex rotation、
完整20列core／source relations與19份Σ-critical刪邊witnesses。
「觸發且成立」為單列44与完整接回；完整933／941來源為「未觸發」。
Σ(M)=1022、Σ(G)=1018，新增拒絕第四色列01023，故整十列Σ相等是反例；
本輪只證共同五個三色列相等。舊U4報告／證書／provenance bytes均未覆寫。

## 驗證與重建

```sh
python3 -S scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
PYTHONHASHSEED=17 python3 -S scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
python3 -S scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 -S scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

Primary與auditor的default／seed17逐byte重播通過，兩者只需標準函式庫。
lake build通過8,831 jobs，只有既有lint；這不形式化本輪紙面拓撲。
文件檢查通過581份Markdown／6,840本地連結；git diff --check及本輪新文字檔的whitespace通過。
正式docs的DocGraph通過62份documents／213 relations／5 families；
預設全worktree仍因既有scratch複本的62個duplicate-id而exit1，保留scratch及此FAIL。
完整argv、stdout／stderr、exit codes、來源與產物hash見
[validation.json](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/validation.json)。

另把四份小輸入及兩個新scripts逐byte複製到空輸出的`/tmp/u4-fresh-dkiwipgb`，
以`python3 -S`、seed17分別從頭生成primary與independent audit，兩份大JSON均與
workspace原證書逐byte相同；不依賴uv、NetworkX或歷史producer。
實際argv、cwd、input hashes及stdout見
[fresh_rebuild.json](../../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/fresh_rebuild.json)。

| 檔案 | bytes | SHA256 |
| --- | ---: | --- |
| Primary script | 20,227 | `7a5cf90621956ffe0fb3935e24e76aca68f625585544296dd54cb793f94d7b64` |
| Auditor script | 30,418 | `08c6468707065738df8ea1441fb58419c0af8be53333adb01aadcb9e4af9cfb6` |
| Primary JSON | 11,211,909 | `54da77c7e7c8c7d13fc402d65f4ac3e096bb43767255d3717f6ccbde2f965d96` |
| Audit JSON | 3,001,769 | `74ce25c3d019a1b94548eee4f5cc330be2058441df0024d8fd41e13141b735ba` |

大JSON只按本輪兩個指定路徑登錄MANIFEST／generated ignore，不接受其他舊artifact漂移。
首次uv record因預設cache在唯讀目錄而exit2；改用既有`UV_CACHE_DIR=/tmp/u3-single-uv-cache`
及offline pinned requirements後成功，沒有sandbox escalation或修改舊證書。
未重跑上游全部degree-4／triangle／topology枚舉、ES／ER、LC額外targets／axioms，
亦未重跑U1／U2／U3大證書。README／HANDOFF入口與研究線tag未變，依DOCUMENTATION
由guide與STATUS更新現況。沒有commit、push、開PR或merge。
