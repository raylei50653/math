# 至多三條精確橋接候選

共同輸入為本輪 [REPORT.md](REPORT.md) 的 same-source contract。A 未通過；以 SD-A 從一般二連通 core 取得內度2的結論一律 conditional。下列候選若直接明設內度2及其實際 block 形狀，其自身證明可以不依 A。

| 候選 | 最弱已知充分前提／輸出 | 反例壓力 | 可能消除的身份 | 尚缺與停止點 |
| --- | --- | --- | --- | --- |
| **BR-SD-1（選定）：三奇環鏈的單一環間 bridge → R27** | 無 U exact-S long／真pair short；M自身 β-minimal、T4、唯一s度5，其餘4；s內度2，C三個odd blocks，J1/J2共用r，J2/J3由唯一原bridge uv連接；兩原s-contacts經原外臂各到末端私有點。給 boundary固定、互斥連通的實際branch sets到R27 domain，保目標degree與四個s色的精確F={D}、重建β-minimality；合成來源非平面minor | uv兩端各完整度4，裸收縮後合併點完整度6；刪兩條附件的list效果必須證。R23 root relation負控制、R20兩點pin負控制禁止把縮環／縮bridge當完整lifting等價 | 無U LS-pair 45／54中此三oddblocks／singlebridge subset；不涵蓋更多cycles、第二條環間bridge或非二連通旁支 | 缺單bridge的原附件／forcing與branch-set構造。成功：任意環長／原臂下取得來源非planarity。失敗：保留最小具名原邊及完整query/刪邊witness的失敗步驟，停於該bridge obstruction；只剩list或布林等價不得宣稱排除 |
| BR-SD-2：無U兩long的二連通適用橋 | 同一G/X=M的精確兩long來源；從其原Σ witnesses及M同β witnesses證H_M沒有P/Q內部割點。最弱充分輸出是對每一具名內部點a，H_M−a仍連通；再用本輪star預算＋A | β-minimal本身不推出二連通；literal割點控制及保留unary的具名反例。沒有actual兩long來源不能把未找到割點當作證明 | 若橋接真，A通過後可關精確noU兩long full identity；橋接前只条件排二連通subset | 缺source-level cut支分配與完整branch relation argument。若找到full-contract source割點，保原rotation/attachments/lifts，停止在非二連通分支；若controls零觸發，unknown |
| BR-SD-3：無U LS-pair profile22的單列原spoke恢復 | 原r唯一spoke e，(r contacts L/S)=(2,2)、s各1、s三spokes，M=X=G−e同β minimal；選一個實際γ∈Q(G)∖Q(X)。最弱充分輸出為同圖 `∃φ∈L_X(γ), φ(r)≠γ(b_i)`；原邊過濾後即完整G lift | fixedβ F={D}、存在一個root pair、root marginals、四列縮環都不足以取得γ的r escape。R23／R20及本輪full-lift投影負控制 | 至少排產生此完整escape的字面profile/schedule；不保其他profiles／所有γ | 缺targetγ的完整fibres非空及literal inequality；成功只以全部原點assignment恢復e。反向若source全部X lifts都鎖r=γ(b_i)，保證據停止；toy鎖色不是來源反例 |

選 BR-SD-1 的原因是它只補一個實際 graph operation 到已採納任意大小結果；不要求先證全部 OPEN cores 二連通，也不要求一般跨列 escape。其A獨立的proof input明設實際內度及block域。BR-SD-2涵蓋整個source-level cut问题，BR-SD-3還需跨列完整fibres，均較寬。

BR-SD-1 還有 palette 壓力：固定β、s=D的原tight Gallai assignment在uv上有singleton palette `{c}`；兩相鄰cycle palettes各是避c的二色集，所以必相交。裸收縮並保原palette錨點，再刪兩B附件把degree6降4，merged list是Col而兩palette聯集≤3，可能使原拒絕D變可染。必須證合法實際attachments／錨點處理；不能當作已知兩互補palettes的R27共用點。

R27引用方式的精化：候選表的「R27 domain」指 **R11定位後R27的正常形／minor合成前提**。原M的T4先證指定框弧；來源minor保同一區域，目標逐項進入R25／R26 forcing-list域、三shared cycles、末端私有contacts／arms、T–S–T palettes及actual錨點，再核degree與四queries／βwitness。單憑region＋F＋degrees不足以省掉palettes或actual branch sets。後續minor不需保持全部T4；若以R27首頁定理對目標作黑盒，則須另證target T4，不得把它視為已繼承。

本輪未執行這三個後續證明；沒有把候選改標 adopted。若後續發現 BR-SD-1 已被某份既有原minor構造完全涵蓋，直接記錄精確mapping，報新增涵蓋0並停止，不開下一個更寬問題。
