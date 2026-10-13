# 2026-09-29：D–E 排除與 no-mixed 全分類完成

依使用者「推進 D-E class」接續工作區 D–D 成果，未 commit／push。
[報告](../c5_adjacent_degree5_no_mixed_de.md)、新 checker 與 artifacts 保存證據。
144 份正向原接合接 60 份幾何得到 48 份必要支援，全部 source K5；
120 個原 IDs 無相容支援。五正跨度恰用完五框邊，D 側兩份飽和原分量
各給原路徑／兩單點框弧 K5，同側另一原分量供避開所選分量的原外部路徑。
保留五原分量、八 contacts、原 zw、全部 actual supports 及完整關係。
不需 T4，0 target 查詢。

含 root 交換方向新增 288 個原 IDs，累計十五類／3,548 份原接合全覆蓋，
與原 retained joins 逐 ID 核對，沒有未處理的 no-mixed class。
出口第九類因此涵蓋全部相鄰雙 degree-5 no-mixed 分拆；來源排除不計作
雙列接受。下一窄入口可接單一較大 mixed 原分量的必要接點與 minimality
介面，本輪未建立該類支援表。一般／共同出口、一般交換完備性、任意來源
完整 Σ、disk 實現與 K∞=K≤5 未證。

本輪驗證：

- `python3 scripts/c5_adjacent_degree5_no_mixed_de.py --check` 與
  `PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_de.py --check`：
  通過，JSON／逐筆表逐 byte 相等。416 次 minor controls、224 份保存證書、
  11 個負控制；核對完整關係、反射、接點座標反序、整分量交換及 root 交換。
- `python3 scripts/c5_adjacent_degree5_no_mixed_dd.py --check`：通過，
  前序覆蓋及 D–E frontier 重播。
- `python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check`：通過，
  五分量幾何及原路徑證據依賴重播。
- `python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check`：通過，
  飽和原路徑與固定框弧依賴重播。
- `lake build`：8,827 jobs 成功，僅既有 AttachmentOrder／SymRelabel
  linter warnings；未新增 Lean theorem，不表示新紙面 topology 已形式化。

- `python3 scripts/check_docs.py`：通過，341 份 Markdown、3,449 個本地連結。
- `python3 tools/docgraph check`：通過，62 documents、213 relations，零 errors／notes。
- `git diff --check`：通過；本輪新檔另核對尾端空白及終止換行。

未獨立重跑 no-mixed 原枚舉、B–B／B–C／B–D／B–E／C–C／C–D／E–E、
其他 t=2／mixed／唯一 degree-5 表、雙拒絕 atlas、R 系列、profiles／閉包、
Lean axiom audit 或外部 degree-list 文獻查核。新 checker 內重算所用依賴
函式，其餘原證據沿用；舊 scripts／artifacts 未改寫。沒有獨立第二審稿者。
依文件治理更新專題、導覽、出口、範圍、STATUS 與歷史；README／HANDOFF
閱讀入口及研究線 tag 不變，故不追加本輪摘要。前輪未提交成果保留。
