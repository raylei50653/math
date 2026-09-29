# 2026-09-29：t_z=2、t_w=0、(2,1,1) 四分量覆蓋與雙列分離

研究基準 `f29b899`，工作目錄 `/home/ray/developer/ai/math`。接續進場時已有的
t2-t1 bridge／endpoints 未提交 bundle；未改寫其 scripts／artifacts。
本輪新增 checker、JSON／逐筆表、[報告](../c5_adjacent_degree5_no_mixed_t2_t0_singles.md)，
更新出口第九類、README、STATUS、HANDOFF 及前輪報告的後續入口；未 commit／push。

## 成果與證據

沿原 3,548 份同色 joins，只處理交接指定的 96 份有序資料；原 IDs、sides、
SHA 及前輪保存的 `next_frontier` 均逐筆綁定。四原分量、六接點、兩原 spokes、
zw 及共同色框完整保留。w 無 spoke 時，C_z 的外部路徑改由原 zw、D_w 內部
及實際附件提供；對 w 側三分量仍可用原 w–z–B 路徑。

| 項目 | 結果 |
| --- | ---: |
| 兩算法一致的支援／placements | 480／480 |
| 原 96 份有支援／空纖維 | 36／60 |
| 必要支援、全為 c=3 | 120 |
| 指定查詢全接受 | 240／240 |
| 完整關係搬運／搬運加上界 | 216／24 |
| 完整 target joins，全有非對角色對 | 336 |
| 雙列皆證／未決／新支援來源排除 | 120／0／0 |
| 具名 contact rotations | 1,920 |
| 字面 target 反射／整分量 D_w、E_w 交換 | 240／120 |
| q／target 的完整 root 色對交換 | 456 |
| 負控制 | 8 |

24 個上界查詢只需 C_z 的全部五種容量／穩定子候選，w 側三份完整關係
皆精確搬運；逐項可取 w=3、z≠3。沒有用新 target minor 或 T4 排除。
此型及整圖 root 交換型接入 [出口第九類](../c5_single_sided_exit.md#1-定義與定理)；
完整 Σ 仍使用來源雙缺失與刪邊繼承，沒有從兩個 target 自動外推。

任意大小覆蓋由紙面 annulus／實際外部路徑論證及外部 degree-list 定理承擔。
本輪重讀 Dvořák 講義 Lemma 7／Theorem 10，連結與前提見報告 §2。
Python 固定域重播不是來源 disk 實現；未新增 Lean theorem。

## 本輪驗證

以下八個 checker 的 `--check` 全部通過，saved JSON／Markdown byte-identical：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_root_degree_excess.py --check
```

`lake build` 通過（8,827 jobs），有既有 AttachmentOrder／SymRelabel linter
warnings；本輪未修改 Lean 檔，也未新增紙面拓撲的形式化。
文件驗證亦通過：297 份 Markdown／3,186 個本地連結；DocGraph 59 文件、
195 關係、5 families，0 errors／notes；HANDOFF 150 行，`git diff --check` 通過。
命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未單獨重跑 t2 bridge／endpoints／path-palettes、t2-t1 初層與 bridge 的
完整鏈、其餘 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、
profiles／閉包及 Lean axiom audit；其已有成果沿用原證據。
t2-t1 endpoints checker 本身重播的依賴控制，與單獨重跑各層明確區分。

## 停止點與下一入口

本型已完成，沒有待解 target。下一步固定為 t_z=2,(2)，t_w=0,(2,2)，
w 側預算 D_w=1、O_w=0；原 96 份中禁色大小 (1,2)／(2,1) 各 48。
首項 retained-join ID=3036、sides=(133,16)，B_z=01、F_z={2}、
w 禁色=({0},{1,2})、c=3。新 JSON 只保存原 ID／SHA，未建立下一型支援。
三原分量、六接點、兩 spokes、zw 及飽和二接點完整關係必須保留。
另 96 份 D_w=0、O_w=1 型及一般出口保留；現行優先序見 [HANDOFF](../HANDOFF.md)。
