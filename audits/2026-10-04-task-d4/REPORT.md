# D₄：正式返回 A₃／B₃／C₃ 的固定快照、獨立稽核與文件整合

2026-10-04，接續 [D₂](../2026-10-04-task-d2/REPORT.md)與
[D₃](../2026-10-04-task-d3/REPORT.md)。基準
HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`；工作根目錄
`/home/ray/developer/ai/math`。本輪不 commit／push。

**三份新增成果的獨立稽核及最終root重播全部通過。**
使用者已正式確認 A₃／B₃／C₃ 最終工作區返回，本輪據此建立新快照；
D₃ 當時「尚未返回」及未整合的歷史敘述保持原文。

## 1. 固定快照與前輪保存

[baseline.json](baseline.json)記錄起始1,566份既有檔案SHA256與本地Git refs，
捕捉期間零漂移。851份輸入的完整bytes凍結，另補一份未列在直接hash
map、但C producer執行時讀取的capacity artifact；[補充表](snapshot_supplement.json)
確認其bytes符合最初baseline，原baseline不覆寫。
固定副本實體在`.snapshot/`，穩定入口[snapshot](snapshot/)為symlink，
避免凍結DocGraph metadata被當成live文件重複計數。

[lineage_complete.json](lineage_complete.json)核對D₂的97份及D₃的94份交付
hash表全部吻合。D₃起始後13份既有並行變更逐份記錄，hash吻合或變更
本身不作數學驗收。直接hash稽核明列D₂的28份證書加A₃／B₃／C₃，
共31份／221條hash records；只有原四份文件hash漂移，沒有非文件漂移。
本範圍不宣稱全倉每份證書皆目前有效。

## 2. 精確驗收範圍與停止點

| 成果 | 本輪要驗收的具名範圍 | 最新停止點及保留 |
| --- | --- | --- |
| A₃ | 原01／01及root交換；四rotations、三hub前提、完整C替換、(a,b,u)投影與完整六角色joint | 18／22框架、44／70支援、56／102singleton schedules；原04／04及交換為候選窄入口，未驗收其他pairs |
| B₃ | W933-101／W941-139長face{0,4,3}；跨拒絕列slack、五leaf型、shared bridges、原K₅ | 與B₂合用只登記兩primary具名骨架封閉；原20／20表不刪，其他19／19原列未新判；933原04／12共享附件{4}保留 |
| C₃ | CPP-134-1／geometry34／join20；strict-list、T／N葉、原五袋十對邊 | 只此key新關閉；與C₂合用恰兩keys，原36／140／900不刪。下一入口geometry34／join60；其他w角色及geometry35未驗收 |

任意大小紙面／外部Gallai、固定Python控制與Lean證據分開。
未知原D_w全relation不造tuples；完整same-graph relations、空fibres、
actual attachments、owner、共同色框與全witnesses保持。
ε≥3、mixed12／mixed22整型、來源實現、一般出口與`K∞=K≤5`仍未證。

### A₃：完整C替換與投影

[A₃ notes](a3/notes.md)及[results](a3/results.json)從原邊獨立核對四份
selected框架的576 rotation assignments／16 disk rotations；8原hub
instances、160合法三hub root pairs、1280 exact-list鄰點子集保持。
繼承A／A₂的完整具名identity、actual支援與全部singleton schedules亦
重新導出，保留18／22、44／70、56／102逐項原JSON。

36份完整degree圖重建2880整圖joins／46080字面fibres（38112空），
51248六角色及2400五角色witnesses；全部91639個serialized coloring
fields驗過。360份(a,b,u)投影等式、5712份只替換C而逐點保持完整外部
的witnesses、720份合法root-pair完整C fibres核對。
原ax非critical的無界論證依原互異色triangle hubs、連通外部K₄排除及
不限接點數三hub引理；未偷用mixed11 sealed triangle或q-minimality。

六角色不等負控制的原joint16／省略ax24 tuples及完整替換witness保存。
36個指定01202固定控制**全為singleton2**；singleton3的10份retained
source schedules與紙面instance另核對，沒有另建singleton3有限來源圖。
兩seed重建完整relations bytes相同，全部控制Σ1023；不證disk來源實現。

### B₃：跨列slack、五leaf型與原K₅

[B₃ notes](b3/notes.md)及[results](b3/results.json)核對52 actual附件候選、
546拒絕row／合法pair exact lists及五種有序leaf signatures。shared接0
在row1仍容許，必由row6 slack排除；其餘兩附件由row1排除，6份反證與
3份共同ledger witnesses保持。degree二shared內部橋鏈另有4次原刪邊
斷開正控制，不把shared contact一概刪去。

14＋2完整degree relation圖重建160完整R_C、960原圖joins、15360
字面fibres（11456空）。2646原R_C、11414 joint、11414 fibre witnesses
逐份核對。共同S₄的3840 R_C、額外23040直接全圖joins及273936搬運
witnesses保存同一色框。30 leaf K₅的300原鄰接／42實際外路、2條件K₄
的20原鄰接／8paths均核對五袋非空、不交、連通及十對原邊。
長nonowner固定證書的連通袋，與紙面選相鄰private點的袋構造分開。

與B₂只登記W933-101／W941-139兩primary來源封閉；W933-171／W941-279
root-swap對應僅保存transport證據，不另登記闭合。原B20／20完整必要
列不改寫，其他19／19未新判；原93304／12共享附件{4}仍保留。

### C₃：雙框strict-list、原葉與精確scope

[C₃ notes](c3/notes.md)及[最終results](c3/style-results.json)為
13579 checks／0 failures；兩seed完整結果、relations與ledger逐byte相同。
pin0的|L|−d=p·s₂排接點碰b₂；pin2 tight Gallai保留T／N兩leaf型，
先以原N葉五袋十對邊K₅排除N，才作接點葉數。無界block／bridge、
connected exterior與leaf-count論證另作紙面審查，外部原Gallai PDF及
SHA256由三audit各自保存；固定Python不形式化此任意大小論證。

八型32pins、四N模型24完整contact tuples／全部intact fibres、104
逐邊刪除的完整U² fibres、416局部及104 context partial witnesses核對；
12原bridge relations各測16endpoint pins，192fibres含全部失敗空份。
4 N-K₅、162 K₄-route minors、條件triangle六tuples／九刪邊／36局部
及9partial witnesses、兩K₅ subdivisions的原邊及路徑互斥性全部通過。
未知D_w沒有造內點染色；partial contexts不稱整份M minimality證書。

從原500 local配置、560cases、140geometries重新建立
[3500具名scope keys](c3/attempt4-default/scope_ledger.json)。只標
(CPP-134-1,30,20)與(CPP-134-1,34,20)兩keys closed，另外3498 keys
未驗收；原36／140／900不刪。固定兩keys保留literal u₀,u₁,u₂與
v₀,v₁,v₂；未知來源的其他keys只保留具名ordered contact symbols及
完整符號relations／fibres，不假設實現。下一g34／j60的side IDs=(27,1)。

## 3. 原checker重播與失敗保存

九份producer A／A₂／A₃、B／B₂／B₃、C／C₂／C₃ 的default及seed17
在固定快照重播。[attempt1](checks/original-attempt1/results.json)為16 PASS／
2 FAIL：兩份C失敗是缺少上述capacity runtime input，完整trace保留。
補入符合捕捉SHA256的原bytes後，[attempt2](checks/original-attempt2/results.json)
18份全部byte-check PASS。沒有改producer、原artifact或舊hash maps。

`lake build`已通過，logs在[lake-initial.log](checks/lake-initial.log)，
範圍含三份正式返回成果；文件整合後沒有再改Lean source，不重跑。
未新增Lean theorem，這不形式化新紙面topology。
原D的40 PASS／4文件hash FAIL、D₂版本／環境失敗、D₃ strict保存失敗
及全部中途attempts均保留原路徑。本輪打包及輔助查找紀錄另見
[packaging_notes.json](packaging_notes.json)。

最終[root replay比較](checks/root_replay_final_comparison.json)三份全部PASS；
只排除A／B的run耗時與B的output目錄，C整份結果完全相同。
沒有排除任何relation、hash、witness、count或scope欄。
初次root比較碰到C audit仍增補source/hash欄而FAIL，完整
[失敗比較](checks/replay_comparison_attempt1.json)、舊輸出與C全部五版
source／attempts保存；等待final source凍結後再重播，未刷新原artifact。
初次control-file review錯把三份新增成果當成三份大型manifest條目而
FAIL亦留[原結果](checks/control_review_attempt1.json)；實際只有A₃／B₃
兩份大型登錄，C₃是直接保存的小artifact，原entries完全不變。
初次[package檢查](checks/package-attempt1.json)的links零錯誤，但C audit
helper末尾多一空行而whitespace FAIL；原source／attempts完整保存。
active helper只修EOF格式後重新核對；歷史attempt sources按原hash保存，
不為取得當前格式PASS而改寫凍結版本。
修復後兩seed的relations／scope ledger與修復前逐byte相同，results只
變helper的source hash；七份C版本與新style-freeze各自保存，最終root
再比包含全部source hash的完整結果，全部相同。
15份本輪文件delta另用`git diff --no-index --check`逐份驗證，含起始
已untracked的專題及新history；全部零whitespace diagnostics。初次
harness誤將no-index代表「有差異」的exit1當FAIL，原結果
[保留](checks/document-diff-check.json)，精確退出碼解讀見
[最終diff核對](checks/document-diff-check-final.json)，沒有修改文件來掩蓋此失敗。

## 4. 文件與重播入口

README、STATUS、Kempe及weak-deletion guides、synthesis與專題後續前綴
同步至本輪驗收範圍。HANDOFF維持薄索引，研究線與tags未改，原bytes保留。
歷史專題正文、checkers、artifacts、history及舊audit包不覆寫。
13份並行更新的人工逐項核對見[document_review.md](document_review.md)，
14份本輪既有文件的SHA256與精確diff另存，不以既有並行更新直接算驗收。

獨立重播使用各子包的新output路徑：

```bash
python3 audits/2026-10-04-task-d4/a3/audit_a3.py --output audits/2026-10-04-task-d4/a3/replay-fresh
python3 audits/2026-10-04-task-d4/b3/audit_b3.py --output /tmp/task-d4-b3
python3 audits/2026-10-04-task-d4/c3/audit_c3.py --output /tmp/task-d4-c3
```

```bash
python3 audits/2026-10-04-task-d4/run_validation.py --repo . --scope original --output /tmp/task-d4-original
python3 audits/2026-10-04-task-d4/run_validation.py --repo . --scope navigation --output /tmp/task-d4-navigation
python3 audits/2026-10-04-task-d4/audit_lineage.py --repo . --output /tmp/task-d4-lineage.json
python3 audits/2026-10-04-task-d4/audit_bundle.py verify --repo . --result /tmp/task-d4-preservation.json
python3 audits/2026-10-04-task-d4/validate_package.py --repo . --output /tmp/task-d4-package.json
```

每次使用新的output路徑，保存先前失敗。`audit_bundle.py capture`不允許
覆寫已存在baseline；接續研究讀兩份guide的具名窄入口。

全倉文件检查為530 Markdown／5505 local links，DocGraph為62文件／
213 relations／5 families、零錯誤，artifact status為ok=143，tracked
diff檢查通過；D₄自身新文件／active source的links與whitespace另檢查，
archived sources保持原bytes並逐份記SHA256。[保存結果](checks/preservation-final.json)
確認1552份既有檔案bytes保持、14份文件改動已明列、protected變更零；
852份固定輸入與HEAD／origin/main本地refs均不變。

本輪未重跑D₂四層全部150圖的獨立MRV整包或D₃全部14,000側joins整包；
前輪證據按已封存交付沿用，新層另作獨立驗收。沒有重開來源catalogue、
R系列、一般出口、Lean axiom audit或remote fetch。實際checks見
[原producer重播](checks/original-attempt2/results.json)、
[整合檢查](checks/navigation-attempt1/results.json)及各子audit原attempts。
本包所有新檔、固定副本、source版本及成功／失敗attempts最後以
`DELIVERY_SHA256.json`封存；表不列自身hash，可用
`python3 audits/2026-10-04-task-d4/seal_delivery.py verify`唯讀核對。

**D₄停止於三份正式返回成果的條件式驗收、版本保存與文件整合。**
下一窄入口：A原04／04及root交換候選；B原93304／12共享附件{4}；
C為CPP-134-1／geometry34／join60、side IDs=(27,1)。這些入口本輪未分析。
最新导航與完整前提由兩份guides維護，未commit／push。
