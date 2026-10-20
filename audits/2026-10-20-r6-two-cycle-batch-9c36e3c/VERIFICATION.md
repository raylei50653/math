# 驗證範圍、重播及證據權威

2026-10-20；Git BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。

## 凍結與紙證

[INPUTS](INPUTS.json)記錄當輪初始工作樹的 104 份完整 bytes 與 SHA。
前輪 audit 當時尚未 commit，不能把這些 bytes 說成來自 Git BASE；
其內嵌前輪 BASE 證據另由原 checker 重播。
本輪 `check_inputs.py` 核對 manifest 本身、完整檔案集合、凍結 bytes
及不可變 live 證據；只允許最外層 routing 文件的 live 漂移。
根層正常／seed17 重播時，不可變證據漂移為零。

任意大小紙證的獨立推導及審閱為
[A proof](A/PROOF.md)、[B proof](B/PROOF.md)、
[A review](A/REVIEW.md)、[B review](B/REVIEW.md)、
[C review](C/CROSS_REVIEW.md)。
審閱中修正一處敘述：三分量 charges `(1,1,0)` 本身不足以推出兩個奇圈；
須用恰兩個完整補圈及 cubic D 的偶數階，才得兩圈皆奇。
修正已納入 B 紙證，沒有藉控制取代任意大小論證。

## 完整有限重播

```sh
python3 -B audits/2026-10-20-r6-two-cycle-batch-9c36e3c/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-two-cycle-batch-9c36e3c/check.py
```

根 checker 依序核對 custody、C 完整有限證書、A 獨立重建與前輪 checker。
它沒有來源輸入模式，也不驗證任意大小紙證或來源必然存在的見證。

七個固定圖合計 275 個完整匹配、16,384 個原頂點集合模補集，
224 個 spoke fibres 及 56 個標記 fibres，均包含空者。
每個合法集合與同圖完整匹配一一對應；每個匹配保全部完整補圈、
完整 primal 分量及區域樹每邊的整側 degree charge。
C 另記九個具有局部字面 incidence 的候選配對。

A 不匯入 C 函式，從原 rotation 重新建面、primal 邊與全部 275 個匹配。
它檢查十個 graph-level 候選配對，其中一個屬不具字面 incidence 的舊弱控制且不合法；
其餘九個與 C 一致。六個配對可交替翻轉，三個通過完整偶性。
正常／seed17 獨立結果見
[normal](A/independent-check.json)、[seed17](A/independent-check-seed17.json)。

根層實際命令、exit codes 與輸出 SHA 見 [replay checks](replay-checks.json)。
正常／seed17 都 exit 0，stdout bytes 相同。
缺權威 manifest 及漏掉完整外側奇圈兩種污染經根 CLI 都 exit 1。
C 的九項負控制包含改分量／整側奇偶、漏空 fibre、虛構 cut、
漏未接合奇分量、改字面標記、改來源權威及 exclusive-create 覆寫拒絕；
見 [C verification](C/VERIFICATION.json)。A 另拒絕缺匹配與改 rotation。

[active certificate](C/certificate.json.gz)採 deterministic gzip。
初稿完整 bytes 也以 [initial archive](C/certificate-initial.json.gz)保留，
未以新稿覆寫；壓縮前 bytes／SHA 見 C verification。
壓縮只處理儲存大小，不縮減 fibres 或完整匹配內容。

所有控制均非完整原來源。即使局部符合 5／5／5，
也未滿足全部來源度數、簡單性、G/U319 與接回要求。
來源實現統一 `not triggered`。

## 工作樹與文件檢查

本輪 `lake build` exit 0、8832 jobs；保留既有 linter warnings。
完整命令、stdout／stderr 與 SHA 見 [lake check](lake-check.json)。
未修改 Lean，沒有新 theorem。

文件連結、formal-docs DocGraph、產物政策及 whitespace 的實際命令與結果
另記於本目錄 `delivery-checks.json`；新 audit 自身的普通 Markdown
連結／錨點、Python／Markdown whitespace 及單檔大小另記 `audit-delivery.json`。
產物政策工具只檢查 Git index；本輪另量測未 stage 新檔，不把 index PASS
誤稱為新 audit 已納入 index。

沒有重跑大型來源枚舉、其他分支的數學 checkers、全部工具測試或全工作樹 DocGraph。
前輪 checker 的重播涵蓋其 14 份權威、32 masks、13 個無內部奇圈 states 及四控制，
不代表以它驗證本輪新紙證。

共享導覽在本輪期間另有獨立 941 更新；本輪只替換兩圈子題，
修改前最新版本保存在 `routing-before/docs/`。初始凍結版本保持原 bytes。
README／HANDOFF 的研究線與 tag 未變，按文件治理核對後不作逐輪摘要。
未 commit、未 push。
