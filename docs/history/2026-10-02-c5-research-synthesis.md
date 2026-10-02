# 2026-10-02：C₅ 全線整合、可反駁假設與投影階數初驗

提交整理（2026-10-02）：使用者後續要求 commit，將整合報告、階數checker、
完整證書及相關索引一併作本機提交。研究重播與Lean build沿用本對話
已通過的結果；提交前核對證書全部來源SHA並重跑文件與staged whitespace檢查。
本次未要求push；下文「未要求commit／push」保留初步研究完成時的語境。

基準 `4565735`，接手時工作區乾淨。使用者要求整理整個C₅研究線，
提出高階整合假設，可以先做初步驗證、後續再實驗。未要求commit／push，
本輪未開子代理，未新增圖或class-pair搜尋。

成果見[全線整合](../c5_research_synthesis.md)及[關係階數](../c5_relation_arity.md)。
README與STATUS加入跨線入口；state／兩點重疊導覽加入新階數結果。
依[文件治理](../DOCUMENTATION.md)，研究線與tag不變，HANDOFF保留原清單。
各線現有停止點沒有被實驗提案取代。

## 新增結果與界線

- 紙面推導精確接合的 `r*≤d(J)≤max(d(Σ_A),d(Σ_B))≤5`。
  這是完整字面關係的投影上界，不是內點上界或多步state充分性。
- 紙面推導S4不變的proper C₅關係若全收T4，則四點投影足夠。
- 132類來源階數為11個二階、101個四階、20個五階；五階類分四個D₅軌道。
  由原邊集重算20反例的完整Σ，保存100份四點scope的完整原圖延拓。
- 1,024個抽象masks有140個不具四階性；全部32個T4全收masks通過，
  含933／941，所以四階性不能充當這兩候選的幾何排除。
- 六個原具名接合從原邊及rotation／交錯路徑證書重建J/P；r*為四個0、兩個4。
  未重新枚舉全部極小repair組合，也未新查class pair。
- H1（候選來源ε≥2）、H2（no-mixed root樹分離）、H3（同Σ的weak出口一致）
  均有精確前提、既有支持、反駁方式與小域實驗；未將有限支持標成一般證明。

## 實際驗證

新artifact以 `python3 scripts/c5_relation_arity_audit.py` 生成，127,300 bytes。
以下檢查通過：

```bash
python3 scripts/c5_relation_arity_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_relation_arity_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

Lean build完成8,831 jobs，只有既有AttachmentOrder／SymRelabel linter warnings。
無新Lean檔，未重跑個別axiom audits；本文兩個紙面引理沒有被形式化。
文件檢查通過417份Markdown、4,265個本地連結；DocGraph通過62份文件、
213條關係、5個families，零errors／notes。

未重跑：大型cell／reduced枚舉、全部no-mixed及mixed來源排除checker、
933／941系列checker、weak-deletion lattice、全部來源替換族、獨立planarity
catalogue驗證。進展摘要沿用當前原報告；新程式重驗範圍如上。
原catalogue及兩點重疊artifacts未改寫。Git發布狀態以即時查詢為準。
