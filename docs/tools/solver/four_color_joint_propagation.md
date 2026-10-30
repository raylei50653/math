# 九點共同限制的自動找型與主傳播

2026-10-25。接續[九點構型共同限制登記](four_color_joint_constraints.md)。
本輪先記搜尋與核對範圍，再實作量測；目標是在未固定九點圖首次消元前，
實際產出 `0=6=9` 的共同表，並核對全部合法解保留。

## 搜尋與因子接入

新增可選 `use_joint_constraints=True`。掃描只讀同一原圖的頂點與原邊，
以原度數及已映射鄰點的共同鄰點縮小候選，逐步建立九個角色的單射映射；
選擇當前候選最少的角色，並按輸入頂點次序搜尋。所有21條必要原邊仍由既有
手動映射檢查器逐一核對。不使用預存的原頂點號、候選色、固定色或圖族名稱作辨識。

這是非誘導原子圖辨識，允許額外原邊與外側附件。同一個三點等色接口按輸入位置排序，
重複映射只保存一份有完整原邊證據的因子。等色關係對接口置換對稱，因此可排序；
完整角色映射及21條原邊仍與該份證據一起保留。

找型在首次傳播與消元以前執行一次，將每份匹配的三元四列表直接加入原有因子網路。
原邊、固定色及其他因子全部保留；既有候選域傳播、完整接口交集及精確消元共同使用它。
未固定時三點的單點候選域可以仍是全部四色，等色資訊保存在完整關係中。
固定其中一點後可以縮限另外兩點候選，但不提前寫色。

## 預算與正確性界線

預設至多128份不同接口，搜尋最多200,000個計數階段。搜尋每一計數階段計入主工作預算，
新增四列也先完整計算、檢查儲存上限，才提交該份因子。新增列與既有條件原環／消元列
共用累積儲存上限；中斷不提交半張共同表。

可選搜尋上限只略過尚未取得的必要因子；已找到並驗證的完整因子仍可使用。
零上限可退回原精確求解器。主工作或儲存上限則回傳 `limit`，不當成無解。
`complete` 僅表示此具名九點構型的映射搜尋完成，不能推成全部跨區共同限制的覆蓋。

任一合法整圖解限制到匹配的21邊原子圖，必滿足已證明的三點等色關係，
所以其完整三元列一定被保留。加入因子不改原圖共同解集；原有可靠縮域與完整消元
再維持相同解集及回填不變式。額外附件可能排空共同解，必要因子非空不保證全圖有解。

## 預先核對範圍

使用30份具名原圖／固定色條件，比較既有交集＋原環＋鄰域共同條件模式，
與再加入自動九點共同限制的模式；關閉已知衝突捷徑及額外C₅以隔離新因子效果。
範圍為未固定九點、原異色固定例、四種單點相容固定色、外接葉、重新編號及次序反轉、
額外 `0–6` 原邊，以及21份逐一刪必要原邊的控制。

每圖只由原邊及固定色獨立枚舉全部解，保存完整參考清單；逐份核對候選域、
消元輸入因子、完整回填fibres及新因子列。未固定主例必須在首次消元前輸出
`(0,6,9)` 的四個全等列，且三點仍未寫色；異色固定例預期零消元判否。
相容固定色應在消元前縮限三點候選，額外原邊則由完整接口交集共同檢查。
正常／seed-17 使用新輸出目錄重播，保留來源快照，不覆寫前輪具名原型證據。

## 實際結果

[30份原圖／固定色條件](../../../artifacts/four_color_joint_propagation/inputs.json) ·
[全部原邊解參考](../../../artifacts/four_color_joint_propagation/references.json) ·
[完整比較摘要](../../../artifacts/four_color_joint_propagation/report.json) ·
[60份完整記錄](../../../artifacts/four_color_joint_propagation/runs/) ·
[代表案例重播](../../../artifacts/four_color_joint_propagation/index.html) ·
[驗證收據](../../../artifacts/four_color_joint_propagation/verification.json) ·
[來源快照](../../../artifacts/four_color_joint_propagation/baseline-source/)

兩模式各30份執行均完成，皆為28份可解、2份無解；沒有主工作或儲存超限、
事件截斷或這批具名找型搜尋截斷。全部判定符合獨立原邊枚舉。

| 同一原圖及條件 | 加共同限制後、首次消元以前的結果 | 全部合法解核對 |
| --- | --- | ---: |
| 未固定九點 | 自動輸出 `(0,6,9)` 的四個全等列，仍未選共同字面色 | 48／48 |
| 固定 `0=0,6=3` | 矛盾由4次消元提前至0次 | 0，與獨立無解參考一致 |
| 四種 `0=c` 的單點相容固定色 | `6、9` 候選同步縮為 `c`，仍未寫色 | 每種12／12 |
| 外接中心葉 | 原九點仍產出同一必要等色關係 | 144／144 |
| 非連續原ID、反轉頂點次序 | 依角色重新找到同一共同接口 | 48／48 |
| 額外原邊 `0–6` | 與完整接口交集共同判否，4次消元提前至0次 | 0，與獨立無解參考一致 |
| 21份逐邊刪除 | 不誤套此型，保留各份異色反控制 | 全部原邊解保留 |

未固定主例由12份等價映射去重為一份三元因子，找型1,831步，之後完整提交四列。
記錄明確位於深度0及首次 `eliminate` 事件之前；未固定三點的單點候選仍為全部四色，
限制由完整表保留。之後主求解器仍完成九次精確消元及回填以取得一份合法整圖染色，
不將提前得到等色表混作免消元的完整可解證書。

30份條件合計保存3,168份完整解記錄，跨條件可以重複。兩模式逐份檢查所有縮域快照、
消元來源域、輸入關係及完整回填選項；新因子的原始列及事件列也另逐份核對。
新模式保存的64,512次輸入關係membership與28,656次回填選項membership均通過。
無解兩例的解保留核對是空集合情形；另有完整原邊窮盡參考支持其判否。

195項相關測試通過，包含新增[11項接入測試](../../../tools/tests/test_four_color_joint_propagation.py)，
保存[完整測試紀錄](../../../artifacts/four_color_joint_propagation/tests.log)。
測試另隔離停用交集／原環／已知衝突時的等色輸出，並涵蓋多構型、去重、零搜尋上限、
查詢及四列提交前中斷、累積儲存上限。所有縮域階段均未替未固定點寫色。

正常／seed-17 的四份輸入／參考／摘要及60份gzip記錄共64檔逐位元組一致，
另19份來源快照也逐位元組一致，並與當輪來源及摘要hash相符。
播放器將共同限制顯示為三點等色；[介面核對](../../../artifacts/four_color_joint_propagation/viewer-verification.json)
以Node核對JavaScript語法及原關係面板函式的10份新因子顯示。
此項採最小DOM，沒有瀏覽器版面覆蓋；Chromium在沙箱內因`shutdown EPERM`無法啟動。
本輪沒有新增Lean定理或重跑Lean build，也未重跑前輪四十份較大圖批次。

## 啟用與重播

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints --joint-constraints --json /tmp/four-color-joint.json --html /tmp/four-color-joint.html
python3 scripts/four_color_joint_propagation_experiment.py --out-dir /tmp/four-color-joint-replay
PYTHONHASHSEED=17 python3 scripts/four_color_joint_propagation_experiment.py --out-dir /tmp/four-color-joint-seed17-replay
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

Python API為 `solve_constraints(graph, use_joint_constraints=True)`，可獨立啟用，
不必先啟用C₅、原環或共同條件搜尋；若要與其他因子的完整共同接口交集，
另外啟用 `use_intersections=True`。CLI對應 `--intersections`。
`joint_max_matches`／`--joint-max-matches` 與
`joint_max_scan_steps`／`--joint-max-scan-steps` 分別控制不同接口與搜尋上限。
歷史模式仍為預設，不自動打開新推理。

這已完成已登記九點構型的自動找型與主因子傳播。其他構型、帶額外共同條件的關係學習、
一般跨區完備性及一般效率保證仍未取得。
