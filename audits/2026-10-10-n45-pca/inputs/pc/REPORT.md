# N45-PC：N45-U-LP 完整來源契約的只讀有限 validator

2026-10-09。任務：[凍結任務全文](frozen/docs/history/2026-10-09-n45-u-long-short-pair-tasks.md)，共用任務頭＋N45-PC。
BASE／獨立 clean checkout HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**完成工具與指定有限域交付。19 N2 的 LP 幾何、完整 target Σ、拒絕 β 的 minimal 45／54 整 U core 各為 0 觸發。**
5 份錯宣告副本全部被拒絕；normal／seed17 只讀重播通過。
這是具名來源契約的有限驗證器，沒有來源排除或新 paper／Lean 結論。
N45-U-LP、一般 N2／E 保持 OPEN，未尋找新 source，未擴大 graph／k 搜尋。

## 1. 版本、凍結與寫入邊界

先讀 HANDOFF／STATUS、Git、指定任務及 N45 權威頁；另外對照 BASE Git objects 的
HANDOFF／STATUS／DOCUMENTATION。共享 main 原有 tracked 與 untracked 工作見
[initial-state.json](initial-state.json)。從 BASE 在本目錄建立自己的 detached
[source checkout](source/docs/HANDOFF.md)，初始／重播均核 HEAD 與 clean status。
只寫本 fresh 目錄；未委派 sub-agents、commit／push、PR、對外訊息或修改共享文件。
未讀取 PG／PR 的新判定，也未 import J／SU-J 或其他 worker checker。

[inputs.json](inputs.json)逐項保存九個指定 frozen hashes，均與任務頭精確相符；
新權威頁與 S／U／SU-A／SU-J／J 證書是 frozen delivery，沒有冒稱 BASE blob。
S 69／U 70／J 66／SU-J 71 項 manifest 全部對 Git objects；union 71 路徑，
另核 54 個既有 control 指向的原 source graph bytes，共125個 BASE 權威路徑。
原 control edges 逐圖等於該原 source 的 canonical_edges，source_sha256 相符。
18份新交付的凍結副本、原件 hash／mtime 亦保存。

工具概念沿用 J／SU-J 的 named contacts／完整 fibres 介面，但程式自行實作：
[validator.py](validator.py)從原邊作 MRV 全染色，再與完整 local lifts 的笛卡兒接合比較；
[checker.py](checker.py)另對照 frozen SU-J 的原介面、full-lift counts 與保存合法 witnesses。
局部 tuples 與同一原圖的 root pins 共用一份 shared coordinate，不用端點 marginals。
獨立性不表示兩個 worker 的 paper 已重新稽核。

## 2. 精確來源契約與判定

量詞為「每個**供給的**具名有限簡單原圖 proposal」，並非枚舉任意大小圖族。
沒有 k 上限；窮舉該有限輸入的染色可能昂貴，若未完成則沒有可採納判定。
完整 LP 契約要求：有序 induced C5 外面、原 rotation 為 disk；忽略明示孤立內點後，
恰兩個原 degree5 roots、rs 不存在，其餘原內點 degree4、ε2、H連通且 full B-touch；
H−{r,s} 恰兩完整 mixed L／S 與唯一原 incidence-one unary U；每份 one-sided、support 非空；
L 原 actual support long、S support 恰為真框邊 pair，原盾弧 (U,L,S)=2+2+1 分割五邊，
U／L 原 support 各連續三點；完整 Σ933／941 或整個 frame 的共同 D5 像，原非框邊全 critical；
X精確等於整份原 U 省略，在同一 literal β 拒絕、root degrees 45／54 且刪每條 retained
非框邊均接受 β。全部 relations／空 fibres／full lifts、原 attachments／ownership／bridges
及 rotation 在同一圖、同一 literal frame 下重建。root 次序可供給，降度側 r 由原 U owner 判定。

`--source`分欄輸出以下 layers；各層用 `triggered and holds`／`not triggered`／`counterexample`，
`missing_sufficient_premises`列缺前提：

| 欄 | 實際核對 |
| --- | --- |
| source_hash_binding | proposal 的 source_sha256 精確綁定原 graph_file bytes；不把 digest 當第三方來源認證 |
| ordered_induced_C5_disk | 原 rotation neighbor sets、每個 dart／faces、有效圖連通、Euler=2、唯一 C5 外面 |
| original_degrees_rs_epsilon2／full_B_touch_H_connected | 原 degree、rs不存在、有效 H 與原 touch；不要求 X full B-touch |
| complete_components_one_sided | 原完整 components、contacts／單一 shared coordinate、ownership、實際附件、原 bridges；由原 complement face 重建盾邊 |
| LP_original_geometry／declared_U_L_S | 原 unit incidence、actual long／真 pair、原2+2+1及五邊分割；不逐 piece 正規化 |
| complete_relations_fibres_full_lifts | 十 literal rows、全部 ordered contact tuples、每 tuple 全 local lifts、16 fibres含空；接合等於直接原邊的全部整圖 lifts |
| full_ten_row_target_whole_D5 | 933／941各10個 whole-frame D5搬運記錄，共10種不同 masks；只搬整個 frame |
| each_nonframe_edge_Sigma_critical | 每條原非框邊至少一個原拒絕 row 在刪邊後接受，交具名 full witness |
| exact_whole_U_omission／declared_X_identity | 完整 V(U)全部省略、其餘原邊全部保留；另保 G−rx 的 vertices、全 lifts，兩圖 root-pair 集合相等 |
| rejecting_beta_minimal_45_54_core | 同 literal β 的 X拒絕與每條 retained 非框邊刪除 full witness；不從原 G 遺傳 criticality |
| core_zero_slack_full_partition | 每個 b∈E_s 的五項 D/O/δ/o/λ逐項為0，原 mixed欄滿額、互斥、union=E_r^X |
| all_Delta_gamma_singleton_forcing | 每個新接受 γ 的原 U contact palette非空 singleton，等於所有 X lifts 的 r投影 |
| LP_common_D_and_spokes／LP_cross_row_Q_Delta | 全 LP 先決條件成立才核：spokes各側色互異、共同 D、S接受(D,D)/L禁止；Q(X)空/單點/相鄰pair及Δ下界 |

錯的可核宣告立即拒絕；未滿 LP 圖類／目標前提為 `not triggered`。
`source_contract`是「這份具名輸入是否完整符合契約」，**不是來源排除 aggregate**。
缺任一充分前提時 `--source` exit2，不能因沒有觸發而 PASS；完整契約成立才 exit0。
`--check` exit0只表示固定 certificate bytes重播相同，明示 LP仍 not triggered。
資料錯誤的 `counterexample`指錯宣告，沒有稱其為 mathematical source counterexample。

## 3. CLAIM、依賴、有限 coverage 與 finding

各項的證據層皆為 stdlib Python 固定域／工具核對。數學前提與任意大小適用範圍由
[N45 權威頁](../../docs/c5_excess_two_nonadjacent_unit_core45.md)、BASE E2／E3／E4及原S/U paper承擔；
本輪没有重證上游分類、外部 Gallai 或新增 Lean。

| CLAIM | 量詞、全部前提／依賴及本輪結論 | 缺控制、未涵蓋與 finding |
| --- | --- | --- |
| PC-01 | 對指定九 hashes與四 manifests的每項，對應 frozen delivery或BASE object；125 BASE paths及18 frozen deliveries相符，clean checkout成立。依 inputs／setup logs。 | 共享主工作樹的未提交頁不是BASE；歷史E4 provenance FAIL另列，不改舊證書。 |
| PC-02 | 對每份供給的具名原 graph＋rotation、pieces、U/L/S、literal β/X，工具逐欄重建上述來源契約；所有保存有限payload重播。依 validator.py、SOURCE_SCHEMA.md。 | 沒有完整LP positive source control；一般輸入分支的 soundness未Lean化，未證任意大小paper或來源不存在。 |
| PC-03 | 固定清單恰19個N2；每圖原component identity、support／rotation／shield、十列full lifts及逐原邊critical witnesses重算。獨立檢出LP幾何0、targetΣ0。依BASE原圖、J清單及SU-J保存payload。 | 11圖full B-touch；7圖unary incidence1，其mixed都真short pair；其餘12圖unary incidence2。因此沒有完整unit-U＋long＋pair控制，不能填target coverage。 |
| PC-04 | 恰7份N2完整unit-U省略，每份10列／160 fibres含空與所有full lifts；X全Σ1023；全部原拒絕β在X接受，所以拒絕minimal45/54為0。每份Δ的新γ singleton forcing成立，共7 instances。 | 缺N2拒絕core的zero-slack／L-S滿額分割正控制；7份接受X不能當LP來源排除。 |
| PC-05 | 另4份N1完整U只作介面校準；4個拒絕β minimal core與zero-slack控制成立、4個新γ singleton forcing；與N2標籤及計数分列。 | 一mixed，且有其他原unary／缺targetΣ、LP；不補N2／LP coverage，不把歷史12個N1 core occurrences擴入本輪。 |
| PC-06 | 五份同一原graph的錯宣告副本：漏完整tuple、錯shared ownership、stale source hash、錯X retained edge、錯declared unit，全拒絕；原合法piece／whole lift及原root-contact／retained edges為oracle。 | 只有malformed-input controls，沒有數學source反例；副本及expected_error只在本fresh目錄，原證書未改。 |
| PC-07 | normal與seed17逐byte重播同final certificate；183個已列原件／凍結輸入／fixtures／證書／程式的bytes及mtime前後零漂移；再次生成預期FileExistsError且證書未變。 | 紙面、Lean、全型來源coverage不由byte replay提升；其他workers並行新增輸出不屬本任務判定。 |

19 N2原Σ分布：959×3、1021×4、1015×4、1007×2、1022×6，均非933／941的整圖D5像。
逐圖必要幾何profile、每candidate缺前提、全部relations／原邊witnesses見
[final certificate](certificate-final-v2.json)，不是只存marginals或counts。

| 固定域查詢／保存項 | 數量 |
| --- | --- |
| N2原圖／原16-pin fibres | 19／3040 |
| N2整U省略／X16-pin fibres | 7／1120 |
| N1原圖／原16-pin fibres | 4／640 |
| N1整U校準／X16-pin fibres | 4／640 |
| 原piece-row完整relations／full piece lifts | 690／2986 |
| 原非框critical edges及其具名witness inventory | 555 |
| N2／N1新γ singleton forcing | 7／4 |
| negative input拒絕 | 5 |

這些查詢不宣稱原7200pins重播等於新paper驗收。本工具把逐圖完整契約與缺前提
交給後續具名source proposal使用；本輪没有positive sample可供LP完整触發。

## 4. 負控制、exclusive-create 與版本保留

五份副本在[negative-inputs-v2/index.json](negative-inputs-v2/index.json)，
`oracle`保留NA7-0002/P0/index0的原tuple與原legal lift、shared vertex9的兩原contact edges，
或原index0整圖lift及retained edge(0,5)。checker先用原邊逐不等式核合法、對原保存tuple，
再要求錯副本被拒絕；沒有由錯副本自己產生oracle。
每份CLI也實跑一次，均exit2，stdout保存拒絕finding。
[合法但缺LP的控制](controls-v2/NA7-0002-P1.json)CLI亦exit2，保全各欄missing，未偽造L／S宣告。

輸出目錄及每個JSON／log用exclusive-create。[build_controls.py](build_controls.py)重建只允許fresh目錄；
[run.py](run.py)在執行前exclusive-reservestdout/stderr/command metadata；checker在計算前
`open('xb')` reserve certificate。對已存在final證書再`--generate`立即FileExistsError，normal／seed17無寫入。

保留本輪開發失敗：首次fixture build誤把BASE舊shield擴充字段當新canonical shield，exit1；
未寫任何fixture，空controls／negative-inputs目錄保留，後續改具名controls-v2／negative-inputs-v2。
`certificate.json`為首次成功payload，對應checker-generation-1.py／validator-generation-1.py；
加強檢查legacy available欄後，一次generation因unary available只列owner而錯判，exit1，
空`certificate-final.json`及完整log保留；修正只核原owner後另建`certificate-final-v2.json`。
舊輸出未覆寫，沒有把程式適配失敗當source反例；唯一可採納重播入口是現在checker的final-v2。

## 5. 重播、驗證與保留 FAIL

根目錄執行，只讀：

```sh
python3 -B audits/2026-10-09-n45-pc/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-pc/checker.py --check
```

後續供給具名proposal的schema、例子與exit含義見[SOURCE_SCHEMA.md](SOURCE_SCHEMA.md)。
`--source`只讀proposal與graph_file並將完整結果寫stdout；不建立結果目錄、不更改輸入。

final certificate：12,850,494 bytes，SHA256
`538e22dcacaab1bf6f170671ab42f8c7e1af26684e7fa3dfaad5c5b9635501c2`。
所有實跑command／env／exit／完整stdout/stderr見[checks.json](checks.json)與logs；
[read-only-after.json](read-only-after.json)對183個檔案報零漂移。
完整inventory見[MANIFEST.sha256](MANIFEST.sha256)，manifest及排除自指項見[delivery.json](delivery.json)。

| 檢查 | 實際結果／界線 |
| --- | --- |
| final normal／seed17 | 各exit0，同certificate bytes；只驗指定固定域及五負控制 |
| 五negative CLI／合法缺LP CLI | 各exit2，預期拒絕；後者source_contract=not triggered |
| 已存在certificate再次generate | exit1／FileExistsError，預期exclusive-create拒絕，證書hash未變 |
| fresh BASE check_docs.py | **exit1**：586 Markdown／6982links，兩歷史missing paths |
| fresh BASE正式docs DocGraph | exit0：62documents／213relations／5families，0errors／notes |
| shared whole-worktree DocGraph | **exit1**：62duplicate-ID errors；原scratch、U/source、SU-J/BASE及PC/source等副本保留，未刪來遮FAIL |
| tracked git diff --check | exit0；本目錄authored文字另核whitespace／report local links |

fresh BASE兩缺檔：`audits/2026-10-04-task-d5/c4/scope_ledger.json`、
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。未補造舊檔。
歷史E4 core／reductions普通及seed17共4次exit1的provenance FAIL另凍結於
[historical-inputs.json](historical-inputs.json)：原E3 REPORT historical SHA
`6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659`與BASE
`73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3`不同。
本輪只讀既有A／batch記錄及四原log，沒有重跑E4大計算，沒有將本工具PASS改稱歷史PASS。

未跑lake build／axioms（沒有Lean改動或新theorem），未跑E3／E4／E4C大枚舉、U1–U4、
新pieces或graph/k搜尋；未審PG／PR、任意大小Gallai／paper及source實現。

## 6. 停止點與文件分層

Closure scope：只完成N45-PC工具、指定有限controls、負控制及可重播交付；無數學branch closure。
L0 Source/Evidence更新限本目錄；L1對回[N45入口](../../docs/c5_excess_two_nonadjacent_unit_core45.md)
§3–4與[Kempe guide](../../docs/c5_kempe_guide.md)，停止點仍N45-U-LP，無數學語義變動。
共同任務明示禁止改共享導航，因此本輪未寫STATUS／HANDOFF／README；交監督端採納時索引。
L2／L3無closure或已採納前提失效，停止擴張；PG／PR的paper依其獨立任務裁決。

Remaining OPEN：唯一原U＋long L＋真short pair S的任意大小同源跨列來源／排除；
singleton short、S LOW／HIGH／long、原55、其他core、無45/54來源、一般N2／E與ε≥3。
下一步只是供後續具名proposal使用此只讀契約；本輪不選下一residual、不尋找新source。
