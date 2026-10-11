# math

C5 boundary-coloring relation、有限證書與 Lean 形式化研究。
**主命題 `K∞=K≤5` 仍未證。**

## 研究入口

| 文件 | 用途 |
| --- | --- |
| [研究線入口](docs/HANDOFF.md) | 新對話先讀；選擇研究線導覽，進行中以 tag 標記 |
| [完整文件索引](docs/STATUS.md) | 查找專題報告、短狀態、後續關係與歷史 |
| [Weak-deletion 開放葉 ledger](docs/c5_open_leaf_ledger.md) | 共鄰 P₃ 固定具名目錄的葉數、關閉事件、階段趨勢與每日觀測入口 |
| [C₅ 全線進展與高階假設](docs/c5_research_synthesis.md) | 跨線成果、同源關係／臨界預算／幾何框架、三個可反駁假設及階數初驗 |
| [Phase B 共通引理候選分析](docs/c5_phase_b_common_lemmas.md) | U1–U4／Weak-deletion、Excess／Mixed／No-mixed、Relation／Repair／State 的精確候選、前提、反例、證明義務與分支效益；條件容量推廣與小型重播 |
| [C₅ class 兩點重疊](docs/c5_two_vertex_overlap_guide.md) | 具名八點接合、拓撲、混合外框與關係修復；現況、停止點及重播入口 |
| [Degree-5／R 系列](docs/c5_degree5_guide.md) | 二連通單缺額定理已完成紙面查證；45／54 的適用性須核實際 core 前提，R31／一般三環及完整來源分類保留 |
| [933／941 excess 與接手入口](docs/c5_kempe_guide.md) | 共同 ε≥2；E3 在三列拒絕前提下排除唯一 degree-6，須連同 D₈ 補表引用。E4／E6 證非相鄰／相鄰 mixed 分量數 m≤2，雙 degree-5 的其餘殘留保留；ε≥3 未證 |
| [ε=2 有限搜尋與雙實作對照](docs/c5_excess_two_independent_search.md) | ES／ER 三種 root 型 k≤9 的 q／critical orbit 集合逐層一致，共179個 critical orbits，無猜想 E 反例；[LC](docs/c5_excess_two_lean_certificates.md) 提供179／179個 Lean soundness 證書，有限完整性與任意大小定理分開 |
| [No-mixed 實驗總覽](docs/c5_no_mixed_span_budget.md) | 十五類證據總表、共同跨度結構及推廣界線 |
| [No-mixed 搬運與介面驗證](docs/c5_no_mixed_hypothesis_audit.md) | 逐 root 不可搬運界、精確接合介面與守恆禁色的證據界線 |
| [No-mixed 統一局部篩選](docs/c5_no_mixed_local_screen.md) | 禁色增長、守恆／非守恆規則與仍依必要表的共同接合 |
| [No-mixed 無增長共同分離](docs/c5_no_mixed_no_growth.md) | 短側弧與色交換不變性的紙面證明、checker 及證據界線 |
| [No-mixed 增長完備性與共同分離](docs/c5_no_mixed_growth_completion.md) | 三個側弧位置的固定框弧配方、免查支援表的存在性證明與重播 |
| [Mixed 容量與三點介面](docs/c5_mixed_capacity_contacts.md) | 逐欄容量、十八側型、各一 incidence 的完整關係界與最小三點控制 |
| [Mixed P₃ 對稱分支](docs/c5_mixed_p3_symmetric.md) | 原五環空內側、完整側支援與五跨度來源排除；不需 T4／Gallai |
| [Mixed P₃ 非對稱分支](docs/c5_mixed_p3_asymmetric.md) | 容許一色側零跨度的六跨度排除，完成兩端各一 root 接線；紙面證明與固定域重播 |
| [Mixed P₃ 中點／端點接線](docs/c5_mixed_p3_middle_endpoint.md) | 保留原末端附件的四區塊證明、完整關係與固定域重播 |
| [Mixed 共鄰 P₃ 的雙扇區](docs/c5_mixed_p3_common_endpoint.md) | 原必要表及 rotation 控制保存；後續 C-W／D₆ 完成 C §1 前提下整個分支的來源排除，固定3500-key ledger 已為0；現況見 weak-deletion 導覽 |
| [共鄰 P₃ 單框點三接點 unary](docs/c5_mixed_p3_one_color_ternary_unary.md) | 固定 C₂ 身份的原 triangle 化約、外路 K₅ 來源排除及完整 witnesses |
| [共鄰 P₃ 雙框點三接點 unary](docs/c5_mixed_p3_two_frame_ternary_unary.md) | 固定 C₃ 身份的新非接點葉 K₅、原 bridges／完整 tuples 控制與葉數證明 |
| [共鄰 P₃ 雙框點兩份 unary](docs/c5_mixed_p3_two_frame_two_unary.md) | 固定 C₄ join60 的逐份完整 relation 排除、九份自身支援配置及原 bridges 控制 |
| [研究目標](docs/c5_boundary_relations.md) | 主命題、最小反例路線與局部壓縮的區別 |
| [文件治理與工作約定](docs/DOCUMENTATION.md) | 文件分工、信任界線、更新及驗證流程 |

項目現況、精確停止點與重播入口由各研究線導覽維護；完整論證與證書見原報告。
ε=2 的E3–E6與C44″覆蓋表、精確前提及保留缺口由[Kempe導覽](docs/c5_kempe_guide.md#3-停止點與保留缺口)維護；
共鄰P₃的C-W／D₆結論及後續接線由[weak-deletion導覽](docs/c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)維護。
U2–U4及M4／M5證據的整批重播與發布範圍見[2026-10-08紀錄](docs/history/2026-10-08-core44-batch-publish.md)。
前序K′／E3–E6整合見[2026-10-04紀錄](docs/history/2026-10-04-kprime-excess-two-progress-publish.md)。

前序A₄／B₄／C₄的固定快照、獨立驗收與scope ledger見[D₅](audits/2026-10-04-task-d5/REPORT.md)；
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

## Python 產生器與大型 artifacts

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
