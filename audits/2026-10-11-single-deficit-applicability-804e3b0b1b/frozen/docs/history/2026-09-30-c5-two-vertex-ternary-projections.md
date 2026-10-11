# 2026-09-30：C₅ 全部三點投影不足與四點 arity 下界

本輪接續兩框共同拉回的未提交成果，只處理原反向十五點三十五邊圖
的完整八點 J。未 commit／push；發布狀態以即時 Git 為準。
目前停止點與下一題由[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護。

## 成果與範圍

- 新增[報告](../c5_two_vertex_ternary_projections.md)、
  [checker](../../scripts/c5_two_vertex_ternary_projections.py)及
  [完整證書](../../artifacts/c5_two_vertex_overlap/ternary_projections.json)。
  所有計算保留原 U 欄序、兩個混合框、實際原邊及共同顏色集合。
- 全部 56 個三點投影各等於三點誘導原邊的正常染色關係。
  兩框加上它們後恰等於補回 b2–b4，保留 76 軌道／1,824 賦色；
  原 J 仍 60／1,440，完整差集為 16／384。
- 16 個殘留軌道各保存 56 份原圖三點延拓，共 896 份；另逐份驗
  共同 S₄ 換色所得 21,504 份具名三點延拓。保存全部具名差集、
  原單框分別延拓及 A／B 原邊拒絕證明。失敗型為 A-only 6、
  B-only 8、共同拒絕 2。
- 在原 U 上、無輔助變數的局部條件合取模型中，任何最大 arity≤3
  的修復都不足。兩個四點投影 `(a0,a1,a2,a3)` 與 `(a2,b0,b2,b4)`
  可直接修復 P，故最小最大 arity 恰為四。沒有宣稱投影個數最少，
  也未涵蓋一般 Boolean 組合或存在輔助變數的表示。
- 更新前報告後續入口、兩點重疊／state 導覽及 STATUS。
  依現行文件治理，研究線及基本入口未變，README／HANDOFF 不追加逐輪摘要。

## 驗證與工作狀態

生成及一般／`PYTHONHASHSEED=17` 逐 byte 重播通過。原 J 由原邊與
七內點回溯重建，三點 closure 由 P 篩選與另一份完整 `4^8` 查詢
比對。全部 28 個二點投影另算後給出同一 P refinement；兩個四點
投影直接從 J 產生，與 P 合取恰好等於 J。

六項 verifier 負控制按預期拒絕：漏掉三點 scope、改動固定色、
延拓違反原邊、把三點 witness 當成八點延拓、刪除合法投影 tuple、
加入不可延拓 tuple。前輪共同拉回 checker 及六份接合／四份來源
代表的既有 checker 重播通過。

`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；未修改 Lean，未將新結果 Lean 化。

文件檢查通過 380 份 Markdown／3,861 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及全部 28 份未追蹤文字檔的最終換行／尾端空白檢查通過。

未重跑來源大枚舉、目錄最小性、獨立拓撲／單框 checker、1,320 份
點對索引或 Lean axiom audit；前輪證書及其來源 hash 鏈均核對。
沒有覆寫舊 scripts／artifacts，沒有操作 Git index，保留全部前輪成果。

下一窄題為固定 P 上四點投影的 scope 選擇與最少個數，依其排除的
完整 54 軌道差集分類最小修復組合；此輪未建立該分類證書。
