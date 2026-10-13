# Lean 形式化導覽

更新：2026-10-04。已整合 LC 的179個 ES 代表 soundness 證書；
具名 repair 普通證明及其他項目的證據範圍沿用各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

把研究中的可重用介面、list 前提、有限證書與數學定理接到具名 Lean theorem，
逐項記錄公理依賴。編譯成功不代表紙面 Gallai、minor 或 disk 論證已形式化。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 共同 repair 判準 | 27 個普通 theorem：W／C 雙向判準、極小修復／極大失敗、唯一最少解、退化支及具名投影介面；兩核心指定框前提由後續實例完成；其餘四圖與拓撲未形式化 | [CommonRepair](lean_common_repair.md) |
| D₁₃ 四接點與密封替換 | 22 個普通 theorem：原圖完整關係、三型構造延拓、全部外部染色保留及密封／缺邊控制；disk 與來源族未匯入 Lean；核心 repair 見下列實例 | [SealedFourPort](lean_sealed_four_port.md) |
| 具名來源 repair 實例 | 34 個普通 theorem：兩方向原35邊 J、指定兩框 P、完整 W／C、各15組極小 repairs、唯一最少對及 r*=4；disk 框完備性與替換來源族仍未形式化 | [NamedRepair](lean_named_repair.md) |
| ε=2 的具名來源 soundness（LC） | 179／179個 ES critical 代表：完整 Σ、逐邊 criticality、degree 型及 genus-0 rotation／框外面。正列與 witness 用 `decide +kernel`，拒絕列用 `native_decide`；558項 axioms audit 無 `sorryAx`。只證所列圖為真，不證枚舉完整性或拓撲 disk 定理；未接入 Math.lean | [LC 證書與公理範圍](c5_excess_two_lean_certificates.md) |
| Root 接合 | 15 個普通 Lean 定理與報告對照；不含完整 minor／disk 層 | [root 工具](lean_root_interfaces.md) |
| 雙拒絕共用工具 | 共用 list／接合引理已具名；完整紙面分類仍有形式化依賴 | [雙拒絕工具](lean_two_rejection_tools.md) |
| 實際接線與 degree-list 緊性 | 13 個普通定理：原圖延拓 iff、degree 拆分、拒絕迫緊等；lists 直接由原圖 attachments 定義 | [BoundaryDegree](lean_boundary_degree.md) |
| Grammar／端點次序 | 指定 triangle grammar 的語義、normal form 與端點編譯已有；embedding 抽取仍在紙面層 | [normal form](attachment_normal_form.md)、[topology](topology_completeness.md) |
| Completion／weak bisimulation | 同頂點 completion 有紙面證明；一般 bisimulation／finite traces 有假設式 Lean 定理，拓撲與生成器未形式化 | [completion](c5_completion_weak_bisimulation.md) |
| 枚舉／有限證書 | Cell 枚舉的 Lean 鏈及外部信任已明列；有限結果不能外推全部 disk | [enumerator](c5_cell_enumerator.md)、[phase 1](phase1.md) |
| 計數代數 | 部分代數形式化可用；不補足 cone／connectivity 或平面來源論證 | [count cone](c5_count_cone_bridge.md)、[Kempe 導覽](c5_kempe_guide.md) |

## 3. 停止點與保留缺口

LC 的固定179張證書已完成；`Math.GeneratedExcessTwoCertificates` 與
`Math.ExcessTwoCertificatesAudit` 為顯式 build targets，預設 Math.lean／CI 尚未匯入。
完整 raw Σ equality 另繼承既有 S₄ cover 的 native 公理，具名依賴見 LC 報告。
是否加入預設 build 的提議保留，首次編譯生成證書約需12分鐘。
ES／ER 的 k≤9 雙實作對照是 Python 有限完整性證據，LC 只提供 soundness；
Lean 的枚舉 completeness、軌道互異、拓撲實現及任意大小分類仍未形式化。

目前 reusable 基礎包含「實際圖 → 剩餘 lists → degree-list 前提 → 拒絕迫緊」，
以及「完整接受集合 → W／C 充要判準 → 全部 repair 模板與極小分類」。
另已接通「D₁₃ 原32邊 → 完整四接點等價 → 密封替換保留全部外部染色」；
此處外部共同色框與附件由同一 `attach`／`outside` 保留。
兩個十五點核心已接通「原圖 J → 指定兩框 P → 完整 W／C → repair 分類與 r*=4」。
下一個窄接口是將核心內 D₁₃ 替換的具名附件接到密封替換定理，
證替換圖在原 U 上的 J 與指定框 P 保持；任意層數的圖結構另行處理。
指定兩框恰為全部 disk 可用框、四個 P=J 圖的具體前提與來源族拓撲仍未形式化。
Gallai／degree-list 外部定理、完整紙面分類、來源 minors 與 disk topology
仍須分別補齊，不能以 BoundaryDegree 或有限 `native_decide` 證書代替。
其他研究線保留上述依賴。

## 4. 閱讀與重播入口

共同 repair 從[具名實例](lean_named_repair.md)進入，再回到[抽象判準](lean_common_repair.md)。
局部來源替換從 [D₁₃ 形式化報告](lean_sealed_four_port.md)及其 audit 命令進入。
圖／list 基礎先讀 root 工具，再讀雙拒絕工具的未完成依賴表，最後讀 BoundaryDegree 的
完整前提、具名 theorem 及 audit 命令。其他領域沿表中報告回到原 Lean 檔。
驗證時依報告執行 `lake build` 與對應 `#print axioms` audit；二者分開記錄。
普通 Lean 證明與 `native_decide` 的 compiler 信任分開；工具鏈以鎖檔為準，
不自動 `lake update`。LC 重播需顯式建置：

```bash
.venv/bin/python scripts/export_excess_two_certificates.py --check
lake --no-cache build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit
lake env lean -j 1 Math/ExcessTwoCertificatesAudit.lean
```

本次發布的實際建置、axiom audit 及未重跑範圍見
[發布驗證紀錄](history/2026-10-04-kprime-excess-two-progress-publish.md)。
