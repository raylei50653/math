# N45-PGA：PG 任意大小幾何獨立 paper 稽核

2026-10-10；BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
僅審 N45-PG，判定先以 exclusive-create 封存於
[independent-judgment.json](independent-judgment.json)，再交付父監督。
未讀 PR/PC 結果或本批監督新判定；不做新研究、擴 k、來源枚舉或再次委派。

**判定：PG-01、02、04、05 成立且可在明列原 LP 前提內搬用；PG-03 的原路/Jordan/bridge identity 成立，八張 embedding 限抽象必要 minor 控制；PG-RES 的 56 整數 profiles 是必要身份。未發現這些窄 claims 的新 paper 缺口。**
新排除只含 **edge-pair 支援且整份 S 恰一個頂點**。
任意大小 `|S|≥2` 的 N45-U-LP 仍 OPEN，沒有完整 LP source control、來源實現或全部 LP 排除。
本判定的 universal paper 證明不以有限控制零觸發為依據。

## 1. 凍結輸入、BASE 与明示信任界

[inputs.json](inputs.json) 記23份輸入、來源路徑、bytes、SHA256與BASE blob IDs。
必要新頁/任務/U/SU-A輸入取自 worker 已凍結 bytes，並核其宣告hash；沒有將未提交新頁稱為BASE blob。
指定 worker [REPORT](frozen/pg/REPORT.md) SHA256 為
`f67da4360ca729bf14a6d04b8a9e62041c5824d3b9734bacaf145a445008584f`，
[certificate](frozen/pg/certificate.json) 為
`75544f2ba3aec74e8c4ccb2f51a42f5fb022009f4a864d76d2d73a2064efd30d`。

BASE依賴從 `git show BASE:path` 取得；重新核bytes与`git rev-parse BASE:path`：

| 原依賴 | Git blob | SHA256 |
| --- | --- | --- |
| [原盾弧 §2](base/docs/c5_unary_shield_budget.md) | `e5a33eac848a4179bd00e20965361a4d1e8c5022` | `c4039e805abcc94a6a8c824ba38e5858420535c5c5528e3bf43aec5721c8e082` |
| [Phase B B-S0/B-C2](base/docs/c5_phase_b_common_lemmas.md) | `a4a743ba081b3c4910d6fcd24a0beee522eb622b` | `6798d5b2a9cb137bfb82a9873d1786ed782a8eea3c1163b443bc52d722c1bc8a` |
| [E3 nonadjacent §3/5](base/artifacts/c5_excess_two_e3/nonadjacent_notes.md) | `57f57e2857aadf022860193509bc2db359d14b0e` | `5ef7008a28c58de5d0299eeecee64e139c3b99a3d82027c38d8f5a121510db4f` |
| [E4 §4/6](base/artifacts/c5_excess_two_e4/REPORT.md) | `13a892c92a1a11aa182a9a9d82a24cb3377d0d75` | `bb0f4be0ef300e1ecb3ff0e417996f744bccbb65dc32b8f8aaaa843ff054a0fc` |

BASE HANDOFF/STATUS/DOCUMENTATION及初始Git state亦保存；主工作樹既有四份tracked修改不作本審閱數學依賴。
本次使用 Math handoff skill 的證據分層與窄停止點規則；父任務明示限新目錄，故不改共享導航/worker/舊證書。

量詞為任意大小有限簡單原 G：ordered induced C5 B 為disk外面；完整Σ=933/941或整圖共同D5像、非框Σ-critical、有效H連通/full B-touch/ε=2；
恰非相鄰原degree5 roots r,s，其餘有效內點原degree4；H−{r,s}完整分量恰U,L,S。
U唯一原unary、唯一contact rx/owner r；X=整份G−V(U)=M為原拒絕literal β的inclusion-minimal45/54 core，r降度。
L原actual support long，S原actual support真框邊兩端。
原contacts/shared單一坐標、附件/support、ownership、rotation/bridges、完整tuples/fibres/空fibres/full lifts始終保留。

**只當明示已採納信任界的SU前提：** [權威頁§1–3](frozen/trusted/docs/c5_excess_two_nonadjacent_unit_core45.md)、
[U WIT/CAP/RES](frozen/trusted/audits/2026-10-09-n45-u/REPORT.md)、
[SU-A採納范围](frozen/trusted/audits/2026-10-09-n45-su-a/independent-judgment.json)的原逐contact witness、2+2+1五盾邊分割、U/L連續三點支援、
coreβ retained spokes同側色互異、E_s非空、每個b∈E_s兩mixed raw columns滿額互斥分割E_r^X/五項零slack、Δ singleton forcing及七格Q(X)/933 q2。
本輪沒有重證上游分類或把SU裁決當新PG proof；PG新幾何與slack步驟在下文獨立推導。

## 2. PG-01：named partition／outside

選 S 的真框邊後，餘四框邊成一條路；兩份具名連續二邊盾弧U/L只可依兩種次序切分。
故5×2=10份，恰一whole D5 orbit。取U/S共用端點為a、方向d=±1，得到
U=(a,a+d,a+2d)、L=(a+2d,a+3d,a+4d)、S=(a+4d,a)。
將**整圖**、U owner、所有ports/rotation、Σ/β同步搬成U012/L234/S40；root交換同樣搬全部原物件。
β(b0)=β(b2)時r02雙spoke受原β-minimality色互異限制，不能另獨立canonicalize拒絕列。

刪L仍有S的原r–s路，刪S仍有L的原路；U只接r，所以H−P均原連通。
原roots在每個K_P的同一open face F_P；其框邊恰E(B)−σ_G(P)：U為23/34/40，L為40/01/12，S為01/12/23/34。
這只列框邊身份，不有限化其他原face邊界。原盾弧引理1(c)禁止H−U接b1、H−L接b3；
不同open faces閉包可共用框點/路段，沒有錯用閉包互斥。

每條原contact e之Σ-critical給自身γ_e与G−e full lift；限制到G−P是合法outside。
若可接回完整P便使原G接受γ_e，矛盾。γ_e可以不同於β及別條e的γ；原幾何共同，禁色不跨列相加。
若原U短，原full B-touch補弧點h只能由H−U碰到，原H−U連通給避U/B的r→h路；未假定X full B-touch。
**判定成立**；不涵蓋singleton-support或缺原one-sided/witness/附件的資料。

## 3. PG-02：三組原K3,3的六袋及27條原邊

寫u0/u2/x為U原附件/contact端點，l3/l4/lr/ls為L原端點，v0/v4/vr/vs為S原端點。
同一piece中端點可shared，三piece頂點集原互斥；B/r/s原互異。
每份整piece只入一袋，故任何shared identity都不會把兩袋合併。

| 假設原spoke | A1/A2/A3 | B1/B2/B3 | 額外原bag連通邊 |
| --- | --- | --- | --- |
| rb4 | U；{b4}；L∪{s} | S∪{b0}；{b2,b3}；{r} | sls；b0v0；b2b3 |
| sb0 | U∪{b0}；L；S | {r}；{s}；{b4} | b0u0 |
| sb2 | U∪{b2}；L；S | {r}；{s}；{b3,b4} | b2u2；b3b4 |

整piece connected，表列原邊連接加入的框點/root，六袋均原connected/disjoint。
全部九個A_i–B_j的**原邊**如下：

| 假設 | A1對B1/B2/B3 | A2對B1/B2/B3 | A3對B1/B2/B3 |
| --- | --- | --- | --- |
| rb4 | u0b0；u2b2；xr | b4v4；b4b3；b4r | svs；l3b3；lrr |
| sb0 | xr；b0s；b0b4 | lrr；lss；l4b4 | vrr；vss；v4b4 |
| sb2 | xr；b2s；b2b3 | lrr；lss；l4b4 | vrr；vss；v4b4 |

每條均由actual support/contact、原框邊或所假設原spoke給定；沒有outside apex或補rs。
故三行各給原K3,3 minor，與平面性矛盾。
加PG-01盾內點禁附件，得 **N_B(r)⊆{b0,b2}，N_B(s)⊆{b4}**。
只需這些原connected sets/edges及平面性，不需degree4/Σ/β/criticality/core。
**判定成立**，任意大小與shared contacts均覆蓋。60份symbolic模板只是逐項控制；contraction沒有作coloring replacement。

## 4. PG-03：原Jordan／bridge与八張abstract embeddings

任取L的一条r-或s-contact，在原L中接至另一root的某contact端點取simple路；shared端點時內路長0仍合法。
加兩條原contacts得長至少2的r–s路；原S亦然。兩路內部互斥並避B，只交r/s，合成長至少4原simple cycle，於原plane graph為Jordan curve。
任一mixed root-contact皆可照此選路納入cycle，故不是H bridge。
U唯一原H contact為rx，刪rx恰隔完整U與原connected H−U，故rx為H bridge；未由此宣稱它為G bridge。

原piece取spanning tree、保所需代表附件/contact而收縮，所得simple skeleton是原graph的必要minor。
worker八張disk embeddings供一組可平面嵌入的abstract skeleton/optional spokes控制，dart/rotation/Euler與B外面可核。
**不把列出的canonical faces宣稱為原graph全部faces或唯一embedding**；
原multiple ports/shared identity、內部faces/private bridges、全部rotation與十列relations都未被小圖保存。
沒有source-to-finite normal form，也不由八張圖宣稱來源存在。
**原path/bridge claim成立；八圖仅接受為抽象有限必要層。**

## 5. PG-04：任意大小strict-slack獨立推導

最弱充分前提為原P connected、每點完整degree4、所有外鄰在B/r/s、proper literal β、E_s非空，且每個b∈E_s完整raw G_P(b)非空。
LP採納U-CAP供|G_P(b)|=k_P^r≥1；需是**raw完整column**，不是僅一個E_r截面或端點marginals。

假设原v同接s与h∈B，且β(h)=b∈E_s。固定任意local pins r=a,s=b。
原list刪去每點全部實際外鄰色；每w有|L(w)|≥deg_P(w)。
v的兩個不同原外鄰s,h同色，故不同禁色數≤4−deg_P(v)−1，
所以 **|L(v)|≥deg_P(v)+1**。
以v為根取原spanning tree，後序先染非根：未染parent使每非根最多deg_P(w)−1已染鄰點；最後v用strict slack。
每個a均得到整份原P的合法lift，故raw G_P(b)=∅，違反非空。
這個local greedy argument不要求a能填入全部outside，更不聲稱每a有X或G全圖lift。

因此原s-contact的每條B附件h必β(h)∉E_s。
X無unary且PG-02給s只可能sb4，所以無spoke時E_s=Col、所有s-contacts無B附件；
恰sb4時E_s=Col−{β(b4)}、所有s-contact附件色必β(b4)。
proper β(b0)≠β(b4)且β(b3)≠β(b4)，故S的s-contact永不接b0，L的永不接b3。
L接b2僅在sb4存在且β(b2)=β(b4)時未被此条件排除；這不是附件存在定理。
無sb4時shared r/s contact無B附件、internal degree2；僅s的contact無B附件、internal degree3，均原degree4算術。
**判定成立**，無需有限化約、Gallai新分類或marginals拼接。

## 6. PG-05：edge-pair的單頂點S

若整份S={v}，原mixed/actual support40迫rv,sv,b0v,b4v四條不同原邊，已用完原degree4。
v是s-contact且接b0，違PG-04；β(b0)在s無spoke與只sb4的E_s中均存在。
亦可直接看原v palette：b0/b4 proper異色留兩色；s=β(b0)無新禁色，每個r=a最多再禁一色，所以完整raw column空。
**窄排除成立**。12種support色賦值/16pin local lifts是固定局部oracle；不是完整原LP source。
這個S的**頂點數一**和**support只有一框點**是兩個不同前提；singleton-support分支不被排除。

## 7. PG-RES：56的量詞及尚缺的來源義務

原roots degree5、rs不存在、唯一原U incidence1给
k_L^r+k_S^r=4−t_r、k_L^s+k_S^s=5−t_s，四k正。
r allowed sets∅/0/2/02的正split數为3/2/2/1；s的∅/4為4/3，故共有(3+2+2+1)(4+3)=56。
这是加literal β相等限制、actual port/degree/rotation、完整relations及source existence前的必要整數data。
**56不是survivors，也不是56個source**。例えばβ(b0)=β(b2)時原β-minimality已禁止r02。
L若單頂點需三個B附件加兩roots五邊，違degree4，所以|L|≥2；PG-05另给|S|≥2。

完整LP source仍缺：同一原G的全部具名頂點/邊/附件/ports/shared坐標/ownership/bridges/rotation，
完整十列Σ933/941及每非框原critical full witness，X恰整U省略/β-minimality，
coreβ全部逐欄滿額互斥與所有Δsingleton forcing，七格Q(X)及933 q2。
本輪没有任意大小正常形或source realization，不能以模板replay填補这些原graph义务。
[PG residual](frozen/pg/residual.json)的N45-PG-OPEN-PORT仍OPEN；只允许传播上述窄必要条件及|S|=1排除。
一般U/N2/E、singleton-support、S其他身份、原55/其他core、单root及ε≥3均未覆盖。

## 8. 檢查、封存與保留失敗

[checks.json](checks.json)逐命令exit/log；[independent_check.py](independent_check.py)不import worker，
只读核23份freeze、四BASE數學依賴、十named partitions、三组27原邊模型、60模板、8抽象embedding、56正整數profiles及48局部r-pin賦值。
任意大小proof由§2–7承擔，不由此script或零source控制承擔。

| 實際檢查 | exit／界線 |
| --- | --- |
| worker普通与seed17，僅在本目錄frozen副本`--check` | 各0，178691bytes exact-byte SHA吻合 |
| 獨立普通与seed17 | 各0，stdout逐byte相等；不寫任何原worker檔 |
| frozen worker重新生成exclusive guard | **1，FileExistsError**，保留stderr；certificate未被改寫 |
| 本inputs.json的exclusive-create guard | **1，FileExistsError**，保留stderr；input freeze未覆寫 |
| 主worktree `git diff --check` | 0；原既有tracked變更仍存在，不推clean或本審閱ownership |
| 最終input漂移／audit文字、JSON、連結檢查 | 見checks.json中的實際exit及logs |

第一次audit-integrity為**exit1**：包裝順序使checks.json尚未建立便先核其連結，失敗log原樣保留。建立checks.json後另跑audit-integrity-v2；最終結果記logs及delivery。這是交付包裝錯誤，不是paper finding或數學反例。

新facts没有Lean source/theorem/native_decide；`lake build`未跑，不能称新PG形式化。
上游S/U/SU有限控制、E3/E4大枚舉、全工作樹DocGraph/正式docs未重跑；本次只新增隔離審閱。
worker保留的兩歷史E4 provenance FAIL、fresh BASE兩歷史缺檔、whole-worktree duplicate IDs仍分層保留，未改history或声称全工作樹docs PASS。
没有新的外部定理/文獻重驗；Gallai等上游已採納依賴仍按§1信任界。
所有本次writes仅在此fresh目录；無commit/push/外部訊息/共享導航修改。

完整hash清單為[MANIFEST.sha256](MANIFEST.sha256)，封存envelope為[delivery.json](delivery.json)。
MANIFEST覆蓋全部regular payload、输入副本及logs，只排除根MANIFEST.sha256與delivery.json以避免hash循環；delivery逐項綁manifest/REPORT/judgment/checks並記最終manifest核驗command/exit/result，自己的hash交父監督記錄。
