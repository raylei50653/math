# N45-U-LP 採納與下一個 singleton-support 窄題

**後續（2026-10-10）：** SS已返回並由[獨立增量／監督採納](../../audits/2026-10-10-n45-ss-supervision/REPORT.md)
在完整契約內排除；與既有U化約及LP合成，指定N45-U身份已全排。
目前窄題見[SS採納與LOW1任務](2026-10-10-n45-ss-adoption.md)。
以下「尚未啟動」及指定pins保存本任務發布時的快照，不表示SS的當前狀態；原任務全文保留。

2026-10-10。PG／PR／PC及PA／PGA／PCA三份獨立增量已限定驗收；
[監督採納](../../audits/2026-10-10-n45-p-supervision/REPORT.md)正式關閉N45-U-LP。
[當前N45權威入口](../c5_excess_two_nonadjacent_unit_core45.md)保留全部前提、信任界與OPEN。
這是任意大小paper＋明列BASE／外部Gallai；19 N2／7整U仍0觸發，4 N1另列校準，沒有新Lean。

原三交付／三稽核的封存不改。原第二批任務頭的九個pins及未啟動文字保留當輪語境，
本輪管理更新的authority具有新hash，見監督的shared-before／management.diff與delivery。
一般N2／E保持OPEN；此後只選N45-U-SS，不另開S LOW／HIGH或graph/k搜尋。

## 1. 下一題的狀態與精確義務

**已備發布文本，尚未啟動。** 不把LP的任務外推論當作SS已驗收。
圖類是唯一原unit unary U、一long mixed L、一singleton-support mixed S，整U省略45／54 core。
S總原incidence至少4；保原U/L盾費(2,2)、(2,3)、(3,2)三種身份。
先核原U盾弧內點不被H−U碰到，再核X自身minimality／degree及唯一實際C；
若足以搬用LP的單-root三分，交該新圖類的完整前提映射與紙面候選，返回後另作獨立增量裁決。

## 2. 可發布的完整任務

```text
任務：N45-U-SS（paper候選，不預先採納）
根目錄：/home/ray/developer/ai/math
BASE：dc8e9aa7d6fccb51f63d30aa3f9c132296d44744
輸出：audits/2026-10-10-n45-u-ss/；若已存在則使用具名新版本並回報，不覆寫。
先核HEAD/Git、BASE HANDOFF/STATUS/DOCUMENTATION，數學BASE依賴對Git objects。
當前authority是新工作交付，不能冒稱BASE blob：
  docs/c5_excess_two_nonadjacent_unit_core45.md
  SHA256：3dd0a492915b5e21d31d862ba8f2c0660250c5d2ded2f075daf54aca8043c942
指定新增paper來源／裁決：
  audits/2026-10-09-n45-pr/REPORT.md
  SHA256：ebcda98bf4f243aaa171d0192724e12690d3565c45fbb6b44b1a738ebcd083da
  audits/2026-10-10-n45-pa/independent-judgment.json
  SHA256：dd647d8e1b09af9b43b3cf5e377ea81afb9fc75f6c38e8192bb5b78841f940ae
  audits/2026-10-09-n45-u/REPORT.md
  SHA256：0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7
  audits/2026-10-09-n45-su-a/independent-judgment.json
  SHA256：97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872
先exclusive-create凍結以上必要輸入/hash；BASE數學依賴另凍結原blobs。
沿已採納U-WIT/U-S3/U-U2/U-SHORT/U-RES及LP/PA的明列前提，閱讀原shield §2、
unattached-boundary §1、no-spoke§4、single-spoke-four§1–5、two-spoke-three-contacts§1–5。

量詞：所有任意大小有限簡單disk原G；ordered induced C5 B是外面，完整Σ933/941或整圖共同D5像，
每非框Σ-critical、ε2、有效H連通/full B-touch；恰兩非相鄰原degree5 roots r,s，其餘完整degree4。
H−{r,s}完整分量恰唯一原unit unary U及mixed L,S；各one-sided、support非空、mixed兩側incidence正。
U唯一原contact rx，X=G−V(U)=M是原拒絕literal β的inclusion-minimal45/54 core，r降度。
L actual support long；S actual support恰一個原框點，總原root incidence≥4。
保同一原圖的具名ordered/shared contacts、全部attachments/support/ownership、bridges/rotation、
同一literal色框、完整tuples/fibres（含空）/全部full lifts；D5/root swap只能搬整圖。

優先義務：
1. 從原U-WIT與原盾費核(U,L)=(2,2)/(2,3)/(3,2)，不要偷用pair S的2+2+1分割或U/L恰三點support。
   逐項核原shield restriction對U盾弧內點的適用性、原F_U面及H−U連通。
2. 在X恰整U省略且繼承T4下，分別處理原σ_U長2／3的全部內點；
   只有原附件真的禁止保留內點碰到時才用同圖改色，不假設X full B-touch。
3. 核X=M自身β-edge-minimal、r完整degree4/s唯一完整degree5、C={r}∪L∪S實際唯一連通分量。
   明寫全部原邊、完整C relation接合及shared單坐標；不收縮替換coloring，不逐列選另一source。
4. 若上一鏈迫β=q_m，將原spokes、5−t_s個互異contacts與F_C精確搬到BASE(5)/(4)/(3)三分。
   核t0不需外部s–B路、t2任意異色位置與全部theorem前提，保933 q2及整圖搬運。
5. 若有缺口，交最小精確lemma義務與反例/缺失前提停止；若成功，只交N45-U-SS新任意大小paper候選。
   可另列更弱一般lemma，但每個量詞及全部充分前提必須明寫，不自動關全部U/N2/E。

不用跨列加容量；不先枚舉新pieces或擴graph/k、不重開U1–U4、singleton總incidence≤3或LP。
PC的LP schema不適用本singleton S；其not-triggered結果不能當SS排除或正控制。
有限控制若沿用既有來源須保完整原edges/witness/rotation並另列coverage；沒有控制不補造來源。
不 import其他worker checker作新paper證明；若新finite計算有必要，另交checker/certificate與normal/seed17只讀重播。

只寫自己的fresh輸出：REPORT.md、inputs.json、逐claim量詞/全部前提/依賴/證據層/coverage/未涵蓋/finding、
checks.json、逐命令exit/log、MANIFEST與delivery；新檔exclusive-create。
不改共享authority/guide/STATUS或其他worker/舊證書，不commit/push/PR/對外訊息、不委派subagents。
歷史E4 provenance FAIL、fresh BASE兩缺檔、whole-worktree duplicate IDs分列保留。
無新Lean/source實現宣稱。paper候選返回後由監督另作独立增量稽核與正式採納；不自行選下一residual。
```

發布僅指任務文本已準備，沒有啟動worker、外部訊息、commit或push。
