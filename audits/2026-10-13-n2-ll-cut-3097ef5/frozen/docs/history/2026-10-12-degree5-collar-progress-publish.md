# 五度鄰環、外圈限制與產物儲存整理發布

2026-10-12。使用者授權「整理目前進展 commit + push」。
起點 HEAD 為 `bc7c0820e6b5e585869b8a59e04f52da0dad2d33`，
origin/main 為 `5d70a39940182ea37c9ca5d36d9ebb7f612160ad`。
本次推送包含尚未推送的度數界提交及以下 connected 整理；最終 SHA 以 Git 為準。

## 採納與精確界線

[全內部五輪及 A／B／C 入口](../c5_degree5_link_reductions.md) 接入四份隔離交付；
[完整外圈入口](../c5_neartri_boundary_collar.md) 接入近三角化來源限制。
所有原 BASE、凍結副本、v1／v2 證書、失敗及負控制保存原 bytes。

- 最小來源必有全內部 induced W5；每個 C4 的有界內部空、proper C5 最多包住一個輪中心。
- A 完成九種位置及完整 pinned 替換契約；來源只留 m=0、m=1、相鄰 m=2。
- B 完成 1,020 項固定域合法操作，沒有保持完整 Σ 的操作；不推成一般不可能性。
- C 的 17,424 組有序 cap pairs 得 66 種 K 內輸出；完整 joints／fibres／literal DFS 相同。
- 933 的 h≥3、n5≥9；941 的 h≥2、n5≥8。h=2 只剩具名 C7 的55列必要上界，非實現。

實際 933／941 最小來源均 `not triggered`，普遍結論依明列的紙面前提。
目前義務是同一 B/U 色框下 annulus 完整 J_p 的縮減或聯集分解；C7 可實現性、
h≥3、跨邊 J_e 同步、十三內點以上、一般 K∞=K≤5 及新 Lean 化均 OPEN。
E-ARC2／N2 的 edge-critical 身份與九格覆蓋未由本批結論改動。

## 產物儲存與歷史證據

[生成產物 CI 紀錄](../../audits/2026-10-12-generated-artifact-ci/REPORT.md)
與新的 index 儲存檢查一起發布。實際生成仍 **PARTIAL**：137／160支產生器、
143／166份主要產物重建一致；一支 mixed-core provenance mismatch、21支下游
blocked、一支 finite-search 環境限制 unverified。沒有為發布重跑整批生成或更新失敗 hash。

既有 staged 的26份原檔移出 Git 前，已逐份核對 HEAD、本地 bytes／mode 與 gzip 還原。
本批另選定七份≥1MB audit JSON、一份保留歷史空白的 review 及原CRLF操作CSV，
append 九份封存，原始 bytes 合計89,701,682、gzip合計5,317,539；
原檔留在本地，舊證書及CSV行尾不改寫。
原 scratch 的度數界探索及附加 small-cap 校準以明列小檔加入；不納入既有大型 ignored 輸出。
新 checkout 執行 `python3 tools/audit_archive.py restore --artifacts` 後再重播。

## 本次驗證

六項正常模式權威重播均 exit 0：deep-wheel、A v2、B v2、C、neartri 主 checker、
collar checker。五包 MANIFEST 逐檔 SHA256 全數相同，既有 seed17／負控制／獨立
審查紀錄沿用；沒有重跑上游大型枚舉、外部計數證書或所有 seed17 控制。

| 重播 | 本次核對範圍 |
| --- | --- |
| Deep-wheel | 240 full boundary fibres、122 short cycles、Σ1023 控制 |
| A v2 | 九個 literal 骨架、362 合法循環接觸編碼、十列完整 fibres |
| B v2 | 1,020操作、10,200項 operation full-lift identities、零Σ等價操作 |
| C | 17,424 pairs、174,240列、657,432 joints、2,606,752 lifts、24,082空列 |
| Neartri | 924完整接合、9,240具名幾何；21環帶／42項閉包只留一項 |

工具單元測試56項 PASS；`tools/artifacts.py status` 的166份主要產物 fingerprint
PASS，不能代替前述生成PARTIAL。儲存CI及完整封存驗證PASS。
文件檢查PASS（634 Markdown／7,886本地連結）、正式docs DocGraph PASS
（62 documents／213 relations）；`lake build` PASS（8,831 jobs，既有linter warnings）。
`git diff --cached --check` PASS。全工作樹DocGraph FAIL：保留歷史快照造成62項
duplicate-ID errors，與正式docs結果分開，未刪舊快照消除診斷。

## 文件傳播

Updated：新 canonical 入口、Kempe guide、STATUS、原任務頁；共面正規形、
度數界及外圈報告加入後續狀態，區分 C 的紙面來源排除與獨立有限計算完成。
Reviewed-unchanged：HANDOFF 沒有線增減，STATUS_HISTORY 保存舊快照；舊 E-ARC2／N2、
degree-5／R 身份及 Lean guide 沒有取得新前提或新 theorem，故不更動其結論。
README 的修改只接入產物操作／CI及生成PARTIAL界線。
Propagation stop：L2；一般父命題仍 OPEN。

提交採 connected 明列白名單；推送後核對 HEAD、origin/main、遠端 main 及工作樹狀態。
