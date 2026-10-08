# 任務 D₈：E3 與 K′ 紙面論證的獨立稽核

2026-10-04；基準 `integrate-kprime-e3 @ 2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac`。
獨立 worktree `/home/ray/developer/ai/math-task-d8`，分支 `task-d8-audit`。
只新增本稽核目錄的交付；三份缺少的 gitignored runtime artifact 依任務授權
重建並核對原 MANIFEST。沒有修改任何既有 tracked 文件／報告／checker，
沒有 commit／push。

**總 verdict：有缺口但可補。** E3 §2 的約化與 triple-critical、§4.1 單橋
carrier、§6 共用 contact、§5 兩個非相鄰新限制，以及 K′ 引理 1–6 成立。
唯一新增缺口 **DG6-1**：E3 degree6 checker 的兩個 `t=1` 分拆固定 spoke=b₀，
卻同時固定拒絕列位置 `{0,1,3}`；缺少其他相對 spoke 位置的涵蓋。
原 26 格中 24 格成立，`(4,1)`／`(3,2)` 兩格有缺口但可補。
稽核附件已在同一固定三列下補跑全部五個原 spoke 位置，每個分拆的50份
具名幾何均為0存活；這補足該有限必要末端，但沒有代改原 producer／報告。
所以原版無限定「(i) 完成」須引用本補表，或待整合者修補後再維持。
未發現 carrier 反例，也未發現偷偷使用 q₂/q₄ 接受或舊省略必Ω篩選。

## 1. 總表與交付

本文原行號全部指基準固定 bytes；參見
[E3 REPORT](../../artifacts/c5_excess_two_e3/REPORT.md) 與
[K′ 文件](../../docs/c5_kempe_diagonal_transport.md)。

| 範圍 | verdict | 具體結果、原引用與影響 |
| --- | --- | --- |
| 1(a) E3 §2：32 子集，包括 Q=B | 成立 | E3:67–74；獨立重算全部32子集，11份bad，五份941三點的完整D₅ orbit；Q=B 的c=1。詳見共同稽核§1。 |
| 1(b) E3 §2.1：triple-critical | 成立 | E3:94–108；M自己Σ-critical，不由G遺傳；自身T4／disk／degree≥4／H連通均已驗；ε=2保留surplus roots並沿原H傳播；真子圖ε≤1符合E2全部前提。詳見共同稽核§2逐步表。 |
| 2：E3 §4 共26分拆 | 有缺口但可補 | E3:184–195；24格成立，t=1的(4,1)/(3,2)缺相對spoke涵蓋。只用三列及T4，未用q₂/q₄接受或省略Ω。DG6-1補表全部50+50幾何為0，詳見degree6稽核。 |
| 2：E3 §4.1 單橋 carrier | 成立 | E3:212–238；K自己q₁-core、實際分類原xy為bridge、兩份root=1的原Gallai assignment、off-path D-membership逐根歸納、exact parent query，最後D∈F_l(q₀)矛盾。6,948固定附件形式交叉核對未推翻；不以有限圖搜尋證無界分類。 |
| 3：E3 §6 共用 contact | 成立 | adjacent_notes:63–89；K₄四tethers到連通X、至少一terminal block沒有private x、原五袋連通及十鄰接都有效。935 singleton拒絕pin仍容許。 |
| 4：(4,4) 一mixed限制 | 成立 | E3:257–264；同一全degree4 q-core兩不同retained mixed給內部互斥z–w原路，長度各≥2，合成≥4 simple cycle，違反實際分類。不是原G只能一mixed。 |
| 4：N-empty | 成立 | nonadjacent_notes:95–115；同一原外z–w路，同色一hub／異色按原邊切兩hub，hub常色只要求N(P)交集；tightness及degree4保持。不把此路借給sole separating mixed。 |
| 5：K′ 引理1–6 | 成立 | K′:63–129；Jordan無界側包含B\J，rotation困w於有界側；完整同ψ抽π及ownership，noncrossing可由互斥連通子圖crosscut證明。必要方向不等於K′來源排除。 |
| 6：普通／seed17重播與正控制 | 成立 | 五個原checker各兩次，共10/10 exit0，逐對stdout相同；951、935、1012全部保留。詳見validation。 |

| 新交付 | 用途 |
| --- | --- |
| [audit_common.md](audit_common.md) | 項1、3、4全部逐格／逐步理由，完整前提與原文行號。 |
| [audit_degree6.md](audit_degree6.md) | 26分拆逐格、carrier逐步、DG6-1最小重現與影響。 |
| [audit_kprime.md](audit_kprime.md) | 引理1–6逐格、Jordan七步、π抽取五步及checker邊界。 |
| [degree6_t1_spoke_coverage.py](degree6_t1_spoke_coverage.py)、[結果](degree6_t1_spoke_coverage.json) | 補齊兩個t=1分拆的五個原spoke位置，固定Q與完整原geometry／ownership；重用原有限solve helper，非独立来源oracle。 |
| [degree6_fixed_shapes.py](degree6_fixed_shapes.py)、[結果](degree6_fixed_shapes.json) | 不import repo checker，兩種實際cyclic分類形狀的全部6,948附件交叉核對。 |
| [independent_foundation.py](independent_foundation.py)、[結果](independent_foundation.json) | 不import repo checker，32子集／D₅ orbit與80個原路hub分袋。 |
| [run_validation.py](run_validation.py)、[validation.json](validation.json) | 原checker重播、缺runtime重建、文件檢查、全部tracked SHA前後及命令exit／完整stdout／stderr。 |
| [baseline_sha256.json](baseline_sha256.json) | 起始所有tracked普通文件SHA。 |
| [degree6_validation.json](degree6_validation.json) | degree6兩個稽核附件生成／check／seed17實際結果。 |

## 2. DG6-1 最小重現與補證方向

原位置：`scripts/c5_excess_two_e3_degree6.py:34–39,322–335`。
`REJECT={1,4,6}`固定named Q={0,1,3}；`one_spoke`的slit從0開始，兩個
`t1`groups都只呼叫`solve((0,),...)`。原`degree6.json`中這兩groups各10筆
的`original_spokes`全部只有[0]（degree6_notes:29–30只報這10筆）。

Q={0,1,3}的D₅ stabilizer只有identity及反射i↦1−i；原spoke的orbits為
`{0,1}`、`{2,4}`、`{3}`。因此不能將spoke2或3旋轉成0後仍固定三個拒絕
位置。整圖D₅搬運若旋轉spoke，也須搬全部三列、contacts、attachments、
ownership與色框；這不是額外接受q₂/q₄問題，而是來源必要域漏了相對位置。

最小重播：

```bash
/home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py --check
```

| t=1分拆 | spoke0/1/2/3/4具名幾何數 | 對應search nodes | 全部存活數 |
| --- | --- | --- | ---: |
| (4,1) | 各10 | 32、31、30、34、30 | 0 |
| (3,2) | 各10 | 18、19、18、19、18 | 0 |

補法：producer在fixed canonical三列下，保留全五個spoke及其同步旋轉的
原slit幾何，或先證stabilizer orbit完備再取代表；保存相對列位置，重生成
證書並修正原10筆數字／涵蓋聲明。本次已在稽核目錄補算，但不修改原檔。

**影響範圍：** E3 REPORT:8、167、240及degree6_notes:5、90的「(i)完成」
在原證据束中缺這兩格的全來源末端。以本補表加原局部必要域推導可補合成；
原checker十條重播通過本身不能消除覆蓋缺口。沒有影響triple-critical、carrier、
非相鄰N1–N3的既有前提、K′引理1–6，亦沒有構造數學反例。

## 3. 正控制與原checker重播

| 原checker | 普通 --check | seed17 --check | 控制／邊界 |
| --- | ---: | ---: | --- |
| E3 foundation | 0 | 0 | 精確E1 951／935：原edges、完整Σ、criticality、rotation、full joins保留。 |
| E3 degree6 | 0 | 0 | 951兩binary省略mask仍959／1015；不存在通用省略必Ω前提。必要表0不自證來源涵蓋。 |
| E3 nonadjacent | 0 | 0 | 951／935補充cells代表同圖literal tuples／fibres保留；其非相鄰前提未出现是N/A，非實現性控制。 |
| E3 adjacent | 0 | 0 | B₂/B₃ joint signatures、完整D₅ rows與spoke表確定。 |
| K′ | 0 | 0 | KD1012-0001、KD935-0003、KD935-0008都L1/L2=true，各四次實際完整交換可延拓。 |

K′ 933的192份、941的384份L2仍存活（1012／935各192），沒有從
八頂點500wirings找不到目标推出一般排除；K′仍未決。
951／935不是指定三列前提的反例，generic引理只在各控制自己的適用前提驗。
本次沒有找到非相鄰雙degree5的控制；這件事屬E4控制工作，不能拿951／935
替代該特定前提。重播記錄只聲稱原指定三張控制存活。

## 4. 驗證、檔案不變性與停止點

全部命令、exit code及完整輸出在validation。普通／seed17對應stdout相同。
缺的degree6.json用相關producer exclusive-create；K′相關producer先在本稽核
目錄全新output重建，逐byte比對所有已tracked輸出相同，再僅將兩份缺少的
ignored runtime輸出還原，SHA／大小吻合MANIFEST。沒有覆寫被稽核artifacts。
兩個封存路徑沒有還原，依使用者允許保留已知文件錯誤。

| 檢查 | 實際exit | 結果 |
| --- | ---: | --- |
| scripts/check_docs.py | 1 | 只有D₅ c4/scope_ledger.json與D₂ integration_doc_changes.diff兩個known missing-path。 |
| 本audit四份Markdown的local links | 0 | 26個本地連結／anchors全部存在；全域check_docs不掃audits，另行讀取。 |
| tools/docgraph check | 0 | 62 documents、213 relations、5 families，0 errors／notes。 |
| git diff --check | 0 | 無whitespace診斷。新交付逐檔no-index均exit1且無診斷（新內容差異）；未誤記成exit0。 |
| tracked基準SHA／HEAD | 通過 | 全部baseline tracked普通文件零漂移，HEAD仍2ac279b；工作樹僅新增本audit目錄，忽略的runtime復原另明列。 |

本次停止於全部指定項目都有verdict、DG6-1最小重現及補表。沒有重證所有
歷史分類、擴大E3範圍、改原報告或commit／push。紙面／外部Gallai與Jordan、
固定Python、來源disk可實現性、Lean與一般出口分開；未新增Lean theorem，
沒有執行lake build，也沒有主張完整ε=2層或K∞=K≤5成立。
