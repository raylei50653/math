# 2026-09-30：C₅ 兩混合框共同拉回與跨框條件修復

本輪承接兩混合框的未提交成果，只比較同一反向接合圖的完整
R255／R1022 共同拉回與原八點 J。未 commit／push；發布狀態以
即時 Git 為準。目前停止點與下一題由
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護。

## 成果與範圍

- 新增[報告](../c5_two_vertex_mixed_pullback.md)、
  [checker](../../scripts/c5_two_vertex_mixed_pullback.py)及
  [完整證書](../../artifacts/c5_two_vertex_overlap/mixed_frame_pullback.json)。
  沿用同一十五點三十五邊原圖、具名 U、兩來源與兩混合框映射；
  兩框只在 a0、a2 的實際顏色相等時接合。
- 完整拉回 P 有 114 軌道／2,736 份賦色；原 J 仍有 60／1,440。
  P∖J 有 54／1,296，J∖P 為空。全部具名差集、54 份軌道記錄、
  每列的兩個原圖分別延拓及原邊拒絕證明均保存。
- 38 軌道違反唯一遺失的原 U 邊 b2–b4。補回後剩 16 軌道：
  A-only 6、B-only 8、A/B 同拒絕 2；拒絕分別由原 A 強迫色鏈
  與原 B 內邊的相同 singleton list 證成。
- 精確公式為 `J=P ∧ b2≠b4 ∧ |{a0,a1,a2,a3}|≤3 ∧
  (a2≠b4 或 b0=b2)`。三條條件各有不可省略例，保存八個條件
  子集合的全部假接受軌道；不宣稱所有可能摘要的最小表示。
- 紙面充分性依完整 R127／R167 公式及原來源內部互斥接合；
  Python 完整集合另核對。未新增 Lean／`native_decide` theorem，
  一般幾何接合政策、多步摘要與 `K∞=K≤5` 未改變。

新 artifact 為 642,664 bytes，未達大型檔門檻。更新兩份前置報告的
後續狀態、兩點／state 導覽及 STATUS 報告／歷史直接索引。
README 入口與 HANDOFF 研究線未變，依 DOCUMENTATION 不逐輪複述。
未啟動 Graphify、sub-agents、來源大枚舉或其他環序搜索。

## 驗證

```bash
python3 scripts/c5_two_vertex_mixed_pullback.py
python3 scripts/c5_two_vertex_mixed_pullback.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_pullback.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

產生及兩次逐 byte 重播通過。原 J 由 `4^8` 賦色與七內點回溯重建，
兩框拉回由具名 natural join 與另一份 `4^8` 完整查詢比對；來源
兩式各檢查全部 `4^5` 賦色。54 份差集軌道的每個失敗條件均有
原邊拒絕證明，108 份分別延拓均逐邊檢查。五項 verifier 負控制
按預期拒絕：刪掉遺失原邊、錯誤強迫色、刪掉 B 衝突邊、改動
共享點顏色及把單框 witness 當成完整 U witness。

兩份混合框 checker 與既有六份接合／四個來源代表皆重播通過。
`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；未修改 Lean。

文件檢查通過 378 份 Markdown／3,845 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 與全部 24 份未追蹤文字檔的最終換行／尾端空白
檢查通過。

未重跑來源大枚舉、目錄最小性、獨立主例及正反向拓撲 checker、
1,320 份點對索引或 Lean axiom audit；兩混合框 checker 已重驗
各自使用的原 rotation 及小代表。未改動舊 scripts／artifacts，
未操作 Git index，保留全部前輪成果。

下一窄題為此固定 J 的跨框 arity：兩框加上全部三點投影是否足夠，
若否保存剩餘差集及其每份三點延拓。此輪未計算該問題。
