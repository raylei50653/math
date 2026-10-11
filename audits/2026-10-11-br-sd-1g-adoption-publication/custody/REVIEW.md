# BR-SD-1g 正式採納 publication：獨立 custody 審查

2026-10-11；reviewer `/root/custody`。本輪owner已批准正式採納完整精確子域、
必要文件回寫，以及通過獨立檢查後commit／push main。
授權不修改任何舊audit／sealed evidence；本reviewer只寫本新publication audit的
`verify.py`、`negative_controls.py`與`custody/`，沒有stage／commit／push。

**Custody／工具審查：原資料零漂移，未處理阻斷finding＝0。**
最終數學／source合同與完整新bundle bytes另由proof reviewer獨立接受。
本文件在root最終negative execution／final acceptance／seal之前交付，
不將尚未執行的命令寫成成功；實際結果須由CHECKS及最終external receipts確認。

## 1. Owner boundary與舊證據

正式文件改動只准5個existing paths：N45 canonical、degree5 guide、interfaces、Kempe guide、STATUS；
新增history固定`docs/history/2026-10-11-br-sd-1g-adoption.md`。
HANDOFF／STATUS_HISTORY／README與其餘原BASE tracked entries皆維持原bytes／modes。
新六份文件的完整path／SHA／size／mode固定於[ADOPTION_MANIFEST](../ADOPTION_MANIFEST.json)，
authoritative owner instruction另記[AUTHORIZATION](../AUTHORIZATION.json)。
文件量詞及原採納1a／1c／1e文字保全由mapping／proof review另核。

新checker不import、修改或mock任何historical verifier；獨立重建下列custody義務：

| 不變證據 | 實際完整覆蓋 |
| --- | --- |
| BASE工作區 | 原sealed WORKSPACE_BEFORE的固定SHA；15743 BASE tree／index entries和filesystem bytes／mode／symlink target，只有明確授權5docs可改 |
| 原BR-SD-1g | 固定原SEAL SHA，159 payload＋seal＝160檔完整inventory；原HEAD／index／work bytes與modes必須相符 |
| 原publication | 固定MANIFEST SHA，全6檔及payload digest；HEAD／index／work完全相符 |
| 三舊audits | filesystem全部313檔paths／hash／size／mode／symlink；原tracked子集合309及4既有ignored local-only分開，禁止額外把4份提升為tracked |
| 原authority | 原31 frozen bytes和research BASE blobs逐項核對；非授權live authority維持舊bytes，授權5docs的live bytes只可等於新approved manifest |
| 已封採納審查 | 原review audit完整281檔paths／hash／size／modes由初始固定inventory SHA核對；原SEAL固定263 payload，DELIVERY固定16 postseal檔；兩個envelope bytes均另固定SHA |
| 舊preflight | 固定本輪建立新目錄前的7項實際原命令record SHA；historical whitelist拒絕與相容性成功保持分層 |

新reviewaudit281之前未tracked，不以原REPORT中的未commit歴史措辭否定本輪owner後續publication授權。
封存原文、原commands、negative controls、failed generations及全部sealed accepts不改；
新的history／TASK記錄當前正式採納，不回寫歷史候選身份。

## 2. 實際precheck與Git階段

本reviewer已實際執行新checker的`--precheck`，exit0：
approved6docs、original160、oldpublication6、review281、old313、authority31、immutable15738
均相符；當時HEAD仍BASE，oldreview／newpublication皆未tracked。
CHECKS存在後另次precheck亦實際exit0，核當時31份root actual receipts及已由同argv成功重播取代的doc初次failure。
這不是postcommit驗證；root必須另行取得normal／hashseed17及完整negative controls的實際紀錄。

Checker要求BASE ancestry與main branch，逐項分開核HEAD、index及working tree。
BASE..HEAD／index／working diff只准5個existing M、history A、oldreview／本publication A；
不能用本機undo掩蓋已commit或stage的越界修改。未授權原entries的HEAD／index OIDs與modes
固定於BASE；working bytes另核原trusted manifest。
新history若在HEAD／index已存在，precheck階段也必須對回approved manifest的完整bytes／mode，
沒有等到最後require-tracked才發現已stage或commit的不一致。

`--check --require-tracked`強制完整281 oldreview及本newaudit（包含新SEAL）在HEAD／index精確齊備，
所有six approved docs的HEAD／index／work bytes／Git mode等於已接受manifest。
因此commit後不要求HEAD仍等於舊BASE，而要求真正descendant加精確新增／修改白名單。
partial tracking、extra paths、改舊audit或額外canonical檔均不能通過。

## 3. Final bytes與封存接口

本新audit只排除自己的`SEAL.json`；沒有postseal／receipt白名單可在封存後繼續寫。
最終proof acceptance只另外排除它自己，必須固定所有其他newpayload及六份approved docs的完整inventory。
其schema固定BASE、0 finding、OPEN／0、source not triggered／no new Lean；
accepted_bundle SHA對回documents＋payloads，不能靠刪清單或只核marginal hashes通過。

`--seal`須取得完整final byte接受，再exclusive-create自己的SEAL，固定filesystem mode644。
Seal核完整exact object、全部payload bytes／modes及六文件；不能overwrite或省略evidence。
`--check`和`--precheck`唯讀，only `--seal`有本newenvelope的寫入分支。
所有postseal／postcommit／postpush實際輸出由root記在repo外`/tmp`及session，
不改final accepted payload或新seal；commit／push完成後還須normal／hashseed17 require-tracked回讀。

CHECKS對actual argv／cwd／actual與expected exits／stdout／stderr digests逐项回讀。
若有root receipt JSON，其原bytes digest與全部原欄位另對回；root-relative及audit-relative
paths都須resolve在本newaudit內，不允許receipt path逃出。
原unexpected failures不改exit或expected；保留說明及原raw logs，
非pending final mode要求commands有同argv、actual0／expected0的實際success，才允許進入seal。

## 4. Memory negative controls與適用界線

[negative_controls.py](../negative_controls.py)使用兩個memfds提供prospective seal及document manifest。
先以valid positive control要求完整唯讀manifest入口exit0，再測9份具名corruptions：
parent CLOSED、source／Lean／closure升級、extra metadata、刪payload再重hash、
改document hash再重hash、document manifest parent drift及coverage不足。
每個拒絕必須符合預期具體錯誤理由，不能把missing acceptance等無關failure當成功negative。
這個`--validate-manifests`入口明確是preseal local manifest／inventory校準，
不代替真實final acceptance或commit後require-tracked檢查。

Root在執行前code review定位兩個harness reason字符串不匹配：
manifest parent drift走scope guard，coverage走approved inventory guard。
本reviewer已按實際guard分開reason map；沒有舊bytes改動，也沒有將尚未跑的控制列為PASS。

memfd控制不產生或修改磁碟seal／文件／原artifact，保存每份actual argv／stdout／stderr／exit。
工具在結束前核六份adopted docs、原manifest、自己的tools和既有seal（若存在）bytes不變。
root將其完整stdout／stderr／exit保存於CHECKS後，proof reviewer才接受整體新bundle。

## 5. 尚待root履行

本reviewer交付此檔後停止寫入，讓root串行完成normal／seed17 precheck、正負控制、
實際CHECKS整合和REPORT，然後由另一reviewer接受完整final bytes。
之後才能exclusive seal、stage／commit／push，以及remote/main／HEAD／index／clean-tree讀回。
tool code或approved docs若再改動，需新的exact-byte review，不能沿用本接受。

**完整N45-S-NOU-LS-PAIR父身份保持OPEN；actual source `not triggered`；
新Lean theorem 0；完整OPEN身份新增無條件關閉0。**
Custody成功不建立actual source，也不擴大到一般兩／多旁支、其他splits／骨架、R31、ε≥3、
一般N45／N2／E或`K∞=K≤5`。
