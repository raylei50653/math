# M2：U1 §3 任意大小、marked 344 域與完整接回的獨立紙面稽核

2026-10-07。凍結候選 `ba0b447f09617591d9f2ba81c988f537af771791`，
來源 checkout `/tmp/math-m2-ba0b447-audit`；本輪只新增本稽核及
`run_controls.py`，沒有修改來源、producer、舊證書或舊稽核。

**判定：指定 §3 化約為 triggered and holds；未找到新的紙面缺口或反例。**
此判定沿用具名全 degree-4 分類與其既有有限拓撲信任界線。
新有限控制核對標記覆蓋與色框搬運；任意大小覆蓋仍由下述紙面推論負責。
本稽核不重新證明全部上游拓撲模板，也不把來源實現、E5 新證明、
U2–U4、一般 ε≥3、一般出口或 K∞=K≤5 判為完成。

## 1. 指定來源與可沿用的前提

主來源為 `docs/c5_excess_two_no_mixed_core44.md` §3，依賴
`docs/c5_excess_two_mixed_omission.md` §4 的保留相鄰 bridge markers 化約。
既有 `audits/2026-10-07-c44pp-mixed-audit/REPORT.md` §1.4 及其
`verify.py` 已給同一必要域的指定稽核；本輪明確沿用其中上游分類的
完整性與原信任界線，而另外重讀化約並寫獨立控制，不 import 該 verifier。

將主來源 §1 給定的 M 帶入時，M 自己是 disk、接受 T4、拒絕 singleton q、
有效內點全 degree 四的 minimal q-core，原 z、w 相鄰且原 zw 是內部 bridge。
上述化約所用的分類、run 附件、marker transfer 都只涉及這些 M 的條件。
「外面還有一份 mixed」並不是它們的前提，因此用在 no-mixed 來源成立。
這裡沒有把 G 的 Σ-criticality 換成 M 的 q-criticality，也沒有另假定
G−zw 全收；M 所需前提由主來源 §1 的 core 身份提供。

主來源的雙 spoke 身份沒有省略原 piece，所以 G=M 加回兩條原具名 spokes。
後續染色接口只需 z、w 的完整 ordered pair，無需保存每個被縮減 contact
的獨立座標。spoke＋unit-unary 身份則另由主來源 §2 處理，本報告不混入
雙 spoke 的有限域計數。

## 2. Run、零 gap 與 singleton markers

分類後的每個可縮 uniform run 都有相同的兩個實際 boundary 鄰點。
任取同一個 proper boundary coloring β，這些點共用可用色集 A，|A|≥2。
用 R_t(A) 表示 t 個 run 內點、兩側外部端點色皆固定時的精確延拓 relation。
端點色可在 A 外，證明不把它们限制到 A 中。

|A|=2 時，所有合法 run 染色交替；正長度的延拓性只依奇偶。
|A|≥3 時，t=1 可選一色同時避開兩端；t≥2 的第一個點至少有兩色可取，
下一個點的可取末色已是全部 A，後續仍是全部 A，最後也能避開右端。
因此 R_(t+2)=R_t，t≥1。t=0 是直接邊，relation 是兩端色不等；
它不能一概當作正偶數 gap。例如 A={0,1,2}、两端都0，零 gap 不可行，
兩點 gap 可行。本輪負控制實際觸發並確認這個差別。

先把原 z、w 當作必須保留的 singleton，把各 run 切成未標記 gaps。
每個零 gap 保持零，正奇 gap 用一點，正偶 gap 用兩點。
原 leaf、triangle 頂點、path 的原兩端以及兩-run 枝的 X 首點均保留。
leaf 的可用色集可能只有一色，因此不能套用 uniform run 的 |A|≥2。
當 marker 是 leaf 或 triangle parent，這個保留規則仍適用。

兩 markers 若在同一 run，因原 zw 是它們之間的原邊，它們必相鄰；
marker 中間沒有正 gap。若跨 run、在 parent–branch 首點或 nonleaf–leaf
邊上，也仍是原相鄰頂點。故沒有收縮操作跨過 zw；原 zw 始終字面保留，
两 marker branch sets 不合併。刪 zw 時也只是刪這條原邊，不會刪去某個
未標記 gap 裡的 transfer 邊。

紙面長度界如下：一個 run 內至多兩個相鄰 markers，加兩個正 gaps 的
最短奇偶代表最多六點；原奇數 run 因奇偶保持只需1、3、5；原正偶數
run 只需2、4、6。無 marker 的 run 用一／兩點。不同 run 分別處理。
這給單 triangle 單-run 家族160份、兩-run 家族64份、偶數 path56份。
雙 triangle 的分類已是六個原內點，原 zw 是唯一直接 bridge，沒有 run，
markers 原樣保留，共64份；合計344份。

每次縮減可在原同附件路徑內用互斥連通 branch sets 實現：刪多餘 spokes
後收縮，boundary 點、markers、leaf 與 triangle 點保持 singleton。
這是 boundary 固定 minor。marker 的原 boundary neighborhood 保持，
所以原來不存在的待接回 spoke 縮減後仍不存在。

## 3. 十列完整 joint relation 與字面接回

Transfer 證明應同時固定所有保留的 marker、triangle、leaf 及必要分隔點色。
各 gap 的 endpoint transfer 完全相同，且 gaps 的內點互斥；在同一份原圖
及同一 β 中逐段選延拓，得到完整保留 tuple 的雙向延拓。最後對非 root
保留座標取存在量詞，才得到 ordered root-pair relation。由此同時保持
M 與 M−zw 在全部十列的 joint root relation。

這不需要將兩 root 色 marginals 相乘。K_β(M*) 中的一對 (a,d) 是同一份
全圖染色的兩個原 root 色，因而加回原 spokes b_z z、b_w w 的精確結果為

`{(a,d)∈K_β(M*): a≠β(b_z), d≠β(b_w)}`。

接回只檢查同一對色的兩條新邊，沒有重新選不同 components 或列的 witness。
兩條邊以外没有其他原 piece 要接回，所以這個 pair interface 在雙 spoke
身份已充分。沒有宣稱其他原 contact 座標在長短圖之間保持一對一相等。

有限域列出每個 root 在 M* 中所有不存在的 boundary spoke 位置。
這包含來源的那兩個字面位置；未先按 G 的 disk、原 spoke 上界或
Σ-criticality 篩選只會放寬待排除域，不會漏掉來源。所存 marker pair 使用
短圖頂點順序；如果原 z、w 的角色相反，用同一整圖頂點映射追蹤兩角色，
並交換兩個 spoke 指派。完整笛卡兒接回域對此封閉，因此沒有 root 次序漏洞。

## 4. 同一整圖 D₅／S₄ 正規化

933／941 接受全部 T4，故 q 是五個 singleton 三色列之一。
一個 boundary D₅ 動作及一個全圖 S₄ 色置換可把 q 對齊01012；
同時搬動整張 G、兩個 named roots、全部 spokes、attachments 与 witnesses。
S₄ 不改變 boundary equality-pattern 接受集合；D₅ 把完整 Σ 搬至同一目標
軌道，有限排除比较全部軌道像，所以没有只固定 q 卻漏掉來源 Σ 的問題。

給整圖頂點映射 φ 及顏色置換 π，一條原 spoke rz 在搬運後為
φ(r)φ(z)，其判準從 `color(z)≠β(r)` 同步變成
`π(color(z))≠π(β(r))`。兩條 spoke 使用同一個 π；各十列的 root pairs
使用同一個字面 U={0,1,2,3}。不能獨立正規化兩側分量，但指定做法未如此。

新控制明確枚舉10列×10個 D₅ 元素×24個 S₄ 置換×16個 ordered root 色對
×25個 spoke endpoint 對，960,000 次確認兩條接回邊的 joint predicate 搬運前後一致。
這是精確字面 transport 的有限控制；完整 relation 的等價由全圖染色的
置換雙射負責，沒有把這個控制說成來源實現證書。

## 5. 依賴與拓撲信任界線

| 具名依賴 | 此化約使用的內容 | 本輪處理與界線 |
| --- | --- | --- |
| `c5_k4_blocks.md` §4、`c5_weak_list_cores.md` | 全 degree-4 minimal q-core 的 Gallai／degree-list 及 block 合成 | 沿用外部 degree-choosability 定理與紙面分類；未新形式化或重審全部上游 |
| `c5_tree_cores.md`、`c5_excess_two_path_edge.md` §2 | 原 path 兩端及同實際附件的正偶 runs；八份 T4 基底 | 重讀附件分類與 parity；只做 marked grammar 控制，未重跑全部拓撲枚舉 |
| `c5_triangle_branches.md` §1–2 | triangle palette、branch 位置與18個 canonical disk bases | 沿用177,280 lifts 的原 NetworkX planarity replay；部分拒絕模板沒有逐例 Kuratowski 證書，不能稱純紙面／純證書拓撲證明 |
| `c5_triangle_forks.md` | 單 triangle 外掛樹不分叉 | 沿用紙面 minor 化約與既有 subdivisions；未重播完整上游枚舉 |
| `c5_triangle_path_reduction.md` §3–5 | 單 run／X,Y^(2m),leaf 附件形狀與8個 normal forms | 重讀任意長度的 minor／transfer；新 marked 控制讀8份保存的原邊集，原18-base 完備性仍依前列 NetworkX 邊界 |
| `c5_two_triangle_blocks.md` | 兩個互斥 triangles、直接 bridge、沒有額外 tree | 沿用既有紙面分類與拓撲證書；沒有把本輪有限控制當成新的無界分類 |
| `c5_excess_two_mixed_omission.md` §4、其344-core artifact、既有 mixed audit §1.4 | 同 source、adjacent singleton bridge markers 的必要域 | 本輪獨立重推 transfer，從上游18＋8邊集及 path 附件表重建 marked grammar，所有344份均有覆蓋 |

E6-D 與原省略身份表是主來源 §1 所需依賴；本報告的入口是已指定的
雙 spoke core 身份，沒有擴展或替代其他稽核者對該身份與 §2 的核對。
Disk／boundary-apex 等價、minor 閉性与 Kuratowski 非平面性仍是紙面拓撲
soundness 前提。新 controls 沒有呼叫 NetworkX 或任一 planarity oracle。
`lake build` 和 LC 公理核對属于 M3，未在本報告執行，也不形式化此任意大小化約。

## 6. 新控制的實際結果與 findings

實際执行：`python3 audits/2026-10-07-m2-u1-audit/run_controls.py`，exit0。

| 控制 | 結果 | 分類 |
| --- | ---: | --- |
| 全部 ∣A∣≥2 色集、兩側字面端點、長度0..24的 transfer | 4,400次一致 | triggered and holds |
| 零 gap 不可誤換正偶 gap | A={0,1,2}、端色(0,0)：R₀=false，R₂=true | triggered and holds，負控制成功觸發 |
| 上游18＋8 templates、run 長度至20、path 原附件表的每個相鄰 bridge marker | 12,282次壓縮皆落入344域，且全344份被覆蓋 | triggered and holds |
| 全圖 D₅／S₄ 下两條 spoke 的 joint predicate | 960,000次一致 | triggered and holds |
| 全部上游 NetworkX 拒絕模板獨立重播 | 未執行 | not triggered，上游信任範圍保留 |
| 完整Σ933／941來源正控制 | 未構造 | not triggered；必要域無目標命中不是來源可實現性 |

輸入 SHA256：

- `artifacts/c5_excess_two_mixed_omission/observations.json`：`ded2ff09f1fba01426d801bfda0d975e9c52b5e89554538d9d963f5656db98cc`。
- `artifacts/c5_triangle_branches/observations.json`：`8cfa0382908cb2ab81b177fcbf81a3ca62f4ad4163a206db5be5f4325a700e3f`。
- `artifacts/c5_triangle_path_reduction/observations.json`：`2689b6fc7e08d91c4ea1ff112b801f50dbcbaffa98f42aad3924360bde897c7e`。

新 control 首次全跑只在期待的 family 字串上失敗：我寫 `even_path`，
既有 schema 名稱實為 `path`。修正這個新控制的期待值後完整重跑 exit0，
沒有改歷史 input 或數學 payload。這是本輪控制程式錯誤，不是來源 finding。

**Findings：沒有需要修改候選的 §3 數學 finding。**
標記、零 gap、leaf／triangle、同源 joint、原 spoke 字面位置及整圖搬運均有
紙面責任與可觸發的有限控制。有限控制不證明無界完備性；完整 U1 驗收仍需
合併原身份／§2 稽核、3,498份接回及 witnesses 的獨立有限稽核與 provenance 核對。
