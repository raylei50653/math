此整合分支納入 C5／完整 Sigma 固定來源研究的部分排除成果、有限證書、文件及獨立稽核。
U1 在明列 full Sigma933/941、epsilon=2、critical disk 與同來源前提下排除 no-mixed adjacent
two-root (4,4) 情形；M2 獨立核對 344 核心、3,498 接回、34,980 接回列查詢，target hit 為 0。
U2–U4、其他殘留 core／例外、E5 新證明、三列推廣、epsilon>=3 及一般出口仍保留。
有限兼容／未觸發控制不提升為來源構造、搜尋完備性或一般定理；紙面論證保留上游分類及
NetworkX／拓撲信任，未新增 U1 Lean 定理。

最終受驗 head：`1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf`。
本地驗收基準：`2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`；實際 PR base 以即時 PR 為準。
M4-L 納入 573 檔／26,469,605 bytes，原 M2／M3／監督 328 檔及 manifests 零漂移。
相對本地 main 基準，整分支差異 1,618 檔、+1,985,529／−70；不是只有末次 commit。
完整依賴、來源及驗證資料由 docs/STATUS.md、docs/c5_kempe_guide.md 與
audits/2026-10-07-m4-local/REPORT.md 導覽。

驗證與界線：

- M3 原 29 指定命令為 28 PASS／1 FAIL；另外四項 strict provenance FAIL，共五項保留。
  差異限 C44 兩個來源 presence/metadata leaves、E3 REPORT metadata、E4C guide hash、
  E5 branches 文件 hash；完整其餘 JSON payload 相同，不宣稱全 strict PASS。
- 最終 SHA 的獨立 checkout：文件／anchors/index、manifest、17 份 Python syntax、
  archive verify、155 產物狀態及預設 DocGraph 通過。
  原工作區保留 scratch，預設 DocGraph 的 62 duplicate-id 仍是 FAIL。
- Whitespace 原 86 項與匯入 immutable raw log 新增 85 項分列；新 authored 診斷 0。
  整分支 git diff --check 仍 exit2，原 vendor／logs bytes 未修改。
- 同 hash 的 109 份 Lean 來源／設定／生成證書沿用 M3 顯式 LC build；
  558 項公理 log 在 M4 與監督端重新解析相同，179 positive 無 native。
  本輪未重跑 build／Lean 公理程序；rejected/valid 與 raw Sigma cover 仍有 native 信任。
  預設 Lean CI 不代替顯式 LC 證據，未交付舊 .olean inventory。
- 原 M1 REPORT／candidate TSV 兩份追回；其餘原 M1 包及部分歷史暫存證據不可用。
  fresh Git blob 核對與 M3 同候選證據不冒稱缺失的原執行 logs。

遠端 CI 以本 PR 最新 final head 的實際 checks／run 為準；舊 SHA、空 checks 與本地驗證
不作遠端成功證據。合併待監督核對即時 head/base、CI、review 狀態並另行授權。


整分支範圍補充：

- K′ 對角 Kempe 轉運、E3–E6 的 ε=2 紙面化約與部分排除、E4C／D₈／D₉ 控制及稽核。
  K′ 仍保留 933／941 的 192／384 筆一致指派，未證來源排除；E3 唯一 degree-6
  全分支排除引用 D₈ 的 DG6-1 補表，雙 degree-5 與指定三列來源缺口仍保留。
- ES 與獨立 ER 的三型 k≤9 集合、計數及 Q 分布一致，共 179 個 critical orbits；
  k≥10 未搜尋，ER 依賴 plantri。LC 證明這 179 個具名 literal graphs 的 Lean soundness，
  未證搜尋 completeness 或拓撲 disk 定理。
- C44 保留 C44-AD3-row0-44 反例（完整 Σ=956）；它不反駁加完整 Σ=933／941 前提的窄命題。
  C44′ 保存 2,416 occurrences／213 literal cores 的相容篩結果，未構造目標來源或得到排除定理；
  C44″ 整理既有排除覆蓋，唯一 mixed 四份指定稽核與 U1 排除後，兩-root44 殘留仍為 U2–U4。

五份 strict FAIL 分別為 C44 input audit 的兩個來源 presence／metadata leaves、
E4 reductions 的 E3 REPORT bytes／hash、E5 controls 的同一 REPORT hash、
E4C 的 Kempe guide hash，以及 E5 branches 的 mixed_core_spokes 文件 hash。
各份完整 JSON 的其他 payload 全等，strict exit1 仍保留。

精確來源與停止點見 docs/c5_kempe_diagonal_transport.md、各 E3–E6 artifacts REPORT、
docs/c5_excess_two_finite_search.md、docs/c5_excess_two_independent_search.md、
docs/c5_excess_two_lean_certificates.md、C44／C44′／C44″ artifacts REPORT，
以及 audits/2026-10-07-c44pp-mixed-audit/REPORT.md。

發布時即時 remote main 與實際 PR base 均為 `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`，
未相對本地驗收基準前進。固定 final head 已正常 fast-forward push；本次不新增 commit。
