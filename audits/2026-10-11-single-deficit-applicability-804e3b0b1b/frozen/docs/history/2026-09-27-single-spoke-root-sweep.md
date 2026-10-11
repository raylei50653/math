# 2026-09-27：單接點未用色守恆掃過 114 筆

研究報告：[root 守恆全表掃描](../c5_single_spoke_root_sweep.md)。
接續 [root 守恆](2026-09-27-single-spoke-root-conservation.md) 的下一步；未 commit／push。

將「單接點分量、d≠a、d 不在 q、p 的支援色中 ⇒ d∉F_C(p)」套用到原 114 筆
全部 228 個指定查詢，與 completion 已存上界合用。新增 14 個接受查詢
（p₁：61、72、78、88、154、172、181、202；p₂：14、18、112、131、193、212）。
兩列已證 66 → 80，只證 p₁ 18 → 12，只證 p₂ 30 → 22，未決 48 → 34。
以另一目標列已知禁色作參考不新增結果。72 組表內反射配對的接受狀態一致。

本輪通過：

```bash
python3 scripts/c5_single_spoke_root_sweep.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
python3 scripts/c5_single_spoke_branch_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
python3 scripts/check_docs.py
git diff --check
```

未跑 `lake build`（本輪無 Lean 變更）；未新增 Lean theorem。
既有 two-spoke checker、R 系列大枚舉與 graph catalogue 未重跑。
