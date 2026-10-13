# 2026-09-29：無 mixed 兩側 t=2 的實際支援、環序與 target 上界

接續未提交的無 mixed 第一輪化約；工作目錄為專案根目錄。
本輪只推進交接指定的 t_z=t_w=2、兩側 (2)，保留進場時其他研究變更。
使用者未要求 commit／push，本輪未執行；未啟動 sub-agents 或 Graphify。

成果入口：[專題報告](../c5_adjacent_degree5_no_mixed_t2.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2/observations.json)、
[支援及原資料纖維表](../../artifacts/c5_adjacent_degree5_no_mixed_t2/support_table.md)。

## 成果與界線

- 原 zw 的細鄰域給兩側各自連續的六單位環序；每份 unary actual support
  至少見兩個 q 色。保留原 zw、四條 spokes、兩個原分量、全部原內邊／
  附件及兩側完整有序接點，沒有收縮來源圖或乘 endpoint marginals。
- 遞增 lifts 與整側 hull-edge masks 兩算法同得 2,550 份幾何、2,560 個
  placements，四種接點方向共 10,240 次具名 root-rotation 控制。
- 原 88 份 frontier 的 ID／side IDs／完整記錄／SHA 綁定；42 份有支援，
  46 份纖維空，得到 322 份必要資料。原 118／3,548 及其 88 份子表未改寫。
- 全部 65,535 個非空二元關係獨立核對每個 singleton-ban 的 95 份完整
  schemas；actual-support 穩定子留下每側 17 或 95 份，未宣稱實現性。
- 644 個 target 查詢共 2,892 組完整禁色候選，已證 512 個接受；
  A/A、A/?、?/A、?/? 為 206、50、50、16，剩 132 個查詢未決。
  322 次 root 交換、644 次字面反射 target 控制皆通過。

證據為任意大小紙面化約＋外部 degree-list 定理＋Python 必要表；本輪
重讀 Dvořák Lemma 7／Theorem 10 第 5–6 頁。未新增 Lean theorem，
未證整型 target 分離、disk 實現、完整 Σ 或一般出口。未用 T4 或四色
定理篩除來源；322 份中本輪沒有新增 K5／T4 來源排除。

下一入口是新 record 4／p₁，原 frontier 31、sides=(137,147)：
B_z=04、S_z=01、F_z(q)={1}；B_w=34、S_w=123、F_w(q)={0}、c=3。
p₁ 的唯一失敗上界 F_w={0,3} 令 E_w=∅；保留 wb3、wb4、zw 及 C_z，
研究同一 C_w 的雙禁色 bridge／固定框弧。這不是實際不可延拓圖。

## 本輪實際驗證

以下七個 checker 均以 `--check` 重播既存／新證書，全部通過：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
```

`lake build` 通過，8,827 jobs；只重播既有 `AttachmentOrder`／`SymRelabel`
style、unused simp 等 warnings，未新增 Lean 檔。

文件／DocGraph／diff 檢查全部通過：文件檢查覆蓋 272 份 Markdown，
DocGraph 有 51 份文件、155 條關係、5 個 families，0 errors／notes。

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑其他 mixed 子類、唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、
profiles／閉包、全圖大枚舉或 Lean axiom audit；未把本輪局部重播寫成
全專案研究證書的完整驗證。README／STATUS／HANDOFF 已接上本輪新入口。
