# 新對話交接：四色 boundary-state／constraint gadget 研究

更新：2026-09-13。工作目錄 `/home/ray/math`。**新對話先讀本文件，再依需要讀分階段報告；不要從零重跑已完成的搜尋。**

## 最新停止點：等待使用者整理數據

使用者要求「先到這」，本輪完成交接後 commit + push，研究暫停。
接手先讀 [討論表示法](state_language.md) → [可重驗觀察表](../artifacts/state_views/examples.md)
→ [局部封環研究](local_closure.md)。等待使用者提供整理後的數據或指定問題，
不要自動開新搜尋、擴充活動面 grammar、研究博弈策略，或繼續下方歷史 fan 5 工作。

目前可用：圖介面分離與完整關係替換的 Lean 證明、固定端點非交叉路徑的摘要定理與有限分類、
多起點分支／接合／預選／強迫的統一表示法，以及同一 C5 的具體觀察表。
一般移動前緣的充分幾何狀態仍未建立；State／Choice 是討論規格，不能當已實作的通用引擎。
所有 proved in Lean、computationally observed 與 conjectured 邊界見各文件。

本輪驗證已完成：`lake build`（新模組無 warning；既有 AttachmentOrder warnings）、
`lake env lean Math/LocalClosureAudit.lean`（輸出在 `artifacts/local_closure/lean-audit.txt`，
無 sorryAx／native 公理）、兩個 Python `--check`、文件連結與 `git diff --check`。
沒有待續的背景研究或待補的數學驗證；後續修改才需依範圍重驗。

重現入口：

```bash
python scripts/local_closure.py --check
python scripts/state_views.py --check
lake build
lake env lean Math/LocalClosureAudit.lean
```

可貼給接手者：

> 先讀 docs/HANDOFF.md 最新停止點、docs/state_language.md、artifacts/state_views/examples.md。
> 我正在整理數據，先使用既有表示法理解接下來提供的材料。研究目前暫停，不自動擴大枚舉、
> 開活動面 grammar 或博弈控制。染色完整關係與幾何合法性分開；Choice 是替代方案，join 是同時約束。

## 2026-09-13 討論表示法與觀察表

使用者要求先整理表述，方便討論多起點延伸、接合、預選分化與狀態強迫。
統一入口：[state_language.md](state_language.md)，採 `Interface / State / Branch / Choice` 四個物件，
以及 `condition / split / join / forget / query / compat / view` 七個動詞。
明確區分替代選擇 Choice、限制同時成立 join、已證等效才合併的 deduplicate。
這是表示法規格；一般幾何 State／Choice API 尚未實作，不能把候選摘要當已證充分狀態。

[狀態觀察表](../artifacts/state_views/examples.md) 可直接看完整色型、相容矩陣與條件強迫。
`python scripts/state_views.py --check` 以既有 loader 核對 catalog，重算七份狀態、四個接合格，
用全域色置換展開的 labeled rows 重驗交集、條件化與 query，逐 byte 比對文件。
本輪只有表示法文件與觀察表工具，沒有新圖搜尋／Lean 定理；幾何仍分別標示。

## 2026-09-13 局部封環與固定端點接線：第一輪

後續提問：週期／博弈式控制依使用者要求僅記為未來注意事項，見 `local_closure.md` §8，不啟動該研究線。

使用者提出施工邊界內凹、局部封環及有限狀態問題，授權開始研究。
新入口：[local_closure.md](local_closure.md)。原 fan 5 停止點保留為另一研究線，沒有開始 fan 6。

**proved in Lean（普通證明）：** `Math/LocalClosure.lean` 的實際 simple-graph 接合
`summary_glue`、任意 separated graph context 的 `replacement`、正確消去／空關係剪枝、
`relation_count` = $2^{4^k}$、degree-two path 色中性與 hub 的缺色條件。
`Math/LocalWiring.lean` 對 fixed-endpoint pairwise-conflict grammar 證明 forbidden-set
摘要更新封閉、全部未來 context 等價 iff 摘要相等，並實例化交錯 chord grammar。

**computationally observed：** 固定 3／4／5／6 個有序端點的非交叉路徑插入 grammar，
活 residual 1／3／11／45 類（含可達 dead：1／4／12／46）。全 support、轉移與 separator replay。
C4 wheel 封閉中心留下「不能用滿四色」，84→60 個賦色，但所有 pair projections 相同。
P=0–x–2、Q=1–y–3 與共同 T=0–z–2 的四份完整染色關係皆為 84；P+T 可同側，Q+T 有交錯／apex K5 subdivision 障礙。
具体圖著色、座標與 subdivision 檢查已完成；topology implication 未 Lean 化。

重現：`python scripts/local_closure.py --check`、`lake build`、
`lake env lean Math/LocalClosureAudit.lean`；artifact 在 `artifacts/local_closure/`。
**沒有主張**任意 disk patches 或移動前緣的幾何有限 signature。
下一個有意義的擴充是活動面上的 introduce／close／forget，先檢驗新增端點與面資訊的必要性；
不直接擴大枚舉，不把固定端點純插入模型當一般施工模型。

## 2026-09-12 Lean 補件：strip 圖語義與 residual 類數下界

新增 `Math/StripGraph.lean`（strip 圖、`Extendable`、附 `search_iff`／`verdict_iff` 正確性證明的回溯著色檢查器、
`residual_injective`）、`scripts/export_stepwise.py` → `Math/StepwiseGenerated.lean`（fan 4／5 代表字、
separator、轉移表；純資料、記錄 JSON SHA-256）、`Math/StepwiseReplay.lean`、`Math/StripGraphAudit.lean`。
**proved in Lean**：`fan4_nerode_lower_bound`／`fan5_nerode_lower_bound`——單列 fan 4／5 的真實可延伸語言
至少有 55／97 個右殘餘；全部 1485／4656 組 separator 由已驗證的檢查器重判，不信任 Python DFA。
`fan5_extendable_iff`：長度 $\le7$ 的全部 21,845 個字上，匯出表格的 live 等於 `Extendable`（有限一致性）。
四個重放定理用 `native_decide`；其餘為普通證明。負控制（竄改 separator／live）會失敗。
**沒有主張**：表格是殘餘自動機（上界）、signature 最小性、雙側 437 類、對齊循環證書的 Lean 實例化、
disk embedding。細節與信任邊界見 [研究文件 §9i](stepwise_state_sufficiency.md#9i-leanstrip-圖語義已驗證的著色檢查器與-residual-類數下界)。
重現：`python scripts/export_stepwise.py --check`、`lake build`、`lake env lean Math/StripGraphAudit.lean`
（審計輸出 `artifacts/stepwise/lean-strip-audit.txt`）。

## 歷史：2026-09-12 fan 5 接手入口（目前不自動續作）

**目前主線：fan 5 的雙側接合，不要開始 fan 6。** 先讀本節及下方雙側摘要，
再讀 [研究文件 §9h](stepwise_state_sufficiency.md#9h-fan-5-雙側接合437-個完整-residual成熟部分-25-類)。
單側最小 signature 的前置結果在 §9f–9g；命名與證明邊界在 §9d。

已完成的工作包括：修正獨立換色 quotient 的充分性判準、移除固定 window 檢驗的任意截止、
泛型 Lean 對齊／更新／pumping 定理、fan 4／5 完整單側分類，以及 fan 5 雙側 437 類最小化。
程式與 JSON 證書一併保存；先利用現有分類，不必重跑前六次歷史搜尋。

**接下來可直接做的研究**：把雙側的 425 種無限語言整理成可讀結構族。
其中成熟 A/A 對應的 24 種交替／奇偶語言已解釋，剩餘 401 種尚未完成結構命名。
從 `fan5_bilateral.json` 的 `classes` 開始：每類含 `left/right` 代表、
`left_delta/right_delta`、語言種類及長度 ≤4 真值向量。
`pair_to_class` 將左右組合映到類別；右側 ID 的意義查 `right_states`，
不能直接把右側 ID 當作單側 ID，應使用其 `reversed_word_class`。
候選結構 signature 應在完整 437 類上驗證雙向更新與類別一一對應，不能只拿樣本無碰撞當證明。

**不可遺失的約定**：沿指定方向首次遇色依序命名 b,c,d；左右框架需保留共同顏色對應。
437 是所有有限中央字（含空字）的固定色標分類；若只剩一洞，允許色集合只有 16 種。
各自換色 orbit、固定 gap 長度的輸出、完整 residual，是不同等價關係。
所有 strip 分類為 computationally observed；proved in Lean 的是泛型定理，加上（見上節）strip 圖語義
與 fan 4／5 的 residual 類數下界 55／97。尚無生成 DFA 的 Lean soundness（上界），也沒有 disk embedding 結論。

本輪可重現檢查（Python 只需標準庫；各 `--check` 重算並逐 byte 比對 artifact）：

```bash
python scripts/stepwise_aligned_reference.py --check
python scripts/stepwise_fan4_quotient.py --check
python scripts/stepwise_fan4_signatures.py --check
python scripts/stepwise_fan5_signatures.py --check
python scripts/stepwise_fan5_bilateral.py --check
python scripts/export_stepwise.py --check
lake build
lake env lean Math/StepwiseStateAudit.lean
lake env lean Math/StripGraphAudit.lean
```

Lean 公理審計輸出保存於 `artifacts/stepwise/lean-state-audit.txt`。
`run_repeat_loop`、`pumped_distinction` 不依賴公理；其餘僅列出標準 `Quot.sound`／`propext`。
上述檢查在本輪提交前重驗；未 push。

## 2026-09-12 fan 5 雙側接合完成第一輪

仍限 fan 5，沒有 fan 6。使用者問左右同時參照後授權開始。
**computationally observed**：K(L,R)={X | LXR 可著色} 的完整固定色標分類為 437 類，
由 97 個左 residual ×97 個右逆像集合的全部 9409 組最小化。
右集合與 reversed-R 的單側類有已驗證轉移雙射；左右需保留共同顏色對應。
細分計數 2→31→267→425→437→437；每類長度≤4 的341-bit向量皆不同，
149017 個 bit 全部獨立整圖 replay，另重驗9409組空字接合。
兩端局部更新均封閉且交換；一洞允許色投影有16種，不能把它當完整gap residual。
成熟 A/A 的1296組壓成25類：1128組無解，其餘為24種指定兩色交替＋長度奇偶語言。
一般437類中：空語言1，有限非空11（{ε} 加至多兩個允許色），無限425。
全部類與轉移已保存；一般425種無限語言尚未全部整理成可讀結構族。
左 cbaba、右 ababc／ababd 在各自框架都是 A_d/A_d，卻分別能填 b／任何gap都無解，
示範相對顏色對應不可省略。未新增Lean strip圖語義證明。
詳見 `docs/stepwise_state_sufficiency.md` §9h；`artifacts/stepwise/fan5_bilateral.json`。
重現：`python scripts/stepwise_fan5_bilateral.py --check`。

## 2026-09-12 fan 5 的 97 類完整解剖

使用者要求先完成 fan 5，**不要繼續 fan 6**。
**computationally observed**：97 個固定色標 residual classes =
E 1＋S 4＋P 12＋U_aba 12＋U_cba 24＋A 36＋F 6＋T 1＋dead 1。
配合指定首次遇色框架為 11 種 signature（含 dead）。
F 只保留允許再填一次的無序兩色集合 B，語言 `{ε} ∪ B`；T 的語言 `{ε}`。
四字 `baba`／`caba` 可與真實內部色域態合併；三字 `aba`／`cba` 必須保留為 U。
成熟 cut 用三色時全部是 T；只用兩色時為 A_cd/A_c/A_d。
與 fan 4 相比，多出的 42 個類全屬長度 3／4 的左端暫態，成熟活 signature 仍只有 A 三種及 T。
先前 `acaba`／`cbaba` 的碰撞解成 T／A_d；分類後不必每態都永久保留第四個邊界色。
全部 822 原始狀態的 3288 次結構更新通過；4656 對 separator 的 9312 端點獨立整圖 replay 通過。
未新增 Lean 圖語義證明。詳見 `docs/stepwise_state_sufficiency.md` §9g；
完整分類、cut 變體、轉移與最小性證書：`artifacts/stepwise/fan5_signatures.json`。
重現：`python scripts/stepwise_fan5_signatures.py --check`。

## 2026-09-12 fan 4 完整 signature → fan 5 collision

**computationally observed**：fan 4 完整最小化為 55 個固定色標 residual classes，
由外部首次遇色框架＋8 種 signature（含 dead）表示：E、S、P、A_cd、A_c、A_d、T、dead。
三字 `aba` 與成熟 `(aba,{c,d})` 合併；三字 `cba` 與成熟 `(aba,{c})` 合併，
所以「是否已引入內部點」不是必要狀態欄位。全部 1485 對都有 separator，兩端皆獨立整圖 replay。
移植同一結構 recipe 到 fan 5 自己的 cut，第一個等長 collision 是 `acba` / `dcba`，
同為虛擬 A_c，接 `b` 前收後拒；第一個成熟 collision 是 `acaba` / `cbaba`，
同為 A_d，接 `b` 前拒後收。遺失的是仍將進入下一 fan 的第四個邊界色。
尚未證明補這一欄已是 fan 5 最小表示，尚未接 Lean。
詳見 `docs/stepwise_state_sufficiency.md` §9f；完整分類、轉移、separator 與著色證書：
`artifacts/stepwise/fan4_signatures.json`；重現：
`python scripts/stepwise_fan4_signatures.py --check`。

## 2026-09-12 fan 4 對 fan 3 quotient 續作

**computationally observed**：最短等長成熟共同活歷史對為 `cbaba` / `cbcba`，
fan 3 完整 cut 同為 `(b,a,d)`，fan 4 接同一 `b` 分別接受／拒絕。
fan 4 的四狀態語義為 `(aba,{c,d})`、`(aba,{c})`、`(aba,{d})`、`(cba,{d})`；
最後一種目前可著色，但任何非空延伸都失敗，殘餘語言為 `{ε}`。
已對全部原始可達狀態驗證成熟 cut 分類與局部轉移，並獨立整圖 replay；未接 Lean。
詳見 `docs/stepwise_state_sufficiency.md` §9e；重現：
`python scripts/stepwise_fan4_quotient.py --check`。

## 2026-09-12 最新續作：對齊參照狀態（試跑七）

使用者已明確指定命名規則：固定方向後，以首次遇到其他顏色的次序命名 $b,c,d$，
$\mathrm{dist}(a,b)<\mathrm{dist}(a,c)<\mathrm{dist}(a,d)$。本輪 strip 方向是向已填歷史回看。
**命名規則不等於特徵摘要；反例否定某個摘要，不能宣稱這個命名本身抹掉 identity，或必須改指向別的 occurrence。**

最新有效結論見 [stepwise_state_sufficiency.md §9d–10](stepwise_state_sufficiency.md#9d-指定方向的對齊參照與局部更新試跑七)。
舊試跑六把殘餘關係各自除以換色，沒有保留與參照框架的對齊，故其「充分」結論需修正。
試跑七對狀態與共同後綴採同一框架；fan 3 已有短反例 $1210$ 與 $2010$，再填 2 時一拒一收，
雖然兩者都恰用 $a,b,c$。應保留的是 frontier 被迫為哪個相對色，而不只是是否被迫。

- **computationally observed（完整有限計算）**：六個形狀 $(3),(4),(2,3),(2,4),(2,2,3),(2,2,4)$
  的對齊殘餘自動機，穩態活狀態數 3、4、12、13、28、41；完整局部更新表已保存。
  狀態 = 顏色參照表＋對齊殘餘類，讀新色後 move-to-front 並同步換色殘餘類。
  全特徵池＋window 3 在三個埋藏 fan 3／深層形狀失敗，均有共同後綴和獨立整圖 replay。
- **computationally observed（完整有限計算）**：六個形狀都有共同循環證書排除任意固定 window。
  舊 `finite_range` 的截止 12 已改成迭代至空集或固定點。
- **proved in Lean**：`Math/StepwiseState.lean` 的泛型換色、register 更新與共同循環保持區分定理，普通證明；
  **尚未**把 Python 表格或 strip 圖語義接到 Lean。審計見 `Math/StepwiseStateAudit.lean`。
- **conjectured／未證**：一般深度的 $|Q|$ 無界與二次／指數成長。深度 $d\le3$ 的數據不能證明無界，
  也不能否定固定種類、內容可變的 registers。舊「任何固定容量都不夠」結論撤回。

入口：`scripts/stepwise_aligned_reference.py`、`artifacts/stepwise/aligned_reference.json`。
`python scripts/stepwise_aligned_reference.py --check` 重做全部新計算、獨立整圖 replay 並逐 byte 比對；
`lake build` 與 `lake env lean Math/StepwiseStateAudit.lean` 檢查形式部分。
下一步保持此命名，從對齊 transition 表反推每色應帶的 latent constraint 資訊，
再用完整 closure 驗證候選的局部更新；不再以樣本或獨立 residual orbit 判充分。

下方六次試跑是歷史記錄；涉及無界成長、單 bit 充分或命名抹掉 identity 的敘述以本節與 §9d–10 修正為準。

## 2026-09-12 最新：逐步填色的資訊充分性（前六次歷史記錄）

使用者提出的新研究問題與四次試跑結果都在 [stepwise_state_sufficiency.md](stepwise_state_sufficiency.md)：
第一部分（第 0–6 節）是問題陳述——把逐步四色填色看成決策樹，問哪些資訊足以判定「存在仍可成功的後繼」（Q1）
與「安全剪枝」（Q2），狀態表示 $S(H)$ 的充分性判準是「同狀態、可被 continuation 區分 ⇒ 不充分」；
第二部分（第 7–11 節）是試跑結果與目前能說的話。

| 試跑 | 檢驗場 | 主要結論 | 腳本 → `artifacts/stepwise/` |
|---|---|---|---|
| 一 | C5：87 個 fan-pentagon patch 為內部，同族 × 10 dihedral 對齊為外部，向前填 $b_0..b_4$ | 未填色歷史永遠可完成（4CT）⇒ 判準必須含已承諾顏色；Σ 的所有壓縮被反例否定；window 3 在深度 4 有 75% 接合圖不充分；$B_{in}\lor B_{out}$ 深度 3 抓不到任何死分支 | `stepwise_sufficiency.py` → `first_run.json` |
| 二 | 同上 | 死分支的局部認證：尾端 ≤2 色 0%、尾端 3 色 12.8%、加色數 78%（多為退化）；只靠 $\Sigma_{in}$ 就死 41.8% | `stepwise_local_fail.py` → `local_fail.json` |
| 三 | 同上，Nerode 不可區分 | window 外需 6／4／3 bits；pair 強迫狀態看不到色數；剩一點 5 個關係夠，剩兩點需完整條件投影關係 | `stepwise_window_state.py` → `window_state.json` |
| 四 | 無限長邊界的一段：平移生成 strip（fan 2／3／4） | fan 2 狀態為空；fan 3／4 只需一個 ± bit「剛封閉 fan 的內部頂點是否被強迫」，window 不需要 | `stepwise_strip.py` → `strip.json` |
| 五 | 同上但精確自動機（左端 + 平移不變、Moore 最小化），內部逐列加深，每列一個 fan 值 | 在 fan 列底下加自由列：類數不變；把 fan 列**埋在** $d$ 層自由列下：穩態 Nerode 類數隨 $d$ 成長（fan 3：2,5,9,14；fan 4：3,8,22,63）；沿邊界重複 $Hu^k$ transient+period ≤6 | `stepwise_strip_width.py` → `strip_width.json` |
| 六 | 同上 10 個形狀；候選 = 以 $a$ 為中心的 window + 其他顏色 $b,c,d$ 的**最近出現**（recency 命名）參照 | 任何有界 window 都不充分（精確）；淺層形狀由 2–4 個 run channel（顏色對 + 長度奇偶／精確到 4）決定；$(2,3)$、$(2,2,4)$ 類 nearest／recency 參照不夠，反例顯示參照必須保留遠端顏色 identity 且相關 occurrence 不一定是最近的——一般的遠端參照模型**未被否定** | `stepwise_remote_reference.py` → `remote_reference.json` |

`python scripts/check_stepwise.py --fast`（約 2 分鐘）重跑六個腳本並比對 40 個關鍵數字，目前全部一致；
不加 `--fast` 約 9 分鐘（多跑 $(2,2,2,3),(2,2,2,4),(2,2,3,3)$ 三個慢形狀，其結果已存在 JSON 裡）。
**全部 computationally observed，沒有 Lean 結果。**

第 3 節已改寫成 $S_n=(a_{n-1},a_n,a_{n+1},q_n)$、$q_n$ = 歷史對未來的 Myhill–Nerode 等價類，並加入使用者的兩點：
$a,b,c,d$ 是**四種顏色本身**、$b^\pm,c^\pm,d^\pm$ 不是三個 bit（$b^\pm$ = 顏色 $b$ 在 $\pm$ 方向上一個**相關的**、距離不限的 occurrence 參照，不預設是最近的），以及
「有限作用距離 ≠ 有限狀態」——要找的是有限記憶、無界傳播距離的規則。試跑六檢驗的是它的 nearest-occurrence 具體版本；下一個問題是「參照該指向哪個 occurrence、能否局部更新」。

目前能說的話（文件第 10 節）：判準的 $H$ 必須含顏色；閉環是 C5 退化的原因；約束列緊貼邊界時狀態是常數個 bit（內部頂點強迫狀態），
但約束列埋在自由列底下時狀態是 cut 上的聯合關係、類數隨深度成長——**任何固定容量的狀態對一般深度不充分**（否定「三 bit」讀法，不否定遠端顏色參照）；
沿邊界拉長的歷史在所有 strip 上都塌縮（有限記憶可跨任意距離），無界需求只來自向內加深；C5 上「必定 fail」多半是 meet 層級事實。
下一步候選（第 11 節）：C6–C8 patch 庫、strip 第一列 gadget 沿邊界混合（fan 2／3 週期）、$|Q(d)|$ 成長律（需狀態換色正規化才跑得動 $d\ge4$）、
外部也做成 strip 取乘積、允許 Kempe 換色、Lean 化（strip 自動機可接 `ColorDFA.lean`）。
待釐清 2、3（是否允許換色、$S$ 是否判合法性）未動。

## 2026-09-12 最新：pp-expression 層

使用者接續要求採用 CSP pp-definability 的下一步；已實作小型 JSON pp 公式，
以明確具名自由／存在變數與 EQ、NEQ、catalog 完整 relation 的原子合取求值。
見 [pp_relations.md](pp_relations.md) 與 `scripts/pp_relations.py`。
本輪以 R767 條件查詢、同 C5 投影、R91∩R935 及無解例子驗證；
`scripts/check_pp_relations.py` 的 106 個公式與七個不合法輸入案例通過。
結論是 **computationally observed**，沒有新增 pp 層的 Lean soundness 證明。
原子保留既有 graph／geometry witness 的來源與 hashes；合成幾何仍 unchecked。

公式、結果與獨立 replay 在 `artifacts/pp_relations/`。未重跑原始枚舉，未啟動
雙 C5／一般 transducer 搜尋或 topology completeness。下方「暫停並 commit + push」
是前一階段歷史停止點；使用者已要求將本輪 pp 變更 commit／push。接手先讀新 pp 文件，
再依需求讀下面原有 boundary relation 背景。

## 2026-09-12 新方向：五邊形內部與同一 C5 的條件強迫庫

使用者已啟動新研究：把內部 K3 換成五邊形 12345 加 13、14，結果見
[fan_pentagon.md](fan_pentagon.md)。完整 `2^25` grammar 的獨立 replay 已完成：
174,456 disk-accepted masks、87 exact Σ（含全部原 42、新增 45）；三色 profiles
仍是原 21 種，最少 2 且大小 2 仍相鄰。全 grammar 結論是 **computationally observed**。
新例子 `mask=1116616 / Σbits=767` 接受 216 個 labeled assignments，恰拒絕 01231
的全域換色；`Math/FanPentagon.lean` 有 exact Σ native 證書與普通局部衝突證明。

最新使用者 scope：**先做 generic boundary relation，但本輪只實作／驗證同一個 C5
boundary 上的 pair forcing；pairwise relation 必須由完整 boundary relation 投影得到，
不要反過來用 pair constraints 代表完整狀態。** 見 [boundary_relations.md](boundary_relations.md)。
`Math/BoundaryRelations.lean` 給泛型 full relation / condition / projection / nonvacuous forcing；
`Math/C5PairForcing.lean` 證 R767 與全體 proper C5 所有 pair projections 相同，卻有不同
conditional forcing。Python catalog 收錄 87 個完整 states 及 750 條派生最小條件推論，
來源、幾何 witness 與計算重驗分開保存。不啟動雙 C5 串接、一般 transducer 或任意 n 搜尋。

本輪驗證已完成：完整 `lake build` 通過（8800 jobs；只有既有 `AttachmentOrder` warnings）；
`Math/FanPentagonAudit.lean` 公理審計通過，無 `sorryAx`，實際輸出
`artifacts/fan_pentagon/lean-audit.txt`。泛型 relation 法則沒有 native 依賴；具體 C5
有限反例及 exact Σ 的 native 依賴已標明。Python 完整 grammar replay、211,410 個
條件 pair 查詢、3,828 對 aligned meet、實際 inside/outside union 染色皆通過。
搜尋四份核心輸出與 relation catalog 重建逐 byte 一致。驗證當時的 source／artifact hashes
保存在 `artifacts/boundary_relations/validation.json`；其中 `source_state` 記錄的是提交前的
驗證快照，並非要求工作樹維持未提交。

**本輪停止點：使用者要求先到這，整理交接後 commit + push。研究已暫停，沒有背景程序
或待完成驗證。** 新對話先讀本節、`docs/boundary_relations.md`、`docs/fan_pentagon.md`，
再看 `Math/BoundaryRelations.lean`、`Math/C5PairForcing.lean` 與
`scripts/boundary_relations.py`。先使用現有 catalog 查詢，不自動重跑完整搜尋。

若使用者要求繼續，接續主題是**同一個 C5 上的多條件強迫，以及真實內外 patches
如何共同實現條件**；保留完整 relation 作主狀態與具名 boundary 對齊。可從
R767 的 `b1=b4 ∧ b0≠b2 ⇒ b0=b3`、R91∩R935 才強迫 `b0=b2` 的例子開始。
下一個研究問題尚未指定；不自行啟動雙 C5 串接、一般 transducer、增加頂點搜尋，
也不自動切回先前的 topology completeness 工作。

接手所需操作與證據：

```bash
python scripts/c5_relation_library.py query 767 --given 'b1=b4' --given 'b0!=b2'
python scripts/c5_relation_library.py meet 91 935
```

* 完整 states 與派生規則：`artifacts/boundary_relations/library.json`。
* 真實內外合成圖：`artifacts/boundary_relations/inside_outside.json`。
* 全庫 query／meet replay：`artifacts/boundary_relations/replay.json`。
* 全 grammar 搜尋／重驗：`artifacts/fan_pentagon/summary.json`、`replay.json`。
* Lean 公理界線：`artifacts/fan_pentagon/lean-audit.txt`。

以下 topology completeness 段落是先前工作的停止點；本輪沒有補上 embedding → endpoint order。

## 先前停止點：triangle topology completeness（歷史背景）

先前已啟動 topology completeness，見 [topology_completeness.md](topology_completeness.md)：一般 triangle disk embedding → 分開共用端點 → 切開 annulus → 端點環序一致的紙上論證已落盤。`Math/AttachmentEndpoints.lean` 證明端點環序 → normal form → `AnnulusAccept` 的編譯接口；**沒有證明 embedding → 端點環序，完整 topology completeness 仍 unresolved in Lean**。若日後明確重啟此線，需獨立 embedding 模型與 Jordan／vertex-star splitting／spanning-arc cutting，不要把端點環序作為 embedding 定義或重做 grammar 分類。

**先前一輪的停止紀錄**：未啟動上述拓撲形式化。該輪完整 `lake build` 通過（8797 jobs；新檔無警告，既有 AttachmentOrder warnings 保留）；`lake env lean Math/AutomataAudit.lean` 通過，兩個新定理只有 `propext / Classical.choice / Quot.sound`，實際輸出在 `artifacts/automata/lean-audit.txt`。該輪未重跑枚舉。這不是本輪的接手指令。

## 30 秒摘要

已建立 Lean 的 exact boundary-coloring relation、有限枚舉、gadget relation algebra 與不信任 Python 的證書重驗流程。固定有序 C5 的 Σ 可以無損壓成十個 S4-orbit bits。

已找到 planar、induced-C5、11 頂點／26 邊的 BAD 圖，且 exact Σ 是全部 120 個四色 boundary assignments。但 C5 是 separating cycle，**不是 disk 外邊界**。

目前方向已從擴大 n 的盲目枚舉，改為 primitive exclusion gadgets → relation library → 反向合成 T4 → 研究幾何接線障礙。最新確認：**即使完整 Σ 相同，接上同一 context 的 disk 合法性仍可能不同**。因此 geometry-aware transition 不能只依賴 Σ。

最新階段 **Finite-state synthesis of triangle disk gadgets**（[automata.md](automata.md)）：在固定 triangle grammar 上，染色與幾何都有沿邊界掃描的有限狀態表示。`ColorDFA` 的 exact Σ 語意對每個 attachment word 都是普通 Lean 證明；`GeometryDFA` 只主張 forward soundness（接受 ⇒ 自建 rotation system 通過 Euler／face checker），其 completeness 仍是 topology gap。Nerode 狀態數、42 個 disk states、1,080 個 T4 ordered realizations、Z5 profile 統計皆為 computationally observed，且只限此 grammar。

2026-09-12 最新：attachment geometry 的 cut-necklace normal form 已雙向 Lean 封口；本輪又完成 **incidence 六種 regime 與飽和分支的 cyclic normal form**。`Math/AttachmentSignature.lean` 證 `(E,X,Z)`（shared junction／singleton／空 boundary 數）只可能是 `(1,4,0),(2,2,1),(2,3,0),(3,0,2),(3,1,1),(3,2,0)`。`A=8` 當且僅當 `(E,X,Z)=(3,2,0)`。

`Math/AttachmentSaturated.lean` 普通證明：三種 junction 都出現、各 packet 非空且 Nodup 時，one-turn ⇔ cyclic word 為 `01 · [1]^y · 12 · [2]^z · 20 · [0]^x`。這個 list theorem 不限制 boundary 長度；C5 飽和時再得到 `x+y+z=2`。因此 degree 型 `(4,2,2)`／`(2,3,3)` 的 singleton 配置與環序都已從幾何推得。**續作 `Math/AttachmentGaps.lean` 已完成三 junction 含空 boundary 的雙向環序：`01 · U · 12 · V · 20 · W`，三段各只允許空 packet 或 singleton 1／2／0，保留原空位。C5 時三段總長為 2，singleton 數加空位數為 2。一／兩 junction 的三個 regimes 也已由下段 AttachmentOrder 涵蓋；GeoReject bridge 現已完成（見下段），不要重做環序分支。**

`Math/AttachmentOrder.lean` 已完成一／兩 junction 的三個 regimes（**proved in Lean**）：`one_junction_normalForm` 給出 `(1,4,0)` 的 C5 形式；`two_junction_cyclic_gaps` 與 `two_junction_gap_inventory` 涵蓋 `(2,2,1)`、`(2,3,0)`，保留空 boundary 位置。六種 incidence regimes 的參數化環序均已涵蓋，後續 GeoReject bridge 現已完成（見下段），不要重做環序分支。

**2026-09-12 最新 bridge 已完成（proved in Lean）**：`Math/GeoRejectBridge.lean` 從 normal form 的 fan ≤ 2、共同鄰居 ≤ 1 與 attachment budget 推出 `runOK_rejection_le_three`。`runOK_three_rejection_structure` 證 `|R|=3` 時 degree 型為 `(2,3,3)`，degree 2 的鄰居為 `{t,t+1}`，`R={t+2,t+3,t+4}`。`normalForm_rejection_bound` 直接以 `AttachmentNormalForm` 為前提。另證 `runOK_profile_ge_two` 與 `runOK_two_profile_adjacent`。不需展開十二類 shape、不枚舉 words，也不引用 native profile 檢查。十二類窮盡性仍是 computationally observed，topology completeness 仍 unresolved。詳見 [attachment_normal_form.md](attachment_normal_form.md)。

2026-09-12 bridge 驗證：完整 `lake build` 通過（8796 jobs；新檔無警告，既有 `AttachmentOrder` linter warnings 保留）。`lake env lean Math/AutomataAudit.lean` 通過；新增 12 個定理的公理依賴均為 `propext / Classical.choice / Quot.sound`，沒有 `sorryAx` 或 native 依賴。實際輸出已更新至 `artifacts/automata/lean-audit.txt`。沒有重跑 word 枚舉或 topology 診斷。

## 1. 使用者要求與禁止事項

2026-09-12 新增研究想法（僅記錄、尚未啟動）：[以額外內部點轉接成 C5 interface](c5_interface_idea.md)。研究 C6／C7 是否在指定 continuation grammar 下可經單一 C5 保持語義；區分可逆編碼的十-orbit 容量限制與一般關係式編碼，後者不能僅因來源狀態超過十個就否定。另記錄五點投影漏掉六點染色 obstruction 的診斷例。此想法不取代既定 normal form → GeoReject 工作順序。

核心問題：是否存在小的、composition-preserving boundary quotient，能描述 relevant planar patches；之後才研究 transition system 的 closed SCC。

* 目前研究順序：先刻畫 attachment geometry 的 normal form，再讓 `GeoReject` 成為 corollary；不要把觀察到的十二類當成證明前提。
* 不直接證四色定理，不以四色定理作搜尋 oracle，不假設 boundary-state conjecture。
* 每個找到的候選保留 deterministic certificate；Lean 重算 graph／boundary／coloring claims，不能信任 Python 的 BAD 結論。
* 區分「平面圖中指定 C5」與「C5 是單側 disk 外邊界」。前者可 BAD，不可偷換成後者的反例。
* 區分已證與計算觀察；不可把有限搜尋無反例外推為一般定理。
* 先做 document-first。除非使用者明確 `/graphify`，或文件無法解釋跨檔架構，不自動跑 Graphify。
* 未獲要求不開 sub-agents、不 commit／push。專案已納入 Git；每輪先檢查實際 `git status`，不要沿用早期「全部 untracked」的歷史狀態，也不可將研究產物視為可刪的臨時檔。

## 2. 信任分類

| 標籤 | 專案中的確切意義 |
| --- | --- |
| proved in Lean | 具名 theorem，沒有 `sorry`、`admit`、手寫四色／boundary 猜想公理。多數有限計算用 `native_decide`，額外信任 native compiler 及生成的計算公理。 |
| computationally observed | Python 枚舉完整性、NetworkX planarity／cofacial 測試、搜尋最小性、拓撲診斷。標準拓撲定理提供解釋，但未因此成為本專案的 Lean theorem。 |
| conjectured / unresolved | geometry signature 的充分性、一般接線 grammar、有限 frontier／closure、尚未定義的 closed SCC。不能作為前提。 |

`#print axioms` 的實際輸出放在各 artifact 目錄的 `lean-audit.txt`。此工具鏈產生 `..._native.native_decide.ax_1_1` 等依賴，不能把 native 決定程序說成純 kernel reduction。

五份三角形 pigeonhole 局部衝突證書用 `decide +kernel`；一般 pigeonhole lemma 是普通證明。這不表示全部染色證書都是純 kernel 計算。

## 3. 基本定義與已完成的有限計算

`Color := Fin 4`；有序 boundary 用 injection。一般 restriction-image 定義為 `SigmaAt`，五邊界版為 `Sigma`：所有能延伸成完整 proper coloring 的 boundary assignments。

```text
GOOD := Σ 中存在使用至多三色的 coloring
BAD  := Σ 非空，且不存在使用至多三色的 coloring
T4   := proper C5 assignments 中恰好使用四色者
```

Lean 枚舉結果：

* C5 proper 4-colorings：240；三色 120，四色 120。
* S4 color orbits：10；再允許 D5 位置作用：2。
* 十個 canonical reps：`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。
* 兩個 S4×D5 reps：`01012 01023`；這是 **coloring 類**，不是只有兩個 patch states。
* 固定 boundary labels、無預染色／外加 list constraints 時，Σ 是 S4-saturated。十-bit encoding 無損且保持 intersection，全部可能 bitsets 的上界是 1024；不宣稱全部可實現。
* 原始 240-bit mask 的 bit i 是 proper tuples 的 lexicographic order，第 0 bit 為最低位；`artifacts/boundary/summary.json` 有完整 raw order。

當兩塊內部不相交、只共享同一個有序 boundary：`Σ(union)=Σ1∩Σ2`。另有 relational composition `∃y, R1(x,y)∧R2(y,z)`、隱藏 terminals、結合律、S4-equivariance。

獨立 D5 canonicalization 不能省略 relative alignment。已有更強反例：`C5+02` 與 `C5+03` 的整個 Σ 互為 reflection，接固定 context `C5+03+13` 後，一個 BAD、一個 GOOD。

## 4. 已完成的圖搜尋與構造

### 第一階段：n=5,6

全部 1,056 個 labeled C5-supergraphs；883 個 planar，250 個 BAD；250 份候選全由 Lean 重驗。最小 `(n,m)` 是 `(5,8)`，含 boundary K4，Σ 有 48 個 coloring。不是 disk patch。

同面測試通過的 223 張圖沒有 BAD；這只涵蓋 n≤6。

### Induced-C5 搜尋

n=5..9 的 planar edge bound 內候選數分別為：

```text
1, 32, 2,047, 258,096, 61,450,327
```

未找到 planar BAD。**n=10 沒有窮舉**。不能宣稱 11 是全域最小頂點數。搜尋是 computationally observed，不是 Lean 的有界完備性定理。

### 11 頂點構造

兩個 8-vertex disk patches 沿完整 C5 黏合，得到 separating-C5 planar BAD。最初 27 邊，刪 `08` 後為 26 邊，Σ 恰為 T4，120 個 coloring。

刪任一 interior vertex／非 boundary 邊不能保持 BAD；這是 deletion-minimal，不是全域 minimum。保留 induced C5 的單邊 contraction 也未給更小 BAD。

資料：`artifacts/construction/`；圖與兩側接線見 [construction.md](construction.md)。`ConstructedAnalysis.minimal_sigma_exact` 等 theorem 連到語意 Σ。

## 5. 目前的 gadget synthesis

Primitive 已驗證：NEQ、以 K5−xy 實現 EQ、K4 frame 排色與強迫第四色。Frame 是相對顏色座標，不是固定紅藍綠黃。共用 frame 與各自隱藏獨立 frame 是不同接線規格：前者可強迫 x=y，後者可接受任何 x,y。

有限 grammar：`有序 induced C5 + 一個內部 K3 + 任意 boundary-to-K3 edges`。

| 項目 | 結果 |
| --- | ---: |
| 接線子集 | 32,768 |
| disk 必要邊數上界內 | 22,819 |
| disk 測試通過 | 7,194 |
| 不同 exact labeled Σ | 42 |
| 單一 component 的 exact T4 | 0 |
| unordered state pairs，含自配對 | 903 |
| intersection 恰為 T4 的 state pairs | 10 |

42 個 state 各保存一個最省邊實現，全部有 Lean exact-relation certificate。十個目標各有完整 graph certificate：五個 26 邊、五個 27 邊，全部 11 頂點、Σ=T4、planar 但 C5 不 cofacial。

最少 26 邊僅限此二元 grammar 的 target synthesis。**幾何測試只涵蓋選出的 state witnesses；未枚舉同 Σ 的全部實現。** 不可將只存最便宜 Σ witness 的優化，未經證明地套用到未來的 disk admissibility 搜尋。

最新決定性最小解的三色模式：

```text
L 接受：01021, 01201
R 接受：01012, 01202, 01212
兩者都接受全部五類四色模式。
```

五份排除證書解釋為「三個相鄰頂點只剩兩色」或「兩個相鄰頂點只剩同一色」。詳見 [gadgets.md](gadgets.md) 及 `artifacts/gadgets/explanation.json`。

`TriangleConstraints.compiled_meaning` 原本只以 `native_decide` 檢查 `leftLinks`／`rightLinks`；`ColorDFA.mem_sigma_triangle` 現在對所有 links 給出普通證明，前者保留為歷史檢查。

**不要混淆兩份 26 邊圖的編號**：`artifacts/construction/minimized.jsonl` 是較早構造；`artifacts/gadgets/bad_certificates.jsonl` 第一行是最新合成解。兩者 exact Σ 都是 T4，但邊集／兩側三色 reps 不同；下節路徑指的是後者。

## 6. 最新進展：非法接線的必要障礙（尚未 Lean 化）

這部分原本只有對話內 read-only 診斷，本交接首次集中落盤。2026-09-11 整理時重新執行確認。**本節的拒絕端證書沒有 Lean topology checker 或 JSON topology certificate。** 接受端（triangle grammar 內的 disk certificate）已於 §7.1 落地，兩者不可混淆。

### 6.1 交錯端點迫使兩塊分居兩側

最新第一張合成圖有兩條完全頂點不相交的路徑：

```text
P = 0–5–2
Q = 1–10–3
boundary order = 0,1,2,3,4
```

端點交錯，因此不能同時嵌入同一側 disk。這是 Jordan separation／cycle-bridge interlacement 障礙，不依賴四色定理。它提供非法的充分證書，也就是合法單側接線的必要排除條件；沒有證明沒有此障礙就一定合法。

十張 target 全有上述形式的證書。依 JSONL 行序 0..9：

| 行 | 0 到 2 的路徑 | 1 到 3 的路徑 |
| --- | --- | --- |
| 0 | 0–5–2 | 1–10–3 |
| 1 | 0–5–6–2 | 1–8–9–3 |
| 2 | 0–5–6–2 | 1–8–10–3 |
| 3 | 0–5–6–2 | 1–8–10–3 |
| 4 | 0–5–2 | 1–10–3 |
| 5 | 0–5–2 | 1–10–3 |
| 6 | 0–5–2 | 1–8–10–3 |
| 7 | 0–5–6–2 | 1–10–3 |
| 8 | 0–5–6–2 | 1–8–10–3 |
| 9 | 0–5–6–2 | 1–8–10–3 |

### 6.2 完整 Σ 也不能決定 disk 接線合法性

取同一個 ordered C5：

```text
P = C5
Q = C5 + {s0,s1,s2}
R = C5 + {t0,t1,t2}，s、t 是不同 interior vertices
```

P、Q、R 各自是 disk patches，Σ 全是 240 個 proper C5 assignments。因為每個 star center 只需避開三個鄰居的顏色，總能選到剩餘色。

但 P∪R 是 disk patch，Q∪R 不是；Q∪R 仍 planar、Σ 仍為全部 240 個。

拓撲原因：若 Q∪R 可以放在 disk 裡，就能在外側加 apex z 鄰接全部 boundary，產生 K3,3 子圖，兩側為 `{s,t,z}` 與 `{0,1,2}`。所以這兩塊不能同側。

這不是 color quotient 壓縮失誤：**即使沒有壓縮，Σ 也未包含此幾何觀察。** 該例可作下一階段 topology-aware congruence 的最小測試之一；尚未證其最小性。

### 6.3 Primitive 的 port 障礙

EQ 圖 K5−xy 自身 planar，但 x,y 不可能同面；若同面便能加 xy 得 K5。K4 frame 的四個 reference ports 也不能同面（加共同 apex 得 K5）。

這些是具體實現的限制，**沒有證明所有 EQ gadget 都不能有同面 ports**。

拓撲背景來源：[MIT：Some Graph Theory，§14.3](https://math.mit.edu/~djk/18.310/Lecture-Notes/some_graph_theory_2007.html)。該引用不是 Lean axiom，也不是搜尋剪枝中的四色定理。

## 7. 建議續作順序

### 7.1 已完成：geometry DFA 作為 topology-certificate 候選（2026-09-11）

在 triangle grammar 內，接受端 certificate 已落地：`GeometryDFA.rotationOf` 從 winding sequence 決定性產生 rotation system，`checkRotation` 驗證鄰居表、每個連通分量 `V − E + F = 2`、C5 為一個 face；`accepted_masks_have_rotation` 以 `native_decide` 對 32,768 個 mask 全部確認，`accept_certificate` 是其 `AnnulusAccept → ∃ run, checker = true` 形式。

* **forward soundness 可形式化**：上述已在 Lean 內。「球面 rotation system 且 C5 facial ⇒ disk embedding」是標準組合拓撲背景，未在 Lean 內證明，與 §6 的 Jordan 障礙同屬 topology 信任範圍。
* **completeness 尚未證明**：自動機拒絕 ⇒ 不存在 disk embedding，沒有證明。
* **`7194 = apex test` 僅為完整有限枚舉觀察**：`accepted_count = 7194`（Lean）與 `scripts/check_automata.py` 的 NetworkX apex-planarity 逐字一致，不因此提升為定理。

§6 的路徑交錯／K3,3 證書仍是 grammar 外的拒絕端證據，尚未 Lean 化。

### 7.2 未開始

1. 把第 6 節路徑／三共同 attachment 證書整理為 deterministic topology-certificate 資料，先讓 Lean 驗證有限組合事實：端點順序、真實邊、內部互不相交、K3,3 模型。
2. 明確定義 disk embedding 或組合 rotation-system 模型，再處理「證書 ⇒ 不能單側」的拓撲 soundness；不能用一個假定的 bridge-conflict 定理把缺口藏起來。
3. 形式化 P/Q/R 同 Σ、不同 context 幾何合法性的例子。染色證明很小，拓撲部分要另列信任範圍。
4. 候選 signature 為 `(Σ, attachments/循環順序, 側別約束或可行 embedding 集合)`；測試 composition congruence，先找反例，不先假設充分。
5. 有明確合法 transition grammar 之後，才研究 closure、有限 frontier 與 SCC。

可先對 bridges 配置 `side∈{inside,outside}`，以交錯／共同 attachment 證書加入 `side_i≠side_j`。這是必要條件方向，不能無條件當作完整判準。

純 intersection transition 已在 `State.lean` 證明單調縮小、互相可達的 exact states 必相同。它不能把 BAD 修成 GOOD（可能縮成 empty），也沒有自動證明哪些 singleton SCC 是 closed。

### 7.3 Z5 現象（觀察，不先當 theorem）

三色 canonical patterns 由唯一色頂點位置索引成 `Z5`（`01012↦4, 01021↦3, 01201↦2, 01202↦1, 01212↦0`）。在 triangle grammar 的 7,194 個 disk-accepted words 上：

* 32 種三色 acceptance subset 實現 21 種；empty 與 singleton 都沒有出現；
* size = 2 只有五個相鄰對 `{t_i, t_{i+1}}`，各 6 個 mask；size ≥ 3 全部實現；
* 十組 T4 target pairs 恰是兩個不相交的實現 profile（5 組相鄰對×相鄰對、5 組相鄰對×補集三元組）。

`GeometryDFA.z5_profiles_checked` 是此 grammar 內的 `native_decide` 檢查，不是 disk patch 的 lemma。

**里程碑「Colour semantics closed」已達成**（`Math/HallTriangle.lean`）：`k3_uncolorable_iff`（Mathlib Hall）→ `reject_iff_hall`：pattern 留有未用色 `d` 時，`¬ Accept (run w b) ↔ PairPinnedToFourth ∨ TripleRestrictedToTwo`，全是普通證明；`regression_guard` 與 `check_automata.py` 只是對 32,768 words 的 regression guard。染色側封口。（`winding ⇒ block` 已於下段證出。）**不要**以「boundary 鄰居是 C5 interval、兩兩交集 ≤ 1」為 geometry lemma 的 statement——這在 1,350 個 accepted words 上是假的（兩內部頂點可共享兩個 boundary 頂點，鄰居集可跳過未接線頂點）；要從 winding 給的「已接線頂點環序上的 block」出發。目標敘述：|R| ≤ 3，且 |R| = 3 只在 degree 型 (2,3,3)、R 為 cyclic 3-interval（目前為觀察；R 現在可寫成 `{u | GeoReject w u}`）。

**2026-09-11 續：`winding ⇒ block` 已證**（`Math/AttachmentBlock.lean`，普通證明，無 native_decide）。`runOK_iff_blocks`：`RunOK w ρ ↔` 弦的三角形位置沿 C5 環讀是某個旋轉下的 `replicate a 0 ++ replicate b 1 ++ replicate c 2`（完整刻畫）。`attachment_block`：`RunOK`、`k ∈ w i`、`k ∈ w j` 時，`i→j` 或 `j→i` 開弧上所有 `m` 都有 `w m ⊆ {k}`。工具是 `stepSum_le_of_sublist`（環和對 sublist 單調）。接著 `Math/GeometryWitness.lean` 把 Hall witness 去色：`GeoReject w u`（只用 `linksOf w k` 是否命中 `u`、`{u+1,u+3}`、`{u+2,u+4}`），`reject_iff_geometry : ¬ Accept (run w b) ↔ GeoReject w u`（任何三色形狀的 b），`threeProfile_eq_geo : threeProfile w = univ.filter (¬ GeoReject w ·)`。**下一步就是 bridge**：從 `RunOK w ρ`（用 `attachment_block`／`runOK_iff_blocks`）證 `#{u | GeoReject w u} ≤ 3` 與 3-interval，兩側都已是純幾何敘述；不要再回頭做 enumeration。

§7.3 的 bridge 最新進度（2026-09-11 續）：`runOK_large_rejection_cases` 已把未封口部分縮到上述四種 degree 型；低 degree 分支由 `runOK_rejection_le_two_of_low_degree` 完成。證明沿用 `stepSum_le_of_sublist`，三個共同鄰居會提供六弦、至少 winding 6 的局部障礙；fan excess 的步數預算給出總 attachment ≤ 8。沒有枚舉 words，沒有使用既有 `z5_profiles_checked` 證明新結論。不要重新做低 degree 分支；最新工作順序已改為先 normal form 幾何分型，再推四型的拒絕 corollary，見下段。完整 bridge 與 topology completeness 仍未證。

**2026-09-11 normal form 續作**：`annulusAccept_iff_normalForm` 與 nondegenerate 版本已證；singleton／shared-junction incidence 公式、pair 唯一性、min-degree ≥ 2 時共同鄰居 ≤ 1 已證。`geoReject_iff_pair_or_opposite` 是第一個以該幾何層為前提的拒絕 corollary。所有新主要定理無 native 依賴。具體參數、雙向證法、具名定理與未解邊界見 [attachment_normal_form.md](attachment_normal_form.md)。

**2026-09-12 bridge 封口**：上述 §7.3 的「下一步」與未封口敘述是歷史進度。現在 `GeoRejectBridge.lean` 已證完整 bound、等號 degree／cyclic interval 結構與 profile corollaries。證明只需 normal form 的 incidence corollaries，未逐型展開環序；一般 disk completeness 與 grammar 外 topology soundness 仍未證。

## 8. 檔案導航

| 檔案 | 接手時看什麼 |
| --- | --- |
| `Math/Boundary.lean`, `Enumeration.lean` | 基本語意、S4／D5、240→10→2 |
| `Math/State.lean` | exact 壓縮、intersection、SCC 限制 |
| `Math/Certificates.lean`, `GeneratedCertificates.lean` | 最早最小 BAD 與 250 份證書 |
| `Math/SplitCertificate.lean` | `edgeCheck_exact`, `splitSigma_exact`；GOOD／BAD／empty 的 exact-relation checker 與 BAD checker |
| `Math/Constructed*.lean` | 較早 11-vertex 構造及 exact T4 |
| `Math/GadgetRelations.lean`, `PrimitiveGadgets.lean` | relation algebra、frame 與 EQ/NEQ 規格 |
| `Math/TriangleConstraints.lean` | pigeonhole 證書、constraints-to-graph 的兩個具體 component 檢查 |
| `Math/GadgetLibrary.lean`, `GadgetTargets.lean`, `GadgetSynthesis.lean` | 42 library witnesses、10 target witnesses、`all_targets_exact` |
| `Math/ColorDFA.lean` | 染色自動機：state invariant、`mem_sigma_triangle`、`splitSigma_triangle`、`acceptedReps_exact`、mask 枚舉 |
| `Math/GeometryDFA.lean` | annulus 自動機、`rotationOf`、`checkRotation`、`accept_certificate`、`accepted_count`、`z5_profiles_checked` |
| `Math/HallTriangle.lean` | `k3_uncolorable_iff`、`reject_iff_hall`、`not_mem_sigma_iff_hall`、具名 witness、regression guard |
| `Math/AttachmentBlock.lean` | `stepSum_le_of_sublist`、`stepSum_mem_iff_blocks`、`runOK_iff_blocks`、`attachment_block`：winding ⇒ block 的普通證明 |
| `Math/GeometryWitness.lean` | `GeoReject`、`reject_iff_geometry`、`threeProfile_eq_geo`：Hall witness 去色，profile 變成 `linksOf` 敘述 |
| `Math/AttachmentBudget.lean` | fan excess ≤ winding、總 attachment ≤ 8、共同 boundary 鄰居 ≤ 2；無 native |
| `Math/GeometryProfile.lean` | 低 degree 時 `|R| ≤ 2`、profile ≥ 3，以及 `|R| ≥ 3` 的四種 degree 型 reduction；無 native |
| `Math/AttachmentNormalForm.lean` | cut-necklace normal form 雙向等價、packet alphabet／junction 唯一性、degree incidence、min-degree ≥ 2 的交集界 ≤ 1；不 import Hall |
| `Math/NormalFormHall.lean` | normal form ⇒ 排除兩個涉及 unique 位置的 triple Hall witnesses |
| `Math/GeoRejectBridge.lean` | 完整 `|R|≤3`、等號 `(2,3,3)` 與 cyclic 3-interval、profile ≥ 2 與等號相鄰對 |
| `Math/AttachmentEndpoints.lean` | 任意 Nodup endpoint packets 加三-block 環序 → normal form → AnnulusAccept；不含拓撲抽取證明 |
| `Math/AttachmentSignature.lean` | packet inventory、六種 incidence regimes、飽和時三 junction 加兩 singleton、兩種 degree 型 |
| `Math/AttachmentGaps.lean` | 三 junction 含空位的雙向 gap normal form；C5 gap 長度與 empty／singleton inventory |
| `Math/AttachmentSaturated.lean` | 三 junction 的 cyclic order、constant gaps、雙向 normal form，以及 C5 飽和時 x+y+z=2 |
| `Math/AttachmentOrder.lean` | 一／兩 junction 的 ordered gaps 雙向 list 定理；一 junction 的 C5 形式、兩 junction 的環序與 empty／singleton inventory |
| `Math/AutomataReplay.lean`, `AutomataAudit.lean` | 42 份 library 證書對自動機的 replay；`#print axioms` |
| `docs/phase1.md`, `construction.md`, `gadgets.md`, `automata.md` | 各階段詳細範圍與結果 |

一般 graph-wiring compiler 的 planar soundness **尚未建立**；不要把 relation 結合律當成 graph embedding 的接線定理。

## 9. 重現與工程注意事項

Lean／mathlib 鎖定 `v4.34.0-rc2`，使用既有 `lake-manifest.json`；不要為接手任務自動 `lake update`。Python 用 `uv run --with networkx==3.5`，不依賴系統 Python 已裝 NetworkX。

```bash
lake build
uv run --with networkx==3.5 python scripts/check_search.py
uv run --with networkx==3.5 python scripts/check_construction.py
uv run --with networkx==3.5 python scripts/check_gadgets.py
lake env lean Math/GadgetAudit.lean
uv run --with networkx==3.5 python scripts/triangle_automata.py
uv run --with networkx==3.5 python scripts/check_automata.py
lake env lean Math/AutomataAudit.lean
```

`triangle_automata.py` 會覆寫 `artifacts/automata/`（含 `nerode_*.json` 的 prefix→class mapping 與未最小化 product states）；兩次執行逐 byte 一致。`Math/GeometryDFA.lean` 的三個 `native_decide` 約需 3–4 分鐘，`HallTriangle.regression_guard` 約 2.5 分鐘。

重建最新合成資料（會覆寫其自己的 generated artifacts）：

```bash
uv run --with networkx==3.5 python scripts/synthesize_gadgets.py
python3 scripts/export_certificates.py --split --relation --namespace FiveBoundary.GadgetLibrary --input artifacts/gadgets/library.jsonl --output Math/GadgetLibrary.lean
python3 scripts/export_certificates.py --split --namespace FiveBoundary.GadgetTargets --input artifacts/gadgets/bad_certificates.jsonl --output Math/GadgetTargets.lean
```

需要只讀拓撲診斷時，可從 JSONL 建圖，分別在 induced subgraphs `{0,2,5,6,7}` 與 `{1,3,8,9,10}` 找 0→2、1→3 路徑，再驗證兩條路徑的 vertex sets 不相交。第 6 節逐行表就是重新執行所得。

性能注意：**不要讓 `native_decide` 枚舉 `Fin 5 → Finset (Fin 3)` 這類 Pi 型別的 `Finset.univ`**（32,768 個函數要數分鐘以上）；改用 `ColorDFA.wordOfMask : ℕ → Word` 對 `Fin 32768` 枚舉，`wordOfMask_surjective`／`wordOfMask_bijective` 已證，可把 mask 結論搬回 `∀ w`。同理 `Accept` 的 `Fin 3 → Color` 枚舉在熱迴圈中用 `acceptB`（`acceptB_iff`）。閉包內的 `let` 若依賴外層參數，會在每次呼叫重算——`rotationOf` 先物化 `rotationTable` 再回傳閉包。

避免直接建立 4^(5+k) 個完整 coloring 的大 Finset；使用已證等價的 split-interior checker。若在 `∀ b` 中重複計算同一 `splitSigma`，應先 `let actual := ...`。要檢查少數 Links 時用 `List.all`，不要透過 `∀ links ∈ list` 讓 native 決定程序枚舉整個 Links 型別。不要同時啟動會寫同一個 `.olean` 的多個 `lake build`。

## 歷史：較早的 C5 catalog 起始訊息（最新入口見文件頂端）

> 請先讀 `/home/ray/math/docs/HANDOFF.md` 最上方最新停止點、`docs/boundary_relations.md` 與 `docs/fan_pentagon.md`。目前已完成內部五邊形加 13、14 的完整搜尋：87 個 exact Σ（原 K3 是 42），以及 generic full boundary relation 和同一有序 C5 上的條件 pair forcing 庫。完整 relation 是唯一主狀態，先套用共同條件、再投影；不得反過來用 pair constraints 代表完整狀態。750 條條件規則、211,410 個 pair 查詢與 3,828 個 aligned meet 已獨立重驗；Lean 已證泛型法則及 pair projections 相同但 conditional forcing 不同的具體反例。普通證明、native finite checks、外部計算／幾何證據分開標示。入口是 `Math/BoundaryRelations.lean`、`Math/C5PairForcing.lean`、`scripts/boundary_relations.py` 和 `scripts/c5_relation_library.py`。使用者要求先暫停並 commit + push，沒有待完成驗證或背景程序。先使用既有 catalog，不自動重跑枚舉；下一個研究問題尚未指定，不自動開雙 C5 串接、一般 transducer、更多頂點搜尋或重啟歷史 topology completeness 工作。
