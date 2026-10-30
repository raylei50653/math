# 四項突破提案的分別驗證

2026-10-29，核對基線 `4476049`。本次驗證四個具體主張，保留
[精確消元主契約](4ct_guide.md#精確消元主線的研究契約)及
[LOCK-NO-GAIN](ck_d_lock_comparison.md)的適用範圍。

目前可分派的工作見[第二輪結果後的五項任務](#第二輪結果後的五項任務)；
前輪規格與收尾見[五份回報的整合與待證工作](#五份回報的整合與待證工作)。
前面各輪保留原驗證範圍，精確命題與證據仍由各專題報告承擔。

| 提案 | 驗證裁決 | 完整來源 |
| --- | --- | --- |
| 七邊割排除 | 紙證成立：全體頂點最小裸平面反例的非平凡邊割至少八。2,520 對雙側一步篩選零存活。原文一項分量斷言過強，但弱化後足以完成證明。 | [七邊割驗證](four_color_seven_cut_verification.md) |
| 兩步瓶頸與 triangle anchor | 瓶頸成立，須在同一指派保留 Group A；原 anchored 表示沒有漏約束。triangle 的 t=2 成立；維度界限只適用於指定原邊來源。四元表拒 24/256，非 12。 | [兩步消元驗證](four_color_two_step_verification.md) |
| Canonical shelling | 可指定反向 canonical ordering，保持剩餘圖單一簡單外環；完整關係遞推成立。圓盤指處理區域，非已消去點的誘導圖；環長可任意大，非空不變量仍缺。 | [剝殼驗證](four_color_shelling_verification.md) |
| 計數錐與跨 split 手術 | 單純非負邊際與 D 等價；即使補成標準 B5 錐，932 仍有十個整數權重的可行證書。手術須完整切開接口，三份邊界 pairing 不足。 | [計數與手術驗證](four_color_counts_surgery_verification.md) |

「八為緊界」只能證明最小度五的二點側估計在八處停止，不能升格為所有邊割方法的
不可能性定理。triangle 的三張表排除四色覆蓋星的指定邊界，不等於排除 C5 的 T4=932。
一般 932 排除、後續多步來源不變量與共同解存在性仍 OPEN。

## 證據與重播

新增四份獨立核對腳本與
[小型 JSON 證書目錄](../audits/2026-10-29-four-fronts-verification-4476049/)。
來源雜湊與實際檢查範圍見[驗證收據](../audits/2026-10-29-four-fronts-verification-4476049/verification.json)。
七邊與計數腳本不需要圖染色 oracle；兩步腳本只讀原邊，另做完整有限搜尋；
剝殼腳本以候選序配合獨立原嵌入核查，只提供幾何證據。
各報告區分一般紙證、外部定理、有限 Python 核對與既有 Lean 的前提。

```bash
python3 scripts/four_color_seven_cut_verification.py --out /tmp/seven-cut.json
uv run --with-requirements requirements.txt python scripts/four_color_two_step_verification.py --out /tmp/two-step-new.json
uv run --with-requirements requirements.txt python scripts/four_color_shelling_verification.py --out /tmp/shelling.json
python3 scripts/four_color_counts_cone_verification.py --out /tmp/counts-cone.json
```

兩步輸出路徑須尚不存在。既有 Errera 手術及 Lean audit 的實跑範圍見計數報告；
新增結構推論尚未 Lean 化，也未修改主求解器。既有 frozen 證據保留，未 commit 或 push。

文件責任：七邊結果由七邊驗證頁承擔，六邊來源保留原證明並連入後續；
兩步候選由獨立驗證頁承擔，原分解定理不變。導覽與 STATUS 更新直接入口，
HANDOFF 的研究線／活躍標記不變。沒有新增可約構形、不可避免性或跨 split closure。

## e1a90fe 基線的四路續進

同日後續分工成果由各權威報告承擔；以上 `4476049` 驗證與 frozen 證據保留。
本輪三份超過1 MB的完整JSON依既有政策封存；新checkout先執行
`python3 tools/audit_archive.py restore --artifacts`，再讀完整fibres或重播各checker。

| 路線 | 續進與仍缺的環節 |
| --- | --- |
| 反向 canonical shelling | [逐列非空與耳朵收口](four_color_reverse_shelling_continuation.md)：`m≥3` 安全，首次失敗只在全頂點 `m=2` 後綴；一般不鎖定仍等強於4CT。 |
| 共同切口／去奇偶 | [P1–P3局部成果](c5_parity_shared_cut_continuation.md)：六項PM式、完整段奇偶重接、五葉C1與至多兩正收益區域；五參考共同排除OPEN。 |
| 非D正控制 | [Bernhart與B₈基準](ck_bernhart_benchmark.md)：正確圖共6–6對角線，D154／B₈最大支援76；5–5另一圖D160／B₈130。古典C還原重播，無新可約性。 |
| 八割／三步來源 | [原面周長與三步控制](four_color_eight_cut_three_step_continuation.md)：三角化短環契約下兩側各至少三點的割≥9；有限多步鬆弛仍留20型，三步空fibre本身可平面。 |

## 從四路成果接續的三項拓撲核對

以下接續保持前輪證書及其hash鎖定報告的原bytes；入口改動前版本見
[本輪來源快照](../audits/2026-10-29-topology-second-continuation-e1a90fe/source-before.json)。

| 新問題 | 權威來源與裁決 |
| --- | --- |
| 能否略過9–11抽象D表 | [小割周長](four_color_bond_perimeter_small_cuts.md)：三角化S34下兩側≥4的割≥10；加S5後兩側≥7的割≥12。完整處理周長五與不連通分支。 |
| 雙偶補參考能否直接迫奇環消失 | [雙參考奇環](c5_two_reference_parity_continuation.md)：雙命中與跨組保留段成立，真disk仍有九環；五參考共同阻斷未解。 |
| Bernhart 76列是否已提供可直接排除的非平面極射線 | [跨split稽核](ck_bernhart_cross_split_audit.md)：原向量非極端，拆成兩個41列lift極射線；同n/y真disk的普通PM表可不同，尚無新座標排除。 |

## 五份回報的整合與待證工作

2026-10-29，五份回報齊全後核對；基線為 `e1a90fe` 加目前未提交研究。
本節只整理跨線關係與可分派的接續義務，不接管各專題的證明或 OPEN 裁決。
目前主攻仍由[精確消元契約](4ct_guide.md#精確消元主線的研究契約)維護。

| 路線與權威來源 | 已完成的範圍 | 尚不能推出 |
| --- | --- | --- |
| [三步共同原附件](four_color_three_step_source_invariant.md) | 原附件互斥路的端點非交錯；保留原路徑／框證書的同源合併與投影持續滿足此條件。拒絕給定兩份完整前驅上全部 split 檢查仍通過的 ALT-OUTER-17。 | 平面 twin 有相同禁色表及空 fibre，故不能由這次來源排除刪除該表或接口列；完整 D 增益未證。 |
| [Bernhart retained 交會](ck_bernhart_retained_intersection.md)／[共同端點續進](ck_bernhart_endpoint_ray_continuation.md) | RIP 已補原 rotation 推離及邊界修正；兩個41列 lift 有局部控制，r₂另有全來源共同配對及六葉封口必要條件。 | 全部正偶比例實現仍未排除；76列新增必零座標仍為0。形式共同 token 作用模型沒有實際原邊／rotation。 |
| [五參考共同輪轉](c5_five_reference_common_rotation.md) | 同一奇環、同一側字上的命中奇偶與完整交錯段限制；F5-CHAIN9 展示十對各自可行而五份共同不可行。 | F5-CHAIN9 只是抽象接口；完整五族代數控制已被舊共同切口拒絕，未證超過完整舊條件。一般五族阻擋仍 OPEN。 |
| [十二割雙 C₆](four_color_twelve_cut_c6_sources.md) | 完整有序接合、跨度至多三、有弦側分類；W₆側已有C還原，[七點W₅加耳後續](four_color_twelve_cut_w5_ear_reduction.md)也以三弦及八列表完成C還原，兩種七點側均排除於頂點最小反例。 | [八點側後續](four_color_twelve_cut_eight_side_classification.md)已完成來源分類與C還原；裸頂點最小反例只餘兩側至少九點的無弦十二割，一般十二割仍OPEN。二點八割及九割五度三角面另題。 |
| [共同原 hub 的飽和後綴](four_color_saturated_hub_continuation.md) | 已非空且原 hub 連滿外環時，關係恰為全部 proper 至多三色列；完整 fibres 乘積及同一正 K 經整段 m=2 收口保留。 | 共同 hub 未覆蓋一般來源；在無分離三角形的最小反例契約下，該類已受古典三度點化約涵蓋。 |

這五項的完成層級不同。W₆及後續七點耳側給出具名構形的較小平面圖與任意染色還原；hub給出指定來源類
整段後綴的非空定理。前三項補共同來源限制及具名拒證，尚未得到一般關係刪列、
射線排除或五族共同矛盾。三路的局部交錯／側別論證可互相參考，但原圖、接口與量詞不同，
不能將各自可行的資料拼成一份共同見證。

### 可分別交付的五個窄任務

以下保留前輪分工規格與交付補註；目前接續工作改讀[第二輪結果後的五項任務](#第二輪結果後的五項任務)。
編號只供分工；主攻次序仍依研究契約。

1. **三步：從來源限制走到完整關係族限制。** 沿用雙輪圈、原外框與三步次序，明定保留哪些
   原附件資訊，提出對後一步完整關係／fibres 的必要命題。驗收須有來源紙證、指定操作保留性，
   並排除一個明列完整舊關係閉包仍保留的具名共同關係候選；不能只再次拒絕同一交錯來源證書。
   真平面 twin 與既有九點空 fibre 必須保留。這是[目前第一個窄缺口](four_color_three_step_source_invariant.md#6-收尾範圍與下一個窄問題)。
   同日[完整關係族控制](four_color_three_step_relation_control.md)已證兩側全部生成表與核心 fibres 相同，
   但完整剩餘外框問題不同；目前交付不可區分控制，正向新刪列驗收仍未達成。
2. **Bernhart：由射線支援強迫實際接線。** 先選一個41列 full lift，對任意同圖正比例實現，
   從其支援與實際合法交換推出共同原邊／retained 接線的限制；證必有切口違反交會奇偶、
   共同側別或後繼 signature 支援。成功須覆蓋全部可能正比例來源，不能只檢查選定局部控制。
   已證非空內部時比例必為偶整數，可作前置限制；不代表排除所有比例。
   即使排除一個 lift，仍須另證整個76列面上的座標必零，才可報新增刪列；
   兩個 rays 只分解保存的那份 lift，未列盡殘餘面。
   [共同端點補證](ck_bernhart_endpoint_ray_continuation.md#1-rip-的共同端點公式及適用範圍)
   已完成原 rotation 推離／邊界修正及16＋2,992組重核；r₂的全來源接續義務為
   [實際標記六葉來源的矛盾](ck_bernhart_endpoint_ray_continuation.md#5-分開驗收與下一個精確義務)，仍OPEN。
3. **五參考：從真來源迫出不可能的共同側字／段接法。** 固定同一 Q、同一相鄰普通族內的
   奇環極小 M，對五個完整偶補參考族的每份 R 同時施加命中、C1集中與完整段限制，
   十種族對保留全部 Cartesian 組合。窄驗收是：在明確來源子類中，由實際原圖條件迫出
   不可行側字／接法；不得直接假設 F5-CHAIN9 的錨點或單缺口側字。
   要宣稱超過舊條件，須提供通過完整舊共同切口檢查的新拒證對照。
   也可先證共同輪轉條件已由完整舊工具推出，則停止把它當作該層的增益候選。
   真 disk 九環及三族集中／合法切口控制均保留；全域五族排除仍是 E932／4CT 等強目標。
4. **十二割：處理七點 W₅ 加三角耳側。** 在已證有弦來源分類下，先把此側的原最小度、
   S5與十二條有序附件共同施加，研究安全的較小平面替換圖。正向驗收須證縮圖無自環、
   嵌入合法，且其每份完整染色保持同一對側見證並可還原；找不到替換只算此候選未解。
   兩側至少八點的無弦來源另列，不能由 W₆ 還原直接推及。二點八割與五度三角面九割可另分工。
   **同日交付：** [七點耳側還原](four_color_twelve_cut_w5_ear_reduction.md)已完成這項窄任務：五個必要附件型全部涵蓋，刪七點補三弦，八列表保持任意完整對側見證。餘下兩側至少八點的無弦來源仍 OPEN。
5. **反向剝殼：擴大無 hub 的可保留非空來源類。** 選一個實際無共同 hub 的 canonical
   飽和來源子類，給出不以待證可染性定義的幾何條件及完整關係不變量，證經每次合法收口
   保留並支持待閉合端點異色的舊列。驗收須確實含有原 hub 定理之外的來源，且區分是否仍被
   古典化約涵蓋。完整固定三色盤支援只是充分條件：已有五個類外階段不滿足，不能要求普遍成立。
   [任務五：原雙錐連弧來源](four_color_no_hub_bipyramid_continuation.md)已交付一個無窮子類：
   完整路 fibre 不變量經兩端所有合法收口保留；有接受四色／拒 proper 三色的真來源。
   此類仍受古典四度點化約涵蓋，一般來源覆蓋與一般不鎖定仍未解。

全部交付沿用同一原圖、同一字面色框、有序實際附件及含空列的完整 fibres；最後才回寫
同一份共同解。一般來源覆蓋、閉合不變量與共同存在性仍是不同義務，有限控制不代替它們。
五份結果均無新增 Lean 證明；紙證、固定域 Python 與未形式化部分分開引用。

本輪只做交叉審閱、既有重播與入口整理，未擴枚舉或修改主求解器。
整合時另依既有政策補封存超過1 MB的五參考證書，原始 bytes 與舊封存紀錄均保留；
新 checkout 仍用 `python3 tools/audit_archive.py restore --artifacts` 還原完整證書後重播。
實際重播與文件檢查範圍見[整合收據](../audits/2026-10-29-five-results-integration-e1a90fe/verification.json)；
各分支較早因並行缺件而失敗的紀錄保留，不追改成通過。未 commit／push。

## 第二輪結果後的五項任務

2026-10-29，第二輪五份結果齊全後核對。以下是接續任務，不是已證結論；
各題先讀當前權威來源與全部假設。三步共同來源仍為主攻。

| 本輪交付 | 對下一輪的限制 |
| --- | --- |
| [三步不可區分控制](four_color_three_step_relation_control.md) | 共同核心表及其關係代數閉包無法區分 ALT／twin；四 port Boolean 接口全接受。完整剩餘問題不同，原圈16型未新刪除。停止只改外框的同核枚舉。 |
| [RIP端點與六葉降階](ck_bernhart_endpoint_ray_continuation.md) | RIP補證完成；r₂非free來源封口為帶標記f的六葉完整lift。尚未排除實際來源或任意正偶比例，新增必零座標0。 |
| [五參考來源排除](c5_five_reference_source_exclusion.md) | 非面奇環的單命中聯集至少缺兩邊；非面端葉三角型已排除。完整舊切口的200條真disk控制保留，嚴格增益及一般蘊涵均未證。 |
| [七點W₅加耳還原](four_color_twelve_cut_w5_ear_reduction.md) | 另一種七點側已完成C還原；連同W₆排除七點側；[八點側後續](four_color_twelve_cut_eight_side_classification.md)再完成全部八點側，裸最小反例只餘兩側至少九點且各自無框弦。 |
| [無hub雙錐連弧](four_color_no_hub_bipyramid_continuation.md) | 無窮子類的完整路fibres與全部合法收口已封閉；所有原環點仍度四，這個子類不進入最小度五的最小反例來源。 |

### 任務一：改變實際共享接口，建立共同外側的跨列限制

**2026-10-30 後續。** [zv 新接口與共同外側交換](four_color_three_step_shared_exterior.md)
已改變第三 bucket、完整核新接口與舊閉包，並建立同原邊的六對接合／精確交換契約。
外框仍全接受；反控制只拒絕交換目標混接，新增解列排除0。下述關係族正向驗收仍 OPEN。

接續[三步控制的缺口](four_color_three_step_relation_control.md#6-對新附件限制的裁決與缺口)。
先選一種明確的新附件契約，例如將z或w的實際外側通道納入接口，仍保持兩中心的完整原鄰域。
所有新增原鄰邊須真正進入相應消元bucket，不得僅附輪轉標籤而沿用舊生成表。
也可直接保留完整外側lift及六對分量，但須明定跨列合法交換如何指回同一來源、同一原邊。

先完整核新接口的Boolean接受表與舊閉包；若又是全接受，只終止該Boolean增益候選，
不繼續擴同核枚舉。正向驗收須有對所有指定平面來源sound的跨列命題、指定操作保留證明，
以及完整舊條件仍接受而新規則拒絕的具名共同候選。保留平面twin、九點控制與合法空fibres。
只給精確消元等式、來源ID保存或再拒ALT，不算完成本題。

### 任務二：標記六葉邊的全染色閉圈條件與二端分離

**2026-10-30 部分完成：** [精確切口契約與保標記控制](ck_bernhart_marked_separation.md)
證目標來源含 f 的二邊割若存在，必有可安全分離的無葉側；完整 fibres、三 split
signed signatures 與倍率均有契約。全染色 MC40 控制否定單邊替換後自動保閉圈標記，
但它不符目標 lift，亦有無標記二端分離；一般分離存在性與 r₂ 排除仍 OPEN。

接續[六葉封口與精確義務](ck_bernhart_endpoint_ray_continuation.md#5-分開驗收與下一個精確義務)。
先處理非free分支：連通plane六葉網路容許平行原邊，保留外面標記邊f，完整計數為
`μ(k,h)`、`μ∈6ℤ₊`；每份完整染色中，f在含其顏色的兩個雙色系統皆屬閉圈。
研究這些條件是否迫出不含葉、可安全分離的二端原區域，或另一項實際切口限制。

驗收可為一般分離定理，並附區域刪除／替換時全部六葉fibres、signed signatures及倍率的精確契約；
或交具名完整反控制。若反控制只滿足閉圈條件而不滿足目標lift，僅否定該一般分離推法。
不得只憑閉圈就收縮原圈；保留其內外附件。free-edge分支另為`λ(k,h)`，不可混入非free倍率。
形式token、B₆可行或一份接線失敗均不能排除射線；r₂與76列面仍分開驗收。

### 任務三：非面五環的二缺邊與完整多命中

**2026-10-30 子類完成：** [完整內側奇偶與 C1 證明](c5_nonfacial_two_gap_exclusion.md)
導出兩分量的實際側字並排空相鄰及不相鄰二缺邊；更強地，非面奇環至少缺三條單命中邊。
完整五族、全部多命中、十種族對與 C1 均保留；一般來源是否落入此子類及三缺以上仍 OPEN。
以下保留本輪原任務契約，結論範圍以新來源為準。

接續[單命中缺邊來源](c5_five_reference_source_exclusion.md)。
先作常規小割奇偶的範圍校正：非面三角在有完整Tait染色的本來源中已可整體排除，
不再把「三角無直接端葉」當新分支；[審閱推論](../audits/2026-10-29-five-results-round2-integration-e1a90fe/review-notes.md)列出含內弦處理的紙證。

選下一個明確子類：固定字奇環極小M的同一非面`O=C₅`，假設完整單命中聯集恰缺兩條原邊e、f。
這兩項是子類假設，尚未由一般五族來源迫出。先導出U₁兩分量的實際側字及e、f的轉側身份，
再研究完整Γ與極小性是否迫出某份實際R，使`H_R`恰命中e、f之一，或迫出其他不可行完整段接法。
全部多命中參考、十種族對及完整C1區域仍保留，不能只挑五份方便的參考。

正驗收可先排一個明列e／f相鄰關係的子型，須由來源推出禁止情形，不能將它當作前提。
尚未迫出的分支明列OPEN；抽象摘要的共存不冒充plane五族反例。保留七／九環與三族控制；
若宣稱嚴格增益仍須另作完整舊共同切口比較，不推成一般E932排除。

### 任務四：雙側至少八點的十二割，先完成八點側來源分類

接續[七點側全部還原後的範圍](four_color_twelve_cut_w5_ear_reduction.md#4-裸平面頂點最小性與結論範圍)。
固定原最小度五、S34／S5、雙無弦C₆、十二條有序跨邊與各側至少八點。
先限一側恰八點，從原三角面、Euler恆等式與度數分類兩個內點的全部可能原誘導圖；
再列盡該側容許的有序附件型，分清必要型與真正可實現型。

驗收首先是分類完備紙證、全部4096框列的完整fibres及含原邊身份的有限重播。
若找到新C還原，再另證縮圖簡單平面、嚴格較小、每份縮圖染色保同一對側見證還原。
不要求或宣稱全部十二割不存在；至少九點側與一般可約性保留OPEN。
二點八割、五度三角面九割另題；不得把固定原圖控制或必要附件型當一般來源覆蓋。

**2026-10-30 交付：** [八點側分類與 C 還原](four_color_twelve_cut_eight_side_classification.md)完成唯一原誘導盤、17 個度數必要候選、兩個混合 S5 排除與 15 個真正可實現型。每型完整 fibres 及原邊／原混合面重播已保存；14 型補三弦、均勻型識別相對框點，全部保持同一對側見證還原。最小反例只餘兩側至少九點；一般十二割與至少九點側不作判定。

### 任務五：進入最小度五來源的無hub收口不變量

接續[雙錐來源的古典涵蓋與界線](four_color_no_hub_bipyramid_continuation.md#4-真正超出-hub三色盤支援但仍屬古典化約)。
新來源必須來自原最小度五、S34／S5的實際球面三角化及canonical飽和階段，並無共同原hub。
先給一份可核原圖／選序以證來源非空，再定義有幾何意義的來源子類，避免僅對雙錐加填區而
重新引入低度點或分離短環。若候選幾何本就違反前提，交付來源不存在證明並停止該候選。

從已有非空完整外側關係出發，提出完整關係／fibre不變量及非空支援子族，證全部指定合法
`m=2`收口保留，且每步都有待閉合端點異色的同一見證舊整列。不強求普遍固定三色盤支援。
驗收包含來源可達性、一般紙證、含空fibres重播及古典化約涵蓋核對；有限圖成功不能升格一般覆蓋。
一般不鎖定與4CT仍OPEN，不以「最後可染」定義來源或不變量。

### 共用交付契約

BASE是`e1a90fe`加目前未提交成果；先凍結引用來源hash。每題使用新報告、新腳本與專屬audit，
結果齊後再統一更新共用入口。保留原圖、字面色框、有序實際附件、全部空／非空fibres與同一見證，
最後才回寫。紙證、Python、Lean及OPEN分開；不以4CT作oracle、不自動commit／push。

本輪核對與重播、封存及文件檢查見[第二輪整合收據](../audits/2026-10-29-five-results-round2-integration-e1a90fe/verification.json)。
以上只分派接續義務，未執行新一輪搜尋，未新增主求解器或Lean改動。
