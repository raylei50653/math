# 2026-10-09：Issue #4 文件分工與收尾核對試點

依據 [Issue #4](https://github.com/raylei50653/math/issues/4)，基準
`main @ 3f2731b7225d35e12872177eb00d3a5b24aa6468`，加上接手時已存在的
Phase B 未提交內容。本紀錄保存 D1–D5 的文件設計、演練與回饋，不是 live-fact
registry，也不裁決新數學命題。治理契約由 [DOCUMENTATION](../DOCUMENTATION.md)
維護；研究現況仍由各 guide 與權威來源維護。

## D1：兩條活躍研究線的唯讀盤點

兩線均由 [HANDOFF](../HANDOFF.md)標記進行中。抽樣閱讀下列路徑，
沒有使用 Graphify，也沒有要求全歷史補 metadata。

| 責任 | Weak-deletion／共鄰端點 P₃ | Kempe／固定完整 Σ 的兩-root44 |
| --- | --- | --- |
| Routing | HANDOFF → [weak-deletion guide](../c5_weak_deletion_guide.md)；STATUS 直接索引 | HANDOFF → [Kempe guide](../c5_kempe_guide.md)；STATUS 直接索引 |
| Summary | guide 的目的、現況表、§3 停止點／保留義務 | guide §3 的兩-root44 收尾與 45／54 等 OPEN 義務 |
| Source | [C-W](../c5_qcore_shield_budget.md) §1、§4–5、§8；由 §8 導向 D₆ 補證 | [C44″](../../artifacts/c5_excess_two_c44pp/REPORT.md)的逐格前提／前序入口，加 guide §3 連向 U1–U4 互補原報告 |
| Evidence | C-W checker／verdicts、[D₆](../../audits/2026-10-04-task-d6/REPORT.md)、[cw-v1 ledger](../c5_open_leaf_ledger.md) | 各 U 報告的 scripts／artifacts／獨立 auditor；[U4 §5](../c5_excess_two_nonadjacent_two_mixed_core44.md#5-證書實際控制與信任界線)明列紙面／Python／Lean 界線 |
| History | C₂–C₄、W、D₃–D₆ 原截點與發布紀錄 | C44″ 當輪覆蓋表與 U1–U4 各輪紀錄；不把當年的 OPEN 當作現況 |

**實際漏失。** 接手的 weak-deletion guide 是 287 行，頁首先稱「3497 葉未關閉」，
再接 W 的完成公告；現況表仍稱共鄰 P₃「36 residual、未證出口」，§3 又先給
geometry35 待辦、後面才說被取代；§4 仍以「另外3497keys未關閉」開場。
來源 [C-W §8](../c5_qcore_shield_budget.md#8-稽核後更正與補證2026-10-04d₆-之後)
及 cw-v1 已確認該指定分支完成排除。錯誤是當前 Summary 保留舊待辦，
不是原必要表必須被刪除。一般出口仍 OPEN，不能把來源排除改稱一般出口證明。

**重複權威風險。** Kempe guide 有 361 行，§3 在已返回任務表、停止點與後續
段落多次列 U1–U4 細節；README、STATUS 與跨線表又重述部分數字。這些短索引／
跨線比較仍有用途，但容易變成多份手動維護的長版現況。本輪只縮短與 P₃ 試點
直接相關的 STATUS 條目；Kempe 未整頁重構，避免與已存在的 Phase B 變更混合。

**合理分散。** U3 分兩報告、C-W 與 D₆ 各負責正 unary／零-unary 的論證，
紙面化約與固定域控制也有不同信任範圍；應由一個來源入口連接，不強行合檔。

**DocGraph 缺口。** 正式 docs 的 metadata 圖有 62 documents、213 relations；
兩條 guide、C-W、U4 都沒有 ID，所以不存在可供查詢的 metadata 反向邊。
這不是「沒有 consumer」。普通 Markdown 引用搜尋仍能定位相關入口；
不能把導航父子、文件引用或 metadata dependency 當成數學蘊涵。

## D2：最小契約落地

在 DOCUMENTATION 保留每次實質研究更新的觸發，明列 L0 Source／Evidence、
L1 所屬 guide 子節／STATUS 對應條目、真正 closure／supersession 或 invalidation
的 L2，以及有實際上層影響才展開的 L3。每輪完成前履行，觸發不等於必須有 diff。
純重播、工具 PASS、PR merge 不自動觸發收尾；已採納結論失效立即核對上游。
短收尾紀錄用現有 History／已授權 PR，沒有新 schema、狀態資料庫、checker 或 CI gate。

## D3：共鄰 P₃ 的漸進披露示範

| 閱讀需求 | 接手版本 | 本輪候選入口 |
| --- | --- | --- |
| 目的與現況 | guide 先呈現多輪截點，再找後續公告 | guide §1 交代一般出口目標；§2、§3 直接給當前已完成／OPEN 範圍 |
| 精確命題與必要前提 | §3 長段重述原來源，需讀到後段才發現待辦被取代 | §3 共鄰端點 P₃ 子題明列 C §1 的圖類、q、root／附件身份及不需 T4 |
| 推論覆蓋 | C₂→C₃→C₄→W→D₆ 分散在同頁敘事 | 一個 C-W 權威來源入口：§4–5 ＋ §8／D₆；說明零-unary 不能由目錄歸零代替 |
| Source／Evidence | 多輪 replay 和 hash 敘事混在現況 | §4 提供當前只讀 checker 與原報告／稽核／歷史入口 |
| 下一個窄問題 | geometry35 先稱待辦，後稱被取代 | 檢查其餘分支的三份不同原 one-sided pieces；缺外路／root-disconnected 時停止推廣 |

導覽由 287 行減為 164 行，保留原 §1–§4／工具子節錨點及原報告、稽核、歷史
路徑。沒有刪原 mathematical evidence；移出的重複推導與逐輪 replay 由既有原報告
承擔，沒有另建一份相同敘事。Phase B 接續段落原文保留。
這是文件結構與語義逐項審閱，沒有聲稱做過讀者實驗或量測閱讀時間。

不能安全省略的條件包括 q-critical 與 Σ-critical 的差別、原完整 degree、
one-sided、每份自身支援／避開自身外路、零-unary 的補證，以及任意大小紙面
化約與有限 key 證書的區別。Summary 保留短邊界，精確論證仍對回 Source。

## D4：局部更新、真收尾與負控制

隔離輸入保存在 [fixtures.json](../../artifacts/docs_issue4_pilot/fixtures.json)，
含 8 個固定演練 case、5 份原輸入 SHA256、實際來源摘錄與明示的注入文字。
它是一次性歷史試點資料，不是未來要同步的狀態總帳。
先核對 5 個輸入 hash，再把個別 case 寫入系統暫存目錄審閱；研究原檔不注入錯誤。

### 一般局部更新的範圍試點

F1 以接手時已存在的 Phase B B-C2 紙面條件容量式作局部更新演練，對回
[Phase B §3.2](../c5_phase_b_common_lemmas.md#32-b-c2任意两自由roots的條件逐欄容量定理)：
同一 proper boundary row、其他 roots 的共同 pins、兩自由 roots、完整 tuples，
拒絕完整接合且另一側非空。這是必要容量式，沒有新增 target／來源排除。
Evidence 核對既有 controls 的入口與限制：只計算相鄰兩 roots、唯一 shared
incidence11 mixed，沒有有限計算覆蓋 χ=0、多 mixed／更多 roots；紙面式的
一般性另由論證承擔。本輪未重跑數學控制。

在隔離副本中，L0 source 由空項加入該既有陳述；L1 topic 加入原接續段落、
index 加入對應短條目。實測只有 `source.txt`、`topic.txt`、`index.txt` 改變；
README、HANDOFF、synthesis、common-language 四份副本 byte hash 相同。
這驗證該局部事件的 L0／L1 有核對、父義務未變時不強制 L2／L3 diff。
接手時 Phase B 整包另外新增跨線 Routing 的 diff 原樣保留；本演練不把那些
已有路由改動冒充本輪「只改 L0／L1」的證據。

### 真收尾的 scope 與反向候選

F2 的 closure scope 是 C44″ 所列：有限簡單有序 induced-C₅ disk、完整 Σ933／941
或整圖 D₅ 像、逐非框邊 Σ-critical、ε=2、原兩 degree-5 roots／其餘有效內點
完整 degree 四；拒絕列的 minimal core 保留兩原 roots 且 core degree=(4,4)。
各格保留原 contacts、attachments、bridges、共同色框及來源前提。
完成依據是任意大小紙面化約與互補分類／接回證據，不是有限搜尋沒找到來源。

權威入口是 [C44″](../../artifacts/c5_excess_two_c44pp/REPORT.md)與
[Kempe §3](../c5_kempe_guide.md#3-停止點與保留缺口)的來源映射：
[U1](../c5_excess_two_no_mixed_core44.md)、
[U2](../c5_excess_two_adjacent_two_mixed_core44.md)、
[U3 incidence11](../c5_excess_two_nonadjacent_one_mixed_core44.md)、
[U3 incidence12／21](../c5_excess_two_nonadjacent_mixed12_core44.md)（22 沿用 E4）、
[U4](../c5_excess_two_nonadjacent_two_mixed_core44.md)，及前序相鄰唯一 mixed 排除。
Sources 各自連 scripts／artifacts；紙面、Python、指定稽核與 Lean 界線分開。

在 `docs/*.md`／README 搜尋這五份 U 報告與 C44″ 的直接 Markdown 引用，
得到 8 份候選：五份 U 報告本身、Kempe、common-language、STATUS。
另核對已知跨線 consumer synthesis 與 Phase B；這些間接／語義 consumers
不能靠直接檔名搜尋保證完整。以下是本次抽樣的語義核對，非全 repo 證明依賴稽核。

| 受影響責任 | 結果與理由 |
| --- | --- |
| 直接父主題 Kempe §3 | Reviewed-unchanged：已明列兩-root44 完成，45／54／55、單-root與無44來源仍 OPEN |
| C44″ 與五份 U sources | Reviewed-unchanged：頁首已有後續涵蓋／閉合關係；保留各輪的原覆蓋表與 evidence |
| common-language 的兩-root44 行 | Reviewed-unchanged：結論限固定完整 Σ／ε=2／逐格前提，仍列非44／E5義務 |
| STATUS 的 C44／U 條目 | Reviewed-unchanged：短索引已指出後續閉合與有限控制界線 |
| synthesis 首段及 Phase B | Reviewed-unchanged：已區分有界收尾與父題未解；歷史快照不覆寫 |
| 上層 Routing | 不要求研究語義更新：父主題仍 OPEN、研究線／活躍狀態未變，L2 影響評估到此停止 |

本輪真實漏失的 P₃ Summary 則標為 **Updated**：weak-deletion 頁首、現況、§3、§4
及 STATUS 對應條目對回 C-W／D₆；已知跨線 common-language、synthesis、README
原本已採納該有界閉合，Reviewed-unchanged。HANDOFF 只有路由，byte hash 保持。

### 隔離負控制的語義審閱

| Case | 觀察輸入 | 審閱判定與動作 |
| --- | --- | --- |
| F2 | 真實 sources 已閉合，父摘要同範圍也已閉合 | Reviewed-unchanged；父 ε≥3／一般出口仍 OPEN，停止傳播 |
| F3 | 注入父摘要「同一固定完整 Σ／ε=2 的兩-root44 仍 OPEN，U2–U4 未排除」 | 發現漏同步：同 scope 下與 U2–U4 及前序完整覆蓋矛盾；該父子節必須更新，其他 OPEN 義務保留 |
| F4 | 注入父摘要「所有 disk 已證 ε≥3／一般共同出口／K∞=K≤5」 | 發現強化宣稱：只排有兩-root44 core 的來源不等於排所有 ε=2 來源；撤回該上層宣稱並立即核對 consumers |
| F5 | B-C2 局部容量進展、controls PASS，45／54 未解 | 保持 OPEN：必要等式未提供跨列或 source 排除證明，不以 PASS 觸發父題 closure |
| F6 | 注入「已採納所有 T4 圖的 one-sided mixed 都有長盾弧」；提供 S935/P0 | 即時 invalidation：盾弧34只有一邊，推廣 consumer 必須撤回並核對直接使用者；Σ935 不反駁固定933／941的原猜想 |
| F7 | 相同內容的純重播／PR merge，沒有新研究事實 | 只記驗證／發布，不能產生新 closure，也不要求上游 diff |
| F8 | C44″ 2026-10-06 表仍寫四類未覆蓋，頁首有 2026-10-08 閉合公告 | 保留歷史：帶日期的舊 OPEN 並非目前父摘要漏同步，不能改寫原表 |

F3 同時注入完整 Kempe guide 的一段現況：其 **5 個錨點、168 個 Markdown
連結保持相同**，仍出現同 scope 的語義矛盾。這證明連結／錨點通過不能
代替收尾 review。F3–F6 的判定由 Agent 對照來源、量詞與範圍作出，
沒有宣稱既有 check_docs 或 DocGraph 可自動判 CLOSED；也沒有新增語義引擎。
F6 是注入的錯誤採納範例，不宣稱實際專案已採納過那個過強命題。

重新審閱時可用標準函式庫讀 `fixtures.json`，核對 `metadata.input_hashes`，
將各 case 的 `source_excerpt`／`parent_excerpt` 寫入新的 TemporaryDirectory，
逐項比對上表的圖類、前提、結論與 Remaining OPEN。F1 的 before／after
也已留在 fixture；不需覆寫工作樹或啟動研究生成器。

## D5：回饋取捨與維護交接

| 觀察問題 → 候選改動 | 需求影響／證據與取捨 | 決策 |
| --- | --- | --- |
| 當前 guide 混入舊待辦 → 短現況＋C-W 權威入口＋Evidence 表 | 287→164 行且實際漏失已修；保留精確前提、補證與原路徑 | 採納本子題示範，不強制所有 guide 同一模板 |
| 每輪上層同步成本 → L0／L1 常態核對、L2／L3 依語義觸發 | F1／F5／F7 保留局部流程，不把「每輪」改成「只有 closure 才維護」 | 採納最小契約 |
| 零 metadata 反向邊漏 consumer → Markdown 搜尋＋已知 consumers | 此次 8 份直接候選外仍需 synthesis／Phase B；不能保證全 repo 完備 | 採納組合查找，捨棄自動全覆蓋假設 |
| 五層機械 schema 可能碎片化 → 主題內自然子節與來源入口 | 不建一命題一檔、Proof DAG 或 live registry；C-W／D₆ 互補報告仍分開 | 採納有用段落，schema 保持可選 |
| 連結檢查看不到同 scope 的 stale OPEN → F3 語義負控制 | anchors／links 相同仍需 review；F4／F6 防強化與錯誤推廣 | 保留人工／Agent 判定，沒有大型 CI gate |

原 Issue 的 owner 約束、closure 語義與信任邊界均保留，沒有需求變更待裁決。
未整頁重構 Kempe、未全域去重 README／STATUS、未補全歷史 metadata；這些不影響
本次小幅試點驗收，也不宣稱全 repo 已消除現況漂移。後續研究每輪按契約局部
核對；真收尾留下短 impact 紀錄，沒有影響就在對應父層停止。

## 本輪檢查與交付界線

| 檢查 | 本輪結果 |
| --- | --- |
| `python3 scripts/check_docs.py` | PASS：585 Markdown、6977 local links；anchors／index／HANDOFF 通過 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | PASS：62 documents、213 relations、5 families，0 errors |
| `python3 tools/docgraph check` | 既有 FAIL：62 duplicate-ID errors，來源是保留的 `scratch/task-c44-delivery/repository/docs/`；修改前後完整診斷 byte 相同 |
| `git diff --check` 與兩份新檔 whitespace | PASS |
| 隔離試點輸入 | 5 份 source SHA256 一致；F1 只有 L0／L1 的三份文字副本改變，四份 Routing／跨線副本 byte 相同；F3 anchors／links 相同但語義矛盾被 review 指出 |
| 接手工作區保留 | 5896 份接手時 tracked／可見 untracked 檔案中，只有 DOCUMENTATION、weak-deletion guide、STATUS 改變，0 檔遺失；原 26 行未提交 diff 新增文字全部仍在 |

本輪新增只有本 History 與 `artifacts/docs_issue4_pilot/fixtures.json`；fixture SHA256
為 `bc44f3895a9393d5a1b435924661845dc27ebca5a4bba948285d5c553246f374`。
Phase B source／script／兩份 artifacts，以及 README、HANDOFF、common-language、
Kempe、state、two-vertex guides 共十份既有檔案 hash 未變。保留檢查的 hash 範圍
是 tracked／可見 untracked，沒有冒稱重驗所有 ignored 大檔；本輪不執行 evidence
生成器，未修改既有研究 scripts、artifacts、audits、Lean 或舊歷史。
未重跑研究枚舉、研究 checker 或 `lake build`；未新增數學定理／Lean 形式化。
未 commit、push、修改 GitHub Issue 或發送評論。接手的 Phase B 產物與 frozen
證據均保留；本紀錄只描述本輪文件工作，不取代原研究與發布紀錄。
