# N45-SU-A：S 六項／U 八項新 claim 的獨立紙面增量稽核

2026-10-09。指定 [增量任務](../2026-10-09-n45-s-supervision/cross-audit-tasks.md)；
BASE／接手及本輪實際 HEAD 均為 `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**裁決：N45-S-01–06 與 N45-U-REL／WIT／CROSS／CAP／S3／U2／SHORT／RES
全部在明列前提內成立且可搬用；本輪未發現新紙面推理缺口，也未建立來源反例。**
這是新 claim 的獨立紙面驗收，並非重述 N45-A 的九項 BASE 依賴稽核。
[S 原交付](../2026-10-09-n45-s/REPORT.md)與 [U 原交付](../2026-10-09-n45-u/REPORT.md)
均未修改。正式整合及 SU-J 的獨立有限增量驗收由監督端另裁決。

只可關閉：S 指定 **原 spoke 省略的 u=2** 子型；U 指定 **整份原 unit unary 省略的
u=2** 及 **兩 short mixed** 子型。S 的 LOW／HIGH、long 配置及 U 的唯一 U＋long／short
完整同源跨列接合仍 OPEN。原 55、其他 core、無 45／54 core 來源、一般 N2、ε≥3、
猜想 E 與一般出口均未關閉。必要身份的成立不證其存在或不存在。

## 1. 凍結、獨立性與實讀來源

先核 HEAD／Git 與 BASE 的 HANDOFF、STATUS、DOCUMENTATION，再讀 S／U 新論證。
共享 STATUS／guide／派工歷史是已有未提交管理修改，沒有作數學來源，也沒有修改。
來源以 `git show BASE:path` 與已保留 clean detached S／U checkout 的實際 bytes 對回。
依任務自行完成，未委派 sub-agent；只 exclusive-create 本 fresh SU-A 目錄的檔案。

| 凍結項 | 本輪確認 |
| --- | --- |
| S REPORT | `51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1` |
| S checker | `94b3fb13e8268080e80a441f595fd3fcab449ea2c2937b2bf92c1725e5977dae` |
| S certificate | `9acb2a6b40de32aeca60ecf9a5b33065c9cba60ad47f5243c1eccadf31f59a02` |
| S inputs | `09aeaaa919c299c5a8c3ed44ef250e6e90a96ab1040e3fd8bea6fbc57b1e63de` |
| S delivery | 精確 21 項 inventory／bytes／hash 相符；另核 delivery.json 自身及 supervision inputs，共 22 個 S 檔 |
| S 數學輸入 | 69 項 declared hash、BASE Git objects、實讀 checkout bytes 三者相符 |
| U REPORT | `0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7` |
| U checker | `37da93a6fe6109f82287eac67db518515b6718c30013f020acfd21e6364162e3` |
| U final certificate | `1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0` |
| U inputs | `ed32a320d7924af82f87fbbe78c12a667fb34222299414ac4fb4839b6895355d` |
| U 凍結交付／來源 | 39 authored 檔與 batch supervision frozen inventory 相符；source/ 的 70 權威 BASE 項另核，不混稱 39 authored 檔 |
| J certificate | `ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4`，本輪核 hash，不代 SU-J 重算 |

輸入清單及 bytes／mtime_ns／hash 初始快照在 [inputs.json](inputs.json)。
額外 BASE 文件檢查工具、歷史 provenance 與 A finding 來源列在
[supplementary-inputs.json](supplementary-inputs.json)；A 僅供保留既有 finding，
沒有用其判定代替新 claim 的推理。

十四項独立裁決先寫入 [independent-judgment.json](independent-judgment.json)，
封存 SHA256 為 `97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872`。
**封存前未讀監督 paper 判定；只核其輸入 inventory／hash。** 封存後才讀 S 監督 §2／§2.1
及 batch supervision §2／§2.1。逐項對照見 [supervision-comparison.json](supervision-comparison.json)：
14 項 verdict 與範圍一致，獨立封存檔未改写。

本輪重新讀 [Dvořák 原始講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
2018-03-24，Lemma 7（PDF 第5頁）、Theorem 10（第6頁）。Lemma 7 的 strict slack
與 Theorem 10 的 connected degree-list／Gallai 前提均逐次核適用性。
原始 [PDF](gallai.pdf) 與 S／U frozen copy 的 SHA256 同為
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；
來源紀錄在 [primary-source.json](primary-source.json)。沒有用四色定理作 oracle。

## 2. 共用原圖前提與沿用界線

主 claim 量化任意大小的有限簡單 G：有序 induced C5 B=(b0,…,b4) 圍 disk 外面，
完整有序 Σ=933／941 或共同搬運整圖的 D5 像；每條非框邊 Σ-critical，ε(G)=2，
有效 H 忽略孤立內點。原完整 degree-5 roots r,s 非相鄰，其餘原內點 degree4；
H−{r,s} 恰兩份完整 mixed P,Q，其餘 unary。所有原頂點、ordered contacts、
shared contact 的單一坐標、actual attachments／support、ownership、原 bridges、
rotation、字面 β、完整 tuples／fibres（包括空 fibres）及 full lifts 保留。

S 身份是原 spoke e=rb_i 被省略，X=G−e=M；U 身份是整份完整 unary U 被省略，
唯一原 root-contact 為 rx，X=G−V(U)=M。兩者各要求 M 是原拒絕 β 的 inclusion-minimal
core，自身 degrees 為45／54；root 交換必搬整圖，不獨立搬 pieces 或色名。
原 incidence=1 不表示每列 F_U 必非空或 singleton。

令 m_r,m_s 為兩原 mixed 的各側 incidence 總和，k_C^r,k_C^s 為原 contact 邊數，
E_r^X／E_s 為完整 side factors 的同時避色集合。固定共同 β、s=b 時，C_C(b)
表示由整份 R_C 共同避全部 contacts 得到的 forbidden r 色欄；shared contact 同時核兩個限制。
D/O/δ/o/λ 都是同一列、同一欄的 B-C2 費用。short 包含 singleton 或一條真框邊的兩端；
long 是其他 actual support。q 下標是 singleton 位置，cells indices 分別為
q0=6、q1=4、q2=3、q3=1、q4=0，T4={2,5,7,8,9}。

| BASE 依賴 | 本輪重新核的適用步驟 | 沿用而未重跑的部分 |
| --- | --- | --- |
| E2 REPORT §1–3／§5.4 | 先同 Σ minimalize、有效度數與 ε 差式、Q⊆原 Q、q2 的位置 | ε≤1 任意大小化約、全四分類及有限末端分類證書 |
| E3 REPORT §2.1／nonadjacent §2–5 | fullB、degree4 飽和、root deletions、N2 one-sided、nonempty support、兩類原unit省略 | 全上游枚舉與既有 degree4 分類 |
| E4 REPORT §4.1／§4.2／§6 | 原 G 的 N-diagonal、局部 lists 不需外部整圖染色、完整 joint、原 contacts／lifts | 原 hub/Gallai 任意大小引理及舊固定控制 |
| CORE_CONSTRAINTS §2／§4 | derivative 的 X/Y distinction；重色spoke E4-D前提，不取 converse | 歷史 byte replay FAIL 照留，不重寫 artifact |
| Phase B §2.1／§2.2／§3.2 | 逐原piece witness／外路／原費用、χ0 degree4逐欄五項零 | B-S0 拓撲與 hub 證明；非本批原容量模板 |
| 原 unary shield §2–4 | 原盾弧邊互斥、支援區間與原 unary 費用；省略者仍付原費 | 上游 hub/Gallai 二／三袋引理，未作全鏈形式化 |
| degree5 tree components §1 | U-S3 的 K4 四方向／tethers；本輪另核 branch 握手式與 connected outside | 不照抄單root/spoke前提；依實際 N2 外部重核 |
| U4 §2 | 僅核搬用限制；retained44 與 O11 下界均未作 S/U 證據 | 不重開 U1–U4；不搬其支援下界或44結構分類 |

因此「成立」是以下新推理在明列 BASE theorem 信任邊界內成立，不表示本輪重新證完
E2、Gallai／hub 或上游有限分類。沒有新增 Lean theorem、native_decide、build 或 axioms audit。

## 3. S 六項獨立裁決

### N45-S-01

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意原spoke e、任意X拒絕β；跨列式也適用尚未minimalize的X。

原圖前提：§2 的S 原 spoke省略身份，並保留下列逐步使用的額外條件。

依賴：BASE E2 REPORT §1-3,§5.4；BASE CORE_CONSTRAINTS §2。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. X全體有效內點≥4且ε=1；保B/完整Σ(X) inclusion-minimalize為Y，surplus差式兩項非負，Y自身Σ-critical。
2. X=M的β-critical⇒每條非框刪邊新增β⇒X自身Σ-critical；這步不從原G遺傳。
3. Q(X)⊆Q(G)，E2只允許空/單點/相鄰pair；933的q2含{2},{1,2},{2,3}；941只容許q0/q1/q3；coreβ須在Q(X)。
4. 新接受γ的每份X lift若r≠γ(b_i)便接回G，故所有lifts都同色；只是原邊不等式解除。

未涵蓋：不給necessary Q的disk實現；不重驗E2全部有限末端分類；不將所有derivatives預填critical。

### N45-S-02

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：每個X拒絕β及每個b∈E_s，非只選一欄。

原圖前提：§2 的S 原 spoke省略身份，並保留下列逐步使用的額外條件。

依賴：BASE Phase B §3.2；Dvořák Lemma7。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 不固定r，固定共同β與s=b；所有r-contact含strict slack，包括shared contact；完整連通R非空，欄禁色≤k_r；反向同理。unary非空但F可空。
2. 原s side incidence=5-m_s，E_s大小≥m_s-1≥1；X r度數4，χ=0；全部其他外部限制只有同一兩roots與B。
3. B-C2逐欄D^u+O^u+δ+o+λ=0，每項非負，五項各零。
4. 故E_r^X大小=m_r；每份r-unary F滿額，retained side factors兩兩不交；每份mixed欄滿額、互斥，raw union恰E，無外溢；全部tuple/lifts仍保存。

未涵蓋：不能由marginals推joint；其他β的F可空；不把degree5的一單位放入X。

### N45-S-03

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：每個S-02列與其全部b∈E_s；c=β(b_i)。

原圖前提：§2 的S 原 spoke省略身份，並保留下列逐步使用的額外條件。

依賴：N45-S-02；BASE CORE_CONSTRAINTS §4 E4-D。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. c不在E：X全部side factors互斥，故唯一retained side factor擋c；加spoke只增O至1。
2. c在E：每欄E由P/Q互斥分割，c每欄唯一mixed owner；加spoke從E刪c，只增λ至1；owner可隨b變。
3. 只有retained blocker也是spoke時才是重色spokes並可用E4-D；unary blocker不滿該前提。

未涵蓋：不給固定mixed跨全部欄owner；不把coreβ與e的其他列critical witness合併。

### N45-S-04

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意properβ、全部16有序pins；任意大小原one-sided mixed C且0<k_r,k_s、k_r+k_s≤3。

原圖前提：局部前提：原C完整degree4；同一disk原G full B-touch；H-C連通；actual support恰{h}；原兩root contacts及shared identity保留。

依賴：BASE E4 REPORT §4.1 N-diagonal；BASE Phase B §3.2的兩方向contact界。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 固定c=β(h)；C的局部限制只見c/兩pins，固定c的共同S3置換保完整compatibility。
2. 原fullB/one-sided/short適用N-diagonal，全部diagonal已接受。
3. 其餘forbidden軌道：(c,b≠c)需要k_s≥3；(a≠c,c)需要k_r≥3；a,b≠c且a≠b需要兩側各≥2。
4. 正incidence總≤3三軌道均不可能，A_C=Col²；套S-02時違反正值欄飽和。

未涵蓋：singleton incidence≥4仍OPEN；不推一般mixed至少pair；局部色雙射不作各piece独立正規化拼圖。

### N45-S-05

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：所有spoke省略身份；short部分另量化P,Q都短。

原圖前提：§2 的S 原 spoke省略身份，並保留下列逐步使用的額外條件。

依賴：N45-S-02；N45-S-04；BASE E4 §4.1；BASE Phase B §2.1；BASE unary shield §2-4；BASE E3 nonadjacent §3。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 原G N-diagonal給兩short全部同色pins；X拒絕⇒E∩E_s空。|E|=m_r, |E_s|≥m_s-1⇒m_r+m_s≤5。
2. 每份mixed至少兩原contacts，故各總incidence≤3；原support非空。singleton依S-04變通用且違反S-02，故兩short均原pair，各收1。
3. 逐原unary選自身Σ-critical contact新接受full lift，限制到G-U得不能接回的outside witness；H-U原連通/fullB給避自身的root到B補弧路。
4. 有long且u=2用原三pieces2+2+2；兩short且u=2用四原pieces1+1+2+2。幾何收費同一G，β_e可不同；spoke不收piece費。

未涵蓋：只關spoke省略原u2子族；整U省略另外由U claims處理；不推原55/一般N2。

### N45-S-06

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意S原身份且兩mixed都short。

原圖前提：§2 的S 原 spoke省略身份，並保留下列逐步使用的額外條件。

依賴：N45-S-05；BASE E4 §4.2；BASE unary shield §2。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. u0原兩short未用色diagonal接回排；S-05排u2，故u1。無unary側t若m_t2，原t三spokes；H-t由另一root/P/Q/U原連通。
2. H-t全體非B點落B+t-star同一開面；fullB迫兩個非spoke框點皆在此面弧，三gap只能1,1,3。
3. 對P/Q/U逐份，t及兩小star面在含H-piece的F_piece；長3弧外兩框邊均仍在∂F_piece，因此三原盾弧均包含於長3弧。
4. 三原盾弧互斥卻需1+1+2=4>3，故m_t≥3；总≤5与m_a≥2迫(m_a,m_t)=(2,3)。
5. LOW：U/e在r，m=(2,3)，n_U+t_r=3且t_r≥1得(1,2)/(2,1)，E/E_s互補2。HIGH：U在s,e在r，m=(3,2)，r原2spokes/X留1，E大小3，E_s為該保留spoke色；n_U+t_s=3。

未涵蓋：LOW/HIGH都是必要身份而非排除/實現；long配置及原55/一般N2仍OPEN；未使用U4 retained44/O11下界。

## 4. U 八項獨立裁決

### N45-U-REL

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意properβ，全部16pins與其全部X lifts；Δ上每個新接受γ。

原圖前提：局部：原連通完整degree4 unary U唯一contact rx；保持原U全頂點/內邊/框附件/共享β。singleton forcing另需eΣ-critical；coreβ另採所有有限簡單 induced-C5 disk G；完整Σ=933/941或整圖共同D5像；非框Σ-critical；有效H恰兩非相鄰原degree5 roots r,s，其餘原degree4；恰兩完整mixed，原contacts/shared identity/support/ownership/bridges/rotation/字面框與full relations不變；不限制pieces大小。 原完整unary U唯一root-contact rx；X=G-V(U)=M為原拒絕β的inclusion-minimal core，root degrees45/54；其他原pieces及spokes完整保留。

依賴：Dvořák Lemma7；原單contact精確relation查詢。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 放開r時U degree-lists≥deg_U且x strict slack，T_U非空；F_U為全部contact色集合共同禁色，T單點才F單點，T≥2則F空。
2. 原G root-pairs為K_X中可用完整U lift避a的pairs；刪唯一contact後U總能獨立接回，所以K_(G-rx)=K_X，圖vertices與lifts各自保留。
3. 每個γ∈Δ，K_X非空、K_G空；每个投影a均要求T_U⊆{a}，T非空迫π_rK_X=T_U=F_U={a_γ}；量化全部X lifts。
4. coreβ時K_X空不約束F；不推F_U(β)非空。

未涵蓋：不把U替成染色star；不推unit每列F singleton；38個F空列為較強版本負控制，非目標來源反例。

### N45-U-WIT

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：每份原piece選一條原critical contact與自身新接受列。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：BASE E3 nonadjacent §3；BASE Phase B §2.1；BASE unary shield §2-4。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. G-e新接受literal全圖lift限制到G-piece，outside合法而整piece不可填，否則原G接受原拒絕γ_e。
2. 原degree4給degree assignment，不可填迫tight；N2其他mixed使H-piece原連通。
3. 若原unary短，fullB補弧點由H-unary碰到，owner root在H-unary原路避自身抵達該B點；逐unary補足B-S0外路。
4. 所有原unary≥2盾邊且互斥，省略U仍付σ_G(U)；不同γ_e的幾何費可同圖相加，染色容量不可跨列相加。

未涵蓋：不收σ_X(U)；不把spoke當piece；分隔piece無one-sided時不得搬用。

### N45-U-CROSS

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意整unit derivative；core必要表再要求β被X拒絕。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：BASE CORE_CONSTRAINTS §2；BASE E2 §1-3,§5.4；N45-U-REL。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 刪原U的degree4點surplus為0，只降r一度，ε(X)=1。保完整Σ minimalize Y而非先宣稱Xcritical；exact surplus差式非負。
2. E2適用Y，Q(X)=Q(Y)⊆Q(G)僅空/單點/相鄰pair；加β∈Q(X)得七格完整表，933 q2不能省。
3. 941 Δ至少1列、933至少2列；每份γ均另滿足U-REL forcing；同一X不能同拒q3及q0/q1。
4. X=Mβminimal另推出XΣcritical，但不作上一步必需前提。

未涵蓋：necessary masks不作disk實現；其他core/ε≥2不套E2；不跨列加費。

### N45-U-CAP

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：每個core拒絕β及每個b∈E_s。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：BASE Phase B §3.2；Dvořák Lemma7；N45-U-REL。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. unary完整R非空且F大小≤原contacts；r degree4給|E_r^X|≥m_r，s degree5給|E_s|≥m_s-1≥1。
2. χ0拒絕join令逐欄D+O+δ+o+λ=0；兩mixed raw columns滿額、互斥，union=E_r^X。
3. 恢复唯一原unit U：F空時D增加1；F={a}在E外時O增加1；F={a}在E內時λ增加1；δ/o與原mixed欄不變。
4. 所有結論按原共同β及b核，不以別列witness補容量。

未涵蓋：D/O及N2拒絕X缺精確有限控制；不把N1 λ控制當N2排除；不乘端點marginals。

### N45-U-S3

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：任意大小原mixed P、0<k_r,k_s且總≤3；不需目標mask或指定coreβ。

原圖前提：原G fullB-touch的disk；P全部原degree4、H-P原連通/one-sided；有P的原Σ-critical contact與完整outside拒絕見證；原contacts實際互異/shared identity保留。

依賴：Dvořák Lemma7/Theorem10；BASE degree5 tree components §1的四tethers機制；BASE E4 §4.1；BASE E3 N-empty（交叉證明用）。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 反設support至多一點，原contact witness產生不可染degree assignment，P為Gallai tree。
2. K4 block每點3 clique邊剩1外接方向；非direct方向只能bridge，四branch互斥且不回另一clique點。branch若不碰G-P，4|T|=2|E(T)|+1矛盾；四tethers與連通G-P形成K5 minor。更大cliques本身非平面。
3. 餘blocks為bridge/odd cycle；每点至多一B邊，root incidence≥3-deg_P(v)。多block至少兩末端private集合，每個≥2 root edges，總≥4。singleton度數≤3；单bridge总≥4；单oddcycle只有triangle可总≤3。
4. triangle三點各exact一root邊及一h附件；Y=(H-P)∪(B-h)由原fullB連通，與h相鄰，各triangle點到Y有原root邊；三點/h/Y為原K5 bags。
5. 獨立alternate：empty support用BASE N-empty排；singleton用原N-diagonal+fixed-c S3軌道+兩方向contact界得通用A；critical contact witness又給至少一forbidden原pin pair，矛盾。不先使用U-S3自身。

未涵蓋：總incidence≥4仍OPEN；S04單獨得通用relation，尚需critical witness才能支援排除；不搬U4/O11/44下界。

### N45-U-U2

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：所有U原身份且恰兩份不同原unary U,V。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：N45-U-WIT；N45-U-CAP；N45-U-S3；BASE N-diagonal/B-S0。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 兩原unary各費2；若mixed有long再費2即矛盾，故两mixed short（先不假設pair）。
2. X拒絕及原兩short N-diagonal⇒E_r^X∩E_s空；|E_r^X|≥m_r, |E_s|≥m_s-1⇒m_r+m_s≤5。
3. 兩mixed各總≥2故各≤3；U-S3的fullB/one-sided/原critical contact均具備，故兩mixed原support≥2；short故各pair費1。
4. 同一原G四pieces1+1+2+2>5；省略U仍付原費；不依retained44下界。

未涵蓋：只關整U省略原u2子族；有限無N2 u2 exact-positive control；不推一般N2。

### N45-U-SHORT

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：所有U原身份，兩mixed都short。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：N45-U-U2；N45-U-WIT；BASE E4 §4.1。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. U存在，原unary≤2與U2排除⇒唯一U；X沒有unary。
2. 原拒絕β用三色，共同未用D避所有原spokes；兩原mixed N-diagonal給完整(D,D) lifts，同一β拼回X矛盾。
3. 原U費2再排两long费2+2，剩long+short；不使用X fullB-touch。

未涵蓋：只關整U省略兩short子族；不排spoke省略LOW/HIGH；不排一般long/short。

### N45-U-RES

**判定：成立且可搬用（以下前提內）；新推理 finding：無。**

量詞：所有U原身份通過上述窄排除後的每個β及每個γ∈Δ。

原圖前提：§2 的U 整份 unary省略身份，並保留下列逐步使用的額外條件。

依賴：N45-U-REL/CAP/S3/U2/SHORT；BASE unary shield §2-3；X β-minimality。證據層：任意大小paper；具名BASE依賴；外部degree-list/Gallai依賴另列；本輪無Lean。

1. 唯一省略U，long L/short S；原incidence式t_r+k_L^r+k_S^r+1=5，t_s+k_L^s+k_S^s=5，各mixed側正。
2. 原U/L盾≥2，S盾≤1；pair S費1迫(U,L,S)=(2,2,1)，U/L各連續3點、原五盾邊分割；singleton S費0，S3只給總incidence≥4，U/L盾只能(2,2)/(2,3)/(3,2)。
3. 原度數給k_S^r≤3,k_S^s≤4；Xβminimal保所有spokes所以各root在β的spokes色互異。
4. X無unary共同D可用；short S接受(D,D)，X拒絕迫long L禁止(D,D)。β逐欄原L/S滿額互斥分割E_r^X；每個新接受γ又有U palette與X r-projection同singleton。

未涵蓋：唯一U+long/short完整同源跨列仍OPEN；singleton S incidence≥4未排；necessary identities不宣稱實現/一般排除。

## 5. 三個關鍵新步驟的原圖核對

### 5.1 S-06：長3面、原 H−t 與三份原盾弧

這是本輪重新證明，沒有由 U4 的 O11／retained44 下界推得。若無 unary 側 t 的
m_t=2，原 t 完整 degree5 給三個不同 spoke 端點 A。另一 root、兩完整 mixed 及唯一 unary
在 H−t 中連通；其非框部分避開 B+t-star，所以只能落在同一個開面。全 B-touch 使
B\A 的兩個非spoke框點都由此連通塊碰到，因而在同一 A-gap；C5 的 gap 長必為1、1、3。

對任一原 C∈{P,Q,U}，K_C=B∪C∪E(C,B) 的非框部分都在長3面內；另兩個小 star 面
不含 C，且可經未列入 K_C 的 t-star 鄰域連到 t。t∈H−C，故兩小面都屬含 H−C 的 F_C。
其兩條框邊仍在 ∂F_C，σ_G(C) 便只能用長3弧的邊。三原盾弧互斥，卻至少占1+1+2=4
邊，與長3矛盾。所有 F_C／σ_G(C) 都在原 G；没有假設 X 自己 full B-touch。

LOW 的原 r-side incidence 為 n_U+t_r=3 且 e 要求 t_r≥1，故只留(1,2)/(2,1)；
HIGH 的原 r 無 unary、m_r=3 故原2 spokes、X留1；E 大小3及與 E_s 不交迫 E_s 為該
保留 spoke 的唯一字面色。這只核必要身份，不將 LOW／HIGH 關閉或聲稱可實現。

### 5.2 U-S3：原 K4 四 tethers、末端計數與最後 triangle

原 contact 的 Σ-critical 新接受全圖 lift 限制到 G−P，得到完整 P 不能接回的 witness。
原 full degree4 給 degree assignment；Lemma 7 核 tight，Theorem 10 核 Gallai tree。
K4 block 的每點已有3 clique edges，僅剩1原外接方向；若不直達 G−P，該方向只能為
P 內 bridge。block 性質使四支枝互斥且不返回另一 K4 點。若支枝 T 不碰 G−P，唯一
離開 T 的原邊為接 K4 的 bridge，完整度數握手式 `4|T|=2|E(T)|+1` 不可能。

原 H−P 連通；P 至多碰 h，故其他至少四框點由 H−P 碰到，G−P 連通。這個外部加四條
tethers 的尾部形成一個 connected hub，配四個 K4 原 singleton bags 得 K5 minor。
這只證非平面性，不是染色收縮或 replacement。

餘下 blocks 為 bridges／odd cycles。每個 private 點最多一B附件；terminal bridge 的
private leaf需至少2 root incidences，terminal odd cycle至少兩個 private degree2點、
每個至少1 root incidence。多block的兩個末端 private 集互斥，合計≥4。單singleton
原度數≤3，單bridge總incidence≥4；單odd cycle每點至少1，總≤3只餘 triangle。

triangle 的三點各恰一root contact及一條到同一h的框附件。Y=(H−P)∪(B\{h})
由原 fullB 與 one-sided 連通，各 triangle 點經自己的原root邊鄰Y，h經框邊鄰Y；
三 triangle singleton、{h}、Y 是互斥、連通、兩兩相鄰的五個原 bags。最後也矛盾。
只用了總incidence≤3，不能將結論提升至 singleton incidence≥4。

### 5.3 N-empty／N-diagonal／S3 軌道的獨立交叉論證

此論證在封存 independent-judgment 時已形成；讀 batch §2.1 之後對照一致。
空 support 由 BASE N-empty：同一 H−P 原root外路提供一／兩hub，任意合法 outside
witness都可接回，與原critical contact矛盾。singleton {h} 則以原 fullB／one-sided 的
N-diagonal 保全部diagonal；固定 c=β(h) 的S3色軌道與兩方向contact界排除總≤3的
所有off-diagonal禁對，所以 A_P=Col²。原critical contact witness的合法outside pair
因而可以接回整P，也矛盾。沒有先假設 U-S3 結論，亦沒有取22個控制的完備性。

S-04 直接證的是局部 complete compatibility 通用；若要搬成 U-S3 的 support 下界，
還需要原 critical-contact witness（以及空支援的 N-empty）。若要在 S 的兩short分支
使用，則原 support非空及 S-02正值欄飽和已提供所需矛盾。只搬這些實際充分前提，
不搬U4的44分類，也不把局部色名雙射作獨立piece正規化。

## 6. Coverage、反例及 finding

以下有限數字僅是本輪**原 S／U checker 的正常／seed17只讀重播**恢復的 frozen payload，
不是 SU-A 新寫的獨立有限判定器；其獨立增量核對仍屬 SU-J。沒有搜索新圖、增加 k、
新有限數學控制或新來源證書。SU-A 的 verify_inputs.py 只核 provenance／bytes／mtime。

| 層／claim | 原固定控制重播與未覆蓋前提 |
| --- | --- |
| S singleton／S-04 | 原288候選，92接點界觸發並成立、196不觸發；這是抽象軌道界，不證原graph/fullB/critical witness前提 |
| S abstract capacity／S-02–03 | 原3模型／4容量欄保完整16pairs及空pairs；缺named graph、full lifts、targetΣ、criticality、minimality，不是來源控制 |
| S counts／S-01、05 | 原12 scalar及完整933／941 Q表只是必要算術，不證disk實現 |
| S 原N2／spoke source | 原19圖190 rows、47 original-spoke×original-rejected-row derivatives全接受；完整target與X拒絕β前提0觸發，沒有S source正控制 |
| U REL | 原23圖，11整U省略；3680 original pins、1760整U省略pins、1760 contact刪除pins；690 local relations、2986 piece lifts；SU-A未獨立重建這些fibres |
| U CAP | 原G90＋X12欄；4份N1低度側placement全λ；D/O及N2拒絕X缺正控制，不能拿N1補N2 |
| U S3／U2／SHORT | 原22低incidence support instances只核必要結論；沒有singleton反證支枝或無界Gallai證明控制；N2 u2／指定45／54省略前提0觸發 |
| U overclaim負控制 | 原38 F空列與72 singleton列；反駁「unit每列F singleton」，不反駁U-REL。NA8-0003／原U=P1={8,9}／x=9／index3=01201 保留具名反例 |
| 來源反例 | SU-A未建立來源反例；有限target不觸發不表示一般排除 |
| Lean | 沒有新增theorem或形式化認證；paper、有限payload及外部定理分開 |

**N45-SU-A-COV-01（保留的缺控制）。** 受影響步驟是 S-01–06 的目標來源適用驗證，
以及 U-CAP 的N2下降側零欄、U-S3的singleton/Gallai反證、U2／SHORT的來源排除校準。
缺精確target／拒絕X／原u2等前提；不得將原checker exit0當紙面命題PASS證據。
這項是coverage finding，沒有新數學反例；本輪不要求搜尋來源正控制。

**原四項 N45-A finding 保留：**

- N45A-F01：歷史 E4 core-constraints／reductions byte replay **FAIL**。本輪未重跑該兩原
  checker，獨立重核其 frozen JSON 的 E3 provenance 與 current BASE E3 hash 確實不符；
  舊30573 bytes／`6d385639…`，current32469／`73ed652a…`。
  「非sources payload相同」沿用 frozen A 的比較，沒有冒稱本輪重算；詳見
  [historical-provenance.json](historical-provenance.json)。不能把來源bytes通過改稱舊replay通過。
- N45A-F02：精確Σ933／941的N2 45／54正控制缺失；12個45／54 occurrences屬N1，不能補本批。
- N45A-F03：一般mixed支援下界仍OPEN。新S/U只在低incidence及各自省略身份內給充分下界；
  singleton incidence≥4、其他core與一般N2沒有由本輪關閉。
- N45A-F04：fresh BASE缺兩個歷史audit targets，本輪實際文件重播仍FAIL。

S 原 COVERAGE／DOC findings、U 原F1/F2/F3/PROV均保留；U 的 failed attempts、初版
certificate.json、final certificate、原路由漂移記錄全部未改。歷史有漂移仍保留其歷史狀態，
不以本輪輸入零漂移覆寫過去。

## 7. 檢查、零漂移及寫入界線

本輪逐命令 argv／cwd／環境／exit／stdout／stderr 保存在 [checks.json](checks.json)及 logs/。

| 本輪檢查 | 結果／實際意義 |
| --- | --- |
| 初始 inventory／anchors／BASE objects | exit0；S21＋delivery、U39、J指定hash、S69／U70權威来源均相符 |
| S 正常／seed17 --check | 各exit0，原certificate逐byte相同；只讀replay，沒有SU-A獨立有限完備性聲明 |
| U 正常／seed17 --check | 各exit0，final7682242 bytes逐byte相同；原initial/final/failed logs不變 |
| 原始Gallai來源fetch | exit0；原文bytes與S/U凍結PDF一致，外部來源前提另作paper核對 |
| fresh BASE check_docs | **exit1**：586 Markdown、6982 links、2 missing paths |
| BASE正式 docs DocGraph | exit0：62 documents、213 relations、5 families、0 errors/notes |
| 主worktree全域DocGraph | **exit1**：62 duplicate-ID errors；原scratch及U/source副本保留，未刪檔隱藏FAIL |
| tracked git diff --check | exit0；另核本fresh輸出文字whitespace／JSON／本地links |
| 收尾provenance正常／seed17 | exit0；與初始快照對回，bytes及mtime_ns零漂移；BASE來源、額外來源及獨立封存檔一致 |

fresh BASE缺的仍是 `audits/2026-10-04-task-d5/c4/scope_ledger.json` 與
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。沒有補造舊產物，也沒有以
主worktree留存副本或formal DocGraph PASS掩蓋fresh BASE FAIL。

未跑：E2/E3/E4/E4C全上游枚舉、U1–U4、ES/ER、新k搜尋、全套minimal core枚舉、Lean
build/axioms，以及SU-J獨立finite checker；原因是本任務為十四新claim的紙面增量審查。
沒有新Lean或新finite控制需要額外certificate。未重播歷史E4兩原checker；其FAIL及來源字段
差異照留。沒有重讀／改寫common reports或更新管理導航以提前正式採納。

L0交付僅本SU-A目錄。L1/L2已讀BASE Kempe guide／STATUS、E4 §4.3／§6與Phase B §2.1的
原45／54／55 OPEN範圍；父N2與猜想E仍OPEN，本輪不改共同文件、不向上層宣告closure。
傳播停止在獨立稽核回報，監督端對回hash及SU-J後再裁決正式採納。

完整輸出hash清單在 [MANIFEST.sha256](MANIFEST.sha256)，另由 [delivery.json](delivery.json)
凍結該manifest與其餘全部輸出；delivery自身不自雜湊。所有原S/J/A/U、舊證書及管理文件
未寫入。未commit／push／PR／對外訊息／sub-agent。
