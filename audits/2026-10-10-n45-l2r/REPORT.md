# N45-L2R：LOW2 原圖、双 U-contact 完整關係與三接點映射獨立裁決

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本輪只新增本專屬 audit，未讀本輪 peer judgments、未再委派。

**裁決：六项 LOW2 claims 在原交付完整十二項契約內均成立，無額外前提或新 gap。**
這是任意大小 paper 的獨立審查；正式管理採納與共享傳播由監督處理。
沒有自行採納全 LOW、HIGH、long、其他 cores 或一般 N2／E。

輸入為完整凍結的 [worker report](frozen/worker/REPORT.md)、[claims](frozen/worker/claims.json)、
[task](frozen/worker/task.md)，85 個 worker regular 檔全列入 [inputs](inputs.json)。
四個 BASE blobs 逐 byte／Git object 核回，八個 current pins 在開始時比對 live 與 frozen copies。
本輪可重播核 frozen inputs，故監督新增目錄／後續文檔採納不會假報 worker 舊 live-inventory FAIL。
沒有重跑已因新增 audit 目錄不再適用的 worker 全 live-inventory checker。

## 六項獨立理由

[structured judgment](independent-judgment.json) 為每项保存完整 source contract、量詞、依賴及空的 additional premises。

| claim | 獨立核對 |
| --- | --- |
| LOW2-CORE | 只刪原 rb_i，r 留 rx1／rx2／rp_r／rq_r，X 完整 degree4、無 B spoke；s 完整 degree5，所有 piece 點的全部 degree4 邊不變。X=M 提供自己的 β-minimality；不從原 G 的 Σ-criticality遺傳。 |
| LOW2-COMP | C 的原頂點恰 r＋U＋P＋Q，原邊恰各 piece 內邊與四條 r contacts，故 sole connected。兩原 U-contact 及其中任意長路／cycle 全留。s 三個 contacts 是原 rotation 繼承清單、互異；共用原點只有一個坐標。 |
| LOW2-JOIN | 用同一 f_U 及同一 r 色 c 同時限制 x1、x2；完整 ordered pair fibres 不等於 marginals product。restriction／union 是逐 assignment 的雙射。全 γ、四種 r pins、全 Col³ 空非空 fibres、全部 C/X/G lifts 保留；G 一般 γ 恰多 f(r)≠γ(b_i)。 |
| LOW2-F | X 自身 minimality 迫 s 兩 β-spokes 異色；原拒絕加完整 join 覆蓋兩可用色，逐刪 s-spoke 的完整 β-witness 解除兩原 spoke 色，故精確 F=Col−{u,v}。C 的三 contact slack 另證 R 非空，不假定任意 pin／tuple 有 lift。 |
| LOW2-MAP | 實際 X 的唯一 degree5 s、完整 degree4 C、sole C、三原 contacts、兩異色 spokes、精確 F 都對回 BASE §§1–5。共同 S₄／D₅不重选附件；933 q2保留。Gallai palette 差推出同一 active triangle／三任意長或零長 arms；actual inactive branches 及 tethers不刪。 |
| LOW2-EXCLUSION | X 上五 connected／disjoint bags 的十對原邊鄰接給 K₅ minor，違反 disk 平面性。所有大小及臂長來自 paper 推導，未以有限 calibration 推普遍結論。 |

逐原邊有 `degree_C(v)=4−d_B(v)−1_[v∈K]`；尤其 r 無 B／s 鄰居，`degree_C(r)=4`。
U 的兩 r 邊可使原 U 路與 r 形成 cycle；接合和 Gallai 推導都保留這份原圖。
當 cycle 不能符合 Gallai block 條件，這已是同一原 C 的 degree-list 矛盾，沒有把它替換為 bridge。

完整 relation 的定義域包含全 64 個 contact tuples。每個 tuple 的 Φ_γ(c,t) 保存所有完整 C assignments；
對 s pin a，只加三個具名 contact 的共同不等式。對 shared r／s contact 是同一原頂點 f(v)，不拆 ports。
原孤立內點僅作獨立四色 free-lift 因子。十列及整列 S₄、整圖 D₅與 root swap共同作用全部資料；
Σ(G)、original support／ownership、short／one-sided 等完整來源身份始終留在條件中。

## r 無 spoke 及原 K₅ 抽取

BASE 的使用不是改 LOW1 字樣：LOW2 的 degree／sole C／雙 U-contact joint 已逐原邊重證。
在同一 C 的兩份 pin lists 上 tightness／Gallai block palettes 及 column independence成立。
active incidence forest 恰三 contact 葉，迫一個 triangle 及三 bridge arms，零長時 triangle vertex 本身即原 contact。
每個 triangle 點用兩 triangle 邊與一 arm 邊（零長時為原 s 邊），完整 degree4恰剩一條原邊。

若這條邊進入 inactive W 且 W 不碰 B，則 W 沒有 s-contact，entry 在 W degree3、其餘完整 degree4。
即使 W 含 r，此處 r 的 X degree4且無原保留 spoke，仍沒有外部 pin。C−W 有 strict slack；
W 用四色 slack coloring，再對整份 W 共同換色避 bridge endpoint，延拓被拒絕的同一 M₂，矛盾。
因此每條所需 tether 在 X 真碰 B，不能用已省略 rb_i 補邊。

| 原 bag pairs | 保留原 X 邊見證 |
| --- | --- |
| 三對 V_i／V_j | 三條 active triangle 邊 |
| 三對 {s}／V_i | 三條原 s-contact 邊；zero arms 同樣有該邊 |
| 三對 V_i／O | 三條实际 boundary tethers 的首離開邊 |
| {s}／O | 原保留 sb_j（或 sb_k） |

O 是原完整 B 加三 tether 內點，由原 C₅ 保連通；tether endpoint 可相同，內點互斥。
各 V_i 是 triangle vertex 加原 arm。只在最終 minor 中用 B 作 bag，沒有作保染色 replacement。

外部依賴明列為 [BASE 三接點 §§1–5](frozen/worker/frozen/BASE/docs/c5_two_spoke_three_contacts.md)、
[BASE R10](frozen/worker/frozen/BASE/docs/c5_degree5_interfaces.md)、
[BASE list-critical](frozen/worker/frozen/BASE/docs/c5_weak_list_cores.md) 及
[Dvořák 官方講義 Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
官方 PDF 與 BASE 同 digest；其敘述由凍結 [PDF text](frozen/worker/logs/gallai-text.stdout.log)核讀。
Gallai 外部定理、紙面推導、有限 relation 校準與工具完整性分開，沒有新 Lean 或 lake build。

## 關係語義校準及工具邊界

[calibration](calibration.json) 是一張 abstract fixed graph 的完整 assignments；
[程式](calibration.py) 分別以 piece joint 與 whole graph 直接枚舉核全 C／X／G lifts。
其 U 是 triangle，有兩 r contacts；P 的一原點同時接 r／s，測 shared 坐標。
逐 240 proper literal rows（全十個 canonical patterns），核 61,440 個 `(r pin,t∈Col³)` 全 ambient fibres，
並核 5,760 个共同 S₄及2,400個整圖 D₅動作。
一般 G lifts 加刪除原 spoke 的 `r≠γ(b_i)`，逐 row 與 direct G 一致。

負對照的 U lists 是 `(2,3)`、`(0,2,3)`、`(0,2,3)`：完整 contact pair 必有一端0；
同一 r=0 的 full pair 無 lift，但兩端 marginals 都含2、3，product 誤允許避0 pair。
這精確校準雙 U-contact 同一 colouring 的必要性，沒有變成 LOW2 source control。
**本輪新有限 source 未建立、未執行，沒有 trigger count；没有 source realization、Σ或β-minimal source證书。**

[只讀 checker](verify.py) 重算校準并逐 byte 核回，核85個 frozen worker檔、worker66 payload與19個exact排除、
四BASE／八frozen pins、六項完整裁決、worker receipt／六工具負控制及拒絕階段。
本輪只有頂層目前 manifest／delivery／receipt及四份具名 receipt logs 被排除；
所有巢狀同名 manifest／delivery／receipt都是本輪普通 payload。
[封存 receipt](receipt.json) 綁全部四份 logs與實際 normal／seed17命令、exit、payload前後。
[delivery](delivery.json)綁本輪manifest和receipt。
receipt內normal／seed17使用`--payload-only`建立外層receipt前的完整payload／incoming-receipt核對；
完成封存後可用以下命令另核當前完整外層metadata，兩者的工具scope明列。

```bash
python3 -B audits/2026-10-10-n45-l2r/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l2r/verify.py
```

worker既存文檔缺檔／whole DocGraph／歷史 provenance FAIL保持其凍結原記錄；
worker四nested repositories初始只核目錄存在，沒有聲稱過去遞迴hash其內容。
本輪不為修這些歷史FAIL改共享或刪舊audit，未另外重跑正式文檔驗證。
無新 Lean、commit／push／PR或外部訊息。

Closure scope：完整十二項 LOW2來源契約內的任意大小 paper排除。
Updated：只本 audit獨立裁決／凍結輸入／semantic calibration與封存。
Reviewed-unchanged：全部共享文檔／原交付與舊 audits。
Remaining OPEN：整LOW需獨立合成裁決，HIGH、long、其他cores／原55、非minimal derivatives、一般N2／E、ε≥3及Lean。
Propagation stop：僅本輪独立審查，待監督處理正式採納。
