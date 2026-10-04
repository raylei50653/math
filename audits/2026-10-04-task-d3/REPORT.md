# D₃：C／C₂ 的獨立稽核

2026-10-04。基準為 [D₂ 整合快照](../2026-10-04-task-d2/REPORT.md)，
HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`。
**C／C₂ 保存的完整 triples、側接合身份、actual attachments、空 fibres、
刪邊 witnesses 及原邊 K₅ subdivision 全部通過獨立稽核；C₂ 只關閉
`CPP-134-1／geometry 30／side_join_id 20`，沒有誤刪整份 case。**

本輪只新增本 audit 包。使用者確認 A₃／B₃／C₃ 尚未交付並指示
「先不處理」，故不回收其草稿、不更新共用文件及最新停止點；
後續同步條件見 [INTEGRATION_PENDING.md](INTEGRATION_PENDING.md)。
歷史 artifacts、成功／失敗紀錄及原 checker bytes 均保留，未 commit／push。

## 1. 基準、方法與證據層

[baseline.json](baseline.json)保存 D₃ 開始時 1,456 份既有檔案的 SHA256，
捕捉時間為 2026-10-04 01:59:57 UTC。獨立核對 D₂ 最終 1,353 份
文件及 D₂ 交付表的 97 份檔案，全部吻合；20 份 C／C₂ 原輸入另外
凍結於 [snapshot](snapshot/)。原 manifest／ignore 的補充副本保存在
`baseline_control_files/`，其 bytes 與開始基準一致。

[C relations 稽核](relations/notes.md)與 [C₂ graph 稽核](graph/REPORT.md)
只用標準函式庫，未匯入 production enumerator、join helper 或 witness
validator。先從具名原邊與同一 q=01012 重建完整染色，再比全部 tuple
集合；保存的 masks、counts、retained／排除 flags 不作判定 oracle。
側角色是原 unary 身份與禁色條件的必要語義資料，沒有假造它們的完整
實現圖。紙面論證另見 [paper/notes.md](paper/notes.md)。

固定 Python 核對與任意大小紙面證明分開：原 Gallai、bridge／leaf 計數
及 disk／Jordan 論證仍屬原報告及外部定理，不由固定控制的數量推得。
本輪沒有新增 Lean theorem、target 查詢、完整 Σ 結論或一般出口證明。

## 2. C：完整 triples、具名側身份及字面 fibres

[最終 results](relations/final/results.json)通過。獨立 MRV 從 500 份原
`(S₀,S₁,S₂)` 的 (3,2,1) actual 附件，重建全部 2,472 份三座標 tuples；
每份 relation 先查重複再比整個集合。101 份側角色、每個 a 的 125 個
有序 joins、560 份 cases 與每份 25 個 side_join IDs 均自行推導後深比較。
具名 contacts、各 unary 接點分拆／禁色、spoke colors、兩 root、原 P₃
及共同色框保持，不把不同 unary 合成一份匿名 union。

| 獨立核對域 | 字面 fibres | 空 fibres |
| --- | ---: | ---: |
| 500 原 P₃，zx₂／wx₂ 保留，未加 zw | 8,000 | 224 |
| 同一 500 原圖加回 zw | 8,000 | 2,224 |
| 336 原 root 交換／路徑反向控制 | 5,376 | 672 |
| 14,000 完整側角色語義 joins，未加 zw | 224,000 | 207,200 |
| 同一 14,000 joins 加回 zw | 224,000 | 224,000 |
| 其中 retained 36 cases／900 joins，未加 zw | 14,400 | 13,300 |

各域重疊，不相加當作來源圖數。每份字面 fibre 都保存具名 `(z,w)`
及完整 `(x₀,x₁,x₂)` 陣列，空 fibre 明寫 `[]`；原 P₃ 未加 zw 的
完整 root–P₃ relation 共 22,248 rows。這些 rows 只給相應原 P₃
控制染色，側角色語義 joins 不稱為未知 unary 的完整 source 染色。
另外保存 112 份整體框反射與共同色置換後的完整 relations。

114,048 份 actual-side-support 候選依原條件重新導出，完整 geometry
JSON 與原資料相等：524 無必要幾何案例、36 retained cases、18 份 local
attachments、140 geometries、900 case-side joins，全部原列保持。
完整 ledgers 見 [local relations](relations/final/local_relations.json)、
[role joints](relations/final/role_joints.json)、
[derived geometries](relations/final/derived_geometries.json)及
[symmetries](relations/final/symmetry_relations.json)。

三份 [負控制](relations/final/negative_controls.json)保留具名假 witness：
local 134 的根對 (1,3) 在同一原 x₂ 上 fibre 空，但兩 root 各自的
fibre 非空；假複製 x₂ 會錯誤接合。只對 C 換色 0／1 而不搬運原 q，
會假接受 (3,1,0)，並違反原 x₁–b₁ 邊。把 C₂ 六份 unary triples
改成座標 marginals 的 Cartesian product，會新增 (0,0,0) 等 21 個
假 rows，並丟失原禁色。三種錯誤都被完整關係核對抓出。

## 3. C₂：同一原身份、完整 unary 及刪邊染色

[graph/results.json](graph/results.json)含 2,513 項檢查，零失敗。
獨立核對 C₂ 對 C 的完整 local／case／geometry／parent_entry JSON，
固定 local 134、case 86／CPP-134-1、geometry 30、join 20、side IDs (8,1)。

原 P₃ 附件為 S₀=014、S₁=14、S₂=4，完整 triples 恰
`{(3,0,1),(3,0,3)}`。兩原 root 均無 spoke，各有一份三接點 unary；
Az={b₁}、Aw={b₂,b₄}，原禁色分別 {0,2,3}／{0,2}。
原 zx₂、wx₂、zw、P₃ 兩內邊及六條 actual 框附件逐條保留。
z 側原 D 被紙面論證迫成 triangle 後，其完整有序 triples 恰為
`(0,2,3)` 的六個 permutations，禁色恰 {0,2,3}。

| C₂ 固定核對 | 結果 |
| --- | --- |
| 四種原點身份／pinned lists | 16 項全部相等 |
| 原 P₃ 字面 root-pair fibres | 16 組，其中 (1,3)、(3,1) 兩組空 |
| 完整原 unary 字面 root-pair fibres | 16 組，z=0／2／3 的 12 組空；w 在此局部域未受原 D_w 約束 |
| 原九條 unary 相關邊逐條刪除 | 全九條，各四個 z 色均可局部染色 |
| 保存的局部染色 witnesses | 36 份逐點／逐原邊核對 |
| 原拒絕三色的刪邊兩端同色 | 27 份全部成立 |
| 原 context partial witnesses | 9 份，z=0、w=1、P₃ tuple=(3,0,3) |

獨立列出每条刪邊後的全部局部染色：刪 attachment 邊時四個 z 色的
數量為 (2,6,2,2)，刪 triangle 內邊時為 (2,12,2,2)；每條刪邊的
原 13 點投影在 z=0、w=1 下恰有兩份染色，保存的 witness 在其中。
局部 36 份不含原 zw constraint，故 z=w=1 的九份不能升為原 source
染色；九份 partial witnesses 則核對全部保留的 context 原邊。

原 D_w 的完整 relation 仍未知。禁色 {0,2} 若來自該原 relation，
就保證 w=1 的完整避色 fibre 非空；本輪沒有填造 D_w tuples 或枚舉
內點，故九份 partial witnesses 不稱為全 source colorings 或全圖
逐邊最小性證書。原 projection 的 w-degree=2，另三條 incidence
屬未枚舉的原 D_w；不把此投影誤報為原 (5,5) 完整來源。

## 4. K₅ subdivision 的原邊及路徑互斥性

固定 branch vertices 為 b₁,z,u₀,u₁,u₂。九條直接路徑由原 triangle
三內邊、三條 zuᵢ 及三條 b₁uᵢ 給出。第十對 z–b₁ 的兩份保存路徑為

- 長路 `z–x₂–b₄–b₃–b₂–b₁`：14 條原邊、9 點的 subdivision。
- 短路 `z–x₂–b₄–b₀–b₁`：13 條原邊、8 點的 subdivision。

兩份分別逐條核對十個不同 branch pairs、endpoints、simple paths、
每條邊的原 provenance、內點不含 branch vertices、內點兩兩互斥、
路徑 edge-disjoint，以及兩路只能共享其共同 endpoints。
共 20 條 paths、90 組路徑對；branch degree 四、內點 degree 二及
完整 subdivision edge union 亦吻合。兩份原 minor 的 disjoint connected
bags 與十對 actual interbag edges 共 20 份 witnesses 全部通過。

32 份 K₄ tether 固定控制另外核對原 context、tether 路徑、connected
hub、袋互斥與 320 份 actual 邊鄰接。這些只是路徑控制，不自稱任意
unary 的來源實現。四份 corruption 負控制（重複路徑點、把 branch
點放進內部、重複 branch pair、加入非原邊）均被獨立 validator 抓出。
完整原邊分類、paths、bags、負控制與 witness 染色都在 graph results。

## 5. geometry 30 排除的精確粒度

[scope results](scope/attempt1/results.json)及
[完整 scope ledger](scope/attempt1/scope_ledger.json)從原 C 的具名資料
建立 140 geometries×25 case-side roles 的 3,500 個必要索引 keys；
這是身份索引，沒有新增來源圖枚舉、target 或排除結論。
唯一標為 C₂ 已關閉的 key 是 **(CPP-134-1,30,20)**。

CPP-134-1 原 geometries `[30,31,32,33,34,35]` 與全部 25 個
side_join IDs 均完整。geometry 30 另 24 個 joins 未被 C₂ 關閉；
該 case 的 150 個 geometry×side keys 中，另 149 個沒有本輪新判定。
geometry 34／join 20 及其 Az={b₁,b₂}、Aw={b₂,b₄} 也保留。
沒有從紙面引理的可能其他適用範圍新增 geometry 31–33 的交付判定。
原 36／140／900 歷史陣列不改成 35／139／899。

三份過寬刪除 predicate 負控制均被拒絕：刪整份 case 會多刪 149 keys；
刪整份 geometry 30 會多刪 24；把 join 20 跨六份 geometry 一起刪，
會多刪五個。原 C₂ summary 的 `predecessor_deletions=0` 亦獨立吻合。

## 6. 紙面前提、保存及歷史失敗

[紙面核對](paper/notes.md)在原明列前提下 PASS：有限簡單 disk 原圖、
原連通 D、完整 degree 四、三個互異原接點及外部只有 z／b₁。
原禁色 0 與 q(b₁)=1 不同，故原不可染 lists 大小恰等於 d_D；
[Dvořák Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的前提符合，未採用一般 critical graph corollary。原 z–x₂–b₄ 與 B
給 connected exterior，bridge slack／S₄ 支援迫 K₄ 四份 actual tethers，
排除大 clique 後兩個 leaf odd cycles 需四個原接點，遂迫原 D=triangle。
原外路再給 §4 的 subdivision。這項任意大小證明不以有限控制替代。
C 的雙扇區／tether 及唯一框色分支亦作獨立紙面核對。

[protected 保存結果](preservation_results.json)逐份記錄起始原 bytes、
凍結輸入、11 份直接 input hashes、Git refs 及工作期間的外部新增。
原 scripts／tools／artifacts（manifest 另核對原 entries）／既有 history／
舊 audit 包與凍結輸入全部保持；HEAD 及本地 origin/main ref 未變。
D／D₂ 的原 40 PASS／
4 文件 hash FAIL、兩份完整 payload 相同但 strict bytes 不同、環境與
中途打包失敗都保留原路徑；本輪未重跑那些歷史 checkers 或 refresh 原
hash maps。四份原文件 hash 漂移仍存在，沒有改寫成 PASS。

**全工作樹 bytes 不變的 strict 檢查沒有通過。**
[strict integrity_results](integrity_results.json)保留 13 份現行文件／控制檔
的前後 hash：並行工作更新 README、STATUS、兩份 guides、專題後續
前綴、研究 synthesis、manifest 與 .gitignore；本 D₃ 沒有執行這些寫入，
也沒有回退、整合或採用尚未交付的結論。凍結輸入、原數學 artifacts／
checker bytes 及 manifest 的原 entries 仍不變。不能把 protected PASS
改寫成整個 live workspace 無漂移。

本輪稽核產生的紀錄也保留：relations 首次成功版本在 attempt1，最終
加入三份負控制的 frozen 版本在 final；graph 的初次 JavaScript
parse failure（未寫檔）在 [attempts.json](graph/attempts.json)；paper
首次兩個 subscript anchor 失敗及修復在
[source_metadata.json](paper/source_metadata.json)。它們與數學／原 artifact
失敗分開記錄，沒有清掉失敗來換最終通過。
Root 初次直接比較 graph 整份輸出的 AssertionError 亦保存於
[replay_comparison.json](checks/replay_comparison.json)：差異是 run timestamp、
relative／absolute root 路徑及 live C₂ 文件 hash 漂移。排除這三個明列
metadata 欄後，全部 graph 核對結果與凍結 audited hashes 相同；relations
整份 JSON 完全相等。此比較沒有刪掉數學 payload 或原輸入 hashes。
首次 package link 檢查因結果檔尚未生成而失敗，完整結果另存
[package-attempt1.json](checks/package-attempt1.json)；修正 validator 對本次
必定生成結果檔的自引用處理後再檢查，原失敗不覆寫。

## 7. 實跑驗證、重播與停止點

[四次原 byte-check](checks/original-attempt1/results.json)在凍結輸入上
執行 C、C₂ 的 default／seed17，全部 PASS。獨立 relations 與 graph
各自實跑通過，root 再以凍結輸入重播通過，結果保存在
[relations root replay](checks/relations-root-replay/results.json)與
[graph root replay](checks/graph-root-replay.json)。

[起始整合驗證](checks/navigation-attempt1/results.json)亦實跑通過：
`lake build` 8,831 jobs（僅既有 lint warnings）、文件 checker 523 Markdown／
5,414 local links、DocGraph 62 documents／213 relations、artifact status
`ok=141`、tracked `git diff --check`。這些是新外部草稿陸續落盤前的
驗證截點；依使用者「先不處理」指示，本輪不以 A₃／B₃／C₃ 草稿重跑
全倉索引檢查。D₃ 自身本地 links／新增檔案 whitespace 另由
[package validation](package_validation.json)核對。

```bash
python3 audits/2026-10-04-task-d3/relations/audit_relations.py \
  --repo audits/2026-10-04-task-d3/snapshot --output /tmp/task-d3-relations
python3 audits/2026-10-04-task-d3/graph/audit_c2_graph.py \
  --source-root audits/2026-10-04-task-d3/snapshot --output /tmp/task-d3-graph.json
python3 audits/2026-10-04-task-d3/audit_scope.py \
  --repo audits/2026-10-04-task-d3/snapshot --output /tmp/task-d3-scope
python3 audits/2026-10-04-task-d3/run_validation.py \
  --repo . --scope original --output /tmp/task-d3-original-replay
python3 audits/2026-10-04-task-d3/audit_bundle.py verify \
  --repo . --scope protected --result /tmp/task-d3-preservation.json
python3 audits/2026-10-04-task-d3/validate_package.py \
  --repo . --output /tmp/task-d3-package.json
```

重播用新的 output 路徑，保留先前 runs；`audit_bundle.py capture` 不可
覆寫本輪 baseline。交付 hash 表在 [DELIVERY_SHA256.json](DELIVERY_SHA256.json)，
表不列自身 hash；最後工作狀態見 [FINAL_STATE.json](FINAL_STATE.json)。

**D₃ 停止於 C／C₂ 獨立稽核交付。** 本 D₃ 未同步共用文件，依據的
停止點仍為凍結 D₂；live 文件有上述外部漂移，不作本輪最新停止點交付。
尚未接收 A₃／B₃／C₃。保留未知 D_w 全關係、其他側接合、來源實現、
指定 target、完整 Σ、一般／共同出口及 `K∞=K≤5`；未自行 commit／push。
