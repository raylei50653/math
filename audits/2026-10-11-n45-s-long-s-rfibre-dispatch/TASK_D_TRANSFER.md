# 任務 D：原 C block-tree 的完整 assignment／r-fibre transfer

任務 ID：`N45-S-LONG-S-BLOCK-TRANSFER`。
專屬輸出：`audits/2026-10-11-n45-s-long-s-block-transfer/`。**本輪可獨立並行；成果待獨立驗收。**

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

這是三份 paper 任務的獨立輔助工作，不負責任何 schedule 的來源排除，不必等 A/B/C。
任意大小 recurrence 的正確性只依 actual block decomposition 與字面附件；
K11/K12 是提升成來源結論時另需的義務，不是該接合恆等式的前提。

1. 寫出任意大小 actual C block-tree 的精確 restriction／union recurrence：原 bridge、任意長
   odd cycle 各有局部規則，在 actual cutvertex 接合全部 assignments。保原 r 上兩 odd-cycle
   blocks、L/S 身份、所有完整 degree4 旁支與 actual B/s attachments。證與 C 所有 proper
   assignments 有雙射，保存各 ordered contact tuple 的全部 preimages、r 色與空 fibres。
   不要求 finite-template compression，不可把存在性或可用色集合當完整介面。
2. 每個共同 literal γ 產生完整 C interface `Λ_C(γ;a,b)`（含避 actual s-contacts 的 pin b），
   全16 pins與空 cells。精確說明何時可接 actual U 全 preimages／s-spoke factors，及原
   rb4 的恢復 filter。若 finite case 未提供 actual U/G，whole-X/G/source coverage 明列未觸發，
   不用抽象 U 代替來源。跨列必出自同一原 C／附件；piece 色搬運返回字面框再接合。
3. 計算前宣告至多8個具名 interface microcases，每個至多11個 C vertices；包含 r 上兩
   triangles、triangle+5-cycle、非根 articulation 的 bridge／odd-cycle 旁支。
   逐點核 `deg_C(v)+|N_B(v)|+1[sv∈E]=4`，包含 r；提供 vertices、original edges、
   attachments、contacts／ownership、L/S、rotation（若未驗 disk topology，明列）。
   若某預宣告 case 不合條件，保存失敗 case／原因，再用新名稱更正；總数仍≤8。
   不將不合條件的圖偷偷刪除後再宣稱覆蓋。
4. 另寫無 transfer/checker imports 的直接原邊枚舉，逐項比全部十列的 assignments、
   tuple/preimage、ambient pins／r fibres及原旁支頂點。case 形狀／degree4不建立Σ-critical
   或 X 同β minimal；未供 K11/K12 完整刪邊 witnesses 時保持 `not triggered`。
5. 指定三個負控制：改一份完整 preimage 的 r 色、刪一個空 ambient fibre、漏一個原旁支。
   驗收器須分別拒絕並指出 named cell／原頂點；留原證書及失敗證書。普通／seed17只讀重播
   一致，authority／舊證書前後零漂移。這些 controls 驗 transfer，不是 target source search。

另交 `transfer-proof.md`、唯讀 checker、independent direct enumerator、`cases.json`、
完整 certificate／negative certificates 與原生命令 logs。基本交付與共同界線照上文。
成功止於任意大小精確 recurrence＋具名介面校準；若較強 cross-row fibre lemma 失敗，
交完整 relation 反例與精確失敗前提，不提升為滿足 K1–K12 的來源反例。
