# 2026-09-29：C–E 五正跨度與原路徑來源排除

依使用者「推進 C-E class」接續工作區 C–D 成果，未 commit／push。
[報告](../c5_adjacent_degree5_no_mixed_ce.md)、新 checker 及 artifacts 保存證據。
144 份正向接合接 60 份幾何得到 96 份必要支援，全部 source K5；108 個
原 IDs 無相容支援。五正跨度恰用完 C5，各支援皆為一條框邊；z 側唯一
飽和分量的兩框點和補弧提供統一 minor，同側另一原分量供原外部路徑。
兩 root 無 spoke，不需 T4，0 target 查詢。整圖 root 交換給 E–C。

含交換新增 288 個 IDs，累計十三類／3,116 份覆蓋，兩類／432 份保留。
下一入口 D–D 的 144 份 IDs 已綁定，首項 join=424、sides=(30,30)，
尚未建立其支援／target 表；D–E 含交換型的 288 份保留。
證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域
證書；未新增 Lean theorem。未證支援實現、任意來源完整 Σ、一般／
共同出口、一般交換完備性或 K∞=K≤5；沒有獨立第二審稿者。

本輪驗證：

- `python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check` 及
  `PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check`：
  通過，JSON／逐筆表逐 byte 相等；416 次 minor controls、11 個控制，
  完整關係反射／座標反序／整分量交換、整圖 root 交換及反向 IDs 均核對。
- `python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check`：通過，前序
  640 份支援與 C–E frontier 重播。
- `python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check`：
  通過，沿用飽和原路徑／固定框弧依賴重播。
- `lake build`：8,827 jobs 成功，僅既有 AttachmentOrder／SymRelabel
  linter warnings；不表示新紙面 topology／minor 已形式化。
- `python3 scripts/check_docs.py`：通過，335 份 Markdown、3,391 個本地連結。
- `python3 tools/docgraph check`：通過，62 documents、213 relations，零 errors／notes。
- `git diff --check`：通過；本輪新檔另檢查尾端空白。

未獨立重跑 no-mixed 原枚舉、B–B／B–C／B–D／B–E／C–C／E–E、A–D、
其他 mixed／唯一 degree-5 表、雙拒絕 atlas、R 系列、profiles／閉包、
Lean axiom audit 或外部 degree-list 文獻查核。新 checker 內重算所用
依賴函式，其餘原證據沿用；舊 scripts／artifacts 未改寫。
依文件治理更新專題、導覽、出口、範圍、STATUS 與歷史；README／HANDOFF
閱讀入口及研究線 tag 不變，故不追加本輪摘要。
