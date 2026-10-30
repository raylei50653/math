# math

研究如何逐步處理圖的著色限制，保留可行的組合，最後回填完整染色。
主目標是四色定理（4CT）：每個有限平面圖都能用四種顏色著色，使相鄰頂點異色。
目前從消元流程尋找平面結構帶來的規律；已有工具與尚缺的論證見[4CT導覽](docs/4ct_guide.md)。

## 研究入口

先由導覽理解問題、核心想法與成果之間的關係；精確定義、完整前提、證明與證據按需求查閱。

| 閱讀需求 | 入口 |
| --- | --- |
| 選擇研究線，查看進行中標記 | [研究線入口](docs/HANDOFF.md) |
| 理解目前主攻與已有成果如何銜接 | [4CT／精確消元與平面不變量](docs/4ct_guide.md) |
| 理解求解流程、消元與最後共同回填 | [四色工具導覽](docs/four_color_guide.md) |
| 查精確研究契約與第一個接續工作 | [消元研究契約](docs/4ct_guide.md#精確消元主線的研究契約) |
| 尋找特定報告、後續來源或歷史紀錄 | [完整文件索引](docs/STATUS.md) |

### 其他主題與查找入口

舊C5分類、換色與結構成果依研究問題選讀；各題結論、適用範圍與未解義務沿來源查閱。

| 想查的問題 | 入口 |
| --- | --- |
| C₅著色關係如何分類與查看 | [C₅組合與結構圖譜](docs/c5_combinatorial_atlas.md) |
| Weak-deletion具名分支的葉數與關閉事件 | [開放葉ledger](docs/c5_open_leaf_ledger.md) |
| 跨線成果有哪些關係與研究假設 | [研究綜合](docs/c5_research_synthesis.md) |
| 哪些共通引理可能連起不同分支 | [Phase B共通引理分析](docs/c5_phase_b_common_lemmas.md) |
| 兩點重疊時如何接合並修復關係 | [兩點重疊導覽](docs/c5_two_vertex_overlap_guide.md) |
| Degree-5來源與R系列如何組織 | [Degree-5導覽](docs/c5_degree5_guide.md) |
| 換色、重接與猜想E的研究入口 | [Kempe導覽](docs/c5_kempe_guide.md) |
| ε=2有限搜尋如何獨立核對 | [雙實作對照](docs/c5_excess_two_independent_search.md)、[Lean有限證書](docs/c5_excess_two_lean_certificates.md) |
| No-mixed各方法如何銜接 | [實驗總覽](docs/c5_no_mixed_span_budget.md) |
| 局部關係搬運需要哪些介面條件 | [搬運與介面驗證](docs/c5_no_mixed_hypothesis_audit.md) |
| No-mixed局部篩選如何運作 | [統一局部篩選](docs/c5_no_mixed_local_screen.md) |
| 無增長與有增長分支如何分離 | [無增長共同分離](docs/c5_no_mixed_no_growth.md)、[增長完備性](docs/c5_no_mixed_growth_completion.md) |
| Mixed容量與三接點介面如何處理 | [容量與介面](docs/c5_mixed_capacity_contacts.md) |
| Mixed三點弧的對稱與非對稱接線 | [對稱分支](docs/c5_mixed_p3_symmetric.md)、[非對稱分支](docs/c5_mixed_p3_asymmetric.md)、[中點／端點](docs/c5_mixed_p3_middle_endpoint.md) |
| 共鄰三點弧的雙扇區與後續來源 | [雙扇區](docs/c5_mixed_p3_common_endpoint.md)、[Weak-deletion導覽](docs/c5_weak_deletion_guide.md) |
| 具名單框點與雙框點如何接線 | [單框點三接點](docs/c5_mixed_p3_one_color_ternary_unary.md)、[雙框點三接點](docs/c5_mixed_p3_two_frame_ternary_unary.md)、[雙框點兩份unary](docs/c5_mixed_p3_two_frame_two_unary.md) |
| 原C5分類目標與最小來源的關係 | [研究目標](docs/c5_boundary_relations.md)、[度數界](docs/c5_saturation_degree_bound.md)、[C5→C4來源橋](docs/c5_c4_boundary_pivot.md)、[完整剝層](docs/c5_c8_peeling.md) |
| 不假設四色定理的原分類證明鏈 | [無4CT前提路線](docs/tasks/c5_no4ct_handoff.md) |
| 文件如何分工、更新與驗證 | [文件維護規則](docs/DOCUMENTATION.md) |

各輪研究與發布詳情由[歷史入口](docs/STATUS.md#歷史紀錄與舊連結)查閱。
歷史artifacts、完整relations／空fibres／witnesses及所有hash失敗保留。
新checkout先執行 `python3 tools/audit_archive.py restore --artifacts`，還原凍結快照及完整
稽核輸出；原SHA256、歷史失敗與replay命令見[封存還原說明](audits/README.md)。

Lean 4 + mathlib 專案。工具鏈版本由 `lean-toolchain` 鎖定，目前對齊 mathlib `v4.34.0-rc2`。

## 本機需求

- `elan`（已裝在 `~/.elan`；zsh 的 PATH 已寫入 `~/.zshrc`）
- VS Code + [Lean 4](https://marketplace.visualstudio.com/items?itemName=leanprover.lean4) 擴充

新開一個終端機，或先：

```bash
source ~/.zshrc
```

確認：

```bash
lean --version
lake --version
```

## 日常指令

第一次（或更新 mathlib 之後）拉編譯快取，避免從零編 mathlib：

```bash
lake exe cache get
```

編譯這個專案：

```bash
lake build
```

只有刻意升級依賴時才執行以下指令；一般接手沿用 `lean-toolchain` 與
`lake-manifest.json` 的鎖定版本：

```bash
lake update
lake exe cache get
```

## Lean CI

[`Lean CI`](.github/workflows/lean_action_ci.yml) 在 push、PR 或手動觸發時，
使用 GitHub 雲端 Ubuntu 24.04 runner 執行 `lake build --no-ansi`。
Lean 工具鏈按 `lean-toolchain` 快取；`leanprover/lean-action` 下載 Mathlib 編譯快取，
並快取 `.lake`（依賴及專案編譯產物）。`.lake` 快取依 OS、架構、工具鏈、
`lake-manifest.json` 與 commit 區分，同依賴的後續提交可沿用前次產物。
首次執行或快取失效時會下載及重建；每次仍執行 Lake 的建置檢查。
建置範圍為預設 `Math` target；未匯入 `Math.lean` 的獨立證書仍須顯式建置。
執行紀錄見 [GitHub Actions](https://github.com/raylei50653/math/actions/workflows/lean_action_ci.yml)。

## Python 產生器與大型 artifacts

[四色染色實驗與約束傳播](docs/four_color_guide.md)提供求解器、有限比較及逐步播放器。
執行 `python3 scripts/four_color_lab.py demo`，再開啟 `artifacts/four_color_lab/index.html`；
`constraint-demo`、`c5-demo`、`conflict-demo` 展示完整關係消元／回填、五環與已知衝突。
自己的圖可用 `python3 scripts/four_color_lab.py solve graph.json --engine constraints --intersections --cycles --cycle-contexts`，
保留共同接口與原環條件，最後倒序回填；適用範圍及未解保證見導覽。
加上 `--joint-constraints` 可自動辨識已登記的九點構型，在消元前加入三點等色必要關係；
完整前提、全部解保留核對及搜尋上限見[自動找型與主傳播](docs/four_color_joint_propagation.md)。
[三角化逐面編號展示](docs/triangle_structure.md)另保存六份嵌入、原點／邊／面身份與有限染色核對。

`scripts/` 的第三方依賴鎖在 `requirements.txt`（Python 3.14）。1 MB 以上的產生檔
（JSON、JSONL、bin）不進 git，只在 [`artifacts/MANIFEST.json`](artifacts/MANIFEST.json) 記錄
sha256、大小與產生器；這些檔案列在 `.gitignore` 的自動產生區塊。新 clone 之後重建並逐位元組驗證：

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py rebuild
uv run --with-requirements requirements.txt python tools/artifacts.py status
```

`rebuild --all` 會重跑全部產生器並檢查輸出與紀錄相同；刻意改動產生器後，用
`tools/artifacts.py record <path>` 接受新輸出，不帶路徑則重新掃描 `artifacts/`、登錄新的大檔。
無法再由產生器逐位元組重現、但仍被下游重播的大檔列在工具的 `FROZEN`，留在 git
（目前只有 `artifacts/c5_single_spoke_two_two/observations.json`）。

[`Generated artifacts` CI](.github/workflows/generated-artifacts.yml) 在每次 push／PR 檢查
Git index，並以 Python 3.14 安裝 `requirements.txt` 後執行 `tools/tests/`：
整個 repo 的 JSON、JSONL、NDJSON、JSON5、bin 達 1,000,000 bytes 時，
預設由腳本生成，不直接追蹤輸出。MANIFEST 所列的產物必須有已追蹤的產生器，
並列入 repo 的 `.gitignore`；已追蹤的大檔不會因為新增 ignore 規則而通過。
一般大型 `artifacts/` 先驗證產生器，再用 `record <path>` 登錄，最後
`git rm --cached -- <path>` 移除追蹤並保留本地檔案。

需要保存原始 hash、失敗紀錄或交付 seal 的歷史稽核資料，以
`python3 tools/audit_archive.py append --paths audits/<path> ...` 選定封存，
核對 gzip 的還原 bytes 後再移除原檔追蹤；新 checkout 先按
[封存說明](audits/README.md)還原。不得以重生成覆寫歷史證據。
必須直接追蹤的大檔在 [逐檔例外表](tools/generated_artifact_exceptions.json) 說明理由：
frozen 證書鎖定大小與 SHA256，bootstrap metadata 指明產生器。目前只保留上述
FROZEN 證書與 `audits/ARCHIVE.json` 主還原索引兩項例外。

本機先 stage 本次變更，再執行與 CI 相同的檢查：

```bash
python3 tools/check_generated_artifacts.py
uv run --python 3.14 --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
```

此 CI 核對儲存規則及產生器登錄，不會執行整批生成。實際重建由
`rebuild --all` 驗證主要產物的 SHA256／大小；單支腳本亦可用其 `--check`。
產生器需要額外 CLI 參數或排他建立的小型伴隨檔時，在 `tools/artifacts.py` 的
`PRODUCER_ARGS`／`ADDITIONAL_OUTPUTS` 明列。伴隨檔對照本次重建前的 bytes，
不代表已核對歷史登錄 hash；`status`／預設 `rebuild` 亦不完整檢查伴隨檔。
`status` 的 `ok` 只表示主要產物與 fingerprint 相符，不能代替實際生成通過。

[2026-10-12 實際生成紀錄](audits/2026-10-12-generated-artifact-ci/REPORT.md)：
隔離 checkout 整批跑過，再針對生成方式修補後重試；目前137／160支產生器、
143／166份主要產物重建 bytes 一致，其餘保留失敗與依賴阻擋。
此次亦掃描本地 `artifacts/`，補登錄先前僅忽略的 split-hub probe 並實際重建；
儲存 CI 不會發現新 checkout 中不存在的未登錄、未追蹤輸出。

未涵蓋的新大型產物，先補明確產生器、完整參數與輸出集合，再實際重建比較，
通過後才登錄與移除追蹤。若輸出不一致，保存原 bytes 與逐輪紀錄，阻擋下游，
不以 `record` 自動接受新結果；需要固定保存的歷史證據走上述封存／逐檔例外。
小檔、其他副檔名、未追蹤或已忽略但未登錄的輸出不在這個 CI 的完整驗證範圍。

## 檔案

| 路徑 | 用途 |
| --- | --- |
| `Math/Basic.lean` | Lean 起始例子；研究入口見 HANDOFF |
| `Math/ColorDFA.lean`, `Math/GeometryDFA.lean` | triangle grammar 的染色／幾何自動機與 Lean 證明 |
| `scripts/triangle_automata.py`, `artifacts/automata/` | 自動機資料的產生器與決定性輸出 |
| `Math/BoundaryRelations.lean`, `Math/C5PairForcing.lean` | 泛型完整 boundary relation 與同一 C5 的投影／條件強迫 |
| `scripts/c5_relation_library.py`, `artifacts/boundary_relations/` | 87 個完整 states、派生 pair 查詢與最小條件規則 |
| `Math/C5Counts.lean`, `Math/C5ParityWord.lean`, `Math/NearTriangulation.lean` | C5 延伸計數恆等式、XOR 邊字四對一、polygon 補完二分法與 Euler 計數；審計 `Math/C5CountsAudit.lean` |
| `Math/KempeSurgery.lean` | 一次 Kempe swap 的六色對精確更新（AC／BD 不動、混合色對＝retained graph＋stars）與「刪 cut、收縮 components、加邊」的連通分量一一對應；審計 `Math/KempeSurgeryAudit.lean` |
| `Math/ForcingLists.lean` | block 報告反覆使用的 forcing-list 基礎引理：bridge 兩側同色 singleton 強迫、forcer 的 c/D swap 對稱（c-forcer 必碰 c 色 boundary）、incident palettes 互異且恰覆蓋 list、兩色 list 環不可著色 iff 奇環且 lists 全同（含 `C5`、triangle、`P=Q=四色\R` 介面、apex 36-case 規則）；審計 `Math/ForcingListsAudit.lean` |
| `Math/RootInterfaces.lean` | 多接點共同關係／禁色、中心 `A \ ⋃ F` 接合、共用 root 交集、單步路徑訊息與 private 色計數；15 個普通 Lean 定理，見 [說明](docs/lean_root_interfaces.md) 及 `Math/RootInterfacesAudit.lean` |
| `Math/TwoRejectionTools.lean` | 雙拒絕證明的九個一般引理；[依賴與重播](docs/lean_two_rejection_tools.md)，審計 `Math/TwoRejectionToolsAudit.lean`；完整 disk 分類仍未形式化 |
| `Math/BoundaryDegree.lean` | 實際邊界接線到 degree-list 緊性、框色單射及延拓準則；[前提與重播](docs/lean_boundary_degree.md)，審計 `Math/BoundaryDegreeAudit.lean` |
| `Math/CommonRepair.lean` | 完整 relation 的 W／C 充要判準、全部極小 repairs、唯一最少解及退化支；[前提與重播](docs/lean_common_repair.md)，審計 `Math/CommonRepairAudit.lean` |
| `Math/SealedFourPort.lean` | D₁₃／四輪星完整具名四接點等價及密封上下文替換；[前提與重播](docs/lean_sealed_four_port.md)，審計 `Math/SealedFourPortAudit.lean`；不含 disk 嵌入 |
| `Math/NamedRepairCore.lean`, `Math/NamedRepair.lean` | 兩個具名十五點核心的 J/P、W／C、完整極小 repairs 及 r*=4；[前提與重播](docs/lean_named_repair.md)，審計 `Math/NamedRepairAudit.lean`；指定框的 disk 完備性另證 |
| `Math/NamedRepairReplacement.lean` | 兩核心 A／B 單側及雙側各一次 D₁₃ 替換，保完整外部關係、原 U 的 J／指定 P 與 repair 分類；[範圍與重播](docs/lean_named_replacement.md)，審計 `Math/NamedRepairReplacementAudit.lean`；任意層數與 disk 框另證 |
| `Math.lean` | 函式庫根，`import` 子模組 |
| `lakefile.toml` | 依賴（mathlib）與編譯選項 |
| `lean-toolchain` | 這個專案用的 Lean 版本 |

開 `Math/Basic.lean` 後，右邊 infoview 會顯示目標與型別。把游標放在 `by` 後面即可逐步看 tactic 狀態。

## 授權與引用

本 repository 以 **Apache License 2.0** 釋出，全文見 [`LICENSE`](LICENSE)；授權涵蓋整個 repo：Lean 證明（`Math/`、`Math.lean`）、產生器（`scripts/`）、文件（`docs/`）與決定性輸出（`artifacts/`）。`lakefile.toml` 亦宣告 `license = "Apache-2.0"`、`licenseFiles = ["LICENSE"]`。

引用資訊見 [`CITATION.cff`](CITATION.cff)；GitHub 頁面右上角 "Cite this repository" 會依它產生 APA／BibTeX：

```bibtex
@software{lei_boundary_colouring_math,
  author  = {Lei, Yue-Hui},
  title   = {Lean 4 formalization of boundary-colouring structure and triangle disk-gadget synthesis for the four-colour problem},
  version = {0.1.0},
  year    = {2026},
  url     = {https://github.com/raylei50653/math},
  license = {Apache-2.0}
}
```
