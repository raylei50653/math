# N45-S-LONG-S-T2-Q2-RESTORE：七 schedules 的同源完整恢復

2026-10-11。BASE：`f2692089ad4259808e27d9b7e882ac09505b180a`。
**全部成果待獨立驗收。**

七個 assigned schedules 均有任意大小紙面排除證明候選。具體構造為
`L_X(q3;0,3)≠∅` 及 `L_X(q4;0,3)≠∅`，兩者皆恢復原 `e=rb4`。
q4 覆蓋五份 schedules；其餘兩份用 q3。沒有建立 actual source、來源枚舉、
Lean 定理或一般 N45/N2/E closure。

## 1. 權威、契約與範圍

工作開始先只讀執行派工 `check_dispatch.py --check`，結果 passes；HEAD 等於指定 BASE。
輸出目錄以 exclusive-create 建立，無 collision。`inputs.json` 分列十二份 BASE Git blobs、
十一份封存 audit SHA256，以及 prior adopted role 的外部 theorem provenance。
本目錄 `frozen/` 保存各權威副本；封存 review 並非 BASE blob。

已讀 frozen long-contract §1 的 K1–K12 全部條款、sealed review 的 REPORT、acceptance、
corrections、fibre-paper-review，以及原 B REPORT §§2–9／obligations。
原 B pending bytes 未改；採納按 review addendum：query partition 為 `12+4+10+4`，
`SF-RESIDUAL` 補列 `SF-T2-Q0-Q1-RESTORED`。本輪沒有借用該 q0→q1 恢復作 β=q2 的證明。
同批其它任務的新結論未作輸入；三份只讀內部分工僅核本任務的推導。

全文量化於同一任意大小、滿足 K1–K12 的原來源，且限定：U owner=s、原 pair S、
`(t_s,m_s,n_U)=(2,2,1)`、`(k_L^r,k_S^r)=(2,2)`，一次共同 whole-source normalization
後為 actual U012/L234/S40、原 s-spokes b0/b2、`t_r=1,e=rb4`。
X=G−e=M 本身為 β=q2=01201 的 inclusion-minimal core，無 retained r-spoke。
actual H_X−s 恰 C={r}∪L∪S 與 U；所有原 edges、rotation、bridges、ownership、
ordered/shared contacts、attachments、全部 assignments、tuples/preimages、空 fibres與孤立因子保留。
每個 L/S 的原 s-incidence 都是1，U 的原 s-incidence也是1。S 不是預設單頂點。

使用已採納 `F_U(β)={1}`，故 actual U 有完整避3 preimage。`F_C(β)={3}`、
`Q(X)={β}`、r 的兩 odd-cycle blocks 亦是已採納背景；以下新證明不需要利用後三項。
新推導只用完整 degree4、connected pieces、具名 incidences、X 拒 β、上述 U 避3，
以及 literal query 的完整雙射。沒有套用四色虛擬框的三色定理或未用色假設。

## 2. 完整 pinned fibres 與 slack

Col={0,1,2,3}。`Λ_T(γ;a,b)` 是同一 actual T 的全部 assignments：滿足原 internal edges、
γ 在所有 actual boundary attachments 的限制、全部原 r-contacts 避 a、全部原 s-contacts 避 b。
shared r/s contact 仍是一個原 vertex，兩個 inequalities 同時作用，並非兩個獨立座標。
未 pin 某 root 時只略去該 root 的 inequalities。

連通圖的 lists 若每點大小至少 internal degree，且至少一點 strict slack，便有完整染色。
取 slack 點為 spanning-tree root，依 child-before-parent 順序貪婪：非 root 在染色時仍有
未染 parent，最多 internal degree−1 個已染鄰點；root 最後由多出一色完成。
這是直接任意大小論證，不需要 Gallai 定理或有限 source。

固定 s=b、尚未 pin r 時，對 T=L/S 的每個原 vertex v，完整 degree 身份給

`|M_b(v)| ≥ 4−|N_B(v)|−1[sv] = deg_T(v)+1[rv]`。

故完整 assignments 非空。令 `B_T(b)={a:Λ_T(β;a,b)=∅}`。
任取一份上述完整 assignment；所有 forbidden a 必出現在它的原 r-contact tuple 中，
否則這一份 assignment 已避 a。因此 `|B_T(b)|≤k_T^r=2`。
這只證共同避色容量界；從不以它代替完整 relation 或選掉其它 preimages。

同理固定 r=a、尚未 pin s 時，S 的 lists 大小至少
`deg_S(v)+1[sv]`，唯一 actual s-contact 提供 strict slack，即使它也是 shared r-contact。
原 degree 身份是計 edges；在 pin s 前只施加 r 一個 restriction，slack 仍存在。

## 3. β 的同列完整避色種子

β 在 actual S40 的逐點色是10。對 a=0、1，先取上述 S 的完整 pre-s assignment。
色 transposition σ=(2 3) 逐色固定所有 actual boundary attachments 及 r=a，
故它對全部原 S assignments、ordered/shared contact tuples、每個 tuple 的全部 preimages、
ambient 空 fibres 都是雙射。如果唯一 s-contact 原色是3，使用 σ 後為2；否則原 assignment
已避3。因此

`Λ_S(β;0,3)≠∅`，`Λ_S(β;1,3)≠∅`。

原 s-spokes 在 β 為0/2，s=3 合法；U 的完整避3 fibre 非空。r 沒有 retained spoke，
L/S 之間無邊，故若某 a 同時不屬 B_L(3) 和 B_S(3)，把同一 β／pins(a,3) 的
全部合法 L/S/U preimages restriction/union 接合便給 Xβ lift，違反 X 拒 β。
所以 `B_L(3)∪B_S(3)=Col`。兩者各至多2；S 的0/1 fibres已非空，迫

`B_S(3)={2,3}`，`B_L(3)={0,1}`。

特別地，同一 actual pieces 的 **局部完整** fibres
`Λ_L(β;2,3)` 與 `Λ_S(β;0,3)` 均非空。它們的 β r pins 不同，
**不是一份 β 全圖 lift**。以下把它們搬到同一目標 literal frame、同一 pins，才完整接合。
此步不使用 N-diagonal；也不從 precoloured-root obstruction 假設一般 rooted bad set 是 pair。

## 4. q2→q4：全部 queries 搬到共同 pins(0,3)

γ=q4=01012。每個實際附件逐點如下；色 maps 的語義是同一固定 piece 的查詢雙射，
不是另一來源的 normalization。

| 原 piece／ordered support | β query | γ query | 完整色 map | 原 pins → 目標 pins |
| --- | --- | --- | --- | --- |
| L234 | 201 | 012 | π=(0 1 2)，3固定 | (2,3)→(0,3) |
| S40 | 10 | 20 | σ=(1 2)，0/3固定 | (0,3)→(0,3) |
| U012 | 012 | 010 | 不主張 β→γ 雙射；另證 γ 避3 | s=3 |

π 作用於 L 的每個原 vertex，保持每條 internal inequality，把每個 actual attachment 的
β 色搬為 γ 色，並同步搬全部原 r/s inequalities。shared contact 的單一顏色同時搬；
逆 map 證明全部 preimages與空 fibres一併雙射。S 的 σ 同理。因此

`Λ_L(q4;0,3) ≅ π Λ_L(β;2,3) ≠∅`，
`Λ_S(q4;0,3) ≅ σ Λ_S(β;0,3) ≠∅`。

在 actual U 的 γ query010 上，未 pin s 的 complete-degree4 lists 由唯一 contact 的
strict slack 保證完整 assignments 非空。(2 3) 固定所有 actual attachments；若 contact 色為3，
全 U 換色後為2，否則原 assignment 已避3。故完整 U 避3 preimages 非空。

q4 的 s-spokes 都是0，s=3 合法。所有 queries 已返回同一 γ frame、同一(0,3)，
全部 restriction/union 給精確全-lift 雙射

`L_X(q4;0,3) ≅ Λ_L(q4;0,3) × Λ_S(q4;0,3) × Λ_U(q4;3) × Col^I ≠∅`。

B、r、s 的固定 assignments 隱含在雙射中；I 是原自由孤立內點全集。
每個因子保全部 assignments，乘積保全部 full lifts，沒有 relation/preimage 數值捏造。
原 `r=0≠q4(b4)=2`，因此此完整 fibre 每份 lift 都恢復原 rb4，並等於 G 的同 pin fibre。

## 5. q2→q3：覆蓋其餘兩 schedules

γ=q3=01021。actual L234 的201→021由 π=(0 2) 搬運；它固定 s=3、把 r=2 搬成0。
actual S40 仍為10，以 identity 保持 r=0/s=3 的全部 fibres。actual U012 仍是010，
§4 的完整 U 避3論證逐附件相同。s-spokes都0。於是

`Λ_L(q3;0,3) ≅ π Λ_L(β;2,3) ≠∅`，
`Λ_S(q3;0,3) ≅ Λ_S(β;0,3) ≠∅`，
`L_X(q3;0,3) ≅ Λ_L(q3;0,3) × Λ_S(q3;0,3) × Λ_U(q3;3) × Col^I ≠∅`。

原 `r=0≠q3(b4)=1`，全部這些 full lifts 均恢復原 rb4。
可再精確核 s=3 切片：q3 的 L/S forbidden r sets 是12／23；q4 是12／13，
皆聯集123。因此兩列 `L_X(γ;a,3)` 在 a=1,2,3 全空，在 a=0 非空。
這不是只有 r 投影；每個非空 fibre 的全部 preimages 由上述完整乘積保存。

## 6. 七份完整 Δ 覆蓋

| Σ orbit | Q(G) | 完整 Δ | 已證 Δ 恢復列 | 選定 pins／原 e 色 |
| --- | --- | --- | --- | --- |
| 933 | 0123 | q0,q1,q3 | q3 | (0,3)，b4=1 |
| 933 | 0124 | q0,q1,q4 | q4 | (0,3)，b4=2 |
| 933 | 0234 | q0,q3,q4 | q3,q4 | 選 q4：(0,3)，b4=2 |
| 933 | 1234 | q1,q3,q4 | q3,q4 | 選 q4：(0,3)，b4=2 |
| 941 | 023 | q0,q3 | q3 | (0,3)，b4=1 |
| 941 | 024 | q0,q4 | q4 | (0,3)，b4=2 |
| 941 | 124 | q1,q4 | q4 | (0,3)，b4=2 |

每份 Q(G) 都是同一 whole-source normalization 後的完整拒列集合，沒有再次獨立設 canonical Σ。
選定 γ 是該份 Δ 中原 G 必拒的列；上面在同源實際 full fibre 恢復 G 接受它，矛盾。
故七 schedules 全部任意大小來源排除候選，沒有新增充分前提。
具名入口 T2-Q2-P22／941-024 特別由 q4 的 full fibre(0,3)閉合。

`coverage.json` 保存七份唯一 spoke variant[0,2]、全部 Δ、十列各16 ordered pins（包含 diagonal），
原 e 每列字面色、必要空 fibres 與已證 fibre。q0／q1 的獨立恢復仍未另證；
它們不是本任務的剩餘 schedule 義務，因每份 assigned schedule 已有上述 Δ 證明。
未提供 actual source，故所有具體 tuple/preimage/lift counts 都為 null，不以 symbolic cell 數冒充來源資料。

## 7. 驗證、findings 與停止界線

`calibration-plan.json` 在執行前固定具名有限域：只核十列／三個 actual supports 的720個
literal 色-map 比較、六份 β 二色 partition 的代數篩選、七份 schedules 的1120個 symbolic
ambient pin cells。沒有圖枚舉、沒有重跑上輪19 controls。
`checker.py` 普通／seed17 只讀 replay 的 stdout byte 相等；錯 L map、刪 diagonal cell 的
兩份負證書保留且均拒絕。這些 controls 僅是 **triggered and holds** 的 literal/pin calibration，
不能代替§2–6的任意大小紙面證明。原生 commands/stdout/stderr/exit 保存在 `logs/`。

缺 `artifacts/c5_no_spoke_exterior/observations.json` 及
`artifacts/c5_single_spoke_residual_locality/observations.json` 的 BASE blobs，finding保留；
各 native Git 查詢 exit128。依賴它們的有限重播未執行；physical/quarantine 未作 BASE 替代。
新紙面恢復不需要它們、舊有限終局鏈或新的外部定理。外部 Gallai PDF pin 僅保留 accepted
β role 的 transitive provenance，本輪未重新下載、未把它當 BASE blob。

`custody-before.json`／`custody-after.json` 核 dispatch inputs、原 direct/fibre/joint 全交付樹、
原證書與 HEAD/tracked diff，前後零漂移。本輪只新增本專屬目錄，無共享 docs 修改，
無原證書／舊 pending 修改，無 commit/push/PR 或外部訊息。

首份 manifest 驗證曾因 validator 以 basename 排除所有同名 delivery.json 而失敗；
兩份封存輸入實際在 payload 內。已修正為只排除本輪根目錄 manifest。
原生 exit1 streams 與首份 delivery 保存在 logs／failed-generations；最後 delivery
重新封存全部檔案，未覆寫失敗候選。此 finding 只涉及 byte-custody validator。
精確 metadata exclusions 只有根目錄 delivery.json 與原生最終驗證 seal-receipt.json；
封存副本中的同名檔案均納入 payload。

| 證據層 | 本輪結論 |
| --- | --- |
| paper | 七 assigned schedules 的 arbitrary-size 同源 full-fibre 恢復／排除候選，待獨立驗收 |
| finite calibration | 固定 literal/pin algebra，triggered and holds；不是 actual graph controls |
| target source | 未建立、未執行；executed=false、trigger_count=null、not triggered |
| source realizability | 未建立；紙面排除與有限 calibration 分開 |
| Lean | 未新增、未宣稱形式化本證明 |
| 一般 N45/N2/E | 不宣稱 closure；t_s=1、β=q0 與其它身份不在本任務內 |

達成指定七 schedules 的窄域紙面證明後停止；本交付的 `pending independent acceptance`
不等於既有研究狀態已採納或共享文件已更新。
