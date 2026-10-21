# W7單障礙、完整原E與L混色路的連貫發布

2026-10-21；發布前BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
使用者授權commit + push；只整理已完成研究與其必要依賴，不新增研究宣稱。

## 來源與數學範圍

依序發布[exploration](../2026-10-21-w7-exploration-30dde27/REPORT.md)、
[single-barrier](../2026-10-21-w7-single-barrier-30dde27/REPORT.md)、
[k1-mixed](../2026-10-21-w7-k1-mixed-30dde27/REPORT.md)、
[L-path](../2026-10-21-w7-L-path-30dde27/REPORT.md)。
317份非快取原證據共138,163,658 bytes；完整SHA與大小見
[evidence-before.json](evidence-before.json)，原路由見[BASE.json](BASE.json)。
失敗初證、v2／v3、完整fibres／空列、所有負控制及原未提交聲明都保持bytes。

profile0、K=1的n／u4／u2／u3／u1來源位置已排，只餘L；原profiles仍為
38已排／2 OPEN。L普通六度／雙五度仍留4／4／2及4／4／3個分palette
必要型，只新增型II／B44466／U=原w的來源子支排除。五邊七spoke型與
一般奇長gap引理為原圖條件結構，沒有提供大cell多內點的來源排除。
L四型、兩短型共同來源、pinched aliases、K≥2／profile1、一般W7／J1／J2、
完整計數錐、合法較小bad及主命題均OPEN；沒有新Lean或來源圖實現。

## 封存與重播合同

按既有artifact政策只封存[三份大型JSON](archive-selection.json)，恰追加
三個gzip blobs：21,816,344 raw bytes／720,740 compressed bytes。
[ARCHIVE-before.json.gz](ARCHIVE-before.json.gz)保存發布前索引；verifier逐項
核舊6,145個file records及3,120個blob records不變，並核新增gzip與還原bytes。
其餘原檔直接Git保存。沒有重新生成舊family、改hash、刪失敗或發布bytecode。

22項發布前原checker重放中21項PASS。mixed/integrate最後歷史receipt比較
失敗，原因是本機多出`transport/__pycache__/check.cpython-314.pyc`；原46份
artifact均零漂移。此失敗與delta保留在本包runs。乾淨臨時overlay不複製
bytecode，同一原checker、證書與routing下mixed/integrate已PASS。
single舊receipt亦曾列衍生bytecode；原receipt保持，不把快取當成發布來源。

原single independent_caps、mixed full_exterior／integrate及L根checker會
嚴查live routing。發布只授權更新STATUS／guide，故[verify.py](verify.py)
分別核28份非routing authority不變，以及三份routing的原SHA。研究重播在
臨時overlay覆以原routing bytes；現行文件另跑正式docs檢查。沒有改原
checker／BASE來接受漂移，也不聲稱現行routing仍與原凍結文件相同。

```sh
python3 tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-21-w7-L-publish-30dde27/verify.py
python3 -B audits/2026-10-21-w7-L-publish-30dde27/verify.py --replay root --replay mixed --replay single --replay integrated --seed17 --log-dir /tmp/w7-L-published-replay
```

覆蓋更大的原E閉包可另加`--replay full-E`；只讀既有universal-C13與v3，
不重建428,506欄。原正常／seed17、負控制與本次實際新重播分開記錄。
本輪lake build、94項工具測試、正式文件及scoped DocGraph均PASS；新紙面
拓撲不因此成為Lean定理。全工作樹DocGraph仍FAIL，72項診斷與前次逐項
相同，沒有新增差異，原失敗完整保留。
[verify_index.py](verify_index.py)另從Git staged objects讀回314份直接檔案及
三份封存JSON，317份原bytes全與發布前SHA相等，沒有無關路徑或bytecode。
這個index保存核對與工作樹歷史routing overlay是兩項檢查，不冒稱完整fresh
checkout隔離重播。其餘本地驗證與結果由[checks.json](checks.json)記錄；
遠端CI與push成功另作即時核對。

## 文件及採納

更新Kempe導覽的現況／停止點、STATUS四包直接索引、README最新發布入口、
audits封存入口與[本次歷史紀錄](../../docs/history/2026-10-21-w7-L-path-publish.md)。
HANDOFF研究線與活躍狀態沒有變化，reviewed-unchanged；State及其他一般
J1／J2摘要未受窄子支排除影響。Propagation stop為L2，父W7仍OPEN。
目前接續由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
發布完成以即時HEAD／origin/main／remote main與工作樹核對為準。
