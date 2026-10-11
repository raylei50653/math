# BR-SD-1g publication：獨立 custody 審查

2026-10-11。Reviewer：`/root/publication_review`。本 reviewer 只寫本 publication 的
`agents/REVIEW.md`／`agents/ACCEPTANCE.json`，不改原160檔、主證明、canonical或Git refs。

**裁決：accepted publication custody；未處理阻斷 findings＝0。**
此次接受只針對下列最終 bytes 的發布保全及Git邊界，不重做任意大小紙面定理，
不新增來源、Lean或canonical採納。紙面原接受與正式採納仍分開；父身份 **OPEN**、
完整 OPEN 身份新增無條件關閉數 **0**、actual source finite **not triggered**。

## 精確接受版本

| Publication 檔案 | SHA256 |
| --- | --- |
| verify.py | `50440b187a9e822d127e91c114079407b13f5e044ac1c371073096e67d7e7958` |
| PUBLICATION.md | `b7a0d52b799c86b3c40f20840ff99aa6abfe17fc044057f7d6b99e2c41339bd2` |

[ACCEPTANCE](ACCEPTANCE.json) 接受以上完整bytes；後續publication manifest與實際staged／
descendant／remote檢查由root執行，不冒充reviewer已做的Git發布。

## 原封存證據與範圍

直接獨立讀取原 SEAL、REPORT、paper REVIEW／ACCEPTANCE、INPUTS與OLD-CUSTODY。
原 SEAL SHA256為
`d3952f60eaba362762d3555b800ba9a03eeaf5171c0404fbea70cfc330ec8edc`；
全部159 payload加SEAL合計160檔，逐檔完整枚舉的bytes／size／mode／symlink均相符，
無遺漏或新增。31份authority各與原frozen、BASE git blob及live path一致；
三舊1a／1c／1e audit完整313檔枚舉也與原manifest一致。獨立回讀exit0。

原 PROOF／MAPPING／REPORT 分別為
`14544b9a09b8fd67bb7a8539ab2566a442cc9cae692e71f966afb9a2adbe9d5e`、
`ea752148d9f5f19ea111f5474b058b06c2920e4ebb9a49e87c97f9cb3b6e52c5`、
`e0a0401988a24e2e63aa88a8a1ded7a0ce25be29a578363ff3834d550eac0c68`；
原paper REVIEW hash為
`4c98bef4166700604f61e1d102ab1ea1c529166ae3bde61c8980fa48244a2c19`。
它們仍是原exact-contract候選排除與原獨立數學接受，沒有改成父身份closure。

## Companion逐項審查

1. 固定完整原SEAL SHA，先核原159-payload digest及完整inventory，
   因此INPUTS／OLD-CUSTODY與原paper acceptance亦被原seal固定，不能縮小清單逃避覆蓋。
2. 再核31份BASE／frozen／live資料、313份三舊audit全目錄、精確paper接受及
   22項原checks的exit／stdout／stderr digest。這是內容custody，不是重新執行22項命令。
3. 實際HEAD必為研究BASE descendant。BASE..HEAD與index相對HEAD各自只准本兩目錄新增；
   working porcelain另查，不能用本機undo遮掉已commit的越界變更。
4. 原audit與publication各自的HEAD／index清單必完整；一旦任一開始tracked即拒絕partial。
   每個blob的SHA／size及Git100644／100755 mode均對工作檔。`--require-tracked`強制两者全齊。
5. publication manifest核完整keys、BASE／原seal／OPEN／0／清單digest及全payload bytes。
   final check另要求reviewer接受verify.py與PUBLICATION.md的精確hashes。
   preseal只容許manifest尚未建立，且不能搭`--require-tracked`，沒有把preseal宣稱sealed。
6. 原fresh verifier不變；原historical「未commit」與BASE-only條款保留。
   新文檔清楚給出postcommit只讀入口，精確白名單在未來canonical變動後會拒絕。
   沒有mock原fresh verifier來冒充它通過，也沒有刪除失敗generation、負證書或凍結bytecode。

讀取PRECHECKS的8項root實際命令紀錄，全部exit0；與文檔的發布前措辭相符。
其中來源synthetic finite與紙面／actual-source分層仍保留。

## 隔離controls與限制

Reviewer以runpy載入新companion，只mock其Git輸出做局部函式controls，未寫原檔或Git。
兩份獨立Python probes均exit0，共21個配置符合預期：

- manifest：合法接受；錯BASE、CLOSED、closures1、多餘key、錯digest、漏payload均拒絕。
- diff：准許目錄新增接受；越界docs、新增lookalike prefix、原payload修改及刪除拒絕。
- HEAD／index：完整合法接受；缺檔、部分tracked、額外檔、錯mode、錯blob、unmerged均拒絕；
  未tracked且非required的研究前階段按設計接受。

Reviewer另實際執行新companion `--check --preseal`，exit0：160原檔、31輸入、313舊檔、
22原checks、67 local links全部通過；當時HEAD仍BASE，兩目錄皆未tracked。
這是manifest建立前的內容回讀，沒有宣稱sealed或已發布。

這些局部controls為 `triggered and holds`，驗工具拒絕路徑；**不是actual來源驗證**。
本review不代替root後續實際sealed／staged／descendant重播與push後refs讀回。
未新增Lean或重跑lake build；完整父身份維持OPEN，新增無條件關閉數0。
