# C₅ 全線進展與高階假設整合

**目前整合快照（2026-10-04，K′／E3–E6／ES／ER／LC）**：
共同 ε≥2，任意大小的 ε≥3 與猜想 E 仍未證。E3 把 ε=2 反例約化為
拒絕 q₀、q₁、q₃，並排除唯一 degree-6；D₈ 的100份相對 spoke 位置補表
是此結論的必要依據。E4／E6 證非相鄰／相鄰 mixed 分量數 m≤2，
E5／E6 收窄相鄰 G1–G4、J6 與 no-mixed；雙 degree-5 仍有殘留。
ES／ER 三型 k≤9 的 q／critical orbit 集合及計數逐層一致，共179個 critical
orbits，無 |Q|+c(Q)>4；LC 完成179／179個 Lean soundness 證書，不證搜尋
完整性或拓撲 disk 定理。K′ 局部資料仍留933／941一致指派，局部題停止。
共鄰 P₃ 則已由 C-W／D₆ 在 C §1 前提下整型來源排除，固定 ledger 為0；
全主線總葉數與每日速度仍未知。精確殘留與未派提議由
[Kempe](c5_kempe_guide.md#3-停止點與保留缺口)及
[weak-deletion](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)導覽維護；
本次驗證與發布範圍見[紀錄](history/2026-10-04-kprime-excess-two-progress-publish.md)。
以下 A／B／C、D₅ 及各輪數字保留當輪截點。

**最終成果獨立驗收（2026-10-04，D₅）**：
[固定快照、scope ledger與版本表](../audits/2026-10-04-task-d5/REPORT.md)驗收A₄／B₄／C₄。
A₄直接核對原04／04與root交換，01202 singleton1／3、完整C替換／外部逐點
保持及投影／六角色joint界線成立；18／22降至16／20，40／58支援與50／84
schedules完整保存，未用D₅來源搬運。B₄只關閉W933-129／04–12／長face{2,3,4}
的shared-{4}附件支；原K的完整degree奇數cut與十對原邊K₅不刪整份骨架。
C₄只新增(CPP-134-1,34,60)，逐份自身支援與完整lifts的2↔3雙射給矛盾；
未知w relation保持，九份配置／27完整組合、3500keys及36／140／900表不刪。
以下各輪數字保留當輪截點；紙面／外部定理／Python／Lean分開。
下一入口僅由兩份導覽維護，mixed12／mixed22整型、ε≥3及一般出口未證。

**後續整理（2026-10-04）**：933／941 的固定完整 Σ、edge-minimal
induced-C₅ disk 來源在有效內部連通、所有有效內點完整 degree≥4 的前提下
均已證 ε≥2。唯一 degree-6 的 ε=2 分支已全排；前序已發布的雙 root
九輪及四-spoke 七輪已推進雙 degree-5 roots，其後另有最新五輪 mixed11
當時未提交成果，以及任務 A／A₂／A₃、B／B₂／B₃、C／C₂／C₃ 的正式返回成果。各輪保持同一原分量、
全部原附件、具名有序接點、實際支援、原嵌入及共同色框。

本批連同後續A₄／B₄／C₄、獨立稽核與完整封存發布；驗證與還原入口見
[發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)。

| 分支 | 後續完成範圍與保留界線 |
| --- | --- |
| t=1 全七分拆 | [整型來源全部排除](c5_excess_two_single_spoke_complete.md)；共同[短支援引理](c5_short_support_singleton.md)、五葉 active tree、原 binary 路徑及四接點固定末端區塊涵蓋任意大小來源 |
| t=2 全五分拆 | [整型來源全部排除](c5_excess_two_two_spoke_complete.md)：復用 t=1 的短支援、singleton profiles、共同 active forest 與原首橋；(2,2) 保留純 pair 層的 20 份抽象控制，加入同一首橋局部 residual 後全排 |
| t=3 全三分拆 | [整型來源全部排除](c5_excess_two_three_spoke_complete.md)：(2,1) 的十份具名配置／8,250 同源 profiles 全無目標，(3) 的 100 容量比較與三 unary 六跨度矛盾完成其餘分拆；原 binary 省略證書保留 |
| t=0 全十一分拆 | [整型來源全部排除](c5_excess_two_no_spoke_complete.md)：真實外部路徑恢復多分量跨度，(6) 由飽和兩原 K₄ 給 K₅；(4,2) 的 7,200 弱 profiles 由 160 同源 binary 路徑框弧證書全排 |
| t=3 spoke＋unary 省略 | [三原 unary 共同扇區](c5_excess_two_three_unary.md)完成 path／tail，連同原 triangle 位置關閉整份條件分支 |
| 雙 roots 的原刪除與 zw 接回 | [原刪 root](c5_excess_two_root_deletions.md)至少一份全收，另一份至多缺一列；相鄰 mixed 兩份均全收。[原路徑](c5_excess_two_path_edge.md)與[單 triangle](c5_excess_two_triangle_edge.md)完成剩餘接回，因此相鄰 mixed 有 Σ(G−zw)=Ω |
| 相鄰唯一 mixed 的 (4,4) q-core | [原身份／雙 spoke](c5_excess_two_mixed_core_spokes.md)、[spoke＋unary](c5_excess_two_mixed_core_spoke_unary.md)、[雙 unary](c5_excess_two_mixed_core_two_unary.md)及[省略原 mixed](c5_excess_two_mixed_omission.md)全部封閉；(5,4)/(4,5) 與原 (5,5) core 仍保留 |
| 相鄰唯一 mixed 的原單 spoke 與五-spoke 型 | [單省略](c5_excess_two_mixed_core_single_spoke.md)若拒絕，省略圖自己是唯一 degree-5 minimal core；[原 leaf joint 纖維及同一 unary 雙列 palette](c5_excess_two_mixed_core_leaf_fibers.md)全排五-spoke 原來源，兩候選總 spokes 都≤4；單省略尚未整型排除 |
| 四-spoke (3,1) 的 mixed-(1,1) 加兩單接點 unary | [原三分量六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md)：原 critical witnesses 與短支援外路徑迫各跨度至少二，同一原圖共同 lifts 只有五段，含 root 交換；完整五點 joint 保留 |
| 四-spoke (3,1) 的 mixed-(1,1) 加一原 binary unary | [原 leaf 完整反像](c5_excess_two_mixed_core_four_spoke_binary.md)與[原 star](c5_excess_two_mixed_core_four_spoke_star.md)保留的32／64份，由[同列端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md)全部作二／三hub Gallai K₅來源排除；含root交換，原完整relations保留，整個子型已排除 |
| 四-spoke (3,1) 的 mixed-(1,2) 加一原單接點 unary | [原三接點身份排除](c5_excess_two_mixed_core_four_spoke_ternary.md)：同色省略後 M 自己是 minimal (3,1) q-core，整份原 C+a 的 (a,y₀,y₁) 接上既有 active-triangle K₅；20／60具名框架全部排除，含root交換，完整六點joint／原ternary保留 |
| 四-spoke (3,1) 的 mixed-(1,3) 無 unary | [原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)：唯一原 K=C+a 的四 contacts 要求三禁色，marked leaf 迫至多二；原 spanning-tree 貪婪直接給 M／G 延拓，20／60 框架全排，含 root 交換；結合前三子型完成 (3,1) 全部四份 incidence 分拆 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：共用 pair | [原三角 sealed mixed](c5_excess_two_mixed_core_four_spoke_equal_pair.md)：原 diamond 封 C 在一個原三角區域，既有三-hub 延拓接 G−C 全收，排除共用 pair 的 7／9 份，含 root 交換；當輪 unequal 殘留由下列短 face 收窄，完整六點 joint 及空纖維保存 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：短 face | [原 unary 非 critical 接線](c5_excess_two_mixed_core_four_spoke_short_face.md)：原 01／02 的 unary 只能碰 01、0 或 12，既有短支援接原外部路徑迫 Σ(G−au)=Σ(G)，含 root 交換及同機制 8／16 份；原六角色 joint 與五角色投影 witness 替換分開保存 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：同一長 face | [原 unary 支援次序](c5_excess_two_mixed_core_four_spoke_long_face.md)：原01／04兩unary若critical必同在三段face，原路徑交錯排除迫支援跨度和≤3，而短支援引理迫≥4；固定原邊非critical，同機制10／10份，unequal剩22／40。完整原relations與空纖維保留；只替換固定短unary的整份witness，C與另一unary外部頂點逐點保持，主張五角色投影相等 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：原 crosscut | [原路徑封 mixed 與二／三 hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md)：941原01／03、933原01／13的critical unary crosscut封C到一框點，同色tightness保degree的Gallai K₅使原ax非critical；新排8／16至14／24。原完整C替換保存外部所有頂點，只主張四角色投影相等 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：共用短框弧 | [原拒絕列完整joint](c5_excess_two_mixed_core_four_spoke_short_arc.md)：941原02／03及最後六份共用點身份以C短支援Fempty及未見色交換構造原01021延拓，至14／18；指定列出口，不宣稱C所有rootpair延拓 |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一 unary：不相交pairs與子型完成 | [原子型完成報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)：最後14／18由一側全短4／8及共同兩段長face10／10全排；原47／75身份完整ledger無重複／遺漏。完整原relations保留；只替換固定短unary的整份witness，C與另一unary外部頂點逐點保持，主張五角色投影相等；其他incidence及ε≥3保留 |

上述為任意大小紙面論證＋Python 固定必要域證書，未新增 Lean theorem，
未提高共同下界至 ε≥3。ε=2 只剩兩個 degree-5 roots；四-spoke (3,1)
在相鄰唯一 mixed 前提下，全部四份原 incidence 分拆及 root 交換
已封閉。上表分列共同跨度、同列端點 hub、三接點身份與四接點
leaf-slack 的證明入口，沒有新增跨列 palette 定理。

(2,2)、mixed-(1,1) 加各側一原單接點 unary 已排共用 spoke-pair
的7／9份、短face的8／16份、同一三段長face的10／10份、原crosscut的
8／16份、共用短框弧的0／6份及不相交pairs的14／18份。
**四spoke(2,2)、mixed11+各側一原unary子型已完成，原47／75全部封閉。**
最新證書逐原identity核對所有六階段排除無重複／遺漏，最後殘留0／0。
原crosscut的C替換、shortarc的指定列完整joint、不相交pairs的原unary
替換分別保留四／六／五角色證據；不把C marginals、mask或收縮當成完整relation。
933原01／13的幾何搬運將Σ933送至940，941部分原身份搬至949，均保存
全圖共同row／color／rootrole transport，不識別不同來源relations。
後續（2026-10-04，任務 A）：[mixed12+a側一unary](c5_excess_two_mixed_core_four_spoke_mixed12.md)
的原01／23及root交換已排，原crosscut／省略圖的單一ternary與完整joint
迫同一U的三列singleton3／2／3，違反未用色守恆。新70／90必要域保存
22／26具名框架、56／92actual支援與72／130完整relations；後續
[A₂的原01／12長／短face排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)
固定原spokes01／12，以原U的actual 2附件crosscut及指定拒絕列01202
上的完整C witness／六角色joint再排兩候選各兩份root身份，
保存其餘20／24框架、52／86actual支援與68／124完整relations。
原C ternary及同框joint保持，不從mixed11完成表推定新incidence分類。
只證該指定列的原root-pair fibre延拓，不主張C所有root-pairs都能延拓；
mixed12整型與來源實現仍未證，下一入口由[Kempe導覽](c5_kempe_guide.md)維護。
同日[A₃的原共用01／01三-hub排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
保存四份rotations、同一原C三-hub前提，替換整份C使原ax非critical；
只主張(a,b,u)投影相等，六角色joint不相等的完整反例仍保留。
01202的U singleton2／3各有原joint矛盾；其餘18／22框架、44／70
actual支援、56／102完整singleton schedules保存。原A與A₂表保持歷史層。
後續（2026-10-04，任務 B）：[mixed22無unary的原四接點身份](c5_excess_two_mixed_core_four_spoke_mixed22.md)
保存七份跨側共享身份、完整四接點 relation 與同框六角色 joint；四條
原 spoke 省略各自全收 Ω，每個原拒絕列的 minimal q-core 均為原 G、
root degrees=(5,5)。47／75 必要骨架各收窄至25份相鄰 spoke-pairs，
sealed triangle 各排5份，仍保留20／20份原 face／tightness 必要見證；
同日[B₂的原01／23短face排除](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
固定W933-101／W941-139、原C位於短face {1,2}，跨全部拒絕列及合法
root-pairs的tightness／leaf-owner限制給原K₅ minor，七份contacts身份
均無短-face殘留。後續[B₃的同骨架長face窄引理](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)
另以shared leaf-bridge slack、五種實際leaf hubs與原外部路徑排除
{0,4,3}，七身份零長-face殘留。兩W的短／長faces分別有證明；其他
骨架及faces仍保留，原20／20必要證書保持歷史層，非來源catalogue。
同日[B₄的原933 04／12 shared-{4}窄支](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)
先鎖定W933-129長face{2,3,4}；真正shared leaf在11原pairs均tight，
不套B₃的min-degree二分類。整份K=C−v的原cut parity迫奇數框附件，
{a},{b},{v},原B,整份K給原K₅；六shared身份／八指定選擇此支全排。
同份骨架其他附件／身份及其他骨架保留；原B／B₃ artifacts不覆寫。
整型、ε≥3與來源實現未證；
停止點與下一入口由 [Kempe 導覽](c5_kempe_guide.md)維護。
其餘 (2,2) incidence／較少 spokes、單省略、原 (5,5) q-core、多 mixed、
no-mixed、非相鄰 roots 及一般來源均仍保留；一般出口與 K∞=K≤5 未證。
現況與下一窄題見 [Kempe 導覽](c5_kempe_guide.md)。
後續（2026-10-04，任務 C）：[mixed P₃ 共端點報告](c5_mixed_p3_common_endpoint.md)
涵蓋任意大小原 unary 的雙扇區／triangle tether；d=2 的兩角色全部作
source 排除，c=2 只保留 used-singleton／pair。36份具名殘留、140份
幾何 rotations、900份 side joins 的固定域沒有 target；未因此證來源
實現或新增 Lean theorem。同日[C₂的一色支援三接點unary排除](c5_mixed_p3_one_color_ternary_unary.md)
只關閉CPP-134-1／geometry 30／side_join_id 20：固定z側原三接點
unary自身支援恰為{b₁}、完整degree四與禁色{0,2,3}，迫原triangle，
原z–x₂–b₄外路給K₅ subdivision。原36／140／900控制保持當輪計數；
未排整份case、該geometry的全部側接合或所有一色支援。不同自身支援
的geometry 34當時仍保留，單框點葉數證明不能直接套用。
同日[C₃的雙框點strict-list／原N葉排除](c5_mixed_p3_two_frame_ternary_unary.md)
只關閉CPP-134-1／geometry 34／side_join_id 20；禁色0排接點碰b₂，
禁色2的原palette分T／N葉，N葉先由五袋十對原邊K₅排除，再重證
接點葉數。C₂／C₃合用只登記兩個具名geometry×join keys；原36／140／900
與全部空fibres／witnesses不刪。下一入口是geometry34／join60，其他w角色
與geometry35未驗收；現行停止點由 [weak-deletion 導覽](c5_weak_deletion_guide.md)維護。
本次正式返回工作區的固定快照、獨立驗收與並行文件核對見
[D₄整合稽核](../audits/2026-10-04-task-d4/REPORT.md)；
[D₂](../audits/2026-10-04-task-d2/REPORT.md)與[D₃](../audits/2026-10-04-task-d3/REPORT.md)
的當輪覆蓋、停止點及所有成功／失敗紀錄保留，沒有回寫新結論。
本批整理、具名殘留分組及文件漂移核對見
[四-spoke 七輪整理與發布紀錄](history/2026-10-03-excess-two-four-spoke-progress-publish.md)；
前序mixed11研究見 [子型完成紀錄](history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md)，
前兩份同輪進展見 [共用短框弧紀錄](history/2026-10-03-excess-two-four-spoke-short-arc.md)
及 [原 crosscut 紀錄](history/2026-10-03-excess-two-four-spoke-crosscut.md)，
前輪見 [同一長 face 紀錄](history/2026-10-03-excess-two-four-spoke-long-face.md)，
前輪見 [原 unary 短 face 紀錄](history/2026-10-03-excess-two-four-spoke-short-face.md)；
前序提交範圍見 [雙 root 整理紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)，
前序唯一 degree-6 見 [t=3／t=0 發布紀錄](history/2026-10-03-excess-two-degree-six-publish.md)，
前序 t=2 批見 [發布紀錄](history/2026-10-03-excess-two-two-spoke-publish.md)，
前序 t=1 批見 [發布紀錄](history/2026-10-03-excess-progress-publish.md)。
下文保留 `b97b107` 當輪的跨線快照及實驗提案，其「未解」依後續成果閱讀。

2026-10-02，基準 `4565735`。這是跨線研究快照與實驗提案，
依當前 [HANDOFF](HANDOFF.md)、八份導覽及原報告整理。
各線即時停止點仍由各自導覽維護；本頁不改變其研究排程。

**整體判斷：目前已建立相當完整的關係語義、低超額核心結構與有限證書工具，
主要缺口集中在同一來源上多個拒絕列的相容性，以及幾何／操作能否隨關係一起保留。**
主命題 `K∞=K≤5`、一般單側／共同出口、多步充分 state 均仍未證。
下面把已完成推導、有限觀察與新假設分開。

## 1. 究竟要證什麼

指定有序 C₅ 為 disk 外框，其餘頂點私有。Σ(G) 是全部可延拓的 boundary
四色染色，僅按**共同** S4 色名置換取軌道，不先商掉框點的 D₅ 位置。
合法 C₅ 有十個 patterns，其中五個使用三色、五個使用四色（T4）。
目標

\[
K_\infty=K_{\le5}
\]

表示每個可實現的完整 Σ 都有至多五個內點的 disk 代表。
它不要求每個原圖都能靠指定的局部改寫縮小，也不要求 minimal obstruction
的原圖大小有界。後者已有無界家族；「小代表」與「小原核心」必須分開。
精確定義見[研究目標](c5_boundary_relations.md)。

目前有兩種主要工作方式：

- **來源排除／出口：** 保留同一原圖及各拒絕列的 minimal cores，利用
  degree、完整接點關係、actual supports、環序和原路徑，排除來源或證指定列延拓。
- **接合／替換／state：** 精確計算共同關係 J，判斷可用 disk 框族，
  修復投影遺失的資訊，再詢問同摘要是否足以支援後續操作。

兩者共用關係代數與幾何工具，但沒有現成定理把「修復成功」直接變成
「一般出口存在」或「主命題成立」。

## 2. 2026-10-02 各線快照

| 研究線 | 已有的實質結果 | 仍需處理的範圍／證據層 |
| --- | --- | --- |
| [State、grammar、枚舉](c5_state_guide.md) | k≤5 catalogue 共132個具名Σ、24個D₅軌道；固定較小grammar另有87類；關係接合及部分grammar語義已有Lean | k=6、7為reduced搜尋及獨立重現，非原邊宇宙精確窮舉；未得所有disk完備性或一般state充分性 |
| [全degree-4](c5_degree4_guide.md) | T4全收、disk minimal q-obstruction、所有有效內點完整degree=4時，Σ=Ω\{q}；任意block tree已合成到路徑／triangle正常形 | 任意大小紙面證明＋外部degree-list定理＋有限證書；完整Gallai／minor／disk鏈未Lean化 |
| [Degree-5／R系列](c5_degree5_guide.md) | 指定三-spoke來源的零／一／二奇環及部分三環位置有任意長排除；唯一degree-5全部核心另已完成指定相鄰雙列分離 | 分離不等於完整來源分類；R31同末端不同二接點的任意長來源minor、其他三環／更多環仍開放 |
| [Sector／3903、3703](c5_sector_3903_guide.md) | 指定sector的雙拒絕分類排除3903等四目標，3703三拒絕另已完成；早期交換分支被更強分類涵蓋 | 均有特定degree、disk、b0接線前提；十二列投影不等於完整Σ；603抽象profiles未因此重算 |
| [Weak-deletion／出口](c5_weak_deletion_guide.md) | 唯一degree-5、相鄰雙root唯一mixed singleton／K2、no-mixed十五類，均由來源排除或指定雙列分離接回條件式出口 | 一般單側及共同出口未證；更大／多mixed、degree≥6、多root／非相鄰root仍保留 |
| [Kempe／計數／候選來源](c5_kempe_guide.md) | 當時有同圖換色更新、六維循環流／十二生成元；933的ε≥2；941的ε=1已收窄到t=2、3及唯一binary原分量。後續941 t=2、t=3全排，與933同得ε≥2 | 933、941一般來源未排除；分別的orbit分解不能補出同染色相容性；一般connectivity／repair策略未證；現行ε=2停止點見[Kempe導覽](c5_kempe_guide.md) |
| [兩點重疊](c5_two_vertex_overlap_guide.md) | 六個具名接合圖、全部U上候選框、J/P差集；兩私有核心r*=4、唯一最少兩份及各15組極小repairs；多種任意大小同class來源族 | 只涵蓋具名圖與指定族；框拓撲、全部來源必要分類、一般class-pair後繼與多步摘要仍開放 |
| [Lean](lean_guide.md) | Root、BoundaryDegree及grammar／enumerator等基礎；新CommonRepair 27、SealedFourPort 22、NamedRepair 34個普通theorems | 抽象repair、D₁₃密封替換與兩具名核心已接入；來源族端到端、全部可用框、一般拓撲及外部degree-list尚未全部接通 |

表中的132與87有不同的研究域；不能把87當132的替代全集。
「唯一degree-5全部分離」與「R31來源minor仍缺」也不矛盾：前者只需要
接受指定target rows，後者要求更強的原圖結構排除。

### 2.1 最接近主命題的剩餘候選

[Kempe screen](c5_kempe_screen.md)把1,023個非空masks篩成153個；
再用外側已知cell相容性留下142個。比既有132多出的十個具名masks，
分成933及941兩個D₅軌道：T4全收，但可延拓的三色singleton位置為
單點或不相鄰兩點。若證明T4全收必有相鄰兩個可延拓singleton，
這條既有條件式路線可導向主命題。

**此screen的外側相容性使用四色定理4CT。** 本頁沿用其明示依賴，
沒有把它當4CT的無循環證明，也沒有用4CT作新搜尋oracle。
一般adjacent-singleton引理、拓撲橋接與有限分類信任仍須分開。

近期的真正橋接是[四容量子覆蓋](c5_excess_one_subcovers.md)：
把weak-deletion累積的單列minimal-core結構，搬回933／941的**同一完整Σ來源**。
不是把幾份獨立圖的lists相加。

| 固定Σ的edge-minimal disk來源 | 當時已知 | 當時下一域／後續結果 |
| --- | --- | --- |
| 933 | ε=Σ內點(deg−4)≥2 | ε=2的root／mixed配置；不能直接套ε=1單root論證 |
| 941 | ε≥1；ε=1時只有一個degree-5 root、一份binary分量及三份單容量因子；t=1已排除 | 當時為t=2、(2,1)，再t=3、(2)；所有十列共用原接線及省略身份。後續t=1 (2,1,1)、[t=2 (2,1)](c5_941_two_spoke.md)、[t=3 (2)](c5_941_three_spoke.md)全排，固定來源下同得ε≥2 |

相鄰的**缺失**singleton兩列（出口候選A），與相鄰的**可延拓**singleton
位置（主命題候選引理）是兩個不同陳述。

## 3. 可整合成什麼共同框架

我建議以「**同源完整關係＋臨界預算＋具名幾何證書**」組織後續研究。
這是研究框架，並非已完成的一條普遍定理。

| 層 | 保留的資料 | 已經發揮的作用 |
| --- | --- | --- |
| 關係 | 同一原分量的完整有序tuples、共同色框、具名接點與完整fibres | 精確root消去、八點natural join、來源等價與投影repair |
| 臨界性 | 每個拒絕列的minimal core、原邊刪除見證、省略因子身份 | 禁色容量、D/O/κ預算、兩個core不能任意獨立選擇 |
| 幾何 | 原attachments、ownership、共同環序、原外部路徑、合法框族 | 跨度≤5、來源K5 minor、框可用性與密封替換 |
| 操作 | 允許刪哪些邊、交換哪個原分量、未來可接觸哪些點 | 決定出口與多步後繼；尚不能只從前三層的粗摘要推出 |

這解釋多條研究為何收斂到相似現象：單一邊際看起來可行，放回同圖、
同接線、同環序後才衝突。no-mixed十五類的共同式
`D+O+κ=degree−4`、樹骨架κ=0、雙root的`m+s+a≤5`，
P₃與941的六跨度排除，以及兩框各自可延拓卻無共同延拓，都屬於這種
相容性問題；但各式仍只在原證明的前提下使用。

特別值得保留的兩個方向：

1. **把任意大的圖換成有限的可觀測關係。** 輪環、雙扇、D₁₃顯示原圖形狀
   可以持續變複雜，邊界關係仍相同。有限關係分類可能比完備的局部改寫分類容易。
2. **把局部可行性提升成同源相容性。** 計數cone、pair marginals、分開的
   Kempe splits、各框的獨立延拓，均有明確資訊缺口；下一個lemma應指定
   哪一份共同見證或幾何連接使它們必須相容。

## 4. 本輪初驗：四點統一假設需要修正

先試較強說法「所有C₅來源都能由全部四點投影重建」。
新[階數報告](c5_relation_arity.md)與[完整證書](../artifacts/c5_relation_arity/observations.json)
得到：

| 最小來源投影階數 | class數 |
| ---: | ---: |
| 2 | 11 |
| 4 | 101 |
| 5 | 20 |

二十個五階類分成四個D₅軌道。已用原邊集重新核對它們的完整Σ，保存
共100份四點restriction的原圖延拓。例R511只拒絕`01232`，但這個拒絕列
的五個四點restrictions都能各自延拓。故**普遍四階來源假設已否定**。

可以保留、而且已有初等紙面證明的是：

\[
\boxed{r^*(J,P)\le d(J)\le
\max\{d(\Sigma_A),d(\Sigma_B)\}\le5,\qquad J\subseteq P.}
\]

這只要求精確兩來源接合與共用色框。另有`T4⊆Σ ⇒ d(Σ)≤4`，
已檢查全部32個T4全收的抽象masks。兩個既有私有核心來源R127／R167
也都是四階，故其接合的四階上界不用逐個來源替換族重新證。
六個原接合的實際r*仍為四個0、兩個4，與舊證書相同。

此初驗提供三個判斷：

- 未來若找接合r*=5，至少一側必出自上述二十類；可避開大部分class pairs。
- T4四階性連933／941都滿足，因此只是語義結構，不能充當disk排除。
- 同來源Σ與同接點雙射已決定J；再證同一合法框族才決定P與全部repairs。
  不需要先證所有圖都可縮回某個共同原核心。

這是本輪新做的有限初驗；其他來源排除結果以原報告為準，沒有全線重驗。

## 5. 三個可反駁的高階假設

### H1：ε=1無法承擔獨立singleton支撐

**後續（2026-10-02）**：H1 已在固定完整 Σ=933／941（或其整圖 D₅ 像）、
Σ-edge-minimal、指定有序 induced-C₅ disk source、有效內部連通及所有
有效內點完整 degree≥4 的既有前提下成立；ε=Σ有效內點(deg_G−4)。
完整 t=1、2、3 排除的合成見 [941 ε≥2 報告](c5_941_three_spoke.md)。
以下支持／未完成／實驗保存 `b97b107` 當輪提案，不再是當前未解題目。
這不推出 ε≥3、來源實現、一般出口或 K∞=K≤5。

**候選陳述。** 固定Σ∈{933,941}及其D₅位置的edge-minimal disk source，
必有ε≥2。這裡minimal指刪任何非框邊都改變完整Σ，並非同一列q的minimal。

933部分已證；941只剩t=2、3。因此這個假設是把「多個單列core」的
局部理論合成「同一來源所有拒絕列」的第一個自然層級。
它仍遠弱於排除兩候選的任意ε來源。

**初步支持：** 不同拒絕列的可省略單容量因子身份不能重用；
unary的未用色D身份不能跨列交換；941 t=1的共同三葉支援已迫六跨度。
**未完成：** t=2的兩條spokes可能改變支援成本，不能照搬t=1計費。

**實驗：** 固定同一binary原分量及全部附件，先分「q₀/q₁都省略spoke」
與「一列省略unary」，核對十列關係及原省略身份。
反例必是同一具名disk source的完整Σ與刪邊見證；必要色角色表存活不算反例。
若沒有反例，第一步只要求完成t=2排除，不提前宣稱ε≥2。

### H2：no-mixed的分離機制可沿degree-5 root樹合成

**候選陳述。** M為T4全收的C₅ disk minimal q-obstruction；
所有有效內點degree為4或5，R為非空degree-5點集，M[R]為樹；
H−R每個原分量只接一個root。則M接受singleton位置與q相鄰的兩個三色列。

這精確保留no-mixed、原分量及T4前提，不包含有環root骨架、mixed、degree≥6。
若成立，在來源另有相鄰雙缺失時可用既有接合定理擴大單側出口可處理類。
它不自動提供共同出口。

**初步支持：** |R|=1由唯一degree-5結果涵蓋；|R|=2由相鄰雙root
no-mixed完成。任意root樹已有source κ=0與邊標色的緊list描述。
**真正缺口：** source邊標色不能直接搬到target，兩側root的五邊跨度證明
也不能對多root各自複製後相加。

**實驗：** 先做三root路徑，逐側保留完整半樹端點訊息及一份共同環序，
而非把三份單root禁色邊際獨立拼起來。輸出target異色接合見證或同圖
來源矛盾；有限支援未發現反例只支持這個三root域。
弱化版本可先增加「每root至多一份不能跨列搬運的原分量」前提，
但此條件在一般樹也須另證，不能沿用雙root界當作已知。

### H3：完整Σ可能決定weak-deletion的第一個可見出口

**候選陳述。** 若G、H都是指定有序C₅ disk圖，且Σ(G)=Σ(H)，
則在保留框邊及全部頂點、允許先silent刪邊再第一次strict enlargement
的語義下，W(G)=W(H)。兩圖的私有內點數可不同。

這是既有[weak quotient](c5_weak_quotient.md)觀察的普遍化，
不是本輪新證的結論。它若成立，會把多種同class來源族與出口研究直接接上；
配合逐目標的證明仍需另外確定W的內容。

**初步支持：** 封存k≤3域的87個observed relations有一致的W。
**反向壓力：** 完整Σ相等只保證外部延拓行為；刪邊會打開原先密封的內部。
非同面控制已顯示disk前提關鍵；固定Kempe摘要也已出現同state不同後繼。
後者不是H3的直接反例，但足以禁止從靜態替換定理推出H3。

**實驗：** 選既有同class的兩個小代表或一次密封替換前後，對一個指定
出口τ保存完整minimal-obstruction族／critical-edge判定。
不只比較Σ、J或repair形狀，也不以找到一條路徑代替完整W。
若失敗，保留同Σ不同W的兩張disk圖及不可達證書；轉向保留具名臨界
obstruction資料的摘要，而不是再增加未說明語義的mask位元。

## 6. 當輪建議：什麼值得先做，什麼可以等實驗

以下保存 2026-10-02 當輪建議順序。現行排程統一由各線導覽維護，
不以此表作為最新 frontier。

| 優先方向 | 為何值得做 | 最小完成／停止條件 |
| --- | --- | --- |
| 941 ε=1的t=2（後續已完成） | 當時直接延伸同源core工具；驗H1的最窄分支 | 原停止條件為完整原關係＋共同支援的來源排除，或一份無法排除的具名必要配置；後續[t=2](c5_941_two_spoke.md)及[t=3合成](c5_941_three_spoke.md)均已完成 |
| mixed P₃共端點 | weak-deletion當前窄缺口，與同源幾何框架相容 | masks=(0,0,3)及反向型；保留原P₃與(3,2,1)實際附件，不能換成singleton |
| 五階來源的少量兩點接合 | 新初驗已把可能r*=5的來源縮到20類／4軌道 | 明列實際合法框族後的完整r*，或附原圖延拓的五階下界見證 |
| 三root no-mixed路徑 | 檢查雙root機制究竟能否沿樹合成 | 只報三root域，不從有限表宣稱任意root樹 |
| 同class不同實現的W比較 | 直接測H3，判斷靜態語義能否升為刪邊動態摘要 | 完整出口判定／反例，不只一條成功操作歷程 |
| Lean具名D₁₃替換接線 | 把既有局部定理接回原U上的J／指定框P，成本邊界清楚 | 端到端具名relation保持；disk框族仍另證 |

不建議立刻重啟更大k圖枚舉，或以「找到更多等價補片」作為所有來源
可化約的替代證據。若目標是repair不變，式(1)與框族證書已提供較直接接口；
若目標是K∞=K≤5，仍應追蹤933／941的同源矛盾，而非把靜態階數當幾何判準。

## 7. 本輪產物、重播與證據邊界

新增[階數推導與初驗](c5_relation_arity.md)、
[checker](../scripts/c5_relation_arity_audit.py)及
[127 KB級證書](../artifacts/c5_relation_arity/observations.json)。
只從既有132份關係、20個五階原圖、六個接合圖與其具名框證書做重播；
沒有新增class pair、拓撲普遍性或Lean theorem。

```bash
python3 scripts/c5_relation_arity_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_relation_arity_audit.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

執行結果、Lean build及未重驗範圍見[本輪紀錄](history/2026-10-02-c5-research-synthesis.md)。
以上保存當輪假設與初驗；H1 已在後續固定來源前提下成立，H2、H3
及一般推廣仍未證；普遍四階來源說法已在當輪淘汰。

## 8. 2026-10-04 新猜想（基準 `0b5e00a`，未證）

本節依[盾弧預算與 hub 原則](c5_unary_shield_budget.md)、ε≥2 案例樹與
[開放葉 ledger](c5_open_leaf_ledger.md) 提出四個可反駁猜想。全部**未證**；
排程仍由 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口) 維護。

**方法界線。** 前提 (S) 下的命題，若主命題成立便因 933／941 無來源而空真，
所以只在 (S) 下「沒找到反例」不提供資訊。下列每個猜想都附一個在**可實現**
圖類上可反駁的版本，用來校準證明能否只靠局部機制。

### 8.1 猜想 E：超額–拒絕定律

記 Q(G) 為**被拒絕**的三色 singleton 位置（P(G) 的補集），c(Q) 為 Q 在 C₅ 上的
連續弧段數，e(Q) 為兩端都在 Q 的框邊數。

> **猜想 E。** G 為指定有序 induced-C₅ disk 圖，T4⊆Σ(G)，每條非框邊 Σ-critical。
> 若 1≤|Q|≤4，則
> \[
> \varepsilon(G)\ \ge\ (|Q|-1)+(c(Q)-1)\;=\;2|Q|-e(Q)-2 .
> \]
> 即：第一個拒絕列免費，之後每多一列花一單位，每多一個不相鄰的拒絕弧段再花一單位。

| Q 的形狀 | 代表 mask | 猜想下界 | k≤5 目錄最小代表的 ε（度數） | 已知證明 |
| --- | ---: | ---: | --- | --- |
| 一點 | 959 | 0 | 0（4,4） | — |
| 相鄰兩點 | 943 | 1 | 1（4,4,5） | — |
| 不相鄰兩點 | 951 | 2 | 2（4⁴,6） | — |
| 三點弧 | 935 | 2 | 2（4,5,5） | — |
| 兩點弧＋孤點 | 941 | **3** | 無代表 | ε≥2 |
| 四點弧 | 933 | **3** | 無代表 | ε≥2 |

**支持。** (i) ε=0 時由[全 degree-4 結論](c5_degree4_guide.md)：H 為單一全 degree-4 分量，
飽和使每個拒絕列的 minimal core 都是 G 本身，故 Σ=Ω∖{q}、|Q|=1，與 E 相符（此推導待寫成正式段落）。
(ii) 933／941 的 ε≥2 與 E 相容，但比 E 弱一單位。
(iii) **非正式 scratch 檢查**：對目錄中全部 20 個 T4 全收、Q 非空的固定標號類，
從其 witness 以 40 種隨機次序貪婪刪除保持 Σ 的邊，得到的最小 ε **全部恰等於** E 的下界。
這只給各類最小 ε 的上界、只看單一 witness 的子圖，不是窮舉，也未存成 checker／artifact。

**若成立。** 933、941 都需 ε≥3，現行整棵 ε=2 雙 root 案例樹（A／B 系列的 16／20 殘留等）為空。
E 也把「H1：ε=1 無法承擔獨立 singleton 支撐」推廣成對所有 Q 形狀的一條加法式。

**反駁與第一步。** 反例是一張 Σ-edge-minimal、T4 全收、ε 低於下界的 disk 圖。
(T1) 先在 ε=1 層驗：用 941／933 的 ε=1 工具（[四容量子覆蓋](c5_excess_one_subcovers.md)、t=1／2／3 分拆）
證明 Q 為不相鄰兩點或三點弧時 ε≠1。這兩類**可實現**，所以證明不能偷用不可實現性，是校準。
(T2) 把上述 scratch 檢查改寫成具名 checker，並在不重跑大枚舉的前提下補小 k 的完整 minimal 代表。
機制線索：相鄰 singleton 列只差一條框邊上的雙色交換（例 01012↔01021），可共用 core；
不相鄰者不行。這正是 E 中 c(Q) 項的來源候選。

**後續（2026-10-04，任務 E1）：** [有限證據報告](c5_excess_rejection_law.md)完整窮舉有效內點 k≤5（排除孤立內點）的 T4 全收、Σ-edge-minimal disk 圖，310 個私有重標號類全部滿足 E，無反例；四種可實現形狀的最小 ε 恰為 0、1、2、2，下界是緊的。兩點弧＋孤點（941）與四點弧（933）在 k≤5 無合格圖，這不構成 ε≥3 的證明。整合者已重播 `--check`（一般與 seed17）及獨立 k=3 原始稽核，全部相符。任意大小的 E 與 k≥6 仍未決。

**後續（2026-10-04，任務 E2）：** [ε≤1 層報告](../artifacts/c5_excess_one_e2/REPORT.md)證明 E 在 ε≤1 成立：(a) ε=0 ⇒ |Q|≤1（補齊 degree≥4、H 連通與飽和）；(b) ε=1 ⇒ Q 為一點或相鄰兩點。935 由「每個拒絕位置都有拒絕鄰點 ⇒ 各列有真子核心」加原 K₃,₃ 排除；951 因拒絕位置互不相鄰，G 可能同時是兩列的 minimal core，需新增雙列 full-minimal、Gallai palette 與盾弧論證（§5.1–5.4）。雙列論證只假設兩個指定列拒絕及 T4 全收，故也涵蓋含不相鄰二點的較大 Q。任意大小紙面化約＋外部 Gallai＋五個新 checker；整合者重播五個 checker（一般與 seed17）並手驗 §2、§4 的 K₃,₃、§5.1 的 palette 表。[D₇ 稽核](../audits/2026-10-04-task-d7/REPORT.md)逐格／逐步確認 (a)、(b)，含 §3.3 每格引用前提、§5.2–5.4 與「ε=1 確被實質使用」；舊 one-pendant 產物層已標為被 terminal-block 層取代（報告 §9）。

**對 ε=2 樹的含意。** E 的 ε=2 層恰等於「ε=2 時不出現 941 形或四點弧 Q」，也就是現行 ε=2 雙 root 樹的目標；E2 的寫法（只假設指定拒絕列＋T4）可作模板。E1 的 Σ=935 代表（4,5,5）正是兩相鄰 degree-5 roots，所以它是 ε=2 雙 root 樹的**正控制**：任何不用到 933／941 特定拒絕列的引理，都必須容許這張圖。

### 8.2 猜想 S：所有 one-sided 分量都有長盾弧

> **猜想 S。** 前提 (S) 下，沒有 one-sided 分量（unary 或 mixed）的實際支援包含於一條框邊的兩端點
> （含空支援與單點支援）。等價地 |σ_P|≥2。

unary 部分即定理 A 第 1 點；推論 B2 處理 roots 同色；剩下的正好是導覽現行入口「雙色 roots 的 hub linkage」。
**若成立**，由 Σ|σ_P|≤5，當 G[R] 連通時全圖**至多兩份分量**，且 spokes 落在 2–3 個框點；
A₄ 殘留中 C 支援為 {0}／{4} 的框架直接消失。
**校準：** 在可實現的 T4 全收 Σ-edge-minimal 圖（8.1 表中各類及更大代表）找短支援 one-sided mixed 分量。
若存在，S 的證明必須用到 933／941 的特定拒絕列（見 8.3），不能只靠 hub linkage。

**後續（2026-10-04，任務 S）：** [校準報告](c5_shield_calibration.md)否定可實現圖類上的推廣。
具名反例 S935／P0={5}：Σ=935，三內點三角剖分，單一 degree-4 點 5 接框邊 34 與相鄰 roots 6、7，
盾弧只有框邊 34，每條非框邊均 critical（另經整合者獨立重算 Σ 與 criticality）。
21 張圖中有 5 份短 one-sided mixed，全屬 935 的同一 D₅ 軌道（Q 為三點弧、兩相鄰 degree-5 roots，與 933／941 的 ε=2 樹同型 root 結構）；unary |σ|≥2、支援連續、盾弧互斥及至多兩份 unary 均無違反。
**原文 S（限定 Σ=933／941）仍未決**，其證明必須用到這兩類特有的拒絕列。
S935 正是「hubs 無法組成」的最小實例：點 5 四鄰 3、4、6、7 依環序排列，對角 3／6、4／7 不相鄰，
可直接作為猜想 K 的測試案例。

### 8.3 猜想 K：交錯阻擋只能靠框上 Kempe 轉運存活

設 P 為 one-sided，S_P⊆{a,b}，ψ 是 P 對列 q 的拒絕見證，相鄰 roots 用兩色。
紙面觀察：若交換 G−P 中某條雙色 Kempe 鏈後的 ψ′ 可延拓到 P，則新框列 q′∈Σ；
若 ψ′ 符合定理 B／B2 的 hub 條件則直接矛盾。故阻擋要存活，所有有用的交換都必須碰框，且送到 Σ 內的列。

> **猜想 K。** hubs 無法組成時，存在碰框的雙色 Kempe 鏈，其交換對應 q 的一個 noncrossing
> block swap（[Kempe screen §2](c5_kempe_screen.md#2-kempe-必要性為何與內點數量無關)）。
> 因此 hub-linkage 的阻擋型可由有限表 {(q, 色對, block) : q∉Σ, q′∈Σ} 索引；
> 對 Σ∈{933,941}，兩側（a 側與 b 側）所需的鏈在 disk 中必交錯，故阻擋不存在。

**反駁：** 一份交錯見證，其所有觸及 N(P) 的 Kempe 鏈都不碰框，且內部交換不能打破交錯。
**第一步：** 用既有 [Kempe screen](../scripts/c5_kempe_screen.py) 的 partition 生成器列出上述有限表（不需圖枚舉），
再仿[盾弧報告 §7 Part B](c5_unary_shield_budget.md#7-有限控制與重播) 做小型 wiring 控制。
K 若成立即完成導覽入口的「不可組成 ⇒ 明列阻擋型」並同時給出 S。

**後續（2026-10-04，任務 K）：** [轉運報告](c5_kempe_transport.md)建好 933／941 各 20 筆單 block 轉運表，
共同 partition 的 a／b 候選全部非交錯；|P|=1 控制只得 Σ=1012 的停止見證 P1-witness-001，
無 hubs 也非交錯型（整合者另行重算 Σ、criticality 與九條 Kempe 鏈，結果相符）。
解讀：|P|=1 時交錯環序在幾何上不可能，真正的阻擋是對角 Kempe 鏈斷開，而每條能延拓 P 的交換都碰框且落在 Σ 內，
恰為 K 的轉運部分。精確化的 K′ 已登記於 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)。固定 933／941 的 K 未決。

### 8.4 猜想 W：盾弧預算移植到單列 q-core（weak-deletion 線）

**引理草稿（紙面，待與既有報告核對）。** M 為 T4⊆Σ(M)、induced-C₅ 的 minimal q-obstruction，
s(q) 為 q 的 singleton 位置。則 B∖{s(q)} 的每一框點都有內部鄰點。
*證明草稿。* 設 v≠s(q) 沒有內部鄰點。v 在 q 中屬重複色，把 v 改成 q 未用的第四色得 q′，
仍是合法框列且屬 T4⊆Σ(M)。q′ 的任一延拓不碰 v，限制後就是 q 的延拓，與 M 拒絕 q 矛盾。∎

> **猜想 W。** 在上述 q-core 中，引理 1、引理 2 與定理 A 的盾弧預算成立，唯一例外是盾弧內點恰為 s(q)。

**用途與界線。** 這會讓任務 C 的共鄰 P₃ 目錄（3,497 個開放 keys）可用「支援連續＋盾弧互斥」一次批量篩，
而非逐 geometry／join 處理。實際能刪多少取決於目錄中支援的稀疏程度，本節不預測數字。
先需核對任務 C 的分量是否 one-sided、內部是否連通。

**後續（2026-10-04，任務 W）：** [q-core 盾弧預算](c5_qcore_shield_budget.md)確認改色引理已見於
[未接內點報告](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)，W 成立但須保留 singleton 缺點：
S_P⊆V(σ_P)⊆S_P∪{s(q)}。任務 C 全部分量 one-sided；更強、不需 T4 的定理 C-W 以 2+2+2>5
把共鄰 P₃ 目錄 3497 keys 全部作來源排除。這比本節預期強得多：不是批量篩掉一部分，而是整個目錄清空。
[D₆ 稽核](../audits/2026-10-04-task-d6/REPORT.md)逐項確認，補零-unary 側後涵蓋 C §1 整個共鄰端點 P₃ 分支；verdict 因盾弧文件 1(d) 更正而改為修訂版，舊版保存為 v1。

### 8.5 建議順序與證據界線

hub linkage 是使用者已登記的現行入口；K 是它的精確化，S 是它的推論，不另開工作。
E 是新方向，若 T1 成功，可能使整棵 ε=2 樹不必續拆；建議在 hub linkage 之後或並行，由使用者決定。
W 屬 weak-deletion 線，成本低，可作 ledger 的第一次批量篩。

本節只有紙面觀察、證明草稿與一次未存檔的 scratch 檢查；沒有新 checker、artifact 或 Lean theorem。
