# 任務 C：t_s=2、β=q2 的七個剩餘 schedules

任務 ID：`N45-S-LONG-S-T2-Q2-RESTORE`。
專屬輸出：`audits/2026-10-11-n45-s-long-s-t2-q2-restore/`。**本輪可獨立並行；成果待獨立驗收。**

## 共同契約、權威與工作界線

工作目錄 `/home/ray/developer/ai/math`。本輪 Git BASE 固定為
`f2692089ad4259808e27d9b7e882ac09505b180a`；舊報告內的較早 BASE 是歷史 provenance。
派工包 `audits/2026-10-11-n45-s-long-s-rfibre-dispatch/` 的 `input-pins.json`
列出 BASE Git blobs 與另行封存 audit 輸入，副本分存 `authority/base/`、`authority/sealed/`。
已驗收 review 尚未 tracked；它的 SHA256 是權威 pin，**不得偽稱 BASE blob**。
工作開始先只讀核派工包：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-rfibre-dispatch/check_dispatch.py --check
```

先讀 frozen long-contract §1 的 **K1–K12 全部條款**、已採納 review 的 REPORT／acceptance／
corrections／fibre-paper-review、原 B REPORT §§2–9 與 obligations。
原 B pending 欄位保持歷史 bytes，採納範圍依 review 及 corrections；沿用
`12+4+10+4` query 分類及 SF-RESIDUAL 的恢復引理依賴補列。

本輪只續攻 **U owner=s、原 pair S、原 r-split `(k_L^r,k_S^r)=(2,2)`**。
用一次共同 whole-source normalization 保留 actual U012／L234／S40、原 e=rb4、t_r=1；
X 無 retained r-spoke，actual H_X−s 的完整兩分量 C=`{r}∪L∪S` 與 U 都保留。
r 在 C 上完整 degree4，incident 兩 odd-cycle blocks；任意大小原 pieces、bridges、旁支無上界。
G 仍是具名 ordered induced-C5 disk、完整 Σ=933/941 或全圖 D5 像、ε=2、非相鄰原
degree5 r/s、其餘有效內點完整 degree4、原 H 連通且 full B-touch、原 pieces 恰 U/L/S。
自由孤立內點保完整染色因子，S 不是預設單頂點。
**X=G−e=M 本身**須是固定原拒列 β 的 inclusion-minimal core：每條 retained 非框邊有
同一 β 的 X−f 完整 witness。G 自己的 Σ-critical witnesses 另留，各邊列可不同。

保留同一原圖、同一色框、ordered／shared contacts、actual attachments／supports、ownership、
rotation、bridges、原 edges，以及全部 assignments、tuples／preimages、空 fibres、完整 lifts。
共同十列依序是 `01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`；
q0=01212、q1=01202、q2=01201、q3=01021、q4=01012。
每列保全部16 ordered `(r,s)` pins、diagonal 與 empty cells。原 e 的恢復条件為
`r≠γ(b4)`：q0/q1/q4 的字面色為2，q2/q3為1；T4 列同樣按字面核，不能借未用色。
目前 24 schedules 是必要域，不是來源圖數，不計完整幾何或 t_s=1 的 spoke 變體。

紙面任務 A/B/C 的目標是：對 assigned domain 中**每個符合契約的原來源**，證至少有一個
`γ∈Δ=Q(G)−{β}` 及 ordered pins `(a,b)`，使完整 `L_X(γ;a,b)` 非空且
`a≠γ(b4)`，同步接合 actual C/U 全 preimages 並恢復原 rb4；或直接在同一來源抽取完整
source-minor 矛盾。每個 schedule 一個 Δ 列即可，不要求所有 Δ 列都能恢復。
X 已接受 γ、r 投影非空、鄰列延拓或另一來源的方便 witness 都不足以證 G 接受 γ。
若新增充分前提，須具名標為 conditional，不能宣稱原 assigned domain 全排。

各任務獨立開始，不等待／引用同批其它 worker 的新結論；共用上輪已驗收資料即可。
只新增自己的專屬輸出目錄；若已存在則停下回報 collision，不覆寫。
不得修改共享 docs、原任務交付、舊證書、其他 worker 目錄；不 commit／push／PR，
不發外部訊息。成果全部標 **待獨立驗收**。
缺 `artifacts/c5_no_spoke_exterior/observations.json` 或
`artifacts/c5_single_spoke_residual_locality/observations.json` 的 BASE blob 時保留 finding，
停止依賴該 blob 的有限重播，紙面部分可繼續；physical／quarantine 不替代 BASE 權威。
不重跑上輪19 controls，不作無上限新圖枚舉，不以 zero triggers 宣稱來源排除。

基本交付 `REPORT.md`、`claims.json`、`inputs.json`、`coverage.json`、`delivery.json`。
每個 claim 明列量詞、前提、結論類型、依賴與原 e／r 座標；inputs 分 BASE blobs、封存 audit
SHA256、外部 theorem pins。coverage 列所有 assigned schedule／spoke 變體、完整 Δ、
已證恢復列或 minor、精確 OPEN fibres。未建立 actual source 時不捏造 relations／preimages 數值。
若跑有限控制，先固定具名輸入及上限，保存全部原生 commands／stdout／stderr／exit，
普通／seed17只讀重播一致，負控制與失敗證書保留，輸入／舊證書前後零漂移。
分列紙面、finite calibration、target source、source realizability、Lean、一般 N45/N2/E；
controls 用 `triggered and holds`／`not triggered`／`counterexample`，未執行的 target source
用 executed=false／trigger_count=null。
若未全解，交最小具名 residual、必要空 fibre 與卡住的引理；抽象 relation 反例只否定
該引理，不能稱滿足 K1–K12 的來源反例。完成窄域證明或精確 residual 後停止並交付。

## 本任務精確範圍與目標

原 profile `(t_s,m_s,n_U)=(2,2,1)`；原 s-spokes b0,b2；β=q2=01201。
已採納 `F_C(β)={3},F_U(β)={1},Q(X)={β}`；只負責七 schedules。

**獨立具名入口 T2-Q2-P22：** Q(G)=024，Δ={q0=01212,q4=01012}。
須在同一原圖證至少一列有完整 r≠2 lift。q0 在五份 Δ、q4 在五份 Δ；兩列的完整
恢復引理聯集可覆蓋全部七 schedules，但仍須逐項證來源與 pin 前提。

本任務 β 身份是 q2，**不繼承以 q0 作拒絕 β 的 q0→q1 恢復**。
優先獨立推導 q2→q0／q2→q4 的 full-fibre 搬運與原 e 恢復；也可給同源 source-minor。
逐附件核 L234／S40／U012 的 literal queries、pins、shared-contact constraints，不能只交
X 接受、端點 marginal 或丟 r 的 projection。四色虛擬框界線與任意大小旁支同樣保留。

## 完整 assigned schedules

| Σ orbit | Q(G) | Δ | 真來源全部 X lifts 所需 r |
| --- | --- | --- | --- |
| 933 | 0123 | q0,q1,q3 | q0→2；q1→2；q3→1 |
| 933 | 0124 | q0,q1,q4 | q0→2；q1→2；q4→2 |
| 933 | 0234 | q0,q3,q4 | q0→2；q3→1；q4→2 |
| 933 | 1234 | q1,q3,q4 | q1→2；q3→1；q4→2 |
| 941 | 023 | q0,q3 | q0→2；q3→1 |
| 941 | 024 | q0,q4 | q0→2；q4→2 |
| 941 | 124 | q1,q4 | q1→2；q4→2 |
