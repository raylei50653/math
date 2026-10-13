# 2026-09-30：C₅ 四點投影的最少個數與唯一組合

本輪接續三點投影的未提交成果，固定原反向十五點三十五邊圖、
同一完整八點 J 及兩框拉回 P。未 commit／push；發布狀態以即時 Git
為準。目前停止點見[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)。

## 成果與證據

- 新增[報告](../c5_two_vertex_quaternary_repairs.md)、
  [checker](../../scripts/c5_two_vertex_quaternary_repairs.py)與
  [完整證書](../../artifacts/c5_two_vertex_overlap/quaternary_repairs.json)。
  原 J 從原邊及七內點回溯重建，全部投影由完整 J 計算。
- 在 P 單獨為基底的模型中，70 份完整四點投影分成八種排除集合；
  無單投影修復，全部 2,415 個無序 scope 對中只有一組成功。
  最少恰為兩份，唯一組合是 `(a0,a1,a2,a3)` 與 `(a2,b0,b2,b4)`。
- 證書保存 70 份完整投影、54 軌道／1,296 份完整差集、每列的全部
  拒絕 scopes 及原邊矛盾、每個單投影及配對的剩餘差集索引。
  配對 bitsets 與完整具名集合交集一致；唯一解另在全部 `4^8`
  賦色上查詢並精確比對 J。
- 三份見證 `01232112`、`01212132`、`01012122` 分別迫使第一
  scope、限制第二 scope、排除錯誤候選；192 份原圖四點延拓及
  4,608 份共同 S₄ 換色核對保存。第一 scope 在任何四點修復中都
  不可省，第二 scope 只在最少兩份時被迫。
- 紙面推論同時給出任意最大 arity≤4、無輔助變數局部合取的
  兩條件下界，以及恰兩條件時的唯一必要 scopes；未分類任意
  條件表本身。不涉及更一般 Boolean 或輔助變數表示。
- 更新前報告後續狀態、兩點重疊／state 導覽與 STATUS。依現行
  文件治理，研究線及基本入口未變，README／HANDOFF 不追加成果摘要。

## 驗證及工作狀態

一般生成及一般／`PYTHONHASHSEED=17` 逐 byte `--check` 已通過；
證書大小為 3,876,919 bytes。九項 verifier 負控制按預期
拒絕：漏 scope、改具名欄序、刪合法 tuple、加非法 tuple、同基數
錯誤剩餘集合、漏配對、漏最小解、加假最小解、延拓違反原邊。
前輪三點 checker 重播通過，包含其六項負控制及原 J 重建。

`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；未將新結果 Lean 化。文件檢查通過 382 份 Markdown／
3,879 個本地連結；DocGraph 通過 62 documents／213 relations／
5 families，零 errors／notes。`git diff --check` 通過。

本輪未重跑來源大枚舉、目錄最小性、獨立拓撲／單框 checker、
六份接合 checker、點對索引或 Lean axiom audit；沿用證書的來源
hash 鏈均核對。未修改 Lean，沒有新 Lean theorem 或 `native_decide`。
沒有覆寫前輪 scripts／artifacts，沒有操作 Git index，保留既有變更。

下一窄題為同一 P 上全部 inclusion-minimal 四點修復，特別是不含
`(a2,b0,b2,b4)` 的較大不可省組合。本輪只完成最少個數與全部達到
該個數的組合；一般多步充分性與 `K∞=K≤5` 仍未證。
