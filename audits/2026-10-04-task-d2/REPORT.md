# D₂：文件整合與新增成果稽核

2026-10-04，HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`。
本次沿用[原D報告](../2026-10-04-task-d/REPORT.md)的證據邊界，
新增A／B成果稽核並同步A／B／C入口，未commit／push。
原D報告是08:58:32 Asia/Taipei截點的40 PASS／4文件hash FAIL；
本次結果另存本目錄，原紀錄不改寫。

## 修訂與停止點

[18項修訂驗收](REVISION_RESULTS.md)全部適用。當前索引與報告後續前綴
改為mixed11子型完成、固定H1已在原source前提下成立；歷史輪次數字、
原正文、舊artifacts與舊checker bytes保留。合法同圖relabeling搬運原
rotation不要求另選canonical rotation相同；Σ／row／共同色框與owner一起搬運。
停止點由各guide維護，HANDOFF保持薄索引。

| 任務 | 最新停止點 | 現行入口 |
| --- | --- | --- |
| A／A₂ mixed12+a-unary | A的70／90→22／26由A₂再排01／12及root交換，保存20／24框架、52／86actual supports、68／124完整singleton schedules | [Kempe §3](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)：原01／01及root交換，四份原disk rotations、原C ternary、U與完整六角色joint |
| B／B₂ mixed22無unary | 七contact身份、四spoke省略各自Ω；B的20／20骨架仍保留，B₂只排W933-101／W941-139短face{1,2}，原G仍(5,5) q-core | [Kempe §3](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)：同一01／23骨架長face{0,4,3}的完整C／shared-contact leaf bridge；933原04／12附件{4}亦保留 |
| C／C₂ 共鄰P₃ | C₂只關閉CPP-134-1／geometry30／side20的單框點自身支援三接點unary窄支；原36／140／900不刪列，0 target | [weak-deletion §3](../../docs/c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)：CPP-134-1／geometry34／side_join_id20，Az={b₁,b₂}，保留原P₃與z–x₂–b₄外路 |

整合期間新增的A₂／B₂／C₂納入最新停止點；原A／B和後續A₂／B₂
分別凍結稽核，保留原輪次和具名域。C／C₂本次只同步入口及原checker
重播，不算入A／B新增完整joint稽核覆蓋。

## A／B新增獨立覆蓋

[A notes](a/notes.md)、[A results](a/results.json)及
[B notes](b/notes.md)、[B results](b/results.json)全部通過。
兩份獨立程式只用標準庫MRV回溯，從actual原邊重建；未匯入production
enumerator、join helper或witness validator。每份原陣列先查重複再比完整
tuple集合，保留contact aliases、owner、actual attachments、原分量與同一色框。

| 本輪新增範圍 | A mixed12 | B mixed22 |
| --- | ---: | ---: |
| 原source-filtered身份／排除／殘留 | 70／90；48／64；22／26 | 47／75；22／50 spoke排除、5／5 sealed排除；20／20 |
| contact身份控制 | x獨立／x=y₀／x=y₁，72圖 | 七份跨側共享身份，28圖 |
| 完整整圖joints | 5,760（5,040六角色＋720五角色） | 1,680六角色 |
| 字面pinned fibres／空fibres | 92,160／73,224 | 26,880／21,008 |
| 每份序列化colouring witness獨立驗證 | 144,830 | 45,178 |
| complete C／U relations | 720／720 | 280完整四contacts R_C |
| 原 carrier relations | K ternary 2,160、L binary 1,440 | 1,120三contacts |
| 原root-swap joint核對 | 2,520 | 840（連完整fibres） |

A另從原source獨立建立域與全部360 disk rotations，核對868 actual
support／singleton screens、37,872 relation rows、1,480個D₅ complete
residual schedules及2,960搬運原rotations；B核對25骨架的2,320 rotation
assignments／60 disk rotations、240份actual附件owner表、14個條件式
原K₅ minor及140條interbag edges。全部具名indices與counterexamples
均存results，不以總數、marginals、mask或orbit數代替關係。

A的[counterexamples](a/counterexamples.json)保留marginal假接合、spoke
省略可染但原圖不接受、投影相同而六角色joint不相等的原tuple／witness。
B保留Pstraight、control20、q01012、roots=(2,3)的完整fibre空但各
marginals非空；933原04／12長face共享contact附件{4}容许deg_C=1。
B的48份spoke省略空joint行亦保留：固定控制圖沒有完整source前提，
不能拿它們當任意大小Ω紙面引理的證明或反例。

## A₂／B₂新增獨立覆蓋

[A₂ notes](a2/notes.md)、[A₂ results](a2/results.json)及
[B₂ notes](b2/notes.md)、[B₂ results](b2/results.json)全部通過，最終輸入
為successor-v2；首版本輸出另存各自v1目錄，不覆蓋原輪次。
A₂沿用新audit自己的MRV與身份工具；B₂只匯入audit-local獨立solver，
兩者均不匯入production enumerator／join／validator。

| 本輪後續新增範圍 | A₂ 01／12 | B₂ 01／23短face |
| --- | ---: | ---: |
| 原身份／完整ledger | 原22／26僅排2／2，原frame全JSON保留其餘20／24 | 兩份frame與B原完整JSON相同，七contact身份；只排短face，20／20骨架不刪列 |
| 固定完整degree圖 | 36（x獨立／共享y₀／共享y₁各12） | 14（七身份×原root swap） |
| 完整C relations | 360 ternary | 140四contacts |
| 完整整圖joints | 2,880（2,520六角色＋360五角色） | 840六角色 |
| 字面pinned fibres／空fibres | 46,080／37,020 | 13,440／10,372 |
| 每份序列化colouring witness獨立驗證 | 81,559 | 9,598（1,960 R_C＋7,638 joint） |
| 原minor／paths controls | 12 K₃,₃／108 paths、8三hub premises／64 local degree-list controls | 7完整degree leaf K₅／10原paths／70 bag edges、2條件式K₄ tether K₅／8 paths／20 bag edges |
| 完整指定列或全域色框核對 | 01202、(a,b,u)=(3,0,2)的36完整C extensions | 3,360獨立S₄ R_C、183,312 transformed joint witnesses |

A₂另核對原actual C supports的64 subsets與16份U-support缺2完整
conflict screens；每份K₃,₃九條paths的原邊、endpoints、simple paths及
interiors互斥均逐條核對。B₂獨立Tarjan分解原leaf blocks、逐角色owner
ledger、實際tethers及K₅ bags；没有從固定pinned root-pair假設逐邊minimal。
長face{0,4,3}、其他face與933原04／12共享contact附件{4}仍保留。
所有負控制與適用前提見各自notes／results；固定控制不證任意大小topology。

**四層新增固定圖coverage共150圖、11,160完整joints、178,560字面fibres，
其中141,624空。** 這是serialized控制的覆蓋總數，不是來源圖枚舉或
disk實現數；各層身份域、carrier relations與紙面引理另外列明。

## 原域與保存核對

沿用原D的獨立[audit_identity.py](../2026-10-04-task-d/identity/audit_identity.py)
對本輪凍結副本重新執行，結果[identity_results.json](identity/identity_results.json)
通過：從原source篩出122份（47／75），六階段陣列無重複且身份欄位
一致，排除互斥、最後0／0；106份canonical partner face集一致，16份
equal-pair self-identity的canonical face差異仍保留，搬運原rotation皆合法。
1,220份D₅ source masks、12,200共同row／color與195,200字面guards
重新核對，沒有改舊ledger checker。

[baseline.json](baseline.json)記錄D₂開始的1,342份既有文件。
[保存程式](audit_integrity.py)及[integrity_results.json](integrity_results.json)
核對1,039份起始scripts／tools／原artifacts／舊history／舊D包未改、所有原artifact
bytes不變、HEAD不變；各既有文件SHA256改動逐份記錄。
整合期間作者新登錄A₂／B₂產物的manifest及.gitignore變化另記，不refresh
舊條目；本次D₂只寫獨立audit與文件，不改production scripts或artifacts。

## 歷史失敗與新文件hash紀錄

[input_hash_audit.json](input_hash_audit.json)涵蓋原D22份及A／B／C、A₂／B₂／C₂
共28份證書、192個直接hash紀錄；仍有原四個文件hash漂移，零非文件
漂移；相對原D截點及D₂起始，新增直接input hash漂移均為零。
11份既有README／docs文件相對D₂開始的新SHA256，及相對原D截點的
11份既有文件改動，均見[document_hash_changes.json](document_hash_changes.json)。
不把未被證書hash綁定的文件
改動稱為byte-check的新失敗，也不宣稱全倉所有證書皆已重播。

[兩份舊證書的完整payload重比較](semantic_payload_results.json)實際重算
全部JSON，僅去除直接input_sha256 map後深比較相同；strict bytes仍
不同、原bytes未改。指定環境default／17重播結果另見
[historical_checks.json](checks/historical_checks.json)，四次原byte-check
失敗仍保留。[初次環境失敗](checks/historical-attempt1/README.md)的两份
singles錯誤為缺NetworkX、未進入byte-check，與歷史hash FAIL分开。

新successor落盤時作者收尾改了A₂／B₂兩份新producer與其產物。
[successor_version_changes](successor_version_changes.json)與兩份source diffs
保存版本SHA256，[完整payload版本比較](successor_version_payload_results.json)
确认兩份去掉直接input_sha256 map後全部payload相同；A₂多綁五個
依賴，B₂整理owner_count與明寫K₄ tether path assertions。
首successor副本的不一致檢查保留在[interim-integrity](checks/interim-integrity/integrity_results.json)，
最終audit另對[successor_baseline_final](successor_baseline_final.json)的凍結
版本重播，不把新增producer版本變化稱作舊artifact漂移或清除舊FAIL。

## 信任界線與重播

獨立audit只核對固定serialized原圖、完整relations／joints／fibres與
原witnesses；任意大小Ω／q-core、disk crosscut、短支援與Gallai仍是
原報告紙面／外部依賴。未證ε≥3、mixed12／mixed22整型、來源實現、
一般／共同出口或`K∞=K≤5`，未新增Lean theorem。
原D的44次結果沿用原紀錄，這次沒有重跑全部22份或來源catalogue、
degree-6全分拆、R系列／閉包／Lean axiom audit。C未做新的獨立joint稽核。

## 實際整合驗證與重播

A、B、A₂最終v2、B₂最終v2的原checker各跑default及hashseed17，
**八次byte-check皆PASS**；具體stdout／stderr／exit code與hash見各層
原replay results。新獨立audit四層皆PASS；原D identity另一次PASS。
兩份舊證書的四次預期hash FAIL及初次環境錯誤另列，沒有混入八次PASS。

| 整合驗收 | 實際結果 |
| --- | --- |
| 文件checker | PASS：523 Markdown、5,414 local links，anchors／index／HANDOFF合法 |
| D₂獨立包links | PASS：9 Markdown、67 local links，0 errors |
| DocGraph | PASS：62 documents、213 relations、5 families，0 errors／notes |
| artifact status | `ok=141`，原manifest files條目不變，作者另新增A₂／B₂ |
| tracked diff與活動audit whitespace | PASS；新audit檔尾空行已修正，v1 archive bytes保留 |

全倉文件檢查、DocGraph、artifact status、diff檢查及C／C₂ seed17重播
已實際通過；`lake build`完成8,831 jobs，僅既有lint warnings，未新增
Lean theorem。[整合檢查logs](checks/navigation_checks.json)記錄最後實跑
命令與結果；[先前整合檢查](checks/interim-successor/integration_checks.json)
亦保留。artifact status是manifest／fingerprint狀態，不取代byte-check或數學證明。
附加包檢查首輪的自引用結果檔尚未落盤與no-index exit-code分類問題
另保留於[navigation-attempt1](checks/navigation-attempt1/README.md)，修正後
重跑通過；這些是audit打包檢查，不改寫任何原數學或byte-check結果。

```bash
python3 audits/2026-10-04-task-d2/a/audit_a.py --repo . --output /tmp/task-d2-a
python3 audits/2026-10-04-task-d2/a2/audit_a2.py --repo . --output /tmp/task-d2-a2
python3 audits/2026-10-04-task-d2/b/audit_b.py --repo . --output /tmp/task-d2-b
python3 audits/2026-10-04-task-d2/b2/audit_b2.py --repo . --output /tmp/task-d2-b2
python3 audits/2026-10-04-task-d/identity/audit_identity.py --repo . --output /tmp/task-d2-identity
python3 audits/2026-10-04-task-d2/run_validation.py --repo . --output /tmp/task-d2-checks --scope integration
```

完整整理紀錄：[history](../../docs/history/2026-10-04-task-d2-integration-audit.md)。
交付文件hash表見[DELIVERY_SHA256.json](DELIVERY_SHA256.json)，表本身不列自身hash。
HEAD仍`0e38127`，未commit／push；本輪停在文件一致與獨立有限稽核。
