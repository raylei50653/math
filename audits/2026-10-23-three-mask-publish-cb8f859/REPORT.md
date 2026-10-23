# 五輪932／933／941整理發布核對

2026-10-23；exclusive BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
使用者明確授權commit + push；研究內容由五輪原報告承擔，本批只整理、
保存及核對發布範圍。累積結果及下一窄義務見
[五輪交接](../../docs/history/2026-10-23-three-mask-five-rounds-publish.md)。

一般932／933／941、實際較小bad、K∞與新Lean保持OPEN；共同k≥23未變。
932的s≥1／d≥2僅限原h=4 C9契約；933的k−8換框圖H*仍在K132；941兩
共同patch合至少六原點，不保證六私有點。所有作用都須保持同一原來源、
完整有序框與附件、空fibres及全部full lifts。

## 保管與範圍

[BASE](BASE.json)凍結五輪738檔／69,861,223 bytes與七份routing入口。
[只讀核對器](verify.py)逐檔檢查完整域、bytes／SHA及入口快照，並區分
live routing合法更新。原報告、原檢查器及歷史未commit／push敘述均不改寫。

本次提交五輪完整相連audit、發布回執、五份相連docs、history紀錄及大型
JSON逐檔frozen例外。共通語言原有單向回填接口已對回權威來源，隨本批保存。
README／HANDOFF研究線與活躍標記不變，依文件治理記reviewed-unchanged。
大型檔例外只保存具名證書／凍結輸入的精確bytes／SHA，不放寬政策。

## 發布驗證

五輪[重播總回執](review/replays/SUMMARY.json)保存全部原入口stdout／stderr、
argv、exit與耗時；正常／seed17的成功數學payload一致，來源負控制均按原入口執行。

| 核對 | 實際結果與限制 |
| --- | --- |
| 第一輪原live root，正常／seed17 | 兩次FAIL均停於歷史routing SHA guard；原失敗完整保存 |
| 第一輪隔離歷史view，正常／seed17 | 兩次PASS；git archive原BASE、覆蓋738原audit及精確frozen handoff bytes，不改checker或expected hash；暫存樹已刪 |
| 第二至五輪原live root，正常／seed17 | 八次PASS，原始JSON相等；各線負控制按原入口執行 |
| 五輪保管 | 738檔／69,861,223 bytes，完整檔案域、bytes／SHA前後零漂移 |
| 文件與來源審核 | [五份docs及history審核](review/docs/REVIEW.md)PASS；共通語言原接口另對回權威原理並fresh重播 |
| 大檔與stage範圍 | [逐檔inventory](review/artifacts/inventory.json)及[stage覆蓋](review/artifacts/stage-coverage-v2.json)核全738檔；6份精確frozen例外，原113份不變，無ignored／scope外遺漏 |
| Lean工程回歸 | `lake build --no-ansi` PASS，8832 jobs；不把新紙證／Python憑證形式化 |
| 工具回歸 | 94項unittest PASS；命令環境使用requirements.txt |
| 正式文件 | 712份Markdown／9420本地連結PASS；正式docs DocGraph 97文件／383關係／12families，0errors |
| 全樹DocGraph | FAIL：97文件／368關係／72個封存duplicate-ID錯誤；獨立保留，未計為正式docs通過 |
| Git index生成檔政策 | 完整暫存後檢查PASS；119大檔精確例外、166 registered outputs；實際indexed計數見local回執 |
| Whitespace | live tracked diff PASS；全index check僅兩個原frozen檔的blank-at-EOF而FAIL；精確排除這兩個完整路徑後其餘index PASS，見[獨立審核](review/docs/WHITESPACE_REVIEW.md) |

第一輪root的932 checker把舊no4ct handoff SHA當固定依賴；該live文件已在
後輪更新。隔離歷史view採第一輪frozen與原Git BASE雙核一致的原bytes，
沒有略過來源守衛，也沒有把兩次live FAIL計成PASS。

兩個保留的whitespace位置是第二輪933故意破壞authority的negative REPORT
末尾，以及第五輪941已凍結checker末尾。前者空行是反控制原bytes的一部分；
兩者都須保原SHA，不藉正規化改寫證據。精確路徑、完整FAIL與scoped PASS
見[完整暫存檢查](review/local/whitespace-index-initial.stdout.txt)及
[限定暫存檢查](review/local/whitespace-index-scoped.json)。
其他檢查argv／stdout／stderr／exit／耗時見[local回執目錄](review/local/)。
遠端CI於push後另查，發布SHA與clean tree由即時Git確認。

```sh
python3 -B audits/2026-10-23-three-mask-publish-cb8f859/verify.py
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/check.py
lake build --no-ansi
uv run --with-requirements requirements.txt python -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
python3 -B tools/check_generated_artifacts.py
git diff --cached --check
```

本批commit／push結果以即時Git核對為準；原研究快照不回填發布結果。
