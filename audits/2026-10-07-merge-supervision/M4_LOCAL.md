# M4-L：正式交付整合與最終本地提交

前序：M1／M2已驗收；M3新增provenance補件經[監督驗收](REPORT.md)閉合，
原strict FAIL仍保留。受驗候選 `ba0b447f09617591d9f2ba81c988f537af771791`，
main基準 `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`。

**可直接發布的任務：** 整合現有audit與監督補件，完成本地交付／commit；
停止於回傳最終SHA，不push、不建立PR、不觸發CI、不merge。
不新證明U2–U4、不擴大k、不改寫候選producer或歷史證書消除FAIL。

## 納入與紀錄

1. 明確路徑納入M2原40檔與DELIVERY、M3原264檔與BUNDLE_INVENTORY、
   本監督報告／程式／新重播輸出；保留原bytes／hash。不要staging scratch交付clone或cache。
2. 依文件治理補STATUS直接報告／歷史入口、相關導覽的audit驗收入口與信任界線，
   不擴張現有數學结論；HANDOFF沒有研究線變更則保持薄入口。
3. 新發布紀錄與驗證ledger明列：原29指定28PASS／1FAIL；C44 input presence、
   E5 branches新hash例外；E4／E5 controls／E4C三份歷史byte FAIL；86項歷史whitespace。
   每項保存實際exit、source／fresh hash、具名leaf allowlist、其餘完整payload相等證據。
   不將本文或M3的metadata診斷改寫為原strict PASS。
4. 查找M1／前次監督/tmp證據的原副本；存在則按原hash保存，沒有則如實記為不可用。
   使用監督的新17blob清單與M3同候選fresh驗證作可核對的新證據；若補跑必要checks，
   使用fresh logs並標「現在重跑」，不能冒稱原M1或前次監督執行輸出。
5. 原helper中/tmp位置屬歷史執行紀錄，不改原M3 bundle。
   為新checkout提供可攜命令／新驗證入口：顯式repo／source／output，
   M3 check_bundle可用`PYTHONPATH=<repo>/scripts`，LC parser顯式`--source`。
   input candidate SHA、tested source hashes與最終commit SHA分欄，不混用parent與main base。

## 驗證與停止點

提交前核對M2／M3原manifest、監督輸出及原來源零byte漂移，並驗新code語法、
新檔whitespace、文件／anchors／index、全新獨立checkout的預設DocGraph。
本地整合工作樹因scratch造成的62 duplicate-id可原樣留存，不能說全工作樹DocGraph通過。
檢查新增候選差異及整分支例外，原86診斷與新增診斷分開。

如果只增加audit／驗收文件，原已核對的數學來源、Lean來源／設定／產物hash全同，
可沿用M3的顯式build及558公理證據，列明未重跑與實際hash。
任何受驗producer、數學前提、corpus、Lean來源／設定／產物變更均須重驗受影響項。
guide／mixed-spokes文件再改可能增加provenance值漂移：必須fresh逐欄診斷、保存新hash，
不得整批忽略provenance，不將先前M3結果混稱最終字句版本重播。

建立本地最終提交後，從該SHA的獨立checkout核對正式驗證包、還原路徑和文件入口；
新執行紀錄如需納入另一提交，回傳其後真正最終SHA及受影響文件重驗。
只有本任務已驗收才進M4-R；此任務不宣告可合併。

## 統一回報

```text
任務：M4-L
候選base SHA／main基準／最終交付SHA：
納入檔案／diffstat／大小與SHA256清單：
M2、M3及監督原bytes／來源漂移：
原/tmp證據追回／不可用／fresh替代驗證的明確分類：
五項strict FAIL及86項whitespace的精確處置：
最終文件／DocGraph／new diff／manifest checks及logs：
沿用M3 LC證據的hash理由／實際未跑項：
新的findings／未解交付缺口：
確認未push／PR／CI dispatch／merge：
```
