# 2026-09-27：單接點未用色守恆與指定 p₂ 延拓

接續既有未提交的五輪 single-spoke 成果；原成果保留，未 commit／push。
研究報告：[單接點未用色守恆](../c5_single_spoke_root_conservation.md)。

完成 (012,04,234)、禁 3 者二接點的指定入口：C₁ 在 p₂ 不禁 3，
與原 completion 合用可取 z=3。任意大小論證由 block-tree 固定色歸納承擔，
沿用 R10 外部 degree-list 定理與既有 K4-free 結構，未新增 Lean theorem。
新 checker 有 2,632 個非 root 局部核對、1,340 個 root 聯集核對與 8 個
實際 root 接線控制；這些不是來源圖大小 cover。

只更新 source_index 23、28 的 p₂；114 筆中兩列已證 64 → 66，
只證 p₁ 20 → 18，只證 p₂ 維持 30，未決查詢 50 → 48。
下一步將通用單接點引理套回原表，與已存完整關係／completion 上界合用。

本輪通過：

```bash
python3 scripts/c5_single_spoke_root_conservation.py --check
python3 scripts/c5_single_spoke_branch_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

`lake build` 完成 8,826 jobs，僅重播既有 linter warnings；未重新進行 Lean
axiom audit。文件／空白檢查不驗證數學；新紙面歸納未 Lean 化。
既有 two-spoke 原 checker、atlas、R 系列大枚舉與 graph catalogue 未重跑。
一般單側／共同出口及 K∞=K≤5 仍未證。
