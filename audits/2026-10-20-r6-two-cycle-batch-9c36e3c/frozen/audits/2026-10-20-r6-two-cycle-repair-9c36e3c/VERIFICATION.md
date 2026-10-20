# 驗證範圍與收據

2026-10-20；BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。

## 紙證與來源邊界

[A 審核](A/REVIEW.md)、[B 審核](B/REVIEW.md)及
[C 交叉審查](C/CROSS_REVIEW.md)獨立核對字面 f/z 扇區、
全部補圈分解、原 rotation 的完整對偶面識別、附樹度和及 13-state 同 O 接合。
審核採納任意大小條件修復；沒有採納來源普遍觸發。
初稿主圈描述曾漏說跳弧端點屬於被切下的完整圈，已在交叉審查中修正。

14 份輸入均以精確 BASE bytes 凍結；原 13 份見 [INPUTS](INPUTS.json)，
額外原 J 幾何見 [B inputs](B/INPUTS.json)。
`check_inputs.py` 同時核對凍結副本、Git BASE 與不可變 live authority。
docs 的 live routing 漂移允許，仍核對其原 BASE 副本。

## 完整有限重播

```sh
python3 -B audits/2026-10-20-r6-two-cycle-repair-9c36e3c/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-two-cycle-repair-9c36e3c/check.py
```

A 以局部內邊直接枚舉，保全部 32 個 spoke masks、15 個 matching fragments
及 13 個局部無奇圈 states；再將完整 PM 遞迴與同一 O 的選邊組裝比較，
四圖共 160 個 PM 均逐完整補圈核對。
B 另獨立重建全部局部 states，見 [independent-check](B/independent-check.json)。
C 保八個 complete marked fibres、每個完整補圈、實際差分批次、原 sphere
rotation 與全部 e-zero Tait rows；active 證書為
[certificate-v2](C/certificate-v2.json)，舊開發證書不覆寫。

子審核的正常／seed17 與污染收據：
[A verification](A/VERIFICATION.json)、[C verification](C/VERIFICATION-v2.json)。
污染涵蓋刪空 fibre、改完整路長、丟完整補圈、改原 z、改跳弧奇偶；
exclusive-create 第二次寫入拒絕。
根層另實際餵入缺權威與缺空 mask 的檔案，兩者皆 exit 1：
[negative checks](negative-checks.json)。

根層首輪正常／seed17 收據見 [checks](checks.json)；
它是在 A 補齊四圖交叉比對前執行，保留該時輸出不覆寫。
最終版本、文件及產物檢查的逐命令收據見 [final checks](final-checks.json)。
所有有限 PASS 僅屬固定圖和接口；來源實現仍 `not triggered`。

## 工作樹檢查與未重跑項目

原 `2026-10-17-r6-two-cycle-cap-3d325d7/check.py` 本輪只讀重播通過：
七稜柱 28 個偶補參考、另一控制 5 個，凍結漂移零。
原 checker 不驗本輪新增條件修復。

本輪 `lake build` exit 0，8832 jobs，僅有既有 AttachmentOrder／SymRelabel
linter warnings；沒有修改 Lean、沒有新增 theorem。
此結果由工具執行紀錄取得，完整 lake stdout 未另存為 audit log。

文件連結、formal docs DocGraph、本 audit 排除 frozen 副本的 scoped DocGraph、
產物政策與 whitespace 的實際結果以 final checks 為準。
最終七項命令全部 exit 0；正常／seed17 stdout bytes 相同。
正式文件檢查涵蓋 702 份 Markdown、9241 條本地連結；
formal DocGraph 為 97 份 metadata 文件、383 關係，無錯誤。
本 audit 沒有宣告 DocGraph metadata，scoped check 的 0 文件／0 錯誤
不承擔其紙證或一般 Markdown 連結權威。
另用既有 Markdown parser 核對本 audit 的 9 份新報告、41 條本地連結／錨點，
並查新 Python／Markdown whitespace 及所有單檔大小，見
[delivery check](delivery-check.json)。最大檔 350894 bytes。
產物政策檢查只涵蓋 indexed files，未把未 stage 的新 audit 假算為 indexed 通過。

首輪額外檔案格式檢查把末尾換行規則套到已有污染 JSON，因七份負控制無
末尾換行而 exit 1；[失敗收據](delivery-attempt1.json)保留。
沒有改寫負控制 bytes；修正檢查範圍為 Python／Markdown 後通過。
不重跑大型來源枚舉、既有九框計數、全部工具測試或全工作樹 DocGraph；
沒有聲稱全工作樹 DocGraph 通過。

同時出現的其他獨立 audit 及其文件更動不屬本輪。檢查整份共享文件時，
會保留其最新內容；本輪只改兩圈子題及相關路由，沒有 commit／push。
