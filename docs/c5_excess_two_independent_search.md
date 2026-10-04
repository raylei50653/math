# 任務 ER：ε=2 有限搜尋的第二套枚舉器

2026-10-04。基準 `integrate-kprime-e3 @ d00aba4e10ea2d05ab216fedd94f5a166b2777ad`；
分支 `task-er-enumerator`；獨立 worktree `/home/ray/developer/ai/math-task-er-enumerator`。
依任務限制只新增本任務 scripts、artifacts 與本報告；未 commit／push。
研究入口仍是 [HANDOFF](HANDOFF.md) 與 [Kempe 導覽](c5_kempe_guide.md)。

**三型完整完成到 k=9。21 個型／層的 q／crit canonical 集合、有標號計數、Q 形狀分布全部與 ES 一致，合計 179 個 crit orbits；沒有猜想 E 反例。**
這是指定有限域的 Python 對照證据；沒有證明 k≥10 完整性、任意大小猜想 E、一般出口或 `K∞=K≤5`，也沒有新增 Lean 定理。

## 1. 問題、群作用與獨立性界線

問題定義沿用 [ES §1](c5_excess_two_finite_search.md#1-完整前提與計數範圍)：
有限簡單圖 G，具名 induced C₅ 框 B=(0,1,2,3,4)，內點為 5..4+k；disk 等價於
加入連至五個框點的 apex 後平面。有效內點全部完整 degree≥4，degree excess ε=2；
共同 S₄ 色框的十列 Σ、T4 mask=932 全收、Q≠∅、每條非框邊 Σ-critical、
每內點至多三條 spokes、H=G−B 連通。
NA／AD roots 固定 5、6，degree=5，分別不相鄰／相鄰；D6 root=5，degree=6；其餘內點 degree=4。
Singleton 列索引按位置是 (6,4,3,1,0)。Q 為拒絕的 singleton 位置集合；
c(Q) 計 C₅ 上弧段，全圈時 c(Q)=1。
有標號計數固定 surplus roots，不額外乘選 root 的組合數。

NA／AD 的群為 D₅×S₂×S_(k−2)，大小 20(k−2)!；D6 為 D₅×S_(k−1)，大小 10(k−1)!。
搬動整圖的具名框、內點與 actual spokes，再在新的共同色框重算 Σ；沒有分量獨立換色或 marginal 替代。

**閱讀流程有一項明確例外：主 agent 開工時讀 ES 報告的範圍過大，讀到 §2，以及部分 §3／§4.1，超出了指定的 §1。**
因此本輪不宣稱「全員只看 §1」的盲實作。没有任何 agent 讀取、import 或複製
`scripts/c5_excess_two_finite_search*.py`；程式與演算法對照仍是分開實作。
染色、canonical、暴力參考三個子任務使用沒有 ES 演算法歷史的獨立上下文，未讀 ES 實作或演算法段落。
比較器只讀 ES JSON 與 crit orbit artifacts。唯一允許沿用的四色列來源是 `c5_kempe_screen.REPS`。

| 部分 | 本輪實作 | 所依賴來源 |
| --- | --- | --- |
| 生成 | connected plane H 的 rotation system，再於同一 face 接上環序 spokes | plantri 5.8；本輪 corner／環序枚舉 |
| Σ | 固定 numeric order 的 explicit frontier tuple transfer DP | 本輪實作與十列 REPS |
| 搜尋篩選 | 固定 numeric order DFS；q orbit 上另以完整 DP 重算 | 本輪實作 |
| Criticality | 每條非框邊實際刪除，重新算十列 DP Σ 與新列 witnesses | 本輪實作 |
| Canonical | ordered equitable refinement＋individualization，保留具名 frame／root roles | 本輪實作；不使用外部 canonical library |
| k≤5 參考 | 所有 H 邊子集 × 所有 degree-prescribed spoke tuples | 本輪實作；apex planarity 用 networkx 3.5 |
| 第三判定 | 全部 4^k 個內點色 tuple，直接測每條邊 | 本輪 Cartesian product，沒有 FCT oracle |

新檔入口：
[主 checker](../scripts/c5_excess_two_independent_search.py)、
[染色模組](../scripts/c5_excess_two_independent_coloring.py)、
[canonical 模組](../scripts/c5_excess_two_independent_canonical.py)、
[暴力參考](../scripts/c5_excess_two_independent_brute.py)。

## 2. 直接組合嵌入生成與完整覆蓋

### 2.1 外部 plane-map 生成器

使用 [官方 plantri 5.8 manual](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
所定義的 `-p -c1 -m1`：connected simple plane graphs，包含 bridges／cut vertices，
同構按球面嵌入判定。它以平面嵌入的構造與刪邊生成圖；本輪沒有先枚舉 H 邊集再測平面性。
程式從官方 5.8 archive 取得，Apache-2.0 授權與原版 source/manual 一併保存於
[vendor](../artifacts/c5_excess_two_independent_search/vendor/plantri-guide.txt)。
這是外部 generator 的完整性依賴，並非本輪從零重寫 plantri 或 Lean 化其演算法。

- archive SHA256：`e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`。
- `plantri.c` SHA256：`3f70de5a3cacc78b2ed25b6a257588da94a518d8ae1dae74bcd0bf259cea07e8`。
- 每次生成與 replay 都核對 source SHA，並用 `cc -O3` 編譯。
- k 層命令為 `plantri -pc1m1 -e{k}:{2*k-1} -a {k}`；不使用 res/mod 切片。

每份 rotation system 的 oriented darts 全部走訪，得到每個面邊界的完整 walk，
並核對 Euler characteristic=2。面 walk 保留重複 cut vertices 與 bridge 的兩侧，沒有把它們簡化成 simple cycle。
逐一指定每個可能的 degree-5 root pair 或 degree-6 root；由完整 prescribed degree 減 H degree 得到各點 spoke need。

### 2.2 同一 face 的所有非交叉 attachments

固定 H 嵌入與指定外面：把每個頂點所需 spokes 分配到它在面 walk 上的全部 corner occurrences，
逐點列出所有 weak compositions。每個配置產生循環的 spoke-origin sequence。
逐一旋轉這個 sequence，將第一條 spoke 的框端固定為 0，再列出所有 nondecreasing 0..4 的框端列。
同一內點不能重複接同一框點；所得圖是 simple。最後添加原五條 C₅ 框邊，不添加框 chords。

完整性理由：任一合格 disk 圖刪去框與 spokes 後给出 connected H 的一份球面 rotation system，
所有 spokes 都位於包含外框的同一 H face。以 regular neighborhood 厚化 H，其所選面的邊界是單一 Jordan curve；
非交叉 spokes 的兩端循環次序一致。原 spoke 在每個面角的分配是某個 weak composition，
其端點次序是上述循環列的某個 cut；D₅ 的旋轉可把 cut 的第一個框端搬成 0。
所以每份 abstract framed graph 至少一個群代表被生成。重複嵌入、face、corner 分配或 root 選擇
最後都由整圖 canonical code 合併，而不把嵌入數誤當 graph orbit 數。
plantri 把鏡像嵌入視為同構；整體鏡像同時反射框的環序，而本輪群包含 D₅ 反射，故仍保留每個 framed graph orbit。

### 2.3 全部剪枝及依據

只使用下列直接證成的必要條件；不使用猜想 E、不設定 Q 的大小上界，也不排除多個拒絕弧段。

1. **degree／spoke cap／root adjacency／H connected**：都是本輪明列前提；若某點 need>0，該點必在所選外面 walk 上。
2. **k≤e_H**：degree 和為 `2e_H+s=4k+2`。augmented disk 的 Euler 界給 `e_H+s≤3k+2`，相減得 e_H≥k。
3. **s≥4，所以 e_H≤2k−1**：T4 全收而 Q≠∅ 必有至少四個框點碰 spokes。
   獨立證明：若只碰 ≤3 個框點，singleton 三色列在這些點上的 partition 至多留一個 repeated pair。
   若有一對，選重複該對的 T4 列；若全部異色，選一對不完全包含於已碰框點的非相鄰 pair。
   適當共同 S₄ 換色後，該 T4 列在所有實際附件端點上與原 singleton 列相同。
   其內點延拓也延拓原 singleton 列，故五個 singleton 都接受，矛盾。
   因此總 spokes 至少四條；代入 degree 等式得到 e_H≤2k−1。
4. **局部 pinned T4 singleton clash**：任一 H 邊兩端被 actual spokes 強迫同一色，該 T4 列不可能接受。
5. **完整 T4 染色決策與 Q 判定**：固定 numeric DFS 精確求 existence；没有 heuristic 或 FCT oracle。

小 k=1,2 三型都因 root 的完整 degree 減可能的 H degree>3 而不合前提；
正式表涵蓋 k=3..9。NA k=3、D6 k=3 也由同一必要 degree 條件為空。
`generation_stats` 只計嵌入／附件 visit 的診斷數，會含重複；不是有標號 disk 或 t4 counts。
因使用已證無 Q 剪枝，本輪不主張完整計主生成器的 disk／t4 counts。

## 3. Σ、criticality、canonical 與小域控制

Σ transfer 處理內點順序固定為 5..4+k。state 是已處理點中仍與未處理點相鄰者的 literal 色 tuple。
每一步列出新點四個可能色，檢查其 actual spokes 與已處理內鄰，再 forget 沒有未來邊的點。
相同 frontier tuple 合併，只消去已完成變數；因此接受當且僅當存在完整 proper coloring。
十列共用同一 graph、具名框與 literal 色名。DFS 是獨立的固定順序搜尋，用於快速 existence screen 與 witnesses。
每條非框邊都實際刪除，DP 重算全部十列；critical 恰為每次都新增至少一個接受列。
每個 q 圖都保留完整原圖、Σ、所有刪邊 masks、新列 witnesses、接受 witnesses 與 apex rotation certificate。

Canonical 初始 partition 把五個框點與 surplus roots 固定成 anchors，普通內點按完整 anchor incidence 等不變量分 cell；
對所有 D₅ frame orders、兩 root orders 作 ordered equitable refinement，再在未分開的 cell 精確 individualize。
code 是此 equivariant refinement tree 的最小完整 adjacency string；不是 ES 的邊集字典序 minimum。
完整 adjacency code 相同當且僅當在指定群的同一 orbit。最小 leaf 的重數等於 stabilizer；
經核對的 true/false twin cell 用 factorial 計重數，orbit size=群大小/stabilizer。
ES 邊集先完整搬入這個 canonical form；ES Σ 與 Q 也沿其 permutation 搬到相同的具名框後逐 orbit 比對。

[controls.json](../artifacts/c5_excess_two_independent_search/controls.json) 每次 `--check` 重算逐 byte：

- 2,131 個染色控制圖、131 次 edge deletions：DP、固定順序 DFS、全 Cartesian product 一致，witnesses 合法。
- 65 個 canonical 控制圖、1,295 個 group images：k≤5 全群 orbit/stabilizer/invariance 一致。
- 控制檔固定保存本輪四份 source、REPS source、plantri source/manual 的 SHA256；報告的文字 hash 不參與數學重播。

暴力版完整訪問所有 H 邊子集与 prescribed spokes tuples；按 uniform relabellings cache outcome，
但每份 original labelled tuple 都加計一次。k=5 原始 degree candidates：NA=4,253,600，AD=13,625,150，D6=9,731,460。
暴力版逐 tuple 累積 Q shape histogram，另與 canonical orbit weights 恢復的 histogram 比對。
k=3..5 的 q／crit 集合、labelled counts、Q histogram 都與嵌入生成器一致。
這個小域 reference 共用本輪染色與 canonical helpers，因此生成方法獨立；染色／canonical 本身另有上列第三方法／全群控制。

三個失敗路徑負控制另外實際執行：aggregate count 錯、來源圖不合 domain、
暴力版僅 per-orbit Σ payload 錯。主 checker 全部 exit 1、保存 STOP 證據，並由 Cartesian product 判定原图与逐邊刪除；
控制 driver exit 0。这些是注入的負控制，不是正式搜尋不一致；原 ES artifacts 没有改動。

## 4. 各型、各層比對

表中數字順序均為 **ER / ES**。不只比較總 orbit 數：每層先把兩邊的完整圖轉入 ER canonical form，
再比較完整集合及逐 orbit 的 Σ、Q、critical flag、stabilizer、orbit size。

| 型 | k | q orbits | crit orbits | q 有標號數 | crit 有標號數 | 結果 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| NA | 3 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 一致 |
| NA | 4 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 一致 |
| NA | 5 | 2 / 2 | 0 / 0 | 240 / 240 | 0 / 0 | 一致 |
| NA | 6 | 9 / 9 | 3 / 3 | 4,320 / 4,320 | 1,440 / 1,440 | 一致 |
| NA | 7 | 48 / 48 | 2 / 2 | 112,800 / 112,800 | 3,600 / 3,600 | 一致 |
| NA | 8 | 500 / 500 | 22 / 22 | 7,027,200 / 7,027,200 | 316,800 / 316,800 | 一致 |
| NA | 9 | 3147 / 3147 | 27 / 27 | 304,403,400 / 304,403,400 | 2,721,600 / 2,721,600 | 一致 |
| AD | 3 | 1 / 1 | 1 / 1 | 10 / 10 | 10 / 10 | 一致 |
| AD | 4 | 3 / 3 | 0 / 0 | 80 / 80 | 0 / 0 | 一致 |
| AD | 5 | 10 / 10 | 0 / 0 | 1,140 / 1,140 | 0 / 0 | 一致 |
| AD | 6 | 35 / 35 | 2 / 2 | 15,600 / 15,600 | 960 / 960 | 一致 |
| AD | 7 | 146 / 146 | 1 / 1 | 325,200 / 325,200 | 2,400 / 2,400 | 一致 |
| AD | 8 | 622 / 622 | 0 / 0 | 8,040,600 / 8,040,600 | 0 / 0 | 一致 |
| AD | 9 | 2461 / 2461 | 5 / 5 | 224,569,800 / 224,569,800 | 403,200 / 403,200 | 一致 |
| D6 | 3 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 一致 |
| D6 | 4 | 2 / 2 | 2 / 2 | 120 / 120 | 120 / 120 | 一致 |
| D6 | 5 | 14 / 14 | 9 / 9 | 3,120 / 3,120 | 2,040 / 2,040 | 一致 |
| D6 | 6 | 37 / 37 | 4 / 4 | 43,200 / 43,200 | 4,800 / 4,800 | 一致 |
| D6 | 7 | 142 / 142 | 25 / 25 | 986,400 / 986,400 | 176,400 / 176,400 | 一致 |
| D6 | 8 | 539 / 539 | 41 / 41 | 25,426,800 / 25,426,800 | 2,016,000 / 2,016,000 | 一致 |
| D6 | 9 | 1926 / 1926 | 35 / 35 | 732,009,600 / 732,009,600 | 14,112,000 / 14,112,000 | 一致 |

各層的 `comparison` 保存 ES source SHA、兩邊計數、兩邊集合大小與差集。
可由 [NA9](../artifacts/c5_excess_two_independent_search/NA_k9.json)、
[AD9](../artifacts/c5_excess_two_independent_search/AD_k9.json)、
[D6-9](../artifacts/c5_excess_two_independent_search/D6_k9.json) 的 `q_orbit_chunks` 找到所有完整 q 圖及證書；
每個 crit 圖另外按型／層保存於 `crit_orbits/orbit_*.json`。

### 4.1 Q 形狀的有標號分布

形狀 key 是 Q 在 D₅ 作用下的字典序最小位置 tuple，comma-join；
`0,1` 是相鄰 pair，`0,2` 是非相鄰 pair。下列 ER 的數字逐項等於 ES §4.2／`q_shape_labelled`。

| 型 | k | q 類有標號 Q 形狀計數 | 與 ES |
| --- | ---: | --- | --- |
| NA | 3 | 空 | 一致 |
| NA | 4 | 空 | 一致 |
| NA | 5 | `0`: 240 | 一致 |
| NA | 6 | `0`: 3,360；`0,1`: 960 | 一致 |
| NA | 7 | `0`: 112,800 | 一致 |
| NA | 8 | `0`: 6,969,600；`0,1`: 57,600 | 一致 |
| NA | 9 | `0`: 303,597,000；`0,1`: 806,400 | 一致 |
| AD | 3 | `0,1,2`: 10 | 一致 |
| AD | 4 | `0`: 80 | 一致 |
| AD | 5 | `0`: 1,020；`0,1`: 120 | 一致 |
| AD | 6 | `0`: 14,640；`0,2`: 960 | 一致 |
| AD | 7 | `0`: 308,400；`0,1`: 16,800 | 一致 |
| AD | 8 | `0`: 7,659,000；`0,1`: 381,600 | 一致 |
| AD | 9 | `0`: 213,129,000；`0,1`: 11,239,200；`0,2`: 201,600 | 一致 |
| D6 | 3 | 空 | 一致 |
| D6 | 4 | `0`: 120 | 一致 |
| D6 | 5 | `0`: 3,000；`0,2`: 120 | 一致 |
| D6 | 6 | `0`: 43,200 | 一致 |
| D6 | 7 | `0`: 943,200；`0,1`: 43,200 | 一致 |
| D6 | 8 | `0`: 24,116,400；`0,1`: 1,310,400 | 一致 |
| D6 | 9 | `0`: 690,480,000；`0,1`: 41,529,600 | 一致 |

AD9 的非相鄰 pair 包含在正式 q 類中；沒有因猜想剪掉它。Σ-critical 通過與否另按每條原非框邊判定。
所有正式 crit 圖的 `|Q|+c(Q)≤4`；沒有出現猜想 E 的反例，未觸發正式 STOP。

## 5. 時間、產物、重播與檢查

Python 固定 `/home/ray/developer/ai/math/.venv/bin/python`（3.14、networkx 3.5），最多 8 workers。
先實測 k≤8 再估 k9：初輪 k8 三型合計 46.528 秒，30,564 個 plane H maps；
k9 有 563,612 maps，數目倍率約 18.44，當時估 5–15 分鐘。
最後 k9 生成＋三型 DP/deletion/rotation 證書＋比較實測 **169.829 秒**。
第一次整輪 k3..9 的量測如下，含 k≤5 reference；之後只重建有加強驗證 metadata 的小層，
不把初稿 artifacts 覆寫，先保存到 scratch 再用 exclusive-create 新建最終檔。

| k | 三型合計 wall seconds |
| --- | ---: |
| 3 | 0.229 |
| 4 | 0.936 |
| 5 | 48.312 |
| 6 | 1.101 |
| 7 | 4.674 |
| 8 | 22.871 |
| 9 | 169.829 |

時間資料是量測紀錄，另存在 `timing_3_9.json` 與 `timing_3_5.json`，不把 elapsed time 放入數學 certificate bytes。
`--check` 重算 controls、21 份 layer JSON、所有 q chunks、179 份 crit JSON 并逐 byte 比較；
時間量測 JSON 与執行 logs 不宣稱可重新產生相同 elapsed time。
合計 9,644 個 q orbits 保存於 54 個 chunks；數學逐 byte 範圍是 255 份 JSON。
實際 exit codes 與完整重播 logs 封存於
[execution_results.json](../artifacts/c5_excess_two_independent_search/verification/execution_results.json)。
初稿與負控制 scratch 已保留至 `/tmp/math-task-er-enumerator-scratch-d00aba4`，不混入交付的正式集合。
chunk 預算 750,000 bytes；目前最大新產物小於 1 MB，故無需執行 `tools/artifacts.py record`，既有 MANIFEST／gitignore 保持原樣。
新 worktree 缺少的既有 NA9 ES validation JSON 已由主 checkout exclusive-copy，
核對 unchanged MANIFEST 的 SHA256=`0b08675df72ecd21415d8fb54df567fc2daa7b802df9bc22c97f4cd6f89dc9bb`，大小 1,152,495 bytes；
該檔是既有 ES 依賴，沒有重新登錄。

三個輔助模組也有獨立命令列驗證：染色／canonical 的 `--check` 委派到 controls 的逐 byte 重播；
暴力版 `--check --output <path>` 重算其指定型／層並比較 bytes，生成使用 `xb`，已有檔案時拒絕覆寫。
AD3 單獨生成、普通／hash-seed check 均 exit 0；重複生成、注入 byte mismatch 均 exit 1；
缺少 `--output` 的 check exit 2。最後只補強這些 CLI，數學函式不變；刷新 source hashes 後再重播全域。

從沒有本輪輸出檔的 checkout 生成；對現有結果重播：

```bash
/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_independent_search.py --jobs 8
/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_independent_search.py --check --jobs 8
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_independent_search.py --check --jobs 8
/home/ray/developer/ai/math/.venv/bin/python scripts/check_docs.py
/home/ray/developer/ai/math/.venv/bin/python tools/docgraph check
git diff --check
```

| 實際執行 | exit code | 說明 |
| --- | ---: | --- |
| 完整生成 k3..9 | 0 | 三型全部一致 |
| 最終小層／controls 生成 | 0 | 只增加失敗路徑与 brute 逐 tuple Q histogram 驗證 |
| 普通 `--check` | 0 | 最終 source 全域逐 byte，257.765 秒 |
| `PYTHONHASHSEED=17 --check` | 0 | 最終 source 全域逐 byte，257.991 秒 |
| `check_docs.py` | 1 | 3 errors：兩個已知 missing-path，加上本新報告未索引 |
| `tools/docgraph check` | 0 | 62 documents、213 relations、5 families；0 errors／notes |
| `git diff --check` | 0 | 不改既有 tracked files；新 Python／報告另做 no-index whitespace 檢查 |

因明確要求只新增檔案，本報告沒有追加到既有 STATUS；check_docs 的新增 unindexed-report 項会如實保留，不修改既有 checker。
`lake build` 未執行：本任務沒有 Lean 變更，也沒有宣稱任何 Lean／拓撲形式化。

**停止點：三型 k=9，全部一致。k≥10 未搜尋。下一入口是本報告與主 checker；原 ES checker／報告未更動。**
