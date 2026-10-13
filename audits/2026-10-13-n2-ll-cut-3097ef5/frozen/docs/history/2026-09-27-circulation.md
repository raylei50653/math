# 2026-09-27：C5 循環流重述與整數 orbit 覆蓋

報告見 [C5 循環流](../c5_circulation.md)。依使用者提出的五點有向圖模型，
從現有 pattern order、partition screen 與計數程式獨立重算；貼文 sandbox
檔案未在此環境取得，沒有把它們列為已重播來源。

完成十座標恆等式與六維循環流的紙面等價、十二循環完整分類，核對 1,023 個
非空 masks 恰有 153 通過、零差異；保存 870 個拒絕的封閉可達集見證。
十二單位循環與既有 B₅ rays 完全相同；36 份三-split 整數 orbit 覆蓋各核對
全部 240 個 assignments，結合整數循環分解，推出任何非負整數恆等式解皆通過
三套分開的既有 orbit 計數要求。另保留十一個 independent singleton faces。

這是抽象代數與 finite certificate；沒有新增來源排除、一般 m≤0 或 Lean theorem。
主線仍是 record 110 的共同切口／實際 tethers，相連分量與完整關係的要求不變。
新 checker、JSON、專題報告及 README／HANDOFF／STATUS 導航一併整理為發布範圍。
舊計數、B₅ 與座標報告只增加有日期的後續入口，保留原有歷史證據敘述。

發布前實際驗證：

- `python3 scripts/c5_circulation_audit.py --check`：逐 byte 重播通過；秩 4／維數 6、
  十二循環、153 非空支撐／870 拒絕、零 mask、十二射線對照、36 份 240 座標
  orbit 覆蓋與十一個 independent faces 全部通過。
- `python3 scripts/c5_kempe_screen.py --check`：153／142／132 的既有 screen 結果原樣重播。
- `python3 scripts/c5_b5_face.py --check`：既有十二圖、特殊 faces 與 gluing 證書原樣重播。
- `lake build`：8,826 jobs 成功，僅重播既有 linter warnings。
- `python3 scripts/check_docs.py`：183 Markdown 頁／2,242 本地連結、索引與
  HANDOFF 150 行上限通過。
- `python3 tools/docgraph check`：20 documents、43 relations、4 families，0 errors／notes。
- `git diff --check`：通過。

未重跑大圖 catalogue、degree-5/R 系列、record 110 surgery、全策略閉包或舊
adjacent-singleton 的全部 witness 搜尋；本輪需要的 orbit generator 已由新 checker
直接重算。build 不認證本頁新紙面論證。依使用者明示要求 commit＋push，
提交與遠端狀態以即時 Git 為準。
