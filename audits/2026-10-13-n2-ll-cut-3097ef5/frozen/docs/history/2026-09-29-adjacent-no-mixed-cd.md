# 2026-09-29：C–D 三飽和原分量來源排除

依使用者「推進 C-D class」接續工作區 C–C 成果，未 commit／push。
[報告](../c5_adjacent_degree5_no_mixed_cd.md)、新 checker 及 artifacts 保存證據。
144 份正向原接合接上 240 份幾何，得到 640 份必要支援，全 source K5；
72 個原 IDs 無相容支援。576 份三個飽和分量各有見證，其餘 64 份各有
兩個；固定只查 z 側、Cw、Dw 分別漏 32、16、16 份。兩 root 均無
spoke，全部使用原分量外部路徑，不需 T4，0 target 查詢。

含 D–C 整圖交換新增 288 個 IDs，累計十二類／2,828 份覆蓋，三類／720
份保留。C–E 下一入口的 144 份正向原 IDs 已綁定，首項 join 12、
sides=(16,64)，尚未建立其支援／target 表。D–D、D–E 保留。

證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域
證書；未新增 Lean theorem。未證支援實現、任意來源完整 Σ、一般／
共同出口、一般交換完備性或 K∞=K≤5。本輪沒有獨立第二審稿者。

本輪驗證：

- `python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check` 及
  `PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check`：
  通過，JSON／逐筆表逐 byte 相等；6,080 次 minor controls、13 個控制，
  完整 schema 反射／整分量交換、整圖 root 交換與反向 IDs 均核對。
- `python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check`：通過，前序
  1,176 份支援與本輪 frontier 重播。
- `python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check`：
  通過，沿用飽和原路徑／固定框弧證書重播。
- `lake build`：8,827 jobs 成功，僅既有 AttachmentOrder／SymRelabel linter
  warnings；不表示新紙面 topology／minor 已形式化。
- `python3 scripts/check_docs.py`：通過，332 份 Markdown、3,362 個本地連結。
- `python3 tools/docgraph check`：通過，62 documents、213 relations，零 errors／notes。
- `git diff --check`：通過；新檔另檢查尾端空白。

未獨立重跑 no-mixed 原枚舉、B–B／B–C／B–D／B–E／E–E、A–D、其他
mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包、
Lean axiom audit 或外部 degree-list 文獻查核。新 checker 內重算所用依賴
函式，其餘原證據沿用。既有 scripts／artifacts 未改寫。
依文件治理更新專題、導覽、出口、範圍、STATUS 與歷史；README／HANDOFF
閱讀入口及研究線 tag 不變，因此未追加本輪摘要。
