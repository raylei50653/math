# 2026-09-29：B–C 飽和原路徑與雙列分離

本輪依使用者「推進 B–C class」接續既有未提交 B–E／E–E 成果，未 commit／push。
[報告](../c5_adjacent_degree5_no_mixed_bc.md) 與新 checker／artifacts 保存完整證據。
180 個原 IDs 接上 780 份幾何，608 必要支援中 584 source K5 排除；
保留 24 份的 48 個 target 全由搬運／容量上界接受，0 未決。
新增正反向 360 個原 IDs，累計九類／2,036 份覆蓋、六類／1,512 份保留。
下一窄入口 B–D，首項 join 2128、sides=(91,30)。

證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 有限證書。
不需 T4；未新增 Lean theorem、未證 disk 實現／任意來源完整 Σ／一般出口。

本輪驗證通過：

- `python3 scripts/c5_adjacent_degree5_no_mixed_bc.py --check`：逐 byte 重播新 JSON／表格；含 1,752 次 minor、1,704 次完整關係搬運及 48 次字面 target 反射的完整候選／root 色對核對。
- `python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check`：前輪 source IDs／覆蓋及 frontier 證書。
- `python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check`：沿用飽和分量／原路徑引理的 A–C 證書。
- `lake build`：8,827 jobs 成功，只有既有 AttachmentOrder／SymRelabel linter warnings；不表示新 B–C 紙面拓撲已形式化。
- `python3 scripts/check_docs.py`、`python3 tools/docgraph check`、`git diff --check`：通過。

未獨立重跑 no-mixed 原枚舉、B–B／B–E、其餘 mixed／唯一 degree-5 完成表、
雙拒絕 atlas、R 系列、profiles／閉包、Lean axiom audit 或外部 degree-list 文獻核對。
其原證據沿用；本輪未改寫既有 artifacts。
README、HANDOFF 的閱讀入口與進行中研究線不變，依文件治理只更新導覽與 STATUS。
