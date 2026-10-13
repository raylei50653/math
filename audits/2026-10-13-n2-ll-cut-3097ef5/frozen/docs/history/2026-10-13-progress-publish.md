# N2、W5／C₇與跨邊搬運進展整理發布

2026-10-13。使用者授權「整理目前進展 commit + push，可分為多個 commit」。
起點本地 HEAD 與遠端 main 均為 `19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
本次整理七份隔離交付及其相連報告、直接父摘要與研究線導覽。

## 採納結果與停止點

| 主題 | 本次整理的精確結果 | 保留界線 |
| --- | --- | --- |
| [N2 一long](../c5_excess_two_n2_one_long_closure.md) | 原末端block minors與固定root完整接回排除完整原55 `(1,0)`；九格八格覆蓋 | 原55 `(2,0)`、一般N2及E-ARC2 OPEN |
| [N2 雙long](../c5_excess_two_n2_double_long_joint.md) | 共同容量接回排 `t=0,1`；剩 `{3,3},t=2/3` 或 `{3,4},t=2`，有效H≤29 | LL-CUT、同一列原完整joint仍缺，不能把可行矩陣當來源 |
| [W5 三色支援](../c5_w5_three_color_support.md) | 同槽位R³相等恰給保B/U pins的雙向total full-lift對照；最小來源私人森林排除，另有特定 `r_min=2` 構造與來源專用商圖no-go | 對照不是fibre雙射；私人含環來源的合法 `r≤6` 代表存在性OPEN |
| [C₇ 外圈](../c5_neartri_boundary_collar.md) | 同圖共同延伸計數排最後具名55列上界；933／941均必 `h≥3,n5≥9` | `h≥3` 來源、十三內點以上一般排除OPEN |
| [跨邊 Kempe](../c5_cross_edge_kempe.md) | 五度輪逐lift雙射、相鄰中心共同缺陷搬運、計數式與單步escape判準 | 普遍同步、一般多步escape與933／941來源排除OPEN |
| [強迫異色](../c5_forced_inequality_transport.md) | 一般平面圖距離無界、證書寬度≤5；分叉／交錯限制及clique分隔枝塊透明 | 原低超額critical C₅來源未觸發；F／Z原域OPEN |

各普遍命題依各來源的紙面證明及明列外部依賴；有限完整fibres與負控制校準
明列圖域。真正最小933／941與完整N2目標仍標 `not triggered`，零觸發不是
來源排除。沒有新增Lean theorem，`K∞=K≤5`仍未證。

## 原證據保存與發布核對

七份原包共413檔的bytes、frozen輸入、seals與舊失敗紀錄全部保持。
八份大型JSON及兩份歷史whitespace原文以既有主封存格式保存，追加10個
路徑、7個gzip blobs、684,507 compressed bytes。既有2,455個原路徑records
及1,527個blob records不改；不重建原產物、不更新舊seal。
新checkout先依[封存說明](../../audits/README.md)還原，再執行各權威報告的checker。

本次另從Git index及封存blobs在新目錄重建全部413檔，逐檔核對SHA256／大小，
確認stage只含明列證據白名單；新重播與詳細結果見
[發布核對](../../audits/2026-10-13-progress-publication/verification.json)。

- N2：七支focused checker各跑normal／seed17，14/14通過；五份保存的破損證書均拒絕。
- W5／C₇：11次focused重播通過；其中C₇聚合器涵蓋16項normal／seed17／破損控制，三份破損證書拒絕；森林另有seed17及刪lift反控制。
- 搬運：跨邊normal／seed17、目錄及獨立完整lifts，強迫異色與替代構造normal／seed17均通過；保存的刪lift證書拒絕。跨邊九項validator及三項獨立破損控制在byte相同的臨時副本重播通過。
- 當前各包最終manifest／DELIVERY及frozen inputs核對相符；一long舊manifest的一項文件hash與跨邊舊ROUTING的共享文件hash差異保留其歷史語境，不修寫原證據。
- 文件連結／索引、正式docs DocGraph、Git whitespace及staged大型產物policy均通過；最終數字以發布核對為準。
- `lake build`回歸通過（8,831 jobs，既有linter warnings保留），只驗現有Lean專案。
- 全工作樹DocGraph仍FAIL：62項凍結副本／scratch重複ID；正式docs通過不當成全域PASS。

未重跑上游大型來源枚舉、全部歷史產物生成、外部文獻計數或舊Lean證書全套。
本次發布不覆寫任何歷史失敗，也不以這些本地結果宣稱遠端CI成功。

## 文件傳播與提交分組

Updated：N2新來源與直接consumers、W5新正式入口與原商圖報告、外圈及其
度數父摘要、跨邊／強迫異色入口、Kempe／State導覽與STATUS對應條目。
Reviewed-unchanged：README／HANDOFF的研究線、入口與進行中標記未變；
其他ε／Gallai／R系列、Lean指南及舊audit的完整前提未獲新一般結論。
Closure scope只含上表各自明列子域；Propagation stop為L2，父命題維持OPEN。

提交分為原證據與封存、N2來源、W5／C₇來源、跨邊／強迫異色來源、共同導覽與
本發布核對。僅stage相連白名單；推送後核對HEAD、origin/main及遠端main相等，
並確認工作樹乾淨。最終SHA以即時Git與本次回覆為準。
