# D₁₃ 首層具名替換的 Lean 驗證紀錄

日期：2026-10-14。基準 HEAD=`77fbd5d`；起始工作樹已有其他研究及工具的未提交變更，
本輪保留這些變更，接續 [Lean 導覽](../lean_guide.md)所列的具名 D₁₃ 替換缺口。
本輪未 commit／push、未更新 Lean／mathlib 鎖檔、未重新生成原來源 artifacts。

同日後續：[C4／T1／Lean 整理發布](2026-10-14-c4-t1-lean-progress-publish.md)
記錄本次使用者授權的 commit＋push 與重播；下文保留形式化當輪語境。

成果與完整前提見 [具名首層替換](../lean_named_replacement.md)。
實作為 [NamedRepairReplacement.lean](../../Math/NamedRepairReplacement.lean)，
公理清單為 [NamedRepairReplacementAudit.lean](../../Math/NamedRepairReplacementAudit.lean)，
原始審計輸出見 [lean-audit.txt](../../artifacts/lean_named_replacement/lean-audit.txt)。

## 成果及精確範圍

32 條普通 theorem 完成兩方向、A 單側、B 單側、雙側各一次替換，
亦包括兩側都保留原 wheel 的控制模式。替換圖依實際邊表定義，
不是把原 J 重新命名。原35邊分解為十三點外部27邊及兩組完整 wheel；
兩個中心均密封，依序固定 A `(h7,y,h9,x)` 與 B `(r,q,w,p)` 四接點。

`exteriorRelation_eq_core` 保留同一十三點外部 row 的完整接受關係，
`joint_iff_graph` 明列同一份 actual full proper coloring 對原 U 的延拓，
`joint_eq`、`candidate_eq`、`system_eq` 再保 J、指定框 P 及完整 repair 系統。
各方向／模式的十五組極小 repairs、唯一最少 pair、唯一 forced A，
以及原 J 投影合取、無輔助變數模型的 `r*=4` 均已傳遞。

A／B 單側替換是23點59邊，雙側是31點83邊。
兩原中心均不在十三點觀察介面中；單側模式未另證另一中心顏色保持。
結論是完整延拓支持相等，沒有宣稱內部 fibres 的延拓數量相等。

## 實際驗證

```bash
python3 scripts/c5_lean_named_repair.py --check
lake env lean Math/NamedRepairReplacement.lean
lake build --no-ansi
lake env lean Math/NamedRepairReplacementAudit.lean
python3 scripts/c5_lean_named_replacement.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

- 既有具名來源核對：兩份35邊核心、六份 witnesses、22份完整 U 補全、
  原點序、角色及指定框 supports 全通過。
- 新模組獨立 Lean 編譯與 olean 建置：exit 0、無警告。
- 預設 `lake build`：8,832 jobs 通過；新模組無警告。既有
  `SymRelabel`／`AttachmentOrder` 的 linter warnings 沿用。
- 公理審計：32／32 公開 theorem 各列一次，原始輸出逐名核對清單相同；
  依賴聯集恰為 `propext`、`Classical.choice`、`Quot.sound`，
  無 `sorryAx`、`Lean.ofReduceBool` 或新增外部公理。
- 新來源核對：以 Lean `#eval` 匯出八份 actual graphs 的頂點數與邊表，
  兩方向、四模式的完整具名點序與原 Python core／cap 施工一致；
  vertices／unique edges 為15／35、23／59、31／83。
  Raw lists 分別43／67／91條，恰重複八條 rim 邊，沒有隱藏額外接線。
- 獨立唯讀 review：外部27邊與原核心完整分解、actual graph 語義、
  十三點 row 到 J／P／system 的傳遞通過；另將六個 once-only 圖逐邊
  對照既存 `repair_caps.json`，全部相同。

- 文件檢查：678份 Markdown、8,798個本地連結，anchors／索引／handoff／導覽現況卡通過。
- 正式 docs DocGraph：95份文件、358條關係、12個 families，零 errors；
  一項 INFO 為既有 `c5.no4ct` family 只有 `c5.no4ct-handoff` 一份成員。
- `git diff --check` 與六份新檔的 newline／尾端 whitespace 檢查通過。

未重跑 LC 生成證書、大枚舉、原 D₁₃ 的整份 Python checker 或全樹 DocGraph；
不將預設 build 說成 LC completeness／topology 的形式化。

## 文件及停止點核對

Closure scope：兩核心指定首層、完整十三點共同外部關係及原 U 的 J／指定框 P／repair 傳遞。
Canonical Source + Evidence：新 Lean 模組、32項 audit 與只讀來源核對。

Updated：成果報告、Lean 導覽、兩點重疊導覽、STATUS 索引；
具名 repair、四接點、共同 repair 與 caps 報告補有日期的後續入口，保留原輪語境。
新模組匯入 Math.lean，README 模組表補入口。

Reviewed-unchanged：HANDOFF 的研究線與 tags；Phase B 的密封完整 relation／同框族傳遞接口。
本輪只提供新的具名首層實例，不改抽象接口或研究線範圍。

Remaining OPEN：任意層數的遞迴實際接線及 ownership、disk 嵌入與全部可用框、
其他四接點實現、改寫完備性、Gallai／minor／枚舉 completeness、一般主命題。
Propagation stop：L2 的直接來源及 consumers；新模組入口作使用方式更新，
沒有一般數學結論變動，不展開其他研究線或跨線 synthesis。
