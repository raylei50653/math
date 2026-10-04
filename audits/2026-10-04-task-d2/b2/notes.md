# D₂ 後續 B₂ 獨立稽核

最終核對輸入為 `/tmp/math-task-d2-successor-v2`。B₂作者收尾後新
producer與新artifact的hash改變；初版snapshot的獨立audit、原兩seed
replay、scripts、results及logs完整留在 [v1](v1/notes.md)。本層結果以
v2為準，舊B與所有歷史artifact原bytes保留。

本層的 [audit_b2.py](audit_b2.py) 與
[independent_core.py](independent_core.py) 只用標準庫及新audit本身
的MRV回溯、原邊witness核對、rotation tracing與Tarjan block分解。
不import任何producer枚舉器、join helper或validator。程式支援任意
`--repo`與`--output`。

```bash
python3 audits/2026-10-04-task-d2/b2/audit_b2.py --repo /tmp/math-task-d2-successor-v2 --output audits/2026-10-04-task-d2/b2
```

[results.json](results.json) 的 `all_checks_passed=true`；精確計數與
input SHA256见该文件，實跑見 [run.log](run.log)。

## 明確新增覆蓋

| 新增範圍 | 獨立稽核實計 |
| --- | ---: |
| 七具名跨側contacts身份及實際共享頂點 | 7 |
| W933-101／W941-139的完整原frame、短face及來源欄位逐JSON相等 | 2；原長face保留 |
| 全拒絕列完整root-pair relations／actual附件owner交集表 | 7 relations／8 tables |
| 已存原disk rotations／D₅搬運rotations與完整mask／完整root-pair relations | 4／40／400 |
| leaf-owner身份、actual adjacent hubs、actual外部path及七身份相容ledger | 4 |
| 同列所有literal pairs的exact private palettes／缺色owner signatures | 48／4 |
| 完整degree relation controls／literal rows／完整四接點R_C | 14／140／140 |
| 獨立完整六角色joint及G−C root-pair關係 | 840 |
| 獨立pinned root-pair fibres，包含逐份獨立pinned重算的空fibres | 13,440，其中10,372空 |
| 原spoke省略／接回 | 560 |
| 原字面root-swap全圖relations及fibres | 420 |
| 獨立全域S₄ R_C重算／joint variant controls／逐份transformed witnesses | 3,360／20,160／183,312 |
| 完整degree leaf K₅ controls／獨立原C block-cut分解／actual paths／十對原邊 | 7／7／10／70 |
| 另存conditional K₄直達／長tethers K₅ controls／actual tether paths／十對原邊 | 2／8／20 |

Payload完整掃描得到 **9,598份** `tuple`＋`coloring` witnesses：1,960
份R_C與7,638份joint。所有原vertex order、literal boundary row、所有
原邊及ordered port tuple均逐份核對，沒有漏掃witness-bearing物件。
原完整relations、各16-pair keys及fibres、source identities和ledger
arrays先檢重複再比較完整内容，不只比set大小。

所有實際boundary附件、原owners及跨側共享contact aliases從同一
原圖邊另行重建。14 relation圖與7 complete-degree leaf minor圖共
**21原圖結構**逐份核對degree與actual supports；共享joint tuples
有5,840份，坐標始終指同一原頂點。7 leaf minors包括nonowner的原
leaf長度3／5／7、a-only／b-only原triangle、Pstraight／Pcross共享
triangle；所有stored原blocks與新Tarjan分解相等。較長nonowner兩
private paths保留為connected bags，各原邊與連通性均核對。

另核對q=01021單列不足以排a-only附件{2}：它對該列所有合法pairs
仍injective，但原row6的q=01212有合法pair讓外鄰同色，排除此同一
實際附件。缺色membership比較使用同一原圖與共同literal色框，未
各自重命名不同pairs。完整frame仍保留長envelope {0,4,3}，沒有把
兩份短face零serialized residual改成整個B的20／20骨架消失。

## 最終v2原checker重播

最終snapshot的B₂原checker default與seed17皆byte-check PASS，分別
**2.081秒／1.822秒**，詳見 [replay-results.json](replay-results.json)、
[default log](replay-seed-default.log)、[seed17 log](replay-seed-17.log)。
初版兩seedPASS仍留在v1，未覆寫。v1→v2完整payload差異由root
整合稽核另記；本層對兩版本都完成固定payload獨立核對。

## 精確限制

兩個具名短face的「任意大小原K₅來源排除」由B₂紙面proof與既有
degree-list theorem承擔。有限controls獨立核對實際序列化graphs、
relations、empty fibres、paths及minors，並不證任意大小Gallai leaf
存在、blockwise-uniform lists或source拓撲。Leaf-owner完整七身份
ledger是必要角色限制；不是新來源catalogue。

14 relation圖不宣稱disk、targetΣ或Σ-critical；560單spoke省略行
在本層有限圖均非空，但不以此替代B有完整source前提的任意大小Ω
引理。7 leaf minors核對完整degree提取controls；2 K₄tether圖保留
未補degree邊，僅為條件式原path certificates。没有由q-minimality
偷推出每個pinned pair後的C逐邊minimal，也不宣稱minor操作保持
R_C／joint／Σ／boundary state。

原B七身份、九份q-core表與Ω論證以逐JSON相等承接，未重新證明其
任意大小內容。W933-101／W941-139原長face、其他原faces、mixed22
整型、ε≥3、一般出口及K∞=K≤5仍保留；沒有新Lean theorem。本層
只新增獨立audit，不改production checker、原artifacts或歷史hash
FAIL，不執行commit／push。
