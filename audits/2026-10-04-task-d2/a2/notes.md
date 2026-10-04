# D₂：A₂ 01／12 successor 的新增完整稽核

最終輸入為 `/tmp/math-task-d2-successor-v2`，版本及 byte 邊界見
[results.json](results.json) 與 [原 checker 重播](original_replay_results.json)。
獨立 [audit_a2.py](audit_a2.py) 只使用 stdlib 及前輪獨立
[audit_a.py](../a/audit_a.py) 的 MRV／身份工具；沒有匯入 production
enumerator、named_frame、join、subdivision finder 或 witness validator。
全部新增稽核 PASS，production files／原 artifacts 沒有被本 audit 改寫。

| A₂ 新增 ledger coverage；含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| 從完整 A 身份域繼承的原殘留 | 22 | 26 |
| 只移除原 01／12 frames | 2 | 2 |
| 完整原 frame／source fields 保留的其餘殘留 | 20 | 24 |
| 保留 actual U face／support records | 52 | 86 |
| 保留完整 singleton schedules | 68 | 124 |
| 01／12 繼承 actual U support records／schedules | 4／4 | 6／6 |

重新執行前輪獨立 A 身份 audit，確認原 70／90 source-filtered 域及原
22／26 residual arrays；A₂ fresh-selected、inherited、excluded、remaining、
root-swap 及 source-mask 陣列另查重，每份剩餘完整 frame 與原 A 逐字面
JSON 相等，沒有 set 化後只核對總數。A₂ 選定完整 frame 四份、原 actual
support 十份的完整 singleton schedule 都是 {2}；每份 source mask 均在
row 4 拒絕 01202。其餘 A 的 domain、D₅ schedules／rotations 稽核重播
屬「繼承 A revalidation」，沒有算作 A₂ 新的數學排除。

| A₂ 新增 topology／完整圖／relations／witness coverage | 數量 |
| --- | ---: |
| 原長 face C actual support 全部 subsets | 64 |
| 原 contracted-path K₃,₃ certificates／9-path witnesses | 12／108 |
| 兩種 C 位置的三-hub premise instances／hub adjacency witnesses | 8／24 |
| 原外鄰所有 subsets 的 exact degree-list local controls | 64 |
| actual U support 缺 2 的完整 source-support conflict screens | 16 |
| 固定完整 degree 圖；x 獨立／共享 y₀／共享 y₁ | 36；12／12／12 |
| 全部十列完整 C ternary／U unary relations | 360／360 |
| C／U tuple witnesses | 3,600／912 |
| 原與各 edge omission 完整六角色 joints／witnesses | 2,520／57,264 |
| 整份 U 省略完整五角色 joints／witnesses | 360／3,240 |
| 六、五角色完整 joints 合計 | 2,880 |
| 16 個字面 root-pairs 的完整 fibres／空 fibres | 46,080／37,020 |
| 獨立 complete-relation joins 與全圖回溯交叉核對 | 2,520 |
| 原 spokes、ax、au 精確接回 | 2,160 |
| G−au=T_N×R_U 完整乘積／singleton identity | 360／360 |
| actual attachment paths／同一 U 的 a-to-2 crosscuts | 192／36 |
| 包含整份 U 省略的完整 variant Σ masks | 288 |
| q=01202、固定 (a,b,u)=(3,0,2) 的完整 C extension | 36 |
| 同一指定列重複保存的完整 records 也各自驗證 | 72 |
| 整圖 root-swap pairs／完整 literal joint checks | 18／1,440 |
| root-swap 全份 coloring witnesses | 30,252 |
| 所有新增序列化 coloring 欄位逐份驗證 | 81,559 |

每份 K₃,₃ 的 branch vertices、九對 endpoints、原邊、simple paths、
互斥 path interiors 均獨立核對；沒有匯入原 subdivision validator。
三-hub bags 的互斥、連通、三條實際 adjacency 與原外鄰到 hub 的 mapping
逐項核對。這些是固定拓撲／list 前提控制，不把原 paths 收縮當成保持
Σ 或完整 joint 的 source-state 操作。

最後一項以遞迴計數全 artifact 的 `coloring` 與
`omission_only_full_coloring` 欄位，確認和實際驗證次数完全相等；包含
15,944 份 edge 接回 removed tuples 的 witnesses、兩份 designated-row
records 及負控制重複保存的 witnesses。Boundary、所有原邊、字面 ports
及共享原頂點都逐份核對；完整空 fibres 保留，沒有乘 marginals。

[counterexamples.json](counterexamples.json) 另保存原 graph／指定 row／
ports 及整份原 witness：第一份 control 的真 guarded C fibre 為空，
marginals 有八份假 tuples；原 joint 有 16 份、ax omission 有 24 份，
省略專有 tuple 與 full coloring 均保存。兩份負控制的 root-spoke
eligibility 或 relation-equality scope 沿用原明示界線。

36 張固定控制的原完整 Σ 獨立算得全部 1023，沒有 933／941 source
realization。長／短 face 的任意大小 crosscut、slack/tightness、Gallai
block-palette、連通外部 K₄ 排除與三-hub extension 仍是原紙面依賴，
本 audit 沒有重新證明外部定理、disk realization 或 Lean topology。
01／12 的任意大小來源排除屬原 A₂ 報告的條件式紙面成果；其餘必要域
仍 20／24。Mixed12 整型、ε≥3、一般出口與 K∞=K≤5 均未證。

原 v1 凍結輸入的 audit 與 default／seed17 原 checker 均 PASS，完整
輸出保留於 [v1_snapshot/results.json](v1_snapshot/results.json) 與
[v1 重播](v1_snapshot/original_replay_results.json)。最終 v2 生產 checker
多綁定依賴 hash；本 audit 獨立確認全部 12 個 bound inputs 目前相等。
V2 default／seed17 重播均 exit 0，耗時 11.251／10.579 秒；A₂ artifact
SHA-256 前後均為
`a69f6d8fd188acb1f414885b7d04303cc0163dd2efe9b4821320b7143d00ccf4`。
原 A／generic source artifacts 前後亦保持原 bytes，未 commit／push。

```bash
python3 audits/2026-10-04-task-d2/a2/audit_a2.py --repo /tmp/math-task-d2-successor-v2
python3 audits/2026-10-04-task-d2/a2/audit_a2.py --repo /home/ray/developer/ai/math
python3 audits/2026-10-04-task-d2/a2/replay_original.py --repo /tmp/math-task-d2-successor-v2
```

獨立 script 的輸出只寫在本 audit directory；`replay_original.py` 同样
只寫新的 logs／results，原生產 checker 始終以唯讀 `--check` 執行。
