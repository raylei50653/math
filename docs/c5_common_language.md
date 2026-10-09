# C₅ 跨線結果對照與共通語言

整理：2026-10-08。依據現有導覽及下列原報告，不新增數學定理、來源分類或計算結果。
本頁是跨線比較入口；各線現況與停止點仍由 [HANDOFF](HANDOFF.md) 所列導覽維護，
歷次整合與假設見 [研究整合快照](c5_research_synthesis.md)。

**共通問題是：局部可行的選擇，能否在同一原圖、同一接線與共同色框下共同成立。**
現有結果已共享完整關係、臨界見證及原幾何的接口；一般單側／共同出口、
任意大小的 ε≥3、一般操作充分性及 `K∞=K≤5` 仍未證。

後續（2026-10-08）：[Phase B 共通引理候選分析](c5_phase_b_common_lemmas.md)
給三組精確候選、最弱已知充分前提、反例與證明義務；包含任意兩自由roots
的條件容量紙面推廣及非平面負控制，未新增目標來源排除或一般操作充分性。

## 1. 比較時固定哪些資料

「同源」指每次比較都回到同一份具名原圖；每列、每個 core、每次刪邊及替換
都記錄與它的對應。對齊顏色時，一次置換作用於整份共同染色，不能讓不同
分量或投影各自重新命名後拼接。

| 層 | 共通名稱與必留資料 | 要回答的問題 |
| --- | --- | --- |
| 關係 | **完整介面**：有序接點、完整 tuples、共同色框、指定 pinning 的 fibres（含空 fibre） | 哪些共同賦色確實有一份完整延拓？ |
| 臨界性 | **原見證**：所用拒絕列、原邊刪除染色、core 與原圖的嵌入、省略因子身份、完整 degree | 哪個原限制不可省略？預算是在哪張圖、哪一列成立？ |
| 幾何 | **原支援**：actual attachments、ownership、bridges、同一環序、外路、盾弧、可用框族 | 各份局部見證能否同時放在這份 disk 來源？ |
| 操作 | **允許上下文**：可刪的原邊、可換色的原分量、可接觸的點、觀測接點與後續操作 | 此等價能否用於這次替換及以後的步驟？ |

### 1.1 固定符號與兩種臨界性

| 名稱 | 本頁的意思 |
| --- | --- |
| `B=(b₀,…,b₄)`、`H`、`Col` | 有序 induced C₅ 外框、忽略孤立內點後的有效內部、色集 `{0,1,2,3}`。disk 要求 B 是外邊界。 |
| `Ω_B`、`Σ(G)`、`T4` | 合法 C₅ 框列、G 可延拓的完整有序框關係、使用四種顏色的框列。十列 pattern 表示與全域 S₄ 展開後的字面關係分別標明；D₅ 搬運作用於整張具名圖。 |
| **disk q-core** | 有指定有序 induced-C₅ 外框的有限簡單 disk 圖拒絕指定三色 proper 列 q，刪任一非框邊後接受 q；有效內部非空連通。這是邊集 inclusion-minimal，並非內點數最少。T4、degree 及 root 型另列。 |
| **固定 Σ 來源** | 完整 Σ 是 933／941 或其整圖 D₅ 像；指定有序 induced-C₅ disk；有效內部連通；所有有效內點完整 degree≥4；逐非框邊 **Σ-critical**。`ε=∑_{v∈H}(deg_G(v)−4)`。 |
| **Σ-critical** | 刪任一非框邊都改變完整 Σ。不同邊可以解除不同拒絕列；不保證原 G 對某一 q 已經 q-minimal。抽出的 q-core 須另核 degree、原因子及刪邊見證。 |
| **完整 degree** | 在該結論指定的整張 G 或 core M 中計算，含框附件／spokes；原 G 的 degree 與抽出 core 的 degree 分別記錄。 |
| `R_C(β)`、`F_C(β)` | 原 C 在框列 β 下、保留 C–B 附件的完整有序接點關係。對鄰接單一 root 的 C，`F_C=⋂_{t∈R_C}set(t)` 是 root 禁色；非空 R_C 的禁色數至多等於接點數。混合分量須保留共同 root-pair 關係。 |
| `J`、`𝓕`、`P` | 原觀測點集上的完整接合關係；整圖可用的具名框族；由該框族完整投影拉回後取交集所得 P。框各自可延拓不保證同一賦色屬於 J。 |
| **one-sided piece** | 移除該原 piece P 後，`H−P` 非空連通；只知道 P 連通不夠。 |

精確接合的共同前提：兩來源只共用指定兩個框點，私有內點互斥，整圖恰為
兩來源邊集聯集，沒有額外跨來源邊；具名接點與字面色框已共同對齊。
完整關係與查詢的基線見 [boundary relation](boundary_relations.md)，
兩種臨界性見 [容量報告 §1](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)。

下表單缺失等式使用十列 pattern 記法：`Ω_B∖{q}` 展開到字面染色後，
刪掉的是 q 的整個全域 S₄ 軌道。接合與 arity 的配置域則是觀測點集 S 上
的全部 `Col^S`，包含不 proper 的 tuples；共同 repair 原文的 Ω 是其指定
配置全集，不能一律解讀成合法 C₅ 框列。原報告中 U 等符號按各自定義使用。

### 1.2 結論與證據分別命名

| 結論名稱 | 可宣稱的內容 |
| --- | --- |
| **來源排除** | 明列前提的實際圖不存在；必要表沒有存活項本身仍須有任意大小化約。 |
| **存在性分離** | 指定列有某份延拓或異色 root pair；從指定 source 染色出發的 repair 操作須另證。 |
| **關係保持** | 在具名觀測接點及允許上下文上完整關係相等；固定 q、三色列、某投影及全部 Σ 分別標明。 |
| **必要預算** | 真實來源必滿足的容量／degree／跨度限制；通過限制不代表來源可實現。 |
| **有限域覆蓋／soundness** | 覆蓋指定模板或驗證提供的證書；域內 completeness、證書 soundness、一般圖 completeness 分別記錄。 |
| **操作充分性** | 明列操作及未來接觸範圍下可安全迭代；靜態 Σ／J 相等不自動提供此結論。 |

證據名稱固定使用 **紙面證明、外部定理、Python 固定域證書、Lean 普通證明、
Lean `native_decide` 證書**；同一行可以有多層，須說明各層承擔哪一步。
`lake build` 是驗證紀錄，不能代替具名 theorem 及公理範圍。

## 2. 結果／前提／共用引理／缺口／證據對照

本表的「disk q-core」及「固定 Σ 來源」均展開為 §1.1 的全部前提。
共用引理名稱由 §3 對回原文；下列結果是代表性接口，並非各線全部成果。

| 結果 | 精確前提 | 共用引理 | 剩餘缺口 | 證據類型 |
| --- | --- | --- | --- | --- |
| **Degree-4／完整單缺失**：`Σ(M)=Ω_B∖{q}` | disk q-core；接受 T4；每個有效內點在 M 中完整 degree=4 | 緊 list／Gallai 化約；完整關係接合；原附件 minor | 任意大小分類整套未 Lean 化；不直接推出一般共同出口 | 任意大小紙面＋外部 degree-choosability＋有限正常形 Python；[degree-4 導覽](c5_degree4_guide.md) |
| **Degree-5／指定來源排除**：二 odd-cycle blocks 分量，環長與外臂不限 | disk q-core 接受 T4；唯一 degree-5 root z 有三 spokes；兩內邊進入同一連通 `C=H−z`；其餘完整 degree=4；C 恰二 odd-cycle blocks、其餘 bridges | 完整接點接合及四個 z 色查詢；緊 list／Gallai 化約；保原附件的 branch sets | R31 同末端不同二接點三環鏈只有正常形；任意長來源 minor 及其他分拆／更多環仍保留 | 紙面＋外部 degree-list＋Python minor／正常形證書；Lean 僅支援接合代數，[degree-5 導覽](c5_degree5_guide.md) |
| **No-mixed／必要超額預算**：`D_r+O_r+κ_r=deg_M(r)−4`；root 骨架是樹時 κ=0 | 固定 q 的逐非框邊 minimal 圖；有序 induced B、H 非空連通；非空 root 集恰為完整 degree≥5 的內點，其餘 degree4；每份原 C 只鄰接一 root。不需 disk／T4 | 完整關係消去；原邊刪除見證；來源超額預算；樹上拒絕證書 | target p 不自動滿足同一等式；一般 root 樹的跨列分離仍未證 | 主恆等式為初等紙面，骨架推論另用外部 Gallai；Python 有限控制，未 Lean 化，[Root 預算 §1–5](c5_root_degree_excess.md) |
| **Weak-deletion／存在性分離**：`p₁=01021`、`p₂=01212` 均有異色 root pair | disk q-core，q=01012；恰兩相鄰 degree-5 roots，其餘 degree4；每份原 C 恰接一 root；保全部附件／bridges／完整關係。不需 T4，不限分量大小 | 完整關係搬運；短側弧無增長；三弧位置引理；原路徑／端點 palette 交換 | 從指定 source 染色出發的逐步 repair 未構造；mixed 與一般出口未涵蓋 | 任意大小紙面＋外部 Gallai／原路徑引理＋Python 回歸，未 Lean 化，[共同分離 §1、§4](c5_no_mixed_growth_completion.md) |
| **q-core／必要盾弧預算**：unary 弧長≥2；one-sided 弧互斥、總長≤5；至多兩份 unary | disk q-core 接受 T4；roots 為 degree≥5 內點，pieces 內點完整 degree4；unary 為 one-sided；其他計費 pieces 也須驗證 one-sided；原 q-critical 接點邊及避開自身的外路 | 盾弧共同預算；短支援 hub 原則；原邊刪除見證 | root-disconnected 分隔型不可直接套用；singleton 未接內點例外須保留；缺 criticality／degree 時廣義六邊說法有反例 | 任意大小紙面＋外部 Gallai／K₅＋Python 控制，未 Lean 化，[盾弧定理 W-A](c5_qcore_shield_budget.md#33-定理-w-aunary-長盾弧及共同五邊預算) |
| **Mixed 共鄰 P₃／來源排除**：C §1 的整個分支閉合 | disk q-core，q=01012；相鄰 degree-5 roots z,w；唯一 mixed 原 P₃=`x₀x₁x₂`，僅 x₂ 同接兩 roots，原附件數 `(3,2,1)`；其餘 degree4 unary。不需 T4／固定 Σ，unary 大小不限 | 原 P₃ 支援迫弧長≥2；原外路＋hub；C-W 的 `2+2+2>5`；D₆ 零-unary 側補證 | 更多 incidences、更大／多 mixed、一般出口未由此完成；不同接點各一 incidence 的 P₃ 已有另份排除 | 任意大小紙面＋外部 Gallai／K₅＋literal-key Python＋D₆ 稽核，未 Lean 化，[C-W 及 §8 補證](c5_qcore_shield_budget.md) |
| **完整 Σ／必要下界**：933、941 均有 ε≥2 | 固定 Σ 來源；各拒絕列的 q-core 回到同一 G，保留原單容量省略身份、完整十列與全部接線 | Degree-4 單缺失；原因子省略身份不跨拒絕列重用；共同容量及原支援預算 | ε≥3、任意 ε 來源排除及來源實現仍未證 | 任意大小紙面合成，沿用外部定理及有限證書；未新增 Lean theorem，[四容量子覆蓋](c5_excess_one_subcovers.md)、[941 收尾](c5_941_three_spoke.md) |
| **ε=2／兩-root44 身份排除**：U1–U4 及前序完成所有兩-root `(4,4)` q-core 格 | 固定 Σ 來源且 ε=2；原 G 的 Σ-critical 與 core 的 q-minimal 分開；保完整 degrees、原 contacts、全部 attachments／空 fibres；逐格採用 C44″ 前提 | 原邊省略身份；盾弧／star-face；slack 延拓；原 minor；保 roots 化約及完整 joint 接回 | `(4,5)/(5,4)`、原 `(5,5)`、單-root 例外與無44來源仍保留；E5／E6 的 G1 新證明義務仍在 | 任意大小紙面化約＋Python 固定必要域及指定獨立稽核，未 Lean 化；[C44″ 覆蓋表](../artifacts/c5_excess_two_c44pp/REPORT.md)、[最新導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口) |
| **Sector／整圖分類**：雙拒絕迫二內點原接線、十二位簽章1855，排除3903 | 有限簡單 induced-C₅ disk；全部內部 `C=K−V(B)` 非空連通；內點完整 degree≤4；b₀ 恰有兩不同內鄰點；α=01212、δ=01213 均拒絕。無須 minimality、T4 或 Kempe 歷史 | 各列拒絕迫緊 list；同圖 block palettes 與原附件的跨列相容性 | 完整分類未 Lean 化；603 profiles 未重算；十二位 sector 簽章不等於完整 Σ | 任意大小紙面＋外部 degree-list＋獨立有限主表；BoundaryDegree／TwoRejectionTools 為部分普通 Lean，[分類命題](c5_two_rejection_proof_zh.md#0-精確命題與適用範圍) |
| **兩點重疊／接合語義**：同 Σ＋具名雙射固定 J；同框族再固定 P／repairs；`r*≤d(J)≤max d(Σ)≤5` | §1.1 精確接合；非空 `J⊆P`；repair 只合取原 J 投影、無輔助變數。四階推論另需兩來源 T4 全收 | 完整關係接合；階數上界；條件式代表無關性；T4 四階引理 | J 相等不保可用框族；消去接點後及多步操作不自動有此上界；來源關係普遍四階已由 R511 否定；接合 r*=5 未由此證成 | 紙面關係代數＋132來源與六接合例 Python；未 Lean 化，[階數報告 §2–4](c5_relation_arity.md) |
| **D₁₃／關係保持**：與四輪星的完整四接點關係相等；密封替換逐份保外部染色 | 原 D₁₃ 32邊及四具名接點；九內點密封；所有外部接線只經四接點；相同 attach／outside。圖層應用另核 ownership 與可用框 | 完整四接點等價；密封上下文替換；同 J／同框族接口 | 第五接點或內點新接線超出前提；任意層來源族的具名附件與 disk 框可用性未端到端 Lean 化；改寫完備性未證 | 局部等價及替換有普通 Lean；來源族與框拓撲另為紙面＋Python，[SealedFourPort](lean_sealed_four_port.md)、[D₁₃ 來源族](c5_two_vertex_repair_caps.md) |
| **State／指定 grammar 正常形**：`AnnulusAccept w ↔ ∃ s, s.Valid ∧ s.word=w` | 固定原有 C₅＋triangle attachment grammar、五個具名框點次序；w 為原 grammar 的有序 attachment packets | 附件正常形以同一旋轉 necklace 切段，保 orientation、環序及每段 Nodup；完整關係查詢與接合 | embedding 抽取及 topology soundness 未 Lean 化；grammar 外、一般 context／future 充分性未證；87 states 與132來源類不同域 | normal form／endpoint-order 編譯有普通 Lean；topology 是紙面及外部拓撲事實；relation 庫為固定域計算，[正常形](attachment_normal_form.md)、[State 導覽](c5_state_guide.md) |
| **Lean／指定 repair 分類**：兩具名核心各15組極小 repairs、唯一最少對、r*=4 | 固定兩十五點35邊核心、原八點次序；J 由原圖染色定義；P 用指定兩混合框；70個四點 scopes；repair 只合取原 J 投影 | 完整 J 延拓 iff；repair iff 覆蓋完整差集；W／C 判準及全部候選條件的 exact witness rejectors | 指定兩框的 disk 可用框完備性、D₁₃ 任意層來源族與同圖換色操作未由此形式化 | CommonRepair／NamedRepair **普通 Lean**（kernel `decide`）；拓撲另為紙面／Python，[NamedRepair](lean_named_repair.md) |
| **LC／固定證書 soundness**：提供的179個 ES 代表均有具名證書 | ES 的179份 literal labelled JSON，NA／AD／D6、k≤9；固定邊、degree profile、完整染色列、刪邊 witnesses 及來源 hashes | 原圖與原刪邊 witness 逐邊核對；完整關係的 S₄ cover | 枚舉 completeness、軌道互異、拓撲 disk 實現及任意大小分類未 Lean 化 | 接受列／刪邊 witness 的 kernel 證明；拒絕列用 **native_decide**；raw Σ equality 另繼承 S₄ cover 的 native 公理，[LC 報告](c5_excess_two_lean_certificates.md) |

## 3. 共用引理的固定叫法

以下名稱是既有引理的共同索引；同名機制下的各版本仍使用各自原前提。
「有相同機制」不表示已有一條涵蓋所有研究線的定理。

| 固定叫法 | 精確接口／使用邊界 | 原入口 |
| --- | --- | --- |
| **完整關係接合** | 保共同變數與色框，先 joint／intersection，再投影。原分量完整 tuples 在同一 root 賦色下選 witness；兩來源須無額外共用私有點／跨邊。 | [Root 消去 §1](c5_root_degree_excess.md#1-同一來源上的完整消去)、[兩來源公式 §2](c5_relation_arity.md#2-接合的紙面上界與代表無關性) |
| **原邊刪除見證／省略身份** | q-critical 邊的刪邊染色給同圖拒絕見證；Σ-critical 須先指定它解除哪列。比較不同列時保同一原 factor；因子省略與單邊刪除的等價要另證。 | [Root minimality §2](c5_root_degree_excess.md#2-minimality-提供的三個前提)、[四容量子覆蓋 §1](c5_excess_one_subcovers.md#1-同源因子真子核心與省略區域) |
| **緊 list／Gallai 化約** | 實際全部外鄰定義剩餘 lists，待處理分量每點完整 degree≤4 提供 list 大小≥內度；連通／拒絕迫緊及 Gallai blocks。Degree-5 應用先將 root 放外部並固定顏色；degree-choosability 為外部依賴。 | [Degree-4 合成](c5_degree4_guide.md)、[Sector lists](c5_two_rejection_proof_zh.md#1-拒絕列使所有-lists-緊並得到-block-palettes)、[Lean BoundaryDegree](lean_boundary_degree.md) |
| **來源超額預算** | `D` 是原接點容量缺額，`O` 是同 root 禁色重疊量，`κ` 是骨架 list 缺額；`D+O+κ=degree−4` 是 source q 的恆等式，κ 不是環數。 | [定義及恆等式](c5_root_degree_excess.md#3-degree-超額的精確-source-預算) |
| **盾弧共同預算** | 同一原環序、one-sided、原外路及 critical 見證給各弧下界，互斥後才可相加。q-core「盾弧定理 W-A」需 T4；共鄰 P₃「C-W」以原 P₃ 外路替代，無須 T4。 | [W-A／C-W](c5_qcore_shield_budget.md)、[來源盾弧版本](c5_unary_shield_budget.md) |
| **原外路＋hub minor** | 對平面圖中完整 degree4 的連通 P，先有不能接回 P 的外部染色；原外路構造至多四個連通、互斥、兩兩相鄰 hubs，覆蓋 N(P)；各 hub 在 N(P) 上常色且常色互異。同列 tightness 保收縮後 degree。Minor 反證不自動提供 Σ 保持，關係保持另依密封替換。 | [短支援 hub](c5_short_support_singleton.md)、[hub 原則定理 B](c5_unary_shield_budget.md#4-定理-bhub-原則) |
| **同源色交換／完整纖維** | 整份原分量的染色與附件共同搬運；未見色交換不變性、端點 tightness 或 slack 必須在所用列重證。不能把 source 禁色硬傳到 target。 | [搬運接口](c5_no_mixed_hypothesis_audit.md)、[共同分離](c5_no_mixed_growth_completion.md)、[U4 完整接回](c5_excess_two_nonadjacent_two_mixed_core44.md) |
| **密封上下文替換** | 具名接點完整關係相等、同 attach、同 outside、內點無額外接線，便保持全部外部染色。接回真實 disk 圖仍核 ownership、環序及可用框。 | [sealed_congr／cap_sealed_replacement](lean_sealed_four_port.md#2-密封內點與任意外部上下文) |
| **同 J／同框族的 repair 保持** | 同來源 Σ 及具名雙射固定 J；另證同可用框族才固定 P／repairs。W／C witness 的 rejectors 必須相對全部候選條件精確相等。 | [代表無關性](c5_relation_arity.md#2-接合的紙面上界與代表無關性)、[共同 repair 判準](c5_two_vertex_common_repair.md) |

**名稱消歧：**「盾弧定理 W-A」是長弧及五邊預算；「repair witness W_A」
是共同 repair 判準的一個 exact-rejector 見證，兩者不共用同一數學陳述。
另外，no-mixed 的 `m+s+a≤5`、盾弧的 `Σ|σ_P|≤5`、來源階數 `d(Σ)≤5`
分別計框弧成本、框邊長度及觀測接點數；不能互換或跨列加總。

## 4. 用這套語言記錄下一份結果

每份結果用同一個句型，並保留上述五欄：

> 在【具名圖類、臨界性、完整 degree、原分量身份及允許上下文】下，保留
> 【觀測接點、完整關係／fibres、附件及原幾何】，由【具名引理及其版本】得到
> 【結論類型、量詞及適用列】。證據為【各層實際承擔的步驟】；仍缺【下一義務】。

共通語言的兩個直接用法：

- **跨線搬引理：**先核原分量身份、critical 刪邊 witness、degree、one-sided
  與避開自身的外路，再搬盾弧下界；不能只因都有 unary 就套同一結論。
- **跨代表搬結果：**先證具名完整 Σ／J 保持，再證可用框族保持；若要多步使用，
  再明列未來可接觸點與操作。這三項義務分別記錄完成或未證。

## 5. 本次依據與驗證範圍

本次只核對各線導覽與表中原報告，新增分類及名稱索引；沒有重跑研究枚舉、
Python 數學證書、Lean build 或公理審計。表中證據描述沿用原報告，具名
theorem／script／artifact 與重播命令由各連結入口維護。

本次文件檢查命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

實際結果：文件連結／錨點／索引檢查通過（583份 Markdown、6909個本地連結）；
正式 docs 的 DocGraph 通過（62份 metadata 文件、213條關係）；`git diff --check` 通過。
預設全工作樹 DocGraph 未通過：保留的 `scratch/task-c44-delivery/repository`
副本與正式 docs 重複62個 ID。文件檢查不驗證數學結論。
