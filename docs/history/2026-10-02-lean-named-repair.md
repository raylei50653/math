# 具名來源 repair 的 Lean 接手紀錄

日期：2026-10-02。接手基準 HEAD=`8b91f9f`；本輪起始工作樹已含前輪
D₁₃ 的未提交模組與文件，並非乾淨工作樹。保留全部既有變更，繼續使用者
指定的「具名來源 J/P 與 W／C 實例」，未開 sub-agent、未 commit／push。

成果報告見 [NamedRepair](../lean_named_repair.md)，
目前停止點由 [Lean 導覽](../lean_guide.md)及
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護。

## 成果與證據

新增 `Math/NamedRepairCore.lean`、`Math/NamedRepair.lean` 及
`Math/NamedRepairAudit.lean`；34 條普通 theorem 由原35邊接到同一份
十五點 proper coloring、原 U 的 J、指定混合框 P、70個四點 scopes、
完整 exact rejectors／coverage，再接既有 CommonRepair 分類。
兩方向各恰15份 inclusion-minimal repairs、唯一最少對 `{A,B}`、
唯一 forced A 與投影合取模型的 `r*=4` 均已形式化。

局部 source lists 及有限補全使用 kernel `decide`／`decide +kernel`。
有限補全以 `List.all`／`List.any` 明確遍歷原十一份補全；避免對所有
`Fin 8 → Color` 函數搜尋補全。這個效能調整不改變完整投影的存在量詞語義。
所有34條公理審計只出現 `propext`、`Classical.choice`、`Quot.sound`
的子集，無 `sorryAx` 或 `Lean.ofReduceBool`；無新增 axioms、`sorry`
或 `native_decide`。

P 的兩框明定；框可用性與完備性尚未 Lean 化。四個退化圖、任意大小
來源族及 D₁₃ 在核心中的具名替換仍是後續接口，一般出口未證。

## 驗證

```bash
python3 scripts/c5_lean_named_repair.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
lake build
lake env lean Math/NamedRepairAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

- 只讀 provenance check：兩份35邊核心、六個 witnesses、22份具名 U 補全、
  原點序、角色及指定框 supports 對照一致。
- 共同 repair checker：六圖、四個退化支、六個 witnesses、30份覆蓋、
  88次不可省檢查、384份接受 scope 延拓、五個前提獨立性控制通過。
- 來源 checker：兩核心、兩個增大控制、四個退化來源、每核心十一份稀疏補全、
  5,760份完整延拓、十二項負控制通過。
- 完整 `lake build`：8,831 jobs 通過；新模組無警告，既有
  AttachmentOrder／SymRelabel 警告沿用。
- NamedRepair axiom audit：34條全通過。
- 文件檢查：408份 Markdown；DocGraph：62份文件／213條關係／五個 families，
  零 errors／notes。Diff 及新增檔 whitespace 檢查通過。

原 artifacts bytes 未改。未重跑其他替換族、D₁₃ checker、大枚舉或其他
模組的獨立 audit；未更新工具鏈。文件更新專題報告、README 模組入口、
兩條導覽、STATUS 索引及舊報告後續入口；HANDOFF 的研究線與 tags 不變，
依文件治理保留薄入口。

## 跨對話接手

可貼用：

> 基準 HEAD 仍為 8b91f9f，工作樹含前輪 D₁₃ 與本輪 NamedRepair 未提交成果。
> 兩個十五點核心已由原35邊形式化 J、指定兩框 P、全部70個 scopes 的 W／C、
> 各15組極小 repairs、唯一最少對及 r*=4，共34條普通 theorem，無 sorry／native_decide。
> 先讀 docs/lean_named_repair.md 及 docs/lean_guide.md；重播入口為
> python3 scripts/c5_lean_named_repair.py --check、lake build、
> lake env lean Math/NamedRepairAudit.lean。下一步將核心內 D₁₃ 的具名附件
> 接到 cap_sealed_replacement，保持原 U 的 J 與指定框 P；disk 框完備性另證。

## 後續整合提交

使用者在上述研究完成後要求 `commit + push`。本整合提交一併收錄前輪
D₁₃ 的22條定理與本輪 NamedRepair 的34條定理、兩份 audit、來源核對腳本、
成果報告及相連導覽／索引／歷史文件；既有 artifacts 不變。

研究程式未再修改，沿用上述已通過的 checker、完整 build 及公理審計。
提交前重新核對文件、DocGraph、diff whitespace 與 artifact 無變更。
本紀錄前文的「未提交」及接手摘要保留研究完成當時的狀態；目前提交與
遠端發布狀態以即時 Git 為準。
