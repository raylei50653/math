# N45-S-LONG-S：三件交付的獨立驗收與剩餘義務

日期：2026-10-11。共同 BASE：`f2692089ad4259808e27d9b7e882ac09505b180a`。

**裁決：A 四個任意大小紙面排除通過；B 的限定排除、原邊恢復及必要域以本驗收更正附錄採納；C 通過固定有限介面校準。**
沒有將有限 controls、零 target triggers 或檔案封存提升成來源排除。
本次裁決為獨立 audit 層採納，原交付的 pending 欄位保持歷史 bytes；共享研究狀態尚未更新。

| 交付 | 原成果 | 獨立驗收 | 採納範圍 |
| --- | --- | --- | --- |
| A／DIRECT | [REPORT](../2026-10-11-n45-s-long-s-direct/REPORT.md)、[delivery](../2026-10-11-n45-s-long-s-direct/delivery.json) | [12-claim 紙面審查](direct-paper-review.md) | `t_s=0` 的 `(m_s,n_U)=(4,1),(3,2),(2,3)`，及 `t_s=1` 的 `(3,1)`；全部契約允許的 pair／singleton splits |
| B／FIBRE | [REPORT](../2026-10-11-n45-s-long-s-fibre/REPORT.md)、[delivery](../2026-10-11-n45-s-long-s-fibre/delivery.json) | [15-claim 紙面審查及補強](fibre-paper-review.md) | 其餘兩 profile 的 singleton、pair `(1,3)/(3,1)` 排除；`t_s=2,β=q0,q1∈Q(G)` 排除；其餘 necessary-domain／X-extension／r-fibre 義務按下列界線保留 |
| C／JOINT | [REPORT](../2026-10-11-n45-s-long-s-joint/REPORT.md)、[delivery](../2026-10-11-n45-s-long-s-joint/delivery.json) | [獨立有限驗收](../2026-10-11-n45-s-long-s-joint-review/REPORT.md) | 固定 19 圖／21 原邊省略／210 列／3,360 ordered pins 的完整 lift 鏈；不採納 target-source 排除 |

## 1. 採納必須保留的完整契約

紙面結論只對派工 K1–K12 成立，見共同 BASE 的
[long-contract](../2026-10-10-n45-s-long-contract/REPORT.md)及 A/B 凍結副本。
原 U 由 s 擁有，原 pieces 正是 U、long L、short pair／singleton S；原 G 是 induced-C5 disk、
完整 Σ=933/941 或同一全圖 D5 像、ε=2、非相鄰 degree5 r/s、其餘有效內點完整 degree4，
原 H 連通且完整 B-touch。只省原 r-spoke e；**X=G−e=M 本身**是同一 β 的 inclusion-minimal core，
不能改取另一 core、另一列或另一來源的 witness。

原 contacts／順序／shared vertices、實際 attachments／supports、ownership、rotation、bridges、
全部 tuples／preimages／空 fibres／full lifts 與同一字面色框均須保留。
`(2,3)` 的定理角色交換不交換原 C 身份或 r 座標。
這些前提不是本次有限 controls 自動建立的來源事實。

## 2. B 的驗收更正附錄

原 B 成果未修改。以下附錄是本次採納的一部分，亦記於 [corrections.json](corrections.json)。

1. 原 REPORT §6 的 30 queries 分類 `14 + 4 + 8 + 4` 應為 **`12 + 4 + 10 + 4`**：
   12 無初表匹配、4 T4 排除、10 後續來源排除、4 retained。
   `β=q1／spoke0／FC={2}` 與 `β=q1／spoke2／FC={0}` 都對到初表 record60，
   應歸後續來源排除。四個 retained queries、必要 β 域及 schedules 均不變。
   record60 的 source-minor 排除仍對回凍結 BASE 的 frame-arc 紙面引理。
2. 原 `claims.json` 的 `SF-RESIDUAL.premises` 須補列 **`SF-T2-Q0-Q1-RESTORED`**。
   28 個 raw schedules 中排除 4 個的依據是該恢復引理，不能僅列 SF-QX／SF-RESTORE。

[independent-domain.py](independent-domain.py)不用 import worker checker，重新搬運完整 boundary row、
supports 與 colour permutation，核全部 30 queries 及 `28−4=24` schedules；
原生執行紀錄在 `logs/independent-domain.*`。

另外，q0→q1 的 X 延拓可由此次已核紙面引理直接建立：γ=q1=01202 時，actual C0234
的附件只見色 0/2，故 `(1 3)` 保持完整 C assignments，令 F_C(γ) 也不變。
全列 `|F_C|≤1` 迫 `3∉F_C(γ)`。actual U012 與 β=q0 的逐附件列完全相同，
故 `F_U(γ)={1}`；原 s-spokes 02 禁色 0/2，於是 s=3 有完整 C/U 接合。
這項補強不依賴 missing BASE final JSON，也不建立其它列的 r 色保證。

在同一原圖上，L234 的 `(0 1)` 全 assignment 雙射固定 r=2、s=3；S40、U012
及孤立因子保持原查詢。完整 Xγ(2,3) 與空 Xβ(2,3) 雙射，含 preimages／空 fibres；
其餘 s pins 由實際 U／spokes 排除。因此**每一** Xγ lift 的 r≠2，皆恢復原 e=rb4。
只在原 `q1∈Q(G)` 時得到來源矛盾；β=q2／其它原拒列仍未解。

SF-T1-MAP、SF-T1-EXTEND、SF-T2-EXTEND 的其它查詢保持對明列凍結 BASE
arbitrary-size support-cover／source-minor／extension 紙面依賴的相對採納。
本次沒有 fresh replay 缺 blob 的終局 JSON，亦未把另一列的 X 延拓當作 G 延拓。

## 3. 六個 profile 的批次覆蓋與主攻缺口

因 L/S 都有實際 s-contact，`m_s≥2`；U 非空且由 s 擁有，`n_U≥1`。
由 `m_s+n_U+t_s=5` 恰得六個 ordered profiles：

| t_s | (m_s,n_U) | 本次判定 |
| --- | --- | --- |
| 0 | (4,1) | A 排除 |
| 0 | (3,2) | A 排除 |
| 0 | (2,3) | A 排除；原 C／r fibres 保留 |
| 1 | (3,1) | A 排除 |
| 1 | (2,2) | B 排 singleton／pair13／pair31；pair22 的同源 r-fibre 留 OPEN |
| 2 | (2,1) | B 排 singleton／pair13／pair31 與 q0→q1 原拒 schedules；其餘 pair22 留 OPEN |

B 剩餘 domain 都是原 pair `(k_L^r,k_S^r)=(2,2)`，`t_r=1,e=rb4`、
actual U012/L234/S40，r incident 兩 odd-cycle blocks。
28 個 `(t_s,Q(G),β)` raw schedules 中，`t_s=2,β=q0,q1∈Q(G)` 排 4，
剩 **24 個必要 schedules**。這個數字不計幾何／spoke variants、不是 24 份來源圖，亦不證任何一份可實現。

兩個可直接續攻的具名停止點：

| 身份 | 同一原圖／原色框上的完整義務 |
| --- | --- |
| T1-P22 | s-spoke b0 或 b2，β=q3=01021，Q(G)=013；F_Cβ={1}、F_Uβ={2,3}。Δ={q0=01212,q1=01202} 若為真來源，其全部 X lifts 都須 r=2。須證至少一列有 r∈{0,1,3} 的**完整** lift，才可恢復 rb4。BASE 的鄰列 q2/q4 本來已被 G 接受。 |
| T2-P22 | s-spokes b0,b2，β=q0=01212，Q(G)=024；F_Cβ={3}、F_Uβ={1}。Δ=q2=01201 須找 r≠1；Δ=q4=01012 須找 r≠2。q1 可恢復，但原 G 已接受 q1，故此 schedule 尚未矛盾。 |

對完整 24 schedules 的全部十列、16 pins、原 e 字面色及 Δ，繼續使用 B 的
`obligations.json`；具名兩例只定位缺口，不取代整個 domain。
目前主攻是這個同源原邊恢復義務，不能以端點 marginal、獨立來源或方便的 r 投影代替。

## 4. 有限校準與 custody 驗證

[checks.json](checks.json)保存本次 A `validate.py --contents --manifest`、B 普通／seed17
只讀 checker 與指定壞證書的原生命令／stdout／stderr／exit。
A exit0；B 普通與 seed17 exit0、stdout byte 相等；壞 C assignment exit1 並在 certificate 比較拒絕。
[replay.py](replay.py)在前後捕捉 A/B/C 全樹、112 份去重 live inputs、HEAD 及 tracked diff，全部零漂移。

[custody-review.md](custody-review.md)及 [independent-custody.py](independent-custody.py)
另核 A 精確 51 payload／3,000,959 bytes／2 metadata exclusions、B 精確 846 payload／55,949,264 bytes／1 exclusion，
BASE／live／frozen 的 18／58 inputs、外部 PDF pin，以及 missing BASE blobs。
B 四份歷史 drafts 保留封存，沒有作 current claims 權威。
原生核驗結果在 `logs/independent-custody.*`。

C 另由無 worker／prior imports 的原邊枚舉及 mixed/provenance 核對驗全部
11,280 X lifts／8,007 G lifts、15,960 ambient cells（12,268 空）、420 mixed records、
6,720 mixed pin cells、5,505 C provenance、3,360 root transports。
普通／seed17一致，改 r 色／刪空 fibre 的两指定負控制均拒絕；詳 C 獨立驗收紀錄。

上述固定 finite-interface 控制均為 **triggered and holds**。
全 target K1–K12 source、private-cover 正分支、singleton 正控制、非零孤立因子及 C 的 t_s=0
均為 **not triggered**；沒有 finite target source 建立或執行，trigger_count=null。
抽象 marginal／lost-r 反例保持各自 **counterexample** 判定。

## 5. 來源 finding、信任界與未解範圍

兩個缺 direct BASE blob 的檔案：

- A：`artifacts/c5_no_spoke_exterior/observations.json`。
- B：`artifacts/c5_single_spoke_residual_locality/observations.json`。

本次 git 查詢再次拒絕（exit128）。實體檔、quarantine／historical 記錄沒有替代 BASE 權威；
相關 finite replay 保持未执行。A 紙面排除不依賴缺失 observations bytes；
B 引用的 tracked support table／BASE 紙面依賴仍明列，終局 JSON 未重播。

外部 Gallai theorem 使用凍結 primary PDF：18／58 BASE inputs 與 PDF pin 均相符，
独立紙面審查實讀 PDF p5–6 Lemma7/Theorem10，tightness／Gallai block palette 前提相符。
本次沒有重新抓取網路來源或建立 Lean 外部引理。

歷史 logs 的精確限度保留：A 初次 setup 只有 merged streams；B `finalize.py` 重建的先前
seal-failure streams 是歷史觀察記錄，不能稱本次獨立原生 subprocess capture。
本 review 的 `logs/` 才是本次實際命令捕捉。未呼叫 B 會寫入的 seal wrapper。

完整 U-owner=s／N45／一般 N2/E、來源實現、ε≥3 主問題及新 Lean 仍未建立。
本次只新增兩個獨立 review 目錄，未修改 A/B/C 原成果、共享 docs 或舊證書；未 commit/push/PR。
機器裁決見 [acceptance.json](acceptance.json)，精確輸入身份見 [input-pins.json](input-pins.json)。
最終 [只讀範圍複核](scope-review.json)確認三件裁決、更正附錄及 OPEN 邊界一致，無阻斷 finding。
