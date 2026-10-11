# N2 九格原表的結構統一與原55必要身份

2026-10-11。只讀基準 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
本分工僅寫此獨占目錄，沒有改既有文檔／腳本／certificate，沒有 commit／push。
證據層是既有紙面結果的適用性核對及新紙面候選；沒有新來源圖、有限來源排除或 Lean theorem。
原55、完整 N2 來源排除與 E-ARC2／三點弧保持 **OPEN**。

**本分工最後的較強共同引理見 [HUB_LEMMA.md](HUB_LEMMA.md)。**
原 singleton-support mixed 若存在，必有 u=t=0；證明使用原 bags
`r∪U,s∪Q,B`（有U）或 `r,s∪Q,B`（有root-spoke）及已採納 hub 定理。
它直接排 u=2，並收窄兩個 u=1 子型的 actual supports。
下文 §4 保留先形成的較繁 u=2 候選，最新提交審核的是該共同引理。

## 1. 「九格」精確對應與現況

使用者已向父端確認，九格是 E4 §4.3 的三個 relation 族乘三個 core 層，
不是九份具名來源，亦不是 HEAD 的九個存活分支。
`artifacts/c5_excess_two_e4/REPORT.md:279-288` 的族為：

| relation 族 | 參數 | 兩-root44 | 45／54 | 原55 |
| --- | --- | --- | --- | --- |
| A：兩 long mixed | `(ell,u)=(2,0)` | 已有完整目標域覆蓋 | 已有完整目標域覆蓋 | OPEN |
| B：long／short，可能一 U | `(1,0),(1,1)` | 已有完整目標域覆蓋 | 已有完整目標域覆蓋 | OPEN |
| C：兩 short，加 U | `(0,1),(0,2)` | 已有完整目標域覆蓋 | 已有完整目標域覆蓋 | OPEN |

所以原九格現有六格已被後續完整契約覆蓋、三格原55保留；參數展開得到五個
`(ell,u)`，這不把族數改寫成五個已實現來源。E4 本身在 `269-272` 明示原表保留當時的
三列前提，限定後續結論不能無條件搬回整表。
本次採用的新統一依據是 `docs/c5_excess_two_arc_spoke_closure.md:219-233`：
在 §1 **完整** N2 目標前提下，每條非框邊刪除全收，每個原拒絕列的唯一有效
minimal core 是原 G 本身的55。這已取代目前目標域內對六格真 core 的逐案路由。

## 2. 全族共有的不變量與域界線

以下都只在 `docs/c5_excess_two_arc_spoke_closure.md:24-40` 與
`docs/c5_excess_two_arc_size_bound.md:25-33` 的完整來源契約內使用：
指定有序 induced C5 disk、完整有序 Sigma=933／941 或整圖共同 D5 像、全部非框邊
Sigma-critical、epsilon=2、有效 H 連通且 full B-touch、兩個非相鄰原 degree5 roots、
其他有效內點完整 degree4、原 H−{r,s} 恰兩 mixed 加 unary、one-sided，兩 mixed support 非空。
共同搬運之後 q0=01212、q1=01202、q3=01021 同時拒絕。
不能把這組完整 Sigma 結果搬到一般只拒絕三列的圖或 932。

| 已證不變量 | 精確依據 |
| --- | --- |
| 每份原 C 刪除全收；三列外部染色各使同一 C 的 degree lists 不可染 | component_slack `154-168`；spoke_closure `56-68` |
| 每條原非框邊刪除全收，所有拒絕列以原 G 自身作55 core | spoke_closure `219-227` |
| 包括 roots 在內，每個內點至多接兩個相鄰框點；root 內度至少3、其他內點至少2 | spoke_closure `229-233` |
| H 是共同中央二連通 block 加至多兩個 root 葉 blocks；U 與葉 blocks 一一對應；u=2 owners 不同；H 無 bridge | size_bound `48-71` |
| 每份原 C 是 bridges／奇環的 cactus（或 singleton）；root incidences k_C 至少2 | size_bound `120-132`；spoke_closure `122-131` |
| 內度2點 D 到五條原框邊的附件映射單射，故 |D|≤5 | size_bound `79-118` |
| 原長支援／unary 盾弧長至少2，short pair 長1、singleton 長0；原盾邊互斥 | E4 `274-286`；unary_shield_budget `101-110,117-142` |
| 三列共同 palette 使同一原 cycle 的普通私有點有同一實際框邊 | spoke_closure `70-88` |
| 原55的有效大小至多35−6u−3t，t是兩 roots 的原框邊附件總数 | size_bound `173-192` |

所有不變量保存同一原 G、同一有序框、ordered／shared contacts、actual supports、
ownership、rotation、bridges、原 pieces 及完整 relations／空 fibres／full lifts。
三列的外部 witness pins 可以不同，不能要求它們相等或取其邊际乘積。
精確整圖 joint 仍是 E4 `315-336` 的
`J_G(beta)=(E_r(beta)×E_s(beta)) intersect A_P(beta) intersect A_Q(beta)`。

立即可得的共同參數限制：

- 每 root 原框附件≤2；帶 U 的 owner 在中央 block、葉 block 各至少兩個內鄰，
  故 owner 框附件≤1。因此 `0≤t≤4−u`。
- 每份 C 的 k_C≥2，且 sum k_C=10−t，所以 `t≤6−2u`。
- 設 p 為 short pair 的份數，則 `2ell+2u+p≤5`。此式只計原幾何盾費，沒有跨列相加禁色容量。

## 3. 可跨 core 身份使用的 singleton mixed 引理

**已採納來源引理的適用性。** 若原 mixed P 只有一個 actual 框支援點 h，則
`k_P=k_P^r+k_P^s≥4`。

一個直接來源 proof 是 `audits/2026-10-09-n45-u/REPORT.md:176-205`：
量詞是任意兩-root disk 的原 degree4、one-sided mixed、full B-touch、原 critical contact；
`179` 明說不需兩-root44、T4 或指定 beta，也沒有45 derivative minimality前提。
其結論 k≤3⇒support≥2 可直接反推上述必要條件。

亦可核回 S04 的局部完整 relation proof（`audits/2026-10-09-n45-s/REPORT.md:126-144`）：
固定 c=beta(h)，固定 c 的共同 S3 色置換保持 P 的完整局部存在性。
N-diagonal（E4 `236-255`）包含全部 `(a,a)`，非 diagonal forbidden pairs 只可能是
以下三個完整 S3 軌道的聯集：

| forbidden orbit | 每列／欄容量需要 |
| --- | --- |
| `(c,b)`, b≠c | k_s≥3 |
| `(a,c)`, a≠c | k_r≥3 |
| `(a,b)`, a,b≠c 且 a≠b | k_r≥2 且 k_s≥2 |

兩側 positive 且總 k≤3 排全部三軌道，所以對每個 proper literal beta，
`A_P(beta)=[4]^2`。由分量必留，全收的 G−P 有每列完整外部染色，因為 P 接受其
實際有序 pins 就可補回原 G，矛盾任一 q0 拒絕。這只是局部色置換的存在性雙射，
補回時仍用原 beta／pins／完整 lifts。
因此沒有從 exact-S 的欄飽和前提偷偷推一般原55的結論。

## 4. 新候選：兩 unary 的原55來源也不可能

以下是新紙面候選 **N2-55-U2-HUB**，需獨立核對後才可接入父端成果。
它不排一般原55，不關閉三點弧。

假設完整 §2 來源另有 u=2。

1. 兩 U 各占至少兩條盾邊，故 ell=0、兩 mixed 中至少一份 singleton support。
   記 singleton 為 P。§3 給 k_P≥4；兩 U 各 k≥2，另一 mixed Q 的 k≥2。
   `sum k_C=10−t` 因而迫 **t=0、k_P=4、k_Q=2、兩 U 各 k=2**。
   兩 U owners 不同，每 root 還有兩份 mixed 的 positive incidences，故
   `k_P=(2,2)`、`k_Q=(1,1)`。若 Q 也 singleton，§3 要 k_Q≥4，矛盾；
   故 Q 是真 short pair。
2. 兩 U 盾長與 Q 盾長分別為2、2、1，恰用五條原框邊。
   整圖共同旋轉／反射並必要時交换 roots，得到
   `S_Ur=012`、`S_Us=234`、`S_Q=40`。
   盾弧內點排除了 P 接1、3，所以 `S_P={h}`、h∈{0,2,4}。
3. 若 h=0 或4，取原 K3,3 的六 bags：
   左側 `P,Q,O=(B−{h}) union Ur union Us`，右側 `{r},{s},{h}`。
   P、Q 都連通，O 中 B−h 是框路，兩 U 各有 B−h 附件，所以 O 連通。
   三右 bags 各 singleton，六 bags 互斥。
   P/Q 均有原 r、s contact 與 h 附件；O−r、O−s 分別來自兩 U；
   O−h 來自原框邊。全部九個跨側鄰接成立，違 disk planarity。
4. 故 h=2。取 P 外的三個原 hubs
   `R={r} union Ur`、`S={s} union Us union Q union (B−{h})`、`T={h}`。
   R 連通；S 由 Q 接 s 及 B−h，另接 Us，亦連通；三 hubs 互斥。
   R−S 有 Ur 到框0或1的原附件；R−T 有 Ur 到框2的原附件；S−T 有原框邊。
   因 P 是原 H−{r,s} 完整分量且 support 只有h，三 hubs 覆蓋 N(P)，其與 N(P)
   的交集恰是 `{r}`、`{s}`、`{h}`。
5. 任取一個原拒絕 proper 列 beta（與上步整圖 D5 一起搬運）；分量必留給 G−P
   一份 beta **完整**染色 psi；它不可補 P，否則原 G 接受同一 beta。
   依 psi(r)、psi(s)、psi(h) 把同色 hubs 合併；原三 hubs 兩兩相鄰，
   合併後仍互斥、連通、兩兩相鄰，至多三份，且 psi 在每份與 N(P) 的交集
   上為常數，各份的常數互異。這完全符合
   `docs/c5_unary_shield_budget.md:155-179` 的已採納 hub 定理 B。
   P 原連通、每點完整 degree4、psi 為不可延拓的外部染色，故定理給原 G 的 K5 minor，矛盾。

此 proof 未重染完整外围，也沒有宣稱收縮圖保 Sigma；hub 色条件只在 N(P) 上判定。
各 branch set 都是同一原圖的集合；原 q0 witness 保持其全外部座標，沒有跨列拼色。
若独立驗證接受，C族的 `(ell,u)=(0,2)` 原55子型可排，五個參數情形縮成四個，
原表仍是三 relation 族 × 三 core 層，餘三格原55名稱不可因此誤寫全 CLOSED。

## 5. 共同引理的完成與缺口

**已證共同化約：** 完整目標 N2 的任意反例是一份每條非框邊刪除全收、三列共同拒絕的
原55圖，H 的 block 骨架、全附件限制、cactus／五個 D 限制及大小界同時成立。
這條共同必要結構引理已把真 core 的六格路由统一。

**新候選共同 hub 條件：** 若某 singleton-support mixed P 的三個外鄰身份
`r,s,h` 能分别裝進互斥、連通、兩兩相鄰的原 hubs，則它不可成為來源必留分量。
proof 正是 §4 第5步，可合併同色 hubs，毋須跨列 pins 相同。
這個條件在 u=2 的逼定幾何下足以排唯一殘留位置 h=2。

**仍缺的結構：** u=0 或1、long／short 混合及剩餘兩short情形，現有資料未保证
所有原件的外鄰可作上述 clique hubs；其他 support 的框鄰需更多坐標／hubs。
共同大小界亦未給同框跨列的 J_G 非空，或必有某原非框邊刪除仍拒絕。
三點弧命題若已證會直接排除 target 三個非連續拒點，但它就是上位 OPEN 目標；
不能借其結論當本次缺失的附件／hub 结构前提。

## 6. 核對與保留界線

- 核對文件／原表／新定理的量詞與行號，没有調用 Graphify：現有文檔足夠說明依賴。
- 新候選保留具体六 bags／三 hubs 及全部鄰接来源供獨立審核。
- 尚無完整 Sigma933／941 target 來源 control；既有 finite controls 的零觸發不作来源排除。
- 本分工没有重跑既有 checker、沒有新有限枚舉或 Lean proof，亦没有把界內未搜到變成任意大小 theorem。
- 在独立驗證完成前，N2-55-U2-HUB 只為紙面候選；原55與 E-ARC2 均保持 OPEN。
