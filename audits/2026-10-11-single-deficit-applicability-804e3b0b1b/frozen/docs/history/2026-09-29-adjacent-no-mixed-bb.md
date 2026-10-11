# 2026-09-29：B–B 四分量支援、完整關係與 target 分離

Git 基準 `f2496f5`，接手時工作區乾淨。依使用者指定順序：先對原 236 份
IDs／sides 建立支援／環序必要覆蓋，保留兩個 binary schemas 與兩個 unary
relations 接合完整 targets，最後只處理剩餘失敗候選。研究完成時成果先留在工作區；後續使用者要求 commit／push。
提交包含本輪 checker、JSON／支援表、報告、導覽、STATUS、出口與範圍文件。[報告](../c5_adjacent_degree5_no_mixed_bb.md)保存完整前提及證據界線。

## 成果

- 兩算法一致給 2,520 份幾何／placements；10,080 次具名 contact rotations。
- 原 236 份接成 888 份必要支援：92 份原資料有支援、144 份纖維空。
  四原分量、六接點、兩 spokes、zw、actual supports 與完整 schemas 全保留。
- 3,504 組完整 target joins：第一層 1,656／1,776 接受，120 個查詢各剩一個
  失敗候選。48 個原路徑／固定框弧反證、72 個原雙端點反證，最終全接受。
  未新增 palette 交換論證；888 份支援沒有額外 source minor 排除。
- 67,104 次完整 relation 搬運、888 個整來源 root swaps、1,776 個字面 target
  反射；120 個失敗候選另核反射與整 root 交換。1,016 份具名 K5 skeletons、
  21 個負控制保留原 Dz／Dw 路徑及兩 root degree-5 incidences。
- 第九類出口加入 B–B。原必要參數累計六型／1,172 份覆蓋，九型／2,376 份
  仍開放；只綁定下一 B–E 的 180 份 IDs，未展開其支援或 target 遍歷。

任意大小覆蓋及 K5 抽取為紙面論證，degree-list／palette 定理沿用既有報告，
本輪未重新查核外部文獻。Python 證書不是來源實現，未新增 Lean theorem；
一般機制完備性、完整 Σ、一般／共同出口及 K∞=K≤5 仍未證。

## 驗證

以下研究檢查均 exit 0；新 checker 在預設及 `PYTHONHASHSEED=17` 下均與
生成的 JSON／Markdown 逐 byte 相同。`lake build` 完成 8,827 jobs，只有
既有 AttachmentOrder／SymRelabel linter 警告。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件檢查通過 314 份 Markdown／3,201 個本地連結；DocGraph 為 62 documents、
213 relations、5 families，0 errors／0 notes；`git diff --check` 通過。
未單獨重跑：重疊／缺額型、
t2 初層及 t2/t1 bridge、其餘 mixed／唯一 degree-5 完成表、Root 預算全控制、
範圍遍歷、雙拒絕 atlas、R 系列、profiles／閉包與 Lean axiom audit。
新 checker 讀取相關原資料並保存輸入 SHA；這不等於重新驗證全部前序成果。

更新專題報告、研究線導覽、STATUS、出口及範圍報告；原重疊型加後續連結。
依 [文件治理](../DOCUMENTATION.md)，研究線及使用入口未變，HANDOFF／README
保持原角色，不加入逐輪數字。舊研究 scripts／artifacts 皆未改寫。

## 發布核對

發布沿用本輪已通過的研究 checker、不同 hash seed 重播及 Lean build；
研究程式、證書及 Lean 檔未再變更。提交前重新核對新證書的 checker／輸入
SHA256，以及文件、DocGraph、diff 檢查。提交及遠端 SHA、工作區乾淨狀態
以發布後 Git readback 為準，不預先宣告推送成功。
