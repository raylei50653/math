# N45-PCA：PC 來源契約工具的獨立限定驗收

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**採納 PC 的凍結交付、固定有限控制與已觀察的 fail-closed 路徑。未見阻塞此限定採納的缺口。**
完整 LP source 的 exit0 正分支仍無正控制；不採納一般 validator soundness、來源排除、
任意大小 paper 或 Lean 結論。N2 三項 0 觸發只表示控制沒有充分前提。

只審 PC 工具；未讀 PG／PR 或新監督 paper 判定，未找 source、擴 graph／k、
委派 subagent、commit／push 或傳送外部訊息。所有新增檔僅在本 fresh PCA 目錄。

## 1. 輸入、authority 與獨立性

先讀共享 HANDOFF／STATUS／Git，再對 BASE Git blobs 與 PC frozen 任務／已採納 N45
權威頁。共享 HEAD 等於 BASE；原四份 tracked 修改與其他 worker 的 untracked 目錄保留。
authority 及寫入限制見 [inputs.json](inputs.json)。未把未提交 N45 權威頁冒稱 BASE blob。

凍結 170 份必要輸入：27 份 PC 程式／報告／schema／證書／manifest／proposals、
125 份逐項對 Git objects 的 BASE authority，以及 18 份 PC frozen upstream 交付。
其中 input bytes 與已記錄的 PC 原件 mtime 在結尾均無漂移；125 份 worker BASE source
核 bytes，沒有聲稱其初始 mtime 已記錄。[結尾核對](checks/read-only-after.json)亦核完整
PC manifest 的 6,026 檔／409,041,001 bytes，全部 hashes 相符，PC/source HEAD=BASE 且 clean。
此完整清單的 byte 核對只屬 integrity，沒有讀取或採納其中 paper 判定。

| 凍結 PC 入口 | SHA256 |
| --- | --- |
| REPORT.md | `55daa44d0c67ac081a9a6fc161cf5d3d28e3532801e8912160db5fdefd5ce1e1` |
| checker.py | `9d7c22b5e41f67013b6325e9f59e8404fc3750d1c149a68ee64b407cc780056c` |
| validator.py | `8e2c04155ccf71b90ef1e16eca94764332d2ff5658558d40c1e0fca4fbb26a8b` |
| SOURCE_SCHEMA.md | `f8a65cfea3afdea78f7b73b4ab50a5f5129667090e68058bce35d85e663dae76` |
| certificate-final-v2.json | `538e22dcacaab1bf6f170671ab42f8c7e1af26684e7fa3dfaad5c5b9635501c2` |

[independent_checker.py](independent_checker.py)不 import PC、J、SU-J 或其他 worker 程式。
它从凍結原邊自行生成 proper restricted-growth C5 十列、用固定 degree 順序全染色，
與 PC 的動態 MRV 路徑不同；重建完整 components、接點、ownership、attachments、support、
shared identity、bridges、rotation faces／shield，再逐項比較完整 relations／fibres／lifts。
對每條刪邊另自行尋找完整 witness，並用原邊驗 PC 保存 witness；不是只重播 worker。
保留 [independent-certificate.json](independent-certificate.json) 的全部原圖／X tuples、
空 fibres、full lifts 與具名 witnesses。證書 10,194,377 bytes，SHA256
`2b4740038d376ffc79d05ced2d9981202e3ada51cf4ea0c2edcf9eb3deca9c82`。

## 2. source 契約逐項稽核

[static-contract-review.json](checks/static-contract-review.json)記錄程式位置、實測與未涵蓋分支。
以下量詞都是每份**供給並完成計算的**具名有限輸入，沒有圖族枚舉或 k 上限。

| 義務 | 核對與裁決 |
| --- | --- |
| 原 finite simple edges／有序 induced C5／disk | normalize 從原邊核 vertex／edge identity；rotation 的完整 neighbor sets、darts、faces、有效連通與 Euler=2／唯一 C5 外面另核。缺 rotation 的 fresh 副本 exit2／not triggered；漏原 neighbor 的副本 exit2並指明原因。 |
| 原 degrees、rs 不存在、ε2、H／full B-touch | 兩個指定 roots 原 degree5，其餘有效內點 degree4；孤立內點按 BASE 慣例忽略於有效 H，但 full lifts 保留完整 vertex set。原 H 與 touch 重建；沒有要求 X full B-touch。 |
| 完整 components／one-sided／唯一 unit U | 每份宣告須恰等於 H−roots 的完整原 component，不能拆／併；重建單側性、原 root contacts、ownership、support，shared contact只有一 coordinate。漏 component、錯 shared ownership與錯 unit 均拒絕。 |
| L long、真 pair S、2+2+1 | support 由 actual attachments 重建，真 pair 必等於原框邊兩端；盾邊從同一 rotation 的 complement face重建，要求2+2+1互斥分割五邊與U／L連續三點。錯 partial L 宣告在完整LP未觸發時仍拒絕。19 N2 無完整幾何正例。 |
| 全十列 whole-D5 target | 全原邊計算十列Σ；933／941各10份共同 whole-frame transport，共10個 distinct masks。独立計算同表；沒有逐 piece 正規化。固定N2的target均未觸發。 |
| 每原非框 edge critical | 每條原非框邊在至少一原拒絕列刪除後有原完整 witness；獨立重算555邊的完整gained-row inventory並驗保存witness。顯式空witness inventory拒絕。 |
| X恰整U省略／β-minimal45／54 | 比完整vertices與全部retained edges，分開保存X與G−rx的full lifts；同字面β的拒絕、降度側及每retained非框刪邊witness重算。N2整U皆接受原拒絕β；4份N1校準另列。錯X retained edge拒絕。 |
| 完整 relations／fibres／full lifts | ordered contact tuples、每tuple全部local lifts、16 fibres含空都比較；Cartesian full-local join與直接整原圖全部 lifts相等。獨立固定域重算全部完整資料；漏tuple與漏空fibre拒絕。 |
| zero slack／Delta forcing | 同β逐欄五項各0，mixed欄满額互斥且union=E_r^X；每新接受γ的原U palette與全部X lifts的r投影同singleton。4個zero-slack欄只屬N1；N2／N1各7／4個forcing instances。 |
| source_contract與CLI | 每個layer非 triggered-and-holds 都加入missing列表；有counterexample則整份counterexample，否則缺前提為not triggered。CLI唯有完整source_contract holds才exit0；固定--check exit0只驗bytes。未見「未觸發即來源排除PASS」aggregate。 |

這是 source 契約實作與有限 evidence 的審查，沒有證明所有 arbitrary-size／generic inputs
的 validator soundness。完整 LP antecedent、LP_common_D_and_spokes、LP_cross_row_Q_Delta
的正分支，在本固定控制中都未執行；不得以 negative probes 或 worker byte replay 補 coverage。

## 3. 固定域，分開 N2 與 N1

| 固定域與義務 | N2 | N1介面校準 |
| --- | ---: | ---: |
| 原圖 | 19 | 4 |
| 原十列16-pin fibres | 3040 | 640 |
| 整U省略 | 7 | 4 |
| X十列16-pin fibres | 1120 | 640 |
| 新γ singleton forcing instances | 7 | 4 |
| 拒絕β minimal45／54 occurrences | 0 | 4 |
| 完整LP幾何／targetΣ触發 | 0／0 | 不計入N2 coverage |

另外合計690份piece-row relations／2,986份piece full lifts／555原非框critical edges。
N2只有11圖full B-touch；7份unit U的兩mixed都真short pair，另外12圖沒有incidence-one
unary U。19圖Σ分布959×3、1021×4、1015×4、1007×2、1022×6，沒有whole-D5 target。
7份N2的X全Σ1023。這些0觸發不是來源排除，也不補任意大小 paper 的前提。

## 4. 負控制、命令與封存

[probe-results.json](checks/probe-results.json)保存五個原負控制與六個fresh probes的原 oracle、
命令、exit與確切reason。新probes的vertices／edges全等於原合法control，只修改宣告／rotation
metadata；[original-oracle.json](probes/original-oracle.json)保原完整legal lift、完整原邊、
shared原點9、兩原root-contact edges及原contact tuple。

| 新probe | 實際結果 |
| --- | --- |
| 缺 original rotation，且不宣告舊shield | exit2／not triggered；disk missing=`original named rotation` |
| rotation 漏原 neighbor | exit2；`rotation neighborhood differs from original edges` |
| 漏一個空 fibre | exit2；`complete empty/nonempty fibres differ: P0 row 0` |
| 漏完整 component | exit2；`declared pieces are not all complete original H-root components` |
| 原short P0錯宣告 partial L | exit2；`declared L has wrong original actual support` |
| 原critical witness inventory顯式空 | exit2；`declared critical witnesses do not cover every original nonframe edge exactly once` |

五個既有負控制的漏tuple、錯shared ownership、stale source hash、錯X retained edge及錯unit
也各exit2，與原expected reason一致。另合法缺LP的原proposal exit2／not triggered。
此處counterexample一詞只屬wrong-declaration finding，沒有數學source反例。

PC normal／seed17均exit0，exact final-v2 bytes一致；独立checker generate、normal／seed17
均exit0。再次生成独立證書預期exit1／FileExistsError，證書hash不變。
全部採納命令見 [checks.json](checks.json) 與 logs；runlog 的自身exit0只表示log成功，
實際子命令exit以command.json為準。新檔均exclusive-create；沒有重跑PC的生成命令。

重播独立有限證書：

```sh
python3 -B audits/2026-10-10-n45-pca/independent_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-pca/independent_checker.py --check
```

兩個探索預覽的presentation／path錯誤另外保存在
[exploratory-failures.json](checks/exploratory-failures.json)，未當作control failure或數學finding。
checks聚合初次把probe-suite wrapper誤分類為source CLI的metadata assertion另外保留於
[checks-generation-failure.json](checks/checks-generation-failure.json)；修正label分類後20份command
全部符合預期exit，已產出的judgment／matrix未覆寫。
PC開發舊輸出／空檔／FileExistsError、歷史E4 provenance FAIL、fresh BASE兩歷史缺檔及
whole-worktree duplicate-ID FAIL均保留在原PC交付，其完整manifest已核；本輪未重跑
這些大計算或doc檢查，沒有以PC replay PASS將其改稱PASS。

## 5. 裁決、未涵蓋與停止點

| CLAIM | 量詞、前提、依賴與證據層 | 裁決及限界 |
| --- | --- | --- |
| PCA-01 | 對本凍結170輸入及PC完整6026-file inventory；BASE Git objects、指定PC hashes與舊frozen delivery；hash／Git integrity | holds。PC-01／PC-07的版本與本次read-only部分可採納，沒有採納 upstream theorem。 |
| PCA-02 | 對列明契約程式及供給的完成計算inputs；schema／原edges／rotation／roles；靜態審閱＋12個CLI controls | holds於所查路徑。PC-02採納為具名有限contract工具實作與觀察到的拒絕行為，不是一般validator soundness證明。 |
| PCA-03 | 恰19原N2、7整U及4原N1／4整U；固定清單／BASE原圖；独立stdlib全染色與完整witness驗證 | holds。PC-03～PC-05的有限數字與0觸發採納，N1不補N2。 |
| PCA-04 | 五個舊wrong-declaration inputs＋六個fresh probes；原合法lift／原named edges oracle；實際CLI | holds。PC-06可採納；沒有數學source counterexample。 |
| PCA-05 | 同一凍結inputs與独立證書；normal／seed17、exclusive-create guard、hash前後檢查 | holds。byte determinism／immutability可採納，沒有補一般大小proof。 |

未涵蓋：完整LP positive source（包括long／真pair的2+2+1）、N2拒絕core／zero-slack正例、
targetΣ下的兩個derived LP正分支；任意大小 pieces、string／mixed vertex names、
額外孤立點、非canonical literal β／root交換的generic CLI正控制、供給合法optional
critical／β witnesses的正控制、各類higher-genus／disconnected malformed rotation，
以及大輸入終止／資源耗盡行為。沒有查source、重證Gallai、paper或Lean。

只完成PC工具的限定驗收，不新增數學closure，不改PG／PR裁決，也不選下一residual。
後續若供給具名source，須凍結原bytes、完整確認契約並獨立核結果；本次0觸發不能當驗證
完整source_contract正分支的證據。最终裁決與範圍先寫
[independent-judgment.json](independent-judgment.json)，然後以
[MANIFEST.sha256](MANIFEST.sha256)／[delivery.json](delivery.json)封存再回報監督。
