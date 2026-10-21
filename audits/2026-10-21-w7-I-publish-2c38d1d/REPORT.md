# 普通短型 I 的共同義務發布核對

2026-10-21；發布前BASE `2c38d1dcb4490017312467deb19d9da02b7bb2a6`。
本目錄只負責發布保存與重播；數學權威是
[原研究報告](../2026-10-21-w7-I-joint-2c38d1d/REPORT.md)，進展摘要見
[發布紀錄](../../docs/history/2026-10-21-w7-I-joint-publish.md)。

## 保存範圍

[evidence-before.json](evidence-before.json)逐份鎖定51份原研究檔、3,158,326 bytes；
連同父六度checker／證書／BASE及其九份frozen輸入，共63份來源、8,613,718 bytes。
原首證、v2、失敗與拒絕紀錄、全部七點lift、空fibres、完整cap assignments均保留。
既有gzip證書直接Git保存；沒有更改ARCHIVE、原blob、生成檔例外或原證書。

原REVIEW／報告的「未commit／push」是研究完成時快照。本目錄與history另記
此次使用者授權的commit + push，不回寫原驗證清單。

## 本次實際驗證

從Git index匯出上述63份來源到獨立臨時根目錄，先逐份核bytes／SHA，再在
該根目錄重播root、geometry、controls、transport四份checker。每份normal與
`PYTHONHASHSEED=17`／optimized均通過、輸出一致，合每模式25個內建負控制。
transport仍核214中間家族、99,009字面像、23,152完整七點kernel、28,987原cap states。
重播沒有借用工作樹未追蹤檔案；[staged-export.json](staged-export.json)記原臨時位置。

`lake build --no-ansi`通過（8832 jobs）；原有linter警告保留。工具測試94項通過。
文件、正式docs DocGraph、暫存whitespace與生成檔政策另作發布前核對；實際
命令、exit code與日誌見[final-checks.json](final-checks.json)。全樹DocGraph仍為
歷史副本的72個duplicate-id，與原研究保存的診斷相同，不列為全域通過。

獨立只讀審查確認原研究SHA、完整來源前提、四個U02單翻後唯一03案例及
各文件OPEN摘要一致；沒有新增配對排除或來源實現。原研究receipt的50項
檔案與兩份子項manifest亦已逐份驗證；所有63份發布來源的漂移為零。

```sh
python3 -B audits/2026-10-21-w7-I-publish-2c38d1d/verify.py
```

此命令核完整發布來源，適用於後續HEAD。原研究的root／geometry／controls
可直接重播；transport仍按父六度BASE的完整frozen bytes核其依賴。沒有對
數學來源重作廣枚舉，沒有新增Lean theorem，`lake build`不形式化新紙證。

## 數學停止點與發布界線

只涵蓋U、V為原E私有點的普通型I。四類替代路至少四邊；混合配對迫私有
色2／3交錯點及條件第五鄰色；02第2／4型翻U02後03唯一。完整二步必要
測試仍留03兩型／02四型，不能將各後繼的獨立survivor拼成來源。

每target八配對同源性、pinched alias、型II、L長路cell、一般W7／J1／J2及
較小bad仍OPEN；原40 profiles仍排38，沒有新完整計數錐或matching結論。
本次只更新相連guide／STATUS及發布入口，HANDOFF活躍線不變。
commit／push成功與即時遠端CI狀態另行核對，不由此報告預先宣稱CI通過。
