# 2026-09-28：(2,2) 兩輪 K5 排除整合發布

接手基準為 `0f474d8`。依使用者要求「整理後 commit + push」，整合既有
[路徑塊支援排除](../c5_single_spoke_two_two_minor.md) 與
[外部路徑接合](../c5_single_spoke_two_two_external.md) 的程式、JSON、支援表、
報告及研究紀錄，連同 README／HANDOFF／STATUS 的後續入口一併提交。
本輪只整理與重播，沒有新增研究排除、改寫原必要表或重啟來源圖枚舉。
採 document-first，未使用 Graphify，未開 sub-agents。

## 成果範圍與停止點

兩輪任意大小紙面 K5 抽取分別排除 26 筆及 210 筆，含 record 110、119、104。
原 T4 保留的 380 筆累計排除 236 筆，剩 144 筆／72 個分量交換型。
剩餘兩列狀態為 A/A 54、A/? 30、?/A 42、?/? 18；原 104 筆 A/A 中另有
50 筆來源已排除，沒有新增或撤回條件式延拓定理。

完整來源記錄、有序接點、slit lifts、actual supports、raw targets 與反射
資料保留；原必要分類及 dual surgery 證書不改寫。各研究紀錄保留當輪
數字與「未 commit／push」語境，當前結果與接手優先序見 [HANDOFF](../HANDOFF.md)。

信任層為紙面證明、沿用的外部 degree-list 定理與有限 Python 控制。
拓撲 skeletons 不是 degree-4／list 來源 cover；未新增 Lean theorem，
`lake build` 不形式化新的 palette 歸納或 K5 抽取。
下一個窄入口仍為 record 15：s=0、支援 (01,0234)、禁色 ({1},{2,3})，
p₁ 已證、p₂ 未決。其餘 (2,2) 可實現性／分離、一般單側／共同出口及
`K∞=K≤5` 仍未證。

## 本輪實際驗證

- `python3 scripts/c5_single_spoke_two_two_minor.py --check`：48 residual rows、
  192 support rows、256 K5 controls、3 負控制；26 排除／354 剩餘；JSON 重播通過。
- `python3 scripts/c5_single_spoke_two_two_external.py --check`：186 support rows、
  496 K5 controls、6 負控制；210 新排除／144 剩餘；JSON 與支援表逐 byte 重播通過。
- `python3 scripts/c5_single_spoke_two_two.py --check`：原 1,530 必要配置、380 T4
  保留，以及完整 schemas／接點／反射與繼承的 relation 控制重播通過。
- `python3 scripts/c5_single_spoke_bridge_path.py --check`：16 tight rows、12 transitions 通過。
- `python3 scripts/c5_single_spoke_branch_palettes.py --check`：16 palette pairs、
  107 closure cases、20 path cases、5 rooted support types 通過。
- `lake build`：8,826 jobs 成功，僅重播既有 AttachmentOrder／SymRelabel linter warnings。

文件檢查通過：189 頁、2,285 本地連結，含 anchors、STATUS 索引及
HANDOFF 的 150 行上限。DocGraph 通過：22 份 metadata 文件、48 relations、
4 families，0 errors／0 notes。`git diff --check` 通過。重播命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑 dual surgery、edge-pair coordinates、circulation、雙拒絕 atlas、
R 系列大覆蓋、大圖 catalogue 或全策略閉包；沒有 Lean source 變更，
未另作 axiom audit。發布狀態以即時 Git 為準；push 後核對本地 HEAD、
origin/main 與遠端 main SHA 一致，並確認工作樹乾淨。
