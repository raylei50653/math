# 2026-09-27：single-spoke 外部雙路徑 completion

報告：[外部雙路徑 completion](../c5_single_spoke_completion.md)。
接手 HEAD 為 `4f26efe`；當時已有尚未提交的 single-spoke 覆蓋、支援表、
checker／artifact 與文件變更。本輪接續這些成果，保留原支援 artifact 及歷史。

完成任意大小的外部雙路徑引理：保持二接點分量全部實際接線，利用其他
分量或原 spoke 提供的兩條不交路徑，收縮為 degree-4 disk completion。
未接 singleton 引理與繼承的 3,492 個接線完整關係排除指定雙禁色。
p₁ 僅由既有 q-preserving 反射及全域色置換搬運。

原窄入口 s=0、(S₁,S₂,S₃)=(01,04,234)、C₃ 二接點的 p₂ 已證可取 z=3。
套回原 19 型／114 筆具名配置後，新增 30 個接受查詢：62 筆兩列已證、
20 筆只證 p₁、32 筆只證 p₂，沒有兩列皆未決的配置。支援型仍不代表可實現。

下一窄入口改為 s=0、(S₁,S₂,S₃)=(01,04,1234)、C₃ 二接點。
p₂ 已證；p₁ 若拒絕必有 R_C₃(p₁)={(2,3),(3,2)}，同圖 F_C₃(q)={3}。
這次 singleton b3 有實際接線，不能再次引用無 singleton attachment 的分類。

實際驗證：

- `python3 scripts/c5_single_spoke_completion.py --check`：通過；完整重播
  3,492 份繼承接線的 q／p₂ tuples、反向接點座標、114 筆分離記錄及輸入 hashes。
- `python3 scripts/c5_single_spoke_cores.py --check`：通過；原覆蓋／支援證書不變。
- `python3 scripts/c5_two_spoke_nonadjacent.py --check`：通過；74 個正常形
  增邊控制與 3,492 個 completion，含 528 個 p₂ 拒絕 completion 的逐邊著色。
- `python3 scripts/c5_two_spoke_reflection.py --check`：通過。
- `lake build`：通過（8,826 jobs）；只有既有 AttachmentOrder／SymRelabel warnings。
- `python3 scripts/check_docs.py`：通過（160 份 Markdown、2,067 個本地連結）；
  將 HANDOFF 重播清單縮為本輪必要範圍後，符合 150 行上限。
- `git diff --check`：通過；新建檔案另核對無 trailing whitespace。

紙面 minor／來源覆蓋、既有外部 degree-list、有限 Python 重播及既有 Lean
反射的信任層保持區分；沒有新增 Lean theorem。未重跑大型 degree-4／R 系列
來源分類、一般 graph catalog、603 profiles、固定點或全部 t=2 檢查。
本輪未 commit／push。
