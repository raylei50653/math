# 941 Γ8／wrong-side接續發布核對

2026-10-23；exclusive BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
使用者明確授權commit + push。本批保存32組相連研究audit與發布收據，
累積結果、精確邊界及接續入口見[整理紀錄](../../docs/history/2026-10-23-941-gamma8-publish.md)
及[Kempe導覽](../../docs/c5_kempe_guide.md)。

## 結論與權威

第七輪空M2／T6／七資源的154入口完整共同星排除兩N及一N一K，只餘
d≠U、K0+K2密封K8。來源到有限包絡的全稱涵蓋由
[原PROOF](../2026-10-23-941-types-wrong-side-round7-6b09cd4/PROOF.md)承擔，
不限制旁觀點數，不把K／U未知尾星封滿。

21份cap保5754完整fibres（3003空）、4236份lifts；72安全候選均要求真正
01232接受witness只選一次H，再以該同一H的三拒絕列完整回填同一原外側。
四類接受殘餘30／85／116／108，K8整支替換及實際外側接合OPEN。
11整型共同八外點、非空九、非單M2十及共同k≥23不變；一般wrong-side、
941／W7／J1／J2、較小bad及matching仍OPEN，沒有新Lean。

## 保存範圍

[BASE](BASE.json)固定1790份原始檔／206,002,019 bytes、32個audit目錄及
六份入口快照。[verify.py](verify.py)核完整檔案域、大小與SHA；live routing
的合法更新另列，原研究檔不得漂移。全部歷史失敗、前版證書、負控制及
「未commit／push」原敘述保留，發布由本紀錄與即時Git承擔。

本次只提交原相連audit、發布回執、Kempe／STATUS／history與生成檔例外。
48份具名大型JSON以精確bytes／SHA保存為frozen例外，既有119份不變；
逐檔見[例外清單](review/artifact-exceptions.json)。README／HANDOFF入口及
研究線標記未變，依文件治理核對後不改。

## 發布驗證

原checker fresh重播、正常／seed17比較與負控制見
[前段總回執](review/replays-early/SUMMARY.json)及[後段總回執](review/replays-late/SUMMARY.json)，
保留每次argv、環境、stdout、stderr、exit及耗時。
[獨立來源與路由審查](review/SOURCE_REVIEW.md)核完整同源／同H邊界。
本次不重做來源研究，不以工程檢查宣稱新形式化。

工程、文件、完整index政策與隔離暫存來源重播的最終結果由下表及
[local原始收據](review/local/)記錄；遠端CI於push後另查。

| 核對 | 實際結果與限制 |
| --- | --- |
| 原研究保管 | 1790份／206,002,019 bytes，fresh前後逐份核SHA零漂移；全部已在index |
| 各原入口normal／seed17／negative | 前段62／62、後段45／45共107次PASS；36組正常／seed17數學payload除seed外一致；385項語義反控制被拒絕 |
| 第七輪外部破壞 | [六項](review/replays-late/EXTERNAL-SUMMARY.json)全以exit 1及指定拒絕原因退回；涵蓋原框、U別名、來源權威、full lift、商圖與殘餘 |
| Lean工程回歸 | `lake build --no-ansi` PASS，8832 jobs；沒有新增Lean theorem |
| 工具回歸 | requirements環境94項unittest PASS |
| 正式文件／docs DocGraph | 713份Markdown／9474本地連結PASS；97文件／383關係／12families，0errors |
| 全樹DocGraph | FAIL：97文件／368關係／72個封存duplicate-ID錯誤，獨立保存 |
| Git index生成檔政策 | PASS；167份大型檔精確例外及166個registered outputs；最終index數見local回執 |
| Whitespace | tracked diff PASS；完整index因8個原始證據位置及重現其空格的原始診斷收據FAIL；精確排除8份原檔與2份診斷後其餘index PASS，未改寫原bytes |
| 隔離暫存來源 | [index export](review/isolated/SUMMARY.json)逐份核1790原檔SHA後，第七輪完整checker PASS；暫存目錄已刪除 |

八個whitespace位置是七份前輪checker的frozen副本末尾空行，以及一份
已封存producer的行尾空格；[精確清單](review/whitespace-exceptions.json)
對回BASE與indexed blob的bytes／SHA。兩份原始診斷stdout也逐位保留被報出的
producer行尾空格，故另列精確診斷例外。完整FAIL、首次限定檢查的診斷FAIL
與最終限定PASS均保留，沒有把scoped PASS誤記成全index無錯。
全樹DocGraph的72項錯誤亦不計入正式docs PASS。

```sh
python3 -B audits/2026-10-23-941-publish-6b09cd4/verify.py
python3 -B audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/check.py
lake build --no-ansi
uv run --with-requirements requirements.txt python -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
python3 -B tools/check_generated_artifacts.py
git diff --cached --check
```

未執行的原研究探索與全專案其他來源checker不列為本次重新驗證；
精確執行範圍由收據列明。發布SHA與clean tree以即時Git核對為準。
