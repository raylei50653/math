# K≤14、W5 圈秩四與組合圖譜整理發布

2026-10-13。使用者授權「整理目前進展 commit + push」。整合起點與三份
原 audit 的 BASE 均為 `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。
本次整理兩組既有成果、重播相連證據並發布，未擴大研究枚舉。

## 採納範圍

| 成果與權威入口 | 本次確認 | 剩餘界線 |
| --- | --- | --- |
| [十四內點界](../c5_k14_sphere.md) | 一般有序 disk-C₅ 的 `K≤14=K≤5`；73球面嵌入、1,001根圖及180,228完整 lifts 主／獨立一致 | K≤15、K∞、任意大小933／941 |
| [C₈ 紙面加強](../c5_k14_sphere.md) | 原h=3八项完整契約必k≥16，沿用原面配對／無葉點證明 | 八項任意大小來源仍留；不採納一般h≥4 |
| [W5 圈秩四](../c5_w5_private_rank4.md) | 完整全域最小內點／最大邊數來源下，任取合法全內部W5，私人ρ≥5；contractible 6,389及essential 2,872完整模板重播 | ρ≥5一般排除／縮減、annulus小代表及R³保存 |
| [組合圖譜](../c5_combinatorial_atlas.md) | 1,023原始masks／135 D₅類；24已知disk類、2 OPEN類；132原witness重播 | 不把必要screen、兩側交集或canonical索引當單側來源實現 |

紙面、外部定理、生成器完備性及Python完整有限證書分層。保留同一原圖、
有序色框、實際附件、rotation、全部fibres／空格及full lifts。
一般`K∞=K≤5`、一般單側／共同出口、E-ARC2與一般五度縮減仍OPEN；
沒有新增Lean theorem，實際933／941最小來源仍`not triggered`。

## 原證據保存及本次驗證

三份原 audit 的185個非快取檔案保持原 bytes、modes、DELIVERY、frozen inputs、
成功與失敗紀錄。[保存核對](../../audits/2026-10-13-k14-rank4-atlas-publication/verify.py)
與[原檔清單](../../audits/2026-10-13-k14-rank4-atlas-publication/IMPORTED.json)
獨立記錄本次整合；11個含歷史whitespace原路徑與7個gzip blobs追加到既有
ARCHIVE，新增12,041 compressed bytes，舊2,501 paths／1,560 blobs records不變。
原始檔仍留在本地；新checkout先依[audit還原入口](../../audits/README.md)還原。

Contractible 原`verify.py`要求HEAD=BASE、空index及既有audit未改，已在
本次staging前取得PASS。發布後保留其隔離條件，使用本次保存核對確認原bytes，
不改舊seal或將歷史gate的適用範圍擴大。

本次重新執行三包主／獨立完整checker、原輸入／seal核對、K14負控制與真正
空fibre校準、W5兩支負控制及必要模板domain／係數計數，全部通過。
圖譜normal及`PYTHONHASHSEED=17 --check`的八份產物逐byte一致；既有
Kempe screen及132份cell witness checker亦通過。圖譜各來源hash與BASE吻合。
完整命令、退出碼與receipts見[發布核對報告](../../audits/2026-10-13-k14-rank4-atlas-publication/REPORT.md)。

`lake build`完成8,831 jobs，僅記既有Lean回歸。正式文件／DocGraph檢查通過；
全工作樹DocGraph仍有62個既有凍結副本duplicate-ID錯誤，獨立列為FAIL。
沒有重跑完整plantri生成、外部Dvořák–Lidický計算證書、舊大圖搜尋或瀏覽器互動測試；
這些原輪次紀錄保留，不冒稱本次全量再驗。

## 文件傳播與發布

Updated：兩份新數學入口及直接consumers、Kempe導覽、組合圖譜與State導覽、
README圖譜入口、STATUS索引、audit還原入口與本次歷史。圖譜的當前
`K≤14 OPEN`文字修正為`K≤14=K≤5`，殘留改為K≤15；原輪次歷史保留。
Reviewed-unchanged：HANDOFF研究線及進行中標記；跨線synthesis／common-language
沒有一般closure，故不重寫。
Remaining OPEN：上述任意大小來源、一般縮減與父命題。
Propagation stop：L2；新下界及有限階數界未完成一般父題。

只stage相連白名單；儲存政策、staged whitespace及Git index匯出保存核對通過後
commit、push。發布SHA、HEAD／origin/main／遠端main相等及工作樹狀態以即時Git為準。
