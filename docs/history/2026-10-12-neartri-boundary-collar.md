# 近三角化完整外圈：本輪結果與交付範圍

2026-10-12。[權威入口](../archive/reports/c5/structure/c5_neartri_boundary_collar.md)／
[隔離證據包](../../audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/REPORT.md)。
本輪未 commit／push。初始 BASE 為 `5d70a39940182ea37c9ca5d36d9ebb7f612160ad`；
執行期間另一路提交 `bc7c0820e6b5e585869b8a59e04f52da0dad2d33` 的度數界與任務。
原凍結输入保留，新接入文件另有 CONCURRENT_INPUTS；未回復或改寫他人的提交。

本輪直接以完整染色限制排除二邊 crosscuts，再沿原邊界鄰點的具名環帶證
933 的 h≥3、n5≥9，以及 941 的 h≥2、n5≥8。最低殘留只剩 941 的
`(4,4,5,4,5)` 外框與 C7 55列必要上界；上界非來源實現。
普遍論證、有限完整欄／fibres、獨立 checker 與未解共同見證分開。

當輪驗證：主 checker 924 完整接合、9,240 具名方向、8,778 目錄 unions；
21 份環帶的 42 項必要閉包排除 41 項。獨立程序用完整 S4 接合、反向欄生成、
restricted-growth partitions 及非同步刪除得到相同結果。
正常／seed17、完整 lift／固定點破損、缺檔與 exclusive-create 控制及文件檢查
以證據包 verification.json 為準。`lake build` 通過 8,831 jobs，僅既有 linter
warnings；沒有新增 Lean 定理。沒有重跑外部計數證書或大型來源圖枚舉。
文件連結／索引、正式 docs 的 DocGraph 及 `git diff --check` 通過；全工作樹
DocGraph 仍因保留的歷史 audits／scratch 重複 IDs 失敗（62 項），未改動那些快照。

來源子域 closure：最小目錄外圖中所有非相鄰兩框接點的二邊 crosscuts。
Canonical Source + Evidence：完整外圈權威入口及隔離 REPORT／兩份主證書。

Updated：共面正規形及既有度數界加入後續連結；Kempe 導覽及 STATUS 接入新下界
與精確 C7 殘留；三份任務標示 C 的來源子域已被 crosscut 排除，但其另訂 132²
cap joins 未執行，不能混稱計算任務完成。

Reviewed-unchanged：README／HANDOFF 的研究線與入口不變；E-ARC2／N2 採不同
edge-critical 前提，沒有引用本輪結論去改其覆蓋、來源或證書。

Remaining OPEN：941 最低外圈的同圖 C7 可實現性／完整覆蓋，h≥3，一般五度
可縮減性、跨邊 J_e 同步、十三內點以上來源與 K∞=K≤5。
Propagation stop：L2；父題仍 OPEN，沒有研究線增減，無需更動全域入口。
