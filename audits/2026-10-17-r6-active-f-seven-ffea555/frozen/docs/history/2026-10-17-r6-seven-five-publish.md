# 非面七缺陷五接點修復：目前進展整理與發布

2026-10-17；研究與提交父 BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`。
使用者授權「整理目前進展 commit + push」。本次相連交付完整研究audit、
Kempe導覽／STATUS、三份大型封存證書的精確產物政策例外及發布驗證紀錄。
研究封存中的「未commit／未push」保留當時研究交付語境，後續提交狀態以Git為準。

## 成果與精確停止點

同一原全域最少內點、次級最多邊的no4ct C5來源，原有序外框
`(x,y,a,b,c)`、原x,y,b四度、r六度，固定原支持S∈{932,933,941}，
保留全部原接線、rotation、私人頂點、完整／空U319 fibres與全部原r lifts。
`J=U/(s=t)`、D=J*及字面`e=(vw)*, f=(pq)*, g=(mz)*`不變，不增加原v五度前提。

權威入口為[整合報告](../../audits/2026-10-17-r6-seven-five-repair-5b9a7b3/REPORT.md)
及[完整紙證](../../audits/2026-10-17-r6-seven-five-repair-5b9a7b3/PROOF.md)。

| 項目 | 已證結果 | 邊界 |
| --- | --- | --- |
| 同圖偶補111參考 | 對非面七缺陷五割恰跨一／三條spokes；三-spoke只有六個局部偶補相容狀態 | 完整32列局部關係，包括空fibres；不宣稱任意局部態皆有來源延拓 |
| 真正完整區域下降 | 對D−(M∩M0)不含唯一標記阻斷圈H的分量，翻其中全部差分圈可安全移除全部奇圈，至少下降二 | 任意大小同圖實際批次，外側逐個完整補圈保留；因此聯合最小匹配全部奇圈集中於H區域 |
| 接入marked-six | 101非面七圈含f時，e不可是spoke；Y=X−{a}明確給同含e,f的cyclic六割 | 任意大小位置排除，不需三-spoke或奇數最小性；沒有排掉e在外側的情形 |
| 單圈交換限制 | 安全Q可把完整補圈(7,8,5)換成(15,5)，奇數仍二 | 固定平面校準，沒有主張完整來源、最小性或marked-six前提 |

**三-spoke完整修復仍PARTIAL；H相連殘案、W110+W101>0、omega_e=0及完整319均OPEN。**
主動f七圈的唯一接觸圈Q恰為H，不能用本次固定參考差分批次直接修復。
尚須找其他安全批次，或切開七-cap構造實際同標記小割並證兩側含圈；
整區邊界漏掉內部e或f，不能直接充當所需禁止割。
一-spoke修復、五長、面七圈、九長以上奇圈及一般110↔101交換另保留。
一般K≤22、固定r6的k≥25與k+5接回成本不變。
接續入口見[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)。

## 封存身份與發布檢查

[初始盤點v2](2026-10-17-r6-seven-five-publication/initial-state-v2.json)凍結77個研究audit檔案，
含原SHA256清單、全部紙證、完整證書、開發seal、污染控制及正常／失敗收據。
原76個seal項與全部77份檔案bytes不改寫；另保留研究交付時STATUS與Kempe導覽快照。
STATUS只追加本發布紀錄的索引連結，屬已授權routing變動。

三份A證書超過1 MB：初始開發seal、active `certificate-v2.json`及完整污染控制。
依既有[產物政策](../../tools/generated_artifact_exceptions.json)，新增三個
`kind=frozen`例外，逐份綁定精確bytes、SHA256及保留原因；不放寬政策門檻，
不刪除證據或改寫seal。發布後可用[只讀custody checker](2026-10-17-r6-seven-five-publication/check_custody.py)
核對全部研究檔案、原清單、routing快照與三項政策例外。

[本次有效檢查收據](2026-10-17-r6-seven-five-publication/checks-v2.json)記錄實際命令、exit code及log hash。
研究時正常／seed17、污染與覆寫拒絕、三路紙證獨立審查見
[原驗證紀錄](../../audits/2026-10-17-r6-seven-five-repair-5b9a7b3/VERIFICATION.md)。
發布重播沿用完整證書，分別驗11份BASE輸入、912匹配對／928區域、32完整列及25標記位置。
有限校準不提升為來源實現；真正最小來源供應仍為not triggered。
沒有新增Lean theorem，既有Lean庫建置與新紙證分開記錄。

本次root及A/B/C正常／seed17重播、94項工具測試、Git index產物政策及
`lake build`均通過；Lean僅建置既有8832 jobs。formal／scoped DocGraph均零錯誤。
初次文件檢查將發布用`.md`快照當成正式頁面，因相對連結位置不同而失敗；
改以`.md.snapshot`保存同一原始bytes後重播，活躍盤點為v2。
原[首輪收據](2026-10-17-r6-seven-five-publication/checks.json)及初始盤點保留；
此修正沒有更動任何研究audit檔案或研究seal。

只讀重播：

```sh
python3 -B docs/history/2026-10-17-r6-seven-five-publication/check_custody.py
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/check.py --check
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/check.py
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/B/check.py
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/C/check.py check audits/2026-10-17-r6-seven-five-repair-5b9a7b3/C/certificate.json
python3 -B scripts/check_docs.py
python3 -B tools/check_generated_artifacts.py
```

不重跑舊大型來源枚舉或九框精確計數。正式／有效範圍DocGraph與全樹分開報告；
未宣稱全樹歷史文件無錯。CI同用Git index檢查大型產物，故產物政策在明確stage後驗證。

Updated：本發布紀錄、STATUS歷史索引、三份精確封存政策例外；研究時導覽及索引一併交付。
Reviewed-unchanged：README／HANDOFF研究線與tag、全部原封存證據與一般界。
Propagation stop：研究子案仍PARTIAL，父題仍OPEN，未提升closure或改寫上層摘要。
