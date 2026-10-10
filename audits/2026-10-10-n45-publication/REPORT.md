# N45 進展整理與 connected evidence 發布

2026-10-10；研究BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
使用者授權commit＋push；本輪沒有新數學claim或新增來源／Lean。
目前採納範圍與保留OPEN見[dated publication record](../../docs/history/2026-10-10-n45-progress-publish.md)。
本輪不改舊sealed bytes／metadata／pins或歷史FAIL。

[scope](scope.json)列46個相連N45 roots、五份current文件與八份既有history；
[inputs](inputs.json)保存完整original file sets、bytes／modes／symlink targets；
[archive](archive.json)及[summary](archive-summary.json)記去重gzip原bytes封存。
9個source prefixes全保，包括原.git marker、nested legacy archive blobs及40個snapshot links；
另兩個negative-replay symlinks維持ordinary Git。
353,331,200-byte tar stdout在原三處保相同hash；新compressed bytes分片，避免巨大普通Git blob。

新[verify.py](verify.py)用真實 `git merge-base --is-ancestor BASE HEAD`，
完整原trees／当前文件hash綁定後，呼叫封存HIGH23的五項custody函式，
原document pin另由[精確transition](document-transition.json)核回：只准STATUS增加一行dated發布索引。
原main固定HEAD==BASE的歷史量詞不改，不假造post-commit舊入口PASS。
[archive.py](archive.py)先核所有gzip parts／完整uncompressed hash，再還原原bytes與literal links；
不覆寫不同檔案或link。復原命令見dated record。

檢查的actual argv／cwd／environment／streams／exit封存在[logs](logs/)。
最終發布Gate另記validation.json；commit與push的即時SHA equality由Git回讀確認。
原DocGraph62duplicate-ID／outside custody FAIL／BASE缺檔／E4 provenance及failed generation保留。
不重跑全部前序有限搜尋、來源枚舉或舊已失效current-pin入口，沿用原凍結receipts。
未新增finite source／source realization／Lean、PR或merge。

初次出版docs check因新history未直接列於STATUS而exit1，原stream與初版verifier／inputs保留。
依既有document治理加一行索引，原STATUS hash仍由HIGH23 frozen draft核回；
其他採納文件不变，原parent不改。最後gate使用新的actual收據，不把初次FAIL覆寫成PASS。

終版actual gates全部通過，見[validation](validation.json)：fresh候選先還原legacy
2,548paths／1,466blobs，再還原本輪49,699paths／5,188blobs；46 roots全部52,453
原files／links及modes匹配。fresh與live publication normal／seed17各byte一致；
漏nested receipt負控制exit2。文件檢查596Markdown／7,242local links、限定docs
DocGraph及staged whitespace通過。lake build exit0、8,831jobs，只保原lint；
原worktree全域DocGraph exit1／62duplicates與所有舊custody FAIL未改。
原始封存資料4,533,048,879 bytes，新compressed bytes240,244,695、每片最多24,000,000 bytes。
Git index無gitlink；nonpayload caches／未相連scratch不納提交，原資料不刪。
