# C5 翻邊、三步分類與 Σ 編碼整理發布

2026-10-13。使用者授權 `commit + push`。本輪整理起點為
`7ad5fb534a8f0a883db5efc20a4018d9c949acb0`；遠端查得
`50d5474f2446403f3b3001d5943571184c8c9936`，兩者之間已有一筆 K4 提交。
本次新提交只收錄下列 cell 工作；正常推送亦包含該既有祖先提交。

## 成果及界線

- [翻邊引理、工具與編碼](../archive/reports/c5/state/c5_cell_flip.md)：同一共同刪邊圖的四格完整 lifts
  給出保 Σ 充要條件；`891→987` 與一內點同關係代表分開核對。
  五格加五格座標使邊界旋轉及加弦成 bit 操作；兩組具名反例說明相同 Σ，
  甚至相同十列延伸數，仍不決定相同局部 flip 的結果。
- [三步距離與分類](../archive/reports/c5/state/c5_cell_flip_classification.md)：132 份目錄代表保留實圖
  作深度三 BFS，20,531 個狀態、132×132 有向距離表及 29 組有限特徵。
  最短性限工具選取的 disk rotation；`>3` 不作全域不可達宣稱。

指定 flip 的四十位元 support 描述不替代完整 fibres 或可迭代實圖。
本輪沒有新增 Lean 定理、任意大小閉包、保 Σ 一般縮減或所有代表的分類。

## 發布核對

本輪重新執行：29 項 cell 測試、凍結輸入的完整 atlas 重播、獨立 20,531 圖
checker、八份路徑的 full-lift／四格與 CSV 核對，以及編碼反例 checker。
編碼核對包括四份完整報告、1,024 次編碼往返及 5,120 次加弦公式控制。
`lake build` 通過 8,831 jobs，保留既有 linter warnings；此結果不將新增 Python
證據提升為 Lean 形式化。全部既有證據包、BASE 與 manifests 保持原位元組。
距離 CSV 使用標準 CRLF，對該單一檔案加入 Git `-text`／`cr-at-eol` 屬性，
保留證書雜湊且繼續檢查實際行尾空白；不改寫原 CSV 或 manifest。

完整工具測試 94 項及 Git index 大型產物儲存政策檢查通過。
文件與正式 docs DocGraph 另依發布時實際結果核對。
全工作樹 DocGraph 的既有 frozen audits／scratch 重複 ID 與正式 docs 分開報告，
不刪舊快照來消除這類錯誤。Git 提交及遠端一致性以最終即時狀態為準。

## 文件傳播

Updated：兩份權威報告、State 導覽、STATUS 與本紀錄。
Reviewed-unchanged：README 的使用方式與 HANDOFF 的研究線清單；本次沒有研究線增減。
Remaining OPEN：任選嵌入的全域最短路、其他同 Σ 代表、多步充分狀態及一般保 Σ 縮減。
Propagation stop：L1；沒有上推既有研究主命題。

提交範圍為三份 artifacts 目錄、三支 scripts、兩份測試、兩份專題報告、
State 導覽、STATUS、本紀錄及上述單檔 Git 屬性；只 stage 該連接範圍中的明列檔案。
