# 任務 ES：ε=2 特化有限搜尋與三種 root 型

2026-10-04；基準 `integrate-kprime-e3 @ c9ce4c5`；分支 `task-es-search`，
獨立 worktree `/home/ray/developer/ai/math-task-es`。
依任務約定只新增 scripts、artifacts 與本報告；未 commit／push。
研究入口是 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)，
本輪將其中「下一任務 ES」轉為可重播的有限搜尋。

**五項驗收全部通過；三型正式完整搜尋已完成到 k=9，未出現猜想 E 的反例。**
NA k=6 恢復三個 crit orbit，各 480 張；所有計數與控制證書見下表及 validation.json。
本文所有計數是指定有限 k 的 Python 證據，不是猜想 E 的任意大小證明。

## 1. 完整前提與計數範圍

G 為有限簡單圖，指定框 B=(0,1,2,3,4) 是 induced C₅，框上恰五條邊；
內點私有。disk 的本輪判定依任務定義：新增 apex，連到全部五個框點後
是平面圖。有效內點排除孤立點；本輪全部內點完整 degree≥4，
ε=Σ(deg_G(v)−4)=2。Σ 是十個合法有序框列在共同 S₄ 換色下的接受集合；
框位置不被個別換色或獨立分量正規化。T4 索引為 {2,5,7,8,9}，mask 932。
singleton 位置 0..4 的三色列索引依序是 [6,4,3,1,0]；Q 是其中拒絕的位置。
每條非框邊 e 都須滿足 Σ(G−e)⊋Σ(G)，並要求 Q≠∅。
c(Q) 計 C₅ 上連續弧段；Q=B 的整圈特別記 c(Q)=1，
而非把只適用 1≤|Q|≤4 的 `|Q|−e(Q)` 式套到整圈。

三型使用固定 root 標號：NA／AD 的 roots 為 5、6，完整 degree 為 5，
分別不相鄰／相鄰；D6 的唯一 root 為 5，完整 degree 為 6。
其餘內點完整 degree 為 4。H 是所有內點的 induced graph。
沿用 [E3 §1–2](../artifacts/c5_excess_two_e3/REPORT.md#1-完整前提與證據層)
與 [E1 §3](c5_excess_rejection_law.md#3-搜尋規模與完整覆蓋) 的已證必要條件：
H 連通；每內點至多三條 spokes。

`edgesets` 計 **H 的有標號邊集**，不是包含 spokes 的完整圖數。
`disk` 計補齊完整 prescribed degree 的所有 disk 接法；`t4` 再要求 T4 全收；
`q` 再要求 Q≠∅；`crit` 再要求全部非框邊 Σ-critical。
有標號數固定 surplus root labels，仍區分全部框 labels 及 degree-4 labels；
不將選擇哪些內點充當 root 的額外組合數乘入。orbit 按下一節的完整群合併。

## 2. 演算法與正確性

### 2.0 原型先保存、後逐行審查

第一步已把來源 scratch 的四份 scripts、暴力 k=6 log／JSON、k=4..6
交叉參考與 k=6..8 原型輸出複製至本 worktree `scratch/task-es-prototype/`，
未將 scratch 入庫。全部來源 SHA 與逐行審查記錄保存於
[prototype_provenance.json](../artifacts/c5_excess_two_finite_search/prototype_provenance.json)。
逐行讀取 `nonadj_fast.py`（1–764）、
`nonadj_search.py`（1–74）、`brute_ref.py`（1–115）、
`nonadj_crosscheck.py`（1–155），初步 counts 只作時間估計，沒有直接採信。

審查發現並在正式版處理：原型的主 workspace 絕對 import path、pool 完成次序的
不確定輸出、結果內含耗時而不能 byte replay、overwrite 寫入、crosscheck 印出
mismatch 卻仍 exit 0，以及 embedding／deletion 證書未與 canonical 代表綁在同一
具名色框。正式版改用本 worktree imports、排序聚合、耗時另記、exclusive-create、
失敗 exit 非零，並在 canonical 原圖重算所有 masks／witnesses／rotations。
原型的群作用整軌道 materialization 也改為支援相同 cell 的精確 canonical 枚舉，
再與獨立全群版驗收。

保存的核心原型 SHA-256 為：

- `nonadj_fast.py`：`068c1867a956630f9e5d1b883f4465c75dc7e33a7292dad4880228e7e645592f`。
- `nonadj_search.py`：`e2c9c67ea5c69decda1ac11dda276654a79b314aa8928029bec87b56a1f10dea`。

### 2.1 內部邊集及附件的完整覆蓋

若 e_H 是 H 邊數、s 是全部 spokes 數，完整 prescribed degrees 給
`2e_H+s=4k+2`，所以非框邊數為 `e_H+s=4k+2−e_H`。
augmented disk 有 k+6 點、框及 apex 邊共十條；Euler 界給非框邊≤3k+2，
因此每份 disk 必 e_H≥k。此界是平面必要條件，不是猜想剪枝。

特化版列出全部允許的 H degree 序列：root 的 H degree 至少為完整 degree 減 3，
degree-4 頂點的 H degree 至少 1、至多 4，並受 k−1 上界；序列總和為偶數，
e_H≥k。root degree 同型排序，degree-4 H degrees 排序，逐點枚舉全部剩餘內部
鄰點組合；只保留 connected H 及 prescribed root adjacency。
任何來源圖都可先在相同完整 degree 類中重標號而落入這些序列，故沒有遺失來源。
H 同構代表另用 root class／H degree 的穩定色細化及剩餘類內置換求 canonical code。
其 private automorphism 數恢復每個 H 的有標號權重。

每個內點 v 的 spoke 數確定為 prescribed degree−deg_H(v)，
在全部五個框點中列出所有該大小的子集。首個附件按 D₅ 分軌道且乘回軌道大小，
其餘附件逐一列出。任一部分 augmented 圖已不可平面時，其超圖亦不可平面，
故可停止該支；此剪枝是 graph planarity 的單調性。完整圖沒有重複計平面嵌入數。

### 2.2 T4 單調剪枝、bitmask 與平行化

對每個 H，枚舉其全部 proper 4-colourings；用 Python 整數 bitset 表示共同內點
賦色集合。每一實際框附件只把該集合與避開框鄰色的 bitset 交集。
十列都在同一 literal 色框中計算；分量 relations 沒有拆成 marginals。
加邊只會使延拓集合縮小。若部分附件已使任一 T4 列為空，所有完成接法亦拒絕
該列，故 fast 可直接剪掉整支。validate 保留這些 branches 到完整 disk 葉，
以取得全部 disk 計數。fast 還使用 §2.5 的安全無 q 支援剪枝，
因此不完整計 disk／t4，兩欄明記 `null`；q／crit 及 q 邊型統計仍是完整數。

H degree 序列及 H 代表分配給 `multiprocessing.Pool --jobs`，各 worker 返回整數
計數及完整 canonical 邊集；主程序按排序集合與整數加總合併。
JSON 不含耗時或完成先後順序，因此排程、jobs 與 hash seed 不改變內容。
正式 k=9 初次生成後，canonical q orbit 的 masks／stabilizer／certificates 收尾
亦改成按具名輸入排序的平行 `imap`；每份 orbit 的計算獨立，輸出再排序，
沒有改變數學域或 JSON bytes。下表生成耗時保留初次生成時的較慢收尾版本；
最終 `--check` 使用這個平行收尾版本，兩者耗時可不同。

### 2.3 一次 criticality 的精確性

固定合法框列 p，任一完整內點賦色的 monochromatic 非框邊集合記為 V。
它延拓 G 當且僅當 V=∅；它延拓 G−e 當且僅當 V⊆{e}。
因此枚舉 **至多一條 monochromatic 邊** 的賦色，便同時給出所有 e 的完整
Σ(G−e)。不用對每條邊重新做十次圖著色決策。

實作用 H 的至多一條 monochromatic 內邊 colourings，再與所有實際 spokes 的
避色 bitset 交集。內邊刪除查該唯一內邊的標記 bitset；spoke 刪除則要求 H
本身 proper、其他 spokes 全部 proper，並令該 spoke 兩端同色。
這兩種情況完整且互斥，因每份允許賦色最多只有一條違規邊。
原已接受的列在每個 G−e 仍接受；只須為原拒絕列找新增 colourings。

[獨立暴力版](../scripts/c5_excess_two_finite_search_brute.py) 不共用這段方法：
逐邊移除原邊，再以十列各自的 ordinary DFS 重算完整 Σ。
小 k 的全部 q 圖直接重算，比對一次 criticality 的全部刪邊 masks。

### 2.4 完整對稱群、canonical form 與 orbit-stabilizer

NA／AD 使用 `D₅ × S₂ × S_(k−2)`，群大小 `20·(k−2)!`；
D6 使用 `D₅ × S_(k−1)`，群大小 `10·(k−1)!`。
S₂ 包含 root 互換，其餘置換只換完整 degree 相同的內點。
這個群搬動 **整張圖及所有實際附件**，不只搬 Q、H 或支援投影。
canonical form 是全部群作用後完整排序邊集的 lexicographic minimum。

特化 canonicalizer 先固定框 map。完整邊集先比較 frame-to-private spokes，
故相同完整 degree 類內按其五框 incidence vector 排序；只有支援完全相同的
頂點仍需列出所有置換。這是尋找同一個全群 minimum 的排序優化，未更換
canonical 定義。獨立暴力版列舉全部允許群元素，逐 orbit 比對兩者結果。
Σ 與 Q 在 canonical **完整圖** 重新計算，保留該代表自己的具名框位置。

每個 canonical form 的最小值達成 map 數等於其 stabilizer 大小，
`orbit_size=group_size/stabilizer_size`。全枚舉的累積權重另獨立驗證等於這個值；
其總和分別等於 q 與 crit 的有標號計數。

### 2.5 已證引理、支援子樹剪枝及 validate 開關

引理限於已證者：拒絕至少兩列須碰齊五個框點；拒絕一列須至少四個框點有
內鄰；H 是樹時在合格來源前提下 ε≤1。沒有 N∅、L-spoke 或猜想 E 剪枝。

單列的框支援引理實際只需 T4。若有至少兩個框點沒有內鄰，任一三色框列中
最多一個位置是 singleton，因此其中至少一個未碰框點使用重複色。
把該點改成尚未使用的第四色，得到合法 T4 列，且所有 actual spokes 的端點色
不變。用一次整圖 S₄ 換色搬回該 literal 列後取其延拓，再把該未碰點改回原色，
仍是完整合法延拓。
因此全部三色列皆接受，Q=∅。若只有一個未碰點 t，同一論證接受 singleton
位置非 t 的全部三色列，故最多拒絕 q_t；這另證多列拒絕須全框支援。
這一步不使用 Σ-critical、root 型或猜想下界。

fast 在部分附件分支記錄 `untouched` 與尚未指派的 spoke 總數 R。
即使每條剩餘 spoke 都接到一個不同的未碰框點，仍至少留下
`|untouched|−R` 個框點無內鄰。因此該值≥2 的整支最終 Q 必空，
可在計 q 前安全剪掉；這是真正提前剪枝，且不損失任何 q、crit 或 q 邊型數。
因為這些無 q 接法仍可能是 disk／T4，fast 的兩個前置數明記 `null`，
正式各 k 五類完整表一律使用 validate。

q 葉之後仍有兩列／樹的 critical-candidate guards；為保存 noncritical 邊型
統計，全部 q 葉仍計算完整刪邊 masks。這些後段 guards 不是 criticality pass
的速度來源。validate 完全關閉本節整組引理剪枝及 guards。
樹引理另有直接 Euler 證明：若 H 是樹，`e_H=k−1`；由
`2e_H+s=4k+ε`，非框邊數 `e_H+s=3k+ε+1`。
augmented disk 的 Euler 界要求它≤3k+2，因此 ε≤1。
這不需要猜想 E。Euler 必要條件 e_H≥k 在本 ε=2 域的兩模式都保留，
已使 disk 來源 H 不可能是樹，所以樹 guard 是冗餘的已證檢查。
實際剪枝數保存於 `lemma_pruning`／`diagnostics`。

小域 fast 實際支援子樹剪枝數（節點數，非圖數）：

| 型 | k=3 | k=4 | k=5 | k=6 |
| --- | ---: | ---: | ---: | ---: |
| NA | 0 | 18 | 282 | 2,745 |
| AD | 0 | 104 | 1,213 | 7,563 |
| D6 | 0 | 54 | 522 | 3,388 |


## 3. k≤6 控制層與驗收

**五項驗收全部通過。** [validation.json](../artifacts/c5_excess_two_finite_search/validation.json)
保存逐型逐 k 的 counts、q／crit canonical 集合與 orbit weights 比對，
全部 canonical forms 都是完整原圖，沒有投影替代。

| 驗收項 | 實際結果 |
| --- | --- |
| NA validate k=4、5、6 五類有標號計數 | 分別完整相等於 `2/80/40/0/0`、`116/4020/3840/240/0`、`5697/182580/175860/4320/1440` |
| k≤6 q／crit 逐 orbit canonical 集合 | NA、AD、D6 與獨立暴力版均相等，orbit weights 亦相等；AD／D6 擴大驗收到 k=6 |
| 一次 criticality 與逐邊 DFS | k≤5 全部 4,710 張有標號 q 圖、72,910 次具名非框刪邊；0 mismatch |
| AD／D6 獨立暴力與正控制 | E1 原始 935（AD、k=3）與 951（D6、k=5）均找到；來源 JSON pointers／hash 保存 |
| fast／validate 一致 | 三型 k≤6 的有標號 q／crit 數、完整 canonical 集合及 orbit weights 全部相同；Q 形狀及四組 noncritical 邊型診斷亦相同 |

NA k=2、3，AD k=2，D6 k=1、2、3 沒有符合 root degree／三-spoke 的內部邊集，
也另以暴力版與枚舉器確認。以下全部是 validate 模式。
秒數採 CLI 印出的核心搜尋耗時；subprocess 起始／完整 wall time 另見 `execution.json`。
NA k=2、3、4 使用 `--jobs 4`，其餘 k≤6 使用 `--jobs 12`；不同 jobs 只改排程。

| 型 | k | edgesets | disk | t4 | q | crit | crit orbits | 搜尋秒數 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NA | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0.115 |
| NA | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0.117 |
| NA | 4 | 2 | 80 | 40 | 0 | 0 | 0 | 0.179 |
| NA | 5 | 116 | 4,020 | 3,840 | 240 | 0 | 0 | 0.185 |
| NA | 6 | 5,697 | 182,580 | 175,860 | 4,320 | 1,440 | 3 | 0.321 |
| AD | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0.143 |
| AD | 3 | 1 | 10 | 10 | 10 | 10 | 1 | 0.149 |
| AD | 4 | 14 | 440 | 240 | 80 | 0 | 0 | 0.156 |
| AD | 5 | 320 | 16,380 | 15,420 | 1,140 | 0 | 0 | 0.200 |
| AD | 6 | 10,771 | 512,460 | 496,620 | 15,600 | 960 | 2 | 0.547 |
| D6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0.149 |
| D6 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0.147 |
| D6 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0.144 |
| D6 | 4 | 7 | 300 | 120 | 120 | 120 | 2 | 0.163 |
| D6 | 5 | 275 | 16,920 | 13,080 | 3,120 | 2,040 | 9 | 0.256 |
| D6 | 6 | 11,582 | 629,550 | 570,750 | 43,200 | 4,800 | 4 | 0.453 |

[positive_controls.json](../artifacts/c5_excess_two_finite_search/positive_controls.json)
另保存 E1 935／951 的兩份 **完整原始 minima 記錄**、原 artifact 路徑／大小／hash、
具名 JSON pointers 及逐記錄 hash，不只擷取邊集。驗收由此新封存檔讀取正控制；
原始 ignored E1 檔存在時另外核對完全相同，缺檔時仍能在乾淨 worktree 重播。
另外以只讀的 source-existence 攔截實際走過「原 E1 缺檔」分支，
完整 validation 輸出與最終存檔逐 byte 相同，exit 0、15.173 秒；原 E1 檔沒有更動。
archive SHA-256 為
`06a122072780680f18fce46b528686d9944704bff6575c730e8ee563df4337cc`。

正控制的 canonical 框 map 可能搬動 Σ mask，因此原始來源 mask 與 canonical mask
分別保存，沒有要求 D₅ 變換保持同一 mask。

| 原始控制 | 本輪 canonical Σ | crit orbit file | orbit 大小 |
| --- | ---: | --- | ---: |
| E1 935，AD k=3，degrees (4,5,5) | 942 | [AD3 orbit 1](../artifacts/c5_excess_two_finite_search/AD_k3_validate/crit_orbits/orbit_0001.json) | 10 |
| E1 951，D6 k=5，degrees (4,4,4,4,6) | 1014 | [D6-5 orbit 3](../artifacts/c5_excess_two_finite_search/D6_k5_validate/crit_orbits/orbit_0003.json) | 120 |
| 導覽 NA6-1 | 999 | [NA6 orbit 2](../artifacts/c5_excess_two_finite_search/NA_k6_validate/crit_orbits/orbit_0002.json) | 480 |
| 導覽 NA6-2 | 999 | [NA6 orbit 3](../artifacts/c5_excess_two_finite_search/NA_k6_validate/crit_orbits/orbit_0003.json) | 480 |
| 導覽 NA6-3 | 959 | [NA6 orbit 1](../artifacts/c5_excess_two_finite_search/NA_k6_validate/crit_orbits/orbit_0001.json) | 480 |

生成器是 [特化搜尋](../scripts/c5_excess_two_finite_search.py)、
[獨立暴力參考](../scripts/c5_excess_two_finite_search_brute.py)，
驗收入口是 [validation driver](../scripts/c5_excess_two_finite_search_validation.py)。
所有生成寫入採 exclusive-create (`xb`)；既有結果存在即拒絕覆寫。
`--check` 重算確定性 JSON，對結果及每個 crit orbit 檔逐 byte 比較。

驗收 driver 最終固定讀取 48 份具名小域輸入，避免正式擴大 k 後意外改動驗收域。
初次用目錄發現輸入時新增了四份 NA k=2、3 的空結果，兩次 replay 因 input-hash
清單改變而 exit 1；沒有數學 mismatch。修正固定輸入後重新 exclusive-create 最終
validation，原初次結果保存在 scratch，最終 ordinary／hash-seed replay 在 §5 記錄。

另外以獨立全群置換補查 canonical form 及 stabilizer：52,728 次窮舉比較、
942 次固定 seed 的隨機比較，全部一致，10.870 秒；這是小域／抽樣的補充檢查，
不代替上述完整 q／crit orbit 集合比對。

## 4. 正式搜尋、orbit 目錄與 Q 形狀

驗收全過後才擴展，三型先完成 k=7，再依實際耗時完成 k=8；
使用三份平行 run，各 `--jobs 10`，合計最多 30 workers。
k=9 先完整產生 H 代表，再按排序位置抽查各型 256 個 templates（包括兩端），
用實測 template CPU 推估附件 pass，另對附件最多的 templates 作壓力取樣。
這是時間估計而非數學上界；沒有把 sample 當作完整圖類結果。

| 型 | k=9 H orbits | H 產生實測秒數 | 附件 pass 推估秒數（10 cores） | 合計估計 |
| --- | ---: | ---: | ---: | ---: |
| NA | 227,468 | 151.468 | 458.433 | 約 10.2 分鐘 |
| AD | 227,963 | 170.803 | 377.844 | 約 9.1 分鐘 |
| D6 | 94,481 | 235.180 | 137.377 | 約 6.2 分鐘 |

完整取樣、壓力取樣及補充 canonical audit 見
[performance_estimates.json](../artifacts/c5_excess_two_finite_search/performance_estimates.json)。
據此判定 k=9 可行才啟動三份正式完整 run。三型已全部完成；本輪停止點為 k=9，
k≥10 沒有正式資料，也沒有從 k=9 的無反例推算更大 k。

k=10 沒有啟動。僅作時間推估：同為 `--jobs 10`，原始生成的 k=8→9
核心時間倍率 NA／AD／D6 分別約 21.46／17.98／19.34。
若下一級倍率相近，k=10 約需 6.66／5.12／4.61 小時／型，之後還須完整兩輪
byte replay。本輪因此停在已完整生成及重播的 k=9。
這使用較慢的原始收尾版本；最終平行收尾可改變耗時，倍率也不是嚴格上界，
不是 k=10 的搜尋結果或來源排除。
以下全部是 validate，故五種 category 計數都是實際完整數，沒有把 fast 的
`disk=null`／`t4=null` 當成零或完整數。

| 型 | k | edgesets | disk | t4 | q | crit | crit orbits | 搜尋秒數 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NA | 7 | 327,173 | 8,217,312 | 7,890,912 | 112,800 | 3,600 | 2 | 2.785 |
| NA | 8 | 22,647,425 | 378,081,900 | 364,646,700 | 7,027,200 | 316,800 | 22 | 52.051 |
| NA | 9 | 1,880,480,735 | 18,061,928,640 | 17,505,537,840 | 304,403,400 | 2,721,600 | 27 | 1116.950 |
| AD | 7 | 479,670 | 16,738,200 | 16,433,400 | 325,200 | 2,400 | 1 | 4.683 |
| AD | 8 | 27,084,365 | 584,858,160 | 576,531,360 | 8,040,600 | 0 | 0 | 57.006 |
| AD | 9 | 1,894,110,540 | 22,305,577,140 | 22,072,426,740 | 224,569,800 | 403,200 | 5 | 1024.962 |
| D6 | 7 | 592,857 | 23,151,000 | 22,027,800 | 986,400 | 176,400 | 25 | 3.741 |
| D6 | 8 | 37,448,684 | 910,589,400 | 881,143,200 | 25,426,800 | 2,016,000 | 41 | 44.302 |
| D6 | 9 | 2,888,856,712 | 38,580,227,280 | 37,711,532,880 | 732,009,600 | 14,112,000 | 35 | 856.999 |

### 4.1 crit orbit 目錄摘要

| 型／k | orbit 大小×orbit 數 | m 範圍 | unary 範圍 | crit 的 Q 形狀（有標號） |
| --- | --- | ---: | ---: | --- |
| NA／6 | 480×3 | 1 | 0–1 | 單點 480；相鄰二點 960 |
| NA／7 | 1,200×1；2,400×1 | 1–2 | 1–2 | 單點 3,600 |
| NA／8 | 14,400×22 | 1–2 | 1–2 | 單點 259,200；相鄰二點 57,600 |
| NA／9 | 100,800×27 | 1–2 | 1–2 | 單點 2,721,600 |
| AD／3 | 10×1 | 1 | 0 | 三點弧 10 |
| AD／6 | 480×2 | 1 | 1 | 非相鄰二點 960 |
| AD／7 | 2,400×1 | 1 | 2 | 單點 2,400 |
| AD／9 | 50,400×2；100,800×3 | 1 | 2 | 非相鄰二點 201,600；單點 201,600 |
| D6／4 | 60×2 | 0 | 1 | 單點 120 |
| D6／5 | 120×1；240×8 | 0 | 1–2 | 單點 1,920；非相鄰二點 120 |
| D6／6 | 1,200×4 | 0 | 1–2 | 單點 4,800 |
| D6／7 | 3,600×1；7,200×24 | 0 | 1–2 | 單點 176,400 |
| D6／8 | 25,200×2；50,400×39 | 0 | 1–2 | 單點 2,016,000 |
| D6／9 | 403,200×35 | 0 | 1–2 | 單點 14,112,000 |

每個 crit orbit 另有 `TYPE_kK_MODE/crit_orbits/orbit_NNNN.json`，
保存 canonical 完整邊集、orbit／stabilizer 大小、完整 Σ、具名 Q、c(Q)、
|Q|+c(Q)、m／unary 數、每個刪 roots 後原分量的 vertices／實際支援／root incidence／
spokes／內邊、各 root spokes。所有 crit 圖再以 NetworkX 產生並檢查完整 augmented
及 disk rotation；逐邊新增列 witness 以獨立 MRV backtracking 計算。
D6 僅一個 root，故 m=0；unary 數計刪該 root 後實際原分量。

### 4.2 全部 q 圖的 Q 形狀

| 型／k | 單點 | 相鄰二點 | 非相鄰二點 | 三點弧 | 兩點弧＋孤點／更大 |
| --- | ---: | ---: | ---: | ---: | ---: |
| NA／5 | 240 | 0 | 0 | 0 | 0 |
| NA／6 | 3,360 | 960 | 0 | 0 | 0 |
| NA／7 | 112,800 | 0 | 0 | 0 | 0 |
| NA／8 | 6,969,600 | 57,600 | 0 | 0 | 0 |
| NA／9 | 303,597,000 | 806,400 | 0 | 0 | 0 |
| AD／3 | 0 | 0 | 0 | 10 | 0 |
| AD／4 | 80 | 0 | 0 | 0 | 0 |
| AD／5 | 1,020 | 120 | 0 | 0 | 0 |
| AD／6 | 14,640 | 0 | 960 | 0 | 0 |
| AD／7 | 308,400 | 16,800 | 0 | 0 | 0 |
| AD／8 | 7,659,000 | 381,600 | 0 | 0 | 0 |
| AD／9 | 213,129,000 | 11,239,200 | 201,600 | 0 | 0 |
| D6／4 | 120 | 0 | 0 | 0 | 0 |
| D6／5 | 3,000 | 0 | 120 | 0 | 0 |
| D6／6 | 43,200 | 0 | 0 | 0 | 0 |
| D6／7 | 943,200 | 43,200 | 0 | 0 | 0 |
| D6／8 | 24,116,400 | 1,310,400 | 0 | 0 | 0 |
| D6／9 | 690,480,000 | 41,529,600 | 0 | 0 | 0 |

### 4.3 全部 q 圖的 noncritical 邊型

下表計 **非 critical 邊的有標號總數**，一張圖可有多條同型邊；
`q_graphs_with_noncritical_type` 另保存至少含該型一條邊的圖數，
`q_noncritical_typesets` 保存每張圖實際出現哪些型，critical 圖另記為 `critical`。
不把不同型的圖數直接相加當作圖聯集數。

| 型／k | root spoke | degree-4 spoke | 內邊含 root | 內邊不含 root |
| --- | ---: | ---: | ---: | ---: |
| NA／5 | 480 | 0 | 0 | 0 |
| NA／6 | 6,720 | 0 | 0 | 0 |
| NA／7 | 201,600 | 412,800 | 420,000 | 306,000 |
| NA／8 | 9,777,600 | 28,123,200 | 29,649,600 | 28,699,200 |
| NA／9 | 357,512,400 | 1,397,743,200 | 1,417,096,800 | 1,762,992,000 |
| AD／3 | 0 | 0 | 0 | 0 |
| AD／4 | 0 | 240 | 240 | 0 |
| AD／5 | 840 | 720 | 960 | 180 |
| AD／6 | 13,920 | 25,920 | 20,400 | 16,560 |
| AD／7 | 369,600 | 1,262,400 | 710,400 | 1,236,000 |
| AD／8 | 8,420,400 | 34,714,800 | 20,205,000 | 48,124,800 |
| AD／9 | 227,354,400 | 1,051,898,400 | 565,538,400 | 1,712,680,200 |
| D6／4 | 0 | 0 | 0 | 0 |
| D6／5 | 0 | 4,320 | 2,160 | 2,520 |
| D6／6 | 14,400 | 136,800 | 64,800 | 115,200 |
| D6／7 | 316,800 | 3,628,800 | 1,411,200 | 4,233,600 |
| D6／8 | 10,369,800 | 108,221,400 | 39,853,800 | 159,944,400 |
| D6／9 | 320,644,800 | 3,608,942,400 | 1,219,176,000 | 6,179,140,800 |

NA k=5 的全部 240 張 q 圖只出現 root spoke 非 critical，與導覽的早期觀察一致；
NA k=6 的三個真正 critical orbit 同時否定 N∅ 與 L-spoke。

### 4.4 與猜想 E 的比較

**截至已列出的完整有限搜尋，沒有 |Q|+c(Q)>4 的合格圖。**
crit 的 Q 只出現單點、相鄰二點、非相鄰二點及三點弧，其 |Q|+c(Q)
分別為 2、3、4、4，均不超過 ε+2=4。
依 [E3 §2](../artifacts/c5_excess_two_e3/REPORT.md#2-第-0-步約化成立)，
`|Q|+c(Q)>4` 等價於 Q 含兩點弧加孤點的三點子集，這些三點都在 D₅ 下等價於
{0,1,3}。checker 逐項驗證全部 32 個 Q 子集的等價式。
任一 crit 圖若觸發該條件，就是猜想 E 在 ε=2 的反例；完整 certificate 已具備
反例保存所需資料，並應停止擴大 k。

## 5. 實際檢查與環境

指定 Python 為 `/home/ray/developer/ai/math/.venv/bin/python`，Python 3.14、
NetworkX 3.5；沒有 numba、pynauty 或 plantri。主枚舉的 augmented planarity
使用環境現有 rustworkx，所有 crit rotation 與控制另經 NetworkX。
沒有四色定理 oracle；沒有新 Lean theorem，沒有執行 lake build。

正式 CLI 的生成與重播命令如下；生成命令只用於尚不存在的目標檔，
已有結果請用 `--check`。不含 `--type/--k` 的生成模式供 `tools/artifacts.py`
producer 使用，只 exclusive-create 本輪明列有限計畫的缺檔；已有小 orbit 證書
先比 byte 後才沿用。`--check` 會真正重跑搜尋，不是只核對存檔自身 checksum。

```sh
PY=/home/ray/developer/ai/math/.venv/bin/python
$PY scripts/c5_excess_two_finite_search.py --type NA --k 6 --validate --jobs 12
$PY scripts/c5_excess_two_finite_search.py --type AD --k 3 --validate --jobs 12
$PY scripts/c5_excess_two_finite_search_brute.py --type D6 --k 5 --jobs 4 --output scratch/task-es-brute/brute_D6_k5.json
$PY scripts/c5_excess_two_finite_search_validation.py
$PY scripts/c5_excess_two_finite_search.py --check --jobs 32
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_finite_search.py --check --jobs 32
$PY scripts/c5_excess_two_finite_search_validation.py --check
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_finite_search_validation.py --check
$PY scripts/check_docs.py
$PY tools/docgraph check
git diff --check
```

正式搜尋 41 份結果（25 validate、16 fast）、獨立 brute 16 份結果的最終
exclusive-create 生成全部實際 exit **0**；來源命令、stdout／stderr、核心秒數與
完整 wall 秒數分別保留於 execution 紀錄。k=9 的三份正式生成也全部 exit 0，
沒有從 scratch 的初步 k=7／8 輸出直接複製正式結果。

小域生成的實際 stdout 示例（全部 exit 0）：

```text
GENERATED NA_k6_validate.json: {'edgesets': 5697, 'disk': 182580, 't4': 175860, 'q': 4320, 'crit': 1440}, crit_orbits=3, seconds=0.321
GENERATED AD_k3_validate.json: {'edgesets': 1, 'disk': 10, 't4': 10, 'q': 10, 'crit': 10}, crit_orbits=1, seconds=0.149
GENERATED: D6 k=5 {'edgesets': 275, 'disk': 16920, 't4': 13080, 'q': 3120, 'crit': 2040}; q_orbits=14 crit_orbits=9; 2.654 seconds; scratch/task-es-brute/brute_D6_k5.json
```

驗收 driver 的最終生成／ordinary replay／`PYTHONHASHSEED=17` replay
已實際分別 exit **0／0／0**，7.867／7.842／7.942 秒。
其輸出包括 `acceptance_passed=true`、4,710 個 labelled q 與 72,910 次刪邊比較
全為 `mismatches=0`。正式搜尋的 full ordinary 及 `PYTHONHASHSEED=17` replay 均已實際通過，
41 份結果及 200 份 orbit 證書在兩輪都逐 byte 相同。
與原生成時不同的 worker 數、平行收尾及 hash seed 都沒有改動任何 byte。

| 實際檢查 | exit code | 實測秒數 | 驗證範圍 |
| --- | ---: | ---: | --- |
| 主搜尋 `--check --jobs 32` | 0 | 961.042 | 41 份結果＋200 份 orbit 檔逐 byte 相同 |
| 主搜尋 `PYTHONHASHSEED=17 --check --jobs 32` | 0 | 1002.873 | 41 份結果＋200 份 orbit 檔逐 byte 相同 |
| 驗收 driver 生成 | 0 | 7.867 | 固定 48 份小域輸入及正控制 archive |
| 驗收 driver `--check` | 0 | 7.842 | 完整 validation.json 逐 byte 相同 |
| 驗收 driver `PYTHONHASHSEED=17 --check` | 0 | 7.942 | 完整 validation.json 逐 byte 相同 |

不以 validation driver 的 replay 代替主搜尋完整重播。


基準 ignored artifact 重建命令：

```sh
/home/ray/developer/ai/math/.venv/bin/python tools/artifacts.py rebuild -j 4
```

實際 exit **1**，316.800 秒；148 個 producers 中 ok=120、blocked=22、failed=4、
mismatch=2。這是歷史產物重建，不是 ES 驗收失敗。
兩份 mismatch 是 E1 observations 與 single-spoke observations；四份 fail 是歷史
producer 遇既有較小產物時的 overwrite guard／缺檔條件。重建階段原有 tracked 檔沒有改變。
E1 原始 ignored observations 從主 workspace 恢復前，核對本 worktree MANIFEST
的 1,125,356 bytes 及 SHA-256
`23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e` 全相同，
以 exclusive-create 恢復該原檔，沒有登錄新 hash 或採信 mismatch `.rebuilt` 作原始控制。

基準文件檢查實際結果：`check_docs` exit **1**，恰兩個任務已知 missing-path：
`audits/2026-10-04-task-d5/c4/scope_ledger.json` 及
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。
`docgraph check` exit **0**（62 documents、213 relations、5 families、0 errors）；
`git diff --check` 也已實際 exit **0**。
新增報告後 `check_docs` 實際 exit **1**，另增加一項
`not directly indexed by STATUS: docs/c5_excess_two_finite_search.md`。
既有 checker 要求每份 docs Markdown 都直接入 STATUS；本任務限定只新增檔，
因此沒有修改原 STATUS 來解除該第三項。實際輸出為
`FAIL: 3 errors`；後續整合者可處理索引。
唯一超過 1 MB 的本任務新檔是 `NA_k9_validate.json`，1,152,495 bytes；
已只對此新檔執行 `tools/artifacts.py record artifacts/c5_excess_two_finite_search/NA_k9_validate.json`，
實際 exit 0。MANIFEST／.gitignore 的變動限該新產物登錄，沒有把歷史 mismatch
重新登錄成新來源。普通及 seed17 的完整 byte 重播均已實際 exit 0；本輪全部數學驗收通過。

## 6. 證據層與限制

| 證據層 | 本輪範圍 |
| --- | --- |
| 新紙面理由 | 枚舉完整性、Euler 邊數必要界、T4 monotonicity、one-pass 等價、full-group canonical／orbit-stabilizer |
| 沿用已證引理 | 有效內點 degree≥4、T4 三-spoke、Q 非空的 H 連通及框支援必要條件；保留各自來源前提 |
| 外部有限圖工具 | rustworkx augmented planarity 決策；每份 crit 另以 NetworkX 檢查 rotation 與 C₅ outer face |
| Python 有限證書 | 三型所列 k 的完整搜尋、獨立小域 brute／全 labelled q 刪邊驗收、保存的完整圖及 witnesses |
| Lean 普通證明／native_decide | 無新增，未執行 lake build |

本輪的結果是完整 prescribed-degree 三型、指定有限 k 的 Python 證據。
演算法覆蓋、單調性及 one-pass 等價性在本報告給出紙面理由；有限 orbit 與
witness 由實際 checker 保存。內部 H 連通及三-spoke、框支援引理沿用已有報告的
適用前提，沒有重證全部任意大小 topology。平面性決策與 NetworkX rotation 是
有限圖 certificate，不是來源化約的 Lean proof。

無反例只表示所列有限域沒有反例；不證成猜想 E 的 ε=2 任意大小層，
不證成 `K∞=K≤5`，不更改 E3／E4 的紙面排除範圍。N∅ 與 L-spoke 的既有
NA6 反例作正控制保留。未列出的 k、未完成的 run 及 scratch 原型初步輸出
不作正式證據。沒有 commit／push，既有導覽、STATUS、HANDOFF 與 README 保持原檔。


## 7. 新增交付範圍

完整新增檔案路徑／大小／hash 清單見 `file_inventory.json`；
實際命令、輸出與 exit codes 見 `execution.json`。

- `scripts/c5_excess_two_finite_search.py`：三型特化搜尋、validate／fast、parallel workers、exclusive-create 與逐 byte replay。
- `scripts/c5_excess_two_finite_search_brute.py`：獨立有標號暴力參考，只供 k≤6 驗收。
- `scripts/c5_excess_two_finite_search_validation.py`：固定具名小域的五項驗收及正控制重播。
- `docs/c5_excess_two_finite_search.md`：本報告。
- `artifacts/c5_excess_two_finite_search/`：41 份搜尋結果、16 份 brute 結果、200 份 crit orbit 完整證書、`validation.json`、`positive_controls.json`，及最終執行／耗時／新增檔案紀錄。

200 份 orbit 檔含小域 fast／validate 的同圖證書各一份；按 validate 計算的
真正不同「型＋k＋orbit」共有 179 份，沒有把 mode 的重播副本算成新圖。
原型及行政 scratch 沒有入庫；本輪初始複製位置是 worktree 的 `scratch/`，
最終封存位置為 `/home/ray/developer/ai/math-task-es-scratch`，僅保留執行過程，
不是正式 checker 的輸入。正式重播依本 artifacts 目錄，不依 `/tmp` 或 scratch。
除明確登錄本任務新大檔所需的 MANIFEST／.gitignore
外，既有研究文件沒有變動。未 commit／push。
