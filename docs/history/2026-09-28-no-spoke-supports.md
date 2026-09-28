# 2026-09-28：no-spoke 環狀支援與 (2,1,1,1) 指定分離

接手 HEAD `2de13f78602b2267376c5eb08ee2957603d549b5` 的既有未提交工作樹，
保留 residual-locality、three-one、four、no-spoke-exterior 的全部產物與
文件修改。本輪沒有 commit／push；優先序見 [HANDOFF](../HANDOFF.md)。

## 結果與證據

[新報告](../c5_no_spoke_supports.md) 從 72 份必要禁色覆蓋推進：

1. 任意大小的 annulus／Jordan 論證保留原分量、五個原接點與全部實際
   boundary 附件，給跨度總和≤5 的環狀區塊序；沒有添加 spoke。
2. (2,1,1,1) 的四個禁色角色只容四種支援配置，兩種有具體 T4 拒絕
   見證；保留兩種、48 筆具名記錄。36 筆雙列由色對稱／容量得到，
   另外 12 個查詢由不同原分量的外部雙路徑 completion 關閉。
3. (2,1,1,1) 的指定雙列分離接回條件式單側出口；失敗側唯一 degree-5
   只剩 t=0 的 (2,2,1)。這不是排除所有 (2,1,1,1) 來源或完整 Σ 分類。
4. (2,2,1) 有 1,952 筆必要支援，T4 排除 1,336，保留 616；其中
   268 筆雙列已證。788 個接受、348 個未決、96 個條件式拒絕查詢。
   條件式拒絕不是可實現來源或反例；尚未完成此分拆。

新 checker 用整數提升、cyclic hull 邊 mask 兩套枚舉獨立核對幾何域；
重播 15／65,535 份非空 unary／binary 完整關係、既有 root 局部歸納及
3,492 份 completion 全接線；另保留原具名接點環序與字面反射 targets。
前序 artifacts 只讀，SHA256 綁定所有直接使用的計算輸入。

任意大小覆蓋仍是紙面證明，使用外部 degree-list 定理及既有 degree-4
分類；本輪核對 Dvořák 講義 Lemma 7／Theorem 10 原文。沒有新增 Lean
theorem，也沒有把 finite support 型當作 disk 可實現性證書。

## 驗證範圍

下列四支 checker 全部通過，新 JSON 逐 byte 重算一致。

```bash
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 成功（8,827 jobs），僅有既存 AttachmentOrder／SymRelabel
linter warnings。文件檢查通過 213 份 Markdown，DocGraph 通過 31 份
metadata 文件／75 條關係／5 families；HANDOFF 保持 150 行。
`git diff --check` 及新增四檔的逐行 whitespace 檢查均通過。

未重跑 single-spoke (2,2) 中間鏈、two-spoke 全表、雙拒絕 atlas、
R 系列大覆蓋、一般 profiles／閉包或 Lean axiom audit。
文件檢查不驗證數學；`lake build` 不形式化本輪紙面圖層定理。

## 精確停止點

新表 record 599（zero-based），分拆 (2,2,1)，
q 下禁色 ({0,1},{0,2},{3})、支援 (012,04,234)。p₁ 已可取 z=2。
若 p₂ 拒絕，原 C₀ 的有序關係須由 q 的 {(0,1),(1,0)} 變為
p₂ 的 {(1,3),(3,1)}。C₁ 在 p₂ 禁 {0,2}，單接點 C₂ 的 F 在 p₂
為空；下一步比較同一 C₀ 的跨列 palettes，保留 C₁／C₂ 實際外部路徑。
其餘必要表、來源可實現性、degree≥6、多 degree-5、一般出口及主命題
仍開放；本輪未重開來源圖枚舉。
