# D₆ 項 5、6 的獨立來源範圍及歷史核對

以下判斷以目前工作區原文的固定快照為準；未執行任何 producer，也未 import 被稽核 checker。
新增依賴先保存於 [dependency_manifest_start.json](dependency_manifest_start.json)，
末次核對另存 `dependency_manifest_end.json`。本檔不代表項 1–3 的獨立驗收。

## 項 5：確認，精確限於 C §1 的來源分支

[原 C 報告](../../../docs/c5_mixed_p3_common_endpoint.md) §1，行 43–77，
要求 finite simple induced-C5 disk、q=01012、非框邊逐邊 q-critical、H 連通、
相鄰 degree-5 roots、其他內點 degree 四、唯一 mixed 原分量為三點路徑，
兩個 roots 都只接 x₂。沒有 Σ=933／941、恰缺兩列、T4 或 target 拒絕的前提。
反向 (3,0,0) 只是同一完整圖的路徑座標反轉，不擴充至其他 incidence 型。

先重新推導容量所需的初等事實。對一份 unary D，未固定 root 時其 lists
至少是原內 degree 加一份 contact slack；以 contact 作最後染色點、逆生成樹
貪婪染色，得到至少一份整分量染色。完整禁色 f_D 是所有 contact tuple
色集合的交集，故 |f_D|≤n_D。逐邊 criticality 迫每份 f_D 非空且有同側
其他分量不禁的私有色；spoke 顏色互異，而且避開各 f_D。
因 zw 及 mixed contact 已用兩份 degree，剩餘至多三份 unary incidences；
兩份相交且各有私有色的 f_D 各至少二色，需要至少四 incidences，故不可能。
因此一側所有禁色來源互斥，得到 |E_r|=1+D_r，D_r∈{0,1}。
這些是重新證明的初等容量／criticality 論證，不借用完整 Σ 或 Gallai。

原 P₃ 的 lists 大小至少 (1,2,3)，固定兩個 root 後至少 (1,2,1)。
一條三點路徑拒絕染色恰須两端皆 singleton、它們取不同色，而中點 list
恰為這兩色：每個中點可取色只能由一份 singleton 端點阻擋。
第一端的 singleton 必為未用色 3，故得 (a,c,d) 為 {0,1,2} 的排列、
完整 triples={(3,d,a),(3,d,3)}、F*={(a,3),(3,a)}。
刪 zw 有可用對角，刪 mixed 邊有非對角；配合上述 F* 及 |E_r|∈{1,2}，
必要 residual 恰為 T/T、{a}/T、{3}/T、T/{a}、T/{3}，T={a,3}。

關鍵的「零 unary」缺漏可以直接補上，不依有限表。

1. E_r=T 時 D_r=1。没有 unary 則 D_r=0，矛盾。
2. E_r={a} 時 root 不能取 3，但所有原 spoke 的 q 色都屬 {0,1,2}。
   所以必须有 unary 禁 3。
3. E_r={3} 時，若沒有 unary，degree 五迫三條 spokes，criticality 迫其
   顏色互異，即 a,c,d。另一側必為 T。刪 q 色 a 的 spoke 後，本側
   只新增 a；另一側仍只有 a 或 3。取 (a,a) 違反 zw，取 (a,3)
   違反 F*；原 root 色 3 亦无合法對。故刪邊後仍拒絕 q，矛盾。
   root 交換時用 (3,a) 得同一矛盾。

因此 C §1 的每個可能來源都在每側至少有一份 unary；没有「一側只剩 spokes」
的未登錄來源。這個排除已隱含在原 C checker 的 full release criteria：
`c5_mixed_capacity_contacts.py` 行 115–128，而不是僅使用其粗 18 型表。
原文 §1 行 108–109 没有把這个短證写出；整合時應補入，不能僅說 3,497 keys
都碰巧有兩份 unary。

原 C §3 的必要幾何亦重新推導如下。x₀ 的三條 spokes 切 disk 為三區，
H−x₀ 連通，故其餘全部圖落在一个區；該區的原框弧 I 至多三邊。
x₀x₁ 加上 x₁ 两條 spokes 在該區切成三個 child sectors；H−{x₀,x₁}
連通，故 S₂、A_z、A_w 同在一个 J⊆I。每份 unary 都碰 B，否則
其完整 forbidden set 在全 S₄ 下不變，只能 ∅ 或 U，與非空及 ≤3 矛盾。
所以原 z–x₂–w 三角的開內側無任何其他內點；所有側附件在三角外側。
保留 x₂ tether 後，在三角和外框間的環帶，三個內邊界點的實際附件按
同一循環次序成塊；否则兩條分離原路徑交叉。故各 root 支援区塊分離，
且都在 S₂ tether 同側，容許共用具名框端點。這給原 (9) 的四種線序。
完整側圖在逐色固定 q(A_r) 的色置換下保持 E_r，得到原 (7) 的三項
必要色支援條件。這些都是必要性，未宣稱 retained skeleton 有原 source 實現。

[獨立 checker](check_scope_history.py) 僅枚舉 500 份 (3,2,1) 原框附件、
有限 root 角色及上述最多三邊 child sector 內的子集，不 import producer。
它沒有重跑原 114,048 個整框側支援候選；改用 19,340 份 bounded-sector
子集乘積。結果見 [independent_scope_results.json](independent_scope_results.json)：

- 500 local supports 中恰 112 份 F* 非空，得到 560 local/residual 案例。
- 524 份無必要幾何，恰 36 retained cases、140 geometries。
- retained 幾何的完整 `(case, Az, Aw)` 集合與原 artifact 逐集合相等。
- 三個 a 各有 125 full release 角色接合，五型各 25；任何 root 零 unary 的
  接合數為零，與原 125 份具名角色的完整集合相等。
- 140×25 展開的完整 `(case, geometry, side_join)` key 集合與 D₅ scope
  ledger 的 3,500 keys 完全相等；没有只核對總數。

故 36 cases 是 C §1 固定來源前提的完整必要殘留覆蓋，不是所有 weak-deletion
或所有 P₃ incidence 型的完備目錄。若 D₆ 項 1–3 的無界紙面證明通過，
不但可以宣告該固定目錄清空，也可宣告 **C §1 的共鄰端點 P₃ 來源分支排除**，
包括完整圖路徑反向；條件是把上述每側必有 unary 的短證寫回。
[W 報告](../../../docs/c5_qcore_shield_budget.md) §7 行 301–302 把少於兩份 unary
來源列為本輪不推出的情形，對單獨 C-W 的條件式定理而言沒有錯；若要升級至
整個 C §1 分支完成，應以這段重新推導取代該限制。

## 項 6：確認，舊控制確實刻意不用 Gallai

原 C 行 35 明言「不需 T4／Gallai」，行 77 排除完整 Σ 等其他研究線前提，
行 312 把任意大小／Jordan 留在紙面層；它只施加整側 stabilizer、雙扇區、
tether 次序等必要條件。沒有對 degree-four unary 啟用 Gallai + hub/minor
的短框邊支援排除。

D₅ 第一列 `(CPP-131-0,0,0)` 的 D_z_0 確實自身支援為 {1,2}，
接點數三、f={0,1}、E_z={2,3}；另一側同型、S₀=014、S₁=14、S₂=1。
固定支援色 {0,1} 的置換可以交換 2、3，並保持 E_z={2,3}，所以它通過
舊 stabilizer 必要條件。兩側支援 {1,2} 與 {2,3} 共用 b₂ 但不共用框邊，
也通過舊必要環序。原 C 行 292–295 明言 contracted skeleton 沒有原
(5,5) root degree、unary 實現或逐邊刪除見證；把它留下没有斷言存在來源。

因此舊工作未排除不是 Σ 前提偷換，也不是它曾有 Gallai 排除但漏套，而是
當時故意只做必要幾何與完整色角色控制。C-W 新增的是 degree-four
拒絕 unary + 避開 D 的原外路 + hub 原則，這正是舊控制未施加的條件。

## Ledger 整合的具體設計：尚未執行

以下是總數學稽核通過後的可操作設計；現有 W verdict 的 strict replay
另有來源文件 hash 漂移，必先修復，不能把原 `--check` 寫成通過。

### 先保留並修復 W verdict 的證據來源

1. 保存原 `verdicts.json` 全部 bytes、SHA256、來源 hash map 與本輪失敗輸出，
   建立有版本的歷史檔，不覆寫成「當時已成功」的資料。
2. 從同一 C₄ predecessor ledger 重新生成修訂版 W verdict。現有 W `--write`
   用 exclusive-create，原檔存在時拒絕覆寫；整合者應先保存原檔至歷史版本
   路徑，再在空的 canonical verdict 路徑生成修訂版，或為 checker 增加明确
   的新輸出路徑。不能手改 artifact hash 來冒充一次重播。
3. 修訂版對比原版，唯一容許的 payload 差異應為
   `/sources/docs~1c5_unary_shield_budget.md/bytes`、`.../sha256`；
   對完整 JSON 做其餘字段完全相等的檢查。keys、IDs、28 份 certificates、
   3,497 個 verdicts、scope-row hashes、完整未知 relation 界線全部不變。
   若有其他差異，停下逐項說明，不視為純文件來源更新。
4. 對修訂版執行 W 一般與 seed17 strict byte replay，應均通過；來源圖檔、
   C₄ ledger、D₅ scope 與全部依賴也重新核 hash。

### 必須處理的循環依賴

原 W checker 行 19、195、229–252 讀 canonical C₄ ledger，只篩當時
`open_unreviewed` 的 3,497 keys。W verdict 把该 ledger bytes SHA256
寫在 sources。若 ledger 原地 `--write` 改成 zero-open，W 後續會重篩
零 keys，而且 W 新關閉的葉不符合舊 D₅ `closed_by=[]`，strict replay
即失效。不能同時聲稱原 predecessor source 不變及 canonical ledger 被更新。

推薦保持原 C₄ `artifacts/c5_open_leaf_ledger/ledger.json`、`trend.csv` 和所有
既有 snapshots 不變；W 版衍生 ledger 輸出至新版本目錄，如
`artifacts/c5_open_leaf_ledger/cw-v1/`。具體在重算器行 20 改 `OUT` 到新目錄，
並保留同一 `COMMON`、`SCOPE`、domain、stable IDs。原 W 仍能對原 C₄
source 完整重播，新 ledger 把修訂 W artifact 列為额外 immutable evidence。
如果一定要求原 canonical ledger 原地更新，則先保存 immutable C₄ predecessor
並為 W 增加明確的 predecessor-input routing；那是額外來源路徑變更，
不能再宣稱修訂版只改了文件 hash。

### `STAGES`、閉合提取與驗證須一起改

原重算器行 24–28 的 STAGES 為 `(stage, producer, single_target)` tuples；
行 124–146 硬編 observations.json、單份 identity、summary=1、scope_delta=-1。
不能只 append `("W","c5_qcore_shield_budget",...)`。

將 STAGES 改成具名規格，各含 `stage`、`kind`、`source`、`targets`；C₂／C₃／C₄
仍是 `kind=single`、原 observations 路徑和原 literal target，新增
`stage=W`、`kind=batch`、修訂 `artifacts/c5_qcore_shield_budget/verdicts.json`。
把行 124–146 分出 `extract_closed_keys(stage_spec, result, open_keys)`：

- single 路線保留原 identity extraction、exact target、summary 一份、零 target
  queries 等檢查，產生一份 key 與其 `/identity` pointer。
- batch 路線從 `/verdicts` 提取 key；驗證無重複、ID=`leaf_id(key)`、判定字串正確、
  恰 3,497 keys，且 key 集合 **等於當時全部 open_keys**，不僅是 subset。
  它與 inherited 三 keys 不相交，兩者聯集等於全部 3,500 domain。
- 驗證 W 的 `domain_sha256`、`common_source`、`scope_source` 和來源 hash map，
  每個 `scope_pointer` 解析至原 D₅ key，`ledger_pointer` 解析至原 C₄ leaf；
  `complete_scope_row_sha256` 是該完整原 row 的 canonical JSON **含末尾 newline**
  SHA256；certificate pointer 可解析且其 canonical hash 等於 certificate ID。
  不重猜 unknown unary 的完整內部圖。
- 對每個 key 建一份 close event，W event ID 用 `W/<stable-leaf-id>` 保持互異，
  保留 `stage="W"`、原 `/verdicts/i` evidence pointer、certificate pointer、
  `scope_delta=-1`、零 target/Lean、研究完成時間 unknown。W 尚未發布，
  `published_commit=null`；不能把旧 `83ca618` 或只是 baseline 的 `ca3870f`
  写成 W 已发布的 commit。然後一次 `census("W",3497)`。
- 用原 `reconcile(universe,before,after,declared_closed)` 檢查本阶段 exactly
  3,497 個關閉，零新葉／拆分／重開，不能略過其 exact-set equality。

原行 148–159 的 D₅閉合檢查需要分清歷史基準和後續事件，不能把 D₅ 改成
W 的新 verdict。先在 C₄ prefix 完成時檢查 historical closure set 恰等於
D₅ 三 keys、每份 sealed closed_by 一致、historical open=3497、下一入口
`(CPP-134-1,35,20)` 當時確實仍 open。W 後再驗證 current closed=3500、
open=0，原三 keys 的閉合來源不變；新 W keys 的 D₅ sealed closed_by 仍空，
新 current row 的 closed_by 才是具名 W event。

保留行 161–175 的三份過寬單 key 刪除負控制；W 另加 missing-key、duplicate-key、
foreign-key、把 historical 三 keys 算成新增等 malformed batch 控制。
行 264 的 printed open=3497/closed=3 改為從當前 leaves 計算；trend 應恰為
`3500→3499→3498→3497→0`，new_closed 恰為 `0,1,1,1,3497`。
行 194 的舊 C₄ 日期樣本保持歷史基準，不改成今天 zero-open。
新的真實觀測只在當時增加新檔，不覆寫既有日期樣本。

### `--write` 前後檢查

先保存 baseline ledger/trend/snapshots 與所有 source hashes；記錄 domain SHA、
全部 3,500 stable IDs、三份 historical closures、精確 3,497 open key 集合。
在新輸出版本目錄尚未發布前，用新 extractor 做 build-only/preflight，核對
上述 exact sets、完整 row hashes、所有 pointers、negative controls 和新 trend。
目前重算器沒有 build-only CLI；整合時應加 `--dry-run`，令其只回報 census
和候選 bytes hashes，從不寫 artifacts。

preflight 全通過後才可由整合者執行一次
`python3 scripts/c5_open_leaf_ledger.py --write`，然後一般/seed17 `--check`。
再次独立比對 new domain、unit、IDs、parents、common/scope pointers 不變；
原 C₄ ledger/trend/snapshots hash 完全不變；原 C₂／C₃／C₄ event 不變；
新 current open=∅、closed=3,500、新 W 恰=舊 open=3,497，不重算三個已關閉 keys。
確認 W strict byte replay仍通過、來源 hash 前後不漂移，再做文件、DocGraph、
`git diff --check`。本稽核未執行上述任何 `--write` 或修改原重算器。
