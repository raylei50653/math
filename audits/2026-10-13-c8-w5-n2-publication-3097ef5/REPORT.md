# 三份研究交付的發布核對

2026-10-13，BASE `3097ef5be241b7777451a5ef8a663f3987d6b866`。
本包只記錄C₈、W5私人單環及N2 LL-CUT+diag的原證據保存、focused replay與
相連文件發布；採納結論及精確OPEN邊界見[整理紀錄](../../docs/history/2026-10-13-c8-w5-n2-publish.md)。

[verification.json](verification.json)列本次實際回歸與未重跑範圍，
[N2 receipt](n2/receipt.json)、[W5 receipt](w5/receipt.json)及[logs](logs/c8-verify.log)
保存原命令結果。[原檔manifest](original-bundles.json)鎖定828個非快取payload的
SHA256／大小／mode；[custody](custody.json)另核舊封存records、新gzip逐byte還原
及Git index輸出。這些核對不替代數學證明，也不把finite controls升格為來源實現。

原三包及frozen檔案保持bytes，新增发布routing只在當前docs。
新checkout先執行 `python3 tools/audit_archive.py restore --artifacts`，再按各
權威報告重播；本包不更新舊seal、歷史hash失敗或生成紀錄。

沒有來源圖大枚舉、外部計數重播或新增Lean theorem；`lake build`只回歸現有專案。
正式docs與全工作樹DocGraph分列，後者若有凍結副本duplicate-ID仍記FAIL。
本地checks不聲稱遠端CI通過；發布SHA與工作樹狀態由即時Git及最終回覆確認。
