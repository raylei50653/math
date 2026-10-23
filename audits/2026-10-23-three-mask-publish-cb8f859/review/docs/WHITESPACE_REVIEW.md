# Frozen whitespace 處理覆審

2026-10-23；唯讀重現。**處理 PASS，完整檢查仍為 FAIL；不得將 scoped PASS 改寫成全域通過。**

`git diff --cached --check` 精確只有：

```text
audits/2026-10-23-three-mask-round2-cb8f859/933/runs/negative-authority-root/audits/2026-10-23-three-mask-methods-cb8f859/933/REPORT.md:139: new blank line at EOF.
audits/2026-10-23-three-mask-round5-cb8f859/941/check.py:218: new blank line at EOF.
```

兩份完整bytes／SHA均吻合publication BASE。第一份10255 bytes是有意污染的authority副本（原authority為10254 bytes），用來讓checker拒絕current-authority drift；round2/933/VERIFICATION.json:8記錄該反控制成功，不能修EOF而破壞其語義。第二份15303 bytes是原round5/941 checker，亦在738份凍結域內。

保留兩檔原bytes及full FAIL，再只排除以上兩個完整path，對其餘index做whitespace檢查，fresh重播exit0。無需改原audit，也不宜整個排除frozen／audit目錄。精確argv、return codes、stdout及兩份BASE records見 [whitespace-receipt.json](whitespace-receipt.json)。

此scope例外只關whitespace，不免除兩檔SHA／內容／checkers的驗證，也不是generated-artifact政策例外。本review未改index；parent在先前文件審核snapshot之後執行stage，與 [receipt.json](receipt.json)記錄的該次審核區間index未變不衝突。五份dirty docs、history、README／HANDOFF及治理文件的九份受審hash目前仍全部匹配。
