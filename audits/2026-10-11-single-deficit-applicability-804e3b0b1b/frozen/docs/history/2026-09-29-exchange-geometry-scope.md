# 2026-09-29：交換或幾何阻斷的適用範圍遍歷

Git 基準 `f29b899`，工作目錄為專案根目錄。
使用者要求遍歷機制假設的適用範圍；本輪以現有必要資料作範圍稽核，
保留進場已有的 t2-t1 bridge／endpoints、t2-t0 singles 未提交 bundle。
新增 [checker](../../scripts/c5_exchange_geometry_scope.py)、
[JSON／生成表](../../artifacts/c5_exchange_geometry_scope/scope_table.md) 與
[報告](../c5_exchange_geometry_scope.md)，接入 root 預算、README、STATUS、HANDOFF。
未修改既有 scripts／artifacts，未 commit／push。

## 結果與界線

- 原 118 份側資料／3,548 份有序接合分成五種預算側型、25 格、15 種 root 交換型。
  已完成三型涵蓋 552 份；其餘 2,996 份仍未建立完整支援／rotation 覆蓋。
- 三份既有表合計 1,002 份支援、2,004 個 target、6,376 組完整候選 joins。
  獨立 16 色對枚舉核對每組 Z，再重算 306 組原失敗候選的反證：
  142 固定框弧／支援、34 首橋、126 原雙端點、4 全路徑交換。
  target 層依序為 1,754 直接接受、86／34／126／4 由後續層完成。
- 新遍歷四色、奇數長 1／3／5／7、全部交替 edge words、四種旁支的
  1,920 份抽象 Gallai lists，皆保存完整有序端點 relation：
  192 份奇數 palette 恒定者有第二禁色；1,728 份變動者只有 source 禁色。
  它們沒有 C5 附件／完整 degree 的來源保證，不能當 disk 反例。
- record 22／p₂ 再核對「d 不守恆、首橋不適用，但雙端點能排除」；
  (2,3,1) 與 (2,3,2) 的完整 relation 再核對首橋不足。

新增 target 結論／來源排除均為零。一般 A 完備性、全分拆、root 樹分離、
完整 Σ 與 K∞=K≤5 均未因此證成；紙面／外部定理證據沿用原報告，未新增 Lean theorem。

## 本輪驗證

以下六個 checker 以 `--check` 重播全部通過，生成內容逐 byte 相同。
`lake build` 通過；文件檢查通過（300 份 Markdown、3,203 個本地連結），
DocGraph 通過（60 文件、199 關係、5 families，0 errors／notes），
HANDOFF 保持 150 行，`git diff --check` 通過。

```bash
python3 scripts/c5_exchange_geometry_scope.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未單獨重跑 t2 初層／bridge／endpoints、t2-t1 初層／bridge 的完整控制鏈；
本輪新 checker 重算其 target 反證並核對輸入 hash，與重播完整 controls 分開。
未重跑 mixed、唯一 degree-5 表、雙拒絕 atlas、R 系列、profiles／閉包或 Lean axiom audit。
沒有擴大 disk 圖枚舉，也未重讀外部 degree-list 講義；沿用已報告的紙面前提與結論。

## 下一入口

依 [HANDOFF](../HANDOFF.md)，仍從 t_z=2,(2)、t_w=0,(2,2)、D_w=1、O_w=0 的
96 份開始 actual-support／rotation 覆蓋；首項 retained-join ID=3036、sides=(133,16)。
此型有 source 飽和二禁色分量，不能照抄 singleton 的「第二禁色矛盾」。
共 12 種未完成交換型（包含另 96 份重疊型）及更一般骨架保留。
