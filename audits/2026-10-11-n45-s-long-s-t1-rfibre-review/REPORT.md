# N45-S-LONG-S-T1-RFIBRE 獨立驗收與本輪整合

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。

A／T1 的14 schedules、28個原spoke查詢全部通過任意大小紙面排除驗收。
九項 claims 在指定完整 K1–K12 範圍採納，coverage附1132-field更正overlay；無紙面阻斷。
與已驗收B/q0、C/q2整合後，本輪24份剩餘schedules／38個spoke查詢全部排除。
這只關閉完整指定契約下的必要域；未建立一般N45/N2/E closure。

## 同源紙面論證

限定原 U owner=s、U012/L234/pair S40、t_s=1、n_U=2、m_s=2、
原r-split(2,2)、原 s-spoke b0或b2、β=q3或q4、X=G−原rb4且X自己β-minimal。
所有原vertices/edges/rotation/ordered與shared contacts、attachments、旁支、完整
tuple preimages與空fibres保留，來源大小沒有上界。

獨立核雙真拒palette引理：完整degree4給lists≥degree，拒絕迫tight；兩root
queries僅在原端contacts改色。完整off-path非root lists相同，leaf-to-root唯一
palettes排路徑odd-cycle，bridge差交替迫正奇長與完整W residual pair。
固定s-contact在path、旁支或shared vertex均只作用同一list；穩定子核W全actual支援。
原U的Gallai／K4-free推廣另核fixedβ真拒、incident-edge slack、四原tethers與
由retained s-spoke接通的B∪s hub，沒有借原rb4或未證T4前提。

β=q4迫每個完整S path block都actual touch04；相鄰兩塊與原L的r→b2路、
原frame給connected/disjoint的K5五bags，全部十鄰接均原X retained edges，原rb4不用。
β=q3同樣minor與leaf-block degree論證，從任意大小原S推得恰兩原點u/v及原uv；
不是預設小S或刪旁支。q0/q1的actual U附件同為012；若同拒s1/3，當前列
的真palette反設即給U原K5 minor。故存在共同b∈{1,3}的完整U preimage；
原S在該b对全部r色相容，actual L完整assignment至少避兩個r色，選其一a≠2，
完整L/S/U/Col^I同pins接合，q0/q1每列均有同源full lift恢復原rb4。
每份q3 schedule的Δ至少含一恢復列；T1-P22兩spokes均由q0閉合。

逐claim主驗收見 [T1-paper-review.md](T1-paper-review.md)，獨立難點複核見
[T1-stabilizer-review.md](T1-stabilizer-review.md)。額外BASE E4 N-diagonal proof與
原pinned Gallai PDF已凍結於authority/；PDF p5–6 Lemma7/Theorem10原文亦已直接核閱。
保留明列上游紙面／外部依賴，未用同輪其它新結論作T1證明前提。

## Coverage更正、校準與custody

原U query010與兩β和literal01012/01021/01023同附件，FU={2,3}迫s2/3空。
原672位置中320已空，補352個X空欄位；G⊆X再補780個G空欄位，其中540由
原X已空、240由新U空推出。合1132個去重field pointers，保conditional空標籤、
原rb4 filter／rejection、collective恢復語義及全部null source preimages。
更正見 [T1-coverage-corrections.json](T1-coverage-corrections.json)，採納副本見
[accepted-coverage.json](accepted-coverage.json)。原交付bytes不動。

獨立無workerimports核48S/8U palette穩定子、8conditional widgets、18path及2leaf
minor skeletons，100bags connected/disjoint、200實際adjacency witnesses、兩structural
負控制及精確corrupt certificate。完整28queries／280列／4480pins／1120diagonal相符。
普通／seed17原生校準均exit0、stdout/stderr byte相同；負證書exit1命中指定階段，
contents/manifest及獨立custody-calibration亦exit0。校準不驗任意大小主證或來源實現。

custody核54payload/1,938,723bytes、55regular files/1directory、唯一排根delivery。
12BASE+11sealed authorities、一份external primary PDF、49immutable inputs與846份
old B payload／原證書全相符。整原target、root guarded union、HEAD/tracked diff零漂移。
詳見 [T1-custody-algebra-review.md](T1-custody-algebra-review.md)、[checks.json](checks.json)、logs。
root首份guard parser在執行重播前遇舊manifest欄名不匹配；失敗script與tool-call
capture限制保在failed-generations/，修正後上述原生重播全通過，未觸原交付。
原 delivery SHA：`2af82d9afdeaa5509dd211a8c6a64b84520dc379efce9fdd48f84832619d2898`。

## 本輪整合與停止點

前次raw28必要schedules已有四份q0→q1排除。本輪B新增q0三份、C新增q2七份，
A新增T1十四份；28=4+3+7+14，完整指定必要域剩0。本輪派出的是24schedules／
38spoke combinations，均有獨立採納的窄域來源矛盾。D另採納任意大小full transfer
恆等式及1,344 assignments校準，新增來源排除仍0；D自身保凍結時24/38歷史ledger。
整合只在新的 [remaining-schedules.json](remaining-schedules.json)，不改舊證書。

兩份缺BASE observations findings保留，dependent finite replay及舊19controls未跑。
target source executed=false、trigger_count=null、not triggered；source realizability、
新Lean與一般N45/N2/E closure均未建立。所有採納只在專屬review，未改共享文件、
原交付或舊證書；未commit/push/PR。見 [acceptance.json](acceptance.json) 及封存
[delivery.json](delivery.json)。
