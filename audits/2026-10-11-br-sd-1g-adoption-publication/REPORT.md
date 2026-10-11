# BR-SD-1g 正式採納與發布證據

Owner 已批准精確採納、文件同步及驗證後的 main commit／push；基準
`c15a635e17d4be814e19aeeeeb765f3d6024099a`。已採納的完整八項合同見
[canonical](../../docs/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)，
歷史、依賴及同步範圍見 [新紀錄](../../docs/history/2026-10-11-br-sd-1g-adoption.md)。

BR-SD-1g 精確子域 ACCEPTED；actual source NOT TRIGGERED；完整父身份 OPEN；
新增 Lean theorem 0；新增完整 OPEN 無條件關閉 0。其餘身份不升級。
本次不新增研究證明，只回寫已經獨立審查的紙面結果。

## 授權、輸入與不可變資料

[AUTHORIZATION](AUTHORIZATION.json) 固定 owner 授權、五份既有文件及一份新 history 的範圍。
原研究160檔、publication6檔、31 frozen authority、313舊 frozen（309 tracked、4既有 ignored/local-only）、
全部既有 seals 與完整281檔獨立採納審查保持 bytes／modes。
[review custody](inputs/REVIEW_AUDIT_CUSTODY.json) 捕捉本次開始時完整281檔。
HANDOFF、STATUS_HISTORY及其他直接 consumer 的 reviewed-unchanged 理由由
[mapping review](mapping/REVIEW.md) 保存。

## 實際檢查

在新增本目錄或改文件之前的七項實際重播見 [PREFLIGHT](logs/PREFLIGHT.json)：
sealed review 正常／seed17 exit0；seal七項負控制 harness exit0；
歷史 publication verifier 正常／seed17 **exit1**；原 independent immutable adapter 正常／seed17 **exit0**。
歷史 exit1 是固定兩目錄白名單拒絕新增獨立審查，不是紙面 finding；保原命令與 stderr，未改 verifier。
文件採納後由本目錄的新獨立相容性 checker 支持已批准 descendant publication，
不以 monkeypatch／import／改寫歷史 verifier 製造 PASS。

採納後的完整實際結果見 [CHECKS](CHECKS.json)：35項成功或符合預期的原始收據，
另保留2項失敗嘗試及同命令成功重播，沒有改 exit code 或 expected code。

| 實際執行 | Exit／適用範圍 |
| --- | --- |
| Fresh independent finite、原 independent、原 primary，正常／seed17 | 六次exit0；三對stdout完全相同，僅六份具名synthetic fixtures |
| 原／fresh三套solver × corrupted／malformed／marginal-corrupted | 九次expected exit1；只校準證書拒絕 |
| 原mapping degree calibration正常／seed17 | 二次exit0，stdout相同；具名degree表，非source realization |
| 新 immutable adoption adapter正常／seed17 | 二次exit0，stdout相同；完整immutable及六份已批准live文件核對 |
| 新manifest memory controls | harness exit0；valid positive exit0，九份具名corruptions各expected exit1，protected bytes不变 |
| Logger disposable controls | harness exit0；regular positive0、symlink logs／parent escape／sealed refusal各expected2，未越界寫入 |
| `scripts/check_docs.py` | 最終exit0，603Markdown／7446local links；首輪missing mapping review的exit1保留 |
| DocGraph `--include 'docs/**/*.md' check` | exit0，62documents／213relations／5families，0errors／0notes |
| `lake build` | exit0，8831jobs；既有linter warnings保留，沒有新Lean theorem |
| `git diff --check`／normative readback | 各exit0；§1、§2.1–2.10、既有§2.11及HANDOFF／STATUS_HISTORY／README逐字不变 |
| 歷史publication verifier，採納前及文件改後的正常／seed17 | 四次expected exit1；原固定工作区／目錄白名單拒絕本次採納，原stderr保留 |

第一次logger harness的positive fixture漏建其所需logs parent；失敗exit1、原harness v1及
raw receipt均保留，修正fixture後同命令exit0。它沒有改實際logger或歷史證據，沒有來源／紙面finding。
新的logger symlink guard及negative harness具體error理由曾由兩位reviewer核對後修正；
最終工具与所有失敗generation一并纳入本次最終bytes審查。

完整數學／量詞、工具與最終bytes接受見 [proof ACCEPTANCE](proof/ACCEPTANCE.json)，
獨立custody核對見 [custody REVIEW](custody/REVIEW.md)；[SEAL](SEAL.json) 封存全部newpayload
及六份已批准文件hash，只排除seal自己的bytes，不設可繼續改payload的postseal白名單。
Final review／seal 後，所有 stage／commit／push／發布後 readback 的實際收據寫在 repository 外，
封存 payload 不為追加 SHA 或結果而改寫。即時發布 SHA 以 Git 讀回與交付回覆為準。

Finite controls 只證具名 synthetic fixtures；任意有限 Wi 的量詞由已審查紙面證明承擔。
Actual source NOT TRIGGERED；lake build 不表示新增 Lean theorem。

## 停止條件

若需要擴大數學結論、修改 frozen artifacts／歷史 verifier，或出現未經審查額外差異，
停止發布並重新提請裁決。發布前須最終獨立 reviewer 無阻斷 finding，
本次差異精確符合 approved manifest，封存讀回正常／seed17成功。
