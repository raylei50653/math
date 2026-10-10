# N45-H1R：原 HIGH1 圖、完整 fibres 與原邊非平面性獨立裁決

2026-10-10。BASE／執行 HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
唯一輸出本目錄；沒有修改共享文件、worker 或任何舊 audit，沒有 commit／push／PR／再委派。
未讀本輪其他獨立稽核的 judgments。原交付的 94 份 regular files 完整凍結於
[worker copy](frozen/worker/REPORT.md)，包含 nested manifest／delivery／receipt；沒有按 basename 排除。
[inputs](inputs.json)另外逐項綁定 34 份來源輸入，其中 16 份 BASE blobs 已向 Git 原物件核 bytes／blob ID。
其餘 current 輸入凍結以支援父端採納後重播；不要求採納後 mutable 文件維持舊 hash。

**獨立裁決：HIGH1-CORE 至 HIGH1-EXCLUSION 十項在完整 H1–H13 內成立，無新增充分前提。**
可採納為任意大小 paper 排除，仍依賴 BASE 已採用的紙面／固定結構化約與外部 Gallai；
Python 只核固定抽象圖的完整語義及 C5 metadata，沒有證明任意大小排除。
正式逐項裁決見 [independent judgment](independent-judgment.json)。HIGH2/3、long、其他 core、原55、
一般 N2／E、來源實現與新 Lean 均不在此裁決範圍。

## 1. 同一完整來源契約與量詞

每項裁決均量化**任意大小有限原 G**，同時滿足以下全部來源前提；子引理所需較少不擴大採納。

| ID | 完整前提 |
| --- | --- |
| H1 | finite simple disk；有序 induced C5 B=(b0,…,b4) 圍外面 |
| H2 | 完整有序 Σ(G)=933／941 或一次共同整圖 D5 像；每條原非框邊 Σ-critical；ε(G)=2 |
| H3 | 有效 H 連通、full B-touch；原孤立內點 I 保留為每份 full lift 的自由因子 |
| H4 | 原 nonadjacent r,s 完整 degree5；其餘有效原內點完整 degree4 |
| H5 | H−{r,s} 恰完整 connected、one-sided、非空 actual support 的 U,P,Q |
| H6 | mixed P/Q 各支援恰一條真原框邊兩端；各接兩 roots；actual attachments／ownership 全留 |
| H7 | 原 U 只接 s，唯一原 contact sx，無 U–r；完整 U 保留 |
| H8 | mixed totals=(3,2)；s 對 P/Q 各一，r 的原分配1及2保具名身份 |
| H9 | 原 r/s 各兩個不同 spokes；只省略 e=rb_i，X 留 rb_j，s 兩 spokes全留 |
| H10 | 固定原拒絕 literal β；X=G−e=M 自己是 β inclusion-minimal45／54 core |
| H11 | 只删 e；所有原 pieces 頂點／內邊／contacts／框附件／其他 spokes全留，無替换 |
| H12 | 原 ordered contacts、shared 頂點單一變量、support／ownership、bridges／rotation、共同 literal 四色框、十列 relations、全部 ambient 空／非空 fibres、r/s pins與 full lifts |
| H13 | D5／S4／root swap共同搬整圖及全部資料；保933 q2；β不必是 U 盾中點，G/X/刪contact圖各有自身原邊與 lifts |

FULL relations 的量詞是每一 proper literal γ、每一 ordered tuple、每一 r/s pin及每份完整 assignment；
F／minimality 的特定結論在固定 β 上；REJECT 則在每一三色 literal γ 上。G 與 X 的邊集一直分開。

## 2. CORE、COMP、JOIN、RESTORE

原 r 度數3 mixed+2 spokes=5；刪唯一 e 後 X 中3 mixed+1 spoke=4。
s 仍2 mixed+1 U+2 spokes=5，所有其他原點仍完整4。H_X=H_G；disk、induced B、T4接受由删邊繼承。
X 的 β-critical witnesses 全來自 H10 自己的 inclusion minimality，未從 G 的 Σ-criticality 遺傳。

H_X−s 恰 C={r}∪P∪Q 與 U。P/Q 各連通且接 r，故 C 連通；其內邊為全部
E(P)、E(Q)、三條 r-mixed contacts；其框附件包括全部 P/Q attachments 與 rb_j。
U 的原內邊／框附件全留，C/U 間無邊。s 的兩 C contacts 分屬不同 pieces而互異；
U 唯一接點為 x。兩份 ordered sublists 取自原 s 三 contacts 總 rotation；
若 r-contact同為s-contact，始終是同一原頂點變量，不拆成獨立 port。

對每一 literal γ，令 S_C(γ)、S_U(γ) 為各自全部 proper assignments，包括實際框附件；
C 的 r 仍須避 γ(b_j)。每一 t∈Col²、c∈Col 保
Φ_C(γ,t,c)={f∈S_C:f(兩 ordered contacts)=t,f(r)=c}，共64 ambient fibres；
U 每一 d∈Col 保 Φ_U(γ,d)，共4 fibres，空 fibre 同樣保留。
X full lifts 的 restriction／union 精確雙射是

```text
s=a 避兩原 s-spoke 色；
f_C∈Φ_C(γ,t,c)，t的兩座標均≠a；
f_U∈Φ_U(γ,d)，d≠a；以及任意原 I→Col。
```

C 內部的 P/Q 再接合同一 r=c 時，兩條 r–P contacts 必同時約束同一份 P assignment。
反向 union 每條 X 原邊恰在分量內、框附件、r-contacts、s-contacts或 I自由因子中核查。
原 G 的全部 lifts 恰加 c≠γ(b_i)，包括全部16雙root pin queries。
不能從 X 接受推出 G 接受；完整 r projection 必須保留。這四項直接原邊證明無額外假設。

## 3. F 與 BASE (2,1) 逐前提映射

X 的 β-minimality 使 s 兩 spokes 異色：同色時删其一不改任何約束。
未 pin s 時，每份 connected 分量至少一原 s contact 有 degree-list slack；其餘點 list≥degree，
所以兩份 relations 非空。r 在 C 中內部degree3＋一原框spoke，仍是完整degree4。

完整 join 給 A_s⊆F_C∪F_U。各 s-spoke 的自身 β-critical witness 迫新釋放的框色未被任何分量禁，
故 F_C∪F_U=A_s。删任一分量 incident 非框邊，只解除該分量所有禁色：外邊新增色、非bridge內邊給
connected slack、bridge兩側各有 slack；另一分量全留。其原完整 witness 供 private color。
兩分量各有 private color而 A_s 恰兩元素，因此 F_C/F_U 是互異 singleton，非接點數猜測。

BASE E4 §4.1 對每一原 one-sided short mixed、任一 literal γ、任一色 a，直接供
全部原 contacts 同時避 a 的完整 assignment。它是局部 list 定理，**不要求已先存在 G−piece 外染色**。
因此在 β 及每一 a≠β(b_j) 上置原 r=s=a，P/Q 各可接回，C避 a；
F_C⊆{β(b_j)}。非空＋精確覆蓋迫 F_C={c0}、F_U={D}，其中 c0 是 A_s 的已見色，D 是 β未用色。
這裡 C lift 明保 r=a，沒有抹去 r fibre。

將 β singleton共同搬到位置4，並以同一 S4 搬為q=01012；e、rb_j、全部 attachments、rotation、
ordered tuples、pins／空 fibres及全部其他拒絕位置同搬。X 的唯一degree5 hub是s，兩分量恰C₂=C、C₁=U。

| normalized s-spokes | 獨立查 BASE 的充分前提／實際 scope |
| --- | --- |
| 02、13 | β同色，已由X自身minimality排除 |
| 03 | sectors §1–3 的(2,1)必要位置表排除；X具disk/T4、完整degrees、實際兩分量及exact singleton cover |
| 01 | adjacent_21 §§1–5：兩不同分量／2與1接點、實際crosscuts、原attachments、tight lists、Gallai與connected-exterior K4；涵蓋兩singleton次序，不需第二拒絕列 |
| 12 | middle_21 §§1–4：同identity、兩原crosscuts、原三exterior hubs、bridge／leaf-cycle K5；兩次序，不需第二拒絕列 |
| 23 | reflection §1–2 全圖(ρ,π)搬回01，保C/U角色及全部r fibres |
| 34、40 | split_support §§1–6：先由reflection支援定理得到指定actual supports；沿用degree-four任意大小結構及既有有限 cover，只給X全列 F/Z；40僅共同reflection。原 e恢復另核 |
| 14、24 | nonadjacent §§1–6：sectors迫兩分量分居長／短區域；actual C₂/C₁ identities、parent pin、pA/pB完整延拓及既有finite-reduction trust全留；24共同reflection。只延拓X，未宣稱延拓G |

BASE mapping 依賴文件的任意大小結構／固定縮減 trust 沿原文，不重跑舊 catalog／全部有限證書。
HIGH1 最終排除使用下一節原 G 證明，不靠 split／nonadjacent 的 X 新接受列。

## 4. 原 K₃,₃、原 U shield 與原 G 同色 full lifts

P/Q 的真支援框邊各是其 one-sided σ 的唯一邊（BASE shield Lemma2），且 σ 邊互斥。
若支援邊共框點 b_v，原 G 六 bags 是左 P,Q,O=B−{b_v}，右 {r},{s},{b_v}。
P/Q connected，O為原C5删一點的四點框路，六 bags互斥；九對原鄰接如下：

| bag pair | 原邊來源 |
| --- | --- |
| P–r、P–s、Q–r、Q–s | 各原mixed contacts |
| P–b_v、Q–b_v | each实际支援含b_v的原attachment |
| O–b_v | 原框邊 |
| O–r、O–s | 原兩distinct spokes各至少一 endpoint≠b_v |

O–r 可恰用 e；這是**原 G** 非平面性反證，不把 e虛構成X邊，bags也未被當 coloring replacement。
故兩支援邊頂點互斥。

原 sx Σ-critical 供 G−sx 的新列完整 witness。它必令 s=x=a；若某原完整 U assignment能避 a，
可重新著色整份U接回G，違反新列身份，故原 U 的某列 F_U非空。
H−U={r,s}∪P∪Q connected。假設U支援包含某框邊，full B-touch供另一框點h的原内鄰點，
H−U內連到s，得到避U的原外路。BASE shield §3／short support 引理連同既有t=0補註
令全部 F_U空，矛盾。故 |σ_U|≥2且actual support至少三點。
連續σ_U與兩mixed σ邊互斥；C5兩條頂點互斥框邊之剩餘邊恰長二及長一兩段，
所以σ_U就是唯一長二段。BASE shield Lemma2 的full B-touch充分前提全成立，
得actual N_B(U)=V(σ_U)=某三個連續框點T。没有事先猜β為盾中點。

固定任一三色 literal γ，未用色D。原 U 未pin s時，在x有slack，故完整palette P_x非空。
其單contact禁色F_U等於P_x是singleton時的那個色，否则空，容量≤1。
若T未見齊γ三色，另有已見色h未在actual U support出現。只在**整份U assignment**上交換D/h，
所有U–B約束均保持，故是所有完整 assignments／空 fibres的雙射。
容量≤1且F_U穩定迫D不被禁；取同一γ下一份完整 f_U，使x≠D。

仍在同一 literal γ置r=s=D。原r/s全部spokes包括e都合法，因為γ未使用D。
BASE E4局部N-diagonal分别提供P/Q全部contacts同時避D的完整 assignments；
与 f_U、兩roots以及任意原I自由因子union，逐項保**所有原G邊**，得到G full lift。
没有独立normalize piece色名，也不是把X接受猜成G接受。

因此Q(G)⊆T。任一q_k在連續三點T見齊三色 iff singleton位置k∈T。
933 原拒絕{0,1,2,3}含四點，941 的{0,1,3}非連續三點；皆不能包含T。
共同D5／S4及完整root rename保持這個原圖矛盾；933 q2保留。
這是無大小上界的紙面排除，依賴BASE／外部Gallai的既有trust；沒有新增來源實現或Lean。

## 5. 獨立固定校準、實跑與封存

[checker](checker.py)採**Cartesian complete assignments＋顯式 inequality factors**，不import worker算法或決策。
[calibration](calibration.json)重算固定toy的每一240 literal列，含10 canonical列全64 C tuple/r fibres、4 U fibres、
16雙root pins、所有X/G assignments；逐欄與凍結worker full semantic fields比對，未以worker PASS作oracle。
完整P/Q join亦核同一r值，shared contact保持單坐標；原孤立点是四色自由因子。

| 控制 | 實際結果／限制 |
| --- | --- |
| 同源完整接合 | triggered and holds；240 literal rows，固定抽象圖，無disk／minimality／完整Σ來源認證 |
| 共同搬運 | triggered and holds；10 canonical rows×10整圖D5×24同一S4=2,400次full X/G lifts；另240列whole root rename |
| endpoint marginals過強版本 | counterexample；γ=01023、s query0；C tuples={(0,0),(0,1),(2,0),(3,0)}。兩marginals各可避0，完整tuple不能同時避0 |
| X接受即G接受過強版本 | counterexample；γ=01012，X兩份 full lifts的r都1，lost-spoke色1，G無lift；toy未滿HIGH1 source契約 |
| 原K₃,₃ schema | triggered and holds；1,000具名spoke/支援metadata；另10 ordered頂點互斥支援的唯一長二U arc，未當作1,000 source graphs |
| 單contact穩定子 | triggered and holds；5個support×240 literal列，以support固定色群的orbits獨立重算所有capacity≤1 invariant F，100個wholeD5拒絕位置矛盾 |
| β/spoke映射 | triggered and holds；由十canonical cells的933／941完整bits獨立推原Q，再核70 labelled β/D5資料及每份10 spoke pairs；933 q2另占10份 |
| 有限HIGH1 source | not triggered；未建立、未執行，沒有trigger數。toy／metadata均非來源 |

normal／seed17實跑stdout／stderr／exit存[checks](checks.json)；兩份只讀重算stdout byte一致。
工具negative另用校準證書的一個wrong byte，真正exit2命中calibration byte comparison，
僅拒絕錯artifact；不把它說成数学或source反例。
封存manifest精確納所有regular payload；只排當前top-level manifest/delivery及receipt列明metadata，
凍結nested metadata全部納入。封存normal／seed17與wrong-manifest digest控制有獨立receipt，
最終完整驗證可用：

```bash
python3 -B audits/2026-10-10-n45-h1r/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h1r/checker.py --check
python3 -B audits/2026-10-10-n45-h1r/verify.py
```

歷史缺檔、worker已有DocGraph62 duplicate-ID及其他FAIL bytes全保留；沒有刪scratch或重跑全樹DocGraph。
本輪僅新目錄的links／whitespace與封存檢查，不新增Lean，所以未重跑lake build。
官方 [Gallai講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)已核Lemma7／Theorem10與凍結PDF，
仍是外部定理trust，不是checker證明。最終採納／共享文件傳播由父端另裁；本audit不自行關更廣分支。
