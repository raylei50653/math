# 四項突破驗證整理發布

2026-10-29。依使用者要求，從基準 `4476049e71dfb6eb86538052f9730e6d57b928b0`
提交[四項分別驗證](../four_color_four_fronts_verification.md)、四份獨立腳本、完整小型證書
及直接文件更新。研究階段原收據與「未提交」文字保留當時語境；目前發布狀態以 Git 為準。

七邊結果是在全體頂點最小裸平面反例前提下的紙證，非平凡邊割下界提高為八。
兩步瓶頸與三角 anchor 有紙面推導，維度界限限於指定原邊來源；新增推論未 Lean 化。
剝殼選序未給共同非空性，標準 B5 錐仍容許 932；LOCK-NO-GAIN 與一般 932／4CT OPEN 不變。
本次沒有修改主求解器、擴大研究枚舉或重寫歷史 frozen 證據。

## 發布檢查

- [完整工具測試](../../audits/2026-10-29-four-fronts-verification-4476049/publication/tool-tests.log)：515 項通過。
- [Lean 建置](../../audits/2026-10-29-four-fronts-verification-4476049/publication/lean-build.log)：8,834 jobs 成功；保留既有 linter warnings。
- 四項研究重播、既有 Lean 公理核對及 Errera 控制沿用同次已完成的
  [研究驗證收據](../../audits/2026-10-29-four-fronts-verification-4476049/verification.json)，
  本次逐份核對來源、文件與證書的全部19個雜湊相等。
- 正式文件、docs-only DocGraph、實際 Git index 產物政策與空白檢查另存
  [發布收據](../../audits/2026-10-29-four-fronts-verification-4476049/publication/checks.json)。
- [全工作樹 DocGraph](../../audits/2026-10-29-four-fronts-verification-4476049/publication/docgraph-whole.log)
  仍因保留快照／scratch 的重複 ID 出現72項錯誤，與原停止範圍相同；不改稱全域通過。

直接消元／邊割來源、求解導覽、4CT導覽與 STATUS 已更新，HANDOFF 的研究線及活躍標記不變。
本次沒有新增大型產物或例外規則；只提交相連檔案。
推送後核對本地、tracking、遠端分支 SHA 與乾淨工作樹；遠端 CI 分開回報。
