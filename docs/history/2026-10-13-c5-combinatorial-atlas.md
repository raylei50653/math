# C5 組合、對稱與可實現關係圖譜整理

後續發布：使用者其後授權整理並 commit + push；K14 的當前入口及本次驗證見
[整合發布紀錄](2026-10-13-k14-rank4-atlas-publish.md)。以下保留原輪次語境。

2026-10-13。使用者要求整理、重算、驗證及可視化既有 C5 relation 研究；
未要求證明一般 `K∞=K≤5`，未授權本次 commit／push。
來源 main 為 `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。

## 交付與分類結論

新增[正式入口](../archive/reports/c5/structure/c5_combinatorial_atlas.md)、
[產生器／checker](../../scripts/c5_combinatorial_atlas.py)及
[圖譜產物](../../artifacts/c5_combinatorial_atlas/atlas.json)。
圖表、HTML、CSV 與核對報告由同一份生成資料產生；原研究程式、witness 圖及
proof artifacts 只讀，原帶標號 Σ key 與邊界對齊語義保留。

重算結果為240個proper邊界染色、10個S4類、1,024個十bit子集合、
1,023個非空masks、135個D5類。D5 orbit size為1／5／10的類數為3／60／72，
Burnside固定非空mask總數為`1023+4·3+5·63=1350`，平均為135。
全部非空masks唯一分到一個orbit，各類保留全部members、stabilizer及等價轉換。

重播既有必要條件得到153個Kempe通過masks／29類，
142個exterior通過masks／26類；已知132個單側disk關係／24類、
未知10個masks／2類。全部135類分成106個Kempe拒絕、3個exterior拒絕、
24個known disk、2個OPEN。132份保存圖各重算完整Σ與boundary-apex planarity。
此輪沒有跑新graph DFS，也沒有把`142→132`當作已證必要條件。

## 同一原框與結構描述

canonical只新增為圖譜索引，不替換既有Σ。已知95與123屬同一D5類，但
原框交集為91；各自改成canonical95再交集則得到95，會改變接合結果。
原始mask、相對D5轉換及字面邊界位置因此完整保留。

132個已知單側關係的兩側對齊交集可產生全部1,023個非空masks；
此項明標為separating C5雙側關係，沒有宣稱全部都可由單側disk實現。

額外描述包括三色singleton support、四色重複色位置對、pair forcing、
chord-compatible、同原框包含／交集／聯集，以及保存witness的attachments、
內部邊、分量與degree指紋。它們不被採納為一般結構或實現性定理。
內部誘導圖另對全部k!個私有頂點置換取最小邊碼，得到12種已選witness骨架；
同一已知D5類的保存圖共用骨架，但同一骨架可對應多類，框附件／chords仍須完整保留。
相同support不能決定relation（已知95／127），相同三色／四色數也不能
決定D5類（127／223等）；負控制隨正式入口記錄。

## OPEN 邊界與來源路由

933全收五種四色、只收一種三色；941全收五種四色、三色singleton support
為非相鄰二點。已知全收T4類的support均含相鄰pair，但一般
adjacent-singleton lemma仍未證。已知429具有非相鄰二點support且不全收T4，
故不能拿掉该前提。抽象Kempe partitions／計數向量不構成來源實現。

現有[十三內點界](../archive/reports/c5/structure/c5_k13_collar.md)`K≤13=K≤5`及其紙面／外部定理／
原有限證書保留，圖譜未重證該結果。一般來源、`K≤14`、`K∞=K≤5`、
E-ARC2與其他父題仍依[Kempe導覽](../archive/guides/c5_kempe_guide.md)維持OPEN。
本次無新來源排除、無新Lean theorem。

## 重播紀錄

生成／核對命令及逐項結果以正式入口與
[verification.json](../../artifacts/c5_combinatorial_atlas/verification.json)為準：

```bash
.venv/bin/python scripts/c5_combinatorial_atlas.py --write
.venv/bin/python scripts/c5_combinatorial_atlas.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_combinatorial_atlas.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
lake build
git diff --check
```

來源輸入paths／SHA-256由
[source_manifest.json](../../artifacts/c5_combinatorial_atlas/source_manifest.json)保存。
新checkout可從固定main資料獨立生成分類；`--check`比對完整清單及產物，
不靠本文的表格數字作驗證。既有source artifacts不因圖譜生成而改寫。

實際結果：正常及`PYTHONHASHSEED=17`重播的八份檔案逐byte相同；
隔離暫存目錄只從main的六份Git blobs與兩支新產生器重建，也逐byte一致。
原132份witness的既有checker重播零mismatches；獨立review另核对1320個
完整fibres、全部saved lifts與135個canonical投影階數。
`check_docs.py`及正式docs範圍DocGraph通過；全工作樹DocGraph保留62個
audits／scratch凍結副本duplicate-id錯誤，未修改歷史metadata。
`lake build`完成8831jobs，僅有既有linter warnings；`git diff --check`通過。
瀏覽器實測135列、10個模式圖、933查詢、OPEN與三色／四色計數篩選、
95旋轉至347及其原witness，手機版面無橫向溢出，page／console errors均為空。

文件路由新增README、state導覽與STATUS直接索引；HANDOFF研究線與進行中
狀態沒有變化，故保留。一般研究結論與OPEN邊界沒有因分類整理而改变。

本次只整理組合分類及證據索引；沒有重新枚舉大图、重播K13球面生成、
重播外部文獻計算證書或新增Lean形式化。若回歸构建成功，也只按既有Lean
回歸記錄，不提升新圖譜信任層。
