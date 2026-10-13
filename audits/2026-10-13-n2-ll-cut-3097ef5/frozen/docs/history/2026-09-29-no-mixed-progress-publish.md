# 2026-09-29：No-mixed 五組成果整理與發布核對

依使用者「整理目前進展 commit + push」整合完整證據包。本地研究基準
`f29b899`；發布前 fetch 發現遠端已有三筆 HANDOFF 整理提交，頂端為
`734632c`。先保存本地內容與雜湊，快轉接上遠端，再還原研究變更；
唯一衝突為 HANDOFF，保留遠端的精簡結構與 display math 格式，將活躍
入口更新為本輪完成後的重疊型。還原時其餘 30 份檔案逐 byte 保持。
文件檢查另發現遠端改名的 §1／§2 不符必備標題，且破壞舊歷史錨點；
已恢復相容標題，保留精簡內容與新的活躍入口。
SSH 驗證失敗後改用現有 GitHub CLI 登入與單次 HTTPS 設定，未改 remote。

## 提交範圍與結論

| 成果 | 結論與證據入口 |
| --- | --- |
| t_z=2、t_w=1 原外部路徑／首橋 | [record 14](../c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) 新增 52 個延拓，1,054／1,120 已證 |
| t_z=2、t_w=1 原雙端點 | [record 22 及整型](../c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) 關閉其餘 66 個查詢，560 份支援的 1,120 查詢全證，0 新來源排除 |
| t_w=0,(2,1,1) 四分量型 | [完整支援與雙列](../c5_adjacent_degree5_no_mixed_t2_t0_singles.md)：96 份原資料接成 120 份支援，240 查詢全接受 |
| 交換或幾何阻斷範圍 | [25 格分類](../c5_exchange_geometry_scope.md) 與 1,920 份抽象路徑控制；原三類／552 份快照保留 |
| t_w=0,(2,2) 缺額型 | [D_w=1、O_w=0](../c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)：96 份原資料接成 364 份支援，source K5 排除 340，保留 24 份的 48 查詢全證 |

一併提交五份 checker、五份 JSON、五份生成表、五份報告與逐輪歷史，
並連接 README、STATUS、HANDOFF、root 預算與出口第九類。整理階段沒有
改動 checker／artifacts 或新增數學結論；原 IDs、完整 relations、實際
支援、具名接點、分量身份與來源／target 候選排除區別均保留。

出口第九類現在涵蓋四種 no-mixed 交換型，共 744 份原 joins；餘
11 型／2,804 份保留。任意大小結果為紙面證明＋外部 degree-list 定理，
Python 重播有限證書；必要表與 minor skeletons 不證 disk 可實現性，
未新增 Lean theorem。一般機制完備性、一般／共同出口及 K∞=K≤5 仍未證。

## 本輪驗證

以下十四個 checker 本輪全部實際重跑，嚴格 `--check` 通過：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
```

`lake build` 通過（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings。未改 Lean，建置成功不表示新紙面 topology 已形式化。
本輪未重讀外部 degree-list 講義，沿用各報告明列的來源與前提。

缺額型 checker 同時重算舊 `c5_single_spoke_two_two.py` 數學 payload
及生成支援表，兩者皆與舊檔相同；唯一 provenance 差異仍為
`docs/c5_single_spoke_cores.md` 的 SHA。原 artifacts 不覆寫；詳見
[當輪差異紀錄](2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)。這項內容重播
不記作舊 checker 的嚴格 `--check` 通過，本輪沒有再單獨執行該舊命令。

未單獨重跑 t2 初層／interfaces、其餘 mixed／唯一 degree-5 完成表、
雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。整合文件後另跑：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
git diff --cached --check
```

文件檢查通過（304 份 Markdown、3,205 個本地連結）；DocGraph 通過
（61 文件、206 關係、5 families，0 errors／notes）。HANDOFF 為 129 行。
工作樹空白檢查已通過；暫存檢查在 commit 前完成。

## 精確交接與發布邊界

下一入口維持 t_z=2,(2)、t_w=0,(2,2)、D_w=0、O_w=1 的 96 份；
首項 retained-join ID=3040、sides=(133,30)，B_z=01、F_Cz={2}、
w 禁色=({0,1},{0,2})、共同 c=3。兩個飽和分量的完整 pair relations
及各自原路徑必須保留；其支援／targets 尚未完成。優先序只見
[HANDOFF](../HANDOFF.md)。

發布以實際 commit／push 和 `HEAD=origin/main=remote main` 回讀及乾淨
工作樹為準；此紀錄不預先聲稱尚未完成的遠端操作。
