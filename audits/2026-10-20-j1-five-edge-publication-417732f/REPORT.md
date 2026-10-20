# J1五邊路研究發布核對

2026-10-20；BASE `417732fc5ef0a012829fd6712333b1c906128d3a`。
本目錄保存使用者授權的整理、commit及push核對，研究證據不改寫。
成果、OPEN界線、完整封存與還原命令見[發布紀錄](../../docs/history/2026-10-20-j1-five-edge-progress-publish.md)。

[SOURCE_FILES](SOURCE_FILES.json.gz)固定原研究2,649份來源。
[check_custody.py](check_custody.py)核對原始bytes、append-only archive、逐blob還原及提交白名單；
加`--index`時只讀Git index中的保存內容。
[fresh_replay.py](fresh_replay.py)只從Git index讀取全部研究檔案／gzip，
在臨時新checkout還原後執行完整數學checker。
[publication-checks](publication-checks.json)記錄實際執行結果。

研究報告中的未commit／push是前一階段快照，保留其原bytes。
最終發布SHA、push及工作樹以完成時Git讀回為準，不預先宣稱CI成功。
