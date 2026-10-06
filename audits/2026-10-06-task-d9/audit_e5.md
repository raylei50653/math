# D₉：E5 L1–L8、四分支與 G2–G4／no-mixed 的獨立稽核

2026-10-06；所有原文行號固定於 `b2ca4520da50c9d2898ac6f8f966ac25df3f9609`。
本文審查 [E5 REPORT](../../artifacts/c5_excess_two_e5/REPORT.md)；G2–G4 的新盾弧限制與
no-mixed 預算實際寫於 [E6 REPORT](../../artifacts/c5_excess_two_e6/REPORT.md)。
遵循 DOCUMENTATION 的紙面／外部 Gallai／固定 Python／Lean 信任界線；沒有新證明輪次、
四色定理 oracle、來源圖搜尋或 Lean build。所有新增檔案均只屬 D₉ 稽核交付。

**本專題 verdict：holds。** 在原文完整來源前提及所引用的外部 Gallai／hub／低 ε 結果下，
L1–L8、四分支依賴表、G2 二邊盾弧、G3 四份具名支援、G4 三邊盾弧與 no-mixed
必要預算成立。未發現新的數學缺口或反例。原 G1–G4 的來源 coverage 殘留仍是殘留，
不把 necessary table 或空觸發控制當作來源排除。

## 1. 前提與逐引理 verdict

共同來源 S：有限簡單 induced-C₅ **disk 外框**；T4 五列全部接受；每條非框邊
Σ-critical；ε=2；相鄰 roots a,b 各完整 degree 五，其餘有效內點完整 degree 四；
固定 q₀,q₁,q₃ 拒絕。H 連通與全 B-touch 來自 E3 的既有來源結構。
需要 minimal-q 時必另取原同圖 core 並核對，不能從 Σ-critical 自動得到。

| 項目 | scope | verdict | 固定原行號與一行理由 |
| --- | --- | --- | --- |
| 四互斥完整分支 | S | holds | E5:32–48；optional 位逐支給定，940 用同一整圖反射搬運全部角色。 |
| 四分支依賴表 | S 與各具名 incidence／frame | holds | E5:50–77；「局部證」和 coverage 分開，932 的強化只用增加拒絕列。 |
| L1 | ε2 proper S；ε0 的 degree-valid S | holds | E5:81–97；minimal pair-core 自身 critical，ε2 飽和迫回 G，proper 拒絕域至多相鄰 pair。 |
| L2 | J2 mixed12；J3 binary／ternary 的原 incidence | holds | E5:103–123；原長環或兩個共 root 三角排除後續全四 core，供應所需 q-minimal 身份。 |
| L3 | J2 mixed11+unit U；J3 binary | holds | E5:127–138；相鄰 pair 不能共用 unique5 minimal core，J2 的全四 M−U 身份至多拒一列。 |
| L4 | L3 兩類、全部十份三-spoke 集 | holds | E5:142–158；同色 guard 冗餘得到必要域 4/2/2/0，932 才是整型排除。 |
| L5 | J3 mixed12+unit U ternary | holds | E5:162–176；同圖 K 三 contacts 的兩禁色、獨立 U singleton 使 active triangle 原 K₅ 適用。 |
| L6 | A=C12+a-unit U，兩側各二 spokes | holds | E5:182–206；C12 排全四，three-contact 定理使 N 與兩 a-spoke omissions Ω，真直積給 singleton identity。 |
| L7 | A 的 S_a=S_b，含非框 pair | holds | E5:210–218；完整 disk skeleton 封 C 於原三角，替換整份 C 恢復原 ax。 |
| L8 | B=C22、無 unary、兩側各二 spokes | holds | E5:226–299；共同 pins tightness、owner signatures 與全部 terminal blocks 給原 K₅，無原 key coverage 假設。 |
| no-mixed 預算（E6-D） | S 且 m=0 | holds | E6:121–145；兩個完整原側的盾弧成本，941 三-spoke 僅013，其他三支各側≤2。 |
| G2／G3 二邊 U（E6-E） | G2／G3，前三支 | holds | E6:149–161；三邊 gap 被 U 佔滿時 C 至多 singleton 支援，指定重色列三 hubs 迫接回。 |
| endpoint 引理（E6-F） | 原 unary 支援恰三點；H−U 連通、全 B-touch | holds | E6:163–175；原 pin-only bags 保完整 degree lists，無需 owner 色先延拓 G−U。 |
| G3 named supports | G3 與前述二邊 U／endpoint | holds | E6:177–192；F_K⊆L 而非等號，endpoint 禁色逐份留下 012/034、123/034、014/123、034/123。 |
| G4 三邊 U（E6-G） | A unequal pairs，四支 | holds | E6:196–226；真 singleton 與同圖 block membership 排二邊；a-incident faces 排全 B，故只餘三邊。 |

## 2. 四分支表及外部前提使用

E5:21–26 明列三列拒絕、T4、原 criticality 與兩個 degree-five roots。
E5:32–41 的 941／933／940／932 沒有默補 q₂/q₄ 接受；它們是完整 mask 的四個互斥情況。
E5:43–48 的反射 φ=[1,0,4,3,2] 同時搬列、附件、root roles、rotation 和字面色。
重新讀取十列只為 boundary S₄ 軌道索引，不能獨立正規化分量。
獨立 checker 重算四個 Q、十列 literal transport、所有十個三-spoke S 的 D_e。

E3 REPORT:96–111 的飽和比較、adjacent_notes:31–34 的 root／ab 全收與雙-spoke
三列必要表在實際 core 上使用；M 自身的 minimality 每次另證。
D₈ supplementary degree-six 表未拿來替代任何 E5 局部 shape、contact 或 relation 前提。
兩 roots degree 五是 E5 明列來源，該表不是 L1–L8 的新有限計算依賴。

E5:68、217 僅在原 A／A₂ 的具名 01/23、01/12 圖形下引用指定三列的局部出口。
E5:69、158、218、307–308 保留 unequal coverage 與 binary schemas；沒有把原 A 的70/90、
B 的47/75 或 binary 的116/256→32/64 ledger 填成新來源 completeness。
L6 補足 A 必要的 NΩ／singleton 前提；L8 自行處理全部框邊 pairs 的原幾何，
沒有將 B₄ 的十三附件縮表或第四拒絕列拿來排其他原附件。

## 3. L1–L5 逐步檢查

**L1。** E5:82–84 先取保留非相鄰拒絕 pair 的 inclusion-minimal M。
刪點補色使有效內點 degree≥4；刪任一非框邊須釋放該 pair 一列，故 M 自己 Σ-critical。
T4 接受與 induced disk 均由原 G 的延拓限制繼承。
E5:86–88 使用對原有效點集的 ε 比較；ε(M)=2 時两個 surplus roots 完整保留，
原 H 的 degree-four 飽和傳播迫所有原邊／點回到 M，與真子圖矛盾。
所以 E2 適用於 M 的 ε≤1，得到不能拒絕非相鄰 pair；C₅ 上任何三點集含非相鄰 pair，
因此 proper S 的 Q 只能空、singleton、相鄰 pair。
E5:92–93 另以 degree-valid ε(S)=0 比較 minimal pair-core，得到 ≤1。
未把任意省略圖本身未驗證的 criticality 填入 E2。

**L2。** E5:103–104 由 root／ab 全收保留 a,b,ab；保留任何 degree-four 原點
即保留整份原 piece。C12／C22 中取另一側 contact x 與不同 y，原 C 路加 ax,yb,ab
是長至少四的環；允許 x 與另一 contact 共享原頂點，但 x≠所選 y。
E5:110–113 對 binary C11 若全四，先迫共享 x 的 abx 原三角，再以 binary-U 的
b–u↝v–b 原環排長環或兩三角共享 b；U 容量二不能以單一 b incidence loss 省掉。
E5:115–117 因 a 已四，C 全保留，上述情況覆蓋 b 是否再降四，故 M 自己 minimal。
J2 mixed12 無 U 的三 contacts 是 a,y₀,y₁，三個原頂點互異；q-minimal 迫兩 b-spokes
異色，符合 [two-spoke 三接點 theorem](../../docs/c5_two_spoke_three_contacts.md#5-second-rows-scope-and-remaining-cases)
的任意不同色 spokes 範圍（該文件:180–185 明列全部two-spoke，含先前非相鄰情況；
:28–37 的三contacts前提不要求其中某contact為leaf）。這一步只作同一全域顏色換名，
不把非相鄰框點搬成相鄰。原active-block／三arm提取只用同一K的三contacts與两禁色；
最終K₅的B袋連通及root–B接線也不要求兩spokes在框上相鄰。
每個三-spoke 集的指定三列之一有重色，故整型排除。

**L3。** E5:128 先用 L1 排非相鄰 pair。E5:129–130 的 unique5 theorem 只套
該 q 自己的 minimal core；其接受 q 的兩框鄰列，使相鄰 pair 不可能共享同一 minimal M。
J2 proper core 保 a 與 C，b 再降度只能一 b-spoke 或整份 unit U。
前者正是 E3 既有 retained-mixed 雙-spoke 三列排除；後者唯一原身份 M−U 全 degree 四。
拒絕時原 H 的飽和使 minimal core 取整份 M−U；E2 ε0 只能單拒絕，故不能供兩列。
J3 binary 已由 L2 取得 M 自己 minimal，直接用 unique5 相鄰列分離。
結論是 |Q_M|≤1，並非 Σ(M)=Ω；原951的非Ω省略警戒沒有被刪除。

**L4。** E5:144–146 的同色 spoke 冗餘在同一 β、同一圖成立：該兩 spoke 的 root
不等色 guard 相同，刪其中一條不改 full Col。故 D_e⊆Q_M，L3 才給 |D_e|≤1。
獨立十集逐spoke算術得到941的012/014/034/123、933的012/123、940的014/034、932空。
它只約束 J2 unit-U／J3 binary 的三-spoke 集；不能擴到未知 J6 或從4/2/2推源可實現性。

**L5。** E5:162–165 的 M 為同一重色原 a-spoke omission，由 L2 minimal。
M−b 的 K=C+a 与 U 是互斥原分量；a,y₀,y₁,u 皆為原角色，前三 contacts 互異。
a 在 K 是 leaf，兩保留 spoke 使 L 兩色；d∉L 時其 list slack 保證接回，故 F_K⊆L。
單 contact U 的完整避色 ≤1，b 的合法域 A 三色；拒絕迫 F_K=L⊆A、F_U=A−L。
實際不可著色的兩份 K lists 與同原 block palettes 才推出 active triangle／三 arms／tethers。
原 single-spoke(3,1) theorem 可整圖 D₅／全域換色命名 q，不讀 optional 列；
它不需要 a 在 K 是 leaf，僅三 contacts、完整 degree-four、两禁色及原至少一 spoke。
K₅ 只用來否定 planar 來源，不當 boundary Σ 或 T4 的 invariant minor。

## 4. L6–L8 逐步檢查

**L6。** E5:183–186 的 N−a、N−b、N−ab 由對應原全收圖再刪 U，故 Ω。
任何 N 拒絕 q 的 core 都保 a,b,ab；a 已四保 C12，b 的後續全四由原長環排除。
因此 N 自己 minimal；N−b=C+a 是三接點，two-spoke theorem 排之。
M=G−任一 a-spoke 也保留原 C、U；M−b 是连通 C+a+U，其 contacts 仍 a,y₀,y₁。
a 此時內度二不影響 theorem。T4 五列本已由子圖繼承，假想拒絕只可能三色列。
E5:191–192 的 U−au contact 有 slack，全部 R_U 非空；不將已降三的 u 稱 minimal。
E5:196–200 保留完整 J_(G−au)=T_N×R_U，原 G 只是同一 au 不等 guard。
拒絕時每份非空直積對都須 a=u；取任意 pair 即迫兩非空投影同一 singleton。
獨立225對 domain 算術只有四組相同 singleton 給空 guard；这是投影真完整 joint 後的結果。

**L7。** E5:210 的封閉使用**完整 B disk 外框加 diamond**：B 的兩條 h↝k 框弧
把 diamond 的外側區域分成只含 a 或只含 b 的面；能容納同一 mixed C 的共同面
只剩 hab、kab 原三角。一般 planar 指定 C₅ 未作外框時不得沿用這一步。
三個原 hubs a,b,h 的三條邊存在，合法外染色使三色互異。
若拒絕 C，exact list tightness 保 degree；Gallai／三-hub 給原 K₅。
因此对 G−ax 的**整份** witness 只替換完整 C、其餘原點固定，可恢復 ax，違 Σ-criticality。
不借 NΩ、不以 root 或 contact marginals 自行拼接；pair h,k 是否原框邊不是封閉的前提。

**L8 骨架。** E5:226–230 對四原 spokes 的 M 用 C22 長環取得 q-minimal，
three-contact two-spoke theorem 得每份 omission Ω。任何非框 pair 在指定三列之一重色，
所以兩原 spoke pairs 必框邊。C22 不可省略，proper q-core 只可省spoke，故原 q-core=G。
G−C 的每 root 合法域至少二，有合法不同色 pins；每個原拒絕 q 阻擋每份合法 pin。
exact list≥deg_C，連通 slack 迫 tight 與 Gallai；B+a+b 連通給 K₄-free。
全部三框點在某指定列重色、全部非框 pair 在某列重色，actual 附件最多兩點且二點必框邊。

**L8 owner 與 odd cycles。** E5:246–260 的兩 pins (d,h_b),(h_a,d) 合法且對 d 的
membership signatures 四種互異。leaf private points 的同一 block list 才迫 owner 類相同。
三列 column／unordered edge signatures 單射，迫单 owner 同一实际 h，無 owner 同一框邊 hk。
單一 odd-cycle 的非空 owner 至多兩 private 點，與至少三點矛盾；無 owner 則沒有必要root contacts。
多block leaf 取相鄰 private u,v，C′ 非空連通。
無owner時 u,v,h,k 為原 K₄，C′保全部root contacts，至少一spoke接補框路，故第五袋連通。
单owner时 u,v 用盡该root的兩 contacts；另一root contacts保在 C′。
兩不同原框邊 pairs 到任意 h 都能選只於 h 相交、各避另一root的原rootcycle paths；
獨立 checker 對全部100份有序框邊pair×h保存實際兩路及互斥檢查。
shared时 u,v,a,b 為 K₄；roots spokes合共至多四框點，full B-touch迫C′另碰框，故C′∪B連通。
三種情況十對 branch-set 邻接皆由原 edges 提供。

**L8 bridges。** E5:282–296 的 private leaf 完整 degree四給：無owner三框附件違tightness；
singleowner二附件必框邊，a=d pin與三列edge signatures迫附件就是S_a，
但完整disk skeleton 的共同face不含該spoke edge兩端。
shared叶恰一原框附件 h；K=C−v 非空連通，剩兩root contacts＋vK共三條cut邊，
4|K|=2|E(K)|+3+n_B 迫 n_B 正奇數。五袋 a,b,v,B,K 均連通且十對邻接都有原邊。
h 可以是任何原實際框點；没有借旧{4}附件篩選或 q₂/q₄ 的角色。
C22 非singleton，K₄-free Gallai 的 terminal blocks 已由 bridge／odd-cycle 覆蓋，整型排除完整。

## 5. E6-D/E/F/G：預算與 G2–G4 推論逐步

**no-mixed。** E6:121–125 使用 t_r≤3（T4）與每侧容量4，迫每侧至少一 unary；
共同盾弧預算至多兩份，故各側恰一。A_r=root+U_r 與補側皆連通，
shield 引理純拓撲證明可用於整側；此步沒有偷套所有A_r點degree-four的要求。
full B-touch 與三點 unary 支援給每侧 λ≥2 且總≤5。
t_r=3 的 spokes 避 U 的盾弧內點，至多兩条在端點，整側至少四支援點，λ≥3。
於是该側 U 恰二邊、整侧恰三邊，三 spokes 是 U 兩端加第三整侧端點，必非連續。
与**通用 L1** 欄位域相交（不是 E5 L3）只餘941的013，actual U 支援123或034；
獨立 checker 對五個三邊整侧弧及两個二邊子弧逐份算術復核。
E6:135–140 使用完整R_U tuple共同避色。原join=(E_z×E_w)−Δ，ab omission是直積。
只有非空直積被對角阻擋時才推E_z=E_w={c}，不预填c=未用色，不假設root deletions各Ω。
E_r可能空的root例外仍明留；這是必要預算，沒有排除跨列来源。

**G2／G3 二邊盾弧。** E6:150 先讀L3–L4才知a-spokes是連續三點；前三支全部包含於
012/123/014/034。H−a=b+C+U连通，落同一a-star面，gaps為1/1/3。
若U≥三邊，只能佔滿三邊gap。spokes和C附件避其內點；C one-sided 支援連續性，
使C在非相鄰兩端至多單點。兩端在某指定列重色c（非框pair都有指定重色列）。
a有兩合法色、b的spokes只見c而先有三色；完整F_U容量≤1/2，仍可選b並選不同a。
a,b,B為互異色的原三hubs（對C僅見c），或C無框附件時兩root hubs；完整C可接回，矛盾。
所以恰二邊，不借未證省略全收。

**endpoint 引理。** E6:163–175 不要求指定三列拒絕。假設端色d被完整F_U禁止，
owner=d给真拒絕 tight lists。H−U連通，full B-touch迫其碰支援外框點。
端色不同時 Z=(H−U)∪(B−{h₁,h₂}) 由该实际附件連通；Z,h₁,h₂两兩邻接，
對N(U)分別見d,β(h₁),β(h₂)且互異。兩端同色時用Z=(H−U)∪(B−{h₁})及h₁。
tightness已禁止同一U點合袋後兩條外鄰重合，故收縮仍完整degree-four、原list。
即使owner spoke禁d而無原G−U合法外染色，這也是**原圖minor上的局部pin-only**定理；
minor不需要保持boundary patterns或T4。原文:172–174已明說這一點，沒有前提偷換。

**G3 支援表。** E6:177–181 的 marked leaf只給F_K⊆L，已足够。
刪同色端spoke後 a剩端色c與middle色r，L為另兩色。
U二邊弧在長gap的一個子弧，其一端色c；endpoint引理使F_U不含c，F_K亦不含c，
故b原spoke必見c。b合法域是L加r；r需由U禁止，endpoint引理迫r=U內點色。
逐字面query便得原表四列；b-spoke只能取a三-spoke兩端，不能任挑同色別框點。
獨立算術由原五個字面qrows重建四列，不讀原證書的decision fields。

**G4 三邊盾弧。** E6:196 由L6供所有拒絕列真singletonR_U=P_N={d_q}；
L6 a-spoke omissions Ω迫S_a框邊，L7排equal pairs。
若U二邊，端點是非框pair，在某指定q重色。該列U支援只見兩色，
交換兩未見色保持整份R_U，singleton必已見；endpoint再排端色，故d_q=內點色≠3。
所有三份owner=d_q都是**存在的**拒絕tight assignments，非contact lists皆含未用色3；
單接點block-tree固定色引理使用同一原block tree，迫contact的3-membership一致。
所以全部d_q≠3，各列只可能內點色。盾弧內點不在S_a；框邊兩端至少一个與內點非鄰，
指定某列使它們重色，便把d_q变成a-spoke禁色，違真P_N identity。
不同pairs時完整B+a+b骨架的a-incident面都只碰B真子集；Sb非框pair也不例外：
至少一b-spoke接S_a長框弧內部，ab與該spoke分開a-incident面。
連通U经au在其中一面，故S_U≠B；支援區間排長4/5。
剩長3，其兩內點無root spokes，原可用框點h₀,h₃,h₄給S_a兩框邊選擇，
Sb可另框邊或h₀h₃非框pair。沒有把σ=B代入僅適用σ≠B的避內點限制。

## 6. 63 原 critical orbit 控制與三向分類

[獨立 checker](audit_e5_controls.py) 沒有 import 原 producer／checker 的decision logic。
讀取54份E4C的source路徑及9份ES的原canonical_edges／disk_rotation，重新算十列全部完整
assignments、Σ、degree、induced B、H连通、critical edge deletions、原pieces／contacts／supports。
完整tuple保存count／SHA，非pair或contact marginals；原同圖root角色、edges與rotation均記在
[結果](e5_controls.json)。除了原63圖，只有固定字面欄位、225個guard與100份原rootcycle
框骨架的局部算術；沒有新增來源圖枚舉。

下表單位為原 orbit，三欄依序是 `triggered and holds / not triggered / counterexample`。

| 項目 | NA 54 | AD 9 | 精確觸發邊界 |
| --- | --- | --- | --- |
| E5 完整指定三列來源下的 L1–L8、G2/G3/G4/no-mixed 每項 | 0 / 54 / 0 | 0 / 9 / 0 | NA非相鄰；AD的Q均不包含013，故不能稱整型命題已由這63圖驗證。 |
| L1 proper-subgraph 拒絕輪廓的泛用中間機制 | 54 / 0 / 0 | 9 / 0 / 0 | 原ε2/T4/critical；检查所有最大proper edge omissions，其Q子集性涵蓋其他proper子圖。 |
| L1 degree-zero 單拒絕輪廓 | 0 / 54 / 0 | 6 / 3 / 0 | 只枚舉保兩原roots、degree-four的rejecting候選；無候選即未觸發，不涵蓋刪root的cores。 |
| L2 retained-mixed incidence | 0 / 54 / 0 | 6 / 3 / 0 | 上述实际rejecting全四候選；原retained mixed每側contact均一。 |
| J2 a-spoke omission 单拒絕的較弱有限結構控制 | 0 / 54 / 0 | 2 / 7 / 0 | 有原J2 mixed11+unit U形狀才算；未要求013，只是兩圖直接算得的機制控制。 |
| E6-F endpoint 泛用引理 | 28 / 26 / 0 | 8 / 1 / 0 | actual U支援三點、H−U連通、fullB-touch；逐完整relation共同避色排兩端色。 |
| E6-G 單接點未用色membership的泛用中間引理 | 22 / 32 / 0 | 8 / 1 / 0 | actual單contactU、至少兩份真拒絕assignments才比較；只有一份不當比較控制。 |

實際instance數：保兩root的rejecting全四候選26份（全部AD）；endpoint完整relation查詢
NA420／AD140；至少兩份拒絕assignment的單接點U為NA24／AD14份分量、
NA72／AD34份真拒絕assignments。以上instance數不當成新增來源orbit數。

L1 的全四控制由固定incidence unit-factor枚舉，不能暗稱所有root-deletion cores都覆蓋。
G4 singleton整型身份在63圖均未觸發；最後一列只檢查實際單接點U的同圖多拒絕membership，
不代表這些控制實現A或其全三列前提。所有not triggered保存在JSON，不折成PASS數。

## 7. 重播、歷史hash與交付界線

原E5三個checkers各default／seed17：controls兩次exit1，local與branches四次exit0；
每對stdout及stderr相同。controls是既有byte/provenance FAIL，原control payload未被重寫。
[歷史差異](historical_replay_differences.json)明列只變
`/source_sha256/artifacts/c5_excess_two_e3/REPORT.md`：歷史6d385639…，基準現況73ed652a…；
移除此provenance欄後原數學payload相同。這不把嚴格byte FAIL改稱PASS。
原log／exit完整見[原重播](original_replays.json)及最終[validation](validation.json)。

獨立checker可在本worktree執行：

```bash
python3 audits/2026-10-06-task-d9/audit_e5_controls.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-06-task-d9/audit_e5_controls.py --check
```

`--root`／`--output`允許只在稽核新目錄產生結果；不帶`--check`使用exclusive-create，
`--check`不寫來源或artifact。本輪stage實際command、exit與log SHA另存
[e5 independent validation](e5_independent_validation.json)，正式worktree的重播由總validation記錄。
沒有未完成的本專題引理審查；G1–G4未解來源、一般ε≥3、source realizability及未形式化拓撲
均保持原停止點，不屬本獨立audit要補的新證明。
