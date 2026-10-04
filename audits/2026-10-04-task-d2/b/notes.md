# D₂ 新增 B 獨立稽核

本層讀取 `/tmp/math-task-d2-snapshot` 的固定 math 輸入，只新增獨立
audit、結果及 log；未修改 producer、helper、原 artifacts 或歷史紀錄。
`audit_b.py` 支援任意 `--repo`、`--output`，只 import Python 標準庫。
它從序列化原邊另寫 MRV 回溯，不呼叫 producer 枚舉器、join helper
或 witness validator。

```bash
python3 audits/2026-10-04-task-d2/b/audit_b.py --repo /tmp/math-task-d2-snapshot --output audits/2026-10-04-task-d2/b
```

結果為 `all_checks_passed=true`；[results.json](results.json) 保存精確
具名 indexes、計數、輸入 SHA256 與範圍界線，實跑見 [run.log](run.log)。

## 明確新增覆蓋

| 新增核對範圍 | 獨立稽核覆蓋 |
| --- | ---: |
| 七份跨側共享身份 D4／S00／S01／S10／S11／Pstraight／Pcross | 7 |
| 從來源原陣列獨立篩選的具名 (2,2) 必要骨架 | 47／75 |
| 同色 spoke 原拒絕列見證／排除骨架 | 84 份見證；22／50 骨架 |
| 相鄰 spoke-pair 域／sealed equal-pair 排除／具名保留 | 25／25；5／5；20／20 |
| 每階段所有 carried 身份出現、四個原來源欄位及 source_sigma | 122；488；122 |
| 完整原 G−C root-pair relations／非空 Ω 行控制 | 1,220 原必要骨架行；280 固定圖行 |
| 同時搬運原 rotations、完整 Σ、row、literal roots／四色框 | 1,220 D₅ rotations及 masks；12,200 root-pair relations |
| 原 root-swap transported rotations／canonical face 集不協變的保存案例 | 122；16 |
| 25 獨立骨架的全 rotation assignments／disk rotations | 2,320／60；兩 masks carried 120 rotations逐份核對 |
| 保留原 face／完整 actual附件 owner必要表／候選附件子集／容許子集 | 60／240／2,240／696 |
| degree admissible q-core 身份算術／原 factor 子集 | 9／32 |
| leaf-owner 缺色 membership signatures | 4 |
| 條件式原 K₅：連通互斥 bags／原 arms／actual tethers／十對原邊 | 14 minors；42 arms；42 tethers；140 interbag edges |
| 完整 degree 原圖／literal rows／完整四接點 R_C | 28／280／280 |
| 完整原圖 joints／獨立完整 R_C guard joins | 1,680／1,680 |
| 完整 pinned root-pair fibres，含逐份獨立 pinned 重算的空 fibres | 26,880，其中 21,008 空 |
| 三接點原 carrier joins／原 spoke 接回 | 1,120／1,120 |
| 字面 root-swap relations及fibres | 840 |
| 獨立全域 S₄ R_C 重算／joint variant controls／個別 transformed witnesses | 6,720／40,320／560,736 |

完整掃描 payload 的所有 `tuple`＋`coloring` 出現共 **45,178**，每份均
核對四色值、原 vertex order、同一 boundary row、所有原邊及原 port tuple。
其中 R_C 4,200、完整 joint 23,364、carrier 17,608、另存 marginal
負見證 6；沒有只檢大小或 set 化後忽略重複。來源 frames、各 status
partition、residual indexes、relations、所有 16-pair fibre key arrays及
q-core factor arrays均先查原陣列重複。所有實際 boundary附件、完整
owner edges、共同原 contact aliases由原圖邊重建後比對。

跨側 alias 的固定 controls 有24圖，核對2,800份共享 R_C tuple及
14,872份共享 joint tuple。Control20、Pstraight、q=01012、roots=(2,3)
的四個 marginals都為 `{1,2,3}`，而完整 fibre 空；六份原 C witnesses
逐份合法，負見證未被 marginals取代。933原04／12、W933-129長 face
的共享 contact actual附件 `{4}` 給 `deg_C=1`，另存結果以阻止把所有
保留 faces 都說成 `min deg_C≥2`。

原 rotations隨 relabeling搬運後逐份合法；不要求另一個 independently
chosen canonical rotation相同。完整 D₅ mask images實算為
933→{933,934,940,948,996}、941→{941,949,950,998,1004}；没有把
933→940偷換為941，也沒有維持錯誤原 mask。

## 原 checker 重播

固定 snapshot的原 mixed22 checker兩次 byte-check均 PASS：default
4.222秒、`PYTHONHASHSEED=17` 4.280秒。詳見
[replay-results.json](replay-results.json)、[default log](replay-seed-default.log)、
[seed17 log](replay-seed-17.log)。重播會沿用 producer重算其依賴的完整
three-contact／three-hub payload；這是原 replay evidence，與本層不
import producer的獨立稽核分開。沒有以重生成清除任何歷史 hash FAIL。

## 精確限制

九份 q-core 身份是指定「四原 spokes＋整份 C」factor模型的完整
degree算術表。C只能全取、原 root／ab刪除全收、(4,4) source排除、
單 spoke省略任意大小Ω、每個拒絕q的q-core必為G，都仍由 B 紙面
飽和論證與既有 two-spoke三接點定理承擔；本層沒有把有限表稱為
那些任意大小定理的獨立證明。

28張原完整 degree controls不具 disk／完整Σ／Σ-critical前提。
其1,120份單spoke省略行中實有 **48空joint行**，已完整保存並核對；
這不反駁有完整source前提的紙面Ω引理，也不能從有限controls普遍
推出Ω。G−C的280固定行皆非空，是另一个直接 root-pair控制。

附件表與leaf-owner signature只驗證序列化的必要限制；Gallai theorem、
任意大小leaf uniform palettes及topology未另行形式化。14 minors只
核對已存條件式提取圖的原邊、bags與paths，不證其來源必存在、不
補 unused arm degree。20／20是具名必要骨架，未視為來源catalogue。
本層不證整個mixed22排除、ε≥3、來源實現、一般出口或K∞=K≤5，
不新增Lean theorem，不宣稱短／長原圖relation等價。

後續 B₂ 成果另以 `../b2/` 的successor snapshot獨立稽核；本層原結果
與原停止點數字保留。
