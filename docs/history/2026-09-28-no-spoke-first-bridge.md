# 2026-09-28：no-spoke 最後 12 查詢與唯一 degree-5 完成

接手 `main`／`60b98ee`，起始工作區乾淨，local HEAD 與已存在的 origin/main
tracking ref 一致；本輪未另查遠端或 commit／push。
最新優先序見 [HANDOFF](../HANDOFF.md)。

## 結果與接合

從交接 record 84／p₁ 開始，先核對原路徑層的 116 筆／12 查詢，再將
single-spoke 首橋推導逐項搬至 no-spoke：同一 C₀ 的 source singleton
證書與 target pair 路徑在首橋共用 β。β=1、2 分別迫使兩塊都接 01、04，
C₁ 的原 z–b2 路徑給 K5。record 84／1472 的 p₁、408／1561 的 p₂
共四項由此延拓。

其餘八項採同一份三框弧：p₁ 用 012／3／4，p₂ 用 0／123／4。
每塊接前兩弧的供應點可以不同；另一原二接點分量有實際 b4 附件，
用原外部路徑接第三弧。原圖五個 branch sets 的連通、不交及十對鄰接
給任意大小反證，關閉 127／419／1390／1564 的雙列。

[新報告](../c5_no_spoke_first_bridge.md) 及 checker 保存 36 組完整拒絕覆蓋：
24 組沿用舊反證，4 組首橋、8 組固定框弧，新消去 12 組。
來源排除仍 500、保留 ID 集仍 116，沒有新增來源排除，沒有把移出來源
計為延拓。116 筆全部雙列已證、0 查詢未決。

必要表的任意大小覆蓋沿用原環狀支援論證；新表不是圖枚舉或可實現性證書。
結合已完成的 t=0、(2,1,1,1) 及其餘四型排除，唯一 degree-5 全部分支
已接回 [條件式單側出口](../c5_single_sided_exit.md)。來源雙缺失及刪邊
繼承仍是完整 Σ(M)=Ω\{q} 的必要輸入，不由 T4 單獨推出。

## 控制與驗證

八支 task-specific checker 全部通過，新 JSON／表逐 byte 重算一致：

```bash
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新控制含 8,748 個固定色歸納步、48 個緊端點、24 個首橋局部配置、
32 個首橋支援／β、32 個剩餘雙列支援、60 份獨立核對的具名三弧分割。
768 份首橋及 768 份可異供應點的框弧 minor，各核對反射；另有 27 個負控制。
五接點、三原分量、零 spoke 全保留，但 skeletons 不滿足整份 degree/list
來源條件。負控制只核對指定 witness 失效，不宣稱刪邊後整圖平面。

`lake build` 成功（8,827 jobs），只有既存 AttachmentOrder／SymRelabel
linter warnings；沒有新增 Lean theorem。本輪重新核對 Dvořák 講義
Lemma 7／Theorem 10 的 degree-assignment、連通及拒絕前提。
文件檢查通過 220 份 Markdown／2,561 個本地連結；DocGraph 通過
33 份 metadata 文件／82 條關係／5 families。HANDOFF 為 126 行。
`git diff --check` 及五份新增檔案的逐行 whitespace 檢查均通過；
完整表在零查詢時的多餘 EOF 空行已由生成器修正，並重生及重播一致。

未重跑其他 single-spoke 中間鏈、two-spoke 全表、雙拒絕 atlas、R 系列
大覆蓋、一般 profiles／閉包、來源圖枚舉或 Lean axiom audit；它們仍沿用
既有證據。文件檢查與 Lean build 不證明本輪紙面拓撲或外部定理。

## 精確停止點

唯一 degree-5 的指定核心分離已完成。一般失敗側每個 minimal core
須碰全部五個 boundary 點，且含 degree≥6 或至少兩個 degree-5。
下一窄方向選恰兩個相鄰 degree-5 的雙 root 介面：先保留 H−{z,w}
每個原分量與所有具名接點，建立有序 root 色對的精確接合及 minimality
必要條件。此方向尚無新分離定理，不乘兩份 endpoint／root marginals，
不假定單 root 刪邊解除性仍成立。
一般單側／共同出口與 `K∞=K≤5` 仍未證。

## 同日 commit／push 接續

使用者其後要求 `commit + push`。本次提交包含 checker、JSON／完整表、
新報告、研究紀錄、README、HANDOFF、STATUS 與直接依賴報告的後續通知，
共 14 檔；上文「未 commit／push」描述研究完成時的狀態。
研究 source／artifacts 未再修改，沿用同一對話已通過的八支 checker 與
`lake build`；發布前重新檢查文件、DocGraph 與 staged whitespace。
提交訊息為 `Complete no-spoke exits with first-bridge and frame-arc proofs`。
實際遠端發布結果以 Git 與本次回覆的 SHA 核對為準。
