# 共面正規形與十二內點界：發布紀錄

2026-10-12。使用者授權 `commit + push`。研究 BASE 與本輪發布前 HEAD 均為
`ab0862485b30b12b538c734271f354630afa8e26`；原 main 已有這份尚未推送的前置提交。
本輪只納入共面研究及其直接文件入口；原工作樹的 generated-artifact 暫存變更保留。
目前發布狀態及提交 SHA 以 Git 為準。

## 採納範圍

[權威入口](../archive/reports/c5/structure/c5_cofacial_normal_form.md) 採納隔離研究的三項紙面結果：

- 聯集封閉目錄與 equality/disequality 分解迫最小來源共面完備。
- global 最少內點、最多邊來源可選成簡單二連通近三角化圖，不增加內點。
- 接 Dvořák–Lidický Corollary 20，得到一般 disk 圖的 `K≤12=K≤5`。

保留 4CT、普遍 Kempe／disk 黏合論證、有限 mask 核對、一般拓撲推導及外部計算
定理的分層。沒有新 Lean theorem，也沒有重新枚舉六至十二內點圖。
`K∞=K≤5`、十三內點以上、一般完整關係重接、N2／E-ARC2 仍 OPEN。

原[隔離報告](../../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/REPORT.md)
與 32 筆 manifest payload 保持原 bytes；其中「未提交／未改共享文件」描述當輪研究
截點。本頁記錄其後的發布接入，沒有改寫歷史證書。

## 文件傳播核對

- Updated：新 canonical 入口、Kempe guide、STATUS；count-cone、Kempe screen、
  boundary-relations、cell enumerator 加日期後續註記。新證據不升格舊 DFS 正確性。
- Reviewed-unchanged：README／HANDOFF 路由與活躍 tag 沒有改變；README 原暫存
  內容不屬本輪。count identities、circulation、B5、dual surgery、Lean guide 的
  既有引理及信任範圍不變。synthesis 的一般主命題與 E 分支仍 OPEN。
- Propagation stop：在直接父題／consumer 層停止；最大邊數正規形不能當作舊
  edge-critical／Gallai／ε 來源的附加前提。

## 驗證與交付

原研究的 root replay 已通過兩份 checker、seed17 與破損證書控制，凍結輸入無漂移。
本輪發布再次核對整份 manifest、紙面審查 SHA、重播及文件檢查；具體命令與結果
保存在 `audits/2026-10-12-cofacial-publication-eb6b2303/`。新發布記錄與原研究 manifest
分開，避免因接入文件而覆寫研究輸入。

發布前實際結果：六次 task replay／負控制符合預期；`check_docs.py` 通過 627
份 Markdown／7,816 個本地連結；正式 docs DocGraph 通過 62 documents／213
relations；`lake build` 與 `git diff --check` 通過。Lean build 只作既有回歸，
不表示新紙面拓撲已形式化。

全工作樹 DocGraph **FAIL**：62 個 duplicate-ID errors，來源為既有 audits／scratch
快照與正式 docs 的重複宣告。本輪新檔案未列於這些錯誤，不刪除舊快照來隱藏失敗。
原研究 manifest 的 32 筆 payload 與發布前 74 份 unrelated staged blob／mode 均已核回。

提交採明列 whitelist。原 74 份 unrelated staged paths 的 blob／mode 會逐项比對，
完整研究快照中被 ignore 規則遮住的檔案也須按 whitelist 納入。推送後核對
`HEAD = origin/main = remote main`；原暫存內容的保留不報成全工作樹 clean。
