# BR-SD-1e：原來源、接點 degree 與 private witnesses 獨立對照

2026-10-11。研究 BASE：`337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`。
本檔正文由獨立 [mapping review](agents/mapping/MAPPING.review.md) 複製並調整相對連結；原稿保留。
該 worker 回讀 actual HEAD／origin/main 均同 BASE；工作樹只有本輪專屬 audit 未追蹤。
遠端 main 與初始乾淨狀態由父端起始紀錄負責，本 worker 未重讀遠端。
只新增本檔，未改 canonical、舊 audit 或其他 worker 產物，未 commit／push。

**Mapping 裁決：本輪所有 degree 合法的 x∈J3／q 外臂均保留兩個原 J1／J2 private
witnesses，包含兩環皆 triangle。** `x=a3=v` 在零長／正長 q 臂都已飽和，直接
結構排除；其他接點的精確預算如下。沒有 actual target disk source 提交。

## 1. 權威來源與證據分工

本 worker 使用本輪 BASE 的 [frozen authority 清單](authority/INPUTS.json)，
讀取 HANDOFF、DOCUMENTATION、STATUS、N45§1／§2.11／§3、degree-5 guide§4、
interfaces§2／§7、common language、unary shield support 定義及指定1a／1c證據與1d歷史。

| 原來源入口 | 本次核對內容 |
| --- | --- |
| [N45 canonical](authority/docs/c5_excess_two_nonadjacent_unit_core45.md.txt) §1、§2.11 | 全部原 G／M 合同、N45-S-NOU-LS-PAIR、split22、原骨架及已採1a／1c界線 |
| [Degree-5 guide](authority/docs/c5_degree5_guide.md.txt) §4、[interfaces](authority/docs/c5_degree5_interfaces.md.txt) §2／§7 | 1e為W接J3／q臂窄殘餘；完整外鄰給degree lists；cutpoint list只等於incident palettes的聯集 |
| [Unary support](authority/docs/c5_unary_shield_budget.md.txt) §1 | actual support是整份原piece的`N_B(P)`，不以禁色marginal替代 |
| [Common language](authority/docs/c5_common_language.md.txt) §1 | 同一原圖、同一literal四色座標、完整relations／fibres／full lifts、來源與finite分層 |
| [1a PROOF](authority/audits/2026-10-11-br-sd-1a-0f181045/PROOF.md.txt) §1–4 | 原w1／w2選點、完整degree／全部原邊list接合、正式blockwise characterization |
| [1c MAPPING](authority/audits/2026-10-11-br-sd-1c-fd6e1112/MAPPING.md.txt)、[PROOF](authority/audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md.txt) §1–3、§6–7 | skeleton不是已完整degree4舊圖；terminal lemma須末端及臂點無額外C邊；錯誤cutpoint推論的負控制 |
| [1c final review](authority/audits/2026-10-11-br-sd-1c-fd6e1112/agents/paper/REVIEW.final-v2.md.txt)、[1d adoption](authority/docs/history/2026-10-11-br-sd-1d-adoption.md.txt) | 已採結果只涵蓋W接J1/J2；本輪不重新使用被旁支破壞的terminal假設 |

以下不是抽象fixture的disk實現，也不是完整來源有限觸發；它是任意候選原來源
若滿足合同，則必有的符號映射及全稱必要條件。

## 2. 同一原 G／M 與所有保留資料

`B=(b0,…,b4)` 是同一有序induced C5外框；Col是同一literal四色集。
原G為有限簡單disk，完整Σ933／941或共同整圖D5像，ε=2，每條非框邊Σ-critical，
保自己的完整刪邊witnesses。原r／s非相鄰，完整degree5，其餘有效原內點完整degree4。
原`H_G−{r,s}=L⊔S`，U=0，L long，S actual support恰為同一真框邊兩端。

唯一原省略邊為`e=rb_i`，`V(M)=V(G)`、`E(M)=E(G)−{e}`，X=M。
M自身拒絕同一proper三色β且對β inclusion-minimal，保全部retained-edge full witnesses；
不從原G的Σ-critical性推遺傳。M只有s完整degree5，其他有效內點完整degree4。
完整45／54只共同交換原roots及所有資料，使r為降度側，不能各block獨立換色。

原s恰有不同有序內鄰p∈L／q∈S，三原B-spokes全留。
`C=H_M−s={r}∪L∪S`是同一實際sole connected component；r split22。
原r的四C鄰居為J1／J2各兩個cycle鄰點，`k_M(r)=0`、`d_M(r)=4`；
G僅多原e，所以`k_G(r)=1`、`d_G(r)=5`。
s在G／M都是兩個原內鄰加三個原B鄰點，完整degree5。

全部ordered/shared contacts、所有原vertices／edges、actual attachments／supports、
ownership、rotation、原bridges、literal β、完整relations、指定pins的fibres（含空fibres）
與full lifts均保留。若effective-H忽略原孤立自由內點，其原坐標與自由因子也保留。
本論證使用其中的degree／接線／拒絕資料，未刪去其他來源身份前提。

## 3. 原骨架與 W 的同源含義

記C0為同一原C中的具名骨架邊子圖：三個任意奇長≥3的原cycle blocks J1／J2／J3，
`J1∩J2={r}`、J3與兩者不交；J2私有u≠r與J3私有v的唯一原bridge uv；
p／q原simple外臂分別到J1／J3私有錨點a1／a3，外臂可零長。
正長臂的off-cycle點與各cycle、另一外臂及uv端點互斥。允許a3=v。

令q臂按原次序為`a3=z0,z1,…,zℓ=q`，ℓ≥0。
ℓ=0時q=a3；ℓ>0時z1,…,zℓ均在J3外，只有q是s-contact。
p臂長h也可為0，h=0時p=a1，h>0時p在J1外。

本檔W指非空off-skeleton原內點集，`W∩V(C0)=∅`，C[W]連通，
`N_C(W)={x}`、x∈V(J3)∪V(q臂)。分支邊子圖為C[W∪{x}]。
完整`V(C)=V(C0)⊔W`、`E(C)=E(C0)∪E(C[W∪{x}])`，没有其他原C邊或旁支。
W沒有s-contact、沒有其他skeleton接線、沒有cross edge，且全部原點屬S。
因此刪r／s後，W仍與x處於同一S，不產生第三份piece或原unary U。

每個原y的B附件記為固定原集合`A(y)=N_B^M(y)`；它由候選來源供給，
不是隨degree表自由挑選。M只刪r-spoke，所以

`N_B^M(S)=N_B^G(S)={b_j,b_{j+1}}`，且所有y∈S（含W）有`A(y)⊆{b_j,b_{j+1}}`。

整份S的附件聯集仍必**恰為**pair，不能僅逐點滿足subset而失去某端點。
原rotation／disk embedding也須由候選來源提供；本檔沒有重新構造或核實某張實例。

## 4. 接點完整 degree：全部重合情況

對原y∈C，`t(y)=1[sy∈E(M)]`、`k(y)=|A(y)|`，完整degree必為

`4=d_M(y)=d_C(y)+k(y)+t(y)`。

對接點x，令`m=|N_C(x)∩W|≥1`，d0(x)=d_C0(x)。則

`d_C(x)=d0(x)+m`，`k(x)=4−d0(x)−m−t(x)`。

| q臂／接点x | d0(x) | t(x) | 完整degree4的必要m／k |
| --- | ---: | ---: | --- |
| ℓ=0，x=q=a3=v | 3 | 1 | **k=−m；任何非空W都超度，結構排除** |
| ℓ=0，x=q=a3≠v | 2 | 1 | m=1、k=0 |
| ℓ=0，x=v≠a3 | 3 | 0 | m=1、k=0 |
| ℓ=0，x∈J3−{v,a3} | 2 | 0 | m=1、k=1，或m=2、k=0 |
| ℓ>0，x=a3=v | 4 | 0 | **k=−m；任何非空W都超度，結構排除** |
| ℓ>0，x=a3≠v | 3 | 0 | m=1、k=0 |
| ℓ>0，x=v≠a3 | 3 | 0 | m=1、k=0 |
| ℓ>0，x∈J3−{v,a3} | 2 | 0 | m=1、k=1，或m=2、k=0 |
| ℓ>0，x=z_i，1≤i<ℓ | 2 | 0 | m=1、k=1，或m=2、k=0；ℓ=1時本列空 |
| ℓ>0，x=q=zℓ | 1 | 1 | m=1、k=1，或m=2、k=0 |

表列全部允许x；ℓ=0無off-cycle臂點，ℓ>0的q／內臂點不能與v／a3重合。
三環互斥及simple外臂合同排除x與r／u／a1／p重合，無其他命名重合漏列。
對J3點可統一寫`d0=2+1[x=v]+1[x=a3且ℓ>0]`，再另加`t=1[x=q]`。

**不可刪附件的精確限制：** 表中m／k是必要條件，不授權把原A(x)改小。
若已供給的原A(x)有大小k0，須用`m=4−d0−t−k0`直接核；m≤0即不能接非空W。
特別是若`d0+k0+t=4`已達上限，任何m≥1都結構排除。
C0只是候選原C的骨架，不是先取一張已完整degree4的舊M再任意增邊。

## 5. 其他原點與 W 的預算、原 blocks 保存

所有未等於x的skeleton點，C-degree等於d0，原附件不得變更：

| 原點類別 | d0 | t | k=4−d0−t |
| --- | ---: | ---: | ---: |
| r | 4 | 0 | 0 |
| J1的a1，h=0／h>0 | 2／3 | 1／0 | 1 |
| J1−{r,a1} | 2 | 0 | 2 |
| J2的u／J2−{r,u} | 3／2 | 0 | 1／2 |
| J3的a3=v，ℓ=0／ℓ>0 | 3／4 | 1／0 | 0 |
| J3的a3≠v，ℓ=0／ℓ>0 | 2／3 | 1／0 | 1 |
| J3的v≠a3／J3−{v,a3} | 3／2 | 0 | 1／2 |
| 正長p／q臂的內點 | 2 | 0 | 2 |
| 正長p／q臂的末端p／q | 1 | 1 | 2 |

對W每個原點w，t(w)=0，`d_C(w)+k(w)=4`；S pair給0≤k(w)≤2，
所以`2≤d_C(w)≤4`。沒有s-contact的degree-1 W leaf不可能完整degree4，
因它會要求三個不同原B附件而超出兩點support。
此局部必要條件不證明其他W topology、附件、rotation或disk可實現。

單接點W不能改變原C0的blocks或bridge身份：任何跨越W與C0的simple cycle
都須兩次通過唯一x，與simple cycle矛盾。原J1／J2／J3仍為各自maximal blocks；
uv及所有原p／q臂邊仍為C的bridges。新blocks只能屬C[W∪{x}]，透過x與原blocks接合。

因W=C[W∪{x}]−x連通，x在分支邊子圖中不是割點，故只屬該子圖一個首block。
待不可著色degree lists與外部Gallai刻畫成立，首block必為Gallai block：
m=1只可能K2／bridge；m=2只可能奇環（含K3）。K4在x需要三條分支邊，超表中預算。
不能以兩份首bridge共用x解釋m=2，因刪x會使W斷成兩份，違反W連通合同。
W後續其他blocks無須分類，仍逐原點保完整degree4與S附件限制。

W非空且無s-contact，x是H_M中的割點；本輪不依H_M二連通、SD-A或R27 minor。

## 6. 可重用 private-witness preservation lemma

在本輪原C0形狀下，取

`w1∈V(J1)−{r,a1}`，`w2∈V(J2)−{r,u}`。

若新增原有限非空連通旁支W的off-skeleton點與C0互斥，且只在單一
`x∈J3／q臂`與骨架接合，沒有其他cross edge、沒有新s-contact，則每個上述w_i均保留：

1. **存在性：** 每個simple奇環至少三點，至多排除兩個不同點，因此各集合非空。
   J1 triangle `(r,a1,w1)`、J2 triangle `(r,u,w2)`各仍有第三點；W不耗用它們。
2. **非割點：** 刪w_i後，本環變成連通path，原接入口r及a1／u均仍在該path。
   其他原blocks及W仍沿其原接點連通，故C−w_i仍連通。
3. **非s-contact：** s只有p／q兩內鄰；p=a1或在J1外臂，q在J3／q臂，
   因而w1、w2均與p／q不同。
4. **唯一block：** 兩點無額外C邊，只屬本環J_i；原block身份由§5保留。
5. **原內度與完整鄰居：**
   `N_M(w_i)={prev_Ji(w_i),next_Ji(w_i)} ⊔ A(w_i)`，`d_C(w_i)=2`、`|A(w_i)|=2`。
   兩個cycle鄰點不同；沒有sw_i邊、W邊或其他cross edge。
6. **原附件不禁D：** D是同一proper三色β未使用的第四色；全部原B附件都由β賦色，
   故不使用D。於是`D∈L^D(w_i)`，不需先假設附件β色互異。

本lemma只保留既有原private點及其鄰居／block身份。若允許額外J1／J2接線、
額外s-contact、合併原cycle blocks或變更原附件／色框，須重新核前提，不能直接搬用。

## 7. 同一原 M 的完整 list 接合與 scoped 結論

對每個原y∈C，原邊定義

`L^D(y)=Col−(β(A(y))∪({D} if sy∈E(M) else ∅))`。

由完整degree4，`|L^D(y)|≥4−k(y)−t(y)=d_C(y)`。
若存在C的完整L^D-coloring，連同原β及s=D，逐類滿足B–B、B–C、s–B、s–C、C–C
全部原M邊（含W邊及附件），給同一β的完整M延拓；被effective-H忽略的原內圖孤立點，逐點從Col−β(A(z))（含D）填色；
真正無任何原鄰居的自由孤點才任填Col。各原坐標及相應full-lift因子均保留。
這違反M自己的拒絕。反向限制亦成立，因此這是s=D時的完整coloring等價，非端點marginals。

連通C不可著色，且其lists是degree assignment，外部Dvořák Theorem10與
blockwise-uniform characterization給原blocks各palette P_K，點list恰為incident palettes
的聯集，相交blocks的palettes互斥。w_i只屬J_i，故`L^D(w_i)=P_Ji`。
§6給`D∈P_J1∩P_J2`，而原`J1∩J2={r}`給`P_J1∩P_J2=∅`，矛盾。

這個同源反證涵蓋表中所有degree合法接點、任意奇環長、任意p／q臂長與任意有限W大小。
表中結構超度接點先行排除。沒有必要研究J3／W內部palette routing或使用terminal lemma。
W接q時q的degree改為`1+m`；接臂內點時該點degree改為`2+m`；不能沿用1c的末端／
臂點無額外C邊假設。本證明只用未改動的J1／J2，不要求那些假設保持。

本mapping支持**candidate scoped exclusion**，canonical採納留owner另行批准。
完整N45-S-NOU-LS-PAIR、其他split22形狀、多旁支Gallai trees、其他45／54／55、ε≥3、
一般出口、R31與主命題均維持OPEN；未宣稱K∞=K≤5。

## 8. 驗證與下一個最小 OPEN

本worker完成上述紙面逐點映射，未建立fixture、未枚舉來源、未重跑舊controls或Lean。
本檔的degree／block／witness命題是全稱紙面論证；沒有actual source，來源實現與完整
target合同的finite trigger均`not triggered`。不能把degree合法列稱為`triggered and holds`。
需要的獨立paper review、正式外部來源核查與audit seal由父端／paper worker分工交付。

本結果內沒有private-witness失效點。下一個最小未涵蓋形狀是同一骨架有兩份原W，
其中一份接J1並耗盡triangle唯一private witness，另一份接J3／q臂；此前提同時
失去兩條既有排除路線的保證，須另核合法degree、实际S附件及完整incident palettes。
本輪不研究該雙旁支形狀，不因其可能性推升完整父身份closure。
