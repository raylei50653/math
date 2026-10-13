# 共同 repair 判準的 Lean 形式化紀錄

日期：2026-10-02。使用者要求補形式化證明，本輪沿最新共同 repair 研究，
補齊抽象集合判準與分類推論，不擴大來源枚舉。專題報告見
[Lean 共同 repair 判準](../lean_common_repair.md)，目前入口見
[Lean 導覽](../lean_guide.md)及[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)。

## 成果及界線

新增 [CommonRepair.lean](../../Math/CommonRepair.lean) 與
[CommonRepairAudit.lean](../../Math/CommonRepairAudit.lean)，並由
[Math.lean](../../Math.lean) 匯入。27 個普通 theorem 涵蓋：

- 保真完整 relation 的 repair／覆蓋等價、單調性及具名投影介面。
- 三種 exact witnesses、兩類覆蓋與全部 repair 模板的雙向等價。
- 全部 inclusion-minimal repairs、唯一 forced A、三個極大失敗集合及完整殘留。
- 有限 repair 至少兩項，唯一最少解 `{A,B}`，以及獨立的 P=J 空 repair 支。

主判準與極小分類沒有有限 Ω／Λ 假設。27 條公理審計至多依賴
`propext`、`Classical.choice`、`Quot.sound`，沒有 `sorryAx`、
`Lean.ofReduceBool` 或新增 axioms。原圖的 J/P、W／C 與 disk 可用框
尚未形式化；六圖仍是 Python 前提證書，不稱端到端 Lean 實例。

原共同 repair checker／artifact 保留原 bytes、來源 hash 及
`new_lean_theorem=false` 的歷史語境。來源替換族與 D₁₃ 證明沒有改動。
下一個形式化入口是具名 J/P 及 W／C 實例，幾何仍獨立處理。

## 驗證

```bash
python3 scripts/c5_two_vertex_common_repair.py --check
lake build
lake env lean Math/CommonRepairAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

共同 repair checker 通過六圖：四個退化、兩個非退化案例，六個 exact
witnesses、30 條覆蓋等式、88 次逐項刪除、384 份接受 scope 延拓與五個
前提獨立性控制；151,000 bytes 證書逐 byte 相同。

`lake build` 通過8,828 jobs，新模組無 linter 警告；僅回放既有
`AttachmentOrder`／`SymRelabel` 警告。27 條 axiom audit 通過。
文件檢查通過404份 Markdown／4,101個本地連結、錨點、索引及 HANDOFF
格式；DocGraph 通過62份文件／213條關係／五個 families，零 errors／notes。
`git diff --check` 通過。

沒有重跑來源替換族、其他研究線、舊大枚舉或其他 Lean 模組的獨立 audit；
沒有重新生成 artifacts，也沒有執行 `lake update`。

依[文件治理](../DOCUMENTATION.md)，更新專題報告、兩條導覽、STATUS
及 README 模組入口；研究線及 tag 未變，HANDOFF 保持薄索引。
形式化完成時尚未要求 commit／push；後續發布見下節。

## 同日提交與發布

後續依使用者 `commit + push` 要求，將 Lean 模組、27 條公理審計、
函式庫匯入、專題報告、導覽、README、STATUS 與本紀錄納入同一提交。
沿用同一對話中已通過的 build、公理審計及六圖 checker；證明與證書未再修改。
提交前重驗文件、DocGraph 與暫存 diff 的 whitespace，推送後核對
`HEAD=origin/main=remote main` 及乾淨工作目錄。發布狀態以即時 Git 為準。
