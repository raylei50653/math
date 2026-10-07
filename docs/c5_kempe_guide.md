# Kempe／重接／計數與策略導覽

更新：2026-10-07（唯一 mixed 指定稽核與 U1 no-mixed44 排除）。本頁維護本線現況；證明及實際重播範圍見各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

本批成果及D至D₅稽核的發布驗證見[發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)；
新checkout的凍結快照／完整輸出先依[封存還原說明](../audits/README.md)還原。

## 1. 目標與範圍

研究固定來源圖上的換色、完整有序關係及計數限制，尋找可證的出口機制。
必要條件、固定圖閉包與一般 disk 定理分開；本線不宣稱已證 `K∞=K≤5`。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 933／941 的 excess／容量／跨度 | 兩候選均已證 ε≥2。唯一 degree-6 root 的 t=0、1、2、3 全部分拆均已作整型來源排除，T4 迫 t≤3，完成此 ε=2 分支。t=0 的 (6) 用飽和兩 K₄，(4,2) 用原 binary 路徑的同源框弧 K₅；若 ε=2，只剩兩個 degree-5 roots。任意大小紙面＋Python、未 Lean 化，一般來源保留 | [t=0 全分拆總報告](c5_excess_two_no_spoke_complete.md)、[t=3 全分拆總報告](c5_excess_two_three_spoke_complete.md)、[t=2 全分拆總報告](c5_excess_two_two_spoke_complete.md)、[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)、[941 ε≥2](c5_941_three_spoke.md) |
| 不依賴 ε 的盾弧預算與 hub 原則 | 任意 ε、任意 roots：one-sided 分量的支援是連續框弧、盾弧兩兩邊互斥；全圖至多兩份 unary，且 spokes／mixed 支援被限制在 2–3 個框點。短支援、K₄ 引理、二／三-hub K₅ 統一成 hub 原則，並推廣到 roots 同色的 mixed 分量。A₄ 殘留 U 支援紀錄 40／58→24／30，無整份 frame 排除。紙面＋Python，未 Lean 化 | [盾弧預算與 hub 原則](c5_unary_shield_budget.md) |
| 雙 root 的 ε=2 收窄 | 相鄰 mixed 刪 roots／zw 全收；相鄰唯一 mixed 已全排 (4,4) 核心、五-spoke 原來源、四-spoke (3,1) 全部 incidence 分拆及 (2,2) 的 mixed-(1,1) 加各側一 unary 整個子型，含 root 交換。原47／75必要身份全部封閉；其他 (2,2) incidence、較少 spokes、單省略及原 (5,5) 核心保留。紙面＋Python，ε≥3 未證，未 Lean 化 | [mixed-(1,1) 子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)、[短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)、[原 crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md)、[同一長 face 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md)、[原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)、[原三接點身份](c5_excess_two_mixed_core_four_spoke_ternary.md)、[binary 端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md) |
| Kempe screen／邊位置對座標 | screen 等價於 20 條蘊涵，1,024 masks 已核對；未新增排除，一般 adjacent-singleton lemma 未證 | [screen](c5_kempe_screen.md)、[座標](c5_edge_pair_coordinates.md) |
| 循環流與計數 | 六維／153 支撐／十二循環；36 份基底覆蓋證三套分開整數 orbit 條件不再收緊恆等式解；未排除平面來源 | [循環流](c5_circulation.md) |
| Count cone／class 計數 | near-triangulation 化約、部分 Lean 代數與 class 級紙面計數已有；cone／connectivity 缺口仍在 | [count cone](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[class 計數](c5_kempe_class_counts.md) |
| 同染色有序重接 | 一步精確公式及同圖三配對同 state／不同後繼反例；record 110 已另由原圖 K5 排除，有限可迭代 state 未證 | [有序重接](c5_dual_path_surgery.md)、[來源排除](c5_single_spoke_two_two_minor.md) |
| Connectivity／候選 state | 同圖更新與有限控制可重播；AB-only／固定 AB\|CD 猜測有反例，多候選不能任意拼成可實現 state | [connectivity](c5_kempe_connectivity.md)、[AB cube](c5_ab_swap_cube.md)、[choices](c5_edge_choices.md) |
| Cut／behavior | retained-component 重建有 Lean 支援；粗 cut 摘要有反例，有界 behavior 控制不證多步充分性 | [cut](c5_cut_interfaces.md)、[behavior](c5_behavior_refinement_results.md)、[state 導覽](c5_state_guide.md) |
| 固定圖策略與 repair | survivor-811 固定閉包、必要低谷／回升與 B₂ 準備已保存；一般 K=4 策略、共同安全 repair 機制未證 | [barriers](c5_strategy_barriers.md)、[repair](c5_repair_interface.md) |

## 3. 停止點與保留缺口

**目前停止點（2026-10-07）：U1 的 no-mixed 兩-root44 身份全排；完整 Σ 的44殘留只剩U2–U4，ε≥3 未證。**
本輪補成相鄰唯一 mixed 四份指定化約／固定域的獨立稽核，並新增U1來源身份排除；
各報告保留當輪停止點與歷史計畫，其他core型照舊。
原 A／B 的逐 pair 必要表仍供追溯，後續三列結論以 E3–E6 的完整前提為準。

| 已返回任務 | 已完成範圍與證據界線 |
| --- | --- |
| K′ | 在同一G−p的拒絕見證ψ（q∉Σ(G)）下，[引理1–6及Jordan側別](c5_kempe_diagonal_transport.md)迫單點四色鄰域的兩條對角鏈皆斷開；933／941仍有192／384筆一致指派，可實現1012／935控制各192。同 ψ 多鏈交換無新排除，局部資料不能分辨來源；K′未決，K型局部題停止 |
| E3／D₈ | [三列約化與triple-critical](../artifacts/c5_excess_two_e3/REPORT.md)；唯一degree-6全分支排除須引用[D₈](../audits/2026-10-04-task-d8/REPORT.md)的DG6-1補表：t=1的(4,1)／(3,2)相對spoke位置100份幾何零存活。E3對A前序的依賴過強更正已保存 |
| E4 | [非相鄰m≤2與N3全排](../artifacts/c5_excess_two_e4/REPORT.md)；N1排mixed22有(4,4)core，N2排兩短無unary，其餘N1／N2保留。當輪缺少的非相鄰正控制後由ES／E4C提供；N∅／L-spoke已由NA6-1–3否定 |
| E5／E6 | [四分支依賴表](../artifacts/c5_excess_two_e5/REPORT.md)與[相鄰m≤2](../artifacts/c5_excess_two_e6/REPORT.md)關閉J6的m≥3。G2的U盾弧恰二；G3剩具名支援約束；G4只剩盾弧恰三；no-mixed為941的013三-spoke或兩側≤2。G1依actual core轉交，G1–G4、J6的m≤2及J4其餘殘留未全排；紙面＋Python，未Lean化 |
| E4C | [54個NA critical orbits ×60項](../artifacts/c5_excess_two_e4c/REPORT.md)不用三列的控制：42項有觸發前提的圖、18項無控制、0反例。真正控制缺口為singleton盾弧、root刪除例外、(4,4)core、根間bridge整側、單root重色core；不把未觸發前提當作引理已驗證 |
| ES／ER | [ES](c5_excess_two_finite_search.md)與[獨立ER](c5_excess_two_independent_search.md)三型k≤9的q／critical orbit集合、計數及Q分布逐層一致，179個critical orbits（NA54／AD9／D6 116），無\|Q\|+c(Q)>4。完整性為有限雙實作證據，ER另依賴plantri；k≥10未搜尋 |
| LC | [179／179個Lean soundness證書](c5_excess_two_lean_certificates.md)，558項axioms audit無sorryAx。拒絕列用native_decide，組合嵌入不等於拓撲disk定理，也不證搜尋完整性。未接入Math.lean／預設CI；是否接入的提議保留 |
| D₉ | [E4／E5／E6紙面引理獨立稽核](../audits/2026-10-06-task-d9/REPORT.md)：N-empty-separating、N-theta、N1-22-44、L1–L8、相鄰m≤2、G2–G4及no-mixed預算全部成立，無新缺口；54 NA＋9 AD控制零反例。指定三列來源前提0／63觸發，三列下的來源排除無有限控制。歷史provenance FAIL與E3 degree6.json未入封存照實保存 |
| C44 | [三型k≤9全部minimal cores](../artifacts/c5_excess_two_c44/REPORT.md)：9,644 q-orbits／179 critical，k≤6逐邊集與暴力一致。具名[C44-AD3-row0-44](../artifacts/c5_excess_two_c44/counterexample_C44-AD3-row0-44.json)（Σ956、Σ-critical；相鄰兩root各三spoke見框色0,1,2，皆迫色3）反駁一般「無兩-root (4,4) core」。加完整Σ=933／941前提的窄命題未證；有限域無此前提的來源，有限統計對它無控制，停止推廣 |
| C44′ | [Σ相容篩](../artifacts/c5_excess_two_c44p/REPORT.md)：C44保存的2,416份兩-root (4,4) occurrences（213份literal core）全部相容；兩private頂點型125 placements中30份可嵌disk、10份相容（一個orbit，具名C44P-AD2-012-034，Σ959）。**篩本身近乎無效：** 933的D₅像恰為T4加任一個非T4列（五列皆可），941為T4加兩列；同框子圖繼承T4，故只拒一個非T4列的core必相容。Σ層必要條件不能排(4,4) core，排除須用來源的多列聯合、criticality或spoke預算；停止此方向 |
| C44″ | [雙-root (4,4) 覆蓋表](../artifacts/c5_excess_two_c44pp/REPORT.md)：完整Σ=933／941下，相鄰m=1已有舊系列全排且不需K′；兩份AD-012-034具名core不能來自此前提的兩-root44來源。當輪整理覆蓋與必要限制；後續指定稽核及U1排除見下兩項 |
| 唯一 mixed 指定稽核 | [四份舊排除稽核](../audits/2026-10-07-c44pp-mixed-audit/REPORT.md)：任意大小化約與固定域核對通過，獨立重算root pairs／S₄支援／368,859份UNSAT proofs／6,008份subdivisions；344域的標記run覆蓋亦通過。沿用上游分類，未重稽核其全部枚舉，未補E5的新證明 |
| U1 no-mixed44 | [U1排除](c5_excess_two_no_mixed_core44.md)：spoke＋unit-U由單點D-forcer與triangle palette衝突；雙spoke以全部344份bridge-marker核心的3,498次接回全排，涵蓋941三-spoke側並更正原收窄。兩-root44身份全排；其他no-mixed core型及root刪除例外保留，紙面＋Python，未Lean化 |

**完整 Σ=933／941 的兩-root (4,4) 殘留。** 沿用 disk、Σ-critical、ε=2、
完整 degrees、同源 contacts／attachments 與整圖 D₅ 搬運；逐格前提與出處見 C44″。

| 未覆蓋家族 | 精確省略身份與必要限制 |
| --- | --- |
| U2：相鄰 m=2 | 恰省略一份 mixed11，保留另一份 mixed11 並共用 x；不得再省略其他因子 |
| U3：非相鄰 N1 | sole C incidence11／12／21，兩側各省略一個 unit；三-spoke set 不可為 024／124 |
| U4：非相鄰 N2 | 恰省略一份 mixed11；(ℓ,u)=(2,0),(1,0),(1,1),(0,1),(0,2)。該44 core所拒絕列的兩側原 spokes 均不得重色 |

U1 已由 [no-mixed44](c5_excess_two_no_mixed_core44.md) 排除。上方三項只列兩-root44 core；單-root 的 N1 刪 root 例外另保留，
(5,4)/(4,5) 及原 G 的 (5,5) core 也未因此排除。
E3 的三列推廣不能直接復用部分精確 Σ 證書；E5／E6 在精確 941／933／940
也依其「新證明」要求保留 G1。C44″ 與本輪指定稽核不完成那項任務；
上游degree-4／triangle分類的全部枚舉沒有重新稽核。
**下一個窄提議（未啟動）：** U2相鄰m=2的mixed11省略身份。
固定保留的原共鄰triangle，檢查被省略mixed11的完整二接點relation、同一實際支援
與兩條mixed路圍成外界的限制；不把singleton收縮當染色替換，不預填省略圖Ω。
本輪驗證見[紀錄](history/2026-10-07-no-mixed-core44.md)；前輪整合見
[整合覆核紀錄](history/2026-10-07-c44pp-integration-review.md)。

不新開逐spoke-pair輪次、擴大k搜尋、案例樹ledger、K型局部題或Lean
枚舉completeness試點。雙degree-5的N1／N2、G1–G4、J6剩餘、no-mixed、
較少spokes、原(5,5)core及一般來源未全排；猜想E任意大小、一般出口與K∞=K≤5未證。
另一個保留題目是把Σ|σ|≤5與逐列D+O恆等式合成單一不等式。
本次重播、歷史文件hash漂移與分支發布見
[發布紀錄](history/2026-10-04-kprime-excess-two-progress-publish.md)。

以下保存固定完整Σ933／941的A／B原身份與停止點；其逐pair下一步不覆蓋上方窄提議。

本線候選來源前提是固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊
Σ-critical、指定有序 induced-C₅ disk、所有有效內點完整 degree≥4。
原分量、有序 contacts、實際 attachments／supports、ownership、嵌入
環序及同一字面四色框始終保持。任意大小化約由紙面與明列外部依賴
承擔；Python 檢查固定必要域、完整 tuples／fibres 及具名 minors。

**共同 ε≥2；唯一 degree-6 的 ε=2 分支已全排。** 941 的 ε=1
全部分支及唯一 degree-6 的 t=0、1、2、3 全分拆見 §2 原報告。
因此 ε=2 只剩兩個完整 degree-5 roots。

| 雙 root 分支 | 最新已完成範圍 | 精確報告 |
| --- | --- | --- |
| 原 root 刪除 | 至少一個刪 root 圖全收，另一個至多缺一列；相鄰且有 mixed 時兩者均全收 | [完整 Σ 與原刪除](c5_excess_two_root_deletions.md) |
| 相鄰 mixed 的原 zw 省略 | 雙 triangle、原樹／偶數路徑與單 triangle 接回全排；Σ(G−zw)=Ω | [雙 triangle](c5_excess_two_root_deletions.md)、[原路徑](c5_excess_two_path_edge.md)、[單 triangle](c5_excess_two_triangle_edge.md) |
| 相鄰唯一 mixed 的 (4,4) q-core | 保留 mixed 的雙 spoke、spoke＋unary、雙 unary 身份及只省略 incidence-(1,1) mixed 的身份均全排 | [原身份表](c5_excess_two_mixed_core_spokes.md)、[spoke＋unary](c5_excess_two_mixed_core_spoke_unary.md)、[雙 unary](c5_excess_two_mixed_core_two_unary.md)、[mixed 省略](c5_excess_two_mixed_omission.md) |
| 相鄰唯一 mixed 的單 spoke 省略 | 省略圖若拒絕 q，自己就是唯一 degree-5 minimal q-core；同色原 spoke 身份限制三-spoke 附件 | [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md) |
| 相鄰唯一 mixed 的五-spoke 原來源 | 八份具名附件共同搬運至 998／1004；原 (b,a,y,u) joint leaf 纖維、同一 unary 雙列 palette 與原圖 K₅ 全排；兩候選總 spokes 都≤4 | [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md) |
| 四-spoke (3,1) 的 mixed-(1,1) 加兩原單接點 unary | 原 Σ-critical witnesses、b–a–框點外路徑與短支援定理迫三份原分量跨度至少六，與共同五段 lifts 矛盾，含 root 交換；288 同源支援域與完整五點 joint 核對 | [兩原 unary 的六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md) |
| 四-spoke (3,1) 的 mixed-(1,1) 加一原 binary unary | 原 star 殘留32／64份由同列 tightness／端點 hub 的二、三 hub Gallai K₅ 全排，含root交換；192原query、10,752完整U schemas與42原degree圖核對。完成這個原incidence子型，ε≥3未證 | [同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)、[原 star](c5_excess_two_mixed_core_four_spoke_star.md)、[marked-leaf](c5_excess_two_mixed_core_four_spoke_binary.md) |
| 四-spoke (3,1) 的 mixed-(1,2) 加一原單接點 unary | 同色原 spoke 省略後 M 自己 minimal；原 K=C+a 的三接點 (a,y₀,y₁) 接上既有 active-triangle K₅，全部20／60框架全排，含root交換。200 queries、50完整degree圖、1,500 joints／24,000纖維；紙面＋Python，ε≥3未證 | [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md) |
| 四-spoke (3,1) 的 mixed-(1,3) 無 unary | 原 K=C+a 的四 contacts=(a,y₀,y₁,y₂) 要求三禁色，但 marked leaf 迫至多二；原逆序貪婪直接構造 M／G 延拓，20／60 框架全排，含 root 交換。80 完整 degree 圖、2,400 joints／38,400 纖維及 2,400 貪婪 witnesses；結合前三子型完成全部 (3,1) incidence 分拆 | [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：共用 pair | 原 spoke diamond 封 C 於一個原三角形，既有三-hub 引理延拓每份合法原三角染色；接原 G−C 全收迫 G 全收，排除相同 pair 的 7／9 份，含原 01／01 與 root 交換。當輪 unequal 殘留由下列短 face 進一步收窄；36 完整 degree 圖、2,520 joints／40,320 fibres | [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：短 face | 原 01／02 的 a-side unary 只能碰 01、0 或 12；原外部路徑與短支援引理使 au 非 critical。含 root 交換及同機制 8／16 份；後續長 face 進一步收窄。74 原骨架的 7,104 rotation assignments、完整六點 joints／空纖維與原 unary witness 替換保存 | [原 unary 短 face 與非 critical 接線](c5_excess_two_mixed_core_four_spoke_short_face.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：同一長 face | 原 01／04 的 U、V 若 critical 必同在三段長 face；實際支援次序迫跨度和≤3，短支援引理迫≥4，故固定一條 unary 邊非 critical。含 root 交換及同機制 10／10 份，unequal pairs 剩 22／40；5,120 actual support pairs、120 explicit apex K₃,₃ subdivisions 與完整六角色 joints 保存 | [同一長 face 的原 unary 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：原 crosscut | 原 941 01／03、933 01／13 的 critical unary 迫原 owner-to-support crosscut，封 C 至一框點；同一外路徑及 tightness 保 degree 的二／三 hubs 使完整 C 延拓每份原外部染色，原 ax 非 critical。含 root 交換新排 8／16，unequal 剩 14／24；48 apex subdivisions、720 joints／11,520 fibres、7,752 C 替換 witnesses | [原 unary crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：共用短框弧 | 941原02／03及最後六份共用點身份用原C短支援Fempty與完整relation穩定子構造候選拒絕列01021的同框joint；963C schemas、101,115六角色tuple witnesses、1,320整圖joins／21,120fibres。當輪殘留14／18由下列完成報告全排 | [短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：不相交pairs及整型完成 | 原不相交pairs一側全短faces4／8、共同兩段長框弧10／10全部非critical，完成原47／75必要身份。2,048rotations、1,280actual支援對、60apex subdivisions與完整identity ledger；所有原C/U/V保持，其他incidence及ε≥3保留 | [原子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md) |
| 任務 A／A₂／A₃／A₄：四-spoke (2,2)、mixed-(1,2)+a 側原 unary | 原01／23、01／12、01／01、04／04及root交換來源排除。A₄重核四rotations，原C支援{0}／{4}、U含123；原互異色三hub及exact degree-list延拓完整C使ax非critical，01202的U singleton1／3均給完整joint矛盾。保存其餘16／20框架、40／58actual支援與50／84schedules；24完整degree控制、240投影等式與2,912整份C替換witnesses。紙面＋Python、整型未排、ε≥3未證 | [A 的原身份](c5_excess_two_mixed_core_four_spoke_mixed12.md)；[A₂的01／12排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)；[A₃的共用01／01排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)；[A₄的原04／04排除](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md) |
| 任務 B：四-spoke (2,2)、mixed-(2,2) 無 unary | 七份具名跨側共享身份及完整四接點／root-pair joint；四條原 spoke 省略各自 Ω，原拒絕 q-core 必是 G (5,5)。47／75 骨架各縮至25相鄰pairs，sealed triangle各排5，20／20原face必要見證保留；tightness及leaf-owner限制、28完整degree控制。任意大小紙面＋Python，未排整型、未證ε≥3 | [B 的原四接點身份與窄化約](c5_excess_two_mixed_core_four_spoke_mixed22.md) |
| B₂：mixed-(2,2) 固定原01／23短 face | W933-101／W941-139的原短face{1,2}全來源排除，七身份零殘留；Gallai leaf的四種owner各由實際外鄰及原外部路徑給K₅。完整四接點fibres保持；同骨架長face由B₃獨立涵蓋，整型保留，紙面＋Python、未Lean化 | [B₂ 原leaf／路徑提取](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md) |
| B₃：mixed-(2,2) 同骨架原長 face | W933-101／W941-139長face{0,4,3}獨立全排，七身份零殘留；shared leaf bridge由跨列slack排除，五種原leaf各以實際外部路徑給K₅。完整四接點fibre與原bridges保持；兩W的短／長faces分別證成，其他骨架及整型保留，紙面＋Python、未Lean化 | [B₃ 原長face窄引理](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md) |
| B₄：933 原04／12、shared contact附件{4} | 精確W933-129長face{2,3,4}；shared leaf在11原pairs全tight，刪leaf後13鄰點附件排5留8。原K=C−v的完整degree cut迫奇數框附件，五原bags給K₅，六shared身份／八指定選擇此支全排；40完整degree圖、2,400joins／38,400fibres。其他附件／身份及整份骨架保留，紙面＋Python、未Lean化 | [B₄ 原shared leaf／cut parity](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md) |

**停止點：(3,1) 全部四份incidence分拆封閉；(2,2)、mixed-(1,1)
加各側一原單接點unary整個子型亦封閉，含root交換。** 原47／75
具名必要身份由共用pair7／9、短face8／16、三段長face10／10、
原crosscut8／16、共用短框弧0／6及不相交pairs14／18完整覆蓋；
identity ledger核對無重複／遗漏，最後殘留0／0。
三種最新論證分清原C替換的四角色投影、原拒絕列的完整joint、
原短unary替換的五角色投影；不把六角色joint或來源Σ當作收縮不變量。
完整原relations與actualsupports保留；只替換固定短unary的整份witness，
C與另一unary外部頂點逐點保持，主張五角色投影相等。固定必要表不提供來源實現。

**任務 A／A₂／A₃／A₄ 停止於 mixed-(1,2)+a 側原 unary 的01／23、01／12、01／01、04／04來源排除，含root交換。**
原a-spoke省略及整份G−U各自Ω的ternary身份沿用A；A₂的原crosscut、
A₃的01／01四rotations／singleton2／3與18／22歷史ledger保持。
A₄重新核對原04／04及root交換：四rotations的共同C faces始終為0ab、4ab，
完整degree握手式迫actual support為{0}或{4}；完整來源支援迫U實際含123，
U長face使用a=5的indices1,2、a=6的0,3，root交換index map為[1,0,3,2]。
原a,b,h三角本來連通、三色互異，逐點exact list等於deg_C，原外部路徑
與K₄排除前提完整核對，故任意大小C皆能延拓。只替換整份原C、固定其餘
原頂點，得π_(a,b,u)J_G=π_(a,b,u)J_(G−ax)，使固定原ax非critical；
完整六角色joints不必相等。01202的原R_U={d}、d=1或3時，
取(a,b,u)=(4−d,d,d)再接出完整原joint而違反拒絕，不沿用A₃色表。
保留完整R_C(x,y₀,y₁)、R_U(u)、actual supports／原schedules及字面色框；
y₀≠y₁、x獨立或共享其中一原接點均保持。新incidence必要域70／90
經A至A₄保存16／20框架、40／58actual U支援與50／84完整schedules。
24張固定完整degree圖／30,720fibres及2,912份整份C替換witnesses只是
關係控制，不實現來源或ledger schedules。詳見[A₄報告與完整殘留](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)。
後續[盾弧預算](c5_unary_shield_budget.md)以支援連續性與 spoke 限制，將其餘actual U支援紀錄刪至24／30、schedules刪至30／50，16／20框架各仍有殘留。
原pair層停止於此；其他共用pairs與unequal入口保留。歷史提議是固定原12／12
及root交換，再逐項核對自身四rotations、原support／schedules與完整ternary。
未將04／04結果登記到其他pairs，mixed12整型與ε≥3仍未證。
A₄直接證明原入口，未用D₅來源搬運；01→04兩份幾何moves將933送至934／948、
941送至950，完整Σ、拒絕列及共同色框的診斷保持，不能當成固定mask shortcut。
933原01／13的幾何D₅搬運將Σ933送至940，原941部分身份搬至949；
所有mask／row／color／rootrole搬運均明列，不識別不同來源relations。
原rotation隨同一relabeling搬運並保持合法；完整Σ、row、共同色框、
owner角色與原分量一同搬運，不要求另行選出的canonical rotation相同。
mixed11的16份equal-pair self-identities已由[原D身份稽核](../audits/2026-10-04-task-d/REPORT.md#逐-identity-的完整性與搬運)
記錄此canonical face集差異，不能把合法搬運寫成canonical embedding字面相等。

**任務 B／B₂／B₃ 停止於 mixed-(2,2) 無 unary 的固定01／23短／長 face 分別全排。**
原 G 的每個拒絕 q-core 仍 (5,5)；B 的原20／20必要骨架證書保持歷史層。
B₂ 排 W933-101／W941-139短face{1,2}，B₃ 獨立排長face{0,4,3}，
各自七身份零殘留；因此僅這兩W的原mixed-capable faces已全部封閉。
長face的shared leaf bridge以全部拒絕列slack排除，degree二的shared
內部bridge鏈保持；nonowner 04／34、a0、b3、shared ab五leaf型的
原外部路徑完成K₅。完整C、actual附件、四接點fibres不作minor不變量。
其他骨架與faces、mixed22整型及ε≥3保留。
詳見 [B₃報告](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)、
[B₂報告](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
及 [B原身份](c5_excess_two_mixed_core_four_spoke_mixed22.md)；A的入口如上。

**B₄停止於W933-129、原933 04／12長face的指定shared-contact附件{4}全排。**
此點確有deg_C=1，全部拒絕rows的11個合法pair均tight；原鄰點
leaf刪除slack只排13必要候選中的5份，保留8份另由原cut parity關閉。
K=C−v的外接恰為剩餘兩條root接線、原bridge及n_B框邊，完整degree四
迫n_B奇數且非零；{a},{b},{v},原B,整份K給十對原鄰接的K₅。
六shared身份的八指定選擇此附件支零殘留；D4與shared空附件、其他
contact附件／短face及其他骨架均不新增排除，W933-129整份骨架仍保留。
完整C／四接點relation、root-pair fibres、shared bridges及原(5,5)q-core
保持，minor不作其不變量。不沿用B₃的min-degree二分類，亦不證ε≥3。
在此窄支停止；下一具名候選入口是同份W933-129、04／12長face{2,3,4}，
指定shared頂點的實際框附件為空集；保留原frame、七身份及全部原bridges。
此入口未分析、未排除，其他contact附件亦保持。

其他 (2,2) incidence、較少 spokes、原 unary 單省略，以及原 G 自己是
(5,5) q-core 的分支仍保留；不能套唯一 degree-5 分離定理。
相鄰多 mixed 在刪 zw 全收後的原來源、no-mixed、非相鄰雙 roots
與 unary 側例外亦保留。**單 spoke 省略尚未整型排除，ε≥3 未證。**
指定列出口不提升為完整候選排除，不重開來源圖枚舉。

本線另保留一般 connectivity、可迭代充分 state 及共同安全 repair
的缺口。固定圖成功歷程不提供跨圖常數上界；一般單側／共同出口
與 K∞=K≤5 未證，接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

A₄／B₄已由[D₅固定快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md)驗收：
A逐身份16／20及全部保留support／schedules不變；B只登記W933-129的
shared-{4}附件支，不刪骨架或長face。十二份producer兩seed byte-check、
獨立最終重播與完整scope／版本／runtime inputs見D₅包；D₄封存不改写。

正式返回A₃／B₃的固定快照與獨立驗收見[D₄整合稽核](../audits/2026-10-04-task-d4/REPORT.md)。
A₃的(a,b,u)投影等式與六角色joint不等反例分開保存；B₂＋B₃只登記
W933-101／W941-139兩primary骨架封閉，原20／20表與其他19／19原列保留。
前序[D₂](../audits/2026-10-04-task-d2/REPORT.md)的A／A₂、B／B₂覆蓋保持當輪截點，
原artifact、witnesses及所有hash／版本失敗不改寫。

任務 A 先讀 [原 unary／ternary 身份](c5_excess_two_mixed_core_four_spoke_mixed12.md)，
再讀 [A₂的01／12長／短face排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)，
接續 [A₃的共用01／01原三hub排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
及 [A₃研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-01-01.md)，
再讀[A₄的原04／04具名入口](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)
與[A₄研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-04-04.md)。最新重播：
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check`。
其餘16／20完整具名殘留、原四rotations、完整support／schedules與六角色
joint controls保存在A₄ artifact；A／A₂／A₃原artifacts保持，mixed12整型仍保留。

任務 B 先讀 [原四接點身份與窄化約](c5_excess_two_mixed_core_four_spoke_mixed22.md)
及 [B 的獨立紀錄](history/2026-10-04-excess-two-four-spoke-mixed22.md)。重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check`。
固定短 face 的接續讀 [B₂ 報告](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
及 [B₂ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check`。
同骨架長 face 讀 [B₃報告](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)
與 [B₃紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-long-face.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check`。
原933 04／12的shared-{4}支讀 [B₄報告](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)
與 [B₄紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-shared4.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check`。

前序已發布七輪的完成範圍、具名殘留、文件 hash 漂移及實際發布驗證見
[四-spoke 整理與發布紀錄](history/2026-10-03-excess-two-four-spoke-progress-publish.md)。
其後short_face、long_face、crosscut、short_arc、disjoint_pairs為另五輪
當時尚未提交成果；本批連同A／B／C及稽核封存一併發布，發布批次數不是成果總輪數。
原五輪與前置的[任務D只讀稽核](../audits/2026-10-04-task-d/REPORT.md)
保留44次check的40 PASS／4文件hash FAIL，以及兩份歷史完整payload相同的結果。
本次文件修訂、A／B新增身份／完整joint／witness覆蓋及新增hash漂移見
[D₂整合稽核](../audits/2026-10-04-task-d2/REPORT.md)與
[整理紀錄](history/2026-10-04-task-d2-integration-audit.md)。
前序九輪的完成範圍、整理發現、實際重播與貼用摘要見
[雙 root 進展整理與提交紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
最新先讀 [mixed-(1,1) 子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
與 [本輪完成紀錄](history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md)，
再讀 [共用短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)
與 [短框弧紀錄](history/2026-10-03-excess-two-four-spoke-short-arc.md)，
再讀 [原 unary crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md)
與 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-crosscut.md)，
再讀 [同一長 face 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md)
與 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-long-face.md)，
再讀 [原 unary 短 face 排除](c5_excess_two_mixed_core_four_spoke_short_face.md)
與 [短 face 紀錄](history/2026-10-03-excess-two-four-spoke-short-face.md)，
再讀 [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md)
與 [本輪研究紀錄](history/2026-10-03-excess-two-four-spoke-equal-pair.md)，
再讀 [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md)，
再讀 [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md)，
再讀 [同列端點 hub 整型排除](c5_excess_two_mixed_core_four_spoke_hubs.md)，
再讀 [原三-spoke star 扇區排除](c5_excess_two_mixed_core_four_spoke_star.md)，
再讀 [四-spoke binary 必要化約](c5_excess_two_mixed_core_four_spoke_binary.md)，
再讀 [四-spoke 六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md)，
再讀 [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md)，
再讀 [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)
與 [省略原 mixed](c5_excess_two_mixed_omission.md)；前置核心身份及
刪 root／zw 化約由 §3 報告表往回追。各輪詳細驗證保留在報告所連研究紀錄。

前序九份 checker 的歷史重播命令（本次只重跑 leaf；文件 hash 漂移另述）：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
```

原不相交pairs完成證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check`
重播，保存32原骨架全部rotations、actual支援次序／外路徑與47／75完整identity ledger。
原短框弧證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check`
重播，保存963完整C schemas、字面六角色witnesses與原拒絕列／Σ共同搬運。
原 crosscut 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check`
重播，保存 actual 原路徑、48 apex K₃,₃ subdivisions、同列 hub／degree
與完整 C 替換；四角色投影相等，六角色 joint 不相等控制分開。
同一長 face 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check`
重播，保存原身份、5,120 actual support pairs、交錯原路徑與120
apex K₃,₃ subdivisions；完整六角色 joints 與固定五角色投影替換分開。
原 unary 短 face 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check`
重播，保存完整具名框架、所有固定骨架 rotations、原短支援外路徑、
完整六角色接合及其他五角色投影的原 U witness 替換。共用 pair 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check`
重播，保存完整原 C／U／V、六點 joints、空纖維、全部 unequal-pair
具名殘留；並唯讀重算既有三-hub payload 相同。原四接點 leaf-slack 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check`
重播，保存完整四點 relations、六點 joints 及原 spanning-tree 全圖 witnesses。
原三接點身份證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check`
重播，並精確重算既有(3,1)完整payload；其獨立checker為
`PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_three_one.py --check`。
原單spoke歷史byte-check有三份既有docs hash漂移；前輪完整數學payload
已唯讀重算相同，本輪沿用該audit，詳見[原三接點身份紀錄](history/2026-10-03-excess-two-four-spoke-ternary.md)。
同列端點 hub 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check`
重播。原 star 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check`
重播，只需 Python 標準函式庫。四-spoke binary 證書另以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check`
重播。兩 unary 的原 `c5_excess_two_mixed_core_four_spoke_singles.py --check`
因 leaf 文件的一份 hash 漂移而未通過；以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_four_spoke_progress_audit.py --check`
完整重算數學 payload 及非文件 inputs，保存差異與原證書。
原 byte-check 狀態與實際沿用／重跑範圍見本次整理紀錄。

前序唯一 degree-6 分支依序讀 [t=0](c5_excess_two_no_spoke_complete.md)、
[t=3](c5_excess_two_three_spoke_complete.md)、
[t=2](c5_excess_two_two_spoke_complete.md)、
[t=1](c5_excess_two_single_spoke_complete.md) 的全分拆總報告，
再追各報告所連原省略證書、[短支援引理](c5_short_support_singleton.md)、
原首橋及末端區塊。共同下界見 [941 ε≥2](c5_941_three_spoke.md)，
minimality 前提見 [容量下界](c5_independent_support_capacity.md)。
前序實際發布範圍見 [唯一 degree-6](history/2026-10-03-excess-two-degree-six-publish.md)、
[t=2](history/2026-10-03-excess-two-two-spoke-publish.md)、
[t=1](history/2026-10-03-excess-progress-publish.md) 的紀錄；沿用證據不等於本輪重跑。

其他路線先讀 screen／座標與循環流的必要條件，再讀有序重接的一步
公式和反例；策略由 barriers 接到 repair interface。各報告列出
checker 與 artifact，使用原報告指定範圍，生成器會寫檔。
循環流驗證見 [2026-09-27 紀錄](history/2026-09-27-circulation.md)。
紙面推導、Python 固定域證書與個別 Lean 代數結果分開；未形式化平面來源排除。
