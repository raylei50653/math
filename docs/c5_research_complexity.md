# 研究線複雜度與抽象潛力試點

No-mixed、CommonRepair 與 N45 的比較顯示兩種值得區分的工作：把已證共同接口接入更多個案，以及證明現有接口仍欠缺的共同充分條件。N45 的完整接合／恢復是前者；target r-fibre 非空是後者。抽象的收益應與個案接入義務一起計量。

本次來源基準為 `4c6587b43c39a3767fc101fa87d9a7bbe9cde7e3`，日期為 2026-10-11。
此基準保存於[基準設定](../artifacts/c5_research_complexity/baseline.json)，不隨後續 commit 改變。
範圍是 No-mixed 十五側型、CommonRepair 的公開定理及兩具名核心、N45 五個 SHORT 與兩個選定 LONG 身份。BR-SD 子域及其他 N45 身份不在此次盤點內；來源現況仍以各題權威報告為準。

[互動命題表與依賴圖](../artifacts/c5_research_complexity/dashboard.html) ·
[完整統計](../artifacts/c5_research_complexity/metrics.json) ·
[命題 CSV](../artifacts/c5_research_complexity/claims.csv) ·
[分組 CSV](../artifacts/c5_research_complexity/peer_groups.csv)

## 計量方法

每筆命題記錄指向具名來源與行範圍，保存完整適用契約、證據層、結論用途及已核對的局部依賴。以下單位各自計數：

| 指標 | 單位及判定 | 使用界線 |
| --- | --- | --- |
| 平行分支寬度 | 父題內具名身份數；依結論再分 source 排除與指定列延拓 | 分支身份數不等於獨立定理數 |
| 同級命題 | 用途、契約與量詞相近的具名陳述 | 相同依賴深度不足以判定同級 |
| 依賴成本 | 選入圖的直接前提、可達前提聯集、最長鏈 | 圖外外部定理及前層引理另列；零深度不表示沒有前提 |
| 接口重用 | 選入圖的直接使用者及可達使用者聯集 | 未宣告／未選入的使用者沒有被排除 |
| 抽象範圍 | 來源一般性、保留觀測、允許行為三欄 | 任意集合、任意大小限定圖類、指定操作等範圍分別比較，不指定單一數值層級 |
| 接入成本 | 前提模式數與展開後的具名實例義務數 | W／C、角色、保真、arity、拓撲義務分開 |
| 證明骨架 | 來源核對後的共同機制標註及使用身份 | 不把共同定理及其特化結果算成重複獨立證明 |

盤點桶、父題分支分拆與同級比較在資料中分別標為 `inventory_bucket`、`branch_partition`、`peer_comparison`。分組可以重疊，不能相加。CommonRepair 的 27 公開宣告是盤點桶，含 helpers、介面與分類推論；兩個核心的 repair 比較和 arity 比較則是不同結果對同一兩份來源的觀測。

依賴邊由原證明的具名引用或已標註的語義重建建立。Markdown 引用及 DocGraph metadata 不自動變成命題依賴。局部 rank 定義為無選入前提者取 0，其餘取 `1 + max(前提 rank)`；不同研究族的命題拆分粒度不同，不以 rank 排序研究難度。

同源比較始終保存原圖、具名／有序 contacts、actual attachments、ownership、bridges、rotation、同一字面色框與完整 relations／fibres。對稱型只在整份來源資料一起搬運的條件下分組，不逐分量獨立正規化。

## 盤點結果

| 研究族 | 選入記錄 | 選入依賴邊 | 最長局部鏈 | 主要計量單位 |
| --- | ---: | ---: | ---: | --- |
| No-mixed | 27 | 42 | 10 | 15 分支身份＋12 共同／合併陳述 |
| CommonRepair | 31 | 47 | 5 | 27 公開宣告＋同一兩核心的 4 結果觀測 |
| N45 | 17 | 30 | 3 | 8 共同機制＋7 選定身份＋2 限定合成結果 |

共 75 筆記錄、119 條選入依賴，並非全研究線的 75 個去重定理。每筆來源、契約、依賴判定與圖外依賴見資料檔及互動詳情。

### No-mixed 的共同預算

A／B／C／D／E 側跨度下界為 2／2／3／4／3。十五個無序側型中，AD、BD、CC、CD、CE、DD、DE、EE 超過同一原圖的五邊預算，共八個來源排除身份；AA、AB、AC、AE、BB、BC、BE 則由後續共同分離定理得到指定 p₁、p₂ 延拓，共七個身份。

共同跨度命題在此次圖中有 11 個直接使用者，包含八個分支及前層結構使用；共同分離命題有七個直接分支使用者。這是已抽象成功的校準組，而非新來源排除。[十五類預算](c5_no_mixed_span_budget.md#24-統一必要不等式及直接推論)、[免表共同分離](c5_no_mixed_growth_completion.md#4-剩下的-pair-必不影響-r並完成共同分離)保留全部原圖前提與任意分量大小。

八個側型排除和原證書中的支援排除使用不同單位。原 3,760 份 source 支援排除中，3,624 份可用短框邊 K5，另 136 份仍需較一般的固定框弧論證；其中包含未被整側成本排除類型的支援子集。因此，八類共同不等式並未使原支援證書冗餘，也未量出「十五份證明壓成兩份」的成本。[證據總表](c5_no_mixed_span_budget.md#3-把十五輪證據放回同一張表)

### CommonRepair 的模式與實例義務

[CommonRepair](lean_common_repair.md#1-完整集合與前提) 的五種 W／C 前提是三個 exact witnesses、`Covers {A,B}`，以及 `∀e∈E, Covers {A,T,e}`。在兩核心各自 `|E|=14` 的具名模型中，實際是每核心 3 witness＋15 cover＝18 個 W／C 義務，兩核心共 36 個。

這 36 個義務不含 J／P 保真、角色互異、scope 模型、原圖與可用框、arity 或拓撲前提。兩核心各十五組極小 repairs 是分類結果的個數；五種模式是共通接口的前提形狀，兩者不能相除當作證明節省比率。

集合層 `repairs_iff_covers` 在此次圖中有七個直接使用者，角色分類 `repairs_iff_template` 有九個。後者可以重用全部 repair 分類；`r*=4` 另需指定原投影模型的至多三點下界和四點 repair 上界。[具名形式化](lean_named_repair.md#3-精確-witnesses-與分類)已接入這兩個核心的指定兩框，disk 框完備性與來源族拓撲仍在原停止點之外。

### N45 的接口與個案契約

選入 SHORT 的 LOW1／LOW2／HIGH1／HIGH2／HIGH3 五個身份，以及 LONG 的 U-owner=r／s 兩個選定身份。[N45 權威入口](c5_excess_two_nonadjacent_unit_core45.md)的其他身份及 BR-SD 採納未由此七個身份代表。

完整接合／恢復在局部圖中有五個直接使用者、十一個可達使用者；這些記錄保留 ambient 空纖維、原 r 座標、全部 assignments、原省略邊與恢復條件。HIGH2 的三色未用色構造與全部 proper γ 的 JOIN／RESTORE／PALETTE 分開；LONG-s 的 q0 原 SF-QX／BASE 信任鏈與 T1／q2 同源構造分開。

| 抽象候選 | 已有接口 | 須保留的接入義務 | 類型 |
| --- | --- | --- | --- |
| 完整接合與原 spoke 恢復 | 完整賦值的限制／聯集與原邊過濾恆等式 | actual components／contacts／全部 tuple preimages；需要延拓時另給非空 fibre witness | 既有接口重用 |
| own-minimal sole-C 映射 | BASE 的 t=0／1／2 限定排除 | X 的實際 sole C、完整 degree、X 自己的同 β witnesses、spokes／外路／tethers | 既有接口重用 |
| target r-fibre 非空充分條件 | 各個案已有明示構造 | 找到共同充分契約；分清聯集非空、固定 pins 存在及原 spoke 過濾後非空 | 需要新定理 |

`contract_specific` 表示接口使用時須提供該個案的專用證據，並不把已採納個案重新標為未證。H1–H13、K1–K13、K1–K12 的編號數僅描述原契約的封裝，不能視為相同成本的原子義務數；LOW1 的散文契約不虛構編號數。

上述排除是完整契約內的任意大小紙面結論；有限 target-source 控制仍是 `not triggered`。接合等式與零觸發不供給來源排除或一般非空性。

## 文件與模組的獨立統計

本次正式 docs 的 metadata 圖有 62 個節點、183 條 `requires`／`derives_from` 依賴，最長鏈 24；另有 30 條 `related` 關係不進入依賴圖。metadata 覆蓋來源基準 commit 所追蹤頂層 docs 的 62／326，約 19.0%，不代表命題覆蓋率；分母由該 commit 的樹取得，不受新報告加入 index 影響。

Lean 排除 Audit／Generated 後有 69 個模組、76 條內部 import 邊、最長鏈 15，以及 872 個來源 theorem 宣告。另列 Generated 三檔共 543 個 theorem、Audit 三十二檔。872 包含 helpers 與有限證明，研究級命題由本次盤點另行分組。前輪粗掃的 871 已修正：`AttachmentBlock.stp_self` 的同列 attribute 曾被 greedy regex 漏計。

文件引用、模組匯入與這次選入命題圖是三份獨立統計。高直接使用者數可以指出值得核對的來源，仍需對回命題適用前提；零使用者不排除紙面引用或未盤點 consumers。

## 可重跑資料與驗證範圍

人工核對的輸入：[No-mixed](../artifacts/c5_research_complexity/inputs/no_mixed.json)、[CommonRepair](../artifacts/c5_research_complexity/inputs/common_repair.json)、[N45](../artifacts/c5_research_complexity/inputs/n45.json)。[統計器](../scripts/c5_research_complexity.py)採標準函式庫，檢查來源引句與 SHA、ID／分組、局部依賴無環、十五側型覆蓋及 W／C 展開算術。生成的 HTML 離線可開啟，不需要外部服務。

```bash
python3 scripts/c5_research_complexity.py
python3 scripts/c5_research_complexity.py --check
PYTHONHASHSEED=17 python3 scripts/c5_research_complexity.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

第一條只更新本試點的 JSON／CSV／HTML；`--check` 唯讀比對產物。來源檔與自動掃描仍讀取 checkout 並保存 SHA，只有來源基準與文件覆蓋分母固定，因此來源改變仍會使舊產物比對失敗。驗證結果見[收據](../artifacts/c5_research_complexity/checks/verification.json)，其中 Git 發布欄是收據建立時的狀態；即時發布狀態以 Git 為準。這些檢查不重跑研究枚舉、來源數學 checker、Lean build 或公理稽核，不產生新的來源圖、拓撲證明或一般出口結論。

後續可先把 N45 的完整接合／恢復整理成單一共同接口規格，再逐身份列明已提供的接入證據；一般 target r-fibre 非空仍作另一個明確的新定理問題。
