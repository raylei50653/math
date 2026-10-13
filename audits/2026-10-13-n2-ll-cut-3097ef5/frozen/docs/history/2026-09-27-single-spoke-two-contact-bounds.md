# 2026-09-27：single-spoke 剩餘二接點上界分類

結果與任意大小證明見 [專題報告](../c5_single_spoke_two_contact_bounds.md)。
從 root sweep 的 34 個 open_queries 只抽出 component 0 有未知上界的
18 個，保留 actual supports、兩份單接點次序、完整 relation 語意及路徑來源。

9 個角色組、6 個 target 相等分割的幾何 reflection orbits；字面反射列另存，
不當作固定 q 的 target 色等價。原 completion 直接關閉 0 個：4 個缺 q
禁色角色前提，其餘 14 個還碰 singleton 並缺原 frame 的指定路徑證據。
新的共同化約關閉全部18：色對稱容量4、外部路徑旁支 K5 6、二接點未用
色對 bridge 障礙8。114筆現為98雙列、4只證p₁、12只證p₂；剩16查詢均
是單接點上界，不繼續擴大本輪範圍。

實際通過：

- `python3 scripts/c5_single_spoke_two_contact_bounds.py --check`：重播3,492個
  完整 relation 接線；65,535個非空 ordered binary relations；兩種 literal
  target 各20個旁支路徑局部型；540份不使用zb0的K5控制；18筆分類。
- `python3 scripts/c5_single_spoke_root_sweep.py --check`。
- `python3 scripts/c5_single_spoke_branch_minor.py --check`。
- `python3 scripts/c5_single_spoke_branch_palettes.py --check`。
- `python3 scripts/c5_single_spoke_bridge_path.py --check`。
- `python3 scripts/c5_single_spoke_completion.py --check`。
- `lake build`：8826 jobs成功；既有 AttachmentOrder、SymRelabel linter warnings。
- `python3 scripts/check_docs.py` 與 `git diff --check`。

未新增 Lean theorem，未重跑一般圖枚舉、雙拒絕 atlas 或 R 系列大覆蓋。
原 artifacts 不改寫；本輪 source／artifact／report 另存。

後續依使用者 `commit + push` 請求發布相連的 checker、artifact、報告、
README 入口及 HANDOFF／STATUS。發布前重播新 checker、文件與 whitespace
檢查；沿用本輪已完成的 Lean build 與上述既有 checker，不重跑無關枚舉。
