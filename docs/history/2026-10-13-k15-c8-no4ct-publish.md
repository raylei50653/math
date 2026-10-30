# K≤15、C8 剝層與無四色定理前提三支接入整理發布

2026-10-13。使用者授權「整理目前進展 commit + push」。整合起點為
`6cafdfb02fe5892a49eee21f92aea2369a25c022`；整理十份既有隔離包，
修正已被後續成果涵蓋的交接停止點，重播相連證據，不擴大研究枚舉。

## 採納範圍與剩餘義務

| 權威入口 | 本次採納 | 剩餘界線 |
| --- | --- | --- |
| [K15-SPHERE](../archive/reports/c5/structure/c5_k15_sphere.md) | 一般有限簡單有序 disk-C5 的 K≤15=K≤5；192球面／2,714根圖／624,617完整lifts | K≤16、任意大小来源及K∞ |
| [C8 剝層](../archive/reports/c5/structure/c5_c8_peeling.md) | 任意大小第一層RING／PINCH／BRIDGE、完整separator轉移；m=10三族16H接八collars全Σ1023，h=3⇒k≥19 | 八項任意大小同圖實現矛盾、m≥11、固定寬度壓縮及h≥4 |
| [無四色定理前提交接](../tasks/c5_no4ct_handoff.md) | 零內點cap下降、受限s<k的C4、直接球面接入K≤15；三支crosscut／外圈與C8依賴修復 | 無界932／933／941、一般主命題及Lean |
| [三支 C8 完整報告](../../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md) | 105查詢排97／留原八項；共同h≥3,n5≥9；932必h≥4,n5≥10；相對N≤k+5商圖可染性接入h=3⇒k≥19 | 必要殘留不是來源實現；h=3界不套到h≥4，不能刪除一般932 |
| [W5 小代表](../../audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md) | 最弱保存為補中心後完整Σ=pr_B R³；102份合法小代表、兩族嚴格替換及χ反控制 | 一般r′≤9存在性、真正最小目錄外來源的縮減；相關構造／條件等價仍明列4CT |
| [singleton 文獻適用性](../../audits/2026-10-13-singleton-literature-6cafdfb/REPORT.md) | 本輪有界查核未找到可直接排除任意大小933／941的已證定理；大小／條件與猜想分開 | 不宣稱不存在其他定理，不新增來源排除 |

一般`K∞=K≤5`、一般單側／共同出口、E-ARC2仍OPEN。
原W5私人ρ≥5的結果保留原契約，未另宣稱本次已將其去依賴推給932。
紙面、外部Corollary20、plantri完備性／C實作、Python完整有限證書及Lean分層；
沒有新增Lean theorem。所有來源接合保留同一原圖、原具名框、實際原邊／面、
全部fibres（含空）及同一色框的完整lifts。

## 原證據保存與實際重播

[本次保存包](../../audits/2026-10-13-k15-c8-no4ct-publication/REPORT.md)記錄
十份原audit的966檔、66,917,185 bytes及mode。原報告、frozen inputs、
證書與歷史成功／失敗均不覆寫；707個凍結／大型／whitespace原路徑追加封存，
355個新blobs共10,062,334 compressed bytes，原ARCHIVE records保持。
新checkout先按[audit還原入口](../../audits/README.md)restore，再執行原checker。

本次22項K15／C8／W5主、獨立、seed17、负控制與校準及9項no4ct
上游／三支接入重播全部通過，命令與退出碼分別保存於
[數學receipts](../../audits/2026-10-13-k15-c8-no4ct-publication/validation/math-results.json)及
[no4ct receipts](../../audits/2026-10-13-k15-c8-no4ct-publication/validation/no4ct-results.json)。
受限C4及W5構造使用已確認版本的既有NetworkX3.5唯讀路徑，避免原uv
launcher的cache寫入限制；collar五項子檢查分別執行，原launcher不改。

`lake build`完成8,831 jobs，僅記既有Lean回歸。正式文件／DocGraph、
Git index儲存政策、whitespace及原檔保存核對另見本次驗證紀錄。
全工作樹DocGraph仍有62個歷史凍結副本duplicate-ID錯誤，分列FAIL；
不刪舊快照或改稱全域通過。初次文件檢查的發布頁尚未建立診斷保留，
完整頁建立後重新檢查。

沒有重跑375,126,827候選的min4完整生成、外部cone證書、全套舊大型
artifact生成或本輪文獻網路檢索；沿用各原輪次receipt與外部信任，不冒稱本次全量再驗。

## 文件傳播與發布

Updated：K15、C8原內圈／剝層權威入口；共面／度數／外圈／apex直接consumers
增加有日期的替代證明接入；no4ct交接、Kempe guide與STATUS改為已完成三支
接入，下一窄入口為同一原C8的m≥11三型（含首次可進入的PINCH），h≥4另列。
W5與singleton文獻保持独立信任界線；README新增no4ct入口并修正舊大小界。
Reviewed-unchanged：HANDOFF研究線與tag、跨線synthesis、N2／E-ARC2及
W5私人ρ≥5原契約；圖譜程式／OPEN類資料無變化，未重建。
Remaining OPEN：上表無界義務、一般五度縮減與主命題。
Propagation stop：L2及受影響README routing；不提升父題或覆寫原研究快照。

按本次相連白名單stage，通過發布檢查後commit、push。
發布SHA、HEAD／origin/main／遠端main一致及clean狀態以即時Git為準。

發布檢查初次plain Python測試缺NetworkX，使用已確認3.5路徑後94項通過；
Git將一份原PDF視為文字而報whitespace，已按原bytes追加封存，原PDF保留。
初次診斷亦保存，修復儲存方式後重新核對index與whitespace。
