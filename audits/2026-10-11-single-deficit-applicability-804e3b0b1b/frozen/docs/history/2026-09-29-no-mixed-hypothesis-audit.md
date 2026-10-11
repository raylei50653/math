# 三 agent 驗證：完整搬運、單框點與守恆 palettes

2026-09-29，起始 Git `0ab88ce`。使用者要求開三個 agent 分別驗證先前
提出的三項假設；主 agent 審閱、補獨立 pair-domain 核對並整合本輪證據。
成果及目前界線見[專題報告](../c5_no_mixed_hypothesis_audit.md)，研究線
入口見[導覽](../c5_weak_deletion_guide.md)。

## 分工與結果

- `transport_criterion`：H 充分條件的完整紙面證明及 G 弱化；既有
  4,164 查詢中 H/G 分別通過 2,932/2,936。四個嚴格性控制全在 AC。
- `singleton_locality`：共同 ordered lifts 下，所有 actual support
  含變動框點 h 的分量至多兩份；精確共同介面保留 root-spokes。兩份
  可同接一 root；不能把未知關係集中誤當幾何證據也只需這兩份分量。
- `palette_switch`：1,780 個守恆 singleton 的 target pair 上界全排除；
  890 固定色矛盾，850 零 β，40 單 β 後作原路徑交換。這是表依賴
  推論，尚未證免分類的換色阻斷機制。

主 agent 將三份程式調整為 repo 相對 ROOT 與新 artifact 目錄，再重播。
Palette checker 另獨立從 24 個色置換／target 支援穩定子重建全部
二元候選，逐分量確認保存 joins 沒有漏候選；確認字面 target 與最終
接受狀態。未改舊必要支援或十五類證書。新增 source 排除及 target
接受均為零。新 palette JSON 每 β 保存一份完整原路徑／框弧見證，
其餘替代見證以數量及 hash 綁定，重播仍全部重新計算。

## 主 agent 實跑

以下通過，三份新 JSON 先以無 `--check` 的相同程式生成：

```bash
python3 scripts/c5_no_mixed_hypothesis_transport.py --check
python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
python3 scripts/c5_no_mixed_span_budget.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
lake build
```

新 JSON 重播逐 byte 相同。舊跨度表重播 5,842 必要支援／4,164 接受；
AA 重播 644 查詢／2,892 joins，AB 重播 1,120 查詢／3,148 joins。
`lake build` 完成 8,827 jobs，保留既有長行、unused simp 與 show tactic
警告；没有新 Lean theorem。

第 3 agent 另重播 `python3 scripts/c5_single_spoke_branch_palettes.py --check`
通過，並在暫存版 audit 使用 `PYTHONHASHSEED=7` 逐 byte 比對。

文件檢查通過：Markdown 連結／錨點及直接索引、DocGraph 62 文件／213
relations、`git diff --check` 均無錯誤。

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

## 沿用、未重跑與停止點

未重跑其餘十二類完成 checker、舊圖枚舉或全庫所有 Python 控制；新
audits 直接讀七類保存資料，以 input SHA 綁定，不把讀取資料說成重跑
其全部生成／原圖證明。既有任意大小支援覆蓋、拓撲引理及外部 degree-list
定理明示沿用。Lean build 不證新紙面拓撲、來源實現或完整 Σ。

下一窄問題是固定外部完整關係後，對 h 附近一或兩份原分量證明共同
跨列相容規則；AA54 與 AB22 保留為守恆／非守恆控制。共同 repair、
一般出口與 K∞=K≤5 仍未證。本輪未要求 commit 或 push。

## 後續提交與發布核對

使用者後續要求 `commit + push`，本次提交收錄三份 checker／JSON、專題
報告、本歷史紀錄及 README／STATUS／weak-deletion 導覽與跨度總覽連結。
研究線與進行中標記未改，依文件治理規則不改 HANDOFF 的導覽清單。

發布前重播三份新 checker 的 `--check` 並核對文件／DocGraph 與 diff。
上一階段同一份程式及證書已通過 hash seed 17、三份相關既有 checker
與 `lake build`；發布階段沿用這些結果，不重跑無變更的 Lean 或舊圖枚舉。
推送後核對 HEAD、origin/main、遠端 main SHA 一致及工作樹乾淨，最終
提交 SHA 與核對結果以即時 Git 及本次回覆為準。
