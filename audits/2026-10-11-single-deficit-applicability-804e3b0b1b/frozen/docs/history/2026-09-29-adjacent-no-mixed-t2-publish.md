# 2026-09-29：無 mixed 兩側 t=2 三輪成果整合發布

本次依使用者「整理一下 commit+push」要求，將 bridge、雙端點及整條
原路徑 palettes 三輪成果合併為一份提交。接手分支 `main`，基準為
`51ef4946fd20d9a4b3b1b797289c1f6216d19c90`，遠端為 `origin`。
發布狀態以 Git 與完成後的本地／tracking／遠端 SHA 核對為準；本文
隨成果提交，不預填自身 commit SHA。原研究紀錄中的「未提交」保留當輪語境。

## 提交範圍與結果

三輪 checker、各自 JSON／完整表、專題報告及研究紀錄一併入庫；同步
README、HANDOFF、STATUS、前序報告通知與 single-sided exit 定理。
原必要表與三輪已生成證書不重建或改寫，使用 `--check` 逐 byte 重播。

| 層 | 新增延拓 | 累計 target 已證 | 雙列皆證 | 未決查詢 |
| --- | ---: | ---: | ---: | ---: |
| 已提交的原支援／環序表 | — | 512／644 | 206 | 132 |
| [原 bridge／固定框弧](../c5_adjacent_degree5_no_mixed_t2_bridge.md) | 68 | 580／644 | 258 | 64 |
| [原雙端點](../c5_adjacent_degree5_no_mixed_t2_endpoints.md) | 60 | 640／644 | 318 | 4 |
| [整條原路徑 palettes](../c5_adjacent_degree5_no_mixed_t2_path_palettes.md) | 4 | 644／644 | 322 | 0 |

本次合計新增 132 個延拓，原 322 份全保留，新增來源排除為 0。
原 IDs、88 份 frontier／side 記錄、完整 q schemas、placements、
四個具名接點 rotations、原分量與共同色框保持。三層依次核對來源
SHA256；完整 joins 與失敗候選的證據鏈保留。

指定圖類的無 mixed 兩側 t=2,(2) 已完成雙列分離，接入
[條件式出口](../c5_single_sided_exit.md) 第九類。完整 Σ(M)=Ω\{q}
仍另用來源雙缺失與刪邊繼承。不需 T4；證據為任意大小紙面證明、
外部 degree-list 定理與 Python 有限控制，未新增 Lean theorem。
必要表可實現性、一般單側／共同出口及 `K∞=K≤5` 仍未證。

下一窄入口保持 **t_z=2,(2)，t_w=1,(2,1)** 的實際支援／環序覆蓋。
原 3,548 份同色 joins 的此有序子表有 136 份，首項 sides=(133,91)；
保留三個原分量、五個接點、三 spokes、zw 與共同色框，root 交換覆蓋反向。
本次僅整理與發布，沒有推進下一型或重開來源圖枚舉。

## 本次驗證

三輪報告列出的 checker 與直接依賴之聯集，共 **15 個 checker 全部通過**：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
git diff --cached --check
```

`lake build` 通過（8,827 jobs），僅重播既有 AttachmentOrder／SymRelabel
的 style／unused simp warnings。沒有新增 Lean 檔，build 不將紙面
palette／minor 證明或外部定理形式化。

文件檢查通過：283 份 Markdown、3,073 個本地連結，HANDOFF 150 行。
DocGraph 通過：54 份文件、168 條關係、5 個 families，0 errors／notes。
`git diff --check` 通過；staged whitespace 另以 `git diff --cached --check`
納入提交前檢查。
其他 mixed／singleton 完成表、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、profiles／閉包、全圖枚舉及 Lean axiom audit 未重跑。
未使用 sub-agents 或 Graphify，沒有引入新依賴或更動工具鏈。

逐輪證明與當時驗證仍見 [bridge 紀錄](2026-09-29-adjacent-no-mixed-t2-bridge.md)、
[雙端點紀錄](2026-09-29-adjacent-no-mixed-t2-endpoints.md) 與
[整條原路徑紀錄](2026-09-29-adjacent-no-mixed-t2-path-palettes.md)。
