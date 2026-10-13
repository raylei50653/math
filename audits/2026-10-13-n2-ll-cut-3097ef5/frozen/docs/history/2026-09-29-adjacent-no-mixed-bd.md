# 2026-09-29：B–D 雙飽和原分量來源排除

依使用者「推進 B–D class」接續既有未提交 B–E／E–E／B–C 成果，未 commit／push。
[報告](../c5_adjacent_degree5_no_mixed_bd.md)、新 checker 及 artifacts 保存本輪證據。
180 份原接合接上 780 份幾何，得到 312 份必要支援，全部 source K5 排除；
108 個原 IDs 無相容支援。288 份在兩個 pair 各有見證，另各 12 份只能由
其中一個 pair 的本規則排除。八份沒有原 spoke-route 見證，必須保留另一
原分量到框的路徑。0 target 查詢、0 新增 target 接受，不需 T4，含 root 交換型。

新增正反向 360 個原 IDs，累計十類／2,396 份覆蓋、五類／1,152 份保留。
下一入口 C–C 的 144 份 IDs 已綁定，首項 join 0、sides=(16,16)；尚未建支援表。
證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 有限證書。
未新增 Lean theorem；未證必要支援實現、任意來源完整 Σ、一般／共同出口或 K∞=K≤5。

本輪驗證通過：

- `python3 scripts/c5_adjacent_degree5_no_mixed_bd.py --check`：逐 byte 重播新 JSON／表格；2,568 次 minor controls、13 個負控制、312 份 source 反射／完整關係搬運／整分量交換／root 交換。
- `python3 scripts/c5_adjacent_degree5_no_mixed_bc.py --check`：沿用四分量幾何、source IDs 與 frontier 證書。
- `python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check`：沿用雙飽和原路徑及 minor 證書；其 spoke-route 結論未直接搬到 B–D。
- `lake build`：8,827 jobs 成功，只有既有 AttachmentOrder／SymRelabel linter warnings；不表示新紙面拓撲已形式化。
- `python3 scripts/check_docs.py`、`python3 tools/docgraph check`、`git diff --check`：通過。

未獨立重跑 no-mixed 原枚舉、A–C 缺額型、B–B／B–E／E–E、其他 mixed／
唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包、Lean axiom audit
或外部 degree-list 文獻核對；依賴函式在新 checker 內重算，原證據沿用。
既有 artifacts 未改寫。README、HANDOFF 的入口與研究線 tag 不變，
依文件治理更新專題、研究線導覽、出口及 STATUS。
