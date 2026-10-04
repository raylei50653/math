# D₂：A mixed12 新成果的獨立身份／完整 joint／witness 稽核

本 audit 以 `/tmp/math-task-d2-snapshot` 為凍結輸入，沒有改寫 production
checker、文件或 artifacts。輸出見 [results.json](results.json)、
[完整負控制](counterexamples.json) 與 [原 checker 重播](original_replay_results.json)。
獨立程式 [audit_a.py](audit_a.py) 只用 stdlib，沒有匯入 production 的
enumerator、join 或 witness validator；獨立 MRV 回溯直接列舉完整字面
colorings，保留共享原頂點及同一 boundary color frame。

新增稽核範圍全部 PASS；這些數字是本 audit 的 coverage，不新增數學來源分類。

| 新增身份／具名域 coverage | 933 | 941 |
| --- | ---: | ---: |
| 獨立 source-filtered named frames | 70 | 90 |
| 排除／保留框架 | 48／22 | 64／26 |
| 保留 actual U face／support records | 56 | 92 |
| 保留完整 singleton schedules | 72 | 130 |
| 窮盡 rotation assignments | 6,432 | 8,224 |
| 全部 disk rotations | 160 | 200 |

從通用單-spoke source 自己構造 a-pair／b-pair 域，核對全部 fresh、excluded、
residual 原陣列重複與 source fields、整份 residual frame 複本、source index
與原邊；沒有先 set 化再只核對大小。共核對 115,856 個原陣列的重複、
800 份 degree-admissible omission identities、868 份 actual-support singleton
screens、37,872 個 singleton relation rows、9,370 份明示 S₄ 衝突及 8,616
份未用色守恆衝突前提。2,056 份短支援骨架路徑逐邊核對；另外 116 份
依賴「完整來源碰齊五框點」的原 C 外路徑只核對其記錄合約，沒有把紙面
存在性當作已列舉的骨架路徑。

160 個整圖 root swaps 核對全部 500 個 U-face／support placements，owner、
C common faces、完整 schedules 及 360 個原 saved rotations。D₅ 的 1,480
完整 residual schedules 與 2,960 個隨之搬運的原 rotations 均合法；完整
source mask、row 與共同色框同時搬運。實際包含 933→940 與 941→949，
不要求另行選出的 canonical rotation 相同，也不把 source mask 固定。

| 新增完整圖／relations／witness coverage | 數量 |
| --- | ---: |
| 固定完整 degree 圖；x 獨立／x=y₀／x=y₁ | 72；30／24／18 |
| 完整 C ternary／U unary relations | 720／720 |
| C／U 完整 tuple witnesses | 6,720／1,104 |
| 原與省略圖完整六角色 joints／witnesses | 5,040／70,482 |
| 整份 U 省略完整五角色 joints／witnesses | 720／6,732 |
| 六、五角色 joints 合計 | 5,760 |
| 字面 pinned root-pair fibres／空 fibres | 92,160／73,224 |
| a-spoke 省略 K=C+a+U ternary／witnesses | 1,440／23,478 |
| b-spoke 省略 L=C+b binary／witnesses | 1,440／10,740 |
| 整份 U 省略刪 b 後 K=C+a ternary／witnesses | 720／8,904 |
| 同圖 complete-relation join 與独立全圖回溯交叉核對 | 5,040 |
| G−au=T_N×R_U 精確乘積 | 720 |
| 原 spokes、ax、au 精確接回 | 4,320 |
| 原附件路徑／封 {3} 的 C 投影等式 | 588／180 |
| 全部原 seven-variant Σ masks | 504 |
| 兩份非空域 singleton guard controls | 225＋225 |
| 原／交換完整圖 pairs | 36 |
| root-swap 字面完整六角色 joint checks | 2,520 |
| root-swap 六／五角色 full coloring checks | 35,241／3,366 |
| 所有序列化 coloring 欄位均已逐份驗證 | 144,830 |

最後一項以遞迴計數所有 `coloring`／`omitted_only_full_coloring` 欄位後，
與實際驗證次数相等，包含 16,654 份接回時被刪 tuple 的 witnesses 及
重複保存的負控制 witnesses。每份完整 colouring 的 boundary、所有原邊、
ports 及共享 x 座標均獨立檢查；空 fibres 也保留完整 16 個字面 root pairs。
原 controls 的完整 Σ 獨立重算為 959 的 4 張、1023 的 68 張，沒有得到
933／941 source realization。

[counterexamples.json](counterexamples.json) 保存三份原圖、指定 row、ports
及全部 stored witness：control 0／row 0 的真 ternary guarded fibre 為空，
marginals 卻給四份假 tuples；control 0／row 6 的 spoke omission 非空但
原 joint 為空；control 42／row 0 的原／ax-omission joints 有 4／6 tuples，
π_(a,b,u) 都是 {(2,3,3)}，六角色 joint 不相等。

原 A checker 在凍結副本 default 與 `PYTHONHASHSEED=17` 實際 exit 0，
耗時 13.311／13.169 秒。原 A artifact SHA-256 前後均為
`c906fa12ada875b624421b8b7402ed4159e8756f78673a974c9056f7fa0a5082`；
獨立 audit 亦確認兩份讀取 source artifacts 的原 bytes 不變。

```bash
python3 audits/2026-10-04-task-d2/a/audit_a.py --repo /tmp/math-task-d2-snapshot
python3 audits/2026-10-04-task-d2/a/audit_a.py --repo /home/ray/developer/ai/math
cd /tmp/math-task-d2-snapshot
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
```

適用界線：短支援、飽和 minimal-core 身份、two-spoke ternary K₅、Gallai
block palettes、連通外部 K₄ 排除及任意大小未用色守恆仍是沿用紙面依賴；
本 audit 沒有重證外部定理、任意大小 disk crosscut 或 Lean topology。
01／23 排除是原報告的條件式紙面成果；有限必要域保留 22／26，未證
mixed12 全型、ε≥3、一般出口、來源實現或 K∞=K≤5。後續 A₂ 的 01／12
新增成果由獨立 successor audit 分開覆蓋，沒有改写本轮历史停止点。
