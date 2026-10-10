# N45-PC source proposal 介面

從研究根目錄使用以下只讀命令。輸出為完整JSON，寫stdout；輸入不更動。

```sh
python3 -B audits/2026-10-09-n45-pc/checker.py --source audits/2026-10-09-n45-pc/controls-v2/NA7-0002-P1.json
```

此真實固定control缺LP前提，所以實際exit2／`not triggered`。
[控制proposal](controls-v2/NA7-0002-P1.json)可用來理解格式；其中L／S為null表示沒有宣告，不能填成LP正控制。
後續以自己的proposal路徑替換命令最後參數；不需重新生成固定certificate。

| proposal欄位 | 規則 |
| --- | --- |
| schema | 字串`n45-pc-v1` |
| graph_file | 相對於proposal所在目錄解析，或absolute path；只讀原graph JSON |
| source_sha256 | graph_file的完整原始bytes SHA256，不能使用重新排版或只edges的hash |
| frame | 五個原具名頂點，按外框順序；全rows共用此order，任一D5調整必一起搬整個frame |
| roots | 两個原具名roots的順序，全relation fibres用此order；r由所宣告U的owner辨識 |
| pieces | 全部H−roots完整原components的declarations；id/vertices列完整components，contact_order為實際contacts的一次排列、shared vertex只有一coordinate。contacts、owners、support、attachments、internal_edges、incidences、kind、one_sided、shared_contacts、original_internal_bridges等若供給都與原邊核對；缺的metadata由原邊重建 |
| roles | U、L、S各指向不同piece id；完整source contract要求三個都供給。L真long、S真edge-pair由原support另核；即使其他LP前提不足，錯的partial L/S/U宣告也拒絕 |
| beta | 五個字面色，依frame次序，colors為0–3，必proper；不逐piece或逐row獨立S4正規化 |
| X | 原G省略整個V(U)後的完整vertices、edges；都按工具canonical排序，以完整原identity比對，不能只給core degree摘要 |
| critical_witnesses（optional） | 每條原非框邊恰一record，`edge,index,full_lift`；原G拒絕index、G−edge接受該literal row，original vertex order的full_lift逐原邊驗證。缺時由原邊自行構造，不假設criticality |
| beta_deletion_witnesses（optional） | X每條retained非框邊恰一record，`edge,full_lift`；X vertex order且同字面beta，逐原邊驗證。缺時自行構造並驗minimality |

原graph JSON至少`id,vertices,edges,rotation`。頂點可為整數或字串，但不能有整數v與字串"v"
同時出現，rotation的JSON keys必一一對到原vertex，值為該原點完整cyclic neighbor order。
省略rotation可計算部分介面，但disk／完整來源不觸發。有效圖忽略原degree0內點，明列其identity；
full lifts仍使用完整供給的vertex set，沒有刪掉它們來取得假full lift。

工具canonical vertices為整數升序後字串字典序；無向edges的兩端與edge list依相同order排序。
contact_order可以為任意指定的一次排列，tuples／fibres需跟這份order一致。
shared contacts與所有attachments/support/bridges由**同一份原邊**重建；不使用marginals。

若piece供給`rows`，必有十個PATTERNS order的完整row。每row包含`index`（optional，若有須正確）、
`tuples=[{"tuple":[...],"lifts":[全部piece colors]}]`與16個
`fibres=[{"pins":[r_color,s_color],"tuple_indices":[...]}]`，lexicographic color order且包含空fibres。
`F`或legacy `available`若供給也完整比較；available只列原owners。
row順序為`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
沒有供給rows時依原圖重建所有tuples/lifts/fibres，不接受只有marginal palettes代替完整資料。
legacy raw shield只取具名edges作核對；canonical shield另有`complement_face,length`，若宣告亦須一致。
BASE舊shield的額外summary欄不是新lemma前提，本工具另從原rotation重建盾弧。

輸出包含每層status與`missing_sufficient_premises`、具名graph/rotation、完整原piece relations、
整圖十列all_16_fibres/all full_lifts、每原非框邊critical witnesses、整U省略與G−rx的不同full lifts、
literal beta的retained-edge witnesses、zero-slack columns及每Delta gamma singleton forcing。

exit0：這份供給的named source完整契約`triggered and holds`，只表示有限source符合已列前提，
沒有承擔不存在性或任意大小paper。
exit2：缺完整LP前提（`not triggered`），或錯資料被拒絕（`counterexample`是declared input finding）。
中止／其他計算失敗：沒有可採納判定，不能当PASS。

固定replay使用`--check`，exit0是certificate bytes相同；stdout亦明示LP未觸發。
`--generate`只為首次固定交付保留，目標final-v2已存在時立即拒絕；不用它處理新proposal。
來源實現與任意大小closure仍由原paper／獨立監督判定，見[REPORT](REPORT.md)。
