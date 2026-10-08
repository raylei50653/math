# E4C：E4 不用三列引理的非相鄰正控制補驗

2026-10-04；基準 `integrate-kprime-e3 @ d00aba4e10ea2d05ab216fedd94f5a166b2777ad`。
獨立 worktree `/home/ray/developer/ai/math-task-e4c-controls`，分支 `task-e4c-controls`。
Python `/home/ray/developer/ai/math/.venv/bin/python`（3.14；networkx 3.5），checker 單 worker；沒有 commit／push。

**完成 54 圖 × 60 項不用指定三列的判定表，另列 2 項三列排除版本；沒有反例。**
42 項至少有一份正控制實際觸發前提；18 項仍缺前提觸發，逐項照實保留。
不用三列的 3240 格中：成立 1722，不適用 1518，反例 0。
「不適用」每格附缺失前提；它不代表通過該引理。禁型沒有實例時，不把必要條件的核對冒稱反證分支的實現控制。

## 1. 來源、精確前提與證據層

對照 [E4 REPORT](../c5_excess_two_e4/REPORT.md)、[CORE_CONSTRAINTS](../c5_excess_two_e4/CORE_CONSTRAINTS.md)、
[E3 非相鄰 notes](../c5_excess_two_e3/nonadjacent_notes.md)、[盾弧原則](../../docs/c5_unary_shield_budget.md)、
[Kempe 導覽](../../docs/c5_kempe_guide.md)及 [ES 報告](../../docs/c5_excess_two_finite_search.md)。
逐一讀取 `NA_k{6,7,8,9}_validate/crit_orbits/orbit_*.json` 的全部 54 個具名代表；不擴大圖族搜尋，不把 D₅ 搬運所得代表的 Q 或 Σ 混在一起。
NA6-1＝NA6-0002、NA6-2＝NA6-0003、NA6-3＝NA6-0001；checker 逐邊核對導覽列出的兩份 hex 邊集，並驗 NA6-2 由 NA6-1 的 06 改為 36。

共同控制前提實算：有限簡單、有序 induced C₅ disk、T4 全收、完整 Σ 每非框邊 strict-critical、ε2、非相鄰 degree5 roots=(5,6)、其餘有效內點 degree4。
原 rotation／全部 faces／C₅ 外面一併驗；未使用四色定理 oracle。三列 {q₀,q₁,q₃} 的原來源前提在 54 圖上全都不成立。
本次把 E4 中逐任意拒絕 β 的步驟和真正依赖指定三列組合的步驟拆開；CORE 的 private-spoke、E4-D 保留逐 β 一般化及其原三列限制。

只有 30 圖碰齊五框點；另 24 圖只碰四框點且都是單缺列。全 B-touch 由 |Q|≥2 推出的 A2 在 6 圖觸發，不能在其他圖憑空使用。
支援區間／unary 支援≥3／局部 N-diagonal 明列全 B-touch；純盾弧四項不需要此條。24 圖中的稀疏 unary supports 不構成引理反例。

本報告是固定具名原圖的 Python 證書；任意大小拓撲／Gallai／degree-list 論證仍由原文件承擔。沒有新 Lean theorem，未執行 lake build；不能外推一般 E4、來源完備性或 `K∞=K≤5`。

## 2. 實算摘要

| 項目 | 實際結果 |
| --- | --- |
| NA 層 k6／k7／k8／k9 | 3／2／22／27 |
| (mixed,unary) | (1,0):1；(1,1):4；(1,2):30；(2,1):19 |
| 完整 Σ | 959×8；999×3；1007×6；1015×12；1020×3；1021×8；1022×14 |
| Q 大小 | 48 圖單缺列；6 圖二缺列 |
| 非框刪邊完整 Σ／新列 full witnesses | 1289 次／1385 份，全部 strict-critical |
| 原 root 刪除 | 108 次全為 Σ=1023；逐列逐 surviving-root pin 與原 side 一致 |
| 每實際拒絕列的全部最小 core | 60 列各唯一；55:48、45:10、54:2；44:0、root省略:0 |
| 45／54 原省略身份 | 8 份 spoke；4 份整 capacity-one unary |
| unit derivatives | 172 份 ε1：160 全收，12 單缺列 |
| 雙側 unit／(1,1) mixed 省略 | 138／2 份，均 ε0且全收 |
| 完整原 local contact tuples | 7373 份，全部伴 full piece lifts；shared contact只一坐標 |
| one-sided pieces | 121 份；盾弧四項均成立，沒有把 sole separating mixed 收盾弧費用 |
| N-diagonal 的嚴格前提 | 11 圖、22 原 mixed、880 個 (β,a,a) fibres，全部非空 |
| 拒絕列重色 spokes | 0；有重色的接受列只控制局部 redundant-spoke 步驟 |

checker 同時算全部 proper β 的完整 R_P、全部 lifts、各 16 有序 root-pair fibres，以及整圖全部 root-pair 延拓。
刪邊時保留原 pieces／contacts／attachments；完整 relation join 與獨立整圖四色回溯的每個 root pair 相等，不只比較 Σ 空性。

每列最小 core 用全部非框邊刪除遞迴＋memo，degree<4 的私有點先剝離（接回等價）。任何 minimal K 的 degree≥4，剝離不會刪 K；
沿 current∖K 的邊逐一刪除仍拒絕，故遞迴一定到每個 K。每份輸出 core 又用各保留非框邊的全染色 witness 驗 q-criticality，並重算完整 Σ。
unit derivative 的同 Σ minimalization 是另一個演算法：每邊一次貪婪嘗試；已使 Σ 擴大的邊在後續只刪邊時仍有那份新增染色，故最終每非框邊 critical。
它不預設 derivative 自己已 critical，也不把某一 greedy core 說成全部逐列 cores。

## 3. 全部引理／中間步驟的前提與結論

下表中 A–E 共 60 項不使用指定三列的身份或同時拒絕；T1、T2 是明確需要三列的原排除版本，供邊界對照。
來源簡稱：E4＝原 REPORT；CORE＝CORE_CONSTRAINTS；E3 notes＝nonadjacent_notes；shield＝盾弧原則。

| ID | 引理／步驟 | 前提 | 結論 | 原來源 |
| --- | --- | --- | --- | --- |
| A1 | 有效內部／度數下限 | induced C₅ disk、T4、非空 Q、完整 Σ-critical | 有效 H 非空連通，全部有效內點 degree≥4 | E3 notes §1；CORE §1 |
| A2 | 全 B-touch 推導 | A1 且 |Q|≥2 | G 碰齊五框點；單缺列不套這個推導 | E3 notes §1 |
| A3 | spokes 上限 | T4 全收 | 每內點至多三條 actual spokes | E4 §1；CORE §4 |
| A4 | mixed 必存在 | 原 H 連通；z、w 非相鄰 | m≥1，兩側 mixed incidence 都≥1 | E3 notes §2；E4 §1 |
| A5 | 原 piece 分類與容量 | 原 H−{z,w} 完整分量，H 連通、兩 roots 非相鄰 | 各 piece 完整 degree4、owner 非空；t_r+Σincidence=5；unary one-sided；sole mixed separating；m≥2 則全 one-sided | E4 §3、§4.3；E3 notes §2–3 |
| A6 | 完整 literal join | 每 β 的整份 R_P、distinct contacts、lifts、16 有序 pins，同一色框 | (E_z×E_w)∩⋂A_C 恰等於整圖 root-pair 延拓 relation；每非空 fibre 有整圖 lift | E4 §6；CORE §6 |
| A7 | 刪邊 relation 身份 | 同一原圖／β；刪一條非框邊 | contact 僅移除該 inequality；piece 內邊／框附件僅改該原局部 relation；join 精確等於 G−e 完整 Σ | E4 §6 |
| B1 | N-empty-separating | 原 mixed C 的 actual N_B(C)=∅；原來源 Σ-critical | 與 Σ-criticality 矛盾；此 forbidden 配置若出現即反例 | E4 §2.1 |
| B2 | E4-N0／外路 hub 分袋 | degree4 mixed P 無框支援，G−P 有原 z–w 路（可走 B） | 每份合法 outside colouring 能填回 P；其 contact 不會 critical | E4 §2.1；CORE §3 |
| B3 | 無框 appendage 接回 | 無框 mixed C，G−C 不連通；原 H 連通、B 連通、原 G 可染 | 不碰 B 的 root 側 A∪C 僅在另一 root 接合，可一次共同 S₄ 配上 pin；內部非框邊非critical | E4 §2.1 |
| B4 | sole mixed 原外路充分條件 | m=1，C 兩側 incidence≤4，原 unary support 非空 | 兩側有原 C 外 side 因子並經 B 原路連接，G−C 有 z–w 路 | CORE §3 |
| B5 | tree-H Euler 排除 | 原 H 是 k 點 connected tree；內部完整 degree 和4k+2；五框 disk | actual attachment 數2k+4，E=3k+8>disk上界3k+7，矛盾 | E4 §2.2 |
| B6 | N-theta | 同一原 disk 有至少三份不同 mixed 原分量 | 三條 internally-disjoint 原 z–w 路至少困住一整原 piece；该 piece 的 actual support 空 | E4 §5 |
| B7 | 無空支援／非樹／m≤2 必要條件 | 合格非相鄰 Σ-critical ε2 原圖（不預設 forbidden 配置） | 全部 mixed actual support 非空；原 H 有 cycle；m≤2 | E4 §2、§5 |
| B8 | E4-F：K₂,m 面容量 | m≥2；原 disk；每 mixed 有 actual support | 收縮整原 pieces 的 K₂,m：V=m+2,E=2m,F=m，各面4環含2 mixed；B 在一面且所有 mixed 接 B，故 m≤2 | CORE §5 |
| C1 | 盾弧純拓撲四項 | connected 原 P；H−P connected，P 及其附件同一 disk；比較互斥 pieces | 原 σ 連續；|S|≥2 時每支援點incident σ；外部不碰 σ 內點（σ≠B）；互斥 pieces 的 σ 邊互斥 | E4 §3.3、§4.3；shield Lemma1 |
| C2 | 支援等於盾弧頂點 | C1；全 B-touch；|S|≥2 | S=V(σ)，故支援為完整連續區間；不從單缺列假設全框 | E4 §3.3、§4.3；shield Lemma2 |
| C2a | short adjacent-pair 盾長 | one-sided piece actual support恰真框邊兩點，且全B-touch | 盾弧恰1邊 | E4 §4.3 |
| C2b | singleton 盾長 | one-sided piece actual support恰singleton，且全B-touch | 盾弧0邊 | E4 §4.3 |
| C3 | contact 拒絕見證的 tight lists | 原 piece degree4；G−contact 新接受 β 的 full lift；G 拒絕 β | 限制到 outside 後 P 不可接回；每 P 點 list 大小恰為原內部 degree | E4 §2.1、§4.1；shield TheoremA/B |
| C3a | unary forbidden-root 見證 | unary 的 contact 是 Σ-critical | 至少一實際 β 的完整 unary tuples 共同避色集合不是全4，即 F_U(β) 非空 | E4 §4.3；shield TheoremA |
| C4 | unary 支援／盾弧下界 | degree4 unary；critical contact；原 H 連通；全 B-touch | support 不含於任一框邊，至少3個連續框點，|σ_U|≥2 | E4 §4.3；E3 notes §3；shield TheoremA |
| C5 | 共同盾弧總預算 | 原互斥 one-sided pieces，同一 disk | Σ_P |σ_P|≤5 | E4 §4.3；shield Lemma1(d) |
| C6 | unary 個數上限 | C4 下界及 C5，同一原來源全 B-touch | u≤2 | E4 §3、§4.3；shield TheoremA |
| C7 | 兩 unary 容量與外部附件限制 | 全 B-touch，恰兩 unary | 盾長排序為(2,2)或(2,3)；所有 roots spokes／mixed support 避開兩 σ 的內點 | E4 §4.3；E3 notes §3；shield TheoremA |
| C8 | long mixed 盾弧下界 | 原 mixed one-sided，actual support 不含於任何框邊 | |σ_C|≥2；此純拓撲步驟不需全 B-touch | E4 §4.3；shield Lemma1(b) |
| C9 | long＋unary／short-pair 預算 | m≥2，全 pieces one-sided，全 B-touch | ℓ+u≤2；Σlong盾長+Σunary盾長+#short-pair≤5 | E4 §4.3 |
| C10 | 局部 N-diagonal | degree4 mixed one-sided；全 B-touch；actual support 含於真框邊 | 全部10 proper β、全部4色 a，(a,a)∈完整 A_C(β)，不要求 pins 延拓 outside | E4 §4.1 |
| C11 | N2-short-no-unary | m=2，兩份 mixed 都短，無 unary；N-diagonal 前提含全 B-touch | 全部5個三色 β 可用未用色 D 接回 G，故全部接受 | E4 §4.2；與三列矛盾是另一步 |
| C12 | 短 mixed 的拒絕列側交集 | 全部原 mixed 都短且 one-sided；N-diagonal 全 B-touch 前提；β 實際拒絕 | E_z(β)∩E_w(β)=∅；off-diagonal joint 仍須完整保留 | E4 §4.2 |
| C13 | 局部 degree-list slack 接回 | connected 原 degree4 piece；固定 β 及全部 root pins；至少一個點 lists 大於原內部 degree | 完整 P 可接回；不得只看 contact marginals | E4 §3.2；E3 root-deletion |
| C14 | 低 degree root 完整側接回 | 原連通 side S_r：root degree≤3，其餘點 full degree4 | 每 β 的 side 至少一份完整延拓；不是任意預釘 root 色都可行 | E4 §3.1；E3 root-deletion |
| D1 | 原 root 刪除 Σ 身份 | 同一原 β；完整 mixed／unary；刪 w（對稱） | Σ(G−w)=Σ(S_z)，保留原 z 色；S_z root degree=5−m_z | E4 §3、§6；E3 notes §2 |
| D1a | 原 root 刪除 pin 身份 | D1 且指定 surviving root 的字面色 a | G−w 與原 S_z 的每 β／a 接受性完全相同 | E3 notes §2 |
| D2 | root-deletion 单缺列例外 | 原 S_r 實際拒絕某 β | m_r=1、原 side root degree4，完整 Σ 僅缺一列 | E4 §3、§6；E3 notes §2 |
| D3 | 全部拒絕列至多一 root 例外 | 兩原 side 同一 disk，完整 root-deletion 身份 | 兩 side 不會同拒；兩 root-deletion 的拒絕列合計≤1 | E4 §3、§6；E3 notes §2 |
| D4 | m≥2 原 root 刪除全收 | m≥2，故兩側 mixed incidence≥2 | 兩個 G−root 均 Σ=1023；任何拒絕列 core 含兩 roots | E4 §4.3；E3 notes §2 |
| D4a | mixed incidence≥2 原刪root全收 | 任一原側r mixed incidence m_r≥2（允許m1） | Σ(G−另一root)=Σ(S_r)=1023；該root省略不能留下拒絕core | E3 notes §2；E4 §3、§6 |
| D5 | 原 degree4 pieces 全取／全不取 | 任意實際拒絕 β 的 inclusion-minimal qcore；原 P full degree4 | P 完全省略或原頂點／內邊／框附件／root contacts 全保留 | E4 §3.1、§6；E3 notes §5 |
| D6 | 完整原 core 省略身份 | D5；qcore 保留两roots；root degrees只4/5 | 55=G；45/54恰一對應側unit spoke／整unary，所有mixed保留；44恰兩側各unit或一11mixed；保留mixed≥1 | E4 §6；CORE §6；E3 notes §5 |
| D7 | nonadjacent44 retained-mixed 限制 | 兩roots degree4的minimal qcore，兩roots非相鄰 | 恰一retained mixed且各側contacts≤2；m1不省soleC，m2只省一11mixed，m3無44 | E4 §3.1、§6；CORE §6 |
| D7a | 44 contact 原triangle／互斥身份 | nonadjacent44 core之retained mixed | root有2contacts則原contact pair間有實際邊；雙2時兩contact sets互斥，兩原roottriangles以直接原bridge相連且无tails | E4 §3.1、§6；E3 notes §5 |
| D8 | N1 mixed22＋44 原 path 身份 | m=1；sole C incidences22；實際拒絕 β 有兩root44 core | 整原 C 是4點 path；root 各接相鄰2點成互斥triangles，以直接原bridge相連，無tails；terminal各2框附件，內點各1 | E4 §3.1 |
| D9 | N1 mixed22＋44 完整側身份 | D8，原 root degree5 | 每側原capacity3；僅三spokes或兩spokes＋capacity1 unary；原 side 每 β 全收 | E4 §3.1 |
| D9a | N1 side only兩種原型 | N1 soleC22＋44core，无retained tails，原root5 | 每側恰三spokes或兩spokes＋一整capacity1 unary；該unit是原core省略因子 | E4 §3.1 |
| D10 | Σ-preserving minimalization | 原unit derivative X 保留B，有效度數≥4；不預設 X critical | 取同Σ inclusion-minimal Y；Y 非框邊自己Σcritical，有效內點 degree≥4 | CORE §2 |
| D11 | ε 單調的 exact identity | D10；X 所有有效內點degree≥4 | ε(X)−ε(Y)=被省頂點Σ(degX−4)+保留頂點Σ(degX−degY)≥0 | CORE §2 |
| D12 | unit derivative／E2 拒絕位置 | 一原unit side省略ε1；兩側各unit或11mixed省略且有效度數≥4則ε0；同Σ minimalization | ε1的完整Q空／單點／相鄰二點，故不能同拒q₃與q₀／q₁；ε0的Q至多一點 | CORE §2、§4 |
| D12a | E4-U literal單位導數列限制 | D12的有效原unit derivative，不預設原G三列全拒 | 同一原省略圖不會同拒q₃及q₀／q₁ | CORE §2、§4 |
| D13 | 每列 minimal core 自身前提 | 任意實際拒絕 β 的全部 inclusion-minimal qcores | 有效H非空連通、有效內點degree≥4、逐邊qcritical且自己Σcritical | E4 §1、§6；CORE §1 |
| D14 | 省略 root 的 exact side core | 實際拒絕 β 的 minimal qcore 省略一root | 恰原 S_r；另一root degree4，完整 Σ 只缺 β；m1且該側mixed incidence1 | E4 §6；CORE §6；E3 notes §2/5 |
| D15 | N1 terminal 單拒絕列 slack 步驟 | D8 的原 terminal 两actual附件；β實際拒絕 | terminal兩框附件在該β必異色；同色會讓connected C list slack而接回 | E4 §3.2 的單列部分 |
| D16 | N1 bridge 分兩整側的純盾弧 | D8；沿原terminal path中間bridge分原H為两connected互斥整側 | 兩原整側各one-sided，actual盾弧服從C1，邊互斥；此步不收separating C盾弧 | E4 §3.3 的拓撲部分 |
| D16a | generic 原bridge兩整側盾弧 | 原H bridge兩側各connected且各含一root；兩側互斥coverH | 各整側one-sided，其原盾弧連續／支援標記／外部附件限制／邊互斥；全Btouch且支援≥2再得S=Vσ | E4 §3.3 的純拓撲前提 |
| E1 | 逐列 redundant-spoke 身份 | 同root两actual spokes在任意 proper β 同色 | 刪任一其中spoke不改該β接受性 | CORE §4 E4-S 的局部步驟 |
| E2 | 完整Q private-spoke | 原spoke對完整Σ critical | 該spoke至少在一份實際新接受拒絕列有private框色 | CORE §4 E4-S 的一般化 |
| E2a | 所有刪spoke新列均private | β∈Σ(G−spoke)∖Σ(G) | 被刪spoke的框色不被同root任何其他原spoke重複 | CORE §4 E4-S 的局部必要條件 |
| E3 | qcore 不能保留重色 spoke pair | 任一實際拒絕β的minimal qcore | 每root在該qcore中保留的spokes框色均不同 | CORE §4 E4-D 證明中間步驟 |
| E4 | N2 每拒絕列至多一重色 root | m=2；β為任意實際拒絕列（不用三列身份） | 兩roots至多一root原spokes重色 | CORE §4 E4-D 的逐q一般化 |
| E5 | N2 單重色 exact 原 spoke core | E4 且恰一root r有原重色spoke pair | 每 minimal qcore恰G減該pair一spoke，自身degree45/54；該derivative再受D12 | CORE §4 E4-D 的逐q一般化 |
| T1 | 原三列 private-spoke 排除 | q₀、q₁、q₃全拒絕且triple-critical | 每spoke在指定三列至少一次private；原3-spoke024／124被排除 | CORE §4 E4-S，明確使用三列 |
| T2 | N1-22-44 三列整類排除 | 原sole mixed22＋44 core且指定三列全拒絕 | terminal actual pair是框邊；兩整側盾弧各≥3；3+3>5整類排除 | E4 §3.2–§3.3，明確使用三列 |

## 4. 每引理總結與不適用理由

「成立」計數以控制圖數計，不把同一圖的多列／多 pins 灌成多張控制。具體每次前提實例與 witnesses 在對應 `controls/NAk-NNNN.json` 的 `lemmas.<ID>.evidence`。

| ID | 成立圖數 | 不適用圖數 | 總結／全部不適用理由 |
| --- | ---: | ---: | --- |
| A1 | 54 | 0 | 有實際前提控制 |
| A2 | 6 | 48 | 有實際前提控制；|Q|<2；此推導不適用 |
| A3 | 54 | 0 | 有實際前提控制 |
| A4 | 54 | 0 | 有實際前提控制 |
| A5 | 54 | 0 | 有實際前提控制 |
| A6 | 54 | 0 | 有實際前提控制 |
| A7 | 54 | 0 | 有實際前提控制 |
| B1 | 0 | 54 | 仍缺控制；無空支援 mixed；反證配置仍缺控制 |
| B2 | 0 | 54 | 仍缺控制；無空支援 mixed＋外部 z–w 原路；仍缺控制 |
| B3 | 0 | 54 | 仍缺控制；無空支援 separating appendage；仍缺控制 |
| B4 | 35 | 19 | 有實際前提控制；非 sole mixed，或 incidence>4／unary無支援 |
| B5 | 0 | 54 | 仍缺控制；原 H 有 cycle；tree 反證配置仍缺控制 |
| B6 | 0 | 54 | 仍缺控制；m<3；theta 前提仍缺控制 |
| B7 | 54 | 0 | 有實際前提控制 |
| B8 | 19 | 35 | 有實際前提控制；m<2；K₂,m 面前提不適用 |
| C1 | 53 | 1 | 有實際前提控制；無 one-sided piece |
| C2 | 29 | 25 | 有實際前提控制；未碰齊五框點，或沒有支援≥2的 one-sided piece |
| C2a | 11 | 43 | 有實際前提控制；未全框，或無adjacent-pair支援的one-sided piece |
| C2b | 0 | 54 | 仍缺控制；無singleton支援的one-sided piece；仍缺控制 |
| C3 | 54 | 0 | 有實際前提控制 |
| C3a | 53 | 1 | 有實際前提控制；無 unary |
| C4 | 29 | 25 | 有實際前提控制；未碰齊五框點，或無 unary |
| C5 | 54 | 0 | 有實際前提控制 |
| C6 | 30 | 24 | 有實際前提控制；未碰齊五框點 |
| C7 | 14 | 40 | 有實際前提控制；未碰齊五框點，或 u≠2 |
| C8 | 4 | 50 | 有實際前提控制；無 one-sided long mixed |
| C9 | 11 | 43 | 有實際前提控制；未碰齊五框點，或 m<2 |
| C10 | 11 | 43 | 有實際前提控制；未碰齊五框點，或無 one-sided short mixed |
| C11 | 0 | 54 | 仍缺控制；m≠2／有 unary／未全框／並非兩份都短；仍缺控制 |
| C12 | 11 | 43 | 有實際前提控制；未全框，或存在 separating／long mixed |
| C13 | 54 | 0 | 有實際前提控制 |
| C14 | 54 | 0 | 有實際前提控制 |
| D1 | 54 | 0 | 有實際前提控制 |
| D1a | 54 | 0 | 有實際前提控制 |
| D2 | 0 | 54 | 仍缺控制；兩份原 root-deletion 都全收 |
| D3 | 54 | 0 | 有實際前提控制 |
| D4 | 19 | 35 | 有實際前提控制；m<2 |
| D4a | 54 | 0 | 有實際前提控制 |
| D5 | 54 | 0 | 有實際前提控制 |
| D6 | 54 | 0 | 有實際前提控制 |
| D7 | 0 | 54 | 仍缺控制；沒有兩-root (4,4) minimal core；仍缺控制 |
| D7a | 0 | 54 | 仍缺控制；沒有兩-root44 core；原triangle／directbridge身份仍缺控制 |
| D8 | 0 | 54 | 仍缺控制；沒有 sole mixed22＋(4,4) core；仍缺控制 |
| D9 | 0 | 54 | 仍缺控制；沒有 sole mixed22＋(4,4) core；仍缺控制 |
| D9a | 0 | 54 | 仍缺控制；沒有sole mixed22＋44 core；side exact兩型仍缺控制 |
| D10 | 54 | 0 | 有實際前提控制 |
| D11 | 54 | 0 | 有實際前提控制 |
| D12 | 54 | 0 | 有實際前提控制 |
| D12a | 54 | 0 | 有實際前提控制 |
| D13 | 54 | 0 | 有實際前提控制 |
| D14 | 0 | 54 | 仍缺控制；所有minimal qcores均保留兩roots；仍缺控制 |
| D15 | 0 | 54 | 仍缺控制；沒有sole mixed22＋(4,4) core；單列terminal步驟仍缺控制 |
| D16 | 0 | 54 | 仍缺控制；沒有sole mixed22＋(4,4) core；整側盾弧步驟仍缺控制 |
| D16a | 0 | 54 | 仍缺控制；原H無把兩roots分開的bridge；generic整側盾弧仍缺控制 |
| E1 | 18 | 36 | 有實際前提控制；沒有任何重色 spoke |
| E2 | 54 | 0 | 有實際前提控制 |
| E2a | 54 | 0 | 有實際前提控制 |
| E3 | 54 | 0 | 有實際前提控制 |
| E4 | 19 | 35 | 有實際前提控制；m≠2 |
| E5 | 0 | 54 | 仍缺控制；所有m=2拒絕列都無重色spokes；exact spoke core仍缺控制 |
| T1 | 0 | 54 | 三列版本不適用；指定 q₀、q₁、q₃ 並非全拒絕；024／124 的三列排除不適用 |
| T2 | 0 | 54 | 三列版本不適用；N1-22-44 整類排除／真框邊／整側盾弧≥3 需要指定三列；所有控制不滿足 |

## 5. 引理 × 控制圖完整表

每格只有「成立」或「不適用」。為縮短表格，`N<ID>` 是「不適用：§4 該 ID 的缺失前提」，且其逐圖原文完整保存於 [summary.json](summary.json)；
同一 ID 的 N 格均有相同缺失前提文字。`✓`＝成立，已計算該項全部所列結論。先驗與反證禁型分開：例如 B7 成立不會代替 B1／B5／B6 的 N 格。

### A1–A7

| 控制圖 | A1 | A2 | A3 | A4 | A5 | A6 | A7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA6-0002](controls/NA6-0002.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA6-0003](controls/NA6-0003.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA7-0001](controls/NA7-0001.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA7-0002](controls/NA7-0002.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0001](controls/NA8-0001.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0002](controls/NA8-0002.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0003](controls/NA8-0003.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0004](controls/NA8-0004.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0005](controls/NA8-0005.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0006](controls/NA8-0006.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0007](controls/NA8-0007.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0008](controls/NA8-0008.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0009](controls/NA8-0009.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0010](controls/NA8-0010.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0011](controls/NA8-0011.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0012](controls/NA8-0012.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0013](controls/NA8-0013.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0014](controls/NA8-0014.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0015](controls/NA8-0015.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0016](controls/NA8-0016.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0017](controls/NA8-0017.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0018](controls/NA8-0018.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0019](controls/NA8-0019.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0020](controls/NA8-0020.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0021](controls/NA8-0021.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA8-0022](controls/NA8-0022.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0001](controls/NA9-0001.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0002](controls/NA9-0002.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0003](controls/NA9-0003.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0004](controls/NA9-0004.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0005](controls/NA9-0005.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0006](controls/NA9-0006.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0007](controls/NA9-0007.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0008](controls/NA9-0008.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0009](controls/NA9-0009.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0010](controls/NA9-0010.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0011](controls/NA9-0011.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0012](controls/NA9-0012.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0013](controls/NA9-0013.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0014](controls/NA9-0014.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0015](controls/NA9-0015.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0016](controls/NA9-0016.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0017](controls/NA9-0017.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0018](controls/NA9-0018.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0019](controls/NA9-0019.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0020](controls/NA9-0020.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0021](controls/NA9-0021.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0022](controls/NA9-0022.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0023](controls/NA9-0023.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0024](controls/NA9-0024.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0025](controls/NA9-0025.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0026](controls/NA9-0026.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| [NA9-0027](controls/NA9-0027.json) | ✓ | NA2 | ✓ | ✓ | ✓ | ✓ | ✓ |

### B1–B7

| 控制圖 | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA6-0002](controls/NA6-0002.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA6-0003](controls/NA6-0003.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA7-0001](controls/NA7-0001.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA7-0002](controls/NA7-0002.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0001](controls/NA8-0001.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0002](controls/NA8-0002.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0003](controls/NA8-0003.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0004](controls/NA8-0004.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0005](controls/NA8-0005.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0006](controls/NA8-0006.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0007](controls/NA8-0007.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0008](controls/NA8-0008.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0009](controls/NA8-0009.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0010](controls/NA8-0010.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0011](controls/NA8-0011.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0012](controls/NA8-0012.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0013](controls/NA8-0013.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0014](controls/NA8-0014.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0015](controls/NA8-0015.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0016](controls/NA8-0016.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0017](controls/NA8-0017.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0018](controls/NA8-0018.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0019](controls/NA8-0019.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA8-0020](controls/NA8-0020.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0021](controls/NA8-0021.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA8-0022](controls/NA8-0022.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0001](controls/NA9-0001.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0002](controls/NA9-0002.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0003](controls/NA9-0003.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0004](controls/NA9-0004.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0005](controls/NA9-0005.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0006](controls/NA9-0006.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0007](controls/NA9-0007.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0008](controls/NA9-0008.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0009](controls/NA9-0009.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0010](controls/NA9-0010.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0011](controls/NA9-0011.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0012](controls/NA9-0012.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0013](controls/NA9-0013.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0014](controls/NA9-0014.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0015](controls/NA9-0015.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0016](controls/NA9-0016.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0017](controls/NA9-0017.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0018](controls/NA9-0018.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0019](controls/NA9-0019.json) | NB1 | NB2 | NB3 | ✓ | NB5 | NB6 | ✓ |
| [NA9-0020](controls/NA9-0020.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0021](controls/NA9-0021.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0022](controls/NA9-0022.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0023](controls/NA9-0023.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0024](controls/NA9-0024.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0025](controls/NA9-0025.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0026](controls/NA9-0026.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |
| [NA9-0027](controls/NA9-0027.json) | NB1 | NB2 | NB3 | NB4 | NB5 | NB6 | ✓ |

### B8–C3a

| 控制圖 | B8 | C1 | C2 | C2a | C2b | C3 | C3a |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | NB8 | NC1 | NC2 | NC2a | NC2b | ✓ | NC3a |
| [NA6-0002](controls/NA6-0002.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA6-0003](controls/NA6-0003.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA7-0001](controls/NA7-0001.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA7-0002](controls/NA7-0002.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0001](controls/NA8-0001.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0002](controls/NA8-0002.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0003](controls/NA8-0003.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0004](controls/NA8-0004.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0005](controls/NA8-0005.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0006](controls/NA8-0006.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0007](controls/NA8-0007.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0008](controls/NA8-0008.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0009](controls/NA8-0009.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0010](controls/NA8-0010.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0011](controls/NA8-0011.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0012](controls/NA8-0012.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0013](controls/NA8-0013.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0014](controls/NA8-0014.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0015](controls/NA8-0015.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0016](controls/NA8-0016.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0017](controls/NA8-0017.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0018](controls/NA8-0018.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0019](controls/NA8-0019.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA8-0020](controls/NA8-0020.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0021](controls/NA8-0021.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA8-0022](controls/NA8-0022.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA9-0001](controls/NA9-0001.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0002](controls/NA9-0002.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0003](controls/NA9-0003.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0004](controls/NA9-0004.json) | NB8 | ✓ | ✓ | NC2a | NC2b | ✓ | ✓ |
| [NA9-0005](controls/NA9-0005.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0006](controls/NA9-0006.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0007](controls/NA9-0007.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0008](controls/NA9-0008.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0009](controls/NA9-0009.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0010](controls/NA9-0010.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA9-0011](controls/NA9-0011.json) | ✓ | ✓ | ✓ | ✓ | NC2b | ✓ | ✓ |
| [NA9-0012](controls/NA9-0012.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0013](controls/NA9-0013.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0014](controls/NA9-0014.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0015](controls/NA9-0015.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0016](controls/NA9-0016.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0017](controls/NA9-0017.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0018](controls/NA9-0018.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0019](controls/NA9-0019.json) | NB8 | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0020](controls/NA9-0020.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0021](controls/NA9-0021.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0022](controls/NA9-0022.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0023](controls/NA9-0023.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0024](controls/NA9-0024.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0025](controls/NA9-0025.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0026](controls/NA9-0026.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |
| [NA9-0027](controls/NA9-0027.json) | ✓ | ✓ | NC2 | NC2a | NC2b | ✓ | ✓ |

### C4–C10

| 控制圖 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | NC4 | ✓ | ✓ | NC7 | NC8 | NC9 | NC10 |
| [NA6-0002](controls/NA6-0002.json) | ✓ | ✓ | ✓ | NC7 | NC8 | NC9 | NC10 |
| [NA6-0003](controls/NA6-0003.json) | ✓ | ✓ | ✓ | NC7 | NC8 | NC9 | NC10 |
| [NA7-0001](controls/NA7-0001.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA7-0002](controls/NA7-0002.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0001](controls/NA8-0001.json) | ✓ | ✓ | ✓ | NC7 | NC8 | NC9 | NC10 |
| [NA8-0002](controls/NA8-0002.json) | ✓ | ✓ | ✓ | NC7 | NC8 | NC9 | NC10 |
| [NA8-0003](controls/NA8-0003.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0004](controls/NA8-0004.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0005](controls/NA8-0005.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0006](controls/NA8-0006.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0007](controls/NA8-0007.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0008](controls/NA8-0008.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0009](controls/NA8-0009.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0010](controls/NA8-0010.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0011](controls/NA8-0011.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0012](controls/NA8-0012.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0013](controls/NA8-0013.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0014](controls/NA8-0014.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0015](controls/NA8-0015.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0016](controls/NA8-0016.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0017](controls/NA8-0017.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0018](controls/NA8-0018.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0019](controls/NA8-0019.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA8-0020](controls/NA8-0020.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0021](controls/NA8-0021.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA8-0022](controls/NA8-0022.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA9-0001](controls/NA9-0001.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0002](controls/NA9-0002.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0003](controls/NA9-0003.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0004](controls/NA9-0004.json) | ✓ | ✓ | ✓ | ✓ | NC8 | NC9 | NC10 |
| [NA9-0005](controls/NA9-0005.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0006](controls/NA9-0006.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0007](controls/NA9-0007.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0008](controls/NA9-0008.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0009](controls/NA9-0009.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0010](controls/NA9-0010.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA9-0011](controls/NA9-0011.json) | ✓ | ✓ | ✓ | NC7 | NC8 | ✓ | ✓ |
| [NA9-0012](controls/NA9-0012.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0013](controls/NA9-0013.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0014](controls/NA9-0014.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0015](controls/NA9-0015.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0016](controls/NA9-0016.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0017](controls/NA9-0017.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0018](controls/NA9-0018.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0019](controls/NA9-0019.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0020](controls/NA9-0020.json) | NC4 | ✓ | NC6 | NC7 | ✓ | NC9 | NC10 |
| [NA9-0021](controls/NA9-0021.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0022](controls/NA9-0022.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0023](controls/NA9-0023.json) | NC4 | ✓ | NC6 | NC7 | ✓ | NC9 | NC10 |
| [NA9-0024](controls/NA9-0024.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0025](controls/NA9-0025.json) | NC4 | ✓ | NC6 | NC7 | NC8 | NC9 | NC10 |
| [NA9-0026](controls/NA9-0026.json) | NC4 | ✓ | NC6 | NC7 | ✓ | NC9 | NC10 |
| [NA9-0027](controls/NA9-0027.json) | NC4 | ✓ | NC6 | NC7 | ✓ | NC9 | NC10 |

### C11–D2

| 控制圖 | C11 | C12 | C13 | C14 | D1 | D1a | D2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA6-0002](controls/NA6-0002.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA6-0003](controls/NA6-0003.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA7-0001](controls/NA7-0001.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA7-0002](controls/NA7-0002.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0001](controls/NA8-0001.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0002](controls/NA8-0002.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0003](controls/NA8-0003.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0004](controls/NA8-0004.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0005](controls/NA8-0005.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0006](controls/NA8-0006.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0007](controls/NA8-0007.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0008](controls/NA8-0008.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0009](controls/NA8-0009.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0010](controls/NA8-0010.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0011](controls/NA8-0011.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0012](controls/NA8-0012.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0013](controls/NA8-0013.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0014](controls/NA8-0014.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0015](controls/NA8-0015.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0016](controls/NA8-0016.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0017](controls/NA8-0017.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0018](controls/NA8-0018.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0019](controls/NA8-0019.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0020](controls/NA8-0020.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0021](controls/NA8-0021.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA8-0022](controls/NA8-0022.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0001](controls/NA9-0001.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0002](controls/NA9-0002.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0003](controls/NA9-0003.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0004](controls/NA9-0004.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0005](controls/NA9-0005.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0006](controls/NA9-0006.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0007](controls/NA9-0007.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0008](controls/NA9-0008.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0009](controls/NA9-0009.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0010](controls/NA9-0010.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0011](controls/NA9-0011.json) | NC11 | ✓ | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0012](controls/NA9-0012.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0013](controls/NA9-0013.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0014](controls/NA9-0014.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0015](controls/NA9-0015.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0016](controls/NA9-0016.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0017](controls/NA9-0017.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0018](controls/NA9-0018.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0019](controls/NA9-0019.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0020](controls/NA9-0020.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0021](controls/NA9-0021.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0022](controls/NA9-0022.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0023](controls/NA9-0023.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0024](controls/NA9-0024.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0025](controls/NA9-0025.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0026](controls/NA9-0026.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |
| [NA9-0027](controls/NA9-0027.json) | NC11 | NC12 | ✓ | ✓ | ✓ | ✓ | ND2 |

### D3–D7a

| 控制圖 | D3 | D4 | D4a | D5 | D6 | D7 | D7a |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA6-0002](controls/NA6-0002.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA6-0003](controls/NA6-0003.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA7-0001](controls/NA7-0001.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA7-0002](controls/NA7-0002.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0001](controls/NA8-0001.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0002](controls/NA8-0002.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0003](controls/NA8-0003.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0004](controls/NA8-0004.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0005](controls/NA8-0005.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0006](controls/NA8-0006.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0007](controls/NA8-0007.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0008](controls/NA8-0008.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0009](controls/NA8-0009.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0010](controls/NA8-0010.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0011](controls/NA8-0011.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0012](controls/NA8-0012.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0013](controls/NA8-0013.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0014](controls/NA8-0014.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0015](controls/NA8-0015.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0016](controls/NA8-0016.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0017](controls/NA8-0017.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0018](controls/NA8-0018.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0019](controls/NA8-0019.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0020](controls/NA8-0020.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0021](controls/NA8-0021.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA8-0022](controls/NA8-0022.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0001](controls/NA9-0001.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0002](controls/NA9-0002.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0003](controls/NA9-0003.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0004](controls/NA9-0004.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0005](controls/NA9-0005.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0006](controls/NA9-0006.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0007](controls/NA9-0007.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0008](controls/NA9-0008.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0009](controls/NA9-0009.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0010](controls/NA9-0010.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0011](controls/NA9-0011.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0012](controls/NA9-0012.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0013](controls/NA9-0013.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0014](controls/NA9-0014.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0015](controls/NA9-0015.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0016](controls/NA9-0016.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0017](controls/NA9-0017.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0018](controls/NA9-0018.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0019](controls/NA9-0019.json) | ✓ | ND4 | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0020](controls/NA9-0020.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0021](controls/NA9-0021.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0022](controls/NA9-0022.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0023](controls/NA9-0023.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0024](controls/NA9-0024.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0025](controls/NA9-0025.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0026](controls/NA9-0026.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |
| [NA9-0027](controls/NA9-0027.json) | ✓ | ✓ | ✓ | ✓ | ✓ | ND7 | ND7a |

### D8–D12a

| 控制圖 | D8 | D9 | D9a | D10 | D11 | D12 | D12a |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA6-0002](controls/NA6-0002.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA6-0003](controls/NA6-0003.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA7-0001](controls/NA7-0001.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA7-0002](controls/NA7-0002.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0001](controls/NA8-0001.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0002](controls/NA8-0002.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0003](controls/NA8-0003.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0004](controls/NA8-0004.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0005](controls/NA8-0005.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0006](controls/NA8-0006.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0007](controls/NA8-0007.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0008](controls/NA8-0008.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0009](controls/NA8-0009.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0010](controls/NA8-0010.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0011](controls/NA8-0011.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0012](controls/NA8-0012.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0013](controls/NA8-0013.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0014](controls/NA8-0014.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0015](controls/NA8-0015.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0016](controls/NA8-0016.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0017](controls/NA8-0017.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0018](controls/NA8-0018.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0019](controls/NA8-0019.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0020](controls/NA8-0020.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0021](controls/NA8-0021.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA8-0022](controls/NA8-0022.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0001](controls/NA9-0001.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0002](controls/NA9-0002.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0003](controls/NA9-0003.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0004](controls/NA9-0004.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0005](controls/NA9-0005.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0006](controls/NA9-0006.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0007](controls/NA9-0007.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0008](controls/NA9-0008.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0009](controls/NA9-0009.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0010](controls/NA9-0010.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0011](controls/NA9-0011.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0012](controls/NA9-0012.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0013](controls/NA9-0013.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0014](controls/NA9-0014.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0015](controls/NA9-0015.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0016](controls/NA9-0016.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0017](controls/NA9-0017.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0018](controls/NA9-0018.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0019](controls/NA9-0019.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0020](controls/NA9-0020.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0021](controls/NA9-0021.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0022](controls/NA9-0022.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0023](controls/NA9-0023.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0024](controls/NA9-0024.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0025](controls/NA9-0025.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0026](controls/NA9-0026.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |
| [NA9-0027](controls/NA9-0027.json) | ND8 | ND9 | ND9a | ✓ | ✓ | ✓ | ✓ |

### D13–E2

| 控制圖 | D13 | D14 | D15 | D16 | D16a | E1 | E2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA6-0002](controls/NA6-0002.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA6-0003](controls/NA6-0003.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA7-0001](controls/NA7-0001.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA7-0002](controls/NA7-0002.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0001](controls/NA8-0001.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0002](controls/NA8-0002.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0003](controls/NA8-0003.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0004](controls/NA8-0004.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0005](controls/NA8-0005.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0006](controls/NA8-0006.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0007](controls/NA8-0007.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0008](controls/NA8-0008.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0009](controls/NA8-0009.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0010](controls/NA8-0010.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0011](controls/NA8-0011.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0012](controls/NA8-0012.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0013](controls/NA8-0013.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0014](controls/NA8-0014.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0015](controls/NA8-0015.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0016](controls/NA8-0016.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0017](controls/NA8-0017.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0018](controls/NA8-0018.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0019](controls/NA8-0019.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA8-0020](controls/NA8-0020.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0021](controls/NA8-0021.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA8-0022](controls/NA8-0022.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0001](controls/NA9-0001.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0002](controls/NA9-0002.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0003](controls/NA9-0003.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0004](controls/NA9-0004.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA9-0005](controls/NA9-0005.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0006](controls/NA9-0006.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0007](controls/NA9-0007.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0008](controls/NA9-0008.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0009](controls/NA9-0009.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0010](controls/NA9-0010.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA9-0011](controls/NA9-0011.json) | ✓ | ND14 | ND15 | ND16 | ND16a | ✓ | ✓ |
| [NA9-0012](controls/NA9-0012.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0013](controls/NA9-0013.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0014](controls/NA9-0014.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0015](controls/NA9-0015.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0016](controls/NA9-0016.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0017](controls/NA9-0017.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0018](controls/NA9-0018.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0019](controls/NA9-0019.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0020](controls/NA9-0020.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0021](controls/NA9-0021.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0022](controls/NA9-0022.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0023](controls/NA9-0023.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0024](controls/NA9-0024.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0025](controls/NA9-0025.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0026](controls/NA9-0026.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |
| [NA9-0027](controls/NA9-0027.json) | ✓ | ND14 | ND15 | ND16 | ND16a | NE1 | ✓ |

### E2a–T2

| 控制圖 | E2a | E3 | E4 | E5 | T1 | T2 |
| --- | --- | --- | --- | --- | --- | --- |
| [NA6-0001](controls/NA6-0001.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA6-0002](controls/NA6-0002.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA6-0003](controls/NA6-0003.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA7-0001](controls/NA7-0001.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA7-0002](controls/NA7-0002.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0001](controls/NA8-0001.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0002](controls/NA8-0002.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0003](controls/NA8-0003.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0004](controls/NA8-0004.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0005](controls/NA8-0005.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0006](controls/NA8-0006.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0007](controls/NA8-0007.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0008](controls/NA8-0008.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0009](controls/NA8-0009.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0010](controls/NA8-0010.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0011](controls/NA8-0011.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0012](controls/NA8-0012.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0013](controls/NA8-0013.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0014](controls/NA8-0014.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0015](controls/NA8-0015.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0016](controls/NA8-0016.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0017](controls/NA8-0017.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0018](controls/NA8-0018.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0019](controls/NA8-0019.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA8-0020](controls/NA8-0020.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0021](controls/NA8-0021.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA8-0022](controls/NA8-0022.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0001](controls/NA9-0001.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0002](controls/NA9-0002.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0003](controls/NA9-0003.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0004](controls/NA9-0004.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0005](controls/NA9-0005.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0006](controls/NA9-0006.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0007](controls/NA9-0007.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0008](controls/NA9-0008.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0009](controls/NA9-0009.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0010](controls/NA9-0010.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0011](controls/NA9-0011.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0012](controls/NA9-0012.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0013](controls/NA9-0013.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0014](controls/NA9-0014.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0015](controls/NA9-0015.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0016](controls/NA9-0016.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0017](controls/NA9-0017.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0018](controls/NA9-0018.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0019](controls/NA9-0019.json) | ✓ | ✓ | NE4 | NE5 | NT1 | NT2 |
| [NA9-0020](controls/NA9-0020.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0021](controls/NA9-0021.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0022](controls/NA9-0022.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0023](controls/NA9-0023.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0024](controls/NA9-0024.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0025](controls/NA9-0025.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0026](controls/NA9-0026.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |
| [NA9-0027](controls/NA9-0027.json) | ✓ | ✓ | ✓ | NE5 | NT1 | NT2 |

## 6. 仍缺控制、反例與對 E4 的影響

**沒有反例，沒有觸發停止条件，沒有修改 E4。** 本次不是把 E4 整份任意大小紙面證明轉成有限 theorem；沒出現的前提仍不得聲稱已被控制校準。

仍缺實際前提觸發共 18 項：

- B1／B2／B3：空支援 mixed、外路 hub 與無框 separating appendage。
- B5／B6：原 H tree Euler 反證配置、m≥3 的 theta 配置。B7 的必要條件已在 54 圖核對。
- C2b／C11：singleton one-sided 盾弧、兩短 mixed 且無 unary。
- D2／D14：root-deletion 真單缺列例外及其 exact root-omitting core。
- D7／D7a／D8／D9／D9a／D15／D16：(4,4) core、root triangles／direct bridge、sole mixed22 的 path／side／單列 terminal／整側中間步驟。
- D16a：原 H bridge 把兩 roots 分到两 connected 整側；這批原 H 沒有此 bridge，generic拓撲版本也無真觸發。
- E5：實際拒絕列只有一root重色時的 exact spoke-omitting core。E4 的至多一重色必要條件19圖已驗，但其更強單重色分支沒被觸發。

T1／T2 的完整三列前提全54不成立，故不放入18项不用三列的缺口中；三列 private-spoke024／124、terminal真框邊、每整側≥3及N1-22-44整型排除的範圍原樣保留。
如果 checker 發現前提成立而結論不成立，會停止在按 k／orbit排序的首份控制，另 exclusive-save `counterexample.json`，保留原完整邊、失敗實例及其 witnesses；不改 E4。
本輪並未發生這種情况，因此沒有製造虛構的最小反例。下一入口是補上述前提控制或獨立證明審查；本輪到指定 54 圖表完成即停止。

## 7. 重播、exit codes 與檔案範圍

[checker](../../scripts/c5_excess_two_e4c_controls.py) 以 `open(..., "x")` exclusive-create 新建；生成產物只用 `xb`，`--check` 只讀重新計算並逐 byte 比對 54 個控制 JSON＋summary.json，共55檔。
原 E4／ES 文件、報告、checker／certificates、README／HANDOFF／STATUS、MANIFEST／.gitignore 均未更動。未缺少任何本任務所讀來源；沒有重建、複製或改記歷史大產物。
各新檔均小於1,000,000 bytes（最大控制 JSON 128,023 bytes），所以沒有需 `tools/artifacts.py record` 的本任務大檔。checks 日誌／validation 不屬於 deterministic 数學certificate。

| 實際執行命令 | exit code | 結果 |
| --- | ---: | --- |
| `/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4c_controls.py` | 0 | 54/54 controls；60 row cores；55 byte files；沒有反例 |
| 同 checker `--check` | 0 | 全55檔逐byte一致 |
| `PYTHONHASHSEED=17` 同 checker `--check` | 0 | 全55檔逐byte一致 |
| `/home/ray/developer/ai/math/.venv/bin/python scripts/check_docs.py` | **1** | 僅兩個基準既有 missing paths，照實保留 |
| `/home/ray/developer/ai/math/.venv/bin/python tools/docgraph check` | 0 | 62 documents／213 relations／5 families；0 errors／notes |
| `git diff --check` | 0 | tracked diff空；另實查新文本whitespace |

上表文件檢查已在報告建立前實際執行；完成報告後會再執行文件／DocGraph／diff檢查，結果及全部新檔SHA另存 `validation.json`，不將預期當成已執行。
已知 missing paths：

```text
../audits/2026-10-04-task-d5/c4/scope_ledger.json
../../audits/2026-10-04-task-d2/integration_doc_changes.diff
```

```sh
/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4c_controls.py
/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4c_controls.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4c_controls.py --check
/home/ray/developer/ai/math/.venv/bin/python scripts/check_docs.py
/home/ray/developer/ai/math/.venv/bin/python tools/docgraph check
git diff --check
```

首次命令在尚無產物時生成；已有產物時會 exclusive-create 失敗，重播應用 `--check`。
checker 草稿僅在 `/tmp` 試算；其中一次因 in-memory tuple/list 比較把同一55 core誤判為不同，draft exit2。修正container比較後全54通过，未寫任何正式certificate，並未出現數學反例。
最終checker始終只 exclusive-create 一次；生成、普通／seed17重播均 exit0。
