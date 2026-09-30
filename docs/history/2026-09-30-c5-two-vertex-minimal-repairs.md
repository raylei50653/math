# 2026-09-30：C₅ 全部 inclusion-minimal 四點修復

接續四點最少個數與唯一組合，固定原反向十五點三十五邊圖、
八點 U、完整 J 與基底 P。接手時工作樹乾淨，分支 main。
研究完成時尚未 commit／push；同日提交整理見文末，發布狀態以即時 Git 為準。目前入口見
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)。

## 成果與證據

- 新增[專題報告](../c5_two_vertex_minimal_repairs.md)、
  [checker](../../scripts/c5_two_vertex_minimal_repairs.py)與
  [完整證書](../../artifacts/c5_two_vertex_overlap/minimal_repairs.json)。
- 以既有 x 迫 S_A；含 S_B 時極小性只容許唯一二份解。
  不含 S_B 時既有 y 迫 S_T，再依完整排除集合枚舉。
  化約後 16 個類子集合與不作化約的全部 256 個子集合相符。
- 三個極小類組合展開成全部十五份具名解：一組 `{S_A,S_B}`，
  以及十四組 `{S_A,S_T,E}`，其中 E 含 `{b2,b4}` 且不等於 S_B。
  十三個 E 屬同一完整排除類，S_W 另成一類，沒有以基數合併。
- 44 份逐份刪除記錄均保存完整殘留軌道 IDs、具名差集大小與
  不可省見證。三份見證 x/y/z 的 192 份原圖局部延拓及原邊拒絕
  證明沿用且重驗，不把分別延拓當共用八點延拓。
- 每組在全部 `4^8` 具名賦色直接查詢完整投影，共 983,040 次；
  十五個完整接受集合都逐 tuple 等於重新從原圖求得的 J，
  恰有 60 軌道／1,440 賦色。Hash 與基數只作紀錄。
- 前報告加後續狀態，更新兩點重疊／state 導覽與 STATUS。
  依文件治理，研究線及基本入口未變，README／HANDOFF 不追加
  逐輪摘要。原 checker 與 artifacts 保留原 bytes。

## 驗證與工作狀態

新生成器完成一般生成；九項負控制按預期拒絕：漏排除類、
同基數錯誤排除集合、漏具名展開、重複組合、scope ID 次序錯誤、
加入非極小超集合、同基數錯誤刪除殘留、不能通過保留 scope 的
見證，以及同基數錯誤修復 relation。

前輪四點 checker 只讀重播通過，包含 2,415 配對、192 份延拓／
4,608 份共同換色及其九項負控制。`lake build` 通過 8,827 jobs，
只有既有 AttachmentOrder／SymRelabel linter warnings；未新增
Lean theorem 或 `native_decide`。

新證書大小 369,091 bytes，小於大型 artifacts 門檻，直接保存。
一般與 `PYTHONHASHSEED=17` 的 `--check` 均逐 byte 通過。
文件檢查通過 385 份 Markdown／3,909 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes；
`git diff --check` 通過。

```bash
python3 scripts/c5_two_vertex_minimal_repairs.py
python3 scripts/c5_two_vertex_minimal_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_minimal_repairs.py --check
python3 scripts/c5_two_vertex_quaternary_repairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪未重跑來源大枚舉、目錄最小性、獨立拓撲／單框 checker、
三點 checker、六份接合 checker、點對索引或 Lean axiom audit；
來源 hash 鏈均核對，J 由原邊及七個原私有內點直接重建。
研究階段沒有修改 Lean，沒有操作 Git index。

指定固定模型的 inclusion-minimal 分類已完成；未指定後續窄題。
一般局部條件表、輔助變數、其他圖、多步充分性及 `K∞=K≤5` 保留。

## 同日提交整理（基準 3ac4159）

依使用者要求，將新 checker、369,091-byte 證書、專題報告、
本紀錄及四份相關導覽／索引更新整理為同一提交，發布至 main。
前輪三點、四點大型證書及其 manifest 均保持原 bytes；新證書
小於 1 MB，直接隨本次提交保存。README／HANDOFF 的既有入口仍有效。

提交前再次執行新 checker 的 `--check` 與 `lake build`，均通過；
不同 hash seed、前輪四點 checker 與其負控制沿用本次對話研究階段
對同一份程式／證書的通過結果。文件、DocGraph 與 staged diff
於整理完成後檢查。提交後以 `HEAD`、`origin/main`、遠端 main
三份 SHA 及工作樹狀態作最後核對，不在本檔預寫尚未產生的 commit SHA。
