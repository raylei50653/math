# 五輪 generated-artifact 與 stage 完整性盤點

2026-10-23；publication BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
只寫本review/artifacts目錄；未改五輪原檔、政策、checker或Git index，未add／commit。

**PASS：五輪738份原檔全部保留，worktree與已暫存blob逐份bytes／SHA均等於
publication BASE。** 五輪檔案數為101、125、164、173、175；共375個不同Git
blob。沒有新增／缺漏原檔，immutable drift為零。

精確大檔例外見[exception-additions.json](exception-additions.json)：

- 6份.json命中政策的`>=1,000,000 bytes`門檻，共16,311,359 bytes。
- 每份逐路徑給`kind=frozen`、用途reason、bytes及SHA256；包含保留的污染
  證書反控制、active certificates與完整frozen snapshots，沒有萬用字元。
- 另11份大.gz共31,109,104 bytes，副檔名不在政策domain；仍包含在完整738份
  證據與暫存核對中，沒有刪除或重新壓縮歷史快照。
- 無須修改tools/check_generated_artifacts.py。[完整119項政策建議副本](generated_artifact_exceptions.proposed.json)
  保留原113條記錄；root合併後的staged policy已逐項比對完全一致。

詳細清單見[inventory-v2.json](inventory-v2.json)，暫存bytes與政策記錄比對見
[index-integrity.json](index-integrity.json)。盤點前後Git index SHA相同，確認
本agent未修改index。v2當時的index policy check已PASS，119份大檔均有例外；
root仍應在最後補stage發布回執後重跑最終checker。

[stage-coverage-v2.json](stage-coverage-v2.json)列明五輪目錄、publication目錄、
五份既有變動docs、新history及政策檔。沒有ignored檔需要force-add，沒有
未追蹤或已變更檔落在建議scope外。README.md與docs/HANDOFF.md已review，
保持不變，不列stage。第一版coverage記錄了當時新history尚未納scope；
v2已明確加入，首版只保留為盤點歷史。

root可使用[stage-pathspecs-v2.paths0](stage-pathspecs-v2.paths0)的NUL分隔精確
pathspec；publication目錄pathspec會包含本review後補的v2／REVIEW／manifest。
所有publication writer仍可能新增回執，提交前應再核scope及完整staged policy。

```sh
git add --pathspec-from-file=audits/2026-10-23-three-mask-publish-cb8f859/review/artifacts/stage-pathspecs-v2.paths0 --pathspec-file-nul
python3 -B tools/check_generated_artifacts.py
```

本盤點只核儲存政策、bytes custody與stage coverage，沒有重跑數學證書、
Lean或遠端CI，亦未提升任何來源／較小bad／一般定理狀態。
