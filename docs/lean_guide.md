# Lean 形式化導覽

更新：2026-10-02。本輪新增共同 repair 判準的普通 Lean 證明與公理審計；
其他項目的證據範圍沿用各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

把研究中的可重用介面、list 前提、有限證書與數學定理接到具名 Lean theorem，
逐項記錄公理依賴。編譯成功不代表紙面 Gallai、minor 或 disk 論證已形式化。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 共同 repair 判準 | 27 個普通 theorem：W／C 雙向判準、極小修復／極大失敗、唯一最少解、退化支及具名投影介面；六圖前提與拓撲尚未匯入 Lean | [CommonRepair](lean_common_repair.md) |
| Root 接合 | 15 個普通 Lean 定理與報告對照；不含完整 minor／disk 層 | [root 工具](lean_root_interfaces.md) |
| 雙拒絕共用工具 | 共用 list／接合引理已具名；完整紙面分類仍有形式化依賴 | [雙拒絕工具](lean_two_rejection_tools.md) |
| 實際接線與 degree-list 緊性 | 13 個普通定理：原圖延拓 iff、degree 拆分、拒絕迫緊等；lists 直接由原圖 attachments 定義 | [BoundaryDegree](lean_boundary_degree.md) |
| Grammar／端點次序 | 指定 triangle grammar 的語義、normal form 與端點編譯已有；embedding 抽取仍在紙面層 | [normal form](attachment_normal_form.md)、[topology](topology_completeness.md) |
| Completion／weak bisimulation | 同頂點 completion 有紙面證明；一般 bisimulation／finite traces 有假設式 Lean 定理，拓撲與生成器未形式化 | [completion](c5_completion_weak_bisimulation.md) |
| 枚舉／有限證書 | Cell 枚舉的 Lean 鏈及外部信任已明列；有限結果不能外推全部 disk | [enumerator](c5_cell_enumerator.md)、[phase 1](phase1.md) |
| 計數代數 | 部分代數形式化可用；不補足 cone／connectivity 或平面來源論證 | [count cone](c5_count_cone_bridge.md)、[Kempe 導覽](c5_kempe_guide.md) |

## 3. 停止點與保留缺口

目前 reusable 基礎包含「實際圖 → 剩餘 lists → degree-list 前提 → 拒絕迫緊」，
以及「完整接受集合 → W／C 充要判準 → 全部 repair 模板與極小分類」。
共同 repair 的下一個可分離缺口是將具名原圖 J/P 及每條 W／C 前提匯入 Lean；
抽象判準不替代六圖前提的 Python 驗證或 disk 可用框證明。
Gallai／degree-list 外部定理、完整紙面分類、來源 minors 與 disk topology
仍須分別補齊，不能以 BoundaryDegree 或有限 `native_decide` 證書代替。
其他研究線保留上述依賴。

## 4. 閱讀與重播入口

共同 repair 從[形式化報告](lean_common_repair.md)及其 audit 命令進入。
圖／list 基礎先讀 root 工具，再讀雙拒絕工具的未完成依賴表，最後讀 BoundaryDegree 的
完整前提、具名 theorem 及 audit 命令。其他領域沿表中報告回到原 Lean 檔。
驗證時依報告執行 `lake build` 與對應 `#print axioms` audit；二者分開記錄。
普通 Lean 證明與 `native_decide` 的 compiler 信任分開；工具鏈以鎖檔為準，
不自動 `lake update`。本輪執行完整 build 及 CommonRepair axiom audit；
未重跑其他模組的獨立 axiom audit。
